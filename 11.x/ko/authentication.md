# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 퀵스타트](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 시도 제한](#login-throttling)
- [수동 사용자 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [무상태 HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호하기](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 제공자 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해시](#automatic-password-rehashing)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 방법을 제공합니다. 웹 애플리케이션에서 이 기능을 구현하는 것은 복잡하고 잠재적으로 위험할 수 있기 때문에, Laravel은 인증을 빠르고, 안전하게, 그리고 쉽게 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 기능은 "가드(guards)"와 "프로바이더(providers)"로 구성되어 있습니다. 가드는 각 요청마다 사용자가 어떻게 인증되는지 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용하여 상태를 유지하는 `session` 가드를 기본으로 제공합니다.

프로바이더는 영구 저장소(데이터베이스 등)에서 사용자를 어떻게 가져올지 정의합니다. Laravel은 [Eloquent](/docs/{{version}}/eloquent) 및 데이터베이스 쿼리 빌더를 통한 사용자 조회를 기본으로 지원합니다. 물론, 필요하다면 애플리케이션에 맞게 추가 프로바이더를 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 인증 서비스의 동작을 세밀하게 조정할 수 있는 옵션이 잘 문서화되어 있습니다.

> [!NOTE]  
> 가드와 프로바이더는 "역할(roles)"이나 "권한(permissions)"과 혼동해서는 안 됩니다. 사용자 권한을 통한 액션 허가에 대해 더 알고 싶다면 [권한(authorization)](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 다른 URL로 이동하면 됩니다. 스타터 키트가 전체 인증 시스템의 스캐폴딩을 자동으로 처리합니다!

**최종적으로 스타터 키트를 사용하지 않는다고 해도, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 스타터 키트를 설치하여 실제 Laravel 프로젝트에서 모든 인증 기능이 어떻게 구현되는지 학습해 볼 수 있습니다.** Breeze는 인증 컨트롤러, 라우트, 뷰까지 생성해주므로, 해당 코드들을 살펴보며 Laravel 인증 기능의 구현 방식을 배울 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

기본적으로 Laravel은 `app/Models` 디렉토리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우에는 MongoDB의 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 작성할 때, 패스워드 컬럼이 최소 60자 이상이어야 합니다. 기본적으로 새 Laravel 애플리케이션의 `users` 테이블 마이그레이션에는 이 길이를 초과하는 컬럼이 이미 포함되어 있습니다.

또한, `users`(또는 해당 역할) 테이블에 null이 허용되는 100자 길이의 문자열 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 사용자가 로그인 시 "로그인 상태 유지" 옵션을 선택할 때 토큰을 저장하는 데 사용됩니다. 역시 기본 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속해서 설명을 진행하기 전에, Laravel의 인증 에코시스템을 전체적으로 살펴보고 각 패키지의 사용 목적을 소개합니다.

먼저 인증이 어떻게 동작하는지 생각해봅니다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼에 아이디와 비밀번호를 입력합니다. 자격 증명이 올바르면, 애플리케이션은 인증된 사용자 정보를 [세션](/docs/{{version}}/session)에 저장하고, 세션 ID가 담긴 쿠키를 브라우저에 발급하여 이후의 요청에서도 사용자를 식별할 수 있게 합니다. 세션 쿠키를 받은 뒤에는, 애플리케이션이 세션 ID로 세션 데이터를 조회하고, 인증 정보를 확인하여 사용자가 "인증됨" 상태임을 판단합니다.

원격 서비스가 API 접근을 위해 인증해야 할 때는, 일반적으로 쿠키를 사용하지 않습니다. 대신, 매 요청마다 API 토큰을 전송합니다. 애플리케이션은 들어온 토큰을 유효 토큰 테이블과 비교하여, 해당 API 토큰 소유자로 요청을 "인증"합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel은 내장 인증 및 세션 서비스를 제공합니다. 주로 `Auth` 및 `Session` 파사드를 통해 접근할 수 있습니다. 이들은 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 확인하고, 인증이 완료되면 적절한 인증 정보를 세션에 저장하고 세션 쿠키를 발급합니다. 이 서비스 사용법은 본 문서에서 다룹니다.

**애플리케이션 스타터 키트**

물론, 이 인증 서비스를 직접 사용해 애플리케이션 고유의 인증 레이어를 구현할 수 있습니다. 그러나 더 빠른 구현을 돕기 위해 [무료 스타터 키트 패키지](/docs/{{version}}/starter-kits)를 제공합니다. 주요 스타터 키트는 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/{{version}}/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/{{version}}/fortify)입니다.

_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인을 포함한 모든 인증 기능을 최소한으로 담으며 심플하게 구현합니다. 뷰는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)를 기반으로 합니다. 자세한 내용은 [응용 프로그램 스타터 키트 문서](/docs/{{version}}/starter-kits)를 참고하세요.

_Laravel Fortify_는 Laravel의 비주얼 없는(Headless) 인증 백엔드이며, 본 문서의 여러 기능(쿠키 기반 인증, 2차 인증, 이메일 인증 등)이 포함되어 있습니다. Fortify는 Laravel Jetstream의 인증 백엔드이며, [Laravel Sanctum](/docs/{{version}}/sanctum)과 결합하여 SPA 인증 백엔드로도 사용할 수 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_은 Fortify의 인증 기능을 [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 기반의 현대적 UI로 노출하는 스타터 키트입니다. 2차 인증, 팀, 브라우저 세션, 프로필 관리, [Laravel Sanctum](/docs/{{version}}/sanctum) 기반의 API 토큰 인증이 내장 지원됩니다. Laravel의 API 인증 옵션은 아래에서 다시 설명합니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리와 인증을 지원하는 두 가지 패키지, [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum)을 제공합니다. 이 라이브러리와 Laravel의 내장 쿠키 인증 라이브러리는 병행 사용이 가능합니다. API 토큰 인증에 중점을 두고 있으며, 내장 인증 서비스는 브라우저 기반 인증에 주력합니다. 대부분의 애플리케이션이 둘 다 활용하게 됩니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"을 지원하는 OAuth2 인증 제공자입니다. 매우 강력하고 복잡한 패키지지만, 대부분의 애플리케이션은 OAuth2의 고급 기능까지는 필요하지 않고, 오히려 혼란을 줄 수 있습니다. SPA나 모바일 애플리케이션의 인증 연동에서 자주 혼동이 있었습니다.

**Sanctum**

OAuth2의 복잡성과 개발자의 혼란에 대응해, 웹 요청과 토큰 기반 API 요청을 모두 다룰 수 있는 보다 단순하고 직관적인 패키지인 [Laravel Sanctum](/docs/{{version}}/sanctum)을 개발했습니다. 웹 UI와 API를 모두 제공하거나, 프론트엔드와 백엔드가 분리된 SPA 또는 모바일 앱 백엔드 인증에 적합합니다.

Sanctum은 하이브리드 웹/API 인증 패키지로, 애플리케이션 인증 전체를 담당할 수 있습니다. 요청에 세션 쿠키가 있는 경우 내장 인증 서비스를, 그렇지 않으면 API 토큰으로 인증을 처리합니다. 작동 방식에 대해 더 알고싶다면 Sanctum의 ["작동 방식"](/docs/{{version}}/sanctum#how-it-works) 문서를 참고하세요.

Sanctum은 [Laravel Jetstream](https://jetstream.laravel.com)에 내장된 API 인증 패키지이며, 대부분의 웹앱 인증 요구에 최적입니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택하기

요약하자면, 브라우저로 접근하는 모놀리식 Laravel 앱을 만든다면 내장 인증 서비스를 사용하게 됩니다.

API 제공이 필요하다면, [Passport](/docs/{{version}}/passport) 또는 [Sanctum](/docs/{{version}}/sanctum) 중 선택해야 합니다. 일반적으로 웹/API/SPAR 인증·모바일 인증에서의 단순성과 완결성 때문에 Sanсtum을 추천합니다(스코프/권한 기능 포함).

SPA 백엔드를 Laravel로 만들 땐 [Laravel Sanctum](/docs/{{version}}/sanctum)이 최선입니다. 이 때는 [인증 라우트 직접 구현](#authenticating-users)하거나 [Laravel Fortify](/docs/{{version}}/fortify)를 헤드리스 인증 서비스로 사용할 수 있습니다.

OAuth2 전체 기능이 반드시 필요한 경우에만 Passport를 사용하세요.

빠르게 시작하고 싶다면 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)로 내장 인증 서비스와 Sanctum 조합을 권장합니다.

<a name="authentication-quickstart"></a>
## 인증 퀵스타트

> [!WARNING]  
> 이 부분은 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 통한 인증에 중점을 두며, 빠른 시작을 위한 UI 스캐폴딩이 포함되어 있습니다. 인증 시스템을 직접 통합하고 싶다면 [수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치해야 합니다. 현재 제공되는 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 인증 기능이 내장된 아름다운 출발점을 제공합니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 인증 기능을 최소화하여 간단하게 제공합니다. 뷰는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com) 기반입니다. 또한, [Livewire](https://livewire.laravel.com) 혹은 [Inertia](https://inertiajs.com) 기반(React/Vue 선택 가능)의 스캐폴딩 옵션도 있습니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 더 강력한 스타터 키트로, [Livewire](https://livewire.laravel.com) 또는 [Inertia/Vue](https://inertiajs.com) 기반 스캐폴딩을 지원합니다. Jetstream은 2차 인증, 팀, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/{{version}}/sanctum) 기반 API 지원, 계정 삭제 등 다양한 기능을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기

스타터 키트를 설치한 뒤, 사용자가 회원가입 및 인증할 수 있게 되면, 종종 현재 인증된 사용자에 접근해야 할 일이 있습니다. 요청 처리 중에는 `Auth` 파사드의 `user` 메서드로 인증된 사용자 인스턴스에 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기
$user = Auth::user();

// 현재 인증된 사용자의 ID 가져오기
$id = Auth::id();
```

또는 인증된 사용자는 `Illuminate\Http\Request` 인스턴스를 통해서도 접근할 수 있습니다. 컨트롤러 메서드에 타입힌트로 주입하면 언제든지 요청의 `user` 메서드로 인증 사용자를 가져올 수 있습니다.

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

들어온 요청의 사용자가 인증되었는지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 인증되었을 때 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인함
}
```

> [!NOTE]  
> `check` 메서드로 사용자가 인증 상태인지 확인할 수는 있지만, 실제로는 미들웨어를 사용하여 인증이 필요한 라우트/컨트롤러에 접근을 제한하는 것이 일반적입니다. 자세한 내용은 [라우트 보호하기](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용하여 인증된 사용자만 특정 라우트에 접근할 수 있도록 할 수 있습니다. Laravel에는 `Illuminate\Auth\Middleware\Authenticate` 클래스에 대한 [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)인 `auth` 미들웨어가 내부적으로 등록되어 있습니다. 단순히 라우트에 미들웨어를 연결하면 됩니다.

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자의 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션합니다. 이 동작은 애플리케이션의 `bootstrap/app.php`에서 `redirectGuestsTo` 메서드로 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저를 사용할 수도 있습니다
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 연결할 때, 어떤 "가드"를 사용할지 지정할 수 있습니다. 지정한 값은 `auth.php` 설정 파일의 `guards` 배열의 키와 일치해야 합니다.

```php
Route::get('/flights', function () {
    // 인증된 관리자만 접근 가능
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 시도 제한

Laravel Breeze 또는 Laravel Jetstream [스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우, 로그인 시도에 대한 레이트 리미팅이 자동으로 적용됩니다. 기본적으로 여러 번 잘못된 인증 시도가 있을 경우 1분간 로그인을 할 수 없습니다. 이 제한은 사용자 이름/이메일과 사용자의 IP 주소를 조합해 구분됩니다.

> [!NOTE]  
> 애플리케이션의 다른 라우트에도 레이트 리미팅을 적용하고 싶다면 [레이트 리미팅 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 수동 사용자 인증

Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)에서 제공하는 인증 스캐폴딩을 반드시 사용해야 하는 것은 아닙니다. 스캐폴딩을 사용하지 않을 경우, Laravel 인증 클래스를 직접 사용해 사용자 인증을 처리해야 합니다. 걱정하지 마세요, 매우 간단합니다!

Laravel의 인증 서비스에 접근하려면 `Auth` [파사드](/docs/{{version}}/facades)를 임포트해야 합니다. 그 다음, 보통 로그인 폼을 통해 인증을 처리할 때는 `attempt` 메서드를 사용합니다. 인증에 성공하면 [세션](/docs/{{version}}/session) 재생성을 통해 [세션 고정 공격 방지](https://en.wikipedia.org/wiki/Session_fixation)도 잊지 마세요.

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
            'email' => '입력하신 자격 증명이 우리 기록과 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 key/value 쌍의 배열을 첫 인자로 받습니다. 예시에서는 `email` 컬럼 값으로 사용자를 찾고, 데이터베이스에 저장된 해시된 비밀번호와 입력한 비밀번호를 비교합니다. 요청의 `password` 값은 해싱하지 않아도 됩니다. 프레임워크가 자동으로 비교 전에 해싱해줍니다. 일치할 경우 인증 세션이 시작됩니다.

Laravel의 인증 서비스는 가드의 "provider" 설정에 따라 사용자를 DB에서 조회합니다. 기본의 `config/auth.php` 에서는 Eloquent 유저 프로바이더가 사용되고, 사용자 조회 시 `App\Models\User` 모델을 사용하도록 지정되어 있습니다. 그 외의 값들은 필요에 따라 변경하면 됩니다.

`attempt`는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

Laravel의 `intended` 메서드는 인증 미들웨어에 의해 중단된 원래 URL로 사용자를 리다이렉트합니다. 적합한 URL이 없으면 기본값도 지정 가능합니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

이메일, 비밀번호 외에 추가 조건(query 조건)을 추가할 수도 있습니다. `attempt` 메서드에 전달하는 배열에 조건을 추가하면 됩니다. 예를 들어, 사용자가 "active"인지 확인하고자 할 때:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공
}
```

복잡한 쿼리 조건의 경우, 크레덴셜 배열에 클로저를 포함할 수 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받아 쿼리 수정이 가능합니다.

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
> 위 예시에서 `email`은 필수 옵션이 아니며, 예시로 사용된 것입니다. DB에서 "아이디"로 사용하는 컬럼명을 활용하세요.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받고, 인증 전 후보 유저를 더 엄격하게 검사할 수 있습니다. 클로저는 유저 인스턴스를 받아 `true`/`false`를 반환해야 합니다.

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
#### 특정 가드 인스턴스 사용

`Auth` 파사드의 `guard` 메서드로, 인증 과정에서 사용할 가드 인스턴스를 지정할 수 있습니다. 이를 통해 별도 사용자 테이블/모델 기반의 독립된 인증을 구현할 수 있습니다.

가드 명칭은 `auth.php`의 `guards` 설정과 일치해야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹앱은 로그인 폼에 "로그인 상태 유지" 체크박스를 제공합니다. 이 기능 제공을 원하면, `attempt` 메서드의 두 번째 인자로 boolean 값을 넘기면 됩니다.

이 값이 `true`면, 사용자가 직접 로그아웃하지 않는 이상 인증 상태가 계속 유지됩니다. 이를 위해 `users` 테이블에 문자열 `remember_token` 칼럼이 필요합니다. 기본 마이그레이션에는 이미 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자를 기억 중
}
```

이 기능이 활성화된 경우, `Auth::viaRemember()` 메서드로 현재 인증 사용자가 "로그인 상태 유지" 쿠키로 인증받았는지 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 직접 인증

이미 유효한 사용자 인스턴스가 있는 경우, `Auth` 파사드의 `login` 메서드로 현재 인증 사용자로 설정 가능합니다. 해당 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/{{version}}/contracts)을 구현해야 합니다. Laravel의 기본 `App\Models\User` 모델이 이미 이를 구현하고 있습니다. 회원가입 직후 등에서 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login`의 두 번째 인자는 "로그인 상태 유지" 여부를 의미합니다.

```php
Auth::login($user, $remember = true);
```

가드 지정도 가능합니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증

DB의 기본키로 사용자를 인증하려면 `loginUsingId` 메서드를 사용하세요. 인자로는 인증할 사용자의 기본키를 넘깁니다.

```php
Auth::loginUsingId(1);
```

두 번째 인자로 `remember` 값을 넘겨 "로그인 상태 유지" 기능 제어도 가능합니다.

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 인증

`once` 메서드를 사용하면 세션/쿠키 없이 한 번의 요청에만 제한적으로 사용자 인증을 할 수 있습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 구현 없이 빠르게 인증 기능을 적용할 수 있도록 해줍니다. 시작하려면 `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 라우트에 연결하세요. 프레임워크에 기본 제공되므로 따로 등록할 필요 없습니다.

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth.basic');
```

미들웨어가 연결되면 해당 라우트에 접근 시 브라우저에서 자격 증명 입력 창이 자동으로 뜹니다. 기본적으로 `users` 테이블의 `email` 칼럼이 "아이디"로 사용됩니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고 사항

PHP FastCGI와 Apache로 Laravel을 서비스 중이라면 HTTP Basic 인증이 제대로 동작하지 않을 수 있습니다. 이 때는 `.htaccess` 파일에 다음 줄을 추가합니다.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 무상태 HTTP Basic 인증

세션에 사용자 식별 쿠키를 저장하지 않고 HTTP Basic 인증을 사용할 수도 있습니다. 이는 API 등에서 HTTP Basic 인증을 사용할 때 주로 유용합니다. 이를 위해 [미들웨어](/docs/{{version}}/middleware)를 정의하고, 이 미들웨어에서 `onceBasic` 메서드를 사용하세요.

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

이 미들웨어를 라우트에 연결하면 됩니다.

```php
Route::get('/api/user', function () {
    // 인증된 사용자만
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃

사용자를 수동으로 로그아웃할 때는 `Auth` 파사드의 `logout` 메서드를 사용합니다. 사용자 세션에서 인증 정보를 제거해 이후 요청에 인증이 적용되지 않게 합니다.

그리고 로그아웃 시 세션 무효화 및 [CSRF 토큰](/docs/{{version}}/csrf) 재생성을 권장합니다. 일반적으로는 로그아웃 후 루트로 리다이렉트합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 사용자 로그아웃
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

Laravel은 사용자가 비밀번호를 변경할 때 현재 기기 외의 다른 기기에서 활성화된 모든 세션을 무효화하는 기능도 제공합니다.

이를 활용하려면 먼저 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증이 필요한 라우트에 포함되어야 합니다. 보통 라우트 그룹에 이 미들웨어를 지정하는 방식으로 사용합니다. 디폴트로는 `auth.session` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)으로 등록되어 있습니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 후, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 현재 비밀번호 확인이 필수입니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

이 메서드가 호출되면, 사용자의 다른 모든 세션이(다른 가드 포함) 완전히 무효화되어 "로그아웃" 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션에서 특정 액션(민감한 작업 등)을 하기 전, 사용자의 비밀번호를 다시 한 번 확인해야 할 때가 있습니다. Laravel은 이를 위한 내장 미들웨어를 제공합니다. 구현을 위해서는 비밀번호 확인 뷰를 보여주는 라우트와, 비밀번호 유효성 검증 및 리다이렉션을 담당하는 라우트가 필요합니다.

> [!NOTE]  
> 아래 설명은 Laravel의 비밀번호 확인 기능을 직접 통합하는 법입니다. 더 빠른 시작이 필요하다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)에도 지원이 포함되어 있습니다.

<a name="password-confirmation-configuration"></a>
### 설정

사용자가 비밀번호를 확인한 뒤, 3시간 동안은 다시 묻지 않습니다. 이 시간은 `config/auth.php`의 `password_timeout` 값을 변경해 조정 가능합니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

우선 사용자에게 비밀번호를 물어볼 폼을 보여주는 라우트를 만듭니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

해당 뷰에는 반드시 `password` 필드가 포함되어야 하며, 사용자가 민감한 영역에 접근한다는 안내 문구도 달 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, "비밀번호 확인" 폼의 제출을 처리하는 라우트를 만듭니다. 이 라우트는 비밀번호 유효성 검증 후, 사용자를 원래 목적지로 보내는 역할을 합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['입력하신 비밀번호가 일치하지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

위 라우트에서는, 입력한 비밀번호가 현재 인증 사용자의 비밀번호와 일치하는지 확인합니다. 유효하면, 세션에 "password confirmed" 타임스탬프를 저장하고, 원하는 위치로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호하기

최근 비밀번호 확인이 필요한 라우트에는 반드시 `password.confirm` 미들웨어를 추가하세요. 이 미들웨어는 사용자 목적지를 세션에 저장해, 비밀번호 확인 후 다시 해당 위치로 리다이렉트 할 수 있도록 도와줍니다.

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

`Auth` 파사드의 `extend` 메서드를 이용해 커스텀 인증 가드를 정의할 수 있습니다. [서비스 프로바이더](/docs/{{version}}/providers)에서 이를 등록하세요. 일반적으로 `AppServiceProvider`에 등록하는 예시입니다.

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
     * 모든 애플리케이션 서비스를 부트스트랩합니다.
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

위 예시에서, `extend`의 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 하며, 해당 인터페이스의 메서드를 전부 구현해야 합니다. 커스텀 가드가 정의되면, `auth.php`의 `guards` 설정에 추가할 수 있습니다.

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

HTTP 요청 기반 커스텀 인증을 가장 빠르게 구현하는 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 하나의 클로저로 인증 과정을 정의할 수 있습니다.

`AppServiceProvider`의 `boot` 메서드에서 `Auth::viaRequest`를 호출하세요. 첫 번째 인자로 드라이버 이름(아무 문자열 가능), 두 번째 인자로는 요청을 받아 사용자 인스턴스 또는 인증 실패 시 `null`을 반환하는 클로저를 넘깁니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 모든 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

이후 `auth.php`의 `guards` 설정에 드라이버 이름을 추가하면 됩니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 인증 미들웨어를 이용해 가드를 적용할 수 있습니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 제공자 추가

관계형 데이터베이스(전통적 DB)를 사용자 저장으로 사용하지 않는 경우, 별도의 사용자 제공자(User Provider)를 직접 구현해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 등록합니다. 반환값은 `Illuminate\Contracts\Auth\UserProvider` 인터페이스를 구현해야 합니다.

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
     * 서비스 부트스트랩
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

등록 후, `auth.php` 설정에서 신규 드라이버로 provider를 정의하세요.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로 guards 설정에서도 이 provider를 사용하도록 지정할 수 있습니다.

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 영구 저장소(MySQL, MongoDB 등)에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오고, 인증을 지원합니다. 이 두 인터페이스 덕분에 사용자 데이터 저장 방식/ORM/클래스 종류와 관계없이 인증 시스템이 잘 동작할 수 있습니다.

계약 인터페이스를 살펴보면:

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

- `retrieveById`: 주로 DB의 기본키 등 식별자를 받아 일치하는 사용자를 반환합니다.
- `retrieveByToken`: 고유 식별자와 "remember me" 토큰으로 사용자를 반환합니다.
- `updateRememberToken`: 사용자 인스턴스의 remember_token을 갱신합니다.
- `retrieveByCredentials`: `Auth::attempt`에 받은 자격 정보를 바탕으로 저장소에서 사용자를 조회합니다(비밀번호 검증/인증은 하지 않음).
- `validateCredentials`: 전달받은 사용자와 자격 정보를 비교해 패스워드 일치 여부를 반환합니다.
- `rehashPasswordIfRequired`: 필요하다면 비밀번호를 재해시(리해싱)합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

UserProvider의 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`는 이 인터페이스 구현체를 반환합니다.

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

- `getAuthIdentifierName`: 사용자의 고유키 컬럼명 반환(MySQL 기본키 등)
- `getAuthIdentifier`: 해당 키 값 반환
- `getAuthPasswordName`: 패스워드 컬럼명 반환
- `getAuthPassword`: 해시된 비밀번호 반환

이 인터페이스 덕분에 인증 시스템은 저장 방식이나 ORM에 관계없이 동작할 수 있습니다. Laravel은 `app/Models/User` 클래스를 기본으로 제공합니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱

Laravel의 기본 비밀번호 해시 알고리즘은 bcrypt 입니다. bcrypt의 "work factor"는 `config/hashing.php` 혹은 `BCRYPT_ROUNDS` 환경변수로 조절합니다.

보통 CPU/GPU 처리 속도 증가에 맞춰 work factor를 조금씩 늘려야 합니다. 만약 work factor를 올려야 한다면, 사용자가 인증할 때 마다 Laravel이 자동으로 비밀번호를 재해싱합니다(스타터 키트/수동 인증 attempt 모두).

이 자동 비밀번호 재해싱은 애플리케이션에 영향을 주지 않지만, 원치 않을 경우 아래처럼 설정을 꺼둘 수 있습니다.

```shell
php artisan config:publish hashing
```

발행된 설정 파일에서 아래 옵션을 비활성화하세요.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트(Events)

Laravel은 인증 과정 중 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 원하는 이벤트에 대해 [리스너](/docs/{{version}}/events)를 정의할 수 있습니다.

<div class="overflow-auto">

| 이벤트 명칭 |
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
