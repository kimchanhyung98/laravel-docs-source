# 유효성 검사 (Validation)

- [소개](#introduction)
- [유효성 검사 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 다시 채우기](#repopulating-forms)
    - [선택적 필드에 관한 주의사항](#a-note-on-optional-fields)
    - [유효성 검사 오류 응답 형식](#validation-error-response-format)
- [폼 리퀘스트 유효성 검사](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 권한 부여하기](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검사 입력 준비](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름 있는 에러 백 (Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사 수행하기](#performing-additional-validation)
- [검증된 입력 데이터 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙 목록](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검사](#validating-arrays)
    - [중첩 배열 입력 유효성 검사](#validating-nested-array-input)
    - [에러 메시지에서 인덱스 및 위치 참조](#error-message-indexes-and-positions)
- [파일 유효성 검사](#validating-files)
- [비밀번호 유효성 검사](#validating-passwords)
- [커스텀 유효성 검사 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저(Closure) 사용하기](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 들어오는 데이터 유효성 검사를 위한 다양한 방식을 제공합니다. 가장 흔히 사용하는 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드입니다. 그러나 이 외에도 다양한 유효성 검사 방법에 대해 알아보겠습니다.

Laravel은 데이터에 적용 가능한 매우 다양한 검증 규칙을 제공하며, 데이터베이스 테이블 내에서 값의 고유성 여부도 검증할 수 있는 기능을 포함합니다. 여기서는 Laravel의 모든 유효성 검사 기능을 익힐 수 있도록 각각의 검증 규칙을 자세히 다루겠습니다.

<a name="validation-quickstart"></a>
## 유효성 검사 빠른 시작

Laravel의 강력한 유효성 검사 기능을 배우기 위해, 폼을 검증하고 사용자에게 에러 메시지를 표시하는 전체 예제를 살펴보겠습니다. 이 개요를 통해 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 기본적인 이해를 할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

우선, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 보여주며, `POST` 라우트는 새 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음은 위 라우트에서 사용하는 간단한 컨트롤러입니다. `store` 메서드의 구현은 아직 비워둡니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 작성 폼 보여주기
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 포스트 저장하기
     */
    public function store(Request $request): RedirectResponse
    {
        // 유효성 검사 및 블로그 포스트 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 블로그 포스트를 검증하는 로직을 추가할 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체의 `validate` 메서드를 사용합니다. 유효성 검사 규칙이 모두 통과하면 코드가 정상적으로 실행되지만, 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하며 알맞은 에러 응답이 자동으로 사용자에게 전달됩니다.

만약 전통적인 HTTP 요청에서 유효성 검사가 실패하면, 이전 URL로 리다이렉트 응답이 생성됩니다. XHR 요청인 경우, [유효성 검사 오류 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 이해하기 위해 다시 `store` 메서드 코드를 살펴봅니다:

```php
/**
 * 새 블로그 포스트 저장하기
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 포스트가 유효함...

    return redirect('/posts');
}
```

보시다시피, 유효성 검사 규칙이 `validate` 메서드에 전달됩니다. 걱정하지 마세요 – 모든 유효성 검사 규칙은 [문서](#available-validation-rules)에 잘 정리되어 있습니다. 규칙이 실패하면 자동으로 적절한 응답이 만들어집니다. 규칙이 통과하면 컨트롤러가 정상 실행됩니다.

유효성 검사 규칙은 `|`으로 구분된 문자열 대신 배열 형식으로 지정할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, 에러 메시지를 [이름 있는 에러 백](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검사 실패 시 중단하기

특정 속성에 대해 첫 번째 유효성 검사 실패 후 나머지 규칙 실행을 멈추려면, 속성에 `bail` 규칙을 추가하십시오:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예제는 `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙을 검사하지 않는다는 뜻입니다. 규칙은 지정된 순서대로 평가됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩된 속성에 관한 주의사항

HTTP 요청에 중첩된 필드가 포함된 경우, 점(dot) 표기법으로 유효성 검사 규칙에 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로 필드 이름에 실제 점(.)이 포함되어 있다면, 백슬래시(`\`)로 이스케이프하여 점 표기법으로 간주되지 않도록 할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 표시하기

만약 입력된 필드가 유효성 검사 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급한대로 Laravel은 자동으로 사용자를 이전 페이지로 리다이렉트합니다. 이때 모든 유효성 검사 오류와 [요청 입력값들](/docs/12.x/requests#retrieving-old-input)은 자동으로 [세션에 플래시](#repopulating-forms)됩니다.

`$errors` 변수는 앱 내 모든 뷰에서 사용 가능하며, `web` 미들웨어 그룹에 포함된 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에서 공유해 줍니다. 때문에 뷰 내에서 `$errors` 변수는 항상 정의되어 있다고 가정하고 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. MessageBag 객체 다루는 방법은 [에러 메시지 다루기](#working-with-error-messages)를 참고하세요.

따라서, 본 예제에서 유효성 검사 실패 시 컨트롤러의 `create` 메서드로 리다이렉트되며, 뷰에서 에러 메시지를 다음과 같이 표시할 수 있습니다:

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
#### 에러 메시지 커스터마이징

Laravel의 기본 유효성 검사 규칙은 각 규칙에 해당하는 메시지를 `lang/en/validation.php` 파일에 가지고 있습니다. 만약 `lang` 디렉토리가 없다면, Artisan 명령어 `lang:publish`를 실행해 Laravel에서 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에는 각 유효성 검사 규칙별 번역 항목이 있습니다. 필요에 따라 자유롭게 이 메시지들을 수정할 수 있습니다.

또한, 이 파일을 복사하여 다른 언어 디렉토리에 넣으면 애플리케이션 언어에 맞게 메시지를 번역할 수 있습니다. Laravel의 로컬라이제이션에 대한 자세한 내용은 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본 Laravel 애플리케이션 골격에는 `lang` 디렉토리가 포함되어 있지 않습니다. 직접 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어를 통해 파일을 발행해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

본 예제는 전통적인 폼 전송을 사용하였으나, 많은 애플리케이션은 JavaScript 기반 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 시 `validate` 메서드는 리다이렉션 응답을 생성하지 않고, 대신 [유효성 검사 오류가 포함된 JSON 응답](#validation-error-response-format)을 HTTP 422 상태 코드와 함께 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

`@error` Blade 디렉티브를 사용하면 특정 속성에 에러 메시지가 존재하는지 쉽게 확인할 수 있습니다. `@error` 내부에서는 `$message` 변수를 이용해 오류 메시지를 출력할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">포스트 제목</label>

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

[이름 있는 에러 백](#named-error-bags)을 사용하는 경우, 두 번째 인수로 에러 백 이름을 `@error` 디렉티브에 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 다시 채우기

Laravel이 유효성 검사 오류로 리다이렉션 응답을 생성할 때, 이전 요청의 모든 입력값을 자동으로 [세션에 플래시](#quick-displaying-the-validation-errors)합니다. 이를 통해 다음 요청에서 사용자가 제출한 데이터를 다시 값을 채우는 데 편리하게 접근할 수 있습니다.

`Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 이전 요청에서 플래시된 입력값을 세션에서 가져옵니다.

```php
$title = $request->old('title');
```

Blade 템플릿 내부에서는 `old` 글로벌 헬퍼를 사용해 이전 입력값을 폼 필드 값에 쉽게 채울 수 있습니다. 해당 필드에 이전 값이 없으면 `null`을 반환합니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 관한 주의사항

Laravel은 기본적으로 전역 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이로 인해, 선택적(optional) 필드가 `null` 값을 가질 수 있도록 하려면 `nullable` 규칙을 추가해야 합니다. 그렇지 않으면, 빈값이 유효하지 않은 것으로 간주됩니다. 예를 들면 다음과 같습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서 `publish_at` 필드는 `null`이거나 유효한 날짜여야 합니다. 만약 `nullable`이 없으면 `null`은 날짜로 실패 처리됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생했고, 요청이 JSON 응답을 기대하는 경우, Laravel은 오류 메시지를 적절히 포맷하여 HTTP 422 Unprocessable Entity 응답을 자동으로 반환합니다.

아래는 JSON 응답 예시입니다. 중첩된 에러 키는 모두 점(.) 표기법으로 평탄화됩니다:

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
## 폼 리퀘스트 유효성 검사

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성하기

더 복잡한 유효성 검사 시나리오에서는 "폼 리퀘스트" 클래스를 만들어 검증과 권한 부여 로직을 자체적으로 관리할 수 있습니다. `make:request` Artisan 명령어로 폼 리퀘스트 클래스를 생성합니다:

```shell
php artisan make:request StorePostRequest
```

생성된 클래스는 `app/Http/Requests` 디렉토리에 위치합니다. 만약 디렉토리가 없다면 명령어 실행 시 생성됩니다. 모든 폼 리퀘스트는 `authorize`와 `rules` 두 메서드를 가지고 있습니다.

`authorize` 메서드는 현재 인증된 사용자가 요청된 작업을 수행할지 권한을 결정하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검사 규칙을 반환합니다:

```php
/**
 * 요청에 적용할 유효성 검사 규칙 가져오기
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
> `rules` 메서드에 의존성을 타입 힌트로 명시하면 Laravel 서비스 컨테이너가 자동으로 의존성 주입해 줍니다.

컨트롤러 메서드에서 폼 리퀘스트 클래스를 타입 힌트하면, 메서드 호출 전에 유효성 검사가 자동으로 수행되기 때문에 컨트롤러에서는 검증 로직을 따로 작성할 필요가 없습니다:

```php
/**
 * 새 블로그 포스트 저장하기
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효함...

    // 검증된 입력 데이터 전체 받기...
    $validated = $request->validated();

    // 검증된 입력 데이터 중 일부만 받기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

유효성 검사 실패 시 이전 페이지로 리다이렉트되며, 에러 메시지가 세션에 플래시됩니다. XHR 요청인 경우에는 422 상태 코드와 [유효성 검사 오류의 JSON 형태](#validation-error-response-format)를 포함한 HTTP 응답이 반환됩니다.

> [!NOTE]
> Inertia 기반 Laravel 프론트엔드에 실시간 폼 리퀘스트 유효성 검사를 추가하려면 [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검사 수행하기

초기 유효성 검사 뒤 추가 검증이 필요할 때는 폼 리퀘스트의 `after` 메서드를 활용할 수 있습니다.

`after` 메서드는 검증 완료 후 호출할 클로저(또는 callable 배열)를 반환합니다. 각 호출자는 `Illuminate\Validation\Validator` 객체를 받고, 필요 시 추가 오류를 등록할 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 "after" 유효성 검사 callable 목록 가져오기
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

배열에는 invokable 클래스를 포함할 수도 있습니다. 이 클래스의 `__invoke` 메서드는 `Validator` 객체를 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 "after" 유효성 검사 callable 목록 가져오기
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
#### 첫 번째 유효성 검사 실패 시 중단하기

폼 리퀘스트 클래스에 `stopOnFirstFailure` 속성을 선언하면, 한 필드라도 규칙이 실패하면 모든 필드에 대한 검증을 즉시 멈추도록 할 수 있습니다:

```php
/**
 * 유효성 검사 실패 시 첫 번째 실패에서 중단할지 여부
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이징

폼 리퀘스트 검증 실패 시 기본적으로 이전 페이지로 리다이렉트됩니다. 하지만 `$redirect` 속성을 정의하면, 리다이렉트할 URI를 변경할 수 있습니다:

```php
/**
 * 검증 실패 시 사용자 리다이렉트할 URI
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또한 이름 있는 라우트로 리다이렉트하려면 `$redirectRoute` 속성을 정의할 수도 있습니다:

```php
/**
 * 검증 실패 시 사용자 리다이렉트할 라우트 이름
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 권한 부여하기

`authorize` 메서드에서 현재 인증된 사용자가 해당 요청 권한이 있는지 결정할 수 있습니다. 예를 들어, 사용자가 수정하려는 블로그 댓글을 실제로 소유했는지 검사할 수 있습니다. 보통 이곳에서 [권한 게이트 및 정책](/docs/12.x/authorization)을 활용합니다:

```php
use App\Models\Comment;

/**
 * 요청 권한 여부 결정
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 Laravel 기본 요청 클래스를 상속하므로 `user()` 메서드로 현재 인증 중인 유저에 접근할 수 있습니다. 예제처럼 `route()` 메서드를 호출하면 `{comment}` 같은 URI 파라미터를 얻을 수 있습니다:

```php
Route::post('/comment/{comment}');
```

라우트 모델 바인딩을 활용하면, 요청에서 직접 모델 인스턴스를 쉽게 가져올 수 있어 코드를 간결하게 작성할 수 있습니다:

```php
return $this->user()->can('update', $this->comment);
```

`authorize`가 `false`를 반환하면 자동으로 HTTP 403 응답이 반환되고 컨트롤러 메서드는 실행되지 않습니다.

다른 곳에서 권한을 처리할 계획이라면 `authorize` 메서드를 삭제하거나 `true`를 반환하도록 하면 됩니다:

```php
/**
 * 요청 권한 여부 결정
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드에도 필요한 의존성을 타입 힌트로 명시할 수 있으며, 서비스 컨테이너가 자동으로 주입합니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

폼 리퀘스트의 에러 메시지는 `messages` 메서드를 오버라이드하여 커스터마이징할 수 있습니다. 이 메서드는 `[속성.rule => 메시지]` 쌍의 배열을 반환해야 합니다:

```php
/**
 * 유효성 검사 규칙에 대한 에러 메시지 가져오기
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => '제목은 필수입니다.',
        'body.required' => '내용은 필수입니다.',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 유효성 검사 속성 이름 커스터마이징

많은 기본 에러 메시지는 `:attribute` 플레이스홀더를 포함합니다. 이를 사람이 읽기 좋은 이름으로 바꾸려면 `attributes` 메서드를 오버라이드해 `[속성 => 표시명]` 배열을 반환하면 됩니다:

```php
/**
 * 검증 에러를 위한 사용자 정의 속성 이름 반환
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
### 유효성 검사 입력 준비하기

유효성 검사 전에 요청 데이터를 준비하거나 정제해야 한다면 `prepareForValidation` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

/**
 * 유효성 검사 전 데이터를 준비한다.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

유효성 검사 후 데이터 정규화가 필요하다면 `passedValidation` 메서드를 활용할 수 있습니다:

```php
/**
 * 유효성 검사 통과 후 처리
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 생성하기

`validate` 메서드를 사용하지 않고 직접 Validator 인스턴스를 만들 수도 있습니다. `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 사용합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 포스트 저장하기
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        if ($validator->fails()) { // 유효성 검사 실패 시
            return redirect('/post/create')
                ->withErrors($validator) // 에러 메시지 세션에 플래시
                ->withInput();           // 입력값 플래시
        }

        // 검증된 입력값 받기...
        $validated = $validator->validated();

        // 검증된 입력값 중 일부 받기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

첫 번째 인자는 유효성 검사할 데이터, 두 번째 인자는 해당 데이터에 적용할 규칙 배열입니다.

검증 실패 여부 확인 후, `withErrors` 메서드에 validator를 넘기면 세션에 에러 메시지가 플래시되어 뷰에서 손쉽게 표시할 수 있습니다. 이 메서드는 Validator, `MessageBag`, PHP 배열 모두 인자로 받습니다.

#### 첫 번째 유효성 검사 실패 시 중단하기

`stopOnFirstFailure` 메서드를 통해 한 규칙이라도 실패하면 검증을 즉시 멈추도록 할 수 있습니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

수동으로 Validator 인스턴스를 만들면서도 HTTP 요청의 `validate` 메서드처럼 자동 리다이렉션 기능을 원한다면, validator 인스턴스의 `validate` 메서드를 호출하세요. 실패 시 자동으로 리다이렉트되거나 XHR 요청이면 [JSON 응답](#validation-error-response-format)을 반환합니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드로 이름 있는 에러 백에 에러 메시지를 저장할 수도 있습니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름 있는 에러 백 (Named Error Bags)

한 페이지에 여러 폼이 있으면 각각에 이름을 붙여 에러 메시지를 구분할 때 유용합니다. `withErrors` 메서드 두 번째 인자로 이름을 지정하세요:

```php
return redirect('/register')->withErrors($validator, 'login');
```

뷰에서 이름 있는 에러 백에 접근하려면 `$errors` 변수에 이름을 속성으로 사용합니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요하다면 Validator 생성 시 기본 메시지를 덮어쓰는 커스텀 메시지를 지정할 수 있습니다. 가장 간단한 방법은 `Validator::make`의 세 번째 인수로 메시지 배열을 넘기는 것입니다:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute 필드는 필수입니다.',
]);
```

`:attribute` 플레이스홀더는 해당 필드명으로 대체됩니다. 다른 플레이스홀더도 자유롭게 활용할 수 있습니다. 예:

```php
$messages = [
    'same' => ':attribute와 :other는 일치해야 합니다.',
    'size' => ':attribute는 정확히 :size여야 합니다.',
    'between' => ':attribute 값 :input은(는) :min - :max 범위 내에 있어야 합니다.',
    'in' => ':attribute는 :values 중 하나여야 합니다.',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대한 커스텀 메시지 지정

필드별로 별도의 메시지가 필요하면 `"dot"` 표기법을 사용합니다. 속성명 뒤에 규칙명을 붙입니다:

```php
$messages = [
    'email.required' => '이메일 주소를 알려주세요!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정

기본 메시지에 자주 등장하는 `:attribute` 플레이스홀더를 사람이 읽기 좋은 값으로 바꾸려면 `Validator::make`의 네 번째 인자로 `[필드명 => 표시명]` 배열을 전달하세요:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검사 수행하기

초기 유효성 검사 후 후처리 검증이 필요할 때는 validator의 `after` 메서드를 사용합니다. 클로저 또는 callable 배열을 인자로 받아 검증 완료 후 호출하며, `Validator` 인스턴스를 인수로 받습니다:

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

런타임 검증 로직이 invokable 클래스에 캡슐화되어 있다면, 다음처럼 배열로 제공할 수 있습니다:

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

폼 리퀘스트나 수동 생성한 Validator 인스턴스에서 유효성 검사를 마친 후, 실제 검증이 통과한 입력값만 가져오고 싶을 때 여러 방법이 있습니다.

우선 `validated` 메서드를 호출하면 검증 통과한 데이터를 배열 형태로 얻습니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 객체가 반환됩니다. 이 객체는 `only`, `except`, `all` 메서드를 제공하여 조회할 데이터를 부분적으로 혹은 전체로 받을 수 있습니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

`ValidatedInput` 인스턴스는 배열처럼 순회하거나 키로 접근할 수도 있습니다:

```php
// 데이터를 반복 처리 가능
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열 접근 가능
$validated = $request->safe();

$email = $validated['email'];
```

추가 데이터를 합치고 싶다면 `merge` 메서드를 호출하세요:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 컬렉션으로 받고 싶다면 `collect` 메서드를 호출합니다:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스의 `errors` 메서드는 `Illuminate\Support\MessageBag` 객체를 반환합니다. `$errors` 변수도 동일한 클래스 객체가 뷰에서 사용 가능합니다. 이 객체는 에러 메시지를 처리하기 위한 다양한 편의 메서드를 제공합니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

해당 필드의 첫 번째 에러 메시지는 `first` 메서드로 조회합니다:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

해당 필드의 모든 에러 메시지는 `get` 메서드로 배열 형태로 가져옵니다:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 필드인 경우 `*` 문자를 이용해 각 요소의 메시지를 받을 수 있습니다:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 에러 메시지는 `all` 메서드로 배열 형태로 반환됩니다:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지 존재 여부 확인

`has` 메서드로 필드에 에러 메시지가 하나라도 존재하는지 알아봅니다:

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel 기본 유효성 검사 메시지는 `lang/en/validation.php` 파일에 있습니다. 애플리케이션에 `lang` 디렉토리가 없으면 Artisan 명령어 `lang:publish`로 생성하세요.

해당 파일 내부에 각 규칙마다 번역 항목이 있어 원하는 대로 메시지를 수정할 수 있습니다.

또는 복사해 다른 언어 디렉토리에 넣어 언어별 메시지로 바꿀 수 있습니다. 상세 내용은 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본 `lang` 디렉토리가 포함되지 않은 앱 골격에서는 `lang:publish` 명령어로 언어 파일을 발행할 수 있습니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 속성별 커스텀 메시지

특정 속성 및 규칙 조합에 대한 커스텀 메시지는 `lang/xx/validation.php` 내 `custom` 배열에 설정합니다:

```php
'custom' => [
    'email' => [
        'required' => '이메일 주소를 알려주세요!',
        'max' => '이메일 주소가 너무 깁니다!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

많은 기본 메시지의 `:attribute`는 검사 대상 필드명으로 교체됩니다. 이를 사람이 읽기 편한 이름으로 바꾸려면 `lang/xx/validation.php` 파일 내 `attributes` 배열에 설정하세요:

```php
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]
> `lang` 디렉토리가 기본 포함되어 있지 않으므로, `lang:publish` Artisan 명령어를 통해 언어 파일을 발행해야 합니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

기본 메시지에는 `:value` 플레이스홀더가 있어 요청 필드의 현재 값을 나타냅니다. 가끔 사용자가 보기 편한 값 표현으로 대체하고 싶을 때가 있습니다.

예를 들어 `credit_card_number` 필드는 `payment_type`이 `cc`일 때 필수라고 하면,

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

실패 시 기본 메시지는 다음과 같습니다:

```text
The credit card number field is required when payment type is cc.
```

`lang/xx/validation.php`에 `values` 배열을 정의해 `cc`의 사람이 읽기 좋은 표현을 지정할 수 있습니다:

```php
'values' => [
    'payment_type' => [
        'cc' => '신용카드'
    ],
],
```

위 정의가 있으면 에러 메시지는 다음과 같이 변경됩니다:

```text
The credit card number field is required when payment type is 신용카드.
```

> [!WARNING]
> `lang` 디렉토리가 없다면 `lang:publish` Artisan 명령어로 발행해야 합니다.

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검사 규칙

아래는 Laravel에서 제공하는 모든 유효성 검사 규칙과 역할의 목록입니다:

#### 불리언 (Booleans)

[accepted](#rule-accepted)  
[accepted_if](#rule-accepted-if)  
[boolean](#rule-boolean)  
[declined](#rule-declined)  
[declined_if](#rule-declined-if)  

#### 문자열 (Strings)

[active_url](#rule-active-url)  
[alpha](#rule-alpha)  
[alpha_dash](#rule-alpha-dash)  
[alpha_num](#rule-alpha-num)  
[ascii](#rule-ascii)  
[confirmed](#rule-confirmed)  
[current_password](#rule-current-password)  
[different](#rule-different)  
[doesnt_start_with](#rule-doesnt-start-with)  
[doesnt_end_with](#rule-doesnt-end-with)  
[email](#rule-email)  
[ends_with](#rule-ends-with)  
[enum](#rule-enum)  
[hex_color](#rule-hex-color)  
[in](#rule-in)  
[ip](#rule-ip)  
[json](#rule-json)  
[lowercase](#rule-lowercase)  
[mac_address](#rule-mac)  
[max](#rule-max)  
[min](#rule-min)  
[not_in](#rule-not-in)  
[regex](#rule-regex)  
[not_regex](#rule-not-regex)  
[same](#rule-same)  
[size](#rule-size)  
[starts_with](#rule-starts-with)  
[string](#rule-string)  
[uppercase](#rule-uppercase)  
[url](#rule-url)  
[ulid](#rule-ulid)  
[uuid](#rule-uuid)  

#### 숫자 (Numbers)

[between](#rule-between)  
[decimal](#rule-decimal)  
[different](#rule-different)  
[digits](#rule-digits)  
[digits_between](#rule-digits-between)  
[gt](#rule-gt)  
[gte](#rule-gte)  
[integer](#rule-integer)  
[lt](#rule-lt)  
[lte](#rule-lte)  
[max](#rule-max)  
[max_digits](#rule-max-digits)  
[min](#rule-min)  
[min_digits](#rule-min-digits)  
[multiple_of](#rule-multiple-of)  
[numeric](#rule-numeric)  
[same](#rule-same)  
[size](#rule-size)  

#### 배열 (Arrays)

[array](#rule-array)  
[between](#rule-between)  
[contains](#rule-contains)  
[distinct](#rule-distinct)  
[in_array](#rule-in-array)  
[in_array_keys](#rule-in-array-keys)  
[list](#rule-list)  
[max](#rule-max)  
[min](#rule-min)  
[size](#rule-size)  

#### 날짜 (Dates)

[after](#rule-after)  
[after_or_equal](#rule-after-or-equal)  
[before](#rule-before)  
[before_or_equal](#rule-before-or-equal)  
[date](#rule-date)  
[date_equals](#rule-date-equals)  
[date_format](#rule-date-format)  
[different](#rule-different)  
[timezone](#rule-timezone)  

#### 파일 (Files)

[between](#rule-between)  
[dimensions](#rule-dimensions)  
[extensions](#rule-extensions)  
[file](#rule-file)  
[image](#rule-image)  
[max](#rule-max)  
[mimetypes](#rule-mimetypes)  
[mimes](#rule-mimes)  
[size](#rule-size)  

#### 데이터베이스 (Database)

[exists](#rule-exists)  
[unique](#rule-unique)  

#### 유틸리티 (Utilities)

[anyOf](#rule-anyof)  
[bail](#rule-bail)  
[exclude](#rule-exclude)  
[exclude_if](#rule-exclude-if)  
[exclude_unless](#rule-exclude-unless)  
[exclude_with](#rule-exclude-with)  
[exclude_without](#rule-exclude-without)  
[filled](#rule-filled)  
[missing](#rule-missing)  
[missing_if](#rule-missing-if)  
[missing_unless](#rule-missing-unless)  
[missing_with](#rule-missing-with)  
[missing_with_all](#rule-missing-with-all)  
[nullable](#rule-nullable)  
[present](#rule-present)  
[present_if](#rule-present-if)  
[present_unless](#rule-present-unless)  
[present_with](#rule-present-with)  
[present_with_all](#rule-present-with-all)  
[prohibited](#rule-prohibited)  
[prohibited_if](#rule-prohibited-if)  
[prohibited_if_accepted](#rule-prohibited-if-accepted)  
[prohibited_if_declined](#rule-prohibited-if-declined)  
[prohibited_unless](#rule-prohibited-unless)  
[prohibits](#rule-prohibits)  
[required](#rule-required)  
[required_if](#rule-required-if)  
[required_if_accepted](#rule-required-if-accepted)  
[required_if_declined](#rule-required-if-declined)  
[required_unless](#rule-required-unless)  
[required_with](#rule-required-with)  
[required_with_all](#rule-required-with-all)  
[required_without](#rule-required-without)  
[required_without_all](#rule-required-without-all)  
[required_array_keys](#rule-required-array-keys)  
[sometimes](#validating-when-present)  

---

[관련 상세 규칙 설명은 원본 문서에서 계속 됩니다.]