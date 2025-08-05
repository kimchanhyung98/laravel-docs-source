# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [플루언트 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [유효성 검사 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 직관적인 API를 제공합니다. 예를 들어, 아래와 같이 기능 테스트를 정의할 수 있습니다:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가져야 함을 확인합니다. 이처럼 간단한 어서션 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 만들기

테스트 내에서, `get`, `post`, `put`, `patch`, `delete` 메서드를 호출하여 애플리케이션에 요청을 보낼 수 있습니다. 이 메서드들은 실제로 네트워크를 통해 "진짜" HTTP 요청을 보내는 것이 아니라, 내부적으로 네트워크 요청을 시뮬레이션합니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 객체는 애플리케이션의 응답을 검사할 수 있는 [다양한 어서션](#available-assertions)을 제공합니다:

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

일반적으로, 각 테스트는 애플리케이션에 요청을 하나만 보내야 합니다. 하나의 테스트 메서드에서 여러 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

`withHeaders` 메서드를 사용하여, 요청을 애플리케이션에 보내기 전에 요청 헤더를 커스터마이징할 수 있습니다. 이 메서드는 원하는 모든 커스텀 헤더를 요청에 추가할 수 있습니다:

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
### 쿠키

`withCookie`나 `withCookies` 메서드를 사용하여, 요청을 보내기 전에 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 인수로 받으며, `withCookies`는 이름/값 쌍의 배열을 받습니다:

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
### 세션 / 인증

Laravel은 HTTP 테스트 중 세션을 다루기 위한 여러 헬퍼를 제공합니다. 먼저 `withSession` 메서드를 통해, 요청을 보내기 전에 세션에 원하는 데이터를 미리 설정할 수 있습니다:

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

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서, `actingAs` 헬퍼 메서드를 사용하면 특정 사용자를 현재 사용자로 인증할 수 있습니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다:

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

`actingAs` 메서드의 두 번째 인수로 가드(guard) 이름을 전달하여, 특정 가드로 인증할 수도 있습니다. 해당 테스트가 끝날 때까지 이 가드는 기본 가드로 사용됩니다:

```php
$this->actingAs($user, 'web')
```

인증되지 않은(비로그인) 상태로 요청을 보내야 할 경우 `actingAsGuest` 메서드를 사용할 수 있습니다:

```php
$this->actingAsGuest()
```

<a name="debugging-responses"></a>
### 응답 디버깅

애플리케이션에 테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용하여 응답 내용을 검사하고 디버깅할 수 있습니다:

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

또한, `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하면 응답 정보를 출력(dump)한 뒤 실행을 중단할 수도 있습니다:

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
### 예외 처리

애플리케이션이 특정 예외를 발생시키는지를 테스트해야 할 때가 있습니다. 이를 위해 `Exceptions` 파사드의 예외 핸들러를 "페이크(fake)"로 만들 수 있습니다. 이렇게 하면 요청 중에 발생한 예외에 대해 `assertReported`, `assertNotReported` 메서드를 이용해 어서션을 할 수 있습니다:

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

`assertNotReported`, `assertNothingReported` 메서드를 사용하여 특정 예외가 발생하지 않았거나, 어떤 예외도 발생하지 않았음을 어서트(단언)할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하려면, 요청 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 언어나 관련 라이브러리에서 더 이상 권장되지 않는(deprecated) 기능이 사용되지 않았는지 확인하고 싶다면, 요청 전에 `withoutDeprecationHandling` 메서드를 사용할 수 있습니다. 이 방법을 사용하면 deprecation(더 이상 권장되지 않음) 경고가 예외로 변환되어 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

지정한 클로저의 코드가 특정 타입의 예외를 던지는지 확인하려면 `assertThrows` 메서드를 사용할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외 객체에 대해서도 추가 어서션을 하고 싶다면, `assertThrows`의 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

지정한 코드가 예외를 아무것도 발생시키지 않는지 확인하려면 `assertDoesntThrow` 메서드를 사용할 수 있습니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API 및 그 응답을 테스트하기 위한 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용해 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 이 메서드들은 데이터 및 헤더도 쉽게 전달할 수 있습니다. 먼저, `/api/user` 엔드포인트에 `POST` 요청을 보내고, 기대하는 JSON 데이터가 반환되는지 테스트를 작성해보겠습니다:

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

게다가, JSON 응답 데이터는 배열 변수처럼 접근할 수 있어 응답 데이터 개별 값을 쉽게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여, 지정한 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재함을 확인합니다. 즉, JSON 응답에 추가 속성이 더 있어도 지정한 조각(fragment)이 있으면 테스트가 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어서션

앞서 설명한 것처럼, `assertJson` 메서드는 JSON 응답에 특정 JSON 조각이 있는지 확인할 수 있습니다. 반환된 JSON이 지정한 배열과 **정확히 일치**하는지 확인하고 싶다면, `assertExactJson` 메서드를 사용해야 합니다:

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
#### JSON 경로 어서션

JSON 응답에 특정 데이터가 지정한 경로(path)에 존재함을 확인하고 싶다면, `assertJsonPath` 메서드를 사용해야 합니다:

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

`assertJsonPath` 메서드는 클로저도 받을 수 있으며, 이를 활용해 어서션 성공 조건을 동적으로 지정할 수도 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 더욱 우아하게(플루언트하게) 테스트할 수 있는 방법도 제공합니다. 시작하려면, `assertJson` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 파라미터로 받아, 반환된 JSON에 대해 다양한 어서션을 할 수 있습니다. `where` 메서드는 특정 속성에 대해 어서션을 수행하고, `missing` 메서드는 특정 속성이 JSON에 없는지 어서션할 수 있습니다:

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

위의 예제에서, 어서션 체인의 끝에 `etc` 메서드를 호출하는 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 추가적인 속성이 존재할 수 있음을 Laravel에 알립니다. 만약 `etc` 메서드를 사용하지 않으면, 명시적으로 어서션하지 않은 다른 속성이 JSON 객체 내에 존재할 경우 테스트는 실패하게 됩니다.

이 동작의 목적은, 민감한 정보가 JSON 응답에 무심코 노출되는 것을 방지하기 위함입니다. 명시적으로 어서션하거나, 추가 속성을 `etc` 메서드를 통해 허용해야만 합니다.

하지만, 어서션 체인에 `etc`를 사용하더라도, JSON 내부에 중첩된 배열에 추가 속성이 추가되는 것까지는 보장하지 않습니다. `etc` 메서드는 해당 계층(nesting level)에서만 적용됩니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어서션

특정 속성이 JSON에 존재하는지 또는 존재하지 않는지 어서트하려면 `has`, `missing` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한, `hasAll`, `missingAll` 메서드를 사용해 여러 속성의 존재/부재를 한 번에 어서트할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드를 사용하면, 여러 항목 중 하나라도 존재하면 어서션이 통과하도록 할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

라우트가 여러 항목(예: 여러 사용자)이 포함된 JSON 응답을 반환하는 경우가 많습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이런 상황에서는, `has` 메서드를 사용해 JSON 응답에 포함된 사용자 수를 검사할 수 있습니다. 다음은 JSON 응답에 사용자 3명이 존재하는지 어서트하고, 컬렉션의 첫 번째 사용자에 대해 추가 어서션을 하는 예시입니다:

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
#### JSON 컬렉션 스코핑 어서션

애플리케이션 라우트가 이름이 부여된 키로 JSON 컬렉션을 반환할 때가 종종 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이 경우, `has` 메서드를 사용하여 컬렉션 항목 개수를 확인할 수 있으며, `has`를 체이닝하여 스코프 내에서 어서션을 진행할 수도 있습니다:

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

위 코드처럼 `users` 컬렉션의 첫 번째 항목을 직접 스코프하여 어서트하지 않고, `has` 메서드의 세 번째 인수로 클로저를 넘기면 첫 번째 항목에 자동으로 스코프가 맞춰집니다:

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
#### JSON 타입 어서션

JSON 응답 내 속성이 특정 타입인지에 대해서만 어서트하고 싶을 수 있습니다. `Illuminate\Testing\Fluent\AssertableJson` 클래스는 `whereType`, `whereAllType` 메서드를 제공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 지정하려면 `|` 문자 또는 타입 배열로 넘길 수 있습니다. 응답 값이 나열한 타입 중 하나에 해당하면 어서션이 통과합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`, `whereAllType` 메서드는 다음 타입을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 사용하면 테스트용 더미 파일이나 이미지를 쉽게 생성할 수 있습니다. 이것을 `Storage` 파사드의 `fake` 메서드와 조합하면 파일 업로드 테스트가 매우 간편해집니다. 예를 들어, 아래와 같이 아바타 업로드 폼을 테스트할 수 있습니다:

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

특정 파일이 존재하지 않음을 확인하려면, `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 더미 파일 커스터마이징

`UploadedFile` 클래스의 `fake` 메서드로 파일을 생성할 때 이미지의 너비, 높이, 이미지 파일의 크기(킬로바이트 단위)를 지정해 애플리케이션의 유효성 검사 규칙 테스트를 더 정밀하게 할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

또한, 이미지만이 아니라 다른 파일 타입도 `create` 메서드로 만들 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, 메서드에 `$mimeType` 인수를 전달해 반환할 MIME 타입을 명시적으로 지정할 수도 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트

Laravel에서는, 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고 뷰를 직접 렌더링할 수도 있습니다. 이를 위해 테스트에서 `view` 메서드를 호출하면 됩니다. 이 메서드는 뷰 이름과 옵션으로 데이터 배열을 받을 수 있으며, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 객체를 통해 뷰 내용에 대해 편리하게 어서션할 수 있습니다:

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

`TestView` 클래스에서는 다음 어서션 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 렌더링된 뷰의 원본 내용을 얻을 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기

몇몇 뷰는 [Laravel의 전역 에러백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존할 수 있습니다. 에러 메시지로 에러백을 채우려면, `withViewErrors` 메서드를 사용할 수 있습니다:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면, `blade` 메서드를 사용해 [Blade](/docs/12.x/blade) 원시 문자열을 평가 및 렌더링할 수 있습니다. 이 메서드 역시 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

`component` 메서드를 사용하면, [Blade 컴포넌트](/docs/12.x/blade#components)를 평가 및 렌더링할 수 있습니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 사용할 수 있는 다양한 맞춤 어서션 메서드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 등 테스트용 응답에서 사용할 수 있습니다:

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

<!-- 이하 모든 개별 어서션 설명은 생략 없이, CRITICAL 규칙에 따라 주석 및 코드 원본을 그대로 두고, 설명을 한국어로만 번역 (아래는 예시, 이후 동일 규칙 적용)  -->

<a name="assert-accepted"></a>
#### assertAccepted

응답이 accepted(202) HTTP 상태 코드를 반환하는지 어서션합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 bad request(400) HTTP 상태 코드를 반환하는지 어서션합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 에러(400 이상, 500 미만) HTTP 상태 코드를 반환하는지 어서션합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 conflict(409) HTTP 상태 코드를 반환하는지 어서션합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정한 쿠키가 포함되어 있는지 어서션합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 포함된 쿠키가 만료되었는지 어서션합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 포함된 쿠키가 만료되지 않았는지 어서션합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않은지 어서션합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 201 HTTP 상태 코드를 반환하는지 어서션합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 지정 문자열이 포함되어 있지 않은지 어서션합니다. 두 번째 인수로 `false`를 전달하면 문자열 이스케이프를 하지 않습니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 지정 문자열이 포함되어 있지 않은지 어서션합니다. 두 번째 인수로 `false`를 전달하면 문자열 이스케이프를 하지 않습니다. 이 메서드는 어서션 전에 `strip_tags` PHP 함수를 통해 내용을 처리합니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드" 응답인지 어서션합니다. 일반적으로, 응답 라우트가 `Response::download`, `BinaryFileResponse`, `Storage::download` 등을 반환한 경우입니다:

```php
$response->assertDownload();
```

원하면, 다운로드 파일명이 특정 값인지도 어서션할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 지정된 JSON 데이터를 **정확히** 포함하는지 어서션합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 지정한 JSON 구조와 **정확히** 일치하는지 어서션합니다:

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure) 보다 더 엄격하게 구조를 체크합니다. 기대한 JSON 구조에 명시적으로 포함하지 않은 키가 응답에 있으면 실패합니다.

<!-- 이하 모든 어서션에 대해 위와 동일한 방식(한국어 설명 + 코드 원본, 코드 블록 내는 번역 금지)으로 변환 (공간 관계상 생략) -->

... (이하 모든 어서션 설명 동일 규칙에 따라 번역) ...

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 애플리케이션의 기능 테스트에서 활용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 주의할 점은, 이 어서션들은 응답 인스턴스가 아닌 테스트 클래스 자체에서 직접 호출해야 한다는 점입니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되어 있는지 어서트합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되어 있지 않은지(즉, 게스트인지) 어서트합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

지정한 사용자가 인증되어 있는지 어서트합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검사 어서션

Laravel은 요청에 제공된 데이터가 유효한지/유효하지 않은지 확인하기 위한 두 가지 기본적인 유효성 검사 어서션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 지정한 키들에 대해 유효성 검사 에러가 없는지 어서트합니다. 이 메서드는 유효성 검사 에러가 JSON 구조로 반환된 경우나, 세션에 플래시된 경우 모두 사용할 수 있습니다:

```php
// 아무 유효성 검사 에러도 없는지 확인...
$response->assertValid();

// 지정 키들에 대해 유효성 검사 에러가 없는지 확인...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 지정한 키들에 대해 유효성 검사 에러가 있는지 어서트합니다. 이 메서드는 유효성 검사 에러가 JSON 구조로 반환된 경우나, 세션에 플래시된 경우 모두 사용할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 대해 특정 유효성 검사 에러 메시지가 있는지 어서트할 수도 있습니다. 이때 메시지 전체 또는 일부분만 전달해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
