# Laravel Fortify

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [Fortify를 언제 사용해야 할까?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리다이렉트 커스터마이징](#customizing-authentication-redirects)
- [이중 인증(2FA)](#two-factor-authentication)
    - [이중 인증 활성화](#enabling-two-factor-authentication)
    - [이중 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [이중 인증 비활성화](#disabling-two-factor-authentication)
- [회원 가입](#registration)
    - [회원 가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 프론트엔드에 종속되지 않는 라라벨 인증 백엔드 구현체입니다. Fortify는 로그인, 회원 가입, 비밀번호 재설정, 이메일 인증 등의 라라벨 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다. Fortify 설치 후, `route:list` 아티즌 명령어를 실행하면 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않으므로, Fortify가 등록한 라우트로 요청을 전송하는 여러분만의 UI와 결합해서 사용해야 합니다. 남은 문서에서 이러한 라우트로 요청을 보내는 방법을 자세히 다룹니다.

> [!NOTE]
> Fortify는 라라벨 인증 기능을 빠르게 구축할 수 있도록 도와주는 패키지입니다. **꼭 사용해야 하는 것은 아닙니다.** 언제든지 [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 공식 문서를 참고하여, 직접 라라벨 인증 기능을 구현할 수 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

앞서 언급했듯이, Laravel Fortify는 프론트엔드에 독립적인 라라벨 인증 백엔드 구현체입니다. 로그인, 회원 가입, 비밀번호 재설정, 이메일 인증 등 라라벨의 모든 인증 기능 구현을 위한 라우트 및 컨트롤러를 등록합니다.

**라라벨의 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** 언제든 [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고해 직접 인증 관련 서비스를 사용할 수 있습니다.

라라벨을 처음 접했다면, 먼저 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용해보길 권장합니다. 스타터 킷은 [Tailwind CSS](https://tailwindcss.com)로 구성된 인증 UI 스캐폴딩을 제공하여, Fortify를 직접 사용하기 전에 라라벨 인증 기능을 쉽게 익히고 경험할 수 있게 해줍니다.

Laravel Fortify는 애플리케이션 스타터 킷의 라우트와 컨트롤러를 UI 없이 단일 패키지 형태로 제공합니다. 이를 통해 백엔드 인증 레이어를 빠르게 구축할 수 있으며, 프론트엔드 구현 방식에 구애받지 않고 사용할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 할까?

언제 Laravel Fortify를 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용 중이라면 모든 인증 기능이 이미 구현되어 있으므로, Fortify를 추가로 설치할 필요가 없습니다.

스타터 킷을 사용하지 않으면서 앱에 인증 기능이 필요하다면, 두 가지 선택지가 있습니다:  
- 인증 기능을 수동으로 직접 구현하기  
- Fortify를 사용해 인증 백엔드를 빠르게 구축하기

Fortify를 설치하면 UI에서 Fortify가 등록한 라우트로 요청을 보내어 사용자 인증 및 등록을 처리할 수 있습니다.

반면, Fortify 없이 인증 기능을 직접 구현하고 싶다면, [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고할 수 있습니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

몇몇 개발자들은 [Laravel Sanctum](/docs/{{version}}/sanctum)과 Fortify의 차이점에 혼란을 느낍니다. 이 두 패키지는 서로 다른(하지만 연관된) 문제를 해결하므로, Fortify와 Sanctum은 상호 대체재가 아니며 동시에 사용할 수 있습니다.

Laravel Sanctum은 API 토큰 관리와 기존 사용자 세션 쿠키 또는 토큰 인증만을 다룹니다. 사용자 등록이나 비밀번호 재설정 등의 라우트는 제공하지 않습니다.

API를 제공하거나 SPA의 백엔드 역할을 하는 앱의 인증 레이어를 직접 구축하려면, 사용자 등록/비밀번호 재설정 등은 Fortify로 처리하고, API 토큰 관리/세션 인증 등은 Sanctum과 함께 사용할 수 있습니다.

<a name="installation"></a>
## 설치

Fortify 설치는 Composer 패키지 관리자를 사용하세요.

```shell
composer require laravel/fortify
```

다음으로 `fortify:install` 아티즌 명령어로 Fortify 리소스를 퍼블리시하세요.

```shell
php artisan fortify:install
```

이 명령은 `app/Actions` 디렉터리에 Fortify 동작 파일을 생성하고(디렉터리가 없으면 생성), `FortifyServiceProvider`, 설정 파일, 필요한 데이터베이스 마이그레이션도 함께 퍼블리시합니다.

그리고 데이터베이스 이주를 실행하세요.

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에 있는 `features` 배열은, Fortify가 기본적으로 노출할 백엔드 라우트 및 기능들을 정의합니다. 다음 기능들은 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능이므로, 아래처럼 필요한 기능만 활성화할 것을 권장합니다.

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

Fortify는 기본적으로 로그인/회원 가입 화면 등 뷰 반환을 위한 라우트를 정의합니다. 그러나 JavaScript 기반의 SPA 등에서는 이런 라우트가 필요하지 않을 수 있습니다. 이런 경우, `config/fortify.php`에서 `views` 값을 `false`로 설정해 뷰 라우트를 비활성화할 수 있습니다.

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰, 비밀번호 재설정 연결 비활성화

Fortify 뷰를 비활성화해도 비밀번호 재설정 기능을 직접 구현한다면, 반드시 "비밀번호 재설정" 뷰를 표시하는 `password.reset` 이름의 라우트를 등록해야 합니다. 이는 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 `password.reset` 네임드 라우트를 통해 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

우선 Fortify에 "로그인" 화면을 반환하는 방법을 알려야 합니다. Fortify는 UI를 제공하지 않는 헤드리스 인증 라이브러리입니다. 이미 구현된 인증 기능의 프론트엔드가 필요하다면, [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하세요.

모든 인증 뷰의 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 사용해 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다. Fortify는 이 뷰를 반환하는 `/login` 라우트를 등록해줍니다.

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

로그인 템플릿에는 `/login`에 POST 요청을 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 `email` 또는 `username`과 `password`를 기대합니다. 이메일/유저네임 필드명은 `config/fortify.php`의 `username` 설정값과 일치해야 합니다. 또한 "로그인 유지" 기능을 위한 불리언 `remember` 필드도 사용할 수 있습니다.

로그인 성공 시, Fortify는 `fortify` 설정 파일의 `home` 옵션에 명시된 URI로 리다이렉트합니다. XHR 요청이라면 200 HTTP 응답을 반환합니다.

로그인 실패 시, 사용자는 로그인 화면으로 다시 리다이렉트되고 검증 오류 메시지가 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 제공됩니다. XHR 요청의 경우, 422 HTTP 응답과 함께 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격 증명과 설정된 인증 가드를 통해 사용자를 자동으로 인증합니다. 그러나 필요하다면 로그인 자격 증명 검증 및 사용자 조회 방식을 자유롭게 정의할 수 있습니다. 이를 위해 Fortify의 `Fortify::authenticateUsing` 메서드를 사용할 수 있습니다.

이 콜백은 HTTP 요청을 받아 검증을 수행하고 성공 시 사용자 인스턴스를 반환해야 합니다. 인증 실패나 사용자를 찾지 못하면 `null` 또는 `false`를 반환하면 됩니다. 주로 `FortifyServiceProvider`의 `boot` 메서드에 정의합니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

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

Fortify가 사용할 인증 가드는 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 단, 설정한 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard`를 구현해야 합니다. SPA 인증에 Fortify를 사용할 경우, 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 같이 사용하는 것이 권장됩니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 인증 요청을 일련의 호출 가능한 클래스로 구성된 파이프라인으로 처리합니다. 원한다면, 로그인 요청이 거칠 커스텀 파이프라인을 정의할 수 있습니다. 각 클래스에는 `__invoke` 메서드가 존재해야 하며, [미들웨어](/docs/{{version}}/middleware)처럼 `$next` 변수로 다음 클래스로 요청을 넘길 수 있습니다.

커스텀 파이프라인은 `Fortify::authenticateThrough` 메서드를 사용해 등록하며, 이는 클래스를 배열로 반환하는 콜백을 받습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot`에서 정의합니다.

다음은 기본 파이프라인 예시로, 필요에 따라 수정해 사용할 수 있습니다:

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

#### 인증 시도 제한(Throttling)

Fortify는 기본적으로 `EnsureLoginIsNotThrottled` 미들웨어로 로그인 시도 횟수를 제한합니다. 이 미들웨어는 사용자명과 IP 주소 조합별로 제한합니다.

일부 앱은 IP 기준 제한 등 다른 정책이 필요할 수 있는데, 이럴 경우 `fortify.limiters.login` 설정을 통해 커스텀 [속도 제한기](/docs/{{version}}/routing#rate-limiting)를 지정할 수 있습니다. 해당 옵션은 `config/fortify.php`에 위치합니다.

> [!NOTE]
> 인증 시도 제한, [이중 인증](/docs/{{version}}/fortify#two-factor-authentication), 외부 웹 방화벽(WAF) 등과 조합해 보안을 극대화할 수 있습니다.

<a name="customizing-authentication-redirects"></a>
### 리다이렉트 커스터마이징

로그인 성공 시 Fortify는 `fortify` 설정의 `home` 옵션에 명시한 URI로 리다이렉트하고, XHR 요청일 경우 200 응답을 반환합니다. 로그아웃 후에는 `/` URI로 리다이렉트됩니다.

이 동작을 더욱 세분화하려면, `LoginResponse` 및 `LogoutResponse` 계약을 [서비스 컨테이너](/docs/{{version}}/container)에 구현체로 바인딩할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `register` 메서드에서 진행합니다.

```php
use Laravel\Fortify\Contracts\LogoutResponse;

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
## 이중 인증(2FA)

Fortify의 이중 인증(2FA) 기능을 활성화하면, 사용자는 로그인시 6자리 토큰을 추가로 입력해야 합니다. 이 토큰은 Google Authenticator와 같은 TOTP 호환 모바일 인증 앱에서 생성합니다.

먼저 `App\Models\User` 모델에 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 추가하세요:

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

다음으로 사용자가 이중 인증을 관리할 수 있는 화면을 구현해야 합니다. 이 화면에서는 이중 인증 활성화/비활성화, 복구 코드 재생성이 가능해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에서 이중 인증 설정 변경 시 비밀번호 재확인을 요구합니다. 따라서 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화

이중 인증을 활성화하려면, Fortify에서 정의한 `/user/two-factor-authentication` 엔드포인트에 POST 요청을 보내면 됩니다. 성공 시 이전 URL로 리다이렉트되고, 세션에 `status` 값이 `two-factor-authentication-enabled`로 저장됩니다. 템플릿에서 해당 상태값을 확인해 성공 메시지를 표시할 수 있습니다. XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

사용자가 이중 인증을 활성화했더라도, 실제 사용 전 유효한 인증 코드를 입력해 "확인(confirmation)"을 마쳐야 합니다. 따라서 성공 메시지에서 확인 절차가 필요하다는 안내를 해야 합니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 이중 인증 설정을 마무리해 주세요.
    </div>
@endif
```

그리고 사용자의 인증 앱에서 스캔할 QR코드를 보여주어야 합니다. Blade를 사용하는 경우, 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 SVG를 가져올 수 있습니다.

```php
$request->user()->twoFactorQrCodeSvg();
```

JavaScript 프론트엔드를 구축하는 경우, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 통해 `svg` 키가 포함된 QR코드를 JSON으로 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인

QR코드를 보여주는 것 외에도, 사용자가 인증 코드를 입력해 이중 인증을 "확인"할 수 있는 입력란을 제공해야 합니다. 인증 코드는 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청하여 앱으로 전달해야 합니다.

성공 시, 이전 URL로 리다이렉트되고 세션에 `status`가 `two-factor-authentication-confirmed`로 설정됩니다.

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        이중 인증이 확인되고 성공적으로 활성화되었습니다.
    </div>
@endif
```

XHR 요청일 경우에도 200 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

이중 인증 복구 코드도 함께 표시해야 합니다. 복구 코드는 사용자가 휴대폰을 잃어버렸을 때 인증에 사용할 수 있습니다. Blade를 사용할 경우, 인증된 사용자 인스턴스에서 복구 코드를 배열로 가져올 수 있습니다.

```php
(array) $request->user()->recoveryCodes()
```

JavaScript 프론트엔드에서는 `/user/two-factor-recovery-codes` 엔드포인트에 GET 요청을 보내면 됩니다. 복구 코드 재생성은 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청하세요.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

인증 과정에서 Fortify는 자동으로 이중 인증 화면(`/two-factor-challenge`)으로 사용자를 리다이렉트합니다. 만약 XHR(비동기) 로그인 요청이라면, 응답에 `two_factor` 불리언 프로퍼티가 포함되니, 이를 이용해 이중 인증 화면으로 이동할지 판단하세요.

이중 인증 화면을 반환하는 방법을 Fortify에 알려야 하며, 모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스를 사용해 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 정의합니다.

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify가 `/two-factor-challenge` 라우트를 정의하며, 이 템플릿에는 `/two-factor-challenge`로 POST 요청하는 폼이 필요합니다. 이때 필요한 필드는 유효한 TOTP 토큰의 `code` 또는 복구코드의 `recovery_code`입니다.

로그인 성공 시 `fortify` 설정의 `home`으로 이동, XHR 요청은 204 응답, 실패할 경우에는 두 번째 인증 화면으로 돌아가며 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors), 또는 XHR의 경우 422 상태로 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화

이중 인증을 비활성화하려면 `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내세요. 요청 전 반드시 [비밀번호 확인](#password-confirmation)이 선행되어야 합니다.

<a name="registration"></a>
## 회원 가입

회원 가입 기능을 구현하려면, 먼저 Fortify에 "회원 가입" 뷰를 반환하는 방법을 알려야 합니다. Fortify는 헤드리스 인증 라이브러리입니다. 이미 구현된 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하세요.

회원 가입 뷰 렌더링 역시 Fortify에서 메서드로 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot`에서 정의합니다.

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify는 `/register` 라우트를 자동 등록해 뷰를 반환합니다. `register` 템플릿에는 `/register` 엔드포인트에 POST 요청하는 폼이 필요합니다.

이 엔드포인트는 `name`(문자열), 이메일/유저네임, `password`, `password_confirmation` 필드를 기대합니다. 이메일/유저네임 필드명은 `fortify` 설정의 `username` 값과 동일해야 합니다.

가입 성공 시, Fortify는 `fortify` 설정의 `home` 경로로 리다이렉트하고, XHR 요청인 경우 201 응답을 반환합니다.

실패 시에는 회원 가입 화면으로 돌아가고 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors), XHR 오류는 422로 반환됩니다.

<a name="customizing-registration"></a>
### 회원 가입 커스터마이징

사용자 검증 및 생성 과정은 Fortify 설치 시 생성되는 `App\Actions\Fortify\CreateNewUser` 액션을 수정해 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능 구현을 시작하려면, 우선 Fortify에 "비밀번호 찾기" 화면을 반환하는 방법을 알려야 합니다. Fortify는 UI를 제공하지 않는 라이브러리입니다. 이미 구현된 인증 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하세요.

아래와 같이 뷰 렌더링 함수로 정의합니다.

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify가 `/forgot-password` 엔드포인트를 정의합니다. 이 템플릿에는 `/forgot-password`로 POST하는 폼이 있어야 하며, 입력값(필드)은 문자열 타입의 `email` 입니다. 이 필드명/컬럼명은 `fortify` 설정의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

요청이 성공하면 Fortify는 `/forgot-password` 엔드포인트로 다시 보내고, 보안 링크가 포함된 이메일을 전송합니다. XHR 요청의 경우 200 응답을 반환합니다.

성공 후 `/forgot-password` 화면으로 돌아오면, 세션의 `status` 변수를 사용해 상태 메시지를 표시할 수 있습니다.

`$status` 변수는 앱 `passwords` [언어 파일](/docs/{{version}}/localization)의 항목과 일치합니다. 값을 커스터마이즈하려면 `lang:publish` 명령을 통해 라라벨 언어 파일을 퍼블리시할 수 있습니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패 시, 사용자는 링크 요청 화면으로 다시 리다이렉트되고 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors), XHR은 422 에러로 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정 기능을 완성하려면, Fortify에 "비밀번호 재설정" 뷰를 반환하는 방법도 알려야 합니다.

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify가 해당 라우트를 정의하며, `reset-password` 템플릿에는 `/reset-password`로 POST하는 폼이 필요합니다.

이 엔드포인트에는 `email`, `password`, `password_confirmation`, 그리고 숨은 필드인 `token`(`request()->route('token')`의 값)이 필요합니다. "email" 필드명은 `fortify` 설정의 `email` 값과 동일해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정에 성공하면, Fortify는 `/login` 라우트로 리다이렉트해 새 비밀번호로 로그인할 수 있게 합니다. 성공 상태 메시지는 `status` 세션 변수로 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청의 경우 200 응답을 반환합니다.

재설정이 실패하면, 재설정 화면으로 돌아가고 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)가, XHR은 422 오류로 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정도 Fortify 설치 시 생성되는 `App\Actions\ResetUserPassword` 액션을 수정해 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원 가입 후 사용자가 계속해서 앱에 접근하기 전에 이메일 주소를 인증하도록 만들고 싶을 수 있습니다. 이 경우, `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하고, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하는지 확인하세요.

이 두 단계를 마치면, 새로 회원 가입한 사용자에게 이메일 인증을 요청하는 메일이 전송됩니다. 이제 Fortify에 이메일 인증 화면을 렌더링하는 방법을 알려야 하며, 이를 통해 사용자는 인증 링크를 확인해야 함을 인지할 수 있습니다.

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify가 이 뷰를 `/email/verify` 엔드포인트에 표시하는 라우트를 등록합니다(`verified` 미들웨어를 통해 이동됨).

이 뷰에는 인증 링크를 메일에서 클릭해야 한다는 안내 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

원한다면, 인증 이메일 재전송 버튼을 `verify-email` 템플릿에 구현하여 `/email/verification-notification` 엔드포인트에 POST 요청을 보낼 수 있습니다. 이 엔드포인트로 요청 시 새 인증 이메일이 전송되고, 성공 시 `/email/verify`로 리다이렉트되며, 세션 `status` 변수를 통해 성공 메시지를 표시할 수 있습니다. XHR 요청시에는 202 응답이 반환됩니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새로운 인증 링크가 이메일로 전송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호

사용자가 이메일 인증을 완료할 때에만 접근을 허용하려면 해당 라우트/그룹에 Laravel의 내장 `verified` 미들웨어를 적용하세요. `verified` 별칭은 자동 등록되며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

앱 개발 중, 특정 민감한 동작은 사용자의 비밀번호를 재확인해야 할 필요가 있습니다. 일반적으로 이 기능은 Laravel의 내장 `password.confirm` 미들웨어로 보호됩니다.

비밀번호 확인 기능을 구현하기 위해서도, Fortify에 "비밀번호 확인" 뷰 반환을 알려야 합니다. Fortify는 프론트엔드를 포함하지 않는 인증 라이브러리입니다. 완성된 UI가 필요하면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하세요.

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify가 `/user/confirm-password` 엔드포인트를 정의하며, 이 템플릿에는 `/user/confirm-password`로 POST 요청하는 폼이 필요합니다. 이 엔드포인트는 사용자의 현재 비밀번호가 담긴 `password` 필드를 기대합니다.

입력된 비밀번호가 맞으면, Fortify는 사용자가 접근하려던 라우트로 리다이렉트합니다. XHR 요청의 경우 201 응답이 반환됩니다.

실패 시, 비밀번호 확인 화면으로 돌아가고 오류는 `$errors` Blade 변수로, XHR은 422 오류로 제공됩니다.