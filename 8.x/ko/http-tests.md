# HTTP 테스트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한(Fluent) JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰(View) 테스트](#testing-views)
    - [Blade & 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 어서션](#available-assertions)
    - [응답 어서션](#response-assertions)
    - [인증 어서션](#authentication-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검사하는 데 사용할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보세요:

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         *
         * @return void
         */
        public function test_a_basic_request()
        {
            $response = $this->get('/');

            $response->assertStatus(200);
        }
    }

`get` 메소드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메소드는 반환된 응답이 지정한 HTTP 상태 코드를 가졌는지 확인합니다. 이 단순한 어서션 외에도, Laravel에는 응답 헤더, 내용, JSON 구조 등을 검사하기 위한 다양한 어서션이 포함되어 있습니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내기 위해 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메소드를 호출할 수 있습니다. 이 메소드들은 실제 "진짜" HTTP 요청을 애플리케이션에 보내는 것이 아닙니다. 대신 네트워크 요청 전체가 내부적으로 시뮬레이션됩니다.

테스트 요청 메소드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신, `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 인스턴스는 [다양한 유용한 어서션](#available-assertions)을 제공하여 애플리케이션의 응답을 검사할 수 있게 합니다:

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         *
         * @return void
         */
        public function test_a_basic_request()
        {
            $response = $this->get('/');

            $response->assertStatus(200);
        }
    }

일반적으로, 각 테스트는 애플리케이션에 단 한 번만 요청을 보내야 합니다. 하나의 테스트 메소드 안에서 여러 번 요청을 실행하면 예기치 않은 동작이 일어날 수 있습니다.

> {tip} 편의를 위해, 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

`withHeaders` 메소드를 사용하여, 요청이 애플리케이션에 전송되기 전에 헤더를 커스터마이징할 수 있습니다. 이 메소드는 요청에 원하는 커스텀 헤더를 추가할 수 있게 해줍니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본적인 기능 테스트 예제.
         *
         * @return void
         */
        public function test_interacting_with_headers()
        {
            $response = $this->withHeaders([
                'X-Header' => 'Value',
            ])->post('/user', ['name' => 'Sally']);

            $response->assertStatus(201);
        }
    }

<a name="cookies"></a>
### 쿠키

`withCookie` 또는 `withCookies` 메소드를 사용하여 요청 전에 쿠키 값을 설정할 수 있습니다. `withCookie` 메소드는 두 개의 인자(쿠키 이름과 값)를 받으며, `withCookies` 메소드는 이름/값 쌍의 배열을 받습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_interacting_with_cookies()
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

HTTP 테스트 도중 세션을 다루기 위한 다양한 헬퍼를 Laravel에서 제공합니다. 먼저, `withSession` 메소드를 이용해 세션 데이터를 지정된 배열로 설정할 수 있습니다. 이 방법은 요청 전에 세션에 데이터를 미리 로드할 때 유용합니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_interacting_with_the_session()
        {
            $response = $this->withSession(['banned' => false])->get('/');
        }
    }

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 관리하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메소드를 사용하면 주어진 사용자를 현재 사용자로 인증할 수 있습니다. 예를 들어, [모델 팩토리](/docs/{{version}}/database-testing#writing-factories)를 이용해 사용자를 생성하고 인증할 수도 있습니다:

    <?php

    namespace Tests\Feature;

    use App\Models\User;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_an_action_that_requires_authentication()
        {
            $user = User::factory()->create();

            $response = $this->actingAs($user)
                             ->withSession(['banned' => false])
                             ->get('/');
        }
    }

지정한 사용자를 인증할 때 사용할 가드를 `actingAs` 메소드의 두 번째 인자로 전달해 지정할 수도 있습니다:

    $this->actingAs($user, 'web')

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 후, `dump`, `dumpHeaders`, `dumpSession` 메소드를 사용하여 응답 내용을 검사하고 디버깅할 수 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         *
         * @return void
         */
        public function test_basic_test()
        {
            $response = $this->get('/');

            $response->dumpHeaders();

            $response->dumpSession();

            $response->dump();
        }
    }

또는, `dd`, `ddHeaders`, `ddSession` 메소드를 이용해 응답 정보를 덤프한 뒤 실행을 중단할 수도 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         *
         * @return void
         */
        public function test_basic_test()
        {
            $response = $this->get('/');

            $response->ddHeaders();

            $response->ddSession();

            $response->dd();
        }
    }

<a name="exception-handling"></a>
### 예외 처리

애플리케이션이 특정 예외를 발생시키는지 테스트하고 싶을 때가 있습니다. 예외가 Laravel의 예외 핸들러에 의해 잡혀 HTTP 응답으로 반환되지 않도록 하려면, 요청을 보내기 전에 `withoutExceptionHandling` 메소드를 호출하면 됩니다:

    $response = $this->withoutExceptionHandling()->get('/');

또한, PHP 언어 자체나 애플리케이션에서 사용하는 라이브러리에 의해 더 이상 지원되지 않는(Deprecated) 기능을 사용하는지 확인하고 싶을 때, 요청 전에 `withoutDeprecationHandling` 메소드를 사용할 수 있습니다. 이 경우, Deprecated 경고가 예외로 변환되어 테스트가 실패하게 됩니다:

    $response = $this->withoutDeprecationHandling()->get('/');

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API와 그 응답을 테스트하기 위한 여러 헬퍼도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메소드로 다양한 HTTP 메소드로 JSON 요청을 보낼 수 있습니다. 데이터와 헤더도 손쉽게 전달할 수 있습니다. 아래는 `/api/user`로 `POST` 요청을 보내고, 예상되는 JSON 데이터가 반환되는지 검사하는 테스트 예시입니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
         *
         * @return void
         */
        public function test_making_an_api_request()
        {
            $response = $this->postJson('/api/user', ['name' => 'Sally']);

            $response
                ->assertStatus(201)
                ->assertJson([
                    'created' => true,
                ]);
        }
    }

또한, JSON 응답 데이터는 배열 변수처럼 사용할 수 있어서 개별 값을 쉽게 검사할 수 있습니다:

    $this->assertTrue($response['created']);

> {tip} `assertJson` 메소드는 응답을 배열로 변환하고, `PHPUnit::assertArraySubset`을 사용해 지정한 배열이 애플리케이션이 반환한 JSON 응답 안에 존재하는지 검사합니다. 따라서 JSON 응답에 다른 속성이 더 있어도 지정된 조각(fragment)만 포함되어 있으면 이 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
#### JSON 정확 일치 어서션

앞서 언급했듯이, `assertJson` 메소드는 JSON 응답 안에 지정된 조각(fragment)이 존재하는지 검사합니다. 만약 응답 JSON과 특정 배열이 **정확히** 일치하는지 확인하려면 `assertExactJson` 메소드를 사용해야 합니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
         *
         * @return void
         */
        public function test_asserting_an_exact_json_match()
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
#### JSON 경로 어서션

JSON 응답에 지정한 경로(path)에 해당 데이터가 포함되어 있는지 확인하려면, `assertJsonPath` 메소드를 사용할 수 있습니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 기능 테스트 예제.
         *
         * @return void
         */
        public function test_asserting_a_json_paths_value()
        {
            $response = $this->postJson('/user', ['name' => 'Sally']);

            $response
                ->assertStatus(201)
                ->assertJsonPath('team.owner.name', 'Darian');
        }
    }

<a name="fluent-json-testing"></a>
### 유창한(Fluent) JSON 테스트

Laravel은 애플리케이션의 JSON 응답을 더욱 유창하게(Fluent) 테스트할 수 있는 방법도 제공합니다. 먼저, `assertJson` 메소드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 인자로 받아, 반환된 JSON에 대해 어서션을 할 수 있게 해줍니다. `where` 메소드를 이용해 특정 속성에 대해 어서션을 하고, `missing` 메소드로 특정 속성이 존재하지 않는지도 검사할 수 있습니다:

    use Illuminate\Testing\Fluent\AssertableJson;

    /**
     * 기본 기능 테스트 예제.
     *
     * @return void
     */
    public function test_fluent_json()
    {
        $response = $this->getJson('/users/1');

        $response
            ->assertJson(fn (AssertableJson $json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->missing('password')
                     ->etc()
            );
    }

#### `etc` 메소드의 이해

위의 예제에서, 어서션 체인 마지막에 `etc` 메소드를 호출한 것을 볼 수 있습니다. 이 메소드는 JSON 객체에 추가 속성이 존재할 수 있음을 Laravel에 알립니다. `etc`를 사용하지 않으면, 선언하지 않은 추가 속성이 JSON 객체에 있을 경우 테스트가 실패합니다.

이 동작의 목적은, 여러분이 JSON 응답에 민감한 정보가 의도치 않게 노출되는 일을 방지할 수 있도록 모든 속성에 대해 명시적 어서션 또는 `etc` 사용을 강제하기 위함입니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성의 존재/부재 어서션

어떤 속성이 존재하거나 없는지 어서트하려면 `has`, `missing` 메소드를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('data')
             ->missing('message')
    );

또한, `hasAll`, `missingAll` 메소드를 사용하면 여러 속성의 존재 여부를 동시에 어서트할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->hasAll('status', 'data')
             ->missingAll('message', 'code')
    );

`hasAny` 메소드로 지정한 속성 중 하나라도 존재하는지 확인할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('status')
             ->hasAny('data', 'message', 'code')
    );

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 어서션

라라벨의 라우트가 여러 아이템(예: 여러 사용자)로 구성된 JSON 응답을 반환할 때가 많습니다:

    Route::get('/users', function () {
        return User::all();
    });

이 경우, 유창한 JSON 객체의 `has` 메소드로 응답에 포함된 사용자에 대해 어서트할 수 있습니다. 예를 들어, 응답이 3명의 사용자를 포함하고, 컬렉션의 첫 번째 사용자에 대해 추가 어서트를 진행할 수 있습니다. `first` 메소드는 클로저를 받아, 그 안에서 첫 번째 객체를 어서트할 수 있게 합니다:

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->has(3)
                 ->first(fn ($json) =>
                    $json->where('id', 1)
                         ->where('name', 'Victoria Faith')
                         ->missing('password')
                         ->etc()
                 )
        );

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어서션의 범위 지정

애플리케이션의 라우트가 명명된 키와 함께 JSON 컬렉션을 반환할 때가 있습니다:

    Route::get('/users', function () {
        return [
            'meta' => [...],
            'users' => User::all(),
        ];
    })

이 경우, `has` 메소드로 컬렉션 내 항목 수를 어서트할 수 있고, 체인으로 어서션 범위를 지정할 수도 있습니다:

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->has('meta')
                 ->has('users', 3)
                 ->has('users.0', fn ($json) =>
                    $json->where('id', 1)
                         ->where('name', 'Victoria Faith')
                         ->missing('password')
                         ->etc()
                 )
        );

또는, `has` 메소드에 클로저를 세 번째 파라미터로 전달하면, 컬렉션의 첫 번째 요소에 대한 어서트를 한 번에 수행할 수도 있습니다:

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->has('meta')
                 ->has('users', 3, fn ($json) =>
                    $json->where('id', 1)
                         ->where('name', 'Victoria Faith')
                         ->missing('password')
                         ->etc()
                 )
        );

<a name="asserting-json-types"></a>
#### JSON 타입 어서션

JSON 응답의 속성이 특정 타입인지 어서트하고 싶은 경우, `Illuminate\Testing\Fluent\AssertableJson` 클래스의 `whereType`, `whereAllType` 메소드를 사용할 수 있습니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('id', 'integer')
             ->whereAllType([
                'users.0.name' => 'string',
                'meta' => 'array'
            ])
    );

여러 타입을 지정하고 싶다면 `|` 문자를 사용하거나, 타입 배열을 두 번째 파라미터로 전달할 수 있습니다. 응답 값이 명시된 타입 중 하나라도 해당되면 어서션은 성공합니다:

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('name', 'string|null')
             ->whereType('id', ['string', 'integer'])
    );

`whereType`, `whereAllType` 메소드가 인식하는 타입은 다음과 같습니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일이나 이미지를 생성할 수 있는 `fake` 메소드를 제공합니다. 이는 `Storage` 파사드의 `fake` 메소드와 결합해 파일 업로드 테스트를 매우 쉽게 만듭니다. 아래는 아바타 업로드 양식을 테스트하는 예시입니다:

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Http\UploadedFile;
    use Illuminate\Support\Facades\Storage;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_avatars_can_be_uploaded()
        {
            Storage::fake('avatars');

            $file = UploadedFile::fake()->image('avatar.jpg');

            $response = $this->post('/avatar', [
                'avatar' => $file,
            ]);

            Storage::disk('avatars')->assertExists($file->hashName());
        }
    }

존재하지 않는 파일에 대해 어서트하려면 `Storage` 파사드의 `assertMissing` 메소드를 사용할 수 있습니다:

    Storage::fake('avatars');

    // ...

    Storage::disk('avatars')->assertMissing('missing.jpg');

<a name="fake-file-customization"></a>
#### 더미 파일 커스터마이징

`UploadedFile` 클래스의 `fake` 메소드로 이미지를 만들 때, 파일의 너비, 높이, 크기(KB단위)를 지정해 애플리케이션의 검증 규칙을 더 잘 테스트할 수 있습니다:

    UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);

이미지 외에 다른 타입의 파일을 만들 때는 `create` 메소드를 사용할 수 있습니다:

    UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);

필요하다면, 메소드에 `$mimeType` 인자를 전달하여 파일이 반환할 MIME 타입을 명확히 정의할 수 있습니다:

    UploadedFile::fake()->create(
        'document.pdf', $sizeInKilobytes, 'application/pdf'
    );

<a name="testing-views"></a>
## 뷰(View) 테스트

Laravel은 시뮬레이션된 HTTP 요청 없이 뷰를 직접 렌더링하는 것도 지원합니다. 이를 위해 테스트에서 `view` 메소드를 호출하면 됩니다. 이 메소드는 뷰 이름과(필요하다면) 데이터 배열을 인자로 받으며, `Illuminate\Testing\TestView` 인스턴스를 반환합니다. 이 인스턴스는 뷰의 내용을 편리하게 어서트하는 다양한 메소드를 제공합니다:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_a_welcome_view_can_be_rendered()
        {
            $view = $this->view('welcome', ['name' => 'Taylor']);

            $view->assertSee('Taylor');
        }
    }

`TestView` 클래스는 다음 어서션 메소드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면, `TestView` 인스턴스를 문자열로 변환하여 렌더링된 뷰의 원시 내용을 얻을 수 있습니다:

    $contents = (string) $this->view('welcome');

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 [Laravel이 제공하는 전역 에러백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 의존할 수 있습니다. 에러 메시지로 에러백을 채우기 위해 `withViewErrors` 메소드를 사용할 수 있습니다:

    $view = $this->withViewErrors([
        'name' => ['Please provide a valid name.']
    ])->view('form');

    $view->assertSee('Please provide a valid name.');

<a name="rendering-blade-and-components"></a>
### Blade & 컴포넌트 렌더링

필요하다면, `blade` 메소드로 원시 [Blade](/docs/{{version}}/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메소드와 마찬가지로 `blade` 메소드도 `Illuminate\Testing\TestView` 인스턴스를 반환합니다:

    $view = $this->blade(
        '<x-component :name="$name" />',
        ['name' => 'Taylor']
    );

    $view->assertSee('Taylor');

[Blade 컴포넌트](/docs/{{version}}/blade#components)를 평가·렌더링하려면 `component` 메소드를 사용하세요. 이 역시 `TestView` 인스턴스를 반환합니다:

    $view = $this->component(Profile::class, ['name' => 'Taylor']);

    $view->assertSee('Taylor');

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션 테스트 시 활용할 수 있는 다양한 커스텀 어서션 메소드를 제공합니다. 이 어서션들은 `json`, `get`, `post`, `put`, `delete` 테스트 메소드가 반환하는 응답에서 사용할 수 있습니다.

<style>
    .collection-method-list > p {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">

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
[assertHeader](#assert-header)
[assertHeaderMissing](#assert-header-missing)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)
[assertJsonPath](#assert-json-path)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertJsonValidationErrorFor](#assert-json-validation-error-for)
[assertLocation](#assert-location)
[assertNoContent](#assert-no-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertSessionHas](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[assertSessionMissing](#assert-session-missing)
[assertSimilarJson](#assert-similar-json)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

</div>

> 이하 어서션들의 설명 및 예제들은 원문과 동일합니다. (코드 블럭·HTML·URL은 번역 대상 아님 지침에 따라 원문 내용이 유지되고, 함수명과 파라미터, 코드 예시 등은 번역하지 않습니다.)

<a name="authentication-assertions"></a>
### 인증 어서션

Laravel은 애플리케이션의 기능 테스트 내에서 활용할 수 있는 다양한 인증 관련 어서션도 제공합니다. 이 메소드들은 `get`, `post` 등의 응답(TestResponse 인스턴스)이 아닌, 테스트 클래스 자체에서 호출되는 점에 유의하세요.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 어서트합니다:

    $this->assertAuthenticated($guard = null);

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지 어서트합니다:

    $this->assertGuest($guard = null);

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 어서트합니다:

    $this->assertAuthenticatedAs($user, $guard = null);
