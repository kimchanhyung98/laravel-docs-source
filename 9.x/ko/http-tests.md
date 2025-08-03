# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 사용자 지정하기](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트하기](#testing-json-apis)
    - [플루언트 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트하기](#testing-file-uploads)
- [뷰 테스트하기](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [유효성 검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 그 응답을 검사하는 매우 직관적인 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보세요:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제입니다.
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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가지고 있음을 확인합니다. 이 간단한 어서션 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 호출할 수 있습니다. 이 메서드들은 실제 HTTP 요청이 아니라 내부에서 네트워크 요청을 시뮬레이션합니다.

`Illuminate\Http\Response` 인스턴스를 반환하는 대신, 테스트 요청 메서드들은 `Illuminate\Testing\TestResponse` 인스턴스를 반환하는데, 이 클래스는 애플리케이션의 응답을 검사할 수 있는 [다양한 유용한 어서션](#available-assertions)을 제공합니다:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제입니다.
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

일반적으로, 각 테스트는 애플리케이션에 하나의 요청만 보내야 합니다. 한 테스트 메서드 내에서 여러 요청을 실행하면 의도치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해 테스트를 실행할 때 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 사용자 지정하기

요청이 애플리케이션에 전송되기 전에 `withHeaders` 메서드를 사용하여 요청 헤더를 사용자 지정할 수 있습니다. 이 메서드를 통해 원하는 커스텀 헤더를 요청에 추가할 수 있습니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제입니다.
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

요청 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 각각 인수로 받고, `withCookies`는 이름과 값 쌍 배열을 전달받습니다:

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

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 통해 세션 데이터를 배열로 설정할 수 있습니다. 이는 요청 전에 세션에 데이터를 로드할 때 유용합니다:

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

Laravel 세션은 보통 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 해당 사용자를 현재 사용자로 간단히 인증하는 방법을 제공합니다. 예를 들어 [모델 팩토리](/docs/9.x/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

또한, `actingAs` 메서드의 두 번째 인자로 가드 이름을 전달해 어떤 가드로 사용자 인증을 수행할지 지정할 수 있습니다. 이 가드는 테스트 과정 동안 기본 가드로 적용됩니다:

```
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

애플리케이션에 테스트 요청을 보낸 뒤, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 확인하고 디버깅할 수 있습니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제입니다.
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

또는 `dd`, `ddHeaders`, `ddSession` 메서드를 사용해 정보를 출력하고 즉시 실행을 중지할 수도 있습니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제입니다.
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

특정 예외가 애플리케이션에서 발생하는지 테스트하고 싶을 때가 있습니다. 예외가 Laravel의 예외 처리기에 의해 잡히고 HTTP 응답으로 변환되는 것을 막으려면 요청 전에 `withoutExceptionHandling` 메서드를 호출하세요:

```
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 언어나 라이브러리에서 더 이상 지원하지 않는 기능을 사용하는지 확인하려면 요청 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이 기능이 비활성화되면, 더 이상 지원되지 않는 경고들이 예외로 변환되어 테스트가 실패하게 됩니다:

```
$response = $this->withoutDeprecationHandling()->get('/');
```

<a name="testing-json-apis"></a>
## JSON API 테스트하기

Laravel은 JSON API와 그 응답을 테스트하기 위한 여러 헬퍼도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드들은 여러 HTTP 메서드에 대한 JSON 요청을 보낼 때 사용됩니다. 데이터와 헤더를 쉽게 전달할 수도 있습니다. 아래는 `/api/user`에 `POST` 요청을 보내고 예상 JSON 데이터 반환을 확인하는 테스트 예제입니다:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제입니다.
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

또한 JSON 응답 데이터는 배열 변수처럼 접근할 수 있어서 JSON 응답 내 개별 값 검사도 편리합니다:

```
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤 `PHPUnit::assertArraySubset`를 사용해 주어진 배열이 JSON 응답 내 존재하는지 검사합니다. 따라서 JSON 응답에 다른 프로퍼티가 있더라도, 주어진 일부 내용만 있으면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어서션

앞서 설명한 `assertJson`은 JSON 응답 내 부분적인 검증에 적합합니다. JSON 응답이 정확하게 주어진 배열과 일치하는지 확인하려면 `assertExactJson` 메서드를 사용하세요:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제입니다.
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
#### JSON 경로 어서션

특정 JSON 경로에 데이터가 있는지 검증하려면 `assertJsonPath` 메서드를 사용하세요:

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 기능 테스트 예제입니다.
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

`assertJsonPath`는 클로저도 인자로 받아 조건에 따라 동적으로 어서션이 통과할지 결정할 수 있습니다:

```
$response->assertJsonPath('team.owner.name', fn ($name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 더 우아하게 테스트하는 방법도 제공합니다. `assertJson` 메서드에 클로저를 전달하면, 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스와 함께 호출되며, JSON에 대해 다양한 어서션을 쉽게 작성할 수 있습니다. `where` 메서드는 특정 JSON 속성을 검사하고, `missing` 메서드는 속성이 없는지 검증합니다:

```
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * 기본 기능 테스트 예제입니다.
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
                 ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                 ->whereNot('status', 'pending')
                 ->missing('password')
                 ->etc()
        );
}
```

#### `etc` 메서드 이해하기

위 예제 마지막에 호출된 `etc` 메서드는 JSON 객체에 추가 속성이 있을 수 있음을 Laravel에 알려줍니다. 만약 `etc` 메서드를 사용하지 않으면, 어서션을 하지 않은 다른 속성이 JSON 객체에 있으면 테스트가 실패합니다.

이는 JSON 응답에 민감한 정보를 의도치 않게 노출하는 것을 방지하기 위한 기능입니다. 즉, 검사할 속성에 대해 명시적으로 어서션하거나 `etc`로 추가 속성을 허용해야 합니다.

하지만, `etc` 메서드는 JSON 구조 내 중첩된 배열에 추가 속성이 있지 않다는 보장은 하지 않습니다. 이 메서드는 호출된 중첩 깊이에서만 추가 속성 없음을 검사합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재 / 부재 어서션

속성의 존재 여부를 어서션하려면 `has`와 `missing` 메서드를 사용하세요:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
         ->missing('message')
);
```

또한, `hasAll`과 `missingAll` 메서드를 통해 여러 속성의 존재 여부를 동시에 검사할 수 있습니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
         ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드는 주어진 속성들 중 적어도 하나가 존재하는지 확인할 때 사용합니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
         ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

라우트가 여러 아이템(예: 여러 사용자)을 포함한 JSON 컬렉션을 반환하는 경우가 많습니다:

```
Route::get('/users', function () {
    return User::all();
});
```

이럴 때, 플루언트 JSON 객체의 `has` 메서드를 사용해 응답에 포함된 사용자 수를 어서션하고, `first` 메서드로 첫 번째 사용자에 대해 추가 검사를 할 수 있습니다. `first`는 클로저를 인자로 받아 해당 JSON 객체를 검사합니다:

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
             ->first(fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어서션 범위 지정

때때로 라우트는 이름이 있는 키에 JSON 컬렉션을 할당해 반환하기도 합니다:

```
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이 경우, `has` 메서드로 컬렉션 내 아이템 개수를 확인하고, 클로저를 세 번째 인자로 넘겨 해당 컬렉션 내 특정 항목에 대한 체인 어서션 범위를 지정할 수 있습니다:

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3)
             ->has('users.0', fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

위와 같이 두 번 호출하는 대신에, 세 번째 인자에 클로저를 넣어 다음과 같이 한 번만 호출할 수 있습니다:

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3, fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="asserting-json-types"></a>
#### JSON 타입 어서션

JSON 응답의 속성이 특정 타입인지 확인하고 싶을 때, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType` 및 `whereAllType` 메서드를 사용하세요:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
         ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`whereType`에 문자열로 `|`로 구분한 여러 타입이나 배열로 타입 리스트를 전달할 수 있습니다. 응답 값이 리스트 중 어느 하나라도 해당하면 성공합니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
         ->whereType('id', ['string', 'integer'])
);
```

지원되는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null`입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트하기

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일이나 이미지를 생성하는 `fake` 메서드를 제공합니다. 이를 `Storage` 파사드의 `fake` 메서드와 함께 사용하면 파일 업로드 테스트가 훨씬 간편해집니다. 예를 들어, 아바타 업로드 폼 테스트는 다음과 같이 작성할 수 있습니다:

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

특정 파일이 존재하지 않음을 어서션하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용하세요:

```
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 더미 파일 커스터마이징

`UploadedFile`의 `fake` 메서드로 이미지를 만들 때, 너비, 높이, 크기(킬로바이트 단위)를 지정할 수도 있어 유효성 검증 규칙 테스트에 유용합니다:

```
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에 다른 타입 파일은 `create` 메서드를 사용해 생성할 수 있습니다:

```
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하면 `$mimeType` 인자를 전달해 명시적으로 MIME 타입도 정할 수 있습니다:

```
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트하기

Laravel은 실제 HTTP 요청 없이도 뷰를 렌더링할 수 있게 합니다. 테스트 내에서 `view` 메서드를 호출하세요. 이 메서드는 뷰 이름과 선택적인 데이터 배열을 인자로 받아 `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 클래스는 뷰 내용을 편리하게 검사할 수 있는 여러 어서션 메서드를 제공합니다:

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

`TestView` 클래스는 다음 어서션 메서드를 지원합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

원한다면 `TestView` 인스턴스를 문자열로 캐스팅해 원본 렌더링 결과를 얻을 수도 있습니다:

```
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 오류 공유하기

일부 뷰는 [Laravel이 제공하는 전역 에러 백](/docs/9.x/validation#quick-displaying-the-validation-errors)에 의존할 수 있습니다. 에러 메시지로 오류 백을 채우려면 `withViewErrors` 메서드를 사용하세요:

```
$view = $this->withViewErrors([
    'name' => ['유효한 이름을 입력해주세요.']
])->view('form');

$view->assertSee('유효한 이름을 입력해주세요.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요 시, `blade` 메서드로 원시 [Blade](/docs/9.x/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

`component` 메서드를 사용하면 [Blade 컴포넌트](/docs/9.x/blade#components)를 평가하고 렌더링할 수 있습니다. `component`는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 사용할 수 있는 다양한 커스텀 어서션 메서드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답 인스턴스에서 호출할 수 있습니다:



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
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
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

응답에 지정한 쿠키가 포함되어 있는지 어서션합니다:

```
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정한 쿠키가 포함되어 있고 만료되었는지 어서션합니다:

```
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정한 쿠키가 포함되어 있고 아직 만료되지 않았는지 어서션합니다:

```
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않음을 어서션합니다:

```
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답의 HTTP 상태 코드가 201인지 어서션합니다:

```
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 특정 문자열이 포함되어 있지 않음을 어서션합니다. 이 메서드는 기본적으로 주어진 문자열을 이스케이프 처리하며, 두 번째 인수에 `false`를 넘기면 이스케이프를 건너뛸 수 있습니다:

```
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 특정 문자열이 포함되어 있지 않음을 어서션합니다. 이 메서드는 기본적으로 주어진 문자열을 이스케이프 처리하고, 응답 내용을 `strip_tags` PHP 함수로 태그를 제거한 뒤 검사합니다. 두 번째 인수에 `false`를 전달하면 이스케이프를 건너뛸 수 있습니다:

```
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드" 응답인지 어서션합니다. 일반적으로 라우트가 `Response::download`, `BinaryFileResponse` 또는 `Storage::download` 응답을 반환했음을 의미합니다:

```
$response->assertDownload();
```

필요하면 다운로드된 파일명이 지정한 이름과 일치하는지도 어서션 가능합니다:

```
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답 JSON 데이터가 주어진 데이터와 **정확히 일치**하는지 어서션합니다:

```
$response->assertExactJson(array $data);
```

<a name="assert-forbidden"></a>
#### assertForbidden

응답 HTTP 상태 코드가 403(금지됨)인지 어서션합니다:

```
$response->assertForbidden();
```

<a name="assert-header"></a>
#### assertHeader

응답에 특정 헤더와 값이 포함되어 있는지 어서션합니다:

```
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 특정 헤더가 포함되어 있지 않음을 어서션합니다:

```
$response->assertHeaderMissing($headerName);
```

<a name="assert-json"></a>
#### assertJson

응답 JSON에 주어진 데이터가 포함되어 있는지 어서션합니다:

```
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환한 뒤 `PHPUnit::assertArraySubset`로 JSON 내 일부 배열 존재 여부를 확인합니다. 따라서 JSON 내 다른 프로퍼티가 존재해도 주어진 부분이 있으면 테스트는 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

지정한 키에 배열이 존재하며 아이템 개수가 기대한 수와 일치하는지 어서션합니다:

```
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답 어디에든 지정한 JSON 데이터가 포함되어 있는지 어서션합니다:

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

<a name="assert-json-is-array"></a>
#### assertJsonIsArray

응답 JSON이 배열인지 어서션합니다:

```
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 어서션합니다:

```
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 주어진 JSON 데이터가 포함되어 있지 않음을 어서션합니다:

```
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 정확히 일치하는 JSON 데이터가 포함되어 있지 않음을 어서션합니다:

```
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

주어진 키에 대해 JSON 유효성 검증 오류가 없는지 어서션합니다:

```
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 더 일반적인 [assertValid](#assert-valid) 메서드는 JSON 혹은 세션에 플래시된 모든 유효성 검증 오류가 없음을 검증할 때 사용할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

지정한 JSON 경로에 기대하는 값이 포함되어 있는지 어서션합니다:

```
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 다음 JSON 응답이 반환되었다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`name` 프로퍼티가 다음 값과 일치하는지 테스트할 수 있습니다:

```
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

지정한 JSON 경로가 응답에 존재하지 않는지 어서션합니다:

```
$response->assertJsonMissingPath($path);
```

예를 들어, 위 JSON 응답에 `user.email` 속성이 없음을 다음과 같이 검사할 수 있습니다:

```
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답 JSON이 주어진 구조와 일치하는지 어서션합니다:

```
$response->assertJsonStructure(array $structure);
```

예를 들어, 아래 JSON 응답이 반환되었다고 가정할 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 JSON 구조 검사를 할 수 있습니다:

```
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때로는 배열 내 객체들의 구조를 검사할 수 있습니다:

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

이럴 때는 `*` 문자를 사용해 배열 내 모든 객체를 검사합니다:

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

유효성 검증 오류가 JSON 형태로 반환될 때, 주어진 키에 오류가 존재하는지 어서션합니다:

```
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON 오류나 세션에 플래시된 오류 모두를 어서션할 때 사용합니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답에 지정한 키에 대해 JSON 유효성 검증 오류가 존재하는지 어서션합니다:

```
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-location"></a>
#### assertLocation

응답의 `Location` 헤더 값이 지정한 URI와 일치하는지 어서션합니다:

```
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 내용이 지정한 문자열과 일치하는지 어서션합니다:

```
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정한 HTTP 상태 코드이며 내용이 없는지 어서션합니다:

```
$response->assertNoContent($status = 204);
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트리밍된 응답 내용이 지정한 문자열과 일치하는지 어서션합니다:

```
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답 HTTP 상태 코드가 404(찾을 수 없음)인지 어서션합니다:

```
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답 HTTP 상태 코드가 200인지 어서션합니다:

```
$response->assertOk();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 암호화되지 않은(평문) 쿠키가 포함되어 있는지 어서션합니다:

```
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정한 URI로 리다이렉트하는지 어서션합니다:

```
$response->assertRedirect($uri);
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 특정 문자열을 포함하는 URI로 리다이렉트하는지 어서션합니다:

```
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 지정한 [이름 있는 라우트](/docs/9.x/routing#named-routes)로 리다이렉트하는지 어서션합니다:

```
$response->assertRedirectToRoute($name = null, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 지정한 [서명된 라우트](/docs/9.x/urls#signed-urls)로 리다이렉트하는지 어서션합니다:

```
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-see"></a>
#### assertSee

응답에 특정 문자열이 포함되어 있음을 어서션합니다. 기본적으로 전달된 문자열을 이스케이프하며, 두 번째 인자에 `false`를 넘기면 이스케이프하지 않습니다:

```
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답에 여러 문자열이 지정한 순서대로 포함되어 있는지 어서션합니다. 기본적으로 문자열들을 이스케이프하며, 두 번째 인자에 `false`를 넘기면 이스케이프하지 않습니다:

```
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 텍스트에 특정 문자열이 포함되어 있는지 어서션합니다. 기본적으로 문자열을 이스케이프하며, 응답 내용은 `strip_tags` 함수로 태그를 제거한 뒤 검사합니다. 두 번째 인자에 `false`를 넘기면 이스케이프하지 않습니다:

```
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에 여러 문자열이 지정한 순서대로 포함되어 있는지 어서션합니다. 기본적으로 문자열을 이스케이프하며, 응답은 `strip_tags`로 태그를 제거한 뒤 검사합니다. 두 번째 인자에 `false`를 넘기면 이스케이프하지 않습니다:

```
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정한 데이터가 포함되어 있는지 어서션합니다:

```
$response->assertSessionHas($key, $value = null);
```

두 번째 인자로 클로저를 전달해 조건을 지정할 수도 있습니다. 클로저가 `true`를 반환하면 어서션이 통과합니다:

```
$response->assertSessionHas($key, function ($value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션의 [플래시된 입력 배열](/docs/9.x/responses#redirecting-with-flashed-session-data)에 특정 키가 존재하는지 어서션합니다:

```
$response->assertSessionHasInput($key, $value = null);
```

조건을 지정한 클로저를 두 번째 인자로 전달할 수도 있습니다:

```
$response->assertSessionHasInput($key, function ($value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 주어진 키/값 쌍 배열이 모두 포함되어 있는지 어서션합니다:

```
$response->assertSessionHasAll(array $data);
```

예를 들어 세션에 `name`과 `status`가 존재하는지 검사하려면:

```
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

주어진 키 배열에 대해 세션에 유효성 검증 오류가 존재하는지 어서션합니다. 연관 배열을 넘기면 각 필드에 특정 오류 메시지가 있는지도 검사합니다. 이 메서드는 오류가 세션에 플래시되는 라우트 테스트에 사용합니다:

```
$response->assertSessionHasErrors(
    array $keys, $format = null, $errorBag = 'default'
);
```

예시:

```
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드에 정확한 메시지 어서션:

```
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON 또는 세션 플래시 오류 모두에 대해 어서션할 때 사용합니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [이름 있는 에러 백](/docs/9.x/validation#named-error-bags) 내에서 주어진 키 배열을 검사합니다. 연관 배열은 각 필드와 메시지 쌍을 검사합니다:

```
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 오류가 전혀 없음을 어서션합니다:

```
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

주어진 키에 대해 세션에 유효성 검증 오류가 없음을 어서션합니다:

```
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 JSON과 세션 플래시 검증 오류가 모두 없음을 어서션합니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 특정 키가 포함되어 있지 않음을 어서션합니다:

```
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답 HTTP 상태 코드를 검사합니다:

```
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답 HTTP 상태 코드가 200 이상 300 미만(성공 범위)에 속하는지 어서션합니다:

```
$response->assertSuccessful();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답 HTTP 상태 코드가 401(인증 필요)인지 어서션합니다:

```
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답 HTTP 상태 코드가 422(처리 불가)인지 어서션합니다:

```
$response->assertUnprocessable();
```

<a name="assert-valid"></a>
#### assertValid

응답에 주어진 키에 대한 유효성 검증 오류가 없음을 어서션합니다. JSON 구조로 반환되거나 세션에 플래시된 오류 모두를 검사할 수 있습니다:

```
// 유효성 오류가 전혀 없음을 어서션...
$response->assertValid();

// 특정 키에 오류가 없음을 어서션...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 주어진 키에 대한 유효성 검증 오류가 있음을 어서션합니다. JSON 구조나 세션 플래시 오류 모두를 검사할 수 있습니다:

```
$response->assertInvalid(['name', 'email']);
```

특정 키에 정확한 혹은 부분 메시지가 포함된 오류가 있는지 검사할 수도 있습니다:

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 특정 데이터가 포함되어 있는지 어서션합니다:

```
$response->assertViewHas($key, $value = null);
```

두 번째 인자로 클로저를 전달해 특정 데이터에 대해 어서션할 수 있습니다:

```
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

뷰 데이터는 배열 변수처럼 접근 가능해 간단히 검사할 수도 있습니다:

```
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

뷰에 특정 데이터 목록이 모두 포함되어 있는지 어서션합니다:

```
$response->assertViewHasAll(array $data);
```

키 배열로 단순 존재 여부를 검사하거나:

```
$response->assertViewHasAll([
    'name',
    'email',
]);
```

키-값 쌍으로 특정 값을 가지고 있는지도 어서션할 수 있습니다:

```
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

라우트가 반환한 뷰가 지정한 뷰 이름과 일치하는지 어서션합니다:

```
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 특정 데이터 키가 포함되어 있지 않음을 어서션합니다:

```
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 인증 관련 어서션도 제공합니다. 이 메서드들은 테스트 클래스 자체에서 호출하며, `get`, `post` 등의 메서드가 반환하는 `Illuminate\Testing\TestResponse` 인스턴스에서는 호출하지 않습니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었음을 어서션합니다:

```
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태임을 어서션합니다:

```
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되어 있음을 어서션합니다:

```
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어서션

Laravel은 요청으로 전달된 데이터가 유효한지 혹은 유효하지 않은지를 확인할 수 있도록 두 가지 주요 유효성 검증 어서션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 지정한 키에 대한 유효성 검증 오류가 없음을 어서션합니다. JSON 형태로 반환되거나 세션에 플래시된 오류를 모두 검사할 수 있습니다:

```
// 유효성 오류가 전혀 없음을 어서션...
$response->assertValid();

// 특정 키에 오류가 없음을 어서션...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 지정한 키에 유효성 검증 오류가 있음을 어서션합니다. JSON 혹은 세션 플래시 오류를 모두 검사할 수 있습니다:

```
$response->assertInvalid(['name', 'email']);
```

특정 키에 포함된 오류 메시지를 전체 혹은 일부로 검사할 수도 있습니다:

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```