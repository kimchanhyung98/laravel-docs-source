# 알림 (Notifications)

- [소개](#introduction)
- [알림 클래스 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레이트 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전송 채널 지정](#specifying-delivery-channels)
    - [알림 큐 처리](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 지정](#customizing-the-sender)
    - [수신자 지정](#customizing-the-recipient)
    - [제목 지정](#customizing-the-subject)
    - [메일러 지정](#customizing-the-mailer)
    - [템플릿 커스터마이즈](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
    - [Mailable 활용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [알림 포맷팅](#formatting-database-notifications)
    - [알림 조회](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 감지](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - ["From" 번호 지정](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림 로컬화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

[이메일 전송](/docs/12.x/mail) 지원 외에도, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전명 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널로 알림을 전송할 수 있는 기능을 제공합니다. 또한, [커뮤니티에서 제작한 다양한 알림 채널들](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 활용하면 수십 가지의 경로로 알림을 보낼 수도 있습니다! 알림을 데이터베이스에 저장해 웹 인터페이스에 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 사건을 사용자에게 알려주는 짧고 정보 전달 위주인 메시지로 설계하는 것이 좋습니다. 예를 들어 빌링 애플리케이션을 개발할 때, "송장 결제 완료" 알림을 이메일 및 SMS 채널을 통해 사용자에게 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 클래스 생성 (Generating Notifications)

Laravel에서 각 알림은 일반적으로 `app/Notifications` 디렉토리에 저장되는 하나의 클래스로 표현됩니다. 이 디렉토리가 없다면 걱정하지 마세요. `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령을 실행하면, `app/Notifications` 디렉토리에 새로운 알림 클래스가 생성됩니다. 각각의 알림 클래스는 필수적으로 `via` 메서드를 포함하고 있으며, `toMail` 또는 `toDatabase` 등과 같은 채널별 메시지 생성 메서드를 원하는 수만큼 정의할 수 있습니다. 이러한 메서드는 해당 채널에 맞는 메시지로 알림 객체를 변환해줍니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, `Notification` [파사드](/docs/12.x/facades)를 사용해 전송할 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 적용되어 있습니다:

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

이 트레이트의 `notify` 메서드는 알림 인스턴스를 인수로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에든 사용할 수 있습니다. 반드시 `User` 모델에만 적용해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는 `Notification` [파사드](/docs/12.x/facades)를 통해 알림을 전송할 수도 있습니다. 이 방식은 여러 개의 notifiable 엔티티(예: 여러 명의 사용자)에게 동시에 알림을 전송해야 할 때 유용합니다. 파사드의 `send` 메서드에 모든 notifiable 엔티티와 알림 인스턴스를 전달하세요:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

또한, 알림 클래스가 `ShouldQueue` 인터페이스를 구현하더라도, `sendNow` 메서드를 사용하여 즉시 알림을 보낼 수 있습니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스는 알림을 어떤 채널로 보낼지 결정하는 `via` 메서드를 가지고 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 등의 채널로 전송할 수 있습니다.

> [!NOTE]
> Telegram, Pusher와 같은 기타 채널을 사용하고 싶다면, 커뮤니티 주도의 [Laravel Notification Channels 사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 전달받으며, 이를 활용해 알림 채널을 동적으로 지정할 수 있습니다:

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
### 알림 큐 처리

> [!WARNING]
> 알림 큐 사용 전에는 먼저 큐 설정을 마치고, [워커를 실행](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

특정 채널이 외부 API 호출 등을 요구하는 경우, 알림 전송에 시간이 걸릴 수 있습니다. 애플리케이션 응답 속도를 높이기 위해, 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해 알림을 큐에 넣는 것이 좋습니다. 이 인터페이스와 트레이트는 `make:notification` 명령어로 생성되는 기본 알림에 이미 import되어 있으므로 바로 추가 사용할 수 있습니다:

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

`ShouldQueue` 인터페이스를 추가하면, 기존 방식대로 알림을 보내도 Laravel이 자동으로 큐 처리해줍니다:

```php
$user->notify(new InvoicePaid($invoice));
```

큐잉 시, 각 수신자와 채널 조합마다 별도의 큐 작업이 생성됩니다. 예를 들어 3명의 수신자, 2개의 채널이라면 6개의 작업이 큐에 등록됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연 전송

알림을 일정 시간 지연 후 전송하고 싶을 경우, 알림 인스턴스 생성 뒤에 `delay` 메서드를 체이닝해 사용할 수 있습니다:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

채널별로 지연 시간을 다르게 지정하려면 배열을 전달하면 됩니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는, 알림 클래스에 `withDelay` 메서드를 정의해 채널별 지연 시간을 지정할 수도 있습니다:

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
#### 알림 큐 연결선 지정

기본적으로 큐 작업은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림만 별도의 큐 연결을 사용하고 싶다면, 생성자에서 `onConnection` 메서드를 호출하세요:

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

또는, 채널별로 각각 다른 큐 연결을 지정하고 싶을 경우, 알림 클래스에 `viaConnections` 메서드를 정의하세요. 이 메서드는 채널명/연결명 쌍의 배열을 반환해야 합니다:

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

채널별로 작업이 저장될 큐 이름을 분리할 수도 있습니다. 이를 위해서는 `viaQueues` 메서드를 알림 클래스에 정의합니다:

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

알림도 [큐 작업처럼](/docs/12.x/queues#job-middleware) 미들웨어 사용이 가능합니다. 이를 위해, 알림 클래스에 `middleware` 메서드를 정의하세요. `$notifiable`과 `$channel` 변수를 인수로 받아 목적지별로 조건을 추가할 수 있습니다:

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

데이터베이스 트랜잭션 내에서 큐 알림을 디스패치할 경우, 큐 작업이 트랜잭션 커밋 전에 실행될 수도 있습니다. 이때 트랜잭션 내 데이터베이스 업데이트가 아직 완료되지 않았으므로, 관련된 데이터가 반영되지 않을 수 있습니다. 이런 문제를 방지하거나 감지하려면, 큐 연결의 `after_commit` 옵션이 `false`인 경우에도, 알림을 전송할 때 `afterCommit` 메서드를 호출해 모든 트랜잭션 커밋 후에 디스패치되도록 지정할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 생성자에서 `afterCommit`을 호출해도 됩니다:

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
> 관련 문제 해결을 위해 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서도 참고하시기 바랍니다.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림 전송 여부 결정

큐 알림이 실제로 수신자에게 전송되기 전에 마지막으로 전송 여부를 통제하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. 해당 메서드가 `false`를 반환하면 알림이 전송되지 않습니다:

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

애플리케이션 사용자로 등록되어 있지 않은 대상에게도 알림을 보내고 싶을 때가 있습니다. `Notification` 파사드의 `route` 메서드를 사용하면 알림 라우팅 정보를 임시로 지정해 알림을 보낼 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일 라우트로 온디맨드 알림을 보낼 때, 수신자 이름을 함께 지정하려면 다음과 같이 이메일 주소를 키, 이름을 값으로 전달합니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널의 라우팅 정보를 한 번에 지정하려면 `routes` 메서드를 사용합니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림 (Mail Notifications)

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅

알림이 이메일 전송을 지원하려면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션성 이메일을 쉽게 구성할 수 있도록 몇 가지 간결한 메서드를 제공합니다. 메일 메시지는 텍스트 라인과 "행동 유도(call to action)" 버튼을 포함할 수 있습니다. 아래는 `toMail` 메서드의 예시입니다:

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
> `toMail` 메서드에서 `$this->invoice->id`처럼 알림 인스턴스 내 데이터를 자유롭게 사용할 수 있습니다. 필요한 데이터는 알림 클래스의 생성자를 통해 전달하면 됩니다.

위 예시에서는 인삿말, 텍스트 라인, 행동 유도 버튼, 추가 텍스트 라인을 순서대로 추가하는 모습을 볼 수 있습니다. `MailMessage` 오브젝트에서 제공하는 메서드를 활용하면 소규모 트랜잭션성 이메일 양식을 쉽고 빠르게 만들 수 있습니다. 메일 채널은 이 내용을 보기 좋은 반응형 HTML 이메일 템플릿과 플레이  
텍스트 버전으로 자동 변환합니다.  
아래는 `mail` 채널로 생성된 이메일 예시입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림 전송 시, 반드시 `config/app.php`의 `name` 설정 값을 지정하세요. 이 값은 알림 메시지의 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

알림이 결제 실패 같은 오류를 안내하는 경우, `error` 메서드를 호출해 메일 메시지가 에러 관련임을 표시할 수 있습니다. `error` 메서드를 사용하면 행동 유도 버튼 색상이 빨간색으로 바뀝니다:

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
#### 기타 메일 알림 포맷팅 옵션

알림 클래스 내에서 직접 "line" 메서드 대신, `view` 메서드를 활용해 이메일을 렌더링할 Blade 템플릿을 지정할 수 있습니다:

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

메일 메시지에 플레이  
텍스트 뷰도 함께 지정하려면, 뷰 이름을 배열로 전달하세요:

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

메시지가 오직 플레이  
텍스트만 있으면 `text` 메서드를 사용할 수 있습니다:

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
### 발신자 지정

기본적으로 전송되는 이메일의 발신(From) 주소는 `config/mail.php` 파일에 정의된 값을 따릅니다. 하지만, 특정 알림만 별도로 발신자를 지정하고 싶다면, `from` 메서드를 사용하세요:

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
### 수신자 지정

`mail` 채널로 알림을 전송할 때, 시스템은 기본적으로 notifiable 엔티티의 `email` 속성을 참조해 수신자 메일 주소를 결정합니다. 만약 수신자 메일 주소를 커스터마이즈하고 싶다면, notifiable 엔티티에 `routeNotificationForMail` 메서드를 추가하세요:

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
        // 이메일 주소만 반환(문자열)...
        return $this->email_address;

        // 이메일 주소와 이름을 함께 반환(배열)...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 지정

기본적으로 이메일 제목은 알림 클래스명을 "Title Case"로 변환한 값입니다. 예를 들어, 알림 클래스가 `InvoicePaid`라면, 제목은 `Invoice Paid`가 됩니다. 다른 제목으로 변경하고 싶으면, 메시지 작성 시 `subject` 메서드를 사용하세요:

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

메일 알림은 기본적으로 `config/mail.php`에 정의된 기본 메일러를 사용합니다. 다른 메일러를 사용하고 싶다면, 메시지 작성 중에 `mailer` 메서드를 호출하세요:

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

메일 알림에서 사용하는 HTML 및 플레이  
텍스트 템플릿을 커스터마이즈할 수 있습니다. 다음 명령어를 실행하면, 메일 알림 템플릿이 `resources/views/vendor/notifications` 디렉토리에 복사됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

이메일 알림에 첨부파일을 추가하려면, 메시지를 작성할 때 `attach` 메서드를 사용합니다. 첫 번째 인수로는 파일의 **절대경로**를 전달합니다:

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
> 알림 메일 메시지가 제공하는 `attach` 메서드는 [attachable 객체](/docs/12.x/mail#attachable-objects)도 지원합니다. 자세한 내용은 [attachable 객체 문서](/docs/12.x/mail#attachable-objects)를 참고하세요.

첨부파일을 추가할 때 두 번째 인수로 배열을 전달하면, 디스플레이 이름(as)이나 MIME 타입을 지정할 수 있습니다:

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

mailable 객체의 `attachFromStorage`는 사용할 수 없습니다. 반드시 해당 파일의 절대 경로를 지정해야 하며, 더 복잡한 첨부 방식이 필요하다면 [mailable](/docs/12.x/mail#generating-mailables)을 `toMail`에서 반환하면 됩니다:

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

여러 파일을 한 번에 첨부하려면 `attachMany` 메서드를 사용하면 됩니다:

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

`attachData` 메서드는 원시 데이터 스트링을 첨부파일로 추가할 수 있습니다. 파일 이름을 지정해줘야 합니다:

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

일부 메일 제공업체(Mailgun, Postmark 등)는 메시지 "태그" 및 "메타데이터" 기능을 지원합니다. 이를 통해 애플리케이션에서 전송되는 이메일 그룹화 및 추적이 가능해집니다. `tag` 및 `metadata` 메서드를 통해 손쉽게 추가할 수 있습니다:

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

Mailgun 드라이버의 태그와 메타데이터에 대해 더 자세히 알고 싶다면 Mailgun 공식 문서([tags](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags), [metadata](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages))와 Postmark의 [tags](https://postmarkapp.com/blog/tags-support-for-smtp), [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 문서를 참고하세요.

Amazon SES를 이용할 때는 `metadata` 메서드로 [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 부착하는 것이 좋습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이즈

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 이용하면, 전송 직전 Symfony Message 인스턴스를 커스터마이즈할 수 있습니다. 다음과 같이 클로저 내에서 직접 헤더 등을 추가할 수 있습니다:

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
### Mailable 활용

필요하다면, 알림의 `toMail` 메서드에서 [mailable 객체](/docs/12.x/mail)를 그대로 반환해도 됩니다. 이 경우, mailable 객체의 `to` 메서드를 이용해 수신자를 지정해야 합니다:

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

[온디맨드 알림](#on-demand-notifications) 전송 시, `toMail`의 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable` 객체입니다. 이 객체의 `routeNotificationFor` 메서드로 이메일 주소를 직접 가져올 수 있습니다:

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

메일 알림 템플릿을 개발할 때, 실제 메일 전송 없이도 Blade 템플릿처럼 바로 브라우저에서 렌더링 결과를 확인할 수 있습니다. 이를 위해, 알림에서 생성된 MailMessage를 라우트 클로저나 컨트롤러에서 그대로 반환하면, 렌더링된 내용을 브라우저에서 미리보기 할 수 있습니다:

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

마크다운 메일 알림 기능을 사용하면, 사전 제작된 알림 템플릿의 이점을 활용하면서, 더 길고 자유로운 메시지를 작성할 수 있습니다. 메시지를 마크다운으로 작성하므로, Laravel은 자동으로 반응형 HTML 템플릿과 플레이  
텍스트 버전을 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성

마크다운 템플릿이 연결된 알림을 생성하려면 `make:notification` 명령어에 `--markdown` 옵션을 사용합니다:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 메일 알림과 마찬가지로, 마크다운 기반 알림 클래스도 `toMail` 메서드를 반드시 정의해야 합니다. 단, `line`이나 `action` 메서드 대신 `markdown` 메서드로 사용할 마크다운 템플릿 이름을 지정합니다. 템플릿에 전달할 데이터는 두 번째 인수로 배열로 넘길 수 있습니다:

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

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법을 조합해, Laravel의 미리 제작된 알림 컴포넌트를 활용하면서, 손쉽게 알림 레이아웃을 구성할 수 있습니다:

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
> 마크다운 이메일 작성 시 과도한 들여쓰기는 피하세요. 마크다운 규칙상, 들여쓰기가 적용된 텍스트는 코드 블록으로 처리됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

`button` 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`, `color`(선택사항) 두 가지 속성을 지원하며, `primary`, `green`, `red` 색상을 지정할 수 있습니다. 여러 개의 버튼 컴포넌트도 사용 가능합니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

`panel` 컴포넌트는 배경색이 약간 다른 박스 영역을 만들어, 특정 메시지 블록을 강조 표시합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

`table` 컴포넌트는 마크다운 테이블을 HTML 테이블로 렌더링합니다. 컬럼 정렬은 마크다운 문법 그대로 지원합니다:

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

모든 마크다운 알림 컴포넌트를 원하는 대로 커스터마이즈할 수 있습니다. 다음 Artisan 명령어를 실행해 컴포넌트 뷰를 로컬 프로젝트로 복사할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령은 마크다운 메일 컴포넌트들을 `resources/views/vendor/mail` 디렉토리에 복사합니다. 이 하위 폴더인 `html`, `text` 디렉토리에서 각 컴포넌트의 HTML/텍스트 버전을 원하는 대로 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트 내 CSS는 `resources/views/vendor/mail/html/themes/default.css` 파일을 수정해서 적용합니다. 이곳을 편집하면 내장된 마크다운 알림의 HTML 스타일이 자동으로 인라인 처리됩니다.

Laravel의 마크다운 컴포넌트 전용 새로운 테마를 만들고 싶을 경우, `html/themes` 디렉토리에 새로운 CSS 파일을 저장한 뒤, `config/mail.php` 파일의 `theme` 옵션을 해당 테마 이름으로 수정하세요.

특정 알림에만 테마를 지정하고 싶다면, 메시지 작성시 `theme` 메서드를 사용하세요:

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

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 타입과 알림을 설명하는 JSON 구조 데이터가 담깁니다.

이 테이블을 쿼리하여 애플리케이션 내에서 알림을 사용자에게 표시할 수 있습니다. 이를 위해서는 먼저 알림 저장용 테이블을 생성해야 합니다. 아래 Artisan 명령어로 테이블 스키마가 담긴 [마이그레이션](/docs/12.x/migrations)을 생성합니다:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> notifiable 모델이 [UUID 혹은 ULID 기본키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용하는 경우, 알림 테이블 마이그레이션의 `morphs` 부분을 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)로 변경해 주세요.

<a name="formatting-database-notifications"></a>
### 알림 포맷팅

데이터베이스에 저장될 알림은 `toDatabase` 또는 `toArray` 메서드를 정의해주어야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아, 순수 PHP 배열(plain PHP array)을 반환해야 합니다. 반환값은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 아래는 `toArray` 메서드 예시입니다:

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

알림이 데이터베이스에 저장되면, `type` 컬럼은 기본적으로 알림 클래스명이 되고, `read_at` 컬럼은 `null`이 됩니다. 이 값을 커스터마이즈하려면, `databaseType`과 `initialDatabaseReadAtValue` 메서드를 알림 클래스에 정의할 수 있습니다:

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

`toArray` 메서드는 `broadcast` 채널에서도 프론트엔드로 전송될 데이터 구성을 위해 사용됩니다. 만약 `database`와 `broadcast` 채널에서 서로 다른 데이터 구조를 적용하고 싶다면, `toArray` 대신 `toDatabase`를 별도로 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 조회

알림이 데이터베이스에 저장된 후에는, notifiable 엔티티에서 손쉽게 확인할 수 있어야 합니다. `Illuminate\Notifications\Notifiable` 트레이트(기본적으로 `App\Models\User`에 포함)는 `notifications`라는 [Eloquent 연관관계](/docs/12.x/eloquent-relationships)를 제공합니다. 이를 통해 해당 엔티티의 모든 알림을 받아올 수 있습니다. 알림은 기본적으로 최신 순으로 정렬됩니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않은" 알림만 조회하고 싶으면, `unreadNotifications` 연관관계를 사용하세요. 역시 최신순으로 정렬됩니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

"읽은" 알림만 조회하려면 `readNotifications`를 사용합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림을 조회하려면, 반드시 알림을 반환하는 컨트롤러를 만들고 해당 컨트롤러의 URL로 HTTP 요청을 보내는 구조를 설계하세요.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리

일반적으로 사용자가 알림을 확인할 때마다 "읽음" 처리를 하게 됩니다. `Notifiable` 트레이트의 `markAsRead` 메서드는 알림의 `read_at` 컬럼을 업데이트합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

각각의 알림을 직접 반복하지 않고, 알림 컬렉션에서 한 번에 호출할 수도 있습니다:

```php
$user->unreadNotifications->markAsRead();
```

또한 데이터베이스 쿼리 한 번으로 일괄 "읽음" 처리를 할 수도 있습니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 삭제하고 싶으면 다음과 같이 호출하세요:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림 (Broadcast Notifications)

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림 전, 먼저 Laravel의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 설정하고 원리를 이해해야 합니다. 이벤트 브로드캐스팅은 서버에서 발생하는 Laravel 이벤트를 자바스크립트 프론트엔드에서 실시간으로 감지할 수 있게 도와줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 시스템을 이용해 알림을 프론트엔드로 실시간 전송합니다. 알림에서 브로드캐스트를 지원하려면, 알림 클래스에 `toBroadcast` 메서드를 정의하세요. `$notifiable` 엔티티를 받아, `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast` 메서드가 없다면, `toArray`의 반환값이 사용됩니다. 반환된 데이터는 JSON으로 브로드캐스트되어 프론트엔드에 전달됩니다. 아래는 예시입니다:

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

모든 브로드캐스트 알림은 큐에 등록되어 전송됩니다. 특정 큐 연결 또는 큐 이름을 지정하고 싶으면, `BroadcastMessage`의 `onConnection` 및 `onQueue` 메서드를 활용하세요:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이즈

브로드캐스트 알림 데이터에는 반드시 `type` 필드에 알림의 클래스명이 포함됩니다. 커스터마이즈가 필요하다면 알림 클래스에 `broadcastType` 메서드를 정의하세요:

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
### 알림 수신 감지

알림은 기본적으로 `{notifiable}.{id}` 포맷의 프라이빗 채널을 통해 브로드캐스트됩니다. 예를 들어, ID가 1인 `App\Models\User` 모델에 알림을 전송하면, `App.Models.User.1` 프라이빗 채널에 브로드캐스트됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용하면, 한 줄 코드로 해당 채널의 알림을 감지할 수 있습니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

Laravel Echo는 React와 Vue 훅을 제공하여 알림 수신을 쉽게 구현할 수 있습니다. `useEchoNotification` 훅을 호출하여 채널의 알림을 감지할 수 있습니다. 이 훅은 컴포넌트가 언마운트될 때 자동으로 채널 구독을 해제합니다:

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

기본적으로 이 훅은 모든 알림 유형을 감지합니다. 특정 타입만 감지하려면, 세 번째 인수로 타입 문자열 또는 배열을 전달하면 됩니다:

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

알림 페이로드의 타입을 지정해 타입 안정성과 편집 편의성을 높일 수도 있습니다:

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

특정 notifiable 엔티티의 브로드캐스트 채널명을 커스터마이즈하려면, 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하면 됩니다:

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

Laravel에서 SMS 알림 전송은 [Vonage](https://www.vonage.com/) (이전 Nexmo) 기반으로 동작합니다. Vonage를 통한 알림 전송 전, `laravel/vonage-notification-channel` 및 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

패키지에는 별도의 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있지만, 꼭 애플리케이션에 복사하지 않아도 됩니다. `VONAGE_KEY`, `VONAGE_SECRET` 환경 변수를 통해 키를 지정할 수 있습니다.

키 설정 후, 반드시 SMS 메시지 발신 번호를 지정하는 `VONAGE_SMS_FROM` 환경 변수를 설정하세요. 이 번호는 Vonage 관리자 페이지에서 생성할 수 있습니다:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

SMS 알림을 지원하려면 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

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
#### 유니코드 메시지

SMS 내용에 유니코드 문자가 포함되어야 한다면 `VonageMessage` 인스턴스 생성 시 `unicode` 메서드를 호출하세요:

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
### "From" 번호 지정

기본 발신 번호(`VONAGE_SMS_FROM` 환경 변수) 이외의 번호로 알림을 전송하고 싶다면, `from` 메서드를 호출하면 됩니다:

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

사용자·팀·클라이언트별로 SMS 비용 추적이 필요하다면, 알림에 "client reference"를 지정할 수 있습니다. Vonage 관리자 페이지에서 해당 참조로 리포트 조회가 가능합니다. 참조는 40자 이내의 문자열이면 됩니다:

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

Vonage 알림을 맞는 번호로 전달하려면 notifiable 엔티티에 `routeNotificationForVonage` 메서드를 정의하세요:

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

Slack 알림 전송을 위해서는 Slack 알림 채널을 Composer로 설치해야 합니다:

```shell
composer require laravel/slack-notification-channel
```

추가적으로, [Slack App](https://api.slack.com/apps?new_app=1)을 만듭니다.

같은 Slack 워크스페이스에만 알림을 전송하는 경우, App에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한이 필요합니다. 이 권한은 Slack App 관리 페이지의 "OAuth & Permissions" 탭에서 추가할 수 있습니다.

그런 다음, App의 "Bot User OAuth Token"을 애플리케이션의 `services.php` 설정 파일의 `slack` 배열에 복사합니다. 이 토큰은 "OAuth & Permissions" 탭에서 확인할 수 있습니다:

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### App 배포

애플리케이션이 외부 Slack 워크스페이스(사용자 소유 워크스페이스)로 알림을 전송해야 할 경우, 반드시 App을 Slack에서 "배포(distribute)"해야 합니다. App 배포는 Slack App의 "Manage Distribution"에서 설정할 수 있습니다. 배포 후에는 [Socialite](/docs/12.x/socialite)로 [Slack Bot 토큰](/docs/12.x/socialite#slack-bot-scopes)을 얻을 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 메시지를 지원하는 알림 클래스는 `toSlack` 메서드를 정의해야 합니다. `$notifiable` 엔티티를 받아, `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. [Slack의 Block Kit API](https://api.slack.com/block-kit)로 리치 메시지를 만들 수 있습니다. 아래 예시를 [Block Kit builder](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에 입력해서 미리보기할 수 있습니다:

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
#### Block Kit Builder 템플릿 직접 사용

플루언트 빌더 대신 Slack Block Kit Builder에서 생성한 JSON을 `usingBlockKitTemplate` 메서드로 바로 전달할 수도 있습니다:

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

Slack의 Block Kit 알림 시스템은 [사용자 인터랙션 처리 기능](https://api.slack.com/interactivity/handling)을 제공합니다. Slack App의 "Interactivity"를 활성화하고, 본인의 애플리케이션에서 처리하는 "Request URL"을 설정해야 합니다.

예를 들어, 아래에서 `actionsBlock` 메서드를 활용해 버튼을 만든 뒤 버튼 클릭 시 Slack이 "Request URL"에 POST 요청을 보냅니다. 이때 누가, 어떤 버튼을 눌렀는지 정보를 받아 추가 처리를 할 수 있습니다. [Slack 요청 검증(Verify)](https://api.slack.com/authentication/verifying-requests)도 함께 하시길 권장합니다:

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
             // ID 기본값: "button_acknowledge_invoice"...
            $block->button('Acknowledge Invoice')->primary();

            // 수동으로 ID 지정...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인(Confirmation) 모달

사용자가 특정 버튼을 누르기 전 확인 팝업을 띄우고 싶다면, 버튼 정의 시 `confirm` 메서드를 사용하세요. 메시지와 함께 `ConfirmObject` 인스턴스를 전달할 수 있습니다:

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
#### Slack Blocks 미리보기

작성 중인 Block Kit 메시지를 바로 미리보고 싶다면, `SlackMessage` 인스턴스의 `dd` 메서드를 호출하세요. 해당 메서드는 Slack [Block Kit Builder](https://app.slack.com/block-kit-builder/)에서 바로 볼 수 있는 URL을 생성합니다. `dd(true)`로 호출하면 원본 페이로드를 그대로 덤프합니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 적절한 슬랙 팀/채널로 전송하려면, notifiable 모델에 `routeNotificationForSlack` 메서드를 추가하세요. 이 메서드는 세 가지 값 중 하나를 반환할 수 있습니다:

- `null` : 라우팅을 알림 객체에 위임합니다. 슬랙 메시지 빌드 중 `to` 메서드를 통해 채널을 지정할 수 있습니다.
- Slack 채널명 문자열(예: `#support-channel`)
- `SlackRoute` 인스턴스 : OAuth 토큰과 채널명을 명시적으로 지정. 이 방식을 사용하면 외부 워크스페이스로 알림을 보낼 수 있습니다.

예를 들어, `routeNotificationForSlack`에서 `#support-channel`을 반환하면, `services.php`에 지정된 Bot User OAuth 토큰이 연결된 워크스페이스의 해당 채널로 알림이 전송됩니다:

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
### 외부 Slack 워크스페이스 알림

> [!NOTE]
> 외부 Slack 워크스페이스로 알림을 보내려면, 반드시 [Slack App을 배포(distribute)](#slack-app-distribution)해야 합니다.

애플리케이션 사용자가 직접 소유한 Slack 워크스페이스로 알림을 보내려면, 사용자의 Slack OAuth 토큰을 먼저 획득해야 합니다. [Laravel Socialite](/docs/12.x/socialite)의 Slack 드라이버를 사용하면, 사용자 인증 및 [Bot 토큰 획득](/docs/12.x/socialite#slack-bot-scopes)이 간편합니다.

토큰을 데이터베이스에 저장한 뒤에는, `SlackRoute::make`를 사용해 해당 워크스페이스의 채널로 직접 라우팅할 수 있습니다. 채널명도 사용자에게 선택하게 할 수 있습니다:

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
## 알림 로컬화 (Localizing Notifications)

Laravel은 알림을 현재 HTTP 요청의 로케일과 다른 언어로 보낼 수 있으며,
큐에 들어간 경우에도 해당 로케일을 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스에서 `locale` 메서드를 사용해 원하는 언어를 설정할 수 있습니다. 알림 전송 시 해당 로케일로 일시적으로 변경된 뒤, 평가 완료 후엔 원래 로케일로 복귀합니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 notifiable 엔티티에 동시에 적용하려면 Notification 파사드의 `locale` 메서드를 사용하면 됩니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

애플리케이션이 사용자의 선호 언어를 저장하고 있다면, notifiable 모델에서 `HasLocalePreference` 인터페이스를 구현하면 Laravel이 해당 로케일로 자동 전송 처리합니다:

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

이 인터페이스를 구현하면, 별도 `locale` 메서드를 호출하지 않아도 자동으로 해당 언어로 알림과 메일이 전송됩니다:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트 (Testing)

알림 전송을 실제로 수행하지 않고, Notification 파사드의 `fake` 메서드로 테스트시 전송 자체를 막을 수 있습니다. 테스트에서는 실제 알림 발송이 아니라 "어떤 알림이 보내졌는가"만 검증하는 것으로 충분한 경우가 많습니다.

`Notification::fake()` 호출 후, 다양한 단언 메서드로 알림이 의도대로 처리되었는지 확인할 수 있습니다:

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

    // Assert a notification was sent twice...
    Notification::assertSentTimes(WeeklyReminder::class, 2);

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

        // Assert a notification was sent twice...
        Notification::assertSentTimes(WeeklyReminder::class, 2);

        // Assert that a given number of notifications were sent...
        Notification::assertCount(3);
    }
}
```

`assertSentTo`, `assertNotSentTo` 메서드에는 클로저를 전달해 "특정 조건을 만족하는 알림이 전송되었는가"를 체크할 수 있습니다. 조건을 만족하는 알림이 1개 이상 전송되면 단언은 성공합니다:

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 알림

테스트 중 온디맨드 알림([on-demand notifications](#on-demand-notifications))이 전송되었는지 확인하려면,
`assertSentOnDemand` 메서드를 사용하세요:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인수로 클로저를 전달해, 의도한 라우트로 알림이 전송되었는지 추가로 확인할 수 있습니다:

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
#### 알림 전송 이벤트

알림이 전송될 때, `Illuminate\Notifications\Events\NotificationSending` 이벤트가 시스템에서 발생합니다. 이 이벤트에는 notifiable 엔티티와 알림 인스턴스가 포함되어 있습니다. 이를 위해 [이벤트 리스너](/docs/12.x/events)를 작성할 수 있습니다:

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

리스너의 `handle` 메서드가 `false`를 반환하면, 해당 알림은 전송되지 않습니다:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

리스너 내에서는 이벤트의 `notifiable`, `notification`, `channel` 속성을 통해 수신자/알림 정보를 확인할 수 있습니다:

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
#### 알림 전송 완료 이벤트

알림이 실제 전송된 후에는, 시스템에서 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)가 발생합니다. 이 이벤트에는 notifiable 엔티티, 알림 인스턴스, 전송 채널, 응답 등이 포함되어 있습니다. 이벤트 리스너에서 다음과 같이 처리할 수 있습니다:

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

이벤트 리스너 내에서 사용 가능한 프로퍼티:

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

Laravel에는 여러 기본 알림 채널이 내장되어 있지만, 다른 방법으로 알림을 전달해야 하는 경우 직접 채널 드라이버를 만들 수 있습니다. 방법은 간단합니다. 먼저 `send` 메서드를 포함하는 클래스를 정의하고, 이 메서드에서 `$notifiable`, `$notification` 두 인수를 받도록 만듭니다.

`send` 메서드 내에서 알림 객체의 메서드를 호출하여 해당 채널에서 이해할 수 있는 메시지 객체를 만들고, 원하는 방식으로 알림을 전달하면 됩니다:

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

채널 클래스가 준비되면, 알림 클래스의 `via` 메서드에서 이 클래스명을 반환하세요. 예를 들어, `toVoice` 메서드는 여러분이 설계한 메시지 객체(`VoiceMessage`)를 반환하면 됩니다:

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