# 유효성 검사(Validation)

- [소개](#introduction)
- [유효성 검사 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재설정(Repopulating)](#repopulating-forms)
    - [옵션 필드에 대한 참고사항](#a-note-on-optional-fields)
    - [유효성 검사 에러 응답 형식](#validation-error-response-format)
- [폼 요청 유효성 검사](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 권한 부여하기](#authorizing-form-requests)
    - [에러 메시지 커스터마이즈하기](#customizing-the-error-messages)
    - [유효성 검사 전 입력 데이터 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [네임드 에러 백(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이즈하기](#manual-customizing-the-error-messages)
    - [유효성 검사 후 후크](#after-validation-hook)
- [검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 검증하기](#validating-arrays)
    - [중첩 배열 입력 검증하기](#validating-nested-array-input)
    - [에러 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 검증하기](#validating-files)
- [비밀번호 검증하기](#validating-passwords)
- [커스텀 유효성 검사 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저(Closure) 사용하기](#using-closures)
    - [암시적 규칙(Implicit Rules)](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터를 검증하기 위해 여러 가지 접근 방식을 제공합니다. 대부분의 경우, 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용합니다. 그러나 이외에도 다양한 검증 방법에 대해 다룰 것입니다.

Laravel에는 데이터에 적용할 수 있는 다양한 편리한 유효성 검사 규칙이 포함되어 있으며, 특정 데이터베이스 테이블의 값이 고유한지까지 검증할 수 있습니다. 이 문서에서는 각 유효성 검사 규칙을 자세히 다루며, Laravel의 모든 검증 기능을 이해할 수 있도록 설명합니다.

<a name="validation-quickstart"></a>
## 유효성 검사 빠른 시작

Laravel의 강력한 유효성 검사 기능을 알아보기 위해, 폼을 검증하고 사용자에게 에러 메시지를 표시하는 예제를 살펴보겠습니다. 이 개요를 통해 들어오는 요청 데이터를 Laravel로 어떻게 검증하는지, 전반적으로 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합니다.

    use App\Http\Controllers\PostController;

    Route::get('/post/create', [PostController::class, 'create']);
    Route::post('/post', [PostController::class, 'store']);

`GET` 라우트는 사용자가 새 블로그 포스트를 생성할 수 있는 폼을 보여주고, `POST` 라우트는 새로운 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이 라우트에 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴봅니다. 지금은 `store` 메서드는 비워둡니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 작성 폼을 보여줍니다.
     *
     * @return \Illuminate\View\View
     */
    public function create()
    {
        return view('post.create');
    }

    /**
     * 새 블로그 포스트 저장.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // 블로그 포스트 검증 후 저장...
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 새로운 블로그 포스트를 검증할 수 있도록 `store` 메서드에 로직을 추가할 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체의 `validate` 메서드를 사용합니다. 유효성 검사 규칙을 통과하면 코드는 정상적으로 계속 실행됩니다. 만약 검증에 실패하면, `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 에러 응답이 자동으로 사용자에게 전송됩니다.

전통적인 HTTP 요청에서 검증에 실패하면, 이전 URL로 리다이렉트 응답이 생성됩니다. 만약 들어오는 요청이 XHR 요청이라면, [유효성 검사 에러 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드에 대해 더 잘 이해하기 위해 `store` 메서드 예제로 돌아가 봅시다.

```php
/**
 * 새 블로그 포스트 저장.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 포스트가 유효함...
}
```

보시다시피, 유효성 검사 규칙은 `validate` 메서드에 전달됩니다. 걱정하지 마세요 - 모든 유효성 검사 규칙은 [아래에 문서화되어 있습니다](#available-validation-rules). 검증에 실패하면, 적절한 응답이 자동으로 생성됩니다. 검증에 성공하면 컨트롤러는 정상적으로 계속 실행됩니다.

또한, 규칙을 `|`로 구분된 문자열 대신 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

추가로, [네임드 에러 백](#named-error-bags)에 에러 메시지를 저장하기 위해 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검사 실패 시 중지하기

때로는 어떤 속성에서 첫 번째 유효성 검사 실패 후 추가 검증을 중단하고 싶을 수 있습니다. 이를 위해 `bail` 규칙을 속성에 지정합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예제에서 `title`의 `unique` 규칙이 실패하면 `max` 규칙은 검사하지 않습니다. 규칙은 지정한 순서대로 검증합니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고사항

들어오는 HTTP 요청이 "중첩된" 필드 데이터를 포함한다면, 검증 규칙에서 "점 표기법(dot notation)"을 사용하여 이런 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 점이 포함되어 있다면, 백슬래시로 점을 이스케이프하여 "점 표기법"으로 해석되는 것을 방지할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 표시하기

만약 들어오는 요청 필드가 주어진 유효성 검사 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트하고, 모든 유효성 검사 에러와 [요청 입력값](/docs/{{version}}/requests#retrieving-old-input)을 [세션에 플래시](/docs/{{version}}/session#flash-data)합니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 애플리케이션의 모든 뷰에 `$errors` 변수를 공유합니다. 이는 `web` 미들웨어 그룹에 의해 제공되며, 이 미들웨어가 적용되면 뷰에서 항상 `$errors` 변수를 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체 사용법에 대한 자세한 내용은 [별도의 문서](#working-with-error-messages)를 참고하세요.

따라서, 예제에서 사용자가 검증에 실패하면 컨트롤러의 `create` 메서드로 리다이렉트되어 뷰에서 에러 메시지를 표시할 수 있습니다.

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
#### 에러 메시지 커스터마이즈하기

Laravel의 내장 유효성 검사 규칙마다 각 에러 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 이 파일에서 각 유효성 검사 규칙에 대한 번역 항목을 찾을 수 있습니다. 필요에 따라 이 메시지들을 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉토리로 복사하여 애플리케이션 언어에 맞는 메시지로 번역할 수 있습니다. Laravel 지역화(Localization)에 대해 더 자세히 알고 싶다면 [지역화 문서](/docs/{{version}}/localization)를 참고하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

이 예제에서는 전통적인 폼을 사용하여 데이터를 애플리케이션으로 전송했습니다. 하지만 많은 애플리케이션에서는 자바스크립트 기반 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 중 `validate` 메서드를 사용할 때, Laravel은 리다이렉트 응답을 생성하지 않습니다. 그 대신, [모든 유효성 검사 에러를 포함한 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 422 HTTP 상태 코드로 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

주어진 속성에 대해 유효성 검사 에러 메시지가 존재하는지 빠르게 확인하려면 [Blade](/docs/{{version}}/blade)에서 `@error` 디렉티브를 사용할 수 있습니다. `@error` 디렉티브 안에서 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다.

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

[네임드 에러 백](#named-error-bags)을 사용하는 경우, 두 번째 인자로 에러 백 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재설정(Repopulating)

유효성 검사 에러로 인해 Laravel이 리다이렉트 응답을 생성하면, 프레임워크는 요청의 모든 입력값을 자동으로 [세션에 플래시](/docs/{{version}}/session#flash-data)합니다. 이는 사용자가 제출하려 했던 폼을 다음 요청에서 쉽게 재설정할 수 있도록 하기 위함입니다.

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하십시오. `old` 메서드는 이전에 플래시된 입력 데이터를 [세션](/docs/{{version}}/session)에서 가져옵니다.

```php
$title = $request->old('title');
```

Blade 템플릿에서 옛 입력값을 표시할 때는 전역 `old` 헬퍼를 사용하는 것이 편리합니다. 해당 필드에 옛 입력이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 참고사항

기본적으로, Laravel에서는 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이 미들웨어는 `App\Http\Kernel` 클래스에 나열되어 있습니다. 때문에, 요청 필드를 "옵션"으로 두고 싶다면 검증 규칙에 `nullable`을 반드시 추가해야 합니다. 그렇지 않으면 `null` 값은 검증에 실패합니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서는 `publish_at` 필드가 `null` 이거나 날짜일 수 있음을 지정합니다. 만약 `nullable`을 명시하지 않으면, `null`은 유효하지 않은 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 에러 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대하면, Laravel은 에러 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래는 검증 에러에 대한 JSON 응답 형식 예시입니다. 중첩 에러 키는 "dot" 표기법으로 평탄화됩니다.

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

> ⚠️ **문서가 매우 깁니다. 요청하신 나머지(폼 요청 유효성 검사 이후~끝) 번역이 추가로 필요하다면 말씀해 주세요. 계속해서 번역해드릴 수 있습니다!**