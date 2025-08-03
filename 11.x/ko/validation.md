# Validation
- [소개](#introduction)
- [검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [검증 오류 출력하기](#quick-displaying-the-validation-errors)
    - [폼 데이터 다시 채우기](#repopulating-forms)
    - [선택 필드에 대한 참고 사항](#a-note-on-optional-fields)
    - [검증 오류 응답 형식](#validation-error-response-format)
- [폼 요청 검증](#form-request-validation)
    - [폼 요청 생성하기](#creating-form-requests)
    - [폼 요청 권한 승인하기](#authorizing-form-requests)
    - [오류 메시지 커스터마이징](#customizing-the-error-messages)
    - [입력 데이터 검증 전 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름 있는 오류 백](#named-error-bags)
    - [오류 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 검증 수행하기](#performing-additional-validation)
- [검증된 입력값 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 검증](#validating-arrays)
    - [중첩 배열 입력 검증하기](#validating-nested-array-input)
    - [오류 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 검증](#validating-files)
- [비밀번호 검증](#validating-passwords)
- [커스텀 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터 검증을 위한 여러 방법을 제공합니다. 가장 일반적인 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용하는 것입니다. 그러나 다른 검증 방법도 함께 살펴보겠습니다.

Laravel에는 데이터에 적용할 수 있는 다양한 편리한 검증 규칙들이 포함되어 있으며, 값이 특정 데이터베이스 테이블에서 유일한지 검증하는 기능도 제공합니다. 이 모든 검증 규칙을 자세히 다루어 Laravel 검증 기능을 완전히 이해할 수 있도록 하겠습니다.

<a name="validation-quickstart"></a>
## 검증 빠른 시작

Laravel의 강력한 검증 기능을 배우기 위해, 폼을 검증하고 오류 메시지를 사용자에게 다시 보여주는 완전한 예제를 살펴봅니다. 이 개요를 통해 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 전반적으로 이해할 수 있을 것입니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정해봅니다:

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 게시물을 작성할 폼을 보여주고, `POST` 라우트는 새 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위 라우트를 처리하는 간단한 컨트롤러를 봅시다. `store` 메서드는 아직 비워둡니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 게시물 작성 폼 표시.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 게시물 저장.
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
### 검증 로직 작성하기

이제 새 게시물을 검증하는 로직을 `store` 메서드에 채워 넣을 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체의 `validate` 메서드를 사용할 것입니다. 검증 규칙을 모두 통과하면 코드가 정상적으로 실행을 계속하며, 검증 실패 시 `Illuminate\Validation\ValidationException` 예외가 발생하고 적절한 오류 응답이 자동으로 사용자에게 전송됩니다.

기본 HTTP 요청에서는 검증이 실패하면 이전 URL로 리다이렉트 응답이 생성됩니다. 만약 들어오는 요청이 XHR 요청이라면 [검증 오류 메시지를 포함한 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드에 대해 더 잘 이해하려면, `store` 메서드로 다시 돌아가 보겠습니다:

```
/**
 * 새 블로그 게시물 저장.
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

보시다시피, 검증 규칙을 `validate` 메서드에 전달합니다. 걱정하지 마세요 — 사용 가능한 모든 검증 규칙은 [문서화](#available-validation-rules)되어 있습니다. 검증 실패 시에는 자동으로 올바른 응답이 생성됩니다. 검증이 성공하면 컨트롤러가 계속 정상적으로 실행됩니다.

규칙은 `|`로 구분된 문자열 대신 배열로도 전달할 수 있습니다:

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, `validateWithBag` 메서드를 사용해 검증하고, 오류 메시지를 특정 [이름 있는 오류 백](#named-error-bags)에 저장할 수 있습니다:

```
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단하기

어떤 경우에는, 필드에 대해 첫 번째 검증 실패 후 나머지 규칙을 실행하지 않고 검증을 중단하고 싶을 수도 있습니다. 이를 위해 `bail` 규칙을 필드에 추가합니다:

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예에서는 `title` 필드의 `unique` 규칙이 실패하면, 이후의 `max` 규칙은 검사하지 않습니다. 규칙은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고 사항

HTTP 요청에 중첩된 필드 데이터가 있다면, 검증 규칙에서 "dot" 문법을 사용해 필드를 지정할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드 이름에 실제 온점(`.`)이 포함되어 있고 이를 dot 문법으로 해석하지 말게 하려면 백슬래시(`\`)로 이스케이프합니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 검증 오류 출력하기

만약 요청된 필드들이 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 말했듯이 Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 그리고 모든 검증 오류와 [요청 입력값](/docs/11.x/requests#retrieving-old-input)이 자동으로 [세션에 플래시됩니다](/docs/11.x/session#flash-data).

`$errors` 변수는 `web` 미들웨어 그룹이 제공하는 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에 의해 모든 뷰에 공유됩니다. 따라서 이 미들웨어가 적용된 뷰에서는 항상 `$errors` 변수를 사용 가능하며, 안전하게 이용할 수 있습니다. `$errors`는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 다루는 자세한 방법은 [문서 설명](#working-with-error-messages)을 참고하세요.

예제에서는 검증 실패 시 사용자가 `create` 메서드로 리다이렉트되고, 뷰에서 오류 메시지를 출력할 수 있습니다:

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

<!-- 게시물 작성 폼 -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 오류 메시지 커스터마이징

Laravel 내장 검증 규칙에는 각각 오류 메시지가 있으며, 이는 애플리케이션의 `lang/en/validation.php` 파일에 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 해당 디렉터리를 생성하도록 Laravel에 지시할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 검증 규칙에 대한 메시지 항목이 있습니다. 필요에 따라 이 메시지들을 자유롭게 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리로 복사해 애플리케이션 언어에 맞게 번역할 수도 있습니다. Laravel 로컬라이제이션에 대한 자세한 내용은 [로컬라이제이션 문서](/docs/11.x/localization)를 참조하세요.

> [!WARNING]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어로 파일을 게시하세요.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 검증

위 예는 전통적인 폼 제출을 사용하여 데이터를 전송했습니다. 하지만 많은 애플리케이션에서는 JavaScript 기반 프론트엔드가 XHR 요청을 보냅니다. `validate` 메서드가 XHR 요청 중에 호출되면 Laravel은 리다이렉트 응답을 생성하지 않고, 대신 모든 검증 오류를 포함한 [JSON 응답](#validation-error-response-format)을 422 HTTP 상태 코드와 함께 반환합니다.

<a name="the-at-error-directive"></a>
#### `@error` 지시어

`@error` [Blade](/docs/11.x/blade) 지시어는 특정 속성의 검증 오류 메시지가 존재하는지 빠르게 확인하는 용도로 사용할 수 있습니다. `@error` 블록 내에서는 `$message` 변수를 출력해 메시지를 표시할 수 있습니다:

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

만약 [이름 있는 오류 백](#named-error-bags)을 사용 중이라면, `@error` 지시어에 두 번째 인수로 백 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 데이터 다시 채우기

Laravel이 검증 오류로 인한 리다이렉트 응답을 생성하면, 프레임워크는 자동으로 [요청에 포함된 모든 입력 값을 세션에 플래시](#)합니다. 이를 통해 다음 요청에서 이전 입력 값을 쉽게 가져와 사용자가 제출하려던 폼을 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력 값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출합니다. 이 메서드는 세션에서 플래시된 이전 입력 값을 꺼냅니다:

```
$title = $request->old('title');
```

Laravel은 글로벌 `old` 헬퍼도 제공합니다. Blade 템플릿 내에서 이전 입력 값을 표시할 때 `old` 헬퍼를 사용하는 것이 더 편리합니다. 해당 필드에 이전 입력값이 없다면 `null`을 반환합니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 필드에 대한 참고 사항

기본적으로 Laravel 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 때문에 "선택" 필드 값이 `null`로 들어갈 수 있고, 이 경우 검증기가 이를 유효하지 않은 값으로 판단할 수 있습니다. 따라서 선택 필드는 `nullable` 규칙으로 표시해 `null` 값을 허용하도록 하는 것이 일반적입니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예에서 `publish_at` 필드는 `null`이거나 유효한 날짜 형식이어야 합니다. `nullable` 규칙이 없으면 `null`은 유효하지 않은 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 검증 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대할 경우, Laravel은 오류 메시지를 자동으로 포맷해 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

다음은 검증 오류에 대한 JSON 응답 예시입니다. 중첩된 오류 키들은 "dot" 표기법으로 평탄화되어 있습니다:

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
## 폼 요청 검증

<a name="creating-form-requests"></a>
### 폼 요청 생성하기

더 복잡한 검증 시나리오에서는 "폼 요청"을 생성하는 것이 권장됩니다. 폼 요청은 자신만의 검증 및 권한 승인 로직을 갖는 맞춤 요청 클래스입니다. `make:request` Artisan CLI 명령으로 폼 요청 클래스를 생성할 수 있습니다:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 해당 디렉터리가 존재하지 않으면 이 명령 실행 시 생성됩니다. 모든 생성된 폼 요청에는 `authorize`와 `rules` 두 메서드가 포함되어 있습니다.

`authorize` 메서드는 현재 인증된 사용자가 해당 요청에 담긴 액션을 수행할 권한이 있는지 판단하는 역할이며, `rules` 메서드는 요청 데이터에 적용할 검증 규칙을 반환합니다:

```
/**
 * 요청에 적용할 검증 규칙 반환.
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
> `rules` 메서드의 시그니처에 필요한 의존성을 타입힌팅할 수 있습니다. 이들은 Laravel의 [서비스 컨테이너](/docs/11.x/container)에서 자동으로 해결됩니다.

검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드의 인자로 해당 폼 요청 클래스를 타입힌트하면, 폼 요청은 컨트롤러 메서드가 호출되기 전 미리 검증됩니다. 따라서 컨트롤러에서 검증 로직을 직접 작성할 필요가 없습니다:

```
/**
 * 새 블로그 게시물 저장.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 들어온 요청이 유효함...

    // 검증된 입력 데이터 받기...
    $validated = $request->validated();

    // 검증된 입력 데이터 일부 받기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 게시물 저장...

    return redirect('/posts');
}
```

검증 실패 시, 사용자에게 이전 위치로 리다이렉트 응답이 생성되고 오류는 세션에 플래시됩니다. XHR 요청이었다면 422 상태 코드와 함께 [검증 오류 JSON 응답](#validation-error-response-format)이 반환됩니다.

> [!NOTE]  
> Inertia 기반 Laravel 프론트엔드에서 실시간 폼 요청 검증을 원한다면 [Laravel Precognition](/docs/11.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 검증 수행

초기 검증이 끝난 후 추가 검증이 필요한 경우, 폼 요청의 `after` 메서드를 사용할 수 있습니다.

`after` 메서드는 검증 완료 후 호출할 콜러블(함수 또는 클로저) 배열을 반환해야 하며, 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 인수로 받아 필요 시 추가 오류 메시지를 발생시킬 수 있습니다:

```
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 검증 콜러블 반환.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    '해당 필드에 문제가 있습니다!'
                );
            }
        }
    ];
}
```

또한 `after` 메서드는 호출 가능한 클래스를 포함할 수도 있습니다. 이 클래스의 `__invoke` 메서드는 `Validator` 인스턴스를 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청의 "after" 검증 콜러블 반환.
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
#### 첫 번째 검증 실패 시 중단

요청 클래스에 `stopOnFirstFailure` 속성을 추가하면, 단일 검증 실패 시 모든 필드 검증을 중단하도록 validator에 알릴 수 있습니다:

```
/**
 * validator가 첫 번째 규칙 실패 시 중단할지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 경로 커스터마이징

폼 요청 검증 실패 시 기본적으로 이전 위치로 리다이렉트합니다. 하지만 이 동작을 원하는 대로 바꿀 수도 있습니다. 이를 위해 폼 요청에 `$redirect` 프로퍼티를 정의하세요:

```
/**
 * 검증 실패 시 리다이렉트할 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 이름 붙은 라우트로 리다이렉트하려면 `$redirectRoute` 프로퍼티를 정의할 수 있습니다:

```
/**
 * 검증 실패 시 리다이렉트할 라우트.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 요청 권한 승인하기

폼 요청 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드에서는 인증된 사용자가 자원에 대한 수정 권한이 있는지 결정할 수 있습니다. 예를 들어, 유저가 수정하려는 댓글을 실제로 소유했는지를 검증할 수 있습니다. 보통 이 메서드 내에서 [인가 게이트 및 정책](/docs/11.x/authorization)와 상호작용합니다:

```
use App\Models\Comment;

/**
 * 요청할 권한이 있는지 판단.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 요청은 기본 Laravel 요청 클래스를 상속하므로, 현재 인증된 사용자에 `user` 메서드로 접근할 수 있습니다. 또한 위 예시에 나온 `route` 메서드는 해당 라우트 경로의 URI 파라미터(예: `{comment}`) 값을 가져옵니다:

```
Route::post('/comment/{comment}');
```

따라서 [라우트 모델 바인딩](/docs/11.x/routing#route-model-binding)을 활용한다면, 코드가 더 간결해집니다:

```
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면 403 HTTP 응답이 자동으로 반환되고, 컨트롤러 메서드는 실행되지 않습니다.

만약 권한 부여 로직을 다른 곳에서 처리한다면, `authorize` 메서드를 제거하거나 단순히 `true`를 반환하도록 할 수 있습니다:

```
/**
 * 요청 권한 승인 여부 결정.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]  
> `authorize` 메서드에 필요한 의존성을 타입힌팅할 수 있습니다. 이는 Laravel [서비스 컨테이너](/docs/11.x/container)에서 자동으로 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이징

폼 요청에서 사용하는 오류 메시지는 `messages` 메서드를 오버라이드하여 변경할 수 있습니다. 이 메서드는 속성과 규칙 쌍, 그리고 해당 오류 메시지를 배열 형태로 반환해야 합니다:

```
/**
 * 정의된 검증 규칙에 대한 오류 메시지 반환.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => '제목을 입력해야 합니다.',
        'body.required' => '내용을 입력해야 합니다.',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 검증 속성 커스터마이징

많은 Laravel 내장 검증 메시지에는 `:attribute` 플레이스홀더가 있습니다. 이 부분을 커스텀 속성명으로 교체하고 싶다면 `attributes` 메서드를 오버라이드하여 속성명-이름 쌍 배열을 반환하세요:

```
/**
 * 검증 오류에 사용할 커스텀 속성 반환.
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
### 입력 데이터 검증 전 준비하기

검증 규칙을 적용하기 전에 요청 데이터 일부를 준비하거나 정제해야 할 경우 `prepareForValidation` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Str;

/**
 * 검증을 위한 데이터 준비.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

유사하게, 검증이 끝난 후 데이터를 정규화해야 한다면 `passedValidation` 메서드를 활용할 수 있습니다:

```
/**
 * 검증이 통과한 후 처리.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 생성하기

요청의 `validate` 메서드를 사용하지 않으려면, `Validator` [파사드](/docs/11.x/facades)를 이용해 수동으로 Validator 인스턴스를 생성할 수 있습니다. `make` 메서드는 새 Validator 인스턴스를 만듭니다:

```
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

        // 검증 완료된 입력 받기...
        $validated = $validator->validated();

        // 검증 완료된 입력 일부만 받기...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 게시물 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인자는 검증할 데이터이고, 두 번째 인자는 검증 규칙 배열입니다.

요청이 실패했는지 판단 후 `withErrors` 메서드로 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용할 때, 리다이렉트 후 뷰에서 자동으로 `$errors` 변수를 사용 가능해서 사용자가 쉽게 오류 메시지를 볼 수 있습니다. `withErrors`는 Validator, `MessageBag`, PHP 배열을 인자로 받을 수 있습니다.

#### 첫 번째 검증 실패 시 중단

`stopOnFirstFailure` 메서드는 단일 검증 실패 시 모든 필드 검증을 중단하도록 Validator에 알립니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

Validator를 수동 생성했더라도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 이용하고 싶다면, 기존 Validator 인스턴스의 `validate` 메서드를 호출하세요. 실패 시 사용자가 자동으로 이전 위치로 리다이렉트되거나, XHR 요청일 경우 [JSON 응답](#validation-error-response-format)이 반환됩니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드를 사용해 실격된 오류 메시지를 [이름 있는 오류 백](#named-error-bags)에 저장할 수도 있습니다:

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름 있는 오류 백

한 페이지에 여러 폼이 있을 경우, 오류 메시지를 담는 `MessageBag`에 이름을 붙이고 싶을 수 있습니다. 이를 위해 `withErrors` 메서드에 두 번째 인자로 이름을 전달합니다:

```
return redirect('/register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수의 이름 있는 `MessageBag` 인스턴스를 접근할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 커스터마이징

필요하다면, Validator 인스턴스가 기본 Laravel 메시지 대신 사용할 커스텀 오류 메시지를 지정할 수 있습니다. 여러 방법이 있지만 첫째, `Validator::make` 메서드의 세 번째 인자로 메시지 배열을 전달할 수 있습니다:

```
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

`:attribute` 플레이스홀더는 검증 중인 실제 필드 이름으로 치환됩니다. 다른 플레이스홀더도 활용 가능합니다. 예:

```
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대한 커스텀 메시지 지정

특정 속성에만 커스텀 오류 메시지를 지정할 수도 있습니다. "dot" 표기법으로 필드 이름 뒤에 규칙을 연결하세요:

```
$messages = [
    'email.required' => '이메일 주소를 입력해주세요!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 사용자 지정 속성 값 지정

Laravel 내장 메시지는 `:attribute` 플레이스홀더를 사용하는데, 이를 특정 필드별로 커스텀 값으로 바꾸려면 `Validator::make`의 네 번째 인자로 속성명-표현 쌍 배열을 전달합니다:

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 검증 수행하기

초기 검증이 끝난 뒤 추가 검증이 필요할 때는 Validator의 `after` 메서드를 사용할 수 있습니다. 이 메서드는 클로저 또는 콜러블 배열을 받고, 검증 완료 후 호출하여 필요 시 추가 오류 메시지를 발생시킬 수 있게 합니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', '해당 필드에 문제가 있습니다!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

`after` 메서드는 콜러블 배열도 받을 수 있는데, "after validation" 로직을 `__invoke` 메서드를 가진 호출 가능한 클래스로 캡슐화 시 유용합니다:

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

폼 요청이나 수동 생성한 Validator로 입력값을 검증한 후, 실제 검증된 데이터를 가져오고 싶을 수 있습니다. 여러 방법이 있습니다. 먼저, 폼 요청이나 Validator 인스턴스의 `validated` 메서드를 호출하면 검증된 데이터 배열을 반환합니다:

```
$validated = $request->validated();

$validated = $validator->validated();
```

또는 `safe` 메서드를 호출해 `Illuminate\Support\ValidatedInput` 인스턴스를 받을 수 있습니다. 이 객체는 `only`, `except`, `all` 메서드를 제공하여 검증 데이터 일부 또는 전체를 쉽게 가져올 수 있습니다:

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

`Illuminate\Support\ValidatedInput` 인스턴스는 반복(iterate)하거나 배열처럼 접근하는 것도 가능합니다:

```
// 반복 사용 가능...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근 가능...
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 필드를 추가하고 싶다면 `merge` 메서드를 호출하세요:

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증 데이터를 [컬렉션](/docs/11.x/collections)으로 받고 싶다면 `collect` 메서드를 사용할 수 있습니다:

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기

`Validator` 인스턴스의 `errors` 메서드 호출 시, `Illuminate\Support\MessageBag` 인스턴스를 받습니다. 이 객체는 오류 메시지를 다루기 편한 다양한 메서드를 제공합니다. 모든 뷰에서 자동으로 사용 가능한 `$errors` 변수도 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드 첫 번째 오류 메시지 가져오기

특정 필드의 첫 번째 오류 메시지를 가져오려면 `first` 메서드를 사용하세요:

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드 모든 오류 메시지 가져오기

특정 필드에 해당하는 모든 오류 메시지 배열이 필요하면 `get` 메서드를 사용하세요:

```
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 필드를 검증하는 경우, `*` 문자를 써서 배열 각 요소별 모든 오류 메시지를 받을 수 있습니다:

```
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드 모든 오류 메시지 가져오기

모든 필드에 대해 모든 오류 메시지를 배열로 받고 싶으면 `all` 메서드를 사용하세요:

```
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드 오류 메시지 존재 여부 확인

특정 필드에 오류 메시지가 하나라도 존재하는지 알아보려면 `has` 메서드를 사용합니다:

```
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel 내장 검증 규칙은 애플리케이션 `lang/en/validation.php` 파일에 오류 메시지가 정의되어 있습니다. 만약 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어를 통해 생성할 수 있습니다.

`lang/en/validation.php` 내 각 검증 규칙별 항목을 필요에 맞게 수정할 수 있습니다.

파일을 다른 언어 디렉터리에 복사해 애플리케이션 언어로 번역하는 것도 가능합니다. 더 자세한 내용은 [로컬라이제이션 문서](/docs/11.x/localization)를 참고하세요.

> [!WARNING]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어를 실행하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션 언어 파일의 `custom` 배열에 속성 및 규칙별 메시지를 지정할 수 있습니다:

```
'custom' => [
    'email' => [
        'required' => '이메일 주소를 알려주세요!',
        'max' => '이메일 주소가 너무 깁니다!',
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

Laravel 내장 메시지에는 `:attribute` 플레이스홀더가 있습니다. 이것을 커스텀 문자열로 바꾸고 싶으면 `attributes` 배열에 지정하세요:

```
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어를 실행하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

Laravel 내장 메시지 중 `:value` 플레이스홀더가 포함된 경우, 실제 요청 속성의 값을 표시합니다. 그러나 때때로 사용자 친화적 표현으로 바꾸고 싶을 수 있습니다.

예를 들어 `payment_type`이 `cc`이면 신용카드 번호가 필요하다고 하는 규칙이 있다고 합시다:

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

검증 실패 시 기본 메시지는 다음과 같습니다:

```none
The credit card number field is required when payment type is cc.
```

`lang/xx/validation.php` 파일 내 `values` 배열을 지정해 `cc` 대신 `credit card`로 표시되게 할 수 있습니다:

```
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어를 실행하세요.

이제 검증 실패 메시지는 이렇게 표시됩니다:

```none
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 검증 규칙

아래는 Laravel에서 제공하는 주요 검증 규칙과 기능별 분류입니다:


#### 부울(Booleans)

<div class="collection-method-list" markdown="1">

[accepted](#rule-accepted)
[accepted_if](#rule-accepted-if)
[boolean](#rule-boolean)
[declined](#rule-declined)
[declined_if](#rule-declined-if)

</div>

#### 문자열(Strings)

<div class="collection-method-list" markdown="1">

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

</div>

#### 숫자(Numbers)

<div class="collection-method-list" markdown="1">

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

</div>

#### 배열(Arrays)

<div class="collection-method-list" markdown="1">

[array](#rule-array)
[between](#rule-between)
[contains](#rule-contains)
[distinct](#rule-distinct)
[in_array](#rule-in-array)
[list](#rule-list)
[max](#rule-max)
[min](#rule-min)
[size](#rule-size)

</div>

#### 날짜(Dates)

<div class="collection-method-list" markdown="1">

[after](#rule-after)
[after_or_equal](#rule-after-or-equal)
[before](#rule-before)
[before_or_equal](#rule-before-or-equal)
[date](#rule-date)
[date_equals](#rule-date-equals)
[date_format](#rule-date-format)
[different](#rule-different)
[timezone](#rule-timezone)

</div>

#### 파일(Files)

<div class="collection-method-list" markdown="1">

[between](#rule-between)
[dimensions](#rule-dimensions)
[extensions](#rule-extensions)
[file](#rule-file)
[image](#rule-image)
[max](#rule-max)
[mimetypes](#rule-mimetypes)
[mimes](#rule-mimes)
[size](#rule-size)

</div>

#### 데이터베이스(Database)

<div class="collection-method-list" markdown="1">

[exists](#rule-exists)
[unique](#rule-unique)

</div>

#### 유틸리티(Utilities)

<div class="collection-method-list" markdown="1">

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

</div>

<a name="rule-accepted"></a>
#### accepted

검증 대상 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"` 이어야 합니다. 이용 약관 동의 같은 필드 검증 시 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

검증 대상 필드는 다른 지정한 필드가 특정 값일 때 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"` 이어야 합니다. 이용 약관 동의 같은 필드 검증 시 활용합니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드는 PHP `dns_get_record` 함수가 반환하는 유효한 A 또는 AAAA DNS 레코드를 가져야 합니다. URL의 호스트명은 `parse_url` 함수로 추출 후 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드는 지정된 날짜 이후여야 합니다. 날짜는 PHP `strtotime` 함수로 `DateTime` 객체로 변환됩니다:

```
'start_date' => 'required|date|after:tomorrow'
```

문자열 대신 다른 필드를 지정해 날짜 비교도 가능합니다:

```
'finish_date' => 'required|date|after:start_date'
```

편의를 위해 날짜 기반 규칙을 유창한(fluent) `date` 룰 빌더로 작성할 수 있습니다:

```
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드는 각각 오늘 이후, 오늘 포함 이후를 표현하는 데 편리합니다:

```
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
#### after_or_equal:_date_

검증 대상 필드는 지정된 날짜와 같거나 이후여야 합니다. 자세한 내용은 [after 규칙](#rule-after)을 참조하세요.

유창한 규칙 빌더로 작성도 가능합니다:

```
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-alpha"></a>
#### alpha

검증 대상 필드는 [유니코드 알파벳 문자 집합인 `\p{L}`와 `\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=)에 포함된 문자만 포함해야 합니다.

ASCII 범위(`a-z`, `A-Z`) 문자만 허용하려면 `ascii` 옵션을 규칙에 추가하세요:

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 대상 필드는 [유니코드 문자 집합 `\p{L}`, `\p{M}`, `\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 ASCII 대시(`-`)와 밑줄(`_`)만 포함해야 합니다.

ASCII 문자만 제한하려면 `ascii` 옵션을 추가하세요:

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증 대상 필드는 [유니코드 문자 집합 `\p{L}`, `\p{M}`, `\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=)에 속하는 문자만 포함해야 합니다.

ASCII 문자만 제한하려면 `ascii` 옵션을 추가합니다:

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 대상 필드는 PHP `array`이어야 합니다.

`array` 규칙에 추가 값이 제공되면, 입력 배열의 각 키가 지정된 값 목록에 존재해야 합니다. 아래 예제에서 입력 배열의 `admin` 키는 허용 값 목록에 없으므로 유효하지 않습니다:

```
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

일반적으로 배열 내 허용할 키를 항상 명시해야 합니다.

<a name="rule-ascii"></a>
#### ascii

검증 대상 필드는 7비트 ASCII 문자만 포함해야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드에서 첫 번째 검증 실패가 발생하면 이후 규칙 검증을 중단합니다.

`bail`은 필드별 검증 중단인 반면, `stopOnFirstFailure`는 단일 실패 시 모든 필드 검증을 중단하게 합니다:

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 대상 필드는 지정된 날짜 이전이어야 합니다. 날짜는 PHP `strtotime` 함수로 `DateTime` 객체로 변환됩니다. `after` 규칙과 마찬가지로 날짜 대신 다른 필드명을 지정할 수도 있습니다.

유창한 규칙 빌더를 사용할 수 있습니다:

```
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday` 또는 `todayOrBefore` 메서드를 이용하면 각각 오늘 이전, 오늘 포함 이전을 표현하기 쉽습니다:

```
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 대상 필드는 지정된 날짜 또는 그 이전이어야 합니다. 위 [before](#rule-before) 규칙을 참조하세요.

유창한 규칙 빌더로도 작성 가능합니다:

```
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

검증 대상 필드 크기는 _min_ 이상 _max_ 이하 범위여야 합니다. 문자열, 숫자, 배열, 파일은 [`size`](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

검증 대상 필드는 `true`, `false`, `1`, `0`, `"1"`, `"0"`으로 변환 가능해야 합니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드는 `{field}_confirmation` 필드와 값이 일치해야 합니다. 예를 들어 `password` 필드가 있다면, `password_confirmation` 필드가 있어야 합니다.

커스텀 확인 필드명도 가능합니다: `confirmed:repeat_username`는 `repeat_username` 필드가 검증 대상과 같아야 함을 의미합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

검증 대상 필드는 지정한 모든 값을 포함하는 배열이어야 합니다.

<a name="rule-current-password"></a>
#### current_password

검증 대상 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 검증자의 첫 번째 인수로 [인증 가드](/docs/11.x/authentication)를 지정할 수 있습니다:

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 대상 필드는 PHP `strtotime` 함수가 인식하는 유효한 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 대상 필드는 지정된 날짜와 같아야 합니다. 날짜는 PHP `strtotime` 함수로 변환됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 대상 필드는 지정된 날짜 형식 중 하나와 일치해야 합니다. 문자열이나 날짜 검증 시 `date` 또는 `date_format` 중 하나만 사용하는 것이 좋습니다. 이 규칙은 PHP [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 포맷을 지원합니다.

유창한 규칙 빌더로 작성 가능:

```
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

검증 대상 필드는 숫자이며, 지정된 소수점 자릿수를 가져야 합니다:

```
// 정확히 두 자리 소수 (예: 9.99)...
'price' => 'decimal:2'

// 두 자리 이상 네 자리 이하 소수...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"`여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

검증 대상 필드는 다른 필드가 특정 값일 때 `"no"`, `"off"`, `0`, `"0"`, `false` 또는 `"false"`여야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드와 지정된 _field_ 값이 달라야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수는 지정한 _value_ 길이와 정확히 일치해야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 대상 정수 길이가 _min_ 이상 _max_ 이하이어야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 아래 명시한 치수 제한을 만족하는 이미지이어야 합니다:

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제한자: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_.

비율 제약은 3/2와 같은 분수 또는 1.5와 같은 실수로 표현 가능합니다:

```
'avatar' => 'dimensions:ratio=3/2'
```

여러 인수를 필요로 하므로 `Rule::dimensions` 메서드로 유창하게 작성하는 것이 편리합니다:

```
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

배열 검증 시 중복된 값이 없어야 합니다:

```
'foo.*.id' => 'distinct'
```

기본적으로 느슨한 비교를 사용하지만, 엄격한 비교가 필요하면 `strict` 매개변수를 추가하세요:

```
'foo.*.id' => 'distinct:strict'
```

대소문자를 무시하려면 `ignore_case` 매개변수를 추가할 수 있습니다:

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 규칙은 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation`이 적용되지만, 아래와 같이 다른 스타일도 적용 가능합니다:

```
'email' => 'email:rfc,dns'
```

다음은 적용 가능한 스타일 목록입니다:

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - RFC 5322 요구사항 준수.
- `strict`: `NoRFCWarningsValidation` - RFC 5322 준수, 끝에 점 두 개 이상 또는 연속 점 허용 안 함.
- `dns`: `DNSCheckValidation` - 유효한 MX 레코드 확인.
- `spoof`: `SpoofCheckValidation` - 동형문자 스푸핑 방지.
- `filter`: `FilterEmailValidation` - PHP `filter_var`로 유효성 검증.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP `filter_var`에서 일부 유니코드 허용.

</div>

유창한 룰 빌더로도 작성 가능합니다:

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
> `dns` 및 `spoof` 검증기는 PHP `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 룰은 클래스 기반 규칙으로, 검증 대상 값이 유효한 Enum 값인지 검사합니다. `Enum` 룰에 Enum 클래스명을 생성자 인자로 넘깁니다. 원시 값을 검증할 때는 백드 Enum을 전달해야 합니다:

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 룰의 `only`와 `except` 메서드로 유효 케이스를 한정할 수 있습니다:

```
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드로 조건부로 룰을 수정할 수 있습니다:

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

검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

다른 필드 값이 특정 값과 같으면, 검증 대상 필드는 반환된 검증 데이터에서 제외됩니다.

복잡한 조건은 `Rule::excludeIf` 메서드를 사용합니다. 불리언 또는 클로저를 받으며, 클로저는 필드 제외 여부를 `true`/`false` 반환으로 알려야 합니다:

```
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

다른 필드 값이 특정 값이 아닌 경우, 검증 대상 필드는 검증된 반환 데이터에서 제외됩니다. _value_가 `null`인 경우 (`exclude_unless:name,null`), 비교 필드가 `null`이거나 요청 데이터에 없을 땐 제외되지 않습니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

다른 필드가 존재하면 검증 대상 필드는 검증 반환 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

다른 필드가 없으면 검증 대상 필드는 반환 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 대상 값이 지정된 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 규칙 기본 사용법

```
'state' => 'exists:states'
```

`column`이 지정되지 않으면 필드명이 컬럼명으로 사용됩니다. 따라서 위 규칙은 `states` 테이블 내 `state` 컬럼 값 중 입력값이 존재하는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
#### 컬럼명 직접 지정하기

테이블명 뒤에 컬럼명을 명시해 사용할 컬럼을 직접 지정할 수 있습니다:

```
'state' => 'exists:states,abbreviation'
```

특정 데이터베이스 연결을 지정하려면 연결명과 테이블명을 콤마 대신 점(`.`)으로 구분해 지정합니다:

```
'email' => 'exists:connection.staff,email'
```

테이블명 대신 Eloquent 모델명을 써서 테이블을 결정할 수도 있습니다:

```
'user_id' => 'exists:App\Models\User,id'
```

쿼리를 수정하려면 `Rule` 클래스를 활용해 구문을 유창하게 조절할 수 있습니다:

```
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

`Rule::exists` 메서드에 두 번째 인자로 컬럼명을 직접 지정할 수도 있습니다:

```
'state' => Rule::exists('states', 'abbreviation'),
```

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 대상 파일은 명시한 확장자 중 하나를 가져야 합니다:

```
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]  
> 확장자를 통한 검증만 의존하지 마세요. 보통 [`mimes`](#rule-mimes) 또는 [`mimetypes`](#rule-mimetypes) 규칙과 함께 사용합니다.

<a name="rule-file"></a>
#### file

검증 대상 필드는 정상 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

필드가 존재할 경우 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 대상 값은 지정한 다른 필드 또는 값보다 커야 합니다. 타입은 같아야 하며, 문자열, 숫자, 배열, 파일은 [`size`](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 대상 값은 지정한 필드 또는 값과 같거나 커야 합니다. 타입은 같아야 하며 [`size`](#rule-size) 규칙과 동일하게 처리합니다.

<a name="rule-hex-color"></a>
#### hex_color

검증 대상 필드는 16진수 CSS 색상 형식이어야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지 여야 하며, jpg, jpeg, png, bmp, gif, svg, webp 형식이 허용됩니다.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 대상 값은 지정한 값 목록에 포함되어야 합니다. 배열을 `implode`해야 하는 경우가 많으므로 `Rule::in` 메서드로 유창하게 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

`array`와 함께 사용할 때, 입력 배열의 모든 값이 `in` 목록에 포함되어야 합니다. 아래 예제에서는 `LAS`는 허용되지 않는 값입니다:

```
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

검증 대상 값은 다른 필드 배열 값 내에 존재해야 합니다.

<a name="rule-integer"></a>
#### integer

검증 대상 필드는 정수여야 합니다.

> [!WARNING]  
> 이 규칙은 입력 타입이 실제 정수인지 검사하는 것은 아니고, PHP 내 `FILTER_VALIDATE_INT`에 통과하는지만 확인합니다. 숫자 타입 검사에는 `numeric` 규칙과 함께 사용하세요.

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

검증 대상 값은 지정 필드 값보다 작아야 하며, 두 값은 동일 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [`size`](#rule-size) 규칙과 같이 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 대상 값은 지정 필드 값보다 작거나 같아야 하며, 두 값은 동일 타입이어야 합니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 대상 필드는 소문자만 포함해야 합니다.

<a name="rule-list"></a>
#### list

검증 대상 필드는 연속된 0부터 `count($array) - 1`까지 정수 키를 갖는 배열이어야 합니다(리스트 배열).

<a name="rule-mac"></a>
#### mac_address

검증 대상 값은 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 대상 값은 지정한 최대값 이하이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 같은 평가 방식을 따릅니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 대상 정수는 자리수가 최대 _value_ 이어야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 대상 파일의 MIME 타입이 지정한 것 중 하나여야 합니다:

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

MIME 타입은 업로드된 파일 내용을 검사해 결정되며, 클라이언트가 알려준 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 대상 파일 확장자가 지정한 확장자 중 하나이어야 합니다:

```
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하지만, 실제로는 파일 내용을 검사해 MIME 타입을 확인합니다. MIME 타입과 확장자 대응표는 아래 링크에서 확인할 수 있습니다:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 규칙은 MIME 타입과 사용자 지정 확장자가 일치하는지 검증하지 않습니다. 예를 들어 `mimes:png` 규칙은 `photo.txt`라는 이름이어도 PNG 내용이면 유효로 간주합니다. 사용자 지정 확장자 검증만 원하면 [`extensions`](#rule-extensions) 규칙을 사용하세요.

<a name="rule-min"></a>
#### min:_value_

검증 대상 값은 지정한 최소값 이상이어야 하며, 문자열, 숫자, 배열, 파일은 [`size`](#rule-size) 규칙과 동일한 평가 방식을 사용합니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 대상 정수는 자리수가 최소 _value_ 이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 대상 값은 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증 대상 필드는 입력 데이터에 없어야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

다른 필드가 지정한 값 중 하나일 경우, 검증 대상 필드가 없어야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

다른 필드가 지정한 값 중 하나가 아닌 경우, 검증 대상 필드는 없어야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

다른 지정 필드 중 하나라도 존재할 때만 검증 대상 필드가 없어야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

다른 지정 필드가 모두 존재할 때만 검증 대상 필드가 없어야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 대상 값은 지정한 값 목록에 없어야 합니다. `Rule::notIn` 메서드로 작성할 수 있습니다:

```
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

검증 대상 값은 지정한 정규식과 일치하면 안 됩니다.

내부적으로 PHP `preg_match`를 사용합니다. 패턴은 `preg_match` 규약에 따르고 적절한 구분자를 포함해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]  
> `regex` / `not_regex` 패턴은 `|` 문자를 포함하는 경우 배열 형식으로 지정하는 것이 좋습니다.

<a name="rule-nullable"></a>
#### nullable

검증 대상 필드는 `null`이어도 유효합니다.

<a name="rule-numeric"></a>
#### numeric

검증 대상 필드는 숫자여야 합니다.

<a name="rule-present"></a>
#### present

검증 대상 필드는 입력 데이터 내에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

다른 필드가 지정된 값 중 하나일 경우, 검증 대상 필드가 입력 데이터 내에 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

다른 필드가 지정된 값 중 하나가 아닐 경우, 검증 대상 필드가 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

다른 지정 필드 중 하나라도 존재할 경우만 검증 대상 필드가 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

다른 지정 필드가 모두 존재할 경우만 검증 대상 필드가 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 대상 필드는 비어 있거나 없어야 합니다. '비어 있음' 조건:

<div class="content-list" markdown="1">

- 값이 `null` 이거나,
- 빈 문자열이거나,
- 빈 배열 또는 빈 Countable 객체거나,
- 빈 경로 업로드된 파일인 경우.

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

다른 필드가 지정된 값 중 하나일 경우, 검증 대상 필드는 비어 있거나 없어야 합니다. 비어 있음 조건은 위와 같습니다.

복잡한 조건이 필요하면 `Rule::prohibitedIf` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

다른 필드가 지정한 값 중 하나가 아닐 경우, 검증 대상 필드는 비어 있거나 없어야 합니다. 비어 있음 조건은 위와 같습니다.

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 대상 필드가 비어있지 않은 경우, 다른 지정 필드들은 모두 비어 있거나 없어야 합니다. 비어 있음의 기준은 위와 같습니다.

<a name="rule-regex"></a>
#### regex:_pattern_

검증 대상 값이 지정한 정규식과 일치해야 합니다.

내부적으로 PHP `preg_match`를 사용하며, 패턴은 `preg_match` 포맷에 따라야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]  
> `regex` / `not_regex` 패턴 사용 시 `|` 문자가 있으면 배열 형식 검증 규칙 지정이 필요할 수 있습니다.

<a name="rule-required"></a>
#### required

검증 대상 필드는 입력 데이터에 존재하고, 비어 있으면 안 됩니다. 비어 있음은 다음 중 하나입니다:

<div class="content-list" markdown="1">

- 값이 `null`,
- 빈 문자열,
- 빈 배열 또는 빈 Countable 객체,
- 경로가 없는 업로드된 파일.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

다른 필드가 특정 값 중 하나일 때 검증 대상 필드는 존재하고 비어 있으면 안 됩니다.

복잡 조건은 `Rule::requiredIf` 메서드로 작성 가능:

```
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

다른 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"`일 경우, 검증 대상 필드는 존재해야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

다른 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"`일 경우 검증 대상 필드는 존재해야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

다른 필드가 지정한 값이 아닐 경우, 검증 대상 필드는 존재해야 합니다. `required_unless:name,null`인 경우, 비교 필드가 `null`이거나 없으면 필드 존재가 강제되지 않습니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

다른 지정한 필드 중 하나라도 존재하면, 검증 대상 필드는 존재해야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

다른 지정 필드가 모두 존재하면, 검증 대상 필드는 존재해야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

다른 지정 필드 중 하나라도 없거나 비어 있을 때만 검증 대상 필드가 존재해야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

다른 지정 필드가 모두 없거나 비어 있을 때만 검증 대상 필드가 존재해야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증 대상 필드는 배열이어야 하며, 지정한 키들을 최소한 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정한 _field_ 값과 검증 대상 필드 값이 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증 대상 값 크기가 _value_와 정확히 일치해야 합니다. 문자열일 땐 문자 수, 숫자일 땐 값 자체, 배열은 요소 수, 파일은 킬로바이트 단위입니다. 예:

```
// 12자 문자열 검증...
'title' => 'size:12';

// 10 정수 검증...
'seats' => 'integer|size:10';

// 5개 요소 배열 검증...
'tags' => 'array|size:5';

// 512 KB 파일 검증...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 대상 필드는 문자열이어야 합니다. `null` 허용 시 `nullable` 규칙을 추가하세요.

<a name="rule-timezone"></a>
#### timezone

검증 대상은 `DateTimeZone::listIdentifiers` 메서드가 인정하는 유효한 타임존 식별자여야 합니다.

옵션 인자를 지정할 수 있습니다:

```
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증 대상 값은 지정된 데이터베이스 테이블 내에 없어야 합니다.

**커스텀 테이블·컬럼명 지정:**

직접 테이블명을 지정하기 보다, Eloquent 모델명을 써서 테이블명을 결정할 수 있습니다:

```
'email' => 'unique:App\Models\User,email_address'
```

컬럼명도 지정할 수 있습니다. 컬럼명 미지정 시 필드명이 컬럼명으로 사용됩니다:

```
'email' => 'unique:users,email_address'
```

**커스텀 DB 연결 지정:**

쿼리할 DB 연결이 다르면 연결명.테이블명 형식으로 지정할 수 있습니다:

```
'email' => 'unique:connection.users,email_address'
```

**특정 ID 무시:**

유니크 검증에서 특정 ID를 무시하려면 `Rule` 클래스를 사용합니다. 아래는 유저 이메일 중복 검증시 자기 자신의 ID는 무시하는 예:

```
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
> `ignore` 메서드에 사용자 입력값을 직접 넣으면 SQL 인젝션 위험이 있으므로, 반드시 신뢰 가능한 시스템 생성 ID(예: Eloquent 모델의 기본키)만 사용해야 합니다.

모델 인스턴스를 직접 전달해도 키를 자동 추출합니다:

```
Rule::unique('users')->ignore($user)
```

기본 키 이름이 `id`가 아니라면 두 번째 인자로 이름을 지정할 수 있습니다:

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

`unique` 룰 기본 컬럼은 검증 속성명이지만, `unique` 메서드 두 번째 인자로 다른 컬럼명을 넘길 수 있습니다:

```
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 where 조건 지정:**

`where` 메서드로 쿼리를 확장할 수 있습니다. 예:

```
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Soft Delete 레코드 무시:**

기본 `unique` 규칙은 소프트 삭제된 레코드도 포함합니다. 무시하려면 `withoutTrashed` 메서드를 호출하세요:

```
Rule::unique('users')->withoutTrashed();
```

`deleted_at` 컬럼명 대신 다른 컬럼명을 쓰면 인자로 넘길 수 있습니다:

```
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증 대상 필드는 대문자만 포함해야 합니다.

<a name="rule-url"></a>
#### url

검증 대상 필드는 유효한 URL이어야 합니다.

허용할 프로토콜을 지정할 수 있습니다:

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증 대상 필드는 유효한 ULID(Universally Unique Lexicographically Sortable Identifier)이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 대상 필드는 유효한 RFC 9562 UUID(버전 1,3,4,5,6,7,8)이어야 합니다.

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 검증 건너뛰기

다른 필드가 특정 값일 경우 해당 필드를 검증하지 않을 수 있습니다. `exclude_if` 규칙 사용 예시:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로 `exclude_unless`는 다른 필드가 값일 때만 검증합니다:

```
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 필드가 존재할 때만 검증

검증 대상 필드가 데이터에 있으면 검증하고 없으면 건너뛰려면 `sometimes` 규칙을 추가하세요:

```
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

이 때 `email` 필드는 `$data`에 있을 때만 검증됩니다.

> [!NOTE]  
> 항상 존재하지만 빈 값 허용 필드 검증 시 [선택 필드 참고](#a-note-on-optional-fields)를 참고하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

예를 들어, 특정 필드 값이 100 이상일 때만 다른 필드를 필수로 하거나, 특정 필드가 존재할 때만 두 개 필드를 검증하는 등의 조건부 검증을 구현할 수 있습니다.

먼저 고정 규칙(static rules)로 Validator 인스턴스를 생성합니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);
```

게임 수가 100 이상일 때 이유를 적도록 조건부 규칙을 추가합니다:

```
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

첫 번째 인자는 조건부 규칙을 적용할 필드명, 두 번째는 추가할 규칙 목록, 세 번째는 조건 클로저입니다. 클로저가 `true` 반환 시 규칙을 추가합니다. 여러 필드도 한 번에 지정 가능:

```
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]  
> 조건부 클로저 첫 번째 인자는 `Illuminate\Support\Fluent` 인스턴스이며, 입력값과 파일에 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 중첩 배열 조건부 검증

인덱스가 알려지지 않은 중첩 배열의 요소별로 필드 조건부 검증도 가능하며, 클로저 인자는 두 번째 매개변수로 해당 요소를 받습니다:

```
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

검증 대상 배열 요소가 배열일 때 `$item`은 `Illuminate\Support\Fluent` 인스턴스이며, 그렇지 않으면 문자열입니다.

<a name="validating-arrays"></a>
## 배열 검증

[`array`](#rule-array) 규칙에 설명된 것처럼 `array` 규칙은 허용 배열 키 목록을 받으며, 목록에 없는 키가 있으면 검증이 실패합니다:

```
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

일반적으로 배열 내 허용할 키를 명시하는 것이 좋습니다. 그렇지 않으면 `validate`와 `validated` 메서드가 검증하지 않은 배열 키까지 결과에 포함할 수 있습니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 검증하기

중첩 배열 기반 폼 입력 검증도 간단합니다. "dot notation"을 사용해 배열 안의 속성도 검증할 수 있습니다. 예를 들어, 입력에 `photos[profile]` 필드가 있다면:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소별로도 검증할 수 있습니다. 예를 들어 배열 내 모든 이메일 주소를 고유하게 검증하려면:

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

언어 파일에서 [커스텀 검증 메시지](#custom-messages-for-specific-attributes)에 `*` 문자를 사용해 배열 필드 메시지를 한 번에 지정할 수 있습니다:

```
'custom' => [
    'person.*.email' => [
        'unique' => '각 사람은 고유한 이메일 주소를 가져야 합니다',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근

배열 요소별 검증 규칙 지정 시 값에 접근하려면 `Rule::forEach` 메서드를 사용하세요. 배열 요소 값과 펼쳐진 속성 이름을 인자로 받아 배열 규칙을 반환합니다:

```
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
### 오류 메시지 인덱스와 위치

배열 검증 시, 실패한 항목의 인덱스나 위치를 오류 메시지에 표시하고 싶다면 [커스텀 메시지](#manual-customizing-the-error-messages) 안에서 `:index`(0부터 시작)와 `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다:

```
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

위 예제에선 두 번째 사진 설명이 비어 있으므로, `"사진 #2에 대해 설명해주세요."` 오류 메시지가 표시됩니다.

깊게 중첩된 인덱스의 경우 `second-index`, `second-position`, `third-index` 등으로 표시할 수 있습니다:

```
'photos.*.attributes.*.string' => '사진 #:second-position 속성에 올바르지 않은 값이 있습니다.',
```

<a name="validating-files"></a>
## 파일 검증

Laravel은 `mimes`, `image`, `min`, `max` 등 업로드 파일 검증 시 유용하게 쓸 수 있는 다양한 규칙을 제공합니다. 개별적으로 규칙을 지정할 수 있지만, 편리하게 쓸 수 있도록 유창한 파일 검증 룰 빌더도 제공합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)           // 최소 1024 바이트
            ->max(12 * 1024),    // 최대 12킬로바이트
    ],
]);
```

<a name="validating-files-file-types"></a>
#### 파일 타입 검증

`types` 메서드는 확장자만 입력받지만 파일 내용을 확인해 MIME 타입을 검사합니다. MIME 타입-확장자 표는 다음 링크에서 확인하세요:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 검증

최소/최대 파일 크기를 문자열과 크기 단위 접미사로 지정 가능하며, `kb`, `mb`, `gb`, `tb` 등 단위를 지원합니다:

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 검증

업로드한 파일이 이미지인지 검증하려면 `File` 룰의 `image` 생성 메서드를 사용하세요. `File::image()`는 jpg, jpeg, png, bmp, gif, svg, webp 이미지임을 보장합니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image(),
    ],
]);
```

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기 검증

업로드된 이미지의 크기를 제한할 수도 있습니다. 예를 들어 너비 최소 1000px, 높이 최소 500px를 적용하려면 `dimensions` 룰을 사용하세요:

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
> 이미지를 위한 크기 검증 상세 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하세요.

<a name="validating-passwords"></a>
## 비밀번호 검증

비밀번호 복잡도 요구사항을 손쉽게 설정하려면 Laravel의 `Password` 룰 객체를 사용합니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 룰 객체로 비밀번호에 최소 글자 수, 문자 포함, 대소문자 혼합, 숫자, 특수 문자 등의 요구사항을 쉽게 설정할 수 있습니다:

```
// 최소 8자 이상...
Password::min(8)

// 글자 포함...
Password::min(8)->letters()

// 대문자, 소문자 모두 포함...
Password::min(8)->mixedCase()

// 숫자 포함...
Password::min(8)->numbers()

// 특수문자 포함...
Password::min(8)->symbols()
```

또한 `uncompromised` 메서드로 비밀번호가 공개된 데이터 유출 목록에 포함된 적 없는지 검사할 수 있습니다:

```
Password::min(8)->uncompromised()
```

내부에서는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 방식을 사용해 사용자의 개인정보를 유출하지 않고 [haveibeenpwned.com](https://haveibeenpwned.com)에서 공개된 비밀번호 여부를 체크합니다.

기본적으로 한 번 이상 데이터 유출에 포함된 비밀번호는 취약한 것으로 간주됩니다. 민감도를 조정하고 싶으면 `uncompromised`에 정수를 넘겨 설정할 수 있습니다:

```
// 한 데이터 유출에서 3회 미만만 허용...
Password::min(8)->uncompromised(3);
```

물론 위 모든 설정을 메서드 체이닝으로 결합할 수 있습니다:

```
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의

애플리케이션 한 곳에 기본 비밀번호 검증 규칙을 정의하는 것이 편리할 수 있습니다. `Password::defaults` 메서드를 이용하면 됩니다. `defaults`는 클로저를 받으며, 이 클로저는 기본 비밀번호 규칙 객체를 반환해야 합니다. 보통 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다:

```php
use Illuminate\Validation\Rules\Password;

/**
 * 애플리케이션 서비스 부트스트랩
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

기본 규칙을 적용할 때는 `defaults` 메서드를 인수 없이 호출하면 됩니다:

```
'password' => ['required', Password::defaults()],
```

추가 규칙을 붙이려면 `rules` 메서드를 사용하세요:

```
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 커스텀 검증 규칙

<a name="using-rule-objects"></a>
### Rule 객체 사용하기

Laravel은 다양한 내장 검증 룰을 제공하지만, 직접 규칙을 만들어야 할 수도 있습니다. `make:rule` Artisan 명령어로 규칙 객체를 생성할 수 있습니다. 예를 들어 문자열이 대문자인지 확인하는 룰을 만들어 보겠습니다. 이 룰 객체는 `app/Rules` 디렉터리에 생성됩니다. 해당 디렉터리가 없으면 자동 생성됩니다:

```shell
php artisan make:rule Uppercase
```

생성된 룰 객체는 `validate` 메서드를 포함합니다. 이 메서드는 속성명, 값, 실패 시 호출할 콜백을 받습니다:

```
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * 검증 로직 실행.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

정의 완료 후에는 다른 검증 규칙과 함께 이 룰 객체 인스턴스를 배열에 포함해 사용할 수 있습니다:

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 번역 메시지 활용하기

실제 문자 메시지 대신 [번역 문자열 키](/docs/11.x/localization)를 쓸 수도 있습니다:

```
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하면 플레이스홀더 치환과 언어를 인자로 넣을 수 있습니다:

```
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

검증 대상 전체 데이터에 룰에서 접근하려면, `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하고 `setData` 메서드를 정의하세요. Laravel은 검증 시작 전에 데이터를 자동으로 설정합니다:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * 검증 데이터 전체.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * 검증 대상 데이터 설정.
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

Validator 인스턴스에도 접근이 필요한 경우 `ValidatorAwareRule` 인터페이스를 구현하세요:

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * 현재 Validator 인스턴스.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Validator 인스턴스 설정.
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

커스텀 룰이 단 한 번만 필요하다면, 룰 객체 대신 클로저를 쓸 수도 있습니다. 클로저는 속성명, 값, 실패 시 호출할 `$fail` 콜백을 인수로 받습니다:

```
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
### 암묵적 규칙

기본적으로 검증할 속성이 존재하지 않거나 빈 문자열이면 기본 규칙과 커스텀 룰 모두 실행되지 않습니다. 예를 들어 [`unique`](#rule-unique) 룰은 빈 문자열에 대해 검증하지 않습니다:

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

암묵적 룰로 만들려면 `make:rule` Artisan 명령어에 `--implicit` 옵션을 붙여 생성하세요:

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]  
> 암묵적 룰은 "필수"임을 암시할 뿐, 실제로는 누락되거나 빈 값에 대해 유효성 검사를 할지는 직접 구현에 따라 다릅니다.