# HTTP 요청

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 접근](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력](#input)
    - [입력값 조회](#retrieving-input)
    - [입력 존재 유무](#input-presence)
    - [추가 입력 병합](#merging-additional-input)
    - [이전 입력](#old-input)
    - [쿠키](#cookies)
    - [입력값 다듬기와 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드 파일 조회](#retrieving-uploaded-files)
    - [업로드 파일 저장](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션이 처리 중인 현재 HTTP 요청과 객체지향적으로 상호작용하고, 요청과 함께 제출된 입력값, 쿠키, 파일 등을 조회할 수 있는 방법을 제공합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청 접근

의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면 라우트 클로저나 컨트롤러 메소드에서 `Illuminate\Http\Request` 클래스를 타입힌트 하면 됩니다. 들어오는 요청 인스턴스는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 주입됩니다.

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

        // 사용자 저장...

        return redirect('/users');
    }
}
```

말씀드린 대로, 라우트 클로저에도 `Illuminate\Http\Request`를 타입힌트할 수 있습니다. 서비스 컨테이너가 해당 클로저 실행 시 요청을 자동으로 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메소드에서 입력값과 함께 라우트 파라미터도 기대한다면, 라우트 파라미터를 다른 의존성 뒤에 나열해야 합니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메소드는 다음처럼 정의할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정한 사용자를 수정합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 수정...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하는 다양한 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 여기서는 가장 중요한 일부 메서드를 다룹니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 얻기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어 요청이 `http://example.com/foo/bar`로 들어오면, `path`는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사하기

`is` 메서드는 요청 경로가 주어진 패턴과 일치하는지 확인합니다. 이 메서드에서 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면 들어온 요청이 [네임드 라우트](/docs/{{version}}/routing#named-routes)와 일치하는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 얻기

들어온 요청의 전체 URL을 얻으려면 `url` 혹은 `fullUrl` 메서드를 사용할 수 있습니다. `url`은 쿼리 스트링 제외, `fullUrl`은 쿼리 스트링을 포함합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 스트링 데이터를 추가하려면 `fullUrlWithQuery` 메서드를 사용합니다. 이 메서드는 주어진 배열을 기존 쿼리 스트링과 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 파라미터를 제외한 현재 URL을 얻고 싶다면 `fullUrlWithoutQuery` 메서드를 사용하세요.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 얻기

들어온 요청의 "호스트"를 얻으려면 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용할 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 얻기

`method` 메서드는 요청의 HTTP 메서드를 반환합니다. `isMethod` 메서드로 메서드 일치 여부를 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

요청에서 헤더를 얻으려면 `header` 메서드를 사용할 수 있습니다. 헤더가 없다면 `null`이 반환됩니다. 두 번째 인자로 기본값을 줄 수도 있습니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 헤더 존재 여부를 검사합니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의상 `bearerToken` 메서드를 이용해 `Authorization` 헤더에서 Bearer 토큰을 쉽게 얻을 수 있습니다. 없으면 빈 문자열이 반환됩니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드는 요청을 보낸 클라이언트의 IP를 반환합니다.

```php
$ipAddress = $request->ip();
```

프록시를 통해 전달된 모든 클라이언트 IP 주소 배열을 얻으려면 `ips` 메서드를 사용하세요. "원본" 클라이언트 IP는 배열 끝에 위치합니다.

```php
$ipAddresses = $request->ips();
```

일반적으로, IP 주소는 신뢰할 수 없는 사용자 제어 입력이므로 정보 제공 용도로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 요청의 `Accept` 헤더를 통해 요청된 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. `getAcceptableContentTypes` 메서드는 요청에서 허용하는 모든 콘텐츠 타입의 배열을 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 받아, 이 중 하나라도 요청에서 허용될 경우 `true`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드를 사용하면 주어진 콘텐츠 타입 배열 중 요청이 가장 선호하는 타입을 알 수 있습니다. 모두 없으면 `null` 반환.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML이나 JSON만 제공할 경우, `expectsJson` 메서드로 요청이 JSON 응답을 기대하는지 빠르게 판단할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청/응답)용 인터페이스를 지정합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻으려면 몇몇 라이브러리가 필요합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 전형적인 Laravel 요청/응답을 PSR-7 호환 구현체로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

설치 후, 라우트 클로저나 컨트롤러에서 PSR-7 요청 인터페이스를 타입힌트하면 PSR-7 요청을 받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]  
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 다시 Laravel 응답 인스턴스로 변환해 보여줍니다.

<a name="input"></a>
## 입력

<a name="retrieving-input"></a>
### 입력값 조회

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 조회

요청에 포함된 모든 입력 데이터를 `all` 메서드로 배열로 조회할 수 있습니다. HTML 폼이든 XHR 요청이든 사용 가능합니다.

```php
$input = $request->all();
```

모든 입력 데이터를 [컬렉션](/docs/{{version}}/collections)으로 조회하려면 `collect` 메서드를 사용합니다.

```php
$input = $request->collect();
```

컬렉션의 일부만 조회하고 싶다면, 키를 지정해 컬렉션으로 얻을 수 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 입력값 하나 조회

HTTP 메서드와 상관없이 `input` 메서드로 사용자 입력을 조회할 수 있습니다.

```php
$name = $request->input('name');
```

요청에 입력값이 없을 때 반환할 기본값을 두 번째 인자로 지정할 수 있습니다.

```php
$name = $request->input('name', 'Sally');
```

배열 형태의 입력값은 "점(.)" 표기법으로 접근할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인자 없이 `input()`을 호출하면 모든 입력값을 연관 배열로 반환합니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 조회

`input` 메서드는 전체 요청 페이로드(쿼리 스트링 포함)에서 값을 조회하지만, `query` 메서드는 오직 쿼리 스트링에서만 값을 조회합니다.

```php
$name = $request->query('name');
```

쿼리 스트링에 값이 없으면 두 번째 인자의 기본값이 반환됩니다.

```php
$name = $request->query('name', 'Helen');
```

인자 없이 `query()`를 호출하면 쿼리 스트링 전체를 연관 배열로 반환합니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 조회

JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 설정되어 있다면 `input` 메서드로 JSON 데이터에 접근할 수 있습니다. "점(.)" 표기법도 사용할 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 조회

입력값을 기본 문자열이 아닌 [`Illuminate\Support\Stringable`](/docs/{{version}}/helpers#fluent-strings) 인스턴스로 받고 싶다면 `string` 메서드를 이용하세요.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-boolean-input-values"></a>
#### 불린(Boolean) 입력값 조회

HTML 체크박스 등에서 "true", "on"과 같은 문자열로 "참" 값을 받을 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes" 값에 `true`를 반환합니다. 나머지는 모두 `false`를 반환합니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜/시간 입력값 조회

입력값이 날짜/시간이라면 `date` 메서드로 [Carbon](https://carbon.nesbot.com/) 인스턴스로 조회할 수 있습니다. 값이 없으면 `null`을 반환합니다.

```php
$birthday = $request->date('birthday');
```

두 번째, 세 번째 인자로 날짜 포맷과 타임존을 지정할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 존재하지만 형식이 올바르지 않으면 `InvalidArgumentException`이 발생하므로, `date` 호출 전 값의 유효성을 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 조회

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php) 값에 해당하는 입력도 조회할 수 있습니다. 값이 없거나 일치하는 Enum backing 값이 없으면 `null` 반환. 첫 번째 인자로 입력명, 두 번째 인자로 Enum 클래스를 전달합니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성으로 입력값 조회

`Illuminate\Http\Request`의 동적 속성을 통해서도 사용자 입력값에 접근할 수 있습니다. 예를 들어, 폼에 `name` 필드가 있으면 다음과 같이 조회합니다.

```php
$name = $request->name;
```

동적 속성을 사용할 때, Laravel은 우선 입력값에서 값을 찾고, 없으면 일치하는 라우트 파라미터에서 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터의 일부만 조회

입력 데이터 일부만 조회하려면 `only`와 `except` 메서드를 사용할 수 있습니다. 배열이나 나열된 인자로 키 목록을 넘길 수 있습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]  
> `only` 메서드는 요청에 존재하는 키/값만 반환합니다. 요청에 없는 키는 무시됩니다.

<a name="input-presence"></a>
### 입력 존재 유무

입력값이 요청에 존재하는지 확인하려면 `has` 메서드를 사용합니다. 값이 존재하면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 인자로 넘기면 모두 존재하는지 확인합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny`는 명시한 값들 중 하나라도 있으면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas`는 값이 존재하면 주어진 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘길 수 있으며, 값이 없으면 해당 클로저가 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재합니다...
}, function () {
    // "name" 값이 없습니다...
});
```

값이 존재하고 비어있지 않은 경우를 확인하려면 `filled`를 사용합니다.

```php
if ($request->filled('name')) {
    // ...
}
```

`anyFilled`는 지정된 값들 중 하나라도 비어있지 않으면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled`는 값이 존재하고 비어있지 않으면 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘기면 값이 "채워져있지 않은" 경우 실행됩니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져있음...
}, function () {
    // "name" 값이 비어있음...
});
```

주어진 키가 요청에 없는지 확인하려면 `missing`과 `whenMissing` 메서드를 사용합니다.

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function (array $input) {
    // "name" 값이 없습니다...
}, function () {
    // "name" 값이 있습니다...
});
```

<a name="merging-additional-input"></a>
### 추가 입력 병합

기존 요청 입력 데이터에 추가 입력 값을 수동으로 병합해야 할 때는 `merge` 메서드를 사용합니다. 이미 존재하는 키는 덮어씁니다.

```php
$request->merge(['votes' => 0]);
```

키가 요청에 없을 때만 병합하려면 `mergeIfMissing`을 사용하세요.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력

Laravel은 한 번의 요청에서 받은 입력을 다음 요청에서 사용할 수 있게 합니다. 이 기능은 유효성 검사 에러가 발생해 폼을 다시 채우고 싶을 때 유용합니다. 단, 기본 [유효성 검사 기능](/docs/{{version}}/validation)을 사용한다면, 직접 세션 입력 플래시 메서드를 호출할 필요가 없을 수도 있습니다. 기본 제공된 유효성 검사가 자동으로 호출해주기 때문입니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값 세션 플래싱

`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력값을 [세션](/docs/{{version}}/session)에 플래시해, 다음 요청에서도 사용할 수 있게 합니다.

```php
$request->flash();
```

`flashOnly`와 `flashExcept`를 사용하면 일부 입력값만 세션에 플래시할 수 있습니다. 비밀번호 등 민감한 정보를 세션에 남기지 않으려 할 때 유용합니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력 플래싱 후 리다이렉트

입력을 세션에 플래시한 다음 이전 페이지로 리다이렉트하는 경우가 많으므로, `withInput` 메서드를 리다이렉트와 체이닝해서 간단히 사용할 수 있습니다.

```php
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 조회

이전 요청에서 플래시된 입력을 조회하려면 `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출합니다. `old`는 세션에서 이전 입력값을 가져옵니다.

```php
$username = $request->old('username');
```

Blade 템플릿 내에서 이전 값을 표시할 때는 글로벌 헬퍼 `old`를 사용하는 것이 더 편리합니다. 해당 필드 값이 없으면 `null` 반환입니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 조회

Laravel이 생성한 모든 쿠키는 암호화 & 서명되어, 클라이언트에서 변경되면 무효 처리됩니다. 요청에서 쿠키 값을 얻으려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 다듬기와 정규화

기본적으로, Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `App\Http\Middleware\TrimStrings`, `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 추가합니다. 이 미들웨어들은 `App\Http\Kernel` 클래스의 `$middleware` 속성에 나열되어 있습니다. 이 미들웨어는 요청의 모든 문자열 필드를 자동으로 trim(양쪽 공백 제거)하고, 빈 문자열은 `null`로 변환합니다. 이로 인해 라우트와 컨트롤러에서 따로 신경 쓸 필요가 없습니다.

#### 입력 정규화 비활성화

입력 정규화 기능을 모든 요청에서 비활성화하고 싶다면, 해당 미들웨어 둘을 `App\Http\Kernel`의 `$middleware`에서 제거하면 됩니다.

일부 요청만 문자열 트리밍/빈 문자열 변환을 끄고 싶다면, 두 미들웨어에서 제공하는 `skipWhen` 메서드를 활용하세요. 이 메서드는 클로저를 인자로 받아 정규화 건너뛰기 여부를 결정합니다. 일반적으로, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use App\Http\Middleware\TrimStrings;
use Illuminate\Http\Request;
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;

/**
 * 애플리케이션 서비스 부트스트랩.
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
## 파일

<a name="retrieving-uploaded-files"></a>
### 업로드 파일 조회

업로드된 파일은 `Illuminate\Http\Request` 인스턴스의 `file` 메서드 또는 동적 속성으로 조회합니다. `file` 메서드는 PHP의 `SplFileInfo`를 확장한 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 파일을 다루는 다양한 메서드가 제공됩니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드로 요청에 파일이 있는지 확인할 수 있습니다.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 확인

파일이 존재하는지 뿐만 아니라, 업로드 과정에 문제가 없었는지 `isValid` 메서드로 검사할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스는 파일의 전체 경로나 확장자 등을 얻는 메서드도 제공합니다. `extension`은 실제 파일 내용을 바탕으로 확장자를 추측하므로, 클라이언트가 설정한 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에는 다양한 메서드가 있습니다. 자세한 정보는 [API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드 파일 저장

업로드된 파일은 일반적으로 [파일시스템](/docs/{{version}}/filesystem)에 저장합니다. `UploadedFile`의 `store` 메서드는 업로드 파일을 지정한 디스크(로컬 또는 Amazon S3 등)에 저장합니다.

`store` 메서드는 파일이 저장될 경로(디스크의 루트 기준)를 첫 번째 인자로 받습니다. 파일명은 자동으로 고유값이 생성되어 사용합니다.

두 번째 인자로 사용할 디스크명을 넘길 수 있습니다. 반환값은 디스크 루트 기준으로 한 파일 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 지정하려면 `storeAs` 메서드를 사용합니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]  
> 파일 저장에 관한 자세한 내용은 [파일 시스템 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정

TLS/SSL 인증서가 종료되는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼 사용 시 HTTPS 링크가 생성되지 않을 수 있습니다. 이는 애플리케이션이 로드 밸런서를 통해 80포트로 트래픽을 전달받고 있어서, 안전한 링크를 만들어야 하는지 알 수 없는 경우입니다.

이 문제를 해결하려면, Laravel에 포함된 `App\Http\Middleware\TrustProxies` 미들웨어에서 신뢰할 수 있는 로드 밸런서/프록시를 설정할 수 있습니다. 신뢰할 수 있는 프록시는 `$proxies` 속성에 배열로 나열합니다. `$headers` 속성으로 프록시 탐지를 위한 헤더들도 설정할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * 애플리케이션이 신뢰하는 프록시 목록.
     *
     * @var string|array
     */
    protected $proxies = [
        '192.168.1.1',
        '192.168.1.2',
    ];

    /**
     * 프록시 탐지에 사용할 헤더들.
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_FOR | Request::HEADER_X_FORWARDED_HOST | Request::HEADER_X_FORWARDED_PORT | Request::HEADER_X_FORWARDED_PROTO;
}
```

> [!NOTE]  
> AWS Elastic Load Balancing 환경에서는 `$headers` 값을 `Request::HEADER_X_FORWARDED_AWS_ELB`로 설정해야 합니다. 사용 가능한 상수에 대한 자세한 내용은 Symfony 문서 [trusting proxies](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

Amazon AWS 또는 기타 "클라우드" 로드 밸런서 공급자를 사용하는 경우, 실제 밸런서의 IP 주소를 알 수 없을 수 있습니다. 이 경우, `"*"`로 모든 프록시를 신뢰하도록 설정할 수 있습니다.

```php
/**
 * 애플리케이션이 신뢰하는 프록시 목록.
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정

기본적으로, Laravel은 HTTP 요청의 `Host` 헤더 값과 무관하게 모든 요청에 응답합니다. 또한, 웹 요청 중 절대 URL을 생성할 때 `Host` 헤더의 값을 사용합니다.

일반적으로 웹 서버(Nginx, Apache 등)에서 특정 호스트 네임을 가진 요청만 애플리케이션으로 전달하게 설정합니다. 그러나 직접 웹 서버를 제어할 수 없고, Laravel 내에서만 특정 호스트에만 응답하도록 제한하려면, `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하세요.

`TrustHosts` 미들웨어는 이미 `$middleware` 스택에 포함되어 있으므로, 주석만 해제해 활성화하면 됩니다. 이 미들웨어의 `hosts` 메서드에서 애플리케이션이 허용할 호스트명을 지정할 수 있습니다. 다른 `Host` 값이 있는 요청은 거부됩니다.

```php
/**
 * 신뢰할 호스트 패턴 반환.
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

`allSubdomainsOfApplicationUrl` 헬퍼는 `app.url` 설정 값의 모든 서브도메인에 매치되는 정규표현식을 반환합니다. 이는 와일드카드 서브도메인을 사용하는 앱 구축 시 모든 서브도메인을 허용할 때 유용합니다.