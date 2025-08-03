# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청하기](#requesting-the-password-reset-link)
    - [비밀번호 재설정하기](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이징](#password-customization)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 기능을 제공합니다. 매번 애플리케이션마다 이 기능을 직접 구현하는 대신, Laravel은 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정을 위한 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [애플리케이션 스타터 킷(starter kit)](/docs/9.x/starter-kits)을 설치하세요. Laravel의 스타터 킷은 잊어버린 비밀번호 재설정을 포함한 전체 인증 시스템의 기본 뼈대를 자동으로 구축해줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델은 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 보통 이 트레이트는 새로운 Laravel 애플리케이션 생성 시 기본으로 포함되어 있습니다.

다음으로, `App\Models\User` 모델에서 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현했는지 확인하세요. Laravel 프레임워크에 기본 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용해 필요한 메서드를 포함하고 있습니다.

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

애플리케이션의 비밀번호 재설정 토큰을 저장하기 위해 테이블이 필요합니다. 이 테이블의 마이그레이션은 기본 Laravel 애플리케이션에 포함되어 있으므로, 다음 명령어로 데이터베이스 마이그레이션만 실행하면 됩니다:

```shell
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청 `Host` 헤더 내용과 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 도중 절대 URL을 생성할 때 `Host` 헤더 값을 사용합니다.

보통은 Nginx, Apache 같은 웹 서버에서 특정 호스트 이름에만 애플리케이션 요청이 전달되도록 설정합니다. 하지만 웹 서버를 직접 제어할 수 없는 경우, Laravel 쪽에서 응답할 호스트 이름을 제한해야 할 수도 있습니다. 이 경우, `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다. 이는 비밀번호 재설정 기능이 있는 애플리케이션에서 특히 중요합니다.

자세한 내용은 [`TrustHosts` 미들웨어 문서](/docs/9.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정하도록 지원하려면 여러 라우트를 정의해야 합니다. 첫째, 사용자 이메일로 비밀번호 재설정 링크를 요청하는 라우트가 필요합니다. 둘째, 이메일로 받은 비밀번호 재설정 링크를 통해 비밀번호를 실제로 변경하는 라우트가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청하기 (Requesting The Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼 (The Password Reset Link Request Form)

먼저, 비밀번호 재설정 링크 요청에 필요한 라우트를 정의합니다. 사용자가 이메일 주소로 요청할 수 있는 폼을 포함하는 뷰를 반환하는 라우트를 작성해보겠습니다:

```
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 `email` 필드를 포함한 폼이 있어, 사용자가 비밀번호 재설정 링크를 요청할 이메일 주소를 입력할 수 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling The Form Submission)

다음으로, "비밀번호를 잊으셨나요" 뷰에서 폼 제출 요청을 처리하는 POST 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고 해당 사용자에게 비밀번호 재설정 요청 링크를 전송하는 역할을 합니다:

```
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

자세히 살펴보면, 먼저 요청의 `email` 속성을 유효성 검증합니다. 그다음, Laravel의 내장 "비밀번호 브로커(password broker)"를 `Password` 파사드를 통해 사용해 비밀번호 재설정 링크를 전송합니다. 비밀번호 브로커는 주어진 필드(여기서는 이메일)를 사용해 사용자를 조회하고, Laravel 내장 [알림 시스템](/docs/9.x/notifications)을 통해 비밀번호 재설정 링크를 이메일로 전송합니다.

`sendResetLink` 메서드는 상태 문자열(status slug)을 반환합니다. 이 상태 문자열은 Laravel의 [로컬라이제이션](/docs/9.x/localization) 도우미를 사용해 사용자에게 보여줄 친근한 메시지로 변환할 수 있습니다. 이 변환은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 관리하며, 상태 문자열별 항목이 정의되어 있습니다.

여기서 궁금할 수 있는 점은 `sendResetLink` 호출 시 Laravel이 어떻게 사용자 레코드를 데이터베이스에서 찾아오는가 하는 점입니다. Laravel 비밀번호 브로커는 인증 시스템의 "유저 프로바이더(user providers)"를 사용해 데이터베이스에서 사용자를 가져옵니다. 비밀번호 브로커에 사용되는 유저 프로바이더는 `config/auth.php` 파일의 `passwords` 설정 배열에서 지정됩니다. 커스텀 유저 프로바이더 작성법은 [인증 문서](/docs/9.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정을 수동으로 구현할 경우, 뷰와 라우트 내용을 직접 정의해야 합니다. 인증 및 검증 로직이 모두 포함된 뼈대가 필요하다면, [Laravel 애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 사용해 보세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정하기 (Resetting The Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼 (The Password Reset Form)

다음으로, 이메일로 받은 비밀번호 재설정 링크를 통해 실제로 비밀번호를 변경할 때 필요한 라우트를 정의합니다. 먼저, 사용자가 링크를 클릭하면 비밀번호 재설정 폼을 보여주는 GET 라우트를 만듭니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증할 `token` 매개변수를 받습니다:

```
Route::get('/reset-password/{token}', function ($token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰는 `email`, `password`, `password_confirmation` 필드와, 숨겨진 `token` 필드를 포함하는 폼을 표시해야 합니다. 이 `token` 필드에는 라우트로 전달된 비밀 토큰 값이 들어있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling The Form Submission)

물론 비밀번호 재설정 폼 제출을 처리하는 POST 라우트도 정의해야 합니다. 이 라우트는 요청을 검증하고 데이터베이스에서 사용자의 비밀번호를 업데이트하는 역할을 수행합니다:

```
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
        function ($user, $password) {
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

자세히 살펴보면, 먼저 요청의 `token`, `email`, `password` 속성들이 유효성 검증됩니다. 그다음, Laravel 내장 "비밀번호 브로커"의 `reset` 메서드로 비밀번호 재설정 요청 자격증명을 확인합니다.

토큰, 이메일, 비밀번호가 모두 유효하면, `reset` 메서드의 두 번째 인자로 전달한 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에서 입력된 평문 비밀번호를 인수로 받으며, 여기서 데이터베이스에 사용자 비밀번호를 업데이트할 수 있습니다.

`reset` 메서드도 상태 문자열(status slug)을 반환하며, 앞서 설명한 것처럼 이는 Laravel의 [로컬라이제이션] 도우미를 통해 사용자에게 친근한 메시지로 변환되어 출력됩니다. 이 메시지는 `lang/{lang}/passwords.php` 언어 파일에서 관리됩니다.

`Password` 파사드의 `reset` 메서드도 비밀번호 재설정 요청 시 사용자 레코드 조회를 위해 인증 시스템의 유저 프로바이더를 사용합니다. 해당 설정은 `config/auth.php` 파일 내 `passwords` 배열에서 확인할 수 있습니다. 커스텀 유저 프로바이더 사용법은 [인증 문서](/docs/9.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

만료된 비밀번호 재설정 토큰은 여전히 데이터베이스에 남아 있을 수 있습니다. 그러나 다음 Artisan 명령어를 사용해 쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/9.x/scheduling)에 아래처럼 등록해 주기적으로 실행할 수 있습니다:

```
$schedule->command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
### 재설정 링크 커스터마이징 (Reset Link Customization)

`ResetPassword` 알림 클래스가 제공하는 `createUrlUsing` 메서드를 사용해 비밀번호 재설정 링크 URL을 커스터마이징할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 인자로 받는 클로저를 인수로 받습니다. 보통 `App\Providers\AuthServiceProvider` 서비스 프로바이더의 `boot` 메서드 안에서 호출합니다:

```
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    ResetPassword::createUrlUsing(function ($user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}
```

<a name="reset-email-customization"></a>
### 재설정 이메일 커스터마이징 (Reset Email Customization)

비밀번호 재설정 링크 전송에 사용되는 알림 클래스를 쉽게 변경할 수 있습니다. 시작하려면 `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서, 비밀번호 재설정 `$token`을 인자로 받아 원하는 URL을 생성한 뒤, 직접 만든 [알림 클래스](/docs/9.x/notifications)를 사용해 사용자에게 알림을 발송할 수 있습니다:

```
use App\Notifications\ResetPasswordNotification;

/**
 * Send a password reset notification to the user.
 *
 * @param  string  $token
 * @return void
 */
public function sendPasswordResetNotification($token)
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```