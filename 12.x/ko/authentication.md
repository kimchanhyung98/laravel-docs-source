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
    - [다른 기기 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 재확인](#password-confirmation)
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

많은 웹 애플리케이션은 사용자가 해당 애플리케이션에서 인증(로그인)할 수 있는 방법을 제공합니다. 이 기능을 웹 애플리케이션에 구현하는 것은 복잡하고 잠재적으로 위험할 수 있습니다. 이러한 이유로, Laravel은 인증을 빠르고, 안전하게, 그리고 쉽게 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 기능은 기본적으로 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각 요청에서 사용자를 어떻게 인증할지 결정합니다. 예를 들어, Laravel에는 세션 저장소와 쿠키를 이용해 상태를 유지하는 `session` 가드가 기본적으로 내장되어 있습니다.

프로바이더는 사용자를 영속적 저장소(주로 데이터베이스)에서 어떻게 불러올지 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 사용하여 사용자를 불러오는 데 기본적으로 지원합니다. 필요하다면 애플리케이션에 맞게 추가 프로바이더를 직접 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel의 인증 서비스를 세밀하게 조정할 수 있는 다양한 설정 옵션이 잘 문서화되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(roles)" 및 "권한(permissions)"과는 다릅니다. 권한을 통한 사용자 행동 인가(authorization)에 대해 더 알고 싶다면 [인가(authorization)](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트 (Starter Kits)

빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션을 마친 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 URL로 이동하면 됩니다. 스타터 키트가 전체 인증 시스템의 기본 구조를 자동으로 만들어 드립니다!

**최종적으로 스타터 키트 없이 직접 구현하더라도, [스타터 키트](/docs/12.x/starter-kits)를 설치해 보는 것은 Laravel의 모든 인증 기능을 실제 프로젝트에서 어떻게 구현할 수 있는지 배우는 좋은 기회가 됩니다.** Laravel 스타터 키트는 인증 컨트롤러, 라우트, 뷰를 포함하고 있으므로, 해당 파일의 코드를 분석하여 Laravel 인증 기능이 어떻게 동작하는지 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우, MongoDB의 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델의 데이터베이스 스키마를 설계할 때, password 컬럼의 길이가 최소 60자 이상이어야 합니다. 기본적으로 새로운 Laravel 애플리케이션의 `users` 테이블 마이그레이션에는 이 조건을 만족하는 컬럼이 포함되어 있습니다.

또한, `users`(또는 이에 준하는) 테이블에 100자 길이의 `remember_token` 컬럼(널 허용, 문자열)이 반드시 존재하는지 확인해야 합니다. 이 컬럼은 사용자가 "로그인 상태 유지" 옵션을 선택할 때 토큰을 저장하는 데 사용됩니다. 역시, 기본 `users` 테이블 마이그레이션에 이 컬럼이 기본 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 본격적으로 시작하기 전에, Laravel의 인증 에코시스템 전반을 살펴보고 각 패키지의 목적을 소개합니다.

먼저 인증이 어떻게 동작하는지 이해해봅시다. 웹 브라우저를 통해 사용자가 로그인 폼에서 아이디와 비밀번호를 입력하면, 자격 증명이 올바르면 해당 사용자의 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 포함되어, 이후 요청에서 사용자와 올바른 세션을 연동할 수 있습니다. 세션 쿠키를 받은 후, 애플리케이션은 세션 ID로 세션 데이터를 불러오고, 인증 정보가 세션에 저장되어 있음을 확인해 그 사용자를 "인증됨"으로 간주합니다.

반면, 외부 서비스가 API에 접근하기 위해 인증해야 하는 경우에는, 웹 브라우저가 없으므로 쿠키 대신 API 토큰을 요청마다 함께 전송합니다. 애플리케이션은 전달받은 토큰이 유효한지 데이터베이스 등에서 확인하고, 해당 토큰과 연결된 사용자로 요청을 "인증"합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel은 기본적으로 인증 및 세션 서비스를 제공합니다. 일반적으로 `Auth`와 `Session` 파사드를 통해 사용할 수 있습니다. 이 기능들은 웹 브라우저 기반의 요청에 대해 쿠키를 이용한 인증을 제공합니다. 사용자의 자격 증명을 확인하거나, 사용자를 인증하는 등의 메서드가 포함되어 있습니다. 추가적으로, 이 서비스는 적절한 인증 데이터를 세션에 저장하고 세션 쿠키를 발급하는 작업도 자동으로 처리합니다. 이러한 서비스 사용 방법은 본 문서에서 자세히 설명합니다.

**애플리케이션 스타터 키트**

인증 서비스를 직접 사용하여 인증 레이어를 직접 구현할 수도 있지만, 보다 빠른 시작을 위해 전체 인증 레이어를 강력하게 구성해주는 [무료 스타터 키트](/docs/12.x/starter-kits)를 제공하고 있습니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리를 돕는 두 가지 옵션 패키지 [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 라이브러리들은 Laravel의 내장 쿠키 기반 인증 라이브러리와 배타적이지 않으며, 주로 API 토큰 기반 인증에 초점을 둡니다. 반면 내장 인증 서비스는 브라우저의 쿠키 기반 인증에 중점을 둡니다. 많은 애플리케이션에서는 이 둘 모두를 동시에 활용합니다.

**Passport**

Passport는 OAuth2 인증 프로바이더로, 다양한 OAuth2 그랜트 타입을 지원하여 여러 유형의 토큰 발급이 가능합니다. 매우 탄탄하고 복잡한 API 인증 패키지이지만, 대부분의 애플리케이션은 그 정도의 복잡성이 필요하지 않습니다. 또한, SPA나 모바일 애플리케이션에서의 OAuth2 활용 및 인증 방법에서 혼란을 느끼는 개발자도 많았습니다.

**Sanctum**

OAuth2의 복잡성과 개발자 혼란에 대응하여, 더 단순하고 직관적이면서도 웹 브라우저 및 API 요청 모두를 토큰으로 처리할 수 있는 인증 패키지를 만들게 되었고, 이것이 [Laravel Sanctum](/docs/12.x/sanctum)입니다. 이 패키지는 API뿐 아니라 브라우저 기반 1st-party 웹 UI, 또는 백엔드와 분리된 SPA, 모바일 클라이언트 등을 아우르며 추천되는 인증 솔루션입니다.

Laravel Sanctum은 웹/ API 인증을 동시에 관리할 수 있는 하이브리드 패키지입니다. Sanctum 기반 애플리케이션은 우선, 요청이 인증된 세션 쿠키를 포함하는지 확인하여 내장 인증 서비스를 먼저 호출합니다. 세션 쿠키가 없을 경우 API 토큰이 포함되어 있으면, 해당 토큰을 사용하여 인증합니다. 자세한 내용은 Sanctum의 ["작동 방식(how it works)"](/docs/12.x/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 정리 및 스택 선택

정리하면, 애플리케이션이 브라우저를 통해 접근되고 모노리식 Laravel 애플리케이션이라면, 내장 인증 서비스만으로 충분합니다.

API를 외부에 제공한다면, [Passport](/docs/12.x/passport) 또는 [Sanctum](/docs/12.x/sanctum) 중 하나로 API 토큰 인증을 설정해야 합니다. 대부분의 경우, Sanctum이 보다 단순하고, API 인증, SPA 인증, 모바일 인증을 모두 지원하며, "스코프" 또는 "능력" 관리도 제공하므로 권장됩니다.

SPA를 Laravel 백엔드가 처리한다면 [Laravel Sanctum](/docs/12.x/sanctum)을 사용해야 합니다. 이 때 [backend 인증 라우트를 직접 구현](#authenticating-users)하거나, [Laravel Fortify](/docs/12.x/fortify)를 "헤드리스 인증 백엔드 서비스"로 사용해서 회원가입, 비밀번호 재설정, 이메일 인증 등을 위한 라우트와 컨트롤러를 활용할 수 있습니다.

OAuth2 명세의 모든 기능이 반드시 필요한 경우에만 Passport 사용을 검토하세요.

빠르게 시작하고 싶으시면, 이미 권장 스택이 반영되어 있는 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하시는 것이 좋습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 부분에서는 UI가 포함된 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)로 인증 기능을 사용하는 방법을 설명합니다. Laravel의 인증 시스템과 직접 연동하려면, [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 스타터 키트는 새로운 Laravel 애플리케이션에 인증 기능을 고급스럽게 디자인된 형태로 바로 적용할 수 있습니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 키트로 애플리케이션을 만들고 사용자가 회원가입 및 인증을 완료했다면, 종종 현재 인증된 사용자와 상호작용할 필요가 있습니다. 들어오는 요청을 처리할 때, `Auth` 파사드의 `user` 메서드를 사용하여 인증된 사용자를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자를 가져옴...
$user = Auth::user();

// 현재 인증된 사용자의 ID를 가져옴...
$id = Auth::id();
```

또는, 사용자가 인증된 이후라면 `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자에 접근할 수 있습니다. 컨트롤러 메서드에 타입힌팅된 클래스를 주입하면 요청의 `user` 메서드를 통해 쉽게 인증 사용자를 얻을 수 있습니다:

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

<a name="determining-if-the-current-user-is-authenticated"></a>
#### 현재 사용자의 인증 여부 판정

들어오는 HTTP 요청의 사용자가 인증되어 있는지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 인증된 사용자인 경우 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있습니다...
}
```

> [!NOTE]
> 사용자가 인증되었는지 `check` 메서드로 확인할 수도 있지만, 보통은 특정 라우트/컨트롤러에 접근하기 전 인증 여부를 미들웨어로 확인하는 것이 일반적입니다. 이에 대한 자세한 내용은 [라우트 보호하기](/docs/12.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/12.x/middleware)를 사용하면 인증된 사용자만 특정 라우트에 접근할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스의 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)인 `auth` 미들웨어를 기본 제공하므로, 라우트 정의에 미들웨어만 붙이면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어는 인증되지 않은 사용자가 접근할 경우, 사용자를 `login` [이름이 지정된 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 애플리케이션의 `bootstrap/app.php`에서 `redirectGuestsTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // 클로저를 사용하는 경우...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리다이렉트

`guest` 미들웨어는 이미 인증된 사용자가 접근할 경우, 해당 사용자를 `dashboard` 또는 `home` 이름의 라우트로 리다이렉트합니다. 이 동작 역시 `bootstrap/app.php`에서 `redirectUsersTo` 메서드로 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // 클로저를 사용하는 경우...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정

`auth` 미들웨어를 라우트에 적용할 때, 어떤 "가드"를 사용할지 지정할 수 있습니다. 지정하는 가드는 `auth.php` 설정 파일의 `guards` 배열에 정의된 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우, 로그인 시도에 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본적으로 여러 번 잘못된 자격 증명을 제공하면 1분 동안 로그인이 차단됩니다. 이 제한은 사용자의 아이디/이메일과 IP 주소별로 개별 적용됩니다.

> [!NOTE]
> 애플리케이션 내 다른 라우트에 속도 제한을 적용하고 싶다면 [속도 제한 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

Laravel의 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)가 제공하는 인증 구조를 꼭 사용해야 하는 것은 아닙니다. 직접 인증 로직을 구현하려면 Laravel 인증 클래스를 직접 사용할 수 있습니다. 걱정하지 마세요, 아주 간단합니다!

`Auth` [파사드](/docs/12.x/facades)를 통해 인증 서비스를 사용할 것이므로, 우선 클래스 상단에 `Auth` 파사드를 임포트하세요. 이제, `attempt` 메서드를 살펴봅니다. 이 메서드는 일반적으로 애플리케이션의 "로그인" 폼에서 인증 요청을 처리할 때 사용됩니다. 인증이 성공하면, [세션](/docs/12.x/session) [고정 공격(session fixation)](https://en.wikipedia.org/wiki/Session_fixation)을 방지하기 위해 사용자의 세션을 재생성해야 합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * 인증 시도를 처리합니다.
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

`attempt` 메서드는 첫 번째 인수로 키/값 쌍의 배열을 받습니다. 배열의 값들은 데이터베이스에서 사용자를 찾는 데 사용됩니다. 위 예시에서 사용자는 `email` 컬럼 값으로 조회됩니다. 사용자가 검색되면, 데이터베이스에 저장된 해시된 패스워드와 폼에서 입력된 `password` 값을 비교합니다. 이때, 들어오는 `password` 값은 해싱하지 않아도 되며, 프레임워크가 자동으로 해싱 후 비교합니다. 두 해시된 패스워드가 일치하면, 인증된 세션이 시작됩니다.

Laravel의 인증 서비스는 가드의 "프로바이더" 설정에 따라 사용자를 데이터베이스에서 조회합니다. 기본 `config/auth.php`에서는 Eloquent 사용자 프로바이더가 지정되어 있고, `App\Models\User` 모델을 사용합니다. 애플리케이션 요구에 따라 이 값을 변경할 수 있습니다.

`attempt` 메서드는 인증에 성공하면 `true`, 실패하면 `false`를 반환합니다.

Laravel의 리다이렉터가 제공하는 `intended` 메서드는 인증 미들웨어로 인해 우회되기 전 사용자가 원했던 URL로 리디렉션 해줍니다. 만약 해당 목적지 URL이 없다면 대체 URI를 지정할 수도 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

원한다면, 이메일과 패스워드 외에도 추가적인 쿼리 조건을 인증에 포함할 수 있습니다. 조건을 추가하려면 `attempt` 메서드에 전달하는 배열에 쿼리 조건을 추가하면 됩니다. 예를 들어, 사용자가 "active" 상태이어야 한다는 조건을 체크할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

더 복잡한 쿼리 조건이 필요하다면, 자격 증명 배열에 클로저를 사용할 수 있습니다. 이 클로저는 쿼리 인스턴스를 받아, 애플리케이션의 필요에 따라 쿼리를 커스터마이즈할 수 있습니다:

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
> 위 예제에서 `email`은 예시일 뿐, 필수 컬럼이 아닙니다. 실제로는 데이터베이스의 "username" 역할을 하는 컬럼명을 사용해야 합니다.

`attemptWhen` 메서드는 두 번째 인수로 클로저를 받아, 사용자를 실제로 인증하기 전에 좀 더 정교한 검사도 수행할 수 있게 합니다. 이 클로저는 잠재적인 사용자 인스턴스를 받아, 인증이 가능한지 `true` 또는 `false`를 반환해야 합니다:

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

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 사용

`Auth` 파사드의 `guard` 메서드를 이용하면, 사용자 인증에 어떤 가드 인스턴스를 사용할지 지정할 수 있습니다. 이로써 서로 다른 인증 모델이나 사용자 테이블을 사용하는 앱 부분을 독립적으로 관리할 수 있습니다.

`guard` 메서드에 전달하는 가드명은 반드시 `auth.php` 설정 파일의 `guards`에 정의되어 있어야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션에서 로그인 폼에 "로그인 상태 유지(remember me)" 체크박스를 제공합니다. 애플리케이션에 해당 기능을 추가하고 싶다면, `attempt` 메서드의 두 번째 인수에 불리언 값을 전달하면 됩니다.

이 값이 `true`면 사용자는 로그아웃하기 전까지(또는 영구적으로) 인증 상태가 유지됩니다. 이때, `users` 테이블에 `remember_token` 문자열 컬럼이 반드시 있어야 합니다. 이 컬럼은 "로그인 상태 유지" 토큰을 저장하는 데 사용됩니다. 기본 `users` 테이블 마이그레이션에 이미 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 '로그인 상태 유지' 중입니다...
}
```

"로그인 상태 유지" 기능을 제공한다면, 현재 사용자가 해당 쿠키로 인증되었는지 `viaRemember` 메서드로 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 지정해야 하는 경우, `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 전달하면 됩니다. 제공된 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 하며, 기본 `App\Models\User` 모델은 이미 해당 인터페이스를 구현하고 있습니다. 이 방식은 회원가입 직후 이미 유효한 사용자 인스턴스가 있을 때 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인수로 불리언 값을 줄 수 있습니다. 이 값이 참이면 인증된 세션을 영구 유지("로그인 상태 유지")할 수 있으며, 사용자가 직접 로그아웃할 때까지 인증이 유지됩니다:

```php
Auth::login($user, $remember = true);
```

필요하다면, `login` 메서드 호출 전에 인증할 가드를 지정할 수 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증하기

데이터베이스 레코드의 기본 키(primary key)로 사용자를 인증하려면, `loginUsingId` 메서드를 사용하면 됩니다. 인증할 사용자의 기본 키를 메서드에 전달하세요:

```php
Auth::loginUsingId(1);
```

`loginUsingId` 메서드의 `remember` 인수에 불리언 값을 전달할 수 있습니다. 이 값이 참이면, 세션이 사용자가 직접 로그아웃할 때까지 유지됩니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 인증하기

`once` 메서드를 사용하면 세션이나 쿠키를 사용하지 않고, 단 한 번의 요청 동안만 사용자를 인증할 수 있습니다. 이 메서드를 호출하면 `Login` 이벤트도 발생하지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증 (HTTP Basic Authentication)

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 로그인 페이지 없이 사용자 인증을 할 수 있는 빠른 방법입니다. 사용하려면, `auth.basic` [미들웨어](/docs/12.x/middleware)를 라우트에 지정하세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 기본 내장되어 있으므로 별도 정의 없이 바로 사용할 수 있습니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth.basic');
```

미들웨어를 라우트에 적용하면, 브라우저로 해당 라우트에 접속 시 자격 증명을 입력하라는 프롬프트가 자동으로 표시됩니다. 기본적으로, `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 사용자의 "username"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 환경에서의 참고사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache를 함께 사용해 Laravel을 배포한 경우, HTTP Basic 인증이 정상 동작하지 않을 수 있습니다. 이 문제는 아래와 같이 `.htaccess` 파일에 줄을 추가해 해결할 수 있습니다:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 무상태 HTTP Basic 인증

세션에 사용자 식별 쿠키를 저장하지 않고도 HTTP Basic 인증을 사용할 수 있습니다. 이 방법은 API 인증 등에 주로 유용합니다. 이를 위해, [미들웨어를 정의](/docs/12.x/middleware)하고 `onceBasic` 메서드를 호출합니다. 만약 `onceBasic`에서 응답이 반환되지 않으면, 요청이 다음 단계로 진행됩니다:

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

정의한 미들웨어를 라우트에 적용하세요:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 수동으로 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 사용자의 세션에서 인증 정보를 제거하여 이후 요청에서 인증 정보를 사용하지 않도록 합니다.

`logout`을 호출한 후에는 세션을 무효화하고 [CSRF 토큰](/docs/12.x/csrf)을 재생성하는 것이 권장됩니다. 로그아웃 후 일반적으로 애플리케이션 루트로 리다이렉트합니다:

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
### 다른 기기 세션 무효화

Laravel은 현재 사용 중인 기기를 제외한 다른 기기에서 로그인된 세션을 무효화(로그아웃) 하는 기능도 제공합니다. 이 기능은 보통 사용자가 비밀번호를 변경하거나 업데이트할 때, 현재 기기의 인증은 유지하되 다른 기기의 세션을 무효화하고 싶을 때 유용합니다.

먼저, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 해당 라우트에 적용되어 있는지 확인해야 합니다. 일반적으로 라우트 그룹에 해당 미들웨어(`auth.session`)를 지정해 대다수 라우트에 쉽게 적용할 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

이제, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 현재 비밀번호를 입력하여 확인해야 하며, 이 값을 입력 폼에서 받아 처리해야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 호출되면, 사용자의 다른 세션이 모두 무효화되어 해당 기기에서 자동으로 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 재확인 (Password Confirmation)

애플리케이션을 개발하다 보면, 특정 동작을 하기 전 또는 민감한 영역에 접근하기 전 사용자의 비밀번호를 다시 확인해야 하는 경우가 있을 수 있습니다. Laravel은 이런 작업을 쉽게 처리할 수 있는 내장 미들웨어를 제공합니다. 이 기능을 구현하려면, 비밀번호 재확인을 요청하는 뷰로 이동하는 라우트와 비밀번호를 검증하고 사용자를 intended(의도한) 위치로 리다이렉트하는 라우트, 두 개가 필요합니다.

> [!NOTE]
> 아래 문서는 Laravel 비밀번호 재확인 기능을 직접 연동하는 방법을 다룹니다. 더 빠르고 쉽게 시작하려면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)에서 이미 이 기능을 지원하고 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호 재확인 후, 3시간(기본값) 동안 다시 비밀번호를 확인하지 않아도 됩니다. 이 시간은 애플리케이션의 `config/auth.php` 설정 파일에 있는 `password_timeout` 값을 변경하여 설정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 재확인 폼

먼저, 사용자의 비밀번호 재입력을 요청하는 뷰를 반환하는 라우트를 만듭니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트에서 반환하는 뷰는 반드시 `password` 필드가 포함된 폼을 가져야 합니다. 또한, 사용자가 민감한 영역에 진입하는 중임을 설명하는 안내문구 등도 추가할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, 위 "비밀번호 확인" 뷰에서 폼 제출 시 POST 요청을 처리하는 라우트를 만듭니다. 이 라우트는 비밀번호를 검증하고, 사용자를 의도한 위치로 리다이렉트하는 역할을 합니다:

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

이 라우트에서는 먼저 요청에 담긴 `password` 값이 인증된 사용자의 비밀번호와 실제로 일치하는지 확인합니다. 패스워드가 유효하다면, 세션에 비밀번호 확인이 이루어졌음을 Laravel에 알리기 위해 `passwordConfirmed` 메서드를 호출합니다. 해당 메서드는 사용자가 마지막으로 비밀번호를 확인한 시점을 세션에 저장합니다. 마지막으로, 사용자를 의도된 목적지로 리다이렉트할 수 있습니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

비밀번호 재확인이 필요한 모든 라우트에 반드시 `password.confirm` 미들웨어를 적용해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며 사용자의 의도한 위치(URL)를 세션에 저장해, 확인 후 해당 위치로 자동 이동하도록 지원합니다. 미들웨어는 사용자를 `password.confirm` [이름이 지정된 라우트](/docs/12.x/routing#named-routes)로 자동 리다이렉트합니다:

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

`Auth` 파사드의 `extend` 메서드를 사용하여 커스텀 인증 가드를 직접 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/12.x/providers) 내에 위치해야 하며, 일반적으로 Laravel의 기본 제공 `AppServiceProvider`에 추가합니다:

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
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Illuminate\Contracts\Auth\Guard의 인스턴스를 반환해야 합니다...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시처럼, `extend`에 넘기는 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 인터페이스의 구현체를 반환해야 합니다. 이 인터페이스에는 커스텀 가드를 정의하기 위한 몇 가지 메서드가 포함되어 있습니다. 커스텀 가드를 정의한 후에는, `auth.php` 설정 파일의 `guards` 설정에 해당 가드를 등록할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 요청 가드 (Closure Request Guards)

HTTP 요청 기반의 간단한 커스텀 인증 시스템을 구현하려면, `Auth::viaRequest` 메서드를 사용하세요. 이 메서드는 하나의 클로저로 인증 프로세스를 쉽게 정의할 수 있습니다.

`viaRequest` 메서드는 인증 드라이버 이름(임의의 문자열)과, 인증 실패 시 `null` 또는 인증된 사용자 인스턴스를 반환하는 클로저(HTTP 요청 인스턴스를 인수로 받음)를 매개로 받습니다. 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 아래처럼 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

이제 커스텀 인증 드라이버를 정의했으므로, `auth.php`의 `guards` 설정에서 해당 드라이버를 지정할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로, 인증 미들웨어를 라우트에 지정할 때 해당 가드를 참조하면 됩니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가 (Adding Custom User Providers)

기존의 관계형 데이터베이스가 아닌 곳에 사용자 정보를 저장한다면, 직접 사용자 프로바이더를 구현해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 사용자 프로바이더를 등록하세요. 이 리졸버는 반드시 `Illuminate\Contracts\Auth\UserProvider`의 구현체를 반환해야 합니다:

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
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider의 인스턴스를 반환해야 합니다...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider`를 통해 프로바이더를 등록했다면, `auth.php`의 `providers`에서 새 드라이버를 사용하도록 설정하세요:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

이제 해당 프로바이더를 `guards` 설정에서 참조할 수 있습니다:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는, `Illuminate\Contracts\Auth\Authenticatable` 구현체(즉, 인증 사용자 인스턴스)를 MySQL, MongoDB 등 영속적 저장소에서 불러오는 역할을 합니다. 이 두 인터페이스 덕분에, 사용자 데이터 저장 방식이나 ORM에 상관없이 인증 메커니즘이 동일하게 작동할 수 있습니다.

아래는 `Illuminate\Contracts\Auth\UserProvider` 계약 전체 예시입니다:

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

- `retrieveById`는 예를 들어 MySQL의 자동증가 ID 등, 사용자를 식별하는 키를 받아 해당 ID와 일치하는 사용자를 반환합니다.
- `retrieveByToken`은 고유 `$identifier`(예: PK)와 "로그인 상태 유지" `$token`(`remember_token` 컬럼 등)을 기반으로 사용자를 조회합니다.
- `updateRememberToken`은 주어진 사용자의 `remember_token`을 새 `$token`으로 갱신합니다. 이 토큰은 "로그인 상태 유지" 인증이나 로그아웃 시 새로 지정됩니다.
- `retrieveByCredentials`는 인증 시도시 `Auth::attempt`에 전달된 자격 증명 배열을 받아, 해당 조건을 만족하는 사용자를 검색합니다. 예를 들어, `$credentials['username']`과 일치하는 사용자 레코드 조회 등. **이 메서드는 비밀번호 인증/검증을 하지 않습니다.**
- `validateCredentials`는 주어진 `$user` 객체와 `$credentials`의 비밀번호를 비교하여 유효성을 판정해야 합니다. 보통 `Hash::check`로 `$user->getAuthPassword()`와 `$credentials['password']`를 비교합니다. 결과로 `true` 또는 `false`를 반환합니다.
- `rehashPasswordIfRequired`는, 필요하다면(기술적으로 지원된다면) 사용자의 비밀번호를 자동 재해싱해야 할 때 실행됩니다. 보통 `Hash::needsRehash`로 재해싱 여부를 확인하고, 필요하면 `Hash::make`로 재해싱 후 저장합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

이제 `UserProvider`의 각 메서드를 살펴봤으니, `Authenticatable` 계약을 살펴봅시다. 프로바이더는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`에서 반드시 이 인터페이스 구현체를 반환해야 합니다:

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

- `getAuthIdentifierName`은 사용자의 "기본 키" 컬럼명을 반환합니다.
- `getAuthIdentifier`는 사용자 레코드의 "기본 키" 값(예: MySQL PK값)을 반환합니다.
- `getAuthPasswordName`은 비밀번호 컬럼명을 반환합니다.
- `getAuthPassword`는 사용자의 해시된 비밀번호를 반환합니다.

이 인터페이스 덕분에, 어떤 ORM이나 저장소 타입이든 "사용자" 클래스를 인증 시스템과 연동할 수 있습니다. Laravel은 `app/Models`에 `App\Models\User` 클래스를 기본 제공하며, 이 클래스가 해당 인터페이스를 이미 구현하고 있습니다.

<a name="automatic-password-rehashing"></a>
## 비밀번호 자동 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt의 "work factor"는 애플리케이션의 `config/hashing.php`나 환경 변수 `BCRYPT_ROUNDS`에서 조정할 수 있습니다.

암호화 파워가 증가하는 만큼 bcrypt work factor도 점차 높아져야 하며, 이 값을 올리면 Laravel은 스타터 키트 혹은 [사용자 수동 인증](#authenticating-users) 시 `attempt` 메서드를 통해 인증하는 과정에서 사용자 비밀번호를 자동으로 재해싱합니다.

이 자동 재해싱 기능은 일반적으로 애플리케이션에 지장을 주지 않습니다. 다만, 이 기능을 비활성화하려면 `hashing` 설정 파일을 퍼블리싱하세요:

```shell
php artisan config:publish hashing
```

설정 파일이 퍼블리싱 되었다면, `rehash_on_login` 값을 `false`로 지정할 수 있습니다:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정 중 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 다음 이벤트 중 원하는 이벤트에 [리스너를 정의](/docs/12.x/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                     |
| -------------------------------------------- |
| `Illuminate\Auth\Events\Registered`          |
| `Illuminate\Auth\Events\Attempting`          |
| `Illuminate\Auth\Events\Authenticated`       |
| `Illuminate\Auth\Events\Login`               |
| `Illuminate\Auth\Events\Failed`              |
| `Illuminate\Auth\Events\Validated`           |
| `Illuminate\Auth\Events\Verified`            |
| `Illuminate\Auth\Events\Logout`              |
| `Illuminate\Auth\Events\CurrentDeviceLogout` |
| `Illuminate\Auth\Events\OtherDeviceLogout`   |
| `Illuminate\Auth\Events\Lockout`             |
| `Illuminate\Auth\Events\PasswordReset`       |

</div>
