# Laravel Fortify

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 서비스 프로바이더](#the-fortify-service-provider)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화하기](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리디렉션 커스터마이징](#customizing-authentication-redirects)
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

[Laravel Fortify](https://github.com/laravel/fortify)는 프론트엔드에 종속되지 않은 Laravel 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스를 제공하지 않으므로, 여러분이 직접 만든 UI와 조합하여 등록된 라우트로 요청을 보내는 방식으로 사용해야 합니다. 이 문서의 나머지 부분에서는 이러한 라우트로 요청을 보내는 방법에 대해 자세히 다룹니다.

> [!NOTE]  
> Fortify는 Laravel의 인증 기능 구현을 빠르게 시작하도록 도와주는 패키지입니다. **반드시 Fortify를 사용해야 하는 것은 아닙니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고해 직접 Laravel의 인증 서비스를 사용할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

앞서 설명한 것처럼, Laravel Fortify는 프론트엔드에 종속되지 않은 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현할 수 있도록 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 쓸 필요는 없습니다.** [인증], [비밀번호 재설정], [이메일 인증] 문서를 참고하여 직접 구현할 수도 있습니다.

Laravel의 초보자라면 Fortify를 사용하기 전에 [Laravel Breeze](/docs/{{version}}/starter-kits) 스타터 키트를 먼저 살펴보는 것이 좋습니다. Breeze는 [Tailwind CSS](https://tailwindcss.com)로 만들어진 사용자 인터페이스와 함께 인증 기본 구조를 제공합니다. Breeze는 Fortify와 달리 라우트와 컨트롤러를 여러분의 앱 안에 직접 게시합니다. 이는 Laravel 인증 시스템을 직접 공부하고 익힌 뒤에 Fortify로 옮겨가는 데 도움이 됩니다.

Fortify는 Laravel Breeze의 라우트와 컨트롤러를 패키지 형태로 제공하지만, 사용자 인터페이스는 포함하지 않습니다. 이를 통해 특정 프론트엔드에 영향을 받지 않고 백엔드 인증 레이어를 신속하게 구축할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나요?

Laravel Fortify를 사용할 시기가 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우에는 별도의 Fortify 설치가 필요 없습니다. 모든 스타터 키트는 인증 기능을 기본적으로 제공합니다.

스타터 키트를 사용하지 않고 인증 기능이 필요하다면, 두 가지 방법이 있습니다: 직접 인증 기능을 구현하거나, Fortify를 설치해 인증 백엔드를 구축하는 것입니다.

Fortify를 설치하면, 여러분의 프론트엔드 UI는 이 문서에서 설명하는 Fortify의 인증 라우트로 요청을 보내어 인증 및 회원가입 기능을 구현하게 됩니다.

Fortify를 쓰지 않고 직접 인증 서비스를 사용하고 싶다면, [인증], [비밀번호 재설정], [이메일 인증] 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

[Laravel Sanctum](/docs/{{version}}/sanctum)과 Fortify의 차이점으로 혼동할 수 있습니다. 두 패키지는 각각 다른(그러나 연관된) 문제를 해결하며, 상호 배타적이거나 경쟁 관계가 아닙니다.

Sanctum은 API 토큰 관리와 세션 쿠키 또는 토큰으로 기존 사용자 인증만을 담당합니다. 즉, 회원가입, 비밀번호 재설정 등과 관련된 라우트를 제공하지 않습니다.

API를 제공하거나 SPA(싱글 페이지 애플리케이션)의 백엔드를 직접 구축하려 할 때, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)을 함께 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 통해 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로, `vendor:publish` 명령어를 사용해 Fortify의 리소스를 게시합니다:

```shell
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

이 명령어는 Fortify의 액션 클래스를 `app/Actions` 디렉토리에 게시합니다(디렉토리가 없다면 새로 생성). 또한 `FortifyServiceProvider`, 설정 파일 및 필요한 데이터베이스 마이그레이션도 함께 게시됩니다.

그리고 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify 서비스 프로바이더

방금 설명한 `vendor:publish` 명령어는 `App\Providers\FortifyServiceProvider` 클래스도 게시합니다. 반드시 이 클래스가 `config/app.php`의 `providers` 배열에 등록되어 있는지 확인하세요.

Fortify 서비스 프로바이더는 Fortify가 게시한 액션을 등록하고, 해당 작업이 실행될 때 Fortify에서 이를 사용하도록 지정합니다.

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에는 `features` 배열이 있습니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 라우트/기능을 정의합니다. [Laravel Jetstream](https://jetstream.laravel.com)과 Fortify를 함께 사용하지 않는 경우, 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능만 활성화할 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화하기

Fortify는 기본적으로 로그인/회원가입 화면 등 뷰를 반환하는 라우트도 정의합니다. 하지만 자바스크립트 기반 SPA(싱글 플레이 애플리케이션)를 개발하는 경우라면 이런 라우트가 필요 없을 수 있습니다. 이럴 땐 `config/fortify.php`의 `views` 값을 `false`로 설정해 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 및 비밀번호 재설정 비활성화

Fortify의 뷰를 사용하지 않으면서 비밀번호 재설정 기능을 구현하려는 경우, 애플리케이션에서 비밀번호 재설정 페이지를 노출하는 `password.reset` 이름의 라우트는 반드시 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 `password.reset` 이름의 라우트로 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

시작하려면 Fortify에 "로그인" 화면을 반환하는 방법을 알려줘야 합니다. Fortify는 프론트엔드가 없는 헤드리스 인증 라이브러리임을 기억하세요. 이미 구현이 완료된 프론트엔드와 인증 기능을 원한다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 사용을 권장합니다.

모든 인증 화면 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드를 통해 커스터마이즈할 수 있습니다. 보통은 `App\Providers\FortifyServiceProvider`의 `boot` 메소드에서 아래와 같이 호출합니다. Fortify는 `/login` 라우트를 정의하여 이 뷰를 반환합니다:

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

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 `email`(또는 `username`)과 `password`를 기대합니다. 필드명의 경우 `config/fortify.php`의 `username` 설정값과 일치해야 합니다. 추가로, 사용자가 Laravel의 "로그인 상태 유지" 기능을 이용하고 싶다면 불리언 `remember` 필드를 폼에 포함할 수 있습니다.

로그인이 성공하면, Fortify는 설정 파일의 `home` 옵션에 지정된 URI로 리디렉트합니다. XHR 요청일 경우 200 HTTP 응답을 반환합니다.

실패하면 사용자는 로그인 화면으로 리디렉트되고, 검증 오류는 [공유 Blade 템플릿 변수]($errors)로 제공됩니다. XHR 요청의 경우 422 HTTP 응답에 검증 오류가 포함되어 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격증명과 설정된 인증 가드를 이용해 사용자를 자동으로 조회 및 인증합니다. 하지만 인증 방식을 완전히 커스터마이즈하고 싶다면, `Fortify::authenticateUsing` 메서드를 사용할 수 있습니다.

이 메서드는 클로저를 받고, 클로저 안에서 요청의 로그인 자격증명을 검증하여 연관된 사용자를 반환하도록 할 수 있습니다. 유효하지 않거나 사용자를 찾지 못하면 `null` 또는 `false`를 반환하세요. 주로 `FortifyServiceProvider`의 `boot` 메서드에서 사용합니다:

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

Fortify에서 사용하는 인증 가드는 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 반드시 `Illuminate\Contracts\Auth\StatefulGuard`의 구현이어야 합니다. SPA 인증에 Fortify를 사용하는 경우, Laravel의 기본 `web` 가드를 [Sanctum](https://laravel.com/docs/sanctum)과 함께 사용하는 것이 일반적입니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 여러 호출 가능한 클래스로 구성된 파이프라인을 통해 처리합니다. 필요하다면 로그인 요청이 거칠 파이프라인을 직접 정의할 수 있습니다. 각 클래스는 `__invoke` 메서드를 가지고 있어, 요청 객체와 함께 [미들웨어] 스타일의 `$next` 변수를 받을 수 있어야 합니다.

커스텀 파이프라인을 정의하려면 `Fortify::authenticateThrough` 메서드를 사용하세요. 이 메서드는 로그인 요청이 통과할 클래스 배열을 반환하는 클로저를 받습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

아래는 커스터마이즈를 위한 기본 파이프라인 예시입니다:

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
### 리디렉션 커스터마이징

로그인 성공 시, Fortify는 `fortify` 설정 파일의 `home`에 지정된 URI로 리디렉션합니다. XHR 요청인 경우 200 HTTP 응답을 반환합니다. 로그아웃 후에는 `/` URI로 리디렉션됩니다.

이 동작을 더 세밀하게 커스터마이즈 하려면, `LoginResponse`와 `LogoutResponse` 계약의 구현체를 Laravel의 [서비스 컨테이너]에 바인딩하면 됩니다. 보통은 `App\Providers\FortifyServiceProvider`의 `register` 메서드에서 처리합니다:

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
## 이중 인증(2FA)

Fortify의 이중 인증 기능이 활성화되면, 사용자는 인증 과정에서 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 시간 기반 일회용 비밀번호(TOTP) 방식으로 생성되며, Google Authenticator와 같은 TOTP 호환 모바일 인증 앱에서 얻을 수 있습니다.

먼저, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하는지 확인하세요:

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

그 다음, 사용자가 이중 인증을 설정/해제하고 복구 코드를 다시 생성할 수 있는 화면을 구현해야 합니다.

> 기본적으로, 설정 파일의 `features` 배열은 이중 인증 설정 변경 전에 [비밀번호 확인](#password-confirmation) 기능이 필요하도록 지정합니다. 따라서 계속 진행하기 전에 Fortify의 비밀번호 확인 기능을 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화

이중 인증을 활성화하려면 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내면 됩니다. 성공하면 이전 URL로 리디렉션되고, 세션 변수 `status`가 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 값을 감지하여 성공 메시지를 띄울 수 있습니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

이중 인증 활성화 후에도, 사용자는 올바른 인증 코드를 입력해 "설정 완료"를 해야 하므로 성공 메시지에 반드시 안내를 포함해야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 이중 인증 구성을 마무리하세요.
    </div>
@endif
```

다음으로, 사용자가 인증 앱에 등록할 수 있도록 이중 인증용 QR 코드를 보여줘야 합니다. Blade를 사용 중이라면 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 QR 코드를 가져올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 프런트엔드라면 `/user/two-factor-qr-code` 엔드포인트로 GET(XHR) 요청해서 `svg` 키가 포함된 JSON 객체를 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인(설정 완료)

QR 코드를 보여주는 것 외에, 사용자가 인증 코드를 입력할 수 있는 텍스트 입력란을 제공해야 합니다. 이 코드는 Fortify가 정의한 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청되어야 합니다.

성공하면 이전 URL로 리디렉션되고, 세션 변수 `status`가 `two-factor-authentication-confirmed`로 바뀝니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        이중 인증이 성공적으로 확인 및 활성화되었습니다.
    </div>
@endif
```

XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

사용자의 이중 인증 복구 코드도 보여주세요. 복구 코드는 사용자가 모바일 기기에 접근하지 못할 때 인증할 수 있게 도와줍니다. Blade를 사용할 경우, 인증된 사용자 인스턴스에서 아래처럼 접근할 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프론트엔드의 경우 `/user/two-factor-recovery-codes` 엔드포인트로 GET(XHR) 요청을 보내면 복구 코드 배열이 반환됩니다.

복구 코드를 재생성하려면, `/user/two-factor-recovery-codes` 엔드포인트로 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

인증 도중 Fortify는 자동으로 사용자를 이중 인증 챌린지 화면으로 리디렉션합니다. 프론트엔드가 XHR 로그인 요청을 보낸 경우, 인증 성공 후 `two_factor` 불리언 값이 포함된 JSON 응답을 반환하므로, 이 값을 검사해 이중 인증 챌린지 화면으로 이동할지 판단해야 합니다.

이중 인증 챌린지 뷰 반환 방법을 Fortify에 알려줘야 합니다. 모든 인증 화면 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 커스터마이즈할 수 있습니다. 아래처럼 주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Fortify가 `/two-factor-challenge` 라우트를 정의해 이 뷰를 반환합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge`로 POST 요청하는 폼을 포함해야 하며, `code` 필드(유효한 TOTP 토큰) 또는 `recovery_code` 필드(복구 코드)를 포함해야 합니다.

로그인 성공 시 Fortify는 설정 파일의 `home`으로 이동하며, XHR 요청이라면 204 HTTP 응답을 반환합니다.

실패 시엔 이중 인증 챌린지 화면으로 리디렉션되고, 검증 오류는 $errors Blade 템플릿 변수 또는 422 HTTP 응답(XHR)이 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화

이중 인증을 비활성화하려면 `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내세요. 이 엔드포인트는 호출 전에 [비밀번호 확인](#password-confirmation)이 필요합니다.

<a name="registration"></a>
## 회원가입

회원가입 기능 구현을 시작하려면 Fortify에 "회원가입(register)" 뷰 반환 방법을 알려줘야 합니다. Fortify는 프론트엔드가 없는 인증 라이브러리임을 기억하세요. 이미 완성된 프론트엔드가 필요한 경우 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 추천합니다.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 다음과 같이 등록합니다:

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

Fortify는 `/register` 라우트를 관리하고, 여러분의 `register` 템플릿은 Fortify가 정의한 `/register` 엔드포인트로 POST 요청하는 폼을 포함해야 합니다.

`/register` 엔드포인트에는 문자열 `name`, 이메일/사용자명, `password`, `password_confirmation` 필드가 필요합니다. 이메일/사용자명 필드명은 `fortify` 설정 파일의 `username` 값과 일치해야 합니다.

회원가입 성공 시, 설정 파일의 `home` 옵션에 있는 URI로 리디렉션되며, XHR 요청의 경우 201 HTTP 응답이 반환됩니다.

실패 시에는 회원가입 화면으로 리디렉션되고, 검증 오류는 $errors Blade 템플릿 변수 또는 422 응답(XHR) 형태로 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

사용자 검증 및 생성 과정은 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정해 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능 구현을 위해 먼저 "비밀번호 재설정 요청(비밀번호 찾기)" 뷰 반환 방법을 Fortify에 알려줘야 합니다. Fortify는 헤드리스 인증 라이브러리라는 점을 다시 한 번 명심하세요.

모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스를 통해 조정하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 다음과 같이 정의합니다:

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

Fortify가 `/forgot-password` 엔드포인트를 관리하며, `forgot-password` 템플릿에는 `/forgot-password`로 POST 요청하는 폼이 있어야 합니다.

`/forgot-password` 엔드포인트는 문자열 `email` 필드를 기대합니다. 필드명/DB 컬럼명은 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 결과 처리

비밀번호 재설정 링크 요청이 성공하면, `/forgot-password`로 다시 리디렉션되고 사용자에게 비밀번호 재설정용 링크가 메일로 전송됩니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

성공한 뒤 `/forgot-password`로 리디렉션되면, 세션 변수 `status`를 활용해 상태 메시지를 보여줄 수 있습니다.

`$status` 세션 변수의 값은 [`passwords` 언어 파일](/docs/{{version}}/localization)에 정의된 번역 문자열 중 하나와 일치합니다. 값을 커스터마이즈하려면, 언어 파일을 Artisan의 `lang:publish`로 게시하여 수정할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패 시에는 비밀번호 재설정 요청 화면으로 돌아가며, 검증 오류는 $errors Blade 변수 또는 XHR의 경우 422 응답에 포함됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정 기능의 마무리를 위해 "비밀번호 재설정" 뷰 반환 방법을 Fortify에 알려야 합니다.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 조정합니다. 주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 다음과 같이 정의합니다:

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

Fortify가 이 뷰를 표시할 라우트를 관리하며, `reset-password` 템플릿에는 `/reset-password`로 POST 요청하는 폼이 있어야 합니다.

`/reset-password` 엔드포인트는 문자열 `email`, `password`, `password_confirmation`, 그리고 `token` 필드(값은 `request()->route('token')`)를 요구합니다. "email" 필드명/DB 컬럼명은 설정 파일의 `email`에 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 결과 처리

비밀번호 재설정 성공 시 `/login` 라우트로 리디렉션되어 사용자가 새 비밀번호로 로그인할 수 있습니다. 또한 세션 변수 `status`가 설정되므로, 로그인 화면에서 성공 메시지를 보일 수 있습니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청이라면 200 HTTP 응답이 반환됩니다.

실패 시에는 비밀번호 재설정 화면으로 이동하며, 검증 오류는 $errors Blade 변수에, XHR 요청일 경우 422 응답에 포함됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션에서 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자가 앱에 계속 접근하기 위해 이메일 주소를 인증해야 할 수 있습니다. 먼저 `fortify` 설정 파일의 `features` 배열에서 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그리고 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하는지도 확인해야 합니다.

이 두 단계를 완료하면, 새로 등록된 사용자에게 이메일 주소 인증 요청 메시지가 발송됩니다. 다만, 사용자에게 이메일 인증 화면(이메일로 발송된 인증 링크를 클릭하라는 안내)이 필요하므로 이를 Fortify에 알려야 합니다.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 다음과 같이 등록합니다:

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

Fortify가 `/email/verify` 엔드포인트에서 이 뷰를 표시하는 라우트를 정의합니다.

`verify-email` 템플릿에는 사용자가 이메일로 발송된 인증 링크를 클릭하도록 안내하는 메시지를 추가하세요.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재발송

원한다면, `verify-email` 템플릿에 `/email/verification-notification` 엔드포인트로 POST 요청을 보내는 버튼을 추가할 수 있습니다. 이 엔드포인트에 요청이 오면 사용자는 새로운 인증 링크가 포함된 이메일을 받을 수 있습니다.

재발송 요청이 성공하면, Fortify는 `/email/verify`로 사용자를 리디렉션하며 세션 변수 `status`를 전달하므로, 이를 통해 성공 메시지를 표시할 수 있습니다. XHR 요청의 경우 202 HTTP 응답이 반환됩니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새로운 이메일 인증 링크가 전송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기

특정 라우트 또는 라우트 그룹이 사용자의 이메일 인증을 요구하도록 하려면, Laravel 내장 `verified` 미들웨어를 라우트에 적용하세요. 이 미들웨어는 `App\Http\Kernel` 클래스에 등록되어 있습니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하면서 일부 액션은 사용자가 실행 전에 반드시 비밀번호를 재확인해야 할 수 있습니다. 이러한 라우트는 Laravel 내장 `password.confirm` 미들웨어로 보호하는 것이 일반적입니다.

비밀번호 확인 기능 구현을 시작하려면 Fortify에 "비밀번호 확인" 뷰 반환 방법을 알려야 합니다. Fortify는 헤드리스 인증 라이브러리임을 상기하세요. 이미 구현 완료된 인증 프론트엔드를 원하면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 사용을 고려하세요.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 다음과 같이 등록합니다:

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

Fortify가 `/user/confirm-password` 엔드포인트를 관리하고, 여러분의 `confirm-password` 템플릿에는 이 엔드포인트로 POST 요청하는 폼이 포함되어야 하며, `password`(현재 비밀번호) 필드를 가져야 합니다.

비밀번호가 사용자의 실제 비밀번호와 일치하면, Fortify는 사용자가 원래 접근하려던 라우트로 리디렉션합니다. XHR 요청의 경우 201 HTTP 응답이 반환됩니다.

실패 시에는 비밀번호 확인 화면으로 이동하며, 검증 오류는 $errors Blade 변수(또는 XHR의 경우 422 응답)로 전달됩니다.