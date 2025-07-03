# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [모델 준비](#model-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이징](#password-customization)

<a name="introduction"></a>
## 소개

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. 라라벨은 이를 애플리케이션마다 직접 구현하지 않아도 되도록, 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정을 도와주는 편리한 기능들을 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 라라벨 애플리케이션에 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 라라벨의 스타터 키트는 비밀번호 재설정 기능을 포함한 전체 인증 시스템을 자동으로 구성해줍니다.

<a name="configuration"></a>
### 설정

애플리케이션의 비밀번호 재설정과 관련된 설정 파일은 `config/auth.php`에 있습니다. 이 파일에 있는 다양한 옵션을 꼭 확인해보시기 바랍니다. 라라벨은 기본적으로 `database` 비밀번호 재설정 드라이버를 사용하도록 설정되어 있습니다.

비밀번호 재설정 `driver` 설정 옵션은 비밀번호 재설정 데이터를 어디에 저장할지 결정합니다. 라라벨은 두 가지 드라이버를 기본으로 제공합니다.

<div class="content-list" markdown="1">

- `database` - 비밀번호 재설정 데이터가 관계형 데이터베이스에 저장됩니다.
- `cache` - 비밀번호 재설정 데이터가 캐시 기반 저장소에 저장됩니다.

</div>

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비사항

<a name="database"></a>
#### Database

기본 `database` 드라이버를 사용할 경우, 애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 일반적으로 이 테이블은 라라벨 기본 마이그레이션인 `0001_01_01_000000_create_users_table.php`에 포함되어 있습니다.

<a name="cache"></a>
#### Cache

비밀번호 재설정을 처리할 수 있는 캐시 드라이버도 사용할 수 있으며, 이 경우 별도의 데이터베이스 테이블이 필요하지 않습니다. 항목은 사용자의 이메일 주소로 키가 설정되므로, 애플리케이션에서 이메일 주소를 캐시 키로 다른 용도로 사용 중이 아니라는 것을 반드시 확인해야 합니다.

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

`artisan cache:clear` 명령 실행 시 비밀번호 재설정 데이터까지 모두 삭제되는 것을 방지하고 싶다면, `store` 설정 키를 통해 별도의 캐시 저장소를 지정할 수 있습니다. 이때 값은 `config/cache.php` 설정 파일에 구성된 저장소 이름과 일치해야 합니다.

<a name="model-preparation"></a>
### 모델 준비

라라벨의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 반드시 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 새 라라벨 애플리케이션에서 생성되는 기본 `App\Models\User` 모델에는 이 트레이트가 이미 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하고 있는지 확인하세요. 프레임워크에 기본으로 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 활용하여 필요한 메서드를 제공합니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정

라라벨은 기본적으로 들어오는 모든 요청에 대해 HTTP 요청의 `Host` 헤더 값에 관계없이 응답합니다. 또한, 웹 요청 중 절대 URL을 생성할 때에도 `Host` 헤더의 값을 사용합니다.

일반적으로는 Nginx나 Apache 같은 웹 서버에 특정 호스트명만 애플리케이션으로 전달하도록 설정하는 것이 가장 좋습니다. 그러나 직접 웹 서버를 제어할 수 없는 경우, 라라벨이 특정 호스트명만 응답하도록 제한하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용할 수 있습니다. 비밀번호 재설정 기능이 있는 애플리케이션에서는 특히 중요한 설정입니다.

이 미들웨어 메서드에 대한 자세한 사용법은 [TrustHosts 미들웨어 문서](/docs/12.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅

비밀번호 재설정 기능을 제대로 구현하려면 여러 개의 라우트가 필요합니다. 먼저, 사용자가 이메일로 비밀번호 재설정 링크를 요청할 수 있도록 두 개의 라우트가 필요합니다. 그리고 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 재설정 폼을 작성하면, 실제로 비밀번호를 재설정하는 라우트 두 개가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청할 때 필요한 라우트를 정의합니다. 가장 먼저, 비밀번호 재설정 링크를 요청하는 폼을 반환하는 뷰 라우트를 만듭니다.

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 사용자가 이메일 주소를 입력해 비밀번호 재설정 링크를 요청할 수 있도록 `email` 필드가 포함된 폼이 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호 찾기" 뷰에서 폼 제출을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고, 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다.

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

진행하기 전에 이 라우트의 동작을 간단하게 살펴보겠습니다. 먼저 요청에 포함된 `email` 속성을 유효성 검증합니다. 그다음, 라라벨에서 제공하는 "패스워드 브로커"(`Password` 파사드 사용)를 활용해 사용자의 비밀번호 재설정 링크를 전송합니다. 패스워드 브로커는 지정된 필드(이 예시에서는 이메일)를 사용해 사용자를 조회하고, 라라벨의 [알림 시스템](/docs/12.x/notifications)을 통해 재설정 링크를 보냅니다.

`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 status 값은 라라벨의 [다국어 지원](/docs/12.x/localization) 헬퍼를 사용해 번역할 수 있고, 이를 이용해 사용자에게 요청 진행 결과를 친절하게 안내할 수 있습니다. 비밀번호 재설정 status에 대한 실제 번역 내용은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 찾을 수 있으며, status 슬러그의 모든 값에 대한 항목이 이 파일에 정의되어 있습니다.

> [!NOTE]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈 하고 싶다면, `lang:publish` 아티즌 명령어로 해당 파일들을 발행(publish)할 수 있습니다.

라라벨이 어떻게 애플리케이션의 데이터베이스에서 `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 사용자 레코드를 가져오는지 궁금하실 수 있습니다. 라라벨의 패스워드 브로커는 인증 시스템의 "user provider"를 활용해 데이터베이스의 사용자를 조회합니다. 패스워드 브로커가 사용하는 user provider는 `config/auth.php`의 `passwords` 설정 배열에서 지정할 수 있습니다. 커스텀 user provider 작성 방법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정 기능을 직접 구현할 경우, 뷰와 라우트 구성을 모두 직접 작성해야 합니다. 인증과 검증 로직까지 모두 포함된 스캐폴딩이 필요하다면 [라라벨 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 참고해 주세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

이제 사용자가 이메일로 전송된 비밀번호 재설정 링크를 클릭하여 새로운 비밀번호를 입력할 수 있도록 실제 비밀번호를 재설정하는 라우트를 정의하겠습니다. 먼저, 사용자가 재설정 링크를 클릭할 때 표시되는 비밀번호 재설정 폼을 보여주는 라우트를 만듭니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증할 때 사용할 `token` 파라미터를 전달받습니다.

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰 안에는 반드시 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 비밀 `$token` 값을 담는 숨겨진(히든) 필드가 포함되어 있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

당연히, 실제로 비밀번호 재설정 폼을 제출하면 이를 처리하는 라우트도 필요합니다. 이 라우트는 들어온 요청을 검증하고, 사용자의 비밀번호를 데이터베이스에 반영하는 역할을 합니다.

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

진행하기 전에 이 라우트의 동작을 좀 더 살펴보겠습니다. 먼저, 요청에 담긴 `token`, `email`, `password` 필드를 검증합니다. 그다음 라라벨의 "패스워드 브로커"(`Password` 파사드 사용)를 활용해 비밀번호 재설정 요청의 자격 정보를 확인합니다.

패스워드 브로커에 전달된 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저에서는 사용자 인스턴스와 비밀번호 재설정 폼에서 입력한 평문 비밀번호를 받아, 데이터베이스에 사용자의 비밀번호를 갱신할 수 있습니다.

`reset` 메서드는 "status" 슬러그를 반환합니다. 이 status 값 역시 라라벨의 [다국어 지원](/docs/12.x/localization) 헬퍼를 통해 사용자에게 친근한 메시지로 안내할 수 있습니다. 실제 번역 내용은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 위치합니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 생성할 수 있습니다.

또한 `Password` 파사드의 `reset` 메서드를 호출할 때 라라벨이 어떻게 데이터베이스에서 사용자 레코드를 가져오는지 궁금하실 수 있습니다. 라라벨의 패스워드 브로커는 인증 시스템 "user provider"를 활용해 사용자 정보를 조회합니다. 패스워드 브로커가 사용하는 user provider는 `config/auth.php`의 `passwords` 설정 배열에 지정할 수 있습니다. 커스텀 user provider를 만드는 법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

`database` 드라이버를 사용할 때, 만료된 비밀번호 재설정 토큰이 데이터베이스에 계속 남아 있을 수 있습니다. 이때는 `auth:clear-resets` 아티즌 명령어를 사용해 해당 레코드들을 쉽게 삭제할 수 있습니다.

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/12.x/scheduling) 기능을 이용해 명령을 반복 실행하도록 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이징

`ResetPassword` 알림(Notifications) 클래스에서 제공하는 `createUrlUsing` 메서드를 사용해 비밀번호 재설정 링크 URL을 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정용 토큰을 인수로 받아오는 클로저를 전달받습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 좋습니다.

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
#### 재설정 이메일 커스터마이징

사용자에게 비밀번호 재설정 링크를 보내는 데 사용하는 알림 클래스를 쉽게 수정할 수 있습니다. 먼저, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 안에서 원하는 [알림 클래스](/docs/12.x/notifications)를 사용해 알림을 발송할 수 있습니다. 비밀번호 재설정 `$token`은 이 메서드의 첫 번째 인수로 전달받으며, 이를 활용해 원하는 방식으로 재설정 링크를 만들고 사용자에게 알림을 보낼 수 있습니다.

```php
use App\Notifications\ResetPasswordNotification;

/**
 * 사용자의 비밀번호 재설정 알림을 전송합니다.
 *
 * @param  string  $token
 */
public function sendPasswordResetNotification($token): void
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```
