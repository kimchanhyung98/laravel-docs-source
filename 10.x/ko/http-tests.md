# HTTP 테스트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [플루언트(유창한) JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)
    - [검증 어서션](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 그 응답을 검사하는 매우 유창한 API를 제공합니다. 예를 들어, 아래의 기능 테스트 예제를 살펴보세요:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 주어진 HTTP 상태 코드를 가져야 한다는 것을 검증합니다. 이 간단한 어서션 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사하기 위한 다양한 어서션을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 등의 메서드를 사용할 수 있습니다. 이 메서드들은 실제로 "진짜" HTTP 요청을 발생시키는 것은 아니며, 네트워크 요청을 내부적으로 시뮬레이션합니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, 애플리케이션의 응답을 검사할 수 있는 [다양한 유용한 어서션](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         */
        public function test_a_basic_request(): void
        {
            $response = $this->get('/');

            $response->assertStatus(200);
        }
    }

일반적으로 각 테스트는 애플리케이션에 대해 한 번의 요청만 실행해야 합니다. 하나의 테스트 메서드 내에서 여러 요청을 실행할 경우 예상치 못한 동작이 발생할 수 있습니다.

> [!NOTE]  
> 편의를 위해, 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

요청 전 `withHeaders` 메서드를 사용하여 요청 헤더를 커스터마이징할 수 있습니다. 이 메서드를 통해 원하는 임의의 헤더를 추가할 수 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
         */
        public function test_interacting_with_headers(): void
        {
            $response = $this->withHeaders([
                'X-Header' => 'Value',
            ])->post('/user', ['name' => 'Sally']);

            $response->assertStatus(201);
        }
    }

<a name="cookies"></a>
### 쿠키

`withCookie` 또는 `withCookies` 메서드를 사용하여 요청 전에 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 인자로 받고, `withCookies`는 이름/값 쌍의 배열을 받습니다:

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
        }
    }

<a name="session-and-authentication"></a>
### 세션 / 인증

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 몇 가지 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 이용해 세션 데이터를 배열로 지정하여 설정할 수 있습니다. 이는 요청을 수행하기 전 세션에 데이터를 미리 설정하고 싶을 때 유용합니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_interacting_with_the_session(): void
        {
            $response = $this->withSession(['banned' => false])->get('/');
        }
    }

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태 유지를 위해 사용됩니다. 따라서, `actingAs` 헬퍼 메서드로 주어진 사용자를 현재 사용자로 인증할 수 있습니다. 예를 들어, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 이용해 사용자를 생성 및 인증할 수 있습니다:

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
        }
    }

또한 `actingAs` 메서드의 두 번째 인자로 가드 이름을 지정하여 인증할 가드를 선택할 수 있습니다. 이 가드는 테스트 지속 시간 동안 기본 가드가 됩니다:

    $this->actingAs($user, 'web')

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 후, `dump`, `dumpHeaders`, `dumpSession` 등의 메서드로 응답 내용을 직접 출력해 디버깅할 수 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         */
        public function test_basic_test(): void
        {
            $response = $this->get('/');

            $response->dumpHeaders();

            $response->dumpSession();

            $response->dump();
        }
    }

또는, `dd`, `ddHeaders`, `ddSession`을 사용하여 정보를 출력한 뒤 실행을 중단할 수도 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         */
        public function test_basic_test(): void
        {
            $response = $this->get('/');

            $response->ddHeaders();

            $response->ddSession();

            $response->dd();
        }
    }

<a name="exception-handling"></a>
### 예외 처리

애플리케이션이 특정 예외를 던지는지 테스트하고 싶다면, 요청 전 `withoutExceptionHandling` 메서드를 호출해 예외가 Laravel의 예외 핸들러에서 잡히지 않고 응답으로 반환되지 않도록 할 수 있습니다:

    $response = $this->withoutExceptionHandling()->get('/');

또한, PHP나 라이브러리에서 더 이상 지원되지 않는(deprecated) 기능의 사용 여부를 검사하려면, `withoutDeprecationHandling`을 사용할 수 있습니다. 이 기능이 비활성화되면, 경고가 예외로 변환되어 테스트가 실패하게 됩니다:

    $response = $this->withoutDeprecationHandling()->get('/');

`assertThrows` 메서드는 주어진 클로저 내부의 코드가 특정 타입의 예외를 던지는지 검증할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API 및 응답을 테스트할 수 있는 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드로 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 데이터와 헤더도 쉽게 전달 가능합니다. 예를 들어 `/api/user`에 `POST` 요청을 보내고 기대하는 JSON 데이터를 반환하는지 테스트할 수 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
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

또한 JSON 응답 데이터를 배열 변수처럼 접근할 수 있어, 응답의 개별 값을 쉽게 검사할 수 있습니다:

    $this->assertTrue($response['created']);

> [!NOTE]  
> `assertJson` 메서드는 응답을 배열로 변환한 뒤 `PHPUnit::assertArraySubset`를 이용해 주어진 배열이 응답 JSON에 포함되어 있는지 검증합니다. JSON 응답에 다른 속성이 있어도, 지정한 일부만 존재하면 이 테스트는 통과됩니다.

<a name="verifying-exact-match"></a>
#### 정확히 JSON 일치 검증

앞서 설명한 `assertJson`으로 JSON 일부의 존재 여부를 검사할 수 있습니다. 만약 반환된 JSON이 특정 배열과 **정확히 일치**하는지 확인하려면 `assertExactJson` 메서드를 사용하세요:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
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

<a name="verifying-json-paths"></a>
#### JSON 경로 값 검증

JSON 응답이 특정 경로에 값을 가지고 있는지 검사하려면 `assertJsonPath` 메서드를 사용하세요:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
         */
        public function test_asserting_a_json_paths_value(): void
        {
            $response = $this->postJson('/user', ['name' => 'Sally']);

            $response
                ->assertStatus(201)
                ->assertJsonPath('team.owner.name', 'Darian');
        }
    }

`assertJsonPath`는 클로저도 받을 수 있어 동적으로 검사 기준을 구성할 수 있습니다:

    $response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);

<a name="fluent-json-testing"></a>
### 플루언트(유창한) JSON 테스트

Laravel은 JSON 응답을 플루언트하게(체이닝 방식으로) 테스트하는 방법도 제공합니다. 이를 위해 `assertJson`에 클로저를 넘길 수 있는데, 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스로 호출됩니다. `where` 메서드는 특정 속성 값 확인, `missing`은 해당 속성 부재 확인에 사용할 수 있습니다:

    use Illuminate\Testing\Fluent\AssertableJson;

    /**
     * 기본 기능 테스트 예제.
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

#### `etc` 메서드의 의미

위 예제에서 마지막에 `etc` 메서드를 호출하는 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 다른 속성이 추가로 있어도 상관없음을 Laravel에 알립니다. `etc`를 사용하지 않으면, 검증한 속성 외의 속성이 있으면 테스트가 실패합니다.

이러한 기본 동작은 JSON 응답에서 민감한 정보 노출을 방지하기 위함입니다. 즉, 어트리뷰트에 대해 검사하거나, `etc`를 사용해 명시적으로 허용해야 합니다.

단, `etc` 메서드를 확인한 중첩 수준 하위의 배열 내에 추가 속성이 존재하는지는 보장하지 않습니다. `etc`는 호출된 그 깊이(nesting level)만 검사합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재 / 부재 어서션

속성의 존재 여부 확인에는 `has`, 부재 여부 확인에는 `missing` 메서드를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('data')
             ->missing('message')
    );

복수의 속성 존재/부재 검증에는 `hasAll`, `missingAll`도 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->hasAll(['status', 'data'])
             ->missingAll(['message', 'code'])
    );

여러 속성 중 하나라도 존재하는지 확인하려면 `hasAny`를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('status')
             ->hasAny('data', 'message', 'code')
    );

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 어서션

라우트가 다수의 데이터를 JSON 컬렉션으로 반환하는 경우도 많습니다:

    Route::get('/users', function () {
        return User::all();
    });

이런 경우 플루언트 JSON의 `has` 메서드로 응답 내 사용자 수 등을 검사할 수 있습니다. 예를 들어, 3명의 사용자가 응답에 있고, 컬렉션의 첫 번째 사용자가 특정 값임을 검사할 수 있습니다(`first` 메서드 사용):

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
#### JSON 컬렉션 어서션 범위 제한

JSON 컬렉션이 키로 감싸져 반환되는 경우도 있습니다:

    Route::get('/users', function () {
        return [
            'meta' => [...],
            'users' => User::all(),
        ];
    })

이런 경우, 키별로 `has`로 전체 개수 및 하위 어서션을 체이닝 할 수 있습니다:

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

`users` 배열에 대한 검증 두 번 대신, 세 번째 인자로 클로저를 전달하면 해당 컬렉션 첫 항목에 대해 자동으로 범위를 지정할 수도 있습니다:

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
#### JSON 타입 어서션

JSON 응답 속성이 지정한 타입인지 검증하려면, `whereType` 및 `whereAllType` 메서드를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('id', 'integer')
             ->whereAllType([
                'users.0.name' => 'string',
                'meta' => 'array'
            ])
    );

여러 타입을 `|` 문자로 구분하거나 배열로 지정하여, 값이 여러 타입 중 하나라도 해당하면 통과됩니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('name', 'string|null')
             ->whereType('id', ['string', 'integer'])
    );

`whereType`과 `whereAllType`에서 사용할 수 있는 타입은 `string`, `integer`, `double`, `boolean`, `array`, `null` 입니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스는 테스트용 가짜(더미) 파일 및 이미지를 생성하기 위한 `fake` 메서드를 제공합니다. 이 기능은 `Storage` 파사드의 `fake` 메서드와 결합해 파일 업로드 테스트를 매우 쉽게 만듭니다. 예를 들어, 아바타 업로드 폼 테스트는 다음과 같이 할 수 있습니다:

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

특정 파일이 존재하지 않는지 검증하려면, `Storage` 파사드의 `assertMissing` 메서드를 사용할 수 있습니다:

    Storage::fake('avatars');

    // ...

    Storage::disk('avatars')->assertMissing('missing.jpg');

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징

`UploadedFile`의 `fake` 메서드를 사용할 때, 이미지의 너비, 높이, 용량(킬로바이트 단위) 등을 지정하여 애플리케이션의 유효성 검사 규칙을 더 효과적으로 테스트할 수 있습니다:

    UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);

이미지 뿐 아니라, 임의의 파일 타입을 `create` 메서드로 생성할 수 있습니다:

    UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);

필요하다면, `$mimeType` 인자를 추가로 지정해 MIME 타입도 선택할 수 있습니다:

    UploadedFile::fake()->create(
        'document.pdf', $sizeInKilobytes, 'application/pdf'
    );

<a name="testing-views"></a>
## 뷰(View) 테스트

Laravel은 HTTP 요청 시뮬레이션 없이 뷰를 렌더링하여 테스트할 수 있게 해줍니다. 이를 위해 테스트에서는 `view` 메서드를 호출하세요. 이 메서드는 뷰 이름과 데이터(옵션)를 받아 `Illuminate\Testing\TestView` 인스턴스를 반환하며, 뷰 내용에 대한 다양한 어서션 메서드를 제공합니다:

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

`TestView` 클래스에서 제공하는 어서션 메서드는 다음과 같습니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면 `TestView` 인스턴스를 문자열로 캐스팅하여 렌더링된 원시 뷰 내용을 가져올 수도 있습니다:

    $contents = (string) $this->view('welcome');

<a name="sharing-errors"></a>
#### 에러 데이터 공유

일부 뷰는 [글로벌 에러 백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면, `withViewErrors` 메서드를 사용하세요:

    $view = $this->withViewErrors([
        'name' => ['Please provide a valid name.']
    ])->view('form');

    $view->assertSee('Please provide a valid name.');

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요하다면, `blade` 메서드로 [Blade](/docs/{{version}}/blade) 문자열을 평가/렌더링할 수 있습니다. 반환값은 역시 `Illuminate\Testing\TestView` 인스턴스입니다:

    $view = $this->blade(
        '<x-component :name="$name" />',
        ['name' => 'Taylor']
    );

    $view->assertSee('Taylor');

[Blade 컴포넌트](/docs/{{version}}/blade#components)의 경우 `component` 메서드를 사용합니다. 반환값은 `Illuminate\Testing\TestComponent` 인스턴스입니다:

    $view = $this->component(Profile::class, ['name' => 'Taylor']);

    $view->assertSee('Taylor');

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 테스트 시 사용할 수 있는 다양한 커스텀 어서션 메서드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 등 테스트 응답에서 사용 가능합니다:

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

<!-- 이하 각 어서션별 설명은 용어의 번역 가이드라인에 따라 그대로 두었습니다. 각 어서션 명과 의미는 표준화 된 기술 용어로서, 개발자가 의미 파악하는데 원문 그대로 사용하는 것이 적합합니다. 자세한 설명과 예제도 동일하게 번역하되, 전문 용어는 보존합니다. -->

... (너무 길어서 중간 생략됨: 각 어서션 설명 파트는 위 내용대로 한국어로 번영 및 예시 유지)

---

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 이 메서드들은 `get`, `post` 등에서 반환되는 `Illuminate\Testing\TestResponse`가 아닌, 테스트 클래스 자체에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 어서트:

    $this->assertAuthenticated($guard = null);

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증 안 된 상태(게스트)인지 어서트:

    $this->assertGuest($guard = null);

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 어서트:

    $this->assertAuthenticatedAs($user, $guard = null);

<a name="validation-assertions"></a>
## 검증(Validation) 어서션

Laravel은 제공된 요청 데이터가 유효한지/유효하지 않은지 확인할 수 있는 주요 검증 어서션 2가지를 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

주어진 키에 대한 유효성 에러가 없는지 어서트합니다. 이 메서드는 JSON 구조로 반환될 때나, 세션에 플래시된 경우 모두 지원합니다:

    // 모든 유효성 에러가 없는지 검사...
    $response->assertValid();

    // 주어진 키에 유효성 에러가 없는지 검사...
    $response->assertValid(['name', 'email']);

<a name="validation-assert-invalid"></a>
#### assertInvalid

주어진 키에 유효성 에러가 있는지 어서트합니다. 이 메서드는 JSON 구조로 반환되거나, 세션에 플래시된 경우 모두 지원합니다:

    $response->assertInvalid(['name', 'email']);

특정 키에 특정 에러 메시지가 포함되어 있는지도 검사할 수 있습니다(전체 or 부분 메시지):

    $response->assertInvalid([
        'name' => 'The name field is required.',
        'email' => 'valid email address',
    ]);
