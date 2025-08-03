# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작 (Validation Quickstart)](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 복원하기](#repopulating-forms)
    - [선택적 필드에 관한 참고사항](#a-note-on-optional-fields)
    - [유효성 검사 오류 응답 포맷](#validation-error-response-format)
- [폼 요청 유효성 검증 (Form Request Validation)](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 권한 부여](#authorizing-form-requests)
    - [오류 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검사 전 입력 준비하기](#preparing-input-for-validation)
- [수동으로 유효성 검사기 생성하기 (Manually Creating Validators)](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [명명된 오류 가방](#named-error-bags)
    - [오류 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사 수행하기](#performing-additional-validation)
- [검증된 입력 데이터를 활용하기](#working-with-validated-input)
- [오류 메시지 작업하기](#working-with-error-messages)
    - [언어 파일에서 사용자 지정 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 규칙들](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 검증하기](#validating-arrays)
    - [중첩된 배열 입력 검증하기](#validating-nested-array-input)
    - [오류 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 검증하기](#validating-files)
- [비밀번호 검증하기](#validating-passwords)
- [사용자 정의 유효성 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에 들어오는 데이터를 검증하는 여러 방법을 제공합니다. 가장 흔히 사용하는 방법은 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드입니다. 하지만 다른 유효성 검증 방식도 다루겠습니다.

Laravel은 데이터에 적용할 수 있는 다양한 편리한 유효성 규칙을 제공하며, 특정 데이터베이스 테이블에서 값의 고유성을 검증할 수도 있습니다. 여기서는 Laravel의 모든 유효성 검증 기능에 익숙해질 수 있도록 각 규칙을 상세히 다루겠습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 배우기 위해, 먼저 폼을 검증하고 사용자에게 오류 메시지를 보여주는 완전한 예제를 살펴보겠습니다. 이 개요를 따라가면서 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 전반을 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트를 정의했다고 가정해 봅시다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새로운 블로그 게시물을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위 라우트에 대응하는 단순 컨트롤러를 살펴봅시다. 일단 `store` 메서드는 비워둡니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물 작성 폼을 보여준다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 게시물을 저장한다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 게시물 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 게시물을 검증하는 로직을 채워봅시다. `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 규칙이 통과하면 코드가 정상 실행되지만, 실패하면 `Illuminate\Validation\ValidationException` 예외가 자동 발생하며 적절한 오류 응답이 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 검증 실패 시 이전 URL로 리다이렉트됩니다. 만약 XHR 요청이면, [유효성 검사 오류 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 이해하기 위해 `store` 메서드를 다시 확인해 봅시다:

```php
/**
 * 새 블로그 게시물을 저장한다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 게시물이 유효함...

    return redirect('/posts');
}
```

보시다시피, 유효성 규칙이 `validate` 메서드에 전달됩니다. 걱정 마세요 — 사용 가능한 모든 유효성 규칙은 [기술 문서](#available-validation-rules)에 정리되어 있습니다. 규칙 검증에 실패하면 적절한 응답이 자동 생성되며, 성공 시 컨트롤러는 계속 실행됩니다.

또는, 규칙을 단일 문자열(`|` 구분자) 대신 배열 형태로도 나타낼 수 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

그리고 `validateWithBag` 메서드를 사용해 요청을 검증하고, 검증 오류 메시지를 [명명된 오류 가방](#named-error-bags)에 저장할 수도 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 최초 실패 시 검증 중지하기

가끔 특정 속성에서 첫 번째 유효성 검사 실패 시 즉시 중단하고 싶을 때가 있습니다. 이때는 해당 속성에 `bail` 규칙을 할당하세요:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예제에서 만약 `title` 속성의 `unique` 규칙이 실패하면, `max` 규칙은 더 이상 검사하지 않습니다. 규칙은 지정한 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 관한 참고사항

들어오는 HTTP 요청에 "중첩"된 필드 데이터가 있다면, 유효성 검사 규칙 내에서 점(`.`) 표기법으로 필드를 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드 이름이 실제 점 문자를 포함할 경우 점 문자가 표현법으로 해석되지 않도록 역슬래시(`\`)로 이스케이프할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 오류 표시하기

그렇다면, 요청 필드들이 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 말씀드렸듯이, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 뿐만 아니라, 모든 유효성 오류와 [요청 입력값](/docs/master/requests#retrieving-old-input)을 자동으로 세션에 [플래시 저장](/docs/master/session#flash-data)합니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 모든 뷰에 `$errors` 변수를 공유하는데, 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있습니다. 이 미들웨어가 적용되면 `$errors` 변수는 항상 뷰에서 사용할 수 있으며, 안전하게 사용 가능하므로 예외 처리를 걱정하지 않아도 됩니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 클래스의 인스턴스입니다. 이 객체와 작업하는 방법은 [오류 메시지 작업하기](#working-with-error-messages) 부분에서 더 자세히 알아볼 수 있습니다.

따라서, 위 예제에서 유효성 검증 실패 시 사용자는 컨트롤러의 `create` 메서드가 보여주는 페이지로 리다이렉트되며, 오류 메시지들을 뷰에 출력할 수 있습니다:

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
#### 오류 메시지 커스터마이징

Laravel 내장 유효성 검사 규칙마다 오류 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 Laravel에게 생성하라고 지시할 수 있습니다.

`lang/en/validation.php` 파일 내에서 각 유효성 규칙에 대한 번역 항목을 찾을 수 있으며, 필요에 따라 이 메시지들을 변경하거나 수정할 수 있습니다.

뿐만 아니라, 해당 파일을 다른 언어 디렉터리로 복사하여 애플리케이션의 언어별로 메시지를 번역할 수도 있습니다. 자세한 내용은 [로컬라이제이션 문서](/docs/master/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 템플릿에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이징하고 싶다면 `lang:publish` Artisan 명령어로 파일을 게시하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검사

이 예에서는 전통적인 폼을 통해 데이터를 전달했지만, 많은 애플리케이션은 자바스크립트 기반 프론트엔드에서 XHR 요청을 보냅니다. XHR 요청 중에 `validate` 메서드를 사용하면 Laravel은 리다이렉션 응답을 생성하지 않고, 대신 [모든 유효성 검사 오류를 담은 JSON 응답](#validation-error-response-format)을 생성하여 422 HTTP 상태 코드와 함께 전송합니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

Blade 템플릿에서 `@error` 디렉티브를 사용하면 특정 속성에 대한 유효성 오류 메시지 존재 여부를 빠르게 확인할 수 있습니다. 이 디렉티브 내부에서 `$message` 변수를 출력하여 오류 메시지를 보여줄 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">게시물 제목</label>

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

명명된 오류 가방을 사용 중이라면, `@error` 디렉티브의 두 번째 인자로 오류 가방 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 복원하기

Laravel이 유효성 검사 실패로 리다이렉트를 생성할 때, 다음 요청에서 쉽게 접근하고 사용자가 제출한 폼을 다시 채울 수 있도록 프레임워크가 자동으로 [요청 입력을 세션에 플래시 저장](/docs/master/session#flash-data)합니다.

이전 요청의 플래시된 입력값을 받으려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하세요. `old` 메서드는 이전에 플래시된 세션 데이터를 가져옵니다:

```php
$title = $request->old('title');
```

또한 Blade 템플릿에서는 전역 `old` 헬퍼를 제공하여 더욱 편리하게 폼을 복원할 수 있습니다. 해당 필드에 이전 입력값이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 관한 참고사항

Laravel은 기본적으로 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 때문에, 요청 필드가 "선택적"일 경우에 `nullable` 규칙을 명시적으로 넣어줘야 `null` 값이 유효성 검사에서 무시됩니다. 예:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예에서는 `publish_at` 필드가 `null`이거나 유효한 날짜여야 함을 의미합니다. 만약 `nullable` 규칙을 넣지 않으면, `null` 값이 유효하지 않은 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 오류 응답 포맷

`Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대할 경우, Laravel은 오류 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

다음은 유효성 오류에 대한 JSON 응답 포맷 예제입니다. 중첩된 오류 키는 점(`.`) 표기법으로 평탄화됩니다:

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
### 폼 요청 생성하기

복잡한 유효성 검사 상황에서는 "폼 요청" 클래스를 만들어 검증과 권한 로직을 별도로 캡슐화할 수 있습니다. 폼 요청 클래스는 `make:request` Artisan CLI 명령어를 사용해 생성합니다:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 해당 디렉터리가 없으면 명령어 실행 시 생성됩니다. 모든 폼 요청 클래스는 `authorize` 메서드와 `rules` 메서드 두 가지를 가집니다.

`authorize` 메서드는 현재 인증된 사용자가 요청이 나타내는 작업을 수행할 권한이 있는지 결정하고, `rules` 메서드는 요청 데이터에 적용할 유효성 규칙을 반환합니다:

```php
/**
 * 요청에 적용할 유효성 규칙을 반환한다.
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
> `rules` 메서드 시그니처에 필요한 의존성은 타입힌팅하면 Laravel [서비스 컨테이너](/docs/master/container)로 자동 해결됩니다.

검증 규칙은 컨트롤러 메서드에서 폼 요청 클래스를 타입힌팅 하면 실행됩니다. 요청이 유효성 검증되기 때문에 컨트롤러에 검증 로직을 넣지 않아도 됩니다:

```php
/**
 * 새 블로그 게시물 저장.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효함...

    // 검증된 입력값 전체 가져오기...
    $validated = $request->validated();

    // 검증된 입력값의 일부만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 게시물 저장...

    return redirect('/posts');
}
```

검증 실패 시 이전 위치로 리다이렉트되며 오류 메시지가 세션에 플래시됩니다. XHR 요청이면 422 상태 코드와 함께 [JSON 방식 오류 메시지](#validation-error-response-format)를 반환합니다.

> [!NOTE]
> Inertia 기반 Laravel 프론트엔드에 실시간 폼 요청 검증을 추가하려면 [Laravel Precognition](/docs/master/precognition)를 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검사 수행하기

초기 유효성 검사 후 추가 검증이 필요한 경우, 폼 요청의 `after` 메서드를 활용할 수 있습니다.

`after` 메서드는 클로저 또는 호출 가능한 배열을 반환해야 하며, 이들은 검증 완료 후 호출됩니다. 각 호출 가능 객체는 `Illuminate\Validation\Validator` 인스턴스를 인자로 받아, 추가 오류 메시지를 추가할 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 유효성 검사 호출자들을 반환한다.
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

`after` 메서드가 반환하는 배열에는 호출 가능한 클래스도 포함할 수 있으며, 이 클래스의 `__invoke` 메서드가 `Validator` 인스턴스를 인자로 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 유효성 검사 호출자들을 반환한다.
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
#### 최초 검증 실패 시 중지하기

폼 요청 클래스에 `stopOnFirstFailure` 프로퍼티를 추가해, 단일 검증 실패 발생 시 모든 속성에 대한 검사를 중단하도록 지시할 수 있습니다:

```php
/**
 * 검증 실패 시 첫 번째 규칙 실패에서 중지할지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이징

폼 요청 유효성 검증 실패 시 사용자를 이전 위치로 돌려보내는 리다이렉트 동작을 커스터마이징하고 싶다면, 폼 요청 클래스에 `$redirect` 프로퍼티를 정의하세요:

```php
/**
 * 검증 실패 시 리다이렉트할 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는 이름 있는 라우트로 리다이렉트하려면 `$redirectRoute` 프로퍼티를 사용할 수 있습니다:

```php
/**
 * 검증 실패 시 리다이렉트할 라우트 이름.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 권한 부여

폼 요청 클래스는 `authorize` 메서드도 포함합니다. 이 메서드에서 인증된 사용자가 특정 리소스를 수정할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 수정하려는 블로그 댓글의 소유자인지 검증할 수 있죠. 보통 이 메서드에서는 [인가 게이트 및 정책](/docs/master/authorization)을 호출합니다:

```php
use App\Models\Comment;

/**
 * 사용자가 이 요청을 수행할 권한이 있는지 판단한다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 요청은 기본 Laravel 요청 클래스를 상속하므로 `user` 메서드로 현재 인증된 사용자에 접근할 수 있습니다. 예제에서 `route` 메서드는 호출된 라우트의 URI 파라미터(예: `{comment}`) 값에 접근할 수 있게 해줍니다:

```php
Route::post('/comment/{comment}');
```

라우트 모델 바인딩을 활용한다면, 요청 객체의 속성으로 이미 조회된 모델에 더 간결하게 접근할 수 있습니다:

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면 403 HTTP 응답이 자동 전송되고 컨트롤러 메서드는 실행되지 않습니다.

다른 곳에서 인가 로직을 처리할 계획이라면, `authorize` 메서드를 완전히 제거하거나 단순히 `true`를 반환하도록 해도 됩니다:

```php
/**
 * 사용자가 이 요청을 수행할 권한이 있는지 판단한다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드에도 필요한 의존성을 타입힌트하면 Laravel [서비스 컨테이너](/docs/master/container)로 자동 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이징

폼 요청 클래스에서 `messages` 메서드를 오버라이드하여 사용하는 오류 메시지를 커스터마이징할 수 있습니다. 반환 값은 속성-규칙 쌍과 메시지 배열입니다:

```php
/**
 * 정의된 유효성 검사 규칙에 대한 오류 메시지를 반환한다.
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

내장 오류 메시지에는 `:attribute` 플레이스홀더가 포함됩니다. 이를 커스텀 이름으로 바꾸려면 `attributes` 메서드를 오버라이드하여 속성-이름 쌍 배열을 반환하세요:

```php
/**
 * 유효성 검사 오류에 대한 사용자 정의 속성 이름을 반환한다.
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
### 유효성 검사 전 입력 준비하기

유효성 규칙 적용 전 요청 데이터 전처리나 정제가 필요하다면 `prepareForValidation` 메서드를 사용할 수 있습니다:

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

검증 완료 후 데이터를 정규화해야 할 경우 `passedValidation` 메서드를 활용하세요:

```php
/**
 * 성공적인 유효성 검사 완료 후 처리.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 유효성 검사기 생성하기 (Manually Creating Validators)

요청에서 `validate` 메서드를 사용하지 않고 직접 유효성 검사기 인스턴스를 생성하려면 `Validator` [파사드](/docs/master/facades)를 활용하면 됩니다. 파사드의 `make` 메서드는 새 유효성 검사기 객체를 생성합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물 저장.
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

        // 검증된 입력값의 일부만 가져오기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 게시물 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드에 첫 번째 인자는 검증할 데이터, 두 번째 인자는 데이터에 적용할 유효성 규칙 배열입니다.

검증 실패 여부 판별 후, `withErrors` 메서드를 사용해 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 리다이렉트 후 `$errors` 변수가 자동으로 뷰에 공유되어 쉽게 오류를 표시할 수 있습니다. `withErrors`는 Validator, `MessageBag`, 또는 PHP 배열 모두를 인자로 받습니다.

#### 최초 실패 시 검증 중지

`stopOnFirstFailure` 메서드를 호출해 단일 검증 오류 발생 시 모든 유효성 검사를 중단시킬 수 있습니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

검증기를 직접 생성해도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 활용하고 싶다면, 생성된 검증기 인스턴스에서 `validate` 메서드를 호출하세요. 유효성 실패 시 자동으로 리다이렉트되거나 XHR 요청이라면 [JSON 응답](#validation-error-response-format)을 반환합니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드로 명명된 오류 가방에 오류 메시지를 저장할 수도 있습니다:

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 명명된 오류 가방

한 페이지에 여러 폼이 있다면 각 폼별로 오류 메시지를 분리해서 관리하고 싶을 수 있습니다. `withErrors` 메서드의 두 번째 인자로 오류 가방의 이름을 지정하세요:

```php
return redirect('/register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수 내 해당 이름으로 된 오류 가방 인스턴스를 참조할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 커스터마이징

필요에 따라 기본 Laravel 오류 메시지 대신 사용할 커스텀 오류 메시지를 지정할 수 있습니다. 몇 가지 지정 방법이 있습니다.

우선 `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지 배열을 전달할 수 있습니다:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위 예의 `:attribute` 플레이스홀더는 검증 대상 필드 이름으로 바뀝니다. 그 외 기타 플레이스홀더도 사용할 수 있습니다. 예:

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

특정 규칙의 커스텀 메시지를 특정 속성에만 적용하려면 점 표기법으로 속성명과 규칙을 함께 지정하세요:

```php
$messages = [
    'email.required' => '이메일 주소는 필수입니다!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성 값 지정

`Validator::make`의 네 번째 인자로 속성 번역 배열을 넘기면, 오류 메시지 내 `:attribute` 플레이스홀더가 해당 이름으로 대체됩니다:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검사 수행하기

초기 검증 뒤 무엇인가 추가 검사를 해야 할 수도 있습니다. 이럴 땐 검증기의 `after` 메서드를 사용하세요. `after`는 클로저 또는 호출 가능한 배열을 인자로 받아 검증 완료 후 호출합니다. 인자로는 `Illuminate\Validation\Validator` 인스턴스가 전달되어 추가 오류를 넣을 수 있습니다:

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

`after`는 호출 가능한 배열도 받으며, 복잡한 "검증 후" 로직을 호출 가능한 클래스로 캡슐화한 경우 매우 유용합니다. 해당 클래스는 `__invoke` 메서드에서 `Validator` 인스턴스를 받습니다:

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
## 검증된 입력 데이터를 활용하기

폼 요청이나 수동 생성한 유효성 검사기의 검증을 거친 후, 실제 검증된 입력 데이터를 가져오려면 여러 방법이 있습니다. 먼저, 폼 요청이나 유효성 검사기 인스턴스의 `validated` 메서드를 호출하면 검증된 데이터 배열을 반환합니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출하면 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하는데, 이 객체는 `only`, `except`, `all` 메서드를 제공하여 검증 데이터의 일부 또는 전부를 가져올 수 있습니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

더불어 `ValidatedInput` 인스턴스는 `foreach` 반복문으로 순회할 수 있고 배열처럼 접근할 수도 있습니다:

```php
// 검증된 데이터 반복 처리하기...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 데이터 접근하기...
$validated = $request->safe();

$email = $validated['email'];
```

검증 데이터에 필드를 추가하려면 `merge` 메서드를 호출할 수 있습니다:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/master/collections) 형태로 가져오려면 `collect` 메서드를 쓰세요:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 작업하기

`Validator` 인스턴스의 `errors` 메서드 호출 시 `Illuminate\Support\MessageBag` 인스턴스를 받게 되며, 오류 메시지 작업에 편리한 다양한 메서드가 포함되어 있습니다. 리다이렉션 후 뷰에 자동 공유되는 `$errors` 변수 역시 이 `MessageBag` 타입입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 오류 메시지 가져오기

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 오류 메시지 가져오기

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 폼 필드인 경우 `*` 와일드카드를 사용해 각 요소에 대한 모든 메시지를 받을 수 있습니다:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 가져오기

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 오류 메시지 존재 여부 확인

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 사용자 지정 메시지 지정하기

Laravel 내장 유효성 규칙 오류 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 만약 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에서 각 규칙에 대해 맞춤 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리에 복사해 애플리케이션별 언어로 번역할 수도 있습니다. 자세한 내용은 [로컬라이제이션 문서](/docs/master/localization)를 보세요.

> [!WARNING]
> Laravel 기본 애플리케이션 템플릿에는 `lang` 디렉터리가 없기 때문에, 언어 파일을 수정하려면 `lang:publish` Artisan 명령어로 파일을 게시해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션 `lang/xx/validation.php` 언어 파일의 `custom` 배열에 속성-규칙별 오류 메시지를 넣어 커스터마이징할 수 있습니다:

```php
'custom' => [
    'email' => [
        'required' => '이메일 주소가 필요합니다!',
        'max' => '이메일 주소가 너무 깁니다!',
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

기본 오류 메시지의 `:attribute` 플레이스홀더를 바꾸려면, `lang/xx/validation.php` 내 `attributes` 배열에서 해당 필드 이름에 대응하는 사용자 정의 이름을 지정하세요:

```php
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]
> 기본 Laravel 템플릿에는 `lang` 디렉터리가 없으므로, 필요하면 `lang:publish` 명령어로 게시하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

일부 유효성 오류 메시지에는 `:value` 플레이스홀더가 있는데, 이는 검증 대상 속성값으로 교체됩니다. 기본값 대신 더 친숙한 값을 표시하려면 `lang/xx/validation.php` 파일 내에 `values` 배열을 정의할 수 있습니다. 예를 들어, `payment_type` 필드 값이 `cc`인 경우 '신용카드'라는 표현을 쓰고 싶다면:

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

기본 오류 메시지는 다음과 같이 나타날 수 있습니다:

```
The credit card number field is required when payment type is cc.
```

이 경우, 언어 파일에 다음과 같이 설정하면,

```php
'values' => [
    'payment_type' => [
        'cc' => '신용카드'
    ],
],
```

오류 메시지는 아래처럼 더 이해하기 쉽게 변경됩니다:

```
The credit card number field is required when payment type is 신용카드.
```

> [!WARNING]
> 기본 Laravel 템플릿에는 `lang` 디렉터리가 없으므로, 필요하면 `lang:publish` 명령어를 실행해 게시하세요.

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 규칙들 (Available Validation Rules)

아래는 Laravel에서 제공하는 모든 사용 가능한 유효성 규칙과 그 설명 목록입니다:

#### 불린형 (Booleans)

- [accepted](#rule-accepted)
- [accepted_if](#rule-accepted-if)
- [boolean](#rule-boolean)
- [declined](#rule-declined)
- [declined_if](#rule-declined-if)

#### 문자열 (Strings)

- [active_url](#rule-active-url)
- [alpha](#rule-alpha)
- [alpha_dash](#rule-alpha-dash)
- [alpha_num](#rule-alpha-num)
- [ascii](#rule-ascii)
- [confirmed](#rule-confirmed)
- [current_password](#rule-current-password)
- [different](#rule-different)
- [doesnt_start_with](#rule-doesnt-start-with)
- [doesnt_end_with](#rule-doesnt-end-with)
- [email](#rule-email)
- [ends_with](#rule-ends-with)
- [enum](#rule-enum)
- [hex_color](#rule-hex-color)
- [in](#rule-in)
- [ip](#rule-ip)
- [json](#rule-json)
- [lowercase](#rule-lowercase)
- [mac_address](#rule-mac)
- [max](#rule-max)
- [min](#rule-min)
- [not_in](#rule-not-in)
- [regex](#rule-regex)
- [not_regex](#rule-not-regex)
- [same](#rule-same)
- [size](#rule-size)
- [starts_with](#rule-starts-with)
- [string](#rule-string)
- [uppercase](#rule-uppercase)
- [url](#rule-url)
- [ulid](#rule-ulid)
- [uuid](#rule-uuid)

#### 숫자 (Numbers)

- [between](#rule-between)
- [decimal](#rule-decimal)
- [different](#rule-different)
- [digits](#rule-digits)
- [digits_between](#rule-digits-between)
- [gt](#rule-gt)
- [gte](#rule-gte)
- [integer](#rule-integer)
- [lt](#rule-lt)
- [lte](#rule-lte)
- [max](#rule-max)
- [max_digits](#rule-max-digits)
- [min](#rule-min)
- [min_digits](#rule-min-digits)
- [multiple_of](#rule-multiple-of)
- [numeric](#rule-numeric)
- [same](#rule-same)
- [size](#rule-size)

#### 배열 (Arrays)

- [array](#rule-array)
- [between](#rule-between)
- [contains](#rule-contains)
- [distinct](#rule-distinct)
- [in_array](#rule-in-array)
- [list](#rule-list)
- [max](#rule-max)
- [min](#rule-min)
- [size](#rule-size)

#### 날짜 (Dates)

- [after](#rule-after)
- [after_or_equal](#rule-after-or-equal)
- [before](#rule-before)
- [before_or_equal](#rule-before-or-equal)
- [date](#rule-date)
- [date_equals](#rule-date-equals)
- [date_format](#rule-date-format)
- [different](#rule-different)
- [timezone](#rule-timezone)

#### 파일 (Files)

- [between](#rule-between)
- [dimensions](#rule-dimensions)
- [extensions](#rule-extensions)
- [file](#rule-file)
- [image](#rule-image)
- [max](#rule-max)
- [mimetypes](#rule-mimetypes)
- [mimes](#rule-mimes)
- [size](#rule-size)

#### 데이터베이스 (Database)

- [exists](#rule-exists)
- [unique](#rule-unique)

#### 유틸리티 (Utilities)

- [bail](#rule-bail)
- [exclude](#rule-exclude)
- [exclude_if](#rule-exclude-if)
- [exclude_unless](#rule-exclude-unless)
- [exclude_with](#rule-exclude-with)
- [exclude_without](#rule-exclude-without)
- [filled](#rule-filled)
- [missing](#rule-missing)
- [missing_if](#rule-missing-if)
- [missing_unless](#rule-missing-unless)
- [missing_with](#rule-missing-with)
- [missing_with_all](#rule-missing-with-all)
- [nullable](#rule-nullable)
- [present](#rule-present)
- [present_if](#rule-present-if)
- [present_unless](#rule-present-unless)
- [present_with](#rule-present-with)
- [present_with_all](#rule-present-with-all)
- [prohibited](#rule-prohibited)
- [prohibited_if](#rule-prohibited-if)
- [prohibited_unless](#rule-prohibited-unless)
- [prohibits](#rule-prohibits)
- [required](#rule-required)
- [required_if](#rule-required-if)
- [required_if_accepted](#rule-required-if-accepted)
- [required_if_declined](#rule-required-if-declined)
- [required_unless](#rule-required-unless)
- [required_with](#rule-required-with)
- [required_with_all](#rule-required-with-all)
- [required_without](#rule-required-without)
- [required_without_all](#rule-required-without-all)
- [required_array_keys](#rule-required-array-keys)
- [sometimes](#validating-when-present)

---

이하는 각 규칙에 대한 상세 설명이며, 본문에서 확인하실 수 있습니다.