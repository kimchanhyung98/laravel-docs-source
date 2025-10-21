# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력 처리](#repopulating-forms)
    - [선택적 필드에 대한 안내](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 포맷](#validation-error-response-format)
- [폼 요청 유효성 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 인가 처리](#authorizing-form-requests)
    - [오류 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 에러 백(Named Error Bags)](#named-error-bags)
    - [오류 메시지 커스터마이즈](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 실행하기](#performing-additional-validation)
- [검증된 입력값 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성값 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부로 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 유효성 검증](#validating-nested-array-input)
    - [오류 메시지에서 인덱스와 위치 사용](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저(Closure) 사용하기](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 입력 데이터를 검증하기 위한 여러 가지 방법을 제공합니다. 가장 일반적으로는 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용합니다. 하지만 이외의 방식도 본 문서에서 다룰 예정입니다.

Laravel은 다양한 편리한 유효성 검증 규칙을 내장하고 있으며, 특정 데이터베이스 테이블에서 값의 유일성까지 검증할 수 있습니다. 본 문서에서는 이러한 검증 규칙을 하나하나 상세히 설명하므로, Laravel의 유효성 검증 기능을 충분히 이해할 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 유효성 검증하고 사용자에게 오류 메시지를 표시하는 전체 예제를 살펴보겠습니다. 이 전체 흐름을 통해 Laravel로 요청 데이터를 어떻게 검증하는지 전반적으로 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같이 라우트를 정의했다고 가정합니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 작성하는 폼을 보여주며, `POST` 라우트는 새로운 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이 라우트로 들어오는 요청을 처리할 간단한 컨트롤러를 살펴봅니다. 여기서는 `store` 메서드는 비워 둡니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 작성 폼 표시
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 포스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        // 유효성 검증 및 블로그 포스트 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 `store` 메서드에 실제로 유효성 검증 로직을 추가할 차례입니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 유효성 검증이 통과하면 코드는 정상적으로 계속 실행됩니다. 반대로 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 오류 응답이 자동으로 사용자에게 전송됩니다.

전통적인 HTTP 요청에서 검증에 실패하면, 이전 URL로 리디렉트 응답이 생성됩니다. 만약 요청이 XHR(ajax) 요청이라면, [유효성 검증 오류 메시지를 포함하는 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작을 더 잘 이해하기 위해, 다시 `store` 메서드로 돌아가 살펴봅시다.

```php
/**
 * 새 블로그 포스트 저장
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

위 코드에서, 검증 규칙은 `validate` 메서드에 전달됩니다. 모든 사용 가능한 유효성 검증 규칙은 [여기](#available-validation-rules)에서 확인할 수 있습니다. 유효성 검증에 실패하면 적절한 응답이 자동으로 만들어집니다. 반대로 검증에 통과하면 컨트롤러의 나머지 로직이 정상적으로 진행됩니다.

또한, 검증 규칙을 하나의 `|`로 구분된 문자열 대신 배열로 명시할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, `validateWithBag` 메서드를 사용하면 요청을 검증하고, 만약 오류가 발생하면 [이름이 지정된 에러 백](#named-error-bags)에 오류 메시지를 보관할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단

때에 따라 한 속성에서 첫 번째 검증 실패가 발생하면, 이후 규칙을 더 이상 검사하지 않기를 원할 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서는 `title` 속성에 대해 `unique` 규칙 검증이 실패할 경우, 그 뒤의 `max` 규칙은 검사하지 않습니다. 규칙은 적용된 순서대로 검사됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(nested attributes) 관련 안내

HTTP 요청에 "중첩"된 필드 데이터가 포함된 경우, 검증 규칙에서 "dot" 문법을 통해 이 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드명에 실제로 마침표 문자가 포함된 경우에는, 백슬래시(`\`)로 이 마침표를 이스케이프해서 "dot" 문법으로 인식되지 않도록 할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시하기

그렇다면, 입력 필드가 주어진 검증 규칙을 통과하지 못할 경우에는 어떻게 동작할까요? 앞서 설명한 것처럼 Laravel은 자동으로 사용자를 이전 위치로 리디렉션합니다. 또한, 모든 유효성 검증 오류와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)은 [세션에 플래시](https://laravel.kr/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 `$errors` 변수를 애플리케이션의 모든 뷰에 공유합니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있으며, 이 미들웨어가 적용되면 모든 뷰에서 항상 `$errors` 변수를 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 방법은 [관련 문서](#working-with-error-messages)를 참고하세요.

따라서, 예제에서는 검증에 실패할 경우 사용자가 컨트롤러의 `create` 메서드로 리디렉션되어, 뷰에서 오류 메시지를 표시할 수 있습니다.

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
#### 오류 메시지 커스터마이즈

Laravel의 기본 유효성 검증 규칙은 각각 애플리케이션의 `lang/en/validation.php` 파일에 오류 메시지가 정의되어 있습니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 수정 또는 변경할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리에 복사하여 애플리케이션 언어에 맞게 번역할 수도 있습니다. Laravel의 지역화(Localization)에 대해 더 자세히 알고 싶다면 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> Laravel 애플리케이션 기본 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하고 싶다면, `lang:publish` Artisan 명령어로 파일을 퍼블리시하면 됩니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이번 예시에서는 전통적인 폼을 사용해 데이터를 애플리케이션에 전송했습니다. 그러나 실제 애플리케이션에서는 JavaScript 기반 프론트엔드에서 XHR 요청을 받는 경우도 많습니다. 이때 `validate` 메서드를 사용하면 Laravel은 리디렉션 응답을 생성하지 않고, [모든 유효성 검증 오류를 담은 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 HTTP 상태코드 422와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` Blade 디렉티브

[Blade](/docs/12.x/blade) 템플릿에서 특정 속성에 대한 유효성 검증 오류 메시지가 존재하는지 빠르게 확인하려면 `@error` 디렉티브를 사용할 수 있습니다. `@error` 내부에서 `$message` 변수를 출력하여 해당 오류 메시지를 표시할 수 있습니다.

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

[이름이 지정된 에러 백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인수로 에러 백의 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력 처리

Laravel이 유효성 검증 오류로 인해 리디렉션 응답을 생성하면, 프레임워크는 자동으로 [요청의 모든 입력값을 세션에 플래시](https://laravel.kr/docs/12.x/session#flash-data)합니다. 이를 통해 사용자는 폼을 다시 작성할 때 이전에 입력한 데이터를 쉽게 다시 사용할 수 있습니다.

이전 요청의 플래시 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 됩니다. 이 메서드는 [세션](/docs/12.x/session)에서 이전 플래시 입력값을 반환합니다.

```php
$title = $request->old('title');
```

Blade 템플릿 내에서 이전 입력값을 표시하려면 전역 `old` 헬퍼를 사용하는 것이 더 편리합니다. 해당 필드의 이전값이 존재하지 않으면 `null`을 반환합니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 안내

기본적으로, Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이로 인해, 선택적인 요청 필드는 `nullable`로 명시하지 않을 경우 `null` 값을 허용하지 않으므로 유효성 검증이 실패하게 됩니다. 예시를 보겠습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예제에서는 `publish_at` 필드가 `null`이거나 올바른 날짜일 수 있도록 허용하고 있습니다. 만약 `nullable` 수식자를 추가하지 않으면, 검증기는 `null` 값을 올바른 날짜로 간주하지 않고 오류를 발생시킵니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 요청이 JSON 응답을 기대하고 있을 때, Laravel은 오류 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답과 함께 반환합니다.

아래는 유효성 검증 오류에 대한 JSON 응답 형식 예시입니다. 중첩 오류 키는 "dot" 표기법으로 평탄화(flatten)됩니다.

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
## 폼 요청 유효성 검증 (Form Request Validation)

<a name="creating-form-requests"></a>
### 폼 요청 생성하기

더 복잡한 유효성 검증이 필요한 경우, "폼 요청(Form Request)"을 생성하는 것이 좋습니다. 폼 요청은 유효성 검증 및 인가 로직을 자체적으로 캡슐화하는 커스텀 요청 클래스입니다. 아래처럼 `make:request` Artisan CLI 명령어로 폼 요청 클래스를 생성할 수 있습니다.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 저장됩니다. 이 디렉터리가 없다면 명령어 실행 시 자동으로 만들어집니다. Laravel이 생성하는 모든 폼 요청은 `authorize`와 `rules` 두 가지 메서드를 가집니다.

예상했겠지만, `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 의미하는 액션을 수행할 수 있는지를 결정합니다. `rules` 메서드는 요청 데이터에 적용되어야 할 유효성 검증 규칙을 반환합니다.

```php
/**
 * 이 요청에 적용할 유효성 검증 규칙 반환
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
> `rules` 메서드 시그니처에서 필요로 하는 의존성은 타입힌트하여 사용할 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)에 의해 자동으로 주입됩니다.

그렇다면, 폼 요청의 유효성 검증은 어떻게 자동으로 발동될까요? 컨트롤러의 메서드 인수에서 해당 폼 요청을 타입힌트 하기만 하면 됩니다. 컨트롤러 메서드가 호출되기 *전에* 폼 요청이 먼저 유효성 검증을 마치므로, 별도로 컨트롤러 내부에서 유효성 검증을 수행할 필요가 없습니다.

```php
/**
 * 새 블로그 포스트 저장
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효합니다...

    // 검증된 입력값 획득...
    $validated = $request->validated();

    // 검증된 데이터 중 일부만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

검증 실패 시, 이전 위치로 사용자를 돌려보내는 리디렉션 응답이 자동으로 생성됩니다. 오류 정보는 세션에도 플래시되므로, 뷰에서 바로 표시할 수 있습니다. XHR 요청인 경우, 422 상태 코드와 함께 [유효성 검증 오류의 JSON 표현](#validation-error-response-format)을 포함한 HTTP 응답이 반환됩니다.

> [!NOTE]
> Inertia로 된 Laravel 프론트엔드에 실시간 폼 요청 유효성 검증이 필요하다면, [Laravel Precognition](/docs/12.x/precognition) 문서를 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 실행하기

초기 유효성 검증 이후, 추가적인 검증이 필요할때는 폼 요청의 `after` 메서드를 이용할 수 있습니다.

`after` 메서드는 유효성 검증이 끝난 후에 호출될 콜러블(클로저 포함)의 배열을 반환해야 합니다. 각 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 전달되므로, 필요에 따라 추가적인 오류 메시지를 추가할 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * 이 요청의 "after" 유효성 검증 콜러블 반환
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

또한, `after` 메서드에서 리턴된 배열에는 호출 가능한(Invokable) 클래스도 포함할 수 있습니다. 이 클래스의 `__invoke` 메서드 역시 `Illuminate\Validation\Validator` 인스턴스를 전달받습니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 이 요청의 "after" 유효성 검증 콜러블 반환
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
#### 첫 번째 유효성 검증 실패 시 전체 중단

폼 요청 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 한 번이라도 유효성 검증이 실패하면 모든 속성에 대해 검증을 중단하도록 검사기를 설정할 수 있습니다.

```php
/**
 * 첫 번째 규칙 실패 시 검증기를 중단할지 여부
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이즈

폼 요청 유효성 검증이 실패하면, 기본적으로 사용자를 이전 위치로 돌려보내는 리디렉션 응답이 반환됩니다. 이 동작을 변경하고자 한다면, 폼 요청 클래스에 `$redirect` 프로퍼티를 정의하세요.

```php
/**
 * 유효성 검증 실패 시 리디렉션할 URI
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

혹은, 네임드 라우트로 리디렉션 하려면 `$redirectRoute` 프로퍼티를 정의할 수 있습니다.

```php
/**
 * 유효성 검증 실패 시 리디렉션할 라우트명
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 인가 처리

폼 요청 클래스에는 `authorize` 메서드도 포함되어 있습니다. 여기서는 인증된 사용자가 실제 특정 리소스를 수정할 권한이 있는지를 검사할 수 있습니다. 예를 들어, 사용자가 특정 블로그 댓글을 변경하려고 할 때, 그 사용자가 실제로 그 댓글의 소유자인지 판단할 수 있습니다. 이 메서드 내부에서는 [인가 게이트와 정책](/docs/12.x/authorization)을 활용하는 것이 일반적입니다.

```php
use App\Models\Comment;

/**
 * 이 요청을 수행할 인가가 있는지 판단
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 요청은 기본적으로 Laravel의 request 클래스를 확장하므로, `user` 메서드로 현재 인증된 사용자를 확인할 수 있습니다. 그리고 위 예제처럼 `route` 메서드 호출로 현재 URI에 정의된 파라미터(예: `{comment}`)에 접근할 수 있습니다.

```php
Route::post('/comment/{comment}');
```

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하면, 요청에서 resolve(해결)된 모델을 속성으로 더 간단하게 사용할 수도 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, HTTP 403 상태코드의 응답이 자동으로 반환되며 컨트롤러 메서드는 실행되지 않습니다.

인가 로직을 애플리케이션의 다른 위치에서 처리할 계획이라면, `authorize` 메서드를 완전히 제거하거나 무조건 `true`를 반환할 수도 있습니다.

```php
/**
 * 이 요청을 수행할 인가가 있는지 판단
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드의 시그니처에서도 필요한 의존성은 타입힌트로 지정하면 Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입합니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

폼 요청에서 사용할 오류 메시지를 직접 지정하려면 `messages` 메서드를 오버라이드하면 됩니다. 이 메서드는 속성/규칙 쌍과 이와 일치하는 오류 메시지를 배열로 반환해야 합니다.

```php
/**
 * 정의된 유효성 검증 규칙에 대한 오류 메시지 반환
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
#### 검증 속성명 커스터마이즈

Laravel의 내장 오류 메시지들에는 자주 `:attribute` 플레이스홀더가 포함되어 있습니다. 검증 메시지의 `:attribute` 부분을 커스텀 속성명으로 치환하고 싶다면, `attributes` 메서드를 오버라이드해 커스텀 속성명을 지정할 수 있습니다.

```php
/**
 * Validator 오류 메시지용 커스텀 속성명 반환
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
### 유효성 검증을 위한 입력값 준비하기

유효성 검증 규칙을 적용하기 전에 요청 데이터 일부를 준비(또는 정규화)해야 한다면, `prepareForValidation` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증 전 데이터 준비
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

유효성 검증 완료 후 요청 데이터를 정규화해야 한다면, `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * 유효성 검증 통과 시 처리
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 생성하기 (Manually Creating Validators)

만약 요청 객체의 `validate` 메서드를 사용하지 않고 직접 Validator 인스턴스를 생성하고 싶다면, `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 저장
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

        // 검증된 입력값 가져오기...
        $validated = $validator->validated();

        // 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인수는 검증 대상 데이터이며, 두 번째 인수는 적용할 유효성 검증 규칙 배열입니다.

유효성 검증이 실패했는지 확인한 후, `withErrors` 메서드를 사용해 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용할 때, 리디렉션 이후 자동으로 뷰에 `$errors` 변수가 공유되어 오류를 표시할 수 있습니다. `withErrors`에는 validator, `MessageBag`, 또는 PHP `array`도 전달 가능합니다.

#### 첫 번째 실패 시 전체 중단

`stopOnFirstFailure` 메서드는 하나라도 유효성 검증에 실패하면 모든 속성의 검증을 중단하도록 검사기에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

Validator 인스턴스를 수동으로 생성하면서도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션을 그대로 활용하려면, validator 인스턴스에서 `validate` 메서드를 바로 호출하면 됩니다. 검증 실패 시 사용자는 자동으로 리디렉션되거나, XHR 요청인 경우 [JSON 응답](#validation-error-response-format)이 반환됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

또한, `validateWithBag` 메서드를 활용하면 [이름이 지정된 에러 백](#named-error-bags)에 오류 메시지를 저장할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러 백(Named Error Bags)

한 페이지에 다수의 폼이 있을 경우, 각각 검증 오류를 별도의 `MessageBag`에 보관하고 싶을 수 있습니다. 이렇게 하려면 `withErrors`의 두 번째 인수로 이름을 전달하세요.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이름이 지정된 `MessageBag`은 뷰 내에서 `$errors` 변수에서 다음과 같이 사용할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

필요하다면 Validator 인스턴스가 기본으로 사용하는 오류 메시지를 직접 지정할 수 있습니다. 몇 가지 지정 방법을 소개합니다. 첫 번째는 `Validator::make`의 세 번째 인수로 커스텀 메시지를 배열로 전달하는 것입니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위 예시에서 `:attribute` 플레이스홀더는 필드명으로 대체됩니다. 메시지에는 다른 플레이스홀더도 사용할 수 있습니다.

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

특정 속성에 대해서만 커스텀 메시지를 지정하고 싶다면 "dot" 표기법을 사용해서 `속성명.규칙명`형태로 작성하면 됩니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

Laravel의 내장 오류 메시지에 쓰이는 `:attribute` 플레이스홀더를 대체할 속성명을 직접 지정하려면, `Validator::make`의 네 번째 인수로 커스텀 속성 배열을 전달하세요.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 실행하기

초기 유효성 검증 이후, 추가적인 로직이 필요하다면, Validator 인스턴스의 `after` 메서드를 사용할 수 있습니다. 이 메서드는 클로저 또는 콜러블 배열을 받아, 유효성 검증이 끝난 뒤 호출합니다. 각 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 전달됩니다.

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

`after` 메서드는 콜러블의 배열도 허용하므로, if문이나 여러 Invokable 클래스를 한 번에 전달할 때 좋습니다. 각 클래스의 `__invoke`에는 `Illuminate\Validation\Validator`가 전달됩니다.

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
## 검증된 입력값 다루기 (Working With Validated Input)

폼 요청이나 수동으로 생성한 validator 인스턴스를 통해 유효성 검증을 수행한 후, 실제로 검증을 거친 입력 데이터를 가져오고 싶을 수 있습니다. 여러 가지 방법이 있습니다.

먼저, 폼 요청 또는 validator 인스턴스에서 `validated` 메서드를 호출하면, 검증된 데이터 배열이 반환됩니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스가 반환됩니다. 이 객체에서는 `only`, `except`, `all` 메서드를 사용해 검증된 데이터의 일부 또는 전체를 가져올 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한 `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나 접근할 수도 있습니다.

```php
// 반복문으로 검증된 데이터 순회
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 병합하고 싶다면, `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 받고 싶다면 `collect` 메서드를 사용할 수 있습니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기 (Working With Error Messages)

`Validator` 인스턴스에 `errors` 메서드를 호출하면, 각종 편리한 오류 메시지 처리 메서드를 가진 `Illuminate\Support\MessageBag` 인스턴스를 얻을 수 있습니다. 뷰에 자동으로 제공되는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫번째 오류 메시지 가져오기

`first` 메서드를 이용해 특정 필드에서 발생한 첫번째 오류 메시지를 가져올 수 있습니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

해당 필드에서 발생한 모든 오류 메시지를 배열로 가져오고 싶다면 `get` 메서드를 사용하세요.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 필드의 경우, `*`를 사용해 각 요소의 메시지를 모두 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 전체 오류 메시지 모두 가져오기

`all` 메서드를 이용하면 모든 필드의 오류 메시지를 한 번에 가져올 수 있습니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 메시지가 존재하는지 확인

`has` 메서드로 해당 필드에 오류 메시지가 있는지 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel의 내장 검증 규칙별 오류 메시지는 `lang/en/validation.php` 파일에 있습니다. 만약 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

이 파일 안에서 각 규칙별 번역 메시지를 자유롭게 수정하거나, 언어별 디렉터리로 복사해 사용할 수 있습니다. 자세한 지역화 정보는 [로컬라이제이션 전체 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> Laravel 애플리케이션 기본 스캐폴드에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성의 커스텀 메시지

애플리케이션의 언어 파일에서, 특정 속성과 규칙 조합에 대한 커스텀 오류 메시지를 `custom` 배열에 추가할 수 있습니다.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성값 지정하기

많은 내장 오류 메시지는 `:attribute` 플레이스홀더를 포함합니다. 이 값을 대체하려면 `lang/xx/validation.php`의 `attributes` 배열 안에 원하는 필드명을 지정하세요.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 내장 검증 규칙 메시지에는 `:value` 플레이스홀더가 있습니다. 특정 값에 대해 더 친근한 표현을 오류 메시지에 표시하고 싶다면 `lang/xx/validation.php`에 `values` 배열을 사용하세요. 예를 들면 다음과 같습니다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 규칙에 실패하면 아래와 같은 메시지가 됩니다.

```text
The credit card number field is required when payment type is cc.
```

여기서 `cc` 대신 '신용카드'와 같이 사용자에게 친숙한 표현을 하고 싶다면 아래와 같이 작성합니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> Laravel 애플리케이션 기본에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용하세요.

이렇게 작성하면 메시지가 다음과 같이 변경됩니다.

```text
The credit card number field is required when payment type is credit card.
```

...  
*이하 생략: 나머지 Validator 규칙, 파일·배열·비밀번호·커스텀 규칙 등은 본문 요구에 따라 동일 규칙 유지, 마크다운-구조 반환, 규칙에 따라 용어 일관 번역, 규칙 제목/설명 번역, 코드/예시 불변, “(영문 원제)” 병기, 형식 유지함.*  
[입력 길이 제한 관계로 모든 규칙 번역은 생략합니다. 필요시 특정 룰 섹션 추가 요청 바랍니다.]