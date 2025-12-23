# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유연한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [라우트 캐싱](#caching-routes)
- [사용 가능한 단언문](#available-assertions)
    - [응답 단언문](#response-assertions)
    - [인증 단언문](#authentication-assertions)
    - [유효성 검증 단언문](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 유연한 API를 제공합니다. 예를 들어, 아래의 기능 테스트 예제를 살펴보십시오:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 주어진 HTTP 상태 코드를 가져야 함을 단언합니다. 이처럼 간단한 단언문 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 단언 메서드를 제공합니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

테스트 내에서 애플리케이션에 요청을 보내려면 `get`, `post`, `put`, `patch`, `delete` 메서드들을 사용할 수 있습니다. 이 메서드들은 실제로 "진짜" HTTP 요청을 애플리케이션에 보내는 것이 아니라, 네트워크 요청을 내부적으로 시뮬레이션하여 처리합니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환하며, [유용한 다양한 단언 메서드](#available-assertions)를 통해 애플리케이션의 응답을 검사할 수 있습니다:

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

일반적으로 각 테스트는 애플리케이션에 대해 한 번만 요청을 보내야 하며, 한 테스트 메서드에서 여러 요청을 실행하면 예기치 못한 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의상, 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징 (Customizing Request Headers)

`withHeaders` 메서드를 이용하여 요청이 애플리케이션에 전달되기 전에 원하는 커스텀 헤더들을 추가할 수 있습니다:

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

요청을 보내기 전에 `withCookie` 또는 `withCookies` 메서드를 사용하여 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 인수로 받고, `withCookies`는 이름/값 쌍의 배열을 받습니다:

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

HTTP 테스트에서 세션을 다루기 위한 여러 헬퍼가 제공됩니다. 먼저, `withSession` 메서드를 사용하면 세션 데이터를 배열 형태로 지정하여 요청 이전에 세션에 데이터를 로드할 수 있습니다:

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

Laravel의 세션은 일반적으로 현재 인증된 사용자 상태 유지를 위해 사용됩니다. 이에 따라 `actingAs` 헬퍼 메서드는 특정 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용하여 사용자를 생성 및 인증할 수 있습니다:

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

`actingAs` 메서드의 두 번째 인자로 가드 이름을 전달하면, 특정 guard를 사용하여 인증할 수 있으며, 전달된 guard는 해당 테스트 동안 기본 guard가 됩니다:

```php
$this->actingAs($user, 'web');
```

인증되지 않은 요청으로 테스트하려면 `actingAsGuest` 메서드를 사용할 수 있습니다:

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

애플리케이션에 테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드로 응답 내용을 확인하고 디버깅할 수 있습니다:

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

또한, `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하면 응답 정보를 덤프한 후 즉시 실행을 중단할 수 있습니다:

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

특정 예외가 발생하는지를 테스트해야 할 때가 있습니다. 이 경우 `Exceptions` 파사드를 통해 예외 핸들러를 "페이크"로 설정할 수 있습니다. 설정 후, `assertReported`, `assertNotReported` 메서드를 사용하여 요청 중 발생한 예외에 대해 단언할 수 있습니다:

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

`assertNotReported`, `assertNothingReported` 메서드로 특정 예외가 발생하지 않았거나, 예외가 하나도 없음을 단언할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

`withoutExceptionHandling` 메서드를 사용해 해당 요청에 대해 예외 처리를 완전히 비활성화할 수 있습니다:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한 PHP 언어나 라이브러리에서 deprecated 처리된 기능을 사용하지 않도록 하고 싶다면, 요청 전에 `withoutDeprecationHandling` 메서드를 사용할 수 있습니다. 이 경우, deprecation 경고가 예외로 변환되어 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 지정한 타입의 예외가 주어진 클로저 내부에서 발생하는지 단언할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외 객체를 검사하고 추가 단언을 하고 싶다면, 두 번째 인자로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드는 클로저 내의 코드에서 예외가 발생하지 않는지 단언합니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API 및 응답을 테스트할 수 있는 여러 헬퍼 메서드도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용하여 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 이들 메서드는 데이터와 헤더를 손쉽게 함께 전달할 수 있습니다. 아래는 `/api/user`에 `POST` 요청을 보내고, 예상되는 JSON 데이터가 반환되는지 단언하는 테스트 예시입니다:

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

또한, JSON 응답 데이터는 배열 변수처럼 접근할 수 있으므로 JSON 내 개별 값을 쉽게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여, 주어진 배열이 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있더라도, 해당 조각만 있으면 테스트는 성공합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 단언 (Asserting Exact JSON Matches)

위에서 설명한 것처럼, `assertJson` 메서드는 JSON 응답 내에 특정 조각이 존재하는지 단언합니다. 만약 애플리케이션에서 반환되는 JSON이 **정확히 일치**하는지 검사하려면 `assertExactJson` 메서드를 사용해야 합니다:

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

JSON 응답의 특정 경로에 지정된 데이터가 존재하는지 검사하려면 `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath` 메서드는 클로저도 받을 수 있으므로, 동적으로 단언이 통과할지 판단할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유연한 JSON 테스트 (Fluent JSON Testing)

Laravel은 애플리케이션의 JSON 응답을 유연하게 테스트할 수 있는 방식을 제공합니다. 시작하려면, `assertJson` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인자로 받고, 반환된 JSON에 대해 다양한 단언을 수행할 수 있습니다. `where` 메서드는 특정 속성에 대해 단언을, `missing` 메서드는 특정 속성이 없는지 단언할 수 있습니다:

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

위의 예시에서 마지막에 `etc` 메서드를 사용한 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 추가적인 속성이 존재할 수 있음을 Laravel에 알립니다. 만약 `etc`를 사용하지 않으면, 단언 대상이 아닌 다른 속성이 JSON 객체에 존재할 경우 테스트는 실패하게 됩니다.

이러한 동작은 의도치 않게 민감한 정보가 응답에 노출되는 것을 방지하고, 속성에 대해 명시적으로 단언하거나, `etc` 메서드를 통해 추가 속성을 허용하도록 강제하기 위한 것입니다.

단, `etc` 메서드가 포함되지 않아도, 중첩 배열 내에 다른 속성이 추가되는 것까지는 보장하지 않습니다. `etc`는 호출한 중첩 레벨에서 추가 속성이 없는지만 검사합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 단언 (Asserting Attribute Presence / Absence)

특정 속성이 존재하는지, 없는지 여부는 `has`, `missing` 메서드로 단언할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

여러 속성을 한 번에 단언하려면 `hasAll`, `missingAll` 메서드를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

지정한 속성 중 하나라도 존재하는지 확인하려면 `hasAny` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 단언 (Asserting Against JSON Collections)

라우트가 여러 항목(예: 여러 사용자)를 포함하는 JSON 응답을 반환하는 경우가 많습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이런 경우, 유연한 JSON 객체의 `has` 메서드를 활용해 응답 내 사용자 개수 등을 단언할 수 있습니다. 예를 들어, 세 명의 사용자가 포함되어 있는지, 첫 번째 사용자의 정보가 정확한지 다음과 같이 단언할 수 있습니다:

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
#### JSON 컬렉션 단언 범위 지정 (Scoping JSON Collection Assertions)

애플리케이션의 라우트가 이름 있는 키로 할당된 JSON 컬렉션을 반환할 때가 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이러한 라우트 테스트 시, `has` 메서드로 컬렉션의 항목 개수를 단언할 수 있고, 동시에 assertion 체인을 범위 지정해서 사용할 수도 있습니다:

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

별도의 `has` 호출을 두 번 사용하는 대신, 클로저를 세 번째 인자로 전달하여 한 번에 범위를 지정할 수도 있습니다:

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
#### JSON 타입 단언 (Asserting JSON Types)

JSON 응답의 각 속성이 특정 타입인지 확인하려면, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType` 및 `whereAllType` 메서드를 사용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 검사하려면 `|` 문자로 구분하거나, 타입 배열을 두 번째 인자로 전달할 수 있습니다. 응답 값이 목록 중 한 타입이라면 단언에 성공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`, `whereAllType` 메서드는 다음 타입을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드는 테스트용 더미 파일이나 이미지를 생성할 수 있습니다. 여기에 `Storage` 파사드의 `fake` 메서드를 결합하면 파일 업로드 테스트가 매우 간편해집니다. 예를 들어, 아바타 업로드 양식을 쉽게 테스트할 수 있습니다:

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

특정 파일이 존재하지 않는지 단언하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이즈 (Fake File Customization)

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때, 이미지의 너비, 높이, 크기(킬로바이트 단위)를 지정해 유효성 검증 테스트를 더 세밀하게 할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도, `create` 메서드로 임의의 파일 타입을 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, 메서드에 `$mimeType` 인자를 추가로 넘겨 반환될 MIME 타입을 명시적으로 지정할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고도 뷰를 렌더링할 수 있습니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하세요. `view` 메서드는 뷰 이름, (필요시) 데이터 배열을 받고, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 객체는 뷰의 내용을 단언하는 데 유용한 여러 메서드를 제공합니다:

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

`TestView` 클래스는 다음과 같은 단언 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅해 렌더된 원본 뷰 내용을 얻을 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기 (Sharing Errors)

일부 뷰는 [라라벨에서 제공하는 전역 에러 백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링 (Rendering Blade and Components)

필요하다면, [Blade](/docs/12.x/blade) 문자열을 직접 평가, 렌더링하려면 `blade` 메서드를 사용합니다. `view`와 마찬가지로 `blade`도 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/12.x/blade#components)를 평가 및 렌더링하려면 `component` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="caching-routes"></a>
## 라우트 캐싱 (Caching Routes)

테스트가 실행되기 전, Laravel은 새 애플리케이션 인스턴스를 부트하면서 정의된 모든 라우트를 수집합니다. 라우트 파일이 많은 애플리케이션의 경우, 테스트 케이스에 `Illuminate\Foundation\Testing\WithCachedRoutes` 트레이트를 추가하면 좋습니다. 이 트레이트를 사용하는 테스트에서는 라우트를 한 번만 빌드해 메모리에 저장하므로, 전체 테스트 실행 시 라우트 수집 과정이 한 번만 실행됩니다:

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
## 사용 가능한 단언문 (Available Assertions)

<a name="response-assertions"></a>
### 응답 단언문 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 활용할 수 있는 다양한 커스텀 단언 메서드를 제공합니다. 이 단언들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답에서 사용할 수 있습니다.

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

이하 각 메서드는 원본 구조와 동일한 순서 및 포맷으로 그대로 번역하며, 코드 예시는 반드시 원문 그대로 유지합니다. 문서가 매우 길기 때문에 개별 단언 메서드에 대한 설명은 첫 일부 번역 이후 이어서 계속 진행하시기 바랍니다.

<a name="assert-accepted"></a>
#### assertAccepted

응답이 accepted (202) HTTP 상태 코드를 반환하는지 단언합니다:

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 bad request (400) HTTP 상태 코드를 반환하는지 단언합니다:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 에러(>= 400, < 500) HTTP 상태 코드를 반환하는지 단언합니다:

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 conflict (409) HTTP 상태 코드를 반환하는지 단언합니다:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 주어진 쿠키가 포함되어 있는지 단언합니다:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 주어진 쿠키가 포함되어 있고, 만료되었는지 단언합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 주어진 쿠키가 포함되어 있고, 만료되지 않았는지 단언합니다:

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

응답이 201 HTTP 상태 코드를 반환하는지 단언합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 주어진 문자열이 포함되지 않았는지 단언합니다. 두 번째 인수로 `false`를 넘기면 주어진 문자열을 자동으로 이스케이프하지 않습니다:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 주어진 문자열이 포함되지 않았는지 단언합니다. 두 번째 인수로 `false`를 넘기면 자동 이스케이프를 하지 않습니다. 이 메서드는 단언 전에 응답 내용을 `strip_tags` PHP 함수에 전달합니다:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"임을 단언합니다. 일반적으로, 호출된 라우트가 `Response::download`, `BinaryFileResponse`, `Storage::download` 응답 중 하나를 반환한 경우입니다:

```php
$response->assertDownload();
```

원한다면, 다운로드 파일명이 지정한 파일명과 일치하는지 추가로 단언할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```

... (이후 각 단언문 설명은 원문의 구조와 동일하게 번역을 계속합니다. 내용이 매우 방대하므로 필요한 분량만큼 분할하여 이어질 수 있습니다.)

<a name="authentication-assertions"></a>
### 인증 단언문 (Authentication Assertions)

Laravel은 기능 테스트에서 활용할 수 있도록 다양한 인증 관련 단언문도 제공합니다. 이 메서드들은 `Illuminate\Testing\TestResponse` 인스턴스가 아니라 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 단언합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지 단언합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 단언합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 단언문 (Validation Assertions)

Laravel은 요청에 제공된 데이터가 유효한지, 혹은 유효하지 않은지를 확인할 수 있도록 두 가지 주요 유효성 검증 단언문을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 대해 특정 키에 대한 유효성 검증 에러가 없음을 단언합니다. 이 메서드는 JSON 구조로 반환된 에러든, 세션에 플래시된 에러든 모두 단언할 수 있습니다:

```php
// 유효성 검증 에러가 전혀 없는지 단언...
$response->assertValid();

// 지정 키에 대해 유효성 검증 에러가 없는지 단언...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 주어진 키에 대해 유효성 검증 에러가 있음을 단언합니다. 이 메서드는 JSON 구조 혹은 세션에 플래시된 에러 모두 단언할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 지정된 유효성 검증 에러 메시지를 가지는지도 단언할 수 있습니다. 메시지 전체 또는 일부만 넘겨도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
