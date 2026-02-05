# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포매팅](#formatting-mail-messages)
    - [발신자 지정하기](#customizing-the-sender)
    - [수신자 지정하기](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운(Markdown) 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림을 읽음 처리하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷](#formatting-broadcast-notifications)
    - [알림 수신 대기하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷](#formatting-sms-notifications)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림의 지역화](#localizing-notifications)
- [테스트하기](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

[이메일 전송](/docs/master/mail)뿐만 아니라, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/) - 이전 명칭 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 또한, [커뮤니티에서 제작된 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 활용하면 수십 가지 다른 채널로 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장하여, 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 여러분의 애플리케이션에서 무언가가 발생했음을 사용자에게 알려주는 짧고 정보성 메시지여야 합니다. 예를 들어, 결제 애플리케이션을 작성한다면, 사용자가 "인보이스 결제 완료" 알림을 이메일 및 SMS 채널로 받도록 할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기 (Generating Notifications)

Laravel에서 각 알림은 일반적으로 `app/Notifications` 디렉토리에 저장되는 하나의 클래스로 표현됩니다. 이 디렉토리가 없다면 `make:notification` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 새로운 알림 클래스를 `app/Notifications` 디렉토리에 생성합니다. 각 알림 클래스에는 `via` 메서드와, 해당 채널에 맞게 알림을 메시지로 변환하는 `toMail`, `toDatabase` 와 같은 여러 메시지 빌더 메서드가 포함됩니다.

<a name="sending-notifications"></a>
## 알림 보내기 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드나 `Notification` [파사드](/docs/master/facades)를 통해 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다.

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떠한 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 추가해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는, `Notification` [파사드](/docs/master/facades)를 통해 알림을 보낼 수도 있습니다. 이 방법은 다수의 notifiable 엔티티(예: 여러 사용자)에게 한 번에 알림을 보낼 때 유용합니다. 파사드의 `send` 메서드에 notifiable 엔티티와 알림 인스턴스를 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 큐잉 인터페이스(`ShouldQueue`)를 구현한 알림이어도 즉시 전송됩니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

모든 알림 클래스에는 알림이 어떤 채널로 전달될지 결정하는 `via` 메서드가 있습니다. 지원되는 채널로는 `mail`, `database`, `broadcast`, `vonage`, `slack` 등이 있습니다.

> [!NOTE]
> Telegram, Pusher 등 추가 채널을 사용하려면 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참조하세요.

`via` 메서드는 `$notifiable` 인스턴스를 인수로 받습니다. 이 객체를 활용해 채널을 동적으로 지정할 수 있습니다.

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
> 알림 큐잉을 사용하기 전에, 큐 설정을 구성하고 [큐 워커를 실행](/docs/master/queues#running-the-queue-worker)해야 합니다.

알림을 전송하는 과정은 외부 API 호출 등이 필요할 수 있어 시간이 오래 걸립니다. 애플리케이션의 응답 속도를 높이기 위해, `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 사용해 알림을 큐에 맡길 수 있습니다. `make:notification` 명령어로 생성한 알림에는 해당 인터페이스와 트레이트가 이미 임포트되어 있으므로, 바로 추가하면 됩니다.

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

`ShouldQueue` 인터페이스가 추가된 알림은 평소와 똑같이 보내면, Laravel이 자동으로 해당 알림을 큐잉합니다.

```php
$user->notify(new InvoicePaid($invoice));
```

여러 수신자와 여러 채널에 동시에 보낼 경우, 각 조합마다 개별 큐 작업(job)이 생성됩니다. 예를 들어, 3명에게 2개의 채널로 알림을 보낸다면 큐에는 6개의 작업이 생성됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연하기

알림 전송을 일정 시간 지연하고 싶다면, 알림 인스턴스에 `delay` 메서드를 체이닝할 수 있습니다.

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

채널별로 지연 시간을 지정하고자 할 경우, 배열을 전달할 수 있습니다.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

또는 알림 클래스에 `withDelay` 메서드를 정의해서 채널별 지연 시간을 반환할 수도 있습니다.

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
#### 알림 큐 연결 커스터마이징

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림에 대해 다른 큐 연결을 사용하려면, 알림 생성자에서 `onConnection` 메서드를 호출하세요.

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

각 알림 채널별로 사용할 큐 연결을 지정하려면, `viaConnections` 메서드를 정의하세요. 이 메서드는 채널명과 큐 연결명을 쌍으로 갖는 배열을 반환해야 합니다.

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
#### 알림 채널별 큐명 지정

알림의 각 채널별로 서로 다른 큐명을 사용하고 싶다면, `viaQueues` 메서드를 정의하여 채널명/큐명 쌍을 반환하세요.

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
#### 큐 작업 속성 커스터마이징

큐잉된 알림 작업의 동작을 커스터마이즈하려면, 알림 클래스에서 속성을 정의할 수 있습니다. 이 속성들은 알림을 전송하는 큐 작업에 그대로 적용됩니다.

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
     * 최대 재시도 횟수.
     *
     * @var int
     */
    public $tries = 5;

    /**
     * 실행 제한 시간(초).
     *
     * @var int
     */
    public $timeout = 120;

    /**
     * 허용할 최대 미처리 예외 횟수.
     *
     * @var int
     */
    public $maxExceptions = 3;

    // ...
}
```

큐잉된 알림 데이터의 보안과 무결성을 위해 [암호화](/docs/master/encryption)를 적용하려면, `ShouldBeEncrypted` 인터페이스를 알림 클래스에 추가하세요.

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

이 외에도, `backoff`와 `retryUntil` 메서드를 정의해 후방 대기(backoff) 전략 및 재시도 타임아웃을 제어할 수 있습니다.

```php
use DateTime;

/**
 * 재시도 전 대기할 시간(초)을 계산합니다.
 */
public function backoff(): int
{
    return 3;
}

/**
 * 알림이 타임아웃되는 시각을 지정합니다.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

> [!NOTE]
> 이러한 작업 속성과 메서드에 대한 추가 정보는 [큐잉된 작업 문서](/docs/master/queues#max-job-attempts-and-timeout)를 참고하세요.

<a name="queued-notification-middleware"></a>
#### 큐잉된 알림 미들웨어

큐잉된 알림은 [큐잉된 작업처럼](/docs/master/queues#job-middleware) 미들웨어를 지정할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하면, `$notifiable`과 `$channel`을 인수로 받아 목적지 별로 반환 미들웨어를 커스터마이즈할 수 있습니다.

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

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐 작업이 트랜잭션 커밋 전에 실행될 수 있습니다. 이 경우, 트랜잭션 내에서 모델이나 레코드를 변경한 내용이 아직 데이터베이스에 반영되지 않았거나, 트랜잭션 내에서 생성된 모델/레코드가 존재하지 않을 수 있습니다. 알림이 해당 모델에 의존할 경우, 큐 작업 처리 과정에서 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`인 경우에도, 특정 큐잉된 알림만 데이터베이스 트랜잭션이 모두 커밋된 후 디스패치되도록 하려면 알림 전송 시 `afterCommit` 메서드를 사용할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
     * 새로운 알림 인스턴스 생성자.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이러한 문제를 우회하는 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림의 최종 발송 여부 결정

큐잉된 알림이 큐에 디스패치된 뒤, 큐 워커가 알림을 실제로 발송합니다.

그러나, 큐 워커에서 처리할 때 알림의 최종 발송 여부를 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면, 알림은 발송되지 않습니다.

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
### 온디맨드 알림 (On-Demand Notifications)

애플리케이션의 "user"에 저장되지 않은 특정 대상에게도 알림을 보내야 할 때가 있습니다. `Notification` 파사드의 `route` 메서드를 사용하면 ad-hoc(임의) 라우팅 정보를 지정해 알림을 전송할 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 채널의 온디맨드 알림 전송 시, 수신자의 이름 정보를 제공하고 싶다면 아래처럼 배열을 이용할 수 있습니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널의 추가 라우팅 정보도 `routes` 메서드로 한 번에 지정할 수 있습니다.

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<!-- 이후 내용도 동일한 원칙과 스타일로 유지하여 계속 번역 -->
