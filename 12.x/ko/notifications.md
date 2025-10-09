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
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 객체 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
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
    - [외부 Slack 워크스페이스에 알림 전송](#notifying-external-slack-workspaces)
- [알림 현지화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

[이메일 전송](/docs/12.x/mail) 지원 외에도, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통해 알림을 전송하는 기능을 제공합니다. 또한 [커뮤니티에서 제작한 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 마련되어 있어 수십 가지 다른 채널로 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션에서 발생한 사건을 사용자에게 알리는 짧고 간단한 정보성 메시지여야 합니다. 예를 들어, 청구 애플리케이션을 개발한다면 "결제 완료" 알림을 이메일과 SMS 채널을 통해 사용자에게 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성 (Generating Notifications)

Laravel에서 각각의 알림은 보통 `app/Notifications` 디렉토리에 저장되는 하나의 클래스로 표현됩니다. 만약 이 디렉토리를 아직 본 적이 없더라도 걱정하지 마세요. `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 `app/Notifications` 디렉토리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스에는 `via` 메서드와, 해당 채널에 맞는 메시지로 변환해주는 `toMail`, `toDatabase` 등 여러 메시지 빌더 메서드가 포함될 수 있습니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 `Notifiable` 트레이트의 `notify` 메서드, 또는 `Notification` [파사드](/docs/12.x/facades)를 사용해 보낼 수 있습니다. `Notifiable` 트레이트는 애플리케이션의 기본 `App\Models\User` 모델에 기본적으로 포함되어 있습니다:

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

이 트레이트에서 제공하는 `notify` 메서드에는 알림 인스턴스를 전달해야 합니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 꼭 `User` 모델에서만 사용할 필요는 없습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는, `Notification` [파사드](/docs/12.x/facades)를 통해 여러 개의 Notifiable 엔티티에 알림을 동시에 전송할 때 유용합니다. 파사드의 `send` 메서드에 Notifiable 엔티티와 알림 인스턴스를 전달하면 알림이 전송됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

알림을 즉시 전송하려면 `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현해도 즉시 전송됩니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스에는 알림이 어느 채널로 전달될지 결정하는 `via` 메서드가 포함되어 있습니다. 지원되는 전송 채널로는 `mail`, `database`, `broadcast`, `vonage`, `slack` 등이 있습니다.

> [!NOTE]
> Telegram이나 Pusher 등 다른 채널을 사용하고 싶다면 커뮤니티에서 제공하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 알림이 전송되는 클래스의 인스턴스인 `$notifiable`을 인자로 받습니다. `$notifiable`을 활용하여 알림이 어떤 채널로 전송될지 동적으로 지정할 수 있습니다:

```php
/**
 * 알림의 전송 채널을 반환
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
> 알림을 큐잉하기 전에, 반드시 큐 설정 및 [작업자 실행](/docs/12.x/queues#running-the-queue-worker)을 완료하세요.

알림 전송에는 시간이 소요될 수 있으며, 특히 외부 API를 호출해야 할 경우 더욱 그렇습니다. 애플리케이션의 응답 속도를 높이기 위해, `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 추가하여 알림을 큐에 넣을 수 있습니다. `make:notification` 명령어로 생성한 알림에는 이미 이 인터페이스와 트레이트가 임포트되어 있으므로, 바로 사용할 수 있습니다:

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

`ShouldQueue` 인터페이스를 추가한 후에는 기존처럼 알림을 전송하면 됩니다. Laravel이 자동으로 이 인터페이스를 감지하여 큐를 통해 알림을 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐잉하면, 수신자와 채널 조합마다 하나의 큐 작업이 생성됩니다. 예를 들어 수신자가 3명이고 채널이 2개면 총 6개의 작업이 큐에 생성됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연 전송

알림 전송을 지연하고 싶다면, 알림 인스턴스에서 `delay` 메서드를 체이닝하면 됩니다:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 지연 시간을 지정하고 싶다면, `delay` 메서드에 배열을 전달하세요:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스 내에 `withDelay` 메서드를 정의할 수도 있습니다. 이 메서드는 채널명과 지연 값을 반환하는 배열을 리턴해야 합니다:

```php
/**
 * 알림 지연 시간을 반환
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
#### 알림 큐 커넥션 커스터마이징

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 특정 알림에 다른 큐 커넥션을 사용하려면, 알림의 생성자에서 `onConnection` 메서드를 호출하세요:

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
     * 새로운 알림 인스턴스 생성
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

또는, 각 알림 채널마다 사용할 큐 커넥션을 지정하고 싶다면 `viaConnections` 메서드를 정의할 수 있습니다. 이 메서드는 채널명과 큐 커넥션명을 매핑한 배열을 반환해야 합니다:

```php
/**
 * 각 알림 채널별 큐 커넥션 반환
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
#### 알림 채널별 큐 커스터마이징

각 알림 채널별로 사용할 큐명을 지정하려면, `viaQueues` 메서드를 알림 클래스에 정의하세요. 이 메서드는 채널명과 큐명 쌍의 배열을 반환해야 합니다:

```php
/**
 * 각 알림 채널별 큐명을 반환
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

알림 클래스 내에 여러 속성을 정의하여, 큐잉된 작업의 동작을 커스터마이징할 수 있습니다. 이 속성들은 실제로 알림을 전송하는 큐 작업에 상속됩니다:

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
     * 알림 시도 횟수
     *
     * @var int
     */
    public $tries = 5;

    /**
     * 타임아웃 시간(초)
     *
     * @var int
     */
    public $timeout = 120;

    /**
     * 실패 허용 예외 최대 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    // ...
}
```

큐잉된 알림 데이터의 보안과 무결성을 [암호화](/docs/12.x/encryption)로 보장하려면, 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요:

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

이 속성들을 직접 정의하는 것 외에도, `backoff`와 `retryUntil` 메서드를 정의해 작업의 재시도 대기 및 제한 시간을 지정할 수 있습니다:

```php
use DateTime;

/**
 * 재시도 전 대기 시간(초)를 계산
 */
public function backoff(): int
{
    return 3;
}

/**
 * 알림 타임아웃 시각을 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

> [!NOTE]
> 위 작업 속성 및 메서드에 대한 자세한 내용은 [큐잉된 작업](/docs/12.x/queues#max-job-attempts-and-timeout) 문서를 참고하세요.

<a name="queued-notification-middleware"></a>
#### 큐잉된 알림 미들웨어

큐잉된 알림 역시 [큐 작업과 같이](/docs/12.x/queues#job-middleware) 미들웨어를 지정할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하세요. 이 메서드는 `$notifiable`과 `$channel` 변수를 받아, 목적지에 따라 미들웨어를 동적으로 반환할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 알림 작업이 거치는 미들웨어 반환
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

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치 될 경우, 큐가 트랜잭션 커밋 전에 작업을 처리할 수 있습니다. 이 경우 데이터베이스에 완전히 반영되지 않은 모델이나 레코드를 참조할 수 있으니 주의해야 합니다. 알림이 해당 모델을 의존하면 예상치 못한 에러가 발생할 수 있습니다.

`after_commit` 설정이 `false`인 경우에도, 알림을 전송할 때 `afterCommit` 메서드를 호출하여 반드시 모든 오픈된 트랜잭션 커밋 이후에 디스패치되도록 지정할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스의 생성자에서 바로 `afterCommit`을 호출할 수도 있습니다:

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
     * 새로운 알림 인스턴스 생성
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이 문제에 대한 자세한 해결 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 전송 여부 결정

백그라운드에서 알림이 큐잉되어 큐 작업자가 수신자에게 알림을 전송합니다. 단, 큐 작업 처리 시점에 실제로 알림을 전송할지 최종 판단이 필요하다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림이 전송되지 않습니다:

```php
/**
 * 알림 전송 여부 결정
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림 (On-Demand Notifications)

가끔, 애플리케이션의 "유저"로 저장되어 있지 않은 대상에게도 알림을 보내야 할 수 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드로 임시 라우팅 정보를 지정한 후 알림을 전송할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 경로로 온디맨드 알림 전송 시 수신자명을 지정하려면, 이메일 주소와 이름을 키-값 쌍으로 담은 배열을 작성하세요:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

또한 `routes` 메서드를 사용하면 여러 채널의 라우팅 정보를 한 번에 제공할 수 있습니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```
