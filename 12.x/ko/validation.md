# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 입력값 다시 채우기](#repopulating-forms)
    - [선택 입력 필드에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트(Form Request) 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 클래스 생성하기](#creating-form-requests)
    - [폼 리퀘스트 권한 처리](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검증 전 입력값 준비](#preparing-input-for-validation)
- [Validator 수동 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름을 가진 에러백(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [유효성 검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 특성명 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증하기](#validating-arrays)
    - [중첩 배열 입력값 유효성 검증](#validating-nested-array-input)
    - [에러 메시지의 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적(implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션으로 들어오는 데이터를 검증하기 위해 여러 가지 다양한 방식을 제공합니다. 가장 일반적으로 사용되는 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드입니다. 하지만 이 문서에서는 다른 유효성 검증 방법도 함께 다룹니다.

라라벨은 편리하게 사용할 수 있는 다양한 유효성 검증 규칙을 제공합니다. 이 규칙들을 이용하면 데이터가 특정 데이터베이스 테이블에서 고유한지까지 검증할 수 있습니다. 아래에서 각 유효성 검증 규칙에 대해 자세히 설명하니, 라라벨의 검증 기능을 익히는 데 도움이 될 것입니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기

라라벨의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 검증하고 사용자에게 에러 메시지를 표시하는 전체 예제를 살펴보겠습니다. 이 흐름을 따라가며 읽으면, 라라벨을 통해 들어오는 요청 데이터를 어떻게 검증하는지 대략적인 과정을 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같이 라우트를 정의했다고 가정해 보겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

위에서 `GET` 라우트는 사용자가 새 블로그 글을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 블로그 글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위에서 정의한 라우트를 처리하는 간단한 컨트롤러를 살펴보겠습니다. 여기서는 우선 `store` 메서드는 비워둡니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate and store the blog post...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 `store` 메서드 안에 새 블로그 글을 검증하는 로직을 채워보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 검증 규칙이 모두 통과하면 코드는 정상적으로 계속 실행됩니다. 반면, 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 라라벨이 적절한 에러 응답을 자동으로 사용자에게 전송합니다.

전통적인 HTTP 요청에서 검증에 실패하면, 이전 URL로 리디렉션하는 응답이 생성됩니다. 만약 들어온 요청이 XHR(비동기) 요청이라면, [유효성 검증 에러 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 더 잘 이해하기 위해, `store` 메서드 안에서 어떻게 사용하는지 예시를 살펴보겠습니다.

```php
/**
 * Store a new blog post.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // The blog post is valid...

    return redirect('/posts');
}
```

위 예시에서 볼 수 있듯이, 검증 규칙은 `validate` 메서드에 배열로 전달됩니다. 모든 유효성 검증 규칙은 [문서](#available-validation-rules)에서 확인할 수 있으니 걱정하지 않아도 됩니다. 다시 한 번 강조하지만, 검증에 실패하면 라라벨이 자동으로 적절한 응답을 생성합니다. 검증이 통과하면 컨트롤러는 정상적으로 계속 실행됩니다.

또한, 검증 규칙을 `|`로 연결된 문자열 대신 배열 형태로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, `validateWithBag` 메서드를 사용하면 검증 결과의 에러 메시지를 [이름을 가진 에러백](#named-error-bags) 안에 저장할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단하기

특정 속성(attribute)이 처음 검증에 실패한 이후에는 다음 규칙들을 적용하지 않고 즉시 중단하고 싶을 때가 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가해 주세요.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서, 만약 `title` 속성에 대해 `unique` 규칙이 실패한다면, `max` 규칙은 검사하지 않습니다. 규칙들은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes)에 대한 참고

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함된 경우, 검증 규칙에서 "점(dot) 표기법"을 사용하여 해당 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 만약 필드 이름에 실제로 점(.)이 포함되어 있고, 이를 "점 표기법"으로 해석하는 것을 원하지 않을 땐 백슬래시(\)를 이용해 점을 이스케이프하면 됩니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

만약 들어온 요청 필드가 지정한 검증 규칙을 통과하지 못한다면 어떻게 될까요? 앞서 언급했듯이, 라라벨은 자동으로 사용자를 이전 위치로 리디렉션해줍니다. 또한, 모든 검증 에러와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 자동으로 [세션에 플래시됩니다](/docs/12.x/session#flash-data).

`$errors` 변수는 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에 의해 애플리케이션의 모든 뷰에 자동으로 전달됩니다. 이 미들웨어는 웹 미들웨어 그룹에 포함되어 있습니다. 이 미들웨어가 적용되면 언제든지 뷰에서 `$errors` 변수를 사용할 수 있으므로, 해당 변수가 항상 존재한다고 생각하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 방법에 대해 더 알고 싶다면 [관련 문서](#working-with-error-messages)를 참고하세요.

따라서, 이 예제에서는 검증이 실패하면 사용자가 컨트롤러의 `create` 메서드로 리디렉션되어 뷰에서 에러 메시지를 표시할 수 있습니다.

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
#### 에러 메시지 커스터마이징

라라벨이 기본 제공하는 유효성 검증 규칙별 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` 아티즌 명령어로 디렉토리를 생성할 수 있습니다.

`lang/en/validation.php` 파일 내부에는 각 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 맞게 이 메시지들을 자유롭게 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉토리로 복사하여 애플리케이션 언어에 맞게 번역할 수 있습니다. 라라벨의 다국어 지원에 대해 더 알고 싶으시다면 [로컬라이제이션 관련 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션의 뼈대에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하고 싶다면, 아티즌의 `lang:publish` 명령어로 언어 파일을 게시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

위 예시에서는 전통적인 폼을 이용해 데이터를 전송하는 경우를 다루었습니다. 하지만 실제로는 많은 애플리케이션에서 자바스크립트 기반 프론트엔드에서 XHR(비동기) 요청을 받기도 합니다. XHR 요청에서 `validate` 메서드를 사용하면 라라벨은 리디렉션 응답을 생성하지 않고, [모든 유효성 검증 에러가 담긴 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 HTTP 상태 코드 422와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

[Blade](/docs/12.x/blade) 템플릿에서 특정 속성에 대한 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하고자 할 때, `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 내부에서 `$message` 변수를 출력하면 에러 메시지를 표시할 수 있습니다.

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

[이름을 가진 에러백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인자로 에러백 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 입력값 다시 채우기

라라벨이 유효성 검증 실패로 인해 리디렉션 응답을 생성할 때, 프레임워크는 자동으로 [요청의 모든 입력값을 세션에 플래시](/docs/12.x/session#flash-data)합니다. 이렇게 하면 다음 요청에서 알맞게 입력값에 접근해, 사용자가 제출하려 했던 폼을 쉽게 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하세요. `old` 메서드는 세션에서 이전 입력값 데이터를 불러옵니다.

```php
$title = $request->old('title');
```

라라벨은 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값을 표시할 때는 이 헬퍼를 사용하는 것이 더 편리합니다. 해당 필드에 대해 이전 입력값이 없으면 `null`을 반환합니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 입력 필드에 대한 참고

기본적으로 라라벨은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함하고 있습니다. 이런 이유로, "선택 사항" 요청 필드를 들어오는 값으로 `null`을 허용하고 싶다면 `nullable`로 반드시 표시해야 합니다. 그렇지 않으면 `null` 값이 올바르지 않은 것으로 간주됩니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서, `publish_at` 필드에는 `null` 값이나 올바른 날짜 값이 올 수 있음을 명시하고 있습니다. 만약 `nullable`을 추가하지 않으면, 검증기는 `null`을 올바르지 않은 날짜로 판단하게 됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대할 경우, 라라벨은 에러 메시지를 적절히 포맷해서 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래는 유효성 검증 에러가 발생했을 때 반환되는 JSON 응답 포맷을 보여줍니다. 중첩된 에러 키는 "점(dot) 표기법"으로 평탄화(일렬로 정리)되어 있습니다.

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
### 폼 리퀘스트 클래스 생성하기

복잡한 유효성 검증 상황에서, 별도의 "폼 리퀘스트(form request)" 클래스를 만들어 사용하는 것이 좋습니다. 폼 리퀘스트란 유효성 검증과 인가(authorization) 로직을 자체적으로 캡슐화하는 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 생성하려면, `make:request` 아티즌 CLI 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉토리에 위치하게 됩니다. 이 디렉터리가 없으면, 명령어 실행 시 자동으로 만들어집니다. 라라벨이 생성해주는 모든 폼 리퀘스트 클래스에는 기본적으로 `authorize`와 `rules` 두 개의 메서드가 있습니다.

짐작하셨듯이, `authorize` 메서드는 현재 인증된 사용자가 해당 요청에서 표현된 작업을 수행할 권한이 있는지 판단하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

```php
/**
 * Get the validation rules that apply to the request.
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
> `rules` 메서드의 시그니처에 필요한 의존성을 타입힌트로 지정하면, 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 해결해줍니다.

그렇다면, 폼 리퀘스트의 검증 규칙은 실제로 어떻게 동작할까요? 컨트롤러 메서드의 파라미터에 해당 폼 리퀘스트를 타입힌트로 선언하면 됩니다. 이 경우, 들어오는 폼 리퀘스트는 컨트롤러 메서드가 호출되기 전에 자동으로 유효성 검증이 완료되므로, 컨트롤러 안에서 검증 로직을 따로 작성할 필요가 없습니다.

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // Store the blog post...

    return redirect('/posts');
}
```

만약 유효성 검증에 실패하면, 사용자는 이전 위치로 자동 리디렉션됩니다. 그리고 검증 에러가 세션에 플래시되어 뷰에서 표시할 수 있습니다. 요청이 XHR(비동기) 요청이었다면 422 상태 코드와 [유효성 검증 에러의 JSON 표현](#validation-error-response-format)이 사용자에게 반환됩니다.

> [!NOTE]
> Inertia를 사용하는 라라벨 프론트엔드에서 실시간 폼 리퀘스트 유효성 검증이 필요하다면 [Laravel Precognition](/docs/12.x/precognition) 문서를 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행하기

초기 유효성 검증이 끝난 뒤 추가적인 검증이 필요한 경우, 폼 리퀘스트의 `after` 메서드를 사용할 수 있습니다.

`after` 메서드는 검증 완료 후 호출될 콜러블(callable) 또는 클로저(closure)들의 배열을 반환해야 하며, 이 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 주입됩니다. 이를 통해 필요시 추가적인 에러 메시지를 생성할 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
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

위에서 언급했듯이, `after` 메서드가 반환하는 배열에는 인보커블 클래스도 포함할 수 있습니다. 이 경우 해당 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 인자로 받게 됩니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
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
#### 첫 번째 유효성 검증 실패 시 전체 중단하기

폼 리퀘스트 클래스에 `stopOnFirstFailure` 속성을 추가하면, 하나의 검증 실패가 발생하면 모든 속성에 대한 검증을 즉시 중단할 수 있습니다.

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

폼 리퀘스트 유효성 검증에 실패했을 때, 자동으로 이전 위치로 리디렉션 응답이 생성됩니다. 하지만 이 동작을 원하는 대로 변경할 수도 있습니다. 이를 위해 폼 리퀘스트에 `$redirect` 속성을 정의하면 됩니다.

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

혹은, 지정한 이름의 라우트로 리디렉션하고 싶다면 `$redirectRoute` 속성을 사용할 수 있습니다.

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 권한 처리

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드에서 인증된 사용자가 실제로 특정 리소스에 대한 권한이 있는지 결정할 수 있습니다. 예를 들어, 사용자가 본인이 작성한 블로그 댓글만 수정할 수 있게 제한하고 싶을 수 있습니다. 주로 [인가 게이트와 정책](/docs/12.x/authorization)을 활용해 구현합니다.

```php
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 라라벨의 기본 요청 클래스를 확장하므로, `user` 메서드를 사용해서 현재 인증된 사용자에 접근할 수 있습니다. 위 예시에서는 `route` 메서드를 호출하여 라우트에 정의된 URI 파라미터(예: `{comment}`)에 접근합니다.

```php
Route::post('/comment/{comment}');
```

따라서 애플리케이션에서 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하는 경우, 리퀘스트의 속성으로 바로 바인딩된 모델을 가져와 코드를 더욱 간결하게 만들 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, 403 상태 코드와 함께 HTTP 응답이 자동으로 반환되며 컨트롤러 메서드는 실행되지 않습니다.

만약 요청의 인가(authorization) 로직을 애플리케이션의 다른 부분에서 처리할 계획이라면 `authorize` 메서드를 아예 제거하거나, 단순히 `true`만 반환할 수도 있습니다.

```php
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드의 시그니처에 필요한 의존성을 타입힌트로 지정하면, 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 해결해줍니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

폼 리퀘스트에서 사용할 에러 메시지를 `messages` 메서드를 오버라이드하여 커스터마이즈할 수 있습니다. 이 메서드는 속성/규칙별 에러 메시지를 배열로 반환해야 합니다.

```php
/**
 * Get the error messages for the defined validation rules.
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
#### 유효성 검증 특성명 커스터마이징

라라벨의 기본 유효성 검증 에러 메시지에는 `:attribute` 플레이스홀더가 자주 사용됩니다. 에러 메시지에서 `:attribute`가 커스텀 특성명으로 대체되기를 원한다면, `attributes` 메서드를 오버라이드하여 커스텀 이름을 지정할 수 있습니다. 이 메서드는 속성/이름 쌍의 배열을 반환해야 합니다.

```php
/**
 * Get custom attributes for validator errors.
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
### 유효성 검증 전 입력값 준비

유효성 검증 규칙을 적용하기 전에 요청 데이터를 준비(정제, 변환)해야 할 필요가 있다면, `prepareForValidation` 메서드를 사용하면 됩니다.

```php
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

또한, 유효성 검증이 끝난 뒤 요청 데이터를 정규화(normalize)해야 할 경우에는 `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## Validator 수동 생성하기

요청 객체의 `validate` 메서드를 사용하기 원하지 않는다면, Validator [파사드](/docs/12.x/facades)를 이용해 직접 validator 인스턴스를 생성할 수도 있습니다. 파사드의 `make` 메서드를 사용하면 새로운 validator 인스턴스를 만들 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
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

        // Retrieve the validated input...
        $validated = $validator->validated();

        // Retrieve a portion of the validated input...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // Store the blog post...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인자는 검증할 데이터이며, 두 번째 인자는 데이터에 적용할 유효성 검증 규칙의 배열입니다.

요청 검증이 실패했는지 판별한 후, `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 방법을 사용하면 리디렉션 이후 뷰에서 `$errors` 변수가 자동으로 전달되어, 사용자에게 에러 메시지를 쉽게 표시할 수 있습니다. `withErrors` 메서드는 validator 인스턴스, `MessageBag`, 또는 PHP 배열을 인자로 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 중단하기

`stopOnFirstFailure` 메서드를 사용하면, 하나의 검증 실패가 발생하면 모든 속성에 대한 검증을 즉시 중단하도록 validator에 알릴 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

수동으로 validator 인스턴스를 생성하더라도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션 기능을 그대로 활용하고 싶다면 validator 인스턴스의 `validate` 메서드를 호출하면 됩니다. 검증에 실패하면, 사용자는 자동으로 리디렉션되거나, XHR 요청일 경우 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

검증 실패 시 에러 메시지를 [이름을 가진 에러백](#named-error-bags) 안에 저장하려면 `validateWithBag` 메서드를 사용하세요.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름을 가진 에러백(Named Error Bags)

한 페이지에 여러 개의 폼이 있는 경우, 검증 에러를 담는 `MessageBag`에 이름을 지정할 수 있습니다. 이렇게 하면, 특정 폼에 대한 에러 메시지만 손쉽게 얻어올 수 있습니다. 이를 위해 `withErrors`의 두 번째 인자로 이름을 전달하세요.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이후 `$errors` 변수에서 이름을 가진 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요하다면, 라라벨이 제공하는 기본 에러 메시지 대신 validator 인스턴스가 사용할 커스텀 에러 메시지를 지정할 수 있습니다. 여러 방법이 있지만, 우선 `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지의 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위 예시에서 `:attribute` 플레이스홀더는 실제 검증 대상 필드명으로 대체됩니다. 유효성 검증 메시지에는 이 외에도 다양한 플레이스홀더를 사용할 수 있습니다. 몇 가지 예시는 다음과 같습니다.

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>

#### 특정 속성에 대한 사용자 정의 메시지 지정

특정 속성에 대해서만 사용자 정의 에러 메시지를 지정하고 싶은 경우가 있습니다. 이럴 때는 "점(dot) 표기법"을 사용할 수 있습니다. 속성의 이름을 먼저 작성하고, 이어서 검증 규칙을 지정하면 됩니다.

```php
$messages = [
    'email.required' => '이메일 주소가 필요합니다!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 사용자 정의 속성 값 지정

라라벨에서 기본 제공하는 많은 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 이 플레이스홀더는 유효성 검증 대상 필드나 속성 이름으로 대체됩니다. 특정 필드에 대해 이 플레이스홀더에 들어갈 값을 커스터마이징하려면, `Validator::make` 메서드의 네 번째 인수로 사용자 정의 속성 배열을 전달하면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 검증 수행하기

기본 유효성 검증이 끝난 뒤에 추가로 검증이 필요한 경우가 있을 수 있습니다. 이럴 때는 Validator의 `after` 메서드를 활용할 수 있습니다. `after` 메서드는 클로저나 호출 가능한(callable) 객체 배열을 받아, 검증이 끝난 후에 호출합니다. 전달된 각 콜러블(callable)은 `Illuminate\Validation\Validator` 인스턴스를 인수로 받으므로, 필요에 따라 추가 에러 메시지를 등록할 수 있습니다.

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

설명한 것처럼, `after` 메서드는 콜러블 객체의 배열도 받을 수 있습니다. "사후 검증" 로직이 인보커블 클래스(임의의 호출이 가능한 클래스)에 캡슐화되어 있다면, 각 클래스의 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받아 검증 로직을 구현할 수 있으므로 편리합니다.

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
## 유효성 검증된 입력 데이터 다루기

폼 요청(form request)이나 수동으로 생성한 Validator 인스턴스를 사용해 들어오는 요청 데이터를 검증한 후, 실제로 검증이 이루어진 데이터를 가져오고 싶을 때가 있습니다. 이런 데이터는 여러 방법으로 가져올 수 있습니다. 먼저, 폼 요청 객체나 Validator 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 검증된 데이터만 담긴 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 요청 객체나 Validator 인스턴스에서 `safe` 메서드를 사용할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 반환된 객체는 `only`, `except`, `all` 메서드를 통해 검증된 데이터의 일부 또는 전체를 손쉽게 조회할 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 이터레이터로 순회하거나 배열 방식으로 접근할 수 있습니다.

```php
// 검증된 데이터를 순회할 수 있습니다.
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근할 수도 있습니다.
$validated = $request->safe();

$email = $validated['email'];
```

추가적으로 검증된 데이터에 새 필드를 더하고 싶다면, `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 가져오고 싶다면, `collect` 메서드를 사용할 수 있습니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 방식으로 에러 메시지를 다룰 수 있는 `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 이 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

특정 필드에 대한 첫 번째 에러 메시지를 가져오려면 `first` 메서드를 사용합니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드에 대해 모든 에러 메시지를 배열 형태로 가져오고 싶다면, `get` 메서드를 사용하면 됩니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 입력 필드를 검증하는 경우, `*` 문자를 사용해 각 배열 요소에 대한 모든 메시지도 조회할 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 전체 에러 메시지 가져오기

모든 필드에 관한 에러 메시지를 배열로 한 번에 가져오려면 `all` 메서드를 사용합니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지가 존재하는지 확인

`has` 메서드를 이용해 특정 필드에 대해 에러 메시지가 있는지 여부를 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 사용자 정의 메시지 지정

라라벨이 기본 제공하는 각 유효성 검증 규칙에는, 애플리케이션의 `lang/en/validation.php` 파일에 위치한 에러 메시지가 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙에 대응하는 번역 항목이 존재합니다. 애플리케이션의 필요에 맞게 자유롭게 이 메시지를 수정하거나 변경할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리에 복사해서 각 언어에 맞는 메시지로 번역해 사용할 수도 있습니다. 라라벨의 지역화에 대해 더 자세히 알고 싶다면, [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이징하려면 `lang:publish` 아티즌 명령어로 파일을 배포할 수 있습니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 사용자 정의 메시지

애플리케이션의 유효성 검증 언어 파일 내에서, 특정 속성과 규칙의 조합에 대해 사용할 에러 메시지를 커스터마이즈할 수 있습니다. 이를 위해, `lang/xx/validation.php` 언어 파일의 `custom` 배열에 직접 메시지를 지정하세요.

```php
'custom' => [
    'email' => [
        'required' => '이메일 주소가 필요합니다!',
        'max' => '이메일 주소가 너무 깁니다!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

라라벨 기본 에러 메시지에는 `:attribute` 플레이스홀더가 자주 사용되며, 이는 유효성 검증 중인 필드 또는 속성 이름으로 대체됩니다. 만약 `:attribute` 부분을 커스텀 값으로 바꾸고 싶다면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 해당 속성명을 지정하면 됩니다.

```php
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이징하려면 `lang:publish` 아티즌 명령어로 파일을 배포할 수 있습니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

라라벨의 일부 유효성 검증 규칙 에러 메시지는 `:value` 플레이스홀더를 포함하며, 이는 요청 속성의 실제 값으로 치환됩니다. 그런데 상황에 따라, `:value` 자리에 사용자 친화적인 설명이 들어가길 바랄 수 있습니다. 예를 들어, `payment_type`이 `cc`일 때 신용카드 번호가 반드시 입력되어야 하는 다음과 같은 규칙이 있다고 가정해봅니다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 유효성 검증 규칙이 실패하면 다음과 같은 에러 메시지가 표시됩니다.

```text
The credit card number field is required when payment type is cc.
```

`cc` 대신 더 이해하기 쉬운 설명을 제공하고 싶다면, 언어 파일의 `values` 배열에 사용자 정의 값을 지정할 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => '신용카드'
    ],
],
```

> [!WARNING]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이징하려면 `lang:publish` 아티즌 명령어로 파일을 배포할 수 있습니다.

이렇게 값을 정의한 후에는 유효성 검증 규칙이 다음과 같이 사용자 친화적인 메시지를 보여줍니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙

아래는 사용 가능한 모든 유효성 검증 규칙과 그 기능을 목록으로 정리한 것입니다.



#### 부울(Boolean)

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### 문자열(String)

<div class="collection-method-list" markdown="1">

[Active URL](#rule-active-url)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Different](#rule-different)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Hex Color](#rule-hex-color)
[In](#rule-in)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Min](#rule-min)
[Not In](#rule-not-in)
[Regular Expression](#rule-regex)
[Not Regular Expression](#rule-not-regex)
[Same](#rule-same)
[Size](#rule-size)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

#### 숫자(Number)

<div class="collection-method-list" markdown="1">

[Between](#rule-between)
[Decimal](#rule-decimal)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Integer](#rule-integer)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Multiple Of](#rule-multiple-of)
[Numeric](#rule-numeric)
[Same](#rule-same)
[Size](#rule-size)

</div>

#### 배열(Array)

<div class="collection-method-list" markdown="1">

[Array](#rule-array)
[Between](#rule-between)
[Contains](#rule-contains)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)

</div>

#### 날짜(Date)

<div class="collection-method-list" markdown="1">

[After](#rule-after)
[After Or Equal](#rule-after-or-equal)
[Before](#rule-before)
[Before Or Equal](#rule-before-or-equal)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Timezone](#rule-timezone)

</div>

#### 파일(File)

<div class="collection-method-list" markdown="1">

[Between](#rule-between)
[Dimensions](#rule-dimensions)
[Extensions](#rule-extensions)
[File](#rule-file)
[Image](#rule-image)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Size](#rule-size)

</div>

#### 데이터베이스(Database)

<div class="collection-method-list" markdown="1">

[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

#### 유틸리티(Utilities)

<div class="collection-method-list" markdown="1">

[Any Of](#rule-anyof)
[Bail](#rule-bail)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Filled](#rule-filled)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Nullable](#rule-nullable)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited If Accepted](#rule-prohibited-if-accepted)
[Prohibited If Declined](#rule-prohibited-if-declined)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required If Declined](#rule-required-if-declined)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Sometimes](#validating-when-present)

</div>

<a name="rule-accepted"></a>
#### accepted

검증 대상 필드의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"` 중 하나여야 합니다. 일반적으로 "이용 약관" 동의와 같은 필드의 유효성 검증에 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

다른 검증 대상 필드가 지정된 값과 일치할 때, 해당 필드의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"` 중 하나여야 합니다. 주로 "이용 약관" 동의 등의 조건부 필드 검증에 사용됩니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드는 `dns_get_record` PHP 함수에 따라 유효한 A 또는 AAAA 레코드가 있어야 합니다. 입력받은 URL의 호스트명은 `parse_url` PHP 함수를 사용해 추출한 뒤 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드의 값이 지정한 날짜 이후여야 합니다. 날짜는 `strtotime` PHP 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`에서 평가할 문자열 날짜 대신, 비교 대상으로 쓸 다른 필드명을 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

날짜 기반 규칙은 유창하게 사용할 수 있는 `date` 규칙 빌더로도 생성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday` 및 `todayOrAfter` 메서드를 이용해, 오늘 이후, 혹은 오늘 또는 이후의 날짜를 표현할 수도 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

검증 대상 필드의 값이 지정한 날짜와 같거나 이후여야 합니다. 더 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

날짜 기반 규칙은 `date` 규칙 빌더로도 유연하게 생성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검증 규칙을 사용하면, 검증 대상 필드가 전달된 여러 검증 규칙 셋 중 하나만 만족해도 유효하다고 판단할 수 있습니다. 예를 들어, 다음 규칙은 `username` 필드가 이메일 또는 6자 이상 알파벳/숫자/대시 조합의 문자열인지 검증합니다.

```php
use Illuminate\Validation\Rule;

'username' => [
    'required',
    Rule::anyOf([
        ['string', 'email'],
        ['string', 'alpha_dash', 'min:6'],
    ]),
],
```

<a name="rule-alpha"></a>
#### alpha

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 해당하는 유니코드 알파벳 문자만으로 구성되어야 합니다.

검증 규칙을 ASCII 문자(`a-z`, `A-Z`)로만 제한하려면, `ascii` 옵션을 규칙에 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 알파벳 및 숫자, 그리고 ASCII 대시(`-`), 언더스코어(`_`)만 허용됩니다.

이 규칙을 ASCII 범위(즉, `a-z`, `A-Z`, `0-9`)로 제한하고 싶다면, `ascii` 옵션을 추가합니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 알파벳과 숫자만으로 이루어져야 합니다.

만약 ASCII 문자(`a-z`, `A-Z`, `0-9`)로만 제한하려면 `ascii` 옵션을 규칙에 추가하세요.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 대상 필드는 PHP의 `array` 타입이어야 합니다.

`array` 규칙에 값을 추가로 지정하면, 입력 배열에 반드시 규칙에 명시된 키만 존재해야 합니다. 아래 예제에서는 입력값에 `admin` 키가 존재하기 때문에 유효하지 않습니다(규칙에 지정된 값에 없기 때문입니다).

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => 'array:name,username',
]);
```

실제로 배열 검증 시에는, 허용할 배열의 키를 항상 명시하는 것이 바람직합니다.

<a name="rule-ascii"></a>
#### ascii

검증 대상 필드는 7비트 ASCII 문자만 허용됩니다.

<a name="rule-bail"></a>
#### bail

해당 필드에서 첫 번째 유효성 검증 실패가 발생하면 이후의 모든 검증을 멈춥니다.

`bail` 규칙은 해당 필드에 대해서만 동작하며, 모든 속성의 검증 자체를 멈추고 싶다면 `stopOnFirstFailure` 메서드를 사용할 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 대상 필드의 값이 지정한 날짜 이전이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다. [after](#rule-after) 규칙처럼, 비교할 날짜로 다른 필드명을 사용할 수도 있습니다.

날짜 기반 규칙은 `date` 규칙 빌더로도 유연하게 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday` 및 `todayOrBefore` 메서드를 활용해 오늘 이전, 또는 오늘 이전/같은 날짜를 쉽게 지정할 수도 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

검증 대상 필드의 값이 지정한 날짜 이전 혹은 같아야 합니다. 날짜는 PHP의 `strtotime` 함수에 의해 유효한 `DateTime` 객체로 변환됩니다. [after](#rule-after) 규칙처럼, 비교 대상으로 다른 필드명을 지정할 수도 있습니다.

날짜 기반 규칙은 `date` 규칙 빌더로 간결하게 생성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

검증 대상 필드의 크기가 _min_ 값 이상, _max_ 값 이하(포함)이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 크기가 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

검증 대상 필드는 불리언 타입으로 변환 가능한 값이어야 합니다. 허용하는 값으로는 `true`, `false`, `1`, `0`, `"1"`, `"0"`이 있습니다.

`strict` 파라미터를 사용하면, 값이 엄격하게 `true` 또는 `false`인 경우에만 유효하다고 판단합니다.

```php
'foo' => 'boolean:strict'
```

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드와 `{field}_confirmation` 필드의 값이 동일해야 합니다. 예를 들어, 검증하려는 필드가 `password`라면, 입력값에도 `password_confirmation` 필드가 반드시 존재해야 하고 두 값이 일치해야 합니다.

커스텀 확인용 필드명을 별도로 지정할 수도 있습니다. 예를 들어, `confirmed:repeat_username` 식으로 작성하면, `repeat_username` 필드가 해당 필드와 일치해야 유효합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

검증 대상 필드는 반드시 지정된 모든 값이 포함된 배열이어야 합니다. 이 규칙은 보통 배열의 특정 값들이 모두 존재하는지 검사할 때 사용합니다. 배열을 `implode`해서 검증해야 하는 경우가 많은데, `Rule::contains` 메서드를 활용하면 훨씬 간결하게 작성할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::contains(['admin', 'editor']),
    ],
]);
```

<a name="rule-current-password"></a>
#### current_password

검증 대상 필드는 현재 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 파라미터로 [인증 가드](/docs/12.x/authentication)를 지정할 수도 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 대상 필드는 `strtotime` PHP 함수에 따라 유효한(상대적인 값이 아닌) 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 대상 필드의 값이 지정한 날짜와 정확히 일치해야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 객체로 처리됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 대상 필드의 값이 지정한 _formats_ 중 하나와 정확히 일치해야 합니다. 한 필드에 대해 `date`와 `date_format`을 동시에 사용해서는 안 됩니다. 이 규칙에서는 PHP [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 형식을 사용할 수 있습니다.

날짜 기반 규칙은 `date` 규칙 빌더로도 쉽게 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>

#### decimal:_min_,_max_

검증 대상 필드는 숫자여야 하며, 지정된 소수 자릿수를 가져야 합니다.

```php
// 소수점 이하 자릿수가 정확히 2자리여야 합니다(예: 9.99)...
'price' => 'decimal:2'

// 소수점 이하 자릿수가 2~4자리 사이여야 합니다...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

다른 검증 대상 필드가 지정된 값과 같을 때, 해당 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수는 자릿수가 _value_와 정확히 일치해야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 대상 정수의 자릿수는 _min_과 _max_ 사이여야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 지정한 파라미터에 맞는 이미지 크기 조건을 만족해야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 조건은 다음과 같습니다: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

_ratio_ 조건은 가로 크기를 세로 크기로 나눈 비율로 지정합니다. 분수(`3/2`)나 실수(`1.5`) 형태로 표현할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

이 규칙은 여러 인자가 필요하므로, `Rule::dimensions` 메서드를 사용해 더 읽기 쉬운 형태로 정의하는 것이 편리합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()
            ->maxWidth(1000)
            ->maxHeight(500)
            ->ratio(3 / 2),
    ],
]);
```

<a name="rule-distinct"></a>
#### distinct

배열을 검증할 때, 해당 필드에 중복된 값이 없어야 합니다.

```php
'foo.*.id' => 'distinct'
```

distinct 규칙은 기본적으로 느슨한(루스) 변수 비교를 사용합니다. 엄격한 비교를 하고 싶다면, 검증 규칙에 `strict` 파라미터를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 구분 없이 비교하려면, `ignore_case` 인자를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값 중 하나로 시작하지 않아야 합니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값 중 하나로 끝나지 않아야 합니다.

<a name="rule-email"></a>
#### email

검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 검증 규칙은 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용하여 이메일 형식을 검사합니다. 기본적으로 `RFCValidation` 검증이 적용되지만, 다른 검증 스타일도 사용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예제는 `RFCValidation`과 `DNSCheckValidation` 검증을 적용합니다. 사용할 수 있는 모든 검증 스타일은 다음과 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 주소를 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 검증하며, 경고가 있으면(예: 마지막에 마침표가 있거나 연속으로 마침표가 있는 경우) 실패 처리합니다.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인이 유효한 MX 레코드를 가지는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 동형 이의나 혼동을 유발하는 유니코드 문자가 이메일 주소에 포함되어 있지 않은지 검사합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일 주소 유효성을 검사합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - `filter_var` 함수 기준으로 유효성을 검사하며, 일부 유니코드 문자를 허용합니다.

</div>

더욱 편리하게, 이메일 검증 규칙은 플루언트 형식의 Rule 빌더로도 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

$request->validate([
    'email' => [
        'required',
        Rule::email()
            ->rfcCompliant(strict: false)
            ->validateMxRecord()
            ->preventSpoofing()
    ],
]);
```

> [!WARNING]
> `dns`와 `spoof` 검증기는 PHP의 `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 클래스 기반 규칙으로, 검증 대상 필드가 유효한 enum 값인지 검증합니다. `Enum` 규칙은 enum의 이름을 생성자 인수로 받습니다. 원시값을 검증할 때는, `backed Enum`을 `Enum` 규칙에 제공해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`와 `except` 메서드를 사용하여 특정 enum case만 유효하도록 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용해 `Enum` 규칙을 조건부로 수정할 수도 있습니다.

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

Rule::enum(ServerStatus::class)
    ->when(
        Auth::user()->isAdmin(),
        fn ($rule) => $rule->only(...),
        fn ($rule) => $rule->only(...),
    );
```

<a name="rule-exclude"></a>
#### exclude

검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

_또다른 필드_의 값이 _value_와 같을 때, 해당 검증 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

더 복잡한 조건의 제외 로직이 필요할 경우, `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 boolean이나 클로저(closure)를 인수로 받으며, 클로저를 전달하면 `true` 또는 `false`를 반환해 검증 필드를 제외할지 여부를 결정합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::excludeIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::excludeIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_

`_anotherfield_`의 값이 _value_와 동일하지 않으면 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`)일 때는 비교 대상 필드가 `null`이거나 요청 데이터에 포함되어 있지 않으면 해당 필드를 제외합니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

_또다른 필드_가 존재하는 경우, 해당 검증 대상 필드는 `validate` 및 `validated`가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

_또다른 필드_가 존재하지 않는 경우, 해당 검증 대상 필드는 `validate` 및 `validated`가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 대상 필드의 값은 지정된 데이터베이스 테이블에 반드시 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

만약 `column` 옵션을 명시하지 않으면, 필드명을 그대로 사용합니다. 즉, 위 예시에서는 요청 데이터의 `state` 속성의 값이 `states` 테이블의 `state` 컬럼에 존재하는지 확인합니다.

<a name="specifying-a-custom-column-name"></a>
#### 커스텀 컬럼 이름 지정

검증 규칙에서 데이터베이스 컬럼명을 명시적으로 지정하려면, 테이블 이름 뒤에 컬럼명을 적어주면 됩니다.

```php
'state' => 'exists:states,abbreviation'
```

경우에 따라 특정 데이터베이스 커넥션을 `exists` 쿼리에 사용해야 할 수도 있습니다. 이때는 커넥션명을 테이블명 앞에 붙여 지정하면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블 이름을 직접 지정하는 대신, Eloquent 모델명을 이용해 테이블명을 결정할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

`Rule` 클래스를 사용하는 방식으로 exists 규칙에서 실행되는 쿼리를 더 세밀하게 커스터마이즈할 수 있습니다. 이 예시에서는 규칙을 배열 형태로 지정하며, `|` 문자로 연결하지 않습니다.

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            $query->where('account_id', 1);
        }),
    ],
]);
```

`Rule::exists` 메서드에서 두 번째 인수로 사용할 컬럼명을 넘기면, 해당 컬럼을 기준으로 exists 규칙이 동작하도록 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

배열로 여러 값을 받아서 이 값들이 모두 데이터베이스에 존재하는지 검사하고 싶다면, 해당 필드에 `exists` 및 [array](#rule-array) 규칙 둘 다를 추가할 수 있습니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이렇게 하면 라라벨이 모든 값이 지정한 테이블에 존재하는지 단일 쿼리로 바로 확인합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 대상 파일의 사용자 지정 확장자가, 나열된 확장자 중 하나와 일치해야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 사용자 지정 확장자만으로 파일을 검증해서는 안 됩니다. 이 규칙은 보통 [mimes](#rule-mimes)나 [mimetypes](#rule-mimetypes) 검증과 함께 사용하는 것이 좋습니다.

<a name="rule-file"></a>
#### file

검증 대상 필드는 정상적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

검증 대상 필드가 요청 데이터에 존재한다면, 그 값은 비어 있지 않아야 합니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 대상 필드는 지정된 _field_ 또는 _value_보다 커야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 평가 방법을 따릅니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 대상 필드는 지정된 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 평가 방법을 따릅니다.

<a name="rule-hex-color"></a>
#### hex_color

검증 대상 필드는 [16진수(hexadecimal)](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값이어야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지(jpg, jpeg, png, bmp, gif, webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙에서는 SVG 파일은 허용하지 않습니다(XSS 취약점 때문). SVG 파일을 허용하려면 `image:allow_svg`와 같이 규칙에 `allow_svg` 지시자를 명시해야 합니다.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 대상 필드는 지정한 값 목록에 포함되어야 합니다. 이 규칙은 배열을 `implode`해서 리스트를 만드는 경우가 많으므로, `Rule::in` 메서드를 써서 더 읽기 쉽게 규칙을 작성할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

`in` 규칙과 `array` 규칙을 함께 사용하면, 입력받는 배열의 각 값이 in 규칙에 지정한 값 항목 중 하나에 포함되어야 합니다. 예를 들어, 아래에서는 입력 배열에 있는 `LAS` 공항 코드는 in 규칙에 지정된 값에 없으므로 유효하지 않습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

검증 대상 필드는 _anotherfield_의 값들 중 하나여야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 대상 필드는 배열이어야 하며, 배열 내에 지정한 _values_ 중 하나 이상의 키를 가져야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증 대상 필드는 정수여야 합니다.

> [!WARNING]
> 이 규칙은 입력값이 "정수 변수형"인지까지 검사하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 필드 타입만 검사합니다. 입력값이 숫자인지도 함께 체크하려면 반드시 [numeric 규칙](#rule-numeric)과 함께 사용하세요.

<a name="rule-ip"></a>
#### ip

검증 대상 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

검증 대상 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증 대상 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증 대상 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증 대상 필드는 지정한 _field_보다 작아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 평가 방법을 따릅니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 대상 필드는 지정한 _field_보다 작거나 같아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 평가 방법을 따릅니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 대상 필드는 모두 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증 대상 필드는 배열이어야 하며, 0에서 `count($array) - 1`까지의 연속된 숫자 키를 가진 리스트(list) 구조여야 합니다.

<a name="rule-mac"></a>
#### mac_address

검증 대상 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 대상 필드는 최대 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 검증 방식이 적용됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 대상 정수의 자릿수는 _value_ 이하여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 대상 파일은 지정한 MIME 타입과 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드한 파일의 실제 내용을 읽어서 프레임워크가 MIME 타입을 추정하며, 이는 클라이언트가 전송한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 대상 파일의 확장자가 나열된 확장자 중 하나와 일치해야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정해도 실제로는 파일 내용을 읽어 MIME 타입을 추정해 확장자와 일치하는지를 검증합니다. MIME 타입과 확장자 전체 목록은 다음에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 검증 규칙은, 파일의 MIME 타입과 사용자가 지정한 확장자의 일치를 확인하지는 않습니다. 예를 들어, `mimes:png` 검증 규칙은 파일 이름이 `photo.txt`이더라도 파일 내용이 올바른 PNG 이미지라면 해당 파일을 PNG 이미지로 간주합니다. 사용자가 지정한 확장자를 반드시 검사하려면 [extensions](#rule-extensions) 규칙을 사용하세요.

<a name="rule-min"></a>
#### min:_value_

검증 대상 필드는 최소 _value_ 이상이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 검증 방식이 적용됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 대상 정수의 자릿수는 최소 _value_ 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증 대상 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_또다른 필드_의 값이 지정된 _value_와 같을 때, 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_또다른 필드_의 값이 지정된 _value_와 같지 않으면, 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

지정한 다른 필드가 존재할 때에만, 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

지정한 다른 필드가 모두 존재할 때에만, 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 대상 필드는 지정한 값 목록에 포함되어서는 안 됩니다. `Rule::notIn` 메서드를 사용해 더 읽기 쉽도록 규칙을 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a name="rule-not-regex"></a>
#### not_regex:_pattern_

검증 대상 필드는 지정한 정규표현식과 일치하지 않아야 합니다.

이 규칙 내부적으로는 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 반드시 `preg_match`와 동일한 포맷(분리자 포함)을 따라야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex`와 `not_regex` 패턴을 사용할 때는, 정규식에 `|` 문자가 포함된다면 `|` 구분 대신 배열로 규칙을 지정해야 할 수 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증 대상 필드는 `null` 값을 가질 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

검증 대상 필드는 [숫자(numeric)](https://www.php.net/manual/en/function.is-numeric.php)여야 합니다.

`strict` 파라미터를 사용하면, 값이 정수 또는 실수 타입일 때만 유효하게 인정하며, 숫자 문자열은 유효하지 않습니다.

```php
'amount' => 'numeric:strict'
```

<a name="rule-present"></a>
#### present

검증 대상 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_또다른 필드_의 값이 지정한 _value_ 중 하나와 같을 때, 검증 대상 필드는 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_또다른 필드_의 값이 지정한 _value_ 중 하나와 같지 않을 때, 검증 대상 필드는 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

지정한 다른 필드 중 하나라도 존재한다면, 검증 대상 필드도 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

지정한 모든 다른 필드가 존재할 때, 검증 대상 필드는 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 대상 필드는 입력 데이터에 존재하지 않거나, 비어 있어야 합니다. 필드가 "비어 있다"고 간주되는 경우는 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 실제 경로를 가지지 않은 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_또다른 필드_의 값이 지정한 _value_ 중 하나와 같을 때, 검증 대상 필드는 존재하지 않거나 비어 있어야 합니다. 필드가 "비어 있다"고 간주되는 경우는 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 실제 경로를 가지지 않은 경우

</div>

더 복잡한 prohibition(금지) 조건이 필요하다면 `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. boolean이나 클로저(closure)를 인수로 받을 수 있으며, closure를 전달하면 true/false로 해당 필드를 금지할지 여부를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf(fn () => $request->user()->is_admin),
]);
```
<a name="rule-prohibited-if-accepted"></a>
#### prohibited_if_accepted:_anotherfield_,...

_또다른 필드_의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나일 때, 해당 검증 필드는 존재하지 않거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_또다른 필드_의 값이 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나일 때, 해당 검증 필드는 존재하지 않거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_또다른 필드_의 값이 지정한 _value_ 중 하나와 같지 않다면, 해당 검증 필드는 존재하지 않거나 비어 있어야 합니다. 필드가 "비어 있다"고 간주되는 조건은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 실제 경로를 가지지 않은 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 대상 필드가 존재하거나 비어 있지 않을 때, _anotherfield_에 명시된 모든 필드는 존재하지 않거나 비어 있어야 합니다. "비어 있다"는 조건은 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 실제 경로를 가지지 않은 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증 대상 필드는 지정한 정규표현식과 일치해야 합니다.

내부적으로 PHP의 `preg_match` 함수를 사용하며, 지정하는 패턴은 `preg_match`에서 요구하는 포맷(구분자 포함)을 따라야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 정규식에 `|` 문자가 포함된 경우 `|` 문자 대신 배열로 규칙을 지정해야 할 수 있습니다.

<a name="rule-required"></a>
#### required

검증 대상 필드는 입력 데이터에 반드시 존재해야 하며, 비어 있지 않아야 합니다. "비어 있다"고 간주되는 조건은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 없는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_또다른 필드_의 값이 지정한 _value_ 중 하나와 같을 때, 검증 대상 필드는 반드시 존재하고 비어 있지 않아야 합니다.

`required_if` 규칙에 더 복잡한 조건을 구성하려면, `Rule::requiredIf` 메서드를 사용할 수 있습니다. boolean이나 클로저(closure)를 인수로 받을 수 있으며, 클로저를 전달하면 true/false로 필드가 필수인지 아닌지를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-required-if-accepted"></a>

#### required_if_accepted:_anotherfield_,...

검증 대상 필드는 _anotherfield_ 필드의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`일 때 반드시 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

검증 대상 필드는 _anotherfield_ 필드의 값이 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`일 때 반드시 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

검증 대상 필드는 _anotherfield_ 필드가 _value_와 같지 않은 경우에 반드시 존재하며 비어 있지 않아야 합니다. 즉, _value_가 `null`이 아니라면 _anotherfield_ 필드도 요청 데이터에 반드시 존재해야 합니다. 만약 _value_가 `null`이라면(`required_unless:name,null`), 비교 대상 필드가 `null`이거나 요청 데이터에서 해당 필드가 누락된 경우를 제외하고 검증 대상 필드가 필수로 요구됩니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

지정된 다른 필드들 중 하나라도 존재하고 비어 있지 않은 경우에만, 검증 대상 필드는 반드시 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

지정된 모든 다른 필드가 모두 존재하고 비어 있지 않은 경우에만, 검증 대상 필드는 반드시 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

지정된 다른 필드들 중 하나라도 비어 있거나 존재하지 않을 때만, 검증 대상 필드는 반드시 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

지정된 모든 다른 필드가 모두 비어 있거나 존재하지 않을 때만, 검증 대상 필드는 반드시 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증 대상 필드는 배열이어야 하며, 지정된 키들을 반드시 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정한 _field_의 값이 검증 대상 필드의 값과 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증 대상 필드는 주어진 _value_와 일치하는 크기를 가져야 합니다. 문자열 데이터의 경우 _value_는 문자 개수를 의미합니다. 숫자 데이터의 경우 _value_는 주어진 정수 값(이 경우, 반드시 `numeric` 또는 `integer` 규칙을 함께 사용해야 합니다)을 의미합니다. 배열의 경우 _size_는 배열의 요소 개수를 뜻합니다. 파일의 경우 _size_는 파일 용량(킬로바이트 단위)을 의미합니다. 아래는 몇 가지 예시입니다.

```php
// 문자열이 정확히 12자여야 하는지 검증...
'title' => 'size:12';

// 입력받은 정수가 10인지 검증...
'seats' => 'integer|size:10';

// 배열에 요소가 정확히 5개 있는지 검증...
'tags' => 'array|size:5';

// 업로드된 파일 용량이 정확히 512킬로바이트인지 검증...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 대상 필드는 문자열이어야 합니다. 만약 필드에 `null`도 허용하고 싶다면, `nullable` 규칙을 필드에 추가해주세요.

<a name="rule-timezone"></a>
#### timezone

검증 대상 필드는 `DateTimeZone::listIdentifiers` 메서드 기준으로 유효한 타임존 식별자여야 합니다.

또한 이 유효성 검사 규칙에는 [`DateTimeZone::listIdentifiers` 메서드에서 허용하는 인수](https://www.php.net/manual/en/datetimezone.listidentifiers.php)를 파라미터로 전달할 수도 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증 대상 필드의 값은 지정한 데이터베이스 테이블 안에 존재하지 않아야 합니다.

**커스텀 테이블/컬럼명 지정하기**

테이블명을 직접 명시하는 대신, Eloquent 모델을 지정해 테이블명을 자동으로 결정하게 할 수 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션은 검증 대상 필드가 참조할 데이터베이스 컬럼명을 지정합니다. 만약 `column` 옵션을 지정하지 않으면, 검증 대상 필드의 이름이 곧 참조 컬럼 이름으로 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**커스텀 데이터베이스 커넥션 지정하기**

Validator가 쿼리할 데이터베이스 연결을 직접 지정하고 싶을 때는, 테이블명 앞에 커넥션명을 붙여서 사용할 수 있습니다.

```php
'email' => 'unique:connection.users,email_address'
```

**지정한 ID는 unique 체크에서 무시하기**

때로는 unique 검증 시 특정 ID는 중복 여부에서 제외하고 싶을 때가 있습니다. 예를 들어, "프로필 수정" 화면에서는 사용자의 이름, 이메일, 위치를 변경할 수 있는데, 사용자가 이메일 필드 값을 변경하지 않았을 때 이미 본인 소유의 이메일이라면 중복 에러가 발생하면 안 됩니다.

이런 경우, `Rule` 클래스를 활용해 해당 사용자의 ID를 무시하도록 설정할 수 있습니다. 이때는 규칙을 배열로 작성하는 방식도 함께 보여드리겠습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```

> [!WARNING]
> `ignore` 메서드에 사용자가 조작할 수 있는 요청 입력값을 절대 넣어서는 안 됩니다. 꼭 시스템에서 생성한 고유 ID, 즉 자동증가 ID나 Eloquent 모델의 UUID처럼, 신뢰할 수 있는 값만 전달해야 합니다. 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해질 수 있습니다.

모델 키 값 대신, 전체 모델 인스턴스를 전달할 수도 있습니다. Laravel이 모델에서 키 값을 자동으로 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

테이블의 기본 키 컬럼명이 `id`가 아니라면, `ignore` 메서드에 컬럼명을 추가 인수로 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 검증 중인 속성명과 동일한 컬럼의 유일성을 검사합니다. 다르게 지정하려면, 두 번째 인수로 컬럼명을 넘길 수 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 where 절로 쿼리 범위 제한하기**

`where` 메서드를 활용해 추가 쿼리 조건을 붙일 수 있습니다. 예를 들어, `account_id` 컬럼 값이 1인 레코드만 검사하려면 아래처럼 작성합니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**soft delete(소프트 삭제)된 레코드는 unique 검사에서 제외하기**

unique 규칙은 기본적으로 soft delete 처리된(예: `deleted_at` 값이 있는) 레코드까지 모두 유일성 검사 대상에 포함합니다. 이를 제외하려면 `withoutTrashed` 메서드를 사용하세요.

```php
Rule::unique('users')->withoutTrashed();
```

만약 soft delete 컬럼명이 `deleted_at`이 아니라면, 그 컬럼명을 인수로 지정할 수 있습니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증 대상 필드는 반드시 대문자여야 합니다.

<a name="rule-url"></a>
#### url

검증 대상 필드는 유효한 URL이어야 합니다.

특정 프로토콜만 유효하다고 제한하고 싶다면, 프로토콜명들을 추가 인자로 지정할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증 대상 필드는 [ULID(Universally Unique Lexicographically Sortable Identifier)](https://github.com/ulid/spec) 규격에 맞는 값이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 대상 필드는 RFC 9562(버전 1, 3, 4, 5, 6, 7, 8 중 하나)의 UUID 규격에 맞는 값이어야 합니다.

특정 UUID 버전을 검증하려면 파라미터로 버전을 지정할 수도 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값이 있을 때 검증 생략하기

다른 필드의 값에 따라 특정 필드의 유효성 검사를 건너뛰고 싶을 때는 `exclude_if` 규칙을 사용할 수 있습니다. 아래 예시에서, `has_appointment` 필드 값이 `false`라면 `appointment_date`와 `doctor_name` 필드는 검증에서 제외됩니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

또는 반대로, 지정한 값이 아닐 때 검사하지 않으려면 `exclude_unless` 규칙을 사용할 수 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 필드가 존재할 때만 검증

경우에 따라 데이터에 해당 필드가 있을 때만 유효성 검사를 수행하고 싶을 수 있습니다. 이럴 때 `sometimes` 규칙을 규칙 목록에 추가하면 간편하게 처리할 수 있습니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예시에서는, `$data` 배열에 `email` 필드가 있을 경우에만 해당 필드의 유효성 검증이 동작합니다.

> [!NOTE]
> 항상 존재해야 하지만 값이 비어 있을 수 있는 필드를 검증하려면, [옵션 필드에 대한 참고사항](#a-note-on-optional-fields)을 확인하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

다른 필드의 값이 특정 조건을 만족할 때만 필수로 요구하는 등, 더 복잡한 조건이 필요할 때도 있습니다. 예를 들어, 다른 필드가 100보다 큰 값을 가진 경우에만 필수로 요구하거나, 특정 필드가 존재할 때만 두 필드에 특정 값이 요구된다든지 하는 상황입니다. 이러한 복잡한 유효성 검증도 어렵지 않습니다.

먼저 변경되지 않는 _정적 규칙_으로 `Validator` 인스턴스를 만들고:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

예를 들어, 게임 수집가를 위한 웹 앱을 만든다고 가정해봅시다. 만약 게임 소유 수가 100개를 넘는 사용자가 회원가입할 경우, "왜 그렇게까지 많은 게임을 소유했나요?"라는 설명을 필수로 입력받고 싶다고 합시다. 예를 들어 중고 판매점 운영이거나 순수히 수집이 취미인 경우 등입니다. 이 요건을 조건부로 추가하려면 `Validator` 인스턴스의 `sometimes` 메서드를 활용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인수는 조건부로 유효성 검증할 필드명, 두 번째는 추가할 유효성 규칙 배열, 세 번째는 `true` 반환 시 규칙을 적용할 클로저입니다. 이 방법을 사용하면 여러 필드에 대해서 한 번에 조건부 검증을 추가할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent` 인스턴스이며, 유효성 검증 중인 입력값과 파일에 모두 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 검증

알 수 없는 인덱스의 중첩 배열 안에 있는 다른 필드를 기준으로 검증하려면, 클로저 두 번째 인자로 현재 배열 항목 자체를 받을 수 있습니다.

```php
$input = [
    'channels' => [
        [
            'type' => 'email',
            'address' => 'abigail@example.com',
        ],
        [
            'type' => 'url',
            'address' => 'https://example.com',
        ],
    ],
];

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

위 예시처럼, 배열인 경우 `$item`은 `Illuminate\Support\Fluent`이고, 배열이 아니라면 문자열이 전달됩니다.

<a name="validating-arrays"></a>
## 배열 입력값 검증

[배열 검증 규칙 문서](#rule-array)에서 설명했듯, `array` 규칙에는 허용된 배열 키 목록을 전달할 수 있습니다. 만약 배열 내에 이 키 목록 이외의 추가 키가 들어 있으면, 검증에 실패하게 됩니다.

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => 'array:name,username',
]);
```

일반적으로는 배열에 포함되어도 되는 키를 반드시 명시적으로 지정하는 것이 좋습니다. 그렇지 않으면 Validator의 `validate` 또는 `validated` 메서드는 중첩 배열의 키 값 전체를 그대로 반환하므로, 검증 규칙에 예외로 처리되지 않은 키까지 포함될 수 있습니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력값 검증

중첩된 배열 타입의 폼 입력값을 검증하는 것도 어렵지 않습니다. 배열 내부의 특정 속성을 검증하려면 "점 표기법(dot notation)"을 사용하면 됩니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]` 필드가 있다면 아래처럼 검증할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소에 대해서도 검증 규칙을 적용할 수 있습니다. 예를 들어, 입력 배열 내 각 이메일이 유일한지 검사하려면 아래와 같이 작성합니다.

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

마찬가지로, [언어 파일에서 배열 기반 필드의 커스텀 메시지](#custom-messages-for-specific-attributes)를 지정할 때에도 `*` 문자를 사용할 수 있어, 모든 필드에 같은 메시지를 손쉽게 쓸 수 있습니다.

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 값 접근하기

유효성 규칙을 동적으로 지정할 때, 중첩 배열의 각 요소 값을 참고해서 규칙을 부여해야 할 때가 있습니다. 이럴 때는 `Rule::forEach` 메서드를 활용할 수 있습니다. `forEach`는 검증할 배열의 각 항목마다 클로저를 실행하여, 해당 요소에 적용할 규칙 배열을 반환하게 설계되어 있습니다. 클로저에는 값과 완전히 펼쳐진 속성명이 함께 전달됩니다.

```php
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="error-message-indexes-and-positions"></a>
### 에러 메시지에서 인덱스/순번 표시하기

배열을 검증할 때는, 검증 실패 항목에 대해 에러 메시지에 해당 배열 요소의 인덱스나 순번을 보여주고 싶을 수 있습니다. 이 경우 [커스텀 메시지](#manual-customizing-the-error-messages)에서 `:index`(0부터 시작), `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'photos' => [
        [
            'name' => 'BeachVacation.jpg',
            'description' => 'A photo of my beach vacation!',
        ],
        [
            'name' => 'GrandCanyon.jpg',
            'description' => '',
        ],
    ],
];

Validator::validate($input, [
    'photos.*.description' => 'required',
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

위 예시에서는 검증이 실패할 경우 `"Please describe photo #2."`라는 메시지가 사용자에게 보여집니다.

좀 더 중첩이 깊은 배열 항목의 인덱스/순번까지 참조해야 한다면 `second-index`, `second-position`, `third-index`, `third-position`과 같이 사용할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 업로드 검증

라라벨은 업로드된 파일을 검증할 때 사용할 수 있는 다양한 유효성 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 각각 개별적으로 조합해 쓸 수 있을 뿐 아니라, 좀 더 편리하게 사용할 수 있도록 "유연한 파일 유효성 검사 빌더(fluent file validation rule builder)"도 지원합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)
            ->max(12 * 1024),
    ],
]);
```

<a name="validating-files-file-types"></a>
#### 파일 형식 검증하기

`types` 메서드에는 단순히 확장자만 지정하지만, 실제로는 파일 내용을 읽어서 MIME 타입 기준으로 확장자를 추론해서 검증합니다. 전체 MIME 타입 및 확장자 목록은 다음에서 확인 가능합니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 검증하기

파일 크기 기준(min, max)을 지정할 때는, 단위가 붙은 문자열 형식도 사용할 수 있어 편리합니다. `kb`, `mb`, `gb`, `tb` 접미사를 지원합니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 검증하기

사용자가 이미지를 업로드하는 경우라면, `File` 규칙의 `image` 생성 메서드를 통해 jpg, jpeg, png, bmp, gif, webp 이미지임을 쉽게 검증할 수 있습니다.

추가적으로 `dimensions` 규칙을 사용하면 이미지의 크기(가로, 세로 등)를 제한할 수도 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image()
            ->min(1024)
            ->max(12 * 1024)
            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),
    ],
]);
```

> [!NOTE]
> 이미지 크기 제한 및 검사에 대해서는 [dimensions 규칙 문서](#rule-dimensions)에서 더 자세히 확인할 수 있습니다.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약점 위험 때문에 SVG 파일은 허용하지 않습니다. 만약 SVG 허용이 필요하다면, `image` 규칙에 `allowSvg: true` 옵션을 전달하세요: `File::image(allowSvg: true)`

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(가로/세로) 검증하기

이미지의 크기를 따로 검증해야 할 경우도 있습니다. 예를 들어, 업로드된 이미지가 최소 1000픽셀 너비와 500픽셀 높이를 가져야 할 때 다음처럼 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

File::image()->dimensions(
    Rule::dimensions()
        ->maxWidth(1000)
        ->maxHeight(500)
)
```

> [!NOTE]
> 이미지 크기 검증에 관한 더 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)에서 확인하실 수 있습니다.

<a name="validating-passwords"></a>
## 비밀번호 검증

비밀번호가 충분히 복잡한지 보장하려면, Laravel의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체는 비밀번호가 문자, 숫자, 특수문자, 대/소문자 혼합 등 다양한 복잡도 조건을 손쉽게 추가하도록 해줍니다.

```php
// 최소 8자 이상 요구...
Password::min(8)

// 문자 1개 이상 포함...
Password::min(8)->letters()

// 대문자, 소문자 각 1개 이상 포함...
Password::min(8)->mixedCase()

// 숫자 1개 이상 포함...
Password::min(8)->numbers()

// 특수문자 1개 이상 포함...
Password::min(8)->symbols()
```

또한 `uncompromised` 메서드를 사용하면 대중적으로 유출된 비밀번호가 아닌지도 확인할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로 `Password` 규칙 객체는 [k-익명성(k-Anonymity)](https://en.wikipedia.org/wiki/K-anonymity) 방식을 이용하여, 사용자의 프라이버시와 보안을 지키면서도 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스 데이터를 바탕으로 비밀번호가 유출되었는지 검사합니다.

기본적으로, 1회라도 유출된 적 있는 비밀번호는 "유출됨"으로 간주됩니다. `uncompromised`의 첫 번째 인수로 허용 임계값을 지정해 커스터마이즈할 수 있습니다.

```php
// 동일 데이터 유출에 3회 미만만 허용...
Password::min(8)->uncompromised(3);
```

위 모든 예시처럼, 각 메서드는 자유롭게 체이닝하여 사용할 수 있습니다.

```php
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 한 곳에 지정하기

비밀번호 검증 기본 규칙을 애플리케이션 전체에서 한 곳에 모아 두고 싶으면, `Password::defaults` 메서드를 사용하면 됩니다. 이 메서드는 클로저를 인수로 받으며, 보통 `defaults` 규칙은 서비스 프로바이더의 `boot` 메서드 내에서 지정해 둡니다.

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
            ? $rule->mixedCase()->uncompromised()
            : $rule;
    });
}
```

이렇게 지정해두면, 검증 시 별도의 인수 없이 `defaults` 메서드를 호출하는 것만으로 기본 비밀번호 규칙이 적용됩니다.

```php
'password' => ['required', Password::defaults()],
```

추가적으로 별도 규칙을 덧붙이고 싶을 때는 `rules` 메서드를 사용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 커스텀 유효성 검사 규칙 만들기

<a name="using-rule-objects"></a>
### Rule 객체 사용하기

라라벨은 다양한 내장 유효성 검증 규칙을 제공하지만, 종종 직접 규칙을 추가하고 싶을 수 있습니다. 그 중 하나가 "Rule 객체"를 직접 만드는 것입니다. 새 Rule 객체를 생성하려면 `make:rule` Artisan 명령어를 사용하세요. 예를 들어, 입력값이 반드시 대문자인지 검사하는 Rule 객체를 생성해봅시다. 라라벨은 새 규칙 파일을 `app/Rules` 디렉터리에 생성하며, 디렉터리가 없을 경우 자동으로 만들어집니다.

```shell
php artisan make:rule Uppercase
```

새 Rule이 생성되면 그 동작을 정의하면 됩니다. Rule 객체에는 `validate`라는 메서드가 하나 있으며, 여기엔 속성명, 값, 실패 시 에러 메시지 전달용 콜백이 넘어옵니다.

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

이제 해당 Rule 객체 인스턴스를 검증 규칙에 포함시키기만 하면 됩니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 검증 오류 메시지 번역하기

실패 콜백에 에러 메시지를 직접 넣는 대신, [번역 문자열 키](/docs/12.x/localization)를 넣고 라라벨이 자동으로 메시지를 번역하도록 할 수 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면 플레이스홀더 교체값이나 언어 코드도 첫 번째, 두 번째 인수로 함께 전달할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

커스텀 검증 규칙 클래스가 검증 대상 전체 데이터 접근이 필요하다면, `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하면 됩니다. 이 인터페이스를 구현하면 반드시 `setData` 메서드를 정의해야 하며, 라라벨이 검증 전에 요청 전체 데이터를 자동으로 넘겨줍니다.

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * All of the data under validation.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array<string, mixed>  $data
     */
    public function setData(array $data): static
    {
        $this->data = $data;

        return $this;
    }
}
```

또는, 규칙 클래스에서 현재 유효성 검사기 인스턴스 자체에 접근해야 한다면 `ValidatorAwareRule` 인터페이스를 구현할 수도 있습니다.

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * The validator instance.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Set the current validator.
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a name="using-closures"></a>

### 클로저(Closure) 사용하기

애플리케이션 전체에서 맞춤 규칙이 단 한 번만 필요하다면, 규칙 객체를 만드는 대신 클로저를 사용할 수 있습니다. 이 클로저는 속성의 이름, 속성 값, 그리고 유효성 검사가 실패할 때 호출해야 하는 `$fail` 콜백을 인수로 받습니다.

```php
use Illuminate\Support\Facades\Validator;
use Closure;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function (string $attribute, mixed $value, Closure $fail) {
            if ($value === 'foo') {
                $fail("The {$attribute} is invalid.");
            }
        },
    ],
]);
```

<a name="implicit-rules"></a>
### 암묵적(Implicit) 규칙

기본적으로 검증 대상 속성이 없거나 빈 문자열로 주어질 경우, 사용자 정의 규칙을 포함한 일반 유효성 검사 규칙들은 실행되지 않습니다. 예를 들어 [unique](#rule-unique) 규칙의 경우, 빈 문자열에 대해서는 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있을 때에도 사용자 정의 규칙을 항상 실행하려면, 해당 규칙이 해당 속성을 반드시 요구(필수)한다고 암시해야 합니다. 새로운 암묵적(implicit) 규칙 객체를 빠르게 생성하려면, `make:rule` Artisan 명령어에 `--implicit` 옵션을 사용하면 됩니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적" 규칙은 속성이 필수임을 단순히 _암시_하기만 합니다. 실제로 해당 규칙이 속성의 누락이나 빈 값까지 잘못된 것으로 처리할지는 여러분이 직접 구현에 맡겨져 있습니다.