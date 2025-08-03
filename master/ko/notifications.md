# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 전송하기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 퍼사드 사용하기](#using-the-notification-facade)
    - [전송 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐잉하기](#queueing-notifications)
    - [즉시 알림 전송하기](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그와 메타데이터 추가하기](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [메일러블 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 조회하기](#accessing-the-notifications)
    - [읽음 표시하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [유니코드 콘텐츠](#unicode-content)
    - [발신 번호 변경하기](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
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

Laravel은 [이메일 전송](/docs/master/mail) 지원 외에도 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 명칭 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 뿐만 아니라, 수십 종 이상의 다른 채널을 위한 다양한 [커뮤니티 제작 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 만들어져 있습니다! 알림을 데이터베이스에 저장하여 웹 인터페이스에서 보여줄 수도 있습니다.

보통 알림은 애플리케이션에서 발생한 어떤 일을 사용자에게 간단히 알려주는 짧고 정보성 메시지여야 합니다. 예를 들어, 청구 애플리케이션이라면 이메일과 SMS 채널을 통해 사용자에게 "Invoice Paid" (청구서 결제 완료) 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서는 알림 하나하나가 일반적으로 `app/Notifications` 디렉토리에 저장되는 단일 클래스로 표현됩니다. 해당 디렉토리가 보이지 않는다면 걱정하지 마십시오. `make:notification` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 `app/Notifications` 디렉토리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스는 `via` 메서드와 채널별로 알림 메시지를 변환하는 `toMail`, `toDatabase` 같은 메시지 작성용 메서드를 포함합니다.

<a name="sending-notifications"></a>
## 알림 전송하기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, `Notification` [퍼사드](/docs/master/facades)를 통해 전송할 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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
> `Notifiable` 트레이트는 여러분의 어떤 모델에도 적용할 수 있습니다. 꼭 `User` 모델에만 국한하지 않아도 됩니다.

<a name="using-the-notification-facade"></a>
### Notification 퍼사드 사용하기

또한, `Notification` [퍼사드](/docs/master/facades)를 사용하여 여러 알림 수신자에게 알림을 전송할 수 있습니다. `send` 메서드에 수신자 컬렉션과 알림 인스턴스를 전달하세요:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드는 알림이 `ShouldQueue` 인터페이스를 구현했더라도 즉시 전송합니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정하기

각 알림 클래스는 알림이 어떤 채널로 전송될지 `via` 메서드에서 지정합니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 전송될 수 있습니다.

> [!NOTE]
> 텔레그램이나 푸셔 같은 다른 채널을 사용하고 싶다면 커뮤니티가 운영하는 [Laravel Notification Channels](http://laravel-notification-channels.com) 사이트를 참고하세요.

`via` 메서드는 알림을 받는 객체 `$notifiable` 인스턴스를 인수로 받습니다. 이를 통해 어떤 채널을 사용할지 결정할 수 있습니다:

```php
/**
 * 알림 전송 채널 가져오기.
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
> 알림을 큐잉하기 전에 반드시 큐 설정을 완료하고 [워커 실행](/docs/master/queues#running-the-queue-worker)을 시작해야 합니다.

알림 전송은 특히 외부 API 호출이 포함될 경우 시간이 걸릴 수 있습니다. 앱의 반응 속도를 높이려면 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가하여 알림 전송을 큐에 맡길 수 있습니다. `make:notification` 명령어로 생성된 알림에는 이미 인터페이스와 트레이트가 임포트되어 있으니 바로 추가하세요:

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

`ShouldQueue` 인터페이스가 추가된 알림은 일반 방식대로 전송하면 Laravel이 자동으로 전송 작업을 큐에 추가합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

큐잉 시 수신자 및 채널별로 큐 작업이 생성됩니다. 예를 들어 수신자 3명, 채널 2개라면 총 6개의 작업이 큐에 디스패치됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연하기

전송 지연이 필요하면 알림 인스턴스 생성 시 `delay` 메서드를 체이닝할 수 있습니다:

```php
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 다른 지연 시간을 지정하려면, `delay`에 채널별 시간을 배열 형태로 전달하세요:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

또는 알림 클래스 내에 `withDelay` 메서드를 구현해 채널과 지연 시각 배열을 반환할 수도 있습니다:

```php
/**
 * 알림 채널별 전송 지연 시각 결정.
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
#### 큐 연결 설정 커스터마이징

기본적으로 알림 큐는 앱의 기본 큐 연결을 사용합니다. 특정 알림에 대해 다른 연결을 지정하고 싶다면, 알림 생성자에서 `onConnection` 메서드를 호출하세요:

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
     * 새 알림 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

혹은 알림이 지원하는 각 채널별로 큐 연결을 다르게 지정하려면 `viaConnections` 메서드를 정의하세요. 이 메서드는 채널명과 큐 연결명을 쌍으로 갖는 배열을 반환해야 합니다:

```php
/**
 * 채널별 사용 큐 연결 결정.
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
#### 알림 채널별 큐 설정 지정

채널별로 구체적인 큐 이름을 지정하고 싶으면 `viaQueues` 메서드를 정의하고 채널과 큐 이름을 배열로 반환하세요:

```php
/**
 * 채널별 사용 큐 이름 결정.
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

큐에 쌓인 알림에 [큐 작업용 미들웨어](/docs/master/queues#job-middleware)를 지정할 수도 있습니다. 알림 클래스에 `middleware` 메서드를 정의해 `$notifiable`, `$channel` 인수를 받아 각각의 채널에 맞는 미들웨어 배열을 반환하세요:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 알림 작업이 거치는 미들웨어 반환.
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
#### 큐 알림과 데이터베이스 트랜잭션

트랜잭션 내에서 큐 디스패치된 알림은 트랜잭션 커밋 전 큐에서 처리될 수 있어 모델이나 DB 레코드의 변경 사항이 미반영될 수 있습니다. 트랜잭션 내에 생성된 모델이 DB에 없을 수도 있습니다. 알림 처리 시 예상하지 못한 에러가 발생할 수 있으니 주의하세요.

만약 큐 연결의 `after_commit` 설정이 `false`라면, 알림 전송 시 `afterCommit` 메서드를 호출해 트랜잭션 커밋 후 디스패치하도록 할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또한 알림 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다:

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
     * 새 알림 인스턴스 생성.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 큐 작업과 DB 트랜잭션 관련 문제 회피법은 [큐 문서](/docs/master/queues#jobs-and-database-transactions) 참고 바랍니다.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림의 전송 여부 결정

큐 작업이 처리된 후에도 전송 여부를 결정하고 싶으면 알림 클래스에 `shouldSend` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 해당 알림은 전송되지 않습니다:

```php
/**
 * 알림 전송 여부 결정.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
### 즉시 알림 전송하기

애플리케이션의 사용자로 등록되어 있지 않은 사람에게 알림을 보내야 할 때, `Notification` 퍼사드의 `route` 메서드를 사용해 즉석에서 알림 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일 라우트에 수신자 이름을 같이 지정하려면, 이메일 주소를 키로 이름을 값으로 하는 배열을 첫 번째 요소로 전달하세요:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널에 즉석 라우팅 정보를 동시에 제공하려면 `routes` 메서드를 사용하세요:

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

이메일로 알림을 보낼 경우, 알림 클래스에 `toMail` 메서드를 정의해야 하며, 이 메서드는 `$notifiable` 객체를 인수로 받아야 하고, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 트랜잭션성 이메일 메시지 생성을 돕는 여러 메서드를 포함합니다. 메시지는 텍스트 라인과 '콜 투 액션' 버튼을 포함할 수 있습니다. 다음은 `toMail` 메서드 예시입니다:

```php
/**
 * 알림의 메일 표현 반환.
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
> 예시에서 `$this->invoice->id`를 참조합니다. 메시지 생성에 필요한 데이터를 알림 생성자에 전달하면 됩니다.

이 예시는 인사말, 텍스트 라인, 콜 투 액션, 다시 텍스트 라인을 등록합니다. `MailMessage` 객체의 이 메서드들 덕분에 간단하고 빠르게 이메일 포맷팅이 가능합니다. 메일 채널이 이 컴포넌트들을 아름답고 반응형 HTML 이메일 템플릿과 일반 텍스트 이메일로 변환해 줍니다. 아래는 `mail` 채널이 생성하는 예시 이메일입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때는 `config/app.php` 파일의 `name` 설정 값을 꼭 지정하세요. 이 값이 메일 알림 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 에러 메시지

결제 실패 같은 에러 알림을 보낼 때는 `error` 메서드를 호출해 에러 메시지임을 알릴 수 있습니다. 이 경우 콜 투 액션 버튼이 검정색 대신 빨간색으로 표시됩니다:

```php
/**
 * 알림의 메일 표현 반환.
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

`line` 메서드로 라인을 정의하는 대신, `view` 메서드로 커스텀 템플릿을 지정할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

또한, 텍스트 버전 뷰를 배열의 두 번째 요소로 지정할 수도 있습니다:

```php
/**
 * 알림의 메일 표현 반환.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

단순 텍스트 메시지만 있을 때는 `text` 메서드를 사용할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환.
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

기본 메일 발신자 주소는 `config/mail.php` 설정 파일에 정의되어 있습니다. 하지만 특정 알림에 한해서 `from` 메서드로 발신자 주소와 이름을 직접 지정할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환.
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

`mail` 채널로 알림 전송 시, 알림 시스템은 기본적으로 수신자 객체에 `email` 속성이 있는지 찾습니다. 알림이 전송될 이메일 주소를 직접 지정하고 싶다면, 수신자 모델에 `routeNotificationForMail` 메서드를 구현하세요:

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
     * mail 채널용 알림 라우팅 정보 반환.
     *
     * @return  array<string,string>|string
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
### 제목 커스터마이징

이메일 제목은 기본적으로 알림 클래스명의 제목형식 변환 결과입니다. 예를 들어, 클래스명이 `InvoicePaid`이면 제목은 `Invoice Paid`가 됩니다. 제목을 다르게 지정하려면 메시지 작성 시 `subject` 메서드를 호출하세요:

```php
/**
 * 알림의 메일 표현 반환.
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

이메일 알림은 기본 메일러(`config/mail.php`에 설정된)를 통해 전송됩니다. 특정 알림에서 다른 메일러를 사용하려면, 메시지 작성 시 `mailer` 메서드에 메일러 이름을 지정하세요:

```php
/**
 * 알림의 메일 표현 반환.
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

알림용 HTML 및 텍스트 이메일 템플릿을 직접 수정하려면 알림 패키지 리소스를 퍼블리시할 수 있습니다. 이 명령어 실행 후 `resources/views/vendor/notifications` 디렉토리에 템플릿이 위치합니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 메시지 작성 시 `attach` 메서드를 사용하세요. 첫 번째 인수는 절대 경로입니다:

```php
/**
 * 알림의 메일 표현 반환.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> `attach` 메서드는 [attachable 객체](/docs/master/mail#attachable-objects)도 지원합니다. 자세한 내용은 해당 문서를 참조하세요.

첨부파일의 표시명과 MIME 타입을 지정할 때는 두 번째 인수로 배열을 넘기세요:

```php
/**
 * 알림의 메일 표현 반환.
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

`attachFromStorage` 메서드는 알림에서는 지원하지 않습니다. 스토리지 디스크 내 파일 첨부는 절대 경로를 넘겨주는 `attach` 메서드를 사용하거나, `toMail`에서 [메일러블](/docs/master/mail#generating-mailables)을 반환하는 방식을 사용하세요:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현 반환.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

필요할 경우 `attachMany` 메서드로 여러 첨부파일도 추가할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환.
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

`attachData` 메서드는 바이트 열을 첨부 파일로 추가할 때 사용합니다. 첨부할 파일명도 지정해야 합니다:

```php
/**
 * 알림의 메일 표현 반환.
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

Mailgun, Postmark 등 일부 메일 서비스는 메일 "태그"와 "메타데이터"를 지원해 이메일 추적과 분류에 사용할 수 있습니다. 메일 메시지에 `tag`와 `metadata` 메서드를 통해 태그와 메타데이터를 지정할 수 있습니다:

```php
/**
 * 알림의 메일 표현 반환.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

Mailgun, Postmark, Amazon SES 등 사용 중인 메일 드라이버의 태그 및 메타데이터 기능 사용 방법은 해당 공식 문서를 참고하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

`MailMessage`의 `withSymfonyMessage` 메서드는 Symfony 메시지 객체가 생성되기 전에 클로저를 호출해 깊이 있는 메시지 커스터마이징을 할 수 있게 합니다:

```php
use Symfony\Component\Mime\Email;

/**
 * 알림의 메일 표현 반환.
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
### 메일러블 사용하기

필요하다면 알림 클래스의 `toMail` 메서드에서 완전한 [메일러블 객체](/docs/master/mail)를 반환할 수 있습니다. 이 경우 수신자는 메일러블 객체의 `to` 메서드를 통해 지정해야 합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * 알림의 메일 표현 반환.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### 메일러블과 즉시 알림

즉시 알림을 보내는 경우, `toMail` 메서드의 `$notifiable`는 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스가 되며, 이 객체는 `routeNotificationFor` 메서드로 전송할 이메일 주소를 얻을 수 있습니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * 알림의 메일 표현 반환.
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

메일 알림 템플릿을 만들 때, 실제 이메일로 보내지 않고 브라우저에서 바로 렌더링 결과를 확인하고 싶을 때가 있습니다. 이때는 알림이 생성하는 `MailMessage` 객체를 라우트나 컨트롤러에서 반환하면 브라우저에 렌더링된 이메일이 표시됩니다:

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

마크다운 메일 알림은 기본 이메일 템플릿을 활용하면서도 훨씬 길고 맞춤화된 메시지를 작성할 수 있는 방식입니다. 메시지를 마크다운으로 작성하면 Laravel이 아름답고 반응형 HTML 템플릿과 자동으로 생성되는 일반 텍스트 버전을 만들어 줍니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

마크다운 템플릿을 가지는 알림을 생성하려면 `make:notification` Artisan 명령어의 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

마크다운 템플릿 알림도 `toMail` 메서드를 정의하며, 대신 `line`, `action` 대신 `markdown` 메서드로 마크다운 템플릿 이름과 데이터를 지정합니다:

```php
/**
 * 알림의 메일 표현 반환.
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

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법을 조합해 쉽고 강력하게 알림을 작성할 수 있습니다:

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
> 마크다운 이메일 작성 시 불필요한 들여쓰기를 피하세요. 마크다운 표준에 따라 들여쓰기된 내용은 코드 블록으로 처리됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 속성을 받으며, 지원 색상은 `primary`, `green`, `red`입니다. 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주변과 색이 약간 다른 배경의 박스에 텍스트 블록을 렌더링해 강조할 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 표 문법을 HTML 테이블로 변환합니다. 열 정렬도 기본 마크다운 정렬 문법을 지원합니다:

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

마크다운 알림 컴포넌트를 앱 내부로 내보내어 커스터마이징하려면 `vendor:publish` Artisan 명령어로 `laravel-mail` 자산 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

퍼블리시 후 `resources/views/vendor/mail` 디렉토리 내 `html`과 `text` 디렉토리에 모든 컴포넌트가 위치하므로 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 퍼블리시하면 `resources/views/vendor/mail/html/themes` 디렉토리 내 `default.css` 파일을 확인할 수 있습니다. CSS를 수정하면 자동으로 모든 마크다운 알림의 인라인 스타일에 적용됩니다.

새 테마를 완전히 만들고 싶다면 해당 디렉토리에 CSS 파일을 추가하고, `config/mail.php` 설정의 `theme` 옵션에 테마 이름을 기입하세요.

개별 알림에 대해 테마를 지정하려면 `MailMessage` 빌더 내에서 `theme` 메서드를 호출하세요:

```php
/**
 * 알림의 메일 표현 반환.
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

`database` 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블은 알림 타입과 JSON 형식 알림 데이터를 포함합니다.

사용자 인터페이스에 알림 정보를 표시하려면 테이블이 필요합니다. `make:notifications-table` 커맨드로 적절한 [마이그레이션](/docs/master/migrations)을 생성한 뒤 마이그레이션을 적용하세요:

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 만약 UUID 또는 ULID 같은 기본 키를 사용한다면, 마이그레이션 내의 `morphs` 메서드를 [`uuidMorphs`](/docs/master/migrations#column-method-uuidMorphs) 또는 [`ulidMorphs`](/docs/master/migrations#column-method-ulidMorphs)으로 바꾸세요.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

데이터베이스에 저장될 알림은 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 구현해야 합니다. 이 메서드는 `$notifiable` 객체를 받아 일반 PHP 배열을 반환하며, 이 배열은 `notifications` 테이블의 `data` 컬럼에 JSON으로 저장됩니다. 예를 들어 `toArray` 메서드는 이렇게 작성합니다:

```php
/**
 * 알림을 배열 표현으로 변환.
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

알림이 DB에 저장되면 `type` 컬럼에 알림 클래스명이 저장되고, `read_at` 컬럼은 기본적으로 `null`입니다. 이 동작을 변경하려면, 알림 클래스에 `databaseType` 및 `initialDatabaseReadAtValue` 메서드를 정의할 수 있습니다:

```
use Illuminate\Support\Carbon;
```

```php
/**
 * 알림의 DB 타입 반환.
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * 초기 "read_at" 값 반환.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase`와 `toArray` 차이

`toArray`는 브로드캐스트 채널이 프론트엔드로 전달할 데이터를 결정할 때도 사용됩니다. DB와 브로드캐스트용 데이터가 다르다면 `toArray` 대신 `toDatabase`를 정의하는 것이 좋습니다.

<a name="accessing-the-notifications"></a>
### 알림 조회하기

알림이 DB에 저장되면, 알림을 수신하는 엔티티에서 이를 쉽게 조회할 수 있어야 합니다. 기본 Laravel `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트는 알림을 반환하는 `notifications` [Eloquent 관계](/docs/master/eloquent-relationships)를 제공합니다. 관계 메서드처럼 접근할 수 있으며, 기본적으로 최신 순으로 정렬됩니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은 알림만 조회하려면 `unreadNotifications`를 사용하세요. 이 역시 최신순입니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림에 접근하려면, 해당 알림을 반환하는 컨트롤러를 정의하고 클라이언트에서 이 URL로 HTTP 요청하세요.

<a name="marking-notifications-as-read"></a>
### 읽음 표시하기

사용자가 알림을 확인하면 알림을 '읽음' 상태로 표시하고 싶을 것입니다. `Notifiable` 트레이트는 알림 DB 레코드의 `read_at` 컬럼을 업데이트하는 `markAsRead` 메서드를 제공합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

또한 알림 컬렉션에 직접 `markAsRead`를 호출할 수도 있습니다:

```php
$user->unreadNotifications->markAsRead();
```

DB에서 직접 대량 업데이트할 수도 있습니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 완전히 삭제하려면 `delete`를 호출합니다:

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 사전 준비

브로드캐스트 알림을 사용하려면 Laravel [이벤트 브로드캐스팅](/docs/master/broadcasting) 설정과 작동 방식을 숙지해야 합니다. 이 기능은 서버 측 이벤트를 자바스크립트 프론트엔드에서 실시간으로 반응할 수 있게 합니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel의 이벤트 브로드캐스팅을 통해 알림을 전송합니다. 자바스크립트 프론트엔드에서 실시간 수신이 가능합니다. 브로드캐스트를 지원하는 알림은 `toBroadcast` 메서드를 구현하며, `$notifiable`을 인수로 받아 `BroadcastMessage` 인스턴스를 반환해야 합니다. `toBroadcast`가 없으면 `toArray`가 대체로 사용됩니다. 다음은 `toBroadcast` 예시입니다:

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트용 알림 표현 반환.
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

브로드캐스트 알림은 모두 큐에 추가됩니다. 큐 연결과 큐 이름을 지정하려면 `BroadcastMessage`의 `onConnection`과 `onQueue` 메서드를 호출하세요:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

브로드캐스트 시 기본으로 알림 타입 필드에는 알림 클래스명이 포함됩니다. 타입을 변경하려면 알림 클래스에 `broadcastType` 메서드를 정의하세요:

```php
/**
 * 브로드캐스트할 알림 타입 반환.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 대기

알림은 `{notifiable}.{id}` 형식 이름의 프라이빗 채널로 브로드캐스트됩니다. 예를 들어 `App\Models\User` ID가 1인 사용자의 경우 `App.Models.User.1` 프라이빗 채널입니다. Laravel Echo를 사용할 때는 `notification` 메서드로 쉽게 수신을 대기할 수 있습니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이징

알림 수신자의 브로드캐스트 채널을 변경하려면 수신자 모델에 `receivesBroadcastNotificationsOn` 메서드를 구현하세요:

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
     * 알림 브로드캐스트 채널 반환.
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

Laravel의 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 명 Nexmo)를 사용합니다. Vonage 채널을 쓰려면 다음 패키지를 설치해야 합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

설정 파일도 있지만 직접 퍼블리시하지 않아도 되며, `.env` 파일의 `VONAGE_KEY`와 `VONAGE_SECRET` 환경 변수를 통해 공개 키와 비밀 키를 지정합니다.

또한 기본 발신 번호를 지정하려면 `VONAGE_SMS_FROM` 환경 변수를 설정하세요. 발신 번호는 Vonage 대시보드에서 생성할 수 있습니다:

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

SMS 지원 알림은 `toVonage` 메서드를 구현해야 하며 `$notifiable`을 인수로 받아 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현 반환.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 콘텐츠

문자에 유니코드가 포함된다면 `VonageMessage` 작성 시 `unicode` 메서드를 호출해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현 반환.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### 발신 번호 변경하기

기본 발신 번호(`VONAGE_SMS_FROM`) 대신 특정 번호로 전송하려면 `from` 메서드를 호출하세요:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현 반환.
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

사용자, 팀, 클라이언트별 비용 추적이 필요하면 "클라이언트 참조" 문자열(최대 40자)을 추가할 수 있습니다. 이 정보는 Vonage 리포트에서 사용됩니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Vonage / SMS 알림 표현 반환.
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

적절한 전화번호로 Vonage 알림을 보내려면 수신자 모델에 `routeNotificationForVonage` 메서드를 정의하세요:

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
     * Vonage 채널용 알림 라우팅.
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

Slack 알림을 보내려면 Slack 알림 채널 패키지를 설치하세요:

```shell
composer require laravel/slack-notification-channel
```

Slack 워크스페이스에 [Slack App](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

App이 속한 워크스페이스만 알림을 보낼 경우, App에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한이 있어야 합니다. App이 Slack 봇으로 메시지를 보내려면 `chat:write:bot` 권한도 필요합니다. 권한은 Slack의 "OAuth & Permissions" 탭에서 설정 가능합니다.

App의 "Bot User OAuth Token"을 복사해 `config/services.php` 내 `slack` 설정 배열에 추가하세요. 토큰은 Slack의 "OAuth & Permissions" 탭에서 확인할 수 있습니다:

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

앱이 유저 소유의 외부 Slack 워크스페이스에 알림을 보낼 경우 Slack에서 앱을 배포(distribute)해야 합니다. 배포는 Slack 앱의 "Manage Distribution" 탭에서 처리할 수 있습니다. 배포 후에는 Socialite 통해 사용자 대신 Slack 봇 토큰을 받을 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 메시지 전송 지원 시 알림 클래스에 `toSlack` 메서드를 구현하세요. `$notifiable` 인수를 받으며, `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. Slack의 [Block Kit API](https://api.slack.com/block-kit)를 사용해 풍부한 메시지를 만들 수 있습니다. 아래 예제는 [Slack Block Kit Builder](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리 볼 수 있습니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현 반환.
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

부드러운 빌더 메서드 대신 Slack Block Kit Builder가 만든 순수 JSON payload를 `usingBlockKitTemplate` 메서드에 넘겨 사용할 수 있습니다:

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Slack 알림 표현 반환.
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

Slack Block Kit 알림 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling) 기능을 제공합니다. 이를 사용하려면 Slack 앱에서 "Interactivity"를 활성화하고, 앱이 제공하는 "Request URL"을 Laravel 애플리케이션 내 URL로 지정해야 합니다. 이 설정은 Slack 앱 관리의 "Interactivity & Shortcuts" 탭에서 조절할 수 있습니다.

아래 예제는 `actionsBlock` 메서드를 사용한 것으로, Slack이 버튼 클릭 시 요청 URL로 `POST`를 보내며 클릭한 유저와 버튼 ID 등의 정보를 전달합니다. 앱은 이를 받아 작업을 수행하고, Slack으로부터 온 요청임을 반드시 [검증](https://api.slack.com/authentication/verifying-requests-from-slack)해야 합니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현 반환.
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

            // ID를 직접 지정...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달

사용자가 버튼 클릭 시 확인 메시지를 표시하려면 버튼 정의 시 `confirm` 메서드를 호출하세요. `confirm`은 메시지와 `ConfirmObject` 인스턴스를 인수로 받는 클로저를 전달받습니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Slack 알림 표현 반환.
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

작성한 블록을 확인하고 싶으면 `SlackMessage` 인스턴스에서 `dd` 메서드를 호출하세요. Slack의 [Block Kit Builder](https://app.slack.com/block-kit-builder/) URL을 생성해 브라우저에 미리보기가 표시됩니다. `dd(true)`로 호출하면 원본 payload를 출력합니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

알림이 올바른 Slack 팀과 채널로 가도록 하려면, 수신자 모델에 `routeNotificationForSlack` 메서드를 정의하세요. 이 메서드는 다음 중 하나를 반환할 수 있습니다:

- `null` — 알림 내 기본 채널 설정을 사용합니다. 알림 내 `SlackMessage`의 `to` 메서드 활용 가능.
- 문자열 — Slack 채널명, 예: `#support-channel`
- `SlackRoute` 인스턴스 — Slack 채널명과 OAuth 토큰을 모두 지정하며, 외부 워크스페이스에 보낼 때 사용.

예를 들어 다음처럼 `#support-channel`을 반환하면 앱 설정된 봇 토큰으로 해당 채널에 메시지가 전송됩니다:

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
     * Slack 채널 알림 라우팅 반환.
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
> 외부 워크스페이스에 알림을 보내려면 Slack 앱이 [배포](#slack-app-distribution)되어 있어야 합니다.

다른 워크스페이스에 알림을 보내려면 사용자의 Slack OAuth 토큰을 얻어야 합니다. Laravel Socialite의 Slack 드라이버를 사용해 Slack 인증 후 봇 토큰을 획득 가능하며, 획득한 토큰과 채널 정보를 DB에 저장하세요.

`SlackRoute::make` 메서드를 활용해 사용자 워크스페이스로 라우팅할 수 있습니다. 보통 사용자가 채널을 직접 지정할 UI를 제공해야 합니다:

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
     * Slack 채널 알림 라우팅 반환.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 로컬라이징

Laravel은 HTTP 요청의 현재 로케일과 다른 언어로 알림을 보낼 수 있으며, 큐잉된 알림도 이 로케일 설정을 기억합니다.

`Illuminate\Notifications\Notification` 클래스의 `locale` 메서드로 원하는 언어를 지정할 수 있습니다. 알림 평가 시 앱 로케일이 변경되었다가 평가 완료 후 이전 로케일로 복구됩니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

`Notification` 퍼사드로도 다수 수신자 대상 다국어 알림 보내기가 가능합니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

앱이 사용자별 선호 언어를 저장한다면, `HasLocalePreference` 계약을 구현해 Laravel이 자동으로 해당 로케일을 사용하도록 할 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자가 선호하는 로케일 반환.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

계약을 구현하면 별도로 `locale` 메서드를 호출하지 않아도 해당 로케일로 알림을 보냅니다:

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트

`Notification` 퍼사드의 `fake` 메서드는 실제 알림 전송을 막고 테스트 시 알림이 전송됐는지만 확인할 때 유용합니다. 보통 알림 전송은 테스트하는 주요 비즈니스 로직과 직접 관련이 없으므로, 알림 전송 여부만 검증하면 됩니다:

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // 주문 발송 처리...

    // 알림이 전혀 전송되지 않았는지 확인...
    Notification::assertNothingSent();

    // 특정 사용자들에게 알림 전송 여부 확인...
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // 특정 알림 전송 안 됐는지 확인...
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // 알림 전송 횟수 확인...
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

        // 주문 발송 처리...

        // 알림이 전혀 전송되지 않았는지 확인...
        Notification::assertNothingSent();

        // 특정 사용자들에게 알림 전송 여부 확인...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 특정 알림 전송 안 됐는지 확인...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 알림 전송 횟수 확인...
        Notification::assertCount(3);
    }
}
```

`assertSentTo`나 `assertNotSentTo`에 클로저를 전달해 조건에 맞는 알림을 검사할 수 있습니다. 조건에 맞는 알림이 하나라도 있으면 성공합니다:

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 즉시 알림 테스트

즉시 알림을 보내는 코드에 대해서는 `assertSentOnDemand` 메서드를 쓸 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인자로 클로저를 넘겨 특정 주소로 온 즉시 알림인지 검증할 수 있습니다:

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

알림 전송 직전에 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 디스패치됩니다. 이 이벤트는 "notifiable" 엔티티와 알림 인스턴스를 포함하며, 앱 내에 이벤트 리스너를 만들어 처리할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * 이벤트 처리.
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

리스너에서 `handle`이 `false`를 반환하면 알림 전송이 중단됩니다:

```php
/**
 * 이벤트 처리.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

리스너는 이벤트의 `notifiable`, `notification`, `channel` 프로퍼티에 접근 가능해 알림 수신자, 알림 객체, 채널 정보를 알 수 있습니다:

```php
/**
 * 이벤트 처리.
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

알림이 전송된 후 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발행됩니다. `notifiable`, `notification` 외에 `channel`, `response` 정보도 포함합니다. 이벤트 리스너를 작성해 처리할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * 이벤트 처리.
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

리스너 내에서 다음 프로퍼티를 사용할 수 있습니다:

```php
/**
 * 이벤트 처리.
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

Laravel은 기본적으로 몇몇 알림 채널을 제공합니다만, 자신만의 채널도 만들 수 있습니다. 방법은 간단합니다: `send` 메서드를 가진 클래스를 만들고, 이 메서드가 `$notifiable`과 `$notification` 인수를 받도록 구현하세요.

`send` 메서드 내에서 알림에서 채널에 맞는 메시지를 얻어 직접 알림을 전송하면 됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 주어진 알림 전송.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable에게 음성 알림 전송...
    }
}
```

정의한 채널 클래스 이름을 알림의 `via` 메서드 반환값으로 지정하면 Laravel이 해당 클래스를 채널로 인식합니다.

알림 클래스에서는 `toVoice` 메서드로 음성 메시지를 표현하는 객체(Object)를 반환하도록 만드세요. 예를 들어 `VoiceMessage` 클래스 등 여러분의 메시지 클래스가 될 수 있습니다:

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
     * 알림 채널 반환.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * 음성 알림 표현 반환.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```