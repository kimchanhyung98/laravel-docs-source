# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [무상태 HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [비밀번호 자동 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증(로그인)할 수 있는 방법을 제공합니다. 이러한 기능을 웹 애플리케이션에서 구현하는 것은 복잡하고 잠재적으로 위험한 작업이 될 수 있습니다. 이런 이유로, Laravel은 인증 기능을 빠르고, 안전하게, 그리고 쉽게 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 시스템은 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각 요청마다 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel에는 세션 저장소와 쿠키를 사용하는 `session` 가드가 기본으로 탑재되어 있습니다.

프로바이더(provider)는 사용자를 영구 저장소에서 어떻게 조회할지를 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 통해 사용자를 조회할 수 있도록 지원합니다. 물론 필요하다면 애플리케이션에 맞게 추가로 프로바이더를 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel의 인증 서비스 동작을 세밀하게 조정할 수 있는 다양한 옵션이 잘 설명되어 있습니다.

> [!NOTE]
> 가드(guard)와 프로바이더(provider)는 "역할(role)"과 "권한(permission)" 개념과 혼동해서는 안 됩니다. 사용자 권한 인가 기능에 대해 자세히 알아보고 싶다면 [인가(authorization)](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션을 실행한 후 브라우저에서 `/register` 또는 애플리케이션에 할당된 URL 중 하나로 접속하면, 스타터 키트가 전체 인증 시스템의 스캐폴딩을 자동으로 제공해줍니다.

**만약 최종 애플리케이션에 스타터 키트를 사용하지 않을 계획이라 하더라도, 한 번쯤 [스타터 키트](/docs/12.x/starter-kits)를 설치하고 내부 동작을 살펴보면, 실제 프로젝트에서 Laravel의 인증 기능이 어떻게 구현되는지 이해하는 데 큰 도움이 됩니다.** 스타터 키트 내부 파일에는 인증 컨트롤러, 라우트, 뷰가 모두 포함되어 있으므로, 직접 해당 코드를 참고하여 인증 시스템 구현법을 배울 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

만약 애플리케이션에서 Eloquent를 사용하지 않는다면, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. 만약 MongoDB를 사용한다면, MongoDB 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 생성할 때는 비밀번호 컬럼의 길이가 최소 60자 이상인지 확인해야 합니다. 새 Laravel 애플리케이션에 기본 포함된 `users` 테이블 마이그레이션은 이미 이 요구사항을 충족합니다.

또한 `users`(또는 그에 상응하는) 테이블에는 널 허용, 길이 100자의 문자열 타입인 `remember_token` 컬럼이 존재하는지 확인해야 합니다. 이 컬럼은 로그인 시 "로그인 상태 유지(remember me)" 옵션을 선택한 사용자의 토큰을 저장하는 데 사용됩니다. 마찬가지로, 새 Laravel 애플리케이션의 기본 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증과 관련된 다양한 패키지를 제공합니다. 본격적으로 시작하기 전에, Laravel의 인증 에코시스템을 전체적으로 살펴보고 각 패키지가 의도한 목적에 대해 간단히 알아보겠습니다.

먼저, 전통적인 인증 방식에 대해 생각해보겠습니다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼을 통해 사용자명과 비밀번호를 입력합니다. 입력한 자격 증명이 올바르면, 애플리케이션은 인증된 사용자 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저로 발급된 쿠키에는 세션 ID가 포함되어 있어서, 이후 요청 시 사용자를 올바른 세션과 연결할 수 있습니다. 세션 쿠키가 서버로 전달되면, 서버에서는 세션 ID로 세션 데이터를 조회하여 인증 정보를 확인하고 사용자를 "인증됨" 상태로 간주합니다.

원격 서비스가 API에 접근하기 위해 인증이 필요할 때는, 브라우저가 없으므로 쿠키 대신 API 토큰을 전송하는 방식을 사용합니다. 애플리케이션은 전달된 토큰을 유효한 API 토큰 테이블과 비교해, 해당 토큰에 연관된 사용자가 수행한 요청임을 "인증"하게 됩니다.

#### Laravel의 내장 브라우저 인증 서비스

Laravel은 기본적으로 내장 인증과 세션 서비스를 제공하며, 일반적으로 `Auth` 및 `Session` 파사드를 통해 접근합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 검증하고 인증하는 메서드들을 지원하며, 인증 데이터는 자동으로 세션에 저장되고 해당 세션 쿠키가 발급됩니다. 이 문서에서는 이러한 서비스 사용법을 자세히 설명합니다.

**애플리케이션 스타터 키트**

이 문서에서 설명하는 대로 인증 서비스를 직접 활용하여 자체 인증 레이어를 구축할 수도 있습니다. 하지만 빠르게 시작할 수 있도록, 전체 인증 레이어를 견고하고 현대적인 방식으로 스캐폴딩하는 [무료 스타터 키트](/docs/12.x/starter-kits)를 제공합니다.

#### Laravel의 API 인증 서비스

API 토큰을 관리하고 인증하는 데 도움을 주는 [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)라는 두 개의 선택적 패키지가 있습니다. 이 패키지들과 쿠키 기반 인증 서비스는 상호배타적이지 않으며, 이 패키지들은 API 토큰 인증에 초점을 두고, 내장 인증 서비스는 브라우저 인증에 초점을 둡니다. 다수의 애플리케이션이 내장 인증 서비스와 API 인증 패키지 둘 다를 사용할 수 있습니다.

**Passport**

Passport는 OAuth2 인증 제공자로, 다양한 OAuth2 "grant type"을 지원하며 여러 종류의 토큰을 발급할 수 있습니다. 일반적으로 Passport는 API 인증을 위한 강력하고 복잡한 패키지입니다. 그러나 대부분의 애플리케이션은 OAuth2 명세에서 제공하는 복잡한 기능까지 필요하지 않으며, 이런 복잡성은 사용자와 개발자 모두에게 혼란을 줄 수 있습니다. 특히, SPA나 모바일 앱에서 Passport와 같은 OAuth2 인증 제공자를 어떻게 활용해야 하는지에 대해 혼란이 많았습니다.

**Sanctum**

OAuth2의 복잡성 및 개발자의 혼란을 해소하기 위해, 우리는 웹 브라우저에서의 1차 요청과 토큰 기반 API 요청을 모두 다루는 더 간단하고 직관적인 인증 패키지를 만들었습니다. 그 결과가 바로 [Laravel Sanctum](/docs/12.x/sanctum)입니다. Sanctum은 API와 1차 웹 UI, 또는 백엔드 Laravel 애플리케이션과 분리된 SPA, 또는 모바일 클라이언트를 지원하려는 경우 권장되는 인증 패키지입니다.

Laravel Sanctum은 웹/ API 하이브리드 인증 패키지로, 애플리케이션의 전체 인증 프로세스를 관리할 수 있습니다. Sanctum 기반 애플리케이션이 요청을 수신할 때, 먼저 세션 쿠키가 인증된 세션을 참조하는지 확인합니다. 이는 앞서 설명한 Laravel의 내장 인증 서비스를 활용하여 이루어집니다. 세션 쿠키로 인증되지 않은 요청의 경우, API 토큰이 있는지 검사하고, 메시지 내에 토큰이 있으면 해당 토큰으로 인증합니다. 이 프로세스에 대해 자세히 알고 싶다면 Sanctum의 ["작동 방식"](/docs/12.x/sanctum#how-it-works) 문서를 참고하세요.

#### 요약 및 스택 선택

요약하면, 브라우저에서 접근하는 단일(모놀리식) Laravel 애플리케이션을 개발 중이라면 내장 인증 서비스를 사용하게 됩니다.

그리고, 외부에서 소비하는 API를 제공한다면 [Passport](/docs/12.x/passport) 또는 [Sanctum](/docs/12.x/sanctum) 중에서 선택하여 API 토큰 인증 기능을 추가할 수 있습니다. 일반적으로 Sanctum이 더 단순하고, API 인증, SPA 인증, 모바일 인증(스코프, 능력(abillity) 포함)을 완료하게 해주므로 추천됩니다.

Laravel 백엔드에서 구동되는 SPA를 구축한다면 [Laravel Sanctum](/docs/12.x/sanctum) 사용이 권장됩니다. 이 경우, [인증 라우트 직접 구현](#authenticating-users) 또는 [Laravel Fortify](/docs/12.x/fortify)를 사용하는 두 가지 방식 중 하나를 선택하면 됩니다. Fortify는 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 기능에 대한 라우트와 컨트롤러를 제공합니다.

OAuth2 명세의 모든 기능이 꼭 필요하다면 Passport를 선택할 수 있습니다.

그리고, 빠르게 시작하고 싶다면 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하여 이미 권장 인증 스택이 포함된 새로운 Laravel 애플리케이션을 바로 시작하실 수 있습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 문서의 이 부분은 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하여 사용자를 인증하는 방법을 설명합니다. UI 스캐폴딩이 포함되어 있어 빠르게 시작할 수 있습니다. 만약 인증 시스템과 직접 통합하고 싶으면 [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

우선, [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 스타터 키트는 새 Laravel 애플리케이션에 인증 기능을 쉽고 아름답게 통합할 수 있는 출발점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 키트로 애플리케이션을 만들고 사용자가 회원가입 및 인증할 수 있게 되면, 현재 인증된 사용자와 상호작용할 일이 많아집니다. 들어오는 요청을 처리하면서, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회...
$user = Auth::user();

// 현재 인증된 사용자의 ID 조회...
$id = Auth::id();
```

또는, 사용자가 인증된 이후에는 `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자에 접근할 수 있습니다. 컨트롤러 메서드에서 타입힌트로 `Illuminate\Http\Request` 객체를 주입하면, `user` 메서드를 통해 언제든 인증된 사용자에 편리하게 접근할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보를 업데이트합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

#### 현재 사용자가 인증되었는지 확인하기

들어오는 HTTP 요청의 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하세요. 이 메서드는 사용자가 인증된 경우 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인 상태입니다...
}
```

> [!NOTE]
> `check` 메서드로 사용자가 인증되었는지 알 수 있지만, 일반적으로는 미들웨어를 사용해 특정 라우트/컨트롤러에 접근 전 인증 여부를 검증합니다. 이에 대한 자세한 내용은 [라우트 보호](/docs/12.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/12.x/middleware)를 사용하면 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 위한 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)인 `auth` 미들웨어가 기본 제공됩니다. 별칭이 이미 내부적으로 지정되어 있으므로, 라우트 정의에 미들웨어만 붙이면 됩니다.

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth');
```

#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일 내 `redirectGuestsTo` 메서드를 사용해 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저 사용 예시...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

#### 인증된 사용자 리다이렉트

`guest` 미들웨어가 인증된 사용자를 감지하면, `dashboard` 또는 `home` 네임드 라우트로 리다이렉트합니다. 이 동작을 `redirectUsersTo` 메서드를 통해 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저 사용 예시...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

#### 가드 지정하기

`auth` 미들웨어를 라우트에 붙일 때, 사용자 인증에 사용할 "가드(guard)"를 별도로 지정할 수도 있습니다. 지정하는 가드의 이름은 `auth.php` 설정 파일의 `guards` 배열 중 하나와 일치해야 합니다.

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용 중이라면, 로그인 시도에 자동으로 속도 제한이 적용됩니다. 기본적으로 일정 횟수 이상 자격 증명이 올바르지 않으면 1분 동안 로그인할 수 없습니다. 이 제한은 사용자의 사용자명/이메일 및 IP 주소별로 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에 속도 제한을 적용하려면 [속도 제한 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)가 제공하는 인증 스캐폴딩을 반드시 사용할 필요는 없습니다. 만약 이 스캐폴딩을 사용하지 않는다면, Laravel의 인증 클래스를 직접 활용해 사용자 인증을 관리해야 합니다. 걱정 마세요, 어렵지 않습니다!

인증 서비스에 접근하기 위해 `Auth` [파사드](/docs/12.x/facades)를 사용할 텐데, 먼저 클래스 상단에서 `Auth`를 임포트해야 합니다. 이제 `attempt` 메서드를 살펴보겠습니다. 일반적으로 이 메서드는 애플리케이션의 "로그인" 폼에서 인증 시도 처리를 위해 사용됩니다. 인증에 성공하면, [세션 고정 공격(session fixation)](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%85%98_%EA%B3%A0%EC%A0%95_%EA%B3%B5%EA%B2%A9) 방지를 위해 반드시 사용자의 [세션](/docs/12.x/session)을 재생성해야 합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * 인증 시도 처리.
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

`attempt` 메서드는 첫 번째 인자로 키-값 쌍의 배열을 받습니다. 이 배열의 값이 데이터베이스 테이블에서 사용자를 찾는 데 사용됩니다. 위 예시의 경우, 사용자는 `email` 컬럼 값으로 조회됩니다. 사용자가 존재할 경우, 데이터베이스에 저장된 해시된 비밀번호와 배열로 전달된 `password` 값이 비교됩니다. 이때 요청된 비밀번호를 직접 해싱할 필요는 없습니다. 프레임워크가 자동으로 비밀번호를 해싱하여 데이터베이스 값과 비교합니다. 해시된 비밀번호가 일치하면 인증된 세션이 시작됩니다.

Laravel 인증 서비스는 가드의 프로바이더 설정에 따라 데이터베이스에서 사용자를 조회합니다. 기본 `config/auth.php` 설정 파일에는 Eloquent 사용자 프로바이더가 지정되어 있으며, 사용자를 조회할 때 `App\Models\User` 모델을 사용하도록 지시합니다. 필요에 따라 이 값을 설정 파일에서 변경할 수 있습니다.

인증이 성공적으로 이루어지면 `attempt` 메서드는 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다.

Laravel의 `redirector`에서 제공하는 `intended` 메서드는, 인증 미들웨어에 의해 중단되기 전 사용자가 원래 접근하려 했던 URL로 리다이렉트합니다. 만약 해당 경로가 불가능하다면 대체 URI를 인자로 줄 수 있습니다.

#### 추가 조건 지정하기

필요하다면, 사용자 이메일과 비밀번호 외에 인증 쿼리에 추가 조건을 더할 수 있습니다. 이는 배열에 조건을 추가하는 것만으로 가능합니다. 예를 들어, 사용자의 "활성화" 여부도 확인할 수 있습니다.

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

더 복잡한 조건이 필요하다면, 배열 내에 클로저(Closure)를 추가로 전달할 수도 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받아, 애플리케이션 특성에 맞게 쿼리를 커스터마이징할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // 인증 성공...
}
```

> [!WARNING]
> 위 예시에서 `email`은 필수 컬럼이 아니라 예시로 든 것일 뿐입니다. 데이터베이스에서 "사용자명"에 해당하는 컬럼명을 여러분의 환경에 맞게 사용하세요.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아, 실제 인증 전 후보 사용자를 더 꼼꼼히 검사할 수 있습니다. 클로저는 사용자 인스턴스를 받아, 인증 여부에 따라 `true` 또는 `false`를 반환해야 합니다.

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // 인증 성공...
}
```

#### 특정 가드 인스턴스 접근하기

`Auth` 파사드의 `guard` 메서드를 통해 인증에 사용할 가드 인스턴스를 직접 지정할 수 있습니다. 이를 통해 애플리케이션의 영역마다 완전히 별도의 인증 모델 혹은 사용자 테이블을 활용할 수 있습니다.

`guard`에 넘기는 이름은 `auth.php` 설정 파일에 정의된 가드 중 하나이어야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션에서 로그인 폼에 "로그인 상태 유지(remember me)" 체크박스를 제공합니다. 이 기능을 구현하려면, `attempt` 메서드의 두 번째 인자로 불리언 값을 전달하면 됩니다.

이 값이 `true`이면, 사용자는 로그아웃하지 않는 한 계속 인증 상태가 유지됩니다. `users` 테이블에는 반드시 문자열 타입의 `remember_token` 컬럼이 있어야 하며, "로그인 상태 유지" 토큰을 저장하는 데 사용됩니다. 기본 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억되고 있습니다...
}
```

만약 이 기능을 제공한다면, `viaRemember` 메서드를 이용해 현재 인증된 사용자가 "로그인 상태 유지" 쿠키로 인증된 것인지 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

#### 사용자 인스턴스 직접 인증하기

이미 유효한 사용자 인스턴스가 있다면, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하여 현재 인증된 사용자로 설정할 수 있습니다. 전달하는 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 합니다. Laravel에 포함된 `App\Models\User`는 이미 이 인터페이스를 구현하고 있습니다. 회원가입 직후와 같이 사용자 인스턴스가 이미 존재하는 경우에 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인자로 `remember me` 기능 활성화를 원하면 불리언 값을 넘길 수 있습니다.

```php
Auth::login($user, $remember = true);
```

필요하다면, 로그인 전 인증 가드를 지정할 수도 있습니다.

```php
Auth::guard('admin')->login($user);
```

#### 사용자 ID로 인증하기

데이터베이스 기본 키(주키)를 이용해 사용자를 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증할 사용자의 PK 값을 인자로 받습니다.

```php
Auth::loginUsingId(1);
```

두 번째 인자로 `remember` 값을 넘길 수 있으며, 로그인 상태 유지 여부를 결정합니다.

```php
Auth::loginUsingId(1, remember: true);
```

#### 1회성 인증

`once` 메서드를 사용하면, 세션이나 쿠키를 생성하지 않고 한 번의 요청 동안만 사용자를 인증할 수 있습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증 (HTTP Basic Authentication)

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 없이도 빠르게 사용자를 인증할 수 있는 방법입니다. 시작하려면, 해당 라우트에 `auth.basic` [미들웨어](/docs/12.x/middleware)를 붙이세요. 이 미들웨어는 Laravel에서 기본 제공되므로 별도로 정의할 필요가 없습니다.

```php
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth.basic');
```

라우트에 미들웨어가 적용되면, 해당 라우트에 접속할 때 브라우저에서 자동으로 자격 증명 입력을 요구합니다. 기본적으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 "사용자명"으로 간주합니다.

#### FastCGI 참고사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache로 Laravel 애플리케이션을 서비스할 경우, HTTP Basic 인증이 정상 동작하지 않을 수 있습니다. 이를 해결하려면 `.htaccess` 파일에 아래 내용을 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

### 무상태 HTTP Basic 인증

세션에 사용자 식별자 쿠키를 저장하지 않고 HTTP Basic 인증을 사용할 수도 있습니다. 이 방법은 API 같은 곳에서 HTTP Authentication을 도입할 때 유용합니다. 이를 위해 [미들웨어 정의](/docs/12.x/middleware)를 만들고, `onceBasic` 메서드를 호출하세요. 응답이 반환되지 않으면 요청이 계속 애플리케이션 내부로 전달됩니다.

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
     * 들어오는 요청 처리.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

그리고 미들웨어를 라우트에 등록하세요.

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 애플리케이션에서 수동으로 로그아웃시키려면, `Auth` 파사드가 제공하는 `logout` 메서드를 사용하세요. 이 메서드는 사용자의 세션에서 인증 정보를 제거하므로, 이후 요청은 인증되지 않습니다.

`logout` 메서드 호출 이외에도, 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/12.x/csrf)을 재생성하는 것이 안전합니다. 로그아웃 후에는 일반적으로 애플리케이션의 루트 URL로 리다이렉트합니다.

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
### 다른 기기의 세션 무효화

Laravel은 사용자가 비밀번호를 변경할 때, 현재 사용 중인 기기는 유지하면서 다른 기기에서의 세션을 무효화(강제 로그아웃)하는 기능도 제공합니다.

먼저 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 적용되어야 하며, 일반적으로 라우트 그룹에 미들웨어를 붙여 대부분의 라우트에서 동작하도록 합니다. 기본적으로 이 미들웨어는 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)인 `auth.session`으로 사용할 수 있습니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

이후, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자의 현재 비밀번호 확인을 필요로 하며, 폼에서 해당 입력값을 받아야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 호출되면, 사용자의 다른 기기에서의 모든 세션이 완전히 무효화되어, 모든 인증 가드에 대해 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션 상에서 사용자가 중요한 작업을 진행하거나 민감한 영역에 접근하기 전, 비밀번호 재확인을 요구해야 할 때가 있습니다. Laravel은 이 과정을 쉽게 할 수 있는 내장 미들웨어를 제공합니다. 이를 구현하려면, 사용자에게 비밀번호를 확인하는 뷰를 보여주는 라우트와 비밀번호 유효성 검증 및 원래 위치로 리다이렉트하는 라우트, 두 개를 작성해야 합니다.

> [!NOTE]
> 아래 설명은 Laravel의 비밀번호 확인 기능을 직접 통합하는 방법을 다룹니다. 더 빠르게 시작하고 싶다면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)에 이 기능이 이미 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호 확인 후에는 3시간 동안 다시 비밀번호 확인을 묻지 않습니다. 이 값은 애플리케이션의 `config/auth.php` 설정 파일의 `password_timeout` 항목을 변경하여 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

#### 비밀번호 확인 폼

먼저, 사용자에게 비밀번호 확인을 요구하는 뷰를 반환하는 라우트를 정의합니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 뷰에서는 `password` 필드가 포함된 폼을 작성하면 됩니다. 또한, 민감한 영역 진입을 위해 비밀번호 확인이 필요함을 안내하는 문구를 넣어도 좋습니다.

#### 비밀번호 확인 처리

이제, 해당 폼에서 제출된 요청을 처리할 라우트를 정의합니다. 이 라우트는 비밀번호를 검증하고 사용자를 원래의 목적지로 리다이렉트합니다.

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

위 라우트를 자세히 살펴보면, 먼저 요청에서 받은 `password` 필드가 실제로 인증된 사용자의 비밀번호와 일치하는지 확인합니다. 비밀번호가 유효하면, Laravel 세션에 비밀번호 확인을 완료했다는 타임스탬프를 기록해야 합니다. `passwordConfirmed` 메서드는 세션에 사용자가 마지막으로 비밀번호를 확인한 시점을 기록합니다. 마지막으로 사용자를 원래 있던 위치로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

특정 작업이 비밀번호 재확인을 필요로 한다면 해당 라우트에 `password.confirm` 미들웨어를 반드시 붙이세요. 이 미들웨어는 Laravel에 기본 설치되어 있으며, 사용자가 비밀번호 확인 후 원래 있었던 위치로 리다이렉트할 수 있도록 자동으로 세션에 목적지를 기록합니다. 그 후, `password.confirm` [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다.

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 사용해 직접 인증 가드를 정의할 수 있습니다. 이 코드는 일반적으로 [서비스 프로바이더](/docs/12.x/providers) 내에 위치해야 하며, 이미 제공되는 `AppServiceProvider`에 추가할 수 있습니다.

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
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 인스턴스를 반환해야 합니다...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시에서처럼, `extend`에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard`를 구현한 인스턴스를 반환해야 합니다. 이 인터페이스는 커스텀 가드를 정의하는 데 필요한 여러 메서드를 포함합니다. 커스텀 가드가 준비되면, `auth.php` 설정 파일의 `guards` 항목에서 원하는 이름으로 사용할 수 있습니다.

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

HTTP 요청 기반으로 커스텀 인증 시스템을 가장 쉽고 빠르게 구현하려면 `Auth::viaRequest` 메서드를 이용하세요. 이 메서드는 하나의 클로저로 인증 프로세스를 정의할 수 있습니다.

`AppServiceProvider`의 `boot` 메서드에서 `viaRequest`를 호출합니다. 첫 번째 인자는 인증 드라이버명으로, 어떤 이름이든 상관없으며 커스텀 가드의 이름입니다. 두 번째 인자는 들어온 HTTP 요청을 받아 사용자 인스턴스를 반환하거나, 인증이 실패하면 `null`을 반환하는 클로저입니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

커스텀 인증 드라이버가 정의되었으면, `auth.php` 설정 파일의 `guards` 항목에 등록하여 사용할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

그리고, 미들웨어에 해당 가드를 지정해 라우트에 할당할 수 있습니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가 (Adding Custom User Providers)

전통적인 관계형 데이터베이스가 아닌 곳에 사용자 정보를 저장한다면, Laravel에 맞는 사용자 프로바이더를 직접 확장해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 사용자 프로바이더를 정의할 수 있습니다. 이 함수는 `Illuminate\Contracts\Auth\UserProvider` 인터페이스를 구현한 인스턴스를 반환해야 합니다.

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
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 인스턴스 반환...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider` 메서드로 프로바이더를 등록한 뒤에는, `auth.php` 설정 파일에서 이 드라이버를 이용하는 `provider`를 정의하세요.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로, `guards` 설정에서 이 프로바이더를 참조하면 됩니다.

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### User Provider 계약

`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable`을 구현한 인스턴스를 MySQL, MongoDB 등 영구 저장소에서 조회하는 책임을 집니다. 이 두 인터페이스 덕분에 사용자 데이터 저장 방식이나 인증된 사용자를 대표하는 클래스가 무엇이든, Laravel 인증 메커니즘은 동일하게 동작할 수 있습니다.

아래는 `Illuminate\Contracts\Auth\UserProvider` 계약입니다.

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

`retrieveById` 메서드는 주로 사용자를 대표하는 키, 예를 들어 MySQL의 자동 증가 ID와 같은 값을 받아 해당 사용자를 찾아서 반환합니다.

`retrieveByToken` 메서드는 고유 `$identifier`와 "로그인 상태 유지" `$token`으로 사용자를 조회합니다. 주로 데이터베이스의 `remember_token` 컬럼에 저장된 값을 검사합니다.

`updateRememberToken`은 `$user` 인스턴스의 `remember_token`을 새 `$token` 값으로 업데이트해줍니다. 성공적으로 "로그인 상태 유지" 인증을 하거나 로그아웃 시 새로운 토큰이 할당됩니다.

`retrieveByCredentials`는 인증 시도시 `Auth::attempt`에 전달된 자격 증명 배열을 받아, 영구 저장소에서 해당 사용자를 쿼리합니다. 일반적으로 `$credentials['username']`값과 "where" 조건을 맞춰 찾습니다. **비밀번호 유효성 검증/인증 처리까지 이 메서드에서 하면 안 됩니다.**

`validateCredentials`는 제공된 `$user`와 `$credentials`의 값으로 사용자를 인증합니다. 예를 들어, 일반적으로 `Hash::check`로 `$user->getAuthPassword()`와 `$credentials['password']` 값을 비교합니다. 비밀번호가 유효한 경우 `true`, 아니면 `false`를 반환해야 합니다.

`rehashPasswordIfRequired`는 필요한 경우(지원될 경우) `$user`의 비밀번호를 재해시합니다. 주로 `Hash::needsRehash`로 비밀번호 재해싱 필요 여부를 판별해, 필요시 `Hash::make`로 비밀번호를 다시 해시하고 영구 저장소에 사용자의 레코드를 업데이트합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

UserProvider의 각 메서드들을 살펴보았으니 이제 `Authenticatable` 계약도 함께 확인해보겠습니다. UserProvider의 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드는 이 인터페이스 구현체를 반환하는 것이 원칙입니다.

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

이 인터페이스는 단순합니다. `getAuthIdentifierName`은 사용자의 "기본키" 컬럼명을, `getAuthIdentifier`는 사용자의 "기본키" 값을 반환합니다. MySQL 기준이라면 사용자의 PK 값이 될 것입니다.  `getAuthPasswordName`은 비밀번호 컬럼명을, `getAuthPassword`는 해시된 비밀번호를 반환합니다.

이 인터페이스 덕분에 인증 시스템은 ORM이나 저장소 추상화 계층에 상관없이 "사용자" 클래스를 다룰 수 있습니다. Laravel에는 이미 `app/Models` 디렉터리에 이 인터페이스를 구현한 `App\Models\User` 클래스가 포함되어 있습니다.

<a name="automatic-password-rehashing"></a>
## 비밀번호 자동 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt 해시의 "워크 팩터(작업 인자)"는 `config/hashing.php` 설정 파일이나 `BCRYPT_ROUNDS` 환경변수를 통해 조정할 수 있습니다.

CPU 및 GPU 성능이 향상될수록 bcrypt 워크 팩터를 점진적으로 높여주는 것이 좋습니다. 워크 팩터를 높이면, 사용자가 Laravel의 스타터 키트로 인증하거나 [수동 인증](#authenticating-users) 시 `attempt` 메서드를 사용할 때, 자동으로 비밀번호 재해싱이 이뤄집니다.

자동 비밀번호 재해싱은 일반적으로 애플리케이션에 아무런 영향을 주지 않습니다. 하지만 필요하다면, `hashing` 설정 파일을 퍼블리시(publish)하여 이 동작을 비활성화할 수 있습니다.

```shell
php artisan config:publish hashing
```

설정 파일을 퍼블리시했다면, `rehash_on_login` 설정 값을 `false`로 지정할 수 있습니다.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

인증 과정에서 Laravel은 다양한 [이벤트](/docs/12.x/events)를 디스패치합니다. 아래 이벤트 중 원하는 이벤트에 대해 [리스너를 정의](/docs/12.x/events)할 수 있습니다.

<div class="overflow-auto">

| 이벤트명                                       |
| ---------------------------------------------- |
| `Illuminate\Auth\Events\Registered`            |
| `Illuminate\Auth\Events\Attempting`            |
| `Illuminate\Auth\Events\Authenticated`         |
| `Illuminate\Auth\Events\Login`                 |
| `Illuminate\Auth\Events\Failed`                |
| `Illuminate\Auth\Events\Validated`             |
| `Illuminate\Auth\Events\Verified`              |
| `Illuminate\Auth\Events\Logout`                |
| `Illuminate\Auth\Events\CurrentDeviceLogout`   |
| `Illuminate\Auth\Events\OtherDeviceLogout`     |
| `Illuminate\Auth\Events\Lockout`               |
| `Illuminate\Auth\Events\PasswordReset`         |

</div>
