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

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 기능을 제공합니다. 매번 직접 이 기능을 구현하는 대신, Laravel은 편리하게 비밀번호 재설정 링크를 보내고 안전하게 비밀번호를 재설정할 수 있는 서비스를 제공합니다.

> [!NOTE]  
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 Laravel [application starter kit](/docs/11.x/starter-kits)을 설치해 보세요. Laravel의 스타터 키트는 잊어버린 비밀번호 재설정을 포함한 전체 인증 시스템의 기본 구성을 자동으로 처리해 줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델은 `Illuminate\Notifications\Notifiable` 트레이트를 반드시 사용해야 합니다. 일반적으로 이 트레이트는 새 Laravel 애플리케이션 생성 시 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하는지 확인하세요. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 필요한 메서드를 포함하기 위해 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용합니다.

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블을 생성해야 합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성 (Configuring Trusted Hosts)

기본적으로, Laravel은 HTTP 요청의 `Host` 헤더 내용과 무관하게 모든 요청에 응답합니다. 또한, `Host` 헤더 값은 웹 요청 중 애플리케이션의 절대 URL을 생성할 때 사용됩니다.

대개는 Nginx 또는 Apache 같은 웹 서버를 구성해 특정 호스트명에 대해서만 애플리케이션에 요청을 전달하도록 하는 것이 좋습니다. 하지만 웹 서버 구성을 직접 제어할 수 없고 Laravel에서 특정 호스트명에 대해서만 응답하도록 제한하려 할 때는, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용해 설정할 수 있습니다. 특히, 비밀번호 재설정 기능을 제공하는 애플리케이션에서는 이 설정이 중요합니다.

이 미들웨어 메서드에 대해 더 자세히 알고 싶다면 [`TrustHosts` 미들웨어 문서](/docs/11.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 하려면 여러 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있게 하는 라우트 두 개를 정의하고, 다음으로 이메일로 전송된 비밀번호 재설정 링크를 통해 실제 비밀번호를 재설정하는 라우트 두 개를 정의해야 합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting the Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청할 수 있는 라우트를 정의합니다. 다음과 같이, 비밀번호 재설정 링크 요청 폼이 포함된 뷰를 반환하는 라우트를 정의해 시작합니다:

```
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 `email` 필드가 포함된 폼이 있어야 하며, 이를 통해 사용자가 특정 이메일 주소에 대해 비밀번호 재설정 링크를 요청할 수 있습니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

이어서, "비밀번호 찾기" 뷰에서 폼 제출 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다:

```
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

이 라우트를 자세히 살펴보면, 먼저 요청의 `email` 속성을 검증합니다. 그 다음에 Laravel 내장 "password broker"를 `Password` 파사드로 사용해 비밀번호 재설정 링크를 사용자에게 전송합니다. password broker는 지정한 필드(여기서는 이메일 주소)로 사용자를 찾아내고 Laravel의 내장 [알림 시스템](/docs/11.x/notifications)을 통해 비밀번호 재설정 링크를 발송합니다.

`sendResetLink` 메서드는 상태를 나타내는 "status" 슬러그를 반환합니다. 이 상태 값은 Laravel의 [지역화](/docs/11.x/localization) 도우미를 사용해 번역 가능하며, 사용자에게 요청 처리 결과를 친절하게 알릴 메시지를 표시할 수 있습니다. 이 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정되며, 해당 언어 파일에는 상태 슬러그별로 대응되는 항목이 포함되어 있습니다.

> [!NOTE]  
> 기본 Laravel 애플리케이션 골격에는 `lang` 디렉토리가 포함되지 않습니다. 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어를 실행해 파일을 게시할 수 있습니다.

`Password` 파사드의 `sendResetLink` 메서드가 데이터베이스에서 사용자 레코드를 어떻게 조회하는지 궁금할 수 있습니다. Laravel password broker는 인증 시스템의 "user providers"를 사용해 데이터베이스 기록을 조회합니다. password broker가 사용하는 user provider는 `config/auth.php` 설정 파일 내 `passwords` 구성 배열에서 지정합니다. 사용자 정의 user provider 작성을 더 자세히 알고 싶다면 [인증 문서](/docs/11.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]  
> 비밀번호 재설정 기능을 직접 구현할 경우, 뷰와 라우트 내용을 스스로 정의해야 합니다. 모든 필요한 인증 및 검증 로직을 포함한 기본 구성을 원한다면 [Laravel application starter kits](/docs/11.x/starter-kits)를 살펴보세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

다음으로, 사용자가 이메일로 전달된 비밀번호 재설정 링크를 클릭해 새 비밀번호를 입력하기 위한 라우트를 정의합니다. 먼저, 비밀번호 재설정 링크를 클릭했을 때 비밀번호 재설정 폼을 보여주는 라우트를 정의합시다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 사용할 `token` 파라미터를 받습니다:

```
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰는 `email`, `password`, `password_confirmation` 필드와 함께, 비밀 값인 `$token`을 담은 숨겨진 `token` 필드를 포함하는 폼을 표시해야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론 비밀번호 재설정 폼 제출을 처리할 라우트를 정의해야 합니다. 이 라우트는 요청을 검증하고, 데이터베이스에서 사용자의 비밀번호를 갱신하는 역할을 합니다:

```
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

이 라우트를 좀 더 자세히 보면, 먼저 요청 내의 `token`, `email`, `password` 속성을 검증합니다. 그 다음, Laravel 내장 "password broker"(Password 파사드)를 사용해서 비밀번호 재설정 요청의 유효성을 검사합니다.

만약 토큰, 이메일 주소, 비밀번호가 유효하면, `reset` 메서드에 전달된 클로저가 호출됩니다. 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에서 받은 평문 비밀번호를 인자로 받으며, 이를 통해 데이터베이스에서 사용자의 비밀번호를 갱신할 수 있습니다.

`reset` 메서드도 상태를 나타내는 "status" 슬러그를 반환하며, 이전 단계와 마찬가지로 [지역화](/docs/11.x/localization) 도우미를 통해 사용자에게 친절한 메시지를 보여 줄 수 있습니다. 이 메시지 역시 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 정의합니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

마지막으로, `Password` 파사드의 `reset` 메서드가 데이터베이스에서 사용자 기록을 어떻게 조회하는지도 궁금할 수 있습니다. password broker는 인증 시스템의 user provider를 활용하며, 설정은 `config/auth.php` 내 `passwords` 배열에서 확인 가능합니다. 사용자 정의 user provider 작성에 대해서는 [인증 문서](/docs/11.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

만료된 비밀번호 재설정 토큰은 여전히 데이터베이스에 남아 있을 수 있습니다. 하지만 `auth:clear-resets` Artisan 명령어로 이 레코드들을 쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 작업을 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/11.x/scheduling)에 이 명령어를 추가할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이징 (Reset Link Customization)

비밀번호 재설정 링크 URL을 커스터마이징 하고 싶다면, `ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 링크 토큰을 받는 클로저를 인자로 받습니다. 일반적으로 이 메서드는 `App\Providers\AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```
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

사용자에게 비밀번호 재설정 링크를 보내는 알림 클래스를 쉽게 수정할 수 있습니다. 시작하려면, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 안에서 직접 만든 [알림 클래스](/docs/11.x/notifications)를 사용해 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`은 이 메서드가 받는 첫 번째 인자이며, 이를 활용해 원하는 비밀번호 재설정 URL을 구축하고 사용자에게 알림을 전송할 수 있습니다:

```
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