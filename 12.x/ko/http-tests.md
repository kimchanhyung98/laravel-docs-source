# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이즈](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유연한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 assertion](#available-assertions)
    - [응답 assertion](#response-assertions)
    - [인증 assertion](#authentication-assertions)
    - [유효성 검증 assertion](#validation-assertions)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션에 HTTP 요청을 보내고 응답을 확인할 수 있도록 아주 직관적인 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보십시오.

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가져야 한다는 것을 검증합니다. 이 간단한 assertion 이외에도, 라라벨은 응답 헤더, 콘텐츠, JSON 구조 등 다양한 응답 정보를 검사할 수 있는 다양한 assertion 메서드를 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 사용할 수 있습니다. 이 메서드들은 실제로 "진짜" HTTP 요청을 보내는 것이 아니라, 네트워크 요청 전체를 내부적으로 시뮬레이션합니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, 애플리케이션의 응답을 검사할 수 있는 [다양한 assertion](#available-assertions) 기능을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다.

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

일반적으로, 각 테스트에서는 한 번만 애플리케이션에 요청을 보내는 것이 좋습니다. 하나의 테스트 메서드 안에서 여러 번 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 테스트를 실행할 때는 편의를 위해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이즈

요청을 애플리케이션에 보내기 전에 `withHeaders` 메서드를 사용하면 원하는 대로 요청 헤더를 커스터마이즈할 수 있습니다. 이 메서드를 이용하면 원하는 커스텀 헤더를 추가할 수 있습니다.

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

요청을 보내기 전에 `withCookie` 또는 `withCookies` 메서드를 이용해 쿠키 값을 지정할 수 있습니다. `withCookie`는 쿠키명과 값을 두 개의 인수로 받고, `withCookies`는 이름/값 쌍의 배열을 인수로 받습니다.

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

라라벨은 HTTP 테스트 중에 세션을 다루기 위한 여러 도우미 메서드를 제공합니다. 먼저, `withSession` 메서드를 사용해 세션 데이터를 배열 형태로 지정할 수 있습니다. 이 방법은 요청을 보내기 전에 세션에 원하는 데이터를 미리 로드해두는 데 유용합니다.

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

라라벨의 세션은 일반적으로 현재 인증된 사용자의 상태 유지를 위해 사용됩니다. 따라서, `actingAs` 도우미 메서드는 지정한 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다.

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

특정 guard를 사용해 사용자를 인증하고 싶다면, `actingAs` 메서드의 두 번째 인수로 guard명을 전달할 수 있습니다. 이때 지정한 guard는 테스트가 진행되는 동안 기본 guard로 사용됩니다.

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청을 애플리케이션에 보낸 뒤에는 `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 확인하고 디버깅할 수 있습니다.

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

또한, 응답 정보를 출력한 뒤 실행을 즉시 중단하고 싶을 때는 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용할 수 있습니다.

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

애플리케이션에서 특정 예외가 발생하는지 테스트해야 할 때가 있습니다. 이럴 경우, `Exceptions` 파사드를 통해 예외 핸들러를 "모킹"할 수 있습니다. 예외 핸들러를 모킹한 후에는, 요청 중에 발생한 예외에 대해 `assertReported`와 `assertNotReported` 메서드로 assertion을 작성할 수 있습니다.

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

`assertNotReported`와 `assertNothingReported` 메서드를 사용하면 주어진 예외가 발생하지 않았거나, 어떤 예외도 발생하지 않았는지 검증할 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하고 싶다면, 요청을 보내기 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한 애플리케이션이 PHP 언어 또는 외부 라이브러리의 deprecated(더 이상 지원되지 않는) 기능을 사용하지 않는지 엄격히 검증하고 싶을 때는, 요청 전 `withoutDeprecationHandling` 메서드를 사용할 수 있습니다. deprecated 처리가 비활성화되면, deprecated 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 주어진 클로저 내에서 특정 타입의 예외가 발생하는지 확인할 때 사용할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외가 발생했을 때, 그 예외를 직접 확인하고 assertion을 작성하고 싶다면 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드를 사용하면 클로저 내 코드에서 어떤 예외도 발생하지 않는지 검증할 수 있습니다.

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

라라벨은 JSON API와 그 응답을 테스트하기 위한 다양한 도우미 메서드도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 등 다양한 HTTP 메서드에 해당하는 JSON 요청을 손쉽게 만들 수 있습니다. 데이터와 헤더도 이 메서드들에 간편하게 전달할 수 있습니다. 예를 들어, `/api/user`에 `POST` 요청을 보내고, 기대하는 JSON 데이터가 반환되었는지 검증하는 테스트를 작성해 보겠습니다.

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

또한, JSON 응답 데이터를 배열 변수처럼 접근할 수 있으므로 반환된 JSON 데이터의 개별 값도 편리하게 확인할 수 있습니다.

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤, 지정한 배열이 애플리케이션이 반환한 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 추가로 있더라도, 지정한 배열 조각이 포함되어 있으면 이 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### JSON 정확히 일치하는지 assertion

앞서 설명한 것처럼, `assertJson` 메서드는 JSON 응답 내부에 주어진 데이터 조각이 존재하는지만 확인합니다. 만약 특정 배열이 애플리케이션이 반환한 JSON과 **정확히 일치**하는지 확인하고 싶다면, `assertExactJson` 메서드를 사용해야 합니다.

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
#### JSON 경로(Path) 기반 assertion

JSON 응답의 특정 경로에 지정된 값이 존재하는지 검증하려면, `assertJsonPath` 메서드를 사용할 수 있습니다.

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

`assertJsonPath` 메서드는 클로저도 인수로 받을 수 있어, assertion이 통과해야 하는지 조건을 동적으로 검사할 수도 있습니다.

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>

### 유연한(Fluent) JSON 테스트

라라벨은 애플리케이션의 JSON 응답을 유연하게 테스트할 수 있는 아름다운 방법도 제공합니다. 시작하려면 `assertJson` 메서드에 클로저(익명 함수)를 전달하면 됩니다. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인자로 받아, 해당 객체를 통해 애플리케이션이 반환한 JSON에 대해 다양한 검증(assertion)을 수행할 수 있습니다. 예를 들어, `where` 메서드를 사용하면 JSON의 특정 속성(attribute)에 대해 값을 검증할 수 있고, `missing` 메서드를 통해 특정 속성이 JSON 내에 존재하지 않음을 검증할 수 있습니다:

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

위 예시의 assertion 체인 마지막에 `etc` 메서드를 호출한 것을 볼 수 있습니다. 이 메서드는 해당 JSON 객체에 우리가 검증하지 않은 다른 속성들이 더 있을 수 있음을 라라벨에게 알려줍니다. 만약 `etc` 메서드를 사용하지 않으면, 해당 JSON 객체에 assertion으로 검증하지 않은 속성이 존재하는 경우 테스트가 실패하게 됩니다.

이러한 동작의 의도는 민감한 정보가 JSON 응답에 실수로 노출되는 것을 방지하기 위함입니다. 즉, 모든 속성에 대해 명시적으로 assertion을 작성하거나, `etc` 메서드를 통해 추가 속성의 존재를 허용하도록 강제합니다.

다만, assertion 체인에 `etc` 메서드를 포함하지 않는 것이, JSON 객체 내부의 중첩된 배열에 추가 속성이 없음까지 담보하는 것은 아닙니다. `etc` 메서드는 해당 메서드가 호출되는 중첩 수준에서만 추가 속성의 존재를 허용한다는 점을 참고하시기 바랍니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성의 존재/부재 검증

속성이 존재하는지 또는 존재하지 않는지를 검증하려면 `has` 및 `missing` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

그리고 `hasAll`, `missingAll` 메서드를 활용하면 여러 속성의 존재 또는 부재를 한 번에 검증할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드를 사용하면 주어진 속성 리스트 중 하나라도 있는지 확인할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 검증

라우트가 여러 항목(예: 여러 명의 사용자 등)을 반환하는 JSON 응답을 보내는 경우가 자주 있습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이런 경우에는, 유연한 JSON 객체의 `has` 메서드를 사용해 응답에 포함된 사용자 수를 검증할 수 있습니다. 예를 들어, JSON 응답이 3명의 사용자를 포함하고 있음을 확인할 수 있습니다. 그 후, `first` 메서드를 이용해 컬렉션의 첫 번째 사용자에 대한 세부 검증을 할 수 있습니다. `first` 메서드는 클로저를 인자로 받아, 해당 클로저의 인자로 첫 번째 객체를 또 다른 assertable JSON 인스턴스로 넘겨줍니다:

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
#### JSON 컬렉션 검증 범위 지정

애플리케이션의 어떤 라우트는 이름이 지정된 키에 할당된 JSON 컬렉션을 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이러한 라우트를 테스트할 때, `has` 메서드를 통해 컬렉션의 항목 개수를 검증할 수 있습니다. 또한, `has` 메서드를 사용해 특정 컬렉션에 대한 assertion 체인의 범위를 지정할 수도 있습니다:

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

하지만, `users` 컬렉션 검증을 위해 `has` 메서드를 두 번 호출하는 대신, 세 번째 인자로 클로저를 전달하여 한 번에 처리할 수도 있습니다. 이 경우, 클로저는 자동으로 컬렉션의 첫 번째 항목을 대상으로 실행됩니다:

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
#### JSON 타입 검증

JSON 응답의 특정 속성이 특정 자료형(type)에 해당하는지만 검증하고 싶을 때가 있습니다. 이를 위해 `Illuminate\Testing\Fluent\AssertableJson` 클래스는 `whereType`과 `whereAllType` 메서드를 제공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

또한, `|` 기호를 사용하거나, `whereType` 메서드의 두 번째 인자로 타입 배열을 전달해서 속성이 여러 자료형 중 하나라도 일치하는지 검증할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`과 `whereAllType` 메서드는 다음 타입을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스는 `fake` 메서드를 제공하여, 테스트용 임시 파일 또는 이미지를 쉽게 생성할 수 있습니다. 여기에 `Storage` 퍼사드의 `fake` 메서드를 조합하면 파일 업로드 테스트가 매우 간단해집니다. 예를 들어, 이 두 기능을 결합해 아바타 업로드 폼 테스트를 쉽게 할 수 있습니다:

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

특정 파일이 존재하지 않음을 검증하고 싶다면, `Storage` 퍼사드가 제공하는 `assertMissing` 메서드를 이용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이즈

`UploadedFile` 클래스의 `fake` 메서드로 파일을 생성할 때, 이미지의 가로, 세로 크기와 파일 크기(킬로바이트 단위)도 지정할 수 있어, 애플리케이션의 유효성 검증 규칙을 좀 더 세밀하게 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지뿐 아니라, `create` 메서드를 사용하면 모든 종류의 파일을 원하는 대로 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, 메서드에 `$mimeType` 인자를 전달해 파일의 MIME 타입을 명시적으로 지정할 수도 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰(View) 테스트

라라벨은 애플리케이션에 실제 HTTP 요청을 보내지 않고도 뷰를 렌더링하여 테스트할 수 있는 기능을 제공합니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하면 됩니다. `view` 메서드는 뷰 이름과 (선택적으로) 데이터를 담은 배열을 인자로 받으며, 반환값으로 `Illuminate\Testing\TestView` 인스턴스를 제공합니다. 이 객체를 이용해 다양한 방식으로 뷰의 내용에 대한 assertion을 수행할 수 있습니다:

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

`TestView` 클래스에서 사용할 수 있는 assertion 메서드는 다음과 같습니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 뷰의 원시 렌더링 결과를 얻을 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기

어떤 뷰는 [라라벨의 글로벌 에러 백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 에러가 필요할 수 있습니다. 에러 메시지를 에러 백에 주입(hydrate)하려면, `withViewErrors` 메서드를 사용할 수 있습니다:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade와 컴포넌트 렌더링

필요한 경우, `blade` 메서드를 통해 [Blade](/docs/12.x/blade)의 원시 문자열을 평가하고 렌더링할 수 있습니다. 이 메서드 역시 `view` 메서드와 마찬가지로 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/12.x/blade#components)를 평가하고 렌더링하려면 `component` 메서드를 사용할 수 있습니다. `component` 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 Assertion(검증) 목록

<a name="response-assertions"></a>
### 응답(Response) Assertion

라라벨의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 유용하게 사용할 수 있는 다양한 맞춤 assertion 메서드를 제공합니다. 이 assertion들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드에서 반환되는 응답 객체에서 사용할 수 있습니다:



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

응답이 HTTP 상태 코드 202(accepted)인지 검증합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 HTTP 상태 코드 400(bad request)인지 검증합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 오류(HTTP 상태 코드 400 이상 500 미만)인지 검증합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 HTTP 상태 코드 409(conflict)인지 검증합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 주어진 이름의 쿠키가 포함되어 있는지 검증합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 주어진 이름의 쿠키가 포함되어 있고, 해당 쿠키가 만료되어 있는지 검증합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 주어진 이름의 쿠키가 포함되어 있고, 해당 쿠키가 만료되지 않았는지 검증합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 주어진 이름의 쿠키가 없는지(존재하지 않는지) 검증합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 HTTP 상태 코드 201(created)인지 검증합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 주어진 문자열이 포함되어 있지 않은지 검증합니다. 두 번째 인자에 `false`를 전달하지 않는 한, 기본적으로 주어진 문자열은 escape 처리됩니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 주어진 문자열이 포함되어 있지 않은지 검증합니다. 두 번째 인자에 `false`를 전달하지 않는 한, 기본적으로 주어진 문자열은 escape 처리됩니다. 이 메서드는 assertion 전에 응답 콘텐츠를 PHP의 `strip_tags` 함수로 태그 제거 처리한 뒤 검증합니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드" 응답인지 검증합니다. 일반적으로 이는 라우트가 `Response::download`, `BinaryFileResponse`, 또는 `Storage::download` 형태로 응답을 반환했음을 의미합니다:

```php
$response->assertDownload();
```

필요하다면, 다운로드 파일이 특정 이름으로 지정되었는지 추가로 검증할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 지정한 JSON 데이터와 정확하게 일치하는지 검증합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 지정한 JSON 구조와 정확하게 일치하는지 검증합니다:

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 더 엄격하게 동작합니다. 즉, 기대하는 구조에 포함되지 않은 키가 응답에 존재할 경우 테스트가 실패합니다.

<a name="assert-forbidden"></a>

#### assertForbidden

응답이 forbidden(403) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 found(302) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 gone(410) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정한 헤더와 값이 존재하는지 확인합니다.

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정한 헤더가 존재하지 않는지 확인합니다.

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 "Internal Server Error"(500) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 지정한 JSON 데이터가 포함되어 있는지 확인합니다.

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메서드는 응답을 배열로 변환하여, 지정한 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 더 있더라도, 지정한 조각(fragment)이 포함되어 있다면 테스트는 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON에서 지정된 키의 배열 항목 개수가 예상 개수와 일치하는지 확인합니다.

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답 안 어디에든 지정한 JSON 데이터가 포함되어 있는지 확인합니다.

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

응답 JSON이 배열인지 확인합니다.

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체(object)인지 확인합니다.

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정한 JSON 데이터가 포함되어 있지 않은지 확인합니다.

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 정확히 지정한 JSON 데이터가 포함되어 있지 않은지 확인합니다.

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에서 지정한 키들에 대한 JSON 유효성 검증(Validation) 오류가 없는지 확인합니다.

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하면, 응답에 대한 유효성 검증 오류가 JSON 형식으로 반환되지 않았는지 **그리고** 세션 저장소에도 오류가 플래시되지 않았는지를 함께 확인할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답의 지정된 경로에 해당 데이터가 존재하는지 확인합니다.

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 아래와 같이 애플리케이션에서 다음 JSON 응답이 반환될 때,

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 객체의 `name` 속성 값이 특정 값과 일치하는지 다음과 같이 확인할 수 있습니다.

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정한 경로(path)가 포함되어 있지 않은지 확인합니다.

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 아래와 같이 애플리케이션에서 다음 JSON 응답이 반환될 때,

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 객체 내에 `email` 속성이 포함되어 있지 않은지 다음과 같이 확인할 수 있습니다.

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 지정한 JSON 구조를 가지고 있는지 확인합니다.

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 애플리케이션의 JSON 응답에 다음 데이터가 담겨 있다면,

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

JSON 구조가 기대와 일치하는지 아래처럼 확인할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때로는 애플리케이션에서 반환하는 JSON 응답이 객체들의 배열로 구성되어 있을 수도 있습니다.

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

이런 경우 모든 객체에 대해 구조를 일괄적으로 확인하려면 `*` 문자를 사용할 수 있습니다.

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

응답에서 지정한 키들에 대해 JSON 형식의 유효성 검증(Validation) 오류가 존재하는지 확인합니다. 이 메서드는 유효성 검증 오류가 세션에 플래시되지 않고 JSON 구조로 반환되는 응답에 대해 사용할 때 적합합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면, 응답에 유효성 검증 오류가 JSON으로 반환되었는지 **또는** 오류가 세션에 플래시되었는지 확인할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답에서 지정한 키에 대해 JSON 형식의 유효성 검증 오류가 존재하는지 확인합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 method not allowed(405) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 moved permanently(301) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답의 `Location` 헤더에 지정한 URI 값이 있는지 확인합니다.

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

지정한 문자열이 응답 내용과 일치하는지 확인합니다.

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정한 HTTP 상태 코드를 가지고, 본문 내용이 없는지 확인합니다.

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트리밍 응답인지 확인합니다.

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

지정한 문자열이 스트리밍 응답 내용과 일치하는지 확인합니다.

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 not found(404) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 200 HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 payment required(402) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정한 평문(암호화되지 않은) 쿠키가 존재하는지 확인합니다.

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정한 URI로 리다이렉트되는지 확인합니다.

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로 리다이렉트되는지 확인합니다.

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답의 리다이렉트 URI에 지정한 문자열이 포함되어 있는지 확인합니다.

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 지정한 [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트되는지 확인합니다.

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 지정한 [서명된 라우트](/docs/12.x/urls#signed-urls)로 리다이렉트되는지 확인합니다.

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 request timeout(408) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

지정한 문자열이 응답에 포함되어 있는지 확인합니다. 두 번째 인자로 `false`를 전달하지 않는 한, 자동으로 문자열을 이스케이프 처리합니다.

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답 내에 지정한 문자열들이 전달된 순서대로 포함되어 있는지 확인합니다. 두 번째 인자로 `false`를 전달하지 않으면 자동으로 문자열을 이스케이프 처리합니다.

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

지정한 문자열이 응답 텍스트에 포함되어 있는지 확인합니다. 두 번째 인자로 `false`를 전달하지 않으면 자동으로 문자열을 이스케이프 처리합니다. 이 검증을 수행하기 전에 응답 내용은 PHP의 `strip_tags` 함수로 HTML 태그가 제거됩니다.

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에 지정한 문자열들이 전달된 순서대로 포함되어 있는지 확인합니다. 두 번째 인자로 `false`를 전달하지 않으면 자동으로 문자열을 이스케이프 처리합니다. 이 검증을 수행하기 전에 응답 내용은 PHP의 `strip_tags` 함수로 HTML 태그가 제거됩니다.

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 에러(500 이상, 600 미만) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 "Service Unavailable"(503) HTTP 상태 코드를 가졌는지 확인합니다.

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션(session)에 지정한 값이 존재하는지 확인합니다.

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인자로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 검증에 성공합니다.

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

[세션에 플래시된 입력값 배열](/docs/12.x/responses#redirecting-with-flashed-session-data)에 지정한 값이 존재하는지 확인합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

필요하다면 두 번째 인자로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 검증에 성공합니다.

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정한 키/값 쌍 배열이 모두 존재하는지 확인합니다.

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 애플리케이션의 세션에 `name`과 `status` 키가 있을 때, 두 값이 모두 존재하며 지정한 값과 일치하는지 아래처럼 검증할 수 있습니다.

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

지정한 `$keys` 값에 대한 에러가 세션에 존재하는지 확인합니다. `$keys`가 연관 배열(associative array)이면, 각 필드(키)에 대해 특정 에러 메시지(값)가 세션에 존재하는지 검증합니다. 이 메서드는 유효성 검증 오류가 JSON 구조로 반환되지 않고 세션에 플래시되는 라우트 테스트에 사용해야 합니다.

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, `name`과 `email` 필드에 대한 유효성 검증 에러 메시지가 세션에 플래시됐는지 확인하려면 아래와 같이 `assertSessionHasErrors` 메서드를 호출할 수 있습니다.

```php
$response->assertSessionHasErrors(['name', 'email']);
```

또는, 특정 필드에 특정 유효성 검증 메시지가 존재하는지 검증하려면 다음과 같이 사용할 수 있습니다.

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면, 응답에 유효성 검증 오류가 JSON으로 반환되었는지 **또는** 오류가 세션에 플래시되었는지 확인할 수 있습니다.

<a name="assert-session-has-errors-in"></a>

#### assertSessionHasErrorsIn

특정 [에러 백](/docs/12.x/validation#named-error-bags) 내에서, 주어진 `$keys`에 대한 에러가 세션에 포함되어 있는지 확인합니다. 만약 `$keys`가 연관 배열(associative array)이라면, 에러 백 내에서 각 필드(키)에 해당하는 특정 에러 메시지(값)가 있는지 검증합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검사 에러가 없는지 검증합니다.

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

지정한 키들에 대해 세션에 유효성 검사 에러가 없는지 검증합니다.

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 더 범용적인 [assertValid](#assert-valid) 메서드를 사용하면, 응답이 JSON으로 반환된 유효성 검사 에러가 없고, 에러가 세션 스토리지에 flash되지 않았음을 동시에 확인할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정한 키가 포함되어 있지 않은지 검증합니다.

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 특정 HTTP 상태 코드를 가지는지 검증합니다.

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공(HTTP 상태 코드가 200 이상, 300 미만) 상태 코드를 가지는지 검증합니다.

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 '요청 횟수 초과'(429) HTTP 상태 코드를 가지는지 검증합니다.

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 '인증되지 않음'(401) HTTP 상태 코드를 가지는지 검증합니다.

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 '처리할 수 없음'(422) HTTP 상태 코드를 가지는지 검증합니다.

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 '지원하지 않는 미디어 타입'(415) HTTP 상태 코드를 가지는지 검증합니다.

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답에서 지정한 키들에 유효성 검사 에러가 없는지 검증합니다. 이 메서드는 유효성 검사 에러가 JSON 구조로 반환되거나, 에러가 세션에 flash된 경우 모두 사용할 수 있습니다.

```php
// 유효성 검사 에러가 전혀 없는지 확인...
$response->assertValid();

// 지정한 키들에 유효성 검사 에러가 없는지 확인...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에서 지정한 키들에 대해 유효성 검사 에러가 있는지 검증합니다. 이 메서드는 유효성 검사 에러가 JSON 구조로 반환되거나, 에러가 세션에 flash된 경우 모두 사용할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

또한, 특정 키에 대해 특정 유효성 검사 에러 메시지가 포함되어 있는지 검증할 수 있습니다. 이때는 전체 메시지 뿐만 아니라, 메시지의 일부분만 제공해도 됩니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

지정한 필드만 유효성 검사 에러가 발생하는지 검증하고 싶다면, `assertOnlyInvalid` 메서드를 사용할 수 있습니다.

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답에서 반환된 뷰가 특정 데이터를 포함하고 있는지 검증합니다.

```php
$response->assertViewHas($key, $value = null);
```

`assertViewHas` 메서드의 두 번째 인자로 클로저를 전달하면, 해당 뷰 데이터에 대해 직접 검증 로직을 작성할 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한, 뷰 데이터를 응답 객체의 배열 변수처럼 접근할 수 있으므로, 간편하게 값을 확인할 수 있습니다.

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 지정한 목록의 데이터가 모두 포함되어 있는지 검증합니다.

```php
$response->assertViewHasAll(array $data);
```

이 메서드는 뷰가 지정한 키에 해당하는 데이터를 단순히 가지고 있는지 확인하는 용도로 사용할 수 있습니다.

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

또는, 뷰 데이터가 특정 값까지 일치하는지 검증할 수도 있습니다.

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

지정한 뷰가 해당 라우트에서 반환되었는지 검증합니다.

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

애플리케이션 응답에서 반환된 뷰에, 지정한 데이터 키가 전달되지 않았음을 검증합니다.

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어서션(Authentication Assertions)

라라벨은 애플리케이션의 기능 테스트(feature test)에서 활용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 이 메서드들은 `get`, `post` 같은 메서드가 반환하는 `Illuminate\Testing\TestResponse` 인스턴스에서가 아니라, 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태임을 검증합니다.

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은(게스트) 상태임을 검증합니다.

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증된 상태임을 검증합니다.

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어서션(Validation Assertions)

라라벨은 요청(request)에 담긴 데이터가 유효하거나 유효하지 않은지를 테스트할 수 있도록, 유효성 검증과 관련된 두 가지 주요 어서션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에서 지정한 키들에 대해 유효성 검증 에러가 없는지 검증합니다. 이 메서드는 유효성 검사 에러가 JSON 구조로 반환되거나, 에러가 세션에 flash된 경우 모두 사용할 수 있습니다.

```php
// 유효성 검증 에러가 없는지 확인...
$response->assertValid();

// 지정한 키들에 유효성 검증 에러가 없는지 확인...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에서 지정한 키들에 대해 유효성 검증 에러가 있는지 검증합니다. 이 메서드는 유효성 검사 에러가 JSON 구조로 반환되거나, 에러가 세션에 flash된 경우 모두 사용할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

또한, 특정 키에 대해 특정 유효성 검증 에러 메시지가 있는지 직접 검증할 수도 있습니다. 이때 전체 메시지나, 일부 문자열만 입력해도 됩니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```