# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치하기](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한(Throttle)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기(Remember Me)](#remembering-users)
    - [기타 인증 방식](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [Stateless HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기에서 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인(Password Confirmation)](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 유저 프로바이더 추가](#adding-custom-user-providers)
    - [User Provider 계약(Contract)](#the-user-provider-contract)
    - [Authenticatable 계약(Contract)](#the-authenticatable-contract)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 방법을 제공합니다. 이러한 기능을 구현하는 것은 복잡하고 잠재적으로 위험할 수 있습니다. 그래서 Laravel은 빠르고 안전하며 쉽게 인증을 구현할 수 있도록 필요한 도구를 제공합니다.

Laravel의 인증 기능은 기본적으로 "가드(guards)"와 "프로바이더(providers)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자가 어떻게 인증되는지 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용해 상태를 유지하는 `session` 가드를 기본 제공합니다.

프로바이더는 사용자를 영구 저장소에서 어떻게 가져올지 정의합니다. Laravel은 [Eloquent](/docs/{{version}}/eloquent) 및 쿼리 빌더를 사용해 사용자를 가져오는 것을 지원하지만, 필요에 따라 추가 프로바이더를 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 있습니다. 이 파일은 인증 서비스의 동작을 미세 조정할 수 있는 여러 옵션을 잘 문서화해 제공합니다.

> [!NOTE]  
> 가드와 프로바이더는 "권한(roles)" 및 "퍼미션(permissions)"과 혼동해서는 안 됩니다. 권한을 통한 사용자 행동 허가에 대한 자세한 내용은 [권한(authorization)](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 다른 URL로 이동하면 전체 인증 시스템의 스캐폴딩이 자동으로 구성됩니다!

**최종 Laravel 애플리케이션에서 스타터 키트를 사용하지 않더라도, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 스타터 키트를 설치해보면 실제 프로젝트에서 Laravel 인증 기능이 어떻게 구현되는지 학습할 수 있는 좋은 기회가 됩니다.** Laravel Breeze는 인증 컨트롤러, 라우트, 뷰를 자동으로 생성하므로, 해당 파일의 코드를 분석해 Laravel 인증 기능 활용법을 쉽게 배울 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. 애플리케이션에서 Eloquent를 사용하지 않는다면, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더도 활용할 수 있습니다.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 작성할 때, 비밀번호 컬럼이 최소 60자 이상인 것을 확인하세요. 기본 `users` 테이블 마이그레이션은 이미 이 길이를 초과하는 컬럼을 생성합니다.

또한 `users`(또는 유사한) 테이블에 100자 길이의 nullable string 타입인 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 "기억하기(rememeber me)" 옵션을 선택한 사용자의 토큰을 저장하는 데 사용됩니다. 역시 기본 `users` 테이블 마이그레이션에 해당 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증 관련 여러 패키지를 제공합니다. 계속 진행하기 전에 Laravel의 전반적인 인증 에코시스템을 살펴보고, 각 패키지의 목적에 대해 알아봅니다.

우선 인증 방식부터 생각해봅시다. 웹 브라우저에서 사용자는 로그인 폼을 통해 아이디와 비밀번호를 입력합니다. 인증 정보가 올바르면 애플리케이션은 인증된 사용자 정보를 [세션](/docs/{{version}}/session)에 저장합니다. 브라우저에는 세션 ID가 담긴 쿠키가 발급되어, 후속 요청에서도 올바른 세션으로 사용자를 연관지을 수 있습니다. 세션 쿠키가 수신되면 애플리케이션은 세션 데이터를 조회해 인증 정보를 확인하고 사용자를 "인증됨" 상태로 간주합니다.

원격 서비스가 API 접근을 인증해야 할 때는 브라우저가 없으므로 쿠키 대신 API 토큰을 요청마다 전송합니다. 애플리케이션은 유효한 API 토큰 목록과 비교해 요청을 인증 처리하게 됩니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel 내장 브라우저 인증 서비스

Laravel은 일반적으로 `Auth`, `Session` 파사드를 통해 사용할 수 있는 내장 인증 및 세션 서비스를 포함합니다. 이 기능은 주로 웹 브라우저에서 시작된 요청에 대한 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명을 검증하고 인증할 수 있는 메서드가 제공되며, 인증 데이터는 자동으로 세션에 저장되고 세션 쿠키도 발급됩니다. 해당 서비스 사용 예시는 이 문서 전체에 담겨 있습니다.

**애플리케이션 스타터 키트**

문서에서 다루듯 인증 서비스를 직접 사용해 자신만의 인증 계층을 구축할 수 있지만, 빠른 시작을 위해 [무료 패키지](/docs/{{version}}/starter-kits)를 제공합니다. 이 패키지들은 현대적인 인증 계층의 스캐폴딩을 제공하며, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/{{version}}/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/{{version}}/fortify)가 대표적입니다.

_Laravel Breeze_ 는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 인증 기능을 미니멀하게 구현한 패키지입니다. 뷰 레이어는 [Blade 템플릿](/docs/{{version}}/blade)으로 되어 있고, [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. 시작하려면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 문서를 참고하세요.

_Laravel Fortify_ 는 Laravel을 위한 헤드리스 인증 백엔드로, 쿠키 기반 인증을 비롯해 2단계 인증, 이메일 인증 등 다양한 기능을 제공합니다. Fortify는 Laravel Jetstream에서 인증 백엔드로 쓰이거나, SPA가 Laravel로 인증할 때 [Sanctum](/docs/{{version}}/sanctum)과 함께 사용할 수 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_은 [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), 그리고 / 또는 [Inertia](https://inertiajs.com)를 기반으로 Fortify의 인증 서비스를 현대적인 UI로 제공하는 강력한 스타터 키트입니다. Jetstream은 2단계 인증, 팀 지원, 브라우저 세션 관리, 프로필 관리, [Laravel Sanctum](/docs/{{version}}/sanctum)과의 API 토큰 인증 등 옵션 기능도 포함하고 있습니다. 보다 자세한 API 인증 관련 설명은 아래에서 이어집니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

API 토큰 관리 및 토큰 인증을 위해 Laravel은 [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum)이라는 두 개의 패키지를 제공합니다. 이들 라이브러리와 Laravel 내장 쿠키 기반 인증 기능은 함께 쓸 수 있습니다. 이 패키지들은 주로 API 토큰 인증에 집중하며, 내장 인증 서비스는 브라우저의 쿠키 인증에 집중합니다. 많은 애플리케이션이 이 두 가지 방식을 모두 사용합니다.

**Passport**

Passport는 여러 OAuth2 "그랜트 타입"을 지원하는 OAuth2 인증 제공자입니다. 다양한 토큰 발급 및 관리 등 robust하고 복잡한 인증 요구 사항에 적합하지만, 대부분의 애플리케이션에는 OAuth2 사양이 제공하는 복잡한 기능까지는 필요하지 않습니다. 또한 SPA 또는 모바일 앱의 인증 방식에 대해 혼란을 겪기도 합니다.

**Sanctum**

OAuth2의 복잡함과 개발자들의 혼란에 대응하기 위해, 좀 더 단순하고 직관적인 인증 패키지로 [Laravel Sanctum](/docs/{{version}}/sanctum)을 개발했습니다. Sanctum은 API, SPA, 일반 웹까지 모두 아우르는 인증 패키지로, 단일 페이지 애플리케이션(SPA), 모바일 앱, 또는 웹 UI+API 조합에 적합합니다.

Sanctum은 하이브리드 웹/API 인증 패키지로, 인증 프로세스 전체를 관리할 수 있습니다. 요청에 세션 쿠키가 있다면 내장 인증 서비스를 통해 인증하고, 쿠키가 없다면 API 토큰을 검사해 인증합니다. 자세한 과정은 Sanctum의 ["동작 방식"](/docs/{{version}}/sanctum#how-it-works) 문서를 참고하세요.

Sanctum은 대부분의 웹 애플리케이션 인증 요구에 가장 적합하다고 판단해 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 키트에 기본 포함되어 있습니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

정리하자면, 브라우저로 접근하는 모놀리식 Laravel 애플리케이션이라면 내장 인증 서비스를 사용하면 됩니다.

서드파티에서 소비될 API를 제공한다면, [Passport](/docs/{{version}}/passport) 또는 [Sanctum](/docs/{{version}}/sanctum)으로 API 토큰 인증을 구현할 수 있습니다. 대체로 Sanctum이 보다 단순하면서도 완벽한 솔루션이므로 권장됩니다.

SPA와 Laravel 백엔드를 함께 개발한다면, [Sanctum](/docs/{{version}}/sanctum)을 쓰세요. 이 때 [인증 라우트를 수동으로 구현](#authenticating-users)하거나, [Fortify](/docs/{{version}}/fortify)를 헤드리스 인증 백엔드로 사용할 수 있습니다.

정말로 OAuth2의 모든 기능이 필요하다면 Passport를 선택하세요.

빠르게 시작하려면, Laravel 내장 인증 기능과 Sanctum이 적용된 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)를 추천합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작

> [!WARNING]  
> 이 문서에서는 UI 스캐폴딩이 포함된 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 활용한 사용자 인증을 다룹니다. 인증 시스템을 직접 통합하고 싶다면 [수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치하기

먼저 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 현재는 Laravel Breeze와 Laravel Jetstream이 대표적이며, 새 Laravel 프로젝트에 인증을 세련되게 적용할 수 있습니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 인증 기능을 심플하게 구현한 미니멀 패키지입니다. 뷰 레이어는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. 또한 [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com) 기반의 스캐폴딩도 선택할 수 있으며, Inertia 기반에서는 Vue 또는 React도 사용 가능합니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 보다 강력한 기능을 제공하는 스타터 키트입니다. [Livewire](https://livewire.laravel.com), [Inertia + Vue](https://inertiajs.com) 중 선택해 스캐폴딩할 수 있습니다. 두 단계 인증, 팀, 프로필 관리, 브라우저 세션 관리, [Sanctum](/docs/{{version}}/sanctum)을 통한 API 지원, 계정 삭제 등 다양한 기능도 포함합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기

인증 스타터 키트 설치 후, 사용자가 회원가입 및 인증할 수 있게 되면 현재 로그인된 사용자와 자주 상호 작용해야 합니다. 요청을 처리하는 중에 `Auth` 파사드의 `user` 메서드를 통해 인증 사용자를 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기...
$user = Auth::user();

// 현재 인증된 사용자의 ID 가져오기...
$id = Auth::id();
```

또는 사용자 인증 후, `Illuminate\Http\Request` 인스턴스에서도 인증 사용자를 얻을 수 있습니다. 컨트롤러 메서드에서 타입힌트로 `Illuminate\Http\Request`를 받으면 언제든 편리하게 `$request->user()`로 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보 수정
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
#### 현재 사용자가 인증되었는지 확인

HTTP 요청을 보낸 사용자가 인증된 상태인지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 인증된 상태면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인 상태임...
}
```
> [!NOTE]  
> `check` 메서드로 인증 상태를 확인할 수 있지만, 일반적으로는 미들웨어로 라우트/컨트롤러에 접근하기 전 인증 상태를 확인합니다. 자세한 내용은 [라우트 보호하기](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/{{version}}/middleware)로 인증된 사용자만 특정 라우트에 접근할 수 있도록 할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어를 기본 제공하므로, 라우트 정의에 미들웨어만 붙이면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, `login` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트합니다. 이 동작을 바꾸고 싶다면 `app/Http/Middleware/Authenticate.php`의 `redirectTo` 메서드를 수정하세요:

```php
use Illuminate\Http\Request;

protected function redirectTo(Request $request): string
{
    return route('login');
}
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

라우트에 `auth` 미들웨어를 붙일 때 특정 가드도 지정할 수 있습니다. 지정한 가드 이름은 `config/auth.php`의 `guards` 배열 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한(Throttling)

Laravel Breeze 또는 Jetstream [스타터 키트](/docs/{{version}}/starter-kits)를 사용하면 로그인 시도 횟수 제한이 자동으로 적용됩니다. 기본적으로 여러 번 실패하면 1분 동안 로그인이 차단됩니다. 제한은 사용자명/이메일과 IP주소 조합마다 개별 적용됩니다.

> [!NOTE]  
> 애플리케이션의 다른 라우트에도 레이트 리밋을 적용하려면 [레이트 리미팅 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증

[애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)가 제공하는 인증 스캐폴딩을 반드시 사용해야 하는 것은 아닙니다. 직접 인증을 구현할 수도 있습니다.

`Auth` [파사드](/docs/{{version}}/facades)를 통해 인증 서비스를 사용할 수 있습니다. 대표적으로 `attempt` 메서드는 로그인 폼에서 인증 시도에 사용합니다. 인증에 성공하면 [세션](/docs/{{version}}/session)을 재생성해 [세션 고정 공격](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%85%98_%EA%B3%A0%EC%A0%95_%EA%B3%B5%EA%B2%A9)을 방지해야 합니다.

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
            'email' => '입력한 정보가 올바르지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 키/값 쌍이 담긴 배열을 첫 인자로 받습니다. 배열의 값으로 데이터베이스에서 사용자를 찾고, 사용자가 있으면 저장된 해시 비밀번호와 입력받은 비밀번호를 비교합니다. **입력받은 비밀번호는 해시하지 않아야 하며, 프레임워크가 알아서 해시해서 비교합니다.** 두 비밀번호가 일치하면 인증 세션이 시작됩니다.

기본적으로 `config/auth.php`의 프로바이더 설정에 따라 사용자를 가져옵니다. 일반적으로 Eloquent 프로바이더가 지정되어 있으며, `App\Models\User` 모델을 사용합니다. 필요에 따라 이 값을 변경할 수 있습니다.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

`redirect()->intended()` 메서드는 인증 미들웨어에 의해 이전에 접근이 차단된 URL로 리다이렉트합니다. 설정된 URL이 없으면 대체 URL을 전달할 수도 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

원한다면 이메일/비밀번호 이외의 조건도 추가할 수 있습니다. 조건을 배열에 추가하면 됩니다. 예시로, 사용자가 "active"일 때만 인증하도록 할 수 있습니다.

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

복잡한 쿼리 조건의 경우, 배열에서 클로저를 통해 쿼리 인스턴스를 조작할 수 있습니다.

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
> 위 예시에서 `email`은 단지 예시일 뿐 필수 옵션이 아닙니다. 실제로는 데이터베이스에서 사용자명을 나타내는 컬럼명을 사용해야 합니다.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아, 조건부로 인증 전에 심층 검사를 수행할 수 있습니다. 예를 들어, 사용자가 금지(banned) 상태인지 검사할 수 있습니다.

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
#### 특정 가드 인스턴스 사용

`Auth` 파사드의 `guard` 메서드로 인증 시 사용할 가드를 지정할 수 있습니다. 이를 통해 인증 대상을 분리(예: 관리자/일반 사용자)할 수 있습니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기(Remember Me)

많은 웹 앱에 로그인 폼에 "로그인 상태 유지" 체크박스가 있습니다. 이 기능을 제공하려면, `attempt` 메서드에 두 번째 인자로 불리언 값을 전달하면 됩니다. 값이 `true`면, 사용자가 직접 로그아웃하지 않는 이상 계속 인증 상태가 유지됩니다. 이 기능을 위해 `users` 테이블에 `remember_token` 문자열 컬럼이 필요하며, 기본 마이그레이션에 이미 포함되어 있습니다.

```php
use Illuminate\Support\Facades/Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 이 사용자는 기억됨...
}
```

"로그인 상태 유지"로 인증된 사용자인지는 `viaRemember` 메서드로 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 직접 인증하기

이미 인증된 사용자 인스턴스가 있다면, `Auth` 파사드의 `login` 메서드에 인스턴스를 전달해 현재 로그인 사용자로 설정할 수 있습니다. 전달되는 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약(Contract)](/docs/{{version}}/contracts)을 구현해야 하며, 기본 `App\Models\User`는 이미 구현되어 있습니다. 보통 회원가입 직후 등에서 자주 사용됩니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

두 번째 인자로 `true`를 전달하면 Remember Me 기능이 적용됩니다.

```php
Auth::login($user, $remember = true);
```

필요하다면 로그인 전 인증 가드를 지정할 수 있습니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증

데이터베이스의 기본 키로 사용자를 인증하려면 `loginUsingId` 메서드를 사용하세요.

```php
Auth::loginUsingId(1);
```

두 번째 인자는 Remember Me 기능을 위한 옵션입니다.

```php
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
#### 1회성 사용자 인증

`once` 메서드는 세션이나 쿠키 없이, 요청 한 번만 인증할 수 있습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://ko.wikipedia.org/wiki/HTTP_%EA%B8%B0%EB%B3%B8_%EC%9D%B8%EC%A6%9D)은 별도의 로그인 페이지 구현 없이 간단하게 인증할 수 있는 방법입니다. `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 라우트에 적용하면 됩니다. 이 미들웨어는 Laravel에 이미 포함되어 있습니다.

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth.basic');
```

미들웨어가 라우트에 적용되면 브라우저에서 해당 경로를 접근할 때 인증 정보 입력 프롬프트가 자동으로 뜹니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자의 "username"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고

PHP FastCGI와 Apache를 함께 사용할 때, HTTP Basic 인증이 제대로 작동하지 않을 수 있습니다. 문제가 발생하면, 애플리케이션 `.htaccess`에 다음 내용을 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP Basic 인증

세션에 사용자 식별자 쿠키를 저장하지 않고, HTTP Basic 인증을 사용할 수도 있습니다. 주로 API 요청 인증에 활용됩니다. 이를 위해 `onceBasic` 메서드를 호출하는 미들웨어를 정의하세요.

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
     * 요청 처리
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

그리고 해당 미들웨어를 라우트에 적용합니다.

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃

사용자를 수동으로 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 사용하면 됩니다. 이 메서드는 세션의 인증 정보를 삭제하여, 이후 요청이 인증되지 않게 만듭니다.

로그아웃 이후에는 세션을 무효화하고, [CSRF 토큰](/docs/{{version}}/csrf)을 재생성하는 것이 권장됩니다. 주로 로그아웃 후 루트 경로로 리다이렉트합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 사용자 로그아웃 처리
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
### 다른 기기에서 세션 무효화

Laravel은 현재 기기를 제외한 다른 모든 기기/브라우저의 세션을 무효화(강제 로그아웃)하는 기능을 제공합니다. 보통 비밀번호 변경 시, 다른 기기는 로그아웃시키고 현재 기기는 유지할 때 사용합니다.

먼저 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어를 인증 세션이 필요한 라우트에 포함시켜야 합니다. 주로 라우트 그룹에 미들웨어를 걸어 두면 대부분의 라우트에 적용할 수 있습니다. `auth.session` 별칭을 사용해 쉽게 지정할 수 있습니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용합니다. 이 메서드는 사용자의 현재 비밀번호를 입력받아야 하며, 비밀번호 확인 폼을 통해 값을 받아야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

이 메서드 실행 시 사용자가 기존에 인증된 다른 모든 기기에서 강제 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인(Password Confirmation)

애플리케이션에서 중요한 액션 수행이나 민감한 영역 이동 전, 사용자의 비밀번호를 재확인하고 싶을 때가 있습니다. Laravel은 이를 위한 미들웨어를 기본 제공하며, 구현 시 뷰를 반환하는 라우트와 비밀번호를 확인하는 라우트, 두 가지를 따로 정의해야 합니다.

> [!NOTE]  
> 이 아래의 내용은 Laravel 비밀번호 확인 기능을 직접 통합하는 방법을 설명하지만, [스타터 키트](/docs/{{version}}/starter-kits)에도 이미 관련 기능이 포함되어 있습니다.

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호를 한번 확인하면 3시간 동안 재확인 요구가 없습니다. 이 시간은 `config/auth.php`에서 `password_timeout` 설정을 변경해 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자에게 비밀번호를 입력받는 뷰를 반환하는 라우트를 정의합니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트가 반환하는 뷰에는 `password` 입력 필드가 있어야 하며, 사용자에게 보호된 영역임을 알리는 문구를 포함해도 좋습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

폼에서 제출된 값을 처리하는 라우트를 정의합니다. 이 라우트는 비밀번호가 맞는지 검증하며, 맞다면 사용자를 원래 목적지로 리다이렉트합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['입력한 비밀번호가 올바르지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

이 라우트의 처리 흐름은 이렇습니다. 먼저 입력받은 비밀번호가 실제 로그인된 사용자의 비밀번호와 일치하는지 확인합니다. 올바를 경우 Laravel 세션에 비밀번호 확인 시각 정보를 저장합니다. 마지막으로 사용자가 가려던 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

최근 비밀번호 확인이 필요한 모든 라우트에는 `password.confirm` 미들웨어를 붙여야 합니다. 이 미들웨어는 사용자의 원래 목적지 정보를 세션에 저장해 두었다가 비밀번호 확인 후 자동으로 그 위치로 리다이렉트합니다. 일단 목적지가 세션에 저장되면, 미들웨어가 `password.confirm` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트합니다.

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

`Auth` 파사드의 `extend` 메서드를 사용해 직접 커스텀 인증 가드를 정의할 수 있습니다. 이 호출은 [서비스 프로바이더](/docs/{{version}}/providers) 내에서 이뤄져야 하며, 기본 제공되는 `AuthServiceProvider`에 작성 가능합니다.

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 인증/인가 서비스 등록
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 구현체 반환

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

콜백 함수는 `Illuminate\Contracts\Auth\Guard` 인터페이스를 구현한 객체를 반환하면 됩니다. 커스텀 가드가 정의된 이후 `auth.php`의 `guards` 설정에서 참조할 수 있습니다.

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

HTTP 요청 기반의 인증 시스템을 가장 간단하게 구현하려면, `Auth::viaRequest` 메서드를 사용할 수 있습니다. 이 메서드는 인증 프로세스를 단일 클로저로 정의할 수 있습니다.

`AuthServiceProvider`의 `boot` 메서드 내에 아래와 같이 호출합니다. 첫 번째 인자는 드라이버 이름(아무 문자열 가능), 두 번째 인자는 HTTP 요청을 받아 사용자 인스턴스를 반환하거나 인증에 실패하면 `null`을 반환하는 클로저입니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 인증/인가 서비스 등록
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

정의가 완료된 드라이버는 `auth.php`의 `guards` 설정에 지정할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 미들웨어에 가드 이름을 지정해서 사용할 수 있습니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 유저 프로바이더 추가

관계형 데이터베이스가 아닌 곳에 사용자를 저장한다면, 커스텀 인증 유저 프로바이더를 직접 만들어 Laravel에 등록해야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해 프로바이더를 정의합니다. 프로바이더 리졸버는 `Illuminate\Contracts\Auth\UserProvider`를 구현해야 합니다.

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 인증/인가 서비스 등록
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 구현체 반환

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

등록 후, `auth.php` 설정 파일에서 프로바이더를 지정합니다.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그리고 이 프로바이더를 사용하는 가드를 설정합니다.

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### User Provider 계약(Contract)

`Illuminate\Contracts\Auth\UserProvider`의 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등에서 어떻게 가져올지 정의합니다. 이 두 인터페이스 덕분에 사용자 정보 저장방식과 모델이 달라도 인증이 작동합니다.

아래는 `Illuminate\Contracts\Auth\UserProvider` 계약의 예시입니다.

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

- `retrieveById`는 주로 (예: MySQL 오토 인크리먼트) 기본키를 받아 해당 사용자를 반환합니다.
- `retrieveByToken`은 유니크 `$identifier`와 "remember me" `$token`으로 사용자를 찾습니다. 보통 `remember_token` 컬럼을 이용합니다.
- `updateRememberToken`은 주어진 `$user` 객체의 `remember_token`을 갱신합니다. "로그인 유지" 성공 시 또는 로그아웃 시 호출됩니다.
- `retrieveByCredentials`는 `Auth::attempt`에 전달된 자격증명 배열을 받아, 해당하는 사용자를 조회(검색)합니다. **이 메서드는 비밀번호 검증을 직접 하면 안됩니다.**
- `validateCredentials`는 주어진 `$user`와 `$credentials` 배열을 비교해 사용자를 인증합니다. 주로 `Hash::check`로 비밀번호를 검증합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약(Contract)

이제 `UserProvider`에서 반환해야 하는 `Authenticatable` 계약 인터페이스를 살펴보겠습니다. `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 등에서 반환해야 합니다.

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

- `getAuthIdentifierName`은 기본키 필드명을,
- `getAuthIdentifier`는 사용자의 기본키 값을,
- `getAuthPassword`는 해시된 비밀번호를 반환해야 합니다.

이 인터페이스 덕분에 ORM/스토리지 레이어와 관계없이 인증 시스템이 동작합니다. Laravel은 기본적으로 `app/Models/User` 클래스에서 이미 이 인터페이스를 구현합니다.

<a name="events"></a>
## 이벤트

인증 처리 과정에서 Laravel은 [여러 이벤트](/docs/{{version}}/events)를 발행합니다. `EventServiceProvider`에서 이러한 이벤트에 리스너를 등록할 수 있습니다.

```php
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
