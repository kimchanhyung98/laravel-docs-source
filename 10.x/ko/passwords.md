# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이징](#password-customization)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 웹 애플리케이션은 사용자가 비밀번호를 잊었을 때 재설정할 수 있는 기능을 제공합니다. 매번 애플리케이션을 만들 때마다 이를 직접 구현하는 대신, Laravel은 비밀번호 재설정 링크를 보내고 보안적으로 비밀번호를 재설정할 수 있는 편리한 서비스를 제공합니다.

> [!NOTE]  
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 Laravel [애플리케이션 스타터 키트](/docs/10.x/starter-kits)를 설치하세요. Laravel의 스타터 키트는 비밀번호 재설정을 포함한 전체 인증 시스템의 뼈대를 자동으로 구성해 줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델은 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 보통 이 트레이트는 새로 생성된 Laravel 애플리케이션의 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하는지 확인하세요. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 이 인터페이스 구현에 필요한 메서드를 포함하는 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용합니다.

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블을 만들어야 합니다. 이 테이블에 대한 마이그레이션은 기본 Laravel 애플리케이션에 포함되어 있으므로, 데이터베이스를 마이그레이션하여 테이블만 생성하면 됩니다.

```shell
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 모든 요청에 응답합니다. 그리고 `Host` 헤더 값은 웹 요청 중 애플리케이션의 절대 URL 생성에 사용됩니다.

보통은 Nginx, Apache 같은 웹 서버를 설정하여 특정 호스트 이름에 해당하는 요청만 애플리케이션에 전달하도록 합니다. 그러나 웹 서버를 직접 설정할 수 없고 Laravel에서 특정 호스트 이름에만 응답하게 해야 한다면, 애플리케이션에 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다. 이는 특히 비밀번호 재설정 기능을 제공하는 경우 중요합니다.

이 미들웨어에 대해 더 알고 싶다면 [`TrustHosts` 미들웨어 문서](/docs/10.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 요청 처리 라우트 두 개가 필요합니다. 그리고 사용자가 이메일로 받은 재설정 링크를 클릭하여 새 비밀번호를 제출할 때 비밀번호를 실제로 변경하는 라우트 두 개가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting the Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼 (The Password Reset Link Request Form)

먼저 비밀번호 재설정 링크 요청 폼을 보여주는 라우트를 정의합니다. 다음 예시는 비밀번호 재설정 링크 요청 폼이 포함된 뷰를 반환합니다.

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰는 `email` 필드가 있는 폼을 포함해야 하며, 사용자가 특정 이메일 주소에 대한 비밀번호 재설정 링크를 요청할 수 있게 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling the Form Submission)

다음으로, "비밀번호 찾기" 뷰에서 제출된 폼 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

Route::post('/forgot-password', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::RESET_LINK_SENT
                ? back()->with(['status' => __($status)])
                : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');
```

자세히 살펴보면, 먼저 요청된 이메일 속성을 검증합니다. 그리고 Laravel 내장 "비밀번호 브로커"(`Password` 파사드)를 사용해 비밀번호 재설정 링크를 사용자에게 전송합니다. 비밀번호 브로커는 주어진 필드(여기서는 이메일)에 해당하는 사용자 정보를 찾아 Laravel 내장 [알림 시스템](/docs/10.x/notifications)을 통해 비밀번호 재설정 링크를 보냅니다.

`sendResetLink` 메서드는 상태 슬러그("status")를 반환하며, Laravel의 [로컬라이제이션](/docs/10.x/localization) 헬퍼를 사용해 사용자가 이해하기 쉬운 메시지로 변환할 수 있습니다. 이 상태 메시지는 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 정의되어 있습니다. 각 상태 값에 대한 항목이 `passwords` 언어 파일 내에 위치합니다.

> [!NOTE]  
> 기본 Laravel 애플리케이션 뼈대에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자화하려면 `lang:publish` Artisan 명령어로 파일을 공개하세요.

`Password` 파사드의 `sendResetLink` 호출 시 Laravel이 어떻게 사용자 정보를 데이터베이스에서 가져오는지 궁금할 수 있습니다. Laravel 비밀번호 브로커는 인증 시스템의 "유저 프로바이더"를 사용해서 데이터베이스 레코드를 조회합니다. 비밀번호 브로커가 사용하는 유저 프로바이더는 `config/auth.php` 설정 파일의 `passwords` 배열에 정의되어 있습니다. 사용자화된 유저 프로바이더 작성법은 [인증 문서](/docs/10.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]  
> 비밀번호 재설정을 직접 구현하면 뷰와 라우트 내용을 스스로 정의해야 합니다. 인증과 검증 로직을 모두 포함하는 자동 스캐폴딩이 필요하면 [Laravel 애플리케이션 스타터 키트](/docs/10.x/starter-kits)를 확인하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼 (The Password Reset Form)

이제 실제로 비밀번호를 재설정하는 데 필요한 라우트를 정의합니다. 사용자가 이메일로 받은 재설정 링크를 클릭하면 비밀번호 재설정 폼을 보여주어야 합니다. 이 라우트는 나중에 재설정 요청을 검증하는 데 사용할 `token` 파라미터를 받습니다.

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰는 `email`, `password`, `password_confirmation` 필드와 함께 숨겨진 `token` 필드를 포함하는 폼을 표시해야 하며, `token` 필드에는 라우트에서 받은 비밀 토큰 값이 들어갑니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling the Form Submission)

비밀번호 재설정 폼 제출을 실제로 처리할 라우트도 정의해야 합니다. 이 라우트는 요청을 검증하고 데이터베이스에서 사용자의 비밀번호를 업데이트합니다.

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

    return $status === Password::PASSWORD_RESET
                ? redirect()->route('login')->with('status', __($status))
                : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');
```

이 라우트를 자세히 보면, 먼저 `token`, `email`, `password` 필드에 대해 검증합니다. 그 후 Laravel 내장 비밀번호 브로커(`Password` 파사드)를 사용해 재설정 요청 자격 증명이 유효한지 검증합니다.

토큰, 이메일 주소, 비밀번호가 모두 유효하면 `reset` 메서드에 전달한 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에서 제출된 평문 비밀번호를 인수로 받으며, 여기서 사용자의 비밀번호를 데이터베이스에 업데이트합니다.

`reset` 메서드도 상태 슬러그를 반환하며, 이전처럼 로컬라이제이션 헬퍼로 친숙한 메시지로 변환이 가능합니다. 상태 메시지 정의는 `lang/{lang}/passwords.php` 언어 파일에 있습니다. 만약 `lang` 디렉토리가 없다면 `lang:publish` Artisan 명령으로 생성할 수 있습니다.

`Password` 파사드의 `reset` 메서드를 호출할 때 Laravel이 어떻게 사용자 레코드를 찾아오는지 궁금하다면, 앞서 설명한 것처럼 인증 시스템의 유저 프로바이더가 이 역할을 수행합니다. 사용자화 프로바이더는 `config/auth.php`의 `passwords` 배열에서 설정합니다. 자세한 내용은 [인증 문서](/docs/10.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

만료된 비밀번호 재설정 토큰은 데이터베이스에 여전히 남아있을 수 있습니다. 그러나 `auth:clear-resets` Artisan 명령을 사용해 쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하고 싶으면 애플리케이션의 [스케줄러](/docs/10.x/scheduling)에 해당 명령을 등록하는 것도 좋은 방법입니다:

```php
$schedule->command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이징 (Reset Link Customization)

비밀번호 재설정 링크 URL은 `ResetPassword` 알림 클래스가 제공하는 `createUrlUsing` 메서드로 사용자화할 수 있습니다. 이 메서드는 두 인수를 받는 클로저를 인자로 받아, 알림을 받는 사용자 인스턴스와 재설정 링크 토큰 값을 전달합니다. 보통 이 설정은 `App\Providers\AuthServiceProvider` 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다.

```php
use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    ResetPassword::createUrlUsing(function (User $user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}
```

<a name="reset-email-customization"></a>
#### 재설정 이메일 커스터마이징 (Reset Email Customization)

비밀번호 재설정 링크를 보내는 알림 클래스를 쉽게 변경할 수도 있습니다. 우선, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서 자신이 만든 어떤 [알림 클래스](/docs/10.x/notifications)든 사용해 알림을 전송할 수 있습니다. 비밀번호 재설정 `$token`은 이 메서드의 첫 번째 인자로 전달되며, 이를 이용해 재설정 URL을 만들고 사용자에게 알림을 보냅니다.

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