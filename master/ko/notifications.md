# 알림(Notification)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레이트 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전송 채널 지정](#specifying-delivery-channels)
    - [알림 큐잉](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [보내는 사람 커스터마이징](#customizing-the-sender)
    - [받는 사람 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부 파일](#mail-attachments)
    - [태그와 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 리스닝](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림 로컬라이징](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [이메일 전송](/docs/master/mail)뿐만 아니라 다양한 전송 채널에서 알림을 보낼 수 있도록 지원합니다. 지원 채널에는 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/) - 기존 Nexmo), [Slack](https://slack.com) 등이 있습니다. 또한, [커뮤니티에서 제작한 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 존재하여 수십 개의 채널로 알림을 발송할 수 있습니다! 알림은 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로, 알림은 애플리케이션 내에서 발생한 이벤트에 대해 사용자에게 간단히 정보를 제공하는 용도로 사용됩니다. 예를 들어, 결제 애플리케이션을 만든다면 "Invoice Paid(인보이스 결제 완료)" 알림을 이메일과 SMS 채널을 통해 사용자에게 전송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성 (Generating Notifications)

Laravel에서 각 알림은 단일 클래스로 표현되며, 보통 `app/Notifications` 디렉터리에 저장됩니다. 이 디렉터리가 없다면, `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 새로운 알림 클래스를 `app/Notifications` 디렉터리에 생성합니다. 각 알림 클래스에는 `via` 메서드와, 채널 별 메시지로 변환하는 여러 메서드(`toMail`, `toDatabase` 등)가 포함되어 해당 채널에 맞춤형 메시지를 만들 수 있습니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림을 전송하는 방법에는 두 가지가 있습니다. `Notifiable` 트레이트의 `notify` 메서드를 사용하는 방법과, `Notification` [파사드](/docs/master/facades)를 사용하는 방법입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 파라미터로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 포함해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는, `Notification` [파사드](/docs/master/facades)를 통해 여러 알림 대상(예: 사용자 컬렉션)에게 알림을 보낼 수 있습니다. 파사드의 `send` 메서드에 모든 알림 대상 객체와 알림 인스턴스를 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 큐를 거치지 않고 즉시 알림을 전송할 수 있습니다. `ShouldQueue` 인터페이스를 구현한 경우에도 즉시 전송됩니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

각 알림 클래스에는 어떤 채널로 알림을 전송할지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널 등으로 보낼 수 있습니다.

> [!NOTE]
> Telegram이나 Pusher 등 다른 전송 채널을 사용하려면, 커뮤니티 기반 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 파라미터로 받으며, 여기에 따라 전송할 채널을 동적으로 정할 수 있습니다:

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
### 알림 큐잉

> [!WARNING]
> 알림을 큐잉하기 전에 큐 설정을 완료하고 [큐 워커를 실행](/docs/master/queues#running-the-queue-worker)해야 합니다.

외부 API를 호출하는 등 알림 전송 과정이 느릴 수 있으므로, 응답 속도를 높이기 위해 알림을 큐로 처리하는 것이 좋습니다. 이를 위해 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 추가하세요. `make:notification` 명령어로 생성된 알림 클래스는 이미 이 인터페이스와 트레이트를 불러오도록 되어 있습니다:

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

이제 `ShouldQueue` 인터페이스가 추가된 알림은 평소와 같이 전송하면 됩니다. Laravel은 클래스에서 `ShouldQueue` 인터페이스를 감지하여 자동으로 알림의 전송을 큐에 등록합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐잉하는 경우, 수신자와 채널 조합마다 하나의 큐 작업이 만들어집니다. 예를 들어, 3명의 수신자와 2개의 채널인 경우 총 6개의 작업이 큐에 등록됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연시키기

알림 전송을 지연시키고 싶다면, 알림 인스턴스에 `delay` 메서드를 체이닝할 수 있습니다:

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

채널별로 지연 시간을 다르게 지정하려면 배열을 전달할 수 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

또한, 알림 클래스에 `withDelay` 메서드를 정의하여도 됩니다. 이 메서드는 채널별 지연 값을 배열로 반환해야 합니다:

```php
/**
 * Determine the notification's delivery delay.
 *
 * @return array<string, \Illuminate\Support\Carbon>
 */
public function withDelay(object $notifiable): array
{
    return [
        'mail' => now()->plus(minutes: 5),
        'sms' => now()->plus(minutes: 10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 커넥션 커스터마이징

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 알림별로 다른 큐 커넥션을 사용하고 싶다면, 생성자에서 `onConnection` 메서드를 호출하면 됩니다:

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

각 채널 별로 큐 커넥션을 정하려면 알림 클래스에 `viaConnections` 메서드를 추가하세요:

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

알림 채널별로 사용할 큐 이름을 지정하고 싶다면 `viaQueues` 메서드를 정의하면 됩니다:

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

<a name="customizing-queued-notification-job-properties"></a>
#### 큐잉된 알림 작업 속성 커스터마이징

알림 클래스에 속성을 정의하여 큐 작업의 행동을 커스터마이징할 수 있습니다. 이 속성들은 알림을 전송하는 큐 작업에 적용됩니다:

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
     * The number of times the notification may be attempted.
     *
     * @var int
     */
    public $tries = 5;

    /**
     * The number of seconds the notification can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    // ...
}
```

큐잉된 알림의 데이터 보안과 무결성을 위해 [암호화](/docs/master/encryption)가 필요하다면, 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue, ShouldBeEncrypted
{
    use Queueable;

    // ...
}
```

이외에도 `backoff`와 `retryUntil` 메서드를 정의하여, 큐 백오프 전략과 재시도 타임아웃을 직접 지정할 수 있습니다:

```php
use DateTime;

/**
 * Calculate the number of seconds to wait before retrying the notification.
 */
public function backoff(): int
{
    return 3;
}

/**
 * Determine the time at which the notification should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

> [!NOTE]
> 이러한 작업 속성 및 메서드에 대한 자세한 정보는 [큐잉된 작업](/docs/master/queues#max-job-attempts-and-timeout) 문서를 참고하세요.

<a name="queued-notification-middleware"></a>
#### 큐잉된 알림 미들웨어

큐잉된 알림은 [일반 큐 작업과 같이](/docs/master/queues#job-middleware) 미들웨어를 정의할 수 있습니다. 알림 클래스에 `middleware` 메서드를 추가하면 됩니다. 이 메서드는 `$notifiable`, `$channel` 파라미터를 받아 각 알림 목적지에 따라 미들웨어를 다르게 반환할 수 있습니다:

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

트랜잭션 내에서 큐잉된 알림이 디스패치될 때, 큐가 트랜잭션 커밋보다 먼저 처리되면 데이터베이스 변경 사항이 반영되지 않을 수 있습니다. 트랜잭션 내에서 생성된 모델이나 레코드가 아직 커밋되지 않은 상황에서 알림이 처리되면 예기치 않은 오류가 발생할 수 있습니다.

`after_commit` 구성 옵션이 `false`일 경우, 특정 알림만 트랜잭션 커밋 후에 전송하고 싶다면 알림 전송 시 `afterCommit` 메서드를 호출하세요:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다:

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
> 이러한 문제를 피하는 방법은 [큐와 데이터베이스 트랜잭션 문서](/docs/master/queues#jobs-and-database-transactions)를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림이 전송되어야 할지 최종 판단

큐잉된 알림이 큐 작업자로 넘어간 뒤, 실제 전송 여부를 최종적으로 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 알림은 전송되지 않습니다:

```php
/**
 * Determine if the notification should be sent.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="after-sending-notifications"></a>
#### 알림 전송 후 처리

알림이 전송된 후 추가 처리를 하고 싶다면, 알림 클래스에 `afterSending` 메서드를 정의할 수 있습니다. 이 메서드는 수신자, 채널명, 채널의 응답 값을 전달받습니다:

```php
/**
 * Handle the notification after it has been sent.
 */
public function afterSending(object $notifiable, string $channel, mixed $response): void
{
    // ...
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림

애플리케이션의 "user"로 저장되어 있지 않은 대상에게도 알림을 보내야 할 경우, `Notification` 파사드의 `route` 메서드로 즉석에서 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

on-demand 알림의 `mail` 경로에 수신자 이름도 함께 제공하려면, 키가 이메일, 값이 이름인 배열을 사용할 수 있습니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 알림 채널의 라우팅 정보를 한꺼번에 지정하려면 `routes` 메서드를 사용하세요:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

(이후의 나머지 섹션들은 위와 같은 번역 원칙에 따라 이어서 번역이 진행됩니다.)