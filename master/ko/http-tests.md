# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
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
- [라우트 캐싱](#caching-routes)
- [사용 가능한 단언 목록](#available-assertions)
    - [응답 단언](#response-assertions)
    - [인증 단언](#authentication-assertions)
    - [유효성 검증 단언](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 아래의 기능 테스트(feature test)를 살펴보세요:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 전달된 HTTP 상태 코드를 갖는지 확인합니다. 이 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등 다양한 항목을 검사할 수 있는 여러 단언 메서드를 제공합니다.

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 호출하면 됩니다. 이 메서드들은 실제로 "진짜" HTTP 요청을 발생시키는 것이 아니라, 네트워크 요청 전체를 내부적으로 시뮬레이션합니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이를 통해 [여러 유용한 단언 메서드](#available-assertions)를 사용하여 애플리케이션의 응답을 손쉽게 검사할 수 있습니다:

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

일반적으로 각 테스트에서는 한 번의 요청만 보내야 합니다. 하나의 테스트 메서드 내에서 여러 번의 요청이 실행되면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해, 테스트 실행 시 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이즈 (Customizing Request Headers)

요청을 보내기 전에 `withHeaders` 메서드를 사용하여 요청의 헤더를 커스터마이즈할 수 있습니다. 이 메서드를 이용하면 원하는 모든 커스텀 헤더를 요청에 추가할 수 있습니다:

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

요청 전에 쿠키 값을 지정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 인수로 받고, `withCookies`는 이름/값 쌍의 배열을 받습니다:

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

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 여러 도우미 메서드를 제공합니다. 먼저, `withSession`을 이용해 세션 데이터를 특정 배열로 설정할 수 있습니다. 이는 요청을 보내기 전에 필요한 데이터를 세션에 미리 저장하는 데 유용합니다:

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

Laravel의 세션은 주로 현재 인증된 사용자의 상태를 관리하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 지정한 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/master/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

`actingAs` 메서드의 두 번째 인수로 가드(guard) 이름을 전달하여, 어떤 가드를 이용해 인증할지 지정할 수도 있습니다. 이 메서드에 전달된 가드는 테스트 전체에서 기본 가드로 동작합니다:

```php
$this->actingAs($user, 'web');
```

반대로 인증되지 않은 상태로 요청을 실행하고 싶다면 `actingAsGuest` 메서드를 사용할 수 있습니다:

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

애플리케이션에 테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 확인하고 디버깅할 수 있습니다:

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dump();
    $response->dumpHeaders();
    $response->dumpSession();
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

        $response->dump();
        $response->dumpHeaders();
        $response->dumpSession();
    }
}
```

또는, `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용해 응답 정보를 덤프하고 이후 실행을 즉시 중단할 수도 있습니다:

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

애플리케이션이 특정 예외를 발생시키는지 테스트해야 할 때가 있습니다. 이를 위해 `Exceptions` 파사드를 이용해 예외 핸들러를 "가짜(fake)"로 만들 수 있습니다. 이렇게 하면, 요청 도중 발생한 예외에 대해 `assertReported`와 `assertNotReported` 메서드로 단언할 수 있습니다:

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

`assertNotReported`, `assertNothingReported` 메서드는 요청 도중 특정 예외가 발생하지 않았음을, 또는 어떤 예외도 발생하지 않았음을 단언할 때 사용합니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에서 예외 처리를 완전히 비활성화하려면, 요청 전에 `withoutExceptionHandling`을 호출하면 됩니다:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 언어나 사용하는 라이브러리에서 더 이상 지원되지 않는(deprecated) 기능을 애플리케이션이 사용하지 않도록 보장하려면, 요청 전에 `withoutDeprecationHandling`을 호출할 수 있습니다. 이 상태에서는 deprecated 경고가 exception으로 변환되어, 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 주어진 클로저 내부의 코드가 지정한 타입의 예외를 발생시키는지 단언합니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외를 검사하고 추가 단언을 하고 싶을 때는, `assertThrows` 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow`는 클로저 내 코드가 어떠한 예외도 발생시키지 않는지 확인할 때 사용합니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API 및 그 응답을 테스트할 수 있는 여러 가지 도우미 메서드도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용하면 HTTP 메서드별로 JSON 요청을 쉽게 테스트할 수 있습니다. 이 메서드들에는 데이터와 헤더도 간편하게 전달할 수 있습니다. 다음은 `/api/user`에 `POST` 요청을 보내고 예상하는 JSON 데이터가 반환되는지 단언하는 테스트 예시입니다:

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

또한, JSON 응답 데이터는 배열 변수처럼 접근할 수 있어, 반환된 개별 값을 쉽게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤, 전달받은 배열이 애플리케이션이 반환한 JSON 응답 내에 존재하는지 확인합니다. 즉, JSON 응답에 다른 속성이 함께 존재하더라도, 주어진 부분(fragment)만 포함되어 있다면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 단언 (Asserting Exact JSON Matches)

앞에서 살펴본 것처럼, `assertJson`은 JSON의 일부분이 존재하는지 확인합니다. 전체 JSON이 **정확히** 일치하는지 확인하려면 `assertExactJson` 메서드를 사용해야 합니다:

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
#### JSON 경로 단언 (Asserting on JSON Paths)

JSON 응답에서 특정 경로에 원하는 데이터가 포함되어 있는지 확인하고 싶다면, `assertJsonPath` 메서드를 사용할 수 있습니다:

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

`assertJsonPath`는 클로저도 받을 수 있어, 동적으로 조건을 평가해 단언할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유창한(Fluent) JSON 테스트

Laravel은 JSON 응답을 더욱 직관적이고 유창하게 테스트할 수 있는 기능도 제공합니다. 먼저, `assertJson` 메서드에 클로저를 전달하면, 클로저 내부에서 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 받아 JSON 응답에 대해 다양한 단언을 수행할 수 있습니다. `where` 메서드는 특정 속성에 대해, `missing`은 특정 속성이 없는지 단언할 때 사용합니다:

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

위 예시에서 단언 체인의 마지막에 `etc` 메서드를 호출했습니다. 이 메서드는 JSON 객체에 추가적인 속성이 있을 수도 있음을 Laravel에 알리는 역할을 합니다. 반대로 `etc`를 사용하지 않으면, 단언하지 않은 속성이 존재하는 경우 테스트가 실패합니다.

이러한 동작의 목적은, JSON 응답에서 민감 정보가 의도치 않게 노출되는 것을 방지하기 위함입니다. 즉, 명시적으로 단언하거나, `etc`로 추가 속성을 허용하라는 의도입니다.

단, `etc`를 단언 체인에 포함하지 않는다고 해서, 중첩된 배열 내부에 추가 속성이 있는지까지 보장해 주지는 않습니다. `etc`는 자신이 호출된 그 수준에서만 추가 속성을 허용합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 단언

특정 속성이 존재하는지 또는 없는지 단언하려면, `has`, `missing` 메서드를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

여러 속성에 대해 한 번에 단언하려면 `hasAll`, `missingAll` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

여러 속성 중 하나라도 존재하면 통과시키고 싶다면 `hasAny`를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 단언

라우트가 여러 항목(예: 여러 사용자)을 포함하는 JSON 응답을 반환하는 경우가 많습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이 상황에서는, 유창 JSON 객체의 `has` 메서드를 활용해 사용자의 개수 등 컬렉션에 대한 단언을 할 수 있습니다. 예를 들어, 응답에 사용자가 3명 포함됐는지, 그리고 첫 번째 사용자의 정보를 추가로 단언하는 예시입니다:

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
#### JSON 컬렉션 단언 범위 지정(Scoping)

경우에 따라, 라우트가 명명된 키(예: `users`)로 할당된 JSON 컬렉션을 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이런 경우, `has`를 사용하여 각 컬렉션의 항목 개수 확인 및 체이닝된 단언을 할 수 있습니다:

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

이렇게 두 번의 `has`를 나눠서 호출하는 대신, 하나의 `has` 호출에서 세 번째 인수로 클로저를 전달해 첫 번째 항목에 대해 자동으로 단언을 수행하게 할 수도 있습니다:

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
#### JSON 타입 단언

JSON 응답의 속성이 특정 타입인지 단언하고 싶다면, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`과 `whereAllType` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`|` 문자를 사용하거나 타입 배열을 두 번째 인수로 넘겨 여러 타입을 허용할 수도 있습니다. 응답 값이 지정된 타입 중 하나에 해당하면 테스트가 통과합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`과 `whereAllType` 메서드는 `string`, `integer`, `double`, `boolean`, `array`, `null` 타입을 인식합니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스는 테스트를 위한 더미 파일 또는 이미지를 생성할 수 있는 `fake` 메서드를 제공합니다. 이것을 `Storage` 파사드의 `fake` 메서드와 함께 사용하면, 파일 업로드 테스트가 아주 간단해집니다. 예를 들어, 사용자 아바타(avatar) 업로드 폼을 손쉽게 테스트할 수 있습니다:

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

특정 파일이 존재하지 않는지 단언하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용하세요:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 더미 파일 커스터마이즈

`UploadedFile`의 `fake` 메서드를 통해 이미지를 생성할 때, 너비, 높이, 파일 크기(킬로바이트 단위)를 지정하여 애플리케이션의 유효성 검사 규칙을 더 잘 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에 다른 파일 유형도 `create` 메서드로 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면 `$mimeType` 인수를 첨부해, 생성할 파일의 MIME 타입을 명시할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel에서는 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고도 뷰를 렌더링할 수 있습니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하세요. `view`는 뷰 이름과 옵션 데이터 배열을 인수로 받으며, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 반환 객체에서는 여러 단언 메서드로 뷰 내용을 간편하게 검사할 수 있습니다:

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

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 단언 메서드를 제공합니다.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅해 렌더된 뷰의 원본 내용을 가져올 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기

일부 뷰는 [Laravel에서 제공하는 전역 에러 백(error bag)](/docs/master/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존할 수 있습니다. 에러 백에 메시지를 채우려면 `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링 (Rendering Blade and Components)

필요하다면, `blade` 메서드를 이용해 원시 Blade 문자열을 평가 및 렌더링할 수 있습니다. `view` 메서드와 마찬가지로, `blade`도 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/master/blade#components)를 평가 및 렌더링할 때는 `component` 메서드를 사용하면 됩니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="caching-routes"></a>
## 라우트 캐싱 (Caching Routes)

테스트 실행 전에는 Laravel이 모든 정의된 라우트를 로드하여 애플리케이션 인스턴스를 재구동합니다. 라우트 파일이 많은 애플리케이션이라면, 테스트 케이스에 `Illuminate\Foundation\Testing\WithCachedRoutes` 트레이트를 추가하는 것이 유용합니다. 이 트레이트를 사용하는 테스트의 경우, 라우트가 딱 한 번만 빌드되어 메모리에 저장되므로, 테스트 전체에서 라우트 수집 과정이 한 번만 실행됩니다:

```php tab=Pest
<?php

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;

pest()->use(WithCachedRoutes::class);

test('basic example', function () {
    $this->get(action([UserController::class, 'index']));

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;
use Tests\TestCase;

class BasicTest extends TestCase
{
    use WithCachedRoutes;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get(action([UserController::class, 'index']));

        // ...
    }
}
```

<a name="available-assertions"></a>
## 사용 가능한 단언 목록 (Available Assertions)

<a name="response-assertions"></a>
### 응답 단언 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트에 사용할 수 있는 다양한 맞춤 단언 메서드를 제공합니다. 이 단언들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답에서 사용할 수 있습니다:

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
[assertHeaderContains](#assert-header-contains)
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

응답이 accepted(202) HTTP 상태 코드인지 단언합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 bad request(400) HTTP 상태 코드인지 단언합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 에러(>= 400, < 500) HTTP 상태 코드인지 단언합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 conflict(409) HTTP 상태 코드인지 단언합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답이 해당 쿠키를 포함하는지 단언합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 해당 쿠키가 포함되고, 해당 쿠키가 만료되었는지 단언합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 해당 쿠키가 포함되고, 만료되지 않았는지 단언합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 해당 쿠키가 포함되어 있지 않은지 단언합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 201 HTTP 상태 코드인지 단언합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

지정한 문자열이 애플리케이션의 응답에 포함되어 있지 않은지 단언합니다. 두 번째 인수로 `false`를 전달하지 않는 한, 주어진 문자열은 자동으로 이스케이프됩니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

지정한 문자열이 응답 텍스트에 포함되지 않았는지 단언합니다. 두 번째 인수로 `false`를 전달하지 않는 한, 주어진 문자열은 자동으로 이스케이프됩니다. `strip_tags` PHP 함수를 통해 응답 내용이 처리된 뒤 단언이 이뤄집니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"로 간주되는지 단언합니다. 일반적으로 라우트에서 `Response::download`, `BinaryFileResponse`, `Storage::download`를 반환한 경우입니다:

```php
$response->assertDownload();
```

파일명이 특정 값인지도 단언할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 주어진 JSON 데이터와 정확히 일치하는지 단언합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 주어진 JSON 구조와 정확히 일치하는지 단언합니다:

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 엄격합니다. 기대한 구조에 포함되지 않은 키가 응답에 있을 경우 테스트가 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 forbidden(403) HTTP 상태 코드인지 단언합니다:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 found(302) HTTP 상태 코드인지 단언합니다:

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 gone(410) HTTP 상태 코드인지 단언합니다:

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정한 헤더와 값이 포함되어 있는지 단언합니다:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-contains"></a>
#### assertHeaderContains

응답에 지정한 헤더에 특정 부분 문자열이 포함되어 있는지 단언합니다:

```php
$response->assertHeaderContains($headerName, $value);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정한 헤더가 없는지 단언합니다:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 "Internal Server Error"(500) HTTP 상태 코드인지 단언합니다:

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답이 주어진 JSON 데이터를 포함하는지 단언합니다:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환하여 주어진 배열이 JSON 응답 내에 존재하는지 확인합니다. JSON 응답에 다른 속성이 존재해도, 부분이 일치하면 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답의 JSON에서, 지정한 키의 배열 길이가 예상한 개수와 맞는지 단언합니다:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답 어디에든 주어진 JSON 데이터가 포함되어 있는지 단언합니다:

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

응답의 JSON이 배열인지 단언합니다:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답의 JSON이 객체인지 단언합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답이 주어진 JSON 데이터를 포함하지 않는지 단언합니다:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답이 전달된 JSON 데이터와 정확히 일치하는 데이터를 포함하지 않는지 단언합니다:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

지정한 키에 대한 JSON 유효성 검증 에러가 응답에 없는지 단언합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하면, 응답에 반환된 JSON 유효성 검증 오류가 없고 세션에도 오류가 없는지 확인할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답이 지정한 경로에 특정 데이터를 포함하는지 단언합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 다음과 같은 JSON 응답이 반환됐다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 `user` 객체의 `name` 속성이 예상한 값과 일치하는지 단언할 수 있습니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정한 경로가 존재하지 않는지 단언합니다:

```php
$response->assertJsonMissingPath($path);
```

예시:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래와 같이 `user` 객체에 `email` 속성이 없는지 단언할 수 있습니다:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 주어진 JSON 구조를 만족하는지 단언합니다:

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 다음과 같은 응답 데이터가 있을 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 구조를 단언할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

애플리케이션이 객체 배열을 포함하는 JSON을 반환할 경우:

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

모든 배열 요소의 구조를 단언하고 싶다면 `*` 문자를 사용합니다:

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

지정한 키에 대해 JSON 유효성 검증 오류가 있는지 단언합니다. 이 메서드는 유효성 검증 오류가 세션이 아닌 JSON 구조로 반환된 경우에 사용해야 합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는, 응답의 JSON이나 세션에 유효성 검증 오류가 존재하는지 함께 단언할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

지정한 키에 대해 JSON 유효성 검증 오류가 있는지 단언합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 method not allowed(405) HTTP 상태 코드인지 단언합니다:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 moved permanently(301) HTTP 상태 코드인지 단언합니다:

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답에 주어진 URI가 `Location` 헤더로 설정됐는지 단언합니다:

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

지정한 문자열이 응답 내용과 완전히 일치하는지 단언합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 주어진 HTTP 상태 코드이고, 내용이 없는지 단언합니다:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트림(Stream) 형태로 반환됐는지 단언합니다:

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

지정한 문자열이 스트리밍 응답 내용과 일치하는지 단언합니다:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 not found(404) HTTP 상태 코드인지 단언합니다:

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 200 HTTP 상태 코드인지 단언합니다:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 payment required(402) HTTP 상태 코드인지 단언합니다:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정한 비암호화(plain) 쿠키가 포함되어 있는지 단언합니다:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 주어진 URI로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로 리다이렉트 중인지 단언합니다:

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리다이렉트되고, [세션에 지정한 에러가 있는지](#assert-session-has-errors) 단언합니다:

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

응답이 이전 페이지로 리다이렉트되고, 세션에 에러 메시지가 없는지 단언합니다:

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 리다이렉트되는 URI에 지정한 문자열이 포함돼 있는지 단언합니다:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 [지정한 네임드 라우트](/docs/master/routing#named-routes)로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 [지정한 서명된 라우트](/docs/master/urls#signed-urls)로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 request timeout(408) HTTP 상태 코드인지 단언합니다:

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

지정한 문자열이 응답에 포함되어 있는지 단언합니다. 두 번째 인수로 `false`를 주지 않는 한, 자동으로 이스케이프 처리됩니다:

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

지정한 문자열들이 응답에 순서대로 포함되어 있는지 단언합니다. 두 번째 인수로 `false`를 주지 않는 한, 자동 이스케이프됩니다:

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

지정한 문자열이 응답 텍스트 내에 포함되어 있는지 단언합니다. 두 번째 인수로 `false`를 주지 않는 한, 자동 이스케이프됩니다. 응답 내용은 `strip_tags` PHP 함수로 처리된 뒤 단언됩니다:

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

지정한 문자열들이 응답 텍스트 내에 순서대로 포함되는지 단언합니다. 두 번째 인수로 `false`를 주지 않는 한, 자동 이스케이프됩니다. 응답 내용은 `strip_tags`로 처리된 뒤 단언됩니다:

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 에러(>= 500, < 600) HTTP 상태 코드인지 단언합니다:

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 "Service Unavailable"(503) HTTP 상태 코드인지 단언합니다:

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정한 데이터가 있는지 단언합니다:

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 전달해, 값 자체를 검사하거나 추가 단언을 할 수 있습니다. 클로저가 `true`를 반환하면 단언이 통과합니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

[플래시 입력 배열](/docs/master/responses#redirecting-with-flashed-session-data)에 값이 있는지 단언합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인수로 클로저를 전달하면, 플래시 입력 값을 직접 검사할 수 있습니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정한 키/값 배열이 모두 존재하는지 단언합니다:

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

세션에 지정한 `$keys`에 대한 에러 메시지가 있는지 단언합니다. 만약 `$keys`가 연관 배열이면, 각 필드(키)에 대해 특정 에러 메시지(값)가 존재하는지 검사합니다. 이 메서드는 유효성 검증 에러가 JSON이 아니라 세션으로 플래시된 경우에 사용하세요:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예시:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드가 특정 에러 메시지를 포함하는지도 단언할 수 있습니다:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는, 응답의 JSON이나 세션에 유효성 검증 오류가 존재하는지 함께 단언할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

[에러 백](/docs/master/validation#named-error-bags) 내에서 `$keys`에 대한 에러가 있는지 단언합니다. `$keys`가 연관 배열이면, 각 필드(키)마다 특정 메시지(값)가 해당 에러 백에 포함돼 있는지 확인합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 에러가 전혀 없는지 단언합니다:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

지정한 키에 대한 유효성 검증 에러가 세션에 없는지 단언합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는, 응답에 반환된 JSON 유효성 검증 오류가 없고 세션에도 오류가 없는지 확인할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정한 키가 포함되어 있지 않은지 단언합니다:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 지정한 HTTP 상태 코드인지 단언합니다:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공적인(>= 200, < 300) HTTP 상태 코드인지 단언합니다:

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 too many requests(429) HTTP 상태 코드인지 단언합니다:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 unauthorized(401) HTTP 상태 코드인지 단언합니다:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 unprocessable entity(422) HTTP 상태 코드인지 단언합니다:

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 unsupported media type(415) HTTP 상태 코드인지 단언합니다:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답의 지정한 키에 대해 유효성 검증 오류가 없는지 단언합니다. 이 메서드는 JSON 구조로 반환된 오류와 세션에 플래시된 오류 모두 단언할 수 있습니다:

```php
// 유효성 검증 오류가 없는지 단언...
$response->assertValid();

// 지정한 키에 유효성 검증 오류가 없는지 단언...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답의 지정한 키에 대해 유효성 검증 오류가 있는지 단언합니다. 이 메서드는 JSON 구조로 반환된 오류와 세션에 플래시된 오류 모두 단언할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 특정 유효성 검증 에러 메시지가 있는지도 단언할 수 있으며, 메시지 전체 또는 일부만 일치해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

지정한 필드만 유효성 검증 오류가 있는지 단언하려면 `assertOnlyInvalid`를 사용하십시오:

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 지정한 데이터가 포함되어 있는지 단언합니다:

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 전달하면, 뷰 데이터에 대해 직접 검사하거나 추가 단언을 할 수 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한, 뷰 데이터는 응답에서 배열 변수처럼 접근할 수 있으므로 편리하게 검사할 수 있습니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 지정한 데이터 목록이 모두 포함되어 있는지 단언합니다:

```php
$response->assertViewHasAll(array $data);
```

다음처럼 키 목록만으로 데이터를 단언하거나,

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

아래처럼 값까지 포함해서 단언할 수도 있습니다:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

해당 뷰가 라우트에 의해 반환됐는지 단언합니다:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

해당 데이터 키가 응답 뷰에 전달되지 않았는지 단언합니다:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 단언 (Authentication Assertions)

Laravel은 애플리케이션의 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 단언도 제공합니다. 이 메서드들은 반드시 테스트 클래스 자체에서 호출해야 하며, `get`/`post` 등이 반환하는 `Illuminate\Testing\TestResponse` 인스턴스에서는 사용할 수 없습니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되어 있는지 단언합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되어 있지 않은(게스트) 상태인지 단언합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되어 있는지 단언합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 단언 (Validation Assertions)

Laravel은 요청 데이터의 유효성 여부를 보장하기 위한 두 가지 주요 유효성 검증 관련 단언을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답의 지정한 키에 대해 유효성 검증 오류가 없는지 단언합니다. 이 메서드는 JSON 구조로 반환된 오류와 세션에 플래시된 오류 모두 단언할 수 있습니다:

```php
// 유효성 검증 오류가 없는지 단언...
$response->assertValid();

// 지정한 키에 유효성 검증 오류가 없는지 단언...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답의 지정한 키에 대해 유효성 검증 오류가 있는지 단언합니다. 이 메서드는 JSON 구조로 반환된 오류와 세션에 플래시된 오류 모두 단언할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 특정 유효성 검증 에러 메시지가 있는지도 단언할 수 있습니다. 전체 메시지나 일부 일치 모두 가능합니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
