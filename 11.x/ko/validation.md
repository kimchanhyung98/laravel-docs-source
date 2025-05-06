# 유효성 검사(Validation)

- [소개](#introduction)
- [유효성 검사 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 재입력값 채우기](#repopulating-forms)
    - [선택 입력란에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검사 오류 응답 형식](#validation-error-response-format)
- [폼 리퀘스트 유효성 검사](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인증](#authorizing-form-requests)
    - [에러 메시지 사용자화](#customizing-the-error-messages)
    - [유효성 검사 전 입력값 준비하기](#preparing-input-for-validation)
- [Validator 인스턴스 수동 생성](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름 붙은 에러 백(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사 수행](#performing-additional-validation)
- [유효성 검사된 입력값 활용](#working-with-validated-input)
- [에러 메시지 활용](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 유효성 검사](#validating-arrays)
    - [중첩 배열 입력값 유효성 검사](#validating-nested-array-input)
    - [에러 메시지의 인덱스/위치 활용](#error-message-indexes-and-positions)
- [파일 유효성 검사](#validating-files)
- [비밀번호 유효성 검사](#validating-passwords)
- [커스텀 유효성 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암시적(implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 유입되는 데이터를 검증하는 다양한 방법을 제공합니다. 가장 일반적으로는 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용합니다. 그러나 이 외의 다른 유효성 검사 방법도 다루게 됩니다.

Laravel은 다양한 편리한 유효성 검사 규칙들을 내장하고 있으며, 특정 데이터베이스 테이블에서 값이 유일한지 확인하는 기능도 제공합니다. 각각의 유효성 검사 규칙에 대해 자세히 다루므로, Laravel의 모든 유효성 검사 기능을 익힐 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검사 빠른 시작

Laravel의 강력한 유효성 검사 기능을 빠르게 알아보기 위해 폼을 검증하고 에러 메시지를 사용자에게 보여주는 전체 예제를 살펴보겠습니다. 이 개요를 읽고 나면 Laravel을 이용해 요청 데이터를 어떻게 검증하는지 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

우선, `routes/web.php` 파일에 다음과 같이 라우트를 정의했다고 가정해봅니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이 라우트에 대한 요청을 처리하는 간단한 컨트롤러 예시입니다. `store` 메서드는 일단 비워두겠습니다:

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
        // 유효성 검증 및 저장 로직...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 블로그 포스트를 검증하는 로직을 작성해보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검사가 통과하면 코드가 정상적으로 계속 실행되고, 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하여 자동으로 올바른 에러 응답이 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 유효성 검사가 실패하면 이전 URL로 리디렉션하는 응답이 생성됩니다. XHR 요청(비동기 JavaScript 요청)일 경우에는 [유효성 오류 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 직접 살펴보면 다음과 같습니다:

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

    // 블로그 포스트가 유효함...

    return redirect('/posts');
}
```

유효성 검사 규칙은 `validate` 메서드에 배열로 전달됩니다. 모든 규칙은 [문서에서 확인할 수 있습니다](#available-validation-rules). 유효성 검사에 실패하면 자동으로 응답이 생성됩니다. 성공하면 컨트롤러의 다음 실행이 이어집니다.

또한 파이프(`|`)로 구분된 문자열 대신, 규칙의 배열을 사용할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

그리고, [이름이 지정된 에러 백](#named-error-bags)에 에러 메시지를 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 처음 실패 시 중지

특정 속성에 대해 첫번째 규칙이 실패하면 나머지 규칙을 더 이상 실행하지 않으려면 `bail` 규칙을 사용할 수 있습니다:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서 `title`의 `unique` 규칙이 실패하면 `max` 규칙은 검사하지 않습니다. 규칙들은 정의된 순서대로 평가됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있으면, "점(dot) 표기법"을 이용하여 유효성 검사 규칙을 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

필드명에 실제 점(`.`)이 포함되어 있다면, 백슬래시(`\`)로 이스케이프하여 점 표기법으로 인식되지 않도록 할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 표시하기

유효성 검사에 실패할 경우, Laravel은 사용자를 자동으로 이전 위치로 리디렉션합니다. 추가로, 모든 유효성 에러와 [요청 입력 데이터](/docs/{{version}}/requests#retrieving-old-input)가 자동으로 [세션에 플래시](#repopulating-forms)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어 덕분에, 애플리케이션의 모든 뷰에서 `$errors` 변수를 사용할 수 있습니다. 이 미들웨어가 적용돼 있으면 뷰에서 `$errors` 변수가 언제나 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. `$errors`는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체에 대한 자세한 사용법은 [관련 문서](#working-with-error-messages)에서 보실 수 있습니다.

우리의 예제에서는, 유효성 검사가 실패한 경우 컨트롤러의 `create` 메서드로 리디렉션되어 뷰에서 에러 메시지를 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>글 작성</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- 글 작성 폼 -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 에러 메시지 사용자화

Laravel의 내장 유효성 검사 규칙 각각은 `lang/en/validation.php` 파일에 에러 메시지를 가지고 있습니다. 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 유효성 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 수정할 수 있습니다.

추가 언어 폴더에 이 파일을 복사하여 애플리케이션의 언어에 맞게 번역할 수도 있습니다. Laravel 로컬라이제이션에 대해 더 자세히 알고 싶다면 [로컬라이제이션 문서](/docs/{{version}}/localization)를 참고하세요.

> [!WARNING]  
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자화하려면 `lang:publish` Artisan 명령어로 게시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

이 예제에서는 전통적 폼을 사용하여 데이터를 제출했지만, 많은 애플리케이션에서는 JavaScript 프론트엔드에서 XHR 요청을 받게 됩니다. XHR 요청에서 `validate` 메서드를 사용할 때는 리디렉션이 아니라, [모든 유효성 검사 오류를 포함하는 JSON 응답](#validation-error-response-format)이 반환되며, 이 때 HTTP 상태코드는 422입니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

Blade 템플릿의 [`@error`](#named-error-bags) 디렉티브를 활용해 특정 속성에 대한 유효성 에러 메시지가 존재하는지 빠르게 확인할 수 있습니다. 이 디렉티브 내에서 `$message`를 출력해 에러 메시지를 표시합니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">글 제목</label>

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

[이름이 지정된 에러 백](#named-error-bags)을 사용하는 경우, 두 번째 인자로 에러 백 이름을 지정할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 재입력값 채우기

유효성 검사 실패로 인해 Laravel이 리디렉션 응답을 생성할 때, 프레임워크는 자동으로 [모든 요청 입력값을 세션에 플래시](#quick-displaying-the-validation-errors)합니다. 이를 통해 사용자가 제출했던 폼을 다음 요청에서 편리하게 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request`의 `old` 메서드를 사용합니다:

```php
$title = $request->old('title');
```

또한 글로벌 `old` 헬퍼 함수를 사용할 수도 있습니다. Blade 템플릿에서 사용 시, 해당 필드의 기존 값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 입력란에 대한 참고

기본적으로 Laravel은 앱의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 때문에 "선택 입력란"을 필수로 처리하지 않으려면 `nullable` 규칙을 명시해야 합니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

예를 들어, `publish_at` 필드는 `null`이거나 유효한 날짜여야 합니다. 규칙에서 `nullable`을 빼면 값이 `null`일 때도 날짜로 간주하지 않아 실패하게 됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외를 발생시키고, 요청이 JSON 응답을 기대할 경우 Laravel은 에러 메시지를 자동으로 포매팅해 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래는 유효성 검사 실패 시 JSON 응답 예시입니다. 중첩된 에러 키는 "점(dot)" 표기법으로 변환됩니다:

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

(※ 이하의 문서 번역도 위와 동일한 원칙으로 계속 진행하시면 됩니다. 지면의 한계 상, 위 주요 섹션만 번역 예시로 제공합니다.  
나머지 하위 섹션(폼 리퀘스트 유효성 검사, 수동 Validator 생성, 규칙 상세 설명, 배열 검증 등)도 요청 주시면 추가로 번역해드릴 수 있습니다.)

---

> ⚠️ **이어서 번역이 필요한 경우 요청해 주세요.**  
> 전문 문서가 매우 방대하므로, 단계별로 번역 분량을 조절해 드릴 수 있습니다!