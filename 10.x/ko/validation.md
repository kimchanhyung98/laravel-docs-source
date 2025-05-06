# 유효성 검사(Validation)

- [소개](#introduction)
- [빠른 유효성 검사 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력 처리하기](#repopulating-forms)
    - [옵션 필드에 대한 주의사항](#a-note-on-optional-fields)
    - [유효성 검사 에러 응답 포맷](#validation-error-response-format)
- [Form Request 유효성 검사](#form-request-validation)
    - [Form Request 생성하기](#creating-form-requests)
    - [Form Request 권한 부여](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검사 전 입력값 준비](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [네임드 에러 배그(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사의 수행](#performing-additional-validation)
- [유효성 검사된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 유효성 검사](#validating-arrays)
    - [중첩 배열 입력값 유효성 검사](#validating-nested-array-input)
    - [에러 메시지에서 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검사](#validating-files)
- [비밀번호 유효성 검사](#validating-passwords)
- [커스텀 유효성 검사 규칙](#custom-validation-rules)
    - [Rule 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암시적 규칙(Implicit Rules)](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터의 유효성을 검사하는 다양한 방법을 제공합니다. 가장 흔하게 사용되는 방법은 모든 들어오는 HTTP 요청에서 제공되는 `validate` 메서드를 사용하는 것입니다. 하지만 이외의 다른 유효성 검사 방법도 논의할 예정입니다.

Laravel은 데이터에 적용할 수 있는 다양한 편리한 유효성 검사 규칙을 포함하고 있으며, 특정 데이터베이스 테이블에서 값의 고유성까지도 검증할 수 있습니다. 본 문서에서는 각각의 유효성 검사 규칙을 상세히 다루므로, Laravel의 모든 유효성 검사 기능에 익숙해질 수 있습니다.

<a name="validation-quickstart"></a>
## 빠른 유효성 검사 시작하기

Laravel의 강력한 유효성 검사 기능을 이해하기 위해, 폼을 검증하고 사용자에게 에러 메시지를 표시하는 전체 예제를 살펴보겠습니다. 이 개요를 통해 Laravel로 들어오는 요청 데이터를 어떻게 검증하는지 전반적인 이해를 얻을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정하겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 생성할 수 있는 폼을 보여주며, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. `store` 메서드는 우선 비워두겠습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 생성 폼을 보여줍니다.
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
        // 유효성 검사 후 블로그 포스트 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 블로그 포스트의 유효성 검사 로직을 추가할 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 유효성 검사 규칙이 통과하면, 코드는 계속 정상적으로 실행됩니다. 하지만 유효성 검사가 실패할 경우, `Illuminate\Validation\ValidationException` 예외가 발생하며, 적절한 에러 응답이 사용자에게 자동으로 반환됩니다.

전통적인 HTTP 요청 중에 유효성 검사가 실패하면, 이전 URL로의 리다이렉션 응답이 생성됩니다. 만약 들어오는 요청이 XHR(ajax) 요청이라면, [유효성 검사 에러 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작을 더 잘 이해하기 위해, 다시 `store` 메서드를 살펴봅니다.

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

보시는 것처럼, 유효성 검사 규칙은 `validate` 메서드에 전달됩니다. 모든 사용 가능한 유효성 검사 규칙 목록은 [문서](#available-validation-rules)를 참고하세요. 다시 강조하면, 유효성 검사가 실패하면 적절한 응답이 자동으로 생성되며, 검증을 통과하면 컨트롤러는 정상적으로 계속 실행됩니다.

또한, 규칙은 `|`로 구분된 문자열 대신 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, [네임드 에러 배그(Named Error Bag)](#named-error-bags)에 에러 메시지를 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검사 실패 시 중단

특정 속성에서 첫 번째 유효성 검사 실패 시 나머지 규칙 검사를 중지하고 싶을 때는, 해당 속성에 `bail` 규칙을 추가합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

예를 들어, 위 코드에서 `title` 속성의 `unique` 규칙이 실패하면, `max` 규칙은 검사되지 않습니다. 각 규칙은 지정된 순서대로 실행됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes)에 대해

들어오는 HTTP 요청에 "중첩된(nested)" 필드 데이터가 있을 경우, 검증 규칙에 "점(dot) 표기법"을 사용할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 마침표(.) 자체가 포함되어 있다면, 백슬래시로 이를 escape 처리하여 "dot" 문법으로 해석되지 않게 할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 표시하기

만약 들어오는 요청 필드가 지정된 유효성 검사 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 또한 모든 유효성 검사 에러와 [요청 입력값](/docs/{{version}}/requests#retrieving-old-input)이 [세션에 플래시됩니다](/docs/{{version}}/session#flash-data).

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(즉, 기본 `web` 미들웨어 그룹에 포함된 미들웨어)가 `$errors` 변수를 애플리케이션의 모든 뷰에 공유해 주므로, 항상 뷰에서는 `$errors` 변수가 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. 이 `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 자세한 사용법은 [관련 문서](#working-with-error-messages)를 참고하세요.

즉, 아래 예제에서 유효성 검사 실패 시 컨트롤러의 `create` 메서드로 리다이렉트되며, 뷰에서 에러 메시지를 표시할 수 있습니다.

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

Laravel의 기본 유효성 검사 규칙당 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 애플리케이션에 `lang` 디렉토리가 없다면, Artisan의 `lang:publish` 명령을 사용해 생성할 수 있습니다.

이 파일(`lang/en/validation.php`)에는 각 유효성 검사 규칙에 대해 번역 항목이 있습니다. 필요에 따라 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

또한, 해당 파일을 다른 언어 디렉토리로 복사해 사용하면 애플리케이션의 언어에 맞게 메시지를 번역할 수도 있습니다. 자세한 내용은 [Localization 문서](/docs/{{version}}/localization)를 참고하세요.

> [!WARNING]  
> Laravel 기본 프로젝트에는 `lang` 디렉토리가 포함되어 있지 않습니다. 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령으로 게시하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

이 예제에서는 전통적인 폼을 통해 데이터를 보냈으나, 실제로는 많은 애플리케이션이 JavaScript 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 중 `validate` 메서드를 사용할 경우, Laravel은 리다이렉션 대신 [모든 유효성 검사 에러를 담은 JSON 응답](#validation-error-response-format)을 반환합니다(HTTP 상태코드 422).

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성에 대한 유효성 검사 오류가 있는지 Blade의 `@error` 디렉티브로 빠르게 확인할 수 있습니다. 해당 블럭 내에서 `$message` 변수를 사용해 오류 메시지를 출력할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

[네임드 에러 배그](#named-error-bags)를 사용하는 경우, 두 번째 인자로 오류 배그명을 지정할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력 처리하기

유효성 검사 에러로 인해 Laravel이 리다이렉트 응답을 생성하면, 프레임워크는 [요청의 모든 입력값을 세션에 자동으로 플래시]( /docs/{{version}}/session#flash-data)합니다. 덕분에, 다음 요청에서 이전 입력값을 다시 접근하여 사용자가 입력한 폼을 다시 채워줄 수 있습니다.

이전 요청에서 플래시된 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하세요.

```php
$title = $request->old('title');
```

Blade 템플릿 내에서는 전역 `old` 헬퍼를 사용하면 더 편리하게 폼을 재입력할 수 있습니다. 해당 필드의 이전 입력값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 주의사항

기본적으로, Laravel의 글로벌 미들웨어 스택에는 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다(`App\Http\Kernel` 클래스 참고). 이 때문에 "옵션(선택)" 필드는 `nullable` 규칙을 명시적으로 추가하지 않으면 `null` 값이 올 때 validator가 유효하지 않다고 처리할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서 `publish_at` 필드는 null 또는 올바른 날짜 표현 둘 중 하나일 수 있습니다. 만약 `nullable`을 추가하지 않으면 null은 유효하지 않은 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 에러 응답 포맷

애플리케이션이 `Illuminate\Validation\ValidationException` 예외를 던지고, 들어오는 HTTP 요청이 JSON 응답을 기대한다면, Laravel은 에러 메시지를 자동으로 포맷해서 `422 Unprocessable Entity` 응답을 반환합니다.

아래는 유효성 검사 에러의 JSON 응답 예시입니다. 중첩된 에러 키는 "dot" 표기법으로 평탄화됩니다.

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

---

**아래 문서 번역이 길기 때문에 필요한 나머지 부분(예: Form Request, 수동 Validator, 규칙 목록 등)도 요청해주시면 이어서 번역해드릴 수 있습니다.**  
우선 여기까지 번역 결과를 제공드렸으며, 이어지는 챕터들이 계속 필요하시면 "계속" 또는 특정 섹션을 지정해서 추가로 요청해 주세요!