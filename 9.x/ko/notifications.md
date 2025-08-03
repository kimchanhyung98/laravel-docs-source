# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 퍼사드 사용하기](#using-the-notification-facade)
    - [배달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
    - [즉시 알림 보내기](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅하기](#formatting-mail-messages)
    - [보내는 사람 설정하기](#customizing-the-sender)
    - [수신자 설정하기](#customizing-the-recipient)
    - [메일 제목 설정하기](#customizing-the-subject)
    - [메일러 설정하기](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가하기](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [메일러블 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [읽음 표시하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 리스닝하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [쇼트코드 알림 포맷팅](#formatting-shortcode-notifications)
    - ["From" 번호 설정하기](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 첨부파일](#slack-attachments)
    - [Slack 알림 라우팅](#routing-slack-notifications)
- [알림 현지화](#localizing-notifications)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

Laravel은 [이메일 전송](/docs/9.x/mail) 지원 외에도 이메일, SMS(Vonage(전 Nexmo)), [Slack](https://slack.com) 등 다양한 배달 채널을 통한 알림 전송을 지원합니다. 또한, 수십 가지 다른 채널을 위한 [커뮤니티 제작 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 있습니다. 알림은 데이터베이스에 저장하여 웹 인터페이스에 표시할 수도 있습니다.

일반적으로 알림은 간결한 정보성 메시지로, 애플리케이션에서 발생한 일을 사용자에게 알려줍니다. 예를 들어, 청구 애플리케이션에서는 "청구서 결제 완료" 알림을 이메일과 SMS 채널을 통해 사용자에게 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서는 알림 하나가 일반적으로 `app/Notifications` 디렉터리에 저장된 하나의 클래스로 표현됩니다. 이 디렉터리가 없다면 걱정하지 마세요. `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령은 새 알림 클래스를 `app/Notifications` 디렉터리에 생성합니다. 각 알림 클래스는 `via` 메서드와 `toMail`, `toDatabase` 등 특정 채널에 맞는 메시지를 생성하는 여러 메서드를 포함합니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 두 가지 방법으로 보낼 수 있습니다: `Notifiable` 트레이트의 `notify` 메서드를 사용하거나 `Notification` [퍼사드](/docs/9.x/facades)를 사용하는 것입니다. 기본적으로 `Notifiable` 트레이트는 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다:

```
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 여러분의 모델 어디에서든 사용할 수 있으며, 꼭 `User` 모델에만 포함될 필요는 없습니다.

<a name="using-the-notification-facade"></a>
### Notification 퍼사드 사용하기

또는, 여러 알림 대상(예: 여러 사용자 컬렉션)에게 한꺼번에 알림을 보낼 때는 `Notification` [퍼사드](/docs/9.x/facades)를 사용할 수 있습니다. 퍼사드의 `send` 메서드에 모든 알림 대상과 알림 인스턴스를 전달합니다:

```
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드는 `ShouldQueue` 인터페이스를 구현한 알림도 지체 없이 즉시 전송합니다:

```
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 배달 채널 지정하기

각 알림 클래스에는 알림이 어떤 채널로 전달될지 결정하는 `via` 메서드가 있습니다. `mail`, `database`, `broadcast`, `vonage`, `slack` 채널 등으로 알림을 보낼 수 있습니다.

> [!NOTE]
> 텔레그램(Telegram)이나 푸셔(Pusher) 같은 다른 채널을 사용하려면, 커뮤니티에서 만든 [Laravel Notification Channels 사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 받아, 알림을 전달할 채널을 결정할 때 이를 활용할 수 있습니다:

```
/**
 * 알림 배달 채널을 가져옵니다.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function via($notifiable)
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐잉하기

> [!WARNING]
> 알림을 큐에 넣기 전에 큐 구성을 하고 [작업자(worker)](/docs/9.x/queues)를 시작해야 합니다.

알림 전송에는 시간이 걸릴 수 있고, 외부 API 호출이 필요할 수도 있습니다. 이를 최적화하려면 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해 알림을 큐에 넣으세요. `make:notification` 명령어로 생성한 알림은 이미 이 인터페이스와 트레이트를 불러와 바로 사용 가능합니다:

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

`ShouldQueue` 인터페이스가 있는 알림은 일반 알림 호출과 동일하게 보내면, Laravel이 해당 알림을 자동으로 큐에 넣습니다:

```
$user->notify(new InvoicePaid($invoice));
```

큐에 여러 수신자와 여러 채널이 있으면, 수신자-채널 조합마다 별도의 작업이 큐에 생성됩니다. 예를 들어, 3명의 수신자와 2개의 채널이라면 6개의 작업이 큐에 큐잉됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연하기

알림 전송을 지연시키려면 알림 객체 생성 시 `delay` 메서드를 체인하세요:

```
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

<a name="delaying-notifications-per-channel"></a>
#### 채널별 알림 지연 설정

채널별로 다른 지연 시간을 지정하려면 `delay`에 배열을 전달하세요:

```
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스에 `withDelay` 메서드를 정의해 채널과 지연 시간을 배열로 반환하도록 할 수도 있습니다:

```
/**
 * 알림 배달 지연 시간을 결정합니다.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function withDelay($notifiable)
{
    return [
        'mail' => now()->addMinutes(5),
        'sms' => now()->addMinutes(10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 연결 설정하기

기본적으로 큐에 넣는 알림은 애플리케이션 기본 큐 연결을 사용합니다. 특정 알림에서 다른 큐 연결을 쓰려면 알림 클래스에 `$connection` 속성을 정의하세요:

```
/**
 * 알림 큐잉 시 사용할 큐 연결 이름입니다.
 *
 * @var string
 */
public $connection = 'redis';
```

또는 `viaConnections` 메서드를 정의해 채널별 큐 연결을 지정할 수도 있습니다:

```
/**
 * 각 알림 채널이 사용할 큐 연결을 결정합니다.
 *
 * @return array
 */
public function viaConnections()
{
    return [
        'mail' => 'redis',
        'database' => 'sync',
    ];
}
```

<a name="customizing-notification-channel-queues"></a>
#### 알림 채널별 큐 이름 설정하기

채널별 사용할 구체적인 큐 이름을 지정하려면 `viaQueues` 메서드를 정의하세요:

```
/**
 * 각 알림 채널이 사용할 큐 이름을 결정합니다.
 *
 * @return array
 */
public function viaQueues()
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 큐 알림과 데이터베이스 트랜잭션

트랜잭션 내에서 큐 알림을 보내면, 큐의 작업이 아직 커밋되지 않은 데이터베이스 데이터에 접근할 수 있습니다. 이로 인해 알림 실행 시 데이터가 반영되지 않아 예기치 않은 문제가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 때, 알림이 트랜잭션 커밋 후에 보내지도록 하고 싶다면 `afterCommit` 메서드를 호출해 전송하세요:

```
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 생성자에서 호출할 수도 있습니다:

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
     * 새 알림 인스턴스 생성
     *
     * @return void
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이 문제 해결에 관련된 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/9.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림 발송 여부 결정하기

큐 작업으로 알림이 처리될 때, 알림 전송 여부를 동적으로 결정하려면 알림 클래스에 `shouldSend` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 알림은 발송되지 않습니다:

```
/**
 * 알림을 보낼지 결정합니다.
 *
 * @param  mixed  $notifiable
 * @param  string  $channel
 * @return bool
 */
public function shouldSend($notifiable, $channel)
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 즉시 알림 보내기 (On-Demand Notifications)

때로는 애플리케이션 사용자로 등록되지 않은 누군가에게 알림을 보내야 할 때가 있습니다. 이럴 때는 `Notification` 퍼사드의 `route` 메서드를 사용해 임시 라우팅 정보를 지정할 수 있습니다:

```
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
            ->route('vonage', '5555555555')
            ->route('slack', 'https://hooks.slack.com/services/...')
            ->route('broadcast', [new Channel('channel-name')])
            ->notify(new InvoicePaid($invoice));
```

메일 수신자의 이름을 함께 지정하려면, 이메일 주소를 키로 하고 이름을 값으로 하는 배열을 첫 번째 인수로 전달하세요:

```
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅하기

알림이 이메일로 전송될 경우, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 객체를 받고, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 간단한 트랜잭션 메일 메시지 작성을 도와주는 메서드를 제공합니다. 메시지는 텍스트 줄(line)과 "콜 투 액션" 버튼(action) 등을 포함할 수 있습니다. 아래는 `toMail` 메서드 예제입니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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
> 예제에서 `toMail` 메서드가 `$this->invoice->id`를 사용하는데, 생성자 등에 필요한 데이터를 전달할 수 있습니다.

위 예제에서는 인사말, 텍스트 줄, 콜 투 액션 버튼, 마지막 텍스트 줄을 차례로 명시했습니다. `MailMessage`가 제공하는 메서드를 통해 쉽게 작고 간단한 트랜잭션성 이메일을 빠르게 생성할 수 있습니다. 메일 채널은 이 내용을 아름답고 반응형인 HTML 템플릿과 일반 텍스트 버전으로 변환합니다. 다음은 `mail` 채널로 전송된 예시 이메일 이미지입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때 `config/app.php` 파일에 `name` 구성 옵션을 설정하세요. 이 값이 메일 알림 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 오류 메시지

결제 실패 같은 오류 알림을 보낼 때는, `error` 메서드를 호출해 오류 상태임을 표시할 수 있습니다. 이 경우 콜 투 액션 버튼이 검정 대신 빨간색으로 표시됩니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->error()
                ->subject('Invoice Payment Failed')
                ->line('...');
}
```

<a name="other-mail-notification-formatting-options"></a>
#### 그 외 메일 알림 포맷팅 옵션

텍스트 줄을 `line` 메서드 대신 커스텀 뷰 템플릿으로 렌더링하려면 `view` 메서드를 사용하세요:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)->view(
        'emails.name', ['invoice' => $this->invoice]
    );
}
```

일반 텍스트 전용 뷰는 다음과 같이 두 번째 인수에 배열로 전달할 수 있습니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)->view(
        ['emails.name.html', 'emails.name.plain'],
        ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 보내는 사람 설정하기

기본적으로 메일의 보내는 사람 주소(from)는 `config/mail.php` 설정 파일에 정의되어 있지만, 특정 알림별로 `from` 메서드를 호출해 지정할 수도 있습니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->from('barrett@example.com', 'Barrett Blair')
                ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 설정하기

메일 채널을 통해 알림을 보낼 때, 알림 대상 모델에서 기본적으로 `email` 속성을 찾아 이메일 주소로 사용합니다. 다른 이메일 주소를 쓰려면 모델에 `routeNotificationForMail` 메서드를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * 메일 채널 알림 라우팅
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return array|string
     */
    public function routeNotificationForMail($notification)
    {
        // 이메일 주소만 반환...
        return $this->email_address;

        // 이메일 주소와 이름 반환...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 메일 제목 설정하기

메일 제목은 기본적으로 알림 클래스명(PascalCase)을 "Title Case"로 변환된 문자열이 사용됩니다. 예: `InvoicePaid` → `Invoice Paid`. 다른 제목을 지정하려면 메시지 생성 시 `subject` 메서드를 호출하세요:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 설정하기

메일 알림은 기본적으로 `config/mail.php`에 정의된 기본 메일러를 사용합니다. 다른 메일러를 사용하려면 메시지 생성 시 `mailer` 메서드에 메일러 이름을 전달하세요:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->mailer('postmark')
                ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 커스터마이징

메일 알림 템플릿을 변경하려면 알림 패키지의 리소스를 게시하세요. 게시 후 `resources/views/vendor/notifications` 에 템플릿이 위치합니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 `attach` 메서드를 호출하고 첫 번째 인수로 절대 경로를 전달합니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file');
}
```

> [!NOTE]
> `attach` 메서드는 [첨부 객체](/docs/9.x/mail#attachable-objects)도 지원합니다. 자세한 내용은 해당 문서를 참고하세요.

첨부파일에 표시 이름(`as`)이나 MIME 타입(`mime`)을 지정하려면 두 번째 인수에 배열을 전달하세요:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file', [
                    'as' => 'name.pdf',
                    'mime' => 'application/pdf',
                ]);
}
```

`attachFromStorage` 메서드를 이용해 직접 스토리지 디스크에서 파일을 첨부할 수는 없습니다. 스토리지 경로의 절대 경로를 `attach` 메서드에 전달하거나, `toMail`에서 [mailable](/docs/9.x/mail#generating-mailables)을 반환하는 방식을 권장합니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return Mailable
 */
public function toMail($notifiable)
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email)
                ->attachFromStorage('/path/to/file');
}
```

여러 파일을 첨부하려면 `attachMany` 메서드를 사용하세요:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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
#### 문자열 데이터 첨부하기

`attachData` 메서드로 바이트 문자열을 첨부파일로 추가할 수도 있습니다. 이때 파일명도 지정해야 합니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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

Mailgun, Postmark 같은 이메일 공급자는 메시지에 태그(tag)와 메타데이터(metadata)를 첨부해 이메일 그룹화나 추적에 활용할 수 있습니다. `tag`와 `metadata` 메서드로 추가할 수 있습니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Comment Upvoted!')
                ->tag('upvote')
                ->metadata('comment_id', $this->comment->id);
}
```

Mailgun 드라이버를 사용하는 경우 [Mailgun 태그 및 메타데이터 문서](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1)와 [Postmark 문서](https://postmarkapp.com/blog/tags-support-for-smtp)를 참고하세요. Amazon SES 사용 시에는 `metadata` 메서드로 [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage`의 `withSymfonyMessage` 메서드에 클로저를 전달하면 메일 전송 전에 Symfony `Email` 메시지를 직접 수정할 수 있습니다. 예를 들어, 커스텀 헤더를 추가할 수 있습니다:

```
use Symfony\Component\Mime\Email;

/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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
### 메일러블 사용하기

필요하다면 알림 클래스의 `toMail`에서 [mailable 객체](/docs/9.x/mail)를 반환할 수도 있습니다. 이 경우 `to` 메서드로 수신자 이메일을 지정해야 합니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return Mailable
 */
public function toMail($notifiable)
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### 메일러블과 즉시 알림

즉시 알림을 보낼 땐, `toMail`에 전달되는 `$notifiable`이 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스일 수 있습니다. 이 객체의 `routeNotificationFor('mail')` 메서드로 이메일 주소를 가져올 수 있습니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;

/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return Mailable
 */
public function toMail($notifiable)
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

메일 알림 템플릿을 설계할 때, 실제 전송하지 않고도 브라우저에서 미리보는 것이 편리할 수 있습니다. Laravel은 알림의 메일 메시지를 직접 라우트 클로저나 컨트롤러에서 반환하면 이를 렌더링해 보여줍니다:

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
## Markdown 메일 알림

Markdown 메일 알림은 Laravel이 미리 제공하는 메일 템플릿을 사용하면서도, 더 자유롭게 긴 메시지를 작성할 수 있습니다. Markdown으로 작성하면 Laravel이 반응형 HTML과 평문 버전을 자동 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

`make:notification` 명령어에 `--markdown` 옵션을 사용해 Markdown 템플릿 알림을 생성할 수 있습니다:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

Markdown을 사용하는 알림 클래스 역시 `toMail` 메서드를 정의하는데, `line`과 `action` 대신 `markdown` 메서드로 템플릿 이름과 데이터를 넘깁니다:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="writing-the-message"></a>
### 메시지 작성하기

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법을 조합해 쉽게 작성하며, Laravel이 미리 만든 UI 컴포넌트를 활용합니다:

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

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url` 필수 및 `color` 옵션을 지원하며, `primary`, `green`, `red` 색상을 지정할 수 있습니다. 여러 버튼도 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주위와 약간 다른 배경색 영역에 텍스트를 감싸, 강조하고 싶은 부분을 표시할 때 사용합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

Markdown 테이블을 HTML 테이블로 변환하여 출력합니다. 마크다운 표 기본 정렬 문법도 지원합니다:

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

모든 Markdown 컴포넌트를 애플리케이션 내로 복사해 수정하려면 `vendor:publish` 명령어로 `laravel-mail` 태그를 지정해 게시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

게시하면 `resources/views/vendor/mail` 디렉터리에 컴포넌트가 복사됩니다. 필요한 대로 커스터마이징할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

게시된 컴포넌트 중 `resources/views/vendor/mail/html/themes` 디렉터리 내 `default.css` 파일을 수정해 스타일을 변경할 수 있습니다. HTML 이메일의 인라인 스타일에 반영됩니다.

전혀 새로운 테마를 만들려면 `html/themes` 폴더에 CSS 파일을 추가한 뒤 `config/mail.php` 의 `theme` 옵션을 새 테마 이름으로 변경하세요.

알림별 프로그래밍적으로 테마를 지정하려면 `toMail` 내에서 `theme` 메서드를 호출해 테마명을 전달하세요:

```
/**
 * 알림의 메일 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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

`database` 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 테이블에는 알림 유형과 알림 내용을 나타내는 JSON 데이터가 포함됩니다.

애플리케이션 UI에서 알림을 표시하려면 먼저 알림 저장용 테이블을 생성해야 합니다. `notifications:table` 명령어로 마이그레이션을 만들고, `migrate` 명령으로 테이블을 생성하세요:

```shell
php artisan notifications:table

php artisan migrate
```

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

데이터베이스에 알림을 저장하려면 `toDatabase` 또는 `toArray` 메서드를 알림 클래스에 정의하세요. 이 메서드는 `$notifiable` 인스턴스를 받고, 직렬화 가능한 평범한 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 예제 `toArray` 메서드를 봅시다:

```
/**
 * 알림의 배열 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function toArray($notifiable)
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs `toArray`

`toArray` 메서드는 `broadcast` 채널 데이터 전송에도 사용됩니다. 데이터베이스용과 브로드캐스트용 배열 표현을 별도로 관리하고 싶다면 `toDatabase` 메서드를 정의하세요.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

데이터베이스에 저장된 알림은 알림 대상 모델의 `Illuminate\Notifications\Notifiable` 트레이트에 정의된 `notifications` [Eloquent 연관관계](/docs/9.x/eloquent-relationships)로 접근할 수 있습니다. 기본적으로 최신 생성일 순으로 정렬됩니다:

```
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은 알림만 가져오려면 `unreadNotifications` 관계를 사용하세요. 역시 최신순입니다:

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림을 조회하려면, 알림 대상(예: 현재 사용자)의 알림을 반환하는 컨트롤러를 정의하고, 해당 컨트롤러 URL로 HTTP 요청을 해야 합니다.

<a name="marking-notifications-as-read"></a>
### 읽음 표시하기

사용자가 알림을 확인하면 일반적으로 읽음 처리합니다. `Notifiable` 트레이트는 알림 데이터베이스 레코드의 `read_at` 컬럼을 업데이트하는 `markAsRead` 메서드를 제공합니다:

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

각 알림을 반복하지 않고 컬렉션에 대해 한꺼번에 호출할 수도 있습니다:

```
$user->unreadNotifications->markAsRead();
```

또한 DB 직접 업데이트로 읽음 처리도 가능합니다:

```
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

데이터베이스에서 알림을 완전히 삭제하려면 `delete` 메서드를 사용하세요:

```
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림 전송 전에는 Laravel [이벤트 방송](/docs/9.x/broadcasting) 설정과 동작을 익혀야 합니다. 이 기능은 서버사이드 Laravel 이벤트를 자바스크립트 프런트엔드에서 실시간으로 받아 처리할 수 있게 해줍니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel의 이벤트 방송 시스템을 활용해 자바스크립트 프런트엔드로 알림을 실시간 전달합니다. 브로드캐스트를 지원하려면 `toBroadcast` 메서드를 알림 클래스에 정의하세요. 이 메서드는 `$notifiable`을 받고 `BroadcastMessage` 인스턴스를 반환해야 합니다. 존재하지 않으면 `toArray` 결과가 대신 사용됩니다. 예제:

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트 가능한 알림 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return BroadcastMessage
 */
public function toBroadcast($notifiable)
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```

<a name="broadcast-queue-configuration"></a>
#### 브로드캐스트 큐 설정

브로드캐스트 알림 전송도 큐 작업으로 처리됩니다. 큐 연결과 큐 이름을 설정하려면 `BroadcastMessage` 인스턴스의 `onConnection`, `onQueue` 메서드를 호출하세요:

```
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

기본적으로 브로드캐스트 데이터에는 알림 클래스의 전체 네임스페이스명이 `type` 필드로 포함됩니다. 이를 변경하려면 `broadcastType` 메서드를 정의하세요:

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트되는 알림의 타입을 반환합니다.
 *
 * @return string
 */
public function broadcastType()
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 리스닝하기

알림은 `{notifiable}.{id}` 형식의 프라이빗 채널로 브로드캐스트됩니다. 예를 들어, `App\Models\User` ID 1에게 보내는 알림은 `App.Models.User.1` 채널에 방송됩니다. [Laravel Echo](/docs/9.x/broadcasting#client-side-installation)에서는 다음처럼 `notification` 메서드를 통해 쉽게 받아볼 수 있습니다:

```
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 브로드캐스트 채널 커스터마이징

알림 대상 엔티티에서 브로드캐스트 채널 이름을 직접 지정하려면 `receivesBroadcastNotificationsOn` 메서드를 정의하세요:

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
     * 사용자가 알림을 받을 방송 채널을 반환합니다.
     *
     * @return string
     */
    public function receivesBroadcastNotificationsOn()
    {
        return 'users.'.$this->id;
    }
}
```

<a name="sms-notifications"></a>
## SMS 알림

<a name="sms-prerequisites"></a>
### 사전 준비

Laravel의 SMS 알림은 [Vonage](https://www.vonage.com/) (전 Nexmo)를 통해 제공합니다. Vonage 알림을 보내려면 `laravel/vonage-notification-channel` 와 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

패키지는 설정 파일도 제공합니다. 직접 내보낼 필요는 없으며, 환경 변수 `VONAGE_KEY`, `VONAGE_SECRET`에 API 키를 설정하면 됩니다.

기본 발신번호는 `VONAGE_SMS_FROM` 환경 변수로 지정하세요. 이 번호는 Vonage 대시보드에서 생성할 수 있습니다:

```
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

SMS 전송을 지원하는 알림은 `toVonage` 메서드를 정의해야 하며, 이 메서드는 `$notifiable`을 받고 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```
/**
 * Vonage / SMS 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 문자 메시지

메시지에 유니코드 문자가 포함된다면 `unicode` 메서드를 호출하세요:

```
/**
 * Vonage / SMS 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->content('Your unicode message')
                ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### "From" 번호 설정하기

`VONAGE_SMS_FROM`에 설정된 기본 발신번호와 다른 번호를 사용하려면 `from` 메서드를 호출하세요:

```
/**
 * Vonage / SMS 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->content('Your SMS message content')
                ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가하기

사용자나 팀별 비용 집계를 위해 클라이언트 참조 ID를 추가할 수 있습니다. Vonage는 이 참조를 보고서에 활용할 수 있으며, 40자 이내 문자열이면 됩니다:

```
/**
 * Vonage / SMS 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

Vonage 알림을 올바른 번호로 보내려면 모델에 `routeNotificationForVonage` 메서드를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Vonage 채널 알림 라우팅
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return string
     */
    public function routeNotificationForVonage($notification)
    {
        return $this->phone_number;
    }
}
```

<a name="slack-notifications"></a>
## Slack 알림

<a name="slack-prerequisites"></a>
### 사전 준비

Slack 알림을 보내려면 다음 명령어로 Slack 알림 채널 패키지를 설치하세요:

```shell
composer require laravel/slack-notification-channel
```

Slack 팀용 [Slack App](https://api.slack.com/apps?new_app=1)을 생성한 뒤, "Incoming Webhook"을 설정하면 웹훅 URL을 얻을 수 있습니다. 이를 알림 라우팅에 사용합니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 알림을 지원하려면 알림 클래스에 `toSlack` 메서드를 정의하세요. 이 메서드는 `$notifiable`을 받고 `Illuminate\Notifications\Messages\SlackMessage` 인스턴스를 반환해야 합니다. Slack 메시지는 텍스트 내용과 추가 포맷이 가능한 "첨부파일(attachments)"을 포함할 수 있습니다. 기본 예제:

```
/**
 * Slack 알림 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\SlackMessage
 */
public function toSlack($notifiable)
{
    return (new SlackMessage)
                ->content('One of your invoices has been paid!');
}
```

<a name="slack-attachments"></a>
### Slack 첨부파일

Slack 메시지에 첨부파일을 추가해 풍부한 포맷을 할 수 있습니다. 예를 들어 애플리케이션 예외 알림을 에러 상태로 보내면서, 예외 세부내역 링크를 첨부할 수 있습니다:

```
/**
 * Slack 알림 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\SlackMessage
 */
public function toSlack($notifiable)
{
    $url = url('/exceptions/'.$this->exception->id);

    return (new SlackMessage)
                ->error()
                ->content('Whoops! Something went wrong.')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Exception: File Not Found', $url)
                               ->content('File [background.jpg] was not found.');
                });
}
```

첨부파일은 표 형식으로 여러 필드를 배열로 지정할 수도 있습니다:

```
/**
 * Slack 알림 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return SlackMessage
 */
public function toSlack($notifiable)
{
    $url = url('/invoices/'.$this->invoice->id);

    return (new SlackMessage)
                ->success()
                ->content('One of your invoices has been paid!')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Invoice 1322', $url)
                               ->fields([
                                    'Title' => 'Server Expenses',
                                    'Amount' => '$1,234',
                                    'Via' => 'American Express',
                                    'Was Overdue' => ':-1:',
                                ]);
                });
}
```

<a name="markdown-attachment-content"></a>
#### Markdown 첨부파일 내용

첨부 필드에 Markdown 문법이 포함되면 `markdown` 메서드로 해당 필드를 지정해 Slack이 파싱하게 할 수 있습니다. 지원되는 필드는 `pretext`, `text`, `fields`입니다. 자세한 내용은 [Slack API 문서](https://api.slack.com/docs/message-formatting#message_formatting)를 참고하세요:

```
/**
 * Slack 알림 표현을 반환합니다.
 *
 * @param  mixed  $notifiable
 * @return SlackMessage
 */
public function toSlack($notifiable)
{
    $url = url('/exceptions/'.$this->exception->id);

    return (new SlackMessage)
                ->error()
                ->content('Whoops! Something went wrong.')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Exception: File Not Found', $url)
                               ->content('File [background.jpg] was *not found*.')
                               ->markdown(['text']);
                });
}
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 특정 팀과 채널로 라우팅하려면 알림 대상 모델에 `routeNotificationForSlack` 메서드를 정의하고, Slack Incoming Webhook URL을 반환하세요:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Slack 채널 알림 라우팅
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return string
     */
    public function routeNotificationForSlack($notification)
    {
        return 'https://hooks.slack.com/services/...';
    }
}
```

<a name="localizing-notifications"></a>
## 알림 현지화

Laravel은 HTTP 요청의 현재 로케일과 다른 언어로 알림을 보낼 수 있으며, 큐잉된 알림도 이 로케일을 기억합니다.

알림 인스턴스에 `locale` 메서드로 언어를 지정하세요. 알림 평가 시 애플리케이션 로케일이 잠시 바뀌었다가 다시 복원됩니다:

```
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

`Notification` 퍼사드를 통한 다수 알림도 다음처럼 가능합니다:

```
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 언어

사용자의 선호 로케일을 애플리케이션에 저장했다면, 알림 대상 모델에서 `HasLocalePreference` 계약을 구현해 Laravel이 자동으로 이를 사용하도록 할 수 있습니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일을 반환합니다.
     *
     * @return string
     */
    public function preferredLocale()
    {
        return $this->locale;
    }
}
```

인터페이스 구현 후에는 `locale` 메서드 호출 없이도 기본 선호 로케일로 알림이 전송됩니다:

```
$user->notify(new InvoicePaid($invoice));
```

<a name="notification-events"></a>
## 알림 이벤트

<a name="notification-sending-event"></a>
#### 알림 전송 중 이벤트

알림 전송 시 `Illuminate\Notifications\Events\NotificationSending` [이벤트](/docs/9.x/events)가 발행됩니다. 이 이벤트는 알림 대상과 알림 인스턴스를 포함하며, `EventServiceProvider`에서 리스너를 등록할 수 있습니다:

```
use App\Listeners\CheckNotificationStatus;
use Illuminate\Notifications\Events\NotificationSending;

/**
 * 애플리케이션 이벤트 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    NotificationSending::class => [
        CheckNotificationStatus::class,
    ],
];
```

리스너에서 `handle` 메서드가 `false`를 반환하면 알림 전송이 취소됩니다:

```
use Illuminate\Notifications\Events\NotificationSending;

/**
 * 이벤트 처리
 *
 * @param  \Illuminate\Notifications\Events\NotificationSending  $event
 * @return void
 */
public function handle(NotificationSending $event)
{
    return false;
}
```

리스너 내에서 `$event->notifiable`, `$event->notification`, `$event->channel` 속성에 접근할 수 있습니다:

```
/**
 * 이벤트 처리
 *
 * @param  \Illuminate\Notifications\Events\NotificationSending  $event
 * @return void
 */
public function handle(NotificationSending $event)
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
#### 알림 전송 완료 이벤트

알림 전송 완료 시 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발행됩니다. 이 이벤트도 `EventServiceProvider`에서 리스너를 등록할 수 있습니다:

```
use App\Listeners\LogNotification;
use Illuminate\Notifications\Events\NotificationSent;

/**
 * 이벤트 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    NotificationSent::class => [
        LogNotification::class,
    ],
];
```

> [!NOTE]
> 리스너를 등록한 뒤에는 `event:generate` Artisan 명령을 사용해 리스너 클래스를 빠르게 생성할 수 있습니다.

리스너 내에서 `$event->notifiable`, `$event->notification`, `$event->channel`, `$event->response` 속성에 접근할 수 있습니다:

```
/**
 * 이벤트 처리
 *
 * @param  \Illuminate\Notifications\Events\NotificationSent  $event
 * @return void
 */
public function handle(NotificationSent $event)
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```

<a name="custom-channels"></a>
## 커스텀 채널

Laravel은 여러 기본 알림 채널을 제공합니다. 그러나 직접 다른 알림 채널 드라이버를 작성할 수도 있습니다. 시작하려면 `send` 메서드를 포함하는 클래스를 정의하세요. 이 메서드는 `$notifiable`와 `$notification` 두 인수를 받습니다.

`send` 메서드 내에서 알림 객체에서 채널별 메시지를 가져와, 원하는 방식으로 알림 대상을 호출하면 됩니다:

```
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 주어진 알림을 보냅니다.
     *
     * @param  mixed  $notifiable
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return void
     */
    public function send($notifiable, Notification $notification)
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable 객체에 알림을 전송...
    }
}
```

알림 클래스의 `via` 메서드에 이 채널 클래스를 반환하도록 하면, `toVoice` 메서드에서 음성 메시지 표현 객체를 반환할 수 있습니다. 예를 들어 다음과 같습니다:

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
     *
     * @param  mixed  $notifiable
     * @return array|string
     */
    public function via($notifiable)
    {
        return [VoiceChannel::class];
    }

    /**
     * 음성 알림 메시지 표현을 반환합니다.
     *
     * @param  mixed  $notifiable
     * @return VoiceMessage
     */
    public function toVoice($notifiable)
    {
        // ...
    }
}
```