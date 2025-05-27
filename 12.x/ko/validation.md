# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [선택 입력 필드에 대한 안내](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가 처리](#authorizing-form-requests)
    - [오류 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검증 전 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 Validator 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [네임드 에러 백(Error Bag) 사용](#named-error-bags)
    - [오류 메시지 커스터마이즈](#manual-customizing-the-error-messages)
    - [추가적인 유효성 검증 수행](#performing-additional-validation)
- [유효성 검증된 입력값 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성명 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 데이터 유효성 검증](#validating-arrays)
    - [중첩 배열 입력값 검증하기](#validating-nested-array-input)
    - [오류 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [Implicit 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션으로 들어오는 데이터를 유효성 검증하기 위한 여러 가지 방법을 제공합니다. 가장 일반적으로는 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 활용합니다. 하지만 이 외에도 다양한 유효성 검증 방법이 있으니, 이 문서에서 모두 다룰 예정입니다.

라라벨에는 데이터에 적용할 수 있는 다양한 편리한 유효성 검증 규칙이 기본 제공되며, 특정 데이터베이스 테이블의 값이 고유(uniq)한지 확인하는 등의 검증도 할 수 있습니다. 이 문서에서는 각 유효성 검증 규칙에 대해 자세히 다룰 예정이니, 라라벨의 모든 유효성 검증 기능에 익숙해질 수 있습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작

라라벨의 강력한 유효성 검증 기능을 이해하기 위해, 폼 입력값을 검증하고 그 결과를 사용자에게 보여주는 전체 예시를 살펴보겠습니다. 이 고수준 개요를 통해 라라벨에서 들어오는 요청 데이터에 대해 어떻게 유효성 검증을 적용하는지 감을 잡을 수 있을 것입니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 아래와 같은 라우트가 정의되어 있다고 가정하겠습니다:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

여기서 `GET` 라우트는 사용자가 새로운 블로그 포스트를 만들 수 있는 폼을 보여주고, `POST` 라우트는 실제로 새 블로그 포스트를 데이터베이스에 저장하는 역할을 합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위 라우트를 처리하는 간단한 컨트롤러 예시를 살펴보겠습니다. 여기서는 일단 `store` 메서드는 비워두었습니다.

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
     * 새 블로그 포스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 포스트를 유효성 검증 후 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 새 블로그 포스트를 저장하기 위한 `store` 메서드에 유효성 검증 로직을 작성해봅시다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용할 수 있습니다. 유효성 검증 규칙을 모두 통과하면 코드가 정상적으로 계속 실행되고, 규칙을 통과하지 못 하면 `Illuminate\Validation\ValidationException` 예외가 발생하여 적절한 오류 응답이 자동으로 사용자에게 전송됩니다.

일반적인 HTTP 요청에서 유효성 검증에 실패하면, 이전 URL로 리다이렉션됩니다. 만약 들어온 요청이 XHR 요청이라면, [유효성 검증 오류 메시지를 담은 JSON 응답](#validation-error-response-format)이 반환됩니다.

이제 다시 `store` 메서드로 돌아가서 `validate` 메서드가 어떻게 동작하는지 보겠습니다:

```php
/**
 * 새 블로그 포스트 저장.
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

보시다시피, 유효성 검증 규칙들을 `validate` 메서드에 전달해주고 있습니다. 걱정하지 마세요. 사용 가능한 모든 유효성 검증 규칙은 [문서화되어 있습니다](#available-validation-rules). 다시 한 번 말씀드리지만, 유효성 검증에 실패하면 적절한 응답이 자동으로 생성됩니다. 검증이 통과하면, 컨트롤러는 정상적으로 계속 실행됩니다.

또한, 유효성 검증 규칙을 `|`(파이프)로 구분된 문자열 대신 배열 형태로 지정할 수도 있습니다:

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

그리고, `validateWithBag` 메서드를 사용하면, [네임드 에러 백](#named-error-bags)에 오류 메시지를 저장하면서 요청을 검증할 수 있습니다:

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 실패 시 검증 중단하기

특정 속성(attribute)에 대해 첫 번째 유효성 검증 규칙에서 실패하면 이후 규칙 검사도 중단하게 하고 싶은 경우가 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다:

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서 `title` 필드의 `unique` 규칙이 실패하면 `max` 규칙은 검사하지 않습니다. 규칙들은 지정한 순서대로 평가됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 안내

들어오는 HTTP 요청이 "중첩된" 필드 데이터를 포함하는 경우, 유효성 검증 규칙에서 "닷(dot) 기법"을 사용하여 해당 필드를 지정할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드명이 실제로 점(.)을 포함하는 경우에는 백슬래시(`\`)로 점을 이스케이프 처리하여 "닷 문법"으로 인식되는 것을 방지할 수 있습니다:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시하기

그렇다면, 폼 입력값이 주어진 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯이, 라라벨은 자동으로 사용자를 이전 위치로 리다이렉션합니다. 그리고 모든 유효성 검증 오류와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 [세션에 플래시](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 모든 뷰에서 `$errors` 변수를 사용할 수 있게 해주며, 이는 `web` 미들웨어 그룹에 포함되어 있습니다. 이 미들웨어가 적용된 경우, 뷰 내에서 언제나 편리하게 `$errors` 변수를 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스이며, 관련 객체를 다루는 방법은 [해당 문서](#working-with-error-messages)에서 자세히 확인할 수 있습니다.

따라서, 예시에서는 유효성 검증에 실패하면 컨트롤러의 `create` 메서드로 리다이렉트되어, 뷰에서 오류 메시지를 표시할 수 있습니다:

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

라라벨 내장 유효성 검증 규칙들은 각각 에러 메시지를 `lang/en/validation.php` 파일 내에 저장하고 있습니다. 만약 애플리케이션 내에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 통해 해당 디렉터리를 생성할 수 있습니다.

`lang/en/validation.php` 파일 안에서는 각 유효성 검증 규칙에 대한 번역 메시지를 찾아볼 수 있습니다. 애플리케이션 필요에 따라 이 메시지들을 자유롭게 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해 해당 언어로 번역할 수도 있습니다. 라라벨의 로컬라이제이션에 대해 더 알고 싶다면 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하시기 바랍니다.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈 하고 싶다면, `lang:publish` Artisan 명령어를 통해 파일을 퍼블리시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청 및 유효성 검증

이 예시에서는 전통적인 폼을 통해 데이터를 전송했습니다. 하지만 실제 애플리케이션에서는 JavaScript 프론트엔드에서 XHR(비동기) 요청을 받는 경우가 많습니다. XHR 요청 중에 `validate` 메서드를 사용할 경우, 라라벨은 리다이렉트 응답을 생성하지 않습니다. 대신, 라라벨은 모든 유효성 검증 오류를 담은 [JSON 응답](#validation-error-response-format)을 반환하며, HTTP 상태 코드는 422로 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성(attribute)에 대한 유효성 검증 오류 메시지가 존재하는지를 빠르게 확인하려면, [Blade](/docs/12.x/blade)의 `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 내에서는 `$message` 변수를 출력해 오류 메시지를 표시할 수 있습니다:

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

[네임드 에러 백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인자로 에러 백의 이름을 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

유효성 검증 오류로 인해 라라벨이 리다이렉트 응답을 생성할 때, 프레임워크는 해당 요청의 모든 입력값을 자동으로 [세션에 플래시](/docs/12.x/session#flash-data)합니다. 이를 통해 사용자는 다음 요청에서 이전에 입력한 값을 쉽게 접근하고, 제출했던 폼을 다시 채울 수 있습니다.

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. 이 메서드는 [세션](/docs/12.x/session)에 저장된 입력 데이터를 반환합니다:

```php
$title = $request->old('title');
```

라라벨은 전역 헬퍼 함수 `old`도 제공합니다. [Blade 템플릿](/docs/12.x/blade) 내에서 이전 입력값을 표시할 때, 이 헬퍼를 쓰는 것이 더 편리합니다. 해당 필드에 대한 이전 입력값이 없다면, `null`이 반환됩니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 입력 필드에 대한 안내

기본적으로 라라벨은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 포함시킵니다. 그 결과, "선택(optional)" 요청 필드를 유효성 검증에서 무효로 처리하지 않으려면 해당 필드의 규칙에 `nullable`을 반드시 추가해야 합니다. 예를 들면:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위의 예시에서는 `publish_at` 필드가 `null`이거나 올바른 날짜 형식일 수 있음을 명시합니다. 만약 규칙 정의에 `nullable`을 추가하지 않으면, 검증기는 `null`도 올바른 날짜가 아니라고 판단하게 됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어온 HTTP 요청이 JSON 응답을 기대하는 경우, 라라벨은 오류 메시지를 자동으로 포맷하고 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래는 유효성 검증 오류에 대한 JSON 응답 포맷 예시입니다. 참고로, 중첩된 오류 키는 "dot" 형태로 평탄화되어 나타납니다:

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

더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(form request)"를 만들어 사용할 수 있습니다. 폼 리퀘스트는 자체적으로 유효성 검증과 인가(authorization) 로직을 캡슐화하는 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 만들려면, `make:request` Artisan CLI 명령어를 사용하세요:

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 만약 해당 디렉터리가 존재하지 않는다면, `make:request` 명령어 실행 시 자동으로 생성됩니다. 라라벨이 만들어주는 각 폼 리퀘스트에는 `authorize`와 `rules`라는 두 개의 메서드가 포함됩니다.

예상할 수 있듯이, `authorize` 메서드는 현재 인증된 사용자가 이 요청이 대표하는 동작을 실행할 수 있는지 판별하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다:

```php
/**
 * 요청에 적용될 유효성 검증 규칙을 반환합니다.
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
> `rules` 메서드의 시그니처에 어떤 의존성이든 타입힌트로 지정할 수 있습니다. 이들은 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 해결됩니다.

그렇다면 유효성 검증 규칙은 어떻게 적용될까요? 컨트롤러 메서드의 인자로 해당 폼 리퀘스트를 타입힌트만 해주면 됩니다. 이때, 컨트롤러 메서드가 실행되기 전에 폼 리퀘스트가 자동으로 검증되므로, 컨트롤러에 검증 로직을 별도로 작성할 필요가 없습니다.

```php
/**
 * 새 블로그 포스트 저장.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 들어온 요청은 이미 유효합니다...

    // 검증된 입력 데이터를 가져옵니다.
    $validated = $request->validated();

    // 일부 검증된 입력 데이터만 가져오기.
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트 저장...

    return redirect('/posts');
}
```

검증에 실패하면, 사용자를 이전 위치로 보내는 리다이렉트 응답이 생성됩니다. 오류도 세션에 플래시되어 화면에 표시할 수 있습니다. 만약 요청이 XHR 요청이었다면, 422 상태 코드와 함께 [유효성 검증 오류의 JSON 표현](#validation-error-response-format)이 사용자에게 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에서 실시간 폼 리퀘스트 유효성 검증이 필요하다면 [Laravel Precognition](/docs/12.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 폼 리퀘스트에서 추가 유효성 검증 수행하기

초기 유효성 검증이 완료된 후에 추가적인 검증이 필요할 때가 있습니다. 이럴 때는 폼 리퀘스트의 `after` 메서드를 이용하세요.

`after` 메서드는 유효성 검증이 끝난 뒤에 호출될 콜러블(callable) 또는 클로저의 배열을 반환해야 합니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아 필요한 경우 추가 오류 메시지를 등록할 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 추가 유효성 검증 콜러블을 반환합니다.
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

설명한 대로, `after` 메서드가 반환하는 배열에는 클래스를 인보커블(호출 가능) 형태로 포함시킬 수도 있습니다. 해당 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 추가 유효성 검증 콜러블을 반환합니다.
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

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하여, 한 번이라도 유효성 검증 실패가 발생하면 남은 모든 속성의 검증을 중단하도록 할 수 있습니다:

```php
/**
 * 첫 번째 규칙 실패 시 검증을 중단할지 여부를 나타냅니다.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이즈

폼 리퀘스트 유효성 검증에 실패하면, 기본적으로 사용자를 이전 위치로 리다이렉트합니다. 그러나 이 동작을 자유롭게 변경할 수 있습니다. 이를 위해 폼 리퀘스트에 `$redirect` 프로퍼티를 정의하세요:

```php
/**
 * 유효성 검증에 실패했을 때 사용자가 리다이렉트될 URI입니다.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 네임드 라우트로 리다이렉트하고 싶다면 `$redirectRoute` 프로퍼티를 대신 지정할 수 있습니다:

```php
/**
 * 유효성 검증에 실패했을 때 사용자가 리다이렉트될 라우트입니다.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가 처리

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 내에서는 인증된 사용자가 실제로 특정 리소스를 수정할 권한이 있는지 결정할 수 있습니다. 예를 들어, 사용자가 자기 자신의 블로그 댓글만 수정 가능하도록 하는 등입니다. 보통 이곳에서 [인가 게이트 또는 정책](/docs/12.x/authorization)과 연동하여 처리를 합니다:

```php
use App\Models\Comment;

/**
 * 해당 요청을 사용자가 수행할 수 있는지 여부를 판별합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 기본 라라벨 요청 클래스를 확장하므로, `user` 메서드를 이용하여 현재 인증된 사용자를 가져올 수 있습니다. 위 예시에서 `route` 메서드는 호출된 라우트에 정의된 URI 파라미터(예: `{comment}`)에 접근할 수 있게 해줍니다:

```php
Route::post('/comment/{comment}');
```

따라서, [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하고 있다면, 요청의 속성(property)으로 해결된 모델에 직접 접근하여 코드를 더 간결하게 만들 수 있습니다:

```php
return $this->user()->can('update', $this->comment);
```

만약 `authorize` 메서드가 `false`를 반환하면, 자동으로 403 상태 코드의 HTTP 응답이 반환되고, 컨트롤러 메서드는 실행되지 않습니다.

요청에 대한 인가 로직을 애플리케이션의 다른 부분에서 처리할 생각이라면, `authorize` 메서드를 아예 제거하거나, 단순히 `true`를 반환해도 됩니다:

```php
/**
 * 해당 요청을 사용자가 수행할 수 있는지 여부를 판별합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드의 시그니처에도 필요한 모든 의존성을 타입힌트로 지정할 수 있습니다. 이 의존성들은 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

폼 리퀘스트에서 사용하는 오류 메시지를 커스터마이즈하려면 `messages` 메서드를 오버라이드하면 됩니다. 이 메서드는 속성/규칙명과 그에 해당하는 오류 메시지가 담긴 배열을 반환해야 합니다:

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

라라벨의 내장 유효성 검증 오류 메시지 중에는 `:attribute` 플레이스홀더를 포함하는 경우가 많습니다. 오류 메시지의 `:attribute` 플레이스홀더를 사용자 지정 속성명으로 바꾸고 싶다면, `attributes` 메서드를 오버라이드하여 속성명 배열을 반환하세요:

```php
/**
 * Validator 오류에 대해 커스텀 속성명을 지정합니다.
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
### 유효성 검증 전 입력값 준비하기

유효성 검증을 적용하기 전에 요청 데이터 중 일부를 준비(정제, 보정)해야 할 경우, `prepareForValidation` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증을 위해 데이터를 준비합니다.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

마찬가지로, 유효성 검증이 끝난 이후에 요청 데이터를 정규화해야 할 경우, `passedValidation` 메서드를 사용할 수 있습니다:

```php
/**
 * 유효성 검증 통과 후의 처리를 담당합니다.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>

## 수동으로 Validator 인스턴스 생성하기

요청(Request) 객체의 `validate` 메서드를 사용하지 않고 직접 유효성 검사기(validator) 인스턴스를 생성하고 싶다면, `Validator` [파사드](/docs/12.x/facades)를 이용할 수 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

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

`make` 메서드의 첫 번째 인자는 유효성 검증할 데이터입니다. 두 번째 인자는 해당 데이터에 적용할 유효성 검증 규칙의 배열입니다.

요청 데이터의 유효성 검사가 실패했는지 확인한 뒤에는, `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 리다이렉트 이후 뷰에서 자동으로 `$errors` 변수를 사용할 수 있게 되며, 이를 통해 사용자가 에러 메시지를 쉽게 확인할 수 있습니다. `withErrors` 메서드는 validator 인스턴스, `MessageBag`, 또는 PHP 배열을 인자로 받을 수 있습니다.

#### 첫 번째 유효성 검사 실패 시 즉시 중단하기

`stopOnFirstFailure` 메서드를 사용하면, 유효성 검사 항목 중 첫 번째 실패가 발생하는 즉시 모든 검증을 중단하도록 validator에 알릴 수 있습니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

수동으로 validator 인스턴스를 생성하면서도 HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 활용하고 싶다면, 기존 validator 인스턴스에서 `validate` 메서드를 호출할 수 있습니다. 유효성 검증에 실패할 경우, 사용자는 자동으로 리다이렉트되거나, XHR 요청일 경우에는 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

유효성 검증에 실패했을 때 에러 메시지를 [이름이 지정된 에러 컬렉션(error bag)](#named-error-bags)에 저장하려면, `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 에러 컬렉션(error bag) 이름 지정하기

한 페이지에 폼이 여러 개 있을 때, 유효성 검증 에러를 담는 `MessageBag`에 이름을 붙여 각 폼에 관련된 에러 메시지를 구분하여 사용할 수 있습니다. 이를 위해 `withErrors` 메서드의 두 번째 인자로 이름을 지정해 전달합니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이후 뷰에서는 `$errors` 변수에서 지정한 이름의 `MessageBag` 인스턴스를 확인할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 직접 지정하기

필요하다면, Laravel이 기본적으로 제공하는 에러 메시지 대신 validator 인스턴스에서 사용할 커스텀 메시지를 직접 지정할 수 있습니다. 커스텀 메시지를 지정하는 방법은 여러 가지가 있으며, 가장 간단하게는 `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지 배열을 전달하면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예시에서 `:attribute` 플레이스홀더는 실제로 유효성 검사 대상 필드의 이름으로 치환됩니다. 이 밖에도 다양한 플레이스홀더를 메시지에서 활용할 수 있습니다. 예를 들어:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 필드에 대한 커스텀 메시지 지정

특정 필드에만 커스텀 메시지를 지정하고 싶을 때는 "점 표기법(dot notation)"을 사용합니다. 필드명 뒤에 검증 규칙명을 붙여서 선언합니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 필드명에 대한 커스텀 치환 값 지정

Laravel의 기본 에러 메시지에는 `:attribute` 플레이스홀더가 자주 사용되며, 이는 유효성 검사 대상 필드명으로 대체됩니다. 특정 필드에 대해 이 치환 값(표시될 이름)을 변경하고 싶을 때는, `Validator::make`의 네 번째 인자로 커스텀 특성 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행하기

경우에 따라, 기본적인 유효성 검사 이후 추가적인 검증을 수행해야 할 수 있습니다. 이때 validator의 `after` 메서드를 사용하면 됩니다. `after`는 클로저(익명 함수) 또는 콜러블(callable)들의 배열을 받을 수 있으며, 본 유효성 검사 이후 호출됩니다. 이때 전달받는 인자는 `Illuminate\Validation\Validator` 인스턴스이므로, 필요한 경우 추가적인 에러 메시지를 등록할 수 있습니다.

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

앞서 언급한 것처럼, `after` 메서드는 콜러블의 배열도 받을 수 있습니다. 특히 "after validation" 로직을 인보커블 클래스(클래스의 `__invoke` 메서드를 구현)에 캡슐화해서 관리할 때 유용합니다. 이 클래스들 역시 `Illuminate\Validation\Validator` 인스턴스를 받게 됩니다.

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
## 유효성 검증 통과 데이터 다루기

폼 요청(form request) 또는 수동으로 생성한 validator 인스턴스를 통해 들어온 요청 데이터를 검증한 후에는 실제로 유효성 검사를 통과한 데이터만 별도로 추출할 수 있습니다. 이를 위해 여러 가지 방법을 사용할 수 있습니다. 가장 기본적으로, 폼 요청이나 validator 인스턴스에서 `validated` 메서드를 호출하면 검증된 데이터의 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 요청이나 validator 인스턴스에서 `safe` 메서드를 사용할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하며, 이 객체는 `only`, `except`, `all` 등을 통해 검증된 데이터의 일부 또는 전체를 추출할 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

`Illuminate\Support\ValidatedInput` 인스턴스는 반복문으로 순회하거나 배열처럼 접근할 수도 있습니다.

```php
// 검증된 데이터는 반복문으로 순회할 수 있습니다.
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근도 가능합니다.
$validated = $request->safe();

$email = $validated['email'];
```

또한, 검증된 데이터에 추가 필드를 더하고 싶다면, `merge` 메서드를 사용하면 됩니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 변환하려면, `collect` 메서드를 호출하세요.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 에러 메시지 관련 편의 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 얻을 수 있습니다. 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

특정 필드에 대해 첫 번째 에러 메시지를 가져오려면, `first` 메서드를 사용합니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드의 모든 에러 메시지 배열을 얻으려면, `get` 메서드를 사용합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 폼 필드를 검증할 때는, `*` 문자를 이용해 각 배열 요소의 에러 메시지도 모두 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드에 대한 모든 에러 메시지 가져오기

모든 필드와 관련된 모든 에러 메시지 배열을 얻으려면, `all` 메서드를 사용합니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지가 존재하는지 확인하기

`has` 메서드를 사용하면, 주어진 필드에 에러 메시지가 있는지 여부를 판단할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

Laravel의 내장 유효성 검증 규칙 각각에는 애플리케이션 `lang/en/validation.php` 파일에 해당 에러 메시지가 정의되어 있습니다. 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 통해 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각각의 검증 규칙에 대응하는 번역 항목이 있습니다. 이 메시지들은 애플리케이션의 요구사항에 맞게 자유롭게 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해 사용자의 언어에 맞는 메시지를 번역할 수도 있습니다. 라라벨의 지역화(localization) 사용 방법은 [로컬라이제이션 전체 문서](/docs/12.x/localization)에서 더 자세히 확인하실 수 있습니다.

> [!WARNING]
> 기본적으로 Laravel의 애플리케이션 스캐폴딩(skeleton)에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어로 해당 파일을 배포해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

애플리케이션의 유효성 검증 언어 파일에서, 특정 속성과 규칙 조합에 대한 커스텀 에러 메시지를 지정할 수 있습니다. 이를 위해 `lang/xx/validation.php` 언어 파일의 `custom` 배열에 메시지를 추가하세요.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성명 치환 값 지정

Laravel의 기본 에러 메시지에는 흔히 `:attribute` 플레이스홀더가 들어 있으며, 이는 검증 대상 필드명으로 치환됩니다. 이 부분을 커스텀 값으로 치환하고 싶다면, `lang/xx/validation.php` 파일 내 `attributes` 배열에 원하는 이름을 정의하세요.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel의 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어로 파일을 배포하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 치환 지정

일부 내장 유효성 검증 규칙 메시지에는 `:value` 플레이스홀더가 들어 있으며, 이는 현재 요청 속성의 값으로 치환됩니다. 그러나, 종종 이 값을 좀 더 알아보기 쉬운 형태로 바꿔서 표시하고 싶을 수 있습니다. 예를 들어, `payment_type`이 `cc`인 경우에만 신용카드 번호를 필수로 입력해야 하는 규칙을 고려해보세요.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 규칙이 실패하면 다음과 같은 에러 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

여기서 `cc`라는 값을 바로 보여주는 대신 좀 더 친절한 이름으로 표시하고 싶다면, `lang/xx/validation.php` 언어 파일에 `values` 배열을 정의하면 됩니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel의 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어로 파일을 배포하세요.

이렇게 하면, 해당 유효성 규칙 실패 시 에러 메시지는 다음과 같이 표시됩니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검사 규칙

아래는 사용 가능한 모든 유효성 검사 규칙과 각각이 수행하는 기능에 대한 목록입니다.



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

#### 기타 유틸리티

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

검증 대상 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 이는 "약관 동의"와 같은 필드를 검증할 때 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

검증 대상 필드는, 지정한 다른 필드가 특정 값과 일치할 경우 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 역시 "약관 동의" 등의 필드 검증에 주로 사용됩니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드에는 유효한 A 또는 AAAA 레코드가 있어야 하며, 이는 PHP의 `dns_get_record` 함수로 확인됩니다. 제공된 URL의 호스트명은 PHP의 `parse_url` 함수를 통해 추출되어 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드는 주어진 날짜 이후의 값이어야 합니다. 해당 날짜는 `strtotime` PHP 함수를 통해 유효한 `DateTime` 인스턴스로 변환됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`으로 평가할 날짜 문자열 대신, 비교할 다른 필드를 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

더 편리하게, 날짜 기반 규칙은 유창한(Fluent) `date` 규칙 빌더를 사용해 만들 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드를 활용하면, 날짜가 "오늘 이후" 또는 "오늘 포함 이후"임을 더욱 간결하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>

#### after_or_equal:_date_

유효성 검사가 적용되는 필드는 지정한 날짜 이후이거나 같은 날짜여야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하시기 바랍니다.

편의를 위해, 날짜 기반 규칙은 플루언트 `date` 규칙 빌더를 사용해 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검사 규칙을 사용하면 해당 필드가 제공된 여러 유효성 검사 규칙 집합 중 하나라도 충족해야 함을 지정할 수 있습니다. 예를 들어, 아래의 규칙은 `username` 필드가 이메일 주소이거나, 최소 6자 이상의 알파벳/숫자(대시 포함) 문자열임을 검사합니다.

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

유효성 검사가 적용되는 필드에는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 해당하는 유니코드 알파벳 문자만 포함되어야 합니다.

이 규칙을 ASCII 문자(`a-z`, `A-Z`)로 제한하려면, 아래와 같이 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

유효성 검사가 적용되는 필드에는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 알파벳 및 숫자 문자, 그리고 ASCII 대시(`-`), 언더스코어(`_`)만 포함되어야 합니다.

이 규칙을 ASCII 문자(`a-z`, `A-Z`, `0-9`)로 제한하려면, 아래와 같이 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

유효성 검사가 적용되는 필드에는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 알파벳 및 숫자 문자만 포함되어야 합니다.

이 규칙을 ASCII 문자(`a-z`, `A-Z`, `0-9`)로 제한하려면, 아래와 같이 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

유효성 검사가 적용되는 필드는 PHP의 `array` 타입이어야 합니다.

`array` 규칙에 추가 인자를 제공하면, 입력 배열의 각 키가 해당 인자 목록에 반드시 존재해야 합니다. 아래 예시에서 입력 배열의 `admin` 키는 `array` 규칙에 명시된 값 목록에 포함되지 않았으므로 유효하지 않습니다.

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

일반적으로, 배열 내에 허용할 키를 항상 명시적으로 지정하는 것이 좋습니다.

<a name="rule-ascii"></a>
#### ascii

유효성 검사가 적용되는 필드는 7비트 ASCII 문자로만 구성되어야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드의 유효성 검사에서 처음 실패가 발생하면, 이후의 나머지 유효성 검사를 모두 중단합니다.

`bail` 규칙은 특정 필드에서만 유효성 검사 실패 시 중단하지만, `stopOnFirstFailure` 메서드는 하나의 유효성 검사 실패가 발생하면 모든 속성의 검증을 즉시 중단하도록 합니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

유효성 검사가 적용되는 필드는 지정한 날짜 이전의 값이어야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 파싱되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 날짜 값에 유효성 검사 대상인 다른 필드의 이름을 지정할 수도 있습니다.

편의를 위해, 날짜 기반 규칙은 플루언트 `date` 규칙 빌더를 사용해 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`, `todayOrBefore` 메서드를 활용하여 "오늘 이전", "오늘 또는 이전" 날짜임을 좀 더 직관적으로 표현할 수도 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

유효성 검사가 적용되는 필드는 지정한 날짜 이전이거나 같은 날짜여야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 파싱되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 날짜 값에 유효성 검사 대상인 다른 필드의 이름을 지정할 수도 있습니다.

편의를 위해, 날짜 기반 규칙은 플루언트 `date` 규칙 빌더를 사용해 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

유효성 검사가 적용되는 필드는 지정한 _min_과 _max_ 사이(양 끝값 포함)의 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

해당 필드는 불린(boolean)로 형 변환이 가능해야 합니다. 허용되는 입력값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<a name="rule-confirmed"></a>
#### confirmed

유효성 검사가 적용되는 필드는 반드시 `{field}_confirmation`이라는 이름의 필드와 값이 일치해야 합니다. 예를 들어, 비밀번호 필드인 `password`의 유효성을 검사할 때는 반드시 입력 값에 `password_confirmation` 필드가 있어야 합니다.

사용자 정의 확인용 필드명을 지정할 수도 있습니다. 예를 들어 `confirmed:repeat_username`으로 지정하면, `repeat_username` 필드가 검사 대상 필드와 동일한지 검사하게 됩니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

해당 필드는 배열이어야 하며, 지정된 모든 매개변수 값들(`_foo_, _bar_, ...`)을 반드시 포함해야 합니다.

<a name="rule-current-password"></a>
#### current_password

유효성 검사가 적용되는 필드 값은 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 매개변수를 이용해 [인증 가드](/docs/12.x/authentication)를 지정할 수도 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

유효성 검사가 적용되는 필드는 PHP의 `strtotime` 함수 기준으로 올바른(상대적이지 않은) 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

해당 필드는 지정한 날짜와 동일해야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 파싱되어 유효한 `DateTime` 인스턴스로 변환됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

해당 필드는 지정한 _formats_ 중 하나와 일치해야 합니다. 날짜 값을 검증할 땐 반드시 `date` 또는 `date_format` 중 하나만 사용해야 하며, 두 규칙을 동시에 적용하면 안 됩니다. 이 규칙에서는 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 포맷을 사용할 수 있습니다.

편의를 위해, 날짜 기반 규칙은 플루언트 `date` 규칙 빌더를 사용해 작성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

해당 필드는 숫자여야 하며, 지정한 소수점 자릿수(개수)를 반드시 가져야 합니다.

```php
// 소수점 이하 자릿수가 정확히 2자리여야 함 (예: 9.99)...
'price' => 'decimal:2'

// 소수점 이하 자릿수가 2자리 이상 4자리 이하여야 함...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

해당 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 값 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

한 필드의 값이 지정된 값과 일치할 때, 해당 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

해당 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

해당 필드는 정확히 _value_ 자리의 정수여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

해당 필드는 _min_자리 이상, _max_자리 이하의 정수여야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

해당 파일은 규칙의 파라미터로 지정된 이미지 크기 제약 조건을 만족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건은: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_ 입니다.

_ratio_ 제약 조건은 너비/높이의 비율로, 분수(`3/2`)나 실수(`1.5`)로 표현할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

이 규칙은 여러 인자를 활용하므로, `Rule::dimensions` 메서드를 사용하여 규칙을 플루언트하게 작성하는 것이 훨씬 편리합니다.

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

배열을 검증할 때, 해당 필드 내에 중복된 값이 없어야 합니다.

```php
'foo.*.id' => 'distinct'
```

`distinct`는 기본적으로 느슨한(loosely) 값 비교를 사용합니다. 엄격한(strict) 비교를 사용하려면 `strict` 파라미터를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 구분 없이 비교하려면 `ignore_case` 인자를 추가하면 됩니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

해당 필드는 지정한 값들 중 하나로 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

해당 필드는 지정한 값들 중 하나로 끝나서는 안 됩니다.

<a name="rule-email"></a>
#### email

해당 필드는 이메일 주소 형식에 맞아야 합니다. 이 규칙은 이메일 주소 검증을 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로는 `RFCValidation` 검증기가 적용되지만, 다른 검증 스타일을 추가로 지정할 수도 있습니다.

```php
'email' => 'email:rfc,dns'
```

위와 같이 지정하면 `RFCValidation`과 `DNSCheckValidation` 검증이 모두 적용됩니다. 사용할 수 있는 검증 스타일의 전체 목록은 아래와 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - 이메일 주소를 [지원 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) 기준으로 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) 기반으로, 경고(예: 끝의 마침표, 연속적인 마침표 등)가 있으면 실패하게끔 엄격하게 이메일을 검증합니다.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인이 올바른 MX 레코드를 갖고 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 이메일 주소에 유사한 모양의(homograph) 문자나 속이는 Unicode 문자가 포함되어 있는지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 유효성을 검사합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수 기준으로 유효성을 검사하면서, 일부 Unicode 문자도 허용합니다.

</div>

편의를 위해, 이메일 유효성 검사 규칙은 플루언트 규칙 빌더로 작성할 수 있습니다.

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

해당 필드는 지정한 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 클래스 기반 규칙으로, 해당 필드가 유효한 열거형(enum) 값을 포함하는지 검사합니다. `Enum` 규칙의 생성자 첫 번째 인자로 enum 클래스명을 전달합니다. 원시 값(primitive value)을 검사할 때는 backed Enum을 지정해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`, `except` 메서드를 사용하면 몇몇 enum 케이스만 유효하도록(혹은 일부 제외하도록) 한정할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용하면 조건부로 `Enum` 규칙을 수정할 수 있습니다.

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

유효성 검사가 적용되는 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

_또 다른 필드_가 _value_와 같을 경우, 해당 필드는 `validate` 및 `validated` 메서드의 반환 데이터에서 제외됩니다.

복잡한 조건에 따라 제외 처리가 필요하다면, `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 인자로 받고, 클로저가 true를 반환하면 해당 필드는 제외됩니다.

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

_또 다른 필드_가 _value_와 같지 않으면, 해당 필드는 `validate` 및 `validated` 메서드의 반환 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`)일 때는, 비교 대상 필드가 `null`이거나, 비교 필드 자체가 요청 데이터에 없다면 제외하지 않습니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

_또 다른 필드_가 존재하면, 해당 필드는 `validate` 및 `validated` 메서드의 반환 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

_또 다른 필드_가 존재하지 않으면, 해당 필드는 `validate` 및 `validated` 메서드의 반환 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

해당 필드는 지정한 데이터베이스 테이블에 반드시 존재하는 값이어야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 생략하면, 필드명이 그대로 사용됩니다. 따라서 위 예시에서는 `states` 데이터베이스 테이블에 `state` 컬럼에 해당 필드 값이 존재하는지를 검사합니다.

<a name="specifying-a-custom-column-name"></a>
#### 커스텀 컬럼명 지정하기

규칙에서 테이블 이름 뒤에 컬럼명을 명시적으로 지정할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

때때로 특정 데이터베이스 연결(connection)을 `exists` 쿼리에 사용해야 할 수도 있습니다. 이럴 땐 테이블명 앞에 연결명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, Eloquent 모델을 지정해서 해당 모델의 테이블을 사용할 수 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

규칙이 실행하는 쿼리를 더 세밀하게 제어하고 싶다면, `Rule` 클래스를 활용하여 규칙을 플루언트하게 작성해 사용하면 됩니다. 이 예시에서는 `|` 대신 규칙 배열로 정의하고, 쿼리를 커스터마이즈합니다.

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

`Rule::exists` 메서드의 두 번째 인자로 컬럼명을 지정하면, `exists` 규칙이 사용할 DB 컬럼명을 명확히 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

배열 값 전체가 데이터베이스에 존재하는지 검사하려면, 필드에 `exists`와 [array](#rule-array) 규칙을 모두 적용하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이렇게 두 규칙을 함께 지정하면, 라라벨은 모든 값에 대한 존재 확인 쿼리를 한 번에 자동으로 실행합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

해당 파일은 지정한 확장자 목록 중 하나의 사용자가 지정한 확장자를 가져야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 확장자만으로 파일의 유효성을 검증하는 것은 매우 위험하므로, 이 규칙은 반드시 [mimes](#rule-mimes), [mimetypes](#rule-mimetypes) 규칙과 항상 조합해서 사용해야 합니다.

<a name="rule-file"></a>
#### file

해당 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

해당 필드는 값이 비어 있지 않아야 하며, 값이 존재할 경우 반드시 입력되어야 합니다.

<a name="rule-gt"></a>
#### gt:_field_

해당 필드는 _field_ 또는 _value_보다 더 커야 합니다. 두 필드는 반드시 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

해당 필드는 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 반드시 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

해당 필드는 [16진수 색상](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값을 가져야 합니다.

<a name="rule-image"></a>
#### image

해당 파일은 이미지(jpg, jpeg, png, bmp, gif, webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 취약점(역자주: 크로스 사이트 스크립팅 보안 이슈) 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용하려면 `image:allow_svg`와 같이 `allow_svg` 지시자를 규칙에 추가하세요.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

해당 필드는 지정한 값 목록 안에 포함되어야 합니다. 배열을 다룰 때는 주로 `implode`를 사용하게 되므로, `Rule::in` 메서드를 통해 규칙을 플루언트하게 작성할 수 있습니다.

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

`in` 규칙이 `array` 규칙과 함께 쓰이면, 입력 배열 내의 모든 값이 `in` 규칙에 지정한 값 목록에 반드시 포함되어야 합니다. 예를 들어, 아래 입력 데이터에서 `LAS` 공항 코드는 공항 목록에 없으므로 유효하지 않습니다.

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

검증 중인 필드는 _anotherfield_의 값 중에 반드시 존재해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 중인 필드는 배열이어야 하며, 해당 배열의 키 중에 주어진 _values_ 중 하나 이상의 키가 반드시 존재해야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증 중인 필드는 반드시 정수여야 합니다.

> [!WARNING]
> 이 유효성 규칙은 입력값이 "정수" 변수 타입인지까지 확인하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙이 허용하는 타입이면 만족한 것으로 간주합니다. 입력값이 숫자인지까지 검증하려면 [numeric 유효성 검사 규칙](#rule-numeric)과 함께 사용해야 합니다.

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

검증 중인 필드는 주어진 _field_보다 작아야 합니다. 두 필드는 반드시 동일한 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 중인 필드는 주어진 _field_보다 작거나 같아야 합니다. 두 필드는 반드시 동일한 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 중인 필드는 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증 중인 필드는 반드시 "리스트"형 배열이어야 합니다. 배열의 키가 0부터 `count($array) - 1`까지의 연속된 숫자일 경우 리스트로 간주합니다.

<a name="rule-mac"></a>
#### mac_address

검증 중인 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 중인 필드는 _value_ 값 이하(max)이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 중인 정수 값의 자릿수가 _value_ 이하여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 중인 파일은 주어진 MIME 타입 중 하나와 일치해야 합니다:

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드된 파일의 MIME 타입을 판별하기 위해 파일 내용이 실제로 읽히며, 프레임워크가 MIME 타입을 추측합니다. 이 값은 클라이언트에서 전송한 MIME 타입과는 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 중인 파일은 나열된 확장자에 대응하는 MIME 타입을 가져야 합니다:

```php
'photo' => 'mimes:jpg,bmp,png'
```

여기서는 확장자만 지정하면 되지만, 실제로는 이 규칙이 파일의 내용을 읽어서 MIME 타입을 추정하여 검사합니다. 전체 MIME 타입과 해당 확장자 목록은 다음 링크에서 확인할 수 있습니다:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 규칙은 사용자가 지정한 확장자와 MIME 타입이 반드시 일치하는지까지는 검사하지 않습니다. 예를 들어, `mimes:png` 검증에서는 실제로 PNG 데이터가 담긴 파일이면 그 파일명이 `photo.txt`여도 PNG 이미지로 간주됩니다. 만약 사용자가 지정한 파일 확장자 자체까지 검증하고 싶다면, [extensions](#rule-extensions) 규칙을 사용할 수 있습니다.

<a name="rule-min"></a>
#### min:_value_

검증 중인 필드의 값은 _value_ 이상이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 중인 정수 값의 자릿수가 _value_ 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 중인 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증 중인 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)의 값이 주어진 _value_ 중 하나와 같을 경우, 검증 중인 필드는 입력 데이터에서 존재하면 안 됩니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_또 다른 필드_(_anotherfield_)의 값이 주어진 _value_와 다를 경우, 검증 중인 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

지정한 다른 필드들 중 어느 하나라도 존재하는 경우에만, 검증 중인 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

지정한 모든 다른 필드가 모두 존재할 때에만, 검증 중인 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 중인 필드는 주어진 값 목록에 포함되지 않아야 합니다. `Rule::notIn` 메서드를 이용해 규칙을 더 명확하게 정의할 수 있습니다:

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

검증 중인 필드는 주어진 정규 표현식과 일치하지 않아야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 형식(구분자 포함)을 따라야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 정규식에 `|` 문자가 포함되어 있다면 규칙을 파이프(`|`) 구분자가 아니라 배열 형태로 지정해야 할 수 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증 중인 필드는 `null`이어도 허용됩니다.

<a name="rule-numeric"></a>
#### numeric

검증 중인 필드는 [숫자 값](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<a name="rule-present"></a>
#### present

검증 중인 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 주어진 _value_ 중 어느 하나와 같을 때, 검증 중인 필드는 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_또 다른 필드_(_anotherfield_)가 주어진 _value_와 같지 않은 경우, 검증 중인 필드는 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

지정한 다른 필드 중 어느 하나라도 존재하면, 검증 중인 필드가 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

지정한 모든 다른 필드가 모두 존재하면, 검증 중인 필드도 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 중인 필드는 반드시 없어야 하거나, 비어 있어야 합니다. "비어 있음"의 기준은 다음 중 하나를 만족하는 경우입니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 업로드된 파일 경로가 비어 있는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)의 값이 주어진 _value_ 중 아무거나와 같으면, 검증 중인 필드는 반드시 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 업로드된 파일 경로가 비어 있는 경우

</div>

복잡한 조건으로 금지 규칙을 제어하려면 `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받을 수 있습니다. 클로저를 전달하면, 반환값이 `true`면 해당 필드를 금지하고, `false`면 허용합니다.

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

_또 다른 필드_(_anotherfield_)의 값이 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나일 경우, 검증 중인 필드는 반드시 없어야 하거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_또 다른 필드_(_anotherfield_)의 값이 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나일 경우, 검증 중인 필드는 반드시 없어야 하거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 주어진 _value_와 다르면, 검증 중인 필드는 반드시 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 업로드된 파일 경로가 비어 있는 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 중인 필드가 없어도 되고 비어 있지 않은 경우, _anotherfield_에 지정된 모든 필드는 반드시 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 업로드된 파일 경로가 비어 있는 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증 중인 필드는 주어진 정규 표현식과 일치해야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 형식(구분자 포함)을 따라야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 정규식에 `|` 문자가 포함되어 있다면 규칙을 파이프(`|`) 구분자가 아니라 배열 형태로 지정해야 할 수 있습니다.

<a name="rule-required"></a>
#### required

검증 중인 필드는 입력 데이터에 존재해야 하며, 비어 있으면 안 됩니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 업로드된 파일 경로가 없는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)의 값이 주어진 _value_ 중 하나일 때, 검증 중인 필드는 반드시 존재해야 하며, 비어 있으면 안 됩니다.

좀 더 복잡한 조건으로 required_if 규칙을 구성하려면 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받을 수 있습니다. 클로저는 해당 필드가 required인지 `true`/`false`로 반환해야 합니다:

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

_또 다른 필드_(_anotherfield_)가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나인 경우, 해당 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_또 다른 필드_(_anotherfield_)가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나인 경우, 해당 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)의 값이 주어진 _value_와 다를 때, 해당 필드는 반드시 존재하며 비어 있을 수 없습니다. 이 규칙은 _anotherfield_가 요청 데이터에 반드시 존재해야 함을 의미합니다(단, _value_가 `null`인 경우 제외). _value_가 `null`일 때(`required_unless:name,null`), 비교 필드가 `null`이거나 요청 데이터에서 누락된 경우에만 해당 필드는 필수가 아닙니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

지정한 다른 필드 중 어떤 것이든 존재하고 비어 있지 않은 경우, 검증 중인 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

지정한 모든 다른 필드가 모두 존재하고 비어 있지 않은 경우, 검증 중인 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

지정한 다른 필드 중 어떤 것이든 비어 있거나 존재하지 않는 경우, 검증 중인 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

지정한 다른 필드가 모두 비어 있거나 존재하지 않는 경우, 검증 중인 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증 중인 필드는 배열이어야 하며, 지정한 키들을 최소한 반드시 포함하고 있어야 합니다.

<a name="rule-same"></a>
#### same:_field_

주어진 _field_의 값이 검증 중인 필드 값과 반드시 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증 중인 필드는 _value_에 해당하는 크기를 가져야 합니다. 문자열일 경우 _value_는 문자 개수, 숫자일 경우 해당 값(이때 `numeric` 또는 `integer` 규칙도 반드시 필요), 배열은 요소의 개수, 파일의 경우 킬로바이트 단위의 용량을 의미합니다. 예시는 다음과 같습니다.

```php
// 문자열이 정확히 12자여야 함
'title' => 'size:12';

// 정수가 10이어야 함
'seats' => 'integer|size:10';

// 배열이 정확히 5개 요소를 가져야 함
'tags' => 'array|size:5';

// 업로드 파일이 정확히 512킬로바이트여야 함
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 중인 필드는 주어진 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 중인 필드는 문자열이어야 합니다. 동시에 `null`도 허용하려면 `nullable` 규칙을 함께 지정해야 합니다.

<a name="rule-timezone"></a>
#### timezone

검증 중인 필드는 `DateTimeZone::listIdentifiers` 메서드에 따라 유효한 타임존 식별자여야 합니다.

이 유효성 규칙에는 [`DateTimeZone::listIdentifiers` 메서드에서 허용하는 인수](https://www.php.net/manual/en/datetimezone.listidentifiers.php)를 직접 넘길 수도 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증 중인 필드는 주어진 데이터베이스 테이블 내에 존재하지 않아야 합니다.

**커스텀 테이블/컬럼명 지정하기:**

테이블명을 직접 지정하는 대신, Eloquent 모델을 지정해서 해당 모델이 사용하는 테이블명으로 검사할 수도 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

옵션 `column`에는 데이터베이스 컬럼명을 직접 지정할 수 있습니다. 지정하지 않으면 검증 중인 필드의 이름이 컬럼명으로 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**커스텀 데이터베이스 연결 사용하기**

때때로 Validator가 사용하는 데이터베이스 연결을 커스텀해야 할 때도 있습니다. 이 경우 테이블명 앞에 연결명을 붙여서 지정할 수 있습니다.

```php
'email' => 'unique:connection.users,email_address'
```

**특정 ID는 unique 검사에서 제외하기:**

사용자 프로필 수정 처럼 특정 ID의 레코드는 unique 검사에서 제외해야 할 때가 있습니다. 예를 들어, 사용자가 이름만 변경하고 이메일은 그대로 둘 때, 해당 이메일이 이미 본인 것이라면 중복 에러가 발생하지 않도록 해야 합니다.

이럴 때는 `Rule` 클래스를 활용해 규칙을 유연하게 정의합니다. 아래에서는 규칙을 `|` 구분자가 아니라 배열로 지정한 예시도 함께 보여줍니다.

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
> `ignore` 메서드에는 반드시 시스템에서 생성한 고유 ID(예: 자동 증가 ID, Eloquent 모델 인스턴스의 UUID 등)만 넣어야 하며, 사용자가 전송한 데이터를 직접 전달하지 마세요. 그렇지 않으면 SQL 인젝션 공격에 취약해질 수 있습니다.

`ignore` 메서드에 모델의 키 값 대신, 전체 모델 인스턴스를 전달해도 됩니다. 라라벨이 자동으로 키를 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

테이블의 기본키 컬럼명이 `id`가 아니면, `ignore` 호출 시 컬럼명을 두 번째 인자로 전달할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 unique 규칙은 검증 중인 필드의 이름과 컬럼명이 일치해야 합니다. 하지만 두 번째 인자로 다른 컬럼명을 넘겨, 해당 컬럼의 중복 여부를 검사하게 할 수 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 where 조건 지정하기:**

`where` 메서드를 통해 쿼리 조건을 더 추가할 수 있습니다. 아래 예시는 `account_id` 컬럼이 1인 레코드만 중복 검사를 하도록 범위를 제한하는 예시입니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Unique 검사에서 소프트 삭제 레코드 제외하기:**

기본적으로 unique 규칙은 소프트 삭제된 레코드도 중복 검사에 포함합니다. 중복 검사에서 소프트 삭제된 레코드를 제외하려면 `withoutTrashed` 메서드를 사용합니다.

```php
Rule::unique('users')->withoutTrashed();
```

만약 모델에서 소프트 삭제 컬럼명이 `deleted_at`이 아니라면, `withoutTrashed` 호출 시 컬럼명을 인자로 전달하면 됩니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증 중인 필드는 대문자여야 합니다.

<a name="rule-url"></a>
#### url

검증 중인 필드는 올바른 URL이어야 합니다.

허용할 URL 프로토콜을 직접 지정하려면, 규칙의 파라미터로 넘길 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증 중인 필드는 유효한 [ULID(Universally Unique Lexicographically Sortable Identifier)](https://github.com/ulid/spec) 형식이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 중인 필드는 RFC 9562(버전 1, 3, 4, 5, 6, 7, 8) 표준의 UUID(범용 고유 식별자)이어야 합니다.

특정 UUID 버전에 맞는 값인지도 규칙에 추가할 수 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 유효성 검증 건너뛰기

다른 필드가 특정 값일 경우, 특정 필드의 유효성 검증 자체를 생략하고 싶을 때가 있습니다. `exclude_if` 유효성 검사 규칙을 사용하면 가능합니다. 아래 예시에서, `has_appointment` 필드가 `false`일 경우 `appointment_date`와 `doctor_name` 필드는 검증에서 제외됩니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

또는, `exclude_unless` 규칙을 사용하여, 특정 필드가 주어진 값이 아닌 경우에만 검증에서 제외할 수도 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>

#### 존재할 때만 유효성 검사하기

특정 상황에서는, 필드가 데이터에 **존재할 때에만** 유효성 검사를 실행하고 싶을 수 있습니다. 이를 빠르게 구현하려면 해당 규칙 목록에 `sometimes` 규칙을 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위의 예제에서는, `email` 필드는 `$data` 배열에 존재하는 경우에만 유효성 검사가 적용됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드의 유효성 검사를 시도하려는 경우, [옵션 필드에 관한 이 참고 사항](#a-note-on-optional-fields)을 확인하시기 바랍니다.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검사

경우에 따라 더 복잡한 조건부 로직에 따라 유효성 검사 규칙을 추가하고 싶을 수 있습니다. 예를 들어, 다른 필드의 값이 100을 초과할 때에만 특정 필드를 필수로 만들고 싶거나, 또 다른 필드가 존재할 때만 두 개의 필드에 특정 값이 필요하도록 할 수도 있습니다. 이러한 유효성 검사 규칙을 추가하는 과정이 어렵게 느껴질 수 있지만, 어렵지 않게 처리할 수 있습니다. 먼저, 변경되지 않는 _고정 규칙_ 으로 `Validator` 인스턴스를 만듭니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

우리 애플리케이션이 게임을 수집하는 사람(콜렉터)을 위한 것이라고 가정해봅시다. 만약 사용자가 100개 이상의 게임을 소유하고 있다고 등록한다면, 왜 그렇게 많은 게임을 가지고 있는지 설명을 추가하도록 요구하고 싶을 수 있습니다. 예를 들어, 중고로 게임을 판매하는 사업을 한다거나, 단순히 수집하는 것을 즐긴다는 이유일 수도 있습니다. 이런 조건부 요구사항을 손쉽게 추가하려면 `Validator` 인스턴스의 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드에 전달하는 첫 번째 인수는 조건부로 유효성 검사를 적용할 필드명입니다. 두 번째 인수는 적용하고자 하는 규칙 목록입니다. 세 번째 인수로 전달된 클로저에서 `true`를 반환하면 해당 규칙이 추가됩니다. 이 메서드를 사용하면 복잡한 조건부 유효성 검사를 매우 간편하게 구성할 수 있습니다. 여러 필드에 조건부로 규칙을 한 번에 추가하는 것도 가능합니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent`의 인스턴스이며, 유효성 검사 대상의 입력 값 및 파일에 접근할 때 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 유효성 검사

경우에 따라, 같은 중첩 배열 내의 다른 필드값(인덱스를 미리 알 수 없는)의 값을 기반으로 특정 필드를 유효성 검사하고 싶을 수 있습니다. 이럴 때에는, 클로저가 배열 내 현재 개별 항목(아이템)을 두 번째 인수로 받을 수 있도록 하면 됩니다.

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

여기서 `$item` 파라미터 역시 배열 데이터일 경우 `Illuminate\Support\Fluent`의 인스턴스이며, 만약 속성값이 배열이 아니라면 단순 문자열입니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[배열 유효성 검사 규칙 문서](#rule-array)에서 논의했듯이, `array` 규칙에서는 허용하는 배열 키 목록을 지정할 수 있습니다. 배열 내에 추가적인 키가 있으면 유효성 검사가 실패하게 됩니다.

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

일반적으로는, 배열 내에 허용할 키를 항상 명시적으로 지정해야 합니다. 그렇지 않으면, 검증기의 `validate` 및 `validated` 메서드는 배열 및 모든 키(다른 중첩 배열 규칙에 의해 유효성 검사를 받지 않은 키까지도)도 반환하게 됩니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력값 유효성 검사

중첩 배열 기반의 폼 입력값 유효성 검사를 어렵지 않게 처리할 수 있습니다. 배열 내 속성에 대해 "점 표기법(dot notation)"을 사용할 수 있습니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]` 필드가 있다면, 아래와 같이 유효성 검사를 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

또한, 배열의 각 요소별로도 유효성 검사를 할 수 있습니다. 예를 들어, 주어진 배열 필드 내 각 이메일이 고유(unique)해야 한다는 검증은 아래와 같이 할 수 있습니다.

```php
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

마찬가지로, [`언어 파일에서 배열 기반 필드를 위한 별도의 사용자 정의 오류 메시지`](#custom-messages-for-specific-attributes)를 지정할 때 `*` 문자를 사용하면, 배열 항목에 대한 공통 유효성 메시지를 아주 쉽게 작성할 수 있습니다.

```php
'custom' => [
    'person.*.email' => [
        'unique' => 'Each person must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근하기

여러분의 배열 필드가 중첩되어 있고, 유효성 검사 규칙을 해당 요소의 실제 값에 따라 동적으로 할당해야 할 때가 있을 수 있습니다. 이럴 때는 `Rule::forEach` 메서드를 사용할 수 있습니다. 이 메서드는, 배열 속성의 각 반복마다 클로저를 호출하며, 현재 값과 확장된 전체 속성명을 인자로 제공합니다. 클로저는 해당 요소에 적용할 규칙 배열을 반환해야 합니다.

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
### 오류 메시지에서 인덱스와 위치 사용하기

배열을 검증할 때, 어플리케이션에서 오류 메시지에 해당 항목의 인덱스(위치)를 명시적으로 표시해주고 싶을 수 있습니다. 이를 위해 [사용자 정의 에러 메시지](#manual-customizing-the-error-messages)에 `:index`(0부터 시작) 또는 `:position`(1부터 시작) 플레이스홀더를 포함할 수 있습니다.

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

위 예제에서는 2번째 사진의 설명이 비어 있으므로, 사용자는 _"Please describe photo #2."_라는 오류 메시지를 보게 됩니다.

필요하다면, `second-index`, `second-position`, `third-index`, `third-position` 등과 같은 식으로 더 깊은 중첩 인덱스나 위치도 참고할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 유효성 검사

라라벨은 파일 업로드 시 사용할 수 있는 다양한 유효성 검사 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 이러한 규칙을 직접 지정할 수도 있지만, 라라벨에서는 더 편리하게 사용할 수 있는 유연한 파일 유효성 검사 규칙 빌더도 지원합니다.

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

`types` 메서드를 호출할 때는 확장자만 지정해 주면 되지만, 실제로는 이 메서드가 파일 내용의 MIME 타입을 읽어 해당 파일의 MIME 타입이 올바른지 검사합니다. 전체 MIME 타입 목록 및 그에 해당하는 확장자는 다음 위치에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 유효성 검사

편의상, 최소/최대 파일 크기는 문자열로 단위를 접미사로 붙여 지정할 수 있습니다. 지원하는 단위는 `kb`, `mb`, `gb`, `tb`입니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 유효성 검사

사용자로부터 업로드받는 이미지 파일에 대해서는, `File` 규칙의 `image` 생성자 메서드를 사용해 해당 파일이 이미지(예: jpg, jpeg, png, bmp, gif, webp)인지 검증할 수 있습니다.

또한, `dimensions` 규칙을 활용하면 이미지의 가로*세로 크기에 제한을 둘 수도 있습니다.

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
> 이미지 크기 유효성 검사에 대한 더 자세한 정보는 [dimensions 규칙 문서](#rule-dimensions)에서 확인하실 수 있습니다.

> [!WARNING]
> 기본적으로 `image` 규칙에서는 XSS 위험이 있기 때문에 SVG 파일이 허용되지 않습니다. SVG 파일도 허용하려면 `File::image(allowSvg: true)`와 같이 `allowSvg: true` 옵션을 전달하세요.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(차원) 유효성 검사

이미지의 가로, 세로 크기를 유효성 검사할 수도 있습니다. 예를 들어, 업로드된 이미지는 가로 1000픽셀 이상, 세로 500픽셀 이상이어야 한다는 규칙을 줄 수 있습니다.

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
> 이미지 크기 검증에 대해 더 알고 싶으시면 [dimensions 규칙 문서](#rule-dimensions)를 참고하세요.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검사

비밀번호가 충분히 복잡한지 확인하려면, 라라벨의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체는 최소 길이, 영어 대ㆍ소문자 혼용, 숫자, 기호 등, 비밀번호 복잡성 요구사항을 쉽게 커스터마이즈할 수 있도록 해줍니다.

```php
// 최소 8자 이상이어야 함...
Password::min(8)

// 영문자가 반드시 포함되어야 함...
Password::min(8)->letters()

// 대문자와 소문자가 각각 최소 하나 포함되어야 함...
Password::min(8)->mixedCase()

// 숫자가 최소 하나 포함되어야 함...
Password::min(8)->numbers()

// 기호가 최소 하나 포함되어야 함...
Password::min(8)->symbols()
```

또한, `uncompromised` 메서드를 이용해 공개적으로 유출된 비밀번호인지 검사해서, 이미 데이터 유출 사고에 포함된 비밀번호는 거부할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로 `Password` 규칙 객체는 [k-익명성(k-Anonymity)](https://en.wikipedia.org/wiki/K-anonymity) 모델을 사용하여 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호가 유출되었는지 확인하되, 사용자의 개인정보나 보안을 침해하지 않습니다.

기본적으로, 비밀번호가 유출 목록에 단 한 번이라도 등장하면 "유출된 것으로" 간주합니다. 이 기준 값(허용 임계값)은 `uncompromised` 메서드의 첫 번째 인자로 지정할 수 있습니다.

```php
// 같은 유출 내에서 3회 미만 등장할 경우만 허용
Password::min(8)->uncompromised(3);
```

물론, 위에서 본 다양한 메서드들을 모두 체이닝하여 결합해서 사용할 수 있습니다.

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

하나의 위치에서 기본 비밀번호 유효성 검사 규칙을 지정해두고, 애플리케이션 전체에서 사용할 수 있다면 편리합니다. 이를 위해 `Password::defaults` 메서드에 클로저를 전달하여, 비밀번호의 기본 규칙 설정을 지정할 수 있습니다. 이 메서드는 보통 애플리케이션 서비스 프로바이더(예: `AppServiceProvider`)의 `boot` 메서드 안에서 호출하면 됩니다.

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

이후에는 특정 비밀번호 필드에 기본 규칙을 적용하고 싶을 때 인자를 생략한 채 `defaults`를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

때때로, 기본 비밀번호 규칙에 추가로 커스텀 규칙을 덧붙이고 싶은 경우 `rules` 메서드를 사용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 커스텀 유효성 검사 규칙

<a name="using-rule-objects"></a>
### Rule 객체 사용하기

라라벨은 이미 다양한 유용한 유효성 검사 규칙들을 제공하지만, 여러분만의 고유한 규칙을 추가로 만들고 싶을 수도 있습니다. 커스텀 검증 규칙을 등록하는 한 가지 방법은 Rule 객체를 사용하는 것입니다. 새 Rule 객체를 만들려면, `make:rule` Artisan 명령어를 사용합니다. 예를 들어, 문자열이 모두 대문자인지 확인하는 규칙을 만들고자 한다면 다음 명령어를 실행하세요. 라라벨은 새 규칙 파일을 `app/Rules` 디렉토리에 생성합니다. 해당 디렉토리가 존재하지 않으면 명령어 실행 시 자동으로 생성됩니다.

```shell
php artisan make:rule Uppercase
```

Rule 클래스를 생성했으면, 이제 그 동작을 정의해주어야 합니다. Rule 객체에는 반드시 하나의 메서드 `validate`가 포함되어야 하며, 이 메서드는 속성명, 값, 그리고 실패 시 호출할 콜백(에러 메시지 전달)을 인자로 받습니다.

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

규칙 클래스를 다 만들었다면, 다른 규칙들과 마찬가지로 해당 Rule 객체의 인스턴스를 검증기에 추가하여 사용할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 검증 메시지 번역하기

실패 시 `$fail` 클로저에 직접적인 에러 메시지 문자열을 전달하는 대신, [번역 문자열 키](/docs/12.x/localization)를 전달해서 라라벨이 자동으로 메시지를 번역하도록 할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

만약 자리 표시자 치환이 필요하거나, 특정 언어로 번역하려면, `translate` 메서드의 첫 번째 및 두 번째 인수로 각각 치환값 배열과 언어 코드를 넘길 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근

만약 커스텀 규칙 클래스 내에서 검증 대상 전체 데이터에 접근해야 한다면, 해당 규칙 클래스가 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하도록 만듭니다. 이 인터페이스는 `setData` 메서드 구현을 요구합니다. 라라벨은(유효성 검사가 시작되기 전에) 자동으로 검증 전체 데이터를 이 메서드에 넘겨줍니다.

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

검증을 수행하는 실제 Validator 인스턴스가 필요하다면, `ValidatorAwareRule` 인터페이스를 구현하면 됩니다.

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

커스텀 규칙이 애플리케이션에서 단 한 번만 필요하다면, Rule 객체 대신 클로저를 사용할 수도 있습니다. 이 클로저는 속성명, 값, 실패 시 호출할 `$fail` 콜백을 인자로 받습니다.

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
### 암묵적(implicit) 규칙

기본적으로, 검증 대상 속성이 없거나 빈 문자열일 때는 일반 유효성 검사 규칙(커스텀 규칙 포함)이 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에는 적용되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

커스텀 규칙을 빈 속성에도 항상 실행하려면, 그 규칙이 "필수(required)"임을 내포(암시)해야 합니다. 이를 위해 `make:rule` Artisan 명령어에 `--implicit` 옵션을 추가해서 암묵적(implicit) 규칙 객체를 빠르게 생성할 수 있습니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙은 속성이 필수임을 _암시_할 뿐입니다. 실제로 누락되었거나 빈 속성을 오류로 처리하는지는 여러분의 구현에 달려 있습니다.