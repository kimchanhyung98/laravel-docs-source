# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification Facade 사용하기](#using-the-notification-facade)
    - [전달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐 처리하기](#queueing-notifications)
    - [즉석 알림 보내기](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [보내는 사람 지정하기](#customizing-the-sender)
    - [수신자 지정하기](#customizing-the-recipient)
    - [제목 지정하기](#customizing-the-subject)
    - [메일러 지정하기](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [메일러 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [필수 사전 조건](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림에 접근하기](#accessing-the-notifications)
    - [알림을 읽음 처리하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [필수 사전 조건](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [필수 사전 조건](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [쇼트코드 알림 포맷팅](#formatting-shortcode-notifications)
    - [발신 번호 지정하기](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [필수 사전 조건](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 첨부파일](#slack-attachments)
    - [Slack 알림 라우팅](#routing-slack-notifications)
- [알림 현지화](#localizing-notifications)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

Laravel은 [이메일 전송](/docs/{{version}}/mail) 지원 외에도 이메일, SMS(이전 명칭 Nexmo인 [Vonage](https://www.vonage.com/communications-apis/) 사용), 그리고 [Slack](https://slack.com) 등 다양한 전달 채널을 통한 알림 전송 기능을 제공합니다. 게다가 여러 커뮤니티가 개발한 다양한 [알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)을 통해 수십 가지의 다른 채널로 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장할 수도 있어, 웹 인터페이스에서 표시할 수 있습니다.

일반적으로 알림은 애플리케이션에서 발생한 일을 사용자에게 알리는 짧고 간결한 정보성 메시지여야 합니다. 예를 들어 청구 애플리케이션이라면, 이메일과 SMS 채널을 통해 사용자에게 "청구서 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 보통 `app/Notifications` 디렉터리에 저장되는 하나의 클래스로 나타냅니다. 만약 이 디렉터리가 없다면 걱정하지 마세요 — `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```
php artisan make:notification InvoicePaid
```

이 명령어를 실행하면 `app/Notifications` 디렉터리에 새로운 알림 클래스가 생성됩니다. 각 알림 클래스는 `via` 메서드와 `toMail`, `toDatabase`와 같은 다양한 메시지 작성 메서드를 포함합니다. 이 메서드들은 특정 채널에 맞게 알림을 메시지로 변환하는 역할을 합니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 두 가지 방법으로 보낼 수 있습니다: `Notifiable` 트레이트의 `notify` 메서드 사용 또는 `Notification` [facade](/docs/{{version}}/facades)를 사용하는 방법입니다. Laravel의 기본 `App\Models\User` 모델에는 기본으로 `Notifiable` 트레이트가 포함되어 있습니다:

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

`notify` 메서드는 알림 인스턴스를 인수로 받습니다:

```
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!TIP]
> `Notifiable` 트레이트는 `User` 모델뿐만 아니라 다른 모델에도 자유롭게 사용할 수 있습니다.

<a name="using-the-notification-facade"></a>
### Notification Facade 사용하기

또는 여러 명의 알림 대상(예: 사용자 컬렉션)에게 한꺼번에 알림을 보내야 할 경우, `Notification` [facade](/docs/{{version}}/facades)를 사용할 수 있습니다. 모든 알림 대상과 알림 인스턴스를 `send` 메서드에 전달하면 됩니다:

```
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하면, 알림이 `ShouldQueue` 인터페이스를 구현했더라도 바로 즉시 알림을 보낼 수 있습니다:

```
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

각 알림 클래스는 알림을 전달할 채널을 결정하는 `via` 메서드를 가집니다. 알림은 `mail`, `database`, `broadcast`, `nexmo`, `slack` 채널 등으로 전송할 수 있습니다.

> [!TIP]
> Telegram이나 Pusher 같은 다른 채널을 사용하려면 커뮤니티에서 관리하는 [Laravel Notification Channels](http://laravel-notification-channels.com) 웹사이트를 참고하세요.

`via` 메서드는 알림 대상 객체인 `$notifiable` 인스턴스를 전달받습니다. 이를 이용해 어떤 채널로 전달할지 동적으로 결정할 수 있습니다:

```
/**
 * 알림 전달 채널 가져오기
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function via($notifiable)
{
    return $notifiable->prefers_sms ? ['nexmo'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐 처리하기

> [!NOTE]
> 알림을 큐에 넣기 전에 큐 설정과 [워크커 시작하기](/docs/{{version}}/queues) 작업을 완료해야 합니다.

알림 전송은 외부 API 호출이 필요한 경우 시간이 걸릴 수 있으므로, 애플리케이션의 응답 속도 개선을 위해 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 추가해 큐로 처리할 수 있습니다. `make:notification` 명령어로 생성된 알림은 이미 이 인터페이스와 트레이트를 임포트해두므로 바로 사용할 수 있습니다:

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

`ShouldQueue` 인터페이스가 추가된 후에는 평소처럼 알림을 보내면 Laravel이 자동으로 큐에 작업을 추가해 비동기 방식으로 전달합니다:

```
$user->notify(new InvoicePaid($invoice));
```

알림 전달을 지연시키고 싶다면 `delay` 메서드를 체인하여 지연 시간을 지정할 수 있습니다:

```
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 지연 시간을 다르게 지정하려면 배열을 넘기면 됩니다:

```
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

알림 큐 작업은 수신자와 채널 조합별로 각각 생성됩니다. 예를 들어 수신자 3명, 채널 2개인 경우 총 6개의 작업이 큐에 dispatch 됩니다.

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 연결 커스터마이징

기본적으로 큐에 넣은 알림은 애플리케이션 기본 큐 연결을 사용합니다. 특정 알림에 대해 다른 큐 연결을 지정하고 싶다면, 알림 클래스에 `$connection` 프로퍼티를 정의하세요:

```
/**
 * 알림 큐 연결 이름
 *
 * @var string
 */
public $connection = 'redis';
```

<a name="customizing-notification-channel-queues"></a>
#### 알림 채널별 큐 커스터마이징

알림이 사용하는 각 전달 채널별로 다른 큐를 지정하고 싶다면, `viaQueues` 메서드를 알림 클래스에 정의할 수 있습니다. 이 메서드는 채널명과 큐명 쌍의 배열을 반환해야 합니다:

```
/**
 * 각 알림 채널별 사용할 큐 결정
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

데이터베이스 트랜잭션 내에서 큐 알림을 dispatch 하면, 큐 작업이 데이터베이스 커밋 이전에 처리될 수 있습니다. 이 경우, 트랜잭션에서 변경 또는 생성한 모델과 데이터가 데이터베이스에 아직 반영되지 않아 알림 처리 시 예상치 못한 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`인 경우에도, 알림을 보낼 때 `afterCommit` 메서드를 호출하여 트랜잭션이 커밋된 후 알림이 큐에 처리되도록 지정할 수 있습니다:

```
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림 클래스 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다:

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
     * 새로운 알림 인스턴스 생성
     *
     * @return void
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!TIP]
> 이 문제에 대한 더 자세한 해결책은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림의 최종 전송 여부 판단

큐에 등록된 알림 작업이 큐 워커에 의해 처리될 때, 알림을 최종적으로 전송할지 판단하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림은 전송되지 않습니다:

```
/**
 * 알림을 보낼지 결정
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
### 즉석 알림 보내기

애플리케이션 사용자 데이터베이스에 등록되지 않은, 외부 사용자에게 임시로 알림을 보내고 싶을 때가 있습니다. 이 경우 `Notification` facade의 `route` 메서드를 활용해 임시 수신자 정보를 지정할 수 있습니다:

```
Notification::route('mail', 'taylor@example.com')
            ->route('nexmo', '5555555555')
            ->route('slack', 'https://hooks.slack.com/services/...')
            ->notify(new InvoicePaid($invoice));
```

`mail` 채널로 보낼 때 수신자 이름도 함께 지정하려면, 이메일 주소를 키로 하고 이름을 값으로 하는 배열 형태로 넘기면 됩니다:

```
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅

알림이 이메일로 전송되도록 지원하려면, 알림 클래스에 `toMail` 메서드를 정의하세요. 이 메서드는 알림 수신자 `$notifiable`를 인수로 받아 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스는 거래용 이메일 메시지 작성에 도움을 주는 메서드를 제공합니다. 이메일에는 텍스트 라인과 "행동 유도 버튼"(call to action)이 포함될 수 있습니다. `toMail` 메서드 예시를 살펴보겠습니다:

```
/**
 * 알림의 메일 표현 생성
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
                ->action('View Invoice', $url)
                ->line('Thank you for using our application!');
}
```

> [!TIP]
> 위 예제에서 `toMail` 메서드 내에서 `$this->invoice->id`를 사용했습니다. 알림 생성자에 원하는 데이터를 주입하여 메시지 생성에 사용할 수 있습니다.

위 코드에서는 인사말, 문장, 행동 유도 버튼, 다시 한 문장 순으로 메일 메시지를 구성합니다. `MailMessage`의 메서드는 작은 이메일을 빠르고 간편하게 만들도록 돕습니다. 메일 채널은 이 메시지를 곧 예쁘고 반응형 HTML 이메일 템플릿과 일반 텍스트 버전으로 변환합니다. 다음은 `mail` 채널로 전송된 예시 이메일입니다:

<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!TIP]
> 메일 알림을 사용할 때 `config/app.php` 설정 파일의 `name` 옵션을 반드시 지정하세요. 이 값은 메일 알림의 헤더와 푸터에 사용됩니다.

<a name="other-mail-notification-formatting-options"></a>
#### 기타 메일 알림 포맷팅 옵션

알림 클래스에 텍스트 "라인"들을 직접 정의하는 대신, `view` 메서드로 사용자 정의 템플릿을 지정할 수 있습니다:

```
/**
 * 알림의 메일 표현 생성
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

메일 메시지에 일반 텍스트 뷰를 지정하려면, 뷰 이름을 배열의 두 번째 요소로 넘기면 됩니다:

```
/**
 * 알림의 메일 표현 생성
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

<a name="error-messages"></a>
#### 오류 메시지

결제 실패 같은 오류를 사용자에게 알릴 때는, `error` 메서드를 호출해 메일 메시지를 오류형으로 지정할 수 있습니다. 이 경우, 행동 유도 버튼은 검은색 대신 빨간색으로 나타납니다:

```
/**
 * 알림의 메일 표현 생성
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Message
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->error()
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-sender"></a>
### 보내는 사람 지정하기

기본적으로 메일의 보내는 사람 주소는 `config/mail.php` 설정 파일에 정의되어 있습니다. 특정 알림마다 보내는 사람을 지정하려면 `from` 메서드를 사용할 수 있습니다:

```
/**
 * 알림의 메일 표현 생성
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
### 수신자 지정하기

`mail` 채널로 알림을 보낼 때 알림 시스템은 자동으로 수신자 모델의 `email` 속성을 찾아 사용합니다. 만약 사용자가 이메일 주소를 저장하는 속성이 다르거나 이름과 함께 반환하고 싶으면, 수신자 모델에 `routeNotificationForMail` 메서드를 정의해 원하는 주소를 반환할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * mail 채널용 알림 라우팅
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return array|string
     */
    public function routeNotificationForMail($notification)
    {
        // 이메일 주소만 반환
        return $this->email_address;

        // 이메일 주소와 이름 배열 반환
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 지정하기

기본적으로 메일 제목은 알림 클래스 이름을 "타이틀 케이스"로 변환한 값입니다. 예를 들어 Class명이 `InvoicePaid`면 메일 제목은 `Invoice Paid`입니다. 제목을 직접 지정하려면 메시지 작성 시 `subject` 메서드를 호출하세요:

```
/**
 * 알림의 메일 표현 생성
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
### 메일러 지정하기

기본 메일러는 `config/mail.php` 설정 파일의 기본값을 사용합니다. 특정 알림을 보내면서 다른 메일러를 지정하려면, 메시지 작성 시 `mailer` 메서드를 호출하면 됩니다:

```
/**
 * 알림의 메일 표현 생성
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

메일 알림 템플릿(HTML과 일반 텍스트)을 직접 수정하고 싶으면, 알림 패키지 리소스를 퍼블리시하세요. 아래 명령어 실행 후 `resources/views/vendor/notifications` 폴더 내에서 템플릿을 볼 수 있습니다:

```
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

메일 알림에 첨부파일을 추가하려면 메시지 작성 시 `attach` 메서드를 사용하세요. 첫 번째 인수로는 파일의 절대 경로를 넘깁니다:

```
/**
 * 알림의 메일 표현 생성
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

첨부파일 이름이나 MIME 타입을 지정하려면, 두 번째 인수에 배열로 옵션을 넘기면 됩니다:

```
/**
 * 알림의 메일 표현 생성
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

`mailable` 객체와 달리, `attachFromStorage`를 직접 사용할 수 없고, 스토리지 디스크의 파일은 절대 경로로 `attach` 메서드에 넘겨야 합니다. 또는 `toMail`에서 [메일러 객체](/docs/{{version}}/mail)를 반환해 첨부할 수 있습니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현 생성
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

<a name="raw-data-attachments"></a>
#### 로우 데이터 첨부파일

문자열 데이터를 첨부파일로 추가할 때는 `attachData` 메서드를 사용합니다. 이때 할당할 파일명도 함께 지정해야 합니다:

```
/**
 * 알림의 메일 표현 생성
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

<a name="using-mailables"></a>
### 메일러 사용하기

필요하다면 알림의 `toMail` 메서드에서 완전한 [메일러 객체](/docs/{{version}}/mail)를 반환할 수 있습니다. 이 경우, 메일러 객체의 `to` 메서드로 수신자 주소를 명시해야 합니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * 알림의 메일 표현 생성
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
#### 메일러와 즉석 알림

[즉석 알림](#on-demand-notifications)에서는 `toMail` 메서드에 전달되는 `$notifiable` 인스턴스가 `Illuminate\Notifications\AnonymousNotifiable` 타입입니다. 이 객체는 `routeNotificationFor` 메서드로 수신자 이메일 주소를 조회할 수 있습니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;

/**
 * 알림의 메일 표현 생성
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

메일 알림 템플릿을 설계할 때는, 실제 이메일을 보내지 않고도 브라우저에서 바로 결과를 미리 보는 게 편리합니다. Laravel에서는 라우트 클로저나 컨트롤러에서 메일 알림의 `toMail` 메서드 결과를 직접 반환하면, HTML이 렌더링되어 브라우저에 표시됩니다:

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

마크다운 기반 메일 알림은 Laravel의 미리 만들어진 템플릿을 활용하면서도 긴 메시지 작성이나 맞춤화가 가능합니다. 메시지는 마크다운 문법으로 작성되어 Laravel이 반응형 HTML 템플릿과 일반 텍스트 버전을 자동 생성합니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

마크다운 메시지용 알림을 만들려면 `make:notification` 명령에 `--markdown` 옵션으로 템플릿 이름을 지정합니다:

```
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

일반 메일 알림과 마찬가지로 `toMail` 메서드를 정의해야 하지만, 메시지 구성에 `line`이나 `action` 대신 `markdown` 메서드를 사용해야 합니다. 두 번째 인자로 템플릿에 전달할 데이터를 배열로 넘길 수 있습니다:

```
/**
 * 알림의 메일 표현 생성
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

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 구문을 조합하여, Laravel이 제공하는 알림용 컴포넌트를 쉽게 조립할 수 있습니다:

```
@component('mail::message')
# Invoice Paid

Your invoice has been paid!

@component('mail::button', ['url' => $url])
View Invoice
@endcomponent

Thanks,<br>
{{ config('app.name') }}
@endcomponent
```

<a name="button-component"></a>
#### 버튼 컴포넌트

`button` 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. 인수로 `url`과 선택적으로 `color`를 받으며, 지원되는 색상은 `primary`, `green`, `red`입니다. 여러 개 버튼도 추가할 수 있습니다:

```
@component('mail::button', ['url' => $url, 'color' => 'green'])
View Invoice
@endcomponent
```

<a name="panel-component"></a>
#### 패널 컴포넌트

`panel` 컴포넌트는 일반 텍스트와 다른 배경색을 가진 패널 박스 안에 내용을 표시해, 사용자 주의를 끌 때 유용합니다:

```
@component('mail::panel')
This is the panel content.
@endcomponent
```

<a name="table-component"></a>
#### 테이블 컴포넌트

`table` 컴포넌트는 마크다운 표를 HTML 표로 변환합니다. 마크다운의 표 정렬 문법도 지원합니다:

```
@component('mail::table')
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
@endcomponent
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

마크다운 알림 컴포넌트를 애플리케이션으로 내보내어 직접 수정할 수 있습니다. 다음 명령어로 `laravel-mail` 태그의 컴포넌트들을 퍼블리시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

`resources/views/vendor/mail` 디렉터리에 HTML과 텍스트 각각에 해당하는 컴포넌트 파일들이 생성되며, 자유롭게 커스터마이징 할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 스타일 커스터마이징

퍼블리시한 컴포넌트 내의 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 있습니다. 이 파일의 CSS를 수정하면 이메일 내 인라인 스타일에 반영됩니다.

새 테마를 만들고 싶다면 이 디렉터리에 새로운 CSS 파일을 추가하고 `mail` 설정 파일의 `theme` 값을 새 테마명으로 변경하세요.

특정 알림에만 테마를 지정하고 싶으면 메시지 작성 시 `theme` 메서드를 사용하세요:

```
/**
 * 알림의 메일 표현 생성
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
### 필수 사전 조건

`database` 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 타입과 JSON 방식의 알림 데이터가 포함됩니다.

저장된 알림은 애플리케이션 UI에서 조회할 수 있습니다. 먼저 `notifications:table` 명령어로 알맞은 마이그레이션을 생성하고 다음 명령으로 마이그레이션을 실행하세요:

```
php artisan notifications:table

php artisan migrate
```

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

데이터베이스에 알림을 저장하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 인스턴스를 받고, 평범한 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 예시 `toArray` 구현입니다:

```
/**
 * 알림의 배열 표현 가져오기
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
#### `toDatabase`와 `toArray` 차이

`toArray` 메서드는 `broadcast` 채널에서도 데이터 수집용으로 사용됩니다. 만약 데이터베이스와 브로드캐스트용 각각 다른 배열 표현이 필요하면, `toDatabase` 메서드를 별도로 정의해야 합니다.

<a name="accessing-the-notifications"></a>
### 알림에 접근하기

데이터베이스에 저장된 알림에 접근하려면, Notifiable 트레이트가 포함된 모델의 `notifications` [엘로퀀트 관계](/docs/{{version}}/eloquent-relationships)를 활용하세요. 기본적으로 Laravel의 `App\Models\User` 모델에 포함되어 있습니다.

다음 예시는 알림들을 조회하는 방법입니다. 알림은 기본적으로 `created_at` 내림차순으로 정렬되어 가장 최근 알림이 제일 앞에 위치합니다:

```
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

읽지 않은 알림만 조회하려면 `unreadNotifications` 관계를 사용하세요:

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!TIP]
> JavaScript 클라이언트에서 알림에 접근하려면, 알림을 반환하는 컨트롤러를 정의하고 그 URL에 HTTP 요청을 보내는 방식을 사용하면 됩니다.

<a name="marking-notifications-as-read"></a>
### 알림을 읽음 처리하기

사용자가 알림을 확인할 때, 알림을 "읽음"으로 표시하는 것이 일반적입니다. `Notifiable` 트레이트의 `markAsRead` 메서드를 사용하면, 데이터베이스 알림 레코드의 `read_at` 열을 업데이트할 수 있습니다:

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

모든 알림을 반복문 없이 한꺼번에 읽음 처리하려면, 알림 컬렉션에 바로 메서드를 호출하거나 데이터베이스에서 직접 업데이트 쿼리를 실행할 수 있습니다:

```
// 컬렉션 전체에 대해
$user->unreadNotifications->markAsRead();

// 쿼리로 한꺼번에 처리
$user = App\Models\User::find(1);
$user->unreadNotifications()->update(['read_at' => now()]);
```

알림을 데이터베이스에서 완전히 삭제하려면 다음과 같이 합니다:

```
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림

<a name="broadcast-prerequisites"></a>
### 필수 사전 조건

브로드캐스트 알림을 사용하려면 Laravel의 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 기능을 먼저 설정하고 익숙해져야 합니다. 이벤트 브로드캐스팅은 서버에서 발생한 Laravel 이벤트를 자바스크립트 프론트엔드에서 실시간으로 받을 수 있게 합니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel의 이벤트 브로드캐스팅 서비스를 통해 실시간으로 클라이언트에 알림을 보냅니다. 브로드캐스트를 지원하려면 알림 클래스에 `toBroadcast` 메서드를 정의하세요. 이 메서드는 `$notifiable` 엔티티를 받아 `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast` 메서드가 없으면 `toArray` 메서드가 데이터를 제공합니다. 반환된 데이터는 JSON으로 인코딩되어 JavaScript 프론트엔드로 전송됩니다. 예시입니다:

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트 가능한 알림 데이터 생성
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

브로드캐스트 알림은 모두 큐에 등록되어 처리됩니다. 큐 연결과 큐 명을 지정하려면, `BroadcastMessage` 인스턴스에서 `onConnection`과 `onQueue` 메서드를 체인하세요:

```
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 커스터마이징

브로드캐스트 알림에는 기본적으로 알림 클래스 이름이 `type` 필드로 포함되어 있습니다. 이 값을 직접 정의하려면 알림 클래스에 `broadcastType` 메서드를 추가하세요:

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * 브로드캐스트 알림 타입 정의
 *
 * @return string
 */
public function broadcastType()
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 대기하기

알림은 `{notifiable}.{id}` 형식의 개인 채널로 브로드캐스트됩니다. 예를 들어 `App\Models\User` ID 1인 대상에게 보낼 때는 `App.Models.User.1` 채널에 브로드캐스트됩니다. [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 사용하는 경우, 다음처럼 간단히 알림 이벤트를 리스닝할 수 있습니다:

```
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 커스터마이징

브로드캐스트 알림을 받을 채널명을 사용자 지정하려면, 수신자 모델에 `receivesBroadcastNotificationsOn` 메서드를 정의하세요:

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
     * 사용자별 브로드캐스트 채널명 정의
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
### 필수 사전 조건

Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 Nexmo)로 구동됩니다. SMS 알림을 사용하려면 `laravel/nexmo-notification-channel`과 `nexmo/laravel` 패키지를 설치해야 합니다:

```
composer require laravel/nexmo-notification-channel nexmo/laravel
```

`nexmo/laravel` 패키지는 별도의 [설정 파일](https://github.com/Nexmo/nexmo-laravel/blob/master/config/nexmo.php)도 제공하지만, 애플리케이션에 퍼블리시하지 않아도 됩니다. 기본적으로 `NEXMO_KEY`, `NEXMO_SECRET` 환경변수를 사용하세요.

또한 `config/services.php`에 `nexmo` 설정값을 추가해야 합니다. 다음 설정 예를 참고하세요:

```
'nexmo' => [
    'sms_from' => '15556666666',
],
```

`sms_from`은 SMS를 발송할 전화번호로, Vonage 대시보드에서 생성한 번호를 사용해야 합니다.

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

알림이 SMS로 전송 가능하도록 하려면, 알림 클래스에 `toNexmo` 메서드를 정의하세요. `$notifiable` 인스턴스를 인자로 받아 `Illuminate\Notifications\Messages\NexmoMessage` 인스턴스를 반환해야 합니다:

```
/**
 * Vonage / SMS 알림 메시지 생성
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 문자 포함

SMS 메시지에 유니코드가 포함될 경우, `unicode` 메서드를 호출해야 올바르게 인코딩됩니다:

```
/**
 * Vonage / SMS 알림 메시지 생성
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your unicode message')
                ->unicode();
}
```

<a name="formatting-shortcode-notifications"></a>
### 쇼트코드 알림 포맷팅

Vonage에서 미리 정의한 메시지 템플릿인 쇼트코드(SMS shortcode) 알림도 지원합니다. 쇼트코드 SMS를 보내려면, 알림 클래스에 `toShortcode` 메서드를 정의하고 반환 값으로 템플릿 타입과 커스텀 변수를 포함한 배열을 넘기세요:

```
/**
 * Vonage / 쇼트코드 알림 포맷팅
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function toShortcode($notifiable)
{
    return [
        'type' => 'alert',
        'custom' => [
            'code' => 'ABC123',
        ],
    ];
}
```

> [!TIP]
> [SMS 알림 라우팅](#routing-sms-notifications)과 같이, `routeNotificationForShortcode` 메서드를 수신자 모델에 구현해야 합니다.

<a name="customizing-the-from-number"></a>
### 발신 번호 지정하기

기본 `config/services.php` 파일의 번호와 달리, 특정 알림에서 발신 번호를 다르게 지정하려면, `NexmoMessage` 인스턴스 생성 시 `from` 메서드를 호출하세요:

```
/**
 * Vonage / SMS 알림 메시지 생성
 *
 * @param  mixed  $notifiable
 * @return NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your SMS message content')
                ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가하기

사용자별 또는 팀별 SMS 비용 추적용으로, Vonage에서 제공하는 "클라이언트 참조" 값을 알림에 넣을 수 있습니다. 40자 이내 문자열이며, 다음과 같이 추가할 수 있습니다:

```
/**
 * Vonage / SMS 알림 메시지 생성
 *
 * @param  mixed  $notifiable
 * @return NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

Vonage 알림을 올바른 전화번호로 라우팅하려면, 수신자 모델에 `routeNotificationForNexmo` 메서드를 정의하세요. 알림 인스턴스를 인자로 받으며, 전화번호 문자열을 반환해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Nexmo 채널용 알림 라우팅
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return string
     */
    public function routeNotificationForNexmo($notification)
    {
        return $this->phone_number;
    }
}
```

<a name="slack-notifications"></a>
## Slack 알림

<a name="slack-prerequisites"></a>
### 필수 사전 조건

Slack으로 알림을 보내려면, Slack Notification Channel 패키지를 설치해야 합니다:

```
composer require laravel/slack-notification-channel
```

슬랙 팀을 위해 [Slack App](https://api.slack.com/apps?new_app=1)을 만들고, 워크스페이스에 "Incoming Webhook"을 설정하세요. 그러면 알림을 전송할 수 있는 웹훅 URL이 생성됩니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

Slack 메시지를 지원하는 알림 클래스는 `toSlack` 메서드를 정의해야 하며, `$notifiable`을 인자로 받아 `Illuminate\Notifications\Messages\SlackMessage` 인스턴스를 반환합니다. Slack 메시지에는 텍스트 구성이 가능하며, 추가적으로 "첨부파일"을 포함시킬 수도 있습니다. 기본적인 `toSlack` 예시는 다음과 같습니다:

```
/**
 * Slack 알림 메시지 생성
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

Slack 메시지에 "첨부파일"을 추가할 수 있는데, 첨부파일은 텍스트보다 풍부한 형식 설정이 가능합니다. 예를 들어 애플리케이션에서 발생한 예외 관련 에러 알림과 상세 링크를 포함하는 경우는 다음과 같습니다:

```
/**
 * Slack 알림 메시지 생성
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

첨부파일에는 사용자에게 보여줄 테이블 형식 데이터도 포함할 수 있습니다:

```
/**
 * Slack 알림 메시지 생성
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
#### 마크다운 첨부파일 내용

첨부파일 필드에 마크다운 문법이 포함되어 있을 경우, `markdown` 메서드를 호출해 어떤 필드를 마크다운으로 해석할지 지정할 수 있습니다. 허용되는 필드는 `pretext`, `text`, `fields`입니다. Slack 첨부파일 포맷에 관한 자세한 내용은 [Slack API 문서](https://api.slack.com/docs/message-formatting#message_formatting)를 참고하세요:

```
/**
 * Slack 알림 메시지 생성
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

Slack 알림을 올바른 팀과 채널에 전달하려면, 수신자 모델에 `routeNotificationForSlack` 메서드를 정의하고 Slack의 웹훅 URL을 반환하세요. 웹훅은 Slack App에서 "Incoming Webhook" 설정을 통해 생성합니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Slack 채널용 알림 라우팅
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

Laravel은 HTTP 요청의 현재 로케일과 달리, 다른 로케일로 알림을 보낼 수 있고, 큐 처리를 할 때도 이 로케일 정보를 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스는 `locale` 메서드를 제공합니다. 이 메서드가 호출되면 알림 처리 중 애플리케이션 로케일이 해당 로케일로 일시 변경되었다가 처리 완료 후 원래대로 복구됩니다:

```
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

`Notification` Facade로 여러 사용자에게 현지화를 적용해 보낼 수도 있습니다:

```
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

애플리케이션에서 각 사용자의 선호 로케일 정보를 저장하는 경우, 수신자 모델에 `HasLocalePreference` 인터페이스를 구현해 Laravel이 자동으로 해당 로케일을 사용하게 할 수 있습니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일 반환
     *
     * @return string
     */
    public function preferredLocale()
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면, `locale` 메서드를 호출하지 않아도 자동으로 선호 로케일이 적용됩니다:

```
$user->notify(new InvoicePaid($invoice));
```

<a name="notification-events"></a>
## 알림 이벤트

<a name="notification-sending-event"></a>
#### 알림 전송 이벤트

알림이 전송될 때 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 발행됩니다. 이벤트에는 해당 수신자와 알림 인스턴스가 포함되어 있습니다. `EventServiceProvider`에 이 이벤트에 대한 리스너를 등록할 수 있습니다:

```
/**
 * 이벤트 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Notifications\Events\NotificationSending' => [
        'App\Listeners\CheckNotificationStatus',
    ],
];
```

만약 리스너의 `handle` 메서드가 `false`를 반환하면 알림 전송이 취소됩니다:

```
use Illuminate\Notifications\Events\NotificationSending;

/**
 * 이벤트 핸들러
 *
 * @param  \Illuminate\Notifications\Events\NotificationSending  $event
 * @return void
 */
public function handle(NotificationSending $event)
{
    return false;
}
```

이벤트 리스너에서 `$event->notifiable`, `$event->notification`, `$event->channel` 프로퍼티에 접근할 수 있습니다.

<a name="notification-sent-event"></a>
#### 알림 전송 완료 이벤트

알림이 전송 완료되면 `Illuminate\Notifications\Events\NotificationSent` 이벤트가 발행되며, `EventServiceProvider`에 리스너를 등록할 수 있습니다:

```
/**
 * 이벤트 리스너 매핑
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Notifications\Events\NotificationSent' => [
        'App\Listeners\LogNotification',
    ],
];
```

> [!TIP]
> 리스너 등록 후 `event:generate` Artisan 명령어로 빠르게 리스너 클래스를 생성할 수 있습니다.

이벤트 핸들러는 `$event->notifiable`, `$event->notification`, `$event->channel`, 그리고 `$event->response` 속성에 접근할 수 있습니다:

```
/**
 * 이벤트 핸들러
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

Laravel은 다양한 기본 알림 채널을 제공하지만, 직접 알림 채널 드라이버를 작성해 다른 채널로 알림을 보내야 할 수도 있습니다. Laravel에서는 간단히 `send` 메서드를 포함한 클래스를 정의하여 시작할 수 있습니다. 이 메서드는 두 개의 인수 `$notifiable`(수신자)와 `$notification`(알림 인스턴스)을 받습니다.

`send` 메서드 내에서, 알림 클래스의 커스텀 메서드를 호출해 메시지 객체를 가져온 후 원하는 방식으로 수신자에게 알림을 보내면 됩니다:

```
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * 주어진 알림 전송하기
     *
     * @param  mixed  $notifiable
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return void
     */
    public function send($notifiable, Notification $notification)
    {
        $message = $notification->toVoice($notifiable);

        // $notifiable에게 알림 전송 처리...
    }
}
```

알림 클래스의 `via` 메서드에서 커스텀 채널 클래스를 반환해 채널로 지정할 수 있습니다. 예를 들어, `toVoice` 메서드는 음성 알림 메시지를 나타내는 자신만의 `VoiceMessage` 클래스를 반환할 수 있습니다:

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
     * 알림 전달 채널 가져오기
     *
     * @param  mixed  $notifiable
     * @return array|string
     */
    public function via($notifiable)
    {
        return [VoiceChannel::class];
    }

    /**
     * 음성 알림 메시지 표현 생성
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