# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [생태계 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증](#http-basic-authentication)
    - [상태 비저장 HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기에서 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가하기](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가하기](#adding-custom-user-providers)
    - [사용자 프로바이더 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 이 기능을 구현하는 것은 복잡하고 잠재적으로 위험할 수 있습니다. 이런 이유로 Laravel은 인증을 빠르고, 안전하며, 쉽게 구현할 수 있도록 필요한 도구를 제공하는 데 중점을 둡니다.

Laravel 인증의 핵심은 "가드(guards)"와 "프로바이더(providers)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용하여 상태를 유지하는 `session` 가드를 기본으로 제공합니다.

프로바이더는 저장소에서 사용자를 어떻게 가져올지 정의합니다. Laravel은 [Eloquent](/docs/{{version}}/eloquent) 및 데이터베이스 쿼리 빌더를 사용하여 사용자를 검색하는 기능을 기본 지원합니다. 하지만 필요에 따라 추가 프로바이더를 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치하며, Laravel 인증 서비스 동작을 조정할 수 있는 여러 잘 문서화된 옵션을 포함하고 있습니다.

> [!TIP]
> 가드와 프로바이더는 "역할(roles)"과 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통해 사용자 작업을 인가하는 방법에 대해 더 알고 싶다면 [인가(authorization)](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트 (Starter Kits)

빠르게 시작하고 싶나요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, `/register` 같은 애플리케이션에 지정된 URL로 브라우저를 열면 스타터 키트가 전체 인증 시스템을 자동으로 구성해줍니다!

**최종 애플리케이션에 스타터 키트를 사용하지 않더라도, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 스타터 키트를 설치하면 실제 Laravel 프로젝트에서 Laravel 인증 기능을 어떻게 구현하는지 배우기에 아주 좋은 기회가 됩니다.** Laravel Breeze는 인증용 컨트롤러, 라우트, 뷰를 생성하므로, 생성된 코드를 통해 Laravel 인증 구현 방식을 살펴볼 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

기본적으로 Laravel은 `app/Models` 디렉토리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함하며, 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용됩니다. Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다.

`App\Models\User` 모델의 데이터베이스 스키마를 설계할 때는, 비밀번호 컬럼이 최소 60자 이상인 문자열이어야 합니다. Laravel 기본 `users` 테이블 마이그레이션은 이미 충분히 긴 컬럼을 생성합니다.

또한 `users` (또는 이에 해당하는) 테이블에 100자 길이의 nullable한 문자열형 `remember_token` 컬럼이 있어야 하며, 이는 사용자가 로그인 시 "나를 기억하기" 옵션을 선택했을 때 사용할 토큰을 저장합니다. 기본 Laravel `users` 테이블 마이그레이션에는 이 컬럼이 기본 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 생태계 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기 전에 Laravel 인증 생태계를 개괄하고 각 패키지의 용도를 설명하겠습니다.

먼저, 인증이 어떻게 작동하는지 고려해보면, 웹 브라우저를 사용하는 경우 사용자는 로그인 폼을 통해 사용자 이름과 비밀번호를 입력합니다. 자격 증명이 올바르면 애플리케이션은 인증된 사용자 정보를 사용자의 [세션](/docs/{{version}}/session)에 저장합니다. 브라우저에 보내진 쿠키에는 세션 ID가 들어 있고, 이후 요청마다 이 세션 ID를 통해 사용자를 식별합니다. 세션 쿠키를 받으면 애플리케이션은 세션 데이터를 조회하고 인증 정보가 세션에 저장되었다는 사실을 인지하여 사용자를 "인증된" 상태로 간주합니다.

원격 서비스가 API에 접근하기 위해 인증해야 할 때는 브라우저가 없으므로 쿠키를 사용하지 않고, 대신 각 요청마다 API 토큰을 전송합니다. 애플리케이션은 이 토큰을 유효한 토큰 목록과 대조하여 요청을 수행하는 사용자를 인증합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 내장 브라우저 인증 서비스

Laravel은 주로 `Auth`와 `Session` 파사드를 통해 액세스하는 내장 인증 및 세션 서비스를 포함합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자 자격 증명을 검증하고 인증하는 메서드를 제공하며, 인증 데이터는 자동으로 세션에 저장되고 세션 쿠키도 발급됩니다. 이 문서에서 이러한 서비스 사용법을 설명합니다.

**애플리케이션 스타터 키트**

본 문서에서 다룬 대로, 이 인증 서비스를 수동으로 다룰 수도 있지만, 더 빠르게 시작할 수 있도록 전체 인증 계층을 튼튼하게 구축하는 [무료 패키지 / 스타터 키트](/docs/{{version}}/starter-kits)를 제공합니다. 대표적으로 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/{{version}}/starter-kits#laravel-jetstream) 그리고 [Laravel Fortify](/docs/{{version}}/fortify)가 있습니다.

- _Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 확인, 비밀번호 확인 등 모든 인증 기능을 최소한으로 구현한 패키지입니다. 뷰 레이어는 간단한 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. [애플리케이션 스타터 키트 문서](/docs/{{version}}/starter-kits)에서 시작 방법을 확인하세요.

- _Laravel Fortify_는 Laravel를 위한 헤드리스(뷰 미포함) 인증 백엔드로, 쿠키 기반 인증뿐 아니라 2단계 인증과 이메일 확인 같은 기능도 포함합니다. Fortify는 Laravel Jetstream의 인증 백엔드로 사용되거나, [Laravel Sanctum](/docs/{{version}}/sanctum)과 함께 SPA 인증을 위해 독립적으로도 사용 가능합니다.

- _[Laravel Jetstream](https://jetstream.laravel.com)_은 Laravel Fortify 인증 서비스를 활용하여 아름답고 현대적인 UI를 제공하는 강력한 스타터 키트입니다. UI는 [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), 또는 [Inertia.js](https://inertiajs.com) 기반입니다. 2단계 인증, 팀 지원, 브라우저 세션 관리, 프로필 관리, 그리고 API 인증을 위해 [Laravel Sanctum](/docs/{{version}}/sanctum)과의 통합 기능도 제공합니다. API 인증 옵션에 대해서는 아래에서 더 다룹니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리 및 API 토큰 인증 요청 처리를 위한 두 가지 선택적 패키지 [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum)을 제공합니다. 이들 라이브러리와 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 라이브러리들은 API 토큰 인증에 집중하며, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션은 두 가지 방식을 모두 사용합니다.

**Passport**

Passport는 OAuth2 인증 공급자로, 다양한 OAuth2 "grant types"를 통해 여러 종류의 토큰 발급을 지원합니다. 전반적으로 API 인증을 위한 복잡하고 강력한 패키지입니다. 하지만 대부분의 애플리케이션은 OAuth2가 제공하는 복잡한 기능이 필요 없으며, OAuth2 활용법 때문에 사용자와 개발자가 혼란을 겪기도 합니다. 예를 들어, SPA나 모바일 앱을 Passport와 같은 OAuth2 인증 공급자와 연동해 인증하는 방법에 대해 혼란이 있었습니다.

**Sanctum**

OAuth2 복잡성과 개발자 혼란에 대응하여, 단순하고 간결하면서 웹 브라우저 기반의 1차 요청과 API 토큰을 통한 요청을 모두 처리할 수 있는 인증 패키지가 만들어졌습니다. 이것이 바로 [Laravel Sanctum](/docs/{{version}}/sanctum)입니다. Sanctum은 SPA, 모바일 클라이언트, 또는 백엔드와 별도로 존재하는 SPA를 갖는 애플리케이션에 적합한 인증 패키지로 권장됩니다.

Sanctum은 하이브리드 웹/API 인증 패키지입니다. Sanctum 기반 애플리케이션이 요청을 받을 때, 먼저 요청에 인증된 세션을 참조하는 세션 쿠키가 포함되어 있는지 확인합니다. 이것은 앞서 설명한 Laravel 내장 인증 서비스를 활용하여 이루어집니다. 만약 세션 쿠키로 인증되지 않은 경우, 요청에 API 토큰이 있는지 검사하여, 토큰이 있으면 해당 토큰을 통해 인증을 수행합니다. 이 과정은 Sanctum 문서 내 ["how it works"](/docs/{{version}}/sanctum#how-it-works) 내용을 참고하세요.

Laravel Sanctum은 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 키트에 기본 포함되어 있는데, 거의 대부분의 웹 애플리케이션 인증 요구에 가장 잘 맞는 패키지이기 때문입니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택 가이드

요약하자면, 애플리케이션이 브라우저를 통해 접근되고 모놀리식 Laravel 애플리케이션을 구축한다면, Laravel 내장 인증 서비스를 사용합니다.

만약 API를 외부에 제공한다면, API 토큰 인증을 위해 [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum) 중 하나를 선택합니다. 일반적으로, Sanctum이 간단하고 완전한 API 인증, SPA 인증, 모바일 인증 기능(스코프/기능 지원 포함)을 제공하므로 권장됩니다.

SPA를 Laravel 백엔드로 운영한다면, [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하세요. Sanctum을 쓸 경우, [직접 인증 라우트 구현](#authenticating-users)하거나, 등록, 비밀번호 재설정, 이메일 인증 등의 라우트와 컨트롤러를 제공하는 [Laravel Fortify](/docs/{{version}}/fortify)를 헤드리스 인증 백엔드로 사용할 수 있습니다.

OAuth2의 모든 기능이 반드시 필요하면 Passport를 선택하세요.

마지막으로, 빠르게 시작하려면 Laravel 내장 인증 서비스와 Laravel Sanctum을 함께 사용하는 [Laravel Jetstream](https://jetstream.laravel.com)을 추천합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!NOTE]
> 이 문서는 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 통한 사용자 인증을 다루며, 이는 빠른 시작을 돕는 UI 스캐폴딩을 포함합니다. Laravel 인증 시스템을 직접 통합하려면 [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치 (Install A Starter Kit)

우선 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 현재 제공되는 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 인증 기능 통합을 위한 훌륭한 출발점을 제공합니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 및 비밀번호 확인을 포함하는 최소한의 간단한 인증 기능 구현입니다. 뷰 레이어는 간단한 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. Breeze는 Vue 또는 React를 사용하는 [Inertia](https://inertiajs.com) 기반 스캐폴딩도 지원합니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 더욱 강력한 스타터 키트로, [Livewire](https://laravel-livewire.com) 또는 [Inertia.js 및 Vue](https://inertiajs.com)를 사용한 애플리케이션 스캐폴딩을 지원합니다. 또한, 2단계 인증, 팀 관리, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/{{version}}/sanctum)을 통한 API 인증 지원, 계정 삭제 등의 기능을 포함합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기 (Retrieving The Authenticated User)

스타터 키트를 설치하고 사용자가 애플리케이션에 등록하고 인증하도록 하면, 현재 인증된 사용자와 상호작용할 필요가 생깁니다. 인바운드 요청을 처리하는 동안, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자를 가져올 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기...
$user = Auth::user();

// 현재 인증된 사용자의 ID 가져오기...
$id = Auth::id();
```

또는, 사용자가 인증된 상태라면, `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자에 접근할 수 있습니다. Laravel은 타입힌팅된 클래스를 자동으로 컨트롤러 메서드에 주입하므로, `Illuminate\Http\Request` 타입힌팅을 활용하면 컨트롤러 내부 어디서든 `user` 메서드를 사용해 편리하게 인증된 사용자 정보를 얻을 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 비행 정보 업데이트
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

들어오는 HTTP 요청 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하세요. 사용자가 인증된 경우 `true`를 반환합니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되어 있음...
}
```

> [!TIP]
> `check` 메서드를 직접 사용해 인증 여부를 확인할 수도 있지만, 보통은 미들웨어를 사용해 라우트나 컨트롤러 접근 전에 인증을 확인합니다. 이에 관한 자세한 내용은 [라우트 보호](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/{{version}}/middleware)를 활용하여 인증된 사용자만 특정 라우트를 접근하도록 제한할 수 있습니다. Laravel은 기본적으로 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어를 제공합니다. 이 미들웨어는 애플리케이션 HTTP 커널에 이미 등록되어 있으므로, 라우트에 간단히 미들웨어만 붙여주면 됩니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 발견하면, `login` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션합니다. 이 동작을 변경하고 싶으면 애플리케이션 `app/Http/Middleware/Authenticate.php` 파일 내 `redirectTo` 메서드를 수정하세요:

```
/**
 * 사용자를 리디렉션할 경로 얻기
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

`auth` 미들웨어를 라우트에 붙일 때, 어떤 "가드"를 사용할지 지정할 수도 있습니다. 이 가드는 `auth.php` 설정 파일의 `guards` 배열 키 중 하나여야 합니다:

```
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한 (Login Throttling)

Laravel Breeze 또는 Laravel Jetstream [스타터 키트](/docs/{{version}}/starter-kits)를 사용하면 로그인 시도에 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본적으로, 여러 번 잘못된 자격 증명을 입력하면 1분간 로그인 시도가 차단됩니다. 제한은 사용자 이름/이메일과 IP 주소 조합 단위로 적용됩니다.

> [!TIP]
> 애플리케이션 내 다른 라우트에 대해 속도 제한을 적용하려면 [속도 제한 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

Laravel [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)에 포함된 인증 스캐폴딩을 굳이 사용하지 않아도 됩니다. 직접 Laravel 인증 클래스를 이용해 사용자 인증을 관리할 수도 있습니다. 어렵지 않으니 걱정하지 마세요!

Laravel 인증 서비스는 `Auth` [파사드](/docs/{{version}}/facades)를 통해 접근합니다. 우선 클래스 상단에 `Auth` 파사드를 임포트해야 합니다. `attempt` 메서드를 살펴봅시다. `attempt`는 보통 로그인 폼에서 인증 시도 처리에 사용됩니다. 인증이 성공하면 [세션](/docs/{{version}}/session)을 재생성하여 [세션 고정 공격](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다:

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
        ]);
    }
}
```

`attempt` 메서드는 첫 번째 인수로 키/값 배열을 받습니다. 배열 값들은 데이터베이스에서 사용자를 찾기 위한 조건입니다. 위 예제는 `email` 컬럼 값을 기반으로 사용자를 탐색합니다. 찾은 사용자의 암호화된 비밀번호와 입력한 `password` 값을 비교하는데, 입력된 비밀번호는 자동으로 해시 처리되므로 별도로 해시하지 않아야 합니다. 두 해시가 일치하면 인증 세션이 시작됩니다.

Laravel 인증 서비스가 사용할 사용자 검색 방식은 인증 가드의 `provider` 설정에 따라 결정됩니다. 기본 `config/auth.php`에서는 Eloquent 사용자 프로바이더와 `App\Models\User` 모델을 사용하도록 설정되어 있습니다. 필요에 따라 설정을 변경하세요.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

`intended` 메서드를 사용하는 Laravel 리다이렉트 기능은 인증 미들웨어에 의해 가로채기 전 사용자가 원래 접근하려 했던 URL로 리다이렉트합니다. 해당 URL이 없을 경우 대비한 대체 URI도 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

필요하면, 이메일과 비밀번호 외에 추가 조건도 `attempt` 메서드 배열에 넣어 인증 쿼리에 포함할 수 있습니다. 예를 들어, 사용자가 "active" 상태인지 확인할 수 있습니다:

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

> [!NOTE]
> 예시에서 `email`은 필수가 아니며, 데이터베이스 테이블의 "사용자 이름"에 해당하는 컬럼명을 사용하면 됩니다.

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근하기

`Auth` 파사드의 `guard` 메서드를 통해 사용할 가드 인스턴스를 지정할 수 있습니다. 이를 통해 서로 다른 인증 대상 모델이나 사용자 테이블을 별도로 관리할 수 있습니다.

`guard`에 전달하는 이름은 `auth.php` 설정 파일 내 `guards` 배열 키 중 하나와 일치해야 합니다:

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹 애플리케이션 로그인 폼에는 "나를 기억하기" 체크박스가 있습니다. 이 기능을 제공하려면, `attempt` 메서드의 두 번째 인수로 불리언 값을 전달하세요.

`true`로 설정하면 Laravel은 사용자가 수동으로 로그아웃할 때까지 인증 상태를 무기한 유지합니다. `users` 테이블에는 "나를 기억하기" 토큰을 저장할 `remember_token` 문자열 컬럼이 있어야 하며, 새로운 Laravel 기본 마이그레이션에 이미 포함되어 있습니다:

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억되고 있음...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증하기

이미 유효한 사용자 인스턴스가 있다면, `Auth` 파사드의 `login` 메서드에 이를 전달해 현재 인증된 사용자로 설정할 수 있습니다. 전달하는 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/{{version}}/contracts)을 구현해야 하며, Laravel이 기본 제공하는 `App\Models\User`는 이미 구현되어 있습니다. 이 방식은 사용자 회원가입 직후 등, 이미 사용자 인스턴스를 가지고 있을 때 유용합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드 두 번째 인수로 불리언을 넘기면 "나를 기억하기" 기능을 사용할지 지정합니다. 이를 `true`로 설정하면 사용자는 세션이 만료될 때까지 혹은 사용자가 직접 로그아웃할 때까지 인증된 상태를 유지합니다:

```
Auth::login($user, $remember = true);
```

필요하면, `login` 호출 전에 인증 가드를 지정할 수도 있습니다:

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증하기

데이터베이스 기본 키로 사용자를 인증하려면 `loginUsingId` 메서드를 사용합니다. 인증할 사용자의 기본 키를 인수로 넘기면 됩니다:

```
Auth::loginUsingId(1);
```

두 번째 인수로 불리언 값을 넘기면 "나를 기억하기" 사용 여부를 정할 수 있습니다:

```
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
#### 단일 요청 인증하기

`once` 메서드는 세션이나 쿠키 없이 단 한 번의 요청에 대해 사용자 인증을 수행합니다:

```
if (Auth::once($credentials)) {
    //
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 로그인 페이지 없이도 애플리케이션 사용자 인증을 빠르게 구현할 수 있는 방법입니다. 시작하려면, 라우트에 `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 붙이세요. 이 미들웨어는 Laravel 프레임워크 기본 내장되어 있어 직접 정의하지 않아도 됩니다:

```
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth.basic');
```

이 미들웨어를 라우트에 붙이면 브라우저에서 해당 URL 접속 시 자동으로 인증 정보 입력 창이 뜹니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블 내 `email` 컬럼을 사용자 이름으로 가정합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고사항

PHP FastCGI와 Apache를 조합해 Laravel 앱을 서비스할 경우, HTTP 기본 인증이 제대로 동작하지 않을 수 있습니다. 다음 내용을 `.htaccess` 파일에 추가하면 문제를 해결할 수 있습니다:

```
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 상태 비저장 HTTP 기본 인증 (Stateless HTTP Basic Authentication)

HTTP 기본 인증을 세션 쿠키를 설정하지 않고 사용할 수도 있습니다. 이는 API 요청 인증에 HTTP 인증 방식을 사용할 때 주로 유용합니다. 방법은 `onceBasic` 메서드를 호출하는 미들웨어를 정의하는 것입니다. 반환된 응답이 없으면 애플리케이션 처리 흐름이 계속됩니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Support\Facades\Auth;

class AuthenticateOnceWithBasicAuth
{
    /**
     * 인바운드 요청 처리
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

이제 이 미들웨어를 [등록](/docs/{{version}}/middleware#registering-middleware)하고 라우트에 붙이세요:

```
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth.basic.once');
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 애플리케이션에서 로그아웃시키려면 `Auth` 파사드의 `logout` 메서드를 사용해 세션에서 인증 정보를 제거하면 됩니다. 이후 요청은 인증되지 않은 상태가 됩니다.

또한 `logout` 호출 후에는 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/{{version}}/csrf)을 재생성하는 것이 권장됩니다. 로그아웃 후 보통 애플리케이션 루트로 리디렉션합니다:

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
### 다른 기기에서 세션 무효화 (Invalidating Sessions On Other Devices)

Laravel은 현재 기기의 세션은 유지하면서, 사용자의 다른 기기에서 활성 세션을 무효화하고 로그아웃시키는 기능을 제공합니다. 보통 사용자가 비밀번호를 변경할 때 사용합니다.

시작하기 전에, `App\Http\Kernel` 클래스의 `web` 미들웨어 그룹에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 활성화되어 있는지 확인하세요:

```
'web' => [
    // ...
    \Illuminate\Session\Middleware\AuthenticateSession::class,
    // ...
],
```

이후 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용이 비밀번호 확인을 요구하며, 애플리케이션에서 입력 폼을 통해 현재 비밀번호를 받아야 합니다:

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 호출되면, 사용자의 다른 기기 세션은 모두 무효화되어 모든 가드에서 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 개발하다 보면, 특정 중요한 작업이나 민감 영역 접속 전에 사용자가 비밀번호를 다시 확인하도록 요구해야 할 때가 있습니다. Laravel은 이 과정을 쉽게 구현할 수 있도록 내장 미들웨어를 제공합니다. 이 기능을 구현하기 위해서는 비밀번호 확인을 요청하는 뷰를 보여주는 라우트와 비밀번호 유효성을 검증하고 사용자 의도대로 리디렉션하는 라우트 두 개를 정의해야 합니다.

> [!TIP]
> 다음 문서는 Laravel 비밀번호 확인 기능과 직접 통합하는 방법을 다룹니다. 더 빠른 시작을 원하면, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)에 이 기능이 포함되어 있으니 참고하세요!

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

비밀번호를 확인한 후 사용자는 3시간 동안 재인증을 요구받지 않습니다. 이 시간 설정은 애플리케이션 `config/auth.php`의 `password_timeout` 설정값을 변경하여 조절할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

우선, 사용자에게 비밀번호 확인을 요청하는 뷰를 반환하는 라우트를 정의합니다:

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트가 반환하는 뷰는 `password` 필드를 포함하는 폼이어야 하며, 사용자에게 민감 영역 접속을 위해 비밀번호 확인이 필요하다는 안내 문구를 포함할 수도 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, 비밀번호 확인 폼에서 제출된 요청을 처리하는 라우트를 정의합니다. 이 라우트는 비밀번호 유효성 검증을 수행하고, 성공 시 사용자를 원래 가려던 위치로 리디렉션합니다:

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

이 라우트를 자세히 보면, 우선 요청 `password` 필드가 현재 인증된 사용자의 비밀번호와 일치하는지 `Hash::check`로 확인합니다. 유효하면 Laravel 세션에 비밀번호가 확인되었음을 저장하기 위해 `passwordConfirmed` 메서드를 호출합니다. 이 메서드는 사용자가 마지막으로 비밀번호를 확인한 시각을 세션에 기록합니다. 마지막으로 사용자가 원래 가려던 주소로 리디렉션합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

최근에 비밀번호 확인이 필요한 작업을 수행하는 모든 라우트에는 `password.confirm` 미들웨어를 붙여야 합니다. 이 미들웨어는 Laravel 기본 설치 시 포함되어 있으며, 사용자의 의도한 목적지를 세션에 자동으로 저장해 비밀번호 확인 후에 해당 위치로 리디렉션하도록 도와줍니다. 미들웨어가 실행되면 `password.confirm` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션됩니다:

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

`Auth` 파사드의 `extend` 메서드를 사용하여 자신만의 인증 가드를 정의할 수 있습니다. 보통 이 호출은 [서비스 프로바이더](/docs/{{version}}/providers) 내에 둡니다. Laravel 기본 제공 `AuthServiceProvider`가 있으므로, 여기에 코드를 추가할 수 있습니다:

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 인증 / 인가 서비스를 등록합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::extend('jwt', function ($app, $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 인스턴스를 반환해야 합니다...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예제에서 알 수 있듯이, `extend`에 전달된 콜백은 `Illuminate\Contracts\Auth\Guard`를 구현한 인스턴스를 반환해야 합니다. 이 인터페이스에는 커스텀 가드를 정의하기 위해 구현해야 하는 몇 가지 메서드가 포함되어 있습니다. 커스텀 가드를 정의한 후에는 `auth.php` 설정 파일 내 `guards` 배열에서 해당 가드를 참조할 수 있습니다:

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

가장 간단한 커스텀 HTTP 요청 기반 인증 시스템 구현 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드는 단일 클로저로 인증 절차를 빠르게 정의할 수 있습니다.

`AuthServiceProvider`의 `boot` 메서드 내에서 `Auth::viaRequest`를 호출합니다. 첫 번째 인수는 커스텀 가드 이름(임의 문자열), 두 번째 인수는 인바운드 HTTP 요청을 받고 인증된 사용자 인스턴스를 반환하거나 인증 실패 시 `null`을 반환하는 클로저입니다:

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션 인증 / 인가 서비스를 등록합니다.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', $request->token)->first();
    });
}
```

이제 커스텀 인증 드라이버가 정의되었으니, `auth.php` 설정 파일 내 `guards` 배열에 다음처럼 추가해 사용할 수 있습니다:

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가하기 (Adding Custom User Providers)

전통적인 관계형 데이터베이스 대신 다른 저장소를 사용할 경우, Laravel에서 자신의 사용자 인증 프로바이더를 확장해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 사용자 프로바이더를 정의할 수 있습니다. 사용자 프로바이더는 `Illuminate\Contracts\Auth\UserProvider` 구현체를 반환해야 합니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 인증 / 인가 서비스를 등록합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::provider('mongo', function ($app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 인스턴스를 반환...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

프로바이더를 등록 후, `auth.php` 설정 파일에서 새 프로바이더를 사용하도록 전환할 수 있습니다. 우선 `providers` 배열에 새 드라이버를 지정합니다:

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로 이 프로바이더를 `guards` 배열에서 참조합니다:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등 영속 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 맡습니다. 이 두 인터페이스 덕분에 사용자 데이터 저장 방식이나 인증 사용자 클래스가 무엇이든 Laravel 인증 메커니즘이 유연하게 작동할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약을 살펴보면 다음과 같습니다:

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

- `retrieveById`: 주로 MySQL 자동 증가 ID 등의 사용자 키를 받아 해당하는 `Authenticatable` 구현체를 반환합니다.

- `retrieveByToken`: 고유한 `$identifier`와 "나를 기억하기"용 `$token`으로 사용자를 조회합니다. 보통 `remember_token` 컬럼과 매칭합니다.

- `updateRememberToken`: 인증된 `$user` 인스턴스에 새 `$token` 값을 저장합니다. "나를 기억하기" 인증 성공 시나 로그아웃 때 새로운 토큰을 할당합니다.

- `retrieveByCredentials`: `Auth::attempt` 시 전달된 자격증명 배열을 받고, 이를 바탕으로 저장소에서 일치하는 사용자를 조회해 `Authenticatable` 구현체를 반환합니다. 보통 `$credentials['username']` 값과 매칭하는 쿼리를 실행합니다. **비밀번호 검증이나 인증은 하지 않습니다.**

- `validateCredentials`: 주어진 `$user`와 `$credentials`를 사용해 인증 여부를 판단합니다. 예를 들어 `Hash::check`를 사용해 사용자의 암호 해시값과 `$credentials['password']`를 비교하기도 합니다. `true` 또는 `false`를 반환합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약 (The Authenticatable Contract)

이제 `UserProvider` 메서드에서 반환하는 객체가 구현해야 하는 `Authenticatable` 계약을 살펴봅니다. 이 계약을 구현하는 인스턴스가 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`에서 반환됩니다:

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

이 인터페이스는 간단합니다. `getAuthIdentifierName`은 사용자 "기본 키" 필드명을 반환하고, `getAuthIdentifier`는 해당 기본 키 값을 반환합니다. MySQL 백엔드를 쓴다면 보통 자동 증가 키입니다. `getAuthPassword`는 사용자의 해시화된 비밀번호를 반환합니다.

이 인터페이스 덕분에 인증 시스템은 어떤 ORM이나 저장소 추상화 레이어를 쓰든지 관계없이 인증 사용자 클래스를 처리할 수 있습니다. Laravel 기본으로는 `app/Models/User` 클래스가 이 인터페이스를 구현하고 포함되어 있습니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel 인증 과정 중 다양한 [이벤트](/docs/{{version}}/events)를 발행합니다. `EventServiceProvider`에서 해당 이벤트에 대한 리스너를 연결할 수 있습니다:

```
/**
 * 애플리케이션 이벤트-리스너 매핑
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