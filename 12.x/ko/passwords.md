# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [모델 준비](#model-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청하기](#requesting-the-password-reset-link)
    - [비밀번호 재설정하기](#resetting-the-password)
- [만료된 토큰 삭제하기](#deleting-expired-tokens)
- [커스터마이징](#password-customization)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 매번 직접 구현하는 대신, 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정을 위한 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에서 Laravel [application starter kit](/docs/12.x/starter-kits)을 설치해 보세요. Laravel의 스타터 킷은 비밀번호 재설정을 포함해 전체 인증 시스템의 뼈대를 자동으로 구성해줍니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 비밀번호 재설정 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에서 제공하는 옵션들을 꼭 확인하세요. 기본적으로 Laravel은 `database` 비밀번호 재설정 드라이버를 사용하도록 설정되어 있습니다.

비밀번호 재설정 `driver` 설정 옵션은 재설정 관련 데이터를 어디에 저장할지를 정의합니다. Laravel은 두 가지 드라이버를 제공합니다:

<div class="content-list" markdown="1">

- `database` - 비밀번호 재설정 데이터가 관계형 데이터베이스에 저장됩니다.
- `cache` - 비밀번호 재설정 데이터가 캐시 기반 스토어 중 한 곳에 저장됩니다.

</div>

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

기본 `database` 드라이버를 사용할 경우 비밀번호 재설정 토큰을 저장할 테이블을 만들어야 합니다. 일반적으로 이 테이블은 Laravel 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="cache"></a>
#### 캐시 (Cache)

비밀번호 재설정을 위한 캐시 드라이버도 제공되며, 이 경우 전용 데이터베이스 테이블이 필요 없습니다. 캐시 항목은 사용자의 이메일 주소를 키로 사용하므로, 애플리케이션의 다른 곳에서 이메일 주소를 캐시 키로 사용하지 않도록 주의해야 합니다:

```php
'passwords' => [
    'users' => [
        'driver' => 'cache',
        'provider' => 'users',
        'store' => 'passwords', // 선택 사항...
        'expire' => 60,
        'throttle' => 60,
    ],
],
```

`artisan cache:clear` 명령어 실행 시 비밀번호 재설정 데이터를 삭제하지 않도록 하려면, `store` 설정 키를 사용해 별도의 캐시 스토어를 지정할 수 있습니다. 이 값은 `config/cache.php` 파일에 설정된 스토어 중 하나여야 합니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용하고 있어야 합니다. 일반적으로 이 트레이트는 Laravel 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을 구현하고 있는지 확인하세요. Laravel 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용해 해당 메서드를 포함하고 있습니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 상관없이 모든 요청에 응답하며, 절대 URL 생성 시 `Host` 헤더 값을 사용합니다.

보통은 Nginx 또는 Apache 같은 웹 서버에서 애플리케이션으로 전달되는 요청의 호스트명을 제한하도록 설정해야 합니다. 하지만 웹 서버를 직접 제어할 수 없고, Laravel이 특정 호스트명으로 오는 요청만 처리하게 하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용하면 됩니다. 이는 특히 비밀번호 재설정 기능이 있을 때 매우 중요합니다.

이 미들웨어 메서드에 대해 자세히 알고 싶다면 [TrustHosts 미들웨어 문서](/docs/12.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 하려면 여러 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 입력하여 비밀번호 재설정 링크를 요청하는 라우트 두 개가 필요합니다. 다음으로, 사용자에게 이메일로 전송된 비밀번호 재설정 링크를 눌러 비밀번호를 실제로 재설정할 때 사용하는 라우트 두 개가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청하기 (Requesting the Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼 (The Password Reset Link Request Form)

먼저, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트를 정의합니다. 시작하기 위해 비밀번호 재설정 링크 요청 폼을 보여주는 뷰를 반환하는 라우트를 정의합니다:

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 `email` 필드가 포함된 폼이 있어야 하며, 사용자가 이메일 주소를 입력해 비밀번호 재설정 링크를 요청할 수 있게 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling the Form Submission)

다음으로, "비밀번호 분실" 뷰에서 전송된 폼 제출을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소 유효성 검증과 비밀번호 재설정 요청 전송을 담당합니다:

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

잠시 이 라우트를 자세히 살펴보겠습니다. 먼저 요청받은 `email` 속성을 검증하고, Laravel 내장 "password broker"(Password 파사드)를 사용해 비밀번호 재설정 링크를 사용자에게 전송합니다. password broker는 주어진 필드(여기서는 이메일 주소)를 이용해 사용자를 찾고, Laravel의 내장 [알림 시스템](/docs/12.x/notifications)을 통해 비밀번호 재설정 링크를 이메일로 보냅니다.

`sendResetLink` 메서드는 상태를 나타내는 문자열을 반환합니다. 이 상태 문자열은 Laravel의 [로컬라이제이션](/docs/12.x/localization) 기능으로 번역 가능하며, 사용자에게 요청 상태에 관한 친근한 메시지를 표시할 때 사용합니다. 상태 문자열에 대한 번역은 애플리케이션의 `lang/{lang}/passwords.php` 파일에 정의되어 있습니다. 각 상태 문자열 값에 대한 항목이 이 언어 파일 내에 있습니다.

> [!NOTE]
> 기본 Laravel 애플리케이션 골격에는 `lang` 디렉토리가 포함되지 않습니다. Laravel 언어 파일을 직접 커스터마이징하려면 `lang:publish` Artisan 명령어로 파일을 배포할 수 있습니다.

Laravel이 `Password` 파사드의 `sendResetLink` 메서드 호출 시 어떻게 애플리케이션 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수 있습니다. Laravel password broker는 인증 시스템 내 "user providers"를 이용해 데이터베이스에서 레코드를 조회합니다. password broker가 사용하는 user provider는 `config/auth.php` 설정 파일 내 `passwords` 구성 배열에 정의되어 있습니다. 사용자 정의 user provider 작성 방법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 수동으로 비밀번호 재설정을 구현할 때는 직접 뷰와 라우트 내용을 정의해야 합니다. 필요한 모든 인증 및 검증 로직을 포함한 스캐폴딩이 필요하다면 [Laravel application starter kits](/docs/12.x/starter-kits)를 확인해보세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정하기 (Resetting the Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼 (The Password Reset Form)

다음으로, 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 새 비밀번호를 입력하면 실제로 비밀번호를 재설정하는 데 필요한 라우트를 정의합니다. 먼저 이 링크를 클릭했을 때 보여줄 비밀번호 재설정 폼을 표시하는 라우트부터 정의합니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 필요한 `token` 매개변수를 받습니다:

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰에는 `email`, `password`, `password_confirmation` 필드와, 받아온 비밀 토큰 `$token` 값을 담은 숨김 `token` 필드를 포함하는 폼이 있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리 (Handling the Form Submission)

물론, 비밀번호 재설정 폼 제출을 처리할 라우트도 필요합니다. 이 라우트는 요청 유효성 검증 및 데이터베이스 내 사용자의 비밀번호 업데이트를 담당합니다:

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

이 라우트도 자세히 살펴봅시다. 먼저 요청 내 `token`, `email`, `password` 속성을 검증합니다. 이어서 Laravel 내장 "password broker"(Password 파사드)를 사용해 비밀번호 재설정 요청 자격 증명을 검증합니다.

만약 `token`, 이메일 주소, 비밀번호가 유효하다면, `reset` 메서드에 전달한 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 새로 입력받은 평문 비밀번호를 인수로 받아, 데이터베이스 내 사용자의 비밀번호를 업데이트할 수 있습니다.

`reset` 메서드도 상태 문자열을 반환하며, 앞서와 같이 이 문자열은 Laravel의 [로컬라이제이션](/docs/12.x/localization) 도구를 통해 사용자에게 친근한 메시지로 변환됩니다. 상태 문자열의 번역은 `lang/{lang}/passwords.php` 파일 내에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

또한, Laravel이 `Password` 파사드의 `reset` 메서드 호출 시 데이터베이스에서 어떻게 사용자 레코드를 불러오는지 궁금할 수 있습니다. password broker는 인증 시스템의 user provider를 이용하며, 이 user provider 설정은 `config/auth.php` 내 `passwords` 배열에서 관리합니다. 사용자 정의 user provider 작성법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제하기 (Deleting Expired Tokens)

`database` 드라이버를 사용하는 경우, 만료된 비밀번호 재설정 토큰이 데이터베이스에 남아 있을 수 있습니다. 이러한 레코드는 `auth:clear-resets` Artisan 명령어로 쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 작업을 자동화하려면 애플리케이션의 [스케줄러](/docs/12.x/scheduling)에 다음과 같이 추가할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 URL 커스터마이징 (Reset Link Customization)

`ResetPassword` 알림 클래스의 `createUrlUsing` 메서드를 통해 비밀번호 재설정 링크 URL을 커스터마이징할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 재설정 토큰을 받는 클로저를 인수로 받습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider` 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다:

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

비밀번호 재설정 링크를 사용자에게 전송하는 알림 클래스를 쉽게 수정할 수 있습니다. 시작하려면 `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서 직접 만든 [알림 클래스](/docs/12.x/notifications)를 사용해 알림을 보낼 수 있습니다. 비밀번호 재설정 토큰 `$token`은 첫 번째 인수로 전달되며, 이를 사용해 원하는 재설정 URL을 생성하고 사용자에게 알림을 보낼 수 있습니다:

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