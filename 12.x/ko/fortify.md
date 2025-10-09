# 라라벨 Fortify (Laravel Fortify)

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능들](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리디렉션 커스터마이징](#customizing-authentication-redirects)
- [2단계 인증](#two-factor-authentication)
    - [2단계 인증 활성화](#enabling-two-factor-authentication)
    - [2단계 인증으로 로그인하기](#authenticating-with-two-factor-authentication)
    - [2단계 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호하기](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Fortify](https://github.com/laravel/fortify)는 라라벨을 위한 프론트엔드에 종속되지 않는 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 라라벨의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후에는 `route:list` 아티즌 명령어를 실행하여 Fortify가 등록한 라우트들을 확인할 수 있습니다.

Fortify는 별도의 사용자 인터페이스(UI)를 제공하지 않으므로, Fortify가 등록한 라우트에 요청을 보내는 여러분만의 UI와 함께 사용해야 합니다. 이러한 라우트에 요청하는 방법은 이 문서의 뒷부분에서 자세히 설명합니다.

> [!NOTE]
> Fortify는 라라벨의 인증 기능을 빠르게 구현할 수 있도록 도와주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** [인증](/docs/12.x/authentication), [비밀번호 재설정](/docs/12.x/passwords), [이메일 인증](/docs/12.x/verification) 관련 공식 문서를 참고하여 라라벨의 인증 서비스를 직접 활용할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란? (What is Fortify?)

앞서 언급했듯이, Laravel Fortify는 라라벨을 위한 프론트엔드에 종속적이지 않은 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다.

**라라벨의 인증 기능을 사용하려면 Fortify를 반드시 설치해야 하는 것은 아닙니다.** [인증](/docs/12.x/authentication), [비밀번호 재설정](/docs/12.x/passwords), [이메일 인증](/docs/12.x/verification) 공식 문서에 따라 직접 구현할 수도 있습니다.

라라벨을 처음 접하는 분들은 Fortify를 사용하기 전에 [스타터 킷](/docs/12.x/starter-kits)을 먼저 살펴보는 것을 권장합니다. 스타터 킷은 [Tailwind CSS](https://tailwindcss.com)로 만들어진 사용자 인터페이스와 인증에 필요한 기본 구현이 이미 포함되어 있으므로, 인증 시스템의 동작 방식을 익히기에 적합합니다.

Fortify는 사실상 스타터 킷의 인증 라우트와 컨트롤러 부분만 별도의 패키지로 제공하는 것이며, UI를 포함하지 않아 다양한 프론트엔드와 조합해 인증 백엔드를 빠르게 구축할 수 있게 해줍니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나? (When Should I Use Fortify?)

Fortify 사용 시기를 고민할 수 있습니다. 우선, 라라벨의 [스타터 킷](/docs/12.x/starter-kits)을 사용 중이라면 Fortify를 별도로 설치할 필요가 없습니다. 모든 스타터 킷에는 이미 완성된 인증 기능이 포함되어 있습니다.

스타터 킷을 사용하지 않고 별도로 인증 기능이 필요한 애플리케이션이라면, 두 가지 방식 중 하나를 선택할 수 있습니다. 직접 인증 서비스를 구현하거나, Fortify로 인증의 백엔드 부분을 빠르게 구축하는 방법이 있습니다.

Fortify를 설치하면, 여러분의 프론트엔드 UI는 인증 및 회원가입 처리를 위해 Fortify가 등록한 라우트에 요청을 보내게 됩니다. 이 문서에서 요청 방식에 대해 설명합니다.

만약 Fortify 사용 대신 인증 관련 기능을 직접 구현하고 싶다면, [인증](/docs/12.x/authentication), [비밀번호 재설정](/docs/12.x/passwords), [이메일 인증](/docs/12.x/verification) 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### 라라벨 Fortify와 라라벨 Sanctum

일부 개발자들은 [Laravel Sanctum](/docs/12.x/sanctum)과 Fortify의 차이점에 대해 혼란스러워할 수 있습니다. 두 패키지는 서로 다른 목적을 가지고 있으므로, Fortify와 Sanctum은 경쟁하거나 상호 배타적이지 않습니다.

Laravel Sanctum은 API 토큰 관리 및 기존 사용자의 세션 또는 토큰 인증에만 집중합니다. 회원가입, 비밀번호 재설정 등의 라우트는 제공하지 않습니다.

만약 API를 제공하는 애플리케이션이나 싱글페이지 애플리케이션(SPA) 백엔드를 직접 구현하는 경우, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)을 함께 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 사용하여 Fortify를 설치합니다.

```shell
composer require laravel/fortify
```

다음으로, `fortify:install` 아티즌 명령어를 통해 Fortify의 리소스를 퍼블리시합니다.

```shell
php artisan fortify:install
```

이 명령어는 `app/Actions` 디렉터리에 Fortify 액션들을 복사합니다. 해당 디렉터리가 없으면 자동으로 생성됩니다. 또한, `FortifyServiceProvider`, 설정 파일, 필요한 데이터베이스 마이그레이션 파일도 함께 추가됩니다.

다음으로 데이터베이스를 마이그레이션합니다.

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능들 (Fortify Features)

`fortify` 설정 파일에는 `features` 설정 배열이 있습니다. 이 배열을 통해 Fortify에서 제공하는 백엔드 라우트와 기능을 개별적으로 활성화할 수 있습니다. 대부분의 라라벨 애플리케이션에서는 기본 인증 기능들만을 아래와 같이 사용하면 충분합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화 (Disabling Views)

Fortify는 기본적으로 로그인/회원가입 등 일부 라우트가 뷰를 반환하도록 설정되어 있습니다. 하지만 자바스크립트 기반의 싱글페이지 애플리케이션(SPA)이라면 이러한 뷰 라우트가 필요 없을 수도 있습니다. 이 경우, `config/fortify.php` 설정 파일의 `views` 값을 `false`로 변경해 관련 라우트 전체를 비활성화할 수 있습니다.

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰와 비밀번호 재설정 비활성화

만약 Fortify의 뷰를 비활성화하면서 애플리케이션에서 비밀번호 재설정 기능을 구현해야 한다면, 반드시 애플리케이션에 `password.reset` 이라는 이름의 라우트를 정의해야 합니다. 이는 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 링크를 생성할 때 `password.reset` 이름의 라우트를 참조하기 때문입니다.

<a name="authentication"></a>
## 인증 (Authentication)

우선, Fortify가 우리의 "로그인" 뷰를 반환하는 방법을 지정해야 합니다. Fortify는 헤드리스(headless) 인증 라이브러리이므로, 미리 완성된 프론트엔드가 필요한 경우에는 [스타터 킷](/docs/12.x/starter-kits)의 사용을 고려하세요.

인증 뷰의 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드를 통해 커스터마이즈할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내부에서 호출합니다. Fortify는 `/login` 라우트를 자동으로 정의하여 지정한 뷰를 반환합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼(form)이 포함되어야 합니다. `/login` 엔드포인트는 `email`(또는 `username`), `password` 값을 기대합니다. 이메일 또는 사용자명 필드명은 `config/fortify.php` 설정 파일의 `username` 값과 일치해야 합니다. 추가로, "로그인 상태 유지" 기능을 위한 불리언 타입의 `remember` 필드를 사용할 수도 있습니다.

로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정한 URI로 리디렉션합니다. 로그인 요청이 XHR(비동기) 요청이었다면 200 HTTP 응답을 반환합니다.

로그인에 실패하면 사용자는 로그인 화면으로 다시 리디렉션되며, 유효성 검증 오류 메시지들은 공유 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)를 통해 뷰에서 접근할 수 있습니다. XHR 요청의 경우 422 응답코드와 함께 유효성 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징 (Customizing User Authentication)

Fortify는 기본적으로 제공된 인증 정보와 설정된 인증 가드를 기반으로 사용자를 조회하고 인증합니다. 그러나 로그인 자격 증명 인증 및 사용자 조회 과정을 완전히 커스터마이즈하고 싶을 때는 `Fortify::authenticateUsing` 메서드를 사용할 수 있습니다.

이 메서드는 HTTP 요청을 전달받는 클로저를 인자로 받습니다. 클로저는 요청에 담긴 로그인 자격 증명을 검증하고 해당 사용자를 반환해야 하며, 자격 증명이 잘못되었거나 사용자를 찾을 수 없으면 `null` 또는 `false`를 반환해야 합니다. 일반적으로 이 코드는 `FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::authenticateUsing(function (Request $request) {
        $user = User::where('email', $request->email)->first();

        if ($user &&
            Hash::check($request->password, $user->password)) {
            return $user;
        }
    });

    // ...
}
```

<a name="authentication-guard"></a>
#### 인증 가드 (Authentication Guard)

Fortify에서 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 단, 설정된 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스를 구현해야 합니다. 만약 SPA 인증에 Fortify를 사용하려면, 라라벨의 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 함께 사용하는 것이 적합합니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징 (Customizing the Authentication Pipeline)

Fortify는 로그인 요청을 여러 클래스가 순차적으로 처리하는 파이프라인 구조를 사용합니다. 만약 로그인을 처리하는 커스텀 파이프라인 클래스를 정의하고 싶다면, `Fortify::authenticateThrough` 메서드를 사용할 수 있습니다. 각 파이프라인 클래스는 `__invoke` 메서드를 구현해야 하며, [미들웨어](/docs/12.x/middleware)처럼 `$next` 인자를 통해 다음 클래스로 요청을 전달합니다.

커스텀 파이프라인을 정의하려면, 클로저에서 파이프라인 클래스를 배열로 반환하세요. 일반적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 작성합니다.

아래는 기본 파이프라인 예시로, 필요에 따라 참고해 수정할 수 있습니다.

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\CanonicalizeUsername;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Features;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            config('fortify.lowercase_usernames') ? CanonicalizeUsername::class : null,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

#### 인증 요청 제한 (Authentication Throttling)

Fortify는 기본적으로 `EnsureLoginIsNotThrottled` 미들웨어를 통해 사용자명과 IP 주소 조합별로 인증 시도를 제한합니다.

일부 애플리케이션은 IP 주소별로만 제한하는 등 다른 방식의 접근을 원할 수 있으므로, `fortify.limiters.login` 설정값을 통해 [사용자 정의 rate limiter](/docs/12.x/routing#rate-limiting)를 지정할 수 있습니다. 해당 옵션은 `config/fortify.php` 파일에 위치합니다.

> [!NOTE]
> 인증 시도 제한, [2단계 인증](/docs/12.x/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF) 등을 적절히 결합하면 사용자 계정을 가장 안정적으로 보호할 수 있습니다.

<a name="customizing-authentication-redirects"></a>
### 리디렉션 커스터마이징 (Customizing Redirects)

로그인에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다. 사용자가 로그아웃하면 루트 URL(`/`)로 리디렉션됩니다.

이 동작을 더 세밀하게 제어하려면 `LoginResponse`와 `LogoutResponse` 계약을 라라벨 [서비스 컨테이너](/docs/12.x/container)에 바인딩할 수 있습니다. 주로 `App\Providers\FortifyServiceProvider`의 `register` 메서드에서 등록합니다.

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->instance(LogoutResponse::class, new class implements LogoutResponse {
        public function toResponse($request)
        {
            return redirect('/');
        }
    });
}
```

<a name="two-factor-authentication"></a>
## 2단계 인증 (Two-Factor Authentication)

Fortify의 2단계 인증(two-factor authentication) 기능을 활성화하면, 사용자는 인증 과정 중 6자리 숫자 토큰 입력을 요구받게 됩니다. 이 토큰은 구글 인증(Google Authenticator) 등 TOTP 호환 모바일 앱으로 생성된 일회용 비밀번호입니다.

사용 전 반드시 애플리케이션의 `App\Models\User` 모델에서 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;

class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;
}
```

그 다음 두 단계 인증 관리 화면(활성화/비활성화, 복구 코드 재생성 등)을 구현해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에서는 2단계 인증 설정 시 비밀번호 확인이 필요하도록 구성되어 있습니다. 따라서, 애플리케이션에 Fortify의 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화 (Enabling Two-Factor Authentication)

2단계 인증 활성화는 Fortify가 제공하는 `/user/two-factor-authentication` 엔드포인트에 POST 요청을 보내는 방식으로 시작합니다. 요청이 성공하면, 사용자는 이전 URL로 리디렉션되며 `status` 세션 변수에 `two-factor-authentication-enabled` 값이 할당됩니다. 이 세션 변수를 템플릿에서 검사해 성공 메시지를 표시할 수 있습니다. XHR 요청이라면 200 응답이 반환됩니다.

사용자가 2단계 인증을 활성화하면, 반드시 유효한 인증 코드를 입력해 "2단계 인증 구성을 완료"해야 합니다. 다음은 상황에 맞는 안내 메시지 예시입니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```

그 다음 사용자가 인증 앱에 등록할 수 있도록 2단계 인증용 QR 코드를 보여줘야 합니다. Blade를 사용하는 경우, 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 SVG QR 코드를 얻을 수 있습니다.

```php
$request->user()->twoFactorQrCodeSvg();
```

만약 자바스크립트 기반 프론트엔드라면 `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보내면 `svg` 키가 포함된 JSON을 받게 됩니다.

<a name="confirming-two-factor-authentication"></a>
#### 2단계 인증 구성 확인

QR 코드 외에도, 사용자가 인증 코드를 입력할 텍스트 입력란을 마련해야 하며, 이 코드는 `/user/confirmed-two-factor-authentication` 엔드포인트에 POST 요청으로 전송됩니다.

인증에 성공하면 사용자는 이전 URL로 리디렉션되고, `status` 변수가 `two-factor-authentication-confirmed`로 변경됩니다.

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```

XHR 요청의 경우에는 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

2단계 인증 복구 코드도 함께 표시해야 합니다. 복구 코드는 사용자가 휴대폰 접근 권한을 잃었을 때를 대비한 인증 수단입니다. Blade를 사용할 경우 아래처럼 복구 코드를 배열로 가져올 수 있습니다.

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 기반 프론트엔드는 `/user/two-factor-recovery-codes` 엔드포인트에 GET 요청을 보내면 복구 코드가 배열 형태로 반환됩니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 로그인하기 (Authenticating With Two-Factor Authentication)

인증 과정에서 Fortify는 자동으로 사용자를 2단계 인증 도전 화면으로 리디렉션합니다. 단, XHR 방식으로 로그인한 경우에는 응답 JSON에 `two_factor` 불리언 값이 포함되며, 이를 확인해 2단계 인증 화면으로 이동할지 결정할 수 있습니다.

2단계 인증 도전 화면을 반환하는 방법 역시 Fortify의 뷰 렌더링 메서드를 통해 지정할 수 있습니다. 통상적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 아래처럼 설정합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify는 `/two-factor-challenge` 라우트를 자동으로 등록하며, 이 뷰에서 실제 도전 폼을 작성해 `/two-factor-challenge` 엔드포인트로 POST 요청을 보냅니다. 이 요청에는 유효한 TOTP 코드가 담긴 `code` 필드 또는 복구 코드가 담긴 `recovery_code` 필드가 있어야 합니다.

로그인에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 이동합니다. XHR 요청의 경우 204 응답을 반환합니다.

실패하면 2단계 인증 화면으로 돌아가고, 유효성 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)나 XHR 응답(422)으로 확인할 수 있습니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화 (Disabling Two-Factor Authentication)

2단계 인증을 비활성화하려면, `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내면 됩니다. Fortify의 2단계 인증 관련 엔드포인트 호출 전에는 [비밀번호 확인](#password-confirmation)이 선행되어야 함을 기억하세요.

<a name="registration"></a>
## 회원가입 (Registration)

회원가입 기능 구현 역시 "회원가입" 뷰 반환 방법을 Fortify에 지정하는 것으로 시작합니다. Fortify는 헤드리스 라이브러리이므로, 미리 완성된 프론트엔드가 필요하다면 [스타터 킷](/docs/12.x/starter-kits) 사용을 고려하세요.

모든 뷰 반환 방식은 `Laravel\Fortify\Fortify` 클래스의 메서드로 지정할 수 있으며, 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify는 `/register` 라우트를 자동으로 등록하며, 회원가입 양식은 Fortify가 정의한 `/register` 엔드포인트로 POST 요청을 보내야 합니다.

`/register` 엔드포인트는 `name`(문자열), email(또는 username), `password`, `password_confirmation` 필드를 기대합니다. 이메일(또는 사용자명) 필드는 애플리케이션의 `fortify` 설정 파일의 `username` 값과 동일한 이름이어야 합니다.

회원가입에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 이동합니다. XHR 요청이라면 201 HTTP 응답이 반환됩니다.

실패하면 회원가입 화면으로 돌아가며, 오류는 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors) 또는 XHR 응답(422)을 통해 접근할 수 있습니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징 (Customizing Registration)

사용자 검증 및 생성 프로세스는 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정해서 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정 (Password Reset)

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting a Password Reset Link)

비밀번호 재설정 기능 구현을 위해 "비밀번호 찾기" 뷰 반환 방법을 Fortify에 지정해야 합니다. Fortify는 별도의 프론트엔드를 제공하지 않으니, 미리 완성된 UI가 필요하다면 [스타터 킷](/docs/12.x/starter-kits) 사용을 고려하세요.

뷰 반환 로직은 `Laravel\Fortify\Fortify` 클래스 메서드를 통해 지정하며, 주로 `App\Providers\FortifyServiceProvider` 내에서 설정합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify는 `/forgot-password` 엔드포인트를 자동 등록하며, 비밀번호 찾기 양식은 이 엔드포인트로 POST 요청을 보내야 합니다.

해당 엔드포인트는 `email` 하나의 문자열 필드를 기대하며, 필드/컬럼 이름은 `fortify` 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면, 사용자는 `/forgot-password` 엔드포인트로 리디렉션되고, 비밀번호 재설정을 위한 보안 링크가 이메일로 전송됩니다. XHR 요청이라면 200 응답이 반환됩니다.

요청이 성공하게 되면, `status` 세션 변수를 활용해 사용자가 요청 상태를 확인할 수 있게 안내 메시지를 출력할 수 있습니다.

`$status` 세션 변수는 애플리케이션의 `passwords` [언어 파일](/docs/12.x/localization)에 정의된 번역 문자열 중 하나입니다. 이를 커스터마이즈하려면 라라벨의 언어 파일을 퍼블리시(publish) 후 수정하면 됩니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패한 경우 비밀번호 재설정 링크 요청화면으로 돌아가고, 유효성 오류는 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors) 혹은 XHR(422) 응답을 통해 확인할 수 있습니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

비밀번호 재설정 기능을 마무리하려면 "비밀번호 재설정" 뷰를 반환하는 방법을 Fortify에 등록해야 합니다.

모든 뷰 반환 로직은 `Laravel\Fortify\Fortify`의 적절한 메서드를 사용하며, 일반적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에 아래처럼 작성합니다.

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify는 자동으로 해당 경로의 라우트를 정의하며, `reset-password` 템플릿에는 `/reset-password` 엔드포인트로 POST 요청을 보내는 폼이 있어야 합니다.

`/reset-password` 엔드포인트는 `email`, `password`, `password_confirmation` 필드와, 숨겨진 필드 `token`(값은 `request()->route('token')`)이 필요합니다. "이메일" 필드/컬럼명은 `fortify` 설정 파일의 `email` 값과 동일해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

재설정이 성공하면, Fortify는 `/login` 라우트로 사용자를 이동시켜 새 비밀번호로 로그인을 유도합니다. 또한, 로그인 화면에서 성공 메시지를 출력할 수 있도록 `status` 세션 변수가 설정됩니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청인 경우 200 응답이 반환됩니다.

실패하면 비밀번호 재설정 화면으로 돌아가고, 유효성 오류는 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)나 XHR(422) 응답으로 확인할 수 있습니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징 (Customizing Password Resets)

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증 (Email Verification)

회원가입 후 사용자가 애플리케이션을 계속 이용하려면 이메일 인증을 요구할 수 있습니다. 먼저, `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그리고 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하는지 확인해야 합니다.

이 두 가지가 완료되면, 새로 가입한 사용자는 본인 이메일 주소 소유권 확인을 위한 이메일을 수신합니다. 이제 다음 단계로 실제 인증 안내 화면을 Fortify에 구현 방법을 알려야 합니다.

모든 뷰 반환 로직은 `Laravel\Fortify\Fortify`의 메서드를 사용하며, 일반적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify는 `/email/verify` 엔드포인트에 대응하는 라우트를 자동으로 정의합니다. 이는 라라벨 내장 `verified` 미들웨어를 통해 리디렉션됩니다.

`verify-email` 템플릿에는 인증 이메일 내 링크를 반드시 확인하라고 사용자에게 안내하는 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재발송

필요하다면 `verify-email` 템플릿에 버튼을 두고, 이를 통해 `/email/verification-notification` 엔드포인트로 POST 요청을 보낼 수 있습니다. 이 요청이 들어오면 인증 이메일 링크가 새로 사용자에게 발송됩니다.

재발송이 성공하면 Fortify가 `/email/verify` 엔드포인트로 사용자를 리디렉션하고, `status` 세션 변수가 설정되어 성공 메시지를 띄울 수 있습니다. XHR 요청의 경우 202 응답이 반환됩니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

특정 라우트 또는 라우트 그룹에 반드시 이메일 인증이 필요하게 만들려면, 라라벨 내장 `verified` 미들웨어를 해당 라우트에 적용하세요. 이 미들웨어 별칭은 자동으로 등록되며, 실제로는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어입니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

일부 기능 또는 작업은 사용자의 비밀번호 확인이 반드시 필요할 수 있습니다. 이런 라우트는 라라벨 내장 `password.confirm` 미들웨어로 보호합니다.

비밀번호 확인 기능을 구현하려면, Fortify에서 "비밀번호 확인" 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 헤드리스 인증 라이브러리이며, 완성된 프론트엔드가 필요하면 [스타터 킷](/docs/12.x/starter-kits) 사용을 고려하세요.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 지정하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 아래와 같이 사용합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify는 `/user/confirm-password` 엔드포인트를 자동으로 등록하며, confirm-password 템플릿은 이 엔드포인트로 POST 요청을 보내는 폼을 포함해야 합니다. `password` 필드에는 사용자의 현재 비밀번호가 입력되어야 합니다.

비밀번호가 일치하면 사용자는 원래 접근하려던 라우트(페이지)로 리디렉션됩니다. XHR 요청의 경우 201 응답이 반환됩니다.

비밀번호가 틀린 경우 비밀번호 확인 화면으로 돌아가고, 유효성 오류는 `$errors` Blade 템플릿 변수 또는 XHR(422) 응답을 통해 확인할 수 있습니다.
