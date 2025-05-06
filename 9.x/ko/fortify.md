# Laravel Fortify

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [Fortify는 언제 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 서비스 프로바이더](#the-fortify-service-provider)
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
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개

[Laravel Fortify](https://github.com/laravel/fortify)는 프론트엔드에 종속적이지 않은 Laravel 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 모든 Laravel 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify 설치 후 `route:list` Artisan 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않으므로, 여러분이 직접 Fortify가 등록한 라우트에 요청을 보내는 사용자 인터페이스와 함께 사용해야 합니다. 이 문서의 나머지 부분에서는 이러한 라우트에 요청하는 방법을 다룹니다.

> **참고**  
> Fortify는 여러분이 Laravel의 인증 기능을 빠르게 구현할 수 있도록 돕는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** 항상 [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 관련 문서를 참고하여 Laravel 인증 서비스를 직접 사용할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란?

앞서 언급했듯이, Laravel Fortify는 프론트엔드에 종속적이지 않은 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 모든 인증 기능을 제공하기 위해 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** [인증](/docs/{{version}}/authentication), [비밀번호 재설정](/docs/{{version}}/passwords), [이메일 인증](/docs/{{version}}/verification) 문서를 참고하여 직접 인증 서비스를 구현할 수 있습니다.

Laravel을 처음 접하는 사용자라면, Fortify 사용에 앞서 [Laravel Breeze](/docs/{{version}}/starter-kits) 스타터 키트를 먼저 살펴보는 것이 좋습니다. Laravel Breeze는 [Tailwind CSS](https://tailwindcss.com)로 만들어진 사용자 인터페이스를 포함하는 인증 스캐폴딩을 제공합니다. Fortify와 달리 Breeze는 라우트와 컨트롤러를 여러분의 애플리케이션으로 직접 퍼블리시해주므로 인증 구조를 익히기 수월합니다.

Laravel Fortify는 사실상 Laravel Breeze의 라우트와 컨트롤러를 UI 없이 패키지로 제공하는 형태입니다. 이를 통해 특정 프론트엔드에 종속되지 않고 인증 기능의 백엔드를 손쉽게 구성할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify는 언제 사용해야 하나요?

Laravel Fortify를 언제 사용하는 것이 적합한지 궁금할 수 있습니다. 먼저, Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우에는 별도로 Fortify를 설치할 필요가 없습니다. 모든 스타터 키트에는 인증이 이미 구현되어 있습니다.

스타터 키트를 사용하지 않으면서 인증 기능이 필요한 경우, 두 가지 선택지가 있습니다. 직접 인증 기능을 구현하거나, Fortify를 설치하여 백엔드 인증 기능을 구현하는 것입니다.

Fortify를 설치하면, 여러분이 만든 사용자 인터페이스가 본 문서에서 설명하는 Fortify의 인증 라우트에 요청을 보내어 인증 및 회원가입을 처리할 수 있습니다.

Fortify를 사용하지 않고 직접 인증 서비스를 다루고 싶다면 해당 기능들의 공식 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify & Laravel Sanctum

일부 개발자들은 [Laravel Sanctum](/docs/{{version}}/sanctum)과 Fortify의 차이점에 대해 혼동할 수 있습니다. 두 패키지는 서로 다른 목적을 가지고 있기 때문에, Fortify와 Sanctum은 상호 배타적이거나 경쟁관계에 있지 않습니다.

Laravel Sanctum은 API 토큰 관리와 세션 쿠키/토큰을 통한 기존 사용자 인증만 처리합니다. 회원가입, 비밀번호 재설정 등의 라우트는 제공하지 않습니다.

API를 제공하거나 싱글 페이지 애플리케이션(SPA) 백엔드로 동작하는 인증 레이어를 직접 구축하려 한다면, Fortify(회원가입·비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)을 모두 사용할 수도 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 이용해 Fortify를 설치하세요:

```shell
composer require laravel/fortify
```

다음으로 `vendor:publish` 명령어를 사용해 Fortify의 리소스를 퍼블리시하세요:

```shell
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

이 명령은 Fortify의 액션을 `app/Actions` 디렉터리에 생성하며, 폴더가 없다면 자동으로 생성됩니다. 또한 `FortifyServiceProvider`, 설정 파일, 필요한 DB 마이그레이션이 모두 퍼블리시됩니다.

이제 데이터베이스 마이그레이션을 실행해야 합니다:

```shell
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify 서비스 프로바이더

위의 `vendor:publish` 명령어는 `App\Providers\FortifyServiceProvider` 클래스도 퍼블리시합니다. 이 클래스가 `config/app.php` 설정 파일의 `providers` 배열에 등록되어 있는지 확인하세요.

Fortify 서비스 프로바이더는 퍼블리시된 액션을 등록하고, Fortify가 각 작업을 실행할 때 해당 액션을 사용하도록 설정합니다.

<a name="fortify-features"></a>
### Fortify 기능

`fortify` 설정 파일은 `features` 설정 배열을 포함합니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 라우트/기능을 정의합니다. [Laravel Jetstream](https://jetstream.laravel.com)과 Fortify를 함께 사용하지 않는 경우, 대부분의 Laravel 애플리케이션이 제공하는 기본 인증 기능만 활성화하는 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인·회원가입 화면 등 뷰를 반환하는 라우트를 정의합니다. 하지만 자바스크립트 기반 SPA를 구현하는 경우 이러한 라우트가 불필요할 수 있습니다. 이런 경우, 애플리케이션의 `config/fortify.php` 파일에서 `views` 설정 값을 `false`로 지정해 이 라우트들을 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화 & 비밀번호 재설정

Fortify의 뷰를 비활성화한 상태에서 직접 비밀번호 재설정 기능을 구현할 경우, 반드시 애플리케이션에서 "비밀번호 재설정" 뷰를 보여주는 `password.reset` 라우트를 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 해당 이름의 라우트를 통해 생성하기 때문입니다.

<a name="authentication"></a>
## 인증

먼저, Fortify가 "로그인" 뷰를 반환하는 방법을 지정해야 합니다. Fortify는 헤드리스 인증 라이브러리임을 기억하세요. 인증 기능의 프론트엔드 구현까지 모두 제공받고 싶다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

모든 인증 화면의 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이징할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다. Fortify는 자동으로 `/login` 라우트를 지정해 이 뷰를 반환합니다:

    use Laravel\Fortify\Fortify;

    /**
     * 애플리케이션 서비스 부트스트랩.
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

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 있어야 합니다. 이 엔드포인트는 문자열 `email`/`username`과 `password`를 기대합니다. 입력 필드명은 `config/fortify.php`의 `username` 값과 일치해야 합니다. 또한, "나를 기억하기" 기능을 위해 불리언 타입의 `remember` 필드도 사용할 수 있습니다.

로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 구성 옵션에 지정된 URI로 리다이렉트합니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

로그인에 실패하면 사용자는 로그인 화면으로 돌아가며, 유효성 검사 에러는 공유된 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다. XHR 요청일 경우 422 HTTP 응답과 함께 에러가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징

Fortify는 기본적으로 제공된 자격증명과 설정된 인증 가드를 이용해 사용자를 조회하고 인증합니다. 그러나 인증 로직 및 사용자 조회 방식을 완전히 커스터마이즈하고 싶다면, `Fortify::authenticateUsing` 메서드를 활용하면 됩니다.

이 메서드는 클로저를 인자로 받아, 해당 클로저에서 요청의 자격증명을 체크하고 사용자를 반환하는 역할을 합니다. 자격증명이 유효하지 않거나 사용자를 찾을 수 없다면 `null` 또는 `false`를 반환해야 합니다. 보통 이 메서드는 Fortify 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify에서 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 단, 설정한 가드가 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스를 구현하는지 확인하세요. SPA 인증을 위해 Fortify를 사용하는 경우, Laravel 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 조합해 사용하는 것이 좋습니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징

Laravel Fortify는 로그인 요청을 여러 클래스의 파이프라인을 거쳐 처리합니다. 원한다면 직접 로그인 요청이 통과할 커스텀 파이프라인 클래스를 정의할 수 있습니다. 각 클래스에는 `Illuminate\Http\Request` 인스턴스를 받고, 다음 클래스로 요청을 전달하는 `$next` 변수가 호출되는 `__invoke` 메서드가 있어야 합니다.

커스텀 파이프라인 정의는 `Fortify::authenticateThrough` 메서드로 할 수 있습니다. 이 메서드는 로그인 요청이 통과할 클래스 배열을 반환하는 클로저를 인자로 받습니다. 일반적으로 이 메서드는 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

아래 예시는 기본 파이프라인 정의로, 수정 시 참고할 수 있습니다:

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
### 리다이렉트 커스터마이징

로그인 성공 시, Fortify는 애플리케이션의 `fortify` 설정 파일의 `home`에 설정된 URI로 이동시킵니다. 로그아웃 시에는 `/` URI로 이동합니다. XHR 요청의 경우 각각 200, 201 등의 HTTP 응답이 반환됩니다.

이 동작을 더욱 세밀하게 제어하려면, `LoginResponse` 및 `LogoutResponse` 계약의 구현체를 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩할 수 있습니다. 일반적으로는 애플리케이션의 `App\Providers\FortifyServiceProvider`의 `register` 메서드에서 진행합니다:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * 애플리케이션 서비스 등록.
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

Fortify의 2단계 인증 기능이 활성화되면, 인증 과정에서 사용자는 6자리 숫자 토큰을 추가로 입력해야 합니다. 이 토큰은 구글 OTP 등 TOTP 호환 모바일 인증 앱에서 생성한 일회용 비밀번호입니다.

시작에 앞서, `App\Models\User` 모델이 꼭 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하도록 하세요:

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

다음으로, 사용자가 2단계 인증을 관리할 수 있는 화면을 구현해야 합니다. 이 화면에서는 2단계 인증의 활성화/비활성화, 복구코드 재생성을 할 수 있어야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에서는, 2단계 인증 설정 변경 시 비밀번호 확인이 필요하도록 구성되어 있습니다. 따라서 2단계 인증 설정 전, Fortify의 [비밀번호 확인](#password-confirmation) 기능이 애플리케이션에 구현되어 있어야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화

2단계 인증을 시작하려면, 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트에 POST 요청을 보내야 합니다. 요청이 성공하면, 사용자는 이전 URL로 리다이렉트되고 `status` 세션 변수에 `two-factor-authentication-enabled`가 할당됩니다. 이 값을 템플릿에서 체크하여 성공 메시지를 띄울 수 있습니다. XHR 요청일 경우 200 HTTP 응답이 반환됩니다.

2단계 인증이 활성화되었더라도 사용자는 유효한 2단계 인증 코드를 입력해 "확인"을 완료해야 합니다. 따라서 아래와 같이 안내 메시지를 보여주세요:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        아래에서 2단계 인증 설정을 마무리하세요.
    </div>
@endif
```

다음으로, 인증 앱에서 스캔할 2단계 인증 QR 코드를 보여주어야 합니다. Blade로 프론트엔드를 구성한다면 아래와 같이 사용자 객체의 `twoFactorQrCodeSvg` 메서드를 사용하면 됩니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

만약 자바스크립트 기반 프론트엔드를 만든다면 `/user/two-factor-qr-code` GET 엔드포인트로 XHR 요청을 보내 JSON 형태(`svg` 키 포함)의 QR 코드를 받아올 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 2단계 인증 확인

사용자에게 QR 코드뿐만 아니라, 입력란을 제공하여 인증 코드를 입력받아 "확인" 절차를 완성해야 합니다. 입력받은 코드는 Fortify의 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청 해주어야 합니다.

요청에 성공하면, 사용자는 이전 URL로 리다이렉트 되고, `status` 세션 변수에 `two-factor-authentication-confirmed`가 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        2단계 인증이 성공적으로 확인 및 활성화되었습니다.
    </div>
@endif
```

XHR로 요청한 경우 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

사용자에게 2단계 인증 복구 코드도 안내해야 합니다. 이 코드는 모바일 장치 접속이 불가능할 때 사용자가 로그인할 수 있도록 도와줍니다. Blade로 프론트엔드를 만들었다면, 로그인된 사용자 객체에서 복구 코드를 이렇게 불러올 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 기반 프론트엔드라면 `/user/two-factor-recovery-codes` GET 엔드포인트에 요청하여 JSON 배열로 복구 코드를 받을 수 있습니다.

복구 코드를 다시 생성하려면 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청을 보내세요.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 인증하기

인증 과정에서 Fortify는 자동으로 사용자를 2단계 인증 도전 화면으로 이동시킵니다. 만약 로그인 요청이 XHR 방식이라면, 인증 성공 시 반환되는 JSON 응답에 `two_factor` 불리언 프로퍼티가 포함됩니다. 이를 확인해 2단계 인증 화면으로 이동할지 결정할 수 있습니다.

2단계 인증 기능 구현을 시작하려면, Fortify에게 2단계 인증 도전 뷰를 반환하는 방법을 지정해야 합니다. 뷰 렌더링 커스터마이징은 항상 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 이루어집니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify는 `/two-factor-challenge` 라우트를 자동으로 지정합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge`로 POST 요청을 보내는 폼이 있어야 하며, 이 요청은 유효한 TOTP 토큰이 담긴 `code` 필드, 또는 복구코드가 담긴 `recovery_code` 필드를 기대합니다.

로그인 성공 시, Fortify는 `fortify` 설정 파일의 `home`에 지정된 URI로 이동시키고, XHR 요청 시엔 204 HTTP 응답을 반환합니다.

실패시에는 두 번째 인증 화면으로(또는 422 HTTP 응답) 유효성 검사 에러와 함께 돌아갑니다. 에러는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화

2단계 인증을 비활성화하려면, `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내세요. Fortify의 2단계 인증 엔드포인트는 [비밀번호 확인](#password-confirmation) 기능이 선행되어야 사용 가능합니다.

<a name="registration"></a>
## 회원가입

회원가입 기능을 구현하려면 Fortify에게 "회원가입" 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 프론트엔드 구현이 없는 헤드리스 인증 라이브러리임을 유념하세요. 모두 구현된 인증 프론트엔드가 필요하다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하세요.

다른 Fortify 렌더링 커스터마이징과 마찬가지로, `Laravel\Fortify\Fortify`의 메서드를 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 내에서 호출하면 됩니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify는 `/register` 라우트 반환을 담당합니다. `register` 템플릿 안에는 `/register`로 POST 요청을 보내는 폼이 있어야 합니다.

`/register` 엔드포인트는 문자열 `name`, 이메일 또는 사용자명, `password`, `password_confirmation` 필드를 요구합니다. 이메일/사용자명 필드명은 설정 파일의 `username` 값과 일치해야 합니다.

회원가입 성공 시, 사용자는 설정한 `home` URI로 리다이렉트되고, XHR 요청일 때는 201 HTTP 응답이 돌아옵니다.

실패 시, 에러는 `$errors` [Blade 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)로 확인할 수 있으며, XHR 요청이라면 422 HTTP 응답으로 전달됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징

회원 검증 및 등록 과정은 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션 파일을 수정하여 커스터마이징할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

비밀번호 재설정 기능을 구현하려면, Fortify에게 "비밀번호 재설정 요청" 뷰를 반환하는 방법을 알려줘야 합니다. Fortify는 항상 헤드리스 인증 패키지임을 기억하세요.

다음처럼 `Fortify::requestPasswordResetLinkView`를 사용하세요:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify는 `/forgot-password` 엔드포인트 뷰 반환을 담당합니다. `forgot-password` 템플릿 안에는 `/forgot-password`로 POST 요청을 보내는 폼이 있어야 합니다.

`/forgot-password` 엔드포인트는 문자열 타입의 `email` 필드가 필요합니다. 필드명/DB 컬럼명은 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면 사용자는 `/forgot-password`로 돌아가며, 비밀번호 재설정용 보안링크가 이메일로 전송됩니다. XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

또한 `status` 세션 변수를 사용해 요청 성공 여부를 사용자에게 보여줄 수 있습니다. 이 값은 `passwords` [언어 파일](/docs/{{version}}/localization)에 정의된 번역 문자열과 일치합니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

실패 시에는 원래 화면으로 돌아오고, 에러는 `$errors`나 422 HTTP 응답으로 제공됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

비밀번호 재설정 완성을 위해 "비밀번호 재설정" 뷰 반환 방법을 Fortify에게 알려야 합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify는 이 뷰를 보여주는 라우트 정의까지 담당합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청을 보내는 폼이 있어야 합니다.

`/reset-password` 엔드포인트는 `email`, `password`, `password_confirmation` 필드, 그리고 `request()->route('token')` 값이 담긴 히든 `token` 필드가 필요합니다. "email" 필드명은 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 성공 시, Fortify는 `/login` 경로로 리다이렉트하며 `status` 세션 변수도 설정됩니다. 이를 로그인 화면에서 활용하여 성공 메시지를 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청은 200 HTTP 응답이 반환됩니다.

실패 시에는 원래 화면으로 돌아가고, 에러는 `$errors`(Blade) 또는 422 HTTP 응답(XHR)으로 제공됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 맞춤 처리할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증

회원가입 후, 사용자가 애플리케이션을 계속 이용하기 전에 이메일 인증을 요구하도록 할 수 있습니다. 먼저 `fortify` 설정 파일의 `features` 배열에서 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 또한 `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

이 설정이 끝나면, 신규 가입자에게 이메일 주소 소유 확인을 위한 이메일이 전송됩니다. 다만, 사용자에게 "이메일 인증 화면"을 보여주는 방법을 Fortify에게 알려야 합니다.

다음 방법으로 뷰를 커스터마이즈할 수 있습니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify는 `/email/verify` 엔드포인트에서 이 뷰를 보여주는 라우트를 정의해줍니다.

`verify-email` 템플릿엔 사용자가 인증 이메일의 링크를 클릭하도록 안내하는 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재발송

원한다면, `verify-email` 템플릿에 `/email/verification-notification`로 POST 요청을 보내는 버튼을 추가할 수 있습니다. 이 엔드포인트로 요청이 오면 인증 이메일이 다시 전송됩니다.

재발송 요청이 성공하면, Fortify는 사용자에게 `/email/verify`로 돌아가게 하고 `status` 세션 변수를 이용해 안내 메시지를 보여줄 수 있도록 합니다. XHR 요청이면 202 HTTP 응답이 반환됩니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        새로운 이메일 인증 링크가 발송되었습니다!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호

특정 라우트 또는 라우트 그룹이 이메일 인증 완료 사용자만 접근할 수 있게 하려면, 라우트에 Laravel 내장 `verified` 미들웨어를 지정하세요. 이 미들웨어는 `App\Http\Kernel`에 등록되어 있습니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인

앱을 개발하다보면 사용자가 특정 작업을 수행하기 전에 비밀번호를 재입력해 확인해야 하는 경우가 있습니다. 이 작업은 보통 Laravel 내장 `password.confirm` 미들웨어로 보호합니다.

비밀번호 확인 기능 구현을 위해, Fortify가 "비밀번호 확인" 뷰를 어떻게 반환할지 지정해야 합니다. Fortify가 헤드리스임을 다시 한번 유념하세요.

다음과 같이 구현합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Fortify는 `/user/confirm-password` 엔드포인트에 이 뷰를 할당합니다. `confirm-password` 템플릿에는 `/user/confirm-password`로 POST 요청을 보내는 폼이 필요하며, 이 폼은 사용자의 현재 비밀번호가 담긴 `password` 필드를 요구합니다.

비밀번호가 일치하면 사용자는 원래 접속하려던 경로로 리다이렉트되고, XHR 요청인 경우 201 HTTP 응답이 반환됩니다.

실패 시에는 비밀번호 확인 화면으로 돌아가고, 에러는 `$errors` Blade 변수 또는 422 HTTP 응답(XHR)으로 확인할 수 있습니다.