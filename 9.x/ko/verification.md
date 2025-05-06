# 이메일 인증

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 알림](#the-email-verification-notice)
    - [이메일 인증 처리](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [커스터마이징](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. Laravel은 애플리케이션마다 이 기능을 직접 구현하지 않아도 되도록, 이메일 인증 요청을 전송하고 인증하는 편리한 빌트인 서비스를 제공합니다.

> **참고**  
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 설치해보세요. 스타터 키트는 이메일 인증 지원을 포함해 전체 인증 시스템의 스캐폴딩을 자동으로 구성해줍니다.

<a name="model-preparation"></a>
### 모델 준비

시작하기 전에, 여러분의 `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하고 있는지 확인하세요:

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

이 인터페이스를 모델에 추가하면, 새로 등록된 사용자에게는 자동으로 이메일 인증 링크가 포함된 이메일이 전송됩니다. `App\Providers\EventServiceProvider`를 살펴보면 알 수 있듯이, Laravel에는 이미 `SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)가 등록되어 있습니다. 이 리스너는 `Illuminate\Auth\Events\Registered` 이벤트에 연결되어 있으며, 해당 이벤트가 발생하면 인증 링크를 사용자에게 보내줍니다.

[스타터 키트](/docs/{{version}}/starter-kits)를 사용하지 않고 직접 회원가입 기능을 구현하는 경우, 회원가입 성공 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 디스패치해야 합니다:

    use Illuminate\Auth\Events\Registered;

    event(new Registered($user));

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, `users` 테이블에 사용자의 이메일 인증 날짜와 시간을 저장할 `email_verified_at` 컬럼이 존재해야 합니다. 기본적으로 Laravel 프레임워크와 함께 제공되는 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다. 따라서, 데이터베이스 마이그레이션만 실행하면 됩니다:

```shell
php artisan migrate
```

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 제대로 구현하려면 세 개의 라우트를 정의해야 합니다. 먼저, 사용자에게 이메일로 전송된 인증 링크를 클릭해야 한다는 알림을 보여주는 라우트가 필요합니다.

두 번째로, 사용자가 이메일에 포함된 인증 링크를 클릭할 때 발생하는 요청을 처리할 라우트가 필요합니다.

세 번째로, 사용자가 인증 링크를 분실했을 때 인증 링크를 재전송할 수 있는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림

앞서 언급했듯이, 사용자가 회원가입 후 이메일로 전송된 인증 링크를 클릭하도록 안내하는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 인증을 마치지 않고 애플리케이션의 다른 부분에 접근하려고 할 때 표시됩니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면, 인증 링크는 자동으로 이메일로 전송됩니다:

    Route::get('/email/verify', function () {
        return view('auth.verify-email');
    })->middleware('auth')->name('verification.notice');

이메일 인증 알림을 반환하는 라우트의 이름은 반드시 `verification.notice` 이어야 합니다. 이 이름이 중요한 이유는, [Laravel에 포함된](#protecting-routes) `verified` 미들웨어가 사용자가 이메일 인증을 완료하지 않은 경우 이 라우트로 자동 리다이렉트하기 때문입니다.

> **참고**  
> 이메일 인증을 직접 구현하는 경우, 인증 알림 뷰의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 인증 관련 뷰가 포함된 스캐폴딩이 필요하다면 [Laravel 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리

그 다음, 사용자에게 전송된 이메일 인증 링크를 클릭할 때 발생하는 요청을 처리할 라우트를 정의해야 합니다. 이 라우트의 이름은 `verification.verify`여야 하며, `auth`와 `signed` 미들웨어를 지정해야 합니다:

    use Illuminate\Foundation\Auth\EmailVerificationRequest;

    Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
        $request->fulfill();

        return redirect('/home');
    })->middleware(['auth', 'signed'])->name('verification.verify');

이 라우트를 좀 더 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 대신 `EmailVerificationRequest` 타입을 사용하고 있다는 점을 알 수 있습니다. `EmailVerificationRequest`는 Laravel에서 제공하는 [폼 요청](/docs/{{version}}/validation#form-request-validation)으로, `id`와 `hash` 파라미터의 유효성 검사를 자동으로 처리합니다.

다음으로, 요청 객체의 `fulfill` 메서드를 호출합니다. 이 메서드는 인증된 사용자 객체의 `markEmailAsVerified` 메서드를 호출하고, `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다. `markEmailAsVerified` 메서드는 기본적으로 제공되는 `App\Models\User` 모델의 `Illuminate\Foundation\Auth\User` 부모 클래스에서 사용 가능합니다. 사용자의 이메일 인증이 완료된 후에는 원하는 곳으로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송

사용자가 인증 이메일을 실수로 삭제하거나 찾지 못할 수도 있습니다. 이를 위해 인증 이메일을 재전송하는 라우트를 정의할 수 있습니다. [인증 알림 뷰](#the-email-verification-notice) 내에 간단한 폼 제출 버튼을 두면 이 라우트로 요청을 보낼 수 있습니다:

    use Illuminate\Http\Request;

    Route::post('/email/verification-notification', function (Request $request) {
        $request->user()->sendEmailVerificationNotification();

        return back()->with('message', 'Verification link sent!');
    })->middleware(['auth', 'throttle:6,1'])->name('verification.send');

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용하면 인증된 사용자 중에서 이메일이 인증된 사용자만 특정 라우트에 접근할 수 있게 할 수 있습니다. Laravel에는 'verified' 미들웨어가 기본 제공되며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 참조합니다. 이 미들웨어는 애플리케이션의 HTTP 커널에 이미 등록되어 있으므로, 라우트 정의에 미들웨어만 추가하면 됩니다. 일반적으로 이 미들웨어는 `auth` 미들웨어와 함께 사용합니다:

    Route::get('/profile', function () {
        // 이 라우트는 이메일이 인증된 사용자만 접근할 수 있습니다...
    })->middleware(['auth', 'verified']);

이 미들웨어가 적용된 라우트에 이메일 인증이 완료되지 않은 사용자가 접근하면 자동으로 `verification.notice` [네임드 라우트](/docs/{{version}}/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
## 커스터마이징

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징

기본 이메일 인증 알림은 대부분의 애플리케이션에 적합하지만, Laravel은 인증 이메일 메시지를 커스터마이징할 수 있는 방법을 제공합니다.

시작하려면, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드에 클로저를 전달하세요. 이 클로저는 알림을 받을 모델 인스턴스와 사용자가 이메일 인증을 위해 접속해야 하는 서명된 인증 URL을 인자로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `toMailUsing`을 호출하는 것이 좋습니다:

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
                ->subject('이메일 주소 인증')
                ->line('아래 버튼을 클릭하여 이메일 주소를 인증해주세요.')
                ->action('이메일 주소 인증하기', $url);
        });
    }

> **참고**  
> 메일 알림에 대해 더 알아보고 싶다면, [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[Laravel 스타터 키트](/docs/{{version}}/starter-kits)를 사용할 경우, Laravel은 이메일 인증 과정에서 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 직접 이메일 인증을 구현하는 경우에도 인증 완료 후 이 이벤트를 수동으로 디스패치할 수 있습니다. 애플리케이션의 `EventServiceProvider`에서 이러한 이벤트에 리스너를 연결할 수 있습니다:

    use App\Listeners\LogVerifiedUser;
    use Illuminate\Auth\Events\Verified;
    
    /**
     * 애플리케이션의 이벤트 리스너 매핑입니다.
     *
     * @var array
     */
    protected $listen = [
        Verified::class => [
            LogVerifiedUser::class,
        ],
    ];