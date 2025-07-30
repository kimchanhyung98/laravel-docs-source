# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한 (Login Throttling)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증](#http-basic-authentication)
    - [상태 비저장 HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호하기](#password-confirmation-protecting-routes)
- [커스텀 가드 추가하기](#adding-custom-guards)
    - [클로저 방식 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가하기](#adding-custom-user-providers)
    - [사용자 프로바이더 계약](#the-user-provider-contract)
    - [인증 가능(Authenticatable) 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/master/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자들이 애플리케이션에 "로그인" 할 수 있도록 인증 기능을 제공합니다. 이 기능을 구현하는 일은 복잡하고 보안상 위험도 있을 수 있습니다. 그래서 Laravel은 빠르고, 안전하며, 쉽게 인증을 구현할 수 있는 도구들을 제공하는 데 중점을 둡니다.

Laravel 인증 시스템의 핵심은 "가드(guards)"와 "프로바이더(providers)"로 구성됩니다. 가드는 요청마다 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel은 세션 저장과 쿠키를 사용해 상태를 유지하는 `session` 가드를 기본 제공합니다.

프로바이더는 영속 저장소에서 사용자를 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/master/eloquent)와 데이터베이스 쿼리 빌더를 사용하여 사용자를 조회하는 프로바이더를 기본적으로 제공합니다. 그러나 필요에 따라 애플리케이션에 맞는 추가 프로바이더를 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치해 있습니다. 이 파일에는 Laravel 인증 서비스의 동작을 조정할 수 있는 여러 문서화된 옵션이 포함되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(roles)" 및 "권한(permissions)"과 혼동하면 안 됩니다. 권한을 통한 사용자 액션 인가에 대해 더 알고 싶다면 [인가(authorization)](/docs/master/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트 (Starter Kits)

빠르게 시작하고 싶나요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 다른 URL로 접속해 보세요. 스타터 키트가 전체 인증 시스템의 스캐폴딩을 자동으로 처리해 줍니다!

**최종 애플리케이션에서 스타터 키트를 사용하지 않더라도, 스타터 키트를 설치해 보면 실제 Laravel 프로젝트에서 인증 기능이 어떻게 구현되는지 학습할 수 있는 좋은 기회가 됩니다.** 스타터 키트는 인증 컨트롤러, 라우트, 뷰를 포함하고 있어 해당 파일들을 살펴보면서 Laravel 인증 기능 구현 방식을 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

기본적으로 Laravel은 `app/Models` 디렉토리에 `App\Models\User` [Eloquent 모델](/docs/master/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

만약 애플리케이션이 Eloquent를 사용하지 않는다면, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우에는 공식 MongoDB의 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델을 위한 데이터베이스 스키마를 설계할 때, 비밀번호 컬럼은 최소 60자 이상이어야 합니다. 물론, Laravel 신규 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이보다 긴 길이의 컬럼을 생성합니다.

또한, `users` 테이블(또는 동등한 테이블)에 100자까지 허용하는 nullable 문자열 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 사용자가 로그인 시 "remember me" 옵션을 선택하면 토큰을 저장하는 데 사용됩니다. 기본 Laravel 마이그레이션에 이미 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 생태계 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기 전에 Laravel 인증 생태계의 전반적인 구조를 살펴보고 각 패키지의 목적을 설명하겠습니다.

우선 인증이 어떻게 작동하는지 생각해 보세요. 웹 브라우저를 사용하는 경우, 사용자는 로그인 폼에서 아이디와 비밀번호를 제공합니다. 이 인증 정보가 정확하면 애플리케이션은 인증된 사용자 정보를 사용자의 [세션](/docs/master/session)에 저장합니다. 브라우저는 세션 ID가 포함된 쿠키를 발급받아, 이후 요청 시 이 쿠키를 통해 올바른 세션에 사용자를 연동합니다. 세션 쿠키를 수신하면 애플리케이션은 세션 데이터를 읽어 인증 정보를 확인하고 해당 사용자를 "인증됨" 상태로 간주합니다.

원격 서비스가 API에 액세스하려면 웹 브라우저가 없으므로 일반적으로 쿠키를 사용하지 않고, 각 요청에 API 토큰을 보내 인증합니다. 애플리케이션은 API 토큰 테이블과 대조하여 요청을 인증된 사용자로 처리합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 내장 브라우저 인증 서비스

Laravel은 기본적으로 `Auth`와 `Session` 파사드로 접근하는 인증 및 세션 서비스를 포함합니다. 이 기능들은 브라우저에서 시작된 요청에 쿠키 기반 인증을 제공합니다. 사용자 자격 증명을 확인하고 인증하는 메서드를 제공하며, 또한 인증 데이터를 세션에 자동 저장하고 세션 쿠키를 발급합니다. 이 문서에서 이 서비스 사용법을 다룹니다.

**애플리케이션 스타터 키트**

이 문서에서 설명한 대로, 직접 Laravel 인증 서비스를 다루어 애플리케이션 맞춤 인증 계층을 만들 수도 있습니다. 하지만 더 빠른 시작을 위한 [무료 스타터 키트](/docs/master/starter-kits)를 제공하여, 완전한 인증 계층의 견고하고 현대적인 스캐폴딩을 제공합니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel API 인증 서비스

Laravel은 API 토큰 관리를 지원하는 두 개의 옵션 패키지인 [Passport](/docs/master/passport)와 [Sanctum](/docs/master/sanctum)을 제공합니다. 이 라이브러리들은 Laravel 내장 쿠키 기반 인증 서비스와 상호 배타적이지 않습니다. 주로 API 토큰 인증에 집중하는 반면, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션이 이 둘을 함께 사용합니다.

**Passport**

Passport는 인증을 위한 OAuth2 공급자로, 다양한 OAuth2 "grant type"을 통해 여러 유형의 토큰을 발급할 수 있습니다. 일반적으로 API 인증에 강력하지만 복잡한 패키지입니다. 대부분 애플리케이션은 OAuth2의 복잡한 기능을 필요로 하지 않아 사용자와 개발자가 혼란스러울 수 있습니다. SPA나 모바일 앱 인증에 OAuth2 기반 Passport를 사용하는 방법도 헷갈릴 수 있습니다.

**Sanctum**

OAuth2 복잡성과 개발자 혼란을 해소하고자, 웹 브라우저에서 사용하는 1차 요청과 API 토큰 요청 모두를 간편하게 처리하는 단순하고 효율적인 패키지로 [Laravel Sanctum](/docs/master/sanctum)을 만들었습니다. Sanctum은 1차 웹 UI와 API, 별도의 SPA 또는 모바일 클라이언트 모두를 지원하는 권장 인증 패키지입니다.

Sanctum 기반 애플리케이션은 요청이 들어오면 세션 쿠키를 포함해 인증 세션을 참조하는지 우선 확인합니다. 이 처리는 앞서 설명한 Laravel 내장 인증 서비스를 호출하여 수행합니다. 만약 세션 쿠키 인증이 아니라면 API 토큰을 검사하고, 토큰이 있으면 해당 토큰으로 인증 요청을 처리합니다. 자세한 작동 방식은 Sanctum 문서의 ["How it works"](/docs/master/sanctum#how-it-works)를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

요약하면, 브라우저를 통해 접속하는 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 사용합니다.

API를 제3자가 소비할 경우, API 토큰 인증을 위해 [Passport](/docs/master/passport) 또는 [Sanctum](/docs/master/sanctum) 중 하나를 선택합니다. 보통 단순하고 완성도 높은 API, SPA, 모바일 인증 및 권한(스코프 또는 능력) 지원이 가능한 Sanctum을 권장합니다.

SPA와 Laravel 백엔드를 조합할 경우, [Laravel Sanctum](/docs/master/sanctum)을 사용하세요. 이때는 백엔드 인증 라우트를 직접 구현하거나, [Laravel Fortify](/docs/master/fortify) 같은 헤드리스 인증 백엔드 서비스를 이용할 수 있습니다.

OAuth2 명세에서 제공하는 모든 기능이 절대적으로 필요할 경우 Passport를 선택하세요.

빠른 시작이 필요하다면, Laravel 내장 인증 서비스를 기본으로 하는 [애플리케이션 스타터 키트](/docs/master/starter-kits)를 추천합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 문서 부분은 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 통한 사용자 인증 방법을 다룹니다. UI 스캐폴딩을 제공하므로 빠르게 시작할 수 있습니다. Laravel 인증 시스템과 직접 통합하고 싶다면 [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치 (Install a Starter Kit)

가장 먼저, [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 설치하세요. 스타터 키트는 새 Laravel 애플리케이션에 인증을 통합하기 위한 세련된 시작점입니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기 (Retrieving the Authenticated User)

스타터 키트로 애플리케이션을 만들고 사용자가 등록 및 인증을 완료한 후, 종종 현재 인증된 사용자와 상호작용할 필요가 있습니다. 들어오는 요청을 처리하는 중에 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기...
$user = Auth::user();

// 인증된 사용자의 ID 가져오기...
$id = Auth::id();
```

또는, 사용자가 인증된 이후부터는 `Illuminate\Http\Request` 인스턴스를 통해서도 접근할 수 있습니다. 컨트롤러 메서드에 타입힌트를 지정하면 해당 객체가 자동으로 주입되므로, 모든 컨트롤러 메서드에서 손쉽게 인증된 사용자를 요청 객체의 `user` 메서드로 얻을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 존재하는 항공편 정보를 업데이트합니다.
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
#### 현재 사용자의 인증 여부 확인하기

들어오는 HTTP 요청을 수행하는 사용자가 인증되었는지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증되어 있으면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있습니다...
}
```

> [!NOTE]
> `check` 메서드를 사용해 인증 여부를 알아낼 수 있지만, 일반적으로는 특정 라우트나 컨트롤러 접근 전에 사용자 인증 여부를 미들웨어에서 검사합니다. 이에 관해서는 [라우트 보호하기](/docs/master/authentication#protecting-routes) 문서를 참조하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

[라우트 미들웨어](/docs/master/middleware)를 사용하면 인증된 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. Laravel은 기본적으로 `auth` 미들웨어를 제공합니다. 이 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 클래스에 대한 [미들웨어 별칭](/docs/master/middleware#middleware-aliases)입니다. Laravel이 내부적으로 별칭을 등록하므로, 라우트에 미들웨어만 연결하면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 기본적으로 `login` [이름 붙은 라우트](/docs/master/routing#named-routes)로 리다이렉션합니다. 이 동작을 변경하려면 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectGuestsTo` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저 방식 사용 예...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리다이렉션

`guest` 미들웨어는 인증된 사용자를 감지하면 기본적으로 `dashboard` 또는 `home` 이름 있는 라우트로 리다이렉션합니다. 이 동작 또한 `bootstrap/app.php` 내에서 `redirectUsersTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저 방식 사용 예...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

라우트에 `auth` 미들웨어를 연결할 때 어떤 "가드"를 사용할지 지정할 수 있습니다. 지정된 가드는 `auth.php` 설정 파일 내 `guards` 배열의 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

[애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용하는 경우, 로그인 시도에는 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본 설정으로는 여러 차례 로그인에 실패하면 1분간 로그인이 제한됩니다. 이 제한은 사용자 이메일/사용자명과 IP 주소별로 적용됩니다.

> [!NOTE]
> 애플리케이션 내 다른 라우트에도 속도 제한을 걸고 싶으면 [속도 제한 문서](/docs/master/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

Laravel 스타터 키트에 포함된 인증 스캐폴딩을 사용할 필요는 없습니다. 사용하지 않기로 결정했다면 Laravel 인증 클래스를 직접 사용해 인증을 관리할 수 있습니다. 걱정 마세요, 어렵지 않습니다!

Laravel 인증 서비스는 `Auth` [파사드](/docs/master/facades)를 통해 접근하며, 클래스 상단에 `Auth` 파사드를 임포트해야 합니다. 우선 `attempt` 메서드를 살펴봅시다. `attempt`는 로그인 폼에서 받은 자격 증명으로 인증을 시도할 때 주로 사용됩니다. 인증이 성공하면 `[세션](/docs/master/session)`을 재생성해 [세션 고정 공격](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

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
            'email' => '입력한 자격 증명이 기록과 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 첫 번째 인수로 키/값 배열을 받습니다. 이 배열의 값으로 데이터베이스에서 사용자를 찾습니다. 예제에서는 `email` 컬럼 값 기준으로 사용자를 조회합니다. 찾으면, 데이터베이스에 저장된 해시된 비밀번호와 전달받은 `password` 값을 비교합니다. 요청의 비밀번호는 직접 해시해서 전달할 필요 없습니다. Laravel이 자동으로 해시 후 비교합니다. 두 해시가 일치하면 인증 세션이 시작됩니다.

기본 `config/auth.php` 설정에서 Eloquent 사용자 프로바이더가 `App\Models\User` 모델과 연결되어 있음을 명심하세요. 필요 시 설정을 변경할 수 있습니다.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

Laravel 리다이렉터의 `intended` 메서드는 인증 미들웨어로 차단되기 전 접속하려 했던 URL로 사용자를 리다이렉트합니다. 이때 대상 URL이 없으면 인자로 지정된 대체 URI로 리다이렉트합니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

원하면 사용자 이메일과 비밀번호 외에도 추가 조건을 인증 쿼리에 넣을 수 있습니다. `attempt` 메서드에 넘기는 배열에 조건을 추가하면 됩니다. 예를 들어, 사용자가 활성 상태인지 확인할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

복잡한 조건은 배열에 클로저를 넣어 처리할 수 있습니다. 클로저에는 쿼리 인스턴스가 전달되어 맞춤 쿼리를 만들 수 있습니다:

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
> 여기서 `email`은 반드시 필요한 옵션이 아니라 단지 예시일 뿐입니다. 데이터베이스 사용자명 컬럼에 맞는 이름을 사용하세요.

`attemptWhen` 메서드는 두 번째 인수로 클로저를 받고, 인증 전 사용자를 더 엄격히 검사할 때 사용합니다. 클로저의 인수는 가능한 사용자 객체이며, `true` 또는 `false`를 반환해 인증 가능 여부를 결정합니다:

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
#### 특정 가드 인스턴스 접근하기

`Auth` 파사드의 `guard` 메서드를 사용해 인증에 특정 가드 인스턴스를 지정할 수 있습니다. 이를 통해 애플리케이션의 일부 영역은 전혀 다른 인증 가능한 모델이나 사용자 테이블을 사용하여 인증을 분리할 수 있습니다.

`guard` 인수는 `auth.php` 설정 파일의 가드 키 중 하나여야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹 애플리케이션 로그인 폼에 "remember me" 체크박스가 있습니다. 이 기능을 넣으려면 `attempt` 메서드 두 번째 인수에 불린 값을 넣어주세요.

이 값이 `true`면 Laravel은 수동 로그아웃 전까지 사용자를 무기한 인증 상태로 유지합니다. 사용자 테이블에 문자열 타입 `remember_token` 컬럼이 있어야 하며, 기본 Laravel 마이그레이션에 이미 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자를 기억하는 중입니다...
}
```

애플리케이션이 "remember me" 기능을 제공한다면, 현재 인증된 사용자가 "remember me" 쿠키를 통해 인증되었는지 확인할 때 `viaRemember` 메서드를 쓸 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증하기

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 설정하려면, `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 전달하세요. 이 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [인터페이스](/docs/master/contracts)를 구현해야 합니다. 기본 제공되는 `App\Models\User`가 이를 구현합니다. 이 방법은 사용자 등록 직후와 같이 이미 인증된 사용자 인스턴스가 있을 때 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드 두 번째 인수에 불린 값을 넣어 "remember me" 기능을 켤 수 있습니다. 이 경우 세션은 무기한 인증 상태를 유지합니다:

```php
Auth::login($user, $remember = true);
```

필요하면 가드를 지정한 뒤 `login` 메서드를 호출할 수도 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증하기

DB 기본 키를 사용해 사용자를 인증할 수도 있습니다. `loginUsingId` 메서드는 인증할 사용자 기본 키를 인수로 받습니다:

```php
Auth::loginUsingId(1);
```

`loginUsingId` 메서드에 `remember` 옵션을 불린으로 전달해 "remember me" 기능을 쓸 수 있습니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 사용자 인증하기

`once` 메서드를 사용하면 세션이나 쿠키 없이 단 한 번의 요청에 대해서만 인증할 수 있습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 로그인 페이지 없이 간단하게 사용자 인증을 구현할 수 있는 방식입니다. 시작하려면 `auth.basic` [미들웨어](/docs/master/middleware)를 라우트에 연결하세요. `auth.basic` 미들웨어는 Laravel에 내장되어 있어 따로 정의할 필요가 없습니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth.basic');
```

이 미들웨어를 라우트에 연결하면, 브라우저에서 해당 URL 접속 시 자동으로 사용자명과 비밀번호 입력 창이 표시됩니다. 기본적으로 `auth.basic`은 사용자명 컬럼으로 `users` 테이블 내 `email` 컬럼을 사용한다고 가정합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고사항

PHP FastCGI와 Apache를 사용해 Laravel을 제공하는 경우, HTTP 기본 인증이 제대로 작동하지 않을 수 있습니다. 이런 문제를 해결하려면 애플리케이션 `.htaccess` 파일에 아래 내용을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 상태 비저장 HTTP 기본 인증 (Stateless HTTP Basic Authentication)

HTTP 기본 인증을 세션 쿠키 없이도 사용할 수 있습니다. 이는 API 요청에 HTTP 인증 방식을 적용할 때 주로 유용합니다. 이를 위해 [미들웨어](/docs/master/middleware)를 정의하여 `onceBasic` 메서드를 호출하세요. 만약 `onceBasic`가 응답을 반환하지 않으면 요청을 어플리케이션 내부로 전달합니다:

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

이 미들웨어를 라우트에 연결하세요:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 여기에 접근 가능합니다...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 애플리케이션에서 수동으로 로그아웃시키려면 `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 인증 정보를 세션에서 제거하며, 이후 요청들은 인증되지 않은 상태가 됩니다.

`logout` 호출 후 세션을 무효화하고 [CSRF 토큰](/docs/master/csrf)를 재생성하는 것이 권장됩니다. 로그아웃 후 보통 애플리케이션 루트로 리다이렉션합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션에서 사용자를 로그아웃합니다.
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
### 다른 기기의 세션 무효화 (Invalidating Sessions on Other Devices)

Laravel은 사용자가 현재 기기의 세션은 유지하면서 다른 기기에서 활성화된 세션만 무효화하는 기능도 제공합니다. 이 기능은 보통 사용자가 비밀번호를 변경 또는 업데이트할 때 유용합니다.

이 기능을 사용하려면, 먼저 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어를 세션 인증을 적용할 라우트에 포함해야 합니다. 보통 라우트 그룹에 이 미들웨어를 적용하며, 기본적으로 `auth.session` [미들웨어 별칭](/docs/master/middleware#middleware-aliases)으로 연결할 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 다음 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 현재 비밀번호를 확인하는 절차를 요구하며, 이를 입력받는 폼이 필요합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 호출 시 사용자의 다른 기기의 모든 세션이 완전히 무효화되어 다른 곳에서는 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션에서 민감한 작업을 수행할 때, 사용자가 비밀번호를 재확인하도록 요구할 수 있습니다. Laravel은 이를 편하게 만드는 내장 미들웨어를 제공합니다. 구현하려면 두 개의 라우트를 정의해야 합니다. 하나는 비밀번호 재확인을 요청하는 뷰를 보여주는 라우트이고, 다른 하나는 비밀번호 유효성 검사 후 원래 의도한 위치로 리다이렉션하는 라우트입니다.

> [!NOTE]
> 아래 문서는 직접 Laravel 비밀번호 확인 기능과 통합하는 법을 다룹니다. 더 빠르게 시작하고자 한다면 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)에서 지원하는 기능을 사용하는 것도 좋습니다!

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

한 번 비밀번호를 재확인하면, 보통 3시간 동안 다시 묻지 않습니다. 이 시간은 애플리케이션 `config/auth.php` 파일 내 `password_timeout` 값을 변경해 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자가 비밀번호를 확인하도록 요청하는 뷰를 반환하는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

반환되는 뷰에는 `password` 필드가 포함된 폼이 있어야 합니다. 물론, 애플리케이션 내 민감한 영역임을 알리고 비밀번호를 입력해야 한다는 설명 텍스트도 넣어 주세요.

<a name="confirming-the-password"></a>
#### 비밀번호 확인

다음은 "비밀번호 확인" 뷰에서 전송된 요청을 처리하는 라우트입니다. 비밀번호 유효성을 검사하고, 확인되면 사용자를 원래 목적지로 리다이렉트합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['입력한 비밀번호가 기록과 일치하지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

위 라우트를 자세히 보면, 요청 내 `password` 필드를 현재 인증된 사용자의 암호와 비교하는 `Hash::check`를 쓰고 있습니다. 비밀번호가 맞으면 Laravel 세션에 `passwordConfirmed`를 호출해 비밀번호 확인 시점을 기록합니다. 이를 통해 Laravel은 언제 사용자가 마지막으로 비밀번호를 확인했는지 판단합니다. 마지막으로 사용자 의도 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호하기

최근에 비밀번호 확인을 요구해야 하는 작업을 수행하는 라우트에는 `password.confirm` 미들웨어를 반드시 할당하세요. 이 미들웨어는 기본 Laravel 설치에 포함되어 있으며, 사용자의 의도 목적지를 세션에 저장해 비밀번호 확인 후 해당 위치로 리다이렉트해줍니다. 미들웨어는 인증되지 않은 사용자는 `password.confirm` 이름 붙은 라우트로 리다이렉트합니다:

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

`Auth` 파사드의 `extend` 메서드를 이용해 직접 인증 가드를 정의할 수 있습니다. 이 코드는 보통 [서비스 프로바이더](/docs/master/providers)에 둡니다. Laravel은 기본적으로 `AppServiceProvider`를 제공하므로, 그곳에 추가할 수 있습니다:

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
            // Illuminate\Contracts\Auth\Guard 구현체 반환...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시에서, `extend`에 전달된 콜백 함수는 반드시 `Illuminate\Contracts\Auth\Guard` 구현 객체를 반환해야 하며, 이 인터페이스를 구현하는 여러 메서드를 직접 작성해야 합니다. 커스텀 가드 정의 후, `auth.php` 설정 파일 내 `guards` 배열에 해당 가드를 등록하세요:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 방식 요청 가드 (Closure Request Guards)

커스텀 HTTP 요청 기반 인증 시스템을 간단히 구현하려면 `Auth::viaRequest` 메서드를 사용하세요. 이 메서드는 단일 클로저를 이용해 인증 과정을 빠르게 정의할 수 있습니다.

`AppServiceProvider`의 `boot` 메서드 내에서 `viaRequest`를 호출합니다. 첫 번째 인수는 인증 드라이버 이름이며, 두 번째는 클로저로 들어오는 `Request` 객체를 받고 인증된 사용자 인스턴스 혹은 실패 시 `null`을 반환해야 합니다:

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

커스텀 인증 드라이버를 정의한 뒤, `auth.php` 설정 파일 내 `guards`에서 드라이버로 설정합니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 라우트에 인증 미들웨어를 할당할 때 가드를 참조할 수 있습니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가하기 (Adding Custom User Providers)

전통적인 관계형 데이터베이스가 아닌 다른 저장소(예: MongoDB)를 사용자 저장소로 사용하는 경우, 직접 사용자 프로바이더를 구현해야 할 수 있습니다. `Auth` 파사드의 `provider` 메서드로 커스텀 사용자 프로바이더를 등록하세요. 이 콜백은 `Illuminate\Contracts\Auth\UserProvider` 구현체를 반환해야 합니다:

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

`provider` 메서드로 프로바이더 등록 후, `auth.php` 파일에서 해당 드라이버를 사용하는 프로바이더를 정의하세요:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그 다음, `guards` 설정에서 이 프로바이더를 참조하세요:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등 영속 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스 덕분에 저장소 방식이나 사용자 클래스 형식에 상관없이 Laravel 인증이 작동합니다.

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

- `retrieveById`는 사용자 키(예: MySQL 자동 증가 ID)를 받고, 해당 사용자의 `Authenticatable` 구현체를 반환해야 합니다.
- `retrieveByToken`은 고유한 `$identifier`와 "remember me" `$token`을 기준으로 사용자를 조회합니다. 기존과 같이 해당하는 사용자 객체를 반환해야 합니다.
- `updateRememberToken`은 `$user` 인스턴스의 `remember_token`을 새 `$token`으로 갱신합니다. "remember me" 인증이나 로그아웃 시 새로운 토큰이 할당됩니다.
- `retrieveByCredentials`는 `Auth::attempt`에 전달된 자격 증명 배열을 받고, 해당 조건과 일치하는 사용자를 조회해 인증 가능한 `Authenticatable` 구현체를 반환합니다. 비밀번호 검증은 하지 않고, 단순 조회만 수행해야 합니다.
- `validateCredentials`는 `$user` 객체와 `$credentials`를 비교하여 인증 여부를 결정합니다(일반적으로 `Hash::check`로 해시된 비밀번호를 확인함). 참/거짓을 반환합니다.
- `rehashPasswordIfRequired`는 필요에 따라 사용자 비밀번호를 재해싱하여 저장소에 갱신합니다. `Hash::needsRehash`와 `Hash::make`를 사용합니다.

<a name="the-authenticatable-contract"></a>
### 인증 가능(Authenticatable) 계약 (The Authenticatable Contract)

`UserProvider`가 반환하는 사용자 객체는 반드시 `Authenticatable` 계약을 구현해야 합니다. 이 계약은 다음과 같습니다:

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
- `getAuthIdentifier`는 사용자의 기본 키 값을 반환합니다(예: MySQL 자동 증가 ID).
- `getAuthPasswordName`은 사용자의 비밀번호 컬럼명을 반환합니다.
- `getAuthPassword`는 사용자의 해시된 비밀번호 값을 반환합니다.
- `getRememberToken`과 `setRememberToken`은 "remember me" 토큰 값을 가져오고 설정합니다.
- `getRememberTokenName`은 해당 토큰 컬럼명을 반환합니다.

이 인터페이스 덕분에 어떤 ORM이나 저장소를 쓰든 사용자 클래스만 인터페이스를 구현하면 Laravel 인증 생태계와 호환됩니다. 기본 Laravel에서 `App\Models\User` 클래스가 이 인터페이스를 이미 구현하고 있습니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt의 "작업 난이도(work factor)"는 애플리케이션 `config/hashing.php` 설정 파일 또는 `BCRYPT_ROUNDS` 환경 변수로 조정 가능합니다.

일반적으로 CPU/GPU 처리 성능이 향상됨에 따라 bcrypt 작업 난이도를 높여야 합니다. 그런 경우, Laravel은 사용자가 인증 시도할 때 자동으로 비밀번호를 재해싱하여 데이터베이스를 갱신합니다. 이는 스타터 키트 기반 인증 혹은 [`attempt` 메서드](#authenticating-users) 수동 인증 시 모두 적용됩니다.

자동 비밀번호 재해싱이 문제를 일으키면, `hashing` 설정 파일을 발행하여 기능을 비활성화할 수 있습니다:

```shell
php artisan config:publish hashing
```

설정 파일을 발행하면, `rehash_on_login` 설정을 `false`로 변경하세요:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정 중 다양한 [이벤트](/docs/master/events)를 발생시킵니다. 다음 이벤트들에 대해 [리스너](/docs/master/events)를 정의할 수 있습니다:

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