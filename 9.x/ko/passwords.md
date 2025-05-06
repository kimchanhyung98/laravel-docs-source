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

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. 애플리케이션을 만들 때마다 이를 직접 구현하도록 강요하는 대신, Laravel은 비밀번호 재설정 링크를 보내고 안전하게 비밀번호를 재설정하는 데 편리한 서비스를 제공합니다.

> **참고**
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. Laravel의 스타터 키트는 비밀번호 재설정을 포함한 전체 인증 시스템 스캐폴딩을 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 일반적으로 이 트레이트는 새로운 Laravel 애플리케이션에서 생성되는 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을 구현하는지 확인하세요. 프레임워크에 포함된 `App\Models\User` 모델은 이 인터페이스를 이미 구현하고 있으며, 필요한 메서드를 포함하기 위해 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용하고 있습니다.

<a name="database-preparation"></a>
### 데이터베이스 준비

비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 이 테이블에 대한 마이그레이션은 기본 Laravel 애플리케이션에 포함되어 있으므로, 다음과 같이 데이터베이스 마이그레이션만 실행하면 됩니다:

```shell
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 중 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더 값이 사용됩니다.

일반적으로 Nginx나 Apache와 같은 웹 서버에서 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 전달하도록 설정해야 합니다. 그러나 웹 서버를 직접 구성할 수 없는 환경에서, 특정 호스트 이름에만 Laravel이 응답하도록 하려면, 애플리케이션의 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다. 특히 애플리케이션에서 비밀번호 재설정 기능을 제공할 경우 이 설정이 중요합니다.

이 미들웨어에 대해 더 알아보려면 [`TrustHosts` 미들웨어 문서](/docs/{{version}}/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있도록 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있게 만드는 라우트 두 개가 필요합니다. 그 다음, 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭하고 폼을 제출하여 실제로 비밀번호를 재설정할 수 있도록 처리하는 라우트 두 개가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트부터 정의하겠습니다. 시작을 위해, 비밀번호 재설정 링크 요청 폼이 담긴 뷰를 반환하는 라우트를 정의합니다:

    Route::get('/forgot-password', function () {
        return view('auth.forgot-password');
    })->middleware('guest')->name('password.request');

이 라우트가 반환하는 뷰에는 `email` 필드가 포함된 폼이 있어야 하며, 사용자는 원하는 이메일 주소에 대해 비밀번호 재설정 링크를 요청할 수 있습니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호를 잊으셨나요" 뷰에서 제출한 폼을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소의 유효성을 검사하고 해당 사용자의 비밀번호 재설정 요청을 전송하는 역할을 합니다:

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

다음으로 넘어가기 전에 이 라우트를 좀 더 자세히 살펴보겠습니다. 먼저, 요청의 `email` 속성에 대한 검증이 이루어집니다. 그 다음, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 통해 사용자에게 비밀번호 재설정 링크를 보냅니다. 비밀번호 브로커는 주어진 필드(이 경우 이메일 주소)로 사용자를 조회하고, 내장 [알림 시스템](/docs/{{version}}/notifications)을 이용해 비밀번호 재설정 링크를 전송합니다.

`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 상태값은 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 헬퍼를 사용해 사용자에게 친근한 메시지도 보여줄 수 있습니다. 비밀번호 재설정 상태에 대한 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 가능한 모든 상태값에 대한 항목이 `passwords` 언어 파일 안에 위치합니다.

`Password` 파사드의 `sendResetLink` 메서드를 호출할 때, Laravel이 어떻게 애플리케이션 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수도 있습니다. Laravel 비밀번호 브로커는 인증 시스템의 "user providers"를 사용하여 데이터베이스 레코드를 읽어옵니다. 비밀번호 브로커가 사용하는 user provider는 `config/auth.php`의 `passwords` 설정 배열에서 지정됩니다. 커스텀 user provider 작성에 대해서는 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

> **참고**
> 비밀번호 재설정을 수동으로 구현할 때는 뷰와 라우트의 내용을 직접 정의해야 합니다. 모든 필요한 인증 및 검증 로직을 포함한 스캐폴딩이 필요하다면, [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 확인해보세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

다음으로, 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 새 비밀번호를 입력할 수 있도록 하는 데 필요한 라우트를 정의하겠습니다. 먼저, 사용자가 재설정 링크를 클릭할 때 표시되는 비밀번호 재설정 폼을 보여주는 라우트를 정의해보겠습니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 사용할 `token` 파라미터를 받습니다:

    Route::get('/reset-password/{token}', function ($token) {
        return view('auth.reset-password', ['token' => $token]);
    })->middleware('guest')->name('password.reset');

이 라우트가 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드(라우트에서 받은 비밀 `$token` 값이 들어가야 함)가 포함된 폼이 있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

당연히, 비밀번호 재설정 폼 제출을 실제로 처리하는 라우트도 정의해야 합니다. 이 라우트는 요청을 검증하고 데이터베이스의 사용자의 비밀번호를 갱신합니다:

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

다음으로 넘어가기 전에 이 라우트를 좀 더 자세히 살펴보겠습니다. 먼저, 요청의 `token`, `email`, `password` 속성에 대한 검증이 이루어집니다. 그 다음, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 이용해 비밀번호 재설정 요청의 자격 증명을 검증합니다.

만약 토큰, 이메일 주소, 비밀번호가 유효하다면, `reset` 메서드에 전달된 클로저(콜백 함수)가 호출됩니다. 이 클로저는 사용자의 인스턴스와 비밀번호 재설정 폼에 입력된 평문 비밀번호를 받아, 데이터베이스에서 사용자의 비밀번호를 갱신할 수 있습니다.

`reset` 메서드는 "status" 슬러그를 반환합니다. 이 상태값은 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 헬퍼를 사용해 사용자에게 친근한 메시지로 보여줄 수 있습니다. 비밀번호 재설정 상태에 대한 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정되며 가능한 모든 상태값에 대한 항목이 포함되어 있습니다.

또한, `Password` 파사드의 `reset` 메서드를 호출할 때 Laravel이 어떻게 애플리케이션 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수도 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "user providers"를 사용하여 데이터베이스 레코드를 조회하며, 비밀번호 브로커에서 사용하는 user provider는 `config/auth.php`의 `passwords` 설정 배열에서 지정됩니다. 커스텀 user provider 작성에 관련해서는 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

만료된 비밀번호 재설정 토큰도 여전히 데이터베이스에 남아 있을 수 있습니다. 그러나 `auth:clear-resets` 아티즌 명령어로 이 레코드들을 손쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하려면, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 해당 명령어를 추가하는 것도 고려해보세요:

    $schedule->command('auth:clear-resets')->everyFifteenMinutes();

<a name="password-customization"></a>
## 커스터마이즈

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이즈

`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하여 비밀번호 재설정 링크의 URL을 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 전달받는 클로저를 인자로 받습니다. 일반적으로 이 메서드는 `App\Providers\AuthServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

사용자에게 비밀번호 재설정 링크를 전송할 때 사용할 알림 클래스를 쉽게 변경할 수 있습니다. 시작하려면, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서, 직접 만든 [알림 클래스](/docs/{{version}}/notifications)를 사용해 알림을 전송할 수 있습니다. 비밀번호 재설정 `$token`은 이 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 이용해 원하는 비밀번호 재설정 URL을 구성하고, 사용자에게 알림을 전송할 수 있습니다:

    use App\Notifications\ResetPasswordNotification;

    /**
     * 사용자에게 비밀번호 재설정 알림을 전송합니다.
     *
     * @param  string  $token
     * @return void
     */
    public function sendPasswordResetNotification($token)
    {
        $url = 'https://example.com/reset-password?token='.$token;

        $this->notify(new ResetPasswordNotification($url));
    }