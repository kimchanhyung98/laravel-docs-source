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
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [Stateless HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 재확인](#password-confirmation)
    - [구성](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 제공자 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션에 "로그인"할 수 있도록 인증 방법을 제공합니다. 이런 기능을 구현하는 것은 복잡하고 잠재적으로 위험할 수 있습니다. 그래서 Laravel은 인증을 빠르고, 안전하며, 쉽게 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 시스템은 "가드(guard)"와 "프로바이더(provider)"로 구성됩니다. 가드는 각 요청에 대해 사용자를 어떻게 인증할지를 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용해 상태를 유지하는 `session` 가드를 기본 제공합니다.

프로바이더는 영구 저장소에서 사용자를 어떻게 조회할지를 정의합니다. Laravel은 [Eloquent](/docs/{{version}}/eloquent)와 데이터베이스 쿼리 빌더를 이용한 사용자 조회를 기본적으로 지원합니다. 필요에 따라 추가 프로바이더를 정의할 수도 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel의 인증 서비스 동작을 조정할 수 있는 다양한 옵션이 잘 문서화되어 있습니다.

> **참고**  
> 가드(guards)와 프로바이더(providers)는 "권한(roles)"과 "퍼미션(permissions)"과는 다릅니다. 권한을 부여하는 방법에 대해 더 알고 싶다면, [권한 부여](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 킷

빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 다른 URL로 이동하면 스타터 킷이 전체 인증 시스템의 스캐폴딩을 모두 처리해줍니다!

**최종 애플리케이션에서 스타터 킷을 사용하지 않더라도, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 스타터 킷을 설치해보면 실제 프로젝트에서 Laravel의 모든 인증 기능을 어떻게 구현하는지 배울 수 있는 좋은 기회가 됩니다.** Breeze는 인증 컨트롤러, 라우트, 뷰를 생성해주므로, 이 파일 내의 코드를 살펴보면 Laravel의 인증 기능이 어떻게 구현되는지 확인할 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. 애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 설계할 때, 패스워드 컬럼의 길이가 최소 60자 이상이어야 합니다. 새 Laravel 애플리케이션에 포함된 기본 `users` 테이블 마이그레이션에서는 이미 이 규격을 초과하는 컬럼이 생성됩니다.

또한, `users`(혹은 이에 상응하는) 테이블에 널(null) 허용, 문자열 타입인 100자 길이의 `remember_token` 컬럼이 포함되어 있어야 합니다. 이 컬럼은 사용자가 "로그인 상태 유지(remember me)"를 선택할 때 토큰을 저장하는 데 사용됩니다. 역시, Laravel의 기본 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속 진행하기 전에 Laravel의 전반적인 인증 에코시스템을 살펴보고, 각 패키지의 용도를 설명하겠습니다.

먼저, 인증이 어떻게 동작하는지 생각해봅시다. 웹 브라우저를 사용하는 경우, 사용자는 로그인 폼을 통해 아이디와 비밀번호를 입력합니다. 인증 정보가 올바르면 애플리케이션은 인증된 사용자 정보를 [세션](/docs/{{version}}/session)에 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 담겨 이후 요청에서 사용자를 올바른 세션에 매핑할 수 있습니다. 세션 쿠키를 받은 후, 애플리케이션은 세션 ID에 기반하여 세션 데이터를 조회, 인증 정보를 확인하고 사용자를 "인증됨"으로 간주합니다.

원격 서비스가 API 접근을 위해 인증을 해야 할 때는 보통 쿠키를 사용하지 않습니다(웹 브라우저가 없기 때문). 대신, 원격 서비스는 매 요청마다 API 토큰을 전송하며, 애플리케이션은 들어온 토큰을 허용된 토큰 목록과 대조하여 해당 토큰 소유자의 요청임을 "인증"합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel에는 내장 인증 및 세션 서비스가 탑재되어 있으며, 보통 `Auth`와 `Session` 파사드를 통해 접근합니다. 이 기능은 웹 브라우저에서 시작되는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 검증하고 인증하는 메서드를 제공하며, 인증에 성공하면 자동으로 세션에 적절한 인증 데이터를 저장하고 세션 쿠키를 발급합니다. 이런 서비스의 사용법은 이 문서 전체에서 다룹니다.

**애플리케이션 스타터 킷**

문서에서 설명한 것처럼, 직접 인증 서비스를 다루어 애플리케이션의 인증 계층을 만들 수 있습니다. 그러나 더 빠른 시작을 위해 인증 계층의 견고한 스캐폴딩을 제공하는 [무료 패키지](/docs/{{version}}/starter-kits)를 출시했습니다. 대표적으로 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/{{version}}/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/{{version}}/fortify)가 있습니다.

_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 Laravel 인증 기능을 단순하고 최소한의 형태로 구현합니다. 뷰는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 작성되어 있습니다. 자세한 사용 방법은 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 문서를 참고하세요.

_Laravel Fortify_는 다양한 인증 기능(쿠키 기반 인증, 2단계 인증, 이메일 인증 등)을 제공하는 헤드리스 인증 백엔드입니다. Fortify는 Laravel Jetstream의 인증 백엔드로 사용하거나, [Sanctum](/docs/{{version}}/sanctum)과 조합하여 SPA(싱글 페이지 애플리케이션) 인증 백엔드로 쓸 수 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_은 Tailwind CSS, [Livewire](https://laravel-livewire.com), [Inertia](https://inertiajs.com) 기반의 아름답고 모던한 UI로 Fortify의 인증 기능을 제공하는 강력한 애플리케이션 스타터 킷입니다. 2단계 인증, 팀(Team), 브라우저 세션 관리, 프로필 관리, [Sanctum](/docs/{{version}}/sanctum) 기반 API 토큰 인증 등 강력한 기능을 제공합니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰을 관리하고 인증하는 데 도움이 되는 두 가지 선택적 패키지, [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum)을 제공합니다. 이 라이브러리들과 내장 쿠키 기반 인증은 상호 배타적이지 않으므로 다양하게 조합할 수 있습니다. 주로 API 토큰 인증에 집중하는 반면, 내장 인증 서비스는 브라우저용 쿠키 인증에 중점을 둡니다. 많은 애플리케이션에서 두 방식을 혼용합니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"(토큰 발급 방식)을 제공하는 OAuth2 인증 제공자입니다. 복잡하고 다기능인 API 인증 패키지이나, 대다수의 애플리케이션은 OAuth2 스펙의 모든 복잡한 기능이 필요하지 않습니다. 또한, 그동안 많은 개발자들이 SPA 또는 모바일 앱을 Passport와 같은 OAuth2 인증 제공자로 인증하는 방법에 혼란을 겪었습니다.

**Sanctum**

OAuth2의 복잡성과 개발자의 혼란에 대응하기 위해, 우리는 더 간단하고 직관적인 인증 패키지 개발에 착수했고, 그 결과가 바로 [Laravel Sanctum](/docs/{{version}}/sanctum)입니다. Sanctum은 자체 UI가 있는 웹 요청과 API 요청 모두에서 사용할 수 있는 인증 패키지로, API와 프론트엔드가 분리된 SPA, 모바일 앱, 일반 웹앱 모두에 권장됩니다.

Sanctum은 하이브리드 웹/API 인증 패키지로, 요청이 오면 먼저 세션 쿠키가 있는지 검사하여 내부 내장 인증 서비스(앞서 설명한)를 통해 인증합니다. 세션 쿠키가 없으면 API 토큰 여부를 검사하여 인증합니다. 자세한 동작 방식은 Sanctum의 ["작동 방식"](/docs/{{version}}/sanctum#how-it-works) 문서를 참고하세요.

Sanctum은 우리가 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 킷에 기본 포함시키는 API 패키지로, 대부분의 웹 애플리케이션 인증에 가장 잘 어울린다고 믿습니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

정리하자면, 브라우저를 통해 접근하는 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 사용합니다.

외부 서비스가 사용하는 API를 제공한다면, [Passport](/docs/{{version}}/passport) 또는 [Sanctum](/docs/{{version}}/sanctum) 중 하나를 API 토큰 인증에 사용해야 합니다. 일반적으로 더 간단하면서 완벽한 솔루션인 Sanctum를 추천합니다(스코프/권한 지원 포함).

Laravel 백엔드로 동작하는 SPA라면 [Sanctum](/docs/{{version}}/sanctum)을 꼭 사용하세요. 이 경우, [회원가입, 비밀번호 재설정, 이메일 인증 등](#authenticating-users) 백엔드 인증 라우트를 직접 구현하거나, [Fortify](/docs/{{version}}/fortify)를 헤드리스 인증 백엔드로 활용할 수 있습니다.

OAuth2 스펙의 모든 기능이 정말 필요할 때만 Passport를 선택하세요.

빠른 시작을 원한다면, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)로 내장 인증 서비스와 Sanctum의 조합을 바로 체험할 것을 권장합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작

> **경고**  
> 이 문서는 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)에서의 사용자 인증(빠른 UI 스캐폴딩 포함)을 다룹니다. 인증 시스템을 직접 통합하고 싶다면 [수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치

먼저, [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치하세요. 현재 제공되는 Laravel Breeze, Laravel Jetstream은 인증이 탑재된 아름다운 기본 시작점을 제공합니다.

Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 지원하며, [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. 또한 [Inertia](https://inertiajs.com)를 기반으로 Vue 또는 React 스캐폴딩도 제공합니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 Breeze보다 더 강력하며, [Livewire](https://laravel-livewire.com) 또는 [Inertia + Vue](https://inertiajs.com)를 지원합니다. Jetstream은 2단계 인증, 팀, 프로필 관리, 브라우저 세션 관리, [Sanctum](/docs/{{version}}/sanctum)을 통한 API 기능, 계정 삭제 등 다양한 고급 기능을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 킷 설치 후 사용자가 온보딩 및 인증된 후에는 현재 인증된 사용자와 상호작용해야 할 일이 많습니다. 요청을 처리할 때, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회
$user = Auth::user();

// 현재 인증된 사용자의 ID 조회
$id = Auth::id();
```

혹은 사용자가 인증된 이후에는 `Illuminate\Http\Request` 인스턴스를 통해서도 사용자 정보를 조회할 수 있습니다. 컨트롤러 메서드의 타입힌트로 `Illuminate\Http\Request`를 지정하면, `user` 메서드로 인증된 사용자에 원활히 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보 수정
     */
    public function update(Request $request)
    {
        // $request->user()
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
#### 현재 사용자가 인증 상태인지 확인하기

요청을 보낸 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용합니다. 인증 상태라면 `true`가 반환됩니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인 되어 있음
}
```

> **참고**  
> `check` 메서드로 인증 여부를 확인할 수 있지만, 보통은 미들웨어에서 인증 여부를 검사하여 특정 라우트/컨트롤러에만 접근 가능하도록 하는 것이 일반적입니다. 자세한 사용법은 [라우트 보호](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용해서 인증된 사용자만 특정 라우트에 접근하도록 할 수 있습니다. Laravel은 `auth` 미들웨어(`Illuminate\Auth\Middleware\Authenticate` 클래스 참조)를 제공합니다. 이미 애플리케이션의 HTTP 커널에 등록되어 있으므로, 사용하고 싶은 라우트에 다음과 같이 적용하세요:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어가 비인증 사용자를 감지하면, `login` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트합니다. 이 동작을 변경하려면, `app/Http/Middleware/Authenticate.php` 파일의 `redirectTo` 함수를 수정하세요:

```php
/**
 * 인증되지 않은 사용자가 리다이렉트 될 경로 반환
 */
protected function redirectTo($request)
{
    return route('login');
}
```

<a name="specifying-a-guard"></a>
#### 특정 가드 지정

`auth` 미들웨어를 라우트에 추가할 때, 어느 "가드"를 사용할지 명시할 수 있습니다. 지정된 가드는 `auth.php` 설정 파일의 `guards` 배열 중 하나의 키여야 합니다:

```php
Route::get('/flights', function () {
    // 관리자 가드로 인증된 사용자만 접속
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한

Laravel Breeze 또는 Jetstream [스타터 킷](/docs/{{version}}/starter-kits)을 사용하면, 로그인 시도에 대해 자동으로 속도 제한(rate limiting)이 적용됩니다. 기본적으로, 사용자가 일정 횟수 이상 잘못된 정보를 입력하면 1분간 로그인을 시도할 수 없습니다. 제한은 사용자 이름/이메일과 IP 기준으로 적용됩니다.

> **참고**  
> 다른 라우트에도 속도제한을 적용하고 싶다면 [속도 제한 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증

[애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)이 제공하는 인증 스캐폴딩을 반드시 사용할 필요는 없습니다. 사용하지 않을 경우, Laravel의 인증 클래스를 직접 사용해서 인증을 관리할 수 있습니다. 걱정하지 마세요! 매우 쉽습니다.

`Auth` [파사드](/docs/{{version}}/facades)를 사용하며, 위쪽에 `Auth` 파사드를 import 해야 합니다. 이어서, `attempt` 메서드를 살펴보겠습니다. 이 메서드는 주로 로그인 폼의 인증 시도 처리를 위해 사용합니다. 인증 성공 시, [세션](/docs/{{version}}/session)을 재생성하여 [세션 고정 공격](https://en.wikipedia.org/wiki/Session_fixation)을 막아야 합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * 인증 시도 처리
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
            'email' => '입력하신 정보가 올바르지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 키/값 배열을 첫 번째 인자로 받습니다. 배열 속 값으로 사용자를 DB에서 조회하며, 위 예시에서는 `email` 컬럼 값으로 사용자를 찾습니다. 사용자를 찾으면, DB에 저장된 해시화된 비밀번호와 폼에서 입력한 비밀번호가 일치하는지 비교합니다. 입력받은 비밀번호를 해시화할 필요는 없습니다(Laravel이 자동으로 처리). 두 비밀번호의 해시가 일치하면 인증 세션이 시작됩니다.

Laravel 인증 서비스는 가드의 "provider" 설정에 따라 사용자를 조회합니다. 기본 `config/auth.php` 파일에서는 Eloquent 사용자 제공자를 지정하고, 사용자 조회 시 `App\Models\User`을 사용합니다. 필요시 설정 파일을 변경할 수 있습니다.

`attempt`는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

`intended`는 인증 미들웨어에 가로채이기 전에 사용자가 원래 방문하려던 URL로 리다이렉트합니다. 목적지 URL이 없을 경우 기본값을 설정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

사용자 이메일, 비밀번호 외에 추가 쿼리를 조건으로 지정할 수도 있습니다. 예를 들어, 사용자가 "active"여야 한다는 조건을 추가할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공
}
```

복잡한 조건이 필요하다면, credentials 배열에 클로저를 넣어 쿼리를 커스터마이징할 수도 있습니다:

```php
if (Auth::attempt([
    'email' => $email, 
    'password' => $password, 
    fn ($query) => $query->has('activeSubscription'),
])) {
    // 인증 성공
}
```

> **경고**  
> 여기서 `email`은 예시일 뿐 필수 필드가 아닙니다. 데이터베이스에서 사용자명에 해당하는 컬럼명을 쓰세요.

`attemptWhen`은 두 번째 인자로 클로저를 받아서, 사용자 인증 전에 추가 검사를 할 수 있습니다:

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function ($user) {
    return $user->isNotBanned();
})) {
    // 인증 성공
}
```

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근

`Auth` 파사드의 `guard` 메서드로 사용자 인증 시 사용할 가드를 지정할 수 있습니다. 이를 통해 서로 다른 모델 또는 사용자 테이블 기반의 인증을 나눠 관리할 수 있습니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기(로그인 상태 유지)

많은 웹 앱에서 로그인 폼에 "로그인 상태 유지" 체크박스를 제공합니다. 이 기능을 구현하려면 `attempt` 메서드 두 번째 인자로 boolean 값을 넘기기만 하면 됩니다.

값이 `true`인 경우, 사용자는 수동 로그아웃 또는 쿠키 삭제 전까지 인증 상태가 유지됩니다. `users` 테이블에는 "remember_token" 컬럼이 있어야 하며, 기본 마이그레이션에 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자를 기억함
}
```

"로그인 상태 유지" 기능을 제공한다면, 현재 사용자가 이 쿠키로 인증되었는지 `viaRemember`를 통해 알 수 있습니다:

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

이미 존재하는 사용자 인스턴스를 인증된 사용자로 설정해야 할 시, `Auth` 파사드의 `login` 메서드에 해당 인스턴스를 전달하면 됩니다. 이 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` 계약을 구현해야하며, Laravel의 기본 `App\Models\User` 모델은 이를 구현하고 있습니다. 회원가입 직후와 같이 이미 유효한 사용자 인스턴스가 있다면 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login`에 두 번째 인자로 boolean 값을 넘기면 "로그인 상태 유지" 옵션을 지정할 수 있습니다:

```php
Auth::login($user, $remember = true);
```

가드 지정도 가능합니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증

DB 레코드의 기본키를 사용해 사용자를 인증하려면 `loginUsingId` 메서드를 사용하세요.

```php
Auth::loginUsingId(1);

Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
#### 일회용 인증(세션/쿠키 미사용)

`once` 메서드를 사용하면 한 번의 요청에 한해 사용자를 인증할 수 있습니다. 세션이나 쿠키는 사용하지 않습니다.

```php
if (Auth::once($credentials)) {
    //
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 없이 빠르게 인증을 제공하는 방법입니다. 시작하려면 `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 라우트에 추가하세요. `auth.basic`은 Laravel 프레임워크에 내장되어 있습니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근
})->middleware('auth.basic');
```

미들웨어가 라우트에 추가되면 브라우저에서 해당 라우트 접속 시 자동으로 인증 창이 나타납니다. `auth.basic` 미들웨어는 기본적으로 `users` 테이블의 `email` 컬럼을 "username"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 사용자 참고

PHP FastCGI + Apache 환경에서 HTTP Basic 인증이 제대로 작동하지 않을 수 있습니다. 아래 코드를 애플리케이션 `.htaccess`에 추가해 주세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP Basic 인증

session에 사용자 식별자 쿠키를 남기지 않는 Stateless HTTP Basic 인증도 가능합니다. API 인증 등에서 유용합니다. 이를 위해 [별도 미들웨어를 정의](/docs/{{version}}/middleware)하세요:

```php
<?php

namespace App\Http\Middleware;

use Illuminate\Support\Facades\Auth;

class AuthenticateOnceWithBasicAuth
{
    /**
     * 요청 처리
     */
    public function handle($request, $next)
    {
        return Auth::onceBasic() ?: $next($request);
    }
}
```

그리고 [라우트 미들웨어로 등록](/docs/{{version}}/middleware#registering-middleware) 후 라우트에 적용하세요:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근
})->middleware('auth.basic.once');
```

<a name="logging-out"></a>
## 로그아웃

사용자를 직접 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 사용하면 됩니다. 이는 세션에서 인증 정보를 제거하여 이후 요청이 인증되지 않도록 합니다.

로그아웃 후에는 세션 무효화 및 [CSRF 토큰](/docs/{{version}}/csrf) 재생성이 권장됩니다. 이후 홈으로 리다이렉트하세요:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 로그아웃 처리
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
### 다른 기기 세션 무효화

Laravel은 사용자가 다른 기기에서 활성화된 세션을 무효화하고 "로그아웃"시킬 수 있는 기능도 제공합니다. 보통 비밀번호 변경 등 민감 작업 시, 현재 사용 중인 기기를 제외한 다른 모든 기기에서 로그아웃할 때 활용합니다.

먼저, 세션 인증을 적용할 라우트에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 포함되어야 합니다. 보통 미들웨어 그룹에 적용합니다. `auth.session` 키로 등록되어 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그런 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 현재 비밀번호 확인이 필요합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

이 메서드 호출 시 사용자의 다른 세션은 모두 무효화되어, 모든 가드에서 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 재확인

애플리케이션을 만들다 보면, 일부 중요한 작업이나 민감한 영역 접근 전에 사용자의 비밀번호를 다시 확인해야 할 수 있습니다. Laravel에는 이를 쉽게 구현할 수 있는 내장 미들웨어가 있습니다. 두 개의 라우트(비밀번호 확인 뷰 표시, 비밀번호 확인 처리)를 정의하면 됩니다.

> **참고**  
> 아래 내용은 Laravel의 비밀번호 재확인 기능을 직접 통합하는 방법입니다. 더 빠른 시작을 원한다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)에도 이 기능이 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
### 구성

비밀번호 재확인 후 3시간 동안은 재확인이 필요 없습니다. 필요시 `config/auth.php`에서 `password_timeout` 값을 수정해 재확인 요청 주기를 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자에게 비밀번호 확인을 요구하는 뷰를 표시하는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

반환되는 뷰에는 `password` 입력 필드가 포함된 폼이 있어야 합니다. 또한, 사용자가 보호된 영역에 접근하므로 비밀번호를 재확인해야 함을 안내하는 설명 텍스트를 추가하면 좋습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

이제 확인 폼을 처리할 라우트를 정의합니다(유효성 검사 및 리다이렉트 처리):

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['입력하신 비밀번호가 올바르지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

위 라우트는 우선 비밀번호가 현재 인증된 사용자의 비밀번호와 일치하는지 확인합니다. 일치한다면 Laravel 세션에 패스워드가 확인되었다는 타임스탬프가 기록되고, 사용자는 의도한 경로로 리다이렉트됩니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

비밀번호 재확인을 필요로 하는 라우트에는 반드시 `password.confirm` 미들웨어를 할당해야 합니다. 이 미들웨어는 기본 Laravel에 포함되어 있으며, 사용자의 의도된 목적지를 세션에 기록하여 비밀번호 확인 후 해당 위치로 리다이렉트하도록 합니다. 이후 `password.confirm` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트됩니다:

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

`Auth` 파사드의 `extend` 메서드로 커스텀 인증 가드를 등록할 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers) 내에서 호출해야 하며, Laravel의 `AuthServiceProvider`를 사용하세요.

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 인증/권한 서비스 등록
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::extend('jwt', function ($app, $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 인스턴스 반환
            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 인터페이스를 구현하는 객체를 반환해야 합니다. 등록이 끝나면, `auth.php` 설정 파일의 `guards`에서 해당 가드를 참조할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 기반 요청 가드

커스텀 HTTP 요청 기반 인증 시스템을 간단하게 구현할 수 있는 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드는 단일 클로저로 인증 절차를 정의할 수 있습니다.

`AuthServiceProvider`의 `boot` 메서드 내에서 호출하세요:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

public function boot()
{
    $this->registerPolicies();

    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

가드 등록 후, `auth.php` 설정 파일에서 아래와 같이 드라이버로 등록합니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 인증 미들웨어를 라우트에 적용할 때 해당 가드를 참조하면 됩니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 제공자(User Provider) 추가

관계형 데이터베이스를 사용하지 않는 경우, 직접 사용자 제공자를 확장해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 제공자를 정의할 수 있으며, 반환 타입은 `Illuminate\Contracts\Auth\UserProvider` 구현체여야 합니다.

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 인증/권한 서비스 등록
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::provider('mongo', function ($app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 인스턴스 반환
            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

등록 후, `auth.php` 파일에서 새 제공자를 사용하도록 설정하세요:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

최종적으로, `guards` 설정에서 제공자를 참조합니다:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 영구 저장소(MySQL, MongoDB 등)에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스 덕분에, 사용자 데이터 저장 방식이나 ORM에 관계없이 인증 시스템이 동일하게 동작합니다.

`UserProvider` 인터페이스를 살펴봅시다:

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
}
```

- `retrieveById`는 사용자 식별자, 예를 들면 MySQL의 자동 증가 ID를 받아 사용자 인스턴스를 반환합니다.
- `retrieveByToken`은 `$identifier`와 `remember_token`을 이용해 사용자를 가져옵니다.
- `updateRememberToken`은 새 `$token`으로 사용자의 `remember_token` 값을 업데이트합니다(재로그인/로그아웃 등).
- `retrieveByCredentials`는 `Auth::attempt`에서 전달된 credentials 배열로 사용자를 조회합니다. **여기에는 비밀번호 검사는 포함되어선 안됩니다.**
- `validateCredentials`는 주어진 `$user`와 `$credentials`가 일치하는지 비교해 인증 결과를 반환해야 합니다(예: `Hash::check`로 비밀번호 비교).

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

`UserProvider`의 각 메서드는 인증 가능한 사용자 객체를 반환해야 하는데, 이 객체는 `Authenticatable` 인터페이스를 구현해야 합니다.

```php
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

- `getAuthIdentifierName`은 "기본키" 필드 이름,  
- `getAuthIdentifier`는 사용자의 "기본키" 값,  
- `getAuthPassword`는 해시된 비밀번호를 반환해야 합니다.

이 인터페이스 덕분에 어떤 ORM/저장소를 사용해도 인증 시스템과 "user" 객체가 언제든 연동될 수 있습니다. Laravel은 기본적으로 `app/Models/User` 클래스가 이 인터페이스를 구현합니다.

<a name="events"></a>
## 이벤트

Laravel은 인증 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 디스패치합니다. `EventServiceProvider`에서 다음 이벤트에 리스너를 지정할 수 있습니다:

```php
/**
 * 애플리케이션 이벤트 Listener 매핑
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
