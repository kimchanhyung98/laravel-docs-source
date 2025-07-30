# 이메일 인증 (Email Verification)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 알림](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [맞춤화](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션에서는 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 각 애플리케이션마다 직접 기능을 새로 구현하지 않도록, Laravel은 이메일 인증 요청을 보내고 확인하는 데 유용한 내장 서비스를 제공합니다.

> [!NOTE]  
> 빠르게 시작하고 싶다면, 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/10.x/starter-kits) 중 하나를 설치하세요. 스타터 키트는 이메일 인증 지원을 포함한 전체 인증 시스템의 기본 골격을 자동으로 구성해 줍니다.

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

이 인터페이스를 모델에 추가하면, 새로 가입하는 사용자에게 이메일 인증 링크가 포함된 이메일이 자동으로 발송됩니다. 애플리케이션의 `App\Providers\EventServiceProvider`를 확인해 보면, Laravel이 이미 `Illuminate\Auth\Events\Registered` 이벤트에 연결된 `SendEmailVerificationNotification` [리스너](/docs/10.x/events)를 포함하고 있음을 알 수 있습니다. 이 이벤트 리스너가 이메일 인증 링크를 사용자에게 발송합니다.

만약 [스타터 키트](/docs/10.x/starter-kits)를 사용하지 않고 직접 회원가입을 구현하고 있다면, 가입 성공 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 발행해야 합니다:

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

다음으로, `users` 테이블에 사용자의 이메일 인증 일시를 저장할 `email_verified_at` 컬럼이 있어야 합니다. 기본적으로 Laravel 프레임워크에 포함된 `users` 테이블 마이그레이션에는 이 컬럼이 이미 포함되어 있습니다. 따라서, 데이터베이스 마이그레이션을 실행하기만 하면 됩니다:

```shell
php artisan migrate
```

<a name="verification-routing"></a>
## 라우팅 (Routing)

이메일 인증을 올바르게 구현하려면 세 가지 라우트를 정의해야 합니다.  
첫 번째는 사용자가 가입 후 Laravel이 보낸 이메일 인증 링크를 클릭하도록 안내하는 알림 페이지를 표시하는 라우트입니다.

두 번째는 사용자가 이메일 내 인증 링크를 클릭했을 때 처리하는 라우트입니다.

세 번째는 사용자가 실수로 첫 번째 인증 링크를 잃어버렸을 경우 인증 링크를 재전송하는 라우트입니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림 (The Email Verification Notice)

앞에서 언급한 대로, 가입 후 Laravel이 발송한 이메일 인증 링크를 사용자가 클릭하도록 안내하는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 인증을 완료하지 않고 애플리케이션의 다른 부분에 접근하려 할 때 표시됩니다. 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있는 한 자동으로 발송된다는 점을 기억하세요:

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이 이메일 인증 알림을 반환하는 라우트는 반드시 `verification.notice`라는 이름을 가져야 합니다. 그 이유는 Laravel의 `verified` 미들웨어가 이메일 인증하지 않은 사용자를 이 라우트 이름으로 자동 리다이렉트하기 때문입니다([라우트 보호](#protecting-routes) 참고).

> [!NOTE]  
> 이메일 인증을 수동으로 구현할 경우, 인증 알림 뷰 파일 내용을 직접 정의해야 합니다. 모든 필요한 인증 및 인증 뷰가 포함된 스캐폴딩이 필요하다면 [Laravel 애플리케이션 스타터 키트](/docs/10.x/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기 (The Email Verification Handler)

다음으로, 사용자가 이메일 인증 링크를 클릭했을 때 요청을 처리하는 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름을 갖고 `auth` 및 `signed` 미들웨어를 달아야 합니다:

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

이 라우트를 좀 더 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 대신 `EmailVerificationRequest` 타입을 사용하는 것을 알 수 있습니다. `EmailVerificationRequest`는 Laravel에 기본 포함된 [폼 요청](/docs/10.x/validation#form-request-validation)으로, 요청의 `id`와 `hash` 매개변수를 자동으로 검증해 줍니다.

그리고 `fulfill` 메서드를 호출하면 인증된 사용자에 대해 `markEmailAsVerified` 메서드가 실행되고, `Illuminate\Auth\Events\Verified` 이벤트가 발행됩니다. `markEmailAsVerified` 메서드는 기본 `App\Models\User` 모델이 상속하는 `Illuminate\Foundation\Auth\User` 클래스에서 제공됩니다. 이렇게 이메일 인증이 완료되면, 원하는 위치로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송 (Resending the Verification Email)

사용자가 인증 이메일을 분실하거나 실수로 삭제하는 일이 있습니다. 이를 위해 사용자가 인증 이메일을 다시 요청할 수 있는 라우트를 정의하는 것이 좋습니다. 그런 후, [인증 알림 뷰](#the-email-verification-notice)에 간단한 폼 제출 버튼을 배치해 이 라우트로 요청할 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/10.x/middleware)를 사용하여 이메일 인증한 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 가리키는 `verified` 미들웨어 별칭을 기본 제공합니다. 이 미들웨어는 이미 애플리케이션 HTTP 커널에 등록되어 있으므로, 라우트 정의에 `verified` 미들웨어를 추가하는 것으로 사용 가능합니다. 보통 `auth` 미들웨어와 함께 붙여 사용합니다:

```
Route::get('/profile', function () {
    // 이메일 인증된 사용자만 이 라우트를 이용할 수 있습니다...
})->middleware(['auth', 'verified']);
```

인증하지 않은 사용자가 이 미들웨어가 붙은 라우트에 접근하면 자동으로 `verification.notice` 이름이 붙은 라우트로 리다이렉트됩니다.

<a name="customization"></a>
## 맞춤화 (Customization)

<a name="verification-email-customization"></a>
#### 인증 이메일 맞춤화 (Verification Email Customization)

기본 이메일 인증 알림은 대부분의 애플리케이션에서 충분하지만, Laravel은 이메일 인증 메일 메시지 생성 방식을 직접 맞춤화할 수 있게 지원합니다.

시작하려면, `Illuminate\Auth\Notifications\VerifyEmail` 알림 클래스가 제공하는 `toMailUsing` 메서드에 클로저를 전달하세요. 클로저는 알림을 받는 모델 인스턴스와 사용자의 이메일 인증에 필요한 서명된 URL을 인수로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 내에서 `toMailUsing` 메서드를 호출합니다:

```
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> [!NOTE]  
> 메일 알림에 대해 더 자세히 알고 싶다면 [메일 알림 문서](/docs/10.x/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트 (Events)

[Laravel 애플리케이션 스타터 키트](/docs/10.x/starter-kits)를 사용할 경우, 이메일 인증 과정 중 Laravel이 [이벤트](/docs/10.x/events)를 자동으로 발행합니다. 이메일 인증을 수동 처리하는 경우, 인증 완료 후 직접 이 이벤트들을 발행하는 것이 좋습니다. 이벤트에 대한 리스너는 애플리케이션의 `EventServiceProvider`에 다음과 같이 등록할 수 있습니다:

```
use App\Listeners\LogVerifiedUser;
use Illuminate\Auth\Events\Verified;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    Verified::class => [
        LogVerifiedUser::class,
    ],
];
```