# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더(customizing-request-headers) 맞춤 설정](#customizing-request-headers)
    - [쿠키 (cookies)](#cookies)
    - [세션 / 인증 (session-and-authentication)](#session-and-authentication)
    - [응답 디버깅 (debugging-responses)](#debugging-responses)
    - [예외 처리 (exception-handling)](#exception-handling)
- [JSON API 테스트 (testing-json-apis)](#testing-json-apis)
    - [유창한 JSON 테스트 (fluent-json-testing)](#fluent-json-testing)
- [파일 업로드 테스트 (testing-file-uploads)](#testing-file-uploads)
- [뷰 테스트 (testing-views)](#testing-views)
    - [Blade 및 컴포넌트 렌더링 (rendering-blade-and-components)](#rendering-blade-and-components)
- [사용 가능한 단언 (available-assertions)](#available-assertions)
    - [응답 단언 (response-assertions)](#response-assertions)
    - [인증 단언 (authentication-assertions)](#authentication-assertions)
    - [유효성 검증 단언 (validation-assertions)](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 확인할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 다음과 같이 기능 테스트가 정의되어 있습니다:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 반환된 응답에 주어진 HTTP 상태 코드가 있어야 함을 단언합니다. 이 간단한 단언 외에도 Laravel은 응답 헤더, 콘텐츠, JSON 구조 등을 검사하기 위한 다양한 단언 메서드를 제공합니다.

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

애플리케이션에 요청을 만들려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 호출하면 됩니다. 이 메서드들은 실제 HTTP 네트워크 요청을 보내지 않고, 내부적으로 요청이 시뮬레이션됩니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 클래스는 [다양한 유용한 단언 메서드들](#available-assertions)을 제공하여 애플리케이션의 응답을 쉽게 검사할 수 있게 해줍니다:

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

일반적으로 각 테스트는 애플리케이션에 한 번의 요청만 수행해야 합니다. 하나의 테스트 메서드 내에서 여러 요청을 실행하면 예상치 못한 동작이 발생할 수 있습니다.

> [!NOTE]
> 테스트를 실행할 때 CSRF 미들웨어는 편의를 위해 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 맞춤 설정

`withHeaders` 메서드를 사용하면 요청을 애플리케이션에 보내기 전에 맞춤 헤더를 추가할 수 있습니다. 이 메서드는 원하는 모든 사용자 정의 헤더를 요청에 추가할 수 있게 해줍니다:

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

요청 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 두 개의 인수로 받고, `withCookies`는 이름/값 쌍 배열을 인수로 받습니다:

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

HTTP 테스트 시 세션과 상호작용할 수 있는 몇 가지 헬퍼가 제공됩니다. 먼저, `withSession` 메서드를 통해 세션 데이터를 배열 형태로 설정할 수 있는데, 이는 애플리케이션에 요청하기 전에 세션에 데이터를 미리 넣어둘 때 유용합니다:

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

Laravel 세션은 보통 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 특정 사용자를 현재 인증 사용자로 간단하게 설정하는 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다:

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

또한, `actingAs` 메서드의 두 번째 인수로 인증에 사용할 guard 이름을 지정할 수 있습니다. 이 guard는 테스트가 실행되는 동안 기본 guard가 됩니다:

```php
$this->actingAs($user, 'web')
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

또는 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하여 응답 정보를 덤프하고 실행을 중단할 수도 있습니다:

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

애플리케이션이 특정 예외를 던지는지 테스트해야 할 때가 있습니다. 이 경우, `Exceptions` 파사드를 통해 예외 핸들러를 "가짜"로 만들 수 있습니다. 예외 핸들러가 가짜로 설정되면, `assertReported`와 `assertNotReported` 메서드를 사용해 요청 중에 발생한 예외에 대한 단언을 할 수 있습니다:

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // 예외가 발생했는지 확인...
    Exceptions::assertReported(InvalidOrderException::class);

    // 예외 내용을 검증...
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

        // 예외가 발생했는지 확인...
        Exceptions::assertReported(InvalidOrderException::class);

        // 예외 내용을 검증...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

`assertNotReported`와 `assertNothingReported` 메서드는 요청 중에 특정 예외가 발생하지 않았거나 아예 발생하지 않았음을 단언할 때 사용합니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

예외 처리를 완전히 비활성화하고 싶다면 요청 전에 `withoutExceptionHandling` 메서드를 호출하세요:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 또는 라이브러리에서 더 이상 권장되지 않는 기능이 사용되는지 확인하고 싶다면 `withoutDeprecationHandling` 메서드를 요청 전에 호출하세요. 비활성화하면 더 이상 권장되지 않는 경고가 예외로 바뀌어 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드를 사용하면 특정 유형의 예외가 던져지는지 단언할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

던져진 예외를 검사하고 단언하려면, `assertThrows` 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow`는 주어진 클로저 내에서 예외가 전혀 던져지지 않음을 단언합니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API와 그 응답을 테스트하기 위한 여러 헬퍼도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용해 다양한 HTTP 메서드로 JSON 요청을 쉽게 보낼 수 있습니다. 데이터와 헤더도 쉽게 전달할 수 있습니다. 다음 예시는 `/api/user`에 `POST` 요청을 보내고 예상 JSON 데이터를 단언하는 테스트입니다:

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

또한 JSON 응답 데이터는 응답을 배열처럼 접근할 수 있어, JSON 반환값 내 개별 값을 간편하게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여 주어진 배열이 JSON 응답 내 포함되어 있는지 검증합니다. 따라서 JSON 응답에 다른 속성이 있어도 주어진 조각이 존재한다면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 단언 (Asserting Exact JSON Matches)

앞서 설명한 `assertJson`은 JSON의 일부 조각 존재를 단언합니다. 만약 애플리케이션이 반환하는 JSON이 주어진 배열과 완벽히 일치하는지 검증하려면 `assertExactJson`을 사용하세요:

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

JSON 응답 내 특정 경로(path)에 주어진 데이터가 포함되어 있는지 확인하려면 `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath`는 클로저도 받아서, 동적으로 단언 조건을 판단할 수도 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트 (Fluent JSON Testing)

Laravel은 애플리케이션의 JSON 응답을 유창하게 테스트하기 위한 멋진 방법도 제공합니다. `assertJson` 메서드에 클로저를 전달하면, 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인수로 받습니다. 이 인스턴스는 반환된 JSON에 대해 단언을 할 수 있도록 해줍니다. `where` 메서드는 JSON 속성을 대상으로 단언하며, `missing` 메서드는 특정 속성이 JSON에 없는지 단언할 때 사용합니다:

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

위 예제에서 단언 체인의 마지막에 `etc` 메서드를 호출한 것을 볼 수 있습니다. 이 메서드는 해당 JSON 객체에 다른 속성이 더 있을 수 있음을 Laravel에 알려줍니다. 만약 `etc`를 호출하지 않으면, 당신이 단언하지 않은 추가 속성이 있다면 테스트가 실패합니다.

이는 JSON 응답에 의도치 않게 민감한 정보가 노출되는 것을 방지하기 위함입니다. 명시적으로 속성에 대해 단언하거나, `etc`로 추가 속성을 허용해야 합니다.

하지만 `etc`는 JSON 객체의 해당 중첩 수준에서만 작동하며, 더 깊은 배열 안에 있는 객체의 속성까지는 보장하지 않습니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재 / 부재 단언

특정 속성이 있거나 없는지 단언하려면 `has` 및 `missing` 메서드를 사용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한 `hasAll`, `missingAll` 메서드로 여러 속성의 존재 또는 부재를 동시에 단언할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드는 전달한 여러 속성 중 적어도 하나가 있는지 단언합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 단언

라우트가 여러 항목(예: 사용자 목록)을 반환하는 JSON 응답이라면, 유창한 JSON 객체의 `has` 메서드를 활용해 응답에 포함된 항목 개수와 개별 요소 단언이 가능합니다. 예를 들어, 응답에 사용자 3명이 포함되어 있고 첫 번째 사용자에 대해 단언하는 예시는 다음과 같습니다:

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
#### JSON 컬렉션 단언 범위 지정

때때로 라우트가 명명된 키를 가진 JSON 컬렉션을 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
});
```

이 경우, `has` 메서드를 통해 컬렉션 항목 수를 단언할 수 있고, 클로저를 전달해 세부 단언 범위를 지정할 수 있습니다:

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

`users` 컬렉션에 대해 두 번 호출하지 않고, 세 번째 인수로 클로저를 전달하면 자동으로 첫 번째 항목 범위 내 클로저가 실행됩니다:

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

JSON 응답 내 속성의 타입만 검증하려면 `Illuminate\Testing\Fluent\AssertableJson` 클래스가 제공하는 `whereType` 및 `whereAllType` 메서드를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`whereType` 두 번째 인수에 `|`로 구분된 문자열 또는 타입 배열을 지정할 수도 있습니다. 응답 값이 목록 중 하나의 타입이면 단언이 성공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

지원하는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null`입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일이나 이미지를 생성하는 `fake` 메서드를 제공합니다. 이것과 함께 `Storage` 파사드의 `fake` 메서드를 사용하면 파일 업로드 테스트가 매우 용이해집니다. 예를 들어, 아바타 업로드 폼 테스트는 아래와 같습니다:

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

특정 파일이 존재하지 않는다는 단언은 `Storage`의 `assertMissing` 메서드를 사용하세요:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 맞춤 설정

`UploadedFile::fake()`로 파일 생성 시 이미지 너비, 높이, 크기(킬로바이트 단위)를 지정하여 유효성 검증 규칙을 좀 더 정확히 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외 다양한 타입 파일은 `create` 메서드로 생성 가능합니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하면 `$mimeType` 인수를 넘겨 MIME 타입을 명확히 정의할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 애플리케이션에 시뮬레이션 HTTP 요청을 보내지 않고도 뷰를 렌더링할 수 있습니다. 이를 위해 테스트 내에서 `view` 메서드를 호출할 수 있습니다. 이 메서드는 뷰 이름과 선택적인 데이터를 배열 형태로 받습니다. 반환값은 `Illuminate\Testing\TestView` 인스턴스이며, 뷰 내용을 편리하게 단언하는 여러 메서드를 제공합니다:

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

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 메서드를 제공합니다.

원시 렌더링 된 뷰 내용을 얻으려면 `TestView` 인스턴스를 문자열로 캐스팅하세요:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 오류 공유

일부 뷰는 Laravel이 제공하는 [글로벌 에러 백(error bag)](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 오류 메시지에 의존할 수 있습니다. 오류 백에 메시지를 채우려면 `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요할 경우, `blade` 메서드를 사용해 원시 [Blade](/docs/12.x/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view`와 마찬가지로 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/12.x/blade#components)를 평가하고 렌더링하려면 `component` 메서드를 사용하세요. `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 단언 (Available Assertions)

<a name="response-assertions"></a>
### 응답 단언

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 유용하게 사용할 수 있는 다양한 사용자 정의 단언 메서드를 제공합니다. 이 단언들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드들이 반환하는 응답에 대해 호출할 수 있습니다:

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
[assertUnsupportedMediaType](#assert-supported-media-type)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-accepted"></a>
#### assertAccepted

응답이 수락됨(HTTP 상태 코드 202)인지 단언합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 잘못된 요청(HTTP 상태 코드 400)인지 단언합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 오류(HTTP 상태 코드 >= 400, < 500)인지 단언합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 충돌(HTTP 상태 코드 409)인지 단언합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 주어진 쿠키가 포함되었는지 단언합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 주어진 쿠키가 포함되고 만료되었는지 단언합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 주어진 쿠키가 포함되고 만료되지 않았는지 단언합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 주어진 쿠키가 포함되지 않았는지 단언합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 생성됨(HTTP 상태 코드 201)인지 단언합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답 결과에 주어진 문자열이 포함되지 않았는지 단언합니다. 두 번째 인수에 `false`를 전달하면 자동 이스케이프가 해제됩니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 본문 텍스트에 주어진 문자열이 포함되지 않았는지 단언합니다. 역시 두 번째 인수에 `false`를 전달하면 이스케이프를 해제할 수 있습니다. 본문은 단언 전에 `strip_tags` PHP 함수에 통과됩니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"인지 단언합니다. 주로 라우트가 `Response::download`, `BinaryFileResponse`, `Storage::download` 응답을 반환했을 때입니다:

```php
$response->assertDownload();
```

특정 파일 이름이 할당되었는지 단언할 수도 있습니다:

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

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 엄격하며, 예상 JSON 구조에 명시되지 않은 키가 응답에 있으면 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 금지됨(HTTP 상태 코드 403)인지 단언합니다:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 리다이렉트(HTTP 상태 코드 302)인지 단언합니다:

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 삭제됨(HTTP 상태 코드 410)인지 단언합니다:

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정된 헤더와 값이 포함되어 있는지 단언합니다:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정된 헤더가 포함되어 있지 않은지 단언합니다:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 내부 서버 오류(HTTP 상태 코드 500)인지 단언합니다:

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 주어진 JSON 데이터가 포함되었음을 단언합니다:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환하여 JSON 내에 주어진 조각이 존재하는지 확인합니다. 다른 속성이 있어도 주어진 조각만 있으면 테스트는 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON 내 주어진 키에 배열이 있고, 그 배열의 항목 수가 특정 개수인지 단언합니다:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 주어진 JSON 데이터가 어디든 포함되어 있는지 단언합니다:

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

응답 JSON이 배열인지 단언합니다:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 단언합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 주어진 JSON 데이터가 포함되지 않았음을 단언합니다:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 정확히 일치하는 JSON 데이터가 포함되지 않았음을 단언합니다:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 주어진 키에 대한 JSON 유효성 검증 오류가 없음을 단언합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 더 일반적인 [assertValid](#assert-valid) 메서드를 사용하면 JSON으로 반환된 유효성 오류가 없고 세션에도 오류가 플래시되지 않았음을 단언할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답이 지정한 경로에 주어진 값을 포함하는지 단언합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 애플리케이션이 다음 JSON을 반환한다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음 단언으로 `user` 객체의 `name` 속성이 지정 값과 일치하는지 확인할 수 있습니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 주어진 JSON 경로가 포함되지 않았음을 단언합니다:

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 다음 JSON 응답이 있을 때:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user.email` 경로가 없다는 것을 다음과 같이 단언할 수 있습니다:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답 JSON이 주어진 구조를 포함하는지 단언합니다:

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 다음 데이터가 응답되어야 한다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

예상 구조는 다음과 같이 표현합니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때로는 응답 JSON이 객체 배열일 수 있습니다:

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

이때 `*` 문자를 사용하여 배열 내 모든 객체들이 다음 구조를 갖도록 단언합니다:

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

응답에 주어진 JSON 유효성 검증 오류가 포함되어 있는지 단언합니다. 이 메서드는 유효성 검증 오류가 JSON 구조로 반환되는 경우에 사용합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON으로 유효성 오류가 반환되거나 세션에 오류가 플래시된 모든 경우를 단언할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답에 주어진 키에 대한 JSON 유효성 검증 오류가 있는지 단언합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 허용되지 않은 메서드(HTTP 상태 코드 405)인지 단언합니다:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 영구 이동됨(HTTP 상태 코드 301)인지 단언합니다:

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답 헤더에 주어진 URI가 `Location` 헤더로 설정되어 있는지 단언합니다:

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 본문이 주어진 문자열과 일치하는지 단언합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 특정 HTTP 상태 코드이며 내용이 없음을 단언합니다:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트림된 응답인지 단언합니다:

```php
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트림된 응답 콘텐츠가 주어진 문자열과 일치하는지 단언합니다:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 찾을 수 없음(HTTP 상태 코드 404)인지 단언합니다:

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 성공(HTTP 상태 코드 200)인지 단언합니다:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 결제 필요(HTTP 상태 코드 402)인지 단언합니다:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 암호화되지 않은 쿠키가 포함되어 있는지 단언합니다:

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

응답이 이전 페이지로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리다이렉트되고 [세션에 주어진 에러가 있는지](#assert-session-has-errors) 단언합니다:

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

응답이 주어진 문자열이 포함된 URI로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 주어진 [명명된 라우트](/docs/12.x/routing#named-routes)로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 주어진 [서명된 라우트](/docs/12.x/urls#signed-urls)로 리다이렉트되는지 단언합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 요청 시간 초과(HTTP 상태 코드 408)인지 단언합니다:

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

응답에 주어진 문자열이 포함되어 있음을 단언합니다. 두 번째 인수로 `false`를 전달하면 이스케이프를 해제합니다:

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답에 주어진 문자열들이 순서대로 포함되어 있음을 단언합니다. 두 번째 인수로 `false`를 전달하면 이스케이프를 해제합니다:

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 본문 텍스트에 주어진 문자열이 포함되어 있음을 단언합니다. 두 번째 인수로 `false`를 전달하면 이스케이프를 해제할 수 있습니다. 본문은 `strip_tags` 함수로 처리된 후 단언합니다:

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 본문 텍스트에 주어진 문자열들이 순서대로 포함되어 있음을 단언합니다. 두 번째 인수로 `false`를 전달하면 이스케이프를 해제합니다. 본문은 `strip_tags` 함수로 처리됩니다:

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 오류(HTTP 상태 코드 >= 500, < 600)인지 단언합니다:

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 서비스 이용 불가(HTTP 상태 코드 503)인지 단언합니다:

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 주어진 데이터가 포함되어 있음을 단언합니다:

```php
$response->assertSessionHas($key, $value = null);
```

두 번째 인수로 클로저를 전달할 수 있으며, 클로저의 반환값이 `true`면 단언이 성공합니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션에 플래시된 입력 배열에 주어진 값이 포함되어 있음을 단언합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인수로 클로저를 전달할 수 있고, 반환값이 `true`이면 단언 성공입니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 주어진 키/값 쌍 배열이 모두 존재함을 단언합니다:

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 세션에 `name`과 `status`가 모두 특정 값으로 존재하는지 단언하려면:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 주어진 `$keys`에 대한 에러가 플래시되어 있음을 단언합니다. `$keys`가 연관 배열이면 각 필드별 특정 에러 메시지가 포함되어 있는지 단언합니다. 이는 유효성 검증 에러가 세션에 플래시되는 라우트 테스트 시 사용하세요:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, `name`과 `email` 필드에 대한 유효성 검증 에러 메시지가 세션에 포함되어 있음을 단언하려면:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

혹은 특정 필드에 특정 에러 메시지가 존재하는 경우:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON과 세션 모두에서 발생된 유효성 오류를 단언할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [에러 백(error bag)](/docs/12.x/validation#named-error-bags)에 속한 세션에 주어진 `$keys` 오류가 플래시되어 있음을 단언합니다. `$keys`가 연관 배열이면 각 필드별 특정 오류 메시지가 포함되어 있는지도 단언합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 오류가 전혀 없음을 단언합니다:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 주어진 키에 해당하는 유효성 검증 오류가 없음을 단언합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> [assertValid](#assert-valid) 메서드를 사용하면 JSON과 세션 양쪽 모두에 오류가 없음을 단언할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 주어진 키가 포함되어 있지 않음을 단언합니다:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 주어진 HTTP 상태 코드를 가지고 있음을 단언합니다:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공(HTTP 상태 코드 >= 200, < 300)인지 단언합니다:

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 너무 많은 요청(HTTP 상태 코드 429)인지 단언합니다:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 인증 필요(HTTP 상태 코드 401)인지 단언합니다:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 처리할 수 없음(HTTP 상태 코드 422)인지 단언합니다:

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 지원하지 않는 미디어 타입(HTTP 상태 코드 415)인지 단언합니다:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답에 해당 키에 대한 유효성 검증 오류가 없음을 단언합니다. 이 메서드는 유효성 오류가 JSON 구조나 세션에 플래시된 경우 모두에 대해 단언할 수 있습니다:

```php
// 유효성 오류가 없음을 단언...
$response->assertValid();

// 특정 키에 유효성 오류가 없음을 단언...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 해당 키에 대한 유효성 검증 오류가 있음을 단언합니다. 이 메서드는 JSON 구조에 오류가 반환되거나 세션에 플래시된 경우 모두 단언 가능합니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 필드가 특정 유효성 오류 메시지를 포함하는지 단언할 수도 있습니다. 메시지 전체 또는 일부분만 제공할 수 있습니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

특정 필드들만 유효성 오류가 있음을 단언하려면 `assertOnlyInvalid`을 사용합니다:

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 주어진 데이터가 포함되어 있음을 단언합니다:

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 전달하면 해당 뷰 데이터에 대해 검사할 수 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한 응답을 배열처럼 접근해 뷰 데이터를 편리하게 검사할 수 있습니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 주어진 여러 데이터가 포함되어 있음을 단언합니다:

```php
$response->assertViewHasAll(array $data);
```

키만 전달하면 해당 키들이 존재하는지를 단언하고:

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

키와 값 쌍을 전달하면 값까지 일치하는지 단언합니다:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

라우트가 주어진 뷰를 반환했음을 단언합니다:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 주어진 데이터 키가 포함되어 있지 않음을 단언합니다:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 단언

Laravel은 인증 관련 다양한 단언도 제공합니다. 이 메서드들은 `Illuminate\Testing\TestResponse` 인스턴스가 아닌 테스트 클래스 자신에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되어 있음을 단언합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았음을 단언합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되어 있음을 단언합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 단언 (Validation Assertions)

Laravel은 요청 데이터가 유효한지 또는 유효하지 않은지 확인하기 위해 두 가지 주요 유효성 검증 단언을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 주어진 키에 대한 유효성 검증 오류가 없음을 단언합니다. JSON 구조나 세션 플래시 오류 모두에 대해 단언 가능합니다:

```php
// 오차가 없음을 단언...
$response->assertValid();

// 특정 키에 오류가 없음을 단언...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 주어진 키에 대한 유효성 검증 오류가 있음을 단언합니다. JSON 구조나 세션 플래시 오류 모두 가능합니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 필드가 특정 오류 메시지를 포함하는지 단언할 수도 있습니다. 전체 또는 일부 메시지를 제공해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```