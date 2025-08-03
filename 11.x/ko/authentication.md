# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 킷](#starter-kits)
    - [데이터베이스 고려 사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 킷 설치](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 제한 (Throttle)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증 (Basic Authentication)](#http-basic-authentication)
    - [상태 비저장 HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가](#adding-custom-user-providers)
    - [사용자 프로바이더 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/11.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션들은 사용자들이 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 이 기능 구현은 복잡하고 위험할 수 있기 때문에, Laravel은 빠르고 안전하며 쉽게 인증 기능을 구현할 수 있는 도구를 제공하는 데 중점을 둡니다.

Laravel 인증 시스템의 핵심은 "가드(guards)"와 "프로바이더(providers)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자가 어떻게 인증되는지를 정의합니다. 예를 들어, Laravel은 세션 스토리지와 쿠키를 사용하여 상태를 유지하는 `session` 가드를 기본 제공하여 배포합니다.

프로바이더는 사용자를 어떻게 지속 저장소에서 가져올지를 정의합니다. Laravel은 [Eloquent](/docs/11.x/eloquent) 및 데이터베이스 쿼리 빌더를 이용해 사용자를 조회하는 기능을 기본 제공합니다. 하지만 필요한 경우 애플리케이션 요구에 맞게 추가 프로바이더를 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치하며, Laravel 인증 서비스 동작을 세밀하게 조정할 수 있는 여러 옵션들이 자세히 문서화되어 있습니다.

> [!NOTE]  
> 가드와 프로바이더는 "역할(roles)"이나 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통한 사용자의 행동 인가에 대해 자세히 알고 싶으면 [authorization](/docs/11.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 킷 (Starter Kits)

빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 설치하세요. 데이터베이스 마이그레이션을 마친 후, `/register` 등 애플리케이션에 할당된 URL로 접속하면 스타터 킷이 인증 시스템 전체를 기본 구성해줍니다!

**최종 애플리케이션에 스타터 킷을 사용하지 않더라도, [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze)를 설치해 보면 실제 Laravel 프로젝트에서 인증 기능을 어떻게 구현하는지 배우는 좋은 기회가 될 수 있습니다.** Laravel Breeze는 인증용 컨트롤러, 라우트, 뷰를 생성해 주므로, 해당 파일의 코드를 살펴보며 Laravel 인증 기능 구현 방식을 학습할 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려 사항 (Database Considerations)

기본적으로 Laravel은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/11.x/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용됩니다.

Eloquent를 사용하지 않는 애플리케이션이라면 Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우, 공식 MongoDB [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델의 데이터베이스 스키마를 설계할 때는 `password` 컬럼이 최소 60자 이상 되어야 합니다. 물론, 새로운 Laravel 애플리케이션의 `users` 테이블 마이그레이션은 이미 이를 만족하는 컬럼을 생성합니다.

또한 `users`(또는 동등한) 테이블에 100자 길이의 nullable 문자열 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 로그인 시 "remember me" 옵션을 선택한 사용자 토큰 저장에 사용되며, 기본 `users` 테이블 마이그레이션에 이미 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증 관련 패키지를 여러 개 제공합니다. 계속하기 전에 Laravel의 인증 에코시스템을 살펴보고 각 패키지가 어떤 목적으로 설계되었는지 간략히 설명하겠습니다.

우선, 인증 작동 방식을 생각해 보겠습니다. 웹 브라우저를 사용할 때 사용자는 로그인 폼에서 사용자명과 비밀번호를 입력합니다. 이 자격 증명이 올바르면 애플리케이션은 인증된 사용자의 정보를 [세션](/docs/11.x/session)에 저장합니다. 브라우저에 발급된 쿠키는 세션 ID를 포함해, 이후 애플리케이션에 대한 요청을 올바른 세션과 연결할 수 있도록 돕습니다. 세션 쿠키를 받으면 애플리케이션은 세션 데이터를 조회해 인증 정보를 확인하고, 사용자를 "인증된 상태"로 간주합니다.

원격 서비스가 API에 접근해야 할 경우, 웹 브라우저가 없으므로 쿠키는 인증에 쓰이지 않습니다. 대신 원격 서비스는 매 요청마다 API 토큰을 API에 보내며, 애플리케이션은 유효한 API 토큰 목록과 대조해 그 토큰과 연관된 사용자로 요청을 "인증"합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 내장 브라우저 인증 서비스

Laravel은 일반적으로 `Auth` 및 `Session` 파사드를 통해 접근하는 내장 인증 및 세션 서비스를 제공합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 이 서비스들은 사용자의 자격 증명을 확인하고 인증하는 메서드를 제공하며, 적절한 인증 데이터를 사용자의 세션에 저장하고 세션 쿠키를 발행합니다. 이 문서 내에서 이러한 서비스 사용 방법을 다룹니다.

**애플리케이션 스타터 킷**

직접 인증 서비스를 수동 사용해 자체 인증 레이어를 구축할 수도 있지만, 더 빠르게 시작할 수 있도록 전체 인증 레이어를 견고하고 현대적으로 기본 구성을 제공하는 [무료 패키지](/docs/11.x/starter-kits)를 제공합니다. 이 패키지는 [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/11.x/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/11.x/fortify)입니다.

_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 확인, 비밀번호 확인을 포함한 모든 Laravel 인증 기능의 최소한의 간단 구현입니다. Breeze의 뷰는 [Blade 템플릿](/docs/11.x/blade)로 작성되며 [Tailwind CSS](https://tailwindcss.com)로 스타일링 되어 있습니다. 시작하려면 Laravel [애플리케이션 스타터 킷](/docs/11.x/starter-kits) 문서를 참고하세요.

_Laravel Fortify_는 본 문서에 다뤄진 쿠키 기반 인증뿐 아니라 2단계 인증, 이메일 확인 등 여러 기능을 구현한 헤드리스 인증 백엔드입니다. Fortify는 Laravel Jetstream의 인증 백엔드로 사용되거나, [Laravel Sanctum](/docs/11.x/sanctum)과 조합해 SPA용 인증을 제공할 수도 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_는 Laravel Fortify 인증 서비스를 소비 및 노출하는 강력한 스타터 킷으로, [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), 또는 [Inertia](https://inertiajs.com) 기반의 세련된 UI를 제공합니다. 2단계 인증, 팀 지원, 브라우저 세션 관리, 프로필 관리, [Laravel Sanctum](/docs/11.x/sanctum) API 토큰 인증 연동을 기본 제공합니다. 아래 내용에서 API 인증에 대해서도 설명합니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel API 인증 서비스

Laravel은 API 토큰 관리 및 API 토큰을 통한 인증 요청 관리를 돕는 선택적 패키지 [Passport](/docs/11.x/passport)와 [Sanctum](/docs/11.x/sanctum)를 제공합니다. 이들 라이브러리와 내장 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 주로 API 토큰 인증에 집중하는 반면, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션은 두 가지를 모두 사용합니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"을 제공하는 OAuth2 인증 프로바이더로, 여러 유형의 토큰 발급을 지원합니다. 전반적으로 API 인증용으로 견고하지만 복잡한 패키지입니다. 대부분 애플리케이션은 OAuth2의 복잡한 기능이 필요 없고, OAuth2는 사용자 및 개발자 모두에게 혼란이 될 수 있습니다. SPA나 모바일 앱 인증에 Passport 같은 OAuth2 프로바이더 사용법이 혼동되기도 했습니다.

**Sanctum**

OAuth2의 복잡성과 개발자 혼란에 대응하여, Laravel은 브라우저의 1차 요청과 토큰 기반 API 요청을 모두 쉽게 처리할 수 있는 단순하고 효율적인 인증 패키지 [Laravel Sanctum](/docs/11.x/sanctum)을 만들었습니다. Sanctum 기반 애플리케이션은 요청을 받으면 우선 Laravel 내장 인증 서비스를 호출해 세션 쿠키에 인증된 세션 참조가 있는지 확인합니다. 없다면 API 토큰을 검사해 요청을 토큰으로 인증합니다. 자세한 내용은 Sanctum ["작동 원리"](/docs/11.x/sanctum#how-it-works) 문서를 참고하세요.

Laravel Sanctum은 대부분 애플리케이션 인증 요구에 맞는 최적 솔루션으로, [Laravel Jetstream](https://jetstream.laravel.com) 스타터 킷에 기본 포함되어 제공됩니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

요약하면, 브라우저로 접속하는 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 사용합니다.

API를 타사에 제공한다면 API 토큰 인증을 위해 [Passport](/docs/11.x/passport) 또는 [Sanctum](/docs/11.x/sanctum)를 선택합니다. 보통 API 인증, SPA 인증, 모바일 인증 지원 모두 가능한 간단하고 완전한 Sanctum을 우선 권장합니다.

SPA가 Laravel 백엔드와 함께 동작한다면 [Laravel Sanctum](/docs/11.x/sanctum)을 사용하는 것이 좋습니다. Sanctum 사용 시, [사용자 인증 라우트를 수동 구현](#authenticating-users)하거나, [Laravel Fortify](/docs/11.x/fortify)를 헤드리스 인증 벡엔드로 활용해 회원가입, 비밀번호 재설정, 이메일 확인 등 기능을 제공할 수 있습니다.

OAuth2 스펙에 따른 모든 기능이 절대적으로 필요하면 Passport를 선택하세요.

빠른 시작을 원하면, [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze)를 추천합니다. Breeze는 Laravel 내장 인증 서비스와 Sanctum을 사용하는 권장 인증 스택을 가장 빠르게 시작할 수 있게 돕습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]  
> 이 문서 부분은 UI 스캐폴딩을 포함한 [Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits) 기반 사용자 인증 방법을 다룹니다. Laravel 인증 시스템을 직접 통합하려면 [수동 사용자 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치 (Install a Starter Kit)

먼저 [Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 설치하세요. 현재 Laravel Breeze와 Laravel Jetstream은 새 Laravel 애플리케이션에 인증을 통합할 수 있는 아름답고 잘 설계된 출발점을 제공합니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 확인, 비밀번호 확인 등 Laravel의 모든 인증 기능을 최소한으로 간단히 구현합니다. Breeze 뷰는 [Blade 템플릿](/docs/11.x/blade)로 작성되고 [Tailwind CSS](https://tailwindcss.com)로 스타일링되며, 추가로 [Livewire](https://livewire.laravel.com)나 [Inertia](https://inertiajs.com) 기반 스캐폴딩을 선택할 수 있고, Inertia 기반 시 Vue 또는 React 중 하나를 선택할 수 있습니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 보다 강력한 스타터 킷으로, [Livewire](https://livewire.laravel.com) 또는 [Inertia와 Vue](https://inertiajs.com) 기반 스캐폴딩을 지원합니다. Jetstream은 2단계 인증, 팀 지원, 프로필 관리, 브라우저 세션 관리, API 지원([Laravel Sanctum](/docs/11.x/sanctum)), 계정 삭제 같은 기능을 선택적으로 포함합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기 (Retrieving the Authenticated User)

인증 스타터 킷을 설치하고 사용자가 애플리케이션에 등록 및 인증하도록 만든 후에는, 현재 인증된 사용자와 상호작용할 필요가 자주 생깁니다. 들어오는 요청을 다루는 중이라면 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기...
$user = Auth::user();

// 현재 인증된 사용자 ID 가져오기...
$id = Auth::id();
```

또는, 사용자가 인증된 후에는 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 접근할 수도 있습니다. 컨트롤러 메서드에 타입힌트를 부여하면 해당 클래스가 자동 주입되므로, `Illuminate\Http\Request` 타입힌트만 하면 `user` 메서드를 통해 쉽게 현재 사용자를 가져올 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 비행 정보 업데이트
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

들어오는 HTTP 요청의 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하세요. 사용자가 인증되었으면 `true`를 반환합니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있음...
}
```

> [!NOTE]  
> `check` 메서드로 인증 여부를 확인할 수 있지만, 일반적으로 특정 라우트/컨트롤러에 대한 접근을 인증된 사용자로 제한할 때는 미들웨어를 사용합니다. 자세한 내용은 [라우트 보호](/docs/11.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/11.x/middleware)를 사용해 인증된 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. Laravel은 `auth` 미들웨어를 기본 제공하며, 이는 내부적으로 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 [미들웨어 별칭](/docs/11.x/middleware#middleware-aliases)입니다. 미들웨어는 라우트 정의에 간단히 붙이면 됩니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어가 인증되지 않은 사용자를 발견하면, 해당 사용자를 `login` [이름 있는 라우트](/docs/11.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드를 통해 수정할 수 있습니다:

```
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 또는 클로저 사용
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 붙일 때 어떤 "가드"를 사용할지도 지정할 수 있습니다. 지정하는 가드 명칭은 `auth.php` 설정 파일의 `guards` 배열 내 키 중 하나여야 합니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

Laravel Breeze 또는 Laravel Jetstream [스타터 킷](/docs/11.x/starter-kits)을 사용하는 경우, 로그인 시도에 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본값으로 사용자가 여러 번 인증에 실패하면 1분 동안 로그인할 수 없습니다. 제한은 사용자명/이메일과 IP 주소 조합에 대해 고유하게 적용됩니다.

> [!NOTE]  
> 애플리케이션 내 다른 라우트에 속도 제한을 적용하려면 [속도 제한 문서](/docs/11.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

Laravel의 [애플리케이션 스타터 킷](/docs/11.x/starter-kits)에 포함된 인증 스캐폴딩을 꼭 사용할 필요는 없습니다. 스캐폴딩을 사용하지 않는다면, Laravel 인증 클래스를 직접 이용해 사용자 인증을 관리해야 합니다. 걱정하지 마세요, 어렵지 않습니다!

우리는 `Auth` [파사드](/docs/11.x/facades)를 사용해 인증 서비스를 호출합니다. 먼저 클래스 상단에 `Auth` 파사드를 임포트하세요. 그다음 `attempt` 메서드를 살펴봅시다. `attempt` 메서드는 기본적으로 애플리케이션 "로그인" 폼의 인증 시도를 처리하며, 인증이 성공하면 [세션](/docs/11.x/session)을 재생성하여 [세션 고정(Session Fixation)](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

```
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
            'email' => '제공된 자격증명이 기록과 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 키/값 쌍 배열을 첫 번째 인수로 받으며, 이 배열 값으로 데이터베이스에서 사용자를 찾습니다. 위 예제에서는 `email` 컬럼 값으로 사용자를 조회합니다. 사용자를 찾으면, 데이터베이스에 저장된 해시된 비밀번호와 입력받은 `password` 값을 비교합니다. 요청된 `password`를 직접 해시하지 말아야 하는데, Laravel 자체에서 비교를 위해 자동으로 해싱 처리를 하기 때문입니다. 두 해시된 비밀번호가 일치하면 인증 세션이 시작됩니다.

기억하세요, Laravel 인증 서비스는 인증 가드의 "프로바이더" 설정에 따라 데이터베이스에서 사용자를 찾아옵니다. 기본 `config/auth.php`에는 Eloquent 사용자 프로바이더가 설정되어 있고 `App\Models\User` 모델을 사용하는 것으로 되어 있습니다. 애플리케이션 요구에 따라 설정 파일을 수정할 수 있습니다.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

Laravel 리다이렉터에 포함된 `intended` 메서드는 사용자가 인증 미들웨어에 가로막히기 전 접근하고자 했던 URL로 리다이렉트합니다. 접근이 불가하면 대체 경로를 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

원한다면 사용자의 이메일과 비밀번호 외에 조건을 추가할 수도 있습니다. `attempt`에 전달하는 배열에 조건을 더 추가하면 됩니다. 예를 들어 사용자가 "active" 상태인지도 체크할 수 있습니다:

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

복잡한 쿼리 조건이 필요하면 배열에 클로저를 추가할 수도 있습니다. 쿼리 인스턴스가 인자로 들어오므로 커스텀 쿼리를 작성할 수 있습니다:

```
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
> 위 예제에서 `email`은 필수 옵션이 아니며 단지 예제로 사용한 컬럼명일 뿐입니다. 실제 데이터베이스에서 "사용자명"에 해당하는 컬럼명을 사용하세요.

`attemptWhen` 메서드는 두 번째 인수로 클로저를 받아서, 인증 직전 추가 사용자 검사를 수행합니다. 클로저는 사용자 인스턴스를 인자로 받고 `true` 또는 `false`를 반환해 인증 가능 여부를 결정합니다:

```
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

`Auth` 파사드의 `guard` 메서드로 어떤 가드 인스턴스를 사용할지 지정할 수도 있습니다. 이 기능으로 완전히 별개의 인증 가능한 모델이나 사용자 테이블로 애플리케이션 내 여러 부분을 독립적으로 인증 관리할 수 있습니다.

`guard` 메서드 인자는 `auth.php` 설정 파일 내 `guards` 배열 키에 대응되어야 합니다:

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹사이트 로그인 폼에 'remember me' 체크박스가 있습니다. 애플리케이션에서 "remember me" 기능을 제공하려면 `attempt` 메서드의 두 번째 인수에 불리언 값을 전달하면 됩니다.

이 값이 `true`일 경우, Laravel은 사용자가 직접 로그아웃할 때까지 또는 무기한으로 인증 상태를 유지합니다. `users` 테이블에 `remember_token` 문자열 컬럼이 있어야 합니다. 새로운 Laravel 애플리케이션의 기본 `users` 마이그레이션에 이미 이 컬럼이 있습니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억됨...
}
```

"remember me" 기능을 제공한다면, 현재 인증된 사용자가 remember me 쿠키로 인증되었는지 `viaRemember` 메서드로 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스로 인증하기

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 설정하려면 `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 넘기세요. 이 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/11.x/contracts)을 구현해야 합니다. Laravel 기본의 `App\Models\User` 모델이 이미 이 인터페이스를 구현합니다. 이 방식은 예를 들어 사용자가 회원가입 직후처럼 이미 유효한 사용자 인스턴스를 갖고 있을 때 유용합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드 두 번째 인수로 불리언 값을 전달할 수 있는데, 이 값은 인증 세션에 대해 "remember me" 기능을 원하는지 나타냅니다. 이 경우 사용자는 수동 로그아웃 전까지 무기한 인증된 상태가 유지됩니다:

```
Auth::login($user, $remember = true);
```

필요하면 가드를 지정해서 `login` 메서드를 호출할 수도 있습니다:

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증하기

사용자 데이터베이스 기본키로 인증하려면 `loginUsingId` 메서드를 사용하세요. 인증하려는 사용자의 기본키를 전달합니다:

```
Auth::loginUsingId(1);
```

두 번째 인자로 `remember` 불리언 값을 줄 수 있습니다:

```
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 1회 인증 (Authenticate a User Once)

`once` 메서드는 애플리케이션에 대해 단발성 인증을 수행하며, 호출 시 세션이나 쿠키를 사용하지 않습니다:

```
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)은 전용 로그인 페이지 없이 빠르게 사용자 인증을 하는 방법입니다. 시작하려면 라우트에 `auth.basic` [미들웨어](/docs/11.x/middleware)를 붙이세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 기본 내장되어 있으므로 직접 정의할 필요가 없습니다:

```
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth.basic');
```

이 미들웨어가 라우트에 붙으면, 브라우저에서 해당 경로에 접속할 때 자동으로 로그인 정보 입력을 요청합니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자명으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고

PHP FastCGI와 Apache로 Laravel 애플리케이션을 제공하는 경우, HTTP 기본 인증이 제대로 작동하지 않을 수 있습니다. 이를 고치려면 애플리케이션의 `.htaccess` 파일에 다음 라인을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 상태 비저장 HTTP 기본 인증 (Stateless HTTP Basic Authentication)

HTTP 기본 인증을 하되 세션에 사용자 식별 쿠키를 설정하지 않고 사용 가능하며, 이는 주로 API 인증에 유용합니다. 이때는 `onceBasic` 메서드를 호출하는 미들웨어를 정의합니다. `onceBasic`에서 응답을 반환하지 않으면 요청은 애플리케이션 내 다음 단계로 전달됩니다:

```
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

다음으로 이 미들웨어를 라우트에 붙이면 됩니다:

```
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

애플리케이션에서 사용자를 수동으로 로그아웃하려면 `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 사용자 세션에서 인증 정보를 제거해 이후 요청이 인증되지 않도록 합니다.

`logout` 호출 외에도 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/11.x/csrf)도 재생성하는 것이 권장됩니다. 일반적으로 로그아웃 후에는 애플리케이션 루트로 리다이렉트합니다:

```
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션에서 사용자를 로그아웃 처리합니다.
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

Laravel은 현재 기기 세션은 유지하면서 다른 기기에서 활성화된 사용자의 세션을 무효화하고 로그아웃시키는 기능도 제공합니다. 이 기능은 사용자가 비밀번호를 변경/갱신할 때 주로 사용합니다.

준비 단계로, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 받는 라우트에 포함되어 있어야 합니다. 보통 라우트 그룹에 적용하며, 기본적으로는 `auth.session` [미들웨어 별칭](/docs/11.x/middleware#middleware-aliases)을 붙이는 방식입니다:

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용합니다. 이 메서드는 사용자가 현재 비밀번호를 입력해 확인하는 것을 요구하며, 애플리케이션이 이를 입력받아야 합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 호출되면, 사용자의 다른 모든 세션이 완전히 무효화되고 이전에 인증받은 모든 가드에서 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 구축하다 보면 중요한 작업 수행 전이나 민감한 영역 진입 전 사용자가 비밀번호를 다시 한 번 확인하도록 요구할 때가 있습니다. Laravel은 이를 쉽게 구현할 수 있는 미들웨어를 내장하고 있습니다. 이 기능 구현 시 두 개의 라우트를 정의해야 하는데, 비밀번호 확인 폼을 보여주는 라우트와 비밀번호 검증 후 사용자를 의도한 목적지로 리다이렉트 해주는 라우트입니다.

> [!NOTE]  
> 아래 설명은 Laravel 비밀번호 확인 기능을 직접 사용하는 방법을 다루지만, 빠른 시작을 원한다면 [Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits)이 이 기능을 기본 지원합니다.

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

비밀번호를 확인한 후 사용자는 기본적으로 3시간 동안 비밀번호를 다시 확인하지 않아도 됩니다. 재확인까지 시간 간격은 `config/auth.php` 설정 파일의 `password_timeout` 값을 수정해 조절할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

우선 사용자가 비밀번호를 확인하도록 요청하는 뷰를 반환하는 라우트를 정의합니다:

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

뒷단 라우트가 반환하는 뷰에는 `password` 필드를 가진 입력 폼이 있어야 하며, 애플리케이션의 민감 구역으로 진입하므로 비밀번호 확인이 필요하다는 안내 문구를 자유롭게 포함할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, 비밀번호 확인 폼에서 전송된 요청을 처리하는 라우트를 정의합니다. 비밀번호를 검증 후 사용자를 의도한 목적지로 리다이렉트 합니다:

```
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

조금 자세히 보면, 먼저 요청의 `password` 값이 인증된 사용자 비밀번호와 실제 일치하는지 확인합니다. 맞으면 Laravel 세션에 `passwordConfirmed` 메서드를 통해 비밀번호 확인 시점의 타임스탬프를 저장합니다. 이를 토대로 Laravel은 이후 비밀번호 확인이 필요한지 판단합니다. 마지막으로 사용자를 원래 가려고 했던 경로로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

비밀번호를 최근에 확인해야만 수행 가능한 작업을 하는 모든 라우트에 `password.confirm` 미들웨어를 반드시 지정하세요. 이 미들웨어는 기본 Laravel 설치 시 포함되어 있으며, 사용자가 비밀번호 확인 후 원래 가려고 했던 경로를 세션에 저장하고 리다이렉트합니다:

```
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 사용해 자신만의 인증 가드를 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/11.x/providers)에 배치하는 것이 좋으며, Laravel 기본 제공 `AppServiceProvider`에 추가할 수 있습니다:

```
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

위 예제 코드에서 보듯 `extend` 메서드에 넘기는 콜백은 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 하며, 이 인터페이스는 커스텀 가드를 정의할 때 구현해야 할 몇 가지 메서드를 포함합니다. 커스텀 가드 정의 후에는 `auth.php` 설정 파일 `guards` 배열에서 이 가드를 참조할 수 있습니다:

```
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 요청 가드 (Closure Request Guards)

가장 간단한 커스텀 HTTP 요청 기반 인증 시스템 구현 방식은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드는 하나의 클로저로 인증 프로세스를 빠르게 정의할 수 있게 해줍니다.

`AppServiceProvider`의 `boot` 메서드에서 `viaRequest`를 호출하세요. 첫 번째 인수는 커스텀 가드 명칭(임의 문자열), 두 번째 인수는 HTTP 요청을 받아 사용자 인스턴스를 반환하거나 인증 실패 시 `null`을 반환하는 클로저입니다:

```
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

커스텀 인증 드라이버를 정의했으면, `auth.php` 설정 파일의 `guards` 배열에 드라이버로 등록하세요:

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로, 인증 미들웨어 사용 시 가드 명칭을 지정합니다:

```
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가 (Adding Custom User Providers)

전통적인 관계형 데이터베이스를 사용하지 않는 경우, Laravel의 인증 시스템에 자신만의 사용자 프로바이더를 확장해 추가해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 정의하며, 사용자 프로바이더 리졸버는 `Illuminate\Contracts\Auth\UserProvider` 구현체를 반환해야 합니다:

```
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

`provider` 메서드로 프로바이더를 등록하면, `auth.php` 설정에서 이 드라이버를 사용하는 프로바이더로 전환할 수 있습니다:

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로, `guards` 설정에서 이 프로바이더를 참조하세요:

```
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### 사용자 프로바이더 계약 (The User Provider Contract)

`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등 영속 저장소에서 가져오는 역할을 합니다. 이 두 인터페이스 덕분에 사용자 데이터 저장 방식이나 인증 사용자 클래스를 바꿔도, Laravel의 인증 메커니즘은 계속 작동할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약은 다음과 같습니다:

```
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

- `retrieveById` 함수는 일반적으로 MySQL 등에서 사용자 키(예: 자동 증가 ID)를 받아 해당하는 `Authenticatable` 구현체를 조회해 반환합니다.

- `retrieveByToken` 함수는 고유 식별자 `$identifier`와 "remember me" `$token`으로 사용자를 조회합니다. 이 토큰은 보통 `remember_token` 컬럼에 저장됩니다. 역시 일치하는 `Authenticatable` 인스턴스를 반환해야 합니다.

- `updateRememberToken` 메서드는 `$user` 인스턴스의 `remember_token`을 새로운 `$token` 값으로 갱신합니다. "remember me" 인증 성공 시 또는 로그아웃 시 새 토큰이 할당됩니다.

- `retrieveByCredentials` 메서드는 `Auth::attempt` 메서드에 전달된 자격 증명 배열을 받아 이에 해당하는 사용자를 영속 저장소에서 조회합니다. 보통 `$credentials['username']` 값과 일치하는 사용자 레코드를 쿼리합니다. 이 메서드는 사용자 비밀번호 검증이나 인증을 수행하지 않아야 하며, `Authenticatable` 구현체를 반환해야 합니다.

- `validateCredentials` 메서드는 주어진 `$user`와 `$credentials`를 비교해 사용자 인증을 수행합니다. 예를 들어 대부분 `Hash::check` 메서드로 `$user->getAuthPassword()`와 `$credentials['password']`를 비교합니다. 이 메서드는 인증 비밀번호가 맞으면 `true`, 틀리면 `false`를 반환합니다.

- `rehashPasswordIfRequired` 메서드는 주어진 `$user`의 비밀번호를 재해싱해야 할 경우 수행합니다. 주로 `Hash::needsRehash`를 사용해 `$credentials['password']`가 재해싱 대상인지 검사하고, 필요 시 `Hash::make`로 새 해시를 만들어 영속 저장소에 반영합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약 (The Authenticatable Contract)

`UserProvider`에서 반환하는 객체는 아래 `Authenticatable` 계약을 구현해야 합니다. 이 인터페이스를 살펴보면:

```
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

- `getAuthIdentifierName` 메서드는 사용자의 "기본 키" 컬럼명을 반환합니다.
- `getAuthIdentifier`는 사용자의 기본 키 값을 반환합니다 (예: MySQL의 자동 증가 ID).
- `getAuthPasswordName`은 비밀번호 컬럼명을 반환합니다.
- `getAuthPassword`는 사용자의 해시된 비밀번호를 반환합니다.
- `getRememberToken`과 `setRememberToken`은 remember token의 값을 가져오고 설정합니다.
- `getRememberTokenName`은 remember token 컬럼명을 반환합니다.

이 인터페이스 덕분에 어떤 ORM이나 저장소를 사용해도 인증 시스템이 일관되게 작동할 수 있습니다. 기본 Laravel에는 `app/Models/User.php`가 이 인터페이스를 구현해 포함되어 있습니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel 기본 비밀번호 해싱 알고리즘은 bcrypt이며, CPU/GPU 성능이 올라감에 따라 work factor를 조정할 수 있습니다. 이 작업은 `config/hashing.php` 설정 파일이나 `BCRYPT_ROUNDS` 환경 변수로 조절합니다.

보통 bcrypt work factor는 시간이 지남에 따라 점진적으로 증가해야 합니다. work factor를 올리면, Laravel은 사용자가 로그인할 때 자동으로 비밀번호를 재해싱하여 데이터베이스에 저장합니다.

대부분 상황에서 자동 재해싱은 애플리케이션에 문제를 일으키지 않지만, 원한다면 `hashing` 설정 파일을 퍼블리시한 후 설정을 꺼둘 수 있습니다:

```shell
php artisan config:publish hashing
```

퍼블리시 후, `rehash_on_login` 값을 `false`로 설정하세요:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정에서 다양한 [이벤트](/docs/11.x/events)를 발생시킵니다. 다음 이벤트에 대해 [리스너](/docs/11.x/events)를 정의할 수 있습니다:

<div class="overflow-auto">

| 이벤트명 |
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