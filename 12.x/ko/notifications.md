# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정](#specifying-delivery-channels)
    - [알림 큐 처리하기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [보내는 사람 커스터마이즈](#customizing-the-sender)
    - [수신자 커스터마이즈](#customizing-the-recipient)
    - [제목 커스터마이즈](#customizing-the-subject)
    - [메일러 지정](#customizing-the-mailer)
    - [템플릿 커스터마이즈](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그와 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
    - [메일러블 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림을 읽음으로 표시하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비사항](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - ["From" 번호 커스터마이즈](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비사항](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 상호작용](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림의 현지화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[이메일 전송](/docs/12.x/mail) 기능 지원 외에도, 라라벨은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/, 이전 명칭은 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 뿐만 아니라, [커뮤니티에서 개발된 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 다수 존재하여 수십 가지 채널을 통한 알림 전송이 가능합니다! 알림은 데이터베이스에 저장할 수도 있으며, 이렇게 저장하면 웹 인터페이스에서 알림 목록을 보여줄 수 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 이벤트를 사용자에게 간결하게 안내하는 정보성 메시지로 사용해야 합니다. 예를 들어, 청구 관련 애플리케이션을 개발 중이라면 "청구서 결제 완료" 알림을 이메일과 SMS 채널을 통해 사용자에게 발송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성

라라벨에서 각 알림은 하나의 클래스로 표현되며, 일반적으로 `app/Notifications` 디렉터리에 저장됩니다. 해당 디렉터리가 애플리케이션에 없다면 `make:notification` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:notification InvoicePaid
```

이 명령어를 실행하면 새로운 알림 클래스가 `app/Notifications` 디렉터리에 생성됩니다. 각 알림 클래스에는 `via` 메서드와, 해당 채널에 맞는 메시지를 빌드하는 여러 메서드(예: `toMail`, `toDatabase` 등)가 포함됩니다. 이들 메서드는 알림을 각 채널에 맞게 메시지로 변환합니다.

<a name="sending-notifications"></a>
## 알림 전송

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드 또는 `Notification` [파사드](/docs/12.x/facades)를 활용하여 두 가지 방식으로 전송할 수 있습니다. `Notifiable` 트레이트는 애플리케이션의 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인자로 받습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 자유롭게 사용할 수 있습니다. `User` 모델에서만 사용해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는 `Notification` [파사드](/docs/12.x/facades)를 통해서도 알림을 보낼 수 있습니다. 이 방식은 여러 개의 notifiable 엔티티(예: 사용자 컬렉션)에게 한 번에 알림을 보내야 할 때 유용합니다. 파사드를 이용해 알림을 전송할 때는 전달 대상 전부와 알림 인스턴스를 `send` 메서드에 함께 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

또한, `sendNow` 메서드를 사용하면 알림이 즉시 전송됩니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하고 있더라도 즉시 전송하며 큐를 거치지 않습니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스에는 알림이 어떤 채널을 통해 전송될지 결정하는 `via` 메서드가 존재합니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널을 통해 보낼 수 있습니다.

> [!NOTE]
> Telegram, Pusher 등 다른 전송 채널을 사용하고 싶다면 커뮤니티가 주도하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고해 보세요.

`via` 메서드는 `$notifiable` 인스턴스를 인자로 받습니다. 이 인스턴스는 알림이 전송되는 대상 클래스의 인스턴스입니다. `$notifiable`을 활용해 어떤 채널을 이용할지 동적으로 결정할 수 있습니다.

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
> 알림을 큐에 추가하려면 큐 설정을 완료하고 [큐 워커를 실행](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림 전송에는 시간이 소요될 수 있는데, 특히 외부 API 호출을 통해 알림을 전송해야 할 때 응답이 늦어질 수 있습니다. 애플리케이션의 반응 속도를 높이기 위해서 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 클래스에 추가하고 알림을 큐에 넣으면 됩니다. `make:notification` 명령어로 생성한 모든 알림 클래스에는 이미 인터페이스와 트레이트가 import되어 있으므로 바로 적용할 수 있습니다.

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

`ShouldQueue` 인터페이스가 알림 클래스에 추가되었다면 평소처럼 알림을 전송하면 라라벨이 자동으로 큐에 알림 전달 작업을 추가합니다.

```php
$user->notify(new InvoicePaid($invoice));
```

알림이 큐에 들어갈 때, 수신자와 채널 조합별로 하나씩 큐 작업이 생성됩니다. 예를 들어, 수신자가 세 명이고, 두 채널(예: 이메일, 데이터베이스)을 사용한다면 큐에는 여섯 개의 작업이 등록됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연시키기

알림 전송을 일정 시간 뒤에 지연해서 보내고 싶다면, 알림 인스턴스를 생성할 때 `delay` 메서드를 체이닝으로 사용할 수 있습니다.

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 서로 다른 지연 시간을 메시지마다 지정하려면 `delay` 메서드에 배열을 전달하면 됩니다.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스에 직접 `withDelay` 메서드를 정의하여, 채널별 지연 시간을 제어할 수 있습니다. 이 메서드는 채널명과 지연 시간을 포함한 배열을 반환합니다.

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
#### 알림 큐 연결 커스터마이즈

기본적으로 큐 처리되는 알림은 애플리케이션의 기본 큐 연결(connection)을 통해 큐에 저장됩니다. 특정 알림에 대해 다른 큐 연결을 사용하고 싶다면, 알림 클래스의 생성자에서 `onConnection` 메서드를 호출하면 됩니다.

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

또는, 알림에서 지원하는 각 채널별로 사용할 큐 연결을 다르게 지정하고 싶다면 `viaConnections` 메서드를 알림 클래스에 정의할 수 있습니다. 이 메서드는 채널 이름과 큐 연결 이름의 쌍으로 이루어진 배열을 반환해야 합니다.

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

알림에서 지원하는 각 채널별로 사용할 큐 이름을 직접 지정하고 싶다면, 알림 클래스에 `viaQueues` 메서드를 정의하세요. 이 메서드는 채널명과 큐 이름의 쌍으로 이루어진 배열을 반환합니다.

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
#### 큐 처리 알림 미들웨어

큐에서 실행되는 알림도 [큐 작업과 마찬가지로 미들웨어](/docs/12.x/queues#job-middleware)를 정의할 수 있습니다. 시작하려면 알림 클래스에 `middleware` 메서드를 정의하세요. 이 메서드는 `$notifiable`과 `$channel` 변수로 목적지에 따라 반환할 미들웨어를 동적으로 커스터마이즈할 수 있습니다.

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

알림이 데이터베이스 트랜잭션 내에서 큐로 디스패치될 때, 데이터베이스 트랜잭션이 커밋되기 전에 큐 작업이 실행될 수 있습니다. 이런 경우, 트랜잭션 중에 모델 또는 데이터베이스 레코드를 변경했더라도 해당 변경사항이 실제 데이터베이스에 반영되기 전에 큐 작업이 처리될 수 있습니다. 따라서 트랜잭션 내에서 새로 생성한 모델이나 레코드가 아직 데이터베이스에 존재하지 않을 수도 있습니다. 알림이 이러한 모델에 의존한다면, 큐 작업 실행 시 예기치 않은 에러가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정값이 `false`로 되어 있더라도, 알림을 보낼 때 `afterCommit` 메서드를 호출하면 모든 열린 데이터베이스 트랜잭션이 커밋된 후 해당 알림을 디스패치하도록 지정할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 알림 클래스의 생성자에서 `afterCommit` 메서드를 호출해도 됩니다.

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
> 이 이슈에 대한 우회 방법 등 상세 내용을 알고 싶다면 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림 발송여부 동적으로 결정하기

큐에 등록된 알림이 백그라운드 처리를 위해 디스패치되면, 일반적으로 큐 워커가 해당 알림을 받아서 지정된 수신자에게 전송합니다.

하지만 알림이 큐 워커에서 처리된 후 실제로 발송해야 할지 최종적으로 판단하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면, 해당 알림은 전송되지 않습니다.

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

때때로 애플리케이션에 "사용자"로 등록되어 있지 않은 대상에게 알림을 보내야 할 때도 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 활용하여 즉석에서 알림 라우팅 정보를 지정할 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일 알림을 온디맨드로 전송할 때 수신자의 이름까지 함께 지정하고 싶다면, 배열을 사용해 첫 번째 요소에 메일 주소를 키로, 이름을 값으로 전달할 수 있습니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 개의 알림 채널에 대해 즉석에서 라우팅 정보를 한 번에 지정할 수 있습니다.

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

알림이 이메일로도 전송될 수 있도록 지원하려면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받고, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 간편하게 트랜잭션 이메일 메시지를 빌드할 수 있도록 몇 가지 간단한 메서드를 제공합니다. 메일 메시지는 단순 텍스트 줄과 "Call To Action"(버튼) 등으로 구성할 수 있습니다. 아래는 예시 `toMail` 메서드입니다.

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
> `toMail` 메서드에서 `$this->invoice->id`를 사용하고 있다는 점에 주의하세요. 알림 메시지 생성에 필요한 데이터라면 어떤 것이든 알림의 생성자에 전달할 수 있습니다.

이 예시에서는 인사말, 텍스트 한 줄, 동작 버튼, 그리고 다시 한 줄의 텍스트를 차례로 등록하고 있습니다. `MailMessage` 객체에서 제공하는 이 메서드들 덕분에 간단하게 트랜잭션 성격의 이메일을 빠르게 작성할 수 있습니다. 메일 채널은 메시지 구성요소를 아름다운 반응형 HTML 이메일 템플릿과 텍스트 전용 버전 형식으로 변환해 줍니다. 다음은 `mail` 채널을 통해 생성된 이메일 예시입니다.

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때는 `config/app.php` 설정 파일에 있는 `name` 옵션을 반드시 설정해 주세요. 이 값은 메일 알림 메시지의 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

일부 알림은 결제 실패 등 오류 상황을 사용자에게 안내해야 할 수 있습니다. 이런 경우, 메시지를 빌드할 때 `error` 메서드를 호출하면 이 메일이 오류임을 표시할 수 있습니다. `error` 메서드를 사용할 경우, 동작 버튼이 검정색 대신 빨간색으로 표시됩니다.

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

알림 클래스 내에서 메시지의 각 "줄"을 직접 정의하는 대신, `view` 메서드를 사용해 이메일 알림에 사용할 커스텀 템플릿을 지정할 수도 있습니다.

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

메일 메시지에 대한 텍스트 뷰를 별도로 지정하고 싶으면, 배열의 두 번째 요소로 뷰 이름을 `view` 메서드에 전달할 수 있습니다.

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

또는, 메시지에 오직 텍스트 뷰만 필요한 경우 `text` 메서드를 사용할 수 있습니다.

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
### 보내는 사람 커스터마이즈

기본적으로 이메일의 발신자 주소(`from` 주소)는 `config/mail.php` 설정 파일에서 정의됩니다. 하지만 특정 알림에 대해 다른 발신 주소를 지정하고 싶으면, `from` 메서드를 사용할 수 있습니다.

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

`mail` 채널을 통해 알림을 전송할 때, 알림 시스템은 Notifiable 엔티티의 `email` 속성을 자동으로 참조합니다. 하지만, 어떤 이메일 주소로 알림을 보낼지 직접 커스터마이즈하고 싶을 때는 Notifiable 엔티티에 `routeNotificationForMail` 메서드를 정의할 수 있습니다.

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

        // 이메일 주소와 이름 반환...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이즈

기본적으로 이메일의 제목(subject)은 알림 클래스의 이름을 "Title Case"(맨 앞글자가 대문자인 형태)로 변환한 값입니다. 예를 들어, 알림 클래스 이름이 `InvoicePaid`라면 이메일의 제목은 `Invoice Paid`가 됩니다. 메시지의 제목을 다르게 지정하고 싶다면, 메시지 빌드 시 `subject` 메서드를 호출하면 원하는 제목으로 커스터마이즈할 수 있습니다.

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

기본적으로 이메일 알림은 `config/mail.php` 설정 파일에 정의된 기본 메일러를 이용해 전송됩니다. 메시지 빌드 시 `mailer` 메서드를 호출하면 런타임에 사용할 메일러를 변경할 수 있습니다.

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

메일 알림에서 사용되는 HTML 및 텍스트 템플릿은 알림 패키지의 리소스를 퍼블리시(publish)하여 커스터마이즈할 수 있습니다. 다음 명령어를 실행하면 메일 알림 템플릿이 `resources/views/vendor/notifications` 디렉터리에 복사됩니다.

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 메시지 빌드 과정에서 `attach` 메서드를 사용하세요. 첫 번째 인자로는 첨부할 파일의 절대 경로를 전달합니다.

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
> 알림 메일 메시지에서 제공하는 `attach` 메서드는 [attachable 객체](/docs/12.x/mail#attachable-objects)도 사용할 수 있습니다. 자세한 내용은 [attachable 객체 관련 문서](/docs/12.x/mail#attachable-objects)를 참고하세요.

첨부파일을 메시지에 추가할 때, 두 번째 인자로 배열을 넘기면 표시할 파일명(`as`)이나 MIME 타입(`mime`)을 지정할 수도 있습니다.

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

메일러블 객체에서처럼 `attachFromStorage`를 통해 스토리지 디스크에서 직접 파일을 첨부하는 것은 불가능합니다. 대신, `attach` 메서드에 스토리지 디스크에 있는 파일의 절대 경로를 전달해서 첨부해야 합니다. 또는, `toMail` 메서드에서 [메일러블](/docs/12.x/mail#generating-mailables)을 반환하는 방식으로 처리할 수도 있습니다.

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

여러 개의 파일을 동시에 첨부하려면 `attachMany` 메서드를 사용할 수 있습니다.

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

`attachData` 메서드는 바이트 문자열과 같이 원시 데이터를 첨부파일로 추가할 때 사용할 수 있습니다. 이 메서드를 호출할 때는 첨부파일로 사용할 파일명을 지정해주어야 합니다.

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
### 태그와 메타데이터 추가

Mailgun, Postmark와 같은 일부 서드파티 이메일 공급자에서는 메시지 "태그"와 "메타데이터"를 지원합니다. 이 기능을 통해 애플리케이션이 전송한 이메일을 그룹화하고 추적할 수 있습니다. `tag`와 `metadata` 메서드를 활용해 태그/메타데이터를 알림 이메일 메시지에 추가할 수 있습니다.

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

Mailgun 드라이버를 사용하는 경우, [태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1)와 [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) 지원에 관한 Mailgun 공식 문서를 참고할 수 있습니다. 마찬가지로, [Postmark의 태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [Postmark 메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서도 참고해 보세요.

Amazon SES를 통해 이메일을 보내는 경우, `metadata` 메서드를 사용해 해당 메시지에 [SES의 "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>

### Symfony 메시지 커스터마이징

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 사용하면 메시지를 전송하기 전에 Symfony Message 인스턴스를 전달받아 커스터마이징할 수 있는 클로저를 등록할 수 있습니다. 이 기능을 이용하면 메시지가 실제로 전달되기 전에 좀 더 세부적으로 메시지를 조정할 수 있습니다.

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
### Mailable 클래스 사용하기

필요하다면, 알림의 `toMail` 메서드에서 전체 [mailable 객체](/docs/12.x/mail)를 반환할 수도 있습니다. `MailMessage` 대신 `Mailable` 객체를 반환할 때는 mailable의 `to` 메서드를 사용해서 수신자를 직접 지정해주어야 합니다.

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
#### Mailable과 온디맨드(임시) 알림

[온디맨드 알림](#on-demand-notifications)을 전송하는 경우, `toMail` 메서드에 전달되는 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable`의 인스턴스입니다. 이 객체는 `routeNotificationFor` 메서드를 제공하며, 이를 통해 온디맨드 알림이 전송되어야 하는 이메일 주소를 가져올 수 있습니다.

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

메일 알림 템플릿을 설계할 때, 일반 Blade 템플릿처럼 렌더링된 메일 메시지를 브라우저에서 미리 확인할 수 있으면 매우 편리합니다. 라라벨에서는 라우트 클로저나 컨트롤러에서 알림이 생성한 메일 메시지를 직접 반환할 수 있습니다. `MailMessage`가 반환되면, 실제로 이메일 전송 없이 브라우저에서 바로 디자인을 미리 볼 수 있게 렌더링됩니다.

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
## Markdown 메일 알림

Markdown 메일 알림 기능을 사용하면, 미리 만들어진 알림 템플릿의 장점을 활용하면서도 좀 더 자유롭게 긴 내용이나 커스텀 메시지를 작성할 수 있습니다. 알림 내용이 Markdown 형식으로 작성되므로, 라라벨은 보기 좋고 반응형인 HTML 템플릿을 자동으로 만들어 주며, 동시에 일반 텍스트 형태도 자동으로 생성해줍니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

Markdown 템플릿이 연결된 알림을 생성하려면 `make:notification` 아티즌 명령어의 `--markdown` 옵션을 사용합니다.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 메일 알림과 마찬가지로, Markdown 템플릿을 사용하는 알림 클래스도 `toMail` 메서드를 정의해야 합니다. 다만, `line`이나 `action` 메서드 대신 `markdown` 메서드를 사용하여 사용할 Markdown 템플릿의 이름을 지정하면 됩니다. 템플릿에서 사용할 데이터를 배열로 두 번째 인자로 전달할 수 있습니다.

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

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법을 조합해서 쉽게 알림 내용을 구성할 수 있으며, 라라벨이 제공하는 다양한 알림 컴포넌트도 활용할 수 있습니다.

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
> Markdown 이메일을 작성할 때에는 들여쓰기를 과도하게 사용하지 마세요. Markdown 규칙에 따라 들여쓰기가 된 내용은 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color` 인자를 받을 수 있습니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 알림에서 버튼 컴포넌트를 원하는 만큼 여러 개 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 나머지 알림 영역과 조금 다른 배경색의 패널로 감싸 보여줍니다. 이렇게 하면 특정 텍스트에 주목시키는 효과를 줄 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 Markdown 테이블을 HTML 테이블로 변환할 수 있습니다. 컴포넌트의 콘텐츠로 Markdown 표를 넣으면 됩니다. 기본 Markdown 표 정렬 문법으로 컬럼 정렬도 지원됩니다.

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

Markdown 알림 컴포넌트 전체를 내 애플리케이션에 내보내(customize) 직접 수정할 수 있습니다. 내보내려면 `vendor:publish` 아티즌 명령어로 `laravel-mail` 에셋 태그를 퍼블리시 하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령은 Markdown 메일 컴포넌트를 `resources/views/vendor/mail` 디렉터리에 복사합니다. `mail` 디렉터리 안에는 각각 HTML과 텍스트 버전의 컴포넌트가 들어 있는 `html`, `text` 폴더가 생성됩니다. 여기서 컴포넌트 파일을 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트들을 내보낸 이후, `resources/views/vendor/mail/html/themes` 디렉터리에는 `default.css` 파일이 있습니다. 이 파일의 CSS를 수정하면, 스타일이 자동으로 Markdown 알림의 HTML에도 인라인 적용됩니다.

라라벨의 Markdown 컴포넌트를 위한 완전히 새로운 테마를 만들고 싶다면, CSS 파일을 `html/themes` 디렉터리에 추가하면 됩니다. CSS 파일을 저장한 후, `mail` 설정 파일에서 사용할 테마의 이름을 `theme` 옵션에 맞춰 변경하면 적용됩니다.

개별 알림마다 사용할 테마를 지정하고 싶을 때는, 알림의 메일 메시지를 만들 때 `theme` 메서드로 테마 이름을 지정할 수 있습니다. 이 메서드는 알림 발송 시 사용할 테마 이름을 인자로 받습니다.

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

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림의 타입, 알림을 설명하는 JSON 데이터 구조 등이 저장됩니다.

애플리케이션의 사용자 인터페이스에서 알림을 보여주려면 이 테이블을 조회하면 됩니다. 그 전에 먼저 알림을 저장할 데이터베이스 테이블을 생성해야 합니다. `make:notifications-table` 명령어를 사용하면 필요한 [마이그레이션](/docs/12.x/migrations)을 쉽게 만들 수 있습니다.

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> notifiable 모델이 [UUID 또는 ULID 기본 키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용하고 있다면, 알림 테이블 마이그레이션에서 `morphs` 대신 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)를 사용해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림의 포맷 정의

알림이 데이터베이스에 저장되도록 지원하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아서 순수 PHP 배열을 반환해야 합니다. 반환된 배열은 `notifications` 테이블의 `data` 컬럼에 JSON으로 저장됩니다. 아래는 예시 `toArray` 메서드입니다.

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

알림이 데이터베이스에 저장될 때, 기본적으로 `type` 컬럼에는 알림의 클래스 이름이 저장되며, `read_at` 컬럼은 `null`로 설정됩니다. 이런 동작을 커스터마이즈하고 싶다면 알림 클래스에 `databaseType`과 `initialDatabaseReadAtValue` 메서드를 정의하면 됩니다.

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
#### `toDatabase` vs. `toArray`

`toArray` 메서드는 `broadcast` 채널에서도 사용되어, 자바스크립트 프론트엔드로 전송할 데이터를 구성합니다. `database`와 `broadcast` 채널에 각기 다른 배열 데이터를 사용하고 싶다면 `toArray` 대신 `toDatabase` 메서드를 정의해야 합니다.

<a name="accessing-the-notifications"></a>
### 데이터베이스에서 알림 가져오기

알림이 데이터베이스에 저장되면, notifiable 엔티티에서 이를 쉽게 접근할 수 있어야 합니다. 라라벨에서 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트에는 해당 엔티티에 대한 알림을 반환하는 `notifications` [Eloquent 연관관계](/docs/12.x/eloquent-relationships)가 포함되어 있습니다. 다른 Eloquent 연관관계와 마찬가지로 이 메서드로 알림을 조회할 수 있습니다. 기본적으로 알림은 최근 생성된 순서대로 정렬되어 반환됩니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않은" 알림만 조회하려면, `unreadNotifications` 연관관계를 사용할 수 있습니다. 역시 가장 최근 알림이 먼저 나옵니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript 클라이언트에서 알림에 접근하려면, 알림을 반환하는 컨트롤러를 애플리케이션에 정의하고 (예: 현재 사용자용) 자바스크립트로 해당 URL에 HTTP 요청을 보내면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리하기

일반적으로 사용자가 알림을 확인하는 시점에 해당 알림을 "읽음" 상태로 표시하고 싶을 것입니다. `Illuminate\Notifications\Notifiable` 트레이트에는 데이터베이스 알림의 `read_at` 컬럼을 갱신해주는 `markAsRead` 메서드가 포함되어 있습니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

모든 알림을 일일이 루프 돌지 않고, 알림 컬렉션에 `markAsRead`를 바로 호출해서 일괄로 읽음 처리할 수도 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

알림 전체를 가져오지 않고도, 데이터베이스에서 바로 모든 알림을 일괄로 읽음 처리하려면 mass-update 쿼리를 사용할 수 있습니다.

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 테이블에서 아예 삭제하려면 `delete` 메서드를 사용합니다.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하려면, 먼저 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 구성하고 익숙해져야 합니다. 이벤트 브로드캐스팅을 이용하면 서버에서 발생하는 라라벨 이벤트에 자바스크립트 프론트엔드가 실시간으로 반응할 수 있습니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷 정의

`broadcast` 채널은 라라벨의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 기능을 사용해서 알림을 브로드캐스트하며, 자바스크립트 프론트엔드는 실시간으로 이 알림을 받아 처리할 수 있습니다. 브로드캐스트가 가능한 알림 클래스에서는 `toBroadcast` 메서드를 정의할 수 있습니다. 이 메서드는 `$notifiable` 엔티티를 받아 `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast` 메서드가 없다면, 알림 데이터는 `toArray` 메서드에서 가져오게 됩니다. 반환되는 데이터는 JSON으로 인코딩되어 자바스크립트 프론트엔드로 브로드캐스트됩니다. 아래는 예시 `toBroadcast` 메서드입니다.

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 알림의 브로드캐스트 표현을 반환합니다.
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

브로드캐스트 알림은 모두 큐에 들어가 전송됩니다. 브로드캐스트 작업에 사용할 큐 커넥션 또는 큐 이름을 지정하고 싶다면, `BroadcastMessage`의 `onConnection`과 `onQueue` 메서드를 사용하세요.

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

데이터뿐 아니라, 모든 브로드캐스트 알림에는 전체 클래스 이름이 담긴 `type` 필드도 포함됩니다. 알림의 `type` 값을 커스터마이징하려면, 알림 클래스에 `broadcastType` 메서드를 정의할 수 있습니다.

```php
/**
 * 브로드캐스팅되는 알림의 타입을 반환합니다.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 리스닝(수신)하기

알림은 `{notifiable}.{id}` 형식의 프라이빗 채널로 브로드캐스트됩니다. 예를 들어, ID가 1인 `App\Models\User` 인스턴스에 알림을 보낸다면, `App.Models.User.1` 프라이빗 채널로 브로드캐스트됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용할 때 채널에서 `notification` 메서드로 쉽게 알림을 수신할 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

Laravel Echo는 알림을 손쉽게 수신할 수 있도록 React와 Vue 훅을 제공합니다. 시작하려면, `useEchoNotification` 훅을 사용합니다. 이 훅은 컴포넌트가 마운트 해제될 때 채널도 자동으로 나가도록 처리해줍니다.

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

기본적으로 훅은 모든 알림을 리스닝합니다. 특정 알림 타입만 리스닝하고 싶다면, `useEchoNotification`에 타입 문자열이나 타입 배열을 세 번째 인자로 전달할 수 있습니다.

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

알림 페이로드 데이터의 타입을 직접 정의하여 더욱 안전하고 편리하게 코딩할 수도 있습니다.

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
#### 알림 채널 커스터마이징

엔티티의 브로드캐스트 알림이 전송되는 채널을 커스터마이즈하고 싶을 때는, notifiable 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하면 됩니다.

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
     * 이 사용자가 알림 브로드캐스트를 받을 채널명을 반환합니다.
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

라라벨에서 SMS 알림 전송은 [Vonage](https://www.vonage.com/) (이전 이름: Nexmo)를 이용합니다. Vonage를 통한 알림 발송 전, `laravel/vonage-notification-channel` 패키지와 `guzzlehttp/guzzle` 패키지를 먼저 설치해야 합니다.

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지에는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있습니다. 그러나 이 설정 파일을 애플리케이션에 별도로 내보낼 필요는 없습니다. `VONAGE_KEY`와 `VONAGE_SECRET` 환경 변수만 지정하면 Vonage의 공개/비밀키를 사용할 수 있습니다.

키 등록이 끝나면, 기본적으로 SMS 발신자로 사용할 전화번호를 `VONAGE_SMS_FROM` 환경 변수에 지정해야 합니다. 해당 번호는 Vonage 콘솔에서 발급받을 수 있습니다.

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷 정의

SMS 전송이 필요한 알림에서는 `toVonage` 메서드를 알림 클래스에 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다.

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
#### 유니코드 문자 포함 메시지

SMS 메시지에 유니코드 문자(예: 한글, 이모지 등)가 포함되어 있다면, `VonageMessage` 인스턴스를 만들 때 `unicode` 메서드를 호출해야 합니다.

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
### 발신 번호 커스터마이징

`VONAGE_SMS_FROM` 환경 변수에 지정한 번호와 다른 번호로 일부 알림을 전송하고 싶다면, `VonageMessage` 인스턴스에 `from` 메서드를 호출해서 원하는 발신 번호를 별도로 지정할 수 있습니다.

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
### 클라이언트 참조값 추가하기

사용자, 팀, 또는 클라이언트별로 비용 추적이 필요하다면, 알림에 "클라이언트 참조값"을 추가할 수 있습니다. Vonage에서는 이 값을 기반으로 각 고객의 SMS 사용 내역 리포트를 생성할 수 있습니다. 클라이언트 참조값은 최대 40자까지 사용할 수 있습니다.

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

Vonage 알림을 적절한 전화번호로 라우팅하기 위해, notifiable 엔티티에 `routeNotificationForVonage` 메서드를 정의하세요.

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
     * Vonage 채널을 위한 알림 라우팅 경로를 반환합니다.
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

Slack 알림 전송을 위해서는 Composer로 Slack 알림 채널 패키지를 설치해야 합니다.

```shell
composer require laravel/slack-notification-channel
```

그리고 Slack 워크스페이스에서 [Slack App](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

동일 워크스페이스 내 알림만 필요하다면, 앱에 `chat:write`, `chat:write.public`, `chat:write.customize` 스코프가 할당되어야 합니다. 이 스코프는 Slack의 앱 관리 화면 "OAuth & Permissions" 탭에서 추가할 수 있습니다.

그 다음, 앱의 "Bot User OAuth Token"을 발급받아 애플리케이션의 `services.php` 설정 파일 내 `slack` 설정 배열에 추가합니다. 토큰은 Slack "OAuth & Permissions" 탭에서 확인할 수 있습니다.

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### Slack App 배포

애플리케이션이 사용자의 외부 Slack 워크스페이스로 알림을 보낼 필요가 있다면, Slack을 통해 "앱 배포(distribute)"가 필요합니다. 배포는 Slack의 앱 관리 화면 "Manage Distribution" 탭에서 진행할 수 있습니다. 앱을 배포한 뒤에는 [Socialite](/docs/12.x/socialite)를 이용해 [Slack Bot 토큰](/docs/12.x/socialite#slack-bot-scopes)을 사용자별로 획득할 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷 정의

Slack 메시지 전송이 필요한 알림은, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. [Slack의 Block Kit API](https://api.slack.com/block-kit)를 활용해서 풍부한 알림 메시지를 만들 수 있습니다. 아래 예시는 [Slack Block Kit builder](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리 볼 수도 있습니다.

```php
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

Block Kit 메시지를 셋업하는 데 빌더 메서드를 일일이 사용하지 않고, Slack Block Kit Builder에서 만든 JSON 페이로드 원본을 `usingBlockKitTemplate` 메서드로 바로 전달할 수도 있습니다.

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

### Slack 상호작용 기능

Slack의 Block Kit 알림 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling)를 위한 강력한 기능을 제공합니다. 이러한 기능을 활용하려면, Slack App에서 "Interactivity"를 활성화하고, 앱에서 제공하는 URL을 "Request URL"로 설정해야 합니다. 이 설정들은 Slack의 "Interactivity & Shortcuts" 앱 관리 탭에서 관리할 수 있습니다.

다음 예제에서는 `actionsBlock` 메서드를 사용하고 있습니다. 사용자가 버튼을 클릭하면 Slack이 "Request URL"로 해당 Slack 사용자, 클릭된 버튼의 ID 등 여러 정보를 포함한 `POST` 요청을 보냅니다. 애플리케이션에서는 이 페이로드를 바탕으로 적절한 동작을 결정할 수 있습니다. 또한 반드시 [요청이 Slack에서 온 것인지 검증](https://api.slack.com/authentication/verifying-requests-from-slack)해야 합니다.

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

사용자가 어떤 동작을 실행하기 전에 반드시 확인을 받도록 하고 싶다면, 버튼을 정의할 때 `confirm` 메서드를 사용할 수 있습니다. `confirm` 메서드는 메시지와, `ConfirmObject` 인스턴스를 전달받는 클로저를 인자로 받습니다.

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
#### Slack 블록 확인하기

지금까지 만들어온 Slack 블록을 빠르게 확인하고 싶으면, `SlackMessage` 인스턴스에서 `dd` 메서드를 호출할 수 있습니다. `dd` 메서드는 Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/)로 연결되는 URL을 생성해 브라우저에서 페이로드와 알림 미리보기를 볼 수 있도록 해줍니다. `dd` 메서드에 `true`를 전달하면 원본 페이로드를 덤프합니다.

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 특정 Slack 팀과 채널로 보내려면, 알림을 받을 모델에 `routeNotificationForSlack` 메서드를 정의해야 합니다. 이 메서드는 다음 세 가지 중 하나의 값을 반환할 수 있습니다.

- `null` - 알림 정의 내에서 설정된 채널로 라우팅을 위임합니다. 알림 내에서 `SlackMessage`를 빌드할 때 `to` 메서드를 사용해 채널을 지정할 수 있습니다.
- 문자열: 알림을 전송할 Slack 채널 이름(예: `#support-channel`).
- `SlackRoute` 인스턴스: OAuth 토큰과 채널명을 직접 지정하는 용도로 사용됩니다. (예: `SlackRoute::make($this->slack_channel, $this->slack_token)`) 외부 워크스페이스로 알림을 보낼 때 활용합니다.

예를 들어, `routeNotificationForSlack` 메서드에서 `#support-channel`을 반환하면, 애플리케이션의 `services.php` 설정 파일에 있는 Bot User OAuth 토큰과 연동된 워크스페이스에서 `#support-channel` 채널로 알림이 전송됩니다.

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
### 외부 Slack 워크스페이스에 알림 보내기

> [!NOTE]
> 외부 Slack 워크스페이스에 알림을 보내기 전에 Slack App을 반드시 [배포(distribute)](#slack-app-distribution)해야 합니다.

실무에서는 애플리케이션 사용자의 Slack 워크스페이스로 알림을 보내고 싶을 때가 많습니다. 이를 위해서는 먼저 사용자별로 Slack OAuth 토큰을 발급받아야 합니다. 다행히도 [Laravel Socialite](/docs/12.x/socialite)에는 Slack 드라이버가 내장되어 있어, 사용자의 Slack 계정으로 쉽게 인증하고 [봇 토큰을 얻을 수 있습니다](/docs/12.x/socialite#slack-bot-scopes).

봇 토큰을 획득해 애플리케이션의 데이터베이스에 저장했다면, `SlackRoute::make` 메서드를 사용하여 해당 사용자의 워크스페이스로 알림을 보낼 수 있습니다. 또한, 알림을 어떤 채널로 보낼지 사용자가 선택할 수 있도록 기회(설정 옵션)를 제공해야 할 수도 있습니다.

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
## 알림의 다국어(로컬라이징) 처리

라라벨은 알림을 HTTP 요청의 현재 언어(locale)와 다르게 보낼 수 있으며, 알림이 큐에 들어간 경우에도 이 언어 설정을 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스는 원하는 언어를 지정할 수 있는 `locale` 메서드를 제공합니다. 알림이 평가되는 동안 해당 언어로 전환되고, 평가가 끝나면 이전 언어로 돌아갑니다.

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 명의 알림 수신자(notifiable)에게 다국어 알림을 보낼 때는 `Notification` 파사드를 사용할 수도 있습니다.

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 언어 적용

일부 애플리케이션에서는 사용자별로 선호하는 언어(locale)를 저장하기도 합니다. 알림을 받을 모델에서 `HasLocalePreference` 컨트랙트를 구현하면, 라라벨이 알림 보낼 때 해당 사용자의 선호 언어 정보를 자동으로 사용할 수 있습니다.

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

이 인터페이스를 구현하면, 라라벨이 알림(및 메일)을 전송할 때 그 사용자에 대해 자동으로 선호 언어를 사용합니다. 따라서 이 인터페이스를 쓸 때는 별도로 `locale` 메서드를 호출할 필요가 없습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

`Notification` 파사드의 `fake` 메서드를 사용하면 실제로 알림을 전송하지 않고 테스트할 수 있습니다. 보통 실제 알림 전송은 테스트하려는 코드의 본질과 관련이 없으므로, 라라벨에게 특정 알림을 전송하도록 "지시되었는지"만 확인하면 충분합니다.

`Notification` 파사드의 `fake`를 호출한 뒤, 특정 사용자에게 알림이 지시됐는지(알림이 전송됐는지) 검사하고, 알림에 전달된 데이터까지 확인할 수 있습니다.

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

`assertSentTo`와 `assertNotSentTo` 메서드에는 클로저를 전달할 수 있으며, 해당 알림이 "조건을 만족하는지" 검사합니다. 조건을 만족하는 알림이 하나라도 전송됐다면 해당 검사는 통과합니다.

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드(즉시) 알림 테스트

테스트 코드에서 [온디맨드 알림](#on-demand-notifications)을 전송한다면, `assertSentOnDemand` 메서드로 온디맨드 알림이 전송됐는지 검사할 수 있습니다.

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` 메서드의 두 번째 인자로 클로저를 전달하면, 해당 온디맨드 알림이 올바른 "라우트" 주소(예: 이메일 등)로 전송됐는지도 확인할 수 있습니다.

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
#### 알림 전송 중 이벤트(Notification Sending Event)

알림이 전송되는 과정에서는 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 알림 시스템에 의해 발생합니다. 이 이벤트에는 실제로 알림을 받는 엔티티("notifiable")와 알림 인스턴스가 포함되어 있습니다. 애플리케이션에서 [이벤트 리스너](/docs/12.x/events)를 만들어 처리할 수 있습니다.

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

`NotificationSending` 이벤트의 리스너에서 `handle` 메서드가 `false`를 반환하면 알림이 전송되지 않습니다.

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 리스너 내부에서는 해당 이벤트의 `notifiable`, `notification`, `channel` 프로퍼티를 통해 수신자, 알림 정보 등을 확인할 수 있습니다.

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
#### 알림 전송 완료 이벤트(Notification Sent Event)

알림이 성공적으로 전송되면, `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)가 알림 시스템에 의해 발생합니다. 이 이벤트에도 수신자("notifiable")와 알림 인스턴스 정보가 포함되어 있습니다. 마찬가지로 [이벤트 리스너](/docs/12.x/events)를 만들어 원하는 작업을 처리할 수 있습니다.

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

이벤트 리스너 내부에서는 해당 이벤트의 `notifiable`, `notification`, `channel`, `response` 프로퍼티를 통해 수신자와 알림 정보, 실제 전송 결과(response)를 확인할 수 있습니다.

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
## 커스텀 채널

라라벨은 여러 기본 알림 채널을 제공합니다. 하지만 필요에 따라 직접 드라이버(채널)를 만들어 다양한 방식으로 알림을 보낼 수도 있습니다. 라라벨에서 커스텀 채널을 만드는 방법은 매우 간단합니다.

먼저, `send` 메서드를 포함하는 클래스를 정의해야 합니다. 이 메서드는 두 개의 인수를 받습니다: `$notifiable`(알림 받을 대상)과 `$notification`(알림 내용)입니다.

`send` 메서드 내에서 알림(`$notification`)의 메서드를 호출하여 해당 채널에 맞게 변환된 메시지 객체를 얻고, 원하는 방식으로 `$notifiable`에게 알림을 전송하면 됩니다.

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

커스텀 알림 채널 클래스를 정의했다면, 알림 클래스에서 `via` 메서드에서 해당 클래스명을 반환하여 사용할 수 있습니다. 이 예시에서 알림의 `toVoice` 메서드는 음성 메시지를 나타내는 여러분만의 객체를 반환할 수 있습니다. 예를 들어, `VoiceMessage` 클래스를 따로 만들어 음성 메시지를 표현할 수도 있습니다.

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