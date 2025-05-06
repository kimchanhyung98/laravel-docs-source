# 비밀번호 재설정

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
    - [신뢰할 수 있는 호스트 구성](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이즈](#password-customization)

<a name="introduction"></a>
## 소개

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 매번 직접 재구현하지 않아도 되도록 비밀번호 재설정 링크 전송 및 안전한 비밀번호 재설정 서비스를 편리하게 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 Laravel [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. Laravel 스타터 키트는 비밀번호 재설정 등 전체 인증 시스템 스캐폴딩을 자동으로 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비

Laravel의 비밀번호 재설정 기능을 사용하려면 애플리케이션의 `App\Models\User` 모델에 `Illuminate\Notifications\Notifiable` 트레이트가 포함되어 있어야 합니다. 일반적으로, 이 트레이트는 기본적으로 새로운 Laravel 애플리케이션의 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을 구현하는지 확인해야 합니다. 프레임워크에 포함된 `App\Models\User` 모델은 이미 해당 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용해 인터페이스 구현에 필요한 메서드를 제공합니다.

<a name="database-preparation"></a>
### 데이터베이스 준비

애플리케이션의 비밀번호 재설정 토큰을 저장하기 위한 테이블이 생성되어야 합니다. 일반적으로, 이는 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성

기본적으로 Laravel은 수신한 모든 요청에 HTTP 요청의 `Host` 헤더 값에 상관없이 응답합니다. 또한, 웹 요청 동안 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더의 값을 사용합니다.

일반적으로 Nginx, Apache와 같은 웹 서버에서 주어진 호스트명과 일치하는 요청만 애플리케이션에 전달되도록 구성해야 합니다. 그러나 직접 웹 서버를 커스터마이징할 수 없는 경우 Laravel이 특정 호스트에만 응답하도록 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용할 수 있습니다. 이는 애플리케이션에서 비밀번호 재설정 기능을 제공할 때 매우 중요합니다.

이 미들웨어 메서드에 대해 더 자세히 알고 싶다면 [TrustHosts 미들웨어 문서](/docs/{{version}}/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있도록 지원하려면 몇 가지 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있도록 하는 라우트 2개가 필요합니다. 두 번째로, 사용자가 이메일로 받은 비밀번호 재설정 링크에 접속해 실제로 비밀번호를 재설정할 수 있도록 처리하는 라우트 2개도 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트를 정의합니다. 우선, 비밀번호 재설정 링크 요청 폼이 포함된 뷰를 반환하는 라우트를 정의합니다:

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트에서 반환하는 뷰에는 사용자가 지정한 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있는 `email` 필드가 있는 폼이 포함되어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호 찾기" 뷰의 폼 제출 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고 해당 사용자에게 비밀번호 재설정 요청을 보내는 역할을 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

Route::post('/forgot-password', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::ResetLinkSent
        ? back()->with(['status' => __($status)])
        : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');
```

진행하기 전에 이 라우트를 좀 더 자세히 살펴보겠습니다. 먼저 요청의 `email` 속성이 검증됩니다. 그 다음, Laravel의 내장 "패스워드 브로커"(`Password` 파사드)를 사용해 해당 사용자에게 비밀번호 재설정 링크를 전송합니다. 패스워드 브로커는 주어진 필드(이 경우는 이메일 주소)로 사용자를 조회하고, Laravel의 내장 [알림 시스템](/docs/{{version}}/notifications)을 통해 비밀번호 재설정 링크를 보냅니다.

`sendResetLink` 메서드는 상태값("status" 슬러그)를 반환합니다. 이 상태값은 Laravel의 [다국어](/docs/{{version}}/localization) 도우미를 사용해 사용자에게 알기 쉬운 메시지로 번역할 수 있습니다. 비밀번호 재설정 상태의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 각 상태값에 대한 항목이 해당 언어 파일에 위치해 있습니다.

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 발행할 수 있습니다.

`Password` 파사드의 `sendResetLink` 메서드 호출 시 Laravel이 어떻게 사용자를 데이터베이스에서 조회하는지 궁금할 수 있습니다. Laravel 패스워드 브로커는 인증 시스템의 "유저 프로바이더"를 통해 데이터베이스 레코드를 조회합니다. 패스워드 브로커가 사용하는 유저 프로바이더는 `config/auth.php` 구성 파일의 `passwords` 설정 배열에서 지정됩니다. 커스텀 유저 프로바이더 작성 방법은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참조하세요.

> [!NOTE]
> 비밀번호 재설정을 직접 구현할 경우, 뷰와 라우트의 내용을 직접 정의해야 합니다. 모든 인증 및 검증 로직이 포함된 스캐폴딩이 필요하다면 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

다음으로 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭하고 새 비밀번호를 입력할 수 있도록 실제 비밀번호 재설정을 위한 라우트를 정의해야 합니다. 먼저 사용자가 재설정 링크를 클릭하면 표시되는 비밀번호 재설정 폼을 보여주는 라우트를 정의하겠습니다. 이 라우트는 나중에 비밀번호 재설정 요청의 유효성을 검증하는 데 사용할 `token` 파라미터를 받습니다:

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트에서 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 비밀 `$token` 값을 담는 숨겨진 `token` 필드가 있는 폼이 표시되어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론, 실제로 비밀번호 재설정 폼 제출을 처리할 라우트도 정의해야 합니다. 이 라우트는 들어온 요청을 검증하고 사용자의 비밀번호를 데이터베이스에서 업데이트합니다:

```php
use App\Models\User;
use Illuminate\Auth\Events\PasswordReset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;

Route::post('/reset-password', function (Request $request) {
    $request->validate([
        'token' => 'required',
        'email' => 'required|email',
        'password' => 'required|min:8|confirmed',
    ]);

    $status = Password::reset(
        $request->only('email', 'password', 'password_confirmation', 'token'),
        function (User $user, string $password) {
            $user->forceFill([
                'password' => Hash::make($password)
            ])->setRememberToken(Str::random(60));

            $user->save();

            event(new PasswordReset($user));
        }
    );

    return $status === Password::PasswordReset
        ? redirect()->route('login')->with('status', __($status))
        : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');
```

진행하기 전에 이 라우트를 좀 더 자세히 살펴보겠습니다. 먼저 요청의 `token`, `email`, `password` 속성이 검증됩니다. 그 다음, Laravel의 내장 "패스워드 브로커"(`Password` 파사드)를 사용해 비밀번호 재설정 요청 자격을 검증합니다.

토큰, 이메일, 비밀번호가 모두 유효하다면 `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에서 입력받은 평문 비밀번호를 전달받으며, 이 내부에서 데이터베이스의 사용자 비밀번호를 업데이트할 수 있습니다.

`reset` 메서드는 상태값("status" 슬러그)를 반환합니다. 이 값은 Laravel의 [다국어](/docs/{{version}}/localization) 도우미를 통해 사용자에게 알기 쉬운 메시지로 번역해 보여줄 수 있습니다. 비밀번호 재설정 상태의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 정의되며, 각 상태값별로 항목이 위치해 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

진행하기 전에, `Password` 파사드의 `reset` 메서드 호출 시 Laravel이 어떻게 사용자 레코드를 데이터베이스에서 가져오는지 궁금할 수 있습니다. Laravel 패스워드 브로커는 인증 시스템의 "유저 프로바이더"를 통해 데이터베이스 레코드를 조회합니다. 어떤 유저 프로바이더를 사용할지는 `config/auth.php` 파일의 `passwords` 설정 배열에서 지정합니다. 커스텀 유저 프로바이더 작성법은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

만료된 비밀번호 재설정 토큰도 데이터베이스에 남아 있을 수 있습니다. 그러나 다음과 같이 `auth:clear-resets` Artisan 명령어로 손쉽게 이 레코드들을 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하고 싶다면 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 해당 명령어를 추가할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이즈

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이즈

`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하여 비밀번호 재설정 링크 URL을 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 전달받는 클로저를 인자로 받습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider`의 `boot` 메서드 내부에서 호출합니다.

```php
use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    ResetPassword::createUrlUsing(function (User $user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}
```

<a name="reset-email-customization"></a>
#### 재설정 이메일 커스터마이즈

사용자에게 비밀번호 재설정 링크를 보내는 데 사용되는 알림 클래스를 쉽게 수정할 수 있습니다. 시작하려면 `App\Models\User` 모델의 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내부에서는 자신이 만든 [알림 클래스](/docs/{{version}}/notifications)를 사용해 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`이 이 메서드로 전달되는 첫 번째 인자입니다. 이 `$token`을 사용해 원하는 비밀번호 재설정 URL을 빌드하고, 사용자에게 알림을 보낼 수 있습니다:

```php
use App\Notifications\ResetPasswordNotification;

/**
 * Send a password reset notification to the user.
 *
 * @param  string  $token
 */
public function sendPasswordResetNotification($token): void
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```
