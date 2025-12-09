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
    - [발신자 지정](#customizing-the-sender)
    - [수신자 지정](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [메일러블 사용](#using-mailables)
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
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [발신번호 커스터마이징](#customizing-the-from-number)
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

[이메일 전송](/docs/12.x/mail) 지원 외에도, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 또한, [커뮤니티가 제작한 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 가지의 다른 채널로 알림을 보낼 수도 있습니다! 알림은 데이터베이스에 저장해 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 사건을 사용자에게 전달하는 짧고 정보성 메시지여야 합니다. 예를 들어, 결제 관련 애플리케이션을 개발 중이라면, "인보이스 결제 완료" 알림을 사용자에게 이메일과 SMS 채널로 발송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성 (Generating Notifications)

Laravel에서 각 알림은 보통 `app/Notifications` 디렉터리에 저장되는 단일 클래스로 표현됩니다. 해당 디렉터리가 없다면, `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 `app/Notifications` 디렉터리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스는 `via` 메서드와, 특정 채널에 적합한 메시지를 만드는 `toMail` 또는 `toDatabase`와 같은 여러 메시지 빌더 메서드를 포함합니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 `Notifiable` 트레이트의 `notify` 메서드 또는 `Notification` [파사드](/docs/12.x/facades)를 사용해 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떠한 모델에도 사용할 수 있습니다. 꼭 `User` 모델에만 한정할 필요는 없습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는 `Notification` [파사드](/docs/12.x/facades)를 사용해 알림을 보낼 수도 있습니다. 이 방식은 여러 개의 노티파이어블 엔티티(예: 여러 사용자)에게 동시에 알림을 보낼 때 유용합니다. 파사드의 `send` 메서드에 모든 노티파이어블 엔티티와 알림 인스턴스를 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 알림이 즉시 전송됩니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하고 있더라도 즉시 전송합니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스는 알림 전송 채널을 결정하는 `via` 메서드를 갖고 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 전송할 수 있습니다.

> [!NOTE]
> Telegram 또는 Pusher와 같은 다른 전송 채널을 사용하려면 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 알림이 전송될 대상 클래스의 인스턴스인 `$notifiable`을 받습니다. `$notifiable` 변수를 활용해 어떤 채널로 알림을 전송할지 동적으로 결정할 수 있습니다:

```php
/**
 * 알림의 전송 채널 반환.
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
> 알림을 큐에 등록하려면 우선 큐 설정을 완료하고, [작업자(worker)를 실행](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림 전송에는 시간이 소요될 수 있으며, 특히 외부 API 호출이 필요한 경우 더 그렇습니다. 애플리케이션의 응답 속도를 개선하려면, 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해 알림을 큐에 등록하세요. 이 두 개는 `make:notification` 명령어로 생성한 모든 알림에서 이미 임포트되어 있으므로 바로 적용할 수 있습니다:

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

`ShouldQueue` 인터페이스를 알림에 추가한 후에는 평소처럼 알림을 보내면 됩니다. Laravel은 해당 클래스에 `ShouldQueue`가 구현된 것을 감지해 자동으로 알림 전송 작업을 큐잉 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림이 큐에 등록될 때, 각각의 수신자-채널 조합마다 큐 작업이 하나씩 생성됩니다. 예를 들어, 수신자가 3명이고 채널이 2개라면 총 6개의 작업이 큐에 등록됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연 전송

알림 전송을 일정 시간 지연시키려면, 알림 인스턴스에 `delay` 메서드를 체이닝하면 됩니다:

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널 별로 지연 시간을 지정하려면, 배열을 전달하면 됩니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

또는, 알림 클래스 자체에 `withDelay` 메서드를 정의할 수도 있습니다. 이 메서드는 채널명과 지연 값을 반환합니다:

```php
/**
 * 알림 전송 지연 시간 반환.
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
#### 알림 큐 연결 커스터마이징

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림에 대해 다른 큐 연결을 사용하려면 알림의 생성자에서 `onConnection` 메서드를 호출하면 됩니다:

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
     * 새 알림 인스턴스 생성자.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

혹은, 알림이 지원하는 각 채널별로 사용할 큐 연결을 지정하려면 `viaConnections` 메서드를 정의하세요. 이 메서드는 채널명/큐 연결명 쌍의 배열을 반환해야 합니다:

```php
/**
 * 각 알림 채널별 사용할 연결 반환.
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

알림이 지원하는 각 채널별로 사용할 큐명을 지정하려면 `viaQueues` 메서드를 정의할 수 있습니다. 이 메서드는 채널명/큐명 쌍의 배열을 반환해야 합니다:

```php
/**
 * 각 알림 채널별 사용할 큐 반환.
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
#### 큐잉 알림 작업 속성 커스터마이징

알림 클래스에 속성을 정의함으로써 큐잉된 작업의 동작을 세밀하게 제어할 수 있습니다. 이러한 속성은 실제로 알림을 전송하는 큐 작업에 상속됩니다:

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
     * 알림 시도 횟수.
     *
     * @var int
     */
    public $tries = 5;

    /**
     * 알림 처리 타임아웃(초).
     *
     * @var int
     */
    public $timeout = 120;

    /**
     * 실패 허용 예외 최대 개수.
     *
     * @var int
     */
    public $maxExceptions = 3;

    // ...
}
```

큐잉된 알림 데이터의 보안 및 무결성을 보장하려면, 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요:

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

또한, 알림 클래스에 `backoff` 및 `retryUntil` 메서드를 추가하여 재시도 간격 및 타임아웃 전략을 세밀하게 지정할 수 있습니다:

```php
use DateTime;

/**
 * 재시도 전 대기 시간(초) 반환.
 */
public function backoff(): int
{
    return 3;
}

/**
 * 알림 타임아웃 시점 반환.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

> [!NOTE]
> 이러한 작업 속성 및 메서드에 대한 자세한 내용은 [큐잉 작업 문서](/docs/12.x/queues#max-job-attempts-and-timeout)를 참고하세요.

<a name="queued-notification-middleware"></a>
#### 큐잉 알림 미들웨어

큐잉된 알림도 [큐 작업과 동일하게 미들웨어](/docs/12.x/queues#job-middleware)를 정의할 수 있습니다. `middleware` 메서드를 알림 클래스에 정의하면, `$notifiable`과 `$channel` 변수를 받아 목적지에 따라 반환할 미들웨어를 커스터마이징할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 알림 작업 미들웨어 반환.
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
#### 큐잉 알림과 데이터베이스 트랜잭션

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치될 경우, 큐 작업이 트랜잭션 커밋 전 실행될 수 있습니다. 이 경우, 트랜잭션 중에 저장된 모델이나 레코드의 변경사항이 아직 데이터베이스에 적용되지 않을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델이나 레코드는 데이터베이스에 존재하지 않을 수도 있습니다. 만약 알림 메시지가 이 모델들에 의존한다면, 의도치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`인 경우에도, 알림을 보낼 때 `afterCommit` 메서드를 호출하여 모든 열린 트랜잭션이 커밋된 후에만 큐잉된 알림을 디스패치할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 알림 클래스 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다:

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
     * 새 알림 인스턴스 생성자.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이러한 문제를 우회하는 방법에 대해 더 알고 싶다면 [큐잉 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉 알림이 실제로 전송될지 여부 결정

알림이 백그라운드 큐에 디스패치된 후에는 일반적으로 큐 워커가 수신자를 대상으로 알림을 전송합니다.

하지만, 큐 워커에서 처리 중 실제로 알림을 전송해야 할지 마지막으로 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림은 전송되지 않습니다:

```php
/**
 * 알림 전송 여부 결정.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림

가끔 애플리케이션에 저장되어 있지 않은 사용자에게 알림을 보내야 할 수도 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 사용하면 즉석에서 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

온디맨드 메일 알림을 보낼 때 수신자의 이름까지 지정하고 싶다면, 배열 형태로 이메일주소=>이름을 지정할 수 있습니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 이용하면 여러 채널에 대한 라우팅 정보를 한 번에 지정할 수 있습니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

(이하, 마찬가지로 규칙에 따라 하위 항목 번역이 이어집니다)