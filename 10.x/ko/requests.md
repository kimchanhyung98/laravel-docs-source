# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청 다루기](#interacting-with-the-request)
    - [요청 인스턴스 접근](#accessing-the-request)
    - [요청 경로, 호스트, 그리고 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력](#input)
    - [입력 데이터 가져오기](#retrieving-input)
    - [입력 존재 여부](#input-presence)
    - [추가 입력 병합하기](#merging-additional-input)
    - [이전 입력 데이터](#old-input)
    - [쿠키](#cookies)
    - [입력 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰하는 프록시 설정하기](#configuring-trusted-proxies)
- [신뢰하는 호스트 설정하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션이 처리하는 현재 HTTP 요청을 객체지향적으로 다룰 수 있도록 하며, 요청과 함께 제출된 입력 데이터, 쿠키, 파일 등을 간편하게 가져올 수 있는 기능을 제공합니다.

<a name="interacting-with-the-request"></a>
## 요청 다루기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청 인스턴스 접근 (Accessing the Request)

의존성 주입(dependency injection)을 통해 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. 이때 Laravel의 [서비스 컨테이너](/docs/10.x/container)가 자동으로 요청 인스턴스를 주입합니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 사용자 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 사용자 저장 처리...

        return redirect('/users');
    }
}
```

앞서 말했듯이, 라우트 클로저에 `Illuminate\Http\Request` 클래스를 타입힌트할 수도 있습니다. 서비스 컨테이너는 실행 시 클로저에 요청 인스턴스를 자동으로 주입합니다:

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 매개변수 (Dependency Injection and Route Parameters)

컨트롤러 메서드가 라우트 매개변수도 기대한다면, 라우트 매개변수는 다른 의존성들 뒤에 위치해야 합니다. 예를 들어, 라우트가 아래처럼 정의되어 있다면:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

`Illuminate\Http\Request`를 타입힌트함과 동시에 `id` 라우트 매개변수도 아래와 같이 받을 수 있습니다:

```
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
        // 사용자 업데이트 처리...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 그리고 메서드 (Request Path, Host, and Method)

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 살펴볼 수 있는 다양한 메서드를 갖고 있으며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 주요 메서드 중 일부를 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기 (Retrieving the Request Path)

`path` 메서드는 요청의 경로 정보를 반환합니다. 즉, 요청 URL이 `http://example.com/foo/bar` 라면, `path` 메서드는 `foo/bar` 를 반환합니다:

```
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로나 라우트 검사하기 (Inspecting the Request Path / Route)

`is` 메서드를 사용하면 요청 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자는 와일드카드로 사용됩니다:

```
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면 요청이 [이름 붙은 라우트](/docs/10.x/routing#named-routes)와 일치하는지 확인할 수 있습니다:

```
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기 (Retrieving the Request URL)

전체 URL(쿼리 문자열 제외)을 가져오려면 `url` 메서드를, 쿼리 문자열을 포함한 전체 URL을 가져오려면 `fullUrl` 메서드를 사용합니다:

```
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열 데이터를 추가하려면 `fullUrlWithQuery` 메서드를 씁니다. 이는 현재 쿼리 문자열과 전달된 배열을 병합합니다:

```
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 문자열 파라미터 없이 현재 URL을 가져오려면 `fullUrlWithoutQuery` 메서드를 사용하세요:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기 (Retrieving the Request Host)

`host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 요청의 호스트 정보를 각각 가져올 수 있습니다:

```
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기 (Retrieving the Request Method)

`method` 메서드는 요청에 사용된 HTTP 동사를 반환합니다. `isMethod` 메서드로는 특정 HTTP 동사와 일치하는지 확인할 수 있습니다:

```
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더 (Request Headers)

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용해 요청 헤더 값을 가져올 수 있습니다. 헤더가 없으면 `null`이 반환되며, 두 번째 인자로 기본값을 지정할 수도 있습니다:

```
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드로 특정 헤더가 요청에 포함되어 있는지 확인할 수 있습니다:

```
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해 `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 Bearer 토큰을 쉽게 가져올 수 있으며, 없으면 빈 문자열을 반환합니다:

```
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소 (Request IP Address)

클라이언트 IP 주소는 `ip` 메서드로 구할 수 있습니다:

```
$ipAddress = $request->ip();
```

프록시를 통해 전달된 모든 클라이언트 IP 주소를 배열로 받고 싶으면 `ips` 메서드를 사용하세요. 이때 "원래" 클라이언트 IP는 배열의 마지막에 위치합니다:

```
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는 사용자 입력으로 간주하고, 참고 정보 용도로만 사용하는 것이 안전합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상 (Content Negotiation)

Laravel은 요청의 `Accept` 헤더를 검사하는 다양한 메서드를 제공합니다. `getAcceptableContentTypes` 메서드는 요청에 허용된 모든 MIME 타입의 배열을 반환합니다:

```
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 MIME 타입 배열을 받으며, 요청이 이 중 하나라도 허용하면 `true`를 반환합니다:

```
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 요청에 가장 선호되는 MIME 타입을 반환합니다. 요청이 제공된 타입 중 어떤 것도 허용하지 않을 경우 `null`을 리턴합니다:

```
$preferred = $request->prefers(['text/html', 'application/json']);
```

대부분 애플리케이션은 HTML 또는 JSON만 제공하므로, `expectsJson` 메서드로 간단히 JSON 응답을 기대하는지 확인할 수 있습니다:

```
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청 (PSR-7 Requests)

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지 인터페이스를 규정하며, 요청과 응답을 모두 포함합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고자 한다면, 아래 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 Laravel 요청과 응답을 PSR-7 호환 구현으로 변환합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리를 설치 후, 라우트 클로저나 컨트롤러 메서드에서 PSR-7 요청 인터페이스를 타입힌트하면 됩니다:

```
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]  
> 만약 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, Laravel이 이를 자동으로 Laravel 응답 인스턴스로 변환하여 처리합니다.

<a name="input"></a>
## 입력 (Input)

<a name="retrieving-input"></a>
### 입력 데이터 가져오기 (Retrieving Input)

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기 (Retrieving All Input Data)

`all` 메서드로 HTML 폼이든 XHR 요청이든 상관없이 요청에 포함된 모든 입력 데이터를 `array`로 가져올 수 있습니다:

```
$input = $request->all();
```

`collect` 메서드는 모든 입력 데이터를 [컬렉션](/docs/10.x/collections) 형태로 반환합니다:

```
$input = $request->collect();
```

부분적으로 입력 데이터를 컬렉션으로 가져올 수도 있습니다:

```
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 특정 입력 값 가져오기 (Retrieving an Input Value)

HTTP 메서드와 상관없이 `input` 메서드를 써서 입력 값을 가져올 수 있습니다:

```
$name = $request->input('name');
```

두 번째 인자로 기본값을 전달할 수 있는데, 요청에 해당 값이 없을 때 반환됩니다:

```
$name = $request->input('name', 'Sally');
```

배열 형식 입력에는 'dot' 표기법을 사용합니다:

```
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

`input` 메서드를 인자 없이 호출하면 모든 입력 데이터를 연관 배열로 반환합니다:

```
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력 값 가져오기 (Retrieving Input From the Query String)

`input` 메서드는 요청 본문과 쿼리 문자열을 모두 조회하지만, `query` 메서드는 쿼리 문자열에서만 값을 가져옵니다:

```
$name = $request->query('name');
```

기본값도 두 번째 인자로 줄 수 있습니다:

```
$name = $request->query('name', 'Helen');
```

`query` 메서드에 인자를 주지 않으면 모든 쿼리 문자열 값을 배열로 반환합니다:

```
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력 값 가져오기 (Retrieving JSON Input Values)

JSON 요청의 `Content-Type` 헤더가 `application/json`으로 정확히 설정됐다면, `input` 메서드로 JSON 데이터에 접근할 수 있습니다. 또한 중첩된 JSON 객체/배열도 'dot' 표기법으로 접근 가능합니다:

```
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### 스트링 처리 가능한 입력 값 가져오기 (Retrieving Stringable Input Values)

일반 문자열 대신 [`Illuminate\Support\Stringable`](/docs/10.x/helpers#fluent-strings) 인스턴스로 가져오려면 `string` 메서드를 사용하세요:

```
$name = $request->string('name')->trim();
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력 값 가져오기 (Retrieving Boolean Input Values)

체크박스 같은 HTML 요소는 "true"나 "on" 같은 문자열로 값을 보내기도 합니다. `boolean` 메서드는 이 값을 편리하게 불리언 타입으로 변환합니다. 이 메서드는 `1`, `"1"`, `true`, `"true"`, `"on"`, `"yes"` 등에 대해 `true`를 반환하고, 그 외는 `false`를 반환합니다:

```
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력 값 가져오기 (Retrieving Date Input Values)

날짜나 시간을 포함한 입력 값을 [`Carbon`](https://carbon.nesbot.com/) 인스턴스로 편리하게 가져오려면 `date` 메서드를 사용하세요. 해당 이름의 입력 값이 없으면 `null`이 반환됩니다:

```
$birthday = $request->date('birthday');
```

`date` 메서드는 두 번째, 세 번째 인자로 날짜 포맷과 타임존도 받을 수 있습니다:

```
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 존재하지만 포맷이 잘못되면 `InvalidArgumentException`이 발생하므로, 미리 유효성 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력 값 가져오기 (Retrieving Enum Input Values)

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php) 타입으로 매핑되는 입력 값도 가져올 수 있습니다. 입력에 해당 값이 없거나 enum이 백업 값에 일치하지 않으면 `null` 반환합니다. `enum` 메서드는 입력 이름과 enum 클래스 이름을 인자로 받습니다:

```
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성으로 입력 값 가져오기 (Retrieving Input via Dynamic Properties)

`Illuminate\Http\Request` 인스턴스의 동적 속성을 사용해 입력 값에 접근할 수도 있습니다. 예를 들어 폼에 `name` 필드가 있다면 다음처럼 쓸 수 있습니다:

```
$name = $request->name;
```

동적 속성 사용 시 Laravel은 먼저 요청 본문에서 해당 값을 찾으며, 없으면 매칭된 라우트 매개변수에서 찾아 반환합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 일부 입력 데이터 가져오기 (Retrieving a Portion of the Input Data)

입력 데이터 중 일부만 선별적으로 가져오려면 `only`, `except` 메서드를 사용합니다. 둘 다 배열이나 동적 인자 목록을 받을 수 있습니다:

```
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]  
> `only` 메서드는 요청에 실제로 존재하는 키만 반환하며, 존재하지 않는 키는 결과에 포함하지 않습니다.

<a name="input-presence"></a>
### 입력 존재 여부 (Input Presence)

`has` 메서드는 요청에 입력 값이 존재하는지 여부를 판단합니다. 존재하면 `true`를 반환합니다:

```
if ($request->has('name')) {
    // ...
}
```

배열을 인자로 넘기면 모든 지정된 값이 있는지 확인합니다:

```
if ($request->has(['name', 'email'])) {
    // ...
}
```

반면 `hasAny` 메서드는 지정된 값 중 하나라도 존재하면 `true`를 반환합니다:

```
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 입력 값이 존재할 때 콜백을 실행합니다:

```
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 콜백을 전달하면, 입력 값이 없을 때 실행합니다:

```
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재...
}, function () {
    // "name" 값이 없음...
});
```

입력 값이 존재하고 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용합니다:

```
if ($request->filled('name')) {
    // ...
}
```

`anyFilled` 메서드는 지정된 값 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다:

```
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 입력 값이 빈 문자열이 아닐 때 콜백을 실행합니다:

```
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 콜백은 "filled"가 아닐 때 실행합니다:

```
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져 있음...
}, function () {
    // "name" 값이 채워져 있지 않음...
});
```

키가 요청에 없음을 판단하려면 `missing` 및 `whenMissing` 메서드를 사용하세요:

```
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function (array $input) {
    // "name" 값이 없음...
}, function () {
    // "name" 값 있음...
});
```

<a name="merging-additional-input"></a>
### 추가 입력 병합하기 (Merging Additional Input)

요청 입력 데이터에 수동으로 값을 추가하거나 덮어쓰려면 `merge` 메서드를 사용하세요. 이미 존재하는 키는 덮어쓰게 됩니다:

```
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 요청에 없는 키에 대해서만 병합합니다:

```
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력 데이터 (Old Input)

Laravel은 한 요청에서 받은 입력을 다음 요청까지 유지할 수 있게 해줍니다. 이 기능은 주로 유효성 검증 실패 후 폼을 다시 채우는데 유용합니다. Laravel 내장 [유효성 검증 기능](/docs/10.x/validation)을 사용하면 직접 세션 입력 플래싱을 호출하지 않아도 자동으로 처리해줍니다.

<a name="flashing-input-to-the-session"></a>
#### 입력 세션에 플래시하기 (Flashing Input to the Session)

`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력 데이터를 [세션](/docs/10.x/session)에 저장해 다음 요청 시 사용할 수 있게 합니다:

```
$request->flash();
```

`flashOnly`, `flashExcept` 메서드를 사용하면 세션에 플래시할 입력의 일부만 지정할 수 있어, 예를 들어 비밀번호 같은 민감 정보는 제외할 때 유용합니다:

```
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력 플래시 후 리다이렉트 (Flashing Input Then Redirecting)

입력 데이터를 세션에 플래시한 뒤 이전 페이지로 리다이렉트할 때는 `withInput` 메서드를 체이닝하면 됩니다:

```
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력 데이터 가져오기 (Retrieving Old Input)

이전 요청에서 플래시된 입력값은 `Illuminate\Http\Request` 인스턴스의 `old` 메서드로 가져올 수 있습니다. 이 메서드는 이전 요청에서 세션에 저장된 입력 데이터를 반환합니다:

```
$username = $request->old('username');
```

Blade 템플릿 안에서는 글로벌 헬퍼 함수 `old`를 사용하는 편이 더 편리합니다. 값이 없으면 `null`이 반환됩니다:

```
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기 (Retrieving Cookies From Requests)

Laravel이 생성한 모든 쿠키는 암호화되고 인증 코드로 서명되어, 클라이언트가 조작한 경우 무효 처리됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 쓰면 됩니다:

```
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력 트리밍 및 정규화 (Input Trimming and Normalization)

기본적으로 Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `App\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어는 요청의 모든 문자열 입력 값을 자동으로 트리밍하고, 빈 문자열은 `null`로 변환합니다. 덕분에 라우트나 컨트롤러에서 이러한 정규화 문제를 신경 쓰지 않아도 됩니다.

#### 입력 정규화 비활성화

모든 요청에 대해 이 동작을 비활성화하려면, 애플리케이션 미들웨어 스택에서 두 미들웨어를 제거하면 됩니다. `App\Http\Kernel` 클래스의 `$middleware` 속성에서 해당 미들웨어를 빼주세요.

특정 요청에 대해서만 문자열 트리밍과 빈 문자열 변환을 비활성화하려면 미들웨어가 제공하는 `skipWhen` 메서드를 사용하세요. 이 메서드는 `true` 또는 `false`를 반환하는 클로저를 인자로 받으며, 일반적으로 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에서 호출합니다.

```php
use App\Http\Middleware\TrimStrings;
use Illuminate\Http\Request;
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    TrimStrings::skipWhen(function (Request $request) {
        return $request->is('admin/*');
    });

    ConvertEmptyStringsToNull::skipWhen(function (Request $request) {
        // ...
    });
}
```

<a name="files"></a>
## 파일 (Files)

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기 (Retrieving Uploaded Files)

`Illuminate\Http\Request` 인스턴스의 `file` 메서드나 동적 속성을 사용해 업로드된 파일을 가져올 수 있습니다. `file` 메서드는 PHP `SplFileInfo` 클래스를 확장한 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 파일 조작을 위한 다양한 메서드를 제공합니다:

```
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드를 사용하면 요청에 파일이 포함되어 있는지 확인할 수 있습니다:

```
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증하기 (Validating Successful Uploads)

파일 존재 여부 외에도 `isValid` 메서드로 파일 업로드가 문제없이 완료되었는지 확인할 수 있습니다:

```
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자 (File Paths and Extensions)

`UploadedFile` 클래스는 파일의 전체 경로와 확장자를 가져오는 메서드도 제공합니다. `extension` 메서드는 클라이언트가 보낸 확장자와 다를 수 있는 파일 내용 기반 추정 확장자를 반환합니다:

```
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 관련 메서드 (Other File Methods)

`UploadedFile`에 관한 자세한 메서드는 [API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기 (Storing Uploaded Files)

파일을 저장하려면 보통 설정된 [파일 시스템](/docs/10.x/filesystem)을 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 디스크(로컬 파일 시스템이나 Amazon S3 같은 클라우드 저장소)로 이동시킵니다.

`store` 메서드는 파일을 저장할 경로를 디스크의 루트 디렉토리를 기준으로 받으며, 파일명은 자동으로 고유 ID가 생성되어 처리됩니다.

디스크 이름은 두 번째 인자로 선택적으로 지정할 수 있으며, 메서드는 디스크 루트 기준 경로를 반환합니다:

```
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

자동으로 파일명이 생성되는 걸 원하지 않는다면 `storeAs` 메서드를 사용하세요. 경로, 파일 이름, 디스크 이름을 인자로 받습니다:

```
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]  
> 파일 저장에 대해 더 자세한 내용은 Laravel의 [파일 저장 문서](/docs/10.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰하는 프록시 설정하기 (Configuring Trusted Proxies)

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼를 이용해도 HTTPS 링크가 아닌 HTTP 링크가 생성될 수 있습니다. 이는 로드 밸런서가 포트 80으로 트래픽을 전달하기 때문입니다.

이를 해결하기 위해 Laravel은 `App\Http\Middleware\TrustProxies` 미들웨어를 제공합니다. 이 미들웨어를 사용해 애플리케이션에서 신뢰할 프록시나 로드 밸런서를 빠르게 설정할 수 있습니다. 신뢰하는 프록시 주소는 `$proxies` 배열로 지정합니다. 아울러 신뢰할 프록시 헤더를 `$headers` 속성에 설정할 수 있습니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * 이 애플리케이션에서 신뢰하는 프록시들
     *
     * @var string|array
     */
    protected $proxies = [
        '192.168.1.1',
        '192.168.1.2',
    ];

    /**
     * 프록시 감지를 위해 사용할 헤더들
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_FOR | Request::HEADER_X_FORWARDED_HOST | Request::HEADER_X_FORWARDED_PORT | Request::HEADER_X_FORWARDED_PROTO;
}
```

> [!NOTE]  
> AWS Elastic Load Balancing을 사용하는 경우 `$headers`는 `Request::HEADER_X_FORWARDED_AWS_ELB`로 설정해야 합니다. `$headers`에 사용 가능한 상수 목록은 Symfony의 [프록시 신뢰 설정 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기 (Trusting All Proxies)

Amazon AWS나 기타 클라우드 로드 밸런서를 사용한다면 실제 프록시 IP를 모를 수 있습니다. 이 경우 `*`로 모든 프록시를 신뢰하도록 지정할 수 있습니다:

```
/**
 * 이 애플리케이션에서 신뢰하는 프록시들
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
## 신뢰하는 호스트 설정하기 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계 없이 모든 요청에 응답하며, 응답 시 절대 URL 생성에 이 헤더를 사용합니다.

보통은 웹 서버(Nginx, Apache 등)에서 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 전달하도록 설정하는 것이 좋습니다. 하지만 서버 직접 설정이 불가능할 때는 Laravel에서 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하여 특정 호스트에 대해서만 응답하도록 제한할 수 있습니다.

`TrustHosts` 미들웨어는 이미 애플리케이션의 `$middleware` 스택에 포함되어 있지만, 기본 상태는 주석 처리되어 있어 활성화하려면 주석을 해제해야 합니다. 이 미들웨어 내부의 `hosts` 메서드에 응답을 허용할 호스트 이름을 명시합니다. 다른 `Host` 헤더 값을 가진 요청은 거부됩니다:

```
/**
 * 신뢰할 호스트 패턴 반환
 *
 * @return array<int, string>
 */
public function hosts(): array
{
    return [
        'laravel.test',
        $this->allSubdomainsOfApplicationUrl(),
    ];
}
```

`allSubdomainsOfApplicationUrl` 헬퍼는 `app.url` 설정 값의 모든 서브도메인과 매칭되는 정규식을 반환합니다. 와일드카드 서브도메인을 활용하는 애플리케이션에서 매우 편리하게 사용할 수 있습니다.