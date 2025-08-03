# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트하기](#testing-json-apis)
    - [플루언트 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어설션](#available-assertions)
    - [응답 어설션](#response-assertions)
    - [인증 어설션](#authentication-assertions)
    - [유효성 검증 어설션](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사하는 매우 직관적인 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보세요:

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
     * 간단한 테스트 예시입니다.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션으로 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가지고 있는지 검증합니다. 이처럼 간단한 어설션 외에도 Laravel은 응답 헤더, 콘텐츠, JSON 구조 등을 검사할 수 있는 다양한 어설션을 포함하고 있습니다.

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

애플리케이션에 요청을 하려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 호출할 수 있습니다. 이 메서드들은 실제 "진짜" HTTP 요청을 보내는 것이 아니라, 내부적으로 네트워크 요청을 시뮬레이션합니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 객체는 애플리케이션의 응답을 검사할 수 있도록 [다양한 유용한 어설션](#available-assertions)을 제공합니다:

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
     * 간단한 요청 테스트 예시입니다.
     */
    public function test_a_basic_request(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

일반적으로, 각 테스트는 애플리케이션에 단 하나의 요청만 보내야 합니다. 단일 테스트 메서드 내에서 여러 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]  
> 편의상, 테스트 실행 시 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징 (Customizing Request Headers)

`withHeaders` 메서드를 이용해 애플리케이션에 요청을 보내기 전에 요청 헤더를 커스터마이징할 수 있습니다. 이 메서드를 사용하면 원하는 모든 커스텀 헤더를 요청에 추가할 수 있습니다:

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
     * 간단한 기능 테스트 예시입니다.
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

`withCookie` 또는 `withCookies` 메서드를 사용하여 요청 전에 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 각각 인수로 받으며, `withCookies`는 이름/값 쌍으로 이루어진 배열을 인수로 받습니다:

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

Laravel은 HTTP 테스트 중 세션과 상호작용하기 위한 여러 헬퍼를 제공합니다. 우선, `withSession` 메서드를 이용해 요청 전에 세션 데이터를 배열로 세팅할 수 있습니다. 이는 애플리케이션에 요청을 보내기 전에 세션에 데이터를 적재할 때 유용합니다:

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

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 주어진 사용자를 현재 인증된 사용자로 간단히 인증할 수 있는 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/11.x/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

또한, `actingAs` 메서드의 두 번째 인수로 가드 이름을 전달해 특정 가드를 통해 사용자를 인증할 수도 있습니다. 이때 지정된 가드는 테스트 전체 동안 기본 가드가 됩니다:

```
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

애플리케이션에 테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용하여 응답 내용을 확인하고 디버깅할 수 있습니다:

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
     * 간단한 테스트 예시입니다.
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

또는, `dd`, `ddHeaders`, `ddSession`, `ddJson` 메서드를 사용해 응답 정보를 덤프하고 실행을 중단할 수도 있습니다:

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->ddHeaders();
    $response->ddSession();
    $response->ddJson();
    $response->dd();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 간단한 테스트 예시입니다.
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

때때로 애플리케이션이 특정 예외를 던지는지 테스트해야 할 때가 있습니다. 이를 위해 `Exceptions` 파사드를 사용해 예외 핸들러를 "가짜화" 할 수 있습니다. 예외 핸들러가 가짜화되면, `assertReported` 및 `assertNotReported` 메서드를 이용해 요청 중 발생한 예외에 대해 어설션을 할 수 있습니다:

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // 예외가 던져졌는지 검증...
    Exceptions::assertReported(InvalidOrderException::class);

    // 예외에 대해 검증...
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
     * 간단한 테스트 예시입니다.
     */
    public function test_exception_is_thrown(): void
    {
        Exceptions::fake();

        $response = $this->get('/');

        // 예외가 던져졌는지 검증...
        Exceptions::assertReported(InvalidOrderException::class);

        // 예외에 대해 검증...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

`assertNotReported` 및 `assertNothingReported` 메서드를 사용하면 요청 중 해당 예외가 발생하지 않았거나, 아예 예외가 발생하지 않았음을 검증할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

요청 전에 `withoutExceptionHandling` 메서드를 호출하면 특정 요청에 대해 예외 처리를 완전히 비활성화할 수도 있습니다:

```
$response = $this->withoutExceptionHandling()->get('/');
```

추가로, PHP 언어나 애플리케이션이 사용하는 라이브러리에서 더 이상 지원하지 않는 기능이 사용되지 않음을 보장하려면, 요청 전에 `withoutDeprecationHandling` 메서드를 호출하세요. 이럴 경우, 더 이상 사용하지 않는 기능 경고가 예외로 변환되어 테스트 실패를 유도합니다:

```
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드를 사용하면 주어진 클로저 내에서 특정 타입의 예외가 던져졌는지 검증할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외 인스턴스를 검토하고 어설션을 하고 싶다면, `assertThrows`의 두 번째 인수로 클로저를 전달할 수도 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

<a name="testing-json-apis"></a>
## JSON API 테스트하기 (Testing JSON APIs)

Laravel은 JSON API와 그 응답을 테스트하기 위한 여러 헬퍼 메서드를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용해 다양한 HTTP 동사로 JSON 요청을 쉽게 보낼 수 있습니다. 또한, 데이터와 헤더도 쉽게 전달할 수 있습니다. 기본 사용법을 위해 `/api/user`에 `POST` 요청을 보내고 예상 JSON 데이터를 검증하는 테스트를 작성해보겠습니다:

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
     * 기본 기능 테스트 예시입니다.
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

또한 JSON 응답 데이터는 배열처럼 접근할 수 있어, JSON 응답 내 개별 값을 쉽게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]  
> `assertJson` 메서드는 응답을 배열로 변환하여 지정한 배열 조각이 JSON 응답에 포함되어 있는지 검증합니다. 만약 JSON 응답에 다른 속성들이 추가로 있어도, 지정한 조각이 포함되어 있다면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어설션 (Asserting Exact JSON Matches)

앞서 설명한 `assertJson` 메서드는 JSON 응답 내에 일부분이 포함되어 있는지만 검증합니다. 만약 애플리케이션이 반환한 JSON과 완전히 **정확하게 일치하는지** 확인하고 싶으면 `assertExactJson` 메서드를 사용하세요:

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
     * 기본 기능 테스트 예시입니다.
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

JSON 응답 내 특정 경로에 지정한 데이터가 존재하는지 검증하려면 `assertJsonPath` 메서드를 사용하세요:

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
     * 기본 기능 테스트 예시입니다.
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

`assertJsonPath` 메서드는 클로저도 인자로 받을 수 있으며, 클로저 내부에서 동적으로 어설션 통과 여부를 결정할 수 있습니다:

```
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트 (Fluent JSON Testing)

Laravel은 애플리케이션의 JSON 응답을 깔끔하고 직관적으로 테스트할 수 있는 방법도 제공합니다. `assertJson` 메서드에 클로저를 전달하면, 클로저 내부에 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스가 전달됩니다. 이 인스턴스를 통해 JSON의 특정 속성에 대해 `where` 메서드로 검사하거나, `missing` 메서드로 해당 속성이 없음을 검증할 수 있습니다:

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
 * 기본 기능 테스트 예시입니다.
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

위 예시에서는 `etc` 메서드를 어설션 체인 마지막에 호출했습니다. 이 메서드는 JSON 객체 내에 다른 속성들이 더 있을 수 있음을 Laravel에 알립니다. 만약 `etc`를 호출하지 않으면, 어설션하지 않은 추가 속성이 JSON 응답에 존재할 경우 테스트가 실패합니다.

이렇게 한 이유는 JSON 응답에 민감한 정보가 의도치 않게 노출되지 않도록 하기 위한 것입니다. 따라서 모든 속성에 대해 명시적으로 어설션을 하거나, `etc` 메서드를 명시적으로 호출해 추가 속성을 허용해야 합니다.

다만 `etc` 메서드는 중첩된 배열 내부에 추가 속성이 없는지까진 보장하지 못하고, 해당 메서드가 호출된 중첩 수준에서만 불필요한 속성이 없음을 보장한다는 점에 유의하세요.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재 여부 어설션 (Asserting Attribute Presence / Absence)

속성이 존재하는지 또는 존재하지 않는지를 검증하려면 `has`와 `missing` 메서드를 사용합니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한 `hasAll`과 `missingAll` 메서드를 사용하면 여러 속성의 존재 여부를 한 번에 검증할 수 있습니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드는 목록 중 적어도 하나의 속성이 존재하는지 확인할 때 사용합니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어설션 (Asserting Against JSON Collections)

라우트가 여러 개 항목을 포함하는 JSON 응답을 반환할 때가 많습니다. 예를 들어 다수의 사용자 정보가 JSON 배열 형태로 반환될 수 있습니다:

```
Route::get('/users', function () {
    return User::all();
});
```

이런 경우 플루언트 JSON 객체의 `has` 메서드를 사용해 JSON 내 사용자 개수를 검증할 수 있습니다. 이어서 `first` 메서드로 컬렉션 첫 번째 객체에 대해 어설션 체인을 이어갈 수 있습니다. `first`는 클로저를 인수로 받아, 컬렉션 첫 아이템에 대해 사용할 또 다른 `AssertableJson` 객체를 제공합니다:

```
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
#### JSON 컬렉션 어설션 스코핑 (Scoping JSON Collection Assertions)

때로는 애플리케이션의 라우트가 네임드 키를 포함하는 JSON 컬렉션을 반환할 수 있습니다:

```
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이런 경우 `has` 메서드를 사용해 컬렉션 내 아이템 개수를 검증할 수 있으며, 또 `has` 메서드를 중첩해 체인으로 스코프를 지정할 수도 있습니다:

```
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

하지만 `users` 컬렉션에 대해 두 번 `has` 메서드를 호출하지 않고, 세 번째 인수로 클로저를 전달해 첫 번째 아이템 스코프로 바로 어설션할 수도 있습니다:

```
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

JSON 응답 내 속성 타입만 검증하고 싶을 때, `Illuminate\Testing\Fluent\AssertableJson`의 `whereType` 및 `whereAllType` 메서드를 사용합니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 `|` 문자로 구분하거나, 배열로 두 번째 인자로 전달할 수 있습니다. 테스트는 지정 타입 중 하나와 일치하면 성공입니다:

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

지원되는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null`입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 사용하면 테스트용 더미 파일 또는 이미지를 생성할 수 있습니다. 이것을 `Storage` 파사드의 `fake` 메서드와 함께 사용하면 파일 업로드 테스트가 훨씬 간편해집니다. 예를 들어 아바타 업로드 폼을 쉽게 테스트할 수 있습니다:

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

특정 파일이 존재하지 않음을 검증하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용하면 됩니다:

```
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징 (Fake File Customization)

`UploadedFile`의 `fake` 메서드로 생성할 때, 이미지의 너비, 높이, 크기(킬로바이트)를 지정해 애플리케이션의 유효성 검증 규칙에 맞춰 테스트할 수 있습니다:

```
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지뿐 아니라 `create` 메서드로 임의 타입의 파일도 생성할 수 있습니다:

```
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하면 `$mimeType` 인수를 전달해 반환할 MIME 타입을 명시적으로 지정할 수 있습니다:

```
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 애플리케이션에 요청하지 않고도 뷰를 렌더링할 수 있게 해줍니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하면 됩니다. 이 메서드는 뷰 이름과 선택적 데이터 배열을 받고, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 객체는 뷰 내용에 대한 어설션을 편리하게 지원합니다:

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

`TestView` 클래스는 다음과 같은 어설션 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면 `TestView` 인스턴스를 문자열로 변환해 원시 렌더링된 뷰 내용을 얻을 수도 있습니다:

```
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기 (Sharing Errors)

일부 뷰는 Laravel이 제공하는 [전역 에러 백(global error bag)](/docs/11.x/validation#quick-displaying-the-validation-errors)에서 공유된 에러에 의존할 수 있습니다. 뷰에 에러 메시지를 부여하려면 `withViewErrors` 메서드를 사용하세요:

```
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링 (Rendering Blade and Components)

필요하다면 `blade` 메서드로 원시 [Blade](/docs/11.x/blade) 문자열을 평가하고 렌더링할 수 있습니다. 이 메서드도 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

`component` 메서드는 [Blade 컴포넌트](/docs/11.x/blade#components)를 평가하고 렌더링합니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

<a name="response-assertions"></a>
### 응답 어설션 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 사용할 수 있는 다양한 커스텀 어설션 메서드를 제공합니다. 이 어설션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답 객체에서 접근할 수 있습니다:

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
[assertUnsupportedMediaType](#assert-unsupported-media-type)  
[assertValid](#assert-valid)  
[assertInvalid](#assert-invalid)  
[assertViewHas](#assert-view-has)  
[assertViewHasAll](#assert-view-has-all)  
[assertViewIs](#assert-view-is)  
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 나쁜 요청(400) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertBadRequest();
```

<a name="assert-accepted"></a>
#### assertAccepted

응답이 수락됨(202) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertAccepted();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 충돌(409) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 특정 쿠키가 포함되어 있는지 검증합니다:

```
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 특정 쿠키가 포함되어 있으며 만료되었는지 검증합니다:

```
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 특정 쿠키가 포함되어 있고 만료되지 않았는지 검증합니다:

```
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 특정 쿠키가 포함되어 있지 않은지 검증합니다:

```
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 생성됨(201) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답 본문에 주어진 문자열이 포함되어 있지 않은지 검증합니다. 두 번째 인수에 `false`를 전달하지 않으면 문자열을 자동으로 이스케이프합니다:

```
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 주어진 문자열이 포함되어 있지 않은지 검증합니다. 두 번째 인수에 `false`를 전달하지 않으면 자동으로 이스케이프합니다. 응답 내용은 PHP의 `strip_tags` 함수를 거친 후 검증됩니다:

```
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"인지 검증합니다. 일반적으로 호출된 라우트가 `Response::download`, `BinaryFileResponse` 또는 `Storage::download` 응답을 반환한 경우입니다:

```
$response->assertDownload();
```

원한다면 다운로드된 파일명이 지정한 파일명인지도 검증할 수 있습니다:

```
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 주어진 JSON 데이터와 정확히 일치하는지 검증합니다:

```
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 주어진 JSON 구조와 정확히 일치하는지 검증합니다:

```
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 엄격합니다. 예상 JSON 구조에 명시되지 않은 키가 응답에 있으면 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 접근 금지(403) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 찾음(302) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 없어진(410) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 특정 헤더가 지정한 값으로 존재하는지 검증합니다:

```
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 특정 헤더가 존재하지 않는지 검증합니다:

```
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 내부 서버 오류(500) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 주어진 JSON 데이터가 포함되어 있는지 검증합니다:

```
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환해 지정한 부분 배열이 포함되어 있는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있어도 지정한 조각이 존재하면 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON의 배열이 지정한 키에 대해 기대하는 아이템 개수와 일치하는지 검증합니다:

```
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답 내에 주어진 JSON 데이터가 어디든 포함되어 있는지 검증합니다:

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

응답 JSON이 배열인지 검증합니다:

```
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 검증합니다:

```
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정한 JSON 데이터가 포함되어 있지 않은지 검증합니다:

```
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 정확히 일치하는 JSON 데이터가 없음을 검증합니다:

```
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 주어진 키에 대한 JSON 유효성 검증 오류가 없는지 확인합니다:

```
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]  
> 더 넓은 범위의 [assertValid](#assert-valid) 메서드로는 JSON 유효성 오류가 없고, 세션에도 오류가 저장되지 않았음을 검증할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답 JSON 특정 경로에 주어진 값이 있는지 검증합니다:

```
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 다음 JSON 응답이 있을 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 객체의 `name` 값이 특정 문자열과 같은지 아래처럼 검증할 수 있습니다:

```
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정한 JSON 경로가 존재하지 않음을 검증합니다:

```
$response->assertJsonMissingPath($path);
```

예를 들어, 위 JSON 응답에서 `user` 객체에 `email` 속성이 없음을 검증하려면:

```
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 지정한 JSON 구조를 포함하고 있음을 검증합니다:

```
$response->assertJsonStructure(array $structure);
```

예를 들어, JSON 응답으로 다음 데이터가 반환되었을 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

JSON 구조가 예상과 일치하는지 아래처럼 검증할 수 있습니다:

```
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때때로 JSON 응답 내에 객체 배열이 포함될 수도 있습니다:

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

이때는 `*` 문자를 사용해 배열 내 모든 객체의 구조를 검증할 수 있습니다:

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

응답에 지정한 키에 대한 JSON 유효성 검증 오류가 포함되어 있음을 검증합니다. 이 메서드는 유효성 오류가 JSON 구조로 반환될 때 사용됩니다:

```
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]  
> 더 넓은 범위의 [assertInvalid](#assert-invalid) 메서드로는 JSON 또는 세션에 유효성 오류가 존재함을 검증할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답이 특정 키에 대해 JSON 유효성 오류를 갖고 있는지 검증합니다:

```
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 허용되지 않은 메서드(405) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 영구 이동(301) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답 헤더 `Location`에 주어진 URI가 있는지 검증합니다:

```
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 내용이 지정한 문자열과 일치하는지 검증합니다:

```
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정한 HTTP 상태 코드를 가지며 콘텐츠가 없는지 검증합니다:

```
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트리밍 응답인지 검증합니다:

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트리밍 응답 내용이 특정 문자열과 일치하는지 검증합니다:

```
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 찾을 수 없음(404) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 OK(200) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 결제 필요(402) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

암호화되지 않은 특정 쿠키가 응답에 포함되어 있는지 검증합니다:

```
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 특정 URI로 리다이렉트하는지 검증합니다:

```
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 리다이렉트하는 URI가 특정 문자열을 포함하는지 검증합니다:

```
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 특정 [명명된 라우트](/docs/11.x/routing#named-routes)로 리다이렉트하는지 검증합니다:

```
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 특정 [서명된 라우트](/docs/11.x/urls#signed-urls)로 리다이렉트하는지 검증합니다:

```
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 요청 시간초과(408) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

응답 본문에 지정한 문자열이 포함되어 있음을 검증합니다. 두 번째 인수를 `false`로 지정하지 않으면 문자열을 자동으로 이스케이프합니다:

```
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답에 지정한 문자열들이 순서대로 포함되어 있음을 검증합니다. 두 번째 인수를 `false`로 지정하지 않으면 자동으로 이스케이프합니다:

```
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 텍스트에 지정한 문자열이 포함되어 있음을 검증합니다. 두 번째 인수를 `false`로 지정하지 않으면 자동으로 이스케이프합니다. 응답 내용은 `strip_tags` 함수를 거쳐 검증됩니다:

```
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에 지정한 문자열들이 순서대로 포함되어 있음을 검증합니다. 두 번째 인수를 `false`로 지정하지 않으면 자동으로 이스케이프합니다. 응답 내용은 `strip_tags` 함수를 거쳐 검증됩니다:

```
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 500 이상 600 미만의 서버 오류 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertServerError();
```

<a name="assert-server-unavailable"></a>
#### assertServiceUnavailable

응답이 서비스 이용 불가(503) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

응답 세션에 특정 데이터가 포함되어 있는지 검증합니다:

```
$response->assertSessionHas($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 전달할 수 있으며, 클로저가 `true`를 반환하면 검증에 성공합니다:

```
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

[플래시된 입력 데이터](/docs/11.x/responses#redirecting-with-flashed-session-data)에 특정 값이 포함되어 있는지 검증합니다:

```
$response->assertSessionHasInput($key, $value = null);
```

필요하다면 두 번째 인수로 클로저를 사용해 검증할 수도 있습니다:

```
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

응답 세션이 특정 키/값 쌍들을 모두 포함하고 있는지 검증합니다:

```
$response->assertSessionHasAll(array $data);
```

예를 들어, 세션 내 `name`과 `status` 키가 존재하며 지정한 값과 일치하는지 검증하려면:

```
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

주어진 `$keys`에 대해 세션에 오류가 포함되어 있는지 검증합니다. 만약 `$keys`가 연관 배열이면, 각 필드 키에 대응하는 오류 메시지도 함께 검증합니다. 이 메서드는 유효성 오류가 세션에 플래시 된 경우에 사용합니다:

```
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, `name`과 `email` 필드에 유효성 오류 메시지가 플래시 됐는지 검증하려면:

```
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드가 특정 오류 메시지를 가지고 있는지 검증할 수도 있습니다:

```
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]  
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면 JSON 응답이나 세션에 유효성 오류가 존재함을 검증할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [에러 백(error bag)](/docs/11.x/validation#named-error-bags) 내에 지정한 `$keys`가 오류를 포함하고 있는지 검증합니다. `$keys`가 연관 배열이면 필드별 오류 메시지도 함께 검사합니다:

```
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 오류가 없음을 검증합니다:

```
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

지정한 키에 대해 세션에 유효성 오류가 없음을 검증합니다:

```
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]  
> 더 넓은 범위의 [assertValid](#assert-valid) 메서드를 사용하면 JSON과 세션 모두 유효성 오류가 없음을 검증할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정한 키가 존재하지 않음을 검증합니다:

```
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 지정한 HTTP 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공(200 이상 300 미만) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 요청 과다(429) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 인증되지 않음(401) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 처리할 수 없음(422) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 지원하지 않는 미디어 타입(415) 상태 코드를 가지고 있는지 검증합니다:

```
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

주어진 키에 대해 응답에 유효성 오류가 없음을 검증합니다. JSON 응답이나 세션에 플래시된 오류 모두 검증합니다:

```
// 유효성 오류가 없음 검증...
$response->assertValid();

// 지정한 키들의 유효성 오류가 없음 검증...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

주어진 키에 대해 응답에 유효성 오류가 있음을 검증합니다. JSON 응답이나 세션에 플래시된 오류 모두 검증합니다:

```
$response->assertInvalid(['name', 'email']);
```

특정 키가 특정 유효성 오류 메시지를 포함하는지도 검증할 수 있습니다. 전체 메시지이거나 일부 문구만 포함해도 됩니다:

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 특정 데이터가 포함되어 있는지 검증합니다:

```
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 넘길 수 있으며, 클로저에서 뷰 데이터에 대한 어설션을 수행할 수 있습니다:

```
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

뷰 데이터는 응답에서 배열처럼 접근 가능하므로, 편리하게 검사할 수도 있습니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 지정한 여러 데이터를 모두 포함하고 있는지 검증합니다:

```
$response->assertViewHasAll(array $data);
```

키 배열을 넘겨서 단순히 존재 여부만 검증하거나:

```
$response->assertViewHasAll([
    'name',
    'email',
]);
```

키-값 쌍으로 구체적인 값을 검증할 수도 있습니다:

```
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

응답이 지정한 뷰를 반환했는지 검증합니다:

```
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 특정 키가 포함되어 있지 않음을 검증합니다:

```
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 관련 어설션 (Authentication Assertions)

Laravel은 애플리케이션 기능 테스트에서 사용할 수 있는 여러 인증 관련 어설션을 제공합니다. 이 메서드들은 `Illuminate\Testing\TestResponse`가 아닌 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 검증합니다:

```
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지 검증합니다:

```
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 검증합니다:

```
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어설션 (Validation Assertions)

Laravel은 요청 데이터가 유효한지 또는 유효하지 않은지를 검증하기 위한 주요 어설션 두 가지를 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

주어진 키에 대한 유효성 오류가 없음을 검증합니다. JSON 또는 세션에 플래시된 오류 모두를 검사합니다:

```
// 오류 없음 검증...
$response->assertValid();

// 지정한 키 오류 없음 검증...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

주어진 키에 대한 유효성 오류가 있음을 검증합니다. JSON 또는 세션에 플래시된 오류 모두를 검사합니다:

```
$response->assertInvalid(['name', 'email']);
```

특정 키에 대한 특정 오류 메시지가 포함되었는지 검증할 수도 있습니다. 전체 메시지이거나 일부 문장만 포함해도 됩니다:

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```