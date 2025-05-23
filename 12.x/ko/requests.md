# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청 객체와 상호작용하기](#interacting-with-the-request)
    - [요청 객체 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드 확인](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값(Input)](#input)
    - [입력값 조회하기](#retrieving-input)
    - [입력값 존재 여부 확인](#input-presence)
    - [추가 입력값 병합](#merging-additional-input)
    - [이전 입력값(Old Input)](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 조회](#retrieving-uploaded-files)
    - [업로드 파일 저장](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

라라벨의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청 정보를 객체 지향적으로 다룰 수 있도록 해주며, 요청과 함께 전달된 입력값, 쿠키, 파일 등을 손쉽게 조회할 수 있습니다.

<a name="interacting-with-the-request"></a>
## 요청 객체와 상호작용하기

<a name="accessing-the-request"></a>
### 요청 객체 접근하기

의존성 주입(Dependency Injection)을 통해 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트 하면 됩니다. 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 요청 인스턴스를 주입해줍니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 사용자를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 사용자 저장 처리...

        return redirect('/users');
    }
}
```

위에서 설명했듯이, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트할 수 있습니다. 서비스 컨테이너가 해당 클로저를 실행할 때 자동으로 요청 인스턴스를 전달합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드에서 라우트 파라미터를 함께 받을 때는, 라우트 파라미터를 다른 의존성 뒤에 나열해야 합니다. 예를 들어 다음과 같이 라우트를 정의했다고 가정해봅시다.

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

이처럼 정의된 라우트에 대해, 컨트롤러 메서드에 `Illuminate\Http\Request`를 타입힌트하고, 두 번째 파라미터로 라우트 파라미터 `id`를 받을 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 사용자를 수정합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 수정 처리...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드 확인

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사할 수 있는 다양한 메서드를 제공합니다. 이 클래스는 `Symfony\Component\HttpFoundation\Request`를 확장하여, 여러 유용한 메서드를 쓸 수 있습니다. 그중 대표적인 메서드들을 아래에서 설명합니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로(path) 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 들어오는 요청 URL이 `http://example.com/foo/bar`인 경우, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 패턴 확인

`is` 메서드를 사용하면, 들어온 요청의 경로가 지정한 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

또한, `routeIs` 메서드를 사용하면, 요청이 [이름을 가진 라우트](/docs/12.x/routing#named-routes)와 일치하는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

들어온 요청의 전체 URL을 얻으려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 스트링이 없는 URL을, `fullUrl`은 쿼리 스트링까지 포함한 전체 URL을 반환합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 스트링 데이터를 더해서 얻고 싶다면, `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 전달한 배열을 기존 쿼리 스트링과 합쳐 반환합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 파라미터를 제외한 현재 URL이 필요하다면 `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기

들어온 요청의 "호스트" 정보를 확인하려면 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용할 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드(HTTP verb) 가져오기

`method` 메서드는 요청의 HTTP 메서드(verb)를 반환합니다. `isMethod` 메서드를 사용하면 HTTP 메서드가 특정 문자열과 일치하는지도 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스의 `header` 메서드를 이용해 요청의 헤더 정보를 조회할 수 있습니다. 지정한 헤더가 없을 경우 `null`을 반환하며, 두 번째 인수로 기본값을 전달할 수 있습니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

지정한 헤더가 요청에 포함되어 있는지 확인하려면 `hasHeader` 메서드를 사용할 수 있습니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의상, `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 bearer 토큰을 쉽게 얻을 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

요청을 보낸 클라이언트의 IP 주소를 얻으려면 `ip` 메서드를 사용합니다.

```php
$ipAddress = $request->ip();
```

프록시를 거친 모든 클라이언트 IP 주소 배열이 필요한 경우, `ips` 메서드를 사용할 수 있습니다. 가장 마지막 요소가 "원래" 클라이언트 IP입니다.

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는, 사용자가 임의로 조작할 수 있는 값이므로 정보 표시 용도로만 활용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상(Content Negotiation)

라라벨은 들어오는 요청의 `Accept` 헤더를 통해 클라이언트가 어떤 콘텐츠 타입을 원하는지 확인할 수 있는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청에서 허용하는 모든 콘텐츠 타입을 배열로 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 전달한 콘텐츠 타입 배열 중 하나라도 요청에서 허용된다면 `true`를 반환합니다. 그렇지 않으면 `false`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

여러 콘텐츠 타입 중에서 어떤 타입이 가장 우선순위가 높은지 확인하려면 `prefers` 메서드를 사용할 수 있습니다. 요청에서 받아들이는 타입 중 해당 배열에서 가장 선호하는 타입을 반환하며, 없으면 `null`을 반환합니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

대부분의 애플리케이션이 HTML 또는 JSON만 제공한다면, `expectsJson` 메서드로 클라이언트가 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청 및 응답)에 대한 인터페이스를 정의합니다. 라라벨 요청 대신 PSR-7 요청 인스턴스를 사용하고 싶다면 몇 가지 라이브러리를 설치해야 합니다. 라라벨은 *Symfony HTTP Message Bridge* 컴포넌트를 활용해 라라벨의 일반적인 요청과 응답 객체를 PSR-7 규격에 맞는 형태로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리들을 설치하면, 라우트 클로저나 컨트롤러 메서드에서 PSR-7 요청 인터페이스를 타입힌트하여 요청 객체를 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 라라벨이 이를 자동으로 다시 라라벨 응답 객체로 변환하여 출력합니다.

<a name="input"></a>
## 입력값(Input)

<a name="retrieving-input"></a>
### 입력값 조회하기

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기

들어온 요청의 모든 입력값을 배열 형태로 조회하려면 `all` 메서드를 사용하면 됩니다. 이 메서드는 HTML 폼이든 XHR 요청이든 관계없이 사용할 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면, 모든 입력값을 [컬렉션](/docs/12.x/collections) 객체로 얻을 수도 있습니다.

```php
$input = $request->collect();
```

또한, `collect` 메서드로 일부 입력값만 컬렉션으로 가져올 수도 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 단일 입력값 가져오기

간단한 메서드들을 활용해, `Illuminate\Http\Request` 인스턴스에서 HTTP 메서드와 관계없이 사용자가 보낸 모든 입력값을 조회할 수 있습니다. `input` 메서드는 전송 방식과 관계없이 입력값을 가져올 수 있습니다.

```php
$name = $request->input('name');
```

입력값이 없을 경우 반환할 기본값을 두 번째 인수로 전달할 수 있습니다.

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력이 있는 폼에서는 "dot" 표기법을 사용해 배열 값을 접근할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

`input` 메서드를 인수 없이 호출하면 모든 입력값을 연관 배열로 한번에 조회할 수 있습니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링 입력값 가져오기

`input` 메서드는 전체 요청 페이로드(쿼리 스트링 포함)에서 값을 조회하지만, 오직 쿼리 스트링에서만 입력값을 조회하고 싶다면 `query` 메서드를 사용합니다.

```php
$name = $request->query('name');
```

쿼리 스트링에 값이 없을 경우 기본값을 두 번째 인수로 전달할 수 있습니다.

```php
$name = $request->query('name', 'Helen');
```

`query` 메서드를 인수 없이 호출하면 쿼리 스트링의 모든 값을 연관 배열로 조회할 수 있습니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있으면 `input` 메서드로 JSON 데이터를 접근할 수 있습니다. "dot" 표기법을 통해 중첩된 JSON 배열/객체 값도 손쉽게 가져올 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 가져오기

입력값을 일반 문자열이 아니라 [Illuminate\Support\Stringable](/docs/12.x/strings) 객체로 받아 다양한 문자열 메서드를 체이닝할 수도 있습니다. 이럴 때는 `string` 메서드를 사용합니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 가져오기

정수로 변환된 입력값이 필요하다면, `integer` 메서드를 사용할 수 있습니다. 이 메서드는 입력값을 정수로 캐스팅하고, 값이 없거나 변환에 실패하면 지정한 기본값을 반환합니다. 페이지네이션 등에서 유용하게 활용할 수 있습니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불린(boolean) 입력값 가져오기

체크박스와 같은 HTML 요소를 다루다 보면 "true"나 "on"처럼 문자열로 표현된 "truthy" 값들이 전달될 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes" 값은 모두 `true`로 변환하며, 그 외에는 `false`를 반환합니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜나 시간을 포함하는 입력값의 경우, `date` 메서드를 통해 [Carbon 인스턴스]로 변환해서 받을 수 있습니다. 해당 이름의 입력값이 없으면 `null`이 반환됩니다.

```php
$birthday = $request->date('birthday');
```

`date` 메서드는 두 번째, 세 번째 인수로 각각 날짜 포맷과 타임존을 지정할 수도 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값은 있지만 포맷이 올바르지 않은 경우 `InvalidArgumentException`이 발생하니, `date` 메서드 사용 전 입력값을 반드시 유효성 검사 하시기 바랍니다.

<a name="retrieving-enum-input-values"></a>
#### 열거형(enum) 입력값 가져오기

입력값으로 [PHP 열거형(enum)](https://www.php.net/manual/en/language.types.enumerations.php) 타입이 전달될 수도 있습니다. 해당 이름의 입력값이 없거나, enum에서 입력값에 일치하는 value가 없으면 `null`을 반환합니다. `enum` 메서드는 입력값 이름과 Enum 클래스명을 첫 번째/두 번째 인수로 받습니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

입력값이 누락 또는 잘못된 경우 기본값을 반환하도록 세 번째 인수로 기본값을 지정할 수도 있습니다.

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

입력값이 PHP enum 형태의 값 배열인 경우, `enums` 메서드를 통해 Enum 인스턴스의 배열을 받을 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 가져오기

`Illuminate\Http\Request` 인스턴스에서는 동적 프로퍼티 방식으로 입력값에 접근할 수도 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 아래와 같이 해당 값을 조회할 수 있습니다.

```php
$name = $request->name;
```

동적 프로퍼티를 사용할 때, 라라벨은 먼저 요청 페이로드에서 해당 값을 찾고, 없으면 라우트 파라미터에서 찾게 됩니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 일부 입력값만 가져오기

입력 데이터 중 일부만 조회하고 싶다면, `only`와 `except` 메서드를 사용할 수 있습니다. 두 메서드는 모두 배열이나 가변 인자 형태로 사용 가능합니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 존재하는 키/값 쌍만 반환하며, 요청에 없는 키는 반환하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 여부 확인

요청에 특정 값이 있는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 해당 값이 존재하면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 전달하면 모든 값이 존재하는지 검사합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 지정한 값들 중 하나라도 있으면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 값이 존재할 때만 지정한 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

`whenHas` 메서드에 두 번째 클로저를 전달하면, 지정한 값이 존재하지 않을 때 해당 클로저가 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 있음...
}, function () {
    // "name" 값이 없음...
});
```

요청에 값이 존재하면서 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용합니다.

```php
if ($request->filled('name')) {
    // ...
}
```

요청에 값이 없거나 빈 문자열인 경우를 확인하려면 `isNotFilled` 메서드를 사용할 수 있습니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 전달하면 모든 값이 없거나 비었는지 검사합니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 지정한 값들 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 요청에 값이 존재하고 비어있지 않을 때만 지정한 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

`whenFilled`에 두 번째 클로저를 전달하면, 값이 "filled" 상태가 아닐 때 두 번째 클로저가 실행됩니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져 있음...
}, function () {
    // "name" 값이 비어 있거나 없음...
});
```

요청에서 특정 키가 아예 없는지 확인하려면, `missing` 및 `whenMissing` 메서드를 사용할 수 있습니다.

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

### 추가 입력 병합하기

때때로 요청(Request)의 기존 입력 데이터에 추가 입력을 수동으로 병합해야 할 때가 있습니다. 이때는 `merge` 메서드를 사용할 수 있습니다. 만약 지정한 입력 키가 이미 요청에 존재한다면, `merge` 메서드에 전달된 데이터로 덮어쓰게 됩니다.

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 요청에 해당 키가 아직 존재하지 않을 때만 입력 데이터를 병합합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값(Old Input)

라라벨에서는 한 번의 요청에서 입력받은 데이터를 다음 요청까지 유지할 수 있습니다. 이 기능은 유효성 검증에서 오류가 발생했을 때, 폼을 다시 채워 넣는 데 특히 유용합니다. 하지만 라라벨의 [유효성 검증 기능](/docs/12.x/validation)을 사용하고 있다면, 이러한 세션 입력 플래싱 메서드를 직접 호출하지 않아도 됩니다. 라라벨의 내장 유효성 검증 기능 중 일부가 자동으로 이 과정을 처리해주기 때문입니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드를 사용하면 현재 입력값을 [세션](/docs/12.x/session)에 저장하여, 다음 요청 시 다시 사용할 수 있습니다.

```php
$request->flash();
```

`flashOnly` 및 `flashExcept` 메서드를 사용하면 요청 데이터 중 일부만을 세션에 플래시할 수 있습니다. 이 메서드는 비밀번호와 같이 민감한 정보가 세션에 저장되지 않도록 할 때 유용하게 활용할 수 있습니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트하기

입력값을 세션에 플래시한 후, 바로 이전 페이지로 리다이렉트하는 경우가 많습니다. 이때는 `withInput` 메서드를 사용해 플래시와 리다이렉트를 쉽게 체이닝할 수 있습니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

플래시된 입력값을 지난 요청에서 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. `old` 메서드는 [세션](/docs/12.x/session)에 저장된 입력값을 반환합니다.

```php
$username = $request->old('username');
```

라라벨에서는 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 이전 입력값을 폼에 채워 넣을 때 이 헬퍼를 사용하면 더 편리합니다. 지정한 필드의 이전 입력값이 없다면 `null`이 반환됩니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

라라벨에서 만들어진 모든 쿠키는 암호화 및 인증 코드로 서명되어 있기 때문에, 클라이언트에서 변경했다면 무효로 처리됩니다. 요청에서 쿠키 값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하면 됩니다.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

라라벨은 기본적으로 애플리케이션의 글로벌 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings` 및 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 두 미들웨어는 요청에서 받은 모든 문자열 필드의 앞뒤 공백을 자동으로 제거하고, 빈 문자열 필드를 `null` 값으로 변환합니다. 덕분에 라우트나 컨트롤러에서 이러한 정규화 처리를 신경 쓸 필요가 없습니다.

#### 입력값 정규화 비활성화하기

이 동작을 모든 요청에 대해 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 호출하여 두 미들웨어를 미들웨어 스택에서 제거하면 됩니다.

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

입력값 트리밍과 빈 문자열 변환을 애플리케이션의 일부 요청에만 비활성화하고 싶다면, `bootstrap/app.php` 파일에서 `trimStrings` 및 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 두 메서드 모두 클로저의 배열을 인자로 받아, 각 클로저가 `true` 또는 `false`를 반환하여 해당 요청에서 정규화 처리를 건너뛸지 여부를 판단합니다.

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

`Illuminate\Http\Request` 인스턴스에서 업로드된 파일은 `file` 메서드나 동적 프로퍼티를 사용하여 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환하며, 이 클래스는 PHP의 `SplFileInfo`를 확장해 파일과 상호작용할 수 있는 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

요청에 특정 파일이 포함되어 있는지 확인하려면 `hasFile` 메서드를 사용하세요.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증

파일이 존재하는지 확인하는 것 외에도, `isValid` 메서드를 통해 파일 업로드에 문제가 없었는지도 검증할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스는 파일의 전체 경로 및 확장자에 접근할 수 있는 메서드도 제공합니다. `extension` 메서드는 파일의 실제 내용을 기반으로 확장자를 추측하는데, 이는 클라이언트가 보낸 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 그 외 파일 메서드

`UploadedFile` 인스턴스에서는 이 외에도 다양한 메서드를 제공합니다. 더 많은 메서드에 대한 정보는 [UploadedFile 클래스 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)에서 확인하실 수 있습니다.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일을 저장하려면, 보통 미리 설정해 둔 [파일 시스템](/docs/12.x/filesystem)을 사용하게 됩니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 로컬 파일 시스템 경로나 Amazon S3와 같은 클라우드 저장소에 이동시켜 저장합니다.

`store` 메서드는 파일을 저장할 경로(파일 시스템의 루트 디렉터리 기준 상대 경로)를 인자로 받습니다. 이 경로에는 파일명을 포함하지 않아야 하며, 파일명은 자동으로 고유 ID가 생성되어 할당됩니다.

또한 두 번째 인수로 파일을 저장할 디스크의 이름도 지정할 수 있습니다. 이 메서드는 파일이 저장된 경로(디스크 루트 기준 상대 경로)를 반환합니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 직접 지정하고 싶을 때는 `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 저장 경로, 파일명, 디스크명을 인수로 받습니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> 라라벨의 파일 저장에 관한 더 자세한 내용은 [파일 저장소 문서](/docs/12.x/filesystem) 전체를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서를 종료(terminate)하는 로드밸런서 뒤에서 애플리케이션을 실행하는 경우, `url` 헬퍼를 사용할 때 HTTPS 링크가 제대로 생성되지 않을 수 있습니다. 대부분 이런 문제는 로드밸런서가 80번 포트로 트래픽을 전달하고 있기 때문에, 애플리케이션이 안전한(secure) 링크를 생성해야 하는 상황임을 인지하지 못해서 발생합니다.

이 문제를 해결하려면, 라라벨에 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화하세요. 이 미들웨어를 사용하면 신뢰할 수 있는 로드밸런서나 프록시를 빠르게 커스터마이즈 할 수 있습니다. 신뢰할 수 있는 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용해 지정합니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 프록시뿐만 아니라, 신뢰할 프록시 헤더도 함께 설정할 수 있습니다.

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
> AWS Elastic Load Balancing을 사용하는 경우, `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`가 되어야 합니다. 만약 표준 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 `Forwarded` 헤더를 사용하는 로드밸런서라면, `headers` 값에 `Request::HEADER_FORWARDED`를 지정해야 합니다. `headers` 값으로 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [proxy 신뢰 설정 문서](https://symfony.com/doc/current/deployment/proxies.html)에서 확인 가능합니다.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS와 같은 클라우드 로드밸런서 제공자를 사용하는 경우, 실제 밸런서의 IP 주소를 알 수 없는 상황이 많습니다. 이때는 `*`를 사용하여 모든 프록시를 신뢰하도록 설정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

기본적으로 라라벨은 HTTP 요청의 `Host` 헤더 값에 상관없이, 수신되는 모든 요청에 응답합니다. 웹 요청 중에는 애플리케이션 절대 URL을 생성할 때도 `Host` 헤더의 값이 사용됩니다.

보통은 Nginx나 Apache와 같은 웹 서버에서, 특정 Hostname만을 애플리케이션에 전달하도록 직접 설정하는 것이 좋습니다. 그러나 웹 서버 설정을 직접 커스터마이즈할 수 없거나, 라라벨에서만 특정 호스트에 대해 응답하도록 제한하고 싶을 때는 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다.

`TrustHosts` 미들웨어를 활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 호출하세요. 이때 `at` 인자를 사용해 애플리케이션이 허용할 호스트명을 지정할 수 있습니다. 다른 `Host` 헤더값으로 들어온 요청은 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로는, 애플리케이션의 URL 하위 도메인에서 들어오는 요청도 자동으로 신뢰합니다. 이 동작을 비활성화하려면 `subdomains` 인자를 사용하세요.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

신뢰할 호스트 목록을 애플리케이션의 설정 파일이나 데이터베이스에서 동적으로 불러오고 싶다면, `at` 인자에 클로저를 전달하면 됩니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```