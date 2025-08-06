# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 생성](#making-requests)
    - [요청 헤더 커스터마이즈](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한(Fluent) JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [유효성 검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 여러분의 애플리케이션에 HTTP 요청을 보내고, 그 응답을 검증할 수 있도록 매우 유창한(Fluent) API를 제공합니다. 예를 들어, 아래의 기능 테스트 코드를 살펴보세요:

```php tab=Pest
<?php

test('the application returns a successful response', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 응답의 HTTP 상태 코드가 주어진 값과 일치하는지 검증합니다. 이처럼 간단한 어서션 외에도, Laravel은 응답 헤더, 본문 컨텐츠, JSON 구조 등 다양한 부분을 검사할 수 있는 여러 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 생성 (Making Requests)

애플리케이션에 요청을 보내려면 테스트 코드에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 사용할 수 있습니다. 이러한 메서드들은 실제 "실제" HTTP 요청을 보내는 것이 아니라, 내부적으로 네트워크 요청을 시뮬레이션합니다.

이 메서드들은 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, 대신 [다양한 유용한 어서션](#available-assertions)이 제공되는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이로써 애플리케이션의 응답을 손쉽게 검증할 수 있습니다:

```php tab=Pest
<?php

test('basic request', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_a_basic_request(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

일반적으로, 각각의 테스트는 단 하나의 요청만 보내도록 만드는 것이 권장됩니다. 하나의 테스트 메서드에서 여러 요청을 실행할 경우 예기치 못한 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해, 테스트 실행 시에는 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이즈 (Customizing Request Headers)

`withHeaders` 메서드를 사용하면 요청을 보내기 전에 원하는 헤더를 자유롭게 설정할 수 있습니다. 아래와 같이 커스텀 헤더를 쉽게 추가할 수 있습니다:

```php tab=Pest
<?php

test('interacting with headers', function () {
    $response = $this->withHeaders([
        'X-Header' => 'Value',
    ])->post('/user', ['name' => 'Sally']);

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
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

요청을 보내기 전에 `withCookie` 또는 `withCookies` 메서드를 통해 쿠키 값을 지정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 각각 인수로 받고, `withCookies`는 이름/값의 배열을 받습니다:

```php tab=Pest
<?php

test('interacting with cookies', function () {
    $response = $this->withCookie('color', 'blue')->get('/');

    $response = $this->withCookies([
        'color' => 'blue',
        'name' => 'Taylor',
    ])->get('/');

    //
});
```

```php tab=PHPUnit
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

        //
    }
}
```

<a name="session-and-authentication"></a>
### 세션 / 인증 (Session / Authentication)

Laravel은 HTTP 테스트 시 세션과 상호작용하기 위한 다양한 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용해 세션 데이터를 배열 형태로 설정할 수 있습니다. 이는 요청 전에 특정 데이터를 세션에 담아둘 때 유용합니다:

```php tab=Pest
<?php

test('interacting with the session', function () {
    $response = $this->withSession(['banned' => false])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session(): void
    {
        $response = $this->withSession(['banned' => false])->get('/');

        //
    }
}
```

Laravel의 세션은 주로 현재 인증된 사용자의 상태 유지를 위해 사용됩니다. 따라서, `actingAs` 헬퍼 메서드를 사용하면 지정한 사용자를 간편하게 인증된 사용자로 설정할 수 있습니다. 예시로, [모델 팩토리](/docs/12.x/eloquent-factories)로 사용자를 생성하고 인증할 수도 있습니다:

```php tab=Pest
<?php

use App\Models\User;

test('an action that requires authentication', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->withSession(['banned' => false])
        ->get('/');

    //
});
```

```php tab=PHPUnit
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

        //
    }
}
```

필요하다면, 두 번째 인수로 사용할 guard 이름을 `actingAs` 메서드에 전달해 인증시 사용할 guard를 지정할 수 있습니다. 이 guard는 해당 테스트가 실행되는 동안 기본 guard로 사용됩니다:

```php
$this->actingAs($user, 'web');
```

반대로 인증되지 않은(비로그인) 상태를 보장하고 싶다면, `actingAsGuest` 메서드를 사용할 수 있습니다:

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

테스트 요청을 보낸 후 응답의 내용을 확인하거나 디버깅하려면, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용할 수 있습니다:

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dumpHeaders();

    $response->dumpSession();

    $response->dump();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
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

또한, `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하면 응답 관련 정보를 출력하고 실행을 즉시 중단할 수도 있습니다:

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dd();
    $response->ddHeaders();
    $response->ddBody();
    $response->ddJson();
    $response->ddSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dd();
        $response->ddHeaders();
        $response->ddBody();
        $response->ddJson();
        $response->ddSession();
    }
}
```

<a name="exception-handling"></a>
### 예외 처리 (Exception Handling)

특정 예외가 실제로 발생하는지 테스트해야 할 때가 있습니다. 이를 위해 `Exceptions` 파사드를 사용하여 예외 핸들러를 "가짜(fake)"로 만들 수 있습니다. 핸들러를 fake한 다음에는 `assertReported`, `assertNotReported` 메서드로 요청 처리 중 발생한 예외에 대해 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // Assert an exception was thrown...
    Exceptions::assertReported(InvalidOrderException::class);

    // Assert against the exception...
    Exceptions::assertReported(function (InvalidOrderException $e) {
        return $e->getMessage() === 'The order was invalid.';
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_exception_is_thrown(): void
    {
        Exceptions::fake();

        $response = $this->get('/');

        // Assert an exception was thrown...
        Exceptions::assertReported(InvalidOrderException::class);

        // Assert against the exception...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

`assertNotReported`, `assertNothingReported` 메서드를 사용하면 지정 예외가 발생하지 않았거나, 아무런 예외도 보고되지 않았는지 검증할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하려면 요청을 보내기 전에 `withoutExceptionHandling` 메서드를 사용하세요:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP나 외부 라이브러리에서 사용 중인 기능 중 더 이상 권장되지 않는(Deprecated) 기능이 애플리케이션에서 사용되는지 확인하고 싶다면, 요청을 보내기 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이 때 deprecation 처리가 비활성화되면 deprecation 경고가 예외로 변환되어 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드를 사용하면 특정 클로저 내 코드가 지정 타입의 예외를 던지는지 검증할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외를 직접 확인하고 추가 검증을 하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드는 주어진 클로저 내 코드가 예외를 발생시키지 않는지 확인할 때 사용합니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API와 그 응답을 테스트하기 위한 다양한 헬퍼도 제공합니다. 예를 들어 `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용하면 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 또한 데이터와 헤더도 손쉽게 전달할 수 있습니다. 아래 예시는 `/api/user`에 `POST` 요청을 보내고, 예상 JSON 데이터가 정상 반환되었는지 검증하는 코드입니다:

```php tab=Pest
<?php

test('making an api request', function () {
    $response = $this->postJson('/api/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
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

또한 JSON 응답 데이터를 배열 변수처럼 바로 접근할 수 있어, 원하는 값을 손쉽게 확인할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤, 주어진 배열이 애플리케이션이 반환한 JSON 응답 내부에 포함되어 있는지 검증합니다. 따라서 JSON 응답에 다른 속성이 더 있더라도, 요청한 정보 조각(fragment)만 있다면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### JSON 전체 일치 검증 (Asserting Exact JSON Matches)

앞서 설명한 `assertJson`은 일부 JSON 조각이 존재하는지 검사합니다. 애플리케이션이 반환한 JSON과 주어진 배열이 **정확히 일치**하는지 확인하려면 `assertExactJson` 메서드를 사용해야 합니다:

```php tab=Pest
<?php

test('asserting an exact json match', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertExactJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
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
#### JSON 경로 값 검증 (Asserting on JSON Paths)

JSON 응답에서 특정 경로에 지정된 데이터가 있는지 확인하려면 `assertJsonPath` 메서드를 사용하세요:

```php tab=Pest
<?php

test('asserting a json path value', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJsonPath('team.owner.name', 'Darian');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
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

`assertJsonPath`는 클로저도 받을 수 있으며, 이를 통해 동적으로 어서션 통과 여부를 결정할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유창한(Fluent) JSON 테스트 (Fluent JSON Testing)

Laravel은 애플리케이션의 JSON 응답을 더욱 명확하고 유연하게(flently) 어서션할 수 있는 방법도 제공합니다. 우선 `assertJson` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인수로 받아, 응답 JSON의 각 속성에 대해 세밀하게 검증할 수 있습니다. `where` 메서드는 특정 속성값 검증, `missing`은 속성이 없는지 확인에 사용합니다:

```php tab=Pest
use Illuminate\Testing\Fluent\AssertableJson;

test('fluent json', function () {
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
});
```

```php tab=PHPUnit
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * A basic functional test example.
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

위 예시처럼, 어서션 체인 마지막에 `etc` 메서드를 호출했습니다. `etc`는 JSON 객체에 다른 속성이 존재할 수도 있음을 Laravel에 알려주는 역할을 합니다. 만약 `etc`를 사용하지 않으면, 명시적으로 어서션하지 않은 추가 속성이 JSON 객체에 있을 때 테스트는 실패하게 됩니다.

이렇게 엄격한 검증은, 민감한 정보가 의도치 않게 노출되지 않도록 개발자에게 명확한 어서션 또는 `etc`로의 명시적 허용을 요구합니다.

다만, `etc`를 사용하지 않아도 JSON 객체 내부의 배열(네스팅된 배열)에는 적용되지 않습니다. `etc`는 해당 호출 위치(네스팅 레벨)에만 적용됩니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어서션

특정 속성이 존재하는지 또는 없는지를 검증하려면 `has`, `missing` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

여러 속성의 존재/부재를 동시에 검증하려면 `hasAll`, `missingAll`을 사용하면 편리합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

주어진 속성 중 하나라도 존재하면 통과시키고 싶다면 `hasAny` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 어서션

종종, 라우트가 여러 항목(예: 여러 사용자 등)이 포함된 JSON 응답을 반환하기도 합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이처럼 여러 항목이 있는 응답에서는 유창한 JSON 객체의 `has` 메서드를 사용해 응답에 기대하는 사용자 수가 맞는지 어서션할 수 있습니다. 예를 들어, 아래는 3명의 사용자가 반환되었는지, 그리고 첫 번째 사용자에 대해 추가적인 검증을 하는 코드입니다:

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
#### JSON 컬렉션 어서션 범위 지정

경우에 따라, 라우트가 특정 키로 할당된 JSON 컬렉션을 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이때, `has` 메서드를 활용하여 컬렉션의 아이템 개수와 특정 속성에 대한 어서션을 구체적으로 할 수 있습니다:

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

또는, `has`에 클로저를 세 번째 인수로 전달하면 컬렉션의 첫 번째 아이템에 대해 자동으로 범위 지정하여 검증할 수 있습니다:

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
#### JSON 타입(type) 검증

응답 JSON의 속성 타입만 검증하고 싶을 때는 `Illuminate\Testing\Fluent\AssertableJson` 클래스에서 제공하는 `whereType`, `whereAllType` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 허용하려면 `|` 문자나, 타입 배열을 두 번째 인수로 전달할 수 있습니다. 나열된 타입 중 하나라도 일치하면 성공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`, `whereAllType`에서는 `string`, `integer`, `double`, `boolean`, `array`, `null` 타입을 인식합니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 통해 테스트용 더미 파일이나 이미지를 쉽게 생성할 수 있습니다. 이 기능은 `Storage` 파사드의 `fake` 메서드와 함께 사용하면 파일 업로드 테스트를 훨씬 간편하게 해줍니다. 예를 들어, 아바타 업로드 폼 테스트는 다음과 같이 작성할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('avatars can be uploaded', function () {
    Storage::fake('avatars');

    $file = UploadedFile::fake()->image('avatar.jpg');

    $response = $this->post('/avatar', [
        'avatar' => $file,
    ]);

    Storage::disk('avatars')->assertExists($file->hashName());
});
```

```php tab=PHPUnit
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

특정 파일이 존재하지 않아야 한다는 점을 검증하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이즈

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때, 이미지의 폭, 높이, 크기(킬로바이트 단위)를 지정하여 애플리케이션의 유효성 검증(Validation) 규칙도 함께 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에 다른 형식의 파일도 `create` 메서드로 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, 메서드에 `$mimeType` 인자를 전달해 파일의 MIME 타입을 명확히 지정할 수도 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고도, 뷰 렌더링만을 테스트할 수 있게 해줍니다. 이를 위해 테스트 코드에서 `view` 메서드를 사용할 수 있습니다. 이 메서드는 뷰 이름과 옵션으로 데이터 배열을 받으며, `Illuminate\Testing\TestView` 인스턴스를 반환해 뷰의 내용을 편리하게 어서션할 수 있는 다양한 메서드를 제공합니다:

```php tab=Pest
<?php

test('a welcome view can be rendered', function () {
    $view = $this->view('welcome', ['name' => 'Taylor']);

    $view->assertSee('Taylor');
});
```

```php tab=PHPUnit
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

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 등 다양한 어서션 메서드를 제공합니다.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 렌더링된 뷰 원본을 바로 얻을 수도 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기

어떤 뷰는 [Laravel의 글로벌 에러 백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 있는 에러 정보를 참조할 수 있습니다. 에러 백에 에러 메시지를 미리 담으려면 `withViewErrors` 메서드를 사용할 수 있습니다:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면, `blade` 메서드를 사용해 [Blade](/docs/12.x/blade) 문자열을 바로 평가(render)할 수 있습니다. 이 메서드도 `view`와 마찬가지로 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

또한 `component` 메서드를 사용하면 [Blade 컴포넌트](/docs/12.x/blade#components)를 직접 평가할 수 있습니다. 이 경우 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션 (Available Assertions)

<a name="response-assertions"></a>
### 응답 어서션 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 테스트 시 활용할 수 있는 다양한 커스텀 어서션 메서드를 제공합니다. 이 메서드들은 `json`, `get`, `post`, `put`, `delete` 등의 테스트 메서드가 반환한 응답에 대해 사용 가능합니다:

<div class="collection-method-list" markdown="1">

[assertAccepted](#assert-accepted)
[assertBadRequest](#assert-bad-request)
[assertClientError](#assert-client-error)
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
[assertExactJsonStructure](#assert-exact-json-structure)
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
[assertStreamed](#assert-streamed)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPaymentRequired](#assert-payment-required)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectBack](#assert-redirect-back)
[assertRedirectBackWithErrors](#assert-redirect-back-with-errors)
[assertRedirectBackWithoutErrors](#assert-redirect-back-without-errors)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertServerError](#assert-server-error)
[assertServiceUnavailable](#assert-service-unavailable)
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
[assertUnsupportedMediaType](#assert-unsupported-media-type)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-accepted"></a>
#### assertAccepted

응답이 accepted (202) HTTP 상태 코드임을 검증합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 bad request (400) HTTP 상태 코드임을 검증합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 에러(400 이상 500 미만) HTTP 상태 코드임을 검증합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 conflict (409) HTTP 상태 코드임을 검증합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정한 쿠키가 포함되어 있는지 검증합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정한 쿠키가 존재하며, 만료되었는지 검증합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정한 쿠키가 존재하며, 만료되지 않았는지 검증합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않은지 검증합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 201 HTTP 상태 코드임을 검증합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 지정한 문자열이 포함되지 않았는지 검증합니다. 두 번째 인수로 `false`를 전달하지 않으면 문자열은 자동으로 이스케이프됩니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 지정한 문자열이 포함되지 않았는지 검증합니다. 두 번째 인수로 `false`를 전달하지 않으면 문자열은 자동으로 이스케이프됩니다. 이 검증은 PHP `strip_tags` 함수로 태그 제거 후 진행됩니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"인지(즉, `Response::download`, `BinaryFileResponse`, `Storage::download` 등으로 응답했는지) 검증합니다:

```php
$response->assertDownload();
```

특정 파일명이 맞는지도 검증할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 주어진 JSON 데이터와 정확히 일치하는지 검증합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 주어진 JSON 구조와 정확히 일치하는지 검증합니다:

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)의 더 엄격한 버전입니다. 예상 JSON 구조에 명시적으로 포함되지 않은 키가 응답에 있으면 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 forbidden (403) HTTP 상태 코드임을 검증합니다:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 found (302) HTTP 상태 코드임을 검증합니다:

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 gone (410) HTTP 상태 코드임을 검증합니다:

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정한 헤더와 값이 존재하는지 검증합니다:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정한 헤더가 존재하지 않는지 검증합니다:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 Internal Server Error (500) HTTP 상태 코드임을 검증합니다:

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 주어진 JSON 데이터가 포함되어 있는지 검증합니다:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환하여 주어진 배열이 응답의 어느 위치에든 포함되어 있는지 확인합니다. 응답 JSON에 다른 속성이 있더라도 이 조각이 존재한다면 테스트는 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON의 지정 key에 기대한 개수의 아이템이 있는지 검증합니다:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 지정한 JSON 데이터 조각이 어디에든 포함되어 있는지 검증합니다:

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

응답 JSON이 배열인지 검증합니다:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 검증합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정한 JSON 데이터가 포함되어 있지 않은지 검증합니다:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 지정한 JSON 데이터가 **정확히** 포함되어 있지 않은지 검증합니다:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 주어진 key에 해당하는 JSON 유효성 검증 에러가 존재하지 않는지 확인합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 더 범용적인 [assertValid](#assert-valid) 메서드는 JSON으로 반환된 유효성 검증 에러나 세션에 플래시된 에러가 없는지 함께 확인할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답의 지정 경로(path)에 주어진 데이터가 존재하는지 검증합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 다음과 같은 JSON 응답이 반환된다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

이렇게 `user` 객체의 `name` 속성이 값이 맞는지 확인할 수 있습니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답의 지정 경로(path)에 데이터가 존재하지 않는지 검증합니다:

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 위 JSON 응답에서 `user.email` 속성이 존재하지 않는지 확인할 수 있습니다:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 주어진 JSON 구조를 만족하는지 검증합니다:

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 아래와 같은 응답에 대해

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 구조를 어서션할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

만약 배열로 된 객체들이 있다면(`*` 사용):

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

모든 객체들의 구조를 한 번에 검증할 수 있습니다:

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

응답에 주어진 key에 JSON 유효성 검증 에러가 존재하는지 검증합니다. 이 메서드는 유효성 에러가 세션이 아닌 JSON으로 반환된 경우에 사용합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 더 범용적인 [assertInvalid](#assert-invalid) 메서드는 JSON과 세션 모두의 유효성 검증 에러에 대해 사용 가능합니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답에 지정한 key에 해당하는 JSON 유효성 검증 에러가 **존재하는지** 검증합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 method not allowed (405) HTTP 상태 코드임을 검증합니다:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 moved permanently (301) HTTP 상태 코드임을 검증합니다:

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답의 `Location` 헤더가 지정한 URI 값과 일치하는지 검증합니다:

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 본문이 주어진 문자열과 일치하는지 검증합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정 상태 코드와 함께 내용이 없는(no content)지 검증합니다:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트리밍 응답임을 검증합니다:

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트리밍된 응답의 내용이 주어진 문자열과 일치하는지 검증합니다:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 not found (404) HTTP 상태 코드임을 검증합니다:

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 200 HTTP 상태 코드임을 검증합니다:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 payment required (402) HTTP 상태 코드임을 검증합니다:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정한 **암호화되지 않은 쿠키(unencrypted cookie)** 가 있는지 검증합니다:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정한 URI로 리다이렉트되는지 검증합니다:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로 리다이렉트되는지 검증합니다:

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리다이렉트되고 [세션에 지정한 에러가 있는지](#assert-session-has-errors) 검증합니다:

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

응답이 이전 페이지로 리다이렉트되고, 세션에 에러 메시지가 없는지 검증합니다:

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 지정한 문자열을 포함하는 URI로 리다이렉트되는지 검증합니다:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 지정한 [이름 라우트](/docs/12.x/routing#named-routes)로 리다이렉트되는지 검증합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 지정한 [서명된 라우트](/docs/12.x/urls#signed-urls)로 리다이렉트되는지 검증합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 request timeout (408) HTTP 상태 코드임을 검증합니다:

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

응답에 지정한 문자열이 포함되어 있는지 검증합니다. 두 번째 인수로 `false`를 전달하지 않으면 문자열은 자동으로 이스케이프됩니다:

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답에 지정한 문자열들이 순서대로 등장하는지 검증합니다. 두 번째 인수로 `false`를 전달하지 않으면 문자열은 자동으로 이스케이프됩니다:

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 텍스트에 지정한 문자열이 포함되어 있는지 검증합니다. 두 번째 인수로 `false`를 전달하지 않으면 문자열은 자동으로 이스케이프됩니다. 응답은 PHP의 `strip_tags` 함수로 태그가 제거된 후 비교됩니다:

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에 지정한 문자열들이 순서대로 등장하는지 검증합니다. 두 번째 인수로 `false`를 전달하지 않으면 문자열은 자동으로 이스케이프됩니다. 응답은 `strip_tags`로 태그 제거 후 비교합니다:

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 에러(500 이상, 600 미만) HTTP 상태 코드임을 검증합니다:

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 Service Unavailable (503) HTTP 상태 코드임을 검증합니다:

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정 데이터를 포함하고 있는지 검증합니다:

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 전달할 수 있고, 해당 값에 대해 `true`를 반환하면 어서션이 통과됩니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션의 [flashed input array](/docs/12.x/responses#redirecting-with-flashed-session-data)에 지정 값이 포함되어 있는지 검증합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인수로 클로저를 전달하면 조건에 맞춰(indirect) 비교할 수 있습니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정 key/value 쌍들이 모두 존재하는지 검증합니다:

```php
$response->assertSessionHasAll(array $data);
```

예시:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 지정 `$keys`에 대한 에러가 존재하는지 검증합니다. `$keys`가 연관 배열(associative array)이면 각 키와 값 조합에 대해 검증합니다. 이 메서드는 유효성 검증 에러가 세션에 플래시된 경우에 씁니다:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예시:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

또는, 특정 필드에 명확한 에러 메시지가 있는지도 확인 가능합니다:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 더 범용적인 [assertInvalid](#assert-invalid) 메서드는 JSON과 세션 모두의 유효성 에러를 검사 가능하게 해줍니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [에러백(error bag)](/docs/12.x/validation#named-error-bags) 내에 `$keys` 에러가 있는지 검증합니다. 이 역시 연관 배열 형태라면 key/value 모두 검증합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 에러가 **없는지** 검증합니다:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 지정 키에 대해 유효성 검증 에러가 없는지 검증합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 더 범용적인 [assertValid](#assert-valid) 메서드는 JSON과 세션 모두의 유효성 검증 에러가 없는지도 함께 확인할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정 key가 존재하지 않는지 검증합니다:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답의 HTTP 상태 코드가 지정한 값과 일치하는지 검증합니다:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공 상태(200 이상, 300 미만) HTTP 상태 코드인지 검증합니다:

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 too many requests (429) HTTP 상태 코드임을 검증합니다:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 unauthorized (401) HTTP 상태 코드임을 검증합니다:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 unprocessable entity (422) HTTP 상태 코드임을 검증합니다:

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 unsupported media type (415) HTTP 상태 코드임을 검증합니다:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답에 지정한 키에 유효성 검증 에러가 **없는지** 검증합니다. JSON, 세션 모두의 검증 에러에 사용할 수 있습니다:

```php
// 유효성 검증 에러가 전혀 없는지...
$response->assertValid();

// 지정 키에 에러가 없는지...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 지정한 키에 유효성 검증 에러가 **있는지** 검증합니다. JSON, 세션 모두의 검증 에러에 사용할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 특정 에러 메시지가 있는지도 어서션 가능합니다. 이때 전체 메시지 또는 일부 메시지도 사용할 수 있습니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

지정한 필드만 에러가 있어야 함을 검증하고 싶다면 `assertOnlyInvalid` 메서드를 사용할 수 있습니다:

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 지정 데이터가 포함되어 있는지 검증합니다:

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 전달하면 뷰 데이터에 대한 상세 조건도 검증할 수 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한, 뷰 데이터는 응답 배열 변수로 바로 접근할 수 있어 결과값을 편리하게 확인할 수 있습니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰가 지정 데이터 목록을 모두 가지고 있는지 검증합니다:

```php
$response->assertViewHasAll(array $data);
```

예를 들어, 단순히 데이터가 존재하는지 검사하거나

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

특정 값까지도 함께 검증할 수 있습니다:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

라우트가 반환한 뷰가 지정 값과 일치하는지 검증합니다:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 지정 키 데이터가 **제공되지 않았는지** 검증합니다:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어서션 (Authentication Assertions)

Laravel은 애플리케이션 기능 테스트 내부에서 사용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 이 메서드들은 테스트 클래스에서 직접 호출해야 하며, `Illuminate\Testing\TestResponse` 인스턴스에서는 사용할 수 없습니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 검증합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지(비로그인인지) 검증합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 검증합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어서션 (Validation Assertions)

Laravel은 요청 데이터가 유효하거나 유효하지 않았음을 보장하기 위한 두 가지 주요 유효성 검증 어서션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 지정 키에 유효성 에러가 없는지 확인합니다. 이 메서드는 응답이 JSON 방식이거나, 세션에 플래시된 경우 모두에 사용할 수 있습니다:

```php
// 유효성 에러가 전혀 없는지 어서션
$response->assertValid();

// 지정 키에 유효성 에러가 없는지 어서션
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 지정 키에 유효성 검증 에러가 포함되어 있는지 확인합니다. (JSON, 세션 모두 사용 가능):

```php
$response->assertInvalid(['name', 'email']);
```

특정 키의 특정 에러 메시지도 어서션할 수 있습니다. 전체 메시지 또는 일부만 입력해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
