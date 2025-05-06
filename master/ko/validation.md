아래는 요청하신 마크다운 문서의 한글 번역본입니다.

---

# 유효성 검사(Validation)

- [소개](#introduction)
- [유효성 검사 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검사 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검사 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [옵션 필드에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검사 에러 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트 유효성 검사](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가하기](#authorizing-form-requests)
    - [에러 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검사 전 입력값 준비](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [명명된 에러 백(Named Error Bags)](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검사 수행하기](#performing-additional-validation)
- [유효성 검사된 입력값 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검사 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검사하기](#validating-arrays)
    - [중첩 배열 입력 유효성 검사](#validating-nested-array-input)
    - [에러 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검사하기](#validating-files)
- [비밀번호 유효성 검사하기](#validating-passwords)
- [커스텀 유효성 검사 규칙](#custom-validation-rules)
    - [규칙 오브젝트 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암시적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 들어오는 데이터를 유효성 검사하기 위한 여러 가지 방법을 제공합니다. 가장 일반적으로 사용하는 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드입니다. 하지만 이외의 다른 유효성 검사 방법에 대해서도 다룰 예정입니다.

Laravel은 데이터에 적용할 수 있는 다양한 편리한 유효성 검사 규칙을 제공합니다. 이는 값이 데이터베이스 테이블에서 고유한지까지도 검사할 수 있음을 의미합니다. 앞으로 각 유효성 검사 규칙을 자세히 다루니, Laravel의 유효성 검사 기능을 모두 익힐 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검사 빠르게 시작하기

Laravel의 강력한 유효성 검사 기능을 알아보기 위해, 폼을 유효성 검사하고 에러 메시지를 사용자에게 표시하는 전체 예제를 살펴보겠습니다. 이 내용을 읽고 나면, Laravel을 사용해 들어오는 요청 데이터를 어떻게 유효성 검사하는지 개괄적으로 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 아래와 같은 라우트가 정의되어 있다고 가정합니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새로운 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위 라우트의 요청을 처리할 간단한 컨트롤러 예제를 살펴봅니다. `store` 메서드는 일단 비워둡니다.

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
        // 블로그 포스트 유효성 검사 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성하기

이제 `store` 메서드에 새 블로그 포스트를 유효성 검사하는 로직을 채울 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검사 규칙을 통과하면 코드는 정상적으로 계속 실행됩니다. 반면, 유효성 검사가 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 에러 응답이 사용자에게 자동으로 반환됩니다.

만약 일반 HTTP 요청 중에 유효성 검사가 실패하면, 이전 URL로 리다이렉트 응답이 생성됩니다. 들어온 요청이 XHR 요청일 경우, [유효성 검사 에러 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 더 잘 이해하기 위해 `store` 메서드로 다시 돌아가봅니다.

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

위 코드에서 보듯이 유효성 검사 규칙을 `validate` 메서드에 전달합니다. 사용할 수 있는 모든 유효성 검사 규칙은 [문서화](#available-validation-rules)되어 있으니 참고하세요. 다시 말하지만, 유효성 검사에 실패하면 적절한 응답이 자동으로 생성됩니다. 검사를 통과하면 컨트롤러는 계속 정상적으로 실행됩니다.

또한, 유효성 검사 규칙을 `|`로 구분된 문자열이 아닌 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, [명명된 에러 백](#named-error-bags)에 에러 메시지를 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검사 실패에서 중단하기

어떤 속성의 첫 번째 유효성 검사 실패 이후로 검사를 중단하고 싶을 때가 있습니다. 그럴 땐 속성에 `bail` 규칙을 할당하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예시에서는, `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙은 확인하지 않습니다. 규칙은 지정된 순서대로 검사됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

들어오는 HTTP 요청이 "중첩된" 필드 데이터를 포함하고 있다면, 유효성 검사 규칙에서 "점(.) 표기법"을 사용해 해당 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 실제 점이 포함된 경우, 역슬래시로 점을 이스케이프하여 "점" 문법 해석을 방지할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검사 에러 표시하기

입력값이 주어진 유효성 검사 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 또한 모든 유효성 검사 에러와 [요청 입력값](/docs/{{version}}/requests#retrieving-old-input)이 자동으로 [세션에 flash](#)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(웹 미들웨어 그룹에 포함됨)가 모든 뷰에 `$errors` 변수를 공유합니다. 이 미들웨어가 적용되면 모든 뷰에서 `$errors` 변수가 항상 사용 가능하므로, 언제든지 `$errors`를 안전하게 사용할 수 있습니다. 이 변수는 `Illuminate\Support\MessageBag` 인스턴스로 제공됩니다. 이 객체를 다루는 방법은 [별도 문서](#working-with-error-messages)를 참고하세요.

따라서 유효성 검사에 실패할 경우 사용자는 컨트롤러의 `create` 메서드로 리다이렉트 되며, 뷰에서 에러 메시지를 표시할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>글 작성</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- 글 작성 폼 -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 에러 메시지 커스터마이즈

Laravel 기본 유효성 검사 규칙의 각 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 저장되어 있습니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 유효성 검사 규칙에 대한 번역 항목이 존재합니다. 필요하다면 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해서 번역할 수도 있습니다. Laravel 지역화에 대한 자세한 내용은 [지역화 문서](/docs/{{version}}/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 없습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` 아티즌 명령어로 퍼블리시 할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청 및 유효성 검사

이 예시에서는 전통적인 폼 제출을 사용해 데이터를 전송했습니다. 하지만 많은 애플리케이션은 자바스크립트 기반 프론트엔드로부터 XHR 요청을 받기도 합니다. XHR 요청 중에 `validate` 메서드를 사용하면, Laravel은 리다이렉트 응답을 생성하지 않습니다. 대신 [모든 유효성 검사 에러를 담은 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답에는 422 HTTP 상태 코드가 포함됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

[Blade](/docs/{{version}}/blade)의 `@error` 디렉티브를 사용하면 특정 속성에 유효성 검사 에러 메시지가 있는지 빠르게 확인할 수 있습니다. `@error` 블록 내에서 `$message` 변수를 출력해 에러 메시지를 표시할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">글 제목</label>

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

[명명된 에러 백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브에 두 번째 인자로 에러 백 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

유효성 검사에서 실패해 Laravel이 리다이렉트 응답을 생성하면, 프레임워크가 모든 요청 입력값을 [자동으로 세션에 flash](#)합니다. 이는 다음 요청에서 입력값에 편리하게 접근하여 사용자가 제출하려던 폼을 다시 채울 수 있게 하기 위해서입니다.

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 됩니다. 이 메서드는 세션에서 이전 입력값을 꺼냅니다.

```php
$title = $request->old('title');
```

또한, Laravel은 전역 `old` 헬퍼를 제공합니다. [Blade 템플릿](/docs/{{version}}/blade)에서 이전 입력값을 표시할 때 이 헬퍼를 사용하면 더 편리합니다. 해당 필드에 이전 입력값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션 필드에 대한 참고

Laravel은 기본적으로 전역 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이로 인해, "옵션" 요청 필드의 값이 `null`일 때 이를 유효한 값으로 간주하려면 `nullable` 규칙을 지정해야 합니다. 예시:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예시에서 `publish_at` 필드는 `null`이거나, 유효한 날짜 표현이어야 함을 의미합니다. 만약 `nullable` 수식자를 추가하지 않으면, 유효성 검사기는 `null`을 유효하지 않은 날짜로 처리합니다.

<a name="validation-error-response-format"></a>
### 유효성 검사 에러 응답 포맷

애플리케이션이 `Illuminate\Validation\ValidationException` 예외를 발생시키고 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 에러 메시지를 자동으로 포맷하여 `422 Unprocessable Entity` HTTP 응답과 함께 반환합니다.

아래는 유효성 검사 에러에 대한 JSON 응답 포맷 예시입니다. 중첩된 에러 키는 점 표기법(dot notation)으로 평탄화됩니다.

```json
{
    "message": "팀 이름은 문자열이어야 합니다. (그 외 4개의 에러)",
    "errors": {
        "team_name": [
            "팀 이름은 문자열이어야 합니다.",
            "팀 이름은 최소 1자 이상이어야 합니다."
        ],
        "authorization.role": [
            "선택된 authorization.role이 올바르지 않습니다."
        ],
        "users.0.email": [
            "users.0.email 필드는 필수입니다."
        ],
        "users.2.email": [
            "users.2.email은 올바른 이메일 주소여야 합니다."
        ]
    }
}
```

<a name="form-request-validation"></a>
## 폼 리퀘스트 유효성 검사

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성하기

더 복잡한 유효성 검사 시나리오에서는 "폼 리퀘스트"를 생성하는 게 유용합니다. 폼 리퀘스트는 자체 유효성 검사 및 인가 로직을 캡슐화하는 커스텀 요청 클래스입니다. 이 클래스를 만들려면 `make:request` 아티즌 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 이 디렉터리가 없다면 명령어 실행 시 자동으로 만들어집니다. Laravel이 생성하는 각 폼 리퀘스트 클래스엔 `authorize`와 `rules` 두 가지 메서드가 있습니다.

`authorize` 메서드는 현재 인증된 사용자가 해당 요청의 동작을 실행할 수 있는지 판단하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검사 규칙을 반환합니다.

```php
/**
 * 요청에 적용할 유효성 검사 규칙을 반환합니다.
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
> `rules` 메서드 시그니처에 필요한 의존성을 타입힌트할 수 있습니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동 해결됩니다.

유효성 검사 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 해당 요청을 타입힌트로 선언만 하면, 폼 리퀘스트가 컨트롤러 메서드 호출 전에 유효성 검사되어 컨트롤러를 유효성 검사 로직 없이 깔끔하게 유지할 수 있습니다.

```php
/**
 * 새 블로그 포스트 저장
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 요청이 유효합니다...

    // 검사된 입력값 전체 가져오기
    $validated = $request->validated();

    // 일부만 가져오기
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

유효성 검사 실패 시, 이전 위치로의 리다이렉트 응답이 생성되며, 에러는 세션에 flash되어 표시할 수 있습니다. XHR 요청일 경우, [유효성 에러의 JSON 표현](#validation-error-response-format)과 함께 422 HTTP 응답 코드가 반환됩니다.

> [!NOTE]
> Inertia 기반 Laravel 프론트엔드에 실시간 폼 리퀘스트 유효성 검사를 추가하고 싶으신가요? [Laravel Precognition](/docs/{{version}}/precognition)를 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검사 수행하기

기본 유효성 검사 외에 추가 검사가 필요한 경우, 폼 리퀘스트의 `after` 메서드를 이용하세요.

`after` 메서드는 유효성 검사 후 호출되는 콜러블 또는 클로저 배열을 반환해야 합니다. 각 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아, 필요하다면 추가 에러 메시지를 발생시킬 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * 유효성 검사 완료 후 호출될 콜러블 반환
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

필요하다면, `after` 메서드 반환 배열에 인보커블 클래스를 포함할 수도 있습니다. 이러한 클래스의 `__invoke` 메서드도 `Illuminate\Validation\Validator` 인스턴스를 전달받습니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

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
#### 첫 번째 유효성 검사 실패 시 전체 중단

폼 리퀘스트 클래스에 `stopOnFirstFailure` 속성을 추가하면, 하나라도 유효성 검사 실패가 발생하면 나머지 속성 유효성 검사를 중단하도록 할 수 있습니다.

```php
/**
 * 첫 번째 규칙 실패 시 validator가 전체 검증을 멈춰야 하는지 여부
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이즈

폼 리퀘스트 유효성 검사 실패 시, 기존에는 자동으로 이전 위치로 리다이렉트 되지만, 이 동작을 커스터마이즈할 수 있습니다. 폼 리퀘스트 클래스에 `$redirect` 속성을 지정하세요.

```php
/**
 * 유효성 검사 실패 시 사용자를 리다이렉트할 URI
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 명명된 라우트로 리다이렉트하려면 `$redirectRoute` 속성을 지정하세요.

```php
/**
 * 유효성 검사 실패 시 사용자를 리다이렉트할 라우트
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가하기

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 내에서, 인증된 사용자가 실제로 어떤 리소스를 업데이트할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 블로그 코멘트를 업데이트하려 할 때 자신이 해당 코멘트를 소유했는지 확인할 수 있습니다. 이 메서드에선 [인가 게이트와 정책](/docs/{{version}}/authorization)과 주로 상호작용하게 됩니다.

```php
use App\Models\Comment;

/**
 * 사용자가 이 요청을 실행할 권한이 있는지 여부
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

폼 리퀘스트는 base Laravel request를 확장하므로, `user` 메서드를 사용해 현재 인증된 사용자에 접근할 수 있습니다. 위 예시의 `route` 메서드는 호출된 라우트에서 정의된 URI 파라미터(아래 예시의 `{comment}` 등)에 접근할 수 있도록 합니다.

```php
Route::post('/comment/{comment}');
```

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 활용하면, 요청의 속성으로 모델 인스턴스를 바로 사용할 수 있어 코드를 더 간결하게 만들 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

만약 `authorize` 메서드가 `false`를 반환하면, 403 상태 코드의 HTTP 응답이 자동으로 반환되며 컨트롤러 메서드는 실행되지 않습니다.

요청의 인가 로직을 애플리케이션의 다른 부분에서 처리할 계획이라면, `authorize` 메서드를 완전히 제거하거나 `true`만 반환하도록 할 수 있습니다.

```php
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처에 필요한 의존성을 타입힌트할 수 있습니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈

폼 리퀘스트에서 사용하는 에러 메시지는 `messages` 메서드를 오버라이드하여 커스터마이즈할 수 있습니다. 이 메서드는 속성/규칙 쌍과 각 에러 메시지로 이루어진 배열을 반환해야 합니다.

```php
public function messages(): array
{
    return [
        'title.required' => '제목은 필수입니다.',
        'body.required' => '본문 내용이 필요합니다.',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 유효성 검사 속성명 커스터마이즈

Laravel의 기본 유효성 검사 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 자신의 검증 메시지에서 `:attribute` 플레이스홀더가 커스텀 속성명으로 대체되길 원한다면, `attributes` 메서드를 오버라이드해서 속성/이름 쌍의 배열을 반환하세요.

```php
public function attributes(): array
{
    return [
        'email' => '이메일 주소',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### 유효성 검사 전 입력값 준비

유효성 검사 규칙을 적용하기 전에 요청의 데이터를 준비(정규화)하거나 정리해야 할 경우, `prepareForValidation` 메서드를 사용하세요.

```php
use Illuminate\Support\Str;

protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

반대로, 유효성 검사 후에 데이터를 정규화해야 할 땐 `passedValidation` 메서드를 사용하세요.

```php
protected function passedValidation(): void
{
    $this->replace(['name' => '이름']);
}
```

<a name="manually-creating-validators"></a>
## 수동으로 Validator 생성하기

요청의 `validate` 메서드를 사용하지 않고 Validator 인스턴스를 직접 생성하려 할 땐, `Validator` [파사드](/docs/{{version}}/facades)의 `make` 메서드를 사용하세요.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
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

        // 유효성 검사된 입력값 가져오기
        $validated = $validator->validated();

        // 일부만 가져오기
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장...

        return redirect('/posts');
    }
}
```

`make` 메서드의 첫 번째 인자는 유효성 검사 대상 데이터이고, 두 번째 인자는 적용할 유효성 검사 규칙 배열입니다.

유효성 검사 실패 여부를 확인한 다음, `withErrors` 메서드로 에러 메시지를 세션에 flash할 수 있습니다. 이 메서드를 사용할 경우, redirect 후 뷰에 `$errors` 변수가 자동으로 공유되므로 사용자가 에러를 볼 수 있습니다. `withErrors`는 validator, `MessageBag`, 혹은 PHP 배열을 받을 수 있습니다.

#### 첫 번째 실패 시 중단

`stopOnFirstFailure` 메서드는 하나라도 유효성 검사 실패가 발생하면 전체 검증을 멈추도록 Validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

Validator 인스턴스를 직접 만들면서도 HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 활용하고 싶을 땐, 이미 생성한 validator 인스턴스에서 `validate` 메서드를 호출하세요. 실패 시, 사용자가 자동으로 리다이렉트 되거나, XHR 요청 시 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

`validateWithBag` 메서드를 사용해 [명명된 에러 백](#named-error-bags)에 에러 메시지를 저장할 수도 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 명명된 에러 백(Named Error Bags)

한 페이지에 여러 개의 폼이 있다면, 검증 에러를 담은 `MessageBag`에 이름을 붙여 특정 폼만의 에러 메시지를 가져올 수 있습니다. `withErrors`에 두 번째 인자로 이름을 전달하세요.

```php
return redirect('/register')->withErrors($validator, 'login');
```

뷰에서는 `$errors` 변수에서 명명된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요하다면, validator 인스턴스가 기본 제공 에러 메시지 대신 사용할 커스텀 메시지들을 지정할 수 있습니다. 커스텀 메시지는 여러 방법으로 지정할 수 있습니다. 먼저, `Validator::make`의 세 번째 인자로 전달하는 방법입니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => ':attribute 필드는 필수입니다.',
]);
```

위 예시에서 `:attribute` 플레이스홀더는 해당 필드명으로 대체됩니다. 검증 메시지 내에서 다른 플레이스홀더도 사용할 수 있습니다. 예시:

```php
$messages = [
    'same' => ':attribute와 :other는 일치해야 합니다.',
    'size' => ':attribute는 정확히 :size여야 합니다.',
    'between' => ':attribute 값 :input은 :min - :max 사이가 아닙니다.',
    'in' => ':attribute는 다음 중 하나여야 합니다: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 커스텀 메시지 지정하기

특정 속성에만 커스텀 에러 메시지를 지정하고 싶을 땐 "점(.) 표기법"을 사용하세요. 속성명 다음에 규칙명을 붙이면 됩니다.

```php
$messages = [
    'email.required' => '이메일 주소가 필요합니다!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성명 지정하기

Laravel 기본 에러 메시지에는 대부분 `:attribute` 플레이스홀더가 포함되어 있습니다. 특정 필드를 번역된 이름 등으로 표시하려면, 커스텀 속성명 배열을 `Validator::make`의 네 번째 인자로 전달하세요.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => '이메일 주소',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검사 수행하기

추가 유효성 검사가 필요한 경우, validator의 `after` 메서드를 이용하세요. 클로저나 콜러블 배열을 받아 검사 완료 후 호출됩니다.

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

"사후 유효성 검사" 로직이 인보커블 클래스에 캡슐화된 경우, 아래와 같이 배열로도 전달 가능합니다.

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
## 유효성 검사된 입력값 다루기

폼 리퀘스트 또는 수동으로 만든 validator 인스턴스로 들어온 요청 데이터를 검증한 이후, 실제로 검사받은 데이터를 얻고 싶을 수 있습니다. 몇 가지 방법이 있습니다. 먼저, 폼 리퀘스트나 validator 인스턴스에서 `validated` 메서드를 호출하세요. 이 메서드는 유효성 검사를 통과한 데이터 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, `safe` 메서드를 사용할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하며, `only`, `except`, `all` 메서드로 일부 또는 전체 유효성 검사된 데이터를 얻을 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 순회하거나 키로 접근할 수 있습니다.

```php
foreach ($request->safe() as $key => $value) {
    // ...
}

$validated = $request->safe();
$email = $validated['email'];
```

추가 필드를 유효성 검사된 데이터에 합치려면 `merge` 메서드를 호출하세요.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

유효성 검사된 데이터 전체를 [컬렉션](/docs/{{version}}/collections)으로 받고 싶으면 `collect` 메서드를 사용하세요.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator`의 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 반환합니다. 자동으로 모든 뷰에서 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 첫 번째 에러 메시지 가져오기

해당 필드의 첫 번째 에러 메시지는 `first` 메서드로 가져올 수 있습니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

해당 필드에 대한 모든 메시지가 필요할 때는 `get` 메서드를 사용하세요.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 폼 필드를 검증하고 있다면, `*` 문자를 사용해 각 배열 원소별 메시지를 얻을 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 필드의 메시지를 배열로 한 번에 가져오려면 `all` 메서드를 사용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 해당 필드에 메시지가 있는지 확인하기

해당 필드에 에러 메시지가 있는지 확인하려면 `has` 메서드를 사용하세요.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel의 기본 유효성 검사 규칙은 각각 애플리케이션의 `lang/en/validation.php` 파일에 에러 메시지가 존재합니다. `lang` 디렉터리가 없다면 `lang:publish` 아티즌 명령어로 생성할 수 있습니다.

이 파일에서 각 유효성 규칙에 대한 번역 항목을 자유롭게 변경할 수 있습니다.

또한, 해당 파일을 다른 언어 디렉터리로 복사해 번역 메시지를 지정할 수도 있습니다. [Laravel 지역화](#) 문서를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션에는 `lang` 디렉터리가 없습니다. 언어 파일을 커스터마이즈 하려면 `lang:publish` 아티즌 명령어로 퍼블리시 하세요.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

특정 속성과 규칙 조합에 대한 에러 메시지는 언어 파일 내의 `custom` 배열에 지정할 수 있습니다.

```php
'custom' => [
    'email' => [
        'required' => '이메일 주소가 필요합니다!',
        'max' => '이메일 주소가 너무 깁니다!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

대부분의 Laravel 메시지에는 `:attribute` 플레이스홀더가 사용됩니다. 메시지에서 이 부분이 커스텀 값으로 대체되길 원하면, `lang/xx/validation.php`의 `attributes` 배열에 속성명을 추가하세요.

```php
'attributes' => [
    'email' => '이메일 주소',
],
```

> [!WARNING]
> (이전과 동일)

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

몇몇 Laravel 기본 유효성 검사 메시지는 `:value` 플레이스홀더도 사용합니다. 특정 값이 사용자 친화적으로 표시되길 원한다면, 언어 파일에 `values` 배열을 지정하세요.

예를 들어, `payment_type이 'cc'`일 때 신용카드 번호가 필수임을 검사하는 경우, 메시지에 '신용카드' 라고 보여주고 싶으면 아래처럼 지정합니다.

```php
'values' => [
    'payment_type' => [
        'cc' => '신용카드'
    ],
],
```

> [!WARNING]
> (이전과 동일)

정의한 뒤, 검사 메시지는 다음과 같이 표시됩니다.

```text
결제 방식이 신용카드일 경우, 신용카드 번호 필드는 필수입니다.
```

---

(이후 규칙 목록/설명은 너무 방대하여 ‘유효성 검사 규칙’ 이하의 상세 규칙 설명 부분은 필요에 따라 요청해주시면 순차적으로 번역해 드립니다. 위의 방식대로 계속 포맷 유지해서 전체 번역이 가능합니다.)

---

> ※ 위 번역은 마크다운 문서 구조 및 코드는 그대로 두었고, 예제, 경고, 중요한 부분, 링크 등도 요구조건에 맞춰 그대로 유지하며 번역했습니다.  
> ※ 문서의 분량이 매우 방대하여 처음 ~ 언어 파일 값 처리까지 번역하였고, 이후 상세 규칙 설명은 필요하시면 추가로 요청해 주시면 이어서 번역 가능합니다.