# 알림(Notification) (Notifications)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 발송](#sending-notifications)
    - [Notifiable 트레잇 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전달 채널 지정](#specifying-delivery-channels)
    - [알림 큐잉 처리](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 커스터마이즈](#customizing-the-sender)
    - [수신자 커스터마이즈](#customizing-the-recipient)
    - [제목 커스터마이즈](#customizing-the-subject)
    - [메일러 지정](#customizing-the-mailer)
    - [템플릿 커스터마이즈](#customizing-the-templates)
    - [첨부 파일 추가](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비 사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비 사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비 사항](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - ["From" 번호 지정](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림의 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비 사항](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 인터랙션](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스에 알림하기](#notifying-external-slack-workspaces)
- [알림 현지화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

라라벨은 [이메일 발송](/docs/12.x/mail) 기능뿐만 아니라, 여러 종류의 전달 채널을 통해 알림을 보낼 수 있도록 지원합니다. 대표적으로 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/) - 이전 명칭 Nexmo), 그리고 [Slack](https://slack.com) 등이 있습니다. 더불어, [커뮤니티에서 제작된 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 존재하여, 수십 가지의 채널로 알림을 발송할 수 있습니다! 또한, 알림을 데이터베이스에 저장하여 웹 인터페이스에서 사용자에게 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 특정 사건을 사용자에게 알려주는 짧고 정보성 메시지입니다. 예를 들어, 결제 관련 애플리케이션을 개발한다고 가정하면, 사용자가 결제한 인보이스에 대해 "인보이스 결제 완료" 알림을 이메일과 SMS 채널을 통해 보내줄 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성

라라벨에서 알림은 각각 하나의 클래스로 표현되며, 보통 `app/Notifications` 디렉토리에 저장됩니다. 만약 이 디렉토리가 처음에는 없다면 걱정하지 않아도 됩니다. `make:notification` 아티즌 명령어를 실행하면 자동으로 생성됩니다.

```shell
php artisan make:notification InvoicePaid
```

이 명령을 실행하면 새로운 알림 클래스가 `app/Notifications` 디렉토리에 생성됩니다. 각각의 알림 클래스에는 `via` 메서드와, 해당 알림을 각 채널에 맞게 메시지로 변환하는 다양한 메시지 빌더 메서드(`toMail`, `toDatabase` 등)가 포함되어 있습니다.

<a name="sending-notifications"></a>
## 알림 발송

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레잇 사용

알림을 발송하는 방법에는 두 가지가 있습니다. 하나는 `Notifiable` 트레잇의 `notify` 메서드를 사용하는 방법이고, 다른 하나는 `Notification` [파사드](/docs/12.x/facades)를 사용하는 것입니다. `Notifiable` 트레잇은 라라벨 애플리케이션의 기본 `App\Models\User` 모델에 기본적으로 포함되어 있습니다.

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

이 트레잇이 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레잇은 어떤 모델에든 사용할 수 있습니다. 반드시 `User` 모델에서만 사용해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또 다른 방법으로, `Notification` [파사드](/docs/12.x/facades)를 통해 알림을 발송할 수 있습니다. 이 방법은 여러 개의 알림 대상 엔티티(예: 여러 유저)에게 동시에 알림을 보내야 할 때 유용합니다. 파사드를 사용할 때는 모든 알림 대상(노티파이어블 엔티티)와 알림 인스턴스를 `send` 메서드에 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

즉시 알림을 발송하고 싶을 때는 `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하고 있더라도 즉시 발송해 줍니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정

모든 알림 클래스에는 해당 알림이 어떤 채널로 발송될지를 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널 중 하나 또는 여러 개로 보낼 수 있습니다.

> [!NOTE]
> Telegram, Pusher 등 다른 전달 채널을 사용하고 싶다면, 커뮤니티가 주도하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고해 보십시오.

`via` 메서드는 `$notifiable` 인스턴스를 매개변수로 받으며, `$notifiable`은 알림을 받게 될 해당 클래스의 인스턴스입니다. `$notifiable`을 활용하여 어느 채널로 알림을 보낼지 결정할 수 있습니다.

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
### 알림 큐잉 처리

> [!WARNING]
> 알림을 큐에 넣기 전에, 큐 구성을 완료하고 [큐 워커를 실행](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림 발송에는 시간이 걸릴 수 있습니다. 특히, 외부 API 호출을 통해 알림을 전달해야 할 경우 더 그렇습니다. 애플리케이션의 응답 속도를 높이려면, 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레잇을 추가하여 알림을 큐에 넣어 처리할 수 있습니다. 이 인터페이스와 트레잇은 `make:notification` 명령어로 생성된 알림에서는 이미 임포트되어 있으므로, 바로 클래스에 추가해 사용할 수 있습니다.

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

이제 `ShouldQueue` 인터페이스를 알림 클래스에 추가했다면, 기존과 동일하게 알림을 발송할 수 있습니다. 라라벨은 클래스에서 `ShouldQueue` 인터페이스를 감지하여, 자동으로 알림 발송 작업을 큐에 등록합니다.

```php
$user->notify(new InvoicePaid($invoice));
```

알림 큐잉 시, 수신자와 채널의 조합별로 각각 큐 작업이 생성됩니다. 예를 들어, 알림이 3명의 수신자와 2개의 채널을 대상으로 한다면, 총 6개의 작업이 큐에 등록됩니다.

<a name="delaying-notifications"></a>
#### 알림 발송 지연시키기

알림의 발송을 일정 시간 지연하고 싶다면, 알림 인스턴스를 만들 때 `delay` 메서드를 체이닝할 수 있습니다.

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

또는, `delay` 메서드에 배열을 전달하여 각 채널별로 다른 지연 시간을 지정할 수도 있습니다.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

다른 방법으로, 알림 클래스 자체에 `withDelay` 메서드를 정의할 수도 있습니다. 이 메서드는 채널별 지연 시간을 배열로 반환해야 합니다.

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
#### 알림이 사용하는 큐 커넥션 지정

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 특정 알림에 대해 별도의 큐 커넥션을 사용하고 싶다면, 알림의 생성자에서 `onConnection` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

또는, 알림이 지원하는 각 채널별로 사용해야 하는 큐 커넥션을 달리 지정하고 싶다면 `viaConnections` 메서드를 알림 클래스에 정의할 수 있습니다. 이 메서드는 채널명/큐 커넥션명 쌍의 배열을 반환해야 합니다.

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
#### 알림 채널별 큐 이름 지정

알림이 지원하는 언급된 각 채널마다 다른 큐 이름을 지정하고 싶다면, 알림 클래스에 `viaQueues` 메서드를 정의할 수 있습니다. 이 메서드는 채널명/큐 이름 쌍의 배열을 반환합니다.

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
#### 큐잉된 알림의 미들웨어

큐잉된 알림은 [큐 작업처럼 미들웨어](/docs/12.x/queues#job-middleware)를 정의할 수 있습니다. 먼저 알림 클래스에 `middleware` 메서드를 정의하세요. 이 메서드는 `$notifiable`과 `$channel` 변수를 받아, 알림의 목적지에 따라 반환되는 미들웨어를 지정할 수 있습니다.

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
        'mail' => [new RateLimited('postmark')],
        'slack' => [new RateLimited('slack')],
        default => [],
    };
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 큐잉된 알림과 데이터베이스 트랜잭션

큐잉된 알림을 데이터베이스 트랜잭션 내에서 디스패치할 경우, 큐 워커가 데이터베이스 트랜잭션이 커밋되기 전에 해당 알림을 처리할 수 있습니다. 이럴 때라면, 트랜잭션 중 변경한 모델이나 데이터베이스 레코드의 최신 정보가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한, 트랜잭션에서 새로 생성한 모델 혹은 레코드가 데이터베이스에 아직 존재하지 않을 수도 있습니다. 만약 알림이 이러한 모델에 의존한다면, 큐잉된 알림 작업이 처리되는 도중 예상치 못한 에러가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정 옵션이 `false`라면, 알림을 발송할 때 `afterCommit` 메서드를 호출하여, 모든 열린 데이터베이스 트랜잭션이 커밋된 후 큐잉된 알림이 디스패치되도록 할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 알림 생성자 내에서 `afterCommit` 메서드를 호출하는 것도 가능합니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이 문제를 우회하는 더 자세한 방법은 [큐잉 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림의 실제 발송 여부 판단

백그라운드 처리를 위해 큐에 넣은 알림은, 보통 큐 워커가 작업을 받아 실제 수신자에게 전송합니다.

하지만, 큐 워커가 해당 알림을 처리할 때 마지막으로 실제로 알림을 발송해야 할지 직접 판단하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면, 알림은 발송되지 않습니다.

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

때로는 애플리케이션의 "사용자"로 등록되어 있지 않은 사람에게도 알림을 보내야 할 수 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 사용해 임시로 알림 라우팅 정보를 지정한 후 알림을 발송할 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일 라우팅으로 온디맨드 알림을 보낼 때, 수신자의 이름도 함께 지정하고 싶다면, 이메일 주소를 키로, 이름을 값으로 하는 배열을 전달하면 됩니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 알림 채널의 라우팅 정보를 한 번에 지정할 수도 있습니다.

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

알림이 이메일 전송을 지원한다면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인수로 받으며, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션 이메일 메시지를 쉽게 작성할 수 있는 여러 간단한 메서드를 제공합니다. 메일 메시지는 여러 줄의 텍스트와 "행동 유도(call to action)" 버튼을 포함할 수 있습니다. 예시 `toMail` 메서드를 살펴보십시오.

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
> 위 예제에서처럼, `toMail` 메서드 내에서 `$this->invoice->id` 등을 자유롭게 사용할 수 있습니다. 알림에서 메시지를 생성하는 데 필요한 데이터는 생성자를 통해 얼마든지 전달할 수 있습니다.

이 예시에서는 인사말, 텍스트 한 줄, 행동 유도 버튼, 다시 텍스트 한 줄을 차례로 추가하고 있습니다. `MailMessage`가 제공하는 이러한 메서드를 사용하면 짧은 트랜잭션 이메일을 손쉽게 빠르게 작성할 수 있습니다. 이메일 채널은 이렇게 작성된 메시지의 각 구성 요소를 보기 좋은 반응형 HTML 이메일 템플릿(플레인 텍스트 버전 포함)으로 변환해줍니다. 아래는 `mail` 채널로 생성된 실제 이메일 예시입니다.

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때, `config/app.php` 설정 파일의 `name` 옵션 값이 반드시 올바르게 설정되어 있는지 확인하세요. 이 값은 메일 알림 메시지의 헤더 및 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 오류 메시지

일부 알림은 인보이스 결제 실패와 같이 사용자에게 오류를 안내하는 내용을 포함해야 할 수 있습니다. 이럴 때는 메시지 빌드 시 `error` 메서드를 호출해 해당 메일 메시지가 오류 관련 메시지임을 나타낼 수 있습니다. `error` 메서드를 사용하면 ‘Call to Action(행동 유도)’ 버튼이 검정색이 아닌 빨간색으로 표시됩니다.

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
#### 메일 알림 기타 포맷팅 옵션

알림 클래스 안에서 여러 줄의 텍스트를 직접 정의하는 대신, `view` 메서드를 사용해 알림 이메일을 렌더링할 커스텀 템플릿을 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

메일 메시지의 두 번째 배열 요소에 뷰 이름을 지정하면, 플레인 텍스트 뷰를 메일 메시지에 사용할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

메시지가 오직 플레인 텍스트 뷰만 가지고 있다면, `text` 메서드를 사용할 수도 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자 커스터마이즈

기본적으로 메일의 발신 또는 from 주소는 `config/mail.php` 설정 파일에서 정의되어 있습니다. 그러나 특정 알림마다 발신자를 다르게 하고 싶다면, `from` 메서드를 사용할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 커스터마이즈

`mail` 채널을 통해 알림을 보낼 때, 라라벨의 알림 시스템은 알림 대상 엔티티에서 자동으로 `email` 속성을 찾습니다. 알림이 발송될 이메일 주소를 직접 지정하고 싶다면, 알림 대상 엔티티(예: User 모델)에 `routeNotificationForMail` 메서드를 정의하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the mail channel.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // 이메일 주소만 반환할 경우...
        return $this->email_address;

        // 이메일 주소와 이름을 함께 반환할 경우...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이즈

기본적으로 메일의 제목은 알림 클래스의 이름을 "Title Case"로 변환한 값입니다. 예를 들어, 알림 클래스가 `InvoicePaid` 라면 이메일 제목은 `Invoice Paid`가 됩니다. 메시지의 제목을 직접 지정하고 싶다면, 메시지 빌드 시 `subject` 메서드를 호출하면 됩니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 지정

기본적으로 이메일 알림은 `config/mail.php` 설정 파일에 정의된 기본 메일러를 사용합니다. 하지만 이메일을 보낼 때 원하는 메일러를 직접 지정하고 싶다면, 메시지 빌드 시 `mailer` 메서드를 사용하면 됩니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 커스터마이즈

메일 알림이 사용하는 HTML 및 플레인 텍스트 템플릿은 알림 패키지의 리소스를 퍼블리시하여 커스터마이즈할 수 있습니다. 아래 명령어를 실행하면 메일 알림 템플릿이 `resources/views/vendor/notifications` 디렉토리에 생성됩니다.

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부 파일 추가

이메일 알림에 파일을 첨부하려면, 메시지 빌딩 과정에서 `attach` 메서드를 사용하면 됩니다. `attach` 메서드의 첫 번째 매개변수에는 파일의 절대 경로를 지정합니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> 알림용 메일 메시지에서 제공하는 `attach` 메서드는 [attachable 객체](/docs/12.x/mail#attachable-objects)도 사용할 수 있습니다. 자세한 내용은 [attachable 객체 문서](/docs/12.x/mail#attachable-objects)를 참고하세요.

메시지에 파일을 첨부할 때 `attach` 메서드의 두 번째 인수로 배열을 넘기면, 표시 이름 또는 MIME 타입도 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
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

Mailable 객체에서 파일을 첨부할 때처럼, `attachFromStorage`를 사용해 스토리지 디스크에서 파일을 바로 첨부할 수는 없습니다. 반드시 스토리지 디스크에 있는 실제 파일의 절대 경로를 사용해 `attach` 메서드를 사용해야 합니다. 또는, `toMail` 메서드에서 [mailable](/docs/12.x/mail#generating-mailables)을 반환하는 방식도 가능합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

필요에 따라, 여러 파일을 한 번에 첨부하려면 `attachMany` 메서드를 사용합니다.

```php
/**
 * Get the mail representation of the notification.
 */
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

`attachData` 메서드를 사용하면, 바이트 스트림 등 임의의 원시 데이터를 첨부 파일로 추가할 수 있습니다. 이때 첨부될 파일의 파일명을 같이 지정해야 합니다.

```php
/**
 * Get the mail representation of the notification.
 */
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

Mailgun, Postmark와 같은 일부 서드파티 이메일 서비스에서는 메시지에 "태그"와 "메타데이터"를 첨부하여, 애플리케이션에서 발송하는 이메일을 그룹화하고 추적할 수 있습니다. 이메일 메시지에 태그와 메타데이터를 추가하려면 `tag`와 `metadata` 메서드를 사용할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

Mailgun 드라이버를 사용 중이라면, Mailgun 공식 문서에서 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대해 더 자세히 알아볼 수 있습니다. 마찬가지로 Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원 문서도 참고할 수 있습니다.

Amazon SES로 이메일을 발송하는 경우, `metadata` 메서드를 사용해 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 추가할 수 있습니다.

<a name="customizing-the-symfony-message"></a>

### Symfony 메시지 커스터마이징

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 사용하면 메시지를 전송하기 전에 해당 Symfony Message 인스턴스에 클로저를 등록하여, 실제 발송 직전에 메시지를 세밀하게 커스터마이징할 수 있습니다. 이를 통해 메시지가 발송되기 전에 필요한 모든 설정을 직접 조정할 수 있습니다.

```php
use Symfony\Component\Mime\Email;

/**
 * 알림의 메일 표현을 반환합니다.
 */
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
### Mailable 객체 사용하기

필요하다면 알림의 `toMail` 메서드에서 전체 [mailable 객체](/docs/12.x/mail)를 반환할 수도 있습니다. `MailMessage` 대신 `Mailable` 객체를 반환하는 경우, 수신자를 mailable 객체의 `to` 메서드를 사용해서 지정해야 합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailable과 주문형 알림(On-Demand Notifications)

[주문형(on-demand) 알림](#on-demand-notifications)을 전송하는 경우, `toMail` 메서드로 전달되는 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable`의 인스턴스입니다. 이 클래스는 주문형 알림이 전송되어야 할 이메일 주소를 가져오는 데 사용할 수 있는 `routeNotificationFor` 메서드를 제공합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * 알림의 메일 표현을 반환합니다.
 */
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

메일 알림 템플릿을 만들 때, 일반 Blade 템플릿을 브라우저에서 빠르게 미리 볼 수 있다면 편리합니다. 그래서 라라벨은 라우트 클로저나 컨트롤러에서 메일 알림이 생성한 메일 메시지를 직접 반환할 수 있도록 지원합니다. `MailMessage`를 반환하면 해당 알림이 브라우저에서 랜더링되어 실제 이메일로 전송하지 않고도 바로 디자인을 검토할 수 있습니다.

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
## 마크다운(Markdown) 메일 알림

마크다운 메일 알림을 사용하면, 알림 메일의 기본 제공 템플릿을 활용하면서도 좀 더 자유롭게 길고 커스터마이즈된 메시지를 작성할 수 있습니다. 메시지가 마크다운으로 작성되기 때문에, 라라벨은 메시지를 아름답고 반응형인 HTML 템플릿으로 랜더링하며, 동시에 일반 텍스트 버전도 자동으로 생성해줍니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

마크다운 템플릿과 함께 알림을 생성하려면, `make:notification` 아티즌 명령어에 `--markdown` 옵션을 사용할 수 있습니다.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 모든 메일 알림처럼, 마크다운 템플릿을 사용하는 알림도 반드시 알림 클래스 내부에 `toMail` 메서드를 정의해야 합니다. 다만, 알림을 구성할 때는 `line`이나 `action` 대신, 사용할 마크다운 템플릿의 이름을 `markdown` 메서드로 지정합니다. 템플릿에서 사용할 데이터 배열은 두 번째 인수로 전달할 수 있습니다.

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
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

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법을 함께 사용하여 손쉽게 알림 메시지를 작성할 수 있습니다. 이렇게 하면 라라벨이 미리 만들어 둔 알림용 컴포넌트를 최대한 활용하여 효율적으로 알림을 구성할 수 있습니다.

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
> 마크다운 이메일을 작성할 때는 들여쓰기를 과도하게 사용하지 마십시오. 마크다운 표준에 따라, 들여쓰기가 있는 컨텐츠는 코드 블록으로 랜더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 랜더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color` 두 가지 인자를 받습니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 한 알림 내에 여러 개의 버튼 컴포넌트를 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 일반 알림 배경과는 약간 다른 배경색의 패널로 감싸서 보여줍니다. 이를 통해 특정 텍스트 블록에 주목을 유도할 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블로 변환하여 랜더링할 수 있습니다. 이 컴포넌트의 컨텐츠로 마크다운 표를 전달하세요. 표 컬럼 정렬은 기본 마크다운 테이블 정렬 문법을 그대로 지원합니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈

마크다운 알림 컴포넌트들은 여러분의 애플리케이션에 직접 복사하여 원하는 대로 수정할 수 있습니다. 컴포넌트를 내보내려면 `vendor:publish` 아티즌 명령어를 사용해서 `laravel-mail` 에셋 태그를 퍼블리시합니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 `resources/views/vendor/mail` 디렉터리에 마크다운 메일 컴포넌트가 복사됩니다. `mail` 디렉터리에는 각각의 컴포넌트에 대한 `html`과 `text` 디렉터리가 있으며, 각 표현(HTML, 텍스트)별로 파일이 포함되어 있습니다. 이제 이 컴포넌트들을 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보낸 후에는, `resources/views/vendor/mail/html/themes` 디렉터리 내의 `default.css` 파일을 수정할 수 있습니다. 이 파일의 CSS는 자동으로 마크다운 알림의 HTML 버전에 인라인 적용됩니다.

만약 라라벨의 마크다운 컴포넌트를 위한 새로운 테마를 완전히 새로 만들고 싶다면, 해당 디렉터리에 CSS 파일을 추가하면 됩니다. 파일명을 지정하고 저장한 후, `mail` 설정 파일의 `theme` 옵션을 변경하여 새 테마 이름에 맞추면 됩니다.

개별 알림에 대해 다른 테마를 적용하고 싶다면, 알림의 메일 메시지를 생성할 때 `theme` 메서드를 호출하세요. 이 메서드는 전송 시 사용할 테마명을 인자로 받습니다.

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
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

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림의 타입 및 알림을 설명하는 JSON 데이터 구조 등이 기록됩니다.

이 테이블을 쿼리하여 애플리케이션의 사용자 인터페이스에서 알림을 표시할 수 있습니다. 하지만, 그러기 전에 알림을 저장할 데이터베이스 테이블을 먼저 생성해야 합니다. `make:notifications-table` 명령어를 사용하면 테이블 스키마가 포함된 [마이그레이션](/docs/12.x/migrations)을 생성할 수 있습니다.

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 알림 가능한(notifiable) 모델이 [UUID 또는 ULID 기본 키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용한다면, 알림 테이블 마이그레이션에서 `morphs` 메서드 대신 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)를 사용해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷 지정

알림이 데이터베이스에 저장될 수 있도록 하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 순수 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 알림 테이블의 `data` 컬럼에 저장됩니다. 아래는 예시 `toArray` 메서드입니다.

```php
/**
 * 알림의 배열 표현을 반환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

알림이 데이터베이스에 저장되면, `type` 컬럼은 기본적으로 알림 클래스의 이름으로 설정되고, `read_at` 컬럼은 기본적으로 `null`로 저장됩니다. 필요하다면 알림 클래스에서 `databaseType`과 `initialDatabaseReadAtValue` 메서드를 정의하여 이 동작을 커스터마이즈할 수도 있습니다.

```php
use Illuminate\Support\Carbon;

/**
 * 알림의 데이터베이스 타입을 반환합니다.
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * "read_at" 컬럼의 초기값을 반환합니다.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase`와 `toArray`의 차이

`toArray` 메서드는 `broadcast` 채널에서도 사용되어, 자바스크립트 프론트엔드로 브로드캐스트 할 데이터를 결정합니다. 만약 `database` 채널과 `broadcast` 채널에 대해 서로 다른 배열 구조를 원한다면, `toArray` 대신 `toDatabase` 메서드를 정의해야 합니다.

<a name="accessing-the-notifications"></a>
### 알림 조회

알림이 데이터베이스에 저장되었으면, 알림 가능한(notifiable) 엔티티에서 이를 손쉽게 조회할 수 있어야 합니다. 라라벨의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트에는 해당 엔티티의 모든 알림을 반환하는 `notifications` [Eloquent 연관관계](/docs/12.x/eloquent-relationships)가 포함되어 있습니다. 이 메서드는 다른 Eloquent 연관관계처럼 사용할 수 있습니다. 기본적으로 알림들은 `created_at` 기준으로 최신 순으로 정렬되어 반환됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않은(unread)" 알림만 조회하려면, `unreadNotifications` 연관관계를 사용할 수 있습니다. 이 역시 최신순으로 정렬되어 반환됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

"읽은(read)" 알림만 조회하고 싶다면, `readNotifications` 연관관계를 이용하세요.

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림을 조회하려면, 알림 가능한 엔티티(예: 현재 사용자)의 알림 목록을 반환하는 알림 컨트롤러를 작성해야 합니다. 그런 다음, 자바스크립트 클라이언트에서 해당 컨트롤러의 URL로 HTTP 요청을 보내도록 구현하면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림을 읽음 상태로 변경하기

일반적으로 사용자가 알림을 확인한 시점에 알림을 "읽음"으로 표시하길 원할 때가 많습니다. `Illuminate\Notifications\Notifiable` 트레이트에서 제공하는 `markAsRead` 메서드를 사용하면 알림의 데이터베이스 레코드의 `read_at` 컬럼이 업데이트되어 "읽음" 상태가 됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

각 알림을 반복 처리하는 대신, 알림 컬렉션 전체에 대해 바로 `markAsRead` 메서드를 사용할 수도 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

알림들을 데이터베이스에서 조회하지 않고 한 번에 "읽음" 처리하려면, 대량 업데이트 쿼리를 이용할 수도 있습니다.

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 데이터베이스에서 삭제하고 싶다면 `delete`를 사용하세요.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하기 전에 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 먼저 설정하고 숙지해야 합니다. 이벤트 브로드캐스팅은 서버에서 발생하는 라라벨 이벤트에 자바스크립트 프론트엔드가 실시간으로 반응할 수 있도록 해줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷 지정

`broadcast` 채널은 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 이용하여 알림을 실시간으로 자바스크립트 프런트엔드로 전송합니다. 브로드캐스팅을 지원하는 알림 클래스에는 `toBroadcast` 메서드를 정의할 수 있습니다. 이 메서드는 `$notifiable` 엔티티를 받아 `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast` 메서드가 없다면, 브로드캐스트할 데이터는 `toArray` 메서드에서 가져옵니다. 반환된 데이터는 JSON으로 인코딩되어 실시간으로 프런트엔드에 브로드캐스트 됩니다. 아래는 예시입니다.

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 알림의 브로드캐스팅 표현을 반환합니다.
 */
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

모든 브로드캐스트 알림은 큐잉됩니다. 브로드캐스트 작업이 큐잉되는 큐 커넥션 또는 큐 이름을 별도로 지정하고 싶다면 `BroadcastMessage`의 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다.

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이즈

데이터 외에도, 모든 브로드캐스트 알림에는 알림 클래스의 전체 이름이 `type` 필드에 자동으로 포함됩니다. 알림의 `type`을 직접 지정하고 싶다면, 알림 클래스에 `broadcastType` 메서드를 정의하세요.

```php
/**
 * 브로드캐스트하는 알림의 타입을 반환합니다.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 리스닝

알림은 `{notifiable}.{id}` 컨벤션을 사용하여 프라이빗 채널에서 브로드캐스트 됩니다. 예를 들어, `App\Models\User` 인스턴스의 ID가 `1`이라면, 해당 알림은 `App.Models.User.1` 프라이빗 채널에서 전송됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용하면, 채널의 `notification` 메서드로 쉽게 알림을 수신할 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue와 함께 사용하기

Laravel Echo는 React와 Vue를 위한 전용 훅을 제공하여, 알림 리스닝을 매우 쉽게 만들어줍니다. 먼저, 알림을 수신하기 위해 `useEchoNotification` 훅을 사용하면 됩니다. 이 훅은 컴포넌트가 언마운트 될 때 자동으로 채널을 떠나게 됩니다.

```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
</script>
```

기본적으로 이 훅은 모든 알림을 리스닝합니다. 리스닝 하고 싶은 알림 타입을 지정하고 싶다면, 문자열 또는 타입의 배열을 `useEchoNotification`에 전달하면 됩니다.

```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
</script>
```

알림 페이로드의 데이터 형태를 지정할 수도 있어서, 타입 안전성과 개발 편의성을 높일 수 있습니다.

```ts
type InvoicePaidNotification = {
    invoice_id: number;
    created_at: string;
};

useEchoNotification<InvoicePaidNotification>(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.invoice_id);
        console.log(notification.created_at);
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이즈

엔티티의 브로드캐스트 알림을 어떤 채널로 송신할지 직접 커스터마이즈하고 싶다면, 해당 notifiable 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * 사용자가 알림 브로드캐스트를 수신하는 채널을 반환합니다.
     */
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

라라벨에서 SMS 알림 전송은 [Vonage](https://www.vonage.com/) (이전 명칭: Nexmo)에서 지원합니다. Vonage를 통해 알림을 전송하려면, `laravel/vonage-notification-channel` 및 `guzzlehttp/guzzle` 패키지를 설치해야 합니다.

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지에는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있지만, 별도로 해당 파일을 애플리케이션에 복사할 필요는 없습니다. 환경 변수 `VONAGE_KEY`와 `VONAGE_SECRET`를 이용해 Vonage의 공개/비공개 키를 정의하기만 하면 됩니다.

키를 정의한 후에는, SMS 발송 기본 전화번호를 지정하는 `VONAGE_SMS_FROM` 환경 변수도 설정해야 합니다. 이 번호는 Vonage 콘솔에서 생성할 수 있습니다.

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷 지정

알림을 SMS로 전송할 경우, 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아, `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * 알림의 Vonage / SMS 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드(Unicode) 컨텐츠

SMS 메시지에 유니코드 문자가 포함되어 있다면, `VonageMessage` 인스턴스를 생성할 때 `unicode` 메서드를 호출해야 합니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * 알림의 Vonage / SMS 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### "보내는 사람(From)" 번호 커스터마이즈

환경 변수 `VONAGE_SMS_FROM`에 정의된 기본 번호와 다른 번호에서 일부 알림을 전송하고 싶다면, `VonageMessage` 인스턴스에서 `from` 메서드를 사용하면 됩니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * 알림의 Vonage / SMS 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조(Client Reference) 추가

사용자, 팀 또는 클라이언트별로 비용 등을 추적하려면, 알림에 "클라이언트 참조"를 추가할 수 있습니다. Vonage는 이 값을 이용해 특정 사용자의 SMS 사용량을 보고서로 확인할 수 있습니다. 클라이언트 참조는 최대 40자까지 가능한 임의의 문자열입니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * 알림의 Vonage / SMS 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->clientReference((string) $notifiable->id)
        ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

Vonage 알림을 올바른 전화번호로 라우팅하려면, notifiable 엔티티에 `routeNotificationForVonage` 메서드를 정의해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Vonage 채널용 알림 라우팅을 정의합니다.
     */
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

Slack 알림을 전송하기 전에, Composer를 통해 Slack 알림 채널을 먼저 설치해야 합니다.

```shell
composer require laravel/slack-notification-channel
```

또한, Slack 워크스페이스에 [Slack 앱](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

앱이 생성된 워크스페이스에만 알림을 전송한다면, 해당 앱에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한이 필요합니다. 이 권한들은 Slack의 "OAuth & Permissions" 앱 관리 탭에서 추가할 수 있습니다.

그 다음, 앱의 "Bot User OAuth Token"을 복사해서 애플리케이션의 `services.php` 설정 파일 내 `slack` 설정 배열에 넣어야 합니다. 이 토큰은 Slack의 "OAuth & Permissions" 탭에서 확인할 수 있습니다.

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

애플리케이션이 사용자의 소유인 외부 Slack 워크스페이스로 알림을 전송해야 한다면, 앱을 Slack을 통해 "배포(distribute)" 해야 합니다. 앱 배포는 Slack의 "Manage Distribution" 탭에서 관리할 수 있습니다. 앱이 배포되면 [Socialite](/docs/12.x/socialite)를 통해 [Slack Bot 토큰](/docs/12.x/socialite#slack-bot-scopes)을 사용자의 권한으로 획득할 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷 지정

알림이 Slack 메시지로 전송될 경우, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. [Slack의 Block Kit API](https://api.slack.com/block-kit)를 사용해서 다채로운 형태의 알림을 구성할 수 있습니다. 아래 예시는 [Slack의 Block Kit builder](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리 볼 수 있습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * 알림의 Slack 표현을 반환합니다.
 */
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
#### Slack Block Kit 빌더 템플릿 사용

Block Kit 메시지를 플루언트 방식으로 빌드하는 대신, Slack Block Kit 빌더에서 생성된 원본 JSON 페이로드를 `usingBlockKitTemplate` 메서드에 그대로 전달할 수도 있습니다.

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * 알림의 Slack 표현을 반환합니다.
 */
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

### Slack 상호작용

Slack의 Block Kit 알림 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling)를 위한 강력한 기능을 제공합니다. 이 기능들을 사용하려면, Slack 앱에서 "Interactivity(상호작용)"를 활성화하고, 애플리케이션에서 서비스하는 URL을 "Request URL"에 설정해야 합니다. 이 설정들은 Slack에서 "Interactivity & Shortcuts" 앱 관리 탭에서 관리할 수 있습니다.

아래 예시는 `actionsBlock` 메서드를 사용하고 있으며, 사용자가 버튼을 클릭하면 Slack은 "Request URL"로 Slack 사용자 정보, 클릭된 버튼의 ID 등 다양한 정보를 포함한 페이로드를 담아 `POST` 요청을 보냅니다. 애플리케이션은 이 페이로드를 기반으로 적절한 작업을 결정할 수 있습니다. 또한 [이 요청이 Slack에서 온 것인지 검증](https://api.slack.com/authentication/verifying-requests-from-slack)하는 절차도 거쳐야 합니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * 알림의 Slack 표현을 반환합니다.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('귀하의 인보이스 중 하나가 결제되었습니다!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('인보이스가 결제되었습니다.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
             // ID는 기본값으로 "button_acknowledge_invoice"가 할당됩니다...
            $block->button('Acknowledge Invoice')->primary();

            // ID를 수동으로 지정합니다...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인(Confirmation) 모달

사용자가 특정 작업을 수행하기 전에 반드시 확인하도록 요구하고 싶다면, 버튼 정의 시 `confirm` 메서드를 사용할 수 있습니다. `confirm` 메서드는 메시지와, `ConfirmObject` 인스턴스를 받는 클로저를 인수로 받습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * 알림의 Slack 표현을 반환합니다.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('귀하의 인보이스 중 하나가 결제되었습니다!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('인보이스가 결제되었습니다.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
            $block->button('Acknowledge Invoice')
                ->primary()
                ->confirm(
                    '결제를 승인하고 감사 메일을 보낼까요?',
                    function (ConfirmObject $dialog) {
                        $dialog->confirm('네');
                        $dialog->deny('아니오');
                    }
                );
        });
}
```

<a name="inspecting-slack-blocks"></a>
#### Slack 블록 미리보기

구성한 블록을 빠르게 확인하고 싶다면, `SlackMessage` 인스턴스에서 `dd` 메서드를 호출할 수 있습니다. `dd` 메서드는 Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/)로 바로 연결되는 URL을 생성하여, 브라우저에서 페이로드와 알림 미리보기를 확인할 수 있도록 합니다. 또한 `dd` 메서드에 `true`를 전달하면 원본 페이로드를 바로 덤프할 수 있습니다.

```php
return (new SlackMessage)
    ->text('귀하의 인보이스 중 하나가 결제되었습니다!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 올바른 Slack 팀 및 채널로 전송하려면, 알림 대상 모델에 `routeNotificationForSlack` 메서드를 정의해야 합니다. 이 메서드는 아래 세 가지 값 중 하나를 반환할 수 있습니다.

- `null` - 이 경우 알림 템플릿에 설정된 채널로 라우팅을 위임합니다. `SlackMessage` 작성 시 `to` 메서드를 이용해 알림 내에서 채널을 지정할 수 있습니다.
- 알림을 전송할 Slack 채널을 지정하는 문자열. 예: `#support-channel`.
- `SlackRoute` 인스턴스. 이를 통해 OAuth 토큰과 채널명을 명시할 수 있습니다. 예: `SlackRoute::make($this->slack_channel, $this->slack_token)` (외부 워크스페이스로 알림을 보낼 때 사용).

예를 들어, `routeNotificationForSlack` 메서드에서 `#support-channel`을 반환하면 애플리케이션의 `services.php` 설정 파일에 등록된 Bot User OAuth 토큰에 연결된 워크스페이스의 해당 채널로 알림이 전송됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Slack 채널로 알림을 라우팅합니다.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return '#support-channel';
    }
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack 워크스페이스 알림 보내기

> [!NOTE]
> 외부 Slack 워크스페이스로 알림을 보내기 전, Slack 앱이 [배포(distributed)](#slack-app-distribution)되어 있어야 합니다.

실제 애플리케이션에서는 여러 사용자가 소유한 Slack 워크스페이스로 알림을 보내야 할 때가 많습니다. 이때 사용자의 Slack OAuth 토큰을 먼저 획득해야 합니다. 다행히 [Laravel Socialite](/docs/12.x/socialite)는 Slack 드라이버를 지원하므로, 애플리케이션 사용자를 Slack에 쉽게 인증시키고 [봇 토큰을 획득](/docs/12.x/socialite#slack-bot-scopes)할 수 있습니다.

봇 토큰을 획득하여 애플리케이션 데이터베이스에 저장한 뒤, `SlackRoute::make` 메서드를 사용해 알림을 사용자의 워크스페이스로 라우팅할 수 있습니다. 추가로, 보통 사용자가 어느 채널로 알림을 받을지 선택할 수 있도록 애플리케이션에서 UI를 제공해야 할 것입니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;
use Illuminate\Notifications\Slack\SlackRoute;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Slack 채널로 알림을 라우팅합니다.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림의 다국어화(Localizing Notifications)

라라벨에서는 알림을 현재 HTTP 요청의 로케일(locale)이 아닌 다른 로케일로 보낼 수 있으며, 심지어 알림이 큐에 등록되었더라도 해당 로케일을 기억합니다.

이를 위해, `Illuminate\Notifications\Notification` 클래스의 `locale` 메서드를 이용해 원하는 언어를 지정할 수 있습니다. 알림이 전송되는 동안에는 지정한 로케일이 활성화되며, 처리가 끝나면 원래 로케일로 되돌아갑니다.

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 알림 대상에 대한 다국어화를 위해서는 `Notification` 파사드에서도 사용할 수 있습니다.

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일 적용

애플리케이션이 각 사용자별로 선호하는 로케일을 저장하는 경우도 많습니다. 알림 대상 모델에서 `HasLocalePreference` 계약(Contract)을 구현하면, 사용자가 설정한 로케일로 알림을 전송하도록 라라벨에 지시할 수 있습니다.

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자가 선호하는 로케일을 반환합니다.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면, 라라벨은 자동으로 해당 모델에 대한 알림 및 메일 발송 시 선호 로케일을 사용합니다. 따라서 이 경우에는 `locale` 메서드를 별도로 호출할 필요가 없습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

알림이 실제로 전송되지 않도록 막으려면 `Notification` 파사드의 `fake` 메서드를 사용하면 됩니다. 보통 테스트하려는 로직과 알림을 실제로 전송하는 일은 별개이므로, 라라벨에서 특정 알림을 전송하도록 "지시"했는지만 확인해도 충분할 때가 많습니다.

`Notification::fake()`를 호출한 후에는, 알림이 특정 사용자에게 전송되었는지 여부뿐만 아니라, 전송 시 전달된 데이터까지도 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // 주문 발송 작업 수행...

    // 알림이 전혀 전송되지 않았는지 확인...
    Notification::assertNothingSent();

    // 지정한 사용자에게 알림이 전송되었는지 확인...
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // 알림이 전송되지 않았는지 확인...
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // 총 알림 전송 건수가 맞는지 확인...
    Notification::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Notification::fake();

        // 주문 발송 작업 수행...

        // 알림이 전혀 전송되지 않았는지 확인...
        Notification::assertNothingSent();

        // 지정한 사용자에게 알림이 전송되었는지 확인...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 알림이 전송되지 않았는지 확인...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 총 알림 전송 건수가 맞는지 확인...
        Notification::assertCount(3);
    }
}
```

`assertSentTo` 혹은 `assertNotSentTo` 메서드에 클로저를 전달하여, 알림이 특정 조건을 만족하는지 검증할 수도 있습니다. 하나 이상의 알림이 해당 조건을 통과하면 어서션은 성공하며, 이 방법으로 다양한 진위 테스트를 작성할 수 있습니다.

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드(동적) 알림 테스트

테스트 중인 코드가 [온디맨드 알림](#on-demand-notifications)을 전송하는 경우, `assertSentOnDemand` 메서드를 이용해 해당 알림이 전송되었는지 테스트할 수 있습니다.

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` 메서드의 두 번째 인수로 클로저를 전달하면, 온디맨드 알림이 정확한 "라우트" 주소로 전송되었는지 추가로 검사할 수 있습니다.

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
#### 알림 전송 시점 이벤트

알림이 전송되는 순간, 알림 시스템에서는 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 발생합니다. 이 이벤트에는 "알림 대상"(notifiable) 엔티티와 알림 인스턴스 자체가 전달됩니다. 애플리케이션에서 이 이벤트를 위한 [이벤트 리스너](/docs/12.x/events)를 작성할 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * 이벤트 처리 메서드
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

리스너의 `handle` 메서드에서 `false`를 반환하면, 해당 알림은 실제로 전송되지 않습니다.

```php
/**
 * 이벤트 처리 메서드
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 리스너에서는 이벤트의 `notifiable`, `notification`, `channel` 속성을 참조하여, 수신 대상이나 알림 자체 정보를 확인할 수 있습니다.

```php
/**
 * 이벤트 처리 메서드
 */
public function handle(NotificationSending $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
#### 알림 전송 완료 이벤트

알림이 실제로 전송된 후에는 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)가 발생합니다. 이 역시 "알림 대상" 엔티티 및 알림 인스턴스를 담고 있습니다. 애플리케이션에서 이 이벤트를 위한 [이벤트 리스너](/docs/12.x/events)를 만들어 사용할 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * 이벤트 처리 메서드
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

이벤트 리스너 안에서는 `notifiable`, `notification`, `channel`, 그리고 `response` 속성을 통해 알림의 수신 대상 및 알림 자체에 대한 다양한 정보를 참조할 수 있습니다.

```php
/**
 * 이벤트 처리 메서드
 */
public function handle(NotificationSent $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```

<a name="custom-channels"></a>
## 커스텀 채널(Custom Channels)

라라벨에는 여러 가지 기본 알림 채널이 내장되어 있지만, 원하는 경우 자체 드라이버를 만들어 다양한 방식으로 알림을 전달할 수도 있습니다. 라라벨에서는 이를 매우 쉽게 구현할 수 있습니다. 우선, `send` 메서드를 포함한 클래스를 하나 정의하세요. 이 메서드는 `$notifiable`과 `$notification` 두 개의 인수를 받습니다.

`send` 메서드 내부에서, 알림 객체의 메서드를 호출하여 해당 채널에서 사용 가능한 메시지 객체를 반환받고, 원하는 방식으로 `$notifiable` 인스턴스에 알림을 전송하면 됩니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 지정된 알림을 전송합니다.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable 인스턴스에 알림을 전송...
    }
}
```

커스텀 알림 채널 클래스를 정의한 뒤에는, 원하는 알림의 `via` 메서드에서 해당 클래스명을 반환하면 됩니다. 아래 예시처럼 알림의 `toVoice` 메서드는 음성 메시지를 나타내는 임의의 객체(예: `VoiceMessage` 클래스)를 반환하도록 정의할 수 있습니다.

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

    /**
     * 알림 채널을 반환합니다.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * 알림의 음성 표현을 반환합니다.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```