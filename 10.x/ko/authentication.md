# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 킷](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 킷 설치](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한 (throttling)](#login-throttling)
- [수동으로 사용자 인증하기](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증 (HTTP Basic Authentication)](#http-basic-authentication)
    - [무상태(stateless) HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호하기](#password-confirmation-protecting-routes)
- [커스텀 가드 추가하기](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가하기](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [소셜 인증](/docs/10.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 방법을 제공합니다. 웹 애플리케이션에서 이 기능을 구현하는 것은 복잡하고 때로는 위험할 수 있습니다. 이 때문에 Laravel은 여러분이 빠르고 안전하며 쉽게 인증을 구현할 수 있도록 도구를 제공합니다.

Laravel 인증의 핵심은 "가드(guards)"와 "프로바이더(providers)"로 구성됩니다. 가드는 각 요청이 어떻게 인증되는지 정의합니다. 예를 들어, Laravel은 상태를 세션 저장소와 쿠키를 사용해 유지하는 `session` 가드를 기본 제공합니다.

한편, 프로바이더는 사용자를 영속 저장소에서 어떻게 가져올지를 정의합니다. Laravel은 Eloquent와 데이터베이스 쿼리 빌더를 사용하여 사용자를 조회하는 기능을 기본 제공합니다. 하지만 애플리케이션의 필요에 따라 추가 프로바이더를 정의할 수도 있습니다.

애플리케이션의 인증 구성 파일은 `config/auth.php`에 있습니다. 이 파일에는 Laravel 인증 서비스의 동작을 조정할 수 있는 여러 문서화된 옵션들이 포함되어 있습니다.

> [!NOTE]  
> 가드와 프로바이더는 "역할(roles)"이나 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통한 사용자 작업 인가에 대해 더 알아보려면 [인가](/docs/10.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 킷 (Starter Kits)

빠르게 시작하길 원한다면? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 설치하세요. 데이터베이스 마이그레이션 후 브라우저에서 `/register` 같은 URL로 접속하면 스타터 킷이 인증 시스템 전체를 자동으로 스캐폴딩합니다!

**최종 Laravel 애플리케이션에서 스타터 킷을 사용하지 않더라도, [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze) 스타터 킷을 설치해보는 것은 Laravel에서 인증 기능이 어떻게 구현되는지 배우는 데 아주 좋은 기회입니다.** Laravel Breeze는 인증 컨트롤러, 라우트, 뷰를 생성해주므로, 이 파일들을 직접 보며 Laravel 인증 기능 구현 방식을 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

기본적으로 Laravel은 `app/Models` 디렉토리에 `App\Models\User` [Eloquent 모델](/docs/10.x/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. 애플리케이션에서 Eloquent를 사용하지 않는다면 Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수도 있습니다.

`App\Models\User` 모델의 데이터베이스 스키마를 구축할 때, 비밀번호 컬럼의 길이가 최소 60자 이상이어야 합니다. 물론 새 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이를 초과하는 컬럼을 생성합니다.

또한, `users`(또는 동등한) 테이블에 문자열 타입이며 100자 길이의 널 허용 `remember_token` 컬럼이 있는지 확인하세요. 이 컬럼은 사용자가 로그인 시 "로그인 유지" 옵션을 선택할 때 토큰을 저장하는 데 사용됩니다. 마찬가지로, 새 Laravel 애플리케이션의 기본 `users` 테이블 마이그레이션은 이 컬럼을 포함합니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증 관련 여러 패키지를 제공합니다. 계속하기 전에 Laravel 인증 에코시스템 전반을 살펴보고 각 패키지가 의도하는 목적을 설명하겠습니다.

먼저 인증 방식부터 생각해 봅시다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼에서 아이디와 비밀번호를 입력합니다. 정보가 올바르면 애플리케이션은 인증된 사용자 정보를 사용자 [세션](/docs/10.x/session)에 저장합니다. 브라우저에 발급된 쿠키는 세션 ID를 담아 이후 요청에 연결합니다. 애플리케이션은 세션 쿠키를 받고, 세션 ID 기반으로 세션 데이터를 불러와 인증 정보를 확인한 뒤 사용자를 "인증됨"으로 처리합니다.

반면, 원격 서비스가 API를 호출해 인증할 때는 웹 브라우저가 없으므로 쿠키 인증을 사용하지 않습니다. 대신, 원격 서비스는 각 요청마다 API 토큰을 전송하여 요청자가 누군지 식별합니다. 애플리케이션은 유효한 API 토큰 목록과 대조해 요청이 올바른지 확인하고 인증합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 내장 브라우저 인증 서비스 (Laravel's Built-in Browser Authentication Services)

Laravel은 보통 `Auth` 및 `Session` 파사드를 통해 접근하는 내장 인증 및 세션 서비스를 제공합니다. 이들은 웹 브라우저로부터 시작된 요청에 대해 쿠키 기반 인증 기능을 지원합니다. 사용자의 자격 증명 확인, 인증 처리 메서드를 제공하며, 적절한 인증 데이터를 사용자 세션에 저장하고 세션 쿠키를 발급합니다. 이 문서에서 이러한 서비스 사용법을 다룹니다.

**애플리케이션 스타터 킷**

앞서 설명했듯 Laravel 인증 서비스를 직접 사용해 애플리케이션에 인증층을 구현할 수도 있지만, 더 빠르게 시작할 수 있도록 강력하고 현대적인 인증 스캐폴딩을 제공하는 [무료 패키지](/docs/10.x/starter-kits)를 공개했습니다. 이 패키지는 [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/10.x/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/10.x/fortify)입니다.

_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 검증, 비밀번호 확인을 포함한 Laravel 인증 기능들의 단순하고 미니멀한 구현입니다. 뷰 계층은 단순한 [Blade 템플릿](/docs/10.x/blade)으로 구성되며, [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. Breeze는 [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com)에 기반한 스캐폴딩 옵션을 제공하며, Inertia에는 Vue 또는 React 중 선택할 수 있습니다.

_Laravel Fortify_는 Laravel를 위한 헤드리스 인증 백엔드로서, 쿠키 기반 인증과 2단계 인증, 이메일 검증 같은 여러 기능을 구현합니다. Fortify는 Laravel Jetstream의 인증 백엔드로 제공되거나, [Laravel Sanctum](/docs/10.x/sanctum)과 함께 독립적으로 SPA 인증 기능에 사용할 수도 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_는 Laravel Fortify 인증 서비스를 활용해 아름답고 현대적인 UI를 제공하는 강력한 애플리케이션 스타터 킷입니다. [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)를 사용하며, 2단계 인증, 팀 지원, 브라우저 세션 관리, 프로필 관리, 그리고 API 토큰 인증을 위한 [Laravel Sanctum](/docs/10.x/sanctum) 통합을 포함합니다. 아래에서 API 인증에 대해서도 다루겠습니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel API 인증 서비스 (Laravel's API Authentication Services)

Laravel은 API 토큰 관리와 API 토큰 인증 요청에 도움을 주는 두 가지 선택적 패키지를 제공합니다: [Passport](/docs/10.x/passport)와 [Sanctum](/docs/10.x/sanctum). 이 라이브러리들과 Laravel 내장 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 이 라이브러리들은 주로 API 토큰 인증에 중점을 두고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 중점을 둡니다. 많은 애플리케이션은 두가지 모두 사용합니다.

**Passport**

Passport는 OAuth2 인증 공급자이며, 다양한 OAuth2 "grant 타입"을 지원해 여러 유형의 토큰 발급이 가능합니다. 전반적으로 robust하고 복잡한 API 인증 패키지입니다. 그러나 대부분의 애플리케이션은 OAuth2가 제공하는 복잡한 기능을 필요로 하지 않으며, 이는 사용자와 개발자 모두에게 혼란을 줄 수 있습니다. 또한 SPA 또는 모바일 앱을 OAuth2 인증 공급자(예: Passport)와 사용해 인증하는 방법이 개발자들 사이에서 혼란스러운 경우가 많았습니다.

**Sanctum**

OAuth2의 복잡성과 개발자 혼란에 대응해, 우리는 웹 브라우저의 1차 웹 요청과 토큰을 이용한 API 요청을 모두 간단하고 효율적으로 처리할 수 있는 인증 패키지를 만들기로 했습니다. 그 결과가 [Laravel Sanctum](/docs/10.x/sanctum)입니다. Sanctum은 1차 웹 UI와 API, 별도의 SPA, 모바일 클라이언트를 제공하는 애플리케이션에 권장되는 인증 패키지입니다.

Laravel Sanctum은 하이브리드 웹/API 인증 패키지로, 애플리케이션의 전체 인증 프로세스를 관리할 수 있습니다. Sanctum 기반 애플리케이션이 요청을 받으면 먼저 요청이 인증 세션을 참조하는 세션 쿠키를 포함하는지 판단합니다. 이는 앞서 논의한 Laravel 내장 인증 서비스를 호출해서 처리합니다. 세션 쿠키로 인증되지 않았다면 요청에서 API 토큰을 찾고, 토큰이 있으면 해당 토큰으로 요청을 인증합니다. 자세한 내용은 Sanctum의 ["동작 원리"](/docs/10.x/sanctum#how-it-works) 문서를 참고하세요.

Laravel Sanctum은 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 킷에 포함된 API 패키지로, 대다수 웹 애플리케이션 요구에 가장 적합하다고 판단됩니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택 (Summary and Choosing Your Stack)

요약하면, 애플리케이션이 브라우저로 접근하고 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 사용합니다.

API를 제3자가 사용하는 경우, API 토큰 인증을 위해 [Passport](/docs/10.x/passport) 또는 [Sanctum](/docs/10.x/sanctum) 중 선택합니다. 일반적으로 Sanctum이 간단하고 완전한 API, SPA, 모바일 인증 솔루션이며 "scope" 또는 "abilities" 지원까지 포함해 선호됩니다.

SPA를 Laravel 백엔드로 구동한다면 [Laravel Sanctum](/docs/10.x/sanctum)을 사용하세요. Sanctum 사용 시 [수동으로 백엔드 인증 라우트 구현](#authenticating-users)하거나 [Laravel Fortify](/docs/10.x/fortify)같은 헤드리스 백엔드 인증 서비스를 활용할 수 있습니다. Fortify는 회원가입, 비밀번호 초기화, 이메일 검증 등의 라우트와 컨트롤러를 제공합니다.

OAuth2 규격에서 제공하는 모든 기능을 꼭 써야 하는 경우만 Passport를 선택하세요.

빠르게 시작하려면 [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze)를 추천합니다. Breeze는 Laravel 내장 인증 서비스와 Sanctum을 이용하는 기본 인증 스택을 바로 사용해 시작할 수 있습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]  
> 이 문서 단원은 [Laravel 애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 사용한 사용자 인증을 다룹니다. 이는 빠른 시작을 위해 UI 스캐폴딩을 제공합니다. Laravel 인증 시스템과 직접 통합하려면 [수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치 (Install a Starter Kit)

먼저 [Laravel 애플리케이션 스타터 킷](/docs/10.x/starter-kits) 중 하나를 설치하세요. 현재 Laravel Breeze와 Laravel Jetstream은 새 Laravel 애플리케이션에 인증을 쉽게 통합할 아름답고 잘 설계된 시작점을 제공합니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 초기화, 이메일 검증, 비밀번호 확인을 포함하는 간단하고 최소한의 인증 구현입니다. Breeze 뷰 계층은 [Blade 템플릿](/docs/10.x/blade) 기반이며 [Tailwind CSS](https://tailwindcss.com)로 스타일링 되었고, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com) 기반 스캐폴딩 옵션과 Inertia 사용 시 Vue 또는 React 중 선택이 가능합니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 더 견고한 스타터 킷으로, [Livewire](https://livewire.laravel.com)나 [Inertia 및 Vue](https://inertiajs.com) 기반 스캐폴딩을 지원합니다. 또한 2단계 인증, 팀, 프로필 관리, 브라우저 세션 관리, API 지원([Laravel Sanctum](/docs/10.x/sanctum)) 및 계정 삭제 등의 기능을 포함합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기 (Retrieving the Authenticated User)

스타터 킷 설치 후 사용자가 애플리케이션에 등록 및 인증하면, 현재 인증된 사용자와 상호작용할 일이 많아집니다. 들어오는 요청을 처리하는 동안 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기...
$user = Auth::user();

// 현재 인증된 사용자의 ID 가져오기...
$id = Auth::id();
```

또는, 사용자가 인증된 후 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 접근할 수 있습니다. 타입힌트된 클래스는 컨트롤러 메서드에 자동으로 주입됩니다. `Illuminate\Http\Request`를 타입힌트하면 요청의 `user` 메서드를 사용해 어떤 컨트롤러 메서드에서도 인증된 사용자에 편리하게 접근 가능:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 비행 정보 업데이트.
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

요청을 보내는 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 사용자가 인증된 경우 `true`를 반환합니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있음...
}
```

> [!NOTE]  
> `check` 메서드로 인증 여부를 알 수 있지만, 일반적으로는 특정 라우트 또는 컨트롤러에 접근을 허용하기 전에 미들웨어를 통해 인증을 확인합니다. 이에 관한 내용은 [라우트 보호하기](/docs/10.x/authentication#protecting-routes) 문서에서 확인하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

[라우트 미들웨어](/docs/10.x/middleware)는 인증된 사용자만 해당 라우트에 접근하도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어를 기본 제공합니다. 이 미들웨어는 HTTP 커널에 이미 등록되어 있으므로, 라우트 정의에 미들웨어만 붙이면 됩니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, `login` [이름붙은 라우트](/docs/10.x/routing#named-routes)로 리디렉션합니다. 이 동작은 `app/Http/Middleware/Authenticate.php` 내 `redirectTo` 메서드를 수정해 변경할 수 있습니다:

```
use Illuminate\Http\Request;

/**
 * 사용자 리디렉션 경로 반환.
 */
protected function redirectTo(Request $request): string
{
    return route('login');
}
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 붙일 때 어느 "가드"를 사용할지 지정할 수도 있습니다. 지정한 가드는 `auth.php` 구성 파일 내 `guards` 배열 키와 일치해야 합니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

Laravel Breeze 혹은 Laravel Jetstream [스타터 킷](/docs/10.x/starter-kits)을 사용할 경우 로그인 시도에 대해 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본 설정에서는 여러 번 로그인 실패 시 해당 username/email과 IP 주소를 기준으로 1분간 로그인이 차단됩니다.

> [!NOTE]  
> 다른 라우트에 속도 제한을 적용하려면 [속도 제한 문서](/docs/10.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 수동으로 사용자 인증하기 (Manually Authenticating Users)

Laravel의 [애플리케이션 스타터 킷](/docs/10.x/starter-kits)의 인증 스캐폴딩을 반드시 사용할 필요는 없습니다. 이를 사용하지 않는다면 Laravel 인증 클래스를 직접 이용해 사용자 인증을 직접 관리해야 합니다. 걱정 마세요, 매우 간단합니다!

Laravel 인증 서비스는 `Auth` [파사드](/docs/10.x/facades)를 통해 접근합니다. 먼저 클래스 상단에 `Auth` 파사드를 임포트하세요. 다음으로 `attempt` 메서드를 살펴봅시다. `attempt` 메서드는 보통 로그인 폼에서 제출된 인증 시도를 처리하는 데 사용합니다. 인증이 성공하면 사용자의 [세션](/docs/10.x/session)을 재생성해 [세션 고정(session fixation)](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

```
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
            'email' => '제공된 자격 증명이 기록과 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드 첫 번째 인자로 키-값 쌍 배열을 받습니다. 배열 내 값들은 데이터베이스에서 사용자를 찾는 조건으로 사용됩니다. 위 예에서는 `email` 컬럼 값이 일치하는 사용자를 찾는 것입니다. 사용자가 발견되면, 데이터베이스에 저장된 해시된 비밀번호와 입력된 `password` 값이 비교됩니다. 요청의 `password`는 해시할 필요 없으며, Laravel이 자동으로 해시하여 비교합니다. 두 해시가 일치하면 인증된 세션이 시작됩니다.

Laravel 인증 서비스는 인증 가드의 `provider` 설정을 기반으로 사용자를 데이터베이스에서 조회합니다. 기본 `config/auth.php` 파일에서는 Eloquent 사용자 프로바이더를 지정하며 `App\Models\User` 모델을 사용하도록 설정되어 있습니다. 애플리케이션 필요에 따라 구성값을 변경할 수 있습니다.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

Laravel 리다이렉터의 `intended` 메서드를 이용하면 인증 미들웨어에 의해 가로막히기 전 시도했던 URL로 사용자를 리다이렉트합니다. 해당 URL이 없을 경우 대체 URI도 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 명시하기

필요하면 사용자의 이메일과 비밀번호 외에 추가적인 쿼리 조건도 인증 쿼리에 추가할 수 있습니다. `attempt`에 전달하는 배열 내에 조건을 추가하기만 하면 됩니다. 예를 들어, 사용자가 활성화(active) 상태인지 확인할 수 있습니다:

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

복잡한 쿼리 조건이 필요하면 배열에 클로저를 추가할 수 있습니다. 클로저는 쿼리 인스턴스를 받아 애플리케이션 요구에 맞게 커스터마이즈할 수 있습니다:

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
> 예시에서 `email`은 필수가 아니며, 단순히 예시로 들어간 것입니다. 데이터베이스 내 "사용자명(username)"에 해당하는 컬럼 이름을 써야 합니다.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받으며, 잠재적 사용자를 더 자세히 검사해 실제 인증 가능 여부를 판단합니다. 클로저에 전달된 사용자가 인증이 가능하면 `true`, 아니면 `false`를 반환해야 합니다:

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

`Auth` 파사드의 `guard` 메서드에 가드 이름을 지정해 특정 가드 인스턴스를 이용할 수 있습니다. 이를 통해 애플리케이션 여러 영역에 대해 서로 다른 인증가능 모델이나 사용자 테이블을 별도로 관리할 수 있습니다.

`guard` 메서드에 전달하는 이름은 `auth.php` 구성 파일 내 `guards` 설정 값 중 하나여야 합니다:

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹 애플리케이션은 로그인 폼에 "로그인 유지(remember me)" 체크박스를 둡니다. "로그인 유지" 기능을 제공하고 싶다면 `attempt` 메서드의 두 번째 인수로 boolean 값을 넣으면 됩니다.

`true`로 설정하면 Laravel은 사용자가 명시적으로 로그아웃할 때까지 무기한 인증 세션을 유지합니다. `users` 테이블에는 "로그인 유지" 토큰을 저장할 `remember_token` 문자열 컬럼이 있어야 합니다. 새 Laravel 애플리케이션의 기본 `users` 테이블 마이그레이션에는 이미 포함되어 있습니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 로그인 유지됨...
}
```

애플리케이션에 "로그인 유지" 기능이 있다면 `viaRemember` 메서드로 현재 인증된 사용자가 "로그인 유지" 쿠키로 인증되었는지 확인할 수 있습니다:

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

기존 사용자 인스턴스를 현재 인증된 사용자로 설정하려면, 사용자 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하세요. 전달하는 사용자는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/10.x/contracts)을 구현해야 합니다. Laravel 기본 `App\Models\User` 모델은 이미 이 인터페이스를 구현합니다. 이 방식은 사용자가 방금 회원가입을 완료했을 때처럼 이미 유효한 사용자 인스턴스를 가지고 있는 경우에 유용합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인수에 boolean 값을 전달해 "로그인 유지" 여부를 지정할 수 있습니다. `true`일 경우 세션을 무기한 인증 상태로 유지하거나, 사용자가 수동 로그아웃할 때까지 유지합니다:

```
Auth::login($user, $remember = true);
```

필요하다면 `login` 호출 전에 인증 가드를 지정할 수도 있습니다:

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증하기

데이터베이스 기본 키(primary key)를 이용해 사용자를 인증하려면 `loginUsingId` 메서드를 사용하세요. 인증할 사용자의 기본 키를 인자로 받습니다:

```
Auth::loginUsingId(1);
```

마찬가지로 두 번째 인수로 "로그인 유지" boolean 값을 전달할 수 있습니다:

```
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 인증하기

`once` 메서드를 사용하면 세션이나 쿠키를 사용하지 않고 단일 요청에 한해 일시적으로 인증할 수 있습니다:

```
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 없이 빠르게 애플리케이션 사용자를 인증하는 방법을 제공합니다. 시작하려면 라우트에 `auth.basic` [미들웨어](/docs/10.x/middleware)를 붙이세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 기본 포함되어 있어 직접 정의하지 않아도 됩니다:

```
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth.basic');
```

미들웨어가 라우트에 붙으면 브라우저 접속 시 자동으로 인증 창이 뜹니다. 기본적으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 사용자의 "사용자명(username)"으로 가정합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 주의사항

만약 PHP FastCGI와 Apache를 사용해 Laravel 앱을 서비스한다면 HTTP 기본 인증이 제대로 작동하지 않을 수 있습니다. 이를 해결하려면 애플리케이션 `.htaccess` 파일에 다음 내용을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 무상태(stateless) HTTP 기본 인증

세션에 사용자 식별 쿠키를 설정하지 않고 HTTP 기본 인증만 사용해 인증할 수도 있습니다. 주로 API 요청 인증에 사용합니다. 이를 위해 `onceBasic` 메서드를 호출하는 미들웨어를 정의하세요. `onceBasic`이 응답을 반환하지 않으면 요청을 다음 미들웨어/애플리케이션으로 전달합니다:

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
     * 요청 처리.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

이후 이 미들웨어를 라우트에 붙입니다:

```
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 수동으로 로그아웃시키려면 `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 사용자의 세션에서 인증 정보를 제거해 이후 요청이 인증되지 않도록 만듭니다.

`logout` 호출 후에는 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/10.x/csrf)을 재생성하는 게 권장됩니다. 로그아웃 후 보통 애플리케이션 루트로 리다이렉트합니다:

```
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 사용자 로그아웃 처리.
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

Laravel은 현재 기기의 인증 세션은 유지하면서 다른 기기에서 활성화된 사용자 세션을 무효화하고 로그아웃시키는 기능도 제공합니다. 이 기능은 보통 사용자가 비밀번호를 변경할 때, 다른 기기 세션을 무효화 하길 원할 때 유용합니다.

우선, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 적용할 라우트에 포함되었는지 확인하세요. 일반적으로 라우트 그룹에 이 미들웨어를 포함시켜 애플리케이션 라우트 대부분에 적용합니다. 기본 설치 상태에서는 `auth.session` 라우트 미들웨어 별칭으로 HTTP 커널에 등록되어 있습니다:

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그다음 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 현재 비밀번호 확인을 요구하며, 애플리케이션에서 입력 폼으로 받아야 합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`를 호출하면 사용자의 다른 세션이 완전히 무효화되어 모든 가드에서 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션에서 특정 작업을 수행하거나 민감 영역에 접근할 때, 사용자가 비밀번호를 다시 확인하도록 요구할 수 있습니다. Laravel은 이를 간편하게 구현할 수 있는 내장 미들웨어를 제공합니다. 이 기능을 구현하려면 두 개의 라우트를 정의해야 합니다: 비밀번호 확인을 요청하는 화면을 보여주는 라우트와 비밀번호 유효성을 확인하고 사용자를 의도한 위치로 리다이렉트하는 라우트입니다.

> [!NOTE]  
> 아래 문서는 Laravel 비밀번호 확인 기능을 직접 통합하는 방법을 다룹니다. 빠른 시작을 원하면 [Laravel 애플리케이션 스타터 킷](/docs/10.x/starter-kits)이 이 기능을 이미 지원합니다.

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

비밀번호를 한 번 확인하면 3시간 동안 다시 확인하지 않습니다. 이 시간은 애플리케이션 `config/auth.php` 설정 파일 내 `password_timeout` 값을 변경해 조절할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자에게 비밀번호 확인 뷰를 보여주는 라우트를 정의합니다:

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

리턴된 뷰에는 `password` 필드를 포함한 폼이 있어야 하며, 사용자가 민감한 영역에 접근하기 위해 비밀번호를 확인해야 한다는 안내 문구를 포함해도 좋습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, "비밀번호 확인" 뷰에서 전달된 폼 요청을 처리하는 라우트를 정의합니다. 비밀번호 유효성을 검증하고 의도한 위치로 리다이렉트합니다:

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

이 라우트를 자세히 보면, 먼저 요청의 `password`가 인증된 사용자의 비밀번호와 실제로 일치하는지 검사합니다. 비밀번호가 유효하면 Laravel 세션에 비밀번호 확인 시간 타임스탬프를 기록하는 `passwordConfirmed` 메서드를 호출합니다. 이 타임스탬프는 이후 사용자가 비밀번호를 마지막으로 확인한 시간을 판단하는 데 쓰입니다. 마지막으로 사용자를 의도한 경로로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호하기

최근 비밀번호 확인이 필요한 작업을 수행하는 라우트에는 `password.confirm` 미들웨어를 반드시 지정하세요. 이 미들웨어는 기본 Laravel 설치 시 포함되어 있으며, 사용자가 비밀번호 확인 후 원래 위치로 돌아갈 수 있도록 세션에 의도한 경로를 자동 저장합니다. 그 후 `password.confirm` 이름붙은 라우트로 리다이렉트합니다:

```
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가하기 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 사용해 자신만의 인증 가드를 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/10.x/providers)에 넣으세요. Laravel은 이미 `AuthServiceProvider`를 제공하므로 그 곳에 작성하면 됩니다:

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 인증/인가 서비스 등록.
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

위 예제에서 볼 수 있듯, `extend` 메서드에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard`를 구현하는 인스턴스를 반환해야 합니다. 이 인터페이스에는 커스텀 가드를 정의하기 위해 구현해야 하는 몇 가지 메서드가 포함됩니다. 커스텀 가드 정의 후에는 `auth.php` 구성 파일의 `guards` 배열에서 해당 가드를 참조할 수 있습니다:

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

HTTP 요청 기반 커스텀 인증 시스템을 가장 간단히 구현하려면 `Auth::viaRequest` 메서드를 사용합니다. 이 메서드는 단일 클로저를 이용해 인증 프로세스를 빠르게 정의할 수 있습니다.

`AuthServiceProvider`의 `boot` 메서드 내에서 `Auth::viaRequest`를 호출하세요. 첫 번째 인자는 인증 드라이버 이름이며, 두 번째 인자는 요청을 받아 사용자 인스턴스를 반환하거나 인증 실패 시 `null`을 반환하는 클로저입니다:

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션 인증 / 인가 서비스 등록.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

커스텀 인증 드라이버가 정의되면, `auth.php` 구성 파일 내 `guards` 배열에 드라이버명과 함께 등록하세요:

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로, 라우트에 미들웨어로 가드를 할당할 때 해당 가드를 참조하세요:

```
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가하기 (Adding Custom User Providers)

전통적인 관계형 데이터베이스가 아닌 다른 저장소에 사용자 데이터를 보관한다면, Laravel 인증 시스템에 맞게 사용자 프로바이더를 직접 확장해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 정의합니다. 프로바이더는 `Illuminate\Contracts\Auth\UserProvider` 인터페이스를 구현해야 합니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 인증 / 인가 서비스 등록.
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

`provider` 메서드로 프로바이더를 등록한 후, `auth.php` 파일 내 `providers` 배열에 해당 드라이버를 등록하세요:

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그다음 `guards` 설정에서 해당 프로바이더를 참조합니다:

```
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### User Provider 계약 (The User Provider Contract)

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등 영속 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 불러오는 책임이 있습니다. 이 두 인터페이스 덕분에 사용자 데이터 저장소와 사용자 클래스 형태에 관계없이 인증 메커니즘이 작동합니다.

`UserProvider` 계약은 다음과 같습니다:

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
}
```

- `retrieveById`는 보통 자동 증가 ID 같은 사용자의 키를 받아 해당 사용자 `Authenticatable` 구현체를 반환합니다.
- `retrieveByToken`은 고유 식별자 `$identifier`와 "로그인 유지" 토큰 `$token`으로 사용자를 조회해 반환합니다.
- `updateRememberToken`은 `$user` 인스턴스의 `remember_token`을 새 토큰으로 업데이트합니다. 이 토큰은 "로그인 유지" 인증 성공 시 또는 로그아웃 시 새로 할당됩니다.
- `retrieveByCredentials`는 `Auth::attempt` 시 전달된 자격증명 배열을 받아 사용자 조회 쿼리를 실행합니다. 보통 `$credentials['username']`에 해당하는 조건으로 사용자 레코드를 찾습니다. 이 메서드는 반드시 비밀번호 인증은 수행하지 않아야 합니다.
- `validateCredentials`는 주어진 `$user`와 `$credentials` 정보를 비교해 사용자가 인증 가능한지 검사합니다. 주로 `Hash::check`를 사용해 비밀번호 검증을 수행하며, 결과로 `true` 또는 `false`를 반환해야 합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약 (The Authenticatable Contract)

`UserProvider` 메서드가 반환하는 `Authenticatable` 구현체는 아래 계약을 따릅니다. 기본적으로 Laravel의 `App\Models\User` 클래스가 이 인터페이스를 구현합니다:

```
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

- `getAuthIdentifierName`은 사용자 기본 키 필드 이름을 반환합니다.
- `getAuthIdentifier`는 기본 키 값(예: MySQL의 자동 증가 ID)을 반환합니다.
- `getAuthPassword`는 사용자의 해시된 비밀번호를 반환합니다.
- `getRememberToken`, `setRememberToken`, `getRememberTokenName`은 "로그인 유지" 토큰 관련 메서드입니다.

이를 통해 Laravel 인증 시스템은 ORM이나 저장소 종류에 관계없이 일관된 방식으로 사용자 클래스와 호환됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 프로세스 도중 다양한 [이벤트](/docs/10.x/events)를 발생시킵니다. 이벤트 서비스 프로바이더(`EventServiceProvider`)에 리스너를 연결할 수 있습니다:

```
/**
 * 애플리케이션 이벤트 리스너 매핑.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Auth\Events\Registered' => [
        'App\Listeners\LogRegisteredUser',
    ],

    'Illuminate\Auth\Events\Attempting' => [
        'App\Listeners\LogAuthenticationAttempt',
    ],

    'Illuminate\Auth\Events\Authenticated' => [
        'App\Listeners\LogAuthenticated',
    ],

    'Illuminate\Auth\Events\Login' => [
        'App\Listeners\LogSuccessfulLogin',
    ],

    'Illuminate\Auth\Events\Failed' => [
        'App\Listeners\LogFailedLogin',
    ],

    'Illuminate\Auth\Events\Validated' => [
        'App\Listeners\LogValidated',
    ],

    'Illuminate\Auth\Events\Verified' => [
        'App\Listeners\LogVerified',
    ],

    'Illuminate\Auth\Events\Logout' => [
        'App\Listeners\LogSuccessfulLogout',
    ],

    'Illuminate\Auth\Events\CurrentDeviceLogout' => [
        'App\Listeners\LogCurrentDeviceLogout',
    ],

    'Illuminate\Auth\Events\OtherDeviceLogout' => [
        'App\Listeners\LogOtherDeviceLogout',
    ],

    'Illuminate\Auth\Events\Lockout' => [
        'App\Listeners\LogLockout',
    ],

    'Illuminate\Auth\Events\PasswordReset' => [
        'App\Listeners\LogPasswordReset',
    ],
];
```