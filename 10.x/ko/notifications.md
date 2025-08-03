# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 전송하기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
    - [온디맨드 알림 (On-Demand Notifications)](#on-demand-notifications)
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
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅하기](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림 읽음 처리하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅하기](#formatting-broadcast-notifications)
    - [알림 수신 대기하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비사항](#sms-prerequisites)
    - [SMS 알림 포맷팅하기](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅하기](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비사항](#slack-prerequisites)
    - [Slack 알림 포맷팅하기](#formatting-slack-notifications)
    - [Slack 인터랙티비티](#slack-interactivity)
    - [Slack 알림 라우팅하기](#routing-slack-notifications)
    - [외부 Slack 워크스페이스에 알림 보내기](#notifying-external-slack-workspaces)
- [알림 현지화(Localizing Notifications)](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

Laravel은 [이메일 전송](/docs/10.x/mail)뿐만 아니라, 이메일, SMS(과거 Nexmo로 불리던 [Vonage](https://www.vonage.com/communications-apis/) 사용), 그리고 [Slack](https://slack.com)을 포함한 다양한 전송 채널을 통한 알림 기능을 제공합니다. 또한, 여러 커뮤니티에서 제작한 다양한 [알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 있어, 수십 가지 다른 채널을 통해 알림을 보내는 것도 가능합니다. 알림은 데이터베이스에 저장해서 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 어떤 일을 간단히 알려주는, 짧고 정보성 있는 메시지여야 합니다. 예를 들어, 청구 애플리케이션을 작성 중이라면, 이메일과 SMS 채널을 통해 "청구서 결제 완료" 알림을 사용자에게 전송할 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 알림 하나는 보통 `app/Notifications` 디렉터리에 저장되는 하나의 클래스입니다. 만약 해당 디렉터리가 없다면 걱정하지 마세요. `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 새 알림 클래스를 `app/Notifications` 디렉터리에 생성합니다. 각 알림 클래스는 `via` 메서드와, `toMail` 또는 `toDatabase` 같은 특정 채널에 맞는 메시지 생성 메서드를 포함합니다. 이 메서드들은 알림을 해당 채널에 맞는 메시지로 변환합니다.

<a name="sending-notifications"></a>
## 알림 전송하기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, `Notification` [파사드](/docs/10.x/facades)를 사용할 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 받습니다:

```
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]  
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 꼭 `User` 모델에만 한정되지 않습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

대안으로, `Notification` [파사드](/docs/10.x/facades)를 통해 알림을 보낼 수 있습니다. 이 방법은 여러 명의 Notifiable 엔티티(예: 여러 사용자 컬렉션)에게 알림을 보낼 때 유용합니다. 파사드의 `send` 메서드에 수신자들과 알림 인스턴스를 전달해 전송합니다:

```
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

또한, `sendNow` 메서드를 사용해 즉시 알림을 보낼 수도 있습니다. `sendNow`는 알림이 `ShouldQueue` 인터페이스를 구현해도 큐를 거치지 않고 바로 전송합니다:

```
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

각 알림 클래스는 어떤 채널로 알림을 전송할지 결정하는 `via` 메서드를 갖고 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 보낼 수 있습니다.

> [!NOTE]  
> Telegram, Pusher 등의 다른 채널을 사용하고 싶다면, 커뮤니티 주도의 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 확인해 보세요.

`via` 메서드는 `$notifiable` 인스턴스를 전달받는데, 이 인스턴스는 알림이 전달될 대상 클래스의 객체입니다. 필요에 따라 `$notifiable`을 참조하여 알림을 보낼 채널을 결정할 수 있습니다:

```
/**
 * 알림의 전송 채널을 반환합니다.
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
> 알림 큐잉 전에 큐 설정 및 큐 워커 작동을 반드시 완료하세요. ([작업 큐 워커 실행하기](/docs/10.x/queues#running-the-queue-worker) 참고)

알림 전송은, 특히 외부 API 호출을 해야 한다면 시간이 걸릴 수 있습니다. 애플리케이션의 응답 속도를 높이려면, `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 사용하여 알림을 큐에 보낼 수 있습니다. `make:notification` 명령어로 생성한 알림에는 기본적으로 해당 인터페이스와 트레이트가 import 되어 있으니 즉시 추가하세요:

```
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

`ShouldQueue`가 추가된 알림은 일반적으로 전송하듯 호출하면 Laravel이 자동으로 큐에 작업을 추가해 비동기로 알림을 보내줍니다:

```
$user->notify(new InvoicePaid($invoice));
```

큐 처리 시 한 수신자와 한 채널 조합마다 개별 작업이 생성됩니다. 예를 들어, 수신자가 3명이고 채널이 2개라면 총 6개의 작업이 큐에 추가됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연 보내기

알림 전송을 지연시키고 싶으면 알림 인스턴스에 `delay` 메서드를 체이닝할 수 있습니다:

```
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

<a name="delaying-notifications-per-channel"></a>
#### 채널별 지연 보내기

`delay` 메서드에 배열을 전달해 각 채널별로 다른 지연 시간을 지정할 수도 있습니다:

```
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는, 알림 클래스 내에 `withDelay` 메서드를 정의하여 채널별 지연을 반환할 수도 있습니다:

```
/**
 * 알림 전송 지연을 채널별로 결정합니다.
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

기본적으로, 큐에 들어가는 알림은 애플리케이션 기본 큐 연결을 사용합니다. 특정 알림에서 다른 큐 연결을 사용하려면 알림 클래스의 생성자에서 `onConnection` 메서드를 호출하면 됩니다:

```
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * 새 알림 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

또는, 알림에서 지원하는 각 채널에 대해 사용할 큐 연결을 지정하고 싶으면 `viaConnections` 메서드를 정의할 수 있습니다. 이 메서드는 채널명과 연결 이름이 포함된 배열을 반환해야 합니다:

```
/**
 * 각 채널에서 사용할 큐 연결을 결정합니다.
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

알림 채널별로 사용할 큐 이름을 지정하려면 `viaQueues` 메서드를 정의할 수 있습니다. 채널명과 큐 이름의 배열을 반환해야 합니다:

```
/**
 * 각 채널에서 사용할 큐 이름을 결정합니다.
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

<a name="queued-notifications-and-database-transactions"></a>
#### 큐 알림과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 큐 알림을 디스패치하면 큐 작업이 트랜잭션 커밋 전에 실행될 수 있습니다. 이 경우 트랜잭션 동안 변경한 모델이나 데이터가 아직 데이터베이스에 반영되지 않아 알림 처리 중 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`라면, `afterCommit` 메서드를 호출해 트랜잭션 커밋 이후에 알림을 디스패치하도록 지정할 수 있습니다:

```
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스 생성자에서 직접 호출할 수도 있습니다:

```
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * 새 알림 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]  
> 관련 문제 우회법에 대해 더 알고 싶다면 [큐 작업과 데이터베이스 트랜잭션](/docs/10.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림의 전송 여부 결정하기

큐에 디스패치된 알림이 큐 워커에서 처리될 때, 실제 전송할지 여부를 최종 판단하려면 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 만약 `false`를 반환하면 알림이 전송되지 않습니다:

```
/**
 * 알림이 전송될지 여부를 판단합니다.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림 (On-Demand Notifications)

애플리케이션 "사용자"로 등록되지 않은 대상에게 알림을 보내야 할 때가 있습니다. `Notification` 파사드의 `route` 메서드를 사용하면 동적으로 알림 수신 경로를 지정할 수 있습니다:

```
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
            ->route('vonage', '5555555555')
            ->route('slack', '#slack-channel')
            ->route('broadcast', [new Channel('channel-name')])
            ->notify(new InvoicePaid($invoice));
```

메일 알림의 경우, 수신자 이름과 이메일 주소를 배열 형태로 전달할 수도 있습니다:

```
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드는 한 번에 여러 채널에 대한 라우팅 정보를 배열로 전달할 수 있습니다:

```
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅하기

알림에 이메일 전송 지원이 있다면 알림 클래스에 `toMail` 메서드를 정의하세요. 이 메서드는 `$notifiable` 엔티티를 전달받으며, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 간단한 이메일 메일 메시지를 쉽게 만들도록 돕는 몇 가지 메서드를 제공합니다. 텍스트 한 줄 라인이나 "액션 버튼" 같은 기능을 포함할 수 있습니다. 예를 살펴봅시다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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
> 위 예시에서 `$this->invoice->id`처럼, 알림 클래스 생성자에 필요한 데이터를 전달해 메시지 생성에 활용하세요.

예시에서는 인사말, 텍스트 라인, 액션 버튼, 다시 텍스트 라인을 등록합니다. `MailMessage`가 제공하는 메서드는 작고 간단한 트랜잭션성 이메일을 빠르게 포맷팅할 수 있게 해줍니다. `mail` 채널은 이 메시지 구성 요소들을 아름답고 반응형인 HTML 이메일 템플릿과 단순 텍스트 버전으로 변환해 줍니다. 다음은 그런 `mail` 채널을 통한 이메일 예시입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]  
> 메일 알림을 보낼 때는 `config/app.php` 설정파일에 있는 `name` 옵션을 적절히 설정하세요. 이 값은 메일 알림의 상단/하단에 표시됩니다.

<a name="error-messages"></a>
#### 에러 메시지

알림 중에는 결제 실패 같은 에러 관련 알림도 있습니다. 이 경우 `error` 메서드를 호출해 메일 메시지가 에러 성격임을 표시할 수 있습니다. `error`를 호출하면 액션 버튼이 검정색 대신 빨간색으로 표시됩니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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
#### 그 밖의 메일 알림 포맷팅 방법

텍스트 라인을 코드로 일일이 적는 대신, 커스텀 템플릿을 지정해 사용할 수도 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

단순 텍스트용 뷰는 두번째 요소로 배열에 포함시켜 전달할 수 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

또는, 텍스트 전용 메시지만 있다면 `text` 메서드를 쓸 수 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

메일의 발신자 주소는 기본적으로 `config/mail.php` 설정에서 지정합니다. 하지만 알림별로 발신자 주소를 지정하고 싶으면 `from` 메서드를 쓸 수 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

`mail` 채널을 통해 알림을 보낼 때, 기본적으로는 Notifiable 엔티티에서 `email` 속성을 찾아 이메일 주소를 참조합니다. 이 기본 동작을 바꾸려면, Notifiable 엔티티에 `routeNotificationForMail` 메서드를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * mail 채널 알림을 위한 라우팅 주소를 리턴합니다.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // 이메일 주소만 반환...
        return $this->email_address;

        // 이메일 주소와 이름 함께 반환...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 커스터마이징

기본적으로 메일 제목은 알림 클래스 이름을 "타이틀 케이스"로 변경한 형태입니다. 예를 들어 `InvoicePaid` 클래스는 기본 제목이 `Invoice Paid`가 됩니다. 다른 제목을 지정하고 싶다면 메시지 빌드 시 `subject` 메서드를 호출하세요:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

기본적으로 메일 알림은 `config/mail.php`에 정의된 기본 메일러를 사용합니다. 실행 시점에 다른 메일러를 사용하고 싶다면 `mailer` 메서드를 통해 지정할 수 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

메일 알림에서 사용하는 HTML 및 단순 텍스트 템플릿은 알림 패키지를 퍼블리시 하면 수정할 수 있습니다. 아래 명령어를 실행하면 템플릿이 `resources/views/vendor/notifications` 디렉터리에 복사됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 메시지 빌드 시 `attach` 메서드를 사용하세요. 첫 인수는 파일의 절대 경로입니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file');
}
```

> [!NOTE]  
> 알림 메일 메시지의 `attach` 메서드는 [attachable objects](/docs/10.x/mail#attachable-objects)도 지원합니다. 필요시 참고하세요.

첨부 시 이름, MIME 타입 등을 옵션으로 지정할 때는 `attach`의 두 번째 인수로 배열을 전달하세요:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

스토리지 디스크에서 바로 첨부하는 `attachFromStorage`는 지원하지 않습니다. 대신 절대 경로를 제공하는 `attach` 메서드를 쓰거나, `toMail`에서 [mailables](/docs/10.x/mail#generating-mailables)를 반환해 사용하는 방식을 추천합니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 메일 알림 표현을 가져옵니다.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email)
                ->attachFromStorage('/path/to/file');
}
```

여러 파일 첨부는 `attachMany` 메서드를 사용합니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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
#### 원시 데이터 첨부하기

`attachData` 메서드를 사용하면 바이너리 바이트 문자열을 원시 첨부파일로 붙일 수 있습니다. 이때는 첨부될 파일 이름을 반드시 지정해야 합니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

Mailgun, Postmark 등 일부 외부 이메일 서비스에서는 메일에 "태그"와 "메타데이터"를 붙여 보내기 유용합니다. 알림 메일 메시지에 `tag`와 `metadata` 메서드를 사용해 태그와 메타데이터를 추가하세요:

```
/**
 * 메일 알림 표현을 가져옵니다.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
                ->greeting('Comment Upvoted!')
                ->tag('upvote')
                ->metadata('comment_id', $this->comment->id);
}
```

Mailgun, Postmark 관련해 더 자세한 내용은 각각의 문서에서 [태그]와 [메타데이터] 관련 내용을 참고하세요. 아마존 SES를 사용하는 경우, [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메타데이터로 첨부하면 됩니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 통해, 최종 메일 전송 전 Symfony 메시지 객체를 직접 조작할 수 있습니다. 클로저를 전달하여 메시지의 헤더나 내용 등을 세밀하게 조정할 기회를 제공합니다:

```
use Symfony\Component\Mime\Email;

/**
 * 메일 알림 표현을 가져옵니다.
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

필요하다면, 알림 클래스의 `toMail` 메서드에서 [mailable 객체](/docs/10.x/mail)를 직접 반환해도 됩니다. 이 경우 수신자를 mailable 객체 내부에서 `to` 메서드로 지정해야 합니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * 메일 알림 표현을 가져옵니다.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailables와 온디맨드 알림

[온디맨드 알림](#on-demand-notifications)을 보낼 때는 `toMail`에 전달되는 `$notifiable`이 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스입니다. 이 객체는 `routeNotificationFor` 메서드를 제공해 이메일 주소를 가져올 수 있습니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * 메일 알림 표현을 가져옵니다.
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

메일 알림 템플릿을 설계할 때, 브라우저에서 Blade 템플릿처럼 바로 렌더링해 보는 것이 유용합니다. Laravel은 라우트 클로저나 컨트롤러에서 메일 알림 메시지를 직접 반환하면, 이를 렌더링해 브라우저에 표시하는 기능을 지원합니다:

```
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

마크다운 문법을 사용하는 메일 알림은 Laravel이 미리 제작한 이메일 템플릿을 활용하되, 좀 더 자유롭게 길고 맞춤화된 메시지를 작성할 수 있도록 해줍니다. Markdown으로 작성하면 Laravel이 아름답고 반응형 HTML 템플릿과 함께 자동으로 일반 텍스트 대비본도 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

Markdown 템플릿이 적용된 알림을 생성하려면 `make:notification` 명령어에 `--markdown` 옵션을 넣습니다:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

모든 메일 알림처럼 `toMail` 메서드를 정의하세요. 그리고 `line`, `action` 대신 `markdown` 메서드로 템플릿 이름을 명시합니다. 템플릿에 전달할 데이터를 두 번째 인수로 배열 형태로 전달할 수 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

Markdown 메일 알림에서는 Blade 컴포넌트와 Markdown 문법을 조합해 쉽게 구성할 수 있습니다. Laravel이 미리 제공하는 컴포넌트를 활용하세요:

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

버튼 컴포넌트는 중앙 정렬된 링크 버튼을 만듭니다. `url`과 선택적 `color` 속성을 받을 수 있으며, 색상은 `primary`, `green`, `red`가 지원됩니다. 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 알림에서 다른 배경색을 가진 영역을 만들어 주의를 끌 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블 문법을 HTML 테이블로 변환합니다. 기본 마크다운 테이블 정렬 문법도 지원됩니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

Markdown 알림 컴포넌트를 내 애플리케이션에 복사해 직접 수정할 수 있습니다. 아래 명령어로 `laravel-mail` 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

복사된 컴포넌트들은 `resources/views/vendor/mail` 디렉터리에 위치합니다. `html`과 `text` 하위디렉터리에 각각 컴포넌트별 템플릿이 들어있습니다. 자유롭게 수정해도 됩니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

퍼블리시된 후, `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 있습니다. 이 CSS를 수정하면 HTML 알림 내에 자동으로 스타일이 인라인 됩니다.

완전히 새 테마를 만들고 싶다면, `html/themes`에 새 CSS 파일을 저장하고 `mail` 설정 파일 내 `theme` 옵션을 새 테마 이름으로 변경하세요.

개별 알림 템플릿에서 테마를 바꾸려면, 메일 메시지 빌드 시 `theme` 메서드 호출해 사용 테마를 지정할 수 있습니다:

```
/**
 * 메일 알림 표현을 가져옵니다.
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

`database` 채널 알림은 알림 정보를 데이터베이스 테이블에 저장합니다. 테이블에는 알림 타입과 알림 내용을 나타내는 JSON 데이터가 들어갑니다.

테이블이 필요하므로, `notifications:table` Artisan 명령어로 올바른 스키마의 마이그레이션을 생성하고 실행하세요:

```shell
php artisan notifications:table

php artisan migrate
```

> [!NOTE]  
> Notifiable 모델이 [UUID 또는 ULID 기본키](/docs/10.x/eloquent#uuid-and-ulid-keys)를 쓴다면, 마이그레이션에서 `morphs` 대신 [`uuidMorphs`](/docs/10.x/migrations#column-method-uuidMorphs) 또는 [`ulidMorphs`](/docs/10.x/migrations#column-method-ulidMorphs)를 사용해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅하기

데이터베이스에 저장 가능한 알림이라면 `toDatabase` 또는 `toArray` 메서드를 정의하세요. `$notifiable`을 받고 PHP 배열을 반환해야 하며, 이 배열은 JSON 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 예:

```
/**
 * 알림의 배열 표현을 가져옵니다.
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

데이터베이스 저장 시 기본적으로 `type` 컬럼은 알림 클래스 이름으로 채워집니다. 이것을 바꾸고 싶으면 `databaseType` 메서드를 정의하세요:

```
/**
 * 데이터베이스에 저장할 알림 타입을 반환합니다.
 *
 * @return string
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs. `toArray`

`toArray` 메서드는 방송(broadcast) 채널에서도 똑같이 사용됩니다. 만약 `database` 채널과 `broadcast` 채널에 대해 다른 배열 표현을 원한다면 `toDatabase`를 따로 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

데이터베이스에 저장된 알림은 Notifiable 모델 내의 `Illuminate\Notifications\Notifiable` 트레이트가 포함하는 `notifications` [Eloquent 연관관계](/docs/10.x/eloquent-relationships)를 통해 편리하게 조회할 수 있습니다. 보통은 아래처럼 사용할 수 있습니다. 최근 알림이 가장 앞에 옵니다:

```
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은(unread) 알림만 가져오려면, `unreadNotifications` 관계를 사용하세요:

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]  
> JavaScript 클라이언트에서 알림을 사용하려면, 알림을 반환하는 컨트롤러를 구현하고 해당 URL에 HTTP 요청을 보내는 방식을 사용하세요.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 처리하기

보통 사용자가 알림을 확인하면 알림을 읽음 상태로 변경합니다. `Notifiable` 트레이트는 `markAsRead` 메서드를 제공하여 `read_at` 컬럼을 업데이트합니다:

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

컬렉션 전체에서 바로 호출할 수도 있습니다:

```
$user->unreadNotifications->markAsRead();
```

DB에서 직접 대량으로 읽음 처리하려면, 업데이트 쿼리를 실행하세요:

```
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 삭제하려면 다음과 같이 할 수 있습니다:

```
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비사항

브로드캐스트 알림을 사용하려면, Laravel의 [이벤트 브로드캐스팅](/docs/10.x/broadcasting) 기능 설정 및 개념을 숙지해야 합니다. 이벤트 브로드캐스팅을 통해 백엔드 Laravel 이벤트를 JavaScript 프런트엔드에서 실시간으로 수신할 수 있습니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅하기

`broadcast` 채널은 이벤트 브로드캐스팅을 통해 JavaScript 프런트엔드에 알림을 실시간으로 전달합니다. 알림에서 `toBroadcast` 메서드를 정의하면 `$notifiable` 엔티티를 받고, `BroadcastMessage` 인스턴스를 반환해야 합니다. 없으면 `toArray`의 결과를 사용합니다. 예:

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트할 알림 표현을 가져옵니다.
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

브로드캐스트 알림은 모두 큐에 추가됩니다. 큐 연결이나 큐 이름을 변경하려면 `BroadcastMessage`의 `onConnection`과 `onQueue` 메서드를 사용하세요:

```
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

모든 브로드캐스트 알림에는 알림 클래스 전체 경로를 담은 `type` 필드가 포함됩니다. 바꾸고 싶으면 알림 클래스에 `broadcastType` 메서드를 정의하세요:

```
/**
 * 브로드캐스트 알림 타입을 반환합니다.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 대기하기

알림은 기본적으로 `{notifiable}.{id}` 채널명으로 개인(private) 채널에 브로드캐스트됩니다. 예를 들어 `App\Models\User` 인스턴스 ID가 1이라면, `App.Models.User.1` 채널에 브로드캐스트됩니다. [Laravel Echo](/docs/10.x/broadcasting#client-side-installation)를 사용할 때는 다음처럼 알림 리스너를 등록할 수 있습니다:

```
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이징

알림을 받을 채널 이름을 커스터마이즈하려면 Notifiable 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * 사용자가 받는 알림 방송 채널을 반환합니다.
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
### 사전 준비사항

Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 Nexmo)를 통해 지원됩니다. 먼저, `laravel/vonage-notification-channel`과 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)을 포함하지만, 별도로 퍼블리시하지 않아도 됩니다. 환경변수 `VONAGE_KEY` 와 `VONAGE_SECRET` 에 Vonage 키를 지정하세요.

또한 기본 발신 번호를 `VONAGE_SMS_FROM` 환경변수에 설정해야 합니다. 이 번호는 Vonage 콘솔에서 생성 가능합니다:

```
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅하기

알림이 SMS 전송을 지원하려면 `toVonage` 메서드를 알림 클래스에 정의하세요. `$notifiable`을 인수로 받고 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 전송용 알림 표현을 가져옵니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 콘텐츠

SMS 본문에 유니코드 문자가 있을 경우, `unicode` 메서드를 호출해서 메시지를 유니코드로 처리하도록 하세요:

```
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 전송용 알림 표현을 가져옵니다.
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

기본 발신 번호와 달리, 특정 알림은 다른 번호로 보내고 싶으면 `from` 메서드를 사용하세요:

```
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 전송용 알림 표현을 가져옵니다.
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

사용자, 팀, 클라이언트별 비용 추적을 위해 "클라이언트 참조" 필드를 추가할 수 있습니다. Vonage 보고서에 활용됩니다. 최대 40자 문자열까지 지정 가능합니다:

```
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 전송용 알림 표현을 가져옵니다.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅하기

Vonage 채널에 알맞은 수신 전화번호를 라우팅하려면 Notifiable 엔티티에 `routeNotificationForVonage` 메서드를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Vonage 채널 알림 라우팅 주소를 반환합니다.
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
### 사전 준비사항

Slack 알림을 보내려면, 먼저 Slack 채널 패키지를 설치하세요:

```shell
composer require laravel/slack-notification-channel
```

그리고 Slack 워크스페이스용 [Slack App](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

만약 Slack App을 생성한 동일 워크스페이스에만 알림을 보낼 예정이라면, App에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한이 부여돼 있어야 합니다. 이 권한은 Slack의 "OAuth & Permissions" 관리 탭에서 추가할 수 있습니다.

그 후, App의 "Bot User OAuth Token"을 복사해 애플리케이션 `services.php` 설정파일 내 `slack` 배열에 넣으세요:

```
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### App 배포

사용자의 워크스페이스 여러 곳에 알림을 보내려면 Slack App을 배포(distribute)해야 합니다. App의 "Manage Distribution" 탭에서 관리하며, 배포 완료 후 Laravel Socialite를 이용해 사용자 대리로 [Slack 봇 토큰을 얻을 수 있습니다](/docs/10.x/socialite#slack-bot-scopes).

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅하기

Slack 메시지 지원을 위해 알림에 `toSlack` 메서드를 정의하세요. 이 메서드는 `$notifiable` 엔티티를 받고 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환합니다. Slack의 Block Kit API를 이용해 풍부한 메시지를 만들 수 있습니다. 아래는 Slack Block Kit 빌더에서 미리보기가 가능한 예시입니다:

```
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현을 가져옵니다.
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

<a name="slack-interactivity"></a>
### Slack 인터랙티비티

Slack의 Block Kit은 [사용자 인터랙션 처리 기능](https://api.slack.com/interactivity/handling)을 지원합니다. 이를 활용하려면 Slack App에서 "Interactivity"를 활성화하고 앱이 수신할 "Request URL"을 지정해야 합니다 (Slack의 "Interactivity & Shortcuts" 탭에서 설정).

다음 예시에서 `actionsBlock` 메서드는 버튼 클릭 시 Slack이 애플리케이션의 "Request URL"로 `POST` 요청을 전송합니다. 요청 페이로드에는 사용자 정보, 클릭된 버튼 ID 등이 포함됩니다. 애플리케이션에서 Slack의 요청임을 검증하는 작업도 필요합니다:

```
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현을 가져옵니다.
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
                 // 기본 ID는 "button_acknowledge_invoice"...
                $block->button('Acknowledge Invoice')->primary();

                // ID 수동 지정...
                $block->button('Deny')->danger()->id('deny_invoice');
            });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달

사용자가 동작 전에 반드시 확인하도록 버튼에 컨펌을 붙일 수 있습니다. `confirm` 메서드는 메시지와 `ConfirmObject`를 받는 클로저를 인수로 받습니다:

```
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현을 가져옵니다.
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
#### Slack 블록 점검하기

지금까지 만든 블록 구성을 빠르게 점검하려면 `SlackMessage`에 `dd` 메서드를 호출하세요. 이 메서드는 Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/) URL을 생성해 출력해 주며, 브라우저에서 페이로드와 알림 미리보기를 확인할 수 있습니다. `true`를 인자로 넘겨 원시 페이로드를 볼 수도 있습니다:

```
return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅하기

Slack 알림이 올바른 팀과 채널로 가도록 하려면, Notifiable 모델에 `routeNotificationForSlack` 메서드를 정의하세요. 반환값으로는 다음 중 하나를 줄 수 있습니다:

- `null`: 알림 클래스 내에 지정된 채널로 전송됨 (`to` 메서드로 채널 지정 가능)
- 문자열: Slack 채널 이름, 예: `#support-channel`
- `SlackRoute` 인스턴스: 외부 워크스페이스와 OAuth 토큰을 지정할 때 쓴다

예를 들어, `#support-channel`을 반환하면 `services.php`에 설정한 토큰에 해당하는 워크스페이스 내 해당 채널에 보내집니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Slack 채널 알림의 라우팅 주소를 반환합니다.
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
> 외부 워크스페이스에 알림을 보낼 때는 Slack App을 반드시 [배포](#slack-app-distribution)해야 합니다.

사용자 소유 외부 Slack 워크스페이스로 알림을 보내려면, 우선 사용자의 Slack OAuth 토큰을 확보해야 합니다. Laravel Socialite의 Slack 드라이버를 사용하면 쉽게 인증 및 봇 토큰을 얻을 수 있습니다.

토큰을 얻고 DB에 저장한 후에는 아래처럼 `SlackRoute::make` 메서드를 이용해 특정 채널과 토큰을 가진 SlackRoute 인스턴스를 반환해 해당 워크스페이스로 라우팅할 수 있습니다:

```
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
     * Slack 채널 알림 라우팅 주소를 반환합니다.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 현지화(Localizing Notifications)

Laravel은 HTTP 요청의 현재 로케일과 다른 언어로도 알림을 보낼 수 있습니다. 큐에 저장된 알림도 이 로케일을 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스는 원하는 로케일을 지정하는 `locale` 메서드를 제공합니다. 알림이 처리될 때 설정한 로케일로 일시적으로 전환하며, 전송 후 원래 로케일로 복원합니다:

```
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

`Notification` 파사드를 통해 여러 Notifiable 엔티티에게 여러 로케일로 전송할 수도 있습니다:

```
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

일부 앱은 사용자의 선호 로케일을 저장합니다. Notifiable 모델이 `HasLocalePreference` 계약을 구현하면, Laravel은 해당 선호 로케일을 자동으로 사용해 알림과 메일을 보냅니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자 선호 로케일을 반환합니다.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

인터페이스를 구현하면 별도로 `locale` 메서드를 호출하지 않아도 됩니다:

```
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

알림이 실제로 전송되는 대신, `Notification` 파사드의 `fake` 메서드를 사용해 테스트에선 전송을 막을 수 있습니다. 보통 알림 전송은 테스트 대상 코드와 관계없으므로, 알림이 전송되었는지 여부를 검증하는 정도로 충분합니다.

`fake` 후에는 특정 알림이 특정 사용자에게 전송됐는지, 또는 전송이 안 됐는지 등을 바로 단언(assert)할 수 있습니다:

```
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

        // 주문 배송 처리...

        // 알림이 전송되지 않았음을 단언
        Notification::assertNothingSent();

        // 특정 사용자에게 알림이 전송되었음을 단언
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 특정 알림이 전송되지 않았음을 단언
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 전송된 알림 개수를 단언
        Notification::assertCount(3);
    }
}
```

또한 단언 메서드에 클로저를 넘겨 추가 검증도 가능합니다. 예상한 알림이 최소 한 건이라도 조건을 만족하면 성공입니다:

```
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 알림

[온디맨드 알림](#on-demand-notifications)의 테스트는 `assertSentOnDemand` 메서드를 씁니다:

```
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인수에 클로저를 넣으면 특정 라우팅 주소에 알림이 보냈는지를 확인할 수 있습니다:

```
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

알림 시스템은 알림이 전송 순간에 `Illuminate\Notifications\Events\NotificationSending` 이벤트를 발생시킵니다. 이 이벤트는 알림 대상 엔티티와 알림 인스턴스를 담고 있습니다. 애플리케이션의 `EventServiceProvider`에서 리스너를 등록할 수 있습니다:

```
use App\Listeners\CheckNotificationStatus;
use Illuminate\Notifications\Events\NotificationSending;

/**
 * 이벤트와 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    NotificationSending::class => [
        CheckNotificationStatus::class,
    ],
];
```

리스너의 `handle` 메서드가 `false`를 반환하면 알림 전송을 중지할 수 있습니다:

```
use Illuminate\Notifications\Events\NotificationSending;

/**
 * 이벤트 처리
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

리스너 내에서 `$event->notifiable`, `$event->notification`, `$event->channel` 프로퍼티에 접근해 알림 대상, 알림 객체, 채널 정보를 확인할 수 있습니다:

```
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

알림이 완료되면 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발생합니다. 이 이벤트 역시 알림 대상과 인스턴스를 담고 있으며, `EventServiceProvider`에 리스너를 등록할 수 있습니다:

```
use App\Listeners\LogNotification;
use Illuminate\Notifications\Events\NotificationSent;

/**
 * 이벤트와 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    NotificationSent::class => [
        LogNotification::class,
    ],
];
```

리스너 안에서 `$event->notifiable`, `$event->notification`, `$event->channel`, `$event->response` 프로퍼티를 확인할 수 있습니다:

```
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

> [!NOTE]  
> 리스너를 `EventServiceProvider`에 등록한 후, 빠르게 클래스를 생성하려면 `event:generate` Artisan 명령어를 사용하세요.

<a name="custom-channels"></a>
## 커스텀 채널

Laravel은 기본적으로 몇 가지 알림 채널을 내장하지만, 직접 만든 채널을 통해 다른 방식으로 알림을 보낼 수도 있습니다.

시작하려면, `send` 메서드를 포함한 클래스를 정의하세요. 이 메서드는 `$notifiable`과 `$notification` 두 인수를 받습니다.

`send` 메서드에서 알림 클래스의 필요한 메서드를 호출해 메시지를 받아 채널에 맞게 전송하세요:

```
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 알림을 전송합니다.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable 인스턴스에게 알림 전송...
    }
}
```

이후, 알림 클래스의 `via` 메서드에서 이 채널 클래스를 반환하면 됩니다. 예시에서는 `toVoice` 메서드를 통해 음성 메시지를 생성합니다. 예를 들어 `VoiceMessage` 클래스를 만들어 메시지를 표현할 수 있습니다:

```
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
     * 알림 채널을 반환합니다.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * 음성 알림 표현을 반환합니다.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```