# 비밀번호 재설정

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
## 소개

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있도록 기능을 제공합니다. 매번 새로운 애플리케이션을 만들 때마다 이를 직접 구현하는 대신, Laravel은 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정에 편리한 서비스를 제공합니다.

> [!NOTE]  
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 Laravel [스타터 킷](/docs/{{version}}/starter-kits)을 설치해 보세요. Laravel 스타터 킷은 비밀번호 재설정을 포함한 전체 인증 시스템 스캐폴딩을 자동으로 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 일반적으로 이 트레이트는 새로 생성한 Laravel 애플리케이션의 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을 구현하고 있는지 확인하세요. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용하여 해당 인터페이스에 필요한 메서드를 포함시킵니다.

<a name="database-preparation"></a>
### 데이터베이스 준비

애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 이 테이블에 대한 마이그레이션은 기본 Laravel 애플리케이션에 포함되어 있으므로, 아래 명령어로 데이터베이스를 마이그레이트 하여 테이블을 생성하면 됩니다:

```shell
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더의 내용과 상관없이 들어오는 모든 요청에 응답합니다. 또한, 웹 요청 중 애플리케이션의 절대 URL을 생성할 때 해당 `Host` 헤더의 값을 사용합니다.

일반적으로 Nginx나 Apache와 같은 웹 서버에서 특정 호스트명과 일치하는 요청만 애플리케이션에 전달하도록 설정해야 합니다. 하지만 웹 서버를 직접 커스터마이징할 수 없는 경우, Laravel에서 특정 호스트명에만 응답하도록 하려면, `App\Http\Middleware\TrustHosts` 미들웨어를 활성화할 수 있습니다. 이 설정은 비밀번호 재설정 기능을 제공하는 애플리케이션에서 특히 중요합니다.

이 미들웨어에 대해 더 자세한 내용은 [`TrustHosts` 미들웨어 공식 문서](/docs/{{version}}/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있도록 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 하는 라우트 쌍이 필요합니다. 두 번째로, 이메일로 전송된 비밀번호 재설정 링크를 클릭하고 비밀번호 재설정 폼을 완료한 후 실제로 비밀번호를 재설정하는 라우트 쌍이 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트를 정의합니다. 시작하려면, 비밀번호 재설정 링크 요청 폼을 반환하는 뷰를 보여주는 라우트를 정의합니다:

    Route::get('/forgot-password', function () {
        return view('auth.forgot-password');
    })->middleware('guest')->name('password.request');

이 라우트가 반환하는 뷰에는 사용자가 특정 이메일 주소에 비밀번호 재설정 링크를 요청할 수 있도록 `email` 필드를 포함한 폼이 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호를 잊으셨나요" 뷰에서 제출된 폼을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소의 유효성을 검증하고, 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다:

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

다음 단계로 넘어가기 전에, 이 라우트의 내용을 좀 더 자세히 살펴보겠습니다. 먼저 요청의 `email` 속성에 대한 유효성 검사가 진행됩니다. 그 다음, Laravel의 내장 "비밀번호 브로커" (`Password` 파사드 사용)를 통해 사용자에게 비밀번호 재설정 링크가 전송됩니다. 비밀번호 브로커는 주어진 필드(이 경우 이메일)를 기준으로 사용자를 조회하고, Laravel의 [알림 시스템](/docs/{{version}}/notifications)을 이용해 재설정 링크를 전송합니다.

`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 헬퍼로 번역해 사용자에게 요청 결과에 대한 친절한 메시지를 표시할 수 있습니다. 비밀번호 재설정 상태의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 모든 상태 슬러그의 가능한 값에 대한 항목이 `passwords` 언어 파일 내에 있습니다.

> [!NOTE]  
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하고 싶다면 `lang:publish` Artisan 명령으로 파일을 퍼블리시할 수 있습니다.

`Password` 파사드의 `sendResetLink` 메서드를 호출할 때, Laravel이 어떻게 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수 있습니다. Laravel 비밀번호 브로커는 인증 시스템의 "사용자 프로바이더"를 활용하여 데이터베이스 레코드를 조회합니다. 비밀번호 브로커에서 사용하는 사용자 프로바이더는 `config/auth.php` 설정 파일의 `passwords` 설정 배열 내에서 정의합니다. 사용자 정의 사용자 프로바이더 작성에 대한 자세한 내용은 [인증 공식 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]  
> 비밀번호 재설정을 수동으로 구현하는 경우, 뷰와 라우트의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 검증 로직을 포함한 스캐폴딩이 필요하다면 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 참고하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

이제, 사용자가 이메일로 전달받은 비밀번호 재설정 링크를 클릭하고 새로운 비밀번호를 입력할 때 실제로 비밀번호를 재설정하는 데 필요한 라우트를 정의하겠습니다. 먼저, 사용자가 비밀번호 재설정 링크를 클릭했을 때 표시되는 폼을 보여주는 라우트를 정의합니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 사용할 `token` 파라미터를 받습니다:

    Route::get('/reset-password/{token}', function (string $token) {
        return view('auth.reset-password', ['token' => $token]);
    })->middleware('guest')->name('password.reset');

이 라우트가 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드를 포함해야 하며, `token` 필드에는 라우트에서 받은 비밀 `$token` 값을 넣어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론, 이제 실제로 비밀번호 재설정 폼이 제출될 때 처리하는 라우트가 필요합니다. 이 라우트는 들어온 요청을 검증하고 데이터베이스에서 사용자의 비밀번호를 업데이트합니다:

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

다음 단계로 넘어가기 전에, 이 라우트를 더 자세히 살펴보겠습니다. 먼저 요청의 `token`, `email`, `password` 속성이 유효성 검사를 거칩니다. 이후, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드 사용)를 통해 비밀번호 재설정 요청 자격 증명을 검증합니다.

토큰, 이메일 주소, 비밀번호가 모두 올바르면 `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저에서는 사용자 인스턴스와 폼에 입력된 평문 비밀번호를 받아 데이터베이스 내 사용자의 비밀번호를 업데이트할 수 있습니다.

`reset` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 헬퍼를 사용해 번역하여 사용자에게 친절한 메시지를 표시할 수 있습니다. 비밀번호 재설정 상태의 번역은 앱의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 모든 상태 값에 대한 항목은 `passwords` 언어 파일 내에 있습니다. 앱에 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령으로 생성할 수 있습니다.

마지막으로, `Password` 파사드의 `reset` 메서드를 호출할 때 Laravel이 어떻게 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수 있습니다. Laravel 비밀번호 브로커는 인증 시스템의 "사용자 프로바이더"를 활용하여 데이터베이스 레코드를 조회합니다. 사용되는 사용자 프로바이더는 `config/auth.php` 설정 파일의 `passwords` 배열 내에서 정의합니다. 사용자 정의 프로바이더 작성에 대한 더 자세한 내용은 [인증 공식 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

만료된 비밀번호 재설정 토큰도 데이터베이스에 남아 있을 수 있습니다. 그러나 아래 `auth:clear-resets` Artisan 명령을 사용해 이 레코드들을 손쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 아래와 같이 명령을 추가해보세요:

    $schedule->command('auth:clear-resets')->everyFifteenMinutes();

<a name="password-customization"></a>
## 커스터마이징

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이징

`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하여 비밀번호 재설정 링크 URL을 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받을 사용자 인스턴스와 비밀번호 재설정 토큰을 인자로 받는 클로저를 전달받습니다. 보통 `App\Providers\AuthServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 이 메서드를 호출합니다:

    use App\Models\User;
    use Illuminate\Auth\Notifications\ResetPassword;

    /**
     * 인증 관련 서비스를 등록합니다.
     */
    public function boot(): void
    {
        ResetPassword::createUrlUsing(function (User $user, string $token) {
            return 'https://example.com/reset-password?token='.$token;
        });
    }

<a name="reset-email-customization"></a>
#### 재설정 이메일 커스터마이징

사용자에게 비밀번호 재설정 링크를 전송할 때 사용되는 알림 클래스를 손쉽게 수정할 수 있습니다. 시작하려면, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서, 자유롭게 만든 [알림 클래스](/docs/{{version}}/notifications)를 사용하여 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`은 해당 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 이용하여 원하는 재설정 URL을 만들고, 사용자의 알림을 보낼 수 있습니다:

    use App\Notifications\ResetPasswordNotification;

    /**
     * 사용자에게 비밀번호 재설정 알림을 전송합니다.
     *
     * @param  string  $token
     */
    public function sendPasswordResetNotification($token): void
    {
        $url = 'https://example.com/reset-password?token='.$token;

        $this->notify(new ResetPasswordNotification($url));
    }
