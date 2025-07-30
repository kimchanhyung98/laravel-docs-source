# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [Request와 상호작용하기](#interacting-with-the-request)
    - [Request 인스턴스 접근하기](#accessing-the-request)
    - [Request 경로, 호스트, 메서드](#request-path-and-method)
    - [Request 헤더](#request-headers)
    - [Request IP 주소](#request-ip-address)
    - [컨텐츠 네고시에이션](#content-negotiation)
    - [PSR-7 Requests](#psr7-requests)
- [입력값 (Input)](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 존재 여부](#input-presence)
    - [추가 입력값 병합하기](#merging-additional-input)
    - [이전 입력값 (Old Input)](#old-input)
    - [쿠키 (Cookies)](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일 (Files)](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 처리 중인 현재 HTTP 요청과 상호작용하고 요청과 함께 전달된 입력값, 쿠키, 파일을 객체지향적으로 다룰 수 있도록 합니다.

<a name="interacting-with-the-request"></a>
## Request와 상호작용하기

<a name="accessing-the-request"></a>
### Request 인스턴스 접근하기

현재 HTTP 요청 인스턴스를 의존성 주입 방식으로 얻으려면, 라우트 클로저나 컨트롤러 메서드에 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. 라라벨 서비스 컨테이너가 자동으로 요청 인스턴스를 주입해 줍니다:

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

앞서 말했듯이 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트할 수 있습니다. 서비스 컨테이너가 클로저 실행 시 자동으로 요청 인스턴스를 주입합니다:

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 매개변수

컨트롤러 메서드에서 라우트 파라미터도 기대하는 경우, 라우트 매개변수를 다른 의존성 뒤에 명시해야 합니다. 예를 들어, 다음처럼 라우트를 정의한 경우:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

`Illuminate\Http\Request`를 타입힌트하고 `id` 라우트 매개변수도 아래와 같이 정의할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 특정 사용자 업데이트
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트 처리...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### Request 경로, 호스트, 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하는 다양한 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서 가장 중요한 몇 가지 메서드를 다룹니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 요청 URL이 `http://example.com/foo/bar` 라면 `path` 메서드는 `foo/bar` 를 반환합니다:

```
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사하기

`is` 메서드는 요청 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 와일드카드 `*` 문자를 사용할 수 있습니다:

```
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면 현재 요청이 [이름 있는 라우트](/docs/11.x/routing#named-routes)와 일치하는지도 확인할 수 있습니다:

```
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용하세요. `url`은 쿼리 스트링을 제외한 URL을 반환하며, `fullUrl`은 쿼리 스트링까지 포함합니다:

```
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

쿼리 스트링에 데이터를 추가하려면 `fullUrlWithQuery` 메서드를 호출합니다. 이 메서드는 배열 형태의 쿼리 파라미터를 현재 쿼리 스트링과 병합합니다:

```
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 파라미터 없이 현재 URL을 얻고 싶을 때는 `fullUrlWithoutQuery` 메서드를 사용하세요:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### Request 호스트 가져오기

`host`, `httpHost`, `schemeAndHttpHost` 메서드로 요청 호스트 정보를 가져올 수 있습니다:

```
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기

`method` 메서드는 요청의 HTTP 메서드(verb)를 반환합니다. `isMethod` 메서드를 사용해 특정 메서드인지 확인할 수 있습니다:

```
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드로 요청 헤더를 가져올 수 있습니다. 요청에 헤더가 없으면 `null`을 반환하고, 두 번째 인수로 기본값을 지정할 수 있습니다:

```
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 특정 헤더가 요청에 포함되어 있는지 확인합니다:

```
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편리하게, `bearerToken` 메서드는 `Authorization` 헤더에서 Bearer 토큰을 가져옵니다. 헤더가 없으면 빈 문자열을 반환합니다:

```
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드를 사용해 요청을 보낸 클라이언트 IP 주소를 얻을 수 있습니다:

```
$ipAddress = $request->ip();
```

프록시가 전달한 모든 클라이언트 IP 주소 배열을 얻으려면 `ips` 메서드를 사용하세요. 배열 맨 끝에 실제 "원래" 클라이언트 IP 주소가 들어있습니다:

```
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는, 사용자가 제어하는 입력으로 간주하고 정보용으로만 활용해야 합니다.

<a name="content-negotiation"></a>
### 컨텐츠 네고시에이션

Laravel은 `Accept` 헤더를 기반으로 요청된 컨텐츠 타입을 검사하는 여러 메서드를 제공합니다. `getAcceptableContentTypes` 메서드는 요청이 수락 가능한 모든 컨텐츠 타입을 배열로 반환합니다:

```
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 전달된 컨텐츠 타입 배열 중 하나라도 요청이 수락할 경우 `true`를 반환합니다:

```
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 제공된 컨텐츠 타입 배열 중 요청에서 가장 선호하는 타입을 반환합니다. 없으면 `null` 반환:

```
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션은 HTML 또는 JSON만 제공합니다. `expectsJson` 메서드는 요청이 JSON 응답을 기대하는지 단순히 확인할 때 유용합니다:

```
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 Requests

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청과 응답을 포함하는 HTTP 메시지 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻으려면 몇 가지 라이브러리를 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 일반 Laravel 요청/응답을 PSR-7 호환 객체로 변환합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

설치 후, 라우트 클로저 또는 컨트롤러 메서드에서 PSR-7 요청 인터페이스를 타입힌트하여 사용할 수 있습니다:

```
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]  
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면 Laravel이 자동으로 다시 Laravel 응답 객체로 변환하여 응답합니다.

<a name="input"></a>
## 입력값 (Input)

<a name="retrieving-input"></a>
### 입력값 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 가져오기

`all` 메서드로 들어오는 요청의 모든 입력을 `array` 형태로 가져올 수 있습니다. HTML 폼 요청이나 XHR 요청 모두에 사용할 수 있습니다:

```
$input = $request->all();
```

`collect` 메서드로 모든 입력값을 [컬렉션](/docs/11.x/collections)으로도 가져올 수 있습니다:

```
$input = $request->collect();
```

`collect` 메서드는 입력값 일부만 선택해 컬렉션으로 가져올 수도 있습니다:

```
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 개별 입력값 가져오기

HTTP 메서드에 상관없이 `input` 메서드로 사용자의 입력값을 얻을 수 있습니다:

```
$name = $request->input('name');
```

두 번째 인자로 기본값을 넘기면, 해당 입력값이 없을 때 그 값이 반환됩니다:

```
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값도 "점(dot)" 문법으로 접근할 수 있습니다:

```
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

`input` 메서드에 아무 인자를 넘기지 않으면 모든 입력값을 연관 배열로 반환합니다:

```
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 가져오기

`input`이 요청 전체 페이로드에서 값을 가져오는 반면, `query` 메서드는 쿼리 스트링에서만 값을 가져옵니다:

```
$name = $request->query('name');
```

요청에 해당 쿼리 파라미터가 없으면 두 번째 인자로 기본값을 지정할 수 있습니다:

```
$name = $request->query('name', 'Helen');
```

아무 인자 없이 호출하면 모든 쿼리 스트링 데이터를 연관 배열로 반환합니다:

```
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

JSON 요청을 처리할 때 `Content-Type` 헤더가 `application/json`으로 적절히 설정되어 있으면 `input` 메서드로 JSON 데이터를 접근할 수 있습니다. 중첩된 JSON 배열이나 객체 내부 값도 "점" 문법으로 접근 가능합니다:

```
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 객체로 입력값 가져오기

입력을 문자열(`string`) 대신 [`Illuminate\Support\Stringable`](/docs/11.x/strings) 인스턴스로 가져오려면 `string` 메서드를 사용하세요:

```
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 가져오기

`integer` 메서드는 입력값을 정수형으로 캐스팅 시도해서 반환합니다. 입력이 없거나 캐스팅이 실패하면 기본값을 반환합니다. 페이징 같은 숫자형 입력에 유용합니다:

```
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기

HTML 체크박스처럼 "true", "on" 같은 문자열로 전달되는 진릿값을 불리언으로 쉽게 가져오려면 `boolean` 메서드를 사용하세요. 1, "1", true, "true", "on", "yes" 는 `true`, 나머지는 `false`로 변환합니다:

```
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜/시간 형식의 입력값은 `date` 메서드를 이용해 Carbon 인스턴스로 편리하게 가져올 수 있습니다. 값이 없으면 `null` 반환:

```
$birthday = $request->date('birthday');
```

두 번째와 세 번째 인자로 날짜 포맷과 타임존을 지정할 수 있습니다:

```
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

형식이 맞지 않으면 `InvalidArgumentException` 예외가 발생합니다. 따라서 `date` 호출 전 입력값을 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### enum 입력값 가져오기

PHP [enum](https://www.php.net/manual/en/language.types.enumerations.php)에 대응하는 값도 가져올 수 있습니다. 해당 이름의 입력값이 없거나 enum에 해당하는 값이 없으면 `null` 반환합니다. `enum` 메서드는 입력 이름과 enum 클래스를 인자로 받습니다:

```
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

배열로 된 enum 입력값은 `enums` 메서드를 사용해 enum 인스턴스 배열로 가져올 수 있습니다:

```
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성으로 입력값 가져오기

`Illuminate\Http\Request` 인스턴스의 동적 속성으로도 입력값에 접근할 수 있습니다. 예를 들어 폼에 `name` 필드가 있으면 다음과 같이 값을 가져올 수 있습니다:

```
$name = $request->name;
```

동적 속성 사용 시 Laravel은 먼저 요청 페이로드에서 값을 찾고, 없으면 매칭된 라우트의 매개변수에서 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값 일부만 가져오기

입력값의 일부만 필요하다면 `only`와 `except` 메서드를 사용하세요. 두 메서드는 배열이나 가변 인자를 받습니다:

```
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]  
> `only`는 요청 안에 있는 키/값만 반환하며, 요청에 없는 키/값은 반환하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 여부

`has` 메서드는 요청에 특정 값이 존재하면 `true`를 반환합니다:

```
if ($request->has('name')) {
    // ...
}
```

배열을 주면 모든 값의 존재 여부를 확인합니다:

```
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny`는 지정한 값 중 하나라도 존재하면 `true`를 반환합니다:

```
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas`는 값이 존재할 때 주어진 클로저를 실행합니다:

```
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘기면 값이 없을 때 실행됩니다:

```
$request->whenHas('name', function (string $input) {
    // "name" 값이 있음
}, function () {
    // "name" 값이 없음
});
```

값이 존재하고 빈 문자열이 아닐 때를 확인하려면 `filled` 메서드를 사용하세요:

```
if ($request->filled('name')) {
    // ...
}
```

값이 없거나 빈 문자열일 때는 `isNotFilled` 메서드를 사용합니다:

```
if ($request->isNotFilled('name')) {
    // ...
}
```

배열로 주면 모든 값이 없거나 빈 문자열인지 확인합니다:

```
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled`는 주어진 값 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다:

```
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled`는 값이 "채워져" 있을 때 클로저를 실행합니다:

```
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저는 값이 없거나 비어있을 때 실행됩니다:

```
$request->whenFilled('name', function (string $input) {
    // "name" 값이 있음
}, function () {
    // "name" 값이 없음
});
```

키가 요청에서 없음을 확인하려면 `missing`과 `whenMissing` 메서드를 사용하세요:

```
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
### 추가 입력값 병합하기

기존 요청 입력값에 새로운 입력값을 수동으로 병합하려면 `merge` 메서드를 사용합니다. 기존에 있는 키는 덮어씁니다:

```
$request->merge(['votes' => 0]);
```

`mergeIfMissing`은 요청에 키가 없을 경우에만 입력을 병합합니다:

```
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값 (Old Input)

Laravel은 한 요청의 입력을 다음 요청으로 "플래시(flash)"하여 유지할 수 있습니다. 이는 검증 오류 발생 후 폼을 다시 채울 때 매우 유용합니다. Laravel 내장 [검증 기능](/docs/11.x/validation)을 사용하면 직접 세션 입력 깜박임 기능을 쓸 필요가 거의 없습니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 깜박이기

`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력값을 [세션](/docs/11.x/session)에 잠시 저장해 다음 요청에서 사용할 수 있게 합니다:

```
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드는 일부 입력값만 깜박이도록 하는 데 유용합니다. 비밀번호 같은 민감한 정보가 세션에 저장되는 걸 방지할 수 있습니다:

```
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값을 세션에 깜박이고 리다이렉트하기

입력값을 세션에 깜박이고 이전 페이지로 리다이렉트하는 일이 흔하므로 `withInput` 메서드를 사용해 간단히 체이닝할 수 있습니다:

```
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

이전 요청에서 세션으로 깜박인 입력값은 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드로 가져올 수 있습니다. 세션에서 이전 입력값을 꺼냅니다:

```
$username = $request->old('username');
```

Blade 템플릿에서라면 전역 `old` 헬퍼를 사용하는 것이 편리하며, 해당 필드의 이전 입력값이 없으면 `null`을 반환합니다:

```
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel에서 생성한 모든 쿠키는 암호화되고 인증 코드로 서명됩니다. 클라이언트가 임의로 변경 시 무효 처리됩니다. 요청에서 특정 쿠키 값을 가져오려면 `Illuminate\Http\Request`의 `cookie` 메서드를 사용하세요:

```
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

기본적으로 Laravel은 `Illuminate\Foundation\Http\Middleware\TrimStrings` 와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 글로벌 미들웨어 스택에 포함해, 모든 입력 문자열 필드를 자동으로 트리밍하고 빈 문자열을 `null`로 변환합니다. 덕분에 라우트나 컨트롤러에서 이런 처리 걱정 없이 코딩할 수 있습니다.

#### 입력값 정규화 비활성화

모든 요청에 대해 이 기능을 끄려면, `bootstrap/app.php`에서 `$middleware->remove` 메서드를 호출해 두 미들웨어를 제거하세요:

```
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware) {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

특정 요청에 대해서만 입력값 정규화를 비활성화하려면 `trimStrings`와 `convertEmptyStringsToNull` 메서드를 사용해, 각각의 인자로 클로저 배열을 넘기고 `true` 또는 `false`를 반환해 스킵 여부를 결정할 수 있습니다:

```
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
### 업로드된 파일 가져오기

`Illuminate\Http\Request` 인스턴스의 `file` 메서드 또는 동적 속성으로 업로드된 파일을 가져올 수 있습니다. 반환되는 `UploadedFile` 클래스는 PHP `SplFileInfo`를 확장하며 파일 조작을 위한 여러 메서드를 제공합니다:

```
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드로 파일 존재 여부를 확인할 수 있습니다:

```
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증하기

파일이 실제로 성공적으로 업로드됐는지 검증하려면 `isValid` 메서드를 사용하세요:

```
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로와 확장자

`UploadedFile` 클래스는 파일의 전체 경로와 확장자를 가져오는 메서드를 갖고 있습니다. `extension` 메서드는 파일 내용 분석을 통해 확장자를 추측하며, 클라이언트가 보낸 확장자와 다를 수 있습니다:

```
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 클래스에 이 외에도 다양한 메서드가 있습니다. 자세한 정보는 [API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일은 보통 설정한 [파일시스템](/docs/11.x/filesystem) 중 하나에 저장합니다. `UploadedFile`의 `store` 메서드는 업로드된 파일을 지정한 디스크에 옮겨 저장하는데 사용하며, 로컬 파일 시스템이나 Amazon S3 같은 클라우드 저장소 일 수 있습니다.

`store` 메서드는 파일 경로(디스크 루트 기준, 파일명 제외)를 인자로 받으며, 고유 ID가 자동으로 생성되어 파일명으로 사용됩니다.

두 번째 인자로는 사용할 디스크 이름을 넘길 수 있습니다. 파일 저장 후 디스크 루트 기준으로 경로를 반환합니다:

```
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

자동으로 파일명을 생성하지 않고 직접 지정하려면 `storeAs` 메서드를 사용하며, 경로, 파일명, 디스크 이름을 인자로 받습니다:

```
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]  
> Laravel의 파일 저장에 대한 자세한 내용은 [파일 저장 문서](/docs/11.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서 종료 기능이 있는 로드 밸런서 뒤에서 애플리케이션을 운영하는 경우, `url` 헬퍼가 HTTPS 링크를 생성하지 않는 문제가 발생할 수 있습니다. 이는 로드 밸런서가 포트 80에서 트래픽을 전달해주기 때문에 애플리케이션이 안전한 링크 생성 여부를 알지 못하기 때문입니다.

이 문제를 해결하려면 Laravel에 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화해서 신뢰할 프록시 목록을 지정하세요. `bootstrap/app.php`에서 `trustProxies` 미들웨어 메서드에 신뢰할 프록시 IP 또는 CIDR 범위를 넘기면 됩니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 프록시 외에도, 신뢰할 프록시가 전달하는 헤더 유형을 설정할 수도 있습니다:

```
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
> AWS Elastic Load Balancing을 사용하는 경우 헤더 값은 `Request::HEADER_X_FORWARDED_AWS_ELB` 이어야 합니다. 표준 `Forwarded` 헤더 ([RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4))를 사용한다면 `Request::HEADER_FORWARDED` 로 설정하세요. 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [trusting proxies 문서](https://symfony.com/doc/7.0/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS 등 클라우드 로드 밸런서의 실제 IP를 모르는 경우, 와일드카드 `*`를 사용해 모든 프록시를 신뢰할 수 있습니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 모든 요청에 응답합니다. 또한 웹 요청 중 절대 URL을 생성할 때 이 `Host` 값을 사용합니다.

일반적으로는 Nginx나 Apache 같은 웹 서버에서 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 전달하도록 설정해야 합니다. 하지만 웹 서버를 직접 설정할 수 없고, Laravel에서 특정 호스트 이름에 대해서만 응답하려면 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화하세요.

`bootstrap/app.php`에서 `trustHosts` 미들웨어 메서드를 호출해 신뢰할 호스트명을 `at` 인자로 지정합니다. 지정하지 않은 `Host` 헤더를 가진 요청은 거부됩니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test']);
})
```

기본적으로 애플리케이션 URL의 서브도메인도 신뢰합니다. 이를 비활성화하려면 `subdomains` 인수를 `false`로 설정하세요:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
})
```

설정 파일이나 데이터베이스에서 신뢰할 호스트 목록을 가져와야 한다면, `at` 인자에 클로저를 넘길 수 있습니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```