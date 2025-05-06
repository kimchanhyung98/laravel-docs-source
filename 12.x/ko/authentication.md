# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트(Starter Kits)](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 제한(Throttling)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [Stateless HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기에서 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 재확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 유저 프로바이더 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/{{version}}/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하여 "로그인"할 수 있는 방법을 제공합니다. 이 기능을 웹 애플리케이션에 구현하는 것은 복잡하고 잠재적으로 위험한 일이 될 수 있습니다. 이러한 이유로 Laravel은 신속하고 안전하며 쉽게 인증 기능을 구현할 수 있도록 도구를 제공합니다.

Laravel의 인증 기능은 기본적으로 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자가 어떻게 인증되는지 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용하여 상태를 유지하는 `session` 가드를 기본 제공합니다.

프로바이더는 사용자를 영구 저장소(예: 데이터베이스)에서 가져오는 방법을 정의합니다. Laravel은 [Eloquent](/docs/{{version}}/eloquent)와 데이터베이스 쿼리 빌더를 이용한 사용자 조회를 지원합니다. 필요에 따라 애플리케이션에 맞는 추가적인 프로바이더를 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일은 Laravel 인증 서비스의 동작을 조정할 수 있도록 여러가지 잘 설명된 옵션을 포함합니다.

> [!NOTE]
> 가드와 프로바이더는 "권한(roles)" 및 "퍼미션(permissions)"과 혼동해서는 안 됩니다. 퍼미션을 통한 사용자 동작 권한 부여(authorization)에 대해 더 알고 싶다면 [권한 부여(authorization)](/docs/{{version}}/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트(Starter Kits)

빠르게 시작하고 싶으신가요? [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 신규 Laravel 프로젝트에 설치해 보세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에 지정된 URL로 접속하면, 스타터 키트가 전체 인증 시스템의 스캐폴딩을 자동으로 구축해줍니다!

**최종 Laravel 애플리케이션에서 스타터 키트를 꼭 사용하지 않아도, [스타터 키트](/docs/{{version}}/starter-kits)를 설치하면 실제 Laravel 프로젝트에서 인증 기능이 어떻게 구현되는지 학습하는 데 큰 도움이 됩니다.** 스타터 키트는 인증 컨트롤러, 라우트, 뷰를 모두 포함하므로, 해당 파일의 코드를 직접 살펴보며 Laravel에서 인증 기능을 구현하는 방식을 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/{{version}}/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 활용할 수 있습니다. MongoDB를 사용하는 경우에는 MongoDB 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 만들 때, 비밀번호 컬럼의 길이는 최소 60자 이상이어야 합니다. 기본적으로 제공되는 `users` 테이블 마이그레이션에는 이미 이보다 긴 컬럼이 생성됩니다.

또한, `users`(또는 동등한) 테이블에는 100자 길이의 nullable string 타입 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 사용자가 "로그인 상태 유지(remember me)" 옵션을 선택할 때 토큰을 저장하는 데 사용됩니다. 역시, Laravel의 기본 `users` 테이블 마이그레이션에는 이미 해당 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기 전에, Laravel의 인증 에코시스템 전반과 각 패키지의 목적을 간단히 살펴보겠습니다.

인증이 어떻게 동작하는지 생각해봅시다. 웹 브라우저를 사용할 때 사용자는 로그인 폼을 통해 사용자명과 비밀번호를 입력합니다. 이 자격 정보가 올바르면, 애플리케이션은 인증된 사용자에 대한 정보를 [세션](/docs/{{version}}/session)에 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 담겨 있어 이후의 요청들도 해당 사용자의 세션과 연결할 수 있습니다. 세션 쿠키가 수신되면, 애플리케이션은 세션 ID를 기반으로 세션 데이터를 조회하고, 인증 정보가 세션에 저장되어 있음을 확인하여 해당 사용자를 "인증됨(authenticated)"으로 간주합니다.

원격 서비스가 API에 접근하기 위해 인증해야 하는 경우, 웹 브라우저가 없으므로 대개 쿠키를 사용하지 않습니다. 대신, 원격 서비스는 각 요청마다 API 토큰을 함께 보냅니다. 애플리케이션은 이 토큰이 유효한지 확인한 후, 관련 사용자를 "인증"된 것으로 간주합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel에는 `Auth` 및 `Session` 파사드를 통해 주로 접근하는 내장 인증 및 세션 서비스가 있습니다. 이 기능들은 웹 브라우저에서 시작하는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자 자격 증명을 검증하고 인증하는 메서드를 제공하며, 적절한 인증 정보가 사용자의 세션에 자동으로 저장되고 세션 쿠키가 발급됩니다. 이 문서에서는 이러한 서비스의 사용 방법을 다룹니다.

**애플리케이션 스타터 키트**

위 문서에서 설명했듯, 인증 서비스를 수동으로 사용하여 애플리케이션만의 인증 계층을 직접 구축할 수도 있습니다. 그러나 좀 더 신속하게 시작할 수 있도록, 강력하고 현대적인 [무료 스타터 키트](/docs/{{version}}/starter-kits)를 제공합니다. 이 키트는 인증 계층의 스캐폴딩을 손쉽게 제공합니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리와 API 요청 인증을 위한 두 가지 선택 패키지 [Passport](/docs/{{version}}/passport)와 [Sanctum](/docs/{{version}}/sanctum)를 제공합니다. 이 라이브러리들과 내장 쿠키 기반 인증 라이브러리는 상호 배타적인 것이 아닙니다. 이 라이브러리들은 주로 API 토큰 인증에 중점을 두며, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 중점을 둡니다. 많은 애플리케이션이 내장 쿠키 기반 인증 서비스와 하나의 API 인증 패키지를 함께 사용할 수 있습니다.

**Passport**

Passport는 다양한 OAuth2 "grant type"을 제공하는 OAuth2 인증 프로바이더로, 다양한 유형의 토큰을 발급할 수 있습니다. API 인증에 적합한 강력하고 복잡한 패키지이지만, 일반적으로 대부분의 애플리케이션은 OAuth2 스펙에서 제공하는 복잡한 기능이 필요하지 않으며, 이는 사용자와 개발자 모두에게 혼란스러울 수 있습니다. 더불어, SPA나 모바일 앱에서 OAuth2 인증 프로바이더(Passport 등)를 사용하는 방법에 대해 혼란을 겪기도 합니다.

**Sanctum**

OAuth2의 복잡성과 개발자의 혼란에 대응하여, 좀 더 간단하고 streamline된 인증 패키지를 만들고자 하였습니다. [Laravel Sanctum](/docs/{{version}}/sanctum)은 웹 브라우저의 첫파티 요청과 API 토큰을 모두 처리할 수 있습니다. 첫파티 웹 UI와 API를 제공하거나, 백엔드와 분리된 SPA(Single Page Application), 또는 모바일 클라이언트를 제공하는 애플리케이션에는 Sanctum이 권장되는 인증 패키지입니다.

Sanctum은 하이브리드 웹/API 인증 패키지로 애플리케이션 전체 인증 프로세스를 관리할 수 있습니다. 요청이 들어오면, 세션 쿠키를 통한 인증인지 API 토큰을 통한 인증인지 판단하여 처리합니다. 자세한 원리에 대해서는 Sanctum의 ["작동 원리"](/docs/{{version}}/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

정리하면, 브라우저를 통한 접근이 필요한 모놀리식 Laravel 애플리케이션을 구축할 경우 Laravel 내장 인증 서비스를 사용하세요.

API가 외부에 제공된다면 [Passport](/docs/{{version}}/passport)나 [Sanctum](/docs/{{version}}/sanctum) 중 하나를 선택해 API 토큰 인증을 제공하면 됩니다. 일반적으로 Sanctum이 간단하고 완전한 솔루션이므로 권장되며, 스코프/권한 기능도 지원합니다.

Laravel 백엔드 기반의 SPA를 구축한다면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하세요. 이 경우, [백엔드 인증 라우트를 직접 구현](#authenticating-users)하거나 [Laravel Fortify](/docs/{{version}}/fortify)를 인증 백엔드로 사용해 회원가입, 비밀번호 재설정, 이메일 인증 등의 기능을 구현할 수 있습니다.

OAuth2의 모든 기능이 반드시 필요한 경우에만 Passport를 선택하세요.

빠르게 시작하고 싶다면, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 추천합니다. 이 키트는 이미 선호되는 인증 스택을 활용하여 프로젝트를 신속하게 시작할 수 있게 합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작

> [!WARNING]
> 이 문서는 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 통한 사용자 인증에 대해 소개합니다. UI 스캐폴딩이 포함되어 있어 빠르게 시작할 수 있습니다. Laravel의 인증 시스템과 직접 통합하고 싶다면, [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치해야 합니다. 이 스타터 키트는 새로운 Laravel 프로젝트에 인증 기능을 빼어난 UI와 함께 손쉽게 도입할 수 있게 해줍니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 키트로 애플리케이션을 생성하고 사용자가 회원가입 및 인증할 수 있도록 한 후, 현재 인증된 사용자와 상호작용하는 것이 자주 필요합니다. 요청을 처리하는 과정에서, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회...
$user = Auth::user();

// 현재 인증된 사용자의 ID 조회...
$id = Auth::id();
```

또는, 사용자가 인증된 후에는 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 접근할 수도 있습니다. 타입힌트된 클래스들은 컨트롤러 메서드에 자동 주입됩니다. 컨트롤러에서 `Illuminate\Http\Request`를 타입힌트로 선언하면, `user` 메서드를 통해 어느 컨트롤러 메서드에서도 편하게 인증된 사용자 정보를 얻을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보 업데이트
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

들어오는 HTTP 요청을 한 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증된 경우 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인된 상태...
}
```

> [!NOTE]
> `check` 메서드로 사용자가 인증되었는지 확인할 수 있지만, 보통은 미들웨어를 이용해 사용자가 인증되었는지 검사한 뒤에 특정 라우트/컨트롤러에 접근시키는 것이 일반적입니다. 자세한 내용은 [라우트 보호](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 이용해 인증된 사용자만 특정 라우트에 접근하도록 할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 위한 `auth` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)을 기본 제공합니다. 별도 등록 없이, 라우트 정의에 해당 미들웨어를 추가하면 됩니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 미인증 사용자 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 사용자를 `login` [이름 지정 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드를 이용해 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // 클로저 사용 예시...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리디렉션

`guest` 미들웨어는 인증된 사용자가 접속할 경우, `dashboard`나 `home` 이름의 라우트로 리디렉션합니다. 이 동작도 `bootstrap/app.php` 파일에서 `redirectUsersTo` 메서드를 통해 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectUsersTo('/panel');

    // 클로저 사용 예시...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정

`auth` 미들웨어를 라우트에 적용할 때, 특정 "가드"를 지정하여 사용자를 인증할 수 있습니다. 지정하는 가드 이름은 `auth.php` 설정 파일의 `guards` 배열의 키 값이어야 합니다:

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한(Throttling)

[애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우, 로그인 시도에 자동으로 속도 제한이 적용됩니다. 기본적으로, 사용자가 여러 번 잘못된 자격 정보를 입력하면 1분 동안 로그인이 차단됩니다. 제한은 사용자의 사용자명/이메일 및 IP별로 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에 대해 속도 제한을 적용하려면, [속도 제한 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증

Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)에서 제공하는 인증 스캐폴딩을 반드시 사용할 필요는 없습니다. 이를 사용하지 않는 경우, Laravel의 인증 클래스를 직접 이용해 사용자 인증을 제어해야 합니다. 걱정 마세요, 매우 쉽습니다!

`Auth` [파사드](/docs/{{version}}/facades)를 이용해 인증 서비스를 사용할 것이므로, 클래스 상단에서 `Auth` 파사드를 임포트해야 합니다. 이제 `attempt` 메서드를 살펴봅시다. 이 메서드는 주로 애플리케이션의 "로그인" 폼에서 인증 시도 처리를 위해 사용됩니다. 인증이 성공하면, [세션](/docs/{{version}}/session) 고정화(session fixation) 공격을 막기 위해 사용자의 세션을 재생성해야 합니다:

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
            'email' => '제공된 자격 정보가 일치하지 않습니다.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 첫 번째 인자로 key/value 쌍의 배열을 받으며, 이 값들은 데이터베이스에서 사용자를 찾는 데 사용됩니다. 위 예시에서는 `email` 컬럼 값으로 사용자를 조회합니다. 사용자가 조회된 경우, 데이터베이스에 저장된 해시된 비밀번호와 메서드에 전달된 `password` 값을 비교합니다. 프레임워크가 자동으로 비교하므로, 요청에서 받은 `password`를 직접 해싱할 필요는 없습니다. 두 해시 값이 일치하면 인증된 세션이 시작됩니다.

Laravel의 인증 서비스는 인증 가드의 프로바이더 설정에 따라 사용자를 조회합니다. 기본적으로, `config/auth.php`에서는 Eloquent 사용자 프로바이더를 지정하며, 사용자를 조회할 때 `App\Models\User` 모델을 사용합니다. 필요한 경우 설정 파일에서 이 값을 변경할 수 있습니다.

`attempt` 메서드는 인증이 성공하면 `true`, 실패하면 `false`를 반환합니다.

‘intended’ 메서드는 인증 미들웨어에 의해 차단되기 전 사용자가 접속하려던 URL로 리다이렉트합니다. 목표 URI가 없을 경우 대체 URI를 전달할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

원한다면, 이메일과 비밀번호 외에 추가적인 조회 조건을 인증 쿼리에 포함할 수 있습니다. `attempt` 메서드에 전달하는 배열에 쿼리 조건을 더하면 됩니다. 예를 들어, 사용자가 "active" 상태인지 확인할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증 성공...
}
```

보다 복잡한 조건이 필요한 경우, 크레덴셜 배열에 클로저를 포함할 수도 있습니다. 이 클로저는 쿼리 인스턴스로 호출되어 필요에 따라 쿼리를 커스터마이즈할 수 있습니다:

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
> 이 예들에서 `email`은 필수 옵션이 아니며, 단순 예시입니다. 데이터베이스의 "사용자명" 역할을 하는 컬럼 이름으로 사용하세요.

`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아, 인증 전 후보 사용자를 더 광범위하게 검토할 때 사용할 수 있습니다. 이 클로저는 사용자를 인자로 받아, 인증이 가능한 경우 `true`, 아니면 `false`를 반환해야 합니다:

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
#### 특정 가드 인스턴스 접근

`Auth` 파사드의 `guard` 메서드를 통해, 인증 시 사용할 가드 인스턴스를 지정할 수 있습니다. 이를 통해 애플리케이션의 서로 다른 파트에서 서로 다른 유저 테이블/모델을 이용해 인증을 관리할 수 있습니다.

전달하는 가드 이름은 `auth.php` 설정 파일에 등록된 guard여야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션은 로그인 폼에 "로그인 상태 유지" 체크박스를 제공합니다. 이 기능을 구현하려면 `attempt` 메서드의 두 번째 인자로 boolean 값을 전달하세요.

이 값이 `true`이면, Laravel은 사용자가 직접 로그아웃할 때까지 인증 상태를 유지합니다. 이 기능을 사용하려면, `users` 테이블에 "remember_token" 컬럼이 반드시 존재해야 합니다. 신규 Laravel 프로젝트에는 이미 포함돼 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 "기억됨"...
}
```

"로그인 상태 유지" 기능이 있을 경우, `viaRemember` 메서드를 통해 현재 인증 사용자가 이 기능으로 인증되었는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증

기존의 사용자 인스턴스를 현재 인증 사용자로 설정하려면 `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 전달하면 됩니다. 전달할 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/{{version}}/contracts)을 구현해야 하며, Laravel의 `App\Models\User`는 이미 해당 인터페이스를 구현하고 있습니다. 이 방식은 주로, 사용자가 회원가입한 직후와 같이 이미 유효한 사용자 인스턴스가 있는 경우에 적합합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

두 번째 인자로 boolean 값을 전달해 "로그인 상태 유지" 기능 여부를 지정할 수 있습니다:

```php
Auth::login($user, $remember = true);
```

필요할 경우, `login` 호출 전에 인증 가드를 지정할 수 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자 ID로 인증

데이터베이스 레코드의 기본키(Primary key)를 통해 사용자를 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다:

```php
Auth::loginUsingId(1);
```

`loginUsingId` 메서드의 `remember` 인자에 boolean 값을 전달하여 "로그인 상태 유지" 여부를 지정할 수 있습니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 1회성 사용자 인증

애플리케이션에 대해 한 요청만 사용자를 인증할 때는, `once` 메서드를 사용할 수 있습니다. 이때 세션이나 쿠키는 사용되지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 없이 빠르게 사용자 인증을 구현할 수 있는 방식입니다. 라우트에 `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 붙이는 것만으로 시작할 수 있습니다. 이 미들웨어는 프레임워크에 내장돼 있으므로 따로 정의할 필요가 없습니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth.basic');
```

해당 미들웨어를 라우트에 추가하면, 브라우저로 접근 시 자동으로 자격 증명을 입력하라는 프롬프트가 표시됩니다. 기본적으로, `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자의 "username"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 주의사항

PHP FastCGI와 Apache로 Laravel을 서비스한다면, HTTP Basic 인증이 제대로 동작하지 않을 수 있습니다. 이 문제를 해결하려면 애플리케이션의 `.htaccess` 파일에 다음 줄을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### Stateless HTTP Basic 인증

세션에 사용자 식별자 쿠키를 저장하지 않고도 HTTP Basic 인증을 사용할 수 있습니다. 이는 주로 API 요청을 HTTP 인증으로 처리할 때 유용합니다. 이를 위해 [미들웨어](/docs/{{version}}/middleware)를 정의하여 `onceBasic` 메서드를 호출하세요. 이 메서드가 응답을 반환하지 않으면 요청이 다음 레이어로 전달됩니다:

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

그리고 해당 미들웨어를 라우트에 적용하세요:

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃

사용자를 수동으로 로그아웃하려면, `Auth` 파사드에서 제공하는 `logout` 메서드를 사용하면 됩니다. 이 메서드는 사용자의 세션에서 인증 정보를 제거하여 이후의 요청에서 인증이 유지되지 않도록 합니다.

또한, `logout` 호출 외에도 사용자의 세션 무효화 및 [CSRF 토큰](/docs/{{version}}/csrf) 재생성을 권장합니다. 일반적으로 사용자를 애플리케이션의 루트로 리디렉션합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 애플리케이션에서 사용자 로그아웃
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

Laravel은 사용자가 현재 기기 외 다른 기기에서 활성화된 세션을 무효화하고 "로그아웃" 시키는 기능도 제공합니다. 이 기능은 주로 사용자가 비밀번호를 변경/업데이트할 때, 현재 기기 인증 상태는 유지하면서 다른 기기 세션을 만료시키는 데 활용됩니다.

먼저, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 필요로 하는 라우트에 포함되어 있는지 확인해야 합니다. 보통, 해당 미들웨어를 라우트 그룹에 적용하면 애플리케이션 대부분의 라우트에서 사용할 수 있습니다. 기본적으로 `auth.session` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)으로 사용할 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그런 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 현재 비밀번호를 입력하여 확인하도록 요구합니다(폼을 통해 받아와야 함):

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 메서드가 호출되면, 사용자의 다른 기기 세션이 완전히 무효화되어, 이전에 인증된 모든 가드에서 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 재확인(Password Confirmation)

애플리케이션을 개발하다 보면 사용자가 민감한 작업을 수행하거나 보호된 영역으로 이동하기 전에 비밀번호를 재확인해야 하는 경우가 있습니다. Laravel은 이 과정을 간단하게 만들어주는 내장 미들웨어를 제공합니다. 이 기능을 구현하려면, 사용자의 비밀번호 확인을 요청하는 뷰를 표시할 라우트와 비밀번호를 확인한 후 사용자를 의도한 경로로 리디렉션하는 라우트 두 개를 정의해야 합니다.

> [!NOTE]
> 아래 문서는 Laravel의 비밀번호 확인 기능을 직접 통합하는 법을 설명합니다. 보다 빠르게 시작하고 싶다면, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)에도 이 기능이 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호 재확인이 성공하면, 사용자는 3시간 동안 다시 비밀번호를 재입력하지 않아도 됩니다. 이 시간을 변경하려면, `config/auth.php`의 `password_timeout` 설정 값을 수정하면 됩니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자의 비밀번호 확인을 요청하는 뷰를 표시하는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트가 반환하는 뷰에는 반드시 `password` 입력 필드가 들어가야 하며, 사용자가 보호된 영역에 접근하니 비밀번호를 다시 입력하라고 안내하는 메시지를 추가할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인

다음으로, 폼에서 제출된 비밀번호를 검증하고 사용자를 의도한 경로로 리디렉션하는 라우트를 정의합니다:

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

이 라우트에서는 먼저 요청의 `password` 값이 현재 인증된 사용자의 비밀번호와 일치하는지 확인합니다. 유효하다면, Laravel 세션에 사용자가 비밀번호를 확인했다고 알립니다. `passwordConfirmed` 메서드는 시간 정보를 세션에 저장하며, 이를 통해 Laravel은 사용자가 마지막으로 비밀번호를 확인한 시점을 추적합니다. 마지막으로, 사용자를 원래 목적지로 리디렉션합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

비밀번호 재확인을 요구하는 작업을 수행하는 라우트에는 반드시 `password.confirm` 미들웨어를 추가해야 합니다. Laravel 설치 시 기본 제공되는 미들웨어로, 사용자의 의도 경로를 세션에 저장해 비밀번호 확인 후 해당 위치로 리디렉션시켜 줍니다. 이후, 미들웨어는 사용자를 `password.confirm` [이름 지정 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션합니다:

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

`Auth` 파사드의 `extend` 메서드를 이용해 나만의 인증 가드를 정의할 수 있습니다. [서비스 프로바이더](/docs/{{version}}/providers)에서 이 메서드를 호출하는 것이 가장 안전합니다. Laravel은 이미 `AppServiceProvider`를 제공하므로 해당 프로바이더에 코드를 추가하면 됩니다:

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
     * 부트스트랩 애플리케이션 서비스
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Illuminate\Contracts\Auth\Guard 인스턴스 반환...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 코드에서처럼, `extend` 메서드에 전달되는 콜백은 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 이 인터페이스의 메서드를 구현해 커스텀 가드를 정의할 수 있습니다. 커스텀 가드 정의 후에는 `auth.php`의 `guards` 설정에서 해당 가드를 참조할 수 있습니다:

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

HTTP 요청 기반 인증 시스템을 가장 간단하게 구현하는 방법은 `Auth::viaRequest` 메서드를 활용하는 것입니다. 이 메서드는 단일 클로저로 간단하게 인증 절차를 정의할 수 있게 해줍니다.

우선, 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 `Auth::viaRequest`를 호출하세요. 첫 인자는 인증 드라이버명(임의의 문자열), 두 번째는 요청을 받아 사용자 인스턴스(또는 실패시 `null`)를 반환하는 클로저입니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * 부트스트랩 애플리케이션 서비스
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

커스텀 인증 드라이버를 정의했다면, 이제 `auth.php`의 `guards` 설정에서 해당 드라이버를 사용할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 해당 가드를 라우트에 인증 미들웨어로 적용하면 됩니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 유저 프로바이더 추가

전통적인 관계형 데이터베이스가 아닌 다른 시스템에 사용자를 저장하는 경우, Laravel을 확장하여 커스텀 인증 유저 프로바이더를 만들어야 합니다. `Auth` 파사드의 `provider` 메서드를 사용해서 정의할 수 있으며, `Illuminate\Contracts\Auth\UserProvider` 구현체를 반환해야 합니다:

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
     * 부트스트랩 애플리케이션 서비스
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Illuminate\Contracts\Auth\UserProvider 인스턴스 반환...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider`를 등록한 후, `auth.php`의 `providers` 항목에서 이 드라이버를 사용할 수 있습니다:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그리고 이 프로바이더를 `guards` 설정에서 참조하세요:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등과 같은 영구 저장소 시스템에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스 덕분에, 사용자 데이터의 저장 방식이나 클래스에 관계없이 Laravel 인증 메커니즘이 정상적으로 동작합니다.

`Illuminate\Contracts\Auth\UserProvider` 인터페이스는 다음과 같습니다:

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

- `retrieveById`: MySQL의 AUTO_INCREMENT 키와 같이 사용자를 식별하는 값을 받아 해당 `Authenticatable` 인스턴스를 반환합니다.
- `retrieveByToken`: 사용자 고유 `$identifier`와 "로그인 유지" `$token`(예: `remember_token` 컬럼)을 받아 해당하는 사용자를 반환합니다.
- `updateRememberToken`: 성공적인 "로그인 유지" 또는 로그아웃 시 `$user`의 `remember_token`을 `$token`으로 갱신합니다.
- `retrieveByCredentials`: `Auth::attempt` 메서드에서 전달된 자격정보 배열을 받아, 일치하는 사용자를 조회합니다. 단, 비밀번호 검증/인증은 수행하지 않습니다.
- `validateCredentials`: `$user`와 `$credentials`를 비교해 사용자를 인증합니다(예시: `Hash::check`로 `$user->getAuthPassword()`와 `$credentials['password']` 비교). 유효하면 `true`, 아니면 `false`를 반환합니다.
- `rehashPasswordIfRequired`: 필요시(및 지원되는 경우) `$user`의 비밀번호를 재해싱합니다. (예: `Hash::needsRehash`로 필요 여부 확인 후, `Hash::make`로 재해싱)

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

UserProvider 메서드를 살펴봤으니, 이제 `Authenticatable` 계약을 봅시다. `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드는 모두 이 인터페이스 구현체를 반환해야 합니다:

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

이 인터페이스는 심플합니다. 
- `getAuthIdentifierName`: 사용자 "기본키" 컬럼명 반환
- `getAuthIdentifier`: 사용자 "기본키" 값 반환
- `getAuthPasswordName`: 비밀번호 컬럼명 반환
- `getAuthPassword`: 해시된 비밀번호 반환

이 인터페이스 덕분에, ORM/스토리지 방식에 상관없이 다양한 "유저" 클래스를 인증 시스템에서 처리할 수 있습니다. Laravel에는 `app/Models` 폴더에 이미 이 인터페이스를 구현한 `App\Models\User` 클래스가 포함되어 있습니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt의 "work factor"는 애플리케이션의 `config/hashing.php`나 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

CPU/GPU 성능이 증가할수록 work factor를 점점 늘리는 것이 좋습니다. work factor를 높이면, Laravel은 인증(스타터 키트 또는 [`attempt` 메서드](#authenticating-users)로 수동 인증 시) 시점에 사용자의 비밀번호를 자동으로 재해싱해줍니다.

자동 비밀번호 재해싱은 보통 애플리케이션에 문제를 일으키지 않지만, 이 동작을 비활성화하려면 `hashing` 설정 파일을 퍼블리시한 후:

```shell
php artisan config:publish hashing
```

`rehash_on_login` 값을 `false`로 설정하세요:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트

Laravel은 인증 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 다음 이벤트에 대해 [리스너](/docs/{{version}}/events)를 정의할 수 있습니다:

<div class="overflow-auto">

| 이벤트 명 |
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
