# Laravel Fortify

- [소개](#introduction)
    - [Fortify란 무엇인가?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 서비스 프로바이더](#the-fortify-service-provider)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화하기](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 맞춤화하기](#customizing-user-authentication)
    - [인증 파이프라인 맞춤화하기](#customizing-the-authentication-pipeline)
    - [리다이렉트 맞춤화하기](#customizing-authentication-redirects)
- [이중 인증](#two-factor-authentication)
    - [이중 인증 활성화하기](#enabling-two-factor-authentication)
    - [이중 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [이중 인증 비활성화하기](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 맞춤화하기](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청하기](#requesting-a-password-reset-link)
    - [비밀번호 재설정하기](#resetting-the-password)
    - [비밀번호 재설정 맞춤화하기](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호하기](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프런트엔드 독립형 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후 `route:list` Artisan 명령어를 실행하면 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않기 때문에, 등록한 라우트에 요청을 보내는 여러분만의 UI와 함께 사용하도록 설계되었습니다. 이 문서 후반부에서 이러한 라우트에 어떻게 요청하는지 구체적으로 다루겠습니다.

> [!NOTE]
> Fortify는 Laravel의 인증 기능 구현을 빠르게 시작할 수 있도록 돕는 패키지임을 기억하세요. **사용이 반드시 강제되는 것은 아닙니다.** 언제든지 Laravel의 [인증](/docs/9.x/authentication), [비밀번호 재설정](/docs/9.x/passwords), [이메일 인증](/docs/9.x/verification) 문서를 참고하여 직접 Laravel 인증 서비스를 사용할 수 있습니다.

<a name="what-is-fortify"></a>
### Fortify란 무엇인가?

앞서 언급했듯이, Laravel Fortify는 Laravel을 위한 프런트엔드 독립형 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 위한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** 언제든지 Laravel의 [인증](/docs/9.x/authentication), [비밀번호 재설정](/docs/9.x/passwords), [이메일 인증](/docs/9.x/verification) 문서를 따라 수동으로 인증 서비스를 구현할 수 있습니다.

Laravel에 익숙하지 않다면, Fortify 사용 전에 [Laravel Breeze](/docs/9.x/starter-kits) 애플리케이션 스타터 킷을 살펴보는 것이 좋습니다. Laravel Breeze는 [Tailwind CSS](https://tailwindcss.com)로 만든 UI가 포함된 인증 스캐폴딩을 제공합니다. Breeze는 라우트와 컨트롤러를 직접 애플리케이션에 퍼블리시하여 Laravel의 인증 기능을 이해하고 익히는 데 도움이 됩니다. 그 후에 Fortify를 사용해도 좋습니다.

Laravel Fortify는 기본적으로 Laravel Breeze의 라우트와 컨트롤러를 사용자 인터페이스 없이 패키지 형태로 제공하는 역할을 합니다. 덕분에 특정 프런트엔드 구현에 종속되지 않고도 애플리케이션 인증 백엔드를 빠르게 구현할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나?

Laravel Fortify를 언제 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 사용 중이라면 Fortify를 별도로 설치할 필요가 없습니다. 스타터 킷에는 이미 인증 기능이 완전하게 구현되어 있기 때문입니다.

스타터 킷을 사용하지 않고 인증 기능이 필요한 애플리케이션을 만든다면, 인증 기능을 직접 구현하거나 Laravel Fortify를 사용해 백엔드 인증 기능을 편리하게 구현하는 두 가지 선택지가 있습니다.

Fortify를 선택하면, 여러분의 UI가 Fortify가 제공하는 인증 라우트에 요청을 보내 사용자 인증과 회원가입 기능을 처리합니다.

직접 Laravel 인증 서비스를 구현하려면 [인증](/docs/9.x/authentication), [비밀번호 재설정](/docs/9.x/passwords), [이메일 인증](/docs/9.x/verification) 문서를 참고하세요.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify & Laravel Sanctum

Laravel Sanctum과 Laravel Fortify의 차이를 혼동하는 개발자가 많습니다. 두 패키지가 서로 연관되었지만 다른 문제를 해결하기 때문에, Fortify와 Sanctum은 상호 배타적이거나 경쟁하는 패키지가 아닙니다.

Laravel Sanctum은 API 토큰 관리와 세션 쿠키 또는 토큰을 이용한 기존 사용자 인증에만 집중합니다. 사용자 회원가입, 비밀번호 재설정 등 관련 라우트는 제공하지 않습니다.

API 백엔드 역할을 하거나 SPA(single-page application)를 위한 인증 레이어를 직접 구축할 때 Laravel Fortify(회원가입, 비밀번호 재설정 등)와 Laravel Sanctum(API 토큰 관리, 세션 인증)을 함께 사용하는 것이 일반적입니다.

<a name="installation"></a>
## 설치

시작하려면, Composer 패키지 매니저로 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로, `vendor:publish` 명령어를 사용해 Fortify 자원을 퍼블리시합니다:

```shell
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

이 명령은 Fortify의 액션을 `app/Actions` 디렉토리에 퍼블리시합니다. 해당 디렉토리가 없으면 새로 생성됩니다. 또한 `FortifyServiceProvider` 클래스, 설정 파일, 필요한 데이터베이스 마이그레이션도 함께 퍼블리시됩니다.

마지막으로 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify 서비스 프로바이더

위의 `vendor:publish` 명령은 `App\Providers\FortifyServiceProvider` 클래스도 퍼블리시합니다. 이 클래스가 애플리케이션의 `config/app.php` 설정 파일 내의 `providers` 배열에 등록되어 있는지 확인하세요.

Fortify 서비스 프로바이더는 Fortify가 퍼블리시한 액션을 등록하고, Fortify가 각 작업을 실행할 때 이 액션들을 사용하도록 지시합니다.

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에는 `features` 설정 배열이 있습니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 라우트 및 기능을 정의합니다. [Laravel Jetstream](https://jetstream.laravel.com)과 함께 Fortify를 사용하지 않는 경우, 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능만 활성화하는 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화하기

기본적으로 Fortify는 로그인 화면이나 회원가입 화면과 같은 뷰를 반환하는 라우트를 정의합니다. 하지만 자바스크립트 기반 SPA를 만든다면 이러한 라우트가 필요 없을 수 있습니다. 이런 경우 애플리케이션의 `config/fortify.php` 설정 파일 내 `views` 값을 `false`로 설정하여 뷰 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화와 비밀번호 재설정

Fortify의 뷰를 비활성화하고 비밀번호 재설정 기능을 구현할 경우, 여전히 `password.reset`라는 이름을 가진 라우트를 설정해야 합니다. 이 라우트는 애플리케이션의 "비밀번호 재설정" 뷰를 표시하도록 책임집니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 `password.reset` 이름의 라우트를 통해 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

시작하려면, Fortify가 우리의 "로그인" 뷰를 반환하는 방식을 정의해야 합니다. Fortify는 템플릿이나 UI를 제공하지 않는 헤드리스 인증 라이브러리임을 기억하세요. 이미 완성된 인증 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 사용하세요.

인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 적절한 메서드를 사용해 모두 맞춤 설정할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다. Fortify가 `/login` 라우트를 정의하고 이 뷰를 반환하도록 처리합니다:

```
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

로그인 템플릿에는 POST 요청을 `/login`으로 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 `email`/`username` 및 `password`를 기대합니다. `email` 또는 `username` 필드명은 애플리케이션의 `config/fortify.php` 설정 파일 내 `username` 값과 일치해야 합니다. 또한 Boolean 타입 `remember` 필드를 포함할 수 있으며, 이는 Laravel의 "remember me" 기능을 사용하려는 지 여부를 의미합니다.

로그인이 성공하면 Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 옵션에 설정된 URI로 리다이렉트합니다. 로그인 요청이 XHR이면 200 HTTP 응답을 반환합니다.

요청이 실패하면 사용자는 로그인 화면으로 다시 리다이렉트되고, 유효성 검사 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/9.x/validation#quick-displaying-the-validation-errors)를 통해 사용할 수 있습니다. 또는 XHR 요청이라면 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 맞춤화하기

Fortify는 제공받은 인증 정보와 애플리케이션에 설정된 인증 가드를 사용해 자동으로 사용자를 조회하고 인증합니다. 그러나 로그인 인증 방법과 사용자 조회 과정을 완전히 직접 제어하고 싶은 경우가 있을 수 있습니다. Fortify는 `Fortify::authenticateUsing` 메서드를 제공하여 이를 쉽게 지원합니다.

이 메서드는 HTTP 요청을 받는 클로저를 인수로 받습니다. 클로저는 로그인 인증 정보를 검증하고, 관련 사용자 인스턴스를 반환해야 합니다. 인증 정보가 올바르지 않거나 사용자가 없으면 `null` 또는 `false`를 반환해야 합니다. 보통 `FortifyServiceProvider`의 `boot` 메서드 내에서 호출합니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
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

애플리케이션의 `fortify` 설정 파일 내에서 Fortify가 사용하는 인증 가드를 맞춤 설정할 수 있습니다. 단, 설정하는 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 구현체여야 합니다. SPA 인증에 Laravel Fortify를 사용할 경우, Laravel 기본 `web` 가드를 [Laravel Sanctum](https://laravel.com/docs/sanctum)과 함께 사용하는 것이 권장됩니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 맞춤화하기

Laravel Fortify는 호출 가능 클래스(invokable classes)를 연결해 로그인 요청을 처리하는 파이프라인을 구현합니다. 필요하다면, 로그인 요청이 통과해야 하는 클래스 배열을 직접 정의할 수 있습니다. 각 클래스는 `Illuminate\Http\Request` 인스턴스와, 요청을 다음 클래스로 넘길 때 호출하는 `$next` 인수가 있는 `__invoke` 메서드를 가져야 합니다. [미들웨어](/docs/9.x/middleware)와 유사합니다.

사용자 정의 파이프라인은 `Fortify::authenticateThrough` 메서드로 지정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다. 아래 예시는 기본 파이프라인 정의이며, 수정 시 출발점으로 사용할 수 있습니다:

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

<a name="customizing-authentication-redirects"></a>
### 리다이렉트 맞춤화하기

로그인이 성공하면 Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 설정값에 정의된 URI로 리다이렉트합니다. XHR 로그인 시에는 200 HTTP 응답을 반환합니다. 사용자가 로그아웃하면 `/` URI로 리다이렉트됩니다.

더 세밀한 동작 제어가 필요하다면, `LoginResponse` 및 `LogoutResponse` 계약 인터페이스 구현체를 Laravel [서비스 컨테이너](/docs/9.x/container)에 바인딩할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 내의 `register` 메서드에서 처리합니다:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
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

Fortify의 이중 인증 기능이 활성화되면, 인증 과정에서 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 시간 기반 일회용 비밀번호(TOTP)이며, Google Authenticator 같은 TOTP 호환 모바일 인증 앱에서 받을 수 있습니다.

먼저 애플리케이션의 `App\Models\User` 모델에서 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용 중인지 확인하세요:

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

다음으로, 사용자가 이중 인증 설정을 관리할 화면을 만들어야 합니다. 여기서는 이중 인증 활성화 및 비활성화, 복구 코드 재생성을 할 수 있어야 합니다.

> 기본값으로, `fortify` 설정 파일 내 `features` 배열은 이중 인증 설정 변경 시 비밀번호 확인을 요구하도록 Fortify에 지시합니다. 따라서, 계속 진행하기 전에 Fortify의 [비밀번호 확인](#password-confirmation) 기능도 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화하기

이중 인증을 활성화하려면 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트에 POST 요청을 보내야 합니다. 요청에 성공하면 이전 URL로 리다이렉트되고, 세션의 `status` 변수는 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 `status` 변수를 감지하여 적절한 성공 메시지를 표시할 수 있습니다. XHR 요청이었다면 200 HTTP 응답이 반환됩니다.

이중 인증 활성화 후에도 사용자는 유효한 이중 인증 코드를 제출해 설정을 "확인"해야 합니다. 따라서 성공 메시지는 이중 인증 확인이 아직 필요함을 안내해야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two factor authentication below.
    </div>
@endif
```

이후 사용자가 모바일 인증 앱에 스캔할 수 있도록 이중 인증 QR 코드를 보여야 합니다. Blade를 사용한다면 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드를 통해 QR 코드 SVG를 가져올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 기반 프런트엔드를 사용하는 경우, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보내 QR 코드를 JSON 객체 (`svg` 키 포함)로 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인

QR 코드를 보여주는 것 외에도, 사용자가 유효한 인증 코드를 입력할 수 있는 텍스트 입력란을 제공해야 하며, 이를 통해 이중 인증 설정을 "확인"하도록 해야 합니다. 이 코드는 Fortify가 제공하는 `/user/confirmed-two-factor-authentication` 엔드포인트에 POST 요청으로 보내야 합니다.

요청이 성공하면 이전 URL로 리다이렉트되고, 세션의 `status` 변수는 `two-factor-authentication-confirmed`로 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two factor authentication confirmed and enabled successfully.
    </div>
@endif
```

XHR 요청이면 200 HTTP 응답을 반환합니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시하기

사용자의 이중 인증 복구 코드도 보여주는 것이 좋습니다. 복구 코드는 모바일 기기에 접근하지 못할 때 인증에 사용되는 코드입니다. Blade를 사용한다면 인증된 사용자 인스턴스를 통해 복구 코드를 배열 형태로 얻을 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프런트엔드를 사용한다면, `/user/two-factor-recovery-codes` 엔드포인트에 XHR GET 요청을 보내서 사용자의 복구 코드 배열을 받을 수 있습니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

인증 과정에서 Fortify는 자동으로 사용자를 이중 인증 챌린지 화면으로 리다이렉트합니다. 단, 애플리케이션이 XHR 로그인 요청을 보내는 경우, 인증 성공 후 반환된 JSON 응답에 `two_factor` 불리언 속성이 포함됩니다. 이 값을 확인하여 이중 인증 챌린지 화면으로 리다이렉트할지 결정해야 합니다.

이중 인증 기능 구현을 시작하려면, Fortify에 이중 인증 챌린지 뷰를 반환하는 방법을 알려야 합니다. Fortify의 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드를 사용해 맞춤 설정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출됩니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify가 `/two-factor-challenge` 경로를 정의하고 이 뷰를 반환하도록 처리합니다. `two-factor-challenge` 템플릿에는 POST 요청을 `/two-factor-challenge` 엔드포인트로 보내는 폼이 있어야 합니다. 이 엔드포인트는 유효한 TOTP 토큰이 담긴 `code` 필드나 복구 코드 중 하나를 담은 `recovery_code` 필드를 기대합니다.

로그인이 성공하면 Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 옵션에 설정된 URI로 리다이렉트합니다. XHR 요청이라면 204 HTTP 응답을 반환합니다.

실패하면 다시 이중 인증 챌린지 화면으로 리다이렉트되고, 유효성 검사 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/9.x/validation#quick-displaying-the-validation-errors)를 통해 제공됩니다. XHR 요청이라면 422 HTTP 오류 응답이 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화하기

이중 인증을 비활성화하려면 애플리케이션에서 Fortify가 제공하는 `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내야 합니다. Fortify의 이중 인증 엔드포인트는 호출 전 [비밀번호 확인](#password-confirmation) 과정을 요구합니다.

<a name="registration"></a>
## 회원가입

회원가입 기능 구현을 시작하려면, Fortify가 "회원가입(register)" 뷰를 반환하는 법을 알려야 합니다. Fortify는 UI가 없는 헤드리스 인증 라이브러리임을 기억하세요. 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 사용하세요.

Fortify의 모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드들을 통해 맞춤 설정할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify가 `/register` 라우트를 정의하고 해당 뷰를 반환합니다. `register` 템플릿에는 POST 요청을 Fortify가 제공하는 `/register` 엔드포인트로 보내는 폼이 포함되어야 합니다.

`/register` 엔드포인트는 문자열 `name`, 이메일 주소 / 사용자 이름, `password`, `password_confirmation` 필드를 기대합니다. 이메일/사용자 이름 필드명은 애플리케이션 `fortify` 설정 파일 내 `username` 설정 값과 일치해야 합니다.

회원가입이 성공하면 Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청이면 201 HTTP 응답을 반환합니다.

실패하면 사용자에게 회원가입 화면으로 다시 리다이렉트되고, 유효성 검사 오류는 `$errors` [Blade 템플릿 변수](/docs/9.x/validation#quick-displaying-the-validation-errors)를 통해 제공됩니다. XHR 요청일 때는 422 HTTP 오류 응답이 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 맞춤화하기

사용자 유효성 검사와 생성 과정은 Laravel Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정하여 맞춤화할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청하기

비밀번호 재설정 기능 구현을 시작하려면, Fortify가 "비밀번호 분실" 뷰를 반환하는 방식을 알려야 합니다. Fortify는 UI를 제공하지 않는 헤드리스 인증 라이브러리임을 기억하세요. 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 사용하세요.

Fortify의 모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드들을 통해 맞춤화할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify가 `/forgot-password` 엔드포인트를 정의하고 뷰를 반환합니다. `forgot-password` 템플릿에는 POST 요청을 `/forgot-password`로 보내는 폼이 있어야 합니다.

`/forgot-password` 엔드포인트는 문자열 `email` 필드를 기대합니다. 이 필드명과 데이터베이스 칼럼명은 애플리케이션의 `fortify` 설정 파일 내 `email` 설정 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청에 성공하면, Fortify는 사용자를 `/forgot-password` 엔드포인트로 리다이렉트하고, 사용자에게 비밀번호 재설정 안전 링크가 포함된 이메일을 전송합니다. XHR 요청이면 200 HTTP 응답을 반환합니다.

성공한 요청 후 `/forgot-password`로 리다이렉트 된 후 `status` 세션 변수로 요청 상태를 표시할 수 있습니다. 이 세션 변수 값은 애플리케이션 `passwords` [언어 파일](/docs/9.x/localization)에 정의된 번역 문자열 중 하나와 일치합니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패하면 사용자를 비밀번호 재설정 링크 요청 화면으로 리다이렉트하며, `$errors` [Blade 템플릿 변수](/docs/9.x/validation#quick-displaying-the-validation-errors)에 유효성 검사 오류가 담깁니다. XHR 요청일 경우 422 HTTP 응답이 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정하기

비밀번호 재설정 기능 구현을 완료하려면 Fortify에 "비밀번호 재설정" 뷰 반환 방법을 알려야 합니다.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 맞춤 설정할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::resetPasswordView(function ($request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify가 해당 뷰를 반환하는 라우트를 정의합니다. `reset-password` 템플릿에는 POST 요청을 `/reset-password`로 보내는 폼이 포함되어야 합니다.

`/reset-password` 엔드포인트는 문자열 `email`, `password`, `password_confirmation` 필드와, 숨겨진 `token` 필드(값은 `request()->route('token')`)를 기대합니다. 이메일 필드명과 데이터베이스 칼럼명은 애플리케이션 `fortify` 설정 파일 내 `email` 설정 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 사용자를 `/login` 경로로 리다이렉트하여 새 비밀번호로 로그인하도록 안내합니다. 또한 로그인 화면에서 재설정 성공 상태를 표시할 수 있도록 `status` 세션 변수를 설정합니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청이라면 200 HTTP 응답을 반환합니다.

실패하면 사용자를 비밀번호 재설정 화면으로 리다이렉트하고, `$errors` [Blade 템플릿 변수](/docs/9.x/validation#quick-displaying-the-validation-errors)에 오류가 포함됩니다. XHR 요청 시 422 HTTP 응답이 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 맞춤화하기

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 맞춤화할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자에게 이메일 주소를 인증하도록 요구할 수 있습니다. 시작하려면 `fortify` 설정 파일의 `features` 배열 내 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 또한, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현했는지 확인해야 합니다.

위 두 단계를 완료하면, 새로 가입한 사용자에게 이메일 주소 소유 인증용 링크가 포함된 이메일이 전송됩니다. 그러나 Fortify에게 이메일 인증 화면을 어떻게 표현할지 알려야 합니다. 이 화면은 사용자가 이메일 내 인증 링크를 클릭하도록 안내합니다.

Fortify 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 맞춤 설정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify는 Laravel 내장 `verified` 미들웨어가 `/email/verify` 경로로 리다이렉트할 때 이 뷰를 반환하는 라우트를 정의합니다.

`verify-email` 템플릿에는 사용자에게 이메일 인증 링크를 클릭하라는 안내 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

필요하다면, `verify-email` 템플릿에 `/email/verification-notification`으로 POST 요청을 보내는 버튼을 추가할 수 있습니다. 이 요청에 성공하면 새 인증 링크 이메일이 사용자에게 발송됩니다(기존 링크를 잃어버렸을 경우 유용).

재전송 요청이 성공하면 Fortify가 `/email/verify`로 리다이렉트하며 `status` 세션 변수를 설정해, 성공 메시지를 사용자에게 보여줄 수 있습니다. XHR 요청일 경우 202 HTTP 응답을 반환합니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기

사용자가 이메일을 인증했는지 여부를 요구하려면 해당 라우트 또는 그룹에 Laravel 내장 `verified` 미들웨어를 붙여야 합니다. 이 미들웨어는 애플리케이션의 `App\Http\Kernel` 클래스에서 등록되어 있습니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 구축하는 동안, 때로 중요한 작업을 수행하기 전에 사용자가 비밀번호를 다시 확인하도록 요구해야 할 때가 있습니다. 보통 이 작업들을 Laravel 내장 `password.confirm` 미들웨어로 보호합니다.

비밀번호 확인 기능 구현을 시작하려면, Fortify가 애플리케이션의 "비밀번호 확인" 뷰를 반환하는 법을 정의해야 합니다. Fortify는 UI를 제공하지 않는 헤드리스 인증 라이브러리임을 기억하세요. 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 사용하세요.

Fortify 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스 내 메서드를 사용해 모두 맞춤 설정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify는 `/user/confirm-password` 엔드포인트를 정의하고 이 뷰를 반환하도록 처리합니다. `confirm-password` 템플릿에는 POST 요청을 `/user/confirm-password`로 보내는 폼이 포함되어야 합니다. 이 요청은 사용자 현재 비밀번호가 담긴 `password` 필드를 포함해야 합니다.

비밀번호가 올바르면 Fortify는 사용자가 접근하려던 라우트로 리다이렉트합니다. XHR 요청일 때는 201 HTTP 응답이 반환됩니다.

실패하면 사용자를 비밀번호 확인 화면으로 리다이렉트하며, 유효성 검사 오류가 `$errors` Blade 템플릿 변수를 통해 제공됩니다. XHR 요청인 경우 422 HTTP 응답이 반환됩니다.