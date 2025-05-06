# 검증(Validation)

- [소개](#introduction)
- [검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재할당(Repopulating)](#repopulating-forms)
    - [선택 필드에 대한 참고](#a-note-on-optional-fields)
- [폼 요청 검증](#form-request-validation)
    - [폼 요청 클래스 생성](#creating-form-requests)
    - [폼 요청 권한 부여](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [검증을 위한 입력 데이터 준비](#preparing-input-for-validation)
- [수동 검증기 생성](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [에러백 이름 지정](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [검증 후 후킹](#after-validation-hook)
- [검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일(언어팩)에서 커스텀 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 검증](#validating-arrays)
    - [검증되지 않은 배열 키 제외](#excluding-unvalidated-array-keys)
    - [중첩 배열 입력값의 검증](#validating-nested-array-input)
- [비밀번호 검증](#validating-passwords)
- [커스텀 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용](#using-rule-objects)
    - [클로저(Closure)로 사용](#using-closures)
    - [암시적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 입력 데이터를 검증하기 위한 여러 가지 방식을 제공합니다. 가장 흔하게는 모든 HTTP 요청에서 사용할 수 있는 `validate` 메소드를 사용합니다. 하지만, 이 문서에서는 그 외 다른 검증 방법들도 다룰 것입니다.

Laravel은 다양한 편리한 검증 규칙을 기본 제공하여 데이터에 손쉽게 적용할 수 있으며, 특정 값이 주어진 데이터베이스 테이블 내에서 유일한지 등도 검증할 수 있습니다. 본 문서에서는 각 검증 규칙을 자세히 설명하여 Laravel 검증 기능을 잘 이해할 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 검증 빠른 시작

Laravel의 강력한 검증 기능을 배우기 위해, 폼 데이터를 검증하고 사용자에게 에러 메시지를 반환하는 전체 예시를 살펴보겠습니다. 이 고수준 개요를 읽으면, Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 전반적인 흐름을 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

우선, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합시다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새로운 블로그 포스트를 작성하는 폼을 보여주고, `POST` 라우트는 데이터베이스에 새 블로그 포스트를 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위의 라우트 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. `store` 메소드는 아직 비워둡니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 새로운 블로그 포스트 작성 폼 표시
     *
     * @return \Illuminate\View\View
     */
    public function create()
    {
        return view('post.create');
    }

    /**
     * 새로운 블로그 포스트 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // 여기서 블로그 포스트의 검증 및 저장 작업...
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 검증 로직 작성하기

이제 `store` 메소드에 새 블로그 포스트를 검증하는 로직을 추가할 차례입니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메소드를 사용합니다. 규칙이 적용된 후, 검증에 성공하면 다음 코드가 정상적으로 계속 실행되고, 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하며, 적절한 에러 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 검증에 실패하면 이전 URL로 리다이렉트 응답이 생성됩니다. 만약 들어오는 요청이 XHR 요청이라면, 검증 에러 메시지를 포함하는 JSON 응답이 반환됩니다.

다시 `store` 메소드 예를 살펴보겠습니다.

```php
/**
 * 새로운 블로그 포스트 저장
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

    // 블로그 포스트는 유효합니다...
}
```

위에서처럼, 검증 규칙은 `validate` 메소드에 전달됩니다. 모든 사용 가능한 검증 규칙은 [문서](#available-validation-rules)에 있습니다. 검증에 실패하면, 적절한 응답이 자동으로 생성됩니다. 검증에 성공하면 컨트롤러는 원래대로 실행을 계속합니다.

또는, 검증 규칙을 `|`로 구분하는 문자열 대신 배열로도 지정할 수 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, `validateWithBag` 메소드를 사용해 [에러백 이름 지정](#named-error-bags)과 함께 요청을 검증할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단

특정 속성에 대해 첫 번째 검증 실패 후 남은 규칙 적용을 중단하고 싶을 수 있습니다. 이럴 때는 `bail` 규칙을 적용하세요:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서는 `title` 속성에서 `unique` 규칙이 실패하면, 그 다음 `max` 규칙은 검사하지 않습니다. 규칙은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

들어오는 HTTP 요청에 "중첩된(nested)" 필드 데이터가 있을 경우, "점(dot) 표기법"을 사용해 검증 규칙에 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 마침표가 포함된 경우, 백슬래시 `\`로 이스케이프 처리하여 점 표기법이 아닌 문자열로 인식되게 할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 검증 에러 표시하기

만약 요청 필드가 주어진 검증 규칙을 통과하지 못한다면 어떻게 될까요? 이전에 설명한 대로, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 또한 모든 검증 에러와 [요청 입력값](/docs/{{version}}/requests#retrieving-old-input)은 [세션에 플래시](/docs/{{version}}/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(기본적으로 `web` 미들웨어 그룹에 포함)는 모든 뷰에 `$errors` 변수(타입: `Illuminate\Support\MessageBag`)를 공유합니다. 이 미들웨어가 적용된 경우, 모든 뷰에서 `$errors` 변수가 항상 존재한다고 간주할 수 있어 안전하게 사용할 수 있습니다. 이 객체를 다루는 방법은 [추가 문서](#working-with-error-messages)에서 확인하세요.

예시에서는, 검증이 실패하면 사용자는 컨트롤러의 `create` 메소드로 리다이렉트 되어, 뷰에서 에러 메시지를 표시할 수 있게 됩니다.

```html
<!-- /resources/views/post/create.blade.php -->

<h1>포스트 작성</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- 포스트 작성 폼 -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 에러 메시지 커스터마이징

Laravel의 내장 검증 규칙마다 에러 메시지가 각 애플리케이션의 `resources/lang/en/validation.php` 파일에 위치합니다. 이 파일에는 각 규칙과 관련된 번역 항목이 있습니다. 필요에 따라 메시지를 자유롭게 수정하거나 변경할 수 있습니다.

또한, 이 파일을 다른 언어 번역 디렉토리로 복사하여 해당 언어로 메시지를 번역할 수도 있습니다. 자세한 사항은 [로컬라이제이션 공식 문서](/docs/{{version}}/localization)를 참고하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 검증

위 예제는 전통적인 폼 제출을 사용했습니다. 하지만 많은 애플리케이션에서는 프론트엔드에서 XHR 요청을 보냅니다. XHR 요청에서 `validate` 메소드를 사용하면 Laravel은 리다이렉션이 아닌, 검증 에러를 모두 담은 JSON 응답(HTTP 상태 코드 422)을 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

[Blade](/docs/{{version}}/blade)의 `@error` 디렉티브를 사용하면, 특정 속성에 검증 에러 메시지가 있는지를 빠르게 확인할 수 있습니다. `@error` 블록 내에서 `$message` 변수를 출력해 에러 메시지를 보여줄 수 있습니다.

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">포스트 제목</label>

<input id="title" type="text" name="title" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

[Named Error Bags](#named-error-bags)를 사용한다면, 두 번째 인자로 에러백 이름을 전달할 수 있습니다.

```html
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재할당(Repopulating)

Laravel이 검증 에러로 리다이렉트 응답을 생성할 때, 요청의 모든 입력값을 [세션에 플래시](/docs/{{version}}/session#flash-data)합니다. 이를 통해 다음 요청에서 입력값을 다시 사용할 수 있어, 사용자가 제출하려던 폼을 다시 채워 넣을 수 있습니다.

플래시된 입력값은 `Illuminate\Http\Request` 인스턴스의 `old` 메소드를 통해 가져올 수 있습니다.

```php
$title = $request->old('title');
```

또한, 전역 `old` 헬퍼를 사용하면 [Blade 템플릿](/docs/{{version}}/blade) 내에서 더욱 편리하게 폼 값을 재할당할 수 있습니다. 해당 필드에 플래시된 값이 없다면 `null`이 반환됩니다:

```html
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 필드에 대한 참고

Laravel은 기본적으로 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 전역 미들웨어 스택에 포함합니다(`App\Http\Kernel`에 정의됨). 때문에, "필수 아님" 필드를 `nullable`로 지정해두지 않으면, 검증기는 `null` 값을 유효하지 않은 것으로 간주할 수 있습니다. 예시:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

여기서는 `publish_at` 필드가 `null` 혹은 올바른 날짜 형식이어도 유효하게 처리됩니다. 만약 `nullable`을 지정하지 않으면, `null` 값이 데이터 유효하지 않다고 처리됩니다.

(이하 문서 계속 - 너무 길어서 1회 응답 제한으로 나누어 번역합니다. 나머지 섹션도 필요하시면 추가 번역 요청 가능합니다.)