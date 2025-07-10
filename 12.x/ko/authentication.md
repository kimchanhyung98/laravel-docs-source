# 인증(Authentication)

- [소개](#introduction)
    - [스타터 킷](#starter-kits)
    - [데이터베이스 고려 사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠르게 시작하기](#authentication-quickstart)
    - [스타터 킷 설치하기](#install-a-starter-kit)
    - [인증된 사용자 조회하기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한(Throttling)](#login-throttling)
- [수동 인증 처리](#authenticating-users)
    - [사용자 기억하기(Remember Me)](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [Stateless HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃 처리](#logging-out)
    - [다른 기기 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 재확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호하기](#password-confirmation-protecting-routes)
- [사용자 정의 가드 추가하기](#adding-custom-guards)
    - [클로저 기반 요청 가드](#closure-request-guards)
- [사용자 정의 User Provider 추가하기](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션에서는 사용자에게 애플리케이션에 인증하고 "로그인"할 수 있는 방법을 제공합니다. 이러한 기능을 웹 애플리케이션에 구현하는 일은 복잡할 수 있고 잠재적으로 위험할 수도 있습니다. 때문에 라라벨은 인증 기능을 빠르고, 안전하며, 쉽게 구축할 수 있는 도구들을 제공합니다.

라라벨의 인증 시스템은 근본적으로 "가드(guard)"와 "프로바이더(provider)"로 구성됩니다. 가드는 각 요청에서 사용자를 어떻게 인증할지 정의합니다. 예를 들어, 라라벨에는 세션 및 쿠키를 이용하여 상태를 관리하는 `session` 가드가 기본으로 포함되어 있습니다.

프로바이더는 지속적으로 저장된 사용자 정보를 어떻게 가져올지 정의합니다. 라라벨은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 사용한 사용자 조회를 기본 지원합니다. 물론 애플리케이션에 필요한 경우 추가 프로바이더도 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 관련 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 라라벨 인증 서비스의 동작을 조정할 수 있는 다양한 옵션들이 상세한 주석과 함께 포함되어 있습니다.

> [!NOTE]
> 가드(guard)와 프로바이더(provider)는 "역할(role)"이나 "권한(permission)"과 혼동해서는 안 됩니다. 권한을 이용해 사용자 행동을 인가(authorize)하는 방법에 대해서는 [인가(authorization)](/docs/12.x/authorization) 문서를 참고해 주세요.

<a name="starter-kits"></a>
### 스타터 킷

빠르게 시작하고 싶으신가요? 라라벨 공식 [스타터 킷](/docs/12.x/starter-kits)을 새 라라벨 애플리케이션에 설치해보세요. 데이터베이스 마이그레이션을 적용한 후 `/register` 혹은 애플리케이션에 할당된 URL에 브라우저로 접속하면 됩니다. 스타터 킷이 전체 인증 시스템 제작을 모두 알아서 처리해줍니다!

**최종적으로 직접 인증 시스템을 구현할 계획이더라도, [스타터 킷](/docs/12.x/starter-kits)을 먼저 설치해서 실제 라라벨 프로젝트에서 인증 기능 전체를 어떻게 구현할 수 있는지 학습하는 방법도 권장합니다.** 라라벨 스타터 킷에는 인증 컨트롤러, 라우트, 뷰 파일이 모두 포함되어 있으므로, 해당 파일의 코드를 살펴보며 라라벨 인증 기능의 구현 방식을 자세히 공부할 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려 사항

기본적으로 라라벨은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

애플리케이션이 Eloquent를 사용하지 않는 경우, 라라벨의 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 활용하실 수 있습니다. 만약 MongoDB를 사용하는 경우, MongoDB 공식 [라라벨 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고해 주세요.

`App\Models\User` 모델의 데이터베이스 스키마를 설계할 때는 비밀번호 컬럼의 길이가 최소 60자 이상이어야 합니다. 기본적으로, 신규 라라벨 애플리케이션에 포함된 `users` 테이블 마이그레이션 파일에는 이보다 더 긴 컬럼이 이미 생성되어 있습니다.

또한, `users`(혹은 동등 역할의 테이블)에 nullable한 문자열 타입의 `remember_token` 컬럼(100자)이 포함되어 있어야 합니다. 이는 사용자가 "로그인 상태 유지" 옵션을 선택할 때 해당 토큰을 저장하는 데 사용됩니다. 역시 기본 제공되는 `users` 테이블 마이그레이션에는 이 컬럼이 이미 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

라라벨은 인증과 관련해 여러 패키지를 제공합니다. 본격적으로 내용을 살펴보기 전에, 라라벨에서 지원하는 인증 관련 에코시스템 전반을 살피고, 각 패키지의 고유한 목적을 간략하게 소개하겠습니다.

먼저, 인증이 어떻게 동작하는지 생각해봅시다. 웹 브라우저를 사용하는 경우, 사용자는 로그인 폼에 사용자명과 비밀번호를 입력합니다. 만약 이 자격 증명이 올바르면, 애플리케이션은 사용자에 대한 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저에 발급된 쿠키에 세션 아이디가 담기므로, 이후의 요청에서도 해당 사용자를 올바른 세션과 연결할 수 있습니다. 세션 쿠키가 브라우저에 전달되면, 애플리케이션은 세션 아이디를 바탕으로 세션 데이터를 조회하여 인증 정보를 확인하고, 사용자가 "인증됨" 상태임을 인지하게 됩니다.

외부 서비스가 API에 접근하기 위해 인증해야 할 때는, 웹 브라우저가 없으므로 인증 방식으로 쿠키를 주로 사용하지는 않습니다. 대신, 외부 서비스는 매 요청마다 API 토큰을 API로 전송합니다. 애플리케이션은 이 토큰을 유효한 토큰 목록과 대조하여, 해당 API 토큰에 연결된 사용자의 요청임을 "인증"합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### 라라벨의 기본 브라우저 인증 서비스

라라벨에는 `Auth`와 `Session` 파사드를 통해 접근 가능한 인증 및 세션 기능이 내장되어 있습니다. 이 기능들은 웹 브라우저에서 시작되는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 확인하고 인증하는 다양한 메서드를 제공하며, 인증 정보는 자동으로 세션에 저장되고 세션 쿠키가 발급됩니다. 이 서비스 활용 방법은 이 문서에서 자세히 설명합니다.

**애플리케이션 스타터 킷**

여기서 설명하는 대로, 인증 서비스를 직접 조작해서 나만의 인증 계층을 구축할 수 있습니다. 하지만 더 빠르게 시작하고 싶다면, 전체 인증 계층이 잘 설계된 [무료 스타터 킷](/docs/12.x/starter-kits)을 이용하세요.

<a name="laravels-api-authentication-services"></a>
#### 라라벨의 API 인증 서비스

라라벨은 API 토큰 관리와 토큰 인증을 지원하는 두 가지 패키지, [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 라이브러리들과 라라벨의 기본 쿠키 기반 인증 라이브러리는 서로 배타적이지 않습니다. Passport, Sanctum은 주로 API 토큰 인증에 집중하고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션에서 이들 모두를 함께 사용할 수도 있습니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"을 지원하는 OAuth2 인증 제공자입니다. 여러 유형의 토큰을 발급할 수 있으며, API 인증을 위한 강력하고 복잡한 기능을 내장하고 있습니다. 하지만 대부분의 애플리케이션에서는 OAuth2 사양에서 제공하는 복잡한 기능까지는 필요하지 않을 수 있고, 사용자는 물론 개발자들도 SPA 또는 모바일 애플리케이션을 OAuth2 인증 제공자(Passport 등)로 인증하는 과정에서 혼란을 겪는 일이 많았습니다.

**Sanctum**

OAuth2의 복잡함과 개발자 혼란에 대응하기 위해, 웹 브라우저의 첫-party 요청과 토큰 기반 API 요청 모두를 단순화해서 처리할 수 있는 더 쉽고 가벼운 인증 패키지를 만들고자 했습니다. 이 목표는 [Laravel Sanctum](/docs/12.x/sanctum)의 릴리즈로 실현되었습니다. Sanctum은 웹 UI와 API 모두를 제공하는 애플리케이션, 백엔드와 완전히 분리된 SPA(싱글 페이지 애플리케이션) 또는 모바일 클라이언트를 제공하는 경우에 가장 권장되는 인증 패키지입니다.

Sanctum은 웹/ API를 아우르는 하이브리드 인증 패키지로, 애플리케이션의 전체 인증 과정을 관리할 수 있습니다. 이는 Sanctum 기반 애플리케이션이 요청을 수신하면, 우선 세션 쿠키에 인증된 세션이 있는지 확인하는 방식으로 동작하기 때문입니다. 이때 라라벨 기본 인증 서비스를 우선 활용합니다. 세션 쿠키 인증이 아니라면, API 토큰이 요청에 존재하는지 검사하고 있다면 해당 토큰을 사용해 인증합니다. 이 과정에 대한 자세한 설명은 Sanctum의 ["동작 방식"](https://laravel.com/docs/12.x/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 정리 및 스택 선택 가이드

정리하면, 브라우저에서 접근하고 모노리스 형태의 라라벨 애플리케이션을 구축한다면, 라라벨 기본 인증 서비스만으로 충분합니다.

추가로, 외부 파트너가 사용할 API를 제공한다면 [Passport](/docs/12.x/passport)나 [Sanctum](/docs/12.x/sanctum) 중 하나를 골라 API 토큰 인증을 제공해야 합니다. 대개는 Sanctum이 더 단순하고 완전한 솔루션이며, API 인증, SPA 인증, 모바일 인증을 모두 지원하고, "스코프(scope)"나 "능력(ability)"도 제공합니다.

SPA(싱글 페이지 애플리케이션) 프론트엔드를 라라벨 백엔드가 지원하는 구조를 만든다면, [Laravel Sanctum](/docs/12.x/sanctum) 사용을 권장합니다. Sanctum을 사용할 때는 [수동으로 백엔드 인증 라우트 구현](#authenticating-users)을 하거나, 회원가입·비밀번호 재설정·이메일 인증 등 주요 기능을 Routes · Controller로 제공하는 [Laravel Fortify](/docs/12.x/fortify)를 무(Headless) 인증 백엔드 서비스로 활용할 수 있습니다.

Passport는 정말로 OAuth2 사양의 모든 기능이 필요할 때만 선택하면 됩니다.

그리고, 빠르게 시작하고 싶다면, [추천하는 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 이용해 곧바로 라라벨 기본 인증 스택을 사용하는 새 애플리케이션 구축을 시작하세요.

<a name="authentication-quickstart"></a>
## 인증 빠르게 시작하기

> [!WARNING]
> 이 부분에서는 UI scaffold와 함께 빠르게 시작할 수 있도록 도와주는 [라라벨 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 이용해 사용자 인증을 구축하는 방법을 다룹니다. 라라벨 인증 시스템을 직접 연동하고 싶으시다면, [수동 인증 처리](#authenticating-users) 문서를 참고해 주세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치하기

먼저, [라라벨 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 설치해야 합니다. 스타터 킷은 새 라라벨 애플리케이션에서 인증 기능을 손쉽게 통합할 수 있도록 세련되게 디자인된 출발점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회하기

스타터 킷으로 애플리케이션을 생성하고, 사용자가 회원가입 및 인증을 마친 뒤에는 종종 현재 인증된 사용자에 접근해야 할 때가 있습니다. 요청을 처리하는 중에는 `Auth` 파사드의 `user` 메서드를 이용해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기
$user = Auth::user();

// 현재 인증된 사용자의 ID 가져오기
$id = Auth::id();
```

또는, 사용자가 인증된 이후라면 `Illuminate\Http\Request` 인스턴스 역시 인증된 사용자에 접근하는 방법으로 활용할 수 있습니다. 타입 힌트된 클래스는 컨트롤러 메서드에 자동 주입되므로, `Illuminate\Http\Request` 객체를 타입 힌트해서 컨트롤러 메서드 어디서든 요청의 `user` 메서드를 통해 인증된 사용자에 쉽게 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보를 수정합니다.
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

들어오는 HTTP 요청의 사용자가 인증되었는지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증된 경우 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있습니다.
}
```

> [!NOTE]
> `check` 메서드로 사용자가 인증되었는지 직접 확인할 수도 있지만, 일반적으로는 해당 사용자가 특정 라우트나 컨트롤러에 접근하기 전에 인증을 확인하는 미들웨어를 사용하는 것이 더 권장되는 방식입니다. 자세한 내용은 [라우트 보호하기](/docs/12.x/authentication#protecting-routes) 문서를 참고해 주세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/12.x/middleware)를 사용해서 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. 라라벨에는 이미 `auth`라는 미들웨어가 포함되어 있는데, 이는 `Illuminate\Auth\Middleware\Authenticate` 클래스를 가리키는 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)입니다. 라라벨에서 이미 내부적으로 별칭이 지정되어 있으므로, 라우트 정의에 미들웨어만 붙이면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리디렉션

`auth` 미들웨어에서 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [네임드 라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectGuestsTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저를 사용할 수도 있습니다
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리디렉션

`guest` 미들웨어에서 인증된 사용자를 감지하면, 해당 사용자를 `dashboard` 또는 `home` 네임드 라우트로 리디렉션합니다. 이 동작 역시 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectUsersTo` 메서드로 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저를 사용할 수도 있습니다
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

라우트에 `auth` 미들웨어를 붙일 때, 사용할 "가드"를 지정할 수도 있습니다. 사용하는 가드명은 `auth.php` 설정 파일의 `guards` 배열에 등록된 키 중 하나여야 합니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한(Throttling)

[애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 사용하는 경우, 로그인 시도는 자동으로 속도 제한이 적용됩니다. 기본적으로 여러 번 로그인에 실패하면 1분간 로그인이 제한되며, 이 제한은 사용자의 사용자명/이메일과 IP 주소 기준으로 별도 관리됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에도 속도 제한을 적용하고 싶다면, [속도 제한(Rate Limiting) 문서](/docs/12.x/routing#rate-limiting)를 참고해 주세요.

<a name="authenticating-users"></a>
## 수동 인증 처리

라라벨의 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)에 포함된 인증 scaffold를 반드시 사용해야 하는 것은 아닙니다. 직접 scaffold를 사용하지 않겠다면, 라라벨 인증 클래스를 직접 이용해 사용자 인증을 처리할 수 있습니다. 걱정하지 마세요, 생각보다 쉽습니다!

우리는 `Auth` [파사드](/docs/12.x/facades)를 사용해서 라라벨의 인증 서비스를 이용할 것이므로, 먼저 클래스 상단에 `Auth` 파사드를 임포트해야 합니다. 그다음, 대표적으로 사용하는 `attempt` 메서드를 살펴봅시다. 이 메서드는 보통 애플리케이션의 "로그인" 폼에서 인증 시도 처리를 담당합니다. 만약 인증에 성공하면, [세션](/docs/12.x/session)을 재생성해서 [세션 고정(Session Fixation) 공격](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

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
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 키/값 쌍의 배열을 첫 번째 인자로 받습니다. 이 배열의 값들은 데이터베이스 테이블에서 사용자를 찾는 데 사용됩니다. 위 예시에서는, `email` 컬럼의 값을 기준으로 사용자를 찾게 됩니다. 사용자가 존재하면, 데이터베이스에 저장된 해시화된 비밀번호와 전달받은 `password` 값이 자동으로 해시되어 비교됩니다. 요청으로 들어온 `password` 값을 직접 해시해서 전달해서는 안 되며, 프레임워크가 알아서 해시 후 비교합니다. 두 비밀번호가 일치하면 사용자에 대한 인증 세션이 시작됩니다.

라라벨의 인증 서비스는 가드의 "provider" 설정에 따라 데이터베이스에서 사용자를 조회합니다. 기본적으로는 `config/auth.php`의 `provider`에 Eloquent 유저 프로바이더가 지정되어 있고, `App\Models\User` 모델을 통해 사용자를 가져오도록 되어 있습니다. 필요에 따라 이 설정은 애플리케이션 요구에 맞게 변경할 수 있습니다.

`attempt` 메서드는 인증에 성공하면 `true`, 실패하면 `false`를 반환합니다.

라라벨의 redirector에서 제공하는 `intended` 메서드는 인증 미들웨어에 의해 접근이 차단된 직전의 원래 URL로 사용자를 되돌려 보냅니다. 원래 목적지 URI가 없을 때 사용할 예비 주소도 함께 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

필요하다면, 이메일과 비밀번호 외에도 추가적인 쿼리 조건을 배열에 추가해 인증 조건을 세분화할 수 있습니다. 예를 들어, 사용자가 "active(활성)" 마크가 되어 있는지도 함께 확인하려면 다음과 같이 배열에 추가하면 됩니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공
}
```

더 복잡한 쿼리 조건이 필요하다면, 자격 증명 배열에 클로저를 추가로 전달할 수 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받아, 애플리케이션의 필요에 따라 쿼리를 자유롭게 조정할 수 있습니다:

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
> 여기서 사용된 `email`은 필수 옵션이 아니라 예시일 뿐입니다. 데이터베이스 테이블에서 "사용자명"에 해당하는 컬럼명을 실제로 사용해야 합니다.

더 심화된 사용자 검증을 하고 싶을 때는, 두 번째 인수로 클로저를 받는 `attemptWhen` 메서드를 사용할 수 있습니다. 이 클로저는 잠재적인 사용자 인스턴스를 받아서 인증 가능한 상태라면 `true`, 아니라면 `false`를 반환해야 합니다:

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
#### 특정 Guard 인스턴스 지정해서 사용하기

`Auth` 파사드의 `guard` 메서드를 사용하면, 인증에 사용할 가드 인스턴스를 직접 지정할 수 있습니다. 덕분에 애플리케이션의 영역별로 완전히 서로 다른 인증 모델/사용자 테이블을 활용해 인증을 세밀하게 나눌 수 있습니다.

`guard` 메서드에 전달되는 가드명은 반드시 `auth.php` 설정 파일에 등록된 가드 중 하나여야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기(Remember Me)

많은 웹 애플리케이션에서는 로그인 폼에 "로그인 유지" 체크박스를 제공합니다. 애플리케이션에서 해당 기능을 지원하고 싶다면, `attempt` 메서드의 두 번째 인자로 불리언 값을 전달하면 됩니다.

이 값이 `true`이면 라라벨은 사용자가 수동으로 로그아웃할 때까지 또는 별도로 지정할 때까지 인증 상태를 지속합니다. 이를 위해 `users` 테이블에 반드시 문자열 타입의 `remember_token` 컬럼이 있어야 하며, 새 라라벨 애플리케이션에서 제공되는 마이그레이션에도 기본으로 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 "로그인 유지" 기능을 선택했습니다.
}
```

로그인 유지 기능이 있는 경우, 현재 인증된 사용자가 "로그인 유지" 쿠키로 인증된 것인지 확인하려면 `viaRemember` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 직접 인증하기

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 직접 설정하고 싶다면, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하면 됩니다. 이때 전달하는 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 합니다. 라라벨의 기본 `App\Models\User` 모델은 이 인터페이스를 이미 구현하고 있습니다. 이 방법은 회원가입 직후 등, 이미 유효한 사용자 인스턴스를 가지고 있을 때 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인수로 불리언 값을 전달할 수도 있습니다. 이 값이 true이면 인증 세션에서 "로그인 유지" 기능이 활성화됩니다. 즉, 사용자가 수동으로 로그아웃하기 전까지 인증 상태가 유지됩니다:

```php
Auth::login($user, $remember = true);
```

필요하다면, `login` 호출 전에 사용할 인증 가드를 지정할 수도 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증하기

데이터베이스의 기본키를 통해 사용자를 인증하고 싶다면, `loginUsingId` 메서드를 활용하세요. 인증하려는 사용자의 기본 키를 전달하면 됩니다:

```php
Auth::loginUsingId(1);
```

이 메서드에도 `remember` 인수로 불리언 값을 넘길 수 있습니다. true이면 "로그인 유지" 인증 세션이 적용됩니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 단일 요청에서만 사용자 인증하기

`once` 메서드를 사용하면, 세션이나 쿠키를 전혀 사용하지 않고 한 번의 요청에만 한정하여 사용자를 인증할 수 있습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 설정 없이도 애플리케이션 사용자를 빠르게 인증하는 방법입니다. 시작하려면, `auth.basic` [미들웨어](/docs/12.x/middleware)를 라우트에 붙여주세요. `auth.basic` 미들웨어는 라라벨 프레임워크에 내장되어 있으므로 별도 정의할 필요가 없습니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근 가능
})->middleware('auth.basic');
```

이 미들웨어를 라우트에 등록하면, 해당 라우트에 접근할 때 브라우저에서 자동으로 인증 정보를 입력하라는 창이 나타납니다. 기본 설정에서는 `users` 데이터베이스 테이블의 `email` 컬럼을 "사용자명"으로 가정합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 주의 사항

PHP FastCGI와 Apache로 라라벨 애플리케이션을 운영할 경우, HTTP Basic 인증이 제대로 동작하지 않을 수 있습니다. 이런 문제를 해결하려면, 애플리케이션의 `.htaccess` 파일에 아래 내용을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP Basic 인증

세션에 사용자 식별자 쿠키를 남기지 않고도 HTTP Basic 인증을 사용할 수 있습니다. 이 방식은 주로 API 요청 인증에 HTTP 인증을 쓸 때 유용합니다. 이를 위해서는, [미들웨어를 직접 정의](/docs/12.x/middleware)하여 `onceBasic` 메서드를 호출하면 됩니다. 만약 `onceBasic` 메서드에서 응답이 반환되지 않으면, 요청은 다음 단계로 계속 전달됩니다:

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

이제, 해당 미들웨어를 라우트에 붙이면 됩니다:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근 가능
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 처리

사용자를 수동으로 로그아웃 처리하려면, `Auth` 파사드에서 제공하는 `logout` 메서드를 사용하세요. 이 메서드는 사용자의 세션에서 인증 정보를 제거하므로, 이후 요청부터는 인증되지 않은 상태가 됩니다.

`logout` 메서드 호출 외에도, 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/12.x/csrf)을 재생성할 것을 권장합니다. 로그아웃 후에는 일반적으로 애플리케이션의 루트 페이지 등으로 사용자를 리디렉션합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 사용자를 애플리케이션에서 로그아웃합니다.
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
### 다른 기기에서의 세션 무효화

라라벨은 사용자가 현재 사용 중인 기기 외에 다른 기기에서 로그인된 세션만을 무효화(즉, 해당 기기에서 "로그아웃" 처리)하는 기능을 제공합니다. 이 기능은 주로 사용자가 비밀번호를 변경하거나 갱신하는 과정에서, 다른 기기의 인증 세션은 모두 종료시키고 현재 기기만 인증 상태를 그대로 유지하도록 하고 싶을 때 활용됩니다.

시작 전, 반드시 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증이 필요한 라우트에 포함되어 있는지 확인하세요. 일반적으로 이 미들웨어는 라우트 그룹에 붙여 애플리케이션의 대부분 라우트에 적용하는 것이 좋습니다. `AuthenticateSession` 미들웨어는 별칭 `auth.session` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 라우트에 붙일 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

이후, `Auth` 파사드에서 제공하는 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 현재 비밀번호를 확인해야 하므로, 애플리케이션에서는 폼을 통해 비밀번호 입력을 받아야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 메서드가 호출되면, 사용자의 모든 다른 세션이 완전히 무효화되어, 이전에 여러 가드로 인증이 되어 있었던 모든 다른 환경에서 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 재확인

애플리케이션을 개발하다 보면, 특정 작업을 실행하기 전에 사용자에게 비밀번호를 다시 한 번 확인 받아야 하거나 민감한 영역으로 이동하기 전에 인증을 다시 요구하고 싶은 경우가 있습니다. 라라벨에는 이를 아주 쉽게 구현할 수 있는 내장 미들웨어가 있습니다. 이 기능을 사용하려면, 사용자의 비밀번호 재확인 요청을 보여주는 라우트와 비밀번호가 올바른지 검사한 후 사용자를 원래 위치로 보내는 라우트 두 가지가 필요합니다.

> [!NOTE]
> 아래의 문서는 라라벨의 비밀번호 재확인 기능을 직접 연동하는 방법에 대해 설명합니다. 더 빠른 적용을 원하신다면 [라라벨 애플리케이션 스타터 킷](/docs/12.x/starter-kits)에서도 해당 기능이 이미 지원되고 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호 확인 이후에는, 기본적으로 3시간 동안 해당 사용자는 다시 비밀번호를 확인하지 않아도 됩니다. 하지만, 이 시간을 조정하고 싶다면 `config/auth.php` 설정 파일의 `password_timeout` 값을 변경하면 됩니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

우선, 비밀번호 재확인을 요청하는 뷰를 보여주는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

예상하듯이, 이 뷰에는 `password` 필드를 가진 폼이 있어야 하며, 사용자에게 현재 애플리케이션의 보호된 영역에 진입하려면 비밀번호 재입력이 필요함을 알리는 안내문도 쉽게 넣을 수 있습니다.

<a name="confirming-the-password"></a>

#### 비밀번호 확인

다음으로, "비밀번호 확인" 뷰에서 폼 요청을 처리할 라우트를 정의해보겠습니다. 이 라우트는 비밀번호를 검증하고, 사용자를 원래 의도한 경로로 리디렉션해주는 역할을 합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

다음 단계로 넘어가기 전에, 이 라우트가 어떻게 동작하는지 좀 더 자세히 살펴보겠습니다. 먼저 요청에서 전달된 `password` 필드는 현재 인증된 사용자의 비밀번호와 실제로 일치하는지 확인합니다. 비밀번호가 올바르다면, Laravel의 세션에 사용자가 비밀번호를 확인했다는 사실을 알려야 합니다. `passwordConfirmed` 메서드는 사용자의 세션에 비밀번호 확인 시점을 타임스탬프로 저장하여, Laravel이 사용자가 마지막으로 비밀번호를 확인한 시점을 알 수 있게 해줍니다. 마지막으로, 사용자를 원래 이동하려던 경로로 리디렉션할 수 있습니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호하기

비밀번호를 최근에 다시 확인해야 하는 액션이 있는 라우트에는 반드시 `password.confirm` 미들웨어를 할당해야 합니다. 이 미들웨어는 라라벨에 기본적으로 포함되어 있으며, 사용자가 비밀번호를 확인한 뒤 다시 원래 위치로 돌아갈 수 있도록 세션에 사용자의 의도한 경로를 자동으로 저장합니다. 의도한 경로를 세션에 저장한 뒤, 미들웨어는 사용자를 `password.confirm` [이름이 지정된 라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다.

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가하기

`Auth` 파사드의 `extend` 메서드를 사용하여 직접 인증 가드(guard)를 정의할 수 있습니다. `extend` 메서드 호출은 [서비스 프로바이더](/docs/12.x/providers) 안에 위치하는 것이 좋습니다. 이미 라라벨에 `AppServiceProvider`가 포함되어 있으므로, 여기에 코드를 추가할 수 있습니다.

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
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시에서처럼, `extend` 메서드에 전달된 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 인터페이스의 구현체를 반환해야 합니다. 이 인터페이스에는 커스텀 가드를 정의할 때 구현해야 할 몇 가지 메서드가 있습니다. 커스텀 가드를 정의했다면, `auth.php` 설정 파일의 `guards` 설정에서 해당 가드를 참조할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 기반 요청 가드

가장 간단하게 커스텀 HTTP 요청 기반 인증 시스템을 구현하는 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드를 활용하면, 하나의 클로저만으로 인증 과정을 빠르게 정의할 수 있습니다.

먼저, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 `Auth::viaRequest`를 호출합니다. `viaRequest` 메서드의 첫 번째 인자는 인증 드라이버의 이름이며, 여러분의 커스텀 가드를 설명하는 아무 문자열이나 가능합니다. 두 번째 인자로 전달되는 클로저는 들어오는 HTTP 요청을 받아, 인증된 User 인스턴스(인증 실패 시에는 `null`)를 반환해야 합니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

커스텀 인증 드라이버를 정의했다면, 이제 `auth.php` 설정 파일의 `guards` 설정에서 드라이버로 설정할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로, 해당 가드를 인증 미들웨어에 지정하여 라우트에 적용할 수 있습니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가하기

만약 사용자 정보를 기존 관계형 데이터베이스가 아닌 다른 저장소에 저장하고 있다면, 라라벨에 직접 사용자 인증 프로바이더를 확장해서 사용할 수 있습니다. 이를 위해 `Auth` 파사드의 `provider` 메서드를 사용하여 커스텀 사용자 프로바이더를 정의합니다. 사용자 프로바이더 리졸버는 `Illuminate\Contracts\Auth\UserProvider` 인터페이스의 구현체를 반환해야 합니다.

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
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider` 메서드를 이용해 프로바이더를 등록했다면, `auth.php` 설정 파일에서 새로 만든 사용자 프로바이더로 변경해줄 수 있습니다. 먼저, `providers` 설정에 새 드라이버를 사용하도록 추가합니다.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그리고 이 프로바이더를 `guards` 설정에서 참조하도록 지정합니다.

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### 사용자 프로바이더(User Provider) 계약

`Illuminate\Contracts\Auth\UserProvider` 구현체는 일반적으로 MySQL, MongoDB 등과 같이 지속적으로 저장되는 시스템에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스 덕분에 사용자 정보 저장 방식과 관계없이 라라벨 인증 시스템의 동작을 보장할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약을 한 번 살펴보겠습니다.

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

`retrieveById` 함수는 일반적으로 MySQL의 자동 증가 ID처럼 사용자를 대표하는 값을 받아서, 해당 ID를 가진 `Authenticatable` 인스턴스를 찾아 반환합니다.

`retrieveByToken` 함수는 고유한 `$identifier`와 "remember me" `$token`을 이용해 사용자를 조회합니다. 이 `$token` 값은 보통 데이터베이스의 `remember_token` 컬럼에 저장되며, 해당 값이 일치하는 `Authenticatable` 인스턴스를 반환해야 합니다.

`updateRememberToken` 메서드는 주어진 `$user` 인스턴스의 `remember_token`을 새로운 `$token`으로 업데이트합니다. 사용자가 "remember me" 인증을 성공하거나 로그아웃할 때 새로운 토큰을 할당합니다.

`retrieveByCredentials` 메서드는 애플리케이션에서 `Auth::attempt`를 통해 전달받은 자격 증명(credential) 배열을 매개변수로 받습니다. 이 메서드는 해당 자격 증명 값에 맞는 사용자를 저장소에서 조회해야 합니다. 보통 "where" 조건을 사용해 예를 들어 `$credentials['username']` 값과 일치하는 사용자 레코드를 찾으며, 그 결과로 `Authenticatable` 구현체를 반환해야 합니다. **이 메서드에서 비밀번호의 검증 또는 인증 과정은 절대 수행하면 안 됩니다.**

`validateCredentials` 메서드는 주어진 `$user`와 `$credentials`를 비교하여 인증 과정을 처리해야 합니다. 일반적으로 이 메서드는 `Hash::check`를 이용하여, `$user->getAuthPassword()`와 `$credentials['password']` 값을 비교합니다. 이 메서드는 비밀번호가 유효한지 여부에 따라 `true` 또는 `false`를 반환해야 합니다.

`rehashPasswordIfRequired` 메서드는 필요하다면(그리고 지원된다면) 주어진 `$user`의 비밀번호를 재해시(rehash)합니다. 예를 들어, 이 메서드는 보통 `Hash::needsRehash`를 이용해 `$credentials['password']` 값이 재해시가 필요한지 검사하고, 필요하다면 `Hash::make`로 비밀번호를 재해시하여 저장소에 업데이트해줍니다.

<a name="the-authenticatable-contract"></a>
### 실제로 인증되는 Authenticatable 계약

이제 `UserProvider`의 각 메서드를 살펴봤으니, `Authenticatable` 계약 인터페이스도 확인해보겠습니다. 사용자 프로바이더에서는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 반드시 이 인터페이스의 구현체를 반환해야 합니다.

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

이 인터페이스는 아주 단순합니다. `getAuthIdentifierName` 메서드는 기본키(primary key) 컬럼의 이름을 반환하고, `getAuthIdentifier`는 사용자의 실제 기본키 값을 반환합니다. MySQL을 사용할 경우, 대개 사용자의 자동 증가 기본키 값이 됩니다. `getAuthPasswordName`은 사용자의 비밀번호 컬럼 이름을, `getAuthPassword`는 해시화된 사용자의 비밀번호 값을 반환합니다.

이 인터페이스 덕분에, 인증 시스템이 어떤 ORM이나 저장소 추상화 계층을 사용하더라도 모든 "user" 클래스로 동작할 수 있습니다. 기본적으로, 라라벨은 `app/Models` 디렉터리에 이 인터페이스를 구현한 `App\Models\User` 클래스를 포함하고 있습니다.

<a name="automatic-password-rehashing"></a>
## 비밀번호 자동 재해시(자동 재해싱)

라라벨에서 기본적으로 사용하는 비밀번호 해시 알고리즘은 bcrypt입니다. bcrypt 해시의 "work factor"(작업 강도)는 애플리케이션의 `config/hashing.php` 설정 파일이나 `BCRYPT_ROUNDS` 환경 변수로 조절할 수 있습니다.

일반적으로, 컴퓨터(CPU/GPU) 성능이 향상됨에 따라 bcrypt의 작업 강도를 점진적으로 증가시키는 것이 좋습니다. 만약 애플리케이션의 bcrypt 작업 강도를 높였다면, 라라벨은 starter kit 또는 [수동 인증](#authenticating-users) 과정에서 사용자 인증이 이루어질 때, 비밀번호를 점진적이고 자동으로 재해시 처리해줍니다.

보통 비밀번호 자동 재해싱 기능은 애플리케이션에 별다른 문제를 일으키지 않지만, 필요하다면 설정 파일을 퍼블리시(publish)하여 이 동작을 비활성화할 수 있습니다.

```shell
php artisan config:publish hashing
```

설정 파일을 퍼블리시한 후에는 `rehash_on_login` 설정 값을 `false`로 변경하면 자동 재해싱이 비활성화됩니다.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트

라라벨은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 이벤트들에 대해 [리스너를 정의](/docs/12.x/events)하여 원하는 동작을 추가할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                     |
| ----------------------------------------------- |
| `Illuminate\Auth\Events\Registered`             |
| `Illuminate\Auth\Events\Attempting`             |
| `Illuminate\Auth\Events\Authenticated`          |
| `Illuminate\Auth\Events\Login`                  |
| `Illuminate\Auth\Events\Failed`                 |
| `Illuminate\Auth\Events\Validated`              |
| `Illuminate\Auth\Events\Verified`               |
| `Illuminate\Auth\Events\Logout`                 |
| `Illuminate\Auth\Events\CurrentDeviceLogout`    |
| `Illuminate\Auth\Events\OtherDeviceLogout`      |
| `Illuminate\Auth\Events\Lockout`                |
| `Illuminate\Auth\Events\PasswordReset`          |

</div>