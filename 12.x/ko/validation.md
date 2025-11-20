# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 메시지 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력하기](#repopulating-forms)
    - [선택 입력 필드에 대한 참고사항](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가](#authorizing-form-requests)
    - [오류 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력 준비](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 오류 백(Named Error Bags)](#named-error-bags)
    - [오류 메시지 커스터마이즈](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [유효성 검증된 입력값 사용하기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에 커스텀 속성명 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에 커스텀 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 검증](#validating-nested-array-input)
    - [오류 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션으로 들어오는 데이터를 유효성 검증하는 여러 가지 방법을 제공합니다. 가장 일반적으로는 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용하게 됩니다. 그러나 이 외에도 여러 가지 유효성 검증 방법을 다룰 예정입니다.

Laravel에는 데이터에 적용할 수 있는 다양한 편리한 유효성 검증 규칙이 포함되어 있습니다. 예를 들어, 특정 데이터베이스 테이블에서 값이 유일한지 확인하는 규칙도 제공합니다. 이 문서에서는 모든 유효성 검증 규칙에 대해 자세히 설명하므로, Laravel의 유효성 검증 기능을 종합적으로 이해할 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 쉽게 익히기 위해, 폼을 유효성 검증하고 사용자에게 오류 메시지를 표시하는 전체 예제를 살펴보겠습니다. 이 한눈에 요약된 과정을 통해, Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지에 대한 전반적인 이해를 얻을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음 라우트가 정의되어 있다고 가정하겠습니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

위의 `GET` 라우트는 사용자가 새 블로그 게시글을 작성할 수 있는 폼을 보여줍니다. `POST` 라우트는 새 블로그 게시글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

이제 위 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 확인하겠습니다. 여기서는 일단 `store` 메서드를 비워두겠습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 게시글 작성 폼을 표시합니다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 게시글을 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 게시글을 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 `store` 메서드 안에 새 블로그 게시글을 검증하는 로직을 작성해보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용할 수 있습니다. 유효성 검증 규칙을 모두 통과하면 코드가 정상적으로 계속 실행됩니다. 하지만 검증에 실패할 경우, `Illuminate\Validation\ValidationException` 예외가 발생하며 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 검증에 실패하면, 이전 URL로 리다이렉트 응답이 자동으로 생성됩니다. 만약 들어오는 요청이 XHR 요청(즉, JavaScript에서 전송한 AJAX 요청)이라면, [유효성 검증 오류 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 작동 방식을 더 잘 이해하기 위해, 다시 `store` 메서드로 돌아가 보겠습니다:

```php
/**
 * 새 블로그 게시글을 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 게시글이 유효합니다...

    return redirect('/posts');
}
```

위에서 보이는 것처럼, 유효성 검증 규칙을 `validate` 메서드에 전달합니다. 사용 가능한 모든 규칙은 [유효성 검증 규칙 문서](#available-validation-rules)를 참고하세요. 검증에 실패해도 적절한 응답이 자동으로 생성됩니다. 만약 검증에 성공하면 컨트롤러의 다음 코드가 정상적으로 실행됩니다.

또한, 검증 규칙을 `|`로 구분된 단일 문자열뿐 아니라 규칙의 배열로도 지정할 수 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

추가로, 요청을 검증하면서 오류 메시지를 [이름이 지정된 오류 백(named error bag)](#named-error-bags)에 저장하고 싶을 때는 `validateWithBag` 메서드를 사용할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단하기

어떤 경우에는 한 속성에 대해 첫 번째 검증 실패가 발생하면 그 다음 검증 규칙은 더 이상 실행하고 싶지 않을 수 있습니다. 이럴 땐 해당 속성에 `bail` 규칙을 추가하세요:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서는 만약 `title` 속성의 `unique` 규칙이 실패하면, `max` 규칙은 검사하지 않습니다. 규칙들은 지정된 순서대로 처리됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고사항

들어오는 HTTP 요청에 "중첩"된 필드 데이터가 포함된 경우, 유효성 검사 규칙에서 "점 표기법(dot notation)"을 사용하여 필드를 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드 이름에 실제 점(`.`)이 포함된 경우, 백슬래시(`\.`)로 해당 점을 이스케이프 처리하여 "dot 문법"으로 해석되지 않도록 할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 메시지 표시하기

만약 들어오는 요청 필드가 지정한 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞에서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 또한, 모든 유효성 오류와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 [세션에 플래시(flash)](/docs/12.x/session#flash-data)되어 저장됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어가 `$errors` 변수를 여러분 애플리케이션의 모든 뷰에 공유합니다(이 미들웨어는 `web` 미들웨어 그룹에 포함됩니다). 이 미들웨어가 적용된 경우, 여러분의 뷰에서는 언제든 `$errors` 변수가 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 사용하는 방법은 [별도 문서](#working-with-error-messages)를 참고하세요.

예제에서는 검증 실패 시 컨트롤러의 `create` 메서드로 리다이렉트되어 뷰에서 오류 메시지를 표시할 수 있습니다:

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
#### 오류 메시지 커스터마이즈

Laravel의 기본 유효성 검증 규칙별 오류 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 사용하여 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 수정하거나 변경할 수 있습니다.

또한, 이 파일을 원하는 언어의 디렉터리로 복사하여 각 언어에 맞게 메시지를 번역하면 됩니다. Laravel의 현지화에 대해 더 알아보고 싶다면 [현지화 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령을 통해 파일을 게시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이 예제에서는 전통적인 form을 이용해 데이터를 애플리케이션에 전송했습니다. 하지만, 많은 애플리케이션이 JavaScript로 구현된 프론트엔드에서 XHR 요청을 받기도 합니다. XHR 요청에서 `validate` 메서드를 사용할 경우, Laravel은 리다이렉트 응답을 생성하지 않습니다. 대신, [유효성 검증 오류가 담긴 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 422 HTTP 상태 코드를 포함합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성의 유효성 검증 오류 메시지가 존재하는지 빠르게 확인하려면, [Blade](/docs/12.x/blade)에서 `@error` 디렉티브를 사용할 수 있습니다. `@error` 디렉티브 내부에서 `$message` 변수를 출력하여 오류 메시지를 표시할 수 있습니다:

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

[이름이 지정된 오류 백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인수로 오류 백의 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력하기

Laravel이 유효성 검증 실패로 리다이렉트 응답을 생성할 때, 프레임워크는 모든 [요청 입력값을 세션에 플래시](/docs/12.x/session#flash-data)합니다. 이렇게 하면, 다음 요청에서 편리하게 입력값에 접근하여 사용자가 제출하려 했던 폼을 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. `old` 메서드는 [세션](/docs/12.x/session)에서 플래시된 입력값을 꺼내옵니다:

```php
$title = $request->old('title');
```

또한, Laravel은 글로벌 헬퍼 함수인 `old`를 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 예전 입력값을 표시할 때는 `old` 헬퍼를 사용하는 것이 더 편리합니다. 입력값이 존재하지 않으면 `null`이 반환됩니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 입력 필드에 대한 참고사항

기본적으로 Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 포함하고 있습니다. 이 미들웨어들로 인해 "선택" 입력 필드를 `nullable`로 지정하지 않으면, `null` 값도 유효하지 않은 것으로 간주됩니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서는 `publish_at` 필드가 `null`이거나 올바른 날짜 형식일 수 있음을 지정합니다. 만약 규칙 정의에 `nullable`을 추가하지 않으면, 검증자는 `null` 값을 유효한 날짜로 보지 않습니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외를 발생시키고 들어오는 HTTP 요청이 JSON 응답을 기대한다면, Laravel은 자동으로 오류 메시지를 포맷하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래는 유효성 검증 오류에 대한 JSON 응답 포맷 예제입니다. 중첩된 오류 키는 평탄화되어 "dot" 표기법으로 표시됩니다:

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

더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(form request)" 클래스를 생성할 수 있습니다. 폼 리퀘스트는 자체적으로 유효성 검증과 인가 로직을 포함하는 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 생성하려면 `make:request` Artisan CLI 명령어를 사용하세요:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치하게 됩니다. 이 디렉터리가 없다면, `make:request` 명령 실행 시 자동 생성됩니다. Laravel에서 생성된 각 폼 리퀘스트에는 `authorize`와 `rules` 두 가지 메서드가 포함되어 있습니다.

예상 가능하듯이, `authorize` 메서드는 현재 인증된 사용자가 요청이 나타내는 동작을 수행할 수 있는지 판단하는 역할이며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다:

```php
/**
 * 요청에 적용되는 유효성 검증 규칙을 반환합니다.
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
> `rules` 메서드 시그니처에서 필요한 의존성을 타입힌트로 명시하면, Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

그렇다면 이 유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드의 파라미터에서 생성한 폼 리퀘스트를 타입힌트로 선언하면 됩니다. 이렇게 하면 컨트롤러 메서드가 호출되기 전에 해당 폼 리퀘스트가 자동으로 유효성 검증을 거치게 됩니다. 따라서 컨트롤러에 유효성 검증 로직을 직접 작성할 필요가 없습니다:

```php
/**
 * 새 블로그 게시글을 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 들어오는 요청이 유효합니다...

    // 검증된 입력값 받아오기...
    $validated = $request->validated();

    // 일부만 받아오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 게시물 저장...

    return redirect('/posts');
}
```

검증에 실패할 경우, 이전 위치로 이동하는 리다이렉트 응답이 자동으로 생성됩니다. 오류 정보도 세션에 플래시되어, 화면 표시용으로 사용 가능합니다. 요청이 XHR 요청이라면 422 상태 코드와 함께 [유효성 검증 오류의 JSON 표현](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반의 Laravel 프론트엔드에서 폼 리퀘스트 실시간 유효성 검증이 필요하다면 [Laravel Precognition](/docs/12.x/precognition)을 확인해보세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행하기

기본 유효성 검증 이후에 추가적인 검증이 필요하다면, 폼 리퀘스트의 `after` 메서드를 사용하세요.

`after` 메서드는 검증 완료 후, 호출될 콜러블(callable) 또는 클로저(closure) 배열을 반환해야 합니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아, 추가 오류 메시지를 등록할 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * 폼 리퀘스트의 "after" 유효성 검증 콜러블을 반환합니다.
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

위 예시처럼, `after` 메서드가 반환하는 배열에는 인보커블(invokable) 클래스도 포함할 수 있습니다. 이 클래스들의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 폼 리퀘스트의 "after" 유효성 검증 콜러블을 반환합니다.
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
#### 첫 번째 유효성 검증 실패 시 중단하기

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 하나라도 유효성 검증에 실패하면 모든 속성에 대한 검증을 즉시 중단하도록 검증자에게 알릴 수 있습니다:

```php
/**
 * 검증자가 첫 번째 규칙 실패 시 전체 검증을 중단할지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이즈

폼 리퀘스트 유효성 검증 실패 시, 이전 위치로 리다이렉트하는 응답이 자동으로 생성됩니다. 하지만 이 동작은 자유롭게 수정할 수 있습니다. 이를 위해 폼 리퀘스트에 `$redirect` 프로퍼티를 정의하세요:

```php
/**
 * 유효성 검증 실패 시 사용자가 리다이렉트될 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

혹은, 네임드 라우트로 리다이렉트하고 싶다면 `$redirectRoute` 프로퍼티를 설정하세요:

```php
/**
 * 유효성 검증 실패 시 사용자가 리다이렉트될 라우트명.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 안에서, 인증된 사용자가 특정 리소스를 실제로 수정(업데이트)할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 자신이 작성한 블로그 댓글만 수정할 수 있도록 검사할 수 있습니다. 일반적으로 이 메서드에서는 [인가 게이트 및 정책](/docs/12.x/authorization)과 상호작용하게 됩니다:

```php
use App\Models\Comment;

/**
 * 사용자가 이 요청을 수행할 인가가 있는지 확인합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 Laravel의 기본 리퀘스트 클래스를 확장하므로, `user` 메서드를 통해 현재 인증된 사용자에게 접근할 수 있습니다. 또한, 위 예시에서의 `route` 메서드를 통해 호출된 라우트의 URI 파라미터(예: `{comment}`) 값에 접근할 수 있습니다:

```php
Route::post('/comment/{comment}');
```

따라서 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용할 경우, 요청의 속성처럼 해석된 모델 인스턴스에 더욱 간단히 접근할 수 있습니다:

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, 자동으로 403 상태 코드와 함께 HTTP 응답이 반환되며 컨트롤러 메서드는 실행되지 않습니다.

요청의 인가 로직을 애플리케이션의 다른 부분에서 처리하려면, `authorize` 메서드를 완전히 제거하거나 그냥 항상 `true`를 반환하도록 구현하면 됩니다:

```php
/**
 * 사용자가 이 요청을 수행할 인가가 있는지 확인합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드의 시그니처에서도 필요한 의존성을 타입힌트로 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

폼 리퀘스트에서 사용하는 오류 메시지를 커스터마이즈하려면 `messages` 메서드를 오버라이드하면 됩니다. 이 메서드는 속성/규칙 쌍에 해당하는 오류 메시지 배열을 반환해야 합니다:

```php
/**
 * 정의된 유효성 검증 규칙에 대한 오류 메시지를 반환합니다.
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

Laravel의 내장 유효성 오류 메시지에는 `:attribute` 플레이스홀더가 자주 포함됩니다. 오류 메시지의 `:attribute` 값을 커스텀 속성명으로 치환하려면, `attributes` 메서드를 오버라이드하여 속성/이름 쌍의 배열을 반환할 수 있습니다:

```php
/**
 * Validator 오류에서 커스텀 속성명을 반환합니다.
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
### 유효성 검증을 위한 입력 준비

검증 규칙을 적용하기 전에 요청 데이터의 일부를 정제하거나 가공해야 할 때는, `prepareForValidation` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증을 위한 데이터 전처리.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

마찬가지로, 유효성 검증이 끝난 후 요청 데이터를 정규화(normalize)해야 한다면, `passedValidation` 메서드를 사용할 수 있습니다:

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
## 수동으로 Validator 생성하기 (Manually Creating Validators)

HTTP 요청의 `validate` 메서드를 사용하지 않고, 직접 Validator 인스턴스를 생성할 수도 있습니다. 이때는 `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 사용합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 게시글을 저장합니다.
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

        // 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 게시글 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인수는 검증할 데이터이며, 두 번째 인수는 데이터에 적용할 유효성 검증 규칙 배열입니다.

요청 검증 실패 여부를 확인한 뒤, `withErrors` 메서드를 사용해 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드는 Validator, `MessageBag`, 또는 PHP 배열 모두를 인수로 받을 수 있습니다. 리다이렉션 후 뷰에서 `$errors` 변수를 통해 자동으로 접근할 수 있어, 사용자에게 오류 메시지를 쉽게 표시할 수 있습니다.

#### 첫 번째 검증 실패 시 중단하기

`stopOnFirstFailure` 메서드를 사용하면, 하나라도 유효성 검증이 실패하면 전체 속성 검증을 중단하도록 할 수 있습니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

Validator 인스턴스를 수동으로 생성하더라도, HTTP 요청의 `validate` 메서드에서 지원하는 자동 리다이렉션 기능을 그대로 사용하고 싶을 수 있습니다. 이럴 경우, 생성된 Validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 검증 실패 시 사용자는 자동으로 리다이렉트 또는, XHR 요청의 경우 [JSON 응답을 받게 됩니다](#validation-error-response-format):

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

오류 메시지를 [이름이 지정된 오류 백](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수도 있습니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 오류 백 (Named Error Bags)

한 페이지에 여러 개의 폼이 있는 경우, 각각의 폼 오류 메시지를 구분해서 관리하고 싶을 수 있습니다. 이럴 때, 오류 메시지를 담은 `MessageBag`에 이름을 붙여서 특정 폼 용 메시지만 구분해 가져올 수 있습니다. 다음과 같이 사용할 수 있습니다:

```php
return redirect('/register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수에서 명명된 `MessageBag` 인스턴스에 접근할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

필요하다면, Validator 인스턴스가 사용하는 기본 오류 메시지 대신 커스텀 오류 메시지를 지정할 수 있습니다. 먼저, `Validator::make` 메서드의 세 번째 인수로 메시지 배열을 전달하는 방법이 있습니다:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

여기서 `:attribute` 플레이스홀더는 검증 대상 필드명으로 치환됩니다. 또 다른 플레이스홀더도 사용할 수 있습니다. 예를 들면:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성만을 위한 커스텀 메시지 지정

특정 속성에 대해서만 커스텀 오류 메시지를 지정하려는 경우, "dot" 표기법을 사용하세요. 속성명 다음에 규칙명을 붙여서 지정합니다:

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

Laravel의 기본 오류 메시지에는 자주 `:attribute` 플레이스홀더가 들어 있습니다. 특정 필드에 자체적 속성명을 사용할 때는, 커스텀 속성 배열을 `Validator::make`의 네 번째 인수로 지정하세요:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행하기

기본 검증 외에 추가적인 검증이 필요하다면, Validator의 `after` 메서드를 사용할 수 있습니다. 이 메서드는 검증 완료 후 실행할 클로저 혹은 콜러블의 배열을 받습니다. 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 전달받으므로, 필요시 추가 오류 메시지를 등록할 수 있습니다:

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

위의 `after` 메서드는 콜러블의 배열도 받을 수 있습니다. 인보커블 클래스로 후처리 유효성 검증 로직을 분리 관리할 수 있으며, 각 클래스는 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받습니다:

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

폼 리퀘스트 또는 수동으로 생성한 Validator 인스턴스를 통해 요청 데이터를 유효성 검증한 뒤, 실제 검증을 통과한 입력값을 얻고 싶을 때가 많습니다. 이를 위해 여러 방법이 제공됩니다. 우선, 폼 리퀘스트나 Validator 인스턴스에서 `validated` 메서드를 호출하세요. 이 메서드는 검증에 통과한 데이터 배열을 반환합니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체는 `only`, `except`, `all` 메서드를 통해 검증된 데이터 일부 또는 전체를 반환합니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복하거나 인덱싱하여 접근할 수 있습니다:

```php
// 반복문 사용...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근...
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 합치고 싶을 때는 `merge` 메서드를 사용할 수 있습니다:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 받고 싶다면 `collect` 메서드를 사용하세요:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기 (Working With Error Messages)

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 방식으로 오류 메시지를 다룰 수 있는 `Illuminate\Support\MessageBag` 인스턴스를 얻을 수 있습니다. `$errors` 변수 역시 이 `MessageBag` 클래스를 사용합니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 오류 메시지 가져오기

특정 필드의 첫 번째 오류 메시지를 가져오려면 `first` 메서드를 사용하세요:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

특정 필드에 대한 모든 메시지를 배열로 얻으려면 `get` 메서드를 사용하세요:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 폼 필드에 대한 각 배열 요소의 모든 메시지를 얻으려면 `*` 문자를 사용하세요:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 가져오기

모든 필드의 메시지를 배열로 가져오려면 `all` 메서드를 사용하세요:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드 오류 메시지 존재 여부 확인

`has` 메서드를 사용해 해당 필드의 오류 메시지가 존재하는지 확인할 수 있습니다:

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에 커스텀 메시지 지정하기

Laravel의 내장 유효성 검증 규칙 오류 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 사용해 생성할 수 있습니다.

이 파일에는 각 유효성 검증 규칙별 번역 항목이 들어 있습니다. 필요에 따라 자유롭게 수정하세요.

또한, 커스텀 언어를 위해 이 파일을 원하는 언어 디렉터리로 복사해 번역할 수도 있습니다. Laravel 현지화에 대해 자세히 알고 싶다면 [현지화 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스텀하려면 `lang:publish` Artisan 명령어로 게시하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성 전용 커스텀 오류 메시지

언어 파일의 `custom` 배열에 특정 속성/규칙 조합용 커스텀 오류 메시지를 지정할 수 있습니다:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에 커스텀 속성명 지정하기

기본 오류 메시지의 `:attribute` 플레이스홀더를 커스텀 값으로 변경하려면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 지정하세요:

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스텀하려면, `lang:publish` Artisan 명령어를 통해 파일을 게시하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에 커스텀 값 지정하기

내장 유효성 검증 규칙 오류 메시지 중 일부는 값에 따라 `:value` 플레이스홀더가 포함될 수 있습니다. 가끔은 이 값 부분에 대해 사용자 친화적인 표시가 필요할 수 있습니다. 예를 들어, `payment_type`이 `cc`일 때 신용카드 번호를 요구하는 규칙이 아래와 같다고 합시다:

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 경우 검증 실패 메시지는 다음과 같이 나옵니다:

```text
The credit card number field is required when payment type is cc.
```

`cc` 표시 대신 좀 더 친절하게 표현하려면, 언어 파일의 `values` 배열을 아래처럼 지정합니다:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스텀하려면 `lang:publish` Artisan 명령어로 파일을 게시하세요.

이제 해당 메시지는 다음과 같이 표시됩니다:

```text
The credit card number field is required when payment type is credit card.
```

# 이하 생략:  
아래 섹션부터는 기존 규칙과 동일하게,  
- 제목은 "한국어 제목 (영어 원제)"  
- 그 외는 자연스럽고 정확하게 번역  
- 코드 및 기술 식별자는 그대로 유지  
방식으로 이어서 상세 규칙을 번역합니다.

> (이어서 요청 시 제공해드릴 수 있습니다.)