# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한 JSON 테스트(Fluent JSON Testing)](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어설션](#available-assertions)
    - [응답 어설션](#response-assertions)
    - [인증 어설션](#authentication-assertions)
    - [유효성 검증 어설션](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사하는 데 매우 직관적인 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보세요:

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

`get` 메서드는 애플리케이션으로 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 특정 HTTP 상태 코드를 가지고 있음을 확인합니다. 이 간단한 어설션 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 어설션을 제공합니다.

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 호출할 수 있습니다. 이 메서드들은 실제 "실제" HTTP 요청을 보내지 않고, 내부적으로 네트워크 요청을 시뮬레이션합니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, 대신 [다양한 유용한 어설션](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이를 통해 애플리케이션의 응답을 편리하게 검사할 수 있습니다:

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

일반적으로 각 테스트는 애플리케이션에 한 번만 요청을 보내야 합니다. 한 테스트 메서드 내에서 여러 요청을 실행할 경우 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해, 테스트 실행 시 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징 (Customizing Request Headers)

`withHeaders` 메서드를 사용해 요청이 애플리케이션에 전송되기 전에 요청 헤더를 커스터마이징할 수 있습니다. 이 메서드는 요청에 원하는 커스텀 헤더를 추가하는 데 사용됩니다:

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

요청을 보내기 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 두 개의 인수로 받고, `withCookies`는 이름/값 쌍 배열을 받습니다:

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

Laravel은 HTTP 테스트 중 세션과 상호작용하는 여러 헬퍼 메서드를 제공합니다. 먼저, `withSession` 메서드를 사용해 요청 이전에 세션 데이터를 배열 형태로 설정할 수 있습니다. 이는 요청 전에 세션에 데이터를 미리 설정할 때 유용합니다:

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

Laravel 세션은 보통 현재 인증된 사용자의 상태 유지를 위해 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 특정 사용자를 현재 인증된 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/master/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

또한 `actingAs` 메서드의 두 번째 인수로 가드 이름을 전달해 인증에 사용할 가드를 지정할 수 있습니다. 지정된 가드는 테스트 기간 동안 기본 가드가 됩니다:

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

애플리케이션에 테스트 요청을 실행한 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 검사하고 디버깅할 수 있습니다:

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

또는 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용해서 응답에 관한 정보를 덤프한 뒤 실행을 중단할 수도 있습니다:

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

때때로 애플리케이션이 특정 예외를 발생시키는지 테스트할 필요가 있습니다. 이를 위해 `Exceptions` 파사드를 사용해 예외 핸들러를 "가짜로" 설정할 수 있습니다. 핸들러가 가짜로 설정된 후에는 요청 중 발생한 예외에 대해 `assertReported`, `assertNotReported` 메서드를 사용해 어설션을 수행할 수 있습니다:

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // 예외 발생 여부 확인...
    Exceptions::assertReported(InvalidOrderException::class);

    // 예외 내용에 대한 어설션...
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

        // 예외 발생 여부 확인...
        Exceptions::assertReported(InvalidOrderException::class);

        // 예외 내용에 대한 어설션...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

`assertNotReported`와 `assertNothingReported` 메서드를 사용하면 특정 예외가 발생하지 않았거나, 아무 예외도 발생하지 않았음을 확인할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하려면 요청 전에 `withoutExceptionHandling` 메서드를 호출하세요:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한 PHP나 애플리케이션에서 사용하는 라이브러리의 비권장(deprecated) 기능이 포함되지 않았는지 확인하려면 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이 설정이 활성화되면 비권장 경고가 예외로 변환되어 테스트가 실패합니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드를 사용해 주어진 클로저 내에서 특정 타입의 예외가 던져지는지 어설션할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외가 던져졌을 때 그 예외에 대해 검사하거나 어설션을 수행하려면 `assertThrows` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API와 응답을 테스트하기 위한 여러 헬퍼 메서드를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용해 다양한 HTTP 동사를 가진 JSON 요청을 보낼 수 있습니다. 데이터와 헤더를 쉽게 전달할 수 있습니다. 시작하기 위해 `/api/user`에 `POST` 요청을 보내고 예상 JSON 데이터를 확인하는 테스트를 작성해 봅시다:

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

또한 JSON 응답 데이터는 배열 변수처럼 응답 객체에서 접근할 수 있어 JSON 내의 개별 값을 편리하게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 다음, 주어진 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 프로퍼티가 있어도 주어진 배열 조각이 있으면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어설션 (Asserting Exact JSON Matches)

앞서 설명한 `assertJson` 메서드는 JSON 응답 안에 특정 일부 데이터가 포함되어 있는지 검사합니다. JSON 전체가 **정확히 일치함**을 확인하려면 `assertExactJson` 메서드를 사용해야 합니다:

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
#### JSON 경로 어설션 (Asserting on JSON Paths)

JSON 응답에서 특정 경로에 특정 데이터가 있는지 확인하려면 `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath`는 두 번째 인수로 클로저도 받으며, 이를 사용해 동적으로 어설션의 통과 여부를 결정할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트 (Fluent JSON Testing)

Laravel은 애플리케이션의 JSON 응답을 유창하게 테스트할 수 있는 훌륭한 방법도 제공합니다. 시작하려면 `assertJson` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인수로 받아, JSON에 대한 어설션을 수행할 수 있습니다. `where` 메서드는 JSON의 특정 속성 값에 대해 어설션하는 데 사용되고, `missing` 메서드는 특정 속성이 JSON에 존재하지 않는지 확인하는 데 사용됩니다:

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

예제에서 마지막으로 호출된 `etc` 메서드에 주목하세요. 이 메서드는 Laravel에 JSON 객체에 다른 속성들도 있을 수 있음을 알립니다. `etc`를 호출하지 않으면 어설션에 포함되지 않은 다른 속성이 존재할 경우 테스트가 실패합니다.

이 동작은 민감한 정보를 JSON 응답에서 의도치 않게 노출하는 것을 방지하기 위한 의도로, 속성에 대해 명시적으로 어설션하거나, `etc` 메서드로 추가 속성을 허용하지 않는 이상 실패하도록 설계되었습니다.

다만, `etc` 메서드는 JSON 객체 내 중첩된 배열에 추가 속성이 있는지 여부는 보장하지 않습니다. 호출된 중첩 단계에서만 추가 속성이 없는지 보장합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재 및 부재 어설션 (Asserting Attribute Presence / Absence)

속성이 존재하는지 또는 없는지 검증하려면 각각 `has`와 `missing` 메서드를 사용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한, 한 번에 여러 속성을 검증하려면 `hasAll`와 `missingAll` 메서드를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

목록 중 최소 하나만 존재하는지 확인하고 싶을 때는 `hasAny` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어설션 (Asserting Against JSON Collections)

라우트가 여러 아이템을 포함한 JSON 응답(예: 여러 사용자)을 반환하는 경우가 많습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이럴 때 유창한 JSON 객체의 `has` 메서드를 사용해 응답 내 사용자 수를 어설션할 수 있습니다. 그리고 `first` 메서드를 사용해 첫 번째 객체에 대한 어설션을 할 수 있습니다. `first`는 클로저를 받아서 해당 JSON 컬렉션의 첫 객체에 맞게 어설션할 수 있도록 해줍니다:

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

경우에 따라 라우트가 명명된 키로 JSON 컬렉션을 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이때 `has` 메서드를 사용해 컬렉션 내 아이템 개수를 어설션하고, 클로저를 인수로 전달해 특정 항목 스코프 내에서 어설션을 할 수 있습니다:

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

또는 `users` 컬렉션에 대해 두 번 호출하지 않고, 세 번째 인자로 클로저를 전달해 첫 번째 아이템에 대한 범위를 자동으로 지정할 수 있습니다:

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

JSON 응답 내 프로퍼티의 타입만 검증하려면 `AssertableJson` 클래스의 `whereType`과 `whereAllType` 메서드를 이용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`whereType` 메서드는 `|` 문자로 여러 타입을 지정할 수 있고, 배열로 여러 타입을 전달할 수도 있습니다. 이 경우 응답 값이 나열된 타입 중 하나만 일치해도 어설션이 통과합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

지원하는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null`입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 이용하면 테스트용 더미 파일 또는 이미지를 생성할 수 있습니다. 이와 `Storage` 파사드의 `fake` 메서드를 함께 사용하면 파일 업로드 테스트를 매우 쉽게 할 수 있습니다. 예를 들어, 아바타 업로드 폼을 테스트할 때 이렇게 쓸 수 있습니다:

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

특정 파일이 존재하지 않음을 어설션하려면 `Storage` 파사드에서 `assertMissing` 메서드를 사용하세요:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징 (Fake File Customization)

`UploadedFile` 클래스의 `fake` 메서드로 이미지 생성 시 너비, 높이, 크기(킬로바이트)를 지정해 애플리케이션의 유효성 검증 규칙을 더 잘 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도 `create` 메서드를 사용해 다른 타입의 파일을 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하면 `$mimeType` 인수로 명시적으로 MIME 타입을 지정할 수도 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 애플리케이션에 시뮬레이션된 HTTP 요청 없이도 뷰를 렌더링하도록 허용합니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하세요. `view` 메서드는 뷰 이름과 선택적 데이터 배열을 인수로 받으며, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 클래스는 뷰 내용에 관한 다양한 편리한 어설션 메서드를 제공합니다:

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

`TestView` 클래스가 제공하는 어설션 메서드는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 등이 있습니다.

필요하면 `TestView` 인스턴스를 문자열로 변환해 렌더링된 뷰의 원초적 내용을 얻을 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유 (Sharing Errors)

어떤 뷰는 Laravel이 제공하는 [글로벌 에러 백(error bag)](/docs/master/validation#quick-displaying-the-validation-errors)에 공유된 에러 메시지에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면 `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링 (Rendering Blade and Components)

필요시 `blade` 메서드를 이용해 원본 [Blade](/docs/master/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

또한 `component` 메서드를 사용하면 [Blade 컴포넌트](/docs/master/blade#components)를 평가하고 렌더링할 수 있습니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

<a name="response-assertions"></a>
### 응답 어설션 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 활용할 수 있는 여러 커스텀 어설션 메서드를 제공합니다. 이들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답에서 사용할 수 있습니다:

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

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 잘못된 요청(HTTP 400 상태 코드)임을 어설션합니다:

```php
$response->assertBadRequest();
```

<a name="assert-accepted"></a>
#### assertAccepted

응답이 수락됨(HTTP 202 상태 코드)임을 어설션합니다:

```php
$response->assertAccepted();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 충돌(HTTP 409 상태 코드)임을 어설션합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 주어진 쿠키가 포함되어 있음을 어설션합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 주어진 쿠키가 포함되어 있고 만료되었음을 어설션합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 주어진 쿠키가 포함되어 있고 만료되지 않았음을 어설션합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 주어진 쿠키가 포함되어 있지 않음을 어설션합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 HTTP 201 상태 코드임을 어설션합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

주어진 문자열이 애플리케이션이 반환한 응답에 포함되지 않음을 어설션합니다. 기본적으로 문자열을 이스케이프 처리하며, 두 번째 인수로 `false`를 전달하면 이스케이프를 하지 않습니다:

```php
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

주어진 문자열이 응답 텍스트에 포함되지 않음을 어설션합니다. 기본적으로 이스케이프 처리하며, 두 번째 인수로 `false`를 전달하면 이스케이프를 하지 않습니다. 이 메서드는 PHP의 `strip_tags` 함수를 사용해 응답 내용을 태그 제거 후 검사합니다:

```php
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 “다운로드”임을 어설션합니다. 일반적으로 라우트가 `Response::download` 응답, `BinaryFileResponse` 또는 `Storage::download` 응답을 반환했음을 의미합니다:

```php
$response->assertDownload();
```

필요하다면 다운로드 파일에 지정된 이름이 있는지 어설션할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 주어진 JSON 데이터와 정확히 일치함을 어설션합니다:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 주어진 JSON 구조와 정확히 일치함을 어설션합니다:

```php
$response->assertExactJsonStructure(array $data);
```

이메서드는 [assertJsonStructure](#assert-json-structure)보다 더 엄격한 버전으로, 기대한 JSON 구조에 명시되지 않은 키가 응답에 있으면 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 금지됨(HTTP 403 상태 코드)임을 어설션합니다:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 발견됨(HTTP 302 상태 코드)임을 어설션합니다:

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 사라짐(HTTP 410 상태 코드)임을 어설션합니다:

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 주어진 헤더와 값이 포함되어 있음을 어설션합니다:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 주어진 헤더가 포함되어 있지 않음을 어설션합니다:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 내부 서버 오류(HTTP 500 상태 코드)임을 어설션합니다:

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답이 주어진 JSON 데이터를 포함하고 있음을 어설션합니다:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메서드는 응답을 배열로 변환 후 지정된 배열이 JSON 응답 내에 포함되어 있는지를 확인합니다. 따라서 JSON 응답에 추가 프로퍼티가 있어도 주어진 조각이 있으면 테스트는 성공합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON 내 주어진 키에 포함된 배열 아이템 수가 기대한 개수인지 어설션합니다:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 지정된 JSON 데이터가 포함되어 있음을 어디서든지 어설션합니다:

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

응답 JSON이 배열임을 어설션합니다:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체임을 어설션합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정된 JSON 데이터가 포함되어 있지 않음을 어설션합니다:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 지정된 JSON 데이터가 정확히 포함되어 있지 않음을 어설션합니다:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 주어진 키의 JSON 유효성 검증 오류가 없음을 어설션합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 JSON으로 반환된 유효성 오류가 없고 세션에도 오류가 플래시되지 않았음을 어설션할 때 사용할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답의 지정된 JSON 경로에 주어진 값이 포함되어 있음을 어설션합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 다음과 같은 JSON 응답이 있을 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 `user` 객체의 `name` 속성이 특정 값과 일치하는지 검사할 수 있습니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정된 JSON 경로가 포함되어 있지 않음을 어설션합니다:

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 위 JSON 응답에 `user.email` 속성이 없는지 확인하려면:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 주어진 JSON 구조를 포함하고 있음을 어설션합니다:

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, JSON 응답이 다음과 같다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음처럼 구조를 어설션할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

종종 JSON 응답에 객체 배열이 포함될 수 있는데:

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

이 경우 `*` 문자를 사용해 배열 내 모든 객체에 대해 구조를 어설션할 수 있습니다:

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

JSON 유효성 검증 오류가 응답에 포함되어 있고, 주어진 키에 해당하는 오류가 있는지 어설션합니다. 이 메서드는 유효성 실패 시 JSON 구조로 오류를 반환하는 API 테스트에 사용합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON으로 반환되거나 세션에 플래시된 유효성 오류가 있는지 어설션하는 데 사용됩니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답에 주어진 키에 대해 어떤 JSON 유효성 검증 오류가 포함되어 있는지 어설션합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 허용되지 않은 메서드(HTTP 405 상태 코드)임을 어설션합니다:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 영구 이동(HTTP 301 상태 코드)임을 어설션합니다:

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

주어진 문자열과 응답 콘텐츠가 정확히 일치함을 어설션합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 주어진 HTTP 상태 코드이며 본문 내용이 없음을 어설션합니다:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트리밍 응답임을 어설션합니다:

```php
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트리밍 응답 콘텐츠가 주어진 문자열과 일치함을 어설션합니다:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 찾을 수 없음(HTTP 404 상태 코드)임을 어설션합니다:

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 HTTP 200 상태 코드임을 어설션합니다:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 결제 필요(HTTP 402 상태 코드)임을 어설션합니다:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

암호화되지 않은 쿠키가 응답에 포함됨을 어설션합니다:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 주어진 URI로 리다이렉트됨을 어설션합니다:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 특정 문자열이 포함된 URI로 리다이렉트되는지 어설션합니다:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 주어진 [명명된 라우트](/docs/master/routing#named-routes)로 리다이렉트됨을 어설션합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 주어진 [서명된 라우트](/docs/master/urls#signed-urls)로 리다이렉트됨을 어설션합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 요청 시간 초과(HTTP 408 상태 코드)임을 어설션합니다:

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

주어진 문자열이 응답에 포함되어 있음을 어설션합니다. 기본적으로 문자열을 이스케이프 처리하며, 두 번째 인수로 `false`를 전달해 이스케이프를 하지 않을 수 있습니다:

```php
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

주어진 문자열들이 응답 내에 순서대로 포함되어 있음을 어설션합니다. 기본적으로 문자열들을 이스케이프 처리하며, 두 번째 인수로 `false`를 전달할 수 있습니다:

```php
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

주어진 문자열이 응답 텍스트에 포함되어 있음을 어설션합니다. 기본적으로 이스케이프 처리하며, 두 번째 인수로 `false`를 전달할 수 있습니다. 검사 전에 `strip_tags` PHP 함수를 사용합니다:

```php
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

주어진 문자열들이 응답 텍스트 내에 순서대로 포함되어 있음을 어설션합니다. 기본적으로 이스케이프 처리하며, 두 번째 인수로 `false`를 전달할 수 있습니다. 검사 전 `strip_tags` 함수를 사용합니다:

```php
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 오류(HTTP 500~599 상태 코드)임을 어설션합니다:

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 서비스 불가(HTTP 503 상태 코드)임을 어설션합니다:

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 주어진 데이터가 포함되어 있음을 어설션합니다:

```php
$response->assertSessionHas($key, $value = null);
```

필요시 두 번째 인수로 클로저를 전달해 값에 대해 검사할 수 있으며, 클로저가 `true` 반환 시 어설션이 통과합니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

[플래시된 입력 데이터 배열](/docs/master/responses#redirecting-with-flashed-session-data)에 특정 값이 포함되어 있음을 어설션합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```

필요시 클로저를 두 번째 인수로 전달할 수 있으며, `true` 반환 시 어설션 통과입니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 주어진 키/값 배열이 모두 포함되어 있음을 어설션합니다:

```php
$response->assertSessionHasAll(array $data);
```

예를 들어 세션에 `name`과 `status`가 포함되어 있고 특정 값인지 확인하려면:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 주어진 `$keys`에 대한 오류가 포함되어 있음을 어설션합니다. `$keys`가 연관 배열이면 각 필드에 특정 오류 메시지가 포함됨을 검사합니다. 이 메서드는 유효성 오류가 세션에 플래시될 때 사용합니다:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, 이름과 이메일 필드에 유효성 오류가 플래시되었는지 검사하려면:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

또는 특정 필드에 특정 오류 메시지가 있는지 검사 가능합니다:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON으로 반환되거나 세션에 플래시된 유효성 오류 여부를 검사할 때 활용할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [에러 백(error bag)](/docs/master/validation#named-error-bags) 내에 주어진 `$keys`에 대한 오류가 포함되어 있음을 어설션합니다. `$keys`가 연관 배열이면 각 필드가 해당 에러 백에 특정 메시지를 포함하는지 검사합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 오류가 하나도 없음을 어설션합니다:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 주어진 키에 대한 유효성 오류가 없음을 어설션합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 JSON 또는 세션에 유효성 오류가 없음도 확인합니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 주어진 키가 포함되어 있지 않음을 어설션합니다:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 특정 HTTP 상태 코드임을 어설션합니다:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공 상태(HTTP 200 이상 300 미만)임을 어설션합니다:

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 요청 과다(HTTP 429 상태 코드)임을 어설션합니다:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 인증되지 않음(HTTP 401 상태 코드)임을 어설션합니다:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 처리할 수 없음(HTTP 422 상태 코드)임을 어설션합니다:

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 지원하지 않는 미디어 타입(HTTP 415 상태 코드)임을 어설션합니다:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답에 주어진 키에 대한 유효성 오류가 없음을 어설션합니다. 이 메서드는 JSON 또는 세션에 유효성 오류가 없는지 검사할 때 사용합니다:

```php
// 유효성 오류가 없음을 어설션...
$response->assertValid();

// 주어진 키에 유효성 오류가 없음을 어설션...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 주어진 키에 대해 유효성 오류가 있음을 어설션합니다. JSON 또는 세션에 플래시된 오류 검사에 사용합니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 특정 오류 메시지를 포함하는지 어설션할 수도 있습니다. 전체 메시지를 제공하거나 일부 메시지 조각만 사용해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

주어진 필드만 유효성 오류가 있음을 검사하려면 `assertOnlyInvalid` 메서드를 사용하세요:

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 주어진 데이터가 포함되어 있음을 어설션합니다:

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 전달하면 특정 뷰 데이터의 값을 검사할 수 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

뷰 데이터는 배열 변수처럼도 접근할 수 있습니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 주어진 키 목록이 모두 포함되어 있음을 어설션합니다:

```php
$response->assertViewHasAll(array $data);
```

예를 들어, 뷰에 단순히 특정 키가 있어야 한다면:

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

특정 키가 명시적 값과 함께 있어야 한다면:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

라우트에서 반환한 뷰가 지정한 뷰와 일치함을 어설션합니다:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 주어진 데이터 키가 포함되어 있지 않음을 어설션합니다:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어설션 (Authentication Assertions)

Laravel은 애플리케이션의 기능 테스트 내에서 활용 가능한 여러 인증 관련 어설션을 제공합니다. 이 메서드들은 `Illuminate\Testing\TestResponse` 인스턴스가 아닌 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었음을 어설션합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았음을 어설션합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되어 있음을 어설션합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어설션 (Validation Assertions)

Laravel은 주로 두 가지 유효성 검증 어설션 메서드를 제공합니다. 요청 데이터가 유효(valid)하거나 유효하지 않음(invalid)을 검사하는 데 사용합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 주어진 키에 유효성 오류가 없음을 어설션합니다. JSON 구조로 오류가 반환되거나 세션에 플래시된 오류 여부 모두 검사합니다:

```php
// 오류가 없음을 검사...
$response->assertValid();

// 특정 키에 오류가 없음을 검사...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 주어진 키에 유효성 오류가 있음을 어설션합니다. JSON 혹은 세션 플래시 오류 모두 검사합니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 특정 오류 메시지를 포함하고 있는지도 검사할 수 있습니다. 메시지는 전체 혹은 일부 내용을 포함해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```