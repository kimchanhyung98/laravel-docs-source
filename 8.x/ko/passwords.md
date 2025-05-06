# 비밀번호 재설정

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이즈](#password-customization)

<a name="introduction"></a>
## 소개

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. 여러분이 만드는 모든 애플리케이션에서 이 기능을 직접 구현하도록 강제하는 대신, Laravel은 비밀번호 재설정 링크를 전송하고 안전하게 비밀번호를 재설정할 수 있는 편리한 서비스를 제공합니다.

> {tip} 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치해보세요. Laravel의 스타터 킷은 비밀번호 재설정을 포함한 전체 인증 시스템의 뼈대를 자동으로 구성해줍니다.

<a name="model-preparation"></a>
### 모델 준비

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용하고 있는지 확인해야 합니다. 일반적으로, 이 트레이트는 새로운 Laravel 애플리케이션에서 생성되는 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하고 있는지 확인해야 합니다. 프레임워크와 함께 제공되는 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 인터페이스에 필요한 메서드를 포함하기 위해 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용합니다.

<a name="database-preparation"></a>
### 데이터베이스 준비

애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 이 테이블에 대한 마이그레이션 파일은 기본 Laravel 애플리케이션에 포함되어 있으므로, 데이터베이스를 마이그레이션하여 해당 테이블을 생성하기만 하면 됩니다:

    php artisan migrate

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정

기본적으로, Laravel은 HTTP 요청의 `Host` 헤더 값에 관계없이 수신하는 모든 요청에 응답합니다. 또한, 웹 요청 중에 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더의 값이 사용됩니다.

일반적으로, Nginx나 Apache와 같은 웹 서버에서 지정한 호스트 이름과 일치하는 요청만 애플리케이션에 전달하도록 설정해야 합니다. 그러나 직접적으로 웹 서버를 커스터마이징할 수 없는 경우, 혹은 Laravel이 특정 호스트 이름에 대해서만 응답하도록 지정해야 하는 경우, 애플리케이션의 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하여 설정할 수 있습니다. 비밀번호 재설정 기능을 제공하는 애플리케이션에서는 특히 중요한 설정입니다.

이 미들웨어에 대해 더 알고 싶다면 [`TrustHosts` 미들웨어 문서](/docs/{{version}}/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있도록 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있도록 하는 두 개의 라우트가 필요합니다. 두 번째로, 사용자가 이메일로 전송된 비밀번호 재설정 링크를 방문하여 비밀번호 재설정 폼을 제출할 수 있도록 하는 두 개의 라우트가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하는 라우트를 정의합니다. 먼저, 비밀번호 재설정 링크 요청 폼을 반환하는 뷰를 돌려주는 라우트를 만들겠습니다:

    Route::get('/forgot-password', function () {
        return view('auth.forgot-password');
    })->middleware('guest')->name('password.request');

이 라우트가 반환하는 뷰에는 사용자가 비밀번호 재설정 링크를 요청할 수 있도록 `email` 필드가 포함된 폼이 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, '비밀번호를 잊으셨나요' 뷰에서 폼 제출 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소의 유효성을 검사하고 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다:

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

진행하기 전에, 이 라우트의 주요 동작을 살펴보겠습니다. 먼저, 요청의 `email` 속성에 대해 유효성 검사가 이루어집니다. 그 다음, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 사용하여 비밀번호 재설정 링크를 사용자에게 전송합니다. 비밀번호 브로커는 지정된 필드(이 경우 이메일 주소)를 통해 사용자를 조회하고, Laravel의 내장 [알림 시스템](/docs/{{version}}/notifications)을 통해 비밀번호 재설정 링크를 전송합니다.

`sendResetLink` 메서드는 "상태" 슬러그를 반환합니다. 이 상태 코드는 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 도우미를 통해 번역되어 요청 상태에 대한 사용자 친화적인 메시지로 표시됩니다. 상태 코드별 번역은 애플리케이션의 `resources/lang/{lang}/passwords.php` 파일 내에 정의되어 있습니다.

`Password` 파사드의 `sendResetLink` 메서드를 호출할 때, Laravel이 어떻게 데이터베이스에서 사용자를 조회하는지 궁금하실 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "유저 프로바이더"를 이용하여 데이터베이스에서 사용자 레코드를 조회합니다. 어떤 유저 프로바이더를 사용할지는 `config/auth.php` 파일의 `passwords` 설정 배열에서 지정합니다. 커스텀 유저 프로바이더 만들기에 대해서는 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

> {tip} 비밀번호 재설정을 직접 구현할 때는 뷰와 라우트의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 검증 로직이 포함된 뼈대를 원한다면 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 참고하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

다음으로, 사용자가 이메일로 전송된 비밀번호 재설정 링크를 클릭한 후 새 비밀번호를 입력하여 실제로 비밀번호를 재설정할 수 있도록 필요한 라우트를 정의합니다. 먼저, 사용자가 비밀번호 재설정 링크를 클릭했을 때 표시되는 재설정 폼 라우트를 정의합시다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 사용할 `token` 파라미터를 받습니다:

    Route::get('/reset-password/{token}', function ($token) {
        return view('auth.reset-password', ['token' => $token]);
    })->middleware('guest')->name('password.reset');

이 라우트가 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드(라우트에서 받은 비밀 `$token` 값이 들어가야 함)가 포함된 폼이 표시되어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론, 실제로 비밀번호 재설정 폼 제출을 처리하는 라우트도 정의해야 합니다. 이 라우트는 요청의 유효성을 검사하고 데이터베이스의 사용자의 비밀번호를 갱신합니다:

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

진행하기 전에, 이 라우트의 동작을 상세히 살펴보겠습니다. 먼저, 요청의 `token`, `email`, `password` 속성에 대해 유효성 검사가 이루어집니다. 그 다음, Laravel의 내장 "비밀번호 브로커"(Password 파사드)를 이용하여 비밀번호 재설정 요청의 자격을 검증합니다.

토큰, 이메일 주소, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달된 클로저가 실행됩니다. 이 클로저는 비밀번호 재설정 폼에서 입력받은 평문 비밀번호와 사용자 인스턴스를 받아, 데이터베이스에 사용자의 비밀번호를 갱신합니다.

`reset` 메서드는 "상태" 슬러그를 반환합니다. 이 상태 값 역시 [로컬라이제이션](/docs/{{version}}/localization) 도우미를 이용해 번역할 수 있습니다. 상태별 번역 내용은 애플리케이션의 `resources/lang/{lang}/passwords.php` 언어 파일에 정의되어 있습니다.

이제 `Password` 파사드의 `reset` 메서드를 호출할 때 Laravel이 어떻게 애플리케이션의 데이터베이스에서 사용자 레코드를 조회하는지 궁금하실 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "유저 프로바이더"를 통해 레코드를 조회합니다. 사용되는 유저 프로바이더는 `config/auth.php` 파일의 `passwords` 설정 배열에서 지정됩니다. 커스텀 유저 프로바이더 작성법은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

만료된 비밀번호 재설정 토큰도 데이터베이스에 남아 있을 수 있습니다. 하지만, `auth:clear-resets` 아티즌 명령어를 사용하여 이러한 레코드를 쉽게 삭제할 수 있습니다:

    php artisan auth:clear-resets

이 과정을 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 다음과 같이 명령어를 추가하면 됩니다:

    $schedule->command('auth:clear-resets')->everyFifteenMinutes();

<a name="password-customization"></a>
## 커스터마이즈

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이즈

`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하면 비밀번호 재설정 링크의 URL을 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받을 사용자 인스턴스와 비밀번호 재설정 토큰을 인자로 받는 클로저를 인자로 받습니다. 보통 이 메서드는 `App\Providers\AuthServiceProvider` 서비스 제공자의 `boot` 메서드에서 호출해야 합니다:

    use Illuminate\Auth\Notifications\ResetPassword;

    /**
     * 인증/인가 서비스를 등록합니다.
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

<a name="reset-email-customization"></a>
#### 재설정 이메일 커스터마이즈

비밀번호 재설정 링크를 사용자에게 전송하는 데 사용되는 알림 클래스를 쉽게 변경할 수 있습니다. 먼저, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내부에서 원하는 [알림 클래스](/docs/{{version}}/notifications)를 사용하여 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`은 이 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 사용하여 원하는 URL을 직접 만들고 사용자의 알림으로 전송하면 됩니다:

    use App\Notifications\ResetPasswordNotification;

    /**
     * 비밀번호 재설정 알림을 사용자에게 전송합니다.
     *
     * @param  string  $token
     * @return void
     */
    public function sendPasswordResetNotification($token)
    {
        $url = 'https://example.com/reset-password?token='.$token;

        $this->notify(new ResetPasswordNotification($url));
    }
