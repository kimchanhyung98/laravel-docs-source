# 알림(Notifications)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포매팅](#formatting-mail-messages)
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부 파일](#mail-attachments)
    - [메일러블 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포매팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포매팅](#formatting-broadcast-notifications)
    - [알림 리스닝](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포매팅](#formatting-sms-notifications)
    - [쇼트코드 알림 포매팅](#formatting-shortcode-notifications)
    - [From 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [슬랙 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [슬랙 알림 포매팅](#formatting-slack-notifications)
    - [슬랙 첨부 파일](#slack-attachments)
    - [슬랙 알림 라우팅](#routing-slack-notifications)
- [알림 현지화](#localizing-notifications)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[이메일 전송](/docs/{{version}}/mail) 지원뿐만 아니라, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/)), 슬랙([Slack](https://slack.com)) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 또한, [커뮤니티에서 개발된 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 개의 다른 채널로 알림을 보낼 수도 있습니다! 알림은 데이터베이스에 저장할 수 있어, 웹 인터페이스에서 사용자에게 노출할 수 있습니다.

일반적으로 알림은 애플리케이션에서 발생한 사건을 사용자에게 알려주는 짧고 정보성 메시지입니다. 예를 들어, 청구 애플리케이션을 작성하는 경우, 이메일 및 SMS 채널을 통해 사용자에게 "인보이스 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성

Laravel에서 각 알림은 하나의 클래스로 표현되며, 일반적으로 `app/Notifications` 디렉터리에 저장됩니다. 해당 디렉터리가 보이지 않아도 걱정하지 마세요. `make:notification` 아티즌 명령어를 실행하면 자동으로 생성됩니다.

```
php artisan make:notification InvoicePaid
```

이 명령은 `app/Notifications` 디렉터리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스에는 `via` 메서드와 `toMail`, `toDatabase` 등 각 채널에 맞는 메시지 생성 메서드가 포함되어 있습니다.

<a name="sending-notifications"></a>
## 알림 전송

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 크게 두 가지 방법으로 전송할 수 있습니다: `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, `Notification` [파사드](/docs/{{version}}/facades)를 사용하는 것입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 적용되어 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 전달받아야 합니다.

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> {tip} `Notifiable` 트레이트는 모든 모델에 사용할 수 있습니다. `User` 모델에만 국한되지 않습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또한 `Notification` [파사드](/docs/{{version}}/facades)를 사용할 수도 있습니다. 이 방식은 여러 엔티티(예: 사용자 컬렉션)에게 한 번에 알림을 보낼 때 유용합니다. 파사드의 `send` 메서드에 모든 알림 대상과 알림 인스턴스를 전달합니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 즉시 알림을 전송합니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하더라도 즉시 전송합니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

모든 알림 클래스에는 해당 알림이 어떤 채널로 전송될지 결정하는 `via` 메서드가 있습니다. 채널로는 `mail`, `database`, `broadcast`, `nexmo`, `slack` 등이 있습니다.

> {tip} Telegram, Pusher 등 추가 채널이 필요하다면 커뮤니티에서 제공하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 확인하세요.

`via` 메서드는 `$notifiable` 인스턴스를 전달받으며, 이 객체를 바탕으로 전송 채널을 결정할 수 있습니다.

```php
/**
 * 알림 전송 채널을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function via($notifiable)
{
    return $notifiable->prefers_sms ? ['nexmo'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐잉하기

> {note} 알림을 큐에 넣기 전에 큐 설정을 완료하고, [워커를 실행](/docs/{{version}}/queues)해야 합니다.

특히 외부 API 호출이 필요한 채널로 알림을 전송할 때에는 시간이 오래 걸릴 수 있습니다. 앱의 응답 속도를 빠르게 하려면 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 클래스에 추가해 알림을 큐에 맡기세요. `make:notification` 명령어로 생성된 알림에는 이미 관련 인터페이스와 트레이트가 임포트되어 있습니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```

`ShouldQueue`가 추가된 알림은 평소처럼 전송하면 Laravel이 자동으로 큐잉 시켜줍니다.

```php
$user->notify(new InvoicePaid($invoice));
```

전송을 지연하려면 알림 인스턴스에 `delay` 메서드를 체이닝하면 됩니다.

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 전송 지연 시간을 다르게 지정하려면 배열로 전달하세요.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

알림 큐잉시, 수신자와 채널 조합별로 개별 작업이 생성됩니다. 예를 들어, 3명의 수신자와 2개 채널이면 6개의 작업이 생성됩니다.

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 연결 커스터마이징

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림에 다른 연결을 사용하고 싶다면 알림 클래스에 `$connection` 속성을 정의하세요.

```php
/**
 * 알림 큐에 사용할 큐 연결 이름
 *
 * @var string
 */
public $connection = 'redis';
```

<a name="customizing-notification-channel-queues"></a>
#### 알림 채널별 큐 커스터마이징

알림이 지원하는 각 채널별로 사용될 큐를 지정할 수 있습니다. 알림 클래스에 `viaQueues` 메서드를 정의해 채널명/큐명 쌍 배열을 반환하세요.

```php
public function viaQueues()
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 큐잉된 알림과 데이터베이스 트랜잭션

큐잉된 알림이 데이터베이스 트랜잭션 중에 dispatch될 경우, 큐 워커에서 알림이 DB 트랜잭션이 커밋되기 전에 처리될 수 있습니다. 이럴 경우, DB 트랜잭션 중 변경된 모델이나 레코드가 아직 DB에 반영되지 않았거나 생성된 모델이 DB에 없을 수 있습니다. 알림이 이런 모델에 의존한다면 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`라도, 알림 전송 시 `afterCommit` 메서드를 호출하면 모든 DB 트랜잭션 커밋 후에 dispatch되게 할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스의 생성자에서 `afterCommit`을 호출할 수도 있습니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> {tip} 이러한 이슈에 대해 더 알아보려면 [큐잉 작업과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 전송 여부 결정

큐에 직렬화된 알림은 백그라운드에서 워커에 의해 처리 및 전송됩니다.

하지만 큐에서 워커가 작업을 처리하면서 해당 알림을 실제로 보낼지 여부를 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. `false`를 반환하면 알림이 전송되지 않습니다.

```php
public function shouldSend($notifiable, $channel)
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림

애플리케이션의 "사용자"로 저장되어 있지 않은 사람에게도 알림을 보내야 할 때가 있습니다. `Notification` 파사드의 `route` 메서드를 사용하여 임의 라우팅 정보를 지정하여 알림을 전송할 수 있습니다.

```php
Notification::route('mail', 'taylor@example.com')
            ->route('nexmo', '5555555555')
            ->route('slack', 'https://hooks.slack.com/services/...')
            ->notify(new InvoicePaid($invoice));
```

메일로 온디맨드 알림을 보낼 때 수신자의 이름을 제공하려면, 배열을 사용하여 이메일 주소를 키, 값을 이름으로 지정하면 됩니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 포매팅

알림이 이메일로 전송될 수 있다면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 전달받고 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 간단하게 트랜잭션 이메일 메시지를 작성할 수 있도록 여러 메서드를 제공합니다. 메시지는 텍스트 라인과 콜 투 액션(CTA, 버튼 등)을 포함할 수 있습니다. 예시를 살펴보세요.

```php
public function toMail($notifiable)
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
                ->greeting('Hello!')
                ->line('One of your invoices has been paid!')
                ->action('View Invoice', $url)
                ->line('Thank you for using our application!');
}
```

> {tip} `toMail` 메서드에서 `$this->invoice->id`와 같이 데이터를 사용할 수 있습니다. 메시지 생성을 위해 필요한 데이터는 생성자에 전달하세요.

이 예제에서는 인사말, 메시지 라인, 콜 투 액션, 그 다음 또 다른 메시지 라인을 등록했습니다. `MailMessage` 객체가 제공하는 메서드로 간단 명료한 트랜잭션 이메일을 빠르게 포매팅할 수 있습니다. 메일 채널은 메시지 구성 요소를 아름답고 반응형인 HTML 이메일 템플릿(및 텍스트 버전)으로 변환합니다. 다음은 `mail` 채널에서 생성한 이메일 예시입니다.

<img src="https://laravel.com/img/docs/notification-example-2.png">

> {tip} 메일 알림을 전송할 때, `config/app.php`의 `name` 옵션이 설정되어 있는지 확인하세요. 이 값은 메일 알림의 헤더와 푸터에 사용됩니다.

<a name="other-mail-notification-formatting-options"></a>
#### 기타 메일 알림 포매팅 옵션

알림 클래스에서 텍스트 라인을 정의하는 대신, `view` 메서드를 이용해 직접 작성한 템플릿을 사용할 수도 있습니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)->view(
        'emails.name', ['invoice' => $this->invoice]
    );
}
```

메일 메시지를 위한 일반 텍스트 뷰를 사용하려면 배열의 두 번째 요소로 뷰 이름을 전달하세요.

```php
public function toMail($notifiable)
{
    return (new MailMessage)->view(
        ['emails.name.html', 'emails.name.plain'],
        ['invoice' => $this->invoice]
    );
}
```

<a name="error-messages"></a>
#### 오류 메시지

일부 알림은 실패한 인보이스 결제처럼 오류 정보를 사용자에게 알리기도 합니다. 메시지 작성 시 `error` 메서드를 호출하여 오류 메일임을 표시할 수 있습니다. 이 경우 콜 투 액션 버튼 색상이 빨간색으로 변경됩니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->error()
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-sender"></a>
### 발신자 커스터마이징

기본적으로 이메일의 발신자(From) 주소는 `config/mail.php`에서 지정합니다. 하지만 특정 알림에 대해 발신자 주소를 바꿀 수 있습니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->from('barrett@example.com', 'Barrett Blair')
                ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 커스터마이징

메일 채널로 알림 전송 시, 시스템은 자동으로 대상 엔티티의 `email` 속성을 찾습니다. 사용할 이메일 주소를 직접 지정하려면 노티파이어블(예: User) 엔티티에 `routeNotificationForMail` 메서드를 추가하세요.

```php
public function routeNotificationForMail($notification)
{
    // 이메일 주소만 반환
    return $this->email_address;

    // 이메일 주소와 이름 반환
    return [$this->email_address => $this->name];
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 이메일의 제목은 알림 클래스명을 "타이틀 케이스"로 변환하여 사용합니다. 예를 들어, 클래스명이 `InvoicePaid`라면 제목은 `Invoice Paid`가 됩니다. 원하는 제목을 직접 지정하려면 `subject` 메서드를 사용하세요.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 커스터마이징

메일 알림은 기본적으로 `config/mail.php`에 지정된 기본 메일러로 발송됩니다. 하지만 `mailer` 메서드를 통해 런타임에 메일러를 변경할 수 있습니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->mailer('postmark')
                ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 커스터마이징

메일 알림에 사용되는 HTML 및 텍스트 템플릿을 수정하려면 패키지 리소스를 퍼블리시하세요. 다음 명령어를 실행하면 템플릿이 `resources/views/vendor/notifications`에 복사됩니다.

```
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부 파일

메일 알림에 첨부 파일을 추가하려면, 메시지 빌더에서 `attach` 메서드를 사용하세요. 첫 번째 인자로 파일의 절대 경로를 전달합니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file');
}
```

파일 첨부 시, 두 번째 인자로 표시 이름과 MIME 타입을 배열로 전달할 수도 있습니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file', [
                    'as' => 'name.pdf',
                    'mime' => 'application/pdf',
                ]);
}
```

메일러블 객체에서처럼 `attachFromStorage`로 직접 저장소의 파일을 첨부할 순 없습니다. 대신 `attach`에 저장소의 절대 경로를 전달하세요. 또는 [메일러블](/docs/{{version}}/mail#generating-mailables)을 `toMail`에서 반환할 수도 있습니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

public function toMail($notifiable)
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email)
                ->attachFromStorage('/path/to/file');
}
```

<a name="raw-data-attachments"></a>
#### 원시 데이터 첨부

`attachData` 메서드를 사용하면 바이트 문자열을 첨부로 추가할 수 있습니다. 파일 이름과 옵션을 함께 제공합니다.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attachData($this->pdf, 'name.pdf', [
                    'mime' => 'application/pdf',
                ]);
}
```

<a name="using-mailables"></a>
### 메일러블(mailable) 사용

필요하다면 알림의 `toMail` 메서드에서 전체 [메일러블 객체](/docs/{{version}}/mail)를 반환할 수도 있습니다. 이 경우, 메일러블의 `to` 메서드로 수신자를 지정해야 합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

public function toMail($notifiable)
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### 메일러블 & 온디맨드 알림

[온디맨드 알림](#on-demand-notifications)을 전송할 때, `toMail`의 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable` 타입이 되며, `routeNotificationFor` 메서드로 이메일 주소를 얻을 수 있습니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;

public function toMail($notifiable)
{
    $address = $notifiable instanceof AnonymousNotifiable
            ? $notifiable->routeNotificationFor('mail')
            : $notifiable->email;

    return (new InvoicePaidMailable($this->invoice))
                ->to($address);
}
```

<a name="previewing-mail-notifications"></a>
### 메일 알림 미리보기

알림 템플릿을 디자인할 때 실제로 메일을 보내지 않고 바로 브라우저에서 결과를 미리보면 매우 편리합니다. 라우트 클로저 또는 컨트롤러에서 알림의 메일 메시지를 직접 반환하면 Blade처럼 브라우저에서 바로 볼 수 있습니다.

```php
use App\Models\Invoice;
use App\Notifications\InvoicePaid;

Route::get('/notification', function () {
    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))
                ->toMail($invoice->user);
});
```

<a name="markdown-mail-notifications"></a>
## 마크다운 메일 알림

마크다운 메일 알림은 미리 빌드된 템플릿의 장점을 그대로 살리면서, 더 길고 커스터마이즈된 메시지도 쉽게 작성할 수 있게 해줍니다. 메시지가 마크다운으로 작성되어 HTML 템플릿과 일반 텍스트 버전이 모두 자동으로 생성됩니다.

<a name="generating-the-message"></a>
### 메시지 생성

마크다운 템플릿을 사용하는 알림을 생성하려면, `make:notification` 아티즌 명령어에 `--markdown` 옵션을 추가하세요.

```
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 메일 알림과 같이, 마크다운 템플릿을 사용하는 알림도 `toMail` 메서드를 정의해야 합니다. 하지만, 메시지 구성 시 `line`이나 `action`이 아닌 `markdown` 메서드로 사용 템플릿 이름을 전달하세요. 두 번째 인자로 템플릿에 사용할 데이터를 배열로 넘길 수 있습니다.

```php
public function toMail($notifiable)
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="writing-the-message"></a>
### 메시지 작성

마크다운 메일 알림은 블레이드 컴포넌트와 마크다운 문법을 조합해서 손쉽게 커스텀 알림을 만들 수 있습니다.

```blade
@component('mail::message')
# Invoice Paid

Your invoice has been paid!

@component('mail::button', ['url' => $url])
View Invoice
@endcomponent

Thanks,<br>
{{ config('app.name') }}
@endcomponent
```

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 링크 버튼을 렌더링합니다. `url`, 그리고 선택적으로 `color` 인자를 받으며, 색상은 `primary`, `green`, `red`가 지원됩니다. 원하는 만큼 버튼 추가가 가능합니다.

```blade
@component('mail::button', ['url' => $url, 'color' => 'green'])
View Invoice
@endcomponent
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 배경색이 다른 패널로 렌더링합니다. 특정 부분을 강조할 때 활용하세요.

```blade
@component('mail::panel')
This is the panel content.
@endcomponent
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환합니다. 컬럼 정렬 역시 마크다운 문법을 그대로 지원합니다.

```blade
@component('mail::table')
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
@endcomponent
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

모든 마크다운 알림 컴포넌트를 퍼블리시해 직접 커스터마이징할 수 있습니다. 다음 명령어로 `laravel-mail` 에셋을 퍼블리시하세요.

```
php artisan vendor:publish --tag=laravel-mail
```

퍼블리시 후, `resources/views/vendor/mail` 디렉터리의 `html`, `text` 폴더에서 마크다운 메일의 각 컴포넌트 뷰를 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 퍼블리시하면, `resources/views/vendor/mail/html/themes/default.css`에서 스타일을 수정할 수 있고, 이 CSS는 자동으로 알림 HTML 본문에 인라인되어 적용됩니다.

마크다운 전용 테마를 새로 만들고 싶다면 이 폴더에 CSS 파일을 추가하고, `mail` 설정 파일의 `theme` 옵션에 테마명을 지정하세요.

개별 알림에만 특정 테마를 적용하고 싶을 땐, 알림 메시지 생성 시 `theme` 메서드로 테마명을 지정하세요.

```php
public function toMail($notifiable)
{
    return (new MailMessage)
                ->theme('invoice')
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="database-notifications"></a>
## 데이터베이스 알림

<a name="database-prerequisites"></a>
### 사전 준비

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 타입 및 알림을 설명하는 JSON 데이터가 저장됩니다.

해당 테이블을 쿼리해서 사용자 인터페이스에 알림을 표시할 수 있습니다. 알림을 저장할 테이블을 만드려면 `notifications:table` 명령어로 마이그레이션을 생성하세요.

```
php artisan notifications:table

php artisan migrate
```

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포매팅

알림을 DB에 저장하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받고, 평범한 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 예시:

```php
public function toArray($notifiable)
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs `toArray`

`toArray`는 `broadcast` 채널에서도 데이터 전송에 사용됩니다. `database`와 `broadcast`에 대해 각각 다른 데이터 구조를 원한다면, `toDatabase` 메서드를 따로 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근

데이터베이스에 저장된 알림은 notifiable 엔티티에서 쉽게 접근할 수 있습니다. `Illuminate\Notifications\Notifiable` 트레이트는 `notifications` [Eloquent 관계](/docs/{{version}}/eloquent-relationships)를 제공합니다. 이를 통해 알림을 조회할 수 있습니다. 최신 알림이 먼저 나오도록 `created_at` 으로 정렬됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않음" 알림만 가져오려면 `unreadNotifications` 관계를 이용하세요.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> {tip} 자바스크립트에서 알림을 접근하려면, 현재 사용자 등 notifiable 엔티티의 알림을 반환하는 컨트롤러를 만들어 HTTP 요청을 보내세요.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리

일반적으로 사용자가 알림을 확인할 때 "읽음" 처리해야 합니다. `Illuminate\Notifications\Notifiable` 트레이트의 `markAsRead` 메서드는 해당 알림의 `read_at` 값을 업데이트합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

각 알림을 반복하지 않고, 알림 컬렉션에서 바로 사용할 수도 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

또는 대량 업데이트 쿼리로 DB 접근 없이 모두 읽음 처리할 수 있습니다.

```php
$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 모두 삭제하려면 다음과 같이 하세요.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하기 전에, Laravel의 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 서비스를 설정하고 숙지해야 합니다. 이 서비스는 서버 측 이벤트를 자바스크립트 프론트엔드에서 실시간으로 수신할 수 있게 해줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포매팅

`broadcast` 채널은 이벤트 브로드캐스팅을 이용해 알림을 자바스크립트 프런트엔드로 전달합니다. 알림이 브로드캐스트를 지원한다면, 알림 클래스에 `toBroadcast` 메서드를 정의하고, 이 메서드는 `$notifiable`을 받아 `BroadcastMessage` 인스턴스를 반환해야 합니다. 없다면 `toArray` 결과를 사용합니다.

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

public function toBroadcast($notifiable)
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```

<a name="broadcast-queue-configuration"></a>
#### 브로드캐스트 큐 설정

모든 브로드캐스트 알림은 큐잉됩니다. 연결/큐 이름 조정이 필요하면 `onConnection`과 `onQueue` 메서드를 사용하세요.

```php
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

브로드캐스트 알림에는 클래스명으로 type 필드가 추가됩니다. 이 값을 직접 지정하려면 알림 클래스에서 `broadcastType` 메서드를 정의하세요.

```php
public function broadcastType()
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 리스닝

알림은 `{notifiable}.{id}` 포맷의 프라이빗 채널로 브로드캐스트됩니다. 예컨대 `App\Models\User` 모델 1번이라면 `App.Models.User.1` 채널입니다. [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) 를 사용하면 다음과 같이 리슨할 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이즈

특정 엔티티가 리슨할 알림 채널을 직접 지정하려면 모델에 `receivesBroadcastNotificationsOn` 메서드를 정의하세요.

```php
public function receivesBroadcastNotificationsOn()
{
    return 'users.'.$this->id;
}
```

<a name="sms-notifications"></a>
## SMS 알림

<a name="sms-prerequisites"></a>
### 사전 준비

Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/) (구 Nexmo)를 사용합니다. 보내려면 `laravel/nexmo-notification-channel`과 `nexmo/laravel` 패키지를 설치하세요.

```
composer require laravel/nexmo-notification-channel nexmo/laravel
```

`nexmo/laravel`은 [설정 파일](https://github.com/Nexmo/nexmo-laravel/blob/master/config/nexmo.php)을 제공하지만, 꼭 퍼블리시할 필요는 없습니다. 환경변수로 `NEXMO_KEY`, `NEXMO_SECRET`만 등록해도 됩니다.

이어, `config/services.php`에 nexmo 설정을 추가합니다.

```php
'nexmo' => [
    'sms_from' => '15556666666',
],
```

`sms_from` 옵션은 Vonage 콘솔에서 발급받은 발신 전화번호로 설정하세요.

<a name="formatting-sms-notifications"></a>
### SMS 알림 포매팅

SMS로 알림을 전송하려면, 알림 클래스에 `toNexmo` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable`을 받아 `Illuminate\Notifications\Messages\NexmoMessage`를 반환해야 합니다.

```php
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 내용

SMS 메시지가 유니코드 문자를 포함할 경우, `unicode` 메서드를 호출해야 합니다.

```php
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your unicode message')
                ->unicode();
}
```

<a name="formatting-shortcode-notifications"></a>
### 쇼트코드 알림 포매팅

Vonage 계정의 쇼트코드(미리 지정된 템플릿)로도 메시지를 보낼 수 있습니다. 알림 클래스에 `toShortcode` 메서드를 정의하세요.

```php
public function toShortcode($notifiable)
{
    return [
        'type' => 'alert',
        'custom' => [
            'code' => 'ABC123',
        ],
    ];
}
```

> {tip} [SMS 알림 라우팅](#routing-sms-notifications)과 마찬가지로, notifiable 모델에 `routeNotificationForShortcode`를 구현해야 합니다.

<a name="customizing-the-from-number"></a>
### From 번호 커스터마이징

특정 알림만 다른 전화번호로 발송하고 싶다면, `NexmoMessage` 인스턴스에서 `from` 메서드를 이용하세요.

```php
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your SMS message content')
                ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가

사용자, 팀, 고객별로 비용을 추적하려면 "클라이언트 참조"를 추가할 수 있습니다. 이 값은 길이 40자 이하의 문자열이며, Vonage 리포트에서 사용됩니다.

```php
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

올바른 번호로 Vonage 알림을 보내려면 notifiable 엔티티에 `routeNotificationForNexmo` 메서드를 정의하세요.

```php
public function routeNotificationForNexmo($notification)
{
    return $this->phone_number;
}
```

<a name="slack-notifications"></a>
## 슬랙 알림

<a name="slack-prerequisites"></a>
### 사전 준비

슬랙 알림을 보내려면 Composer로 슬랙 채널 패키지를 먼저 설치해야 합니다.

```
composer require laravel/slack-notification-channel
```

슬랙팀용 [Slack App](https://api.slack.com/apps?new_app=1)을 생성하고, 워크스페이스에 "Incoming Webhook"을 설정하세요. 슬랙에서 제공하는 웹훅 URL을 [슬랙 알림 라우팅](#routing-slack-notifications)에 사용하세요.

<a name="formatting-slack-notifications"></a>
### 슬랙 알림 포매팅

슬랙 메시지 전송을 지원하려면 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. `$notifiable`을 받아 `Illuminate\Notifications\Messages\SlackMessage` 인스턴스를 반환합니다. 슬랙 메시지는 텍스트와 첨부(attachment, 필드 포함)를 가질 수 있습니다. 기본 예시는 다음과 같습니다.

```php
public function toSlack($notifiable)
{
    return (new SlackMessage)
                ->content('One of your invoices has been paid!');
}
```

<a name="slack-attachments"></a>
### 슬랙 첨부 파일

슬랙 메시지에 "첨부"를 추가해 더 풍부한 포매팅을 사용할 수 있습니다. 예를 들어, 예외 알림 메시지를 URL과 함께 보낼 수 있습니다.

```php
public function toSlack($notifiable)
{
    $url = url('/exceptions/'.$this->exception->id);

    return (new SlackMessage)
                ->error()
                ->content('Whoops! Something went wrong.')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Exception: File Not Found', $url)
                               ->content('File [background.jpg] was not found.');
                });
}
```

첨부에서 데이터를 배열로 지정해도 되며, 자동으로 테이블 형태로 보여줍니다.

```php
public function toSlack($notifiable)
{
    $url = url('/invoices/'.$this->invoice->id);

    return (new SlackMessage)
                ->success()
                ->content('One of your invoices has been paid!')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Invoice 1322', $url)
                               ->fields([
                                    'Title' => 'Server Expenses',
                                    'Amount' => '$1,234',
                                    'Via' => 'American Express',
                                    'Was Overdue' => ':-1:',
                                ]);
                });
}
```

<a name="markdown-attachment-content"></a>
#### 마크다운 첨부 내용

필드 내에 마크다운이 포함되어 있다면 `markdown` 메서드로 슬랙에 포매팅 필드를 알려줄 수 있습니다. 허용되는 값은 `pretext`, `text`, `fields` 등이며, 자세한 내용은 [Slack API 문서](https://api.slack.com/docs/message-formatting#message_formatting)를 참고하세요.

```php
public function toSlack($notifiable)
{
    $url = url('/exceptions/'.$this->exception->id);

    return (new SlackMessage)
                ->error()
                ->content('Whoops! Something went wrong.')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Exception: File Not Found', $url)
                               ->content('File [background.jpg] was *not found*.')
                               ->markdown(['text']);
                });
}
```

<a name="routing-slack-notifications"></a>
### 슬랙 알림 라우팅

올바른 슬랙 팀과 채널로 알림을 보내려면 notifiable 엔티티에 `routeNotificationForSlack` 메서드를 정의하세요. 이 메서드는 전달할 웹훅 URL을 반환해야 합니다.

```php
public function routeNotificationForSlack($notification)
{
    return 'https://hooks.slack.com/services/...';
}
```

<a name="localizing-notifications"></a>
## 알림 현지화

Laravel은 HTTP 요청에서 사용하는 기본 로케일과 무관하게, 별도의 로케일로 알림을 보낼 수 있습니다. 또한 알림이 큐잉될 때도 이 로케일 정보를 기억합니다.

`Illuminate\Notifications\Notification` 클래스의 `locale` 메서드를 이용해 원하는 언어코드를 지정할 수 있습니다. 알림 처리 시 지정한 로케일로 변경 후, 평가가 끝나면 다시 이전 로케일로 돌아옵니다.

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 notifiable 엔티티에 대해 `Notification` 파사드로도 현지화할 수 있습니다.

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

애플리케이션에서 사용자별 선호 로케일을 저장할 때가 있습니다. notifiable 모델에서 `HasLocalePreference` 계약을 구현하면, 이 로케일이 알림 전송에 자동 사용됩니다.

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    public function preferredLocale()
    {
        return $this->locale;
    }
}
```

인터페이스 구현 시, 알림 전송 및 메일러블에 자동으로 선호 로케일이 반영되므로 별도 `locale` 메서드 호출이 필요하지 않습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="notification-events"></a>
## 알림 이벤트

<a name="notification-sending-event"></a>
#### 알림 전송 중 이벤트

알림이 전송되면 `Illuminate\Notifications\Events\NotificationSending` [이벤트](/docs/{{version}}/events)가 디스패치됩니다. 여기에는 notifiable 엔티티와 알림 인스턴스가 포함됩니다. `EventServiceProvider`에서 리스너를 등록할 수 있습니다.

```php
protected $listen = [
    'Illuminate\Notifications\Events\NotificationSending' => [
        'App\Listeners\CheckNotificationStatus',
    ],
];
```

리스너의 `handle` 메서드가 `false`를 반환하면, 알림은 전송되지 않습니다.

```php
use Illuminate\Notifications\Events\NotificationSending;

public function handle(NotificationSending $event)
{
    return false;
}
```

이벤트 리스너 안에서는 `notifiable`, `notification`, `channel` 속성을 통해 수신자와 알림 정보에 접근할 수 있습니다.

```php
public function handle(NotificationSending $event)
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
#### 알림 전송 완료 이벤트

알림이 전송된 후에는 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/{{version}}/events)가 디스패치됩니다. 이 이벤트 역시 notifiable, notification 인스턴스를 가집니다. `EventServiceProvider`에서 리스너를 등록하세요.

```php
protected $listen = [
    'Illuminate\Notifications\Events\NotificationSent' => [
        'App\Listeners\LogNotification',
    ],
];
```

> {tip} 리스너를 등록한 후, `event:generate` 아티즌 명령으로 빠르게 리스너 클래스를 생성할 수 있습니다.

리스너에서 `notifiable`, `notification`, `channel`, `response`에 접근해 더 많은 정보를 알 수 있습니다.

```php
public function handle(NotificationSent $event)
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```

<a name="custom-channels"></a>
## 커스텀 채널

Laravel은 여러 내장 알림 채널을 제공하지만, 자체 드라이버를 만들어 다른 채널로도 알림을 보낼 수 있습니다. 새 클래스에 `send` 메서드를 정의하면 됩니다. 이 메서드는 `$notifiable`, `$notification` 두 인자를 받습니다.

`send` 메서드 내에서 알림 인스턴스를 사용해 채널에 맞는 메시지를 만들고, 원하는 방식으로 `$notifiable`에게 보냅니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    public function send($notifiable, Notification $notification)
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable에게 알림 전송...
    }
}
```

이제 알림 클래스의 `via` 메서드에서 커스텀 채널 클래스명을 반환하면, 해당 채널로 알림이 전송됩니다. 예를 들어, 알림의 `toVoice`는 메시지 표현 객체를 반환할 수 있습니다.

```php
<?php

namespace App\Notifications;

use App\Notifications\Messages\VoiceMessage;
use App\Notifications\VoiceChannel;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification
{
    use Queueable;

    public function via($notifiable)
    {
        return [VoiceChannel::class];
    }

    public function toVoice($notifiable)
    {
        // ... 메시지 반환
    }
}
```