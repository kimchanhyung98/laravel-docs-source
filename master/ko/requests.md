# HTTP 요청

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력](#input)
    - [입력값 조회](#retrieving-input)
    - [입력 존재 여부](#input-presence)
    - [추가 입력 병합](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 조회](#retrieving-uploaded-files)
    - [업로드된 파일 저장](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청과 상호작용하고, 요청과 함께 전송된 입력값, 쿠키, 파일 정보를 객체 지향적으로 조회할 수 있도록 지원합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청 접근하기

현재 HTTP 요청의 인스턴스를 의존성 주입을 통해 얻고자 할 때, 라우트 클로저나 컨트롤러 메서드의 타입힌트로 `Illuminate\Http\Request` 클래스를 지정하세요. Laravel [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 해당 요청 인스턴스를 주입합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 유저 저장하기.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 유저 저장...

        return redirect('/users');
    }
}
```

위에서 언급한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request`를 타입힌트로 사용할 수 있습니다. 서비스 컨테이너가 클로저 실행 시점에 요청을 자동으로 주입합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입 및 라우트 파라미터

컨트롤러 메서드에서 라우트 파라미터의 입력값도 함께 받고 싶다면, 라우트 파라미터를 나머지 의존성 뒤에 작성하세요. 예를 들어, 다음과 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서 `Illuminate\Http\Request`를 타입힌트로 지정하면서 라우트 파라미터 `id`도 아래와 같이 받아올 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 유저 정보 수정.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 유저 수정...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드

`Illuminate\Http\Request` 인스턴스는 다양한 방식으로 HTTP 요청 정보를 조회하는 메서드를 제공합니다. 이 클래스는 `Symfony\Component\HttpFoundation\Request`를 확장합니다. 아래에서 대표적인 메서드들을 설명합니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 조회

`path` 메서드는 현재 요청의 경로 정보를 반환합니다. 예를 들어, 요청이 `http://example.com/foo/bar`로 들어왔다면, `path` 메서드는 `foo/bar`를 반환합니다:

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사

`is` 메서드는 요청 경로가 특정 패턴과 일치하는지 확인합니다. 이 때 `*` 문자를 와일드카드로 사용할 수 있습니다:

```php
if ($request->is('admin/*')) {
    // ...
}
```

또한, `routeIs` 메서드를 사용하면 요청이 [네임드 라우트](/docs/{{version}}/routing#named-routes)에 일치하는지 확인할 수 있습니다:

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 조회

요청의 전체 URL을 얻으려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url`은 쿼리스트링을 제외한 URL을, `fullUrl`은 쿼리스트링까지 포함하여 반환합니다:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리스트링 데이터(배열)를 추가하려면 `fullUrlWithQuery` 메서드를 사용합니다. 이 메서드는 전달한 배열의 쿼리 파라미터와 현재 쿼리스트링을 병합합니다:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 파라미터를 제외한 현재 URL을 얻고 싶다면 `fullUrlWithoutQuery` 메서드를 사용하세요:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 조회

요청의 "호스트"를 얻으려면 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용할 수 있습니다:

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 조회

`method` 메서드는 요청의 HTTP 메서드(POST, GET 등)를 반환합니다. `isMethod`로 HTTP 메서드가 특정 문자열과 일치하는지도 검사할 수 있습니다:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스의 `header` 메서드로 요청 헤더를 조회할 수 있습니다. 헤더가 없으면 `null`이 반환되며, 두 번째 인자로 기본값을 지정할 수 있습니다:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

지정한 헤더가 요청에 포함되어 있는지 확인하려면 `hasHeader` 메서드를 사용하세요:

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편리하게도, `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 bearer 토큰을 바로 읽어올 수 있습니다. 해당 헤더가 없으면 빈 문자열을 반환합니다:

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

요청을 보낸 클라이언트의 IP 주소를 얻으려면 `ip` 메서드를 사용하세요:

```php
$ipAddress = $request->ip();
```

프록시를 거쳐 온 모든 클라이언트의 IP 주소 배열을 가져오려면 `ips` 메서드를 사용할 수 있습니다. 이 배열에서 "원본" 클라이언트의 IP 주소는 배열의 마지막에 있습니다:

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는 사용자 제어 입력으로 간주하고, 참고 용도로만 사용하는 것이 좋습니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 요청의 `Accept` 헤더를 통해 요청자가 원하는 콘텐츠 타입을 확인할 수 있는 여러 메서드를 제공합니다. 먼저 `getAcceptableContentTypes` 메서드는 요청자가 받아들일 수 있는 모든 콘텐츠 타입의 배열을 반환합니다:

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 배열로 주어진 콘텐츠 타입 중 하나라도 요청에서 허용된다면 `true`를 반환합니다. 아니라면 `false`를 반환합니다:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드로 여러 콘텐츠 타입 중에서 요청자가 가장 선호하는 타입을 알아낼 수 있습니다. 제공한 타입 중 아무것도 요청에서 수용되지 않으면 `null`을 반환합니다:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

HTML이나 JSON만을 제공하는 애플리케이션의 경우, `expectsJson` 메서드로 요청이 JSON 응답을 기대하는지 빠르게 판단할 수 있습니다:

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청 및 응답 등 HTTP 메시지를 위한 인터페이스를 정의합니다. Laravel이 아닌 PSR-7 요청 인스턴스를 필요로 한다면 우선 관련 라이브러리를 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge*를 이용해 기본 요청/응답을 PSR-7 호환 구현체로 변환합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리 설치 후, 라우트 클로저 또는 컨트롤러에서 요청 인터페이스를 타입힌트로 지정하여 PSR-7 요청을 얻을 수 있습니다:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 다시 Laravel 응답 인스턴스로 변환해 표시합니다.

<a name="input"></a>
## 입력

<a name="retrieving-input"></a>
### 입력값 조회

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 조회

`all` 메서드를 사용해 요청으로 들어온 모든 입력값을 `array` 형태로 조회할 수 있습니다. HTML 폼이든 XHR 요청이든 관계없이 이용 가능합니다:

```php
$input = $request->all();
```

`collect` 메서드를 사용하면 [컬렉션](/docs/{{version}}/collections)으로 요청 입력값을 받습니다:

```php
$input = $request->collect();
```

특정 배열 입력만 컬렉션으로 받고 싶다면 아래와 같이 사용할 수 있습니다:

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 단일 입력값 조회

간단한 메서드 몇 개로 요청의 HTTP 메서드(POST, GET 등)에 관계없이 입력값을 얻을 수 있습니다. HTTP 메서드에 상관없이 `input` 메서드를 사용하면 입력값을 조회할 수 있습니다:

```php
$name = $request->input('name');
```

`input` 메서드의 두 번째 인자로 기본값을 지정할 수 있습니다. 입력값이 없을 경우 해당 값이 반환됩니다:

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값은 "도트" 표기법을 사용해 읽을 수 있습니다:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

아무 인자 없이 `input`을 호출하면, 모든 입력값을 연관 배열로 반환합니다:

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리스트링 입력값 조회

`input` 메서드는 요청 전체(포함: 쿼리스트링·폼데이터)에서 값을 읽는 반면, `query` 메서드는 쿼리스트링 값만 반환합니다:

```php
$name = $request->query('name');
```

해당 쿼리 파라미터가 없을 때는 두 번째 인자에 지정한 기본값이 반환됩니다:

```php
$name = $request->query('name', 'Helen');
```

인자 없이 `query`를 호출하면 쿼리스트링 전체를 연관 배열로 반환합니다:

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 조회

애플리케이션에 JSON 요청이 전송될 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 지정되어 있다면 `input` 메서드로 JSON 데이터 값을 조회할 수 있습니다. 중첩된 값도 "도트" 표기법으로 참조 가능합니다:

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 조회

기본 string 대신 [`Illuminate\Support\Stringable`](/docs/{{version}}/strings) 인스턴스를 얻고 싶다면 `string` 메서드를 사용할 수 있습니다:

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 조회

입력값을 정수로 변환하려면 `integer` 메서드를 사용하세요. 값이 없거나 변환에 실패하면 지정한 기본값을 반환합니다. 이 메서드는 페이지네이션 등 수치형 입력에 유용합니다:

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 조회

HTML 체크박스 등에서 문자열 "true"나 "on"과 같은 실제로는 문자열인 "참" 값을 받는 경우, `boolean` 메서드를 쓰면 `1`, "1", true, "true", "on", "yes" 등은 true로, 나머지는 false로 변환됩니다:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 조회

날짜/시간 값을 입력받을 때에는 `date` 메서드를 통해 입력값을 Carbon 인스턴스로 받을 수 있습니다. 값이 없으면 `null`이 반환됩니다:

```php
$birthday = $request->date('birthday');
```

두 번째, 세 번째 인자로 날짜 포맷과 타임존도 지정할 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 있지만 형식이 올바르지 않으면 `InvalidArgumentException`이 발생합니다. 따라서 `date` 메서드 사용 전에 입력값을 검증하는 것이 권장됩니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 조회

입력값이 [PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)에 해당할 경우, `enum` 메서드를 사용해 값이 일치하는 enum 인스턴스를 조회할 수 있습니다. 값이 없거나 일치하는 enum 값이 없으면 `null`을 반환합니다. 첫 인자는 입력명, 두 번째 인자는 enum 클래스입니다:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

입력값이 enum 배열인 경우 `enums` 메서드로 enum 인스턴스 배열을 받을 수 있습니다:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 조회

`Illuminate\Http\Request` 인스턴스에서 동적 프로퍼티로도 입력값을 조회할 수 있습니다. 예를 들어, form에 `name` 필드가 있다면 아래와 같이 접근하면 됩니다:

```php
$name = $request->name;
```

동적 프로퍼티 사용 시 Laravel은 먼저 요청 페이로드에서 값을 찾고, 없으면 매치된 라우트의 파라미터에서 값을 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값 일부만 추출

입력값 일부만 추출하려면 `only`, `except` 메서드를 사용할 수 있습니다. 인자는 배열 또는 가변 인자 모두 지원합니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 존재하는 키/값만 반환합니다. 요청에 없는 값은 무시됩니다.

<a name="input-presence"></a>
### 입력 존재 여부

`has` 메서드를 사용해 요청에서 값이 존재하는지 확인할 수 있습니다. 값이 있으면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    // ...
}
```

배열을 전달하면 모든 값이 존재하는지를 확인합니다:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 하나라도 존재하면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 값이 존재할 때 지정한 클로저를 실행합니다:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

값이 존재하지 않을 때 실행할 두 번째 클로저도 지정할 수 있습니다:

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 있음...
}, function () {
    // "name" 값이 없음...
});
```

값이 존재하며 빈 문자열이 아닐 때를 확인하려면 `filled` 메서드를 사용합니다:

```php
if ($request->filled('name')) {
    // ...
}
```

값이 존재하지 않거나 빈 문자열일 때는 `isNotFilled` 메서드를 사용합니다:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 전달하면 모든 값이 없거나 빈 경우만 `true`입니다:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled`는 하나라도 빈 문자열이 아닌 값이 있으면 `true`를 반환합니다:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 값이 비어있지 않으면 클로저를 실행합니다:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

채워지지 않은 값을 처리할 두 번째 클로저도 지정 가능:

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 입력됨...
}, function () {
    // "name" 값이 비어있음...
});
```

지정한 키가 요청에 없는지 확인하려면 `missing`, `whenMissing`을 사용하세요:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // "name" 값이 없음...
}, function () {
    // "name" 값이 존재함...
});
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합

기존 요청 입력값에 추가 입력 데이터를 수동으로 병합하고 싶을 땐 `merge` 메서드를 사용하세요. 이미 해당 입력값이 존재하면 덮어씁니다:

```php
$request->merge(['votes' => 0]);
```

입력값이 아직 존재하지 않을 때만 병합하고 싶다면 `mergeIfMissing` 메서드를 사용하세요:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값

Laravel은 한 번의 요청에서 입력값을 다음 요청까지 유지할 수 있습니다. 이 기능은 주로 폼 유효성 검사 실패 후 폼에 값을 다시 채우는 데 쓰입니다. 하지만, Laravel의 [유효성 검사 기능](/docs/{{version}}/validation)을 사용하는 경우에는 별도로 세션 입력값 플래시 메서드를 직접 호출할 필요가 없습니다. 내장된 유효성 검사 기능이 자동 호출합니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력값을 [세션](/docs/{{version}}/session)에 플래시(임시 저장)합니다. 다음 요청에서 해당 값을 사용할 수 있습니다:

```php
$request->flash();
```

요청 입력값의 일부만 세션에 저장하고 싶을 때 `flashOnly`, `flashExcept`를 사용하세요. 비밀번호 등 민감정보를 세션에 남기지 않을 때 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력 플래시 후 리디렉션

입력값을 세션에 플래시한 뒤 이전 페이지로 리디렉트하는 경우가 많은데, 이 때는 `withInput` 메서드를 사용해 쉽게 연결할 수 있습니다:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

이전 요청에서 플래시된 입력을 조회하려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하세요. 이 메서드는 [세션](/docs/{{version}}/session)에서 플래시된 입력값을 불러옵니다:

```php
$username = $request->old('username');
```

Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/{{version}}/blade)에서 이전 입력값으로 폼을 자동 채우고자 할 때 더 편리합니다. 값이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키값 조회

Laravel이 생성한 모든 쿠키는 암호화되어 서명도 추가됩니다. 따라서 클라이언트가 쿠키를 변경하면 무효 처리됩니다. 쿠키 값을 조회하려면, `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

Laravel은 기본적으로 애플리케이션의 글로벌 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이 미들웨어들은 요청에 들어오는 모든 문자열 필드를 자동으로 trim하고, 빈 문자열을 `null`로 변환합니다. 이렇게 하면 라우트나 컨트롤러에서 이런 정규화를 신경 쓸 필요가 없습니다.

#### 입력 정규화 비활성화

모든 요청에서 이 동작을 비활성화하려면, 애플리케이션의 `bootstrap/app.php`에서 `$middleware->remove`로 두 미들웨어를 제거하세요:

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

일부 요청에서만 문자열 트리밍/빈문자열 변환을 비활성화하고 싶으면, `trimStrings` 및 `convertEmptyStringsToNull` 메서드를 사용해주세요. 각각의 메서드는 true/false를 반환하는 클로저 배열을 인자로 받으며, `true`이면 정규화 건너뜁니다:

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
### 업로드된 파일 조회

업로드된 파일을 조회하려면 `Illuminate\Http\Request` 인스턴스의 `file` 메서드 또는 동적 프로퍼티를 사용하세요. `file` 메서드는 PHP의 `SplFileInfo`를 확장한 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 파일 조작을 위한 다양한 메서드를 갖고 있습니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```

요청에 파일이 포함되어 있는지 확인하려면 `hasFile` 메서드를 사용하세요:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 검증

파일이 요청에 존재하는지 뿐만 아니라, 업로드 과정에 문제가 없었는지도 `isValid` 메서드로 검사할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로와 확장자

`UploadedFile` 클래스에는 파일의 전체 경로와 확장자를 조회하는 메서드도 있습니다. `extension`은 파일 내용을 바탕으로 확장자를 추정합니다. 실제 클라이언트가 올린 파일 확장자와 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에는 다양한 추가 메서드가 있습니다. 자세한 내용은 [클래스 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드 파일 저장

업로드한 파일을 저장할 때는 구성한 [파일시스템](/docs/{{version}}/filesystem) 중 하나를 사용합니다. `UploadedFile`의 `store` 메서드는 업로드 파일을 디스크(로컬, Amazon S3 등)에 옮깁니다.

`store` 메서드의 첫 인자는 파일이 저장될 경로(파일명 제외, 루트 기준), 두 번째 인자는 사용할 디스크 이름입니다. 반환값은 디스크 루트 기준 저장 경로입니다:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 직접 지정하려면 `storeAs` 메서드를 사용합니다. 첫 인자는 경로, 두 번째는 파일명, 세 번째는 디스크 이름입니다:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> 파일 저장에 관한 자세한 내용은 [파일 시스템 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서를 종료하는 로드밸런서 뒤에 애플리케이션을 배포할 때, `url` 헬퍼로 생성된 링크가 HTTPS가 아닌 경우가 있습니다. 이는 대부분 80번 포트로 트래픽이 전달되어 애플리케이션이 보안 연결임을 알지 못할 때 발생합니다.

이 문제는 Laravel 기본 미들웨어인 `Illuminate\Http\Middleware\TrustProxies`를 활성화하여 해결할 수 있습니다. 이 미들웨어로 신뢰할 프록시(또는 로드밸런서)를 지정합니다. 애플리케이션의 `bootstrap/app.php`에서 `trustProxies` 미들웨어 메서드를 사용해 신뢰할 프록시 IP나 대역을 지정하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 프록시 설정 외에도, 신뢰할 프록시 헤더를 지정할 수 있습니다:

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
> AWS Elastic Load Balancing을 사용한다면 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`이어야 합니다. 로드밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 표준 `Forwarded` 헤더를 사용한다면 값은 `Request::HEADER_FORWARDED`입니다. 사용 가능한 상수 목록 등 자세한 내용은 Symfony [proxy 신뢰 문서](https://symfony.com/doc/7.0/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

Amazon AWS나 기타 클라우드 로드밸런서를 쓴다면 실제 밸런서의 IP를 알 수 없는 경우가 많습니다. 이런 경우 `*`를 사용해 전체 프록시를 신뢰할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

Laravel은 기본적으로 어떤 HTTP 요청의 `Host` 헤더와 상관없이 모든 요청을 처리합니다. 또한 웹 요청 중 절대 URL을 생성할 때 `Host` 헤더 값을 사용합니다.

일반적으로는 Nginx, Apache 등 웹서버에서 특정 호스트 요청만 애플리케이션에 전달하도록 설정하는 것이 좋습니다. 그러나 웹서버를 직접 수정할 수 없거나 Laravel 자체가 특정 호스트만 허용하도록 제한하고 싶다면, `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화할 수 있습니다.

`TrustHosts` 미들웨어를 활성화하려면, `bootstrap/app.php`의 `trustHosts` 미들웨어 메서드를 호출하세요. 이 때, `at` 인자에 허용할 호스트명 목록을 지정합니다. 이외의 호스트로 요청이 들어오면 애플리케이션이 거부합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 앱 URL의 하위 도메인에서 오는 요청도 자동으로 신뢰합니다. 이 기능을 끄고 싶으면 `subdomains` 인자를 false로 지정하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

신뢰할 호스트를 구성 파일이나 DB 등에서 읽어야 한다면, `at` 인자에 클로저를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```