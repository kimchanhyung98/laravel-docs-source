# Laravel Fortify

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [Fortify를 언제 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리디렉션 커스터마이징](#customizing-authentication-redirects)
- [이중 인증 (Two Factor Authentication)](#two-factor-authentication)
    - [이중 인증 활성화](#enabling-two-factor-authentication)
    - [이중 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [이중 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청하기](#requesting-a-password-reset-link)
    - [비밀번호 재설정 처리하기](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호하기](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드와 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel이 제공하는 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치하면 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않기 때문에 직접 작성한 UI가 Fortify가 등록한 라우트에 요청을 보내는 방식으로 동작합니다. 이 문서의 나머지 부분에서 이러한 라우트에 요청을 보내는 방법을 자세히 설명합니다.

> [!NOTE]  
> Fortify는 Laravel의 인증 기능 구현 시 빠른 출발점을 제공하는 패키지임을 기억하세요. **Fortify 사용은 필수가 아닙니다.** [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), [email verification](/docs/11.x/verification) 문서를 참고하여 Laravel 인증 기능을 직접 구현할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

앞서 언급했듯이, Laravel Fortify는 프론트엔드에 독립적인 Laravel용 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 Fortify를 반드시 사용해야 하는 것은 아닙니다.** 필요하면 [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), [email verification](/docs/11.x/verification) 문서를 참고해 직접 인증 기능을 구현할 수 있습니다.

Laravel에 익숙하지 않은 경우에는 Fortify를 사용하기 전에 [Laravel Breeze](/docs/11.x/starter-kits) 애플리케이션 스타터 킷을 먼저 살펴보는 것이 좋습니다. Laravel Breeze는 [Tailwind CSS](https://tailwindcss.com)로 구축된 사용자 인터페이스를 포함하는 인증 스캐폴딩을 제공합니다. Breeze는 라우트와 컨트롤러를 직접 애플리케이션 내에 게시하여 Laravel 인증 기능을 공부하고 익힐 수 있도록 도와줍니다.

Laravel Fortify는 본질적으로 Laravel Breeze의 라우트와 컨트롤러를 사용자 인터페이스 없이 패키지 형태로 제공하는 것입니다. 이를 통해 특정 프론트엔드 구현에 종속되지 않고도 애플리케이션 인증 백엔드 구현을 빠르게 구성할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 하나요?

Laravel Fortify를 언제 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 사용하는 경우라면 Fortify를 별도로 설치할 필요가 없습니다. 이미 스타터 킷에 완전한 인증 구현이 포함되어 있기 때문입니다.

애플리케이션 스타터 킷을 사용하지 않고 인증 기능이 필요한 경우에는 두 가지 선택지가 있습니다. 하나는 직접 인증 기능을 구현하는 것이고, 다른 하나는 Laravel Fortify를 설치해 인증 기능의 백엔드 구현을 제공받는 것입니다.

Fortify를 설치하면 제작한 UI가 이 문서에서 설명하는 Fortify의 인증 라우트에 요청을 보내어 사용자 인증과 회원가입을 진행할 수 있습니다.

직접 Laravel의 인증 서비스를 사용하고 싶다면, Fortify를 사용하지 않고도 [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), [email verification](/docs/11.x/verification) 문서를 따라 구현하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

일부 개발자는 [Laravel Sanctum](/docs/11.x/sanctum)과 Laravel Fortify의 차이를 혼동할 수 있습니다. 두 패키지는 서로 다른 문제를 다루기에 서로 상반되거나 경쟁하는 패키지가 아닙니다.

Laravel Sanctum은 API 토큰 관리와 이미 존재하는 사용자의 세션 쿠키 또는 토큰을 활용한 인증에만 집중합니다. Sanctum은 사용자 등록, 비밀번호 재설정 같은 라우트를 제공하지 않습니다.

만약 API를 제공하거나 싱글 페이지 애플리케이션의 백엔드 역할을 하는 인증 계층을 직접 구축한다면 Laravel Fortify(사용자 등록, 비밀번호 재설정 등)와 Laravel Sanctum(API 토큰 관리, 세션 인증)을 함께 사용하는 것이 가능합니다.

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 관리자를 사용해 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로, `fortify:install` Artisan 명령어를 실행해 Fortify의 리소스를 발행합니다:

```shell
php artisan fortify:install
```

이 명령어는 `app/Actions` 디렉토리에 Fortify의 액션들을 발행하는데, 해당 디렉토리가 없다면 생성됩니다. 또한 `FortifyServiceProvider`, 구성 파일, 필요한 데이터베이스 마이그레이션도 함께 발행됩니다.

그 후, 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 구성 파일은 `features`라는 설정 배열을 포함하고 있습니다. 이 배열은 Fortify가 기본으로 노출할 백엔드 라우트 및 기능들을 정의합니다. [Laravel Jetstream](https://jetstream.laravel.com)과 함께 Fortify를 사용하지 않는 경우, 대부분의 Laravel 애플리케이션에서 기본 인증 기능으로 제공하는 다음 기능만 활성화할 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면 또는 회원가입 화면 같은 뷰를 반환하도록 라우트를 정의합니다. 하지만 자바스크립트 기반 싱글 페이지 애플리케이션을 구축하는 경우 이런 라우트가 필요 없을 수 있습니다. 이런 상황에서는 애플리케이션의 `config/fortify.php` 구성 파일 내 `views` 설정 값을 `false`로 지정해 해당 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화 시 비밀번호 재설정

Fortify 뷰를 비활성화하면서 비밀번호 재설정 기능을 구현한다면, 여전히 애플리케이션의 "비밀번호 재설정" 뷰를 표시할 책임이 있는 `password.reset`라는 이름의 라우트를 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림 클래스가 비밀번호 재설정 URL을 해당 네임드 라우트를 통해 생성하기 때문에 필요합니다.

<a name="authentication"></a>
## 인증

먼저, Fortify에게 "로그인" 뷰를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리임을 기억하세요. 이미 완성된 Laravel 인증 기능의 프론트엔드 구현을 원한다면 [애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 사용하는 것이 좋습니다.

인증 뷰 렌더링 로직의 모든 부분은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 적절한 메서드로 커스터마이징할 수 있습니다. 보통 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다. Fortify는 `/login` 라우트를 정의해 이 뷰를 반환합니다:

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

로그인 템플릿에는 `/login`에 POST 요청을 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email` 또는 `username` 필드와 `password` 필드를 기대합니다. 이 email/username 필드의 이름은 `config/fortify.php` 설정 파일 내 `username` 값과 일치해야 합니다. 추가로 `remember`라는 부울 필드를 제공하면 Laravel이 제공하는 "remember me" 기능을 사용할지 여부를 나타낼 수 있습니다.

로그인 시도가 성공하면 Fortify는 애플리케이션 `fortify` 구성 파일 내 `home` 설정 옵션에 지정된 URI로 리디렉션합니다. 로그인 요청이 XHR이라면 HTTP 200 응답을 반환합니다.

성공하지 못하면 사용자는 로그인 화면으로 리디렉션되고, 유효성 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/11.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청이라면 HTTP 422 응답과 함께 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 제공받은 자격 증명과 애플리케이션에 설정된 인증 가드를 기반으로 자동으로 사용자를 조회하고 인증합니다. 하지만 가끔 로그인 자격 증명을 검증하는 방식과 사용자 조회를 완전히 커스터마이징하고 싶을 수 있습니다. Fortify는 `Fortify::authenticateUsing` 메서드로 이를 쉽게 구현할 수 있도록 지원합니다.

이 메서드는 HTTP 요청 인스턴스를 인자로 받는 클로저를 인수로 받습니다. 클로저 내에서 로그인 자격 증명을 검증하고, 관련된 사용자 인스턴스를 반환해야 합니다. 자격 증명이 유효하지 않거나 사용자가 없으면 `null` 또는 `false`를 반환해야 합니다. 보통 이 메서드는 `FortifyServiceProvider`의 `boot` 메서드 내에서 호출합니다:

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

Fortify가 사용할 인증 가드는 애플리케이션의 `fortify` 구성 파일 내에서 커스터마이징할 수 있습니다. 단, 설정하는 가드는 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스를 구현해야 합니다. 싱글 페이지 애플리케이션(SPA)을 인증하는 데 Fortify를 사용한다면 Laravel 기본 `web` 가드를 [Laravel Sanctum](https://laravel.com/docs/sanctum)과 함께 사용하는 것이 권장됩니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 여러 인보커블(invokable) 클래스의 파이프라인을 거쳐 인증합니다. 원한다면 로그인 요청을 처리하기 위한 커스텀 파이프라인을 정의할 수 있습니다. 각 클래스는 `__invoke` 메서드를 가지며, 이 메서드는 HTTP 요청 인스턴스와 다음 클래스로 요청을 전달하는 `$next` 변수를 인자로 받습니다. 이는 [미들웨어](/docs/11.x/middleware)와 유사한 동작입니다.

커스텀 파이프라인은 `Fortify::authenticateThrough` 메서드로 정의할 수 있습니다. 이 메서드는 로그인 요청 처리 클래스 배열을 반환하는 클로저를 인수로 받습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다.

아래 예시는 기본 파이프라인을 담고 있어 수정 시 시작점으로 활용할 수 있습니다:

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

#### 인증 시도 제한 (Authentication Throttling)

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어를 통해 인증 시도 제한 기능을 적용합니다. 이 미들웨어는 사용자 이름과 IP 주소 조합별로 인증 시도 수를 제한합니다.

응용프로그램에 따라서는 IP 주소만으로 제한하거나 다른 방식의 제한이 필요할 수 있습니다. 따라서 Fortify는 `fortify.limiters.login` 구성 옵션을 통해 사용자가 직접 [레이트 리미터(rate limiter)](/docs/11.x/routing#rate-limiting)를 지정하도록 허용합니다. 이 설정은 애플리케이션의 `config/fortify.php` 구성 파일에 위치합니다.

> [!NOTE]  
> 인증 시도 제한, [이중 인증](/docs/11.x/fortify#two-factor-authentication), 외부 웹 방화벽(WAF)을 혼합하여 활용하는 것이 가장 강력한 보안 방어책이 됩니다.

<a name="customizing-authentication-redirects"></a>
### 리디렉션 커스터마이징

로그인 시도가 성공하면 Fortify는 애플리케이션 `fortify` 구성 파일 내 `home` 설정 옵션에서 지정한 URI로 리디렉션합니다. 로그인 요청이 XHR인 경우에는 HTTP 200 응답을 반환합니다. 사용자가 로그아웃하면 루트 URI(`/`)로 리디렉션됩니다.

이 동작을 고급으로 커스터마이징해야 한다면, `LoginResponse` 및 `LogoutResponse` 계약(contract)의 구현체를 Laravel [서비스 컨테이너](/docs/11.x/container)에 바인딩할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드 내에서 처리합니다:

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
## 이중 인증 (Two Factor Authentication)

Fortify의 이중 인증 기능이 활성화되면 사용자는 인증과정에서 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 Google Authenticator 같은 TOTP(Time-based One-Time Password) 호환 모바일 인증 앱에서 받고 생성할 수 있습니다.

우선, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하는지 확인해야 합니다:

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

다음으로, 사용자가 이중 인증 설정을 관리할 수 있는 화면을 애플리케이션에 구현하세요. 이 화면에서는 이중 인증 활성화 및 비활성화, 재생성 가능한 복구 코드 재발급 기능을 포함해야 합니다.

> 기본적으로 `fortify` 구성 파일의 `features` 배열에 있는 이중 인증 설정은 변경 시 비밀번호 확인을 요구하도록 합니다. 따라서 애플리케이션에 Fortify의 [비밀번호 확인](#password-confirmation) 기능이 구현되어 있어야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화

이중 인증 활성화를 시작하려면 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 요청이 성공하면 사용자는 이전 URL로 리디렉션되고, 세션 변수 `status`가 `two-factor-authentication-enabled`으로 설정됩니다. 템플릿 내에서 이 `status` 값을 감지해 적절한 성공 메시지를 표시할 수 있습니다. XHR 요청의 경우 HTTP 200 응답을 반환합니다.

이중 인증 활성화를 선택한 후에는 사용자가 유효한 이중 인증 코드를 제출해 이중 인증 구성을 "확인"해야 합니다. 따라서 "성공" 메시지에는 이중 인증 구성을 완료해야 한다는 안내문이 포함되어야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two factor authentication below.
    </div>
@endif
```

다음으로, 사용자가 인증 앱에 스캔할 수 있도록 이중 인증 QR 코드를 표시해야 합니다. Blade를 사용한 프론트엔드라면, 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 QR 코드 SVG를 가져올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 기반 프론트엔드인 경우, `/user/two-factor-qr-code` 엔드포인트로 XHR GET 요청을 보내 사용자의 이중 인증 QR 코드를 JSON(`svg` 키 포함) 형태로 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인

이중 인증 QR 코드를 표시하는 것 외에, 사용자가 올바른 인증 코드를 제출하여 이중 인증 구성을 "확인"할 수 있게 해야 합니다. 이 코드는 Fortify가 정의한 `/user/confirmed-two-factor-authentication` 엔드포인트에 POST 요청으로 전송됩니다.

요청이 성공하면 사용자는 이전 URL로 리디렉션되고, 세션 변수 `status`가 `two-factor-authentication-confirmed`로 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two factor authentication confirmed and enabled successfully.
    </div>
@endif
```

XHR 요청의 경우 HTTP 200 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

복구 코드는 모바일 기기 분실 시 사용자가 인증할 수 있는 코드입니다. Blade 기반 프론트엔드라면 인증된 사용자 인스턴스에서 다음과 같이 복구 코드를 조회할 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프론트엔드에서는 `/user/two-factor-recovery-codes` 엔드포인트에 XHR GET 요청을 보내 복구 코드 배열을 JSON으로 받을 수 있습니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

인증 과정에서 Fortify는 자동으로 사용자를 애플리케이션의 이중 인증 챌린지 화면으로 리디렉션합니다. 그러나 로그인 요청이 XHR인 경우, 성공 응답에 `two_factor` 부울 속성이 포함된 JSON 객체가 포함됩니다. 이 값을 확인해 앱 내에서 이중 인증 챌린지 화면으로 리디렉션할지 결정할 수 있습니다.

이중 인증 기능 구현을 위해 Fortify에게 이중 인증 챌린지 뷰를 반환하는 방법을 알려야 합니다. Fortify의 모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 커스터마이징할 수 있습니다. 보통은 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

Fortify는 `/two-factor-challenge` 라우트를 정의해 이 뷰를 반환합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge` 엔드포인트에 POST 요청을 보내는 폼이 포함되어야 하며, 이 엔드포인트는 유효한 TOTP 토큰을 담는 `code` 필드 또는 복구 코드 중 하나를 담는 `recovery_code` 필드를 기대합니다.

로그인 시도가 성공하면 Fortify는 애플리케이션 `fortify` 구성 파일 내 `home` 옵션에 지정된 URI로 리디렉션합니다. 로그인 요청이 XHR인 경우 HTTP 204 응답이 반환됩니다.

실패하면 사용자는 이중 인증 챌린지 화면으로 다시 리디렉션되고, 유효성 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/11.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청의 경우 HTTP 422 응답과 함께 오류가 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화

이중 인증 비활성화를 위해서는 애플리케이션에서 Fortify의 `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내야 합니다. Fortify의 이중 인증 관련 엔드포인트들은 호출 전에 [비밀번호 확인](#password-confirmation) 과정을 요구합니다.

<a name="registration"></a>
## 회원가입

애플리케이션의 회원가입 기능을 구현할 때 Fortify에게 "회원가입" 뷰를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리이므로, 완성된 프론트엔드 구현이 필요하면 [애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 사용하는 것을 권장합니다.

Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 커스터마이징할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

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

Fortify는 `/register` 라우트를 정의해 이 뷰를 반환합니다. 회원가입 템플릿에는 Fortify가 정의한 `/register` 엔드포인트에 POST 요청을 보내는 폼이 포함되어야 합니다.

`/register` 엔드포인트는 문자열 `name`, 문자열 이메일/사용자 이름, `password`, `password_confirmation` 필드를 기대합니다. email/username 필드 이름은 애플리케이션 `fortify` 구성 파일 내 `username` 설정값과 일치해야 합니다.

회원가입이 성공하면 Fortify는 애플리케이션 `fortify` 구성 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청이라면 HTTP 201 응답을 반환합니다.

실패하면 회원가입 화면으로 다시 리디렉션되고, 유효성 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/11.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청 시에는 HTTP 422 응답과 함께 오류가 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

사용자 검증 및 생성 과정은 Laravel Fortify 설치 시 자동 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정해 변경할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청하기

비밀번호 재설정 기능 구현을 시작하려면 Fortify에게 "비밀번호 찾기" 뷰를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리이니 완성된 프론트엔드가 필요하다면 [애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 사용하는 게 좋습니다.

Fortify 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

Fortify는 `/forgot-password` 엔드포인트를 정의해 이 뷰를 반환합니다. `forgot-password` 템플릿에는 `/forgot-password` 엔드포인트에 POST 요청을 보내는 폼이 포함되어야 합니다.

`/forgot-password` 엔드포인트는 문자열 타입의 `email` 필드를 기대합니다. 필드명과 데이터베이스 컬럼명은 애플리케이션 `fortify` 구성 파일 내 `email` 설정과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면 Fortify는 `/forgot-password` 엔드포인트로 사용자를 리디렉션하고, 안전한 비밀번호 재설정 링크를 담은 이메일을 사용자에게 전송합니다. XHR 요청인 경우 HTTP 200 응답을 반환합니다.

성공 후 `/forgot-password`로 리디렉션되면 `status` 세션 변수를 사용해 비밀번호 재설정 링크 요청 결과 상태를 표시할 수 있습니다.

`$status` 세션 변수에는 애플리케이션 `passwords` [언어 파일](/docs/11.x/localization)에 정의된 번역 문자열 중 하나가 들어갑니다. Laravel 언어 파일을 게시하지 않았다면 `lang:publish` Artisan 명령어로 게시하여 수정할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패한 경우 사용자는 비밀번호 재설정 링크 요청 화면으로 리디렉션되며, 유효성 검사 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/11.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청 시에는 HTTP 422 응답과 함께 오류가 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 처리하기

비밀번호 재설정 기능 구현을 완료하려면 Fortify에게 "비밀번호 재설정" 뷰를 반환하는 방법을 알려야 합니다.

Fortify 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

Fortify는 이 뷰를 반환하는 라우트를 자동으로 정의합니다. `reset-password` 템플릿에는 `/reset-password`에 POST 요청을 보내는 폼이 포함되어야 합니다.

`/reset-password` 엔드포인트는 문자열 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 필드 `token` (값은 `request()->route('token')`)을 기대합니다. 이메일 필드명과 데이터베이스 컬럼명은 애플리케이션 `fortify` 구성 파일의 `email` 설정과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 사용자가 새 비밀번호로 로그인하도록 `/login` 라우트로 리디렉션합니다. 추가로 `status` 세션 변수를 설정해 로그인 화면에서 성공 메시지를 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청이라면 HTTP 200 응답이 반환됩니다.

실패 시 사용자는 비밀번호 재설정 화면으로 리디렉션되고, 유효성 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/11.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청의 경우 HTTP 422 응답과 함께 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 프로세스는 Laravel Fortify 설치 시 자동 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자가 계속 애플리케이션에 접근하기 전에 이메일 주소를 인증하도록 요구할 수 있습니다. 시작하려면 `fortify` 구성 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그리고 애플리케이션의 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하는지 확인합니다.

이 두 설정이 완료되면, 새로 가입한 사용자에게 이메일 주소 소유를 확인하는 이메일이 전송됩니다. 하지만 Fortify에게 이메일 인증 화면을 어떻게 표시할지 알려야 합니다.

Fortify의 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

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

Fortify는 Laravel 내장된 `verified` 미들웨어가 `/email/verify` 엔드포인트로 리디렉션할 때 사용하는 라우트를 정의합니다.

`verify-email` 템플릿에는 사용자가 이메일로 받은 인증 링크를 클릭하도록 안내하는 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

필요하다면, 애플리케이션의 `verify-email` 템플릿에 버튼을 추가해 `/email/verification-notification` 엔드포인트로 POST 요청을 발생시킬 수 있습니다. 이 엔드포인트는 새 인증 링크를 사용자에게 이메일로 전송합니다. 사용자가 이전 인증 메일을 삭제하거나 분실했을 때 유용합니다.

인증 링크 재전송 요청이 성공하면 Fortify는 `/email/verify` 엔드포인트로 리디렉션하고, `status` 세션 변수를 설정합니다. 이를 통해 성공 메시지를 사용자에게 알릴 수 있습니다. XHR 요청 시 HTTP 202 응답을 반환합니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기

특정 라우트 또는 라우트 그룹이 인증된 사용자 중 이메일 인증을 완료한 사용자만 접근하도록 하려면 Laravel 내장 `verified` 미들웨어를 라우트에 붙이면 됩니다. `verified` 미들웨어는 Laravel에서 기본으로 등록된 별칭(alias)이며, 실제로는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션 개발 중 특정 작업을 수행하기 전에 사용자가 비밀번호를 다시 한번 확인하도록 요구해야 할 때가 있습니다. 보통 이런 라우트는 Laravel 내장 `password.confirm` 미들웨어로 보호합니다.

비밀번호 확인 기능을 구현하려면 Fortify에게 "비밀번호 확인" 뷰를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리임을 기억하세요. 완성된 프론트엔드가 필요하면 [애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 이용하세요.

모든 Fortify 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

Fortify는 `/user/confirm-password` 엔드포인트를 정의하고 이 뷰를 반환합니다. `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트에 POST 요청을 보내는 폼이 포함되어야 하며, `password` 필드에는 사용자의 현재 비밀번호가 담겨야 합니다.

비밀번호가 현재 비밀번호와 일치하면 Fortify는 사용자가 접근하려던 라우트로 리디렉션합니다. XHR 요청이라면 HTTP 201 응답이 반환됩니다.

실패 시 사용자는 비밀번호 확인 화면으로 리디렉션되고, 유효성 오류는 공유된 `$errors` Blade 템플릿 변수로 확인 가능합니다. XHR 요청에서는 HTTP 422 응답과 함께 오류가 전달됩니다.