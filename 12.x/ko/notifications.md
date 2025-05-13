# 알림(Notification) (Notifications)

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
    - [Mailable 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비 사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림 읽음 처리하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비 사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비 사항](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅하기](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비 사항](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 알림 라우팅하기](#routing-slack-notifications)
    - [외부 Slack 워크스페이스에 알림 보내기](#notifying-external-slack-workspaces)
- [알림 로컬라이징](#localizing-notifications)
- [테스트하기](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

라라벨은 [이메일 발송](/docs/12.x/mail) 기능뿐만 아니라, 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 이름 Nexmo), [Slack](https://slack.com) 등 다양한 전달 채널을 통해 알림을 전송하는 기능도 제공합니다. 또한, [커뮤니티에서 제작된 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 가지의 다양한 경로로도 알림을 보낼 수 있습니다! 알림은 데이터베이스에도 저장할 수 있어서 웹 인터페이스 내에 표시할 수도 있습니다.

일반적으로 알림은 사용자에게 애플리케이션에서 발생한 어떤 사건을 간단히 알려주는 짧은 정보성 메시지입니다. 예를 들어, 결제 애플리케이션을 개발할 때, 사용자가 결제를 완료하면 "인보이스 결제 완료" 알림을 이메일과 SMS 채널을 통해 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

라라벨에서는 각 알림이 보통 `app/Notifications` 디렉터리에 개별 클래스로 정의되어 있습니다. 만약 애플리케이션에 이 디렉터리가 없다면, `make:notification` 아티즌 명령어를 실행하면 자동으로 생성됩니다.

```shell
php artisan make:notification InvoicePaid
```

이 명령어를 실행하면 새로운 알림 클래스가 `app/Notifications` 디렉터리에 생성됩니다. 각 알림 클래스에는 `via` 메서드와, 해당 채널에 맞게 메시지를 변환하는 여러 개의 메시지 빌더 메서드(`toMail`, `toDatabase` 등)가 포함됩니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 두 가지 방식으로 보낼 수 있습니다. 하나는 `Notifiable` 트레이트의 `notify` 메서드를 사용하는 방법이고, 또 하나는 `Notification` [파사드](/docs/12.x/facades)를 사용하는 방법입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다.

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
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 추가해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는, `Notification` [파사드](/docs/12.x/facades)를 통해서도 알림을 보낼 수 있습니다. 이 방식은 여러 명의 사용자 등 다수의 알림 대상에게 동시에 알림을 보내야 할 때 유용합니다. 파사드를 이용해 알림을 전송할 때는, 알림 대상 엔티티들과 알림 인스턴스를 `send` 메서드에 전달합니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

즉시 알림을 보내고 싶다면, `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림에 `ShouldQueue` 인터페이스가 구현되어 있더라도 즉시 알림을 전송합니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

각 알림 클래스에는 해당 알림이 어느 채널로 전달될지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 등의 채널로 전송할 수 있습니다.

> [!NOTE]
> Telegram, Pusher와 같이 공식 지원되지 않는 채널을 사용하고 싶다면, 커뮤니티가 관리하는 [Laravel Notification Channels 사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 인수로 받으며, 이 값은 알림을 받을 대상 클래스의 인스턴스입니다. `$notifiable` 객체를 활용해서 어떤 채널에 알림을 보낼지 조건을 지정할 수 있습니다.

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
> 알림 큐를 사용하기 전에 큐 설정을 마치고 [워크 커를 실행](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림 전송은 외부 API 호출 등이 필요한 경우 처리 시간이 오래 걸릴 수 있습니다. 애플리케이션의 응답 속도를 높이기 위해, 알림을 큐잉할 수 있습니다. 이를 위해 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가하면 됩니다. `make:notification` 명령어로 생성한 알림 클래스에는 이미 이 인터페이스와 트레이트를 바로 사용할 수 있도록 import 되어 있습니다.

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

`ShouldQueue` 인터페이스를 추가했다면, 알림을 평소와 같이 보내면 됩니다. 라라벨은 자동으로 이 인터페이스를 감지하여 알림 전송을 큐에 넣습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐잉할 때는 수신자와 채널 조합별로 각각 큐 작업이 생성됩니다. 예를 들어, 수신자가 3명이고 채널이 2개라면, 큐에 6개의 작업이 생성됩니다.

<a name="delaying-notifications"></a>
#### 알림 발송 지연시키기

알림 전송을 일정 시간 이후에 지연해서 보내고 싶다면, 알림 인스턴스 생성 시 `delay` 메서드를 체이닝(연결)해서 사용할 수 있습니다.

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 다른 지연 시간을 지정하고 싶다면, `delay` 메서드에 배열을 전달할 수 있습니다.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스 내에 `withDelay` 메서드를 정의해서도 지연 시간을 지정할 수 있습니다. `withDelay` 메서드는 채널명과 지연 값을 매핑한 배열을 반환해야 합니다.

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
#### 알림 큐 커넥션 커스터마이징

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 특정 알림에서 별도의 큐 커넥션을 사용하고 싶다면, 알림의 생성자에서 `onConnection` 메서드를 호출할 수 있습니다.

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

또는 알림이 지원하는 각 채널별로 다른 큐 커넥션을 지정하고 싶다면, 알림 클래스에 `viaConnections` 메서드를 정의하세요. 이 메서드는 채널명과 큐 커넥션명을 매핑한 배열을 반환해야 합니다.

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
#### 알림 채널별 큐 이름 커스터마이징

각 알림 채널별로 사용될 큐 이름을 다르게 설정하고 싶다면, 알림 클래스에 `viaQueues` 메서드를 정의할 수 있습니다. 이 메서드는 채널명과 큐 이름의 쌍을 배열로 반환해야 합니다.

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

큐잉된 알림은 [큐잉된 작업과 동일하게 미들웨어](/docs/12.x/queues#job-middleware)를 정의할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하면 시작할 수 있습니다. 이 메서드는 `$notifiable`과 `$channel` 변수를 받아, 알림의 목적지에 따라 어떤 미들웨어를 적용할지 결정할 수 있습니다.

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

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치(전송)될 경우, 알림이 큐 워커에 의해 처리되는 시점에 트랜잭션이 아직 커밋되지 않았을 수 있습니다. 이 경우 트랜잭션 내에서 수정한 모델이나 레코드가 데이터베이스에 반영되어 있지 않을 수 있습니다. 또한 트랜잭션 내에서 새로 생성한 모델이나 레코드가 데이터베이스에 존재하지 않을 수도 있습니다. 알림이 이러한 모델에 의존한다면, 큐 작업 처리 시 예기치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정 값이 `false`일 때, 특정 큐잉된 알림만 모든 데이터베이스 트랜잭션 커밋 이후에 디스패치되도록 하고 싶다면, 알림 전송 시 `afterCommit` 메서드를 체이닝해서 사용할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스의 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
> 이러한 이슈에 대한 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림의 발송 여부 결정하기

큐잉된 알림이 큐에 디스패치되면, 일반적으로 큐 워커에서 받아서 예정된 수신자에게 알림을 보냅니다.

하지만, 큐 워커에서 알림이 처리되는 시점에 실제로 발송할지 마지막으로 판단하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 알림은 발송되지 않습니다.

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

애플리케이션의 "사용자"로 저장되어 있지 않은 대상에게 알림을 보내야 하는 경우가 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 사용하여 임의의 라우팅 정보를 지정한 뒤 알림을 보낼 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 라우트로 온디맨드 알림을 보낼 때 수신자 이름까지 지정하고 싶다면, 이메일 주소를 키, 이름을 값으로 하는 배열을 전달하면 됩니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 이용하면, 여러 알림 채널에 대한 라우팅 정보를 한 번에 지정할 수도 있습니다.

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

알림이 이메일로도 전송될 수 있도록 하려면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인수로 받아, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션성 이메일 메시지를 쉽게 작성할 수 있는 몇 가지 메서드를 제공합니다. 메일 메시지는 여러 줄의 텍스트와 "Call to Action" 버튼을 포함할 수 있습니다. 아래는 `toMail` 메서드의 예시입니다.

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
> 위 `toMail` 메서드에서 `$this->invoice->id`를 사용한 것에 주목하세요. 알림 메시지 작성에 필요한 모든 데이터는 알림 클래스의 생성자를 통해 전달할 수 있습니다.

이 예시에서는 인사말(greeting), 텍스트 한 줄, Call to Action, 다시 한 번의 텍스트 줄을 등록했습니다. `MailMessage` 객체가 제공하는 이러한 메서드 덕분에, 간단한 트랜잭션성 이메일을 쉽고 빠르게 포맷팅할 수 있습니다. `mail` 채널은 이런 메시지 구성요소들을 아름답고 반응형이며, 텍스트 버전도 함께 제공하는 HTML 이메일 템플릿으로 변환합니다. 아래는 `mail` 채널로 생성된 이메일의 예시입니다.

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때는 반드시 `config/app.php` 설정 파일에서 `name` 설정 값을 지정해야 합니다. 이 값은 메일 알림의 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 오류 메시지

일부 알림은 결제 실패와 같은 오류 상황을 사용자에게 알려줍니다. 이런 경우, 메시지 작성 시 `error` 메서드를 호출하면 해당 알림이 오류와 관련 있다는 걸 표시할 수 있습니다. `error` 메서드를 사용하면, Call to Action 버튼이 검정색 대신 빨간색으로 표시됩니다.

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
#### 메일 알림의 기타 포맷팅 옵션

알림 클래스 안에서 "lines"를 직접 정의하는 대신, `view` 메서드를 사용하여 커스텀 템플릿을 지정해서 알림 이메일을 렌더링할 수도 있습니다.

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

`view` 메서드에 배열의 두 번째 요소로 plain-text 뷰 이름을 전달하면 메일 메시지의 텍스트 버전도 지정할 수 있습니다.

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

혹시 메시지가 오직 plain-text 뷰만 필요하다면, `text` 메서드를 활용할 수 있습니다.

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
### 발신자 커스터마이징

기본적으로 메일의 발신자/From 주소는 `config/mail.php` 설정 파일에 정의되어 있습니다. 단, 특정 알림마다 발신자 주소를 다르게 지정하고 싶다면 `from` 메서드를 사용할 수 있습니다.

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
### 수신자 커스터마이징

`mail` 채널을 통해 알림을 보낼 때, 라라벨은 기본적으로 알림 대상 엔티티에서 `email` 속성을 찾아 알림을 전송합니다. 만약 다른 이메일 주소로 알림을 보내고 싶다면, 알림 대상 엔티티에 `routeNotificationForMail` 메서드를 정의할 수 있습니다.

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
        // 이메일 주소만 반환...
        return $this->email_address;

        // 이메일 주소와 이름 모두 반환...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 메일의 제목(subject)은 알림 클래스의 이름을 "Title Case"로 변환한 값입니다. 예를 들어 알림 클래스 이름이 `InvoicePaid`라면, 이메일 제목은 `Invoice Paid`가 됩니다. 메시지의 제목을 직접 지정하고 싶다면, 메시지 작성 시 `subject` 메서드를 사용할 수 있습니다.

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

### 메일러 커스터마이징

기본적으로 이메일 알림은 `config/mail.php` 설정 파일에 정의된 기본 메일러를 통해 발송됩니다. 하지만, 메시지를 생성할 때 `mailer` 메서드를 호출하여 런타임에 다른 메일러를 지정할 수도 있습니다.

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
### 템플릿 커스터마이징

메일 알림에 사용되는 HTML 및 일반 텍스트 템플릿을 수정하려면 알림 패키지의 리소스를 퍼블리시하면 됩니다. 아래 명령어를 실행하면 메일 알림 템플릿이 `resources/views/vendor/notifications` 디렉터리에 생성됩니다.

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부 파일

이메일 알림에 첨부 파일을 추가하려면 메시지를 만들 때 `attach` 메서드를 사용하면 됩니다. `attach` 메서드의 첫 번째 인자로 파일의 절대 경로를 전달합니다.

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
> 알림 메일 메시지의 `attach` 메서드는 [attachable objects](/docs/12.x/mail#attachable-objects)도 지원합니다. 더 자세한 정보는 [attachable object 문서](/docs/12.x/mail#attachable-objects)를 참고하시기 바랍니다.

파일을 첨부할 때, `attach` 메서드의 두 번째 인자로 배열을 전달하면 파일의 표시 이름(디스플레이 이름)과 MIME 타입도 지정할 수 있습니다.

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

일반적인 mailable 객체에서 파일을 첨부하는 방법과는 다르게, 알림에서는 `attachFromStorage`를 사용해 바로 스토리지 디스크에서 파일을 첨부할 수 없습니다. 대신, 스토리지 디스크상의 파일의 절대 경로를 `attach` 메서드에 전달해야 합니다. 또는, `toMail` 메서드에서 [mailable](/docs/12.x/mail#generating-mailables)을 반환하는 방법도 사용할 수 있습니다.

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

필요하다면, `attachMany` 메서드를 사용해 여러 개의 파일을 한 번에 첨부할 수 있습니다.

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

`attachData` 메서드를 사용하면 바이트 문자열 데이터를 첨부 파일로 추가할 수 있습니다. 이 메서드를 사용할 때는 첨부 파일로 할당할 파일 이름을 반드시 지정해야 합니다.

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

Mailgun, Postmark 같은 일부 외부 이메일 제공 업체는 메시지를 그룹화하고 추적하는 데 사용할 수 있는 "태그" 및 "메타데이터" 기능을 지원합니다. 메일 메시지에 태그 및 메타데이터를 추가하려면 `tag` 및 `metadata` 메서드를 사용하면 됩니다.

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

애플리케이션에서 Mailgun 드라이버를 사용하는 경우, [Mailgun 태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1) 및 [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) 관련 공식 문서를 참고하세요. Postmark를 사용하는 경우에도 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 참고 문서를 확인하실 수 있습니다.

Amazon SES를 사용하여 이메일을 보내는 경우, 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가하려면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 사용하면 메시지 전송 전에 Symfony Message 인스턴스를 받아 커스터마이징할 수 있는 클로저를 등록할 수 있습니다. 이를 활용하면 실제 메시지 발송 전에 다양한 커스터마이징이 가능합니다.

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

필요하다면, 알림의 `toMail` 메서드에서 전체 [mailable 객체](/docs/12.x/mail)를 반환할 수 있습니다. `MailMessage` 대신 `Mailable`을 반환할 때에는, mailable 객체의 `to` 메서드를 사용해 직접 수신자를 지정해 주어야 합니다.

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
#### Mailable과 주문형(On-Demand) 알림

[주문형 알림](#on-demand-notifications)을 보내는 경우, `toMail` 메서드에서 전달받는 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable`의 인스턴스입니다. 이 클래스는 `routeNotificationFor` 메서드를 제공하며, 주문형 알림을 보낼 이메일 주소를 가져오는 데 사용할 수 있습니다.

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

메일 알림 템플릿을 디자인할 때, 일반 Blade 템플릿처럼 렌더링된 메일 메시지를 브라우저에서 즉시 확인할 수 있으면 매우 편리합니다. 이를 위해 라라벨에서는 알림에서 생성된 메일 메시지를 라우트 클로저나 컨트롤러에서 바로 반환할 수 있도록 지원합니다. `MailMessage`가 반환되면 실제 이메일 주소로 보내지지 않고, 즉시 브라우저에 렌더링되어 디자인을 미리 볼 수 있습니다.

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

Markdown 메일 알림을 사용하면 라라벨이 제공하는 사전 제작된 메일 알림 템플릿을 활용하면서도, 더 길고 자유롭게 맞춤화된 메시지를 작성할 수 있습니다. 메시지가 Markdown 문법으로 작성되므로, 라라벨은 내용을 아름답고 반응형인 HTML 템플릿으로 렌더링하고, 동시에 일반 텍스트 버전도 자동으로 만들어줍니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

Notification과 연결된 Markdown 템플릿을 생성하려면, `make:notification` 아티즌 명령어의 `--markdown` 옵션을 사용합니다.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 메일 알림과 마찬가지로, Markdown 템플릿을 사용하는 알림 클래스에도 `toMail` 메서드를 정의해야 합니다. 다만, `line`이나 `action` 메서드 대신, 어떤 Markdown 템플릿을 사용할 것인지 `markdown` 메서드를 통해 지정합니다. 템플릿에서 사용할 데이터를 배열로 두 번째 인자에 넘길 수 있습니다.

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

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법의 조합으로 작성됩니다. 이를 통해 라라벨의 사전 제작된 알림 컴포넌트를 활용하면서 쉽게 읽고 쓸 수 있는 알림을 만들 수 있습니다.

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
> Markdown 이메일을 작성할 때는 불필요한 들여쓰기를 사용하지 마세요. Markdown 표준에 따르면, 들여쓰기된 내용은 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 필수 인자로 `url`을, 옵션으로 `color`를 받습니다. 지원하는 색상은 `primary`, `green`, `red`입니다. 알림 메시지에 버튼 컴포넌트를 여러 번 추가해도 됩니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 알림 본문과는 다르게 살짝 다른 배경색을 가진 패널로 렌더링합니다. 이를 통해 사용자의 주의를 특정 블록으로 끌 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 Markdown 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트에는 Markdown 테이블을 본문으로 전달하며, 기본 Markdown 테이블 정렬 문법을 그대로 사용할 수 있습니다.

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

원하는 경우, 마크다운 알림 컴포넌트 전체를 직접 커스터마이즈할 수 있도록 내보낼 수 있습니다. 컴포넌트를 내보내려면, `laravel-mail` 태그로 `vendor:publish` 아티즌 명령어를 사용하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어로 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 퍼블리시됩니다. `mail` 디렉터리 안에는 각각의 컴포넌트별 HTML용과 텍스트용 디렉터리가 별도로 존재합니다. 이 컴포넌트들은 자유롭게 수정 가능합니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보내고 나면, `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생깁니다. 이 CSS 파일을 자유롭게 수정하면, 해당 스타일이 자동으로 마크다운 알림의 HTML 본문에 인라인 형태로 반영됩니다.

라라벨의 마크다운 컴포넌트용으로 새로운 테마를 완전히 만들고 싶다면, 임의의 CSS 파일을 `html/themes` 디렉터리에 저장하면 됩니다. 원하는 테마로 CSS 파일명을 붙인 뒤 저장한 다음, `mail` 설정 파일의 `theme` 옵션 값을 새 테마 이름으로 변경하면 적용됩니다.

개별 알림에 대해 테마를 지정하고 싶다면, 알림을 만드는 과정에서 `theme` 메서드를 사용하면 됩니다. 이 메서드에 사용하고자 하는 테마 이름을 전달하세요.

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
### 사전 준비사항

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블은 알림의 타입, 그리고 알림을 설명하는 JSON 데이터 구조 같은 정보를 담습니다.

이 정보를 바탕으로 애플리케이션 UI에서 알림을 표시할 수 있습니다. 다만 그 전에, 알림을 저장할 데이터베이스 테이블을 생성해야 합니다. 다음 명령어를 사용해 올바른 테이블 스키마를 가진 [마이그레이션](/docs/12.x/migrations)을 생성할 수 있습니다.

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 알림을 받을 모델이 [UUID 또는 ULID 기본키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용하는 경우, 알림 테이블 마이그레이션에서 `morphs` 메서드 대신 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)를 사용해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포매팅

알림을 데이터베이스에 저장할 수 있도록 지원하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아서 평범한 PHP 배열을 반환해야 하며, 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 아래는 예시 `toArray` 메서드입니다.

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

알림이 데이터베이스에 저장되면, `type` 컬럼에는 기본적으로 알림 클래스 명이 저장되고 `read_at` 컬럼은 `null`로 설정됩니다. 이 동작을 변경하고 싶다면 알림 클래스에 `databaseType` 및 `initialDatabaseReadAtValue` 메서드를 정의할 수 있습니다.

```
use Illuminate\Support\Carbon;
```

```php
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

`toArray` 메서드는 `broadcast` 채널에서도 브로드캐스트할 데이터를 결정할 때 사용됩니다. 만약 `database` 채널과 `broadcast` 채널에 서로 다른 배열을 반환하고 싶다면, `toArray` 대신 `toDatabase` 메서드를 정의해야 합니다.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

알림이 데이터베이스에 저장된 후, 노티파이어블(알림을 받을 수 있는) 엔티티로부터 알림을 쉽게 조회할 수 있는 방법이 필요합니다. 라라벨의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트에서는 해당 엔티티와 연결된 알림을 반환하는 `notifications` [Eloquent 관계](/docs/12.x/eloquent-relationships)를 제공합니다. 이 메서드는 일반 Eloquent 관계처럼 사용할 수 있으며, 기본적으로 생성일시(`created_at`)가 가장 최신인 알림부터 컬렉션 앞쪽에 정렬되어 반환합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

오직 읽지 않은("unread") 알림만 조회하려면 `unreadNotifications` 관계를 사용하면 됩니다. 역시 최신순으로 정렬됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript 클라이언트에서 알림을 조회하려면 애플리케이션에 알림 컨트롤러를 정의해, 특정 노티파이어블 엔티티(예: 현재 사용자) 대상으로 알림을 반환하도록 구현해야 합니다. 그리고 JavaScript에서 해당 컨트롤러 URL로 HTTP 요청을 보내면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리하기

일반적으로 사용자가 알림을 확인하면 이를 "읽음" 상태로 표시하고 싶을 것입니다. `Illuminate\Notifications\Notifiable` 트레이트는 `read_at` 컬럼을 업데이트하는 `markAsRead` 메서드를 제공합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

각 알림을 반복하면서 처리하지 않고, 전체 알림 컬렉션에 대해 바로 `markAsRead` 메서드를 호출할 수도 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

또는, 데이터베이스에서 알림을 직접 조회하지 않고도, 일괄 업데이트 쿼리를 사용해서 한 번에 모두 읽음으로 처리할 수도 있습니다.

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

테이블에서 알림을 완전히 삭제하려면 `delete` 메서드를 사용하세요.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비사항

알림을 브로드캐스트하기 전에, 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 반드시 구성하고 숙지해야 합니다. 이벤트 브로드캐스팅은 서버 측 라라벨 이벤트에 자바스크립트 프론트엔드가 실시간으로 반응할 수 있는 기능을 제공합니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포매팅

`broadcast` 채널은 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 활용하여 자바스크립트 프론트엔드에 실시간으로 알림을 전달합니다. 알림에서 브로드캐스팅을 지원하려면 알림 클래스에 `toBroadcast` 메서드를 정의하면 됩니다. 이 메서드는 `$notifiable` 엔티티를 받아 `BroadcastMessage` 인스턴스를 반환해야 하며, 만약 이 메서드가 없다면 브로드캐스트할 데이터를 위해 `toArray`가 자동으로 사용됩니다. 반환된 데이터는 JSON으로 인코딩되어 프론트엔드로 전송됩니다. 아래는 예시 `toBroadcast` 메서드입니다.

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

모든 브로드캐스트 알림은 큐에 등록되어 비동기적으로 처리됩니다. 브로드캐스트 작업에 사용될 큐 커넥션 또는 큐 이름을 지정하고 싶다면 `BroadcastMessage`의 `onConnection`, `onQueue` 메서드를 사용할 수 있습니다.

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

명시적으로 지정한 데이터 외에도, 모든 브로드캐스트 알림에는 알림의 전체 클래스명이 들어 있는 `type` 필드가 포함됩니다. 알림의 `type` 값을 커스터마이징하려면 알림 클래스에 `broadcastType` 메서드를 정의하면 됩니다.

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
### 알림 수신 리스너

알림은 `{notifiable}.{id}` 패턴을 따르는 프라이빗 채널에서 브로드캐스트됩니다. 예를 들어, ID가 `1`인 `App\Models\User` 인스턴스에 알림을 보내면, 해당 알림은 `App.Models.User.1` 프라이빗 채널로 브로드캐스트됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용할 경우, `notification` 메서드를 통해 해당 채널에서 알림을 쉽게 수신할 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이징

특정 엔티티가 브로드캐스트 알림을 수신하는 채널을 직접 지정하고 싶다면, 노티파이어블 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하세요.

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

라라벨에서 SMS 알림을 전송하는 기능은 [Vonage](https://www.vonage.com/) (이전 명칭: Nexmo) 기반으로 동작합니다. Vonage를 통해 알림을 전송하려면, 먼저 `laravel/vonage-notification-channel` 및 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지에는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있습니다. 하지만, 이 설정 파일을 반드시 직접 애플리케이션에 내보낼 필요는 없습니다. 대신, `VONAGE_KEY`와 `VONAGE_SECRET` 환경 변수를 사용해 Vonage의 퍼블릭 및 시크릿 키를 정의하면 됩니다.

키를 정의한 후에는 SMS 메시지의 기본 발신 전화번호를 지정하기 위해 `VONAGE_SMS_FROM` 환경 변수를 설정해야 합니다. 이 전화번호는 Vonage 콘솔 패널에서 생성할 수 있습니다:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷 지정

알림이 SMS로 전송될 수 있도록 지원하려면, 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 전달받으며, `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림의 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 문자 메시지

SMS 메시지에 유니코드(Unicode) 문자가 포함되어야 하는 경우, `VonageMessage` 인스턴스를 생성할 때 `unicode` 메서드를 호출해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림의 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### 발신 번호 맞춤 설정

만약 `VONAGE_SMS_FROM` 환경 변수에 지정된 전화번호와 다른 번호로 일부 알림을 발송하고 싶다면, `VonageMessage` 인스턴스에서 `from` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림의 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 레퍼런스 추가

사용자, 팀 또는 클라이언트별 비용 추적이 필요하다면, 알림에 "client reference(클라이언트 레퍼런스)"를 추가할 수 있습니다. Vonage는 이 클라이언트 레퍼런스로 관련 통계를 조회할 수 있으므로, 특정 고객의 SMS 사용량을 더 잘 파악할 수 있습니다. 클라이언트 레퍼런스는 최대 40자까지의 문자열이면 됩니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림의 표현을 반환합니다.
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

Vonage 알림을 올바른 전화번호로 라우팅하기 위해서는, 알림을 받을 엔티티(예: User 모델)에 `routeNotificationForVonage` 메서드를 정의해야 합니다:

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
     * Vonage 채널을 위한 알림 라우팅.
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

Slack 알림을 전송하려면 Composer를 통해 Slack 알림 채널을 먼저 설치해야 합니다:

```shell
composer require laravel/slack-notification-channel
```

추가로, Slack 워크스페이스에 [Slack App](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

알림을 생성된 Slack App과 동일한 워크스페이스로만 전송하고 싶다면, App에 `chat:write`, `chat:write.public`, `chat:write.customize` 스코프가 추가되어 있어야 합니다. 이 스코프들은 Slack의 "OAuth & Permissions" App 관리 탭에서 추가할 수 있습니다.

이후, App의 "Bot User OAuth Token"을 복사해서 애플리케이션의 `services.php` 설정 파일 내 `slack` 설정 배열에 아래와 같이 저장합니다. 해당 토큰은 Slack의 "OAuth & Permissions" 탭에서 찾을 수 있습니다:

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

애플리케이션이 외부(사용자 소유) Slack 워크스페이스로 알림을 보낼 계획이라면, Slack을 통해 App을 "배포(distribute)" 해야 합니다. App 배포는 Slack App의 "Manage Distribution" 탭에서 관리할 수 있습니다. App이 배포된 이후에는 [Socialite](/docs/12.x/socialite)를 사용해 [Slack Bot 토큰을 얻을 수 있습니다](/docs/12.x/socialite#slack-bot-scopes).

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷 지정

알림이 Slack 메시지로 전송될 수 있도록 지원하려면, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 전달받고, `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. 또한 [Slack의 Block Kit API](https://api.slack.com/block-kit)를 사용해 다양한 형태의 알림 메시지를 구성할 수 있습니다. 아래 예시는 [Slack의 Block Kit builder](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리 확인할 수 있습니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림의 표현을 반환합니다.
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
#### Slack Block Kit Builder 템플릿 사용

Block Kit 메시지를 작성할 때, 메서드를 체이닝해서 메시지를 만들지 않고 Slack의 Block Kit Builder에서 생성한 순수 JSON 페이로드를 `usingBlockKitTemplate` 메서드에 전달할 수도 있습니다:

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Slack 알림의 표현을 반환합니다.
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
### Slack 상호작용(Interactivity)

Slack의 Block Kit 알림 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling)와 같은 강력한 기능을 제공합니다. 이를 활용하려면 Slack App에서 "Interactivity" 기능을 활성화한 뒤, 애플리케이션에서 제공하는 URL을 "Request URL"로 설정해야 합니다. 이 설정은 Slack의 "Interactivity & Shortcuts" App 관리 탭에서 할 수 있습니다.

아래 예시처럼 `actionsBlock` 메서드를 활용하면, Slack은 버튼 클릭 시 "Request URL"로 Slack 사용자의 정보, 클릭된 버튼 ID 등이 담긴 `POST` 요청을 전송합니다. 애플리케이션에서는 이 페이로드를 바탕으로 적절한 동작을 처리할 수 있습니다. 또한 [요청자가 Slack인지 검증하는 절차](https://api.slack.com/authentication/verifying-requests-from-slack)도 반드시 구현해야 합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림의 표현을 반환합니다.
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
             // ID는 기본값으로 "button_acknowledge_invoice"가 사용됩니다...
            $block->button('Acknowledge Invoice')->primary();

            // ID를 직접 설정할 수도 있습니다...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인(Confirmation) 모달 사용

사용자 행동에 대해 사전 확인을 받아야 한다면, 버튼을 정의할 때 `confirm` 메서드를 호출할 수 있습니다. 이 메서드는 메시지와, `ConfirmObject` 인스턴스를 전달받는 클로저를 인자로 받습니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림의 표현을 반환합니다.
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
#### Slack 블록 미리보기(Inspecting Slack Blocks)

작성 중인 블록의 결과를 바로 확인하고 싶다면, `SlackMessage` 인스턴스에 `dd` 메서드를 호출해 볼 수 있습니다. 이 메서드는 Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/) 미리보기 링크를 생성해서 dump해주며, 브라우저에서 페이로드와 알림 미리보기를 즉시 확인할 수 있습니다. `dd` 메서드에 `true`를 인자로 넘기면 원시 페이로드도 dump합니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 올바른 워크스페이스 및 채널로 전송하려면, notifiable 모델에서 `routeNotificationForSlack` 메서드를 정의해주면 됩니다. 이 메서드는 아래 중 한 가지 값을 반환할 수 있습니다:

- `null` - 알림 자체에 설정된 채널을 사용하도록 라우팅을 위임합니다. 알림 작성 시 `to` 메서드를 사용해 채널을 지정할 수 있습니다.
- 알림을 전송할 Slack 채널을 나타내는 문자열 값(예: `#support-channel`)
- `SlackRoute` 인스턴스 - OAuth 토큰 및 채널명을 지정하여 외부 워크스페이스로 알림 전송을 지원합니다(예: `SlackRoute::make($this->slack_channel, $this->slack_token)`).

예를 들어, `routeNotificationForSlack` 메서드에서 `#support-channel`을 반환하면, 애플리케이션의 `services.php`에 등록된 Bot User OAuth 토큰과 연결된 워크스페이스의 `#support-channel` 채널로 알림이 전송됩니다:

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
     * Slack 채널을 위한 알림 라우팅.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return '#support-channel';
    }
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack 워크스페이스 알림 전송

> [!NOTE]
> 외부 Slack 워크스페이스로 알림을 보내기 전, Slack App이 [배포](#slack-app-distribution)되어 있어야 합니다.

애플리케이션 사용자들이 소유한 외부 Slack 워크스페이스로 알림을 자주 보내야 할 수 있습니다. 이를 위해서는 먼저 해당 사용자의 Slack OAuth 토큰을 받아와야 합니다. 다행히도, [Laravel Socialite](/docs/12.x/socialite)는 Slack 드라이버를 기본 제공하며, 이를 통해 애플리케이션 사용자를 Slack에 쉽게 인증시켜 [봇 토큰을 획득할 수 있습니다](/docs/12.x/socialite#slack-bot-scopes).

봇 토큰을 발급받아 애플리케이션 데이터베이스에 저장한 후, 알림을 해당 워크스페이스로 라우팅하려면 `SlackRoute::make` 메서드를 사용할 수 있습니다. 또한, 사용자에게 알림을 받을 채널을 직접 지정할 수 있는 기능을 제공하는 것이 좋습니다:

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
     * Slack 채널을 위한 알림 라우팅.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 다국어화(Localizing Notifications)

라라벨은 HTTP 요청의 현재 로케일과 다른 언어로 알림을 보낼 수 있도록 지원하며, 알림이 큐에 쌓인 경우에도 이 로케일을 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스에서는 원하는 언어를 설정할 수 있는 `locale` 메서드를 제공합니다. 알림이 평가(evaluate)될 때 애플리케이션의 로케일이 해당 언어로 전환되었다가, 완료되면 원래 로케일로 복귀합니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

다수의 notifiable 엔트리(수신자)에 대해서도 `Notification` 파사드의 `locale`을 사용해 일괄 로케일 설정이 가능합니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 언어(User Preferred Locales)

애플리케이션에 각 사용자의 선호 로케일 정보가 저장된 경우, notifiable 모델에 `HasLocalePreference` 계약을 구현하면, 라라벨이 알림 발송 시 사용자의 선호 로케일을 자동으로 적용하도록 할 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호하는 로케일을 반환합니다.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면, 라라벨이 자동으로 해당 로케일을 사용해 알림과 메일을 해당 모델에 전송합니다. 따라서, 이 방식을 쓸 때는 별도로 `locale` 메서드를 호출할 필요가 없습니다:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

알림이 실제로 전송되지 않도록 하려면, `Notification` 파사드의 `fake` 메서드를 사용할 수 있습니다. 보통 알림 전송은 여러분이 실제로 테스트하고자 하는 코드와는 무관합니다. 대부분의 경우, 라라벨이 특정 알림을 전송하도록 명령받았는지만 검증하면 충분합니다.

`Notification` 파사드의 `fake`를 호출한 후에는, 알림이 특정 사용자에게 전송되었는지, 또는 알림이 실제로 어떤 데이터를 받았는지 등을 assert로 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // Perform order shipping...

    // 알림이 전송되지 않았음을 assert...
    Notification::assertNothingSent();

    // 특정 사용자에게 알림이 전송되었음을 assert...
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // 알림이 전송되지 않았음을 assert...
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // 알림이 총 3건 전송되었음을 assert...
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

        // 알림이 전송되지 않았음을 assert...
        Notification::assertNothingSent();

        // 특정 사용자에게 알림이 전송되었음을 assert...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 알림이 전송되지 않았음을 assert...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 알림이 총 3건 전송되었음을 assert...
        Notification::assertCount(3);
    }
}
```

`assertSentTo` 또는 `assertNotSentTo` 메서드에 클로저를 전달하여, 특정 조건(진위 테스트)에 통과하는 알림이 전송되었는지까지 검증할 수 있습니다. 해당 진위 테스트를 통과한 알림이 한 건이라도 전송되었다면 assertion이 성공합니다:

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

테스트 중인 코드가 [온디맨드 알림](#on-demand-notifications)을 전송하는 경우, `assertSentOnDemand` 메서드를 통해 해당 알림이 정상적으로 전송되었는지 확인할 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` 메서드의 두 번째 인수로 클로저를 전달하면, 온디맨드 알림이 정확한 "라우트" 주소로 전송되었는지도 검증할 수 있습니다:

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
#### 알림 전송 이벤트(Notification Sending Event)

알림이 전송될 때, 알림 시스템은 `Illuminate\Notifications\Events\NotificationSending` 이벤트를 발생시킵니다. 이 이벤트 안에는 "notifiable" 엔티티와 알림 인스턴스가 담겨 있습니다. 애플리케이션에 [이벤트 리스너](/docs/12.x/events)를 등록하여 이 이벤트를 처리할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * 이벤트 처리 로직
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

만약 `NotificationSending` 이벤트에 대한 리스너의 `handle` 메서드에서 `false` 값을 반환하면, 해당 알림은 실제로 전송되지 않습니다:

```php
/**
 * 이벤트 처리 로직
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 리스너 안에서는 해당 알림 수신자(notifiable), 알림(notification), 그리고 채널(channel) 정보에 접근할 수 있으며, 이를 이용해 수신자나 알림 자체에 대한 추가 정보를 얻을 수 있습니다:

```php
/**
 * 이벤트 처리 로직
 */
public function handle(NotificationSending $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>

#### Notification Sent 이벤트

알림이 발송되면, 라라벨의 알림 시스템에서 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)가 디스패치됩니다. 이 이벤트는 "알림을 받을 대상(notifiable)" 엔터티와 해당 알림 인스턴스를 포함하고 있습니다. 애플리케이션 내에서 이 이벤트를 처리하는 [이벤트 리스너](/docs/12.x/events)를 자유롭게 생성할 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * 이벤트를 처리합니다.
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

이벤트 리스너 내부에서는 `notifiable`, `notification`, `channel`, `response`와 같은 프로퍼티를 통해, 알림의 수신자와 해당 알림에 대한 다양한 정보를 확인할 수 있습니다.

```php
/**
 * 이벤트를 처리합니다.
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
## 커스텀 채널

라라벨은 몇 가지 알림 채널을 기본으로 제공하지만, 여러분만의 드라이버를 만들어 다른 방식으로 알림을 전송하고 싶을 수도 있습니다. 라라벨에서는 커스텀 채널도 아주 쉽게 구현할 수 있습니다. 먼저, `send` 메서드를 포함하는 클래스를 하나 정의하세요. 이 메서드는 두 개의 인수, 즉 `$notifiable`과 `$notification`을 받아야 합니다.

`send` 메서드 내부에서는, 알림 인스턴스의 메서드를 호출해 해당 채널에서 이해할 수 있는 메시지 객체를 얻고, 원하는 방식대로 `$notifiable` 인스턴스에 알림을 전송하면 됩니다.

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

        // $notifiable 인스턴스에 알림을 전송합니다...
    }
}
```

커스텀 알림 채널 클래스를 정의한 후에는, 원하는 알림의 `via` 메서드에서 이 클래스명을 반환하면 됩니다. 아래 예제에서 알림의 `toVoice` 메서드는 음성 메시지를 나타낼 수 있는 어떤 객체든 반환할 수 있습니다. 예를 들어, 음성 메시지를 표현하기 위한 자체 `VoiceMessage` 클래스를 정의할 수도 있습니다.

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
     * 알림이 전송될 채널을 반환합니다.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * 알림의 음성 메시지 표현을 반환합니다.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```