# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
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
    - [메일러블 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비 사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림을 읽음으로 표시](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비 사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비 사항](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [슬랙 알림](#slack-notifications)
    - [사전 준비 사항](#slack-prerequisites)
    - [슬랙 알림 포맷팅](#formatting-slack-notifications)
    - [슬랙 인터랙티비티](#slack-interactivity)
    - [슬랙 알림 라우팅](#routing-slack-notifications)
    - [외부 슬랙 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림 현지화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[이메일 발송](/docs/12.x/mail) 기능에 더해, 라라벨은 다양한 전달 채널을 통해 알림을 보낼 수 있도록 지원합니다. 예를 들어, 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 과거 Nexmo), [Slack](https://slack.com) 등이 있습니다. 이외에도 다양한 [커뮤니티에서 제작한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 가지 종류의 채널로 알림을 전달할 수도 있습니다! 또한 웹 인터페이스에서 표시할 수 있도록 알림을 데이터베이스에 저장할 수도 있습니다.

일반적으로 알림은 애플리케이션에서 발생한 어떤 일을 사용자에게 짧고 간단하게 알려주는 정보성 메시지여야 합니다. 예를 들어, 결제 관련 애플리케이션을 작성한다면, 사용자의 이메일 및 SMS를 통해 "청구서 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

라라벨에서 각 알림은 하나의 클래스로 표현되며, 보통 `app/Notifications` 디렉터리에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없다면 걱정하지 마십시오. `make:notification` 아티즌 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어를 실행하면 새로운 알림 클래스가 `app/Notifications` 디렉터리에 생성됩니다. 각 알림 클래스에는 `via` 메서드와, 해당 채널에 맞춘 메시지를 생성하기 위한 메서드(`toMail`, `toDatabase` 등)가 들어 있습니다. 이 메서드들은 알림을 해당 채널에 맞는 메시지로 변환합니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림을 보내는 방법에는 두 가지가 있습니다. 첫 번째는 `Notifiable` 트레이트의 `notify` 메서드를 사용하는 것이고, 두 번째는 `Notification` [파사드](/docs/12.x/facades)를 이용하는 것입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받아 처리합니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 한정해서 사용할 필요가 없습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는, `Notification` [파사드](/docs/12.x/facades)를 이용해서 알림을 보낼 수도 있습니다. 이 방법은 여러 명의 수신자, 예를 들어 사용자 컬렉션에 한 번에 알림을 보낼 때 유용합니다. 파사드를 사용할 때는, 모든 수신자와 알림 인스턴스를 `send` 메서드에 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

즉시 알림을 보내고 싶다면 `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하고 있어도 즉시 알림을 발송합니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

모든 알림 클래스는 `via` 메서드를 가지고 있으며, 이 메서드에서 어떤 채널을 통해 알림을 보낼지 결정합니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 등의 채널로 발송할 수 있습니다.

> [!NOTE]
> Telegram이나 Pusher와 같은 추가 채널을 사용하고 싶다면, 커뮤니티에서 운영하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하십시오.

`via` 메서드는 `$notifiable` 인스턴스를 전달받는데, 이는 알림이 전송될 대상 클래스의 인스턴스입니다. 이를 활용해 어떤 채널로 알림을 보낼지 동적으로 결정할 수 있습니다:

```php
/**
 * 알림의 전달 채널을 반환합니다.
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
> 알림을 큐잉하기 전에, 먼저 큐를 설정하고 [큐 워커를 실행](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림 발송 작업은 시간이 오래 걸릴 수 있습니다. 특히 외부 API 호출이 필요한 채널로 발송할 때 그렇습니다. 애플리케이션의 응답 속도를 높이기 위해, 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해서 알림을 큐에 넣을 수 있습니다. 이 인터페이스와 트레이트는 `make:notification` 명령어로 생성되는 알림 클래스라면 이미 임포트되어 있으므로, 바로 추가해서 사용할 수 있습니다:

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

`ShouldQueue` 인터페이스를 알림 클래스에 추가하면, 평소처럼 알림을 보내도 라라벨이 이 인터페이스를 감지하여 알림 발송을 자동으로 큐에 넣어 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림이 큐에 등록될 때는, 수신자와 채널의 조합마다 각각 하나의 큐 작업이 생성됩니다. 예를 들어, 세 명의 수신자와 두 개의 채널에 알림을 보내는 경우, 총 6개의 작업이 큐에 등록됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연시키기

알림 발송을 특정 시간만큼 지연시키고 싶다면, 알림 인스턴스 생성 시 `delay` 메서드를 체이닝해서 사용할 수 있습니다.

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

각 채널마다 지연 시간을 다르게 지정하려면, `delay` 메서드에 배열을 전달하면 됩니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는, 알림 클래스에 `withDelay` 메서드를 직접 정의해도 됩니다. 이 메서드는 채널 이름과 지연 시간을 배열로 반환해야 합니다:

```php
/**
 * 알림별 전송 지연 시간을 결정합니다.
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

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 연결(커넥션)을 이용해 처리됩니다. 특정 알림에서만 다르게 연결을 지정하고 싶다면, 알림 클래스의 생성자에서 `onConnection` 메서드를 호출하세요:

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
        $this->onConnection('redis');
    }
}
```

또한, 각 알림 채널마다 별도의 큐 연결(커넥션)을 지정하고 싶다면, 알림 클래스에 `viaConnections` 메서드를 정의하면 됩니다. 이 메서드는 채널명/큐 커넥션명 쌍으로 구성된 배열을 반환해야 합니다:

```php
/**
 * 각 알림 채널별로 사용할 큐 연결을 결정합니다.
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

각 알림 채널마다 사용할 큐(Queue)를 별도로 지정하고 싶다면, 알림 클래스에 `viaQueues` 메서드를 정의하면 됩니다. 이 메서드는 채널명/큐명 쌍으로 이루어진 배열을 반환해야 합니다:

```php
/**
 * 각 알림 채널별로 사용할 큐 이름을 결정합니다.
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

큐잉된 알림도 [큐 작업과 동일하게 미들웨어](/docs/12.x/queues#job-middleware)를 정의할 수 있습니다. 시작하려면, 알림 클래스에 `middleware` 메서드를 정의하세요. 이 메서드는 `$notifiable`과 `$channel` 변수를 받아, 알림의 목적지에 따라 반환할 미들웨어를 맞춤 설정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 알림 작업이 거쳐야 할 미들웨어를 반환합니다.
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

큐잉된 알림이 데이터베이스 트랜잭션 내부에서 디스패치될 경우, 큐 워커가 데이터베이스 트랜잭션이 커밋되기 전에 해당 알림 작업을 처리할 수 있습니다. 이렇게 되면 트랜잭션 중 변경된 모델이나 데이터베이스 레코드가 아직 데이터베이스에 반영되지 않은 상태에서 알림이 발송될 수 있습니다. 또한, 트랜잭션 내부에서 새로 생성된 모델이나 레코드도 존재하지 않을 수 있습니다. 알림이 이런 모델을 필요로 한다면, 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정 옵션이 `false`라면, 해당 알림을 모든 열린 데이터베이스 트랜잭션 커밋 후에 디스패치하도록 `afterCommit` 메서드를 사용해 명시할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 알림 클래스의 생성자 안에서 `afterCommit` 메서드를 호출해도 됩니다:

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
> 이런 문제를 우회하는 방법에 대해 더 알아보고 싶다면, [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림의 실제 전송 여부 결정하기

큐잉된 알림이 백그라운드에서 큐로 디스패치된 후, 보통은 큐 워커가 작업을 받아 최종 수신자에게 알림을 전송하게 됩니다.

하지만, 큐 워커에서 알림을 처리한 후 실제로 전송할지 여부를 최종적으로 직접 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림은 전송되지 않습니다:

```php
/**
 * 알림을 전송할지 여부를 결정합니다.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림

때때로, 애플리케이션의 "user"로 저장되지 않은 사람에게 알림을 보내야 할 수 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 사용하여 임의의 알림 라우팅 정보를 지정한 뒤 알림을 전송할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 라우트로 온디맨드 알림을 보내는 경우, 수신자의 이름 정보를 함께 지정하고 싶다면, 이메일 주소를 키로 하고 이름을 값으로 하는 배열을 첫 번째 요소로 전달할 수 있습니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 개의 알림 채널에 대해 임의 라우팅 정보를 한 번에 지정하려면, `routes` 메서드를 사용하세요:

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

알림을 이메일로 보낼 수 있도록 지원하려면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 전달받으며, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션성(거래성) 이메일 메시지를 쉽게 만들 수 있도록 몇 가지 간단한 메서드를 제공합니다. 메일 메시지는 텍스트 라인과 "call to action(행동 유도)" 버튼을 포함할 수 있습니다. 다음은 `toMail` 메서드의 예시입니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
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
> 위 예시의 `toMail` 메서드에서 `$this->invoice->id`를 사용한 것을 볼 수 있습니다. 알림에서 필요한 모든 데이터는 알림의 생성자를 통해 전달할 수 있습니다.

이 예제에서는 인사말, 본문 텍스트 한 줄, 행동 유도 버튼, 그리고 또 다른 텍스트 한 줄을 등록했습니다. `MailMessage` 객체가 제공하는 이 메서드들을 사용하면, 작은 트랜잭션성 이메일을 빠르고 손쉽게 포맷할 수 있습니다. mail 채널은 여기서 등록한 메시지 요소들을 깔끔하고 반응형인 HTML 이메일 템플릿(그리고 그에 대응하는 일반 텍스트 메일)로 변환합니다. 다음은 `mail` 채널로 생성된 이메일 예시입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때, `config/app.php` 파일의 `name` 설정 값을 반드시 지정하세요. 이 값은 메일 알림 메시지의 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 오류 메시지

일부 알림은 실패한 청구서 결제와 같이 사용자에게 오류 상황을 알려줍니다. 이럴 때는 메시지 생성 시 `error` 메서드를 호출해 메일 메시지가 오류 상황임을 표시할 수 있습니다. `error` 메서드를 사용하면, 행동 유도 버튼의 색상이 검정 대신 빨간색으로 변경됩니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
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
#### 기타 메일 알림 포맷팅 옵션

알림 클래스 내부에서 텍스트 라인을 직접 정의하는 대신, `view` 메서드를 이용해 커스텀 템플릿을 지정하여 알림 이메일을 렌더링할 수도 있습니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

`view` 메서드에 배열을 전달하면, 메일 메시지의 일반 텍스트 뷰도 함께 지정할 수 있습니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

만약 메시지가 일반 텍스트 뷰만 가진다면, `text` 메서드를 사용할 수도 있습니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자 커스터마이징

기본적으로 이메일의 발신자(From) 주소는 `config/mail.php` 설정 파일에 정의되어 있습니다. 단, 특정 알림에서만 별도의 발신자를 지정하고 싶다면 `from` 메서드를 사용하세요:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 커스터마이징

`mail` 채널로 알림을 전송할 때, 알림 시스템은 기본적으로 수신자 엔터티의 `email` 속성을 참조합니다. 다른 이메일 주소를 사용하고 싶다면, 수신자 엔터티에 `routeNotificationForMail` 메서드를 정의하면 됩니다:

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
     * mail 채널로 알림을 라우팅합니다.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // 이메일 주소만 반환하는 경우...
        return $this->email_address;

        // 이메일 주소와 이름을 함께 반환하는 경우...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 이메일 제목은 알림 클래스명을 "타이틀 케이스"로 변환한 값입니다. 예를 들어, 알림 클래스명이 `InvoicePaid`라면 제목은 `Invoice Paid`가 됩니다. 다른 제목을 사용하고 싶다면 메시지 생성 시 `subject` 메서드를 호출하면 됩니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 커스터마이징

기본적으로 이메일 알림은 `config/mail.php`에 정의된 기본 메일러로 전송됩니다. 하지만 실행 시점에 다른 메일러를 지정하고 싶다면, 메시지 생성 시 `mailer` 메서드를 호출하면 됩니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 커스터마이징

메일 알림에서 사용되는 HTML 및 일반 텍스트 템플릿은 notification 패키지의 리소스를 퍼블리시(publish)해서 수정할 수 있습니다. 해당 명령어를 실행하면 메일 알림 템플릿이 `resources/views/vendor/notifications` 경로에 생성됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

이메일 알림에 첨부파일을 추가하려면, 메시지 생성 시 `attach` 메서드를 사용하세요. `attach` 메서드의 첫 번째 인수로는 파일의 절대 경로를 지정해야 합니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> 알림 메일 메시지의 `attach` 메서드는 [attachable 객체](/docs/12.x/mail#attachable-objects)도 지원합니다. 자세한 내용은 [attachable 객체 문서](/docs/12.x/mail#attachable-objects)를 참고하세요.

첨부파일을 추가하면서 표시될 이름이나 MIME 타입을 지정하려면, `attach` 메서드의 두 번째 인수로 배열을 전달하면 됩니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
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

메일러블(mailable) 객체에서처럼 스토리지 디스크에서 직접 파일을 첨부하는(`attachFromStorage`) 방식은 알림에서는 사용할 수 없습니다. 대신, 파일의 절대 경로를 활용한 `attach` 메서드를 사용해야 하며, 필요하다면 `toMail` 메서드에서 [메일러블](/docs/12.x/mail#generating-mailables)을 반환하는 방법도 있습니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

여러 개의 파일을 첨부하려면, `attachMany` 메서드를 사용하세요:

```php
/**
 * 알림의 메일 표현을 반환합니다.
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

`attachData` 메서드를 사용하면, 문자열 형태의 바이너리 데이터를 첨부파일로 추가할 수 있습니다. 이때 첨부파일로 쓰일 파일명을 반드시 지정해야 합니다:

```php
/**
 * 알림의 메일 표현을 반환합니다.
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

Mailgun, Postmark와 같은 외부 이메일 서비스에서는 이메일을 그룹화/추적할 수 있는 "태그" 및 "메타데이터" 기능을 지원합니다. 이메일 메시지에 태그와 메타데이터를 추가하려면, `tag` 및 `metadata` 메서드를 활용하세요:

```php
/**
 * 알림의 메일 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

Mailgun 드라이버를 사용하는 경우, 더 자세한 정보는 Mailgun 문서의 [태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1), [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) 항목을 참고하세요. 마찬가지로, Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원에 대한 공식 문서를 참고하실 수도 있습니다.

Amazon SES를 이용해 이메일을 전송하는 경우, `metadata` 메서드를 활용해 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>

### Symfony 메시지 커스터마이징

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 사용하면, 메시지를 발송하기 전에 Symfony Message 인스턴스를 전달받아 클로저에서 원하는 대로 커스터마이징할 수 있습니다. 이 방법을 이용하면, 메시지가 실제로 전송되기 전에 다양한 방식으로 메시지를 세밀하게 조정할 수 있습니다.

```php
use Symfony\Component\Mime\Email;

/**
 * Get the mail representation of the notification.
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
### Mailable 사용하기

필요하다면, 알림(Notification)의 `toMail` 메서드에서 [mailable 객체](/docs/12.x/mail)를 전체적으로 반환할 수도 있습니다. 만약 `MailMessage` 대신 `Mailable`을 반환할 경우, mailable 객체의 `to` 메서드를 사용해 수신자를 지정해야 합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailable과 온디맨드(On-Demand) 알림

[온디맨드 알림](#on-demand-notifications)을 발송하는 경우, `toMail` 메서드에 전달되는 `$notifiable` 객체는 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스입니다. 이 객체는 온디맨드 알림을 보낼 이메일 주소를 알아내기 위한 `routeNotificationFor` 메서드를 제공합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
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

메일 알림 템플릿을 설계할 때, Blade 템플릿처럼 렌더링된 메일 메시지를 브라우저에서 바로 미리 볼 수 있다면 매우 편리합니다. 이를 위해, 라라벨에서는 알림에서 생성된 메일 메시지를 라우트 클로저나 컨트롤러에서 바로 반환할 수 있도록 지원합니다. `MailMessage`를 반환하면, 해당 메시지는 브라우저에서 렌더링되어 실제 이메일 주소로 전송하지 않아도 디자인을 빠르게 확인할 수 있습니다.

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

마크다운(Markdown) 기반 메일 알림을 사용하면, 라라벨이 제공하는 기본 템플릿의 장점을 누리면서, 더 긴 내용이나 자유로운 커스터마이징이 가능합니다. 메시지를 마크다운으로 작성하면, 라라벨이 보기 좋고 반응형인 HTML 템플릿과 자동으로 생성되는 플레인 텍스트 버전을 함께 만들어줍니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

마크다운 템플릿을 사용하는 알림을 생성하고 싶다면, Artisan의 `make:notification` 명령어에서 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 메일 알림과 마찬가지로, 마크다운 템플릿을 사용하는 알림 클래스에도 반드시 `toMail` 메서드를 정의해야 합니다. 다만, 알림을 만들 때 `line`이나 `action` 메서드 대신, 사용할 마크다운 템플릿의 이름을 `markdown` 메서드로 지정합니다. 템플릿에 전달할 데이터가 있다면 두 번째 인수로 배열을 전달하면 됩니다.

```php
/**
 * Get the mail representation of the notification.
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

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법을 조합해 사용할 수 있습니다. 이를 통해, 라라벨이 미리 만들어놓은 다양한 알림 컴포넌트를 손쉽게 활용하며 알림 메시지를 작성할 수 있습니다.

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
> 마크다운 이메일을 작성할 때는 들여쓰기를 과도하게 사용하지 마세요. 마크다운 표준에 따라, 들여쓰기된 내용은 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color` 인자를 받을 수 있습니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 하나의 알림 메시지에 여러 개의 버튼 컴포넌트를 추가할 수도 있습니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 일반 알림 내용과 다른 색 배경이 적용된 패널 안에 보여줍니다. 이를 통해 강조하고 싶은 특정 내용에 시선을 집중시킬 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 마크다운 표 문법으로 작성한 표를 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 표 내용을 인자로 받으며, 마크다운 표 문법의 열 정렬 기능도 지원합니다.

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

마크다운 알림 컴포넌트 전체를 내 애플리케이션으로 내보내서 직접 수정할 수도 있습니다. 컴포넌트를 내보내려면, `vendor:publish` Artisan 명령어에서 `laravel-mail` 에셋 태그를 지정해 실행하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉토리에 복사됩니다. `mail` 폴더 안에는 `html`와 `text` 폴더가 있으며, 각각의 폴더에 각 컴포넌트의 HTML/텍스트 버전이 포함되어 있습니다. 이 컴포넌트 파일들은 원하는 대로 자유롭게 수정이 가능합니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보낸 후에는, `resources/views/vendor/mail/html/themes` 디렉토리에 위치한 `default.css` 파일을 수정하여 CSS를 변경할 수 있습니다. 이 파일의 스타일은 자동으로 마크다운 알림의 HTML 결과물에 인라인(inline) 형태로 적용됩니다.

라라벨의 마크다운 컴포넌트용으로 완전히 새로운 테마를 제작하고 싶다면, 직접 만든 CSS 파일을 `html/themes` 디렉토리에 추가하면 됩니다. 새로 만든 CSS 파일의 이름을 기억해두었다가, `mail` 설정 파일의 `theme` 옵션에 파일 이름을 등록하면 해당 테마가 적용됩니다.

특정 알림에만 별도의 테마를 적용하고 싶다면, 알림 메시지 빌드 시에 `theme` 메서드를 호출해 사용하려는 테마 이름을 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
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

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 타입과 알림에 대한 설명을 포함한 JSON 데이터 구조가 저장됩니다.

이 테이블에서 데이터를 조회하여 애플리케이션의 UI에 알림을 표시할 수 있습니다. 그 전에, 알림을 담을 데이터베이스 테이블을 먼저 생성해야 합니다. `make:notifications-table` 명령어를 사용하면 적절한 테이블 스키마가 있는 [마이그레이션](/docs/12.x/migrations) 파일을 바로 생성할 수 있습니다.

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 알림 대상을 나타내는 모델이 [UUID 또는 ULID 기본 키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용한다면, 알림 테이블 마이그레이션에서 `morphs` 메서드 대신 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)를 사용해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

알림을 데이터베이스 테이블에 저장하고 싶다면, 알림 클래스에서 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받아서, 결과를 평범한 PHP 배열로 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 아래는 예시 `toArray` 메서드입니다.

```php
/**
 * Get the array representation of the notification.
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

알림이 데이터베이스에 저장되면, `type` 컬럼에는 알림 클래스명이 기본적으로 기록되고, `read_at` 컬럼은 기본값으로 `null`이 들어갑니다. 이 동작을 변경하려면, 알림 클래스에서 `databaseType`과 `initialDatabaseReadAtValue` 메서드를 직접 정의할 수 있습니다.

```php
use Illuminate\Support\Carbon;

/**
 * Get the notification's database type.
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * Get the initial value for the "read_at" column.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs. `toArray`

`toArray` 메서드는 `broadcast` 채널에서도 전달할 데이터를 결정할 때 사용됩니다. 만약 `database` 채널과 `broadcast` 채널에서 서로 다른 구조의 배열이 필요하다면, `toArray` 대신 `toDatabase` 메서드를 따로 정의하시기 바랍니다.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

알림이 데이터베이스에 저장된 후에는, 알림 대상 엔티티에서 손쉽게 해당 알림을 조회할 수 있어야 합니다. 라라벨의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트에는 대상 엔티티의 알림을 반환하는 `notifications` [Eloquent 연관관계](/docs/12.x/eloquent-relationships)가 정의되어 있습니다. 이 메서드는 일반적인 Eloquent 연관관계처럼 사용하면 됩니다. 기본적으로 알림은 `created_at` 순서로 정렬되며, 최신 알림이 컬렉션 맨 앞에 놓입니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은("unread") 알림만 조회하려면, `unreadNotifications` 연관관계를 사용하세요. 역시 `created_at` 순으로 최신 알림이 먼저 정렬됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림을 조회하려면, 현재 사용자와 같은 알림 대상 엔티티의 알림 데이터를 반환하는 알림 컨트롤러를 만들어야 합니다. 이후, 해당 컨트롤러의 URL로 자바스크립트에서 HTTP 요청을 보내면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림을 읽음으로 표시하기

일반적으로 사용자가 알림을 확인하면, 해당 알림을 "읽음" 상태로 변경하려고 할 것입니다. `Illuminate\Notifications\Notifiable` 트레이트는 데이터베이스 알림의 `read_at` 컬럼을 갱신하는 `markAsRead` 메서드를 제공합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

개별 알림을 반복 처리하지 않고, 알림 컬렉션 전체에 바로 `markAsRead` 메서드를 사용할 수도 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

데이터베이스에서 알림을 미리 가져오지 않고 모두 읽음 처리하려면, 대량 수정 쿼리를 이용할 수 있습니다.

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

테이블에서 알림을 완전히 삭제하려면 `delete`를 사용하세요.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스팅 알림을 사용하기 전에, 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스 설정과 사용법을 충분히 숙지해야 합니다. 이벤트 브로드캐스팅은 자바스크립트 기반 프론트엔드에서 서버 측 라라벨 이벤트에 실시간으로 반응하는 기능을 제공합니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 라라벨 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 기능을 활용하여 알림을 실시간으로 송출하고, 자바스크립트 기반 프론트엔드가 이를 받아 처리할 수 있도록 합니다. 알림 클래스에 `toBroadcast` 메서드를 정의하면 해당 기능을 사용할 수 있습니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받아, 반드시 `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast` 메서드를 정의하지 않았다면, 데이터를 수집할 때 `toArray` 메서드가 대신 사용됩니다. 반환된 데이터는 JSON으로 인코딩되어 자바스크립트 프론트엔드로 전송됩니다. 예시 `toBroadcast` 메서드는 다음과 같습니다.

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * Get the broadcastable representation of the notification.
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

모든 브로드캐스트 알림은 브로드캐스팅 처리를 위해 큐에 쌓입니다. 브로드캐스트 처리에 사용할 큐 연결(connection)이나 큐 이름을 지정하려면, `BroadcastMessage`의 `onConnection` 및 `onQueue` 메서드를 chaining 방식으로 사용할 수 있습니다.

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

브로드캐스트 알림은 데이터 외에, 알림의 전체 클래스명을 포함하는 `type` 필드도 함께 전송합니다. 이 `type` 값을 커스터마이즈하려면 알림 클래스에 `broadcastType` 메서드를 정의하면 됩니다.

```php
/**
 * Get the type of the notification being broadcast.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 리스닝하기

알림은 `{notifiable}.{id}` 형식의 프라이빗 채널로 브로드캐스트됩니다. 예를 들어, ID가 1인 `App\Models\User` 인스턴스에 알림을 보낼 때는 `App.Models.User.1` 프라이빗 채널로 전송됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용할 경우, `notification` 메서드를 활용해 해당 채널의 알림을 손쉽게 받을 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

Laravel Echo는 React와 Vue를 위한 hook을 제공하여 알림 리스닝을 더욱 간편하게 만들어줍니다. 먼저 `useEchoNotification` hook을 호출하면, 컴포넌트가 언마운트될 때 자동으로 채널 연결이 해제되는 등 편리한 이용이 가능합니다.

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

기본적으로 이 hook은 모든 알림 타입을 리스닝합니다. 리스닝할 알림 타입을 지정하고 싶다면, 문자열 또는 문자열 배열을 `useEchoNotification`의 세 번째 인수로 넘겨주세요.

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

알림 페이로드의 구조(타입)를 별도로 지정해, 타입 안전성과 편집 편의성을 높일 수도 있습니다.

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

특정 엔티티의 브로드캐스트 알림 채널을 커스터마이즈하고 싶다면, 알림 대상 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하면 됩니다.

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
     * The channels the user receives notification broadcasts on.
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

라라벨에서 SMS 알림 발송은 [Vonage](https://www.vonage.com/) (이전 Nexmo) 서비스를 통해 제공됩니다. 먼저, `laravel/vonage-notification-channel`과 `guzzlehttp/guzzle` 패키지를 설치해야 합니다.

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)을 포함하지만, 이 파일을 반드시 내 애플리케이션에 복사할 필요는 없습니다. 단순히 환경 변수 `VONAGE_KEY`, `VONAGE_SECRET`에 Vonage의 퍼블릭 및 시크릿 키를 지정하면 됩니다.

키를 등록했다면, 기본 발신 전화번호를 지정하는 `VONAGE_SMS_FROM` 환경 변수도 꼭 설정하세요. 이 번호는 Vonage 관리자 패널에서 발급받을 수 있습니다.

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

알림을 SMS로 보낼 수 있어야 한다면, 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받아, `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 메시지 지원

SMS 메시지에 유니코드 문자가 포함되어 있다면, `VonageMessage` 인스턴스를 만들 때 `unicode` 메서드를 반드시 호출하세요.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### "From" 번호 커스터마이즈

기본 환경 변수에서 지정한 번호가 아닌, 다른 발신번호로 일부 알림을 발송하고 싶다면, `VonageMessage` 인스턴스의 `from` 메서드를 사용하면 됩니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가

사용자, 팀, 또는 클라이언트 별로 SMS 비용을 추적하고 싶다면, 알림에 "client reference"를 추가하세요. Vonage에서는 이 참조값으로 관련된 SMS 사용량 보고서를 제공합니다. 클라이언트 참조는 최대 40자의 임의의 문자열을 사용할 수 있습니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
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

Vonage 알림을 올바른 전화번호로 라우팅하려면, 알림 대상 엔티티에 `routeNotificationForVonage` 메서드를 정의하세요.

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
     * Route notifications for the Vonage channel.
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

Slack 알림을 발송하기 전에, 먼저 Slack 알림 채널 패키지를 Composer로 설치해야 합니다.

```shell
composer require laravel/slack-notification-channel
```

또한, 자신의 Slack 워크스페이스에 사용할 [Slack 앱](https://api.slack.com/apps?new_app=1)을 직접 생성해야 합니다.

만약 만든 앱과 동일한 워크스페이스로만 알림을 전송할 계획이라면, "OAuth & Permissions"에서 `chat:write`, `chat:write.public`, `chat:write.customize` 권한(scope)를 앱에 추가하면 됩니다.

다음으로, 앱의 "Bot User OAuth Token" 값을 복사해서 애플리케이션의 `services.php` 설정 파일 안의 `slack` 설정 배열에 등록하세요. 이 토큰은 Slack의 "OAuth & Permissions" 탭에서 확인할 수 있습니다.

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### 앱 배포 (App Distribution)

만약 사용자 소유의 외부 Slack 워크스페이스로 알림을 보내려면, Slack의 "Manage Distribution" 탭에서 앱을 "배포"해야 합니다. 앱을 배포한 뒤에는, [Socialite](/docs/12.x/socialite)로 [Slack Bot 토큰을 발급받는 방법](/docs/12.x/socialite#slack-bot-scopes)을 이용하세요.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

알림을 Slack 메시지로 발송할 수 있어야 한다면, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받아 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. [Slack의 Block Kit API](https://api.slack.com/block-kit)를 활용해 다양한 형태의 메시지를 만들 수 있습니다. 아래 예제는 [Slack의 Block Kit builder](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리보기 할 수 있습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
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
#### Slack Block Kit Builder 템플릿 사용하기

Block Kit 메시지를 직접 빌더 메서드로 만들지 않고, Slack Block Kit Builder가 생성한 JSON 페이로드를 그대로 `usingBlockKitTemplate` 메서드에 전달할 수도 있습니다.

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Get the Slack representation of the notification.
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

### Slack 인터랙티브 기능

Slack의 Block Kit 알림 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling)를 위한 강력한 기능을 제공합니다. 이 기능을 사용하려면 Slack 앱에서 "Interactivity"를 활성화하고, "Request URL"을 애플리케이션에서 제공하는 URL로 설정해야 합니다. 이러한 설정은 Slack의 "Interactivity & Shortcuts" 앱 관리 탭에서 관리할 수 있습니다.

아래 예제에서는 `actionsBlock` 메서드를 사용합니다. 사용자가 버튼을 클릭하면 Slack이 "Request URL"로 Slack 사용자 정보, 클릭된 버튼의 ID 등 다양한 데이터를 포함한 `POST` 요청을 전송합니다. 애플리케이션에서는 이 페이로드(payload)를 바탕으로 알맞은 동작을 수행할 수 있습니다. 또한, 반드시 [요청이 Slack에서 온 것인지를 검증](https://api.slack.com/authentication/verifying-requests-from-slack)해야 합니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
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
        })
        ->actionsBlock(function (ActionsBlock $block) {
             // ID defaults to "button_acknowledge_invoice"...
            $block->button('Acknowledge Invoice')->primary();

            // Manually configure the ID...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달(Confirmation Modals)

사용자가 버튼을 클릭했을 때 작업을 바로 실행하는 것이 아니라, 반드시 확인(Confirm) 후 작업이 진행되길 원한다면 버튼을 정의할 때 `confirm` 메서드를 사용할 수 있습니다. `confirm` 메서드는 메시지와, `ConfirmObject` 인스턴스를 전달받는 클로저를 인자로 받습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
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
        })
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
}
```

<a name="inspecting-slack-blocks"></a>
#### Slack Block 구조 확인하기

지금까지 구성한 블록의 구조를 빠르게 확인하고 싶을 때는, `SlackMessage` 인스턴스에서 `dd` 메서드를 호출할 수 있습니다. 이 메서드를 사용하면 Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/)로 연결되는 URL을 생성하여, 브라우저에서 페이로드와 알림 구조를 미리 볼 수 있습니다. `dd` 메서드에 `true`를 전달하면, 원본 페이로드(raw payload)를 덤프합니다.

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 적절한 Slack 팀 및 채널로 전달하려면, 알림을 받을 모델에 `routeNotificationForSlack` 메서드를 정의해야 합니다. 이 메서드는 세 가지 값 중 하나를 반환할 수 있습니다.

- `null` : 알림 자체에 설정된 채널로 라우팅합니다. 이 경우, `SlackMessage`를 구성할 때 `to` 메서드를 사용해 채널을 지정할 수 있습니다.
- 알림을 보낼 Slack 채널명을 지정하는 문자열. 예를 들어, `#support-channel` 등입니다.
- `SlackRoute` 인스턴스: OAuth 토큰과 채널명을 함께 제공할 수 있습니다. 예시: `SlackRoute::make($this->slack_channel, $this->slack_token)`  
  이 방식은 외부 워크스페이스로 알림을 전송할 때 사용합니다.

예를 들어, `routeNotificationForSlack` 메서드에서 `#support-channel`을 반환하면, 애플리케이션의 `services.php` 설정 파일에 있는 Bot User OAuth 토큰과 연결된 워크스페이스 내 `#support-channel`로 알림이 전송됩니다.

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
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return '#support-channel';
    }
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack 워크스페이스로 알림 전송

> [!NOTE]
> 외부 Slack 워크스페이스로 알림을 전송하기 전에, Slack 앱을 [배포(distribute)](#slack-app-distribution)해야 합니다.

실제로는 애플리케이션 사용자에게 속한 Slack 워크스페이스로 알림을 전송하고 싶은 경우가 많습니다. 이를 위해 먼저 해당 사용자의 Slack OAuth 토큰을 획득해야 합니다. 다행히도, [Laravel Socialite](/docs/12.x/socialite)는 Slack 드라이버를 지원하여, 애플리케이션 사용자 인증 및 [봇 토큰(bot token)](/docs/12.x/socialite#slack-bot-scopes) 획득을 쉽게 할 수 있습니다.

봇 토큰을 획득해서 데이터베이스에 저장했다면, `SlackRoute::make` 메서드를 활용하여 사용자의 워크스페이스로 알림을 보낼 수 있습니다. 또한, 어떤 채널로 알림을 전송할지 사용자가 직접 선택하도록 애플리케이션에서 설정 기회를 제공하는 것이 일반적입니다.

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
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 다국어(Localization) 지원

라라벨에서는 HTTP 요청의 현재 로케일(locale)과 다른 언어로 알림을 전송할 수 있습니다. 또한, 알림이 큐(Queue)에 들어가더라도 해당 로케일 정보를 기억합니다.

이 기능을 사용하려면, `Illuminate\Notifications\Notification` 클래스의 `locale` 메서드로 원하는 언어를 지정하면 됩니다. 알림을 평가하는 동안 애플리케이션은 해당 로케일로 임시 변경되었다가, 평가가 끝나면 원래 로케일로 복구됩니다.

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 명의 알림 수신자에 대해 로케일을 지정하려면 `Notification` 파사드의 `locale` 메서드를 사용할 수 있습니다.

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

때로는 애플리케이션에서 각 사용자의 선호 로케일을 저장해두기도 합니다. 이럴 경우, 노티파이어블(notifiable) 모델에 `HasLocalePreference` 계약(Contract)을 구현하면, 라라벨이 알림을 전송할 때 해당 로케일을 자동으로 사용하라고 지정할 수 있습니다.

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면, 라라벨은 자동으로 알림과 메일 전송시 선호 로케일을 사용합니다. 따라서 이 인터페이스를 사용할 때는 `locale` 메서드를 명시적으로 호출할 필요가 없습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

알림이 실제로 발송되는 것을 막기 위해 `Notification` 파사드의 `fake` 메서드를 사용할 수 있습니다. 대부분 테스트하려는 코드와 알림 전송은 직접적으로 관련이 없으므로, 실제로는 "라라벨이 특정 알림을 보내도록 지시받았다"는 사실만 검증하면 충분한 경우가 많습니다.

`Notification` 파사드의 `fake` 메서드를 호출한 뒤, 사용자가 알림을 받도록 지시를 받았는지, 알림이 받은 데이터는 무엇인지 등 다양한 assert(검증)를 할 수 있습니다.

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // Perform order shipping...

    // Assert that no notifications were sent...
    Notification::assertNothingSent();

    // Assert a notification was sent to the given users...
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // Assert a notification was not sent...
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // Assert that a given number of notifications were sent...
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

        // Perform order shipping...

        // Assert that no notifications were sent...
        Notification::assertNothingSent();

        // Assert a notification was sent to the given users...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // Assert a notification was not sent...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // Assert that a given number of notifications were sent...
        Notification::assertCount(3);
    }
}
```

`assertSentTo` 또는 `assertNotSentTo` 메서드에 클로저를 넘기면, 특정 조건을 만족하는 알림이 전송(또는 미전송)되었는지 "진실 테스트"로 검증할 수 있습니다. 한 건이라도 조건을 통과한 알림이 있다면 해당 검증은 성공합니다.

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

테스트 코드에서 [온디맨드 알림](#on-demand-notifications)을 전송하는 경우, `assertSentOnDemand` 메서드로 해당 알림이 전송되었는지 확인할 수 있습니다.

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` 메서드에 두 번째 인자로 클로저를 전달하면, 올바른 "라우트" 주소(예: 메일주소)로 알림이 발송되었는지 추가로 검증할 수 있습니다.

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
#### NotificationSending 이벤트

알림이 전송되기 직전에, 노티피케이션 시스템은 `Illuminate\Notifications\Events\NotificationSending` 이벤트를 발생시킵니다. 이 이벤트에는 "notifiable" 엔티티(알림 대상)와 알림 인스턴스가 포함되어 있습니다. 애플리케이션에서 이 이벤트를 위한 [이벤트 리스너](/docs/12.x/events)를 만들 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

만약 `NotificationSending` 이벤트를 리슨하는 리스너의 `handle` 메서드가 `false`를 반환하면, 해당 알림은 전송되지 않습니다.

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 리스너 내부에서는 `notifiable`, `notification`, `channel` 속성을 활용해 수신자와 알림에 대한 추가 정보를 확인할 수 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
#### NotificationSent 이벤트

알림이 실제로 전송된 시점에는, 노티피케이션 시스템이 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)를 발생시킵니다. 이 이벤트 역시 "notifiable" 엔티티와 알림 인스턴스를 포함합니다. 애플리케이션에서 이 이벤트를 위한 [이벤트 리스너](/docs/12.x/events)를 만들 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

이벤트 리스너 내부에서는 `notifiable`, `notification`, `channel`, `response` 속성을 통해 수신자와 알림에 대한 더 많은 정보를 확인할 수 있습니다.

```php
/**
 * Handle the event.
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

라라벨은 일부 알림 채널을 내장하고 있지만, 직접 구현한 드라이버로 다른 방식의 알림도 손쉽게 전송할 수 있습니다. 커스텀 채널 작성은 다음과 같습니다.  
먼저 `send` 메서드를 가진 클래스를 정의합니다. 이 메서드는 두 개의 인수, 즉 `$notifiable` 객체와 `$notification`을 받습니다.

`send` 메서드 안에서 알림 객체의 메서드를 호출하여 채널이 이해할 수 있는 메시지 객체를 얻고, 원하는 방식으로 `$notifiable` 인스턴스에 알림을 발송하면 됩니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * Send the given notification.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // Send notification to the $notifiable instance...
    }
}
```

커스텀 알림 채널 클래스를 정의했으면, 알림의 `via` 메서드에서 해당 클래스 이름을 반환하면 됩니다. 아래 예시에서는 알림 클래스의 `toVoice` 메서드가 음성 메시지(Voice Message)를 구성하는 객체를 반환합니다. 예를 들어, 직접 정의한 `VoiceMessage` 클래스 등을 사용할 수 있습니다.

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
     * Get the notification channels.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * Get the voice representation of the notification.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```