# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청 다루기](#interacting-with-the-request)
    - [요청 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값(Input)](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 존재 확인](#input-presence)
    - [추가 입력값 병합](#merging-additional-input)
    - [이전 입력값(Old Input)](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 여러분의 애플리케이션에서 현재 처리 중인 HTTP 요청에 대해 객체 지향적으로 접근할 수 있는 방법을 제공합니다. 이 클래스를 이용하면 요청과 함께 전송된 입력값, 쿠키, 파일 등을 손쉽게 조회할 수 있습니다.

<a name="interacting-with-the-request"></a>
## 요청 다루기

<a name="accessing-the-request"></a>
### 요청 접근하기

현재 HTTP 요청 인스턴스를 의존성 주입 방식으로 받으려면, 라우트 클로저나 컨트롤러 메서드의 파라미터에 `Illuminate\Http\Request` 클래스를 타입힌트 하면 됩니다. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 요청 인스턴스를 주입해줍니다.

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

위에서 설명했듯이, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트 할 수 있습니다. 서비스 컨테이너가 클로저가 실행될 때 요청 인스턴스를 자동으로 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드가 라우트 파라미터도 함께 받을 경우, 다른 의존성 뒤에 라우트 파라미터를 나열해야 합니다. 예를 들어, 아래와 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

여전히 `Illuminate\Http\Request`를 타입힌트로 선언하면서, 아래와 같이 `id` 라우트 파라미터도 함께 받을 수 있습니다:

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
        // 사용자를 업데이트합니다...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 확인하기 위한 다양한 메서드를 제공합니다. 또한 이 클래스는 `Symfony\Component\HttpFoundation\Request`를 확장하고 있습니다. 아래에서는 자주 사용되는 주요 메서드들을 소개합니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로(Path) 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 들어오는 요청의 URL이 `http://example.com/foo/bar` 라면, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로 / 라우트 확인하기

`is` 메서드는 들어오는 요청 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 이 메서드를 사용할 때는 `*` 문자를 와일드카드로 쓸 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면, [이름이 지정된 라우트](/docs/12.x/routing#named-routes)와 요청이 매칭되었는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url`은 쿼리 문자열을 제외한 순수 URL만 리턴하고, `fullUrl`은 쿼리 문자열까지 포함한 전체 URL을 반환합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 스트링 데이터를 추가하고 싶을 때는 `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 현재 쿼리 스트링과 주어진 배열의 값을 합쳐 새로운 URL을 생성합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 스트링 파라미터를 제외한 현재 URL을 구하고 싶다면 `fullUrlWithoutQuery`를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트(Host) 가져오기

`host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용해 요청의 "호스트" 정보를 가져올 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드(Method) 가져오기

`method` 메서드는 요청의 HTTP 메서드(예: GET, POST 등)를 반환합니다. 또한, `isMethod` 메서드를 사용하면 HTTP 메서드가 특정 값과 일치하는지 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

요청 헤더는 `header` 메서드를 이용해서 `Illuminate\Http\Request` 인스턴스에서 조회할 수 있습니다. 만약 해당 헤더가 요청에 없다면, `null`이 반환됩니다. 두 번째 인자에 기본값을 지정하면, 헤더가 없을 때 그 값을 반환합니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 요청에 특정 헤더가 포함되어 있는지를 확인할 수 있습니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

또한, `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 bearer 토큰을 간편하게 가져올 수 있습니다. 만약 해당 헤더가 없다면 빈 문자열을 반환합니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

요청을 보낸 클라이언트의 IP 주소는 `ip` 메서드로 확인할 수 있습니다.

```php
$ipAddress = $request->ip();
```

프록시 등을 통해 전달된 모든 클라이언트 IP 주소 목록이 필요하다면 `ips` 메서드를 사용할 수 있습니다. 배열의 마지막 값이 실제(원본) 클라이언트의 IP가 됩니다.

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는 사용자가 조작 가능한 값이므로 정보용으로만 참고해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 요청의 `Accept` 헤더를 이용하여, 요청이 어떤 콘텐츠 타입을 원하는지 확인할 수 있는 다양한 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청이 허용하는 모든 콘텐츠 타입의 배열을 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 여러 콘텐츠 타입이 담긴 배열을 인자로 받아, 요청이 그 중 하나라도 허용하면 `true`, 아니면 `false`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 주어진 콘텐츠 타입 배열 중에서 요청이 가장 선호하는 타입을 반환합니다. 만약 어떤 타입도 허용되지 않으면 `null`을 반환합니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML 또는 JSON만 반환하는 경우가 많으므로, 들어오는 요청이 JSON 응답을 기대하는지 빠르게 판단할 때는 `expectsJson` 메서드를 사용할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청 및 응답)에 대한 인터페이스를 정의합니다. 라라벨의 기본 요청 객체 대신 PSR-7 요청 객체를 사용하고 싶다면, 몇 가지 라이브러리를 별도로 설치해야 합니다. 라라벨은 일반 라라벨 요청 및 응답을 PSR-7에 맞게 변환하기 위해 *Symfony HTTP Message Bridge* 컴포넌트를 사용합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

위 라이브러리를 설치한 후, 라우트 클로저나 컨트롤러 메서드에서 요청 인터페이스를 타입힌트하여 PSR-7 요청 객체를 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트 또는 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 이를 라라벨 응답 인스턴스로 변환하여 출력합니다.

<a name="input"></a>
## 입력값(Input)

<a name="retrieving-input"></a>
### 입력값 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 가져오기

들어오는 모든 요청 입력값을 `array`로 받고 싶다면 `all` 메서드를 사용할 수 있습니다. 이 메서드는 요청이 HTML 폼이든 XHR 요청이든 상관없이 동작합니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면, 모든 요청 입력값을 [컬렉션](/docs/12.x/collections)으로 받아올 수 있습니다.

```php
$input = $request->collect();
```

또한, `collect` 메서드는 일부 입력값만 골라 컬렉션으로 가져오는 것도 가능합니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 특정 입력값 하나 가져오기

요청의 HTTP 메서드(GET, POST 등)와 상관없이, `input` 메서드로 특정 입력값을 손쉽게 가져올 수 있습니다.

```php
$name = $request->input('name');
```

`input` 메서드의 두 번째 인자로 기본값을 지정할 수 있으며, 입력값이 없으면 지정한 기본값이 반환됩니다.

```php
$name = $request->input('name', 'Sally');
```

폼에 배열 타입 입력값이 포함되어 있다면 "점(.) 표기법"을 사용해 특정 값을 조회할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

아무 인자 없이 `input` 메서드를 호출하면 모든 입력값을 연관 배열로 받아올 수 있습니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 가져오기

`input` 메서드는 전체 요청 페이로드(쿼리 스트링 포함)에서 값을 가져오지만, `query` 메서드는 오직 쿼리 스트링에서만 값을 가져옵니다.

```php
$name = $request->query('name');
```

만약 요청에 해당 쿼리 스트링 값이 없다면 두 번째 인자에 지정한 값이 반환됩니다.

```php
$name = $request->query('name', 'Helen');
```

아무 인자 없이 `query` 메서드를 호출하면 모든 쿼리 스트링 값을 연관 배열로 받아올 수 있습니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

애플리케이션에 JSON 요청이 전송된 경우, 요청의 `Content-Type` 헤더가 올바르게 `application/json`으로 설정되어 있으면 `input` 메서드로 JSON 데이터에 접근할 수 있습니다. "점(.) 표기법"을 사용해 배열/객체 내부의 값도 조회할 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable(문자열 객체)로 입력값 가져오기

입력값을 단순 문자열로 받아오는 대신, `string` 메서드를 사용하면 [Illuminate\Support\Stringable](/docs/12.x/strings) 인스턴스로 받아올 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형(Integer) 입력값 가져오기

입력값을 정수형으로 받고 싶다면 `integer` 메서드를 사용할 수 있습니다. 이 메서드는 입력값을 정수로 캐스팅하려 시도하며, 값이 없거나 캐스팅이 실패하면 여러분이 지정한 기본값을 반환합니다. 페이지네이션 등 숫자 입력에 특히 유용합니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언(Boolean) 입력값 가져오기

HTML의 체크박스와 같이, "true"나 "on" 같은 문자열이 실제로는 참(truthy) 값을 의미하는 경우가 있습니다. 편리하게, `boolean` 메서드는 이 값을 불리언으로 변환해줍니다. 다음 값에 대해 `true`를 반환하고, 그 외에는 모두 `false`가 반환됩니다: 1, "1", true, "true", "on", "yes"

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### 배열(Array) 입력값 가져오기

배열 형태의 입력값을 받을 때는 `array` 메서드를 사용할 수 있습니다. 이 메서드는 항상 입력값을 배열로 변환해 줍니다. 입력값이 없다면 빈 배열을 반환합니다.

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### 날짜(Date) 입력값 가져오기

날짜/시간 입력값은 편리하게 `date` 메서드로 가져올 수 있으며, 이 값은 Carbon 인스턴스로 반환됩니다. 해당 이름의 입력값이 없으면 `null`이 반환됩니다.

```php
$birthday = $request->date('birthday');
```

`date` 메서드는 두 번째, 세 번째 인자로 날짜 포맷과 타임존을 각각 지정할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 있지만 형식이 잘못된 경우 `InvalidArgumentException`이 발생하므로, 이 메서드를 호출하기 전에 유효성 검증을 하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### 열거형(Enum) 입력값 가져오기

[PHP의 열거형(enum)](https://www.php.net/manual/en/language.types.enumerations.php) 값에 대응하는 입력값도 요청에서 받아올 수 있습니다. 요청에 해당 이름의 입력값이 없거나, enum의 값이 입력값과 일치하지 않으면 `null`이 반환됩니다. `enum` 메서드는 입력값의 이름과 enum 클래스명을 첫 번째, 두 번째 인자로 받습니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

기본값을 세 번째 인자로 지정해서, 값이 없거나 올바르지 않을 때 반환하도록 할 수도 있습니다.

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

입력값이 enum에 대응하는 값들의 배열이라면 `enums` 메서드로 열거형 인스턴스 배열을 받아올 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 접근하기

`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티를 통해서도 입력값에 접근할 수 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 다음과 같이 해당 값을 가져올 수 있습니다.

```php
$name = $request->name;
```

동적 프로퍼티를 사용할 때 라라벨은 먼저 요청 페이로드에서 값을 찾고, 없으면 매칭된 라우트의 파라미터에서 해당 값을 찾게 됩니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 일부 입력값만 골라 가져오기

입력값 중에서 일부만 뽑아야 할 경우, `only` 및 `except` 메서드를 사용할 수 있습니다. 두 메서드는 배열이나 가변 인자 리스트(여러 문자열)를 인자로 받습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 전달한 키들에 대해 입력값이 존재하는 key/value 쌍만 반환합니다. 요청에 없는 값은 반환하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 확인

요청에 값이 있는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 요청에 값이 있으면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열로 전달할 경우, `has` 메서드는 전달된 모든 값이 모두 존재하는지 확인합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 전달된 값 중 하나라도 존재하면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 요청에 값이 있으면 지정한 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

`whenHas` 메서드에 두 번째 클로저를 전달하면, 값이 없을 때 해당 클로저가 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재할 때...
}, function () {
    // "name" 값이 존재하지 않을 때...
});
```

입력값이 요청에 존재하고, 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용할 수 있습니다.

```php
if ($request->filled('name')) {
    // ...
}
```

요청에 값이 없거나, 빈 문자열인 경우를 확인하고자 하면 `isNotFilled` 메서드를 사용할 수 있습니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

`isNotFilled` 메서드에 배열로 여러 값을 넘기면, 모두 값이 없거나 빈 문자열인지 확인합니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 전달한 값 중 하나라도 빈 문자열이 아니라면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 값이 존재하고 빈 문자열이 아닐 때 지정한 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 함께 넘기면, 값이 "채워지지(filled)" 않았을 때 그 클로저가 실행됩니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 입력된 경우...
}, function () {
    // "name" 값이 입력되지 않은 경우...
});
```

특정 키가 요청에 존재하지 않는지 확인하고자 할 때는 `missing`, `whenMissing` 메서드를 사용할 수 있습니다.

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // "name" 값이 없는 경우...
}, function () {
    // "name" 값이 있는 경우...
});
```

<a name="merging-additional-input"></a>

### 추가 입력 병합하기

가끔은 기존 요청 입력 데이터에 추가 입력을 수동으로 병합해야 할 때가 있습니다. 이를 위해 `merge` 메서드를 사용할 수 있습니다. 만약 지정된 입력 키가 요청에 이미 존재한다면, `merge` 메서드에 전달한 데이터로 해당 키의 값이 덮어써집니다.

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 요청 입력 데이터에 해당 키가 아직 존재하지 않을 때에만 입력 데이터를 병합합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력 값 다루기

라라벨에서는 한 번의 요청에서 받은 입력을 다음 요청으로 전달하여 보관할 수 있습니다. 이 기능은 폼 유효성 검증 에러 발생 시 기존 입력값을 다시 채워 넣는 데 특히 유용합니다. 다만, 라라벨에서 제공하는 [유효성 검증 기능](/docs/12.x/validation)을 사용할 경우, 일부 내장된 유효성 검증 기능에서 세션 입력 플래싱 메서드를 자동으로 호출하므로 직접 해당 메서드를 사용하지 않아도 될 수 있습니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값 세션에 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력값을 [세션](/docs/12.x/session)에 플래시하여 사용자가 다음 요청 시에도 해당 입력값을 사용할 수 있게 합니다.

```php
$request->flash();
```

`flashOnly` 및 `flashExcept` 메서드를 사용하면 요청 데이터 중 일부만 세션에 플래시할 수 있습니다. 이 방법은 비밀번호와 같이 민감한 정보가 세션에 저장되는 것을 막는 데 유용합니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력 플래시 후 리디렉션

입력을 세션에 플래시한 뒤 이전 페이지로 리디렉션하는 경우가 많기 때문에, `withInput` 메서드를 사용하여 리디렉션에 입력 플래시를 간편하게 체이닝할 수 있습니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

이전 요청에서 플래시된 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 됩니다. 이 메서드는 [세션](/docs/12.x/session)에 저장된 이전 입력 데이터를 반환합니다.

```php
$username = $request->old('username');
```

라라벨은 전역 `old` 헬퍼 함수도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값을 폼에 재입력하는 경우, `old` 헬퍼를 사용하는 것이 더 편리합니다. 만약 해당 입력값이 존재하지 않으면 `null`이 반환됩니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

라라벨 프레임워크에서 생성된 모든 쿠키는 암호화되어 있고 인증 코드로 서명되어 있습니다. 따라서 클라이언트 측에서 쿠키가 변경되면 유효하지 않은 것으로 처리됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하면 됩니다.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력 트리밍 및 정규화

기본적으로 라라벨은 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 애플리케이션의 글로벌 미들웨어 스택에 포함시킵니다. 이 미들웨어들은 요청에 들어온 모든 문자열 필드를 자동으로 양쪽 공백을 제거(trim)해주고, 빈 문자열 필드는 자동으로 `null`로 변환합니다. 이렇게 하면 라우트와 컨트롤러에서 입력 정규화 처리를 따로 신경 쓰지 않아도 됩니다.

#### 입력 정규화 비활성화

이 동작을 모든 요청에서 비활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 사용하여 이 두 미들웨어를 미들웨어 스택에서 제거할 수 있습니다.

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

애플리케이션의 일부 요청에 대해서만 문자열 트리밍과 빈 문자열 변환 기능을 비활성화하고 싶다면, `bootstrap/app.php` 파일에서 `trimStrings` 및 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 두 메서드 모두 true/false를 반환하는 클로저 배열을 인자로 받으며, 해당 요청에 대해 입력 정규화 동작을 건너뛸지 여부를 결정합니다.

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

`Illuminate\Http\Request` 인스턴스에서는 `file` 메서드 또는 동적 프로퍼티를 통해 업로드된 파일을 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환하며, 이 클래스는 PHP의 `SplFileInfo`를 상속받아 파일을 다루기 위한 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드를 사용하면 요청에 파일이 존재하는지 확인할 수 있습니다.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증

파일의 존재 여부 뿐만 아니라, 파일 업로드 과정에서 문제가 없었는지도 `isValid` 메서드를 통해 검증할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로와 확장자

`UploadedFile` 클래스는 파일의 전체 경로나 확장자를 확인할 수 있는 메서드도 제공합니다. `extension` 메서드는 파일의 실제 내용을 기반으로 확장자를 추측하며, 이 확장자는 클라이언트에서 전송한 확장자와 다를 수도 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 그 외 파일 관련 메서드

`UploadedFile` 인스턴스에는 이 외에도 다양한 메서드들이 있습니다. 해당 클래스의 [API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)에서 자세한 내용을 확인할 수 있습니다.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일은 보통 설정해둔 [파일 시스템](/docs/12.x/filesystem)을 통해 저장합니다. `UploadedFile` 클래스의 `store` 메서드를 사용하면, 업로드된 파일을 로컬 파일 시스템 또는 Amazon S3와 같은 클라우드 스토리지 위치 등 다양한 디스크로 이동시킬 수 있습니다.

`store` 메서드의 첫 번째 인자는 파일이 저장될 경로(파일 시스템의 root 디렉토리 기준 상대 경로)입니다. 이 경로에는 파일 이름을 포함시키지 않아야 하며, 고유한 ID 기반의 파일명이 자동으로 생성되어 사용됩니다.

두 번째 인자로 파일을 저장할 디스크의 이름을 지정할 수도 있습니다. 반환값은 디스크 root 기준 저장 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 직접 지정하고 싶다면, `storeAs` 메서드를 사용하세요. 인자는 경로, 파일명, 디스크명 순서대로 전달합니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> 라라벨의 파일 저장에 대한 더 자세한 정보는 [파일 스토리지 문서](/docs/12.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼를 사용해도 HTTPS 링크가 생성되지 않는 현상이 발생할 수 있습니다. 이는 로드 밸런서가 포트 80으로 트래픽을 전달하기 때문에, 애플리케이션이 보안 연결임을 알지 못할 수 있기 때문입니다.

이 문제를 해결하려면, 라라벨에 기본 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화하고, 애플리케이션이 신뢰하는 로드 밸런서 또는 프록시를 지정하면 됩니다. 신뢰할 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드로 설정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

프록시를 지정하는 것 외에도, 애플리케이션에서 신뢰할 프록시 헤더도 설정할 수 있습니다.

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
> AWS Elastic Load Balancing을 사용하는 경우, `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`이어야 합니다. 로드 밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)에서 정의한 표준 `Forwarded` 헤더를 사용할 경우에는, `headers` 값을 `Request::HEADER_FORWARDED`로 설정해야 합니다. `headers` 값에 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [프록시 신뢰 관련 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS와 같은 "클라우드" 로드 밸런서 공급자를 사용한다면, 실제 밸런서의 IP 주소를 알 수 없는 경우가 많습니다. 이 경우에는 `*`를 사용해 모든 프록시를 신뢰할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

기본적으로 라라벨은 HTTP 요청의 `Host` 헤더 값과 관계없이 모든 요청에 응답하며, 웹 요청의 경우 애플리케이션의 절대 URL을 생성할 때도 `Host` 헤더 값을 사용합니다.

일반적으로 Nginx나 Apache와 같은 웹 서버에서 특정 호스트명과 일치하는 요청만 애플리케이션에 전달하도록 설정해야 합니다. 그러나 웹 서버를 직접 설정할 수 없는 상황에서, 라라벨 자체에서 특정 호스트에만 응답하도록 하려면 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다.

`TrustHosts` 미들웨어를 활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 호출하세요. `at` 인자를 사용해 애플리케이션이 응답할 호스트명을 지정할 수 있습니다. 지정한 호스트 이외의 요청(다른 `Host` 헤더 값)은 모두 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 애플리케이션의 URL 하위 도메인에서 오는 요청도 자동으로 신뢰합니다. 이 동작을 비활성화하려면 `subdomains` 인자를 사용하세요.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

애플리케이션의 설정 파일이나 데이터베이스에서 신뢰할 호스트 목록을 동적으로 가져와야 하는 경우, `at` 인자에 클로저를 전달할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```