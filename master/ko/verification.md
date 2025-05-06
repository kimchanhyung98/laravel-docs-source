# 이메일 인증

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 안내](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [커스터마이징](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 직접 이 기능을 구현할 필요가 없도록, Laravel은 이메일 인증 요청을 보내고 검증하는 편리한 기본 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 설치하세요. 스타터 키트는 이메일 인증 지원을 포함하여 인증 시스템 전체를 자동으로 구성합니다.

<a name="model-preparation"></a>
### 모델 준비

시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약을 구현하는지 확인하세요:

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

이 인터페이스가 모델에 추가되면, 신규 등록된 사용자에게 이메일 인증 링크가 포함된 이메일이 자동으로 전송됩니다. 이는 Laravel이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)를 자동으로 등록하기 때문에 자연스럽게 동작합니다.

[스타터 키트](/docs/{{version}}/starter-kits)를 사용하지 않고 애플리케이션 내에서 회원가입을 직접 구현하는 경우, 사용자의 회원가입이 성공한 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트가 발생하도록 해야 합니다:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, `users` 테이블에 사용자의 이메일이 인증된 날짜와 시간을 저장할 수 있도록 `email_verified_at` 컬럼이 포함되어야 합니다. 일반적으로 이 컬럼은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 올바르게 구현하려면 세 개의 라우트를 정의해야 합니다. 첫째, 사용자가 회원가입 후 이메일로 받은 인증 링크를 클릭해야 한다는 안내를 표시하는 라우트가 필요합니다.

둘째, 사용자가 메일의 인증 링크를 클릭했을 때 처리할 라우트가 필요합니다.

셋째, 사용자가 인증 링크를 분실했을 때 인증 메일을 재발송하는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 안내

앞서 언급한 바와 같이, 회원가입 후 Laravel이 이메일로 보낸 인증 링크를 클릭하라는 안내를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 인증을 하지 않은 상태에서 애플리케이션의 다른 부분에 접근하려고 할 때 표시됩니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하면 인증 링크는 자동으로 전송됩니다:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이메일 인증 안내를 반환하는 라우트는 반드시 `verification.notice`라는 이름이어야 합니다. 이 이름이 정확히 할당되어야 하는 이유는, [Laravel에 포함된](#protecting-routes) `verified` 미들웨어가 사용자의 이메일이 인증되지 않은 경우 자동으로 이 라우트로 리디렉션하기 때문입니다.

> [!NOTE]
> 이메일 인증을 수동으로 구현하는 경우, 인증 안내 뷰의 내용을 직접 정의해야 합니다. 모든 필요한 인증 및 인증 뷰가 포함된 스캐폴딩을 원하신다면 [Laravel 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기

다음으로, 사용자가 이메일로 받은 인증 링크를 클릭했을 때 처리할 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름을 가지며 `auth`, `signed` 미들웨어가 적용되어야 합니다:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

여기서 이 라우트를 좀 더 자세히 살펴보겠습니다. 먼저 일반적인 `Illuminate\Http\Request` 인스턴스 대신 `EmailVerificationRequest` 요청 타입을 사용합니다. `EmailVerificationRequest`는 Laravel에 포함된 [폼 요청](/docs/{{version}}/validation#form-request-validation)으로, 요청의 `id`와 `hash` 파라미터를 자동으로 검증해줍니다.

다음으로, `fulfill` 메서드를 바로 호출할 수 있습니다. 이 메서드는 인증된 사용자에 대해 `markEmailAsVerified` 메서드를 호출하고, `Illuminate\Auth\Events\Verified` 이벤트를 발생시킵니다. `markEmailAsVerified` 메서드는 `Illuminate\Foundation\Auth\User` 기본 클래스를 통해 기본 `App\Models\User` 모델에서 제공됩니다. 사용자의 이메일 주소가 인증된 후에는 원하는 곳으로 리디렉션할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송

사용자가 인증 이메일을 분실하거나 실수로 삭제할 수도 있습니다. 이런 경우를 위해, 사용자가 인증 이메일 재전송을 요청할 수 있는 라우트를 정의할 수 있습니다. 이 라우트는 [인증 안내 뷰](#the-email-verification-notice) 내에 간단한 폼 버튼을 두어 요청할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용하여 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스의 [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)인 `verified`를 제공합니다. 이 별칭은 이미 Laravel에 의해 자동 등록되므로, 라우트 정의에 `verified` 미들웨어만 붙이면 됩니다. 일반적으로 이 미들웨어는 `auth` 미들웨어와 함께 사용됩니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware(['auth', 'verified']);
```

인증되지 않은 사용자가 이 미들웨어가 적용된 라우트에 접근하려 하면, 자동으로 `verification.notice` [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션됩니다.

<a name="customization"></a>
## 커스터마이징

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징

기본 이메일 인증 알림은 대부분 애플리케이션의 요구를 충족하지만, Laravel은 인증 메일 메시지를 커스터마이징할 수 있는 방법을 제공합니다.

우선, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드에 클로저를 전달하세요. 이 클로저는 알림을 받을 모델 인스턴스와 사용자가 이메일 주소를 인증하기 위해 방문해야 할 서명된 인증 URL을 전달받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 `toMailUsing` 메서드를 호출합니다:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * 애플리케이션 서비스 부트스트랩.
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
> 메일 알림에 대해 더 자세히 알고 싶다면 [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[Laravel 스타터 키트](/docs/{{version}}/starter-kits)를 사용할 때, Laravel은 이메일 인증 과정에서 `Illuminate\Auth\Events\Verified` [이벤트](/docs/{{version}}/events)를 디스패치합니다. 애플리케이션에서 이메일 인증을 직접 처리하는 경우에도 인증 완료 후 이러한 이벤트를 수동으로 발생시킬 수 있습니다.