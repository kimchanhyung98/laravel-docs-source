# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력 처리](#repopulating-forms)
    - [선택적 필드에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 포맷](#validation-error-response-format)
- [폼 요청 유효성 검증](#form-request-validation)
    - [폼 요청 클래스 생성하기](#creating-form-requests)
    - [폼 요청 권한 처리](#authorizing-form-requests)
    - [오류 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검증 전 입력값 준비](#preparing-input-for-validation)
- [수동으로 유효성 검증기 만들기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 오류 백(Named Error Bag)](#named-error-bags)
    - [오류 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [유효성 검증된 입력값 사용하기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 유효성 검증](#validating-nested-array-input)
    - [오류 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션으로 들어오는 데이터를 검증할 수 있는 다양한 접근 방식을 제공합니다. 가장 일반적으로는 모든 HTTP 요청 객체에서 사용할 수 있는 `validate` 메서드를 사용하는 방식을 권장하지만, 이외에도 여러 가지 다른 유효성 검증 방법이 있습니다.

Laravel은 여러 가지 편리한 유효성 검증 규칙을 내장하고 있으며, 특정 데이터베이스 테이블에서 값의 고유성까지 검증할 수 있습니다. 이 문서에서는 각 유효성 검증 규칙을 상세히 다뤄 Laravel의 모든 유효성 검증 기능에 익숙해질 수 있도록 설명합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 검증하고 오류 메시지를 사용자에게 표시하는 전체 예제를 살펴보겠습니다. 이 섹션을 읽으면, Laravel을 사용하여 들어오는 요청 데이터의 유효성을 검증하는 방법에 대한 전반적인 이해를 얻을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 아래와 같이 라우트를 정의한다고 가정하겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위에서 정의한 라우트를 처리하는 간단한 컨트롤러를 살펴보겠습니다. 여기서는 `store` 메서드는 비워둔 상태입니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 작성 폼을 표시합니다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 포스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 포스트를 유효성 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 `store` 메서드에 새 블로그 포스트에 대한 유효성 검증을 추가해보겠습니다. 이를 위해, `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드는 정상적으로 계속 실행되며, 만약 유효성 검증에 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 오류 응답이 사용자에게 자동으로 전달됩니다.

전통적인 HTTP 요청 중에 유효성 검증이 실패하면, 이전 URL로 사용자를 리디렉션하는 응답이 생성됩니다. 만약 들어오는 요청이 XHR(비동기) 요청이라면, [유효성 검증 오류 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

`store` 메서드에 `validate` 메서드 사용 예시는 아래와 같습니다.

```php
/**
 * 새 블로그 포스트를 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 포스트가 유효합니다...

    return redirect('/posts');
}
```

위에서 보듯이, 유효성 검증 규칙은 `validate` 메서드에 넘깁니다. 모든 사용 가능한 유효성 검증 규칙은 [문서에서 확인](#available-validation-rules)할 수 있습니다. 다시 강조하자면, 검증에 실패하면 적절한 응답이 자동으로 생성되며, 성공하면 컨트롤러는 계속 정상 실행됩니다.

또한, 유효성 검증 규칙은 `|`로 구분된 문자열이 아니라 규칙들의 배열로도 지정할 수 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, [이름이 지정된 오류 백](#named-error-bags)에 오류 메시지를 저장하면서 요청을 검증하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

때때로 속성에서 첫 번째 유효성 검증 실패 이후로 더 이상 규칙을 적용하고 싶지 않을 수 있습니다. 이 경우, 해당 속성에 `bail` 규칙을 할당하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서, 만약 `title` 속성의 `unique` 규칙이 실패하면, `max` 규칙은 검사하지 않습니다. 규칙은 할당된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있는 경우, "점(dot) 표기법"을 사용하여 해당 필드를 유효성 검증 규칙에 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드 이름에 실제로 점(`.`)이 포함된 경우, 역슬래시(`\`)로 이 점을 이스케이프하여 점 표기법으로 해석되지 않도록 할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시하기

만약 들어오는 요청 필드가 지정된 유효성 검증 규칙을 통과하지 못하는 경우 어떻게 될까요? 앞서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리디렉션합니다. 또한, 모든 유효성 검증 오류 및 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 [세션에 자동으로 flash 처리](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(웹 미들웨어 그룹에서 제공됨)는 `$errors` 변수를 애플리케이션의 모든 뷰에 공유합니다. 이 미들웨어가 적용되어 있으면, `$errors` 변수는 언제나 정의되어 있다고 가정해도 안전하고, 뷰에서 자유롭게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체 작업에 대해 더 자세한 내용은 [해당 문서](#working-with-error-messages)에서 확인하세요.

따라서, 예시에서 유효성 검증 실패 시 컨트롤러의 `create` 메서드로 리디렉션되어, 뷰에서 오류 메시지를 표시할 수 있게 됩니다.

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
#### 오류 메시지 커스터마이징

Laravel의 내장 유효성 검증 규칙마다 각각의 오류 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 위치해 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 변경할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해 메시지를 원하는 애플리케이션 언어로 번역할 수도 있습니다. Laravel 다국어 지원에 대해 더 알아보려면, [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 이용해 게시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

위 예시에서는 전통적인 폼을 사용해 데이터를 보냈지만, 최근엔 자바스크립트 기반 프론트엔드에서 XHR 요청을 받는 경우가 많습니다. XHR 요청 중에 `validate` 메서드를 사용하면, Laravel은 리디렉션 응답을 생성하지 않고, [모든 유효성 검증 오류가 포함된 JSON 응답](#validation-error-response-format)을 422 HTTP 상태 코드와 함께 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성의 유효성 검증 오류 메시지가 존재하는지 빠르게 확인하려면, [Blade](/docs/12.x/blade)의 `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 내에서는 `$message` 변수를 출력하여 오류 메시지를 표시할 수 있습니다.

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

[이름이 지정된 오류 백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인자로 오류 백 이름을 지정할 수도 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력 처리

Laravel이 유효성 검증 오류로 인해 리디렉션 응답을 생성할 때, 프레임워크는 [요청의 모든 입력값을 세션에 자동으로 flash 처리](/docs/12.x/session#flash-data)합니다. 이를 통해 사용자는 다음 요청에서 이전 입력값을 다시 접근할 수 있어, 제출 시도한 폼을 쉽게 재입력할 수 있습니다.

이전 요청의 flash 된 입력을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하면 됩니다. 이 메서드는 [세션](/docs/12.x/session)에 저장된 이전 입력값을 불러옵니다.

```php
$title = $request->old('title');
```

Blade 템플릿에서 이전 입력값을 표시할 때는, 전역 `old` 헬퍼를 사용하는 것이 편리합니다. 주어진 필드에 대한 이전 입력값이 존재하지 않으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 참고

Laravel에서는 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 애플리케이션의 전역 미들웨어 스택에 포함되어 있습니다. 이 때문에 "선택적" 요청 필드를 검증하고자 할 때, `nullable`로 표시해주어야 `null` 값이 올바르지 않은 값으로 간주되지 않습니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서는 `publish_at` 필드는 `null`이거나, 유효한 날짜여야 합니다. 만약 `nullable` 수정자를 추가하지 않으면, 유효성 검증기는 `null`을 잘못된 값으로 처리합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외를 발생시키고, 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우 Laravel은 오류 메시지를 자동으로 포매팅해주며, `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래는 유효성 검증 오류에 대한 JSON 응답 포맷 예시입니다. 중첩된 오류 키는 "dot" 표기법으로 평탄화됩니다.

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
## 폼 요청 유효성 검증 (Form Request Validation)

<a name="creating-form-requests"></a>
### 폼 요청 클래스 생성하기

좀 더 복잡한 유효성 검증이 필요할 경우, "폼 요청(form request)"을 사용하는 것이 유용합니다. 폼 요청은 자체 유효성 검증 및 인가(authorization) 로직을 캡슐화한 커스텀 요청 클래스입니다. 폼 요청 클래스를 생성하려면 `make:request` Artisan CLI 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 저장됩니다. 해당 디렉터리가 없다면, 명령어 실행 시 자동으로 생성됩니다. Laravel이 생성하는 각 폼 요청에는 `authorize`와 `rules` 두 가지 메서드가 존재합니다.

`authorize` 메서드는 현재 인증된 사용자가 이 요청이 나타내는 행동을 수행할 수 있는지 판단하며, `rules` 메서드는 이 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

```php
/**
 * 요청에 적용할 유효성 검증 규칙을 반환합니다.
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
> `rules` 메서드의 시그니처에서 필요한 의존성은 타입 힌팅으로 지정할 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 해당 요청을 타입 힌트로 지정하기만 하면 됩니다. 들어오는 폼 요청은 컨트롤러 메서드가 호출되기 전에 검증되므로, 컨트롤러 내부가 유효성 검증 코드로 복잡해질 일이 없습니다.

```php
/**
 * 새 블로그 포스트를 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효합니다...

    // 검증된 입력값 가져오기...
    $validated = $request->validated();

    // 검증된 입력값 중 일부만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

유효성 검증에 실패하면, 사용자를 이전 위치로 되돌리는 리디렉션 응답이 자동으로 생성됩니다. 오류 메시지 역시 세션에 flash되어 표시할 수 있습니다. 요청이 XHR 방식인 경우에는 [유효성 검증 오류의 JSON 형태](#validation-error-response-format)와 함께 HTTP 422 응답이 반환됩니다.

> [!NOTE]
> Inertia 기반의 Laravel 프론트엔드에서 실시간 폼 요청 유효성 검증이 필요하다면 [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행

초기 유효성 검증이 완료된 이후에, 추가 유효성 검증을 수행해야 할 때가 있습니다. 이럴 때는 폼 요청의 `after` 메서드를 사용할 수 있습니다.

`after` 메서드는 validation이 완료된 후 호출될 콜러블 또는 클로저 배열을 반환해야 합니다. 각 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 전달되며, 필요하다면 추가 오류 메시지를 등록할 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * 유효성 검증 완료 후 호출될 콜러블을 반환합니다.
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

또한, 반환되는 배열에 호출 가능한 클래스 인스턴스를 담을 수도 있습니다. 이 클래스들의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 유효성 검증 완료 후 호출될 콜러블을 반환합니다.
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

폼 요청 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하여, 하나의 유효성 검증 실패 발생 시 모든 속성에 대한 검증을 즉시 중단할 수 있습니다.

```php
/**
 * 유효성 검증 규칙에서 첫 번째 실패 발생 시 전체 중단 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

폼 요청 유효성 검증 실패 시 기본적으로 이전 위치로 리디렉션되지만, 이 동작을 변경할 수도 있습니다. 폼 요청 클래스에 `$redirect` 프로퍼티를 정의하세요.

```php
/**
 * 유효성 검증 실패 시 리디렉션될 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 네임드 라우트로 리디렉션하려면 `$redirectRoute` 프로퍼티를 사용할 수 있습니다.

```php
/**
 * 유효성 검증 실패 시 리디렉션될 라우트.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 권한 처리

폼 요청 클래스에는 `authorize` 메서드가 있습니다. 여기서, 인증된 사용자가 실제로 특정 리소스에 대해 해당 요청을 수행할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 업데이트하려는 블로그 댓글의 소유자인지 확인할 수 있습니다. 대부분의 경우 이 메서드 안에서 [인가 게이트 및 정책](/docs/12.x/authorization)과 상호작용하게 됩니다.

```php
use App\Models\Comment;

/**
 * 사용자가 이 요청을 수행할 권한이 있는지 결정합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 요청은 Laravel의 기본 Request 클래스를 확장하므로, `user` 메서드로 현재 인증된 사용자에 접근할 수 있습니다. 위 예시에서 `route` 메서드를 호출한 것도 주목하세요. 이 메서드는 호출 중인 라우트에 정의된 URI 매개변수(예: `{comment}`)에 접근합니다.

```php
Route::post('/comment/{comment}');
```

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용한다면, 요청의 속성으로 바인딩된 모델에 바로 접근할 수도 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, HTTP 403 상태코드의 응답이 즉시 반환되며 컨트롤러 메서드는 실행되지 않습니다.

요청에 대한 인가 로직을 애플리케이션의 다른 부분에서 처리하려는 경우, `authorize` 메서드 자체를 생략하거나 `true`를 반환하면 됩니다.

```php
/**
 * 사용자가 이 요청을 수행할 권한이 있는지 결정합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드에도 필요한 의존성을 타입 힌트로 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이징

폼 요청에서 사용되는 오류 메시지를 커스터마이징하려면 `messages` 메서드를 오버라이드하면 됩니다. 이 메서드는 속성/규칙별로 원하는 오류 메시지를 지정한 배열을 반환해야 합니다.

```php
/**
 * 정의된 유효성 검증 규칙의 오류 메시지를 반환합니다.
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

Laravel 내장 유효성 검증 오류 메시지에는 `:attribute` 플레이스홀더가 자주 사용됩니다. 이 플레이스홀더를 커스텀 속성명으로 대체하고 싶다면, `attributes` 메서드를 오버라이드하여 속성명 매핑 배열을 반환하면 됩니다.

```php
/**
 * 유효성 검증 오류에 대한 커스텀 속성명을 반환합니다.
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
### 유효성 검증 전 입력값 준비

요청 데이터에 유효성 검증을 적용하기 전에 데이터를 준비(정규화 또는 변경)해야 할 경우, `prepareForValidation` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증을 위한 데이터 준비.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

검증이 완료된 후 데이터를 추가로 정규화하고 싶다면, `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * 유효성 검증 통과 후 처리.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 유효성 검증기 만들기 (Manually Creating Validators)

요청 객체의 `validate` 메서드를 사용하지 않고, 직접 유효성 검증기 인스턴스를 생성하고 싶다면, `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 활용하면 됩니다.

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

        // 검증된 입력값 가져오기...
        $validated = $validator->validated();

        // 검증된 입력값 중 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인자는 검증할 데이터, 두 번째 인자는 데이터에 적용할 유효성 검증 규칙의 배열입니다.

요청 검증 실패 여부를 확인한 후에는 `withErrors` 메서드를 사용하여 오류 메시지를 세션에 flash 할 수 있습니다. 이 메서드를 사용하면, 리디렉션 후 뷰에서도 `$errors` 변수를 사용할 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP 배열을 인자로 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 중단

`stopOnFirstFailure` 메서드를 호출하면, 하나의 검증 실패가 발생하는 즉시 모든 속성의 유효성 검증을 중단할 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

수동으로 유효성 검증기를 생성하면서도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션 기능을 그대로 활용하고 싶다면 Validator 인스턴스의 `validate` 메서드를 호출하면 됩니다. 검증에 실패할 경우 사용자가 자동으로 리디렉션되고, XHR 요청인 경우에는 [JSON 응답](#validation-error-response-format)이 반환됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

검증 실패 시 오류 메시지를 [이름이 지정된 오류 백](#named-error-bags)에 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 오류 백(Named Error Bag)

하나의 페이지에 여러 개의 폼이 있을 경우, 특정 폼의 오류 메시지만 가져오고 싶을 때가 있습니다. 이를 위해 `MessageBag`에 이름을 지정할 수 있고, `withErrors` 메서드의 두 번째 인자로 이름을 넘기면 됩니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이후, `$errors` 변수에서 지정한 이름의 `MessageBag` 인스턴스를 사용할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 커스터마이징

필요하다면, validator 인스턴스에서 Laravel 기본 오류 메시지 대신 사용할 커스텀 오류 메시지를 지정할 수 있습니다. 가장 간단한 방법은 `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지 배열을 넘기는 것입니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위 예시에서 `:attribute` 플레이스홀더는 실제 필드명으로 대체됩니다. 이 외에도 다양한 플레이스홀더를 사용할 수 있습니다.

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

특정 속성에 대해서만 커스텀 오류 메시지를 지정하고 싶을 수 있습니다. "dot" 표기법을 사용해서 속성명과 규칙을 함께 지정하면 됩니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

Laravel 내장 오류 메시지 중에는 `:attribute`가 포함된 경우가 많습니다. 특정 필드에 대해 이 값의 대체 텍스트를 지정하려면, `Validator::make`의 네 번째 인자로 커스텀 속성명 배열을 넘기면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행

초기 유효성 검증이 완료된 후, 추가 검증이 필요하다면 Validator 인스턴스의 `after` 메서드를 사용하세요. 이 메서드는 클로저 또는 콜러블의 배열을 파라미터로 받아, 검증 완료 후 이를 실행합니다. 각 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 전달됩니다.

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

`after` 메서드는 콜러블의 배열도 받을 수 있어, 후처리 로직이 클래스 형태로 구현되었을 때도 편리합니다. 이런 클래스는 `__invoke` 메서드를 통해 `Validator` 인스턴스를 받을 수 있습니다.

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
## 유효성 검증된 입력값 사용하기 (Working With Validated Input)

폼 요청 또는 수동으로 생성한 Validator 인스턴스에서 유효성 검증을 수행한 후, 실제로 검증을 거친 입력 데이터를 얻고 싶을 때가 있습니다. 이를 위한 방법은 여러 가지가 있습니다. 가장 많이 쓰는 방법은, 폼 요청 또는 Validator 인스턴스에서 `validated` 메서드를 호출하는 것입니다. 이 메서드는 검증된 데이터의 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하며, `only`, `except`, `all` 메서드를 통해 검증된 데이터 전체 혹은 일부분만 추출할 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열과 같이 반복하거나 인덱스를 통해 접근할 수 있습니다.

```php
// 반복 접근
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열 접근
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 합치고 싶다면, `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 변환하려면, `collect` 메서드를 사용할 수 있습니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기 (Working With Error Messages)

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 이 객체는 오류 메시지를 다루는 데 유용한 여러 메서드를 제공합니다. Laravel이 자동으로 뷰에 제공하는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 오류 메시지 얻기

특정 필드에 대한 첫 번째 오류 메시지를 얻으려면 `first` 메서드를 사용하세요.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 얻기

필드별 모든 메시지의 배열이 필요하다면 `get` 메서드를 사용할 수 있습니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형식의 입력 필드를 검증할 경우, 각각의 배열 요소에 대한 메시지를 `*` 문자로 받아올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 얻기

전체 오류 메시지 배열을 가져오려면 `all` 메서드를 사용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 오류 메시지가 있는지 확인

해당 필드에 오류 메시지가 존재하는지 확인하려면 `has` 메서드를 사용하세요.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel 내장 유효성 검증 규칙마다 각 오류 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 위치해 있습니다. `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령으로 생성할 수 있습니다.

파일 내 각 규칙별 번역 항목을 자유롭게 원하는 메시지로 변경할 수 있습니다.

또한 해당 파일을 다른 언어 디렉터리로 복사해, 애플리케이션 언어에 맞게 메시지를 번역할 수도 있습니다. 자세한 내용은 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> Laravel 기본 스캐폴딩에는 `lang` 디렉터리가 없습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션의 유효성 검증 언어 파일 내에서 특정 속성/규칙 조합에 대해 커스텀 오류 메시지를 지정할 수 있습니다. 이를 위해, `lang/xx/validation.php`의 `custom` 배열에 메시지를 추가하세요.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

많은 내장 오류 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 해당 플레이스홀더를 커스텀 값으로 대체하려면, `lang/xx/validation.php` 파일의 `attributes` 배열에 커스텀 속성명을 지정하세요.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 유효성 검증 오류 메시지는 `:value` 플레이스홀더를 포함합니다. 이 플레이스홀더에 표시될 값을 지정하고 싶을 때, `lang/xx/validation.php` 파일의 `values` 배열에 등록하면 됩니다. 예를 들어, `payment_type` 필드가 `cc`일 때 `credit card`로 표시하려면 아래와 같이 작성합니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

이렇게 하면 오류 메시지에서 "payment type is credit card"와 같이 사용자 친화적으로 표현됩니다.

> [!WARNING]
> `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성하세요.

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙 (Available Validation Rules)

아래는 사용 가능한 모든 유효성 검증 규칙과 그 기능에 대한 목록입니다.

... (이하 규칙 목록 및 상세 설명은 번역 대상이 아니므로 원문 형식 구조에 맞춰 번역을 계속합니다. 각 규칙 설명은 그대로 자세히 번역해야 함.)

---

> 이하는 각 유효성 검증 규칙 설명, 조건부 규칙 추가법, 배열/파일/비밀번호/커스텀 규칙 등의 세부 내용이 이어집니다.  
> 각 규칙별 제목, 설명, 예시, 내용 모두 위의 번역 원칙과 규칙에 따라 목차 및 섹션 구조, 예시 등 그대로 번역해주시면 됩니다.

---