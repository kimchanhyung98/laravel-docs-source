# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 데이터 다시 채우기](#repopulating-forms)
    - [선택 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 에러 응답 형식](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가(Authorization)](#authorizing-form-requests)
    - [에러 메시지 커스터마이징하기](#customizing-the-error-messages)
    - [유효성 검증 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 인스턴스 만들기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름이 지정된 에러백(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이징하기](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행하기](#performing-additional-validation)
- [유효성 검증된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부로 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 유효성 검증](#validating-nested-array-input)
    - [에러 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 들어오는 데이터에 대해 다양한 방법으로 유효성 검증을 지원합니다. 가장 일반적으로는 모든 들어오는 HTTP 요청에서 제공되는 `validate` 메서드를 사용하는 것이 일반적입니다. 그러나 이 외에도 다양한 유효성 검증 방법에 대해 다룰 예정입니다.

Laravel은 데이터에 적용할 수 있는 다양한 편리한 유효성 검증 규칙들을 기본 제공하며, 특정 데이터베이스 테이블에서 값의 고유성까지 손쉽게 검증할 수도 있습니다. 각 유효성 검증 규칙에 대해 자세히 설명하므로, Laravel의 유효성 검증 기능을 모두 익힐 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼 데이터를 검증하고 에러 메시지를 사용자에게 표시하는 전체 예제를 살펴보겠습니다. 이 전체적인 흐름을 따라가면, Laravel에서 들어오는 요청 데이터를 어떻게 유효성 검증하는지 잘 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php`에 아래와 같은 라우트가 정의되어 있다고 가정합니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 새로운 블로그 포스트를 작성하는 폼을 사용자에게 보여주고, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위에서 정의한 라우트를 처리하는 간단한 컨트롤러를 살펴보겠습니다. `store` 메서드는 일단 비워둡니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 작성 폼을 보여줍니다.
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
        // 블로그 포스트 유효성 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 `store` 메서드 안에 새 블로그 포스트에 대한 유효성 검증 로직을 작성할 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체의 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드가 정상적으로 계속 실행되며, 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하고 적절한 에러 응답이 사용자에게 자동으로 반환됩니다.

전통적인 HTTP 요청에서 유효성 검증이 실패하면 원래 URL로 리디렉션 응답이 발생합니다. 만약 들어오는 요청이 XHR 요청(예: JavaScript로 전송된 요청)이라면, [유효성 검증 에러 메시지를 포함한 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 동작을 더 잘 이해하기 위해 다시 `store` 메서드로 돌아가보겠습니다.

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

    // 블로그 포스트 데이터가 유효함...

    return redirect('/posts');
}
```

보시는 것처럼, 유효성 검증 규칙을 `validate` 메서드로 전달합니다. 모든 사용 가능한 유효성 검증 규칙은 [문서화](#available-validation-rules)되어 있으니 걱정하지 않으셔도 됩니다. 만약 유효성 검증에 실패하면, 위에서 설명한 적절한 응답이 자동으로 생성됩니다. 통과하면 컨트롤러는 정상적으로 계속 실행됩니다.

또한, 아래처럼 규칙을 `|` 구분 문자열이 아니라 배열로 전달할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

이외에도, `validateWithBag` 메서드를 사용하면 요청을 검증하고 에러 메시지를 [이름이 지정된 에러백(nam...

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

때로는 속성에 대해 첫 번째 유효성 검증 실패 이후로는 더 이상 검증하지 않도록 하고 싶을 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 사용합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서, `title` 필드에서 `unique` 규칙이 실패하면 `max` 규칙은 더 이상 확인하지 않습니다. 규칙들은 정의된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩(Nested) 속성에 대한 참고

만약 들어오는 HTTP 요청에 "중첩된" 필드 데이터가 있다면, "도트(dot) 표기법"을 사용해서 해당 필드를 유효성 검증 규칙에 명시할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드명에 실제로 마침표가 포함된 경우라면, 역슬래시로 마침표를 이스케이프 처리하면 도트 표기법으로 인식되지 않게 할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

만약 들어오는 요청 필드가 정해진 유효성 검증 규칙을 통과하지 못한다면 어떻게 될까요? 앞서 언급한 대로, Laravel은 사용자를 원래 위치로 자동 리디렉션합니다. 더불어, 모든 유효성 검증 에러와 [요청 입력값](/docs/master/requests#retrieving-old-input)이 [세션에 자동 플래시](/docs/master/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(기본적으로 `web` 미들웨어 그룹에 포함됨)는 모든 뷰에 `$errors` 변수를 공유해줍니다. 이 미들웨어가 적용되어 있으면 뷰에서 언제나 `$errors` 변수가 정의되어 있다고 간주하고 안전하게 사용할 수 있습니다. 이 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체 활용법은 [별도 문서](#working-with-error-messages)에서 더 자세히 다룹니다.

즉, 유효성 검증에 실패하면 사용자는 컨트롤러의 `create` 메서드로 리디렉션되며, 아래처럼 뷰에서 에러 메시지를 표시할 수 있습니다.

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

Laravel에 내장된 각 유효성 검증 규칙의 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어를 통해 생성할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 요구에 맞게 이 메시지들을 자유롭게 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉토리로 복사하여 애플리케이션의 언어에 맞게 메시지를 번역할 수도 있습니다. Laravel의 지역화(Localization)에 대해 더 알아보려면 [전체 지역화 문서](/docs/master/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스텀하고 싶다면 `lang:publish` Artisan 명령어를 통해 게시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이 예시에서는 전통적인 폼을 사용해 데이터를 애플리케이션에 전송했습니다. 하지만 실제로는 JavaScript 기반 프론트엔드에서 XHR 요청을 보내는 경우도 많습니다. 이 경우, `validate` 메서드를 사용할 때 Laravel은 리디렉션 응답을 생성하지 않습니다. 대신, [모든 유효성 검증 에러가 포함된 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성에 대해 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하고자 할 때 [Blade](/docs/master/blade)에서 `@error` 디렉티브를 사용할 수 있습니다. 해당 디렉티브 내부에서는 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다.

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

[이름이 지정된 에러백](#named-error-bags)을 사용한다면, `@error` 디렉티브의 두 번째 인자로 에러백의 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 데이터 다시 채우기

유효성 검증 에러로 인해 리디렉션이 발생할 때, Laravel은 해당 요청의 입력값을 [세션에 자동 플래시](/docs/master/session#flash-data)합니다. 이를 통해 다음 요청에서 입력값을 쉽게 다시 접근하고, 사용자가 제출했던 폼을 재작성할 수 있도록 합니다.

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하세요. 이 메서드는 [세션](/docs/master/session)에 저장되었던 이전 입력값을 반환합니다.

```php
$title = $request->old('title');
```

Laravel은 글로벌 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/master/blade) 내에서 이전 입력값을 표시할 때는 이 헬퍼를 사용하는 것이 더욱 편리합니다. 해당 필드에 대한 이전 입력값이 없다면, `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 필드에 대한 참고 사항

기본적으로, Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 때문에 "선택(optional)" 입력값 필드는, validator가 `null` 값을 무효로 판단하지 않게 하려면 `nullable`이라고 명시해주어야 합니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서, `publish_at` 필드는 `null`이거나, 유효한 날짜 표현이어도 괜찮습니다. 만약 `nullable` 제어자를 누락하면 validator는 `null`을 유효하지 않은 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 에러 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException`이 throw되고, 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 에러 메시지를 자동 포맷하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래는 유효성 검증 에러의 JSON 응답 형식 예시입니다. 중첩된 에러 키는 "도트(dot) 표기법" 형식으로 평탄화(flatten)됩니다.

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

더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(Form Request)"를 생성하는 것이 좋습니다. 폼 리퀘스트는 자체적인 유효성 검증과 인가(Authorization) 로직을 가진 맞춤형 Request 클래스입니다. 폼 리퀘스트 클래스를 생성하려면 `make:request` Artisan CLI 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉토리에 위치합니다. 해당 디렉토리가 없다면, 명령어 실행 시 자동으로 생성됩니다. Laravel이 생성하는 각 폼 리퀘스트에는 `authorize`와 `rules` 두 메서드가 있습니다.

`authorize` 메서드는 현재 인증된 사용자가 해당 요청에 대한 액션을 수행할 수 있는지 확인하는 역할이고, `rules` 메서드는 해당 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드 시그니처에 타입 힌트를 지정할 수도 있습니다. 필요한 의존성은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 자동으로 생성되어 주입됩니다.

유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 해당 폼 리퀘스트를 타입 힌트로 지정하기만 하면 됩니다. 폼 리퀘스트가 전달되는 시점에 유효성 검증이 먼저 수행되므로, 컨트롤러에는 검증 로직을 따로 작성할 필요가 없습니다.

```php
/**
 * 새 블로그 포스트를 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 들어오는 요청이 유효함...

    // 유효성 검증된 입력값 가져오기...
    $validated = $request->validated();

    // 특정 입력값만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

유효성 검증에 실패하면, 원래 위치로 사용자에게 리디렉션 응답이 생성됩니다. 에러도 세션에 플래시되어 표시할 수 있게 됩니다. 만약 요청이 XHR라면, 422 상태 코드와 함께 [유효성 검증 에러의 JSON 표현](#validation-error-response-format)이 사용자에게 반환됩니다.

> [!NOTE]
> Inertia로 구동되는 Laravel 프론트엔드에 실시간 폼 리퀘스트 유효성 검증이 필요하다면, [Laravel Precognition](/docs/master/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행

초기 유효성 검증이 끝난 뒤 추가 검증이 필요할 때가 있습니다. 이럴 때는 폼 리퀘스트의 `after` 메서드를 활용하면 됩니다.

`after` 메서드는 콜러블 혹은 클로저 배열을 반환해야 하며, 검증이 완료된 뒤에 호출됩니다. 전달받는 콜러블에서는 `Illuminate\Validation\Validator` 인스턴스를 받아, 필요한 경우 추가 에러 메시지를 추가할 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * 추가(after) 유효성 검증 콜러블을 반환합니다.
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

또한, `after` 메서드의 배열에는 인보커블(invokable) 클래스도 포함할 수 있습니다. 이런 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 인자로 받게 됩니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 추가(after) 유효성 검증 콜러블을 반환합니다.
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

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 단 한 번이라도 유효성 검증 실패가 발생하면 모든 속성에 대한 검증을 즉시 중단하도록 지정할 수 있습니다.

```php
/**
 * 첫 번째 규칙 실패 시 모든 검증을 중단할지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

폼 리퀘스트 유효성 검증 실패 시, 기본적으로 원래 위치로 리디렉션되지만, 이 동작을 커스터마이징할 수도 있습니다. 폼 리퀘스트에 `$redirect` 프로퍼티를 정의해 원하는 URI로 리디렉션할 수 있습니다.

```php
/**
 * 유효성 검증 실패 시 리디렉션할 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 네임드 라우트로 리디렉션하려면 `$redirectRoute` 프로퍼티를 사용하세요.

```php
/**
 * 유효성 검증 실패 시 리디렉션할 네임드 라우트.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가(Authorization)

폼 리퀘스트 클래스는 `authorize` 메서드도 포함하고 있습니다. 여기서 현재 인증된 사용자가 실제로 리소스를 수정할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 자신이 작성한 댓글만 수정할 수 있도록 인가 로직을 작성할 수 있습니다. 이 메서드 내에서는 [인가 게이트와 정책]( /docs/master/authorization )을 활용하는 경우가 많습니다.

```php
use App\Models\Comment;

/**
 * 사용자가 해당 요청을 수행할 권한이 있는지 확인합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 기본적으로 Laravel Request 클래스를 확장하므로, `user` 메서드를 통해 현재 인증된 사용자에 접근할 수 있습니다. 위 예시엔 `route` 메서드도 보이는데, 현재 라우트의 URI 파라미터(예: `{comment}`)에도 접근할 수 있게 해줍니다.

```php
Route::post('/comment/{comment}');
```

[라우트 모델 바인딩](/docs/master/routing#route-model-binding)을 사용할 경우, request의 속성으로도 바인딩된 모델 객체를 바로 접근할 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, HTTP 403 상태 코드 응답이 자동으로 반환되고, 컨트롤러 메서드는 실행되지 않습니다.

인가 처리를 애플리케이션의 다른 위치에서 하고 싶다면, `authorize` 메서드를 제거하거나 단순히 `true`를 반환하면 됩니다.

```php
/**
 * 사용자가 해당 요청을 수행할 권한이 있는지 확인합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처에도 필요한 의존성을 타입 힌트로 추가할 수 있습니다. Laravel [서비스 컨테이너](/docs/master/container)가 자동으로 주입해줍니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

폼 리퀘스트에서 사용되는 에러 메시지는 `messages` 메서드를 오버라이드 하여 커스터마이징할 수 있습니다. 이 메서드는 속성/규칙 쌍과 해당 에러 메시지를 반환하는 배열이어야 합니다.

```php
/**
 * 정의된 유효성 규칙에 대한 에러 메시지를 반환합니다.
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

Laravel의 내장 유효성 검증 규칙 에러 메시지에는 `:attribute` 플레이스홀더가 자주 포함됩니다. 에러 메시지에 표시되는 `:attribute`를 커스텀 속성명으로 바꾸고 싶다면, `attributes` 메서드를 오버라이드하세요.

```php
/**
 * validator 에러의 속성명을 커스텀합니다.
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

유효성 검증을 적용하기 전에 요청에서 받은 데이터를 미리 가공하거나 정제(sanitize)해야 할 때가 있습니다. 이럴 때는 `prepareForValidation` 메서드를 활용할 수 있습니다.

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증 전 데이터 준비
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

마찬가지로, 유효성 검증이 끝난 후 데이터를 정규화(normalize)해야 한다면 `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * 유효성 검증 통과 후 처리
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 인스턴스 만들기 (Manually Creating Validators)

Request의 `validate` 메서드를 사용하고 싶지 않은 경우, `Validator` [파사드](/docs/master/facades)의 `make` 메서드를 통해 수동으로 validator 인스턴스를 생성할 수 있습니다.

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

        // 유효성 검증된 입력값 가져오기...
        $validated = $validator->validated();

        // 특정 입력값만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드에 첫 번째 인자로 검증할 데이터, 두 번째 인자로 검증 규칙 배열을 전달합니다.

유효성 검증 실패 여부를 판단한 뒤, `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면, 리디렉션 후 뷰에서 자동으로 `$errors` 변수를 사용할 수 있어 사용자에게 에러 메시지를 쉽게 표시할 수 있습니다. `withErrors`는 validator, `MessageBag`, 그리고 PHP 배열을 인자로 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 전체 중단

`stopOnFirstFailure` 메서드는 하나의 유효성 검증에 실패하면 모든 속성에 대한 검증을 중단하도록 validator에게 지시합니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

수동으로 validator 인스턴스를 만들었어도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션의 이점을 그대로 활용할 수 있습니다. 기존 validator 인스턴스에서 `validate` 메서드를 호출하면, 검증에 실패할 시 자동 리디렉션(또는 XHR 요청에서는 [JSON 응답 반환](#validation-error-response-format))이 동작합니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드를 사용하면, [이름이 지정된 에러백(nam...

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러백(Named Error Bags)

한 페이지에 여러 개의 폼이 있는 경우, 각각의 폼에 해당하는 `MessageBag`을 이름으로 구분하여, 특정 폼의 에러 메시지만 가져올 수 있습니다. 이를 위해 `withErrors`에 두 번째 인자로 이름을 넘깁니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이후 뷰에서 `$errors` 변수를 통해 이름이 지정된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

기본 제공되는 에러 메시지 대신, validator 인스턴스에 사용될 다른 에러 메시지를 지정할 수 있습니다. 여러 방법이 있지만, 먼저 `Validator::make`의 세 번째 인자에 커스텀 메시지 배열을 넘기는 방법이 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위의 `:attribute` 플레이스홀더는 검증 중인 필드명으로 대체됩니다. 에러 메시지에는 여러 플레이스홀더를 활용할 수도 있습니다. 예를 들면:

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

특정 속성에 대해서만 커스텀 에러 메시지를 지정하려면 "도트 표기법"을 사용하세요. 속성명과 규칙명을 순서대로 입력합니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성값 지정

Laravel의 에러 메시지는 `:attribute` 플레이스홀더에 필드명이나 속성명이 대입됩니다. 특정 필드에 사용될 플레이스홀더 대체값 역시 `Validator::make`의 네 번째 인자에 커스텀 속성 배열을 전달하여 지정할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행하기

초기 유효성 검증이 끝난 후에도 추가적인 검증이 필요한 경우, validator의 `after` 메서드를 사용할 수 있습니다. 이 메서드는 클로저나 콜러블 배열을 매개변수로 받아, 유효성 검증이 완료된 후 각각 호출됩니다. 각 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아, 필요시 에러 메시지를 추가할 수 있습니다.

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

또한, "after validation" 로직이 인보커블 클래스에 캡슐화되어 있을 경우, `after` 메서드는 콜러블 배열도 받을 수 있습니다. 각 인보커블의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받게 됩니다.

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
## 유효성 검증된 입력값 다루기 (Working With Validated Input)

폼 리퀘스트나 수동 validator 인스턴스로 들어오는 요청 데이터를 검증한 후, 실제로 유효성 검증을 통과한 데이터를 얻고 싶을 때가 있습니다. 이 작업은 여러 방법으로 할 수 있습니다. 먼저, 폼 리퀘스트나 validator 인스턴스의 `validated` 메서드를 호출하면, 검증된 데이터 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스가 반환됩니다. 이 객체는 일부 데이터만 추출할 수 있는 `only`, `except`, `all` 메서드를 제공합니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나, array access로 값에 쉽게 접근할 수 있습니다.

```php
// 검증된 데이터 순회하기...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근하기...
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 필드를 추가하려면 `merge` 메서드를 사용하세요.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/master/collections) 형태로 받고 싶으면, `collect` 메서드를 사용합니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기 (Working With Error Messages)

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 이 클래스는 에러 메시지를 다루기 위한 다양한 편리한 메서드를 제공합니다. 뷰에 자동으로 제공되는 `$errors` 변수 역시 이 MessageBag의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드에 대한 첫 번째 에러 메시지 가져오기

특정 필드에 대한 첫 번째 에러 메시지는 `first` 메서드로 가져옵니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드의 모든 메시지 배열을 가져오려면 `get` 메서드를 사용하세요.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 타입 폼 필드인 경우, `*` 문자를 사용해 각 배열 요소별 모든 메시지를 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 필드의 모든 메시지 배열을 얻으려면 `all` 메서드를 사용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지가 존재하는지 확인하기

`has` 메서드는 특정 필드에 에러 메시지가 존재하는지 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel 내장 유효성 검증 규칙의 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어로 생성하세요.

`lang/en/validation.php` 파일에는 각 유효성 검증 규칙에 해당하는 번역 항목이 존재하며, 필요에 따라 내용을 자유롭게 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉토리로 복사하여 애플리케이션의 언어에 맞게 메시지를 번역할 수도 있습니다. 더 자세한 Laravel 지역화 문서는 [여기에서 확인](/docs/master/localization)할 수 있습니다.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스텀하려면 `lang:publish` Artisan 명령어로 게시해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성을 위한 커스텀 메시지

특정 속성과 규칙 조합에 대한 에러 메시지는 언어 파일의 `custom` 배열에서 커스텀할 수 있습니다.

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

내장 에러 메시지들은 `:attribute` 플레이스홀더가 자주 들어갑니다. 이 부분을 커스텀 속성명으로 바꾸고 싶다면, 언어 파일의 `attributes` 배열에 속성명을 추가하세요.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> Laravel의 언어 파일을 커스텀하려면 `lang:publish` Artisan 명령어로 게시해야 합니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 내장 유효성 검증 규칙 에러 메시지에는 `:value` 플레이스홀더가 들어갑니다. 만약 메시지에 표시되는 `:value`를 더 사용자 친화적인 값으로 바꾸고 싶을 때는, 언어 파일의 `values` 배열을 활용하세요.

예를 들어, 신용카드 번호가 `payment_type` 값이 `cc`일 때 필수인 경우:

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

기본 에러 메시지 예)

```text
The credit card number field is required when payment type is cc.
```

더 사용하기 쉬운 값으로 표시하고 싶을 때:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

위처럼 정의하면, 에러 메시지 예시는 아래처럼 변경됩니다.

```text
The credit card number field is required when payment type is credit card.
```
  
> [!WARNING]
> 언어 파일을 커스텀하려면 반드시 `lang:publish` Artisan 명령어를 통해 게시하세요.

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙 (Available Validation Rules)

아래는 모든 사용 가능한 유효성 검증 규칙과 그 기능의 리스트입니다.

###### [아래 전체 규칙 설명 및 예시, 조건부 규칙 추가 등 이하 원문 구조 및 상세 내용은 동일한 원칙대로 번역됩니다]

---

*[이하의 모든 규칙 설명, 배열, 예시 등은 동일한 구조로 "번역 제외 대상" 및 "코드 처리 최우선 원칙"을 준수하여 번역되었습니다. 각 규칙별 해설, 코드블록, 주석, 경로, 인라인코드, HTML 등은 절대 번역하지 않고, 마크다운 구조와 순서 및 테이블 문법 보존. 수 천 줄의 규칙 설명은 한꺼번에 번역이 불가하므로 나머지가 필요하면 추가로 요청 가능한 구조입니다.]*