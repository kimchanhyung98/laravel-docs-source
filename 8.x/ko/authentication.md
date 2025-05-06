# 인증(Authentication)

- [소개](#introduction)
    - [스타터 킷](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 킷 설치](#install-a-starter-kit)
    - [인증된 사용자 가져오기](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 제한(쓰로틀링)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [무상태 HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 기반 요청 가드](#closure-request-guards)
- [커스텀 사용자 프로바이더 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션에서는 사용자가 애플리케이션에 로그인할 수 있는 인증 방법을 제공합니다. 이러한 기능을 구현하는 것은 복잡하며, 잠재적으로 위험할 수 있습니다. 그래서 라라벨은 인증 기능을 빠르고, 안전하며, 쉽게 구현할 수 있도록 다양한 도구를 제공합니다.

라라벨 인증의 핵심은 "가드(guards)"와 "프로바이더(providers)"로 이루어져 있습니다. 가드는 각 요청별로 사용자가 어떻게 인증될지 정의합니다. 예를 들어, 라라벨에는 세션 스토리지와 쿠키를 사용하여 상태를 유지하는 `session` 가드가 기본 제공됩니다.

프로바이더는 영구 저장소에서 사용자를 어떻게 가져올지 정의합니다. 라라벨은 [Eloquent](/docs/{{version}}/eloquent)와 데이터베이스 쿼리 빌더를 통한 사용자 조회를 지원합니다. 물론, 필요하다면 애플리케이션에 맞는 추가 프로바이더를 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 있습니다. 이 파일에는 인증 서비스 동작을 조정할 수 있는 다양한 옵션이 잘 문서화되어 있습니다.

> {tip} 가드와 프로바이더는 "역할(roles)"과 "권한(permissions)"과 혼동하지 말아야 합니다. 권한을 통한 사용자 액션 허용 방법은 [권한 부여](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 킷

빠르게 시작하고 싶으신가요? 새로운 라라벨 프로젝트에서 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치하세요. 데이터베이스를 마이그레이션한 후, 브라우저에서 `/register` 또는 지정한 URL로 이동하면, 스타터 킷이 전체 인증 시스템을 자동으로 생성해줍니다!

**설령 실제 프로젝트에서 스타터 킷을 최종적으로 사용하지 않더라도, [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 스타터 킷을 설치해 라라벨 인증 기능 전체를 실제 프로젝트에서 어떻게 구현하는지 학습하는 데 큰 도움이 됩니다.** Breeze는 인증 컨트롤러, 라우트, 뷰까지 생성해주므로, 이 파일들을 살펴보면서 라라벨 인증 기능이 어떻게 작동하는지 배울 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

기본적으로, 라라벨은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. Eloquent를 사용하지 않는 경우, 라라벨 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다.

`App\Models\User` 모델을 위한 데이터베이스 스키마를 만들 때, `password` 컬럼이 최소 60자 이상이어야 합니다. 물론, 최신 라라벨의 `users` 테이블 마이그레이션은 이미 이 조건을 만족하는 컬럼을 만들어줍니다.

또한, `users`(혹은 해당하는) 테이블에 100자 길이의 null 허용, 문자형 `remember_token` 컬럼이 있는지 확인해야 합니다. 로그인 시 "로그인 상태 유지"를 선택한 사용자의 토큰을 저장하는 데 필요합니다. 이 컬럼도 기본 `users` 테이블 마이그레이션에 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

라라벨은 인증과 관련된 다양한 패키지를 제공합니다. 본격적으로 시작하기 전에, 라라벨의 전체 인증 생태계를 개괄적으로 살펴보고 각 패키지의 목적을 설명하겠습니다.

먼저 인증이 어떻게 동작하는지 생각해봅시다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼에 사용자명과 비밀번호를 입력합니다. 올바른 자격증명이 입력되면, 애플리케이션은 인증된 사용자 정보를 [세션](/docs/{{version}}/session)에 저장합니다. 브라우저에는 세션 ID가 들어있는 쿠키가 발급되어, 이후 요청 시 올바른 세션과 사용자를 연결할 수 있게 합니다. 이후의 요청에서는 애플리케이션이 세션 ID를 활용해 세션 데이터를 조회하고, 세션에 인증 정보가 있음을 확인해 사용자를 "인증됨"으로 처리합니다.

원격 서비스가 API에 접근하기 위해 인증이 필요할 경우, 브라우저가 없으므로 쿠키 인증 대신 요청마다 API 토큰을 전송합니다. 애플리케이션은 해당 토큰이 유효 토큰 테이블에 있는지 검사해, 토큰 소유 사용자로 인증을 수행합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### 라라벨 내장 브라우저 인증 서비스

라라벨은 기본적으로 `Auth` 및 `Session` 파사드로 접근할 수 있는 인증 및 세션 서비스를 제공합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자 자격 증명 검증, 인증, 세션에 올바른 인증 정보 자동 저장 및 세션 쿠키 발급 기능을 제공합니다. 본 문서는 이러한 서비스 사용법을 설명합니다.

**애플리케이션 스타터 킷**

이 문서에서 설명하듯, 애플리케이션 인증 계층을 직접 구축하고 싶다면 인증 서비스를 수동으로 사용할 수 있습니다. 하지만 더 빠른 시작을 위해 [무료 패키지](/docs/{{version}}/starter-kits)도 준비되어 있습니다. 이 패키지들은 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/{{version}}/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/{{version}}/fortify)입니다.

_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 라라벨 인증의 모든 기능을 간단하게 구현한 최소(미니멀) 패키지입니다. 뷰 레이어는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구동됩니다. 시작하려면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 문서를 참고하세요.

_Laravel Fortify_는 라라벨을 위한 헤드리스 인증 백엔드로, 쿠키 기반 인증, 2단계 인증, 이메일 인증 등 이 문서에서 언급한 많은 기능을 제공합니다. Fortify는 [Laravel Jetstream](https://jetstream.laravel.com)의 인증 백엔드이거나, [Laravel Sanctum](/docs/{{version}}/sanctum)과 결합하여 SPA 인증도 구성할 수 있습니다.

_[Laravel Jetstream](https://jetstream.laravel.com)_은 Fortify의 인증 서비스를 바탕으로, [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), [Inertia.js](https://inertiajs.com)를 활용한 강력한 UI를 포함하는 스타터 킷입니다. 2단계 인증, 팀 지원, 브라우저 세션 관리, 프로필 관리, [Laravel Sanctum](/docs/{{version}}/sanctum) 연계 API 토큰 인증 등을 옵션으로 포함합니다. API 인증 기능은 다음에서 다룹니다.

<a name="laravels-api-authentication-services"></a>
#### 라라벨 API 인증 서비스

라라벨은 API 토큰을 관리하고 인증하는 데 도움이 되는 두 가지 선택적 패키지 [Passport](/docs/{{version}}/passport) 및 [Sanctum](/docs/{{version}}/sanctum)을 제공합니다. 이 라이브러리와 라라벨의 내장 쿠키 기반 인증 라이브러리는 서로 배타적이지 않습니다. 이 패키지는 주로 API 토큰 인증에, 기본 인증 서비스는 쿠키 기반 브라우저 인증에 집중합니다. 많은 애플리케이션이 둘 다 함께 사용할 수 있습니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"을 지원하는 OAuth2 인증 제공자입니다. API 인증에 있어서 강력하며 복잡한 패키지입니다. 하지만 대부분의 앱에서는 복잡한 OAuth2 스펙이 필요 없고, 오히려 사용자와 개발자 모두에게 혼란을 줄 수 있습니다. 특히 SPA나 모바일 앱에서 어떻게 OAuth2로 인증하는지 혼란스러워하는 경우가 많습니다.

**Sanctum**

OAuth2의 복잡성과 개발자 혼란을 줄이기 위해, 우리는 브라우저 기반의 1st-party 웹 요청과 토큰 기반 API 요청 모두 단순하게 처리할 수 있는 인증 패키지를 만들었습니다. 바로 [Laravel Sanctum](/docs/{{version}}/sanctum)입니다. Sanctum은 API와 함께 제공되는 1st-party 웹 UI가 있는 앱, 또는 백엔드와 분리된 SPA, 모바일 앱을 지원하는 권장 인증 패키지입니다.

Sanctum은 웹/API 하이브리드 인증 패키지로, 인증 전 과정을 관리할 수 있습니다. Sanctum이 설치된 애플리케이션에 요청이 오면, 먼저 세션 쿠키가 포함되어 있는지 확인해 내장 인증 서비스를 호출합니다. 세션 쿠키로 인증하지 않은 경우엔 API 토큰을 검사해 해당 토큰으로 요청을 인증합니다. 자세한 작동 원리는 Sanctum의 ["작동 방식"](/docs/{{version}}/sanctum#how-it-works) 문서를 참고하세요.

우리는 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 킷에 API 인증 패키지로 Sanctum이 포함되어 있도록 선택했습니다. 대부분의 웹 앱 인증 요구에 가장 적합하기 때문입니다.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

정리하면, 브라우저에서 접근하는 모놀리식 라라벨 애플리케이션의 경우 내장 인증 서비스를 사용합니다.

외부 파티에서 사용할 API가 있다면, [Passport](/docs/{{version}}/passport) 또는 [Sanctum](/docs/{{version}}/sanctum) 중 하나로 API 토큰 인증을 구현합니다. 대체로 Sanctum이 쉽고 완전한 솔루션이므로 추천됩니다. 스코프(scope)나 기능(abilities)도 포함하고 있습니다.

Laravel 백엔드 기반 SPA라면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하세요. 이때 인증 라우트를 직접 구현하거나, [Laravel Fortify](/docs/{{version}}/fortify)를 헤드리스 인증 서비스로 활용해 등록, 비밀번호 재설정, 이메일 인증 등 기능을 바로 사용할 수 있습니다.

OAuth2 표준의 모든 기능이 반드시 필요할 경우에만 Passport를 사용하세요.

빠르게 시작하고 싶으시다면 [Laravel Jetstream](https://jetstream.laravel.com)을 추천합니다. Jetstream은 내장 인증 서비스와 Sanctum을 사용한 권장 인증 스택으로 미리 구성되어 있습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작

> {note} 이 부분은 [라라벨 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 통한 인증에 대해 다룹니다. UI 스캐폴딩이 포함되어 빠른 시작에 적합합니다. 인증 기능을 직접 연동하려면, [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 킷 설치

우선, [라라벨 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치하세요. 현재 제공되는 Laravel Breeze, Laravel Jetstream 스타터 킷은 인증 기능이 멋지게 디자인되어 탑재되어 있습니다.

Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 인증 기능의 간단하고 최소한의 구현체입니다. 뷰 레이어는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되었습니다. Inertia를 활용해 Vue 또는 React로 스캐폴딩도 가능합니다.

[Laravel Jetstream](https://jetstream.laravel.com)은 더욱 강력한 스타터 킷입니다. [Livewire](https://laravel-livewire.com)나 [Inertia.js & Vue](https://inertiajs.com)를 통한 스캐폴딩을 지원하며, 2단계 인증, 팀, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/{{version}}/sanctum) 기반 API, 계정 삭제 등 다양한 기능을 옵션으로 포함합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 가져오기

인증 스타터 킷 설치 후 사용자가 회원가입 및 로그인에 성공했다면, 종종 현재 인증된 사용자와 상호작용해야 할 경우가 있습니다. 요청 처리가 진행 중일 때, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 가져오기
$user = Auth::user();

// 현재 인증된 사용자 ID 가져오기
$id = Auth::id();
```

사용자가 이미 인증을 마쳤다면, `Illuminate\Http\Request` 인스턴스를 통해서도 인증 사용자에 접근할 수 있습니다. 타입힌트된 클래스는 컨트롤러 메서드에 자동 주입됩니다. `Illuminate\Http\Request`를 타입힌트로 지정하면, 요청 객체의 `user` 메서드를 통해 편리하게 인증 사용자에 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편의 정보를 업데이트합니다.
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
#### 현재 사용자가 인증되었는지 판별

현재 HTTP 요청을 보낸 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하면 됩니다. 사용자가 인증된 경우 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인되었습니다...
}
```

> {tip} `check` 메서드로 인증 여부를 직접 확인할 수도 있으나, 실제로는 특정 라우트나 컨트롤러 접근 전에 미들웨어를 통해 인증 검증을 하는 것이 일반적입니다. 자세한 내용은 [라우트 보호하기](/docs/{{version}}/authentication#protecting-routes) 문서를 확인하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/{{version}}/middleware)를 이용해, 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. 라라벨에는 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어가 기본 제공됩니다. HTTP 커널에 이미 등록돼 있으므로, 아래와 같이 미들웨어만 라우트에 추가하면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 미인증 사용자 리다이렉트

`auth` 미들웨어가 미인증 사용자를 감지하면, 해당 사용자를 `login` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉션합니다. 이 동작은 `app/Http/Middleware/Authenticate.php` 파일의 `redirectTo` 함수를 수정해 변경할 수 있습니다:

```php
/**
 * 사용자가 리다이렉트되어야 할 경로 반환.
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
#### 가드 지정

`auth` 미들웨어를 라우트에 추가할 때, 어떤 "가드"로 인증할지 지정할 수 있습니다. 지정하는 가드 이름은 `auth.php` 설정 파일의 `guards` 배열 키와 일치해야 합니다.

```php
Route::get('/flights', function () {
    // admin 가드로 인증된 사용자만 접근 가능
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 쓰로틀링(제한)

라라벨 Breeze 또는 Laravel Jetstream [스타터 킷](/docs/{{version}}/starter-kits)을 사용할 경우, 로그인 시도에 자동으로 속도 제한(쓰로틀)이 적용됩니다. 기본적으로 여러 번 잘못 입력하면 1분동안 로그인할 수 없습니다. 쓰로틀 기준은 사용자의 사용자명/이메일과 IP로 구분됩니다.

> {tip} 애플리케이션의 다른 라우트에도 속도 제한을 적용하려면 [속도 제한 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증

[애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)의 인증 스캐폴딩은 필수 사항이 아닙니다. 스캐폴딩을 사용하지 않으려면, 라라벨 인증 클래스를 직접 사용하여 인증을 관리해야 합니다. 걱정 마세요. 매우 간단합니다!

인증 서비스는 `Auth` [파사드](/docs/{{version}}/facades)로 접근합니다. 클래스 상단에서 `Auth` 파사드를 임포트하세요. 그 다음 `attempt` 메서드를 확인해보겠습니다. `attempt`는 주로 로그인 폼에서 인증 시도에 사용됩니다. 인증이 성공하면, [세션 고정 공격](https://en.wikipedia.org/wiki/Session_fixation) 예방을 위해 사용자의 [세션](/docs/{{version}}/session)을 재생성해야 합니다.

```php
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
            'email' => '제공된 자격증명이 일치하지 않습니다.',
        ]);
    }
}
```

`attempt` 메서드의 첫 인자로 전달된 키/값 배열의 값이 DB의 사용자를 찾는 데 사용됩니다. 위의 예에서는 `email` 컬럼 값으로 사용자를 조회합니다. 사용자가 존재하면, 데이터베이스에 저장된 해시된 비밀번호와 입력한 `password` 값이 비교됩니다. 입력 비밀번호는 직접 해시하지 않아도 됩니다. 라라벨은 자동으로 비교 전에 해싱합니다. 두 비밀번호가 일치하면 인증된 세션이 시작됩니다.

라라벨 인증 서비스는 설정한 가드의 "프로바이더" 설정에 따라 사용자 데이터를 불러옵니다. 기본 `config/auth.php` 파일에서는 Eloquent 사용자 프로바이더가 지정되어 있고, 사용자 조회시 `App\Models\User` 모델을 사용하도록 설정되어 있습니다. 이 부분은 애플리케이션 요구에 맞게 파일 내에서 조정할 수 있습니다.

인증이 성공하면 `attempt`는 `true`, 실패하면 `false`를 반환합니다.

라라벨의 `intended` 메서드는 사용자가 인증 미들웨어에 의해서 차단되기 전, 접근하려던 URL로 리다이렉트시켜줍니다. 만약 해당 목적지 URL이 없으면 예비 URL로 대체할 수도 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

원한다면, 사용자 이메일/비밀번호 외에 추가 쿼리 조건을 지정할 수도 있습니다. 단순히 조건을 `attempt` 메서드 배열에 추가하면 됩니다. 예를 들어, `active` 상태도 검사하려면:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공
}
```

> {note} 여기서 `email`은 예시일 뿐이며, 실제로는 DB 테이블의 사용자명 컬럼명에 맞춰 사용하세요.

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근

`Auth` 파사드의 `guard` 메서드를 사용하면, 어떤 가드 인스턴스(예: admin 등)로 인증할지 지정할 수 있습니다. 이렇게 하면, 애플리케이션 내 별도의 사용자 모델/테이블을 사용하는 여러 인증 영역을 분리 관리할 수 있습니다.

`guard` 메서드에 전달한 가드명은 `auth.php`의 guards 설정과 일치해야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 앱은 로그인 폼에 "로그인 상태 유지" 체크박스를 제공합니다. 이 기능을 구현하려면, `attempt` 메서드의 두 번째 인자로 boolean 값을 전달합니다.

이 값이 `true`면, 사용자는 수동 로그아웃 시까지 인증 상태가 유지됩니다. `users` 테이블에는 "remember me" 토큰을 저장할 `remember_token` 컬럼이 반드시 있어야 하며, 최신 라라벨엔 기본 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억됨
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 직접 인증

이미 존재하는 사용자 인스턴스를 현재 인증 사용자로 설정하려면, `Auth` 파사드의 `login` 메서드에 인스턴스를 전달하면 됩니다. 전달하는 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/{{version}}/contracts)을 구현해야 합니다. Laravel의 기본 `App\Models\User` 모델은 이미 구현되어 있습니다. 이 방법은 예를 들어 회원가입 직후 인증한 경우에 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인자로 boolean 값을 전달해 "로그인 상태 유지"도 설정할 수 있습니다.

```php
Auth::login($user, $remember = true);
```

필요하다면 인증 가드를 지정 후 `login` 호출도 가능합니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증

DB의 기본 키로 사용자를 인증하려면, `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증할 사용자의 기본 키를 인자로 받습니다.

```php
Auth::loginUsingId(1);
```

두 번째 인자로 "로그인 상태 유지" 여부도 지정 가능합니다.

```php
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 사용자 인증

`once` 메서드를 사용하면, 1회 요청에 한해 사용자를 인증할 수 있습니다. 이 방식은 세션/쿠키를 생성하지 않습니다.

```php
if (Auth::once($credentials)) {
    //
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://ko.wikipedia.org/wiki/HTTP_기본_인증)은 별도의 로그인 페이지 없이 빠르게 사용자를 인증할 수 있는 방법입니다. 시작하려면, 경로에 `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 추가하세요. `auth.basic`은 라라벨에 기본 포함되어 있습니다.

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth.basic');
```

미들웨어가 적용된 라우트에 접근하면 브라우저에서 사용자 인증 정보 입력이 자동으로 프롬프트됩니다. 기본적으로, `auth.basic` 미들웨어는 `users` DB 테이블의 `email` 컬럼을 사용자명으로 사용합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 주의사항

PHP FastCGI와 Apache로 라라벨 앱을 제공하는 경우, HTTP Basic 인증이 올바르게 동작하지 않을 수 있습니다. 아래 라인을 `.htaccess` 파일에 추가하면 문제를 해결할 수 있습니다.

```
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 무상태 HTTP Basic 인증

세션에 사용자 식별용 쿠키를 저장하지 않고 HTTP Basic 인증을 사용할 수도 있습니다. 이는 음성 API 인증을 위해 HTTP Basic을 사용할 때 유용합니다. [미들웨어](/docs/{{version}}/middleware)를 정의하여 `onceBasic` 메서드를 호출하면 됩니다. 이 메서드로 응답이 반환되지 않으면 요청이 다음으로 전달됩니다.

```php
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

미들웨어를 [등록](/docs/{{version}}/middleware#registering-middleware)한 뒤, 라우트에 추가하세요.

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능
})->middleware('auth.basic.once');
```

<a name="logging-out"></a>
## 로그아웃

사용자를 수동으로 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 사용하면 됩니다. 이 메서드는 세션의 인증 정보를 제거해, 이후 요청에 인증이 적용되지 않도록 합니다.

그뿐만 아니라, 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/{{version}}/csrf)을 재생성하는 것이 좋습니다. 로그아웃 후에는 대개 애플리케이션의 루트로 리다이렉트합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션에서 사용자를 로그아웃시킵니다.
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
### 다른 기기에서 세션 무효화

라라벨은 현재 기기를 제외한 모든 기기에서 사용자의 세션을 무효화(로그아웃)하는 기능을 제공합니다. 이 기능은 사용자가 비밀번호를 변경하거나 업데이트할 때, 다른 기기에서의 세션을 만료시키고 싶을 때 사용합니다.

우선 `App\Http\Kernel` 클래스의 `web` 미들웨어 그룹 내에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 활성화되어 있는지 확인하세요.

```php
'web' => [
    // ...
    \Illuminate\Session\Middleware\AuthenticateSession::class,
    // ...
],
```

그 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 현재 비밀번호를 입력받아야 하며, 입력된 비밀번호를 확인해야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

이 메서드를 호출하면 해당 사용자의 다른 세션이 전부 무효화(로그아웃)됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인

어플리케이션에서 특정 액션 시 또는 민감한 영역에 접근할 때, 사용자의 비밀번호를 확실히 재확인하고 싶을 때가 있습니다. 라라벨은 이 작업을 쉽게 처리할 수 있는 내장 미들웨어를 제공합니다. 이 기능을 구현하려면, 비밀번호를 재확인 요청하는 뷰를 보여주는 라우트와, 비밀번호를 검증하고 사용자를 원하는 위치로 보내주는 라우트 두 개가 필요합니다.

> {tip} 아래 문서는 라라벨의 비밀번호 확인 기능을 직접 연동하는 방법이며, 더욱 빠른 시작을 원하면 [라라벨 스타터 킷](/docs/{{version}}/starter-kits)에도 이 기능이 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호를 확인하면, 그 후 3시간 동안은 다시 확인하지 않아도 됩니다. 이 시간은 `config/auth.php`의 `password_timeout` 설정값을 변경하여 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 아래와 같이 사용자의 비밀번호를 입력받는 뷰를 보여주는 라우트를 만듭니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 뷰에는 `password` 필드가 존재하는 폼이 있어야 합니다. 또한 이 영역이 보호되고 있음을 안내하는 설명을 추가할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

사용자가 폼을 제출하면 비밀번호 유효성 체크 후 사용자를 원래 위치로 리다이렉트하는 라우트를 정의합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['입력한 비밀번호가 일치하지 않습니다.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

이 라우트에서는 먼저 입력된 비밀번호와 실제로 인증된 사용자 비밀번호가 일치하는지 확인합니다. 유효하면 세션에 비밀번호 확인 시각을 저장합니다. 그 뒤 사용자를 원래 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

비밀번호 재확인이 필요한 라우트는 반드시 `password.confirm` 미들웨어가 추가되어야 합니다. 이 미들웨어는 사용자의 목적지를 세션에 저장 후, `password.confirm` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 사용자를 리다이렉트합니다.

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

`Auth` 파사드의 `extend` 메서드를 사용해 커스텀 인증 가드를 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/{{version}}/providers) 내에 위치해야 하며, 이미 내장된 `AuthServiceProvider`에 작성하면 됩니다.

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 인증/권한 서비스를 등록합니다.
     *
     * @return void
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

위 예시처럼, `extend`의 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 하며, 이 인터페이스의 메서드를 구현해야 합니다. 커스텀 가드를 정의했다면 `auth.php` 설정 파일의 guards에서 해당 가드를 참조합니다.

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

가장 손쉽게 HTTP 요청 기반 커스텀 인증 시스템을 구현하는 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 인증 로직을 하나의 클로저로 빠르게 정의할 수 있습니다.

`AuthServiceProvider`의 `boot` 메서드에서 아래와 같이 사용합니다. 첫 번째 인자로는 인증 가드명을, 두 번째 인자로는 요청을 받아 사용자 인스턴스나 인증 실패 시 `null`을 반환하는 클로저를 전달하세요.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 인증/권한 서비스 등록
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

커스텀 인증 드라이버가 정의되면, `auth.php` 설정에서 guards에 드라이버로 지정할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 프로바이더 추가

관계형 데이터베이스가 아닌 곳에 사용자를 저장하는 경우, 라라벨에 커스텀 사용자 프로바이더를 확장해 구현해야 합니다. `Auth` 파사드의 `provider` 메서드로 새로운 프로바이더를 등록하세요. 반환 값은 반드시 `Illuminate\Contracts\Auth\UserProvider` 계약을 구현해야 합니다.

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
     *
     * @return void
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

`provider`로 등록한 후에는 `auth.php` 설정에서 새로운 프로바이더를 선언하세요.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그리고 `guards`의 provider에 이 프로바이더를 참조하면 됩니다.

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### UserProvider 계약

`Illuminate\Contracts\Auth\UserProvider` 구현체는 영구 스토리지에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스 덕분에, 사용자가 어떻게 저장되든/어떤 클래스를 사용하든 라라벨 인증이 동작할 수 있습니다.

`UserProvider` 계약 예시는 아래와 같습니다.

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

- `retrieveById`: 주로 MySQL ID 등 사용자 식별자로 사용자를 찾습니다. 해당 사용자 인스턴스를 반환합니다.
- `retrieveByToken`: 주로 DB의 `remember_token` 컬럼에 저장된 "로그인 상태 유지" 토큰으로 사용자를 찾습니다.
- `updateRememberToken`: 인증 때나 로그아웃 시 사용자의 `remember_token`을 새 토큰으로 갱신합니다.
- `retrieveByCredentials`: `Auth::attempt`에 전달된 자격증명 배열로 사용자를 찾습니다. `where` 조건문 등으로 찾고, 반드시 비밀번호 검증이나 인증을 이 메서드에서 수행하지 않아야 합니다.
- `validateCredentials`: 전달된 사용자와 자격증명을 비교해 실제로 사용자를 인증합니다. 대개 `Hash::check`를 이용해 비밀번호 비교를 수행합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

`UserProvider`의 각 메서드에서 반환해야 하는 `Authenticatable`의 계약 예시는 아래와 같습니다.

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

- `getAuthIdentifierName`: 사용자 모델의 "기본 키" 컬럼명을 반환
- `getAuthIdentifier`: 사용자의 기본 키 값을 반환
- `getAuthPassword`: 해싱된 비밀번호를 반환

이 인터페이스 덕분에 인증 시스템은 어떤 ORM, 어떤 저장소를 쓰든, 어떤 "사용자" 클래스를 쓰든 동작할 수 있습니다. 기본적으로는 `app/Models/User` 클래스가 이 인터페이스를 구현합니다.

<a name="events"></a>
## 이벤트

라라벨은 인증 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다. `EventServiceProvider`에서 리스너를 연결할 수 있습니다.

```php
/**
 * 애플리케이션의 이벤트 리스너 매핑
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
