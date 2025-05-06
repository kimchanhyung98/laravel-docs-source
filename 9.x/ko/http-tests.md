# HTTP 테스트

- [소개](#introduction)
- [요청 생성](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [플루언트 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade & 컴포넌트 렌더링](#rendering-blade-and-components)
- [사용 가능한 단언 메서드](#available-assertions)
    - [응답 단언](#response-assertions)
    - [인증 단언](#authentication-assertions)
    - [검증 단언](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검증할 수 있는 매우 플루언트한 API를 제공합니다. 예시로 아래의 기능 테스트를 살펴보세요:

```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_a_basic_request()
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가져야 함을 확인합니다. 이 간단한 단언 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검증할 수 있는 다양한 단언 메서드를 제공합니다.

<a name="making-requests"></a>
## 요청 생성

애플리케이션에 요청을 보내려면 테스트 내에서 `get`, `post`, `put`, `patch`, `delete` 메서드 중 하나를 사용할 수 있습니다. 이 메서드들은 실제 "진짜" HTTP 요청을 보내지 않고, 네트워크 요청 전체를 내부적으로 시뮬레이션합니다.

이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 것이 아니라, `Illuminate\Testing\TestResponse`의 인스턴스를 반환합니다. 이는 [유용한 다양한 단언](#available-assertions) 메서드를 제공하여 애플리케이션의 응답을 검사할 수 있게 해줍니다.

```php
// 예시 생략 (위와 동일)
```

일반적으로, 각 테스트는 하나의 요청만을 보내는 것이 좋습니다. 테스트 메서드 내에서 여러 요청이 실행되면 예기치 않은 동작이 발생할 수 있습니다.

> **참고**  
> 편의를 위해 테스트 실행 시 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

`withHeaders` 메서드를 사용하여 요청이 애플리케이션으로 전송되기 전에 헤더를 커스터마이징할 수 있습니다. 이 메서드는 요청에 원하는 커스텀 헤더를 추가할 수 있게 해줍니다.

```php
// 예시 생략
```

<a name="cookies"></a>
### 쿠키

`withCookie` 또는 `withCookies` 메서드를 사용해 요청 전에 쿠키 값을 설정할 수 있습니다. `withCookie`는 쿠키 이름과 값을 인자로 받고, `withCookies`는 이름/값 쌍의 배열을 받습니다.

```php
// 예시 생략
```

<a name="session-and-authentication"></a>
### 세션 / 인증

Laravel은 HTTP 테스트 중 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 예를 들어, `withSession` 메서드로 세션 데이터를 배열로 설정할 수 있습니다. 이는 요청하기 전에 세션에 데이터를 미리 채워넣고 싶을 때 유용합니다.

```php
// 예시 생략
```

Laravel의 세션은 보통 현재 인증된 사용자 상태를 유지하는 데 사용됩니다. `actingAs` 헬퍼는 특정 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 이용해 사용자를 생성하고 인증할 수 있습니다.

```php
// 예시 생략
```

또한 인증에 사용할 가드를 두 번째 인자로 지정할 수 있습니다. 지정 시, 테스트 동안 해당 가드가 기본 가드가 됩니다.

```php
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청 실행 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용해 응답 내용을 검사하고 디버깅할 수 있습니다.

```php
// 예시 생략
```

또는, 정보를 출력하고 실행을 중단하려면 `dd`, `ddHeaders`, `ddSession` 메서드를 사용할 수 있습니다.

```php
// 예시 생략
```

<a name="exception-handling"></a>
### 예외 처리

애플리케이션이 특정 예외를 발생시키는지 테스트하려면, 요청 전에 `withoutExceptionHandling` 메서드를 호출하여 예외가 Laravel의 예외 핸들러에 의해 잡혀 HTTP 응답으로 반환되지 않도록 할 수 있습니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한, PHP 또는 사용 중인 라이브러리에서 더 이상 사용되지 않는 기능을 애플리케이션이 사용하지 않도록 하고 싶다면, 요청 전에 `withoutDeprecationHandling`을 호출할 수 있습니다. 이 경우, 더 이상 사용되지 않는 기능의 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API 및 그 응답을 쉽게 테스트할 수 있는 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드는 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다. 데이터와 헤더도 쉽게 전달할 수 있습니다. 예를 들어 `/api/user`에 `POST` 요청을 보내고 기대한 JSON 데이터가 반환됐는지 테스트할 수 있습니다.

```php
// 예시 생략
```

또한, JSON 응답 데이터는 배열 변수처럼 접근할 수 있으므로, 반환된 개별 값을 쉽게 검사할 수 있습니다.

```php
$this->assertTrue($response['created']);
```

> **참고**  
> `assertJson` 메서드는 응답을 배열로 변환하고 `PHPUnit::assertArraySubset`을 이용해 지정한 배열이 응답 JSON에 존재하는지 확인합니다. 응답 JSON에 다른 속성이 있어도 지정한 조각만 있으면 테스트가 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 단언

앞서 언급했듯 `assertJson`은 JSON의 일부가 존재하는지를 확인합니다. 반환된 JSON이 지정한 배열과 **정확히 일치하는지** 확인하려면 `assertExactJson`을 사용하세요.

```php
// 예시 생략
```

<a name="verifying-json-paths"></a>
#### JSON 경로로 단언

JSON 응답에 특정 경로에 데이터가 포함되어 있는지 확인하려면 `assertJsonPath`를 사용하세요.

```php
// 예시 생략
```

`assertJsonPath`는 클로저도 받을 수 있어 동적으로 단언 여부를 결정하게 할 수 있습니다.

```php
$response->assertJsonPath('team.owner.name', fn ($name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 플루언트 JSON 테스트

Laravel은 응답 JSON을 플루언트하게 테스트할 수 있는 아름다운 방법도 제공합니다. 시작하려면 `assertJson`에 클로저를 전달하세요. 이 클로저에는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스가 주어집니다. `where`로 속성 단언, `missing`으로 속성 부재 단언이 가능합니다.

```php
use Illuminate\Testing\Fluent\AssertableJson;

// ...
public function test_fluent_json()
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                 ->where('name', 'Victoria Faith')
                 ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                 ->whereNot('status', 'pending')
                 ->missing('password')
                 ->etc()
        );
}
```

#### `etc` 메서드의 역할

위 예시에서, 단언 체인 끝에 `etc` 메서드를 호출한 것을 볼 수 있습니다. 이 메서드는 JSON 객체에 추가 속성이 존재할 수 있음을 Laravel에 알립니다. `etc`를 사용하지 않으면, 테스트는 명시적으로 단언한 속성 이외의 속성이 객체에 존재할 때 실패합니다.

이 동작의 의도는, JSON 응답에서 속성에 대해 명시적으로 단언하거나 `etc`로 허용하지 않은 경우, 민감 정보가 무심코 노출되는 것을 방지하기 위함입니다.

다만, 단언 체인에 `etc`를 포함하지 않는다고 해서 JSON 객체의 중첩 배열에서 추가 속성이 존재하지 않음을 보장하지는 않습니다. `etc`는 해당 네스팅 레벨까지만 유효합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 단언

속성의 존재나 부재를 단언하려면 `has`, `missing` 메서드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
         ->missing('message')
);
```

`hasAll`, `missingAll`로 여러 속성을 한 번에 단언할 수도 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
         ->missingAll(['message', 'code'])
);
```

지정한 속성 중 하나라도 존재하는지 확인하려면 `hasAny`를 사용하세요.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
         ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션 단언

기본적으로 라우트가 여러 항목을 포함한 JSON 컬렉션을 반환할 수 있습니다. 이런 경우 fluent JSON 객체의 `has` 메서드로 응답에 포함된 사용자 수 등을 단언할 수 있습니다. 또한, `first` 메서드로 첫 번째 항목에 대한 단언을 체이닝할 수 있습니다.

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
             ->first(fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 단언 범위 지정

라우트가 이름이 지정된 키의 JSON 컬렉션을 반환할 때가 있습니다. 예를 들면:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이런 경우 `has`로 컬렉션 항목 수를 단언할 수 있고, 추가적으로 스코프를 지정하여 체이닝도 가능합니다.

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3)
             ->has('users.0', fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

또한, `has`의 세 번째 인자로 클로저를 제공하면 컬렉션의 첫 번째 항목으로 자동으로 스코프가 지정됩니다.

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3, fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="asserting-json-types"></a>
#### JSON 타입 단언

응답의 속성이 특정 타입임만 확인하고 싶을 때는 `whereType`과 `whereAllType`을 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
         ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`|`를 써서 여러 타입을 지정하거나, 타입 배열을 두 번째 인자로 전달할 수도 있습니다. 값이 지정한 타입 중 하나면 단언이 통과합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
         ->whereType('id', ['string', 'integer'])
);
```

`whereType`, `whereAllType`이 인식하는 타입: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 사용하여 테스트용 가짜 파일이나 이미지를 생성할 수 있습니다. 이 기능과 `Storage` 파사드의 `fake` 메서드를 결합하면 파일 업로드 테스트가 간단해집니다. 예를 들어, 아바타 업로드 폼을 쉽게 테스트할 수 있습니다.

```php
// 예시 생략
```

파일이 존재하지 않음도 `Storage` 파사드의 `assertMissing`으로 검증할 수 있습니다.

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징

`UploadedFile` 클래스의 `fake` 메서드로 파일 생성 시, 이미지의 너비, 높이, 크기(킬로바이트 단위)를 지정해 검증 규칙 테스트를 세부적으로 할 수 있습니다.

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 외 다른 파일 타입은 `create` 메서드를 쓰세요.

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요하다면 `$mimeType` 인자로 MIME 타입을 명확하게 정의할 수도 있습니다.

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트

Laravel에서는 HTTP 요청을 시뮬레이션하지 않고도 뷰를 렌더링할 수 있습니다. 테스트 내에서 `view` 메서드를 호출하면 됩니다. `view`는 뷰 이름과 데이터 배열을 받아 `Illuminate\Testing\TestView` 인스턴스를 반환하며, 여러 단언 메서드를 통해 뷰의 내용을 쉽게 검증할 수 있습니다.

```php
// 예시 생략
```

`TestView` 클래스가 제공하는 단언 메서드:
`assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

필요하다면 `TestView` 인스턴스를 문자열로 캐스팅해 렌더된 뷰의 원시 내용을 얻을 수 있습니다.

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 에러 공유

일부 뷰는 [Laravel이 제공하는 글로벌 에러 백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면 `withViewErrors`를 활용하면 됩니다.

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade & 컴포넌트 렌더링

필요하다면 `blade` 메서드로 [Blade](/docs/{{version}}/blade) 문자열을 평가 및 렌더링할 수 있습니다. 결과는 `Illuminate\Testing\TestView` 인스턴스로 반환됩니다.

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

[Blade 컴포넌트](/docs/{{version}}/blade#components)의 평가 및 렌더링은 `component` 메서드를 사용하세요. 결과는 `Illuminate\Testing\TestComponent`입니다.

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
## 사용 가능한 단언 메서드

<a name="response-assertions"></a>
### 응답 단언

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 테스트 시 활용할 수 있는 다양한 커스텀 단언 메서드를 제공합니다. 이 단언은 `json`, `get`, `post`, `put`, `delete` 등의 메서드로 반환된 응답에서 사용할 수 있습니다.

<!-- HTML/스타일, 링크 URL은 번역하지 않음 -->

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
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
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

<a name="assert-cookie"></a>
#### assertCookie

응답에 지정한 쿠키가 포함되어 있는지 단언합니다.

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정한 쿠키가 포함되어 있고 만료되었는지 단언합니다.

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정한 쿠키가 포함되어 있고 만료되지 않았는지 단언합니다.

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정한 쿠키가 포함되어 있지 않은지 단언합니다.

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

응답이 201 HTTP 상태 코드를 가졌는지 단언합니다.

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

응답에 지정된 문자열이 포함되어 있지 않은지 단언합니다. 두 번째 인자를 `false`로 전달하지 않는 한 자동으로 문자열을 이스케이프합니다.

```php
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

응답 텍스트에 지정된 문자열이 포함되어 있지 않은지 단언합니다. 두 번째 인자 `false` 전달 시 이스케이프 생략. 단언 전 응답 내용은 PHP의 `strip_tags` 함수를 거칩니다.

```php
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"인지 단언합니다(`Response::download`, `BinaryFileResponse`, `Storage::download` 형태).

```php
$response->assertDownload();
```

원한다면 다운로드 파일명이 맞는지도 단언할 수 있습니다.

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

응답이 지정 JSON 데이터와 정확히 일치하는지 단언합니다.

```php
$response->assertExactJson(array $data);
```

<a name="assert-forbidden"></a>
#### assertForbidden

응답이 403 HTTP 상태 코드(접근 금지)를 가졌는지 단언합니다.

```php
$response->assertForbidden();
```

<a name="assert-header"></a>
#### assertHeader

응답에 지정한 헤더와 값이 포함되어 있는지 단언합니다.

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

응답에 지정한 헤더가 없는지 단언합니다.

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-json"></a>
#### assertJson

응답에 지정 JSON 데이터가 포함되어 있는지 단언합니다.

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson`은 응답을 배열로 변환 후 `PHPUnit::assertArraySubset`으로 단언합니다. 따라서 응답 JSON에 다른 속성이 있어도 지정한 조각만 있으면 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

지정 키에 대해 응답 JSON 배열의 항목 수가 예상과 같은지 단언합니다.

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 지정 JSON 데이터 일부가 어디에든 포함되어 있는지 단언합니다.

```php
$response->assertJsonFragment(['name' => 'Taylor Otwell']);
```

<a name="assert-json-is-array"></a>
#### assertJsonIsArray

응답 JSON이 배열인지 단언합니다.

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 단언합니다.

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 지정 JSON 데이터가 포함되어 있지 않은지 단언합니다.

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 지정 JSON 데이터가 **정확히** 포함되어 있지 않은지 단언합니다.

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

주어진 키에 대해 응답이 JSON 검증 오류를 가지지 않음을 단언합니다.

```php
$response->assertJsonMissingValidationErrors($keys);
```

> **참고**  
> 더 일반적인 [assertValid](#assert-valid)로 JSON 검증 오류 및 세션 저장소 오류 없음도 단언할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

지정 경로에 데이터가 포함되어 있는지 단언합니다.

```php
$response->assertJsonPath($path, $expectedValue);
```

예시:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답이 지정 경로를 포함하지 않는지 단언합니다.

```php
$response->assertJsonMissingPath($path);
```

예시:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

응답의 JSON 구조가 기대와 일치하는지 단언합니다.

```php
$response->assertJsonStructure(array $structure);
```

예시 구조:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

구조 단언 예시:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

배열 객체가 있을 때는 `*` 문자로 배열의 모든 객체 구조를 단언할 수 있습니다.

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

응답이 주어진 키에 대해 JSON 검증 오류를 가지는지 단언합니다. 이 메서드는 검증 오류가 세션이 아닌 JSON 구조로 반환될 때 사용합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> **참고**  
> 더 일반적인 [assertInvalid](#assert-invalid)로 JSON 및 세션 검증 오류도 단언할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답이 주어진 키에 대해 JSON 검증 오류를 가지는지 단언합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-location"></a>
#### assertLocation

응답의 `Location` 헤더에 지정된 URI 값이 있는지 단언합니다.

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

응답 내용이 지정된 문자열과 일치하는지 단언합니다.

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정 HTTP 상태 코드 및 내용 없음임을 단언합니다.

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed-content"></a>
#### assertStreamedContent

응답의 스트리밍 내용이 지정된 문자열과 일치하는지 단언합니다.

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

응답이 404 HTTP 상태 코드(찾을 수 없음)를 가지는지 단언합니다.

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

응답이 200 HTTP 상태 코드임을 단언합니다.

```php
$response->assertOk();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정된 암호화되지 않은(plain) 쿠키가 포함되어 있는지 단언합니다.

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

응답이 지정 URI로 리다이렉트하는지 단언합니다.

```php
$response->assertRedirect($uri);
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 지정 문자열이 포함된 URI로 리다이렉트하는지 단언합니다.

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 지정 [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트하는지 단언합니다.

```php
$response->assertRedirectToRoute($name = null, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 지정 [서명된 라우트](/docs/{{version}}/urls#signed-urls)로 리다이렉트하는지 단언합니다.

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-see"></a>
#### assertSee

응답에 지정 문자열이 포함되어 있는지 단언합니다. 두 번째 인자를 `false`로 전달하지 않는 한 자동 이스케이프합니다.

```php
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

응답에 지정 문자열들이 순서대로 포함되어 있는지 단언합니다. 두 번째 인자를 `false`로 전달하지 않는 한 자동 이스케이프합니다.

```php
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

응답 텍스트에 지정 문자열이 포함되어 있는지 단언합니다. 두 번째 인자 `false` 전달 시 이스케이프 생략. 응답 내용은 `strip_tags` PHP 함수로 처리됩니다.

```php
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

응답 텍스트에 지정 문자열들이 순서대로 포함되어 있는지 단언합니다. 두 번째 인자 `false` 전달 시 이스케이프 생략. 응답 내용은 `strip_tags` PHP 함수로 처리됩니다.

```php
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-session-has"></a>
#### assertSessionHas

세션에 지정된 데이터가 포함되어 있는지 단언합니다.

```php
$response->assertSessionHas($key, $value = null);
```

필요시, 두 번째 인자로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 단언이 통과합니다.

```php
$response->assertSessionHas($key, function ($value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션의 [플래시 입력 배열](/docs/{{version}}/responses#redirecting-with-flashed-session-data)에 지정 값이 있는지 단언합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

필요시, 두 번째 인자로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 단언이 통과합니다.

```php
$response->assertSessionHasInput($key, function ($value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션에 지정된 키/값 쌍 배열이 모두 포함되어 있는지 단언합니다.

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 세션에 `name`, `status`가 있다면:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 주어진 `$keys`에 대한 오류가 포함되어 있는지 단언합니다. `$keys`가 연관배열이면 각 필드(키)에 특정 오류 메시지(값)가 있는지 확인합니다.
세션에 검증 오류가 플래시되는 라우트 테스트에 사용하세요.

```php
$response->assertSessionHasErrors(
    array $keys, $format = null, $errorBag = 'default'
);
```

예시:

```php
$response->assertSessionHasErrors(['name', 'email']);
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> **참고**  
> 더 일반적인 [assertInvalid](#assert-invalid)로 JSON 및 세션 검증 오류도 단언할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

특정 [에러 백](/docs/{{version}}/validation#named-error-bags) 내에서 주어진 `$keys`에 대한 오류가 세션에 포함되어 있는지 단언합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

세션에 검증 오류가 없는지 단언합니다.

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

주어진 키에 대해 세션에 검증 오류가 없는지 단언합니다.

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> **참고**  
> 더 일반적인 [assertValid](#assert-valid)로 JSON 및 세션 검증 오류 없음도 단언할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 지정된 키가 없는지 단언합니다.

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### assertStatus

응답이 지정 HTTP 상태 코드를 가지는지 단언합니다.

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

응답이 성공(200 이상 300 미만) HTTP 상태 코드임을 단언합니다.

```php
$response->assertSuccessful();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 401 HTTP 상태 코드(인증 필요)임을 단언합니다.

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 422 HTTP 상태 코드(처리 불가)임을 단언합니다.

```php
$response->assertUnprocessable();
```

<a name="assert-valid"></a>
#### assertValid

지정 키에 대해 응답에 검증 오류가 없는지 단언합니다. 이 메서드는 검증 오류가 JSON 혹은 세션에 플래시될 때 모두 사용 가능합니다.

```php
// 오류 없음 단언
$response->assertValid();

// 지정 키에 오류 없음 단언
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

주어진 키에 대해 응답이 검증 오류를 가지는지 단언합니다. JSON 혹은 세션 오류 모두 단언할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

특정 키가 특정 오류 메시지를 가지는지도 단언할 수 있습니다. 메시지 전체나 일부만 제공해도 됩니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 지정 데이터가 포함되어 있는지 단언합니다.

```php
$response->assertViewHas($key, $value = null);
```

두 번째 인자에 클로저를 전달하면 해당 뷰 데이터에 대해 추가 단언을 할 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또는 뷰 데이터는 배열처럼 접근 가능합니다.

```php
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 지정된 데이터 배열이 모두 포함되어 있는지 단언합니다.

```php
$response->assertViewHasAll(array $data);
```

단순히 데이터 키가 있는지만 또는 값까지 일치하는지도 확인 가능.

```php
$response->assertViewHasAll([
    'name',
    'email',
]);

$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

반환된 뷰가 지정된 뷰인지 단언합니다.

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

응답 뷰의 데이터에 지정 키가 없는지 단언합니다.

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 단언

Laravel은 기능 테스트에서 사용할 수 있는 다양한 인증 관련 단언도 제공합니다. 이 메서드들은 `get`, `post` 등이 반환한 `TestResponse` 인스턴스가 아닌 테스트 클래스 본문에서 호출합니다.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 단언합니다.

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지(게스트인지) 단언합니다.

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 단언합니다.

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 검증 단언

Laravel은 요청 데이터의 유효성 여부를 보장하기 위해 주로 두 가지 검증 단언 메서드를 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

응답이 지정된 키에 대해 검증 오류가 없는지 단언합니다. 이 메서드는 JSON 구조 또는 세션 오류 모두에 사용할 수 있습니다.

```php
// 오류 없음 단언
$response->assertValid();

// 지정 키에 오류 없음 단언
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

응답이 주어진 키에 대해 검증 오류를 가지는지 단언합니다. JSON 구조 또는 세션 오류 모두에 사용할 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

키가 특정 오류 메시지를 가지는지도 단언할 수 있습니다. 전체 메시지 또는 부분 문자열 모두 가능.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
