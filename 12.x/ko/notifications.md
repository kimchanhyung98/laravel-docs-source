# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐에 넣기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅하기](#formatting-mail-messages)
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가하기](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailables 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [읽은 알림 표시하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 청취하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [발신 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 인터랙티비티](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스에 알림 보내기](#notifying-external-slack-workspaces)
- [알림 다국어화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

Laravel은 [이메일 보내기](/docs/12.x/mail) 기능 외에도 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/) (구 Nexmo)), [Slack](https://slack.com) 등 다양한 전달 채널을 통한 알림 보내기를 지원합니다. 또한, 커뮤니티에서 만든 다양한 [알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 가지 채널에 알림을 전송할 수 있습니다. 알림은 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션에서 발생한 이벤트를 사용자가 알 수 있게 알려주는 간단한 정보성 메시지여야 합니다. 예를 들어, 청구 애플리케이션에서는 "송장 결제 완료" 알림을 이메일과 SMS 채널을 통해 사용자에게 전송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 보통 `app/Notifications` 폴더에 저장되는 단일 클래스입니다. 만약 애플리케이션에 이 폴더가 없더라도 걱정하지 마세요. `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령은 `app/Notifications` 폴더에 새 알림 클래스를 생성합니다. 각 알림 클래스는 `via` 메서드와 `toMail`, `toDatabase` 등 각 채널별 메시지 생성 메서드를 포함하며, 해당 채널에 맞는 메시지로 알림을 변환합니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드 또는 `Notification` [파사드](/docs/12.x/facades)를 사용해 보낼 수 있습니다. 기본적으로 `App\Models\User` 모델에 `Notifiable` 트레이트가 포함되어 있습니다:

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
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 한정하지 않아도 됩니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는 `Notification` [파사드](/docs/12.x/facades)를 사용해 알림을 전송할 수 있습니다. 이 방법은 여러 개체(예: 여러 사용자)에게 동시에 알림을 보낼 때 유용합니다. 파사드의 `send` 메서드에 알림 대상과 알림 인스턴스를 넘기면 됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면 `ShouldQueue` 인터페이스를 구현했더라도 즉시 알림을 보낼 수 있습니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

각 알림 클래스에는 알림이 어떤 채널로 전달될지 결정하는 `via` 메서드가 있습니다. `mail`, `database`, `broadcast`, `vonage`, `slack` 채널 등이 있습니다.

> [!NOTE]
> Telegram, Pusher 등 다른 채널을 사용하고 싶으면 커뮤니티에서 관리하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 알림 대상 객체인 `$notifiable` 인자를 받으며, 이를 이용해 전달할 채널을 동적으로 설정할 수 있습니다:

```php
/**
 * 알림이 전달될 채널을 반환합니다.
 *
 * @return array<int, string>
 */
public function via(object $notifiable): array
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐에 넣기

> [!WARNING]
> 알림을 큐에 넣기 전에 큐 설정을 구성하고 [워커 실행](/docs/12.x/queues#running-the-queue-worker)을 반드시 시작하세요.

알림 전송에는 시간이 걸릴 수 있고, 특히 외부 API 호출이 필요한 채널은 응답 시간이 느릴 수 있습니다. 성능 개선을 위해 알림 클래스에 `ShouldQueue` 인터페이스 구현과 `Queueable` 트레이트를 추가하면 알림이 자동으로 큐에 등록됩니다.

`make:notification` 명령어로 생성한 모든 알림 클래스는 이미 인터페이스와 트레이트가 임포트되어 있으므로 바로 다음과 같이 적용할 수 있습니다:

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

이제 알림은 기존처럼 `notify` 메서드로 보내면 되며, Laravel이 자동으로 큐에 넣어 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림이 여러 수신자와 여러 채널 조합으로 보내지면, 각 수신자-채널마다 작업이 개별적으로 큐에 쌓입니다.

<a name="delaying-notifications"></a>
#### 알림 지연시키기

알림 전달을 지연하고 싶으면 알림 인스턴스 생성 시점에 `delay` 메서드를 메서드 체이닝할 수 있습니다:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 다르게 지연시간을 지정하려면 `delay` 메서드에 채널별 시간 배열을 넘기면 됩니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스에 `withDelay` 메서드를 정의해 채널별 지연 시간을 반환할 수도 있습니다:

```php
/**
 * 알림의 전달 지연을 결정합니다.
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

기본적으로 알림은 애플리케이션의 기본 큐 연결을 사용해 큐에 넣어집니다. 특정 알림에 대해 다른 큐 연결을 사용하고 싶으면 알림 생성자에서 `onConnection` 메서드를 호출하세요:

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
     * 새 알림 인스턴스 생성자
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

또는 알림 클래스에 `viaConnections` 메서드를 구현해 채널별 큐 연결 이름을 배열로 지정할 수도 있습니다:

```php
/**
 * 각 알림 채널별로 사용할 큐 연결을 지정합니다.
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

각 채널별로 사용할 큐 이름을 지정하려면 `viaQueues` 메서드를 알림 클래스에 정의하세요. 배열 형태로 채널 이름과 큐 이름을 반환해야 합니다:

```php
/**
 * 각 알림 채널별 큐 이름을 반환합니다.
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
#### 큐 미들웨어 정의하기

큐 작업과 마찬가지로, 큐에 넣은 알림에 미들웨어를 정의할 수도 있습니다. 알림 클래스에 `middleware` 메서드를 정의하고 `$notifiable`, `$channel` 인자를 받아 조건에 맞는 미들웨어 배열을 반환하세요:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 알림 큐 작업에 통과시킬 미들웨어를 반환합니다.
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

데이터베이스 트랜잭션 내부에서 큐 알림을 발생시키면, 트랜잭션이 커밋되기 전에 큐 작업이 먼저 실행될 수 있습니다. 따라서 트랜잭션 내에서 발생한 모델 변경사항 또는 새로 생성한 모델이 큐 작업 내에서 반영되지 않아 오류가 발생하는 상황이 생길 수 있습니다.

만약 큐 연결 설정 `after_commit` 옵션이 `false`인 경우에도 알림을 트랜잭션 커밋 후에 전달하도록 지정하려면, 알림을 보낼 때 `afterCommit` 메서드를 호출하세요:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스 생성자에서 직접 호출할 수 있습니다:

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
     * 새 알림 인스턴스 생성자
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 큐 작업과 데이터베이스 트랜잭션 관련 문제를 더 자세히 알고 싶으면 [큐 작업과 DB 트랜잭션 문서](/docs/12.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림을 전송할지 결정하기

큐 작업으로 대기 중인 알림이 실제로 전송될지 최종적으로 판단하고 싶으면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드는 `$notifiable`, `$channel`을 인자로 받고, `false`를 반환하면 알림 전송이 취소됩니다:

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

애플리케이션의 사용자로 저장되어 있지 않은 사람에게 임시로 알림을 보내야 할 때가 있습니다. 이런 경우, `Notification` 파사드의 `route` 메서드를 사용해서 채널별 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 채널의 수신자 이름까지 제공하려면 이메일 주소와 이름을 키-값 배열로 전달하세요:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널의 라우팅 정보를 한 번에 설정하려면 `routes` 메서드에 배열을 넘기면 됩니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅하기

이메일로 보낼 수 있는 알림이라면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 객체를 받고 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 간단한 트랜잭션용 이메일 메시지를 빠르게 만들기 위한 여러 메서드를 제공합니다. 메일 메시지는 여러 텍스트 줄과 "콜 투 액션" 버튼을 포함할 수 있습니다. 예를 들어 `toMail` 메서드는 다음과 같습니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
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
> 예시에서는 `$this->invoice->id`를 사용하지만, 알림의 생성자에 필요한 데이터를 자유롭게 전달할 수 있습니다.

위 코드는 인삿말, 정보 텍스트, 버튼, 다시 텍스트 한 줄을 등록합니다. `MailMessage`가 제공하는 메서드로 짧은 트랜잭션 메일을 쉽게 포맷할 수 있습니다. `mail` 채널은 이를 기반으로 아름답고 반응형인 HTML 이메일과 일반 텍스트 버전을 자동으로 생성합니다. 다음은 `mail` 채널로 생성된 이메일 예시입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림 시 `config/app.php`의 `name` 설정값이 메일 헤더와 푸터에 사용되니 꼭 설정하세요.

<a name="error-messages"></a>
#### 에러 메시지

실패한 송장 결제 등 에러를 알리는 알림이라면, `error` 메서드를 호출해 메시지를 에러용으로 표시할 수 있습니다. 그러면 버튼 스타일이 검정색 대신 빨간색으로 변경됩니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

알림 클래스에 텍스트 줄을 정의하는 대신, `view` 메서드를 사용해 직접 커스텀 메일 뷰를 지정할 수 있습니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

평문용 별도 뷰를 지정하려면 `view` 메서드에 배열로 뷰 이름을 전달하세요:

```php
/**
 * 메일 알림 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

평문만 있으면 `text` 메서드를 사용할 수도 있습니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

기본적으로 발신자 주소는 `config/mail.php` 설정 파일에서 정의됩니다. 특정 알림에 대해 발신자를 변경하려면 `from` 메서드를 호출하세요:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

메일 채널이 알림 수신자를 결정할 때 기본적으로 수신자 객체에서 `email` 속성을 찾습니다. 이메일 주소를 커스터마이징하려면, 수신자 모델에 `routeNotificationForMail` 메서드를 정의하세요:

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
     * 메일 채널 라우팅 정보를 반환합니다.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // 이메일 주소만 반환
        return $this->email_address;

        // 이메일 주소와 이름을 배열로 반환
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

이메일 제목 기본값은 알림 클래스명을 공백으로 구분한 "타이틀 케이스"입니다. 예: `InvoicePaid` 클래스는 `Invoice Paid`가 기본 제목입니다. 이 값을 변경하려면 `subject` 메서드를 사용합니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

기본적으로 이메일 알림은 `config/mail.php`에 설정된 기본 메일러로 발송됩니다. 실행 시점에 다른 메일러를 이용하려면 `mailer` 메서드를 호출하세요:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

메일 알림에 사용되는 HTML 및 평문 템플릿을 커스터마이징하려면 알림 패키지 리소스를 퍼블리시하세요. 다음 명령어 실행 후 템플릿은 `resources/views/vendor/notifications` 폴더에 생성됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 메시지 빌더에서 `attach` 메서드를 사용하세요. 첫 번째 인자로는 파일 절대 경로를 전달합니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> `attach` 메서드는 [attachable 객체](/docs/12.x/mail#attachable-objects)도 지원합니다. 자세한 내용은 관련 문서를 참고하세요.

첨부파일 이름과 MIME 타입을 지정하려면 `attach`의 두 번째 인자로 배열을 전달하세요:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

`attachFromStorage`를 사용해 스토리지 디스크에 저장된 파일을 직접 첨부하는 기능은 지원하지 않습니다. 대신 절대 경로로 `attach`를 쓰거나, `toMail` 메서드에서 [메일러 객체](/docs/12.x/mail#generating-mailables)를 반환해 사용하는 방식을 권장합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 메일 알림 표현을 반환합니다.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

여러 파일을 첨부하려면 `attachMany` 메서드를 사용하세요:

```php
/**
 * 메일 알림 표현을 반환합니다.
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
#### 바이트 배열 첨부파일

`attachData` 메서드로는 원시 데이터(바이트 배열)를 파일로 첨부할 수 있으며, 파일 명도 지정해야 합니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
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
### 태그 및 메타데이터 추가하기

Mailgun, Postmark 등 서드파티 이메일 제공업체는 메일 태그와 메타데이터 기능을 지원합니다. 이를 활용해 이메일 그룹핑 및 추적이 가능합니다. `tag`와 `metadata` 메서드로 태그와 메타데이터를 추가할 수 있습니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

Mailgun, Postmark 및 Amazon SES를 사용하는 경우에는 해당 서비스 문서를 참고하여 태그와 메타데이터를 적절히 활용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage`의 `withSymfonyMessage` 메서드를 사용하면 메일 전송 직전에 Symfony Message 객체를 다룰 수 있어 상세한 메시지 커스터마이징이 가능합니다:

```php
use Symfony\Component\Mime\Email;

/**
 * 메일 알림 표현을 반환합니다.
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
### Mailables 사용하기

필요하다면 알림의 `toMail` 메서드에서 완전한 [메일러 객체](/docs/12.x/mail)를 반환할 수도 있습니다. 이 경우 수신자 지정은 메일러 객체의 `to` 메서드를 통해 해야 합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * 메일 알림 표현을 반환합니다.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailables와 온디맨드 알림

온디맨드 알림을 보내는 경우, `toMail` 메서드에 전달되는 `$notifiable`은 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스입니다. 이 객체의 `routeNotificationFor` 메서드로 이메일 주소를 얻을 수 있습니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * 메일 알림 표현을 반환합니다.
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

메일 알림 템플릿을 만들면서 바로 브라우저에서 렌더링 결과를 보고 싶을 때가 있습니다. 이럴 때는 라우트 또는 컨트롤러에서 알림의 `toMail` 메서드를 호출해 반환하면, 메시지가 브라우저에 HTML로 렌더링되어 보여집니다:

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

Markdown 메일 알림을 사용하면 Laravel이 미리 만든 메일 알림 템플릿을 활용하면서, 더 길고 맞춤형 메시지를 쉽게 작성할 수 있습니다. Markdown 기반이므로 HTML 메일과 평문 메일을 자동 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

Markdown 템플릿을 사용할 알림을 만들려면 `make:notification` Artisan 명령어에 `--markdown` 옵션을 사용합니다:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

기본 메일 알림과 동일하게 알림 클래스에 `toMail` 메서드를 정의하되, `line`, `action` 메서드 대신 `markdown` 메서드로 템플릿명과 데이터를 지정합니다:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법을 같이 사용해 메시지 구조를 쉽고 편리하게 생성할 수 있습니다:

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
> Markdown 표준에 따라 불필요한 들여쓰기는 피해야 하며, 과도한 들여쓰기는 코드 블록으로 인식됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

`<x-mail::button>` 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 인수를 제공합니다. 허용 색상은 `primary`, `green`, `red`입니다. 원하는 만큼 버튼을 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

`<x-mail::panel>` 컴포넌트는 알림의 특정 텍스트 블록에 다른 배경 색상을 적용하여 강조할 때 사용합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

Markdown 테이블을 HTML 테이블로 변환하려면 `<x-mail::table>` 컴포넌트를 사용합니다. 기본 Markdown 표 문법에 따라 열 정렬도 지원합니다:

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

Markdown 알림 컴포넌트를 애플리케이션으로 내보내 자신만의 스타일로 변경하려면 `vendor:publish` Artisan 명령어를 실행하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이후 `resources/views/vendor/mail` 폴더에 HTML, 텍스트 형태의 마크다운 컴포넌트가 생성됩니다. 자유롭게 수정해서 사용하세요.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

퍼블리시 후 `resources/views/vendor/mail/html/themes` 폴더에 `default.css`가 있습니다. 이 파일을 수정하면 스타일이 알림에 자동 적용됩니다.

새 테마 CSS 파일을 `html/themes` 폴더에 추가하고, `config/mail.php`의 `theme` 옵션을 새 파일명으로 변경해 새로운 테마를 적용할 수 있습니다.

특정 알림에서 테마를 바꾸려면 메일 메시지 빌더의 `theme` 메서드를 사용하세요:

```php
/**
 * 메일 알림 표현을 반환합니다.
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

`database` 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 테이블에는 알림 타입과 JSON 형태의 알림 데이터가 들어갑니다.

먼저 `make:notifications-table` 명령어로 적절한 마이그레이션을 만들고, 마이그레이션을 실행해 테이블을 생성해야 합니다:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 만약 수신자 모델에서 [UUID 또는 ULID 기본 키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용한다면, 마이그레이션 내의 `morphs` 메서드를 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)로 변경하세요.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

데이터베이스에 알림을 저장하려면 `toDatabase` 또는 `toArray` 메서드를 알림 클래스에 정의해야 합니다. `$notifiable` 객체를 받고 평범한 PHP 배열을 반환해야 하며, 이 배열이 JSON 형태로 `notifications` 테이블의 `data` 칼럼에 저장됩니다. 예를 들면:

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

알림이 데이터베이스에 저장되면 기본적으로 `type` 칼럼은 알림 클래스명, `read_at` 칼럼은 `null`로 설정됩니다. 이 동작은 알림 클래스에서 `databaseType`과 `initialDatabaseReadAtValue` 메서드를 구현해 변경할 수 있습니다:

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
 * "read_at" 칼럼의 초기 값을 반환합니다.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs `toArray`

`toArray` 메서드는 `broadcast` 채널에도 사용되어 브로드캐스트할 데이터를 결정합니다. 알림 데이터를 데이터베이스 저장용과 브로드캐스트 전송용으로 다르게 구성하고 싶으면 `toDatabase` 메서드를 별도로 구현하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

데이터베이스에 저장된 알림을 조회하려면 `Notifiable` 트레이트가 기본 제공하는 `notifications` [Eloquent 연관관계](/docs/12.x/eloquent-relationships)를 사용할 수 있습니다. 기본 정렬은 최신 알림이 앞에 오도록 `created_at` DESC 방식입니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은 알림만 조회하려면 `unreadNotifications` 연관관계를 사용하세요:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

읽은 알림은 `readNotifications` 연관관계로 조회할 수 있습니다:

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript 클라이언트가 알림에 접근하려면, 애플리케이션에 적절한 알림 컨트롤러를 정의하여 현재 사용자 등 대상자의 알림 정보를 반환하도록 구현하세요. 클라이언트에서 HTTP 요청을 통해 알림을 불러올 수 있습니다.

<a name="marking-notifications-as-read"></a>
### 읽은 알림 표시하기

보통 유저가 알림을 읽으면 읽음 표시를 해야 합니다. `Notifiable` 트레이트의 `markAsRead` 메서드가 데이터베이스의 `read_at` 칼럼을 업데이트합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

컬렉션 단위로 `markAsRead`를 호출할 수도 있습니다:

```php
$user->unreadNotifications->markAsRead();
```

알림을 데이터베이스에서 직접 읽음 표시만 하려면 다음 방법처럼 대량 업데이트도 가능합니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 삭제하려면 다음과 같이 합니다:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하려면 Laravel의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 설정하고 사용법에 익숙해야 합니다. 서버 쪽 이벤트를 JavaScript 프론트엔드에서 실시간 감지할 수 있게 해줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel 이벤트 브로드캐스팅을 사용해 알림을 실시간으로 프런트엔드로 전달합니다. 브로드캐스트를 지원하는 알림 클래스는 `toBroadcast` 메서드를 정의하세요. `$notifiable` 객체를 받고 `BroadcastMessage` 인스턴스를 반환해야 합니다. `toBroadcast`가 없으면 `toArray` 메서드의 반환값을 사용합니다.

예시:

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트 가능한 알림 표현을 반환합니다.
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

브로드캐스트 알림은 큐에 들어가 큐 작업으로 처리됩니다. 큐 연결과 큐 이름을 지정하려면 `BroadcastMessage`의 `onConnection`, `onQueue` 메서드를 호출하세요:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

기본으로 브로드캐스트 데이터에 `type` 필드에 알림 클래스명이 자동으로 추가됩니다. 다른 이름을 쓰고 싶으면 `broadcastType` 메서드를 구현하세요:

```php
/**
 * 브로드캐스트할 알림 타입을 반환합니다.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 청취하기

알림은 `{notifiable}.{id}` 형식의 private 채널로 브로드캐스트됩니다. 예를 들어 `App\Models\User` 모델 ID가 `1`인 경우 `App.Models.User.1` 채널입니다.

Laravel Echo를 사용할 경우, 다음과 같이 청취할 수 있습니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

Laravel Echo는 React와 Vue용 알림 청취 훅을 제공합니다. 사용 예시는 다음과 같습니다:

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

특정 알림 타입만 청취하려면 세 번째 인자로 타입 문자열 또는 배열을 전달할 수 있습니다:

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

타입스크립트 타입도 지정해 코드 작성 시 안정성과 편리함을 높일 수 있습니다:

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
#### 브로드캐스트 채널 커스터마이징

알림이 브로드캐스트되는 채널 이름을 변경하려면 수신자 모델에 `receivesBroadcastNotificationsOn` 메서드를 정의하세요:

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
     * 유저가 알림을 받는 브로드캐스트 채널을 반환합니다.
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

Laravel의 SMS 알림은 [Vonage](https://www.vonage.com/) (구 Nexmo)를 사용합니다. SMS 알림을 사용하려면 `laravel/vonage-notification-channel`과 `guzzlehttp/guzzle` 패키지를 설치하세요:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지는 설정 파일이 포함되어 있지만, 필수는 아닙니다. 환경 변수 `VONAGE_KEY` 및 `VONAGE_SECRET`에 Vonage 공개 및 비밀 키를 지정하세요.

또한 환경 변수 `VONAGE_SMS_FROM` 에 기본 발신 번호를 지정해야 합니다. 번호는 Vonage 콘솔에서 생성합니다:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

SMS 전송을 지원하는 알림은 `toVonage` 메서드를 정의해야 하며, `$notifiable`을 받고 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 메시지

유니코드 문자가 포함된 SMS는 `unicode` 메서드를 호출해 처리해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현을 반환합니다.
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

기본 발신 번호 외 별도의 번호를 사용하려면 `from` 메서드를 호출하세요:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현을 반환합니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가하기

사용자, 팀, 클라이언트별 비용 추적을 위해 Vonage에 클라이언트 참조를 추가할 수 있습니다. 최대 길이는 40자입니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현을 반환합니다.
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

Vonage SMS 채널이 올바른 번호로 알림을 보낼 수 있게 수신자 모델에 `routeNotificationForVonage` 메서드를 정의하세요:

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
     * Vonage 채널용 알림 라우팅 정보를 반환합니다.
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

Slack 알림 전송을 위해서는 Composer로 Slack 알림 채널을 설치해야 합니다:

```shell
composer require laravel/slack-notification-channel
```

또한 Slack 워크스페이스용 [Slack App](https://api.slack.com/apps?new_app=1)을 생성하세요.

같은 워크스페이스로만 알림을 보낸다면 App에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한(스코프)을 부여해야 합니다. 각 권한은 Slack App 관리 페이지의 "OAuth & Permissions"에서 추가할 수 있습니다.

이후 App의 "Bot User OAuth Token"을 복사해 애플리케이션의 `config/services.php` 내 `slack` 배열 설정에 환경 변수로 넣으세요:

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

앱 배포는 애플리케이션 사용자의 외부 Slack 워크스페이스에 알림을 보내려면 필수입니다. Slack App 관리 페이지의 "Manage Distribution" 탭에서 배포를 관리할 수 있습니다. 앱 배포 후, [Socialite](/docs/12.x/socialite)를 사용해 사용자별 Slack Bot 토큰을 획득해야 합니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 메시지를 지원하는 알림은 `toSlack` 메서드를 정의하고, `$notifiable` 인자를 받으며 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다.

[Slack Block Kit API](https://api.slack.com/block-kit)를 통해 풍부한 메시지를 만들 수 있습니다. Slack Block Kit Builder(https://app.slack.com/block-kit-builder)에서 아래 JSON도 미리보기 가능합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현을 반환합니다.
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

유창한 메시지 빌더 대신 Slack Block Kit Builder에서 만든 JSON을 그대로 `usingBlockKitTemplate` 메서드에 넘겨 사용할 수도 있습니다:

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Slack 알림 표현을 반환합니다.
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
### Slack 인터랙티비티

Slack Block Kit 알림으로 사용자의 상호작용을 처리하려면 Slack 앱에서 "Interactivity"를 활성화하고, "Request URL"을 애플리케이션의 특정 URL로 설정해야 합니다. 이 설정은 Slack 앱 관리 페이지의 "Interactivity & Shortcuts" 탭에서 합니다.

다음 예시는 `actionsBlock` 메서드를 사용해 Slack이 유저 클릭 데이터를 POST 요청으로 보내는 구성입니다. 애플리케이션은 이 페이로드를 바탕으로 동작을 결정하며, Slack 요청 검증도 고려해야 합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현을 반환합니다.
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

            // 수동으로 ID 지정
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달

버튼 클릭 전에 사용자가 확인하도록 하려면 버튼 정의 시 `confirm` 메서드를 호출하세요. 첫 인자로 메시지, 두 번째 인자로 `ConfirmObject` 인스턴스를 받는 클로저를 전달합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현을 반환합니다.
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
#### Slack 블록 검사하기

빌드한 Slack 메시지 블록을 빠르게 검토하려면 `dd` 메서드를 호출하세요. Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/) URL을 생성하여 브라우저에 표시합니다. `true`를 인자로 넘기면 원시 페이로드를 덤프합니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 적절한 팀과 채널로 보내려면 수신자 모델에 `routeNotificationForSlack` 메서드를 정의하세요. 반환값으로는 다음이 가능합니다:

- `null`: 알림 내부에 지정된 기본 채널로 라우팅함
- 문자열: Slack 채널 이름 (예: `#support-channel`)
- `SlackRoute` 인스턴스: OAuth 토큰과 채널을 직접 지정할 때 사용 (외부 워크스페이스 전송용)

예제(수신자 모델 내):

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
     * Slack 채널 알림 라우팅 정보를 반환합니다.
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
> 외부 Slack 워크스페이스로 알림을 보내려면 Slack App을 [배포](#slack-app-distribution)해야 합니다.

사용자별 Slack OAuth 토큰을 획득하려면 [Laravel Socialite](/docs/12.x/socialite) Slack 드라이버를 사용해 인증 과정을 구현하세요.

토큰과 채널 정보를 DB에 저장했다면, `SlackRoute::make` 메서드로 알림 라우팅을 지정할 수 있습니다. 사용자가 직접 채널을 지정할 수 있게 만드는 애플리케이션 UI도 필요할 수 있습니다:

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
     * Slack 채널 알림 라우팅 정보를 반환합니다.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 다국어화

Laravel은 HTTP 요청의 현재 로케일과 다른 로케일로 알림을 전송할 수 있으며, 큐에 들어간 경우에도 이 로케일을 기억합니다.

알림 클래스에 `locale` 메서드로 원하는 언어를 설정할 수 있습니다. 알림이 평가되는 동안 해당 로케일로 변하며, 평가 완료 후 이전 로케일로 돌아갑니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

`Notification` 파사드로도 여러 수신자의 로케일을 지정할 수 있습니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### 유저 선호 로케일

만약 유저 모델에 선호 로케일이 저장되어 있다면, `HasLocalePreference` 계약을 구현해 Laravel이 해당 로케일을 자동으로 사용하도록 할 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 유저 선호 로케일 반환
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

인터페이스 구현 후에는 `locale` 메서드 호출 없이도 자동으로 해당 로케일이 사용됩니다:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

`Notification` 파사드의 `fake` 메서드를 사용하면 알림 전송을 차단해 테스트 중 실제 알림이 보내지지 않게 할 수 있습니다. 보통 알림 전송은 테스트 대상 코드와 별개이므로, 알림이 보내졌는지 여부만 검증하면 충분합니다.

`fake` 호출 후에는 다음처럼 알림 전송 여부 및 대상과 데이터를 확인할 수 있습니다:

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // 배송 처리...

    // 알림이 전혀 보내지지 않았는지 확인
    Notification::assertNothingSent();

    // 지정된 사용자에게 알림이 전송되었는지 확인
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // 알림이 전송되지 않았음을 확인
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // 특정 개수만큼 알림이 전송되었는지 확인
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

        // 배송 처리...

        // 알림이 전혀 보내지지 않았는지 확인
        Notification::assertNothingSent();

        // 지정된 사용자에게 알림이 전송되었는지 확인
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 알림이 전송되지 않았음을 확인
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 특정 개수만큼 알림이 전송되었는지 확인
        Notification::assertCount(3);
    }
}
```

`assertSentTo`나 `assertNotSentTo`에 클로저를 넣어 조건 검증을 할 수도 있습니다. 조건을 만족하는 알림이 하나 이상 있으면 검증이 성공합니다:

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

테스트 중에 [온디맨드 알림](#on-demand-notifications)을 보냈다면, `assertSentOnDemand` 메서드로 검증할 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인자로 클로저를 넘겨 특정 라우트 주소에 보낸 온디맨드 알림인지 검증할 수도 있습니다:

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
#### 알림 전송 중 이벤트

알림을 전송할 때 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 발생합니다. `notifiable` 객체와 알림 인스턴스를 포함하며, 애플리케이션에서 [이벤트 리스너](/docs/12.x/events)를 만들어 처리할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * 이벤트 핸들러
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

이벤트 리스너가 `handle` 메서드에서 `false`를 반환하면 해당 알림 전송이 취소됩니다:

```php
/**
 * 이벤트 핸들러
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

리스너 내에서는 `$event->channel`, `$event->notifiable`, `$event->notification` 속성을 참조할 수 있습니다.

<a name="notification-sent-event"></a>
#### 알림 전송 완료 이벤트

알림 전송이 완료되면 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발생합니다. `notifiable` 객체, 알림 인스턴스, 채널, 응답을 포함합니다:

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * 이벤트 핸들러
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

리스너 내에서는 `$event->channel`, `$event->notifiable`, `$event->notification`, `$event->response` 속성을 사용할 수 있습니다.

<a name="custom-channels"></a>
## 커스텀 채널

Laravel은 기본 여러 알림 채널을 제공하지만, 필요에 따라 자신만의 커스텀 알림 채널을 만들 수도 있습니다.

시작하려면, `send` 메서드를 가진 클래스를 정의하세요. `send` 메서드는 `$notifiable`와 `$notification` 두 인자를 받습니다.

`send` 내에서 알림에 커스텀 메서드(ex: `toVoice`)를 호출해 채널에 맞는 메시지 객체를 받고, 이를 바탕으로 전달을 구현합니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 알림 전송 처리
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable에 알림 메시지 전송 구현...
    }
}
```

알림 클래스의 `via` 메서드에 커스텀 채널 클래스를 리턴하며, 채널별 메시지 메서드도 정의하세요:

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
     * 알림 채널 반환
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * 음성 알림 메시지 반환
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```