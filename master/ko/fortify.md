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
    - [리다이렉션 커스터마이징](#customizing-authentication-redirects)
- [이중 인증(2FA)](#two-factor-authentication)
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
    - [라우트 보호하기](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel용 프론트엔드 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 모든 Laravel 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify 설치 후 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트들을 확인할 수 있습니다.

Fortify는 자체적인 사용자 인터페이스를 제공하지 않으므로, Fortify가 등록한 라우트에 요청을 보내는 별도의 사용자 인터페이스와 함께 사용해야 합니다. 이러한 라우트에 어떻게 요청을 보내야 하는지, 본 문서의 나머지 부분에서 자세히 다룹니다.

> [!NOTE]
> Fortify는 Laravel 인증 기능 구현을 빠르게 시작할 수 있도록 제공되는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고하여 직접 인증 서비스를 구현할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

이미 언급했듯이, Laravel Fortify는 프론트엔드 독립적인 Laravel용 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** [공식 인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 관련 문서를 참고해 직접 상호작용할 수 있습니다.

Laravel를 처음 접하는 경우에는 Fortify를 사용하기 전에 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 확인해 볼 것을 권장합니다. 스타터 킷은 [Tailwind CSS](https://tailwindcss.com)로 제작된 사용자 인터페이스와 인증 스캐폴딩을 제공합니다. 이를 통해 Laravel 인증 기능을 익힌 뒤, Fortify로 해당 기능을 백엔드만 빠르게 구현하는 선택지를 사용할 수 있습니다.

Laravel Fortify는 스타터 킷의 라우트와 컨트롤러를 별도의 UI 없이 패키지 형태로 제공하여, 프론트엔드에 구애받지 않고 인증 백엔드 구현을 빠르게 구축할 수 있게 합니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 하나요?

Laravel Fortify를 언제 사용해야 할지 고민중이라면, 우선 Laravel의 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용 중인 경우 Fortify를 따로 설치할 필요가 없습니다. 스타터 킷에는 이미 완전한 인증 기능이 포함되어 있기 때문입니다.

만약 스타터 킷을 사용하지 않고, 애플리케이션에 인증이 필요하다면 두 가지 방법이 있습니다: 직접 인증 기능을 구현하거나, Fortify를 사용하여 백엔드 인증 기능을 빠르게 구축하는 것입니다.

Fortify를 설치하는 경우, 사용자 인터페이스는 본 문서에 설명된 Fortify의 인증 라우트로 요청을 보내어 사용자 인증 및 회원가입을 처리해야 합니다.

Fortify를 사용하지 않고 직접 인증 서비스를 구현하려면 [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 관련 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

일부 개발자들은 [Laravel Sanctum](/docs/{{version}}/sanctum)과 Laravel Fortify의 차이점으로 혼동하기도 합니다. 두 패키지는 밀접하지만 서로 다른 문제를 해결하므로, 상호 배타적이거나 경쟁 관계가 아닙니다.

Laravel Sanctum은 API 토큰 관리 및 세션 쿠키 또는 토큰으로 기존 사용자를 인증하는 기능만 제공합니다. 회원가입, 비밀번호 재설정 등 라우트는 제공하지 않습니다.

따라서 API 제공 애플리케이션이나 싱글 페이지 애플리케이션(SPA) 백엔드를 직접 구현하는 경우, 사용자는 Laravel Fortify(회원가입, 비밀번호 재설정 등)와 Laravel Sanctum(API 토큰 관리, 세션 인증)을 모두 사용할 수 있습니다.

<a name="installation"></a>
## 설치

우선 Composer 패키지 관리자를 이용해 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로, `fortify:install` Artisan 명령어를 사용해 Fortify 리소스를 퍼블리시하세요:

```shell
php artisan fortify:install
```

이 명령어는 Fortify의 액션을 `app/Actions` 디렉터리에 퍼블리시합니다(존재하지 않으면 자동 생성). 이 외에도 `FortifyServiceProvider`, 설정 파일, 필요한 데이터베이스 마이그레이션이 퍼블리시됩니다.

그 다음 데이터베이스 마이그레이션을 진행해야 합니다:

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에는 `features` 설정 배열이 있습니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 라우트/기능을 정의합니다. 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능만 활성화하는 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면, 회원가입 화면 등 뷰를 반환하는 라우트를 정의합니다. 하지만 자바스크립트 기반의 싱글 페이지 애플리케이션(SPA)을 개발하는 경우 이런 라우트가 필요하지 않을 수 있으므로, 애플리케이션의 `config/fortify.php` 파일 내 `views` 설정값을 `false`로 변경해 라우트를 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰와 비밀번호 재설정 비활성화

Fortify의 뷰를 비활성화하면서 비밀번호 재설정 기능을 구현하려면, 애플리케이션에서 "비밀번호 재설정" 뷰를 표시할 책임이 있는 `password.reset` 이름의 라우트를 직접 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 `password.reset` 라우트로 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

인증 화면을 반환하는 방법을 Fortify에 알려야 합니다. Fortify는 자체 UI가 없는 헤드리스 인증 라이브러리입니다. 만약 인증 UI까지 포함한 구현을 원한다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 것이 더 편리합니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출하는 방식으로 사용하면 됩니다. 예를 들어 `/login` 라우트는 Fortify가 자동 정의하며, 아래와 같이 뷰 반환 로직을 작성할 수 있습니다:

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

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 `email`/`username`과 `password` 문자열을 받으며, 이 필드명은 `config/fortify.php`의 `username` 값과 일치해야 합니다. 추가로 `remember`라는 불리언 필드를 보내면 "로그인 상태 유지" 기능을 사용할 수 있습니다.

로그인 성공 시, Fortify는 애플리케이션 `fortify` 설정 파일의 `home` 옵션에 지정한 URI로 리다이렉트합니다. XHR 요청이라면 200 HTTP 응답을 반환합니다.

로그인 실패 시, 사용자는 다시 로그인 화면으로 리다이렉트되고, 검증 오류는 공유 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다. XHR 요청일 경우 422 HTTP 상태와 함께 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격 증명과 설정된 인증 가드를 활용해 사용자를 검증합니다. 하지만 로그인 자격 증명 검증 및 사용자 조회 로직을 직접 정의하고 싶을 때는 `Fortify::authenticateUsing` 메서드로 커스터마이즈할 수 있습니다.

이 메서드는 HTTP 요청을 전달받는 클로저를 인자로 받으며, 클로저는 전달받은 자격 증명을 검증 후, 연관된 사용자 인스턴스를 반환해야 합니다. 인증 실패 또는 사용자가 없다면 `null`이나 `false`를 반환하세요. 일반적으로 이 메서드는 `FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify에서 사용할 인증 가드는 애플리케이션 `fortify` 설정 파일에서 설정할 수 있습니다. 단, 설정된 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard`를 구현해야 합니다. SPA에서 Fortify를 사용하려면 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)의 조합을 권장합니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 인증 요청을 일련의 Invokable한 클래스 파이프라인을 수행하며 처리합니다. 로그인 요청에 대해 파이프라인을 커스터마이즈하려면 파이프라인 클래스를 배열로 반환하는 클로저를 `Fortify::authenticateThrough` 메서드에 전달하면 됩니다. 이때 각 클래스는 `__invoke` 메서드를 통해 요청을 처리하며, 미들웨어와 유사하게 `$next` 변수를 통해 다음 클래스로 요청을 전달합니다.

주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출하며, 아래는 기본 파이프라인 예시입니다:

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

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어로 인증 시도를 제한합니다. 이 미들웨어는 사용자 이름과 IP 조합별로 시도를 제한합니다.

일부 애플리케이션에서는 IP 기준 제한 등 다른 정책이 필요할 수 있으므로, Fortify는 `fortify.limiters.login` 설정 옵션으로 [속도 제한자](/docs/{{version}}/routing#rate-limiting)를 직접 지정할 수 있습니다. 이 설정은 `config/fortify.php` 파일에서 관리합니다.

> [!NOTE]
> 시도 제한, [이중 인증](/docs/{{version}}/fortify#two-factor-authentication), 외부 웹 방화벽(WAF)을 조합할 때 가장 강력한 보안이 가능합니다.

<a name="customizing-authentication-redirects"></a>
### 리다이렉션 커스터마이징

로그인 성공 시, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리다이렉션합니다. XHR 요청일 경우 200 HTTP 응답을 반환합니다. 로그아웃 후 사용자는 `/` URI로 리다이렉트됩니다.

이 행동을 고급 커스터마이즈하려면, `LoginResponse` 및 `LogoutResponse` 계약을 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 바인딩하면 됩니다. 보통 `App\Providers\FortifyServiceProvider`의 `register` 메서드에 작성합니다:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * 애플리케이션 서비스 등록.
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
## 이중 인증(2FA)

Fortify의 이중 인증 기능을 활성화하면, 인증 과정에서 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 시간 기반 일회용 비밀번호(TOTP)로, 구글 인증기와 같은 TOTP 호환 모바일 앱에서 생성할 수 있습니다.

먼저, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레잇을 사용하는지 확인하세요:

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

그 다음 사용자가 이중 인증 설정을 관리할 수 있는 화면을 구현해야 합니다. 이 화면에서는 이중 인증 활성화/비활성화, 복구 코드 재생성이 가능해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열은 이중 인증 설정 변경 전 비밀번호 확인을 요구하도록 안내합니다. 따라서 먼저 Fortify의 [비밀번호 확인](#password-confirmation) 기능을 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화

이중 인증 활성화를 시작하려면, `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내세요. 성공 시 사용자는 이전 URL로 리다이렉트되며, `status` 세션 변수는 `two-factor-authentication-enabled`로 설정됩니다. 이 값은 템플릿에서 성공 메시지 출력 시 참고할 수 있습니다. XHR 요청 시 200 HTTP 응답이 반환됩니다.

이중 인증을 활성화해도, 사용자는 실제로 이중 인증 코드를 입력해 "확인" 과정을 거쳐야 합니다. 따라서 성공 메시지에서는 추가 확인 안내를 제공해야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 이중 인증 설정을 마무리해 주세요.
    </div>
@endif
```

다음으로 사용자가 인증 앱에 등록할 이중 인증 QR 코드를 보여줘야 합니다. Blade를 사용하는 경우, 유저 인스턴스의 `twoFactorQrCodeSvg` 메서드로 QR코드를 얻을 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 기반 프론트엔드의 경우, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보내면 QR 코드 SVG를 포함한 JSON 객체를 반환합니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 설정 확인

QR코드와 함께, 사용자가 이중 인증 앱에서 생성된 코드를 입력할 수 있는 입력 창을 만들어야 합니다. 사용자가 입력한 코드는 Fortify가 제공하는 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청으로 보내면 됩니다.

요청이 성공하면 사용자는 이전 URL로 리다이렉트되며, `status` 세션 변수는 `two-factor-authentication-confirmed`로 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        이중 인증이 성공적으로 확인 및 활성화되었습니다.
    </div>
@endif
```

XHR 요청 시 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

이중 인증 복구 코드를 사용자에게 보여주어야 합니다. 복구 코드는 사용자가 모바일 접근 권한을 잃었을 때 로그인에 사용할 수 있습니다. Blade를 사용하는 경우 인증된 사용자 인스턴스의 `recoveryCodes()` 메서드로 접근할 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 기반 프론트엔드의 경우, `/user/two-factor-recovery-codes` 엔드포인트에 XHR GET 요청(혹은 POST로 재생성)을 보내면 복구 코드를 받을 수 있습니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

인증 과정 중 Fortify는 자동으로 애플리케이션의 이중 인증 도전 화면으로 리다이렉트합니다. 만약 XHR 로그인 요청이라면, 인증 성공시 반환된 JSON 객체의 `two_factor` 불리언 값을 참고해 이중 인증 화면으로 리다이렉트해야 하는지 알 수 있습니다.

Fortify가 이중 인증 도전 화면을 어떻게 렌더링할지 정의하려면, 아래와 같이 `Laravel\Fortify\Fortify` 클래스의 메서드를 활용해 커스터마이징합니다(보통 `FortifyServiceProvider`의 `boot` 내):

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

Fortify는 `/two-factor-challenge` 라우트를 자동 등록하며, 뷰에는 `/two-factor-challenge`로 POST하는 폼이 포함되어야 합니다. 이때 `code` 필드(유효한 TOTP 토큰) 또는 `recovery_code` 필드(복구 코드)를 입력합니다.

인증 성공 시, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청이라면 204 HTTP 응답이 반환됩니다.

실패 시에는 다시 도전 화면으로 리다이렉트되며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)로 출력하거나, XHR 요청의 경우 422 HTTP 상태로 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화

이중 인증을 비활성화하려면, `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내야 합니다. Fortify의 이중 인증 관련 엔드포인트는 [비밀번호 확인](#password-confirmation) 후에 호출할 수 있습니다.

<a name="registration"></a>
## 회원가입

회원가입 기능을 구현하려면, Fortify가 "회원가입" 뷰를 반환하는 방식을 지정해야 합니다. Fortify 자체는 UI가 없는 인증 라이브러리이며, UI까지 함께 사용하려면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)이 더 적합합니다.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 커스터마이즈할 수 있습니다. 보통 `FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify는 `/register` 라우트를 자동 정의하며, `register` 템플릿에는 `/register`로 POST하는 폼이 포함되어야 합니다.

`/register` 엔드포인트는 `name`(문자열), `email`/`username`(문자열), `password` 및 `password_confirmation` 필드를 기대하며, 이메일/사용자명 필드명은 `fortify` 설정 파일의 `username` 값과 일치해야 합니다.

회원가입 성공시 설정된 URI로 리다이렉트, XHR 요청시 201 HTTP 응답이 반환됩니다.

실패 시에는 다시 회원가입 화면, 혹은 XHR일 때 422와 함께 검증 오류가 전달됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

사용자 검증 및 생성 과정은 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능을 구현하려면, Fortify가 "비밀번호 찾기" 뷰를 반환하는 방법을 지정해야 합니다. Fortify는 UI가 없는 라이브러리이며, UI까지 사용하려면 [스타터 킷](/docs/{{version}}/starter-kits)을 사용하세요.

아래와 같이 뷰 렌더링 로직을 커스터마이즈합니다:

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

Fortify는 `/forgot-password` 엔드포인트를 자동 정의하며, `forgot-password` 템플릿에는 해당 엔드포인트로 POST 요청하는 폼이 필요합니다.

`/forgot-password`는 `email` 문자열 필드를 받으며, 필드명은 `fortify` 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

요청이 성공하면 `/forgot-password`로 리다이렉트되며, 사용자에게 이메일로 보안 링크가 전송됩니다. XHR 요청이면 200 HTTP 응답이 반환됩니다. 성공 후 리다이렉트된 화면에서는 `status` 세션 값을 사용해 성공 메시지를 나타낼 수 있습니다.

`$status` 값은 애플리케이션의 `passwords` [언어 파일](/docs/{{version}}/localization) 내 번역 문자열과 일치합니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패한 경우에도 다시 해당 화면으로 리다이렉트되며, `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 또는 422 오류(HTTP/JSON) 형태로 검증 오류가 전달됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정을 마무리하려면 "비밀번호 재설정" 뷰 반환 방식을 Fortify에 지시해야 합니다.

아래 예시처럼 설정합니다:

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

Fortify는 라우트 정의를 자동 처리하며, `reset-password` 템플릿에는 `/reset-password`로 POST 요청하는 폼이 필요합니다.

`/reset-password`는 `email`, `password`, `password_confirmation` 필드와, `request()->route('token')` 값을 담는 숨은 필드 `token`이 필요합니다. "email" 필드명/DB컬럼은 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

성공 시 `/login` 라우트로 리다이렉트하며, 로그인 화면에서 성공 메시지를 띄울 수 있도록 `status` 세션 변수가 설정됩니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청의 경우 200 HTTP 응답이 반환됩니다. 실패 시, 다시 재설정 화면 혹은 422 검증 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 커스터마이징할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자가 이메일 인증을 완료해야 하도록 설정할 수 있습니다. 이를 위해 먼저 `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 다음, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하고 있는지 확인합니다.

이 두 가지 사전 작업이 완료되면 새로 가입한 사용자에게 이메일 인증 링크가 전송됩니다. 이 인증 화면(이메일 인증 필요 메시지를 보여주는 화면)의 렌더링 방식도 Fortify에 지시해야 합니다.

아래와 같이 뷰 렌더링 로직을 작성합니다:

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

Fortify는 `/email/verify`로 리다이렉트되는 경우 이 뷰를 렌더링하는 라우트를 자동 정의합니다.

`verify-email` 템플릿에는 사용자가 이메일의 인증 링크를 클릭하라는 안내 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

원하는 경우 `verify-email` 템플릿에 `/email/verification-notification` 엔드포인트로 POST 요청을 보내는 버튼을 추가할 수 있습니다. 이 엔드포인트는 사용자가 기존 인증 링크를 분실한 경우 새 인증 이메일을 발송합니다.

성공 시 Fortify는 `/email/verify`로 리다이렉트하면서 `status` 세션 변수를 제공합니다. XHR 요청의 경우 202 HTTP 응답이 반환됩니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새로운 이메일 인증 링크가 전송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기

특정 라우트나 라우트 그룹에 이메일 인증 여부를 검증하려면, 라우트에 Laravel의 내장 `verified` 미들웨어를 추가하세요. 이 미들웨어 별칭은 자동으로 등록되어 있으며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션에서 일부 액션은 실행 전 사용자가 비밀번호를 확인하도록 요구할 수 있습니다. 이 경우, 해당 라우트에 Laravel의 내장 `password.confirm` 미들웨어를 사용할 수 있습니다.

비밀번호 확인 기능을 구현하려면 Fortify가 "비밀번호 확인" 뷰를 반환하는 방식을 지정해야 합니다. Fortify는 UI가 없는 인증 라이브러리이므로, UI가 필요하다면 [스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 것이 좋습니다.

Fortify 뷰 렌더링 로직은 다음과 같이 지정할 수 있습니다:

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

Fortify는 `/user/confirm-password` 엔드포인트를 자동 등록합니다. `confirm-password` 템플릿에는 해당 엔드포인트로 POST 요청을 보내는 폼이 있어야 하며, `password` 필드에는 사용자의 현재 비밀번호가 필요합니다.

비밀번호가 일치하면 Fortify는 사용자가 원래 접근하려던 라우트로 리다이렉트합니다. XHR 요청의 경우 201 HTTP 응답이 반환됩니다.

검증 실패 시, 다시 비밀번호 확인 화면 또는 422 응답이 반환됩니다. 검증 오류는 공유 `$errors` Blade 템플릿 변수로 확인할 수 있습니다.