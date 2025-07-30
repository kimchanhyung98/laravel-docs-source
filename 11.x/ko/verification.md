# 이메일 인증 (Email Verification)

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
## 소개 (Introduction)

많은 웹 애플리케이션에서 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 직접 이 기능을 구현할 필요 없이, Laravel은 이메일 인증 요청을 전송하고 검증하는 편리한 내장 서비스를 제공합니다.

> [!NOTE]  
> 빠르게 시작하고 싶다면, 새로운 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits) 중 하나를 설치하세요. 스타터 킷은 이메일 인증 지원을 포함한 전체 인증 시스템의 기반을 자동으로 구성해 줍니다.

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

모델에 이 인터페이스가 추가되면, 새로 등록한 사용자에게 이메일 인증 링크가 자동으로 담긴 이메일이 발송됩니다. 이는 Laravel이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/11.x/events)를 자동으로 등록하기 때문에 원활하게 작동합니다.

만약 [스타터 킷](/docs/11.x/starter-kits)을 사용하지 않고 직접 회원가입을 구현하는 경우, 사용자의 등록이 성공한 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 수동으로 디스패치해야 합니다:

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

다음으로, `users` 테이블에 사용자의 이메일이 인증된 시각을 저장할 `email_verified_at` 컬럼이 있어야 합니다. 이 컬럼은 보통 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 마이그레이션에 포함되어 있습니다.

<a name="verification-routing"></a>
## 라우팅 (Routing)

이메일 인증을 제대로 구현하려면 세 개의 라우트를 정의해야 합니다. 먼저, 등록 후 Laravel이 사용자에게 보낸 인증 이메일의 링크를 클릭하라는 안내를 보여줄 라우트가 필요합니다.

두 번째, 사용자가 이메일 내 인증 링크를 클릭할 때 이 요청을 처리할 라우트가 필요합니다.

세 번째, 사용자가 최초 인증 링크를 잃어버렸을 경우 인증 링크를 재전송하는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 안내 (The Email Verification Notice)

앞서 언급한 것처럼, 등록 후 Laravel이 보낸 이메일 인증 링크를 클릭하라는 안내 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 이메일 인증을 완료하지 않은 사용자가 애플리케이션의 다른 부분에 접근하려 할 때 표시됩니다. 이 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하는 한 자동으로 이메일로 발송됩니다:

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이메일 인증 안내를 반환하는 라우트의 이름은 반드시 `verification.notice`여야 합니다. 이는 Laravel에 포함된 `verified` 미들웨어가 이메일 인증이 완료되지 않았을 경우 자동으로 이 라우트로 리다이렉트하기 때문입니다.

> [!NOTE]  
> 이메일 인증을 직접 구현할 경우, 인증 안내 뷰 내용을 직접 정의해야 합니다. 인증과 관련된 필요한 모든 뷰를 포함하는 스캐폴딩이 필요하면 [Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기 (The Email Verification Handler)

다음으로, 사용자가 이메일 인증 링크를 클릭할 때 생성되는 요청을 처리하는 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름을 가져야 하며, `auth`와 `signed` 미들웨어가 적용되어야 합니다:

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

잠시 이 라우트에 대해 자세히 살펴보겠습니다. 우선, 일반적인 `Illuminate\Http\Request` 대신 `EmailVerificationRequest` 타입을 사용했습니다. 이 `EmailVerificationRequest`는 Laravel에 포함된 [폼 요청](/docs/11.x/validation#form-request-validation) 클래스로, 요청의 `id`와 `hash` 파라미터를 자동으로 검증합니다.

그다음, `fulfill` 메서드를 호출하는데, 이 메서드는 인증된 사용자에게 `markEmailAsVerified` 메서드를 호출하고 `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다. `markEmailAsVerified` 메서드는 기본 `App\Models\User`가 확장하는 `Illuminate\Foundation\Auth\User` 클래스에 제공됩니다. 사용자의 이메일 인증이 완료되면 원하는 위치로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송 (Resending the Verification Email)

사용자가 인증 이메일을 잘못 삭제하거나 분실하는 경우가 있습니다. 이를 위해 인증 이메일 재전송을 요청할 수 있는 라우트를 정의할 수 있습니다. 이 라우트에는 단순한 폼 제출 버튼을 [이메일 인증 안내 뷰](#the-email-verification-notice)에 추가해 요청할 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/11.x/middleware)를 통해 이메일 인증을 완료한 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스의 별칭인 `verified` 미들웨어를 기본으로 제공합니다. 이 별칭은 Laravel에 의해 자동 등록되므로, 단순히 `verified` 미들웨어를 라우트에 붙이기만 하면 됩니다. 보통은 `auth` 미들웨어와 함께 사용합니다:

```
Route::get('/profile', function () {
    // 이메일 인증된 사용자만 이 라우트에 접근 가능...
})->middleware(['auth', 'verified']);
```

인증하지 않은 사용자가 이 미들웨어가 지정된 라우트에 접근하면, 자동으로 `verification.notice` [네임드 라우트](/docs/11.x/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
## 커스터마이징 (Customization)

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징 (Verification Email Customization)

기본 이메일 인증 알림으로도 대부분 애플리케이션에서 충분하지만, 이메일 인증 메일 메시지를 직접 커스터마이징 하는 것도 가능합니다.

이는 `Illuminate\Auth\Notifications\VerifyEmail` 알림 클래스가 제공하는 `toMailUsing` 메서드에 클로저를 전달하여 시작합니다. 클로저는 알림을 받는 노티파이어(notifiable) 모델 인스턴스와 사용자가 이메일 인증을 위해 방문해야 하는 서명된 이메일 인증 URL을 인수로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드 내에서 작성합니다:

```
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
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> [!NOTE]  
> 메일 알림에 관해 더 자세히 알고 싶다면, [메일 알림 문서](/docs/11.x/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트 (Events)

[Laravel 애플리케이션 스타터 킷](/docs/11.x/starter-kits)을 사용할 경우, Laravel은 이메일 인증 과정 중 `Illuminate\Auth\Events\Verified` [이벤트](/docs/11.x/events)를 디스패치합니다. 애플리케이션에서 이메일 인증을 직접 처리한다면, 인증이 완료된 후 직접 이 이벤트들을 디스패치할 수도 있습니다.