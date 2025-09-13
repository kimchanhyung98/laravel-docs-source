# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [경로 보호](#protecting-routes)
    - [로그인 제한](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방식](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [무상태 HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 디바이스의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [경로 보호](#password-confirmation-protecting-routes)
- [사용자 지정 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [사용자 지정 사용자 제공자 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 이러한 기능을 웹 애플리케이션에 직접 구현하는 것은 복잡하고 위험할 수 있습니다. 그래서 Laravel은 인증을 빠르고, 안전하게, 그리고 쉽게 구현할 수 있는 도구를 제공합니다.

Laravel의 인증 시스템은 기본적으로 "가드(guard)"와 "제공자(provider)"로 구성되어 있습니다. 가드는 요청마다 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel은 세션 저장소와 쿠키를 사용하여 상태를 유지하는 `session` 가드를 기본으로 제공합니다.

제공자는 애플리케이션의 영구 저장소에서 사용자를 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 통한 사용자 조회를 기본으로 지원합니다. 물론, 필요에 따라 추가적인 제공자를 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치해 있습니다. 이 파일에는 Laravel 인증 서비스의 동작을 세부적으로 조정할 수 있는 다양한 옵션이 잘 문서화되어 있습니다.

> [!NOTE]
> 가드와 제공자는 "역할(roles)" 및 "권한(permissions)" 개념과 혼동해서는 안 됩니다. 권한을 이용한 사용자 동작 인가(authorize)에 대해 더 알고 싶다면 [인가(authorization)](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트 (Starter Kits)

빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에서 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 이후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 URL로 접속하면, 스타터 키트가 전체 인증 시스템의 골격을 자동으로 구성해줍니다!

**최종적으로 스타터 키트를 사용하지 않더라도, [스타터 키트](/docs/12.x/starter-kits)를 설치하는 것은 Laravel의 인증 기능이 실제 Laravel 프로젝트에서 어떻게 구현되는지 배우는 좋은 기회입니다.** 스타터 키트에는 인증 컨트롤러, 라우트, 뷰가 포함되어 있으므로, 이러한 파일 내 코드를 살펴봄으로써 인증 기능의 실제적인 구현 방식을 학습할 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

기본적으로, Laravel은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있도록 제공됩니다.

만약 애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 이용하는 `database` 인증 제공자를 사용할 수 있습니다. MongoDB를 사용하는 경우에는, MongoDB의 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참조하세요.

`App\Models\User` 모델을 위한 데이터베이스 스키마를 작성할 때, 비밀번호 컬럼이 최소 60자 이상이 되도록 하세요. 기본적으로 새 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이 길이를 초과하는 컬럼을 생성합니다.

또한, `users`(또는 이에 준하는) 테이블에는 널 허용 및 100자 길이의 문자열 타입 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 사용자가 로그인 시 "기억하기(remember me)" 옵션을 선택할 때 토큰을 저장하는 데 사용됩니다. 역시, 기본 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속 읽기 전에, Laravel의 전반적인 인증 에코시스템을 간단히 살펴보고 각 패키지의 목적을 안내하겠습니다.

먼저, 인증이 어떻게 동작하는지 생각해 봅시다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼에서 사용자명과 비밀번호를 입력합니다. 이 인증 정보가 올바르면, 애플리케이션은 인증된 사용자 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저로 전달된 쿠키에는 세션 ID가 담겨, 이후의 요청은 해당 사용자를 올바른 세션과 연결할 수 있습니다. 세션 쿠키가 전달되면, 애플리케이션은 세션 ID로 세션 데이터를 읽고 인증 정보를 기반으로 해당 사용자를 "인증된" 상태로 간주합니다.

원격 서비스가 API에 접근하기 위해 인증이 필요한 경우에는, 웹 브라우저가 없으므로 대개 쿠키를 사용하지 않습니다. 대신 원격 서비스는 각 요청마다 API 토큰을 전달합니다. 애플리케이션은 전달받은 토큰을 유효한 API 토큰 테이블에서 검증하고, 해당 토큰에 연결된 사용자로 요청을 "인증"합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel은 기본적으로 인증 및 세션 서비스를 제공하며, 보통 `Auth` 및 `Session` 파사드로 접근합니다. 이들은 웹 브라우저에서 발생한 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명 확인, 인증 처리 등을 위한 메서드를 제공하며, 인증 데이터 저장 및 세션 쿠키 발급 또한 자동으로 처리합니다. 이러한 기능 사용 방법은 이 문서의 뒷부분에서 다룹니다.

**애플리케이션 스타터 키트**

이 문서에서 설명한 것처럼, 인증 서비스를 직접 다루어 애플리케이션 고유의 인증 레이어를 만들 수도 있습니다. 하지만 더 빠르게 시작하고 싶다면, [무료 스타터 키트](/docs/12.x/starter-kits)를 활용해 인증 레이어 전체를 현대적이고 견고하게 구성할 수 있습니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리를 돕고, API 토큰으로 인증된 요청을 처리할 수 있게 두 개의 선택적 패키지 [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 라이브러리들과 내장 쿠키 기반 인증 서비스는 서로 대체재가 아니라, 각각의 목적이 다릅니다. API 인증(토큰 기반)에 집중하는 것이 주요 목적이며, 브라우저 인증은 내장 서비스의 역할입니다. 많은 애플리케이션이 이 둘을 함께 사용하기도 합니다.

**Passport**

Passport는 OAuth2 인증 제공자로, 다양한 OAuth2 "그랜트 유형"을 통해 여러 종류의 토큰 발급이 가능합니다. 전반적으로 매우 강력하면서도 복잡한 API 인증 패키지로, 대부분의 애플리케이션은 OAuth2 스펙의 모든 기능이 필요하지 않을 수 있습니다. 또한 OAuth2를 이용한 SPA나 모바일 애플리케이션 인증 방법에 대해 혼란을 겪는 개발자도 많았습니다.

**Sanctum**

OAuth2의 복잡성과 개발자의 혼란을 해결하기 위해, Laravel은 보다 간단하면서 웹 요청과 API 토큰 인증 모두를 처리할 수 있는 패키지 [Laravel Sanctum](/docs/12.x/sanctum)을 개발했습니다. Sanctum은 자체적으로 웹 UI뿐 아니라 별도의 백엔드가 존재하는 SPA(싱글 페이지 애플리케이션) 또는 모바일 클라이언트까지 포괄하는 인증 방식으로, 대부분의 경우 권장됩니다.

Laravel Sanctum은 웹/ API 인증을 아우르는 하이브리드 인증 패키지입니다. 요청이 들어오면, 먼저 세션 쿠키를 통해 인증된 세션이 있는지 확인하고, 해당 쿠키가 없다면 API 토큰이 첨부되었는지를 검사합니다. 자세한 동작 방식은 Sanctum의 ["작동 원리"](https://laravel.com/docs/12.x/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

정리하자면, 애플리케이션이 브라우저로 접근되고 모놀리식 Laravel 애플리케이션 구조를 사용한다면 내장 인증 서비스를 사용하면 됩니다.

API를 외부에 제공한다면, [Passport](/docs/12.x/passport) 또는 [Sanctum](/docs/12.x/sanctum) 중 하나를 선택해 API 토큰 인증을 구현해야 합니다. 일반적으로 Sanctum이 더 단순하고 완벽한 솔루션이며, API/SPA/모바일 인증에 권장됩니다. "스코프(scope)" 또는 "ability" 같은 고급 기능도 지원합니다.

만약 SPA가 백엔드는 Laravel, 프론트엔드는 별도라면 반드시 [Laravel Sanctum](/docs/12.x/sanctum)을 사용해야 합니다. 이 경우 인증 경로를 [직접 구현](#authenticating-users)하거나, [Laravel Fortify](/docs/12.x/fortify)를 인증용 백엔드로 활용할 수 있습니다.

OAuth2의 모든 상세 기능이 꼭 필요하다면 Passport를 선택하면 됩니다.

빠르게 시작하고 싶다면, [공식 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 이용해 당장 인증이 적용된 새 Laravel 애플리케이션을 만들어보세요.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 부분에서는 UI 스캐폴딩을 포함한 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 통한 인증 방법을 다룹니다. 인증 시스템을 직접 연동하고 싶다면 [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 스타터 키트는 인증을 손쉽게 통합할 수 있도록 아름답게 디자인된 시작점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회

스타터 키트로 애플리케이션을 만들고, 사용자가 가입/로그인할 수 있게 된 이후에는 현재 로그인한 사용자와 상호작용해야 할 때가 많습니다. 들어오는 요청에서, `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자를 가져올 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

// 현재 인증된 사용자 조회
$user = Auth::user();

// 인증된 사용자의 ID 조회
$id = Auth::id();
```

또는, 사용자가 인증된 후에는 `Illuminate\Http\Request` 인스턴스를 통해서도 인증 사용자를 가져올 수 있습니다. 컨트롤러 메서드에 `Illuminate\Http\Request` 객체를 타입힌트로 선언하면, 어디서든 편리하게 요청의 `user` 메서드로 인증 사용자를 액세스할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 기존 항공편 정보 업데이트.
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
#### 현재 사용자의 인증 여부 확인

HTTP 요청을 보낸 사용자가 인증되어 있는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하세요. 이 메서드는 사용자가 인증되어 있으면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // 사용자가 로그인한 상태...
}
```

> [!NOTE]
> 인증 여부를 `check`로 확인할 수도 있지만, 보통은 미들웨어를 통해 사용자가 특정 경로나 컨트롤러에 접근하기 전에 인증 상태를 확인하도록 처리합니다. 자세한 내용은 [경로 보호](/docs/12.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 경로 보호

[라우트 미들웨어](/docs/12.x/middleware)를 활용해 인증된 사용자만 특정 경로에 접근하도록 제한할 수 있습니다. Laravel에는 `Illuminate\Auth\Middleware\Authenticate` 클래스를 위한 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)인 `auth` 미들웨어가 있습니다. 이 미들웨어는 Laravel 내부에 이미 등록되어 있으므로, 경로 정의에 바로 추가하면 됩니다.

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 미인증 사용자 리디렉션

`auth` 미들웨어는 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [네임드 라우트](/docs/12.x/routing#named-routes)로 자동 리디렉션합니다. 만약 이 동작을 변경하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드로 수정할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // 클로저를 사용할 수도 있습니다...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증 사용자 리디렉션

`guest` 미들웨어는 인증된 사용자가 감지되면, 해당 사용자를 `dashboard` 또는 `home` 네임드 라우트로 리디렉션합니다. 이 역시 `bootstrap/app.php` 파일에서 `redirectUsersTo` 메서드로 동작을 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // 클로저를 사용할 수도 있습니다...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정

`auth` 미들웨어를 경로에 추가할 때, 어떤 "가드"로 인증할지 지정할 수 있습니다. 지정한 가드는 `auth.php` 설정 파일의 `guards` 배열 키 값과 일치해야 합니다.

```php
Route::get('/flights', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한(Login Throttling)

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용한다면, 로그인 시도에 대한 비율 제한이 자동으로 적용됩니다. 사용자가 여러 번 올바르지 않은 인증 정보를 입력하면, 1분간 로그인 시도가 차단됩니다. 제한은 사용자의 사용자명/이메일, 그리고 IP 주소를 기준으로 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 경로에 비율 제한을 적용하고 싶다면, [비율 제한 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)에서 제공하는 인증 스케폴딩을 필수로 사용해야 하는 것은 아닙니다. 이 스케폴딩 없이 직접 인증 로직을 구현하려면, Laravel의 인증 클래스를 직접 활용해야 합니다. 걱정하지 마세요, 어렵지 않습니다!

`Auth` [파사드](/docs/12.x/facades)를 통해 인증 서비스를 사용할 수 있으므로, 클래스 상단에 `Auth` 파사드를 반드시 임포트하세요. 이제, 보통 로그인 폼에서 인증을 처리할 때 사용하는 `attempt` 메서드를 살펴보겠습니다. 인증에 성공하면 [세션](/docs/12.x/session)을 재생성하여 [세션 고정 공격](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%85%98_%EA%B3%A0%EC%A0%95) 방지 효과도 얻을 수 있습니다.

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

`attempt` 메서드는 첫 번째 인수로 키/값 쌍의 배열을 받습니다. 이 배열 값은 데이터베이스에서 사용자를 조회하는 데 쓰입니다. 예시에서는 `email` 컬럼을 기반으로 사용자를 찾게 됩니다. 사용자가 발견되면, 데이터베이스의 해시된 비밀번호와 입력받은 비밀번호가 비교됩니다. 프레임워크가 자동으로 입력된 비밀번호를 해시해 비교하므로, 비밀번호 값은 해시하지 마세요. 비밀번호가 일치하면 인증 세션이 시작됩니다.

Laravel 인증 서비스는 "가드"의 "제공자" 설정에 따라 사용자를 데이터베이스에서 불러옵니다. 기본 `config/auth.php` 파일에서는 Eloquent 사용자 제공자가 지정되어 있으며, 사용자를 조회할 때 `App\Models\User` 모델을 사용합니다. 필요에 따라 설정을 변경할 수도 있습니다.

`attempt` 메서드는 인증이 성공하면 `true`, 실패하면 `false`를 반환합니다.

`intended` 메서드는 리다이렉터에서 제공하며, 사용자가 인증 미들웨어로 인해 중단되기 전에 접근하려던 URL로 사용자를 리다이렉트합니다. 대상 경로가 없을 때 사용할 기본 경로도 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

이메일, 비밀번호 검증 이외에도, 인증에 추가 쿼리 조건을 붙일 수 있습니다. 배열 내에 추가 조건을 넣어 `attempt` 메서드에 전달하기만 하면 됩니다. 예를 들어, 사용자가 "활성(active)" 상태여야 함을 확인할 수도 있습니다.

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // 인증에 성공했습니다...
}
```

더 복잡한 쿼리가 필요한 경우 배열 내에 클로저를 추가하여 쿼리 인스턴스에 직접 조건을 추가할 수도 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // 인증에 성공했습니다...
}
```

> [!WARNING]
> 위 예시들에서 `email` 컬럼명은 단순 예시일 뿐 필수 사항이 아닙니다. 자신의 데이터베이스에서 "사용자 이름" 역할을 하는 컬럼명을 사용해야 합니다.

추가적으로, `attemptWhen` 메서드는 두 번째 인수로 클로저를 받아 인증 대상 사용자를 더 정밀하게 검사할 수 있습니다. 클로저는 사용자 인스턴스를 받아 true/false를 반환합니다.

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // 인증에 성공했습니다...
}
```

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근

`Auth` 파사드의 `guard` 메서드로 인증에 사용할 가드 인스턴스를 명시적으로 지정할 수 있습니다. 이를 통해 애플리케이션의 다른 영역별로 별개 인증 모델이나 사용자 테이블을 사용할 수 있습니다.

`guard`에 전달하는 이름은 `auth.php`의 `guards` 설정에 등록된 키와 일치해야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션은 로그인 폼에 "기억하기(remember me)" 체크박스를 제공합니다. 애플리케이션에서 해당 기능을 지원하려면, `attempt` 메서드의 두 번째 인수로 불리언 값을 전달하세요.

이 값이 `true`면, Laravel이 사용자를 영구적으로(또는 수동 로그아웃 시까지) 로그인 상태로 유지합니다. 이 기능을 사용하려면 `users` 테이블에 `remember_token` 컬럼(문자열 타입)이 있어야 합니다. 새 Laravel 애플리케이션의 마이그레이션에는 기본적으로 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // 사용자가 기억되는 중...
}
```

"기억하기" 기능이 있다면, 현재 인증된 사용자가 "기억하기" 쿠키로 로그인했는지 `viaRemember` 메서드로 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방식

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스로 인증

이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 설정해야 할 경우, `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 전달하세요. 전달된 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현해야 하며, 기본 `App\Models\User` 모델이 이미 구현하고 있습니다. 이 방법은, 예를 들어 회원가입 직후처럼, 이미 유효한 사용자 인스턴스가 있을 때 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인수로 불리언 값을 전달하면, "기억하기" 기능을 적용할지 여부를 결정할 수 있습니다. 참값이면 세션을 영구 인증 상태로 유지합니다.

```php
Auth::login($user, $remember = true);
```

필요 시, `login` 호출 전 가드를 지정할 수도 있습니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증

사용자의 데이터베이스 PK(기본키) 값으로 인증하려면, `loginUsingId` 메서드를 사용할 수 있습니다.

```php
Auth::loginUsingId(1);
```

"기억하기" 기능을 쓰려면 두 번째 인수에 불리언 값을 전달하세요.

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 사용자 인증

`once` 메서드는 세션이나 쿠키 없이, 한 번의 요청 동안만 사용자를 인증할 때 사용합니다. 이 메서드를 사용할 때는 `Login` 이벤트가 발생하지 않습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증 (HTTP Basic Authentication)

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지를 만들 필요 없이 간단하게 인증을 처리할 수 있는 방법입니다. 사용하려면, 해당 경로에 `auth.basic` [미들웨어](/docs/12.x/middleware)를 추가하세요. `auth.basic` 미들웨어는 Laravel에 포함되어 있으므로 별도 정의 없이 사용 가능합니다.

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근 가능...
})->middleware('auth.basic');
```

이 미들웨어를 경로에 추가하면, 브라우저에서 해당 경로로 접근 시 자동으로 인증 정보를 요구하는 프롬프트가 나타납니다. 기본적으로, `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자명으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 관련 참고사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache로 애플리케이션을 제공할 경우, HTTP Basic 인증이 제대로 동작하지 않을 수 있습니다. 이런 경우, 아래 내용을 애플리케이션의 `.htaccess` 파일에 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 무상태 HTTP Basic 인증

세션에 사용자 ID 쿠키를 저장하지 않고 기본 인증만을 사용할 수도 있습니다. 주로 API 인증에 사용하려는 경우 유용합니다. 이를 위해 [미들웨어를 정의](/docs/12.x/middleware)하고 `onceBasic` 메서드를 호출하세요. `onceBasic` 메서드가 null을 반환하지 않으면 요청 처리가 이어집니다.

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

이제 미들웨어를 경로에 연결하세요.

```php
Route::get('/api/user', function () {
    // 인증된 사용자만 접근 가능...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 수동으로 로그아웃 처리하려면, `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 사용자의 세션에서 인증 정보를 제거하여 이후 요청에서 더 이상 인증이 유지되지 않게 합니다.

`logout` 호출 외에도, 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/12.x/csrf)을 재생성하는 것이 권장됩니다. 로그아웃 이후에는 일반적으로 애플리케이션의 루트 경로로 리디렉션합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * 사용자를 로그아웃 처리.
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
### 다른 디바이스의 세션 무효화

Laravel은 한 사용자가 비밀번호를 변경할 때 등, "현재 디바이스는 유지하고" 다른 모든 디바이스의 세션을 무효화하는 기능도 제공합니다.

먼저, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 필요로 하는 경로에 포함되어 있는지 확인해야 합니다. 보통 라우트 그룹에 이 미들웨어를 설정해 대다수 경로에 적용합니다. 이 미들웨어는 기본적으로 `auth.session` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 사용 가능합니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그런 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 사용자가 현재 비밀번호를 입력해 인증해야 하며, 입력값은 폼을 통해 받아야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices`가 호출되면, 사용자의 다른 모든 세션이 완전히 무효화되어, 이전에 인증된 모든 가드에서 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션에서 일부 민감한 작업이나 영역으로 접근시에 사용자가 비밀번호를 다시 한 번 입력해 확인해야 하는 경우가 있습니다. Laravel은 이를 쉽게 처리할 수 있도록 기본 미들웨어를 제공합니다. 해당 기능은 "비밀번호 확인" 뷰를 보여주는 라우트와, 실제 비밀번호 유효성 검증 및 사용자를 의도한 위치로 리디렉션하는 라우트를 구현해야 합니다.

> [!NOTE]
> 아래 문서는 Laravel의 비밀번호 확인 기능을 직접 연동하는 방법에 대해 다루지만, 좀 더 빠르게 시작하려면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 활용하세요. 이미 지원이 내장되어 있습니다.

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호 확인 이후, 3시간 동안은 다시 비밀번호를 확인하도록 요구하지 않습니다. 이 시간 길이는 애플리케이션의 `config/auth.php` 설정 파일에서 `password_timeout` 값으로 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자에게 비밀번호를 입력하라는 뷰를 반환하는 라우트를 만듭니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 뷰에는 반드시 `password` 입력 필드가 포함되어야 하며, 사용자가 보호된 영역에 접근하려 하므로 비밀번호를 다시 입력해야 한다는 안내 문구도 넣어 주세요.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

이제, 폼으로부터 실제 요청을 처리하여 비밀번호 유효성 검증 및 리디렉션을 하는 라우트도 정의합시다.

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

이 라우트를 살펴보면, 먼저 입력한 비밀번호가 인증 사용자 계정의 실제 비밀번호와 일치하는지 검증합니다. 만약 일치한다면, Laravel 세션에 사용자가 비밀번호를 확인했다는 것을 남기기 위해 `passwordConfirmed` 메서드를 호출합니다. 이 메서드는 세션에 타임스탬프를 저장해, Laravel에서 사용자가 마지막으로 비밀번호를 언제 확인했는지 판단할 수 있게 도와줍니다. 마지막으로 사용자를 원래 의도한 목적지로 리디렉션합니다.

<a name="password-confirmation-protecting-routes"></a>
### 경로 보호

비밀번호 재확인을 요구하는 모든 경로에는 `password.confirm` 미들웨어를 반드시 적용해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 사용자의 "의도한 목적지" 정보를 세션에 저장한 후, `password.confirm` [네임드 라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다.

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 사용자 지정 가드 추가 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드로 사용자 지정 인증 가드를 직접 정의할 수 있습니다. 이 코드는 [서비스 제공자](/docs/12.x/providers) 내에 작성해야 하며, 보통 `AppServiceProvider`를 사용합니다.

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
            // Illuminate\Contracts\Auth\Guard 인스턴스를 반환해야 함...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예제에서처럼, `extend` 메서드에 전달된 콜백에서는 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 이 인터페이스가 정의한 몇 가지 메서드를 직접 구현해야 하며, 커스텀 가드를 정의한 후에는 `auth.php`의 `guards` 설정에서 사용할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 요청 가드 (Closure Request Guards)

HTTP 요청 기반의 단순한 커스텀 인증 시스템을 만들 때는 `Auth::viaRequest` 메서드로 빠르게 구현할 수 있습니다. 이 메서드는 하나의 클로저로 인증 과정을 정의할 수 있게 해줍니다.

`AppServiceProvider`의 `boot` 메서드 안에서 `viaRequest`를 호출해 시작하세요. 첫 번째 인자는 커스텀 가드의 이름(아무 문자열), 두 번째 인자는 요청 객체를 받아 사용자 인스턴스를 반환하거나, 인증 실패 시 null을 반환하는 클로저입니다.

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

커스텀 인증 드라이버를 정의한 뒤, `auth.php`의 `guards` 설정에서 해당 드라이버를 지정하세요.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

그리고 라우트 미들웨어 지정 시 해당 가드를 사용하면 됩니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 사용자 지정 사용자 제공자 추가 (Adding Custom User Providers)

사용자를 전통적인 관계형 데이터베이스에 저장하지 않는 경우, Laravel에 맞는 사용자 지정 인증 제공자를 구현해야 합니다. `Auth` 파사드의 `provider` 메서드로 직접 등록해줄 수 있으며, 반드시 `Illuminate\Contracts\Auth\UserProvider` 인터페이스를 구현한 객체를 반환해야 합니다.

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
            // Illuminate\Contracts\Auth\UserProvider 인스턴스를 반환...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

사용자 제공자를 등록한 후, `auth.php`에서 아래와 같이 새 드라이버를 지정합니다.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

이제 이 제공자를 `guards` 설정에서 사용할 수 있습니다.

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등 다양한 영구 저장소에서 조회·가져오는 역할을 담당합니다. 이 두 인터페이스 덕분에 사용자가 어디에 어떤 방식으로 저장되어 있든 인증 메커니즘은 일관되게 동작할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약을 살펴봅시다.

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

- `retrieveById`는 주로 자동 증가 PK 등 사용자를 고유하게 식별할 수 있는 키를 받아 그에 해당하는 `Authenticatable` 구현체를 반환해야 합니다.
- `retrieveByToken`은 고유 `$identifier`와 "remember me" `$token`으로 사용자를 조회합니다. 예를 들어 `remember_token` 컬럼을 검색하여 일치하는 사용자를 반환합니다.
- `updateRememberToken`은 사용자 인스턴스의 `remember_token` 값을 새 토큰으로 갱신합니다. 이 과정은 "기억하기"가 성공하거나 로그아웃시에 사용됩니다.
- `retrieveByCredentials`는 로그인 시 `Auth::attempt`로 전달되는 자격 증명 배열을 받아, 해당 조건에 맞는 사용자를 조회합니다. 일반적으로 `$credentials['username']` 값을 기반으로 쿼리합니다. **여기서는 비밀번호 비교 작업을 하지 마세요.**
- `validateCredentials`는 주어진 사용자와 입력 자격 증명을 비교해 인증을 수행합니다. 보통 `Hash::check`로 `$user->getAuthPassword()`와 `$credentials['password']`를 비교하고, 일치 여부를 true/false로 반환합니다.
- `rehashPasswordIfRequired`는 필요하다면 사용자의 비밀번호를 재해싱하고 영구 저장소에 업데이트합니다. 보통 `Hash::needsRehash`와 `Hash::make`를 활용합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

이제 `UserProvider`의 각 메서드를 이해했으니, `Authenticatable` 계약도 살펴보겠습니다. 제공자는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스를 준수하는 객체를 반환해야 합니다.

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

이 인터페이스는 매우 간단합니다.
- `getAuthIdentifierName`: 사용자의 "주키(primary key) 컬럼명" 반환
- `getAuthIdentifier`: 사용자의 "주키" 값 반환(예: MySQL의 자동 증가 PK)
- `getAuthPasswordName`: 비밀번호 컬럼명 반환
- `getAuthPassword`: 해시된 비밀번호 값을 반환

이 인터페이스 덕분에 ORM/추상화 계층에 상관없이 어떤 "사용자" 클래스도 인증 시스템과 연동할 수 있습니다. Laravel 기본 제공 `App\Models\User` 클래스도 이 계약을 구현합니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt 해시의 "work factor"는 애플리케이션의 `config/hashing.php` 설정 혹은 `BCRYPT_ROUNDS` 환경 변수로 조절할 수 있습니다.

컴퓨팅 파워가 향상됨에 따라 bcrypt work factor 값을 점진적으로 늘리는 것이 일반적입니다. work factor를 변경하더라도, 사용자가 Laravel의 스타터 키트 혹은 [수동 인증](#authenticating-users) 시 `attempt` 메서드를 통해 로그인하면, 자동으로 비밀번호가 새 work factor로 재해싱되고 저장됩니다.

일반적으로 자동 비밀번호 재해싱은 애플리케이션에 영향을 주지 않으나, 만약 이 동작을 비활성화하고 싶다면 `hashing` 설정 파일을 직접 배포한 후 다음과 같이 설정할 수 있습니다.

```shell
php artisan config:publish hashing
```

설정 파일에서 `rehash_on_login` 값을 `false`로 지정하세요.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 이벤트에 대해 [리스너를 정의](/docs/12.x/events)하여 활용할 수 있습니다.

<div class="overflow-auto">

| 이벤트명                                         |
| ---------------------------------------------- |
| `Illuminate\Auth\Events\Registered`            |
| `Illuminate\Auth\Events\Attempting`            |
| `Illuminate\Auth\Events\Authenticated`         |
| `Illuminate\Auth\Events\Login`                 |
| `Illuminate\Auth\Events\Failed`                |
| `Illuminate\Auth\Events\Validated`             |
| `Illuminate\Auth\Events\Verified`              |
| `Illuminate\Auth\Events\Logout`                |
| `Illuminate\Auth\Events\CurrentDeviceLogout`   |
| `Illuminate\Auth\Events\OtherDeviceLogout`     |
| `Illuminate\Auth\Events\Lockout`               |
| `Illuminate\Auth\Events\PasswordReset`         |
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

</div>
