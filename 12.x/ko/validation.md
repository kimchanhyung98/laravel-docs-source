# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠르게 시작하기](#validation-quickstart)
    - [라우트 정의하기](#quick-defining-the-routes)
    - [컨트롤러 생성하기](#quick-creating-the-controller)
    - [유효성 검증 로직 작성하기](#quick-writing-the-validation-logic)
    - [유효성 검증 에러 표시하기](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [옵션(선택) 필드 관련 참고 사항](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 포맷](#validation-error-response-format)
- [폼 리퀘스트(Form Request) 유효성 검증](#form-request-validation)
    - [폼 리퀘스트 생성하기](#creating-form-requests)
    - [폼 리퀘스트 인가 처리](#authorizing-form-requests)
    - [에러 메시지 커스터마이징](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력값 준비하기](#preparing-input-for-validation)
- [수동으로 유효성 검사기(Validator) 생성하기](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [이름 있는 에러 백(Error Bag) 사용하기](#named-error-bags)
    - [에러 메시지 커스터마이징](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [유효성 검증된 입력 데이터 다루기](#working-with-validated-input)
- [에러 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 메시지 지정하기](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정하기](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정하기](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가하기](#conditionally-adding-rules)
- [배열 유효성 검증하기](#validating-arrays)
    - [중첩 배열 입력 검증](#validating-nested-array-input)
    - [에러 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증하기](#validating-files)
- [비밀번호 유효성 검증하기](#validating-passwords)
- [커스텀 유효성 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용하기](#using-rule-objects)
    - [클로저 사용하기](#using-closures)
    - [암묵적(Implicit) 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

라라벨은 애플리케이션의 들어오는 데이터를 검증하는 여러 가지 방법을 제공합니다. 가장 일반적으로는, 모든 들어오는 HTTP 요청에 사용할 수 있는 `validate` 메서드를 이용합니다. 다만, 이 문서에서는 그 외에도 다양한 유효성 검증 방식을 다루고 있습니다.

라라벨은 매우 다양한 편리한 유효성 검증 규칙을 내장하고 있으며, 데이터가 특정 데이터베이스 테이블에서 유일한지까지 검증할 수 있습니다. 본 문서에서는 이 모든 유효성 검증 규칙을 상세히 다루어, 라라벨의 유효성 검증 기능을 충분히 익힐 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠르게 시작하기

라라벨의 강력한 유효성 검증 기능을 익히기 위해, 폼을 검증하고 사용자에게 에러 메시지를 표시하는 예제를 전체적으로 살펴보겠습니다. 이 전체적인 개요를 읽으면, 라라벨에서 들어오는 요청 데이터를 어떻게 검증하는지 전반적인 흐름을 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의하기

먼저, `routes/web.php` 파일에 다음과 같이 라우트를 정의한다고 가정하겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

여기서 `GET` 라우트는 사용자에게 새 블로그 글을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 작성된 새 블로그 글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 위의 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 이 시점에서는 `store` 메서드는 비워두겠습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * 새 블로그 글을 작성하는 폼을 보여줍니다.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * 새 블로그 글을 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 블로그 글 검증 및 저장...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성하기

이제 `store` 메서드에 새 블로그 글 데이터를 검증하는 로직을 추가해보겠습니다. 이 작업을 위해서는 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용하면 됩니다. 유효성 검증 규칙을 통과하면 코드가 정상적으로 계속 실행됩니다. 반면, 유효성 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하면서 적절한 에러 응답이 자동으로 사용자에게 반환됩니다.

일반 HTTP 요청의 경우, 유효성 검증에 실패하면 이전 URL로 자동으로 리디렉션되는 응답이 생성됩니다. 만약 들어오는 요청이 XHR(즉, AJAX) 요청이라면, [유효성 검증 에러 메시지를 담은 JSON 응답](#validation-error-response-format)을 반환합니다.

이제 `store` 메서드에서 `validate` 메서드가 실제로 어떻게 동작하는지 살펴보겠습니다.

```php
/**
 * 새 블로그 글을 저장합니다.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // 블로그 글 데이터가 정상적으로 검증됨...

    return redirect('/posts');
}
```

보시는 것처럼, 유효성 검증 규칙들은 `validate` 메서드에 인수로 전달됩니다. 걱정하지 마세요 — 사용 가능한 모든 유효성 검증 규칙은 [별도의 문서에서](#available-validation-rules) 확인할 수 있습니다. 다시 한 번 강조하면, 유효성 검증에 실패하면 자동으로 적절한 응답이 반환됩니다. 만약 검증에 통과하면 컨트롤러는 정상적으로 계속 실행됩니다.

또한, 검증 규칙은 하나의 `|`로 구분된 문자열에서, 배열 형태로도 지정할 수 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한, 요청을 검증하고 발생한 에러 메시지를 [이름 있는 에러 백](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

어떤 경우에는, 특정 속성(attribute)에 대해 처음 발생한 유효성 검증 에러 이후로는 더 이상 검증 규칙을 적용하지 않고 멈추고 싶을 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예제의 경우, 만약 `title` 필드의 `unique` 규칙이 실패하면 그 뒤의 `max` 규칙은 검사하지 않습니다. 규칙들은 지정된 순서대로 차례로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes) 관련 참고 사항

들어오는 HTTP 요청 데이터에 "중첩된" 필드가 포함되어 있다면, 유효성 검증 규칙에서 "점(dot) 표기법"을 사용하여 이 필드들을 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 만약 필드 이름에 실제 점(.)이 포함된 경우 — 즉, 점을 "점 표기법"으로 인식시키고 싶지 않다면 — 백슬래시를 사용해 점을 이스케이프할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 에러 표시하기

그렇다면, 만약 들어온 요청의 필드들이 주어진 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 설명한 것처럼, 라라벨은 자동으로 사용자를 이전 위치로 리디렉션합니다. 그리고 모든 유효성 검증 에러 및 [요청 입력값](/docs/12.x/requests#retrieving-old-input)은 [세션에 플래시(일시 저장)](/docs/12.x/session#flash-data)됩니다.

`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 `web` 미들웨어 그룹을 사용하는 모든 뷰에서 `$errors` 변수를 공유해줍니다. 이 미들웨어가 적용된 상태라면, 모든 뷰에서 항상 `$errors` 변수가 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. 이 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 활용하는 방법에 대해서는 [관련 문서](#working-with-error-messages)를 참고하세요.

따라서, 이 예제에서는 검증에 실패하면 컨트롤러의 `create` 메서드로 사용자가 리디렉션되며, 이때 뷰에서 에러 메시지를 표시할 수 있습니다.

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

라라벨이 기본적으로 제공하는 유효성 검증 규칙마다, 각각의 에러 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 담겨 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 이를 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에서는 각 유효성 검증 규칙별로 번역 메시지를 정의할 수 있습니다. 필요에 따라 자유롭게 수정하거나 변경할 수 있습니다.

또한, 이 메시지 파일을 다른 언어 디렉터리로 복사하여, 애플리케이션에서 사용할 언어에 맞게 번역할 수 있습니다. 라라벨의 다국어(현지화) 처리에 대해 더 알고 싶다면, [Localization 문서](/docs/12.x/localization)를 참고하시기 바랍니다.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이징하고 싶을 경우, `lang:publish` 아티즌 명령어로 파일을 배포(publish)할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이번 예제에서는 전통적인 폼을 이용해 데이터를 전송했지만, 많은 애플리케이션에서는 JavaScript 기반 프론트엔드로부터 XHR(AJAX) 요청을 받습니다. 이런 경우에도 `validate` 메서드를 사용하면, 라라벨은 리디렉션 응답을 생성하지 않고, [유효성 검증 에러가 포함된 JSON 응답](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 속성(attribute)에 대한 유효성 검증 에러 메시지가 존재하는지 빠르게 확인하려면, [Blade](/docs/12.x/blade)의 `@error` 디렉티브를 사용할 수 있습니다. `@error` 디렉티브 내부에서는 `$message` 변수를 echo 하여 에러 메시지를 표시할 수 있습니다.

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

[이름 있는 에러 백](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인수로 에러 백 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

라라벨이 유효성 검증 에러로 인해 리디렉션 응답을 생성하면, 프레임워크는 모든 요청의 입력값을 [세션에 플래시(일시 저장)](/docs/12.x/session#flash-data)합니다. 이렇게 하면, 사용자가 폼을 다시 작성할 때 입력했던 값을 쉽게 불러와서 폼을 재구성할 수 있습니다.

이전 요청에서 플래시된 입력값을 불러오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. 이 메서드는 [세션](/docs/12.x/session)에서 이전에 플래시된 입력 데이터를 꺼내옵니다.

```php
$title = $request->old('title');
```

라라벨은 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값을 표시할 때는 `old` 헬퍼를 활용하는 것이 더 편리합니다. 지정한 필드에 이전 입력값이 없으면 `null`을 반환합니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 옵션(선택) 필드 관련 참고 사항

기본적으로 라라벨은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함하고 있습니다. 이 때문에 "선택" 요청 필드를 validator가 `null` 값을 에러로 간주하지 않게 하려면, 규칙에 반드시 `nullable`을 명시해주어야 합니다. 예시:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예제에서는, `publish_at` 필드는 `null`이거나 날짜로 변환 가능한 값이면 유효하게 처리됩니다. 만약 규칙 정의에 `nullable`을 명시하지 않으면, validator는 `null` 값을 유효하지 않은 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 포맷

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고, 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, 라라벨은 유효성 검증 에러 메시지를 포맷해서 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

아래 예시는 유효성 검증 에러의 JSON 응답 포맷입니다. 중첩된 에러 키들은 "dot" 표기법으로 평탄화되어 제공된다는 점에 유의하세요.

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
## 폼 리퀘스트(Form Request) 유효성 검증

<a name="creating-form-requests"></a>
### 폼 리퀘스트 생성하기

더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(form request)" 클래스를 만드는 것이 좋습니다. 폼 리퀘스트는 고유의 유효성 검증과 인가 로직을 캡슐화하는 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 생성하려면, `make:request` 아티즌 CLI 명령을 사용하면 됩니다.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, `make:request` 명령을 실행할 때 자동으로 생성됩니다. 라라벨이 생성하는 모든 폼 리퀘스트 클래스에는 `authorize`와 `rules` 두 개의 메서드가 존재합니다.

예상하셨겠지만, `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 나타내는 동작을 수행할 권한이 있는지를 판단합니다. `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드의 시그니처에 필요한 의존성을 타입힌트로 선언할 수 있습니다. 이 경우 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

그렇다면, 유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러의 메서드에서 폼 리퀘스트 타입을 타입힌트로 지정하기만 하면 됩니다. 컨트롤러 메서드가 호출되기 전에 들어오는 폼 리퀘스트가 먼저 검증되므로, 컨트롤러 내부에 유효성 검증 코드를 넣을 필요가 없습니다.

```php
/**
 * 새 블로그 글을 저장합니다.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // 들어온 요청 데이터는 이미 유효함...

    // 유효성 검증된 입력값 가져오기...
    $validated = $request->validated();

    // 검증된 입력값 중 일부만 가져오기...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // 블로그 글 저장...

    return redirect('/posts');
}
```

유효성 검증에 실패하면, 이전 위치로 사용자에게 보낼 리디렉션 응답이 생성됩니다. 에러 정보도 함께 세션에 플래시되어 뷰에서 표시할 수 있게 됩니다. 만약 요청이 XHR이었다면, 422 상태 코드와 [유효성 검증 에러를 포함한 JSON 응답](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> Inertia 기반 라라벨 프론트엔드에서 실시간 폼 리퀘스트 유효성 검증이 필요하다면, [Laravel Precognition](/docs/12.x/precognition)을 확인하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행하기

초기 유효성 검증이 끝난 후 추가로 검증해야 할 사항이 있다면, 폼 리퀘스트의 `after` 메서드를 사용하면 됩니다.

`after` 메서드는, 유효성 검증이 끝난 뒤 호출할 콜러블 또는 클로저 함수의 배열을 반환해야 합니다. 이 때 전달되는 콜러블들은 `Illuminate\Validation\Validator` 인스턴스를 인수로 받으며, 필요하다면 추가적인 에러 메시지를 등록할 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 추가(after) 유효성 검증 콜러블들을 반환합니다.
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

또한, 반환되는 배열에는 호출 가능한(invokable) 클래스도 포함할 수 있습니다. 이런 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * 요청에 대한 추가(after) 유효성 검증 콜러블들을 반환합니다.
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

폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 하나라도 유효성 검증에 실패하면 모든 속성에 대한 검증을 즉시 중단하도록 validator에 지시할 수 있습니다.

```php
/**
 * 하나의 규칙이라도 실패하면 validator가 전체 검증을 중단해야 하는지 여부를 지정합니다.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

폼 리퀘스트 유효성 검증에 실패하면, 기본적으로 사용자가 이전 위치로 리디렉션됩니다. 그러나 직접 이 동작을 커스터마이즈할 수도 있습니다. 폼 리퀘스트에서 `$redirect` 프로퍼티를 지정하면 됩니다.

```php
/**
 * 유효성 검증 실패 시 사용자를 리디렉션할 URI입니다.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

혹은, 지정된 이름의 라우트로 리디렉션하고 싶다면 `$redirectRoute` 프로퍼티를 사용하면 됩니다.

```php
/**
 * 유효성 검증 실패 시 사용자를 리디렉션할 라우트입니다.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 폼 리퀘스트 인가 처리

폼 리퀘스트 클래스는 `authorize` 메서드도 포함하고 있습니다. 이 메서드에서는 인증된 사용자가 실제로 특정 리소스를 업데이트할 권한이 있는지 등을 판단할 수 있습니다. 예를 들어, 사용자가 실제로 업데이트하려는 블로그 댓글을 소유하고 있는지 확인할 수 있습니다. 대개 이 메서드 안에서는 [인가 게이트와 정책](/docs/12.x/authorization)을 활용하게 됩니다.

```php
use App\Models\Comment;

/**
 * 사용자가 이 요청을 수행할 인가 권한이 있는지 판단합니다.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 폼 리퀘스트는 라라벨의 기본 Request 클래스를 확장하므로, `user` 메서드를 사용해 현재 인증된 사용자를 가져올 수 있습니다. 또한 위 예제에서 `route` 메서드를 호출하여, 현재 호출되는 라우트에서 정의한 URI 파라미터(예: 아래의 `{comment}`)를 사용할 수 있다는 점도 참고하세요.

```php
Route::post('/comment/{comment}');
```

따라서, [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용한다면, 요청 객체의 속성으로 바인딩된 모델을 더 간단히 접근할 수도 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면, 자동으로 403 상태 코드와 함께 HTTP 응답이 반환되며 컨트롤러 메서드는 실행되지 않습니다.

만약 요청의 인가 로직을 애플리케이션의 다른 부분에서 처리할 예정이라면, `authorize` 메서드를 아예 제거하거나, 단순히 `true`를 반환하게 만들어도 됩니다.

```php
/**
 * 사용자가 이 요청을 수행할 인가 권한이 있는지 판단합니다.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처에도 필요한 의존성을 타입힌트로 지정할 수 있습니다. 서비스 컨테이너를 통해 자동으로 주입됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

폼 리퀘스트가 사용하는 에러 메시지는 `messages` 메서드를 오버라이드하여 직접 커스터마이징할 수 있습니다. 이 메서드는 속성/규칙 쌍과 이에 대응하는 에러 메시지의 배열을 반환해야 합니다.

```php
/**
 * 정의된 유효성 검증 규칙에 대한 에러 메시지를 반환합니다.
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

라라벨이 기본으로 제공하는 유효성 검증 규칙의 에러 메시지에는 `:attribute` 플레이스홀더가 자주 사용됩니다. 만약 커스텀 속성명으로 이 플레이스홀더를 대체하고 싶다면, `attributes` 메서드를 오버라이드하여 커스텀 속성명을 지정할 수 있습니다. 이 메서드는 속성/이름 쌍의 배열을 반환해야 합니다.

```php
/**
 * validator 에러에 사용할 커스텀 속성명을 반환합니다.
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

유효성 검증 규칙을 적용하기 전에, 요청 데이터를 준비하거나 정제(clean/normalize)해야 할 경우, `prepareForValidation` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

/**
 * 유효성 검증용 데이터 준비.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

마찬가지로, 검증이 끝난 이후에 데이터를 정규화(normalize)할 필요가 있다면, `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * 유효성 검증 통과 후 추가 작업을 처리합니다.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>

## 수동으로 Validator 생성하기

요청(Request) 객체의 `validate` 메서드를 사용하지 않고 직접 검증기를 생성하고 싶을 때는, `Validator` [파사드](/docs/12.x/facades)를 사용할 수 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 만듭니다.

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

`make` 메서드의 첫 번째 인수는 유효성 검증 대상 데이터입니다. 두 번째 인수는 데이터에 적용할 검증 규칙(rule)들의 배열입니다.

요청 유효성 검사가 실패했는지 확인한 후, `withErrors` 메서드를 이용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 redirect 이후에 `$errors` 변수가 자동으로 뷰와 공유되어, 사용자에게 에러 메시지를 손쉽게 표시할 수 있습니다. `withErrors` 메서드는 validator 인스턴스, `MessageBag`, 또는 PHP `array` 모두를 인수로 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 즉시 종료하기

`stopOnFirstFailure` 메서드는 처음 발생한 실패 이후, 남은 모든 속성의 유효성 검증을 중지하도록 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리다이렉션

수동으로 validator 인스턴스를 만들면서도 HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 그대로 사용하고 싶다면, 기존 validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 만약 유효성 검증에 실패한다면, 사용자는 자동으로 되돌아가거나, XHR 요청의 경우에는 [JSON 응답이 반환](#validation-error-response-format)됩니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

검증 실패 시 에러 메시지를 [이름 있는 에러 백(naming error bag)](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름 있는 에러 백(Named Error Bags)

한 페이지에 여러 폼이 있을 때, 각 폼별로 검증 에러가 저장된 `MessageBag`을 네이밍하여 특정 폼의 에러 메시지를 분리해서 조회할 수 있습니다. 이를 위해 `withErrors`에 두 번째 인수로 이름을 전달하세요.

```php
return redirect('/register')->withErrors($validator, 'login');
```

이후 `$errors` 변수에서 원하는 이름의 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요하다면, validator 인스턴스가 라라벨에서 기본적으로 제공하는 에러 메시지 대신 커스텀 에러 메시지를 사용하도록 지정할 수 있습니다. 커스텀 메시지 지정 방법은 여러 가지가 있으며, 가장 간단하게는 `Validator::make` 메서드에 세 번째 인수로 메시지 배열을 넘기는 것입니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

위 예시에서 `:attribute` 플레이스홀더는 실제로 검증되는 필드명으로 대체됩니다. 유효성 검증 메시지에서 아래와 같이 다양한 플레이스홀더도 사용 가능합니다.

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대한 커스텀 에러 메시지 지정

특정 속성에만 맞춤 에러 메시지를 사용하고 싶을 때는 "점(dot) 표기법"을 사용할 수 있습니다. 속성명 뒤에 규칙명을 붙여서 메시지를 지정하세요.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 속성명(필드명) 커스터마이즈

라라벨의 기본 에러 메시지들에는 `:attribute` 플레이스홀더가 들어 있으므로, 필드명 표시를 원하는 값으로 바꿀 수 있습니다. 이를 위해서는 `Validator::make`의 네 번째 인수로 커스텀 속성명 배열을 넘깁니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행하기

필요하다면, 기본 유효성 검증이 끝난 후 추가적으로 더 검증을 수행할 수 있습니다. 검증기(validator) 인스턴스의 `after` 메서드를 사용하여 가능하며, 이 메서드에는 검증이 완료된 뒤 실행될 클로저나 호출 가능한 객체(callable)의 배열을 전달할 수 있습니다. 전달된 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 넘겨지므로, 필요시 추가적인 에러 메시지를 설정할 수 있습니다.

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

위에서 알 수 있듯, `after` 메서드는 콜러블의 배열도 받을 수 있습니다. "after validation" 로직이 각각의 호출 가능한 클래스로 분리되어 있다면 매우 편리합니다. 이 클래스들은 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받게 됩니다.

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
## 유효성 검증된 입력 데이터 다루기

폼 리퀘스트 또는 수동 생성 validator 인스턴스를 사용하여 요청 데이터를 검증한 후, 실제로 검증된 데이터만 추출해서 사용하고 싶을 때가 있습니다. 몇 가지 방법이 있습니다. 먼저, 폼 리퀘스트 또는 validator 인스턴스의 `validated` 메서드를 호출할 수 있으며, 이 메서드는 검증된 데이터 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는, 폼 리퀘스트 또는 validator 인스턴스의 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하여, `only`, `except`, `all` 메서드를 제공해 일부 혹은 전체 검증된 데이터에 손쉽게 접근할 수 있습니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

뿐만 아니라, `Illuminate\Support\ValidatedInput` 인스턴스는 반복(iterate)도 가능하며 배열처럼 접근할 수도 있습니다.

```php
// 검증된 데이터를 반복(iterate)할 수 있습니다...
foreach ($request->safe() as $key => $value) {
    // ...
}

// 배열처럼 접근할 수도 있습니다...
$validated = $request->safe();

$email = $validated['email'];
```

추가로, 검증된 데이터에 새로운 필드를 합쳐야 한다면 `merge` 메서드를 사용할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

[컬렉션](/docs/12.x/collections) 인스턴스로 변환하고 싶을 때는 `collect` 메서드를 사용하세요.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 에러 메시지 다루기

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 여러 가지 편리한 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 또한, 모든 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 특정 필드의 첫 번째 에러 메시지 가져오기

특정 필드에 대해 첫 번째 에러 메시지를 얻으려면 `first` 메서드를 사용하세요.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 특정 필드의 모든 에러 메시지 가져오기

특정 필드에 대한 모든 에러 메시지 배열이 필요하다면 `get` 메서드를 사용하세요.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 형식의 폼 필드를 검증할 때는 `*` 문자를 사용해 각 배열 요소에 대한 모든 에러 메시지도 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 에러 메시지 가져오기

모든 필드에 대한 모든 에러 메시지 배열이 필요하다면 `all` 메서드를 사용하세요.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 특정 필드에 에러 메시지가 있는지 확인하기

특정 필드에 에러 메시지가 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 커스텀 메시지 지정하기

라라벨이 제공하는 내장 유효성 검증 규칙 각각은 애플리케이션의 `lang/en/validation.php` 파일에 에러 메시지가 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

`lang/en/validation.php` 파일 내에서 각 유효성 검증 규칙에 해당하는 번역 항목을 찾을 수 있습니다. 애플리케이션의 요구에 맞게 메시지를 자유롭게 변경할 수 있습니다.

또한, 이 파일을 다른 언어 디렉터리로 복사해 각 언어별로 메시지를 번역할 수 있습니다. 라라벨의 로컬라이제이션(다국어) 지원에 대해 더 자세히 알고 싶다면 [로컬라이제이션 문서](/docs/12.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩(skeleton)에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨 언어 파일을 커스터마이징하려면, `lang:publish` Artisan 명령어를 통해 파일을 배포(publish)할 수 있습니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 커스텀 메시지

`lang/xx/validation.php` 언어 파일의 `custom` 배열에 원하는 속성 및 규칙 조합에 대한 커스텀 에러 메시지를 지정할 수 있습니다.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성명 지정

라라벨의 기본 에러 메시지 상당수에는 `:attribute` 플레이스홀더가 포함되어 있으며, 해당 필드 또는 속성 이름으로 대체됩니다. 이때 `:attribute` 부분을 커스텀 값으로 바꾸고 싶다면, `lang/xx/validation.php` 파일의 `attributes` 배열에 원하시는 한국어 이름을 지정하세요.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어를 사용하세요.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값(value) 이름 커스터마이즈

라라벨의 일부 내장 유효성 검증 규칙 에러 메시지에는 요청 속성의 현재 값이 `:value` 플레이스홀더로 표시됩니다. 하지만, 경우에 따라 에러 메시지에서 `:value` 부분에 좀 더 사용자 친화적인 표현을 쓸 수도 있습니다. 예를 들어, 아래와 같이 `payment_type`이 `cc`일 때 `credit_card_number`가 필수(required_if)인 규칙을 생각해봅시다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 규칙이 실패하면, 아래와 같은 에러 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

`cc` 값 대신, 좀 더 이해하기 쉬운 값을 보여주고 싶다면, 언어 파일(`lang/xx/validation.php`)의 `values` 배열에 다음과 같이 추가할 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면, `lang:publish` Artisan 명령어를 사용하세요.

이렇게 값을 지정하면, 아래와 같은 메시지가 에러로 출력됩니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 유효성 검증 규칙

아래는 사용 가능한 유효성 검증 규칙의 목록과 각각의 기능 설명입니다.

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

검증 대상 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이어야 합니다. 주로 "서비스 약관 동의"와 같은 필드의 유효성 검사에 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

검증 대상 필드는, 다른 특정 필드가 지정된 값일 때 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값이어야 합니다. 이 규칙도 "서비스 약관 동의"와 비슷한 케이스에 사용됩니다.

<a name="rule-active-url"></a>
#### active_url

검증 대상 필드는 `dns_get_record` PHP 함수의 기준에 따라 올바른 A 또는 AAAA 레코드를 가져야 합니다. URL의 호스트명은 PHP의 `parse_url` 함수를 통해 추출된 후, `dns_get_record`로 전달됩니다.

<a name="rule-after"></a>
#### after:_date_

검증 대상 필드는 지정된 날짜 이후의 값이어야 합니다. 날짜는 `strtotime` PHP 함수로 전달되어, 유효한 `DateTime` 인스턴스로 변환됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`에서 평가할 날짜 문자열 대신, 비교 대상이 될 다른 필드를 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

더 편리하게 날짜 기반의 규칙을 만들고 싶다면, 유창한(fluent) `date` 규칙 빌더를 사용할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

오늘 이후이거나, 오늘 또는 오늘 이후를 원하는 경우 각각 `afterToday`, `todayOrAfter` 메서드를 활용할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>

#### after_or_equal:_date_

검증하려는 필드는 지정된 날짜 이후이거나 같은 값이어야 합니다. 더 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

편의를 위해 날짜 기반의 규칙은 유창한 `date` 규칙 빌더를 사용해서 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검증 규칙을 사용하면, 해당 필드가 지정한 검증 규칙 집합 중 하나라도 만족하면 통과하도록 설정할 수 있습니다. 예를 들어 아래의 규칙은 `username` 필드가 이메일 주소이거나, 6자 이상이며 알파벳·숫자·대시를 포함할 수 있는 경우 통과합니다.

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

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함된 전체 유니코드 알파벳 문자로만 이루어져 있어야 합니다.

만약 ASCII 문자(`a-z`, `A-Z`)로만 제한하고 싶다면, `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 해당하는 유니코드 영숫자, 그리고 ASCII 대시(`-`), 언더스코어(`_`)만 포함해야 합니다.

ASCII 문자(`a-z`, `A-Z`, `0-9`)로만 제한하려면 `ascii` 옵션을 사용할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)의 전체 유니코드 영숫자 문자만 포함해야 합니다.

ASCII 문자(`a-z`, `A-Z`, `0-9`)로만 제한하려면 `ascii` 옵션을 사용할 수 있습니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

검증 대상 필드는 PHP의 `array`(배열) 타입이어야 합니다.

`array` 규칙에 추가 값이 제공된 경우, 입력 배열의 각 키는 규칙에 명시한 값 목록에 반드시 포함되어야 합니다. 아래 예시에서 입력 배열의 `admin` 키는 `array` 규칙에 지정한 목록 안에 없기 때문에 유효하지 않습니다.

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

일반적으로 허용할 배열 키를 명확히 지정하는 것이 바람직합니다.

<a name="rule-ascii"></a>
#### ascii

검증 대상 필드는 전부 7비트 ASCII 문자이어야 합니다.

<a name="rule-bail"></a>
#### bail

해당 필드에서 첫 번째 검증이 실패하면 해당 필드에 대한 나머지 검증을 중단합니다.

`bail` 규칙은 지정한 필드에 한해서 첫 실패 시 더 이상 검증하지 않지만, `stopOnFirstFailure` 메서드는 모든 필드의 한 번 실패가 발생하면 전체 검증을 중단합니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

검증 대상 필드는 지정한 날짜보다 이전이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 검증 중인 다른 필드명을 값으로 사용할 수 있습니다.

날짜 기반 규칙은 유창한 `date` 규칙 빌더를 사용하여 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`, `todayOrBefore` 메서드를 활용하면 날짜가 오늘 이전 또는 오늘과 이전임을 더 간결하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 대상 필드는 지정한 날짜와 같거나 이전이어야 합니다. 날짜는 PHP의 `strtotime` 함수로 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다. [after](#rule-after) 규칙과 같이, 검증 중인 다른 필드명을 값으로 지정할 수 있습니다.

날짜 기반 규칙은 유창한 `date` 규칙 빌더를 사용해서 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

검증 대상 필드는 _min_ 값과 _max_ 값(이상 이하 포함) 사이의 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

검증 대상 필드는 boolean으로 형변환될 수 있어야 합니다. 허용 가능한 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"` 입니다.

<a name="rule-confirmed"></a>
#### confirmed

검증 대상 필드와 짝을 이루는 `{field}_confirmation` 필드가 일치해야 합니다. 예를 들어, 검증 중인 필드가 `password`라면, 입력 값에 반드시 `password_confirmation` 필드가 존재해야 합니다.

커스텀 확인 필드명을 사용할 수도 있습니다. 예를 들어, `confirmed:repeat_username`을 지정하면, 해당 필드 값이 `repeat_username` 필드와 일치해야 합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

검증 대상 필드는 지정한 값들(_foo_, _bar_ 등)을 모두 포함하는 배열이어야 합니다. 배열을 `implode`하여 규칙을 만드는 일이 잦으므로, `Rule::contains` 메서드를 사용해 규칙을 좀 더 유창하게 작성할 수 있습니다.

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

검증 대상 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 인수로 [인증 가드](/docs/12.x/authentication)를 지정할 수도 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

검증 대상 필드는 PHP의 `strtotime` 함수로 판별 가능한 유효한(상대적이지 않은) 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 대상 필드는 지정한 날짜와 정확히 같아야 합니다. 날짜는 PHP의 `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 대상 필드는 지정한 _formats_ 중 하나와 반드시 일치해야 합니다. 한 필드 검증에 `date` 규칙과 `date_format` 규칙을 **동시에** 사용해서는 안 됩니다. 이 규칙은 PHP [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 포맷을 사용할 수 있습니다.

날짜 기반 규칙은 유창한 `date` 규칙 빌더를 이용해 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

검증 대상 필드는 숫자이며, 지정한 소수점 자릿수를 가져야 합니다:

```php
// 정확히 소수점 2자리(9.99)...
'price' => 'decimal:2'

// 소수점 2자리 이상 4자리 이하...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

다른 필드가 지정한 값과 같을 때, 검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나여야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 대상 필드는 _field_와 값이 달라야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 대상 정수는 자리수가 _value_와 정확히 일치해야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 대상 정수 자리수는 _min_에서 _max_ 사이여야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 대상 파일은 규칙에 명시한 이미지 크기 제약 조건을 충족해야 합니다:

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_.

_ratio_ 조건은 가로/세로 비율로 지정합니다. 분수(`3/2`)나 실수(`1.5`)로 입력할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

인자가 여러 개 필요한 규칙이므로, `Rule::dimensions` 메서드로 더 편리하게 규칙을 작성할 수 있습니다.

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

배열 검증 시, 해당 필드 안에 중복되는 값이 없어야 합니다.

```php
'foo.*.id' => 'distinct'
```

`distinct`는 기본적으로 느슨한 변수 비교를 사용합니다. 엄격한 비교를 원한다면, 규칙 정의에 `strict` 파라미터를 추가하세요.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 구분 없이 비교하고 싶다면, `ignore_case` 인자를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### email

검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 규칙은 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용해 이메일 주소를 검증합니다. 기본적으로 `RFCValidation` 검증기가 적용되며, 다양한 검증 스타일도 사용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예시는 `RFCValidation`과 `DNSCheckValidation` 검증을 모두 적용합니다. 적용 가능한 모든 검증 스타일은 다음과 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일을 검증합니다.
- `strict`: `NoRFCWarningsValidation` - RFC에 맞게 이메일을 검증하되, 경고(예: 마지막에 붙는 점, 연속된 점 등)가 있으면 실패 처리합니다.
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 동형 문자나 혼동을 유발하는 유니코드 문자가 포함되어 있지 않은지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일이 유효한지 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수로, 일부 유니코드 문자가 허용된 이메일을 검증합니다.

</div>

편의를 위해 유창한 규칙 빌더로 이메일 유효성 검증 규칙을 작성할 수 있습니다.

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
> `dns` 및 `spoof` 검증기를 사용하려면 PHP의 `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

검증 대상 필드는 지정한 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은, 검증 대상 값이 지정한 열거형(enum) 값 중 하나에 해당되는지를 확인하는 클래스 기반 규칙입니다. `Enum` 규칙의 생성자에는 enum 이름을 인자로 넘깁니다. 원시값(primitive value)을 검증할 때는, 열거형 뒷받침값(Backed Enum)을 전달해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only`와 `except` 메서드를 이용해, 유효하게 받아들일 enum 케이스를 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용해 `Enum` 규칙을 조건에 따라 동적으로 수정할 수도 있습니다.

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

검증 대상 필드는 `validate`와 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

검증 대상 필드는 _anotherfield_가 _value_와 같을 때 `validate` 및 `validated` 메서드에서 반환하는 요청 데이터에서 제외됩니다.

복잡한 조건의 제외 로직이 필요하다면, `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 받아, `true`를 반환하면 해당 필드를 제외합니다.

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

검증 대상 필드는 _anotherfield_가 _value_와 **같지 않은 경우** `validate`, `validated` 메서드의 반환 데이터에서 제외됩니다. _value_가 `null`일 경우(`exclude_unless:name,null`), 비교하는 필드가 `null`이거나 요청 데이터에 존재하지 않을 때만 해당 필드가 제외되지 않습니다.

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

검증 대상 필드는 _anotherfield_ 필드가 존재할 때 `validate`, `validated` 메서드의 반환 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

검증 대상 필드는 _anotherfield_ 필드가 존재하지 않을 때 `validate`, `validated` 메서드의 반환 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

검증 대상 필드는 지정한 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 지정하지 않으면, 필드명이 컬럼명으로 사용됩니다. 즉, 이 예시에서는 `states` 테이블의 `state` 컬럼에 요청 받은 `state` 값이 존재하는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
#### 데이터베이스 컬럼명 명시하기

규칙에서 테이블명 다음에 컬럼명을 지정할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

특정 데이터베이스 커넥션을 통해 `exists` 쿼리를 실행하려면, 테이블 앞에 커넥션명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 명시하는 대신, Eloquent 모델명을 지정할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

유효성 검증 규칙으로 더 복잡한 쿼리를 작성하고 싶다면, `Rule` 클래스를 사용해 규칙을 유창하게 정의할 수 있습니다. 아래 예시에서는 규칙들을 배열로 전달하여, `|` 문자 없이도 여러 규칙을 설정할 수 있습니다.

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

`Rule::exists` 메서드의 두 번째 인자로 컬럼명을 넘겨주면, 생성된 `exists` 규칙에서 사용할 데이터를 명확히 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

데이터베이스에 여러 값이 존재하는지 배열로 한 번에 확인하고 싶다면, 해당 필드에 `exists`와 [array](#rule-array) 규칙을 모두 추가합니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이렇게 하면, 라라벨은 모든 값을 한 번의 쿼리로 검사합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

검증 대상 파일의 확장자가 지정한 확장자 목록 중 하나여야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일 확장자만으로 파일 검증을 신뢰하지 마세요. 이 규칙은 반드시 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 함께 사용해야 합니다.

<a name="rule-file"></a>
#### file

검증 대상 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

해당 필드가 존재한다면 비어 있지 않아야 합니다.

<a name="rule-gt"></a>
#### gt:_field_

검증 대상 필드는 지정한 _field_ 또는 _value_보다 커야 합니다. 두 필드는 타입이 같아야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

검증 대상 필드는 지정한 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 타입이 같아야 하며, 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

검증 대상 필드는 [16진수 색상](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 값이어야 합니다.

<a name="rule-image"></a>
#### image

검증 대상 파일은 이미지 파일(jpg, jpeg, png, bmp, gif, webp)이어야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 취약성 위험 때문에 SVG 파일을 허용하지 않습니다. SVG 파일 허용이 필요하다면 `image:allow_svg` 옵션을 사용할 수 있습니다.

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

검증 대상 필드는 지정한 값 목록 안에 포함되어야 합니다. 배열을 `implode`하는 과정이 자주 발생하므로, `Rule::in` 메서드를 사용하여 규칙을 유창하게 만들 수 있습니다.

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

`in` 규칙이 `array` 규칙과 함께 사용되면, 입력 배열의 각 값이 반드시 규칙에서 지정한 값 목록에 모두 들어 있어야 합니다. 아래 예시에서 입력 배열의 `LAS` 공항 코드는 규칙에서 허용한 공항 목록에 포함되어 있지 않아 유효하지 않습니다.

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

검증 대상 필드는 _anotherfield_에 지정된 값들 중 하나와 일치해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 대상 필드는 배열이어야 하고, 해당 배열의 키 중에 지정된 _values_ 중 하나라도 포함해야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

검증 대상 필드는 정수여야 합니다.

> [!WARNING]
> 이 유효성 검증 규칙은 입력값이 실제로 "정수" 타입인지까지 확인하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 타입이어야만 합니다. 입력값이 진짜 숫자인지 확인하고 싶다면 [numeric 유효성 검증 규칙](#rule-numeric)과 이 규칙을 함께 사용하시기 바랍니다.

<a name="rule-ip"></a>
#### ip

검증 대상 필드는 IP 주소이어야 합니다.

<a name="ipv4"></a>
#### ipv4

검증 대상 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

검증 대상 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

검증 대상 필드는 올바른 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

검증 대상 필드는 지정된 _field_ 보다 작아야 합니다. 두 필드는 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

검증 대상 필드는 지정된 _field_ 이하의 값을 가져야 합니다. 두 필드는 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lowercase"></a>
#### lowercase

검증 대상 필드는 반드시 소문자여야 합니다.

<a name="rule-list"></a>
#### list

검증 대상 필드는 배열이면서, 리스트 형태여야 합니다. 배열의 키가 0부터 `count($array) - 1`까지 연속되는 숫자일 때 리스트로 간주됩니다.

<a name="rule-mac"></a>
#### mac_address

검증 대상 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

검증 대상 필드는 _value_ 이하의 값만 허용됩니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 대상 정수 값의 자릿수는 최대 _value_까지 허용됩니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

검증 대상 파일은 지정된 MIME 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

업로드된 파일의 MIME 타입을 판별하는 과정에서는 파일 내용을 읽어 실제 MIME 타입을 추정하므로, 클라이언트가 제공한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 대상 파일은 지정한 확장자에 해당하는 MIME 타입이어야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하면 되지만, 이 규칙은 실제로는 파일 내용을 읽어서 MIME 타입을 판별해 검증합니다. 전체 MIME 타입과 해당 확장자 목록은 아래 페이지에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 검증 규칙은 파일의 MIME 타입과 사용자가 지정한 확장자가 일치하는지까지는 확인하지 않습니다. 예를 들어, `mimes:png` 규칙이라면, 파일 내용이 실제 PNG 형식이면 파일 이름이 `photo.txt`여도 유효한 PNG 이미지로 판단합니다. 파일명이 가진 확장자까지 점검하려면 [extensions](#rule-extensions) 규칙을 활용할 수 있습니다.

<a name="rule-min"></a>
#### min:_value_

검증 대상 필드는 _value_ 이상의 값을 가져야 합니다. 문자열, 숫자, 배열, 파일 모두 [size](#rule-size) 규칙과 동일하게 처리됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 대상 정수 값의 자릿수는 최소 _value_ 이상이어야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

검증 대상 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 _value_와 같으면, 검증 대상 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_또 다른 필드_(_anotherfield_)가 _value_와 같은 값이 아닐 경우, 검증 대상 필드는 입력 데이터에 존재하면 안 됩니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

명시된 다른 필드들 중 하나라도 존재한다면(입력 값이 있다면), 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

명시된 모든 필드가 존재하는 경우에만, 검증 대상 필드는 존재해서는 안 됩니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

검증 대상 필드는 주어진 값 목록에 포함되어서는 안 됩니다. `Rule::notIn` 메서드를 활용하면 좀 더 유연하게 규칙을 작성할 수 있습니다.

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

검증 대상 필드는 지정된 정규식과 일치하지 않아야 합니다.

내부적으로 이 규칙은 PHP의 `preg_match` 함수를 사용합니다. 정규식 규칙에 사용할 패턴에는 유효한 구분자(Delimiter)를 반드시 포함시켜야 합니다. 예를 들어: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` 또는 `not_regex` 패턴에서 정규식에 `|` 기호가 들어간 경우, validation 규칙들을 배열로 지정해야 합니다. `|` 문자를 구분자 대신 사용하면 정규식이 정상 동작하지 않을 수 있습니다.

<a name="rule-nullable"></a>
#### nullable

검증 대상 필드는 `null`이어도 유효합니다.

<a name="rule-numeric"></a>
#### numeric

검증 대상 필드는 [숫자형(numeric)](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<a name="rule-present"></a>
#### present

검증 대상 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 _value_ 중 하나와 같다면, 검증 대상 필드가 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_또 다른 필드_(_anotherfield_)가 _value_와 같지 않을 경우, 검증 대상 필드는 반드시 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

다른 명시된 필드 중 단 하나라도 입력 데이터에 존재한다면, 검증 대상 필드도 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

모든 명시된 필드가 입력 데이터에 존재한다면, 검증 대상 필드도 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

검증 대상 필드는 입력 데이터에 존재하지 않거나 '비어 있어야' 합니다. 여기서 '비어 있다'는 상태는 다음 중 하나에 해당하면 '비어 있음'으로 간주합니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만 경로가 비어 있는 경우

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 _value_와 같을 때, 검증 대상 필드는 입력 데이터에 없어야 하거나 비어 있어야 합니다. '비어 있음'의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만 경로가 비어 있는 경우

</div>

더 복잡한 조건부 필드 금지 로직이 필요할 경우, `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 인자로 받을 수 있으며, 클로저로 전달하면 반환값에 따라 검증 대상 필드가 금지될지(true) 여부를 결정합니다.

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

_또 다른 필드_(_anotherfield_)가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값일 경우, 검증 대상 필드는 없어야 하거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_또 다른 필드_(_anotherfield_)가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 값 중 하나와 같을 경우, 검증 대상 필드는 없어야 하거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 _value_와 같지 않을 경우, 검증 대상 필드는 없어야 하거나 비어 있어야 합니다. '비어 있음'은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만 경로가 비어 있는 경우

</div>

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

검증 대상 필드가 비어 있지 않은 경우, _anotherfield_로 지정된 모든 필드는 없어야 하거나 비어 있어야 합니다. 여기에서 '비어 있음'의 기준은 다음과 같습니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 값이 업로드된 파일이지만 경로가 비어 있는 경우

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

검증 대상 필드는 지정된 정규식 패턴과 일치해야 합니다.

이 규칙은 내부적으로 PHP의 `preg_match`을 사용하며, 지정된 패턴은 유효한 구분자를 반드시 포함해야 합니다. 예시: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴에서 정규식 안에 `|` 문자가 포함될 경우, 규칙을 파이프(`|`)로 구분하지 말고 배열로 지정하는 것이 필요할 수 있습니다.

<a name="rule-required"></a>
#### required

검증 대상 필드는 입력 데이터에 반드시 존재해야 하며, 비어있지 않아야 합니다. '비어 있음'은 다음 조건을 만족할 때 해당됩니다.

<div class="content-list" markdown="1">

- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열 또는 비어 있는 `Countable` 객체인 경우
- 값이 없는 업로드 파일의 경우

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 _value_ 중 하나와 같을 때, 검증 대상 필드는 반드시 존재해야 하고 비어있지 않아야 합니다.

더 복잡한 조건을 만들고 싶다면 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 인자로 받아 반환 값에 따라서 필수 여부를 결정할 수 있습니다.

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

_또 다른 필드_(_anotherfield_)가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값일 때, 검증 대상 필드가 존재하며 비어 있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_또 다른 필드_(_anotherfield_)가 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 값 중 하나일 때, 검증 대상 필드가 반드시 존재해야 하며 비어있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_또 다른 필드_(_anotherfield_)가 _value_와 같지 않을 경우, 검증 대상 필드는 반드시 존재해야 하고 비어 있으면 안 됩니다. 또한 _anotherfield_는 _value_가 `null`이 아니라면 요청 데이터에 반드시 존재해야 합니다. 만약 _value_가 `null`(`required_unless:name,null`)이고 참조 필드가 `null`이거나 데이터에 존재하지 않으면 검증 대상 필드가 필수가 아닙니다.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

다른 명시된 필드들 중 하나라도 존재하고 비어 있지 않으면, 검증 대상 필드도 반드시 존재해야 하며 비어 있어서는 안 됩니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

명시된 모든 필드가 존재하고 비어 있지 않은 경우에만, 검증 대상 필드는 필수이며 비어 있으면 안 됩니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

명시된 다른 필드들 중 하나라도 비어 있거나 존재하지 않는 경우, 검증 대상 필드는 필수이고 반드시 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

명시된 다른 모든 필드가 비어 있거나 존재하지 않을 때에만, 검증 대상 필드는 필수이며 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

검증 대상 필드는 배열이고, 지정한 키들 중 최소한 한 개는 반드시 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

지정한 _field_의 값과 검증 대상 필드 값이 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

검증 대상 필드는 지정된 _value_와 정확히 일치하는 크기를 가져야 합니다. 문자열의 경우, _value_는 문자 수를 의미합니다. 숫자의 경우 _value_는 정수 값을 의미하며, 반드시 `numeric` 또는 `integer` 규칙이 함께 필요합니다. 배열은 요소 개수, 파일은 킬로바이트 단위 크기입니다. 예시를 살펴봅시다.

```php
// 문자열 길이가 정확히 12글자인지 검증
'title' => 'size:12';

// 입력값이 10과 일치하는 정수인지 검증
'seats' => 'integer|size:10';

// 배열의 요소가 정확히 5개인지 검증
'tags' => 'array|size:5';

// 업로드된 파일의 크기가 정확히 512킬로바이트인지 검증
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 대상 필드는 지정된 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 대상 필드는 문자열이어야 합니다. 만약 필드가 `null` 값도 허용하려면, `nullable` 규칙을 함께 지정해야 합니다.

<a name="rule-timezone"></a>
#### timezone

검증 대상 필드는 `DateTimeZone::listIdentifiers` 메서드로 정의된 유효한 타임존 식별자여야 합니다.

[DateTimeZone::listIdentifiers 메서드](https://www.php.net/manual/en/datetimezone.listidentifiers.php)가 허용하는 인수 역시 이 유효성 검증 규칙에 전달할 수 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

검증 대상 필드는 지정된 데이터베이스 테이블에 이미 존재해서는 안 됩니다.

**커스텀 테이블/컬럼명 지정:**

테이블명을 직접 명시하는 대신, Eloquent 모델을 지정하면 해당 모델의 테이블명을 자동으로 사용합니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션을 사용하여 데이터베이스의 컬럼명을 직접 지정할 수 있습니다. `column`이 지정되지 않으면, 검증 대상 필드의 이름이 컬럼명으로 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**커스텀 데이터베이스 커넥션 지정:**

Validator가 실행하는 데이터베이스 쿼리에 커스텀 커넥션을 사용해야 할 때는, 테이블명 앞에 커넥션명을 붙이면 됩니다.

```php
'email' => 'unique:connection.users,email_address'
```

**특정 ID는 무시하도록 Unique 규칙 적용:**

사용자가 이미 해당 이메일을 소유하고 있다면, 예를 들어 "프로필 수정" 화면에서 이름만 변경했을 때 이메일의 중복 오류가 발생하지 않도록 해당 사용자의 ID는 unique 체크에서 무시해야 할 수 있습니다.

Validator에서 특정 사용자의 ID를 무시하도록 하려면, `Rule` 클래스를 사용해 규칙을 유연하게 작성해야 하며, 이때 규칙을 배열로 작성합니다.

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
> 사용자로부터 전달받은 입력값은 절대로 `ignore` 메서드에 전달하면 안 됩니다. 오직 시스템에서 생성된 고유 ID(예: auto-increment ID, Eloquent 모델의 UUID 등)만 전달해야 하며, 그렇지 않을 경우 SQL 인젝션 공격에 취약해질 수 있습니다.

모델 키 값 대신 전체 모델 인스턴스를 `ignore`에 전달할 수도 있습니다. 라라벨이 자동으로 키 값을 추출해줍니다:

```php
Rule::unique('users')->ignore($user)
```

테이블의 기본키 컬럼명이 `id`가 아닌 경우, 두 번째 인자로 컬럼명을 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 검증 대상 속성 이름과 같은 컬럼의 유일성을 검사합니다. 두 번째 인자로 다른 컬럼명을 지정할 수도 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 WHERE 조건 지정하기:**

쿼리를 더 세분화하고 싶으면 `where` 메서드를 활용해 추가 조건을 지정할 수 있습니다. 예를 들어, `account_id`가 1인 레코드로만 한정해 검색할 수 있습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Unique 검사에서 Soft Delete 제외하기:**

기본적으로 unique 규칙은 soft deleted(소프트 삭제된) 레코드까지 포함해 유일성을 검사합니다. soft deleted 데이터를 검사 대상에서 빼고 싶다면 `withoutTrashed` 메서드를 호출하면 됩니다.

```php
Rule::unique('users')->withoutTrashed();
```

소프트 삭제 컬럼명이 `deleted_at`이 아니라면, 컬럼명을 인자로 전달할 수 있습니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

검증 대상 필드는 반드시 대문자여야 합니다.

<a name="rule-url"></a>
#### url

검증 대상 필드는 올바른 URL이어야 합니다.

검증 시에 허용할 URL 프로토콜을 직접 지정하고 싶다면, 해당 프로토콜을 규칙의 파라미터로 전달하면 됩니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

검증 대상 필드는 [ULID(Universally Unique Lexicographically Sortable Identifier)](https://github.com/ulid/spec)여야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 대상 필드는 RFC 9562(버전 1, 3, 4, 5, 6, 7, 8)의 유효한 UUID여야 합니다.

특정 버전의 UUID만 허용하고 싶으면 아래와 같이 지정할 수 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부로 규칙 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값일 때 유효성 검증 건너뛰기

다른 필드가 특정 값을 가진 경우, 해당 필드는 유효성 검증을 하지 않도록 하고 싶을 때가 있습니다. 이럴 땐 `exclude_if` 유효성 검증 규칙을 사용할 수 있습니다. 아래 예시에서는 `has_appointment` 필드 값이 `false`일 경우, `appointment_date`와 `doctor_name` 필드는 검증하지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

반대로, 특정 필드의 값이 지정된 값이 아니면 검증을 건너뛰려면 `exclude_unless` 규칙을 사용합니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>

#### 값이 존재할 때만 유효성 검사하기

특정 상황에서는, 어떤 필드가 **존재할 때에만** 해당 필드에 대한 유효성 검사를 수행하고 싶을 수 있습니다. 이를 간단하게 처리하려면, 규칙 목록에 `sometimes` 규칙을 추가하면 됩니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예시에서 `email` 필드는 `$data` 배열에 값이 있을 때에만 유효성 검사가 실행됩니다.

> [!NOTE]
> 값이 항상 존재해야 하지만 비어있을 수도 있는 필드를 검증하려면 [옵션 필드에 대한 참고 사항](#a-note-on-optional-fields)을 확인하시기 바랍니다.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검사

때로는 좀 더 복잡한 조건에 따라 유효성 검사 규칙을 추가하고 싶을 수 있습니다. 예를 들어, 어떤 필드는 다른 필드의 값이 100보다 클 때에만 필수로 만들고 싶을 수 있습니다. 또는 특정 필드가 존재할 때 두 개의 필드가 각각 지정된 값을 가져야 할 때도 있습니다. 이러한 유효성 검사 규칙을 추가하는 일은 생각만큼 어렵지 않습니다.

우선, _항상 고정되는_ 기본 규칙들을 이용해 `Validator` 인스턴스를 생성합니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

예시로, 우리 웹 애플리케이션이 게임 수집가를 위한 것이라고 가정해 봅시다. 게임 수집가가 회원가입할 때 소유한 게임 개수가 100개가 넘어간다면, 왜 그렇게 많은 게임을 가지고 있는지 설명하도록 하고 싶습니다. 예를 들어 중고 게임 상점을 운영하거나, 단순히 게임 수집을 즐기는 경우가 있을 것입니다. 이와 같은 조건부 필수 입력을 구현하려면, `Validator` 인스턴스의 `sometimes` 메서드를 사용하면 됩니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드의 첫 번째 인자는 조건부로 유효성 검사를 적용할 필드명입니다. 두 번째 인자는 추가할 규칙들의 목록이고, 세 번째 인자인 클로저가 `true`를 반환하면 해당 규칙이 적용됩니다. 이 방식으로 복잡한 조건부 유효성 검사도 수월하게 구축할 수 있습니다. 여러 필드에 조건부 유효성 검사를 동시에 적용하는 것도 가능합니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent`의 인스턴스이며, 검증 대상의 입력 값 및 파일에 접근할 때 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 배열 요소에 대한 복잡한 조건부 유효성 검사

때때로 같은 중첩 배열 내의 다른 필드를 기준으로 조건에 따라 유효성 검사 규칙을 적용하고 싶을 때가 있습니다. 이때, 클로저의 두 번째 인자로 현재 검증 중인 배열의 개별 항목(배열 요소)을 받을 수 있습니다:

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

여기서 클로저에 전달되는 `$item` 파라미터는 속성 데이터가 배열인 경우에는 `Illuminate\Support\Fluent`의 인스턴스이고, 그렇지 않으면 문자열이 됩니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[배열 유효성 검사 규칙 문서](#rule-array)에서 설명한 것처럼, `array` 규칙은 허용할 배열 키들의 목록을 인수로 받을 수 있습니다. 배열에 추가적인 키가 존재한다면 유효성 검사에 실패하게 됩니다.

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

일반적으로, 배열 내에 허용할 키 이름을 명시적으로 지정하는 것이 항상 좋습니다. 그렇지 않으면, 검증기의 `validate` 및 `validated` 메서드는 모든 배열 및 그 모든 키를, 다른 중첩 배열 규칙에 의해 검증되지 않은 키까지도 검증된 데이터로 반환하게 됩니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력값 유효성 검사

배열로 된 폼 입력의 중첩 항목도 어렵지 않게 유효성 검사할 수 있습니다. "점(.) 표기법"을 사용해 배열 내부 속성을 검사하면 됩니다. 예를 들어, HTTP 요청에 `photos[profile]` 입력값이 포함되어 있다면 다음과 같이 검증할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소를 개별적으로 검증하는 것도 가능합니다. 예를 들어, 배열 필드 내 각 이메일이 고유한지 확인하려면 아래와 같이 처리할 수 있습니다.

```php
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

또한, [커스텀 유효성 메시지](#custom-messages-for-specific-attributes) 지정 시에도 `*` 문자를 사용할 수 있어서, 배열 기반 필드에 대해 하나의 일반적인 메시지를 사용할 수 있습니다.

```php
'custom' => [
    'person.*.email' => [
        'unique' => 'Each person must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터에 접근하기

특정 중첩 배열 요소의 값을 기준으로 규칙을 지정하고 싶을 때가 있습니다. 이럴 때는 `Rule::forEach` 메서드를 이용하면 됩니다. `forEach` 메서드는 배열 속성의 각 항목을 대상으로 클로저를 실행하며, 배열 요소의 값과 완전히 확장된 속성명을 전달받습니다. 클로저는 해당 배열 요소에 적용될 규칙 배열을 반환해야 합니다.

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
### 오류 메시지에서 인덱스 및 위치 표시

배열을 검증할 때, 특정 배열 항목에서 유효성 검사가 실패했을 경우 오류 메시지에서 해당 항목의 인덱스나 위치를 참조하고 싶을 수 있습니다. 이럴 때는 [커스텀 유효성 메시지](#manual-customizing-the-error-messages)에서 `:index`(0부터 시작), `:position`(1부터 시작) 플레이스홀더를 사용할 수 있습니다.

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

위 예시에서 유효성 검사가 실패하면 사용자에게 _"Please describe photo #2."_와 같은 오류 메시지가 보여집니다.

필요에 따라 더 깊이 중첩된 인덱스와 위치도 `second-index`, `second-position`, `third-index`, `third-position` 등과 같이 참조할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 유효성 검사

라라벨은 `mimes`, `image`, `min`, `max` 등 여러 파일 업로드에 사용할 수 있는 유효성 검사 규칙을 제공합니다. 파일 검증 시 이 규칙들을 개별적으로 지정해도 되지만, 라라벨에서는 보다 편리하게 사용할 수 있는 유연한 파일 유효성 규칙 빌더도 제공합니다.

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
#### 파일 유형 검사

`types` 메서드에 확장자만 지정해도 되지만, 실제로는 해당 파일의 내용을 읽어 MIME 타입을 추측하고 해당 MIME 타입에 대해 검사합니다. MIME 타입 및 그에 대응하는 확장자의 전체 목록은 아래에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 검사

사용자 편의를 위해, 최소 및 최대 파일 크기는 단위 접미사를 붙인 문자열로도 지정할 수 있습니다. 지원하는 단위는 `kb`, `mb`, `gb`, `tb`입니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 검사

사용자가 이미지를 업로드하는 경우, `File` 규칙의 `image` 생성자 메서드를 이용해 파일이 이미지(jpg, jpeg, png, bmp, gif 또는 webp)인지 쉽게 검증할 수 있습니다.

또한, `dimensions` 규칙으로 이미지의 크기를 제한할 수도 있습니다.

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
> 이미지 크기 검증에 대한 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하시기 바랍니다.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약점 우려로 SVG 파일을 허용하지 않습니다. SVG 파일도 허용해야 한다면, `image` 규칙에 `allowSvg: true`를 전달할 수 있습니다: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기(사이즈) 검사

이미지의 크기도 검증할 수 있습니다. 예를 들어, 업로드된 이미지가 너비 1000픽셀, 높이 500픽셀 이상이어야 한다면 다음과 같이 `dimensions` 규칙을 사용할 수 있습니다.

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
> 이미지 크기 검증에 대한 자세한 내용은 [dimensions 규칙 문서](#rule-dimensions)를 참고하시기 바랍니다.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검사

비밀번호가 충분히 복잡한지 확인하려면 라라벨의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체를 사용하면, 비밀번호 최소 글자 수, 영문 포함, 숫자 포함, 대소문자 혼합, 특수문자 포함 등 비밀번호 복잡도 규칙을 손쉽게 맞춤 설정할 수 있습니다.

```php
// 최소 8자 이상...
Password::min(8)

// 영문자 1개 이상 포함...
Password::min(8)->letters()

// 대소문자 각각 1개 이상 포함...
Password::min(8)->mixedCase()

// 숫자 1개 이상 포함...
Password::min(8)->numbers()

// 특수문자 1개 이상 포함...
Password::min(8)->symbols()
```

또한 `uncompromised` 메서드를 사용하면 공개된 비밀번호 유출(데이터 누출) 목록에 해당 비밀번호가 포함되어 있지 않은지 검사할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 방식과 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 이용하여, 사용자의 개인정보를 침해하지 않고 비밀번호 유출 여부를 판단합니다.

기본적으로, 데이터 유출 목록에 1번이라도 등장하면 해당 비밀번호는 취약하다고 판단됩니다. 이 기준치는 `uncompromised` 메서드의 첫 번째 인자로 변경할 수 있습니다.

```php
// 동일한 데이터 유출 내에서 비밀번호가 3번 미만 등장할 때만 허용...
Password::min(8)->uncompromised(3);
```

물론, 위의 모든 메서드는 체이닝하여 사용할 수 있습니다.

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

애플리케이션 전체에서 공통적으로 사용할 비밀번호 유효성 규칙을 한 곳에 지정해두면 편리합니다. 이를 위해 `Password::defaults` 메서드를 사용하면 됩니다. 이 메서드는 클로저를 인수로 받으며, 클로저는 기본 비밀번호 규칙 구성이 포함된 값을 반환합니다. 보통 `defaults` 규칙은 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

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

이후, 특정 비밀번호에 대해 기본 비밀번호 규칙을 적용하려면 인수 없이 `defaults` 메서드를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

가끔 기본 비밀번호 규칙에 추가적인 유효성 규칙을 더 붙이고 싶을 수 있습니다. 이때는 `rules` 메서드를 사용하면 됩니다.

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
### 규칙 객체 사용하기

라라벨에서는 다양한 기본 유효성 검사 규칙을 제공하고 있지만, 직접 커스텀 규칙을 정의해야 할 때도 있습니다. 이를 위한 한 가지 방법은 규칙 객체(Rule Object)를 사용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용할 수 있습니다. 예를 들어, 문자열이 대문자인지 검사하는 규칙을 만들고자 한다면 아래와 같이 Artisan 명령어를 실행하세요. 라라벨은 새 규칙을 `app/Rules` 디렉토리에 생성합니다. 만약 해당 디렉토리가 없다면, 규칙을 만들 때 자동으로 생성됩니다.

```shell
php artisan make:rule Uppercase
```

규칙 파일이 생성되었다면, 규칙의 동작을 정의할 수 있습니다. 규칙 객체에는 `validate`라는 단 하나의 메서드가 있으며, 이 메서드는 속성명, 값, 그리고 유효성 검사 실패 시 호출할 에러 메시지 콜백을 전달받습니다.

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

규칙 객체가 완성되면, 다른 유효성 검사 규칙들과 함께 해당 객체의 인스턴스를 검증기에 넘겨 사용할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 검사 메시지 번역

`$fail` 클로저에 직접 에러 메시지를 전달하는 대신, [번역 문자열 키](/docs/12.x/localization)를 사용해 라라벨이 에러 메시지를 번역하도록 할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요에 따라, `translate` 메서드의 첫 번째, 두 번째 인자로 자리 표시자 치환 값들과 사용 언어를 지정할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근하기

커스텀 규칙 클래스에서 현재 검증 중인 모든 데이터를 사용하고 싶은 경우, `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스에는 `setData` 메서드를 정의해야 하며, 해당 메서드는(유효성 검사 시작 전) 라라벨에 의해 검증 데이터 전체를 자동으로 전달받게 됩니다.

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

또는, 유효성 검사를 수행하는 validator 인스턴스에 접근해야 할 경우에는 `ValidatorAwareRule` 인터페이스를 구현하면 됩니다.

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
### 클로저(익명 함수)로 규칙 정의하기

애플리케이션 전체에서 딱 한 번만 사용할 간단한 커스텀 유효성 검사가 필요하다면, 규칙 객체 대신 클로저를 사용할 수 있습니다. 클로저는 속성명, 속성값, 그리고 검증 실패시 실행할 `$fail` 콜백을 전달받습니다.

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

기본적으로, 유효성 검사 대상 속성이 존재하지 않거나 빈 문자열일 경우, 커스텀 규칙을 포함한 일반적인 규칙들은 실행되지 않습니다. 예를 들어 [unique](#rule-unique) 규칙은 빈 문자열에 대해서는 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있어도 커스텀 규칙이 반드시 실행되게 하려면, 해당 규칙이 필수(required)임을 암시해야 합니다. 새로운 암묵적(implicit) 규칙 객체를 빠르게 생성하려면, `make:rule` Artisan 명령어에 `--implicit` 옵션을 추가하세요.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙은 해당 속성이 필수임을 _암시_할 뿐입니다. 실제로 속성이 없거나 비어 있을 때 에러가 발생할지는 구현에 따라 다릅니다.