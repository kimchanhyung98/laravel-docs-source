# Laravel Fortify

- [소개](#introduction)
    - [Fortify란 무엇인가?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 사용자화](#customizing-user-authentication)
    - [인증 파이프라인 사용자화](#customizing-the-authentication-pipeline)
    - [리다이렉트 사용자화](#customizing-authentication-redirects)
- [2단계 인증](#two-factor-authentication)
    - [2단계 인증 활성화](#enabling-two-factor-authentication)
    - [2단계 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [2단계 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 사용자화](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 사용자화](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel용 프론트엔드 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후에는 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않으므로, 여러분만의 UI를 만들어 Fortify가 등록한 라우트에 요청을 보내야 합니다. 이 문서의 나머지 부분에서는 이 라우트들에 요청하는 방법을 자세히 다룹니다.

> [!NOTE]
> Fortify는 Laravel의 인증 기능 구현을 빠르게 시작할 수 있도록 돕는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** Laravel의 인증, 비밀번호 재설정, 이메일 인증 문서([authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), [email verification](/docs/12.x/verification))를 참고해 직접 구현해도 됩니다.

<a name="what-is-fortify"></a>
### Fortify란 무엇인가?

앞서 언급했듯, Laravel Fortify는 Laravel용 프론트엔드 독립적인 인증 백엔드 구현체입니다. 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** Laravel의 인증 관련 공식 문서([authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), [email verification](/docs/12.x/verification))를 참고해 직접 구현할 수 있습니다.

Laravel에 익숙하지 않은 경우, 먼저 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 살펴보시길 권장합니다. 스타터 키트는 [Tailwind CSS](https://tailwindcss.com)를 사용한 UI와 함께 제공되는 인증 스캐폴딩을 포함하여, Laravel 인증 기능을 이해하고 익힐 수 있도록 돕습니다. 그런 다음 Fortify를 사용해 인증 기능을 구현하는 것도 좋습니다.

Laravel Fortify는 애플리케이션 스타터 키트의 라우트와 컨트롤러를 사용자 인터페이스 없이 패키지 형태로 제공합니다. 덕분에 특정 프론트엔드 디자인에 의존하지 않고도 애플리케이션 인증 구현 백엔드를 빠르게 구축할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나?

Laravel Fortify를 언제 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 키트](/docs/12.x/starter-kits) 중 하나를 사용한다면 Fortify를 설치할 필요가 없습니다. 대부분 스타터 키트가 이미 완전한 인증 구현을 포함하기 때문입니다.

애플리케이션 스타터 키트를 사용하지 않고 인증 기능이 필요하다면, 직접 구현하거나 Fortify를 사용해 인증 백엔드를 제공받는 두 가지 방법이 있습니다.

Fortify를 설치하면 여러분의 UI가 이 문서에 상세히 설명된 Fortify의 인증 라우트에 요청을 보내 사용자 인증과 회원가입을 처리하게 됩니다.

직접 Laravel 인증 서비스를 다루고 싶다면, 항상 [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), [email verification](/docs/12.x/verification) 문서를 참고해 수동으로 구현할 수 있습니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

일부 개발자는 [Laravel Sanctum](/docs/12.x/sanctum)과 Laravel Fortify의 차이를 혼동하기도 합니다. 두 패키지는 서로 관련 있지만 서로 대체하거나 경쟁하는 관계가 아닙니다.

Laravel Sanctum은 API 토큰 관리와 세션 쿠키 또는 토큰 방식으로 기존 사용자를 인증하는 데 집중합니다. Sanctum은 사용자 등록, 비밀번호 재설정 같은 라우트를 제공하지 않습니다.

만약 API를 제공하거나 SPA(싱글 페이지 애플리케이션)의 백엔드를 구축하는 인증 레이어를 직접 만들려고 한다면, Laravel Fortify(사용자 등록, 비밀번호 재설정 등)와 Laravel Sanctum(API 토큰 관리, 세션 인증)을 동시에 함께 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용해 Fortify를 설치합니다:

```shell
composer require laravel/fortify
```

다음으로, `fortify:install` Artisan 명령어를 실행해 Fortify 리소스를 게시합니다:

```shell
php artisan fortify:install
```

이 명령어는 `app/Actions` 디렉토리(존재하지 않으면 생성됨)에 Fortify의 액션을 게시합니다. 또한 `FortifyServiceProvider`, 설정 파일, 필요한 모든 데이터베이스 마이그레이션이 게시됩니다.

마지막으로 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에는 `features` 배열이 있습니다. 이 배열은 Fortify가 기본으로 제공할 백엔드 라우트 및 기능을 정의합니다. 대부분의 Laravel 애플리케이션에서 기본 인증 기능만 활성화할 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면, 회원가입 화면과 같은 뷰를 반환하는 라우트를 정의합니다. 하지만 JavaScript 기반 싱글 페이지 애플리케이션을 구축하는 경우 이 라우트가 필요 없을 수 있습니다. 이럴 때는 애플리케이션의 `config/fortify.php` 설정 파일에서 `views` 값을 `false`로 설정해 해당 라우트들을 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화와 비밀번호 재설정

Fortify의 뷰를 비활성화하지만 비밀번호 재설정 기능은 구현할 경우, 애플리케이션 내에서 `password.reset`이라는 이름의 라우트를 반드시 정의해야 합니다. Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 `password.reset` 이름 라우트를 통해 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

시작하려면, Fortify에 로그인 뷰를 반환하는 방법을 알려야 합니다. Fortify는 헤드리스(headless) 인증 라이브러리이므로, 이미 완성된 Laravel 인증 프론트엔드 구현이 필요하다면 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하는 편이 좋습니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드를 이용해 사용자화할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스 내 `boot` 메서드에서 호출해야 합니다. Fortify가 `/login` 경로를 정의하여 지정한 뷰를 반환합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

로그인 템플릿에는 `/login`에 POST 요청하는 폼이 있어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email` 또는 `username`과 `password`를 받습니다. 이메일 또는 사용자 이름 필드 이름은 `config/fortify.php` 설정 파일 내 `username` 값과 일치해야 합니다. 또한, 사용자가 "기억하기" 기능을 사용하려는 경우 `remember`라는 불리언 필드를 함께 보낼 수 있습니다.

로그인 시도가 성공하면 Fortify는 `fortify` 설정 파일 내 `home` 옵션에 지정된 URI로 리다이렉트합니다. 만약 로그인 요청이 XHR 요청일 경우, 200 HTTP 응답이 반환됩니다.

성공하지 못하면 로그인 화면으로 리다이렉트되고, 유효성 검증 오류가 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)를 통해 사용 가능합니다. XHR 요청일 경우 422 HTTP 응답과 함께 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 사용자화

Fortify는 제공된 자격 증명과 애플리케이션에 설정된 인증 가드를 토대로 자동으로 사용자 인증 및 조회를 진행합니다. 하지만 로그인 자격 증명 인증 방법과 사용자 조회 방식을 완전히 사용자화하고자 할 때도 있습니다. 다행히 Fortify는 `Fortify::authenticateUsing` 메서드를 통해 이를 손쉽게 수행할 수 있습니다.

이 메서드는 HTTP 요청을 매개변수로 받는 클로저를 인수로 받습니다. 이 클로저는 요청의 로그인 자격 증명을 검증하고 해당 사용자를 반환해야 합니다. 자격 증명이 유효하지 않거나 사용자를 찾지 못하면 `null` 또는 `false`를 반환해야 합니다. 보통 `FortifyServiceProvider` 내 `boot` 메서드에서 호출합니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
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

Fortify가 사용하는 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 사용자화할 수 있습니다. 다만, 설정되는 가드는 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스를 구현하는지 확인해야 합니다. SPA를 인증할 때는 Laravel의 기본 `web` 가드를 [Laravel Sanctum](https://laravel.com/docs/sanctum)과 함께 사용하는 것이 권장됩니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 사용자화

Laravel Fortify는 로그인 요청을 호출 가능 클래스(invokable class)들의 파이프라인을 통해 인증합니다. 필요한 경우 로그인 요청을 어떤 클래스들을 거치도록 할지 사용자 정의 파이프라인을 정의할 수 있습니다. 각 클래스는 `__invoke` 메서드를 가지며 `Illuminate\Http\Request`와 다음 단계로 요청을 넘기는 `$next`를 인수로 받는 [미들웨어](/docs/12.x/middleware)와 유사한 구조입니다.

사용자 정의 파이프라인은 `Fortify::authenticateThrough` 메서드로 정의합니다. 이 메서드는 클로저를 인수로 받아 로그인 요청을 통과시킬 클래스들의 배열을 반환해야 합니다. 보통 `App\Providers\FortifyServiceProvider` 내 `boot`에서 호출합니다.

아래 예시는 기본 파이프라인 정의로, 사용자화 시 시작점으로 사용할 수 있습니다:

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

#### 인증 시도 제한(Throttle)

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어를 사용해 인증 시도를 제한합니다. 이 미들웨어는 사용자 이름과 IP 조합별로 제한을 적용합니다.

어떤 애플리케이션은 IP 주소 단독으로 제한하는 등 다른 제한 방식이 필요할 수 있습니다. 이럴 때는 `fortify.limiters.login` 설정 옵션을 통해 자신만의 [레이트 리미터](/docs/12.x/routing#rate-limiting)를 지정할 수 있습니다. 해당 설정은 애플리케이션 `config/fortify.php`에 있습니다.

> [!NOTE]
> 제한, [2단계 인증](/docs/12.x/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF)을 조합하면, 애플리케이션 사용자 보호에 가장 강력한 방어선을 갖출 수 있습니다.

<a name="customizing-authentication-redirects"></a>
### 리다이렉트 사용자화

로그인 성공 시 Fortify는 `fortify` 설정 파일 내 `home` 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청일 경우 200 HTTP 응답이 반환됩니다. 로그아웃 시에는 사용자를 `/` URI로 리다이렉트합니다.

이 동작을 더 세밀하게 사용자화하려면, `LoginResponse`와 `LogoutResponse` 계약의 구현체를 Laravel [서비스 컨테이너](/docs/12.x/container)에 바인딩하면 됩니다. 보통 이 코드는 애플리케이션 `App\Providers\FortifyServiceProvider` 클래스 내 `register` 메서드에서 작성합니다:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * 애플리케이션 서비스 등록
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
## 2단계 인증

Fortify의 2단계 인증 기능이 활성화되면, 사용자는 인증 과정 중 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 시간 기반 일회용 비밀번호(TOTP)로 생성되며, 구글 인증기(Google Authenticator) 같은 TOTP 지원 모바일 인증 앱에서 확인할 수 있습니다.

먼저 애플리케이션의 `App\Models\User` 모델이 반드시 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하도록 설정되어 있어야 합니다:

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

이후에는 사용자들이 2단계 인증 설정을 관리할 수 있는 화면을 만들어야 합니다. 이 화면에서는 2단계 인증 활성화, 비활성화와 2단계 인증 복구 코드 재생성이 가능해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열 내 2단계 인증 기능에서는 수정 전에 비밀번호 확인을 요구합니다. 따라서 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화

2단계 인증을 시작하려면 `/user/two-factor-authentication` 경로로 POST 요청을 보내야 합니다. 요청이 성공하면, 사용자 브라우저는 이전 URL로 리다이렉트되고 세션 변수 `status`가 `two-factor-authentication-enabled`로 설정됩니다. 이 값을 템플릿에서 감지해 성공 메시지를 표시할 수 있습니다. XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

2단계 인증 활성화를 선택했더라도, 사용자는 유효한 2단계 인증 코드를 입력해 인증 구성을 "확인"해야 합니다. 따라서 성공 메시지는 2단계 인증 확인이 여전히 필요함을 안내해야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 2단계 인증 구성 완료를 마무리해 주세요.
    </div>
@endif
```

이후 사용자가 인증 앱으로 스캔할 수 있도록 2단계 인증 QR 코드를 보여줘야 합니다. Blade를 사용하는 경우, 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드를 통해 SVG 코드를 가져올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

JavaScript 기반 프론트엔드를 구축하는 경우, `/user/two-factor-qr-code` GET 요청을 XHR으로 보내 사용자 2단계 인증 QR 코드를 JSON 형태로 받을 수 있습니다. 해당 응답은 `svg` 키가 포함됩니다.

<a name="confirming-two-factor-authentication"></a>
#### 2단계 인증 확인

사용자의 2단계 인증 QR 코드 표시 외에, 2단계 인증 구성을 "확인"하기 위한 유효한 코드를 입력하는 텍스트 필드를 제공해야 합니다. 이 코드는 Fortify가 제공하는 `/user/confirmed-two-factor-authentication` 경로로 POST 요청해 제출합니다.

요청이 성공하면 이전 URL로 리다이렉트되고, 세션 변수 `status`가 `two-factor-authentication-confirmed`로 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        2단계 인증이 성공적으로 확인되어 활성화되었습니다.
    </div>
@endif
```

XHR 요청일 경우 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

사용자가 모바일 기기에 접근할 수 없을 때를 대비한 2단계 인증 복구 코드를 보여줘야 합니다. Blade를 사용하는 경우 인증된 사용자 인스턴스에서 복구 코드를 배열로 가져올 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

JavaScript 기반 프론트엔드라면, `/user/two-factor-recovery-codes` 경로에 GET XHR 요청을 보내 복구 코드 배열을 JSON으로 받을 수 있습니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 경로에 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 인증하기

인증 과정에서 Fortify는 자동으로 사용자를 2단계 인증 챌린지 화면으로 리다이렉트합니다. 단, 로그인 요청이 XHR일 경우 인증 성공 응답에 `two_factor`라는 불리언 속성이 포함되어 있습니다. 이 값을 검사해 2단계 인증 챌린지 화면으로 리다이렉트할지 판단할 수 있습니다.

2단계 인증 챌린지 뷰 반환 방법을 Fortify에 알려줘야 합니다. 모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 사용자화할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify가 `/two-factor-challenge` 경로를 정의하고 뷰를 반환합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge`로 POST 요청하는 폼이 있어야 합니다. 이 경로는 `code`(유효한 TOTP 토큰) 또는 `recovery_code`(복구 코드 중 하나) 필드를 기대합니다.

로그인이 성공하면 `fortify` 설정 내 `home` 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청일 경우 204 HTTP 응답이 반환됩니다.

실패 시 두 단계 인증 챌린지 화면으로 리다이렉트되며, 검증 오류는 `$errors` Blade 변수로 사용 가능합니다. XHR 요청일 경우 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화

2단계 인증을 비활성화하려면 `/user/two-factor-authentication` 경로에 DELETE 요청을 보내야 합니다. Fortify 2단계 인증 관련 엔드포인트 호출 전에 [비밀번호 확인](#password-confirmation)이 필요합니다.

<a name="registration"></a>
## 회원가입

회원가입 기능 구현을 시작하려면 Fortify에 회원가입 뷰 반환 방법을 알려야 합니다. Fortify는 헤드리스 인증 라이브러리이므로 이미 완성된 Laravel 인증 프론트엔드 구현이 필요하면 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 권장합니다.

Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 사용자화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 내 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify가 `/register` 라우트를 정의하고 뷰를 반환합니다. `register` 템플릿에는 Fortify가 정의한 `/register`로 POST 요청하는 폼이 포함되어야 합니다.

`/register` 엔드포인트는 문자열 `name`, 이메일 또는 사용자 이름, `password`, `password_confirmation` 필드를 기대합니다. 이메일 또는 사용자 이름 필드명은 애플리케이션 `fortify` 설정 파일 내 `username` 값과 일치해야 합니다.

회원가입이 성공하면 `fortify` 설정 파일 `home` 옵션에 지정된 URI로 리다이렉트됩니다. XHR 요청일 경우 201 HTTP 응답이 반환됩니다.

성공하지 못하면 회원가입 화면으로 리다이렉트되고, 검증 오류는 `$errors` [Blade 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다. XHR 요청일 때는 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 사용자화

사용자 검증과 생성 과정은 Laravel Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정하여 사용자화할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능을 구현하려면 Fortify에 "비밀번호 찾기" 뷰 반환 방법을 알려야 합니다. Fortify는 헤드리스 인증 라이브러리이므로 이미 완성된 Laravel 인증 UI가 필요하면 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하세요.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 해당 메서드를 통해 사용자화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 내 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify는 `/forgot-password` 경로를 정의하고 뷰를 반환합니다. `forgot-password` 템플릿에는 `/forgot-password`로 POST 요청하는 폼이 포함됩니다.

`/forgot-password` 엔드포인트는 문자열 `email` 필드를 기대합니다. 해당 필드명과 데이터베이스 칼럼명은 `fortify` 설정 파일 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면, Fortify는 사용자를 `/forgot-password`로 리다이렉트하고 비밀번호 재설정에 필요한 안전한 링크가 포함된 이메일을 발송합니다. XHR 요청이라면 200 HTTP 응답을 반환합니다.

성공 후 `/forgot-password`로 리다이렉트되면, `status` 세션 변수를 사용해 비밀번호 재설정 링크 요청 상태 메시지를 표시할 수 있습니다.

`status` 값은 애플리케이션 내 `passwords` [언어 파일](/docs/12.x/localization)에 정의된 번역 문자열 중 하나와 일치합니다. Laravel의 언어 파일을 공개하지 않았다면 `lang:publish` Artisan 명령어로 공개하여 수정할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패 시 비밀번호 재설정 링크 요청 화면으로 리다이렉트되고, 검증 오류는 `$errors` [Blade 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)에서 확인할 수 있습니다. XHR 요청일 경우 422 HTTP 응답과 함께 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

애플리케이션의 비밀번호 재설정 기능을 완료하려면 Fortify에 "비밀번호 재설정" 뷰 반환 방법을 알려야 합니다.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드를 통해 사용자화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify가 이 뷰를 반환하는 라우트를 정의합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청하는 폼이 필요합니다.

`/reset-password` 엔드포인트는 문자열 `email`, `password`, `password_confirmation` 필드와 숨겨진 `token` 필드를 기대합니다. `token` 필드 값은 `request()->route('token')`입니다. `email` 필드명과 데이터베이스 칼럼명은 애플리케이션 `fortify` 설정 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 `/login` 경로로 리다이렉트하여 사용자가 새 비밀번호로 로그인할 수 있게 합니다. 또한 `status` 세션 변수가 설정되어 로그인 화면에서 성공 메시지를 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청일 경우 200 HTTP 응답이 반환됩니다.

요청 실패 시 비밀번호 재설정 화면으로 리다이렉트되고 검증 오류는 `$errors` [Blade 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다. XHR일 경우 422 HTTP 코드와 함께 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 사용자화

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 사용자화할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

가입 후 사용자가 이메일 주소를 인증한 뒤 애플리케이션에 접근하도록 할 수 있습니다. 시작하려면 `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있어야 합니다. 또한 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

설정이 완료되면 가입한 사용자에게 이메일 소유권 인증 요청 메일이 발송됩니다. 다만, Fortify에 이메일 인증 필요 화면을 어떻게 표시할지 알려줘야 합니다.

모든 Fortify 뷰 렌더링은 `Laravel\Fortify\Fortify` 메서드로 사용자화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 내 `boot`에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify는 Laravel 내장 `verified` 미들웨어가 리다이렉트하는 `/email/verify` 경로를 정의하여 뷰를 반환합니다.

`verify-email` 템플릿에는 이메일 인증 링크를 이메일에서 클릭해야 한다는 안내 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

원한다면 `verify-email` 템플릿에 POST 요청을 `/email/verification-notification` 경로로 보내는 버튼을 추가할 수 있습니다. 요청 시 새 인증 이메일 링크가 사용자에게 전송되어, 이전 링크를 분실하거나 삭제한 경우 새 인증 링크를 받을 수 있습니다.

성공 시 Fortify는 `/email/verify` 경로로 리다이렉트하고 `status` 세션 변수를 설정하여 사용자에게 성공 메시지를 전달할 수 있습니다. XHR 요청인 경우 202 HTTP 응답을 반환합니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새 이메일 인증 링크가 발송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호

특정 라우트 또는 라우트 그룹에 사용자의 이메일 인증이 필요하도록 하려면 Laravel 내장 `verified` 미들웨어를 해당 라우트에 붙이면 됩니다. `verified` 미들웨어는 Laravel에서 자동 등록되며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하다 보면, 특정 작업을 수행하기 전에 사용자가 비밀번호를 재확인하게 하고 싶을 때가 있습니다. Laravel 내장 `password.confirm` 미들웨어로 이러한 경로를 보호하는 것이 일반적입니다.

비밀번호 확인 기능을 구현하려면 Fortify에 비밀번호 확인 뷰 반환 방법을 알려야 합니다. Fortify는 헤드리스 인증 라이브러리이므로, 이미 완성된 Laravel 인증 UI가 필요하면 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 추천합니다.

Fortify 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 사용자화하며, 보통 `App\Providers\FortifyServiceProvider` 내 `boot`에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify는 `/user/confirm-password` 경로를 정의하고 뷰를 반환합니다. `confirm-password` 템플릿에는 `/user/confirm-password`로 POST 요청하는 폼이 있어야 하며, `password` 필드를 포함해야 합니다 (사용자의 현재 비밀번호).

비밀번호가 일치하면 Fortify는 사용자가 접근하려던 라우트로 리다이렉트합니다. XHR 요청의 경우 201 HTTP 응답이 반환됩니다.

실패하면 비밀번호 확인 화면으로 리다이렉트되고 검증 오류는 `$errors` Blade 변수로 확인 가능합니다. XHR 요청 시 422 HTTP 응답과 함께 에러가 반환됩니다.