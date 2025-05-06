# 이메일 인증

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
## 소개

많은 웹 애플리케이션에서는 사용자가 애플리케이션을 이용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 직접 이 기능을 구현할 필요 없이, Laravel은 이메일 인증 요청을 보내고 인증하는 기능을 편리하게 제공하고 있습니다.

> [!NOTE]  
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 설치하세요. 스타터 킷은 이메일 인증 지원을 포함하여 전체 인증 시스템 구성을 알아서 처리해 줍니다.

<a name="model-preparation"></a>
### 모델 준비

시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약을 구현하고 있는지 확인하세요:

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

이 인터페이스를 모델에 추가하면 새로 등록된 사용자에게 자동으로 이메일 인증 링크가 포함된 이메일이 전송됩니다. 애플리케이션의 `App\Providers\EventServiceProvider`를 살펴보면, Laravel에는 이미 `SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)가 `Illuminate\Auth\Events\Registered` 이벤트에 등록되어 있음을 확인할 수 있습니다. 이 이벤트 리스너는 사용자에게 이메일 인증 링크를 전송합니다.

[스타터 킷](/docs/{{version}}/starter-kits)을 사용하지 않고 직접 회원가입을 구현하는 경우, 사용자의 회원가입이 성공한 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 디스패치해야 합니다:

    use Illuminate\Auth\Events\Registered;

    event(new Registered($user));

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, 사용자의 이메일 주소가 인증된 날짜와 시간을 저장하기 위해 `users` 테이블에 `email_verified_at` 컬럼이 있어야 합니다. 기본적으로, Laravel 프레임워크와 함께 제공되는 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다. 따라서 데이터베이스 마이그레이션만 실행하면 됩니다:

```shell
php artisan migrate
```

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 제대로 구현하려면 세 개의 라우트를 정의해야 합니다. 먼저, 회원 가입 후 Laravel이 전송한 이메일의 인증 링크를 클릭하라는 안내를 사용자에게 보여주는 라우트가 필요합니다.

둘째, 사용자가 이메일의 인증 링크를 클릭하면 해당 요청을 처리하는 라우트가 필요합니다.

셋째, 사용자가 인증 링크를 실수로 분실한 경우 재전송할 수 있는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림

앞서 언급했듯, 회원가입 후 Laravel이 전송한 이메일 인증 링크를 클릭하라는 안내 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일을 인증하지 않고 애플리케이션의 다른 부분에 접근하려 할 때 표시됩니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있는 한, 인증 링크가 자동으로 사용자에게 전송됩니다:

    Route::get('/email/verify', function () {
        return view('auth.verify-email');
    })->middleware('auth')->name('verification.notice');

이메일 인증 알림을 반환하는 라우트는 반드시 `verification.notice`라는 이름으로 지정해야 합니다. 이는 [Laravel에 기본 포함된](#protecting-routes) `verified` 미들웨어가 사용자의 이메일이 인증되지 않았을 때 자동으로 이 라우트 이름으로 리디렉션하기 때문입니다.

> [!NOTE]  
> 이메일 인증을 직접 구현하는 경우, 인증 알림 뷰의 내용을 스스로 정의해야 합니다. 모든 필수 인증 및 인증 뷰가 포함된 구조가 필요하다면 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 확인하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기

다음으로, 사용자가 이메일로 전송된 인증 링크를 클릭할 때 발생하는 요청을 처리하는 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름과 `auth`, `signed` 미들웨어를 할당해야 합니다:

    use Illuminate\Foundation\Auth\EmailVerificationRequest;

    Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
        $request->fulfill();

        return redirect('/home');
    })->middleware(['auth', 'signed'])->name('verification.verify');

여기서 조금 더 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 인스턴스 대신 `EmailVerificationRequest` 타입을 사용하고 있음을 알 수 있습니다. `EmailVerificationRequest`는 Laravel에 포함된 [폼 요청](/docs/{{version}}/validation#form-request-validation)으로, 요청의 `id`와 `hash` 파라미터를 자동으로 검증합니다.

그 다음 바로 `fulfill` 메서드를 호출할 수 있습니다. 이 메서드는 인증된 사용자에게 `markEmailAsVerified` 메서드를 호출하고, `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다. `markEmailAsVerified` 메서드는 `Illuminate\Foundation\Auth\User` 기본 클래스 덕분에 기본 `App\Models\User` 모델에서 이용 가능합니다. 사용자의 이메일 주소가 인증된 후에는 원하는 위치로 리디렉션할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송

가끔 사용자가 이메일 인증 메일을 분실하거나 실수로 삭제할 수도 있습니다. 이를 위해, 사용자가 인증 이메일을 재요청할 수 있도록 하는 라우트를 정의할 수 있습니다. [인증 알림 뷰](#the-email-verification-notice) 내에 간단한 폼 제출 버튼을 두고 이 라우트로 요청을 보낼 수 있습니다:

    use Illuminate\Http\Request;

    Route::post('/email/verification-notification', function (Request $request) {
        $request->user()->sendEmailVerificationNotification();

        return back()->with('message', 'Verification link sent!');
    })->middleware(['auth', 'throttle:6,1'])->name('verification.send');

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 이용하면 인증된 사용자만 특정 라우트에 접근할 수 있도록 제어할 수 있습니다. Laravel은 `verified` 미들웨어 별칭(별명)을 기본 제공하며, 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스의 별칭입니다. 이 미들웨어는 애플리케이션의 HTTP 커널에 이미 등록되어 있으므로, 라우트에 이 미들웨어만 추가하면 됩니다. 일반적으로 `auth` 미들웨어와 함께 사용합니다:

    Route::get('/profile', function () {
        // 인증된 사용자만 접근 가능...
    })->middleware(['auth', 'verified']);

이 미들웨어가 할당된 라우트에 인증되지 않은 사용자가 접근하려 하면, 자동으로 `verification.notice` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션됩니다.

<a name="customization"></a>
## 커스터마이징

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징

기본 이메일 인증 알림으로도 대부분의 애플리케이션에서 충분하지만, Laravel은 이메일 인증 메일의 내용을 자유롭게 커스터마이징 할 수 있게 해줍니다.

먼저, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드에 클로저(Closure)를 전달하세요. 클로저는 알림을 받는 노티파이어블 모델 인스턴스와 사용자가 이메일 주소를 인증하기 위해 방문해야 하는 서명된 인증 URL을 전달받습니다. 클로저는 반드시 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

    use Illuminate\Auth\Notifications\VerifyEmail;
    use Illuminate\Notifications\Messages\MailMessage;

    /**
     * 인증/권한 서비스를 등록합니다.
     */
    public function boot(): void
    {
        // ...

        VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
            return (new MailMessage)
                ->subject('이메일 주소를 인증하세요')
                ->line('아래 버튼을 클릭하여 이메일 주소를 인증하세요.')
                ->action('이메일 인증', $url);
        });
    }

> [!NOTE]  
> 이메일 알림에 대해 더 알아보고 싶다면 [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 경우, 이메일 인증 과정에서 Laravel이 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 애플리케이션에서 이메일 인증을 직접 처리하는 경우에도, 인증이 완료된 후 해당 이벤트를 직접 디스패치할 수 있습니다. 애플리케이션의 `EventServiceProvider`에서 이 이벤트에 리스너를 등록할 수 있습니다:

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