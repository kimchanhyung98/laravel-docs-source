# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력 (Input)](#input)
    - [입력 데이터 가져오기](#retrieving-input)
    - [입력 존재 여부 확인](#input-presence)
    - [추가 입력 병합하기](#merging-additional-input)
    - [기존 입력값 (Old Input)](#old-input)
    - [쿠키](#cookies)
    - [입력 자르기 및 정규화](#input-trimming-and-normalization)
- [파일 (Files)](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정하기](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청과 상호작용할 수 있는 객체 지향적 방식을 제공하며, 요청과 함께 제출된 입력, 쿠키, 파일을 가져오는 기능을 지원합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청에 접근하기 (Accessing the Request)

현재 HTTP 요청 인스턴스를 의존성 주입으로 받으려면, 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입 힌트하면 됩니다. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 요청 인스턴스를 주입합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 사용자를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 사용자 저장 처리...

        return redirect('/users');
    }
}
```

앞서 언급했듯이, 라우트 클로저에도 `Illuminate\Http\Request` 클래스를 타입 힌트할 수 있습니다. 서비스 컨테이너가 클로저 실행 시 자동으로 현재 요청을 주입합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 매개변수 (Dependency Injection and Route Parameters)

컨트롤러 메서드에서 라우트 매개변수를 함께 받고자 할 때는, 라우트 매개변수를 의존성 뒤에 나열해야 합니다. 예를 들어, 라우트가 다음과 같이 정의되어 있을 때:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드는 `Illuminate\Http\Request`와 `id` 매개변수를 다음과 같이 받을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 사용자를 업데이트합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트 처리...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드 (Request Path, Host, and Method)

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사할 수 있는 다양한 메서드를 제공합니다. 이 클래스는 `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 중요한 몇 가지 메서드를 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기 (Retrieving the Request Path)

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 요청이 `http://example.com/foo/bar`로 들어왔다면 `path` 메서드는 `foo/bar`를 반환합니다:

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로 / 라우트 검사하기 (Inspecting the Request Path / Route)

`is` 메서드는 들어오는 요청 경로가 주어진 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다:

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면 들어오는 요청이 특정 [이름 있는 라우트](/docs/12.x/routing#named-routes)와 일치하는지 확인할 수 있습니다:

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기 (Retrieving the Request URL)

전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용합니다. `url`은 쿼리 스트링을 제외한 URL을 반환하며, `fullUrl`은 쿼리 스트링을 포함합니다:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 스트링 데이터를 추가하고 싶으면 `fullUrlWithQuery` 메서드를 사용하세요. 이 메서드는 현재 쿼리 스트링과 배열로 전달된 쿼리 문자열 변수를 병합합니다:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 문자열 파라미터를 제외한 현재 URL을 가져오려면 `fullUrlWithoutQuery` 메서드를 사용하세요:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기 (Retrieving the Request Host)

요청의 호스트는 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 확인할 수 있습니다:

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기 (Retrieving the Request Method)

`method` 메서드는 요청에 사용된 HTTP 동사를 반환합니다. 특정 HTTP 동사인지 확인하려면 `isMethod` 메서드를 사용할 수 있습니다:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더 (Request Headers)

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용해 요청 헤더 값을 가져올 수 있습니다. 헤더가 없으면 `null`을 반환하지만, 두 번째 인자로 기본값을 지정할 수 있습니다:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 지정한 헤더가 요청에 포함되어 있는지를 확인합니다:

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해 `bearerToken` 메서드를 사용해 `Authorization` 헤더에서 Bearer 토큰을 얻을 수 있습니다. 만약 해당 헤더가 없다면 빈 문자열을 반환합니다:

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소 (Request IP Address)

`ip` 메서드는 요청을 보낸 클라이언트의 IP 주소를 반환합니다:

```php
$ipAddress = $request->ip();
```

프록시를 통해 전달된 모든 클라이언트 IP 주소 목록이 필요한 경우는 `ips` 메서드를 사용하며, 배열 끝에 "원본" 클라이언트 IP가 위치합니다:

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는, 사용자 조작 가능 입력으로 간주하며 정보용으로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상 (Content Negotiation)

Laravel은 `Accept` 헤더를 확인해 클라이언트가 요청한 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. `getAcceptableContentTypes` 메서드는 요청에서 허용하는 콘텐츠 타입 배열을 반환합니다:

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 배열로 콘텐츠 타입을 받고, 요청이 허용하는 타입이 있으면 `true`, 없으면 `false`를 반환합니다:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 제공된 콘텐츠 타입 배열 중에서 가장 선호하는 타입을 반환합니다. 해당 타입이 없으면 `null`을 반환합니다:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML 또는 JSON만 제공하므로, `expectsJson` 메서드를 사용해 요청이 JSON 응답을 기대하는지 간단히 확인할 수 있습니다:

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청 (PSR-7 Requests)

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청, 응답)를 위한 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고 싶다면 몇 가지 라이브러리를 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 Laravel 요청과 응답을 PSR-7 호환 구현으로 변환합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

설치 후, 라우트 클로저나 컨트롤러 메서드에서 `ServerRequestInterface`를 타입 힌트해 PSR-7 요청을 받을 수 있습니다:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트 또는 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 자동으로 Laravel 응답 인스턴스로 변환되어 프레임워크가 출력합니다.

<a name="input"></a>
## 입력 (Input)

<a name="retrieving-input"></a>
### 입력 데이터 가져오기 (Retrieving Input)

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기 (Retrieving All Input Data)

`all` 메서드는 HTML 폼, XHR 요청 여부에 상관없이 모든 입력 데이터를 `array`로 반환합니다:

```php
$input = $request->all();
```

`collect` 메서드는 [컬렉션](/docs/12.x/collections) 형태로 모든 입력 데이터를 반환할 수 있습니다:

```php
$input = $request->collect();
```

부분 입력만 가져오고 싶을 때도 `collect`를 사용할 수 있습니다:

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 특정 입력 값 가져오기 (Retrieving an Input Value)

`Illuminate\Http\Request` 인스턴스에서, HTTP 동사와 관계없이 항상 `input` 메서드를 사용해 사용자 입력에 접근할 수 있습니다:

```php
$name = $request->input('name');
```

두 번째 인자로 기본값을 지정할 수 있으며, 입력값이 없을 경우 기본값이 반환됩니다:

```php
$name = $request->input('name', 'Sally');
```

배열 형태 입력은 "점 표기법(dot notation)"으로 접근할 수 있습니다:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

아무 인자 없이 호출하면 모든 입력 값을 연관 배열로 반환합니다:

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력 값 가져오기 (Retrieving Input From the Query String)

`input` 메서드는 요청 페이로드 전체(쿼리 스트링 포함)에서 값을 가져오지만, `query` 메서드는 오로지 쿼리 문자열에 대해서만 동작합니다:

```php
$name = $request->query('name');
```

값이 없으면 두 번째 인자로 지정한 기본값을 반환합니다:

```php
$name = $request->query('name', 'Helen');
```

아무 인자 없이 호출하면 모든 쿼리 문자열 값을 연관 배열로 반환합니다:

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력 값 가져오기 (Retrieving JSON Input Values)

JSON 요청에서 `Content-Type` 헤더가 `application/json`으로 정확히 설정되어 있다면, `input` 메서드를 통해 JSON 데이터에 접근할 수 있습니다. 중첩된 JSON 배열 또는 객체도 점 표기법으로 가져올 수 있습니다:

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### 문자열 처리 가능한 입력 값 가져오기 (Retrieving Stringable Input Values)

입력 값을 원시 문자열이 아닌 [Illuminate\Support\Stringable](/docs/12.x/strings) 인스턴스로 받고 싶으면 `string` 메서드를 사용하세요:

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력 값 가져오기 (Retrieving Integer Input Values)

`integer` 메서드는 입력 값을 정수로 변환 시도합니다. 입력이 없거나 변환이 실패하면 기본값을 반환합니다. 페이지네이션 숫자 입력 등에서 유용합니다:

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력 값 가져오기 (Retrieving Boolean Input Values)

HTML 체크박스 등에서 문자열 형태로 전달되는 "참값"(예: "true", "on")을 불리언으로 변환할 때는 `boolean` 메서드를 사용합니다. 이 메서드는 1, "1", true, "true", "on", "yes"를 참으로 판단하고, 그 외는 거짓으로 처리합니다:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### 배열 입력 값 가져오기 (Retrieving Array Input Values)

`array` 메서드는 값을 배열로 강제 변환해 반환합니다. 입력이 없으면 빈 배열을 반환합니다:

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력 값 가져오기 (Retrieving Date Input Values)

날짜/시간 형식 입력은 `date` 메서드를 사용해 Carbon 인스턴스로 받을 수 있습니다. 값이 없으면 `null`을 반환합니다:

```php
$birthday = $request->date('birthday');
```

두 번째, 세 번째 인자로 날짜 포맷과 타임존을 지정할 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력 값이 있지만 형식이 올바르지 않으면 `InvalidArgumentException` 예외가 발생하므로, 사전에 유효성 검사를 권장합니다.

<a name="retrieving-enum-input-values"></a>
#### enum 입력 값 가져오기 (Retrieving Enum Input Values)

PHP [enum](https://www.php.net/manual/en/language.types.enumerations.php)에 대응하는 입력 값은 `enum` 메서드로도 받을 수 있습니다. 입력이 없거나 enum에 매칭되는 값이 없으면 `null`을 반환합니다. `enum` 메서드는 입력 이름과 enum 클래스를 인자로 받습니다:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

기본값도 지정할 수 있습니다:

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

배열 형태 enum 값은 `enums` 메서드를 사용해 enum 인스턴스 배열로 받을 수 있습니다:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력 가져오기 (Retrieving Input via Dynamic Properties)

`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티로도 입력값에 접근할 수 있습니다. 예를 들어 `name` 필드가 있을 때:

```php
$name = $request->name;
```

동적 프로퍼티 사용 시 Laravel은 우선 요청 payload에서 값을 찾고, 없으면 매칭된 라우트 매개변수에서 값을 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터 일부만 가져오기 (Retrieving a Portion of the Input Data)

입력의 일부만 필요할 때는 `only`와 `except` 메서드를 사용하세요. 두 메서드는 배열 또는 여러 인수를 받을 수 있습니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 존재하는 키/값 페어만 반환하며, 없는 키는 결과에 포함하지 않습니다.

<a name="input-presence"></a>
### 입력 존재 여부 확인 (Input Presence)

`has` 메서드로 특정 입력 값이 존재하는지 확인할 수 있습니다. 존재하면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    // ...
}
```

배열로 여러 키를 넘기면 모두 존재하는지 확인합니다:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny`는 하나라도 존재하면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 입력 값이 존재할 때 주어진 클로저를 실행합니다:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘겨 값이 없을 때의 동작을 정의할 수도 있습니다:

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재함
}, function () {
    // "name" 값이 없음
});
```

값이 존재하고 빈 문자열이 아닐 때는 `filled` 메서드를 사용합니다:

```php
if ($request->filled('name')) {
    // ...
}
```

값이 없거나 빈 문자열일 때는 `isNotFilled`를 사용합니다:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 넘겨 모두 빈 문자열이거나 없는지 확인할 수도 있습니다:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled`는 지정된 값 중 하나라도 빈 문자열이 아니면 `true`입니다:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled`는 값이 존재하고 비어있지 않을 때 클로저를 실행합니다:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저는 값이 없거나 빈 문자열일 때 실행됩니다:

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져 있음
}, function () {
    // "name" 값이 채워져 있지 않음
});
```

키가 요청에 없는지 확인하려면 `missing`과 `whenMissing` 메서드를 사용합니다:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // "name" 값이 없음
}, function () {
    // "name" 값이 있음
});
```

<a name="merging-additional-input"></a>
### 추가 입력 병합하기 (Merging Additional Input)

기존 입력에 수동으로 추가 입력을 병합하려면 `merge` 메서드를 사용하세요. 기존 키가 있으면 덮어씁니다:

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 키가 없을 때만 병합합니다:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 기존 입력값 (Old Input)

Laravel은 다음 요청에서 이전 입력을 유지할 수 있게 해줍니다. 검증 오류 발생 시 폼 재출력을 쉽게 하도록 도와줍니다. Laravel의 내장 [유효성 검사 기능](/docs/12.x/validation)을 사용하면 직접 세션 입력 플래싱 메서드를 사용할 필요가 거의 없습니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값 세션에 플래시하기 (Flashing Input to the Session)

`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력값을 [세션](/docs/12.x/session)에 저장해서 다음 요청 때 사용할 수 있게 합니다:

```php
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드로 입력값의 일부만 플래시할 수 있습니다. 민감한 정보(예: 비밀번호)를 세션에 저장하는 것을 피할 때 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리디렉션 (Flashing Input Then Redirecting)

입력값 플래시 후 이전 페이지로 리디렉션하는 경우 `withInput` 메서드를 쉽게 체이닝할 수 있습니다:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기 (Retrieving Old Input)

`Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출해 이전에 플래시된 입력 데이터를 세션에서 얻을 수 있습니다:

```php
$username = $request->old('username');
```

Blade 템플릿 내에서는 전역 `old` 헬퍼가 더 편리합니다. 해당 폼 필드에 이전 입력값이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기 (Retrieving Cookies From Requests)

Laravel이 생성하는 쿠키는 암호화되고 인증 코드로 서명되어 있어, 클라이언트가 변경하면 무효로 간주됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력 자르기 및 정규화 (Input Trimming and Normalization)

기본적으로 Laravel은 글로벌 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings` 와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이들은 모든 문자열 입력을 자동으로 앞뒤 공백을 제거하고, 빈 문자열을 `null`로 변환합니다. 덕분에 라우트나 컨트롤러에서 입력 정규화에 신경 쓸 필요가 없습니다.

#### 입력 정규화 비활성화하기

입력 정규화를 전역에서 비활성화하려면, 애플리케이션 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 사용해 두 미들웨어를 제거할 수 있습니다:

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware) {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

특정 요청에 대해서만 자르기 및 빈 문자열 변환을 비활성화하려면 `trimStrings` 와 `convertEmptyStringsToNull` 미들웨어 메서드를 `bootstrap/app.php`에 아래와 같이 설정할 수 있습니다. 이 메서드들은 예외를 지정하는 클로저 배열을 받으며, 클로저는 해당 요청에서 정규화를 건너뛸지 여부를 `true`/`false`로 반환해야 합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```

<a name="files"></a>
## 파일 (Files)

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기 (Retrieving Uploaded Files)

`Illuminate\Http\Request` 인스턴스에서 `file` 메서드 또는 동적 프로퍼티로 업로드된 파일을 얻을 수 있습니다. `file` 메서드는 PHP `SplFileInfo`를 확장한 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 파일과 상호작용할 여러 메서드를 제공합니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```

업로드된 파일이 있는지 확인하려면 `hasFile` 메서드를 사용하세요:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증하기 (Validating Successful Uploads)

파일 존재 여부 외에, `isValid` 메서드로 업로드 과정에 문제 없는지도 확인할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자 (File Paths and Extensions)

`UploadedFile` 클래스는 파일의 전체 경로나 확장자에 접근하는 메서드도 제공합니다. `extension` 메서드는 파일 내용에 기반해 확장자를 추측하는데, 클라이언트가 보낸 확장자와 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드 (Other File Methods)

`UploadedFile` 인스턴스가 제공하는 다른 메서드도 다양합니다. 자세한 정보는 [클래스의 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기 (Storing Uploaded Files)

업로드된 파일 저장은 대부분 설정된 [파일시스템](/docs/12.x/filesystem)을 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 구성된 디스크 중 하나로 이동시킵니다. 로컬 파일 시스템이나 Amazon S3 같은 클라우드 스토리지 모두 가능합니다.

`store`는 파일이 저장될 위치(파일명 제외, 루트 상대 경로)를 첫 번째 인자로 받습니다. 파일명은 고유 ID로 자동 생성됩니다.

두 번째 인자는 사용할 디스크 이름이며, 이 메서드는 저장된 파일의 디스크 루트 상대 경로를 반환합니다:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 직접 지정하려면 `storeAs` 메서드를 사용하며 경로, 파일명, 디스크명을 인자로 받습니다:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> 파일 저장에 대한 자세한 내용은 [전체 파일 저장 문서](/docs/12.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정하기 (Configuring Trusted Proxies)

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 앱을 실행할 때, `url` 헬퍼로 HTTPS 링크가 생성되지 않을 수 있습니다. 이는 앱이 포트 80에서 로드 밸런서의 트래픽을 받아 HTTP로 처리하기 때문입니다.

이 문제는 Laravel 기본 제공 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화해 로드 밸런서(프록시)를 신뢰 대상에 추가함으로써 해결할 수 있습니다. 신뢰할 프록시는 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드로 지정합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

추가로, 신뢰할 프록시 헤더도 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> [!NOTE]
> AWS Elastic Load Balancing을 사용할 경우 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB` 여야 합니다. 표준 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 `Forwarded` 헤더를 사용하는 로드 밸런서라면 `Request::HEADER_FORWARDED`를 사용하세요. 가능한 상수에 대한 자세한 사항은 Symfony 문서의 [프록시 신뢰](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기 (Trusting All Proxies)

AWS 같은 클라우드 로드 밸런서 제공자는 실제 프록시 IP를 알기 어려울 수 있습니다. 이 경우 `*`를 사용해 모든 프록시를 신뢰할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정하기 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용에 상관없이 모든 요청에 응답하며, 웹 요청 시 절대 URL 생성에 해당 헤더 값을 사용합니다.

보통 Nginx, Apache 같은 웹서버에서 특정 호스트명에 해당하는 요청만 애플리케이션에 전달하도록 설정해야 합니다. 그러나 웹서버 직접 설정 권한이 없고 Laravel에서 특정 호스트명만 응답하도록 제한하고 싶을 때는 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하세요.

`TrustHosts` 미들웨어는 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드로 활성화하며, `at` 인수로 신뢰할 호스트명을 지정합니다. 다른 호스트의 요청은 차단됩니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 서브도메인 요청도 자동으로 신뢰하는데, 이 동작을 비활성화하려면 `subdomains` 인수를 `false`로 설정하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

신뢰할 호스트를 애플리케이션 설정 파일이나 데이터베이스에서 동적으로 가져와야 한다면, `at` 인수에 클로저를 전달할 수도 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```