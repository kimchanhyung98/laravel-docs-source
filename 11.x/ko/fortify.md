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
- [2단계 인증](#two-factor-authentication)
    - [2단계 인증 활성화](#enabling-two-factor-authentication)
    - [2단계 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [2단계 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정하기](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호하기](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 프론트엔드에 독립적인 Laravel용 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후 `route:list` 아티즌 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 UI를 제공하지 않기 때문에, 직접 구현한 UI에서 Fortify가 등록한 라우트로 요청을 보내는 방식으로 활용해야 합니다. 본 문서의 나머지 부분에서는 이러한 라우트로 어떻게 요청을 보내는지에 대해 자세히 다룹니다.

> [!NOTE]  
> Fortify는 Laravel 인증 기능 구현을 빠르게 시작할 수 있도록 도와주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 등 Laravel 공식 문서를 참고해 직접 인증 서비스를 연동할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

앞서 언급한 것처럼, Laravel Fortify는 프론트엔드와 무관하게 동작하는 Laravel용 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 라우트와 컨트롤러를 등록합니다.

**Laravel 인증 기능을 사용하기 위해 Fortify를 반드시 써야 하는 것은 아닙니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 공식 문서를 참고해 직접 기능을 구현할 수 있습니다.

Laravel를 처음 접하는 분이라면, Fortify 사용 전에 [Laravel Breeze](/docs/{{version}}/starter-kits) 스타터 킷을 먼저 경험해보는 것을 추천합니다. Breeze는 [Tailwind CSS](https://tailwindcss.com)로 제작된 사용자 인터페이스와 인증 스캐폴딩(뼈대 코드)을 제공합니다. Breeze와 달리 Fortify는 라우트와 컨트롤러만 패키지로 제공하고 UI는 포함하지 않아, 후면 인증 구현을 빠르게 구축할 수 있지만 프론트엔드에 대한 선택권을 보장합니다.

Laravel Fortify는 본질적으로 Laravel Breeze의 라우트와 컨트롤러를 UI 없이 패키지로 제공하는 형태입니다. 이를 통해 특정 프론트엔드 방식에 얽매이지 않고 빠르게 인증 백엔드를 구축할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 할까?

Laravel의 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 경우, 이미 모든 인증 기능이 구현되어 있기 때문에 Fortify를 따로 설치할 필요가 없습니다.

스타터 킷을 사용하지 않고 인증이 필요한 애플리케이션이라면, 두 가지 선택지가 있습니다: 직접 인증 기능을 구현하거나, Fortify를 사용해 인증 백엔드를 제공받는 방법입니다.

Fortify를 설치하면, UI에서는 본 문서에 설명된 Fortify 인증 라우트로 요청을 보내어 인증 및 회원가입을 처리할 수 있습니다.

반면, Fortify 없이 직접 인증을 구현하고 싶다면 [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 공식 문서를 참고해 구현할 수 있습니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

일부 개발자들은 [Laravel Sanctum](/docs/{{version}}/sanctum)과 Fortify의 차이점에 대해 혼동할 수 있습니다. 두 패키지는 각각 연관된, 그러나 다른 목적을 가지고 있습니다. Fortify와 Sanctum은 상호 배타적이지 않으며, 경쟁 관계가 아닙니다.

Laravel Sanctum은 API 토큰 관리 및 세션 쿠키・토큰을 이용한 기존 사용자 인증만 담당합니다. 회원가입, 비밀번호 재설정 등 라우트는 제공하지 않습니다.

따라서, SPA(단일 페이지 앱) 또는 API 전용 백엔드를 직접 구축하려는 경우에는 Fortify(회원가입, 비밀번호 재설정 등)를 API 토큰 관리 및 세션 인증을 위한 Sanctum과 함께 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용해 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로 `fortify:install` 아티즌 명령어로 Fortify 리소스를 퍼블리시합니다:

```shell
php artisan fortify:install
```

이 명령어는 `app/Actions` 디렉터리에 Fortify 액션들을 복사하며, 디렉터리가 없다면 생성합니다. 또한, `FortifyServiceProvider`, 설정 파일, 필요한 마이그레이션 파일이 퍼블리시됩니다.

이제 DB 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일의 `features` 배열을 통해 Fortify가 기본적으로 제공하는 백엔드 라우트/기능을 정의할 수 있습니다. Fortify와 [Laravel Jetstream](https://jetstream.laravel.com)을 함께 사용하지 않는다면, 일반적으로 아래와 같은 기본 인증 기능만 활성화하길 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인, 회원가입 등 뷰를 반환하는 라우트도 등록합니다. 그러나 JavaScript 기반 SPA를 개발 중이라면 이러한 라우트가 필요하지 않습니다. 따라서 `config/fortify.php`의 `views` 값에 `false`를 지정하면 해당 라우트 등록을 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화 시 비밀번호 재설정

Fortify의 뷰를 비활성화하고 직접 비밀번호 재설정 기능을 구현하는 경우, 반드시 애플리케이션에 `password.reset`이라는 이름의 라우트를 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 `password.reset` 이름의 라우트로 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

먼저, Fortify가 "로그인" 뷰를 어떻게 반환할지 지정해야 합니다. Fortify는 UI가 없는 인증 라이브러리임을 기억하세요. 이미 완성된 프론트엔드 인증 구현이 필요하다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하세요.

모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 커스터마이징 할 수 있습니다. 일반적으로는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메소드에서 이 메소드를 호출하게 됩니다. `/login` 라우트는 Fortify가 자동으로 정의하며, 여기서 해당 뷰를 반환합니다:

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

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 있어야 합니다. 이 엔드포인트는 `email`(또는 `username`)과 `password` 값이 필요합니다. 해당 필드명은 `config/fortify.php`의 `username` 값과 동일해야 합니다. 라라벨의 "로그인 유지(remember me)" 기능을 사용하고 싶다면 불리언 `remember` 필드를 추가할 수 있습니다.

로그인 성공 시 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청이라면 HTTP 200 응답이 반환됩니다.

로그인에 실패하면 사용자는 다시 로그인 화면으로 리다이렉트되고, 검증 오류는 공유 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에서 확인할 수 있습니다. XHR 요청인 경우 422 HTTP 응답으로 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격증명 및 설정된 인증 가드를 사용해 사용자를 인증합니다. 그러나, 로그인 자격 인증과 사용자 검색을 완전히 커스터마이즈하고 싶다면, `Fortify::authenticateUsing` 메소드를 사용할 수 있습니다.

이 메소드는 HTTP 요청을 받는 클로저를 인수로 받으며, 요청에 첨부된 로그인 자격증명을 직접 검증하고 인증된 사용자 인스턴스를 반환해야 합니다. 자격 증명이 유효하지 않거나 사용자를 찾지 못했다면, `null` 또는 `false`를 반환해야 합니다. 이 메소드는 보통 `FortifyServiceProvider`의 `boot` 메소드에서 등록합니다:

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

Fortify에서 사용하는 인증 가드는 `fortify` 설정 파일에서 지정할 수 있습니다. 단, 여기서 지정하는 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 구현체여야 합니다. SPA용 인증을 위해 Fortify를 사용한다면, Laravel 기본 `web` 가드를 [Laravel Sanctum](https://laravel.com/docs/sanctum)과 함께 사용하는 것을 권장합니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 여러 인보커블(호출 가능한) 클래스의 파이프라인을 거쳐 처리합니다. 만약 직접 파이프라인을 구성하고 싶다면, `Fortify::authenticateThrough` 메소드를 사용할 수 있습니다. 각 클래스는 `Illuminate\Http\Request` 인스턴스를 받는 `__invoke` 메소드와, [미들웨어](/docs/{{version}}/middleware)처럼 다음 미들웨어로 요청을 넘기는 `$next` 변수를 사용해야 합니다.

사용자 정의 파이프라인은 클로저에서 클래스 배열을 반환하도록 구현하며, 이 메소드는 일반적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메소드에서 호출합니다.

아래는 커스터마이징의 기준이 되는 기본 파이프라인 예시입니다:

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

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어로 인증 시도를 제한합니다. 이 미들웨어는 사용자명과 IP주소 조합별로 인증 시도를 제한합니다.

IP 주소별로만 제한하는 등, 다른 방식의 인증 시도 제한이 필요한 경우, `fortify.limiters.login` 옵션을 통해 [사용자 정의 Rate Limiter](/docs/{{version}}/routing#rate-limiting)를 지정할 수 있습니다. 해당 옵션은 `config/fortify.php`에 위치합니다.

> [!NOTE]  
> 시도 제한(Throttling), [2단계 인증](/docs/{{version}}/fortify#two-factor-authentication), 외부 WAF(웹 애플리케이션 방화벽)를 조합하면 보다 강력한 보안을 제공할 수 있습니다.

<a name="customizing-authentication-redirects"></a>
### 리다이렉트 커스터마이징

로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 옵션에 따라 URI로 리다이렉트합니다. XHR 요청이라면 HTTP 200이 반환되고, 사용자가 로그아웃하면 `/` URI로 리다이렉트됩니다.

이 동작을 더 상세히 커스터마이징하려면, Laravel [서비스 컨테이너](/docs/{{version}}/container)에 `LoginResponse`, `LogoutResponse` 계약(Contract)의 구현체를 바인딩할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `register` 메소드에서 구현합니다:

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
## 2단계 인증

Fortify의 2단계 인증 기능을 활성화하면, 인증 과정에서 사용자가 6자리 숫자 토큰을 입력해야 하며, 이 토큰은 Google Authenticator 등, TOTP 호환 모바일 인증 앱에서 생성할 수 있습니다.

먼저, `App\Models\User` 모델에 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트가 추가되어야 합니다:

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

그런 다음, 사용자가 2단계 인증을 관리할 수 있는 화면(활성화/비활성화, 복구코드 재발급 등)을 구축해야 합니다.

> 참고: 기본적으로, `fortify` 설정 파일의 `features` 배열에는 2단계 인증 설정 변경 시 비밀번호 확인이 필요하도록 지정되어 있습니다. 따라서 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화

2단계 인증을 활성화하려면 UI에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 성공 시 사용자는 이전 URL로 리다이렉트되고, `status` 세션 변수로 `two-factor-authentication-enabled`가 설정됩니다. 이 변수를 활용해 성공 메시지를 표시할 수 있습니다. XHR 요청일 경우 HTTP 200 응답이 반환됩니다.

활성화 직후 사용자는 2단계 인증을 "확인"하기 위해 인증 코드를 입력해야 합니다. 따라서 성공 메시지에 추가 안내 텍스트를 넣는 것이 좋습니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 2단계 인증 설정을 마무리하세요.
    </div>
@endif
```

그리고 사용자가 인증 앱에 등록할 QR 코드를 표시해야 합니다. Blade를 사용하는 경우 `twoFactorQrCodeSvg` 메소드를 통해 SVG 이미지를 얻을 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

JavaScript 기반 프론트엔드에서는 `/user/two-factor-qr-code`로 GET 요청을 보내면, QR 코드 SVG가 포함된 JSON 객체를 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 2단계 인증 확인

사용자에게 QR 코드뿐만 아니라 인증 코드 입력란도 제공해서 "2단계 인증 설정"을 마무리해야 합니다. 이 코드는 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청됩니다.

요청이 성공하면 이전 URL로 리다이렉트되고, `status` 세션 변수로 `two-factor-authentication-confirmed`가 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        2단계 인증이 정상적으로 확인되고 활성화되었습니다.
    </div>
@endif
```

XHR로 요청한 경우 HTTP 200 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

2단계 인증 복구 코드도 사용자에게 제공해야 합니다. 복구 코드를 통해 휴대폰을 분실한 경우에도 로그인할 수 있습니다. Blade에서 인증된 사용자 인스턴스를 통해 복구 코드를 확인할 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

JavaScript 프론트엔드에서는, `/user/two-factor-recovery-codes`로 GET 요청해 복구 코드의 JSON 배열을 받을 수 있습니다.

복구 코드 재발급은 `/user/two-factor-recovery-codes`로 POST 요청하여 수행합니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 인증하기

인증 과정에서는 Fortify가 자동으로 2단계 인증 도전(challenge) 화면으로 리다이렉트합니다. XHR 로그인 요청의 경우에는 인증 성공 시 반환되는 JSON에 `two_factor` 불리언 값이 있어, 이를 통해 2단계 인증 화면으로 이동이 필요한지 판단할 수 있습니다.

2단계 인증 도전 뷰 반환 방법을 Fortify에 알려주어야 합니다. 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 커스터마이징 가능합니다:

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

Fortify는 `/two-factor-challenge` 라우트를 자동으로 등록하며, 이 뷰를 반환합니다. 해당 템플릿에는 `/two-factor-challenge`로 POST 요청하는 폼이 있어야 하며, `code`(TOTP 토큰) 또는 `recovery_code` 필드(복구 코드) 중 하나를 받아야 합니다.

로그인 성공 시, Fortify는 `home` 설정 값에 따라 리다이렉트하고, XHR 요청 시엔 HTTP 204가 반환됩니다.

실패하면, 인증 도전 화면으로 돌아가 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 오류를 확인할 수 있습니다. XHR 요청의 경우 HTTP 422와 오류가 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화

2단계 인증을 비활성화하려면, `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보냅니다. 이때, Fortify의 2단계 인증 관련 엔드포인트를 호출하려면 반드시 [비밀번호 확인](#password-confirmation)이 선행되어야 합니다.

<a name="registration"></a>
## 회원가입

회원가입 구현 역시 Fortify에 "회원가입" 뷰 반환 방법을 알려주는 것으로 시작합니다. Fortify는 UI가 없는 인증 라이브러리입니다. 완성된 프론트엔드 인증이 필요하다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 이용하세요.

Fortify의 모든 뷰 반환 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 커스터마이징할 수 있습니다:

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

Fortify는 `/register` 라우트를 등록하며, 뷰 반환 후 POST 요청을 `/register` 엔드포인트에 보냅니다.

`/register` 엔드포인트는 문자열 `name`, 이메일 주소/사용자명, `password`, `password_confirmation` 필드를 기대합니다. 이메일 또는 사용자명 필드명은 설정 파일의 `username` 값과 일치해야 합니다.

가입이 성공하면, Fortify는 `home` 설정 값에 지정된 URI로 리다이렉트합니다. XHR 요청일 경우 HTTP 201이 반환됩니다.

실패하면, 다시 회원가입 화면으로 돌아가며, 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. XHR 요청이면 422 응답과 함께 오류가 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

회원 검증 및 생성 과정은 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정해 커스터마이징할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능 구현의 첫 단계는, "비밀번호 분실" 뷰 반환을 Fortify에 알려주는 것입니다. 이미 완성된 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 참고하세요.

뷰 렌더링 로직은 아래처럼 커스터마이즈 가능합니다:

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

Fortify는 `/forgot-password` 라우트를 자동으로 등록합니다. 해당 템플릿에는 `/forgot-password`로 POST 요청을 보내는 폼이 있어야 하며, 필드로 이메일이 필요합니다. 필드 이름/DB 컬럼명은 설정 파일의 `email` 값과 같아야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 결과 처리

요청이 성공하면 사용자는 `/forgot-password`로 리다이렉트되고, 보안 링크가 포함된 이메일을 받게 됩니다. XHR 요청 성공 시에는 200 응답만 반환됩니다.

이 화면에서는 `status` 세션 변수로 요청 결과 메시지를 표시할 수 있습니다.

`$status` 값은 애플리케이션의 `passwords` [언어 파일](/docs/{{version}}/localization)에 정의된 번역 문자열과 일치합니다. 이 값을 커스터마이징하려면 언어 파일을 퍼블리시해 수정할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패하면, 다시 재설정 링크 요청 화면으로 돌아가며, 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 또는 XHR 요청의 경우 422 응답으로 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정하기

비밀번호 재설정 뷰 반환 방법도 Fortify에 지정해야 합니다:

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

Fortify는 이 뷰를 표시하는 라우트를 자동으로 등록합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청하는 폼이 있어야 하며, `email`, `password`, `password_confirmation` 필드와 함께 `request()->route('token')` 값을 담은 숨김 필드도 포함해야 합니다. 이메일 필드명 역시 `fortify` 설정의 `email` 값과 같아야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 결과 처리

재설정 성공 시 `/login` 라우트로 리다이렉트되어 새 비밀번호로 로그인할 수 있습니다. 그리고 `status` 세션 변수로 재설정 성공 메시지를 로그인 화면에 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청은 HTTP 200 응답만 반환됩니다.

실패하면, 다시 재설정 화면으로 돌아가며, 오류는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 제공됩니다. XHR 요청이라면 422 응답을 받게 됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후 사용자에게 이메일 인증을 요구할 수 있습니다. 먼저, `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그리고, `App\Models\User` 클래스가 반드시 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

이 두 가지를 완료하면, 신규 가입 사용자에게 이메일 주소 인증 요청 메일이 자동으로 전송됩니다. 이제 Fortify에 이메일 인증 안내 화면을 어떻게 표시할지 알려주어야 합니다.

아래처럼 뷰 반환 메소드를 지정합니다:

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

Fortify는 사용자가 `/email/verify`로 리다이렉트될 때 이 뷰를 반환하는 라우트를 자동 등록합니다(내장 `verified` 미들웨어에 의해).

`verify-email` 템플릿에는 이메일에 전송한 인증 링크를 클릭하라는 안내 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

필요하다면 `verify-email` 화면에 `/email/verification-notification` 엔드포인트로 POST 요청하는 버튼을 추가할 수 있습니다. 이 엔드포인트에 요청이 오면 새 인증 메일이 전송되어, 이전 인증 링크를 분실한 경우에도 사용자에게 새 인증 링크를 제공합니다.

요청 성공 시, Fortify는 `/email/verify`로 리다이렉트하고, `status` 세션 변수로 성공 메시지를 표시할 수 있습니다. XHR 요청 일 경우 HTTP 202가 반환됩니다:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새 이메일 인증 링크가 발송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호하기

특정 라우트나 라우트 그룹에서 이메일 인증이 완료된 사용자만 접근하게 하려면, `verified` 미들웨어를 적용하세요. 이 미들웨어는 Laravel이 자동으로 등록하고, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하다보면 사용자가 민감한 작업을 수행하기 전에 비밀번호를 한 번 더 확인받고 싶을 때가 있습니다. 이런 경우 Laravel의 내장 `password.confirm` 미들웨어로 라우트를 보호할 수 있습니다.

비밀번호 확인 화면을 구현하려면, Fortify에 어떻게 뷰를 반환할지 알려주어야 합니다. 역시 이미 만들어진 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 참고하세요.

뷰 렌더링 로직은 다음과 같이 지정할 수 있습니다:

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

Fortify는 `/user/confirm-password` 엔드포인트를 자동 등록해 해당 뷰를 반환합니다. 템플릿에는 `/user/confirm-password`로 POST 요청을 보내는 폼이 있으며, 현재 비밀번호를 입력해야 합니다.

비밀번호가 일치하면 Fortify는 사용자가 원래 접근하려던 라우트로 리다이렉트합니다. XHR 요청의 경우 HTTP 201이 반환됩니다.

실패하면 비밀번호 확인 화면으로 돌아가며, 오류는 공유 `$errors` Blade 변수로 제공되며, XHR 요청이라면 422 응답을 받게 됩니다.
