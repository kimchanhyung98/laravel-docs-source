# 이메일 인증 (Email Verification)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 알림](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [커스터마이징](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션을 이용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 직접 이 기능을 구현하는 대신, Laravel은 이메일 인증 요청을 보내고 확인하는 데 편리한 내장 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits) 중 하나를 설치해 보세요. 스타터 키트는 이메일 인증 지원을 포함한 전체 인증 시스템을 자동으로 구성해 줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

시작하기 전에 `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하는지 확인하세요:

```
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

모델에 이 인터페이스를 추가하면, 새로 등록된 사용자에게 자동으로 이메일 인증 링크가 포함된 이메일이 발송됩니다. 애플리케이션의 `App\Providers\EventServiceProvider`를 살펴보면, Laravel이 이미 `Illuminate\Auth\Events\Registered` 이벤트에 연결된 `SendEmailVerificationNotification` [리스너](/docs/9.x/events)를 포함하고 있음을 알 수 있습니다. 이 이벤트 리스너가 사용자에게 인증 이메일 링크를 보내는 역할을 합니다.

만약 스타터 키트를 사용하지 않고 직접 회원 가입 로직을 구현하는 경우, 회원 가입이 성공하면 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 직접 발송해야 합니다:

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

다음으로, `users` 테이블에 사용자의 이메일 주소 인증 완료 시각을 저장할 `email_verified_at` 컬럼이 포함되어 있어야 합니다. 기본적으로 Laravel에 포함된 `users` 테이블 마이그레이션은 이미 이 컬럼을 포함하므로, 데이터베이스 마이그레이션을 실행하면 됩니다:

```shell
php artisan migrate
```

<a name="verification-routing"></a>
## 라우팅 (Routing)

이메일 인증을 제대로 구현하려면, 세 가지 라우트를 정의해야 합니다. 첫째, 사용자에게 이메일 인증 링크를 클릭하라는 알림을 보여줄 라우트입니다. 이 알림은 사용자가 회원 가입 후 Laravel이 보낸 인증 이메일에서 링크를 클릭하도록 안내하기 위한 것입니다.

둘째, 사용자가 이메일 인증 링크를 클릭했을 때 요청을 처리할 라우트가 필요합니다.

셋째, 사용자가 처음 인증 링크를 분실했거나 삭제했을 경우, 인증 링크를 재전송할 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림 (The Email Verification Notice)

앞서 언급한 대로, 사용자가 회원 가입 후 Laravel이 보낸 이메일 인증 링크를 클릭하도록 안내하는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 이메일 인증을 완료하지 않은 사용자가 다른 애플리케이션 부분에 접근할 때 보여집니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면, 링크는 자동으로 이메일로 전송됩니다:

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이메일 인증 알림을 반환하는 라우트는 반드시 `verification.notice`라는 이름을 가져야 합니다. 이 이름은 Laravel 내장 `verified` 미들웨어가 사용자 이메일이 확인되지 않았을 때 자동으로 리다이렉트하는 대상이기 때문에 중요합니다.

> [!NOTE]
> 이메일 인증을 수동으로 구현하는 경우, 인증 알림 뷰의 내용을 직접 정의해야 합니다. 필요 시 모든 인증 및 인증 관련 뷰가 포함된 [Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기 (The Email Verification Handler)

이제, 사용자가 인증 이메일의 링크를 클릭했을 때 요청을 처리할 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름을 가지며 `auth`와 `signed` 미들웨어가 적용되어야 합니다:

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

이 라우트를 좀 더 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 대신에 `EmailVerificationRequest` 요청 객체를 사용하고 있습니다. `EmailVerificationRequest`는 Laravel에 내장된 [폼 요청](/docs/9.x/validation#form-request-validation) 객체로, 요청 파라미터인 `id`와 `hash` 값을 자동으로 검증해 줍니다.

그 후, `fulfill` 메서드를 호출하는데, 이 메서드는 인증된 사용자의 `markEmailAsVerified` 메서드를 호출해 이메일 인증을 완료 처리하고, `Illuminate\Auth\Events\Verified` 이벤트를 발동합니다. `markEmailAsVerified` 메서드는 기본 `App\Models\User` 모델이 상속하는 `Illuminate\Foundation\Auth\User` 클래스에서 제공됩니다. 이메일 인증이 완료되면 원하는 페이지로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송 (Resending The Verification Email)

사용자가 인증 이메일을 분실하거나 실수로 삭제할 수 있기 때문에, 인증 이메일 재전송을 처리하는 라우트를 정의하는 것이 좋습니다. 사용자는 [인증 알림 뷰](#the-email-verification-notice)에 간단한 폼 제출 버튼을 배치해 이 라우트에 요청을 보낼 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/9.x/middleware)를 사용해 인증된 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 참조하는 `verified` 미들웨어를 기본으로 제공합니다. 이 미들웨어는 애플리케이션의 HTTP 커널에 이미 등록돼 있으므로, 라우트 정의에 단순히 미들웨어를 추가하기만 하면 됩니다. 보통 `auth` 미들웨어와 함께 사용합니다:

```
Route::get('/profile', function () {
    // 인증 이메일을 확인한 사용자만 접근 가능합니다...
})->middleware(['auth', 'verified']);
```

인증되지 않은 사용자가 이 미들웨어가 적용된 라우트에 접근하면, 자동으로 `verification.notice` [명명된 라우트](/docs/9.x/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
## 커스터마이징 (Customization)

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징 (Verification Email Customization)

기본 이메일 인증 알림은 대부분 애플리케이션 요구사항을 충족하지만, Laravel은 이메일 인증 메일 메시지의 구성을 커스터마이징할 수 있도록 지원합니다.

먼저, `Illuminate\Auth\Notifications\VerifyEmail` 알림 클래스가 제공하는 `toMailUsing` 메서드에 클로저를 전달하세요. 이 클로저는 알림을 받을 모델 인스턴스와 사용자가 이메일 인증을 위해 방문해야 하는 서명된 URL을 인수로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스 안의 `boot` 메서드에서 `toMailUsing`을 호출합니다:

```
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * 인증/인가 서비스를 등록합니다.
 *
 * @return void
 */
public function boot()
{
    // ...

    VerifyEmail::toMailUsing(function ($notifiable, $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> [!NOTE]
> 이메일 알림에 대해 더 알고 싶다면 [메일 알림 문서](/docs/9.x/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트 (Events)

[Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits)를 사용할 경우, 이메일 인증 과정 중 Laravel이 자동으로 [이벤트](/docs/9.x/events)를 발송합니다. 수동으로 인증 로직을 구현 중인 경우, 인증 완료 후 이 이벤트들을 직접 발송하는 것이 좋습니다. 애플리케이션의 `EventServiceProvider`에 이벤트 리스너를 등록할 수 있습니다:

```
use App\Listeners\LogVerifiedUser;
use Illuminate\Auth\Events\Verified;

/**
 * 애플리케이션 이벤트 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    Verified::class => [
        LogVerifiedUser::class,
    ],
];
```