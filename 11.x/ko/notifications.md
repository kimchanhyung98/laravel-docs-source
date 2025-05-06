# 알림(Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐 처리하기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 지정하기](#customizing-the-sender)
    - [수신자 지정하기](#customizing-the-recipient)
    - [제목 지정하기](#customizing-the-subject)
    - [메일러 지정하기](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그와 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
    - [메일러블 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [DB 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [DB 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림 읽음 표시](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 리스닝](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - [발신 번호 지정](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [슬랙 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [슬랙 알림 포맷팅](#formatting-slack-notifications)
    - [슬랙 인터렉티비티](#slack-interactivity)
    - [슬랙 알림 라우팅](#routing-slack-notifications)
    - [외부 슬랙 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림 현지화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[이메일 전송](/docs/{{version}}/mail) 지원 외에도, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 또한 커뮤니티에서 구축한 [다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 개가 넘는 다양한 채널로 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장되어 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 짧고 정보성 메시지로, 애플리케이션 내에서 발생한 사건을 사용자에게 알리는 용도입니다. 예를 들어, 청구서 결제 애플리케이션을 개발 중이라면 이메일 및 SMS 채널을 통해 사용자의 "청구서 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 하나의 클래스로 표현되며, 일반적으로 `app/Notifications` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, 아래의 Artisan 명령어로 자동 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령은 새로운 알림 클래스를 `app/Notifications` 디렉터리에 생성합니다. 각 알림 클래스는 `via` 메서드와 `toMail`, `toDatabase` 등과 같은 다양한 메시지 빌딩 메서드를 포함하고 있으며, 이 메서드들은 해당 채널에 맞는 메시지로 알림을 변환합니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, `Notification` [파사드](/docs/{{version}}/facades)를 사용해 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인자로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 모든 모델에 사용할 수 있습니다. 반드시 `User` 모델에만 한정되지 않습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는, `Notification` [파사드](/docs/{{version}}/facades)를 통해 알림을 보낼 수도 있습니다. 이 방법은 여러 명의 Notifiable 엔티티(예: 유저 컬렉션)에게 동시에 알림을 보낼 때 유용합니다. 파사드를 사용할 때는, Notifiable 엔티티들과 알림 인스턴스를 `send` 메서드에 전달합니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 알림이 즉시 전송됩니다(알림이 `ShouldQueue` 인터페이스를 구현하고 있더라도 즉시 전송함):

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

모든 알림 클래스에는 알림이 어떤 채널로 전송될지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 전송할 수 있습니다.

> [!NOTE]
> Telegram, Pusher 등 다른 채널을 사용하려면 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 받으며, 이를 이용해 알림을 어느 채널로 보낼지 결정할 수 있습니다:

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
### 알림 큐 처리하기

> [!WARNING]
> 알림을 큐 처리하기 전에 큐를 설정하고 [워커를 시작](/docs/{{version}}/queues#running-the-queue-worker)해야 합니다.

알림을 보내는 데 시간이 걸릴 수 있는데, 특히 외부 API를 통해 전송하는 경우엔 더욱 그렇습니다. 애플리케이션 응답 속도를 높이기 위해, 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해 큐로 처리할 수 있습니다. 이 인터페이스와 트레이트는 `make:notification` 명령어로 생성하는 모든 알림에 이미 import되어 있으므로, 바로 사용할 수 있습니다:

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

이제 `ShouldQueue` 인터페이스가 추가된 알림을 평소처럼 보내면 Laravel이 자동으로 큐에 넣어 전송을 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

큐 처리 시, 각 수신자 및 채널 조합마다 하나의 큐 작업(Job)이 생성됩니다. 예를 들면, 3명의 수신자와 2개의 채널이 있다면 6개의 작업이 큐에 dispatch됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연시키기

알림 전송을 지연하려면, 알림 인스턴스에 `delay` 메서드를 체이닝하세요:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널마다 지연 시간을 다르게 하고 싶다면, `delay` 메서드에 배열을 전달할 수 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스 자체에 `withDelay` 메서드를 정의할 수도 있습니다:

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

기본적으로 큐 알림은 애플리케이션의 기본 큐 연결(connection)을 사용합니다. 특정 알림에서 큐 연결을 변경하려면, 알림의 생성자에서 `onConnection` 메서드를 호출하면 됩니다:

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

알림 채널마다 큐 연결을 지정하려면 `viaConnections` 메서드를 정의하면 됩니다:

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

알림 채널별로 사용할 큐 이름을 바꾸고 싶다면 `viaQueues` 메서드를 정의할 수 있습니다:

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
#### 큐 알림 미들웨어

큐로 처리되는 알림에도 [작업 용 미들웨어](/docs/{{version}}/queues#job-middleware)처럼 미들웨어를 정의할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하면 되고, `$notifiable`과 `$channel`을 인자로 받아 목적지에 맞게 미들웨어를 커스터마이즈 할 수 있습니다:

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
#### 큐 알림과 DB 트랜잭션

큐 알림을 데이터베이스 트랜잭션 내에서 dispatch하면, 트랜잭션 커밋 전에 큐 워커가 알림을 처리할 수 있습니다. 이 경우 트랜잭션 중에 수정된 모델이나 DB 레코드는 아직 커밋이 안됐으므로, 알림에서 그런 데이터를 참고할 시 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`라면, 알림 전송 시 `afterCommit` 메서드를 호출해 트랜잭션 커밋 이후로 알림 dispatch를 지정할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 생성자에서 호출할 수도 있습니다:

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
> 이 이슈에 대한 자세한 내용은 [큐 작업과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림 전송 여부 결정하기

큐 알림이 워커에서 처리될 때, 실제로 알림을 전송할지 여부를 마지막에 결정할 수 있습니다. 알림 클래스에 `shouldSend` 메서드를 정의하면, 이 메서드가 `false`를 반환할 경우 알림은 전송되지 않습니다:

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

때때로 “User” 모델이 아닌 임의 대상에게 알림을 보내야 할 수 있습니다. 이 경우 `Notification` 파사드의 `route` 메서드를 사용해 알림 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일 라우트에 수신자 이름을 추가하고 싶다면, 이메일 주소를 key로, 이름을 value로 하는 배열을 전달하면 됩니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 채널의 라우팅 정보를 한 번에 지정할 수 있습니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

---

*아래의 추가 번역(메일 알림, 마크다운 알림, DB 알림, SMS, 슬랙, 테스트 등)도 요청하실 경우 이어서 상세히 번역해 드릴 수 있습니다. 혹은 필요한 일부만 요청해주셔도 됩니다.*