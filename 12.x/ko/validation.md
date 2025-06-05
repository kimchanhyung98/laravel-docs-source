# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [선택적 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 포맷](#validation-error-response-format)
- [폼 요청(Form Request) 유효성 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 권한 부여](#authorizing-form-requests)
    - [에러 메시지 커스터마이즈하기](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 에러 백](#named-error-bags)
    - [에러 메시지 커스터마이즈하기](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [유효성 검증된 입력값 사용하기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부로 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력 검증](#validating-nested-array-input)
    - [에러 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저(Closure) 사용하기](#using-closures)
    - [암묵적 규칙 사용하기](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터의 유효성을 검증하는 다양한 방법을 제공합니다. 가장 일반적으로는 모든 HTTP 요청 객체에 사용할 수 있는 `validate` 메서드를 많이 사용합니다. 이 문서에서는 그 외에도 여러 가지 검증 방식에 대해 설명합니다.

라라벨은 데이터에 적용할 수 있는 다양한 편리한 유효성 검증 규칙을 내장하고 있습니다. 예를 들어, 값이 데이터베이스의 특정 테이블에서 고유한지 검사하는 기능도 제공합니다. 이 문서에서는 이러한 모든 검증 규칙에 대해 하나씩 자세히 다루어, 라라벨의 유효성 검증 기능을 충분히 익힐 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기

라라벨의 강력한 유효성 검증 기능을 빠르게 익혀보기 위해, 이번에는 폼 데이터를 검증하고 에러 메시지를 사용자에게 되돌려 보여주는 완벽한 예시를 살펴봅니다. 이 과정을 통해 라라벨로 들어오는 요청 데이터를 어떻게 유효성 검증하는지 큰 흐름을 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 아래와 같은 라우트가 정의되어 있다고 가정해봅니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새로운 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 그 포스트를 데이터베이스에 저장하는 역할을 합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

이제 위의 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 우선 `store` 메서드는 비워두었습니다.

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

이제 `store` 메서드에 새로운 블로그 포스트의 유효성 검증 로직을 추가해 보겠습니다. 여기서는 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 유효성 검증 규칙에 통과하면, 코드는 정상적으로 계속 실행되고, 유효성 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 자동으로 발생하면서 적절한 에러 응답이 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 유효성 검증에 실패한 경우, 이전 URL로 리디렉션하는 응답이 생성됩니다. 만약 들어오는 요청이 XHR 요청이라면, [유효성 검증 에러 메시지가 담긴 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작을 좀 더 자세히 알아보기 위해, 다시 `store` 메서드를 살펴봅니다.

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

보시다시피, 유효성 검증 규칙을 `validate` 메서드에 전달합니다. 모든 유효성 검증 규칙은 [공식 문서](#available-validation-rules)에서 자세히 소개되어 있으니 참고하셔도 됩니다. 다시 한 번, 검증에 실패하면 라라벨이 자동으로 올바른 응답을 생성합니다. 검증에 성공하면 컨트롤러는 정상적으로 이어서 실행됩니다.

또한, 유효성 규칙을 `|` 문자를 기준으로 나열하는 대신, 배열 형태로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, `validateWithBag` 메서드를 사용하면 [이름이 지정된 에러 백](#named-error-bags)에 에러 메시지를 저장할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

특정 속성에 대해 첫 번째 규칙이 실패하면, 이후 규칙을 더 이상 검사하지 않고 멈추고 싶을 때가 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서는 `title`에 대해 `unique` 규칙이 실패하면, 그 뒤의 `max` 규칙은 검사되지 않습니다. 규칙들은 정의한 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes)에 대한 참고 사항

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있으면, "dot" 구문(점 표기법)을 사용해서 검증 규칙을 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 만약 필드 이름 자체에 실제로 점(`.`)이 포함되어 있는데 dot 구문으로 해석되지 않게 하려면, 점을 역슬래시(`\`)로 이스케이프 해주면 됩니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

그렇다면, 만약 요청된 필드 값이 지정된 규칙을 통과하지 못했다면 어떻게 될까요? 앞서 언급한 것처럼, 라라벨은 자동으로 사용자를 이전 위치로 리디렉션합니다. 그리고 모든 유효성 검증 에러와 [요청 입력 값](/docs/12.x/requests#retrieving-old-input)은 세션에 [flash 데이터로 저장](https://laravel.com/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 모든 뷰에 `$errors` 변수를 공유합니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있으므로, 뷰에서 언제나 `$errors` 변수가 정의되어 있다고 가정할 수 있고 안전하게 사용할 수 있습니다. `$errors`는 `Illuminate\Support\MessageBag` 클래스의 인스턴스입니다. 이 객체를 다루는 방법은 [관련 문서](#working-with-error-messages)를 참고하세요.

따라서 예시에서 사용자가 유효성 검증에 실패하면, 컨트롤러의 `create` 메서드로 리디렉션되고, 뷰에서 아래처럼 에러 메시지를 출력할 수 있습니다.

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

라라벨의 내장 유효성 검증 규칙은 각각 오류 메시지가 `lang/en/validation.php` 파일에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에서 각 검증 규칙에 대한 메시지를 확인할 수 있습니다. 애플리케이션의 상황에 맞게 이 메시지들을 자유롭게 수정하거나 변경할 수 있습니다.

또한, 다른 언어로 메시지를 번역하려면 이 파일을 언어별 디렉터리에 복사하여 사용할 수 있습니다. 라라벨의 로컬라이제이션에 대해 더 자세히 알고 싶다면, [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 구조에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령을 사용하여 해당 파일들을 복사해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이 예시에서는 전통적인 폼을 사용하여 데이터를 애플리케이션에 전달했습니다. 그러나, 실제로는 자바스크립트 프론트엔드에서 XHR 요청을 보내는 경우가 많습니다. XHR 요청에서 `validate` 메서드를 사용할 때, 라라벨은 리디렉션 응답을 생성하지 않습니다. 대신, [모든 유효성 검증 에러가 포함된 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답의 HTTP 상태 코드는 422입니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

[Blade](/docs/12.x/blade)의 `@error` 디렉티브를 사용하면 특정 속성에 대한 유효성 검증 에러 메시지가 존재하는지 빠르게 확인할 수 있습니다. `@error` 블록 내에서는 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다.

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

[이름이 지정된 에러 백](#named-error-bags)을 사용 중인 경우, `@error` 디렉티브의 두 번째 인자로 에러 백의 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

유효성 검증 에러로 인해 라라벨이 리디렉션 응답을 생성하면, 프레임워크는 요청의 모든 입력값을 자동으로 [세션에 flash 데이터로 저장](https://laravel.com/docs/12.x/session#flash-data)합니다. 이렇게 하면 사용자가 제출하려 했던 폼을 다시 보여주면서 입력값을 쉽게 복원할 수 있습니다.

이전 요청에서 flash 된 입력값을 가져오고 싶다면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 됩니다. `old` 메서드는 세션에 저장된 이전 입력 데이터를 반환합니다.

```php
$title = $request->old('title');
```

라라벨은 글로벌 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/12.x/blade) 안에서 예전 입력값을 출력할 때, 이 헬퍼를 쓰면 더욱 편리하게 폼을 다시 채울 수 있습니다. 해당 필드에 이전 입력값이 없다면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 참고 사항

라라벨은 기본적으로 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 전역 미들웨어 스택에 포함하고 있습니다. 이로 인해, "선택적" 요청 필드는 `nullable`로 지정해주지 않으면 `null` 값이 유효하지 않은 것으로 간주될 수 있습니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서는 `publish_at` 필드가 `null`이거나 올바른 날짜 형식이어야 함을 지정했습니다. 만약 규칙 정의에서 `nullable` 수정자를 빼면, 해당 필드가 `null`일 경우 잘못된 날짜로 판정됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고 들어오는 HTTP 요청이 JSON 응답을 기대할 경우, 라라벨은 에러 메시지들을 자동으로 포매팅해서 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래는 유효성 검증 에러의 JSON 응답 포맷 예시입니다. 중첩된 에러 키는 "dot" 표기법으로 평탄화됩니다.

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
## 폼 요청(Form Request) 유효성 검증

<a name="creating-form-requests"></a>
### 폼 요청 생성하기

좀 더 복잡한 유효성 검증이 필요한 경우, "폼 요청(form request)"을 사용할 수 있습니다. 폼 요청은 자체적으로 유효성 검증과 인가(authorization) 로직을 캡슐화하는 커스텀 요청 클래스입니다. 폼 요청 클래스를 생성하려면, `make:request` Artisan CLI 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 이 디렉터리가 없다면 명령어 실행 시 자동으로 생성됩니다. 라라벨이 생성한 각 폼 요청에는 `authorize`와 `rules`라는 두 가지 메서드가 포함되어 있습니다.

예상할 수 있듯, `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 나타내는 작업을 수행할 수 있는지를 결정하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드의 시그니처에서 필요한 의존성을 타입힌트로 명시할 수 있습니다. 그러면 라라벨 [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해 줍니다.

그렇다면 유효성 검증 규칙은 언제 적용될까요? 컨트롤러 메서드의 요청 파라미터로 form request 타입을 명시(type-hint)하기만 하면 됩니다. 즉, 요청이 컨트롤러 메서드에 도달하기 전에 폼 요청 클래스가 자동으로 유효성 검증을 수행하므로, 컨트롤러 내부에 검증 코드를 작성할 필요가 없습니다.

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

유효성 검증이 실패하면, 자동으로 사용자를 이전 위치로 리디렉션하는 응답이 생성됩니다. 에러도 세션에 flash 되어 화면에 표시할 수 있습니다. XHR 요청인 경우, 422 상태 코드의 HTTP 응답과 함께 [유효성 검증 에러의 JSON 포맷](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에 실시간 form request 유효성 검증을 추가하고 싶으신가요? [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 폼 요청에서 추가 유효성 검증 수행하기

기본 유효성 검증이 끝난 후, 추가적인 검증이 필요한 경우가 있습니다. 폼 요청의 `after` 메서드를 사용하면 이를 구현할 수 있습니다.

`after` 메서드는 검증이 끝난 뒤 호출될 콜러블(callable) 또는 클로저의 배열을 반환해야 합니다. 각 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 전달되며, 필요하다면 이를 통해 추가 에러 메시지를 등록할 수 있습니다.

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

위에서 보듯, `after` 메서드가 반환하는 배열에 인보커블(invokable) 클래스를 담을 수도 있습니다. 이러한 클래스의 `__invoke` 메서드에도 `Illuminate\Validation\Validator` 인스턴스가 전달됩니다.

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
#### 첫 번째 유효성 검증 실패 시 전체 검증 중단하기

폼 요청 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 하나의 유효성 검증 실패가 발생한 뒤부터 모든 속성에 대한 검증을 멈추도록 할 수 있습니다.

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이즈하기

폼 요청의 유효성 검증이 실패할 때, 기본적으로는 사용자를 이전 위치로 리디렉션하지만, 이 동작은 자유롭게 커스터마이즈할 수 있습니다. `$redirect` 프로퍼티를 폼 요청에 정의하면 됩니다.

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 특정 라우트 이름으로 리디렉션하고 싶다면 `$redirectRoute` 프로퍼티를 사용하면 됩니다.

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 권한 부여

폼 요청 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 안에서는 인증된 사용자가 실제로 특정 리소스를 업데이트할 권한이 있는지를 판단할 수 있습니다. 예를 들어, 사용자가 블로그 댓글을 수정하려고 할 때, 권한이 있는 사용자인지 검사할 수 있습니다. 보통 이곳에서는 [인가 게이트(gate)나 정책(policy)](/docs/12.x/authorization)와 상호작용하게 됩니다.

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

모든 폼 요청 클래스는 기본 라라벨 Request 클래스를 상속하므로, `user` 메서드로 현재 인증된 사용자에 접근할 수 있습니다. 또한, 위 예시의 `route` 메서드처럼 현재 라우트에서 정의된 URI 파라미터(예: 아래 예시의 `{comment}`처럼)에도 접근할 수 있습니다.

```php
Route::post('/comment/{comment}');
```

따라서, [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하고 있다면, 폼 요청에서 바인딩된 모델을 속성처럼 쉽게 접근하여 코드를 더욱 간결하게 작성할 수도 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, 자동으로 403 상태 코드의 HTTP 응답이 반환되고 컨트롤러 메서드는 실행되지 않습니다.

요청에 대한 인가 로직을 다른 부분에서 처리하려면, `authorize` 메서드를 아예 제거하거나 단순히 `true`를 반환해도 됩니다.

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
> `authorize` 메서드의 시그니처에 필요한 의존성을 타입힌트로 명시할 수 있습니다. 그러면 라라벨 [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해 줍니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈하기

폼 요청의 `messages` 메서드를 오버라이드하여 에러 메시지를 커스터마이즈할 수 있습니다. 이 메서드는 속성/규칙 쌍과 해당 에러 메시지의 배열을 반환해야 합니다.

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
#### 유효성 검증 속성 커스터마이즈하기

라라벨의 내장 유효성 검증 메시지에는 종종 `:attribute` 플레이스홀더가 포함됩니다. 이 플레이스홀더가 에러 메시지 내에서 커스텀 속성명으로 대체되기를 원한다면 `attributes` 메서드를 오버라이드하여 속성/이름 쌍의 배열을 반환하면 됩니다.

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
### 유효성 검증을 위한 입력값 준비하기

유효성 검증 규칙을 적용하기 전에, 요청 데이터의 전처리나 정제가 필요하다면, `prepareForValidation` 메서드를 활용할 수 있습니다.

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

마찬가지로, 유효성 검증이 끝난 후에 요청 데이터를 정규화할 필요가 있다면, `passedValidation` 메서드를 사용할 수 있습니다.

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

## 수동으로 Validator 인스턴스 생성하기

요청 객체의 `validate` 메서드를 사용하지 않고, 직접 `Validator` [파사드](/docs/12.x/facades)를 이용해 validator 인스턴스를 생성할 수 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트를 저장합니다.
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

        // 검증된 입력값을 가져옵니다...
        $validated = $validator->validated();

        // 검증된 입력값의 일부만 가져옵니다...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트를 저장합니다...

        return redirect('/posts');
    }
}
```

`make` 메서드에 첫 번째 인수로는 검증 대상 데이터, 두 번째 인수로는 해당 데이터에 적용할 유효성 검증 규칙의 배열을 전달합니다.

요청 유효성 검증에 실패한 경우, `withErrors` 메서드를 사용해 오류 메시지를 세션에 플래시할 수 있습니다. 이 방법을 사용하면, `$errors` 변수는 리다이렉션 후 뷰(view)에서도 자동으로 사용할 수 있으므로, 사용자가 오류 메시지를 쉽게 확인할 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP 배열을 인수로 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 중단하기

`stopOnFirstFailure` 메서드는 한 번이라도 검증에 실패하면 이후 모든 속성의 검증을 중단하도록 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

직접 validator 인스턴스를 생성하되, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능도 활용하고 싶다면, 이미 생성한 validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 검증에 실패하면 사용자는 자동으로 리다이렉트되고, XHR 요청의 경우 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

검증 실패 시 오류 메시지를 [이름이 지정된 오류 가방(namded error bag)](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 오류 가방 (Named Error Bags)

한 페이지에 여러 개의 폼이 있는 경우, 각 폼에 대한 오류 메시지를 쉽게 구분해 가져오기 위해 `MessageBag`에 이름을 붙이고 싶을 수 있습니다. 이를 위해 `withErrors`의 두 번째 인수로 원하는 이름을 전달하면 됩니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이제 `$errors` 변수에서 이름이 지정된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

필요하다면 라라벨이 제공하는 기본 오류 메시지 대신, validator 인스턴스가 사용할 사용자 정의 오류 메시지를 지정할 수 있습니다. 커스텀 메시지 지정 방법은 몇 가지가 있습니다. 먼저, `Validator::make` 메서드의 세 번째 인수로 커스텀 메시지 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예시에서 `:attribute` 플레이스홀더는 검증 중인 실제 필드명으로 치환됩니다. 유효성 메시지에서는 이 외에도 다양한 플레이스홀더를 사용할 수 있습니다. 예를 들면 다음과 같습니다.

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성의 커스텀 메시지 지정

특정 속성에 대해서만 커스텀 오류 메시지를 지정하고 싶을 때는 "dot" 표기법을 사용하면 됩니다. 속성명을 먼저 쓰고, 이어서 규칙명을 점으로 이어서 작성합니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정하기

라라벨의 기본 오류 메시지 대부분에는 `:attribute` 플레이스홀더가 포함되어 있으며, 실제 검증하는 필드의 이름으로 치환됩니다. 특정 필드에 대해 이 플레이스홀더에 들어갈 이름을 커스텀으로 지정하려면, `Validator::make`의 네 번째 인수로 커스텀 속성명 배열을 넘겨주면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검사 수행하기

초기 유효성 검증이 끝난 뒤, 추가적인 검증을 수행해야 할 때도 있습니다. 이럴 때는 validator의 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 클로저나 콜러블(callable) 배열을 인수로 받아, 검증이 완료된 후 호출해 줍니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아, 필요하다면 추가 오류 메시지를 발생시킬 수 있습니다.

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

앞서 설명한 것처럼, `after` 메서드는 콜러블의 배열도 받을 수 있습니다. 이는 "추가 검증" 로직을 호출 가능한 클래스(인보커블 클래스)로 캡슐화했다면 특히 편리합니다. 이 클래스들은 `__invoke` 메서드로 `Illuminate\Validation\Validator` 인스턴스를 받게 됩니다.

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
## 검증된 입력값 다루기

폼 요청이나 직접 생성한 validator 인스턴스에서 요청 데이터를 검증한 후, 실제로 검증을 거친 데이터를 따로 가져오고 싶을 수 있습니다. 몇 가지 방법이 있는데, 먼저 폼 요청 또는 validator 인스턴스에서 `validated` 메서드를 호출하면 검증된 데이터의 배열이 반환됩니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 요청이나 validator 인스턴스에서 `safe` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. return된 객체는 `only`, `except`, `all` 메서드를 제공하여, 검증된 데이터의 일부 또는 전체를 손쉽게 가져올 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나 배열 인덱스로 접근할 수 있습니다.

```php
// 검증된 데이터 반복 처리...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열 인덱스로 접근하기...
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 더하고 싶다면, `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 받고 싶을 때는, `collect` 메서드를 사용합니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 오류 메시지 처리 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 모든 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 오류 메시지 가져오기

특정 필드에 대한 첫 번째 오류 메시지를 얻으려면, `first` 메서드를 사용합니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

특정 필드의 모든 오류 메시지를 배열로 받고 싶을 때는, `get` 메서드를 사용합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 입력 필드를 검증하는 경우, `*` 문자를 사용해 각 배열 요소의 모든 메시지를 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 오류 메시지 전체 가져오기

모든 필드에 대한 오류 메시지를 배열로 얻으려면, `all` 메서드를 사용합니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 오류 메시지가 있는지 확인하기

`has` 메서드를 사용하면 특정 필드에 오류 메시지가 존재하는지 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정

라라벨의 기본 유효성 검사 규칙은 각 오류 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 위치해 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어를 사용해 생성할 수 있습니다.

`lang/en/validation.php` 파일에서는 각 검증 규칙별로 번역 메시지 항목을 확인할 수 있습니다. 필요에 따라 애플리케이션 요구에 맞게 이 메시지들을 자유롭게 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉토리로 복사하여, 애플리케이션 언어에 맞게 메시지를 번역할 수 있습니다. 라라벨의 로컬라이제이션에 대해 자세히 알아보려면 [로컬라이제이션 전체 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴드에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 퍼블리시해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션의 유효성 검증 언어 파일에서, 특정 속성과 규칙 조합에 대한 오류 메시지를 커스터마이즈할 수 있습니다. 이를 위해 `lang/xx/validation.php`의 `custom` 배열에 직접 메시지를 추가하면 됩니다.

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

라라벨의 기본 오류 메시지 중 상당수는 `:attribute` 플레이스홀더를 포함하며, 검증하는 필드명이나 속성명으로 대체됩니다. 이 플레이스홀더가 사용자 정의 값으로 치환되도록 하려면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 커스텀 속성명을 지정하면 됩니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴드에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 퍼블리시해야 합니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 라라벨의 기본 유효성 규칙 오류 메시지에는 `:value` 플레이스홀더가 있으며, 해당 필드의 현재 값으로 치환됩니다. 그러나 때로는 이 값 대신 더 사용자 친화적인 값을 표시하고 싶을 수 있습니다. 예를 들어, 다음 규칙은 `payment_type`이 `cc`일 때 신용카드 번호를 요구합니다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 유효성 검사가 실패하면, 다음과 같은 오류 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

`cc` 값 대신 더 읽기 쉬운 표현을 표시하고 싶으면, `lang/xx/validation.php` 언어 파일의 `values` 배열에 다음과 같이 지정하면 됩니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴드에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 퍼블리시해야 합니다.

이 값을 정의한 후에는, 유효성 검증 실패 시 아래와 같은 오류 메시지가 표시됩니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙

아래는 사용할 수 있는 모든 유효성 검증 규칙과 그 기능에 대한 목록입니다.

#### Booleans(불리언)

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### Strings(문자열)

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

#### Numbers(숫자)

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

#### Arrays(배열)

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

#### Dates(날짜)

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

#### Files(파일)

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

#### Database(데이터베이스)

<div class="collection-method-list" markdown="1">

[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

#### Utilities(유틸리티)

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

검증 대상 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이어야 합니다. 이 규칙은 "이용 약관 동의"와 같은 필드 유효성 검사에 유용하게 사용할 수 있습니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

검증 대상 필드는, 추가로 지정한 다른 필드가 특정 값과 일치할 때 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이어야 합니다. 이 규칙 역시 "이용 약관 동의"나 비슷한 상황에서 유용하게 사용할 수 있습니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드는, PHP의 `dns_get_record` 함수 기준으로 올바른 A 또는 AAAA 레코드를 가져올 수 있는 유효한 값이어야 합니다. 제공된 URL의 호스트명은 PHP의 `parse_url` 함수로 추출된 후 `dns_get_record` 함수에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드는, 지정된 날짜 이후의 값이어야 합니다. 날짜들은 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스가 됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`이 평가할 날짜 문자열 대신, 비교 대상으로 사용할 다른 필드명을 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

편의를 위해, 날짜 기반 규칙은 유창한(fluid) `date` 규칙 빌더로도 생성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드를 통해 '오늘 이후' 또는 '오늘이거나 이후'를 표현할 수도 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>

#### after_or_equal:_date_

검증 대상 필드는 주어진 날짜와 같거나 그 이후의 값이어야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

날짜 기반 규칙은 아래와 같이 플루언트하게 `date` 규칙 빌더를 사용하여 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검증 규칙을 사용하면 검증 대상 필드가 제공된 여러 검증 규칙 집합 중 하나만 충족해도 통과하도록 지정할 수 있습니다. 예를 들어, 아래 규칙은 `username` 필드가 이메일 주소이거나, 최소 6자 이상의 영문자, 숫자, 대시(`-`)가 포함된 alpha-numeric 문자열 중 하나이어야 함을 검증합니다.

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

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) 에 포함된 유니코드 문자(알파벳 문자)로만 구성되어야 합니다.

ASCII 범위(`a-z`, `A-Z`)의 문자만 허용하려면 검증 규칙에 `ascii` 옵션을 추가하면 됩니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) 에 포함된 유니코드 영문자/숫자 또는 ASCII 대시(`-`), 밑줄(`_`) 문자로만 구성되어야 합니다.

ASCII 범위(`a-z`, `A-Z`, `0-9`)만 허용하려면 `ascii` 옵션을 추가하면 됩니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) 에 포함된 유니코드 영문자/숫자로만 구성되어야 합니다.

ASCII 범위(`a-z`, `A-Z`, `0-9`)만 허용하려면 `ascii` 옵션을 추가하세요.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 대상 필드는 PHP의 `array`여야 합니다.

`array` 규칙에 추가 값을 지정하면, 입력 배열 내 각 키가 규칙에 지정한 값 목록 내에 반드시 포함되어 있어야 합니다. 아래 예시에서 입력 배열의 `admin` 키는 `array` 규칙에 지정한 값 목록에 포함되어 있지 않기 때문에 유효하지 않습니다.

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

일반적으로, 배열 내에 허용할 키를 명확하게 지정하는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

검증 대상 필드는 반드시 7비트 ASCII 문자로만 이루어져야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드의 유효성 검사에서 첫 번째 실패가 발생하면, 그 이후의 규칙 검증을 중단합니다.

`bail` 규칙은 특정 필드에 대해 실패 시 그 필드의 추가 규칙 검증만 중단하지만, `stopOnFirstFailure` 메서드를 사용하면 하나라도 유효성 검증에 실패할 경우 모든 속성의 검증을 즉시 중단하게 할 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 대상 필드는 주어진 날짜 이전의 값이어야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다. 또한 [after](#rule-after) 규칙처럼, 검증 대상인 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

날짜 기반 규칙은 아래와 같이 플루언트하게 `date` 규칙 빌더를 사용하여 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`와 `todayOrBefore` 메서드를 사용하면, 쉽게 오늘 이전 또는 오늘 또는 그 이전만 허용하도록 규칙을 작성할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 대상 필드는 주어진 날짜와 같거나 그 이전의 값이어야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다. 또한 [after](#rule-after) 규칙처럼, 검증 대상인 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

날짜 기반 규칙은 아래와 같이 플루언트하게 `date` 규칙 빌더를 사용하여 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

검증 대상 필드는 _min_값과 _max_값 사이(포함)의 크기여야 합니다. 문자열, 숫자, 배열, 파일의 경우 [size](#rule-size) 규칙과 동일한 방식으로 평가합니다.

<a name="rule-boolean"></a>
#### boolean

검증 대상 필드는 불리언(boolean) 값으로 변환이 가능해야 합니다. 허용되는 입력 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드는 `{field}_confirmation` 필드와 값이 일치해야 합니다. 예를 들어, 검증하려는 필드가 `password`라면 `password_confirmation` 필드도 입력 데이터에 반드시 있어야 하며, 두 값이 동일해야 합니다.

맞춤 확인 필드명을 직접 지정할 수도 있습니다. 예를 들어, `confirmed:repeat_username`을 사용하면, `repeat_username` 필드가 검증 대상 필드와 동일한지 검사합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

검증 대상 필드는 주어진 값들을 모두 포함하는 배열이어야 합니다. 이 규칙은 종종 배열을 `implode`해서 사용해야 하므로, `Rule::contains` 메서드를 사용하면 더 간결하게 규칙을 작성할 수 있습니다.

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

검증 대상 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 파라미터로 [인증 가드](/docs/12.x/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 대상 필드는 PHP의 `strtotime` 함수 기준으로 유효한(상대적이지 않은) 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 대상 필드는 주어진 날짜와 정확히 같아야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 대상 필드는 주어진 _formats_ 중 하나와 반드시 일치해야 합니다. 한 필드에 대해 `date`와 `date_format` 중 **하나만** 사용해야 하며, 두 규칙을 동시에 적용해서는 안 됩니다. 이 유효성 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 포맷을 사용할 수 있습니다.

날짜 기반 규칙은 플루언트한 `date` 규칙 빌더로 아래와 같이 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

검증 대상 필드는 숫자여야 하며, 지정한 소수점 자리수를 반드시 가져야 합니다.

```php
// 소수점 두 자리(예: 9.99)만 허용...
'price' => 'decimal:2'

// 2자리에서 4자리까지의 소수점 허용...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

`anotherfield`값이 지정한 값과 같을 때, 검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드는 지정한 _field_와는 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수는 정확히 _value_ 길이(자리수)를 가져야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 대상 정수는 지정한 _min_~_max_ 길이(자리수) 내에 있어야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 규칙의 파라미터에 지정한 이미지 크기 조건을 충족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_

_ratio_ 제약 조건은 이미지의 가로/세로 비율로 설정할 수 있습니다. `3/2`와 같은 분수 또는 `1.5`와 같은 실수(float)로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

여러 인자를 전달해야 하므로, `Rule::dimensions` 메서드를 사용하면 더 편리하게 작성할 수 있습니다.

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

배열을 검증할 때, 해당 필드에는 중복 값이 없어야 합니다.

```php
'foo.*.id' => 'distinct'
```

`distinct`는 기본적으로 느슨한(loose) 비교를 사용합니다. 엄격한(strict) 비교를 사용하고 싶다면, `strict` 파라미터를 규칙에 추가하세요.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 구분 없이 비교하려면, `ignore_case`를 규칙 인자로 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값들 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값들 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 유효성 검사는 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 검증이 적용되며, 필요에 따라 다른 검증 스타일도 사용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예시는 `RFCValidation`과 `DNSCheckValidation` 검증을 모두 적용합니다. 사용할 수 있는 모든 검증 스타일은 아래와 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) 기준으로 이메일을 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) 기준으로, 경고(예: 마지막에 마침표, 연속된 마침표 등)가 있을 경우 실패합니다.
- `dns`: `DNSCheckValidation` - 이메일의 도메인에 유효한 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 호모그래프(homograph) 또는 속이는(deceptive) 유니코드 문자가 포함되어 있지 않은지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 유효한 이메일 주소인지 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수 기준이지만 일부 유니코드 문자를 허용합니다.

</div>

이메일 유효성 검증 규칙도 플루언트하게 작성할 수 있습니다.

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
> `dns`, `spoof` 검증기는 PHP `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 클래스 기반 규칙으로, 검증 대상 필드가 올바른 enum 값인지 확인합니다. 이 규칙은 enum 클래스명을 생성자 인자로 받으며, 기본 타입(primitive) 값을 검증할 때는 backed Enum을 Enum 규칙에 제공해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`, `except` 메서드를 사용하면, 유효한 enum 케이스를 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용하면 `Enum` 규칙을 조건에 따라 동적으로 수정할 수도 있습니다.

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

검증 대상 필드는 `validate` 또는 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

지정한 _anotherfield_ 필드의 값이 _value_일 때, 검증 대상 필드는 `validate` 또는 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

복잡한 조건부 제외 로직이 필요한 경우, `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 인자로 받으며, 클로저는 해당 필드를 제외해야 하면 `true`, 아니면 `false`를 반환해야 합니다.

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

지정한 _anotherfield_가 _value_와 같지 않으면, 검증 대상 필드는 `validate` 또는 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`일 때)이라면, 비교 대상 필드가 `null`이거나 요청 데이터에 없을 때만 제외되지 않습니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

_ anotherfield_ 필드가 존재할 때, 검증 대상 필드는 `validate` 또는 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

_ anotherfield_ 필드가 존재하지 않을 때, 검증 대상 필드는 `validate` 또는 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 대상 필드는 해당 데이터베이스 테이블에 값이 반드시 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 지정하지 않으면, 필드명이 그대로 사용됩니다. 예를 들어 위와 같이 사용하면, `states` 테이블에서 `state` 컬럼이 요청의 `state` 속성값과 일치하는 레코드가 존재하는지 검사하게 됩니다.

<a name="specifying-a-custom-column-name"></a>
#### 커스텀 컬럼명 지정하기

검증 규칙에서 사용할 데이터베이스 컬럼명을 테이블명 다음에 명시적으로 지정할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

때로는 `exists` 쿼리를 수행할 데이터베이스 연결(connection)까지 지정해야 할 수 있습니다. 이럴 때는 테이블명 앞에 연결명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, 검증 규칙에서 사용할 Eloquent 모델을 명시할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

실행되는 쿼리를 더 세밀하게 커스터마이즈하고 싶다면, `Rule` 클래스를 사용해 규칙을 배열로 정의할 수 있습니다. 아래 예시처럼 `|` 대신 배열을, 그리고 쿼리 빌더를 활용하면 됩니다.

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

`Rule::exists` 메서드에 두 번째 인수로 컬럼명을 전달하여, `exists` 규칙의 컬럼명을 명확하게 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

여러 개의 값 배열이 모두 데이터베이스에 존재하는지 검증하고 싶다면, 해당 필드에 `exists`와 [array](#rule-array) 규칙을 모두 추가하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

위와 같이 `exists`와 `array` 규칙이 동시에 할당되면, Laravel은 지정한 테이블에서 주어진 모든 값의 존재 여부를 한 번의 쿼리로 확인합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 대상 파일의 확장자가 아래 나열된 확장자 중 하나여야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일의 확장자로만 파일 유효성을 검증하는 것은 위험할 수 있으므로, 이 규칙은 일반적으로 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 함께 사용하는 것이 안전합니다.

<a name="rule-file"></a>
#### file

검증 대상 필드는 정상적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

검증 대상 필드가 입력 데이터에 존재하는 경우, 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 대상 필드는 지정한 _field_ 또는 _value_보다 커야 합니다. 두 필드는 반드시 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일의 경우 [size](#rule-size) 규칙과 동일한 방식으로 평가합니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 대상 필드는 지정한 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 반드시 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일의 경우 [size](#rule-size) 규칙과 동일한 방식으로 평가합니다.

<a name="rule-hex-color"></a>
#### hex_color

검증 대상 필드는 [16진수 색상(hexadecimal color)](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 올바른 색상 값이어야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지(jpg, jpeg, png, bmp, gif, webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 취약성 가능성으로 인해 SVG 파일은 허용하지 않습니다. SVG 파일을 허용하려면, `image` 규칙에 `allow_svg` 지시어를 추가하세요 (`image:allow_svg`).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 대상 필드는 지정한 값 목록 중 하나여야 합니다. 이 규칙도 배열을 `implode`해서 사용할 일이 많으므로, `Rule::in` 메서드를 사용하면 더 간결하게 규칙을 작성할 수 있습니다.

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

`in` 규칙이 `array` 규칙과 함께 사용될 경우, 입력 배열 내 각 값이 모두 `in` 규칙에 지정된 값 목록에 반드시 포함되어 있어야 합니다. 아래 예시에서 입력 배열의 `LAS`는 `in` 규칙의 값 목록에 포함되어 있지 않으므로 유효하지 않습니다.

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

검증할 필드는 _anotherfield_의 값 목록 중 하나와 일치해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증할 필드는 배열이어야 하며, 해당 배열의 키 중 주어진 _values_ 중 하나 이상을 반드시 포함해야 합니다:

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증할 필드는 정수여야 합니다.

> [!WARNING]
> 이 유효성 검증 규칙은 입력값이 실제 "정수(integer)" 타입인지 여부를 검증하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 타입이면 통과합니다. 입력값이 숫자인지를 정확히 검증하려면 [numeric 유효성 검증 규칙](#rule-numeric)과 조합해서 사용하는 것이 좋습니다.

<a name="rule-ip"></a>
#### ip

검증할 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

검증할 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증할 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증할 필드는 올바른 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증할 필드는 지정된 _field_보다 작아야 합니다. 두 필드는 반드시 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 비교합니다.

<a name="rule-lte"></a>
#### lte:_field_

검증할 필드는 지정된 _field_보다 작거나 같아야 합니다. 두 필드는 반드시 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-lowercase"></a>
#### lowercase

검증할 필드는 모두 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증할 필드는 배열이면서 리스트(list) 형태여야 합니다. 배열의 키가 0에서 `count($array) - 1`까지 연속된 숫자로 구성되어 있으면 리스트로 간주합니다.

<a name="rule-mac"></a>
#### mac_address

검증할 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증할 필드는 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증할 정수는 최대 _value_ 자리수까지 허용됩니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증할 파일은 지정된 MIME 타입 중 하나와 일치해야 합니다:

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드된 파일의 MIME 타입을 확인할 때 라라벨은 파일의 실제 내용을 읽어 MIME 타입을 추정하며, 이는 클라이언트가 제공한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증할 파일은 명시된 확장자에 해당하는 MIME 타입이어야 합니다:

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하면 되지만, 실제로는 파일의 내용을 읽어서 MIME 타입을 추정하여 검증합니다. MIME 타입과 각 확장자의 전체 목록은 아래 링크에서 확인할 수 있습니다:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 검증 규칙은 실제로 파일의 MIME 타입과 사용자가 부여한 파일 확장자가 일치하는지까지는 확인하지 않습니다. 예를 들어, `mimes:png` 규칙은, 파일 이름이 `photo.txt` 라도 실제로 PNG 포맷의 데이터가 들어 있다면 유효한 PNG 파일로 간주합니다. 사용자가 직접 입력한 파일 확장자를 별도로 검증하고 싶다면 [extensions](#rule-extensions) 규칙을 이용하세요.

<a name="rule-min"></a>
#### min:_value_

검증할 필드는 _value_ 이상의 값을 가져야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증할 정수는 최소 _value_ 자리수여야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증할 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증할 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_anotherfield_ 필드가 지정된 _value_ 중 하나와 일치하는 경우, 검증할 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_anotherfield_ 필드가 지정된 _value_와 같지 않은 경우에만, 검증할 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

명시된 다른 필드 중 하나라도 존재하면, 검증할 필드는 반드시 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

명시된 다른 모든 필드가 모두 존재할 때만, 검증할 필드는 반드시 존재하지 않아야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증할 필드는 주어진 값 목록에 포함되어 있으면 안 됩니다. `Rule::notIn` 메서드를 사용하면 더 직관적으로 이 규칙을 생성할 수 있습니다:

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

검증할 필드는 지정된 정규 표현식과 일치하지 않아야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 지정한 패턴은 반드시 `preg_match`에서 요구하는 형식(유효한 구분자 포함)을 따라야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` 또는 `not_regex` 규칙에서 정규표현식 패턴에 `|` 문자가 포함되는 경우, 유효성 규칙을 배열로 지정해야 할 수도 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증할 필드는 `null` 값을 가질 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

검증할 필드는 [숫자(numeric)](https://www.php.net/manual/en/function.is-numeric.php)여야 합니다.

<a name="rule-present"></a>
#### present

검증할 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 지정된 _value_ 중 하나와 같을 때, 검증할 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_ anotherfield_ 필드가 지정된 _value_가 아닐 때, 검증할 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

명시된 다른 필드 중 하나라도 존재하면, 검증할 필드도 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

명시된 다른 모든 필드가 모두 존재할 때만, 검증할 필드도 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증할 필드는 입력 데이터에 없어야 하거나, "비어 있음" 상태여야 합니다. "비어 있음"의 기준은 다음 중 하나에 해당합니다:

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 경로 정보 없이 존재하는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 지정된 _value_ 중 하나와 같으면, 검증할 필드는 반드시 입력 데이터에 없어야 하거나 "비어 있음" 상태여야 합니다. "비어 있음"의 기준은 다음과 같습니다:

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 경로 정보 없이 존재하는 경우

</div>

복잡한 조건으로 필드를 금지시켜야 한다면, `Rule::prohibitedIf` 메서드를 활용할 수 있습니다. 이 메서드는 불리언값이나 클로저를 인자로 받을 수 있습니다. 클로저를 전달하면, 반환값(`true` 혹은 `false`)에 따라 해당 필드를 금지시킬지 결정합니다:

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

_ anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이면, 검증할 필드는 반드시 없어야 하거나 "비어 있음" 상태여야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_ anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이면, 검증할 필드는 반드시 없어야 하거나 "비어 있음" 상태여야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_ anotherfield_ 필드가 지정된 _value_ 중 하나와 다르다면, 검증할 필드는 반드시 없어야 하거나 "비어 있음" 상태여야 합니다. "비어 있음"의 기준은 다음과 같습니다:

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 경로 정보 없이 존재하는 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증할 필드가 존재하고 "비어 있지 않은" 경우, _anotherfield_에 지정된 모든 필드는 반드시 없어야 하거나 "비어 있음" 상태여야 합니다. "비어 있음"의 기준은 다음과 같습니다:

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 경로 정보 없이 존재하는 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증할 필드는 지정된 정규 표현식 패턴과 반드시 일치해야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 지정한 패턴은 `preg_match`에서 요구하는 형식(유효한 구분자 포함)을 따라야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` 또는 `not_regex` 규칙에서 정규표현식에 `|` 문자가 들어가는 경우, `|` 구분자가 아닌 배열 형태로 규칙을 나누어 지정해야 할 수도 있습니다.

<a name="rule-required"></a>
#### required

검증할 필드는 입력 데이터에 반드시 존재하고 "비어 있지 않아야" 합니다. "비어 있음"의 기준은 다음 중 하나에 해당합니다:

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일이 경로 정보 없이 존재하는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 지정된 _value_ 중 하나와 같으면, 검증할 필드는 반드시 존재하고 "비어 있지 않아야" 합니다.

보다 복잡한 조건으로 `required_if` 규칙을 만들고 싶다면, `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언값이나 클로저를 인자로 받을 수 있습니다. 클로저를 전달하면 반환값(`true` 또는 `false`)에 따라 해당 필드가 필수인지 여부를 동적으로 결정합니다:

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

_ anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이면, 검증할 필드는 반드시 존재하고 "비어 있지 않아야" 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_ anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이면, 검증할 필드는 반드시 존재하고 "비어 있지 않아야" 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_ anotherfield_ 필드가 지정된 _value_ 중 하나가 아니면, 검증할 필드는 반드시 존재하고 "비어 있지 않아야" 합니다. 또한, _value_가 `null`일 경우(_required_unless:name,null_), 비교 필드가 `null`이거나 요청 데이터에서 아예 빠져 있으면 검증할 필드는 필수 항목이 아닙니다. 그렇지 않으면 반드시 필수입니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

명시된 다른 필드 중 하나라도 "비어 있지 않고 존재"하면, 검증할 필드도 반드시 존재하고 "비어 있지 않아야" 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

명시된 모든 필드가 모두 "비어 있지 않고 존재"할 때만, 검증할 필드도 반드시 존재하고 "비어 있지 않아야" 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

명시된 다른 필드 중 하나라도 "비어 있거나 존재하지 않으면", 검증할 필드는 반드시 존재하고 "비어 있지 않아야" 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

명시된 모든 필드가 "비어 있거나 존재하지 않을 때만", 검증할 필드는 반드시 존재하고 "비어 있지 않아야" 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증할 필드는 배열이어야 하며, 명시한 키들 중 최소한 하나 이상을 반드시 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정한 _field_의 값과 검증할 필드가 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증할 필드는 지정한 _value_ 크기와 정확히 일치해야 합니다. 문자열 데이터는 _value_만큼의 문자 수, 숫자 데이터는 _value_ 값(이때 해당 필드에 `numeric` 또는 `integer` 규칙이 필요), 배열은 _size_가 요소의 개수를 의미하고, 파일은 _size_가 파일의 용량(킬로바이트 단위)을 의미합니다. 예시를 함께 살펴보겠습니다:

```php
// 문자열의 길이가 정확히 12자인지 검증...
'title' => 'size:12';

// 입력받은 정수가 값 10과 같은지 검증...
'seats' => 'integer|size:10';

// 배열이 정확히 5개의 요소를 갖는지 확인...
'tags' => 'array|size:5';

// 업로드된 파일의 용량이 정확히 512킬로바이트인지 검사...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증할 필드는 주어진 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증할 필드는 문자열이어야 합니다. 이 필드가 `null` 값도 허용하려면 `nullable` 규칙을 함께 지정해야 합니다.

<a name="rule-timezone"></a>
#### timezone

검증할 필드는 `DateTimeZone::listIdentifiers` 메서드가 반환하는 유효한 타임존 식별자여야 합니다.

[DateTimeZone::listIdentifiers 메서드](https://www.php.net/manual/en/datetimezone.listidentifiers.php)에서 허용하는 인수들도 이 검증 규칙에 함께 전달할 수 있습니다:

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증할 필드의 값이 지정한 데이터베이스 테이블 내에 존재하지 않아야 합니다.

**사용자 정의 테이블/컬럼명 지정:**

테이블 이름을 직접 지정하는 대신, Eloquent 모델명을 지정해서 라라벨이 테이블명을 유추하도록 할 수 있습니다:

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션(두 번째 값)을 사용하면 검증 대상 컬럼명을 직접 지정할 수 있습니다. 만일 `column`을 지정하지 않으면, 해당 필드명이 컬럼명으로 자동 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**사용자 정의 데이터베이스 커넥션 지정**

때로는 Validator가 쿼리를 실행할 때 사용할 커넥션을 직접 지정해야 할 수도 있습니다. 이 경우, 테이블명 앞에 접속할 커넥션명을 붙이면 됩니다:

```php
'email' => 'unique:connection.users,email_address'
```

**특정 ID는 unique 검사에서 제외시키기:**

종종, 특정 ID는 유효성 검사에서 무시하고 싶을 때가 있습니다. 예를 들어, "프로필 정보 수정" 화면에서 사용자의 이름, 이메일, 위치 등을 입력받는다고 가정합시다. 이때 이메일 주소가 고유한지 확인하되, 사용자가 이메일을 수정하지 않고 이름만 바꾼 경우에는 본인 이메일이 이미 존재해도 에러가 나면 안 됩니다.

이럴 때는 `Rule` 클래스를 사용해 해당 사용자의 ID를 무시하도록 유연하게 규칙을 정의할 수 있습니다. 아래 예에서는 규칙을 배열 형태로 지정하여 `|` 문자 대신 배열로 나열하고 있습니다:

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
> 사용자가 임의로 조작 가능한 입력값을 `ignore` 메서드에 절대 전달해서는 안 됩니다. 반드시 시스템에서 자동 발급한 고유 ID, 예를 들어 Eloquent 모델 인스턴스의 auto-incrementing ID나 UUID만 전달해야 합니다. 이를 실수로 어길 경우 SQL 인젝션 공격에 노출될 수 있습니다.

모델의 키 값을 넘기는 대신, 모델 인스턴스 전체를 `ignore`에 전달할 수도 있습니다. 라라벨이 자동으로 키 값을 추출해서 사용합니다:

```php
Rule::unique('users')->ignore($user)
```

테이블에서 기본키 컬럼명이 `id`가 아닌 경우, 두 번째 인수로 컬럼명을 지정할 수 있습니다:

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 검증 대상 필드명과 동일한 컬럼을 조회합니다. 다른 컬럼명을 검사하려면, `unique` 메서드의 두 번째 인수로 컬럼명을 넘기면 됩니다:

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 Where 조건문 적용하기:**

조회 쿼리에 추가 조건을 붙이고 싶다면, `where` 메서드를 통해 쿼리를 커스텀할 수 있습니다. 아래와 같이 `account_id` 컬럼 값이 1인 레코드만 조회 대상으로 좁힐 수 있습니다:

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Unique 검사에서 Soft Delete 레코드 제외하기:**

기본적으로 unique 규칙은 Soft Delete 된 레코드까지도 포함하여 중복을 검색합니다. Soft Delete 레코드(논리적 삭제)를 제외하고 싶다면, `withoutTrashed` 메서드를 사용하세요:

```php
Rule::unique('users')->withoutTrashed();
```

만약 Soft Delete 컬럼명이 `deleted_at`이 아니라면, `withoutTrashed` 호출 시 컬럼명을 직접 지정할 수 있습니다:

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증할 필드는 모두 대문자여야 합니다.

<a name="rule-url"></a>
#### url

검증할 필드는 올바른 URL이어야 합니다.

특정 URL 프로토콜만 유효값으로 허용하고 싶다면, 검증 규칙에 프로토콜 이름을 파라미터로 넘길 수 있습니다:

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증할 필드는 [범용 유니크 정렬 가능 식별자(Universally Unique Lexicographically Sortable Identifier)](https://github.com/ulid/spec) (ULID)여야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증할 필드는 RFC 9562 (버전 1, 3, 4, 5, 6, 7, 8) 기준의 범용 고유 식별자(UUID)여야 합니다.

또한 아래와 같이 UUID 버전을 지정하여 해당 버전의 UUID만 유효하도록 검증할 수 있습니다:

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 필드가 특정 값일 때 유효성 검증 건너뛰기

특정 필드가 어떤 값일 때, 다른 필드의 유효성 검증을 건너뛰고 싶을 때는 `exclude_if` 검증 규칙을 사용할 수 있습니다. 아래 예제처럼 `has_appointment` 필드의 값이 `false`인 경우, `appointment_date`와 `doctor_name` 필드는 검증 대상에서 제외됩니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로, `exclude_unless` 규칙을 사용하면 지정된 값이 아닐 때만 필드 검증을 건너뛸 수 있습니다:

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>

#### 존재할 때만 유효성 검사하기

특정 상황에서는, 검증 대상 데이터에 해당 필드가 존재할 때에만 유효성 검사를 실행하고 싶을 수 있습니다. 이를 빠르게 처리하려면 `sometimes` 규칙을 규칙 목록에 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예제에서 `email` 필드는 `$data` 배열에 존재할 때만 유효성 검사가 적용됩니다.

> [!NOTE]
> 항상 존재하지만 비어 있을 수 있는 필드를 검증하려는 경우, [옵션 필드에 대한 주의 사항](#a-note-on-optional-fields)을 참고하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검사

가끔 더 복잡한 조건 로직에 따라 유효성 검사 규칙을 추가하고 싶을 수 있습니다. 예를 들어, 다른 필드의 값이 100을 초과할 때만 특정 필드를 필수로 요구할 수 있습니다. 또는 한 필드가 존재할 때만 두 개의 필드가 특정 값을 가져야 할 수도 있습니다. 이러한 유효성 검사 규칙 추가도 어렵지 않습니다. 먼저, _항상 적용되는_ 정적 규칙으로 `Validator` 인스턴스를 생성합니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

웹 애플리케이션이 게임 수집가들을 위한 시스템이라고 가정하겠습니다. 만약 게임 수집가가 회원가입 시 자신이 100개 이상의 게임을 소유하고 있다고 입력하면, 그 이유를 설명하도록 요구하고 싶을 수 있습니다. 예를 들어, 중고 게임 판매점을 운영한다거나, 단순히 게임 수집을 취미로 삼는 경우일 수 있습니다. 조건부로 이러한 항목을 요구하려면 `Validator` 인스턴스의 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인자로는 조건부 유효성 검사를 하고자 하는 필드명을, 두 번째 인자로는 적용하고자 하는 규칙들의 목록을 전달합니다. 세 번째 인자로 전달한 클로저가 `true`를 반환하면 해당 규칙들이 적용됩니다. 이 방식은 복잡한 조건부 유효성 검사도 손쉽게 구현할 수 있게 해줍니다. 또한 여러 필드에 대해 조건부 검사를 동시에 적용할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent` 인스턴스이며, 유효성 검사가 필요한 입력값이나 파일에 접근하는 데 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 유효성 검사

경우에 따라 인덱스를 알 수 없는 동일한 중첩 배열의 다른 필드를 기준으로 유효성 검사를 해야 할 때가 있습니다. 이럴 때 클로저의 두 번째 인자로, 현재 검증 중인 배열 항목 자체를 받을 수 있습니다.

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

위 방식에서, 클로저의 `$item` 파라미터 역시 속성 데이터가 배열 형태일 때는 `Illuminate\Support\Fluent`의 인스턴스입니다. 그렇지 않을 경우에는 문자열이 될 수 있습니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[배열 유효성 검사 규칙 문서](#rule-array)에서 설명한 것처럼, `array` 규칙은 허용되는 배열 키 목록을 인수로 받습니다. 배열 안에 추가적인 키가 있다면 검증에 실패하게 됩니다.

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

일반적으로, 배열 안에 허용하고자 하는 키를 반드시 명시하는 것이 좋습니다. 그렇지 않으면, validator의 `validate` 및 `validated` 메서드는 배열과 그 모든 키(다른 중첩 배열 유효성 검사 규칙으로 검증되지 않은 키도 포함)의 모든 검증된 데이터를 반환하게 됩니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 유효성 검사

중첩 배열 구조로 된 폼 입력 필드의 유효성 검사도 어렵지 않습니다. 배열 안의 속성을 도트 표기법(dot notation)으로 지정해 검증할 수 있습니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]` 필드가 있다면 다음과 같이 유효성 검사를 할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

또한 배열의 각 요소에 대해서도 유효성 검사를 적용할 수 있습니다. 예를 들어, 주어진 배열 입력 필드의 각 이메일이 고유함을 검증하려면 아래와 같이 합니다.

```php
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

마찬가지로, 언어 파일에서 [커스텀 유효성 검사 메시지](#custom-messages-for-specific-attributes)를 지정할 때도 `*` 문자를 사용할 수 있어, 배열 기반 필드에 하나의 메시지를 적용하는 것이 매우 편리합니다.

```php
'custom' => [
    'person.*.email' => [
        'unique' => 'Each person must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근하기

특정 중첩 배열 요소의 값에 따라 속성에 대한 유효성 검사 규칙을 동적으로 지정해야 할 때, `Rule::forEach` 메서드를 활용할 수 있습니다. `forEach` 메서드는 검증 대상 배열 속성의 각 항목마다 클로저를 실행하며, 클로저는 해당 속성 값과 완전히 확장된 속성명을 전달받아, 그 요소별로 적용할 규칙의 배열을 반환해야 합니다.

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
### 에러 메시지에서 인덱스와 위치 사용

배열을 검증할 때, 유효성 검증에 실패한 항목의 인덱스나 위치를 사용자에게 에러 메시지로 표시하고 싶을 수 있습니다. 이 기능을 위해 [커스텀 유효성 검사 메시지](#manual-customizing-the-error-messages)에서 `:index`(0부터 시작)와 `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다.

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

위 예제에서, 유효성 검증 실패 시 사용자에게 "Please describe photo #2."라는 에러 메시지가 표시됩니다.

필요하다면, 더 깊이 중첩된 인덱스나 위치도 아래와 같이 참조할 수 있습니다: `second-index`, `second-position`, `third-index`, `third-position` 등.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 유효성 검사

라라벨에서는 `mimes`, `image`, `min`, `max` 등 파일 업로드를 검증할 수 있는 다양한 유효성 검사 규칙을 제공합니다. 물론 파일을 검증할 때 이 규칙들을 일일이 지정할 수도 있지만, 보다 편리하게 사용할 수 있는 유연한 파일 유효성 검사 규칙 빌더도 제공됩니다.

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
#### 파일 유형 유효성 검사

`types` 메서드에 확장자만 지정해도 되지만, 이 메서드는 실제로 파일의 내용을 읽어 MIME 타입을 판별해 파일 유형을 검증합니다. MIME 타입과 해당 확장자의 전체 목록은 아래에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 유효성 검사

파일 크기의 최소값과 최대값을 설정할 때는, 단위를 나타내는 접미어가 붙은 문자열로 지정할 수 있어 더욱 편리합니다. `kb`, `mb`, `gb`, `tb` 등의 접미어가 지원됩니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 유효성 검사

사용자 업로드 이미지 파일을 검증하는 경우, `File` 규칙의 `image` 생성자 메서드를 사용하면 해당 파일이 이미지(jpg, jpeg, png, bmp, gif, webp) 파일임을 보장할 수 있습니다.

추가적으로, `dimensions` 규칙을 조합하면 이미지의 크기를 제한할 수도 있습니다.

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
> 이미지 크기 검증에 대한 더 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

> [!WARNING]
> 기본적으로, `image` 규칙은 XSS(크로스사이트스크립팅) 취약점 가능성 때문에 SVG 파일은 허용하지 않습니다. SVG 파일을 허용해야 하는 경우, `image` 규칙에 `allowSvg: true`를 전달할 수 있습니다: `File::image(allowSvg: true)`

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기 유효성 검사

이미지의 크기(가로, 세로) 자체도 검증할 수 있습니다. 예를 들어, 업로드된 이미지가 최소 1000px 너비와 500px 높이를 가지도록 하려면 아래와 같이 `dimensions` 규칙을 사용할 수 있습니다.

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
> 이미지 크기 검증에 관한 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하세요.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검사

비밀번호가 충분한 복잡성을 갖도록 하려면 라라벨의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체를 활용하면, 최소 몇 자 이상, 적어도 하나 이상의 영문자, 숫자, 기호, 대소문자 조합 등 다양한 비밀번호 복잡성 요구사항을 쉽게 커스터마이즈할 수 있습니다.

```php
// 최소 8자 이상 필요...
Password::min(8)

// 적어도 영문자 하나 이상...
Password::min(8)->letters()

// 대문자와 소문자 각각 하나 이상...
Password::min(8)->mixedCase()

// 적어도 숫자 하나 이상...
Password::min(8)->numbers()

// 적어도 기호 하나 이상...
Password::min(8)->symbols()
```

또한 `uncompromised` 메서드를 사용하면, 공개된 비밀번호 유출 데이터에 포함되지 않은 비밀번호인지 검사할 수도 있습니다.

```php
Password::min(8)->uncompromised()
```

`Password` 규칙 객체 내부적으로는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 모델을 활용하여, [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호 유출 여부를 확인하지만 사용자 프라이버시나 보안을 침해하지 않습니다.

기본적으로 데이터 유출에 비밀번호가 한 번이라도 등장하면 부적합으로 간주합니다. 이 임계값(몇 번 이하로 등장해야 하는지 조건)은 `uncompromised` 메서드에 첫 번째 인수로 지정해 변경할 수 있습니다.

```php
// 유출 데이터에서 최대 2번(3번 미만) 등장해야만 유효함...
Password::min(8)->uncompromised(3);
```

물론 위에서 소개한 모든 조건 메서드를 체이닝해 한번에 지정할 수도 있습니다.

```php
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의하기

비밀번호에 대한 기본 유효성 검사 규칙을 애플리케이션 내 한 곳에 지정해두면 편리할 수 있습니다. 이를 위해 `Password::defaults` 메서드를 사용할 수 있고, 이 메서드에는 클로저를 전달합니다. 클로저는 기본 `Password` 규칙 객체 설정을 반환해야 합니다. 보통은 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `defaults`를 호출합니다.

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

이후, 특정 비밀번호에 대해 유효성 검사 시 기본 규칙을 적용하려면 인수 없이 `defaults`를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

가끔은 기본 비밀번호 유효성 검사 규칙에 추가 규칙을 덧붙이고 싶을 수 있습니다. 이럴 때는 `rules` 메서드를 사용하면 됩니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 커스텀 유효성 검사 규칙

<a name="using-rule-objects"></a>
### 규칙 객체 사용하기

라라벨은 이미 다양한 편리한 유효성 검사 규칙을 제공합니다. 그러나 상황에 따라 직접 유효성 검사 규칙을 만들어야 할 수도 있습니다. 커스텀 규칙 등록 방법 중 하나는 "규칙 객체"를 이용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용하세요. 예를 들어, 문자열이 모두 대문자인지 확인하는 규칙을 만들 수 있습니다. 라라벨은 규칙 객체를 `app/Rules` 디렉토리에 저장합니다. 이 디렉토리가 없다면 Artisan 명령어 실행 시 자동으로 생성됩니다.

```shell
php artisan make:rule Uppercase
```

규칙 객체가 생성되면, 동작을 정의할 수 있습니다. 규칙 객체에는 단일 메서드 `validate`가 존재하며, 이 메서드는 속성명, 값, 그리고 유효성 검사 실패 시 실행할 콜백(에러 메시지)을 받습니다.

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

이렇게 정의한 규칙 객체를, 나머지 유효성 검사 규칙들과 함께 해당 규칙 객체의 인스턴스를 전달해 validator에 추가할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 검사 메시지 번역하기

`$fail` 클로저에 실제 메시지 대신, [번역 문자열 키](/docs/12.x/localization)를 전달하고, 라라벨이 해당 에러 메시지를 번역하도록 할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면 `translate` 메서드의 첫 번째, 두 번째 인수로 플레이스홀더 치환과 원하는 언어를 각각 지정할 수도 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

커스텀 유효성 검사 규칙 클래스에서, 검증 대상 전체 데이터에 접근할 필요가 있다면, 클래스에 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하면 됩니다. 이 인터페이스는 `setData` 메서드를 정의하도록 요구합니다. 이 메서드는 라라벨이 검증을 진행하기 전에 자동으로 호출되어, 검증 중인 모든 데이터를 전달받게 됩니다.

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

또는, 유효성 검사 실행에 사용되는 validator 인스턴스 자체에 접근해야 하는 경우, 클래스에 `ValidatorAwareRule` 인터페이스를 추가로 구현하면 됩니다.

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
### 클로저(익명 함수) 사용하기

특정 커스텀 규칙이 애플리케이션 내에서 한 번만 필요하다면, 규칙 객체 대신 클로저(익명 함수)로도 구현할 수 있습니다. 이 클로저는 속성명, 값, 유효성 검사 실패 시 실행할 `$fail` 콜백을 전달받습니다.

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

기본적으로, 검증 대상 속성이 존재하지 않거나 빈 문자열일 때는, 기본 규칙은 물론, 커스텀 규칙조차도 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에는 적용되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있어도 커스텀 규칙을 실행하고 싶다면, 해당 규칙이 해당 속성을 필수로 암시(암묵적으로 required)해야 합니다. 새 암묵적 규칙 객체를 생성하려면, `make:rule` Artisan 명령어에 `--implicit` 옵션을 추가해 실행합니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적" 규칙은 속성이 필수임을 _암시_ 만 합니다. 실제로 누락되거나 비어 있는 속성을 유효하지 않다고 판단할지는, 여러분의 규칙 구현에 달려 있습니다.