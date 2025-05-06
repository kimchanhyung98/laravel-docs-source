# HTTP 요청

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 접근하기](#accessing-the-request)
    - [요청 경로, 호스트 및 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값](#input)
    - [입력값 조회](#retrieving-input)
    - [입력값 존재 여부 판별](#determining-if-input-is-present)
    - [추가 입력값 병합](#merging-additional-input)
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

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청과, 요청에 포함된 입력값, 쿠키, 파일 등을 객체 지향적으로 다룰 수 있는 방법을 제공합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청 접근하기

의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면 라우트 클로저 또는 컨트롤러 메소드에서 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. 들어오는 요청 인스턴스는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 사용자를 저장합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $name = $request->input('name');

        //
    }
}
```

위에서 언급한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트할 수 있습니다. 서비스 컨테이너가 실행 시점에 자동으로 요청 인스턴스를 클로저에 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    //
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입 & 라우트 파라미터

컨트롤러 메소드에서 라우트 파라미터의 입력값도 필요하다면, 파라미터를 나머지 의존성 뒤에 순서대로 나열해야 합니다. 예를 들어 아래와 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메소드에서 `Illuminate\Http\Request`를 타입힌트하고 `id` 라우트 파라미터에도 접근할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 사용자를 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트 및 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 조사하는 다양한 메서드를 제공합니다. 또한 `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서는 가장 중요한 몇 가지 메서드를 살펴봅니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 조회

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 들어오는 요청이 `http://example.com/foo/bar`를 대상으로 한다면, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사

`is` 메서드를 사용하면 요청 경로가 특정 패턴과 일치하는지 검사할 수 있습니다. 이때 `*`을 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    //
}
```

`routeIs` 메서드를 사용하면 현재 요청이 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)와 일치하는지 알 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    //
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 조회

들어오는 요청의 전체 URL을 조회하려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url`은 쿼리 문자열 없는 URL을, `fullUrl`은 쿼리 문자열을 포함한 전체 URL을 반환합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열 데이터를 추가하고 싶으면 `fullUrlWithQuery` 메서드를 사용하세요. 이 메서드는 전달된 쿼리 정보와 현재 쿼리 문자열을 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 조회

`host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 들어온 요청의 "호스트" 정보를 가져올 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드(HTTP Verb) 조회

`method` 메서드는 요청의 HTTP 메서드를 반환합니다. `isMethod` 메서드를 사용하면 요청의 HTTP 메서드가 특정 문자열과 일치하는지 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    //
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스의 `header` 메서드를 사용하면 특정 요청 헤더를 조회할 수 있습니다. 해당 헤더가 없으면 `null`이 반환됩니다. 두 번째 인자로 기본값을 전달하면, 헤더가 없을 경우 그 값이 반환됩니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드로 요청에 특정 헤더가 포함되어 있는지 확인할 수 있습니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    //
}
```

편의를 위해, `bearerToken` 메서드는 `Authorization` 헤더에서 베어러 토큰을 조회합니다. 헤더가 없으면 빈 문자열을 반환합니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드를 사용하면 요청을 보낸 클라이언트의 IP 주소를 조회할 수 있습니다.

```php
$ipAddress = $request->ip();
```

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 들어오는 요청의 `Accept` 헤더를 통해 요청된 콘텐츠 타입을 조사하는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청이 수용 가능한 모든 콘텐츠 타입을 배열로 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 받아, 그 중 하나라도 요청에서 허용된다면 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드를 사용하면 주어진 배열 중에서 요청이 가장 선호하는 콘텐츠 타입을 알 수 있습니다. 어떤 것도 허용되지 않으면 `null`을 반환합니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML 또는 JSON만 제공하는 경우 `expectsJson` 메서드로 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청/응답을 비롯한 HTTP 메시지를 위한 인터페이스를 정의합니다. Laravel의 요청 대신 PSR-7 요청 인스턴스를 사용하려면 몇 가지 라이브러리를 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 일반 Laravel 요청/응답을 PSR-7 호환 구현으로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리들을 설치하면, 라우트 클로저나 컨트롤러 메소드에서 PSR-7 요청 인터페이스를 타입힌트하여 PSR-7 요청을 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    //
});
```

> **참고**
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면 자동으로 Laravel 응답 인스턴스로 변환되어 프레임워크가 표시합니다.

<a name="input"></a>
## 입력값

<a name="retrieving-input"></a>
### 입력값 조회

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 조회

`all` 메서드를 사용하여 들어오는 요청의 모든 입력값을 `array`로 가져올 수 있습니다. 이 메서드는 HTML 폼이나 XHR 요청 모두에서 사용할 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드로 요청의 모든 입력값을 [컬렉션](/docs/{{version}}/collections)으로 가져올 수도 있습니다.

```php
$input = $request->collect();
```

`collect` 메서드는 요청 입력값의 하위 집합을 컬렉션으로 조회할 수도 있습니다.

```php
$request->collect('users')->each(function ($user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 개별 입력값 조회

간단한 몇 가지 메서드를 사용해 HTTP 메서드와 상관없이 `Illuminate\Http\Request` 인스턴스에서 모든 사용자 입력값에 접근할 수 있습니다. `input` 메서드는 HTTP 메서드 종류에 관계없이 입력값을 조회합니다.

```php
$name = $request->input('name');
```

`input` 메서드의 두 번째 인자에 기본값을 전달할 수 있습니다. 요청에 값이 없으면 이 값이 반환됩니다.

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값을 사용하는 폼에서는 `dot` 표기법을 사용해 배열에 접근할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인자 없이 `input` 메서드를 호출하면 모든 입력값을 연관 배열로 가져올 수 있습니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력값 조회

`input` 메서드는 요청 전체(쿼리 문자열 포함)에서 값을 가져오지만, `query` 메서드는 오직 쿼리 문자열에서만 값을 조회합니다.

```php
$name = $request->query('name');
```

요청에 없는 쿼리 문자열 값에 대해 두 번째 인자로 기본값을 전달할 수 있습니다.

```php
$name = $request->query('name', 'Helen');
```

인자 없이 `query` 메서드를 호출하면 모든 쿼리 문자열 값을 연관 배열로 가져올 수 있습니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 조회

애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있으면 `input` 메서드로 JSON 데이터를 접근할 수 있습니다. 또한 "dot" 표기법을 사용하여 JSON 배열/객체 안의 중첩된 값에도 접근할 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 조회

요청의 입력값을 원시 `string`이 아닌 [`Illuminate\Support\Stringable`](/docs/{{version}}/helpers#fluent-strings) 인스턴스로 얻으려면 `string` 메서드를 사용할 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-boolean-input-values"></a>
#### Boolean 입력값 조회

HTML 체크박스와 같은 요소는 실제로 문자열인 "truthy" 값을 가질 수 있습니다. 예: "true", "on" 등. `boolean` 메서드를 사용하면 이런 값을 Boolean으로 변환할 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환하고, 그 외의 값은 모두 `false`를 반환합니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 조회

편의를 위해, 날짜/시간이 포함된 입력값은 `date` 메서드를 사용해 Carbon 인스턴스로 가져올 수 있습니다. 요청에 해당 이름의 입력값이 없으면 `null`이 반환됩니다.

```php
$birthday = $request->date('birthday');
```

`date` 메서드의 두 번째, 세 번째 인자는 날짜 형식과 타임존을 지정하는 데 사용할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 있지만 유효하지 않은 형식이면 `InvalidArgumentException`이 발생하므로, `date` 메서드 호출 전에 입력값을 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 조회

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)에 해당하는 입력값도 요청에서 조회할 수 있습니다. 요청에 값이 없거나 입력값과 일치하는 enum 백킹 값이 없는 경우에는 `null`이 반환됩니다. `enum` 메서드는 입력값의 이름과 enum 클래스를 첫 번째, 두 번째 인자로 받습니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 조회

`Illuminate\Http\Request` 인스턴스에서 동적 프로퍼티로 사용자 입력값에 접근할 수도 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 아래처럼 접근할 수 있습니다.

```php
$name = $request->name;
```

동적 프로퍼티 사용 시, Laravel은 먼저 요청 페이로드에서 파라미터의 값을 찾고, 없으면 라우트 파라미터에서 조회합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값 일부만 조회

입력값의 일부만 얻으려면 `only` 및 `except` 메서드를 사용할 수 있습니다. 이 메서드들은 배열 또는 다수의 인자를 받을 수 있습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> **주의**
> `only` 메서드는 요청에 존재하는 key/value 값만 반환합니다. 요청에 없는 값은 반환하지 않습니다.

<a name="determining-if-input-is-present"></a>
### 입력값 존재 여부 판별

`has` 메서드를 사용하면 요청에 특정 값이 존재하는지 판별할 수 있습니다. 값이 있으면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    //
}
```

배열을 넘기면, 지정한 모든 값이 요청에 존재할 때만 `true`가 반환됩니다.

```php
if ($request->has(['name', 'email'])) {
    //
}
```

`whenHas` 메서드는 값이 존재할 때 주어진 클로저를 실행합니다.

```php
$request->whenHas('name', function ($input) {
    //
});
```

두 번째 클로저를 전달하면, 값이 없을 때 그 클로저가 실행됩니다.

```php
$request->whenHas('name', function ($input) {
    // "name" 값이 존재함...
}, function () {
    // "name" 값이 없음...
});
```

`hasAny` 메서드는 지정한 값 중 하나라도 있으면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    //
}
```

값이 존재하고 비어 있지 않은지 확인하려면 `filled` 메서드를 사용하세요.

```php
if ($request->filled('name')) {
    //
}
```

`whenFilled` 메서드는 값이 존재하고 비어 있지 않을 때 클로저를 실행합니다.

```php
$request->whenFilled('name', function ($input) {
    //
});
```

두 번째 클로저를 넘기면 값이 "채워지지 않은 경우" 실행됩니다.

```php
$request->whenFilled('name', function ($input) {
    // "name" 값이 채워짐...
}, function () {
    // "name" 값이 채워지지 않음...
});
```

주어진 키가 요청에 없는지 확인하려면 `missing` 및 `whenMissing` 메서드를 사용할 수 있습니다.

```php
if ($request->missing('name')) {
    //
}

$request->whenMissing('name', function ($input) {
    // "name" 값이 누락됨...
}, function () {
    // "name" 값이 존재함...
});
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합

가끔은 기존 요청 입력 데이터에 입력값을 수동으로 병합해야 할 때가 있습니다. 이럴 때 `merge` 메서드를 사용하세요. 동일한 입력 키가 이미 있으면 입력 값이 덮어써집니다.

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 해당 키가 존재하지 않을 때만 입력값을 병합합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값

Laravel에서는 한 요청에서 입력값을 다음 요청까지 보존할 수 있습니다. 이 기능은 검증 오류 발생 후 폼을 다시 채울 때 특히 유용합니다. 다만, Laravel의 [검증 기능](/docs/{{version}}/validation)을 사용할 때는 수동으로 세션 입력값을 플래시하지 않아도 기본 제공 검증 기능이 자동으로 처리합니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기

`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력값을 [세션](/docs/{{version}}/session)에 플래시하여, 다음 요청 때 사용 가능합니다.

```php
$request->flash();
```

`flashOnly` 및 `flashExcept` 메서드로 특정 입력값 일부만 세션에 플래시할 수 있습니다. 이 방법으로 비밀번호 등 민감한 정보를 세션에 남기지 않을 수 있습니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트

보통 입력값을 세션에 플래시하고 이전 페이지로 리다이렉트해야 할 때가 많으므로, `withInput` 메서드를 사용해 리다이렉트에 입력값 플래시를 체이닝할 수 있습니다.

```php
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 조회

이전 요청에서 플래시된 입력값을 조회하려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. 이 메서드는 이전에 플래시된 입력값을 [세션](/docs/{{version}}/session)에서 가져옵니다.

```php
$username = $request->old('username');
```

또한 Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/{{version}}/blade)에서 이전 입력값을 표시할 때 이 헬퍼가 더욱 편리하게 사용할 수 있습니다. 입력값이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 조회

Laravel 프레임워크가 생성한 모든 쿠키는 암호화되고 인증 코드로 서명되어, 클라이언트에 의해 변경된 경우 무효 처리됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

기본적으로 Laravel은 `App\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 전역 미들웨어 스택에 등록합니다. 이 미들웨어들은 `App\Http\Kernel` 클래스의 `$middleware` 속성에 명시되어 있습니다. 요청이 들어올 때 모든 문자열 입력값을 자동으로 트리밍하고, 빈 문자열은 `null`로 변환합니다. 덕분에 라우트 및 컨트롤러에서는 별도로 신경 쓸 필요가 없습니다.

#### 입력값 정규화 비활성화

이 동작을 모든 요청에 대해 비활성화하려면, `App\Http\Kernel` 클래스의 `$middleware` 속성에서 해당 미들웨어를 제거하면 됩니다.

일부 요청에만 문자열 트리밍과 빈 문자열 변환을 비활성화하려면, 해당 미들웨어에서 제공하는 `skipWhen` 메서드를 사용하세요. 이 메서드는 입력값 정규화 여부를 반환하는 클로저를 받습니다. 일반적으로 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use App\Http\Middleware\TrimStrings;
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    TrimStrings::skipWhen(function ($request) {
        return $request->is('admin/*');
    });

    ConvertEmptyStringsToNull::skipWhen(function ($request) {
        // ...
    });
}
```

<a name="files"></a>
## 파일

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 조회

`Illuminate\Http\Request` 인스턴스에서 `file` 메서드나 동적 프로퍼티로 업로드된 파일을 조회할 수 있습니다. `file` 메서드는 PHP `SplFileInfo` 클래스를 확장한 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환하며, 파일과 상호작용할 수 있는 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드로 요청에 파일이 포함되어 있는지 확인할 수 있습니다.

```php
if ($request->hasFile('photo')) {
    //
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 검사

파일이 요청에 존재하는지 확인하는 것뿐 아니라, `isValid` 메서드로 파일 업로드에 문제가 없는지도 확인할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    //
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스에는 파일의 전체 경로와 확장자를 조회할 수 있는 메서드도 있습니다. `extension` 메서드는 파일의 실제 내용을 기반으로 확장자를 추측하며, 이는 클라이언트에서 보내온 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에는 다양한 다른 메서드도 있습니다. 자세한 내용은 [해당 클래스의 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장

업로드된 파일을 저장할 때는 보통 구성된 [파일시스템](/docs/{{version}}/filesystem)을 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 설정된 디스크로 이동합니다. 디스크는 로컬 파일 시스템, Amazon S3 등 클라우드 저장소일 수 있습니다.

`store` 메서드는 파일시스템 루트 디렉터리를 기준으로 저장 경로를 받습니다. 이 경로는 파일명을 포함하지 않아야 하며, 고유 ID로 자동 생성된 이름이 사용됩니다.

`store` 메서드는 디스크 이름(두 번째 인자)을 옵션으로 받습니다. 반환값은 디스크 루트 대비 저장된 파일의 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 직접 지정하고 싶다면 `storeAs` 메서드를 사용할 수 있습니다. 경로, 파일명, 디스크명을 인자로 받습니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> **참고**
> Laravel의 파일 저장에 대한 자세한 내용은 [파일 저장소 전체 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼로 HTTPS 링크가 생성되지 않는 경우가 발생할 수 있습니다. 이는 일반적으로 로드 밸런서에서 80번 포트로 트래픽이 포워딩되어 애플리케이션이 안전한(secure) 연결임을 알지 못하기 때문입니다.

이를 해결하려면, Laravel 애플리케이션에 포함된 `App\Http\Middleware\TrustProxies` 미들웨어를 사용하면 됩니다. 이 미들웨어에서 신뢰할 수 있는 프록시(로드 밸런서)를 `$proxies` 속성의 배열로 지정하세요. 또한 신뢰할 헤더도 `$headers` 속성으로 구성할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * 이 애플리케이션의 신뢰할 수 있는 프록시 목록.
     *
     * @var string|array
     */
    protected $proxies = [
        '192.168.1.1',
        '192.168.1.2',
    ];

    /**
     * 프록시 탐지를 위한 헤더 목록.
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_FOR | Request::HEADER_X_FORWARDED_HOST | Request::HEADER_X_FORWARDED_PORT | Request::HEADER_X_FORWARDED_PROTO;
}
```

> **참고**
> AWS Elastic Load Balancing을 사용하는 경우, `$headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`로 설정해야 합니다. `$headers`에 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [프록시 신뢰 구성 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

Amazon AWS 등 "클라우드" 로드 밸런서 제공업체를 사용할 때 실제 밸런서의 IP를 알 수 없다면, `*`로 전체 프록시를 신뢰하세요.

```php
/**
 * 이 애플리케이션의 신뢰할 수 있는 프록시 목록.
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더와 무관하게 모든 요청에 응답합니다. 또한 `Host` 헤더의 값은 웹 요청 중 절대 URL을 생성할 때 사용됩니다.

보통은 웹 서버(예: Nginx, Apache)에서 특정 호스트네임과 일치하는 요청만 애플리케이션에 전달하도록 서버를 구성하는 것이 좋습니다. 하지만 서버 자체를 제어할 수 없고, Laravel에 직접 응답할 호스트를 지정하려면 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하세요.

`TrustHosts` 미들웨어는 기본적으로 `$middleware` 스택에 포함되어 있지만 주석이 처리되어 있습니다. 주석을 해제하면 활성화됩니다. 미들웨어의 `hosts` 메서드에서 애플리케이션이 응답할 호스트명 목록을 지정할 수 있습니다. 다르게 오는 `Host` 헤더의 요청은 거부됩니다.

```php
/**
 * 신뢰할 호스트 패턴 목록을 반환.
 *
 * @return array
 */
public function hosts()
{
    return [
        'laravel.test',
        $this->allSubdomainsOfApplicationUrl(),
    ];
}
```

`allSubdomainsOfApplicationUrl` 헬퍼 메서드는 `app.url` 설정값의 모든 서브도메인과 일치하는 정규식을 반환합니다. 이 헬퍼로 와일드카드 서브도메인을 사용하는 애플리케이션에서도 모든 서브도메인을 편리하게 허용할 수 있습니다.