# 알림(Notification)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 전송하기](#sending-notifications)
    - [Notifiable 트레이트 사용](#using-the-notifiable-trait)
    - [Notification 퍼사드 사용](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 지정하기](#customizing-the-sender)
    - [수신자 지정하기](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 지정](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
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
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림 로컬라이징](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[이메일 전송](/docs/{{version}}/mail) 지원 외에도, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 발송을 지원합니다. 또한 [커뮤니티 기반 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 가지 다른 채널로 알림 전송이 가능합니다! 알림은 데이터베이스에 저장되어 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 사용자가 애플리케이션 내에서 발생한 일에 대해 간략히 정보를 받는 메시지입니다. 예를 들어, 결제 애플리케이션을 작성한다면 사용자의 이메일과 SMS 채널을 통해 "청구서가 결제됨" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 `app/Notifications` 디렉터리에 저장되는 하나의 클래스로 표현됩니다. 애플리케이션에 이 디렉터리가 없다면 `make:notification` Artisan 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 새로운 알림 클래스를 `app/Notifications` 디렉터리에 생성합니다. 각 알림 클래스에는 `via` 메서드와 다양한 채널에 맞게 포맷된 메시지를 만드는 `toMail`, `toDatabase`와 같은 일련의 메서드가 포함됩니다.

<a name="sending-notifications"></a>
## 알림 전송하기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 `Notifiable` 트레이트의 `notify` 메서드 또는 `Notification` [퍼사드](/docs/{{version}}/facades)로 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트의 `notify` 메서드는 알림 인스턴스를 인자로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. `User` 모델에만 제한되지 않습니다.

<a name="using-the-notification-facade"></a>
### Notification 퍼사드 사용

또는, `Notification` [퍼사드](/docs/{{version}}/facades)를 통해 여러 알림 대상을 한 번에 지정하여 알림을 전송할 수 있습니다. `send` 메서드에 알림 대상과 알림 인스턴스를 전달하세요:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 `ShouldQueue` 인터페이스를 구현한 경우에도 즉시 전송됩니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

모든 알림 클래스는 어떤 채널로 메시지를 보낼지 결정하는 `via` 메서드를 가집니다. 지원하는 채널에는 `mail`, `database`, `broadcast`, `vonage`, `slack` 등이 있습니다.

> [!NOTE]
> Telegram, Pusher와 같은 채널을 사용하려면 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 받으며, 이를 이용해 알림 전송 채널을 동적으로 결정할 수 있습니다:

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
### 알림 큐잉하기

> [!WARNING]
> 알림 큐를 사용하기 전에 큐 설정을 마치고 [워커를 시작](/docs/{{version}}/queues#running-the-queue-worker)해야 합니다.

알림 전송은 외부 API 호출 등으로 인해 시간이 걸릴 수 있습니다. 응답 속도를 높이려면 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해 알림을 큐에 넣으세요. `make:notification` 으로 생성한 경우 이미 이들이 임포트되어 있습니다.

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

`ShouldQueue` 적용 후, 평소대로 알림을 보내면 Laravel이 자동으로 큐잉 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

큐잉 시, 수신인과 채널의 조합마다 하나씩 job이 생성됩니다. 예: 3명·2채널 = 6개의 job.

<a name="delaying-notifications"></a>
#### 알림 지연 전송

알림 전송을 지연하려면 `delay` 메서드를 체이닝하세요:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

채널별로 지연 시간을 지정하려면 배열을 전달하세요:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는, 알림 클래스에 `withDelay` 메서드를 정의할 수도 있습니다:

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
#### 알림 큐 커넥션 지정

기본적으로 애플리케이션의 디폴트 큐 커넥션을 사용합니다. 특정 알림에 대해 다른 커넥션을 사용하려면 생성자에서 `onConnection`을 호출하세요:

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

채널별 큐 커넥션을 지정하려면 `viaConnections` 메서드를 정의하세요:

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
#### 알림 채널별 큐 지정

알림 채널별로 사용할 큐를 지정하려면 `viaQueues` 메서드를 정의합니다:

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

<a name="queued-notification-middleware"></a>
#### 큐잉된 알림 미들웨어

큐잉된 알림은 [큐잉된 작업과 동일하게 미들웨어](/docs/{{version}}/queues#job-middleware)를 정의할 수 있습니다. `middleware` 메서드를 알림 클래스에 정의하면, `$notifiable`과 `$channel`을 인자로 받아 알림의 목적지에 따라 미들웨어를 맞춤 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the notification job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(object $notifiable, string $channel)
{
    return match ($channel) {
        'email' => [new RateLimited('postmark')],
        'slack' => [new RateLimited('slack')],
        default => [],
    };
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 알림 큐와 데이터베이스 트랜잭션

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치되면, 큐에서 트랜잭션 커밋 전에 job을 처리할 수도 있습니다. 이로 인해 트랜잭션 내에서 생성/수정된 데이터가 반영되지 않을 수 있습니다. 만약 알림 전송이 해당 데이터에 의존한다면 예기치 않은 에러가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`인 경우에도, 알림 인스턴스에 `afterCommit` 메서드를 체이닝하여 모든 트랜잭션 커밋 후 알림을 디스패치할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 생성자에서 `afterCommit`을 호출할 수 있습니다:

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

> [!NOTE]
> 해당 이슈의 해결책에 대해서는 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 발송 여부 결정

백그라운드에서 큐잉된 알림은 큐 워커가 job을 받아 수신자에게 발송합니다. 하지만, 최종적으로 알림을 발송할지 여부를 확인하려면 `shouldSend` 메서드를 알림 클래스에 정의하세요. `false`를 반환하면 알림이 전송되지 않습니다:

```php
/**
 * Determine if the notification should be sent.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림

애플리케이션의 "user"로 저장되지 않은 대상에게 알림을 보내야 할 때는, `Notification` 퍼사드의 `route` 메서드를 사용하여 임시로 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 라우트에 수신자명을 함께 제공하려면 배열을 사용하세요:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널에 대해 한 번에 라우팅 정보를 지정하려면 `routes` 메서드를 사용할 수 있습니다:

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

알림을 이메일로 보낼 수 있다면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 인자로 받고, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스에는 트랜잭션 이메일 메시지 빌드를 도와주는 간단한 메서드들이 있습니다. 예시:

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
> `toMail` 내에서 `$this->invoice->id`와 같이 필요한 데이터를 생성자에서 주입할 수 있습니다.

이 예시에서는 인사말, 본문, 콜 투 액션(버튼), 감사 인사를 포함합니다. `MailMessage` 객체의 이 메서드 덕분에 짧고 트랜잭셔널한 이메일을 간단하게 만들 수 있습니다.

메일 채널은 이 메시지 구성을 아름답고 반응형인 HTML 템플릿(및 플레인 텍스트 본문)으로 변환합니다.

> [!NOTE]
> 메일 알림 발송 시, `config/app.php`의 `name` 옵션을 알맞게 설정하세요. 이 값은 메시지의 헤더와 풋터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

실패한 결제 등 오류를 알릴 경우 `error` 메서드를 사용해 메일 메시지가 에러임을 표시할 수 있습니다. 이 경우 행동 버튼이 검정색 대신 빨간색으로 표시됩니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->error()
        ->subject('Invoice Payment Failed')
        ->line('...');
}
```

<a name="other-mail-notification-formatting-options"></a>
#### 기타 메일 포맷팅 옵션

메시지 라인을 직접 작성하는 대신 `view` 메서드로 커스텀 Blade 템플릿을 지정할 수 있습니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

플레인 텍스트 뷰도 지정 가능합니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

플레인 텍스트만 보낼 경우 `text` 메서드를 사용합니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자 지정하기

기본적으로 발신 이메일은 `config/mail.php`에 설정되어 있습니다. 특정 알림에 대해 발신자를 지정하려면 `from` 메서드를 사용하세요:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 지정하기

기본적으로 `mail` 채널로 알림을 보낼 때 notifiable 엔터티의 `email` 프로퍼티를 사용합니다. 알림 수신 이메일을 커스터마이징하려면 엔터티에 `routeNotificationForMail` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    public function routeNotificationForMail(Notification $notification): array|string
    {
        // 이메일만 반환
        return $this->email_address;

        // 이메일과 이름 반환
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 제목은 알림 클래스명을 Title Case로 포맷한 결과입니다. 예: `InvoicePaid` → `Invoice Paid`. 다르게 지정하려면 `subject` 메서드를 사용하세요:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 지정

기본적으로 메일 알림은 `config/mail.php`에 지정된 메일러를 사용합니다. 특정 알림에 대해 다른 메일러를 사용하려면 `mailer` 메서드를 사용하세요:

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

메일 알림의 HTML/텍스트 템플릿은 리소스를 퍼블리싱하여 수정할 수 있습니다. 아래 명령어로 알림 패키지의 리소스를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

이메일 알림에 첨부파일을 추가하려면 `attach` 메서드를 사용하세요. 첫 번째 인자로 파일의 절대경로를 지정합니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> `attach` 메서드는 [첨부 객체](/docs/{{version}}/mail#attachable-objects) 역시 지원합니다.

파일명이나 MIME 유형 등 표시 설정이 필요할 때는 두 번째 인자로 배열을 전달합니다:

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

Mailable에서는 `attachFromStorage`를 바로 사용할 수 있지만, 알림에서는 반드시 절대경로를 통해 파일을 붙여야 합니다. 혹은, `toMail` 메서드에서 [mailable](/docs/{{version}}/mail#generating-mailables)를 반환할 수도 있습니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

여러 파일을 첨부하려면 `attachMany` 메서드를 사용하세요:

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

바이트 스트링을 첨부하려면 `attachData`를 사용하고, 첨부파일명도 명시합니다:

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
### 태그 및 메타데이터 추가

Mailgun, Postmark 등의 일부 외부 메일 서비스는 메시지 "태그"와 "메타데이터" 지원합니다. 이를 활용해 메일을 그룹화·추적할 수 있습니다:

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

각 메일 서비스에서 태그/메타데이터에 대한 자세한 내용은 공식 문서를 참고하세요. Amazon SES를 사용할 경우에도 `metadata`로 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage`의 `withSymfonyMessage` 메서드를 사용하면, 메일 발송 전 Symfony Message 인스턴스를 직접 커스터마이징할 수 있습니다:

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
### Mailable 사용

필요하다면, 알림의 `toMail` 메서드에서 완전한 [mailable 객체](/docs/{{version}}/mail)를 반환할 수 있습니다. 이 경우 수신자를 반드시 `to` 메서드로 지정해야 합니다:

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

[온디맨드 알림](#on-demand-notifications) 전송 시, `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable` 타입입니다. `routeNotificationFor` 메서드로 이메일 주소를 얻을 수 있습니다:

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

메일 알림 템플릿을 빠르게 미리 보고 싶을 때, 라우트 클로저나 컨트롤러에서 알림의 메일 메시지를 반환하면 브라우저에서 Blade 템플릿처럼 렌더링된 결과를 확인할 수 있습니다:

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

마크다운 메일 알림을 사용하면 사전 제공된 템플릿을 활용하면서, 더 긴 맞춤 메시지도 작성할 수 있습니다. 메시지는 Markdown 규격으로 작성되며, Laravel이 반응형 HTML·플레인 텍스트 둘 다 자동으로 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

마크다운 전용 템플릿이 있는 알림 생성 시, Artisan 명령어에 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

마크다운 탬플릿을 사용하는 알림도 `toMail` 메서드를 정의해야 하며, `line`, `action` 대신 `markdown` 메서드로 템플릿명을, 그리고 사용 데이터는 두 번째 인자로 넘깁니다:

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

마크다운 알림은 Blade 컴포넌트와 Markdown 문법을 조합합니다. 예시:

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
> 마크다운 이메일 작성 시 과도한 들여쓰기는 사용하지 마세요. 표준 Markdown 파서는 들여쓴 내용을 코드 블록으로 인식합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데로 정렬된 버튼 링크를 렌더링합니다. `url`과 `color`(옵션)를 받을 수 있으며, `primary`, `green`, `red` 색상이 지원됩니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 입력된 내용을 패널 스타일(배경색 차이로 구분)에 감싸어 시선을 끄는 용도로 사용 가능합니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 Markdown 표를 HTML 표로 렌더링합니다. 정렬도 Markdown 표 문법대로 적용됩니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

모든 마크다운 컴포넌트 리소스를 직접 앱으로 퍼블리시해 맞춤 수정할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

명령어 실행 후, 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 저장됩니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 퍼블리시 후 `resources/views/vendor/mail/html/themes/default.css`에서 스타일을 수정할 수 있습니다. 새로운 테마를 만드려면 CSS 파일을 같은 폴더에 두고, `mail` 설정의 `theme` 항목을 해당 이름으로 변경하면 됩니다.

특정 알림에 테마를 적용하려면 `theme` 메서드를 사용하세요:

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

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 유형, JSON 형태의 데이터 구조 등이 저장됩니다.

알림을 표시하려면 마이그레이션으로 알림 테이블부터 생성해야 합니다:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> Notifiable 모델이 [UUID 또는 ULID PK](/docs/{{version}}/eloquent#uuid-and-ulid-keys)를 사용한다면, 마이그레이션의 `morphs`를 [`uuidMorphs`](/docs/{{version}}/migrations#column-method-uuidMorphs) 또는 [`ulidMorphs`](/docs/{{version}}/migrations#column-method-ulidMorphs)로 교체하세요.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

알림을 DB에 저장하려면 `toDatabase` 또는 `toArray` 메서드를 알림 클래스에 정의하세요. 이 메서드는 메시지 데이터를 평문 PHP 배열로 반환합니다. 리턴값은 JSON으로 인코딩되어 DB의 `data` 컬럼에 들어갑니다.

```php
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

기본적으로 `type` 필드는 클래스명, `read_at`은 null입니다. 이를 커스터마이징하려면 `databaseType`/`initialDatabaseReadAtValue` 메서드를 구현하세요:

```php
use Illuminate\Support\Carbon;

public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs `toArray`

`toArray`는 `broadcast` 채널에도 사용됩니다. 데이터베이스·브로드캐스트용 배열을 분리하고 싶다면 `toDatabase`를, 아니라면 `toArray` 하나만 구현하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

알림이 DB에 저장되면, notifiable 엔터티(Eloquent 모델)에서 `notifications` 관계(기본 User 모델에 포함된 Notifiable 트레이트 제공)를 통해 접근할 수 있습니다. 기본 정렬은 최신 순입니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않음" 알림만 조회하려면 `unreadNotifications` 관계를 사용하세요:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트에서 알림을 조회하려면, 알림 컨트롤러를 작성해 현재 사용자에 대한 알림 목록을 반환하도록 구현하고 해당 URL로 HTTP 요청하면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리

일반적으로 알림을 사용자가 확인하면 읽음으로 처리합니다. Notifiable 트레이트의 `markAsRead` 메서드를 사용하세요:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

알림 컬렉션 전체를 한 번에 읽음 처리할 수도 있습니다:

```php
$user->unreadNotifications->markAsRead();
```

읽음 처리만 하고 DB에서 제거하지 않으려면 아래와 같이 대량 업데이트도 가능합니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

아예 알림을 테이블에서 삭제하려면:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하기 전, Laravel [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 설정이 필요합니다. 이를 통해 JS 프론트엔드에서 서버 측 이벤트에 실시간 반응할 수 있습니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting)을 통해 알림을 외부에 실시간으로 전송합니다. 알림 클래스에서 `toBroadcast` 메서드를 정의하고, `BroadcastMessage`를 반환하세요. 없으면 `toArray` 결과가 사용됩니다.

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

모든 브로드캐스트 알림은 큐에 등록됩니다. 사용 커넥션/큐 명을 설정하려면 `onConnection`, `onQueue` 메서드를 사용하세요:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

브로드캐스트 데이터엔 항상 `type` 필드(알림 클래스 전체 이름)가 포함됩니다. 이 값을 변경하려면 `broadcastType` 메서드를 정의하세요:

```php
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 대기

알림은 `{notifiable}.{id}` 형태의 private 채널에 브로드캐스팅됩니다. 예를 들어, `User` 클래스 id 1 → `App.Models.User.1` 채널.

[Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 사용할 때는 아래와 같이 청취하면 됩니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이징

엔터티별 브로드캐스트 채널명을 커스터마이징하려면 `receivesBroadcastNotificationsOn`을 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    public function receivesBroadcastNotificationsOn(): string
    {
        return 'users.'.$this->id;
    }
}
```

<a name="sms-notifications"></a>
## SMS 알림

<a name="sms-prerequisites"></a>
### 사전 준비

Laravel의 SMS 알림은 [Vonage](https://www.vonage.com/)가 지원합니다. `laravel/vonage-notification-channel`, `guzzlehttp/guzzle` 패키지가 필요합니다.

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

설정 파일 대신, `.env`의 `VONAGE_KEY`, `VONAGE_SECRET`, `VONAGE_SMS_FROM`에 키와 기본 발신번호를 지정하세요.

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

SMS로 보낼 수 있는 알림은 `toVonage` 메서드를 구현하세요. `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환합니다:

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

SMS가 유니코드 문자를 포함할 경우 `unicode` 메서드를 호출하세요:

```php
use Illuminate\Notifications\Messages\VonageMessage;

public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### "From" 번호 커스터마이징

환경변수에 지정한 발신번호 외 다른 번호로 전송하려면 `from` 메서드를 사용하세요:

```php
use Illuminate\Notifications\Messages\VonageMessage;

public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가

Vonage의 "client reference"는 최대 40자까지 가능하며, 사용·팀·클라이언트 단위 비용 추적 등에 활용할 수 있습니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->clientReference((string) $notifiable->id)
        ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

Vonage 알림 대상 지정은 notifiable 엔터티에 `routeNotificationForVonage` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    public function routeNotificationForVonage(Notification $notification): string
    {
        return $this->phone_number;
    }
}
```

<a name="slack-notifications"></a>
## Slack 알림

<a name="slack-prerequisites"></a>
### 사전 준비

Slack 알림을 발송하려면 Composer로 다음 패키지를 설치하세요:

```shell
composer require laravel/slack-notification-channel
```

그리고 [Slack App](https://api.slack.com/apps?new_app=1)을 생성합니다.

같은 워크스페이스 내에서만 알림을 보내도 된다면 `chat:write`, `chat:write.public`, `chat:write.customize` 스코프가 필요합니다. App의 "OAuth & Permissions" 탭에서 추가하고, Bot OAuth 토큰을 config/services.php의 `slack.notifications.bot_user_oauth_token` 항목에 적어주세요.

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### 앱 배포

외부 워크스페이스에도 알림을 보내려면, Slack App을 "배포(Distribute)"해야 하며, [Socialite](/docs/{{version}}/socialite)로 [Slack Bot 토큰](/docs/{{version}}/socialite#slack-bot-scopes)을 얻을 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 알림을 지원하려면 알림 클래스에 `toSlack` 메서드를 정의하고, `Illuminate\Notifications\Slack\SlackMessage`를 반환하세요. [Block Kit API](https://api.slack.com/block-kit)를 활용해 리치 메시지를 만들 수 있습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
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

<a name="using-slacks-block-kit-builder-template"></a>
#### Block Kit 빌더 템플릿 사용

Builder JSON 템플릿을 직접 제공하려면 `usingBlockKitTemplate` 메서드를 사용합니다:

```php
public function toSlack(object $notifiable): SlackMessage
{
    $template = <<<JSON
        {
          "blocks": [
            {
              "type": "header",
              "text": {
                "type": "plain_text",
                "text": "Team Announcement"
              }
            },
            {
              "type": "section",
              "text": {
                "type": "plain_text",
                "text": "We are hiring!"
              }
            }
          ]
        }
    JSON;

    return (new SlackMessage)
        ->usingBlockKitTemplate($template);
}
```

<a name="slack-interactivity"></a>
### Slack 상호작용(Interactivity)

Block Kit을 활용하면 [유저 상호작용](https://api.slack.com/interactivity/handling)을 지원할 수 있습니다. Slack App에서 interactivity와 "Request URL"을 설정하세요. `actionsBlock` 사용 예시:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
// ... (생략) ...
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        // ... (이전 블록)
        ->actionsBlock(function (ActionsBlock $block) {
            $block->button('Acknowledge Invoice')->primary();
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달

버튼 클릭시 확인 모달을 띄우려면 `confirm`을 사용하세요:

```php
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
// ... (생략)
->actionsBlock(function (ActionsBlock $block) {
    $block->button('Acknowledge Invoice')
        ->primary()
        ->confirm(
            'Acknowledge the payment and send a thank you email?',
            function (ConfirmObject $dialog) {
                $dialog->confirm('Yes');
                $dialog->deny('No');
            }
        );
});
```

<a name="inspecting-slack-blocks"></a>
#### Slack 블록 확인하기

`SlackMessage` 객체에서 `dd` 호출 시 Block Kit Builder용 URL을 확인할 수 있습니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 라우팅

notifiable 모델에 `routeNotificationForSlack` 메서드를 정의하면 Slack 알림의 라우팅을 제어할 수 있습니다.

- null: 알림 클래스 내 `to()` 메서드에서 지정한 채널 사용
- 문자열: 채널명(e.g. `#support-channel`)
- SlackRoute 인스턴스: Bot 인증 토큰과 채널 모두 지정 (외부 워크스페이스 전송용)

예시:

```php
public function routeNotificationForSlack(Notification $notification): mixed
{
    return '#support-channel';
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack 워크스페이스 알림

> [!NOTE]
> 외부 워크스페이스 전송 전, Slack App을 [배포](#slack-app-distribution)해야 합니다.

외부 워크스페이스(사용자 소유)로 알림을 보내려면 Socialite의 Slack 드라이버로 사용자의 bot 토큰을 얻고, DB에 저장한 뒤, `SlackRoute::make`로 라우팅하면 됩니다. 사용자가 수신 채널을 선택할 기회를 제공할 수도 있습니다.

```php
public function routeNotificationForSlack(Notification $notification): mixed
{
    return SlackRoute::make($this->slack_channel, $this->slack_token);
}
```

<a name="localizing-notifications"></a>
## 알림 로컬라이징

Laravel에서는 HTTP 요청의 기본 로케일과 다른 언어로 알림을 전송할 수 있으며, 큐에 넣혀도 해당 언어를 유지합니다.

`Illuminate\Notifications\Notification`의 `locale` 메서드로 원하는 언어를 설정하세요:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 알림 대상을 로컬라이징하려면 퍼사드에 `locale`을 체이닝하세요:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 유저 선호 언어 사용

사용자별 선호 언어를 저장한다면, notifiable 모델에 `HasLocalePreference`를 구현하세요:

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

이 인터페이스를 구현하면, Laravel이 자동으로 해당 로케일로 알림·메일을 전송합니다.

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

`Notification` 퍼사드의 `fake` 메서드로 실제 알림 전송을 차단할 수 있습니다. 테스트에서는 Laravel이 알림을 보내도록 지시했는지만 검증하면 됩니다.

예시(Pest):

```php
use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // 주문 처리...

    Notification::assertNothingSent();
    Notification::assertSentTo([$user], OrderShipped::class);
    Notification::assertNotSentTo([$user], AnotherNotification::class);
    Notification::assertCount(3);
});
```

예시(PHPUnit):

```php
namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Notification::fake();

        // 주문 처리...

        Notification::assertNothingSent();
        Notification::assertSentTo([$user], OrderShipped::class);
        Notification::assertNotSentTo([$user], AnotherNotification::class);
        Notification::assertCount(3);
    }
}
```

콜백을 사용해 알림이 특정 조건을 만족할 때만 검증할 수도 있습니다:

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

온디맨드 알림도 `assertSentOnDemand`/`assertNotSentOnDemand`로 검증 가능합니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

콜백을 두 번째 인자로 넘겨 특정 라우팅 정보까지 검증할 수 있습니다:

```php
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
#### 알림 전송 직전 이벤트

알림이 전송되려 할 때, `Illuminate\Notifications\Events\NotificationSending` 이벤트가 발생합니다. 이벤트 리스너를 만들어 알림 전송 과정을 후킹할 수 있습니다.

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

리스너의 `handle`에서 false를 반환하면 전송이 중단됩니다:

```php
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 내부의 `notifiable`, `notification`, `channel` 프로퍼티로 정보를 확인할 수 있습니다.

<a name="notification-sent-event"></a>
#### 알림 전송 후 이벤트

알림이 실제로 전송되면 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발생합니다. 이벤트 리스너 내부에서 `notifiable`, `notification`, `channel`, `response`에 접근할 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

<a name="custom-channels"></a>
## 커스텀 채널

Laravel에는 일부 채널이 내장되어 있으나, 직접 드라이버를 만들어 알림을 다른 방식으로 전달할 수도 있습니다. 우선 `send` 메서드를 가지는 클래스를 하나 생성하세요. `$notifiable`, `$notification`를 인자로 받습니다.

알림 객체에서 원하는 메시지 정보를 추출한 뒤, 마음대로 알림을 전송하면 됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable에게 알림 전송...
    }
}
```

이제 알림 클래스의 `via` 메서드에서 이 커스텀 채널 클래스명을 반환하세요:

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
