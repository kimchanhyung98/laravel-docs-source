# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 전송하기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 퍼사드 사용하기](#using-the-notification-facade)
    - [전달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 사용자 지정하기](#customizing-the-sender)
    - [수신자 사용자 지정하기](#customizing-the-recipient)
    - [제목 사용자 지정하기](#customizing-the-subject)
    - [메일러 사용자 지정하기](#customizing-the-mailer)
    - [템플릿 사용자 지정하기](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그와 메타데이터 추가하기](#adding-tags-metadata)
    - [Symfony 메시지 사용자 지정하기](#customizing-the-symfony-message)
    - [Mailables 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 사용자 지정하기](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [전제 조건](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [읽음 표시하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [전제 조건](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 듣기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [전제 조건](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 내용](#unicode-content)
    - [발신 번호 사용자 지정하기](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [전제 조건](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 인터랙티비티](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스에 알림 보내기](#notifying-external-slack-workspaces)
- [알림 로컬라이징](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

Laravel은 [이메일 전송](https://laravel.com/docs/11.x/mail) 지원뿐만 아니라 이메일, SMS (이전 Nexmo였던 [Vonage](https://www.vonage.com/communications-apis/)) 및 [Slack](https://slack.com)을 포함하여 다양한 전달 채널을 통한 알림 전송을 지원합니다. 또한 수십 가지 다양한 채널에 대한 알림 전송을 가능하게 하는 [커뮤니티 제작 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 존재합니다! 알림은 데이터베이스에 저장해서 웹 인터페이스에 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 상황에 대해 사용자에게 알려주기 위한 간단하고 정보성 있는 메시지여야 합니다. 예를 들어 청구 애플리케이션이라면 "Invoice Paid"(송장 결제 완료) 알림을 이메일과 SMS 채널을 통해 사용자에게 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 보통 `app/Notifications` 디렉토리에 저장되는 단일 클래스 하나로 표현됩니다. 애플리케이션에 이 디렉터리가 없더라도 걱정하지 마세요 - `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

위 명령을 실행하면 `app/Notifications` 디렉토리에 새 알림 클래스가 생성됩니다. 각 알림 클래스는 `via` 메서드와 다양한 메시지 작성 메서드(`toMail`, `toDatabase` 등)를 포함하는데, 이 메서드들은 알림을 특정 채널에 맞춘 메시지로 변환합니다.

<a name="sending-notifications"></a>
## 알림 전송하기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 크게 두 가지 방식으로 전송할 수 있습니다: `Notifiable` 트레이트의 `notify` 메서드를 사용하거나 `Notification` [퍼사드](/docs/11.x/facades)를 사용하는 방법입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인자로 기대합니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 모든 모델에서 사용할 수 있습니다. 반드시 `User` 모델에만 포함시켜야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 퍼사드 사용하기

또는 `Notification` 퍼사드를 통해 알림을 보낼 수 있습니다. 이 방법은 다수의 수신자(예: 여러 사용자)에게 알림을 보낼 때 유용합니다. 퍼사드를 이용해 알림을 전송하려면, 모든 수신 대상과 알림 인스턴스를 `send` 메서드에 전달하세요:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

즉시 알림을 보내려면 `sendNow` 메서드를 사용하면 됩니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하더라도 즉시 전송합니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

모든 알림 클래스는 `via` 메서드를 갖고 있으며, 이 메서드에서 알림이 전달될 채널들을 지정합니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널에서 전송할 수 있습니다.

> [!NOTE]
> Telegram이나 Pusher와 같은 다른 채널을 사용하고 싶다면, 커뮤니티에서 제공하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 객체를 인자로 받는데, 이는 알림이 전송되는 모델 인스턴스입니다. 이 객체를 활용해 적절한 전달 채널을 결정할 수 있습니다:

```php
/**
 * 알림의 전달 채널 반환
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
> 알림 큐잉 전에 큐를 설정하고 [큐 워커를 실행](/docs/11.x/queues#running-the-queue-worker)해야 합니다.

알림 전송은 특히 외부 API 호출이 필요할 경우 시간이 걸릴 수 있습니다. 애플리케이션의 응답 시간을 개선하기 위해 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 추가해 알림을 큐에 넣을 수 있습니다. `make:notification` 명령어로 생성된 알림 클래스는 이미 해당 인터페이스와 트레이트를 가져오므로 바로 추가할 수 있습니다:

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

`ShouldQueue` 인터페이스를 추가한 후에는 평소처럼 알림을 전송하면 됩니다. Laravel은 클래스에 `ShouldQueue`가 설정된 것을 감지해 자동으로 큐에 알림 전송 작업을 등록합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐에 넣을 때, 각 수신자와 채널 조합마다 하나씩 큐 작업이 생성됩니다. 예를 들어, 수신자가 3명이고 채널이 2개라면 총 6개의 작업이 큐에 쌓입니다.

<a name="delaying-notifications"></a>
#### 알림 지연하기

알림 전달을 지연하고 싶다면 알림 인스턴스 생성 시 `delay` 메서드를 체이닝하여 사용하세요:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 개별 지연 시간을 지정하려면 `delay` 메서드에 배열을 전달할 수 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또 다른 방법으로, 알림 클래스 내에 `withDelay` 메서드를 정의할 수 있습니다. 이 메서드는 채널 이름과 지연 시간 값을 담은 배열을 반환해야 합니다:

```php
/**
 * 알림의 전달 지연 시간 설정
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
#### 알림 큐 연결 사용자 지정하기

기본적으로 큐에 쌓인 알림은 애플리케이션의 기본 큐 연결을 사용합니다. 특정 알림에 다른 큐 연결을 사용하길 원할 경우, 알림 클래스 생성자에서 `onConnection` 메서드를 호출하세요:

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
     * 새 알림 인스턴스 생성
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

또한 채널별로 큐 연결을 다르게 지정하려면 `viaConnections` 메서드를 정의할 수 있습니다. 이 메서드는 채널명과 큐 연결명을 쌍으로 갖는 배열을 반환해야 합니다:

```php
/**
 * 채널별로 사용할 큐 연결 지정
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
#### 알림 채널별 큐 사용자 지정하기

알림 클래스에 `viaQueues` 메서드를 정의해 채널별로 사용할 큐 이름을 지정할 수도 있습니다. 이 메서드는 채널명과 큐 이름을 쌍으로 갖는 배열을 반환해야 합니다:

```php
/**
 * 채널별 큐 이름 지정
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

큐에 쌓인 알림은 [큐 작업 미들웨어](/docs/11.x/queues#job-middleware)를 정의할 수 있습니다. 시작하려면 알림 클래스에 `middleware` 메서드를 정의하세요. 이 메서드는 `$notifiable`과 `$channel` 변수를 받아 알림을 전달할 목적지에 따라 미들웨어 배열을 반환할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 알림 큐 작업에서 통과할 미들웨어 반환
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
#### 큐잉된 알림과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 큐잉한 알림이 디스패치되면, 트랜잭션 커밋 전에 큐 워커가 알림 작업을 처리할 수 있습니다. 이 경우 트랜잭션 내에서 모델이나 데이터베이스 레코드에 한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있으며, 트랜잭션 내에 생성된 모델이나 레코드가 아예 데이터베이스에 존재하지 않을 수도 있습니다. 만약 알림이 이런 모델이나 데이터에 의존한다면, 예상치 못한 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`로 설정되어 있다면, 알림 전송 시 `afterCommit` 메서드를 호출해 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후에만 알림이 디스패치되도록 할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스의 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다:

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
     * 새 알림 인스턴스 생성
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이러한 문제 해결에 대한 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션 문서](/docs/11.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림을 전송할지 여부 결정하기

큐에 쌓인 알림이 워커에 의해 처리될 때 최종적으로 알림을 전송할지 판단하려면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 알림은 전송되지 않습니다:

```php
/**
 * 알림을 전송할지 결정
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림

때로 애플리케이션에 저장된 "사용자"가 아닌 임시 수신자에게 알림을 보내야 할 수도 있습니다. `Notification` 퍼사드의 `route` 메서드를 사용하면 알림 전송 전에 임시 라우팅 경로를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 경로로 보내면서 수신자의 이름도 같이 제공하려면, 이메일 주소를 키로, 이름을 값으로 갖는 배열 형태를 넘기면 됩니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널에 임시 라우팅 정보를 지정하려면 `routes` 메서드를 사용할 수 있습니다:

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

메일 채널을 지원하는 알림은 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 개체를 받아 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션성 이메일 메시지를 쉽게 작성할 수 있도록 간단한 메서드들을 제공합니다. 예를 들어 텍스트 한 줄, 액션 버튼(호출), 추가 텍스트 등을 포함할 수 있습니다. 예시 `toMail` 메서드는 다음과 같습니다:

```php
/**
 * 알림의 메일 표현 반환
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
> 위 예제에서 `$this->invoice->id`를 사용했네요. 알림 생성자에 알림 메시지 생성을 위한 데이터는 자유롭게 전달할 수 있습니다.

이 예제에서는 인사말, 한 줄 텍스트, 호출 버튼, 그리고 마지막 텍스트 한 줄을 순서대로 등록합니다. `MailMessage` 객체의 메서드들 덕분에 소규모 트랜잭션 이메일을 빠르고 쉽게 구성할 수 있습니다. 메일 채널은 이를 반응형 HTML 이메일 템플릿과 기본 텍스트 버전으로 자동 변환합니다. 아래는 `mail` 채널로 생성되는 이메일 예시입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" alt="알림 메일 예시" />

> [!NOTE]
> 메일 알림을 보낼 때는 `config/app.php` 설정 파일에 `name` 옵션을 꼭 지정하세요. 이 값이 메일 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 오류 메시지

청구 결제 실패와 같은 오류 알림을 보낼 때는 `error` 메서드를 호출해 오류용 메일임을 표시할 수 있습니다. 이 경우 액션 버튼 색상은 검정색 대신 빨간색으로 바뀝니다:

```php
/**
 * 알림의 메일 표현 반환
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
#### 그 외 메일 알림 포맷 옵션

알림 클래스 내에서 텍스트 줄을 일일이 작성하는 대신, `view` 메서드로 사용자 지정 템플릿을 지정할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

`view` 메서드에 배열을 전달하면, 첫 번째 요소는 기본 템플릿이고 두 번째는 일반 텍스트용 뷰를 지정합니다:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

순수 텍스트 뷰만 있을 때는 `text` 메서드를 이용하면 됩니다:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자 사용자 지정하기

메일 발신자 주소는 기본적으로 `config/mail.php` 설정에서 지정됩니다. 하지만 특정 알림에서 다른 발신자 주소를 지정하고 싶으면 `from` 메서드를 사용하세요:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 사용자 지정하기

`mail` 채널로 알림을 보낼 때 시스템은 기본적으로 알림 수신 객체(`$notifiable`)에 `email` 속성을 찾습니다. 수신 이메일 주소를 커스텀 지정하고 싶으면 수신 모델에 `routeNotificationForMail` 메서드를 정의하세요:

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
     * mail 채널에서 알림 라우팅 경로 지정
     *
     * @return array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // 이메일 주소만 반환
        return $this->email_address;

        // 이메일 주소와 이름을 함께 반환
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 사용자 지정하기

기본적으로 메일은 알림 클래스 이름을 기반으로 한 제목(Title Case)이 지정됩니다. 예를 들어 `InvoicePaid` 알림은 제목이 `Invoice Paid`가 됩니다. 다른 제목을 사용하고 싶다면 `subject` 메서드를 호출하세요:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 사용자 지정하기

이메일 알림은 기본 메일러(`config/mail.php`에서 정의)를 사용합니다. 실행 시 특정 메일러를 사용하려면 메시지 구성 시 `mailer` 메서드를 호출하세요:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 사용자 지정하기

메일 알림에 사용되는 HTML 및 텍스트 템플릿은 알림 패키지 리소스를 퍼블리시해서 사용자 지정할 수 있습니다. 아래 명령을 실행하면 템플릿이 `resources/views/vendor/notifications` 디렉터리에 복사됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 메시지 작성 중 `attach` 메서드를 사용하세요. 첫 번째 인자는 파일의 절대 경로입니다:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> 알림 메일 메시지의 `attach` 메서드는 [첨부 가능한 객체](/docs/11.x/mail#attachable-objects)도 지원합니다. 자세한 내용은 첨부 가능한 객체 문서를 참고하세요.

첨부 시 파일 표시 이름이나 MIME 타입 같은 추가 정보를 배열로 두 번째 인자에 전달할 수도 있습니다:

```php
/**
 * 알림의 메일 표현 반환
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

mailable 객체의 `attachFromStorage`처럼 스토리지 디스크에서 바로 첨부하는 메서드는 사용할 수 없습니다. 절대 경로를 이용해 `attach`를 호출하거나, `toMail` 메서드에서 [mailable](/docs/11.x/mail#generating-mailables) 객체를 반환하세요:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

여러 파일을 한꺼번에 첨부하려면 `attachMany` 메서드를 사용하세요:

```php
/**
 * 알림의 메일 표현 반환
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
#### 원시 데이터 첨부

`attachData` 메서드는 바이트 문자열(raw string) 데이터를 첨부파일로 추가할 때 사용합니다. 이때는 첨부파일명도 반드시 지정해야 합니다:

```php
/**
 * 알림의 메일 표현 반환
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
### 태그와 메타데이터 추가하기

Mailgun, Postmark 같은 일부 제3자 이메일 제공자는 메시지 "태그"와 "메타데이터"를 지원하여 이메일 그룹핑 및 추적에 활용할 수 있습니다. 태그와 메타데이터는 `tag`, `metadata` 메서드로 추가할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

Mailgun, Postmark, Amazon SES를 사용하는 경우 각 서비스 문서를 참고해 태그와 메타데이터 기능을 활용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 사용자 지정하기

`MailMessage`의 `withSymfonyMessage` 메서드는 메일 전송 전에 Symfony 메시지 객체를 직접 조작할 수 있도록 콜백을 등록하는 기능입니다. 이를 사용해 메일을 깊이 있게 사용자 지정할 수 있습니다:

```php
use Symfony\Component\Mime\Email;

/**
 * 알림의 메일 표현 반환
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

필요하다면 알림 `toMail` 메서드에서 [mailable 객체](/docs/11.x/mail)를 반환할 수 있습니다. 이 때는 Mailable 객체에서 직접 수신자 지정이 필요합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * 알림의 메일 표현 반환
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailables와 온디맨드 알림

온디맨드 알림을 보낼 때 `toMail`에 전달되는 `$notifiable`은 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스가 됩니다. 이 객체는 이메일 주소를 반환하는 `routeNotificationFor` 메서드를 제공합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * 알림의 메일 표현 반환
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

메일 알림 템플릿을 설계하는 동안, 실제 이메일을 보내지 않고도 브라우저에서 렌더링 결과를 빠르게 확인하고 싶을 수 있습니다. Laravel은 `MailMessage` 객체를 라우트 클로저나 컨트롤러에서 직접 반환할 수 있도록 지원합니다. 이 경우 메일 메시지는 브라우저에 렌더링되어 표시됩니다:

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

Markdown 메일 알림은 Laravel 기본 템플릿을 활용하면서도 길고 맞춤화된 메시지를 쓸 수 있게 해줍니다. Markdown 문법을 사용하므로 Laravel이 반응형 HTML 템플릿과 기본 텍스트 버전을 자동으로 생성해 줍니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

Markdown 템플릿을 사용하는 알림을 생성하려면 `make:notification` 명령어의 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 메일 알림과 마찬가지로, 알림 클래스에 `toMail` 메서드를 정의해야 하지만, 텍스트 줄과 호출버튼 대신 `markdown` 메서드로 템플릿명을 지정합니다. 템플릿에 전달할 데이터를 두 번째 인자로 넘길 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환
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

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법을 조합하여 작성합니다. Laravel의 미리 만들어진 컴포넌트를 활용해 쉽게 알림을 구성할 수 있습니다:

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

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url`과 옵션인 `color` 속성을 받습니다. 지원하는 색상은 `primary`, `green`, `red`입니다. 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 알림 본문과 약간 다른 배경색이 적용된 박스 영역 안에 텍스트를 보여줍니다. 특정 내용을 강조하는 데 유용합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

Markdown 테이블 문법을 HTML 테이블로 변환해주는 컴포넌트입니다. 컬럼 정렬도 Markdown 표준 문법을 따라 지원합니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 사용자 지정하기

Markdown 알림 컴포넌트를 애플리케이션으로 내보내 사용자 지정할 수 있습니다. 이때 `vendor:publish` Artisan 명령어로 `laravel-mail` 에셋 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이후 `resources/views/vendor/mail` 아래 `html` 및 `text` 디렉터리에 각각 HTML과 텍스트용 컴포넌트가 위치합니다. 자유롭게 수정 가능합니다.

<a name="customizing-the-css"></a>
#### CSS 사용자 지정하기

컴포넌트를 퍼블리시하면 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. 이 CSS 내용을 수정하면 자동으로 HTML 알림 템플릿에 인라인 스타일로 적용됩니다.

새 테마를 만들고 싶으면 이 디렉터리에 새 CSS 파일을 추가한 후, `mail` 설정 파일의 `theme` 옵션을 새 파일명으로 변경하세요.

특정 알림에서만 테마를 바꾸려면 메시지 작성 시 `theme` 메서드를 호출하면 됩니다:

```php
/**
 * 알림의 메일 표현 반환
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
### 전제 조건

`database` 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 유형과 함께 JSON 데이터 구조가 포함됩니다.

애플리케이션 UI에 알림을 보여주기 위해서는 먼저 알림 저장용 테이블을 생성해야 합니다. `make:notifications-table` 명령어로 적합한 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 만약 알림 대상 모델들이 [UUID 또는 ULID 기본키](/docs/11.x/eloquent#uuid-and-ulid-keys)를 사용한다면, 마이그레이션에서 `morphs` 대신 [`uuidMorphs`](/docs/11.x/migrations#column-method-uuidMorphs) 또는 [`ulidMorphs`](/docs/11.x/migrations#column-method-ulidMorphs)를 사용하세요.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

데이터베이스에 저장되는 알림은 `toDatabase` 또는 `toArray` 메서드를 정의해 알림 데이터를 배열 형태로 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 예제 `toArray` 메서드는 다음과 같습니다:

```php
/**
 * 알림의 배열 표현 반환
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

알림을 DB에 저장할 때, 기본적으로 `type` 컬럼은 알림 클래스명, `read_at` 컬럼은 `null`로 설정됩니다. 이 동작을 바꾸려면, 알림 클래스에 `databaseType`과 `initialDatabaseReadAtValue` 메서드를 정의할 수 있습니다:

```php
use Illuminate\Support\Carbon;

/**
 * 알림의 데이터베이스 타입 반환
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * "read_at" 컬럼의 초기값 반환
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs. `toArray`

`toArray` 메서드는 `broadcast` 채널에서도 브로드캐스트할 데이터를 결정하는 데 사용됩니다. `database`와 `broadcast` 채널에 대해 각각 다른 배열 표현을 원하면 `toArray` 대신 `toDatabase` 메서드를 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

알림이 데이터베이스에 저장된 후에는, notifiable 모델에서 `Illuminate\Notifications\Notifiable` 트레이트에 포함된 `notifications` [Eloquent 관계](/docs/11.x/eloquent-relationships)를 통해 쉽게 접근할 수 있습니다. 기본적으로 알림은 `created_at` 내림차순으로 정렬됩니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않은" 알림만 조회하려면 `unreadNotifications` 관계를 사용하세요:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript 클라이언트에서 알림을 읽으려면, 해당 알림을 반환하는 컨트롤러를 정의하고 HTTP 요청을 보내 데이터를 받아오면 됩니다.

<a name="marking-notifications-as-read"></a>
### 읽음 표시하기

사용자가 알림을 확인하면 일반적으로 "읽음" 상태로 표시합니다. `Notifiable` 트레이트는 `markAsRead` 메서드를 제공하며, 이는 데이터베이스의 `read_at` 컬럼을 갱신합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

컬렉션에서 일괄 호출해도 됩니다:

```php
$user->unreadNotifications->markAsRead();
```

또한 데이터베이스 쿼리를 직접 사용해 알림을 조회하지 않고도 일괄 업데이트할 수 있습니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 삭제하려면 다음처럼 쓸 수 있습니다:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 전제 조건

브로드캐스트 알림을 이용하기 전 Laravel의 [이벤트 브로드캐스팅](/docs/11.x/broadcasting)을 설정하고 사용법을 숙지하세요. 이벤트 브로드캐스트는 Laravel 서버 이벤트를 JavaScript 프론트엔드가 실시간으로 받을 수 있게 해줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel 이벤트 브로드캐스팅 서비스를 이용해 알림을 프론트엔드에 실시간 전달합니다. 알림 클래스에 `toBroadcast` 메서드를 정의해 `BroadcastMessage` 인스턴스를 반환하세요. `toBroadcast`가 없으면 `toArray` 데이터로 대체됩니다. 반환 데이터는 JSON 인코딩되어 프론트엔드에 브로드캐스트됩니다. 예제:

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 알림의 브로드캐스트 표현 반환
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
#### 브로드캐스트 큐 구성

브로드캐스트 알림은 모두 큐에 쌓입니다. 큐 연결이나 큐 이름을 지정하려면 `BroadcastMessage`의 `onConnection`과 `onQueue` 메서드를 사용하세요:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 사용자 지정하기

브로드캐스트 알림에는 알림 클래스명을 담은 `type` 필드가 기본으로 포함됩니다. 이 값을 바꾸려면 알림 클래스에 `broadcastType` 메서드를 정의하세요:

```php
/**
 * 브로드캐스트할 알림 타입 반환
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 듣기

브로드캐스트 알림은 `{notifiable}.{id}` 형식의 private 채널에 전달됩니다. 예를 들어, ID가 1인 `App\Models\User` 객체에게 보내면 `App.Models.User.1` 채널이 됩니다. [Laravel Echo](/docs/11.x/broadcasting#client-side-installation)를 이용하면 다음처럼 알림을 쉽게 받을 수 있습니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 브로드캐스트 채널 사용자 지정

알림의 브로드캐스트 채널을 수신 모델에서 변경하고 싶으면, `receivesBroadcastNotificationsOn` 메서드를 정의하세요:

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
     * 유저가 받을 브로드캐스트 채널 이름 반환
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
### 전제 조건

Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 Nexmo) 기반으로 작동합니다. 이를 사용하려면 `laravel/vonage-notification-channel`과 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

설정 파일을 애플리케이션에 퍼블리시하지 않아도 됩니다. 대신 `.env` 파일에 `VONAGE_KEY`, `VONAGE_SECRET` 환경 변수를 지정하세요. 기본 발신 번호는 역시 `.env`의 `VONAGE_SMS_FROM`로 설정하며, 이 번호는 Vonage 콘솔에서 생성할 수 있습니다:

```
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

SMS 채널로 알림을 지원하려면 알림 클래스에 `toVonage` 메서드를 정의하고, `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 표현 반환
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 내용

SMS 메시지가 유니코드 문자를 포함한다면, `VonageMessage` 작성시 `unicode` 메서드를 호출해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 표현 반환
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### 발신 번호 사용자 지정하기

기본 발신 번호 대신 다른 번호로 보내고 싶다면 `from` 메서드를 호출하세요:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 표현 반환
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

사용자별 비용 추적용으로 Vonage가 지원하는 "client reference"도 추가할 수 있습니다. 최대 40자 문자열입니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 표현 반환
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

Vonage 알림을 올바른 전화번호로 보내려면, 수신 모델에 `routeNotificationForVonage` 메서드를 정의하세요:

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
     * Vonage 채널용 라우팅 경로 반환
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
### 전제 조건

Slack 알림을 쓰려면 우선 Slack 알림 채널을 Composer로 설치하세요:

```shell
composer require laravel/slack-notification-channel
```

아울러 Slack 워크스페이스에 [Slack App](https://api.slack.com/apps?new_app=1)도 생성해야 합니다.

알림을 같은 워크스페이스 내에서 보낼 경우, Slack 앱에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한이 있어야 합니다. 앱 메시지를 Slack App 이름으로 전송하려면 `chat:write:bot` 권한도 필요합니다. 권한은 Slack 앱의 "OAuth & Permissions" 탭에서 추가합니다.

그리고 "Bot User OAuth Token"을 `services.php` 설정 파일 내 `slack` 배열에 복사해 넣어야 합니다. 이 토큰은 Slack "OAuth & Permissions" 탭에서 확인할 수 있습니다:

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

애플리케이션에서 사용자의 소유 Slack 워크스페이스로 알림을 보내려면, Slack 앱을 "배포(distribute)"해야 합니다. 이는 Slack 앱의 "Manage Distribution" 탭에서 관리할 수 있습니다. 배포 후 [Socialite](/docs/11.x/socialite)를 이용해 사용자를 인증하고 Slack 봇 토큰을 받을 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 메시지를 지원할 경우, 알림 클래스에 `toSlack` 메서드를 정의해 `$notifiable` 객체를 받고 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. Slack의 Block Kit API를 이용해 다양한 메시지를 만들 수 있습니다. 아래 예시는 [Slack Block Kit 빌더](https://app.slack.com/block-kit-builder/)에서 미리보기 가능하며, 블록들을 체이닝으로 구성하는 예시입니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 표현 반환
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

Slack Block Kit Builder에서 생성한 원본 JSON 페이로드를 그대로 `usingBlockKitTemplate` 메서드로 전달할 수도 있습니다:

```php
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 표현 반환
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

Slack Block Kit 알림은 [사용자 인터랙션 처리 기능](https://api.slack.com/interactivity/handling)을 지원합니다. Slack 앱의 "Interactivity"를 활성화하고, 애플리케이션이 이 요청을 처리할 URL("Request URL")을 설정해야 합니다. 이 설정은 Slack 앱의 "Interactivity & Shortcuts" 탭에서 가능합니다.

예를 들어, `actionsBlock` 메서드를 사용하는 알림에서는 사용자가 버튼 클릭 시 Slack이 POST 요청을 보내며, 여기에는 Slack 사용자 정보, 버튼 ID 등이 포함되어 있습니다. 애플리케이션은 이를 받아 알맞은 동작을 수행해야 합니다. 요청 출처가 Slack임을 반드시 [검증](https://api.slack.com/authentication/verifying-requests-from-slack)해야 합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 표현 반환
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
             // ID는 기본적으로 "button_acknowledge_invoice"...
            $block->button('Acknowledge Invoice')->primary();

            // 직접 ID 지정 가능
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달

사용자가 버튼 클릭 시 작업을 확실히 확인하게 하려면, 버튼에 `confirm` 메서드를 추가하세요. 이 메서드는 메시지와 클로저를 인자로 받으며, 클로저 내에서 `ConfirmObject`를 이용해 버튼명을 지정합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 표현 반환
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

빌드한 블록을 빠르게 검사하려면 `SlackMessage` 인스턴스에서 `dd` 메서드를 호출하세요. 이 메서드는 Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/) URL을 생성해 브라우저에서 페이로드를 미리 볼 수 있도록 해줍니다. `true` 인자를 넘기면 원시 JSON 페이로드를 덤프합니다:

```php
return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

슬랙 알림을 올바른 채널과 팀으로 보내려면, 수신 모델에 `routeNotificationForSlack` 메서드를 정의하세요. 반환값은 다음 중 하나가 될 수 있습니다:

- `null`: 알림 내에 지정된 채널로 라우팅을 위임 (SlackMessage의 `to` 메서드로 채널 지정 가능)
- 문자열: 슬랙 채널명 (예: `#support-channel`)
- `SlackRoute` 인스턴스: OAuth 토큰과 채널명을 함께 지정 가능, 외부 워크스페이스 전송 시 사용

예를 들어 아래 메서드는 앱 설정 파일의 봇 유저 토큰에 연동된 워크스페이스 내 `#support-channel`로 알림을 보냅니다:

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
     * Slack 채널용 라우팅 경로 반환
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
> 외부 Slack 워크스페이스로 알림을 보내려면 Slack 앱이 [배포되어 있어야 합니다](#slack-app-distribution).

사용자의 Slack 워크스페이스에 알림을 보내려면, 해당 사용자의 Slack OAuth 토큰을 먼저 받아야 합니다. [Laravel Socialite](/docs/11.x/socialite)의 Slack 드라이버를 사용하면 이를 간단히 처리할 수 있습니다.

그런 다음 사용자의 워크스페이스로 알림을 보내려면 `SlackRoute::make` 메서드를 사용할 수 있습니다. 보통 사용자에게 알림을 받을 채널을 지정할 기회를 애플리케이션이 제공해야 합니다:

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
     * Slack 채널용 라우팅 경로 반환
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 로컬라이징

Laravel은 HTTP 요청의 현재 로케일과 다른 로케일로 알림을 보낼 수 있으며, 큐잉할 때도 이 로케일을 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스의 `locale` 메서드로 원하는 언어를 지정하세요. 알림 처리 시 애플리케이션 언어가 변경되었다가 완료 후 원래대로 복원됩니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

`Notification` 퍼사드는 다수의 수신자도 그대로 지원합니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

사용자의 선호 로케일을 DB에 저장하는 경우, notifiable 모델에 `HasLocalePreference` 계약을 구현해 선호 로케일을 알려줄 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일 반환
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

인터페이스 구현 후 Laravel은 자동으로 이 선호 로케일을 사용하므로, `locale` 메서드 호출이 필요 없습니다:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

`Notification` 퍼사드의 `fake` 메서드를 사용해 알림 전송을 가로챌 수 있습니다. 알림 전송은 보통 테스트 대상 코드와 직접적인 관련이 없으므로, 주로 특정 알림이 이벤트로서 보내졌는지 여부만 검사하면 충분합니다.

`fake` 호출 후, 알림이 지정된 수신자에게 전송되었는지, 어떤 데이터가 전달되었는지 다음과 같이 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // 주문 배송 로직 수행...

    // 알림이 전혀 전송되지 않았음을 확인
    Notification::assertNothingSent();

    // 특정 사용자에게 알림이 전송되었는지 확인
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

        // 주문 배송 로직 수행...

        // 알림이 전혀 전송되지 않았음을 확인
        Notification::assertNothingSent();

        // 특정 사용자에게 알림이 전송되었는지 확인
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

`assertSentTo` 또는 `assertNotSentTo`에 클로저를 넘겨 특정 조건을 확인할 수도 있습니다. 조건을 만족하는 알림이 1개 이상 전송된 경우 성공합니다:

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

테스트 코드가 [온디맨드 알림](#on-demand-notifications)을 보낼 경우, `assertSentOnDemand` 메서드로 검증할 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인자로 클로저를 넘겨 특정 라우트 주소에 온디맨드 알림이 전송되었는지 확인할 수도 있습니다:

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

알림이 전송되는 도중 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 발송됩니다. 이 이벤트는 수신자 객체와 알림 인스턴스를 포함합니다. 애플리케이션에서 이 이벤트에 대응하는 [리스너](/docs/11.x/events)를 작성할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * 이벤트 처리
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

만약 `handle` 메서드가 `false`를 반환하면 알림 전송을 중단합니다:

```php
/**
 * 이벤트 처리
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

리스너 내에서 이벤트의 `notifiable`, `notification`, `channel` 속성에 접근할 수 있습니다:

```php
/**
 * 이벤트 처리
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

알림 전송이 완료되면 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발송됩니다. 이 이벤트 역시 수신자와 알림 인스턴스를 포함하며, 리스너를 작성해 대응할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * 이벤트 처리
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

리스너 내에서는 `notifiable`, `notification`, `channel`, `response` 속성에 접근할 수 있습니다:

```php
/**
 * 이벤트 처리
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

Laravel은 기본적으로 몇 가지 알림 채널을 제공하지만, 직접 알림 드라이버를 만들어 다른 채널로 알림을 전송할 수도 있습니다. 다음과 같이 `send` 메서드를 갖는 클래스를 정의해 시작할 수 있습니다. `send` 메서드는 `$notifiable`과 `$notification`을 인자로 받습니다.

`send` 메서드 내에서 알림의 커스텀 메시지 객체를 얻고, 원하는 방식으로 수신자에게 메시지를 전달하세요:

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 알림 전송
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable에게 알림 전송...
    }
}
```

이제 알림 클래스의 `via` 메서드에서 해당 채널 클래스를 반환할 수 있습니다. 아래 예시는 `toVoice` 메서드가 음성 메시지를 표현하는 임의의 `VoiceMessage` 객체를 반환하는 상황입니다:

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
     * 알림 채널 지정
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * 음성 메시지 표현 반환
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```