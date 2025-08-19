# 인증(Authentication)

- [소개](#introduction)
    - [스타터 킷](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 킷 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기 기능](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [상태 없는 HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기에서 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [사용자 정의 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [사용자 정의 사용자 제공자 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 로그인](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 '로그인'할 수 있는 방법을 제공합니다. 이러한 기능을 웹 애플리케이션에 구현하는 것은 복잡하고 위험할 수 있습니다. 이를 위해 Laravel은 빠르고 안전하며 쉽게 인증을 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 기능은 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 사용자가 각 요청마다 어떻게 인증되는지 정의합니다. 예를 들어, Laravel에는 session 스토리지와 쿠키를 이용하여 상태를 유지하는 `session` 가드가 기본으로 제공됩니다.

프로바이더는 사용자를 영구적인 저장소에서 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 이용한 사용자 조회를 기본 지원합니다. 물론, 필요에 따라 추가 프로바이더를 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일은 Laravel의 인증 서비스를 세밀하게 조정할 수 있는 다양한 옵션을 잘 설명하여 제공합니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(roles)"과 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 이용해 사용자 작업을 인가하는 방법은 [인가(authorization)](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 킷 (Starter Kits)

빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 설치하세요. 데이터베이스 마이그레이션을 완료한 뒤, 브라우저에서 `/register`나 애플리케이션에 할당된 다른 URL로 이동하면 됩니다. 스타터 킷이 전체 인증 시스템의 스캐폴딩을 자동으로 처리해줍니다!

**최종적으로 스타터 킷을 사용하지 않는다고 해도, 실제 Laravel 프로젝트에 [스타터 킷](/docs/12.x/starter-kits)을 설치해보면 Laravel의 인증 기능들을 어떻게 구현하는지 학습할 수 있는 좋은 기회가 됩니다.** Laravel 스타터 킷에는 인증 컨트롤러, 라우트, 뷰 등이 포함되어 있으므로, 해당 파일의 코드를 보면서 인증 기능의 실제 구현 방법을 배울 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

Laravel에는 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)이 포함되어 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

만약 애플리케이션이 Eloquent를 사용하지 않는 경우에는 Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우, 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델을 위한 데이터베이스 스키마를 생성할 때, 비밀번호 컬럼의 길이가 최소 60자 이상인지 확인해야 합니다. 물론, 새 Laravel 애플리케이션에 기본 포함된 `users` 테이블 마이그레이션에서는 이미 이보다 더 긴 컬럼을 생성합니다.

또한, `users` (혹은 이에 상응하는) 테이블에는 100자 길이의 nullable string 타입 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 "사용자 기억하기(remember me)" 옵션 선택 시 토큰 저장에 사용됩니다. 역시, 기본 포함된 `users` 테이블 마이그레이션에 이미 해당 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 다양한 패키지를 제공합니다. 계속 읽기 전에, Laravel의 인증 에코시스템을 전반적으로 살펴보고 각각의 패키지가 어떤 용도로 제공되는지 설명합니다.

먼저, 인증이 어떻게 동작하는지 생각해 봅시다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼을 통해 사용자명과 비밀번호를 입력합니다. 이 정보가 올바르면, 애플리케이션은 인증된 사용자 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 담겨 있어, 이후의 요청에서 해당 사용자를 올바른 세션과 연결해줍니다. 세션 쿠키를 받은 후, 애플리케이션은 세션 ID를 바탕으로 세션 데이터를 조회하며, 세션에 인증 정보가 저장되어 있는지 확인하고 사용자를 "인증된 상태"로 간주합니다.

원격 서비스가 API에 액세스하기 위해 인증해야 할 때는, 웹 브라우저가 없으므로 쿠키 대신 API 토큰을 사용합니다. 원격 서비스는 매 요청마다 API에 토큰을 전송하며, 애플리케이션은 해당 토큰이 유효한지 검사하여 해당 토큰과 연관된 사용자가 요청한 것으로 "인증" 처리를 합니다.

#### Laravel의 내장 브라우저 인증 서비스

Laravel에는 `Auth`와 `Session` 파사드로 접근할 수 있는 인증 및 세션 서비스가 내장되어 있습니다. 이 기능들은 웹 브라우저에서 발생하는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명 확인과 사용자 인증, 인증 정보를 세션에 저장하고 세션 쿠키를 발급하는 기능을 지원합니다. 이 서비스들의 활용 방법은 본 문서에서 자세히 다루고 있습니다.

**애플리케이션 스타터 킷**

이 문서에서 안내하는 것처럼, 인증 서비스를 직접 활용하여 자체 인증 레이어를 구축할 수 있습니다. 하지만, 더욱 빠르게 시작할 수 있도록 [무료 스타터 킷](/docs/12.x/starter-kits)을 제공하여, 인증 레이어 전체의 견고하고 현대적인 스캐폴딩을 준비해 드립니다.

#### Laravel의 API 인증 서비스

Laravel은 API 토큰을 관리하고 API 토큰 요청을 인증할 수 있도록 [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum) 두 가지 선택적 패키지를 제공합니다. 이 라이브러리들은 Laravel의 내장 쿠키 기반 인증 라이브러리와 상호 배타적이지 않습니다. 이들 라이브러리는 주로 API 토큰 인증에 초점을 두며, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 초점을 둡니다. 많은 애플리케이션에서 내장 쿠키 기반 인증 서비스와 API 인증 패키지 중 하나를 동시에 사용할 수 있습니다.

**Passport**

Passport는 OAuth2 인증 프로바이더로, 다양한 유형의 토큰을 발급할 수 있는 여러 OAuth2 "Grant Type"을 제공합니다. 전반적으로 강력하고 복잡한 API 인증 패키지입니다. 다만, 대부분의 애플리케이션에는 OAuth2에서 제공하는 복잡한 기능이 불필요하며, 이는 사용자와 개발자 모두에게 혼란을 줄 수 있습니다. 더불어, SPA 애플리케이션이나 모바일 애플리케이션에서 OAuth2 인증 프로바이더(Passport 등)를 사용하는 방법 역시 혼란을 일으킬 소지가 있습니다.

**Sanctum**

OAuth2의 복잡성과 관련된 개발자 혼란을 해소하기 위해, 웹 브라우저의 1차 요청과 API 요청(토큰 사용) 모두를 처리할 수 있는 더 간단하고 직관적인 인증 패키지를 개발했습니다. 이렇게 탄생한 것이 [Laravel Sanctum](/docs/12.x/sanctum)으로, 별도의 백엔드 Laravel 애플리케이션 외에 프론트엔드(UI), SPA, 모바일까지 아우르며 사용하기에 적합한 권장 인증 패키지입니다.

Laravel Sanctum은 웹과 API 인증을 모두 융합한 패키지로, 애플리케이션 전체 인증 과정을 관리할 수 있습니다. 그 원리는, 요청을 수신하면 먼저 세션 쿠키에 인증 세션이 포함되어 있는지 확인합니다(앞서 언급한 내장 인증 서비스 활용). 세션 쿠키를 통한 인증이 아니라면, API 토큰이 있는지 확인하고, 있다면 해당 토큰으로 인증 처리합니다. 이 동작 원리에 대한 더 자세한 설명은 Sanctum ["작동 방식"](/docs/12.x/sanctum#how-it-works) 문서를 참고하세요.

#### 요약 및 인증 스택 선택

정리하자면, 브라우저를 통해 접근하는 단일형(monolithic) Laravel 애플리케이션이라면 Laravel의 내장 인증 서비스를 활용합니다.

다음으로, 외부에서 소비할 수 있는 API를 제공한다면 [Passport](/docs/12.x/passport) 또는 [Sanctum](/docs/12.x/sanctum) 중 하나를 선택하여 API 토큰 인증을 구현합니다. 일반적으로 Sanctum이 단순하면서도 API, SPA, 모바일 인증까지 폭넓게 지원하므로 가능하다면 Sanctum을 권장합니다("scopes"나 "abilities" 기능 포함).

만약 단일 페이지 애플리케이션(SPA)이 Laravel 백엔드를 사용할 경우 [Sanctum](/docs/12.x/sanctum)을 사용해야 합니다. Sanctum 사용 시, [직접 인증 라우트를 구현](#authenticating-users)하거나, [Laravel Fortify](/docs/12.x/fortify)를 Headless 인증 백엔드 서비스로 활용하여 회원가입, 비밀번호 재설정, 이메일 인증 등 기능의 라우트와 컨트롤러를 제공합니다.

OAuth2 사양이 제공하는 모든 기능이 반드시 필요한 경우에만 Passport를 선택하세요.

그리고, 빠르게 시작하고 싶다면 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 권장합니다. 스타터 킷에는 Laravel의 권장 인증 서비스가 이미 탑재되어 있습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 섹션에서는 UI 스캐폴딩이 포함된 [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 통해 사용자를 인증하는 방법을 다룹니다. 인증 시스템과 직접 연동하려면 [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치 (Install a Starter Kit)

먼저, [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 설치하세요. 스타터 킷은 새 Laravel 애플리케이션에 인증을 적용할 수 있도록 세련된 시작 지점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회 (Retrieving the Authenticated User)

스타터 킷으로 애플리케이션을 생성하고, 사용자가 회원가입 및 인증할 수 있게 되면, 종종 현재 인증된 사용자와 상호작용할 필요가 있습니다. 들어오는 요청을 처리할 때 `Auth` 파사드의 `user` 메서드를 이용해 인증된 사용자를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

또한, 사용자가 인증된 후에는 `Illuminate\Http\Request` 인스턴스로도 인증된 사용자에 접근할 수 있습니다. 타입 힌트로 지정한 클래스는 컨트롤러 메서드에 자동으로 주입됩니다. `Illuminate\Http\Request` 객체에 타입 힌트를 지정하면, 컨트롤러의 어떤 메서드에서도 request의 `user` 메서드를 통해 인증된 사용자에 손쉽게 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

#### 현재 사용자가 인증되었는지 확인

들어오는 HTTP 요청의 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증되었으면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` 메서드로 사용자의 인증 여부를 확인할 수 있지만, 보통은 미들웨어로 특정 라우트나 컨트롤러 접근 전 인증을 강제합니다. 이 방법에 대한 자세한 내용은 [라우트 보호](/docs/12.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/12.x/middleware)를 사용하여, 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 대상으로 하는 `auth` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)을 기본 제공하므로, 라우트 정의에 미들웨어를 간단히 추가하면 됩니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [이름 지정 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

#### 인증된 사용자 리다이렉트

`guest` 미들웨어가 인증된 사용자를 감지하면, 사용자를 `dashboard` 또는 `home` 이름 지정 라우트로 리다이렉트합니다. 이 동작 역시 `bootstrap/app.php`에서 `redirectUsersTo` 메서드로 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

#### 가드 지정

`auth` 미들웨어를 라우트에 적용할 때, 인증에 사용할 "가드"를 명시할 수 있습니다. 지정하는 가드는 `auth.php` 설정 파일의 `guards` 배열 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

[애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 사용하는 경우, 로그인 시도에 대한 속도 제한(rate limiting)이 기본적으로 적용됩니다. 사용자가 올바르지 않은 자격 증명을 여러 번 입력하면 1분간 로그인을 할 수 없게 됩니다. 제한은 사용자의 사용자명/이메일과 IP 주소 조합에 따라 고유하게 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에 속도 제한을 적용하려면 [요청 속도 제한 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

[애플리케이션 스타터 킷](/docs/12.x/starter-kits)에 포함된 인증 스캐폴딩을 반드시 사용할 필요는 없습니다. 스캐폴딩을 사용하지 않을 경우, Laravel의 인증 클래스를 직접 이용하여 사용자 인증을 관리할 수 있습니다. 걱정하지 마세요, 매우 쉽습니다!

Laravel 인증 서비스는 `Auth` [파사드](/docs/12.x/facades)로 접근하며, 클래스 상단에 `Auth` 파사드를 반드시 import 해야 합니다. 그리고 `attempt` 메서드를 사용합니다. 보통 `attempt` 메서드는 애플리케이션의 "로그인" 폼으로부터의 인증 시도 처리에 사용됩니다. 인증에 성공하면 [세션](/docs/12.x/session) 고정 공격(session fixation) 방지를 위해 사용자의 세션을 재생성해야 합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
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

`attempt` 메서드는 첫 번째 인자로 key-value 배열을 받습니다. 이 배열의 값은 데이터베이스에서 사용자를 찾는 데 사용됩니다. 위 예시의 경우, `email` 컬럼 값을 바탕으로 사용자를 조회합니다. 사용자가 찾으면, 데이터베이스에 저장된 해시된 비밀번호와 전달받은 `password` 값을 내부적으로 비교합니다. 요청된 `password`는 직접 해시할 필요가 없습니다. 프레임워크가 알아서 암호화된 비밀번호와 비교해줍니다. 두 비밀번호가 일치하면 인증된 세션이 시작됩니다.

Laravel의 인증 서비스는 인증 가드의 "프로바이더" 설정에 따라 데이터베이스에서 사용자를 조회합니다. 기본 설정 파일(`config/auth.php`)에서는 Eloquent 사용자 프로바이더가 명시되어 있으며, 사용자를 조회할 때 `App\Models\User` 모델을 사용하도록 설정되어 있습니다. 애플리케이션 요구에 따라 해당 설정값을 변경할 수 있습니다.

`attempt` 메서드는 인증에 성공하면 `true`, 그렇지 않으면 `false`를 반환합니다.

`intended` 메서드는 인증 미들웨어에 가로채이기 전 사용자가 접근을 시도한 URL로 리다이렉트합니다. 만약 접근하려던 URI가 없으면 대체 경로를 지정할 수 있습니다.

#### 추가 조건 지정

이메일과 비밀번호 외에, 인증 쿼리에 추가 조건을 넣고 싶다면, `attempt` 메서드에 전달하는 배열에 조건을 추가하면 됩니다. 예를 들어, 사용자가 "활성(active)" 상태인지 확인할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

복잡한 쿼리 조건의 경우, credentials 배열에 클로저를 전달할 수도 있습니다. 이 클로저는 쿼리 인스턴스를 받아 애플리케이션 요구에 맞게 쿼리를 커스터마이징할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> [!WARNING]
> 여기서 `email`은 단지 예시일 뿐, 필수 옵션은 아닙니다. 데이터베이스 상에서 "사용자명"에 해당하는 컬럼을 이용하세요.

`attemptWhen` 메서드를 사용하면, 두 번째 인자로 클로저를 전달하여 사용자를 인증하기 전에 추가 검사를 수행할 수 있습니다. 클로저는 잠재적 사용자 인스턴스를 받고, 인증 가능 여부(true/false)를 반환합니다:

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

#### 특정 가드 인스턴스 사용

`Auth` 파사드의 `guard` 메서드를 통해, 인증에 사용할 가드 인스턴스를 지정할 수 있습니다. 이를 통해 애플리케이션의 각 독립 영역마다 별도의 인증 모델이나 사용자 테이블로 인증을 관리할 수 있습니다.

`guard` 메서드에 전달하는 가드 이름은 `auth.php` 설정 파일에 등록된 가드 중 하나여야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 기능 (Remembering Users)

많은 웹 애플리케이션에는 로그인 폼에서 "로그인 상태 유지" 체크박스가 있습니다. 이런 기능을 제공하려면, `attempt` 메서드의 두 번째 인자로 boolean 값을 전달하면 됩니다.

이 값이 `true`면, 사용자는 직접 로그아웃하지 않는 한 무기한 인증 상태가 유지됩니다. 이 기능을 사용하려면, `users` 테이블에 "remember me" 토큰 저장용 string 타입 `remember_token` 컬럼이 필요합니다. Laravel의 기본 사용자 테이블 마이그레이션에 이미 해당 컬럼이 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

애플리케이션에서 "로그인 상태 유지" 기능을 제공하는 경우, `viaRemember` 메서드로 현재 인증 사용자가 "remember me" 쿠키로 인증되었는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

#### 사용자 인스턴스 직접 인증

이미 존재하는 사용자 인스턴스를 인증 중 사용자로 설정해야 한다면, 해당 사용자 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하면 됩니다. 이때 사용자 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 합니다. Laravel의 기본 `App\Models\User` 모델은 이미 이 인터페이스를 구현합니다. 흔히 사용자가 회원가입 직후 곧바로 로그인 처리할 때 이 방식이 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

두 번째 인자로 boolean 값을 전달하면 "로그인 상태 유지" 기능을 사용할 수 있습니다. 즉, 이 경우 세션이 무기한 인증 상태로 유지되거나, 사용자가 직접 로그아웃할 때까지 유지됩니다:

```php
Auth::login($user, $remember = true);
```

필요하다면, `login` 메서드 호출 전 인증 가드를 지정할 수도 있습니다:

```php
Auth::guard('admin')->login($user);
```

#### ID로 사용자 인증

데이터베이스 레코드의 기본 키(primary key)를 이용해 사용자를 인증하려면, `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증할 사용자의 기본 키를 인자로 받습니다:

```php
Auth::loginUsingId(1);
```

두 번째 인자로 boolean 값을 전달하여 "로그인 상태 유지" 기능을 적용할 수 있습니다. 이는 무기한 인증 유지 또는 직접 로그아웃까지 인증됨을 의미합니다:

```php
Auth::loginUsingId(1, remember: true);
```

#### 1회성 인증

한 번의 요청에서만 사용자를 인증하고자 한다면, `once` 메서드를 사용할 수 있습니다. 이 메서드는 세션이나 쿠키를 사용하지 않으며, `Login` 이벤트도 발송하지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증 (HTTP Basic Authentication)

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 없이 빠르게 인증을 구현할 수 있는 방법입니다. 사용하려면 [미들웨어](/docs/12.x/middleware)인 `auth.basic`을 라우트에 적용하세요. 이 미들웨어는 Laravel 프레임워크에 기본 내장되어 있으므로 직접 정의할 필요가 없습니다:

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

이 미들웨어를 라우트에 적용하면, 브라우저에서 해당 라우트에 접근할 때 인증 창이 자동으로 표시됩니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자명으로 사용합니다.

#### FastCGI 참고사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache로 Laravel 애플리케이션을 구동할 때 HTTP Basic 인증이 올바로 동작하지 않을 수 있습니다. 이런 문제가 발생하면, 애플리케이션의 `.htaccess` 파일에 다음 줄을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

### 상태 없는 HTTP Basic 인증 (Stateless HTTP Basic Authentication)

세션에 사용자 식별자 쿠키를 저장하지 않고 HTTP Basic 인증을 사용할 수도 있습니다. 특히, API의 인증에 HTTP 인증을 사용하는 경우에 유용합니다. 이 기능을 위해서는, `onceBasic` 메서드를 호출하는 [미들웨어](/docs/12.x/middleware)를 정의하세요. 만약 `onceBasic`에서 응답이 반환되지 않으면, 요청은 애플리케이션의 다음 단계로 전달됩니다:

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
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

이제, 해당 미들웨어를 라우트에 적용합니다:

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 수동으로 로그아웃 시키려면, `Auth` 파사드의 `logout` 메서드를 사용하세요. 이로써 사용자의 세션에서 인증 정보가 제거되어, 이후의 요청에서 인증되지 않게 됩니다.

`logout` 호출 후에는, 사용자의 세션 무효화 및 [CSRF 토큰](/docs/12.x/csrf) 재생성을 권장합니다. 보통 로그아웃 후에는 애플리케이션의 루트 경로로 리다이렉트합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
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
### 다른 기기에서 세션 무효화 (Invalidating Sessions on Other Devices)

Laravel은 현재 기기를 제외한 사용자의 다른 기기에서 로그인된 세션을 무효화하는 기능을 제공합니다. 이 기능은 보통 사용자가 비밀번호를 변경하거나 업데이트할 때, 다른 기기에서는 강제로 로그아웃시키고 현재 기기는 인증 상태를 유지하고 싶을 때 사용합니다.

먼저, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증이 필요한 라우트에 포함되어 있는지 확인하세요. 일반적으로 대부분의 라우트에 적용하려면, 라우트 그룹 정의에 미들웨어를 추가하면 됩니다. 기본적으로 `AuthenticateSession` 미들웨어는 `auth.session` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 라우트에 적용할 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

이제, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이때, 반드시 현재 비밀번호를 확인해야 하며, 비밀번호는 입력 폼을 통해 받도록 해야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 메서드가 호출되면, 사용자의 다른 세션이 완전히 무효화되어 이전에 인증된 모든 가드에서 "로그아웃"됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 개발하다 보면, 특정 작업을 실행하거나 민감한 영역으로 이동하기 전에 사용자의 비밀번호 재확인을 요구해야 할 때가 있습니다. Laravel은 이를 쉽게 처리할 수 있도록 내장 미들웨어를 제공합니다. 이 기능을 구현하려면 두 개의 라우트가 필요합니다: 사용자의 비밀번호 확인을 요청하는 뷰를 표시하는 라우트와, 비밀번호 유효성을 검증해 사용자를 의도한 위치로 리다이렉트하는 라우트입니다.

> [!NOTE]
> 아래 내용은 Laravel의 비밀번호 확인 기능을 직접 통합하는 방법을 다루지만, 더 빠르게 시작하려면 [Laravel 애플리케이션 스타터 킷](/docs/12.x/starter-kits)에서 이 기능을 바로 사용할 수 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

비밀번호를 한 번 확인한 사용자에게는 3시간 이내에는 비밀번호를 다시 확인하도록 요구하지 않습니다. 하지만, 사용자가 재확인 메시지를 받기까지의 시간을 애플리케이션의 `config/auth.php` 설정 파일 중 `password_timeout` 값으로 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

#### 비밀번호 확인 폼

먼저, 사용자의 비밀번호 확인을 요청하는 뷰를 표시하는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트에서는, 반환되는 뷰에 반드시 `password` 필드를 포함한 폼이 있어야 합니다. 또한, 민감한 영역에 접근하려 하니 비밀번호를 재확인해야 한다는 설명도 뷰에 포함하면 좋습니다.

#### 비밀번호 확인 처리

다음으로, 비밀번호 확인 폼으로부터 요청을 처리할 라우트를 정의합니다. 이 라우트는 비밀번호를 검증하고 사용자를 의도한 위치로 리다이렉트합니다:

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

이 라우트에서 우선 요청된 `password` 값이 인증 사용자의 비밀번호와 일치하는지 확인합니다. 비밀번호가 유효하다면, Laravel 세션에 사용자가 비밀번호를 확인했다는 정보를 기록해야 합니다. `passwordConfirmed` 메서드는 사용자의 세션에 타임스탬프를 저장하여, 나중에 Laravel이 마지막 비밀번호 확인 시점을 알 수 있게 해줍니다. 마지막으로, 사용자를 의도한 위치로 리다이렉트합니다.

### 라우트 보호 (Protecting Routes)

비밀번호 최근 확인이 필요한 작업을 처리하는 라우트에는 반드시 `password.confirm` 미들웨어를 지정해야 합니다. 이 미들웨어는 Laravel 기본 설치 시 포함되어 있으며, 사용자가 비밀번호를 확인하지 않았다면 현재 요청 위치를 세션에 저장한 뒤 자동으로 `password.confirm` [이름 지정 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다:

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 사용자 정의 가드 추가 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 이용해, 자신만의 인증 가드를 정의할 수 있습니다. `extend` 메서드는 [서비스 프로바이더](/docs/12.x/providers) 내에서 호출하는 것이 좋습니다. Laravel에는 이미 기본적으로 `AppServiceProvider`가 있으니, 해당 프로바이더에 코드를 추가하면 됩니다:

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

위 예시처럼, `extend` 메서드에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 이 인터페이스에 정의된 몇 가지 메서드를 직접 구현해야 커스텀 가드로 사용할 수 있습니다. 커스텀 가드를 정의한 후, `auth.php` 설정 파일의 `guards` 섹션에서 해당 가드를 참조할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

### 클로저 요청 가드 (Closure Request Guards)

HTTP 요청 기반의 커스텀 인증 시스템을 가장 손쉽게 구현하는 방법은 `Auth::viaRequest` 메서드를 이용하는 것입니다. 이 메서드를 이용하면 하나의 클로저로 인증 과정을 간결하게 정의할 수 있습니다.

시작하려면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 `Auth::viaRequest`를 호출합니다. 첫 번째 인자로 인증 드라이버의 이름을 지정하며(아무 문자열이나 가능), 두 번째 인자로는 들어오는 HTTP 요청을 받아 사용자 인스턴스를 반환하거나 인증 실패 시 `null`을 반환하는 클로저를 지정합니다:

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

이제 `auth.php` 설정 파일의 `guards` 섹션에서 위에서 정의한 커스텀 드라이버를 사용하도록 지정할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이후, 인증 미들웨어를 라우트에 할당할 때 해당 가드를 참조하면 됩니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 사용자 정의 사용자 제공자 추가 (Adding Custom User Providers)

전통적인 관계형 데이터베이스가 아닌 곳에 사용자를 저장하는 경우, 자체 인증 사용자 제공자를 확장해야 할 수 있습니다. 이때 `Auth` 파사드의 `provider` 메서드를 사용하여 커스텀 사용자 제공자를 정의할 수 있습니다. 제공자 리졸버는 `Illuminate\Contracts\Auth\UserProvider` 구현체를 반환해야 합니다:

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

이렇게 `provider` 메서드로 제공자를 등록한 후, `auth.php` 설정 파일에서 새로운 드라이버를 사용하는 `provider`를 정의하면 됩니다:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로, 이 제공자를 `guards` 설정에서 참조할 수 있습니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

### User Provider 계약 (The User Provider Contract)

`Illuminate\Contracts\Auth\UserProvider` 구현체는 영구 저장소(MySQL, MongoDB 등)로부터 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 조회하는 역할을 합니다. 이 두 인터페이스 덕분에, 사용자 데이터 저장 방식이나 인증 사용자 클래스를 교체하더라도, Laravel 인증 메커니즘은 문제없이 동작할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약의 구조를 살펴봅시다:

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

- `retrieveById`는 보통 사용자의 primary key(예: MySQL의 오토 인크리먼트 ID 등)를 받아 해당 사용자를 조회하고 반환합니다.
- `retrieveByToken`은 고유 `$identifier`와 "remember me" `$token`(보통 데이터베이스의 `remember_token` 컬럼)에 근거하여 사용자를 조회합니다.
- `updateRememberToken`은 전달된 `$user` 인스턴스의 `remember_token`을 새로운 `$token` 값으로 업데이트합니다. 이 메서드는 주로 "로그인 상태 유지" 인증 성공 혹은 로그아웃 시 사용됩니다.
- `retrieveByCredentials`는 인증 시도 시 `Auth::attempt`에 전달되는 자격 증명 배열을 받아, 해당 조건의 사용자를 영구 저장소에서 조회합니다. 보통 "where" 조건으로 username과 일치하는 사용자를 찾고, `Authenticatable` 구현체를 반환합니다. **이 메서드는 비밀번호 유효성 검증이나 인증을 수행하면 안 됩니다.**
- `validateCredentials`는 주어진 `$user`와 `$credentials`를 비교해 인증 여부를 판단해야 합니다. 예를 들어 `Hash::check`로 `$user->getAuthPassword()`와 `$credentials['password']`를 비교한 결과를 반환할 수 있습니다.
- `rehashPasswordIfRequired`는 필요 시(및 지원 가능한 경우) `$user`의 비밀번호를 재해싱합니다. 예를 들어, `Hash::needsRehash`로 `$credentials['password']`의 재해싱 필요성을 검사하고, 필요하다면 `Hash::make`로 비밀번호를 재해싱해서 사용자의 기록을 업데이트합니다.

### Authenticatable 계약 (The Authenticatable Contract)

이제 `UserProvider`의 각 메서드를 살펴본 김에, `Authenticatable` 계약도 보겠습니다. 사용자 제공자는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`에서 이 인터페이스 구현체를 반환해야 합니다:

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

- `getAuthIdentifierName`은 사용자에 대한 "primary key" 컬럼명을 반환,
- `getAuthIdentifier`는 primary key 값을 반환합니다. 예를 들어 MySQL에서는 오토 인크리먼트된 값입니다.
- `getAuthPasswordName`은 비밀번호 컬럼명을 반환,
- `getAuthPassword`는 해시된 비밀번호 값을 반환합니다.

이 인터페이스 덕분에 어떤 ORM이나 저장소 추상 계층을 사용하든, 인증 시스템은 어떤 "사용자" 클래스와도 연동될 수 있습니다. Laravel은 기본적으로 `app/Models` 디렉터리에 이 인터페이스를 구현하는 `App\Models\User` 클래스를 포함하고 있습니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt 해시의 "work factor"는 애플리케이션의 `config/hashing.php` 설정 파일이나 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

컴퓨터·그래픽카드 처리 성능이 올라감에 따라 bcrypt work factor도 점진적으로 높여야 합니다. work factor를 높이면, 사용자 인증(예: 스타터 킷이나 [수동 인증](#authenticating-users)로 `attempt` 메서드 호출 시) 시 Laravel이 알아서 비밀번호를 부드럽게 자동 재해싱해줍니다.

자동 재해싱은 일반적으로 애플리케이션에 영향을 주지 않지만, 이 동작을 중단하고 싶다면 `hashing` 구성 파일을 퍼블리시해서 쓸 수 있습니다:

```shell
php artisan config:publish hashing
```

설정 파일을 퍼블리시한 후, `rehash_on_login` 값을 `false`로 지정하면 됩니다:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 발행합니다. 다음 이벤트 중 어느 것에도 [리스너를 정의](/docs/12.x/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                         |
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
