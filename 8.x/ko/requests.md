# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로 및 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력 (Input)](#input)
    - [입력 데이터 가져오기](#retrieving-input)
    - [입력 존재 여부 확인](#determining-if-input-is-present)
    - [추가 입력 병합하기](#merging-additional-input)
    - [이전 입력](#old-input)
    - [쿠키](#cookies)
    - [입력 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정하기](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청과 상호작용하며, 요청과 함께 제출된 입력(input), 쿠키, 파일을 객체 지향적으로 다룰 수 있게 해줍니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기

<a name="accessing-the-request"></a>
### 요청에 접근하기

의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다. Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 해당 요청 인스턴스를 주입해 줍니다:

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

앞서 설명한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트할 수 있습니다. 서비스 컨테이너가 클로저 실행 시 자동으로 요청 객체를 주입합니다:

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    //
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 매개변수

컨트롤러 메서드가 라우트 매개변수도 기대하는 경우, 라우트 매개변수를 다른 의존성 뒤에 나열해야 합니다. 예를 들어, 라우트가 다음과 같이 정의된 경우:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드를 아래와 같이 정의하면 `Illuminate\Http\Request`를 타입힌트하면서도 `id` 라우트 매개변수를 접근할 수 있습니다:

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
### 요청 경로 및 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하기 위한 다양한 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 여기서는 몇 가지 중요한 메서드를 다뤄보겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어 들어오는 요청이 `http://example.com/foo/bar` 라면, `path` 메서드는 `foo/bar`를 반환합니다:

```
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로나 라우트 검사하기

`is` 메서드를 사용하여 들어오는 요청 경로가 지정한 패턴과 일치하는지 확인할 수 있습니다. 이 메서드에서 `*` 문자를 와일드카드로 사용할 수 있습니다:

```
if ($request->is('admin/*')) {
    //
}
```

`routeIs` 메서드로 들어온 요청이 [이름 있는 라우트](/docs/{{version}}/routing#named-routes)와 일치하는지 확인할 수 있습니다:

```
if ($request->routeIs('admin.*')) {
    //
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

들어오는 요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 문자열 없이 URL만 반환하며, `fullUrl` 메서드는 쿼리 문자열까지 포함해서 반환합니다:

```
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열을 추가하고 싶다면 `fullUrlWithQuery` 메서드를 호출하면 됩니다. 이 메서드는 전달한 배열의 쿼리 문자열 변수를 현재 쿼리 문자열과 합칩니다:

```
$request->fullUrlWithQuery(['type' => 'phone']);
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 가져오기

`method` 메서드는 요청의 HTTP 메서드(동사)를 반환합니다. `isMethod` 메서드를 사용하여 요청 메서드가 지정한 문자열과 일치하는지 확인할 수 있습니다:

```
$method = $request->method();

if ($request->isMethod('post')) {
    //
}
```

<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용해 특정 요청 헤더를 조회할 수 있습니다. 요청에 해당 헤더가 없으면 `null`이 반환됩니다. 하지만 `header` 메서드는 두 번째 인자로 기본값을 지정할 수 있어, 헤더가 없을 때 기본값을 반환합니다:

```
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 요청에 특정 헤더가 포함되어 있는지 확인할 수 있습니다:

```
if ($request->hasHeader('X-Header-Name')) {
    //
}
```

편리하게도 `bearerToken` 메서드를 사용해 `Authorization` 헤더에서 Bearer 토큰을 가져올 수 있습니다. 만약 해당 헤더가 없으면 빈 문자열을 반환합니다:

```
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드를 사용하면 애플리케이션에 요청을 보낸 클라이언트의 IP 주소를 가져올 수 있습니다:

```
$ipAddress = $request->ip();
```

<a name="content-negotiation"></a>
### 콘텐츠 협상(Content Negotiation)

Laravel은 `Accept` 헤더를 통해 요청된 콘텐츠 타입을 검사하는 여러 메서드를 제공합니다. 먼저 `getAcceptableContentTypes` 메서드는 요청에서 허용하는 모든 콘텐츠 타입의 배열을 반환합니다:

```
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 인자로 받아, 요청에서 그 중 하나라도 허용하면 `true`를, 아니면 `false`를 반환합니다:

```
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 지정한 콘텐츠 타입 배열 중에서 요청이 가장 선호하는 타입을 반환합니다. 만약 요청이 제공한 타입을 하나도 허용하지 않으면 `null`을 반환합니다:

```
$preferred = $request->prefers(['text/html', 'application/json']);
```

대부분 애플리케이션이 HTML 또는 JSON만 제공하는 경우가 많으므로, `expectsJson` 메서드를 사용하면 들어오는 요청이 JSON 응답을 기대하는지 빠르게 판별할 수 있습니다:

```
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청과 응답)에 대한 인터페이스를 정의합니다. 만약 Laravel 요청 대신 PSR-7 요청 인스턴스를 받고 싶다면, 몇 가지 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 일반 Laravel 요청과 응답을 PSR-7 호환 구현으로 변환합니다:

```
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리들을 설치한 뒤에는, 라우트 클로저나 컨트롤러 메서드에서 요청 인터페이스를 타입힌트해 PSR-7 요청을 받을 수 있습니다:

```
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    //
});
```

> [!TIP]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 Laravel 응답 인스턴스로 변환해 표시합니다.

<a name="input"></a>
## 입력 (Input)

<a name="retrieving-input"></a>
### 입력 데이터 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기

`all` 메서드를 사용하면 들어오는 요청의 모든 입력 데이터를 배열 형태로 가져올 수 있습니다. 이 메서드는 HTML 폼이나 XHR 요청인지에 상관없이 사용할 수 있습니다:

```
$input = $request->all();
```

`collect` 메서드를 사용하면 들어오는 요청의 모든 입력 데이터를 [컬렉션](/docs/{{version}}/collections) 형태로 가져올 수 있습니다:

```
$input = $request->collect();
```

`collect` 메서드는 입력 데이터의 일부만 컬렉션으로 가져오는 것도 지원합니다:

```
$request->collect('users')->each(function ($user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 입력 값 가져오기

몇 가지 간단한 메서드를 사용해 HTTP 메서드에 상관없이 `Illuminate\Http\Request` 인스턴스에서 사용자 입력을 모두 접근할 수 있습니다. `input` 메서드는 HTTP 메서드와 무관하게 입력 값을 가져올 수 있습니다:

```
$name = $request->input('name');
```

`input` 메서드의 두 번째 인자로 기본값을 전달할 수 있습니다. 요청에 해당 입력 값이 없을 때 기본값이 반환됩니다:

```
$name = $request->input('name', 'Sally');
```

배열 입력이 포함된 폼에서는 "점(dot)" 표기법을 사용해 배열 요소에 접근합니다:

```
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인수 없이 `input` 메서드를 호출하면 모든 입력 값을 연관 배열 형태로 가져옵니다:

```
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력 가져오기

`input` 메서드는 전체 요청 페이로드(쿼리 문자열 포함)에서 값을 가져오는 반면, `query` 메서드는 쿼리 문자열에서만 값을 가져옵니다:

```
$name = $request->query('name');
```

요청에 해당 쿼리 문자열 값이 없으면 두 번째 인자의 기본값이 반환됩니다:

```
$name = $request->query('name', 'Helen');
```

인수 없이 `query` 메서드를 호출하면 모든 쿼리 문자열 값을 연관 배열로 가져옵니다:

```
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력 값 가져오기

애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있으면 `input` 메서드를 통해 JSON 데이터를 접근할 수 있습니다. "점(dot)" 구문을 사용해 중첩된 JSON 배열 내 값을 가져올 수도 있습니다:

```
$name = $request->input('user.name');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력 값 가져오기

체크박스와 같은 HTML 요소를 다룰 때 "true", "on" 등의 문자열로 진위 값을 받을 수 있습니다. `boolean` 메서드를 사용하면 이 값을 불리언으로 변환할 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"를 `true`로 처리하며, 나머지는 모두 `false`로 반환합니다:

```
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력 값 가져오기

날짜/시간이 포함된 입력 값은 `date` 메서드를 통해 Carbon 인스턴스로 편리하게 가져올 수 있습니다. 만약 이름에 해당하는 입력 값이 없으면 `null`을 반환합니다:

```
$birthday = $request->date('birthday');
```

`date` 메서드의 두 번째와 세 번째 인자로 각각 날짜 형식과 타임존을 지정할 수 있습니다:

```
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력 값이 있지만 형식이 올바르지 않으면 `InvalidArgumentException` 예외가 발생하므로, `date` 메서드를 호출하기 전에 입력 값을 검증하는 것이 좋습니다.

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티로 입력 값 가져오기

`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티를 통해 사용자 입력에 접근할 수도 있습니다. 예를 들어, `name` 필드를 포함하는 폼이 있다면 다음과 같이 값을 얻을 수 있습니다:

```
$name = $request->name;
```

동적 프로퍼티 사용 시, Laravel은 먼저 요청 페이로드에서 해당 파라미터를 찾고, 없다면 매칭된 라우트의 파라미터를 검색합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터 일부분 가져오기

입력 데이터의 일부만 얻고 싶을 때는 `only` 또는 `except` 메서드를 사용할 수 있습니다. 두 메서드 모두 배열이나 가변 인수를 받습니다:

```
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!NOTE]
> `only` 메서드는 요청에 존재하는 키/값 쌍만 반환하며, 요청에 없는 키는 결과에 포함하지 않습니다.

<a name="determining-if-input-is-present"></a>
### 입력 존재 여부 확인

`has` 메서드는 요청에 값이 존재하는지 확인합니다. 해당 값이 있으면 `true`를 반환합니다:

```
if ($request->has('name')) {
    //
}
```

배열을 인자로 전달하면, 지정한 모든 값이 존재하는지 검사합니다:

```
if ($request->has(['name', 'email'])) {
    //
}
```

`whenHas` 메서드는 특정 값이 존재할 때 주어진 클로저를 실행합니다:

```
$request->whenHas('name', function ($input) {
    //
});
```

두 번째 클로저를 전달하면 해당 값이 없을 때 실행할 콜백으로 사용됩니다:

```
$request->whenHas('name', function ($input) {
    // "name" 값이 존재할 때...
}, function () {
    // "name" 값이 없을 때...
});
```

`hasAny` 메서드는 지정한 값 중 하나라도 존재하면 `true`를 반환합니다:

```
if ($request->hasAny(['name', 'email'])) {
    //
}
```

값이 존재하고 비어 있지 않은지 확인하려면 `filled` 메서드를 사용할 수 있습니다:

```
if ($request->filled('name')) {
    //
}
```

`whenFilled` 메서드는 해당 값이 존재하고 비어 있지 않을 때 클로저를 실행합니다:

```
$request->whenFilled('name', function ($input) {
    //
});
```

두 번째 클로저를 전달하면, 값이 "filled"하지 않을 때 실행됩니다:

```
$request->whenFilled('name', function ($input) {
    // "name" 값이 채워졌을 때...
}, function () {
    // "name" 값이 채워지지 않았을 때...
});
```

키가 요청에 없음을 확인하려면 `missing` 메서드를 사용할 수 있습니다:

```
if ($request->missing('name')) {
    //
}
```

<a name="merging-additional-input"></a>
### 추가 입력 병합하기

가끔 요청의 기존 입력 데이터에 추가 입력을 수동으로 병합해야 할 때가 있습니다. 이럴 때는 `merge` 메서드를 사용하세요:

```
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 대응되는 키가 요청 입력 데이터에 없을 때에만 입력을 병합합니다:

```
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력

Laravel은 한 요청의 입력을 다음 요청에서 유지할 수 있습니다. 이 기능은 특히 유효성 검증 오류가 발생했을 때 폼을 다시 채울 때 유용합니다. 다만 Laravel 내장 [유효성 검증 기능](/docs/{{version}}/validation)을 사용할 경우, 수동으로 세션에 입력을 플래시할 필요가 없는 경우가 많습니다.

<a name="flashing-input-to-the-session"></a>
#### 세션에 입력 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력을 [세션](/docs/{{version}}/session)에 플래시 처리해서, 사용자가 다음 요청 때 입력에 접근할 수 있게 만듭니다:

```
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드를 사용해, 요청 데이터의 일부만 세션에 플래시할 수도 있습니다. 이 메서드들은 비밀번호 등 민감한 정보를 세션에 저장하지 않게 할 때 유용합니다:

```
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력 플래시 후 리다이렉트하기

입력 데이터를 세션에 플래시한 후 이전 페이지로 리다이렉트하는 경우가 많은데, `withInput` 메서드를 사용해 리다이렉트에 플래시를 쉽게 체인할 수 있습니다:

```
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력 값 가져오기

이전 요청에서 플래시된 입력을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 됩니다. `old` 메서드는 이전 요청의 플래시된 입력 데이터를 [세션](/docs/{{version}}/session)에서 꺼내옵니다:

```
$username = $request->old('username');
```

Laravel은 전역적인 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/{{version}}/blade)에서 이전 입력 값을 폼에 다시 채울 때, `old` 헬퍼를 사용하는 것이 더 편리합니다. 해당 필드의 이전 입력이 없으면 `null`이 반환됩니다:

```
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel에서 생성된 모든 쿠키는 암호화 및 인증 코드가 서명되어 있어, 클라이언트가 변경한 경우 무효로 간주됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요:

```
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력 트리밍 및 정규화

기본적으로 Laravel은 애플리케이션의 글로벌 미들웨어 스택에서 `App\Http\Middleware\TrimStrings`와 `App\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어들은 `App\Http\Kernel` 클래스의 글로벌 미들웨어 스택에 등록되어 있습니다. 이들은 요청의 모든 문자열 필드를 자동으로 트리밍하고, 빈 문자열을 `null`로 변환해 줍니다. 이 기능을 통해 라우트나 컨트롤러에서 입력 정규화에 신경 쓸 필요가 없습니다.

이 동작을 비활성화하고 싶다면, 애플리케이션의 미들웨어 스택에서 해당 두 미들웨어를 `App\Http\Kernel` 클래스의 `$middleware` 프로퍼티에서 제거하면 됩니다.

<a name="files"></a>
## 파일

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기

`Illuminate\Http\Request` 인스턴스에서 `file` 메서드나 동적 프로퍼티를 사용해 업로드된 파일을 가져올 수 있습니다. `file` 메서드는 PHP의 `SplFileInfo` 클래스를 확장하고 파일과 관련된 여러 메서드를 제공하는 `Illuminate\Http\UploadedFile` 인스턴스를 반환합니다:

```
$file = $request->file('photo');

$file = $request->photo;
```

`hasFile` 메서드를 사용해 요청에 파일이 존재하는지 확인할 수 있습니다:

```
if ($request->hasFile('photo')) {
    //
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증

파일이 존재하는지 확인하는 것 외에, `isValid` 메서드를 사용하면 파일 업로드에 문제가 없었는지 검증할 수 있습니다:

```
if ($request->file('photo')->isValid()) {
    //
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스는 파일의 절대 경로와 확장자를 얻는 메서드도 제공합니다. `extension` 메서드는 파일 내용을 기반으로 확장자를 추측합니다. 이 확장자는 클라이언트가 보낸 확장자와 다를 수 있습니다:

```
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에서는 그 외에도 다양한 메서드를 사용할 수 있습니다. 자세한 내용은 [해당 클래스의 API 문서](https://api.symfony.com/master/Symfony/Component/HttpFoundation/File/UploadedFile.html)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기

업로드된 파일을 저장하려면 보통 구성한 [파일시스템](/docs/{{version}}/filesystem) 중 하나를 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 파일을 지정한 디스크(로컬 파일시스템 또는 Amazon S3 같은 클라우드 저장소)로 이동시킵니다.

`store` 메서드는 파일을 저장할 경로(파일시스템의 루트 디렉토리 기준)를 인수로 받습니다. 이 경로에는 파일명이 포함되지 않아야 하며, 파일명은 고유 ID가 자동 생성됩니다.

두 번째 인수로 저장할 디스크의 이름을 지정할 수 있습니다. 이 메서드는 디스크 루트 기준 파일 경로를 반환합니다:

```
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

자동으로 파일명이 생성되길 원하지 않을 경우, `storeAs` 메서드를 사용하면 경로, 파일명, 디스크 이름을 직접 지정할 수 있습니다:

```
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!TIP]
> Laravel의 파일 저장 관련 자세한 내용은 [파일 저장 문서](/docs/{{version}}/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정하기

TLS/SSL 인증서 종료(load balancer 뒤에서 운영하는) 환경의 애플리케이션은 `url` 헬퍼를 사용할 때 HTTPS 링크가 생성되지 않는 문제를 경험할 수 있습니다. 이는 보통 로드 밸런서가 포트 80에서 트래픽을 전달하여, 애플리케이션이 보안 링크를 생성해야 하는지 알지 못하기 때문입니다.

이를 해결하려면, Laravel 애플리케이션에 포함된 `App\Http\Middleware\TrustProxies` 미들웨어를 사용해 신뢰할 프록시 또는 로드 밸런서를 간편하게 설정할 수 있습니다. `TrustProxies` 미들웨어에서 `$proxies` 프로퍼티에 신뢰할 프록시 목록을 배열로 지정하세요. 신뢰할 프록시를 설정하는 것 외에도, 신뢰할 프록시를 탐지하는 데 사용할 `$headers`도 설정할 수 있습니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * 애플리케이션의 신뢰할 프록시 목록.
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
    protected $headers = Request::HEADER_X_FORWARDED_FOR 
        | Request::HEADER_X_FORWARDED_HOST 
        | Request::HEADER_X_FORWARDED_PORT 
        | Request::HEADER_X_FORWARDED_PROTO;
}
```

> [!TIP]
> AWS Elastic Load Balancing을 사용하는 경우, `$headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`여야 합니다. `$headers` 프로퍼티에 사용할 수 있는 상수들은 Symfony 문서의 [trusting proxies](https://symfony.com/doc/current/deployment/proxies.html)에서 자세히 확인할 수 있습니다.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS나 다른 클라우드 로드 밸런서를 사용할 경우, 실제 로드 밸런서 IP 주소를 모르는 일이 많습니다. 이럴 때는 다음과 같이 `*`를 사용해 모든 프록시를 신뢰할 수 있습니다:

```
/**
 * 애플리케이션의 신뢰할 프록시 목록.
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정하기

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 값과 관계없이 모든 요청에 응답합니다. 또한, `Host` 헤더 값을 웹 요청 처리 시 절대 URL 생성에 사용합니다.

보통은 Nginx, Apache 같은 웹 서버에서 특정 호스트 이름에만 요청을 애플리케이션으로 전달하도록 설정하는 것이 바람직합니다. 그러나 직접 웹 서버 설정을 변경할 수 없는 경우나, Laravel이 특정 호스트 이름에만 응답하도록 설정해야 할 경우 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화해 설정할 수 있습니다.

`TrustHosts` 미들웨어는 이미 애플리케이션의 `$middleware` 스택에 포함되어 있지만, 주석 처리되어 있어 활성화가 필요합니다. 이 미들웨어의 `hosts` 메서드에서 애플리케이션이 응답할 호스트 이름을 지정할 수 있습니다. 지정한 호스트 이외 요청은 거부됩니다:

```
/**
 * 신뢰할 호스트 패턴을 가져옵니다.
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

`allSubdomainsOfApplicationUrl` 헬퍼 메서드는 애플리케이션의 `app.url` 구성 값의 모든 하위 도메인과 일치하는 정규식을 반환합니다. 와일드카드 하위 도메인 기능을 활용하는 애플리케이션에서 모든 하위 도메인을 쉽게 허용할 수 있게 도와줍니다.