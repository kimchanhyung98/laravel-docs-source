# HTTP 요청

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력(Input)](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 존재 확인](#input-presence)
    - [추가 입력 병합](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 처리 중인 현재 HTTP 요청에 대해 객체 지향적으로 상호작용할 수 있는 방법을 제공하며, 요청과 함께 전송된 입력값, 쿠키, 파일도 손쉽게 조회할 수 있습니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청에 접근하기

의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. 들어오는 요청 인스턴스는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 사용자 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 사용자 저장...

        return redirect('/users');
    }
}
```

위에서 언급한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트할 수 있습니다. 서비스 컨테이너가 실행 시점에 자동으로 요청을 주입해줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드가 라우트 파라미터 입력도 기대한다면, 라우트 파라미터를 다른 의존성 뒤에 나열해야 합니다. 예를 들어, 아래와 같이 라우트가 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

여전히 `Illuminate\Http\Request`를 타입힌트하며, 아래처럼 `id` 값을 메서드의 두 번째 인자로 받을 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 사용자 업데이트
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하기 위한 다양한 메서드를 제공합니다. 해당 클래스는 `Symfony\Component\HttpFoundation\Request` 를 확장합니다. 아래 주요 메서드들을 정리합니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 조회

`path` 메서드는 요청 경로 정보를 반환합니다. 예를 들어, 들어오는 요청 주소가 `http://example.com/foo/bar`라면, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사

`is` 메서드는 요청 경로가 주어진 패턴과 일치하는지 확인할 수 있습니다. 이 메서드에서는 `*` 기호를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면, [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)와 일치하는지 판단할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 조회

전체 요청 URL을 얻으려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리스트링을 제외한 URL을 반환하고, `fullUrl`은 쿼리스트링도 포함한 전체 URL을 반환합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리스트링을 추가하고 싶다면 `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 전달한 배열을 현재 쿼리스트링 변수와 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 파라미터를 제외한 현재 URL이 필요하다면 `fullUrlWithoutQuery` 메서드를 사용하면 됩니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 조회

들어오는 요청의 "호스트" 값을 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 얻을 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 조회

`method` 메서드는 요청의 HTTP 메서드를 문자열로 반환합니다. 또한, `isMethod` 메서드를 사용해 HTTP 메서드가 특정 값과 일치하는지 검사할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스의 `header` 메서드를 사용하여 요청 헤더를 가져올 수 있습니다. 헤더가 요청에 없을 경우 기본적으로 `null`을 반환합니다. 단, 두 번째 인자로 기본값을 전달할 수 있습니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 해당 헤더가 요청에 존재하는지 여부를 반환합니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해 `bearerToken` 메서드를 사용해 `Authorization` 헤더의 Bearer 토큰을 쉽게 가져올 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드를 사용해 요청을 보낸 클라이언트의 IP 주소를 가져올 수 있습니다.

```php
$ipAddress = $request->ip();
```

프록시를 통해 전달된 모든 클라이언트 IP 주소가 포함된 배열이 필요한 경우 `ips` 메서드를 사용할 수 있습니다. 배열의 마지막이 "원본" 클라이언트 IP입니다.

```php
$ipAddresses = $request->ips();
```

일반적으로, IP 주소는 신뢰할 수 없는 사용자 입력이므로 참고용으로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 요청의 `Accept` 헤더를 통해 요청된 콘텐츠 타입을 검사하기 위한 여러 메서드를 제공합니다. 우선, `getAcceptableContentTypes` 메서드는 요청이 수락할 수 있는 모든 콘텐츠 타입을 배열로 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 받아, 해당 타입 중 하나라도 요청에서 허용하면 `true`를, 그렇지 않으면 `false`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 주어진 배열 중 요청이 가장 선호하는 콘텐츠 타입을 반환합니다. 해당 타입이 없으면 `null`을 반환합니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML 또는 JSON만 제공하기 때문에, 들어오는 요청이 JSON 응답을 기대하는지 빠르게 확인하려면 `expectsJson` 메서드를 사용할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청과 응답 등 HTTP 메시지를 위한 인터페이스를 정의합니다. Laravel 기본 요청 대신 PSR-7 요청 인스턴스를 사용하려면 몇 가지 라이브러리를 설치해야 합니다. Laravel은 전형적인 요청/응답을 PSR-7 호환으로 변환하기 위해 *Symfony HTTP Message Bridge* 컴포넌트를 사용합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리들을 설치한 후, 라우트 클로저 또는 컨트롤러 메서드에서 PSR-7 요청 인터페이스를 타입힌트하면 PSR-7 요청 객체를 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 다시 Laravel 응답 인스턴스로 변환하여 출력합니다.

<a name="input"></a>
## 입력(Input)

<a name="retrieving-input"></a>
### 입력값 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 가져오기

`all` 메서드를 사용하여 들어오는 요청의 모든 입력을 `array` 형태로 가져올 수 있습니다. 이 메서드는 요청이 HTML 폼이든 XHR 요청이든 상관없이 사용할 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면 요청 입력값을 [컬렉션](/docs/{{version}}/collections) 형태로도 가져올 수 있습니다.

```php
$input = $request->collect();
```

`collect` 메서드는 일부 입력값만 컬렉션으로 받을 수도 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 단일 입력값 가져오기

몇 가지 간단한 메서드로 `Illuminate\Http\Request` 인스턴스에서 모든 사용자 입력값에 접근할 수 있습니다. 어떤 HTTP 메서드(POST/GET 등)를 사용했는지 상관없이 `input` 메서드를 사용해 값을 가져올 수 있습니다.

```php
$name = $request->input('name');
```

요청에 해당 입력값이 없을 때를 대비해, 두 번째 인자로 기본값을 전달할 수 있습니다.

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값과 작업할 때는 "dot" 표기법을 사용하여 배열 내 값을 가져올 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인자 없이 `input` 메서드를 호출하면 모든 입력값을 연관 배열로 반환합니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력 가져오기

`input` 메서드는 전체 요청(쿼리스트링 포함)에서 값을 가져오지만, `query` 메서드는 오직 쿼리스트링에서만 값을 가져옵니다.

```php
$name = $request->query('name');
```

요청에 해당 쿼리스트링 값이 없으면 두 번째 인자로 전달한 기본값이 반환됩니다.

```php
$name = $request->query('name', 'Helen');
```

인자 없이 `query`를 호출하면 모든 쿼리스트링 값을 연관 배열로 반환합니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

애플리케이션에 JSON 형식 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 설정되어 있다면 `input` 메서드를 통해 JSON 데이터에 접근할 수 있습니다. "dot" 표기법으로 중첩 JSON 값도 조회할 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable(문자열 빌더) 입력값 가져오기

요청 입력값을 원시 `string` 대신 [Illuminate\Support\Stringable](/docs/{{version}}/strings) 인스턴스로 받고 싶다면 `string` 메서드를 사용할 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수로 입력값 가져오기

입력값을 정수로 받고 싶다면 `integer` 메서드를 사용하세요. 이 메서드는 값을 정수로 변환하려고 시도합니다. 값이 없거나 변환에 실패하면 지정한 기본값이 반환됩니다. 페이지네이션 등 숫자 입력에 유용합니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기

HTML 체크박스와 같은 요소에서 "true", "on" 등 문자열 형태로 참 값을 받는 경우가 많습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes" 값을 `true`로, 나머지는 `false`로 변환해줍니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜/시간이 포함된 입력값은 `date` 메서드를 사용해 [Carbon](https://carbon.nesbot.com/) 인스턴스로 받을 수 있습니다. 입력값이 없으면 `null`이 반환됩니다.

```php
$birthday = $request->date('birthday');
```

`date` 메서드는 두 번째와 세 번째 인자로 날짜 포맷과 타임존도 받을 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 있지만 올바른 포맷이 아닌 경우 `InvalidArgumentException`이 발생할 수 있으므로, `date` 메서드 호출 전 입력값을 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum(열거형) 입력값 가져오기

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)과 일치하는 입력값도 요청에서 가져올 수 있습니다. 입력값이 없거나 일치하는 값이 없으면 `null`이 반환됩니다. `enum` 메서드에 입력값 이름과 enum 클래스를 인자로 넘깁니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

입력값이 enum 값 배열인 경우, `enums` 메서드를 통해 enum 인스턴스 배열로 받을 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티를 통한 입력값 접근

`Illuminate\Http\Request` 인스턴스에서 동적 프로퍼티로 사용자 입력에 접근할 수 있습니다. 예를 들어, 폼에 `name` 필드가 있으면 아래처럼 값을 가져올 수 있습니다.

```php
$name = $request->name;
```

동적 프로퍼티 사용 시, Laravel은 먼저 요청 페이로드(payload)에서 해당 값을 찾고, 없으면 매칭된 라우트의 파라미터에서 필드를 검색합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값의 일부만 가져오기

입력 데이터의 일부분만 필요하다면 `only`와 `except` 메서드를 사용할 수 있습니다. 이 메서드들은 배열 또는 동적 인자 목록을 받을 수 있습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에서 존재하는 키의 키/값 쌍만 반환합니다. 요청에 없는 키/값 쌍은 반환되지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 확인

`has` 메서드를 사용하면 요청에 특정 값이 존재하는지 알 수 있습니다. 해당 값이 존재하면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 넘기면 배열에 입력한 모든 값이 요청에 존재하는지 확인합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 지정된 값 중 하나라도 존재하면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 값이 존재하면 주어진 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 `whenHas`에 넘기면 값이 없을 때 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 있습니다...
}, function () {
    // "name" 값이 없습니다...
});
```

입력값이 요청에 존재하면서 빈 문자열이 아닌지도 확인할 수 있습니다. 이를 위해 `filled` 메서드를 사용합니다.

```php
if ($request->filled('name')) {
    // ...
}
```

반대로, 입력값이 없거나 빈 문자열일 때 확인하고 싶다면 `isNotFilled` 메서드를 사용하면 됩니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열로 전달할 수도 있습니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 지정한 값 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 값이 채워져 있을 때만 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘기면 값이 채워져 있지 않을 때 실행됩니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져 있음...
}, function () {
    // "name" 값이 비어 있거나 없음...
});
```

`missing`과 `whenMissing` 메서드를 통해 키가 존재하지 않는지도 확인할 수 있습니다.

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
### 추가 입력값 병합

기존 요청 입력값에 직접 추가값을 병합해야 할 때가 있습니다. 이럴 땐 `merge` 메서드를 사용하세요. 입력값 키가 이미 있으면 새 값으로 덮어씁니다.

```php
$request->merge(['votes' => 0]);
```

입력값이 이미 없을 때만 병합하려면 `mergeIfMissing` 메서드를 사용합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값

Laravel은 한 번의 요청에서 다음 요청까지 입력값을 유지할 수 있는 기능을 제공합니다. 이 기능은 검증 오류 후 폼 값을 다시 채워줄 때 매우 유용합니다. 단, Laravel 내장 [검증 기능](/docs/{{version}}/validation)을 사용하는 경우, 세션 입력 전송 메서드를 직접 사용할 필요가 없으며, Laravel 검증 시스템이 자동으로 호출해줍니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시 저장

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력값을 [세션](/docs/{{version}}/session)에 플래시 저장하여, 다음 요청에서 해당 입력값을 사용할 수 있게 합니다.

```php
$request->flash();
```

`flashOnly` 및 `flashExcept` 메서드를 사용해 민감한 정보(예: 비밀번호)를 세션에 남기지 않고 일부 값만 플래시 저장할 수도 있습니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트

주로 플래시 저장 후 이전 페이지로 리다이렉트하는 경우, `withInput` 메서드를 체이닝하여 사용할 수 있습니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 조회

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출합니다. 세션에서 이전 입력 데이터를 읽어옵니다.

```php
$username = $request->old('username');
```

Blade 템플릿 등에서 이전 입력값을 출력하려면 글로벌 `old` 헬퍼를 사용하는 것이 더 편리합니다. 필드에 해당하는 값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel에서 생성된 모든 쿠키는 암호화 및 인증코드로 서명되므로, 클라이언트가 쿠키를 수정하면 무효화됩니다. 쿠키 값을 얻으려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

기본적으로, Laravel 애플리케이션의 전역 미들웨어 스택에는 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이 미들웨어들은 요청의 모든 문자열 필드를 자동으로 트리밍하며(여백 제거), 빈 문자열은 `null`로 변환합니다. 이러한 정규화 작업 덕분에 라우트와 컨트롤러에서 별도로 신경 쓸 필요가 없습니다.

#### 입력값 정규화 비활성화

모든 요청에 대해 이 동작을 비활성화하려면 `bootstrap/app.php`에서 `$middleware->remove` 메서드를 사용해 두 미들웨어를 제거할 수 있습니다.

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

일부 요청에만 정규화 과정을 비활성화하려면 같은 파일에서 `trimStrings`와 `convertEmptyStringsToNull` 메서드에서 예외 조건을 클로저로 지정할 수 있습니다. 클로저는 `true` 또는 `false`를 반환해야 합니다.

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
## 파일

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기

`Illuminate\Http\Request` 인스턴스의 `file` 메서드 또는 동적 프로퍼티를 통해 업로드된 파일을 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 이는 PHP `SplFileInfo`를 확장하여 파일과 상호작용하는 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드는 특정 파일이 요청에 첨부되어 있는지 여부를 확인합니다.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증

파일이 있는지뿐 아니라 파일 업로드 과정에 문제가 없었는지도 `isValid` 메서드를 통해 확인할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스에는 파일의 전체 경로 또는 확장자를 얻는 메서드도 있습니다. `extension` 메서드는 파일 내용을 기반으로 확장자를 추측하며, 이는 클라이언트(브라우저)가 지정한 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에는 다양한 유용한 메서드가 있습니다. 자세한 내용은 [클래스 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장

업로드된 파일을 저장할 때는 보통 [파일시스템](/docs/{{version}}/filesystem)에 설정한 드라이브를 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 로컬 또는 Amazon S3 같은 클라우드 드라이브로 이동시켜 저장합니다.

`store` 메서드는 파일시스템 root 디렉터리 기준 저장 경로를 받으며, 파일명은 주지 않아도 자동으로 고유한 이름이 생성됩니다.

또한, 두 번째 인자로 디스크명을 지정할 수 있으며, 반환값은 해당 디스크 루트 기준 저장 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 직접 지정하려면 `storeAs` 메서드를 사용하세요. 경로, 파일명, 디스크명을 인자로 받습니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel의 파일 저장에 대한 자세한 정보는 [파일시스템 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

로드밸런서를 통해 TLS/SSL 인증서를 종료하는 환경에서 애플리케이션이 `url` 헬퍼 호출 시 HTTPS 링크를 생성하지 못하는 경우가 있습니다. 보통 애플리케이션이 로드밸런서로부터 포트 80(HTTP)으로 넘어온 트래픽이라 안전한 링크임을 알지 못하기 때문입니다.

이 문제를 해결하려면, Laravel 애플리케이션에 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화하여, 신뢰할 프록시나 로드밸런서를 빠르게 설정할 수 있습니다. 신뢰할 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드로 지정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 프록시 외에 신뢰할 프록시 헤더도 설정할 수 있습니다.

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
> AWS Elastic Load Balancing을 사용하는 경우, `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB` 여야 합니다. 로드밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 표준 `Forwarded` 헤더를 사용할 경우에는 `Request::HEADER_FORWARDED`를 사용해야 합니다. `headers`에 사용할 수 있는 상수에 대한 자세한 설명은 [Symfony 공식 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

Amazon AWS 등 "클라우드" 로드밸런서를 사용할 경우, 모든 프록시 IP를 알지 못할 수 있습니다. 이때는 `*`를 지정해 모든 프록시를 신뢰할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

기본적으로, Laravel은 HTTP 요청의 `Host` 헤더 값과 상관없이 모든 요청에 응답합니다. 또한, 기본적으로 절대 URL 생성 시에도 `Host` 헤더 값을 사용합니다.

보통 웹서버(Nginx, Apache)에 특정 호스트명만 Laravel로 전달하도록 구성해야 하지만, 직접 웹서버 설정을 바꿀 수 없는 경우 Laravel 레벨에서 응답할 호스트명을 제한할 수 있습니다. 이때 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다.

`TrustHosts` 미들웨어는 `bootstrap/app.php`에서 `trustHosts` 메서드로 활성화하며, `at` 인자로 응답하게 할 호스트명을 배열로 전달하면 해당 호스트 이외 요청은 모두 차단됩니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 애플리케이션의 URL 서브도메인 도착 요청도 자동으로 신뢰합니다. 이 기능을 끄려면 `subdomains` 인자를 사용합니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

신뢰할 호스트명을 설정할 때 설정파일이나 데이터베이스를 참조해야 한다면, `at` 인자로 클로저를 넘겨 동적으로 값을 반환할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
