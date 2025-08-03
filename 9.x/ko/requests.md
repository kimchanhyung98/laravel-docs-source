# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 인스턴스 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [컨텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력값이 존재하는지 확인하기](#determining-if-input-is-present)
    - [추가 입력값 병합하기](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 자르기 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정하기](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청과 상호작용할 수 있는 객체지향적 방법을 제공하며, 요청과 함께 전송된 입력값, 쿠키, 파일들을 가져오는 기능을 제공합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청 인스턴스 접근하기 (Accessing The Request)

현재 HTTP 요청 인스턴스를 의존성 주입으로 얻으려면 라우트 클로저 또는 컨트롤러 메서드에 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. Laravel의 [서비스 컨테이너](/docs/9.x/container)가 자동으로 요청 인스턴스를 주입해 줍니다.

```
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

앞서 설명한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request`를 타입힌트하여 사용할 수 있습니다. 이에 따라 서비스 컨테이너가 실행 시점에 자동으로 요청을 주입합니다:

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    //
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입 & 라우트 매개변수 (Dependency Injection & Route Parameters)

컨트롤러 메서드가 라우트 매개변수 입력도 함께 기대한다면, 라우트 매개변수는 다른 의존성 뒤에 나열해야 합니다. 예를 들어, 아래와 같이 라우트가 정의되어 있다면:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

다음과 같이 컨트롤러 메서드에 `Illuminate\Http\Request`를 타입힌트하고 라우트 매개변수 `id`를 받을 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정한 사용자를 업데이트합니다.
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
### 요청 경로, 호스트, 메서드 (Request Path, Host, & Method)

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하는 다양한 메서드를 제공합니다. 이 클래스는 `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 가장 중요한 몇 가지 메서드를 아래에서 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기 (Retrieving The Request Path)

`path` 메서드는 요청 경로 정보를 반환합니다. 예를 들어, 요청 URL이 `http://example.com/foo/bar`라면 `path` 메서드는 `foo/bar`를 반환합니다:

```
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로나 라우트 확인하기 (Inspecting The Request Path / Route)

`is` 메서드를 사용하면 현재 요청 경로가 특정 패턴과 일치하는지 검증할 수 있습니다. 이때 와일드카드 문자인 `*`를 사용할 수 있습니다:

```
if ($request->is('admin/*')) {
    //
}
```

`routeIs` 메서드를 사용하면 현재 요청이 [이름이 지정된 라우트](/docs/9.x/routing#named-routes)와 일치하는지 확인할 수 있습니다:

```
if ($request->routeIs('admin.*')) {
    //
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기 (Retrieving The Request URL)

요청에 대해 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용하세요. `url` 메서드는 쿼리 문자열을 제외한 URL을 반환하며, `fullUrl`은 쿼리 문자열도 포함한 전체 URL을 반환합니다:

```
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열을 추가로 덧붙이고 싶다면 `fullUrlWithQuery` 메서드를 호출하면 됩니다. 이 메서드는 기존 쿼리 문자열과 인자로 전달한 배열을 병합합니다:

```
$request->fullUrlWithQuery(['type' => 'phone']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기 (Retrieving The Request Host)

요청의 "호스트"를 `host`, `httpHost`, `schemeAndHttpHost` 메서드로 가져올 수 있습니다:

```
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기 (Retrieving The Request Method)

`method` 메서드는 요청의 HTTP 메서드를 반환합니다. 특정 HTTP 메서드인지 확인하려면 `isMethod` 메서드를 사용할 수 있습니다:

```
$method = $request->method();

if ($request->isMethod('post')) {
    //
}
```

<a name="request-headers"></a>
### 요청 헤더 (Request Headers)

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드로 특정 요청 헤더 값을 가져올 수 있습니다. 헤더가 없으면 기본값으로 `null`이 반환되지만, 두 번째 인자에 기본값을 지정할 수도 있습니다:

```
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드로 특정 헤더가 존재하는지도 확인할 수 있습니다:

```
if ($request->hasHeader('X-Header-Name')) {
    //
}
```

편의상 `bearerToken` 메서드는 `Authorization` 헤더에서 Bearer 토큰을 추출하는 데 사용됩니다. 해당 헤더가 없으면 빈 문자열을 반환합니다:

```
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소 (Request IP Address)

`ip` 메서드를 통해 클라이언트가 요청을 보낸 IP 주소를 가져올 수 있습니다:

```
$ipAddress = $request->ip();
```

<a name="content-negotiation"></a>
### 컨텐츠 협상 (Content Negotiation)

Laravel은 요청 헤더의 `Accept` 값을 검사하는 여러 메서드를 제공합니다. 우선 `getAcceptableContentTypes` 메서드는 요청에서 수용 가능한 컨텐츠 타입 배열을 반환합니다:

```
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 인자로 배열을 받아 요청이 해당 컨텐츠 타입 중 하나라도 허용하면 `true`, 그렇지 않으면 `false`를 반환합니다:

```
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 인자로 받은 컨텐츠 타입 배열 중 요청에서 가장 선호하는 타입을 반환합니다. 해당 타입이 없으면 `null`을 반환합니다:

```
$preferred = $request->prefers(['text/html', 'application/json']);
```

대부분 애플리케이션은 HTML이나 JSON만 반환하므로, `expectsJson` 메서드로 요청이 JSON 응답을 기대하는지도 쉽게 확인할 수 있습니다:

```
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청 (PSR-7 Requests)

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청과 응답을 포함한 HTTP 메시지 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻으려면 몇몇 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge*를 이용해 Laravel 요청 및 응답을 PSR-7 호환 구현체로 변환합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리들을 설치한 후, 라우트 클로저나 컨트롤러 메서드에 PSR-7 요청 인터페이스를 타입힌트하면 PSR-7 요청 인스턴스를 받을 수 있습니다:

```
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    //
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, Laravel이 이를 자동으로 기본 Laravel 응답 인스턴스로 변환하여 화면에 출력합니다.

<a name="input"></a>
## 입력값 (Input)

<a name="retrieving-input"></a>
### 입력값 가져오기 (Retrieving Input)

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 가져오기 (Retrieving All Input Data)

`all` 메서드는 현재 요청의 모든 입력 데이터를 연관 배열로 반환합니다. HTML 폼 요청이나 XHR 요청 모두에서 사용할 수 있습니다:

```
$input = $request->all();
```

`collect` 메서드를 사용하면 모든 입력을 Laravel의 [컬렉션](/docs/9.x/collections) 형태로 받을 수 있습니다:

```
$input = $request->collect();
```

`collect` 메서드는 입력의 일부만 골라 컬렉션으로 가져오는 것도 가능합니다:

```
$request->collect('users')->each(function ($user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 특정 입력값 가져오기 (Retrieving An Input Value)

간단한 메서드로 HTTP 메서드에 관계없이 모든 사용자 입력을 가져올 수 있습니다. `input` 메서드를 사용하면 됩니다:

```
$name = $request->input('name');
```

두 번째 인자로 기본값을 전달하면, 요청에 해당 입력이 없을 때 기본값을 반환합니다:

```
$name = $request->input('name', 'Sally');
```

배열 입력이 포함된 폼에서는 "점(.)" 표기법을 써서 배열의 하위 값을 조회할 수 있습니다:

```
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인자를 지정하지 않으면 모든 입력값을 연관 배열로 반환합니다:

```
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력값 가져오기 (Retrieving Input From The Query String)

`input` 메서드는 전체 요청에서 값을 가져오지만, `query` 메서드는 쿼리 문자열에서만 값을 가져옵니다:

```
$name = $request->query('name');
```

두 번째 인자로 기본값을 넘길 수도 있습니다:

```
$name = $request->query('name', 'Helen');
```

인자 없이 호출하면 쿼리 문자열의 모든 값을 연관 배열로 반환합니다:

```
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기 (Retrieving JSON Input Values)

JSON 요청을 보낼 때, 요청 헤더의 `Content-Type`이 `application/json`으로 올바르게 설정되어 있으면 `input` 메서드로 JSON 데이터를 접근할 수 있습니다. 점(.) 문법으로 중첩된 배열이나 객체 필드도 조회 가능합니다:

```
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### 문자열 객체형 입력값 가져오기 (Retrieving Stringable Input Values)

입력값을 기본 문자열이 아니라 [`Illuminate\Support\Stringable`](/docs/9.x/helpers#fluent-strings) 객체로 받고 싶으면 `string` 메서드를 이용할 수 있습니다:

```
$name = $request->string('name')->trim();
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언형 입력값 가져오기 (Retrieving Boolean Input Values)

체크박스 같은 HTML 요소에서 "true", "on"과 같은 문자열이 오더라도, `boolean` 메서드를 사용하면 불리언으로 변환하여 가져올 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환하며, 그 외는 `false`를 반환합니다:

```
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기 (Retrieving Date Input Values)

날짜/시간 입력값을 Carbon 인스턴스로 가져오려면 `date` 메서드를 사용하세요. 만약 해당 이름의 입력값이 없으면 `null`이 반환됩니다:

```
$birthday = $request->date('birthday');
```

`date` 메서드는 두 번째와 세 번째 인자로 각각 날짜 포맷과 타임존을 지정할 수 있습니다:

```
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 존재하지만 포맷이 올바르지 않으면 `InvalidArgumentException` 예외가 발생하므로, `date` 메서드를 호출하기 전에 검증하는 것을 권장합니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 가져오기 (Retrieving Enum Input Values)

요청에서 [PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)과 대응하는 입력값도 가져올 수 있습니다. 입력값이 없거나 enum에 해당 백업 값이 없으면 `null`을 반환합니다. `enum` 메서드는 첫 번째 인자로 입력 이름, 두 번째 인자로 enum 클래스를 받습니다:

```
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성으로 입력값 가져오기 (Retrieving Input Via Dynamic Properties)

`Illuminate\Http\Request` 인스턴스의 동적 속성으로도 사용자 입력에 접근 가능합니다. 예를 들어, 폼에 `name` 필드가 있으면 다음과 같이 값에 접근할 수 있습니다:

```
$name = $request->name;
```

동적 속성을 사용할 때 Laravel은 먼저 요청 본문(payload)에서 찾고, 없으면 라우트 매개변수에서 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터의 일부만 가져오기 (Retrieving A Portion Of The Input Data)

입력 데이터 중 일부만 가져오려면 `only`와 `except` 메서드를 사용하세요. 두 메서드 모두 배열 또는 여러 개의 인자를 받을 수 있습니다:

```
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 존재하는 key/value 쌍만 반환하며, 요청에 없는 값은 반환하지 않습니다.

<a name="determining-if-input-is-present"></a>
### 입력값 존재 여부 판단하기 (Determining If Input Is Present)

`has` 메서드는 특정 값이 요청에 존재하는지 검사해 `true`/`false`를 반환합니다:

```
if ($request->has('name')) {
    //
}
```

배열을 인자로 전달하면 모든 값이 존재해야 `true`를 반환합니다:

```
if ($request->has(['name', 'email'])) {
    //
}
```

`whenHas` 메서드는 지정한 값이 존재할 때 주어진 클로저를 실행합니다:

```
$request->whenHas('name', function ($input) {
    //
});
```

두 번째 인자로는 값이 없을 때 실행할 클로저를 전달할 수 있습니다:

```
$request->whenHas('name', function ($input) {
    // "name" 값이 존재...
}, function () {
    // "name" 값이 존재하지 않음...
});
```

`hasAny` 메서드는 지정한 값 중 하나라도 있으면 `true`를 반환합니다:

```
if ($request->hasAny(['name', 'email'])) {
    //
}
```

입력값이 있고 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용하세요:

```
if ($request->filled('name')) {
    //
}
```

`whenFilled` 메서드는 값이 존재하고 빈 문자열이 아니면 클로저를 실행합니다:

```
$request->whenFilled('name', function ($input) {
    //
});
```

두 번째 인자로는 "빈 값 아님" 조건 미충족 시 실행할 클로저를 줄 수 있습니다:

```
$request->whenFilled('name', function ($input) {
    // "name" 값이 채워져 있음...
}, function () {
    // "name" 값이 비어 있음...
});
```

특정 key가 요청에 없으면 `missing`과 `whenMissing` 메서드를 사용할 수 있습니다:

```
if ($request->missing('name')) {
    //
}

$request->whenMissing('name', function ($input) {
    // "name" 값 없음...
}, function () {
    // "name" 값 존재...
});
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합하기 (Merging Additional Input)

기존 입력 데이터에 새로운 입력을 수동으로 병합해야 할 경우 `merge` 메서드를 사용하세요. 이미 존재하는 key는 덮어씁니다:

```
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 요청에 해당 key가 없을 때만 병합합니다:

```
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값 (Old Input)

Laravel은 요청 시점에 입력 데이터를 세션에 저장해 다음 요청에서도 유지할 수 있게 지원합니다. 이는 유효성 검사 오류 후 폼을 다시 채울 때 유용합니다. Laravel 내장 [유효성 검사 기능](/docs/9.x/validation)을 사용하는 경우 수동으로 세션 입력 플래싱 메서드를 직접 호출하지 않아도 편리합니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값 세션에 플래시하기 (Flashing Input To The Session)

`Illuminate\Http\Request`의 `flash` 메서드는 요청의 현재 입력을 [세션](/docs/9.x/session)에 플래시하여 다음 요청까지 사용할 수 있도록 합니다:

```
$request->flash();
```

특정 입력만 플래시하려면 `flashOnly`, 제외하려면 `flashExcept` 메서드를 씁니다. 민감한 정보(예: 비밀번호)를 세션에 저장하지 않고자 할 때 유용합니다:

```
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트하기 (Flashing Input Then Redirecting)

입력값을 플래시한 뒤 이전 페이지로 리다이렉트할 때는 `withInput` 메서드를 이용해 쉽게 체이닝할 수 있습니다:

```
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기 (Retrieving Old Input)

이전 요청에 플래시된 입력값은 `Illuminate\Http\Request` 인스턴스의 `old` 메서드로 꺼내올 수 있습니다. `old` 메서드는 세션에서 이전 입력을 가져옵니다:

```
$username = $request->old('username');
```

Blade 템플릿에서는 글로벌 `old` 헬퍼를 사용하는 것이 더욱 편리합니다. 필드에 이전 입력값이 없으면 `null`을 반환합니다:

```
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기 (Retrieving Cookies From Requests)

Laravel에서 생성된 모든 쿠키는 암호화되고 인증 코드로 서명되어 있어, 클라이언트가 임의로 변경하면 무효가 됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request`의 `cookie` 메서드를 사용하세요:

```
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 자르기 및 정규화 (Input Trimming & Normalization)

기본적으로 Laravel은 `App\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 글로벌 미들웨어 스택에 포함합니다. 이들은 `App\Http\Kernel` 클래스의 `$middleware` 프로퍼티에서 지정되며, 요청에 들어오는 모든 문자열 필드를 자동으로 트림(trim)하고, 빈 문자열은 `null`로 변환합니다. 이로 인해 라우트와 컨트롤러에서 별도의 정규화 처리 걱정 없이 코드를 작성할 수 있습니다.

#### 입력값 정규화 비활성화하기

모든 요청에 대해 이 기능을 비활성화하려면, `App\Http\Kernel` 클래스의 `$middleware` 배열에서 위 두 미들웨어를 제거하면 됩니다.

일부 요청만 정규화를 비활성화하려면 두 미들웨어가 제공하는 `skipWhen` 메서드를 사용하세요. 이 메서드는 클로저를 받고, `true`를 반환하면 정규화를 건너뜁니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use App\Http\Middleware\TrimStrings;
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;

/**
 * 애플리케이션 서비스 부트스트랩
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
## 파일 (Files)

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기 (Retrieving Uploaded Files)

`Illuminate\Http\Request` 인스턴스의 `file` 메서드나 동적 속성을 통해 업로드된 파일에 접근할 수 있습니다. `file` 메서드는 PHP의 `SplFileInfo` 클래스를 확장한 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 해당 파일과 상호작용할 수 있는 여러 메서드를 제공합니다:

```
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드로 파일이 요청에 포함되어 있는지 확인할 수 있습니다:

```
if ($request->hasFile('photo')) {
    //
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증하기 (Validating Successful Uploads)

파일 존재 여부를 확인하는 것 외에, `isValid` 메서드를 사용해 업로드 과정에 오류가 없었는지도 검증할 수 있습니다:

```
if ($request->file('photo')->isValid()) {
    //
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자 (File Paths & Extensions)

`UploadedFile` 클래스는 파일의 절대 경로와 확장자를 가져오는 메서드를 포함합니다. `extension` 메서드는 파일 내용을 기반으로 확장자를 추측하므로, 클라이언트가 전달한 확장자와 다를 수 있습니다:

```
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드 (Other File Methods)

`UploadedFile` 인스턴스에서 사용 가능한 기타 메서드는 [API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기 (Storing Uploaded Files)

업로드된 파일을 저장하려면 일반적으로 설정된 [파일 시스템](/docs/9.x/filesystem)을 이용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 로컬 디스크나 Amazon S3 같은 클라우드 저장소 위치로 이동합니다.

`store` 메서드는 파일 시스템 루트 디렉터리를 기준으로 저장할 경로를 받으며, 파일명은 자동으로 고유 ID가 생성됩니다.

두 번째 인자로 스토리지 디스크 이름을 지정할 수 있습니다. 메서드는 해당 디스크 루트 기준 저장 경로를 반환합니다:

```
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

자동 생성된 파일명이 아닌 직접 지정하고 싶다면, 저장할 경로, 파일명, 디스크명을 인자로 받는 `storeAs` 메서드를 사용하세요:

```
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel에서 파일 저장 관련 더 자세한 내용은 [파일 시스템 문서](/docs/9.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정하기 (Configuring Trusted Proxies)

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼가 HTTPS 링크를 제대로 생성하지 못하는 경우가 있습니다. 이는 보통 트래픽이 포트 80을 통해 로드 밸런서에서 전달되기에 애플리케이션이 안전한(https) 링크를 생성해야 할지 모르는 상황 때문입니다.

이를 해결하려면 Laravel에 기본 내장된 `App\Http\Middleware\TrustProxies` 미들웨어를 사용해 신뢰할 프록시 서버를 지정할 수 있습니다. 이 미들웨어의 `$proxies` 프로퍼티에 신뢰할 프록시의 IP 주소를 배열로 등록합니다. 또한 신뢰할 프록시 헤더를 나타내는 `$headers` 프로퍼티도 설정할 수 있습니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * 애플리케이션에서 신뢰할 프록시들
     *
     * @var string|array
     */
    protected $proxies = [
        '192.168.1.1',
        '192.168.1.2',
    ];

    /**
     * 프록시 감지에 사용할 헤더 플래그
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_FOR
        | Request::HEADER_X_FORWARDED_HOST
        | Request::HEADER_X_FORWARDED_PORT
        | Request::HEADER_X_FORWARDED_PROTO;
}
```

> [!NOTE]
> AWS Elastic Load Balancing을 사용하는 경우, `$headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`를 사용해야 합니다. 더 다양한 상수 및 사용법은 Symfony의 [프록시 신뢰 설정 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기 (Trusting All Proxies)

AWS 등 클라우드 로드 밸런서를 사용할 때 실제 로드 밸런서 IP 주소를 모르는 경우가 많습니다. 이럴 때는 프록시 배열에 `*`를 지정해 모두 신뢰할 수 있습니다:

```
/**
 * 애플리케이션에서 신뢰할 프록시들
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정하기 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 모든 요청에 응답합니다. 또한 절대 URL 생성 시 `Host` 헤더 값을 사용합니다.

일반적으로 웹 서버(Nginx, Apache 등)에서 특정 호스트명에 맞는 요청만 애플리케이션에 전달하도록 구성하는 것이 좋습니다. 하지만 웹 서버 설정을 변경할 수 없는 경우 Laravel에서 애플리케이션이 응답할 신뢰할 호스트명을 제한할 수 있습니다. 이를 위해 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다.

`TrustHosts` 미들웨어는 이미 `$middleware` 스택에 포함되어 있으나, 주석 처리되어 있을 수 있으니 주석을 해제해 활성화하세요. 이 미들웨어의 `hosts` 메서드에서 애플리케이션이 응답할 호스트 패턴을 지정할 수 있습니다. 지정된 호스트와 다른 `Host` 헤더를 가진 요청은 거부됩니다:

```
/**
 * 신뢰할 호스트 패턴 배열 반환
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

`allSubdomainsOfApplicationUrl` 헬퍼 메서드는 `app.url` 설정값의 모든 서브도메인에 대응하는 정규 표현식을 반환합니다. 이를 통해 와일드카드 서브도메인을 사용하는 애플리케이션에서 모든 서브도메인을 허용할 수 있습니다.