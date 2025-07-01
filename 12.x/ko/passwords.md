# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [모델 준비](#model-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이즈](#password-customization)

<a name="introduction"></a>
## 소개

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 기능을 제공합니다. 라라벨은 여러분이 매번 직접 재설정 기능을 구현하지 않아도 되도록, 비밀번호 재설정 링크 발송과 안전한 비밀번호 재설정을 위한 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 라라벨 애플리케이션에 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 설치해 보세요. 라라벨의 스타터 킷은 비밀번호 재설정 기능을 포함한 전체 인증 시스템 스캐폴딩을 자동으로 처리해줍니다.

<a name="configuration"></a>
### 설정

애플리케이션의 비밀번호 재설정 설정 파일은 `config/auth.php`에 위치해 있습니다. 이 파일 내에서 사용할 수 있는 다양한 옵션들을 꼭 검토해 보시기 바랍니다. 기본적으로 라라벨은 `database` 비밀번호 재설정 드라이버를 사용하도록 설정되어 있습니다.

비밀번호 재설정의 `driver` 설정 옵션은 비밀번호 재설정 데이터가 어디에 저장될지 결정합니다. 라라벨은 두 가지 드라이버를 기본으로 제공합니다.

<div class="content-list" markdown="1">

- `database` - 비밀번호 재설정 데이터가 관계형 데이터베이스에 저장됩니다.
- `cache` - 비밀번호 재설정 데이터가 캐시 기반 저장소 중 하나에 저장됩니다.

</div>

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="database"></a>
#### 데이터베이스

기본값인 `database` 드라이버를 사용할 경우, 애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블을 생성해야 합니다. 이 테이블은 보통 라라벨의 기본 마이그레이션 파일인 `0001_01_01_000000_create_users_table.php`에 포함되어 있습니다.

<a name="cache"></a>
#### 캐시

캐시 드라이버를 사용하면 별도의 데이터베이스 테이블 없이 비밀번호 재설정 처리를 할 수 있습니다. 항목들은 사용자의 이메일 주소를 키로 저장되므로, 애플리케이션 내에서 다른 용도로 이메일 주소를 캐시 키로 사용하고 있지 않은지 반드시 확인해야 합니다.

```php
'passwords' => [
    'users' => [
        'driver' => 'cache',
        'provider' => 'users',
        'store' => 'passwords', // Optional...
        'expire' => 60,
        'throttle' => 60,
    ],
],
```

`artisan cache:clear` 명령어를 실행했을 때 비밀번호 재설정 데이터까지 삭제되지 않게 하려면, `store` 설정 키를 사용해 비밀번호 재설정만을 위한 별도의 캐시 저장소를 지정할 수 있습니다. 이 값은 `config/cache.php` 파일에 정의된 저장소 이름 중 하나와 일치해야 합니다.

<a name="model-preparation"></a>
### 모델 준비

라라벨의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 반드시 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 이 트레이트는 새로운 라라벨 애플리케이션을 생성할 때 기본적으로 추가되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을(인터페이스를) 구현하고 있는지 확인하세요. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용해 필요한 메서드를 제공합니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정

기본적으로 라라벨은 요청에 포함된 HTTP `Host` 헤더의 내용과 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 중 애플리케이션의 절대 URL을 생성할 때도 `Host` 헤더 값을 사용합니다.

보통은 Nginx, Apache와 같은 웹 서버에서 특정 호스트명에 일치하는 요청만 애플리케이션으로 전달하도록 설정해야 합니다. 그러나 웹 서버를 직접 설정할 수 없는 환경이라면, 라라벨에서 특정 호스트명에만 응답하도록 `bootstrap/app.php` 파일의 `trustHosts` 미들웨어 메서드를 사용할 수 있습니다. 비밀번호 재설정 기능을 제공하는 애플리케이션이라면 이 설정이 특히 중요합니다.

이 미들웨어 메서드에 대해 더 자세히 알아보려면 [TrustHosts 미들웨어 문서](/docs/12.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있게 기능을 구현하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 두 개의 라우트가 필요합니다. 이어서, 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 폼을 제출하면 실제로 비밀번호를 재설정하는 처리를 위한 라우트 두 개가 더 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크 요청에 필요한 라우트를 정의합니다. 시작하려면, 비밀번호 재설정 링크 요청 폼을 렌더링하는 뷰를 반환하는 라우트를 아래와 같이 작성하세요.

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 `email` 필드가 포함된 폼이 있어야 하며, 사용자가 입력한 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있게 해야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호를 잊으셨나요" 뷰에서 폼이 제출될 때 요청을 처리할 라우트를 정의합니다. 이 라우트는 이메일 주소의 유효성을 검사하고 해당 사용자에게 비밀번호 재설정 링크를 전송하는 역할을 합니다.

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

이 라우트의 동작을 자세히 살펴보면, 먼저 요청에서 `email` 값이 유효한지 검증합니다. 그 뒤 라라벨에서 제공하는 "비밀번호 브로커"(`Password` 파사드)를 사용해 해당 사용자에게 비밀번호 재설정 링크를 보냅니다. 비밀번호 브로커는 지정된 필드(이 경우 이메일)로 사용자를 찾아, 라라벨의 [알림 시스템](/docs/12.x/notifications)을 이용해 비밀번호 재설정 링크를 이메일로 전송합니다.

`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 상태값은 라라벨의 [로컬라이제이션](/docs/12.x/localization) 헬퍼로 번역할 수 있으며, 사용자에게 요청 처리 결과에 대한 안내 메시지를 보여주는 데 사용됩니다. 비밀번호 재설정 상태에 대한 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 관리됩니다. 각 status 슬러그에 해당하는 메시지가 이 파일에 정의되어 있습니다.

> [!NOTE]
> 기본적으로 라라벨 애플리케이션에는 `lang` 디렉터리가 포함되어 있지 않습니다. 직접 번역 파일을 커스터마이즈하고 싶다면 `lang:publish` 아티즌 명령어를 통해 언어 파일을 복사할 수 있습니다.

그렇다면 라라벨은 어떻게 비밀번호 브로커가 데이터베이스에서 사용자를 가져와야 하는지 알까요? 라라벨의 비밀번호 브로커는 애플리케이션 인증 시스템의 "user provider"를 사용해 데이터베이스 레코드를 조회합니다. 비밀번호 브로커에서 사용할 user provider는 `config/auth.php` 파일의 `passwords` 배열 설정에서 지정되어 있습니다. 사용자 정의 user provider 작성법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고해주세요.

> [!NOTE]
> 비밀번호 재설정 기능을 직접 구현하는 경우, 관련 뷰와 라우트를 모두 직접 작성해야 합니다. 인증과 이메일 인증 관련 로직을 포함해 모든 필요한 코드가 포함된 스캐폴딩을 원한다면 [라라벨 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 참고하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

이제 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 새 비밀번호를 입력할 수 있도록 하는 라우트를 정의하겠습니다. 먼저, 사용자가 비밀번호 재설정 링크를 클릭했을 때 표시되는 폼을 위한 라우트는 아래와 같이 작성합니다. 이 라우트는 `token` 파라미터를 받으며, 추후 비밀번호 재설정 요청 검증에 사용됩니다.

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드(라우트로 받은 `$token` 값이 들어감)가 포함된 폼을 출력해야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론, 실제로 비밀번호 재설정 폼이 제출되었을 때 해당 요청을 처리하는 라우트도 정의해야 합니다. 이 라우트는 사용자의 요청을 검증하고 데이터베이스의 비밀번호를 업데이트해줍니다.

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

이 라우트의 동작을 자세히 살펴보면, 먼저 `token`, `email`, `password` 값의 유효성을 검사합니다. 그 다음에는 라라벨의 "비밀번호 브로커"(`Password` 파사드)를 사용해 해당 자격 정보(토큰, 이메일, 비밀번호)를 검증합니다.

만약 비밀번호 브로커가 받은 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달한 클로저가 실행됩니다. 이 클로저는 사용자 인스턴스와 사용자가 입력한 평문 비밀번호를 전달받아, 비밀번호를 실제로 변경하고, "remember me" 토큰을 갱신합니다.

`reset` 메서드는 "status" 슬러그를 반환하며, 이를 라라벨의 [로컬라이제이션](/docs/12.x/localization) 헬퍼로 번역해 사용자에게 안내할 수 있습니다. 이 값은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 정의되어 있습니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어를 통해 직접 디렉터리를 추가할 수 있습니다.

여기서도 마찬가지로, 라라벨이 어떻게 데이터베이스에서 사용자 정보를 가져올지 궁금할 수 있습니다. 라라벨의 비밀번호 브로커는 인증 시스템의 "user provider"를 이용합니다. 브로커가 사용할 user provider는 `config/auth.php`의 `passwords` 설정 배열에서 지정합니다. 사용자 정의 provider 작성법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

`database` 드라이버를 사용하는 경우, 만료된 비밀번호 재설정 토큰 기록이 데이터베이스에 남아 있을 수 있습니다. 이 기록은 `auth:clear-resets` 아티즌 명령어로 쉽게 삭제할 수 있습니다.

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/12.x/scheduling)에 해당 명령어를 등록하는 방법이 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이즈

<a name="reset-link-customization"></a>
#### 비밀번호 재설정 링크 URL 커스터마이즈

`ResetPassword` 알림(노티피케이션) 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하면 비밀번호 재설정 링크 URL을 원하는 대로 커스터마이즈할 수 있습니다. 이 메서드는 노티피케이션을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 인자로 받는 클로저를 전달받으며, 주로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 일반적입니다.

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
#### 비밀번호 재설정 이메일 커스터마이즈

사용자에게 비밀번호 재설정 링크를 전송하는 알림(노티피케이션) 클래스를 쉽게 변경할 수 있습니다. 시작하려면 `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하면 됩니다. 이 메서드 내에서 직접 만든 [노티피케이션 클래스](/docs/12.x/notifications)를 사용해 원하는 방식으로 알림을 전송할 수 있습니다. 비밀번호 재설정 `$token`이 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 사용해 원하는 비밀번호 재설정 URL을 만들고 사용자에게 알림을 전송할 수 있습니다.

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
