# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 퀵스타트](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [다른 인증 방식](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [Stateless HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기에서 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우트 설정](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 패스워드 리해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

대부분의 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 방법을 제공합니다. 이러한 기능을 웹 애플리케이션에 구현하는 것은 꽤 복잡할 수 있으며, 보안적으로도 많은 위험이 따릅니다. 라라벨은 이러한 인증 기능을 빠르고, 안전하며, 손쉽게 구현할 수 있는 다양한 도구들을 제공합니다.

라라벨의 인증 시스템의 핵심은 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각각의 요청에서 사용자가 어떻게 인증되는지를 정의합니다. 예를 들어, 라라벨은 세션 저장소와 쿠키를 사용하여 상태를 유지하는 `session` 가드를 기본으로 제공합니다.

프로바이더는 사용자를 영구 스토리지(데이터베이스 등)에서 어떻게 조회하는지를 정의합니다. 라라벨은 [Eloquent](/docs/12.x/eloquent) 및 데이터베이스 쿼리 빌더를 통한 사용자 조회를 기본으로 지원합니다. 필요에 따라 추가적인 프로바이더를 자유롭게 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 라라벨 인증 서비스의 동작을 세밀하게 제어할 수 있는 다양한 옵션이 잘 정리되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(role)"과 "권한(permission)"과 혼동해서는 안됩니다. 권한을 통한 사용자 액션 인가에 대해 더 알고 싶다면 [인가(authorization)](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶으신가요? 신규 라라벨 애플리케이션에 [라라벨 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치해 보세요. 데이터베이스 마이그레이션을 마친 후, `/register` 또는 애플리케이션에 할당된 아무 URL에 접속하면, 스타터 키트가 인증 시스템 전체의 스캐폴딩을 자동으로 처리해줍니다!

**최종적으로 라라벨 애플리케이션에서 스타터 키트를 사용하지 않을 계획이라도, [스타터 키트](/docs/12.x/starter-kits)를 설치해 보는 것은 라라벨의 인증 기능이 실제 프로젝트에서 어떻게 구현되어 있는지 배울 수 있는 훌륭한 기회가 될 수 있습니다.** 스타터 키트에는 인증 컨트롤러, 라우트, 뷰가 모두 포함되어 있으므로, 파일 내부의 코드를 직접 살펴보며 라라벨 인증의 실제 구현 방법을 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

라라벨은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

만약 애플리케이션에서 Eloquent를 사용하지 않는다면, 라라벨 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 활용할 수 있습니다. 애플리케이션에서 MongoDB를 사용하는 경우에는 MongoDB 공식 [라라벨 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 확인하세요.

`App\Models\User` 모델을 위한 데이터베이스 스키마를 만들 때, 패스워드 컬럼의 길이가 최소 60자 이상이 되도록 설정해야 합니다. 참고로, 신규 라라벨 애플리케이션에 기본 포함된 `users` 테이블 마이그레이션은 이미 이보다 더 긴 컬럼을 생성합니다.

또한, `users`(또는 동등한) 테이블에 100자 길이의 nullable 문자열형 `remember_token` 컬럼이 포함되어 있는지 반드시 확인하세요. 이 컬럼은 사용자가 로그인 시 "로그인 유지(remember me)" 옵션을 선택했을 때 토큰을 저장하는 데 사용됩니다. 역시, 라라벨의 기본 `users` 테이블 마이그레이션에는 이 컬럼이 이미 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

라라벨은 인증과 관련된 여러 패키지를 제공합니다. 본격적으로 설명에 들어가기 전에, 라라벨 인증 에코시스템의 전체적인 흐름과 각 패키지의 용도에 대해 간략히 살펴보겠습니다.

먼저, 인증이 어떻게 동작하는지 생각해봅시다. 웹 브라우저 환경에서는 사용자가 로그인 폼에 아이디와 패스워드를 입력합니다. 인증 정보가 올바르다면, 애플리케이션은 해당 사용자의 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저로 전송되는 쿠키에는 세션 ID가 포함되어 있어, 이후 요청마다 이 세션 ID를 통해 사용자와 올바른 세션을 연결할 수 있게 됩니다. 세션 쿠키가 전달되면, 애플리케이션은 세션 ID로 세션 데이터를 조회하고, 세션에 인증 정보가 있음을 확인한 후 사용자를 "인증된 사용자"로 간주합니다.

반면, 원격 서비스에서 API 접근을 위해 인증이 필요한 경우에는, 브라우저가 아니므로 쿠키가 잘 사용되지 않습니다. 이런 경우, 원격 서비스는 요청마다 API 토큰을 API로 전송합니다. 애플리케이션은 이 토큰이 유효한지 데이터베이스의 토큰 테이블과 비교하여, 해당 API 토큰에 연결된 사용자를 "인증된 사용자"로 처리합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### 라라벨의 기본 브라우저 인증 서비스

라라벨은 기본적인 인증 및 세션 서비스를 제공하며, 일반적으로 `Auth`와 `Session` 파사드를 통해 접근할 수 있습니다. 이 기능들은 웹 브라우저에서 시작되는 요청에 대해 쿠키 기반 인증을 제공합니다. 다양한 메서드를 이용해 사용자의 자격증명을 검증하고 인증할 수 있습니다. 추가로, 인증에 필요한 모든 데이터를 자동으로 세션에 저장하고 세션 쿠키도 발급해줍니다. 이 서비스들을 사용하는 방법은 본 문서에서 자세히 다루고 있습니다.

**애플리케이션 스타터 키트**

이 문서에 설명된 대로, 이러한 인증 서비스를 수동으로 활용해 직접 인증 레이어를 구현할 수도 있습니다. 하지만 더 빠른 시작을 원한다면, [무료 스타터 키트](/docs/12.x/starter-kits)를 사용하면 강력하고 현대적인 인증 스캐폴딩이 포함된 프로젝트를 빠르게 만들 수 있습니다.

<a name="laravels-api-authentication-services"></a>
#### 라라벨의 API 인증 서비스

라라벨은 API 토큰을 관리하고 토큰으로 인증된 요청을 처리할 수 있도록 두 가지 선택적 패키지, [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 라이브러리들과 라라벨의 기본 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 즉, 이 패키지들은 주로 API 토큰 인증에 집중되어 있으며, 기본 인증 서비스는 브라우저 쿠키 기반 인증에 초점을 맞춥니다. 실제로 많은 애플리케이션이 기본 쿠키 기반 인증 서비스와 API 인증 패키지 중 하나를 동시에 활용합니다.

**Passport**

Passport는 OAuth2 인증 제공자로, 다양한 OAuth2 "grant type"을 지원하여 여러 종류의 토큰 발급이 가능합니다. 즉, API 인증에 대해 robust(강력하고 복잡한) 지원을 제공합니다. 다만, 대부분의 애플리케이션은 OAuth2 명세가 제공하는 복잡한 기능까지 필요로 하진 않으며, 실제 사용자와 개발자 모두에게 헷갈림을 줄 수 있습니다. 특히, SPA, 모바일 앱을 OAuth2 인증 패키지로 처리하는 방법에서 혼란이 있었습니다.

**Sanctum**

OAuth2의 복잡함과 개발자 혼란에 대응하기 위해, 우리는 웹 브라우저의 1차 요청과 토큰을 이용한 API 요청을 모두 손쉽게 처리할 수 있는 더 간단하고 직관적인 인증 패키지를 개발하게 되었습니다. 그 결과물인 [Laravel Sanctum](/docs/12.x/sanctum)은 API와 웹 UI, 그리고 백엔드 라라벨 애플리케이션과 분리된 SPA(싱글 페이지 애플리케이션), 탐 모바일 클라이언트까지 모두 지원하는 권장 인증 패키지입니다.

라라벨 Sanctum은 웹/ API 인증을 모두 아우르며, 애플리케이션 인증 전체를 통합 관리할 수 있습니다. 작동 원리는, 요청이 들어오면 먼저 세션 쿠키가 존재하는지 확인하여 인증 여부를 파악하고, (즉, 앞서 설명한 기본 인증 서비스를 활용합니다) 만약 쿠키가 없다면 API 토큰을 체크해 토큰으로 인증을 수행합니다. 보다 자세한 과정은 Sanctum의 ["작동 방식"](/docs/12.x/sanctum#how-it-works) 문서를 참고해 주세요.

<a name="summary-choosing-your-stack"></a>
#### 요약과 인증 스택 선택

요약하자면, 브라우저를 통해 접근하고 모놀리식(monoithic) 라라벨 애플리케이션을 구축하는 경우, 라라벨의 기본 인증 서비스를 사용하면 됩니다.

다음으로, 서드파티에서 소비할 API를 제공하는 경우에는 [Passport](/docs/12.x/passport) 혹은 [Sanctum](/docs/12.x/sanctum) 중에서 선택해 API 토큰 인증 기능을 추가할 수 있습니다. 일반적으로, Simple하고 완결된 솔루션이 필요한 경우에는 Sanctum이 권장됩니다. Sanctum은 API 인증뿐 아니라 SPA, 모바일 인증도 지원하며 "scope"(권한 범위), "ability"(능력) 등도 함께 제공합니다.

SPA(싱글 페이지 애플리케이션)에 라라벨 백엔드를 사용하는 경우에는 [Laravel Sanctum](/docs/12.x/sanctum)을 이용하는 것이 가장 좋습니다. Sanctum을 사용할 때는 [직접 인증 라우트를 구현](#authenticating-users)하거나, 회원가입, 비밀번호 재설정, 이메일 인증 등 관련 기능의 라우트/컨트롤러를 제공하는 [Laravel Fortify](/docs/12.x/fortify)를 headless 인증 백엔드로 활용할 수 있습니다.

OAuth2 명세에서 제공하는 모든 기능이 반드시 필요한 경우에만 Passport를 선택하면 됩니다.

그리고, 빠르게 시작하고 싶다면, [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하면 라라벨의 기본 인증 스택이 미리 탑재된 프로젝트를 바로 시작하실 수 있습니다.

<a name="authentication-quickstart"></a>
## 인증 퀵스타트

> [!WARNING]
> 이 절에서는 빠른 시작을 위해 UI 스캐폴딩이 포함된 [라라벨 애플리케이션 스타터 키트](/docs/12.x/starter-kits) 기반의 인증을 안내합니다. 만약 라라벨의 인증 기능을 직접 활용해 통합하고 싶다면, [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [라라벨 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 스타터 키트는 인증이 필요한 신규 프로젝트에 아름답고 잘 디자인된 시작점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 키트로 애플리케이션을 생성한 뒤, 사용자가 회원 가입 및 인증을 완료하면, 인증된 현재 사용자 정보를 조회해야 하는 경우가 많습니다. 들어오는 요청을 처리하는 과정에서 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자를 조회할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회...
$user = Auth::user();

// 현재 인증된 사용자의 ID 조회...
$id = Auth::id();
```

또한, 이미 인증된 사용자라면, `Illuminate\Http\Request` 인스턴스에서도 인증된 사용자를 불러올 수 있습니다. 클래스 타입 힌트를 활용하면 컨트롤러 메서드에 자동으로 객체가 주입되므로, 어디서든 `request`의 `user` 메서드로 인증된 사용자 정보를 손쉽게 이용할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 비행편 정보 업데이트.
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

들어오는 HTTP 요청을 작성한 사용자가 인증되어 있는지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증된 상태라면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인 상태입니다...
}
```

> [!NOTE]
> `check` 메서드로도 사용자의 인증 여부를 확인할 수 있지만, 대부분의 경우 특정 라우트 또는 컨트롤러에 접근하기 전에 미들웨어로 인증된 사용자임을 검증하는 방법을 사용합니다. 보다 자세한 내용은 [라우트 보호하기](/docs/12.x/authentication#protecting-routes)를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/12.x/middleware)를 사용하여, 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. 라라벨은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)인 `auth`로 등록하고 있으므로, 이 미들웨어를 라우트에 바로 적용할 수 있습니다.

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능합니다...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 미인증 사용자 리다이렉트

`auth` 미들웨어가 미인증 사용자를 감지하면, 해당 사용자를 `login` [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드를 사용해 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저 사용 예시...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증 사용자 리다이렉트

`guest` 미들웨어가 인증된 사용자를 감지하면, 사용자에게 `dashboard` 또는 `home` 네임드 라우트로 리다이렉트합니다. 이 동작 또한 `redirectUsersTo` 메서드로 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저 사용 예시...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### Guard 지정하기

`auth` 미들웨어를 라우트에 적용할 때, 사용자 인증에 사용할 "가드"를 직접 지정할 수도 있습니다. 지정하는 가드는 `auth.php` 설정 파일 내 `guards` 배열의 키와 일치해야 합니다.

```php
Route::get('/flights', function () {
    // 인증된 admin 가드를 사용하는 사용자만 접근...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하면 로그인 시도에 자동으로 rate limiting(속도 제한)이 적용됩니다. 기본적으로 여러 번 인증 정보 입력에 실패하면, 1분간 로그인이 제한됩니다. 제한은 사용자의 아이디/이메일과 IP 주소마다 고유하게 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에도 rate limit을 적용하고 싶다면 [rate limiting 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증

반드시 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)에서 제공하는 인증 스캐폴딩을 사용할 필요는 없습니다. 직접 라라벨 인증 클래스를 이용해 사용자 인증을 제어할 수도 있으니 걱정하지 마세요!

라라벨의 인증 서비스에는 `Auth` [파사드](/docs/12.x/facades)를 주로 사용하므로, 클래스 상단에 `Auth` 파사드를 임포트해야 합니다. 이제 `attempt` 메서드를 살펴보겠습니다. `attempt` 메서드는 일반적으로 애플리케이션의 "로그인" 폼에서 인증을 처리할 때 사용합니다. 인증에 성공했다면 [세션](/docs/12.x/session)을 재생성(regenerate)하여 [세션 고정 공격](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%85%98_%EA%B3%A0%EC%A0%95_%EA%B3%B5%EA%B2%A9)을 방지해야 합니다.

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

`attempt` 메서드는 첫 번째 인자로 key/value 쌍의 배열을 받습니다. 이 배열의 값들은 데이터베이스에서 사용자를 찾는 데 사용되며, 위 예시에서는 `email` 컬럼 값으로 사용자를 찾게 됩니다. 사용자를 찾으면, DB에 저장된 해시된 비밀번호와 입력받은 `password` 값이 서로 일치하는지 비교합니다. 입력받은 `password`를 직접 해시하지 않아도 되며, 프레임워크가 자동으로 해시를 적용해 비교합니다. 두 비밀번호가 일치하면 해당 사용자의 인증 세션이 시작됩니다.

라라벨 인증 서비스는 가드의 "프로바이더" 설정에 따라 사용자 조회 방법을 결정합니다. 기본적으로 `config/auth.php`에는 Eloquent 사용자 프로바이더가 설정되어 있고, 사용자 조회에 `App\Models\User` 모델을 활용하도록 지정되어 있습니다. 애플리케이션 상황에 따라 설정 파일에서 이 값을 자유롭게 변경할 수 있습니다.

`attempt` 메서드는 인증에 성공하면 `true`를, 실패 시에는 `false`를 반환합니다.

라라벨의 redirector에서 제공하는 `intended` 메서드는, 인증 미들웨어에 막히기 전 사용자가 원래 접근하려던 URL로 리다이렉트합니다. 만약 목적지가 명확하지 않으면 대체 URI를 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

필요하다면, 사용자 이메일과 비밀번호 외에 추가 쿼리 조건을 지정해서 인증할 수도 있습니다. 단순히 `attempt` 메서드에 전달하는 배열에 조건을 추가하면 됩니다. 예를 들어, 사용자가 "active" 상태임을 검증할 수 있습니다.

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증에 성공했을 때...
}
```

더 복잡한 쿼리 조건이 필요하다면, 자격증명 배열에 클로저를 추가할 수도 있습니다. 이 클로저는 쿼리 인스턴스를 받고, 애플리케이션 상황에 따라 쿼리를 커스터마이즈할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // 인증에 성공했을 때...
}
```

> [!WARNING]
> 위 예시에서 `email`은 필수값이 아니며, 예제로 사용된 것일 뿐입니다. 예를 들면, 자신의 DB에서 "username" 컬럼을 사용한다면 이에 맞춰 사용하세요.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아, 실제 인증 전에 잠재적 사용자에 대한 추가 검사 로직을 수행할 수 있습니다. 이 클로저는 해당 사용자 인스턴스를 받고, 인증 가능한 경우 `true`, 그렇지 않으면 `false`를 반환해야 합니다.

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // 인증에 성공했을 때...
}
```

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근

`Auth` 파사드의 `guard` 메서드를 활용하면, 인증을 수행할 때 사용할 가드 인스턴스를 직접 지정할 수 있습니다. 이를 통해 각기 다른 인증 모델이나 사용자 테이블을 사용하는 여러 파트를 독립적으로 관리할 수 있습니다.

가드 이름은 `auth.php` 설정 파일에서 정의된 guard 키와 일치해야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

웹 애플리케이션에서는 로그인 폼에 "로그인 유지" 체크박스를 제공하는 경우가 많습니다. 이런 기능을 지원하려면, `attempt` 메서드 두 번째 인자로 불리언 값을 전달하면 됩니다.

이 값이 `true`면, 라라벨은 사용자가 수동으로 로그아웃할 때까지 인증 상태를 유지해 줍니다. 이를 위해 `users` 테이블에 문자열 타입의 `remember_token` 컬럼이 반드시 있어야 하며, 라라벨의 기본 `users` 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 로그인 유지로 인증됨...
}
```

만약 애플리케이션에서 "로그인 유지" 기능을 지원한다면, 현재 인증된 사용자가 해당 쿠키로 인증되었는지 확인할 때 `viaRemember` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 다른 인증 방식

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스로 직접 인증

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 설정해야 한다면, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하면 됩니다. 여기서 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 합니다. 라라벨의 `App\Models\User` 모델은 이미 해당 인터페이스를 구현하고 있습니다. 이 방식은 회원가입 직후처럼 이미 인증된 사용자 인스턴스가 있을 때 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

"로그인 유지" 세션이 필요한 경우, `login` 메서드의 두 번째 인자로 불리언 값을 줄 수 있습니다. 이 값이 `true`면 사용자가 직접 로그아웃할 때까지 인증 상태가 계속 유지됩니다.

```php
Auth::login($user, $remember = true);
```

필요하다면, `login` 호출 전에 인증에 사용할 가드를 직접 지정할 수도 있습니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 직접 인증

사용자의 데이터베이스 기본 키를 통해 인증하려면, `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증할 사용자의 기본 키를 인자로 받습니다.

```php
Auth::loginUsingId(1);
```

"로그인 유지" 기능도 지원하며, 두 번째 인자로 전달할 수 있습니다.

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 1회용 인증

`once` 메서드를 사용하면 세션이나 쿠키를 전혀 사용하지 않고, 한 번의 요청에 한해서만 인증할 수 있습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://ko.wikipedia.org/wiki/%EA%B8%B0%EB%B3%B8_%EC%9D%B8%EC%A6%9D)은 별도의 "로그인" 페이지 없이, 간단하게 사용자를 인증할 수 있는 방법을 제공합니다. 시작하려면, `auth.basic` [미들웨어](/docs/12.x/middleware)를 라우트에 추가하면 됩니다. `auth.basic` 미들웨어는 라라벨 프레임워크에 기본 포함되어 있습니다.

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth.basic');
```

미들웨어가 라우트에 적용되면, 브라우저에서 해당 라우트로 접근할 때 인증 정보를 입력하라는 프롬프트가 자동으로 표시됩니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자의 "username"으로 가정합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI에 대한 참고

라라벨 애플리케이션을 PHP FastCGI와 Apache로 제공하는 경우에는 HTTP Basic 인증이 올바로 동작하지 않을 수 있습니다. 이 문제를 해결하려면, 애플리케이션 루트의 `.htaccess` 파일에 다음 라인을 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP Basic 인증

세션에 사용자 식별자 쿠키를 남기지 않고 HTTP Basic인증을 사용할 수도 있습니다. 주로 API 요청에 HTTP 인증 방식을 적용할 때 유용합니다. 이를 위해 [미들웨어를 정의](/docs/12.x/middleware)하고, 해당 미들웨어에서 `onceBasic` 메서드를 호출하면 됩니다. `onceBasic`이 응답을 반환하지 않으면, 요청은 계속 애플리케이션 안쪽으로 전달됩니다.

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

그 다음, 해당 미들웨어를 라우트에 적용하세요.

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃

사용자를 수동으로 로그아웃 처리하려면, `Auth` 파사드의 `logout` 메서드를 사용하면 됩니다. 이 메서드는 사용자 세션에서 인증 정보를 제거하여, 이후 요청에 더 이상 인증 정보가 남지 않도록 합니다.

logout 호출 후, 세션 무효화 및 [CSRF 토큰](/docs/12.x/csrf) 재생성 또한 권장합니다. 로그아웃 처리 이후에는 대개 애플리케이션의 루트 경로로 리다이렉트합니다.

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

라라벨은 한 사용자의 세션 중, 현재 사용 중인 기기를 제외한 다른 장치에서의 세션을 무효화("로그아웃")하는 기능도 제공합니다. 이 기능은 주로 사용자가 비밀번호를 변경할 때, 다른 기기에서의 로그인 세션을 만료시키고 싶을 때 유용합니다.

시작하기 전에, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 적용할 라우트에 포함되어 있는지 확인하세요. 보통 라우트 그룹에 이 미들웨어를 추가하여 애플리케이션의 대다수 라우트에 일괄 적용할 수 있습니다. 기본적으로 `AuthenticateSession` 미들웨어는 `auth.session` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 적용할 수 있습니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 후, `Auth` 파사드에서 제공하는 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 현재 비밀번호를 다시 입력해야 하며, 애플리케이션에서 해당 값을 입력받아야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 호출되면, 사용자의 다른 기기에서 기존에 인증되었던 모든 세션이 완전히 무효화되어 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하다 보면, 사용자가 민감한 액션을 수행하거나 민감한 영역에 접근하기 전에 비밀번호를 한 번 더 확인하도록 해야 할 때가 있습니다. 라라벨은 이를 자연스럽고 쉽게 구현할 수 있도록 기본 미들웨어를 제공합니다. 이 기능을 구현하려면, 비밀번호 확인 폼을 띄우는 라우트와 비밀번호를 검증해 사용자를 최종 목적지로 리다이렉트하는 라우트, 두 개를 정의해야 합니다.

> [!NOTE]
> 아래 문서는 라라벨의 비밀번호 확인 기능을 직접 통합하는 방법을 안내합니다. 다만, 더 손쉽게 시작하고 싶다면 [라라벨 애플리케이션 스타터 키트](/docs/12.x/starter-kits)에도 이 기능이 이미 내장되어 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호를 확인한 후, 기본적으로 3시간 동안은 다시 비밀번호 확인을 요구하지 않습니다. 하지만, 애플리케이션의 `config/auth.php` 파일 내 `password_timeout` 값을 변경하여 재확인 시간을 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우트 설정

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자의 비밀번호 확인을 요청하는 뷰를 띄울 라우트를 정의합니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

예상하셨겠지만, 이 뷰에는 `password` 필드가 포함된 폼이 있어야 합니다. 또한, 이 영역이 보호된 공간이므로 비밀번호 확인이 필요함을 사용자에게 안내하는 문구를 자유롭게 추가할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 검증

그 다음, "비밀번호 확인" 뷰에서 전송된 폼 데이터를 처리할 라우트를 만듭니다. 이 라우트는 비밀번호를 검증하고, 사용자를 의도한 목적지로 리다이렉트합니다.

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

위 라우트를 더 자세히 살펴보면, 먼저 요청으로 입력된 `password`가 실제 인증된 사용자의 비밀번호와 일치하는지 확인합니다. 비밀번호가 올바르면, 라라벨 세션에 비밀번호 확인 사실을 기록해야 합니다. `passwordConfirmed` 메서드는 사용자의 세션에 시간 정보를 남겨, 라라벨이 마지막으로 비밀번호를 확인한 시점을 기억할 수 있게 합니다. 마지막으로, 사용자를 원래 이동하려던 주소로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

최근 비밀번호 확인이 필요한 라우트에는 반드시 `password.confirm` 미들웨어를 지정해야 합니다. 이 미들웨어는 라라벨 기본 설치에 포함되어 있으며, 사용자가 비밀번호를 확인한 후 원래 접근하려던 위치로 리다이렉트할 수 있도록, 의도한 목적지를 세션에 저장합니다. 목적지가 저장된 후, 미들웨어는 사용자를 `password.confirm` [네임드 라우트](/docs/12.x/routing#named-routes)로 리다이렉트합니다.

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

`Auth` 파사드의 `extend` 메서드를 활용해 나만의 인증 가드를 정의할 수 있습니다. 이 코드는 보통 [서비스 프로바이더](/docs/12.x/providers) 내부에 위치해야 합니다. 라라벨의 `AppServiceProvider`를 활용해 코드를 추가할 수 있습니다.

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
            // Illuminate\Contracts\Auth\Guard 인스턴스를 반환해야 함

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예시처럼 `extend`에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard` 인터페이스의 구현체를 반환해야 합니다. 직접 커스텀 가드를 구현한 후, 이를 `auth.php` 설정 파일의 `guards` 항목에서 참조하면 됩니다.

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

간단한 HTTP 요청 기반의 커스텀 인증 시스템은 `Auth::viaRequest` 메서드를 통해 Closure로 바로 구현할 수 있습니다.

시작하려면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 `viaRequest`를 호출하세요. 첫 번째 인자는 임의의 드라이버 이름이고, 두 번째 인자는 클로저로 해당 인증 과정을 구현합니다. 이 클로저는 들어오는 HTTP 요청을 받아, 인증에 성공하면 사용자 인스턴스를 반환하고 실패하면 `null`을 반환해야 합니다.

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

이렇게 커스텀 인증 드라이버를 정의했다면, `auth.php`의 `guards` 구성에 해당 드라이버명을 지정할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로, 인증 미들웨어를 라우트에 적용할 때 커스텀 가드를 참조하면 됩니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가

전통적인 관계형 데이터베이스가 아닌 곳에 사용자를 저장하는 경우, 라라벨에 직접 사용자 프로바이더를 구현해야 합니다. 이를 위해 `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 사용자 프로바이더를 등록할 수 있습니다. 등록 콜백은 `Illuminate\Contracts\Auth\UserProvider`의 구현체를 반환해야 합니다.

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
            // Illuminate\Contracts\Auth\UserProvider 인스턴스를 반환해야 함

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider` 메서드로 프로바이더를 등록한 뒤, `auth.php` 설정 파일에서 해당 드라이버를 사용하는 provider를 정의합니다.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로, 해당 provider를 `guards` 설정에서 참조할 수 있습니다.

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등의 영구 스토리지 시스템에서 조회하는 역할을 합니다. 이 두 인터페이스를 통해 사용자 데이터 저장 방식이나 인증 사용자 클래스 유형과 관계없이 인증 메커니즘이 일관성 있게 동작할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약의 메서드는 아래와 같습니다.

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

- `retrieveById`: 주로 사용자의 PK(예: auto-increment ID)로 사용자를 조회해서 반환합니다.
- `retrieveByToken`: 고유 `$identifier`와 "로그인 유지" `$token` 값(예: `remember_token` 컬럼)에 해당하는 사용자를 조회해서 반환합니다.
- `updateRememberToken`: 주어진 `$user` 인스턴스의 `remember_token`을 새로운 `$token` 값으로 업데이트합니다. 로그인 유지 인증이나 로그아웃 시 새로운 토큰을 할당합니다.
- `retrieveByCredentials`: `Auth::attempt` 등에서 매개변수로 전달받는 자격증명 배열을 기반으로, 해당하는 사용자를 조회합니다. 주로 `username` 같은 필드로 쿼리하고, 결과로 인증 대상 사용자 인스턴스를 반환해야 하며, **여기서는 비밀번호 검증을 하지 않습니다**.
- `validateCredentials`: 주어진 `$user`와 `$credentials`를 비교해 사용자를 인증할 수 있는지 확인합니다. 보통 `Hash::check`를 이용해서 비밀번호가 맞는지 비교 후, `true`/`false`를 반환합니다.
- `rehashPasswordIfRequired`: 필요 시, 해당 사용자의 비밀번호를 리해시합니다. 예를 들어, `Hash::needsRehash`로 비밀번호가 재해시가 필요한지 판단한 뒤, 필요하면 `Hash::make`로 비밀번호를 재해시하고, 스토리지에 업데이트해야 합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

UserProvider의 각 메서드를 살펴본 뒤, 이제는 `Authenticatable` 계약을 보겠습니다. UserProvider는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`에서 반드시 이 인터페이스의 구현체를 반환해야 합니다.

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

이 인터페이스는 단순합니다.
- `getAuthIdentifierName`: 사용자의 "기본 키" 컬럼명을 반환합니다.
- `getAuthIdentifier`: 사용자의 "기본 키" 값을 반환합니다. (MySQL에서는 자동 증가 PK 등)
- `getAuthPasswordName`: 비밀번호 컬럼명을 반환합니다.
- `getAuthPassword`: 해시된 비밀번호 값을 반환합니다.

이 외에도 `remember_token` 컬럼과 관련된 메서드도 포함되어 있습니다.

이 인터페이스를 통해, 인증 시스템은 어떤 ORM이나 스토리지를 사용하더라도 모든 "사용자" 클래스를 다룰 수 있도록 설계되었습니다. 디폴트로 라라벨에는 `App\Models\User` 클래스가 이 인터페이스를 구현해 제공됩니다.

<a name="automatic-password-rehashing"></a>
## 자동 패스워드 리해싱

라라벨의 기본 비밀번호 해시 알고리즘은 bcrypt입니다. bcrypt 해시의 "work factor"(비용 지수)는 애플리케이션의 `config/hashing.php` 또는 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

보통 CPU/GPU 성능이 향상될수록 bcrypt의 work factor를 점진적으로 올려주는 것이 좋습니다. work factor를 올렸을 때, 라라벨은 사용자가 [시작 키트] 혹은 [수동 인증](#authenticating-users) 중 `attempt` 메서드를 통해 인증하는 시점마다, 필요한 경우 자동으로 비밀번호를 리해싱 처리합니다.

이 자동 패스워드 리해싱은 일반적으로 애플리케이션에 영향을 주지 않지만, 이 기능을 원치 않는 경우에는 아래처럼 설정 파일을 배포 후, 관련 옵션을 꺼둘 수 있습니다.

```shell
php artisan config:publish hashing
```

설정 파일이 배포되면, `rehash_on_login` 값을 `false`로 지정하세요.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트

라라벨은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 디스패치합니다. 다음 이벤트에 대해 [리스너를 정의](/docs/12.x/events)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                   |
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