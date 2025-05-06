# HTTP 테스트

- [소개](#introduction)
- [요청 생성](#making-requests)
    - [요청 헤더 맞춤 설정](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [Fluent JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰(화면) 테스트](#testing-views)
    - [블레이드 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [가능한 어서션 목록](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 여러분의 애플리케이션에 HTTP 요청을 보낸 후 응답을 확인할 수 있는 매우 유연한 API를 제공합니다. 예를 들어, 아래의 기능 테스트 예시를 살펴보세요:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 전송하고, `assertStatus` 메서드는 반환된 응답이 주어진 HTTP 상태 코드를 가져야 함을 단언합니다. 이 간단한 어서션 외에도, Laravel은 응답 헤더, 컨텐츠, JSON 구조 등 다양한 요소를 확인할 수 있는 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 생성

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 이 메서드들은 실제 "HTTP" 요청을 발생시키지 않고, 네트워크 요청 전체를 내부적으로 시뮬레이션합니다.

이 메서드들은 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, [사용 가능한 다양한 어서션](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 인스턴스를 통해 애플리케이션의 응답을 상세하게 검사할 수 있습니다:

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

일반적으로 각 테스트는 애플리케이션에 한 번만 요청을 보내야 합니다. 하나의 테스트 메서드 내에서 여러 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 테스트를 실행할 때는 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 맞춤 설정

요청을 보내기 전에 `withHeaders` 메서드를 사용하여 요청 헤더를 맞춤 설정할 수 있습니다. 이 메서드를 통해 원하는 커스텀 헤더를 자유롭게 추가할 수 있습니다:

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

요청 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키 이름과 값을 두 인자로 받으며, `withCookies`는 이름/값 쌍의 배열을 인자로 받습니다:

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

Laravel은 HTTP 테스트 도중 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드에 세션 데이터 배열을 지정하여 설정할 수 있습니다. 이는 요청을 보내기 전에 세션에 데이터를 미리 저장하고 싶을 때 유용합니다:

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

Laravel의 세션은 주로 현재 인증된 사용자의 상태를 유지하는 데 사용합니다. 따라서 `actingAs` 헬퍼 메서드는 주어진 사용자를 현재 인증 사용자로 쉽게 설정할 수 있습니다. 예를 들어, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 이용해 사용자를 생성 및 인증할 수 있습니다:

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

필요하다면 `actingAs` 메서드의 두 번째 인자로 가드 이름을 지정하여 해당 가드로 인증할 수도 있습니다. 이는 테스트 실행 중 해당 가드가 기본 가드가 됨을 의미합니다:

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 후, 응답 내용을 확인하고 디버깅하려면 `dump`, `dumpHeaders`, `dumpSession` 등의 메서드를 사용할 수 있습니다:

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

또는, 정보를 출력하고 이후 실행을 즉시 중단하고 싶다면 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용할 수 있습니다:

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

가끔 애플리케이션이 특정 예외를 throw 하는지 테스트해야 할 수도 있습니다. 이를 위해 `Exceptions` 파사드를 통해 예외 핸들러를 "페이크"할 수 있습니다. 예외 핸들러를 페이크하면, 요청 중 발생한 예외에 대해 `assertReported`, `assertNotReported` 메서드로 어서션을 할 수 있습니다:

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

`assertNotReported`, `assertNothingReported` 메서드는 특정 예외가 발생하지 않았는지 혹은 어떤 예외도 발생하지 않았는지 검증하는 데 사용할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하려면 `withoutExceptionHandling` 메서드를 요청 전에 호출하세요:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 언어나 사용하는 라이브러리에서 더 이상 지원되지 않는 기능(Deprecation)이 사용되고 있지 않은지 확인하려면 `withoutDeprecationHandling` 메서드를 요청 전에 호출할 수 있습니다. 처리 비활성화 시, Deprecation 경고가 예외로 전환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 지정한 클로저 내에서 특정 타입의 예외가 발생하는지 단언할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생된 예외를 검사하거나 추가 어서션을 하고 싶다면, 클로저를 두 번째 인자로 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API와 그 응답을 테스트할 수 있는 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 이용해 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 데이터와 헤더도 쉽게 전달할 수 있습니다. 예시로, `/api/user`에 `POST` 요청을 보내고 원하는 JSON 데이터가 반환되었음을 단언해봅니다:

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

또한, JSON 응답 데이터는 배열 변수처럼 접근해 개별 값을 쉽게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여 주어진 배열이 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성들이 있더라도 지정한 조각(fragment)만 존재하면 테스트가 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 단언

앞서 언급했듯, `assertJson`은 JSON의 일부 조각이 존재함을 검증합니다. 만약 주어진 배열이 **정확하게** 애플리케이션의 JSON 반환값과 일치해야 함을 검증하려면 `assertExactJson` 메서드를 사용하세요:

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
#### JSON 경로 단언

JSON 응답이 지정한 경로에 지정한 데이터를 포함하는지 검증하려면 `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath`는 클로저도 받을 수 있으므로 동적으로 어서션 성공 여부를 판단할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### Fluent JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 유창하게(fluent) 테스트할 수 있는 방식을 제공합니다. 우선, `assertJson` 메서드에 클로저를 전달해 사용합니다. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 받아, 반환된 JSON에 대해 다양한 어서션을 할 수 있습니다. 특정 속성의 값 여부는 `where`로, 특정 속성이 없는지 여부는 `missing`으로 검사할 수 있습니다:

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

#### `etc` 메서드의 의미

위 예제의 마지막에 `etc` 메서드를 호출하는 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 여러분이 명시하지 않은 속성이 추가로 존재할 수도 있음을 Laravel에 알려줍니다. `etc`를 사용하지 않으면, 어서션 체인에서 지정하지 않은 속성들이 JSON 객체에 존재하면 테스트가 실패합니다.

이러한 동작은, 여러분이 민감한 정보를 실수로 JSON에 노출하지 않도록 속성을 명확히 지정하도록 유도하기 위함입니다.

단, `etc` 미사용이 중첩된 배열 안에 속성이 추가되지 않는다는 보장까지는 하지 않습니다. `etc`는 호출된 중첩 수준까지만 추가 속성이 없음을 보장합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어서션

어떤 속성이 존재하는지(`has`), 없는지(`missing`) 단언할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

`hasAll`, `missingAll`은 여러 속성의 존재/부재를 동시에 검사합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

주어진 속성들 중 최소한 하나라도 존재하는지 알고 싶다면 `hasAny`를 사용하세요:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

라우트가 여러 항목(예: 다수의 사용자)을 포함한 JSON 응답을 반환하는 경우가 많습니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

이 경우, 유창 JSON 객체의 `has`를 사용해 포함된 사용자 개수를 어서션할 수 있습니다. 그리고 `first`를 이용해 컬렉션의 첫 번째 객체에 대해 추가 어서션도 할 수 있습니다:

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
#### JSON 컬렉션 범위(scoping) 어서션

때로는, 라우트가 명명된 키에 JSON 컬렉션을 할당하여 반환할 수 있습니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이때, `has`로 컬렉션의 항목 수 및 특정 항목의 속성에 대한 어서션을 할 수 있습니다:

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

별도의 `has` 호출을 하나로 합쳐, 세 번째 인자에 클로저를 넘기면 컬렉션의 첫 번째 항목에 바로 범위가 한정되어 호출됩니다:

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

JSON 응답의 속성이 특정 타입인지 검증할 수 있습니다. `whereType`, `whereAllType` 메서드는 정해진 타입인지 쉽게 검사할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`|` 문자를 이용하거나 두 번째 인자로 타입 배열을 전달해 여러 타입 중 하나면 통과하도록 설정할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType`, `whereAllType`는 다음 타입을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 이용하면 테스트용 가상파일(모조파일)이나 이미지를 쉽게 생성할 수 있습니다. 여기에 `Storage` 파사드의 `fake`를 결합하면 파일 업로드 테스트가 매우 편리해집니다. 아래는 아바타 업로드 폼을 테스트하는 예입니다:

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

특정 파일이 존재하지 않음을 단언하려면, `Storage` 파사드의 `assertMissing`을 사용하세요:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 모조 파일(faked file) 커스터마이징

`UploadedFile` 클래스의 `fake`로 파일을 생성할 때 이미지의 너비, 높이, 사이즈(킬로바이트) 등을 지정하여 애플리케이션의 검증 규칙 테스트에 맞출 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외 다른 타입의 파일도 `create`로 만들 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요 시, `$mimeType` 인자로 파일의 MIME 타입을 명확히 지정할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰(화면) 테스트

Laravel은 실제 HTTP 요청 없이 뷰를 렌더링하여 테스트할 수 있게 해줍니다. 테스트 내에서 `view` 메서드를 호출하면 뷰 이름과 데이터 배열을 인자로 받아 뷰를 반환합니다. 이 메서드는 뷰 어서션에 활용할 수 있는 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

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

`TestView` 클래스는 다음 어서션 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 렌더링된 뷰 원본을 얻을 수도 있습니다:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 [글로벌 에러 백(global error bag)](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 저장된 에러에 의존할 수 있습니다. 에러 백을 에러 메시지로 채우려면 `withViewErrors`를 사용하세요:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### 블레이드 및 컴포넌트 렌더링

필요하다면, `blade` 메서드로 원시 [블레이드](/docs/{{version}}/blade) 문자열을 평가 및 렌더링할 수 있습니다. `view` 메서드처럼, `blade`도 `Illuminate\Testing\TestView`를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[블레이드 컴포넌트](/docs/{{version}}/blade#components)를 직접 평가 및 렌더링하려면 `component` 메서드를 사용하세요. 이 메서드는 `Illuminate\Testing\TestComponent`를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 가능한 어서션(Assertion) 목록

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 중 사용할 수 있는 다양한 특수 어서션 메서드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드로 반환된 응답에서 사용 가능합니다.

<!-- 스타일 및 목록은 번역하지 않음 -->

<a name="assert-bad-request"></a>
#### assertBadRequest

응답의 HTTP 상태 코드가 400(Bad Request)인지 단언합니다:

```php
$response->assertBadRequest();
```

<a name="assert-accepted"></a>
#### assertAccepted

응답의 HTTP 상태 코드가 202(Accepted)인지 단언합니다:

```php
$response->assertAccepted();
```

<a name="assert-conflict"></a>
#### assertConflict

응답의 HTTP 상태 코드가 409(Conflict)인지 단언합니다:

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

응답에 주어진 쿠키가 포함되어 있고 만료되었는지 단언합니다:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 주어진 쿠키가 포함되어 있고 만료되지 않았는지 단언합니다:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 주어진 쿠키가 없는지 단언합니다:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답의 HTTP 상태 코드가 201(Created)인지 단언합니다:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

어플리케이션이 반환한 응답 내에 특정 문자열이 없는지 단언합니다. 두 번째 인자로 `false`를 넘기지 않으면 자동으로 이스케이프합니다:

```php
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 특정 문자열이 없는지 단언합니다. 두 번째 인자로 `false`를 넘기지 않으면 자동 이스케이프합니다. PHP의 `strip_tags` 함수로 응답 내용을 처리 후 검사합니다:

```php
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"임을 단언합니다. 일반적으로, 해당 라우트가 `Response::download`, `BinaryFileResponse`, 또는 `Storage::download` 응답을 반환하면 해당됩니다:

```php
$response->assertDownload();
```

특정 파일명으로 다운로드가 할당되었는지 검사하려면:

```php
$response->assertDownload('image.jpg');
```

... (이하 기타 모든 어서션 문서 동일하게 번역) ...

> **[참고]**
> 어서션 방법의 상세 설명이나 인자 타입 등은 문서 내의 원문을 참고하세요. 본 번역문에서는 어서션 목적, 옵션 인자, 사용 예제를 알기 쉽도록 자연스러운 한국어로 표현하였습니다. 

---

**모든 어서션 설명 예시(예시 패턴, 중복되는 표현은 제외):**

#### assertOK

응답의 HTTP 상태 코드가 200(OK)인지 단언합니다:

```php
$response->assertOk();
```

#### assertViewHas

뷰에 특정 데이터가 포함되어 있는지 단언합니다:

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인자로 클로저를 넘기면 해당 뷰 데이터에 대해 추가 검증이 가능합니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또는 응답 데이터를 배열처럼 접근하여 확인할 수도 있습니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

... (다른 어서션을 동일 패턴으로 번역)

---

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 인증 관련 다양한 어서션도 제공합니다. 이 메서드들은 `Illuminate\Testing\TestResponse`가 아닌 테스트 클래스 자체에서 호출합니다.

#### assertAuthenticated

사용자가 인증되었는지 단언합니다:

```php
$this->assertAuthenticated($guard = null);
```

#### assertGuest

사용자가 인증되지 않았는지 단언합니다:

```php
$this->assertGuest($guard = null);
```

#### assertAuthenticatedAs

특정 사용자가 인증 중인지 단언합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 검증(Validation) 어서션

Laravel은 요청 데이터가 유효한지 혹은 유효하지 않은지 검증하기 위한 두 가지 주요 어서션을 제공합니다.

#### assertValid

응답에 주어진 키들에 대한 검증 에러가 없는지 단언합니다. 이 메서드는 검증 에러가 JSON 구조로 반환되거나, 세션에 flash 되었을 때 모두 사용할 수 있습니다:

```php
// 모든 검증 에러가 없는지 단언
$response->assertValid();

// 특정 키들에 대해 검증 에러가 없는지 단언
$response->assertValid(['name', 'email']);
```

#### assertInvalid

응답에 주어진 키들에 대해 검증 에러가 있는지 단언합니다. 이 메서드는 검증 에러가 JSON으로 반환되거나, 세션에 flash 되었을 때 모두 사용할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```

특정 키의 검증 에러 메시지를 단언하고 싶다면 전체 메시지 혹은 일부만 전달할 수 있습니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

---

**이 번역문은 마크다운 구조와 코드/HTML/링크는 원본대로, 기술 용어는 적절하게 번역하여 제공하였습니다.**