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

많은 웹 애플리케이션은 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 애플리케이션마다 직접 이 기능을 구현하는 대신, Laravel은 이메일 인증 요청을 전송하고 확인하는 편리한 내장 서비스를 제공합니다.

> [!TIP]
> 빠르게 시작하고 싶다면, 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 설치하세요. 스타터 킷은 이메일 인증 지원을 포함한 전체 인증 시스템의 스캐폴딩을 처리해 줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하고 있는지 확인하세요:

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

모델에 이 인터페이스가 추가되면, 새로 등록된 사용자에게 이메일 인증 링크가 포함된 이메일이 자동으로 전송됩니다. `App\Providers\EventServiceProvider`를 살펴보면, Laravel이 이미 `Illuminate\Auth\Events\Registered` 이벤트에 연결된 `SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)를 포함하고 있음을 확인할 수 있습니다. 이 이벤트 리스너가 사용자에게 이메일 인증 링크를 전송합니다.

만약 [스타터 킷](/docs/{{version}}/starter-kits)을 사용하지 않고 직접 회원가입 기능을 구현한다면, 사용자 등록 성공 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 디스패치해야 합니다:

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

다음으로, `users` 테이블에 사용자의 이메일이 인증된 날짜와 시간을 저장할 `email_verified_at` 컬럼이 있어야 합니다. 기본적으로 Laravel 프레임워크에 포함된 `users` 테이블 마이그레이션에 이미 이 컬럼이 포함되어 있습니다. 따라서 데이터베이스 마이그레이션을 실행하면 됩니다:

```
php artisan migrate
```

<a name="verification-routing"></a>
## 라우팅 (Routing)

이메일 인증을 올바르게 구현하려면 세 가지 라우트를 정의해야 합니다. 

첫째, 사용자가 가입 후 Laravel이 전송한 인증 이메일의 링크를 클릭하라는 알림을 보여주는 라우트가 필요합니다.

둘째, 사용자가 이메일에 포함된 인증 링크를 클릭했을 때 발생하는 요청을 처리하는 라우트가 필요합니다.

셋째, 사용자가 처음 받은 인증 이메일을 분실했을 경우 인증 링크를 재전송하는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림 (The Email Verification Notice)

앞서 언급했듯, Laravel이 회원가입 후 자동으로 사용자에게 이메일 인증 링크를 이메일로 전송하기 때문에, 사용자가 이메일을 확인할 수 있도록 안내하는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일을 인증하지 않은 상태로 애플리케이션의 다른 부분에 접근하려고 할 때 표시됩니다. 

다음은 인증 알림을 위한 라우트 예시입니다:

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이 라우트는 `verification.notice`라는 이름을 가져야 합니다. 이 이름을 반드시 지정해야 하는데, Laravel에 포함된 `verified` 미들웨어가 이메일을 인증하지 않은 사용자를 이 라우트로 자동 리다이렉트하기 때문입니다.

> [!TIP]
> 이메일 인증을 직접 구현하는 경우, 인증 알림 뷰를 직접 정의해야 합니다. 필요한 모든 인증 및 인증 뷰가 포함된 스캐폴딩을 원한다면 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기 (The Email Verification Handler)

다음으로, 사용자가 이메일의 인증 링크를 클릭했을 때 발생하는 요청을 처리할 라우트를 정의합니다. 이 라우트는 `verification.verify`라는 이름을 가지고, `auth`와 `signed` 미들웨어가 할당되어야 합니다:

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

여기서 `EmailVerificationRequest`를 사용하는데, 이는 Laravel에 포함된 [폼 요청](/docs/{{version}}/validation#form-request-validation) 클래스입니다. 이 클래스는 요청의 `id`와 `hash` 파라미터를 자동으로 검증합니다.

`fulfill` 메서드를 호출하면 인증된 사용자의 `markEmailAsVerified` 메서드가 실행되고, `Illuminate\Auth\Events\Verified` 이벤트가 디스패치됩니다. 기본 `App\Models\User` 모델은 `Illuminate\Foundation\Auth\User` 기본 클래스를 통해 `markEmailAsVerified` 메서드를 사용할 수 있습니다. 사용자의 이메일이 인증된 후에는 원하는 위치로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송 (Resending The Verification Email)

사용자가 인증 이메일을 실수로 삭제하거나 분실할 수 있습니다. 이를 대비해 인증 이메일을 재전송할 수 있는 라우트를 정의할 수 있습니다. 해당 라우트로 요청을 보내는 간단한 폼 제출 버튼을 [인증 알림 뷰](#the-email-verification-notice)에 추가하면 됩니다:

```
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용해 이메일 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 `verified` 미들웨어를 기본으로 제공하며, 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 참조합니다. 이 미들웨어는 애플리케이션의 HTTP 커널에 이미 등록되어 있으므로, 라우트 정의에 미들웨어만 할당하면 됩니다:

```
Route::get('/profile', function () {
    // 이메일 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('verified');
```

이메일 미인증 사용자가 이 미들웨어가 할당된 라우트에 접근 시도하면, 자동으로 `verification.notice` [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
## 커스터마이징 (Customization)

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징 (Verification Email Customization)

기본 이메일 인증 알림은 대부분의 애플리케이션 요구사항을 충족하지만, Laravel은 이메일 인증 메일 메시지 생성 방식을 커스터마이징할 수 있는 유연성을 제공합니다.

먼저, `Illuminate\Auth\Notifications\VerifyEmail` 알림의 `toMailUsing` 메서드에 클로저를 전달하세요. 클로저는 알림을 받는 모델 인스턴스와 사용자가 이메일 인증을 위해 방문해야 하는 서명된 이메일 인증 URL을 전달받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 보통 이 코드는 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Register any authentication / authorization services.
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

> [!TIP]
> 메일 알림에 대해 더 알고 싶다면 [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트 (Events)

[Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 경우, 인증 과정 중에 [이벤트](/docs/{{version}}/events)가 자동으로 디스패치됩니다. 직접 이메일 인증을 구현하는 경우에는 인증 완료 후 수동으로 이러한 이벤트를 디스패치하는 것이 좋습니다. 애플리케이션의 `EventServiceProvider`에서 이벤트 리스너를 등록할 수 있습니다:

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Auth\Events\Verified' => [
        'App\Listeners\LogVerifiedUser',
    ],
];
```