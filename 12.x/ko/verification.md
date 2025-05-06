# 이메일 인증

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 안내](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [커스터마이즈](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션들은 사용자가 앱을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 직접 이 기능을 구현하는 대신, 라라벨은 이메일 인증 요청을 전송하고 검증할 수 있는 편리한 내장 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 라라벨 애플리케이션에서 [라라벨 스타터 키트](/docs/{{version}}/starter-kits)를 설치해보세요. 스타터 키트는 이메일 인증 지원을 포함한 전체 인증 시스템의 스캐폴딩을 자동으로 처리해줍니다.

<a name="model-preparation"></a>
### 모델 준비

시작에 앞서, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약(Contract)을 구현하고 있는지 확인하세요:

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

이 인터페이스를 모델에 추가하면, 새로 등록된 사용자에게 이메일 인증 링크가 자동으로 전송됩니다. 이는 라라벨이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)를 자동으로 등록해주기 때문에 자연스럽게 동작합니다.

만약 [스타터 키트](/docs/{{version}}/starter-kits)를 사용하지 않고 직접 회원가입을 구현한다면, 사용자의 회원가입이 성공적으로 완료된 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 디스패치해야 합니다:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, 여러분의 `users` 테이블에는 사용자의 이메일이 인증된 날짜와 시간을 저장할 `email_verified_at` 컬럼이 반드시 존재해야 합니다. 이 컬럼은 보통 라라벨의 기본 `0001_01_01_000000_create_users_table.php` 마이그레이션 파일에 포함되어 있습니다.

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 올바르게 구현하기 위해서는 세 가지 라우트를 정의해야 합니다. 첫 번째는 사용자가 회원가입 후 라라벨이 보낸 인증 링크를 클릭하라는 안내를 표시하는 라우트입니다.

두 번째는 사용자가 이메일의 인증 링크를 클릭했을 때 해당 요청을 처리하는 라우트입니다.

세 번째는 사용자가 인증 링크를 잃어버렸을 경우 인증 링크를 재전송할 수 있도록 하는 라우트입니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 안내

앞서 언급했듯이, 회원가입 후 사용자가 이메일로 받은 인증 링크를 클릭하라는 안내를 보여주는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 주소 인증 없이 애플리케이션의 다른 부분에 접근하려 할 때 표시됩니다. 이메일 인증 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면 자동으로 전송됩니다:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이메일 인증 안내를 반환하는 라우트는 반드시 `verification.notice`라는 이름을 가져야 합니다. 라라벨에 [포함된](#protecting-routes) `verified` 미들웨어는 사용자가 이메일을 인증하지 않았을 경우 자동으로 이 이름의 라우트로 리디렉션시키기 때문입니다.

> [!NOTE]
> 이메일 인증을 직접 구현하는 경우, 인증 안내 뷰의 내용을 직접 정의해야 합니다. 인증, 이메일 인증 뷰가 모두 포함된 스캐폴딩이 필요하다면 [라라벨 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기

이제 사용자가 이메일로 받은 인증 링크를 클릭할 때 요청을 처리할 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름을 가져야 하며, `auth` 및 `signed` 미들웨어가 지정되어야 합니다:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

이 라우트를 좀 더 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 인스턴스 대신 `EmailVerificationRequest` 타입을 사용하고 있습니다. `EmailVerificationRequest`는 라라벨에서 제공하는 [폼 요청](/docs/{{version}}/validation#form-request-validation) 객체로, 요청에 포함된 `id`와 `hash` 파라미터의 유효성을 자동으로 검사해줍니다.

그 다음, `fulfill` 메서드를 바로 호출할 수 있습니다. 이 메서드는 인증된 사용자에게 `markEmailAsVerified` 메서드를 호출하고, `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다. `markEmailAsVerified` 메서드는 `Illuminate\Foundation\Auth\User` 기반 클래스에 의해 기본 `App\Models\User` 모델에서 사용할 수 있습니다. 사용자의 이메일이 인증되면, 원하는 곳으로 리디렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송

사용자가 인증 이메일을 실수로 분실하거나 삭제했을 수 있습니다. 이를 위해 사용자가 인증 이메일을 다시 받을 수 있도록 라우트를 정의할 수 있습니다. [인증 안내 뷰](#the-email-verification-notice)에 버튼 하나만 추가해 이 라우트로 요청을 보낼 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', '인증 링크가 전송되었습니다!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용하여 인증된 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. 라라벨에는 `verified`라는 [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)이 포함되어 있습니다. 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스에 대한 별칭입니다. 이 별칭은 자동으로 등록되어 있으므로, 라우트를 정의할 때 `verified` 미들웨어를 추가하기만 하면 됩니다. 일반적으로는 `auth` 미들웨어와 함께 사용합니다:

```php
Route::get('/profile', function () {
    // 인증된 사용자만 이 라우트에 접근 가능...
})->middleware(['auth', 'verified']);
```

만약 인증되지 않은 사용자가 이 미들웨어가 지정된 라우트에 접근하면, 자동으로 `verification.notice` [이름을 가진 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션됩니다.

<a name="customization"></a>
## 커스터마이즈

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이즈

기본 이메일 인증 알림은 대부분의 애플리케이션에서 충분하지만, 라라벨에서는 인증 이메일 메시지를 직접 커스터마이즈할 수도 있습니다.

이를 위해, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드에 클로저(익명 함수)를 전달하면 됩니다. 이 클로저는 알림을 받는 모델 인스턴스와 사용자가 이메일 인증을 위해 방문해야 할 서명된(URL이 검증된) 인증 주소를 인자로 받습니다. 클로저에서는 반드시 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 이 코드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('이메일 주소 인증')
            ->line('아래 버튼을 클릭하여 이메일 주소를 인증하세요.')
            ->action('이메일 주소 인증하기', $url);
    });
}
```

> [!NOTE]
> 메일 알림에 대해 더 알아보고 싶다면, [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[라라벨 스타터 키트](/docs/{{version}}/starter-kits)를 사용할 경우, 이메일 인증 과정에서 라라벨은 `Illuminate\Auth\Events\Verified` [이벤트](/docs/{{version}}/events)를 디스패치합니다. 만약 이메일 인증 과정을 직접 구현한다면, 인증 완료 후 이 이벤트를 수동으로 디스패치할 수도 있습니다.