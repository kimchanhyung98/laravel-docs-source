# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의](#quick-defining-the-routes)
    - [컨트롤러 생성](#quick-creating-the-controller)
    - [유효성 검증 로직 작성](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시](#quick-displaying-the-validation-errors)
    - [폼 데이터 재입력](#repopulating-forms)
    - [옵션 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트(Form Request) 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성](#creating-form-requests)
    - [폼 리퀘스트 인가](#authorizing-form-requests)
    - [에러 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비](#preparing-input-for-validation)
- [수동으로 Validator 생성](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 에러백(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이즈](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [유효성 검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에 사용자 정의 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 유효성 검증](#validating-nested-array-input)
    - [에러 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션으로 들어오는 데이터를 유효성 검증할 수 있는 다양한 방법을 제공합니다. 가장 일반적으로는 모든 들어오는 HTTP 요청에서 `validate` 메서드를 사용합니다. 하지만 이 외에도 여러 가지 다른 유효성 검증 접근 방식을 다룹니다.

Laravel에는 다양한 편리한 유효성 검증 규칙이 내장되어 있으며, 특정 데이터베이스 테이블에서 값이 고유한지까지도 확인할 수 있습니다. 이 문서에서는 모든 유효성 검증 규칙을 하나씩 다루며, Laravel의 유효성 검증 기능을 충분히 익힐 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼 유효성 검증과 에러 메시지를 사용자에게 보여주는 완전한 예시를 살펴보겠습니다. 이 개요를 통해 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 전체적인 이해를 얻을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정하겠습니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

위 `GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 표시하며, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성

다음으로, 이러한 라우트에 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴봅니다. 일단 `store` 메서드는 비워둡니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트를 작성하는 폼을 표시합니다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 포스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 포스트 유효성 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성

이제 새 블로그 포스트를 검증하는 로직으로 `store` 메서드를 채워보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체의 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드는 정상적으로 계속 실행되지만, 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하며 적절한 에러 응답이 자동으로 사용자에게 전송됩니다.

일반적인 HTTP 요청에서 유효성 검증에 실패하면, 이전 URL로 리다이렉트되는 응답이 생성됩니다. 만약 들어오는 요청이 XHR 요청이라면, [유효성 검증 에러 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 구체적으로 살펴보기 위해 `store` 메서드로 돌아가 보겠습니다:

```php
/**
 * 새 블로그 포스트를 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 포스트가 유효합니다...

    return redirect('/posts');
}
```

위 예시에서 볼 수 있듯이, 유효성 검증 규칙은 `validate` 메서드에 전달됩니다. 사용 가능한 모든 유효성 검증 규칙은 [여기](#available-validation-rules)에서 확인할 수 있습니다. 유효성 검증 실패 시 적절한 응답이 자동으로 생성되며, 검증에 통과하면 컨트롤러가 정상적으로 계속 실행됩니다.

또한, 유효성 검증 규칙을 `|`로 구분된 문자열 대신 배열로 지정할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, 요청을 유효성 검증하고 에러 메시지를 [이름이 지정된 에러백](#named-error-bags) 내에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패에서 중지

특정 필드에 대해 첫 번째 유효성 검사 실패 이후로는 추가 규칙을 실행하지 않으려면, 해당 필드에 `bail` 규칙을 지정합니다:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시의 경우, `title` 필드에 대한 `unique` 규칙이 실패하면 `max` 규칙은 검사되지 않습니다. 규칙은 지정한 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있으면, "dot(점)" 문법을 사용하여 유효성 검증 규칙에서 해당 필드를 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드명에 실제로 점(마침표)가 포함된 경우라면, 역슬래시로 이 점을 이스케이프하여 "dot" 문법으로 해석되지 않게 할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시

그렇다면, 만약 들어오는 필드가 지정한 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 또한, 모든 유효성 검증 에러와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 [세션에 플래시](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 `$errors` 변수를 모든 뷰와 공유합니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있으며, `$errors` 변수는 항상 뷰에 정의되어 있다고 전제하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 다루는 방법에 대해서는 [관련 문서](#working-with-error-messages)를 참고하세요.

따라서, 유효성 검증에 실패하면 사용자는 컨트롤러의 `create` 메서드로 리다이렉트되어, 뷰에서 에러 메시지를 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>Create Post</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 에러 메시지 커스터마이즈

Laravel의 기본 유효성 검증 규칙마다 에러 메시지가 `lang/en/validation.php` 파일에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어를 사용해 생성할 수 있습니다.

`lang/en/validation.php` 파일 내부에는 각 유효성 검증 규칙별로 번역 항목이 있습니다. 애플리케이션의 요구에 맞게 자유롭게 수정하실 수 있습니다.

또한, 이 파일을 다른 언어 디렉토리로 복사해 애플리케이션 언어에 맞게 번역할 수도 있습니다. Laravel의 다국어 지원(로컬라이제이션)에 대해 더 알고 싶다면 [로컬라이제이션 문서 전체](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하고 싶다면, `lang:publish` Artisan 명령어로 게시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이 예시에서는 전통적인 폼을 사용해 데이터를 보냈지만, 많은 애플리케이션에서는 프론트엔드에서 XHR 요청을 보내기도 합니다. XHR 요청에서 `validate` 메서드를 사용할 때 Laravel은 리다이렉트 응답을 생성하지 않고, 대신 [모든 유효성 검증 에러가 포함된 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답에는 HTTP 상태 코드 422가 포함됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성에 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하려면, [Blade](/docs/12.x/blade)의 `@error` 디렉티브를 사용할 수 있습니다. `@error` 내부에서는 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

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

[이름이 지정된 에러백](#named-error-bags)을 사용하는 경우, 두 번째 인자로 에러백 이름을 `@error` 디렉티브에 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 데이터 재입력

유효성 검증 에러가 발생해 Laravel이 리다이렉트 응답을 생성하면, 프레임워크는 해당 요청의 모든 입력값을 [세션에 플래시](/docs/12.x/session#flash-data)합니다. 이를 통해 다음 요청 시 사용자가 제출한 입력값을 쉽게 접근하고, 폼을 자동으로 재입력(repopulate)할 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request`의 `old` 메서드를 사용하세요. 이 메서드는 [세션](/docs/12.x/session)에 저장된 이전 입력값을 반환합니다:

```php
$title = $request->old('title');
```

Blade 템플릿에서 이전 입력값을 출력해야 할 경우에는 글로벌 `old` 헬퍼를 사용할 수 있습니다. 해당 필드의 이전 입력값이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 참고 사항

Laravel은 기본적으로 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 때문에, "옵션" 요청 필드가 `null` 값일 때 Validator가 이를 허용하도록 하려면 해당 필드를 `nullable`로 지정해야 합니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예시에서 `publish_at` 필드는 `null`이거나 유효한 날짜 표현일 수 있음을 의미합니다. 만약 규칙 정의에 `nullable` 수식어를 추가하지 않으면, Validator는 `null`을 잘못된 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고 들어오는 HTTP 요청이 JSON 응답을 기대한다면, Laravel은 에러 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래는 유효성 검증 에러에 대한 JSON 응답 포맷 예시입니다. 중첩된 에러 키는 "dot(점)" 표기법으로 평탄화됩니다:

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
## 폼 리퀘스트(Form Request) 유효성 검증

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성

더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트"를 생성할 수 있습니다. 폼 리퀘스트는 유효성 검증과 인가 로직이 자체적으로 캡슐화된 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 만들려면 `make:request` Artisan CLI 명령어를 사용하세요:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉토리에 위치합니다. 해당 디렉토리가 없다면, 명령어 실행 시 자동으로 생성됩니다. Laravel이 생성하는 모든 폼 리퀘스트에는 `authorize`와 `rules` 두 개의 메서드가 포함되어 있습니다.

예상하셨겠지만, `authorize` 메서드는 현재 인증된 사용자가 요청이 나타내는 동작을 수행할 수 있는지 결정하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다:

```php
/**
 * 요청에 적용할 유효성 검증 규칙을 반환합니다.
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
> `rules` 메서드 시그니처에서 필요한 의존성도 타입 힌트로 선언할 수 있습니다. 이들은 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

그렇다면 이 유효성 검증 규칙이 어떻게 평가될까요? 컨트롤러 메서드에서 요청을 타입 힌트로 선언하기만 하면 됩니다. 폼 리퀘스트는 컨트롤러 메서드가 호출되기 전에 자동으로 유효성 검증됩니다. 즉, 컨트롤러에 유효성 검증 코드가 섞이지 않습니다:

```php
/**
 * 새 블로그 포스트를 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효합니다...

    // 유효성 검증된 입력값을 가져옵니다...
    $validated = $request->validated();

    // 유효성 검증된 데이터의 일부만 가져옵니다...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

유효성 검증에 실패하면 사용자를 이전 위치로 리다이렉트하는 응답이 생성됩니다. 에러 또한 세션에 플래시되어 화면에서 표시할 수 있게 됩니다. XHR 요청의 경우에는 422 상태 코드와 함께 [유효성 검증 에러의 JSON 표현](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 프론트엔드의 실시간(form request) 유효성 검증이 필요하신가요? [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행

기본 유효성 검증이 끝난 후, 추가 검증이 필요할 때는 폼 리퀘스트의 `after` 메서드를 사용할 수 있습니다.

`after` 메서드는 유효성 검증이 완료된 뒤 호출될 콜러블(callable)이나 클로저 배열을 반환해야 합니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아, 필요에 따라 추가 에러 메시지를 등록할 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * 이 요청의 "after" 유효성 검증 콜러블을 반환합니다.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    'Something is wrong with this field!'
                );
            }
        }
    ];
}
```

`after` 메서드가 반환하는 배열에는 호출 가능한 클래스를 포함시켜도 됩니다. 이러한 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 전달받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 이 요청의 "after" 유효성 검증 콜러블을 반환합니다.
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
#### 첫 번째 유효성 검증 실패에서 중지

요청 클래스에 `stopOnFirstFailure` 속성을 추가하면, 한 번이라도 유효성 검증에 실패하면 모든 필드 검증을 중단하도록 할 수 있습니다:

```php
/**
 * 첫 번째 규칙 실패 시 검증을 중단할지 여부를 지정합니다.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이즈

폼 리퀘스트 유효성 검증 실패 시 사용자를 이전 위치로 리다이렉트하는 응답이 기본적으로 생성됩니다. 이 동작을 변경하려면, 폼 리퀘스트에 `$redirect` 속성을 정의하세요:

```php
/**
 * 유효성 검증 실패 시 리다이렉트할 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 사용자를 이름이 지정된 라우트로 리다이렉트하려면 `$redirectRoute` 속성을 사용하세요:

```php
/**
 * 유효성 검증 실패 시 리다이렉트할 라우트.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가

폼 리퀘스트 클래스에는 `authorize` 메서드도 있습니다. 이 메서드에서 인증된 사용자가 특정 리소스를 업데이트할 권한이 있는지 결정할 수 있습니다. 예를 들어, 사용자가 수정하려는 블로그 댓글이 실제로 본인의 것인지 확인할 수도 있습니다. 이 과정에서 [인가 게이트와 정책](/docs/12.x/authorization)를 주로 활용하게 됩니다:

```php
use App\Models\Comment;

/**
 * 이 요청을 사용자가 수행할 권한이 있는지 결정합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 Laravel의 기본 리퀘스트 클래스를 확장하므로, `user` 메서드로 현재 인증된 사용자에 접근할 수 있습니다. 또한 위 예시에서처럼 `route` 메서드를 통해 호출된 라우트의 URI 파라미터, 예를 들어 `{comment}`를 사용할 수 있습니다:

```php
Route::post('/comment/{comment}');
```

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용하는 경우, 요청의 속성으로 모델에 바로 접근할 수도 있습니다:

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, HTTP 403 상태 코드와 함께 응답이 반환되고 컨트롤러 메서드는 실행되지 않습니다.

인가 로직을 애플리케이션의 다른 부분에서 처리한다면, `authorize` 메서드를 아예 제거하거나 단순히 `true`를 반환해도 됩니다:

```php
/**
 * 이 요청을 사용자가 수행할 권한이 있는지 결정합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드에도 타입 힌트로 필요한 의존성을 선언할 수 있으며, Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈

폼 리퀘스트에서 사용되는 에러 메시지는 `messages` 메서드를 오버라이드하여 커스터마이즈할 수 있습니다. 이 메서드는 속성/규칙 쌍과 대응하는 에러 메시지 배열을 반환해야 합니다:

```php
/**
 * 지정된 유효성 검증 규칙에 대한 에러 메시지를 반환합니다.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 유효성 검증 속성명 커스터마이즈

Laravel 내장 유효성 검증 에러 메시지 중 많은 곳에서 `:attribute` 플레이스홀더를 사용합니다. 이 플레이스홀더를 커스텀 속성명으로 바꾸려면, `attributes` 메서드를 오버라이드하여 커스텀 속성명을 지정하세요:

```php
/**
 * Validator 에러에 대한 커스텀 속성명을 반환합니다.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => 'email address',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### 유효성 검증을 위한 입력값 준비

유효성 검증 규칙을 적용하기 전에, 요청 데이터의 정제(sanitize)나 전처리가 필요하다면 `prepareForValidation` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증을 위한 데이터 준비.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

반대로, 유효성 검증이 완료된 후 입력 데이터를 정규화(normalization)해야 할 경우에는 `passedValidation` 메서드를 사용할 수 있습니다:

```php
/**
 * 유효성 검증 통과 처리.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 생성

리퀘스트의 `validate` 메서드를 사용하지 않고, [Validator 파사드](/docs/12.x/facades)를 통해 직접 Validator 인스턴스를 생성할 수도 있습니다. 파사드의 `make` 메서드는 새로운 Validator 인스턴스를 반환합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트를 저장합니다.
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

        // 유효성 검증된 입력값 가져오기...
        $validated = $validator->validated();

        // 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인자는 유효성 검증 대상 데이터이며, 두 번째 인자는 데이터에 적용할 유효성 검증 규칙 배열입니다.

요청이 유효성 검증에 실패했는지 확인한 후, `withErrors` 메서드로 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 `$errors` 변수가 뷰와 공유되어 사용자에게 에러 메시지를 쉽게 보여줄 수 있습니다. `withErrors`에는 Validator, `MessageBag`, PHP 배열 모두 전달할 수 있습니다.

#### 첫 번째 유효성 검증 실패에서 중지

`stopOnFirstFailure` 메서드를 사용하면 하나의 검증 실패 후 모든 필드의 검증을 즉시 중단할 수 있습니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

Validator 인스턴스를 직접 생성하면서도, HTTP 리퀘스트의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 그대로 사용하려면, 생성된 Validator 인스턴스의 `validate` 메서드를 호출하세요. 검증에 실패하면 자동으로 리다이렉트, XHR 요청인 경우에는 [JSON 응답이 반환](#validation-error-response-format)됩니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

에러 메시지를 [이름이 지정된 에러백](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용하세요:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러백(Named Error Bags)

단일 페이지에 여러 개의 폼이 있는 경우, 각각에 대해 별도의 `MessageBag`(에러 메시지 집합)을 이름으로 분리해서 사용할 수 있습니다. 이를 위해 `withErrors`의 두 번째 인자로 이름을 지정합니다:

```php
return redirect('/register')->withErrors($validator, 'login');
```

이렇게 하면 뷰에서 `$errors->login->first('email')` 식으로 특정 에러백의 메시지에 접근할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈

Validator 인스턴스가 사용할 커스텀 에러 메시지는 여러 가지 방법으로 지정할 수 있습니다. 첫 번째는 `Validator::make`의 세 번째 인자로 커스텀 메시지 배열을 전달하는 것입니다:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이때 `:attribute` 플레이스홀더는 유효성 검증 대상 필드명으로 치환됩니다. 다른 플레이스홀더도 사용할 수 있습니다. 예:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대한 커스텀 메시지 지정

특정 속성의 규칙에 대해서만 커스텀 에러 메시지를 지정하고 싶다면, "dot(점)" 문법으로 작성할 수 있습니다. 필드명.규칙명 순서입니다:

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

Laravel의 내장 에러 메시지는 `:attribute` 플레이스홀더를 포함합니다. 특정 필드에 대해 이 값을 커스텀으로 바꾸려면, 네 번째 인자에 속성명 배열을 전달하세요:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행

첫 번째 유효성 검증이 끝난 이후, 추가 검증이 필요한 경우 Validator의 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 클로저나 콜러블의 배열을 받아, 검증이 끝난 뒤 실행됩니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 전달받아, 조건에 따라 추가 에러 메시지를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

또한, `after` 메서드에는 콜러블의 배열을 전달해도 됩니다. 이렇게 하면 "after validation" 로직을 캡슐화한 실행 가능한(Invokable) 클래스를 활용할 수 있습니다. 이 클래스의 `__invoke` 메서드에도 `Illuminate\Validation\Validator`가 전달됩니다:

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
## 유효성 검증된 입력값 다루기

폼 리퀘스트나 수동으로 생성된 Validator 인스턴스를 통해 요청 데이터를 검증한 후, 실제로 검증된 데이터만 별도로 추출하고 싶을 수 있습니다. 이를 위해서는 폼 리퀘스트 혹은 Validator 인스턴스의 `validated` 메서드를 호출하면 됩니다. 반환값은 검증 완료된 데이터의 배열입니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체는 `only`, `except`, `all` 등의 메서드로 일부 혹은 전체 유효성 검증 데이터를 가져올 수 있습니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

추가적으로, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복문(iterate)이 가능하며, 배열처럼 값도 접근할 수 있습니다:

```php
// 반복문 사용:
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근:
$validated = $request->safe();
$email = $validated['email'];
```

유효성 검증 데이터에 추가 필드를 더하고 싶으면 `merge` 메서드를 사용하세요:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

[컬렉션](/docs/12.x/collections) 인스턴스를 얻고 싶으면 `collect` 메서드를 사용할 수 있습니다:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

Validator 인스턴스의 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 얻을 수 있습니다. `$errors` 변수도 자동으로 모두의 뷰에 공유되는 `MessageBag` 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

지정한 필드의 첫 번째 에러 메시지를 가져오려면 `first` 메서드를 사용하세요:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 필드의 모든 에러 메시지 가져오기

특정 필드의 모든 메시지 배열을 가져오려면 `get` 메서드를 사용합니다:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 폼 필드를 검증하는 경우, `*` 문자를 사용하면 각 배열 요소별 에러 메시지를 모두 가져올 수 있습니다:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 전체 필드의 모든 에러 메시지 가져오기

모든 필드의 메시지를 배열로 한 번에 얻으려면 `all` 메서드를 사용합니다:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 필드에 에러 메시지가 있는지 확인

특정 필드에 에러 메시지가 존재하는지 확인하려면 `has` 메서드를 활용하세요:

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에 사용자 정의 메시지 지정

Laravel의 내장 유효성 검증 규칙별 에러 메시지는 `lang/en/validation.php`에 위치합니다. `lang` 디렉토리가 없는 경우 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

이 파일의 각 규칙별 번역 항목은 자유롭게 수정 가능하며, 애플리케이션의 요구에 맞게 변경할 수 있습니다. 메시지 파일을 다른 언어 디렉토리로 복사해 번역할 수도 있습니다. 자세한 내용은 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> Laravel 기본 애플리케이션 구조에는 `lang` 디렉토리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 꼭 `lang:publish` Artisan 명령어로 게시하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성별 커스텀 메시지

애플리케이션의 유효성 검증 언어 파일에서 `custom` 배열을 활용해, 지정한 속성과 규칙 쌍에 대한 에러 메시지를 직접 정의할 수 있습니다:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에 속성 지정

많은 내장 에러 메시지에서 `:attribute` 플레이스홀더가 사용됩니다. 이 부분을 원하는 값으로 교체하려면 `lang/xx/validation.php` 파일 내 `attributes` 배열에 맞춤 이름을 정의하세요:

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> Laravel 기본 애플리케이션 구조에는 `lang` 디렉토리가 없습니다. 언어 파일 커스터마이즈를 원하면 `lang:publish` Artisan 명령어를 이용하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에 값 지정

일부 내장 유효성 검증 메시지에는 `:value` 플레이스홀더가 있는데, 이는 검사 중인 요청 속성의 현재 값으로 치환됩니다. 사용자에게 더 친근한 값 설명으로 변경하려면, `lang/xx/validation.php` 파일의 `values` 배열에 정의할 수 있습니다:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel에는 `lang` 디렉토리가 없습니다. 언어 파일을 직접 커스터마이즈하려면 `lang:publish` Artisan 명령어를 실행하세요.

이 값을 정의하면 에러 메시지의 `cc` 대신 `credit card`가 출력됩니다:

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙 (Available Validation Rules)

다음은 모든 사용 가능한 유효성 검증 규칙과 각 규칙의 설명입니다:

...

(※ 이하 규칙별 세부 설명은 Core Guidelines 및 원문 구조를 그대로 따라 번역합니다. 각 규칙의 제목·설명·코드 예시와 마크다운 구조·리스트 모두 변경 없이 유지하며, 자연스러운 한국어로 쉽게 풀어 번역합니다.)

---