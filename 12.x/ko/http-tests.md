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
    - [유효성 검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션에 HTTP 요청을 보내고, 그 응답을 검증할 수 있는 매우 플루언트한 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트(feature test)를 살펴보겠습니다.

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

여기서 `get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가지는지 확인합니다. 이 단순한 어서션 외에도, 라라벨은 응답 헤더, 본문 콘텐츠, JSON 구조 등을 검사할 수 있는 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 만들기

테스트 내에서 애플리케이션에 요청을 보내기 위해서는 `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 이 메서드들은 실제 네트워크를 통해 "진짜" HTTP 요청을 보내지 않고, 내부적으로 네트워크 요청을 시뮬레이션하여 처리합니다.

요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, [다양한 유용한 어서션](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이로써 애플리케이션의 응답을 쉽게 검사할 수 있습니다.

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

일반적으로 각 테스트는 애플리케이션에 한 번만 요청을 보내야 합니다. 단일 테스트 메서드 내에서 여러 번 요청을 보내면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 테스트 실행 시에는 편의를 위해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

요청을 보낼 때 헤더를 커스터마이즈하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드를 이용하면 요청에 원하는 커스텀 헤더를 추가할 수 있습니다.

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

요청을 보내기 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 각각 인수로 받고, `withCookies`는 이름/값 쌍의 배열을 인수로 받습니다.

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

라라벨은 HTTP 테스트 시 세션을 다루기 위한 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드로 세션 데이터를 배열로 미리 설정할 수 있습니다. 이 기능은 요청을 보내기 전에 세션에 데이터를 미리 로드해야 할 때 유용합니다.

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

라라벨의 세션은 주로 로그인한 사용자의 상태를 유지하는 데 사용됩니다. 따라서, `actingAs` 헬퍼 메서드를 사용하면 특정 사용자를 현재 사용자로 간단히 인증할 수 있습니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다.

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

인증에 사용할 guard를 지정하고 싶다면, `actingAs` 메서드의 두 번째 인수로 guard 이름을 전달할 수 있습니다. 이렇게 지정하면, 해당 guard가 해당 테스트 실행 동안 기본 guard가 됩니다.

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답의 내용을 확인하고 디버깅할 수 있습니다.

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

또한, `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 이용해 응답의 정보를 출력한 뒤 코드 실행을 중단할 수도 있습니다.

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

애플리케이션에서 특정 예외가 발생하는지 테스트해야 할 때가 있습니다. 이를 위해 `Exceptions` 파사드를 사용하여 예외 핸들러를 "가짜(fake)"로 만들 수 있습니다. 예외 핸들러가 가짜로 설정된 후에는, 요청 처리 중 발생한 예외에 대해 `assertReported`와 `assertNotReported` 메서드로 어서션할 수 있습니다.

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

`assertNotReported`와 `assertNothingReported` 메서드는 요청 처리 중 특정 예외가 발생하지 않았거나, 어떤 예외도 발생하지 않았음을 어서트하는 데 사용할 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하려면, 요청을 보내기 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 언어나 사용하는 라이브러리가 더 이상 지원하지 않는(deprecated) 기능이 사용되지 않도록 확실히 하고 싶다면, 요청 전 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이 기능을 비활성화하면, deprecation 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드를 이용해, 주어진 클로저 내에서 특정 유형의 예외가 발생하는지 어서션할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외를 직접 확인하고 추가 어서션을 하고 싶다면, `assertThrows`의 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

반대로, 클로저 내의 코드가 예외를 전혀 발생시키지 않는지 검증하려면 `assertDoesntThrow` 메서드를 사용하면 됩니다.

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

라라벨은 JSON API 및 그 응답을 테스트할 수 있는 다양한 헬퍼 메서드도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson`과 같은 메서드는 각각의 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 이 메서드에 데이터를 배열로 전달하거나, 필요에 따라 헤더를 함께 보낼 수도 있습니다. 예를 들어, `/api/user`에 `POST` 요청을 보내고 기대하는 JSON 데이터가 정상적으로 반환되는지 테스트해보겠습니다.

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

또한, JSON 응답 데이터는 배열 변수처럼 접근할 수 있어서, JSON 응답 내 개별 값 검증이 편리합니다.

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤, 주어진 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 검증합니다. 따라서, JSON에 다른 속성이 더 포함되어 있더라도, 주어진 조각(fragment)이 있다면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### JSON의 정확한 일치(assertExactJson) 어서션

앞서 언급한 것처럼, `assertJson` 메서드는 JSON 응답 내에 특정 데이터를 포함하고 있는지 어서트합니다. 만약 애플리케이션에서 반환한 JSON이 주어진 배열과 **정확히 일치하는지** 확인하려면 `assertExactJson` 메서드를 사용해야 합니다.

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
#### JSON 경로(Path)로 값 어서트하기

JSON 응답에서 특정 경로에 주어진 데이터가 존재하는지 검증하고 싶다면, `assertJsonPath` 메서드를 활용합니다.

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

`assertJsonPath` 메서드는 또한 클로저를 인수로 받을 수 있어, 동적으로 어서션의 성공 여부를 판단할 수 있습니다.

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>

### 플루언트 JSON 테스트

라라벨은 여러분의 애플리케이션이 반환하는 JSON 응답을 더 유연하고 아름답게 테스트할 수 있는 방법도 제공합니다. 사용을 시작하려면, `assertJson` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인자로 받으며, 이를 활용해 반환된 JSON 데이터에 대해 다양한 assert(확인)를 수행할 수 있습니다. `where` 메서드는 JSON의 특정 속성에 대한 확인을, `missing` 메서드는 JSON에서 특정 속성이 존재하지 않음을 확인할 때 사용합니다.

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

위 예제에서 assert 체인의 마지막에 `etc` 메서드를 호출한 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 여러분이 assert로 명시하지 않은 다른 속성들도 포함될 수 있음을 라라벨에 알리는 역할을 합니다. 만약 `etc` 메서드를 사용하지 않는다면, assert에서 확인하지 않은 속성이 JSON 객체에 존재할 경우 테스트가 실패합니다.

이러한 동작의 의도는, JSON 응답에서 민감한 정보가 무심코 노출되지 않도록 하기 위함입니다. 즉, 속성을 포함하고 싶다면 명확히 assert로 확인하거나, 그렇지 않으면 `etc`를 사용해 추가 속성 허용을 명확히 해야 합니다.

단, `etc` 메서드를 체인에서 호출하지 않는다고 해서, 여러분의 JSON 객체 내에 중첩된 배열들에 추가 속성이 없는 것은 보장하지 않습니다. `etc`는 호출된 그 중첩 레벨에만 해당하는 속성의 추가 여부만 확인합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 확인하기

특정 속성이 존재하는지, 혹은 존재하지 않는지 확인하려면 `has`와 `missing` 메서드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한, `hasAll`과 `missingAll` 메서드를 이용하면 여러 속성의 존재 여부를 한 번에 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

지정한 여러 속성들 중 하나 이상이 존재하는지 확인하려면 `hasAny` 메서드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 테스트

라우트가 여러 객체(예: 여러 사용자)를 담은 JSON 응답을 반환하는 경우가 많습니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

이런 경우에는 플루언트 JSON 객체의 `has` 메서드를 이용해 응답에 포함된 사용자 수 등을 확인할 수 있습니다. 예를 들어, JSON 응답에 3명의 사용자가 존재하는지 확인한 뒤, `first` 메서드로 첫 번째 사용자에 대해 추가로 체크해볼 수 있습니다. `first` 메서드는 클로저를 인자로 받아, JSON 컬렉션의 첫 번째 객체에 대해 assert를 할 수 있습니다.

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
#### JSON 컬렉션 스코프 지정하여 테스트하기

때때로 라우트가 이름이 부여된 키에 JSON 컬렉션을 할당해서 반환하기도 합니다.

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이때는 `has` 메서드를 활용해 컬렉션 아이템 수에 대한 assert(확인)를 하거나, assert들의 체인을 특정 컬렉션에 스코프해서 작성할 수 있습니다.

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

`users` 컬렉션에 대해 두 번의 `has` 호출로 별도 assert를 작성하는 대신, 세 번째 인자로 클로저를 전달하는 한 번의 `has` 호출만으로도 동일한 효과를 얻을 수 있습니다. 이때 클로저는 자동으로 컬렉션의 첫 번째 아이템에 스코프 됩니다.

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

JSON 응답 내 속성들의 타입(type)이 원하는 타입인지 검증하고 싶을 때가 있습니다. `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`, `whereAllType` 메서드를 사용하면 손쉽게 타입을 체크할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`whereType` 메서드의 두 번째 인자로 여러 타입을 지정할 수도 있습니다. `|` 문자를 사용하거나 타입 배열을 넘기면, 값이 그 중 하나라도 맞으면 검증에 성공합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType` 및 `whereAllType` 메서드는 다음 타입들을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일이나 이미지를 생성해주는 `fake` 메서드를 제공합니다. 여기에 `Storage` 파사드의 `fake` 메서드를 결합하면 파일 업로드 테스트가 아주 간단해집니다. 예를 들어, 아바타 업로드 폼을 다음과 같이 테스트할 수 있습니다.

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

특정 파일이 존재하지 않는지 확인하고 싶다면, `Storage` 파사드가 제공하는 `assertMissing` 메서드를 사용할 수 있습니다.

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 테스트용 파일 커스터마이즈하기

`UploadedFile` 클래스의 `fake` 메서드로 파일을 만들 때, 테스트 상황에 더 잘 맞도록 이미지의 가로/세로 길이, 파일 크기(킬로바이트 단위)를 지정할 수 있습니다.

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외에도, `create` 메서드를 사용하면 어떤 유형이든 파일을 생성할 수 있습니다.

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면, `$mimeType` 인자를 추가로 전달하여 반환될 파일의 MIME 타입을 명시적으로 지정할 수 있습니다.

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰(View) 테스트

라라벨은 애플리케이션에 대하여 실제 HTTP 요청을 수행하지 않고도 뷰를 렌더링하여 테스트하는 기능을 제공합니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하면 됩니다. `view` 메서드는 뷰 이름과(필요하다면) 데이터 배열을 인자로 받으며, 반환값은 `Illuminate\Testing\TestView` 인스턴스입니다. 이 인스턴스는 뷰의 내용을 assert(확인)할 수 있는 여러 가지 메서드를 제공합니다.

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

`TestView` 클래스는 다음과 같은 assert 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 뷰의 원본 렌더링 결과를 얻을 수도 있습니다.

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 메시지를 공유하기

어떤 뷰들은 [라라벨이 제공하는 글로벌 에러 백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존하기도 합니다. 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용할 수 있습니다.

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면, `blade` 메서드를 이용해 [Blade](/docs/12.x/blade) 원본 문자열을 평가하고 렌더링할 수도 있습니다. `view` 메서드처럼, `blade` 역시 반환값으로 `Illuminate\Testing\TestView` 인스턴스를 반환합니다.

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

`component` 메서드를 활용하면 [Blade 컴포넌트](/docs/12.x/blade#components)를 평가하고 렌더링할 수 있습니다. 이 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다.

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 Assertion 메서드

<a name="response-assertions"></a>
### 응답(Response) Assertion

라라벨의 `Illuminate\Testing\TestResponse` 클래스는 여러분의 애플리케이션을 테스트할 때 활용할 수 있는 다양한 커스텀 assertion 메서드를 제공합니다. 이 assertion들은 `json`, `get`, `post`, `put`, `delete` 등 테스트 메서드에서 반환된 응답에서 사용할 수 있습니다.

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

응답이 HTTP 상태 코드 202(accepted)를 반환하는지 확인합니다.

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

응답이 HTTP 상태 코드 400(bad request)을 반환하는지 확인합니다.

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

응답이 400 이상 500 미만의 HTTP 상태 코드(클라이언트 에러)를 반환하는지 확인합니다.

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

응답이 HTTP 상태 코드 409(conflict)를 반환하는지 확인합니다.

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정한 쿠키가 포함되어 있는지 확인합니다.

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정한 쿠키가 포함되어 있고, 해당 쿠키가 만료되었는지 확인합니다.

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정한 쿠키가 포함되어 있고, 해당 쿠키가 만료되지 않았는지 확인합니다.

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않은지 확인합니다.

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 HTTP 201 상태 코드(created)를 반환하는지 확인합니다.

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답 본문에 지정한 문자열이 포함되어 있지 않은지 확인합니다. 두 번째 인자를 `false`로 전달하지 않는 한, 지정한 문자열은 자동으로 이스케이프됩니다.

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 지정한 문자열이 포함되어 있지 않은지 확인합니다. 두 번째 인자를 `false`로 전달하지 않는 한, 지정한 문자열은 자동으로 이스케이프됩니다. 이 메서드는 응답 내용을 `strip_tags` PHP 함수로 처리한 뒤 assert를 수행합니다.

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드" 가능한 응답인지 확인합니다. 일반적으로 호출된 라우트가 `Response::download`, `BinaryFileResponse`, `Storage::download` 응답을 반환할 때 해당합니다.

```php
$response->assertDownload();
```

파일 이름까지 확인하고 싶다면, 다운로더블 파일에 지정된 파일 이름이 맞는지 assert할 수도 있습니다.

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답에 지정한 JSON 데이터가 정확히 일치하는지 확인합니다.

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답의 JSON 구조가 지정한 구조와 정확히 일치하는지 확인합니다.

```php
$response->assertExactJsonStructure(array $data);
```

이 메서드는 [assertJsonStructure](#assert-json-structure)보다 더 엄격하게 동작합니다. `assertJsonStructure`와 달리, 예상 JSON 구조에 명시되지 않은 키가 응답에 하나라도 포함되어 있을 경우 테스트가 실패합니다.

<a name="assert-forbidden"></a>

#### assertForbidden

응답의 HTTP 상태 코드가 forbidden(403)임을 확인합니다.

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

응답의 HTTP 상태 코드가 found(302)임을 확인합니다.

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

응답의 HTTP 상태 코드가 gone(410)임을 확인합니다.

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정된 헤더와 값이 존재하는지 확인합니다.

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정된 헤더가 없는지 확인합니다.

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

응답의 HTTP 상태 코드가 "Internal Server Error"(500)임을 확인합니다.

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

응답이 지정된 JSON 데이터를 포함하고 있는지 확인합니다.

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메서드는 응답을 배열로 변환하여, 지정된 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서, JSON 응답에 다른 프로퍼티가 더 포함되어 있어도 지정된 일부 데이터만 있으면 이 테스트는 통과하게 됩니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답의 JSON에서 지정한 키에 해당하는 배열이 기대하는 개수의 아이템을 가지고 있는지 확인합니다.

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 주어진 JSON 데이터 조각이 어디든 포함되어 있는지 확인합니다.

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

응답의 JSON이 배열인지 확인합니다.

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답의 JSON이 객체인지 확인합니다.

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답이 지정한 JSON 데이터를 포함하고 있지 않은지 확인합니다.

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

응답이 지정한 키에 대한 JSON 유효성 검증 에러가 없는지 확인합니다.

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 범용적인 [assertValid](#assert-valid) 메서드를 사용하면, 응답에 JSON으로 반환된 유효성 검증 에러가 없고 **또한** 세션 스토리지에도 에러가 저장되지 않았는지 확인할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답의 지정한 경로(path)에 기대하는 값이 포함되어 있는지 확인합니다.

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어, 애플리케이션에서 다음과 같은 JSON 응답을 반환한다고 가정해 보겠습니다.

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래와 같이, `user` 객체의 `name` 프로퍼티가 지정한 값과 일치하는지 확인할 수 있습니다.

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정한 경로(path)가 포함되어 있지 않은지 확인합니다.

```php
$response->assertJsonMissingPath($path);
```

예를 들어, 애플리케이션에서 다음과 같은 JSON 응답을 반환한다고 가정해 보겠습니다.

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래와 같이, `user` 객체에 `email` 프로퍼티가 포함되어 있지 않은지 확인할 수 있습니다.

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답의 JSON이 특정 구조를 가지고 있는지 확인합니다.

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 애플리케이션이 다음과 같은 JSON 데이터를 반환한다고 가정해 보겠습니다.

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

아래와 같이 JSON 구조가 기대한 대로 되어 있는지 확인할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때로는, 애플리케이션이 반환하는 JSON 응답에 객체의 배열이 포함될 수 있습니다.

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

이와 같은 상황이라면, 배열 내 모든 객체의 구조를 확인할 때 `*` 문자를 사용할 수 있습니다.

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

응답이 지정한 키에 대한 JSON 유효성 검증 에러를 포함하고 있는지 확인합니다. 이 메서드는 유효성 검증 에러가 세션에 저장되는 대신 JSON 구조로 반환되는 응답을 테스트할 때 사용해야 합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 범용적인 [assertInvalid](#assert-invalid) 메서드를 사용하면, 응답에 JSON으로 반환된 유효성 검증 에러가 있는지 **또는** 에러가 세션에 저장되어 있는지 모두 확인할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답이 지정한 키에 대한 JSON 유효성 검증 에러를 가지고 있는지 확인합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

응답의 HTTP 상태 코드가 method not allowed(405)임을 확인합니다.

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답의 HTTP 상태 코드가 moved permanently(301)임을 확인합니다.

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

지정한 문자열이 응답의 본문 내용과 일치하는지 확인합니다.

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정된 HTTP 상태 코드를 가지고 있고, 본문이 비어 있는지 확인합니다.

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트리밍 방식의 응답인지 확인합니다.

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

지정한 문자열이 스트리밍 응답의 내용과 일치하는지 확인합니다.

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답의 HTTP 상태 코드가 not found(404)임을 확인합니다.

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답의 HTTP 상태 코드가 200임을 확인합니다.

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답의 HTTP 상태 코드가 payment required(402)임을 확인합니다.

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정한 이름의 암호화되지 않은 쿠키가 존재하는지 확인합니다.

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 주어진 URI로 리다이렉션되는지 확인합니다.

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로 리다이렉트되고 있는지 확인합니다.

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리다이렉트되고, [세션에 지정한 에러가 있는지](#assert-session-has-errors) 확인합니다.

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

응답이 이전 페이지로 리다이렉트되고, 세션에 어떤 에러 메시지도 포함되어 있지 않은지 확인합니다.

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 지정한 문자열을 포함하는 URI로 리다이렉트되는지 확인합니다.

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 지정한 [이름 있는 라우트](/docs/12.x/routing#named-routes)로 리다이렉트되는지 확인합니다.

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

응답의 HTTP 상태 코드가 request timeout(408)인지 확인합니다.

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

지정한 문자열이 응답 내에 포함되어 있는지 확인합니다. 두 번째 인수로 `false`를 전달하지 않는 한, 이 어설션은 지정한 문자열을 자동으로 이스케이프 처리합니다.

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

지정한 문자열들이 응답 내에 순서대로 포함되어 있는지 확인합니다. 두 번째 인수로 `false`를 전달하지 않는 한, 이 어설션은 지정한 문자열들을 자동으로 이스케이프 처리합니다.

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답의 텍스트에 지정한 문자열이 포함되어 있는지 확인합니다. 두 번째 인수로 `false`를 전달하지 않는 한, 이 어설션은 지정한 문자열을 자동으로 이스케이프 처리합니다. 어설션이 실행되기 전에, 응답 내용은 PHP의 `strip_tags` 함수로 태그가 제거됩니다.

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답의 텍스트에 지정한 문자열들이 순서대로 포함되어 있는지 확인합니다. 두 번째 인수로 `false`를 전달하지 않는 한, 이 어설션은 지정한 문자열들을 자동으로 이스케이프 처리합니다. 어설션이 실행되기 전에, 응답 내용은 PHP의 `strip_tags` 함수로 태그가 제거됩니다.

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

응답의 HTTP 상태 코드가 서버 오류(500 이상, 600 미만) 범위인지 확인합니다.

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답의 HTTP 상태 코드가 "Service Unavailable"(503)임을 확인합니다.

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정한 데이터가 존재하는지 확인합니다.

```php
$response->assertSessionHas($key, $value = null);
```

필요하다면, `assertSessionHas` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 어설션은 통과합니다.

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션의 [플래시 입력값 배열](/docs/12.x/responses#redirecting-with-flashed-session-data)에 지정한 값이 존재하는지 확인합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

필요하다면, `assertSessionHasInput` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 어설션은 통과합니다.

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정한 키/값 쌍의 배열 전체가 존재하는지 확인합니다.

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 애플리케이션의 세션에 `name` 및 `status` 키가 포함되어 있다면, 다음과 같이 두 값이 모두 존재하고 특정 값을 가지고 있는지 확인할 수 있습니다.

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 주어진 `$keys`에 대한 에러가 존재하는지 확인합니다. `$keys`가 연관 배열인 경우, 세션에 각 필드(키)에 대해 특정 에러 메시지(값)가 존재하는지 확인합니다. 이 메서드는 유효성 검증 에러가 JSON이 아닌 세션에 플래시되어 저장될 때 경로를 테스트할 때 사용해야 합니다.

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, `name`과 `email` 필드에 대한 유효성 검증 에러 메시지가 세션에 기록되어 있는지 확인하려면, 아래와 같이 `assertSessionHasErrors` 메서드를 사용할 수 있습니다.

```php
$response->assertSessionHasErrors(['name', 'email']);
```

또는, 특정 필드에 특정 에러 메시지가 있는지도 확인할 수 있습니다.

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 범용적인 [assertInvalid](#assert-invalid) 메서드를 사용하면, 응답에 JSON으로 반환된 유효성 검증 에러가 있는지 **또는** 에러가 세션에 저장되어 있는지 모두 확인할 수 있습니다.

<a name="assert-session-has-errors-in"></a>

#### assertSessionHasErrorsIn

특정 [에러 백](/docs/12.x/validation#named-error-bags) 내에서 주어진 `$keys`에 대한 에러가 세션에 포함되어 있는지 확인합니다. 만약 `$keys`가 연관 배열(associative array)이라면, 에러 백 안의 각 필드(키)마다 특정 에러 메시지(값)가 세션에 포함되어 있는지 확인합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 유효성 검증 에러가 없는지 확인합니다.

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

세션에 주어진 키에 대해 유효성 검증 에러가 없는지 확인합니다.

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 좀 더 범용적인 [assertValid](#assert-valid) 메서드는, 응답에 유효성 검증 에러가 JSON 데이터로 반환되지 않았으며 **또한** 에러가 세션에 플래시(flash)되지 않았음을 모두 확인하는 데 사용할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 주어진 키가 존재하지 않는지 확인합니다.

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답에 특정 HTTP 상태 코드가 존재하는지 확인합니다.

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답에 HTTP 성공 상태 코드(200 이상 300 미만)가 존재하는지 확인합니다.

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답에 너무 많은 요청(HTTP 429) 상태 코드가 존재하는지 확인합니다.

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답에 인증되지 않음(HTTP 401) 상태 코드가 존재하는지 확인합니다.

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답에 처리할 수 없음(HTTP 422) 상태 코드가 존재하는지 확인합니다.

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

응답에 지원되지 않는 미디어 타입(HTTP 415) 상태 코드가 존재하는지 확인합니다.

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

주어진 키에 대해 응답에 유효성 검증 에러가 없는지 확인합니다. 이 메서드는 유효성 검증 에러가 JSON 구조로 반환되었거나, 세션에 플래시된 경우 모두를 검증할 때 사용할 수 있습니다.

```php
// 유효성 검증 에러가 없는지 확인합니다...
$response->assertValid();

// 특정 키에 대해 유효성 검증 에러가 없는지 확인합니다...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

주어진 키에 대해 응답에 유효성 검증 에러가 있는지 확인합니다. 이 메서드는 유효성 검증 에러가 JSON 구조로 반환되었거나, 세션에 플래시된 경우 모두를 검증할 때 사용할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

또한, 특정 키에 대해 원하는 유효성 검증 에러 메시지가 포함되어 있는지 확인할 수 있습니다. 이때는 전체 메시지 또는 일부 메시지만을 지정하여 검증이 가능합니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

만약 주어진 필드들만 유효성 검증 에러가 있는지(즉, 이외의 필드는 에러가 없는지) 확인하고 싶다면, `assertOnlyInvalid` 메서드를 사용할 수 있습니다.

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰(view)에 특정 데이터가 포함되어 있는지 확인합니다.

```php
$response->assertViewHas($key, $value = null);
```

`assertViewHas` 메서드의 두 번째 인자로 클로저를 전달하면, 해당 뷰 데이터에 대해 좀 더 세밀하게 검사하거나 커스텀 assertion을 할 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한, 뷰 데이터는 응답(response)에서 배열 변수로 접근할 수 있으므로, 편리하게 값을 확인할 수 있습니다.

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰(view)에 주어진 데이터 목록이 포함되어 있는지 확인합니다.

```php
$response->assertViewHasAll(array $data);
```

이 메서드는 뷰에 특정 키와 일치하는 데이터가 존재하는지만 확인할 때 사용할 수 있습니다.

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

또는, 뷰에 있는 데이터가 실제로 특정한 값을 가지는지 검증할 수도 있습니다.

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

해당 뷰가 해당 라우트에서 반환되었는지 확인합니다.

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

애플리케이션의 응답에서 반환된 뷰에 특정 데이터 키가 포함되어 있지 않은지 확인합니다.

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 관련 Assertion

라라벨은 애플리케이션의 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 assertion 메서드도 제공합니다. 이 메서드들은 `get`이나 `post`와 같이 `Illuminate\Testing\TestResponse` 인스턴스를 반환하는 메서드가 아닌, 테스트 클래스 자체에서 호출된다는 점에 유의하세요.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 확인합니다.

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지(게스트인지) 확인합니다.

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증 상태인지 확인합니다.

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 유효성 검증(Validation) Assertion

라라벨에서는 요청에 전달된 데이터가 유효한지, 아니면 유효성 검증에 실패했는지 확인할 수 있도록 두 가지 주요 assertion 메서드를 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

주어진 키에 대해 응답에 유효성 검증 에러가 없는지 확인합니다. 이 메서드는 유효성 검증 에러가 JSON 구조로 반환된 경우나 세션에 플래시된 경우 모두에서 사용할 수 있습니다.

```php
// 유효성 검증 에러가 없는지 확인합니다...
$response->assertValid();

// 특정 키에 대해 유효성 검증 에러가 없는지 확인합니다...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

주어진 키에 대해 응답에 유효성 검증 에러가 있는지 확인합니다. 이 메서드는 유효성 검증 에러가 JSON 구조로 반환되었거나 세션에 플래시된 경우 모두에서 사용할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

또한, 특정 키에 대해 원하는 유효성 검증 에러 메시지가 포함되어 있는지 확인할 수 있습니다. 이때 전체 메시지 또는 메시지의 일부만 지정할 수도 있습니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```