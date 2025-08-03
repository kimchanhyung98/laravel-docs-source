# 검증 (Validation)

- [소개](#introduction)
- [검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [검증 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [선택적 필드에 대한 주의사항](#a-note-on-optional-fields)
- [폼 요청 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 권한 확인하기](#authorizing-form-requests)
    - [오류 메시지 맞춤화하기](#customizing-the-error-messages)
    - [검증을 위한 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 밸리데이터 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름 붙은 오류 가방](#named-error-bags)
    - [오류 메시지 맞춤화](#manual-customizing-the-error-messages)
    - [검증 후 후크](#after-validation-hook)
- [검증된 입력값 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일 내 맞춤 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일 내 속성 이름 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일 내 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 검증하기](#validating-arrays)
    - [검증하지 않은 배열 키 제외하기](#excluding-unvalidated-array-keys)
    - [중첩 배열 입력 검증하기](#validating-nested-array-input)
- [비밀번호 검증하기](#validating-passwords)
- [사용자 지정 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 들어오는 데이터를 검증할 수 있는 여러 가지 방법을 제공합니다. 가장 일반적인 방법은 모든 HTTP 요청에 사용 가능한 `validate` 메서드를 이용하는 것입니다. 하지만 이외에도 다양한 검증 방법을 살펴보겠습니다.

Laravel은 데이터에 적용할 수 있는 매우 다양한 편리한 검증 규칙을 포함하고 있습니다. 특정 데이터가 데이터베이스 내에서 유일한지 검증하는 기능도 제공하죠. 모든 검증 규칙을 자세히 설명하므로 Laravel의 모든 검증 기능을 익히는 데 도움이 될 것입니다.

<a name="validation-quickstart"></a>
## 검증 빠른 시작

Laravel의 강력한 검증 기능을 이해하기 위해, 폼 검증과 검증 오류 메시지를 사용자에게 다시 표시하는 완전한 예제를 살펴보겠습니다. 이 개요를 통해 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 큰 그림을 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합니다:

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자에게 새 블로그 글 작성 폼을 표시하며, `POST` 라우트는 새 블로그 게시글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이 라우트를 처리하는 간단한 컨트롤러를 살펴봅니다. `store` 메서드는 아직 비워둡니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 새 블로그 글 작성 폼을 표시합니다.
     *
     * @return \Illuminate\View\View
     */
    public function create()
    {
        return view('post.create');
    }

    /**
     * 새 블로그 글을 저장합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // 블로그 글을 검증하고 저장합니다...
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 검증 로직 작성하기

이제 `store` 메서드를 새 블로그 글을 검증하기 위한 로직으로 채워보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 검증 규칙이 통과하면 코드는 정상적으로 계속 실행되지만, 검증이 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하며 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 검증 실패 시, 이전 URL로 리다이렉트 응답이 생성됩니다. XHR 요청인 경우, 검증 오류 메시지를 포함한 JSON 응답이 반환됩니다.

`validate` 메서드를 좀 더 잘 이해하기 위해 `store` 메서드 코드를 살펴봅시다:

```
/**
 * 새 블로그 글을 저장합니다.
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

    // 블로그 글이 유효함...
}
```

보시는 것처럼, 검증 규칙들은 `validate` 메서드에 전달됩니다. 걱정하지 마세요. 모든 가능한 검증 규칙은 [문서화되어 있습니다](#available-validation-rules). 검증 실패 시 적절한 응답이 자동 생성되며, 통과 시에는 컨트롤러 로직이 정상적으로 이어집니다.

대안으로, 검증 규칙을 문자열 대신 배열 형식으로도 지정할 수 있습니다:

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, `validateWithBag` 메서드를 써서 요청을 검증하고 오류 메시지를 [이름이 지정된 오류 가방](#named-error-bags)에 저장할 수 있습니다:

```
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 검사 중단하기

가끔 검사 과정에서 첫 번째 실패가 발생하면 더 이상 다른 검증 규칙을 실행하지 않도록 하고싶을 때가 있습니다. 이럴 때는 `bail` 규칙을 해당 속성에 지정하세요:

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서, `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙은 평가되지 않습니다. 규칙들은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 주의사항

HTTP 요청에 "중첩" 필드가 포함된 경우, 검증 규칙에서는 "dot" 문법을 써서 지정할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 마침표가 포함된 경우, 역슬래시로 이스케이프하여 "dot" 문법으로 인식되지 않도록 할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 검증 오류 표시하기

요청 필드가 주어진 검증 규칙에 통과하지 못하면 어떻게 될까요? 앞서 설명한 대로, Laravel은 자동으로 이전 위치로 리다이렉트합니다. 그리고 모든 검증 오류 및 [요청 입력 값](/docs/{{version}}/requests#retrieving-old-input)이 자동으로 세션에 [플래시](flash)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(웹 미들웨어 그룹에 포함됨)는 모든 뷰에 `$errors` 변수를 공유합니다. 따라서 컨트롤러에서 오류가 발생하여 리다이렉트될 때, 뷰 내에서 항상 `$errors` 변수를 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 다루는 방법은 [오류 메시지 작업](#working-with-error-messages)을 참고하세요.

예제에서, 검증 실패 시 사용자에게 컨트롤러 `create` 메서드로 리다이렉트하여 뷰에서 오류 메시지를 표시할 수 있습니다:

```html
<!-- /resources/views/post/create.blade.php -->

<h1>글 작성하기</h1>

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
#### 오류 메시지 맞춤화하기

Laravel 내장 검증 규칙에 대한 기본 오류 메시지는 애플리케이션의 `resources/lang/en/validation.php` 파일에 위치합니다. 이 파일 내에서 각 검증 규칙별 메시지를 확인할 수 있으며, 필요에 따라 애플리케이션 요구사항에 맞게 수정할 수 있습니다.

추가로 이 파일을 다른 번역 언어 디렉터리로 복사하여 애플리케이션 언어에 맞게 메시지 번역을 만들 수도 있습니다. Laravel 로컬라이제이션에 대해 더 자세히 알고 싶다면 [로컬라이제이션 문서](/docs/{{version}}/localization)를 참고하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 검증

예제에서는 전통적인 HTML 폼을 통해 데이터를 전송했지만, 많은 애플리케이션은 자바스크립트 기반 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 시 `validate` 메서드를 사용하면 Laravel은 리다이렉트 응답을 생성하지 않고, 422 HTTP 상태 코드와 함께 검증 오류 메시지를 포함한 JSON 응답을 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` Blade 지시어

[Blade](/docs/{{version}}/blade)의 `@error` 지시어를 사용하면 특정 속성에 대해 검증 오류 메시지가 존재하는지 손쉽게 확인할 수 있습니다. `@error` 블록 안에서 `$message` 변수를 출력하여 오류 메시지를 표시할 수 있습니다:

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">글 제목</label>

<input id="title" type="text" name="title" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

만약 [이름 붙은 오류 가방](#named-error-bags)을 사용한다면, `@error` 지시어의 두 번째 인자로 오류 가방 이름을 넘길 수 있습니다:

```html
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

Laravel이 검증 오류로 인해 리다이렉션 응답을 생성할 때, 프레임워크는 자동으로 [요청 입력값 전부를 세션에 플래시]( /docs/{{version}}/session#flash-data)합니다. 이는 다음 요청 시 사용자가 제출하려던 폼을 쉽게 다시 채울 수 있도록 하기 위함입니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하세요. `old` 메서드는 이전에 플래시된 세션 데이터를 반환합니다:

```
$title = $request->old('title');
```

또한, Blade 템플릿 내에서는 전역 `old` 헬퍼를 사용하는 편이 편리합니다. 주어진 필드에 대한 과거 입력값이 없다면 `null`을 반환합니다:

```
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 주의사항

기본적으로, Laravel은 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 애플리케이션의 전역 미들웨어 스택에 포함시킵니다. 이 미들웨어들은 `App\Http\Kernel` 클래스 내에 나열돼있습니다. 그래서 "선택적" 요청 필드는 `nullable` 규칙을 반드시 명시하여야 검증기가 `null` 값을 유효하지 않은 값으로 처리하지 않습니다. 예를 들어:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

여기서는 `publish_at` 필드를 `null`이거나 유효한 날짜일 수 있다고 명시했습니다. `nullable`을 생략하면 검증기는 `null` 값을 부적절한 날짜로 간주합니다.

<a name="form-request-validation"></a>
## 폼 요청 검증 (Form Request Validation)

<a name="creating-form-requests"></a>
### 폼 요청 생성하기

더 복잡한 검증 시나리오를 위해 "폼 요청" 클래스를 생성할 수 있습니다. 폼 요청은 검증 및 권한 로직을 자체적으로 포함하는 요청 클래스입니다. `make:request` Artisan 명령어로 생성할 수 있습니다:

```
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 이 디렉터리가 없으면 명령 실행 시 생성됩니다. 생성된 폼 요청 클래스에는 `authorize`와 `rules` 두 메서드가 포함됩니다.

`authorize` 메서드는 현재 인증된 사용자가 요청된 행동을 수행할 권한이 있는지 확인합니다. `rules` 메서드는 요청에 적용할 검증 규칙 배열을 반환합니다:

```
/**
 * 요청에 적용할 검증 규칙을 반환합니다.
 *
 * @return array
 */
public function rules()
{
    return [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ];
}
```

> [!TIP]
> `rules` 메서드의 시그니처에 필요한 의존성을 타입 힌팅하면 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 해결해 줍니다.

그럼 어떻게 검증 규칙을 평가할까요? 컨트롤러 메서드에 폼 요청 클래스를 타입 힌트하기만 하면 됩니다. 폼 요청은 컨트롤러 메서드가 실행되기 전에 자동으로 검증하며, 검증 로직을 컨트롤러에 직접 작성할 필요가 없습니다:

```
/**
 * 새 블로그 글을 저장합니다.
 *
 * @param  \App\Http\Requests\StorePostRequest  $request
 * @return Illuminate\Http\Response
 */
public function store(StorePostRequest $request)
{
    // 검증된 요청 데이터...

    // 검증된 입력값 전체를 가져오기
    $validated = $request->validated();

    // 검증된 입력값 중 특정 필드만 가져오기
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);
}
```

검증 실패 시, 자동으로 이전 위치로 리다이렉트 응답이 보내지고 오류 메시지가 세션에 플래시됩니다. XHR 요청이라면 422 상태 코드와 함께 JSON 형태의 검증 오류가 반환됩니다.

<a name="adding-after-hooks-to-form-requests"></a>
#### 폼 요청에 후속 후크 추가하기

검증 후 추가 작업을 수행하고 싶으면 `withValidator` 메서드를 사용할 수 있습니다. 이 메서드는 완성된 검증기 인스턴스를 받아 실제 규칙 평가 전에 검증기의 메서드를 호출할 수 있게 해줍니다:

```
/**
 * 검증기 인스턴스를 구성합니다.
 *
 * @param  \Illuminate\Validation\Validator  $validator
 * @return void
 */
public function withValidator($validator)
{
    $validator->after(function ($validator) {
        if ($this->somethingElseIsInvalid()) {
            $validator->errors()->add('field', '이 필드에 문제가 있습니다!');
        }
    });
}
```

<a name="request-stopping-on-first-validation-rule-failure"></a>
#### 첫 번째 검증 실패 시 전체 중단 속성

폼 요청 클래스에 `stopOnFirstFailure` 속성을 추가하면, 검증기는 단일 검증 실패가 발생하면 모든 속성에 대한 검증을 중단하도록 알릴 수 있습니다:

```
/**
 * 검증 규칙 실패 시 첫 실패에서 검증을 중단할지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 맞춤 설정

기본적으로, 폼 요청 검증 실패 시 이전 위치로 리다이렉트됩니다. 하지만 이 동작을 변경하고 싶으면, 폼 요청 클래스 내에 `$redirect` 속성을 정의하세요:

```
/**
 * 검증 실패 시 리다이렉트할 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 라우트 이름으로 리다이렉트할 경우 `$redirectRoute` 속성을 지정할 수 있습니다:

```
/**
 * 검증 실패 시 리다이렉트할 라우트 이름.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 권한 확인하기

폼 요청 클래스의 `authorize` 메서드에서 인증된 사용자가 요청된 작업을 수행할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 자신이 작성하지 않은 블로그 댓글 수정 요청을 시도하는지 등을 확인할 수 있습니다. 보통 이곳에서 [인가 게이트와 정책](/docs/{{version}}/authorization)을 사용합니다:

```
use App\Models\Comment;

/**
 * 요청 권한을 확인합니다.
 *
 * @return bool
 */
public function authorize()
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

폼 요청 클래스는 Laravel의 기본 요청 클래스를 상속받아, 현재 인증된 사용자를 `user` 메서드로 조회할 수 있습니다. 예시 코드처럼 `route` 메서드를 호출하여 라우트 URI에서 정의된 매개변수(예: `{comment}`)를 얻을 수 있습니다:

```
Route::post('/comment/{comment}');
```

만약 [라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용 중이라면, 요청 객체에서 바로 매핑된 모델 인스턴스를 속성으로 접근할 수도 있습니다:

```
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면 HTTP 403 응답이 자동 생성되고 컨트롤러 메서드는 실행되지 않습니다.

만약 해당 요청의 권한 판단을 다른 곳에서 처리한다면, 간단히 `authorize` 메서드에서 `true`를 반환해도 됩니다:

```
/**
 * 요청 권한을 확인합니다.
 *
 * @return bool
 */
public function authorize()
{
    return true;
}
```

> [!TIP]
> `authorize` 메서드에 필요한 의존성을 타입 힌팅하면 Laravel [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 해결해 줍니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 맞춤화하기

폼 요청에 사용할 오류 메시지는 `messages` 메서드를 오버라이드하여 조정할 수 있습니다. 이 메서드는 속성명과 규칙 조합별 커스텀 메시지 배열을 반환해야 합니다:

```
/**
 * 정의된 검증 규칙에 대한 오류 메시지를 반환합니다.
 *
 * @return array
 */
public function messages()
{
    return [
        'title.required' => '제목은 필수 입력입니다',
        'body.required' => '내용은 필수 입력입니다',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 검증 속성 이름 맞춤화하기

많은 Laravel 내장 검증 메시지에서 `:attribute` 자리표시자가 포함되어 있습니다. 이 부분을 사용자 지정 이름으로 대체하려면 `attributes` 메서드를 오버라이드하세요. 속성명과 사용자 지정 이름 배열을 반환하면 됩니다:

```
/**
 * 검증기 오류를 위해 사용자 지정 속성 이름을 반환합니다.
 *
 * @return array
 */
public function attributes()
{
    return [
        'email' => '이메일 주소',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### 검증을 위한 입력값 준비하기

검증 규칙을 적용하기 전에 요청 데이터에서 전처리나 정제를 수행해야 할 때가 있습니다. 이럴 때는 `prepareForValidation` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Str;

/**
 * 검증을 준비하기 위한 데이터 전처리.
 *
 * @return void
 */
protected function prepareForValidation()
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 밸리데이터 생성하기

요청의 `validate` 메서드를 사용하지 않으려면, `Validator` [파사드](/docs/{{version}}/facades)를 이용해 밸리데이터 인스턴스를 직접 만들 수 있습니다. `make` 메서드가 새 검증기 인스턴스를 생성합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 글 저장
     *
     * @param  Request  $request
     * @return Response
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        if ($validator->fails()) {
            return redirect('post/create')
                        ->withErrors($validator)
                        ->withInput();
        }

        // 검증된 입력값 가져오기...
        $validated = $validator->validated();

        // 검증된 입력 중 특정 필드만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 글 저장...
    }
}
```

`make` 메서드의 첫 번째 인자는 검증 대상 데이터이며, 두 번째는 데이터에 적용할 검증 규칙 배열입니다.

검증 실패 여부를 판단한 후 `withErrors` 메서드를 호출해 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 쓰면 `$errors` 변수가 리다이렉트 후 뷰에 자동 공유되어 쉽게 오류를 표시할 수 있습니다. `withErrors`는 밸리데이터, `MessageBag`, 또는 PHP 배열을 인자로 받습니다.

#### 첫 번째 검증 실패 시 중단

`stopOnFirstFailure` 메서드로 단일 검증 실패 발생 시 모든 속성에 대한 검증 중단을 알릴 수 있습니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

밸리데이터 인스턴스를 직접 만들되, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 사용하고 싶을 땐, 밸리데이터 인스턴스의 `validate` 메서드를 호출하세요. 실패 시 자동으로 리다이렉션 혹은 XHR 요청이면 JSON 응답을 반환합니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

이름 붙은 오류 가방에 메시지를 저장하려면 `validateWithBag` 메서드를 이용합니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름 붙은 오류 가방

한 페이지 내 여러 폼이 있을 때, 각기 다른 오류 가방 이름을 지정하면 특정 폼에 대한 오류 메시지만 쉽게 조회할 수 있습니다. `withErrors` 호출 시 두 번째 인자로 이름을 전달하세요:

```
return redirect('register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수에서 이름 붙은 가방에 접근할 수 있습니다:

```
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 맞춤화

필요에 따라 Laravel 기본 메시지 대신 밸리데이터 인스턴스에 맞춤 오류 메시지를 지정할 수 있습니다. 가장 간단한 방법은 `Validator::make` 메서드의 세 번째 인자로 메시지 배열을 전달하는 것입니다:

```
$validator = Validator::make($input, $rules, [
    'required' => 'The :attribute field is required.',
]);
```

`required` 메시지 내 `:attribute`는 검증 대상 필드명으로 대체됩니다. 메시지 내 다른 자리표시자도 사용할 수 있습니다:

```
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 맞춤 메시지 지정

특정 속성에 대해서만 메시지를 지정하려면 "dot" 문법으로 속성명과 규칙명을 연결해 지정할 수 있습니다:

```
$messages = [
    'email.required' => '이메일 주소를 꼭 알려주세요!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 사용자 지정 속성명 지정

기본 메시지 내 `:attribute` 자리표시자의 대체명칭을 바꾸고 싶다면, `Validator::make` 메서드의 네 번째 인자로 배열을 넘겨 속성명 커스텀 매핑을 지정할 수 있습니다:

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="after-validation-hook"></a>
### 검증 후 후크

검증 완료 직후 실행할 콜백을 등록해 추가 검사를 하거나 메시지를 더할 수 있습니다. 밸리데이터 인스턴스의 `after` 메서드에 콜백을 전달하세요:

```
$validator = Validator::make(...);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', '이 필드에 문제가 있습니다!'
        );
    }
});

if ($validator->fails()) {
    //
}
```

<a name="working-with-validated-input"></a>
## 검증된 입력값 다루기

폼 요청이나 직접 생성한 밸리데이터 인스턴스로 요청 데이터를 검증한 후, 검증된 입력값만 따로 가져올 수 있습니다.

먼저, 폼 요청이나 밸리데이터 인스턴스에서 `validated` 메서드를 호출하면, 검증된 데이터 배열을 얻을 수 있습니다:

```
$validated = $request->validated();

$validated = $validator->validated();
```

대안으로, `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체를 통해 일부 필드만 `only()`, 특정 필드 제외 `except()`, 전체 데이터 모두 `all()` 메서드로 선택할 수 있습니다:

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나 배열 식으로 접근할 수 있습니다:

```php
// 검증된 데이터 반복하기
foreach ($request->safe() as $key => $value) {
    //
}

// 배열로 접근하기
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 더하고 싶으면 `merge` 메서드를 호출할 수 있습니다:

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/{{version}}/collections)으로 받고 싶다면 `collect` 메서드를 사용하세요:

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기

`Validator` 인스턴스의 `errors` 메서드를 호출하면, `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. 이 객체는 오류 메시지를 다루기 위한 다양한 편리한 메서드를 포함합니다. 자동으로 뷰에 공유되는 `$errors` 변수도 `MessageBag` 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 오류 메시지 가져오기

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

```
foreach ($errors->get('email') as $message) {
    //
}
```

만약 배열 형태 필드를 검증하고 있다면, `*` 와일드카드를 사용해 배열 각 요소의 메시지를 모두 가져올 수도 있습니다:

```
foreach ($errors->get('attachments.*') as $message) {
    //
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 가져오기

```
foreach ($errors->all() as $message) {
    //
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 오류 메시지 존재 여부 확인

```
if ($errors->has('email')) {
    //
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일 내 맞춤 메시지 지정하기

Laravel 내장 검증 규칙의 기본 오류 메시지는 `resources/lang/en/validation.php` 파일에 위치합니다. 각 규칙별로 번역 항목이 포함되어 있어 필요에 따라 수정하여 사용할 수 있습니다.

추가로 해당 파일을 다른 로컬 번역 언어 디렉터리로 복사하여 애플리케이션 언어에 맞게 번역할 수도 있습니다. 더 자세한 내용은 [로컬라이제이션 문서](/docs/{{version}}/localization)를 참고하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 맞춤 메시지

애플리케이션의 검증 번역 파일 내 `custom` 배열에 속성명과 규칙별 메시지 배열을 추가하면 특정 속성과 규칙 조합에 맞는 맞춤 오류 메시지를 지정할 수 있습니다:

```
'custom' => [
    'email' => [
        'required' => '이메일 주소를 꼭 알려주세요!',
        'max' => '이메일 주소가 너무 깁니다!',
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일 내 속성 이름 지정하기

많은 내장 오류 메시지에 포함되는 `:attribute` 자리표시자를 커스텀 값으로 교체하려면, `resources/lang/xx/validation.php` 파일 내 `attributes` 배열에 사용자 지정 속성명을 정의하세요:

```
'attributes' => [
    'email' => '이메일 주소',
],
```

<a name="specifying-values-in-language-files"></a>
### 언어 파일 내 값 지정하기

내장 검증 규칙 메시지 중 `:value` 자리표시자가 요청 값으로 대체되는 경우가 있습니다. 때로는 이 값을 좀 더 친숙한 표현으로 바꾸고 싶을 수 있습니다.

예를 들어, `payment_type` 값이 `cc`일 때 `credit_card_number` 필드가 필수인 경우:

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

검증 실패 시 출력 메시지는 다음과 같습니다:

```
The credit card number field is required when payment type is cc.
```

이때 `cc` 대신 사용자 친화적 용어를 알맞게 바꾸고 싶으면 `values` 배열에 값을 지정합니다:

```
'values' => [
    'payment_type' => [
        'cc' => '신용카드',
    ],
],
```

그러면 메시지는 이렇게 출력됩니다:

```
The credit card number field is required when payment type is 신용카드.
```

<a name="available-validation-rules"></a>
## 사용 가능한 검증 규칙

아래는 사용 가능한 모든 검증 규칙과 그 기능 목록입니다:

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Active URL](#rule-active-url)
[After (Date)](#rule-after)
[After Or Equal (Date)](#rule-after-or-equal)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Array](#rule-array)
[Bail](#rule-bail)
[Before (Date)](#rule-before)
[Before Or Equal (Date)](#rule-before-or-equal)
[Between](#rule-between)
[Boolean](#rule-boolean)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Dimensions (Image Files)](#rule-dimensions)
[Distinct](#rule-distinct)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude Without](#rule-exclude-without)
[Exists (Database)](#rule-exists)
[File](#rule-file)
[Filled](#rule-filled)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Image (File)](#rule-image)
[In](#rule-in)
[In Array](#rule-in-array)
[Integer](#rule-integer)
[IP Address](#rule-ip)
[MAC Address](#rule-mac)
[JSON](#rule-json)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Min](#rule-min)
[Multiple Of](#multiple-of)
[Not In](#rule-not-in)
[Not Regex](#rule-not-regex)
[Nullable](#rule-nullable)
[Numeric](#rule-numeric)
[Password](#rule-password)
[Present](#rule-present)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Regular Expression](#rule-regex)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#validating-when-present)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[Unique (Database)](#rule-unique)
[URL](#rule-url)
[UUID](#rule-uuid)

</div>

<a name="rule-accepted"></a>
#### accepted

검증 대상 필드는 `"yes"`, `"on"`, `1`, 또는 `true` 중 하나여야 합니다. 주로 "서비스 약관 동의"와 같은 필드 검증에 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:다른필드,값,...

다른 필드가 지정한 값과 같다면, 해당 필드도 `"yes"`, `"on"`, `1`, 또는 `true`여야 합니다. "서비스 약관 동의" 등 조건부 검증 시 사용합니다.

<a name="rule-active-url"></a>
#### active_url

검증 필드 값은 `dns_get_record` PHP 함수로 조회 가능한 유효한 A 또는 AAAA DNS 레코드가 있어야 합니다. URL의 호스트네임은 `parse_url` 함수로 먼저 추출합니다.

<a name="rule-after"></a>
#### after:_date_

검증 필드는 지정한 날짜 이후여야 합니다. 날짜 문자열은 `strtotime` 함수로 변환되어 처리됩니다:

```
'start_date' => 'required|date|after:tomorrow'
```

날짜 문자열 대신, 다른 필드 이름을 지정해 비교 기준으로 사용할 수도 있습니다:

```
'finish_date' => 'required|date|after:start_date'
```

<a name="rule-after-or-equal"></a>
#### after_or_equal:_date_

검증 필드는 지정 날짜 이후거나 같아야 합니다. 더 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

<a name="rule-alpha"></a>
#### alpha

검증 필드는 오로지 알파벳 문자만 포함해야 합니다.

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 필드는 알파벳, 숫자, 대시(`-`), 밑줄(`_`)만 포함할 수 있습니다.

<a name="rule-alpha-num"></a>
#### alpha_num

검증 필드는 알파벳과 숫자만 포함해야 합니다.

<a name="rule-array"></a>
#### array

검증 필드는 PHP 배열이어야 합니다.

`array` 규칙에 추가 허용 키를 지정하면, 입력 배열의 키가 반드시 지정한 키 목록에 존재해야 합니다. 예를 들어 다음에서 `admin` 키는 검증 실패합니다:

```
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => 'array:username,locale',
]);
```

일반적으로 배열 내 허용 키를 구체적으로 명시하는 것이 좋습니다. 그렇지 않으면 `validate`와 `validated` 메서드가 검증되지 않은 키까지 모두 반환할 수 있습니다.

필요하다면, `AppServiceProvider`의 `boot` 메서드에서 밸리데이터의 `excludeUnvalidatedArrayKeys` 메서드를 호출해 검증되지 않은 배열 키를 결과에 포함하지 않도록 할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

/**
 * 애플리케이션 서비스 등록
 *
 * @return void
 */
public function boot()
{
    Validator::excludeUnvalidatedArrayKeys();
}
```

<a name="rule-bail"></a>
#### bail

첫 번째 검증 실패가 발생하면 해당 필드에 대한 나머지 검증 규칙 실행을 중단합니다.

`bail` 규칙은 필드별 중단용이고, `stopOnFirstFailure` 메서드는 전 필드에 대한 단일 실패 시 전체 중단용입니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 필드는 지정한 날짜 이전이어야 합니다. 날짜 문자열은 PHP `strtotime` 함수를 통해 변환됩니다. [`after`](#rule-after) 규칙처럼 비교 대상 필드명을 지정할 수도 있습니다.

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 필드는 지정 날짜 이전이거나 같아야 합니다. `before` 규칙과 같은 방법으로 동작합니다.

<a name="rule-between"></a>
#### between:_min_,_max_

검증 필드는 크기가 지정한 최솟값 `min`과 최댓값 `max` 사이여야 합니다. 문자열, 숫자, 배열, 파일에 대해 [`size`](#rule-size) 규칙과 같은 방식으로 평가합니다.

<a name="rule-boolean"></a>
#### boolean

검증 필드는 불리언으로 변환 가능한 값이어야 합니다. 허용값은 `true`, `false`, `1`, `0`, `"1"`, `"0"` 입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드는 `{field}_confirmation` 이름의 필드와 값이 일치해야 합니다. 예를 들어 `password` 필드의 경우 `password_confirmation` 필드가 있어야 합니다.

<a name="rule-current-password"></a>
#### current_password

검증 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙 첫 번째 인자로 [인증 가드](/docs/{{version}}/authentication)를 지정할 수 있습니다:

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 필드는 `strtotime` 함수가 인식할 수 있는 유효한 절대 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 필드는 지정한 날짜와 같아야 합니다. 날짜 문자열로 변환 시 `strtotime` 함수를 사용합니다.

<a name="rule-date-format"></a>
#### date_format:_format_

검증 필드는 지정한 포맷과 일치해야 합니다. `date`와 `date_format`은 둘 다 쓰지 않는 것이 좋습니다. PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 포맷을 사용할 수 있습니다.

<a name="rule-declined"></a>
#### declined

검증 필드는 `"no"`, `"off"`, `0`, 또는 `false` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:다른필드,값,...

다른 필드가 지정한 값과 같다면, 해당 필드가 `"no"`, `"off"`, `0`, 또는 `false` 여야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드는 지정된 `_field_` 값과 달라야 합니다.

<a name="rule-digits"></a>
#### digits:_값_

검증 필드는 숫자이며 정확히 지정한 길이 `_value_`여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 필드는 숫자이며 길이가 `_min_`과 `_max_` 사이여야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 지정된 치수 제한을 만족하는 이미지여야 합니다:

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

허용 제약조건은 _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_ 입니다.

`_ratio_` 제약은 가로/세로 비율로서 `3/2` 또는 `1.5`와 같이 지정할 수 있습니다:

```
'avatar' => 'dimensions:ratio=3/2'
```

여러 매개변수를 사용할 때는 `Rule::dimensions` 메서드로 유연하게 생성 가능합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
    ],
]);
```

<a name="rule-distinct"></a>
#### distinct

배열 검증 시, 중복 값이 없어야 합니다:

```
'foo.*.id' => 'distinct'
```

기본은 느슨한 비교이며, 엄격한 비교를 위해 `strict` 매개변수를 추가할 수 있습니다:

```
'foo.*.id' => 'distinct:strict'
```

대소문자를 무시하려면 `ignore_case` 매개변수도 가능합니다:

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-email"></a>
#### email

검증 필드는 이메일 형식이어야 합니다. 이 규칙은 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본은 `RFCValidation`이지만 여러 스타일이 있습니다:

```
'email' => 'email:rfc,dns'
```

`rfc`, `strict`, `dns`, `spoof`, `filter` 등 다양한 검증 스타일 적용 가능.

`filter` 검증기는 PHP 내장 `filter_var` 함수를 쓰며, Laravel 5.8 이전 기본 이메일 검증 방법이었습니다.

> [!NOTE]
> `dns`와 `spoof` 검증에 PHP `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_값1_,_값2_,...

검증 필드는 지정한 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 클래스 기반 규칙으로, 필드 값이 유효한 PHP 8.1+ Enum 값인지 검증합니다:

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rules\Enum;

$request->validate([
    'status' => [new Enum(ServerStatus::class)],
]);
```

> [!NOTE]
> Enum은 PHP 8.1 이상에서만 사용할 수 있습니다.

<a name="rule-exclude"></a>
#### exclude

검증 대상 필드는 `validate`와 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:다른필드,값

다른 필드가 지정 값과 같으면, 검증 대상 필드는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-unless"></a>
#### exclude_unless:다른필드,값

다른 필드가 지정 값과 다르면, 해당 필드를 요청 데이터에서 제외합니다. 값이 `null`인 경우(`exclude_unless:name,null`)는 기준 필드 또한 `null`이거나 요청에 없을 때 제외합니다.

<a name="rule-exclude-without"></a>
#### exclude_without:다른필드

다른 필드가 존재하지 않을 경우, 검증 필드를 요청 데이터에서 제외합니다.

<a name="rule-exists"></a>
#### exists:_테이블_,_컬럼_

검증 필드 값은 지정한 데이터베이스 테이블 내에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 규칙 기본 사용법

```
'state' => 'exists:states'
```

테이블 내의 `state` 컬럼 값이 요청 값과 일치하는 레코드가 있어야 합니다.

<a name="specifying-a-custom-column-name"></a>
#### 커스텀 컬럼명 지정

테이블명 뒤에 컬럼명을 명시할 수 있습니다:

```
'state' => 'exists:states,abbreviation'
```

특정 데이터베이스 커넥션을 지정하려면 연결명도 가능합니다:

```
'email' => 'exists:connection.staff,email'
```

테이블명 대신 Eloquent 모델명을 사용할 수도 있습니다:

```
'user_id' => 'exists:App\Models\User,id'
```

문 실행 쿼리를 커스터마이징하려면 `Rule` 클래스를 활용하세요:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function ($query) {
            return $query->where('account_id', 1);
        }),
    ],
]);
```

<a name="rule-file"></a>
#### file

검증 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

검증 필드는 존재할 경우 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_필드_

검증 필드 값은 지정된 다른 필드 값보다 커야 합니다. 두 필드는 같은 타입이어야 하며 [`size`](#rule-size) 규칙과 같은 평가 방식을 따릅니다.

<a name="rule-gte"></a>
#### gte:_필드_

검증 필드 값은 지정된 다른 필드 값보다 크거나 같아야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지(jpg, jpeg, png, bmp, gif, svg, webp)여야 합니다.

<a name="rule-in"></a>
#### in:_값1_,_값2_,...

검증 필드는 지정 값 목록 내에 포함되어야 합니다. 배열 검증 시 `Rule::in` 메서드 이용도 가능합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

배열과 함께 쓰면 입력 배열의 각 값이 지정된 목록에 모두 포함돼야 합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
        Rule::in(['NYC', 'LIT']),
    ],
]);
```

`LAS`는 지정값에 없어 유효하지 않습니다.

<a name="rule-in-array"></a>
#### in_array:_다른필드_.*

검증 필드는 다른 지정 필드 값들 중 하나에 속해야 합니다.

<a name="rule-integer"></a>
#### integer

검증 필드는 정수여야 합니다.

> [!NOTE]
> 해당 검증은 데이터 타입을 체크하는 것이 아니라 PHP `FILTER_VALIDATE_INT` 필터가 허용하는 형식만 충족하는지 검사합니다. 숫자 여부 검증 시에는 `[numeric](#rule-numeric)` 규칙과 함께 사용하세요.

<a name="rule-ip"></a>
#### ip

검증 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

검증 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증 필드는 IPv6 주소여야 합니다.

<a name="rule-mac"></a>
#### mac_address

검증 필드는 MAC 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_필드_

검증 필드는 지정된 다른 필드 값보다 작아야 합니다.

<a name="rule-lte"></a>
#### lte:_필드_

검증 필드는 지정된 다른 필드 값보다 작거나 같아야 합니다.

<a name="rule-max"></a>
#### max:_값_

검증 필드는 최대 크기 `값`을 넘지 않아야 합니다. [`size`](#rule-size) 규칙과 같은 방식으로 평가합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_MIME타입1_,_MIME타입2_,...

검증 파일은 지정한 MIME 타입 중 하나와 일치해야 합니다:

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드 파일의 실제 내용 기반 MIME 타입을 판단합니다.

<a name="rule-mimes"></a>
#### mimes:_확장자1_,_확장자2_,...

검증 파일은 지정한 확장자에 해당하는 MIME 타입이어야 합니다.

<a name="basic-usage-of-mime-rule"></a>
#### MIME 규칙 기본 사용법

```
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정해도 파일 내용으로 MIME 타입을 판단해 검증합니다. 전체 MIME 타입과 확장자 목록은 다음 링크에서 확인할 수 있습니다:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_값_

검증 필드는 최소 크기 `_값_` 이상이어야 합니다.

<a name="multiple-of"></a>
#### multiple_of:_값_

검증 필드는 지정한 숫자의 배수여야 합니다.

> [!NOTE]
> `multiple_of` 규칙 사용을 위해선 [`bcmath` PHP 확장](https://www.php.net/manual/en/book.bc.php)이 필요합니다.

<a name="rule-not-in"></a>
#### not_in:_값1_,_값2_,...

검증 필드는 지정한 값 목록에 포함되면 안 됩니다.

```
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a name="rule-not-regex"></a>
#### not_regex:_패턴_

검증 필드는 지정한 정규 표현식과 일치하면 안 됩니다.

내부적으로 PHP `preg_match` 함수를 사용하기에 패턴은 `preg_match` 규칙을 따라야 합니다. 예시: `'email' => 'not_regex:/^.+$/i'`.

> [!NOTE]
> `regex` 또는 `not_regex` 패턴은 `|` 같은 문자가 포함될 경우 배열 형식으로 규칙을 지정하는 것이 좋습니다.

<a name="rule-nullable"></a>
#### nullable

검증 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

검증 필드는 숫자 형식이어야 합니다.

<a name="rule-password"></a>
#### password

검증 필드는 인증된 사용자의 비밀번호와 일치해야 합니다.

> [!NOTE]
> 이 규칙은 Laravel 9에서 제거 예정이며, `current_password` 규칙으로 대체되었습니다.

<a name="rule-present"></a>
#### present

검증 필드는 입력에 존재해야 하지만 비어 있을 수 있습니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 필드는 비어 있거나 존재하지 않아야 합니다.

<a name="rule-prohibited-if"></a>
#### prohibited_if:다른필드,값,...

다른 필드가 특정 값과 일치하면 검증 필드는 비어 있거나 존재하지 않아야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:다른필드,값,...

다른 필드가 특정 값과 일치하지 않으면 검증 필드는 비어 있거나 존재하지 않아야 합니다.

<a name="rule-prohibits"></a>
#### prohibits:다른필드,...

검증 필드가 존재하면 `prohibits`에 지정된 다른 필드는 비어 있거나 존재하지 않아야 합니다.

<a name="rule-regex"></a>
#### regex:_패턴_

검증 필드는 지정한 정규 표현식과 일치해야 합니다.

PHP `preg_match` 함수 규칙에 따라 패턴 지정이 필요하며, 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!NOTE]
> 패턴에 `|` 문자가 포함되면 배열 방식으로 규칙 지정이 권장됩니다.

<a name="rule-required"></a>
#### required

검증 필드는 입력 데이터에 존재해야 하며 비어 있으면 안 됩니다. "비어 있음"은 다음 조건 중 하나에 해당할 때입니다:

- 값이 `null`
- 빈 문자열
- 빈 배열 또는 `Countable` 객체
- 경로가 없는 업로드 파일

<a name="rule-required-if"></a>
#### required_if:다른필드,값,...

다른 필드가 지정 값 중 하나와 일치하면 검증 필드는 필수입니다.

더 복잡한 조건은 `Rule::requiredIf` 메서드를 써서 불리언이나 클로저를 전달할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf(function () use ($request) {
        return $request->user()->is_admin;
    }),
]);
```

<a name="rule-required-unless"></a>
#### required_unless:다른필드,값,...

다른 필드가 지정 값 중 하나가 아니라면 검증 필드는 필수입니다. 해당 다른 필드는 요청에 반드시 있어야 하며, 값이 `null`인 경우(`required_unless:name,null`) 기준 필드가 `null`이거나 없으면 제외됩니다.

<a name="rule-required-with"></a>
#### required_with:필드1,필드2,...

다른 지정 필드 중 하나라도 존재하고 비어 있지 않으면 검증 필드는 필수입니다.

<a name="rule-required-with-all"></a>
#### required_with_all:필드1,필드2,...

다른 지정 필드가 모두 존재하고 비어 있지 않으면 검증 필드는 필수입니다.

<a name="rule-required-without"></a>
#### required_without:필드1,필드2,...

다른 지정 필드 중 하나라도 비어 있거나 존재하지 않으면 검증 필드는 필수입니다.

<a name="rule-required-without-all"></a>
#### required_without_all:필드1,필드2,...

다른 지정 필드가 모두 비어 있거나 존재하지 않으면 검증 필드는 필수입니다.

<a name="rule-same"></a>
#### same:_필드_

검증 필드는 지정된 `_필드_`와 값이 같아야 합니다.

<a name="rule-size"></a>
#### size:_값_

검증 필드 크기가 지정된 `_값_`과 정확히 일치해야 합니다. 세부적인 평가 기준은 다음과 같습니다:

- 문자열: 문자 수
- 숫자: 정수 값 (`numeric` 또는 `integer` 규칙과 함께 사용)
- 배열: 배열 요소 개수
- 파일: 파일 크기(킬로바이트)

예시:

```php
'title' => 'size:12'; // 길이가 12인 문자열
'seats' => 'integer|size:10'; // 10인 정수
'tags' => 'array|size:5'; // 5개 요소 배열
'image' => 'file|size:512'; // 512KB 파일
```

<a name="rule-starts-with"></a>
#### starts_with:_값1_,_값2_,...

검증 필드는 주어진 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 필드는 문자열이어야 합니다. 이 필드가 `null`일 수도 있으면 `nullable` 규칙을 함께 지정하세요.

<a name="rule-timezone"></a>
#### timezone

검증 필드는 PHP `timezone_identifiers_list` 함수에서 반환하는 유효한 타임존 식별자여야 합니다.

<a name="rule-unique"></a>
#### unique:_테이블_,_컬럼_

검증 필드는 지정 테이블 내에서 유일해야 합니다.

**테이블 및 컬럼명 지정:**

테이블명 대신 Eloquent 모델명을 써서 테이블명을 결정할 수 있습니다:

```
'email' => 'unique:App\Models\User,email_address'
```

컬럼명을 지정하지 않으면 필드명이 컬럼명으로 사용됩니다:

```
'email' => 'unique:users,email_address'
```

**커스텀 데이터베이스 연결 지정:**

```
'email' => 'unique:connection.users,email_address'
```

**특정 ID 무시하기:**

업데이트 시 현재 모델 ID를 무시하려면 `Rule` 클래스를 사용합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```

> [!NOTE]
> `ignore` 메서드에 사용자의 입력 대신 시스템 생성된 식별자만 넘겨야 합니다. 그렇지 않으면 SQL 인젝션 위험이 있습니다.

### 모델 인스턴스 직접 지정하기:

```
Rule::unique('users')->ignore($user)
```

### 기본 PK 이름이 아닌 경우 컬럼명 지정:

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

### 컬럼명 변경:

```
Rule::unique('users', 'email_address')->ignore($user->id),
```

### 추가 조건 지정:

```
'email' => Rule::unique('users')->where(function ($query) {
    return $query->where('account_id', 1);
})
```

<a name="rule-url"></a>
#### url

검증 필드는 유효한 URL 문자열이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 필드는 RFC 4122(버전 1, 3, 4, 5)의 UUID여야 합니다.

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 검증 건너뛰기

특정 필드가 지정된 값이면 다른 필드를 검증하지 않으려면 `exclude_if` 규칙을 사용합니다. 예:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

또는 `exclude_unless`로 반대 조건을 지정할 수도 있습니다:

```
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 존재할 때만 검증하기

어떤 필드를 데이터 내에 존재할 때만 검증하고 싶으면 `sometimes` 규칙을 사용하세요:

```
$v = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예제에서 `email` 필드는 `$data` 배열에 있을 때만 검증됩니다.

> [!TIP]
> 항상 존재하지만 비어 있을 수 있는 필드를 검증할 때는 [선택적 필드 주의사항](#a-note-on-optional-fields)을 참고하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

예를 들어, 다른 필드가 100 이상일 때만 특정 필드를 필수로 지정하거나, 특정 필드가 존재할 때만 두 필드 값을 검증하는 등 복잡한 조건부 검증 구현이 가능합니다.

먼저 정적인 규칙만 포함해 `Validator` 인스턴스를 만듭니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);
```

100개 이상의 게임을 보유한 사용자는 이유를 입력하게 하려면 `sometimes` 메서드를 사용합니다:

```
$validator->sometimes('reason', 'required|max:500', function ($input) {
    return $input->games >= 100;
});
```

인자는 차례로, 조건부 검증할 필드명, 추가할 규칙, 조건 판단 함수입니다. 조건이 참이면 규칙이 추가됩니다.

여러 필드를 한꺼번에 조건부 검증할 수도 있습니다:

```
$validator->sometimes(['reason', 'cost'], 'required', function ($input) {
    return $input->games >= 100;
});
```

> [!TIP]
> 클로저의 `$input`은 `Illuminate\Support\Fluent` 인스턴스로, 입력값과 파일 모두 접근 가능합니다.

<a name="complex-conditional-array-validation"></a>
#### 배열 복잡한 조건부 검증

특정 배열 내 원소가 다른 원소에 따라 검증 규칙이 다를 때, 클로저가 두 번째 인자로 현재 원소를 받을 수도 있습니다:

```
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

$validator->sometimes('channels.*.address', 'email', function ($input, $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function ($input, $item) {
    return $item->type !== 'email';
});
```

`$item`은 배열일 경우 `Illuminate\Support\Fluent` 인스턴스이며, 배열이 아니면 문자열입니다.

<a name="validating-arrays"></a>
## 배열 검증하기

[`array` 검증 규칙](#rule-array)에서 살펴봤듯, 허용되는 배열 키 리스트를 지정할 수 있습니다. 지정되지 않은 키가 포함되면 검증 실패합니다:

```
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => 'array:username,locale',
]);
```

배열 내 허용 키를 구체적으로 지정하는 것이 이상적입니다. 지정하지 않으면 `validate`나 `validated` 호출 시 검증되지 않은 배열 키까지 반환해버립니다.

<a name="excluding-unvalidated-array-keys"></a>
### 검증하지 않은 배열 키 제외하기

필요하다면 `AppServiceProvider` `boot` 메서드에서 `<code>Validator::excludeUnvalidatedArrayKeys()</code>`를 호출해, 검증 규칙에 명지한 키만 검증 결과에 포함하도록 할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

/**
 * 애플리케이션 서비스 등록
 *
 * @return void
 */
public function boot()
{
    Validator::excludeUnvalidatedArrayKeys();
}
```

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 검증하기

중첩된 배열 형태 입력값 검증도 어렵지 않습니다. 점 표기법(dot notation)을 이용해 지정할 수 있습니다. 예를 들어 요청에 `photos[profile]` 필드가 있을 때:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

또한 배열 각 요소를 검증할 수도 있습니다. 예를 들어, 배열 내 각 이메일이 고유해야 한다면 다음과 같이:

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

언어 파일에 커스텀 메시지 작성 시에도 다음과 같이 `*`를 활용해 배열 필드에 하나의 메시지로 대응할 수 있습니다:

```
'custom' => [
    'person.*.email' => [
        'unique' => '각 사람은 고유한 이메일 주소를 가져야 합니다',
    ]
],
```

<a name="validating-passwords"></a>
## 비밀번호 검증하기

비밀번호 복잡도를 명확히 하기 위해 Laravel은 `Password` 규칙 객체를 제공합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 객체로 최소 길이, 문자, 숫자, 기호, 대소문자 혼용 등 복잡도를 쉽게 지정할 수 있습니다:

```php
// 최소 8자 필수...
Password::min(8)

// 최소 한 글자 이상 의무...
Password::min(8)->letters()

// 최소 각각 대문자와 소문자 필수...
Password::min(8)->mixedCase()

// 최소 숫자 한 개 이상 필수...
Password::min(8)->numbers()

// 최소 기호 한 개 이상 필수...
Password::min(8)->symbols()
```

또한, 공개된 비밀번호 유출 데이터베이스에 등록된 비밀번호인지 검증하려면 `uncompromised` 메서드를 사용하세요:

```
Password::min(8)->uncompromised()
```

내부적으로, `Password` 규칙은 [k-anonymity](https://en.wikipedia.org/wiki/K-anonymity) 모델을 활용해 [haveibeenpwned.com](https://haveibeenpwned.com)을 통한 비밀번호 유출 여부를 개인 정보 없이 판별합니다.

기본적으로, 데이터 유출에서 1회 이상 등장하면 손상된 것으로 간주합니다. 이는 `uncompromised` 메서드 첫 번째 인자로 검출 임계값을 지정해 조절할 수 있습니다:

```php
// 동일 유출 내 3회 미만으로만 존재해야 함...
Password::min(8)->uncompromised(3);
```

물론 위 규칙들을 체인으로 연결해 다 함께 적용할 수 있습니다:

```
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의하기

비밀번호 기본 검증 규칙을 한 곳에서 관리하려면 `Password::defaults` 메서드를 사용하세요. `defaults` 메서드는 클로저를 인자로 받으며, 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Validation\Rules\Password;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
                    ? $rule->mixedCase()->uncompromised()
                    : $rule;
    });
}
```

그 후, 검증 로직에서 기본 규칙을 적용할 때는 인자 없이 `defaults`를 호출하면 됩니다:

```
'password' => ['required', Password::defaults()],
```

기본 규칙에 추가 규칙을 붙이고 싶으면 `rules` 메서드를 활용하세요:

```
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 사용자 지정 검증 규칙

<a name="using-rule-objects"></a>
### 규칙 객체 사용하기

Laravel에는 유용한 검증 규칙이 많지만, 직접 커스텀 규칙을 정의할 수도 있습니다. 규칙 객체는 `make:rule` Artisan 명령어로 생성할 수 있습니다. 예를 들어 모든 문자가 대문자인지 확인하는 규칙을 만들어 봅시다. 규칙은 `app/Rules` 폴더에 생성됩니다:

```
php artisan make:rule Uppercase
```

규칙 객체는 두 메서드를 가집니다: `passes`와 `message`. `passes`는 속성명과 값이 들어오며 유효하면 `true`를 반환해야 합니다. `message`는 검증 실패 시 사용할 오류 메시지를 반환합니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class Uppercase implements Rule
{
    /**
     * 유효성 검사를 수행합니다.
     *
     * @param  string  $attribute
     * @param  mixed  $value
     * @return bool
     */
    public function passes($attribute, $value)
    {
        return strtoupper($value) === $value;
    }

    /**
     * 검증 오류 메시지를 반환합니다.
     *
     * @return string
     */
    public function message()
    {
        return 'The :attribute must be uppercase.';
    }
}
```

```php
/**
 * 검증 오류 메시지 반환
 *
 * @return string
 */
public function message()
{
    return trans('validation.uppercase');
}
```

이렇게 언어 파일을 통해 번역 메시지를 반환할 수도 있습니다.

정의된 규칙 객체는 밸리데이터 내 다른 규칙과 함께 인스턴스로 전달해 사용 가능합니다:

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 추가 데이터 접근하기

검증 대상 전체 데이터를 규칙 클래스가 접근해야 한다면, `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하세요. 이 인터페이스는 `setData` 메서드를 요구하며, 데이터를 전달할 때 호출됩니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;
use Illuminate\Contracts\Validation\DataAwareRule;

class Uppercase implements Rule, DataAwareRule
{
    /**
     * 검증 대상 전체 데이터
     *
     * @var array
     */
    protected $data = [];

    // ...

    /**
     * 검증 데이터를 설정합니다.
     *
     * @param  array  $data
     * @return $this
     */
    public function setData($data)
    {
        $this->data = $data;

        return $this;
    }
}
```

검증 인스턴스에 접근해야 하는 경우 `ValidatorAwareRule` 인터페이스를 구현하면 됩니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;

class Uppercase implements Rule, ValidatorAwareRule
{
    /**
     * 검증기 인스턴스
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * 현재 검증기를 설정합니다.
     *
     * @param  \Illuminate\Validation\Validator  $validator
     * @return $this
     */
    public function setValidator($validator)
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a name="using-closures"></a>
### 클로저 사용하기

일회성 커스텀 규칙이면 클로저로 정의할 수 있습니다. 클로저는 속성명, 값, 검증 실패 시 호출할 콜백 `$fail`을 인자로 받습니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function ($attribute, $value, $fail) {
            if ($value === 'foo') {
                $fail('The '.$attribute.' is invalid.');
            }
        },
    ],
]);
```

<a name="implicit-rules"></a>
### 암묵적 규칙

기본적으로 검증 필드가 없거나 빈 문자열이라면, 일반 규칙이나 커스텀 규칙이 호출되지 않습니다. 예를 들어, [`unique`](#rule-unique) 규칙은 빈 문자열에 대해 검증하지 않습니다:

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

필드가 없어도 규칙이 실행되게 하려면 `Illuminate\Contracts\Validation\ImplicitRule` 인터페이스를 구현하여 "암묵적" 규칙으로 만들어야 합니다. 이 인터페이스는 `Rule` 인터페이스를 확장하며 추가 메서드는 필요 없습니다.

암묵적 규칙 객체는 다음과 같이 생성할 수 있습니다:

```
 php artisan make:rule Uppercase --implicit
```

> [!NOTE]
> "암묵적" 규칙은 필드가 반드시 필요하다는 의미를 내포하지만, 실제로 필드가 없거나 비어 있을 때도 검증 실패시킬지는 규칙 로직에 따라 다릅니다.