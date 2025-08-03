# Laravel Fortify (Laravel Fortify)

- [소개](#introduction)
    - [Fortify란 무엇인가?](#what-is-fortify)
    - [언제 Fortify를 사용해야 하나?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 서비스 프로바이더](#the-fortify-service-provider)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 맞춤화](#customizing-user-authentication)
    - [인증 파이프라인 맞춤화](#customizing-the-authentication-pipeline)
    - [리다이렉션 맞춤화](#customizing-authentication-redirects)
- [2단계 인증](#two-factor-authentication)
    - [2단계 인증 활성화](#enabling-two-factor-authentication)
    - [2단계 인증으로 로그인하기](#authenticating-with-two-factor-authentication)
    - [2단계 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 맞춤화](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 맞춤화](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호하기](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프런트엔드 독립 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후 `route:list` Artisan 명령어를 실행하면 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체적인 사용자 인터페이스(UI)를 제공하지 않으므로, 여러분의 사용자 인터페이스가 Fortify가 등록한 라우트에 요청을 보낼 수 있도록 하도록 설계되었습니다. 이 문서 뒷부분에서 이러한 라우트에 요청을 보내는 방법을 자세히 다루겠습니다.

> [!TIP]
> Fortify는 Laravel의 인증 기능을 구현하는 데 도움을 주는 패키지입니다. **사용할 의무는 없습니다.** 언제든지 [authentication](/docs/{{version}}/authentication), [password reset](/docs/{{version}}/passwords), [email verification](/docs/{{version}}/verification) 문서를 참고하여 직접 인증 서비스를 구현할 수 있습니다.

<a name="what-is-fortify"></a>
### Fortify란 무엇인가?

앞서 언급한 대로, Laravel Fortify는 Laravel을 위한 프런트엔드 독립 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 Fortify를 반드시 사용할 필요는 없습니다.** 언제든지 [authentication](/docs/{{version}}/authentication), [password reset](/docs/{{version}}/passwords), [email verification](/docs/{{version}}/verification) 문서를 참고하여 직접 인증 서비스를 구현할 수 있습니다.

Laravel에 익숙하지 않은 사용자라면, Laravel Fortify를 사용하기 전에 [Laravel Breeze](/docs/{{version}}/starter-kits) 애플리케이션 스타터 키트를 먼저 살펴보는 것을 권장합니다. Laravel Breeze는 [Tailwind CSS](https://tailwindcss.com)로 구축된 UI를 포함한 인증 스캐폴딩을 제공합니다. Fortify와 달리 Breeze는 라우트와 컨트롤러를 직접 애플리케이션에 퍼블리시합니다. 이를 통해 Laravel 인증 기능을 직접 공부하고 익힐 수 있습니다.

Laravel Fortify는 본질적으로 Laravel Breeze의 라우트와 컨트롤러를 UI가 없는 패키지 형태로 제공합니다. 덕분에 특정 프런트엔드 기술에 얽매이지 않고도 애플리케이션의 인증 백엔드를 빠르게 구성할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### 언제 Fortify를 사용해야 하나?

언제 Laravel Fortify를 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우 Fortify를 설치할 필요가 없습니다. 왜냐하면 스타터 키트들은 모두 완전한 인증 기능을 이미 제공하기 때문입니다.

만약 스타터 키트를 사용하지 않고 애플리케이션에 인증 기능이 필요하다면, 두 가지 옵션이 있습니다: 직접 인증 기능을 구현하거나 Laravel Fortify를 사용하여 인증 백엔드를 제공하는 것입니다.

Fortify를 설치하면, 여러분의 사용자 인터페이스는 이 문서에서 설명하는 Fortify의 인증 라우트에 요청을 보내 사용자 인증 및 회원가입을 수행합니다.

반대로 Fortify를 사용하지 않고 Laravel 인증 서비스를 직접 사용하고 싶다면, [authentication](/docs/{{version}}/authentication), [password reset](/docs/{{version}}/passwords), [email verification](/docs/{{version}}/verification) 문서를 참고해 수동으로 구현할 수 있습니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify & Laravel Sanctum

Laravel Sanctum과 Laravel Fortify의 차이점이 혼동되는 경우가 종종 있습니다. 두 패키지는 서로 다른, 그러나 관련된 문제를 해결하기 때문에 경쟁하지 않으며 병행해서 사용할 수 있습니다.

Laravel Sanctum은 API 토큰 관리와 세션 쿠키 또는 토큰을 이용한 기존 사용자 인증에 집중합니다. Sanctum은 사용자 회원가입, 비밀번호 재설정 등의 라우트를 제공하지 않습니다.

API를 제공하거나 SPA(단일 페이지 애플리케이션)의 백엔드로서 인증 레이어를 구축한다면, Laravel Fortify(회원가입, 비밀번호 재설정 등)와 Laravel Sanctum(API 토큰 관리, 세션 인증)을 함께 사용하는 경우가 많습니다.

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 관리자를 사용해 Fortify를 설치하세요:

```nothing
composer require laravel/fortify
```

다음으로, `vendor:publish` 명령어를 사용해 Fortify 리소스를 퍼블리시합니다:

```bash
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

이 명령은 Fortify의 액션들을 `app/Actions` 디렉토리에 퍼블리시하며, 이 디렉토리가 없다면 새로 생성됩니다. 또한 Fortify의 설정 파일과 마이그레이션도 함께 퍼블리시됩니다.

마지막으로 데이터베이스 마이그레이션을 수행하세요:

```bash
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify 서비스 프로바이더

위의 `vendor:publish` 명령어는 `App\Providers\FortifyServiceProvider` 클래스도 함께 퍼블리시합니다. 이 클래스가 애플리케이션의 `config/app.php` 설정 파일 내 `providers` 배열에 등록되어 있는지 반드시 확인하세요.

Fortify 서비스 프로바이더는 Fortify가 퍼블리시한 액션들을 등록하며, 각 작업을 Fortify가 실행할 때 이 액션들을 사용하도록 지시합니다.

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일 내에는 `features` 배열이 있습니다. 이 배열은 기본적으로 Fortify가 어떤 백엔드 라우트 및 기능을 노출할지 정의합니다. 만약 Fortify를 [Laravel Jetstream](https://jetstream.laravel.com)과 함께 사용하지 않는다면, 대부분의 Laravel 애플리케이션이 제공하는 기본 인증 기능만 활성화하기를 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면, 회원가입 화면처럼 뷰를 반환하는 목적의 라우트를 정의합니다. 하지만 JavaScript 기반 싱글 페이지 애플리케이션(SPA)을 만든다면 이 라우트들이 필요 없을 수 있습니다. 이런 경우 `config/fortify.php` 설정 파일 내 `views` 설정값을 `false`로 바꿔서 해당 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화 및 비밀번호 재설정

Fortify의 뷰를 비활성화하고 비밀번호 재설정 기능을 구현할 경우, 애플리케이션 내에 `password.reset` 이름의 라우트를 반드시 정의해야 합니다. 이유는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 `password.reset` 명명된 라우트에서 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

시작하려면 Fortify에게 로그인 뷰를 어떻게 반환할지 알려줘야 합니다. Fortify는 헤드리스(프런트엔드가 없는) 인증 라이브러리입니다. 이미 완성된 Laravel 인증 기능 프런트엔드를 원한다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 것이 좋습니다.

Fortify의 모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스가 제공하는 적절한 메서드로 맞춤화할 수 있습니다. 일반적으로 이는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다. 그러면 Fortify가 `/login` 경로를 등록하여 해당 뷰를 반환합니다:

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

로그인 템플릿은 `/login`으로 POST 요청을 보내는 폼을 포함해야 합니다. `/login` 엔드포인트는 문자열형 `email` 또는 `username` 필드와 `password` 필드를 기대합니다. `email` / `username` 필드의 이름은 `config/fortify.php` 설정 파일 내의 `username` 값과 일치해야 합니다. 추가로 `remember`라는 불리언 필드를 포함할 수 있으며, 이는 Laravel이 제공하는 "remember me" 기능을 사용하고자 함을 의미합니다.

로그인 시도가 성공하면 Fortify는 `fortify` 설정 파일 내 `home` 설정값에 지정된 URI로 리다이렉트합니다. 요청이 XHR인 경우 200 HTTP 응답이 반환됩니다.

로그인 시도가 실패하면 로그인 화면으로 다시 리다이렉트되며, 검증 오류 내용은 공유된 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR인 경우에는 422 HTTP 응답과 함께 검증 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 맞춤화

Fortify는 제공된 자격 증명과 애플리케이션에 설정된 인증 가드를 바탕으로 자동으로 사용자를 조회하고 인증합니다. 하지만 때때로 로그인 자격 증명 검증과 사용자 조회 과정을 완전히 맞춤화할 필요가 있을 수 있습니다. Fortify는 `Fortify::authenticateUsing` 메서드를 통해 이 작업을 쉽고 유연하게 할 수 있도록 지원합니다.

이 메서드는 HTTP 요청을 인자로 받는 클로저를 받습니다. 클로저 내부에서 로그인 자격 증명 유효성을 검사하고 해당 사용자를 반환해야 합니다. 자격 증명이 부적절하거나 사용자를 찾지 못하면 `null` 또는 `false`를 반환해야 합니다. 보통 이 메서드는 `FortifyServiceProvider` 클래스의 `boot` 메서드 안에서 호출합니다:

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

Fortify가 사용할 인증 가드는 `fortify` 설정 파일에서 맞춤화할 수 있습니다. 다만, 설정되는 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스를 구현해야 합니다. SPA 인증용으로 Fortify를 사용하는 경우 Laravel 기본 `web` 가드를 [Laravel Sanctum](https://laravel.com/docs/sanctum)과 함께 사용하는 것이 권장됩니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 맞춤화

Laravel Fortify는 로그인 요청을 다루기 위해 호출 가능한(invokable) 클래스들의 파이프라인을 사용합니다. 원한다면 로그인 요청이 처리될 클래스들의 커스텀 파이프라인을 정의할 수 있습니다. 각 클래스는 HTTP 요청 인스턴스인 `Illuminate\Http\Request`와 다음 클래스에게 요청을 전달할 `$next` 인자를 받는 `__invoke` 메서드를 구현해야 하며, 이는 미들웨어와 유사합니다.

커스텀 파이프라인을 정의하려면 `Fortify::authenticateThrough` 메서드를 사용합니다. 이 메서드는 로그인 요청에 사용할 클래스 배열을 반환하는 클로저를 인자로 받습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다.

아래 예시는 기본 파이프라인 정의로, 이를 참고해 수정할 수 있습니다:

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
### 리다이렉션 맞춤화

로그인 성공 시 Fortify는 애플리케이션 `fortify` 설정 파일 내 `home` 옵션에 정의된 URI로 리다이렉트합니다. 요청이 XHR인 경우 200 HTTP 응답이 반환됩니다. 사용자가 로그아웃하면 `/` URI로 리다이렉트됩니다.

이 동작을 세밀하게 맞춤화해야 할 경우, Laravel [서비스 컨테이너](/docs/{{version}}/container)에 `LoginResponse`, `LogoutResponse` 계약의 구현체를 바인딩할 수 있습니다. 보통 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드 내에서 다음처럼 정의합니다:

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
## 2단계 인증

Fortify의 2단계 인증 기능이 활성화되면, 사용자는 로그인 시 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 TOTP(Time-based One-Time Password) 방식으로 생성되며, Google Authenticator 같은 호환 앱에서 확인할 수 있습니다.

시작하려면, 애플리케이션 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하는지 확인하세요:

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

그 다음, 사용자가 자신의 2단계 인증 설정을 관리할 수 있는 화면을 만들어야 합니다. 이 화면에서는 2단계 인증 활성화/비활성화 및 복구 코드 재생성 기능을 제공해야 합니다.

> 기본적으로 `fortify` 설정 파일 `features` 배열 내 2단계 인증 기능은 변경 전 비밀번호 확인을 요구합니다. 따라서 Fortify의 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현하는 것이 좋습니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화

2단계 인증을 활성화하려면, `/user/two-factor-authentication` 엔드포인트에 POST 요청을 보내세요. 요청이 성공하면 사용자 브라우저는 이전 URL로 리다이렉트되고, `status` 세션 변수는 `two-factor-authentication-enabled`로 설정됩니다. 템플릿 내에서 이 값을 체크해 성공 메시지를 표시할 수 있습니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm text-green-600">
        Two factor authentication has been enabled.
    </div>
@endif
```

이어서 사용자가 자신의 인증 앱으로 스캔할 수 있도록 2단계 인증 QR 코드를 표시해야 합니다. Blade를 사용할 경우, 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드를 통해 SVG 형태의 QR 코드를 얻을 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

JavaScript 프런트엔드라면 `/user/two-factor-qr-code` 엔드포인트에 GET XHR 요청을 보내 QR 코드를 JSON 형태로 받아올 수 있습니다. 이 응답은 `svg` 키를 포함합니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시하기

사용자는 자신의 2단계 인증 복구 코드를 반드시 확인할 수 있어야 합니다. 복구 코드는 모바일 기기에 접근할 수 없을 때 인증할 수 있도록 도와줍니다. Blade를 사용할 경우, 인증된 유저 인스턴스의 `recoveryCodes()` 메서드로 복구 코드 배열을 얻을 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

JavaScript 프런트엔드라면 `/user/two-factor-recovery-codes` 엔드포인트에 GET XHR 요청을 보내 JSON 배열로 복구 코드를 받아올 수 있습니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청을 보내세요.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 로그인하기

로그인 과정에서 Fortify는 자동으로 사용자를 2단계 인증 도전 화면으로 리다이렉트합니다. 하지만 XHR을 통한 로그인 요청에서는, 성공 시 반환되는 JSON 응답에 `two_factor` 불리언 속성이 포함됩니다. 이 값을 확인하여 2단계 인증 화면으로 리다이렉트할지 판단해야 합니다.

2단계 인증 도전 뷰를 반환하는 방법을 Fortify에 알려줘야 합니다. Fortify의 인증 뷰 렌더링 로직도 `Laravel\Fortify\Fortify` 클래스의 메서드로 맞춤화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 다음과 같이 호출합니다:

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

Fortify는 `/two-factor-challenge` 라우트를 정의하며 이 뷰를 반환합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge` 엔드포인트로 POST 요청을 보내는 폼이 포함되어야 합니다. 이 POST 요청은 유효한 TOTP 토큰이 담긴 `code` 필드나 사용자의 복구 코드 중 하나가 담긴 `recovery_code` 필드를 기대합니다.

로그인 시도가 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청이라면 204 HTTP 응답을 반환합니다.

로그인 실패 시에는 두 단계 인증 도전 화면으로 리다이렉트되며, 검증 오류 내용은 공유된 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 확인 가능합니다. XHR인 경우엔 422 HTTP 오류와 함께 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화

2단계 인증을 비활성화하려면 Fortify의 2단계 인증 엔드포인트인 `/user/two-factor-authentication`에 DELETE 요청을 보내세요. Fortify의 2단계 인증 관련 엔드포인트는 호출 전에 [비밀번호 확인](#password-confirmation)이 필요하다는 점을 기억하세요.

<a name="registration"></a>
## 회원가입

애플리케이션 회원가입 기능 구현을 시작하려면 Fortify에게 "회원가입" 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 헤드리스 인증 라이브러리입니다. 완성된 Laravel 인증 프런트엔드를 원한다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 맞춤화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

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

Fortify는 `/register` 라우트를 정의하고 이 뷰를 반환합니다. `register` 템플릿에는 Fortify가 정의한 `/register` 엔드포인트에 POST 요청을 보내는 폼을 포함해야 합니다.

`/register`는 문자열 타입 `name`, 이메일 주소 또는 사용자명, `password`, `password_confirmation` 필드를 기대합니다. 이메일/사용자명 필드 이름은 `fortify` 설정 파일의 `username` 값과 일치해야 합니다.

회원가입에 성공하면, Fortify는 `fortify` 설정 파일 내 `home` 설정값으로 리다이렉트합니다. 요청이 XHR이면 200 HTTP 응답이 반환됩니다.

회원가입에 실패하면, 사용자에게 다시 회원가입 화면으로 리다이렉트하며 검증 오류 내용이 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 제공됩니다. XHR 요청 시 검증 오류는 422 HTTP 응답과 함께 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 맞춤화

사용자 유효성 검증 및 생성 로직은 Laravel Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정하여 맞춤화할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능 구현을 시작하려면 Fortify에게 "비밀번호 찾기" 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 헤드리스 인증 라이브러리입니다. 완성된 Laravel 인증 프런트엔드를 원한다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 맞춤화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

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

Fortify는 `/forgot-password` 엔드포인트를 정의하며 이 뷰를 반환합니다. `forgot-password` 템플릿은 `/forgot-password` 엔드포인트에 POST 요청을 보내는 폼을 포함해야 합니다.

`/forgot-password` 엔드포인트는 문자열형 `email` 필드를 기대합니다. 이 필드의 이름과 데이터베이스 컬럼은 `fortify` 설정 파일 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면 Fortify는 사용자에게 다시 `/forgot-password` 페이지로 리다이렉트하며, 비밀번호 재설정 링크가 포함된 이메일을 전송합니다. 요청이 XHR인 경우 200 HTTP 응답이 반환됩니다.

리다이렉션 후, `status` 세션 변수로 비밀번호 재설정 링크 요청 상태를 표시할 수 있습니다. 이 세션 값은 해당 애플리케이션의 `passwords` [언어 파일](/docs/{{version}}/localization)에 정의된 문자열과 일치합니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

요청이 실패하면 다시 비밀번호 재설정 링크 요청 화면으로 리다이렉트되며, 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 읽을 수 있습니다. XHR인 경우 422 HTTP 응답과 함께 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정 기능을 마무리하려면 Fortify에게 "비밀번호 재설정" 뷰를 반환하는 방법을 알려줘야 합니다.

모든 비밀번호 재설정 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스 메서드로 맞춤 가능하며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

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

Fortify는 해당 뷰를 반환하는 라우트를 정의합니다. `reset-password` 템플릿에는 `/reset-password` 엔드포인트에 POST 요청을 보내는 폼이 포함되어야 합니다.

`/reset-password` 엔드포인트는 문자열형 `email` 필드, `password`, `password_confirmation` 필드, 그리고 `request()->route('token')` 값이 담긴 숨김 필드 `token`을 기대합니다. "email" 필드와 데이터베이스 컬럼명은 `fortify` 설정 파일 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 `/login` 라우트로 리다이렉트하며, 로그인 화면에서 성공 상태를 표시할 수 있도록 `status` 세션 변수를 설정합니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

요청이 XHR이라면 200 HTTP 응답이 반환됩니다.

요청에 실패하면 비밀번호 재설정 화면으로 리다이렉트되며, 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 볼 수 있습니다. XHR인 경우 422 HTTP 응답과 함께 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 맞춤화

비밀번호 재설정 과정은 Laravel Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정하여 맞춤화할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후, 사용자가 애플리케이션에 계속 접근하기 전에 이메일 주소를 인증하도록 요구할 수 있습니다. 시작하려면 `fortify` 설정 파일 내 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하고, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

이 두 단계를 완료하면, 신규 가입자에게 이메일 소유권을 인증하라는 안내 이메일이 전송됩니다. 하지만 Fortify에 이메일 인증 화면을 어떻게 표시할지 알려줘야 합니다. 이 뷰도 `Laravel\Fortify\Fortify` 클래스의 메서드로 맞춤화할 수 있으며, 보통 `App\Providers\FortifyServiceProvider` 클래스 `boot` 메서드 내에서 호출합니다:

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

Fortify는 Laravel 내장 `verified` 미들웨어에 의해 `/email/verify` 엔드포인트에 리다이렉트 시 해당 뷰를 표시하는 라우트를 정의합니다.

`verify-email` 템플릿에는 이메일 인증 링크를 클릭하라는 안내 문구를 포함하세요.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

원한다면, `verify-email` 템플릿에 `/email/verification-notification` 엔드포인트에 POST 요청을 보내는 버튼을 추가할 수 있습니다. 이 엔드포인트는 새 인증 이메일 링크를 사용자에게 전송하며, 이전 링크를 잃어버렸거나 삭제했을 때 새 링크를 받을 수 있도록 합니다.

이 링크 재전송 요청이 성공하면 Fortify는 사용자를 `/email/verify`로 리다이렉트하고 `status` 세션 변수를 설정합니다. 이를 통해 해당 작업이 성공했다는 정보를 사용자에게 알릴 수 있습니다. XHR 요청의 경우 202 HTTP 응답이 반환됩니다:

```html
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기

라우트 또는 라우트 그룹이 사용자의 이메일 인증을 요구하도록 하려면 Laravel 내장 `verified` 미들웨어를 라우트에 붙이세요. 이 미들웨어는 애플리케이션의 `App\Http\Kernel` 클래스에 등록되어 있습니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하다 보면, 종종 사용자가 특정 작업을 수행하기 전에 비밀번호를 다시 확인하도록 요구해야 하는 경우가 있습니다. 보통 이러한 라우트는 Laravel 내장 `password.confirm` 미들웨어로 보호됩니다.

비밀번호 확인 기능 구현을 시작하려면 Fortify에게 비밀번호 확인 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 헤드리스 인증 라이브러리입니다. 완성된 Laravel 인증 프런트엔드를 원한다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 맞춤 가능하며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

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

Fortify는 `/user/confirm-password` 엔드포인트를 정의하며 이 뷰를 반환합니다. `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트에 POST 요청을 보내는 폼이 포함되어야 합니다. 이 엔드포인트는 사용자의 현재 비밀번호가 담긴 `password` 필드를 기대합니다.

입력한 비밀번호가 현재 비밀번호와 일치하면 Fortify는 사용자를 원래 접근하려던 라우트로 리다이렉트합니다. XHR 요청이라면 201 HTTP 응답이 반환됩니다.

비밀번호 확인 실패 시 확인 화면으로 다시 리다이렉트되며, 검증 오류가 `$errors` Blade 템플릿 변수로 제공됩니다. XHR인 경우에는 422 HTTP 응답과 함께 오류가 반환됩니다.