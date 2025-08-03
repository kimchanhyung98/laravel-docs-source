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

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 기능을 제공합니다. 매번 모든 애플리케이션에서 이 기능을 직접 구현하는 대신, Laravel은 비밀번호 재설정 링크 발송과 안전한 비밀번호 재설정을 위한 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 Laravel [애플리케이션 스타터 킷](/docs/master/starter-kits)을 설치해보세요. 스타터 킷은 잊어버린 비밀번호 재설정을 포함한 전체 인증 시스템의 스캐폴딩(구성)을 자동으로 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델에는 `Illuminate\Notifications\Notifiable` 트레이트가 반드시 포함되어야 합니다. 일반적으로 이 트레이트는 새 Laravel 애플리케이션에 기본으로 생성되는 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하고 있는지 확인하세요. 프레임워크가 제공하는 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 이 인터페이스 구현에 필요한 메서드를 포함하기 위해 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용합니다.

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블을 생성해야 합니다. 보통 이 테이블 생성은 Laravel 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청 `Host` 헤더의 내용과 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 중 절대 URL을 생성할 때 이 `Host` 헤더 값을 사용합니다.

보통은 Nginx나 Apache 같은 웹 서버에서 주어진 호스트명과 일치하는 요청만 애플리케이션에 전달하도록 설정하는 것이 좋습니다. 하지만 웹 서버 설정을 직접 변경할 수 없거나, Laravel이 특정 호스트로만 응답하도록 제한해야 하는 경우, 애플리케이션의 `bootstrap/app.php` 파일 내 `trustHosts` 미들웨어 메서드를 사용해 이 작업을 수행할 수 있습니다. 특히 비밀번호 재설정 기능을 제공하는 애플리케이션에서는 이 설정이 중요합니다.

해당 미들웨어 메서드에 관한 자세한 내용은 [`TrustHosts` 미들웨어 문서](/docs/master/requests#configuring-trusted-hosts)를 참고하시기 바랍니다.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 정상적으로 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 자신의 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있도록 하는 라우트가 필요합니다. 그리고 사용자가 이메일로 받은 비밀번호 재설정 링크를 방문하여 새 비밀번호를 제출했을 때 실제로 비밀번호를 재설정하는 라우트도 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting the Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼 (The Password Reset Link Request Form)

먼저 비밀번호 재설정 링크 요청에 필요한 라우트를 정의해보겠습니다. 다음은 비밀번호 재설정 링크 요청 폼을 반환하는 라우트 예시입니다:

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 사용자가 비밀번호 재설정 링크를 요청할 이메일 주소를 입력할 수 있는 `email` 필드를 포함하는 폼이 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling the Form Submission)

다음으로, "비밀번호 잊음" 뷰에서 전송하는 폼 제출 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고 해당 사용자에게 비밀번호 재설정 링크를 전송하는 역할을 합니다:

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

좀 더 자세히 살펴보면, 요청의 `email` 속성을 유효성 검증한 후 Laravel 내장 "패스워드 브로커"를 `Password` 파사드로 호출하여 비밀번호 재설정 링크를 사용자에게 전송합니다. 패스워드 브로커는 이메일로 사용자를 데이터베이스에서 찾아 Laravel 내장 [알림 시스템](/docs/master/notifications)을 이용해 비밀번호 재설정 링크를 발송합니다.

`sendResetLink` 메서드는 상태 슬러그(status slug)를 반환하는데, Laravel의 [로컬라이제이션](/docs/master/localization) 도움 함수인 `__()`를 이용해 사용자에게 친숙한 메시지로 변환할 수 있습니다. 이 상태 메시지는 애플리케이션 내 `lang/{lang}/passwords.php` 언어 파일에서 관리하며, 각 상태값에 대한 항목이 포함되어 있습니다.

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 커스터마이징하고 싶다면 `lang:publish` Artisan 명령어로 파일을 발행할 수 있습니다.

Laravel이 `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 어떻게 데이터베이스에서 사용자 레코드를 찾아내는지 궁금할 수 있습니다. Laravel 패스워드 브로커는 인증 시스템의 "유저 프로바이더(user providers)"를 사용해 데이터베이스 레코드를 조회합니다. 패스워드 브로커가 사용하는 유저 프로바이더는 `config/auth.php` 설정 파일의 `passwords` 설정 배열에서 지정됩니다. 커스텀 유저 프로바이더 작성 방법은 [인증 문서](/docs/master/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 직접 비밀번호 재설정 기능을 구현하는 경우, 뷰와 라우트 내용을 모두 정의해야 합니다. 모든 인증과 검증 로직이 포함된 스캐폴딩이 필요하다면 [Laravel 애플리케이션 스타터 킷](/docs/master/starter-kits)을 확인해보세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼 (The Password Reset Form)

이제 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 새 비밀번호를 입력할 수 있게 할 라우트를 정의합니다. 먼저, 비밀번호 재설정 폼을 보여주는 라우트입니다. 이 라우트는 비밀번호 재설정 요청 검증에 사용할 `token` 파라미터를 받습니다:

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰는 `email`, `password`, `password_confirmation` 필드를 포함하는 폼과, 라우트가 받은 비밀 토큰인 `token` 값을 담는 숨겨진 필드를 포함해야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling the Form Submission)

물론, 비밀번호 재설정 폼의 제출 요청을 처리하는 라우트도 정의해야 합니다. 이 라우트는 요청 유효성을 검사하고, 비밀번호를 데이터베이스에 업데이트하는 역할을 합니다:

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

좀 더 깊게 보면, 이 라우트는 요청으로부터 `token`, `email`, `password` 속성의 유효성을 먼저 검사합니다. 이후 Laravel 내장 "패스워드 브로커"를 `Password` 파사드로 호출해 비밀번호 재설정 요청 자격 증명을 검증합니다.

만약 토큰, 이메일 주소, 비밀번호 정보가 전부 유효하다면, `reset` 메서드에 전달한 클로저가 호출됩니다. 이 클로저는 비밀번호 재설정 폼에서 받은 평문 비밀번호와 사용자 인스턴스를 인자로 받아 데이터베이스에서 비밀번호를 업데이트합니다.

`reset` 메서드는 상태 슬러그를 반환하며, 이 상태값 역시 Laravel의 [로컬라이제이션](/docs/master/localization) 도우미를 통해 사용자에게 보여줄 친숙한 메시지로 변환할 수 있습니다. 상태 메시지 번역은 애플리케이션 내 `lang/{lang}/passwords.php` 언어 파일에 정의되어 있으며, 필요한 경우 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

다시 한번, `Password` 파사드의 `reset` 메서드가 어떻게 데이터베이스에서 사용자 레코드를 찾는지 궁금할 수 있습니다. Laravel 패스워드 브로커는 인증 시스템의 "유저 프로바이더"를 사용해 사용자 정보를 조회합니다. 패스워드 브로커가 사용하는 유저 프로바이더는 `config/auth.php` 설정 파일의 `passwords` 설정 배열에서 지정되어 있습니다. 커스텀 유저 프로바이더 작성 방법은 [인증 문서](/docs/master/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

비밀번호 재설정 토큰 중 만료된 것은 여전히 데이터베이스에 남아 있을 수 있습니다. 하지만 `auth:clear-resets` Artisan 명령어로 간단히 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 작업을 정기적으로 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/master/scheduling)에 아래처럼 명령어를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이징 (Reset Link Customization)

비밀번호 재설정 링크 URL은 `ResetPassword` 알림(Notification) 클래스가 제공하는 `createUrlUsing` 메서드로 커스터마이징할 수 있습니다. 이 메서드는 비밀번호 재설정 알림을 받는 사용자 인스턴스와 토큰을 인자로 받는 클로저를 받습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 서비스 프로바이더 `boot` 메서드 내에서 호출합니다:

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
#### 재설정 이메일 커스터마이징 (Reset Email Customization)

사용자에게 비밀번호 재설정 링크를 보내는 알림 클래스를 쉽게 수정할 수 있습니다. 우선, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 해당 메서드 내에서, 직접 만든 원하는 [알림 클래스](/docs/master/notifications)를 사용해 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`은 이 메서드의 첫 번째 인자로 전달됩니다. 이 토큰을 활용해 비밀번호 재설정 URL을 생성한 후 사용자에게 알림을 전송하면 됩니다:

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