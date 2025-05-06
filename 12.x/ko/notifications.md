# 알림(Notifications)

- [소개](#introduction)
- [알림 클래스 생성](#generating-notifications)
- [알림 전송하기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐 처리(Queueing)](#queueing-notifications)
    - [온디맨드 알림(즉석 알림)](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 설정](#customizing-the-sender)
    - [수신자 커스텀](#customizing-the-recipient)
    - [제목 커스텀](#customizing-the-subject)
    - [메일러 커스텀](#customizing-the-mailer)
    - [템플릿 커스텀](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony Message 커스텀](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스텀](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - ["From" 번호 커스텀](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 라우팅](#routing-sms-notifications)
- [슬랙(Slack) 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [슬랙 알림 포맷팅](#formatting-slack-notifications)
    - [슬랙 상호작용(Interactivity)](#slack-interactivity)
    - [슬랙 라우팅](#routing-slack-notifications)
    - [외부 워크스페이스에 알림 보내기](#notifying-external-slack-workspaces)
- [알림 현지화(Localizing)](#localizing-notifications)
- [테스트하기](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

Laravel은 [이메일 전송](/docs/{{version}}/mail) 기능 외에도 다양한 전송 채널을 지원합니다. 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 구 Nexmo), [Slack](https://slack.com) 등이 대표적입니다. 또한, 다양한 [커뮤니티 기반 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 제공되어 수십 개 이상의 채널로 알림을 전송할 수 있습니다! 알림은 데이터베이스에도 저장할 수 있으며, 저장된 알림은 웹 인터페이스에서 표시할 수 있습니다.

보통 알림은 사용자에게 애플리케이션에서 발생한 특정 이벤트를 짧고 간단하게 알려주는 용도로 사용됩니다. 예를 들어, 결제 애플리케이션을 개발 중이라면, 사용자의 청구서가 결제되었을 때 "Invoice Paid(청구서 결제 완료)" 알림을 이메일과 SMS로 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 클래스 생성하기

Laravel에서 각 알림은 클래스 단위로 표현되며, 일반적으로 `app/Notifications` 디렉터리에 저장됩니다. 만약 디렉터리가 없다면, 아래의 `make:notification` 아티즌 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령은 새로운 알림 클래스를 `app/Notifications`에 생성합니다. 각각의 알림 클래스에는 `via` 메서드와, 해당 채널에 맞는 메시지 구성 메서드들(`toMail`, `toDatabase` 등)이 포함됩니다.

<a name="sending-notifications"></a>
## 알림 전송하기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드 또는 `Notification` [파사드](/docs/{{version}}/facades)를 이용해 전송할 수 있습니다. `Notifiable` 트레이트는 기본적으로 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트에서 제공하는 `notify` 메서드는 알림 인스턴스를 인자로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 `User` 모델 외 모든 모델에서 사용이 가능합니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

여러 "notifiable" 엔티티(예: 다수의 사용자)에게 알림을 보내야 할 경우 `Notification` [파사드](/docs/{{version}}/facades)를 사용할 수 있습니다. 이 경우, `send` 메서드에 대상 엔티티들과 알림 인스턴스를 전달합니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

바로 전송하고 싶다면 `sendNow` 메서드를 사용할 수도 있습니다. 이 메서드는 `ShouldQueue` 인터페이스가 구현된 경우에도 바로 전송됩니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

각 알림 클래스에는 알림이 어떤 채널(`mail`, `database`, `broadcast`, `vonage`, `slack` 등)로 보내질지 결정하는 `via` 메서드가 있습니다.

> [!NOTE]
> Telegram, Pusher 등 다른 채널을 사용하려면, 커뮤니티 주도의 [Laravel Notification Channels 사이트](http://laravel-notification-channels.com)를 참조하세요.

`via` 메서드는 `$notifiable` 인스턴스를 받아서 채널을 동적으로 결정할 수 있습니다:

```php
public function via(object $notifiable): array
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐 처리(Queueing)

> [!WARNING]
> 알림을 큐로 처리하려면, 큐 설정을 완료하고 [워커를 실행](/docs/{{version}}/queues#running-the-queue-worker)해야 합니다.

알림 채널이 외부 API 호출을 포함하는 경우, 전송이 오래 걸릴 수 있습니다. 애플리케이션 반응속도를 높이기 위해 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 추가하면 알림을 큐에 넣을 수 있습니다. `make:notification` 명령으로 생성된 알림에는 이미 import 되어 있으니 바로 추가할 수 있습니다:

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

이제 `ShouldQueue`가 추가됐다면 기존과 동일한 방식으로 알림을 전송할 수 있고, Laravel이 자동으로 큐에 넣어줍니다.

```php
$user->notify(new InvoicePaid($invoice));
```

큐잉 시, 수신자와 채널 조합마다 하나씩 큐 잡이 생성됩니다. 예를 들어, 3명의 수신자와 2개의 채널이 있다면 6개의 잡이 생성됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연 전송

알림을 일정 시간 뒤에 전송하고 싶다면, 인스턴스 생성 후 `delay` 메서드를 체이닝하세요:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널에 대해 지연 시간을 배열로 지정할 수도 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스에 `withDelay` 메서드를 정의해도 됩니다:

```php
public function withDelay(object $notifiable): array
{
    return [
        'mail' => now()->addMinutes(5),
        'sms' => now()->addMinutes(10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
#### 큐 연결(커넥션) 변경

알림 큐에 사용할 커넥션을 지정하려면 생성자에서 `onConnection`을 호출하세요:

```php
public function __construct()
{
    $this->onConnection('redis');
}
```

또는 채널별로 사용할 큐 커넥션을 지정하려면 `viaConnections` 메서드를 사용하세요:

```php
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

채널별로 사용할 큐를 지정하려면 `viaQueues` 메서드를 정의하세요:

```php
public function viaQueues(): array
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="queued-notification-middleware"></a>
#### 큐 알림 미들웨어

큐에 저장된 알림에도 [잡 미들웨어](/docs/{{version}}/queues#job-middleware)를 사용할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하세요. `$notifiable`, `$channel` 두 인자가 전달됩니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

public function middleware(object $notifiable, string $channel)
{
    return match ($channel) {
        'mail' => [new RateLimited('postmark')],
        'slack' => [new RateLimited('slack')],
        default => [],
    };
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 큐 알림과 DB 트랜잭션

큐 알림이 DB 트랜잭션 내에서 디스패치되면, 때때로 트랜잭션 커밋 전에 큐 워커가 처리할 수 있습니다. 이 경우, 트랜잭션 내에서 생성/수정된 데이터가 아직 반영되지 않아 예기치 않은 문제가 발생할 수 있습니다.

큐 커넥션의 `after_commit`이 `false`라도, 알림을 디스패치할 때 `afterCommit` 메서드를 호출해 트랜잭션 커밋 후 알림이 보내지도록 할 수 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->afterCommit());
```
혹은 생성자에서 호출해도 됩니다.

```php
public function __construct()
{
    $this->afterCommit();
}
```

> [!NOTE]
> 추가 정보는 [큐 잡과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 실제 전송 여부 결정

큐에 들어간 후 실제로 알림을 보낼지 여부를 최종적으로 결정하려면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. `false`를 반환하면 해당 알림은 전송되지 않습니다:

```php
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림(즉석 알림)

앱 사용자가 아닌 대상에게 알림을 보낼 경우 `Notification` 파사드의 `route` 메서드를 사용해 임시로 라우팅 정보를 지정한 뒤 알림을 보내세요:

```php
Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일로 보낼 때 이름도 지정하려면 배열로 전달합니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 채널에 대한 경로를 한 번에 지정할 수 있습니다:

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

이메일로 발송이 가능하도록 하려면 알림 클래스에 `toMail` 메서드를 구현해야 합니다. 이 메서드는 `$notifiable` 객체를 받아 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션 메일 작성에 도움이 되는 다양한 메서드를 제공합니다. 예를 들어:

```php
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
> `toMail` 메서드에서 `$this->invoice->id`처럼 필요한 모든 데이터를 생성자에 주입해서 사용할 수 있습니다.

예시에서 보듯이, 인사말, 텍스트 줄, 콜 투 액션, 설명 줄 등을 간편하게 작성할 수 있습니다. 메일 채널은 HTML, 텍스트 형식의 아름다운 반응형 이메일을 생성해줍니다.

<img src="https://laravel.com/img/docs/notification-example-2.png">

> [!NOTE]
> 메일 알림을 보낼 땐 반드시 `config/app.php`의 `name` 옵션을 지정하세요. 이 값이 메일의 헤더와 풋터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

일부 알림(예: 결제 실패)은 에러를 전달합니다. 이럴 땐 `error` 메서드를 통해 버튼 색깔을 빨간색으로 변경 가능합니다:

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
#### 기타 메일 알림 포맷 옵션

알림 클래스에서 직접 여러 줄을 작성하는 방식 외에, `view` 메서드로 커스텀 템플릿을 사용할 수도 있습니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

두 번째 인자에 텍스트 전용 뷰 이름도 배열로 전달 가능합니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

텍스트 이메일만 있는 경우에는 `text` 메서드를 쓰세요:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자(customizing the sender)

이메일의 발신자/From 주소는 기본적으로 `config/mail.php`에서 정의되어 있지만, 개별 알림마다 `from` 메서드로 지정할 수 있습니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 커스텀(customizing the recipient)

`mail` 채널로 보낼 때는 기본적으로 `email` 속성을 사용합니다. 만약 다른 주소로 보내려면 모델에 `routeNotificationForMail` 메서드를 정의하세요:

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
### 제목 커스텀(customizing the subject)

기본적으로 제목은 클래스명을 Title Case로 변환한 값입니다. 제목을 직접 정하려면 `subject` 메서드를 사용하세요:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 커스텀

메일 알림은 기본적으로 `config/mail.php` 에서 지정된 메일러로 전송되지만, 개별 메시지에 대해 `mailer` 메서드로 지정이 가능합니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 커스텀

메일 알림의 HTML 및 텍스트 템플릿을 커스텀하려면 노티피케이션 패키지의 리소스를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-notifications
```
이 명령을 실행하면 메일 템플릿이 `resources/views/vendor/notifications`에 생성됩니다.

<a name="mail-attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메시지 빌더에 `attach` 메서드를 사용하세요. 첫 번째 인자는 파일의 절대경로입니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> `attach` 메서드는 [attachable 객체](/docs/{{version}}/mail#attachable-objects)도 지원합니다. 자세한 내용은 관련 문서를 참고하세요.

첨부 시 표시 이름이나 MIME 타입을 두 번째 인자로 배열로 전달할 수 있습니다:

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

`mailable`에서처럼 `attachFromStorage`로 직접 스토리지에서 첨부하는 것은 지원하지 않습니다. 필요하다면 `toMail`에서 mailable을 반환하세요:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

여러 개의 파일을 첨부하려면 `attachMany` 메서드를 사용하세요:

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
#### 원시 데이터 첨부

`attachData` 메서드를 사용하면 바이트 스트림(문자열)을 첨부파일로 전송할 수 있습니다:

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
### 태그와 메타데이터 추가

Mailgun, Postmark 등 일부 메일 서비스는 "태그"와 "메타데이터"를 지원합니다. `tag`와 `metadata` 메서드로 추가할 수 있습니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

각 서비스별 자세한 사용법은 공식 문서를 참고하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony Message 커스텀

`withSymfonyMessage` 메서드를 사용하면 Symfony Message 인스턴스를 직접 조작할 수 있습니다:

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
### Mailable 객체 사용

필요하다면, 알림의 `toMail`에서 [mailable 객체](/docs/{{version}}/mail)를 반환할 수도 있습니다. 이 경우, 받는 사람은 mailable의 `to` 메서드로 지정해주세요:

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

[온디맨드 알림](#on-demand-notifications) 전송 시, `toMail`로 전달된 `$notifiable`은 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스입니다. 이 객체의 `routeNotificationFor` 메서드로 실제 이메일 주소를 조회할 수 있습니다:

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

메일 알림 템플릿을 빠르게 브라우저에서 미리보려면, 알림에서 생성한 메시지를 라우트나 컨트롤러에서 바로 반환하세요:

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

마크다운 메일 알림은 기본 템플릿을 활용하면서, 더 긴 메시지와 자유로운 커스터마이즈가 가능합니다. 메시지는 마크다운 문법으로 작성하며, Laravel이 자동으로 HTML과 텍스트 이메일을 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

마크다운 알림 클래스를 만들 때는 `make:notification` 명령에 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

기존의 `line`, `action` 대신 `markdown` 메서드로 사용할 템플릿과 데이터를 지정합니다:

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
### 메시지 작성하기

마크다운 알림은 Blade 컴포넌트와 마크다운 문법을 혼합해 작성합니다:

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

> [!NOTE]
> 마크다운 이메일 작성 시, 들여쓰기를 과도하게 사용하지 마세요. 들여쓰기는 코드 블록으로 해석됩니다.

#### 버튼 컴포넌트

버튼을 가운데에 렌더링합니다. `url`과(optional) `color`(primary, green, red) 속성을 사용할 수 있습니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

#### 패널 컴포넌트

특정 내용을 패널(배경색이 약간 다른 박스)로 강조할 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

#### 테이블 컴포넌트

마크다운 테이블을 HTML 테이블로 변환합니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스텀

마크다운 알림 컴포넌트를 직접 커스텀하려면 아래 명령을 이용하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

`resources/views/vendor/mail` 경로에 컴포넌트가 복사됩니다. `html`, `text` 하위 폴더에서 개별 컴포넌트를 수정할 수 있습니다.

#### CSS 커스텀

`resources/views/vendor/mail/html/themes/default.css` 에서 CSS를 수정하세요. 새 테마를 만들고 싶으면 해당 디렉터리에 CSS 파일을 만들고 `mail` 설정 파일의 `theme` 옵션을 변경하세요.

개별 알림별로 테마를 지정하려면 `theme` 메서드를 사용하세요:

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
## 데이터베이스 알림

<a name="database-prerequisites"></a>
### 사전 준비

`database` 채널은 알림을 DB 테이블에 저장합니다. `make:notifications-table` 명령어로 마이그레이션 파일을 생성하세요:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> [UUID나 ULID 프라이머리 키](/docs/{{version}}/eloquent#uuid-and-ulid-keys)를 사용한다면 마이그레이션의 `morphs` 대신 [uuidMorphs](/docs/{{version}}/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/{{version}}/migrations#column-method-ulidMorphs)로 교체하세요.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

DB 저장이 가능하도록 하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 구현해야 합니다. 해당 메서드는 평문 PHP 배열을 반환해야 하며, 해당 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 칼럼에 저장됩니다:

```php
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

기본적으로 `type` 칼럼은 알림 클래스명, `read_at`는 `null`로 저장됩니다. `databaseType` 및 `initialDatabaseReadAtValue` 메서드로 커스텀도 가능합니다:

```php
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

#### `toDatabase` vs. `toArray`

`toArray` 메서드는 `broadcast` 채널에서도 사용됩니다. DB 저장용/브로드캐스트용 각기 다른 포맷이 필요하다면 `toDatabase` 메서드를 따로 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근

DB에 저장된 알림은 notifiable 엔티티(보통 유저)의 `notifications` [Eloquent 관계](/docs/{{version}}/eloquent-relationships)를 통해 조회할 수 있습니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은(unread) 알림만 조회하려면 `unreadNotifications` 관계를 사용합니다:

```php
foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림을 접근하려면, 별도 컨트롤러를 만들어 REST API 등으로 전달하도록하세요.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리

알림을 읽음 처리를 하려면, 각각의 알림에서 `markAsRead` 메서드를 호출하세요:

```php
foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

전체 알림에 한 번에 사용 가능:

```php
$user->unreadNotifications->markAsRead();
```

DB에서 조회 없이 대량 업데이트도 가능합니다:

```php
$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 삭제하려면:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하려면 Laravel의 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 기능을 설정해야 합니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 기능을 이용하여, 자바스크립트 프론트엔드에서 실시간으로 알림을 받을 수 있도록 합니다. 알림 클래스에 `toBroadcast` 메서드를 정의할 수 있으며, 이 메서드는 `BroadcastMessage` 인스턴스를 반환해야 합니다:

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

#### 브로드캐스트 큐 설정

브로드캐스트 알림은 모두 큐잉됩니다. 사용 커넥션/큐 이름은 `onConnection`, `onQueue` 메서드로 지정할 수 있습니다:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

#### 알림 타입 커스텀

브로드캐스트 알림엔 알림의 클래스명이 기본 `type` 필드로 포함됩니다. 직접 지정하려면 `broadcastType` 메서드를 정의하세요:

```php
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 대기

알림은 `{notifiable}.{id}` 형식의 private 채널로 방송됩니다. 예를 들어, User(1)에게 전송한 알림은 `App.Models.User.1` 채널에 브로드캐스트됩니다. [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)로 리스닝이 가능합니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

#### 알림 채널 커스텀

엔티티별로 브로드캐스트 알림 채널을 커스텀하려면 `receivesBroadcastNotificationsOn` 메서드를 notifiable 모델에 정의하세요:

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

Laravel의 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 Nexmo)와 [guzzlehttp/guzzle] 패키지가 필요합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

환경변수를 아래처럼 지정하세요:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

알림 클래스에 `toVonage` 메서드를 정의하고, 이 메서드가 `Illuminate\Notifications\Messages\VonageMessage`를 반환해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

#### 유니코드 콘텐츠

SMS 메시지에 유니코드 문자가 포함된다면 `unicode` 메서드를 사용하세요:

```php
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### 발신번호 커스텀

특정 알림을 다른 발신번호(From)로 보내고 싶다면 `from` 메서드를 사용하세요:

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

사용자별 비용 산정 등을 위해 클라이언트 참조 값을 추가할 수 있습니다. Vonage에서 보고서로 활용할 수 있습니다:

```php
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->clientReference((string) $notifiable->id)
        ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

알림이 올바른 번호로 전송되도록 notifiable 모델에 `routeNotificationForVonage`를 정의합니다:

```php
public function routeNotificationForVonage(Notification $notification): string
{
    return $this->phone_number;
}
```

<a name="slack-notifications"></a>
## 슬랙(Slack) 알림

<a name="slack-prerequisites"></a>
### 사전 준비

아래 패키지를 설치하세요.

```shell
composer require laravel/slack-notification-channel
```

또한 슬랙 앱을 생성하고, 필요한 OAuth 스코프(`chat:write`, `chat:write.public`, `chat:write.customize`)를 부여한 후 "Bot User OAuth Token"을 설정하고 `services.php`에 아래와 같이 입력하세요:

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

#### 앱 배포(App Distribution)

외부 워크스페이스로 알림을 보내려면 슬랙 앱을 배포해야 합니다. [Socialite](/docs/{{version}}/socialite)로 슬랙 Bot 토큰을 얻을 수 있습니다.

<a name="formatting-slack-notifications"></a>
### 슬랙 알림 포맷팅

알림 클래스에 `toSlack` 메서드를 정의하고, 내부에서 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환하세요. [Block Kit API](https://api.slack.com/block-kit)를 지원합니다:

```php
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

#### Block Kit 템플릿 사용

Builder에서 만든 JSON 코드를 `usingBlockKitTemplate`로 바로 전달할 수도 있습니다.

<a name="slack-interactivity"></a>
### 슬랙 상호작용(Interactivity)

슬랙 Block Kit에서는 상호작용을 처리할 'Request URL'을 등록해야 하며, [요청 검증](https://api.slack.com/authentication/verifying-requests-from-slack)도 하세요. 예시는 생략합니다.

#### 확인 모달(Confirmation Modal)

확정 대화상자를 띄우려면 `confirm` 메서드를 사용하세요.

#### 블록 구조 빠르게 확인하기

`SlackMessage` 인스턴스의 `dd` 메서드를 호출하면 Block Kit Builder 미리보기 URL을 확인할 수 있습니다.

<a name="routing-slack-notifications"></a>
### 슬랙 라우팅

슬랙 알림이 적절한 팀/채널로 전송될 수 있게 notifiable 모델의 `routeNotificationForSlack`에 다음 중 하나를 반환하세요:

- `null` : 노티피케이션 내부에서 채널을 설정
- 문자열 : 채널명(예: `#support-channel`)
- `SlackRoute`: 외부 워크스페이스용(Token+채널 지정)

```php
public function routeNotificationForSlack(Notification $notification): mixed
{
    return '#support-channel';
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 워크스페이스에 알림 보내기

> [!NOTE]
> 외부 워크스페이스 전송 전, 앱이 배포되어 있어야 합니다.

앱 사용자 워크스페이스에 알림을 보내려면, Slack OAuth 토큰을 Socialite로 획득 후 `SlackRoute::make`을 사용하세요:

```php
public function routeNotificationForSlack(Notification $notification): mixed
{
    return SlackRoute::make($this->slack_channel, $this->slack_token);
}
```

<a name="localizing-notifications"></a>
## 알림 현지화(Localizing)

Laravel에서는 현재 HTTP 요청의 로케일과 다른 언어로 알림을 보낼 수 있으며, 큐에 들어가서 처리되어도 해당 언어 정보를 유지합니다.

`locale` 메서드로 언어를 지정하세요:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

파사드를 통한 다중 사용자 지정도 가능합니다:

```php
Notification::locale('es')->send($users, new InvoicePaid($invoice));
```

### 사용자 선호 로케일(User Preferred Locales)

유저별로 선호 로케일을 저장한 경우, notifiable 모델에 `HasLocalePreference` 인터페이스를 구현하면 Laravel이 자동으로 해당 로케일을 사용합니다:

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

인터페이스를 구현하면, 매번 `locale` 메서드를 호출할 필요가 없습니다.

<a name="testing"></a>
## 테스트하기

`Notification` 파사드의 `fake` 메서드를 사용하면 알림 실제 전송 없이, 노티피케이션이 전송되었는지 테스트할 수 있습니다.

```php tab=Pest
test('orders can be shipped', function () {
    Notification::fake();

    // ...작업 수행

    Notification::assertNothingSent();
    Notification::assertSentTo([$user], OrderShipped::class);
    Notification::assertNotSentTo([$user], AnotherNotification::class);
    Notification::assertCount(3);
});
```

```php tab=PHPUnit
class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Notification::fake();

        // ...작업 수행

        Notification::assertNothingSent();
        Notification::assertSentTo([$user], OrderShipped::class);
        Notification::assertNotSentTo([$user], AnotherNotification::class);
        Notification::assertCount(3);
    }
}
```

조건 검증이 필요한 경우 클로저를 활용하세요:

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

#### 온디맨드 알림 테스트

[온디맨드 알림](#on-demand-notifications)은 `assertSentOnDemand`로 검증하세요:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

클로저로 전송 "route"까지 같이 검증할 수 있습니다.

<a name="notification-events"></a>
## 알림 이벤트

#### Notification Sending Event

알림 전송 시점에 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 발생합니다. 수신자, 알림 인스턴스 등 정보가 담겨 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

핸들러가 `false`를 반환하면 알림이 전송되지 않습니다.

알림, 수신자, 채널 정보는 이벤트 속성에서 접근할 수 있습니다.

#### Notification Sent Event

알림 전송 후에는 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/{{version}}/events)가 발생합니다. 알림, 수신자, 채널, response 등 다양한 정보가 포함됩니다.

<a name="custom-channels"></a>
## 커스텀 채널

Laravel이 기본 제공하는 채널 외에 직접 채널을 만들 수도 있습니다. `send($notifiable, $notification)` 메서드를 가지는 클래스를 작성하면 됩니다.

```php
class VoiceChannel
{
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // 원하는 방식으로 $notifiable에 메세지 전송
    }
}
```

커스텀 채널을 사용하려면 알림의 `via` 메서드에서 클래스명을 반환하고, `toVoice` 등 채널에 맞는 메시지 생성 메서드를 구현합니다.

```php
class InvoicePaid extends Notification
{
    use Queueable;

    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```
