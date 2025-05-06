# HTTP 테스트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이즈](#customizing-request-headers)
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
    - [검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사할 수 있는 매우 플루언트한 API를 제공합니다. 예를 들어, 아래의 기능 테스트를 살펴보세요:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 반환된 응답의 HTTP 상태 코드가 지정한 값과 일치하는지 확인합니다. 이 간단한 어서션 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, 또는 `delete` 메서드를 사용할 수 있습니다. 이 메서드들은 실제 "진짜" HTTP 요청을 보내는 것이 아니라, 내부적으로 네트워크 요청을 시뮬레이션합니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, [다양한 유용한 어서션](#available-assertions)을 지원하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 객체를 통해 애플리케이션의 응답을 쉽게 검사할 수 있습니다:

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

일반적으로 각 테스트는 애플리케이션에 한 번만 요청을 보내야 합니다. 하나의 테스트 메서드 내에서 여러 요청을 보낼 경우 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해, 테스트를 실행할 때는 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이즈

`withHeaders` 메서드를 사용하여 요청이 애플리케이션으로 전송되기 전에 헤더를 커스터마이즈할 수 있습니다. 이 메서드를 이용해 원하는 커스텀 헤더를 추가할 수 있습니다:

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

요청을 보낼 때 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie` 메서드는 쿠키 이름과 값을 각각 인자로 받고, `withCookies` 메서드는 이름/값 쌍의 배열을 인자로 받습니다:

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

Laravel은 HTTP 테스트 중에 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용해 원하는 배열로 세션 데이터를 설정할 수 있습니다. 이는 요청을 보내기 전에 세션에 데이터를 미리 저장할 때 유용합니다:

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

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 쓰입니다. 따라서, `actingAs` 헬퍼 메서드는 주어진 사용자를 인증된 사용자로 설정하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

`actingAs` 메서드에 두 번째 인자(가드 이름)를 전달하여 사용자의 인증에 사용할 가드를 지정할 수도 있습니다. 지정한 가드는 해당 테스트 진행 중 기본 가드로 사용됩니다.

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 후 응답을 검사 및 디버깅할 때, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용할 수 있습니다:

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

또는, `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하여 응답 정보를 덤프한 뒤 실행을 즉시 중단할 수도 있습니다:

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

애플리케이션이 특정 예외를 발생시키는지 테스트할 필요가 있을 때가 있습니다. 이를 위해 `Exceptions` 파사드를 이용해 예외 핸들러를 "가짜"로 만들 수 있습니다. 예외 핸들러가 가짜로 설정되면, `assertReported`와 `assertNotReported` 메서드를 사용해 요청 중 발생한 예외에 대한 어서션을 할 수 있습니다:

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // 예외가 발생했는지 확인...
    Exceptions::assertReported(InvalidOrderException::class);

    // 예외 인스턴스에 대한 추가 어서션...
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

        // 예외 인스턴스에 대한 추가 어서션...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

`assertNotReported`와 `assertNothingReported` 메서드를 사용하면, 특정 예외가 발생하지 않았거나, 어떤 예외도 발생하지 않았는지 확인할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리 자체를 완전히 비활성화하려면, 요청을 보내기 전에 `withoutExceptionHandling` 메서드를 호출하세요:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, 애플리케이션이 PHP나 사용 라이브러리에서 더 이상 지원하지 않는 기능(Deprecated Feature)을 사용하지 않았는지 확인하고 싶다면, 요청 전 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이 설정이 비활성화되면, deprecated 경고가 예외로 변환되어 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 주어진 클로저 내 코드가 특정 타입의 예외를 발생시키는지 확인합니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외 인스턴스를 검사하거나 어서션을 하고 싶을 때는 두 번째 인자로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드는 주어진 클로저 내 코드에서 예외가 발생하지 않았는지 확인합니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel에는 JSON API와 응답을 테스트하기 위한 다양한 헬퍼가 있습니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 이용해 여러 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 이 메서드들에는 데이터와 헤더를 쉽게 전달할 수 있습니다. 예를 들어 `/api/user`로 `POST` 요청을 보내고 예상한 JSON 응답이 전송됐는지 테스트해보겠습니다:

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

또한 JSON 응답 데이터는 배열 변수를 통해 바로 접근할 수 있어서, 개별 값을 쉽게 확인할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환해 애플리케이션이 반환한 JSON 내에 주어진 배열이 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 더 있어도, 지정한 일부만 맞으면 이 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어서션

앞서 설명한 것처럼, `assertJson` 메서드는 JSON 응답 내에 특정 JSON 조각이 존재하는지 확인합니다. 반환된 JSON이 특정 배열과 **정확히 일치**하는지 확인하려면 `assertExactJson` 메서드를 사용하세요:

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
#### JSON 경로에 대한 어서션

JSON 응답에서 지정한 경로에 원하는 데이터가 있는지 검증하려면 `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath`는 클로저도 받을 수 있으므로, 동적으로 어서션 통과 여부를 결정할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 더 유연하고 아름답게 검사할 수 있는 방법도 제공합니다. 시작하려면, `assertJson` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 받아 JSON에 대한 다양한 어서션을 할 수 있게 해줍니다. `where` 메서드는 특정 속성에 대한 어서션, `missing` 메서드는 특정 속성 누락 여부를 확인할 수 있습니다:

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

#### `etc` 메서드의 동작

위 예제에서 어서션 체인의 끝에 `etc` 메서드를 호출했습니다. 이 메서드는 JSON 객체에 다른 속성이 더 있을 수 있음을 Laravel에 알리는 역할을 합니다. 만약 `etc` 메서드를 사용하지 않을 경우, JSON 객체에 명시적으로 어서션하지 않은 속성이 있으면 테스트가 실패하게 됩니다.

이 동작의 목적은 의도치 않게 JSON 응답에 민감한 정보가 노출되는 것을 방지하기 위함입니다. 개발자가 해당 속성에 대해 명시적으로 어서션하거나, 추가 속성을 `etc`로 허용하도록 강제합니다.

다만, `etc`를 사용하지 않는다고 해서, 중첩된 배열 내에 추가 속성이 없다는 보장은 되지 않습니다. `etc`는 메서드가 호출된 중첩 레벨까지만 검사합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어서션

특정 속성이 존재하는지 또는 없는지 확인하려면 `has`, `missing` 메서드를 사용합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

여러 속성의 존재/부재를 동시에 검사하려면 `hasAll`, `missingAll` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

주어진 목록 중 하나라도 존재하는지 확인하려면 `hasAny` 메서드를 사용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

보통 여러 사용자 등 다수의 아이템을 포함하는 JSON 응답을 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이 경우, 플루언트 JSON 객체의 `has` 메서드를 이용해 컬렉션의 아이템 수를, `first` 메서드를 이용해 첫 번째 객체에 대한 어서션을 할 수 있습니다:

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
#### JSON 컬렉션 어서션의 스코프 지정

경우에 따라 애플리케이션 경로에서 "users"와 같이 이름이 지정된 키의 JSON 컬렉션이 반환될 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이럴 때도 `has` 메서드를 이용해 각 컬렉션 및 개별 아이템의 어서션을 스코프할 수 있습니다:

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

`users` 컬렉션 검사와 개별 아이템 검사를 분리하지 않고, 세 번째 인자로 클로저를 제공해 한 번에 첫 번째 아이템에 대한 어서션을 할 수도 있습니다:

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

JSON 응답의 속성 타입만 검사하고 싶다면, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType` 또는 `whereAllType` 메서드를 사용할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 검사할 경우 `|` 문자나 타입 배열을 두 번째 인자로 전달할 수 있습니다. 응답 값이 나열된 타입 중 하나와 일치하면 어서션이 통과합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`과 `whereAllType`은 `string`, `integer`, `double`, `boolean`, `array`, `null` 타입을 지원합니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 이용하면 테스트에 사용할 임시 파일이나 이미지를 만들 수 있습니다. 이를 `Storage` 파사드의 `fake` 기능과 조합하면 파일 업로드 테스트가 매우 쉬워집니다. 예를 들어 프로필 이미지 업로드 폼을 이렇게 테스트할 수 있습니다:

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

특정 파일이 존재하지 않는지 확인하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### Fake 파일 커스터마이즈

`UploadedFile` 클래스의 `fake` 메서드로 파일을 생성할 때, 이미지의 가로/세로와 크기(KB 단위)를 지정해 애플리케이션의 검증 규칙을 테스트할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에 다른 타입의 파일은 `create` 메서드를 사용해 만들 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, `$mimeType` 인자를 전달해 파일의 MIME 타입을 명시적으로 지정할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트

Laravel에서는 애플리케이션에 HTTP 요청을 시뮬레이션하지 않고도 뷰를 렌더링할 수 있습니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하면 됩니다. 이 메서드는 뷰 이름과 옵션으로 데이터 배열을 인자로 받으며, 반환값으로 여러 편리한 어서션 메서드를 지원하는 `Illuminate\Testing\TestView` 인스턴스를 돌려줍니다:

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

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText` 등의 어서션 메서드를 제공합니다.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅해 원시 렌더링된 뷰 내용을 가져올 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 [Laravel의 글로벌 에러 백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 저장된 에러가 필요할 수 있습니다. 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면, `blade` 메서드를 사용해 원시 [Blade](/docs/{{version}}/blade) 문자열을 평가, 렌더링할 수 있습니다. `view` 메서드와 비슷하게, `blade` 메서드도 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/{{version}}/blade#components)는 `component` 메서드를 이용해 평가 및 렌더링할 수 있습니다. 이 경우 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 사용할 수 있는 다양한 커스텀 어서션 메서드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드에서 반환된 response 객체에서 사용할 수 있습니다.

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

상세한 어서션 설명은 각 링크를 참고하세요.

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 애플리케이션의 기능 테스트 내에서 사용할 수 있는 인증 관련 어서션도 제공합니다. 이 메서드들은 테스트 클래스 자체에서 호출된다(응답 인스턴스가 아님)에 유의하세요.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 확인합니다:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되어 있지 않은지 확인합니다:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 확인합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 검증 어서션

Laravel은 요청에 전달된 데이터가 유효하거나(혹은 무효)함을 보장하기 위한 두 가지 기본 검증 관련 어서션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답이 주어진 키에 대한 검증 에러가 없는지 확인합니다. 이 메서드는 검증 에러가 JSON 구조로 반환되거나, 세션에 flash된 경우 모두 어서션할 수 있습니다:

```php
// 검증 에러가 없음을 어서트...
$response->assertValid();

// 주어진 키에 대한 검증 에러가 없음을 어서트...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답이 주어진 키에 대한 검증 에러를 포함하는지 확인합니다. 이 메서드는 검증 에러가 JSON 구조로 반환되거나, 세션에 flash된 경우 모두 어서션할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 특정 검증 에러 메시지를 갖는지 어서션할 수도 있습니다. 이때 전체 메시지나, 메시지의 일부만 전달해도 됩니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

---

*각 어서션의 예시와 설명은 원문을 참고해주세요. 코드, HTML, 링크 및 마크다운 구조는 번역 대상이 아니거나 이미 유지되었습니다.*