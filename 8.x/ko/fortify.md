# Laravel Fortify

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [Fortify를 언제 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 서비스 프로바이더](#the-fortify-service-provider)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리디렉션 커스터마이징](#customizing-authentication-redirects)
- [2단계 인증](#two-factor-authentication)
    - [2단계 인증 활성화](#enabling-two-factor-authentication)
    - [2단계 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [2단계 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 검증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 프론트엔드와 무관한 Laravel용 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하기 위해 필요한 라우트와 컨트롤러를 등록합니다. Fortify 설치 후 `route:list` Artisan 명령어를 실행해 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않으므로, 여러분이 직접 구현한 UI가 Fortify가 등록하는 라우트로 요청을 보내는 구조로 사용됩니다. 이 문서의 나머지 부분에서는 이러한 라우트로 어떻게 요청을 보낼지 자세히 설명합니다.

> {tip} Fortify는 Laravel의 인증 기능 구현을 빠르게 시작할 수 있도록 도와주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고하여 직접 Laravel의 인증 서비스를 사용할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

앞서 설명한 것처럼, Laravel Fortify는 프론트엔드에 독립적인 인증 백엔드 구현체로, 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 위한 경로(라우트)와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용해야 하는 것은 아닙니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고하여 직접 구현할 수 있습니다.

Laravel에 익숙하지 않다면, Fortify를 사용하기 전에 [Laravel Breeze](/docs/{{version}}/starter-kits) 스타터 키트를 먼저 살펴보는 것이 좋습니다. Laravel Breeze는 [Tailwind CSS](https://tailwindcss.com)로 작성된 UI와 인증 구성을 포함하고 있습니다. Breeze는 Fortify와 달리 라우트와 컨트롤러가 직접 애플리케이션에 퍼블리시되어, 인증 기능을 직접 학습하고 익힐 수 있습니다.

Laravel Fortify는 본질적으로 Laravel Breeze의 라우트와 컨트롤러를 UI 없이 패키지 형태로 제공하므로, 특정한 프론트엔드에 종속되지 않고 인증 백엔드 구현을 빠르게 구성할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 하나요?

Laravel Fortify를 언제 사용하는 것이 적합한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우, 별도의 설치가 필요하지 않습니다. 모든 스타터 키트에는 이미 완전한 인증 기능이 내장되어 있기 때문입니다.

스타터 키트를 사용하지 않고 인증 기능이 필요한 경우, 직접 인증 기능을 구현하거나, Fortify를 백엔드 구현체로 사용할 수 있습니다.

Fortify를 설치하면 여러분의 프론트엔드 UI가 Fortify가 제공하는 인증 라우트로 요청을 보내어 인증 및 회원가입을 진행할 수 있습니다.

Fortify를 사용하지 않고 직접 Laravel의 인증 서비스를 사용하고 싶다면, [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고하세요.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

[Laravel Sanctum](/docs/{{version}}/sanctum)과 Fortify의 차이에 대해 헷갈려하는 개발자들이 있습니다. 이 두 패키지는 서로 관련 있지만, 전혀 다른 문제를 해결하며, 서로 배타적이거나 경쟁하는 패키지가 아닙니다.

Laravel Sanctum은 API 토큰 관리와 세션/토큰 기반 기존 사용자 인증만 담당합니다. 사용자 회원가입, 비밀번호 재설정 등 관련 라우트는 제공하지 않습니다.

API를 제공하거나 단일 페이지 애플리케이션(SPA)의 백엔드로 사용되는 경우, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)을 모두 함께 사용하는 것이 가능합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저로 Fortify를 설치합니다:

```nothing
composer require laravel/fortify
```

다음으로, `vendor:publish` 명령어로 Fortify의 리소스를 퍼블리시합니다:

```bash
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

이 명령어는 Fortify의 액션을 `app/Actions` 디렉터리에 퍼블리시합니다(폴더가 없으면 새로 생김). 뿐만 아니라, Fortify 설정 파일과 마이그레이션도 함께 퍼블리시됩니다.

데이터베이스 마이그레이션을 진행하세요:

```bash
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify 서비스 프로바이더

위에서 진행한 `vendor:publish` 명령어는 `App\Providers\FortifyServiceProvider` 클래스도 함께 퍼블리시합니다. 이 클래스가 `config/app.php`의 `providers` 배열에 등록되어 있는지 확인하세요.

Fortify 서비스 프로바이더는 퍼블리시된 액션을 등록하고, 해당 작업이 수행될 때 Fortify가 이 액션을 사용하도록 지정합니다.

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일에는 `features` 배열이 있습니다. 이 배열은 Fortify가 기본적으로 제공할 백엔드 라우트/기능을 정의합니다. [Laravel Jetstream](https://jetstream.laravel.com)과 함께 사용하지 않는다면, 다음과 같이 대부분의 Laravel 애플리케이션이 사용하는 기본 인증 기능만 활성화하는 것을 추천합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면, 회원가입 화면 등 뷰를 반환하는 라우트를 정의합니다. 하지만, JavaScript 위주의 싱글 페이지 애플리케이션을 구축하고 있다면 이러한 라우트가 필요하지 않을 수 있습니다. 이 경우, `config/fortify.php` 파일의 `views` 값을 `false`로 설정하여 이 라우트들을 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 및 비밀번호 재설정 비활성화

Fortify의 뷰를 비활성화하고, 비밀번호 재설정 기능을 직접 구현하는 경우, 반드시 애플리케이션의 "비밀번호 재설정" 뷰를 보여주는 `password.reset` 라우트를 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 이 라우트를 통해 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

먼저, Fortify에 "로그인" 화면을 어떻게 반환할지 알려주어야 합니다. Fortify는 헤드리스(화면 없는) 인증 라이브러리임을 기억하세요. 모두 구현된 프론트엔드 인증 기능이 필요하다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

보통 인증 뷰 화면 렌더링은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드를 통해 커스터마이즈할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다. Fortify는 `/login` 라우트 정의 및 이 뷰 반환을 자동으로 처리합니다:

    use Laravel\Fortify\Fortify;

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 들어 있어야 합니다. 이 엔드포인트는 `email` / `username`(문자열)과 `password`(문자열)를 받으며, 해당 필드명은 `config/fortify.php`의 `username`값과 일치해야 합니다. 추가로 `remember`(불리언) 필드를 통해 "로그인 상태 유지" 여부를 전달할 수 있습니다.

로그인 성공 시, Fortify는 `fortify` 설정 파일의 `home` 옵션에 설정된 URI로 리디렉션합니다. XHR 요청일 경우 200 HTTP 응답을 반환합니다.

로그인 실패 시, 사용자는 다시 로그인 화면으로 리디렉션되며 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 검증 에러 메시지를 조회할 수 있습니다. XHR 요청인 경우 422 HTTP 응답에 에러가 포함됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격증명과 Guard 설정에 따라 사용자를 인증합니다. 그러나 로그인 자격증명 검증 과정 및 사용자 조회 방식 전체를 직접 제어하고자 할 때, `Fortify::authenticateUsing` 메서드를 사용하면 됩니다.

이 메서드는 요청을 받는 클로저를 인수로 받고, 로그인 자격증명을 직접 검증하여 일치 시 사용자 인스턴스를 반환합니다. 일치하지 않으면 `null` 또는 `false`를 반환해야 하며, 일반적으로 이 코드는 `FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify가 사용하는 인증 가드는 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 단, 여기에 지정되는 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard`를 구현해야 합니다. SPA에서 Fortify 인증을 사용한다면 [Laravel Sanctum](https://laravel.com/docs/sanctum)과 함께 기본 `web` 가드를 사용하는 것이 좋습니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 일련의 인보커블 클래스(파이프라인)로 인증합니다. 만약 이 파이프라인을 커스터마이즈하고 싶다면, 원하는 클래스 배열을 반환하는 클로저를 `Fortify::authenticateThrough` 메서드로 지정하세요. 각 클래스는 `Illuminate\Http\Request` 인스턴스와, 미들웨어처럼 다음 클래스로 호출을 넘기는 역할의 `$next` 변수를 받아야 합니다.

아래는 Fortify의 기본 인증 파이프라인 예시로, 커스터마이징의 시작점이 될 수 있습니다:

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

로그인에 성공하면 Fortify는 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청은 200 HTTP 응답을 반환합니다. 로그아웃 시에는 루트(`/`)로 리디렉션됩니다.

더 세밀한 동작이 필요하다면, `LoginResponse` 및 `LogoutResponse` 계약의 구현체를 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 바인딩할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `register` 메서드에서 등록합니다:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * 애플리케이션 서비스를 등록합니다.
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

Fortify의 2단계 인증 기능을 활성화하면, 로그인 과정에서 6자리 숫자 토큰(인증 앱에서 생성된 TOTP)을 추가로 입력해야 합니다. Google Authenticator와 같이 TOTP를 지원하는 모바일 인증 앱에서 토큰을 생성할 수 있습니다.

먼저, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하고 있는지 확인하세요:

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

다음으로, 사용자가 2단계 인증을 관리할 수 있는 화면을 구축해야 합니다. 이 화면에는 2단계 인증 활성화/비활성화, 복구 코드 재생성 옵션 등이 포함되어야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에서 Fortify의 2단계 인증은 수정 전 비밀번호 확인(Password Confirmation)이 필요하도록 지정되어 있습니다. 따라서, 이 기능을 구현하기 전에 Fortify의 [비밀번호 확인](#password-confirmation) 기능도 함께 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화

2단계 인증을 활성화하려면, 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 성공 시, 이전 페이지로 리디렉션되고 세션 변수 `status`가 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 값을 감지해 성공 메시지를 표시할 수 있습니다. XHR 요청인 경우 200 HTTP 응답을 반환합니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm text-green-600">
        2단계 인증이 활성화되었습니다.
    </div>
@endif
```

그 다음, 사용자가 인증 앱에 등록할 수 있도록 2단계 인증용 QR코드를 보여주어야 합니다. Blade를 쓸 경우, 사용자 인스턴스에 있는 `twoFactorQrCodeSvg` 메서드로 QR코드 SVG를 가져올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

자바스크립트 기반 프론트엔드라면, `/user/two-factor-qr-code` 엔드포인트로 XHR GET 요청을 보내면 JSON 객체(`svg` 키 포함)로 QR코드를 받을 수 있습니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시하기

사용자의 2단계 인증 복구 코드도 함께 보여주어야 합니다. 복구 코드는 사용자가 모바일 기기를 분실했을 때 인증에 사용할 수 있습니다. Blade에서는 인증된 사용자 인스턴스의 `recoveryCodes` 메서드를 이용하면 됩니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프론트엔드의 경우, `/user/two-factor-recovery-codes` 엔드포인트에 GET 요청을 보내면 복구 코드 배열을 얻을 수 있습니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트로 POST 요청을 보내세요.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 인증하기

인증 과정에서 Fortify는 자동으로 사용자를 2단계 인증 챌린지 화면으로 리디렉션합니다. XHR 로그인 요청이라면, 성공시 반환되는 JSON 응답에 `two_factor`(불리언) 속성이 포함되니, 이 값으로 2단계 인증 챌린지 화면으로 전환할지 판단합니다.

2단계 인증 기능을 구현하려면, Fortify에서 2단계 인증 챌린지 뷰를 반환하도록 지정해 주어야 합니다. 모든 인증 관련 뷰의 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify는 `/two-factor-challenge` 라우트와 이 뷰 반환 처리를 자동으로 합니다. 뷰에는 `/two-factor-challenge` 엔드포인트로 POST 요청을 보내는 폼이 필요합니다. 여기에 `code`(유효한 TOTP 토큰) 또는 `recovery_code`(복구 코드) 필드가 포함되어야 합니다.

로그인 성공 시 설정된 `home` URI로 리디렉션합니다. XHR 요청은 204 HTTP 응답을 반환합니다.

실패 시에는 다시 2단계 챌린지 화면으로 리디렉션되고, `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)로 검증 에러를 받을 수 있습니다. XHR 요청이라면 422 응답에 에러가 포함되어 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화

2단계 인증을 비활성화하려면 `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내야 합니다. Fortify의 2단계 인증 관련 엔드포인트는 항상 [비밀번호 확인](#password-confirmation)이 선행되어야 한다는 점을 기억하세요.

<a name="registration"></a>
## 회원가입

회원가입 기능 구현을 시작하려면 Fortify에 "회원가입" 화면을 반환하는 법을 알려주어야 합니다. Fortify는 헤드리스 인증 라이브러리임을 기억하세요. 프론트엔드가 완전히 구현된 인증 기능이 필요하다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify는 `/register` 라우트 정의와 해당 뷰 반환을 자동으로 처리합니다. `register` 템플릿에는 `/register`로 POST 요청을 보내는 폼이 필요합니다.

`/register` 엔드포인트는 `name`(문자열), 이메일/사용자명(문자열), `password`, `password_confirmation`을 요구합니다. 이메일/사용자명 필드는 반드시 설정 파일의 `username` 값과 일치해야 합니다.

회원가입 성공 시, `home` URI로 리디렉션하고 XHR 요청은 200 HTTP 응답을 받습니다.

실패 시에는 다시 회원가입 화면으로 리디렉션되며, `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 또는 XHR 응답 내 422 코드로 에러를 받을 수 있습니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

회원 검증 및 생성 과정은 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션에서 자유롭게 수정할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능 구현을 시작하려면 Fortify에 "비밀번호 찾기" 화면을 어떻게 반환할지 알려주어야 합니다. Fortify는 헤드리스 인증 라이브러리임을 기억하세요. 인증 프론트엔드가 필요하면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

아래와 같이 뷰 렌더링 로직을 `Laravel\Fortify\Fortify`에서 지정할 수 있습니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify는 `/forgot-password` 엔드포인트를 스스로 정의하고 뷰를 반환합니다. 해당 템플릿에는 `/forgot-password`로 POST 요청을 보내는 폼이 있어야 하며, 필드는 `email`이어야 합니다(설정 파일의 `email` 값과 일치).

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

요청 성공 시 Fortify는 사용자에게 비밀번호 재설정 이메일을 보내고, `/forgot-password`로 리디렉션합니다. XHR 요청은 200 응답을 받습니다.

성공 후 `/forgot-password`에서 세션 변수 `status`로 비밀번호 재설정 요청 결과 메시지를 출력할 수 있습니다. 이 값은 여러분의 `passwords` [언어 파일](/docs/{{version}}/localization)의 값 중 하나입니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패 시에는 다시 해당 화면으로 리디렉션되어 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 또는 XHR 422 응답에 에러가 전달됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정을 구현하려면 "비밀번호 재설정" 뷰 반환 로직을 Fortify에 알려야 합니다.

뷰 렌더링 로직은 `Laravel\Fortify\Fortify`를 통해 지정하며, 보통 `App\Providers\FortifyServiceProvider`의 `boot`에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify는 해당 라우트 정의와 보기 반환을 자동으로 처리합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청을 보내는 폼이 있어야 하며, `email`, `password`, `password_confirmation`, 그리고 `token`(hidden) 필드가 필요합니다. "email" 필드는 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

요청이 성공하면 Fortify가 `/login` 라우트로 리디렉션해 사용자가 새 비밀번호로 로그인할 수 있게 합니다. 추가로 `status` 세션 변수를 이용해 로그인 화면에 성공 메시지를 표시할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청은 200 응답을 받습니다.

실패 시에는 다시 재설정 화면으로 리디렉션, `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 또는 XHR 422 응답에 에러가 포함됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 Fortify 설치 시 생성되는 `App\Actions\ResetUserPassword` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 이후 사용자가 계속 애플리케이션을 이용하기 전에 이메일 주소를 검증하도록 할 수 있습니다. 먼저, `fortify` 설정 파일의 `features` 배열에서 `emailVerification` 기능이 활성화되어 있는지 확인하고, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail`을 구현하고 있는지 확인하세요.

이 두 과정을 완료하면 신규 회원은 이메일 인증 요청 메일을 받게 됩니다. 이제 사용자가 이메일의 인증 링크를 클릭하라는 안내를 보여줄 화면을 Fortify에 지정해야 합니다.

아래와 같이 뷰 렌더링 로직을 구현하세요:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify는 사용자가 내장 `verified` 미들웨어로 `/email/verify` 엔드포인트에 리디렉션 될 때 이 라우트를 자동으로 처리합니다.

`verify-email` 템플릿에는 사용자가 이메일 인증 링크 클릭을 안내하는 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

원한다면, `verify-email` 템플릿에 `/email/verification-notification`으로 POST 요청하는 버튼을 추가할 수 있습니다. 이 엔드포인트가 요청을 받으면, 새 인증 링크 이메일을 발송합니다.

요청이 성공하면 Fortify가 사용자를 `/email/verify` 엔드포인트로 리디렉션하며, `status` 세션 변수를 통해 성공 메시지를 표시할 수 있습니다. XHR 요청은 202 HTTP 응답을 반환합니다:

```html
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새로운 이메일 인증 링크가 발송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호

특정 라우트 또는 라우트 그룹에 이메일 인증된 사용자만 접근 가능하도록 하려면, 라우트에 내장 `verified` 미들웨어를 적용해야 합니다. 이 미들웨어는 `App\Http\Kernel`에 등록되어 있습니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하다 보면, 일부 행동(예: 중요한 정보 변경)은 실제 구현 전에 사용자의 비밀번호 확인이 필요한 경우가 있습니다. 이런 라우트는 Laravel 내장 `password.confirm` 미들웨어로 보호되는 것이 일반적입니다.

비밀번호 확인 기능 구현을 위해 Fortify에 "비밀번호 재확인" 화면 반환 로직을 알려주어야 합니다. Fortify는 헤드리스 인증 라이브러리임을 기억하세요. 인증 프론트엔드가 필요하면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

아래와 같이 뷰 렌더링을 지정할 수 있습니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Fortify는 `/user/confirm-password` 엔드포인트를 자동으로 정의하며, `confirm-password` 템플릿에는 `/user/confirm-password`로 POST 요청하는 폼이 들어 있어야 합니다. 이 엔드포인트는 사용자의 현재 `password` 필드를 요구합니다.

비밀번호가 일치하면, 사용자가 접근하려 했던 라우트로 리디렉션되며, XHR 요청은 201 HTTP 응답을 받습니다.

실패 시에는 다시 비밀번호 확인 화면으로 리디렉션되고, `$errors` Blade 템플릿 변수 또는 XHR 422 응답에 검증 에러가 포함됩니다.