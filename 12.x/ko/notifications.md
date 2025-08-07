# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레잇 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전송 채널 지정](#specifying-delivery-channels)
    - [알림 큐잉](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포매팅](#formatting-mail-messages)
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부 파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포매팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포매팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포매팅](#formatting-sms-notifications)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 레퍼런스 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포매팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림 전송](#notifying-external-slack-workspaces)
- [알림 지역화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [이메일 전송](/docs/12.x/mail) 지원 외에도, 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 기존 명칭 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 기능도 제공합니다. 또한, [커뮤니티 기반의 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)이 개발되어, 수십 가지 채널을 통해 사용자가 원하는 방식으로 알림을 전송할 수 있습니다! 알림을 데이터베이스에 저장해 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 특정 이벤트를 사용자에게 알리는 짧은 정보성 메시지입니다. 예를 들어, 결제 관련 애플리케이션을 개발한다면, 사용자가 청구서를 결제하면 이메일과 SMS 채널로 "청구서 결제 완료" 알림을 발송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성 (Generating Notifications)

Laravel에서 각 알림(notification)은 하나의 클래스로 표현되며, 일반적으로 `app/Notifications` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, `make:notification` Artisan 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 새로운 알림 클래스를 `app/Notifications` 디렉터리에 추가합니다. 각 알림 클래스에는 `via` 메서드와, 해당 채널 특성에 맞춘 `toMail` 또는 `toDatabase`와 같은 여러 가지 메시지 빌더 메서드가 포함됩니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레잇 사용

알림은 `Notifiable` 트레잇의 `notify` 메서드 또는 `Notification` [파사드](/docs/12.x/facades)를 통해 전송할 수 있습니다. `Notifiable` 트레잇은 애플리케이션의 기본 `App\Models\User` 모델에 기본적으로 포함되어 있습니다:

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

해당 트레잇이 제공하는 `notify` 메서드는 알림 인스턴스를 받아 처리합니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레잇은 어떤 모델에든 사용할 수 있습니다. 반드시 `User` 모델에만 포함해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

다른 방법으로는, `Notification` [파사드](/docs/12.x/facades)를 이용해 알림을 전송할 수 있습니다. 이 방법은 여러 알림 대상(예: 유저 컬렉션 등)에게 동시에 알림을 보내야 할 때 유용합니다. 파사드를 사용할 때는 모든 알림 대상과 알림 인스턴스를 `send` 메서드에 전달합니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

즉시 알림을 전송하고 싶다면 `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림 클래스가 `ShouldQueue` 인터페이스를 구현하더라도 즉시 알림을 전송합니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스는 `via` 메서드를 가지며, 이 메서드는 알림이 어떤 채널로 전송될지 결정합니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널을 기본적으로 지원합니다.

> [!NOTE]
> Telegram, Pusher 등 다른 채널을 사용하고 싶다면 커뮤니티에서 제공하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 전달받으며, 알림이 전송되는 대상 객체 인스턴스입니다. `$notifiable`을 이용해 어느 채널로 전송할지 동적으로 결정할 수 있습니다:

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
> 알림을 큐로 처리하기 전에 큐를 구성하고 [워커를 시작](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림 전송 중 외부 API 호출 등의 작업이 필요하다면 시간이 오래 걸릴 수 있습니다. 응답 속도를 높이기 위해, 알림 클래스를 큐에 넣어 비동기로 처리할 수 있습니다. 이를 위해 `ShouldQueue` 인터페이스와 `Queueable` 트레잇을 알림 클래스에 추가하세요. 이 인터페이스와 트레잇은 `make:notification` 명령어로 생성되는 모든 알림에 미리 임포트되어 있습니다.

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

`ShouldQueue` 인터페이스가 추가된 후에는 기존과 똑같이 알림을 전송하면 됩니다. Laravel은 해당 인터페이스를 감지해 자동으로 알림을 큐 작업으로 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐에 올릴 때는 수신자와 채널의 조합 별로 별도의 큐 작업이 생성됩니다. 예를 들어, 수신자가 3명이고 채널이 2개라면 6개의 작업이 큐에 들어갑니다.

<a name="delaying-notifications"></a>
#### 알림 지연 전송

알림 전송을 지연하려면 알림 인스턴스 생성 시 `delay` 메서드를 체이닝하세요:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

여러 채널에 대해 각각 지연시간을 다르게 설정하려면 배열을 전달하세요:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스에 `withDelay` 메서드를 정의해도 됩니다. 이 메서드는 채널별 지연시간을 배열로 반환해야 합니다:

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

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림에 대해 다른 큐 연결을 지정하려면 알림 생성자에서 `onConnection` 메서드를 호출하세요:

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

또는 알림이 지원하는 각 채널별로 큐 연결을 다르게 지정하려면 `viaConnections` 메서드를 정의하세요. 이 메서드는 채널 이름과 큐 연결 이름의 쌍으로 이루어진 배열을 반환해야 합니다:

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
#### 각 채널별 큐 이름 커스터마이즈

지원되는 각 채널별로 사용할 큐 이름을 지정하려면 `viaQueues` 메서드를 정의하세요:

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
#### 큐잉된 알림용 미들웨어

큐잉된 알림에서는 [큐 작업 미들웨어](/docs/12.x/queues#job-middleware)처럼 미들웨어를 정의할 수 있습니다. 알림 클래스에 `middleware` 메서드를 추가하면 됩니다. 이 메서드는 `$notifiable`과 `$channel` 변수를 받으며, 알림 대상에 따라 반환할 미들웨어를 조건부로 구성할 수 있습니다:

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
#### 큐 알림과 데이터베이스 트랜잭션

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치되면, 트랜잭션이 커밋되기 전 큐가 먼저 알림을 처리할 수 있습니다. 이 경우, 트랜잭션 내에서 변경된 모델이나 레코드가 아직 데이터베이스에 반영되지 않았을 수 있으며, 트랜잭션 내에서 생성한 데이터도 존재하지 않을 수 있습니다. 알림이 이런 모델에 의존한다면, 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`인 경우에도, 알림 전송 시점에 `afterCommit` 메서드를 체이닝해, 모든 열린 트랜잭션이 커밋된 후에만 알림을 디스패치하도록 할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스 생성자에서 `afterCommit`을 호출해도 됩니다:

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
> 이러한 문제를 해결하는 자세한 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 실제 전송 여부 제어

큐에 들어간 알림이 백그라운드에서 처리될 때, 실제로 수신자에게 보낼지 최종적으로 결정하고 싶다면 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림이 전송되지 않습니다:

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

애플리케이션의 "유저"로 저장되지 않은 누군가에게 알림을 보내야 할 때가 있습니다. 이 경우 `Notification` 파사드의 `route` 메서드를 사용하여 임시 라우팅 정보를 지정한 뒤 알림을 전송할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

온디맨드 방식으로 `mail` 라우트로 알림을 보낼 때, 수신인 이름을 지정하려면 배열 형태로 이메일 주소와 이름을 함께 넘기면 됩니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 채널에 대한 임시 라우팅 정보를 한꺼번에 지정할 수 있습니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림 (Mail Notifications)

<a name="formatting-mail-messages"></a>
### 메일 메시지 포매팅

알림을 이메일로 보낼 수 있도록 지원하려면 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 객체를 받아 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스에는 거래 관련 이메일을 쉽게 작성할 수 있는 몇 가지 주요 메서드가 준비되어 있습니다. 메일 메시지에는 여러 줄의 텍스트와 행동 유도("call to action") 버튼을 포함할 수 있습니다. 예시:

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
> 본 예시에서 `toMail` 메서드에 `$this->invoice->id`를 사용했습니다. 알림 생성자에 필요한 데이터를 전달해 사용할 수 있습니다.

이 예시에서는 인사말, 텍스트 한 줄, 행동 유도 버튼, 그리고 다시 한 줄의 텍스트를 추가하고 있습니다. `MailMessage`의 직관적인 메서드를 사용해 짧고 간단한 거래 메일을 손쉽게 포매팅할 수 있습니다. `mail` 채널은 이 내용을 예쁜 반응형 HTML 메일(및 플레인 텍스트 대체본)로 변환해줍니다.

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 전송할 때는 반드시 `config/app.php` 설정 파일의 `name` 옵션을 설정해야 합니다. 이 값은 메일 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

일부 알림은 결제 실패와 같은 오류 상황을 사용자에게 안내하기도 합니다. `MailMessage`에서 `error` 메서드를 호출하면 해당 메일이 에러와 관련되었음을 표시할 수 있으며, 이 경우 행동 유도 버튼은 검정이 아닌 빨간색으로 표시됩니다.

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
#### 다른 메일 알림 포매팅 옵션

알림 클래스 내에서 직접 텍스트 라인을 정의하는 대신, `view` 메서드를 통해 메일 알림에 사용할 커스텀 템플릿을 지정할 수 있습니다:

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

`view` 메서드에 배열로 플레인 텍스트 뷰까지 같이 전달해줄 수도 있습니다:

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

메시지가 오로지 플레인 텍스트로만 이루어진 경우엔 `text` 메서드를 사용할 수 있습니다:

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

기본적으로 이메일의 발신자(From) 주소는 `config/mail.php` 설정 파일에서 정의됩니다. 특정 알림에서 발신자를 바꾸고 싶다면 `from` 메서드를 사용하세요:

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

`mail` 채널로 알림을 전송할 때, 시스템은 자동으로 notifiable 객체의 `email` 속성을 찾아 사용합니다. 어떤 속성을 메일 주소로 쓸지 직접 지정하려면 notifiable 객체에 `routeNotificationForMail` 메서드를 정의하세요:

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
        // 이메일 주소만 반환
        return $this->email_address;

        // 이메일 주소와 이름 함께 반환
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 이메일의 제목(subject)은 알림 클래스명을 "타이틀 케이스"로 변환한 값입니다. 예를 들어 `InvoicePaid`라면 제목은 `Invoice Paid`가 됩니다. 제목을 직접 지정하려면 메시지 빌딩 시 `subject` 메서드를 사용하세요:

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

기본적으로 이메일 알림은 `config/mail.php`에 정의된 기본 메일러를 사용합니다. 다른 메일러를 사용하고 싶을 경우 `mailer` 메서드를 호출하여 런타임 시 지정할 수 있습니다:

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

메일 알림에 사용되는 HTML 및 플레인 텍스트 템플릿을 커스터마이즈하고 싶다면, notification 패키지의 리소스를 퍼블리시하세요. 아래 명령어 실행 시 템플릿이 `resources/views/vendor/notifications`에 복사됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부 파일

이메일 알림에 파일을 첨부하려면, 메시지 빌딩 중 `attach` 메서드를 사용합니다. `attach`에는 첨부할 파일의 절대 경로를 첫 번째 인자로 전달합니다:

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
> notification 메일 메시지의 `attach` 메서드는 [Attachable 객체](/docs/12.x/mail#attachable-objects)도 지원합니다. 더욱 자세한 내용은 [attachable object 문서](/docs/12.x/mail#attachable-objects)를 참고하세요.

첨부 파일의 표시 이름과 MIME 타입을 지정하고 싶다면, 두 번째 인자로 배열을 넘기세요:

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

메일러 객체(mailable)와 다르게 `attachFromStorage`로 스토리지 디스크에서 직접 첨부할 수는 없습니다. 절대 경로를 사용하거나, `toMail`에서 [mailable](/docs/12.x/mail#generating-mailables)을 반환하는 방식을 고려해야 합니다:

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

여러 파일을 한 번에 첨부하고 싶다면 `attachMany` 메서드를 사용하세요:

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

`attachData` 메서드를 사용하면 바이트 스트링 그대로 첨부파일을 만들 수 있습니다. 파일명도 지정해야 합니다:

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

Mailgun, Postmark 등 일부 서드파티 이메일 플랫폼은 메시지 "태그"나 "메타데이터"를 통해 발송 이메일을 그룹화하거나 추적할 수 있습니다. 알림 메일에서 `tag`, `metadata` 메서드로 해당 정보를 추가할 수 있습니다:

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

Mailgun 환경에서는 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages), Postmark의 경우 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 공식 문서를 참고하세요.

Amazon SES를 사용하는 경우 SES ["tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)는 `metadata` 메서드를 통해 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 사용하면, Symfony Message 인스턴스가 전송되기 전 커스터마이즈할 수 있는 클로저를 등록할 수 있습니다. 이를 활용해 메시지에 심도 있게 수정할 수 있습니다:

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
### Mailable 사용

필요하다면, 알림의 `toMail` 메서드에서 [mailable 객체](/docs/12.x/mail)를 반환해도 됩니다. 이 경우는 mailable 객체에서 수신자 지정이 필요합니다.

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
#### Mailable과 온디맨드 알림

[온디맨드 알림](#on-demand-notifications)을 보낼 때, `toMail` 메서드로 전달되는 `$notifiable` 객체는 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스입니다. 이 객체의 `routeNotificationFor` 메서드를 사용해 이메일 주소를 얻을 수 있습니다:

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

메일 알림 템플릿을 작성할 때, 실제 이메일을 보내지 않고도 브라우저에서 바로 미리보기가 가능합니다. 라우트 클로저 또는 컨트롤러에서 알림의 mail 메시지를 반환하면, 이를 브라우저에서 렌더링해 빠르게 결과를 확인할 수 있습니다:

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
## 마크다운 메일 알림 (Markdown Mail Notifications)

마크다운 메일 알림은 기본 제공되는 알림 템플릿의 장점을 활용하면서도, 좀 더 길고 맞춤화된 메시지를 마크다운 문법으로 작성할 수 있는 기능을 제공합니다. Laravel은 마크다운 메시지를 예쁘고 반응형인 HTML 템플릿과 자동으로 생성되는 플레인 텍스트 버전으로 변환해줍니다.

<a name="generating-the-message"></a>
### 메시지 생성

마크다운 템플릿이 포함된 알림을 생성하려면, `make:notification` Artisan 명령어에서 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

생성된 알림 클래스에서도 기존과 마찬가지로 `toMail` 메서드를 정의하면 됩니다. 그러나 `line`과 `action` 대신, `markdown` 메서드를 사용하여 사용할 마크다운 템플릿 이름을 지정할 수 있습니다. 템플릿에 넘길 데이터는 두 번째 인자로 배열로 전달합니다:

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
### 메시지 작성

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법을 결합해, Laravel의 알림 컴포넌트를 적극적으로 활용할 수 있습니다:

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
> 마크다운 이메일 작성 시, 과도한 들여쓰기를 피하세요. 마크다운 규칙상 들여쓰기가 많은 컨텐츠는 Code Block으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color`(지원 색상: `primary`, `green`, `red`)를 인수로 사용합니다. 원하는 만큼 여러 버튼 컴포넌트를 추가해도 무방합니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블럭을 약간 다른 색상의 패널에 배치해 강조 효과를 줍니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 표를 HTML 테이블로 변환하여 렌더링합니다. 기본 마크다운 표 정렬 문법도 지원합니다:

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

모든 마크다운 알림 컴포넌트를 애플리케이션에 내보내 customizing할 수 있습니다. `vendor:publish` Artisan 명령어로 `laravel-mail` 에셋 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

명령 실행 시 `resources/views/vendor/mail` 폴더에 마크다운 메일 컴포넌트가 복사됩니다. `mail` 폴더 내에는 각각 `html`, `text` 디렉터리와 각 컴포넌트별 템플릿이 제공되며, 자유롭게 수정 가능합니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 내보내기 후, `resources/views/vendor/mail/html/themes` 폴더에 `default.css` 파일이 있습니다. 원하는 스타일로 CSS를 수정하면 해당 스타일이 자동으로 HTML 버전의 마크다운 알림 내에 인라인 처리됩니다.

새로운 마크다운 테마를 만들고 싶다면, `html/themes` 폴더에 CSS 파일을 추가하고, `mail` 설정 파일의 `theme` 항목을 새 테마 이름으로 변경하면 됩니다.

개별 알림에서 사용할 테마를 바꾸려면 mail 메시지 빌더에 `theme` 메서드를 호출하세요:

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
## 데이터베이스 알림 (Database Notifications)

<a name="database-prerequisites"></a>
### 사전 준비

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 타입, 알림을 설명하는 JSON 데이터 구조 등이 들어갑니다.

이 테이블에서 정보를 쿼리하여 애플리케이션에서 알림을 표시할 수 있습니다. 먼저 알림을 저장할 데이터베이스 테이블을 생성해야 하며, `make:notifications-table` 명령어로 [마이그레이션](/docs/12.x/migrations)을 생성할 수 있습니다:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> notifiable 모델이 [UUID 또는 ULID 기본키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용하는 경우, notification 마이그레이션에서 `morphs` 대신 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)를 사용해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포매팅

알림을 데이터베이스에 저장할 수 있게 하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의하세요. 이 메서드는 `$notifiable` 인스턴스를 받아 플레인 PHP 배열을 반환해야 하며, 반환값은 JSON으로 인코드되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 다음은 예시입니다:

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

알림이 데이터베이스에 저장되면 `type` 컬럼은 기본적으로 알림 클래스명, `read_at` 컬럼은 `null`로 셋팅됩니다. 이 동작을 커스터마이즈하려면 `databaseType` 및 `initialDatabaseReadAtValue` 메서드를 알림 클래스에 정의하면 됩니다:

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

`toArray` 메서드는 `broadcast` 채널에서도 데이터를 가져올 때 사용됩니다. `database`와 `broadcast` 채널에 서로 다른 구조의 데이터를 저장하고 싶다면, `toArray` 대신 `toDatabase` 메서드를 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근

알림이 데이터베이스에 저장된 후, notifiable 객체에서 편리하게 접근할 수 있어야 합니다. Laravel의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레잇에는 해당 엔티티의 알림을 반환하는 [Eloquent 연관관계](/docs/12.x/eloquent-relationships) `notifications`가 포함되어 있습니다. 다음처럼 사용할 수 있습니다. 기본적으로는 `created_at` 기준 내림차순으로 정렬됩니다(최신 알림이 먼저):

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않음(unread)" 알림만 가져오려면 `unreadNotifications` 연관관계를 이용하세요:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

"읽음(read)" 알림만 가져올 땐 `readNotifications` 연관관계를 사용하세요:

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림을 조회하려면, notifiable에 대한 알림을 반환하는 컨트롤러를 구현하고, 해당 URL로 HTTP 요청을 날려야 합니다.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리

일반적으로 사용자가 알림을 확인하면 "읽음" 처리해야 합니다. `Illuminate\Notifications\Notifiable` 트레잇은 알림 DB 레코드의 `read_at` 컬럼을 갱신하는 `markAsRead` 메서드를 제공합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

반복문 없이도, 알림 컬렉션 자체에 `markAsRead`를 직접 호출할 수 있습니다:

```php
$user->unreadNotifications->markAsRead();
```

모든 알림을 한꺼번에 "읽음" 처리하려면 마스-업데이트 쿼리를 사용할 수도 있습니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 DB에서 완전히 삭제하려면 `delete` 메서드를 사용할 수 있습니다:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림 (Broadcast Notifications)

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하기 전에, Laravel의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 기능을 이해하고 설정해야 합니다. 이벤트 브로드캐스팅 기능은 서버에서 발생한 Laravel 이벤트에 자바스크립트 프론트엔드가 실시간으로 반응할 수 있게 해줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포매팅

`broadcast` 채널은 Laravel의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 기능을 활용해, 자바스크립트 프론트엔드에서 실시간으로 알림을 수신할 수 있도록 브로드캐스팅합니다. 알림 클래스에 `toBroadcast` 메서드를 정의하면 알림을 브로드캐스트로 지원할 수 있습니다. 이 메서드는 `$notifiable` 인스턴스를 받아 `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast`가 없으면 `toArray`가 데이터 공급에 사용됩니다.

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

모든 브로드캐스트 알림은 큐에 등록되어 전송됩니다. 사용되는 큐 연결 또는 큐 이름을 지정하려면 `BroadcastMessage`의 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

데이터 이외에, 모든 브로드캐스트 알림에는 전체 클래스명이 포함된 `type` 필드가 추가됩니다. 타입 값 자체를 커스터마이즈하려면 알림 클래스에 `broadcastType` 메서드를 정의하세요:

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
### 알림 수신 대기

알림은 `{notifiable}.{id}` 형식의 프라이빗 채널에서 브로드캐스트됩니다. 예를 들어, ID가 `1`인 `App\Models\User` 인스턴스에 알림을 보낸다면, `App.Models.User.1` 채널에서 방송됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용하면 `notification` 메서드로 간편하게 수신할 수 있습니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue에서 사용

Laravel Echo는 React, Vue용 Hooks를 제공해 알림 수신을 더욱 쉽게 만듭니다. `useEchoNotification` 훅을 호출하여 알림을 수신하세요. 이 훅은 컴포넌트가 언마운트되면 자동으로 채널에서 떠납니다:

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

기본적으로 훅은 모든 알림을 수신하지만, 특정 타입만 지정할 수도 있습니다:

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

알림 데이터 구조의 타입을 명확히 지정해 더욱 안전하게 사용할 수 있습니다:

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
#### 알림 채널명 커스터마이즈

엔티티의 브로드캐스트 알림이 어느 채널로 방송될지 커스터마이즈하고 싶을 때는, notifiable 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하세요:

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
## SMS 알림 (SMS Notifications)

<a name="sms-prerequisites"></a>
### 사전 준비

Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/)가 담당합니다(이전 명칭 Nexmo). Vonage로 알림을 전송하려면, `laravel/vonage-notification-channel`과 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)을 포함합니다. 별도로 가져오지 않아도 되며, 환경 변수 `VONAGE_KEY`, `VONAGE_SECRET`를 통해 Vonage 키 정보를 지정하면 됩니다.

키를 지정한 뒤에는 발신 번호를 의미하는 `VONAGE_SMS_FROM` 환경 변수를 지정해야 하며, 해당 번호는 Vonage 콘트롤 패널에서 발급받을 수 있습니다:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포매팅

알림을 SMS로 보낼 수 있도록 하려면, 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

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
#### 유니코드 문자 지원

SMS 메시지에 유니코드가 포함된다면, `unicode` 메서드를 호출해 반드시 올바르게 처리해야 합니다:

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
### "From" 번호 커스터마이징

기본 발신 번호 외 다른 번호로 특정 알림을 보내고 싶다면 VonageMessage의 `from` 메서드를 사용하세요:

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
### 클라이언트 레퍼런스 추가

사용자·팀·고객별 SMS 비용을 추적하려면 "클라이언트 레퍼런스"를 첨부할 수 있습니다. Vonage에서는 이 값을 기준으로 SMS 사용량 리포트를 생성할 수 있습니다. 이 값은 40자 이하의 문자열이면 됩니다:

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

Vonage 알림을 올바른 전화번호로 보내려면, notifiable 엔티티에 `routeNotificationForVonage` 메서드를 정의해야 합니다:

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
## Slack 알림 (Slack Notifications)

<a name="slack-prerequisites"></a>
### 사전 준비

Slack 알림 전송 전 Composer를 통해 Slack 채널을 설치해야 합니다:

```shell
composer require laravel/slack-notification-channel
```

그리고 [Slack App](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

동일 워크스페이스 내에서만 사용한다면 Slack App에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한이 있어야 하며, "OAuth & Permissions" 탭에서 설정 가능합니다.

다음으로, "Bot User OAuth Token"을 앱의 `services.php` 설정 파일의 slack 설정 배열에 입력하세요:

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

외부 워크스페이스(사용자 소유)로 알림을 보내려면 Slack App을 "배포"해야 합니다. "Manage Distribution" 메뉴를 통해 배포를 진행한 뒤, [Socialite](/docs/12.x/socialite)로 [Slack Bot 토큰 발급](/docs/12.x/socialite#slack-bot-scopes)을 지원할 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포매팅

Slack 메시지 전송을 지원하려면, 알림 클래스에 `toSlack` 메서드를 정의하세요. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환합니다. [Slack Block Kit API](https://api.slack.com/block-kit)를 활용해 다양한 알림 서식을 만들 수 있습니다. 예제:

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
#### Slack Block Kit Builder 템플릿 사용

플루언트 빌더 대신, Block Kit Builder에서 생성한 JSON 템플릿을 `usingBlockKitTemplate` 메서드에 전달할 수도 있습니다:

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
### Slack 상호작용

Slack의 Block Kit 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling)를 위한 강력한 기능을 제공합니다. Slack App에서 "Interactivity"를 활성화하고, 애플리케이션의 엔드포인트를 "Request URL"에 지정해야 합니다.

아래 예시처럼, `actionsBlock`을 이용해 버튼을 추가하면 Slack이 해당 사용, 버튼 ID 등 관련 데이터를 `POST`로 전달합니다. 이에 따라 필요한 처리를 할 수 있습니다.

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
             // ID 기본값: "button_acknowledge_invoice"
            $block->button('Acknowledge Invoice')->primary();

            // ID 직접 정의
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달 사용

행동 전 사용자의 확인을 요청해야 할 경우, 버튼 정의 시 `confirm` 메서드를 사용하세요:

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
#### Slack 블록 미리보기

작성한 블록을 빠르게 확인하고 싶다면 `SlackMessage` 인스턴스의 `dd` 메서드를 호출하세요. 이 메서드는 [Block Kit Builder](https://app.slack.com/block-kit-builder/) URL을 생성해 줍니다. 파라미터로 `true`를 전달하면 원본 페이로드를 확인할 수 있습니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 올바른 팀 및 채널로 보내려면 notifiable 모델에 `routeNotificationForSlack` 메서드를 정의해야 합니다. 반환값은 다음 중 하나입니다:

- `null`: notification 클래스 내에서 채널 지정(예: `to` 메서드로 설정)
- 문자열: Slack 채널 지정(예: `#support-channel`)
- `SlackRoute` 인스턴스: OAuth 토큰과 채널명 모두 지정(외부 워크스페이스용)

예시:

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
### 외부 Slack 워크스페이스 알림 전송

> [!NOTE]
> 외부 워크스페이스 알림 전송시, Slack App의 [배포](#slack-app-distribution)가 선행되어야 합니다.

애플리케이션 사용자의 Slack 워크스페이스로 직접 알림을 보내는 경우가 많습니다. 이를 위해서는 먼저 사용자별 Slack OAuth 토큰을 획득해야 합니다. [Laravel Socialite](/docs/12.x/socialite)가 Slack 드라이버를 제공하여 인증 및 [Bot 토큰 발급](/docs/12.x/socialite#slack-bot-scopes)을 쉽게 할 수 있습니다.

토큰을 DB 등에 보관한 후에는 `SlackRoute::make` 메서드를 사용해 알림을 해당 워크스페이스의 지정 채널로 라우팅할 수 있습니다:

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
## 알림 지역화 (Localizing Notifications)

Laravel은 현재 HTTP 요청의 언어(locale)와 상관없이 특정 로케일로 알림을 보낼 수 있으며, 알림이 큐에 들어간다 해도 이 로케일 정보를 기억합니다.

이를 위해서는 `Illuminate\Notifications\Notification` 클래스의 `locale` 메서드를 사용하여 원하는 언어를 지정할 수 있습니다. 알림 평가 중에는 해당 locale로 전환되며, 평가가 끝나면 이전 locale로 되돌아갑니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 명의 notifiable 엔티티에 지역화된 알림을 보낼 때는 Notification 파사드를 활용할 수 있습니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

사용자별로 선호하는 로케일을 저장하는 경우, notifiable 모델에서 `HasLocalePreference` 계약을 구현하면 됩니다. 이를 통해 Laravel은 알림/메일 발송 시 자동으로 해당 로케일을 사용합니다:

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

이 인터페이스를 구현했다면, `locale` 메서드를 따로 호출할 필요 없이 알림/메일 전송 시 자동으로 preferred locale이 반영됩니다:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시 notificaion이 실제로 전송되지 않게 하려면 `Notification` 파사드의 `fake` 메서드를 사용하세요. 일반적으로 알림 전송 자체는 실제 테스트 대상이 아니므로 알림이 전송 호출만 되었는지 assert하는 것으로 충분합니다.

`Notification::fake()` 호출 이후에는, 알림 전송/미전송 여부, 전송 대상, 채널 등의 정보까지 assert가 가능합니다:

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // Perform order shipping...

    // 아무 알림도 전송되지 않았는지 확인
    Notification::assertNothingSent();

    // 특정 유저에게 해당 알림이 전송되었는지 확인
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // 알림이 전송되지 않았는지 확인
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // 총 3건 발송되었는지 확인
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

        // 아무 알림도 전송되지 않았는지 확인
        Notification::assertNothingSent();

        // 특정 유저에게 해당 알림이 전송되었는지 확인
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 알림이 전송되지 않았는지 확인
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 해당 알림이 2번 전송되었는지 확인
        Notification::assertSentTimes(WeeklyReminder::class, 2);

        // 총 3건 발송되었는지 확인
        Notification::assertCount(3);
    }
}
```

`assertSentTo`, `assertNotSentTo` 메서드에는 클로저를 전달해 특정 조건을 만족하는 알림이 전송되었는지 판별할 수 있습니다. "진실성 테스트"를 통과한 알림이 하나라도 있으면 assert가 성공합니다:

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

[온디맨드 알림](#on-demand-notifications) 전송 여부를 테스트할 땐 `assertSentOnDemand` 메서드를 사용할 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인자로 클로저를 전달하면 특정 "route" 주소로 온디맨드 알림이 전송됐는지 확인할 수 있습니다:

```php
Notification::assertSentOnDemand(
    OrderShipped::class,
    function (OrderShipped $notification, array $channels, object $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="notification-events"></a>
## 알림 이벤트 (Notification Events)

<a name="notification-sending-event"></a>
#### NotificationSending 이벤트

알림이 전송될 때, `Illuminate\Notifications\Events\NotificationSending` 이벤트가 항상 디스패치됩니다. 이 이벤트에는 notifiable 엔티티, 알림 인스턴스 등이 포함됩니다. 애플리케이션 내에서 [이벤트 리스너](/docs/12.x/events)를 구현할 수 있습니다:

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

리스너가 `handle` 메서드에서 `false`를 반환하면 알림은 전송되지 않습니다:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 리스너 내부에서 아래 속성에 접근할 수 있습니다:

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

알림이 실제 전송된 후에는 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)가 디스패치됩니다. 역시 notifiable 엔티티, 알림 인스턴스 등이 전달되며, [리스너](/docs/12.x/events)에서 처리할 수 있습니다:

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

리스너 내부에서는 아래 속성에도 접근이 가능합니다:

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
## 커스텀 채널 (Custom Channels)

Laravel에는 여러가지 알림 채널이 기본으로 포함되어 있지만, 필요에 따라 새 드라이버를 직접 구현할 수도 있습니다. 클래스를 정의하고, `send` 메서드에서 `$notifiable`과 `$notification`을 받아 처리하면 됩니다.

`send` 메서드에서 알림의 메시지 객체를 얻어 해당 notifiable 인스턴스에 전달만 하면 됩니다:

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

        // $notifiable 인스턴스로 알림 전송
    }
}
```

정의한 채널 클래스를 알림의 `via` 메서드에서 반환하면, 이를 이용해 알림을 전송할 수 있습니다. 이 때, 예를 들어 `toVoice` 등의 메서드에서 직접 포맷한 메시지 객체(`VoiceMessage` 등)를 반환합니다:

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
