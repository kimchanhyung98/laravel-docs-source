# HTTP 테스트

- [소개](#introduction)
- [요청 생성하기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [블레이드 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [지원하는 어설션](#available-assertions)
    - [응답 어설션](#response-assertions)
    - [인증 어설션](#authentication-assertions)
    - [검증 어설션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 수행하고 그 응답을 검사할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 아래의 기능 테스트를 살펴보세요:

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

`get` 메서드는 애플리케이션에 `GET` 요청을 수행하며, `assertStatus` 메서드는 반환된 응답이 지정된 HTTP 상태 코드를 가져야 함을 검사합니다. 이 간단한 어설션 외에도, Laravel에는 응답 헤더, 콘텐츠, JSON 구조 등을 검사할 수 있는 다양한 어설션이 포함되어 있습니다.

<a name="making-requests"></a>
## 요청 생성하기

애플리케이션에 요청을 보내려면, 테스트 내에서 `get`, `post`, `put`, `patch`, 또는 `delete` 메서드를 호출하면 됩니다. 이 메서드들은 실제 "HTTP" 요청을 보내는 것이 아니라 네트워크 요청 전체를 내부적으로 시뮬레이션합니다.

`Illuminate\Http\Response` 인스턴스를 반환하는 대신, 테스트 요청 메서드는 `Illuminate\Testing\TestResponse` 인스턴스를 반환하여 [다양한 유용한 어설션](#available-assertions)을 제공해 애플리케이션의 응답을 검사할 수 있습니다:

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

일반적으로 각 테스트에서는 애플리케이션에 한 번만 요청을 보내는 것이 바람직합니다. 하나의 테스트 메서드 내에서 여러 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]  
> 편의를 위해, 테스트를 실행할 때는 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

`withHeaders` 메서드를 사용하여 요청이 애플리케이션에 전달되기 전에 헤더를 커스터마이징할 수 있습니다. 이 메서드는 원하는 모든 커스텀 헤더를 요청에 추가할 수 있도록 해줍니다:

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

`withCookie` 또는 `withCookies` 메서드를 사용하여 요청 전에 쿠키 값을 설정할 수 있습니다. `withCookie` 메서드는 쿠키 이름과 값을 각각 인자로 받고, `withCookies` 메서드는 이름/값 쌍의 배열을 인자로 받습니다:

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

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 다양한 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용하여 세션 데이터를 지정한 배열로 설정할 수 있습니다. 이는 요청을 보내기 전에 세션에 데이터를 미리 저장해두는 데 유용합니다:

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

Laravel 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 그래서 `actingAs` 헬퍼 메서드는 주어진 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용해 사용자를 생성하고 인증할 수 있습니다:

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

`actingAs` 메서드의 두 번째 인자로 가드 이름을 전달하여 어떤 가드를 통해 사용자를 인증할지도 지정할 수 있습니다. 테스트가 진행되는 동안 해당 가드는 기본 가드로 사용됩니다:

    $this->actingAs($user, 'web')

<a name="debugging-responses"></a>
### 응답 디버깅

애플리케이션에 테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 검사하고 디버깅할 수 있습니다:

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

또는 `dd`, `ddHeaders`, `ddSession`, `ddJson` 메서드를 사용하여 응답 정보를 덤프하고 실행을 중지할 수 있습니다:

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
     * A basic test example.
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
### 예외 처리

어플리케이션에서 특정 예외가 발생하는지 테스트해야 할 때가 있습니다. 이를 위해, `Exceptions` 파사드를 통해 예외 핸들러를 "가짜(faking)"로 만들 수 있습니다. 한 번 예외 핸들러가 가짜로 설정되면, 요청 중에 발생한 예외에 대해 `assertReported` 및 `assertNotReported` 메서드를 사용할 수 있습니다:

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

`assertNotReported`와 `assertNothingReported` 메서드는 주어진 예외가 요청 중에 발생하지 않았거나, 어떠한 예외도 발생하지 않았음을 검사할 때 사용할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에 대해 예외 처리를 완전히 비활성화하려면, 요청을 실행하기 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다:

    $response = $this->withoutExceptionHandling()->get('/');

또한, 애플리케이션이 PHP 또는 라이브러리에서 deprecated된 기능을 사용하지 않음을 보장하고 싶다면, 요청 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이 방법은 deprecated 경고를 예외로 변환하여 테스트를 실패하게 만듭니다:

    $response = $this->withoutDeprecationHandling()->get('/');

지정된 클로저 내의 코드가 특정 타입의 예외를 발생시키는지 검사하려면 `assertThrows` 메서드를 사용할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외를 검사하고 추가 어설션을 하고 싶다면, `assertThrows` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API와 그 응답을 테스트할 수 있도록 다양한 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드들은 다양한 HTTP 메서드로 JSON 요청을 쉽게 발송할 수 있습니다. 데이터와 헤더도 간단히 전달할 수 있습니다. 예를 들어, `/api/user`로 `POST` 요청을 보내고 예상한 JSON 데이터가 반환되었는지 검사해보겠습니다:

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

또한, JSON 응답 데이터는 배열 변수처럼 응답에서 바로 접근할 수 있어, 반환된 값을 손쉽게 검사할 수 있습니다:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]  
> `assertJson` 메서드는 응답을 배열로 변환해, 주어진 배열이 애플리케이션의 JSON 응답 내에 존재하는지 검사합니다. 따라서 JSON 응답에 추가 속성이 더 있더라도, 해당 조각(fragment)만 있으면 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### JSON 정확 일치 어설션

앞서 설명했듯이, `assertJson` 메서드는 JSON 응답 내에 지정된 조각이 존재하는지 검사합니다. 만약 반환된 JSON이 주어진 배열과 **정확하게 일치**하는지 확인하고 싶다면, `assertExactJson` 메서드를 사용해야 합니다:

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
#### JSON 경로 어설션

JSON 응답이 특정 경로에 지정된 데이터를 가지고 있는지 확인하려면, `assertJsonPath` 메서드를 사용하세요:

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

`assertJsonPath` 메서드는 클로저도 인자로 받아 어설션의 통과 여부를 동적으로 결정할 수 있습니다:

    $response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);

<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 유창하게 테스트할 수 있는 아름다운 방법도 제공합니다. 이를 시작하려면, `assertJson` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인자로 받아, 반환된 JSON에 대한 어설션을 체이닝 방식으로 진행할 수 있습니다. `where` 메서드는 특정 속성의 값을 검사하고, `missing` 메서드는 특정 속성이 JSON에 없는지 검사합니다:

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

위 예제에서 마지막에 `etc` 메서드가 사용된 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 다른 속성이 더 있을 수 있음을 Laravel에 알리는 역할을 합니다. 만약 `etc` 메서드를 사용하지 않으면, 명시적으로 어설션하지 않은 속성이 JSON 객체에 포함되어 있으면 테스트가 실패하게 됩니다.

이러한 동작의 목적은 민감한 정보가 JSON 응답에 실수로 노출되는 것을 방지하기 위해, 속성에 대해 명시적으로 어설션 하거나 `etc` 메서드를 통해 추가 속성을 허용하도록 강제하는 데 있습니다.

단, `etc` 메서드가 없다 하더라도, 중첩된 배열 안에서 추가 속성이 없는지를 보장하지 않습니다. `etc` 메서드는 해당 레벨의 속성에만 영향을 미칩니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 어설션

속성의 존재 여부를 어설션하려면 `has` 및 `missing` 메서드를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('data')
            ->missing('message')
    );

또한, `hasAll`과 `missingAll` 메서드를 사용하여 여러 속성의 존재/부재를 한 번에 어설션할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->hasAll(['status', 'data'])
            ->missingAll(['message', 'code'])
    );

최소한 하나의 속성이 존재하는지만 검사하려면 `hasAny` 메서드를 사용하세요:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('status')
            ->hasAny('data', 'message', 'code')
    );

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 어설션

라우트가 여러 항목(예: 사용자 여러 명)이 담긴 JSON 응답을 반환할 때가 많습니다:

    Route::get('/users', function () {
        return User::all();
    });

이 경우, 유창한 JSON 객체의 `has` 메서드를 이용해 포함된 사용자 수를 검사할 수 있습니다. 예를 들어, JSON 응답이 3명의 사용자를 포함하고 첫 번째 사용자에 대한 일부 속성을 검사하려면 `first` 메서드를 사용합니다:

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

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어설션 범위 설정

어떤 라우트는 JSON 컬렉션을 명명된 키로 반환합니다:

    Route::get('/users', function () {
        return [
            'meta' => [...],
            'users' => User::all(),
        ];
    })

이런 라우트를 테스트할 때는, `has` 메서드를 사용해 컬렉션 내 항목 수를 어설션하거나, 어설션 체이닝 범위를 스코프할 수 있습니다:

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

`users` 컬렉션에 대해 별도의 `has` 호출을 두 번 하는 대신, 세 번째 인자로 클로저를 전달해서 첫 번째 아이템에 대한 어설션도 한 번에 할 수 있습니다:

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

<a name="asserting-json-types"></a>
#### JSON 타입 어설션

JSON 응답의 속성이 특정 타입인지 검사하고 싶은 경우, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`과 `whereAllType` 메서드를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('id', 'integer')
            ->whereAllType([
                'users.0.name' => 'string',
                'meta' => 'array'
            ])
    );

`|` 문자를 사용하거나 타입 배열을 두 번째 인자로 전달해 여러 타입 중 하나만 맞아도 통과할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('name', 'string|null')
            ->whereType('id', ['string', 'integer'])
    );

인식 가능한 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null` 입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 통해, 테스트용 가짜 파일 또는 이미지를 생성할 수 있습니다. 이를 `Storage` 파사드의 `fake` 메서드와 조합하면 파일 업로드 테스트가 매우 쉬워집니다. 예를 들어, 아바타 업로드 폼을 테스트하려면 다음과 같이 사용합니다:

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

특정 파일이 존재하지 않는지 검사하려면 `Storage` 파사드의 `assertMissing` 메서드를 사용하세요:

    Storage::fake('avatars');

    // ...

    Storage::disk('avatars')->assertMissing('missing.jpg');

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징

`UploadedFile` 클래스의 `fake` 메서드로 파일을 생성할 때, 이미지의 너비/높이/크기(킬로바이트 단위)를 지정하여 애플리케이션의 검증 규칙을 더 잘 테스트할 수 있습니다:

    UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);

이미지 외에도, `create` 메서드를 사용하면 다른 유형의 파일도 생성할 수 있습니다:

    UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);

필요하다면, 파일의 MIME 타입을 세 번째 인자로 명시적으로 지정할 수 있습니다:

    UploadedFile::fake()->create(
        'document.pdf', $sizeInKilobytes, 'application/pdf'
    );

<a name="testing-views"></a>
## 뷰 테스트

Laravel에서는 시뮬레이션된 HTTP 요청 없이도 뷰를 렌더링할 수 있습니다. 이를 위해 테스트 내부에서 `view` 메서드를 호출하세요. `view` 메서드는 뷰 이름과 데이터 배열을 인자로 받아, 다양한 어설션에 편리하게 사용할 수 있는 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

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

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅해서 뷰의 원본 내용을 가져올 수도 있습니다:

    $contents = (string) $this->view('welcome');

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 [글로벌 에러 백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 공유된 에러에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용하세요:

    $view = $this->withViewErrors([
        'name' => ['Please provide a valid name.']
    ])->view('form');

    $view->assertSee('Please provide a valid name.');

<a name="rendering-blade-and-components"></a>
### 블레이드 및 컴포넌트 렌더링

필요시, `blade` 메서드를 사용해 원시 [블레이드](/docs/{{version}}/blade) 문자열을 평가·렌더링 할 수 있습니다. 이 역시 `view` 메서드처럼 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

    $view = $this->blade(
        '<x-component :name="$name" />',
        ['name' => 'Taylor']
    );

    $view->assertSee('Taylor');

`component` 메서드로 [블레이드 컴포넌트](/docs/{{version}}/blade#components)를 평가·렌더링 할 수 있습니다. `component` 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

    $view = $this->component(Profile::class, ['name' => 'Taylor']);

    $view->assertSee('Taylor');

<a name="available-assertions"></a>
## 지원하는 어설션

<a name="response-assertions"></a>
### 응답 어설션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 여러 종류의 맞춤 어설션 메서드를 제공합니다. 이 어설션들은 `json`, `get`, `post`, `put`, `delete` 등의 테스트 메서드로 반환된 응답에서 사용할 수 있습니다:

<!-- 스타일 및 리스트 부분은 그대로 유지 -->

#### assertBadRequest

응답이 잘못된 요청(400) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertBadRequest();

#### assertAccepted

응답이 허용됨(202) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertAccepted();

#### assertConflict

응답이 충돌(409) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertConflict();

#### assertCookie

응답에 지정된 쿠키가 포함되어 있는지 어설션합니다:

    $response->assertCookie($cookieName, $value = null);

#### assertCookieExpired

응답에 지정된 쿠키가 포함되어 있고 만료되었는지 어설션합니다:

    $response->assertCookieExpired($cookieName);

#### assertCookieNotExpired

응답에 지정된 쿠키가 포함되어 있고 만료되지 않았는지 어설션합니다:

    $response->assertCookieNotExpired($cookieName);

#### assertCookieMissing

응답에 지정된 쿠키가 포함되어 있지 않은지 어설션합니다:

    $response->assertCookieMissing($cookieName);

#### assertCreated

응답이 201 HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertCreated();

#### assertDontSee

응답 내에 지정한 문자열이 포함되어 있지 않은지 어설션합니다. 두 번째 인자로 `false`를 전달하면 자동 이스케이프가 비활성화됩니다:

    $response->assertDontSee($value, $escaped = true);

#### assertDontSeeText

응답 텍스트에 지정한 문자열이 포함되어 있지 않은지 어설션합니다. 두 번째 인자로 `false`를 전달하면 자동 이스케이프가 비활성화됩니다. 이 메서드는 어설션 전에 응답 내용을 PHP의 `strip_tags` 함수로 처리합니다:

    $response->assertDontSeeText($value, $escaped = true);

#### assertDownload

응답이 "다운로드" 형태인지 어설션합니다 (`Response::download` 또는 `BinaryFileResponse`, `Storage::download` 반환 시):

    $response->assertDownload();

다운로드 파일명이 지정한 값과 일치하는지도 어설션할 수 있습니다:

    $response->assertDownload('image.jpg');

#### assertExactJson

응답이 제공된 JSON 데이터와 정확히 일치하는지 어설션합니다:

    $response->assertExactJson(array $data);

#### assertExactJsonStructure

응답이 제공된 JSON 구조와 정확하게 일치하는지 어설션합니다:

    $response->assertExactJsonStructure(array $data);

이 메서드는 [assertJsonStructure](#assert-json-structure)의 더 엄격한 버전으로, 응답에 예상 구조에 명시적으로 포함되지 않은 키가 있으면 실패합니다.

#### assertForbidden

응답이 금지됨(403) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertForbidden();

#### assertFound

응답이 찾음(302) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertFound();

#### assertGone

응답이 없어짐(410) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertGone();

#### assertHeader

응답에 지정한 헤더와 값이 포함되어 있는지 어설션합니다:

    $response->assertHeader($headerName, $value = null);

#### assertHeaderMissing

응답에 지정한 헤더가 포함되어 있지 않은지 어설션합니다:

    $response->assertHeaderMissing($headerName);

#### assertInternalServerError

응답이 "내부 서버 오류"(500) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertInternalServerError();

#### assertJson

응답이 지정한 JSON 데이터를 포함하고 있는지 어설션합니다:

    $response->assertJson(array $data, $strict = false);

`assertJson` 메서드는 응답을 배열로 변환하여, 주어진 배열이 애플리케이션의 JSON 응답 내에 포함되어 있는지 검사합니다. 추가 속성이 있어도 해당 조각이 존재하면 통과합니다.

#### assertJsonCount

응답 JSON이 지정한 키의 배열 항목 수를 정확히 가지는지 어설션합니다:

    $response->assertJsonCount($count, $key = null);

#### assertJsonFragment

응답 어디에든 지정한 JSON 데이터가 포함되어 있는지 어설션합니다.

#### assertJsonIsArray

응답 JSON이 배열인지 어설션합니다:

    $response->assertJsonIsArray();

#### assertJsonIsObject

응답 JSON이 객체인지 어설션합니다:

    $response->assertJsonIsObject();

#### assertJsonMissing

응답이 제공된 JSON 데이터를 포함하지 않는지 어설션합니다:

    $response->assertJsonMissing(array $data);

#### assertJsonMissingExact

응답이 제공된 JSON 데이터와 정확히 일치하는 부분을 포함하지 않는지 어설션합니다:

    $response->assertJsonMissingExact(array $data);

#### assertJsonMissingValidationErrors

응답이 지정한 키에 대해 JSON 검증 에러가 없는지 어설션합니다:

    $response->assertJsonMissingValidationErrors($keys);

> [!NOTE]  
> 더 일반적인 [assertValid](#assert-valid) 메서드를 사용하면 JSON과 세션 스토리지로 플래시된 에러가 모두 없는지 한 번에 검사할 수 있습니다.

#### assertJsonPath

응답이 지정한 경로에 해당 값이 정확히 존재하는지 어설션합니다:

    $response->assertJsonPath($path, $expectedValue);

#### assertJsonMissingPath

응답이 지정한 경로를 포함하지 않는지 어설션합니다:

    $response->assertJsonMissingPath($path);

#### assertJsonStructure

응답이 주어진 JSON 구조를 가지는지 어설션합니다:

    $response->assertJsonStructure(array $structure);

배열에 포함된 객체의 구조를 어설션할 때는 `*` 를 사용할 수 있습니다.

#### assertJsonValidationErrors

응답이 지정한 키에 대해 JSON 검증 에러를 포함하는지 어설션합니다. 이 메서드는 검증 에러가 JSON 구조로 반환될 때 사용합니다:

    $response->assertJsonValidationErrors(array $data, $responseKey = 'errors');

> [!NOTE]  
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드는 JSON 또는 세션 플래시 모두에 대한 검증 에러 검사에 사용할 수 있습니다.

#### assertJsonValidationErrorFor

지정한 키에 대해 어떤 JSON 검증 에러가 있는지 어설션합니다:

    $response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');

#### assertMethodNotAllowed

응답이 허용되지 않은 메서드(405) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertMethodNotAllowed();

#### assertMovedPermanently

응답이 영구 이동(301) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertMovedPermanently();

#### assertLocation

응답의 `Location` 헤더가 지정된 URI 값을 가지는지 어설션합니다:

    $response->assertLocation($uri);

#### assertContent

응답 내용이 지정한 문자열과 일치하는지 어설션합니다:

    $response->assertContent($value);

#### assertNoContent

응답이 지정된 HTTP 상태 코드를 가지고, 콘텐츠가 없는지 어설션합니다:

    $response->assertNoContent($status = 204);

#### assertStreamed

응답이 스트림 응답인지 어설션합니다:

    $response->assertStreamed();

#### assertStreamedContent

스트림 응답 내용이 지정한 문자열과 일치하는지 어설션합니다:

    $response->assertStreamedContent($value);

#### assertNotFound

응답이 찾을 수 없음(404) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertNotFound();

#### assertOk

응답이 200 HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertOk();

#### assertPaymentRequired

응답이 결제 필요(402) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertPaymentRequired();

#### assertPlainCookie

응답에 암호화되지 않은(평문) 쿠키가 포함되어 있는지 어설션합니다:

    $response->assertPlainCookie($cookieName, $value = null);

#### assertRedirect

응답이 지정 URI로 리디렉션되는지 어설션합니다:

    $response->assertRedirect($uri = null);

#### assertRedirectContains

응답의 리디렉션 URI에 지정 문자열이 포함되는지 어설션합니다:

    $response->assertRedirectContains($string);

#### assertRedirectToRoute

응답이 지정된 [이름 있는 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션되는지 어설션합니다:

    $response->assertRedirectToRoute($name, $parameters = []);

#### assertRedirectToSignedRoute

응답이 지정된 [서명된 라우트](/docs/{{version}}/urls#signed-urls)로 리디렉션되는지 어설션합니다:

    $response->assertRedirectToSignedRoute($name = null, $parameters = []);

#### assertRequestTimeout

응답이 요청 시간 초과(408) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertRequestTimeout();

#### assertSee

응답 내에 지정한 문자열이 포함되어 있는지 어설션합니다. 두 번째 인자로 `false`를 전달하면 자동 이스케이프가 비활성화됩니다:

    $response->assertSee($value, $escaped = true);

#### assertSeeInOrder

응답 내에 여러 문자열이 지정한 순서대로 포함되어 있는지 어설션합니다. 두 번째 인자로 `false`를 전달하면 자동 이스케이프가 비활성화됩니다:

    $response->assertSeeInOrder(array $values, $escaped = true);

#### assertSeeText

응답 텍스트 내에 지정한 문자열이 포함되어 있는지 어설션합니다. 두 번째 인자로 `false`를 전달하면 자동 이스케이프가 비활성화됩니다. 응답 내용은 `strip_tags` 처리 후 어설션됩니다:

    $response->assertSeeText($value, $escaped = true);

#### assertSeeTextInOrder

응답 텍스트 내에 여러 문자열이 지정한 순서대로 포함되어 있는지 어설션합니다. 두 번째 인자로 `false`를 전달하면 자동 이스케이프가 비활성화됩니다. 응답 내용은 `strip_tags` 처리 후 어설션됩니다:

    $response->assertSeeTextInOrder(array $values, $escaped = true);

#### assertServerError

응답이 서버 오류(>= 500, < 600) 상태 코드를 가졌는지 어설션합니다:

    $response->assertServerError();

#### assertServiceUnavailable

응답이 "서비스 이용 불가"(503) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertServiceUnavailable();

#### assertSessionHas

세션에 지정된 데이터가 포함되어 있는지 어설션합니다:

    $response->assertSessionHas($key, $value = null);

두 번째 인자로 클로저를 전달해 조건 검사도 가능합니다:

    $response->assertSessionHas($key, function (User $value) {
        return $value->name === 'Taylor Otwell';
    });

#### assertSessionHasInput

세션의 [플래시된 입력 데이터](/docs/{{version}}/responses#redirecting-with-flashed-session-data)에 지정된 값이 있는지 어설션합니다:

    $response->assertSessionHasInput($key, $value = null);

클로저를 두 번째 인자로 전달할 수 있습니다:

    use Illuminate\Support\Facades\Crypt;

    $response->assertSessionHasInput($key, function (string $value) {
        return Crypt::decryptString($value) === 'secret';
    });

#### assertSessionHasAll

세션이 주어진 키/값 쌍 배열을 모두 포함하고 있는지 어설션합니다:

    $response->assertSessionHasAll(array $data);

예시:

    $response->assertSessionHasAll([
        'name' => 'Taylor Otwell',
        'status' => 'active',
    ]);

#### assertSessionHasErrors

세션에 주어진 `$keys`에 대한 에러가 있는지 어설션합니다. `$keys`가 연관 배열일 경우 각 필드(키)에 대해 특정 에러 메시지(값)가 있는지 확인합니다. 이 메서드는 검증 에러가 세션으로 플래시될 때 사용할 수 있습니다:

    $response->assertSessionHasErrors(
        array $keys = [], $format = null, $errorBag = 'default'
    );

필드별 특정 에러 메시지만 검사하기도 가능합니다:

    $response->assertSessionHasErrors([
        'name' => 'The given name was invalid.'
    ]);

> [!NOTE]  
> [assertInvalid](#assert-invalid) 메서드는 JSON 또는 세션 플래시 모두에 대해 검증 에러를 어설션할 수 있습니다.

#### assertSessionHasErrorsIn

지정된 [에러 백](/docs/{{version}}/validation#named-error-bags) 내에서 특정 에러가 존재하는지 어설션합니다.

    $response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);

#### assertSessionHasNoErrors

세션에 검증 에러가 없는지 어설션합니다:

    $response->assertSessionHasNoErrors();

#### assertSessionDoesntHaveErrors

세션에 주어진 키에 대한 검증 에러가 없는지 어설션합니다:

    $response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');

> [!NOTE]  
> 더 일반적인 [assertValid](#assert-valid) 메서드 참고.

#### assertSessionMissing

세션에 주어진 키가 포함되지 않았는지 어설션합니다:

    $response->assertSessionMissing($key);

#### assertStatus

응답이 지정된 HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertStatus($code);

#### assertSuccessful

응답이 성공적인(>= 200, < 300) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertSuccessful();

#### assertTooManyRequests

응답이 과도한 요청(429) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertTooManyRequests();

#### assertUnauthorized

응답이 인증되지 않음(401) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertUnauthorized();

#### assertUnprocessable

응답이 처리 불가(422) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertUnprocessable();

#### assertUnsupportedMediaType

응답이 지원하지 않는 미디어 타입(415) HTTP 상태 코드를 가졌는지 어설션합니다:

    $response->assertUnsupportedMediaType();

#### assertValid

응답에 특정 키에 대한 검증 에러가 없는지 어설션합니다. 본 메서드는 JSON 또는 세션 플래시 모두를 대상으로 사용할 수 있습니다:

    // 검증 에러가 모두 없는지 검사
    $response->assertValid();

    // 주어진 키에 검증 에러가 없는지 검사
    $response->assertValid(['name', 'email']);

#### assertInvalid

응답에 특정 키에 대한 검증 에러가 존재하는지 어설션합니다. 본 메서드는 JSON 또는 세션 플래시 모두를 대상으로 사용할 수 있습니다:

    $response->assertInvalid(['name', 'email']);

특정 에러 메시지로 검사할 수도 있습니다:

    $response->assertInvalid([
        'name' => 'The name field is required.',
        'email' => 'valid email address',
    ]);

#### assertViewHas

응답 뷰가 특정 데이터 조각을 포함하고 있는지 어설션합니다:

    $response->assertViewHas($key, $value = null);

두 번째 인자로 클로저를 전달하면 뷰 데이터 조각을 검사할 수 있습니다:

    $response->assertViewHas('user', function (User $user) {
        return $user->name === 'Taylor';
    });

뷰 데이터에 배열 변수로 접근 가능하므로, 바로 검사가 가능합니다:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

#### assertViewHasAll

응답 뷰에 데이터가 모두 있는지 어설션합니다:

    $response->assertViewHasAll(array $data);

키만 검사하거나, 키와 값을 모두 검사할 수도 있습니다.

#### assertViewIs

지정한 뷰가 반환되었는지 어설션합니다:

    $response->assertViewIs($value);

#### assertViewMissing

응답 뷰에 특정 데이터 키가 포함되어 있지 않은지 어설션합니다:

    $response->assertViewMissing($key);

<a name="authentication-assertions"></a>
### 인증 어설션

Laravel은 기능 테스트에서 사용할 수 있는 다양한 인증 관련 어설션도 제공합니다. 이 메서드들은 테스트 클래스 자체에서 호출하며, `json`, `get`, `post` 등에서 반환된 `Illuminate\Testing\TestResponse` 인스턴스에서는 사용하지 않습니다.

#### assertAuthenticated

특정 사용자가 인증되었는지 어설션합니다:

    $this->assertAuthenticated($guard = null);

#### assertGuest

사용자가 인증되지 않았는지 어설션합니다:

    $this->assertGuest($guard = null);

#### assertAuthenticatedAs

특정 사용자가 인증되었는지 어설션합니다:

    $this->assertAuthenticatedAs($user, $guard = null);

<a name="validation-assertions"></a>
## 검증 어설션

Laravel은 요청에 제공된 데이터가 유효 또는 무효임을 보장하기 위한 두 가지 검증 관련 어설션을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답이 제공된 키에 대한 검증 에러가 없는지 어설션합니다. 본 메서드는 JSON 또는 세션 플래시에 대해 모두 사용할 수 있습니다:

    // 검증 에러가 전혀 없는지 검사
    $response->assertValid();

    // 주어진 키에 검증 에러가 없는지 검사
    $response->assertValid(['name', 'email']);

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답이 제공된 키에 대한 검증 에러를 포함하는지 어설션합니다. 본 메서드는 JSON 또는 세션 플래시에 대해 모두 사용할 수 있습니다:

    $response->assertInvalid(['name', 'email']);

특정 키에 대해 특정 에러 메시지가 포함되었는지 검사할 수도 있습니다(전체 메시지 또는 일부만 제공 가능):

    $response->assertInvalid([
        'name' => 'The name field is required.',
        'email' => 'valid email address',
    ]);
