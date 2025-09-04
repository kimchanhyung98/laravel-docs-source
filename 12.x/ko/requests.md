# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값 처리](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력 존재 여부 확인](#input-presence)
    - [추가 입력값 병합하기](#merging-additional-input)
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

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션이 처리 중인 HTTP 요청에 대해 객체 지향적으로 상호작용할 수 있는 방식을 제공하며, 요청과 함께 제출된 입력값, 쿠키, 파일 등을 가져올 수 있도록 해줍니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청에 접근하기

의존성 주입(dependency injection)을 통해 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저 또는 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 됩니다. 들어오는 요청 인스턴스는 Laravel [서비스 컨테이너](/docs/12.x/container)에 의해 자동으로 주입됩니다.

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

        // 사용자를 저장합니다...

        return redirect('/users');
    }
}
```

위와 같이, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트로 지정할 수 있습니다. 서비스 컨테이너는 클로저가 실행될 때 자동으로 요청을 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드에서 라우트 파라미터 입력값도 함께 받으려면, 의존성 인수들 뒤에 라우트 파라미터를 나열하면 됩니다. 예를 들어 라우트가 다음과 같이 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

아래와 같이 컨트롤러 메서드를 정의하면 `Illuminate\Http\Request` 타입힌트로 요청을 받고, `id` 라우트 파라미터도 사용할 수 있습니다.

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
        // 사용자를 업데이트합니다...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사할 수 있는 다양한 메서드를 제공합니다. 이 클래스는 `Symfony\Component\HttpFoundation\Request`를 확장하고 있습니다. 아래에서 가장 중요한 몇 가지 메서드를 다루겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어 요청이 `http://example.com/foo/bar`라면, `path` 메서드의 반환값은 `foo/bar`가 됩니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로 및 라우트 검사

`is` 메서드는 요청 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자로 와일드카드 패턴을 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면, 요청이 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)와 매칭되었는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

들어온 요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 문자열 없이 URL만 반환하고, `fullUrl` 메서드는 쿼리 문자열까지 포함합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열 데이터를 추가하고 싶다면, `fullUrlWithQuery` 메서드를 사용합니다. 이 메서드는 현재 쿼리 문자열에 주어진 배열 데이터를 병합하여 반환합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 문자열 파라미터를 제외한 현재 URL을 얻으려면 `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기

요청의 "호스트" 정보를 얻으려면 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용할 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드(HTTP Verb) 가져오기

`method` 메서드는 요청의 HTTP 메서드를 반환합니다. 그리고 `isMethod` 메서드를 사용하여, HTTP 메서드가 주어진 문자열과 일치하는지 검사할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용하여 요청 헤더 값을 가져올 수 있습니다. 해당 헤더가 없으면 `null`이 반환됩니다. 다만, 두 번째 인수로 기본값을 넘기면, 헤더가 요청에 없을 때 해당 값이 반환됩니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 요청에 지정한 헤더가 포함되어 있는지 확인합니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해, `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 bearer 토큰을 쉽게 추출할 수 있습니다. 해당 헤더가 없으면 빈 문자열을 반환합니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드로 요청을 보낸 클라이언트의 IP 주소를 가져올 수 있습니다.

```php
$ipAddress = $request->ip();
```

여러 프록시를 거쳐 전달된 모든 클라이언트 IP 주소의 배열이 필요하다면 `ips` 메서드를 사용할 수 있습니다. "원본" 클라이언트 IP 주소는 배열의 마지막에 위치합니다.

```php
$ipAddresses = $request->ips();
```

IP 주소는 신뢰할 수 없는, 사용자에 의해 조작 가능한 입력값임을 염두에 두고, 참고용 정보로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 요청의 `Accept` 헤더를 검사하여 요청된 콘텐츠 타입을 확인할 수 있는 여러 메서드를 제공합니다. 우선, `getAcceptableContentTypes` 메서드는 요청이 수락 가능한 모든 콘텐츠 타입의 배열을 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 인수로 받아, 요청이 이 중 하나라도 허용하면 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드를 사용하면, 주어진 콘텐츠 타입 배열 중에서 요청이 가장 선호하는 콘텐츠 타입을 판단할 수 있습니다. 요청에 일치하는 타입이 없으면 `null`이 반환됩니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

대부분의 애플리케이션이 HTML 혹은 JSON만 제공하는 경우, 요청이 JSON 응답을 기대하는지 빠르게 판단하려면 `expectsJson` 메서드를 사용할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청, 응답 등)에 대한 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고 싶다면 몇 가지 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 이용해 일반 Laravel 요청/응답을 PSR-7 호환 구현체로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

라이브러리 설치 후, 라우트 클로저나 컨트롤러 메서드에서 요청 인터페이스를 타입힌트로 지정하면 PSR-7 요청 인스턴스를 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 자동으로 Laravel 응답 인스턴스로 변환되어 프레임워크가 응답을 처리합니다.

<a name="input"></a>
## 입력값 처리 (Input)

<a name="retrieving-input"></a>
### 입력값 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기

`all` 메서드를 사용하여 들어온 요청의 모든 입력값을 `array` 형태로 가져올 수 있습니다. 이 메서드는 요청이 HTML 폼이든 XHR 요청이든 상관 없이 사용 가능합니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면, 모든 입력값을 [컬렉션](/docs/12.x/collections) 형태로 가져올 수 있습니다.

```php
$input = $request->collect();
```

또한, `collect` 메서드에 인수로 키를 넘기면 해당 입력값 부분만을 컬렉션으로 가져올 수도 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 개별 입력값 가져오기

`Illuminate\Http\Request` 인스턴스에서 HTTP 메서드와 관계없이, 아래 메서드들을 통해 유저 입력값을 편리하게 접근할 수 있습니다. 대표적으로 `input` 메서드는 HTTP 메서드와 관계 없이 사용 가능하며, 원하는 입력값을 반환합니다.

```php
$name = $request->input('name');
```

입력값이 없을 때 반환할 기본값을 두 번째 인수로 넘길 수도 있습니다.

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 폼 입력값을 다룰 때는 "dot" 표기법을 사용할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

매개변수 없이 `input` 메서드를 호출하면 모든 입력값을 연관 배열로 반환합니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력값 가져오기

`input` 메서드는 전체 요청 페이로드(쿼리 문자열도 포함)에서 값을 가져옵니다. 만약 쿼리 문자열에서만 값을 가져오고 싶다면 `query` 메서드를 사용하세요.

```php
$name = $request->query('name');
```

요청에 해당 쿼리 파라미터가 없을 때 반환할 기본값은 두 번째 인수로 지정할 수 있습니다.

```php
$name = $request->query('name', 'Helen');
```

`query` 메서드를 인수 없이 호출하면, 모든 쿼리 문자열 값을 연관 배열로 반환합니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

애플리케이션에 JSON 요청이 들어오는 경우, `Content-Type` 헤더가 `application/json`으로 올바르게 지정되어 있다면 `input` 메서드를 통해 JSON 데이터를 가져올 수 있습니다. "dot" 표기법도 지원하므로, JSON 배열·객체 내부에 중첩된 값도 조회 가능합니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 가져오기

입력값을 기본 `string` 형태로 받는 대신, `string` 메서드를 사용하면 [Illuminate\Support\Stringable](/docs/12.x/strings) 인스턴스로 입력값을 다룰 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 가져오기

입력값을 정수 형태로 받고 싶다면 `integer` 메서드를 사용할 수 있습니다. 이 메서드는 입력값을 정수로 캐스팅하려 시도하며, 값이 없거나 변환에 실패한 경우 지정한 기본값을 반환합니다. 페이지네이션 등 숫자 입력에 유용합니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기

체크박스와 같은 HTML 요소는 값이 문자열로 넘어올 수 있습니다(예: "true", "on" 등). 편의를 위해 `boolean` 메서드를 이용하면 입력값을 불리언으로 변환해 가져올 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환하며, 이외에는 `false`를 반환합니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### 배열 형태의 입력값 가져오기

배열 형태의 입력값은 `array` 메서드로 항상 배열로 변환하여 반환받을 수 있습니다. 요청에 주어진 입력값이 없으면 빈 배열이 반환됩니다.

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜/시간이 포함된 입력값은 편리하게 `date` 메서드를 사용해 Carbon 인스턴스로 변환해 가져올 수 있습니다. 해당 이름으로 입력값이 없으면 `null`이 반환됩니다.

```php
$birthday = $request->date('birthday');
```

`date` 메서드의 두 번째와 세 번째 인수로 날짜 포맷과 타임존을 지정할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 존재하지만 형식이 올바르지 않다면 `InvalidArgumentException`이 발생하므로, 이 메서드 사용 전 입력값 검증을 권장합니다.

<a name="retrieving-enum-input-values"></a>
#### Enum(열거형) 입력값 가져오기

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)과 일치하는 입력값도 요청에서 가져올 수 있습니다. 입력값이 없거나, enum에 매칭되는 값이 없다면 `null`이 반환됩니다. `enum` 메서드의 첫 번째 인수는 입력값의 이름, 두 번째는 enum 클래스명을 전달합니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

값이 없거나 올바르지 않을 때 반환할 기본값도 세 번째 인수로 넘길 수 있습니다.

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

입력값이 PHP enum에 매칭되는 값들의 배열이라면, `enums` 메서드로 해당 enum 인스턴스 배열을 받을 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 가져오기

`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티를 통해서도 입력값에 접근할 수 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 아래와 같이 값을 읽을 수 있습니다.

```php
$name = $request->name;
```

동적 프로퍼티 사용 시, Laravel은 먼저 요청 페이로드에서 값을 찾고, 없으면 매칭된 라우트의 파라미터에서 값을 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값의 일부만 가져오기

입력값의 일부만 추출하려면 `only`와 `except` 메서드를 사용할 수 있습니다. 이 두 메서드는 배열이나 여러 인수를 받을 수 있습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 존재하는 키-값 쌍만 반환하며, 요청에 없는 키-값 쌍은 반환하지 않습니다.

<a name="input-presence"></a>
### 입력 존재 여부 확인

요청에 특정 값이 존재하는지 확인하고 싶다면 `has` 메서드를 사용할 수 있습니다. 값이 있으면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 넘기면, 명시한 모든 값이 존재하면 `true`가 반환됩니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 전달된 값들 중 하나라도 존재하면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 값이 있을 때 지정한 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘기면, 값이 없을 때 해당 클로저가 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재할 때...
}, function () {
    // "name" 값이 존재하지 않을 때...
});
```

값이 요청에 존재하고, 빈 문자열이 아닐 때 확인하려면 `filled` 메서드를 사용할 수 있습니다.

```php
if ($request->filled('name')) {
    // ...
}
```

요청에서 값이 없거나 빈 문자열일 때는 `isNotFilled` 메서드를 사용할 수 있습니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 넘길 경우, `isNotFilled`는 전달된 모든 값이 없거나 빈 문자열인 경우에만 `true`를 반환합니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 전달한 값들 중 하나라도 빈 문자열이 아닌 값이 있으면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 요청에 값이 존재하고 빈 문자열이 아닐 때 지정한 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘기면, 값이 "filled"가 아닐 때 해당 클로저가 실행됩니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워졌을 때...
}, function () {
    // "name" 값이 채워지지 않았을 때...
});
```

특정 키가 요청에 존재하지 않는지 확인하려면 `missing` 또는 `whenMissing` 메서드를 사용할 수 있습니다.

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // "name" 값이 없을 때...
}, function () {
    // "name" 값이 존재할 때...
});
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합하기

기존 요청의 입력 데이터에 추가 입력값을 수동으로 병합해야 할 때는 `merge` 메서드를 사용할 수 있습니다. 이미 존재하는 키가 있으면 주어진 값으로 덮어씁니다.

```php
$request->merge(['votes' => 0]);
```

해당 키가 존재하지 않을 때만 입력값을 병합하려면 `mergeIfMissing` 메서드를 사용하세요.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값

Laravel은 한 요청에서 입력값을 세션에 저장하여 다음 요청 동안 유지할 수 있게 해줍니다. 이 기능은 주로 유효성 검증 오류 발생 시 폼을 다시 채우는 데 유용합니다. Laravel의 [유효성 검증 기능](/docs/12.x/validation)을 사용하면 이 세션 입력값 플래시 메서드를 직접 호출하지 않아도 필요한 경우 자동으로 처리해 줍니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력값을 [세션](/docs/12.x/session)에 플래시하여, 사용자의 다음 요청에서도 값이 유지되도록 합니다.

```php
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드를 사용하면, 입력값 중 일부분만 세션에 저장할 수 있습니다. 비밀번호 등 민감한 정보는 세션에서 제외하는 데 유용합니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트

입력값을 세션에 플래시한 뒤 이전 페이지로 리다이렉트하는 경우가 많으므로, `withInput` 메서드를 리다이렉트와 함께 쉽게 체이닝할 수 있습니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하거나, [세션](/docs/12.x/session)에서 값을 읽어올 수 있습니다.

```php
$username = $request->old('username');
```

Laravel에서는 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값으로 폼을 다시 채울 때 더욱 편리하게 사용할 수 있습니다. 해당 필드에 이전 입력값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel이 생성하는 모든 쿠키는 암호화되어 있고 인증 코드로 서명되어 있습니다. 클라이언트 측에서 값이 변경된 경우 무효 처리됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화 (Input Trimming and Normalization)

Laravel은 기본적으로 애플리케이션의 글로벌 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어들은 들어오는 모든 문자열 필드의 앞뒤 공백을 자동으로 제거하고, 빈 문자열을 `null`로 변환합니다. 이를 통해 라우트나 컨트롤러에서 입력값 정규화에 신경 쓰지 않아도 됩니다.

#### 입력값 정규화 비활성화하기

모든 요청에 대해 이러한 동작을 끄고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 호출하여 두 미들웨어를 스택에서 제거하면 됩니다.

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

애플리케이션의 일부 요청에 대해서만 문자열 트리밍 또는 빈 문자열 변환을 비활성화하려면, `bootstrap/app.php` 파일에서 `trimStrings` 및 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 이 메서드들은 각각 true/false를 반환하는 클로저 배열을 인수로 받습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
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
### 업로드된 파일 가져오기

업로드된 파일은 `Illuminate\Http\Request` 인스턴스의 `file` 메서드나 동적 프로퍼티를 통해 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 인스턴스를 반환하는데, 이는 PHP의 `SplFileInfo`를 상속하며 파일과 상호작용할 수 있는 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

업로드된 파일이 요청에 포함되어 있는지 확인하려면 `hasFile` 메서드를 사용할 수 있습니다.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 성공적으로 업로드 되었는지 검증하기

파일이 요청에 존재하는지 확인하는 것 외에도, `isValid` 메서드를 사용해 업로드 과정에 오류가 없었는지 검증할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스에는 파일의 전체 경로와 확장자를 확인할 수 있는 메서드들이 있습니다. `extension` 메서드는 파일 내용을 분석하여 확장자를 추측합니다. 이 값은 클라이언트에서 제공한 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 관련 메서드

`UploadedFile` 인스턴스에서는 이 밖에도 다양한 메서드를 사용할 수 있습니다. 자세한 내용은 [클래스의 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일을 저장하려면, 보통 [파일시스템](/docs/12.x/filesystem)에 구성한 저장소 중 하나를 사용합니다. `UploadedFile` 클래스의 `store` 메서드로 로컬 filesystem이든 Amazon S3와 같은 클라우드 스토리지든 파일을 손쉽게 이동시킬 수 있습니다.

`store` 메서드는 파일을 저장할 경로(파일시스템 루트 기준 상대경로)를 첫 번째 인수로 받습니다. 파일명은 지정하지 않아도 되며, 고유한 ID로 자동 생성됩니다.

두 번째 인수로는 저장소(disk) 이름을 지정할 수 있습니다. 반환값은 해당 저장소 루트 기준 저장된 파일의 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 직접 지정하고 싶다면 `storeAs` 메서드를 사용하세요. 이 메서드는 저장 경로, 파일명, 저장소 이름을 순서대로 인수로 받습니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel의 파일 저장에 대해 더 자세한 내용은 [파일시스템 문서](/docs/12.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정하기 (Configuring Trusted Proxies)

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼 사용 시 HTTPS 링크가 생성되지 않는 현상이 있을 수 있습니다. 이는 보통 로드 밸런서에서 포트 80으로 트래픽을 전달받기 때문에 애플리케이션이 HTTPS를 인식하지 못하기 때문입니다.

이 문제를 해결하려면, Laravel에 기본 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화해 프록시나 로드 밸런서를 신뢰할 수 있도록 지정할 수 있습니다. 신뢰할 프록시는 애플리케이션의 `bootstrap/app.php` 파일의 `trustProxies` 미들웨어 메서드에서 지정합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

추가로, 신뢰할 프록시 헤더도 아래와 같이 지정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> [!NOTE]
> AWS Elastic Load Balancing을 사용한다면 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`를 사용해야 합니다. 로드 밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)에서 정의한 표준 `Forwarded` 헤더를 사용하는 경우에는 `Request::HEADER_FORWARDED`를 사용합니다. `headers` 값으로 사용할 수 있는 상수에 대한 자세한 설명은 Symfony의 [프록시 신뢰 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS나 기타 "클라우드" 로드 밸런서 환경에서는 실제 프록시의 IP를 알기 어려운 경우가 많습니다. 이런 경우에는 `*`를 사용해 모든 프록시를 신뢰하면 됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정하기 (Configuring Trusted Hosts)

Laravel은 기본적으로 HTTP 요청의 `Host` 헤더 값이 무엇이든 모든 요청에 응답합니다. 또한, 웹 요청에서 절대 URL을 생성할 때 `Host` 헤더의 값이 사용됩니다.

보통은 웹 서버(Nginx, Apache 등)에서 특정 호스트명만 애플리케이션에 전달되도록 설정합니다. 하지만, 웹 서버 설정이 불가능하거나 Laravel에서 직접 처리해야 할 경우 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화해 특정 호스트에만 응답하도록 할 수 있습니다.

`TrustHosts` 미들웨어를 활성화하려면 `bootstrap/app.php` 파일의 `trustHosts` 미들웨어 메서드를 호출하면 됩니다. 이때 `at` 인수로 응답을 허용할 호스트명 배열을 지정할 수 있습니다. 그 외의 요청은 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 애플리케이션 URL의 서브도메인에서 오는 요청도 자동으로 신뢰하도록 되어 있습니다. 만약 이 동작을 사용하지 않으려면 `subdomains` 인수로 끌 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

신뢰할 호스트를 애플리케이션의 설정 파일이나 데이터베이스 등에서 동적으로 읽어오려면, `at` 인수에 클로저를 전달할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
