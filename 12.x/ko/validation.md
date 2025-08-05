# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력 처리](#repopulating-forms)
    - [옵션 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가(Authorization)](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검증 입력값 준비하기](#preparing-input-for-validation)
- [Validator 수동 생성](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 에러 백](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [검증된 입력값 사용하기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성명 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 유효성 검증](#validating-nested-array-input)
    - [에러 메시지의 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저(Closure) 사용하기](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션으로 유입되는 데이터를 유효성 검증하는 여러 방법을 제공합니다. 일반적으로 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 가장 많이 사용합니다. 하지만 이 밖에도 다양한 유효성 검증 방법에 대해 다루겠습니다.

Laravel은 데이터에 적용 가능한 다양한 편리한 유효성 검증 규칙을 포함하고 있으며, 특정 데이터베이스 테이블에서 값의 유일성까지 검증할 수 있습니다. 이 모든 유효성 검증 규칙에 대해 자세히 설명하니 Laravel의 유효성 검증 기능을 잘 익힐 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 유효성 검증하고 에러 메시지를 사용자에게 표시하는 전체 예제를 살펴봅니다. 이 전체적인 절차를 통해 Laravel에서 요청 데이터를 어떻게 검증하는 지 감을 잡을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

여기서 `GET` 라우트는 사용자가 새로운 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음은 위 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러 예시입니다. `store` 메서드는 일단 비워두겠습니다.

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

이제 `store` 메서드에 새 블로그 포스트에 대한 유효성 검증 로직을 채워 넣을 차례입니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드가 정상적으로 계속 실행되며, 반대로 유효성 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 에러 응답이 자동으로 사용자에게 전송됩니다.

전통적인 HTTP 요청에서 유효성 검증에 실패하면, 이전 URL로 리다이렉트 응답이 자동으로 생성됩니다. 만약 들어온 요청이 XHR 요청인 경우, [유효성 검증 에러 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 좀 더 쉽게 이해하기 위해 아래와 같이 `store` 메서드를 채워 넣을 수 있습니다.

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

보시다시피, 유효성 검증 규칙은 `validate` 메서드에 전달됩니다. 사용 가능한 모든 유효성 검증 규칙은 [이곳](#available-validation-rules)에 문서화되어 있습니다. 다시 한 번 이야기하지만, 검증에서 실패하면 적절한 응답이 자동으로 만들어집니다. 통과하면 컨트롤러가 그대로 계속 실행됩니다.

또한, 검증 규칙은 하나의 `|`로 연결된 문자열이 아니라, 규칙들의 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, [이름이 지정된 에러 백](#named-error-bags)에 에러 메시지를 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단하기

때로는 한 속성(attribute)에서 첫 번째 검증 실패가 발생했다면, 남은 규칙 실행을 중단하고 싶을 수 있습니다. 이를 위해 해당 속성에 `bail` 규칙을 추가하세요.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서 `title` 속성의 `unique` 규칙이 통과하지 못하면, 그 뒤의 `max` 규칙은 아예 검사하지 않습니다. 검증 규칙은 지정한 순서대로 실행됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

들어오는 HTTP 요청에 "중첩(nested)" 필드 데이터가 포함된 경우, "점(dot) 표기법"을 사용해 해당 필드를 유효성 검증 규칙에 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 만약 필드 이름에 실제 마침표가 있을 때는 백슬래시로 마침표를 이스케이프하면 "점 표기법" 구문으로 인식되는 것을 방지할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

만약 들어온 요청의 필드가 주어진 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 이전에 언급했듯이, Laravel은 사용자를 이전 위치로 자동 리다이렉트 시킵니다. 그리고 모든 유효성 검증 에러와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 [세션에 플래시(flash)](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 모든 뷰에 `$errors` 변수를 공유해줍니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있기 때문에, `$errors` 변수는 항상 사용할 수 있다고 가정하고 뷰에서 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 더 자세한 방법은 [별도 문서](#working-with-error-messages)를 참고하세요.

따라서 유효성 검증 실패 시, 사용자는 컨트롤러의 `create` 메서드로 리다이렉트 되어 뷰에서 에러 메시지를 표시할 수 있습니다.

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

Laravel의 내장 유효성 검증 규칙들은 모두 애플리케이션의 `lang/en/validation.php` 파일에 에러 메시지가 정의되어 있습니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에서는 각각의 유효성 검증 규칙에 해당하는 번역 메시지를 확인할 수 있습니다. 필요에 따라 메시지를 자유롭게 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리에 복사하여 애플리케이션의 필요에 맞게 다국어 지원도 할 수 있습니다. Laravel의 로컬라이제이션 관련 자세한 내용은 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 커스터마이즈 하고 싶다면, `lang:publish` Artisan 명령어로 퍼블리시하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이번 예제에서는 전통적인 폼을 통해 데이터를 전송했습니다. 하지만, 많은 애플리케이션은 JavaScript 기반 프론트엔드에서 XHR 요청을 받기도 합니다. XHR 요청에서 `validate` 메서드를 사용할 경우, Laravel은 리다이렉트 응답을 보내지 않고, [유효성 검증 에러 메시지가 포함된 JSON 응답](#validation-error-response-format)을 반환합니다. 이 때 HTTP 상태 코드는 422입니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성에 대해 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하고 싶다면, [Blade](/docs/12.x/blade)의 `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 안에서는 `$message` 변수를 출력하여 에러 메시지를 표시합니다.

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

[이름이 지정된 에러 백](#named-error-bags)을 사용하는 경우, 두 번째 인자로 에러 백 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력 처리

Laravel은 유효성 검증 에러로 인한 리다이렉션 시 모든 요청 입력값을 [세션에 플래시](/docs/12.x/session#flash-data)합니다. 이렇게 하면 사용자가 제출을 시도했던 입력값을 다음 요청에서 쉽게 접근하고, 폼을 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하세요. 이 메서드는 [세션](/docs/12.x/session)에 저장된 이전 입력값을 가져옵니다.

```php
$title = $request->old('title');
```

또한, 글로벌 헬퍼 함수인 `old`도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 폼을 다시 채울 때 훨씬 편리하게 사용할 수 있습니다. 해당 필드에 저장된 이전 입력값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 참고 사항

기본적으로 Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함하고 있습니다. 이로 인해 "옵션" 필드에 대해 유효성 검증 시 `null` 값이 유효하지 않게 되므로, `nullable` 규칙을 꼭 추가해줘야 합니다. 예를 들면,

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예시에서 `publish_at` 필드는 `null`이거나 유효한 날짜여야 합니다. 만약 `nullable`을 명시하지 않으면 `null` 값은 무효한 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대할 때, Laravel은 자동으로 에러 메시지들을 포맷해서 `422 Unprocessable Entity` 응답을 반환합니다.

아래는 유효성 검증 에러에 대한 JSON 응답 예시입니다. 중첩된 에러 키는 "dot" 표기법으로 평탄화됩니다.

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
## 폼 리퀘스트 유효성 검증 (Form Request Validation)

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성하기

더 복잡한 유효성 검증이 필요한 상황이라면 "폼 리퀘스트(form request)"를 만들 수 있습니다. 폼 리퀘스트는 자체적으로 유효성 검증과 인가 로직을 캡슐화한 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스는 `make:request` Artisan CLI 명령어로 생성할 수 있습니다.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 생성됩니다. 이 디렉터리가 없으면 명령어 실행 시 자동으로 만들어집니다. Laravel에서 생성되는 각 폼 리퀘스트에는 `authorize`와 `rules` 두 가지 메서드가 기본으로 포함되어 있습니다.

`authorize` 메서드는 현재 인증된 사용자가 요청된 작업을 수행할 수 있는지 판단하고, `rules` 메서드는 해당 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드의 시그니처 내에 필요한 의존성을 타입힌트로 지정할 수 있으며, [서비스 컨테이너](/docs/12.x/container)에서 자동으로 주입됩니다.

유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 해당 요청을 타입힌트로 받기만 하면 됩니다. 폼 리퀘스트는 컨트롤러 메서드가 실행되기 전에 자동으로 검증을 처리하므로, 컨트롤러 내에서 직접 검증 코드를 작성할 필요가 없습니다.

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

유효성 검증에 실패하면, 사용자를 이전 위치로 돌려보내는 리다이렉트 응답이 자동 생성됩니다. 에러는 세션에 플래시되어 뷰에서 사용할 수 있습니다. 요청이 XHR(ajax) 요청이었다면 422 상태 코드와 [유효성 검증 에러의 JSON 표현](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 프론트엔드에 실시간 폼 리퀘스트 유효성 검증이 필요하다면 [Laravel Precognition](/docs/12.x/precognition)을 확인해 보세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행

초기 유효성 검증이 끝난 뒤에 추가 검증이 필요한 경우, 폼 리퀘스트의 `after` 메서드를 활용할 수 있습니다.

`after` 메서드는 콜러블(클로저 또는 호출 가능한 객체)의 배열을 반환해야 하며, 이들은 검증이 완료된 후 호출됩니다. 콜러블로 전달되는 파라미터는 `Illuminate\Validation\Validator` 인스턴스이며, 필요 시 추가 에러 메시지를 수동으로 넣을 수 있습니다.

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

위 예시에서 보듯, `after` 메서드에서 반환된 배열에는 호출 가능한 클래스도 포함될 수 있습니다. 이런 클래스의 `__invoke` 메서드 역시 `Illuminate\Validation\Validator` 인스턴스를 파라미터로 받습니다.

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
#### 첫 번째 유효성 검증 실패 시 전체 중단

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 한 번이라도 유효성 검증이 실패하면 모든 속성에 대해 남은 검증을 즉시 중단합니다.

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이징

폼 리퀘스트 유효성 검증 실패 시 사용자를 이전 위치로 리다이렉트합니다. 하지만, 이를 자유롭게 바꿀 수 있습니다. `$redirect` 프로퍼티를 추가하세요.

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

이름이 지정된 라우트로 리다이렉트 하려면 `$redirectRoute` 프로퍼티를 사용하세요.

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가(Authorization)

폼 리퀘스트 클래스에는 `authorize` 메서드도 있습니다. 이 메서드 내에서 인증된 사용자가 해당 리소스를 업데이트할 권한이 실제로 있는지 검사할 수 있습니다. 예를 들어, 사용자가 블로그 댓글을 실제로 소유하고 있는지 확인할 수 있습니다. 대부분의 경우, 여기서 [인가(Gate/Policy)](/docs/12.x/authorization)와 상호작용하게 됩니다.

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

폼 리퀘스트는 Laravel의 기본 Request 클래스를 상속하므로, 현재 인증된 사용자를 `user` 메서드로 접근할 수 있습니다. 또한 위 예시의 `route` 메서드를 통해 라우트에서 정의된 URI 파라미터(예: `{comment}`)에 접근할 수 있습니다.

```php
Route::post('/comment/{comment}');
```

만약 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용한다면, 코드가 더 간결해질 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, 403 상태 코드와 함께 HTTP 응답이 생성되고 컨트롤러 메서드는 실행되지 않습니다.

만약 인가 로직을 폼 리퀘스트밖의 다른 부분에서 처리한다면, `authorize` 메서드를 제거하거나 무조건 `true`를 반환하면 됩니다.

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
> `authorize` 메서드의 시그니처에도 필요한 의존성을 타입힌트로 지정할 수 있으며, [서비스 컨테이너](/docs/12.x/container)에서 자동으로 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

폼 리퀘스트가 사용할 에러 메시지를 `messages` 메서드를 오버라이드 하여 커스터마이즈 할 수 있습니다. 이 메서드는 속성/규칙 쌍별로 해당 에러 메시지를 반환하는 배열이어야 합니다.

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
#### 유효성 검증 속성명 커스터마이즈

Laravel의 많은 내장 형식 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 이 자리에 원하는 속성명이 들어가게 하려면 `attributes` 메서드를 오버라이드하세요. 이 메서드는 속성/커스텀명 쌍을 반환해야 합니다.

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
### 유효성 검증 입력값 준비하기

유효성 검증 규칙 적용 전에 데이터를 전처리하거나 정제(sanitize)해야 하는 경우 `prepareForValidation` 메서드를 사용할 수 있습니다.

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

마찬가지로, 유효성 검증 이후에 요청 데이터를 정규화(normalize)해야 한다면 `passedValidation` 메서드를 사용할 수 있습니다.

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
## Validator 수동 생성 (Manually Creating Validators)

`validate` 메서드를 사용하지 않고 직접 Validator 인스턴스를 만들어 검증을 수행할 수도 있습니다. `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 사용하세요.

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

`make` 메서드의 첫 번째 인자는 검증 대상 데이터, 두 번째 인자는 적용할 유효성 검증 규칙 배열입니다.

검증 실패 여부가 결정된 후에는 `withErrors` 메서드로 에러 메시지를 세션에 플래시할 수 있습니다. 이 방법을 사용할 경우, 리다이렉트 후에 `$errors` 변수가 자동으로 뷰에 전달되어 사용자에게 쉽게 표시할 수 있습니다. `withErrors`에는 Validator, `MessageBag`, PHP 배열 모두 전달 가능합니다.

#### 첫 번째 유효성 검증 실패 시 전체 중단

`stopOnFirstFailure` 메서드를 사용하면 한번이라도 실패가 발생하면 해당 Validator 전체에서 검증을 중단합니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

수동으로 Validator 인스턴스를 생성하더라도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션을 그대로 사용할 수 있습니다. Validator 인스턴스에서 `validate` 메서드를 호출하면, 유효성 검증에 실패할 경우 자동으로 리다이렉트(또는 XHR라면 [JSON 응답](#validation-error-response-format))됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

검증 실패 시 [이름이 지정된 에러 백](#named-error-bags)에 에러를 넣고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러 백

한 페이지에 여러 개의 폼이 있다면, 에러 메시지를 특정 폼에만 표시하고 싶을 수 있습니다. 이를 위해 두 번째 인자에 이름을 지정하여 `withErrors`를 사용하면 됩니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이렇게 하면 `$errors` 변수에서 해당 이름에 해당하는 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요하다면, Validator 인스턴스가 사용할 커스텀 에러 메시지를 Laravel이 제공하는 기본 에러 메시지 대신 지정할 수 있습니다. 방법은 여러 가지가 있는데, 첫번째는 `Validator::make` 메서드의 세 번째 인자로 메시지 배열을 전달하는 것입니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예시에서 `:attribute`는 실제 필드 이름으로 치환됩니다. 다른 플레이스홀더도 사용할 수 있습니다.

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

특정 속성에 대해서만 커스텀 메시지를 지정하려면 "dot" 표기법을 사용하세요. 속성 이름 뒤에 규칙 이름을 붙여 배열의 키로 사용합니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

많은 내장 에러 메시지는 `:attribute` 플레이스홀더를 포함하는데, 필드명 대신 표시될 값 역시 변경할 수 있습니다. 네 번째 인자로 커스텀 속성명 배열을 전달하세요.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행

초기 유효성 검증 후 추가적인 검증을 해야 할 때 Validator의 `after` 메서드를 사용할 수 있습니다. 이 메서드는 클로저 또는 콜러블 배열을 인자로 받으며, 검증 완료 후 호출됩니다.

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

별도의 클래스에서 "after" 검증 로직을 정의했다면 콜러블 클래스를 배열로 전달할 수도 있습니다. 이런 클래스는 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받습니다.

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
## 검증된 입력값 사용하기 (Working With Validated Input)

폼 리퀘스트 또는 커스텀 Validator 인스턴스로 들어오는 요청 데이터를 검증한 후, 실제로 검증이 적용된 데이터를 추출하고 싶을 수 있습니다. 여러 가지 방법이 있습니다. 폼 리퀘스트나 Validator 인스턴스의 `validated` 메서드를 호출하면 검증된 데이터 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출할 수 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하며, 이 객체의 `only`, `except`, `all` 메서드로 데이터의 일부 혹은 전체를 추출할 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 순회하거나 접근할 수도 있습니다.

```php
// 검증된 데이터 순회
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 값 접근
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 필드를 추가하려면 `merge` 메서드를 사용하세요.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 객체로 받고 싶다면 `collect` 메서드를 호출하세요.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기 (Working With Error Messages)

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. `$errors` 변수 역시 이 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

`first` 메서드를 사용하면 특정 필드의 첫 번째 에러 메시지를 가져옵니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

`get` 메서드를 사용하면 특정 필드의 모든 메시지를 배열로 반환합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 폼 필드라면 `*` 문자를 이용하여 각 요소의 모든 메시지를 한 번에 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 에러 메시지 전부 가져오기

`all` 메서드를 사용하면 모든 필드의 모든 메시지를 배열로 반환합니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지가 있는지 확인

`has` 메서드를 통해 해당 필드에 에러 메시지가 존재하는지 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel의 내장 유효성 검증 규칙의 각 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

각 규칙별로 번역 메시지를 이 파일에서 자유롭게 변경할 수 있고, 다국어를 위해 다른 언어 디렉터리로 복사해서 사용할 수도 있습니다. 더 자세한 사항은 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션에는 `lang` 디렉터리가 없습니다. 언어 파일이 필요하다면 `lang:publish` 명령어로 퍼블리시 하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성/규칙별 커스텀 메시지

특정 속성과 규칙 조합에 대해 에러 메시지를 언어 파일의 `custom` 배열에 지정할 수 있습니다.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성명 지정하기

내장 에러 메시지의 `:attribute` 자리에 표시될 속성명을 `attributes` 배열에 지정할 수 있습니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션에는 `lang` 디렉터리가 없습니다. 언어 파일이 필요하다면 `lang:publish` 명령어로 퍼블리시 하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 내장 유효성 검증 에러 메시지는 `:value` 플레이스홀더를 포함합니다. 특정 필드의 값에 대해 좀 더 읽기 쉬운 표현으로 대체하고 싶다면, `values` 배열에 정의할 수 있습니다. 예를 들어, `payment_type` 값이 `cc`일 때, 사용자에게 "credit card"라고 표시하고 싶다면 아래와 같이 작성합니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션에는 `lang` 디렉터리가 없습니다. 언어 파일이 필요하다면 `lang:publish` 명령어로 퍼블리시 하세요.

위처럼 값을 정의하면 에러 메시지에서 `"payment type is credit card"`와 같이 좀 더 친절하게 보이게 됩니다.

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙 (Available Validation Rules)

아래는 Laravel에서 사용할 수 있는 모든 유효성 검증 규칙들과 그 기능을 정리한 목록입니다.

#### 불린(Boolean) 관련

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### 문자열(String) 관련

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

#### 숫자(Number) 관련

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

#### 배열(Array) 관련

<div class="collection-method-list" markdown="1">

[Array](#rule-array)
[Between](#rule-between)
[Contains](#rule-contains)
[Doesnt Contain](#rule-doesnt-contain)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)

</div>

#### 날짜(Date) 관련

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

#### 파일(File) 관련

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

#### 데이터베이스(Database) 관련

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

...  
(이하의 유효성 검증 규칙별 상세 설명 및 사용법, 조건부 규칙/배열/파일/비밀번호/커스텀 검증 등, 상세 규칙 목록은 원본의 순서와 구조를 유지해서 전항을 한글로 자연스럽고 명확하게 번역해야 하며, 코드ㆍ파라미터ㆍ예시 블록 등은 절대 번역하지 않고 원본 그대로 출력해야 합니다.  
너무 길어질 경우 나머지 규칙별 설명은 이어서 출력하겠습니다.)
