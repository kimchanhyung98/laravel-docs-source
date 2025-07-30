# 검증 (Validation)

- [소개](#introduction)
- [검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [검증 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 다시 채우기](#repopulating-forms)
    - [선택적 필드에 관한 주의사항](#a-note-on-optional-fields)
    - [검증 오류 응답 형식](#validation-error-response-format)
- [폼 요청 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 승인하기](#authorizing-form-requests)
    - [오류 메시지 맞춤화하기](#customizing-the-error-messages)
    - [검증용 입력 준비하기](#preparing-input-for-validation)
- [수동으로 검증기 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [명명된 오류 묶음](#named-error-bags)
    - [오류 메시지 맞춤화하기](#manual-customizing-the-error-messages)
    - [검증 후 후크](#after-validation-hook)
- [검증된 입력 처리하기](#working-with-validated-input)
- [오류 메시지 처리하기](#working-with-error-messages)
    - [언어 파일에서 맞춤 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 검증하기](#validating-arrays)
    - [중첩된 배열 입력 검증하기](#validating-nested-array-input)
    - [오류 메시지의 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 검증하기](#validating-files)
- [비밀번호 검증](#validating-passwords)
- [커스텀 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [내재적(잠재적) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터를 검증하기 위한 여러 가지 방법을 제공합니다. 가장 일반적인 방법은 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용하는 것입니다. 하지만 다른 검증 방법들도 설명할 예정입니다.

Laravel은 다양한 편리한 검증 규칙을 포함하고 있으며, 특정 데이터가 데이터베이스 테이블에 고유한지 검증하는 기능도 제공합니다. 모든 검증 규칙을 자세히 살펴보며 Laravel 검증 기능을 완전히 익힐 수 있도록 하겠습니다.

<a name="validation-quickstart"></a>
## 검증 빠른 시작

Laravel의 강력한 검증 기능을 이해하려면, 폼을 검증하고 에러 메시지를 사용자에게 다시 보여주는 완전한 예제를 살펴보는 것이 가장 좋습니다. 이 개요를 통해 Laravel로 요청 데이터를 검증하는 기본적인 흐름을 쉽게 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, 다음과 같은 라우트가 `routes/web.php` 파일에 정의되어 있다고 가정합니다:

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 게시물을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

이제 이 라우트에 대한 요청을 처리하는 간단한 컨트롤러를 살펴봅니다. `store` 메서드는 아직 비워둡니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물 작성 폼을 보여줍니다.
     *
     * @return \Illuminate\View\View
     */
    public function create()
    {
        return view('post.create');
    }

    /**
     * 새 블로그 게시물을 저장합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // 블로그 게시물 검증 및 저장...
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 검증 로직 작성하기

이제 `store` 메서드를 채워서 새 게시물을 검증하는 로직을 추가할 준비가 되었습니다. `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 검증 규칙을 통과하면 코드가 정상적으로 계속 실행됩니다. 하지만 실패하면 `Illuminate\Validation\ValidationException` 예외가 던져지고 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청의 경우, 검증 실패 시 이전 URL로 리다이렉트 응답이 생성됩니다. 만약 요청이 XHR이라면, [검증 오류 메시지를 포함한 JSON 응답](#validation-error-response-format)을 반환합니다.

`validate` 메서드 사용법을 이해하기 위해 다시 `store` 메서드를 봅시다:

```
/**
 * 새 블로그 게시물을 저장합니다.
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

    // 블로그 게시물 검증 완료...
}
```

보시다시피, `validate` 메서드에 검증 규칙을 전달합니다. 걱정하지 마세요 — 사용 가능한 모든 검증 규칙은 [문서](#available-validation-rules)에 정리되어 있습니다. 또한, 검증 실패하면 적절한 응답이 자동으로 생성됩니다. 검증 통과 시 컨트롤러가 정상적으로 계속 실행됩니다.

규칙은 `|`로 구분된 문자열 대신 배열 형태로도 지정할 수 있습니다:

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

추가로, `validateWithBag` 메서드를 사용해 검증하고, 오류 메시지를 [명명된 오류 묶음](#named-error-bags)에 저장할 수 있습니다:

```
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단하기

때로는 첫 번째 검증 실패 후 추가 검사를 중단하고 싶을 수 있습니다. 이때는 `bail` 규칙을 속성에 할당하면 됩니다:

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예에서는 `title` 속성의 `unique` 규칙이 실패하면, 뒤따르는 `max` 규칙은 검사되지 않습니다. 규칙은 작성된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 관한 주의사항

만약 요청 데이터에 "중첩" 필드가 들어온다면, 검증 규칙에서 "닷(dot) 표기법"을 사용해 지정할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 마침표가 포함되어 있다면 백슬래시(`\`)로 이스케이프하여 닷 표기법 해석을 막을 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 검증 오류 표시하기

만약 검증 규칙을 통과하지 못했다면 어떻게 될까요? 앞서 설명했듯 Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 게다가 모든 검증 오류와 [요청 입력 값](/docs/9.x/requests#retrieving-old-input)은 자동으로 세션에 [플래시(flash)됩니다](/docs/9.x/session#flash-data).

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어 덕분에 `$errors` 변수가 모든 뷰에 공유됩니다. 이 미들웨어는 `web` 미들웨어 그룹에서 제공됩니다. 따라서 언제나 뷰에서 `$errors` 변수를 안전하게 사용할 수 있습니다. `$errors`는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체에 대해 더 알고 싶으면 [오류 메시지 조작 섹션](#working-with-error-messages)을 참조하세요.

즉, 예제를 기준으로 하면, 사용자는 검증 실패 시 컨트롤러의 `create` 메서드로 리다이렉트되고, 뷰에서 아래처럼 오류 메시지를 표시할 수 있습니다:

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
#### 오류 메시지 맞춤화하기

Laravel 내장 검증 규칙은 각각 애플리케이션의 `lang/en/validation.php` 파일에 오류 메시지를 갖고 있습니다. 이 파일에서 각 검증 규칙에 대응하는 번역 항목을 볼 수 있으며, 필요에 맞게 자유롭게 수정할 수 있습니다.

또한 이 파일을 복사해 다른 언어 디렉터리에 넣어 애플리케이션 언어에 맞게 메시지를 번역할 수 있습니다. Laravel 다국어 지원에 관해서는 [로컬라이제이션 문서](/docs/9.x/localization)를 참고하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 검증

이 예제에서는 전통적인 폼을 사용해 데이터를 전송했습니다. 그러나 많은 애플리케이션은 JavaScript 프론트엔드에서 XHR 요청을 받습니다. 이런 경우 `validate` 메서드가 호출되면 Laravel은 리다이렉션 응답을 생성하지 않고, [검증 오류 메시지를 포함하는 JSON 응답](#validation-error-response-format)을 422 상태 코드와 함께 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

`@error` Blade 디렉티브를 사용하면 특정 속성의 검증 오류 메시지 존재 여부를 쉽게 확인할 수 있습니다. `@error` 내에서는 `$message` 변수를 출력해 오류 메시지를 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">게시물 제목</label>

<input id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

명명된 오류 묶음(named error bags)을 사용한다면, `@error`의 두 번째 인자로 오류 묶음 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 다시 채우기

검증 오류로 리다이렉션할 때, Laravel은 요청된 모든 입력 값을 자동으로 [세션에 플래시(flash)](/docs/9.x/session#flash-data)합니다. 이 덕분에 다음 요청에서 플래시된 입력 데이터를 가져와 사용자가 제출했던 폼을 손쉽게 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력을 꺼내려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. `old` 메서드는 플래시된 데이터를 세션에서 가져옵니다:

```
$title = $request->old('title');
```

Blade 템플릿에서는 전역 `old` 헬퍼를 사용해 입력값을 채우는 것이 더욱 편리합니다. 해당 필드에 예전 입력값이 없으면 `null`을 반환합니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 관한 주의사항

Laravel은 기본적으로 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이는 `App\Http\Kernel` 클래스에 나열됩니다. 따라서 선택적인 필드가 `null` 값을 가질 수 있도록 하려면 보통 `nullable` 규칙을 명시해야 검증기에서 `null`이 유효하지 않은 값으로 간주되는 것을 방지할 수 있습니다. 예:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

`publish_at` 필드는 `null` 또는 유효한 날짜 형식이어야 한다는 뜻입니다. `nullable` 규칙이 없으면 `null` 값은 잘못된 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 검증 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대할 때 Laravel은 오류 메시지를 자동으로 포맷해 `422 Unprocessable Entity` 상태 코드와 함께 반환합니다.

다음은 검증 오류에 대한 JSON 응답 예시입니다. 중첩된 오류 키는 "닷(dot)" 표기법으로 평탄화(flatten) 됩니다:

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
## 폼 요청 검증

<a name="creating-form-requests"></a>
### 폼 요청 생성하기

복잡한 검증 시나리오에서는 별도의 "폼 요청(Form Request)" 클래스를 만들 수도 있습니다. 폼 요청은 검증과 인가 로직을 캡슐화하는 커스텀 요청 클래스입니다. 생성하려면 `make:request` Artisan 명령어를 사용하세요:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 해당 디렉터리가 없으면 명령어 실행 시 자동 생성됩니다. 생성된 폼 요청은 `authorize`와 `rules` 두 메서드를 포함합니다.

`authorize` 메서드는 현재 인증된 사용자가 요청 행위를 수행할 권한이 있는지 판단하며, `rules`는 요청 데이터에 적용할 검증 규칙을 반환합니다:

```
/**
 * 이 요청에 적용할 검증 규칙을 반환합니다.
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

> [!NOTE]
> `rules` 메서드 매개변수에 필요한 의존성을 타입힌팅하면 Laravel [서비스 컨테이너](/docs/9.x/container)를 통해 자동으로 주입됩니다.

검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드의 인수로 해당 폼 요청 타입힌트를 지정하기만 하면 됩니다. 컨트롤러가 호출되기 전에 폼 요청에 대해 검증이 수행되어, 컨트롤러 내부에 검증 로직을 추가할 필요가 없습니다:

```
/**
 * 새 블로그 게시물을 저장합니다.
 *
 * @param  \App\Http\Requests\StorePostRequest  $request
 * @return Illuminate\Http\Response
 */
public function store(StorePostRequest $request)
{
    // 요청 데이터는 유효합니다...

    // 검증된 입력 데이터 획득...
    $validated = $request->validated();

    // 검증된 데이터의 일부만 획득...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);
}
```

검증 실패 시 오류는 세션에 플래시되고, 이전 위치로 리다이렉트됩니다. XHR 요청이라면 422 상태 코드 및 [JSON 오류 표현]을 포함한 응답이 반환됩니다.

<a name="adding-after-hooks-to-form-requests"></a>
#### 폼 요청에 "검증 후" 후크 추가하기

폼 요청에 "검증 후" 실행할 후크를 추가하려면 `withValidator` 메서드를 사용하세요. 이 메서드는 완성된 검증기 인스턴스를 받은 후, 실제 검증 규칙 평가 전에 추가 작업을 수행할 수 있도록 해줍니다:

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
#### 첫 번째 실패 시 전체 중단 속성

요청 클래스에 `stopOnFirstFailure` 속성을 추가하면, 하나라도 검증 실패가 발생할 때 모든 속성에 대한 검증을 중단하도록 검증기에 알릴 수 있습니다:

```
/**
 * 검증 규칙 중 첫 번째 실패 시 중단할지 여부
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 맞춤화

기본적으로 폼 요청 검증 실패 시 이전 URL로 리다이렉트됩니다. 만약 리다이렉트 위치를 변경하고 싶다면, 폼 요청 클래스에 `$redirect` 속성을 정의하세요:

```
/**
 * 검증 실패 시 사용자를 리다이렉트할 URI
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는 이름 있는 라우트로 리다이렉트하려면 `$redirectRoute` 속성을 정의할 수 있습니다:

```
/**
 * 검증 실패 시 리다이렉트할 라우트 이름
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 승인하기

폼 요청 클래스의 `authorize` 메서드에서 인증된 사용자가 리소스를 수정할 권한이 있는지 검증할 수 있습니다. 예를 들어, 사용자가 수정하려는 블로그 댓글의 소유자인지 판단할 수 있습니다. 보통 이 메서드 안에서 [인가 게이트 및 정책](/docs/9.x/authorization)을 호출합니다:

```
use App\Models\Comment;

/**
 * 요청을 승인할 권한이 있는지 판단합니다.
 *
 * @return bool
 */
public function authorize()
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 요청은 기본 Laravel 요청 클래스를 상속하므로, 현재 인증된 사용자를 `user` 메서드로 가져올 수 있습니다. 위 예제에선 `route` 메서드 호출로 라우트 매개변수인 `{comment}` 값을 얻고 있습니다:

```
Route::post('/comment/{comment}');
```

[라우트 모델 바인딩](/docs/9.x/routing#route-model-binding)을 활용하면, resolved 된 모델을 요청 클래스의 속성으로 바로 접근할 수 있어 더 간결합니다:

```
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면 403 상태 응답이 자동 반환되고 컨트롤러는 실행되지 않습니다.

다른 곳에서 인가 로직을 처리할 계획이라면 단순히 `true`를 반환해 무조건 승인 처리할 수 있습니다:

```
/**
 * 요청을 승인할 권한이 있는지 판단합니다.
 *
 * @return bool
 */
public function authorize()
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 내 필요한 의존성을 타입힌팅하면 Laravel [서비스 컨테이너](/docs/9.x/container)에서 자동으로 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 맞춤화하기

폼 요청에서 사용하는 오류 메시지를 맞춤화하려면 `messages` 메서드를 재정의하세요. 이 메서드는 속성/규칙 쌍과 오류 메시지 배열을 반환해야 합니다:

```
/**
 * 정의한 검증 규칙에 대한 오류 메시지를 반환합니다.
 *
 * @return array
 */
public function messages()
{
    return [
        'title.required' => '제목은 필수입니다.',
        'body.required' => '본문은 필수입니다.',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 검증 속성 맞춤화하기

Laravel 내장 검증 오류 메시지에는 보통 `:attribute` 자리표시자가 포함됩니다. 이를 원하는 이름으로 변경하려면 `attributes` 메서드를 재정의해 속성명과 사용자 친화적 이름을 맵핑하세요:

```
/**
 * 검증 오류용 속성명을 반환합니다.
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
### 검증용 입력 준비하기

검증 규칙을 적용하기 전에 요청 데이터의 가공이나 정제가 필요하다면 `prepareForValidation` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Str;

/**
 * 검증을 위한 데이터 준비 작업을 수행합니다.
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

반대로 검증 완료 후 데이터를 정규화하고자 할 경우 `passedValidation` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Str;

/**
 * 검증 성공 후 처리를 수행합니다.
 *
 * @return void
 */
protected function passedValidation()
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 검증기 생성하기

`validate` 메서드를 사용하지 않고 직접 검증기 인스턴스를 생성하려면 `Validator` [파사드](/docs/9.x/facades)의 `make` 메서드를 사용할 수 있습니다. `make`는 새로운 검증기 인스턴스를 생성합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물을 저장합니다.
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

        // 검증된 입력 데이터 획득...
        $validated = $validator->validated();

        // 검증된 입력 일부만 획득...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 게시물 저장...
    }
}
```

첫 번째 인자는 검증할 데이터이고, 두 번째 인자는 그 데이터에 적용할 규칙 배열입니다.

검증 실패 여부를 판단한 뒤 `withErrors` 메서드로 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드 사용 시 리다이렉션 후 뷰에서 `$errors` 변수가 자동으로 공유되어 사용자가 쉽게 오류를 확인할 수 있습니다. `withErrors`는 검증기, `MessageBag`, 혹은 PHP 배열도 받을 수 있습니다.

#### 첫 번째 검증 실패 시 중단하기

`stopOnFirstFailure` 메서드를 호출하면 하나라도 검증 실패가 발생하는 순간 전체 필드 검증을 중단하도록 설정할 수 있습니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

수동으로 검증기를 생성해 쓰면서도 HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 활용하고 싶다면 검증기 인스턴스에 `validate` 메서드를 호출하세요. 검증 실패 시 자동으로 이전 페이지로 리다이렉션하거나, XHR 요청 시 [JSON 오류 응답](#validation-error-response-format)을 반환합니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드를 호출해 명명된 오류 묶음에 저장할 수도 있습니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 명명된 오류 묶음

한 페이지에 여러 폼이 있을 때는 검증 오류 메시지들을 구분하기 위해 오류 묶음에 이름을 부여할 수 있습니다. 이를 위해 `withErrors` 두 번째 인자에 오류 묶음 이름을 전달하세요:

```
return redirect('register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수에서 아래처럼 접근할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 맞춤화하기

검증기 인스턴스에 기본 Laravel 오류 메시지 대신 커스텀 메시지를 지정할 수 있습니다. 여러 방법이 있지만, 우선 `Validator::make` 세 번째 인자로 메시지 배열을 전달할 수 있습니다:

```
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

`:attribute` 자리표시자는 검증 대상 필드명으로 치환됩니다. 그 밖에 여러 자리표시자를 활용할 수 있습니다:

```
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성만 커스텀 메시지 지정하기

가끔 특정 필드에 한해서만 커스텀 메시지를 지정하고 싶을 수 있습니다. 이런 경우 "닷(dot)" 표기법으로 메시지 키를 작성하세요:

```
$messages = [
    'email.required' => '이메일 주소를 알려주세요!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정하기

Laravel 기본 오류 메시지에서는 `:attribute` 가 실제 필드명으로 치환됩니다. 이를 특정 필드에 대해 친근한 이름으로 바꾸려면, `Validator::make` 네 번째 인자로 속성명 배열을 전달하세요:

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="after-validation-hook"></a>
### 검증 후 후크

검증 완료 후 추가 유효성 검사나 오류 메시지 추가가 필요하면 검증기에 콜백을 붙일 수 있습니다. `after` 메서드를 호출해 시작합니다:

```
$validator = Validator::make(/* ... */);

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
## 검증된 입력 처리하기

폼 요청이나 수동 검증기를 사용해 검증 후, 실제 검증된 입력 데이터를 얻고 싶을 때가 있습니다.

우선 `validated` 메서드를 호출하면 검증을 통과한 데이터를 배열로 반환합니다:

```
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스가 반환되며, 여기서 `only`, `except`, `all` 메서드로 부분적으로 또는 전체를 얻을 수 있습니다:

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

`ValidatedInput` 객체는 배열처럼 반복(iterate)하거나 배열 방식으로 접근할 수도 있습니다:

```
// 반복 처리 가능
foreach ($request->safe() as $key => $value) {
    //
}

// 배열처럼 접근 가능
$validated = $request->safe();

$email = $validated['email'];
```

추가 필드를 합치고 싶으면 `merge` 메서드를 사용하세요:

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/9.x/collections) 형태로 얻으려면 `collect` 메서드를 호출하면 됩니다:

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 처리하기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 객체를 반환하는데, 이 객체는 오류 메시지 조작을 위한 여러 메서드를 제공합니다. 앞서 설명한 자동 공유된 `$errors` 변수도 `MessageBag` 클래스 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 오류 메시지 가져오기

필드에 대한 첫 번째 오류 메시지를 얻으려면 `first` 메서드를 사용하세요:

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

필드에 대한 모든 오류 메시지 배열을 얻으려면 `get` 메서드를 사용합니다:

```
foreach ($errors->get('email') as $message) {
    //
}
```

배열 필드를 검증할 때는 `*` 와일드카드를 사용해 모든 배열 요소 오류를 가져올 수 있습니다:

```
foreach ($errors->get('attachments.*') as $message) {
    //
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 가져오기

모든 오류 메시지를 배열로 받으려면 `all` 메서드를 사용하세요:

```
foreach ($errors->all() as $message) {
    //
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 메시지 존재 여부 확인하기

필드에 오류 메시지가 하나라도 있으면 `has` 메서드가 `true`를 반환합니다:

```
if ($errors->has('email')) {
    //
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 맞춤 메시지 지정하기

Laravel 내장 검증 규칙마다 `lang/en/validation.php` 파일에 해당하는 기본 오류 메시지가 있습니다. 필요에 따라 이 메시지들을 수정할 수 있습니다.

다른 언어로 번역하고 싶으면 이 파일을 해당하는 언어 폴더에 복사하여 수정하면 됩니다. 다국어 지원에 관한 자세한 내용은 [로컬라이제이션 문서](/docs/9.x/localization)를 참고하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성과 규칙에 맞춘 커스텀 메시지

애플리케이션 언어 파일 내 `custom` 배열에 속성별 규칙 조합에 대한 커스텀 메시지를 추가할 수 있습니다:

```
'custom' => [
    'email' => [
        'required' => '이메일 주소를 알려주세요!',
        'max' => '이메일 주소가 너무 깁니다!',
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 이름 지정하기

Laravel 기본 오류 메시지에 포함된 `:attribute` 자리표시자를 원하는 이름으로 변경하려면 `attributes` 배열에 매핑하세요:

```
'attributes' => [
    'email' => '이메일 주소',
],
```

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 검증 규칙 메시지는 `:value` 자리표시자를 포함하는데, 요청 값 대신 사용자 친화적인 값으로 바꾸고 싶을 때가 있습니다. 예를 들어 `payment_type` 필드가 `cc`일 때 `credit_card_number` 필드가 필수인 규칙에서:

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

검증 실패 시 기본 메시지는 다음과 같습니다:

```none
The credit card number field is required when payment type is cc.
```

`cc` 대신 친숙한 명칭을 사용하고 싶다면 `lang/xx/validation.php`의 `values` 배열에 아래처럼 정의하세요:

```
'values' => [
    'payment_type' => [
        'cc' => '신용카드',
    ],
],
```

이제 메시지는 다음과 같이 나옵니다:

```none
The credit card number field is required when payment type is 신용카드.
```

<a name="available-validation-rules"></a>
## 사용 가능한 검증 규칙

아래는 Laravel에서 제공하는 모든 검증 규칙과 그 설명입니다:

<div class="collection-method-list" markdown="1">

[accepted](#rule-accepted)
[accepted_if](#rule-accepted-if)
[active_url](#rule-active-url)
[after (Date)](#rule-after)
[after_or_equal (Date)](#rule-after-or-equal)
[alpha](#rule-alpha)
[alpha_dash](#rule-alpha-dash)
[alpha_num](#rule-alpha-num)
[array](#rule-array)
[ascii](#rule-ascii)
[bail](#rule-bail)
[before (Date)](#rule-before)
[before_or_equal (Date)](#rule-before-or-equal)
[between](#rule-between)
[boolean](#rule-boolean)
[confirmed](#rule-confirmed)
[current_password](#rule-current-password)
[date](#rule-date)
[date_equals](#rule-date-equals)
[date_format](#rule-date-format)
[decimal](#rule-decimal)
[declined](#rule-declined)
[declined_if](#rule-declined-if)
[different](#rule-different)
[digits](#rule-digits)
[digits_between](#rule-digits-between)
[dimensions (Image Files)](#rule-dimensions)
[distinct](#rule-distinct)
[doesnt_start_with](#rule-doesnt-start-with)
[doesnt_end_with](#rule-doesnt-end-with)
[email](#rule-email)
[ends_with](#rule-ends-with)
[enum](#rule-enum)
[exclude](#rule-exclude)
[exclude_if](#rule-exclude-if)
[exclude_unless](#rule-exclude-unless)
[exclude_with](#rule-exclude-with)
[exclude_without](#rule-exclude-without)
[exists (Database)](#rule-exists)
[file](#rule-file)
[filled](#rule-filled)
[gt](#rule-gt)
[gte](#rule-gte)
[image (File)](#rule-image)
[in](#rule-in)
[in_array](#rule-in-array)
[integer](#rule-integer)
[ip](#rule-ip)
[json](#rule-json)
[lt](#rule-lt)
[lte](#rule-lte)
[lowercase](#rule-lowercase)
[mac_address](#rule-mac)
[max](#rule-max)
[max_digits](#rule-max-digits)
[mimetypes](#rule-mimetypes)
[mimes](#rule-mimes)
[min](#rule-min)
[min_digits](#rule-min-digits)
[missing](#rule-missing)
[missing_if](#rule-missing-if)
[missing_unless](#rule-missing-unless)
[missing_with](#rule-missing-with)
[missing_with_all](#rule-missing-with-all)
[multiple_of](#rule-multiple-of)
[not_in](#rule-not-in)
[not_regex](#rule-not-regex)
[nullable](#rule-nullable)
[numeric](#rule-numeric)
[password](#rule-password)
[present](#rule-present)
[prohibited](#rule-prohibited)
[prohibited_if](#rule-prohibited-if)
[prohibited_unless](#rule-prohibited-unless)
[prohibits](#rule-prohibits)
[regex](#rule-regex)
[required](#rule-required)
[required_if](#rule-required-if)
[required_unless](#rule-required-unless)
[required_with](#rule-required-with)
[required_with_all](#rule-required-with-all)
[required_without](#rule-required-without)
[required_without_all](#rule-required-without-all)
[required_array_keys](#rule-required-array-keys)
[same](#rule-same)
[size](#rule-size)
[sometimes](#validating-when-present)
[starts_with](#rule-starts-with)
[string](#rule-string)
[timezone](#rule-timezone)
[unique (Database)](#rule-unique)
[uppercase](#rule-uppercase)
[url](#rule-url)
[ulid](#rule-ulid)
[uuid](#rule-uuid)

</div>

<a name="rule-accepted"></a>
#### accepted

검증 대상 필드는 `"yes"`, `"on"`, `1`, 혹은 `true` 중 하나여야 합니다. 예를 들어 '이용 약관 동의' 등을 검증할 때 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

검증 대상 필드는 다른 필드가 특정 값일 때 `"yes"`, `"on"`, `1`, 혹은 `true` 중 하나여야 합니다. '동의 필드가 특정 조건일 때만 필수' 같은 경우에 유용합니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드는 `dns_get_record` PHP 함수가 유효하다고 판단하는 A 또는 AAAA DNS 레코드를 가져야 합니다. URL 호스트명은 `parse_url`로 추출합니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드는 주어진 날짜보다 이후여야 합니다. 날짜는 `strtotime` 함수로 `DateTime` 인스턴스화됩니다:

```
'start_date' => 'required|date|after:tomorrow'
```

날짜 문자열 대신 다른 필드 값을 기준으로 지정할 수도 있습니다:

```
'finish_date' => 'required|date|after:start_date'
```

<a name="rule-after-or-equal"></a>
#### after_or_equal:_date_

검증 대상 필드는 주어진 날짜와 같거나 이후여야 합니다. 자세한 내용은 [after](#rule-after) 규칙 참조.

<a name="rule-alpha"></a>
#### alpha

검증 대상 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=)와 [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 해당하는 유니코드 문자로만 이루어져야 합니다.

ASCII 문자 범위(`a-z`, `A-Z`)로 제한하려면 `ascii` 옵션을 규칙에 추가하세요:

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 대상 필드는 유니코드 알파벳 대소문자(`\p{L}`, `\p{M}`, `\p{N}`), ASCII 대시(`-`), 언더스코어(`_`)만 포함해야 합니다.

ASCII 범위로 제한하려면 `ascii` 옵션을 추가하세요:

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증 대상 필드는 유니코드 알파벳 문자와 숫자(`\p{L}`, `\p{M}`, `\p{N}`)만 포함해야 합니다.

ASCII 범위로 제한하려면 `ascii` 옵션을 추가하세요:

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 대상 필드는 PHP 배열이어야 합니다.

`array` 규칙의 인수로 키 목록을 지정하면, 배열의 키가 지정한 목록 안에 있어야 유효합니다. 예:

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
    'user' => 'array:name,username',
]);
```

위 예에서 `admin` 키는 명시되지 않아 검증에 실패합니다.

일반적으로 허용할 배열 키 목록을 명시하는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

검증 대상 필드는 7비트 ASCII 문자로만 이루어져야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드 검증 실패 시 그 즉시 해당 필드의 추가 규칙 검증을 중단합니다.

`bail`은 특정 필드만 해당하는 반면, `stopOnFirstFailure`는 전체 필드 중 첫 실패 시 모든 검증을 중지시킵니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 대상 필드는 주어진 날짜 이전이어야 합니다. 날짜는 `strtotime` 변환됩니다. `after` 규칙과 같이 다른 필드를 날짜 기준으로 지정할 수도 있습니다.

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 대상 필드는 주어진 날짜와 같거나 이전이어야 합니다. `before` 규칙의 추가 변형입니다.

<a name="rule-between"></a>
#### between:_min_,_max_

검증 대상 필드 크기가 최소 _min_ 과 최대 _max_ (포함) 사이여야 합니다. 문자열, 수치, 배열, 파일 크기 모두 [`size`](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

검증 대상 필드는 boolean으로 캐스팅할 수 있어야 하며, 허용 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드는 `{field}_confirmation`이라는 이름의 필드와 일치해야 합니다. 예: `password` 검증 시 `password_confirmation` 필드가 있어야 합니다.

<a name="rule-current-password"></a>
#### current_password

검증 대상 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 첫 번째 인자로 인증 가드를 지정할 수 있습니다:

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 대상 필드는 `strtotime` 함수가 올바른 날짜로 해석하는 유효한 비상대 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 대상 필드는 주어진 날짜와 정확히 일치해야 합니다. 날짜는 `strtotime`으로 변환합니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 대상 필드는 지정한 하나 이상의 날짜 형식 중 하나와 일치해야 합니다. `date` 또는 `date_format` 중 하나만 사용해야 하며, PHP `DateTime` 클래스가 지원하는 포맷을 사용할 수 있습니다.

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

검증 대상 필드는 숫자형이어야 하며 소수점 자릿수가 지정된 수여야 합니다:

```
// 정확히 소수점 이하 2자리 (예: 9.99)
'price' => 'decimal:2'

// 소수점 이하 2~4자리
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 대상 필드는 `"no"`, `"off"`, `0`, `false` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

검증 대상 필드는 다른 필드가 특정 값일 때 `"no"`, `"off"`, `0`, `false` 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드 값이 지정 필드와 달라야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수의 길이가 정확히 _value_ 자리여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 대상 정수 길이가 _min_ 이상 _max_ 이하이어야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일이 이미지이며 규칙에 명시된 치수 조건을 만족해야 합니다:

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

지원하는 제약조건: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_.

`ratio`는 너비/높이 비율로, `3/2` 같은 분수 또는 실수 `1.5` 형태로 지정할 수 있습니다:

```
'avatar' => 'dimensions:ratio=3/2'
```

`Rule::dimensions` 메서드로 좀더 손쉽게 작성할 수도 있습니다:

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

배열 검증 시, 중복된 값을 허용하지 않습니다:

```
'foo.*.id' => 'distinct'
```

기본적으로 PHP 느슨한 비교를 사용하며, 엄격한 비교를 원하면 `strict` 옵션을 추가하세요:

```
'foo.*.id' => 'distinct:strict'
```

대소문자 차이를 무시하려면 `ignore_case` 옵션을 추가합니다:

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

필드는 지정한 값들 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

필드는 지정한 값들 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

필드는 이메일 주소 형식이어야 합니다. 이 검증은 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본값은 `RFCValidation`이지만 다른 검증 옵션도 지정할 수 있습니다:

```
'email' => 'email:rfc,dns'
```

검증 옵션 목록:

- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`
- `filter_unicode`: `FilterEmailValidation::unicode()`

`filter`는 PHP `filter_var` 함수 기반이며 Laravel 5.8 이전 기본 이메일 검증 방법입니다.

> [!WARNING]
> `dns` 와 `spoof` 옵션 사용 시 PHP `intl` 확장 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

필드는 지정한 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

클래스 기반 규칙으로, 필드가 유효한 PHP 8.1+ [enum](https://www.php.net/manual/en/language.enumerations.php) 값인지 검증합니다. 예:

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rules\Enum;

$request->validate([
    'status' => [new Enum(ServerStatus::class)],
]);
```

> [!WARNING]
> enum은 PHP 8.1 이상에서만 지원됩니다.

<a name="rule-exclude"></a>
#### exclude

검증 대상 필드를 `validate` 및 `validated` 메서드 결과에서 제외합니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

다른 필드가 특정 값인 경우, 검증 대상 필드를 결과에서 제외합니다.

복잡한 조건이 필요하면 `Rule::excludeIf` 메서드에 불린 혹은 클로저를 전달하세요:

```
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

다른 필드가 특정 값과 같지 않으면 검증 대상에서 제외합니다. 만약 값이 `null`이면 비교 필드가 `null`이거나 없을 때 제외됩니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

다른 필드가 존재하면 검증 대상 필드를 제외합니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

다른 필드가 없으면 검증 대상 필드를 제외합니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 대상 값이 지정한 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 기본 사용법

```
'state' => 'exists:states'
```

열 이름 지정이 없으면 필드명이 열 이름이 됩니다. 위 예는 `states` 테이블에 `state` 열 값이 존재하는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 지정 열 이름 지정하기

테이블명 뒤에 열을 명시해 열 이름을 직접 지정할 수 있습니다:

```
'state' => 'exists:states,abbreviation'
```

특정 데이터베이스 연결을 지정할 수도 있습니다:

```
'email' => 'exists:connection.staff,email'
```

Eloquent 모델명을 직접 지정해 테이블명을 결정할 수도 있습니다:

```
'user_id' => 'exists:App\Models\User,id'
```

쿼리 조건을 맞춤화하려면 `Rule::exists` 메서드를 이용하세요:

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

`Rule::exists` 메서드 두 번째 인자로 열 이름을 지정할 수 있습니다:

```
'state' => Rule::exists('states', 'abbreviation'),
```

<a name="rule-file"></a>
#### file

검증 대상 필드는 성공적으로 업로드 된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

필드가 존재할 때 비어있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 필드 값이 지정 필드 값보다 커야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 필드 값이 지정 필드 값과 같거나 커야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지여야 하며, 파일 형식은 jpg, jpeg, png, bmp, gif, svg, webp 중 하나여야 합니다.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 대상 값이 지정한 값 목록에 포함되어야 합니다. 배열로 값을 전달하고 싶다면 `Rule::in` 메서드를 활용하세요:

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

`in` 규칙과 `array` 규칙을 함께 쓰면 배열 각 원소가 지정한 값 목록에 있어야 합니다:

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
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```

위 예에서는 `LAS` 원소가 목록에 없어 검증에 실패합니다.

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

값이 다른 배열 필드 값 중 하나에 포함되어야 합니다.

<a name="rule-integer"></a>
#### integer

필드는 정수여야 합니다.

> [!WARNING]
> 변수 타입이 정수인지가 아니라 PHP `FILTER_VALIDATE_INT`가 통과할만한 값인지 검사합니다. 숫자인지 확실히 하려면 [`numeric`](#rule-numeric) 규칙과 함께 사용하세요.

<a name="rule-ip"></a>
#### ip

필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

필드 값이 지정 필드 값보다 작아야 합니다. 같은 타입이어야 하며, [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

필드 값이 지정 필드 값과 같거나 작아야 합니다.

<a name="rule-lowercase"></a>
#### lowercase

필드는 모두 소문자여야 합니다.

<a name="rule-mac"></a>
#### mac_address

필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

필드 값이 최대 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

정수 길이가 최대 _value_ 자리여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 대상 파일이 지정 MIME 타입 중 하나여야 합니다:

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

파일 내용으로 MIME 타입을 판별하며, 클라이언트 제공 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

파일이 지정 확장자에 대응하는 MIME 타입이어야 합니다.

<a name="basic-usage-of-mime-rule"></a>
#### mimes 기본 사용법

```
'photo' => 'mimes:jpg,bmp,png'
```

확장자를 지정할 뿐이지만, 파일 내용을 읽어 MIME 타입을 추측해 검증합니다. MIME 타입과 확장자 정보는 다음 위치 참고:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_value_

필드 값이 최소 _value_ 이상이어야 합니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

정수 길이가 최소 _value_ 자리여야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

필드 값이 _value_ 의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

필드가 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

다른 필드가 지정 값일 경우, 검증 필드는 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

다른 필드가 지정 값이 아니면 검증 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

다른 지정 필드 중 하나라도 존재하면 검증 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

다른 지정 필드가 모두 존재하면 검증 필드는 없어야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

필드 값이 지정된 값 목록에 포함되어서는 안 됩니다. `Rule::notIn`으로도 작성할 수 있습니다:

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
#### not_regex:_pattern_

필드 값이 지정 정규식과 매칭되지 않아야 합니다.

PHP `preg_match` 형식을 따라야 하며 구분자 필요:

예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` 및 `not_regex`를 배열 규칙으로 작성하는 것이 좋습니다, 특히 패턴에 `|` 문자가 포함될 때.

<a name="rule-nullable"></a>
#### nullable

필드가 `null` 값을 허용합니다.

<a name="rule-numeric"></a>
#### numeric

필드가 숫자여야 합니다.

<a name="rule-password"></a>
#### password

필드가 인증된 사용자의 비밀번호여야 합니다.

> [!WARNING]
> 이 규칙은 Laravel 9에서 `current_password`로 이름이 변경되었으며, 앞으로 제거될 예정입니다. 대신 [current_password](#rule-current-password) 규칙 사용 권장합니다.

<a name="rule-present"></a>
#### present

필드가 입력 데이터 내에 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

필드가 없어야 하거나 비어 있어야 합니다. "비어있음"의 기준:

- 값이 `null`
- 빈 문자열
- 빈 배열 혹은 빈 `Countable` 객체
- 업로드된 파일이나 빈 경로

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

다른 필드가 특정 값일 때 필드는 없어야 하거나 비어 있어야 합니다. "비어있음" 조건은 위와 동일합니다.

복잡한 조건은 `Rule::prohibitedIf` 메서드를 불린 또는 클로저로 사용하세요:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

다른 필드가 특정 값이 아니면 없어야 하거나 비어 있어야 합니다. "비어있음" 조건 동일합니다.

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

해당 필드가 존재할 경우, 지정한 다른 필드들은 모두 없어야 하거나 비어 있어야 합니다.

<a name="rule-regex"></a>
#### regex:_pattern_

필드가 지정한 정규식과 매칭되어야 합니다. 패턴은 PHP `preg_match` 규격이며 구분자가 필요합니다. 예: `'email' => 'regex:/^.+@.+$/i'`

> [!WARNING]
> `regex` 및 `not_regex`는 규칙 배열 형식을 사용하는 것을 권장합니다.

<a name="rule-required"></a>
#### required

필드가 입력 데이터에 존재하며 비어있으면 안 됩니다. "비어있음" 기준:

- `null`
- 빈 문자열
- 빈 배열 또는 빈 Countable
- 경로 없는 업로드 파일

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

다른 필드가 특정 값일 때 필드가 존재하고 비어있지 않아야 합니다.

복잡한 조건은 `Rule::requiredIf`를 사용하세요:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

다른 필드가 특정 값이 아니면 필드가 존재하고 비어있지 않아야 합니다. 비교 필드는 특정 경우(값이 `null`)를 제외하면 반드시 존재해야 합니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

다른 지정 필드 중 어느 하나라도 존재하고 비어있지 않을 때 필드는 존재해야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

다른 지정 필드가 모두 존재하고 비어있지 않을 때 필드는 존재해야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

다른 지정 필드 중 하나라도 비어있거나 없을 때 필드는 존재해야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

다른 지정 필드가 모두 비어있거나 없을 때 필드는 존재해야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

필드는 배열이며 지정된 키들을 최소한 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정 필드와 값이 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

길이가 정확히 _value_ 여야 합니다. 문자열은 글자 수, 숫자형은 수치, 배열은 원소 수, 파일은 킬로바이트 크기로 평가합니다.

예:

```
// 문자 길이 12인지 검증
'title' => 'size:12'

// 정수값이 10인지 검증
'seats' => 'integer|size:10'

// 배열 원소 수가 5인지 검증
'tags' => 'array|size:5'

// 업로드 파일이 512KB인지 검증
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

필드는 지정 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

필드는 문자열이어야 합니다. 만약 `null`도 허용하려면 함께 `nullable` 규칙을 붙이세요.

<a name="rule-timezone"></a>
#### timezone

필드는 `timezone_identifiers_list` PHP 함수에 의해 유효한 시간대 식별자여야 합니다.

<a name="rule-unique"></a>
#### unique:_table_,_column_

필드 값은 지정 데이터베이스 테이블에 존재하지 않아야 합니다.

**테이블 및 컬럼 지정:**

Eloquent 모델명을 직접 지정할 수도 있습니다:

```
'email' => 'unique:App\Models\User,email_address'
```

컬럼명을 지정하지 않으면 필드명이 기본 컬럼명이 됩니다:

```
'email' => 'unique:users,email_address'
```

**특정 연결 지정:**

```
'email' => 'unique:connection.users,email_address'
```

**특정 ID 무시하기:** 

사용자가 이메일을 바꾸지 않은 경우처럼, 특정 ID에 대한 중복 검증을 제외하려면 `Rule` 클래스를 활용합니다:

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

> [!WARNING]
> 사용자 입력을 `ignore` 메서드에 직접 넣으면 SQL 주입 공격에 취약해집니다. 반드시 시스템에서 생성한 고유 ID만 넣어야 합니다.

모델 인스턴스 전체를 넘겨도 자동으로 키를 추출합니다:

```
Rule::unique('users')->ignore($user)
```

기본 PK(`id`)가 아니라 다른 컬럼도 지정할 수 있습니다:

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 필드명과 같은 컬럼명을 검사하지만 다음과 같이 바꿀 수도 있습니다:

```
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 조건 달기:**

쿼리를 더욱 특정 조건으로 제한하려면 `where` 메서드를 사용하세요:

```
'email' => Rule::unique('users')->where(fn ($query) => $query->where('account_id', 1))
```

<a name="rule-uppercase"></a>
#### uppercase

필드는 모두 대문자여야 합니다.

<a name="rule-url"></a>
#### url

필드는 유효한 URL이어야 합니다.

<a name="rule-ulid"></a>
#### ulid

필드는 유효한 ULID([Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec))여야 합니다.

<a name="rule-uuid"></a>
#### uuid

필드는 RFC 4122 버전 1, 3, 4, 5 중 하나에 따른 UUID여야 합니다.

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 검증 건너뛰기

특정 필드 값에 따라 다른 필드 검증을 제외할 때 `exclude_if` 규칙을 사용합니다. 예:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로 `exclude_unless`는 특정 값일 때만 검증합니다:

```
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 값이 존재할 때만 검증하기

필드가 입력 데이터에 존재할 때만 검증하려면 `sometimes` 규칙을 추가하세요:

```
$v = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

`email` 필드는 존재할 때만 검증됩니다.

> [!NOTE]
> 항상 존재해야 하지만 빈 값 가능 필드는 [선택적 필드 주의사항](#a-note-on-optional-fields)을 참조하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

예를 들어 `games` 필드가 100 이상일 때 `reason` 필드를 필수로 하려면 다음처럼 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);

$validator->sometimes('reason', 'required|max:500', function ($input) {
    return $input->games >= 100;
});
```

여러 필드를 한꺼번에 조건 지정할 수도 있습니다:

```
$validator->sometimes(['reason', 'cost'], 'required', function ($input) {
    return $input->games >= 100;
});
```

`$input`은 `Illuminate\Support\Fluent` 객체입니다. 입력 데이터와 파일을 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 검증

배열 내 인덱스를 알 수 없는 중첩 필드를 조건부로 검증하려면, 불필요한 인자인 `$item`을 클로저 인자로 받아 사용합니다:

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

<a name="validating-arrays"></a>
## 배열 검증하기

[`array` 규칙](#rule-array)처럼 유효 배열 키를 지정할 수 있습니다. 지정하지 않은 키가 존재하면 검증에 실패합니다:

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

배열 내 허용할 키를 항상 명시하는 것이 권장되며, 그렇지 않으면 `validate`/`validated` 결과에 검증하지 않은 키까지 포함됩니다.

<a name="validating-nested-array-input"></a>
### 중첩된 배열 입력 검증하기

HTTP 요청의 `photos[profile]` 같은 중첩 필드는 "닷 표기법"으로 다음과 같이 검증 가능합니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열 요소마다 검증할 수도 있습니다. 예: 이메일 배열 내 모든 항목의 고유성 검사:

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

언어 파일의 [커스텀 메시지 지정하기](#custom-messages-for-specific-attributes)에 `*` 문자를 사용하면 배열 전용 메시지 작성이 편리합니다:

```
'custom' => [
    'person.*.email' => [
        'unique' => '각 사람은 고유한 이메일 주소를 가져야 합니다.',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근하기

배열 내 각 원소별 폭넓은 검사 규칙이 필요하면 `Rule::forEach`를 사용하세요. 각 배열 요소의 값과 완전한 속성명을 받아 배열 요소별 규칙을 정할 수 있습니다:

```
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function ($value, $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="error-message-indexes-and-positions"></a>
### 오류 메시지 인덱스 및 위치

배열 검증 오류에서 어느 위치, 몇 번째 요소가 문제인지 알려주려면 `:index` (0부터 시작), `:position` (1부터 시작) 자리표시자를 커스텀 메시지에 포함하세요:

```
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
    'photos.*.description.required' => '사진 #:position 에 대한 설명을 작성해주세요.',
]);
```

위 예는 2번째 사진이 설명이 없어 아래 오류 메시지를 사용자에게 보여줍니다:

_"사진 #2 에 대한 설명을 작성해주세요."_

<a name="validating-files"></a>
## 파일 검증하기

Laravel은 업로드 파일 검증용으로 `mimes`, `image`, `min`, `max` 같은 다양한 규칙을 제공합니다. 개별 규칙을 일일이 지정할 수 있지만, `File` 검증 규칙 생성기를 사용하면 편리합니다:

```
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

이미지 업로드를 위한 검증에서는 `File::image()` 생성자를 사용하고, `dimensions` 규칙으로 크기를 제한할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;
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
> 이미지 치수 검증 관련 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참조하세요.

<a name="validating-files-file-types"></a>
#### 파일 타입

`types` 메서드는 확장자만 지정해도 되지만, 실제로는 파일 내용을 읽어 MIME 타입을 추측해 검증합니다. MIME 타입과 확장자 매핑 목록은 다음에서 확인하세요:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-passwords"></a>
## 비밀번호 검증

비밀번호 복잡도 유지를 위해 Laravel은 `Password` 규칙 클래스를 제공합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체는 최소 길이, 문자 포함 조건, 대소문자 혼합, 숫자, 기호 등 복잡도 조건을 쉽게 설정하게 해줍니다:

```
// 최소 8자
Password::min(8)

// 최소 한 글자 포함
Password::min(8)->letters()

// 최소 한 대문자 및 한 소문자 포함
Password::min(8)->mixedCase()

// 최소 한 숫자 포함
Password::min(8)->numbers()

// 최소 한 기호 포함
Password::min(8)->symbols()
```

추가로, 공개 유출 여부도 체크할 수 있습니다:

```
Password::min(8)->uncompromised()
```

이 기능은 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 비동기적으로 조회합니다.

유출 횟수 기준을 설정할 수도 있습니다:

```
// 3번 미만 유출만 허용
Password::min(8)->uncompromised(3);
```

모든 조건은 체인으로 연결 가능합니다:

```
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 설정

애플리케이션 한 곳에서 기본 비밀번호 검증 규칙을 지정할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 설정합니다:

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

사용 시 다음처럼 합니다:

```
'password' => ['required', Password::defaults()],
```

기본 규칙에 추가 규칙을 붙이려면 `rules` 메서드를 활용하세요:

```
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 커스텀 검증 규칙

<a name="using-rule-objects"></a>
### 규칙 객체 사용하기

Laravel 내장 검증 규칙 외에 자신만의 규칙이 필요할 수 있습니다. `make:rule` Artisan 명령어로 새로운 규칙 객체를 생성하세요. 예를 들어 문자열이 대문자인지 검사하는 규칙을 만들려면:

```shell
php artisan make:rule Uppercase --invokable
```

`app/Rules` 폴더에 생성되며, 객체는 `__invoke` 메서드 하나로 동작을 정의합니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\InvokableRule;

class Uppercase implements InvokableRule
{
    /**
     * 검증 규칙을 실행합니다.
     *
     * @param  string  $attribute
     * @param  mixed  $value
     * @param  \Closure  $fail
     * @return void
     */
    public function __invoke($attribute, $value, $fail)
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

규칙 작성 후, 검증 규칙 배열에 객체 인스턴스를 추가하세요:

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 메시지 번역하기

직접 메시지 대신 [번역 키]를 전달해 언어별 메시지를 쓸 수도 있습니다:

```
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

`translate` 메서드 인자로 자리표시자 배열과 번역할 언어를 지정할 수 있습니다:

```
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

검증 대상 전체 데이터가 필요하면 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하세요. `setData` 메서드가 자동 호출됩니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\InvokableRule;

class Uppercase implements DataAwareRule, InvokableRule
{
    /**
     * 검증 중인 전체 데이터.
     *
     * @var array
     */
    protected $data = [];

    // ...

    /**
     * 검증 데이터 세팅.
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

또한 검증기 인스턴스가 필요하면 `ValidatorAwareRule`을 구현하고 `setValidator`를 만드세요:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\InvokableRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;

class Uppercase implements InvokableRule, ValidatorAwareRule
{
    /**
     * 검증기 인스턴스.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * 검증기 설정.
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

일회성 커스텀 규칙은 클로저로도 작성 가능합니다. 클로저는 속성명, 값, 그리고 실패 시 호출할 `$fail` 콜백을 받습니다:

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
### 내재적(잠재적) 규칙

기본적으로, 검증 중인 속성이 존재하지 않거나 빈 문자열일 땐 일반 규칙과 커스텀 규칙이 실행되지 않습니다. 예를 들어 [`unique`](#rule-unique) 규칙은 빈 문자열에 대해 실행하지 않습니다:

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

빈 값에도 검증해야 하는 규칙을 만들려면 해당 규칙이 "required" 속성을 암묵적으로 포함한다고 명시해야 합니다. Artisan 명령어를 `--implicit` 옵션과 함께 사용하여 만들 수 있습니다:

```shell
php artisan make:rule Uppercase --invokable --implicit
```

> [!WARNING]
> "내재적" 규칙은 단지 "required"를 암시할 뿐이며, 실제로 결측값에 대해 유효성 실패를 발생시키는지는 직접 제어해야 합니다.