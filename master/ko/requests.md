# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [컨텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 존재 여부](#input-presence)
    - [추가 입력 병합하기](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정하기](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션이 처리 중인 HTTP 요청을 객체지향적으로 다룰 수 있게 해줍니다. 또한 요청과 함께 전송된 입력값, 쿠키, 파일도 쉽게 가져올 수 있습니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청에 접근하기 (Accessing the Request)

의존성 주입(dependency injection)을 통해 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저 또는 컨트롤러 메서드에 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. Laravel의 [서비스 컨테이너](/docs/master/container)가 자동으로 요청 인스턴스를 주입합니다.

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

        // 사용자 저장 로직...

        return redirect('/users');
    }
}
```

위 예시처럼, 라우트 클로저에서 `Illuminate\Http\Request`를 타입힌트할 수도 있습니다. 서비스 컨테이너가 해당 요청 인스턴스를 클로저에 자동 주입해줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 매개변수 (Dependency Injection and Route Parameters)

컨트롤러 메서드가 라우트 매개변수도 기대하는 경우, 라우트 매개변수는 다른 의존성 뒤에 나열해야 합니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서 `Illuminate\Http\Request`를 타입힌트하고, `id` 라우트 매개변수에도 접근하려면 다음과 같이 정의할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정한 사용자를 업데이트합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트 로직...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드 (Request Path, Host, and Method)

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하는 여러 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 이 중 몇 가지 중요한 메서드를 살펴봅니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기 (Retrieving the Request Path)

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어 요청 URL이 `http://example.com/foo/bar` 라면 `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로나 라우트 검사 (Inspecting the Request Path / Route)

`is` 메서드를 사용하면 요청 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드는 요청이 특정 [이름 있는 라우트](/docs/master/routing#named-routes)와 일치하는지 판단할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기 (Retrieving the Request URL)

요청에 대한 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리스트링 없이 URL만 반환하며, `fullUrl` 메서드는 쿼리스트링까지 포함합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리스트링 데이터를 추가하려면 `fullUrlWithQuery` 메서드를 사용합니다. 이 메서드는 주어진 쿼리스트링 변수 배열과 현재 쿼리스트링을 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리스트링 파라미터를 제외하고 URL을 가져오려면 `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기 (Retrieving the Request Host)

요청의 "호스트" 정보를 다음 메서드들로 가져올 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기 (Retrieving the Request Method)

`method` 메서드는 요청의 HTTP 메서드(VERB)를 반환합니다. `isMethod` 메서드를 사용해 HTTP 메서드가 특정 값인지 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더 (Request Headers)

`header` 메서드를 이용해 요청 헤더 값을 가져올 수 있습니다. 해당 헤더가 없으면 `null`이 반환되거나, 두 번째 인자로 기본값을 지정할 수 있습니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 특정 헤더가 요청에 포함되어 있는지 여부를 확인합니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

간편하게 `Authorization` 헤더에서 Bearer 토큰만 가져오려면 `bearerToken` 메서드를 사용하세요. 헤더가 없으면 빈 문자열을 반환합니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소 (Request IP Address)

`ip` 메서드는 요청을 보낸 클라이언트의 IP 주소를 반환합니다.

```php
$ipAddress = $request->ip();
```

프록시를 거친 모든 클라이언트 IP 주소를 포함한 배열을 받고 싶으면 `ips` 메서드를 사용하세요. 배열의 마지막이 "원본" 클라이언트 IP입니다.

```php
$ipAddresses = $request->ips();
```

참고로 IP 주소는 신뢰할 수 없는 사용자 입력으로 간주하고, 주로 정보용으로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 컨텐츠 협상 (Content Negotiation)

Laravel은 요청의 `Accept` 헤더를 통해 요청된 미디어 타입을 확인하는 여러 메서드를 제공합니다.

`getAcceptableContentTypes` 메서드는 요청이 허용하는 모든 컨텐츠 타입을 배열로 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 컨텐츠 타입 배열을 받아, 요청이 그중 어느 하나라도 허용하면 `true`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 컨텐츠 타입 배열 중에서 요청자가 가장 선호하는 타입을 반환합니다. 없으면 `null`입니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML과 JSON 만을 다뤄서, 요청이 JSON 응답을 기대하는지 빠르게 확인하려면 `expectsJson` 메서드를 사용합니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청 (PSR-7 Requests)

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청과 응답)에 대한 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 받고 싶으면 몇몇 라이브러리를 설치해야 합니다. Laravel은 Symfony HTTP Message Bridge 컴포넌트를 사용해 Laravel 요청과 응답을 PSR-7 호환형으로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

설치 후 라우트 클로저나 컨트롤러 메서드에 PSR-7 요청 인터페이스를 타입힌트하여 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트 또는 컨트롤러에서 PSR-7 응답 객체를 반환하면 Laravel이 자동으로 Laravel 응답 객체로 변환하여 처리합니다.

<a name="input"></a>
## 입력 (Input)

<a name="retrieving-input"></a>
### 입력값 가져오기 (Retrieving Input)

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기 (Retrieving All Input Data)

`all` 메서드를 사용하면 HTML 폼이든 XHR 요청이든 상관없이 모든 요청 입력 데이터를 `array` 형태로 가져올 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면 입력 데이터를 [컬렉션](/docs/master/collections)으로 가져올 수도 있습니다.

```php
$input = $request->collect();
```

부분적인 입력 데이터를 컬렉션으로 가져오는 것도 가능합니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 특정 입력값 가져오기 (Retrieving an Input Value)

HTTP 메서드에 상관없이 사용자 입력값에 접근하려면 `input` 메서드를 사용하세요.

```php
$name = $request->input('name');
```

두 번째 인자로 기본값을 넘기면 요청에 값이 없을 때 기본값을 반환합니다.

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값에는 점(dot) 표기법으로 접근할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인자가 없으면 모든 입력값을 연관 배열로 가져옵니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리스트링의 입력값 가져오기 (Retrieving Input From the Query String)

`input` 메서드는 전체 요청 페이로드에서 값을 가져오지만, `query` 메서드는 쿼리스트링에서만 값을 가져옵니다.

```php
$name = $request->query('name');
```

기본값도 지정할 수 있습니다.

```php
$name = $request->query('name', 'Helen');
```

인자가 없으면 모든 쿼리스트링 값을 연관 배열로 받습니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기 (Retrieving JSON Input Values)

JSON 요청에서 `Content-Type` 헤더가 `application/json`으로 설정되어 있다면, `input` 메서드로 JSON 데이터를 접근할 수 있습니다. 점 표기법도 사용할 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 가져오기 (Retrieving Stringable Input Values)

입력을 원시 문자열 대신, [`Illuminate\Support\Stringable`](/docs/master/strings) 객체로 받고 싶으면 `string` 메서드를 사용하세요.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 가져오기 (Retrieving Integer Input Values)

입력을 정수로 받고 싶으면 `integer` 메서드를 사용합니다. 입력값이 없거나 변환에 실패하면 기본값을 반환합니다. 페이지네이션 등 숫자 입력 처리에 유용합니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기 (Retrieving Boolean Input Values)

체크박스 같은 HTML 요소에서 받는 "true", "on" 같은 문자열 값을 불리언으로 처리하려면 `boolean` 메서드를 사용하세요. 1, "1", true, "true", "on", "yes"는 `true`로 처리되며 나머지는 `false`입니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기 (Retrieving Date Input Values)

날짜/시간 입력값을 Carbon 인스턴스로 받고 싶으면 `date` 메서드를 사용하세요. 입력값이 없으면 `null`을 반환합니다.

```php
$birthday = $request->date('birthday');
```

두 번째, 세 번째 인자로 날짜 형식과 타임존도 지정할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 존재하지만 형식이 올바르지 않으면 `InvalidArgumentException` 예외가 발생하므로, 미리 유효성 검사를 하길 권장합니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 가져오기 (Retrieving Enum Input Values)

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)에 해당하는 입력값도 요청에서 가져올 수 있습니다. 값이 없거나 유효하지 않으면 `null`을 반환합니다. `enum` 메서드는 입력 이름과 enum 클래스를 인자로 받습니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

배열 형태 enum 입력값은 `enums` 메서드로 enum 인스턴스 배열로 받을 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 가져오기 (Retrieving Input via Dynamic Properties)

`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티로도 입력값에 접근할 수 있습니다. 예를 들어 폼 필드가 `name`이라면 다음과 같이 접근할 수 있습니다.

```php
$name = $request->name;
```

동적 프로퍼티를 사용할 때 Laravel은 먼저 요청 페이로드에서 해당 값을 찾고, 없으면 매칭된 라우트 매개변수에서도 검색합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터 일부 가져오기 (Retrieving a Portion of the Input Data)

입력 데이터 중 일부만 가져오려면 `only` 또는 `except` 메서드를 사용하세요. 배열 또는 인수 목록을 인자로 받을 수 있습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 존재하는 키/값만 반환하며, 요청에 없는 키/값은 포함하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 여부 (Input Presence)

`has` 메서드를 사용하면 요청에 특정 값이 존재하는지 확인할 수 있습니다. 존재하면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 인자로 주면, 배열 내 모든 값이 존재해야 `true`를 반환합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 배열 내 어느 하나라도 존재하면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 특정 값이 존재할 때 주어진 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 전달하면, 특정 값이 없을 때 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재할 때...
}, function () {
    // "name" 값이 없을 때...
});
```

값이 존재하고 빈 문자열이 아닌 경우를 확인하려면 `filled` 메서드를 사용합니다.

```php
if ($request->filled('name')) {
    // ...
}
```

값이 없거나 빈 문자열인 경우 확인하려면 `isNotFilled` 메서드를 사용합니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 인자로 주면, 모두 빈 문자열 또는 미존재여야 `true`를 반환합니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 배열 내 어느 하나라도 빈 문자열이 아니면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 값이 존재하고 빈 문자열이 아닐 때 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 전달해 값이 빈 문자열이거나 없을 때 실행하도록 할 수 있습니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 비어 있지 않을 때...
}, function () {
    // "name" 값이 비어 있을 때...
});
```

특정 키가 요청에 없음을 확인하려면 `missing`과 `whenMissing` 메서드를 사용하세요.

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // "name" 값이 없음...
}, function () {
    // "name" 값이 있음...
});
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합하기 (Merging Additional Input)

이미 존재하는 요청 입력 데이터에 추가 입력을 수동으로 병합해야 할 때가 있습니다. 이때 `merge` 메서드를 사용하세요. 이미 존재하는 키는 새로운 데이터로 덮어씌워집니다.

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 병합할 키가 요청에 없을 때만 병합합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값 (Old Input)

Laravel은 한 요청의 입력값을 다음 요청에도 보존하는 기능을 제공합니다. 이는 유효성 검사 오류가 있을 때 폼을 다시 채우는데 유용합니다. 하지만 Laravel 내장 [유효성 검사 기능](/docs/master/validation)을 사용하면 직접 세션 입력 플래시 메서드를 호출하지 않아도 자동으로 호출됩니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기 (Flashing Input to the Session)

`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력값을 [세션](/docs/master/session)에 플래시하여 다음 요청에서도 사용할 수 있게 합니다.

```php
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드는 세션에 플래시할 입력값 일부를 선택할 때 유용합니다. 예를 들어 비밀번호 같은 민감한 정보는 제외할 수 있습니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트 (Flashing Input Then Redirecting)

보통 입력값을 세션에 플래시 한 뒤, 이전 페이지로 리다이렉트하는 경우가 많습니다. 이때 `withInput` 메서드를 리다이렉트 체인에 이어 호출하면 간편합니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기 (Retrieving Old Input)

이전 요청에서 플래시된 입력값은 `Illuminate\Http\Request` 인스턴스의 `old` 메서드로 가져올 수 있습니다. `old` 메서드는 세션에서 이전 플래시 데이터를 꺼냅니다.

```php
$username = $request->old('username');
```

Blade 템플릿 내에서는 글로벌 `old` 헬퍼를 사용하는 것이 편리합니다. 이전 입력값이 없으면 `null`을 반환합니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기 (Retrieving Cookies From Requests)

Laravel에서 생성된 쿠키는 모두 암호화되고 인증 코드가 서명되어 있어, 클라이언트가 쿠키를 변조하면 무효로 처리됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화 (Input Trimming and Normalization)

기본적으로 Laravel은 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 글로벌 스택에 포함합니다. 이 미들웨어들은 모든 들어오는 문자열 입력값을 자동으로 트리밍하고, 빈 문자열을 `null`로 변환해 줍니다. 덕분에 라우트나 컨트롤러에서 이런 작업을 신경 쓰지 않아도 됩니다.

#### 입력값 정규화 비활성화하기

애플리케이션의 모든 요청에서 이 동작을 비활성화하려면, `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드로 두 미들웨어를 제거하세요.

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

요청의 일부에서만 문자열 트리밍과 빈 문자열 변환을 비활성화하고 싶으면, `bootstrap/app.php`에서 `trimStrings`와 `convertEmptyStringsToNull` 미들웨어 메서드에 조건 클로저를 넘기면 됩니다. 클로저는 `true` 또는 `false`를 반환해 해당 요청에 적용 여부를 결정합니다.

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

`Illuminate\Http\Request` 인스턴스에서 업로드된 파일은 `file` 메서드나 동적 프로퍼티로 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 인스턴스를 반환하는데, 이 클래스는 PHP의 `SplFileInfo`를 확장하며 파일 조작에 유용한 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

파일이 요청에 포함되었는지 확인하려면 `hasFile` 메서드를 사용합니다.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증 (Validating Successful Uploads)

파일이 실제로 성공적으로 업로드되었는지는 `isValid` 메서드로 확인할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자 (File Paths and Extensions)

`UploadedFile` 클래스는 파일의 전체 경로와 확장자에 접근하는 메서드도 제공합니다. `extension` 메서드는 파일 내용 기반으로 확장자를 추측하며, 이 확장자는 클라이언트가 보낸 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드 (Other File Methods)

`UploadedFile` 인스턴스에서 사용할 수 있는 다양한 메서드가 있습니다. 자세한 내용은 [클래스 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기 (Storing Uploaded Files)

파일 저장에는 일반적으로 설정한 [파일 시스템](/docs/master/filesystem)을 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 지정한 디스크(로컬 또는 클라우드 스토리지)로 옮겨줍니다.

`store` 메서드는 파일을 저장할 경로를 인자로 받으며, 경로에 파일명은 포함하지 않아야 합니다. 파일명은 자동으로 고유한 ID를 생성합니다.

두 번째 인자로 디스크 이름을 지정할 수 있습니다. 메서드는 디스크 루트부터의 저장 경로를 반환합니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 직접 지정하려면 `storeAs` 메서드를 사용하세요.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel 파일 저장에 대한 자세한 내용은 [파일 저장 문서](/docs/master/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정하기 (Configuring Trusted Proxies)

TLS/SSL 인증서를 종료시키는 로드밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼로 HTTPS 링크를 만들지 않는 경우가 있습니다. 이는 로드밸런서가 포트 80으로 트래픽을 전달해주기 때문에, 애플리케이션이 보안 링크를 생성해야 한다는 사실을 알지 못해서 발생합니다.

이 문제를 해결하려면 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화해야 합니다. 이 미들웨어는 애플리케이션이 신뢰할 프록시 서버나 로드밸런서를 정의할 수 있게 해줍니다. 신뢰할 프록시는 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드로 설정하세요.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 프록시 외에도 신뢰할 프록시 헤더를 설정할 수 있습니다.

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
> AWS Elastic Load Balancing을 사용하는 경우 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`이어야 합니다. 표준 `Forwarded` 헤더([RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4))를 사용하는 로드밸런서는 `Request::HEADER_FORWARDED` 값을 써야 합니다. 사용할 수 있는 상수에 대한 자세한 내용은 Symfony 문서의 [신뢰할 수 있는 프록시](https://symfony.com/doc/7.0/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기 (Trusting All Proxies)

Amazon AWS 또는 기타 클라우드 로드밸런서 제공업체를 사용하는 경우 실제 프록시 IP를 알 수 없을 때가 있습니다. 이때는 아래처럼 `*`로 모든 프록시를 신뢰할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정하기 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용에 상관없이 모든 요청에 응답합니다. 또한 URL 생성 시 이 `Host` 헤더 값을 기반으로 절대 URL을 만듭니다.

보통은 Nginx, Apache 같은 웹서버에서 특정 호스트명에 대해서만 애플리케이션에 요청을 보내도록 설정합니다. 하지만 웹서버를 직접 설정할 수 없고 Laravel에서 특정 호스트명만 응답하도록 설정하고 싶다면, `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다.

`TrustHosts` 미들웨어는 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드로 활성화할 수 있습니다. `at` 인자로 신뢰할 호스트명을 배열로 지정하면, 지정되지 않은 `Host` 헤더가 포함된 요청은 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 애플리케이션 URL의 서브도메인에서도 요청을 신뢰합니다. 이 동작을 끄려면 `subdomains` 인자를 `false`로 설정하세요.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

신뢰할 호스트 목록을 설정 파일이나 데이터베이스에서 동적으로 가져와야 한다면, `at` 인자에 클로저를 넘길 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```