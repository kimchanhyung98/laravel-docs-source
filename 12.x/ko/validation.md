# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [선택 필드에 대한 안내](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 형식](#validation-error-response-format)
- [폼 요청 유효성 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청의 권한 부여](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 에러 백 사용하기](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [유효성 검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 데이터 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 검증](#validating-nested-array-input)
    - [에러 메시지의 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적(implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션으로 들어오는 데이터를 검증할 수 있는 다양한 방법을 제공합니다. 가장 일반적으로 사용되는 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드입니다. 하지만, 이 외에도 다양한 접근 방식이 있으므로 본 문서에서 함께 다루겠습니다.

라라벨은 매우 다양한 편리한 유효성 검증 규칙을 기본 제공하며, 특정 데이터베이스 테이블 내의 값이 유일한지 검증하는 기능도 지원합니다. 이 문서에서는 모든 유효성 검증 규칙에 대해 자세히 설명하므로, 라라벨의 유효성 검증 기능을 폭넓게 이해할 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기

라라벨의 강력한 유효성 검증 기능을 살펴보기 위해, 폼 데이터를 검증하고 발생한 에러 메시지를 사용자에게 표시하는 전체 예제를 알아보겠습니다. 이번 장에서는 전체 흐름을 통해 들어오는 요청 데이터를 어떻게 라라벨로 쉽게 검증하는지 개념을 잡을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같이 라우트가 정의되어 있다고 가정하겠습니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

이 중 `GET` 라우트는 사용자가 새 블로그 글을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 블로그 글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위의 두 라우트를 처리하는 간단한 컨트롤러 구조를 살펴보겠습니다. 우선 `store` 메서드는 비워둔 상태입니다:

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

이제 `store` 메서드에 새 블로그 글을 검증하는 코드를 작성해보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용할 수 있습니다. 검증 규칙을 모두 통과하면, 이후 코드가 정상적으로 실행됩니다. 만약 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 자동으로 발생하며, 적합한 에러 응답이 사용자에게 반환됩니다.

기본적인 HTTP 요청에서 검증에 실패한 경우에는 이전 URL로 자동 리디렉션 응답이 생성됩니다. 요청이 XHR(비동기 JavaScript) 요청이라면, [유효성 검증 에러 메시지가 담긴 JSON 응답](#validation-error-response-format) 이 반환됩니다.

`validate` 메서드가 어떻게 동작하는지 예시 코드를 통해 살펴보겠습니다:

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

위와 같이, 검증 규칙들은 `validate` 메서드에 배열 형태로 전달됩니다. 걱정하지 마세요. 모든 사용 가능한 검증 규칙들은 [문서에서 확인](#available-validation-rules)하실 수 있습니다. 다시 말하지만, 검증에 실패하면 적합한 응답이 자동으로 반환되고, 검증에 성공하면 컨트롤러의 나머지 로직이 계속 실행됩니다.

또한, 각 필드의 규칙을 `|`로 구분된 문자열이 아니라 배열로 명시할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한 `validateWithBag` 메서드를 활용하면, 요청의 검증 결과 에러 메시지를 [이름이 지정된 에러 백(Named Error Bag)](#named-error-bags)에 저장할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

때로는 한 속성의 검증 규칙 중 첫 번째 실패가 발생하면, 이후 규칙 검증을 중단하고 싶을 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서는, `title` 속성에 대해 `unique` 규칙이 실패하면 그 뒤의 `max` 규칙은 더 이상 확인하지 않습니다. 규칙들은 작성한 순서대로 차례로 적용됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 안내

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있을 경우, 검증 규칙에서 "닷(dot) 표기법"을 사용하여 이러한 필드를 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드명에 실제로 마침표가 포함되어 있다면, 역슬래시(`\`)를 사용해 마침표를 이스케이프하면 "dot" 문법으로 인식되지 않게 할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

그렇다면, 만약 요청 필드가 지정한 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯, 라라벨은 자동으로 사용자를 이전 위치로 리디렉션합니다. 그리고, 검증 에러 메시지와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)은 모두 [세션에 플래시(flash)](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어, 즉 `web` 미들웨어 그룹에서 제공되는 미들웨어가, 애플리케이션의 모든 뷰에 `$errors` 변수를 공유합니다. 따라서 이 미들웨어가 적용된 경우, 뷰에서는 언제나 `$errors` 변수가 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 객체의 인스턴스입니다. 이 객체에 대해 자세히 알고 싶으시면 [관련 문서](#working-with-error-messages)를 참고하세요.

따라서 예시에서는, 검증에 실패하면 컨트롤러의 `create` 메서드로 사용자가 다시 리디렉션되고, 뷰에서 에러 메시지를 표시할 수 있습니다:

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

라라벨이 기본으로 제공하는 유효성 검증 규칙 각각의 에러 메시지는 애플리케이션 내 `lang/en/validation.php` 파일에 위치합니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 사용하여 디렉터리를 생성할 수 있습니다.

`lang/en/validation.php` 파일 내부에는 각 검증 규칙에 대한 번역 메시지 엔트리가 준비되어 있습니다. 여러분은 애플리케이션에 맞게 이 메시지들을 자유롭게 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해 각 언어에 맞게 메시지를 번역할 수도 있습니다. 라라벨의 다국어 지원에 대해 더 자세히 알고 싶으시면 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어를 통해 직접 퍼블리시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

위 예시에서는 일반 폼을 사용해 데이터를 서버로 전송했습니다. 하지만, 실제 여러 애플리케이션에서는 JavaScript 기반 프론트엔드에서 XHR(비동기) 요청을 보내기도 합니다. 이런 상황에서 `validate` 메서드를 사용할 경우, 라라벨은 리디렉션 응답을 생성하지 않습니다. 대신 [모든 유효성 검증 에러가 담긴 JSON 응답](#validation-error-response-format)을 반환하며, HTTP 상태 코드는 422로 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

Blade 템플릿에서 특정 속성에 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하려면 `@error` [Blade](/docs/12.x/blade) 디렉티브를 사용할 수 있습니다. `@error` 디렉티브 내부에서는 `$message` 변수를 바로 출력하여 에러 메시지를 표시하면 됩니다:

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

[이름이 지정된 에러 백](#named-error-bags)을 사용하는 경우라면, 두 번째 인자로 에러 백의 이름을 지정해 `@error` 디렉티브에 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

라라벨에서 유효성 검증 에러로 리디렉션이 발생하면, 프레임워크는 해당 요청의 입력값 모두를 [세션에 플래시](https://laravel.com/docs/12.x/session#flash-data)합니다. 이렇게 하면 다음 요청 시 이전 입력값을 쉽게 꺼내와서, 사용자가 작성하던 폼을 그대로 다시 보여줄 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하면 됩니다. 이 메서드는 [세션](https://laravel.com/docs/12.x/session)에 저장된 이전 입력값을 반환합니다:

```php
$title = $request->old('title');
```

라라벨은 또한 전역적으로 `old` 헬퍼 함수를 제공합니다. Blade 템플릿에서 이전 입력값을 폼에 미리 채우고자 할 때는, `old` 헬퍼를 활용하는 것이 더욱 편리합니다. 해당 필드에 대해 이전 입력값이 없다면, 반환값은 `null`입니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 필드에 대한 안내

기본적으로 라라벨의 글로벌 미들웨어 스택에는 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이로 인해, "선택" 입력 필드는 만약 `nullable` 규칙이 적용되어 있지 않으면, 값이 `null`일 때 유효하지 않은 값으로 간주될 수 있습니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서는, `publish_at` 필드는 `null`이거나 올바른 날짜 데이터만 통과됩니다. 만약 해당 규칙에 `nullable` 수식자를 추가하지 않는다면, `null`값은 유효하지 않은 날짜값으로 처리됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, 라라벨은 에러 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래 예시는 유효성 검증 에러에 대한 JSON 응답 형식입니다. 참고로, 중첩 에러 키는 "dot(닷) 표기법"으로 평탄화(flatten)되어 반환됩니다:

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
## 폼 요청 유효성 검증

<a name="creating-form-requests"></a>
### 폼 요청 생성하기

더 복잡한 유효성 검증 시나리오의 경우, "폼 요청(form request)"을 생성해 사용할 수 있습니다. 폼 요청은 검증 및 인가(권한 부여) 로직을 자체적으로 캡슐화하는 커스텀 요청 클래스입니다. 폼 요청 클래스를 생성하려면, `make:request` Artisan CLI 명령어를 사용하면 됩니다:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 만약 해당 디렉터리가 없다면, `make:request` 명령어 실행 시 자동으로 생성됩니다. 라라벨이 만들어주는 폼 요청 클래스에는 `authorize`와 `rules` 두 가지 메서드가 있습니다.

예상하셨듯이, `authorize` 메서드는 현재 인증된 사용자가 이 요청으로 표현되는 작업을 수행할 수 있는지 결정합니다. `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다:

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
> `rules` 메서드의 시그니처에 필요한 의존성을 타입힌트로 선언할 수 있으며, 라라벨의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

그렇다면, 이 규칙들은 어떻게 적용될까요? 컨트롤러에서 요청 파라미터를 해당 폼 요청 클래스로 타입힌트만 해주면 됩니다. 들어오는 폼 요청은 컨트롤러 메서드가 호출되기 전에 자동 검증되므로, 컨트롤러 내부에는 검증 로직이 남지 않습니다:

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // 검증된 입력값 전체를 가져오기
    $validated = $request->validated();

    // 검증된 입력값의 일부분만 가져오기
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 글 저장...

    return redirect('/posts');
}
```

검증에 실패하면, 사용자를 이전 위치로 되돌려보내는 리디렉션 응답이 자동 생성됩니다. 에러 또한 세션에 플래시되어 보여줄 수 있습니다. 요청이 XHR(비동기) 요청이었다면, 422 상태 코드와 함께 [유효성 검증 에러의 JSON 표현](#validation-error-response-format)이 포함된 응답이 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에서 실시간 폼 요청 유효성 검증이 필요하다면, [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 폼 요청에서 추가 유효성 검증 수행하기

초기 유효성 검증이 완료된 후, 추가 검증이 필요한 경우가 있습니다. 폼 요청 클래스의 `after` 메서드를 활용해 이 작업을 수행할 수 있습니다.

`after` 메서드는 검증 완료 후 호출할 콜러블 또는 클로저 배열을 반환해야 합니다. 이 콜러블들은 `Illuminate\Validation\Validator` 인스턴스를 매개변수로 받아 추가 에러 메시지를 발생시킬 수 있습니다:

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

위에서 언급한 대로, `after` 메서드가 반환하는 배열에는 호출 가능한 클래스 인스턴스를 포함시킬 수도 있습니다. 이 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다:

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

폼 요청 클래스에 `stopOnFirstFailure` 속성을 추가하면, 한 번의 유효성 검증 실패가 발생했을 때 모든 속성의 검증을 즉시 중단하도록 설정할 수 있습니다:

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

폼 요청 검증이 실패했을 때 사용자를 이전 위치가 아닌 다른 위치로 리디렉션하고 싶다면, 폼 요청 클래스에 `$redirect` 속성을 정의하면 됩니다:

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 지정한 네임드 라우트로 리디렉션하고 싶다면 `$redirectRoute` 속성을 사용할 수 있습니다:

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청의 권한 부여

폼 요청 클래스에는 `authorize` 메서드도 존재합니다. 이 메서드 내에서, 인증된 사용자가 해당 리소스를 업데이트할 권한이 실제로 있는지 확인할 수 있습니다. 예를 들어, 사용자가 수정하려는 블로그 댓글의 실제 소유자인지를 판단할 수 있습니다. 대부분의 경우, 이 메서드는 [인가 게이트(gate) 또는 정책(policy)](/docs/12.x/authorization)과 상호작용하게 됩니다:

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

모든 폼 요청은 라라벨의 기본 요청 클래스를 확장하므로, `user` 메서드를 사용해 현재 인증된 사용자에 접근할 수 있습니다. 또한, 위 예시에서 볼 수 있듯 `route` 메서드를 통해 해당 라우트의 URI 파라미터(예: `{comment}`)에 접근할 수 있습니다:

```php
Route::post('/comment/{comment}');
```

따라서, [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하는 경우라면, 요청 속성으로 해결된 모델을 코드에서 더 간단하게 접근할 수 있습니다:

```php
return $this->user()->can('update', $this->comment);
```

만약 `authorize` 메서드에서 `false`를 반환하면, HTTP 403 상태 코드와 함께 컨트롤러 메서드는 실행되지 않고 응답이 반환됩니다.

요청의 권한 검증 로직을 애플리케이션 내 다른 부분에 위임하려면, `authorize` 메서드를 제거하거나 단순히 `true`를 반환하도록 만들 수 있습니다:

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
> `authorize` 메서드의 시그니처에 필요한 의존성도 타입힌트로 선언할 수 있으며, 라라벨의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

폼 요청 클래스에서 사용되는 에러 메시지는 `messages` 메서드를 오버라이드하여 커스터마이징할 수 있습니다. 이 메서드는 속성/규칙마다 커스텀 에러 메시지를 할당하는 배열을 반환해야 합니다:

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
#### 유효성 검증 속성명 커스터마이징

라라벨의 내장 유효성 검증 에러 메시지 배포본에는 `:attribute` 플레이스홀더를 포함한 규칙이 많습니다. 해당 플레이스홀더가 커스텀 속성명으로 치환되길 원한다면, `attributes` 메서드를 오버라이드하여 원하는 속성명을 반환하면 됩니다:

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

유효성 검증 전에 요청 데이터를 미리 가공하거나 정제(sanitize)해야 할 경우, `prepareForValidation` 메서드를 사용하세요:

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

마찬가지로, 유효성 검증이 끝난 후 요청 데이터를 정규화해야 한다면, `passedValidation` 메서드를 활용하면 됩니다:

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

## 수동으로 Validator 생성하기

요청에서 `validate` 메서드를 사용하지 않고, [facade](/docs/12.x/facades)인 `Validator`를 직접 활용하여 validator 인스턴스를 수동으로 만들 수도 있습니다. facade의 `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새로운 블로그 게시글 저장.
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

        // 검증에 통과한 입력값 가져오기...
        $validated = $validator->validated();

        // 검증에 통과한 입력값 중 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 게시글 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인자는 검증할 데이터이며, 두 번째 인자는 데이터에 적용할 검증 규칙들의 배열입니다.

요청 데이터의 검증이 실패했는지 확인한 후, `withErrors` 메서드를 사용해 에러 메시지를 세션에 저장할 수 있습니다. 이 방법을 사용하면 리다이렉트 이후 `$errors` 변수가 뷰와 자동으로 공유되어, 사용자에게 에러 메시지를 쉽게 보여줄 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP `array`를 인자로 받을 수 있습니다.

#### 첫 번째 검증 실패 시 중지

`stopOnFirstFailure` 메서드는 하나의 검증 항목에서 실패가 발생하면, 나머지 속성에 대한 검증을 중지하도록 validator에 알릴 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

validator 인스턴스를 수동으로 생성하더라도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 그대로 활용하고 싶다면, 이미 존재하는 validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 검증에 실패하면 사용자는 자동으로 리다이렉트되며, XHR 요청의 경우에는 [JSON 응답](#validation-error-response-format)이 반환됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

만약 검증 실패 시 [이름을 가진 에러백](#named-error-bags)에 에러 메시지를 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름 있는 에러백(Named Error Bags)

하나의 페이지에 여러 개의 폼이 있을 때, 검증 에러를 담는 `MessageBag`에 이름을 붙여 특정 폼에 대한 에러 메시지만 가져올 수 있습니다. 이를 위해서 `withErrors`의 두 번째 인자로 이름을 전달하면 됩니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이후 뷰에서 `$errors` 변수의 해당 이름을 통해 에러 메시지에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요하다면, 라라벨에서 기본 제공하는 에러 메시지 대신 validator 인스턴스가 사용할 커스텀 에러 메시지를 지정할 수 있습니다. 커스텀 메시지는 여러 가지 방법으로 지정할 수 있습니다. 가장 먼저, `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지 배열을 전달하면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

여기서 `:attribute` 플레이스홀더는 실제 검증 중인 필드명으로 대체됩니다. 에러 메시지에서 사용할 수 있는 다른 플레이스홀더도 사용할 수 있습니다. 예를 들어:

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

때때로 특정 속성에만 커스텀 에러 메시지를 지정하고 싶을 수 있습니다. 이를 위해 "점 표기법(dot notation)"을 사용하세요. 먼저 속성명을, 그리고 그 뒤에 규칙명을 붙입니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

라라벨의 기본 에러 메시지 중에는 `:attribute` 플레이스홀더가 들어간 것이 많고, 이 부분은 검증되는 필드명이나 속성명으로 대체됩니다. 특정 필드에 대해 이 플레이스홀더가 대체될 값을 커스터마이징하고 싶다면, `Validator::make`의 네 번째 인자로 커스텀 속성명을 지정하는 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 검증 수행

초기 검증이 끝난 후, 추가적인 검증이 필요한 경우 validator의 `after` 메서드를 사용하면 됩니다. `after` 메서드는 클로저 또는 호출 가능한(callable) 요소의 배열을 받아, 검증이 끝난 후 이들을 호출합니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아, 추가 에러 메시지를 필요에 따라 추가할 수 있습니다.

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

위에서 설명한 것처럼, `after` 메서드는 콜러블의 배열도 받을 수 있습니다. 만약 "추가 검증" 로직이 호출 가능한 클래스로 캡슐화되어 있다면, 이 클래스의 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받게 됩니다.

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
## 검증된 입력 데이터 활용하기

폼 리퀘스트나 수동으로 생성한 validator 인스턴스를 통해 요청 데이터를 검증한 뒤, 실제로 검증을 통과한 요청 데이터들을 가져오고 싶을 수 있습니다. 방법은 여러 가지가 있습니다. 우선, 폼 리퀘스트나 validator 인스턴스에서 `validated` 메서드를 호출하면 검증을 통과한 데이터 배열을 바로 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 리퀘스트나 validator 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하며, 이 객체는 검증을 통과한 데이터 중 일부만 가져오거나 전체 데이터를 배열로 가져오는 `only`, `except`, `all` 등의 메서드를 제공합니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나 인덱스로 접근할 수 있습니다.

```php
// 검증된 데이터 반복 처리...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근...
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 필드를 추가하고 싶을 때는 `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 받고 싶다면, `collect` 메서드를 호출하면 됩니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 여러 편의 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 반환합니다. 모든 뷰에 자동으로 제공되는 `$errors` 변수도 이 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

필드별 첫 번째 에러 메시지를 가져오려면 `first` 메서드를 사용하세요.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드에 대한 모든 메시지 배열이 필요할 때는 `get` 메서드를 사용합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열형 필드를 검증할 때는 `*` 문자를 사용해 배열의 각 요소에 대한 모든 메시지를 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 필드의 메시지 배열이 필요할 때는 `all` 메서드를 사용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 해당 필드에 메시지가 존재하는지 확인하기

특정 필드에 대해 에러 메시지가 존재하는지 확인하려면 `has` 메서드를 사용합니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정

라라벨의 내장 검증 규칙마다 에러 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각각의 검증 규칙에 대한 번역 항목이 있습니다. 필요에 따라 해당 메시지를 자유롭게 수정하거나 변경해도 됩니다.

또한, 이 파일을 원하는 언어의 디렉터리로 복사하여 애플리케이션의 언어에 맞게 에러 메시지를 번역할 수 있습니다. 라라벨의 로컬라이제이션에 대해 더 자세히 알고 싶다면 [로컬라이제이션 전체 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 게시해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션의 검증 언어 파일에서, 지정한 속성과 규칙 조합에 대한 에러 메시지를 커스터마이즈할 수 있습니다. 이를 위해 `lang/xx/validation.php` 언어 파일의 `custom` 배열에 커스텀 메시지를 추가합니다.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성명 지정

라라벨의 내장 에러 메시지 상당수는 `:attribute` 플레이스홀더를 포함하며, 해당 부분은 검증 중인 필드나 속성의 이름으로 치환됩니다. 검증 메시지의 `:attribute` 부분을 커스텀 값으로 대체하려면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 원하는 이름을 지정하면 됩니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 게시해야 합니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정

라라벨의 일부 내장 검증 규칙 에러 메시지에는 `:value` 플레이스홀더가 있으며, 이것은 현재 요청 속성의 값으로 치환됩니다. 하지만, 때로는 검증 메시지의 `:value` 부분을 값 자체 대신 더 사용자 친화적인 표시로 바꾸고 싶을 수 있습니다. 예를 들어 `payment_type`이 `cc`일 때 신용카드 번호가 필수라는 규칙을 생각해봅시다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

만약 이 검증이 실패하면 다음과 같은 에러 메시지를 보여줍니다.

```text
The credit card number field is required when payment type is cc.
```

이때 `cc`가 아닌 더 보기 쉬운 값을 표시하고 싶다면, 언어 파일의 `values` 배열에 지정할 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 게시해야 합니다.

이렇게 값을 정의하면, 검증 규칙은 다음과 같이 더 친근한 내용의 에러 메시지를 생성합니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙

아래는 사용 가능한 모든 유효성 검증 규칙과 각 규칙의 기능입니다.



#### 불리언(Booleans)

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### 문자열(Strings)

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

#### 숫자(Numbers)

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

#### 배열(Arrays)

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

#### 날짜(Dates)

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

#### 파일(Files)

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

#### 데이터베이스(Database)

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

<a name="rule-accepted"></a>
#### accepted

해당 필드의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 일반적으로 "이용약관 동의"와 같은 필드의 유효성 검증에 쓰입니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

만약 지정한 다른 필드가 특정 값과 동일하다면, 해당 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 마찬가지로 "이용약관 동의"와 같은 검증에 유용하게 사용됩니다.

<a name="rule-active-url"></a>
#### active_url

해당 필드는 `dns_get_record` PHP 함수 기준, 올바른 A 또는 AAAA 레코드를 가져야 합니다. 제공된 URL의 호스트네임은 `parse_url` 함수로 추출된 후 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

해당 필드는 특정 날짜 이후의 값이어야 합니다. 이 날짜는 PHP의 `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`으로 평가할 날짜 문자열 대신, 비교 기준이 될 또 다른 필드를 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

더 편리하게 사용할 수 있도록, date 관련 규칙은 유창한(Fluent) `date` 규칙 빌더를 통해 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드를 사용하면, 날짜가 오늘 이후이거나 오늘 혹은 그 이후여야 한다는 요구 조건을 더 간결하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>

#### after_or_equal:_date_

검증할 필드는 지정한 날짜와 같거나 이후의 값이어야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

편의를 위해, 날짜 기반의 규칙은 유창한 `date` 규칙 빌더를 사용하여 생성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검사 규칙을 사용하면 해당 필드가 제공된 여러 유효성 검사 규칙 중 **하나라도** 만족해야 함을 지정할 수 있습니다. 예를 들어, 아래 규칙은 `username` 필드가 이메일 주소이거나, 최소 6자 이상의 알파벳/숫자/대시로만 이루어진 문자열인지 검증합니다.

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

검증할 필드는 반드시 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함된 유니코드 알파벳 문자로만 구성되어 있어야 합니다.

이 규칙을 ASCII 범위(`a-z`, `A-Z`)의 문자로만 제한하고 싶다면, `ascii` 옵션을 추가하면 됩니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증할 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 유니코드 알파벳/숫자, 그리고 ASCII 대시(`-`)와 언더스코어(`_`) 문자로만 이루어져야 합니다.

이 규칙을 ASCII 범위(`a-z`, `A-Z`, `0-9`)로만 제한하고 싶다면, `ascii` 옵션을 사용할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증할 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 유니코드 알파벳/숫자 문자로만 이루어져야 합니다.

이 규칙을 ASCII 범위(`a-z`, `A-Z`, `0-9`)의 문자로 제한하려면, `ascii` 옵션을 사용하세요.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증할 필드는 PHP의 `array`여야 합니다.

`array` 규칙에 추가 값을 전달하면, 입력 배열에 포함된 모든 키가 지정한 값 목록 내에 반드시 존재해야 합니다. 아래 예시에서 입력 배열에 존재하는 `admin` 키는 `array` 규칙에 명시된 값 목록에 포함되어 있지 않기 때문에 올바르지 않은 값이 됩니다.

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

일반적으로, 배열 내에 허용되는 키를 항상 명확히 지정하는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

검증할 필드는 반드시 7비트 ASCII 문자만 포함해야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드에 대해 첫 번째 유효성 검증 오류가 발생하면 이후의 유효성 검증은 중지합니다.

`bail` 규칙은 특정 필드에서 검증 실패 시 그 필드의 추가 검증만 중단하지만, `stopOnFirstFailure` 메서드를 사용하면 전체 입력 데이터에서 단 하나의 검증 실패만 발생해도 모든 필드에 대한 검증을 즉시 중단하도록 할 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증할 필드는 지정한 날짜 이전의 값이어야 합니다. 날짜는 PHP의 `strtotime` 함수에 의해 올바른 `DateTime` 인스턴스로 변환되어 평가됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 날짜 값 대신 다른 필드명을 지정할 수도 있습니다.

이 규칙 역시 유창한 `date` 빌더를 통해 편리하게 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`와 `todayOrBefore` 메서드를 사용하면 날짜가 오늘 이전, 혹은 오늘이거나 이전이어야 함을 보다 명확하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증할 필드는 지정한 날짜와 같거나 그 이전의 값이어야 합니다. 날짜는 PHP의 `strtotime` 함수에 의해 올바른 `DateTime` 인스턴스로 변환되어 평가됩니다. 또한 [after](#rule-after) 규칙처럼 날짜 대신 다른 필드명을 값으로 사용할 수 있습니다.

이 규칙 역시 유창한 `date` 빌더로 손쉽게 정의할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

검증할 필드는 지정한 _min_과 _max_ 사이(포함)의 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일 등에서는 [size](#rule-size) 규칙과 동일한 방식으로 크기가 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

검증할 필드는 불리언 형으로 변환 가능해야 합니다. 허용되는 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증할 필드와 `{field}_confirmation` 필드의 값이 일치해야 합니다. 예를 들어, 검증 필드가 `password`라면 입력 데이터에 `password_confirmation` 필드가 존재해야 하고, 그 값이 일치해야 합니다.

커스텀 확인 필드명을 직접 지정할 수도 있습니다. 예를 들어 `confirmed:repeat_username`으로 지정하면, 해당 필드와 `repeat_username` 필드가 일치하는지 확인합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

검증할 필드는 지정된 매개변수 값들을 모두 포함하고 있는 배열이어야 합니다. 보통 이 규칙을 사용할 때는 배열을 `implode`하는 경우가 많기 때문에, `Rule::contains` 메서드를 활용해 규칙을 더 편하게 정의할 수 있습니다.

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

검증할 필드는 현재 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 매개변수로 [인증 가드](/docs/12.x/authentication)를 지정할 수도 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증할 필드는 PHP의 `strtotime` 함수 기준으로 유효한 날짜여야 하며, 상대적인 날짜 표현은 사용할 수 없습니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증할 필드는 지정한 날짜와 정확히 일치해야 합니다. 날짜는 PHP의 `strtotime` 함수에 전달되어 적합한 `DateTime` 인스턴스로 변환되어 평가됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증할 필드는 지정된 _formats_ 형식 중 하나와 일치해야 합니다. 날짜 필드 검증 시에는 반드시 `date` 또는 `date_format` 중 하나만 사용해야 하며, 둘을 동시에 사용하면 안 됩니다. 이 규칙에서는 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 날짜 포맷을 사용할 수 있습니다.

날짜 기반의 규칙 역시 유창한 `date` 빌더로 정의할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

검증할 필드는 숫자여야 하며, 지정한 소수점 이하 자리수를 반드시 가져야 합니다.

```php
// 소수점 이하 두 자리(예: 9.99)여야 함...
'price' => 'decimal:2'

// 소수점 이하 2~4자리여야 함...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증할 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

만약 다른 필드 값이 지정한 값과 같을 때, 현재 필드는 반드시 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증할 필드는 지정한 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증할 정수는 정확히 _value_ 길이의 숫자여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증할 정수는 지정한 _min_ 이상 _max_ 이하의 길이(자릿수)를 가져야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증할 파일은 지정된 파라미터에 따른 이미지 크기 조건을 반드시 충족해야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용할 수 있는 크기 조건은 다음과 같습니다: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_.

_ratio_(비율)는 너비를 높이로 나눈 형태로 표현해야 하며, 분수(`3/2`)나 소수(`1.5`)로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

이 규칙은 인자가 여러 개 필요한 경우가 많으므로, `Rule::dimensions` 메서드를 사용해 규칙을 더 읽기 쉽게 만들 수 있습니다.

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

배열 검증 시, 해당 필드 내에는 중복된 값이 존재해선 안 됩니다.

```php
'foo.*.id' => 'distinct'
```

Distinct 규칙은 기본적으로 느슨한(동등성) 비교를 사용합니다. 엄격한(타입도 비교) 검사를 하고 싶다면 `strict` 파라미터를 추가하세요.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 차이를 무시하고자 할 때는 `ignore_case`를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증할 필드는 지정한 값들로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증할 필드는 지정한 값들로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

검증할 필드는 이메일 주소 형식이어야 합니다. 이 규칙은 이메일 주소 유효성 검증을 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로는 `RFCValidation` 검사가 적용되지만, 다른 스타일의 검사도 적용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예제는 `RFCValidation` 및 `DNSCheckValidation` 검사를 적용합니다. 사용할 수 있는 유효성 검사 스타일의 전체 목록은 다음과 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 주소를 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일을 검증하되, 경고(예: 끝에 점이 있거나 연속된 점 등)가 있으면 실패 처리합니다.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 동형 이의 문자(homograph) 또는 속임수 유니코드 문자가 포함되어 있지 않은지 검사합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일의 유효성을 검사합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - 유니코드 문자의 일부를 허용하며, PHP의 `filter_var` 함수 기준으로 검사합니다.

</div>

더 유연한 규칙 빌더로 이메일 유효성 검사를 정의하는 것도 가능합니다.

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
> `dns`, `spoof` 검사기는 PHP의 `intl` 확장(extension)이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증할 필드는 지정한 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 해당 필드가 유효한 열거형(Enum) 값인지를 검증하는 클래스 기반 규칙입니다. `Enum` 규칙에는 열거형 클래스명을 생성자 인자로 지정합니다. 원시 값을 검증하려면, 백드(값 기반) Enum을 `Enum` 규칙에 전달해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`, `except` 메서드는 특정 Enum 케이스만 유효하도록 제한할 때 사용할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용하면 조건적으로 Enum 규칙을 변경할 수 있습니다.

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

해당 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 자동으로 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

_또 다른 필드_가 _value_ 값과 같을 때, 해당 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 자동으로 제외됩니다.

만약 더 복잡한 조건부 제외 로직이 필요하다면, `Rule::excludeIf` 메서드를 활용할 수 있습니다. 이 메서드는 불리언 값 또는 클로저(익명함수)를 받을 수 있으며, 클로저가 true를 반환하면 필드를 제외하게 됩니다.

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

_또 다른 필드_의 값이 _value_와 다를 경우, 해당 필드는 `validate` 및 `validated` 메서드 반환 데이터에서 자동으로 제외됩니다. 만약 _value_가 `null`일 때(`exclude_unless:name,null`), 비교 필드가 null이거나, 아예 데이터에 없을 경우에만 필드가 유지됩니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

_또 다른 필드_가 존재한다면, 해당 필드는 요청 데이터 반환 시 자동으로 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

_또 다른 필드_가 존재하지 않을 때, 해당 필드는 요청 데이터 반환 시 자동으로 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증할 필드는 지정한 데이터베이스 테이블 내에 반드시 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 명시하지 않으면, 필드명과 동일한 컬럼이 사용됩니다. 즉, 이 예시에서 규칙은 `states` 데이터베이스 테이블 내에 `state` 컬럼 값이 요청 데이터의 `state` 값과 일치하는 레코드가 존재하는지 검사하게 됩니다.

<a name="specifying-a-custom-column-name"></a>
#### 커스텀 컬럼명 지정하기

유효성 검사 규칙에서 사용할 컬럼명을 테이블명 뒤에 지정하여 명시할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

때로는 특정한 DB 연결(connection)을 지정해야 할 수도 있습니다. 이 경우 테이블명 앞에 연결명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, Eloquent 모델명을 지정해 자동으로 해당 모델의 테이블을 사용할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

규칙에서 실행되는 쿼리를 커스터마이징하고 싶다면, `Rule` 클래스를 활용해 유창하게 규칙을 정의할 수 있습니다. 이 예에서는 규칙을 `|` 대신 배열로 지정하는 방법도 함께 보여줍니다.

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

`Rule::exists`에서 두 번째 인자로 컬럼명을 넘기면, 명시적으로 검증할 컬럼명을 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

배열 형태의 값들이 데이터베이스에 존재하는지 한 번에 검증하려면, 해당 필드에 `exists`와 [array](#rule-array) 규칙을 함께 추가하세요.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이렇게 두 규칙을 동시에 지정하면, 라라벨은 배열 내 모든 값이 지정 테이블에 존재하는지 한 번의 쿼리로 검사합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증할 파일의 확장자가, 명시한 목록 중 하나와 일치해야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일의 확장자만을 기준으로 검증하는 것에 절대적으로 의존해서는 안 됩니다. 이 규칙은 반드시 [mimes](#rule-mimes)나 [mimetypes](#rule-mimetypes) 규칙과 함께 사용하는 것이 좋습니다.

<a name="rule-file"></a>
#### file

검증할 필드는 정상적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

해당 필드는 값이 존재한다면 반드시 비어 있지 않아야 합니다.

<a name="rule-gt"></a>
#### gt:_field_

검증할 필드는 지정한 _field_ 또는 _value_보다 커야 합니다. 두 필드는 반드시 동일한 타입이어야 하며, 문자열/숫자/배열/파일 등에서는 [size](#rule-size) 규칙과 동일하게 크기가 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

검증할 필드는 지정한 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 반드시 동일한 타입이어야 하며, 문자열/숫자/배열/파일 등에서는 [size](#rule-size) 규칙과 동일하게 크기가 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

검증할 필드는 [16진수](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값이어야 합니다.

<a name="rule-image"></a>
#### image

검증할 파일은 이미지(jpg, jpeg, png, bmp, gif, webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 취약점 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 한다면 `image:allow_svg` 형태로 규칙에 allow_svg 지시어를 추가하세요.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증할 필드는 지정한 값 목록에 포함되어야 합니다. 배열을 `implode`해서 이 규칙을 적용할 때가 많으므로, `Rule::in` 메서드를 사용하면 더 간결하게 정의할 수 있습니다.

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

`in` 규칙과 `array` 규칙을 동시에 지정하면, 입력 배열의 각 값이 반드시 지정한 값 목록 내에 포함되어야 합니다. 아래 예시에서 입력 배열에 `LAS` 값이 포함되어 있는데, `in` 규칙에서는 허용 목록에 없으므로 유효하지 않습니다.

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

검증하려는 필드는 _anotherfield_의 값들 중 하나여야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증하려는 필드는 지정된 _values_ 중 적어도 하나 이상의 키를 가진 배열이어야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증하려는 필드는 정수여야 합니다.

> [!WARNING]
> 이 유효성 규칙은 입력값의 PHP 변수 타입이 "정수"인지 여부를 검사하지 않으며, 입력값이 PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 타입인지만 확인합니다. 만약 해당 입력값이 숫자값임을 확인하려면 [numeric 유효성 규칙](#rule-numeric)과 함께 사용하시기 바랍니다.

<a name="rule-ip"></a>
#### ip

검증하려는 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

검증하려는 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증하려는 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증하려는 필드는 올바른 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증하려는 필드는 지정된 _field_보다 작아야 합니다. 두 필드는 반드시 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

검증하려는 필드는 지정된 _field_보다 작거나 같아야 합니다. 두 필드는 반드시 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lowercase"></a>
#### lowercase

검증하려는 필드는 모두 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증하려는 필드는 리스트 형태의 배열이어야 합니다. 배열의 키가 0부터 `count($array)-1`까지 연속된 숫자일 때, 해당 배열을 리스트로 간주합니다.

<a name="rule-mac"></a>
#### mac_address

검증하려는 필드는 올바른 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증하려는 필드는 최대 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 역시 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증하려는 정수는 최대 _value_ 자리수 이내여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증하려는 파일은 지정된 MIME 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드된 파일의 MIME 타입을 확인할 때, 프레임워크는 파일 자체의 내용을 읽어 MIME 타입을 추정(guess)하며, 이는 클라이언트가 제공한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증하려는 파일은 명시된 확장자에 해당하는 MIME 타입을 가져야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하면 되지만, 실제로 이 규칙은 파일 내용을 읽어 MIME 타입을 추정해 검증합니다. 각 확장자와 해당 MIME 타입의 전체 목록은 아래 링크에서 확인하실 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 규칙은 MIME 타입과 사용자가 지정한 확장자가 일치하는지까지 검증하지는 않습니다. 예를 들어, `mimes:png` 유효성 검증 규칙에서는, 파일 이름이 `photo.txt`라고 해도 그 파일의 내용이 실제로 올바른 PNG 형식이라면 유효하다고 간주됩니다. 만약 사용자가 지정한 파일 확장자까지 검증하고 싶다면 [extensions](#rule-extensions) 규칙을 사용하시기 바랍니다.

<a name="rule-min"></a>
#### min:_value_

검증하려는 필드는 최소 _value_ 이상이어야 합니다. 문자열, 숫자, 배열, 파일 역시 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증하려는 정수는 최소 _value_ 자리수 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증하려는 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증하려는 필드는 입력 데이터에 존재해서는 안 됩니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

만약 _anotherfield_ 필드가 지정한 _value_와 일치한다면, 검증하려는 필드는 반드시 입력 데이터에 없어야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

만약 _anotherfield_ 필드가 지정한 _value_와 일치하지 않는 경우에만, 검증하려는 필드는 입력 데이터에 없어야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

나열된 다른 필드 중 하나라도 존재하면, 검증하려는 필드는 입력 데이터에 없어야만 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

나열된 다른 모든 필드가 모두 존재하는 경우에만, 검증하려는 필드는 입력 데이터에 없어야만 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증하려는 필드는 지정한 값 목록에 포함되어 있지 않아야 합니다. `Rule::notIn` 메서드를 활용해 규칙을 좀 더 선언적으로 정의할 수도 있습니다.

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

검증하려는 필드는 지정한 정규 표현식과 일치하지 않아야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 해당 패턴은 반드시 `preg_match`에서 요구하는 포맷(구분자 포함)을 따라 작성해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`

> [!WARNING]
> `regex` 또는 `not_regex` 패턴에 파이프( | ) 문자가 들어가는 경우, 유효성 규칙을 배열로 지정해야 할 수 있습니다. 그렇지 않으면 예상치 못한 동작이 발생할 수 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증하려는 필드는 `null` 값을 가질 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

검증하려는 필드는 [숫자값](https://www.php.net/manual/en/function.is-numeric.php)이여야 합니다.

<a name="rule-present"></a>
#### present

검증하려는 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

만약 _anotherfield_ 필드가 지정한 _value_ 값과 같다면, 검증하려는 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_ anotherfield_ 필드가 지정한 _value_와 일치하지 않는 경우, 검증하려는 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

지정된 다른 필드 중 하나라도 존재하면, 검증하려는 필드는 반드시 입력 데이터에 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

지정된 다른 모든 필드가 존재하면, 검증하려는 필드는 반드시 입력 데이터에 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증하려는 필드는 입력 데이터에 없거나 "비어있어야" 합니다. 필드가 "비어 있다"고 간주되는 경우는 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 비어 있는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 나열된 값(_value_)과 일치하는 경우, 검증하려는 필드는 입력 데이터에 없어야 하거나 "비어있어야" 합니다. (비어 있는 경우의 기준은 위와 동일)

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 비어 있는 경우

</div>

복잡한 조건부 금지 로직이 필요하다면, `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 혹은 클로저를 인수로 받을 수 있으며, 클로저일 경우 해당 필드를 금지해야 할 경우 `true`, 아니면 `false`를 반환해야 합니다.

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

_ anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나와 같으면, 검증하려는 필드는 없어야 하거나 "비어있어야" 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_ anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나와 같으면, 검증하려는 필드는 없어야 하거나 "비어있어야" 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_ anotherfield_ 필드가 나열된 값(_value_)과 일치하지 않는 한, 검증하려는 필드는 없어야 하거나 "비어있어야" 합니다. (비어 있는 경우의 기준은 위와 동일)

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 비어 있는 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증하려는 필드가 없거나 비어 있지 않은 경우, _anotherfield_로 지정한 모든 필드가 없어야 하거나 비어있어야 합니다. (비어 있는 경우의 기준은 동일)

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 비어 있는 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증하려는 필드는 지정한 정규 표현식 패턴과 일치해야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 패턴은 반드시 적합한 구분자까지 포함하여 지정해야 하며, 예시: `'email' => 'regex:/^.+@.+$/i'`

> [!WARNING]
> `regex`와 `not_regex` 유효성 규칙 모두 파이프(`|`) 문자가 패턴에 들어간 경우, 규칙을 문자열로 연결하지 말고 반드시 배열로 지정해야 합니다.

<a name="rule-required"></a>
#### required

검증하려는 필드는 입력 데이터에 반드시 존재해야 하며, "비어있지" 않아야 합니다. 필드가 "비어 있다"고 간주되는 조건은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 비어 있는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 나열된 값(_value_)과 일치하는 경우, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

`required_if` 규칙의 조건이 더욱 복잡하다면, `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 혹은 클로저를 인수로 받을 수 있으며, 클로저일 경우 필드가 필수인지 여부에 따라 `true` 또는 `false`를 반환하면 됩니다.

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

_ anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나와 같다면, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_ anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나와 같다면, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_ anotherfield_ 필드가 나열된 값(_value_) 중 하나와 일치하지 않는 경우에만, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다. 또한, _anotherfield_ 필드는 _value_가 `null`이 아닌 이상 반드시 요청 데이터에 포함되어야 합니다. _value_가 `null`일 때(`required_unless:name,null`), 비교 필드가 `null`이거나 요청 데이터에 존재하지 않으면 검증하려는 필드는 필수가 아닙니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

지정한 다른 필드 중 하나라도 존재하고 비어있지 않으면, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

지정한 다른 모든 필드가 존재하고 비어있지 않은 경우에만, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

지정한 다른 필드가 하나라도 비어 있거나 존재하지 않는 경우, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

지정한 다른 모든 필드가 모두 비어 있거나 존재하지 않는 경우, 검증하려는 필드는 반드시 존재하고 비어있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증하려는 필드는 배열이어야 하며, 최소한 지정한 키들을 반드시 가지고 있어야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정한 _field_의 값과 검증하려는 필드의 값이 반드시 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증하려는 필드는 지정한 _value_와 정확히 일치하는 크기를 가져야 합니다. 문자열의 경우 _value_는 문자 수, 숫자의 경우 _value_는 그 값 자체(그리고 해당 속성은 `numeric` 또는 `integer` 규칙도 포함해야 함), 배열의 경우에는 원소의 개수, 파일의 경우에는 파일 크기(킬로바이트 단위)가 됩니다. 아래는 몇 가지 예시입니다.

```php
// 문자열이 반드시 12글자인지 확인...
'title' => 'size:12';

// 주어진 정수가 반드시 10인지 확인...
'seats' => 'integer|size:10';

// 배열이 반드시 5개의 항목을 가지는지 확인...
'tags' => 'array|size:5';

// 업로드된 파일이 정확히 512킬로바이트인지 확인...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증하려는 필드는 지정한 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증하려는 필드는 문자열이어야 합니다. 만약 `null`도 허용하려면 `nullable` 규칙을 같이 지정해야 합니다.

<a name="rule-timezone"></a>
#### timezone

검증하려는 필드는 `DateTimeZone::listIdentifiers` 메서드에 따라 올바른 타임존 식별자여야 합니다.

`DateTimeZone::listIdentifiers` 메서드가 허용하는 인자를 이 유효성 규칙에 전달할 수도 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증하려는 필드는 지정한 데이터베이스 테이블 내에 존재하면 안 됩니다.

**사용자 정의 테이블 / 컬럼 이름 지정하기:**

테이블명을 직접 지정하는 대신, Eloquent 모델명을 명시해 해당 모델의 테이블을 자동으로 참조하게 할 수 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션을 사용하면, 필드와 매핑되는 DB 컬럼명을 직접 지정할 수 있습니다. 이 옵션이 없을 땐, 검증하려는 필드명이 그대로 컬럼명으로 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**사용자 정의 데이터베이스 커넥션 지정하기:**

Validator가 수행하는 쿼리에 특정 데이터베이스 커넥션을 지정하고 싶다면, 테이블명 앞에 커넥션 이름을 붙이면 됩니다.

```php
'email' => 'unique:connection.users,email_address'
```

**Unique 규칙에서 특정 ID 무시하기:**

때로는 유니크 검증 시 특정 ID는 제외하고 싶을 수 있습니다. 예를 들어, "프로필 수정" 화면에서 사용자의 이름, 이메일, 위치를 수정할 때, 이메일 컬럼의 값이 유일한지 검사하고 싶지만, 사용자가 이메일 주소를 변경하지 않았을 경우, 자기 자신의 이메일 때문에 에러가 발생해서는 안 됩니다.

이때는 validator에게 해당 사용자의 ID를 무시하라고 지시하면 됩니다. 이를 위해 `Rule` 클래스를 활용해 규칙을 선언적으로 만들 수 있으며, 아래 예시에서는 유효성 검증 규칙들을 배열로 지정합니다.

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
> 사용자가 입력한 값을 그대로 `ignore` 메서드에 전달해서는 절대 안 됩니다. 항상 시스템 내부에서 생성된 고유 ID(예: 자동증분 값, Eloquent 모델의 UUID 등)만 사용해야 합니다. 그렇지 않으면 SQL 인젝션 공격에 취약해질 수 있습니다.

모델의 키 값을 직접 넘겨주는 대신, 모델 인스턴스를 통째로 넘길 수도 있습니다. 그러면 라라벨이 내부적으로 키 값을 자동 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

만약 테이블의 기본키가 `id`가 아니라면, `ignore` 메서드에 컬럼명을 두 번째 인수로 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로, `unique` 규칙은 검증하려는 속성명과 동일한 컬럼에서 중복 여부를 검사합니다. 만약 다른 컬럼명을 지정하려면, `unique` 메서드의 두 번째 인수로 컬럼명을 전달하면 됩니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 Where 절 조건 추가:**

`where` 메서드를 이용해 쿼리 조건을 더 추가할 수 있습니다. 예를 들어, `account_id`가 1인 레코드만 대상으로 하려면 다음과 같이 작성합니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Unique 체크 시 소프트 삭제된 레코드 무시하기:**

기본적으로 unique 규칙은 소프트 삭제된 레코드도 중복 체크에 포함합니다. 소프트 삭제된 레코드를 제외하고 중복을 검사하려면, `withoutTrashed` 메서드를 호출합니다.

```php
Rule::unique('users')->withoutTrashed();
```

만약 소프트 삭제 컬럼명이 `deleted_at`이 아니라면, `withoutTrashed` 메서드에 컬럼명을 인수로 넘기면 됩니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증하려는 필드는 모두 대문자이어야 합니다.

<a name="rule-url"></a>
#### url

검증하려는 필드는 유효한 URL이어야 합니다.

특정 URL 프로토콜만 허용하려면, 해당 프로토콜을 규칙 인수로 전달할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증하려는 필드는 [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID)이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증하려는 필드는 RFC 9562(버전 1, 3, 4, 5, 6, 7 또는 8) 형식의 UUID이어야 합니다.

지정한 UUID 버전의 규격과 일치하는지 검증할 수도 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 필드의 유효성 검증 건너뛰기

때로는, 어떤 필드가 특정 값을 갖고 있다면 다른 필드의 유효성 검증을 아예 하지 않고 싶을 수 있습니다. 이럴 때는 `exclude_if` 유효성 검증 규칙을 사용할 수 있습니다. 아래 예시에서는, `has_appointment` 필드가 `false`일 경우 `appointment_date`와 `doctor_name` 필드는 검증 대상에서 제외됩니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로, 어떤 필드가 특정 값을 가진 경우에만 유효성 검증을 하고 싶다면 `exclude_unless` 규칙을 사용할 수 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>

#### 존재할 때만 유효성 검사하기

특정 상황에서는, 데이터 내에 특정 필드가 존재할 때에만 유효성 검사를 수행하고 싶을 수 있습니다. 이럴 때는 간단하게 해당 필드의 규칙 목록에 `sometimes` 규칙을 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예시에서는, `$data` 배열에 `email` 필드가 있을 경우에만 해당 필드에 대한 유효성 검사가 실행됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드를 검사하려면 [옵션 필드에 대한 안내](#a-note-on-optional-fields)를 참고하시기 바랍니다.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검사

좀 더 복잡한 조건에 따라 유효성 검사 규칙을 추가하고 싶을 때가 있습니다. 예를 들어, 어떤 필드는 다른 필드의 값이 100보다 클 때만 필수로 만들고 싶을 수 있습니다. 또는, 특정 필드가 존재할 때에만 두 필드가 특정 값을 가져야 할 수도 있습니다. 이러한 조건부 유효성 규칙도 어렵지 않게 추가할 수 있습니다. 우선, 먼저 _항상 적용되는_ 규칙(static rules)로 `Validator` 인스턴스를 만듭니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

예를 들어, 이 웹 애플리케이션이 '게임 수집가'를 위한 것이라고 가정하겠습니다. 만약 어떤 사용자가 100개가 넘는 게임을 소유하고 있다고 등록했다면, 왜 그렇게 많은 게임을 갖고 있는지 설명을 받으려 할 수 있습니다. 예를 들어, 중고 게임 매장을 운영하거나, 단순히 수집이 취미일 수도 있습니다. 이러한 조건부 규칙은 `Validator` 인스턴스의 `sometimes` 메서드를 사용해 쉽게 추가할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인자는 조건부로 유효성 검사를 적용할 필드명입니다. 두 번째 인자는 적용할 규칙들의 목록입니다. 세 번째 인자로 넘기는 클로저가 `true`를 반환하면 해당 규칙이 추가됩니다. 이 방식을 활용하면 복잡한 조건부 유효성 검사를 간단히 구현할 수 있습니다. 아래와 같이 여러 필드에 동시에 조건부 유효성 검사를 적용할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 매개변수는 `Illuminate\Support\Fluent` 인스턴스이며, 여기에 유효성 검사 대상의 입력값이나 파일에 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 유효성 검사

때로는 중첩 배열 내에서, 인덱스를 알 수 없는 상태에서 다른 필드를 기준으로 유효성 검사를 해야 할 때도 있습니다. 이런 상황에서는 클로저의 두 번째 인자로, 유효성 검사가 수행되는 배열의 현재 항목을 받을 수 있습니다.

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

위에서 본 것처럼, 클로저의 `$input` 매개변수와 마찬가지로 `$item` 매개변수도 배열 데이터인 경우 `Illuminate\Support\Fluent`의 인스턴스입니다. 배열 데이터가 아닌 경우에는 문자열로 전달됩니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[배열 유효성 검사 규칙 문서](#rule-array)에서 설명했듯이, `array` 규칙은 허용되는 배열 키 목록을 지정할 수 있습니다. 만일 배열 내에 추가적인 키가 있으면, 유효성 검사가 실패합니다.

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

일반적으로, 배열 안에 허용할 키를 항상 명시하는 것이 좋습니다. 그렇지 않으면, 검증기의 `validate` 및 `validated` 메서드에서 배열 전체와 모든 키가(다른 중첩 배열 규칙으로 검증되지 않은 키까지도) 반환될 수 있습니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력값 유효성 검사

배열안에 중첩된 형태로 전달되는 폼 입력 필드에 대한 유효성 검사도 어렵지 않습니다. 배열 내부의 속성을 유효성 검사할 때는 "점 표기법(dot notation)"을 사용할 수 있습니다. 예를 들어, HTTP 요청에 `photos[profile]` 필드가 있다면, 다음과 같이 유효성 검사를 할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소에 대해 유효성 검사를 할 수도 있습니다. 예를 들어, 배열 입력 필드 내 각 이메일이 고유해야 한다는 조건을 검사하려면 다음과 같이 합니다.

```php
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

마찬가지로, [언어 파일에서 사용자 정의 유효성 메시지](#custom-messages-for-specific-attributes)를 지정할 때도 `*` 문자를 활용할 수 있어, 배열 기반 필드에 대해 단일 메시지를 손쉽게 사용할 수 있습니다.

```php
'custom' => [
    'person.*.email' => [
        'unique' => '각 사용자의 이메일 주소는 중복될 수 없습니다',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근하기

유효성 검사 규칙을 할당할 때, 특정 중첩 배열 요소의 값을 활용해야 할 수도 있습니다. 이럴 때는 `Rule::forEach` 메서드를 사용할 수 있습니다. 이 `forEach` 메서드는 유효성 검사 대상 배열 속성의 각 항목에 대해 클로저를 호출합니다. 클로저는 해당 배열 요소의 값과, 명확하게 확장된 전체 속성명을 인자로 받아옵니다. 그리고 클로저는 배열 요소에 적용할 규칙의 배열을 반환해야 합니다.

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
### 에러 메시지 인덱스와 순번 활용

배열을 유효성 검사할 때, 애플리케이션에서 보여주는 에러 메시지에서 어느 항목이 실패했는지 인덱스(또는 순서)를 표시하고 싶을 수 있습니다. 이런 경우, [사용자 정의 유효성 메시지](#manual-customizing-the-error-messages)에서 `:index`(0부터 시작)와 `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다.

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
    'photos.*.description.required' => '사진 #:position에 대한 설명을 입력하세요.',
]);
```

위 예시에서는, 두 번째 사진에 대해 유효성 검사가 실패하면 _"사진 #2에 대한 설명을 입력하세요."_ 라는 메시지가 사용자에게 보여집니다.

필요하다면 더 깊은 중첩의 인덱스와 순번을 `second-index`, `second-position`, `third-index`, `third-position` 등으로 사용할 수도 있습니다.

```php
'photos.*.attributes.*.string' => '사진 #:second-position에 잘못된 속성이 있습니다.',
```

<a name="validating-files"></a>
## 파일 유효성 검사

라라벨은 파일 업로드에 사용할 수 있는 다양한 유효성 검사 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 개별적으로 이러한 규칙을 지정해서 파일 유효성 검사를 할 수도 있지만, 라라벨에서는 더 편리한 유창한(fluent) 파일 유효성 검사 규칙 빌더도 제공합니다.

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
#### 파일 타입 유효성 검사

`types` 메서드를 사용할 때 단순히 파일 확장자만 지정하면 되지만, 이 메서드는 실제로 파일의 내용을 읽어 MIME 타입을 유추해서 체크합니다. 각 확장자에 대응되는 MIME 타입 전체 목록은 아래 링크에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 유효성 검사

파일 크기의 최소, 최대 값을 지정할 때는, 문자열로 단위를 함께 붙일 수도 있습니다. 지원되는 단위는 `kb`, `mb`, `gb`, `tb`입니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 유효성 검사

사용자가 업로드하는 이미지 파일에 대해 유효성 검사를 하려면, `File` 규칙의 `image` 생성자 메서드를 사용해서JPEG, PNG, BMP, GIF, WebP 등 이미지 파일만 허용하게 할 수 있습니다.

추가로, `dimensions` 규칙을 활용하면 이미지의 크기를 제한할 수도 있습니다.

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
> 이미지 크기 유효성 검사에 대한 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하세요.

> [!WARNING]
> 기본적으로, `image` 규칙은 XSS 취약성 위험 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 한다면, `allowSvg: true` 옵션을 `image` 규칙에 넘기면 됩니다: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(치수) 유효성 검사

이미지의 폭과 높이에 대한 유효성 검사를 하고 싶을 때도 있습니다. 예를 들어, 업로드한 이미지가 최소 1000픽셀 폭과 500픽셀 높이 이상이어야 한다면 아래와 같이 `dimensions` 규칙을 사용합니다.

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
> 이미지 크기 유효성 검사에 대한 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하세요.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검사

비밀번호의 복잡성을 쉽게 보장하려면, 라라벨의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체를 사용하면 최소 길이, 영문, 숫자, 특수문자, 대/소문자 혼합 등 비밀번호 복잡성 요구사항을 손쉽게 지정할 수 있습니다.

```php
// 8자 이상이어야 함...
Password::min(8)

// 영문자가 하나 이상 포함되어야 함...
Password::min(8)->letters()

// 대소문자가 각각 최소 하나 이상 포함되어야 함...
Password::min(8)->mixedCase()

// 숫자가 하나 이상 포함되어야 함...
Password::min(8)->numbers()

// 특수문자가 하나 이상 포함되어야 함...
Password::min(8)->symbols()
```

또한, 비밀번호가 공개적으로 유출된 적이 없는지도(`uncompromised` 메서드) 쉽게 확인할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로, `Password` 규칙 객체는 [k-익명성(k-Anonymity)](https://en.wikipedia.org/wiki/K-anonymity) 모델을 활용해서 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호 유출 여부를 확인하지만, 사용자의 개인정보나 보안은 보호됩니다.

기본적으로, 데이터 유출에 해당 비밀번호가 한 번이라도 포함되어 있다면 유출된 것으로 간주합니다. 이 임계값(threshold)은 `uncompromised` 메서드의 인자를 통해 조정할 수 있습니다.

```php
// 동일한 데이터 유출에서 3회 미만으로 나타난 경우만 허용...
Password::min(8)->uncompromised(3);
```

물론, 위 예시들의 메서드는 모두 체이닝해서 사용할 수 있습니다.

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

비밀번호에 대한 기본 유효성 검사 규칙을 애플리케이션의 한 곳에 모아서 지정하는 것이 더 편리할 수 있습니다. 이때는 `Password::defaults` 메서드를 사용하면 됩니다. 이 메서드는 클로저를 인자로 받으며, 이 클로저는 기본 설정을 반환해야 합니다. 일반적으로, 이 `defaults` 규칙은 애플리케이션 서비스 프로바이더의 `boot` 메서드 안에서 호출합니다.

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

이후 특정 비밀번호 필드에 기본 규칙을 적용할 때는, 인자 없이 `defaults` 메서드를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

경우에 따라, 기본 비밀번호 규칙에 추가적인 유효성 규칙을 함께 사용하고 싶을 수도 있습니다. 이럴 때는 `rules` 메서드를 활용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 사용자 정의 유효성 검사 규칙

<a name="using-rule-objects"></a>
### 규칙 객체 사용하기

라라벨은 다양한 유효성 검사 규칙을 기본으로 제공하지만, 직접 규칙을 만들어야 할 때도 있습니다. 사용자 정의 유효성 검사 규칙을 등록하는 한 가지 방법은 규칙 객체(rule object)를 사용하는 것입니다. 새로운 규칙 객체를 생성하려면, `make:rule` Artisan 명령어를 사용할 수 있습니다. 예를 들어, 입력 문자열이 모두 대문자인지 확인하는 규칙을 만들고 싶다면 다음과 같이 명령어를 실행합니다. 규칙 객체는 `app/Rules` 디렉터리에 생성됩니다. 이 디렉터리가 없으면, Artisan 명령어 실행 시 자동으로 만들어집니다.

```shell
php artisan make:rule Uppercase
```

규칙이 생성되면, 동작을 직접 구현해야 합니다. 규칙 객체는 `validate`라는 하나의 메서드만 필요합니다. 이 메서드는 속성명, 값, 그리고 실패 시 검증 에러 메시지를 전달받을 콜백을 인자로 받습니다.

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

규칙이 구현된 후에는, 인스턴스를 일반 유효성 검사 규칙과 함께 전달하여 사용할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 검사 메시지의 다국어 처리

`$fail` 클로저에 문자 메시지를 직접 지정하는 대신, [번역 문자열 키](/docs/12.x/localization)를 전달하고 라라벨이 에러 메시지를 번역하도록 할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면, 플레이스홀더 치환 값과 기본 언어를 첫 번째 및 두 번째 인자로 `translate` 메서드에 지정할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근

사용자 정의 유효성 검사 규칙 클래스에서 유효성 검사 중인 모든 데이터를 접근해야 한다면, 클래스에 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하면 됩니다. 이 인터페이스는 `setData` 메서드 구현을 요구하며, 라라벨이 자동으로 모든 유효성 검사 데이터를 전달해줍니다(유효성 검사 전에).

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

또는, 유효성 검사를 실제로 수행하는 Validator 인스턴스에 접근해야 할 경우에는 `ValidatorAwareRule` 인터페이스를 구현하면 됩니다.

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
### 클로저(Closure)로 사용자 정의 규칙 만들기

프로젝트 내에서 한 번만 사용할 커스텀 규칙이 필요하다면, 규칙 객체 대신 클로저를 사용할 수도 있습니다. 이 클로저는 속성명, 값, 그리고 실패 시 호출할 `$fail` 콜백을 인자로 받습니다.

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
### 암묵적 규칙(Implicit Rule)

기본적으로 유효성 검사 시, 속성이 존재하지 않거나 빈 문자열일 경우에는 일반 규칙은 물론 커스텀 규칙마저 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에 적용되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있더라도 루틴을 실행하도록 하려면 규칙 자체가 그 속성이 필수임을 **암시(implicit)** 해야 합니다. 새 암묵적 규칙 객체를 빠르게 만들려면, `make:rule` Artisan 명령어에 `--implicit` 옵션을 추가하세요.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙은 단지 해당 속성을 필수로 _암시_ 할 뿐입니다. 실제로 누락 또는 빈 속성을 에러로 처리할지 여부는 여러분의 규칙 구현에 달려 있습니다.