# HTTP 요청

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로 및 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값](#input)
    - [입력값 가져오기](#retrieving-input)
    - [입력이 존재하는지 확인](#determining-if-input-is-present)
    - [추가 입력 병합](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 구성](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 구성](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청과 상호작용하고, 요청과 함께 제출된 입력값, 쿠키, 파일을 객체 지향적으로 가져올 수 있는 방법을 제공합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청에 접근하기

HTTP 요청 인스턴스를 의존성 주입을 통해 얻으려면, 라우트 클로저 또는 컨트롤러 메소드에 `Illuminate\Http\Request` 클래스를 타입힌트 하면 됩니다. 들어오는 요청 인스턴스는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에서 자동으로 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 유저 저장
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

앞에서 설명했듯이, 라우트 클로저에서도 `Illuminate\Http\Request`를 타입힌트로 사용할 수 있습니다. 서비스 컨테이너는 실행 시 요청을 자동으로 주입합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    //
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입 & 라우트 파라미터

컨트롤러 메소드에서 라우트 파라미터도 함께 받고 싶을 경우, 라우트 파라미터를 다른 의존성 뒤에 위치하게 하세요. 예를 들어, 라우트를 다음과 같이 정의한 경우:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

아래와 같이 컨트롤러 메소드를 정의하면 `Illuminate\Http\Request`를 타입힌트 하면서 라우트 파라미터 `id`도 같이 받을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 유저 업데이트
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
### 요청 경로 및 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청에 대한 다양한 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서 주요 메서드 몇 가지를 소개합니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 정보 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 들어오는 요청이 `http://example.com/foo/bar`라면, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로 / 라우트 검사

`is` 메서드는 들어오는 요청 경로가 특정 패턴과 일치하는지 확인합니다. `*` 문자를 와일드카드로 사용할 수 있습니다:

```php
if ($request->is('admin/*')) {
    //
}
```

`routeIs` 메서드를 사용하면, 들어오는 요청이 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)인지 확인할 수 있습니다:

```php
if ($request->routeIs('admin.*')) {
    //
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

들어오는 요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url`은 쿼리 문자열 없이, `fullUrl`은 쿼리 문자열까지 포함한 URL을 반환합니다:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열 데이터를 추가하고 싶다면 `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 주어진 쿼리 문자열 배열을 현재 쿼리 문자열과 합칩니다:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기

`method` 메서드는 요청의 HTTP 메서드(verb)를 반환합니다. `isMethod` 메서드를 사용하면 메서드가 특정 문자열과 일치하는지도 확인할 수 있습니다:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    //
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용해 요청 헤더를 가져올 수 있습니다. 요청에 해당 헤더가 없다면 `null`이 반환됩니다. 하지만 두 번째 인수로 기본값을 지정할 수 있습니다:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드를 사용해 요청에 특정 헤더가 포함되어 있는지 확인할 수 있습니다:

```php
if ($request->hasHeader('X-Header-Name')) {
    //
}
```

편의상, `bearerToken` 메서드를 사용해 `Authorization` 헤더에서 Bearer 토큰을 가져올 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다:

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드는 요청을 보낸 클라이언트의 IP 주소를 반환합니다:

```php
$ipAddress = $request->ip();
```

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 `Accept` 헤더를 통해 요청된 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청에서 허용하는 모든 콘텐츠 타입의 배열을 반환합니다:

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입의 배열을 받아, 요청이 이 중 하나라도 허용하면 `true`를, 아니면 `false`를 반환합니다:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드를 사용하면 주어진 콘텐츠 타입 중 가장 선호되는 타입을 알 수 있습니다. 만약 제공된 타입 중 어떤 것도 요청이 허용하지 않으면 `null`을 반환합니다:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML이나 JSON만 제공하므로, `expectsJson` 메서드를 사용해 들어오는 요청이 JSON 응답을 기대하는지 빠르게 알 수 있습니다:

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청과 응답을 포함한 HTTP 메시지 인터페이스를 지정합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 받고 싶다면 몇몇 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 이용해 일반 Laravel 요청 및 응답을 PSR-7 호환 구현체로 변환합니다:

```bash
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리 설치 후, 라우트 클로저 또는 컨트롤러 메소드에서 PSR-7 요청 인터페이스를 타입힌트하면 PSR-7 요청을 받을 수 있습니다:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    //
});
```

> {tip} 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 Laravel 응답 인스턴스로 변환하여 출력합니다.

<a name="input"></a>
## 입력값

<a name="retrieving-input"></a>
### 입력값 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 데이터 가져오기

`all` 메서드를 사용하여 들어오는 요청의 모든 입력값 데이터를 `array`로 가져올 수 있습니다. 이 메서드는 HTML 폼이든, XHR 요청이든 상관 없이 사용할 수 있습니다:

```php
$input = $request->all();
```

`collect` 메서드를 사용하면 모든 입력값을 [컬렉션](/docs/{{version}}/collections)으로 가져올 수도 있습니다:

```php
$input = $request->collect();
```

또한, `collect` 메서드는 입력값의 부분집합을 컬렉션 형태로 가져올 수도 있습니다:

```php
$request->collect('users')->each(function ($user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 단일 입력값 가져오기

몇 가지 간단한 메서드로, `Illuminate\Http\Request` 인스턴스의 모든 사용자 입력값을 HTTP 메서드에 상관 없이 접근할 수 있습니다. 예를 들어 `input` 메서드는 요청 메서드와 관계 없이 사용자 입력값을 가져옵니다:

```php
$name = $request->input('name');
```

`input` 메서드의 두 번째 인수로 기본값을 전달할 수 있으며, 입력값이 없을 때 이 값이 반환됩니다:

```php
$name = $request->input('name', 'Sally');
```

배열 입력이 포함된 폼을 다룰 때는 "점(.)" 표기법을 사용해 배열 요소에 접근할 수 있습니다:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인수 없이 `input` 메서드를 호출하면 모든 입력값을 연관 배열로 반환합니다:

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 가져오기

`input` 메서드는 쿼리 스트링을 포함해 전체 요청 페이로드에서 값을 가져오지만, `query` 메서드는 쿼리 스트링 값만 가져옵니다:

```php
$name = $request->query('name');
```

해당 쿼리 값이 없을 경우 두 번째 인수로 전달한 값이 반환됩니다:

```php
$name = $request->query('name', 'Helen');
```

인수 없이 `query` 메서드를 호출하면 쿼리 스트링 값 전체를 연관 배열로 반환합니다:

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

애플리케이션에 JSON 요청을 전송할 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있다면, `input` 메서드를 통해 JSON 데이터를 가져올 수 있습니다. 또한, "점(.)" 표기법을 사용해 JSON 배열 내에 중첩된 값을 가져올 수도 있습니다:

```php
$name = $request->input('user.name');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기

HTML 체크박스 등으로 인해 문자열로 된 "진실값(truthy)"을 받을 수 있습니다(예: "true", "on" 등). 편의상, `boolean` 메서드를 사용하면 이러한 값을 불리언으로 가져올 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes" 값을 `true`로 처리하며, 그 외는 `false`를 반환합니다:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜/시간이 포함된 입력값은 `date` 메서드로 Carbon 인스턴스로 가져올 수 있습니다. 입력값이 없으면 `null`이 반환됩니다:

```php
$birthday = $request->date('birthday');
```

두 번째 및 세 번째 인수로 날짜 포맷과 타임존을 각각 지정할 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 있지만 형식이 유효하지 않으면 `InvalidArgumentException`이 발생하므로, `date` 메서드 호출 전 입력값을 검증하는 것이 좋습니다.

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력값 가져오기

`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티를 통해서도 입력값에 접근할 수 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 아래처럼 원하는 값을 가져올 수 있습니다:

```php
$name = $request->name;
```

동적 프로퍼티 사용 시, 해당 파라미터 값이 먼저 요청의 페이로드에서 검색되며, 거기 없으면 라우트 파라미터에서 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값 일부만 가져오기

입력 데이터의 부분집합이 필요하다면 `only`와 `except` 메서드를 사용할 수 있습니다. 이 메서드들은 배열이나 여러 인수를 받을 수 있습니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> {note} `only` 메서드는 요청에 존재하는 key/value만 반환하며, 요청에 없는 key는 반환하지 않습니다.

<a name="determining-if-input-is-present"></a>
### 입력이 존재하는지 확인

요청에 값이 있는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 값이 존재하면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    //
}
```

배열을 전달하면, `has`는 지정한 모든 값이 있는지 확인합니다:

```php
if ($request->has(['name', 'email'])) {
    //
}
```

`whenHas` 메서드는 해당 값이 있을 경우 지정한 클로저를 실행합니다:

```php
$request->whenHas('name', function ($input) {
    //
});
```

두 번째 클로저를 `whenHas`에 넘기면, 값이 없을 때 실행됩니다:

```php
$request->whenHas('name', function ($input) {
    // "name" 값이 존재할 때
}, function () {
    // "name" 값이 없을 때
});
```

`hasAny` 메서드는 지정한 값 중 하나라도 있으면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    //
}
```

값이 존재하며 비어있지 않은지 확인하려면 `filled` 메서드를 사용하세요:

```php
if ($request->filled('name')) {
    //
}
```

`whenFilled` 메서드는 값이 존재하고 비어있지 않을 때 클로저를 실행합니다:

```php
$request->whenFilled('name', function ($input) {
    //
});
```

두 번째 클로저를 넘기면, 값이 "채워져 있지" 않을 때 실행됩니다:

```php
$request->whenFilled('name', function ($input) {
    // "name" 값이 채워졌을 때
}, function () {
    // "name" 값이 채워지지 않았을 때
});
```

요청에 특정 키가 없는지 확인하려면 `missing` 메서드를 사용하세요:

```php
if ($request->missing('name')) {
    //
}
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합

기존 요청 입력값에 수동으로 추가 입력을 병합해야 할 때가 있습니다. 이런 경우 `merge` 메서드를 사용할 수 있습니다:

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 해당 키가 이미 존재하지 않을 때만 값을 병합합니다:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값

Laravel은 한 번의 요청에서 입력을 다음 요청까지 유지할 수 있게 해줍니다. 이 기능은 유효성 검사 오류 이후 폼을 다시 채울 때 유용합니다. 하지만 Laravel의 [유효성 검사 기능](/docs/{{version}}/validation)을 사용한다면, 이 세션 입력 플래시(flash) 메서드를 직접 사용할 필요가 없을 수 있습니다. Laravel의 일부 내장 유효성 검사 기능이 자동으로 호출하기 때문입니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력값을 [세션](/docs/{{version}}/session)에 플래시하여 다음 요청에서 사용할 수 있도록 합니다:

```php
$request->flash();
```

입력값의 일부만 세션에 플래시하려면 `flashOnly`와 `flashExcept` 메서드를 사용할 수 있습니다. 비밀번호 같은 민감한 정보는 세션에 남기지 않을 때 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력 플래시 후 리다이렉트

입력을 세션에 플래시한 뒤 이전 페이지로 리다이렉트하고 싶을 때가 많으므로, `withInput` 메서드를 사용해 리다이렉트에 입력 플래싱을 쉽게 연결할 수 있습니다:

```php
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 조회

이전 요청에서 플래시된 입력을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다. 이 메서드는 [세션](/docs/{{version}}/session)에서 이전 입력값을 가져옵니다:

```php
$username = $request->old('username');
```

Blade 뷰(template)에서는 Laravel이 제공하는 전역 `old` 헬퍼를 사용하는 것이 더 편리합니다. 해당 필드에 이전 입력값이 없다면 `null`이 반환됩니다:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel에서 생성된 모든 쿠키는 암호화되고 인증 코드로 서명됩니다. 즉, 클라이언트에서 변경했다면 유효하지 않게 처리됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `cookie` 메서드를 사용하세요:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화

기본적으로 Laravel에는 애플리케이션의 글로벌 미들웨어 스택에 `App\Http\Middleware\TrimStrings`와 `App\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이 미들웨어들은 `App\Http\Kernel` 클래스의 글로벌 미들웨어 스택에 등록되어 있으며, 자동으로 모든 요청의 문자열 필드를 잘라내고, 빈 문자열은 `null`로 변환합니다. 이런 처리 덕분에 라우트나 컨트롤러에서 정규화 문제를 걱정하지 않아도 됩니다.

이 동작을 비활성화하려면, 애플리케이션의 미들웨어 스택에서 두 미들웨어를 제거하면 됩니다(`App\Http\Kernel` 클래스의 `$middleware` 속성에서 제거).

<a name="files"></a>
## 파일

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기

`Illuminate\Http\Request` 인스턴스에서 `file` 메서드나 동적 프로퍼티를 사용해 업로드된 파일을 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환하며, 이는 PHP의 `SplFileInfo` 클래스를 확장해 다양한 파일 관련 메서드를 제공합니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```

요청에 파일이 있는지 확인하려면 `hasFile` 메서드를 사용하세요:

```php
if ($request->hasFile('photo')) {
    //
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증

파일이 존재하는지 확인하는 것 외에, `isValid` 메서드로 업로드 중 문제가 없었는지 확인할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    //
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 & 확장자

`UploadedFile` 클래스는 파일의 전체 경로와 확장자에 접근하는 메서드도 제공합니다. `extension` 메서드는 파일 내용을 기반으로 확장자를 추측하며, 클라이언트 전달 값과 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에서 사용할 수 있는 다양한 메서드가 있습니다. 자세한 내용은 [클래스 API 문서](https://api.symfony.com/master/Symfony/Component/HttpFoundation/File/UploadedFile.html)를 참조하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일을 저장하려면, [파일 시스템](/docs/{{version}}/filesystem) 설정 중 하나를 주로 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 로컬 파일시스템이나 Amazon S3 등의 클라우드 스토리지같은 디스크로 이동합니다.

`store` 메서드는 파일 시스템의 루트 디렉터리에 대해 상대적인 저장 경로를 받습니다. 이 경로에는 파일명을 포함하지 않으며, 고유한 ID로 파일명이 자동 생성됩니다.

두 번째 인수로 저장할 디스크 이름을 선택적으로 지정할 수 있습니다. 반환 값은 디스크의 루트에 대한 상대 경로입니다:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 직접 지정하고 싶으면, `storeAs` 메서드를 사용하세요(경로, 파일명, 디스크명을 인수로 받음):

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> {tip} Laravel에서 파일 저장에 대한 더 자세한 내용은 [파일 시스템 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 구성

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼 사용 시 HTTPS 링크가 생성되지 않는 현상이 발생할 수 있습니다. 이는 주로 애플리케이션이 80 포트로 전달된 트래픽만 보기 때문에, HTTPS로 동작해야 할지 알 수 없어서 발생합니다.

이를 해결하기 위해, Laravel에 포함된 `App\Http\Middleware\TrustProxies` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 신뢰할 수 있는 로드 밸런서나 프록시를 신속하게 설정할 수 있게 해줍니다. 신뢰할 프록시는 미들웨어의 `$proxies` 속성에 배열로 지정합니다. 더불어, 신뢰할 프록시 `$headers`도 같이 설정할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * 이 애플리케이션에서 신뢰할 프록시
     *
     * @var string|array
     */
    protected $proxies = [
        '192.168.1.1',
        '192.168.1.2',
    ];

    /**
     * 프록시를 탐지할 때 사용할 헤더
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_FOR | Request::HEADER_X_FORWARDED_HOST | Request::HEADER_X_FORWARDED_PORT | Request::HEADER_X_FORWARDED_PROTO;
}
```

> {tip} AWS Elastic Load Balancing을 사용하는 경우, `$headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`여야 합니다. `$headers` 속성에 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [프록시 신뢰 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참조하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

Amazon AWS나 다른 "클라우드" 로드 밸런서 공급자를 사용할 때는 실제 밸런서의 IP 주소를 알 수 없는 경우가 많습니다. 이런 경우, `*`를 사용해 모든 프록시를 신뢰할 수 있습니다:

```php
/**
 * 이 애플리케이션에서 신뢰할 프록시
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 구성

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 모든 요청에 응답합니다. 또한, 웹 요청 중에 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더의 값이 사용됩니다.

보통은 Nginx나 Apache 같은 웹서버에서 지정된 호스트 이름에만 요청을 전달하도록 설정하는 것이 좋습니다. 그러나 웹서버를 직접 설정할 수 없고, Laravel이 특정 호스트 이름에만 응답하게 하고 싶다면, `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하여 지정할 수 있습니다.

`TrustHosts` 미들웨어는 이미 애플리케이션의 `$middleware` 스택에 포함되어 있으며, 활성화하려면 주석 처리를 해제하면 됩니다. 이 미들웨어의 `hosts` 메서드에서 애플리케이션이 응답해야 하는 호스트 이름을 지정할 수 있습니다. 지정된 `Host` 값이 아닌 요청은 거부됩니다:

```php
/**
 * 신뢰할 호스트 패턴 반환
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

`allSubdomainsOfApplicationUrl` 헬퍼 메서드는 애플리케이션의 `app.url`에 대한 모든 하위 도메인을 정규표현식으로 반환합니다. 이 메서드는 와일드카드 하위 도메인을 사용하는 애플리케이션에서 모든 하위 도메인을 허용하는 데 편리합니다.