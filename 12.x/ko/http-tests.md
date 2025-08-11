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
- [사용 가능한 어설션](#available-assertions)
    - [응답 어설션](#response-assertions)
    - [인증 어설션](#authentication-assertions)
    - [유효성 검증 어설션](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 HTTP 요청을 보내고 그 응답을 점검할 수 있는 매우 직관적인 API를 제공합니다. 예를 들어, 아래에 정의된 기능(Feature) 테스트를 살펴보십시오.

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보냅니다. `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가져야 함을 검증합니다. 이 간단한 어설션 외에도, Laravel은 응답 헤더, 본문, JSON 구조 등 다양한 요소를 점검할 수 있는 여러 어설션을 포함합니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

애플리케이션에 요청을 보내기 위해서는 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 사용하면 됩니다. 이 메서드들은 실제 네트워크상에서 "진짜" HTTP 요청을 보내는 것이 아니라, 내부적으로 요청/응답 처리를 시뮬레이션합니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환하며, [여러 유용한 어설션](#available-assertions)을 제공하여 애플리케이션의 응답을 쉽게 점검할 수 있습니다.

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

일반적으로, 각 테스트는 단 하나의 요청만을 애플리케이션에 보내는 것이 좋습니다. 하나의 테스트 메서드 내에서 여러 요청을 보내면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의상 테스트를 실행할 때 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징 (Customizing Request Headers)

`withHeaders` 메서드를 사용하면 애플리케이션에 요청을 보내기 전에 요청 헤더를 커스터마이즈할 수 있습니다. 이 메서드는 요청에 원하는 커스텀 헤더를 추가할 수 있게 해줍니다.

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

`withCookie` 또는 `withCookies` 메서드를 사용하여 요청 전에 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 각각 인수로 받고, `withCookies`는 이름/값 쌍의 배열을 받습니다.

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

Laravel은 HTTP 테스트에서 세션 조작을 위한 다양한 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용해 세션 데이터를 원하는 배열로 미리 채워 둘 수 있습니다. 이 기능은 요청 전에 세션에 값을 저장할 때 유용하게 사용됩니다.

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

Laravel에서 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서, `actingAs` 헬퍼 메서드를 사용하면 지정한 사용자를 현재 사용자로 간편하게 인증할 수 있습니다. 예를 들어 [모델 팩토리](/docs/12.x/eloquent-factories)를 이용해 사용자를 생성하고 인증할 수 있습니다.

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

특정 guard를 사용해 사용자를 인증하고 싶다면, `actingAs` 메서드의 두 번째 인수로 guard 이름을 전달할 수 있습니다. 이렇게 지정한 guard는 해당 테스트 동안 기본 guard로 사용됩니다.

```php
$this->actingAs($user, 'web');
```

인증되지 않은(게스트) 상태로 요청을 보내려면 `actingAsGuest` 메서드를 사용할 수 있습니다.

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 응답 디버깅 (Debugging Responses)

테스트에서 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답의 내용을 점검하고 디버깅할 수 있습니다.

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

또는, 실행을 중단하면서 응답 정보를 출력해야 한다면 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용할 수 있습니다.

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

특정 예외가 발생하는지 테스트하고 싶을 때가 있습니다. 이럴 때는 `Exceptions` 파사드에서 예외 핸들러를 "faking" 할 수 있습니다. 예외 핸들러를 페이크로 만든 후, `assertReported` 및 `assertNotReported` 메서드를 사용하여 요청 중에 발생한 예외를 점검할 수 있습니다.

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

`assertNotReported`, `assertNothingReported` 메서드는 요청 중에 해당 예외가 발생하지 않았음을, 혹은 예외가 전혀 발생하지 않았음을 검증할 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

`withoutExceptionHandling` 메서드를 사용하면, 특정 요청에서 예외 처리를 완전히 비활성화할 수 있습니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 또는 사용 중인 라이브러리의 더 이상 지원되지 않는(deprecated) 기능이 애플리케이션에서 사용되고 있지 않은지 확인하려면, `withoutDeprecationHandling` 메서드를 사용할 수 있습니다. 이 설정을 사용하면, deprecation 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 특정 클로저가 지정한 타입의 예외를 던지는지 검증합니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

던져진 예외에 대해 추가적인 검증을 하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드는, 지정한 클로저 내의 코드에서 어떤 예외도 발생하지 않는지 검증합니다.

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel은 JSON API 및 그 응답을 위한 다양한 헬퍼도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드로 여러 HTTP 메서드의 JSON 요청을 손쉽게 보낼 수 있습니다. 이 메서드들로 데이터와 헤더도 쉽게 함께 전달할 수 있습니다. 예를 들어 `/api/user`에 `POST` 요청을 보내고, 예상하는 JSON 데이터가 반환되는지 다음과 같이 테스트할 수 있습니다.

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

또한, JSON 응답 데이터를 배열 변수처럼 접근할 수 있으므로, 반환값을 편리하게 점검할 수 있습니다.

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여, 전달된 배열이 애플리케이션에서 반환된 JSON 응답 내부에 존재하는지 확인합니다. JSON 내에 다른 속성이 더 있더라도, 주어진 JSON 조각이 있으면 테스트를 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 검증 (Asserting Exact JSON Matches)

앞서 설명한 `assertJson` 메서드는 JSON 조각이 응답에 존재함을 확인합니다. 만약 응답 데이터가 애플리케이션이 반환한 JSON과 **정확히** 일치하는지를 검증하려면, `assertExactJson` 메서드를 사용하세요.

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

특정 경로(path)에 기대하는 데이터가 포함되어 있는지 확인하려면 `assertJsonPath` 메서드를 사용하세요.

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

`assertJsonPath`는 클로저도 인수로 받을 수 있어, 동적으로 해당 경로의 값에 대해 검증 로직을 작성할 수 있습니다.

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트 (Fluent JSON Testing)

Laravel은 JSON 응답을 좀 더 자연스럽고 체계적으로 테스트할 수 있도록 도와주는 플루언트(fluent) JSON 테스트 방식을 제공합니다. 가장 먼저, `assertJson` 메서드에 클로저를 전달하면, Laravel이 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 전달합니다. 이 인스턴스를 사용해 JSON 객체 속성 별 검증을 수행할 수 있습니다. 예를 들어, `where` 메서드로 특정 속성 값을, `missing` 메서드로 특정 속성이 없는지 검증하고, 마지막엔 `etc` 메서드를 활용할 수 있습니다.

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

위 예시에서 마지막에 `etc` 메서드를 호출하는 것을 볼 수 있습니다. 이 메서드는 해당 JSON 객체에 명시한 속성 외의 다른 속성들이 존재할 수 있음을 Laravel에 알려줍니다. 만약 `etc`를 사용하지 않으면, 어설션 대상 외의 속성이 JSON 객체에 존재할 경우 테스트가 실패합니다.

이 방식은 민감 정보가 JSON으로 노출되지 않도록, 해당 속성에 대한 어설션을 명시적으로 작성하거나, `etc`를 명시해 추가 속성 허용을 의도적으로 선택하도록 유도합니다.

단, 어설션 체인에 `etc`를 사용하지 않는다고 해서, JSON 객체 "내부의 배열"에 추가 속성이 없다는 보장은 할 수 없습니다. `etc`는 호출된 해당 계층(nesting level)에만 적용됩니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### JSON 속성 존재 / 부재 어설션

특정 속성이 존재하는지, 혹은 없는지 어설션하려면 `has` 및 `missing` 메서드를 각각 사용합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한, 여러 속성을 한 번에 점검하려면 `hasAll`, `missingAll`을 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

리스트 중 하나 이상의 속성만 있으면 되는 경우에는 `hasAny`를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어설션

라우트가 여러 항목을 포함하는 JSON 컬렉션(예: 여러 사용자)을 반환할 경우가 많습니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

이럴 때는 플루언트 JSON 객체의 `has` 메서드로 컬렉션 내 항목 수를 검증할 수 있습니다. 이어서, `first` 메서드를 사용해 컬렉션의 첫 번째 객체에 대해 어설션 체인을 연결할 수 있습니다.

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
#### JSON 컬렉션 어설션 범위 지정

때로는 이름이 지정된 키에 할당된 JSON 컬렉션이 반환되기도 합니다.

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이 때 `has` 메서드를 사용해 컬렉션의 항목 수 및 범위를 지정할 수 있습니다. 또한, `has`의 세 번째 인수로 클로저를 넘기면 어설션 범위를 지정된 항목에 한정할 수 있습니다.

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
#### JSON 타입 어설션

JSON 응답의 속성 값이 특정 타입인지만 검사하고 싶을 때는, `whereType` 및 `whereAllType` 메서드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`whereType`에는 복수의 타입을 `|` 문자 또는 타입 배열로 넘길 수 있습니다. 응답 값의 타입이 나열된 타입 중 하나만 일치해도 통과합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType` 및 `whereAllType` 메서드는 `string`, `integer`, `double`, `boolean`, `array`, `null` 타입을 인식합니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 사용하면 테스트용 가짜 파일이나 이미지를 손쉽게 생성할 수 있습니다. 여기에 `Storage` 파사드의 `fake` 기능을 결합하면 파일 업로드 테스트가 매우 간단해집니다. 아래 예시처럼 아바타 업로드 폼을 손쉽게 테스트할 수 있습니다.

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

특정 파일이 존재하지 않는지 어설션하려면, `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다.

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이즈

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때 이미지의 너비, 높이, 크기(킬로바이트)도 지정하여 애플리케이션의 유효성 검증을 잘 테스트할 수 있습니다.

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도, `create` 메서드를 활용하면 임의의 파일 형태를 만들 수 있습니다.

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, 파일의 MIME 타입을 명시적으로 설정할 수도 있습니다.

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

Laravel은 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고도 뷰(View)를 직접 렌더링하여 테스트할 수 있습니다. 이를 위해 테스트 내에서 `view` 메서드를 사용할 수 있습니다. 이 메서드는 뷰 이름과(필요 시) 데이터 배열을 받아, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 객체를 통해 뷰 내용을 검증하는 다양한 메서드를 사용할 수 있습니다.

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

`TestView` 클래스에서는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 등의 어설션 메서드를 제공합니다.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 원시 렌더링 결과를 얻을 수도 있습니다.

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유하기

일부 뷰는 [Laravel의 전역 에러 백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 저장된 에러 정보를 필요로 할 수 있습니다. 에러 메시지로 에러 백을 미리 채우려면 `withViewErrors` 메서드를 사용하세요.

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링 (Rendering Blade and Components)

필요하다면, `blade` 메서드로 [Blade](/docs/12.x/blade)의 원시 템플릿 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로, 이 메서드는 `Illuminate\Testing\TestView` 인스턴스를 반환합니다.

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/12.x/blade#components)를 평가하고 렌더링하려면, `component` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다.

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

<a name="response-assertions"></a>
### 응답 어설션 (Response Assertions)

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 사용할 수 있는 다양한 맞춤형 어설션 메서드를 제공합니다. 이 어설션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드로 반환된 응답에서 사용할 수 있습니다.

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

응답이 HTTP 상태 코드 202(accepted)임을 검증합니다.

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 HTTP 상태 코드 400(bad request)임을 검증합니다.

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 오류(HTTP 상태 코드 400~499)임을 검증합니다.

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 HTTP 상태 코드 409(conflict)임을 검증합니다.

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정된 쿠키가 포함되어 있는지 검증합니다.

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정된 쿠키가 포함되어 있고, 해당 쿠키가 만료되었는지 검증합니다.

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정된 쿠키가 포함되어 있고, 해당 쿠키가 만료되지 않았는지 검증합니다.

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정된 쿠키가 포함되어 있지 않은지 검증합니다.

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 HTTP 상태 코드 201(created)임을 검증합니다.

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 지정한 문자열이 포함되어 있지 않은지 검증합니다. 두 번째 인수로 `false`를 전달하면 자동 이스케이프를 비활성화할 수 있습니다.

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트 내에 지정한 문자열이 포함되어 있지 않은지 검증합니다. 두 번째 인수로 `false`를 전달하면 자동 이스케이프를 비활성화할 수 있습니다. 검증 전에 응답 내용에 `strip_tags`를 적용합니다.

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"임을 검증합니다. 대부분은 해당 라우트가 `Response::download`, `BinaryFileResponse`, 또는 `Storage::download` 응답을 반환한 경우입니다.

```php
$response->assertDownload();
```

다운로드 파일의 이름까지 일치하는지 어설션할 수도 있습니다.

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 지정한 JSON 데이터와 정확히 일치하는지 검증합니다.

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 지정한 JSON 구조와 완전히 일치하는지 검증합니다.

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)의 더욱 엄격한 버전입니다. 기대한 JSON 구조에 명시하지 않은 키가 응답에 포함되어 있다면 테스트가 실패합니다.

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 HTTP 상태 코드 403(forbidden)임을 검증합니다.

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답이 HTTP 상태 코드 302(found)임을 검증합니다.

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답이 HTTP 상태 코드 410(gone)임을 검증합니다.

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정된 헤더(및 값)가 존재하는지 검증합니다.

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정한 헤더가 존재하지 않는지 검증합니다.

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답이 HTTP 500(Internal Server Error) 상태 코드임을 검증합니다.

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답에 지정한 JSON 데이터가 포함되어 있는지 검증합니다.

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환하여, 전달된 배열이 응답 JSON 내에 포함되어 있는지만 점검합니다. 응답에 다른 속성이 포함되어 있어도, 해당 조각이 있으면 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

지정한 키에 대한 응답 JSON에서 배열의 항목 개수가 기대한 개수와 일치하는지 어설션합니다.

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답 어디에든지 지정한 JSON 조각이 포함되어 있는지 검증합니다.

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

응답 JSON이 배열인지 검증합니다.

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 검증합니다.

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정된 JSON 데이터가 **포함되어 있지 않은지** 검증합니다.

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 지정한 JSON 데이터가 **정확히** 일치해서 포함되어 있지 않은지 검증합니다.

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 지정한 키에 대한 JSON 유효성 검증 에러가 없는지 검증합니다.

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 좀 더 일반적인 [assertValid](#assert-valid) 메서드를 사용하면, 응답에 유효성 검증 에러가 **JSON**으로 반환되지 않았으며 **세션에도 에러가 저장되어 있지 않은** 상태임을 검증할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답의 특정 경로에 지정한 값이 있는지 검증합니다.

```php
$response->assertJsonPath($path, $expectedValue);
```

예시 : 아래 JSON 응답에서

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user.name` 속성이 지정한 값과 일치하는지 어설션할 수 있습니다.

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 특정 경로가 **존재하지 않는지** 검증합니다.

```php
$response->assertJsonMissingPath($path);
```

예시 : 위 JSON 응답에서 `user.email` 속성이 없는지 검증합니다.

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답의 JSON 구조가 기대하는 구조와 일치하는지 검증합니다.

```php
$response->assertJsonStructure(array $structure);
```

예시 : JSON 응답이 아래와 같고

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음처럼 구조를 어설션할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

애플리케이션에서 반환하는 JSON 응답이 객체 배열인 경우도 있습니다.

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

이 때는 `*`를 사용하여 배열 내부의 모든 항목의 구조를 점검할 수 있습니다.

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

응답에 지정한 키에 대한 JSON 유효성 검증 에러가 있는지 검증합니다. 이 메서드는 검증 에러가 JSON 구조로 반환될 때 어설션에 사용합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 좀 더 포괄적인 [assertInvalid](#assert-invalid) 메서드는 에러가 JSON 혹은 세션에 플래시된 경우 모두 검증할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

지정한 키에 하나라도 JSON 유효성 검증 에러가 존재하는지 검증합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답이 HTTP 405(Method Not Allowed) 상태 코드임을 검증합니다.

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 HTTP 301(Moved Permanently) 상태 코드임을 검증합니다.

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

응답의 `Location` 헤더가 지정된 URI와 같은지 검증합니다.

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 내용이 주어진 문자열과 정확히 일치하는지 검증합니다.

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정한 HTTP 상태 코드를 가지며, 본문이 없는지 검증합니다.

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트림(stream) 응답인지 검증합니다.

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

스트림 응답의 내용이 기대한 값과 동일한지 검증합니다.

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 HTTP 404(Not Found) 상태 코드임을 검증합니다.

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 HTTP 200 상태 코드임을 검증합니다.

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 HTTP 402(Payment Required) 상태 코드임을 검증합니다.

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답이 지정한 암호화되지 않은 쿠키를 포함하고 있는지 검증합니다.

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정한 URI로의 리다이렉트인지 검증합니다.

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로의 리다이렉트인지 검증합니다.

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리다이렉트되며, [세션에 지정한 에러가 포함](#assert-session-has-errors)되어 있는지 검증합니다.

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

응답이 이전 페이지로 리다이렉트되며, 세션에 에러 메시지가 없는지 검증합니다.

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 주어진 문자열을 포함하는 URI로 리다이렉트되고 있는지 확인합니다.

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 지정한 [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트되는지 검증합니다.

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 지정한 [서명된 라우트](/docs/12.x/urls#signed-urls)로 리다이렉트되는지 검증합니다.

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 HTTP 408(Request Timeout) 상태 코드임을 검증합니다.

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

응답에 지정한 문자열이 포함되어 있는지 검증합니다. 두 번째 인수에 `false`를 넘기면 자동 이스케이프가 적용되지 않습니다.

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답 내에 지정한 여러 문자열이 해당 순서대로 포함되어 있는지 검증합니다. 두 번째 인수에 `false`를 넘기면 자동 이스케이프가 적용되지 않습니다.

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 텍스트에 지정한 문자열이 포함되어 있는지 검증합니다. 두 번째 인수에 `false`를 넘기면 자동 이스케이프가 적용되지 않습니다. 응답 내용이 `strip_tags` 함수를 거친 후 어설션이 수행됩니다.

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에서 지정한 문자열들이 해당 순서대로 포함되어 있는지 검증합니다. 두 번째 인수에 `false`를 넘기면 자동 이스케이프가 적용되지 않습니다. 응답 내용이 `strip_tags` 함수를 거친 후 어설션이 수행됩니다.

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 오류(HTTP 500~599) 상태 코드인지 검증합니다.

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 HTTP 503(Service Unavailable) 상태 코드임을 검증합니다.

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션이 지정한 데이터를 포함하고 있는지 검증합니다.

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면, 두 번째 인수에 클로저를 넘겨 해당 세션 데이터에 대한 추가 점검을 할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과합니다.

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션에 [플래시된 입력 데이터](/docs/12.x/responses#redirecting-with-flashed-session-data)가 포함되어 있는지 확인합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인수로 클로저를 넘기면, 해당 데이터에 대해 추가 어설션을 할 수 있습니다.

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션이 지정한 키/값 전체 쌍을 포함하는지 검증합니다.

```php
$response->assertSessionHasAll(array $data);
```

예시 : 세션에 `name`, `status` 키가 기대하는 값으로 존재하는지 어설션

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 지정한 `$keys`에 대한 에러가 있는지 검증합니다. `$keys`가 연관 배열이면, 세션에 특정 필드(키)에 대해 지정한 에러 메시지(값)가 있는지 확인합니다. 검증 에러가 JSON이 아닌 세션에 플래시되는 라우트 테스트에 이 메서드를 사용합니다.

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예: `name`, `email` 필드에 대한 유효성 검증 에러 메시지가 세션에 플래시 됐는지 확인

```php
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드에 특정 에러 메시지가 있는지도 어설션할 수 있습니다.

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 좀 더 일반적인 [assertInvalid](#assert-invalid) 메서드는, 응답에 유효성 검증 에러가 JSON으로 반환되거나 세션에 플래시된 경우 모두 어설션할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

지정한 [에러 백](/docs/12.x/validation#named-error-bags) 내에서 `$keys`에 대한 에러가 있는지 검증합니다. `$keys`가 연관 배열일 때, 각 키에 명시한 값(에러 메시지)이 있는지도 확인합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 에러가 하나도 없는지 검증합니다.

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 지정한 키에 대한 유효성 검증 에러가 없는지 검증합니다.

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 더 일반적인 [assertValid](#assert-valid) 메서드는 응답에 유효성 검증 에러가 JSON으로 반환되지 않았으며, 세션에도 플래시되지 않은지까지 어설션할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정한 키가 **없는지** 검증합니다.

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 지정한 HTTP 상태 코드임을 검증합니다.

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공(HTTP 200~299) 상태 코드임을 검증합니다.

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 HTTP 429(Too Many Requests) 상태 코드임을 검증합니다.

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 HTTP 401(Unauthorized) 상태 코드임을 검증합니다.

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 HTTP 422(Unprocessable Entity) 상태 코드임을 검증합니다.

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답이 HTTP 415(Unsupported Media Type) 상태 코드임을 검증합니다.

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

응답에 지정된 키에 대해 유효성 검증 에러가 없는지 확인합니다. JSON 구조로 반환되거나, 세션에 플래시된 에러 모두 검증할 수 있습니다.

```php
// 아무 에러도 없는지 검증...
$response->assertValid();

// 지정한 키의 에러가 없는지 검증...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

응답에 지정된 키에 대해 유효성 검증 에러가 있는지 확인합니다. JSON, 세션 모두 검사합니다.

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 지정한 에러 메시지를 가지는지도 검증할 수 있습니다. 전체 메시지 또는 일부만 일치해도 통과합니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

만약 명시한 필드만 에러가 있는지 확인하려면, `assertOnlyInvalid` 메서드를 사용할 수 있습니다.

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 지정한 데이터를 포함하는지 검증합니다.

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 넘기면, 해당 데이터에 대해 상세한 점검을 할 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한 응답의 뷰 데이터에 배열처럼 접근할 수도 있습니다.

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 지정한 데이터 목록이 모두 있는지 확인합니다.

```php
$response->assertViewHasAll(array $data);
```

예: 데이터 존재만 체크, 값까지 체크

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

혹은, 데이터가 특정 값인지도 함께 어설션할 수 있습니다.

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

지정한 뷰가 이 응답에서 반환됐는지 검증합니다.

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰에 지정한 데이터 키가 **포함되지 않았는지** 검증합니다.

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어설션 (Authentication Assertions)

Laravel은 애플리케이션의 Feature 테스트 내에서 사용할 수 있는 다양한 인증 관련 어설션도 제공합니다. 이 메서드들은 `get`, `post` 등이 반환하는 `Illuminate\Testing\TestResponse` 인스턴스가 아닌, 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

유저가 인증된 상태임을 검증합니다.

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

유저가 비인증(게스트) 상태임을 검증합니다.

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 유저가 인증된 상태임을 검증합니다.

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증 어설션 (Validation Assertions)

Laravel은 요청에서 전달된 데이터가 유효한지, 또는 유효하지 않았는지 검증하는 두 가지 주요 어설션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답에 지정한 키에 대해 유효성 검증 에러가 없는지 점검합니다. JSON 구조로 반환되거나, 세션에 플래시된 에러 모두 체크할 수 있습니다.

```php
// 아무 에러도 없는지 검증...
$response->assertValid();

// 지정한 키의 에러가 없는지 검증...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답에 지정한 키에 대해 유효성 검증 에러가 있는지 점검합니다. JSON, 세션 모두 검사합니다.

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 지정한 에러 메시지를 가지는지도 어설션할 수 있습니다. 전체 메시지 혹은 일부 일치만으로도 가능합니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
