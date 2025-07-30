# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 킷](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 킷 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증](#http-basic-authentication)
    - [상태 비저장 HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃 처리](#logging-out)
    - [다른 기기 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가하기](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가하기](#adding-custom-user-providers)
    - [사용자 프로바이더 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션이 사용자들이 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 이 기능을 웹 애플리케이션에 구현하는 것은 복잡하고 위험할 수도 있습니다. 이런 이유로 Laravel은 인증을 빠르고, 안전하며, 쉽게 구현하는 데 필요한 도구들을 제공하려 노력합니다.

Laravel 인증 시스템의 핵심은 **가드(guards)** 와 **프로바이더(providers)** 로 나뉩니다. 가드는 각 요청마다 사용자가 어떻게 인증되는지를 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 이용해 상태를 유지하는 `session` 가드를 기본으로 제공합니다.

프로바이더는 사용자 정보를 지속 저장소에서 어떻게 가져올지 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 사용해 사용자를 조회하는 기본 프로바이더를 제공합니다. 그러나 애플리케이션 필요에 따라 추가 프로바이더를 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 구성 파일은 `config/auth.php`에 위치해 있습니다. 이 파일에는 Laravel 인증 서비스를 조정할 수 있는 여러 옵션이 잘 문서화되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(roles)"과 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통한 사용자 작업 인가에 대해 더 알고 싶다면 [인가](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 킷 (Starter Kits)

빠르게 시작하고 싶나요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 설치하세요. 데이터베이스 마이그레이션 완료 후, `/register` 또는 애플리케이션에 할당된 다른 URL로 접속하면 스타터 킷이 여러분의 전체 인증 시스템을 자동으로 구성해 줍니다!

**최종적으로 스타터 킷을 사용하지 않더라도, [스타터 킷](/docs/12.x/starter-kits)을 설치해 실제 Laravel 프로젝트에서 인증 기능을 구현하는 방법을 배우는 좋은 기회가 될 수 있습니다.** 스타터 킷은 인증 컨트롤러, 라우트, 뷰를 포함하고 있으므로, 해당 코드들을 검토하면서 Laravel 인증 기능 구현 방식을 이해할 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

기본적으로 Laravel은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

Eloquent를 사용하지 않는다면 Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용한다면 MongoDB 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델의 데이터베이스 스키마를 설계할 때는 비밀번호 컬럼 길이를 최소 60자로 설정하세요. 물론 새 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이를 초과하는 길이의 컬럼을 생성합니다.

또한, `users` (또는 동일한) 테이블에 널을 허용하는 100자 길이의 문자열 `remember_token` 컬럼이 포함되었는지 확인하세요. 이 컬럼은 사용자가 로그인 시 "기억하기" 옵션을 선택하면 토큰을 저장하는 데 사용됩니다. 이 컬럼도 기본 마이그레이션에 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증 관련된 여러 패키지를 제공합니다. 계속하기 전에 Laravel 인증 에코시스템을 전반적으로 살펴보고 각 패키지가 어떤 용도인지 이야기하겠습니다.

먼저 인증이 어떻게 작동하는지 생각해 봅시다. 웹 브라우저로 로그인 폼에서 사용자명과 비밀번호를 입력하면, 올바르다면 애플리케이션은 인증된 사용자 정보들을 사용자 세션에 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 포함되어 이후 요청이 해당 세션과 연결되도록 합니다. 세션 쿠키 수신 후, 애플리케이션은 세션 ID를 바탕으로 세션 데이터를 가져오고 인증 정보가 세션에 저장되어있음을 확인하여 사용자를 "인증됨"으로 간주합니다.

반면, 원격 서비스가 API에 액세스하기 위해 인증할 때는 일반적인 쿠키 기반 인증이 아니라 API 토큰을 매 요청마다 전송합니다. 애플리케이션은 유효한 API 토큰 목록과 비교하여, 해당 API 토큰에 연동된 사용자를 인증하게 됩니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 내장 브라우저 인증 서비스

Laravel은 일반적으로 `Auth` 및 `Session` 파사드를 통해 접근하는 내장 인증 및 세션 서비스를 포함합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 검증하고 인증하는 메서드를 제공하며, 인증 데이터는 자동으로 세션에 저장되고 세션 쿠키가 발급됩니다. 이러한 서비스의 사용법은 본 문서에서 다룹니다.

**애플리케이션 스타터 킷**

본 문서에서 설명했듯이, 직접 수동으로 이 인증 서비스를 다뤄 인증 계층을 구성할 수도 있지만, 더 빠르게 시작할 수 있도록 전체 인증 계층을 튼튼하게 스캐폴딩해주는 [무료 스타터 킷](/docs/12.x/starter-kits)을 제공하고 있습니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리 및 API 토큰 인증 요청 처리를 도와주는 선택적 패키지 두 가지, [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 두 라이브러리와 Laravel 내장 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 이 라이브러리들은 주로 API 토큰 인증에 중점을 두고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션이 내장 쿠키 기반 인증 서비스와 API 인증 패키지 중 하나를 함께 사용합니다.

**Passport**

OAuth2 인증 제공자로 다양한 OAuth2 "grant types"를 지원해 여러 유형의 토큰을 발급할 수 있습니다. 전반적으로 강력하고 복잡한 API 인증 패키지입니다. 그러므로 대부분 애플리케이션은 OAuth2가 제공하는 복잡한 기능을 필요로 하지 않아 사용과 개발에 혼동이 있을 수 있습니다. 또한 OAuth2 공급자인 Passport를 사용해 SPA나 모바일 애플리케이션 인증을 구현하는 방법에 대해 개발자들이 혼란을 겪어왔습니다.

**Sanctum**

OAuth2의 복잡성과 개발자 혼란에 대응해, 더 단순하고 간소화된 인증 패키지를 목표로 개발된 것이 [Laravel Sanctum](/docs/12.x/sanctum)입니다. Sanctum은 1) 브라우저에서 발생하는 1차 웹 요청과 2) API 요청에 토큰 인증을 모두 다룰 수 있는 하이브리드 웹/API 인증 패키지입니다. Sanctum 기반 애플리케이션은 요청이 오면, 우선 세션 쿠키 참고해 인증된 세션이 있는지 확인합니다. 그 후 세션 쿠키 인증이 아닌 경우 API 토큰을 찾아 이를 사용해 인증합니다. 해당 동작 프로세스는 Sanctum 문서 ["how it works"](/docs/12.x/sanctum#how-it-works)에서 자세히 확인할 수 있습니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

요약하면, 브라우저로 접속하는 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 주로 사용합니다.

서드파티 API 소비자가 사용할 API를 제공한다면, [Passport](/docs/12.x/passport) 또는 [Sanctum](/docs/12.x/sanctum) 중 하나를 선택해 API 토큰 인증을 구현해야 합니다. 일반적으로는 더 단순하고 완전한 솔루션인 Sanctum을 선호합니다. Sanctum은 API 인증, SPA 인증, 모바일 인증을 지원하며 "스코프" 또는 "권한" 기능까지 포함합니다.

SPA를 Laravel 백엔드와 함께 구축한다면, [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 적합합니다. 이 때는 [직접 백엔드 인증 라우트를 구현](#authenticating-users)하거나, 등록, 비밀번호 초기화, 이메일 인증 등을 제공하는 헤드리스 인증 서비스인 [Laravel Fortify](/docs/12.x/fortify)를 이용할 수 있습니다.

OAuth2 명세에 따른 모든 기능이 절대 필요한 경우에만 Passport를 선택하세요.

빠르게 시작하고자 한다면 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 추천합니다. 이미 Laravel 내장 인증 서비스를 우선 스택으로 사용하는 완성된 솔루션입니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 부분은 UI 스캐폴딩을 포함한 [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits) 기반 사용자 인증을 다룹니다. Laravel 인증 시스템을 직접 통합하고 싶다면 [수동 사용자 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치 (Install a Starter Kit)

먼저, [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 설치하세요. 이 스타터 킷은 신선한 Laravel 애플리케이션에 인증을 쉽게 도입할 수 있도록 세련된 시작점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회 (Retrieving the Authenticated User)

스타터 킷으로 애플리케이션을 생성하고 사용자 등록 및 인증이 가능해지면, 종종 현재 인증된 사용자와 상호 작용해야 합니다. 요청 처리 중 `Auth` 파사드의 `user` 메서드를 사용해 현재 인증된 사용자를 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회...
$user = Auth::user();

// 현재 인증된 사용자 ID 조회...
$id = Auth::id();
```

또는 인증 후에는 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 접근할 수 있습니다. 타입힌팅한 클래스가 자동으로 컨트롤러 메서드에 주입되므로, `Illuminate\Http\Request` 객체를 타입힌팅한 후, 컨트롤러 내부 어디에서든 요청 객체의 `user` 메서드로 인증된 사용자에 편리하게 접근할 수 있습니다:

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
#### 현재 사용자가 인증되었는지 확인하기

들어오는 HTTP 요청의 사용자가 인증되어 있는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 사용자가 인증되었다면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자 로그인이 된 상태입니다...
}
```

> [!NOTE]
> `check` 메서드로 인증 여부를 확인할 수 있지만, 일반적으로는 특정 라우트 또는 컨트롤러 접근 전에 사용자가 인증되었는지 확인하는 미들웨어를 사용합니다. 자세한 내용은 [라우트 보호하기](/docs/12.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

[라우트 미들웨어](/docs/12.x/middleware)를 사용하면 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 `auth` 미들웨어를 기본 포함하는데, 이 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 클래스의 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)입니다. 이 미들웨어는 이미 내부적으로 별칭 등록이 되어 있어 단순히 라우트 정의에 붙이기만 하면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 경로에 접근할 수 있습니다...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 비인증 사용자 리다이렉트 처리

`auth` 미들웨어가 비인증 사용자를 감지하면 `login` [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다. 이 동작을 애플리케이션의 `bootstrap/app.php` 파일 내 `redirectGuestsTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저 사용 예...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증 사용자 리다이렉트 처리

`guest` 미들웨어가 인증 사용자임을 감지하면, 사용자에게 `dashboard` 또는 `home` 네임드 라우트로 리다이렉트합니다. 이 동작을 `bootstrap/app.php` 파일 내 `redirectUsersTo` 메서드를 통해 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저 사용 예...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 붙일 때, 어떤 "가드"를 통해 인증할지 지정할 수 있습니다. 지정하는 가드는 `auth.php` 설정 파일 내 `guards` 배열의 키 중 하나여야 합니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

우리 [애플리케이션 스타터 킷](/docs/12.x/starter-kits) 중 하나를 사용할 경우, 로그인 시도에 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본 설정으로 몇 번 실패하면 1분간 로그인할 수 없습니다. 제한은 사용자명/이메일 주소와 IP 주소를 기준으로 개별 적용됩니다.

> [!NOTE]
> 애플리케이션 내 다른 라우트에 속도 제한을 적용하고 싶다면 [속도 제한 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

Laravel [애플리케이션 스타터 킷](/docs/12.x/starter-kits)에 포함된 인증 스캐폴딩을 사용하지 않아도 됩니다. 이 경우 Laravel 인증 클래스를 직접 활용해 사용자 인증을 관리해야 합니다. 걱정 마세요, 어렵지 않습니다!

`Auth` [파사드](/docs/12.x/facades)를 사용해 Laravel 인증 서비스를 이용할 것이므로, 클래스 상단에 `Auth`를 임포트해야 합니다. 우선 `attempt` 메서드를 확인해 봅시다. 이 메서드는 통상 애플리케이션 "로그인" 폼의 인증 시도에 사용됩니다. 인증에 성공하면 [세션](/docs/12.x/session)을 재생성해 [세션 고정 공격](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

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
            'email' => '제공된 자격 증명이 기록과 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드의 첫 번째 인수는 키/값 쌍 배열입니다. 배열 값에 따라 사용자를 데이터베이스에서 찾습니다. 위 예시에서는 `email` 컬럼으로 사용자를 조회합니다. 사용자를 찾으면 데이터베이스에 저장된 해시된 비밀번호와 배열의 `password` 값을 비교합니다. 요청 비밀번호 값은 직접 해싱하면 안 됩니다. 프레임워크가 내부에서 자동 해싱 후 비교해줍니다. 두 해시가 일치하면 인증 세션이 시작됩니다.

Laravel 인증 서비스는 `auth` 가드의 `provider` 구성에 따라 데이터베이스에서 사용자를 조회합니다. 기본 `config/auth.php` 파일은 Eloquent 사용자 프로바이더를 지정하며 `App\Models\User` 모델을 사용해 사용자를 조회합니다. 필요 시 구성 파일에서 이를 변경할 수 있습니다.

`attempt`는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

Laravel 리다이렉트기의 `intended` 메서드는 인증 미들웨어에 의해 차단된 후 유저가 접근하려던 URL로 리다이렉트합니다. 이 URL이 없다면 기본값을 받을 수도 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

원한다면 인증 쿼리에 사용자 이메일과 비밀번호 외에 추가 조건을 넣을 수 있습니다. 배열에 쿼리 조건들을 포함하기만 하면 됩니다. 예를 들어 사용자가 "active" 상태인지 확인할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

복잡한 조건이 있다면 배열 내에 클로저를 포함할 수도 있습니다. 이 클로저는 쿼리 인스턴스를 전달받아 원하는 조건을 자유롭게 넣을 수 있습니다:

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
> 위 예시에서 `email`은 필수 옵션이 아니며 예시일 뿐입니다. 데이터베이스 테이블 내 실제 "사용자명"에 해당하는 컬럼명을 사용해야 합니다.

`attemptWhen` 메서드는 두 번째 인수로 클로저를 받아, 인증 대상 사용자를 보다 정밀히 검증할 수 있습니다. 클로저는 인증 대상 사용자 객체를 받고 `true` 또는 `false`를 반환해 인증 가능 여부를 결정합니다:

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
#### 특정 가드 인스턴스에 접근하기

`Auth` 파사드의 `guard` 메서드로 어느 가드 인스턴스를 사용할지 지정하면서 사용자를 인증할 수 있습니다. 이 방법은 애플리케이션 여러 부분에서 서로 다른 인증 가능 모델이나 사용자 테이블을 사용하는 경우 유용합니다.

`guard`에 넘기는 가드 이름은 `auth.php` 구성 파일에 정의된 가드 중 하나여야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹 애플리케이션이 로그인 폼에 "기억하기(remember me)" 체크박스를 제공합니다. "기억하기" 기능을 구현하려면 `attempt` 메서드 두 번째 인수로 불리언 값을 전달하세요.

`true`일 경우 Laravel은 사용자를 무기한 인증 상태로 유지하거나 사용자가 직접 로그아웃할 때까지 인증을 유지합니다. `users` 테이블에는 `remember_token` 문자열 컬럼이 있어야 하며 새 Laravel 앱에서 기본 마이그레이션에 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억된 상태입니다...
}
```

애플리케이션에 "기억하기" 기능이 있을 경우, 현재 인증된 사용자가 "기억하기" 쿠키로 인증되었는지 `viaRemember` 메서드로 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 직접 인증

이미 유효한 사용자 인스턴스가 있을 경우, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달해 현재 인증 사용자로 설정할 수 있습니다. 전달하는 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 합니다. Laravel 기본 제공 `App\Models\User` 모델은 이미 이 인터페이스를 구현합니다. 이 방식은 예를 들어 사용자가 회원가입 후 바로 인증 상태로 만들 때 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드 두 번째 인수로 불리언 값을 전달해 "기억하기" 기능도 활성화할 수 있습니다:

```php
Auth::login($user, $remember = true);
```

필요하면 `login` 호출 전에 특정 가드를 지정할 수도 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증

사용자 데이터베이스 기본 키로 인증하려면 `loginUsingId` 메서드를 사용하세요. 인증하고자 하는 사용자의 기본 키를 인수로 받습니다:

```php
Auth::loginUsingId(1);
```

이 메서드에도 `remember` 불리언 인수를 줄 수 있습니다. `true`라면 "기억하기"가 적용됩니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 인증

`once` 메서드를 사용하면 한 요청 동안만 인증 상태가 됩니다. 이 경우 세션이나 쿠키는 사용되지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도 로그인 페이지 없이 간단하게 사용자 인증을 수행할 수 있습니다. 시작하려면 라우트에 `auth.basic` [미들웨어](/docs/12.x/middleware)를 붙이세요. `auth.basic`은 Laravel 프레임워크에 포함되어 있어 별도 정의가 필요 없습니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth.basic');
```

미들웨어를 설정하면 브라우저에서 해당 경로 접근 시 자동으로 인증 정보를 요구하는 창이 뜹니다. 기본 설정으로 `auth.basic` 미들웨어가 `users` 테이블의 `email` 컬럼을 사용자명으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고

PHP FastCGI 및 Apache 환경에서 실행 시 HTTP 기본 인증이 정상 작동하지 않을 수 있습니다. 이 경우 `.htaccess` 파일에 다음 줄을 추가해 문제를 해결할 수 있습니다:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 상태 비저장 HTTP 기본 인증 (Stateless HTTP Basic Authentication)

사용자 식별 쿠키 없이도 HTTP 기본 인증을 사용할 수 있습니다. 이는 주로 API용으로 HTTP 인증을 사용할 때 유용합니다. 이를 위해 `onceBasic` 메서드를 호출하는 미들웨어를 정의하세요. 인증 실패 시 응답이 돌아오면 요청은 차단되고, 그렇지 않으면 애플리케이션 다음 단계로 넘어갑니다:

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
     * 들어오는 요청 처리
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

이후 라우트에 미들웨어를 붙입니다:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 처리 (Logging Out)

사용자를 애플리케이션에서 수동 로그아웃할 때는 `Auth` 파사드의 `logout` 메서드를 사용합니다. 이 메서드는 사용자 세션에서 인증 정보를 제거해 이후 요청이 인증되지 않도록 합니다.

`logout` 호출과 함께 세션 무효화와 [CSRF 토큰](/docs/12.x/csrf) 재생성을 수행하는 것이 권장됩니다. 로그아웃 후 보통 애플리케이션 루트로 리다이렉트합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션에서 사용자 로그아웃 처리
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
### 다른 기기 세션 무효화 (Invalidating Sessions on Other Devices)

Laravel은 현재 기기의 세션은 유지하면서도, 다른 기기에서 활성화된 사용자의 세션을 무효화하고 로그아웃 처리하는 기능을 제공합니다. 보통 비밀번호 변경 또는 업데이트 시 활용합니다.

먼저 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어를 세션 인증이 필요한 라우트에 포함시켜야 합니다. 보통 라우트 그룹에 넣어 애플리케이션 대부분 경로에 적용합니다. 기본적으로 `auth.session` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 라우트에 붙일 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 후 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 현재 비밀번호 확인을 필요로 하므로, 비밀번호를 입력받는 폼이 있어야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

이 메서드 호출 시 사용자의 다른 모든 세션이 완전히 무효화되어, 이전에 인증한 모든 가드에서 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 개발하다 보면, 특정 민감한 작업이나 영역에 진입할 때 비밀번호 확인을 추가하고 싶을 수 있습니다. Laravel은 이를 쉽게 구현할 수 있는 미들웨어를 내장하고 있습니다. 비밀번호 확인 기능 구현을 위해서는 크게 두 개의 라우트를 정의해야 합니다. 하나는 비밀번호 확인 뷰를 표시하는 라우트, 다른 하나는 비밀번호 유효성 확인 후 원래 목적지로 리다이렉트하는 라우트입니다.

> [!NOTE]
> 아래 문서 내용은 Laravel 비밀번호 확인 기능과 직접 연동하는 법을 다루지만, 빨리 시작하려면 [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)이 이 기능을 포함하고 있으니 활용하세요!

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

비밀번호를 한 번 확인하면 기본적으로 3시간 동안 다시 확인하지 않습니다. 이 시간은 `config/auth.php` 설정 파일의 `password_timeout` 값을 변경해 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

우선 비밀번호 확인을 요청하는 뷰를 반환하는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트가 반환하는 뷰에는 비밀번호 입력 폼이 있어야 하며, 사용자에게 민감 영역 진입 전 비밀번호 확인이 필요함을 설명하는 문구도 포함하면 좋습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로 "비밀번호 확인" 뷰 폼에서 POST 요청을 처리할 라우트를 정의합니다. 비밀번호 유효성 검사 후 사용자를 원래 이동시키려는 경로로 리다이렉트합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['제공된 비밀번호가 기록과 일치하지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

위 라우트 동작을 좀 더 상세히 보면, 우선 요청의 `password` 필드가 인증된 사용자 비밀번호와 실제로 일치하는지 검사합니다. 유효하다면 Laravel 세션에 비밀번호가 확인된 시점을 알려주는 타임스탬프를 저장합니다. `passwordConfirmed` 메서드가 이를 담당합니다. 마지막으로 원래 가고자 했던 경로로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

최근에 비밀번호 확인이 필요한 작업을 하는 라우트에는 `password.confirm` 미들웨어를 적용해야 합니다. 이 미들웨어는 기본 Laravel 설치에 포함되어 있고, 사용자 의도 목적지 경로를 세션에 자동 저장합니다. 저장 후에는 사용자에게 `password.confirm` [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다:

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가하기 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 사용해 직접 인증 가드를 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/12.x/providers)에 작성하는 것이 바람직합니다. Laravel은 기본적으로 `AppServiceProvider`가 포함되어 있으니 그곳에 넣을 수 있습니다:

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
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 구현체를 반환...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시에서 보듯, `extend` 메서드에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard` 인터페이스 구현체를 반환해야 합니다. 이 인터페이스에는 커스텀 가드 정의를 위해 구현해야 할 몇 가지 메서드가 포함되어 있습니다. 가드를 정의한 후 `auth.php`의 `guards` 설정에 등록해 사용할 수 있습니다:

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

가장 단순한 HTTP 요청 기반 커스텀 인증 시스템 구현 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드를 사용하면 하나의 클로저로 인증 과정을 빠르게 정의할 수 있습니다.

시작하려면 애플리케이션 `AppServiceProvider`의 `boot` 메서드 내에 `Auth::viaRequest` 호출을 넣으세요. 첫 인자는 커스텀 가드가 될 인증 드라이버 이름(문자열)이고, 두 번째 인자는 들어오는 HTTP 요청을 받는 클로저입니다. 클로저는 사용자를 반환하거나 인증 실패 시 `null`을 반환하면 됩니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

커스텀 인증 드라이버를 정의했으면, 이제 `auth.php`의 `guards` 설정 파일에 다음과 같이 드라이버로 등록합니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로 인증 미들웨어를 라우트에 지정할 때 해당 가드를 사용하세요:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가하기 (Adding Custom User Providers)

사용자 데이터를 전통적인 관계형 데이터베이스가 아닌 다른 저장소에 보관한다면, Laravel 인증용 사용자 프로바이더를 커스텀 구현해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 사용자 프로바이더를 등록하세요. 이 리졸버는 `Illuminate\Contracts\Auth\UserProvider` 인터페이스 구현체를 반환해야 합니다:

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
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 구현체 반환...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

프로바이더를 등록한 후, `auth.php` 설정에서 새 드라이버를 쓰는 프로바이더를 정의합니다:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그리고 `guards` 설정에서 이 프로바이더를 사용하도록 참조할 수 있습니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### 사용자 프로바이더 계약 (The User Provider Contract)

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등과 같은 지속 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스를 통해 Laravel 인증 메커니즘은 사용자 데이터 저장 방식과 관계없이 동작합니다.

`Illuminate\Contracts\Auth\UserProvider` 계약은 다음과 같습니다:

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

- `retrieveById`는 일반적으로 사용자 키값(예: MySQL의 자동증가 ID)을 인수로 받고, 해당 키에 매칭되는 `Authenticatable` 구현체(사용자 객체)를 반환해야 합니다.
- `retrieveByToken`는 고유 식별자와 "기억하기" 토큰을 받아서 해당 토큰을 가진 사용자를 반환합니다. 이 토큰은 일반적으로 `remember_token` 컬럼에 저장됩니다.
- `updateRememberToken`는 "$user" 인스턴스의 `remember_token`을 새 토큰 값으로 갱신합니다. 이 토큰은 "기억하기" 인증 성공 또는 로그아웃 시 갱신됩니다.
- `retrieveByCredentials`는 `Auth::attempt` 등에서 전달된 인증 정보를 받아 해당 조건에 부합하는 사용자 조회 쿼리를 수행합니다. 이 메서드는 **비밀번호 확인이나 인증을 직접 수행해서는 안 됩니다.**
- `validateCredentials`는 실제 `$user` 객체와 `$credentials`를 비교해 비밀번호가 유효한지 판단합니다. 보통 `Hash::check`를 사용해 `$user->getAuthPassword()`와 `$credentials['password']`를 비교합니다. Boolean(true/false)를 반환해야 합니다.
- `rehashPasswordIfRequired`는 필요 시 사용자 비밀번호를 재해싱 합니다. 예를 들어 `Hash::needsRehash`를 사용해 해싱 알고리즘 설정이 변경되었을 때 비밀번호를 갱신합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약 (The Authenticatable Contract)

`UserProvider` 메서드 중 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`는 `Authenticatable` 인터페이스 구현체를 반환해야 합니다. `Authenticatable` 계약은 다음과 같습니다:

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

- `getAuthIdentifierName`는 사용자의 "기본 키" 컬럼명을 반환합니다.
- `getAuthIdentifier`는 해당 사용자의 기본 키 값을 반환합니다. MySQL이라면 자동증가 ID 등이 여기에 해당합니다.
- `getAuthPasswordName`은 사용자 비밀번호 컬럼명을 반환합니다.
- `getAuthPassword`는 해시된 비밀번호를 반환합니다.

이 인터페이스를 구현하면 ORM이나 저장 방식에 관계없이 인증 시스템이 동작합니다. 기본적으로 Laravel `app/Models` 디렉터리의 `App\Models\User` 클래스가 이 인터페이스를 구현합니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel 기본 해싱 알고리즘은 bcrypt입니다. bcrypt "work factor"는 애플리케이션의 `config/hashing.php` 설정 파일 또는 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

CPU/GPU 성능 향상에 따라 bcrypt 작업량을 증가시키는 게 권장됩니다. 작업량 설정 변경 시 Laravel은 사용자들이 로그인할 때 _자동으로_ 비밀번호를 재해싱합니다. 이는 Laravel 스타터 킷을 통한 인증 이거나, [수동 사용자 인증](#authenticating-users)의 `attempt` 메서드를 통해 수행됩니다.

자동 재해싱은 애플리케이션 동작에 방해되지 않도록 설계되었으나, 필요하면 `hashing` 설정 파일을 퍼블리시 해 비활성화할 수 있습니다:

```shell
php artisan config:publish hashing
```

퍼블리시 후 `rehash_on_login` 값을 `false`로 설정하세요:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 다음 이벤트들에 대해 [리스너](/docs/12.x/events)를 정의할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                      |
| ----------------------------------------------- |
| `Illuminate\Auth\Events\Registered`             |
| `Illuminate\Auth\Events\Attempting`             |
| `Illuminate\Auth\Events\Authenticated`          |
| `Illuminate\Auth\Events\Login`                   |
| `Illuminate\Auth\Events\Failed`                  |
| `Illuminate\Auth\Events\Validated`               |
| `Illuminate\Auth\Events\Verified`                |
| `Illuminate\Auth\Events\Logout`                  |
| `Illuminate\Auth\Events\CurrentDeviceLogout`     |
| `Illuminate\Auth\Events\OtherDeviceLogout`       |
| `Illuminate\Auth\Events\Lockout`                 |
| `Illuminate\Auth\Events\PasswordReset`           |

</div>