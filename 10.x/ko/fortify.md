# Laravel Fortify

- [소개](#introduction)
    - [Fortify란 무엇인가?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 서비스 프로바이더](#the-fortify-service-provider)
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
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러들을 등록합니다. Fortify를 설치한 후에는 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스를 제공하지 않으므로, 직접 만든 UI와 함께 Fortify가 등록한 라우트에 요청을 보내는 방식으로 사용하게 됩니다. 이 문서의 나머지 부분에서 이러한 라우트에 요청하는 구체적인 방법을 다루겠습니다.

> [!NOTE]  
> Fortify는 Laravel의 인증 기능을 빠르게 구현할 수 있도록 도와주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** 필요하다면 [인증](/docs/10.x/authentication), [비밀번호 재설정](/docs/10.x/passwords), [이메일 인증](/docs/10.x/verification) 공식 문서를 참고하여 Laravel 인증 서비스를 직접 구현할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란 무엇인가?

앞서 설명한 바와 같이, Laravel Fortify는 Laravel을 위한 프론트엔드 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 꼭 Fortify를 사용할 필요는 없습니다.** 문서에서 다루는 [인증](/docs/10.x/authentication), [비밀번호 재설정](/docs/10.x/passwords), [이메일 인증](/docs/10.x/verification) 내용을 참고해 직접 구현할 수도 있습니다.

Laravel에 익숙하지 않은 경우, 먼저 [Laravel Breeze](/docs/10.x/starter-kits) 애플리케이션 스타터 킷을 살펴보는 것도 좋은 방법입니다. Breeze는 Tailwind CSS를 사용한 UI와 함께 인증 스캐폴딩을 제공합니다. Breeze는 Fortify와 달리 라우트와 컨트롤러를 애플리케이션 내부로 복사해주므로, 이를 통해 Laravel 인증 기능을 공부하고 익힐 수 있습니다. Fortify는 Breeze의 라우트와 컨트롤러를 UI 없이 패키지 형태로 제공하여, 특정 UI에 구애받지 않고 빠르게 인증 백엔드를 구현할 수 있게 해줍니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나?

Laravel Fortify를 언제 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 이미 사용하고 있다면 Fortify를 따로 설치할 필요가 없습니다. 스타터 킷에는 완전한 인증 기능이 이미 구현되어 있기 때문입니다.

만약 스타터 킷을 사용하지 않고 인증 기능이 필요한 애플리케이션을 개발 중이라면, 두 가지 선택지가 있습니다. 하나는 직접 인증 기능을 구현하는 것이고, 다른 하나는 Fortify를 설치하여 인증 기능의 백엔드 구현을 맡기는 것입니다.

Fortify를 사용하면 문서에서 설명하는 Fortify의 인증 라우트에 UI가 요청을 보내 사용자를 인증하고 등록하는 구조가 됩니다.

반면 직접 인증 서비스를 구현하려면 [인증](/docs/10.x/authentication), [비밀번호 재설정](/docs/10.x/passwords), [이메일 인증](/docs/10.x/verification) 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum 비교

일부 개발자들은 [Laravel Sanctum](/docs/10.x/sanctum)과 Laravel Fortify의 차이를 혼동합니다. 두 패키지는 관련되었지만 그 목적이 다르기에 서로 배타적이거나 경쟁 관계가 아닙니다.

Laravel Sanctum은 API 토큰 관리와 기존 사용자 인증(session 쿠키 또는 토큰 사용)에 집중합니다. Sanctum은 사용자 등록, 비밀번호 재설정 같은 라우트를 제공하지 않습니다.

API를 제공하거나 SPA(single-page application) 백엔드 인증 레이어를 직접 구현할 때는 Laravel Fortify(사용자 등록, 비밀번호 재설정 등)와 Laravel Sanctum(API 토큰 관리, 세션 인증)을 함께 사용하는 경우가 많습니다.

<a name="installation"></a>
## 설치

먼저 Composer로 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로 `vendor:publish` 명령어를 실행해 Fortify 리소스를 퍼블리시합니다:

```shell
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

이 명령어는 Fortify가 제공하는 액션들을 `app/Actions` 디렉터리에 퍼블리시합니다. 해당 디렉터리가 없으면 생성합니다. 또한 `FortifyServiceProvider`, 설정 파일, 그리고 필요한 모든 데이터베이스 마이그레이션도 퍼블리시됩니다.

이후 데이터베이스 마이그레이션을 수행하세요:

```shell
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify 서비스 프로바이더

앞서 실행한 `vendor:publish` 명령어는 `App\Providers\FortifyServiceProvider` 클래스를 퍼블리시합니다. 이 클래스를 애플리케이션의 `config/app.php` 설정 파일 내 `providers` 배열에 등록해야 합니다.

Fortify 서비스 프로바이더는 퍼블리시된 액션들을 등록하고, Fortify가 해당 작업을 수행할 때 이 액션들을 사용하도록 지시합니다.

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일 내에는 `features` 배열이 있습니다. 이 배열은 Fortify가 기본으로 노출할 백엔드 라우트 및 기능들을 정의합니다. 만약 Fortify를 [Laravel Jetstream](https://jetstream.laravel.com)과 함께 사용하지 않는다면, 보통 대부분 Laravel 애플리케이션에서 사용하는 기본 인증 기능인 다음 기능들만 활성화할 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면, 회원가입 화면처럼 뷰를 반환하는 라우트를 정의합니다. 그러나 자바스크립트 기반 SPA(single-page application)를 빌드한다면 이러한 라우트가 필요 없을 수 있습니다. 이 경우 `config/fortify.php` 설정 파일에서 `views` 값을 `false`로 설정하여 뷰 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화와 비밀번호 재설정

만약 Fortify의 뷰 라우트를 비활성화하고 비밀번호 재설정 기능을 구현할 예정이라면, 애플리케이션 내에 `password.reset`라는 이름의 라우트를 반드시 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 이 라우트를 통해 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

먼저 Fortify에 로그인 페이지를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리임을 기억하세요. 미리 완성된 Laravel 인증 UI를 원한다면 [애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 사용하세요.

인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드를 사용해 모두 커스터마이징할 수 있습니다. 보통은 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 이 메서드를 호출합니다. 그러면 Fortify가 해당 뷰를 반환하는 `/login` 라우트를 정의해줍니다:

```
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

로그인 템플릿에는 POST 방식으로 `/login`에 요청하는 폼이 있어야 합니다. `/login` 라우트는 문자열 타입의 `email` 또는 `username` 필드와 `password` 필드를 기대합니다. `email` 또는 `username` 필드 이름은 `config/fortify.php` 내 `username` 설정값과 일치해야 합니다. 추가로, 사용자가 "기억하기" 기능을 켜길 원한다면 불리언 `remember` 필드를 전달할 수 있습니다.

로그인 시도가 성공하면, Fortify는 애플리케이션의 `fortify` 설정 파일 내 `home` 옵션에서 지정한 URI로 리디렉션합니다. 만약 XHR 요청이라면 200 HTTP 응답을 반환합니다.

로그인 시도가 실패하면 사용자는 로그인 화면으로 되돌아가며, 유효성 검증 오류 메시지가 `$errors` [Blade 템플릿 변수](/docs/10.x/validation#quick-displaying-the-validation-errors)를 통해 제공됩니다. XHR 요청인 경우 422 HTTP 응답과 함께 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 전달된 자격증명(credentials)과 애플리케이션에 설정된 인증 가드를 이용해 사용자를 조회하고 인증합니다. 하지만 경우에 따라 로그인 자격증명을 인증하고 관련 사용자를 조회하는 과정을 완전히 직접 커스터마이징하고 싶을 수 있습니다. 다행히도 Fortify는 `Fortify::authenticateUsing` 메서드로 이를 쉽게 구현할 수 있습니다.

이 메서드는 HTTP 요청을 파라미터로 받아, 요청 정보로 로그인 자격증명 검증 후 해당 사용자 인스턴스를 반환하는 클로저를 받습니다. 자격증명이 올바르지 않거나 사용자를 찾을 수 없으면 `null` 또는 `false`를 반환해야 합니다. 일반적으로 이 메서드는 `FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

Fortify가 사용하는 인증 가드는 `fortify` 설정 파일에서 커스터마이징할 수 있습니다. 단, 설정하는 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard`를 구현해야 합니다. SPA 인증용으로 Fortify를 사용하는 경우 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 함께 사용해야 합니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 여러 개의 호출 가능한(invokable) 클래스가 연결된 파이프라인으로 처리합니다. 필요하다면, 로그인 요청 시 거쳐야 할 클래스의 커스텀 파이프라인을 정의할 수 있습니다. 각 클래스는 `__invoke` 메서드를 가지며 `Illuminate\Http\Request` 인스턴스와 다음 클래스로 요청을 넘기기 위한 `$next` 변수를 받습니다. 이는 Laravel 미들웨어와 비슷한 방식입니다.

커스텀 파이프라인은 `Fortify::authenticateThrough` 메서드를 사용해 정의하며, 이 메서드는 로그인 요청 처리에 통과할 클래스 배열을 반환하는 클로저를 받습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

아래 예시는 기본 파이프라인 설정으로, 커스터마이징의 출발점으로 활용할 수 있습니다:

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

로그인 성공 시 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. 로그인 요청이 XHR인 경우 200 HTTP 응답을 반환하며, 로그아웃 후에는 `/` URI로 리디렉션됩니다.

이 동작을 좀 더 세밀하게 제어하려면 `LoginResponse`와 `LogoutResponse` 계약(인터페이스)의 구현체를 Laravel [서비스 컨테이너](/docs/10.x/container)에 바인딩하면 됩니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드에서 처리합니다:

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
## 이중 인증 (Two Factor Authentication)

Fortify의 이중 인증 기능을 활성화하면, 인증 과정 중 사용자는 6자리 숫자의 토큰을 입력해야 합니다. 이 토큰은 시간 기반 일회용 비밀번호(TOTP) 알고리즘을 사용해 생성되며, Google Authenticator 같은 TOTP 호환 모바일 앱에서 받아볼 수 있습니다.

시작하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하고 있는지 확인하세요:

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

다음으로, 사용자가 이중 인증 설정을 관리할 수 있는 화면을 만드세요. 이 화면에서는 사용자가 이중 인증을 켜고 끄거나 복구 코드를 재생성할 수 있어야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에서 Fortify의 이중 인증 설정은 변경 전에 비밀번호 확인을 요구하도록 지정되어 있습니다. 따라서, [비밀번호 확인](#password-confirmation) 기능을 애플리케이션에 구현한 뒤 진행하는 것이 좋습니다.

<a name="enabling-two-factor-authentication"></a>
### 이중 인증 활성화

이중 인증을 활성화하려면 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트에 POST 요청을 보내야 합니다. 요청이 성공하면 이전 URL로 리디렉션되며, 세션 변수 `status`에 `two-factor-authentication-enabled`가 설정됩니다. 이 세션 변수를 템플릿에서 확인해 성공 메시지를 표시할 수 있습니다. XHR 요청이었다면 200 HTTP 응답을 반환합니다.

이중 인증 활성화 후에도 사용자는 유효한 이중 인증 코드를 입력해 설정을 "확인(confirm)"해야 합니다. 따라서 성공 메시지에는 아직 이중 인증 확인 과정이 필요하다는 안내를 포함해야 합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 이중 인증 설정을 마무리해 주세요.
    </div>
@endif
```

다음으로, 사용자가 인증 앱에서 QR 코드를 스캔할 수 있도록 QR 코드를 표시해야 합니다. Blade 뷰라면, 인증 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드를 호출해 QR 코드 SVG를 얻을 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 기반 프론트엔드를 구축 중이라면 `/user/two-factor-qr-code` 엔드포인트에 GET XHR 요청을 보내 QR 코드 데이터를 JSON 형식으로 받아올 수 있습니다. 이 엔드포인트는 `svg` 키를 포함한 JSON 객체를 반환합니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인

QR 코드와 함께 사용자가 이중 인증 설정을 “확인”할 수 있도록 유효한 인증 코드를 입력하는 텍스트 입력란도 제공해야 합니다. 이 코드는 `/user/confirmed-two-factor-authentication` 엔드포인트에 POST 요청으로 전달됩니다.

요청이 성공하면 이전 URL로 리디렉션되고 세션 변수 `status`에는 `two-factor-authentication-confirmed`가 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        이중 인증이 확인되었으며 성공적으로 활성화되었습니다.
    </div>
@endif
```

XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

또한 사용자의 이중 인증 복구 코드를 보여줘야 합니다. 이 코드는 사용자가 휴대기기를 잃어버렸을 때 인증하는 데 사용됩니다. Blade 뷰에서는 현재 인증된 사용자 인스턴스에서 복구 코드를 배열 형태로 얻을 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프론트엔드라면 `/user/two-factor-recovery-codes` 엔드포인트에 GET XHR 요청을 보내 복구 코드 배열을 JSON으로 받을 수 있습니다.

복구 코드는 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청하여 재생성할 수도 있습니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 이중 인증으로 인증하기

Fortify의 이중 인증 기능이 활성화된 경우, 인증 과정에서 자동으로 애플리케이션의 이중 인증 챌린지 화면으로 리디렉션됩니다. 다만, 로그인 요청이 XHR인 경우 성공 응답에 `two_factor`라는 불리언 속성이 포함된 JSON 객체가 포함됩니다. 이 값을 검사해 사용자에게 이중 인증 챌린지 화면으로 리디렉트할지 여부를 판단해야 합니다.

이중 인증 챌린지 뷰를 반환하도록 Fortify에 알려주는 작업부터 시작합니다. Fortify의 모든 인증 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스 메서드를 통해 커스터마이징할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify는 `/two-factor-challenge` 라우트를 정의해 이 뷰를 반환합니다. `two-factor-challenge` 뷰 템플릿에는 POST 방식으로 `/two-factor-challenge` 엔드포인트에 요청하는 폼이 있어야 하며, `code` 필드에 유효한 TOTP 토큰 혹은 `recovery_code` 필드에 복구 코드 중 하나를 받아야 합니다.

로그인 시도가 성공하면 Fortify는 `fortify` 설정 파일 내 `home` 옵션의 URI로 리디렉션합니다. XHR 요청의 경우 204 HTTP 응답을 반환합니다.

실패할 경우 사용자에게 다시 이중 인증 도전 화면으로 돌아가게 하며, 유효성 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/10.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청이라면 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 이중 인증 비활성화

이중 인증을 비활성화하려면, 애플리케이션에서 `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내야 합니다. Fortify의 이중 인증 라우트들은 호출 전에 [비밀번호 확인](#password-confirmation)을 요구하므로 이를 구현해 두어야 합니다.

<a name="registration"></a>
## 회원가입

애플리케이션 회원가입 기능을 구현하려면 먼저 Fortify에게 회원가입 뷰를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리입니다. 완성된 인증 UI를 쓰고 싶으면 [애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 사용하세요.

모든 Fortify 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스 메서드를 통해 커스터마이징할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify는 해당 뷰를 반환하는 `/register` 라우트를 정의합니다. `register` 뷰에는 Fortify가 정의한 `/register` 엔드포인트에 POST 방식 요청을 보내는 폼이 포함되어야 합니다.

`/register` 엔드포인트는 문자열인 `name`, 이메일 주소 또는 사용자명, `password`, `password_confirmation` 필드를 기대합니다. 이메일 또는 사용자명 필드 이름은 애플리케이션의 `fortify` 설정 파일 내 `username` 값과 일치해야 합니다.

회원가입이 성공하면 Fortify는 설정된 `home` URI로 리디렉션하거나 XHR 요청일 경우 201 HTTP 응답을 반환합니다.

요청이 실패하면 회원가입 화면으로 다시 이동하며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/10.x/validation#quick-displaying-the-validation-errors)에서 확인할 수 있습니다. XHR 요청이면 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

사용자 검증과 생성 과정은 Fortify 설치 시 자동 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정해 커스터마이징할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

애플리케이션 비밀번호 재설정 기능을 구현하려면 먼저 Fortify에 "비밀번호 분실" 뷰를 반환하는 방법을 알려야 합니다. Fortify는 UI가 없는 인증 라이브러리임을 기억하세요. 미리 완성된 인증 UI를 원하면 [애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 사용하세요.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스 메서드로 모두 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify는 `/forgot-password` 엔드포인트를 정의해 이 뷰를 반환합니다. `forgot-password` 뷰에는 POST 방식으로 `/forgot-password`에 요청하는 폼이 있어야 합니다.

`/forgot-password` 엔드포인트는 문자열 `email` 필드를 기대하며, 이 필드 이름과 데이터베이스 컬럼 이름은 `fortify` 설정 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면 Fortify는 `/forgot-password` 경로로 리디렉션하며, 사용자에게 안전한 비밀번호 재설정 링크가 포함된 메일을 발송합니다. XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

성공적으로 리디렉션된 후에는 `status` 세션 변수를 이용해 요청 결과 상태를 화면에 표시 가능합니다.

`$status` 세션 변수 값은 애플리케이션의 `passwords` [언어 파일](/docs/10.x/localization)에 정의된 번역 문자열 중 하나입니다. 만약 Laravel 언어 파일을 아직 퍼블리시하지 않았다면 `lang:publish` Artisan 명령어로 퍼블리시할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

요청이 실패할 경우 비밀번호 재설정 링크 요청 화면으로 돌아가며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/10.x/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청이라면 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정 기능을 마무리하려면 Fortify에게 "비밀번호 재설정" 뷰를 반환하는 방법을 알려야 합니다.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스 메서드로 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify는 이 뷰를 반환하는 라우트를 정의합니다. `reset-password` 뷰에는 POST 방식으로 `/reset-password`에 요청하는 폼을 포함해야 합니다.

`/reset-password` 엔드포인트는 `email`(문자열), `password`, `password_confirmation` 필드 및 숨겨진 필드 `token`(값은 `request()->route('token')`)을 기대합니다. 이메일 필드 이름과 데이터베이스 컬럼명은 `fortify` 설정 파일 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 사용자가 새 비밀번호로 로그인하도록 `/login` 경로로 리디렉션합니다. 이와 함께 성공 상태를 표시하기 위한 `status` 세션 변수도 설정됩니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청인 경우 200 HTTP 응답을 반환합니다.

요청이 실패하면 비밀번호 재설정 화면으로 돌아가며, 검증 오류는 `$errors` [Blade 템플릿 변수](/docs/10.x/validation#quick-displaying-the-validation-errors)를 통해 확인 가능합니다. XHR 요청 시 422 HTTP 응답과 함께 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 Fortify 설치 시 자동 생성된 `App\Actions\ResetUserPassword` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자가 애플리케이션을 계속 이용하기 전에 이메일 주소를 인증하도록 요구할 수 있습니다. 이를 위해 먼저 `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그다음 사용자 모델인 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하는지 확인해야 합니다.

이 두 설정이 완료되면 새로 등록된 사용자들에게 이메일 소유권 인증 메일이 전송됩니다. 그러나 사용자에게 이메일 인증 링크를 누르도록 안내하는 인증 화면도 Fortify에 알려줘야 합니다.

Fortify의 모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스 메서드를 통해 커스터마이징 가능하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify는 Laravel 내장 `verified` 미들웨어가 `/email/verify` 엔드포인트로 리디렉션할 때 이 뷰를 반환하는 라우트를 정의합니다.

`verify-email` 템플릿에는 사용자에게 이메일로 전송된 인증 링크를 클릭하라는 안내 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

필요하다면, `verify-email` 뷰에 POST 방식으로 `/email/verification-notification` 엔드포인트에 요청하는 버튼을 추가할 수 있습니다. 이 엔드포인트에 요청이 들어오면 새 이메일 인증 링크가 사용자에게 발송됩니다. 이전 링크를 실수로 삭제했거나 분실했을 때 유용합니다.

인증 링크 재전송 요청이 성공하면 Fortify는 `/email/verify`로 리디렉션하며, 상태를 알리는 `status` 세션 변수를 설정합니다. 이를 통해 성공 메시지를 사용자에게 보여줄 수 있습니다. XHR 요청일 경우 202 HTTP 응답이 반환됩니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새로운 이메일 인증 링크가 이메일로 전송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호

특정 라우트나 라우트 그룹에 대해 이메일 인증을 완료한 사용자만 접근하도록 제한하려면, Laravel 내장 `verified` 미들웨어를 해당 라우트에 적용하세요. 이 미들웨어는 애플리케이션의 `App\Http\Kernel` 클래스에 등록되어 있습니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하다 보면, 특정 작업 수행 전 사용자가 비밀번호를 재확인하도록 요구하는 경우가 있습니다. 보통 이 라우트들은 Laravel 내장 `password.confirm` 미들웨어로 보호합니다.

비밀번호 확인 기능을 구현하려면 먼저 Fortify가 "비밀번호 확인" 뷰를 반환하는 방법을 알아야 합니다. Fortify는 UI가 없는 라이브러리임을 기억하세요. 완성된 인증 UI가 필요하면 [애플리케이션 스타터 킷](/docs/10.x/starter-kits)을 사용하세요.

Fortify의 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스 메서드를 통해 자유롭게 커스터마이징할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify는 `/user/confirm-password` 엔드포인트를 정의해 이 뷰를 반환합니다. `confirm-password` 뷰에는 `/user/confirm-password`에 POST 방식으로 요청하는 폼이 포함되어야 하며, 이 엔드포인트는 사용자의 현재 비밀번호가 담긴 `password` 필드를 기대합니다.

비밀번호가 올바르면 Fortify는 사용자가 원래 접근하려던 라우트로 리디렉션합니다. XHR 요청인 경우 201 HTTP 응답이 반환됩니다.

요청이 실패하면 비밀번호 확인 화면으로 돌아가며, 검증 오류는 공유된 `$errors` Blade 템플릿 변수를 통해 확인할 수 있습니다. XHR 요청 시 422 HTTP 응답과 함께 오류가 반환됩니다.