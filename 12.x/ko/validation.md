# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [옵션 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 형식](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 권한 부여](#authorizing-form-requests)
    - [에러 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 에러 백](#named-error-bags)
    - [에러 메시지 커스터마이즈](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부로 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 검증](#validating-nested-array-input)
    - [에러 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 업로드 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 오브젝트 사용하기](#using-rule-objects)
    - [클로저(Closures) 사용하기](#using-closures)
    - [암묵적 규칙(Implicit Rules)](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션으로 들어오는 데이터를 검증하기 위한 여러 다양한 방법을 제공합니다. 가장 일반적으로는 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 이용합니다. 하지만, 이 외에도 다양한 검증 방법에 대해 다룰 예정입니다.

라라벨은 데이터에 적용할 수 있는 편리한 유효성 검증 규칙들을 매우 다양하게 내장하고 있으며, 특정 데이터베이스 테이블의 값이 유니크한지까지도 쉽게 검증할 수 있습니다. 이 문서에서는 라라벨의 모든 유효성 검증 기능과 규칙에 대해 자세히 설명하므로, 여러분이 다양한 검증 기능을 모두 익힐 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기

라라벨의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 검증하고 에러 메시지를 사용자에게 표시하는 전반적인 예제를 살펴보겠습니다. 이 내용을 읽으시면 라라벨로 들어오는 요청 데이터를 어떻게 검증할 수 있는지 전체적인 흐름을 쉽게 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같이 라우트를 정의했다고 가정해봅니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

여기서, `GET` 라우트는 사용자에게 새로운 블로그 포스트 작성 폼을 보여주고, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위에서 정의한 라우트로 들어온 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 우선, `store` 메서드는 비워두겠습니다.

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

이제 `store` 메서드에 새 블로그 포스트를 검증하는 로직을 작성해보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용할 것입니다. 유효성 검증 기준을 통과하면 코드는 정상적으로 계속 실행되지만, 만약 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 올바른 에러 응답이 자동으로 사용자에게 반환됩니다.

일반적인 HTTP 요청에서 유효성 검증이 실패하면, 이전 URL로 자동 리디렉션이 이루어집니다. 만약 들어온 요청이 XHR(비동기 자바스크립트) 요청이라면, [유효성 검증 에러 메시지를 포함한 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작 원리를 이해하기 위해 `store` 메서드의 예시로 돌아가 보겠습니다.

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

위 예제에서처럼, 검증 규칙들은 `validate` 메서드에 배열 형태로 전달됩니다. 걱정하지 마세요. 사용 가능한 모든 유효성 검증 규칙은 [문서에 정리되어 있습니다](#available-validation-rules). 다시 한 번, 검증에 실패하면 적절한 응답이 자동으로 반환되며, 검증을 통과하면 컨트롤러가 정상적으로 실행됩니다.

또한, 검증 규칙을 단일 `|` 문자로 연결된 문자열이 아닌, 규칙 배열로도 지정할 수 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

추가로, 오류 메시지를 [이름이 지정된 에러 백](#named-error-bags)에 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 최초 유효성 검증 실패 시 중단하기

때때로, 어떤 속성(attribute)에서 첫 번째로 유효성 검증이 실패하면 이후의 검증 규칙을 더 이상 실행하지 않고 중단하고 싶을 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서는, 만약 `title` 속성에 대한 `unique` 규칙이 실패하면, `max` 규칙은 평가되지 않습니다. 규칙들은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes)에 대한 참고

만약 들어오는 HTTP 요청에 "중첩"된 필드 데이터가 있다면, 검증 규칙에서 "도트(dot) 표기법"을 사용해 이런 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드 이름에 실제로 점(`.`) 문자가 포함된 경우, 백슬래시(`\`)로 점을 이스케이프하여 이를 도트 표기법으로 해석하지 않도록 명시할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

이제, 만약 요청 필드가 주어진 규칙을 통과하지 못한다면 어떻게 될까요? 앞서 설명했듯, 라라벨은 자동으로 사용자를 원래 위치로 리디렉션합니다. 그리고 모든 유효성 검증 에러와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 [세션에 플래시](https://laravel.kr/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(이 미들웨어는 `web` 미들웨어 그룹에 포함됨)를 통해 `$errors` 변수가 어플리케이션의 모든 뷰에서 공유됩니다. 이 미들웨어가 적용되어 있으면 모든 뷰에서 `$errors` 변수를 항상 사용할 수 있으며, 안전하게 에러 정보를 출력할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 활용하는 방법은 [추가 문서](#working-with-error-messages)를 참고하세요.

따라서, 우리의 예시에서는, 검증에 실패하면 사용자는 컨트롤러의 `create` 메서드로 리디렉션되며, 뷰에서 에러 메시지를 다음과 같이 표시할 수 있습니다.

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
#### 에러 메시지 커스터마이즈

라라벨이 내장한 기본 유효성 검증 규칙들은 각자 에러 메시지를 애플리케이션의 `lang/en/validation.php` 파일에 가지고 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, Artisan 명령어 `lang:publish`를 사용해 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 유효성 검증 규칙에 대한 번역 엔트리가 있습니다. 이 메시지들은 여러분의 애플리케이션 요구에 따라 자유롭게 수정 가능하며, 필요하다면 다른 언어 디렉토리에 이 파일을 복사한 뒤 해당 언어로 번역해 사용할 수도 있습니다. 라라벨의 로컬라이제이션에 대한 자세한 내용은 [로컬라이제이션 공식 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 퍼블리시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이번 예제에서는 전통적인 폼 전송을 통해 데이터를 받아왔습니다. 하지만 많은 애플리케이션은 자바스크립트 기반 프론트엔드에서 XHR 요청을 받아 처리합니다. XHR 요청 환경에서 `validate` 메서드를 사용할 때, 라라벨은 리디렉션 응답을 생성하지 않습니다. 대신, [모든 유효성 검증 에러가 포함된 JSON 응답](#validation-error-response-format)을 반환하며, 이는 422 HTTP 상태 코드로 응답됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

주어진 속성에 대한 유효성 검증 에러 메시지가 있는지 빠르게 확인하려면 [Blade](/docs/12.x/blade)에서 `@error` 디렉티브를 사용할 수 있습니다. `@error` 디렉티브 안에서는 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다.

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

[이름이 지정된 에러 백](#named-error-bags)을 사용할 경우, `@error` 디렉티브의 두 번째 인자로 에러 백의 이름을 넘길 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

유효성 검증 실패로 인해 라라벨이 리디렉션 응답을 생성할 때, 프레임워크는 해당 요청의 모든 입력값을 자동으로 [세션에 플래시](https://laravel.kr/docs/12.x/session#flash-data)합니다. 이는 사용자가 입력했던 값을 다음 요청에서 쉽게 활용할 수 있도록 해주며, 사용자가 제출했던 폼을 다시 채울 때 편리하게 사용됩니다.

플래시된 이전 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 사용하면 됩니다. `old` 메서드는 [세션](/docs/12.x/session)에서 플래시된 입력값을 반환합니다.

```php
$title = $request->old('title');
```

라라벨은 전역적으로 `old` 헬퍼 함수도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값을 표시하려면 `old` 헬퍼를 사용하는 것이 보다 편리합니다. 해당 필드에 대한 이전 값이 없다면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 참고 사항

라라벨은 기본적으로 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 전역 미들웨어 스택에 포함하고 있습니다. 이로 인해, '옵션' 필드를 검증할 때 `null`(값 없음)이 유효한 값으로 처리되기를 원한다면, 해당 필드에 `nullable`을 명시적으로 추가해주어야 합니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서는, `publish_at` 필드는 `null`이거나, 올바른 날짜 문자열이어야 합니다. 만약 `nullable` 수식어가 규칙에 지정되지 않으면, 검증기는 `null` 값을 유효한 날짜로 인정하지 않습니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 형식

애플리케이션이 `Illuminate\Validation\ValidationException` 예외를 발생시키고, 들어온 HTTP 요청이 JSON 응답을 기대하는 경우, 라라벨은 자동으로 에러 메시지를 포맷하여 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래는 유효성 검증 에러 발생 시 반환되는 JSON 응답 예시입니다. 참고로 중첩된 에러 키는 "도트 표기법" 형식으로 평탄화되어 나타납니다.

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
## 폼 리퀘스트 유효성 검증

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성하기

좀 더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(form request)"를 생성하여 사용할 수 있습니다. 폼 리퀘스트는 자체적으로 유효성 검증 및 인가 로직을 포함하는 커스텀 리퀘스트 클래스입니다. 폼 리퀘스트 클래스는 `make:request` Artisan CLI 명령어로 쉽게 생성할 수 있습니다.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉토리에 위치합니다. 만약 이 디렉토리가 없다면, 위 명령어 실행 시 자동으로 생성됩니다. 라라벨이 생성한 폼 리퀘스트에는 `authorize`와 `rules` 두 가지 메서드가 포함되어 있습니다.

예상하셨겠지만, `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 나타내는 동작을 수행할 수 있는지 판단하고, `rules` 메서드는 요청 데이터에 적용해야 할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드 시그니처에 필요로 하는 의존성을 타입힌트 할 수 있습니다. 라라벨 [서비스 컨테이너](/docs/12.x/container)에서 자동으로 주입해줍니다.

그렇다면 실제로 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드의 인자로 해당 폼 리퀘스트를 타입힌트로 지정하기만 하면 됩니다. 폼 리퀘스트 객체는 컨트롤러가 실행되기 전에 미리 유효성 검증을 마치므로, 컨트롤러 코드가 검증 로직으로 지저분해질 걱정이 없습니다.

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

검증에 실패하면, 사용자는 자동으로 원래 위치로 리디렉션되며, 에러 정보가 세션에 플래시되어 뷰에서 표시할 수 있습니다. 만약 요청이 XHR 방식이라면, 422 상태 코드와 함께 [유효성 검증 에러가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에 실시간 폼 리퀘스트 유효성 검증을 추가하고 싶으신가요? [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행하기

경우에 따라, 기본 유효성 검증 이후에 추가 유효성 검사를 해야 할 수도 있습니다. 이때는 폼 리퀘스트의 `after` 메서드를 활용할 수 있습니다.

`after` 메서드는 유효성 검증 완료 후 실행되는 콜러블(콜백 함수 또는 클로저) 배열을 반환해야 합니다. 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 전달받아, 필요하다면 추가적인 에러 메시지를 등록할 수 있습니다.

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

설명했듯, `after` 메서드에서 반환하는 배열에는 호출 가능한 클래스(Invokable class)도 넣을 수 있습니다. 각 클래스의 `__invoke` 메서드에서는 `Illuminate\Validation\Validator` 인스턴스를 인자로 받습니다.

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
#### 최초 유효성 검증 실패 시 전체 검증 중단

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 하나의 검증 오류가 발생하자마자 이후 모든 속성의 유효성 검증을 중단하도록 지정할 수 있습니다.

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이즈

폼 리퀘스트 유효성 검증이 실패하면, 기본적으로 사용자를 원래 위치로 리디렉션합니다. 이 동작은 자유롭게 변경할 수 있습니다. `$redirect` 프로퍼티를 폼 리퀘스트에 정의하면, 원하는 URI로 리디렉션됩니다.

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 라우트 명으로 리디렉션하려면 `$redirectRoute` 프로퍼티를 사용할 수도 있습니다.

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 권한 부여

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 안에서 인증된 사용자가 실제로 특정 리소스를 수정할 권한(인가)이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 자신이 소유한 블로그 댓글만 수정할 수 있는지 확인할 수 있습니다. 이 메서드에서는 보통 [인가 게이트 및 정책](/docs/12.x/authorization)을 활용하게 됩니다.

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

모든 폼 리퀘스트는 라라벨 기본 Request 클래스를 상속하므로, `user` 메서드로 현재 인증된 사용자에 접근할 수 있습니다. 또한, 위 예시에서 사용한 `route` 메서드는 호출된 라우트의 URI 파라미터에 접근할 수 있게 해주며, 아래처럼 `{comment}`와 같은 파라미터에 접근할 수 있습니다.

```php
Route::post('/comment/{comment}');
```

따라서, [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하고 있다면, request의 속성으로 바인딩된 모델에 바로 접근할 수 있어 코드를 더 간결하게 만들 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

만약 `authorize` 메서드가 `false`를 반환하면, 403 상태 코드의 HTTP 응답이 자동으로 반환되며, 컨트롤러 메서드는 실행되지 않습니다.

요청에 대한 인가 로직을 애플리케이션의 다른 위치에서 처리하고 싶다면, `authorize` 메서드를 아예 삭제하거나 다음과 같이 무조건 `true`를 반환해도 됩니다.

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
> `authorize` 메서드 시그니처에 필요한 의존성을 타입힌트로 지정하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈

폼 리퀘스트에서 사용할 에러 메시지는 `messages` 메서드를 오버라이드하여 커스터마이즈할 수 있습니다. 이 메서드는 속성/규칙 키와 해당 에러 메시지가 들어 있는 배열을 반환해야 합니다.

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
#### 유효성 검증 속성 이름 커스터마이즈

라라벨의 내장 유효성 검증 에러 메시지 일부에는 `:attribute` 플레이스홀더가 사용됩니다. 해당 부분에 커스텀 속성명을 지정하고 싶다면 `attributes` 메서드를 오버라이드하여 속성명 배열을 반환하면 됩니다.

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
### 유효성 검증을 위한 입력 준비하기

유효성 검증 규칙을 적용하기 전에 넘어온 데이터를 가공(준비, 정제)할 필요가 있다면, `prepareForValidation` 메서드를 사용할 수 있습니다.

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

마찬가지로, 유효성 검증 통과 이후에도 데이터를 정규화해야 할 때는 `passedValidation` 메서드를 사용할 수 있습니다.

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

요청 객체의 `validate` 메서드를 사용하지 않고, 직접 validator 인스턴스를 생성하여 유효성 검증을 할 수도 있습니다. 이를 위해서는 `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 활용합니다. 이 메서드는 새로운 validator 인스턴스를 생성합니다.

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

`make` 메서드의 첫 번째 인자는 검증 대상 데이터이며, 두 번째 인자는 데이터에 적용해야 할 유효성 검증 규칙 배열입니다.

요청의 유효성 검증에 실패한 경우, `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 리디렉션 후 뷰에서 `$errors` 변수를 자동으로 사용할 수 있으므로, 쉽고 간편하게 사용자에게 에러를 표시할 수 있습니다. `withErrors`는 validator, `MessageBag`, 또는 PHP 배열을 인자로 받을 수 있습니다.

#### 최초 유효성 검증 실패 시 중단

`stopOnFirstFailure` 메서드를 사용하면, 하나의 검증 실패가 일어난 뒤 모든 속성에 대한 유효성 검증을 바로 중단하도록 할 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

만약 수동으로 validator 인스턴스를 생성하더라도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션 기능을 그대로 활용하고 싶다면, validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 검증 실패 시 사용자가 자동으로 리디렉션되거나, XHR 요청이라면 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

유효성 검증 실패 시 에러 메시지를 [이름이 지정된 에러 백](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러 백

한 페이지에 여러 개의 폼이 있는 경우, 각각의 폼에 대한 유효성 검증 에러가 저장될 `MessageBag`에 별도의 이름을 붙이고 싶을 수 있습니다. 이를 위해 `withErrors`에 두 번째 인자로 이름을 지정해주면 됩니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

그 후, 해당 이름이 붙은 `MessageBag` 인스턴스에 `$errors` 변수로 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈

필요하다면, validator 인스턴스에서 라라벨이 제공하는 기본 에러 메시지 대신, 원하는 커스텀 에러 메시지를 지정할 수 있습니다. 방법은 여러 가지가 있으며, 가장 먼저, `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지 배열을 전달하는 방법이 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예시에서 `:attribute` 플레이스홀더는 실제 검증 대상 필드명으로 치환됩니다. 유효성 검증 메시지에는 이 외에도 다양한 플레이스홀더를 사용할 수 있습니다. 예를 들면 다음과 같습니다.

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>

#### 특정 속성에 대한 커스텀 메시지 지정하기

때로는 특정 속성에만 사용자 정의 에러 메시지를 지정하고 싶을 수 있습니다. 이럴 때는 "점(dot)" 표기법을 사용할 수 있습니다. 우선 속성명을, 그 다음에 규칙을 점으로 구분해서 작성하면 됩니다.

```php
$messages = [
    'email.required' => '이메일 주소가 꼭 필요합니다!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 사용자 정의 속성 값 지정하기

라라벨의 기본 내장 에러 메시지에는 `:attribute` 자리 표시자가 포함되어 있어, 이 부분이 유효성 검사를 받는 필드 또는 속성 이름으로 교체됩니다. 특정 필드에 대해 이 자리 표시자를 대체할 값을 커스텀하고 싶다면, `Validator::make` 메서드의 네 번째 인자로 커스텀 속성 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검사 수행하기

때때로 최초 유효성 검증이 끝난 후에 추가적인 검증을 하고 싶을 때가 있습니다. 이럴 때는 validator의 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 클로저나 호출 가능한(callable) 객체의 배열을 받아, 모든 기본 유효성 검사가 끝난 뒤에 호출됩니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 인자로 받으므로, 필요하다면 추가로 에러 메시지를 등록할 수 있습니다.

```php
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

앞서 설명했듯이, `after` 메서드는 콜러블의 배열도 받을 수 있습니다. "after validation" 로직이 호출 가능한 클래스로 캡슐화되어 있다면, 이 방식이 특히 편리합니다. 각 클래스의 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 주입받아 사용할 수 있습니다.

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
## 유효성 검사된 입력값 활용하기

폼 리퀘스트 또는 수동으로 생성한 validator 인스턴스를 통해 들어온 요청 데이터를 유효성 검증한 후, 실제로 검증을 거친 데이터만 따로 얻고 싶은 경우가 많습니다. 이를 위해 여러 방법을 제공하고 있습니다. 우선, 폼 리퀘스트(혹은 validator 인스턴스)에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 유효성 검증을 통과한 데이터만 담은 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 리퀘스트나 validator 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체는 `only`, `except`, `all` 메서드를 제공하여, 검증된 데이터 배열에서 일부만, 혹은 전체를 쉽게 추출할 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

추가로, `Illuminate\Support\ValidatedInput` 인스턴스는 반복문을 사용할 수도 있고, 배열처럼 접근도 가능합니다.

```php
// 검증된 데이터를 반복문으로 순회할 수 있습니다.
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 직접 접근할 수 있습니다.
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 필드를 추가하고 싶다면, `merge` 메서드를 사용할 수도 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

[컬렉션](/docs/12.x/collections) 인스턴스로 변환해서 사용하고 싶다면, `collect` 메서드를 호출하면 됩니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 방법으로 에러 메시지를 다루기 편리한 `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 뷰에서 자동으로 사용할 수 있게 제공되는 `$errors` 변수 또한 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

특정 필드의 첫 번째 에러 메시지만 가져오려면, `first` 메서드를 사용하세요.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드에 대한 모든 메시지를 배열로 받고 싶다면, `get` 메서드를 사용하면 됩니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 폼 필드에 대한 유효성 검증이라면, `*` 문자를 사용하여 각 배열 요소의 에러 메시지를 모두 가져올 수도 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 필드의 모든 에러 메시지를 배열로 받고 싶을 때는 `all` 메서드를 이용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지가 있는지 확인하기

어떤 필드에 에러 메시지가 존재하는지 확인하려면, `has` 메서드를 사용하세요.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에 사용자 정의 메시지 지정하기

라라벨의 기본 내장 유효성 검사 규칙마다, 에러 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성하도록 안내할 수 있습니다.

`lang/en/validation.php` 파일 내부에는 각 유효성 검사 규칙에 대한 메시지 항목이 있습니다. 필요에 따라 이 메시지들을 자유롭게 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어 폴더로 복사해서 메시지를 애플리케이션 언어에 맞게 번역할 수도 있습니다. 라라벨의 로컬라이제이션(다국어 지원)에 대해 더 알아보고 싶다면, 전체 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 직접 커스터마이징하고 싶다면, `lang:publish` Artisan 명령어로 파일을 배포하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션의 유효성 검사 언어 파일에서, 특정 속성과 규칙 조합에 사용할 에러 메시지도 자유롭게 지정할 수 있습니다. 이를 위해 각 언어 파일(`lang/xx/validation.php`)의 `custom` 배열에 메시지 커스터마이징을 추가하면 됩니다.

```php
'custom' => [
    'email' => [
        'required' => '이메일 주소가 꼭 필요합니다!',
        'max' => '이메일 주소가 너무 깁니다!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

라라벨의 많은 내장 에러 메시지에는 `:attribute` 자리 표시자가 포함되어 있어, 해당 부분이 유효성 검증 중인 필드나 속성 이름으로 바뀝니다. 만약 유효성 검사 메시지에서 `:attribute` 부분을 원하는 값으로 변경하고 싶다면, 언어 파일(`lang/xx/validation.php`)의 `attributes` 배열에서 커스텀 속성 이름을 지정해주면 됩니다.

```php
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 직접 커스터마이징하고 싶다면, `lang:publish` Artisan 명령어로 파일을 배포하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

라라벨의 일부 내장 유효성 검사 규칙 에러 메시지에는 `:value` 자리 표시자가 포함되어, 현재 요청 속성의 값으로 바뀝니다. 하지만 때로는 `:value` 부분을 더 읽기 쉬운 형태로 커스텀해서 보여주고 싶을 수 있습니다. 예를 들어, 아래와 같이 `payment_type` 필드 값이 `cc`일 때 신용카드 번호가 필수인 유효성 검사 규칙을 생각해봅시다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 검사 규칙이 실패하면, 아래와 같은 에러 메시지가 나옵니다.

```text
The credit card number field is required when payment type is cc.
```

이때 `cc` 대신 사용자가 이해하기 쉬운 표현으로 보여주고 싶다면, 언어 파일(`lang/xx/validation.php`)의 `values` 배열을 아래와 같이 지정해줄 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => '신용카드'
    ],
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 직접 커스터마이징하고 싶다면, `lang:publish` Artisan 명령어로 파일을 배포하세요.

이렇게 값을 정의해두면, 유효성 검사 규칙은 다음과 같은 에러 메시지를 만들어줍니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙

아래는 사용 가능한 모든 유효성 검사 규칙과 기능에 대한 목록입니다.



#### 불린(Boolean) 관련

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### 문자열 관련

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

#### 숫자 관련

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

#### 배열 관련

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

#### 날짜 관련

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

#### 파일 관련

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

#### 데이터베이스 관련

<div class="collection-method-list" markdown="1">

[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

#### 유틸리티

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

유효성 검증 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이어야 합니다. 이 규칙은 "이용약관 동의" 등과 같은 필드를 검증할 때 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

유효성 검증 중인 필드는, `anotherfield` 값이 특정 값과 일치할 때 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이어야 합니다. 역시 "이용약관 동의" 등과 유사한 필드에 쓸 수 있습니다.

<a name="rule-active-url"></a>
#### active_url

검증 중인 필드는 PHP의 `dns_get_record` 함수 기준으로, 유효한 A 또는 AAAA 레코드를 가져야 합니다. 전달된 URL의 호스트명은 PHP의 `parse_url` 함수로 추출된 후, `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

해당 필드는 특정 날짜 이후의 값이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어, 유효한 `DateTime` 인스턴스로 처리됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`으로 평가할 날짜 문자열 대신, 비교할 다른 필드명을 지정하여 사용할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

더 편리하게는, date 기반 규칙을 유창하게 작성할 수 있는 `date` 규칙 빌더를 이용할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드를 사용해서, 날짜가 오늘 이후(혹은 오늘 이후이거나 같은 날짜)임을 더 자연스럽게 표현할 수도 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

해당 필드는 지정된 날짜 이후이거나, 바로 그 날짜의 값이어야 합니다. 자세한 동작은 [after](#rule-after) 규칙을 참고하세요.

date 기반의 플루언트 규칙 빌더를 사용할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검사 규칙은, 해당 필드가 여러 개의 유효성 검사 규칙 세트 중 하나라도 통과하면 유효로 판단합니다. 예를 들면, 아래 규칙은 `username` 필드가 이메일이거나, 6자 이상 알파벳・숫자・대시로 이뤄져 있을 때 통과시킵니다.

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

해당 필드는 모두 유니코드 알파벳 문자([`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=))이어야 합니다.

만약 ASCII 범위(`a-z`, `A-Z`) 문자만 허용하려면, 검증 규칙에서 `ascii` 옵션을 추가하세요.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

해당 필드는 모두 유니코드 알파벳, 숫자([`\p{L}`], [`\p{M}`], [`\p{N}`]), 그리고 ASCII 대시(`-`), 밑줄(`_`) 문자로만 구성되어야 합니다.

ASCII 범위의 문자 및 기호(`a-z`, `A-Z`, `0-9`)만 허용하고 싶다면, `ascii` 옵션을 사용하면 됩니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

해당 필드는 모두 유니코드 알파벳, 숫자([`\p{L}`], [`\p{M}`], [`\p{N}`])로만 구성되어야 합니다.

ASCII 범위(`a-z`, `A-Z`, `0-9`)만 허용하려면, `ascii` 옵션을 추가하세요.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

해당 필드는 PHP의 `array` 여야 합니다.

추가적인 값을 `array` 규칙에 지정할 경우, 입력 배열의 각 키가 규칙에 명시된 목록에 반드시 포함되어 있어야 합니다. 예시에서, 입력 배열의 `admin` 키는 규칙에 명시된 값이 아니므로 잘못된 값이 됩니다.

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

일반적으로는, 배열 내에서 허용되는 키를 항상 명확히 지정해두는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

해당 필드는 완전히 7비트 ASCII 문자로만 이루어져 있어야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드에서 첫 번째 유효성 검사 실패가 발생하면, 그 이후의 규칙 검사는 중지합니다.

`bail` 규칙은 특정 필드에 한해 첫 번째 실패만 감지하면 유효성 검사를 멈추는 반면, `stopOnFirstFailure` 메서드는 어떠한 필드에서든 한 번이라도 실패가 발생하면 나머지 모든 속성의 검증을 즉시 중단합니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

해당 필드는 지정된 날짜 이전의 값이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어, 유효한 `DateTime` 인스턴스로 처리됩니다. 또한, [after](#rule-after) 규칙처럼 비교 대상이 될 다른 필드명을 지정할 수도 있습니다.

date 기반의 플루언트 규칙 빌더를 사용할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`와 `todayOrBefore` 메서드를 활용하면, 날짜가 오늘 이전(또는 오늘 이하)임을 직관적으로 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

해당 필드는 지정한 날짜 이전이거나 같은 값이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어, 유효한 `DateTime` 인스턴스로 처리됩니다. [after](#rule-after) 규칙과 마찬가지로, 비교할 다른 필드명을 지정할 수도 있습니다.

date 기반의 플루언트 규칙 빌더를 사용할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

해당 필드는 _min_과 _max_ (포함) 사이 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 크기가 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

해당 필드는 불린 값으로 변환될 수 있어야 합니다. `true`, `false`, `1`, `0`, `"1"`, `"0"` 값이 허용됩니다.

보다 엄격하게, 값이 반드시 `true` 또는 `false`일 때만 유효로 인정하려면 `strict` 파라미터를 추가할 수 있습니다.

```php
'foo' => 'boolean:strict'
```

<a name="rule-confirmed"></a>
#### confirmed

해당 필드와 `{field}_confirmation` 필드가 동일해야 합니다. 예를 들어, `password` 필드라면, 반드시 `password_confirmation` 입력 필드도 함께 존재하고 그 값이 일치해야 합니다.

커스텀 확인 필드명(confirmation field name)도 지정할 수 있습니다. 예를 들어, `confirmed:repeat_username` 규칙은 `repeat_username` 필드가 검증 대상 필드와 일치하는지 확인합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

해당 필드는 반드시 전달된 모든 값들이 포함되어 있는 배열이어야 합니다. 이 규칙은 보통 배열을 `implode`해서 규칙 문자열 작성이 번거로운데, `Rule::contains` 메서드로 더욱 유창하게 작성할 수 있습니다.

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

해당 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 추가로, 규칙의 첫 번째 파라미터로 [인증 가드](/docs/12.x/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

해당 필드는 PHP의 `strtotime` 함수로 판별할 때 유효한, 상대적(relative)이 아닌 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

해당 필드는 지정된 날짜 값과 정확히 같아야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어, 유효한 `DateTime` 인스턴스로 처리됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

해당 필드는 지정된 _formats_ 중 하나와 일치해야 합니다. 날짜 필드를 검증할 때는 반드시 `date` 또는 `date_format` 규칙 둘 중 하나만 사용해야 하며, 둘을 함께 쓰는 것은 권장되지 않습니다. 이 유효성 검증 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 포맷을 사용할 수 있습니다.

플루언트 date 규칙 빌더로도 편하게 규칙을 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>

#### decimal:_min_,_max_

검증 대상 필드는 숫자여야 하며, 지정된 소수 자릿수를 가져야 합니다.

```php
// 정확히 소수점 둘째 자리까지(예: 9.99) 이어야 합니다...
'price' => 'decimal:2'

// 소수점 둘째 자리에서 넷째 자리까지 허용됩니다...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

검증 대상 필드는, 다른 검증 필드가 지정한 값과 같으면 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수는 정확히 _value_ 길이여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 대상 정수의 길이는 _min_에서 _max_ 사이여야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 규칙의 파라미터로 지정된 이미지 크기 요건을 충족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건은 다음과 같습니다: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

_ratio_(비율) 제약 조건은 너비를 높이로 나눈 값입니다. 분수(`3/2`)나 실수(`1.5`)로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

이 규칙은 여러 개의 인자가 필요하므로, `Rule::dimensions` 메서드를 사용해 규칙을 플루언트하게 작성하는 것이 더 편리할 때가 많습니다.

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

배열을 검증할 때, 대상 필드는 중복된 값을 가질 수 없습니다.

```php
'foo.*.id' => 'distinct'
```

distinct 규칙은 기본적으로 느슨한(비엄격) 변수 비교를 사용합니다. 엄격한 비교가 필요하다면, 검증 규칙 정의에 `strict` 파라미터를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 차이를 무시하게 하고 싶다면 `ignore_case`를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 끝나서는 안 됩니다.

<a name="rule-email"></a>
#### email

검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 검증 규칙은 이메일 주소 검증을 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 검증기가 적용되며, 다른 검증 스타일도 사용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예제에서는 `RFCValidation`과 `DNSCheckValidation`이 적용됩니다. 사용 가능한 모든 검증 스타일은 다음과 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)를 기준으로 이메일을 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)를 바탕으로 이메일을 검증하며, 경고(예: 마지막에 오는 점, 연속된 여러 점)가 발견될 경우 실패합니다.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 동형 이의어(Homograph) 또는 속이는 Unicode 문자가 이메일에 포함되어 있지 않은지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일 유효성을 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수 기준으로, 일부 Unicode 문자를 허용하면서 이메일 유효성을 확인합니다.

</div>

편의를 위해 플루언트 규칙 빌더를 사용해 이메일 검증 규칙을 만들 수도 있습니다.

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
> `dns` 및 `spoof` 검증을 사용하려면 PHP의 `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 클래스 기반 규칙으로, 검증 대상 필드가 유효한 열거형(enum) 값을 포함하는지 확인합니다. `Enum` 규칙에는 해당 enum 클래스명을 생성자 인자로 줍니다. 기본 타입 값을 검증할 경우, `Enum` 규칙에 백킹된(값이 있는) Enum을 지정해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`와 `except` 메서드를 사용하면, 유효한 enum 케이스를 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용하면, 조건부로 `Enum` 규칙을 수정할 수 있습니다.

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

검증 대상 필드는 `validate`, `validated` 메서드를 사용해 반환될 요청 데이터에서 제외(exclude)됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

다른 필드가 _value_와 같을 경우, 검증 대상 필드는 `validate`, `validated` 메서드를 사용해 반환될 요청 데이터에서 제외됩니다.

복잡한 조건의 제외 로직이 필요하다면 `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불린값 또는 클로저를 인자로 받아, 클로저의 결과가 `true`일 때 필드가 제외됩니다.

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

검증 대상 필드는, _anotherfield_가 _value_와 같지 않으면 `validate`, `validated` 메서드를 통해 반환될 요청 데이터에서 제외됩니다. 만약 _value_가 `null`(`exclude_unless:name,null`)이라면, 비교 필드가 `null`이거나 요청 데이터에 해당 필드가 없을 때만 제외됩니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

만약 _anotherfield_ 필드가 존재하면, 검증 대상 필드는 `validate`, `validated` 메서드를 통해 반환될 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

_ anotherfield_ 필드가 존재하지 않을 경우, 검증 대상 필드는 `validate`, `validated` 메서드를 통해 반환될 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 대상 필드는 지정된 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 지정하지 않으면, 필드명이 자동으로 사용됩니다. 즉, 위의 경우에는 데이터베이스의 `states` 테이블에 `state` 칼럼이 요청의 `state` 값과 일치하는 레코드가 있는지 검증하게 됩니다.

<a name="specifying-a-custom-column-name"></a>
#### 커스텀 컬럼명 지정

검증 규칙에서, 데이터베이스 테이블명 다음에 컬럼명을 명시적으로 지정할 수도 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

특정 데이터베이스 커넥션을 지정해서 `exists` 쿼리를 실행해야 할 때는, 테이블명 앞에 커넥션명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, Eloquent 모델을 지정하여 해당 모델의 테이블명을 기준으로 참조할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

검증 규칙이 실행하는 쿼리를 커스터마이징하고 싶다면, `Rule` 클래스를 사용해서 규칙을 플루언트하게 정의할 수 있습니다. 아래 예제에서는, 구분자 `|` 대신 배열로 규칙을 지정하는 방법도 보여줍니다.

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

`Rule::exists` 메서드로 생성한 `exists` 규칙에, 두 번째 인자로 컬럼명을 전달해 사용할 컬럼을 명확히 지정할 수도 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

배열 값 중, 각 요소가 모두 데이터베이스에 존재하는지 검증하려면, `exists` 규칙과 [`array`](#rule-array) 규칙을 함께 적용하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

위처럼 두 규칙이 적용된 경우, 라라벨은 지정된 테이블에서 모든 값의 존재 여부를 한 번의 쿼리로 자동 확인합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 대상 파일은 지정한 확장자 중 하나를(사용자 배정 확장자) 가져야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일의 사용자 부여 확장자만으로 검증에 의존해서는 안 됩니다. 이 규칙은 보통 [mimes](#rule-mimes)나 [mimetypes](#rule-mimetypes) 규칙과 반드시 함께 사용해야 합니다.

<a name="rule-file"></a>
#### file

검증 대상 필드는 정상적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

검증 대상 필드는 존재할 경우 비어 있지 않아야 합니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 대상 필드는 주어진 _field_ 값 또는 _value_ 값보다 커야 합니다. 두 필드는 동일한 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 처리/비교합니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 대상 필드는 주어진 _field_ 혹은 _value_ 이상이어야 합니다. 두 필드는 타입이 같아야 하며, 문자열, 숫자, 배열, 파일 등은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

검증 대상 필드는 [16진수(hexadecimal)](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값이어야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지여야 하며, (jpg, jpeg, png, bmp, gif, webp 중 하나여야 합니다).

> [!WARNING]
> image 규칙은 기본적으로 SVG 파일을 허용하지 않습니다(XSS 공격 가능성 때문). SVG 파일을 허용하려면 `image` 규칙에 `allow_svg` 지시어(`image:allow_svg`)를 추가하면 됩니다.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 대상 필드는 주어진 값 목록 내에 포함되어야 합니다. 이 규칙은 종종 배열을 `implode` 해야 하므로, `Rule::in` 메서드를 사용해 플루언트하게 규칙을 만들 수 있습니다.

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

`in` 규칙이 `array` 규칙과 함께 사용되면, 입력 배열의 각 값이 `in` 규칙에 지정된 값 목록에 모두 포함되어야 합니다. 아래 예제에서 입력 배열에 포함된 `LAS`는 `in` 규칙의 허용 목록에 없기 때문에 유효하지 않습니다.

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

검증 대상 필드는 _anotherfield_ 필드의 값들 중 하나와 일치해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 대상 필드는 최소한 주어진 _values_ 중 하나를 키로 가진 배열이어야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증 대상 필드는 정수여야 합니다.

> [!WARNING]
> 이 검증 규칙은 입력값이 "integer" 변수 타입인지까지 확인하지 않고, PHP의 `FILTER_VALIDATE_INT`로 수용 가능한 종류의 값인지만 판별합니다. 입력이 실제 숫자인지까지 확실히 검증하고 싶다면 [numeric](#rule-numeric) 규칙도 함께 사용하시기 바랍니다.

<a name="rule-ip"></a>
#### ip

검증 대상 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

검증 대상 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증 대상 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증 대상 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증 대상 필드는 주어진 _field_ 값보다 작아야 합니다. 두 필드는 동일 타입이어야 하며, 문자열, 숫자, 배열, 파일 등은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 대상 필드는 주어진 _field_ 값 이하이어야 합니다. 두 필드는 타입이 같아야 하며, 문자열, 숫자, 배열, 파일 등은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 대상 필드는 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증 대상 필드는 리스트인 배열이어야 합니다. 배열의 키가 0부터 `count($array) - 1`까지 연속된 정수여야 리스트로 간주됩니다.

<a name="rule-mac"></a>
#### mac_address

검증 대상 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 대상 필드는 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 등은 [size](#rule-size) 규칙과 같은 방식으로 검증됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 대상 정수는 최대 _value_ 길이(자리수)를 가져야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 대상 파일은 주어진 MIME 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

파일의 MIME 타입은 업로드된 파일의 내용을 직접 읽어 판단하며, 클라이언트가 보낸 MIME 타입과 다를 수도 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 대상 파일은 지정된 확장자에 대응하는 MIME 타입이어야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하더라도, 이 규칙은 실제로 파일의 내용을 읽어 MIME 타입을 판별하여 검사합니다. 전체 MIME 타입 및 이에 대응하는 확장자 목록은 아래 링크에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 검증 규칙은 MIME 타입과 사용자가 부여한 확장자가 일치하는지까지 확인하지는 않습니다. 예를 들어, `photo.txt`라는 파일명이라도 파일의 실제 내용이 PNG 포맷이면 `mimes:png` 규칙에서는 유효한 PNG 이미지로 간주됩니다. 사용자 부여 확장자도 검증하고 싶다면, [extensions](#rule-extensions) 규칙을 함께 사용하세요.

<a name="rule-min"></a>
#### min:_value_

검증 대상 필드는 최소 _value_ 이상이어야 합니다. 문자열, 숫자, 배열, 파일 등은 [size](#rule-size) 규칙과 동일하게 처리됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 대상 정수는 최소 _value_ 길이(자리수)를 가져야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증 대상 필드는 입력 데이터에 포함되어 있지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

만약 _anotherfield_ 필드가 _value_ 중 하나와 같다면, 검증 대상 필드는 포함되어 있지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_ anotherfield_ 필드가 _value_ 중 하나와 같지 않다면, 검증 대상 필드는 포함되어 있지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

지정한 필드 중 하나라도 존재하는 경우에만, 검증 대상 필드는 존재해서는 안 됩니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

모든 지정한 필드가 존재하는 경우에만, 검증 대상 필드는 존재해서는 안 됩니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 대상 필드는 주어진 값 목록에 포함되어서는 안 됩니다. `Rule::notIn` 메서드를 사용해 플루언트하게 규칙을 만들 수 있습니다.

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

검증 대상 필드는 지정한 정규 표현식과 일치하지 않아야 합니다.

내부적으로는 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 형식(유효한 구분자 포함)을 따라야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴에서, 정규 표현식에 `|` 문자가 포함된 경우, 구분자 `|` 대신 배열로 규칙을 지정하는 것이 필요할 수 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증 대상 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

검증 대상 필드는 [숫자형(numeric)](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<a name="rule-present"></a>
#### present

검증 대상 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 _value_ 중 하나와 같으면, 검증 대상 필드는 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_ anotherfield_ 필드가 _value_ 중 하나와 다를 때, 검증 대상 필드는 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

지정된 필드들 중 하나라도 존재하면, 검증 대상 필드 또한 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

모든 지정된 필드가 존재하면, 검증 대상 필드 또한 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 대상 필드는 누락(missing)되어 있거나 비어 있어야 합니다. "비어 있다"는 것은 아래 조건 중 하나에 해당할 때를 말합니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 비어 있는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 _value_ 중 하나와 같을 때, 검증 대상 필드는 누락되어 있거나 비어 있어야 합니다. "비어 있다"의 정의는 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 빈 경우

</div>

복잡한 조건부 금지(조건부 미허용)가 필요하다면 `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불린값이나 클로저를 받아, 클로저가 반환하는 값이 `true`이면 필드가 금지됩니다.

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

_ anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나일 경우, 검증 대상 필드는 누락되어 있거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_ anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나일 때, 검증 대상 필드는 누락되거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_ anotherfield_ 필드가 _value_ 중 하나와 같지 않은 경우, 검증 대상 필드는 누락되거나 비어 있어야 합니다. "비어 있다"는 아래 조건 중 하나에 해당할 때를 의미합니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 빈 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 대상 필드가 누락되지 않았거나 비어 있지 않으면, _anotherfield_에 지정된 모든 필드는 누락되거나 비어 있어야 합니다. "비어 있다" 정의는 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 빈 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증 대상 필드는 지정된 정규 표현식과 일치해야 합니다.

내부적으로는 PHP의 `preg_match` 함수를 사용합니다. 패턴 지정 시에는 `preg_match`에서 요구하는 유효한 구분자를 포함해서 작성해야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`

> [!WARNING]
> `regex`, `not_regex` 패턴을 사용할 때, 정규식에 `|` 문자가 포함되어 있다면, 배열로 규칙을 지정하는 것이 필요할 수 있습니다.

<a name="rule-required"></a>
#### required

검증 대상 필드는 입력 데이터에 반드시 존재해야 하며, 비어 있으면 안 됩니다. "비어 있다"는 다음 항목 중 하나가 해당될 때를 의미합니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드된 파일의 경로가 없는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_ anotherfield_ 필드가 _value_ 중 하나와 같으면, 검증 대상 필드는 반드시 존재해야 하고 비어 있으면 안 됩니다.

`required_if` 규칙에 대해 더 복잡한 조건식을 만들고 싶을 때는 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불린값 또는 클로저를 인자로 받아, 클로저 결과가 `true`이면 검증 대상 필드가 필수로 지정됩니다.

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

해당 필드는, 검증 대상인 _anotherfield_ 필드의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`일 경우 반드시 존재해야 하며 비어 있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

해당 필드는, 검증 대상인 _anotherfield_ 필드의 값이 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`일 경우 반드시 존재해야 하며 비어 있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

해당 필드는, _anotherfield_ 필드의 값이 지정된 _value_와 같지 않은 경우 반드시 존재하며 비어 있지 않아야 합니다. 또한 _anotherfield_ 필드는 _value_가 `null`이 아닌 이상, 반드시 요청 데이터 내에 존재해야 합니다. 만약 _value_가 `null`(`required_unless:name,null`)이라면, 비교 대상 필드가 `null`이거나 요청 데이터에 존재하지 않을 때를 제외하고, 해당 필드는 반드시 필요하게 됩니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

해당 필드는 지정한 다른 필드들 중 하나라도 존재하고 비어 있지 않으면 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

해당 필드는 지정한 다른 모든 필드가 존재하고 비어 있지 않을 때에만 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

해당 필드는, 지정한 다른 필드 중 하나라도 비어 있거나 존재하지 않는 경우에만 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

해당 필드는, 지정한 모든 필드가 비어 있거나 존재하지 않을 때에만 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

해당 필드는 배열이어야 하며, 지정된 키들을 모두 반드시 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정된 _field_의 값이 검증 대상 필드와 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

해당 필드의 크기가 주어진 _value_와 정확히 일치해야 합니다. 문자열의 경우, _value_는 글자 수를 의미합니다. 숫자 데이터는 _value_와 동일한 정수여야 하며(이때 해당 필드에도 `numeric` 또는 `integer` 규칙이 있어야 합니다), 배열의 경우 요소 개수가 _size_에 해당합니다. 파일은 킬로바이트 단위의 파일 크기가 _size_와 일치해야 합니다. 다음은 예시입니다.

```php
// 문자열이 정확히 12글자인지 검증...
'title' => 'size:12';

// 주어진 정수가 10인지 검증...
'seats' => 'integer|size:10';

// 배열이 정확히 5개의 요소를 가지는지 검증...
'tags' => 'array|size:5';

// 업로드된 파일이 정확히 512킬로바이트인지 검증...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

해당 필드는 지정된 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

해당 필드는 문자열이어야 합니다. 만약 필드의 값이 `null`이어도 허용하고 싶다면, `nullable` 규칙을 함께 지정해야 합니다.

<a name="rule-timezone"></a>
#### timezone

해당 필드는 `DateTimeZone::listIdentifiers` 메서드 기준으로 유효한 타임존 식별자여야 합니다.

또한 [`DateTimeZone::listIdentifiers` 메서드가 허용하는 인자들](https://www.php.net/manual/en/datetimezone.listidentifiers.php)을 이 검증 규칙에 함께 전달할 수 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

해당 필드는 지정된 데이터베이스 테이블에 존재하지 않아야 합니다.

**커스텀 테이블/컬럼명 지정하기**

테이블명을 직접 지정하는 대신, Eloquent 모델명을 지정하여 해당 테이블명을 자동으로 결정할 수도 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션을 사용해 필드가 연결된 데이터베이스 컬럼을 명시할 수 있습니다. 만약 `column` 옵션을 지정하지 않으면, 검증 대상 필드의 이름이 컬럼으로 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**커스텀 데이터베이스 커넥션 사용**

때때로 Validator가 쿼리할 때 사용할 데이터베이스 커넥션을 직접 지정해야 할 때가 있습니다. 이때는 테이블명 앞에 커넥션명을 추가하십시오.

```php
'email' => 'unique:connection.users,email_address'
```

**특정 ID를 무시하도록 Unique 규칙 강제하기**

특정 ID를 unique 검증에서 무시하고 싶을 때가 있습니다. 예를 들어 "프로필 수정" 화면에서 사용자의 이름, 이메일, 위치 등의 필드를 수정할 때, 이메일의 유일성을 검증해야 합니다. 하지만 사용자가 이메일을 변경하지 않은 경우에는 이미 그 이메일을 소유하고 있으므로 중복 오류가 발생하지 않아야 합니다.

사용자의 ID를 무시하도록 validator에 지시하려면, `Rule` 클래스를 사용하여 규칙을 유연하게 정의할 수 있습니다. 이 예시에서는 규칙을 `|` 문자 대신 배열로 지정하고 있습니다.

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
> 사용자 요청으로부터 받은 값을 `ignore` 메서드에 전달해서는 안 됩니다. 대신 시스템이 자동으로 생성한 고유 ID(예: 자동 증가 ID 또는 Eloquent 모델의 UUID)만 전달해야 하며, 그렇지 않으면 SQL 인젝션 공격에 취약해질 수 있습니다.

`ignore` 메서드에 일반적인 모델 키의 값 대신 전체 모델 인스턴스를 전달할 수도 있습니다. 그러면 Laravel이 해당 인스턴스에서 키 값을 자동으로 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

테이블에서 기본 키 컬럼명이 `id`가 아니라면, `ignore` 호출 시 컬럼명을 두 번째 인자로 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 현재 검증 대상 필드와 이름이 일치하는 컬럼의 유일성을 확인합니다. 하지만 두 번째 인자로 다른 컬럼명을 명시할 수도 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 where 절 지정하기**

`where` 메서드를 사용해 쿼리에 추가로 조건을 붙일 수 있습니다. 예를 들어 `account_id` 컬럼 값이 1인 레코드만 검사하도록 쿼리를 범위 제한할 수 있습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**unique 체크 시 소프트 삭제 레코드 제외**

기본적으로 unique 규칙은 소프트 삭제된 레코드도 포함하여 유일성을 검사합니다. 소프트 삭제된 레코드는 검사 대상에서 제외하고 싶다면 `withoutTrashed` 메서드를 호출하면 됩니다.

```php
Rule::unique('users')->withoutTrashed();
```

만약 소프트 삭제 컬럼명이 `deleted_at`이 아니라면, `withoutTrashed` 호출 시 컬럼명을 인자로 전달하십시오.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

해당 필드는 대문자여야 합니다.

<a name="rule-url"></a>
#### url

해당 필드는 올바른 URL 형식이어야 합니다.

특정 URL 프로토콜만 허용하고 싶다면, 검증 규칙의 파라미터로 프로토콜을 전달할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

해당 필드는 [ULID(Universally Unique Lexicographically Sortable Identifier)](https://github.com/ulid/spec) 형식의 유효한 값이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

해당 필드는 RFC 9562(버전 1, 3, 4, 5, 6, 7, 8)의 UUID(범용 고유 식별자) 형식이어야 합니다.

또한 UUID의 버전을 같이 지정해 검증할 수도 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 검증 건너뛰기

다른 필드의 값이 특정 값일 때, 어떤 필드에 대한 검증을 건너뛰고 싶을 때가 있습니다. 이럴 때는 `exclude_if` 검증 규칙을 사용할 수 있습니다. 아래 예제에서 `has_appointment` 값이 `false`일 경우, `appointment_date`와 `doctor_name` 필드에 대한 검증이 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

또는, `exclude_unless` 규칙을 사용해, 다른 필드가 특정 값이 아닐 때만 검증을 건너뛸 수도 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 필드가 존재할 때에만 검증하기

어떤 상황에서는 특정 필드가 데이터에 존재하는 경우에만 검증을 수행하고 싶을 수 있습니다. 빠르게 구현하려면, 규칙 목록에 `sometimes` 규칙을 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예제에서 `email` 필드는 `$data` 배열에 있을 때에만 검증됩니다.

> [!NOTE]
> 항상 존재하되 비어 있을 수 있는 필드를 검증하고 싶다면, [선택적 필드에 관한 이 노트](#a-note-on-optional-fields)를 참고하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

더 복잡한 조건문을 기반으로 검증 규칙을 동적으로 추가해야 할 때가 있습니다. 예를 들어, 한 필드가 100보다 큰 경우에 다른 필드를 필수로 요구한다거나, 두 필드가 특정 값이 되려면 또 다른 필드가 반드시 존재해야 할 수도 있습니다. 이런 검증도 어렵지 않게 구현할 수 있습니다. 먼저, 절대 변하지 않는 _고정 규칙(static rules)_ 들로 `Validator` 인스턴스를 생성합니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

예를 들어, 게임 수집가용 웹 애플리케이션에서 회원가입 시, 100개 이상의 게임을 소유한 사용자는 그 이유를 설명하도록 요구하고 싶다고 가정합시다. 운영 중인 중고 게임 가게 때문일 수도 있고, 단순한 취미일 수도 있습니다. 이러한 조건부 요구사항은 `Validator` 인스턴스의 `sometimes` 메서드를 활용하여 손쉽게 구현할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인자는 조건부로 검증할 필드명이며, 두 번째 인자는 추가할 규칙 목록입니다. 세 번째 인자로 넘긴 클로저가 `true`를 반환하면 해당 규칙이 적용됩니다. 이 메서드를 사용하면 복잡한 조건부 검증도 부담없이 작성할 수 있습니다. 여러 필드를 동시에 조건부로 검증하고 싶다면 배열로 여러 필드명을 넘길 수 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent` 인스턴스이며, 검증 대상의 입력값과 파일에 접근할 때 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 검증

때로는 중첩 배열에서, 그 인덱스를 알지 못하는 상태에서 또 다른 필드 값을 기반으로 특정 필드를 검증해야 할 수도 있습니다. 이런 상황에서는, 클로저의 두 번째 인자로 현재 배열 아이템이 전달되게 할 수 있습니다.

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

`$input`과 함께 넘어오는 `$item`은, 배열일 경우 `Illuminate\Support\Fluent`의 인스턴스고, 배열이 아닐 때는 문자열입니다.

<a name="validating-arrays"></a>
## 배열 검증

[배열 관련 검증 규칙 문서](#rule-array)에서 설명한 것처럼, `array` 규칙은 허용된 배열 키의 목록을 받습니다. 배열에 명시되지 않은 추가 키가 포함돼 있으면 검증이 실패합니다.

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

일반적으로 배열 내에 허용할 키들을 항상 명시하는 것이 좋습니다. 그렇지 않으면, validator의 `validate` 및 `validated` 메서드는 전체 배열과 모든 키(중첩된 배열에도 유효성 검증이 적용되지 않은 키들까지)를 반환할 수 있습니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 검증

중첩 배열 형태로 폼 데이터를 입력 받는 경우, 복잡하게 느껴질 수 있지만, "닷(.) 표기법"을 사용하면 배열 내부의 속성들을 검증하는 것이 간편해집니다. 예를 들어, HTTP 요청에 `photos[profile]` 필드가 있다면 아래와 같이 검증할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소에 대해서도 검증할 수 있습니다. 예를 들어, 배열 형태로 받은 각 이메일이 유일해야 한다면:

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

또한, [언어 파일에서 사용자 지정 검증 메시지 지정](#custom-messages-for-specific-attributes) 시, `*` 문자를 활용해 배열 필드에 동일한 메시지를 쉽게 쓸 수 있습니다.

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근하기

어떤 경우에는, 특정 중첩 배열 항목에 대해 검증 규칙을 부여하면서 해당 값에 접근해야 할 수 있습니다. `Rule::forEach` 메서드를 통해 이를 쉽게 구현할 수 있습니다. 이 메서드는, 검증 대상 배열의 각 요소에 대해 클로저를 실행하며, 각 요소의 값과 전체 속성 이름을 전달합니다. 이 클로저는 해당 배열 요소에 적용할 규칙 목록을 반환해야 합니다.

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
### 에러 메시지에서 인덱스 및 위치 표시하기

배열 검증 시, 검증에 실패한 항목의 인덱스나 순번(위치)을 에러 메시지에 표시하고 싶을 때가 있습니다. 이때 [커스텀 검증 메시지](#manual-customizing-the-error-messages)에서 `:index`(0부터 시작), `:position`(1부터 시작) 플레이스홀더를 활용할 수 있습니다.

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

위 예시의 경우, 검증이 실패하면 사용자에게 _"Please describe photo #2."_라는 메시지가 나타납니다.

필요하다면 더 깊은 중첩의 인덱스 및 위치도 `second-index`, `second-position`, `third-index`, `third-position` 등으로 참조할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 검증

라라벨에서는 업로드된 파일의 형식이나 크기 등 다양한 조건을 검증할 수 있는 여러 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 개별 규칙을 조합해 파일 검증을 할 수도 있지만, 라라벨이 제공하는 유창한 파일 검증 규칙 빌더(File Rule builder)를 사용할 수도 있습니다.

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
#### 파일 형식 검증

`types` 메서드에서 확장자만 지정하면 되지만, 실제로는 확장자가 아니라 파일의 내용을 읽어서 MIME 타입을 기반으로 검증합니다. 지원하는 모든 MIME 타입과 확장자 목록은 아래 링크에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 검증

더 편리하게, 최소/최대 파일 크기를 문자열로 지정할 수 있으며 뒤에 단위를 붙일 수 있습니다. `kb`, `mb`, `gb`, `tb` 단위가 지원됩니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 검증

애플리케이션에서 이미지 업로드를 허용하고 있다면, `File` 규칙의 `image` 생성 메서드를 사용해 jpg, jpeg, png, bmp, gif, webp 형식의 이미지만 받도록 할 수 있습니다.

또한, `dimensions` 규칙을 활용해 이미지의 폭/높이 등 크기를 제한할 수 있습니다.

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
> 이미지 크기(폭/높이) 검증에 관한 더 자세한 내용은 [dimension 규칙 문서](#rule-dimensions)를 참고하세요.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약성 우려로 인해 SVG 파일은 허용하지 않습니다. SVG 파일도 허용하려면 `allowSvg: true`를 `image` 규칙에 전달할 수 있습니다: `File::image(allowSvg: true)`

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(폭/높이) 검증

이미지의 폭/높이도 검증할 수 있습니다. 예를 들어 최소 1000픽셀 폭, 500픽셀 높이의 이미지만 허용하려면 `dimensions` 규칙을 사용하면 됩니다.

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
> 이미지 크기(폭/높이) 검증에 관한 더 자세한 내용은 [dimension 규칙 문서](#rule-dimensions)를 참고하세요.

<a name="validating-passwords"></a>
## 비밀번호 검증

보안 수준을 충분히 확보하기 위해, 라라벨의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체는 영문, 숫자, 기호, 대소문자 혼합 등 보다 복잡한 비밀번호 요구 정책을 쉽게 커스터마이징할 수 있게 해줍니다.

```php
// 최소 8자 요구...
Password::min(8)

// 영문 글자 최소 1개 포함 요구...
Password::min(8)->letters()

// 대소문자 혼합 요구...
Password::min(8)->mixedCase()

// 숫자 최소 1개 포함 요구...
Password::min(8)->numbers()

// 기호 최소 1개 포함 요구...
Password::min(8)->symbols()
```

또한, `uncompromised` 메서드를 사용해 비밀번호가 유출된 적이 있는지(공개된 비밀번호 유출 데이터에 포함돼 있는지)도 즉시 검증할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로, `Password` 규칙 객체는 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스와 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 모델을 활용하여, 사용자의 프라이버시와 보안을 해치지 않으면서 비밀번호 유출 여부를 확인합니다.

기본적으로 비밀번호가 데이터 유출에 한 번이라도 포함되면 불합격 처리됩니다. 이 임계값은 `uncompromised` 메서드의 첫 번째 인자 값으로 조정할 수 있습니다.

```php
// 같은 데이터 유출에 3번 미만으로 나타난 경우만 허용...
Password::min(8)->uncompromised(3);
```

물론, 위의 예시 메서드들은 모두 체이닝하여 사용할 수 있습니다.

```php
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의

애플리케이션의 한 곳에서 기본 비밀번호 규칙을 정의해두고, 반복적으로 재사용하는 것이 편리할 수 있습니다. 이를 위해서는 `Password::defaults` 메서드에 클로저를 전달하여 기본 비밀번호 규칙 구성을 반환하도록 하면 됩니다. 일반적으로 이 코드는 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다.

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

그 후 비밀번호 검증 시 별도의 인수 없이 `defaults` 메서드를 호출해 기본 규칙을 바로 적용할 수 있습니다.

```php
'password' => ['required', Password::defaults()],
```

필요에 따라, 기본 비밀번호 규칙에 추가 검증을 붙이고 싶다면 `rules` 메서드를 활용하십시오.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 커스텀 검증 규칙

<a name="using-rule-objects"></a>
### 규칙 객체(Rule Objects) 사용

라라벨에서는 다양한 유용한 검증 규칙을 제공하지만, 때로는 직접 검증 규칙을 정의해서 사용하고 싶을 수 있습니다. 이 중 하나의 방법은 규칙 객체(Rule Object)를 사용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 쓸 수 있습니다. 이 명령어를 사용해 문자열이 대문자인지 검사하는 규칙을 만들어 보겠습니다. 새 규칙은 `app/Rules` 디렉터리에 생성되며, 해당 디렉터리가 없다면 Artisan이 자동으로 생성합니다.

```shell
php artisan make:rule Uppercase
```

규칙 객체가 생성되었다면, 이제 동작을 정의할 차례입니다. 규칙 객체는 `validate`라는 단 하나의 메서드를 가지고 있습니다. 이 메서드는 속성명, 값, 그리고 검증 실패 시 호출할 콜백(검증 에러 메시지 전달용)을 받게 됩니다.

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

규칙을 정의했다면, 이후 Validator에 해당 규칙 객체 인스턴스를 검증 규칙 배열에 추가해 사용할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 검증 메시지 번역하기

`$fail` 클로저에 단순 문자열 메시지를 전달하는 대신, [번역 문자열 키](/docs/12.x/localization)를 전달해서 라라벨이 오류 메시지를 번역하도록 할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면 `translate` 메서드의 첫 번째 인자로 플레이스홀더 대체값, 두 번째 인자로 번역할 언어 코드를 전달할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

커스텀 검증 규칙 클래스에서 검증 중인 모든 데이터를 접근해야 할 때는, 클래스에서 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하면 됩니다. 이 인터페이스를 구현하면, 라라벨은 검증이 진행되기 전에 모든 데이터가 담긴 배열을 `setData` 메서드로 자동 전달합니다.

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

또는, 해당 검증을 수행하는 validator 인스턴스 자체에 접근이 필요하다면, `ValidatorAwareRule` 인터페이스 구현이 가능합니다.

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

### 클로저 사용하기

애플리케이션에서 한 번만 커스텀 규칙이 필요하다면, 규칙 객체 대신 클로저를 사용할 수도 있습니다. 클로저는 속성(attribute)의 이름, 속성 값, 그리고 유효성 검증에 실패할 경우 호출해야 하는 `$fail` 콜백을 인자로 받습니다.

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

기본적으로, 검증하려는 속성이 존재하지 않거나 빈 문자열일 경우에는 커스텀 규칙을 포함한 일반적인 유효성 검사 규칙이 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에 대해서는 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

커스텀 규칙이 속성 값이 비어 있을 때도 실행되길 원한다면, 해당 규칙이 해당 속성이 필수임을 '암시'해야 합니다. 새로운 암묵적 규칙 객체를 빠르게 생성하려면 `make:rule` Artisan 명령어에 `--implicit` 옵션을 추가하세요.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적" 규칙은 속성이 필수임을 _암시_ 할 뿐입니다. 실제로 값이 없거나 속성이 누락된 경우 해당 속성을 무효 처리할지는 여러분이 직접 구현해야 합니다.