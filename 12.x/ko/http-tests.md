# HTTP 테스트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이즈](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [Fluent JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade와 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 그 응답을 검사할 수 있는 매우 유연한 API를 제공합니다. 예를 들어, 아래와 같이 기능 테스트를 작성할 수 있습니다:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보냅니다. `assertStatus` 메서드는 반환된 응답의 HTTP 상태 코드가 지정한 값과 일치하는지 확인합니다. 이 간단한 어서션 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 호출하면 됩니다. 이 메서드들은 실제로 "진짜" HTTP 요청을 보내지 않고, 네트워크 요청을 내부적으로 시뮬레이션합니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, [여러 가지 유용한 어서션](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다.

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

일반적으로 각 테스트에서는 애플리케이션에 단 한 번의 요청만 만들어야 합니다. 하나의 테스트 메서드에서 여러 번 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이즈

`withHeaders` 메서드를 사용하여 요청이 애플리케이션에 전송되기 전에 헤더를 커스터마이즈할 수 있습니다. 이 메서드를 통해 원하는 커스텀 헤더를 요청에 추가할 수 있습니다.

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

요청을 보내기 전에 `withCookie`나 `withCookies` 메서드로 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 두 개의 인수로 받아들이고, `withCookies`는 이름/값 쌍의 배열을 받습니다.

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

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용하여 세션 데이터를 원하는 배열로 설정할 수 있습니다. 이는 요청을 보내기 전 세션에 데이터를 미리 로드할 때 유용합니다.

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

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용합니다. 따라서 `actingAs` 헬퍼 메서드를 사용하면 지정한 사용자를 현재 사용자로 간단하게 인증할 수 있습니다. 예시에서는 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용해 사용자를 생성, 인증합니다.

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

또한, `actingAs` 메서드의 두 번째 인수로 가드 이름을 지정해 어떤 가드를 사용할지 정할 수 있습니다. 이렇게 지정한 가드는 테스트가 끝날 때까지 기본 가드로 적용됩니다.

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 후 응답 내용을 검사하거나 디버깅하려면 `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용할 수 있습니다.

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

또한, 응답에 대한 정보를 덤프하고 실행을 중단하려면 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용할 수도 있습니다.

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

애플리케이션이 특정 예외를 발생시키는지 테스트해야 할 때가 있습니다. 이를 위해 `Exceptions` 파사드를 통해 예외 핸들러를 "가짜(faked)"로 만들 수 있습니다. 이렇게 하면 `assertReported`, `assertNotReported` 같은 메서드로 요청 중 발생한 예외에 대한 어서션을 할 수 있습니다.

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

`assertNotReported`, `assertNothingReported` 메서드를 사용하면, 특정 예외나 어떤 예외도 발생하지 않았는지 확인할 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

`withoutExceptionHandling` 메서드를 요청 전에 호출하면, 해당 요청에서 예외 처리를 완전히 비활성화할 수 있습니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

그리고, PHP 또는 사용하는 라이브러리에서 deprecated된 기능을 앱이 사용하지 않는지도 보장하려면, 요청 전 `withoutDeprecationHandling`를 호출하세요. 비활성화 시 경고가 예외로 변환되어 테스트가 실패합니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 특정 클로저 내부의 코드가 지정한 타입의 예외를 발생시키는지 확인합니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

예외를 검사하거나 어서션에 활용하려면 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드는 주어진 클로저 내 코드가 아무 예외도 발생시키지 않는지 확인합니다.

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API 및 그 응답을 테스트할 수 있는 여러 헬퍼도 제공합니다. 예를 들어 `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 통해 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있으며, 데이터와 헤더를 쉽게 전달할 수 있습니다. 우선 `/api/user`로 `POST` 요청을 보내고, 응답에 기대하는 JSON 데이터가 반환되었는지 어서션하는 테스트를 작성해봅니다.

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

또한, JSON 응답 데이터는 응답에서 배열 변수처럼 접근할 수 있어, 개별 값을 쉽게 검사할 수 있습니다.

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여, 지정한 배열이 애플리케이션에서 반환된 JSON 응답 안에 존재하는지 확인합니다. JSON 응답에 다른 속성이 더 포함돼 있어도, 지정한 조각이 존재하면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 어서션

앞서 언급했듯, `assertJson`은 JSON의 일부 조각(fragment)이 포함되어 있는지 확인하는 데 사용합니다. 반면, 반환되는 JSON이 특정 배열과 **정확히 일치하는지** 검증하려면 `assertExactJson` 메서드를 사용하세요.

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

JSON 응답이 특정 경로에 지정된 데이터를 포함하고 있는지 확인하려면 `assertJsonPath` 메서드를 사용하세요.

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

`assertJsonPath`에 클로저를 넘겨, 어서션의 통과 여부를 동적으로 판단할 수 있습니다.

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### Fluent JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 플루언트하게(fluent) 검증할 수 있는 아름다운 방법도 제공합니다. `assertJson` 메서드에 클로저를 전달하면, Laravel이 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 넘겨줍니다. 이 인스턴스는 JSON 응답에 다양한 어서션을 할 때 사용합니다. `where`로 특정 속성을 검증하고, `missing`으로 지정된 속성이 누락되었는지 검사할 수 있습니다.

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

위 예시에서 어서션 체인의 끝에 `etc` 메서드를 사용했습니다. 이 메서드는 해당 JSON 오브젝트에 추가적인 속성이 더 있을 수 있음을 Laravel에 알립니다. 만약 `etc`를 사용하지 않으면, 지정되지 않은 속성이 JSON 오브젝트에 존재할 경우 테스트가 실패합니다.

이 방식은, 민감 정보가 의도치 않게 JSON 응답에 노출되는 것을 방지할 수 있도록, 반드시 속성을 명시적으로 어서션하거나 `etc`로 허용하도록 강제하는 의도를 갖고 있습니다.

단, `etc`가 어서션 체인에 없다고 해서, JSON 오브젝트 내부에 중첩된 배열에 추가 속성이 없는 것을 보장하지는 않습니다. `etc`는 사용되는 계층에서만 속성의 추가 여부를 검사합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 유무 어서션

특정 속성이 응답에 있는지 또는 없는지 검사하려면 `has`, `missing` 메서드를 사용하세요.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

여러 속성의 유무도 `hasAll`, `missingAll`로 한 번에 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

`hasAny` 메서드를 사용하면, 주어진 목록 중 하나 이상의 속성이 있는지 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

라우트가 여러 항목(예: 사용자 여러 명)이 포함된 JSON 응답을 반환하는 경우가 자주 있습니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

이 경우, 플루언트 JSON 객체의 `has` 메서드로 포함된 사용자 수를 검증할 수 있습니다. 이어서, `first` 메서드에 클로저를 전달하여 첫 번째 사용자에 대해 더 상세한 어서션을 할 수 있습니다.

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
#### JSON 컬렉션 어서션 스코프 지정

라우트가 이름이 지정된 키에 JSON 컬렉션을 할당해 반환하는 경우도 있습니다.

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이런 상황에서는 `has`로 컬렉션 아이템 수를 검증하고, 또 이 메서드를 체인으로 사용해 스코프를 지정할 수 있습니다.

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

또한, `has` 메서드를 한 번만 호출하고 클로저를 세 번째 인자로 넘기면, 해당 컬렉션의 첫 번째 항목에 자동으로 스코프되어 호출됩니다.

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

JSON 응답의 속성이 특정 타입인지 검증하고 싶을 때, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`, `whereAllType` 메서드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

여러 타입을 지정하려면 `|` 문자를 사용하거나, 두 번째 인수에 타입 배열을 넘길 수 있습니다. 응답 값이 나열된 타입 중 하나라도 해당되면 어서션이 통과합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`, `whereAllType`가 인식하는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null`입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드는 테스트용 더미 파일이나 이미지를 손쉽게 생성할 수 있습니다. 이 기능은 `Storage` 파사드의 `fake` 메서드와 결합하면 파일 업로드 테스트가 매우 간편해집니다. 예를 들어, 아바타 업로드 폼을 쉽게 테스트할 수 있습니다.

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

지정한 파일이 존재하지 않는지 확인하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다.

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이즈

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때, 이미지의 너비, 높이, 크기(킬로바이트 단위)를 지정하여 애플리케이션의 검증 규칙 테스트를 더 세밀하게 할 수 있습니다.

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도, `create` 메서드를 통해 다른 타입의 파일도 생성 가능합니다.

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, 메서드에 `$mimeType` 인수를 넘겨 파일이 반환해야 할 MIME 타입을 명시할 수도 있습니다.

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트

Laravel은 애플리케이션에 시뮬레이션된 HTTP 요청 없이도 뷰를 렌더링할 수 있습니다. 테스트 내에서 `view` 메서드를 호출하면 됩니다. `view`는 뷰 이름과 데이터 배열(선택)을 받으며, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 인스턴스는 뷰 내용에 대해 다양한 어서션 메서드를 제공합니다.

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

필요하다면, `TestView` 인스턴스를 문자열로 변환해서 렌더링된 뷰 원본을 얻을 수도 있습니다.

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 [Laravel에서 제공하는 글로벌 에러 백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용하세요.

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade와 컴포넌트 렌더링

필요하다면, `blade` 메서드를 사용하여 [Blade](/docs/{{version}}/blade) 원시 문자열을 평가하고 렌더링할 수 있습니다. `view`와 마찬가지로, 이 메서드도 `Illuminate\Testing\TestView` 인스턴스를 반환합니다.

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/{{version}}/blade#components)를 평가·렌더링하려면 `component` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다.

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 활용할 수 있는 다양한 커스텀 어서션 메서드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답 인스턴스에서 사용할 수 있습니다.

<style>
    .collection-method-list > p {
        columns: 14.4em 2; -moz-columns: 14.4em 2; -webkit-columns: 14.4em 2;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

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

#### assertBadRequest

응답이 '잘못된 요청(400)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertBadRequest();
```

#### assertAccepted

응답이 '허용됨(202)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertAccepted();
```

#### assertConflict

응답이 '충돌(409)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertConflict();
```

#### assertCookie

응답에 지정한 쿠키가 포함되어 있는지 확인합니다.

```php
$response->assertCookie($cookieName, $value = null);
```

#### assertCookieExpired

응답에 지정한 쿠키가 포함되어 있고, 만료되었는지 확인합니다.

```php
$response->assertCookieExpired($cookieName);
```

#### assertCookieNotExpired

응답에 지정한 쿠키가 포함되어 있고, 만료되지 않았는지 확인합니다.

```php
$response->assertCookieNotExpired($cookieName);
```

#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않은지 확인합니다.

```php
$response->assertCookieMissing($cookieName);
```

#### assertCreated

응답이 201 HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertCreated();
```

#### assertDontSee

주어진 문자열이 응답 내에 포함되어 있지 않은지 확인합니다. 두 번째 인수를 `false`로 넘기면 문자열 이스케이프를 하지 않습니다.

```php
$response->assertDontSee($value, $escape = true);
```

#### assertDontSeeText

주어진 문자열이 응답 텍스트에 포함되어 있지 않은지 확인합니다. 두 번째 인수를 `false`로 넘기면 문자열 이스케이프를 하지 않습니다. 이 메서드는 어서션 전 `strip_tags` PHP 함수를 사용해 응답 내용을 처리합니다.

```php
$response->assertDontSeeText($value, $escape = true);
```

#### assertDownload

응답이 "다운로드"인지 확인합니다. 일반적으로 이는 라우트가 `Response::download`, `BinaryFileResponse`, `Storage::download` 응답을 반환했음을 의미합니다.

```php
$response->assertDownload();
```

다운로드 파일명이 지정됐는지 어서션할 수도 있습니다.

```php
$response->assertDownload('image.jpg');
```

#### assertExactJson

응답이 주어진 JSON 데이터와 정확히 일치하는지 확인합니다.

```php
$response->assertExactJson(array $data);
```

#### assertExactJsonStructure

응답이 주어진 JSON 구조와 정확히 일치하는지 확인합니다.

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 더 엄격하게, 응답에 예상한 JSON 구조에 명시되지 않은 키가 있으면 실패합니다.

#### assertForbidden

응답이 '금지됨(403)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertForbidden();
```

#### assertFound

응답이 '찾음(302)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertFound();
```

#### assertGone

응답이 '사라짐(410)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertGone();
```

#### assertHeader

응답에 주어진 헤더와 값이 존재하는지 확인합니다.

```php
$response->assertHeader($headerName, $value = null);
```

#### assertHeaderMissing

응답에 해당 헤더가 없는지 확인합니다.

```php
$response->assertHeaderMissing($headerName);
```

#### assertInternalServerError

응답이 "내부 서버 오류(500)" HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertInternalServerError();
```

#### assertJson

응답이 지정한 JSON 데이터를 포함하는지 확인합니다.

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환하여, 지정 배열이 존재하면 다른 프로퍼티가 더 있어도 성공합니다.

#### assertJsonCount

응답 JSON이 지정한 키에서 예상 개수의 배열 항목을 가지고 있는지 확인합니다.

```php
$response->assertJsonCount($count, $key = null);
```

#### assertJsonFragment

응답 내 어디에서든 지정한 JSON 데이터 조각을 포함하는지 확인합니다.

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

#### assertJsonIsArray

응답 JSON이 배열인지 확인합니다.

```php
$response->assertJsonIsArray();
```

#### assertJsonIsObject

응답 JSON이 객체인지 확인합니다.

```php
$response->assertJsonIsObject();
```

#### assertJsonMissing

응답에 지정한 JSON 데이터가 없는지 확인합니다.

```php
$response->assertJsonMissing(array $data);
```

#### assertJsonMissingExact

응답에 정확히 일치하는 JSON 데이터가 없는지 확인합니다.

```php
$response->assertJsonMissingExact(array $data);
```

#### assertJsonMissingValidationErrors

응답이 지정된 키에 대해 JSON 검증 오류가 없는지 확인합니다.

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 응답에 JSON으로 반환된 검증 오류가 없고, 세션에도 오류가 플래시되지 않았는지 어서트하는 데 사용할 수 있습니다.

#### assertJsonPath

응답이 지정한 경로에 해당 값이 있는지 확인합니다.

```php
$response->assertJsonPath($path, $expectedValue);
```

예시: 응답이 다음과 같다면,

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 `user` 객체의 `name` 프로퍼티를 어서트할 수 있습니다.

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

#### assertJsonMissingPath

응답에 지정한 경로가 존재하지 않는지 확인합니다.

```php
$response->assertJsonMissingPath($path);
```

예시: 다음 응답에서

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 객체에 `email` 프로퍼티가 없는지 어서트할 수 있습니다.

```php
$response->assertJsonMissingPath('user.email');
```

#### assertJsonStructure

응답이 지정한 JSON 구조를 가지는지 확인합니다.

```php
$response->assertJsonStructure(array $structure);
```

예시: 다음 응답

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래처럼 구조을 어서트할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

애플리케이션이 객체 배열을 반환하는 경우,

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

`*` 문자를 사용해 배열 내 모든 객체의 구조를 어서트할 수 있습니다.

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

#### assertJsonValidationErrors

지정된 키에 대해 응답에 JSON 검증 오류가 있는지 확인합니다. 이 메서드는 검증 오류가 세션이 아닌 JSON 구조로 반환될 때 사용합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON이나 세션으로 반환된 오류를 모두 어서트할 수 있습니다.

#### assertJsonValidationErrorFor

지정 키에 대해 응답이 하나 이상의 JSON 검증 오류를 가졌는지 확인합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

#### assertMethodNotAllowed

응답이 '허용되지 않는 메서드(405)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertMethodNotAllowed();
```

#### assertMovedPermanently

응답이 '영구 이동(301)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertMovedPermanently();
```

#### assertLocation

응답의 `Location` 헤더가 지정한 URI 값을 가지는지 확인합니다.

```php
$response->assertLocation($uri);
```

#### assertContent

응답 내용이 주어진 문자열과 일치하는지 확인합니다.

```php
$response->assertContent($value);
```

#### assertNoContent

응답이 지정 HTTP 상태 코드와, 내용이 없는지 확인합니다.

```php
$response->assertNoContent($status = 204);
```

#### assertStreamed

응답이 스트리밍 응답이었는지 확인합니다.

    $response->assertStreamed();

#### assertStreamedContent

스트리밍 응답 내용이 지정한 문자열과 일치하는지 확인합니다.

```php
$response->assertStreamedContent($value);
```

#### assertNotFound

응답이 '찾을 수 없음(404)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertNotFound();
```

#### assertOk

응답이 200 HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertOk();
```

#### assertPaymentRequired

응답이 '결제 필요(402)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertPaymentRequired();
```

#### assertPlainCookie

응답에 지정된 암호화되지 않은 쿠키가 있는지 확인합니다.

```php
$response->assertPlainCookie($cookieName, $value = null);
```

#### assertRedirect

응답이 지정 URI로 리디렉션 되는지 확인합니다.

```php
$response->assertRedirect($uri = null);
```

#### assertRedirectBack

응답이 직전 페이지로 리디렉션되는지 확인합니다.

```php
$response->assertRedirectBack();
```

#### assertRedirectContains

응답 URI가 지정 문자열을 포함한 곳으로 리디렉션되는지 확인합니다.

```php
$response->assertRedirectContains($string);
```

#### assertRedirectToRoute

응답이 지정 [이름 있는 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션되는지 확인합니다.

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

#### assertRedirectToSignedRoute

응답이 지정 [서명된 라우트](/docs/{{version}}/urls#signed-urls)로 리디렉션되는지 확인합니다.

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

#### assertRequestTimeout

응답이 '요청 타임아웃(408)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertRequestTimeout();
```

#### assertSee

지정 문자열이 응답에 포함되어 있는지 확인합니다. 두 번째 인수를 `false`로 넘기면 문자열 이스케이프를 하지 않습니다.

```php
$response->assertSee($value, $escape = true);
```

#### assertSeeInOrder

여러 문자열이 지정한 순서대로 응답에 포함되어 있는지 확인합니다. 두 번째 인수를 `false`로 넘기면 문자열 이스케이프를 하지 않습니다.

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

#### assertSeeText

지정 문자열이 응답 텍스트에 포함되어 있는지 확인합니다. 두 번째 인수를 `false`로 넘기면 문자열 이스케이프를 하지 않습니다. 어서션 전 응답 내용을 `strip_tags` 함수를 거칩니다.

```php
$response->assertSeeText($value, $escape = true);
```

#### assertSeeTextInOrder

여러 문자열이 지정한 순서대로 응답 텍스트에 포함되어 있는지 확인합니다. 두 번째 인수를 `false`로 넘기면 문자열 이스케이프를 하지 않습니다. 어서션 전 응답 내용을 `strip_tags` 함수를 거칩니다.

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

#### assertServerError

응답이 서버 오류(>= 500, < 600) HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertServerError();
```

#### assertServiceUnavailable

응답이 "서비스 사용불가(503)" HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertServiceUnavailable();
```

#### assertSessionHas

세션에 지정 데이터가 포함되어 있는지 확인합니다.

```php
$response->assertSessionHas($key, $value = null);
```

두 번째 인수로 클로저를 전달할 수 있으며, 클로저가 true를 반환하면 어서션이 통과합니다.

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

#### assertSessionHasInput

세션의 [플래시 입력값 배열](/docs/{{version}}/responses#redirecting-with-flashed-session-data)에 값이 있는지 확인합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

두 번째 인수로 클로저를 넘길 수 있습니다.

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

#### assertSessionHasAll

세션이 주어진 키/값 쌍 배열을 모두 포함하는지 확인합니다.

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 세션에 `name`, `status` 키가 있으면 다음과 같이 어서트합니다.

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

#### assertSessionHasErrors

세션이 지정 `$keys`에 대해 오류를 포함하고 있는지 확인합니다. `$keys`가 연관 배열이면, 각 필드(키)에 지정된 오류 메시지(값)가 존재하는지 확인합니다. 검증 오류가 세션에 플래시될 때 사용하는 메서드입니다.

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예시로 `name`, `email` 필드에 검증 오류가 세션에 플래시되었는지 어서트하려면:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

특정 필드가 특정 오류 메시지를 가졌는지 확인할 수도 있습니다.

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON이든 세션이든, 검증 오류를 모두 어서트할 수 있습니다.

#### assertSessionHasErrorsIn

지정 [에러 백](/docs/{{version}}/validation#named-error-bags) 내에서 지정 `$keys`에 대한 오류가 포함되어 있는지 확인합니다. `$keys`가 연관 배열이면, 에러 백 내 각 필드에 지정 오류 메시지가 있는지 확인합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

#### assertSessionHasNoErrors

세션에 검증 오류가 없는지 확인합니다.

```php
$response->assertSessionHasNoErrors();
```

#### assertSessionDoesntHaveErrors

지정 키에 대한 세션에 검증 오류가 없는지 확인합니다.

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 응답에 JSON 오류가 없고 세션에도 오류가 없는지 모두 어서트할 수 있습니다.

#### assertSessionMissing

세션에 지정 키가 없는지 확인합니다.

```php
$response->assertSessionMissing($key);
```

#### assertStatus

응답이 지정한 HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertStatus($code);
```

#### assertSuccessful

응답이 성공(>=200, <300) HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertSuccessful();
```

#### assertTooManyRequests

응답이 '요청 과다(429)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertTooManyRequests();
```

#### assertUnauthorized

응답이 '인증되지 않음(401)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertUnauthorized();
```

#### assertUnprocessable

응답이 '처리 불가(422)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertUnprocessable();
```

#### assertUnsupportedMediaType

응답이 '지원하지 않는 미디어 타입(415)' HTTP 상태 코드를 가지는지 확인합니다.

```php
$response->assertUnsupportedMediaType();
```

#### assertValid

응답이 지정된 키에 대해 검증 오류가 없는지 확인합니다. 이 메서드는 JSON 또는 세션으로 오류가 반환된 경우 모두 어서트할 수 있습니다.

```php
// 검증 오류가 하나도 없는지 어서트
$response->assertValid();

// 지정 키에 검증 오류가 없는지 어서트
$response->assertValid(['name', 'email']);
```

#### assertInvalid

응답이 지정된 키에 대해 검증 오류가 있는지 확인합니다. 이 메서드는 JSON 또는 세션으로 오류가 반환된 경우 모두 어서트할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

키에 특정 검증 오류 메시지가 있는지 어서트하려면 전체 메시지 또는 부분 문자열을 전달하면 됩니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

오류가 있는 필드가 제공한 것만 있는지 확인하려면 `assertOnlyInvalid` 메서드를 사용할 수 있습니다.

```php
$response->assertOnlyInvalid(['name', 'email']);
```

#### assertViewHas

응답 뷰에 지정 데이터가 포함되어 있는지 확인합니다.

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인수로 클로저를 넘기면, 특정 뷰 데이터를 검사하고 어서트할 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한, 뷰 데이터를 배열 변수처럼 접근해 쉽게 검사할 수도 있습니다.

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

#### assertViewHasAll

응답 뷰에 주어진 데이터 목록이 있는지 확인합니다.

```php
$response->assertViewHasAll(array $data);
```

뷰에 키만 있는지 어서트할 수도 있고,

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

특정 값까지 검증할 수도 있습니다.

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

#### assertViewIs

지정한 뷰가 라우트에서 반환됐는지 확인합니다.

```php
$response->assertViewIs($value);
```

#### assertViewMissing

응답 뷰에 지정 데이터 키가 없는지 확인합니다.

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 애플리케이션의 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 이 메서드들은 `get`, `post` 등에서 반환한 `Illuminate\Testing\TestResponse`가 아니라, 테스트 클래스 본체에서 호출합니다.

#### assertAuthenticated

사용자가 인증되었는지 확인합니다.

```php
$this->assertAuthenticated($guard = null);
```

#### assertGuest

사용자가 인증되지 않았는지 확인합니다.

```php
$this->assertGuest($guard = null);
```

#### assertAuthenticatedAs

특정 사용자가 인증되었는지 확인합니다.

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 검증 어서션

Laravel은 요청에 제공된 데이터가 유효했는지, 아니었는지 확인하기 위한 두 가지 주요 검증 어서션을 제공합니다.

#### assertValid

응답이 지정된 키에 대해 검증 오류가 없는지 확인합니다. 이 메서드는 JSON 또는 세션으로 오류가 반환될 때 모두 사용할 수 있습니다.

```php
// 검증 오류가 하나도 없는지 어서트
$response->assertValid();

// 지정 키에 검증 오류가 없는지 어서트
$response->assertValid(['name', 'email']);
```

#### assertInvalid

응답이 지정된 키에 대해 검증 오류가 있는지 확인합니다. 이 메서드는 JSON 또는 세션으로 오류가 반환될 때 모두 사용할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

주어진 키에 특정 검증 오류 메시지가 있는지도 전체 메시지나 부분 문자열로 어서트할 수 있습니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
