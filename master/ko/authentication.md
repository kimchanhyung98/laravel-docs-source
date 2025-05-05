# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한(Throttle)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증](#http-basic-authentication)
    - [Stateless HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호하기](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 제공자 추가](#adding-custom-user-providers)
    - [사용자 제공자 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해시](#automatic-password-rehashing)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 방법을 제공합니다. 이 기능을 웹 애플리케이션에 구현하는 것은 복잡하고 위험할 수 있습니다. 이러한 이유로 Laravel은 인증을 빠르고, 안전하게, 그리고 쉽게 구현할 수 있는 다양한 도구를 제공합니다.

Laravel의 인증 시스템은 기본적으로 "가드(guards)"와 "프로바이더(providers)"로 구성되어 있습니다. 가드는 각 요청에서 사용자가 어떻게 인증되는지를 정의합니다. 예를 들어, Laravel에는 세션 저장소와 쿠키를 이용해 상태를 관리하는 `session` 가드가 기본으로 제공됩니다.

프로바이더는 사용자를 영구 저장소에서 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/{{version}}/eloquent)와 데이터베이스 쿼리 빌더를 사용한 사용자 조회를 지원합니다. 필요하다면 추가적인 프로바이더를 자유롭게 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel 인증 서비스의 동작 방식을 조정할 수 있는 여러 옵션이 잘 설명되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(roles)"과 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통한 사용자 액션 승인(authorizing)에 대해 더 알고 싶다면 [권한(authorization)](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 앱에 할당된 다른 URL로 이동하면 스타터 키트가 전체 인증 시스템의 스캐폴딩을 자동으로 처리해줍니다!

**최종적으로 스타터 키트를 사용하지 않을 계획이라 해도, [스타터 키트](/docs/{{version}}/starter-kits)를 설치하여 실제 Laravel 프로젝트에서 인증 기능이 어떻게 구현되는지 학습하는 데 큰 도움이 됩니다.** 스타터 키트에는 인증 컨트롤러, 라우트, 뷰가 모두 포함되어 있으니 직접 그 코드를 살펴보면서 구현 방법을 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버에서 사용할 수 있습니다.

애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우에는 MongoDB 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델의 데이터베이스 스키마를 만들 때, 비밀번호 컬럼의 길이가 최소 60자는 되어야 합니다. 기본 제공되는 `users` 테이블 마이그레이션은 이미 이 조건을 충족하므로 추가 조치가 필요 없습니다.

또한, `users`(또는 동등한) 테이블에 100자 길이의 널 허용 문자열(nullable string) 컬럼인 `remember_token`도 포함되어 있는지 확인해야 합니다. 이 컬럼은 사용자가 로그인 시 "로그인 상태 유지(remember me)"를 선택할 때 토큰을 저장하는 데 사용됩니다. 역시, 기본 제공 `users` 테이블 마이그레이션에 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속해서 진행하기 전에, Laravel의 전반적인 인증 에코시스템을 간단히 살펴보고 각 패키지의 목적에 대해 논의하겠습니다.

먼저 인증이 어떻게 작동하는지 생각해봅시다. 웹 브라우저를 사용할 때 사용자는 로그인 폼에 사용자명과 비밀번호를 입력합니다. 올바른 자격 증명이라면 애플리케이션은 [세션](/docs/{{version}}/session)에 인증된 사용자 정보를 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 저장되며, 이후의 요청에서 해당 사용자를 올바른 세션에 연결할 수 있게 해줍니다. 세션 쿠키가 수신되면 애플리케이션은 세션 데이터를 불러와 인증된 사용자의 정보를 확인하고 인증된 것으로 간주합니다.

외부 서비스가 API에 접근하기 위해 인증해야 할 경우에는 (웹 브라우저가 없기 때문에) 쿠키 대신 각 요청에 API 토큰을 전송합니다. 애플리케이션은 유효한 토큰 목록과 대조하여 요청을 인증하고, 해당 토큰에 연결된 사용자로 요청을 처리합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel은 일반적으로 `Auth`와 `Session` 파사드를 통해 접근되는 내장 인증과 세션 기능을 제공합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 검증하고 인증하는 메서드가 제공되며, 인증에 성공하면 자동으로 사용자의 세션에 정보를 저장하고 세션 쿠키를 발급합니다. 이 문서에서 이 특징들을 어떻게 활용하는지 자세히 다룹니다.

**애플리케이션 스타터 키트**

이 문서에서 다루듯, 이러한 인증 기능을 수동으로 활용하여 여러분만의 인증 계층을 구축할 수 있습니다. 그러나 더 빠르게 시작하고 싶다면, 전체 인증 계층의 현대적인 스캐폴딩을 제공하는 [무료 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰을 관리하고 토큰 기반 요청을 인증하는 데 도움이 되는 두 개의 선택적 패키지, [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum)을 제공합니다. 이 라이브러리들과 Laravel의 쿠키 기반 인증 시스템은 상호 배타적이지 않습니다. 이 패키지들은 주로 API 토큰 인증에, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 초점을 둡니다. 많은 애플리케이션이 쿠키 기반 서비스와 API 인증 패키지 모두를 사용할 수 있습니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"을 제공하는 OAuth2 인증 공급자입니다. 복잡하고 다양한 API 인증 시나리오에 유용한 robust 패키지이지만, 대부분의 애플리케이션에서는 OAuth2 사양의 복잡한 기능들이 필요하지 않고, 많은 개발자와 사용자에게는 오히려 혼란을 줄 수 있습니다. SPA나 모바일 앱에서 Passport 같은 OAuth2 인증을 어떻게 사용하는지 혼동하는 경우도 많습니다.

**Sanctum**

OAuth2의 복잡함과 개발자 혼동에 대응하여, 웹 브라우저의 1차 요청과 API 토큰 기반 요청을 모두 처리할 수 있는, 더 간결하고 단순화된 인증 패키지로 [Laravel Sanctum](/docs/{{version}}/sanctum)이 탄생했습니다. Sanctum은 1차 웹 UI와 API를 함께 제공하거나, 백엔드와 분리된 SPA, 모바일 클라이언트가 필요한 애플리케이션에 권장되는 인증 패키지입니다.

Sanctum은 웹/ API 하이브리드 인증 패키지이기 때문에 인증 전체 프로세스를 관리할 수 있습니다. Sanctum 기반 애플리케이션은 요청이 들어오면 먼저 세션 쿠키를 확인해 인증된 세션인지 판별하고, 그렇지 않으면 API 토큰을 찾아 인증하는 구조입니다. 자세한 동작은 Sanctum의 ["작동 방식"](/docs/{{version}}/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

요약하면, 애플리케이션이 브라우저에서 접근되고 모놀리식 Laravel 애플리케이션을 구축한다면, Laravel의 내장 인증 서비스를 사용하면 됩니다.

API도 제공해야 한다면, [Passport](/docs/{{version}}/passport) 또는 [Sanctum](/docs/{{version}}/sanctum) 중에서 선택하여 API 토큰 인증을 구현할 수 있습니다. 일반적으로, Sanctum이 더 단순하고 SPA, 모바일 인증 등 폭넓은 시나리오를 지원하기 때문에 추천드립니다.

Laravel 백엔드를 기반으로 하는 SPA라면, 역시 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하세요. 이 경우, [직접 인증 라우트 구현](#authenticating-users) 또는 [Laravel Fortify](/docs/{{version}}/fortify)를 헤드리스 인증 백엔드로 활용할 수도 있습니다.

반드시 OAuth2 표준의 복잡한 모든 기능이 필요한 경우에만 Passport를 고려하세요.

빠른 시작이 필요하다면, [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하여 권장 인증 스택이 적용된 새로운 Laravel 프로젝트를 바로 시작하세요.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작

> [!WARNING]
> 이 문서의 본 섹션에서는 인증 UI 스캐폴딩이 포함된 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)로 사용자 인증을 다룹니다. 인증 시스템을 직접 통합하고 싶다면, [수동 인증 사용](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 스타터 키트는 인증이 포함된 아름다운 디자인의 출발점을 제공해줍니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 키트로 생성한 앱에서 사용자가 회원가입 및 인증을 완료했다면, 현재 인증된 사용자와 상호작용해야 할 일이 자주 있습니다. 요청을 처리할 때, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자를 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회
$user = Auth::user();

// 현재 인증된 사용자의 ID 조회
$id = Auth::id();
```

또는, 인증이 완료된 후에는 `Illuminate\Http\Request` 인스턴스를 통해서도 인증 사용자에 접근할 수 있습니다. 컨트롤러 메서드에서 타입 힌트로 `Illuminate\Http\Request` 객체를 주입받으면 `user` 메서드를 활용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 비행 정보를 업데이트합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
#### 현재 사용자가 인증되었는지 확인하기

들어온 HTTP 요청을 한 사용자가 인증 상태인지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 사용자가 인증 상태라면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인 상태입니다.
}
```

> [!NOTE]
> 실제로는 `check` 메서드로 인증 여부를 확인하는 것보다는, 미들웨어로 보호할 라우트에 인증을 요구하는 것이 일반적입니다. 자세한 내용은 [라우트 보호하기](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/{{version}}/middleware)를 이용해 특정 라우트에 인증된 사용자만 접근을 허용할 수 있습니다. Laravel은 `auth` 미들웨어를 기본 제공하며, 이 미들웨어는 `Illuminate\Auth\Middleware\Authenticate`의 [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)입니다. 별칭이 이미 설정되어 있으니, 단순히 라우트에 미들웨어를 붙이면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 미인증 사용자 리다이렉트

`auth` 미들웨어는 미인증 사용자가 접근하면 자동으로 `login` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트합니다. 이 동작은 `bootstrap/app.php`에서 `redirectGuestsTo`로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저 사용
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리다이렉트

`guest` 미들웨어가 인증된 사용자를 만나면, 자동으로 `dashboard` 혹은 `home` 네임드 라우트로 리다이렉트합니다. 이 동작 역시 `redirectUsersTo`로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저 사용
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 붙일 때, 어떤 "가드"를 사용할지도 명시할 수 있습니다. 이때 지정하는 가드 이름은 `auth.php`의 `guards` 배열의 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // admin 가드로 인증된 사용자만 접근 가능
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한(Throttle)

[스타터 키트](/docs/{{version}}/starter-kits)를 사용한다면 로그인 시도에도 자동으로 레이트 제한이 적용됩니다. 기본값으로 올바른 자격 증명을 여러 번 실패하면 1분 동안 로그인을 할 수 없게 됩니다. 제한은 사용자명(이메일)과 IP 주소별로 적용됩니다.

> [!NOTE]
> 다른 라우트도 제한하고 싶다면, [레이트 제한 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증

[스타터 키트](/docs/{{version}}/starter-kits)에 포함된 인증 스캐폴딩을 반드시 사용할 필요는 없습니다. 사용하지 않는다면 Laravel의 인증 클래스를 직접 사용해 사용자 인증 로직을 구현해야 합니다. 걱정하지 마세요. 매우 간단합니다!

Laravel 인증 서비스를 사용할 때는 `Auth` [파사드](/docs/{{version}}/facades)를 활용합니다. 먼저, 클래스 상단에 `Auth` 파사드를 임포트하고, 인증 시도를 처리하는 `attempt` 메서드를 확인합시다. 보통 애플리케이션의 "로그인" 폼에서 인증에 사용합니다. 인증이 성공하면 [세션](/docs/{{version}}/session)을 재생성하여 [세션 고정(session fixation)](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * 인증 시도 처리
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => '입력한 자격 증명이 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt`는 키-값 쌍의 배열을 첫 번째 인자로 받습니다. 이 배열을 이용해 데이터베이스에서 사용자를 찾고, 비밀번호 칼럼의 해시값과 입력값을 비교합니다. 비밀번호는 직접 해시하지 않아도 되며, 프레임워크가 알아서 해시 후 DB와 비교합니다. 두 비밀번호가 일치하면 인증된 세션이 시작됩니다.

사용자 조회는 인증 가드의 "provider" 설정에 따라 진행됩니다. 기본 `config/auth.php`에는 Eloquent 사용자 프로바이더와 `App\Models\User` 모델이 등록되어 있으므로 필요에 따라 변경하시면 됩니다.

`attempt`는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

`intended` 메서드는 인증 미들웨어에 가로챈 후 접근하려던 URL로 사용자를 리다이렉트해줍니다. 대체 URI도 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

원한다면 `attempt`의 배열 인자에 이메일, 비밀번호 외에 추가 쿼리 조건을 넣을 수도 있습니다. 예를 들어, 사용자가 "active"한지도 확인할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공
}
```

복잡한 쿼리 조건이 필요할 때는, 배열 내에 클로저를 넘겨 커스텀 쿼리를 적용할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // 인증 성공
}
```

> [!WARNING]
> 위 예시에서 `email`은 반드시 필요한 옵션이 아니라 예시로 사용했습니다. 데이터베이스에서 "username" 역할을 하는 컬럼명을 사용하세요.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아, 인증 전에 후보 사용자를 더 철저히 검사할 수 있습니다. 클로저는 후보 사용자 인스턴스를 받아 true/false를 반환해야 합니다:

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // 인증 성공
}
```

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 사용하기

`Auth` 파사드의 `guard` 메서드를 이용하면 인증 시 사용할 가드 인스턴스를 직접 지정할 수 있습니다. 이를 통해 앱의 서로 다른 부분에서 다른 인증 모델/테이블을 사용할 수 있습니다.

`guard`에 넘기는 가드 이름은 `auth.php`의 설정과 일치해야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기("Remember Me")

많은 웹 앱에서는 로그인 폼에 "로그인 상태 유지" 체크박스를 제공합니다. 이 기능을 추가하려면 `attempt`의 두 번째 인자에 boolean 값을 넘기면 됩니다.

이 값이 `true`라면, Laravel은 사용자가 직접 로그아웃하기 전까지 인증 상태를 유지합니다. `users` 테이블에는 "remember_token" 칼럼이 포함되어 있어야 하며, 기본 마이그레이션에 이미 추가되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억됨
}
```

이 기능이 있다면, 현재 인증된 사용자가 "로그인 상태를 유지"로 인증되었는지 확인하려면 `viaRemember` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 로그인

이미 존재하는 사용자 인스턴스를 인증된 사용자로 지정하고 싶다면, 그 인스턴스를 `Auth` 파사드의 `login` 메서드에 넘기세요. 주어진 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/{{version}}/contracts)을 구현해야 하며, Laravel의 `App\Models\User`는 이미 구현되어 있습니다. 이는 예를 들어 회원 가입 직후 곧바로 인증 처리에 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

두 번째 인자에 boolean 값을 넘기면 "로그인 상태 유지" 여부를 조정할 수 있습니다:

```php
Auth::login($user, $remember = true);
```

필요하다면, 로그인 전에 인증 가드도 지정할 수 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증

데이터베이스의 주키(primary key)로 사용자를 인증하려면 `loginUsingId` 메서드를 사용하세요:

```php
Auth::loginUsingId(1);
```

이 메서드의 `remember` 인자에 boolean을 넘기면 "로그인 상태 유지" 옵션을 적용할 수 있습니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 1회성 사용자 인증

`once` 메서드는 한 번의 요청에만 유효한 인증을 하고, 세션이나 쿠키를 사용하지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지를 만들지 않고 빠르게 인증 기능을 구현할 수 있습니다. 시작하려면, `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 라우트에 붙이세요. 이 미들웨어는 Laravel 프레임워크에 포함되어 있으니 따로 정의하지 않아도 됩니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth.basic');
```

미들웨어가 붙으면 라우트에 접근할 때 자동으로 브라우저가 자격 증명을 요구합니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 "사용자명"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 주의

PHP FastCGI와 Apache 조합에서 HTTP 기본 인증이 정상동작하지 않을 수 있습니다. 이 경우, 앱의 `.htaccess` 파일에 아래 코드를 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP 기본 인증

세션에 사용자 식별 쿠키를 설정하지 않고 HTTP 기본 인증을 사용할 수도 있습니다. 이는 API 인증에 유용합니다. [미들웨어를 정의](/docs/{{version}}/middleware)해 `onceBasic` 메서드를 호출하도록 만드세요. 응답이 반환되지 않으면 요청은 애플리케이션의 다음 단계로 넘어갑니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * 들어오는 요청을 처리합니다.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

그 후, 이 미들웨어를 라우트에 붙이세요:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃

사용자를 애플리케이션에서 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 인증 정보를 세션에서 제거하여 이후 요청 시 더 이상 인증 상태가 되지 않도록 합니다.

`logout` 호출 후에는 세션을 무효화하고 [CSRF 토큰](/docs/{{version}}/csrf)도 재생성하는 것이 좋습니다. 로그아웃 후 보통 루트 라우트로 리다이렉트합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 로그아웃 처리
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
### 다른 기기의 세션 무효화

Laravel은 다른 기기(브라우저 등)의 세션을 무효화하면서 현재 기기의 인증은 유지하는 기능도 제공합니다. 이 기능은 사용자가 비밀번호를 변경할 때, 다른 모든 기기에서 강제로 로그아웃시키고자 할 때 유용합니다.

먼저, 세션 인증을 적용할 라우트에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 포함되었는지 확인하세요. 보통 라우트 그룹에 붙이면 대부분의 라우트에 쉽게 적용할 수 있습니다. 기본적으로 `auth.session` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)으로 등록되어 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 후, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 사용자가 현재 비밀번호를 한번 더 입력해야 하므로, 입력 폼을 구현해야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 실행되면 해당 사용자의 다른 모든 세션(가드 포함)이 완전히 무효화되어 강제 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인

앱에서 민감한 영역에 접근하거나 중요한 액션을 수행하기 전에 사용자의 비밀번호를 다시 한 번 확인하고 싶을 때가 있습니다. Laravel은 이 작업을 매우 쉽게 할 수 있는 내장 미들웨어를 제공합니다. 이 기능을 사용하려면, 비밀번호 확인 화면을 보여주는 라우트와, 입력된 비밀번호가 올바른지 확인 후 원하는 위치로 리다이렉트하는 라우트 두 개가 필요합니다.

> [!NOTE]
> 아래 문서는 이 기능을 수동으로 통합하는 방법을 다룹니다. 더 빠른 시작을 원한다면 [스타터 키트](/docs/{{version}}/starter-kits)에서도 지원됩니다!

<a name="password-confirmation-configuration"></a>
### 설정

사용자가 비밀번호를 확인하고 나면 3시간 동안 다시 묻지 않습니다. 이 시간 간격은 `config/auth.php`의 `password_timeout` 값을 변경해서 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 비밀번호 확인 뷰를 보여주는 라우트를 정의합시다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트가 반환하는 뷰에는 `password` 필드가 있는 폼이 있어야 하며, 민감 영역임을 안내하는 텍스트도 자유롭게 추가하세요.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, 폼 요청을 처리할 라우트를 정의합니다. 이 라우트는 비밀번호를 검증하고, 사용자를 원하는 위치로 리다이렉트합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['입력한 비밀번호가 일치하지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

우선 요청받은 비밀번호가 실제 인증된 사용자와 일치하는지 확인하고, 일치하면 Laravel 세션에 비밀번호 확인 시간을 기록합니다(`passwordConfirmed`). 이로써 사용자가 마지막으로 언제 비밀번호를 확인했는지 알 수 있으며, 이후엔 원하는 위치로 리다이렉트할 수 있습니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호하기

비밀번호 재확인이 필요한 라우트에는 반드시 `password.confirm` 미들웨어를 지정해야 합니다. 이 미들웨어는 기본적으로 사용자 의도 목적지(location)을 세션에 저장하여, 비밀번호 확인 후 해당 위치로 바로 보내줄 수 있도록 해줍니다:

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가

`Auth` 파사드의 `extend` 메서드를 사용해 직접 인증 가드를 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/{{version}}/providers) 내에 배치해야 하며, 기본 제공되는 `AppServiceProvider`가 적합합니다:

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * 어플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 인스턴스 반환
            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시처럼, `extend`에 넘기는 콜백은 `Illuminate\Contracts\Auth\Guard`를 구현해야 합니다. 해당 인터페이스의 메서드를 구현한 후, `auth.php`의 `guards` 설정에서 아래처럼 참조할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 요청 가드

클로저 하나로 간단히 HTTP 요청 기반 커스텀 인증 시스템을 구현하려면, `Auth::viaRequest` 메서드를 사용하세요.

`AppServiceProvider`의 `boot` 안에서 `viaRequest` 메서드를 호출하며, 첫 인자는 인증 드라이버 이름(임의), 두 번째 인자는 요청을 받아 사용자 인스턴스 또는 null을 반환하는 클로저입니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 어플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

정의 후에는 `auth.php`에 아래처럼 등록하세요:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 미들웨어에서 해당 가드를 쓸 수 있습니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 제공자 추가

관계형 데이터베이스가 아닌 다른 저장소를 쓸 때는 직접 사용자 제공자(User Provider)를 확장해야 합니다. 이를 위해 `Auth` 파사드의 `provider` 메서드를 활용하세요. 반환값은 반드시 `Illuminate\Contracts\Auth\UserProvider`를 구현해야 합니다:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * 어플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 인스턴스 반환
            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider`로 등록 후, `auth.php`에서 아래처럼 지정하세요:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그리고 가드에서 해당 provider를 참조합니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### 사용자 제공자 계약

`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 객체를 MySQL, MongoDB 등 영구 저장소에서 조회해 반환해야 합니다. 이 두 인터페이스 덕분에, 사용자 저장 방식과 상관없이 Laravel의 인증 메커니즘이 항상 동작할 수 있습니다.

다음은 `UserProvider` 계약입니다:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```

| 메서드  | 용도  |
|--------|-------|
| `retrieveById` | 사용자 대표값(예: MySQL 자동증가 키)으로 사용자 조회 |
| `retrieveByToken` | $identifier와 "remember me" $token으로 사용자 조회 |
| `updateRememberToken` | 사용자 인스턴스에 새로운 remember_token 할당 |
| `retrieveByCredentials` | Auth::attempt 등으로 전달된 자격 정보로 사용자 조회(단, 비밀번호 검증은 여기서 하면 안 됨) |
| `validateCredentials` | 주어진 User와 $credentials를 비교해 인증 여부 반환(보통 Hash::check 사용) |
| `rehashPasswordIfRequired` | 필요/지원 시, 사용자 비밀번호를 재해시함 |

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

`UserProvider`에서 사용자 객체를 반환할 때, 반드시 `Authenticatable` 인터페이스를 구현해야 합니다:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

| 메서드  | 용도  |
|--------|-------|
| `getAuthIdentifierName` | 사용자 "주키" 컬럼명 반환 |
| `getAuthIdentifier` | 사용자 "주키" 값 반환(예: id) |
| `getAuthPasswordName` | 비밀번호 컬럼명 반환 |
| `getAuthPassword` | 비밀번호 해시값 반환 |
| 그 외 remember_token getter/setter 등 |

이 인터페이스 덕분에, 어떤 "사용자" 클래스와 ORM, 스토리지든 상관없이 시스템 동작을 보장할 수 있습니다. Laravel에서는 `app/Models/User`가 이 인터페이스를 구현하여 기본 제공됩니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해시

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt의 "work factor"는 `config/hashing.php` 또는 `BCRYPT_ROUNDS` 환경 변수를 통해 조정할 수 있습니다.

컴퓨팅 성능이 향상될 때마다 work factor를 조금씩 올려주는 것이 좋으며, 값을 변경해도 사용자들이 로그인할 때 자동으로 비밀번호 재해시가 적용됩니다(스타터 키트로 로그인하거나, [수동 인증](#authenticating-users)의 attempt 사용 시).

만약 이 동작이 필요 없다면, `hashing` 설정 파일을 퍼블리시하세요:

```shell
php artisan config:publish hashing
```

출력된 설정 파일의 `rehash_on_login` 값을 false로 변경하세요:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트

Laravel은 인증 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 아래 이벤트 중 필요한 곳에 [리스너](/docs/{{version}}/events)를 등록할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Auth\Events\Registered` |
| `Illuminate\Auth\Events\Attempting` |
| `Illuminate\Auth\Events\Authenticated` |
| `Illuminate\Auth\Events\Login` |
| `Illuminate\Auth\Events\Failed` |
| `Illuminate\Auth\Events\Validated` |
| `Illuminate\Auth\Events\Verified` |
| `Illuminate\Auth\Events\Logout` |
| `Illuminate\Auth\Events\CurrentDeviceLogout` |
| `Illuminate\Auth\Events\OtherDeviceLogout` |
| `Illuminate\Auth\Events\Lockout` |
| `Illuminate\Auth\Events\PasswordReset` |

</div>