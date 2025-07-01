# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 재입력 지원](#repopulating-forms)
    - [선택 필드에 대한 안내](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 형식](#validation-error-response-format)
- [폼 리퀘스트 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성](#creating-form-requests)
    - [폼 리퀘스트 인가(Authorization)](#authorizing-form-requests)
    - [오류 메시지 커스터마이즈](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비](#preparing-input-for-validation)
- [Validator 직접 생성하기](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 오류 백(Named Error Bags)](#named-error-bags)
    - [오류 메시지 커스터마이즈](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [유효성 검증된 입력값 활용](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 커스텀 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 검증하기](#validating-arrays)
    - [중첩 배열 입력값 검증](#validating-nested-array-input)
    - [오류 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 검증하기](#validating-files)
- [비밀번호 검증하기](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 활용](#using-rule-objects)
    - [클로저 활용](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션에 들어오는 데이터를 검증하는 여러 가지 방법을 제공합니다. 가장 일반적으로는, 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 활용합니다. 하지만 본 문서에서는 이외에도 다양한 유효성 검증 방법들을 설명합니다.

라라벨에는 다양한 편리한 유효성 검증 규칙이 내장되어 있어, 데이터가 데이터베이스의 특정 테이블에서 유일한지 검증하는 등 다양한 요구사항을 만족할 수 있습니다. 이 문서에서는 라라벨이 제공하는 모든 유효성 검증 규칙에 대해 자세히 다루어, 여러분이 각 기능을 자유롭게 활용할 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작

라라벨의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 검증하고 오류 메시지를 사용자에게 보여주는 전체 과정을 예시로 살펴보겠습니다. 이 내용을 한 번에 파악하면 라라벨에서 요청 데이터를 어떻게 검증하는지 전반적으로 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정하겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새로운 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새로 작성된 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위 라우트에서 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 이 예시에서는 `store` 메서드는 아직 비워둔 상태입니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새로운 블로그 포스트 작성 폼을 보여줍니다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새로운 블로그 포스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 유효성 검증 후 블로그 포스트를 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제, `store` 메서드를 실제로 새로운 블로그 포스트의 유효성을 검증하도록 채워 넣을 차례입니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용할 것입니다. 유효성 검증 규칙을 통과하면 코드는 정상적으로 앞으로 진행되지만, 검증에 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하며, 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 유효성 검증에 실패하면, 이전 URL로 리다이렉트하는 응답이 생성됩니다. 만약 요청이 XHR(비동기 JavaScript) 요청인 경우, [유효성 검증 오류 메시지가 담긴 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드의 사용 방식을 이해하기 위해, 다시 한 번 `store` 메서드를 예로 들면 아래와 같습니다.

```php
/**
 * 새로운 블로그 포스트를 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 포스트 데이터가 유효합니다...

    return redirect('/posts');
}
```

보시다시피, 유효성 검증 규칙들은 `validate` 메서드의 인수로 전달됩니다. 모든 유효성 검증 규칙은 [여기서](#available-validation-rules) 문서화되어 있으니 참고하셔도 좋습니다. 다시 한 번 강조하자면, 검증에 실패할 경우 적절한 응답이 자동으로 생성되며, 검증에 통과하면 컨트롤러가 정상적으로 실행됩니다.

또한, 유효성 검증 규칙은 하나의 `|` 구분자를 사용하는 문자열 대신 규칙의 배열로도 지정할 수 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

추가로, `validateWithBag` 메서드를 이용하면 [이름이 지정된 오류 백](#named-error-bags)에 오류 메시지를 저장할 수도 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 실패 시 즉시 중단하기

때로는 하나의 속성(attribute)에 대해 첫 번째 유효성 검증이 실패하면 나머지 규칙을 더 이상 검사하지 않고 중단하고 싶을 때가 있습니다. 이를 위해, 해당 속성에 `bail` 규칙을 추가합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

위 예시에서는 `title` 속성의 `unique` 규칙이 실패하면, 그 뒤에 있는 `max` 규칙은 검증하지 않습니다. 이렇게 규칙은 지정한 순서대로 차례로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes)에 관한 안내

들어오는 HTTP 요청에 "중첩된(nested)" 필드 데이터가 있는 경우, 유효성 검사 규칙에서 "점(dot) 표기법"을 사용하여 해당 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로, 필드명에 실제로 마침표('.')가 포함되어 있을 경우, 백슬래시(`\`)를 사용해 점을 이스케이프 처리하면 "점 표기법"으로 해석되지 않습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시하기

그렇다면, 요청 필드가 지정한 유효성 검증 규칙을 통과하지 못했을 때는 어떻게 될까요? 앞서 설명한 것처럼, 라라벨은 자동으로 사용자를 이전 위치로 리다이렉트해 줍니다. 이와 더불어, 모든 유효성 검증 오류와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 자동으로 [세션에 flash 데이터로 저장](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어(이 미들웨어는 `web` 미들웨어 그룹에서 제공됨)가 모든 뷰에 `$errors` 변수를 공유합니다. 이 미들웨어가 적용된 경우, 항상 뷰에서 `$errors` 변수를 사용할 수 있으니 변수가 무조건 정의되었다고 가정해도 괜찮습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 클래스의 인스턴스입니다. 이 객체를 다루는 방법은 [관련 문서](#working-with-error-messages)에서 추가로 확인하실 수 있습니다.

예시에서는, 유효성 검증에 실패하면 사용자가 컨트롤러의 `create` 메서드로 리다이렉트되어, 뷰에서 오류 메시지를 보여줄 수 있습니다.

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

라라벨의 내장 유효성 검증 규칙은 각각 오류 메시지를 함께 가지고 있으며, 이 메시지들은 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 해당 디렉터리를 생성할 수 있습니다.

`lang/en/validation.php` 파일에는 각 유효성 규칙마다 변역 엔트리가 포함되어 있습니다. 애플리케이션의 요구에 따라 자유롭게 이 메시지들을 변경하거나 수정할 수 있습니다.

또한, 이 파일을 다른 언어용 디렉터리로 복사해, 각 언어에 맞춰 메시지를 번역할 수도 있습니다. 라라벨의 로컬라이제이션에 대해 더 알고 싶다면 [로컬라이제이션 전체 문서](/docs/12.x/localization)를 참고하시기 바랍니다.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션의 스캐폴딩(skeleton)에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` 아티즌 명령어로 파일을 퍼블리시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이 예제에서는 전통적인 폼 방식으로 데이터를 애플리케이션에 전송했습니다. 그러나 실제 애플리케이션에서는 JavaScript를 사용하는 프론트엔드에서 XHR(비동기) 요청을 받는 경우가 많습니다. XHR 요청에서 `validate` 메서드를 사용할 때는 리다이렉트 응답이 아닌, [유효성 검증 오류가 모두 담긴 JSON 응답](#validation-error-response-format)이 반환됩니다. 이 JSON 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

[Blade](/docs/12.x/blade)에서 제공하는 `@error` 디렉티브를 사용하면, 특정 필드에 대한 유효성 검증 오류 메시지가 있는지 쉽게 확인할 수 있습니다. `@error` 블록 내부에서는 `$message` 변수를 출력해 오류 메시지를 표시할 수 있습니다.

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

[이름이 지정된 오류 백](#named-error-bags)을 사용하는 경우, 두 번째 인수로 오류 백 이름을 `@error` 디렉티브에 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 재입력 지원

유효성 검증 에러로 인해 라라벨이 리다이렉트 응답을 생성할 때, 프레임워크는 [요청의 모든 입력값을 세션에 flash 데이터로 자동 저장](/docs/12.x/session#flash-data)합니다. 이는 사용자가 제출한 폼을 다음 요청에서 쉽게 재입력 할 수 있도록 도와줍니다.

이전 요청의 flash 된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. 이 메서드는 [세션](/docs/12.x/session)에 저장된 입력값을 반환합니다.

```php
$title = $request->old('title');
```

라라벨은 전역 `old` 헬퍼 함수도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값을 보여줄 때는 간편하게 `old` 헬퍼를 사용할 수 있습니다. 해당 필드에 이전 입력값이 없다면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 필드에 대한 안내

기본적으로 라라벨은 애플리케이션의 전역 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 포함하고 있습니다. 이 때문에, "선택적(optional)" 요청 필드를 `nullable`로 지정하지 않으면, 값이 `null`인 경우 유효하지 않다고 간주되는 경우가 자주 발생합니다. 예를 들어,

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예시에서는 `publish_at` 필드가 `null`이거나 올바른 날짜 형식 중 하나일 수 있다고 명시한 것입니다. 만약 규칙 정의에서 `nullable`을 추가하지 않으면, 검증기는 `null` 값을 유효하지 않은 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어온 HTTP 요청이 JSON 응답을 기대하는 경우, 라라벨은 자동으로 오류 메시지를 포맷해 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래는 유효성 검증 오류에 대한 JSON 응답 형식의 예시입니다. 중첩된 오류 키는 "점(dot) 표기법"으로 평탄화되어 제공됩니다.

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
### 폼 리퀘스트 생성

더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(Form Request)"를 생성하는 방법을 고려할 수 있습니다. 폼 리퀘스트는 자체적으로 유효성 검증과 인가(authorization) 로직을 캡슐화한 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 생성하려면 `make:request` 아티즌 CLI 명령어를 사용합니다.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 해당 디렉터리가 없다면, `make:request` 명령 실행 시 자동으로 생성됩니다. 라라벨에서 만들어주는 폼 리퀘스트에는 기본적으로 `authorize`와 `rules` 두 가지 메서드가 포함되어 있습니다.

예상하셨듯이, `authorize` 메서드는 현재 인증된 사용자가 해당 요청에서 표현하는 동작을 수행할 수 있는지 판단하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드 시그니처에서 필요한 의존성을 타입힌트로 명시하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 해결됩니다.

그렇다면 이 유효성 검증 규칙은 언제 평가될까요? 컨트롤러 메서드의 인수에서 해당 폼 리퀘스트를 타입힌트로 지정하면 됩니다. 들어온 폼 리퀘스트는 컨트롤러 메서드가 호출되기 전에 자동으로 유효성 검증이 완료되므로, 별도의 검증 코드를 컨트롤러에 추가할 필요가 없습니다.

```php
/**
 * 새로운 블로그 포스트를 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 들어온 요청은 이미 유효성 검증을 통과한 상태입니다...

    // 유효성 검증된 입력값 전체를 가져옵니다...
    $validated = $request->validated();

    // 유효성 검증된 입력값 일부만 가져옵니다...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 포스트를 저장...

    return redirect('/posts');
}
```

만약 유효성 검증에 실패하면, 사용자는 이전 위치로 리다이렉트되어 오류가 세션에 flash 되어 표시됩니다. 요청이 XHR인 경우에는 [유효성 검증 오류의 JSON 표현](#validation-error-response-format)이 포함된 HTTP 422 상태 코드 응답이 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에 실시간 폼 리퀘스트 유효성 검증을 추가하고 싶으신가요? [Laravel Precognition](/docs/12.x/precognition) 문서를 확인해 보세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행

때로는 최초의 유효성 검증이 끝난 뒤에, 추가로 검증해야 할 사항이 있을 수도 있습니다. 이럴 때는 폼 리퀘스트의 `after` 메서드를 사용할 수 있습니다.

`after` 메서드는 유효성 검증이 완료된 뒤에 실행할 callable 또는 클로저(Closure)의 배열을 반환해야 합니다. 이 callable은 `Illuminate\Validation\Validator` 인스턴스를 받아, 필요 시 추가 오류 메시지를 등록할 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 "after" 검증 콜러블(callable)들을 반환합니다.
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

설명에서처럼, `after` 메서드가 반환하는 배열에는 클래스 인스턴스를 추가할 수도 있습니다. 이 경우 클래스의 `__invoke` 메서드가 `Illuminate\Validation\Validator` 인스턴스를 인자로 받아 실행됩니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 "after" 검증 콜러블(callable)들을 반환합니다.
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

리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 하나의 유효성 검증 실패가 발생한 순간 모든 속성에 대한 검증을 멈추도록 할 수 있습니다.

```php
/**
 * 유효성 검증이 첫 번째 규칙에서 실패하면 검증을 멈출지 여부.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리다이렉트 위치 커스터마이즈

폼 리퀘스트 유효성 검증에 실패하면, 사용자는 기본적으로 이전 위치로 리다이렉트됩니다. 하지만 원하는 경우 이 동작을 변경할 수 있습니다. 폼 리퀘스트에 `$redirect` 프로퍼티를 정의하면 됩니다.

```php
/**
 * 유효성 검증 실패시 사용자가 리다이렉트될 URI.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는, 네임드 라우트로 리다이렉트하고 싶다면 `$redirectRoute` 프로퍼티도 사용할 수 있습니다.

```php
/**
 * 유효성 검증 실패시 사용자가 리다이렉트될 라우트.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가(Authorization)

폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드에서 인증된 사용자가 실제로 특정 리소스를 수정할 권한이 있는지 판단할 수 있습니다. 예를 들어, 사용자가 자신이 소유한 블로그 코멘트만 수정 가능하도록 할 수도 있습니다. 대부분의 경우, 이 메서드 내에서 [인가 게이트와 정책](/docs/12.x/authorization)과 상호작용하게 됩니다.

```php
use App\Models\Comment;

/**
 * 사용자가 이 요청을 수행할 권한이 있는지 판단합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 기본 라라벨 리퀘스트 클래스를 상속하므로, `user` 메서드를 통해 현재 인증된 사용자를 가져올 수 있습니다. 위 예시에서는 `route` 메서드를 활용해, 요청 라우트에서 정의된 URL 파라미터에 접근하는 점도 참고하세요. 예컨대 `{comment}` 파라미터가 포함된 아래 라우트와 같이요.

```php
Route::post('/comment/{comment}');
```

따라서 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용한다면, request의 속성으로 바인딩된 모델에 바로 접근해 코드를 더 간결하게 만들 수도 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, 컨트롤러 메서드는 실행되지 않고 403 상태 코드의 HTTP 응답이 자동으로 반환됩니다.

요청에 대한 인가(Authorization) 로직을 애플리케이션의 다른 곳에서 처리하고자 한다면, `authorize` 메서드를 아예 삭제하거나 항상 `true`를 반환하게 해도 무방합니다.

```php
/**
 * 사용자가 이 요청을 수행할 권한이 있는지 판단합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처에 필요한 의존성을 타입힌트로 선언하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 커스터마이즈

폼 리퀘스트에서 사용되는 오류 메시지를 커스터마이즈하려면 `messages` 메서드를 오버라이드하면 됩니다. 이 메서드는 속성/규칙-메시지 쌍의 배열을 반환해야 합니다.

```php
/**
 * 정의한 유효성 검증 규칙에 대한 오류 메시지를 반환합니다.
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

라라벨 내장 유효성 규칙의 오류 메시지 중에는 `:attribute` 플레이스홀더가 포함된 경우가 많습니다. 이 플레이스홀더가 커스텀 속성명으로 대체되길 원한다면, `attributes` 메서드를 오버라이드해 속성명 쌍을 반환하면 됩니다.

```php
/**
 * 유효성 검증 오류에 사용할 커스텀 속성명을 반환합니다.
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
### 유효성 검증을 위한 입력값 준비

유효성 검증 규칙을 적용하기 전에, 요청 데이터 일부를 사전 가공하거나 정규화할 필요가 있다면, `prepareForValidation` 메서드를 활용하세요.

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증을 위한 데이터 사전 준비.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

마찬가지로, 유효성 검증이 완료된 후 요청 데이터를 정규화하고 싶다면 `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * 유효성 검증에 통과한 후 추가 처리.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>

## 수동으로 Validator 인스턴스 생성하기

요청 객체의 `validate` 메서드를 사용하지 않고, 직접 Validator 인스턴스를 생성하여 유효성 검증을 수행할 수도 있습니다. 이때는 `Validator` [파사드](/docs/12.x/facades)의 `make` 메서드를 사용합니다. `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * 새로운 블로그 포스트 저장
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

        // 유효성 검증을 통과한 입력값을 가져옴...
        $validated = $validator->validated();

        // 유효성 검증을 통과한 입력값 중 일부만 가져옴...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // 블로그 포스트 저장 처리...

        return redirect('/posts');
    }
}
```

`make` 메서드에 전달하는 첫 번째 인수는 유효성 검증 대상 데이터이며, 두 번째 인수는 해당 데이터에 적용할 유효성 검증 규칙 배열입니다.

요청 유효성 검증 실패 여부를 확인한 후, `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면, `$errors` 변수가 리다이렉션 이후 뷰에 자동으로 공유되어 사용자에게 쉽게 에러를 표시할 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, PHP `array` 모두를 인자로 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 중지

`stopOnFirstFailure` 메서드는 유효성 검증 과정에서 최초로 실패한 항목이 있으면, 그 이후의 모든 속성에 대한 검증을 즉시 중단하도록 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

Validator 인스턴스를 수동으로 생성하면서도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 활용하고 싶을 때는, 기존 Validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 유효성 검증에 실패하면, 사용자는 자동으로 리다이렉트되거나 XHR 요청일 경우 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

검증에 실패할 경우 에러 메시지를 [이름이 지정된 에러 백](#named-error-bags)에 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러 백(Named Error Bags)

한 페이지에서 여러 개의 폼을 사용하는 경우, 각각의 폼에 대한 유효성 검증 에러 메시지를 별도로 관리하고 싶을 수 있습니다. 이럴 때는, `withErrors`의 두 번째 인자로 이름을 지정해 `MessageBag`을 구분하여 저장할 수 있습니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

그 후 뷰에서 `$errors` 변수로부터 지정한 이름의 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이즈

필요하다면, 라라벨이 제공하는 기본 에러 메시지 대신 Validator 인스턴스가 사용할 사용자 정의 에러 메시지를 지정할 수 있습니다. 사용자 정의 메시지를 지정하는 방법은 여러 가지가 있습니다. 첫 번째로, `Validator::make` 메서드의 세 번째 인수로 커스텀 메시지를 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위 예시에서 `:attribute` 플레이스홀더는 실제 검증 중인 필드명으로 치환됩니다. 검증 메시지에는 이외에도 다양한 플레이스홀더를 사용할 수 있습니다. 예를 들어:

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

때때로, 특정 속성에만 커스텀 에러 메시지를 지정하고 싶을 수 있습니다. 이럴 때는 "dot" 표기법을 사용해 속성명과 규칙명을 함께 지정하면 됩니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성 이름 지정

라라벨의 기본 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있으며, 이는 검증 중인 필드명 또는 속성명으로 치환됩니다. 특정 필드의 이름 치환값을 커스터마이즈하려면, `Validator::make`의 네 번째 인자로 커스텀 속성 배열을 전달하면 됩니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행하기

기본 유효성 검증이 끝난 뒤, 추가적인 검증 과정을 실행하고 싶을 때는 validator의 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 클로저 또는 콜러블(callable) 배열을 인수로 받아, 검증 완료 후 실행됩니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 전달받아, 필요하다면 추가 에러 메시지를 등록할 수 있습니다.

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

앞서 설명한 대로, `after` 메서드는 콜러블 배열도 받을 수 있으므로, "추가 검증 로직"을 인보커블 클래스에 캡슐화해 둘 경우 매우 유용합니다. 이러한 클래스는 `__invoke` 메서드로 `Illuminate\Validation\Validator` 인스턴스를 전달받게 됩니다.

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
## 유효성 검증된 입력값 다루기

폼 리퀘스트나 수동으로 생성한 validator 인스턴스를 통해 유효성 검증을 마친 후 실제 검증이 수행된 입력 데이터를 가져오고 싶을 때가 있습니다. 이 작업에는 몇 가지 방법이 있습니다. 첫 번째로, 폼 리퀘스트 객체나 validator 인스턴스의 `validated` 메서드를 호출하면 됩니다. 이 메서드는 유효성 검증을 통과한 데이터의 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 리퀘스트 혹은 validator 인스턴스의 `safe` 메서드를 사용할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 반환된 오브젝트에서 `only`, `except`, `all` 메서드를 통해 검증된 데이터의 하위 집합 또는 전체 배열을 가져올 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하거나 배열 형태로 접근할 수도 있습니다.

```php
// 검증된 데이터 반복
foreach ($request->safe() as $key => $value) {
    // ...
}

// 검증된 데이터 배열 접근
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 합치고 싶을 때는 `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 가져오고 싶다면, `collect` 메서드를 사용하면 됩니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 에러 메시지들을 다루기에 편리한 `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 이 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

특정 필드에 대한 첫 번째 에러 메시지를 가져오려면 `first` 메서드를 사용합니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드에 대한 모든 에러 메시지 배열을 가져오고 싶다면 `get` 메서드를 사용합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형태의 폼 필드에 대해 검증할 때는, `*` 문자를 사용해 각 배열 요소에 대한 모든 메시지를 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 필드에 대한 모든 메시지 배열을 얻으려면 `all` 메서드를 사용합니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드의 에러 메시지 존재 여부 확인

`has` 메서드를 사용하면, 특정 필드에 대해 하나 이상의 에러 메시지가 존재하는지 여부를 알 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정

라라벨의 내장 유효성 검증 규칙마다 해당 애플리케이션의 `lang/en/validation.php` 파일에 에러 메시지가 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어를 통해 생성할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙별 번역 메시지가 있습니다. 이 메시지는 애플리케이션 필요에 따라 자유롭게 수정할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해 자체 언어로 번역할 수도 있습니다. 라라벨의 로컬라이제이션에 대해 더 자세히 알고 싶다면, 전체 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어로 파일을 퍼블리시해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성의 커스텀 메시지

특정 속성 및 규칙 조합에 대해 사용되는 에러 메시지는 애플리케이션의 validation 언어 파일의 `custom` 배열에서 커스텀할 수 있습니다. 아래와 같이 메시지를 추가하세요.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 이름 지정

라라벨의 내장 에러 메시지들은 `:attribute` 플레이스홀더를 포함하며, 이는 유효성 검증 대상 필드명 또는 속성명으로 치환됩니다. 이 치환값을 커스터마이즈하고 싶다면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열을 사용해 지정할 수 있습니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어로 파일을 퍼블리시해야 합니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값(Value) 지정

라라벨의 일부 내장 유효성 검증 규칙의 에러 메시지에는 `:value` 플레이스홀더가 포함되어 있으며, 검증 대상 속성의 현재 값으로 치환됩니다. 경우에 따라 이 값을 좀 더 사용자 친화적인 표현으로 바꾸고 싶을 수 있습니다. 예를 들어, `payment_type` 필드의 값이 `cc`일 때 신용카드 번호가 필수인 유효성 검증 규칙을 보겠습니다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 유효성 검증이 실패하면 아래와 같은 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

`cc`라는 값 대신 좀 더 이해하기 쉬운 표현을 쓰고 싶다면, `lang/xx/validation.php` 언어 파일 안의 `values` 배열에 값을 매핑해줄 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어로 파일을 퍼블리시해야 합니다.

이 값을 정의하고 나면, 아래와 같이 더 유저 친화적인 메시지가 표시됩니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙

아래는 사용할 수 있는 모든 유효성 검증 규칙 목록과 그 기능입니다.

#### 불리언(Booleans)

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### 문자열(Strings)

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

#### 숫자(Numbers)

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

#### 배열(Arrays)

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

#### 날짜(Dates)

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

#### 파일(Files)

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

#### 데이터베이스(Database)

<div class="collection-method-list" markdown="1">

[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

#### 유틸리티(Utilities)

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

검증 대상 필드 값은 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 주로 서비스 약관 동의 등과 비슷한 항목 검증에 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

다른 검증 대상 필드의 값이 특정 값과 같을 경우, 이 필드도 반드시 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 서비스 약관 동의 등 유사 필드의 조건부 검증에 사용됩니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드의 값은 `dns_get_record` PHP 함수 기준으로 유효한 A 또는 AAAA 레코드를 가져야 합니다. URL에 제공된 호스트명은 `parse_url` PHP 함수로 추출한 뒤 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드는 지정된 날짜 이후여야 합니다. 이때 날짜는 `strtotime` PHP 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`으로 판별할 날짜 문자열 대신, 다른 필드명을 지정해 그 값을 기준으로 비교할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

좀 더 간편하게 date 기반 규칙을 작성하고 싶다면, 유창한 `date` 규칙 빌더를 사용할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드를 사용하면, 날짜가 오늘 이후이거나 오늘 또는 이후임을 유창하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>

#### after\_or\_equal:_date_

검증 중인 필드는 지정된 날짜와 같거나 이후의 값이어야 합니다. 더 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

날짜 기반 규칙을 더 편리하게 작성하려면 fluent한 `date` 규칙 빌더를 사용할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 검증 규칙을 사용하면 검증 중인 필드가 지정된 여러 검증 규칙 집합 중 하나라도 통과해야 함을 지정할 수 있습니다. 예를 들어 아래 규칙은 `username` 필드가 이메일 주소이거나 6자 이상의 영숫자 문자열(대시 포함)임을 검증합니다.

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

검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) 범위에 해당하는 유니코드 알파벳 문자만으로 이루어져 있어야 합니다.

이 규칙을 ASCII 문자(`a-z`, `A-Z`)만 허용하도록 제한하려면 `ascii` 옵션을 규칙에 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) 범위의 유니코드 영숫자 문자만, 그리고 ASCII 대시(`-`)와 언더스코어(`_`)만으로 이루어져 있어야 합니다.

이 규칙을 ASCII 문자(`a-z`, `A-Z`, `0-9`)만 허용하도록 제한하려면 `ascii` 옵션을 사용할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) 범위의 유니코드 영숫자 문자만으로 이루어져 있어야 합니다.

이 규칙을 ASCII 영숫자(`a-z`, `A-Z`, `0-9`)로만 제한하려면 `ascii` 옵션을 사용합니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 중인 필드는 PHP의 `array` 타입이어야 합니다.

`array` 규칙에 추가 값을 지정하면 입력 배열의 각 키가 해당 값 목록에 포함되어야 합니다. 아래 예시에서 입력 배열의 `admin` 키는 규칙에 지정된 값 목록에 없으므로 잘못된 값입니다.

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

일반적으로 배열에 어떤 키가 허용되는지 반드시 명시하는 것을 권장합니다.

<a name="rule-ascii"></a>
#### ascii

검증 중인 필드는 반드시 7비트 ASCII 문자로만 구성되어 있어야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드에 대해 최초의 검증 실패 이후에는 더 이상의 검증 규칙을 실행하지 않습니다.

`bail` 규칙은 특정 필드의 검증을 실패 시 중단하지만, `stopOnFirstFailure` 메서드는 하나의 검증 실패가 발생하면 모든 속성의 검증을 중단하도록 Validator에 지시합니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 중인 필드는 지정된 날짜 이전의 값이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 검증 중인 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

날짜 기반 규칙을 더 편리하게 작성하려면 fluent한 `date` 규칙 빌더를 사용할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`와 `todayOrBefore` 메서드를 활용하면 날짜가 오늘 이전이거나, 오늘 혹은 그 이전이어야 한다는 조건을 fluent하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

검증 중인 필드는 지정된 날짜와 같거나 그 이전이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 검증 중인 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

날짜 기반 규칙을 더 편리하게 작성하려면 fluent한 `date` 규칙 빌더를 사용할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

검증 중인 필드는 지정된 _min_ 및 _max_ 범위(포함) 내의 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

검증 중인 필드는 불리언으로 변환될 수 있는 값이어야 합니다. 허용되는 입력값은 `true`, `false`, `1`, `0`, `"1"`, `"0"` 입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 중인 필드는 `{field}_confirmation` 형식의 일치하는 필드가 있어야 합니다. 예를 들어, 검증 대상이 `password`라면, 입력값에 반드시 `password_confirmation` 필드가 함께 있어야 하고 두 값이 동일해야 합니다.

사용자 정의 확인 필드명을 전달할 수도 있습니다. 예를 들어 `confirmed:repeat_username`을 사용하면, 해당 필드는 `repeat_username` 필드와 값이 일치해야 합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

검증 중인 필드는 지정된 모든 파라미터 값을 포함해야 하는 배열이어야 합니다. 이 규칙은 보통 배열을 `implode` 해야 할 때 자주 사용되므로, `Rule::contains` 메서드를 활용하면 fluent하게 규칙을 만들 수 있습니다.

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

검증 중인 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 파라미터를 사용해 [인증 가드](/docs/12.x/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 중인 필드는 PHP의 `strtotime` 함수에서 지원하는 유효한 날짜(상대 날짜는 불가)여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 중인 필드는 지정된 날짜와 완전히 일치해야 합니다. 날짜는 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 중인 필드는 지정된 _formats_ 중 하나와 형식이 일치해야 합니다. 필드 유효성 검증 시에는 `date` 또는 `date_format` 중 **하나만** 사용해야 하며, 두 규칙을 같이 사용해서는 안 됩니다. 이 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 형식을 지원합니다.

날짜 기반 규칙을 더 편리하게 작성하려면 fluent한 `date` 규칙 빌더를 사용할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

검증 중인 필드는 숫자여야 하며, 지정된 소수점 자릿수를 가져야 합니다.

```php
// 소수점 아래 정확히 두 자리(9.99)여야 함
'price' => 'decimal:2'

// 소수점 아래 2~4자리 허용
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

다른 특정 필드가 지정된 값과 일치할 경우, 검증 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 중인 필드는 _field_ 와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 중인 정수는 반드시 _value_ 자릿수만큼 정확한 길이를 가져야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 중인 정수의 자릿수는 지정된 _min_과 _max_ 범위 내에 있어야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 중인 파일은 규칙의 파라미터로 지정한 이미지 크기 제약을 만족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건은 다음과 같습니다: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

_ratio_ 제약은 너비를 높이로 나눈 값을 의미하며, 분수(`3/2`) 또는 소수(`1.5`)로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

이 규칙은 여러 인자 지정이 필요하기 때문에, `Rule::dimensions` 메서드를 사용해 fluent하게 규칙을 만들면 보다 편리합니다.

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

배열 검증 시, 각 항목의 값이 중복되어서는 안 됩니다.

```php
'foo.*.id' => 'distinct'
```

기본적으로 distinct는 느슨한(형 변환을 허용하는) 비교를 사용합니다. 엄격한(타입까지 일치하는 경우) 비교를 쓰려면 `strict` 파라미터를 추가하세요.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 구분을 무시하려면 `ignore_case`를 규칙의 인자에 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증 중인 필드는 지정된 값 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증 중인 필드는 지정된 값 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

검증 중인 필드는 이메일 주소 형식이어야 합니다. 이 검증 규칙은 이메일 주소 유효성 검증을 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 검증기가 적용되지만, 다른 검증 스타일도 지정할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예시에서는 `RFCValidation`과 `DNSCheckValidation`이 모두 적용됩니다. 적용 가능한 전체 검증 스타일은 아래와 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따른 이메일 주소 유효성 검증.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따른 확인, 경고(예: 마지막에 오는 점, 연속 두 번의 점 등)가 있으면 실패.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인.
- `spoof`: `SpoofCheckValidation` - 동형 이의어(homograph)나 속이는 유니코드 문자가 포함되지 않았는지 확인.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일 유효성 검증.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수 기준에 일부 유니코드 문자 허용 포함해 이메일 유효성 검증.

</div>

이메일 검증 규칙 역시 fluent rule builder로 작성할 수 있습니다.

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
> `dns` 및 `spoof` 검증기는 PHP `intl` 확장이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증 중인 필드는 지정된 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 해당 필드 값이 유효한 Enum 값인지 검증하는 클래스 기반 규칙입니다. `Enum` 규칙은 생성자 인자로 enum 이름만 받습니다. 원시값 기반 Enum을 검증할 때는 backed Enum을 인자로 제공해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`와 `except` 메서드를 사용하면 유효한 enum 값을 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 활용하면 특정 조건에 따라 `Enum` 규칙을 동적으로 변경할 수 있습니다.

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

검증 중인 필드는 `validate` 및 `validated` 메서드를 통해 반환되는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

다른 필드가 _value_ 와 같을 때, 검증 중인 필드는 `validate` 및 `validated` 메서드로 반환되는 요청 데이터에서 제외됩니다.

복잡한 조건으로 필드를 제외해야 한다면 `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 인자로 받으며, 클로저의 반환 값이 `true`이면 필드를 제외합니다.

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

다른 필드 값이 _value_ 와 같지 않으면, 검증 중인 필드는 `validate` 및 `validated` 메서드에서 반환되는 요청 데이터에서 제외됩니다. _value_ 가 `null`(`exclude_unless:name,null`)일 경우, 비교 대상 필드가 `null`이거나 존재하지 않으면 검증 중인 필드가 제외됩니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

다른 필드가 요청 데이터에 존재할 때, 검증 중인 필드는 `validate` 및 `validated` 메서드에서 반환되는 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

다른 필드가 요청 데이터에 존재하지 않을 때, 검증 중인 필드는 `validate` 및 `validated` 메서드에서 반환되는 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 중인 필드는 지정된 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 지정하지 않으면, 검증 대상 필드명이 그대로 사용됩니다. 위 예시에서는 요청의 `state` 값이 `states` 테이블의 `state` 컬럼에 존재하는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 지정 컬럼 이름 명시

원하는 데이터베이스 컬럼명을 테이블명 뒤에 명시하면, 해당 컬럼을 기준으로 검증할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

`exists` 쿼리에 특정 데이터베이스 연결을 사용해야 하는 경우, 테이블명 앞에 연결 이름을 붙여서 지정할 수 있습니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, Eloquent 모델명을 지정하여 테이블명을 유추하도록 할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

검증 규칙이 실행하는 쿼리를 직접 커스텀하고 싶다면, `Rule` 클래스를 사용해서 규칙을 fluent하게 정의할 수 있습니다. 이 예제에서는 규칙을 배열로 나열하여 `|` 대신 사용하는 예시도 보여줍니다.

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

`Rule::exists` 메서드에 컬럼명을 두 번째 인자로 전달하면, 해당 컬럼을 기준으로 `exists` 검증 규칙을 명시할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

배열 내 여러 값이 데이터베이스에 존재하는지 검증하려면, 해당 필드에 `exists`와 [array](#rule-array) 규칙을 모두 지정하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이 두 규칙이 모두 지정되면, Laravel은 지정된 모든 값이 테이블에 존재하는지 단일 쿼리로 자동 검증합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 중인 파일은 나열한 확장자 중 하나를 사용자 할당 확장자로 가져야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일의 사용자 할당 확장자만으로 파일을 검증하는 데 절대 의존해서는 안 됩니다. 이 규칙은 보통 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 항상 함께 사용하는 것이 안전합니다.

<a name="rule-file"></a>
#### file

검증 중인 필드는 정상적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

검증 중인 필드는 입력 데이터에 존재한다면 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 중인 필드는 지정된 _field_ 또는 _value_ 보다 커야 합니다. 두 필드의 타입은 같아야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 중인 필드는 지정된 _field_ 또는 _value_ 이상이어야 합니다. 두 필드의 타입이 같아야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

검증 중인 필드는 [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 컬러 값이어야 합니다.

<a name="rule-image"></a>
#### image

검증 중인 파일은 이미지여야 하며, 파일 형식은 jpg, jpeg, png, bmp, gif, webp 중 하나이어야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 보안 취약점 가능성으로 인해 SVG 파일을 허용하지 않습니다. SVG 파일을 허용하려면 `image:allow_svg` 디렉티브를 image 규칙에 추가합니다.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 중인 필드는 지정한 값 목록에 포함되어야 합니다. 배열을 `implode` 해야 할 때가 많으므로, `Rule::in` 메서드를 사용하면 규칙 작성이 더 직관적입니다.

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

`in` 규칙과 `array` 규칙을 함께 사용할 경우, 입력 배열의 각 값이 `in` 규칙에 나열된 값 목록에 모두 포함되어야 합니다. 아래 예시에서 입력 배열의 `LAS` 공항 코드는 값 목록에 없으므로 유효하지 않습니다.

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

검증 중인 필드의 값이 _anotherfield_의 값들 중에 존재해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 중인 필드는 배열이어야 하며, 해당 배열에 지정한 _values_ 중 적어도 하나 이상을 키로 가지고 있어야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증 중인 필드의 값은 정수여야 합니다.

> [!WARNING]
> 이 유효성 검사는 입력값이 "integer" 타입 변수인지 실제로 확인하지 않으며, PHP의 `FILTER_VALIDATE_INT`에서 허용하는 타입인지만 확인합니다. 숫자인지 엄밀하게 검사하고 싶다면 이 규칙을 [numeric](#rule-numeric) 유효성 검사와 함께 사용하시기 바랍니다.

<a name="rule-ip"></a>
#### ip

검증 중인 필드의 값은 IP 주소이어야 합니다.

<a name="ipv4"></a>
#### ipv4

검증 중인 필드의 값은 IPv4 주소이어야 합니다.

<a name="ipv6"></a>
#### ipv6

검증 중인 필드의 값은 IPv6 주소이어야 합니다.

<a name="rule-json"></a>
#### json

검증 중인 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증 중인 필드의 값은 지정한 _field_의 값보다 작아야 합니다. 두 필드는 동일한 타입이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가합니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 중인 필드의 값은 지정한 _field_의 값보다 작거나 같아야 합니다. 두 필드는 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가합니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 중인 필드의 값은 모두 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증 중인 필드는 배열이어야 하며, 이 배열은 리스트 형태이어야 합니다. 리스트란 배열의 키가 0부터 `count($array) - 1`까지 연속된 숫자일 때를 의미합니다.

<a name="rule-mac"></a>
#### mac_address

검증 중인 필드는 MAC 주소이어야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 중인 필드의 값은 최대 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 같은 방식으로 평가합니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 중인 정수 값에는 최대 _value_ 자리수까지만 허용됩니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 대상 파일의 MIME 타입이 지정한 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드된 파일의 MIME 타입을 확인하기 위해, 라라벨은 파일의 내용을 읽고 MIME 타입을 추정합니다. 이 과정에서 클라이언트가 제공한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 대상 파일은 지정한 확장자 목록과 대응되는 MIME 타입이어야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하지만, 실제로는 파일의 내용을 읽어 유효한 MIME 타입인지 판단합니다. MIME 타입과 해당 확장자 전체 목록은 다음 위치에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 검사는 파일의 MIME 타입과 파일 확장자가 일치하는지까지는 확인하지 않습니다. 예를 들어, `mimes:png` 규칙은 실제로 PNG 포맷인 파일은 파일명이 `photo.txt`여도 유효한 PNG 이미지로 판단합니다. 사용자에게 할당된 파일 확장자까지 검사하고 싶다면 [extensions](#rule-extensions) 규칙을 사용하시기 바랍니다.

<a name="rule-min"></a>
#### min:_value_

검증 중인 필드는 최소 _value_ 값 이상이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 같은 방식으로 평가합니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 중인 정수 값은 최소 _value_ 자리수 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 중인 필드의 값은 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

입력 데이터에 검증 중인 필드가 존재하면 안 됩니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_또다른 필드(_anotherfield_)가 지정한 _value_와 같으면, 검증 중인 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_또다른 필드(_anotherfield_)가 지정한 _value_와 같지 않으면, 검증 중인 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

다른 지정한 필드들 중 하나라도 존재한다면, 검증 중인 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

모든 지정한 필드가 모두 존재하는 경우에만, 검증 중인 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 중인 필드의 값이 지정한 값 목록에 포함되어 있으면 안 됩니다. `Rule::notIn` 메서드를 사용해 좀 더 명확하게 규칙을 구성할 수 있습니다.

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

검증 중인 필드는 지정한 정규 표현식과 일치하지 않아야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 패턴은 `preg_match`에서 요구하는 형식과 구분자를 반드시 함께 사용해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`

> [!WARNING]
> `regex` 또는 `not_regex` 규칙에서 패턴에 `|` 문자가 포함된다면, 유효성 검사 규칙 전체를 배열로 지정하는 것을 권장합니다.

<a name="rule-nullable"></a>
#### nullable

검증 중인 필드는 `null`이어도 무방합니다.

<a name="rule-numeric"></a>
#### numeric

검증 중인 필드는 [숫자(numeric)](https://www.php.net/manual/en/function.is-numeric.php)여야 합니다.

<a name="rule-present"></a>
#### present

검증 중인 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_또다른 필드(_anotherfield_)가 지정한 _value_ 중 하나와 같을 때, 검증 중인 필드는 반드시 입력 데이터에 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_또다른 필드(_anotherfield_)가 지정한 _value_와 같지 않을 때, 검증 중인 필드는 반드시 입력 데이터에 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

다른 지정한 필드들 중 하나라도 존재하는 경우에만, 검증 중인 필드는 반드시 입력 데이터에 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

모든 지정한 필드가 모두 존재하는 경우에만, 검증 중인 필드는 반드시 입력 데이터에 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 중인 필드는 입력 데이터에 없어야 하거나, "비어 있는" 값이어야 합니다. "비어 있음"이란 다음 경우를 포함합니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드 파일이 경로만 있고 실제 내용이 없는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_또다른 필드(_anotherfield_)가 지정한 _value_ 중 하나와 같을 때, 검증 중인 필드는 입력 데이터에 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드 파일이 경로만 있고 실제 내용이 없는 경우

</div>

복잡한 조건의 금지(prohibit) 로직이 필요하다면, `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 인자로 받으며, 클로저를 사용하는 경우 `true` 또는 `false`를 반환해야 해당 필드의 금지 여부를 결정할 수 있습니다.

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

_또다른 필드(_anotherfield_)가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나와 같으면, 검증 중인 필드는 입력 데이터에 없어야 하거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_또다른 필드(_anotherfield_)가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나와 같으면, 검증 중인 필드는 입력 데이터에 없어야 하거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_또다른 필드(_anotherfield_)가 지정한 _value_ 중 하나와 같지 않으면, 검증 중인 필드는 입력 데이터에 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드 파일이 경로만 있고 실제 내용이 없는 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 중인 필드가 입력 데이터에 존재하거나 비어 있지 않은 경우, _anotherfield_에 지정한 모든 필드는 입력 데이터에 없어야 하거나 비어 있어야 합니다. "비어 있음"의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드 파일이 경로만 있고 실제 내용이 없는 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증 중인 필드는 지정한 정규 표현식과 일치해야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 패턴은 `preg_match`에서 요구하는 형식과 유효한 구분자가 포함되어야 합니다. 예시: `'email' => 'regex:/^.+@.+$/i'`

> [!WARNING]
> `regex` 또는 `not_regex` 규칙에서 패턴에 `|` 문자가 포함될 경우, 유효성 검사 규칙 전체를 배열로 지정해야 정상적으로 동작합니다.

<a name="rule-required"></a>
#### required

검증 중인 필드는 입력 데이터에 반드시 존재해야 하며, "비어 있지 않은" 값이어야 합니다. "비어 있음"이란 다음 경우를 의미합니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 빈 `Countable` 객체인 경우
- 업로드 파일이 경로만 있고 실제 내용이 없는 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_또다른 필드(_anotherfield_)가 지정한 _value_ 중 하나와 같을 때, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

보다 복잡한 조건으로 `required_if` 규칙을 구성하려면, `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언이나 클로저를 인자로 받으며, 클로저 사용 시 `true` 또는 `false`를 반환하면 해당 조건에서 필드가 필수(required)인지 결정하게 됩니다.

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

_또다른 필드(_anotherfield_)가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나와 같을 때, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_또다른 필드(_anotherfield_)가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나와 같을 때, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_또다른 필드(_anotherfield_)가 지정한 _value_ 중 하나와 같지 않은 경우, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다. 또한 _anotherfield_는 _value_가 `null`이 아닌 경우 요청 데이터에 필수로 존재해야 합니다. 만약 _value_가 `null`(`required_unless:name,null`)인 경우, 비교할 필드가 `null`이거나 요청 데이터에서 존재하지 않으면 검증 대상 필드는 필수로 간주되지 않습니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

다른 지정한 필드들 중 하나라도 존재하고 비어 있지 않은 경우, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

모든 지정한 필드가 존재하고 비어 있지 않은 경우, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

다른 지정한 필드들 중 하나라도 비어 있거나 존재하지 않을 경우에만, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

지정한 모든 필드들이 모두 비어 있거나 존재하지 않을 때만, 검증 중인 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증 중인 필드는 배열이어야 하며, 지정한 키들을 반드시 모두 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정한 _field_의 값이 검증 중인 필드의 값과 반드시 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증 중인 필드의 크기가 지정한 _value_와 정확히 일치해야 합니다. 문자열 데이터의 경우 _value_는 문자 개수, 숫자 데이터의 경우 _value_는 특정 정수값(단, `numeric` 또는 `integer` 규칙 동시 필요), 배열의 경우 요소 개수, 파일은 킬로바이트(1KB) 단위의 파일 크기와 비교합니다. 예시는 다음과 같습니다.

```php
// 문자열이 정확히 12글자인지 검사
'title' => 'size:12';

// 정수값이 10과 일치하는지 검사
'seats' => 'integer|size:10';

// 배열의 요소가 정확히 5개인지 검사
'tags' => 'array|size:5';

// 파일 용량이 정확히 512KB인지 검사
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 중인 필드의 값이 지정한 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 중인 필드는 문자열이어야 합니다. 만약 해당 필드가 `null` 값 또한 허용하려면, `nullable` 규칙을 함께 지정하면 됩니다.

<a name="rule-timezone"></a>
#### timezone

검증 중인 필드는 `DateTimeZone::listIdentifiers` 메서드에 따라 유효한 타임존 식별자여야 합니다.

`DateTimeZone::listIdentifiers` 메서드에서 허용하는 인수들도 이 유효성 검사에서 전달 가능합니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증 중인 필드의 값이 지정한 데이터베이스 테이블에 이미 존재하면 안 됩니다.

**커스텀 테이블 및 컬럼명 지정하기:**

테이블명을 직접 지정하는 대신, Eloquent 모델을 지정해 해당 모델이 사용하는 테이블로 검증을 진행할 수도 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션을 사용하면, 해당 필드가 매핑되는 데이터베이스 컬럼명을 명시할 수 있습니다. 생략하면 필드명과 동일한 컬럼명을 자동으로 사용합니다.

```php
'email' => 'unique:users,email_address'
```

**커스텀 데이터베이스 연결 지정하기**

때때로 Validator가 쿼리할 데이터베이스 연결을 명시적으로 지정해야 할 수 있습니다. 이럴 땐 테이블명 앞에 연결명(connection name)을 붙여줍니다.

```php
'email' => 'unique:connection.users,email_address'
```

**특정 ID 무시하고 unique 검사하기:**

일부 상황에서는 unique 검증 시 지정한 ID(예: 기존 레코드의 ID)를 무시해야 할 수도 있습니다. 예를 들어, 프로필 업데이트 화면에서 이름과 이메일, 위치 정보가 있을 때, 이메일이 기존과 달라졌을 때만 중복 검사를 하고, 사용자가 본인 이메일을 유지할 경우에는 오류가 발생하지 않아야 합니다.

이런 경우, Validator에게 해당 사용자의 ID를 무시한 채 unique 검사를 하도록 `Rule` 클래스를 활용해 규칙을 선언합니다. 이 예시처럼, 규칙 전체를 배열로 선언하면 됩니다.

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
> 사용자 요청(request)에서 받은 입력값을 그대로 `ignore` 메서드에 전달해서는 안 됩니다. 시스템적으로 생성된 고유한 식별자(예: 자동 증가 ID, Eloquent 모델의 UUID 등)만 사용하십시오. 그렇지 않으면 SQL 인젝션 공격에 노출될 수 있습니다.

모델 키 값이 아니라 아예 모델 인스턴스를 그대로 전달해도, 라라벨이 알아서 기본키를 추출해서 처리해줍니다.

```php
Rule::unique('users')->ignore($user)
```

테이블의 기본키 컬럼명이 `id`가 아닌 경우, `ignore` 메서드에 컬럼명을 두 번째 인자로 함께 전달할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 검증 중인 속성의 이름과 같은 컬럼에서 중복을 확인합니다. 만약 컬럼명이 다르다면, `unique` 메서드의 두 번째 인자로 컬럼명을 지정해 사용할 수 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가적인 where 조건문 지정하기:**

`where` 메서드를 사용해 추가적인 쿼리 조건을 지정할 수도 있습니다. 예를 들어, `account_id` 컬럼이 1인 레코드만 대상으로 unique 검사를 할 수도 있습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**소프트 삭제된 레코드는 unique 검사에서 무시하기:**

기본적으로 unique 규칙은 소프트 삭제된(soft deleted) 레코드까지 검사합니다. 소프트 삭제된 레코드를 무시하려면 `withoutTrashed` 메서드를 사용합니다.

```php
Rule::unique('users')->withoutTrashed();
```

소프트 삭제 컬럼이 `deleted_at`이 아니라면, `withoutTrashed`에 컬럼명을 인자로 전달하면 됩니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증 중인 필드의 값은 모두 대문자여야 합니다.

<a name="rule-url"></a>
#### url

검증 중인 필드는 유효한 URL이어야 합니다.

특정 프로토콜만 허용하고 싶다면, 프로토콜명을 유효성 검사 규칙의 파라미터로 전달할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증 중인 필드는 [ULID(Universally Unique Lexicographically Sortable Identifier)](https://github.com/ulid/spec) 형식이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 중인 필드는 RFC 9562(버전 1, 3, 4, 5, 6, 7, 8 중 하나)의 유효한 UUID이어야 합니다.

특정 버전의 UUID만 허용하도록 추가 옵션을 지정할 수도 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 필드 유효성 검사 건너뛰기

다른 필드가 특정 값일 때, 특정 필드의 유효성 검사 자체를 건너뛰고 싶을 때가 있습니다. 이럴 때는 `exclude_if` 유효성 검사 규칙을 사용할 수 있습니다. 아래 예시에서는 `has_appointment` 필드 값이 `false`일 경우, `appointment_date` 및 `doctor_name` 필드에 대해 유효성 검사를 수행하지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로, `exclude_unless` 규칙을 사용하면 다른 필드가 특정 값이 아닐 때만 유효성 검사를 건너뛸 수도 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>

#### 필드가 존재할 때만 유효성 검사하기

특정 상황에서는, 데이터에 해당 필드가 존재할 때에만 유효성 검사를 실행하고 싶을 때가 있습니다. 이를 빠르게 처리하려면 `sometimes` 규칙을 규칙 리스트에 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예시에서처럼, `$data` 배열에 `email` 필드가 존재하는 경우에만 해당 필드에 대해 유효성 검사가 실행됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드에 대해 유효성 검사를 시도하는 경우, [옵션 필드에 관한 설명](#a-note-on-optional-fields)을 참고하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검사

때로는 더 복잡한 조건부 논리에 따라 유효성 검증 규칙을 추가하고 싶을 수 있습니다. 예를 들어, 어떤 필드가 100보다 큰 값을 가질 때만 다른 필드를 필수로 요구해야 하거나, 또는 특정 필드가 있을 때만 두 필드에 특정한 값을 요구해야 할 수 있습니다. 이러한 조건부 유효성 검증도 어렵지 않게 처리할 수 있습니다. 먼저, 변하지 않는 _고정 규칙(Static Rules)_ 으로 `Validator` 인스턴스를 생성합니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

이제 우리 웹 애플리케이션이 게임 수집가들을 위한 것이라고 가정해 봅시다. 만약 어떤 게임 수집가가 100개가 넘는 게임을 보유한 상태로 회원 가입을 한다면, 왜 이렇게 많은 게임을 소유하고 있는지에 대한 설명을 써주길 원한다고 가정하겠습니다. 예를 들어, 중고 게임 판매점을 운영하거나, 단순히 게임 수집을 즐긴다고 설명할 수도 있습니다. 이 요구사항을 조건부로 추가하려면 `Validator` 인스턴스에 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인수는 조건부로 유효성을 검사할 필드명입니다. 두 번째 인수는 적용하려는 규칙 목록이고, 세 번째 인수로 넘긴 클로저가 `true`를 반환하면 해당 규칙들이 추가됩니다. 이 방식을 활용하면 복잡한 조건부 유효성 검사도 아주 간단하게 작성할 수 있습니다. 여러 필드를 한 번에 조건부로 검증하도록 작성할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저로 전달되는 `$input` 매개변수는 `Illuminate\Support\Fluent` 인스턴스이며, 유효성 검사 대상의 입력값 및 파일에 접근할 때 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 배열 내 조건부 유효성 검사

경우에 따라 중첩 배열 안의 다른 필드값에 따라 어떤 필드값을 조건부로 검사하고 싶지만, 배열 인덱스를 모를 수도 있습니다. 이러한 상황에서는 클로저에서 두 번째 인수로 현재 배열 항목을 받을 수 있으며, 이 두 번째 인수로 각 배열 요소에 대해 개별적인 유효성 검사 조건을 지정할 수 있습니다.

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

위 예시에서처럼, 클로저의 `$input`, `$item` 매개변수 모두 기본적으로 `Illuminate\Support\Fluent` 인스턴스입니다(유효성 검증 대상 데이터가 배열인 경우). 그렇지 않다면 문자열이 될 수도 있습니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[배열 유효성 검사 규칙 문서](#rule-array)에서처럼, `array` 규칙은 허용되는 배열 키 목록을 지정할 수 있습니다. 배열 내부에 추가 키가 있으면 유효성 검사에 실패합니다.

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

일반적으로는 항상 배열에 존재할 수 있는 키를 명확하게 지정해주는 것이 좋습니다. 그렇지 않으면, validator의 `validate` 및 `validated` 메서드는 해당 배열과 모든 키(다른 중첩된 배열 유효성 검사 규칙에 의해 검증되지 않은 키까지 포함)를 반환하게 됩니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력값 유효성 검사

중첩 배열 기반의 폼 입력 필드도 쉽게 유효성 검증할 수 있습니다. 배열 내부 속성은 "닷 표기법(dot notation)"으로 지정할 수 있습니다. 예를 들어, HTTP 요청에 `photos[profile]` 필드가 포함되어 있다면 다음과 같이 유효성 검증이 가능합니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

또한 배열의 각 요소마다 개별 유효성 검사를 적용할 수도 있습니다. 예를 들어, 배열 필드 내 이메일이 모두 고유해야 할 경우 아래와 같이 작성할 수 있습니다.

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

이처럼 [언어 파일에서 사용자정의 유효성 메시지](#custom-messages-for-specific-attributes)를 지정할 때도 `*` 문자를 사용할 수 있어, 배열 기반 필드에 단일 메시지를 쉽게 적용할 수 있습니다.

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 값 접근하기

특정 중첩 배열 요소의 값을 검사 규칙에 활용해야 할 때가 있습니다. 이런 경우 `Rule::forEach` 메서드를 사용하면 됩니다. 이 메서드는 유효성 검증 중인 배열 속성의 각 반복마다, 해당 속성의 값과 확장된 속성명을 클로저에 전달하며, 클로저에서 해당 요소에 적용할 규칙 배열을 반환하면 됩니다.

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
### 에러 메시지의 인덱스와 위치 지정

배열 유효성 검사를 할 때, 어플리케이션에서 에러 메시지를 표시할 때 어떤 항목이 실패했는지 인덱스나 위치 정보를 포함하고 싶을 수 있습니다. 이를 위해 [사용자 정의 유효성 메시지](#manual-customizing-the-error-messages)에 `:index`(0부터 시작), `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다.

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

위 예시의 경우, 검증에 실패하면 _"Please describe photo #2."_ 와 같은 에러 메시지가 사용자에게 표시됩니다.

필요하다면 더 깊이 중첩된 인덱스 및 위치도 `second-index`, `second-position`, `third-index`, `third-position` 등으로 지정할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 유효성 검사

라라벨에서는 파일 업로드 검증을 위한 여러 가지 유효성 검사 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 파일 유효성 검사 시 각각의 규칙을 개별적으로 지정할 수도 있지만, 더욱 편리하게 사용할 수 있는 "플루언트(유창한) 파일 유효성 규칙 빌더"도 제공합니다.

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
#### 파일 유형 유효성 검사

`types` 메서드를 사용할 때는 확장자만 지정하면 되지만, 실제로 이 메서드는 파일 내용을 분석하여 MIME 타입을 추정하고 해당하는 확장자와 일치하는지 검사합니다. MIME 타입 전체 목록과 각 확장자 매핑은 아래에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 유효성 검사

편의를 위해 파일 크기의 최소/최대값을 문자열로 지정할 때 단위를 붙여 쓸 수 있습니다. `kb`, `mb`, `gb`, `tb` 접미사가 지원됩니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 유효성 검사

애플리케이션에서 사용자가 이미지를 업로드하는 경우, `File` 규칙의 `image` 생성 메서드를 사용하여 jpg, jpeg, png, bmp, gif, webp 파일이 업로드됐는지 검사할 수 있습니다.

또한, `dimensions` 규칙을 사용하면 이미지의 크기를 제한할 수도 있습니다.

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
> 이미지 크기(치수)에 대한 검증 방법의 더 많은 정보는 [dimension 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약성 위험 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 한다면, `image` 규칙에 `allowSvg: true` 옵션을 전달하세요: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(치수) 유효성 검사

이미지의 크기도 쉽게 검증할 수 있습니다. 예를 들어, 업로드된 이미지가 너비 1000픽셀 이상, 높이 500픽셀 이상이어야 한다면 다음과 같이 `dimensions` 규칙을 사용할 수 있습니다.

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
> 이미지 크기 검증에 대한 더 많은 내용은 [dimension 규칙 문서](#rule-dimensions)를 참고하세요.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검사

비밀번호가 충분히 복잡한지 검증하기 위해, 라라벨의 `Password` 규칙 객체를 활용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체를 사용하면 비밀번호 최소 길이, 문자/숫자/특수문자 포함, 대소문자 혼합 등 다양한 복잡성 요건을 손쉽게 지정할 수 있습니다.

```php
// 최소 8자리 요구...
Password::min(8)

// 최소 한 글자 이상 포함...
Password::min(8)->letters()

// 대문자와 소문자 각각 최소 한 글자 이상 포함...
Password::min(8)->mixedCase()

// 숫자 최소 한 자리 포함...
Password::min(8)->numbers()

// 기호(특수문자) 최소 한 개 포함...
Password::min(8)->symbols()
```

또한, 공개된 비밀번호 유출 데이터에서 해당 비밀번호가 유출된 적이 없는지 `uncompromised` 메서드를 이용해 검사할 수도 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로 이 `Password` 규칙 객체는 [k-익명성(k-Anonymity)](https://ko.wikipedia.org/wiki/K-익명성) 모델을 사용하며, [haveibeenpwned.com](https://haveibeenpwned.com) 서비스에서 유출 여부를 확인하지만, 사용자의 개인정보나 보안을 침해하지 않습니다.

기본적으로, 데이터 유출 목록에 해당 비밀번호가 한 번이라도 등장하면 "유출된 비밀번호"로 간주합니다. 이 기준치(threshold)는 `uncompromised` 메서드의 첫 번째 인수로 조정할 수 있습니다.

```php
// 동일한 데이터 유출 목록에 3회 미만으로 등장 시에만 허용...
Password::min(8)->uncompromised(3);
```

위의 모든 메서드는 체이닝해서 사용할 수 있습니다.

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

비밀번호에 대한 기본 유효성 검사 규칙을 애플리케이션 한 곳에서 지정하고 싶을 때가 있습니다. `Password::defaults` 메서드를 사용하면 아주 쉽게 구현할 수 있습니다. 이 메서드는 클로저를 인수로 받고, 여기서 `Password` 규칙의 기본 구성을 반환해야 합니다. 일반적으로 이 코드는 애플리케이션의 서비스 프로바이더 내 `boot` 메서드에서 호출합니다.

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

이렇게 하면 특정 비밀번호에 대해 기본 규칙을 적용하고 싶을 때 인수를 생략하고 `defaults` 메서드를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

기본 비밀번호 규칙에 추가 유효성 검증 규칙을 연결하고 싶을 때는 `rules` 메서드를 사용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 사용자 정의 유효성 검사 규칙

<a name="using-rule-objects"></a>
### 규칙 객체(Rule Object) 사용

라라벨은 다양한 유용한 유효성 검증 규칙을 제공하지만, 여러분만의 사용자 정의 규칙을 만들고 싶을 수도 있습니다. 가장 표준적인 방법은 "규칙 객체(Rule Object)"를 이용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` 아티즌 명령어를 사용합니다. 예를 들어, 문자열이 모두 대문자인지 확인하는 규칙을 만든다고 가정해 봅시다. 라라벨은 새 규칙 파일을 `app/Rules` 디렉터리에 생성합니다. (해당 디렉터리가 없다면 명령 실행 시 자동으로 만들어집니다.)

```shell
php artisan make:rule Uppercase
```

규칙이 생성되면 그 동작 방식을 구현할 수 있습니다. 규칙 객체는 하나의 핵심 메서드인 `validate`를 포함하고 있습니다. 이 메서드는 속성명(attribute), 값(value), 그리고 실패 시 호출해야 할 $fail 콜백을 받습니다. $fail 콜백에는 에러 메시지를 전달합니다.

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

이렇게 규칙이 완성되었으면, 다른 유효성 검사 규칙들과 함께 규칙 객체의 인스턴스를 검증기에 전달해서 사용할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 메시지 번역하기

$fail 클로저에 직접 에러 메시지 문자열을 전달하는 대신, [번역 문자열 키](/docs/12.x/localization)를 전달하여 라라벨에서 해당 메시지를 번역하게 할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면, `translate` 메서드의 첫 번째와 두 번째 인수로 치환 값 및 선호하는 언어를 지정할 수도 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

사용자 정의 유효성 검사 규칙 클래스에서 유효성 검사 대상의 전체 데이터를 접근해야 한다면, 규칙 클래스에서 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스는 클래스에 `setData` 메서드를 정의하도록 요구합니다. 이 메서드는 라라벨이 유효성 검사를 실행하기 전에 자동으로 호출하여 전체 데이터를 주입해줍니다.

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

또는, 유효성 검사를 실행 중인 validator 인스턴스에 접근해야 할 경우 `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

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
### 클로저 이용하기

애플리케이션 전체에서 단 한 번만 사용할 기능이라면, 규칙 객체 대신 클로저를 사용할 수도 있습니다. 클로저는 속성명, 값, 그리고 `$fail` 콜백(검증 실패 시 호출할 함수)을 인수로 받습니다.

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

기본적으로, 검사 대상 속성이 존재하지 않거나 빈 문자열일 경우, 기본 유효성 검사 규칙은 실행되지 않습니다. 사용자 정의 규칙도 마찬가지입니다. 예를 들어, [unique](#rule-unique) 규칙은 값이 빈 문자열일 때 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있어도 사용자 정의 규칙을 항상 실행하려면, 해당 규칙이 해당 속성에 대해 "필수" 성격을 암묵적으로 내포해야 합니다. 이러한 규칙 객체를 빠르게 만들려면 `make:rule` 아티즌 명령어에 `--implicit` 옵션을 추가하세요.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙은 단순히 해당 속성이 필수임을 _내포_ 한다는 의미입니다. 실제로 값이 없거나 비어 있을 때 유효하지 않음 처리를 할지는 규칙 구현에 달려 있습니다.