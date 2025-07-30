# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
    - [신뢰할 수 있는 호스트 구성](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이징](#password-customization)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 웹 애플리케이션은 사용자가 비밀번호를 잊었을 때 비밀번호를 재설정할 수 있는 방법을 제공합니다. 매번 직접 다시 구현할 필요 없이, Laravel은 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정을 위한 편리한 서비스를 제공합니다.

> [!TIP]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 Laravel [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치하세요. Laravel 스타터 킷은 비밀번호 재설정을 포함한 전체 인증 시스템의 기본 구조를 자동으로 구성해 줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 위해서는 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 보통 이 트레이트는 새 Laravel 애플리케이션과 함께 생성되는 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

그다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을 구현하는지 확인하세요. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용해 필요한 메서드를 포함하고 있습니다.

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 생성되어 있어야 합니다. 이 테이블에 관한 마이그레이션은 기본 Laravel 애플리케이션에 포함되어 있으므로, 단순히 데이터베이스 마이그레이션만 수행하면 됩니다:

```
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 모든 요청에 응답합니다. 또한 웹 요청 중 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더 값을 사용합니다.

일반적으로, Nginx 또는 Apache 같은 웹 서버를 구성하여 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 전달하도록 하는 것이 좋습니다. 그러나 웹 서버를 직접 구성할 수 없는 경우, Laravel이 특정 호스트 이름에만 응답하도록 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화할 수 있습니다. 이는 특히 비밀번호 재설정 기능을 제공할 때 중요합니다.

이 미들웨어에 대해 자세히 알고 싶다면 [`TrustHosts` 미들웨어 문서](/docs/{{version}}/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 지원하려면 여러 라우트를 정의해야 합니다. 먼저, 이메일 주소를 사용해 비밀번호 재설정 링크를 요청하는 기능을 위한 라우트 쌍이 필요합니다. 다음으로, 재설정 링크를 클릭해 비밀번호 재설정 폼을 작성하고 제출하는 과정을 위한 라우트 쌍이 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting The Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼 (The Password Reset Link Request Form)

먼저, 비밀번호 재설정 링크 요청을 위한 라우트를 정의합니다. 시작하려면, 비밀번호 재설정 링크 요청 폼을 보여 주는 뷰를 반환하는 라우트를 정의하세요:

```
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 `email` 필드를 포함한 폼이 있어야 하며, 사용자가 비밀번호 재설정 링크를 요청할 이메일 주소를 입력할 수 있도록 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling The Form Submission)

다음으로, "비밀번호 찾기" 뷰에서 제출된 폼 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고 관련 사용자에게 비밀번호 재설정 링크를 전송하는 역할을 합니다:

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

잠시 이 라우트를 자세히 살펴보겠습니다. 먼저 요청된 이메일 속성이 유효한지 검증합니다. 그 다음, Laravel의 내장된 "password broker"를 `Password` 파사드를 통해 사용해 비밀번호 재설정 링크를 전송합니다. password broker는 주어진 필드(여기서는 이메일 주소)를 통해 사용자를 조회하고, Laravel의 내장 [알림 시스템](/docs/{{version}}/notifications)을 사용해 비밀번호 재설정 링크를 사용자에게 전송하는 일을 담당합니다.

`sendResetLink` 메서드는 상태를 나타내는 "status" 슬러그를 반환합니다. 이 상태는 Laravel의 [지역화](/docs/{{version}}/localization) 도구를 써서 사용자 친화적인 메시지로 변환되어 출력할 수 있습니다. 비밀번호 재설정 상태에 관한 번역은 애플리케이션 내 `resources/lang/{lang}/passwords.php` 언어 파일에 정의되어 있으며, 상태 슬러그별로 해당 메시지가 포함되어 있습니다.

Laravel이 `Password` 파사드의 `sendResetLink` 메서드 호출 시 어떻게 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수 있습니다. Laravel의 password broker는 인증 시스템의 "user providers"를 사용해 DB 레코드를 조회합니다. 이 user provider는 `config/auth.php` 설정 파일의 `passwords` 구성 배열에서 설정됩니다. 커스텀 user provider 작성에 관해 더 알고 싶다면 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

> [!TIP]
> 비밀번호 재설정을 직접 구현할 경우, 라우트와 뷰의 내용을 직접 정의해야 합니다. 모든 필요한 인증 및 검증 로직이 포함된 스캐폴딩을 원한다면 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 확인해 보세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting The Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼 (The Password Reset Form)

다음으로, 사용자가 이메일로 전송된 비밀번호 재설정 링크를 클릭해 새로운 비밀번호를 입력할 수 있도록 하는 폼을 보여 주는 라우트를 정의합니다. 이 라우트는 이후 비밀번호 재설정 요청 검증에 사용할 `token` 파라미터를 받습니다:

```
Route::get('/reset-password/{token}', function ($token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰에는 `email`, `password`, `password_confirmation` 필드와 숨겨진 `token` 필드가 포함되어야 하며, `token` 필드에는 라우트에서 받은 비밀 토큰이 담겨 있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling The Form Submission)

물론, 비밀번호 재설정 폼 제출을 처리하는 라우트도 정의해야 합니다. 이 라우트는 요청의 유효성을 검증하고, 데이터베이스에서 사용자의 비밀번호를 실제로 업데이트하는 역할을 합니다:

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

이 라우트를 살펴보면, 먼저 요청 값인 `token`, `email`, `password`의 유효성을 검증합니다. 그 뒤, `Password` 파사드를 통해 내장된 password broker를 사용하여 제출된 자격증명으로 비밀번호 재설정 요청의 유효성을 확인합니다.

만약 비밀번호 재설정 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 원문 비밀번호를 전달받으며, 여기서 데이터베이스에 사용자의 비밀번호를 업데이트합니다.

`reset` 메서드는 "status" 슬러그를 반환합니다. 이 상태는 Laravel의 [지역화](/docs/{{version}}/localization)를 이용해 사용자에게 친숙한 메시지로 변환할 수 있습니다. 이 상태 메시지에 관한 번역은 애플리케이션의 `resources/lang/{lang}/passwords.php` 언어 파일에 정의돼 있습니다.

또한, Laravel이 `Password` 파사드의 `reset` 메서드 호출 시 어떻게 사용자 레코드를 DB에서 조회하는지 궁금하다면, 앞서 설명한 것처럼 password broker가 인증 시스템의 user providers를 이용합니다. user provider 설정은 `config/auth.php`의 `passwords` 배열에서 정의되어 있습니다. 커스텀 user provider 작성에 관해서는 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

만료된 비밀번호 재설정 토큰은 데이터베이스에 여전히 남아 있을 수 있습니다. 하지만 `auth:clear-resets` Artisan 명령어를 사용해 쉽게 삭제할 수 있습니다:

```
php artisan auth:clear-resets
```

이 작업을 자동화하고 싶다면 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 명령어를 추가하는 방식을 고려하세요:

```
$schedule->command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 URL 커스터마이징 (Reset Link Customization)

`ResetPassword` 알림 클래스가 제공하는 `createUrlUsing` 메서드를 사용해 비밀번호 재설정 링크 URL을 커스터마이징할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 전달받는 클로저를 인수로 받습니다. 보통 이 메서드를 `App\Providers\AuthServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
#### 비밀번호 재설정 이메일 커스터마이징 (Reset Email Customization)

비밀번호 재설정 링크를 사용자에게 보내는 알림 클래스를 쉽게 수정할 수 있습니다. 시작하려면, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서 직접 생성한 [알림 클래스](/docs/{{version}}/notifications)를 사용해 재설정 알림을 보낼 수 있습니다. 비밀번호 재설정 토큰 `$token`은 첫 번째 인자로 전달되며, 이를 이용해 원하는 비밀번호 재설정 URL을 구성해 사용자를 대상으로 알림을 보낼 수 있습니다:

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