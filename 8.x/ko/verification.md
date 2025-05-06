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

많은 웹 애플리케이션에서는 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 직접 이 기능을 구현할 필요 없이, 라라벨은 이메일 인증 요청을 전송하고 인증하는 편리한 내장 서비스를 제공합니다.

> {tip} 빠르게 시작하고 싶으신가요? 새 라라벨 애플리케이션에 [라라벨 스타터 키트](/docs/{{version}}/starter-kits)를 설치하세요. 스타터 키트에서는 전체 인증 시스템 스캐폴딩은 물론, 이메일 인증까지 자동으로 설정해줍니다.

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

이 인터페이스를 모델에 추가하면, 신규 가입자에게 이메일 인증 링크가 자동으로 포함된 이메일이 발송됩니다. 애플리케이션의 `App\Providers\EventServiceProvider`를 살펴보면, 라라벨에 이미 `Illuminate\Auth\Events\Registered` 이벤트에 연결된 `SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)가 포함되어 있는 것을 볼 수 있습니다. 이 이벤트 리스너가 사용자에게 이메일 인증 링크를 전송합니다.

[스타터 키트](/docs/{{version}}/starter-kits)를 사용하지 않고 직접 회원가입을 구현하는 경우, 회원가입이 성공한 뒤에 `Illuminate\Auth\Events\Registered` 이벤트를 꼭 발생시켜야 합니다:

    use Illuminate\Auth\Events\Registered;

    event(new Registered($user));

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, `users` 테이블에 사용자의 이메일 인증이 완료된 날짜와 시간이 저장될 수 있도록 `email_verified_at` 컬럼이 포함되어 있어야 합니다. 라라벨 프레임워크에 기본으로 포함된 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있으므로, 데이터베이스 마이그레이션만 실행하면 됩니다:

    php artisan migrate

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 올바르게 구현하려면 세 가지 라우트를 정의해야 합니다. 먼저, 사용자가 회원가입 후 라라벨이 보낸 인증 이메일의 링크를 클릭해야 함을 알리는 알림을 표시하는 라우트가 필요합니다.

둘째, 사용자가 이메일의 인증 링크를 클릭할 때 요청을 처리하는 라우트가 필요합니다.

셋째, 사용자가 인증 링크를 분실했을 경우 인증 링크를 다시 발송해주는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림

먼저, 회원가입 후 라라벨이 발송한 이메일 인증 링크를 클릭하라고 사용자에게 안내하는 화면을 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일을 인증하지 않은 상태로 애플리케이션의 다른 부분에 접근하려 할 때 표시됩니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있으면 링크는 자동으로 이메일로 전송됩니다:

    Route::get('/email/verify', function () {
        return view('auth.verify-email');
    })->middleware('auth')->name('verification.notice');

이메일 인증 알림을 반환하는 이 라우트는 반드시 `verification.notice`라는 이름으로 지정되어야 합니다. [라라벨에 기본 포함된](#protecting-routes) `verified` 미들웨어는 사용자가 이메일을 인증하지 않았다면 이 라우트 이름으로 자동 리다이렉트합니다.

> {tip} 이메일 인증을 직접 구현하는 경우, 인증 알림 화면의 내용을 직접 정의해야 합니다. 모든 인증 및 인증 뷰를 포함한 스캐폴딩을 원한다면, [라라벨 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기

다음으로, 사용자가 이메일에서 인증 링크를 클릭할 때 요청을 처리하는 라우트를 정의해야 합니다. 이 라우트의 이름은 `verification.verify`이고, `auth` 및 `signed` 미들웨어가 할당되어야 합니다:

    use Illuminate\Foundation\Auth\EmailVerificationRequest;

    Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
        $request->fulfill();

        return redirect('/home');
    })->middleware(['auth', 'signed'])->name('verification.verify');

이 라우트를 자세히 살펴봅시다. 먼저, 보통 사용하는 `Illuminate\Http\Request`가 아닌 `EmailVerificationRequest` 타입을 사용합니다. `EmailVerificationRequest`는 라라벨에 포함된 [폼 리퀘스트](/docs/{{version}}/validation#form-request-validation)로, `id`와 `hash` 파라미터의 유효성을 자동으로 검증합니다.

그 다음, 요청에서 바로 `fulfill` 메소드를 호출할 수 있습니다. 이 메소드는 인증된 사용자의 `markEmailAsVerified` 메소드를 호출해주고, `Illuminate\Auth\Events\Verified` 이벤트를 발생시킵니다. `markEmailAsVerified` 메소드는 `Illuminate\Foundation\Auth\User` 베이스 클래스를 통해 기본 `App\Models\User` 모델에서 사용할 수 있습니다. 이메일이 인증되면, 원하시는 경로로 사용자를 리다이렉트하실 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송

때때로 사용자가 이메일 인증 메일을 분실하거나 실수로 삭제할 수 있습니다. 이를 위해, 인증 이메일을 재전송할 수 있도록 라우트를 정의해 두는 것이 좋습니다. [인증 알림 뷰](#the-email-verification-notice) 안에 간단한 폼 제출 버튼을 두고, 이 라우트로 요청을 보낼 수 있습니다:

    use Illuminate\Http\Request;

    Route::post('/email/verification-notification', function (Request $request) {
        $request->user()->sendEmailVerificationNotification();

        return back()->with('message', '인증 링크가 전송되었습니다!');
    })->middleware(['auth', 'throttle:6,1'])->name('verification.send');

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/{{version}}/middleware)를 사용해 인증된 사용자에게만 특정 라우트를 접근할 수 있도록 제한할 수 있습니다. 라라벨에는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 참조하는 `verified` 미들웨어가 내장되어 있습니다. 이 미들웨어는 애플리케이션 HTTP 커널에 이미 등록되어 있으므로, 라우트 정의에 미들웨어만 추가하면 됩니다:

    Route::get('/profile', function () {
        // 인증된 사용자만 이 라우트에 접근할 수 있습니다...
    })->middleware('verified');

이 미들웨어가 할당된 라우트에 인증되지 않은 사용자가 접근하려 하면, 자동으로 [네임드 라우트](/docs/{{version}}/routing#named-routes) `verification.notice`로 리다이렉트됩니다.

<a name="customization"></a>
## 커스터마이징

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징

기본 이메일 인증 알림은 대부분의 애플리케이션 요구사항을 충족하지만, 라라벨에서는 인증 이메일 메시지의 작성 방식을 커스터마이징할 수 있습니다.

시작하려면, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메소드에 클로저를 전달하세요. 이 클로저는 알림을 받는 notifiable 모델 인스턴스와 사용자가 이메일 인증을 위해 방문해야 하는 서명된 이메일 인증 URL을 전달받습니다. 클로저에서는 반드시 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로, 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메소드 내에서 `toMailUsing`을 호출하면 됩니다:

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
                ->line('아래 버튼을 클릭하여 이메일 주소를 인증하세요.')
                ->action('이메일 주소 인증', $url);
        });
    }

> {tip} 메일 알림에 대해 더 자세히 알고 싶다면, [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[라라벨 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우, 라라벨은 이메일 인증 프로세스 중 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 애플리케이션에서 이메일 인증을 수동으로 처리하는 경우에는 인증 완료 후 해당 이벤트를 수동으로 발생시키길 원할 수 있습니다. 애플리케이션의 `EventServiceProvider`에서 이 이벤트에 리스너를 연결할 수 있습니다:

    /**
     * 애플리케이션의 이벤트 리스너 매핑입니다.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Auth\Events\Verified' => [
            'App\Listeners\LogVerifiedUser',
        ],
    ];