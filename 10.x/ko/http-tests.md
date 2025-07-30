# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade와 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어설션](#available-assertions)
    - [응답 어설션](#response-assertions)
    - [인증 어설션](#authentication-assertions)
    - [밸리데이션(유효성 검증) 어설션](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 아래 정의된 기능 테스트를 살펴보세요:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 반환된 응답이 주어진 HTTP 상태 코드를 가져야 함을 어설트합니다. 이 간단한 어설션 외에도, Laravel은 응답 헤더, 콘텐츠, JSON 구조 등 다양한 부분을 검사할 수 있는 여러 어설션을 포함하고 있습니다.

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

애플리케이션에 요청을 보내기 위해 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 호출할 수 있습니다. 이 메서드들은 실제 네트워크 요청을 보내지 않고 내부적으로 요청 전체를 시뮬레이션합니다.

이 메서드들은 `Illuminate\Http\Response` 인스턴스를 반환하지 않고 `Illuminate\Testing\TestResponse` 인스턴스를 반환하며, 이는 애플리케이션 응답을 검사할 수 있는 [다양한 유용한 어설션](#available-assertions)을 제공합니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제.
     */
    public function test_a_basic_request(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

일반적으로 각 테스트는 애플리케이션에 하나의 요청만 만들어야 합니다. 하나의 테스트 메서드 내에서 여러 요청을 실행하면 예상치 못한 동작이 발생할 수 있습니다.

> [!NOTE]  
> 편의를 위해, 테스트 실행 시 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징 (Customizing Request Headers)

`withHeaders` 메서드를 사용하면 요청이 애플리케이션에 전송되기 전에 요청 헤더를 커스터마이징할 수 있습니다. 이 메서드는 원하는 커스텀 헤더를 요청에 추가할 수 있게 합니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제.
     */
    public function test_interacting_with_headers(): void
    {
        $response = $this->withHeaders([
            'X-Header' => 'Value',
        ])->post('/user', ['name' => 'Sally']);

        $response->assertStatus(201);
    }
}
```

<a name="cookies"></a>
### 쿠키 (Cookies)

요청 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie` 메서드는 쿠키 이름과 값을 각각 인수로 받으며, `withCookies` 메서드는 이름/값 쌍의 배열을 받습니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_cookies(): void
    {
        $response = $this->withCookie('color', 'blue')->get('/');

        $response = $this->withCookies([
            'color' => 'blue',
            'name' => 'Taylor',
        ])->get('/');
    }
}
```

<a name="session-and-authentication"></a>
### 세션 / 인증 (Session / Authentication)

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용하여 세션 데이터를 배열로 미리 설정할 수 있습니다. 이는 요청을 발생시키기 전에 세션에 데이터를 넣고 싶을 때 유용합니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session(): void
    {
        $response = $this->withSession(['banned' => false])->get('/');
    }
}
```

Laravel 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 주어진 사용자를 현재 인증된 사용자로 간단히 인증시키는 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/10.x/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_an_action_that_requires_authentication(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
                         ->withSession(['banned' => false])
                         ->get('/');
    }
}
```

`actingAs` 메서드의 두 번째 인자로 가드 이름을 지정하여 특정 가드를 이용해 사용자를 인증할 수도 있습니다. 이때 지정한 가드는 테스트가 진행되는 동안 기본 가드로 설정됩니다:

```php
$this->actingAs($user, 'web');
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

애플리케이션으로 테스트 요청을 한 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 검사하고 디버깅할 수 있습니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dumpHeaders();

        $response->dumpSession();

        $response->dump();
    }
}
```

또는 `dd`, `ddHeaders`, `ddSession` 메서드를 사용하면 응답 정보를 덤프한 후 실행을 중지할 수 있습니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->ddHeaders();

        $response->ddSession();

        $response->dd();
    }
}
```

<a name="exception-handling"></a>
### 예외 처리 (Exception Handling)

애플리케이션이 특정 예외를 던지는지 테스트하고 싶을 때가 있습니다. Laravel의 예외 핸들러가 해당 예외를 잡아서 HTTP 응답으로 되돌려주는 것을 방지하려면, 요청 전에 `withoutExceptionHandling` 메서드를 호출할 수 있습니다:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, 애플리케이션이 PHP나 사용하는 라이브러리에 의해 더 이상 사용되지 않는(deprecated) 기능을 사용하고 있지 않음을 확인하려면 `withoutDeprecationHandling` 메서드를 요청 전에 호출할 수 있습니다. 이 모드에서는 더 이상 사용되지 않는 기능에 대한 경고가 예외로 변환되어 테스트가 실패하도록 합니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드로는 특정 클로저 내 코드가 특정 타입의 예외를 던지는지 어설션할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API 및 그 응답을 테스트하기 위한 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용해 다양한 HTTP 동사로 JSON 요청을 만들 수 있으며, 데이터와 헤더를 손쉽게 전달할 수 있습니다. 시작하려면, `/api/user`에 `POST` 요청을 보내고 예상 JSON 데이터가 반환되는지 검사하는 테스트를 작성해 봅시다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제.
     */
    public function test_making_an_api_request(): void
    {
        $response = $this->postJson('/api/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJson([
                'created' => true,
            ]);
    }
}
```

또한 JSON 응답 데이터는 응답 객체에서 배열 변수처럼 접근할 수 있어 JSON 응답 내 개별 값을 손쉽게 검사할 수 있습니다:

```php
$this->assertTrue($response['created']);
```

> [!NOTE]  
> `assertJson` 메서드는 응답을 배열로 변환하고 `PHPUnit::assertArraySubset`를 사용해 주어진 배열이 애플리케이션이 반환한 JSON 응답 내에 존재하는지 검증합니다. 따라서 JSON 응답에 다른 속성이 있더라도 주어진 조각이 존재하면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어설션 (Asserting Exact JSON Matches)

앞에서 언급한 `assertJson`은 JSON 내 일부 조각이 존재하는지 검증합니다. 만약 애플리케이션이 반환한 JSON이 주어진 배열과 **정확하게 일치하는지** 검증하고 싶다면 `assertExactJson` 메서드를 사용하세요:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제.
     */
    public function test_asserting_an_exact_json_match(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertExactJson([
                'created' => true,
            ]);
    }
}
```

<a name="verifying-json-paths"></a>
#### JSON 경로 어설션 (Asserting on JSON Paths)

JSON 응답의 특정 경로에 주어진 데이터가 있는지 검증하고 싶으면 `assertJsonPath` 메서드를 사용하세요:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제.
     */
    public function test_asserting_a_json_paths_value(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJsonPath('team.owner.name', 'Darian');
    }
}
```

`assertJsonPath` 메서드는 클로저도 인자로 받을 수 있어서, 동적으로 어설션 성공 여부를 판단할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트 (Fluent JSON Testing)

Laravel은 JSON 응답을 더욱 아름답고 직관적으로 테스트하는 방법을 제공합니다. `assertJson` 메서드에 클로저를 전달하면, 해당 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인자로 받아 테스트할 수 있습니다. `where` 메서드는 JSON의 특정 속성에 대한 어설션을, `missing` 메서드는 해당 속성이 JSON에 없음을 어설션합니다:

```php
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * 기본 기능 테스트 예제.
 */
public function test_fluent_json(): void
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                 ->where('name', 'Victoria Faith')
                 ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                 ->whereNot('status', 'pending')
                 ->missing('password')
                 ->etc()
        );
}
```

#### `etc` 메서드 이해하기

위 예시에서 `etc` 메서드를 체인 마지막에 호출한 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 다른 속성들이 있을 수 있음을 Laravel에 알립니다. 만약 `etc` 메서드를 호출하지 않으면, 어설션하지 않은 다른 속성이 존재할 경우 테스트가 실패합니다.

이 동작은 JSON 응답에 민감한 정보를 의도치 않게 포함시키는 것을 방지하기 위한 것입니다. 속성에 대해 명시적으로 어설션을 하거나, `etc` 메서드로 추가 속성을 허용하도록 해야 합니다.

다만 주의할 점은 `etc` 메서드가 호출된 깊이에서만 추가 속성 존재를 허용할 뿐, 중첩된 배열 안의 추가 속성까지 통제하는 것은 아닙니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어설션 (Asserting Attribute Presence / Absence)

속성이 존재하는지 혹은 없는지 어설션하려면 `has`와 `missing` 메서드를 사용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
         ->missing('message')
);
```

또한, 여러 속성에 대해 동시에 확인하려면 `hasAll`과 `missingAll` 메서드를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
         ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드는 주어진 여러 속성 중 적어도 하나가 존재하는지 확인할 때 씁니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
         ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어설션 (Asserting Against JSON Collections)

종종 경로가 여러 항목을 담은 JSON 컬렉션(예: 여러 사용자)을 반환합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이때 유창한 JSON 객체의 `has` 메서드를 이용해 사용자 개수를 어설션할 수 있습니다. 그리고 `first` 메서드를 사용해 컬렉션의 첫 번째 객체에 대한 어설션을 체인 할 수 있습니다. `first`는 또 다른 `AssertableJson` 인스턴스를 받아 첫 아이템에 대해 테스트할 수 있게 합니다:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
             ->first(fn (AssertableJson $json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어설션 범위 지정 (Scoping JSON Collection Assertions)

경로가 명명된 키로 할당된 JSON 컬렉션을 반환하는 경우가 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
});
```

이런 경우 `has` 메서드로 컬렉션 내 항목 개수를 어설션할 수 있고, 클로저를 인자로 전달해 어설션 체인을 범위(scope) 지정할 수 있습니다:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3)
             ->has('users.0', fn (AssertableJson $json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

또한, `users` 컬렉션에 대해 별도의 `has` 호출 없이 세 번째 인자로 클로저를 주면, 첫 번째 항목에 대해 자동으로 범위 체인이 구성됩니다:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3, fn (AssertableJson $json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="asserting-json-types"></a>
#### JSON 타입 어설션 (Asserting JSON Types)

JSON 응답 내 속성이 특정 타입인지 어설션 하고 싶을 때가 있습니다. `Illuminate\Testing\Fluent\AssertableJson` 클래스는 `whereType`과 `whereAllType` 메서드를 제공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
         ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`whereType`의 두 번째 인자로 `|` 구분자 또는 배열로 여러 타입을 지정할 수 있습니다. 응답 값이 나열된 타입 중 하나이면 어설션 성공으로 간주합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
         ->whereType('id', ['string', 'integer'])
);
```

지원하는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null`입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드는 테스트용 가짜 파일이나 이미지를 생성하는 기능을 제공합니다. 이는 `Storage` 파사드의 `fake` 메서드와 결합해 파일 업로드 테스트를 간단하게 만듭니다. 예를 들어, 아바타 업로드 폼 테스트는 다음과 같이 작성할 수 있습니다:

```php
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_avatars_can_be_uploaded(): void
    {
        Storage::fake('avatars');

        $file = UploadedFile::fake()->image('avatar.jpg');

        $response = $this->post('/avatar', [
            'avatar' => $file,
        ]);

        Storage::disk('avatars')->assertExists($file->hashName());
    }
}
```

또한, 특정 파일이 존재하지 않음을 검증할 때는 `assertMissing` 메서드를 사용하면 됩니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징 (Fake File Customization)

`UploadedFile`의 `fake` 메서드로 파일을 생성할 때, 너비, 높이, 크기(킬로바이트 단위)를 지정해 애플리케이션의 밸리데이션 규칙을 보다 정밀하게 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지뿐 아니라 다른 타입 파일도 `create` 메서드로 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요할 경우 MIME 타입을 명시할 수도 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 HTTP 요청 없이도 뷰를 렌더링할 수 있는 기능을 제공합니다. 테스트 내에서 `view` 메서드를 호출해 뷰 이름과 선택적인 데이터 배열을 전달하세요. 이 메서드는 `Illuminate\Testing\TestView` 인스턴스를 반환하며, 이를 통해 뷰 내용에 대해 편리한 어설션을 할 수 있습니다:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_a_welcome_view_can_be_rendered(): void
    {
        $view = $this->view('welcome', ['name' => 'Taylor']);

        $view->assertSee('Taylor');
    }
}
```

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`와 같은 어설션 메서드를 제공합니다.

필요하다면 `TestView` 인스턴스를 문자열로 변환해 렌더링된 뷰의 원시 콘텐츠를 얻을 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유 (Sharing Errors)

일부 뷰는 [Laravel이 제공하는 전역 에러 백](/docs/10.x/validation#quick-displaying-the-validation-errors)에 공유된 에러를 필요로 합니다. 에러 메시지로 에러 백을 채우려면 `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade와 컴포넌트 렌더링 (Rendering Blade and Components)

필요에 따라, `blade` 메서드를 사용하여 원시 [Blade](/docs/10.x/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로 `blade`는 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/10.x/blade#components)를 평가하고 렌더링하려면 `component` 메서드를 사용하세요. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

<a name="response-assertions"></a>
### 응답 어설션 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 중 이용할 수 있는 다양한 커스텀 어설션 메서드를 제공합니다. 이들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드들의 반환 응답 객체에서 호출할 수 있습니다.

<div class="collection-method-list" markdown="1">

[assertAccepted](#assert-accepted)  
[assertBadRequest](#assert-bad-request)  
[assertConflict](#assert-conflict)  
[assertCookie](#assert-cookie)  
[assertCookieExpired](#assert-cookie-expired)  
[assertCookieNotExpired](#assert-cookie-not-expired)  
[assertCookieMissing](#assert-cookie-missing)  
[assertCreated](#assert-created)  
[assertDontSee](#assert-dont-see)  
[assertDontSeeText](#assert-dont-see-text)  
[assertDownload](#assert-download)  
[assertExactJson](#assert-exact-json)  
[assertForbidden](#assert-forbidden)  
[assertFound](#assert-found)  
[assertGone](#assert-gone)  
[assertHeader](#assert-header)  
[assertHeaderMissing](#assert-header-missing)  
[assertInternalServerError](#assert-internal-server-error)  
[assertJson](#assert-json)  
[assertJsonCount](#assert-json-count)  
[assertJsonFragment](#assert-json-fragment)  
[assertJsonIsArray](#assert-json-is-array)  
[assertJsonIsObject](#assert-json-is-object)  
[assertJsonMissing](#assert-json-missing)  
[assertJsonMissingExact](#assert-json-missing-exact)  
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)  
[assertJsonPath](#assert-json-path)  
[assertJsonMissingPath](#assert-json-missing-path)  
[assertJsonStructure](#assert-json-structure)  
[assertJsonValidationErrors](#assert-json-validation-errors)  
[assertJsonValidationErrorFor](#assert-json-validation-error-for)  
[assertLocation](#assert-location)  
[assertMethodNotAllowed](#assert-method-not-allowed)  
[assertMovedPermanently](#assert-moved-permanently)  
[assertContent](#assert-content)  
[assertNoContent](#assert-no-content)  
[assertStreamedContent](#assert-streamed-content)  
[assertNotFound](#assert-not-found)  
[assertOk](#assert-ok)  
[assertPaymentRequired](#assert-payment-required)  
[assertPlainCookie](#assert-plain-cookie)  
[assertRedirect](#assert-redirect)  
[assertRedirectContains](#assert-redirect-contains)  
[assertRedirectToRoute](#assert-redirect-to-route)  
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)  
[assertRequestTimeout](#assert-request-timeout)  
[assertSee](#assert-see)  
[assertSeeInOrder](#assert-see-in-order)  
[assertSeeText](#assert-see-text)  
[assertSeeTextInOrder](#assert-see-text-in-order)  
[assertServerError](#assert-server-error)  
[assertServiceUnavailable](#assert-server-unavailable)  
[assertSessionHas](#assert-session-has)  
[assertSessionHasInput](#assert-session-has-input)  
[assertSessionHasAll](#assert-session-has-all)  
[assertSessionHasErrors](#assert-session-has-errors)  
[assertSessionHasErrorsIn](#assert-session-has-errors-in)  
[assertSessionHasNoErrors](#assert-session-has-no-errors)  
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)  
[assertSessionMissing](#assert-session-missing)  
[assertStatus](#assert-status)  
[assertSuccessful](#assert-successful)  
[assertTooManyRequests](#assert-too-many-requests)  
[assertUnauthorized](#assert-unauthorized)  
[assertUnprocessable](#assert-unprocessable)  
[assertUnsupportedMediaType](#assert-supported-media-type)  
[assertValid](#assert-valid)  
[assertInvalid](#assert-invalid)  
[assertViewHas](#assert-view-has)  
[assertViewHasAll](#assert-view-has-all)  
[assertViewIs](#assert-view-is)  
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 잘못된 요청(HTTP 400) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertBadRequest();
```

<a name="assert-accepted"></a>
#### assertAccepted

응답이 수락됨(HTTP 202) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertAccepted();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 충돌(HTTP 409) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 주어진 쿠키가 포함되었는지 어설션합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 주어진 쿠키가 포함되어 있고 만료된 상태인지 어설션합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 주어진 쿠키가 포함되어 있으며 만료되지 않은 상태인지 어설션합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 주어진 쿠키가 포함되어 있지 않은지 어설션합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 HTTP 201 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

주어진 문자열이 애플리케이션이 반환한 응답에 포함되어 있지 않은지 어설션합니다. 두 번째 인자로 `false`를 주면 자동 이스케이프가 해제됩니다:

```php
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

주어진 문자열이 응답 텍스트에 포함되어 있지 않은지 어설션합니다. 두 번째 인자로 `false`를 주면 자동 이스케이프가 해제됩니다. 응답 내용은 PHP 함수 `strip_tags`에 전달되어 태그가 제거된 후 검사됩니다:

```php
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 다운로드용인지 어설션합니다. 보통 `Response::download`, `BinaryFileResponse`, `Storage::download` 응답일 때 해당합니다:

```php
$response->assertDownload();
```

특정 파일명으로 다운로드되는지 검사하려면 파일명을 인자로 전달하세요:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답에 주어진 JSON 데이터가 정확히 일치하는지 어설션합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 금지됨(HTTP 403) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 리다이렉트(HTTP 302) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 사라짐(HTTP 410) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 주어진 헤더와 값이 있는지 어설션합니다:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 주어진 헤더가 없는지 어설션합니다:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 내부 서버 오류(HTTP 500) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 주어진 JSON 데이터가 포함되어 있는지 어설션합니다:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메서드는 응답을 배열로 변환하고 `PHPUnit::assertArraySubset`를 이용해 주어진 배열이 JSON 응답 내에 존재하는지 확인합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON이 주어진 키에서 기대하는 아이템 개수를 가진 배열인지 어설션합니다:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 JSON 내 어디에든 주어진 JSON 데이터가 포함되어 있는지 어설션합니다:

```php
Route::get('/users', function () {
    return [
        'users' => [
            [
                'name' => 'Taylor Otwell',
            ],
        ],
    ];
});

$response->assertJsonFragment(['name' => 'Taylor Otwell']);
```

<a name="assert-json-is-array"></a>
#### assertJsonIsArray

응답 JSON이 배열인지 어설션합니다:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 어설션합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 주어진 JSON 데이터가 포함되어 있지 않은지 어설션합니다:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 주어진 JSON이 **정확히** 포함되어 있지 않은지 어설션합니다:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 주어진 키에 대한 JSON 밸리데이션 에러가 없는지 어설션합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]  
> 더 일반적인 [assertValid](#assert-valid) 메서드는 JSON으로 반환된 밸리데이션 에러가 없고 세션에 플래시된 에러가 없음을 어설션합니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답에 주어진 경로에 해당하는 값이 기대값과 일치하는지 어설션합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 다음 JSON 응답이 반환된다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 객체의 `name` 속성이 특정 값인지 다음과 같이 검사합니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 주어진 경로가 존재하지 않는지 어설션합니다:

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 위의 JSON 응답에 `user.email` 속성이 없는지 검사하려면:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 주어진 JSON 구조를 가지는지 어설션합니다:

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 다음 JSON 응답이 반환되면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래와 같이 구조가 일치하는지 검사할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

만약 JSON 응답이 객체 배열로 이루어진 경우:

```json
{
    "user": [
        {
            "name": "Steve Schoger",
            "age": 55,
            "location": "Earth"
        },
        {
            "name": "Mary Schoger",
            "age": 60,
            "location": "Earth"
        }
    ]
}
```

`*` 문자를 사용해 배열 내 모든 객체에 대해 구조를 어설션할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        '*' => [
             'name',
             'age',
             'location'
        ]
    ]
]);
```

<a name="assert-json-validation-errors"></a>
#### assertJsonValidationErrors

응답이 JSON 밸리데이션 에러를 주어진 키에 대해 포함하는지 어설션합니다. 이 메서드는 밸리데이션 에러가 JSON 구조로 반환된 경우에 사용합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]  
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON 반환 또는 세션 플래시된 밸리데이션 에러가 존재함을 어설션합니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

주어진 키에 대해 JSON 밸리데이션 에러가 존재하는지 어설션합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 허용되지 않은 메서드(HTTP 405) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 영구 이동(HTTP 301) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답 헤더 `Location`에 주어진 URI가 포함되어 있음을 어설션합니다:

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

주어진 문자열이 응답 콘텐츠와 일치하는지 어설션합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 주어진 HTTP 상태 코드이고 콘텐츠가 없는지 어설션합니다:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

주어진 문자열이 스트리밍된 응답 콘텐츠와 일치하는지 어설션합니다:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 찾을 수 없음(HTTP 404) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 성공(HTTP 200) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 결제 필요(HTTP 402) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 주어진 암호화되지 않은 쿠키가 포함되었는지 어설션합니다:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 주어진 URI로 리다이렉트하는지 어설션합니다:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 주어진 문자열을 포함하는 URI로 리다이렉트하는지 어설션합니다:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 주어진 [이름이 지정된 라우트](/docs/10.x/routing#named-routes)로 리다이렉트하는지 어설션합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 주어진 [서명된 라우트](/docs/10.x/urls#signed-urls)로 리다이렉트하는지 어설션합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 요청 시간 초과(HTTP 408) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

주어진 문자열이 응답에 포함되어 있는지 어설션합니다. 두 번째 인자를 `false`로 하면 자동 이스케이프가 해제됩니다:

```php
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

주어진 문자열들이 응답 내에 순서대로 포함되어 있는지 어설션합니다. 두 번째 인자를 `false`로 하면 자동 이스케이프가 해제됩니다:

```php
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

주어진 문자열이 응답 텍스트 내에 포함되어 있는지 어설션합니다. 두 번째 인자를 `false`로 하면 자동 이스케이프가 해제됩니다. 응답 텍스트는 `strip_tags` 함수로 태그가 제거된 뒤 검사됩니다:

```php
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

주어진 문자열들이 응답 텍스트 내에 순서대로 포함되어 있는지 어설션합니다. 두 번째 인자를 `false`로 하면 자동 이스케이프가 해제됩니다. 응답 텍스트는 `strip_tags`로 태그가 제거된 뒤 검사됩니다:

```php
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 오류(HTTP 500 이상 600 미만) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertServerError();
```

<a name="assert-server-unavailable"></a>
#### assertServiceUnavailable

응답이 서비스 불가(HTTP 503) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션이 주어진 데이터를 포함하는지 어설션합니다:

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인자로 클로저를 전달해, 클로저 반환값이 `true`인 경우 어설션이 통과하도록 할 수 있습니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션 플래시 입력 배열에 주어진 값이 있는지 어설션합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인자에 클로저를 전달해 조건을 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 주어진 키/값 배열 전체가 존재하는지 어설션합니다:

```php
$response->assertSessionHasAll(array $data);
```

예를 들어 세션에 `name`과 `status` 키가 있고 각각 아래 값인지 어설션하려면:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 주어진 키에 대한 에러가 존재하는지 어설션합니다. `$keys`가 연관 배열이면 각 필드별 특정 에러 메시지도 어설션합니다. 이 메서드는 밸리데이션 에러가 세션에 플래시 되는 라우트 테스트에 적합합니다:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어 `name`과 `email` 필드에 세션 플래시된 밸리데이션 에러가 있는지 검사하려면:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드에 특정 에러 메시지가 포함되어 있는지도 확인할 수 있습니다:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]  
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON 또는 세션 플래시에 대한 밸리데이션 에러 존재를 어설션합니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [에러 백](/docs/10.x/validation#named-error-bags)에서 주어진 키에 대한 에러가 존재하는지 어설션합니다. `$keys`가 연관 배열이면 각 필드별 에러 메시지 또한 검사합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 밸리데이션 에러가 존재하지 않는지 어설션합니다:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

주어진 키에 대한 밸리데이션 에러가 세션에 존재하지 않는지 어설션합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]  
> [assertValid](#assert-valid) 메서드는 JSON 및 세션 플래시 밸리데이션 에러가 없음을 포괄적으로 어설션합니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 주어진 키가 없는지 어설션합니다:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 주어진 HTTP 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답 상태 코드가 성공 범위(>= 200, < 300)인지 어설션합니다:

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 요청 수 초과(HTTP 429) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 권한 없음(HTTP 401) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 처리할 수 없음(HTTP 422) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 지원하지 않는 미디어 타입(HTTP 415) 상태 코드를 가졌는지 어설션합니다:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

주어진 키에 대해 밸리데이션 에러가 없음을 어설션합니다. JSON으로 반환된 에러 또는 세션 플래시에 대한 검증 모두 가능:

```php
// 밸리데이션 에러가 전혀 없음을 어설션...
$response->assertValid();

// 주어진 키들에 에러가 없음 어설션...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

주어진 키에 대해 밸리데이션 에러가 있음을 어설션합니다. JSON 반환 또는 세션 플래시 에러 모두 가능:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 특정 밸리데이션 에러 메시지를 포함하는지도 검사할 수 있습니다. 전체 메시지 혹은 일부만 제공해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰가 주어진 데이터를 포함하는지 어설션합니다:

```php
$response->assertViewHas($key, $value = null);
```

클로저 전달로 특정 데이터에 대해 조건을 검사할 수도 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

뷰 데이터를 배열 변수처럼 접근해 검사할 수도 있습니다:

```php
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 주어진 데이터 집합이 모두 존재하는지 어설션합니다:

```php
$response->assertViewHasAll(array $data);
```

다음처럼 키만 지정해 데이터 존재 여부를 확인할 수 있고:

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

키와 값 쌍으로 정확한 데이터 값을 어설션할 수도 있습니다:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

주어진 뷰가 라우트에 의해 반환되었는지 어설션합니다:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

주어진 키의 뷰 데이터가 반환된 뷰에서 누락되었는지 어설션합니다:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어설션 (Authentication Assertions)

Laravel은 애플리케이션 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 어설션을 제공합니다. 이들은 `Illuminate\Testing\TestResponse`가 아닌 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 어설션합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지 어설션합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 어설션합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 밸리데이션 어설션 (Validation Assertions)

Laravel은 요청 데이터가 유효(valid)했는지 또는 유효하지 않았는지 검증할 수 있는 주요 밸리데이션 어설션 두 가지를 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 주어진 키에 대한 밸리데이션 에러가 없음을 어설션합니다. JSON 반환 또는 세션 플래시 모두 가능합니다:

```php
// 밸리데이션 에러가 없음을 어설션...
$response->assertValid();

// 특정 키들에 에러가 없음을 어설션...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 주어진 키에 대해 밸리데이션 에러가 존재함을 어설션합니다. JSON 반환 또는 세션 플래시 모두 가능합니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 대해 전체 혹은 일부 밸리데이션 에러 메시지를 확인할 수도 있습니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```