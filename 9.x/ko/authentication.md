# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [생태계 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치하기](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증](#http-basic-authentication)
    - [상태 비저장 HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호하기](#password-confirmation-protecting-routes)
- [커스텀 가드 추가하기](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가하기](#adding-custom-user-providers)
    - [사용자 프로바이더 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [소셜 인증](/docs/9.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자들이 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 이 기능을 구현하는 일은 복잡하고 잠재적으로 위험할 수 있습니다. 이러한 이유로 Laravel은 빠르고 안전하며 쉽게 인증 기능을 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 서비스는 기본적으로 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자가 어떻게 인증되는지 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용하는 기본 `session` 가드를 포함합니다.

프로바이더는 사용자를 영구 저장소에서 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/9.x/eloquent)와 데이터베이스 쿼리 빌더를 사용하여 사용자를 조회하는 기능을 기본 지원합니다. 필요에 따라 애플리케이션에 맞는 추가 프로바이더를 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 있습니다. 이 파일에는 Laravel 인증 서비스 동작을 조정할 수 있는 여러 잘 설명된 옵션이 포함되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(roles)" 및 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통한 사용자 액션 인가에 대해 더 알고 싶다면 [authorization](/docs/9.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트 (Starter Kits)

빠르게 시작하고 싶으세요? 새 Laravel 애플리케이션에서 [Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에서 할당한 다른 URL로 이동하세요. 스타터 키트가 전체 인증 시스템을 자동으로 설정해 줍니다!

**최종 애플리케이션에서 스타터 키트를 사용하지 않더라도, [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze) 스타터 키트를 설치해 보는 것은 실제 Laravel 프로젝트에서 Laravel의 모든 인증 기능이 어떻게 구현되는지 배우는 좋은 기회가 됩니다.** Laravel Breeze는 인증 컨트롤러, 라우트, 뷰를 생성하므로, 이 파일들을 살펴보며 Laravel 인증 기능 구현 방식을 배우실 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

기본적으로 Laravel은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/9.x/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. 애플리케이션에서 Eloquent를 사용하지 않는다면, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 만들 때, 비밀번호 컬럼은 최소 60자 이상이어야 합니다. 물론 새 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이 길이를 초과하는 칼럼을 생성합니다.

또한, `users` 테이블(또는 동등한 테이블)에 100자 길이의 널 가능(nullable) 문자열 타입 `remember_token` 컬럼이 있는지 확인하세요. 이 칼럼은 사용자가 애플리케이션 로그인 시 "로그인 상태 유지(remember me)"를 선택할 때 토큰을 저장하는 용도입니다. 기본 `users` 테이블 마이그레이션에는 이미 이 칼럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 생태계 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기 전에 Laravel 인증 생태계를 간략히 살펴보고 각 패키지의 용도에 대해 살펴보겠습니다.

먼저, 인증이 어떻게 동작하는지 생각해 보면, 웹 브라우저를 사용하는 사용자가 로그인 폼에서 사용자 이름과 비밀번호를 입력합니다. 이 자격 증명이 올바르면 애플리케이션은 인증된 사용자 정보를 사용자 [세션](/docs/9.x/session)에 저장합니다. 브라우저에는 세션 ID가 포함된 쿠키가 발급되어, 후속 요청 시 해당 세션과 사용자를 연결합니다. 세션 쿠키를 받으면 애플리케이션은 세션 ID로 세션 데이터를 조회하고, 세션에 저장된 인증 정보를 확인하여 사용자를 '인증됨' 상태로 간주합니다.

반면 원격 서비스가 API에 접근하기 위해 인증해야 할 경우, 웹 브라우저가 없기 때문에 쿠키를 사용하지 않습니다. 대신, 원격 서비스는 각 요청마다 API 토큰을 전송합니다. 애플리케이션은 유효한 API 토큰 테이블과 대조하여 토큰을 검증하고, 해당 토큰에 연결된 사용자를 "인증"하여 요청을 처리합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 기본 브라우저 인증 서비스

Laravel은 일반적으로 `Auth` 및 `Session` 파사드를 통해 접근하는 내장 인증 및 세션 서비스를 포함합니다. 이 서비스들은 웹 브라우저에서 시작되는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자 자격증명을 확인하고 사용자를 인증하는 메서드를 포함하며, 사용자의 세션에 올바른 인증 데이터를 자동 저장하고 세션 쿠키를 발급합니다. 이 문서에서 이러한 서비스를 사용하는 방법을 설명합니다.

**애플리케이션 스타터 키트**

이 문서에서 다루는 인증 서비스를 수동으로 조작하여 애플리케이션 고유 인증 계층을 만들 수도 있지만, 더 빠르게 시작할 수 있도록 전체 인증 계층을 견고하고 현대적으로 생성해 주는 [무료 패키지들](/docs/9.x/starter-kits)을 제공합니다. 이들은 [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/9.x/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/9.x/fortify)입니다.

_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 인증 기능을 단순하고 최소한으로 구현한 패키지입니다. Breeze의 뷰 계층은 간단한 [Blade 템플릿](/docs/9.x/blade)과 [Tailwind CSS](https://tailwindcss.com)를 사용하여 스타일링되어 있습니다. 시작하려면 Laravel [애플리케이션 스타터 키트](/docs/9.x/starter-kits) 문서를 참고하세요.

_Laravel Fortify_는 헤드리스(백엔드 전용) 인증 백엔드로, 쿠키 기반 인증을 포함해 이 문서에 나온 여러 인증 기능을 구현합니다. Fortify는 Laravel Jetstream의 인증 백엔드로 사용되거나, [Laravel Sanctum](/docs/9.x/sanctum)과 결합해 SPA용 인증 백엔드로 독립 사용될 수 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_은 Laravel Fortify의 인증 서비스를 사용해 아름답고 현대적인 UI를 제공하는 완전한 애플리케이션 스타터 키트입니다. 이것은 [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), 및/또는 [Inertia](https://inertiajs.com)를 사용해 구축됩니다. Jetstream은 이중 인증, 팀 지원, 브라우저 세션 관리, 프로필 관리, [Laravel Sanctum](/docs/9.x/sanctum)과의 통합을 통한 API 토큰 인증 등을 지원합니다. API 인증에 대한 자세한 내용은 아래를 참조하세요.

<a name="laravels-api-authentication-services"></a>
#### Laravel API 인증 서비스

Laravel은 API 토큰 관리와 API 토큰을 사용한 요청 인증을 지원하는 선택적 패키지 두 가지를 제공합니다: [Passport](/docs/9.x/passport)와 [Sanctum](/docs/9.x/sanctum). 이들 라이브러리와 Laravel 내장 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 두 라이브러리는 주로 API 토큰 인증에 집중하고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션이 Laravel 내장 쿠키 인증과 API 인증 패키지 중 하나를 함께 사용합니다.

**Passport**

Passport는 OAuth2 인증 프로바이더로, 다양한 OAuth2 "grant types"를 지원해 여러 종류의 토큰을 발급할 수 있습니다. 일반적으로 API 인증용으로 견고하지만 복잡한 패키지입니다. 대부분 애플리케이션은 OAuth2 사양이 제공하는 복잡한 기능을 필요로 하지 않으며, OAuth2 인증 제공자 사용에 대해 개발자들이 혼란을 겪기도 합니다.

**Sanctum**

OAuth2 복잡성과 개발자 혼란에 대응해, 더 간단하고 직관적인 인증 패키지를 개발하였습니다. 이는 웹 브라우저의 1차 요청과 API 토큰을 이용한 API 요청 모두 처리할 수 있습니다. 이 목표는 [Laravel Sanctum](/docs/9.x/sanctum)을 통해 실현되었습니다. Sanctum은 SPA가 백엔드 Laravel 애플리케이션과 인증하거나, 모바일 클라이언트를 제공하는 애플리케이션에 권장되는 인증 패키지입니다.

Laravel Sanctum은 웹 요청과 API 요청을 모두 처리하는 하이브리드 인증 패키지입니다. Sanctum 기반 애플리케이션이 요청을 받으면, 먼저 세션 쿠키를 확인해 인증된 세션이 있는지 조회합니다. 이때 Laravel 내장 인증 서비스를 호출합니다. 만약 세션 쿠키로 인증되지 않으면, 요청에서 API 토큰을 찾고 이를 통해 인증합니다. 자세한 동작 원리는 Sanctum의 ["how it works"](/docs/9.x/sanctum#how-it-works) 문서를 참고하세요.

Laravel Sanctum은 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 키트에 포함된 API 패키지로, 대부분 웹 애플리케이션에 가장 적합하다고 생각됩니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

요약하자면, 애플리케이션이 브라우저를 이용하고 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 사용합니다.

API를 외부에 제공하는 경우, API 토큰 인증을 위해 [Passport](/docs/9.x/passport) 또는 [Sanctum](/docs/9.x/sanctum)을 선택합니다. 보통 Sanctum이 더 간단하고 완전한 API, SPA, 모바일 인증 솔루션이며 "스코프" 또는 "능력" 지원도 하므로 권장됩니다.

SPA를 Laravel 백엔드로 구축한다면 [Laravel Sanctum](/docs/9.x/sanctum)을 사용하세요. 이 경우 자체 백엔드 인증 라우트를 직접 구현하거나 [Laravel Fortify](/docs/9.x/fortify)를 헤드리스 인증 백엔드로 활용해 회원가입, 비밀번호 재설정, 이메일 확인 등의 라우트와 컨트롤러를 사용할 수 있습니다.

OAuth2 사양의 모든 기능이 반드시 필요하다면 Passport를 선택할 수 있습니다.

빠르게 시작하고 싶다면, Laravel의 내장 인증과 Laravel Sanctum 조합으로 구성된 인증 스택을 사용하는 [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze) 설치를 권합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 문서 부분은 인증 스타터 키트(/docs/9.x/starter-kits)를 이용한 사용자 인증 방법을 다룹니다. 인증 UI가 포함되어 있어 빠르게 시작할 수 있습니다. Laravel 인증 시스템을 직접 통합하려면 [수동 사용자 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치하기 (Install A Starter Kit)

먼저 [Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits)를 설치하세요. 현재의 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 인증 기능을 새 Laravel 애플리케이션에 통합하기 위한 멋진 출발점입니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel 인증 기능을 최소, 간단하게 구현합니다. Breeze 뷰 계층은 간단한 [Blade 템플릿](/docs/9.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. Vue 또는 React 기반의 [Inertia](https://inertiajs.com) 스캐폴딩도 제공합니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 [Livewire](https://laravel-livewire.com), 또는 [Inertia와 Vue](https://inertiajs.com)를 사용한 스캐폴딩을 제공하는 더 강력한 애플리케이션 스타터 키트입니다. 선택적 이중 인증, 팀 기능, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/9.x/sanctum) API 지원, 계정 삭제 등의 기능도 포함합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기 (Retrieving The Authenticated User)

인증 스타터 키트를 설치하고 사용자가 애플리케이션에 회원가입하고 인증할 수 있게 하면, 현재 인증된 사용자와 상호작용해야 합니다. 들어오는 요청을 처리할 때, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회...
$user = Auth::user();

// 현재 인증된 사용자 ID 조회...
$id = Auth::id();
```

또한, 사용자 인증 후 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 접근할 수도 있습니다. Laravel은 타입힌팅된 클래스들을 자동 주입하므로, 컨트롤러 메서드에서 `Illuminate\Http\Request` 객체를 타입힌팅해 요청의 `user` 메서드를 통해 인증 사용자에 편리하게 접근할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보 업데이트
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        // $request->user()
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
#### 현재 사용자가 인증되었는지 확인하기

요청을 하는 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하세요. 사용자가 인증되었으면 `true`를 반환합니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있음...
}
```

> [!NOTE]
> `check` 메서드로 인증 상태를 확인할 수 있지만, 일반적으로는 미들웨어를 사용해 특정 라우트/컨트롤러 접근 전에 사용자가 인증되었는지 검증합니다. 자세한 내용은 [라우트 보호하기](/docs/9.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

[라우트 미들웨어](/docs/9.x/middleware)를 사용해 인증된 사용자만 특정 라우트에 접근하도록 할 수 있습니다. Laravel은 기본적으로 `auth` 미들웨어를 제공합니다. 이 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조합니다. 이 미들웨어는 애플리케이션의 HTTP 커널에 이미 등록되어 있으므로, 라우트 정의에 미들웨어만 붙이면 됩니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있음...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉트하기

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 사용자를 `login` [네임드 라우트](/docs/9.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 애플리케이션의 `app/Http/Middleware/Authenticate.php` 파일 내 `redirectTo` 함수 수정으로 변경할 수 있습니다:

```
/**
 * 사용자를 리다이렉트할 경로를 반환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return string
 */
protected function redirectTo($request)
{
    return route('login');
}
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 붙일 때, 사용자를 인증하는 데 사용할 가드를 지정할 수도 있습니다. 지정된 가드는 `auth.php` 설정 파일 내 `guards` 배열 키 중 하나와 일치해야 합니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있음...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

Laravel Breeze 또는 Laravel Jetstream [스타터 키트](/docs/9.x/starter-kits)를 사용할 경우, 로그인 시도에 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본적으로 여러 번 로그인 실패 시, 1분 동안 로그인을 시도할 수 없습니다. 제한은 사용자 이름/이메일과 IP 주소 조합 별로 적용됩니다.

> [!NOTE]
> 애플리케이션 내 다른 라우트에 속도 제한을 적용하려면 [속도 제한 문서](/docs/9.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

Laravel [애플리케이션 스타터 키트](/docs/9.x/starter-kits)의 인증 스캐폴딩을 사용하지 않아도 됩니다. 만약 사용하지 않는다면, Laravel 인증 클래스를 직접 사용해 사용자 인증을 관리해야 합니다. 걱정하지 마세요, 생각보다 쉽습니다!

여기서는 `Auth` [파사드](/docs/9.x/facades)를 사용해 Laravel 인증 서비스를 접근합니다. 따라서 클래스 상단에 `Auth` 파사드 임포트를 잊지 마세요. 다음으로 `attempt` 메서드를 살펴봅니다. `attempt`는 일반적으로 애플리케이션 로그인 폼의 인증 시도를 처리하는 데 사용됩니다. 인증에 성공하면 세션 고정(session fixation)을 방지하기 위해 사용자의 [세션](/docs/9.x/session)을 재생성해야 합니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * 인증 시도 처리
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function authenticate(Request $request)
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

`attempt` 메서드는 첫 번째 인자로 키/값 배열을 받습니다. 배열 값들은 데이터베이스에서 사용자를 조회하는 데 쓰입니다. 위 예제에선 `email` 컬럼 값으로 사용자를 찾습니다. 사용자가 조회되면, 데이터베이스에 저장된 해시된 비밀번호와 배열 안의 `password` 값을 비교합니다. 요청으로 받은 `password`는 직접 해시처리하지 마세요. Laravel이 내부에서 자동으로 해시 처리해 비교합니다. 두 해시가 일치하면 사용자의 인증 세션이 시작됩니다.

Laravel 인증 서비스는 설정된 인증 가드의 "프로바이더" 설정에 따라 데이터베이스에서 사용자를 조회합니다. 기본 `config/auth.php` 구성에는 Eloquent 사용자 프로바이더가 지정되어 있고 `App\Models\User` 모델을 사용하도록 되어 있습니다. 필요에 따라 구성 파일에서 이를 변경할 수 있습니다.

`attempt` 메서드는 인증에 성공하면 `true`, 실패하면 `false`를 반환합니다.

Laravel 리디렉터의 `intended` 메서드는 인증 미들웨어 때문에 가로챈 이전 요청 URL로 리다이렉트합니다. 기본값으로 대체할 URI도 줄 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 명시하기

원한다면, 사용자 이메일과 비밀번호 외에 인증 쿼리에 추가 조건을 넣을 수 있습니다. `attempt` 메서드에 넘겨주는 배열에 추가 조건을 넣으면 됩니다. 예를 들어, 사용자가 활성 상태(`active` 컬럼이 1인지)를 확인할 수 있습니다:

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

복잡한 조건은 클로저로 정의할 수도 있습니다. 클로저는 쿼리 인스턴스를 받아 애플리케이션 요구에 따라 쿼리를 커스터마이징할 수 있습니다:

```
if (Auth::attempt([
    'email' => $email, 
    'password' => $password, 
    fn ($query) => $query->has('activeSubscription'),
])) {
    // 인증 성공...
}
```

> [!WARNING]
> 여기서 `email`은 필수 옵션이 아닙니다. 단지 예시일 뿐이며, 데이터베이스 "사용자 이름"에 해당하는 컬럼명을 사용하세요.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아 잠재적 사용자를 더 자세히 검사한 후 인증 여부를 결정할 수 있습니다. 클로저 인자는 대상 사용자이며, `true` 또는 `false`를 반환해 인증 여부를 나타냅니다:

```
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function ($user) {
    return $user->isNotBanned();
})) {
    // 인증 성공...
}
```

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근하기

`Auth` 파사드의 `guard` 메서드로 사용할 가드 인스턴스를 지정할 수 있습니다. 이 기능으로 애플리케이션 내 서로 다른 부분을 서로 다른 인증 가능한 모델이나 사용자 테이블로 관리할 수 있습니다.

`guard`에 넘기는 이름은 `auth.php` 설정 파일 내 `guards` 배열의 키 중 하나여야 합니다:

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹 애플리케이션은 로그인 폼에 "로그인 상태 유지" 체크박스를 제공합니다. 이 기능을 구현하려면 `attempt` 메서드 두 번째 인자로 `true` 또는 `false` 불리언 값을 넘기면 됩니다.

`true`일 경우, Laravel은 사용자를 무기한 인증 상태로 유지하거나 사용자가 직접 로그아웃할 때까지 인증을 유지합니다. 이를 위해 `users` 테이블에 문자열 타입 `remember_token` 칼럼이 있어야 하며, 새 Laravel 애플리케이션의 기본 마이그레이션에 이미 포함되어 있습니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억되고 있음...
}
```

"로그인 상태 유지" 기능을 제공하면, `viaRemember` 메서드로 현재 인증 사용자가 remember me 쿠키로 인증됐는지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증하기

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 지정하려면, `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 넘기면 됩니다. 이 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [인터페이스](/docs/9.x/contracts)를 구현해야 합니다. Laravel에 기본 포함된 `App\Models\User` 모델은 이미 이를 구현합니다. 이 방법은 예컨대 사용자가 회원가입 직후와 같이, 이미 유효한 사용자 인스턴스가 있을 때 유용합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 두 번째 인자로 `true` 또는 `false` 불리언을 넘겨 "로그인 상태 유지" 기능을 활성화할 수도 있습니다. 이 값이 `true`면 세션이 무기한 인증 상태를 유지하거나 사용자가 명시적 로그아웃할 때까지 유지됩니다:

```
Auth::login($user, $remember = true);
```

필요하다면, `login` 호출 전에 인증 가드를 지정할 수도 있습니다:

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증하기

사용자 데이터베이스 주요 키로 사용자를 인증하려면 `loginUsingId` 메서드를 사용합니다. 이 메서드는 인증할 사용자의 기본 키를 받습니다:

```
Auth::loginUsingId(1);
```

두 번째 인자로 불리언을 넘겨 로그인 상태 유지 기능을 제어할 수 있습니다:

```
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
#### 일회성 인증 (Authenticate A User Once)

`once` 메서드는 세션이나 쿠키 없이 단일 요청에 대해 사용자를 인증할 때 씁니다:

```
if (Auth::once($credentials)) {
    //
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 로그인 페이지 없이 애플리케이션 사용자를 인증하는 빠른 방법입니다. 시작하려면 라우트에 `auth.basic` [미들웨어](/docs/9.x/middleware)를 붙이세요. 이 미들웨어는 Laravel에 내장되어 있어 추가 정의가 필요 없습니다:

```
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있음...
})->middleware('auth.basic');
```

라우트에 미들웨어를 붙이면 브라우저에서 라우트에 접근 시 자동으로 자격 증명 입력을 요구합니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자 이름으로 가정합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 주의사항

PHP FastCGI와 Apache를 함께 사용할 경우 HTTP 기본 인증이 제대로 작동하지 않을 수 있습니다. 해결하려면 애플리케이션 `.htaccess` 파일에 다음 줄을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 상태 비저장 HTTP 기본 인증 (Stateless HTTP Basic Authentication)

세션에 사용자 식별 쿠키를 설정하지 않고 HTTP 기본 인증을 사용할 수도 있습니다. 주로 API 인증에 HTTP 인증을 쓰려 할 때 유용합니다. 이를 위해 `onceBasic` 메서드를 호출하는 미들웨어를 정의하세요. `onceBasic`이 응답을 반환하지 않으면 요청을 애플리케이션 내부로 넘깁니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Support\Facades\Auth;

class AuthenticateOnceWithBasicAuth
{
    /**
     * 들어오는 요청 처리
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, $next)
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

이후 [라우트 미들웨어 등록](/docs/9.x/middleware#registering-middleware) 후 라우트에 붙이세요:

```
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있음...
})->middleware('auth.basic.once');
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

애플리케이션에서 사용자를 수동으로 로그아웃시키려면 `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 세션에서 인증 정보를 제거해 이후 요청이 인증되지 않게 합니다.

`logout` 호출에 더해 세션 무효화와 [CSRF 토큰](/docs/9.x/csrf) 재생성이 권장됩니다. 로그아웃 후에는 보통 홈페이지로 리다이렉트합니다:

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션에서 사용자 로그아웃 처리
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function logout(Request $request)
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
### 다른 기기 세션 무효화 (Invalidating Sessions On Other Devices)

Laravel은 현재 기기의 세션은 유지하면서, 사용자가 다른 기기에서 활성화한 세션만 무효화하고 로그아웃시키는 기능도 제공합니다. 보통 사용자가 비밀번호를 변경할 때, 다른 기기 세션을 무효화하면서 현재 기기 인증은 유지할 때 사용합니다.

먼저, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증이 필요한 라우트에 포함되어 있는지 확인하세요. 보통 라우트 그룹에 한 번만 적용합니다. 기본적으로 `auth.session` 키로 HTTP 커널에 등록되어 있습니다:

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

이후 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 사용자가 현재 비밀번호를 입력해 확인하는 과정을 필요로 하므로, 애플리케이션에서 별도의 입력 폼을 구현해야 합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 호출 시 사용자의 다른 모든 세션이 완전히 무효화되어, 이전에 인증된 모든 가드가 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 개발하면서, 특정 작업을 수행하거나 민감 영역에 접근하기 전에 사용자가 비밀번호를 재확인해야 할 때가 있습니다. Laravel은 이를 간단히 구현할 수 있는 미들웨어를 내장하고 있습니다. 이를 구현하려면, 비밀번호 확인 폼을 보여주는 라우트와 비밀번호가 유효한지 확인하고 사용자를 의도한 목적지로 리다이렉트하는 라우트 두 개를 정의해야 합니다.

> [!NOTE]
> 아래 문서는 Laravel 비밀번호 확인 기능을 직접 통합하는 방법입니다. 빠르게 시작하려면 [Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits)에서 기본 지원 기능을 활용하세요.

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

비밀번호를 한 번 확인하면 기본적으로 3시간 동안 다시 확인을 요구하지 않습니다. 이 시간을 변경하려면 애플리케이션 `config/auth.php` 설정 파일 내 `password_timeout` 값을 조정하세요.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저 비밀번호 확인을 요청하는 뷰를 보여주는 라우트를 정의합니다:

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트가 반환하는 뷰는 `password` 필드가 포함된 폼이어야 합니다. 또한 사용자가 보호된 영역에 진입하려 한다는 등의 설명 문구를 포함해도 좋습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음은 "비밀번호 확인" 뷰에서 제출된 폼 요청을 처리할 라우트입니다. 비밀번호가 유효한지 확인해, 유효하면 사용자를 의도한 목적지로 리다이렉트합니다:

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

루트를 더 자세히 보면, 먼저 요청 `password` 값이 인증된 사용자의 실제 비밀번호와 일치하는지 확인합니다. 비밀번호가 유효하면 Laravel 세션에 사용자가 비밀번호를 확인했다는 타임스탬프를 기록합니다(`passwordConfirmed` 메서드). 이후 의도한 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호하기

최근 비밀번호 확인이 필요한 작업을 수행하는 라우트에는 `password.confirm` 미들웨어를 반드시 지정해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 사용자의 의도 목적지를 세션에 자동 저장하고, 비밀번호 확인이 필요하면 `password.confirm` [네임드 라우트](/docs/9.x/routing#named-routes)로 리다이렉트합니다:

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

`Auth` 파사드의 `extend` 메서드를 사용해 직접 인증 가드를 정의할 수 있습니다. 보통 [서비스 프로바이더](/docs/9.x/providers) 내에서 호출합니다. Laravel은 기본적으로 `AuthServiceProvider`를 제공하니, 이곳에 코드를 작성하시면 됩니다:

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 인증/인가 서비스를 등록합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::extend('jwt', function ($app, $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 구현체를 반환...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

예제에서 보듯, `extend`에 넘기는 콜백은 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 이 인터페이스는 커스텀 가드를 정의할 때 구현해야 하는 몇 가지 메서드를 포함합니다. 커스텀 가드를 정의한 뒤에는 `auth.php` 설정의 `guards` 배열에서 가드를 참조할 수 있습니다:

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

가장 간단한 맞춤 HTTP 요청 기반 인증 시스템 구현 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드는 단일 클로저로 인증 과정을 빠르게 정의하게 해줍니다.

`AuthServiceProvider`의 `boot` 메서드 내에서 `Auth::viaRequest`를 호출하세요. 첫 번째 인자는 커스텀 가드 이름이며, 두 번째 인자는 HTTP 요청을 받고 사용자 인스턴스 또는 인증 실패 시 `null`을 반환하는 클로저입니다:

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션 인증/인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

이 맞춤 인증 드라이버를 정한 뒤 `auth.php` 설정 `guards` 내 드라이버로 지정할 수 있습니다:

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

나중에 미들웨어에 가드를 지정하여 라우트에 연결하세요:

```
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가하기 (Adding Custom User Providers)

관계형 데이터베이스를 사용하지 않고 사용자 정보를 관리한다면, Laravel 인증을 확장해 자체 인증 사용자 프로바이더를 만들어야 합니다. `Auth` 파사드의 `provider` 메서드를 사용하며, 반환 값은 `Illuminate\Contracts\Auth\UserProvider` 인터페이스 구현체여야 합니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 인증/인가 서비스 등록
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::provider('mongo', function ($app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 구현체 반환...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider` 메서드로 프로바이더를 등록한 뒤, `auth.php` 설정 파일에서 새 사용자 프로바이더로 전환할 수 있습니다. 먼저 새 드라이버를 사용하는 프로바이더를 정의합니다:

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로, `guards` 설정에서 이 프로바이더를 참조합니다:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등 영구 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스는 데이터 저장 방식이나 사용자 객체 종류에 관계없이 인증 시스템이 작동하게 해줍니다.

`Illuminate\Contracts\Auth\UserProvider` 인터페이스는 다음과 같습니다:

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

- `retrieveById`는 사용자의 고유 키(예: MySQL 자동 증가 ID)를 받아 해당하는 `Authenticatable` 구현체를 반환합니다.
- `retrieveByToken`은 고유 식별자와 "로그인 상태 유지" 토큰을 이용해 사용자를 조회합니다.
- `updateRememberToken`은 `$user` 인스턴스의 `remember_token`을 새 토큰으로 갱신합니다. 토큰은 "remember me" 인증 성공 시나 로그아웃 시 새로 할당됩니다.
- `retrieveByCredentials`는 `Auth::attempt` 호출 시 넘긴 자격증명 배열을 받아, 저장소에서 이를 만족하는 사용자 레코드를 조회해 `Authenticatable` 구현체를 반환합니다. 일반적으로 `username` 같은 컬럼값 조건으로 쿼리를 수행합니다. 이 함수는 비밀번호 인증을 수행하면 안 됩니다.
- `validateCredentials`는 `$user`와 `$credentials`를 비교해 사용자를 인증합니다. 보통 이 메서드에서 `Hash::check`로 비밀번호를 비교합니다. 결과로 `true` 또는 `false`를 반환합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약 (The Authenticatable Contract)

위 `UserProvider` 메서드들이 반환하는 객체는 `Authenticatable` 인터페이스를 구현해야 합니다:

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

이 인터페이스는 간단합니다. `getAuthIdentifierName`은 사용자의 "기본 키" 필드명을 반환하고, `getAuthIdentifier`는 기본 키 값을 반환합니다. MySQL 백엔드라면 보통 자동 증가하는 주요 키입니다. `getAuthPassword`는 사용자의 해시된 비밀번호를 반환합니다.

이 인터페이스를 통해 어떤 ORM이나 저장소를 쓰든 상관없이 Laravel 인증 시스템이 작동합니다. Laravel 기본값으로 `app/Models/User` 클래스가 이 인터페이스를 구현하고 있습니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정 중 다양한 [이벤트](/docs/9.x/events)를 발생시키며, 이를 `EventServiceProvider`에 리스너로 연결할 수 있습니다:

```
/**
 * 애플리케이션 이벤트 리스너 매핑
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