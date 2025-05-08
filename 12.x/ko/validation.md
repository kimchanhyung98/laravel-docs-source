# 유효성 검사(Validation)

- [소개](#introduction)
- [유효성 검사 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력 처리하기](#repopulating-forms)
    - [옵션 필드에 대한 주의사항](#a-note-on-optional-fields)
    - [유효성 검사 에러 응답 포맷](#validation-error-response-format)
- [Form Request 유효성 검사](#form-request-validation)
    - [Form Request 생성하기](#creating-form-requests)
    - [Form Request 권한 처리](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검사 전 입력값 준비](#preparing-input-for-validation)
- [Validator 인스턴스 수동 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 에러 백](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사 실행](#performing-additional-validation)
- [유효성 검사 통과 데이터 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검사](#validating-arrays)
    - [중첩 배열 입력 유효성 검사](#validating-nested-array-input)
    - [에러 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검사](#validating-files)
- [비밀번호 유효성 검사](#validating-passwords)
- [커스텀 유효성 규칙](#custom-validation-rules)
    - [규칙 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암시적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 유입되는 데이터를 검증할 수 있는 다양한 방식을 제공합니다. 대부분의 경우, 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용합니다. 하지만 이외의 다른 유효성 검사 접근법에 대해서도 다룰 예정입니다.

Laravel은 여러 유용한 유효성 검사 규칙을 제공하며, 특정 데이터베이스 테이블의 값이 고유한지도 검증할 수 있습니다. 이 문서에서는 이러한 각종 유효성 규칙을 자세히 설명하여 Laravel의 검증 기능을 충분히 이해할 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 유효성 검사 빠르게 시작하기

Laravel의 강력한 유효성 검사 기능을 익히기 위해, 폼을 검증하고 유효성 검사 에러 메시지를 사용자에게 표시하는 전체 예제를 살펴보겠습니다. 이 개요를 통해 Laravel로 들어오는 요청 데이터를 검증하는 방법을 빠르게 익힐 수 있습니다:

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저 `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정해봅니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 글을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 블로그 글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이 라우트로 들어오는 요청을 처리할 간단한 컨트롤러를 살펴보겠습니다. `store` 메서드는 우선 비워둡니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 글 작성 폼 출력
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 글 저장
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 글 유효성 검사 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 블로그 글의 유효성 검사를 위한 로직을 추가할 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용할 것입니다. 유효성 규칙을 통과하면 코드가 정상적으로 계속 실행됩니다. 하지만 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 에러 응답이 사용자에게 자동으로 반환됩니다.

전통적인 HTTP 요청에서 유효성 검사에 실패하면, 이전 URL로 리다이렉트 응답이 생성됩니다. XHR 요청이라면, [유효성 검사 에러 메시지를 포함한 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작을 더 잘 이해하기 위해, `store` 메서드를 다시 살펴보겠습니다:

```php
/**
 * 새 블로그 글 저장
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 글 데이터가 유효함...

    return redirect('/posts');
}
```

보시다시피 유효성 규칙을 `validate` 메서드에 전달합니다. 모든 유효성 검사 규칙은 [문서화되어 있습니다](#available-validation-rules). 유효성 검사에 실패하면 적합한 응답이 자동 생성되며, 통과한 경우 컨트롤러는 정상적으로 실행을 계속합니다.

또한, 다음과 같이 배열 형태로 규칙을 지정할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

추가로, [이름이 지정된 에러 백](#named-error-bags)을 사용하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검사 실패 시 중단하기

가끔 한 속성에 대해 유효성 검사 규칙이 처음 실패하면, 이후 규칙을 중지하고 싶을 수 있습니다. 이를 위해 해당 속성에 `bail` 규칙을 지정하면 됩니다:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예제에서 `title`의 `unique` 규칙이 실패하면, `max` 규칙은 검사하지 않습니다. 규칙들은 지정된 순서대로 검사됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 주의사항

들어오는 HTTP 요청에 "중첩(nested)" 필드 데이터가 있을 경우, 유효성 검사 규칙 내에서 "도트(dotted)" 문법을 사용할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 마침표가 있는 경우, 백슬래시(`\.`)로 이를 escape하여 "도트 문법"으로 해석되는 것을 방지할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 표시하기

입력 필드가 주어진 유효성 규칙을 통과하지 못하면 어떻게 될까요? 언급했듯이 Laravel은 자동으로 사용자를 이전 위치로 리다이렉트해줍니다. 또한 모든 유효성 검사 에러와 [요청 입력](docs/{{version}}/requests#retrieving-old-input)이 [세션에 플래시(flash)됩니다](/docs/{{version}}/session#flash-data).

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(기본적으로 `web` 미들웨어 그룹에 포함)가 모든 뷰에 `$errors` 변수를 공유합니다. 이 미들웨어가 적용되면, 항상 `$errors` 변수가 뷰에서 사용 가능하므로 안전하게 사용해도 됩니다. `$errors`는 `Illuminate\Support\MessageBag` 인스턴스이며, 자세한 사용법은 [메시지 객체 다루기 문서](#working-with-error-messages)를 참고하세요.

따라서, 유효성 검사가 실패하면 사용자는 컨트롤러의 `create` 메서드로 리다이렉트되어, 뷰에서 에러 메시지를 표시할 수 있습니다:

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

Laravel 기본 내장 유효성 검사 규칙은 각각의 에러 메시지가 `lang/en/validation.php` 파일에 위치합니다. 애플리케이션에 `lang` 디렉터리가 없는 경우 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

해당 파일에서 각 유효성 검사 규칙에 대한 번역 항목이 제공됩니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 수정하세요.

또한 이 파일을 다른 언어 폴더로 복사해 각 언어별 에러 메시지로 번역할 수도 있습니다. Laravel의 로컬라이제이션에 대해서는 [로컬라이제이션 문서](/docs/{{version}}/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어로 파일을 발행하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

이 예제에서는 전통적인 폼으로 데이터를 전송했지만, 실제로는 많은 애플리케이션이 JavaScript로 구동되는 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 중 `validate` 메서드를 사용할 때, Laravel은 리다이렉트 응답을 생성하지 않고, [모든 유효성 검사 에러를 담은 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 422 HTTP 상태 코드를 포함합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성에 유효성 검사 에러 메시지가 존재하는지 빠르게 확인하고 싶다면, [Blade](/docs/{{version}}/blade)에서 `@error` 디렉티브를 사용하세요. 내부에서 `$message` 변수를 출력하면 해당 에러 메시지를 표시할 수 있습니다:

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

[이름이 지정된 에러 백](#named-error-bags)을 사용하는 경우, `@error`의 두 번째 인자로 에러 백 이름을 넘길 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력 처리하기

유효성 검사로 인해 Laravel이 리다이렉트 응답을 생성하면, [요청의 모든 입력값이 세션에 플래시됩니다](/docs/{{version}}/session#flash-data). 이는 다음 요청에서 입력 값을 쉽게 다시 꺼내서, 사용자가 제출하려던 폼을 다시 채워둘 수 있도록 도와줍니다.

이전에 플래시된 입력값을 꺼내려면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하세요. 이 메서드는 [세션](/docs/{{version}}/session)에서 이전에 플래시된 데이터를 가져옵니다:

```php
$title = $request->old('title');
```

또한 Laravel은 글로벌 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/{{version}}/blade) 내에서 이전 값을 표시할 때는 `old` 헬퍼가 더 편리합니다. 해당 필드의 이전 값이 없다면 `null`을 반환합니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 주의사항

Laravel의 전역 미들웨어 스택에는 기본적으로 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이로 인해 "옵션" 요청 필드를 `nullable`로 명시하지 않으면, `null` 값이 유효하지 않은 것으로 간주됩니다. 예시:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예제에서 `publish_at` 필드는 `null`이거나 유효한 날짜 표현이어도 됩니다. 만약 규칙에 `nullable` 수정자를 추가하지 않으면 검증기는 `null` 값을 유효하지 않은 날짜로 처리할 수 있습니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 에러 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대할 경우 Laravel은 에러 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

다음은 유효성 검사 에러용 JSON 응답 포맷 예시입니다. 중첩된 에러 키는 "도트" 표기법으로 평탄화됩니다:

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

(**이하의 분량이 많아 3만자 제한으로 인해 메시지를 나눠서 전송합니다.**  
곧바로 이어서 Form Request 유효성 검사부터 번역이 시작됩니다.)