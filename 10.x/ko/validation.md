# Validation

- [소개](#introduction)
- [검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [검증 오류 메시지 표시하기](#quick-displaying-the-validation-errors)
    - [폼 재입력 값 채우기](#repopulating-forms)
    - [선택적 필드에 관한 주의사항](#a-note-on-optional-fields)
    - [검증 오류 응답 형식](#validation-error-response-format)
- [폼 요청 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 권한 부여](#authorizing-form-requests)
    - [오류 메시지 사용자화](#customizing-the-error-messages)
    - [검증을 위한 입력 데이터 준비](#preparing-input-for-validation)
- [수동으로 밸리데이터 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [명명된 오류 가방](#named-error-bags)
    - [오류 메시지 사용자화](#manual-customizing-the-error-messages)
    - [추가 검증 수행하기](#performing-additional-validation)
- [검증된 입력 데이터 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 사용자 지정 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 검증하기](#validating-arrays)
    - [중첩 배열 입력 검증하기](#validating-nested-array-input)
    - [오류 메시지에서 인덱스와 위치 표시하기](#error-message-indexes-and-positions)
- [파일 검증하기](#validating-files)
- [비밀번호 검증하기](#validating-passwords)
- [커스텀 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터를 검증하는 여러 가지 방법을 제공합니다. 보통은 모든 HTTP 요청 객체에서 사용할 수 있는 `validate` 메서드를 이용하는 것이 가장 일반적입니다. 하지만 이 문서에서는 다른 검증 방법들도 함께 다룹니다.

Laravel은 데이터에 적용할 수 있는 다양한 편리한 검증 규칙을 포함하고 있으며, 데이터베이스 테이블 내에서 값이 고유한지 검증하는 기능도 제공합니다. Laravel의 다양한 검증 기능을 잘 알 수 있도록 각 검증 규칙을 자세히 설명합니다.

<a name="validation-quickstart"></a>
## 검증 빠른 시작

Laravel의 강력한 검증 기능을 배우기 위해, 폼 검증과 오류 메시지를 사용자에게 표시하는 완전한 예제를 살펴보겠습니다. 이 높은 수준의 개요를 이해하면 Laravel로 들어오는 요청 데이터를 어떻게 검증하는지 기본적인 흐름을 쉽게 익힐 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트들이 정의되어 있다고 가정합시다:

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 생성하는 폼을 표시합니다. `POST` 라우트는 새 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이 라우트들의 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. `store` 메서드는 일단 비워둡니다.

```
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
     * 새로운 블로그 포스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 포스트 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 검증 로직 작성하기

이제 `store` 메서드를 검증 로직으로 채울 차례입니다. 여기서는 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 검증이 성공하면 코드가 정상적으로 실행되며, 실패하면 `Illuminate\Validation\ValidationException` 예외가 던져지고 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

일반 HTTP 요청에서 검증 실패 시, 이전 URL로 리다이렉트 응답이 생성됩니다. 요청이 XHR 요청(비동기 자바스크립트 요청)인 경우에는 [검증 오류 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드에 대해 더 잘 이해하기 위해, `store` 메서드를 다시 살펴보겠습니다:

```
/**
 * 새로운 블로그 포스트를 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 포스트가 유효한 경우...

    return redirect('/posts');
}
```

위에서 보듯, 검증 규칙은 `validate` 메서드에 전달됩니다. 걱정하지 마세요, 모든 규칙은 [여기](#available-validation-rules)에 문서화되어 있습니다. 검증 실패 시 적절한 응답이 자동으로 생성됩니다. 검증이 통과하면 컨트롤러 실행이 정상적으로 계속됩니다.

또한 규칙을 `|` 문자열 대신 배열로 지정할 수도 있습니다:

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

더불어, `validateWithBag` 메서드를 사용해 요청을 검증하고 해당 검증 오류 메시지를 [명명된 오류 가방](#named-error-bags)에 저장할 수도 있습니다:

```
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 검증 실패 시 중단하기

가끔은 속성에 대해 첫 번째 검증 실패가 발생하면 추가 검증을 하지 않고 멈추고 싶을 때가 있습니다. 그런 경우 `bail` 규칙을 해당 필드에 추가하면 됩니다:

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예에서 `title` 필드의 `unique` 검증이 실패하면 그 뒤의 `max` 규칙은 더 이상 검사하지 않습니다. 규칙들은 명시한 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 관한 주의사항

만약 들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있다면, `.`(점) 표기법으로 필드를 지정할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드명에 실제로 `.` 문자가 포함되어 있다면, 이를 이스케이프(`\.`)하여 점 문법으로 해석되는 것을 방지할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 검증 오류 메시지 표시하기

그렇다면, 요청 필드가 검증을 통과하지 못하면 어떻게 될까요? 앞서 설명했듯 Laravel은 자동으로 사용자를 이전 페이지로 리다이렉트합니다. 이와 함께 모든 검증 오류 메시지와 [요청 입력 데이터](/docs/10.x/requests#retrieving-old-input)도 자동으로 [세션에 플래시](/docs/10.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어가 설치되어 있으면, 모든 뷰에서 `$errors` 변수를 사용할 수 있습니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 기본적으로 활성화됩니다. 따라서 뷰에서 `$errors` 변수가 항상 정의되어 있음을 안심하고 사용할 수 있으며, 이 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 방법은 [오류 메시지 다루기](#working-with-error-messages)를 참고하세요.

예시에서는 검증 실패 시 사용자에게 `create` 메서드의 뷰를 다시 보여주면서 오류 메시지를 출력할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>포스트 생성</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- 포스트 생성 폼 -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 오류 메시지 사용자화

Laravel 내장 검증 규칙마다 기본 오류 메시지가 `lang/en/validation.php`에 위치해 있습니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에는 각 검증 규칙별 번역 항목이 있으며, 필요하면 메시지를 자유롭게 수정할 수 있습니다.

또한 이 파일을 복사해 다른 언어용 디렉터리에 넣으면 애플리케이션의 다국어 메시지를 정의할 수 있습니다. 자세한 내용은 [Laravel 로컬라이제이션 문서](/docs/10.x/localization)를 참고하세요.

> [!WARNING]  
> 기본 Laravel 애플리케이션에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이징하고 싶다면 `lang:publish` Artisan 명령으로 파일을 발행하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 검증

예제에서는 전통적인 폼을 통해 데이터를 전송했지만, 많은 앱은 JavaScript 기반 프론트엔드에서 XHR 요청을 받습니다. 이때 `validate` 메서드를 사용하면 Laravel은 리다이렉션 대신 [검증 오류 메시지를 포함한 JSON 응답](#validation-error-response-format)을 422 HTTP 상태 코드와 함께 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

Blade 뷰에서 `@error` 디렉티브를 사용해 특정 속성에 검증 오류 메시지가 있는지 쉽게 확인할 수 있습니다. `@error` 내부에서는 `$message` 변수를 출력해 메시지를 노출할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">포스트 제목</label>

<input id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

명명된 오류 가방을 사용하는 경우, 두 번째 인자로 오류 가방 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 재입력 값 채우기

검증 오류가 발생해 리다이렉트될 때, Laravel은 요청에 포함된 모든 입력값을 자동으로 [세션에 플래시](/docs/10.x/session#flash-data)합니다. 이를 통해 사용자는 제출을 시도했던 폼에 이전 값을 다시 채울 수 있습니다.

이전 요청의 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하세요. `old`는 이전에 플래시된 세션 데이터를 꺼냅니다:

```
$title = $request->old('title');
```

Blade 템플릿에서는 `old()` 글로벌 헬퍼 함수가 더 편리합니다. 지정한 필드에 이전 값이 없으면 `null`을 반환합니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 관한 주의사항

기본적으로 Laravel은 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 전역 미들웨어 스택에 포함합니다 (`App\Http\Kernel`에서 확인 가능). 이 때문에 "선택적" 필드 중 값이 없을 수 있는 컬럼은 `nullable` 규칙을 꼭 지정해야, 검증기가 `null`을 유효하지 않은 값으로 처리하지 않습니다. 예를 들어:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 경우 `publish_at` 필드는 `null`이거나 적절한 날짜여야 합니다. 만약 `nullable` 규칙을 지정하지 않으면, `null` 값이 올바른 날짜가 아니라고 판단됩니다.

<a name="validation-error-response-format"></a>
### 검증 오류 응답 형식

만약 요청 처리 도중 `Illuminate\Validation\ValidationException` 예외가 발생하고 요청 헤더가 JSON 응답을 기대하면, Laravel은 오류 메시지를 자동으로 정리해 `422 Unprocessable Entity` HTTP 상태 코드와 함께 반환합니다.

아래는 검증 오류의 JSON 응답 예시입니다. 중첩 오류 키는 모두 점(`.`) 표기법으로 평탄화됩니다:

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

더 복잡한 검증 상황에서는 "폼 요청" 클래스를 만드는 것이 편리합니다. 폼 요청은 자체 검증과 권한 부여 로직을 캡슐화하는 커스텀 요청 클래스입니다. 생성은 `make:request` Artisan 명령으로 할 수 있습니다:

```shell
php artisan make:request StorePostRequest
```

생성된 클래스는 `app/Http/Requests` 디렉터리에 위치하게 되며, 해당 경로가 없으면 명령 실행 시 자동 생성됩니다. 폼 요청 클래스에는 보통 `authorize`와 `rules` 두 메서드가 포함됩니다.

`authorize` 메서드는 현재 인증된 사용자가 요청된 작업을 수행할 권한이 있는지 판단합니다. `rules` 메서드는 요청의 데이터에 적용할 검증 규칙을 배열 형식으로 반환합니다:

```
/**
 * 요청에 적용할 검증 규칙 가져오기
 *
 * @return array<string, \Illuminate\Contracts\Validation\Rule|array|string>
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
> `rules` 메서드 인자로 필요한 의존성 주입도 가능하며, 자동으로 Laravel [서비스 컨테이너](/docs/10.x/container)가 해결해 줍니다.

검증 규칙은 어떻게 적용될까요? 컨트롤러 메서드에서 타입힌트로 폼 요청을 지정하기만 하면, 컨트롤러 호출 전에 요청이 자동 검증됩니다. 따라서 컨트롤러 내에 검증 로직을 넣을 필요가 없습니다:

```
/**
 * 새 블로그 포스트 저장
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청 데이터가 이미 유효합니다...

    // 검증된 입력 데이터를 가져오기...
    $validated = $request->validated();

    // 검증된 데이터 중 일부만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

검증 실패 시 사용자는 이전 페이지로 리다이렉트되고, 오류는 세션에 플래시되어 메시지로 표시됩니다. XHR 요청이라면 422 상태 코드와 함께 [JSON 형식의 오류 메시지](#validation-error-response-format)가 반환됩니다.

> [!NOTE]  
> Inertia 기반 Laravel 프론트엔드에 실시간 폼 요청 검증을 추가하고 싶으면 [Laravel Precognition](/docs/10.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 검증 수행하기

초기 검증 완료 후 추가 검증이 필요한 경우, 폼 요청의 `after` 메서드를 활용할 수 있습니다.

`after` 메서드는 `Validator` 인스턴스를 인자로 받는 클로저나 콜러블 배열을 반환해야 하며, 검증 후 호출됩니다. 추가 오류를 직접 추가할 수 있습니다:

```
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 검증 콜러블들 가져오기
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    '이 필드에 문제가 있습니다!'
                );
            }
        }
    ];
}
```

배열 요소로는 호출 가능한(인보크 가능한) 클래스도 넣을 수 있으며, 이들의 `__invoke` 메서드도 `Validator`를 인자로 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 검증 콜러블들 가져오기
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
#### 첫 유효성 실패 시 검증 중단

폼 요청 클래스에 `$stopOnFirstFailure` 프로퍼티를 `true`로 선언하면, 단일 규칙 실패 발생 시 나머지 속성에 대한 검증을 중단하도록 할 수 있습니다:

```
/**
 * 유효성 검사 실패 시 첫 실패에서 중단할지 여부
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이징

검증 실패 시 기본적으로 이전 주소로 리다이렉션하지만, 원하는 경로로 변경할 수 있습니다. `$redirect` 프로퍼티에 경로 문자열을 지정하세요:

```
/**
 * 검증 실패 시 리다이렉션할 URI
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는 네임드 라우트로 리다이렉트하려면 `$redirectRoute` 프로퍼티를 설정합니다:

```
/**
 * 검증 실패 시 리다이렉트할 라우트 이름
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 권한 부여

폼 요청에는 `authorize` 메서드가 있어 인증된 사용자가 실제로 해당 작업 권한이 있는지 판단할 수 있습니다. 예를 들어 사용자가 수정하려는 블로그 댓글의 소유자인지 여부를 확인할 수 있습니다. 대개 [인가 게이트 및 정책](/docs/10.x/authorization)을 활용합니다:

```
use App\Models\Comment;

/**
 * 사용자가 요청을 수행할 권한이 있는지 결정합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

폼 요청은 기본 Laravel 요청 클래스를 상속하므로, `user` 메서드로 인증된 사용자에 접근 가능합니다. 또한 위 예제처럼 `route` 메서드를 호출해 요청 URI 경로 변수에 접근할 수 있습니다. 예컨대 다음 라우트의 `{comment}` 파라미터를 받습니다:

```
Route::post('/comment/{comment}');
```

따라서 라우트 모델 바인딩을 쓰면, 다음처럼 더 간결하게 소유자 여부를 판별할 수 있습니다:

```
return $this->user()->can('update', $this->comment);
```

만약 `authorize` 메서드가 `false`를 반환하면, 403 HTTP 응답이 자동으로 반환되고 컨트롤러 메서드는 호출되지 않습니다.

별도의 위치에 권한 검증 로직이 있다면 `authorize` 메서드를 삭제하거나 다음처럼 항상 `true` 반환하게 만들 수도 있습니다:

```
/**
 * 사용자가 요청할 권한 있는지 결정
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]  
> `authorize` 메서드도 필요한 의존성 주입을 활용할 수 있으며, 서비스 컨테이너가 해결합니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 사용자화

폼 요청에서 오류 메시지를 바꾸려면 `messages` 메서드를 오버라이딩하세요. 이 메서드는 속성-규칙 조합과 해당 메시지 배열을 반환해야 합니다:

```
/**
 * 정의된 검증 규칙의 오류 메시지 가져오기
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => '제목이 필수입니다.',
        'body.required' => '메시지를 입력해주세요.',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 검증 속성명 사용자화

Laravel 기본 메시지에 자주 등장하는 `:attribute` 자리표시자를 특정 맞춤 속성명으로 바꾸고 싶으면, `attributes` 메서드를 재정의하여 속성명-표시명 쌍 배열을 반환하세요:

```
/**
 * 검증 오류에 사용할 사용자 지정 속성명 반환
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => '이메일 주소',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### 검증을 위한 입력 데이터 준비

검증 규칙을 적용하기 전에 요청 데이터를 준비하거나 정제해야 할 경우, `prepareForValidation` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Str;

/**
 * 검증을 위한 데이터 준비
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

검증 통과 후 데이터를 정규화해야 한다면 `passedValidation` 메서드가 호출됩니다:

```
/**
 * 검증 후 처리
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 밸리데이터 생성하기

`validate` 메서드 대신 직접 Validator 인스턴스를 생성하여 사용할 수 있습니다. `Validator` [Facade](/docs/10.x/facades)의 `make` 메서드를 호출합니다:

```
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
            return redirect('post/create')
                        ->withErrors($validator)
                        ->withInput();
        }

        // 검증된 입력 데이터 가져오기...
        $validated = $validator->validated();

        // 검증된 데이터 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드 첫 번째 인자는 검증할 데이터, 두 번째는 검증 규칙 배열입니다.

`fails()` 메서드로 검증 실패 여부를 판단 후, `withErrors` 메서드로 오류 메시지를 세션에 플래시합니다. 리다이렉트 후 뷰에서 `$errors` 변수를 이용해 오류 메시지를 출력할 수 있습니다. `withErrors`는 Validator, MessageBag, 배열 모두 받습니다.

#### 첫 번째 실패 시 검증 중단

`stopOnFirstFailure` 메서드를 호출하면 첫 실패 시 다른 규칙 검증을 멈출 수 있습니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

수동 Validator를 생성하면서도 `validate` 메서드의 자동 리다이렉션 기능을 이용하려면, 생성한 Validator 인스턴스에서 `validate()` 메서드를 호출하세요. 실패하면 사용자에게 자동으로 리다이렉트하거나 XHR 요청이면 [JSON 오류 메시지](#validation-error-response-format)를 반환합니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

명명된 오류 가방을 이용하려면 `validateWithBag`을 사용하세요:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 명명된 오류 가방

하나의 페이지에 여러 폼이 있으면 각각 별도의 `MessageBag`을 명명하여 사용하면 편리합니다. `withErrors` 메서드에 두 번째 인자로 이름을 지정하세요:

```
return redirect('register')->withErrors($validator, 'login');
```

뷰에서는 `$errors->login`으로 이름 붙은 오류 가방을 접근합니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 사용자화

필요하면 `Validator::make`의 세 번째 인자에 사용자 지정 메시지 배열을 지정할 수 있습니다:

```
$validator = Validator::make($input, $rules, [
    'required' => 'The :attribute field is required.',
]);
```

이 때, `:attribute` 자리표시자는 검증 대상 필드명으로 치환됩니다. 다른 자리표시자도 사용할 수 있습니다. 예:

```
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 속성별 사용자 메시지 지정

특정 속성에만 사용자 지정 메시지를 지정하려면 `.` 표기법을 씁니다. 예:

```
$messages = [
    'email.required' => '이메일 주소를 알려주세요!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 사용자 지정 속성 표시값 지정

`Validator::make` 네 번째 인자에 속성명-사용자 속성명 배열을 전달해 `:attribute`를 교체할 값을 바꿀 수도 있습니다:

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 검증 수행하기

초기 검증 후 추가 검증이 필요할 경우, Validator 인스턴스의 `after` 메서드에 클로저나 콜러블 배열을 넣어 호출할 수 있습니다. 이 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 인자로 받으며 오류를 수동 추가할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', '이 필드에 문제가 있습니다!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

`after` 메서드는 콜러블 배열도 받는데, 주로 인보크 가능한 클래스에서 `__invoke` 메서드를 활용할 수 있어 편리합니다:

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
## 검증된 입력 데이터 다루기

폼 요청이나 수동 생성 Validator로 검증 후, 실제 검증된 데이터를 가져오고 싶을 때가 있습니다. 여러 방법이 있습니다.

우선, 폼 요청이나 Validator 인스턴스에서 `validated` 메서드를 호출하면 검증된 데이터 배열을 반환합니다:

```
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 객체가 반환됩니다. 이 객체에선 `only`, `except`, `all` 메서드로 검증 데이터를 부분적으로 또는 전체를 가져올 수 있습니다:

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

`ValidatedInput` 인스턴스는 반복문으로 순회하거나 배열처럼 접근할 수도 있습니다:

```
// 검증된 데이터 반복
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 임의 값을 추가하고 싶으면 `merge`를 호출하세요:

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증 데이터를 [컬렉션](/docs/10.x/collections) 형태로 받고 싶으면 `collect` 메서드를 씁니다:

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기

`Validator` 인스턴스의 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 받습니다. 이 객체는 오류 메시지를 편리하게 다루는 여러 메서드를 제공합니다. 자동으로 뷰에 주입되는 변수 `$errors`도 `MessageBag` 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 오류 메시지 가져오기

`first` 메서드로 필드별 첫 번째 오류 메시지를 가져올 수 있습니다:

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

`get` 메서드로 필드별 모든 메시지를 배열로 얻을 수 있습니다:

```
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 필드를 검증할 땐 `*` 와일드카드를 쓸 수 있습니다:

```
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 가져오기

`all` 메서드를 써서 모든 메시지 배열을 얻을 수 있습니다:

```
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 오류가 있는지 확인

`has` 메서드는 특정 필드에 오류 메시지가 있는지 여부를 Boolean으로 알려줍니다:

```
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 사용자 지정 메시지 지정하기

Laravel 내장 검증 메시지는 애플리케이션의 `lang/en/validation.php`에 있습니다. 만약 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php`에서 각 검증 규칙별 메시지를 볼 수 있으며 자유롭게 변경할 수 있습니다.

또한 이 파일을 복사해 다른 언어용 폴더에 넣으면 다국어 메시지 전환이 가능합니다. 자세한 내용은 [로컬라이제이션 문서](/docs/10.x/localization)를 참고하세요.

> [!WARNING]  
> 기본 Laravel 앱에는 `lang` 폴더가 없습니다. 언어 파일을 바꾸고 싶으면 `lang:publish` 명령어로 발행하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 사용자 메시지

속성별/규칙별로 특정 메시지를 커스터마이즈하려면 `lang/xx/validation.php` 파일 내 `custom` 배열에 메시지를 추가하세요:

```
'custom' => [
    'email' => [
        'required' => '이메일 주소가 꼭 필요합니다!',
        'max' => '이메일 주소가 너무 깁니다!',
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

:attribute 플레이스홀더 대신 사용자화한 값을 사용하려면, `lang/xx/validation.php` 의 `attributes` 배열을 이용합니다:

```
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]  
> 기본 Laravel 앱에는 `lang` 폴더가 없습니다. 언어 파일을 바꾸고 싶으면 `lang:publish` 명령어로 발행하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 규칙 메시지에 등장하는 `:value` 플레이스홀더를 더 친숙한 값으로 교체할 수 있습니다. 예를 들어 `payment_type`이 `cc`일 때 크레딧 카드 번호가 필요하게 하는 규칙:

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

검증 실패 시 세부 메시지는 기본적으로:

```none
The credit card number field is required when payment type is cc.
```

`lang/xx/validation.php`에 다음을 추가해 사용자가 보는 값을 바꿀 수 있습니다:

```
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

바뀐 메시지는 다음과 같습니다:

```none
The credit card number field is required when payment type is credit card.
```

> [!WARNING]  
> 기본 Laravel 앱에는 `lang` 폴더가 없습니다. 언어 파일을 바꾸고 싶으면 `lang:publish` 명령어로 발행하세요.

<a name="available-validation-rules"></a>
## 사용 가능한 검증 규칙

아래는 지원하는 모든 검증 규칙과 그 기능 목록입니다.

<div class="collection-method-list" markdown="1">

[accepted](#rule-accepted)
[accepted_if](#rule-accepted-if)
[active_url](#rule-active-url)
[after (date)](#rule-after)
[after_or_equal (date)](#rule-after-or-equal)
[alpha](#rule-alpha)
[alpha_dash](#rule-alpha-dash)
[alpha_num](#rule-alpha-num)
[array](#rule-array)
[ascii](#rule-ascii)
[bail](#rule-bail)
[before (date)](#rule-before)
[before_or_equal (date)](#rule-before-or-equal)
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
[dimensions (image files)](#rule-dimensions)
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
[exists (database)](#rule-exists)
[extensions](#rule-extensions)
[file](#rule-file)
[filled](#rule-filled)
[gt](#rule-gt)
[gte](#rule-gte)
[hex_color](#rule-hex-color)
[image (file)](#rule-image)
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
[present](#rule-present)
[present_if](#rule-present-if)
[present_unless](#rule-present-unless)
[present_with](#rule-present-with)
[present_with_all](#rule-present-with-all)
[prohibited](#rule-prohibited)
[prohibited_if](#rule-prohibited-if)
[prohibited_unless](#rule-prohibited-unless)
[prohibits](#rule-prohibits)
[regex](#rule-regex)
[required](#rule-required)
[required_if](#rule-required-if)
[required_if_accepted](#rule-required-if-accepted)
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
[unique (database)](#rule-unique)
[uppercase](#rule-uppercase)
[url](#rule-url)
[ulid](#rule-ulid)
[uuid](#rule-uuid)

</div>

<a name="rule-accepted"></a>
#### accepted

검증 대상 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 보통 이용 약관 동의 등의 필드 검증에 사용됩니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

검증 대상 필드는, 다른 필드값이 특정 값일 경우 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 동의 여부 등 조건부 필드 검증에 유용합니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드는 PHP의 `dns_get_record` 함수가 확인하는 유효한 A 또는 AAAA DNS 레코드를 가져야 합니다. URL 호스트네임은 `parse_url` 함수로 추출되어 검증에 사용됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 값이 지정된 날짜 이후여야 합니다. 날짜는 내부적으로 PHP `strtotime` 함수에 전달되어 변환됩니다:

```
'start_date' => 'required|date|after:tomorrow'
```

날짜 문자열 대신 다른 필드명도 지정할 수 있습니다:

```
'finish_date' => 'required|date|after:start_date'
```

<a name="rule-after-or-equal"></a>
#### after_or_equal:_date_

검증 대상 값이 지정된 날짜 이후이거나 같은 날짜여야 합니다. 상세 내용은 [after](#rule-after) 규칙 참조.

<a name="rule-alpha"></a>
#### alpha

검증 대상 값은 전부 유니코드 문자여야 하며, [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함되는 문자만 가능합니다.

아스키 문자 범위(`a-z` 및 `A-Z`)만 허용하려면 `ascii` 옵션을 규칙에 추가하세요:

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

문자는 유니코드 문자 중 [`\p{L}`], [`\p{M}`], [`\p{N}`], 그리고 아스키 대시(`-`)와 아스키 언더스코어(`_`)만 포함해야 합니다.

아스키 문자만 허용하려면 다음과 같이 합니다:

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

문자는 유니코드 문자 중 [`\p{L}`], [`\p{M}`], [`\p{N}`]만 포함해야 합니다.

아스키 문자만 허용하려면 다음과 같이 합니다:

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 대상이 PHP 배열이어야 합니다.

`array` 규칙에 추가 인자를 지정하면, 배열의 키는 규칙에 명시한 목록에 포함되어야 합니다. 아래 예에서 `admin` 키는 규칙 목록에 없어 검증 실패합니다:

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

일반적으로 배열에 허용되는 키 목록을 명시하는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

검증 대상 값이 7비트 아스키 문자로만 이루어져야 합니다.

<a name="rule-bail"></a>
#### bail

첫 번째 검증 실패 발생 후 해당 필드에 대한 검증을 중단합니다.

`bail` 규칙은 특정 필드별 검증 중단이고, `stopOnFirstFailure`는 모든 속성에 대해 첫 실패 시 검증 전체를 멈춥니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 대상 값이 지정한 날짜 이전이어야 합니다. 날짜는 `strtotime` 함수로 변환됩니다. `after` 규칙처럼 다른 필드명도 지정할 수 있습니다.

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 대상 값이 지정한 날짜 이전이거나 같은 날짜여야 합니다. `strtotime` 기준이며, 다른 필드명도 가능합니다.

<a name="rule-between"></a>
#### between:_min_,_max_

값이 지정된 최소값과 최대값(포함) 사이여야 합니다. 문자열, 숫자, 배열, 파일 크기에 모두 동일한 방식으로 적용됩니다. 자세한 내용은 [`size`](#rule-size) 규칙 참고.

<a name="rule-boolean"></a>
#### boolean

값이 논리형으로 변환할 수 있어야 합니다. 허용 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"` 입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드가 `{field}_confirmation`이라는 이름의 필드와 값이 일치해야 합니다. 예를 들어 `password`라면 `password_confirmation` 필드가 있어야 합니다.

<a name="rule-current-password"></a>
#### current_password

인증된 사용자의 비밀번호와 일치해야 합니다. 첫 번째 인자로 인증 guard를 지정할 수 있습니다:

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

값이 유효한, 상대적이지 않은 날짜 문자열이어야 하며, PHP `strtotime` 함수로 확인됩니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

값이 지정된 날짜와 같아야 합니다. `strtotime` 기반으로 처리됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

값이 지정된 날짜 형식 중 하나와 일치해야 합니다. `date` 규칙과 함께 쓰면 안 됩니다. PHP `DateTime` 클래스에서 지원하는 모든 날짜 형식을 지원합니다.

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

값이 숫자이며 소수점 이하 자릿수가 주어진 범위 내여야 합니다:

```
// 소수점 두 자리
'price' => 'decimal:2'

// 2~4자리 소수점
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

값이 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

해당 필드는, 다른 필드의 값이 특정 값일 때 위 지정된 값 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

해당 필드와 다른 필드의 값이 서로 달라야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

정수일 때 값의 길이가 정확히 주어진 값이어야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

정수일 때 값의 길이가 주어진 최소값과 최대값 사이여야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 이미지이며, 다음 제약 조건을 만족해야 합니다:

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

가능한 제약 조건은 _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_ 입니다.

비율은 분수(`3/2`) 또는 부동소수점(`1.5`)으로 표현할 수 있습니다:

```
'avatar' => 'dimensions:ratio=3/2'
```

`Rule::dimensions` 메서드를 이용해 플루언트하게 규칙을 만들 수도 있습니다:

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

배열 데이터 검증 시 중복 값이 없어야 합니다:

```
'foo.*.id' => 'distinct'
```

기본적으로 느슨한 비교를 합니다. 엄격한 비교를 원하면 `strict` 옵션을 추가합니다:

```
'foo.*.id' => 'distinct:strict'
```

대소문자를 무시하는 경우 `ignore_case` 옵션도 쓸 수 있습니다:

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

값이 지정된 문자열 중 어느 것으로도 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

값이 지정된 문자열 중 어느 것으로도 끝나서는 안 됩니다.

<a name="rule-email"></a>
#### email

값이 이메일 형식이어야 합니다. 이 검증은 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본 검증은 `RFCValidation` 스타일이지만 다른 스타일도 적용 가능합니다:

```
'email' => 'email:rfc,dns'
```

사용 가능한 검증 스타일 목록:

- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`
- `filter_unicode`: `FilterEmailValidation::unicode()`

`filter`는 PHP 함수 `filter_var` 기반이며, Laravel 5.8 이전 기본 이메일 검증 방식입니다.

> [!WARNING]  
> `dns` 및 `spoof` 검사에는 PHP `intl` 확장이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

값이 지정된 문자열 중 어느 것으로도 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 클래스 기반 규칙으로, 값이 유효한 Enum 값인지 검증합니다. `Enum` 생성자에 Enum 클래스 이름을 지정합니다. 기본값은 백드 Enum입니다:

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙은 `only`와 `except` 메서드로 검사할 Enum 케이스 집합을 제한할 수 있습니다:

```
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 이용해 조건부로 규칙을 설정할 수도 있습니다:

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

검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 결과 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

`anotherfield` 필드 값이 특정 값일 때 검증 대상 필드를 결과 데이터에서 제외합니다.

복잡한 조건을 지정하려면 `Rule::excludeIf` 메서드를 사용하며, 불리언 또는 클로저를 인자로 받습니다:

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

검증 대상 필드를 제외하는데, `anotherfield` 값이 특정 값과 다를 경우 결과 데이터에서 제외합니다. 값이 `null`일 경우, 비교 필드가 `null`이거나 요청에 없을 때 제외됩니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

`anotherfield` 필드가 존재하면 검증 대상 필드를 결과 데이터에서 제외합니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

`anotherfield` 필드가 없으면 검증 대상 필드를 결과 데이터에서 제외합니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

값이 주어진 데이터베이스 테이블의 특정 컬럼에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 규칙 기본 사용법

```
'state' => 'exists:states'
```

컬럼명이 지정되지 않으면 필드명을 사용합니다. 예를 들어 위 예에서는 `states` 테이블에 `state` 컬럼에 일치하는 값이 있어야 합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 지정 컬럼명 명시

테이블명 뒤에 컬럼명을 붙여 지정할 수 있습니다:

```
'state' => 'exists:states,abbreviation'
```

때로는 연결할 데이터베이스 커넥션도 지정 가능합니다:

```
'email' => 'exists:connection.staff,email'
```

테이블명 대신 Eloquent 모델명도 지정할 수 있습니다:

```
'user_id' => 'exists:App\Models\User,id'
```

쿼리를 커스터마이징하려면 `Rule` 클래스를 활용하세요:

```
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            return $query->where('account_id', 1);
        }),
    ],
]);
```

`Rule::exists` 메서드 두 번째 인자로 컬럼명을 명시할 수 있습니다:

```
'state' => Rule::exists('states', 'abbreviation'),
```

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 대상 파일 확장자가 지정된 것 중 하나여야 합니다:

```
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]  
> 파일 확장자만으로 검증하는 것은 충분치 않으니, 보통 [`mimes`](#rule-mimes) 또는 [`mimetypes`](#rule-mimetypes) 규칙과 함께 사용하세요.

<a name="rule-file"></a>
#### file

검증 대상 필드는 정상 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

존재하는 경우 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

값이 지정 필드 또는 값보다 커야 하며, 크기 비교 기준은 [`size`](#rule-size) 규칙과 동일합니다.

<a name="rule-gte"></a>
#### gte:_field_

값이 지정 필드 또는 값보다 크거나 같아야 하며, 크기 비교 기준은 [`size`](#rule-size) 규칙과 동일합니다.

<a name="rule-hex-color"></a>
#### hex_color

16진수 색상값이어야 합니다.

<a name="rule-image"></a>
#### image

업로드된 파일이 이미지여야 합니다(jpg, jpeg, png, bmp, gif, svg, webp 확장자 포함).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

값이 지정된 리스트 내에 포함되어야 합니다. `Rule::in` 메서드를 사용해 배열을 통한 선언도 가능합니다:

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

`in` 규칙과 `array` 규칙이 조합되면 배열 내 모든 값이 리스트에 포함되어야 합니다:

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

위의 예에서 `LAS`가 리스트에 없어 실패합니다.

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

값이 `anotherfield` 필드 값 배열에 존재해야 합니다.

<a name="rule-integer"></a>
#### integer

값이 정수여야 합니다.

> [!WARNING]  
> 이 규칙은 변수 타입이 아니라 PHP의 `FILTER_VALIDATE_INT`에 통과하는 값인지 확인합니다. 숫자 타입 검증은 `numeric` 규칙과 같이 쓰세요.

<a name="rule-ip"></a>
#### ip

유효한 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

유효한 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

유효한 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

올바른 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

값이 지정 필드 값보다 작아야 합니다. 크기 비교 기준은 [`size`](#rule-size) 규칙과 동일합니다.

<a name="rule-lte"></a>
#### lte:_field_

값이 지정 필드 값보다 작거나 같아야 합니다. 크기 비교 기준은 [`size`](#rule-size) 규칙과 동일합니다.

<a name="rule-lowercase"></a>
#### lowercase

값이 소문자여야 합니다.

<a name="rule-mac"></a>
#### mac_address

MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

값이 최대 값 이하여야 합니다. 크기 비교 기준은 [`size`](#rule-size) 규칙과 동일합니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

정수 일 때 자리 수가 최대 값 이하여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

파일 MIME 타입이 지정된 타입 중 하나여야 합니다:

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

서버측에서 파일 내용을 읽어 MIME 타입을 유추하기 때문에 클라이언트가 보낸 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

파일 확장자가 지정된 것 중 하나여야 합니다:

```
'photo' => 'mimes:jpg,bmp,png'
```

파일 내용을 읽어 MIME 타입도 검사합니다. MIME 타입과 확장자가 다르면 주의해야 합니다. 전체 MIME 타입-확장자 목록은 다음 링크를 참고하세요:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자 차이

이 규칙은 MIME 타입과 사용자 지정 확장자간 일치 여부를 확인하지 않습니다. 예를 들어, `mimes:png` 는 파일 내용이 PNG라면 실제 파일명이 `.txt`여도 통과합니다. 확장자 검사를 하려면 [`extensions`](#rule-extensions) 규칙을 병행하세요.

<a name="rule-min"></a>
#### min:_value_

값이 최소 값 이상이어야 합니다. 크기는 [`size`](#rule-size) 규칙과 동일 기준입니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

정수 자리수가 최소 값 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

값이 지정 값의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

필드가 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

`anotherfield` 필드가 특정 값일 때 필드는 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

`anotherfield` 필드가 특정 값이 아닌 경우 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

나열된 다른 필드 중 어느 하나라도 존재하면 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

나열된 다른 필드가 모두 존재해야 필드는 존재하지 않아야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

값이 지정한 목록에 포함되어 있으면 안 됩니다. `Rule::notIn` 으로도 선언할 수 있습니다:

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

값이 정규식에 매치되지 않아야 합니다.

내부적으로 PHP `preg_match`를 사용하므로, 패턴은 `preg_match` 구문을 따라 유효한 구분자를 포함해야 합니다. 예:

`'email' => 'not_regex:/^.+$/i'`

> [!WARNING]  
> `regex`/`not_regex` 패턴을 `|` 구분자 없이 배열로 명시해야 할 수도 있습니다. 특히 정규식에 `|` 포함 시 주의하세요.

<a name="rule-nullable"></a>
#### nullable

필드가 `null`일 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

값이 숫자형이어야 합니다.

<a name="rule-present"></a>
#### present

입력 데이터에 필드가 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

`anotherfield` 필드가 특정 값일 때 필드가 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

`anotherfield` 필드가 특정 값이 아니면 필드는 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

나열된 다른 필드 중 어느 하나라도 존재하면 필드가 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

나열된 모든 다른 필드가 존재하면 필드가 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

필드가 없는 상태거나 비어 있어야 합니다. 비어있다는 뜻은 다음 중 하나에 해당합니다:

- 값이 `null`
- 빈 문자열
- 빈 배열 혹은 `Countable` 객체가 비어 있음
- 업로드 된 파일 경로가 빈 문자열

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

`anotherfield` 필드가 특정 값일 때 필드가 없어야 하거나 비어 있어야 합니다.

비어있다는 조건은 [`prohibited`](#rule-prohibited) 규칙과 동일합니다.

복잡한 조건은 `Rule::prohibitedIf` 메서드에 부울 혹은 클로저로 지정 가능합니다:

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

`anotherfield` 필드가 특정 값이 아니면 필드가 없어야 하거나 비어 있어야 합니다.

비어있다는 조건은 [`prohibited`](#rule-prohibited) 규칙과 동일합니다.

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

필드가 존재하고 비어 있지 않으면, 지정된 모든 `anotherfield` 필드가 존재하지 않거나 비어 있어야 합니다.

<a name="rule-regex"></a>
#### regex:_pattern_

값이 지정한 정규식과 매치되어야 합니다.

정규식은 PHP `preg_match` 구문을 따르고, 유효한 구분자 포함해야 합니다. 예:

`'email' => 'regex:/^.+@.+$/i'`

> [!WARNING]  
> `regex`/`not_regex` 규칙을 `|` 구분자 대신 배열로 써야 할 수도 있습니다. 특히 정규식 안에 `|`가 있을 때 주의하세요.

<a name="rule-required"></a>
#### required

필드가 반드시 존재하며 비어 있으면 안 됩니다. 비어 있다는 뜻은:

- 값이 `null`
- 빈 문자열
- 빈 배열 혹은 `Countable` 객체가 비어 있음
- 업로드된 파일이지만 경로가 없음

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

`anotherfield` 필드가 특정 값이면 필드가 반드시 존재하고 빈 값이 아니어야 합니다.

복잡한 조건은 `Rule::requiredIf` 메서드에 부울이나 클로저로 지정할 수 있습니다:

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

<a name="rule-required-if-accepted"></a>
#### required_if_accepted:_anotherfield_,...

`anotherfield` 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나일 때 필드가 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

`anotherfield` 필드가 특정 값이 아니면 필드가 존재하고 비어 있지 않아야 합니다. 만약 값이 `null`이라면(예: `required_unless:name,null`), 비교 필드가 `null`이거나 요청에 없으면 필드는 필수입니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

나열된 필드 중 하나라도 존재하고 빈 값이 아니면 필드가 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

나열된 필드가 모두 존재하고 빈 값이 아니면 필드가 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

나열된 필드 중 하나 이상이 없거나 빈 값이면 필드가 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

나열된 필드가 모두 없거나 빈 값일 때 필드가 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

필드가 배열이며, 지정된 키들을 반드시 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

검증 대상 필드와 지정 필드의 값이 같아야 합니다.

<a name="rule-size"></a>
#### size:_value_

값이 지정 크기와 같아야 합니다. 크기 기준은 다음과 같습니다:

- 문자열: 문자 수
- 숫자: 숫자 값 (numeric/ip integer 규칙 필요)
- 배열: 원소 개수
- 파일: 파일 크기(킬로바이트)

예시:

```
// 길이가 정확히 12자인 문자열 검증...
'title' => 'size:12';

// 값이 10인 정수 검증...
'seats' => 'integer|size:10';

// 원소가 5개인 배열 검증...
'tags' => 'array|size:5';

// 크기가 512KB인 파일 검증...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

값이 지정된 문자열 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

값이 문자열이어야 합니다. `null`을 허용하려면 `nullable` 규칙도 지정하세요.

<a name="rule-timezone"></a>
#### timezone

유효한 타임존 식별자여야 하며, `DateTimeZone::listIdentifiers` 메서드 결과 내에 있어야 합니다.

옵션 값으로 `DateTimeZone::listIdentifiers` 인자를 전달할 수 있습니다:

```
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

값이 데이터베이스 테이블 내에서 유일해야 합니다.

**테이블/컬럼명 지정:**

테이블명 대신 Eloquent 모델 명으로도 지정 가능:

```
'email' => 'unique:App\Models\User,email_address'
```

컬럼명을 명시하지 않으면 필드명 사용:

```
'email' => 'unique:users,email_address'
```

**커스텀 커넥션 지정:**

SQL 쿼리에 사용할 연결명을 테이블명 앞에 붙일 수 있습니다:

```
'email' => 'unique:connection.users,email_address'
```

**특정 ID 무시하기:**

기존 레코드 업데이트 시 해당 ID를 무시하려면 `Rule` 클래스를 사용하세요. 다음은 배열 규칙 예입니다:

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
> 사용자 입력을 `ignore`에 직접 넣으면 SQL 인젝션 위험이 있으니 절대 하지 마세요. 시스템에서 생성된 정수 ID나 UUID만 넣으세요.

`ignore`에 모델 인스턴스를 넣으면 키 값이 자동으로 추출됩니다:

```
Rule::unique('users')->ignore($user)
```

키 컬럼명이 `id`가 아니면 두 번째 인자로 컬럼명을 지정할 수 있습니다:

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 검증 대상 필드명이 컬럼명으로 쓰이나, 다르게 지정하고 싶으면 첫 번째 인자가 컬럼명입니다:

```
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 where 구문 추가:**

쿼리를 추가로 제한하려면 `where` 메서드를 씁니다:

```
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

<a name="rule-uppercase"></a>
#### uppercase

값이 모두 대문자여야 합니다.

<a name="rule-url"></a>
#### url

값이 유효한 URL이어야 합니다.

프로토콜을 특정할 수도 있습니다:

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

값이 유효한 ULID(범용 고유 레키시컬 식별자)여야 합니다.

<a name="rule-uuid"></a>
#### uuid

값이 RFC 4122 버전 1, 3, 4, 5 UUID여야 합니다.

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 검증 스킵하기

특정 필드 값에 따라 다른 필드 검증을 하지 않으려면 `exclude_if` 규칙을 사용합니다. 예를 들어 `has_appointment`가 `false`이면 `appointment_date`와 `doctor_name`은 검증되지 않습니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로 `exclude_unless`를 써서 특정 값일 때만 검증할 수도 있습니다:

```
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 값이 존재할 때만 검사하기

검증 대상 필드가 존재하는 경우에만 검사하려면 `sometimes` 규칙을 추가하세요:

```
$v = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예에서 `email` 필드는 `$data` 배열 내에 있을 때만 검증됩니다.

> [!NOTE]  
> 필드가 항상 존재하지만 비어 있을 수 있다면 [선택적 필드에 관한 주의사항](#a-note-on-optional-fields)을 참고하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

좀 더 복잡한 조건에 따라 검증 규칙을 추가할 수 있습니다. 예를 들어, 어떤 필드 값이 100 이상인 경우 특정 이유(reason)를 필수화하거나 여러 필드를 한꺼번에 조건부로 검사할 수도 있습니다.

먼저 고정된(변하지 않는) 정적 규칙으로 Validator를 만들고:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);
```

게임 수가 100개 이상이면 이유 필드를 특정 규칙으로 추가해봅니다:

```
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드 첫 인자는 필드명, 두 번째는 추가할 규칙, 세 번째는 조건 클로저입니다. 클로저가 참을 반환하면 규칙이 추가됩니다.

여러 필드에 조건부 규칙 추가도 가능합니다:

```
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]  
> 클로저 인자인 `$input`은 `Illuminate\Support\Fluent` 인스턴스이며, 검증 대상 입력과 파일에 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 중첩 배열 조건부 검증

배열 내 요소가 다른 요소 값에 따라 규칙이 달라야 할 경우, 두 번째 인자 `$item`을 클로저로 받아 처리합니다:

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

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

`$input`과 `$item`은 배열인 경우 `Fluent` 객체로, 그렇지 않을 경우 문자열입니다.

<a name="validating-arrays"></a>
## 배열 검증하기

[`array`](#rule-array) 규칙처럼, 배열 키를 명시하지 않으면 배열 내 모든 키가 결과에 포함되어 검증되지 않은 키도 포함될 수 있습니다. 예를 들어:

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

그러므로 배열 키 목록을 항상 지정하는 게 좋습니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 검증

중첩 배열 폼 입력도 점 표기법으로 쉽게 검증 가능합니다. 예를 들어, 들어오는 요청에 `photos[profile]` 필드가 있다면:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열 내 각 요소에도 규칙을 적용할 수 있습니다. 예를 들어 `person.*.email` 배열 각 이메일이 고유해야 한다면:

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

언어 파일 내 메시지 커스터마이즈도 `*` 와일드카드를 쓸 수 있습니다:

```
'custom' => [
    'person.*.email' => [
        'unique' => '각 사람은 고유한 이메일 주소여야 합니다.',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근

검증 규칙을 동적으로 생성할 때 입력값과 풀 네임 속성명을 인자로 받는 `Rule::forEach` 메서드를 사용하세요:

```
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
### 오류 메시지에서 인덱스와 위치 표시하기

배열 검증 시 실패한 배열 원소 위치를 오류 메시지에 명시하고 싶으면, `:index` (0부터 시작) 또는 `:position` (1부터 시작) 자리표시자를 메시지에 포함하세요:

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
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

위 예에서 검증 실패 시 `Please describe photo #2.` 메시지가 나옵니다.

더 깊게 중첩된 인덱스도 `second-index`, `second-position`, `third-index`, `third-position` 등으로 참조할 수 있습니다:

```
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 검증하기

Laravel은 `mimes`, `image`, `min`, `max` 등 다양한 규칙으로 업로드된 파일을 검증할 수 있습니다. 직접 규칙을 지정해도 되지만, `File` 규칙 빌더를 쓰면 CRUD 작업이 편리합니다:

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

이미지 파일 검증 시 `File::image()` 메서드도 유용하며, 이미지 크기는 `dimensions` 규칙으로 제한 가능합니다:

```
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
> 이미지 크기 제한은 [dimensions 규칙 문서](#rule-dimensions)에서 자세히 확인할 수 있습니다.

<a name="validating-files-file-sizes"></a>
#### 파일 크기 단위

최소 및 최대 크기는 문자열로 `kb`, `mb`, `gb`, `tb` 단위 접미사를 붙여 지정할 수 있습니다:

```php
File::image()
    ->min('1kb')
    ->max('10mb')
```

<a name="validating-files-file-types"></a>
#### 파일 유형

`types` 메서드에 확장자만 지정하지만, 내부적으로 파일 내용을 열어 MIME 타입까지 검사합니다. MIME 타입과 확장자의 완전한 목록은 다음 링크를 참고하세요:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-passwords"></a>
## 비밀번호 검증하기

비밀번호 복잡성 보장을 위해 Laravel `Password` 규칙 객체를 사용할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체는 최소 문자 수, 최소 문자 포함, 대소문자 혼합, 숫자 포함, 기호 포함 같은 요구사항 커스터마이즈를 체이닝으로 지원합니다:

```
// 최소 8자
Password::min(8)

// 최소 한 개 문자 포함
Password::min(8)->letters()

// 대문자, 소문자 각 최소 한 개 포함
Password::min(8)->mixedCase()

// 최소 한 개 숫자 포함
Password::min(8)->numbers()

// 최소 한 기호 포함
Password::min(8)->symbols()
```

더해, `uncompromised` 메서드로 공개된 비밀번호 데이터 유출 여부를 검사할 수 있습니다:

```
Password::min(8)->uncompromised()
```

내부적으로 [k-익명성](https://en.wikipedia.org/wiki/K-anonymity) 모델 기반으로 서비스 [haveibeenpwned.com](https://haveibeenpwned.com)을 익명으로 조회합니다.

기본 정책은 데이터 유출 내 최소 1회 나타나면 실패 처리이며, 이 임계값을 인자로 조정할 수 있습니다:

```
// 최대 3회 이하 유출인 경우까지 허용
Password::min(8)->uncompromised(3);
```

위 모든 메서드를 체이닝할 수 있습니다:

```
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의

애플리케이션 공통 기본 비밀번호 규칙을 쉽게 지정하려면 `Password::defaults` 메서드를 이용하세요. 이 메서드는 클로저를 인자로 받아 기본 비밀번호 규칙을 반환합니다. 보통 서비스 프로바이더 `boot` 메서드내에서 정의합니다:

```php
use Illuminate\Validation\Rules\Password;

/**
 * 애플리케이션 서비스 부트스트랩
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

그런 다음 규칙을 적용할 때는 인자 없이 `defaults`를 호출합니다:

```
'password' => ['required', Password::defaults()],
```

기본 규칙에 추가 규칙을 더 붙이려면 `rules` 메서드를 쓰면 됩니다:

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

Laravel의 기본 검증 규칙들 외에 자신만의 규칙을 지정할 수 있습니다. 한 방법으로 규칙 객체를 사용합니다. 새로운 규칙을 만들려면 Artisan 명령을 쓰세요:

```shell
php artisan make:rule Uppercase
```

이 명령은 `app/Rules` 경로에 `Uppercase` 클래스를 생성합니다.

규칙 객체는 `validate` 메서드를 갖습니다. 이 메서드는 속성명, 값, 실패 시 호출할 `$fail` 콜백을 인자로 받습니다:

```
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * 규칙 실행
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

정의 후 검증시 규칙 객체를 인스턴스로 전달하세요:

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 검증 메시지 번역

`$fail` 클로저에 리터럴 메시지 대신 [번역 키](/docs/10.x/localization)를 지정해 자동 번역을 할 수 있습니다:

```
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하면 번역 시 자리표시자 치환이나 언어 지정도 할 수 있습니다:

```
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근

규칙 객체에서 전체 검증 데이터를 사용하려면 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하세요. 여기엔 `setData` 메서드가 요구되며, 전체 데이터를 담은 배열이 전달됩니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * 검증 중인 전체 데이터
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * 데이터 설정
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

검증을 수행하는 Validator 인스턴스가 필요하다면 `ValidatorAwareRule` 인터페이스를 구현하세요:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * Validator 인스턴스
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Validator 설정
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a name="using-closures"></a>
### 클로저 사용하기

한 번만 쓰는 간단한 규칙이라면 클로저로도 할 수 있습니다. 클로저는 속성명, 값, 실패 시 호출할 `$fail` 콜백을 인자 받습니다:

```
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
### 암묵적 규칙

기본적으로 필드가 없거나 빈 문자열이면 일반 검증 규칙(커스텀 포함)은 실행되지 않습니다. 예를 들어 `unique` 규칙은 빈 문자열에 대해 검증하지 않습니다:

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

커스텀 규칙을 빈 필드에도 적용하려면, 해당 규칙이 암묵적으로 필수임을 의미해야 합니다. `--implicit` 옵션으로 규칙 클래스를 생성할 수 있습니다:

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]  
> 암묵적 규칙은 필드를 필수라고 "암시"만 할 뿐, 실제로 필드가 없거나 빈 경우 실패시키는지 여부는 개발자가 구현해야 합니다.