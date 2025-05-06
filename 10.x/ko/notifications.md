# 알림(Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉(Queueing)하기](#queueing-notifications)
    - [온디맨드(즉시 지정) 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러(Mailer) 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그/메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [DB 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [DB 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 라우팅](#routing-slack-notifications)
    - [외부 Workspace 알림](#notifying-external-slack-workspaces)
- [알림 지역화(로컬라이징)](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[email 전송](/docs/{{version}}/mail) 외에도, Laravel은 email, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 Nexmo), [Slack](https://slack.com) 등 다양한 전달 채널을 통한 알림 전송을 지원합니다. 또한, [커뮤니티가 제작한 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 많으니, 다양한 채널로 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 일을 사용자에게 알리는 짧은 정보성 메시지여야 합니다. 예를 들어, 결제 애플리케이션을 작성 중이라면, 사용자가 결제 성공 시 "청구서 결제 완료" 알림을 이메일 및 SMS 채널로 전송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 보통 `app/Notifications` 디렉터리에 저장되는 하나의 클래스로 표현됩니다. 이 디렉터리가 보이지 않아도 걱정하지 마세요. 아래와 같이 `make:notification` Artisan 명령을 실행하면 자동으로 생성됩니다.

```shell
php artisan make:notification InvoicePaid
```

이 명령은 `app/Notifications` 디렉터리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스에는 `via` 메서드와 채널별 메시지 빌더 메서드(`toMail`, `toDatabase` 등)가 포함되어 해당 채널에 맞는 메시지로 변환해줍니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 두 가지 방식으로 보낼 수 있습니다: 모델의 `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, [Notification 파사드](/docs/{{version}}/facades)를 사용하는 방법입니다. 기본적으로 `App\Models\User` 모델에는 `Notifiable` 트레이트가 포함되어 있습니다:

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

트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 받아서 사용합니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]  
> `Notifiable` 트레이트는 모든 모델에 사용할 수 있으며, 반드시 `User` 모델에만 제한되는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는 [Notification 파사드](/docs/{{version}}/facades)를 사용하여 알림을 보낼 수 있습니다. 컬렉션 등 복수의 엔티티에 알림을 보내야 할 때 유용합니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면, `ShouldQueue` 인터페이스를 구현해도 즉시 알림을 전송할 수 있습니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

모든 알림 클래스는 어느 채널로 전달할 것인지 결정하는 `via` 메서드를 가지고 있습니다. Laravel의 기본 채널은 `mail`, `database`, `broadcast`, `vonage`, `slack`가 있습니다.

> [!NOTE]  
> 텔레그램, Pusher 등의 다른 채널을 쓰고 싶다면 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 받아, 그에 맞는 채널을 결정할 수 있습니다.

```php
/**
 * Get the notification's delivery channels.
 *
 * @return array<int, string>
 */
public function via(object $notifiable): array
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐잉(Queueing)하기

> [!WARNING]  
> 알림 큐잉 전에 큐 설정을 완료하고 [큐 워커를 실행](/docs/{{version}}/queues#running-the-queue-worker)해야 합니다.

알림 채널이 외부 API 호출이 필요하다면 전송에 시간이 걸릴 수 있습니다. 응답 속도를 높이려면 `ShouldQueue` 인터페이스 및 `Queueable` 트레이트를 클래스에 추가하여 알림을 큐로 보낼 수 있습니다. `make:notification` 명령을 사용하면 이미 필요한 인터페이스와 트레이트가 포함되어 있으니 바로 추가하면 됩니다.

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

`ShouldQueue` 인터페이스가 추가된 후에는 평소처럼 알림을 전송하면 됩니다. Laravel이 자동으로 큐에 넣어줍니다.

```php
$user->notify(new InvoicePaid($invoice));
```

큐잉 시, 수신자와 채널 조합별로 하나씩 잡이 생성됩니다. 예를 들어, 수신자 3명, 채널 2개면 6개의 잡이 만들어집니다.

<a name="delaying-notifications"></a>
#### 알림 지연 전송(Delay)

알림 전송을 지연시키고 싶다면 알림 인스턴스에 `delay` 메서드를 체이닝하세요.

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

<a name="delaying-notifications-per-channel"></a>
#### 채널별로 지연 전송

`delay` 메서드에 배열을 넘겨서, 채널별로 서로 다른 지연값을 줄 수 있습니다.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스에 `withDelay` 메서드를 정의해도 됩니다.

```php
/**
 * Determine the notification's delivery delay.
 *
 * @return array<string, \Illuminate\Support\Carbon>
 */
public function withDelay(object $notifiable): array
{
    return [
        'mail' => now()->addMinutes(5),
        'sms' => now()->addMinutes(10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 연결 커스터마이징

큐잉된 알림은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림에 다른 연결을 사용하려면 생성자 안에서 `onConnection` 메서드를 호출하세요.

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
        $this->onConnection('redis');
    }
}
```

또는 채널별로 큐 연결을 지정하려면 `viaConnections` 메서드를 정의하면 됩니다.

```php
/**
 * Determine which connections should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaConnections(): array
{
    return [
        'mail' => 'redis',
        'database' => 'sync',
    ];
}
```

<a name="customizing-notification-channel-queues"></a>
#### 채널별 큐 지정

채널별로 사용할 큐를 지정하려면 `viaQueues` 메서드를 사용하세요.

```php
/**
 * Determine which queues should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaQueues(): array
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 큐잉 알림과 DB 트랜잭션

트랜잭션 내에서 큐잉된 알림을 디스패치하면, 트랜잭션이 커밋되기 전에 큐 워커가 잡을 처리할 수 있습니다. 이 경우 모델이나 데이터베이스 레코드의 변경사항이 아직 반영되지 않았을 수 있습니다. 큐 연결의 `after_commit` 옵션이 `false`여도 알림 전송시 `afterCommit` 메서드를 호출하여 모든 트랜잭션이 커밋된 후 알림을 디스패치할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

생성자에 `afterCommit`을 넣을 수도 있습니다.

```php
public function __construct()
{
    $this->afterCommit();
}
```

> [!NOTE]
> 이 문제를 우회하는 방법은 [큐 잡과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림의 발송 여부 결정

큐에 보낸 후, 실제로 알림을 보낼지 최종 판단이 필요하다면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. `false`를 반환하면 해당 알림은 전송되지 않습니다.

```php
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드(즉시 지정) 알림

애플리케이션 내 "user"가 아닌 임의의 대상에게 알림을 보내려면, Notification 파사드의 `route` 메서드로 즉석 라우팅 정보를 지정할 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
            ->route('vonage', '5555555555')
            ->route('slack', '#slack-channel')
            ->route('broadcast', [new Channel('channel-name')])
            ->notify(new InvoicePaid($invoice));
```

메일 라우트에 수신자 이름을 함께 제공하려면 아래처럼 배열의 키에 이메일, 값에 이름을 넣으면 됩니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널을 동시에 지정하려면 `routes` 메서드를 사용하세요.

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅

알림이 이메일로 전송되려면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 객체를 받고, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스에는 트랜잭션 이메일 메시지 빌드에 도움이 되는 간단한 메서드들이 있습니다. 아래는 `toMail` 예시입니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
                ->greeting('Hello!')
                ->line('One of your invoices has been paid!')
                ->lineIf($this->amount > 0, "Amount paid: {$this->amount}")
                ->action('View Invoice', $url)
                ->line('Thank you for using our application!');
}
```

> [!NOTE]
> 알림의 메시지 작성을 위해 필요한 데이터는 생성자를 통해 전달할 수 있습니다.

위 예시에서는 인사말, 한 줄 텍스트, 액션(버튼), 또 한 줄 텍스트를 추가합니다. 이처럼 `MailMessage` 객체의 메서드로 트랜잭션 이메일을 쉽게 구성할 수 있습니다. 메일 채널은 메일 컴포넌트들을 보기 좋은 반응형 HTML 템플릿과 plain-text로 변환하여 전송합니다.

> [!NOTE]
> 메일 알림을 사용할 때, `config/app.php`의 `name` 옵션을 반드시 지정하세요. 해당 값이 메일 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

사용자에게 결제 실패 같은 에러 알림을 전송할 경우, `error` 메서드를 사용해 메시지가 에러임을 표시할 수 있습니다. 이 때 액션 버튼 색상이 빨간색으로 바뀝니다.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->error()
                ->subject('Invoice Payment Failed')
                ->line('...');
}
```

<a name="other-mail-notification-formatting-options"></a>
#### 기타 메일 포맷 옵션

알림 클래스에서 텍스트 라인을 직접 정의하는 대신, `view` 메서드로 이메일 렌더링에 사용할 커스텀 뷰를 지정할 수 있습니다.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

plain-text 뷰를 지정하려면, 배열 형식으로 전달하세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

또는 메시지에 plain-text만 사용할 경우 `text` 메서드를 활용할 수 있습니다.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자 커스터마이징

이메일의 발신 주소/이름은 기본적으로 `config/mail.php`에서 정의됩니다. 특정 알림에 대해서는 `from` 메서드로 직접 지정할 수 있습니다.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->from('barrett@example.com', 'Barrett Blair')
                ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 커스터마이징

기본적으로 `mail` 채널은 notifiable 엔티티의 `email` 속성을 찾습니다. 전송에 사용할 이메일을 커스터마이징하려면 notifiable 엔티티에 `routeNotificationForMail` 메서드를 정의할 수 있습니다.

```php
public function routeNotificationForMail(Notification $notification): array|string
{
    // 이메일 주소만 반환
    return $this->email_address;

    // 이메일 주소와 이름 반환
    return [$this->email_address => $this->name];
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 이메일 제목은 알림 클래스의 이름을 "Title Case"로 변환한 값입니다(`InvoicePaid` → `Invoice Paid`). 원하는 제목이 있다면 `subject` 메서드를 사용하세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러(Mailer) 커스터마이징

기본적으로 메일 알림은 `config/mail.php`의 기본 메일러로 전송됩니다. 상황에 따라 `mailer` 메서드로 별도의 메일러를 지정할 수 있습니다.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->mailer('postmark')
                ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 커스터마이징

메일 알림에서 사용하는 HTML/텍스트 템플릿을 커스터마이징하려면, 패키지 리소스를 퍼블리시하세요.

```shell
php artisan vendor:publish --tag=laravel-notifications
```

이 명령 실행 후 `resources/views/vendor/notifications` 디렉터리에 템플릿이 복사됩니다.

<a name="mail-attachments"></a>
### 첨부파일

메일 메시지에 첨부파일을 추가하려면 `attach` 메서드를 사용하세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file');
}
```

> [!NOTE]
> 알림 메일 메시지의 `attach` 메서드는 [attachable 객체](/docs/{{version}}/mail#attachable-objects) 사용도 지원합니다.

파일의 표시 이름이나 MIME 타입을 지정하려면 두 번째 인자로 배열을 넘기세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file', [
                    'as' => 'name.pdf',
                    'mime' => 'application/pdf',
                ]);
}
```

Mailable 객체와 달리 `attachFromStorage`는 직접 사용할 수 없으니, 스토리지 디스크 파일의 절대경로를 `attach`로 전달하세요. 아니면 `toMail`에서 [mailable](/docs/{{version}}/mail#generating-mailables)를 반환할 수도 있습니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email)
                ->attachFromStorage('/path/to/file');
}
```

여러 개 파일을 첨부할 때는 `attachMany`를 사용하세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attachMany([
                    '/path/to/forge.svg',
                    '/path/to/vapor.svg' => [
                        'as' => 'Logo.svg',
                        'mime' => 'image/svg+xml',
                    ],
                ]);
}
```

<a name="raw-data-attachments"></a>
#### Raw 데이터 첨부

`attachData` 메서드는 바이트 데이터(String)를 첨부파일로 추가합니다. 첨부파일의 파일명을 인자로 전달하세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attachData($this->pdf, 'name.pdf', [
                    'mime' => 'application/pdf',
                ]);
}
```

<a name="adding-tags-metadata"></a>
### 태그/메타데이터 추가

Mailgun, Postmark 등 일부 메일 서비스에서는 메시지 "태그"와 "메타데이터"를 지원합니다. 이메일 메시지에 태그와 메타데이터를 다음처럼 추가할 수 있습니다.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Comment Upvoted!')
                ->tag('upvote')
                ->metadata('comment_id', $this->comment->id);
}
```

Amazon SES를 사용하는 경우에도 `metadata` 메서드를 이용해 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage`의 `withSymfonyMessage` 메서드는 실제 메시지 전송 직전에 Symfony 메시지 인스턴스를 커스터마이징할 수 있는 기회를 줍니다.

```php
use Symfony\Component\Mime\Email;

public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->withSymfonyMessage(function (Email $message) {
                    $message->getHeaders()->addTextHeader(
                        'Custom-Header', 'Header Value'
                    );
                });
}
```

<a name="using-mailables"></a>
### Mailable 사용하기

필요에 따라, 알림의 `toMail` 메서드에서 [mailable 객체](/docs/{{version}}/mail)를 반환할 수 있습니다. 이 경우 수신자를 mailable 객체의 `to` 메서드로 지정하셔야 합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailable과 온디맨드 알림

[온디맨드 알림](#on-demand-notifications)을 전송하는 경우, `toMail`의 `$notifiable`은 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스입니다. `routeNotificationFor` 메서드를 통해 이메일 주소를 가져올 수 있습니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

public function toMail(object $notifiable): Mailable
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

메일 알림 템플릿을 디자인할 때, 루트 클로저나 컨트롤러에서 mail notification의 메시지를 반환하면 웹 브라우저에서 바로 미리볼 수 있습니다.

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
## Markdown 메일 알림

Markdown 메일 알림은 사전에 준비된 알림용 템플릿을 활용하면서 긴 메시지나 커스텀 메시지를 자유롭게 작성하도록 해줍니다. Markdown으로 작성된 메시지는 Laravel에서 아름답고 반응형인 HTML 템플릿과 텍스트 버전으로 자동 출력됩니다.

<a name="generating-the-message"></a>
### 메시지 생성

Markdown 템플릿과 함께 알림을 생성하려면 `make:notification` Artisan 명령에 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

사용 방식은 일반 메일 알림과 같습니다. 다만 메시지 내용을 작성할 때는 `line`, `action` 대신 `markdown` 메서드로 템플릿을 지정하면 됩니다.

```php
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="writing-the-message"></a>
### 메시지 작성

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법을 결합해 쉽게 알림을 만들 수 있습니다.

```blade
<x-mail::message>
# Invoice Paid

Your invoice has been paid!

<x-mail::button :url="$url">
View Invoice
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

<a name="button-component"></a>
#### 버튼 컴포넌트

중앙 정렬 버튼을 만들려면 `url`과 `color` 속성을 사용하세요. 색상은 `primary`, `green`, `red`를 지원합니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 블록 내에 다른 배경색을 적용해 텍스트 강조가 가능합니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

Markdown 테이블을 HTML 테이블로 변환합니다. 정렬도 Markdown 기본 문법을 따릅니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

Markdown 컴포넌트를 직접 커스터마이징하려면, 아래 명령어로 퍼블리시하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

`resources/views/vendor/mail` 경로에 `html`과 `text` 디렉터리가 추가되며, 각각의 컴포넌트가 포함됩니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 퍼블리시하면 `resources/views/vendor/mail/html/themes` 경로에 `default.css`를 볼 수 있습니다. CSS를 수정하면 스타일이 자동으로 인라인되어 적용됩니다. 새 테마를 만들려면 `html/themes`에 추가하고, `config/mail.php`에서 테마 옵션을 수정하세요.

특정 알림에만 커스텀 테마를 적용하려면 `theme` 메서드를 사용하세요.

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->theme('invoice')
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="database-notifications"></a>
## DB 알림

<a name="database-prerequisites"></a>
### 사전 준비

`database` 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 테이블 구조에는 알림 타입과 JSON 형태의 데이터가 포함됩니다.

아래 명령어로 알림 테이블 migration을 실행하세요.

```shell
php artisan notifications:table

php artisan migrate
```

> [!NOTE]
> [UUID/ULID](/docs/{{version}}/eloquent#uuid-and-ulid-keys) 기본키를 사용할 경우 migration에서 `morphs` 대신 [`uuidMorphs`](/docs/{{version}}/migrations#column-method-uuidMorphs) 또는 [`ulidMorphs`](/docs/{{version}}/migrations#column-method-ulidMorphs)를 사용하세요.

<a name="formatting-database-notifications"></a>
### DB 알림 포맷팅

알림 내용을 DB에 저장하려면 `toDatabase` 또는 `toArray` 메서드를 정의하세요. 반환된 PHP 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다.

```php
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

기본적으로 `type` 컬럼에는 알림 클래스명이 저장됩니다. 이를 변경하고 싶다면 `databaseType` 메서드를 정의하세요.

```php
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase`와 `toArray`의 차이

`broadcast` 채널도 `toArray` 결과를 사용하므로, DB와 방송용 데이터를 따로 다르게 하려면 `toDatabase`를 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근

DB에 저장된 알림은 Notifiable 트레이트의 `notifications` [Eloquent 관계](/docs/{{version}}/eloquent-relationships)로 조회할 수 있습니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

안 읽은(unread) 알림만 조회하려면 `unreadNotifications` 관계를 사용하세요.

```php
foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서도 알림을 쓰려면, 컨트롤러에서 현재 사용자 등의 알림을 반환하는 API를 만들면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리

사용자가 알림을 확인하면 `"read"`로 표시해야 할 때가 많습니다. Notifiable 트레이트의 `markAsRead` 메서드를 사용하세요.

```php
foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

콜렉션 전체에 대해 한 번에 할당할 수도 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

DB에서 직접 모두 업데이트하려면 mass-update 쿼리를 사용하세요.

```php
$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 삭제하려면 `delete`를 호출합니다.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 전, Laravel의 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 기능을 먼저 숙지하고 설정하세요.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 알림을 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 서비스로 내보내며, JS 프론트엔드에서 실시간으로 수신할 수 있습니다. 알림 클래스에 `toBroadcast` 메서드를 정의하면, 반환된 `BroadcastMessage` 인스턴스가 JSON으로 변환되어 방송됩니다.

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

public function toBroadcast(object $notifiable): BroadcastMessage
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```

<a name="broadcast-queue-configuration"></a>
#### 브로드캐스트 큐 설정

모든 브로드캐스트 알림은 자동으로 큐잉됩니다. 큐 연결이나 큐명을 직접 지정하려면 `onConnection`, `onQueue`를 사용하세요.

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

방송 알림 데이터에는 항상 알림의 클래스명(full name)이 `type` 필드로 포함됩니다. 커스터마이징하려면 `broadcastType` 메서드를 정의하세요.

```php
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신

알림은 `{notifiable}.{id}` 규칙의 프라이빗 채널로 브로드캐스트됩니다. 예를 들어, ID 1인 `App\Models\User`에게 알림을 보낸 경우 `App.Models.User.1` 채널에서 받을 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이징

알림이 어떤 채널에 브로드캐스트될지 커스터마이징하려면 notifiable 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 추가하세요.

```php
public function receivesBroadcastNotificationsOn(): string
{
    return 'users.'.$this->id;
}
```

<a name="sms-notifications"></a>
## SMS 알림

<a name="sms-prerequisites"></a>
### 사전 준비

Laravel의 SMS 알림은 [Vonage](https://www.vonage.com/)를 기본 지원합니다. 먼저 다음 패키지를 설치하세요.

```
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

환경 파일에 Vonage 키/시크릿 및 기본 발신번호(`VONAGE_SMS_FROM`)를 설정하세요.

```
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

알림 클래스에 `toVonage` 메서드를 정의하면 됩니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 콘텐츠

SMS에 유니코드 문자가 포함될 경우, `unicode` 메서드를 호출하세요.

```php
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
                ->content('Your unicode message')
                ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### "From" 번호 커스터마이징

특정 알림만 별도의 전화번호로 보내고 싶으면 `from`을 사용하십시오.

```php
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
                ->content('Your SMS message content')
                ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가

사용자 별로 비용 추적이 필요하다면, 알림에 "client reference"를 추가할 수 있습니다.

```php
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 라우팅

Vonage 알림을 올바른 번호로 전송하려면, notifiable 엔티티에 `routeNotificationForVonage` 메서드를 추가하세요.

```php
public function routeNotificationForVonage(Notification $notification): string
{
    return $this->phone_number;
}
```

<a name="slack-notifications"></a>
## Slack 알림

<a name="slack-prerequisites"></a>
### 사전 준비

Slack 알림을 보내려면 아래 패키지를 먼저 설치하세요.

```shell
composer require laravel/slack-notification-channel
```

또한, [Slack App](https://api.slack.com/apps?new_app=1)을 생성하고, 필요한 권한 범위(`chat:write`, `chat:write.public`, `chat:write.customize`)를 할당한 후, Bot User OAuth Token을 `services.php`에 등록해야 합니다.

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### 앱 배포(App Distribution)

외부 Slack 워크스페이스 사용자를 대상으로 알림을 보내야 한다면 Slack에서 앱을 "배포"해야 합니다. 자세한 내용은 Slack의 "Manage Distribution" 메뉴와 [Socialite 도큐먼트](/docs/{{version}}/socialite#slack-bot-scopes)를 참고하세요.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack로 메시지를 보낼 수 있는 알림은 클래스 내에 `toSlack` 메서드를 정의하세요. 이 메서드는 `Illuminate\Notifications\Slack\SlackMessage`를 반환해야 하며, [Slack의 Block Kit API](https://api.slack.com/block-kit)를 지원합니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
            ->text('One of your invoices has been paid!')
            ->headerBlock('Invoice Paid')
            ->contextBlock(function (ContextBlock $block) {
                $block->text('Customer #1234');
            })
            ->sectionBlock(function (SectionBlock $block) {
                $block->text('An invoice has been paid.');
                $block->field("*Invoice No:*\n1000")->markdown();
                $block->field("*Invoice Recipient:*\ntaylor@laravel.com")->markdown();
            })
            ->dividerBlock()
            ->sectionBlock(function (SectionBlock $block) {
                $block->text('Congratulations!');
            });
}
```

<a name="slack-interactivity"></a>
### Slack 상호작용

Slack Block Kit을 이용하면 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling)가 가능합니다. Slack App에 "Interactivity" 기능을 활성화하고, "Request URL"을 등록하세요.

버튼 클릭 등 상호작용 정보를 처리하려면 `actionsBlock`을 사용할 수 있습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
// ...
->actionsBlock(function (ActionsBlock $block) {
    $block->button('Acknowledge Invoice')->primary();
    $block->button('Deny')->danger()->id('deny_invoice');
});
```

<a name="slack-confirmation-modals"></a>
#### 확인(Confirmation) 모달

버튼 클릭 시 동작 전에 확인 모달을 띄우려면, `confirm` 메서드를 사용하세요.

```php
$block->button('Acknowledge Invoice')
      ->primary()
      ->confirm(
          'Acknowledge the payment and send a thank you email?',
          function (ConfirmObject $dialog) {
              $dialog->confirm('Yes');
              $dialog->deny('No');
          }
      );
```

<a name="inspecting-slack-blocks"></a>
#### Slack Block 빠른 확인

구성한 Block을 빠르게 확인하려면 `dd` 메서드를 사용하여 Slack Block Kit Builder에서 바로 확인할 수 있습니다.

```php
return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 라우팅

Slack 알림을 올바른 팀 및 채널로 전송하려면 notifiable 모델에 `routeNotificationForSlack` 메서드를 정의합니다. 반환값은 다음 셋 중 하나일 수 있습니다:

- `null` (알림 내에서 채널 지정)
- 채널명 문자열(`'#support-channel'`)
- `SlackRoute` 인스턴스(`SlackRoute::make($this->slack_channel, $this->slack_token)`)

```php
public function routeNotificationForSlack(Notification $notification): mixed
{
    return '#support-channel';
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack Workspace 알림

> [!NOTE]
> 외부 Slack에 알림을 보내기 전 앱을 [배포](#slack-app-distribution)해야 합니다.

사용자별로 Slack 봇 토큰을 Socialite로 받아오고, 스토리지에 저장한 후 `SlackRoute::make`를 사용해 알림을 보낼 수 있습니다.

```php
public function routeNotificationForSlack(Notification $notification): mixed
{
    return SlackRoute::make($this->slack_channel, $this->slack_token);
}
```

<a name="localizing-notifications"></a>
## 알림 지역화(로컬라이징)

알림은 HTTP 요청의 현재 로케일과 별도로 다른 언어로 전송할 수 있습니다. 이 로케일 설정은 큐잉된 알림에도 적용됩니다.

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 사용자에게 동시에 지정하려면 Notification 파사드를 활용하세요.

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일 사용

사용자별 선호 언어를 따로 저장하는 경우, notifiable 모델에 `HasLocalePreference` 컨트랙트를 구현하세요.

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이후 별도로 `locale`을 지정하지 않아도 우선 사용자의 선호 언어로 발송됩니다.

<a name="testing"></a>
## 테스트

`Notification` 파사드의 `fake` 메서드를 이용하면 실제로 알림이 전송되지 않게 할 수 있습니다. 그 후 `assertSentTo`, `assertNothingSent`, `assertCount` 등 다양한 어서션도 지원합니다.

```php
Notification::fake();

Notification::assertNothingSent();

Notification::assertSentTo([$user], OrderShipped::class);

Notification::assertNotSentTo([$user], AnotherNotification::class);

Notification::assertCount(3);
```

클로저를 전달하여 알림 데이터까지 체크할 수 있습니다.

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 알림 테스트

온디맨드 알림 전송 여부는 `assertSentOnDemand`로 검사할 수 있습니다.

```php
Notification::assertSentOnDemand(OrderShipped::class);

Notification::assertSentOnDemand(
    OrderShipped::class,
    function (OrderShipped $notification, array $channels, object $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="notification-events"></a>
## 알림 이벤트

<a name="notification-sending-event"></a>
#### 알림 발송 전 이벤트

알림이 발송될 때, `Illuminate\Notifications\Events\NotificationSending` [이벤트](/docs/{{version}}/events)가 발생합니다. 이벤트 리스너에서 이 이벤트를 수신하면 알림을 취소(`false` 반환)할 수도 있습니다.

```php
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 내에서 `notifiable`, `notification`, `channel` 속성 등 다양한 정보에 접근할 수 있습니다.

<a name="notification-sent-event"></a>
#### 알림 발송 후 이벤트

알림 발송 후에는 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/{{version}}/events)가 발생합니다. 리스너에 등록된 이벤트입니다.

```php
protected $listen = [
    NotificationSent::class => [
        LogNotification::class,
    ],
];
```

이벤트 내에서 `notifiable`, `notification`, `channel`, `response`에 접근할 수 있습니다.

> [!NOTE]
> 리스너 생성 후 `event:generate` Artisan 명령으로 클래스를 자동 생성할 수 있습니다.

<a name="custom-channels"></a>
## 커스텀 채널

Laravel은 여러 기본 채널을 지원하지만, 직접 구현한 채널로 알림을 보낼 수 있습니다.

커스텀 채널 클래스는 `send` 메서드를 구현해야 하며, `$notifiable`, `$notification` 인자를 받습니다. 이 메서드 내에서 알림 객체의 메시지를 작성하고 원하는 방식으로 전송하면 됩니다.

```php
namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);
        // $notifiable 엔티티에 메시지 전송
    }
}
```

작성한 커스텀 채널은 알림 클래스의 `via`에서 사용하세요.

```php
public function via(object $notifiable): string
{
    return VoiceChannel::class;
}
```

`toVoice`와 같은 메서드는 자유롭게 설계할 수 있습니다. 예시는 별도의 `VoiceMessage` 클래스를 만들어 사용하는 방식입니다.