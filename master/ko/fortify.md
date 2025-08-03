# Laravel Fortify

- [소개](#introduction)
    - [Fortify란 무엇인가요?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리다이렉트 커스터마이징](#customizing-authentication-redirects)
- [이중 인증](#two-factor-authentication)
    - [이중 인증 활성화](#enabling-two-factor-authentication)
    - [이중 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [이중 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드에 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후에는 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스를 제공하지 않으므로, 직접 만든 사용자 인터페이스와 연동되어 이 라우트에 요청을 보내도록 설계되었습니다. 이 문서에서는 이러한 라우트에 어떻게 요청을 보내는지 자세히 설명합니다.

> [!NOTE]
> Fortify는 Laravel의 인증 기능을 빠르게 구현할 수 있도록 도와주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** 언제든 Laravel의 인증, 비밀번호 재설정, 이메일 인증 공식 문서([authentication](/docs/master/authentication), [password reset](/docs/master/passwords), [email verification](/docs/master/verification))에 따라 직접 인증 서비스를 구현할 수 있습니다.

<a name="what-is-fortify"></a>
### Fortify란 무엇인가요?

앞서 언급했듯이, Laravel Fortify는 Laravel을 위한 프론트엔드에 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용해야 하는 것은 아닙니다.** 언제든 Laravel의 공식 인증, 비밀번호 재설정, 이메일 인증 문서를 참고하여 직접 구현할 수 있습니다.

Laravel에 익숙하지 않은 분들은 Fortify 사용 전 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 먼저 살펴보시길 권장합니다. 스타터 킷은 [Tailwind CSS](https://tailwindcss.com)로 만든 UI와 함께 인증 기능을 구현해 줍니다. 덕분에 Fortify가 해당 기능을 구현해주기 전, Laravel 인증 기능을 미리 익힐 수 있습니다.

Laravel Fortify는 결국 스타터 킷에서 제공하는 라우트와 컨트롤러를 사용자 인터페이스를 제외한 패키지 형태로 제공합니다. 따라서 특정 프론트엔드 방식을 강제하지 않으면서도 애플리케이션 인증 백엔드 구현을 빠르게 준비할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나요?

언제 Laravel Fortify를 사용하는 것이 적절할지 고민할 수 있습니다. 우선, Laravel의 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용 중이라면, Fortify를 별도로 설치할 필요가 없습니다. 스타터 킷에 이미 완벽한 인증 기능이 포함되어 있기 때문입니다.

스타터 킷을 사용하지 않으며, 애플리케이션에 인증 기능이 필요한 경우, 다음 두 가지 옵션이 있습니다: 직접 인증 기능을 구현하거나 Laravel Fortify를 사용하여 백엔드 구현을 맡기는 방법입니다.

Fortify를 설치하면, 여러분의 사용자 인터페이스는 이 문서에서 설명하는 Fortify의 인증 라우트에 요청을 보내 사용자 인증 및 회원가입 기능을 처리할 수 있습니다.

반대로 Fortify를 사용하지 않고 직접 인증 서비스를 구현하고 싶다면, [authentication](/docs/master/authentication), [password reset](/docs/master/passwords), [email verification](/docs/master/verification) 공식 문서를 참고해 구현할 수 있습니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum의 차이점

Laravel Sanctum와 Laravel Fortify의 차이로 혼동하는 개발자도 종종 있습니다. 이 두 패키지는 서로 다른, 그러나 관련된 문제를 해결하기 때문에 경쟁 관계나 상호 배타적인 패키지가 아닙니다.

Laravel Sanctum은 API 토큰 관리와 세션 쿠키 또는 토큰을 통한 기존 사용자 인증에만 집중합니다. Sanctum은 회원가입, 비밀번호 재설정 등의 라우트를 제공하지 않습니다.

만약 API를 제공하거나 SPA(싱글 페이지 애플리케이션)의 백엔드를 만들면서 인증 레이어를 직접 구축하려 한다면, 사용자 등록과 비밀번호 재설정을 위한 Laravel Fortify와 API 토큰 관리 및 세션 인증을 위한 Laravel Sanctum을 함께 사용하는 것이 가능합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로, `fortify:install` Artisan 명령어를 실행하여 Fortify의 리소스를 퍼블리시 합니다:

```shell
php artisan fortify:install
```

이 명령어는 `app/Actions` 디렉터리(존재하지 않으면 생성됨)에 Fortify의 액션들을 퍼블리시하고, `FortifyServiceProvider`, 설정 파일, 그리고 필요한 데이터베이스 마이그레이션도 함께 퍼블리시합니다.

마지막으로 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에는 `features` 배열이 있습니다. 이 배열은 기본적으로 Fortify가 활성화할 백엔드 라우트와 기능들을 정의합니다. 대부분 Laravel 애플리케이션이 제공하는 기본 인증 기능만 사용하려면 다음 세 가지 기능만 활성화할 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면이나 회원가입 화면 등 뷰를 반환하는 라우트도 정의합니다. 하지만 자바스크립트 기반 SPA를 구축한다면 이러한 라우트가 필요 없을 수 있습니다. 이런 경우, 애플리케이션의 `config/fortify.php` 설정 파일에서 `views` 값을 `false`로 설정해 뷰 반환 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화와 비밀번호 재설정

Fortify 뷰를 비활성화했는데 비밀번호 재설정 기능을 구현하려면, `password.reset`이라는 이름의 라우트를 반드시 정의해야 합니다. 이 라우트는 애플리케이션의 "비밀번호 재설정" 뷰를 보여주는 역할입니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 `password.reset`이라는 이름의 라우트를 통해 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

시작하려면 Fortify에 "로그인" 뷰를 어떻게 반환할지 알려줘야 합니다. Fortify는 클라이언트 UI 없이 백엔드만 제공하는 인증 라이브러리임을 기억하세요. 이미 완성된 Laravel 인증 기능 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용하세요.

모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 적절한 메서드들을 통해 커스터마이징할 수 있습니다. 보통 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 안에서 이 메서드를 호출합니다. Fortify는 `/login` 라우트를 정의하여 이 뷰를 반환합니다:

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

로그인 템플릿에는 `/login` 경로로 POST 요청을 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email` 또는 `username`과 `password`를 기대합니다. 이메일이나 사용자명 필드 이름은 `config/fortify.php` 설정 파일 내 `username` 값과 일치해야 합니다. 또한, 사용자에게 "로그인 유지" 기능을 제공하기 위해 불리언 `remember` 필드를 전달할 수도 있습니다.

로그인이 성공하면 Fortify는 애플리케이션의 `fortify` 설정 파일에 정의된 `home` 옵션의 URI로 리다이렉트합니다. 로그인 요청이 XHR(비동기) 요청이었으면 200 HTTP 응답이 반환됩니다.

로그인에 실패하면 사용자는 로그인 화면으로 다시 리다이렉트되며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청일 경우에는 422 HTTP 응답과 함께 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격 증명과 애플리케이션에서 설정한 인증 가드를 바탕으로 사용자를 자동으로 조회하고 인증합니다. 그러나 로그인을 어떻게 처리하고 사용자를 검색할지 완전히 직접 정의하고 싶을 수도 있습니다. Fortify는 `Fortify::authenticateUsing` 메서드를 통해 쉽게 이를 구현할 수 있습니다.

이 메서드는 클로저(익명 함수)를 인자로 받으며, 이 클로저는 들어오는 HTTP 요청을 받고 로그인 자격 증명을 검증한 후 관련된 사용자 인스턴스를 반환해야 합니다. 자격 증명이 유효하지 않거나 사용자를 찾을 수 없으면 `null` 또는 `false`를 반환해야 합니다. 보통 `FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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
#### 인증 가드

Fortify가 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 커스터마이징할 수 있습니다. 단, 설정한 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스 구현체여야 합니다. SPA 인증에 Fortify를 사용하려면 Laravel 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 함께 사용하는 것이 권장됩니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 일련의 호출 가능한 클래스(Invokable class)로 구성된 파이프라인을 통해 처리합니다. 원한다면 로그인 요청이 거치는 파이프라인을 직접 커스텀할 수 있습니다. 각 클래스는 들어오는 `Illuminate\Http\Request` 인스턴스를 받고, 미들웨어처럼 다음 클래스로 요청을 전달하는 `$next` 변수를 받는 `__invoke` 메서드를 가져야 합니다.

커스텀 파이프라인은 `Fortify::authenticateThrough` 메서드에서 클로저로 정의할 수 있습니다. 이 클로저는 로그인 요청이 통과할 클래스 배열을 반환해야 합니다. 보통 이 메서드는 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

아래 예시는 기본 파이프라인 정의이며, 여기에 원하는 대로 수정해 사용하세요:

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

#### 인증 시도 제한 (Throttling)

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어로 인증 시도를 제한합니다. 이 미들웨어는 사용자명과 IP 주소 조합별 고유한 시도 제한을 적용합니다.

일부 애플리케이션은 IP 주소만으로 제한하는 등의 다른 방식이 필요할 수 있으므로, Fortify는 `fortify.limiters.login` 설정 옵션을 통해 직접 [속도 제한(rate limiter)](/docs/master/routing#rate-limiting)을 지정할 수 있습니다. 이 설정은 `config/fortify.php` 파일에 위치합니다.

> [!NOTE]
> 인증 시도 제한, [이중 인증](/docs/master/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF)을 조합하면 합법적 사용자 보호에 가장 강력한 방어 체계를 구축할 수 있습니다.

<a name="customizing-authentication-redirects"></a>
### 리다이렉트 커스터마이징

로그인 성공 시 Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 옵션에 정의된 URI로 리다이렉트합니다. 로그인 요청이 XHR(비동기) 요청이었다면 200 HTTP 응답이 반환됩니다. 사용자가 로그아웃한 뒤에는 `/` URI로 리다이렉트됩니다.

이 동작을 고급으로 커스터마이징하려면 Laravel [서비스 컨테이너](/docs/master/container)에 `LoginResponse` 및 `LogoutResponse` 계약의 구현체를 바인딩할 수 있습니다. 보통 이는 애플리케이션 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드에서 수행합니다:

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
## 이중 인증

Fortify의 이중 인증 기능이 활성화되면, 인증 과정에서 사용자는 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 Google Authenticator 같은 TOTP 호환 모바일 인증 앱에서 생성된 시간 기반 일회용 비밀번호입니다.

먼저 애플리케이션의 `App\Models\User` 모델에 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트가 포함되어야 합니다:

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

다음으로, 사용자가 이중 인증 설정을 관리할 수 있는 화면을 만들어야 합니다. 이 화면은 이중 인증 활성화/비활성화 및 인증 복구 코드를 재생성하는 기능을 제공해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에 포함된 이중 인증 기능은 설정 변경 전 비밀번호 확인을 요구합니다. 따라서 이 문서의 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화

사용자가 이중 인증을 활성화하려면, 애플리케이션이 Fortify의 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 요청이 성공하면 사용자는 이전 페이지로 리다이렉트되고, 세션의 `status` 변수는 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 세션 변수를 확인해 성공 메시지를 표시할 수 있습니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

이중 인증을 활성화한 후에도 사용자는 유효한 인증 코드를 제출해 이중 인증 설정을 "확인"해야 합니다. 따라서 성공 메시지에는 이중 인증 확인이 아직 필요함을 안내해야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two factor authentication below.
    </div>
@endif
```

다음으로 사용자가 인증 앱으로 스캔할 수 있도록 이중 인증 QR 코드를 표시하세요. Blade를 사용한다면 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 SVG 코드를 얻을 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 프론트엔드를 사용한다면, `/user/two-factor-qr-code` 엔드포인트로 GET XHR 요청을 보내 QR 코드 SVG를 포함한 JSON 객체를 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인

이중 인증 QR 코드를 보여주는 것 외에도, 사용자가 인증 코드를 입력해 이중 인증 설정을 "확인"할 수 있도록 텍스트 입력 필드를 제공해야 합니다. 이 인증 코드는 Fortify의 `/user/confirmed-two-factor-authentication` 엔드포인트에 POST 요청으로 보내야 합니다.

성공 시 사용자는 이전 페이지로 리다이렉트되고, 세션의 `status` 변수는 `two-factor-authentication-confirmed`로 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two factor authentication confirmed and enabled successfully.
    </div>
@endif
```

AJAX 요청이라면 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

사용자가 모바일 기기에 접근할 수 없을 때 인증할 수 있도록 복구 코드를 표시해야 합니다. Blade를 쓰는 경우 인증된 사용자 인스턴스에서 복구 코드를 배열로 가져올 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프론트엔드에서는 `/user/two-factor-recovery-codes` 엔드포인트에 GET XHR 요청을 보내 복구 코드 배열을 JSON 형태로 받을 수 있습니다.

복구 코드를 재생성하려면 POST 요청을 같은 엔드포인트에 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

인증 과정 중 Fortify는 자동으로 애플리케이션의 이중 인증 도전 화면으로 리다이렉트합니다. 하지만 로그인 요청이 XHR이라면, 성공 응답 JSON에 `two_factor`라는 불리언 속성이 포함됩니다. 이 값을 확인하여 이중 인증 화면으로 리다이렉트할지 결정하세요.

이중 인증 도전 뷰를 반환하는 방식을 Fortify에 알려줘야 합니다. 모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify`의 메서드로 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify가 `/two-factor-challenge` 경로를 정의하며 이 뷰를 반환합니다. 해당 템플릿에는 POST 요청을 `/two-factor-challenge`로 보내는 폼이 포함되어야 합니다. 이 엔드포인트는 유효한 TOTP 토큰을 담은 `code` 필드 또는 사용자 복구 코드 중 하나인 `recovery_code` 필드를 기대합니다.

로그인이 성공하면 Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 옵션에 정의된 URI로 리다이렉트합니다. XHR 요청이라면 204 HTTP 응답이 반환됩니다.

실패 시 사용자는 도전 화면으로 리다이렉트되고, 검증 오류는 `$errors` Blade 템플릿 변수에서 확인할 수 있습니다. XHR 요청일 경우 422 HTTP 응답으로 검증 오류가 전달됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화

이중 인증을 비활성화하려면, 애플리케이션이 Fortify의 `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내야 합니다. 이중 인증 관련 Fortify 엔드포인트는 호출 전에 [비밀번호 확인](#password-confirmation)이 필요함을 기억하세요.

<a name="registration"></a>
## 회원가입

애플리케이션의 회원가입 기능 구현을 시작하려면, Fortify에 "회원가입" 뷰를 반환하는 방식을 알려줘야 합니다. Fortify는 프론트엔드 없이 백엔드 인증 라이브러리임을 기억하세요. 이미 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용하세요.

모든 회원가입 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify는 `/register` 라우트를 정의하여 이 뷰를 반환합니다. `register` 템플릿은 Fortify가 정의한 `/register` 엔드포인트로 POST 요청을 보내는 폼을 포함해야 합니다.

`/register` 엔드포인트는 문자열 타입의 `name`, 문자열 이메일 주소/사용자명, `password`, `password_confirmation` 필드를 요구합니다. 이메일/사용자명 필드명은 `fortify` 설정 파일 내 `username` 옵션과 일치해야 합니다.

회원가입 성공 시 Fortify는 `fortify` 설정 파일 내 `home` 옵션에 정의된 URI로 리다이렉트합니다. XHR 요청일 경우 201 HTTP 응답이 반환됩니다.

실패 시 사용자는 회원가입 화면으로 리다이렉트되며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)에서 확인할 수 있습니다. XHR 요청 시 422 HTTP 응답으로 검증 오류가 전달됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

사용자 검증과 생성 과정은 Laravel Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정하여 커스터마이징할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

애플리케이션의 비밀번호 재설정 기능을 구현하려면 Fortify에 "비밀번호 찾기" 뷰를 반환하는 방식을 알려줘야 합니다. Fortify는 프론트엔드 없이 백엔드 인증 라이브러리임을 기억하세요. 이미 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용하세요.

모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify는 `/forgot-password` 엔드포인트를 정의하여 이 뷰를 반환합니다. `forgot-password` 템플릿은 `/forgot-password`로 POST 요청을 보내는 폼을 포함해야 합니다.

`/forgot-password` 엔드포인트는 문자열 타입의 `email` 필드를 기대합니다. 이 필드명/DB 컬럼명은 애플리케이션의 `fortify` 설정 파일 내 `email` 옵션과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 결과 처리

비밀번호 재설정 링크 요청이 성공하면, Fortify는 사용자를 `/forgot-password` 경로로 리다이렉트하고, 사용자에게 비밀번호 재설정에 사용할 수 있는 안전한 링크를 포함하는 이메일을 보냅니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

성공 후 `/forgot-password` 페이지로 리다이렉트되면, 세션 `status` 변수를 사용해 재설정 링크 요청 상태 메시지를 표시할 수 있습니다.

이 세션 변수의 값은 애플리케이션의 `passwords` [언어 파일](/docs/master/localization)에 정의된 번역 문자열 중 하나와 일치합니다. Laravel의 언어 파일을 퍼블리시하지 않았다면, `lang:publish` Artisan 명령어로 퍼블리시 후 수정 가능 합니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

요청이 실패하면 사용자는 비밀번호 재설정 링크 요청 화면으로 리다이렉트되며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청일 경우 422 HTTP 응답과 함께 오류가 전달됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

애플리케이션의 비밀번호 재설정 기능 구현을 마치려면 Fortify에 "비밀번호 재설정" 뷰를 반환하는 방식을 알려줘야 합니다.

모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify는 이 뷰를 표시하는 라우트를 정의합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청을 보내는 폼을 포함해야 합니다.

`/reset-password` 엔드포인트는 문자열 `email`, `password`, `password_confirmation` 필드와 숨긴 필드 `token`(값은 `request()->route('token')`)을 기대합니다. 이메일 필드명/DB 컬럼명은 `fortify` 설정 파일 내 `email` 옵션과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 결과 처리

비밀번호 재설정 요청이 성공하면 Fortify는 사용자를 `/login` 경로로 리다이렉트해 새 비밀번호로 로그인할 수 있게 합니다. 또한 `status` 세션 변수를 설정해 성공 상태 메시지를 로그인 화면에 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청일 경우 200 HTTP 응답이 반환됩니다.

요청 실패 시 사용자는 비밀번호 재설정 화면으로 리다이렉트되고, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)에서 확인할 수 있습니다. XHR 요청 시 422 HTTP 응답으로 오류가 전달됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 커스터마이징할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자가 계속해서 애플리케이션을 이용하기 전에 이메일 주소를 인증하도록 유도하려 할 수 있습니다. 시작하려면 `fortify` 설정 파일 내 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그리고 애플리케이션의 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현했는지 확인해야 합니다.

설정이 완료되면 새로 가입한 사용자에게 이메일 주소 소유를 확인하도록 이메일이 발송됩니다. 그러나 이메일에 첨부된 인증 링크를 클릭하라는 안내 화면을 보여주는 방식을 Fortify에 알려줘야 합니다.

모든 이메일 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify는 Laravel 내장 `verified` 미들웨어에 의해 `/email/verify` 엔드포인트로 리다이렉트될 때 이 뷰를 표시하는 라우트를 정의합니다.

`verify-email` 템플릿에는 사용자에게 이메일로 전송된 인증 링크를 클릭하라는 안내 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

필요하다면, 애플리케이션의 `verify-email` 템플릿에 `/email/verification-notification`으로 POST 요청을 트리거하는 버튼을 추가할 수 있습니다. 이 엔드포인트를 통해 새로운 인증 이메일이 사용자에게 전송되어 이전 링크를 분실하거나 삭제한 경우 새 링크를 받을 수 있습니다.

재전송 요청이 성공하면 Fortify는 `/email/verify` 엔드포인트로 `status` 세션 변수를 포함해 리다이렉트하여, 성공 메시지를 표시할 수 있게 합니다. XHR 요청일 경우 202 HTTP 응답이 반환됩니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호

특정 라우트 또는 라우트 그룹에 사용자 이메일 인증이 완료된 경우에만 접근하도록 하려면, Laravel 내장 `verified` 미들웨어를 해당 라우트에 붙이면 됩니다. `verified` 미들웨어는 Laravel이 자동으로 등록하며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션 개발 중 가끔 사용자에게 민감한 작업 수행 전에 현재 비밀번호 재확인을 요구해야 할 경우가 있습니다. 일반적으로 이러한 라우트는 Laravel 내장 `password.confirm` 미들웨어로 보호됩니다.

비밀번호 확인 기능을 구현하려면, Fortify에 애플리케이션의 "비밀번호 확인" 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 프론트엔드가 없는 백엔드 인증 라이브러리임을 기억하세요. 이미 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 쓰시길 권장합니다.

모든 비밀번호 확인 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스 메서드로 커스터마이징할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

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

Fortify는 `/user/confirm-password` 엔드포인트를 정의해 뷰를 반환합니다. `confirm-password` 템플릿에는 `/user/confirm-password`로 POST 요청을 보내는 폼을 포함해야 합니다. 이 엔드포인트는 사용자의 현재 비밀번호를 담은 `password` 필드를 기대합니다.

비밀번호가 사용자 현재 비밀번호와 일치하면 Fortify는 사용자가 요청했던 라우트로 리다이렉트합니다. XHR 요청인 경우 201 HTTP 응답이 반환됩니다.

요청이 실패하면 사용자는 비밀번호 확인 화면으로 리다이렉트되고, 검증 오류는 `$errors` Blade 템플릿 변수에서 확인할 수 있습니다. XHR 요청일 경우 422 HTTP 응답으로 검증 오류가 반환됩니다.