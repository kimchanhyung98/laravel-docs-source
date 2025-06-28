# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 재입력값 자동 채우기](#repopulating-forms)
    - [선택 입력 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가하기](#authorizing-form-requests)
    - [에러 메시지 커스터마이즈하기](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉트](#automatic-redirection)
    - [이름이 지정된 에러 배그 사용하기](#named-error-bags)
    - [에러 메시지 커스터마이즈하기](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [유효성 검증된 입력값 사용하기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력 유효성 검증](#validating-nested-array-input)
    - [에러 메시지의 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저(Closure) 사용하기](#using-closures)
    - [암묵적(implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션에 들어오는 데이터를 검증하는 데 여러 가지 다양한 방법을 제공합니다. 가장 일반적으로는, 모든 들어오는 HTTP 요청 객체에서 사용할 수 있는 `validate` 메서드를 사용합니다. 이 외에도 다양한 유효성 검증 방법들이 있으므로, 여기에서 모두 살펴보겠습니다.

라라벨에는 편리하게 사용할 수 있는 다양한 유효성 검증 규칙들이 내장되어 있습니다. 예를 들어, 특정 데이터베이스 테이블에서 값이 고유(유니크)한지 검증하는 기능도 제공합니다. 이 문서에서는 각각의 유효성 검증 규칙을 자세히 다루므로, 라라벨의 모든 유효성 검증 기능을 익힐 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작

라라벨의 강력한 유효성 검증 기능을 익히기 위해, 폼 데이터를 검증하고 에러 메시지를 사용자에게 보여주는 예제 전체 과정을 살펴보겠습니다. 이 개괄적인 예를 따라가면, 라라벨에서 들어오는 요청 데이터를 어떻게 검증하는지 전체적인 이해를 빠르게 얻을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같이 라우트를 정의했다고 가정해 보겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

여기서 `GET` 라우트는 사용자가 새로운 블로그 글을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새로운 블로그 글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이러한 라우트에서 들어오는 요청을 처리하는 컨트롤러를 예로 살펴보겠습니다. 이때, `store` 메서드는 일단 비워 둡니다.

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

이제 `store` 메서드에 새로운 블로그 글을 검증하는 로직을 추가하겠습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검증에 설정한 규칙을 통과하면 정상적으로 코드가 실행되고, 검증에 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하며 자동으로 적절한 에러 응답이 사용자에게 전송됩니다.

전통적인 HTTP 요청에서 유효성 검증이 실패하면, 이전 URL로 자동으로 리다이렉트 응답이 생성됩니다. 만약 들어오는 요청이 XHR 요청이라면, [유효성 검증 에러 메시지가 담긴 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작을 더 자세히 이해하기 위해, 다시 `store` 메서드로 돌아가 보겠습니다.

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

위 예시에서 보듯, 유효성 검증 규칙들은 `validate` 메서드에 전달됩니다. 걱정하지 않으셔도 됩니다. 사용 가능한 모든 유효성 검증 규칙들이 [문서화되어 있습니다](#available-validation-rules). 유효성 검증에 실패하면 자동으로 적절한 응답이 생성되고, 검증을 통과하면 컨트롤러의 뒷부분 코드가 그대로 실행됩니다.

또한, 검증 규칙들은 `|`로 구분한 문자열 대신 배열 형태로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

뿐만 아니라, [이름이 지정된 에러 배그](#named-error-bags) 안에 에러 메시지를 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

때때로 필드에 대해 한 번 실패한 뒤에는 추가 검증을 중단하고 싶을 수도 있습니다. 이럴 때는 해당 필드의 규칙에 `bail` 규칙을 추가하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이렇게 하면 `title` 속성의 `unique` 규칙에서 검증이 실패하는 경우, 그 뒤의 `max` 규칙은 검사하지 않습니다. 규칙들은 지정한 순서대로 평가됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고 사항

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 있다면, 유효성 검증 규칙을 지정할 때 "점(dot) 표기법"을 사용할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 점(.) 문자가 포함되어 있고, 이것이 "점 표기법"으로 해석되지 않게 하려면 백슬래시로 점을 이스케이프 처리하면 됩니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

그렇다면, 입력 필드가 지정한 유효성 검증 규칙을 통과하지 못했을 때 어떻게 될까요? 앞서 언급했듯이, 라라벨은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 그리고 모든 유효성 검증 에러와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 자동으로 [세션에 플래시](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(이 미들웨어는 `web` 미들웨어 그룹에 포함됨)가 모든 뷰에 `$errors` 변수를 공유합니다. 이 미들웨어가 적용되면, 모든 뷰에서 항상 `$errors` 변수를 안전하게 사용할 수 있다는 점을 전제로 작성하셔도 좋습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스가 되며, 이 객체를 다루는 방법에 대한 자세한 내용은 [해당 문서](#working-with-error-messages)에서 확인하실 수 있습니다.

따라서, 위 예시에서 유효성 검증이 실패하면 사용자는 컨트롤러의 `create` 메서드로 리다이렉트되어, 뷰에서 에러 메시지를 표시할 수 있습니다.

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

라라벨이 기본으로 제공하는 유효성 검증 규칙에는 각각 오류 메시지가 존재하며, 이 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 저장되어 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 이용해 직접 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 검증 규칙별로 번역 엔트리가 존재합니다. 이 파일의 메시지는 애플리케이션의 필요에 따라 자유롭게 수정하거나 변경할 수 있습니다.

또한, 해당 파일을 다른 언어 디렉터리로 복사해 각 언어에 맞게 메시지를 번역할 수도 있습니다. 라라벨의 현지화(localization) 기능에 대해 자세히 알고 싶다면, 완전한 [현지화 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 라라벨 애플리케이션 스캐폴딩에는 기본적으로 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어를 통해 언어 파일을 퍼블리시 해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

위 예제에서는 전통적인 폼을 이용해 데이터를 서버로 전송했습니다. 하지만 많은 애플리케이션이 JavaScript 기반 프론트엔드로부터 XHR 요청을 받기도 합니다. XHR 요청에서 `validate` 메서드를 사용할 경우, 라라벨은 리다이렉트 응답을 생성하지 않습니다. 대신 [모든 유효성 검증 에러가 담긴 JSON 응답](#validation-error-response-format)을 생성하고, 이 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

주어진 속성에 대한 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하려면, [Blade](/docs/12.x/blade)에서 `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 내부에서는 `$message` 변수를 출력해 에러 메시지를 표시할 수 있습니다.

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

[이름이 지정된 에러 배그](#named-error-bags)를 사용하는 경우, `@error` 디렉티브의 두 번째 인자로 에러 배그 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 재입력값 자동 채우기

라라벨은 유효성 검증 에러로 인해 리다이렉트 응답을 생성할 때, 프레임워크가 자동으로 [요청의 모든 입력값을 세션에 플래시](/docs/12.x/session#flash-data)합니다. 이 기능 덕분에 다음 요청에서 입력값에 다시 쉽게 접근하여, 사용자가 제출했던 폼을 편리하게 재구성할 수 있습니다.

이전 요청에서 플래시된 입력값을 얻으려면, `Illuminate\Http\Request`의 `old` 메서드를 호출하면 됩니다. `old` 메서드는 [세션](/docs/12.x/session)에서 플래시된 입력 데이터를 반환합니다.

```php
$title = $request->old('title');
```

라라벨은 전역적으로 사용할 수 있는 `old` 헬퍼 함수도 제공합니다. [Blade 템플릿](/docs/12.x/blade) 안에서 옛 입력값을 출력할 때 가장 간편하게 사용할 수 있습니다. 해당 필드에 기존 입력값이 없다면, `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 입력 필드에 대한 참고 사항

라라벨은 기본적으로 글로벌 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 포함하고 있습니다. 이러한 이유로, "선택(optional)" 입력 필드에 대해 검증 시 `null` 값을 유효하다고 처리하려면, 해당 필드를 `nullable`로 지정해야 합니다. 예를 들어,

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서는 `publish_at` 필드가 `null`이거나, 올바른 날짜 형식일 수 있도록 지정했습니다. 만약 규칙 정의에서 `nullable` 수정자를 빼면, 유효성 검증기는 `null` 값을 유효하지 않은 날짜로 처리합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 포맷

애플리케이션이 `Illuminate\Validation\ValidationException` 예외를 발생시키고, 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, 라라벨이 자동으로 에러 메시지를 형식화해 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래 예시에서는 유효성 검증 에러에 대한 JSON 응답 포맷을 확인할 수 있습니다. 참고로, 중첩된 에러 키는 "점(dot) 표기법"으로 평평하게(flatten) 표시됩니다.

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

보다 복잡한 유효성 검증이 필요한 경우 "폼 리퀘스트(Form Request)"를 생성할 수도 있습니다. 폼 리퀘스트는 고유의 유효성 검증 및 인가 로직을 캡슐화하는 커스텀 리퀘스트 클래스입니다. 폼 리퀘스트 클래스를 생성하려면 `make:request` Artisan CLI 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치하게 됩니다. 이 디렉터리가 존재하지 않으면 `make:request` 명령 실행 시 자동으로 생성됩니다. 라라벨이 생성해주는 각 폼 리퀘스트에는 `authorize`와 `rules` 두 개의 메서드가 있습니다.

예상하신 대로, `authorize` 메서드는 현재 인증된 사용자가 요청이 표현하는 동작을 실제로 수행할 수 있는지 판단하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드의 시그니처에 필요한 의존성을 타입힌트로 선언하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동 해결됩니다.

그렇다면, 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드의 파라미터에서 해당 폼 리퀘스트를 타입힌트로 지정하기만 하면 됩니다. 들어온 폼 리퀘스트가 컨트롤러 메서드 호출 이전에 검증되기 때문에, 컨트롤러 내에서 검증 로직을 일일이 작성할 필요가 없습니다.

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // 검증된 입력값 가져오기...
    $validated = $request->validated();

    // 검증된 입력값 중 일부만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 글 저장하기...

    return redirect('/posts');
}
```

유효성 검증에 실패할 경우, 사용자를 이전 위치로 돌려보내는 리다이렉트 응답이 자동으로 생성되며, 에러도 세션에 플래시되어 표시할 수 있습니다. 요청이 XHR 요청이었다면, HTTP 상태 코드 422와 함께 [유효성 검증 에러의 JSON 표현](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에서 실시간 폼 리퀘스트 유효성 검증이 필요하시다면 [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 폼 리퀘스트에서 추가 유효성 검증 수행하기

때로는 기본 검증이 끝난 뒤에 추가 검증이 필요할 수 있습니다. 이 경우 폼 리퀘스트의 `after` 메서드를 사용하세요.

`after` 메서드는 유효성 검증이 끝난 후 호출될 콜러블이나 클로저들을 배열로 반환해야 합니다. 지정한 콜러블들은 `Illuminate\Validation\Validator` 인스턴스를 인자로 받아, 필요한 경우 추가적으로 에러 메시지를 등록할 수도 있습니다.

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

위에서 설명한 것처럼, `after` 메서드가 반환하는 배열에는 호출 가능한 클래스를 포함할 수도 있습니다. 이 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 인자로 받습니다.

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

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가해, 단 하나라도 유효성 검증 실패가 발생하면 모든 필드에 대한 이후 검증을 즉시 중단하도록 할 수 있습니다.

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이즈하기

폼 리퀘스트 유효성 검증이 실패하면, 사용자를 이전 위치로 돌려보내는 리다이렉트 응답이 자동으로 생성됩니다. 이 동작은 자유롭게 커스터마이즈할 수 있습니다. 이를 위해, 폼 리퀘스트 클래스에 `$redirect` 프로퍼티를 정의하세요.

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 사용자를 이름이 지정된 라우트로 리다이렉트하고 싶다면 `$redirectRoute` 프로퍼티를 사용하세요.

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가하기

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드에서 인증된 사용자가 실제로 해당 리소스를 업데이트할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 블로그 댓글을 수정하려고 할 때 자신이 그 댓글의 소유자인지 검사할 수 있습니다. 이때 주로 [인가 게이트 및 정책](/docs/12.x/authorization)과 상호작용하게 됩니다.

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

모든 폼 리퀘스트는 기본적인 라라벨 리퀘스트 클래스를 확장하므로, 현재 인증된 사용자에 접근하려면 `user` 메서드를 사용할 수 있습니다. 그리고 위 코드에서 사용한 `route` 메서드를 주목하세요. 이 메서드는 호출되는 라우트에 정의된 URI 파라미터(예: 아래 예시의 `{comment}`)를 가져올 수 있게 해줍니다.

```php
Route::post('/comment/{comment}');
```

따라서, 애플리케이션이 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 이용한다면, 리퀘스트의 프로퍼티로 바인딩된 모델에 바로 접근해 코드를 더 간결하게 작성할 수도 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, HTTP 403 상태 코드의 응답이 자동으로 전송되고 컨트롤러 메서드는 실행되지 않습니다.

인가(authorization) 로직을 애플리케이션의 다른 곳에서 처리할 계획이라면, `authorize` 메서드를 아예 제거하거나 단순히 `true`를 반환해도 됩니다.

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
> `authorize` 메서드의 시그니처에 필요한 의존성을 타입힌트로 지정하면, 자동으로 라라벨 [서비스 컨테이너](/docs/12.x/container)에서 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈하기

폼 리퀘스트에서 사용하는 에러 메시지는 `messages` 메서드를 오버라이딩해 커스터마이즈할 수 있습니다. 이 메서드는 속성/규칙과 그에 해당하는 메시지 배열을 반환해야 합니다.

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
#### 유효성 검증 속성명 커스터마이즈하기

라라벨이 기본으로 제공하는 유효성 검증 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 이 플레이스홀더를 커스텀 속성명으로 치환하려면, `attributes` 메서드를 오버라이딩해서 커스텀 속성명을 지정할 수 있습니다. 이 메서드는 속성/이름 쌍의 배열을 반환해야 합니다.

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

유효성 검증 규칙을 적용하기 전에 요청에서 받은 데이터를 준비(정규화 또는 sanitize)해야 하는 경우, `prepareForValidation` 메서드를 사용할 수 있습니다.

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

마찬가지로, 유효성 검증이 끝난 뒤에 요청 데이터를 정규화해야 할 경우에는 `passedValidation` 메서드를 사용할 수 있습니다.

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

요청에서 `validate` 메서드를 사용하는 대신, `Validator` [파사드](/docs/12.x/facades)를 활용하여 직접 validator 인스턴스를 생성할 수 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 만들어 줍니다.

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

`make` 메서드의 첫 번째 인수는 유효성 검사를 진행할 데이터이며, 두 번째 인수는 해당 데이터에 적용할 유효성 검사 규칙들의 배열입니다.

요청의 유효성 검사가 실패했는지 확인한 후에는 `withErrors` 메서드를 사용하여 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 리디렉션 이후 뷰에서 `$errors` 변수에 자동으로 에러들이 공유되므로, 사용자에게 손쉽게 에러 메시지를 다시 보여줄 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP `배열(array)`을 인수로 받을 수 있습니다.

#### 최초 유효성 실패 시 즉시 중단하기

`stopOnFirstFailure` 메서드를 사용하면 첫 번째로 유효성 검사가 실패한 속성이 발견되는 즉시 이후 모든 속성에 대한 검사를 중단하도록 validator에 알릴 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

수동으로 validator 인스턴스를 만들면서도, HTTP 요청 객체의 `validate` 메서드가 제공하는 자동 리디렉션 기능을 활용하고 싶다면, 이미 생성한 validator 인스턴스에 대해 `validate` 메서드를 호출하면 됩니다. 이 경우 유효성 검사가 실패하면 사용자가 자동으로 리디렉션되고, XHR 요청의 경우에는 [JSON 형식 응답](#validation-error-response-format)이 반환됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

유효성 검사가 실패했을 때 에러 메시지를 [이름이 지정된 에러 백](#named-error-bags)에 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 있는 에러 백 사용하기

한 페이지에 여러 개의 폼이 있을 때, 각각의 폼에 대한 에러 메시지를 구분하기 위해 `MessageBag`에 이름을 지정할 수 있습니다. 이를 위해서는 `withErrors`의 두 번째 인수로 이름을 전달하면 됩니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

그러면 뷰에서 `$errors` 변수로 이름이 지정된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징하기

필요하다면 validator 인스턴스가 사용할 에러 메시지를 라라벨에서 제공하는 기본 메시지 대신, 커스텀 메시지로 지정할 수 있습니다. 커스텀 메시지는 여러 가지 방법으로 지정할 수 있습니다. 첫 번째로, `Validator::make` 메서드에 세 번째 인수로 커스텀 메시지 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예시에서 `:attribute` 플레이스홀더는 실제 유효성 검사를 수행하는 필드의 이름으로 치환됩니다. 유효성 검증 메시지에는 이 외에도 여러 플레이스홀더를 사용할 수 있습니다. 예를 들어:

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

특정 속성에 대해서만 에러 메시지를 커스텀해야 할 때가 있습니다. 이럴 때는 "점 표기법(dot notation)"을 사용하면 됩니다. 속성명 다음에 규칙명을 점으로 이어 붙여 지정하세요.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 속성별 커스텀 표시값 지정하기

라라벨의 기본 에러 메시지들은 `:attribute` 플레이스홀더를 포함하는 경우가 많으며, 이는 검증 대상 필드의 이름으로 치환됩니다. 특정 필드에 대해 이 플레이스홀더를 사용자 정의 값으로 바꾸고 싶다면, `Validator::make`의 네 번째 인수로 커스텀 속성 배열을 전달하면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 검증 수행하기

처음 수행한 유효성 검사 이후에 추가적인 검증이 필요할 수도 있습니다. 이런 경우 validator의 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 클로저 또는 콜러블(callable)들의 배열을 받을 수 있으며, 유효성 검사 이후에 호출됩니다. 이때 각각의 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 전달받아 추가적으로 에러 메시지를 등록할 수 있습니다.

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

앞서 언급한 것처럼, `after` 메서드는 콜러블의 배열도 인수로 받을 수 있습니다. 특히 "검증 후"에 필요한 로직을 인보커블 클래스(invokable class)로 분리해 두었다면 더욱 편리합니다. 인보커블 클래스의 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받을 수 있습니다.

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

폼 리퀘스트나 수동으로 생성한 validator 인스턴스를 통해 요청 데이터를 검증한 후, 실제로 검증이 통과된 데이터를 활용하고 싶을 수 있습니다. 이 작업도 여러 방법으로 수행할 수 있습니다. 먼저, 폼 리퀘스트 또는 validator 인스턴스에서 `validated` 메서드를 호출하면 유효성 검사가 완료된 데이터 배열을 반환받을 수 있습니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 리퀘스트나 validator 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체에서는 `only`, `except`, `all` 메서드를 사용하여 검증된 데이터 중 일부만 또는 전체를 배열로 가져올 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

추가로, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나 배열 접근 방식으로 사용할 수도 있습니다.

```php
// 검증된 데이터를 반복(iterate)할 수 있습니다.
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근할 수 있습니다.
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 새로운 필드를 추가하고 싶다면 `merge` 메서드를 사용하면 됩니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 가져오고 싶다면 `collect` 메서드를 사용할 수 있습니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 다양한 편의 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 반환합니다. 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

주어진 필드에 대해 첫 번째 에러 메시지를 가져오려면 `first` 메서드를 사용합니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 배열 가져오기

특정 필드에 대한 모든 에러 메시지를 배열로 가져오려면 `get` 메서드를 사용합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 필드에 대해 검증할 때는, `*` 문자를 사용하여 모든 배열 요소에 대한 메시지를 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드에 대한 모든 에러 메시지 배열 가져오기

모든 필드에 대한 에러 메시지를 배열로 가져오려면 `all` 메서드를 사용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드의 에러가 존재하는지 확인하기

`has` 메서드를 사용하면 특정 필드에 대한 에러 메시지가 존재하는지 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

라라벨의 기본 유효성 검사 규칙마다 애플리케이션의 `lang/en/validation.php` 파일에 에러 메시지가 미리 등록되어 있습니다. 애플리케이션에서 `lang` 디렉토리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 유효성 검사 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 변경하거나 수정할 수 있습니다.

또한, 이 파일을 복사해서 다른 언어 디렉터리에 넣으면 애플리케이션의 언어에 맞는 에러 메시지 번역도 가능해집니다. 라라벨의 로컬라이제이션에 대해 더 알고 싶다면 [로컬라이제이션 공식 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 배포해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션의 언어 파일에서, 특정 속성과 규칙 조합에 대한 에러 메시지를 커스터마이즈할 수 있습니다. 이를 위해서 `lang/xx/validation.php` 언어 파일의 `custom` 배열에 원하는 메시지를 추가하면 됩니다.

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

라라벨의 기본 에러 메시지 대부분에는 `:attribute` 플레이스홀더가 포함되어 있는데, 이는 검증하고 있는 필드 또는 속성의 이름으로 치환됩니다. 유효성 검사 메시지의 `:attribute` 부분을 커스텀 값으로 바꾸고 싶다면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 원하는 값을 지정할 수 있습니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 배포해야 합니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

라라벨 기본 유효성 검사 규칙의 에러 메시지 중 일부는 `:value` 플레이스홀더를 포함하고 있으며, 이는 요청 속성의 현재 값으로 치환됩니다. 하지만 경우에 따라서는 `:value`가 실제 값 대신 더 이해하기 쉬운 표현으로 바뀌길 원할 수 있습니다. 예를 들어, 아래와 같이 `payment_type` 값이 `cc`일 때 신용카드 번호가 필수라는 규칙이 있다고 가정합니다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 유효성 검사 규칙이 실패하면 아래와 같은 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

`cc` 대신 사용자 친화적인 값을 보여주고 싶다면, `lang/xx/validation.php` 언어 파일의 `values` 배열에 다음과 같이 지정할 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 배포해야 합니다.

이렇게 값을 정의하면 이후 유효성 검사 실패 시 아래와 같이 메시지가 표시됩니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검사 규칙

아래는 라라벨에서 제공하는 모든 유효성 검사 규칙과 그 기능의 목록입니다.

#### 불리언

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### 문자열

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

#### 숫자

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

#### 배열

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

#### 날짜

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

#### 파일

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

#### 데이터베이스

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

유효성 검사를 진행하는 필드는 반드시 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값을 가져야 합니다. 이 규칙은 이용 약관 동의와 같은 필드 검증에 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

다른 필드가 특정 값일 때, 현재 필드는 반드시 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 이 규칙 역시 "이용약관 동의" 등에서 조건부로 사용할 수 있습니다.

<a name="rule-active-url"></a>
#### active_url

유효성 검사를 진행하는 필드는 PHP의 `dns_get_record` 함수 기준으로 올바른 A 또는 AAAA 레코드가 있어야 합니다. 제공된 URL의 호스트명은 `parse_url` PHP 함수로 추출한 뒤 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

유효성 검사를 진행하는 필드는 지정된 날짜 이후의 값을 가져야 합니다. 지정한 날짜는 `strtotime` 함수로 변환되어 올바른 `DateTime` 인스턴스로 처리됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`에서 날짜 문자열을 평가하도록 직접 명시하지 않고, 단순히 다른 필드명을 넘겨 서로 비교하는 것도 가능합니다.

```php
'finish_date' => 'required|date|after:start_date'
```

추가로, 플루언트하게 규칙을 생성할 수 있게 도와주는 rule 빌더를 활용하면 날짜 기반 규칙을 더 읽기 쉽게 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

날짜가 오늘 이후여야 한다는 식의 조건은, `afterToday`, `todayOrAfter` 메서드를 사용하여 보다 직관적으로 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>

#### after\_or\_equal:_date_

유효성 검사가 적용되는 필드는 지정된 날짜와 같거나 그 이후의 값이어야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

날짜 기반 규칙은 보다 간편하게 fluent `date` 규칙 빌더로 작성할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검사 규칙은 검증 대상 필드가 주어진 여러 유효성 검사 규칙 세트 중 어느 하나라도 만족하면 통과되도록 지정할 수 있습니다. 예를 들어 아래 규칙은 `username` 필드가 이메일 주소이거나, 최소 6자 이상의 알파벳/숫자/대시로만 이루어진 문자열인지 확인합니다.

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

유효성 검사 대상 필드는 전체가 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 해당하는 유니코드 알파벳 문자여야 합니다.

이 유효성 검사 규칙을 ASCII 범위(`a-z`, `A-Z`)의 문자로 제한하고 싶다면 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

유효성 검사 대상 필드는 전체가 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 영문자/숫자, 그리고 ASCII 대시(`-`), 언더스코어(`_`) 문자여야 합니다.

이 규칙을 ASCII 범위(`a-z`, `A-Z`, `0-9`) 문자로만 제한하려면 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

유효성 검사 대상 필드는 전체가 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 영문자/숫자여야 합니다.

ASCII 범위(`a-z`, `A-Z`, `0-9`) 문자로만 제한하고 싶을 때는 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

유효성 검사 대상 필드는 PHP의 `array` 타입이어야 합니다.

추가 인수를 `array` 규칙에 넘기면, 입력 배열의 모든 키가 규칙에 전달된 값 목록에 포함되어야만 유효합니다. 아래 예시에서 입력 배열에 있는 `admin` 키는 허용된 목록에 없으므로 유효하지 않습니다.

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

일반적으로, 배열에 허용되는 키는 항상 명확하게 지정하는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

유효성 검사 대상 필드는 전부 7비트 ASCII 문자여야 합니다.

<a name="rule-bail"></a>
#### bail

한 필드에서 유효성 검사를 수행할 때 첫 번째 검증 실패 이후로 해당 필드의 나머지 규칙을 실행하지 않습니다.

`bail` 규칙은 특정 필드에만 적용되며, 하나의 규칙이 실패하면 그 필드의 후속 규칙들은 더 이상 검사하지 않습니다. 반면, `stopOnFirstFailure` 메서드는 한 번의 유효성 검사 실패가 발생하면 모든 속성에 대한 검증을 즉시 중단하도록 검사기를 동작시킵니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

유효성 검사 대상 필드는 지정된 날짜 이전의 값이어야 합니다. 날짜는 PHP `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 유효성 검사 중인 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

날짜 기반 규칙은 fluent `date` 규칙 빌더로도 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday` 및 `todayOrBefore` 메서드를 활용하면, 오늘 이전, 또는 오늘까지 포함해 이전 날짜여야 함을 더욱 직관적으로 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

유효성 검사 대상 필드는 지정된 날짜와 같거나 이전의 값이어야 합니다. 날짜는 PHP `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다. [after](#rule-after) 규칙과 마찬가지로, 유효성 검사 중인 다른 필드명을 `date` 값으로 사용할 수도 있습니다.

날짜 기반 규칙은 fluent `date` 규칙 빌더로도 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

유효성 검사 대상 필드는 주어진 _min_과 _max_ 범위(포함) 내 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

유효성 검사 대상 필드는 boolean으로 형변환될 수 있어야 합니다. 허용된 입력값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<a name="rule-confirmed"></a>
#### confirmed

유효성 검사 대상 필드는 `{field}_confirmation` 형식의 필드와 값이 일치해야 합니다. 예를 들어, 검증 대상이 `password` 필드라면 `password_confirmation` 필드가 입력값에 반드시 있어야 합니다.

맞춤 확인 필드명을 인수로 전달할 수도 있습니다. 예를 들어, `confirmed:repeat_username`처럼 지정하면, `repeat_username` 필드의 값이 현재 검증 대상 필드와 일치하는지 검사합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

유효성 검사 대상 필드는 배열이며, 지정한 모든 값(parameter)을 포함하고 있어야 합니다. 이 규칙은 배열 값을 `implode` 해야 하는 경우가 많으므로, `Rule::contains` 메서드를 사용해 더욱 간단하게 규칙을 작성할 수 있습니다.

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

유효성 검사 대상 필드는 현재 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 파라미터로 [인증 가드](/docs/12.x/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

유효성 검사 대상 필드는 PHP의 `strtotime` 함수 기준으로 유효하고 상대적이지 않은 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

유효성 검사 대상 필드는 주어진 날짜와 같아야 합니다. 날짜는 PHP `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

유효성 검사 대상 필드는 주어진 _formats_ 중 하나와 일치해야 합니다. 한 필드를 검증할 때는, `date` 또는 `date_format` 중 하나만 사용해야 합니다. 이 검증 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 포맷을 사용할 수 있습니다.

날짜 기반 규칙은 fluent `date` 규칙 빌더로도 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

유효성 검사 대상 필드는 숫자이며, 지정된 소수점 자릿수를 가져야 합니다.

```php
// 정확히 소수점 이하 두 자리가 있어야 합니다(예: 9.99)...
'price' => 'decimal:2'

// 소수점 이하 2~4자리 범위여야 합니다...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

유효성 검사 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

유효성 검사 대상 필드는, 해당하는 다른 필드가 특정 값과 같을 때 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

유효성 검사 대상 필드는 _field_와(과) 서로 다른 값이어야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수는 정확히 _value_ 자리여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

정수 검증 대상은 _min_과 _max_ 사이(포함)의 길이를 가져야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일이 이미지일 경우, 규칙의 파라미터로 지정한 크기 제약조건을 만족해야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약조건은 다음과 같습니다: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

_ratio_ 제약조건은 '가로/세로 비율'을 의미합니다. `3/2`와 같은 분수, 또는 `1.5`와 같은 실수로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

다수의 인수가 필요한 규칙이므로, `Rule::dimensions` 메서드를 활용해 더욱 간결하게 규칙을 작성할 수도 있습니다.

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

배열을 검증할 때, 해당 필드는 중복된 값이 없어야 합니다.

```php
'foo.*.id' => 'distinct'
```

`distinct`는 기본적으로 느슨한(타입을 엄격하게 비교하지 않는) 비교를 사용합니다. 엄격한 비교를 사용하려면 `strict` 파라미터를 규칙에 추가하세요.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 차이를 무시하고 중복을 검사하려면 `ignore_case` 파라미터를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

유효성 검사 대상 필드는 주어진 값 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

유효성 검사 대상 필드는 주어진 값 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

유효성 검사 대상 필드는 이메일 주소 형식이어야 합니다. 이 유효성 검사 규칙은 이메일 유효성 검사를 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로는 `RFCValidation` 검증기가 적용되지만, 다른 검증 스타일을 지정할 수도 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예시는 `RFCValidation`과 `DNSCheckValidation` 검증을 모두 적용합니다. 적용할 수 있는 모든 검증 스타일은 아래와 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - 이메일 주소를 [지원 RFC들](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) 기준으로 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원 RFC들](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) 기준으로 경고(예: 끝에 점이 있거나 연속된 점 등)가 있으면 실패 처리합니다.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 올바른 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 이메일 주소에 동형 이의어(homograph) 또는 속이는 유니코드 문자가 포함됐는지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일 주소가 유효한지 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수 기준으로, 일부 유니코드 문자를 허용하며 이메일이 유효한지 확인합니다.

</div>

더 편리하게, 이메일 주소의 유효성 검사는 fluent 규칙 빌더로도 작성할 수 있습니다.

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
> `dns` 및 `spoof` 검증기는 PHP의 `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

유효성 검사 대상 필드는 지정된 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 검증 대상 필드가 올바른 Enum(열거형) 값을 포함하고 있는지 확인하는 클래스 기반 규칙입니다. `Enum` 규칙은 생성자 인수로 Enum의 이름만 받습니다. 원시 값(기본값)을 검증할 때는 backed Enum을 `Enum` 규칙에 전달해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`, `except` 메서드를 사용하면 Enum의 특정 케이스만 유효한 값으로 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 활용하면, 상황에 따라 Enum 규칙을 동적으로 수정할 수 있습니다.

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

유효성 검사 대상 필드는 `validate` 및 `validated` 메서드 호출 결과 반환되는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

유효성 검사 대상 필드는 지정한 _anotherfield_의 값이 _value_와 같을 때, `validate`, `validated` 메서드의 반환 요청 데이터에서 제외됩니다.

복잡한 조건에 따라 필드를 제외해야 하는 경우에는 `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 boolean 값이나 클로저(익명 함수)를 인수로 받습니다. 클로저를 사용할 경우, 해당 필드를 제외해야 하면 `true`, 아니면 `false`를 반환하면 됩니다.

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

유효성 검사 대상 필드는 _anotherfield_의 값이 _value_일 때만, `validate` 및 `validated` 메서드 반환 요청 데이터에서 제외되지 않습니다. _value_가 `null`(`exclude_unless:name,null`)일 경우, 비교 대상 필드가 `null`이거나 요청 데이터에서 없을 때만 제외 대상 필드가 유지됩니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

유효성 검사 대상 필드는 _anotherfield_가 존재하면, `validate`, `validated` 메서드 반환 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

유효성 검사 대상 필드는 _anotherfield_가 존재하지 않을 때, `validate`, `validated` 메서드 반환 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

유효성 검사 대상 필드는 지정한 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

만약 `column` 옵션을 지정하지 않으면, 필드명이 그대로 사용됩니다. 위 예시의 경우, `states` 데이터베이스 테이블에 `state` 컬럼의 값이 요청의 `state` 속성과 일치하는 레코드가 존재하는지 검사합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 정의 컬럼명 지정

유효성 검사 규칙에서 사용할 데이터베이스 컬럼명을 직접 지정하고 싶으면, 테이블명 뒤에 추가하면 됩니다.

```php
'state' => 'exists:states,abbreviation'
```

가끔 특정 데이터베이스 커넥션을 이 `exists` 쿼리에 사용해야 할 수도 있습니다. 이때는 테이블명 앞에 커넥션명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, Eloquent 모델을 사용하여 테이블명을 결정하도록 지정하는 방법도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

만약 유효성 검사 규칙이 실행하는 쿼리를 직접 커스터마이즈하고 싶다면, `Rule` 클래스를 이용해 chain 방식으로 규칙을 정의할 수 있습니다. 아래 예시에서는 구분자를 `|`로 쓰는 대신 배열 형태로 규칙을 지정합니다.

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

`Rule::exists` 메서드로 생성한 규칙에 두 번째 인수로 컬럼명을 지정하면 명확하게 사용할 컬럼명을 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

여러 값이 데이터베이스에 존재하는지 배열로 한 번에 검사하고 싶다면, 해당 필드에 `exists`와 [array](#rule-array) 규칙을 모두 추가하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이 두 규칙이 필드에 모두 할당될 경우, Laravel은 내부적으로 지정된 모든 값이 해당 테이블에 존재하는지 한 번의 쿼리로 검사합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

유효성 검사 대상 파일은 지정된 확장자 목록 중 하나여야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일 검증 시, 사용자 할당 확장자만으로는 제대로 된 보안 검증이 어렵습니다. 이 규칙은 반드시 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 함께 사용해야 합니다.

<a name="rule-file"></a>
#### file

유효성 검사 대상 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

유효성 검사 대상 필드는 입력 데이터에 존재한다면 반드시 비어 있지 않아야 합니다.

<a name="rule-gt"></a>
#### gt:_field_

유효성 검사 대상 필드는 주어진 _field_ 혹은 _value_ 보다 커야 합니다. 두 필드는 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 기준으로 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

유효성 검사 대상 필드는 주어진 _field_ 혹은 _value_ 이상이어야 합니다. 두 필드는 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

유효성 검사 대상 필드는 [16진수(헥사)](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 올바른 색상값이어야 합니다.

<a name="rule-image"></a>
#### image

유효성 검사 대상 파일은 이미지(jpg, jpeg, png, bmp, gif, webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 SVG 파일을 허용하지 않습니다. 이는 XSS(크로스사이트 스크립팅) 취약점 때문입니다. 만약 SVG 파일을 허용해야 한다면, image 규칙에 `allow_svg` 지시자를 추가하세요(`image:allow_svg`).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

유효성 검사 대상 필드는 지정된 값 목록에 포함되어야 합니다. 이 규칙은 배열을 `implode`하는 경우가 많으므로, `Rule::in` 메서드를 사용해 간결하게 작성할 수 있습니다.

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

`in` 규칙과 `array` 규칙을 함께 사용하면, 입력 배열의 각 값이 모두 in 규칙에 지정된 목록에 포함되어야 합니다. 아래 예시에서 입력 배열에 있는 `LAS` 코드는 허용된 공항 목록에 없으므로 유효하지 않습니다.

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

검증 중인 필드는 _anotherfield_의 값들 중에 존재해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 중인 필드는 배열이어야 하며, 해당 배열의 키 중 적어도 하나는 주어진 _values_ 중 하나여야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증 중인 필드는 정수여야 합니다.

> [!WARNING]
> 이 유효성 검사 규칙은 입력 값이 "정수" 변수형인지 확인하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 타입만 검사합니다. 입력 값이 숫자인지도 함께 확인하려면 [`numeric` 유효성 검사 규칙](#rule-numeric)과 조합하여 사용하는 것이 좋습니다.

<a name="rule-ip"></a>
#### ip

검증 중인 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

검증 중인 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증 중인 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증 중인 필드는 올바른 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증 중인 필드는 지정된 _field_ 보다 작아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 비교됩니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 중인 필드는 지정된 _field_ 보다 작거나 같아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 비교됩니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 중인 필드는 모두 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증 중인 필드는 리스트 배열이어야 합니다. 배열의 키가 0부터 `count($array) - 1`까지의 연속된 숫자여야 리스트로 간주됩니다.

<a name="rule-mac"></a>
#### mac_address

검증 중인 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 중인 필드는 최대 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 중인 정수는 최대 길이가 _value_ 이하여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 중인 파일은 지정된 MIME 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드된 파일의 MIME 타입은 파일의 내용을 읽어 프레임워크가 추측합니다. 이 값은 클라이언트가 보낸 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 중인 파일은 나열된 확장자에 해당하는 MIME 타입이어야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정해도 되지만, 실제로는 파일의 내용을 읽어 MIME 타입을 추측하여 검사합니다. 전체 MIME 타입 목록과 그에 해당하는 확장자는 아래 링크에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 검사 규칙은 유저가 파일에 지정한 확장자와 실제 MIME 타입이 일치하는지는 확인하지 않습니다. 예를 들어, `mimes:png` 규칙은 파일 내용이 올바른 PNG 이미지라면 파일명이 `photo.txt`여도 유효하다고 판단합니다. 유저가 지정한 확장자를 검사하고 싶다면 [extensions](#rule-extensions) 규칙을 사용할 수 있습니다.

<a name="rule-min"></a>
#### min:_value_

검증 중인 필드는 최소 _value_ 이상이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 중인 정수는 최소 길이가 _value_ 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 중인 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증 중인 필드는 입력값에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_또 다른 필드_가 주어진 _value_와 같으면, 검증 중인 필드가 입력값에 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_또 다른 필드_가 지정된 _value_와 같지 않을 경우에만, 검증 중인 필드가 입력값에 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

명시된 다른 필드들 중 하나라도 존재하면, 검증 중인 필드는 입력값에 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

명시된 다른 필드들 모두가 입력값에 존재하면, 검증 중인 필드는 존재하지 않아야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 중인 필드는 지정된 값 목록에 포함되어 있으면 안 됩니다. `Rule::notIn` 메서드를 사용해 이 규칙을 메서드 체이닝으로 정의할 수도 있습니다.

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

검증 중인 필드는 지정한 정규표현식과 일치하지 않아야 합니다.

내부적으로 이 규칙은 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`가 요구하는 형식과 유효한 구분자를 포함해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` 및 `not_regex` 규칙을 사용할 때, 정규표현식에 `|` 문자가 포함되어 있으면, 파이프 구분자 대신 배열 형태로 유효성 검사 규칙을 명시해야 할 수도 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증 중인 필드는 `null`이어도 허용됩니다.

<a name="rule-numeric"></a>
#### numeric

검증 중인 필드는 [숫자형(numeric)](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<a name="rule-present"></a>
#### present

검증 중인 필드는 입력값에 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_또 다른 필드_가 주어진 _value_ 중 하나와 같으면, 검증 중인 필드는 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_또 다른 필드_가 주어진 _value_와 같지 않은 경우에만, 검증 중인 필드는 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

명시된 다른 필드들 중 하나라도 존재하면, 검증 중인 필드도 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

명시된 다른 필드들 모두가 존재하면, 검증 중인 필드도 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 중인 필드는 입력값에 없거나 비어 있어야 합니다. "비어 있음"의 기준은 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나, 비어있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만, 경로가 비어 있는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_또 다른 필드_가 주어진 _value_ 중 하나와 같으면, 검증 중인 필드는 입력값에 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나, 비어있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만, 경로가 비어 있는 경우

</div>

복잡한 조건에 따라 입력값을 허용/금지하고 싶을 때는 `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언(true/false) 값이나 클로저(Closure)를 받을 수 있습니다. 클로저를 사용하면 반환값이 `true`일 때 금지하도록 지정할 수 있습니다.

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

_또 다른 필드_가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나인 경우, 검증 중인 필드는 입력값에 없거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_또 다른 필드_가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나인 경우, 검증 중인 필드는 입력값에 없거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_또 다른 필드_가 주어진 _value_ 중 하나와 같지 않을 때만, 검증 중인 필드는 입력값에 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나, 비어있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만, 경로가 비어 있는 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 중인 필드가 존재하거나 비어있지 않은 경우, _또 다른 필드들_은 모두 반드시 없거나 비어 있어야 합니다. "비어 있음"의 기준은 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나, 비어있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만, 경로가 비어 있는 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증 중인 필드는 지정한 정규표현식과 일치해야 합니다.

내부적으로 이 규칙은 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`가 요구하는 형식과 유효한 구분자를 포함해야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` 및 `not_regex` 규칙을 사용할 때, 정규 표현식에 `|` 문자가 포함되어 있으면, 파이프 구분자 대신 배열 형태로 규칙을 명시해야 할 수 있습니다.

<a name="rule-required"></a>
#### required

검증 중인 필드는 입력값에 반드시 존재해야 하며, 비어 있으면 안 됩니다. "비어 있음"의 기준은 아래와 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나, 비어있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만 경로가 비어 있는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_또 다른 필드_가 주어진 _value_ 중 하나와 같으면, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

더 복잡한 조건의 required_if 규칙을 만들고 싶을 때는 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 받을 수 있습니다. 클로저가 사용될 경우, true를 반환하면 필드가 필수로 적용됩니다.

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

_또 다른 필드_가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나와 같으면, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_또 다른 필드_가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나와 같으면, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_또 다른 필드_가 주어진 _value_와 같지 않은 경우에만, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다. 이 규칙은 또한 요청 데이터에 _또 다른 필드_가 _value_가 null이 아니라면 반드시 존재하게 만듭니다. 만약 _value_가 `null`이라면(`required_unless:name,null`), 비교 대상 필드가 null이거나 존재하지 않을 경우 검증 중인 필드는 필수가 아니게 됩니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

명시된 다른 필드들 중 하나라도 존재하고 비어 있지 않으면, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

명시된 다른 필드들 모두가 존재하고 비어 있지 않으면, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

명시된 다른 필드들 중 하나라도 비어 있거나 존재하지 않을 때, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

명시된 다른 필드들 모두가 비어 있거나 존재하지 않을 때, 검증 중인 필드는 반드시 존재하고 비어 있으면 안 됩니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증 중인 필드는 배열이어야 하며, 지정된 키들이 반드시 포함되어 있어야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정된 _field_는 검증 중인 필드와 값이 같아야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증 중인 필드는 _value_의 크기와 정확히 일치해야 합니다. 문자열의 경우 _value_는 문자 개수, 숫자의 경우 지정한 정수값, 배열은 요소 개수, 파일의 경우는 킬로바이트 단위의 파일 크기를 의미합니다. 예시:

```php
// 문자열이 정확히 12글자인지 검사
'title' => 'size:12';

// 숫자가 10인지 검사
'seats' => 'integer|size:10';

// 배열 요소가 정확히 5개인지 검사
'tags' => 'array|size:5';

// 업로드된 파일이 정확히 512KB인지 검사
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 중인 필드는 주어진 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 중인 필드는 문자열이어야 합니다. 필드에 `null`도 허용하고 싶다면, `nullable` 규칙을 같이 지정해야 합니다.

<a name="rule-timezone"></a>
#### timezone

검증 중인 필드는 `DateTimeZone::listIdentifiers` 메서드 기준으로 유효한 타임존 식별자여야 합니다.

`DateTimeZone::listIdentifiers` 메서드에서 허용하는 [인자 목록](https://www.php.net/manual/en/datetimezone.listidentifiers.php)도 이 검증 규칙에 파라미터로 사용할 수 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증 중인 필드는 지정된 데이터베이스 테이블에 존재하지 않아야 합니다.

**사용자 지정 테이블 / 컬럼명 지정하기:**

테이블명을 직접 지정하는 대신, Eloquent 모델을 지정하여 테이블명을 결정할 수도 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션을 사용하면 필드에 대응되는 데이터베이스 컬럼명을 지정할 수 있습니다. 지정하지 않으면 검증 중인 필드명과 동일한 컬럼이 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**사용자 지정 데이터베이스 연결 사용하기**

Validator가 쿼리할 때 특정 데이터베이스 연결을 사용하고 싶다면, 테이블명 앞에 연결명을 붙일 수 있습니다.

```php
'email' => 'unique:connection.users,email_address'
```

**고유성 검사에서 특정 ID를 무시하도록 강제하기:**

가끔은 고유성 검사 시 특정 ID의 레코드는 무시하도록 하고 싶을 수 있습니다. 예를 들어, "프로필 수정" 화면에서 이름, 이메일, 지역 정보를 입력받을 때, 이메일 주소의 고유성은 확인하되 사용자가 이메일을 변경하지 않았다면(즉, 본인의 이메일로 이미 등록된 레코드는 허용) 검증 에러가 발생하지 않길 원할 수 있습니다.

이때는 `Rule` 클래스를 사용하여 fluent하게 규칙을 정의할 수 있습니다. 예시처럼 파이프(`|`)를 사용하는 대신 유효성 검사 규칙을 배열로 지정합니다.

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
> 유저가 직접 입력하는 값을 `ignore` 메서드에 전달해서는 절대 안 됩니다. 시스템이 자동 생성하는 고유 ID(예: 자동 증가 PK 또는 Eloquent 모델 인스턴스에서 가져온 UUID)만 사용해야 합니다. 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해집니다.

모델의 PK 값을 직접 넘기는 대신, 전체 모델 인스턴스를 넘겨줄 수도 있습니다. 라라벨은 자동으로 키 값을 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

만약 PK 컬럼명이 `id`가 아닌 경우, `ignore` 메서드 호출 시 컬럼명을 명시할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 검증 중인 필드명과 동일한 컬럼에서 고유성을 검사합니다. 하지만 두 번째 인자로 컬럼명을 지정할 수도 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 where 조건절 지정하기:**

`where` 메서드를 사용해 쿼리에 추가 조건을 지정할 수 있습니다. 예를 들어, `account_id` 컬럼 값이 1인 레코드만 대상으로 범위를 좁힐 수 있습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**고유성 검사 시 소프트 삭제 레코드 제외하기:**

기본적으로 unique 규칙은 소프트 삭제된 레코드도 고유성 검사에 포함합니다. 소프트 삭제된 레코드를 제외하고 검사하려면, `withoutTrashed` 메서드를 호출하면 됩니다.

```php
Rule::unique('users')->withoutTrashed();
```

만약 소프트 삭제 컬럼명이 `deleted_at`이 아니라면, 해당 컬럼명을 인자로 지정하면 됩니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증 중인 필드는 모두 대문자여야 합니다.

<a name="rule-url"></a>
#### url

검증 중인 필드는 유효한 URL이어야 합니다.

허용할 URL 프로토콜(스킴)을 지정하고 싶다면, 해당 프로토콜을 같이 명시할 수도 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증 중인 필드는 유효한 [ULID(범용 고유 사전순 정렬 식별자)](https://github.com/ulid/spec)여야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 중인 필드는 RFC 9562(v1, 3, 4, 5, 6, 7, 8 중 하나) 규격에 맞는 UUID(범용 고유 식별자)여야 합니다.

특정 버전의 UUID만 허용할 수도 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 유효성 검사 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 유효성 검사 건너뛰기

때때로, 다른 필드가 특정 값일 경우에는 검사하고 싶지 않은 필드가 있을 수 있습니다. 이때는 `exclude_if` 유효성 검사 규칙을 사용할 수 있습니다. 다음 예시에서는, `has_appointment` 필드가 `false`일 때 `appointment_date`와 `doctor_name` 필드는 유효성 검사가 수행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반면, `exclude_unless` 규칙을 사용하면, 다른 필드가 특정 값이 아닐 때 검사를 건너뛸 수 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>

#### 필드가 존재할 때만 유효성 검사하기

특정 상황에서는 유효성 검사를 수행하고자 하는 필드가 데이터에 **존재할 때만** 해당 필드에 대한 검사를 실행하고 싶을 수 있습니다. 이를 빠르게 처리하려면, `sometimes` 규칙을 규칙 목록에 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예제에서, `email` 필드는 `$data` 배열에 존재할 때만 유효성 검사가 수행됩니다.

> [!NOTE]
> 반드시 존재해야 하지만 비어 있을 수 있는 필드를 검증하려는 경우에는 [옵션 필드에 관한 이 안내](#a-note-on-optional-fields)를 참고하시기 바랍니다.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검사

더 복잡한 조건에 따라 유효성 검사 규칙을 추가하고자 할 때가 있습니다. 예를 들어, 어떤 필드의 값이 100보다 클 때만 특정 필드가 필수이거나, 다른 필드가 있을 때 두 개의 필드 모두 특정 값을 가져야 할 수도 있습니다. 이러한 조건부 유효성 검사는 어렵지 않게 구현할 수 있습니다. 먼저, _변하지 않는_ 기본 규칙(static rules)으로 `Validator` 인스턴스를 만듭니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

웹 애플리케이션이 게임 수집가를 위한 것이라고 가정해봅시다. 만약 게임 수집가가 100개가 넘는 게임을 보유 중인 상태로 회원가입을 하면, 왜 그렇게 많은 게임을 소유하고 있는지 그 이유를 설명받고 싶을 수 있습니다. 예를 들어, 중고 게임 상점을 운영한다거나 순수히 게임 수집 자체를 취미로 삼고 있을 수도 있습니다. 이런 요구사항을 조건부로 추가하기 위해, `Validator` 인스턴스의 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인수는 조건부로 유효성 검사를 할 필드의 이름입니다. 두 번째 인수에는 적용할 규칙 목록을 전달합니다. 세 번째 인수로는 클로저를 넘기며, 이 클로저가 `true`를 반환하면 해당 규칙이 적용됩니다. 이 방식을 활용하면 복잡한 조건부 유효성 검사를 간단하게 구현할 수 있습니다. 여러 개의 필드에 조건부 검사를 동시에 추가할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저로 전달되는 `$input` 인수는 `Illuminate\Support\Fluent`의 인스턴스이며, 검증 중인 입력 데이터 및 파일을 참조하는 데 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 유효성 검사

가끔은 배열 내 중첩 필드의 값에 따라, 그 인덱스를 정확히 모를 때 특정 필드를 검증해야 할 수도 있습니다. 이런 상황에서는 클로저에 두 번째 인수를 선언하여, 검증 대상으로 삼는 현재 배열 아이템을 전달받을 수 있습니다.

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

클로저로 전달되는 `$input`과 동일하게, `$item` 인수도 배열 형태의 속성 데이터라면 `Illuminate\Support\Fluent` 인스턴스이고, 그렇지 않으면 문자열이 됩니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[배열 유효성 검사 규칙 문서](#rule-array)에서 다룬 것처럼, `array` 규칙에는 허용할 배열 키 목록을 나열할 수 있습니다. 배열에 이 외의 추가 키가 있으면 유효성 검사가 실패합니다.

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

일반적으로, 배열 내에 허용할 키 목록을 반드시 지정하는 것이 좋습니다. 그렇지 않으면, 검증기(validator)의 `validate` 및 `validated` 메서드는 배열 및 (하위 검증 규칙으로 유효성 검증을 받지 않은) 모든 키들도 검증 통과 데이터로 반환합니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력값 유효성 검사

배열 기반의 중첩 폼 입력값도 어렵지 않게 유효성 검사를 할 수 있습니다. 배열 내부 속성을 검증할 때는 "닷(dot) 표기법"을 활용하면 됩니다. 예를 들어, HTTP 요청에 `photos[profile]` 필드가 있으면 다음과 같이 검증할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소별로도 검증이 가능합니다. 예를 들어, 배열 형태 입력 필드 내 각 이메일이 유일한지 확인하고 싶다면 다음처럼 작성할 수 있습니다.

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

마찬가지로, [언어 파일에서 사용자 지정 메시지 작성](#custom-messages-for-specific-attributes) 시에도 `*` 문자를 활용할 수 있어, 배열 기반 필드에 하나의 검증 메시지만 사용하기가 쉽습니다.

```php
'custom' => [
    'users.*.email' => [
        'unique' => '각 사용자마다 유일한 이메일 주소가 있어야 합니다.',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근하기

유효성 검사 규칙을 할당할 때, 중첩 배열 요소의 값을 참조해야 할 때가 있습니다. 이럴 때는 `Rule::forEach` 메서드를 사용할 수 있습니다. `forEach`는 검증 중인 배열 속성의 각 반복마다 클로저를 호출하며, 각 요소의 값과 전체 확장된 속성명을 전달합니다. 클로저는 해당 배열 요소에 적용할 규칙 배열을 반환해야 합니다.

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
### 에러 메시지에서 인덱스와 위치 참조하기

배열 검증 시, 애플리케이션에서 표시하는 에러 메시지 내에서 특정 항목의 인덱스나 위치를 참조하고 싶을 수 있습니다. 이를 위해 [사용자 지정 검증 메시지](#manual-customizing-the-error-messages)에서 `:index`(0부터 시작)와 `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다.

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
    'photos.*.description.required' => '사진 #:position의 설명을 입력해 주세요.',
]);
```

위 예제의 경우, 유효성 검사가 실패하면 사용자는 _"사진 #2의 설명을 입력해 주세요."_라는 에러 메시지를 보게 됩니다.

더 깊게 중첩된 인덱스와 위치가 필요하다면, `second-index`, `second-position`, `third-index`, `third-position` 등도 사용할 수 있습니다.

```php
'photos.*.attributes.*.string' => '사진의 속성 #:second-position이 유효하지 않습니다.',
```

<a name="validating-files"></a>
## 파일 유효성 검사

라라벨은 파일 업로드 유효성 검사에 사용할 수 있는 다양한 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 파일 검증 시 각각의 규칙을 직접 지정해도 되고, 라라벨이 제공하는 유창한(Fluent) 파일 유효성 검사 규칙 빌더를 사용할 수도 있습니다.

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

`types` 메서드를 사용할 때 파일 확장자만을 지정하면 충분하지만, 실제로는 해당 파일의 내용을 읽어서 MIME 타입을 추론해 검사합니다. MIME 타입 목록 및 확장자 전체 리스트는 아래에서 확인하실 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 유효성 검사

간편하게 파일 크기의 최소/최대 값을 문자열과 단위 접미사(`kb`, `mb`, `gb`, `tb` 지원)를 써서 지정할 수 있습니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 유효성 검사

사용자가 이미지를 업로드할 수 있는 애플리케이션에서는, `File` 규칙의 `image` 생성 메서드를 이용하여 대상 파일이 이미지(jpg, jpeg, png, bmp, gif, webp)임을 보장할 수 있습니다.

여기에 더해, `dimensions` 규칙을 사용하여 이미지의 크기도 제한할 수 있습니다.

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
> 이미지의 크기(가로/세로 등)를 검증하는 방법에 대한 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하세요.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약점 발생 가능성 때문에 SVG 파일을 허용하지 않습니다. SVG 파일도 허용하고 싶다면 `image` 규칙에 `allowSvg: true` 옵션을 넘기면 됩니다: `File::image(allowSvg: true)`

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(가로/세로) 유효성 검사

이미지의 가로/세로 크기도 유효성 검증이 가능합니다. 예를 들어, 업로드된 이미지가 가로 1000픽셀, 세로 500픽셀 이상인지 검사하려면 `dimensions` 규칙을 사용할 수 있습니다.

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
> 이미지의 크기(픽셀 단위 등) 검증에 대한 더 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하십시오.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검사

비밀번호가 적절한 복잡성을 갖추도록 하려면, 라라벨의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체는 비밀번호의 복잡성 요건(최소 길이, 영어 대·소문자, 숫자, 기호 등)을 쉽게 커스터마이즈할 수 있게 해줍니다.

```php
// 8자 이상 필수...
Password::min(8)

// 하나 이상의 영문자 필수...
Password::min(8)->letters()

// 대문자와 소문자 각각 최소 1개씩...
Password::min(8)->mixedCase()

// 하나 이상의 숫자 필수...
Password::min(8)->numbers()

// 하나 이상의 기호 필수...
Password::min(8)->symbols()
```

또한, 비밀번호가 공개된 데이터 유출(password data breach)에서 이미 노출된 적이 없는지도 `uncompromised` 메서드로 검사할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로 `Password` 규칙 객체는 [k-익명성(k-Anonymity)](https://en.wikipedia.org/wiki/K-anonymity) 모델을 활용하여 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호 유출 여부를 확인하되, 사용자의 개인정보와 보안을 침해하지 않도록 설계되어 있습니다.

기본값으로, 해당 비밀번호가 데이터 유출에서 한 번이라도 나타나면 '노출됨'으로 간주됩니다. 이 임계값(threshold)은 `uncompromised` 메서드의 첫 번째 인수로 변경할 수 있습니다.

```php
// 동일 데이터 유출에서 3번 미만만 허용...
Password::min(8)->uncompromised(3);
```

물론, 위 예시의 모든 메서드를 체이닝하여 조합할 수 있습니다.

```php
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 지정하기

애플리케이션에서 사용할 기본 비밀번호 유효성 검사 규칙을 한 곳에서 정의하면 편리합니다. `Password::defaults` 메서드와 클로저를 이용해 이를 지정할 수 있습니다. 이 메서드는 보통 앱의 서비스 프로바이더 `boot` 메서드 내에서 호출하는 것이 좋습니다.

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

이후 특정 비밀번호 필드에 기본 규칙을 적용하려면 인수 없이 `defaults` 메서드를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

가끔은 기본 비밀번호 규칙에 추가적으로 유효성 검사 규칙을 붙이고 싶을 수도 있습니다. 이때는 `rules` 메서드를 사용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 사용자 지정 유효성 검사 규칙

<a name="using-rule-objects"></a>
### 규칙 객체(Rule Object) 사용하기

라라벨에서는 많은 기본 유효성 검사 규칙을 제공하지만, 사용자만의 규칙을 정의하고 싶을 때가 있습니다. 이때 가장 대표적인 방법이 규칙 객체를 사용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용하십시오. 예를 들어, 문자열이 모두 대문자인지 검증하는 규칙을 생성해보겠습니다. 라라벨은 새 규칙 파일을 `app/Rules` 디렉토리에 생성합니다. 이 디렉터리가 없다면 Artisan 명령 실행 시 자동으로 만들어집니다.

```shell
php artisan make:rule Uppercase
```

규칙 파일이 생성되면, 이제 규칙의 실제 동작을 정의할 차례입니다. 규칙 객체에는 하나의 `validate` 메서드가 있습니다. 이 메서드는 속성명, 값, 유효성 검사 실패 시 호출할 콜백(에러 메시지 지정)을 인수로 받습니다.

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

규칙이 정의되면, 생성한 규칙 객체를 다른 유효성 검사 규칙들과 함께 검증기에 인스턴스로 전달하여 사용할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 검사 메시지 다국어 처리

`$fail` 클로저에 직접 에러 메시지 문자열을 적는 대신, [번역 문자열 키](/docs/12.x/localization)를 지정하고 라라벨이 자동 번역하도록 만들 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면, `translate` 메서드의 인수로 치환할 값(배열)과 언어 코드를 각각 첫 번째, 두 번째로 넘길 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

사용자 정의 유효성 검사 규칙 클래스에서 검증 대상 전체 데이터를 접근해야 한다면, `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하면 됩니다. 이 인터페이스는 반드시 `setData` 메서드를 구현해야 하며, 라라벨이 검증 시작 전에 모든 데이터 배열을 전달하여 호출합니다.

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

또는, 유효성 검사를 수행하는 검증기 인스턴스에 접근이 필요하다면, `ValidatorAwareRule` 인터페이스를 구현하면 됩니다.

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
### 클로저(익명 함수)로 규칙 만들기

특정 검증 규칙이 애플리케이션 내에서 단 한 번만 필요하다면, 별도 규칙 객체 대신 클로저(익명 함수)를 사용할 수도 있습니다. 이 클로저는 속성 이름, 값, 그리고 유효성 검사 실패 시 호출할 `$fail` 콜백을 받습니다.

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

기본적으로, 검증 대상 속성이 없거나 빈 문자열이라면, 기본 규칙과 사용자 정의 규칙 모두 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에 대해 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있어도 사용자 정의 규칙이 반드시 실행되길 원한다면, 해당 규칙이 '필수'임을 암시해야 합니다. 암묵적 규칙 객체를 만드는 가장 빠른 방법은 `make:rule` Artisan 명령어를 `--implicit` 옵션과 함께 사용하는 것입니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙은 속성이 반드시 존재해야 함을 _암시_합니다. 실제로 해당 규칙이 비어 있거나 없는 속성을 불합격 처리할지는 여러분의 코드에서 직접 구현해야 합니다.