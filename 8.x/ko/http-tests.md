# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더 사용자 지정](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어설션](#available-assertions)
    - [응답 어설션](#response-assertions)
    - [인증 어설션](#authentication-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보세요:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_a_basic_request()
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 반환된 응답의 HTTP 상태 코드가 지정한 값과 일치하는지 확인합니다. 이 간단한 어설션 외에도 Laravel은 응답 헤더, 내용, JSON 구조 등 다양한 어설션을 제공하여 응답을 자세히 검사할 수 있습니다.

<a name="making-requests"></a>
## 요청 만들기

애플리케이션에 요청을 만들려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 호출할 수 있습니다. 이 메서드들은 실제 네트워크 요청을 보내는 것이 아니라 내부적으로 네트워크 요청을 시뮬레이션합니다.

`Illuminate\Http\Response` 인스턴스를 반환하는 대신, 테스트 요청 메서드는 `Illuminate\Testing\TestResponse` 인스턴스를 반환하며, 이 인스턴스는 애플리케이션의 응답을 검사할 수 있는 다양한 유용한 [어설션 메서드](#available-assertions)를 제공합니다:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_a_basic_request()
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

일반적으로, 각 테스트는 애플리케이션에 단일 요청만 보내야 합니다. 한 테스트 메서드에서 여러 요청을 실행하면 예상치 못한 동작이 발생할 수 있습니다.

> [!TIP]
> 편의를 위해, 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 사용자 지정

`withHeaders` 메서드를 사용하면 요청이 애플리케이션에 전송되기 전에 요청 헤더를 사용자 지정할 수 있습니다. 이 메서드는 원하는 커스텀 헤더를 요청에 추가할 수 있게 해줍니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_interacting_with_headers()
    {
        $response = $this->withHeaders([
            'X-Header' => 'Value',
        ])->post('/user', ['name' => 'Sally']);

        $response->assertStatus(201);
    }
}
```

<a name="cookies"></a>
### 쿠키

요청을 보내기 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 인수로 받으며, `withCookies`는 이름과 값의 배열을 인수로 받습니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_cookies()
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
### 세션 / 인증

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용해 세션 데이터를 배열로 설정할 수 있습니다. 이는 요청 전에 세션에 데이터를 미리 담아야 할 때 유용합니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session()
    {
        $response = $this->withSession(['banned' => false])->get('/');
    }
}
```

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 특정 사용자를 현재 인증된 사용자로 간단히 설정할 수 있는 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/{{version}}/database-testing#writing-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_an_action_that_requires_authentication()
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
                         ->withSession(['banned' => false])
                         ->get('/');
    }
}
```

또한, `actingAs` 메서드에 두 번째 인수로 가드 이름을 전달하여 해당 가드를 통해 사용자를 인증하도록 지정할 수 있습니다:

```
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

애플리케이션에 테스트 요청을 보내고 나면 `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 확인하고 디버깅할 수 있습니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $response = $this->get('/');

        $response->dumpHeaders();

        $response->dumpSession();

        $response->dump();
    }
}
```

또는 `dd`, `ddHeaders`, `ddSession` 메서드를 사용하면 응답 정보를 덤프한 후 실행을 중단할 수 있습니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $response = $this->get('/');

        $response->ddHeaders();

        $response->ddSession();

        $response->dd();
    }
}
```

<a name="exception-handling"></a>
### 예외 처리

특정한 예외가 애플리케이션에서 발생하는지를 테스트하고 싶을 때가 있습니다. 이 경우 Laravel의 예외 처리기가 예외를 잡아 HTTP 응답으로 반환하지 않도록 하려면 요청 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다:

```
$response = $this->withoutExceptionHandling()->get('/');
```

추가로, PHP 언어나 애플리케이션이 사용하는 라이브러리에서 더 이상 권장되지 않는 기능이 사용되는 것을 확인하고 싶다면, 요청 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 비활성화된 경우, 더 이상 권장되지 않는 기능에 대한 경고가 예외로 전환되어 테스트 실패로 이어집니다:

```
$response = $this->withoutDeprecationHandling()->get('/');
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API와 그 응답을 테스트하는 데 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용해 다양한 HTTP 동사로 JSON 요청을 보낼 수 있고, 데이터와 헤더를 쉽게 전달할 수 있습니다. 시작하기 위해 `/api/user`에 `POST` 요청을 보내고, 예상되는 JSON 데이터가 반환되는지 테스트해봅시다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_making_an_api_request()
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

또한, JSON 응답 데이터를 배열 변수처럼 접근할 수 있어 JSON 응답 내 개별 값을 손쉽게 검사할 수 있습니다:

```
$this->assertTrue($response['created']);
```

> [!TIP]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤 `PHPUnit::assertArraySubset`를 사용해 JSON 응답 내에 주어진 배열이 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 포함되어 있어도, 지정된 부분 배열이 존재하면 테스트는 성공합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어설션 (Asserting Exact JSON Matches)

앞서 언급한 `assertJson`은 JSON 응답 내 일부 조각(fragment) 존재 여부를 확인하는 용도입니다. 만약 응답의 JSON이 주어진 배열과 **정확히 일치하는지** 검증하고 싶다면 `assertExactJson` 메서드를 사용하세요:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_asserting_an_exact_json_match()
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
#### JSON 경로 어설션 (Asserting On JSON Paths)

JSON 응답 내 특정 경로(path)에 지정된 값이 존재하는지 확인하려면 `assertJsonPath` 메서드를 사용하세요:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_asserting_a_json_paths_value()
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJsonPath('team.owner.name', 'Darian');
    }
}
```

<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트 (Fluent JSON Testing)

Laravel은 애플리케이션의 JSON 응답을 유창하게 테스트할 수 있는 훌륭한 방법도 제공합니다. 시작하려면 `assertJson` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스가 인수로 전달되며, 이를 이용해 JSON 응답에 대해 다양한 어설션을 할 수 있습니다. `where` 메서드는 JSON 내 특정 속성에 대해 어설션을 수행할 때, `missing` 메서드는 속성이 JSON에 없는지를 확인할 때 사용합니다:

```
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * A basic functional test example.
 *
 * @return void
 */
public function test_fluent_json()
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                 ->where('name', 'Victoria Faith')
                 ->missing('password')
                 ->etc()
        );
}
```

#### `etc` 메서드 이해하기

위 예시에서 `etc` 메서드를 어설션 체인의 끝에 호출한 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 다른 속성이 있을 수도 있다는 것을 Laravel에 알리는 역할을 합니다. 만약 `etc` 메서드를 호출하지 않으면, 검증하지 않은 다른 속성들이 JSON 객체에 존재할 경우 테스트가 실패합니다.

이 동작은 사용자가 JSON 응답에서 노출시키지 말아야 할 민감한 정보를 의도치 않게 노출하는 것을 방지하기 위함입니다. 즉, 반드시 명시적으로 어설션하거나, `etc` 메서드를 통해 추가 속성을 허용해야 합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재 / 부재 어설션 (Asserting Attribute Presence / Absence)

속성이 존재하는지 여부를 확인하려면 `has`와 `missing` 메서드를 사용할 수 있습니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
         ->missing('message')
);
```

또한, 여러 속성의 존재 여부를 한꺼번에 확인하려면 `hasAll`와 `missingAll` 메서드를 사용할 수 있습니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll('status', 'data')
         ->missingAll('message', 'code')
);
```

지정한 속성 중 최소 하나의 존재 여부를 확인할 때는 `hasAny` 메서드를 이용하세요:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
         ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 어설션 (Asserting Against JSON Collections)

종종 라우트가 여러 항목이 포함된 JSON 응답을 반환합니다. 예컨대 여러 사용자 목록일 때:

```
Route::get('/users', function () {
    return User::all();
});
```

이럴 때 유창한 JSON 객체의 `has` 메서드를 사용해 응답에 포함된 사용자 수를 검증할 수 있습니다. 이어서 `first` 메서드를 사용해 컬렉션의 첫 번째 객체에 대해 구체적으로 어설션할 수 있습니다. `first`는 클로저를 인수로 받고, 해당 클로저를 통해 첫 번째 객체의 속성을 검사합니다:

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
             ->first(fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어설션 범위 지정 (Scoping JSON Collection Assertions)

때때로 라우트가 키를 가진 JSON 컬렉션을 반환할 수 있습니다:

```
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이 경우, `has` 메서드를 사용해 컬렉션 내 항목 수를 확인할 수 있습니다. 또한, `has` 메서드를 체인 내에 범위로 지정해 어설션을 진행할 수도 있습니다:

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3)
             ->has('users.0', fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->missing('password')
                     ->etc()
             )
    );
```

물론 `users` 컬렉션에 대해 두 번 호출하는 대신, `has` 메서드의 세 번째 인자로 클로저를 전달하여 첫 번째 요소에 대해 자동으로 스코프된 어설션을 진행할 수도 있습니다:

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3, fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="asserting-json-types"></a>
#### JSON 타입 어설션 (Asserting JSON Types)

JSON 응답의 속성들이 특정 타입인지 확인하려면 `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`와 `whereAllType` 메서드를 사용할 수 있습니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
         ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 지정할 경우 `|` 기호를 사용하거나, `whereType` 메서드의 두 번째 인수에 타입 배열을 전달할 수 있습니다. 이 때 응답의 값이 지정한 타입 중 하나와 일치하면 어설션이 성공합니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
         ->whereType('id', ['string', 'integer'])
);
```

`whereType` 및 `whereAllType` 메서드는 다음 타입을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일이나 이미지를 생성하는 `fake` 메서드를 제공합니다. 이를 `Storage` 파사드의 `fake` 메서드와 함께 사용하면 파일 업로드 테스트를 매우 간단하게 할 수 있습니다. 예를 들어, 아바타 업로드 폼 테스트를 손쉽게 만들 수 있습니다:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_avatars_can_be_uploaded()
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

특정 파일이 존재하지 않음을 어설션하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

```
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 페이크 파일 사용자 지정

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때 이미지의 너비, 높이, 크기(킬로바이트 단위)를 지정하여 애플리케이션의 유효성 검사 규칙을 더 잘 테스트할 수 있습니다:

```
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도, `create` 메서드를 써서 임의의 다른 타입 파일을 생성할 수 있습니다:

```
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면 `$mimeType` 인수를 전달해 파일이 반환할 MIME 타입을 명시할 수도 있습니다:

```
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트

Laravel은 애플리케이션에 실제 HTTP 요청을 시뮬레이션하지 않고 뷰를 렌더링할 수 있도록 합니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하세요. `view` 메서드는 뷰 이름과 선택적 데이터 배열을 인수로 받으며, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 인스턴스는 뷰 내용에 대해 편리한 어설션 메서드들을 제공합니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_a_welcome_view_can_be_rendered()
    {
        $view = $this->view('welcome', ['name' => 'Taylor']);

        $view->assertSee('Taylor');
    }
}
```

`TestView` 클래스는 다음 어설션 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면 `TestView` 인스턴스를 문자열로 캐스팅해서 렌더링된 뷰 원본을 얻을 수 있습니다:

```
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 Laravel이 제공하는 [전역 오류 백(Error Bag)](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에서 공유되는 에러가 필요할 수 있습니다. 에러 메시지를 오류 백에 채우려면 `withViewErrors` 메서드를 사용하세요:

```
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면 `blade` 메서드를 사용해 원시 Blade 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로 `blade` 메서드는 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

또한 `component` 메서드를 사용해 [Blade 컴포넌트](/docs/{{version}}/blade#components)를 평가하고 렌더링할 수 있습니다. `view` 메서드처럼 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션

<a name="response-assertions"></a>
### 응답 어설션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 사용할 수 있는 다양한 커스텀 어설션 메서드를 제공합니다. 이 어설션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드에서 반환되는 응답 객체에서 호출할 수 있습니다:


<div class="collection-method-list" markdown="1">

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
[assertHeader](#assert-header)
[assertHeaderMissing](#assert-header-missing)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)
[assertJsonPath](#assert-json-path)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertJsonValidationErrorFor](#assert-json-validation-error-for)
[assertLocation](#assert-location)
[assertNoContent](#assert-no-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertSessionHas](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[assertSessionMissing](#assert-session-missing)
[assertSimilarJson](#assert-similar-json)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정한 쿠키가 포함되었는지 어설션합니다:

```
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정한 쿠키가 포함되어 있고 만료되었는지 어설션합니다:

```
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정한 쿠키가 포함되어 있고 만료되지 않았는지 어설션합니다:

```
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않은지 어설션합니다:

```
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답 상태 코드가 201인지 어설션합니다:

```
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답 본문에 지정한 문자열이 포함되어 있지 않은지 어설션합니다. 두 번째 인수에 `false`를 넘기면 문자열이 이스케이프되지 않습니다:

```
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답의 텍스트(HTML 태그 제거 후)에 지정한 문자열이 포함되어 있지 않은지 어설션합니다. 두 번째 인수에 `false`를 넘기면 문자열이 이스케이프되지 않습니다:

```
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드" 응답인지 어설션합니다. 보통 `Response::download`, `BinaryFileResponse` 또는 `Storage::download`로 생성된 응답입니다:

```
$response->assertDownload();
```

다운로드된 파일 이름이 특정 이름인지 어설션할 수도 있습니다:

```
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 지정한 JSON 데이터와 정확히 일치하는지 어설션합니다:

```
$response->assertExactJson(array $data);
```

<a name="assert-forbidden"></a>
#### assertForbidden

응답의 HTTP 상태 코드가 403 금지(Forbidden)인지 어설션합니다:

```
$response->assertForbidden();
```

<a name="assert-header"></a>
#### assertHeader

응답 헤더에 지정한 이름과 값이 존재하는지 어설션합니다:

```
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답 헤더에 지정한 이름이 존재하지 않는지 어설션합니다:

```
$response->assertHeaderMissing($headerName);
```

<a name="assert-json"></a>
#### assertJson

응답에 지정한 JSON 데이터(부분 집합)가 포함되어 있는지 어설션합니다:

```
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메서드는 응답을 배열로 변환한 후 `PHPUnit::assertArraySubset`를 사용해 JSON 응답 내에 지정된 배열이 존재하는지 확인합니다. 만약 JSON 응답에 다른 속성이 많아도, 지정된 부분만 존재하면 테스트는 성공합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON 내 지정한 키에 있는 배열의 항목 수가 기대한 값과 일치하는지 어설션합니다:

```
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 지정한 JSON 데이터가 어디에든 포함되어 있는지 어설션합니다:

```
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

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정한 JSON 데이터가 포함되어 있지 않은지 어설션합니다:

```
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 지정한 JSON 데이터와 정확히 일치하는 데이터가 포함되어 있지 않은지 어설션합니다:

```
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 지정한 키에 대한 JSON 유효성 검사 오류가 없음을 어설션합니다:

```
$response->assertJsonMissingValidationErrors($keys);
```

> [!TIP]
> 더 일반적인 [assertValid](#assert-valid) 메서드는 JSON 또는 세션에 플래시 된 유효성 검사 오류가 없음을 어설션하는 데 사용할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답 JSON 내 지정한 경로에 주어진 값이 포함되어 있음을 어설션합니다:

```
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 애플리케이션에서 반환한 JSON 응답이 다음과 같다면:

```js
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 오브젝트의 `name` 속성값이 'Steve Schoger'인지 확인할 수 있습니다:

```
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답 JSON이 지정한 구조를 포함하고 있는지 어설션합니다:

```
$response->assertJsonStructure(array $structure);
```

예를 들어, JSON 응답이 다음과 같다면:

```js
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 구조를 확인할 수 있습니다:

```
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때때로 JSON 응답에 객체 배열이 포함될 수 있습니다:

```js
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

이럴 때 구조 어설션에서 `*` 문자를 사용해 배열 내 모든 객체 구조를 검사할 수 있습니다:

```
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

응답에 지정한 키에 대한 JSON 유효성 검사 오류가 포함되어 있음을 어설션합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되는 응답을 테스트할 때 사용하세요:

```
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!TIP]
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON으로 반환되거나 세션에 플래시 된 검증 오류가 포함되었음을 어설션할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답이 지정한 키에 대해 JSON 유효성 검사 오류를 포함하고 있는지 어설션합니다:

```
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-location"></a>
#### assertLocation

응답 헤더 `Location`에 지정한 URI가 포함되어 있는지 어설션합니다:

```
$response->assertLocation($uri);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답의 HTTP 상태 코드가 지정한 값이고, 본문 내용이 없는지 어설션합니다:

```
$response->assertNoContent($status = 204);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답의 HTTP 상태 코드가 404 Not Found인지 어설션합니다:

```
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답의 HTTP 상태 코드가 200 OK인지 어설션합니다:

```
$response->assertOk();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정한 암호화되지 않은 쿠키가 포함되었는지 어설션합니다:

```
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정한 URI로 리다이렉트되는지 어설션합니다:

```
$response->assertRedirect($uri);
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 지정한 문자열을 포함하는 URI로 리다이렉트되는지 어설션합니다:

```
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 지정한 서명된(signed) 라우트로 리다이렉트되는지 어설션합니다:

```
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-see"></a>
#### assertSee

응답 본문에 지정한 문자열이 포함되었는지 어설션합니다. 두 번째 인수로 `false`를 넘기면 문자열이 이스케이프되지 않습니다:

```
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답 본문에 지정한 문자열들이 순서대로 포함되었는지 어설션합니다. 두 번째 인수로 `false`를 넘기면 문자열이 이스케이프되지 않습니다:

```
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답의 텍스트(HTML 태그 제거 후)에 지정한 문자열이 포함되었는지 어설션합니다. 두 번째 인수로 `false`를 넘기면 문자열이 이스케이프되지 않습니다:

```
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트(HTML 태그 제거 후)에 지정한 문자열들이 순서대로 포함되었는지 어설션합니다. 두 번째 인수로 `false`를 넘기면 문자열이 이스케이프되지 않습니다:

```
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정한 키와 값이 포함되었는지 어설션합니다:

```
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 전달해 조건을 검사할 수 있으며, 클로저가 `true`를 반환하면 어설션이 성공합니다:

```
$response->assertSessionHas($key, function ($value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

[플래시된 입력값 배열](/docs/{{version}}/responses#redirecting-with-flashed-session-data)에서 지정한 키와 값이 포함되었는지 어설션합니다:

```
$response->assertSessionHasInput($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 성공합니다:

```
$response->assertSessionHasInput($key, function ($value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정한 키와 값들의 배열이 모두 포함되었는지 어설션합니다:

```
$response->assertSessionHasAll(array $data);
```

예를 들어, 세션에 `name`과 `status` 키가 존재하고 다음과 같은 값을 가지고 있는지 검사할 수 있습니다:

```
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 지정한 키들 또는 필드에 대한 유효성 검사 오류가 포함되었는지 어설션합니다. `$keys`가 연관 배열이면 각 필드의 특정 오류 메시지도 검사합니다. 이 메서드는 유효성 검사 오류가 세션에 플래시되는 라우트를 테스트할 때 사용하세요:

```
$response->assertSessionHasErrors(
    array $keys, $format = null, $errorBag = 'default'
);
```

예를 들어, `name`과 `email` 필드에 유효성 검사 오류 메시지가 플래시되었는지 검사할 수 있습니다:

```
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드에 대해 특정 오류 메시지가 포함되었는지도 검사할 수 있습니다:

```
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

지정한 [에러 백(Error Bag)](/docs/{{version}}/validation#named-error-bags) 내에 특정 키에 대한 유효성 검사 오류가 포함되었는지 어설션합니다. `$keys`가 연관 배열이면 각 필드에 대해 특정 오류 메시지도 검사합니다:

```
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검사 오류가 하나도 없는지 어설션합니다:

```
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 지정한 키들에 대한 유효성 검사 오류가 없는지 어설션합니다:

```
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정한 키가 포함되어 있지 않은지 어설션합니다:

```
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답 상태 코드가 지정한 HTTP 상태 코드인지 어설션합니다:

```
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답 상태 코드가 성공 범위(200 이상, 300 미만)에 있는지 어설션합니다:

```
$response->assertSuccessful();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답 상태 코드가 401 인증 안 됨(Unauthorized)인지 어설션합니다:

```
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답 상태 코드가 422 처리 불가(Unprocessable Entity)인지 어설션합니다:

```
$response->assertUnprocessable();
```

<a name="assert-valid"></a>
#### assertValid

응답에 지정한 키에 대해 유효성 검사 오류가 없음을 어설션합니다. JSON으로 반환되었거나 세션에 플래시된 유효성 검사 오류가 없음을 모두 검사합니다:

```
// 유효성 검사 오류가 하나도 없는지 어설션...
$response->assertValid();

// 지정한 키들에 대해 유효성 검사 오류가 없는지 어설션...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 지정한 키에 대해 유효성 검사 오류가 있음을 어설션합니다. JSON으로 반환되었거나 세션에 플래시된 유효성 검사 오류를 검사할 수 있습니다:

```
$response->assertInvalid(['name', 'email']);
```

특정 키에 대해 특정 오류 메시지가 포함되었는지도 검사할 수 있습니다. 이때 메시지 전체 또는 일부만 포함된 메시지도 가능합니다:

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 특정 데이터를 포함하고 있는지 어설션합니다:

```
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 넘기면 해당 뷰 데이터의 조건을 검사할 수 있습니다:

```
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

뷰 데이터는 응답 배열 변수처럼 접근해 검증할 수도 있습니다:

```
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰가 지정한 여러 데이터를 모두 포함하는지 어설션합니다:

```
$response->assertViewHasAll(array $data);
```

뷰가 지정한 키를 포함하는지 어설션:

```
$response->assertViewHasAll([
    'name',
    'email',
]);
```

뷰 데이터가 특정 값을 가지고 있는지 어설션:

```
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

응답이 특정 뷰를 반환했는지 어설션합니다:

```
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 지정한 데이터 키가 포함되어 있지 않은지 어설션합니다:

```
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어설션

Laravel은 인증 관련 다양한 어설션도 제공합니다. 주의할 점은 이 메서드들은 `Illuminate\Testing\TestResponse` 인스턴스가 아니라 테스트 클래스 자체에서 호출해야 한다는 것입니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 어설션합니다:

```
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았음을 어설션합니다:

```
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 어설션합니다:

```
$this->assertAuthenticatedAs($user, $guard = null);
```