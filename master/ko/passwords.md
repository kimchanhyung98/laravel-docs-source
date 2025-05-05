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

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. 매번 직접 이 기능을 구현하는 대신, Laravel은 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정을 손쉽게 처리할 수 있는 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에서 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치해보세요. Laravel의 스타터 키트는 비밀번호 재설정 등 전체 인증 시스템의 스캐폴딩을 자동으로 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용하고 있는지 확인해야 합니다. 일반적으로, 이 트레이트는 새로운 Laravel 애플리케이션에서 기본적으로 생성되는 `App\Models\User` 모델에 이미 포함되어 있습니다.

그리고 `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하고 있는지도 확인해야 합니다. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용하여 인터페이스 구현에 필요한 메서드를 포함하고 있습니다.

<a name="database-preparation"></a>
### 데이터베이스 준비

애플리케이션의 비밀번호 재설정 토큰을 저장하기 위한 테이블이 필요합니다. 보통 이 테이블은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션 파일에 포함되어 있습니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용에 관계 없이 모든 요청에 응답합니다. 또한, 웹 요청 중 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더의 값을 사용합니다.

일반적으로, Nginx나 Apache와 같은 웹 서버를 설정하여 특정 호스트네임과 일치하는 요청만 애플리케이션에 전달하도록 구성해야 합니다. 하지만 웹 서버를 직접 설정할 수 없는 경우, Laravel에 특정 호스트네임에 대해서만 응답하도록 알려줘야 할 수도 있습니다. 이럴 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용하면 됩니다. 특히 비밀번호 재설정 기능을 제공하는 애플리케이션에서는 이 설정이 중요합니다.

이 미들웨어 메서드에 대한 자세한 내용은 [`TrustHosts` 미들웨어 문서](/docs/{{version}}/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있도록 지원하려면 여러 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있는 라우트 두 개가 필요합니다. 그리고, 사용자가 이메일로 전송된 비밀번호 재설정 링크를 클릭하고 비밀번호 재설정 폼을 완료하면 실제로 비밀번호를 재설정하는 라우트 두 개도 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트를 정의해보겠습니다. 우선, 비밀번호 재설정 링크 요청 폼을 반환하는 뷰를 반환하는 라우트를 정의합니다.

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트에서 반환하는 뷰에는 `email` 필드가 포함된 폼이 있어야 하며, 사용자는 해당 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있습니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호 찾기" 뷰에서 폼 제출 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고, 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다.

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

이 라우트를 조금 더 자세히 살펴보겠습니다. 먼저, 요청 객체의 `email` 속성이 검증됩니다. 다음으로, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 이용해 해당 사용자에게 비밀번호 재설정 링크를 전송합니다. 비밀번호 브로커는 주어진 필드(이 경우 이메일 주소)로 사용자를 찾아 [알림 시스템](/docs/{{version}}/notifications)을 통해 비밀번호 재설정 링크를 전송합니다.

`sendResetLink` 메서드는 "상태" 슬러그를 반환합니다. 이 상태는 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 도우미를 사용해 사용자에게 친화적인 메시지로 변환할 수 있습니다. 비밀번호 재설정 상태 메시지의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 의해 결정됩니다. 각 상태 별 슬러그에 대한 항목이 이 파일 내에 위치합니다.

> [!NOTE]
> 기본적으로, Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

Laravel이 어떻게 `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "사용자 프로바이더"를 이용해 레코드를 조회합니다. 이 프로바이더는 `config/auth.php`의 `passwords` 설정 배열에서 구성됩니다. 사용자 정의 프로바이더 작성에 대한 자세한 내용은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정을 직접 구현할 경우, 뷰와 라우트의 내용을 자신이 직접 정의해야 합니다. 인증 및 검증 로직이 모두 포함된 스캐폴딩이 필요하다면 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

이제 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 새로운 비밀번호를 입력한 후, 실제로 비밀번호를 재설정하는 데 필요한 라우트를 정의해보겠습니다. 우선 사용자가 재설정 링크를 클릭하면 표시되는 폼을 보여주는 라우트를 정의합니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증할 때 사용할 `token` 파라미터를 받습니다.

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트에서 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드가 반드시 포함되어야 하며, `token` 필드는 라우트에서 받은 `$token` 값을 포함해야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

당연히, 비밀번호 재설정 폼의 제출을 실제로 처리하는 라우트도 정의해야 합니다. 이 라우트는 요청을 검증한 후 데이터베이스에서 사용자의 비밀번호를 업데이트합니다.

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

이 라우트를 조금 더 자세히 살펴보면, 먼저 요청 객체의 `token`, `email`, `password` 속성이 검증됩니다. 그 다음, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 사용해서 재설정 요청 자격을 검증합니다.

토큰, 이메일 주소, 비밀번호가 모두 정확하다면, `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에 입력된 평문 비밀번호를 받아 데이터베이스에서 사용자의 비밀번호를 업데이트합니다.

`reset` 메서드는 "상태" 슬러그를 반환합니다. 이 상태는 Laravel의 [로컬라이제이션](/docs/{{version}}/localization) 도우미를 사용해 사용자에게 친화적인 메시지로 변환할 수 있습니다. 비밀번호 재설정 상태 메시지의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 파일에서 관리합니다. 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

여기서도 Laravel이 어떻게 `Password` 파사드의 `reset` 메서드로 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "사용자 프로바이더"를 사용합니다. 이 프로바이더는 `config/auth.php`의 `passwords` 설정 배열에서 구성됩니다. 사용자 정의 프로바이더 작성에 대한 자세한 내용은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

만료된 비밀번호 재설정 토큰은 데이터베이스에 남아 있을 수 있습니다. 하지만 `auth:clear-resets` Artisan 명령어를 사용해 해당 레코드를 손쉽게 삭제할 수 있습니다.

```shell
php artisan auth:clear-resets
```

이 프로세스를 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 명령어를 추가할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이즈

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이즈

`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하면 비밀번호 재설정 링크의 URL을 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 받는 클로저를 인자로 받습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하면 좋습니다.

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

비밀번호 재설정 링크를 전송하는 데 사용되는 알림 클래스를 손쉽게 커스터마이즈할 수 있습니다. `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하면 됩니다. 이 메서드 안에서 직접 만든 [알림 클래스](/docs/{{version}}/notifications)를 사용하여 알림을 전송할 수 있습니다. 비밀번호 재설정 `$token`은 해당 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 사용해서 원하는 형태의 비밀번호 재설정 URL을 만들고 사용자에게 직접 알림을 보낼 수 있습니다.

```php
use App\Notifications\ResetPasswordNotification;

/**
 * 사용자인 비밀번호 재설정 알림 전송.
 *
 * @param  string  $token
 */
public function sendPasswordResetNotification($token): void
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```
