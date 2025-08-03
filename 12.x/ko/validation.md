# 유효성 검사 (Validation)

- [소개](#introduction)
- [유효성 검사 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 출력하기](#quick-displaying-the-validation-errors)
    - [폼에 입력값 다시 채우기](#repopulating-forms)
    - [선택적 필드에 관한 주의사항](#a-note-on-optional-fields)
    - [유효성 검사 에러 응답 형식](#validation-error-response-format)
- [폼 리퀘스트 유효성 검사](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 권한 검사](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검사용 입력 데이터 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 에러 백](#named-error-bags)
    - [수동으로 에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사 수행하기](#performing-additional-validation)
- [검증된 입력 데이터 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 이름 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검사](#validating-arrays)
    - [중첩 배열 입력 유효성 검사](#validating-nested-array-input)
    - [에러 메시지의 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검사](#validating-files)
- [비밀번호 유효성 검사](#validating-passwords)
- [커스텀 유효성 검사 규칙](#custom-validation-rules)
    - [룰 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적 룰](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 들어오는 데이터의 유효성을 검사하는 여러 가지 방법을 제공합니다. 가장 일반적인 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 이용하는 것입니다. 하지만 이외에도 다양한 유효성 검사 방법들을 함께 다룰 예정입니다.

Laravel은 데이터에 적용할 수 있는 매우 다양한 편리한 유효성 검사 규칙을 포함하고 있으며, 특정 데이터베이스 테이블 내에서 고유한지 여부를 검사하는 기능도 제공합니다. Laravel의 모든 유효성 검사 규칙을 자세히 살펴본 후, 이를 충분히 익힐 수 있도록 설명할 것입니다.

<a name="validation-quickstart"></a>
## 유효성 검사 빠른 시작

Laravel의 강력한 유효성 검사 기능을 배우기 위해, 폼을 검증하고 에러 메시지를 사용자에게 다시 보여주는 완전한 예제를 살펴봅시다. 이 전체적인 개요를 읽으면 Laravel을 이용해 들어오는 요청 데이터를 어떻게 효과적으로 검증할 수 있는지 큰 그림을 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 요청은 사용자가 새 블로그 게시물을 작성할 폼을 보여주는 역할을 하며, `POST` 요청은 데이터베이스에 새 게시물을 저장하는 역할을 합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

이제, 위 라우트들을 처리하는 간단한 컨트롤러를 살펴봅시다. `store` 메서드는 아직 비워둡니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물 작성을 위한 폼을 보여줍니다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 게시물을 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 게시물 유효성 검사 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 블로그 게시물을 검증하는 로직을 작성해봅시다. 여기에 Laravel의 `Illuminate\Http\Request` 객체에 내장된 `validate` 메서드를 사용할 것입니다. 유효성 검사 규칙을 모두 통과하면 코드가 정상적으로 계속 실행되지만, 유효성 검사가 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하며 적절한 에러 응답이 자동으로 사용자에게 전송됩니다.

전통적인 HTTP 요청에서 유효성 검사가 실패하면, 이전 URL로 리디렉션 응답이 생성됩니다. 만약 XHR 요청일 경우, [유효성 검사 에러 메시지를 포함하는 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 더 잘 이해하려면 `store` 메서드를 자세히 살펴보죠:

```php
/**
 * 새 블로그 게시물을 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 게시물 유효함...

    return redirect('/posts');
}
```

보시다시피, 유효성 검사 규칙들이 `validate` 메서드에 전달됩니다. 걱정하지 마세요 - 사용 가능한 모든 유효성 검사 규칙은 [여기](#available-validation-rules)에 문서화되어 있습니다. 다시 말하지만, 유효성 검사가 실패하면 적절한 응답이 자동 생성됩니다. 성공하면 컨트롤러가 정상적으로 실행됩니다.

또한, 유효성 검사 규칙을 문자열 대신 규칙 배열 형태로 지정할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

그리고 `validateWithBag` 메서드를 사용하여 요청을 검증하고 에러 메시지를 [이름이 지정된 에러 백](#named-error-bags)에 저장할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검사 실패 시 검사 중단하기

특정 속성(attribute)에 대해 첫 번째 유효성 검사 실패 후 더 이상의 규칙 검증을 중단하고 싶을 때가 있죠. 이럴 땐 해당 속성에 `bail` 규칙을 추가하면 됩니다:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서 `title` 속성의 `unique` 규칙이 실패하면, `max` 규칙은 검사하지 않습니다. 규칙들은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 주의사항

만약 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있다면, 유효성 검사 규칙에서 "점(dot) 표기법"을 사용해 이를 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드 이름에 실제 점(`.`) 문자가 포함되어 있어 점 표기법으로 해석되는 것을 방지하려면 역슬래시(`\`)로 이스케이프하면 됩니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 출력하기

그렇다면 요청 필드가 유효성 검사 규칙을 통과하지 못하면 어떻게 될까요? 앞서 말했듯이 Laravel은 자동으로 사용자를 이전 위치로 리디렉션합니다. 또한, 모든 유효성 검사 에러와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 자동으로 [세션에 플래시](#)됩니다.

`$errors` 변수는 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에서 애플리케이션의 모든 뷰에 공유됩니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있습니다. 따라서 미들웨어가 적용된 뷰에서는 항상 안전하게 `$errors` 변수를 사용할 수 있습니다. `$errors`는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 다루는 방법은 [관련 문서](#working-with-error-messages)를 참고하세요.

예를 들어, 유효성 검사 실패 시 사용자는 컨트롤러의 `create` 메서드로 리디렉션됩니다. 이를 통해 뷰에서 에러 메시지를 보여줄 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>게시물 작성</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- 게시물 작성 폼 -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 에러 메시지 커스터마이징

Laravel 내장 유효성 검사 규칙 각각은 애플리케이션의 `lang/en/validation.php` 언어 파일에 에러 메시지 항목이 있습니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에는 각 유효성 검사 규칙 별 메시지 번역 항목이 있습니다. 필요에 따라 이 메시지를 수정하거나 변경할 수 있습니다.

또한, 해당 파일을 다른 언어용 디렉터리로 복사해 애플리케이션의 언어에 맞게 메시지를 번역할 수도 있습니다. Laravel 다국어 지원에 대해 더 알고 싶다면 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어를 사용해 복사해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

이 예제는 전통적인 폼 제출을 가정했습니다. 하지만 JavaScript 기반 프론트엔드에서 XHR 요청으로 데이터를 보내는 앱도 많습니다. XHR 요청 중 `validate` 메서드를 사용하면 Laravel은 리디렉션 응답을 생성하지 않고, 대신 [모든 유효성 검사 에러를 포함하는 JSON 응답](#validation-error-response-format)을 HTTP 422 상태 코드와 함께 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

Blade 템플릿에서 `@error` 디렉티브를 써서 특정 속성에 대한 유효성 검사 에러가 있는지 빠르게 확인할 수 있습니다. `@error` 블록 내에서는 `$message` 변수를 출력해 에러 메시지를 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">게시물 제목</label>

<input
    id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

만약 [이름이 지정된 에러 백](#named-error-bags)을 사용 중이라면, `@error` 두 번째 인수로 에러 백 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼에 입력값 다시 채우기

Laravel이 유효성 실패로 리디렉션 응답을 생성하면, 해당 요청의 모든 입력값들을 자동으로 [세션에 플래시](#)해줍니다. 이렇게 하면 다음 요청에서 입력값을 쉽게 가져와 사용자가 시도했던 폼 내용을 다시 채울 수 있습니다.

이전에 플래시된 입력값은 `Illuminate\Http\Request` 인스턴스의 `old` 메서드로 불러올 수 있습니다. 이 메서드는 [세션](/docs/12.x/session)을 통해 저장된 값을 반환합니다:

```php
$title = $request->old('title');
```

또한, Blade 템플릿에서는 전역 `old` 헬퍼가 제공되어 폼을 다시 채우기 편리합니다. 필드에 플래시된 이전 입력값이 없으면 `null`을 반환합니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 관한 주의사항

기본적으로 Laravel은 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 글로벌 미들웨어 스택에 포함시킵니다. 따라서, 선택적인 필드라면 유효성 검사기에게 `null` 값을 유효하지 않은 값으로 간주하지 말라는 의미로 `nullable` 규칙을 명시해야 할 때가 많습니다. 예를 들면:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서 `publish_at` 필드는 `null`이거나 유효한 날짜 문자열이어야 합니다. 만약 `nullable`이 없으면, `null` 값은 유효하지 않은 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 에러 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 요청이 JSON 응답을 기대하는 경우 Laravel은 자동으로 에러 메시지를 포맷하여 HTTP 422 응답과 함께 반환합니다.

다음은 JSON 응답 예시입니다. 중첩된 에러 키는 "점(dot) 표기법"으로 평탄화됩니다:

```json
{
    "message": "The team name must be a string. (and 4 more errors)",
    "errors": {
        "team_name": [
            "The team name must be a string.",
            "The team name must be at least 1 characters."
        ],
        "authorization.role": [
            "The selected authorization.role is invalid."
        ],
        "users.0.email": [
            "The users.0.email field is required."
        ],
        "users.2.email": [
            "The users.2.email must be a valid email address."
        ]
    }
}
```

<a name="form-request-validation"></a>
## 폼 리퀘스트 유효성 검사

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성하기

복잡한 유효성 검사 시나리오에서는 "폼 리퀘스트"를 생성해 검증과 승인(authorization) 로직을 클래스 안에 캡슐화할 수 있습니다. 폼 리퀘스트 클래스는 `make:request` Artisan 명령어로 생성합니다:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트는 `app/Http/Requests` 디렉터리에 위치합니다. 존재하지 않으면 명령 실행 시 생성됩니다. 폼 리퀘스트 클래스는 주로 `authorize`와 `rules` 두 가지 메서드를 갖습니다.

`authorize` 메서드는 현재 인증된 사용자가 요청된 작업을 수행할 권한이 있는지 판단하는 역할을 하며, `rules` 메서드는 검증 규칙을 배열로 반환합니다:

```php
/**
 * 요청에 적용할 유효성 검사 규칙을 반환합니다.
 *
 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
 */
public function rules(): array
{
    return [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ];
}
```

> [!NOTE]
> `rules` 메서드 시그니처에 필요 의존성 주입을 선언해도 Laravel 서비스 컨테이너가 자동으로 해결해줍니다.

검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드에 폼 리퀘스트 클래스를 타입힌팅해주기만 하면 됩니다. 컨트롤러 메서드가 호출되기 전에 자동으로 유효성 검사가 수행되고, 따라서 컨트롤러 내부에 검증 코드를 추가할 필요가 없습니다:

```php
/**
 * 새 블로그 게시물을 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효합니다...

    // 검증된 입력 데이터를 가져옵니다...
    $validated = $request->validated();

    // 검증된 입력 데이터 일부만 선택하거나 제외할 수 있습니다...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 게시물 저장...

    return redirect('/posts');
}
```

검증 실패 시 이전 위치로 리디렉션되고, 에러도 세션에 플래시되어 표시할 수 있습니다. 만약 요청이 XHR이면, HTTP 422 상태 코드와 함께 [유효성 검사 오류의 JSON 표현](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 Laravel 프론트엔드에 실시간 폼 검사(validation)를 추가하려면 [Laravel Precognition](/docs/12.x/precognition)을 확인하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검사 수행하기

초기 유효성 검사 후 추가 검사가 필요할 때 폼 리퀘스트의 `after` 메서드를 활용할 수 있습니다.

`after` 메서드는 검증 종료 후 호출할 콜러블(또는 콜러블 배열)을 반환해야 합니다. 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아 필요 시 추가 에러 메시지를 생성할 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 유효성 검사 콜러블 배열을 반환합니다.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    '이 필드에 문제가 있습니다!'
                );
            }
        }
    ];
}
```

`after`는 호출 가능한 클래스 인스턴스도 배열에 포함할 수 있습니다. 이 경우 호출 가능한 클래스의 `__invoke` 메서드가 `Validator` 인스턴스를 받아 실행됩니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 유효성 검사 콜러블 배열을 반환합니다.
 */
public function after(): array
{
    return [
        new ValidateUserStatus,
        new ValidateShippingTime,
        function (Validator $validator) {
            //
        }
    ];
}
```

<a name="request-stopping-on-first-validation-rule-failure"></a>
#### 첫 번째 유효성 검사 실패 시 검사 중단

리퀘스트 클래스에 `$stopOnFirstFailure` 속성을 추가하여, 하나의 룰에서 실패가 발생하면 나머지 속성들에 대한 검증을 중단하도록 할 수 있습니다:

```php
/**
 * 유효성 검사기에서 첫 번째 룰 실패 시 중단할지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

폼 리퀘스트 유효성 검사 실패 시 기본적으로 이전 위치로 리디렉션됩니다. 하지만 `$redirect` 속성에 URI를 지정해 리디렉션 위치를 원하는 곳으로 바꿀 수 있습니다:

```php
/**
 * 유효성 검사 실패 시 리디렉션할 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는 이름이 지정된 라우트로 리다이렉트할 때는 `$redirectRoute` 속성을 정의합니다:

```php
/**
 * 유효성 검사 실패 시 리디렉션할 라우트 이름.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 권한 검사

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 여기서 인증된 사용자가 실제로 요청된 작업을 수행할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 업데이트하려는 댓글 소유자인지 확인할 수 있죠. 일반적으로는 [게이트 및 정책](/docs/12.x/authorization)과 연동합니다:

```php
use App\Models\Comment;

/**
 * 사용자의 요청 권한을 판단합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 베이스 Laravel Request를 상속하므로 `user` 메서드로 현재 인증된 사용자에 접근할 수 있습니다. 또한 위 예시에서 `route` 메서드를 호출해, 라우트에서 정의된 URI 파라미터 (예: `{comment}`)에 접근할 수 있습니다:

```php
Route::post('/comment/{comment}');
```

라우트 모델 바인딩을 사용하면 이렇게 간결하게도 작성 가능합니다:

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면 403 HTTP 응답을 자동으로 반환하며, 컨트롤러 메서드는 실행되지 않습니다.

만약 권한 로직을 다른 곳에서 처리한다면 `authorize` 메서드를 완전히 삭제하거나 `true`를 반환하도록 구현할 수 있습니다:

```php
/**
 * 사용자의 요청 권한을 판단합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처에도 필요한 의존성을 주입받을 수 있으며, Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동 해결합니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

`messages` 메서드를 오버라이드해 폼 리퀘스트의 유효성 검사 규칙에 쓰이는 에러 메시지를 커스터마이징할 수 있습니다. 이 메서드는 `속성.룰` 키와 대응하는 메시지 문자열 배열을 반환합니다:

```php
/**
 * 정의된 유효성 검사 규칙에 대한 에러 메시지 반환.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => '제목은 반드시 입력해야 합니다.',
        'body.required' => '본문은 반드시 입력해야 합니다.',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 속성명 커스터마이징

Laravel 기본 에러 메시지에는 `:attribute` 플레이스홀더가 많습니다. 이 값을 커스텀 속성명으로 치환하려면, `attributes` 메서드를 오버라이드해 속성명과 표시명을 배열로 반환하세요:

```php
/**
 * 유효성 검사 에러의 속성명 커스터마이징.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => '이메일 주소',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### 유효성 검사용 입력 데이터 준비하기

유효성 검사를 적용하기 전에 요청 데이터를 준비하거나 정제해야 할 경우 `prepareForValidation` 메서드를 사용하세요:

```php
use Illuminate\Support\Str;

/**
 * 유효성 검사 전 데이터 준비.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

반대로 유효성 검사 후 데이터 정규화를 원하면 `passedValidation` 메서드를 오버라이드할 수 있습니다:

```php
/**
 * 유효성 검사 성공 후 처리.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 생성하기

요청의 `validate` 메서드를 사용하지 않고 직접 `Validator` [퍼사드](/docs/12.x/facades)를 활용해 Validator 인스턴스를 만들 수도 있습니다. 퍼사드의 `make` 메서드가 Validator 인스턴스를 생성합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        if ($validator->fails()) {
            return redirect('/post/create')
                ->withErrors($validator)
                ->withInput();
        }

        // 검증된 입력 데이터 가져오기...
        $validated = $validator->validated();

        // 일부 필드만 선택하거나 제외하기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 게시물 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드 첫 번째 인자는 검증할 데이터, 두 번째는 유효성 규칙 배열입니다.

검증 실패 여부를 검사한 후에는 `withErrors` 메서드로 에러 메시지를 세션에 플래시할 수 있습니다. 이 때 `$errors` 변수가 자동으로 뷰에서 공유되므로 바로 사용할 수 있습니다. `withErrors`는 Validator 인스턴스, `MessageBag`, 또는 배열을 인자로 받을 수 있습니다.

#### 첫 번째 유효성 검사 실패 시 검사 중단

`stopOnFirstFailure` 메서드를 호출해, 하나의 규칙이 실패하면 검증을 즉시 중단하도록 지정할 수 있습니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

수동 Validator 객체를 만들더라도, 아래처럼 `validate` 메서드를 호출해 HTTP 요청의 `validate` 메서드와 같은 자동 리디렉션 기능을 활용할 수 있습니다. 실패하면 자동으로 리디렉션하거나 XHR 요청이면 [JSON 응답](#validation-error-response-format)을 반환합니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드로 [이름이 지정된 에러 백](#named-error-bags)에 오류 메시지를 저장할 수도 있습니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러 백 (Named Error Bags)

한 페이지에 여러 폼이 있을 때 각각의 에러 메시지를 별도 백에 저장해 구분하고 싶으면, `withErrors` 두 번째 인자로 이름을 지정하세요:

```php
return redirect('/register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수에서 이름이 지정된 에러 백을 아래처럼 접근할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 수동으로 에러 메시지 커스터마이징

수동 생성 Validator에 대해 Laravel 기본 메시지 대신 커스텀 메시지를 지정할 수 있습니다. 여러 방식이 있는데, 가장 일반적인 방법은 `Validator::make` 세 번째 인자로 메시지 배열을 전달하는 것입니다:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

`:attribute` 플레이스홀더는 유효성 검사 중인 필드명으로 교체됩니다. 다양한 플레이스홀더를 활용할 수 있습니다:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대해 커스텀 메시지 지정하기

특정 속성과 규칙에만 커스텀 메시지를 지정하려면 "점 표기법"으로 속성명과 규칙을 키로 사용하세요:

```php
$messages = [
    'email.required' => '이메일 주소를 알려주세요!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정하기

Laravel 내장 에러 메시지 대부분에 `:attribute` 플레이스홀더가 있습니다. 이를 특정 필드에 대해 커스텀한 값으로 치환하려면 `Validator::make` 네 번째 인자로 커스텀 속성 배열을 넘기세요:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검사 수행하기

초기 유효성 검사 후 추가 검사가 필요하면, Validator의 `after` 메서드를 사용하세요. 이 메서드는 유효성 검사 완료 후 호출할 클로저나 콜러블 배열을 인수로 받습니다. 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아 추가 에러 메시지를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', '이 필드에 문제가 있습니다!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

콜러블 배열을 전달하는 것도 가능합니다. 이는 호출 가능한 클래스에 `__invoke` 메서드가 구현되어 있을 때 유용합니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;

$validator->after([
    new ValidateUserStatus,
    new ValidateShippingTime,
    function ($validator) {
        // ...
    },
]);
```

<a name="working-with-validated-input"></a>
## 검증된 입력 데이터 다루기

폼 리퀘스트나 수동 생성 Validator 인스턴스로 들어오는 요청 데이터를 검증한 후, 실제 검증에 통과한 입력 데이터를 가져오고 싶을 때가 많습니다. 몇 가지 방법이 있습니다.

먼저, 폼 리퀘스트나 Validator 인스턴스에서 `validated` 메서드를 호출하면 검증된 데이터를 배열로 반환합니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 객체를 반환하며, 이 객체는 `only`, `except`, `all` 같은 메서드를 제공해 검증된 데이터 일부나 전부를 쉽게 가져올 수 있습니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

`ValidatedInput` 인스턴스는 배열처럼 반복문으로 순회하거나 인덱스로 접근할 수도 있습니다:

```php
// 검증된 데이터 반복 처리
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근
$validated = $request->safe();

$email = $validated['email'];
```

추가 필드를 검증된 데이터에 병합하려면 `merge` 메서드를 호출하세요:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections)으로 받고 싶다면 `collect` 메서드를 사용하세요:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 반환합니다. 이 클래스는 에러 메시지를 편리하게 처리하는 다양한 메서드를 제공합니다. 뷰에서 자동으로 제공되는 `$errors` 변수도 `MessageBag` 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드 첫 번째 에러 메시지 조회

특정 필드의 첫 번째 에러 메시지를 가져오려면 `first` 메서드를 사용하세요:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드 모든 에러 메시지 조회

특정 필드에 대해 모든 에러 메시지를 배열로 받고 싶으면 `get` 메서드를 사용하세요:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형식의 폼 필드를 검사하는 경우, `*` 문자를 사용해 배열 요소 각각의 메시지를 가져올 수도 있습니다:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 에러 메시지 모두 조회

애플리케이션 내 모든 필드에 걸린 에러 메시지 배열을 받고 싶다면 `all` 메서드를 사용하세요:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 필드에 에러 메시지 존재 여부 판단

`has` 메서드로 특정 필드에 에러 메시지가 있는지 판단할 수 있습니다:

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel 내장 유효성 검사 규칙 별 에러 메시지는 애플리케이션의 `lang/en/validation.php` 언어 파일에 있습니다. 만약 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

이 파일 내에서 각 규칙에 할당된 메시지 텍스트를 필요에 따라 수정하거나 바꿀 수 있습니다.

복사해서 다른 언어 디렉터리에 넣으면 애플리케이션 언어에 맞게 번역할 수 있습니다. Laravel 다국어 관련 자세한 건 [다국어 문서](/docs/12.x/localization)를 참조하세요.

> [!WARNING]
> 기본 Laravel 프로젝트에는 `lang` 디렉터리가 포함돼 있지 않습니다. 언어 파일을 수정하고 싶으면 `lang:publish` Artisan 명령어로 퍼블리시해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

언어 파일에서 `custom` 배열 안에 원하는 속성명과 규칙별 메시지를 작성하여 특정 조합에 대한 메시지를 커스터마이징할 수 있습니다:

```php
'custom' => [
    'email' => [
        'required' => '이메일 주소를 알려주세요!',
        'max' => '이메일 주소가 너무 깁니다!',
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 이름 지정하기

메시지에서 `:attribute` 플레이스홀더를 특정한 사용자 정의 명칭으로 대체하려면, 언어 파일의 `attributes` 배열에 명칭을 지정하면 됩니다:

```php
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]
> 기본 Laravel 프로젝트에는 `lang` 디렉터리가 포함돼 있지 않습니다. 언어 파일을 수정하려면 `lang:publish` 명령어로 퍼블리시하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

Laravel 내장 메시지 중에는 `:value` 플레이스홀더가 있는데, 이는 요청된 필드 값으로 대체됩니다. 하지만 때로는 더 사용자 친화적인 값 표시를 원할 수도 있습니다.

예를 들어, `payment_type` 필드가 `cc`일 경우에만 `credit_card_number` 필드가 필수라는 규칙이 있고 이것이 실패하면 메시지가 아래처럼 표시됩니다:

```text
The credit card number field is required when payment type is cc.
```

이때 `cc` 대신 더 친숙한 표현을 쓰려면 언어 파일의 `values` 배열에 해당 매핑을 추가하세요:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

그러면 다음과 같이 메시지가 변경됩니다:

```text
The credit card number field is required when payment type is credit card.
```

> [!WARNING]
> 기본적으로 `lang` 디렉터리는 없으니 `lang:publish` 명령어로 퍼블리시해야 합니다.

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검사 규칙

아래는 Laravel에서 제공하는 모든 유효성 검사 규칙 목록과 기능입니다:

#### Boolean 관련 규칙

[accepted](#rule-accepted)  
[accepted_if](#rule-accepted-if)  
[boolean](#rule-boolean)  
[declined](#rule-declined)  
[declined_if](#rule-declined-if)  

#### 문자열 관련 규칙

[active_url](#rule-active-url)  
[alpha](#rule-alpha)  
[alpha_dash](#rule-alpha-dash)  
[alpha_num](#rule-alpha-num)  
[ascii](#rule-ascii)  
[confirmed](#rule-confirmed)  
[current_password](#rule-current-password)  
[different](#rule-different)  
[doesnt_start_with](#rule-doesnt-start-with)  
[doesnt_end_with](#rule-doesnt-end-with)  
[email](#rule-email)  
[ends_with](#rule-ends-with)  
[enum](#rule-enum)  
[hex_color](#rule-hex-color)  
[in](#rule-in)  
[ip](#rule-ip)  
[json](#rule-json)  
[lowercase](#rule-lowercase)  
[mac_address](#rule-mac)  
[max](#rule-max)  
[min](#rule-min)  
[not_in](#rule-not-in)  
[regex](#rule-regex)  
[not_regex](#rule-not-regex)  
[same](#rule-same)  
[size](#rule-size)  
[starts_with](#rule-starts-with)  
[string](#rule-string)  
[uppercase](#rule-uppercase)  
[url](#rule-url)  
[ulid](#rule-ulid)  
[uuid](#rule-uuid)  

#### 숫자 관련 규칙

[between](#rule-between)  
[decimal](#rule-decimal)  
[different](#rule-different)  
[digits](#rule-digits)  
[digits_between](#rule-digits-between)  
[gt](#rule-gt)  
[gte](#rule-gte)  
[integer](#rule-integer)  
[lt](#rule-lt)  
[lte](#rule-lte)  
[max](#rule-max)  
[max_digits](#rule-max-digits)  
[min](#rule-min)  
[min_digits](#rule-min-digits)  
[multiple_of](#rule-multiple-of)  
[numeric](#rule-numeric)  
[same](#rule-same)  
[size](#rule-size)  

#### 배열 관련 규칙

[array](#rule-array)  
[between](#rule-between)  
[contains](#rule-contains)  
[doesnt_contain](#rule-doesnt-contain)  
[distinct](#rule-distinct)  
[in_array](#rule-in-array)  
[in_array_keys](#rule-in-array-keys)  
[list](#rule-list)  
[max](#rule-max)  
[min](#rule-min)  
[size](#rule-size)  

#### 날짜 관련 규칙

[after](#rule-after)  
[after_or_equal](#rule-after-or-equal)  
[before](#rule-before)  
[before_or_equal](#rule-before-or-equal)  
[date](#rule-date)  
[date_equals](#rule-date-equals)  
[date_format](#rule-date-format)  
[different](#rule-different)  
[timezone](#rule-timezone)  

#### 파일 관련 규칙

[between](#rule-between)  
[dimensions](#rule-dimensions)  
[extensions](#rule-extensions)  
[file](#rule-file)  
[image](#rule-image)  
[max](#rule-max)  
[mimetypes](#rule-mimetypes)  
[mimes](#rule-mimes)  
[size](#rule-size)  

#### 데이터베이스 관련 규칙

[exists](#rule-exists)  
[unique](#rule-unique)  

#### 유틸리티 관련 규칙

[anyOf](#rule-anyof)  
[bail](#rule-bail)  
[exclude](#rule-exclude)  
[exclude_if](#rule-exclude-if)  
[exclude_unless](#rule-exclude-unless)  
[exclude_with](#rule-exclude-with)  
[exclude_without](#rule-exclude-without)  
[filled](#rule-filled)  
[missing](#rule-missing)  
[missing_if](#rule-missing-if)  
[missing_unless](#rule-missing-unless)  
[missing_with](#rule-missing-with)  
[missing_with_all](#rule-missing-with-all)  
[nullable](#rule-nullable)  
[present](#rule-present)  
[present_if](#rule-present-if)  
[present_unless](#rule-present-unless)  
[present_with](#rule-present-with)  
[present_with_all](#rule-present-with-all)  
[prohibited](#rule-prohibited)  
[prohibited_if](#rule-prohibited-if)  
[prohibited_if_accepted](#rule-prohibited-if-accepted)  
[prohibited_if_declined](#rule-prohibited-if-declined)  
[prohibited_unless](#rule-prohibited-unless)  
[prohibits](#rule-prohibits)  
[required](#rule-required)  
[required_if](#rule-required-if)  
[required_if_accepted](#rule-required-if-accepted)  
[required_if_declined](#rule-required-if-declined)  
[required_unless](#rule-required-unless)  
[required_with](#rule-required-with)  
[required_with_all](#rule-required-with-all)  
[required_without](#rule-required-without)  
[required_without_all](#rule-required-without-all)  
[required_array_keys](#rule-required-array-keys)  
[sometimes](#validating-when-present)

---

위 목록 다음부터는 규칙별 설명과 예제를 소개합니다. (위 문서가 너무 길어 여기서 마칩니다. 필요하면 이어서 제공 가능합니다.)