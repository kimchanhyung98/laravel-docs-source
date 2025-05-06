# HTTP 요청

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메소드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값(Input)](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 존재 확인](#input-presence)
    - [추가 입력값 병합하기](#merging-additional-input)
    - [이전 입력값 사용하기](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 현재 처리 중인 HTTP 요청과 상호작용하고, 요청과 함께 전송된 입력값, 쿠키, 파일 등을 객체 지향적으로 다룰 수 있도록 해줍니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청 접근하기

의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저나 컨트롤러 메소드에서 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 요청 인스턴스를 주입합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 사용자 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 사용자 저장...

        return redirect('/users');
    }
}
```

앞서 언급한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request`를 타입힌트할 수 있습니다. 서비스 컨테이너가 자동으로 해당 요청을 주입합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메소드에서 라우트 파라미터도 함께 입력받아야 하는 경우, 다른 의존성 뒤에 라우트 파라미터를 나열하면 됩니다. 예시:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메소드에서 다음과 같이 작성할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 사용자 정보 수정.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 정보 수정...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메소드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 확인하기 위한 다양한 메소드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에 주요 메소드들을 설명합니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기

`path` 메소드는 요청의 경로 정보를 반환합니다. 예를 들어, 요청이 `http://example.com/foo/bar`일 경우, `path` 메소드는 `foo/bar`를 반환합니다:

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로 / 라우트 확인

`is` 메소드를 사용하면, 들어오는 요청의 경로가 주어진 패턴과 일치하는지 확인할 수 있습니다. 이 메소드에서는 `*` 와일드카드 문자를 사용할 수 있습니다:

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메소드를 사용하면, 들어오는 요청이 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)와 일치하는지 확인할 수 있습니다:

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

들어오는 요청의 전체 URL을 불러오려면 `url` 또는 `fullUrl` 메소드를 사용할 수 있습니다.  
`url` 메소드는 쿼리 스트링 없이 URL을 반환하고, `fullUrl`은 쿼리 스트링까지 포함해서 반환합니다:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 스트링 데이터를 추가하고 싶다면, `fullUrlWithQuery` 메소드를 사용할 수 있습니다. 이 메소드는 현재 쿼리 스트링에 지정한 배열을 병합합니다:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 스트링 파라미터를 제거한 상태의 현재 URL이 필요하다면, `fullUrlWithoutQuery` 메소드를 사용할 수 있습니다:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기

들어오는 요청의 "호스트"는 `host`, `httpHost`, `schemeAndHttpHost` 메소드로 가져올 수 있습니다:

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메소드 가져오기

`method` 메소드는 HTTP 요청의 메소드를 반환합니다. `isMethod` 메소드를 사용하면 해당 메소드가 특정 문자열과 일치하는지 확인할 수 있습니다:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스의 `header` 메소드로 요청 헤더를 가져올 수 있습니다. 헤더가 존재하지 않으면 `null`이 반환됩니다. 하지만 두 번째 인자로 기본값을 넘기면, 해당 헤더가 없을 때 그 값이 반환됩니다:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메소드를 사용하면 요청에 특정 헤더가 있는지 확인할 수 있습니다:

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

`bearerToken` 메소드를 사용하면 `Authorization` 헤더에서 베어러 토큰을 편리하게 추출할 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다:

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메소드로 요청을 보낸 클라이언트의 IP 주소를 가져올 수 있습니다:

```php
$ipAddress = $request->ip();
```

프록시로 전달된 모든 클라이언트 IP 주소 목록이 필요하다면, `ips` 메소드를 사용할 수 있습니다. "원본" 클라이언트 IP는 배열의 마지막에 위치합니다:

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는, 사용자가 제어할 수 있는 입력값이므로 참고용으로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 `Accept` 헤더를 통해 요청이 원하는 콘텐츠 타입을 검사하는 여러 메소드를 제공합니다. 먼저, `getAcceptableContentTypes` 메소드는 요청에서 허용하는 모든 콘텐츠 타입을 배열로 반환합니다:

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메소드는 전달된 배열 중 하나라도 요청에서 허용하면 `true`, 아니면 `false`를 반환합니다:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메소드를 사용하면 주어진 콘텐츠 타입 배열에서 요청이 가장 선호하는 타입을 알 수 있습니다. 아무것도 허용하지 않으면 `null`이 반환됩니다:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML이나 JSON만 반환한다면, `expectsJson` 메소드로 현재 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다:

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청 및 응답)에 대한 인터페이스를 지정합니다. Laravel에서 기본 `Request`가 아닌 PSR-7 요청 객체를 사용하려면 관련 라이브러리를 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 통해 PSR-7 호환 구현을 제공합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

설치 후, 라우트 클로저나 컨트롤러에서 PSR-7 요청 인터페이스를 타입힌트 하면 인스턴스를 받을 수 있습니다:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]  
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 Laravel 응답 인스턴스로 변환하여 표시합니다.

<a name="input"></a>
## 입력값(Input)

<a name="retrieving-input"></a>
### 입력값 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 가져오기

`all` 메소드를 사용해 들어오는 요청의 모든 입력값을 `array`로 가져올 수 있습니다. 이 메소드는 HTML 폼 요청과 XHR 요청 모두에서 사용 가능합니다:

```php
$input = $request->all();
```

`collect` 메소드를 사용하면 모든 입력값을 [컬렉션](/docs/{{version}}/collections) 형태로도 가져올 수 있습니다:

```php
$input = $request->collect();
```

특정 입력값만 컬렉션으로 가져오려면, `collect('users')`처럼 사용할 수 있습니다:

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 입력값 하나 가져오기

간단한 메소드로 요청 인스턴스에서 모든 사용자 입력값에 접근할 수 있습니다. HTTP 메소드와 상관없이 `input` 메소드를 사용해 입력값을 가져올 수 있습니다:

```php
$name = $request->input('name');
```

두 번째 인자로 기본값을 전달하면, 해당 입력이 없을 때 그 값을 반환합니다:

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값이 있는 폼은 "dot" 표기법을 사용할 수 있습니다:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

아무런 인자 없이 `input` 메소드를 호출하면, 모든 입력값을 연관 배열로 반환합니다:

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 가져오기

`input` 메소드는 전체 요청 데이터(쿼리 스트링 포함)에서 값을 가져오지만, `query` 메소드는 쿼리 스트링 값만 가져옵니다:

```php
$name = $request->query('name');
```

쿼리 스트링에 값이 없으면 두 번째 인자로 전달된 기본값이 반환됩니다:

```php
$name = $request->query('name', 'Helen');
```

인자 없이 호출하면 모든 쿼리 스트링 값을 연관 배열로 반환합니다:

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

애플리케이션에 JSON 요청이 전달될 때, 요청의 `Content-Type` 헤더가 `application/json`으로 설정되어 있다면 `input` 메소드로 JSON 데이터를 가져올 수 있습니다. "dot" 표기법으로 중첩된 값을 가져올 수도 있습니다:

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 가져오기

입력값을 기본 `string`이 아닌 [`Illuminate\Support\Stringable`](/docs/{{version}}/strings) 인스턴스로 받고 싶다면 `string` 메소드를 사용할 수 있습니다:

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 가져오기

입력값을 정수로 변환해서 받고 싶다면 `integer` 메소드를 사용할 수 있습니다. 값이 없거나 변환에 실패하면 기본값을 반환합니다. 페이지네이션 등에서 유용합니다:

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기

체크박스 등에서 "true", "on" 등 문자열이 전송되는 경우, `boolean` 메소드로 이를 불리언 값으로 변환해 받을 수 있습니다. 이 메소드는 1, "1", true, "true", "on", "yes"의 경우 `true`, 그 외는 `false`를 반환합니다:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜/시간을 포함한 입력값은 `date` 메소드로 Carbon 인스턴스로 변환해서 받을 수 있습니다. 값이 없으면 `null`이 반환됩니다:

```php
$birthday = $request->date('birthday');
```

두 번째, 세 번째 인자를 통해 날짜 포맷과 타임존을 지정할 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 있지만 포맷이 올바르지 않을 경우 `InvalidArgumentException`이 발생하므로, 이 메소드 사용 전 입력값을 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 가져오기

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)과 매칭되는 입력값도 가져올 수 있습니다. 값이 없거나 일치하는 enum이 없으면 `null`을 반환합니다. 첫 번째 인자는 입력값의 이름, 두 번째는 enum 클래스입니다:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

Enum 배열처럼 여러 값을 한 번에 받을 때는 `enums` 메소드를 사용할 수 있습니다:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 접근

`Illuminate\Http\Request` 인스턴스에서 동적 프로퍼티를 통해서도 사용자 입력값에 접근할 수 있습니다. 예를 들어 폼에 `name` 필드가 있다면 다음과 같이 사용할 수 있습니다:

```php
$name = $request->name;
```

동적 프로퍼티 사용 시, Laravel은 먼저 요청 페이로드에서 값을 찾고, 없으면 매치된 라우트의 파라미터에서 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 일부 입력값만 가져오기

입력값의 일부만 필요하면 `only`와 `except` 메소드를 사용할 수 있습니다. 두 메소드 모두 배열이나 인자 리스트를 받습니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]  
> `only` 메소드는 요청에 존재하는 키만 반환하며, 존재하지 않는 키는 반환하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 확인

`has` 메소드를 사용해 특정 값이 요청에 있는지 확인할 수 있습니다. 값이 존재하면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    // ...
}
```

배열을 넘기면, 모든 값이 존재할 때만 `true`를 반환합니다:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메소드는 지정한 값 중 하나라도 있으면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메소드는 값이 있으면 첫 번째 클로저를 실행합니다:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

지정한 값이 없을 때 두 번째 클로저를 실행할 수도 있습니다:

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 있음...
}, function () {
    // "name" 값이 없음...
});
```

값이 있고, 비어 있지 않은 문자열인지 확인하려면 `filled` 메소드를 사용합니다:

```php
if ($request->filled('name')) {
    // ...
}
```

값이 없거나 비어있는지 확인하려면 `isNotFilled` 메소드를 사용합니다:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 넘기면, 모두 없는 경우에만 `true`를 반환합니다:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메소드는 지정한 값 중 하나라도 비어있지 않으면 `true`를 반환합니다:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메소드는 값이 있고 비어있지 않으면 클로저를 실행합니다:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저까지 지정하면, 채워진 경우와 아니라면 경우에 따라 실행할 수 있습니다:

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져 있음...
}, function () {
    // "name" 값이 채워져 있지 않음...
});
```

값이 없을 때는 `missing`과 `whenMissing` 메소드를 사용할 수 있습니다:

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
### 추가 입력값 병합하기

추가 입력값을 기존 요청 데이터에 병합해야 할 경우, `merge` 메소드를 사용할 수 있습니다. 이미 존재하는 키가 있다면 새로운 값으로 덮어씁니다:

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메소드는 해당 키가 존재하지 않는 경우만 값을 추가합니다:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값 사용하기

Laravel에서는 한 번의 요청에서 받은 입력값을 다음 요청에도 사용할 수 있습니다. 이 기능은 주로 유효성 검사에서 오류가 발생했을 때 폼을 다시 채울 때 사용됩니다.  
Laravel의 [유효성 검사 기능](/docs/{{version}}/validation)을 사용할 경우, 입력값 플래시 관련 메소드를 직접 사용할 필요가 없는 경우가 많습니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시

`Illuminate\Http\Request` 클래스의 `flash` 메소드는 현재 입력값을 [세션](/docs/{{version}}/session)에 플래시시켜, 사용자의 다음 요청에서 사용할 수 있게 합니다:

```php
$request->flash();
```

`flashOnly`와 `flashExcept` 메소드는 일부 입력값만 세션에 플래시시킬 때 사용합니다. 예를 들어 비밀번호와 같은 민감한 정보를 저장하지 않을 때 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 플래시 후 리다이렉트

입력값을 플래시하고 나서 이전 페이지로 리다이렉트하는 경우가 많으므로, `withInput` 메소드로 체이닝할 수 있습니다:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메소드를 사용하세요. 세션에서 이전 입력값을 가져옵니다:

```php
$username = $request->old('username');
```

Laravel에서는 글로벌 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/{{version}}/blade)에서 입력값을 다시 채울 때 이 헬퍼를 쓰면 더욱 편리합니다. 값이 없으면 `null`이 반환됩니다:

```html
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel이 생성하는 모든 쿠키는 암호화되고 인증 코드로 서명되므로, 클라이언트에서 변조된 경우 유효하지 않게 됩니다. 요청에서 쿠키 값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `cookie` 메소드를 사용하세요:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

기본적으로 Laravel에는 `Illuminate\Foundation\Http\Middleware\TrimStrings` 및 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어가 글로벌 스택에 포함되어 있습니다. 이 미들웨어들은 들어오는 모든 문자열 필드를 자동으로 트리밍하고, 빈 문자열을 `null`로 변환합니다. 이를 통해 라우트나 컨트롤러에서 입력 정규화로 인한 고민 없이 코딩할 수 있습니다.

#### 입력 정규화 비활성화

모든 요청에 대해 이 동작을 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메소드로 해당 미들웨어를 제거하면 됩니다:

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

일부 요청에만 문자열 트리밍, 빈 문자열 변환을 비활성화하고 싶다면, `bootstrap/app.php`에서 각각 `trimStrings`, `convertEmptyStringsToNull` 미들웨어 메소드에 클로저 배열을 전달하세요. 클로저는 정규화를 건너뛰어야 할 때 `true`를 반환합니다:

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

`Illuminate\Http\Request` 인스턴스에서 `file` 메소드나 동적 프로퍼티를 사용하여 업로드된 파일에 접근할 수 있습니다.  
`file` 메소드는 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 이 클래스는 PHP `SplFileInfo`를 확장하여 파일 관련 다양한 메소드를 제공합니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메소드로 요청에 파일이 있는지 확인할 수 있습니다:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 정상 여부 검증

파일이 존재하는지 확인하는 것 이외에, `isValid` 메소드로 업로드 과정에서 문제가 없었는지 검증할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스는 파일의 전체 경로 및 확장자에 접근하는 메소드도 포함합니다. `extension` 메소드는 파일 내용을 기반으로 확장자를 추정하며, 클라이언트가 보낸 확장자와 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메소드

`UploadedFile` 인스턴스에는 다양한 메소드가 있습니다. 자세한 내용은 [클래스의 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일을 저장하려면, 일반적으로 미리 구성된 [파일 시스템](/docs/{{version}}/filesystem) 중 하나를 사용합니다.  
`UploadedFile` 클래스의 `store` 메소드는 업로드된 파일을 로컬이나 S3 같은 클라우드 저장소에 옮길 수 있습니다.

`store` 메소드는 파일이 저장될 경로(파일 시스템의 루트로부터 상대 경로)를 받으며, 파일명은 생성된 고유 ID로 자동 결정됩니다.

두 번째 인자에는 저장할 디스크 이름을 지정할 수 있습니다. 반환값은 디스크 루트에서의 상대 경로입니다:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 직접 지정하려면, `storeAs` 메소드에 경로, 파일명, 디스크 이름을 차례로 전달하세요:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]  
> 파일 저장에 관한 자세한 내용은 전체 [파일 저장소 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 앱을 실행할 때, `url` 헬퍼로 HTTPS 링크가 생성되지 않는 경우가 있습니다. 이는 일반적으로 로드 밸런서가 80번 포트로 트래픽을 전달해 앱이 HTTPS임을 인지하지 못하기 때문입니다.

이럴 때, `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화해, 앱이 신뢰할 로드 밸런서 또는 프록시 IP를 지정할 수 있습니다.  
신뢰할 프록시는 애플리케이션의 `bootstrap/app.php`에서 `trustProxies` 미들웨어 메소드로 지정합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 프록시뿐만 아니라 신뢰해야 하는 프록시 헤더도 구성할 수 있습니다:

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
> AWS Elastic Load Balancing을 사용한다면, `headers` 값으로 `Request::HEADER_X_FORWARDED_AWS_ELB`를 사용해야 합니다. 로드 밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 표준 `Forwarded` 헤더를 사용한다면, `headers` 값으로 `Request::HEADER_FORWARDED`를 사용하세요. 더 자세한 상수 정보는 Symfony의 [신뢰할 수 있는 프록시 문서](https://symfony.com/doc/7.0/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

AWS와 같은 "클라우드" 로드 밸런서를 사용할 경우, 실제 밸런서의 IP를 모르기도 합니다. 이럴 땐 `*`로 모든 프록시를 신뢰할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

Laravel은 기본적으로 HTTP 요청의 `Host` 헤더 값과 무관하게 모든 요청에 응답합니다. 또한, 절대 URL을 생성할 때 이 `Host`의 값을 사용합니다.

일반적으로는 웹 서버(Nginx, Apache 등)에서 특정 호스트명만 애플리케이션으로 넘기도록 구성하지만, 서버 설정이 어렵거나 불가능할 경우 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하여 Laravel에 허용할 호스트를 직접 지정할 수 있습니다.

`TrustHosts` 미들웨어는 애플리케이션의 `bootstrap/app.php` 파일에서 활성화하며, `at` 인자에 허용할 호스트명을 배열로 지정합니다. 이외의 `Host`로 들어온 요청은 거부됩니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 애플리케이션 URL의 서브도메인도 자동으로 신뢰합니다. 이 동작을 비활성화하려면 `subdomains` 인자를 `false`로 설정하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

설정 파일이나 데이터베이스에서 신뢰할 호스트 정보를 불러와야 한다면, 클로저를 `at` 인자로 넘길 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```