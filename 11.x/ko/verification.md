# 이메일 인증

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 안내](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재발송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [커스터마이징](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션에서는 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 이 기능을 애플리케이션마다 직접 구현하는 대신, Laravel은 이메일 인증 요청을 전송하고 검증하는 데 편리한 내장 서비스를 제공합니다.

> [!NOTE]  
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에서 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 스타터 키트는 이메일 인증 지원을 포함한 전체 인증 시스템의 스캐폴딩을 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비

시작하기 전에 `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약(Contract)을 구현하고 있는지 확인하세요:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}
```

이 인터페이스를 모델에 추가하면, 새로 등록된 유저에게 이메일 인증 링크가 담긴 이메일이 자동으로 전송됩니다. 이는 Laravel이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)를 자동으로 등록하기 때문에 매끄럽게 처리됩니다.

[스타터 키트](/docs/{{version}}/starter-kits)를 사용하지 않고 직접 회원가입을 구현하는 경우, 사용자 등록이 성공하면 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 디스패치해야 합니다:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, `users` 테이블에는 사용자의 이메일이 인증된 날짜와 시간을 저장할 `email_verified_at` 컬럼이 있어야 합니다. 보통 이 컬럼은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 올바르게 구현하려면 세 가지 라우트가 필요합니다. 첫째, 사용자에게 회원 가입 후 Laravel이 발송한 인증 이메일의 링크를 클릭하라고 안내하는 라우트가 필요합니다.

둘째, 사용자가 이메일의 인증 링크를 클릭했을 때 요청을 처리하는 라우트가 필요합니다.

셋째, 사용자가 인증 링크를 실수로 잃어버린 경우 인증 링크를 다시 발송할 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 안내

앞서 언급했듯이, 가입 후 Laravel이 이메일로 보낸 인증 링크를 클릭하라고 사용자를 안내하는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 인증 없이 애플리케이션의 다른 부분에 접근할 때 표시됩니다. 이메일 인증 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있는 한 자동으로 발송됩니다:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이메일 인증 안내를 반환하는 라우트의 이름은 반드시 `verification.notice`여야 합니다. 이 이름이 중요한 이유는, [Laravel에 포함된](#protecting-routes) `verified` 미들웨어가 사용자가 이메일을 인증하지 않은 경우 해당 라우트 이름으로 자동 리다이렉트하기 때문입니다.

> [!NOTE]  
> 이메일 인증을 직접 구현하는 경우, 인증 안내 뷰의 내용을 직접 정의해야 합니다. 필요 authentication 및 인증 뷰가 모두 포함된 스캐폴딩을 원한다면 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기

다음으로, 사용자가 회원가입 시 받은 이메일 인증 링크를 클릭했을 때 발생하는 요청을 처리할 라우트를 정의해야 합니다. 이 라우트의 이름은 `verification.verify`이어야 하며, `auth`와 `signed` 미들웨어를 적용해야 합니다:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

이 라우트를 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 인스턴스 대신 `EmailVerificationRequest`를 사용하고 있습니다. `EmailVerificationRequest`는 Laravel에 내장된 [폼 요청](/docs/{{version}}/validation#form-request-validation)으로, 요청의 `id`와 `hash` 파라미터를 자동으로 검증합니다.

그 다음, 바로 `fulfill` 메서드를 호출하여 인증 과정을 완료할 수 있습니다. 이 메서드는 인증된 사용자에 대해 `markEmailAsVerified` 메서드를 호출하고, `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다. `markEmailAsVerified` 메서드는 `Illuminate\Foundation\Auth\User` 기본 클래스 덕분에 기본 `App\Models\User` 모델에서 사용할 수 있습니다. 이메일 인증이 완료되면 사용자를 원하는 곳으로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재발송

때때로 사용자가 이메일 인증 메일을 잃어버리거나 실수로 삭제할 수 있습니다. 이를 위해, 사용자가 인증 이메일을 다시 받을 수 있도록 라우트를 추가할 수 있습니다. [인증 안내 뷰](#the-email-verification-notice)에 간단한 폼 제출 버튼을 넣어 이 라우트로 요청을 보낼 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', '인증 링크가 발송되었습니다!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용하여 인증된 사용자만 특정 라우트에 접근하도록 할 수 있습니다. Laravel에는 `verified` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)이 포함되어 있는데, 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스의 별칭입니다. 이 별칭은 Laravel에서 이미 자동으로 등록되어 있으므로, 라우트 정의에 `verified` 미들웨어만 붙이면 됩니다. 보통은 `auth` 미들웨어와 함께 사용합니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 접근할 수 있습니다...
})->middleware(['auth', 'verified']);
```

이 미들웨어가 적용된 라우트에 이메일을 인증하지 않은 사용자가 접근하면 자동으로 `verification.notice` [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
## 커스터마이징

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징

기본 이메일 인증 알림도 대부분의 애플리케이션에서 충분하지만, Laravel은 이메일 인증 메일 메시지 구성 방식을 커스터마이즈할 수 있도록 지원합니다.

시작하려면, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드로 클로저를 전달하세요. 이 클로저는 알림을 받는 notifiable 모델 인스턴스와, 사용자가 인증을 위해 방문해야 하는 서명된 이메일 인증 URL을 인자로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하세요:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('이메일 주소 인증')
            ->line('아래 버튼을 클릭하여 이메일 주소를 인증하세요.')
            ->action('이메일 주소 인증', $url);
    });
}
```

> [!NOTE]  
> 메일 알림에 대해 더 자세히 알고 싶으시면, [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우, 이메일 인증 과정에서 Laravel은 `Illuminate\Auth\Events\Verified` [이벤트](/docs/{{version}}/events)를 디스패치합니다. 애플리케이션에서 이메일 인증을 직접 처리하는 경우, 인증 완료 후 이 이벤트를 수동으로 디스패치할 수도 있습니다.
