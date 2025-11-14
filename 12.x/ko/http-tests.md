# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 보내기](#making-requests)
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
- [라우트 캐싱](#caching-routes)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [유효성 검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 간결한 API를 제공합니다. 예를 들어, 아래의 기능 테스트(feature test) 예제를 살펴보세요:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가져야 함을 검증합니다. 이 외에도, Laravel에는 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 어서션이 포함되어 있습니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 이 메서드들은 실제로 "진짜" HTTP 요청을 애플리케이션에 보내지는 않습니다. 대신 네트워크 요청 전체가 내부적으로 시뮬레이션됩니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 객체는 애플리케이션의 응답을 검사할 수 있는 [여러 유용한 어서션](#available-assertions)을 제공합니다:

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

일반적으로 각 테스트는 한 번만 애플리케이션에 요청을 보내야 합니다. 하나의 테스트 메서드에서 여러 번 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해, 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

요청을 보내기 전에 `withHeaders` 메서드를 사용하여 요청의 헤더를 커스터마이즈할 수 있습니다. 이 메서드는 원하는 모든 커스텀 헤더를 요청에 추가할 수 있도록 해줍니다:

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

요청 전 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 각각 인수로 받고, `withCookies`는 이름/값 쌍의 배열을 인수로 받습니다:

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

Laravel은 HTTP 테스트 중에 세션을 다루기 위한 여러 헬퍼를 제공합니다. 먼저 `withSession` 메서드를 사용하면 세션 데이터를 지정한 배열로 미리 채울 수 있습니다. 이 방법은 요청을 보내기 전에 세션을 원하는 데이터로 준비하는 데 유용합니다:

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

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 그래서 `actingAs` 헬퍼 메서드는 지정한 사용자를 현재 사용자로 인증하는 간편한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

필요하다면 `actingAs` 메서드의 두 번째 인수로 가드 이름을 지정하여 사용할 가드를 선택할 수 있습니다. 이 경우 해당 테스트가 진행되는 동안 그 가드가 기본 가드로 사용됩니다:

```php
$this->actingAs($user, 'web');
```

요청이 인증되지 않았음을 보장하려면 `actingAsGuest` 메서드를 사용할 수 있습니다:

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 후에는 `dump`, `dumpHeaders`, `dumpSession` 메서드를 통해 응답 내용을 검사하고 디버깅할 수 있습니다:

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

또는, 정보를 덤프하고 실행을 중단하려면 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용할 수 있습니다:

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

애플리케이션이 특정 예외를 발생시키는지 테스트해야 할 때도 있습니다. 이를 위해 `Exceptions` 파사드를 통해 예외 핸들러를 "페이크(faked)"할 수 있습니다. 예외 핸들러가 페이크된 상태에서는, 요청 중에 발생한 예외에 대해 `assertReported`, `assertNotReported` 메서드를 활용할 수 있습니다:

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

`assertNotReported`와 `assertNothingReported` 메서드는 요청 중에 특정 예외가 발생하지 않았거나, 어떤 예외도 발생하지 않았음을 검증할 때 사용합니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에서 예외 처리를 완전히 비활성화하려면 요청 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 언어나 사용하는 라이브러리에서 deprecated(사용 중단 예정) 기능이 사용되지 않았음을 보장하고 싶다면 요청 전에 `withoutDeprecationHandling` 메서드를 호출하세요. Deprecation 핸들링이 비활성화되면, 사용 중단 경고가 예외로 변환되어 테스트가 실패합니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

특정 코드 블록이 지정한 타입의 예외를 발생시키는지 검증하려면 `assertThrows` 메서드를 사용할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외 객체를 직접 검사하며 어서션을 하고 싶다면, `assertThrows`의 두 번째 인자로 클로저를 넘기면 됩니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

클로저 안의 코드가 어떠한 예외도 띄우지 않아야 함을 검사하려면 `assertDoesntThrow` 메서드를 사용하세요:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API 및 그 응답을 테스트하기 위한 여러 헬퍼도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 통해 다양한 HTTP verb로 JSON 요청을 보낼 수 있습니다. 이 메서드에 데이터나 헤더도 쉽게 전달할 수 있습니다. 예를 들어, `/api/user`에 `POST` 요청을 보내고 예상되는 JSON 데이터가 반환되었는지 검증하는 테스트를 다음과 같이 만들 수 있습니다:

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

또한, JSON 응답의 데이터를 배열 변수처럼 직접 접근할 수 있어 반환된 개별 값을 간편하게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여, 지정한 배열이 애플리케이션이 반환한 JSON 응답 내에 존재하는지 확인합니다. 즉, JSON에 다른 속성이 더 있어도 해당 조각(fragment)이 존재하는지만 검사하여 테스트를 통과시킵니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 확인

앞서 언급한 것처럼 `assertJson`은 JSON 내의 조각이 존재하는지 확인합니다. 만약 지정한 배열이 애플리케이션이 반환한 JSON과 **정확히 일치**하는지 확인하고 싶다면, `assertExactJson` 메서드를 사용해야 합니다:

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

JSON 응답의 특정 경로(path)에 원하는 데이터가 포함되어 있는지 검증하려면 `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath`는 클로저도 받을 수 있어, 동적으로 어서션을 처리할 수도 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 좀 더 유연하게(플루언트하게) 테스트할 수 있는 방법도 제공합니다. 먼저, `assertJson` 메서드에 클로저를 전달하면 해당 클로저가 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인수로 받아 호출됩니다. 이 객체의 `where` 메서드를 사용하면 JSON의 특정 속성에 대해 어서션을 할 수 있고, `missing` 메서드로는 특정 속성이 없는지를 검사할 수 있습니다:

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

#### `etc` 메서드 이해

위의 예제에서 어서션 체인 마지막에 사용된 `etc` 메서드는 JSON 오브젝트에 다른 속성이 더 있을 수도 있음을 Laravel에 알리는 역할을 합니다. `etc` 메서드를 사용하지 않으면, JSON 오브젝트에 여러분이 어서션을 하지 않은 속성이 존재할 경우에도 테스트가 실패합니다.

이런 동작은 여러분이 민감한 정보를 의도치 않게 JSON 응답에 노출하는 것을 방지해줍니다. 즉, 속성 하나하나에 대해 반드시 어서션하거나, 그렇지 않다면 명시적으로 `etc`를 통해 추가 속성을 허용해야 합니다.

하지만, 주의할 점은 `etc` 메서드를 어서션 체인에 포함하지 않는다고 해서 JSON 오브젝트 내부에 중첩된 배열(예: 배열 안의 배열)에 추가 속성이 들어가는 일까지 막지는 못한다는 점입니다. `etc`는 호출된 중첩 레벨에서만 추가 속성을 막습니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어서션

속성이 존재함을 어서트하려면 `has`를, 부재를 어서트하려면 `missing` 메서드를 사용하면 됩니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

여러 속성의 존재 혹은 부재를 동시에 검사할 수 있는 `hasAll`, `missingAll` 메서드도 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

지정한 여러 속성 중 적어도 하나가 존재하는지만 검사하고 싶다면 `hasAny`를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

경로가 여러 항목(예: 여러 사용자)을 가진 JSON 응답을 반환한다면:

```php
Route::get('/users', function () {
    return User::all();
});
```

이런 상황에서는 플루언트 JSON 객체의 `has` 메서드로 응답의 사용자 수를 검증할 수 있습니다. 그리고 `first` 메서드를 사용해 컬렉션의 첫 번째 요소에 대해 추가 어서션을 할 수 있습니다. `first` 메서드는 클로저를 받아, 이 안에서 첫 번째 JSON 객체에 대해 어서션을 할 수 있습니다:

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

아래처럼 JSON 컬렉션이 명명된 키에 할당되어 반환되는 상황도 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이런 경우, `has` 메서드를 사용해 해당 컬렉션의 항목 수를 어서트할 수 있고, 또 아래처럼 어서션 체인 범위(scope)를 지정할 수 있습니다:

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

`users` 컬렉션에 대한 어서션을 두 번 나누어 작성하는 대신, 한 번의 호출로 클로저를 세 번째 인수로 전달해 아래처럼 좀 더 우아하게 작성할 수 있습니다. 이때 클로저는 컬렉션의 첫 번째 아이템을 자동으로 범위로 지정해 실행됩니다:

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

JSON 응답의 속성이 특정 타입임만 확인하려면 `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`, `whereAllType` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 `|` 문자로 구분해서, 또는 배열로 전달할 수도 있습니다. 응답 값이 나열된 타입 중 하나라도 일치하면 어서션은 성공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`과 `whereAllType` 메서드에서 지원하는 타입: `string`, `integer`, `double`, `boolean`, `array`, `null`

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 이용하면 테스트 용 가상 파일이나 이미지를 쉽게 생성할 수 있습니다. `Storage` 파사드의 `fake` 메서드와 함께 사용하면 파일 업로드 테스트가 매우 간단해집니다. 예를 들어, 아바타 업로드 폼을 테스트하는 코드는 다음과 같습니다:

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

특정 파일이 존재하지 않는지 검증하려면, `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가상 파일 커스터마이즈

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때, 이미지의 너비, 높이, 크기(kb)도 지정해 애플리케이션의 유효성 검증을 좀 더 잘 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도, `create` 메서드를 사용해 원하는 종류의 파일을 만들 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면 MIME 타입도 인수로 지정할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트

Laravel에서는 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고도 뷰를 렌더링해 볼 수 있습니다. 이를 위해 테스트에서 `view` 메서드를 호출하면 됩니다. `view` 메서드는 뷰 이름과(필요하다면) 데이터 배열을 인수로 받습니다. 반환값은 `Illuminate\Testing\TestView` 인스턴스이며, 이 객체를 통해 뷰 내용에 대해 다양한 어서션을 할 수 있습니다:

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

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 의 여러 어서션 메서드를 제공합니다.

또한, 필요하다면 `TestView` 인스턴스를 문자열로 캐스팅해 렌더링된 뷰의 원본 내용을 얻을 수도 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 Laravel이 제공하는 [글로벌 에러 백(global error bag)](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존할 수 있습니다. 테스트 내에서 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면, `blade` 메서드를 사용해 원시 [Blade](/docs/12.x/blade) 문자열을 평가(evaluate)하고 렌더링할 수 있습니다. 이 메서드 역시 `view` 메서드처럼 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/12.x/blade#components)를 평가 및 렌더링할 때는 `component` 메서드를 사용할 수 있습니다. 반환값은 `Illuminate\Testing\TestComponent`입니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="caching-routes"></a>
## 라우트 캐싱

테스트가 실행되기 전에, Laravel은 정의된 모든 라우트를 수집하고 애플리케이션의 새 인스턴스를 부트합니다. 라우트 파일이 많은 애플리케이션의 경우, 테스트 케이스에 `Illuminate\Foundation\Testing\WithCachedRoutes` 트레잇을 추가하면 좋습니다. 이 트레잇을 사용하는 테스트에서는 라우트가 한 번만 빌드되어 메모리에 저장되며, 테스트 전체에서 라우트 수집 과정이 한 번만 실행됩니다:

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
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스에는 테스트에 쓸 수 있는 다양한 커스텀 어서션 메서드가 포함되어 있습니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 같은 테스트 메서드가 반환하는 응답에서 사용할 수 있습니다:

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

응답이 HTTP 202 Accepted 상태 코드임을 어서트합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 HTTP 400 Bad Request 상태 코드임을 어서트합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 에러(HTTP 400 이상, 500 미만) 상태 코드임을 어서트합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 HTTP 409 Conflict 상태 코드임을 어서트합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정한 쿠키가 포함되어 있음을 어서트합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정한 쿠키가 포함되어 있고, 만료되어 있음을 어서트합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정한 쿠키가 포함되어 있으며, 만료되지 않았음을 어서트합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않음을 어서트합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 HTTP 201 Created 상태 코드임을 어서트합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 지정한 문자열이 포함되지 않았음을 어서트합니다. 두 번째 인수로 `false`를 전달하면 문자열이 escape되지 않습니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 지정한 문자열이 포함되지 않았음을 어서트합니다. 두 번째 인수로 `false`를 전달하면 문자열이 escape되지 않습니다. 이 메서드는 어서션 전, 응답 내용을 PHP의 `strip_tags` 함수로 처리합니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드" 응답임을 어서트합니다. 보통 라우트가 `Response::download`, `BinaryFileResponse`, `Storage::download` 응답을 반환하는 경우에 해당합니다:

```php
$response->assertDownload();
```

원한다면 다운로드되는 파일의 이름도 어서트할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 지정한 JSON 데이터와 정확히 일치함을 어서트합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 지정한 JSON 구조와 정확히 일치함을 어서트합니다:

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 더 엄격한 방식으로, 기대한 구조에 없는 키가 응답에 포함되어 있으면 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 HTTP 403 Forbidden 상태 코드임을 어서트합니다:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 HTTP 302 Found 상태 코드임을 어서트합니다:

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 HTTP 410 Gone 상태 코드임을 어서트합니다:

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정한 헤더와 값이 포함되어 있음을 어서트합니다:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정한 헤더가 존재하지 않음을 어서트합니다:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 HTTP 500 Internal Server Error 상태 코드임을 어서트합니다:

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 지정한 JSON 데이터가 포함되어 있음을 어서트합니다:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메서드는 응답을 배열로 변환해서 지정한 배열이 JSON 응답 내에 존재하는지 확인합니다. JSON 응답에 다른 속성이 더 있어도 이 조각이 있으면 테스트는 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON에 주어진 키에 해당하는 배열이 기대한 개수만큼 있는지 어서트합니다:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답 어디에든지 지정한 JSON 데이터가 포함되어 있음을 어서트합니다:

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

응답 JSON이 배열임을 어서트합니다:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 오브젝트임을 어서트합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정한 JSON 데이터가 포함되어 있지 않음을 어서트합니다:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 정확히 일치하는 JSON 데이터가 포함되어 있지 않음을 어서트합니다:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 지정한 키에 대한 JSON 유효성 검증 에러가 없음을 어서트합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 좀 더 범용적인 [assertValid](#assert-valid) 메서드는, JSON으로 반환된 유효성 검증 에러가 없었을 뿐 아니라 세션에도 에러가 플래시되지 않았음을 동시에 확인할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답의 지정한 경로(path)에 지정한 데이터가 있는지 어서트합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 아래와 같이 JSON 응답이 반환될 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 오브젝트의 `name` 속성이 특정 값과 일치하는지 아래처럼 어서트할 수 있습니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정한 경로(path)가 없음을 어서트합니다:

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 아래와 같이 JSON 응답이 반환될 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 오브젝트에 `email` 속성이 없음을 아래처럼 어서트할 수 있습니다:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 지정한 구조의 JSON을 포함하는지 어서트합니다:

```php
$response->assertJsonStructure(array $structure);
```

아래와 같이 JSON 응답이 있다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래와 같이 JSON 구조를 어서트할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

애플리케이션의 JSON 응답이 오브젝트들의 배열을 포함할 수도 있습니다:

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

이 경우, 배열의 모든 오브젝트에 대한 구조 검증에는 `*`을 사용할 수 있습니다:

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

응답에 지정한 키의 JSON 유효성 검증 에러가 있음을 어서트합니다. 이 메서드는 유효성 검증 에러가 세션에 플래시되는 대신 JSON 구조로 반환되는 경우 어서트에 사용해야 합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 범용적인 [assertInvalid](#assert-invalid) 메서드는 JSON으로 반환되든 세션에 플래시되든 유효성 검증 에러가 있었는지 어서트할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답에 지정한 키의 JSON 유효성 검증 에러가 하나라도 있는지 어서트합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 HTTP 405 Method Not Allowed 상태 코드임을 어서트합니다:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 HTTP 301 Moved Permanently 상태 코드임을 어서트합니다:

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답의 `Location` 헤더에 지정한 URI가 있는지 어서트합니다:

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 내용이 지정한 문자열과 일치하는지 어서트합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정한 HTTP 상태 코드와 함께 내용이 없음을 어서트합니다:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트림 형태로 반환됐음을 어서트합니다:

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트림 응답의 내용이 지정한 문자열과 일치하는지 어서트합니다:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 HTTP 404 Not Found 상태 코드임을 어서트합니다:

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 HTTP 200 OK 상태 코드임을 어서트합니다:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 HTTP 402 Payment Required 상태 코드임을 어서트합니다:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정한 암호화되지 않은 쿠키가 포함되어 있음을 어서트합니다:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정한 URI로 리다이렉트되는지 어서트합니다:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로 리다이렉트되는지 어서트합니다:

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리다이렉트되며, [세션에 지정한 에러](#assert-session-has-errors)가 있는지 어서트합니다:

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

응답이 이전 페이지로 리다이렉트되며, 세션에 에러 메시지가 없는지 어서트합니다:

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 지정 문자열을 포함한 URI로 리다이렉트되는지 어서트합니다:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 [네임드 라우트](/docs/12.x/routing#named-routes)로의 리다이렉트임을 어서트합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 [서명된 라우트](/docs/12.x/urls#signed-urls)로의 리다이렉트임을 어서트합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 HTTP 408 Request Timeout 상태 코드임을 어서트합니다:

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

응답에 지정한 문자열이 포함되어 있는지 어서트합니다. 두 번째 인수로 `false`를 전달하면 문자열이 escape되지 않습니다:

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답에 지정한 문자열들이 순서대로 포함되는지 어서트합니다. 두 번째 인수로 `false`를 전달하면 escape하지 않습니다:

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 텍스트에 지정한 문자열이 포함되어 있는지 어서트합니다. 두 번째 인수로 `false`를 전달하면 escape하지 않습니다. 응답 내용은 어서션 전에 `strip_tags`로 처리됩니다:

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에 지정한 문자열들이 순서대로 포함되어 있는지 어서트합니다. 두 번째 인수로 `false`를 전달하면 escape하지 않습니다. 응답 내용은 어서션 전에 `strip_tags`로 처리됩니다:

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 에러(HTTP 500 이상, 600 미만) 상태 코드임을 어서트합니다:

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 HTTP 503 Service Unavailable 상태 코드임을 어서트합니다:

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정한 데이터가 포함되어 있는지 어서트합니다:

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 어서션이 통과합니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션에 [플래시된 인풋 배열](/docs/12.x/responses#redirecting-with-flashed-session-data)에 값이 포함되어 있는지 어서트합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인수로 클로저를 전달해 값에 대해 추가 어서션을 할 수 있습니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정한 키/값 쌍의 배열이 모두 포함되어 있는지 어서트합니다:

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 세션에 `name`, `status`가 들어 있다면 아래처럼 두 값을 동시에 어서트할 수 있습니다:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 지정한 `$keys`에 대한 에러가 있는지 어서트합니다. `$keys`에 연관 배열을 전달하면, 각 필드(키)에 특정 에러 메시지(값)가 있는지도 어서트합니다. 이 메서드는 유효성 검증 에러가 세션에 플래시될 때 사용해야 합니다:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, `name`, `email` 필드에 세션 플래시 유효성 검증 에러 메시지가 있는지 어서트하는 방법은 아래와 같습니다:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

또는, 특정 필드에 특정 에러 메시지가 있는지도 어서트할 수 있습니다:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 좀 더 범용적인 [assertInvalid](#assert-invalid) 메서드는 JSON으로 반환되든, 세션에 플래시되든 유효성 검증 에러를 어서트할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

[에러 백](/docs/12.x/validation#named-error-bags)에 지정한 `$keys`에 대한 에러가 있는지 어서트합니다. `$keys`에 연관 배열을 전달하면, 해당 에러 백에 각각의 메시지가 있는지도 어서트합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 에러가 전혀 없음을 어서트합니다:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 지정한 키에 대한 유효성 검증 에러가 없음을 어서트합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 범용적인 [assertValid](#assert-valid)는 JSON 유효성 검증 에러와 세션 플래시 에러 둘 모두 어서트할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정한 키가 없음을 어서트합니다:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 지정한 HTTP 상태 코드임을 어서트합니다:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공(HTTP 200 이상 300 미만) 상태 코드임을 어서트합니다:

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 HTTP 429 Too Many Requests 상태 코드임을 어서트합니다:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 HTTP 401 Unauthorized 상태 코드임을 어서트합니다:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 HTTP 422 Unprocessable Entity 상태 코드임을 어서트합니다:

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 HTTP 415 Unsupported Media Type 상태 코드임을 어서트합니다:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답에 지정한 키에 대한 유효성 검증 에러가 전혀 없음을 어서트합니다. 이 메서드는 JSON 구조 또는 세션 플래시 모두에 대해 사용할 수 있습니다:

```php
// 유효성 검증 에러가 전혀 없는지 어서트...
$response->assertValid();

// 지정한 키에 에러가 없는지 어서트...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 지정한 키에 대한 유효성 검증 에러가 있음을 어서트합니다. 이 메서드는 JSON 구조 또는 세션 플래시 모두에 대해 사용할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 특정 유효성 검증 에러 메시지가 있는지도 어서트할 수 있으며, 메시지 전체 또는 일부만 전달해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

오직 지정한 필드에만 유효성 검증 에러가 있음을 어서트하려면 `assertOnlyInvalid` 메서드를 사용할 수 있습니다:

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답의 뷰에 지정한 데이터가 포함되어 있는지 어서트합니다:

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 전달해 데이터에 추가 어서션을 할 수 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한, 뷰 데이터에 배열 표기법으로 직접 접근할 수 있어 값 확인이 편리합니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 지정한 데이터 목록이 모두 포함되어 있는지 어서트합니다:

```php
$response->assertViewHasAll(array $data);
```

아래처럼 뷰에 데이터가 있는지만 검증할 수도 있고,

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

값까지 함께 어서트할 수도 있습니다:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

지정 뷰가 라우트에서 반환됐는지 어서트합니다:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답에 포함된 뷰 데이터에 지정한 키가 없는지 어서트합니다:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel에서는 애플리케이션의 기능 테스트에서 사용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 이 메서드들은 테스트 클래스(self)에서 직접 호출하며, `get`, `post` 같은 메서드가 반환하는 `Illuminate\Testing\TestResponse` 인스턴스가 아닙니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되어 있는지 어서트합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되어 있지 않은지 어서트합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증된 상태인지 어서트합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어서션

Laravel은 요청에 제공된 데이터가 유효했는지(또는 유효하지 않았는지) 확인할 수 있는 두 가지 주요 유효성 검증 어서션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 지정한 키에 대한 유효성 검증 에러가 없음을 어서트합니다. JSON 구조이거나 세션에 플래시된 에러 모두에 사용 가능합니다:

```php
// 유효성 검증 에러가 없는지 어서트...
$response->assertValid();

// 지정한 키에 에러가 없는지 어서트...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 지정한 키에 유효성 검증 에러가 있음을 어서트합니다. JSON 구조이거나 세션에 플래시된 에러 모두에 사용 가능합니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키에 특정 유효성 검증 에러 메시지가 있는지도 어서트할 수 있으며, 전체 메시지나 일부만 전달해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
