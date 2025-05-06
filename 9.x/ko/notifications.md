# 알림(Notifications)

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
    - [첨부 파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 요구사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 요구사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 리스닝하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 요구사항](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - [숏코드 알림 포맷팅](#formatting-shortcode-notifications)
    - [발신 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 요구사항](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 첨부파일](#slack-attachments)
    - [Slack 알림 라우팅](#routing-slack-notifications)
- [알림 로컬라이징](#localizing-notifications)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개

[이메일 전송](/docs/{{version}}/mail) 지원 외에도, Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 명칭 Nexmo), [Slack](https://slack.com) 등 다양한 채널을 통한 알림 전송을 지원합니다. 또한, [커뮤니티에서 개발된 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 제공되어 수십 가지 채널을 통해 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션 내에서 발생한 일을 사용자에게 알려주는 짧고 정보성 메시지여야 합니다. 예를 들어, 결제 애플리케이션을 개발 중이라면, 사용자가 송장을 결제하면 이메일과 SMS 채널을 통해 "송장 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기

Laravel에서 각 알림은 일반적으로 `app/Notifications` 디렉토리에 저장되는 하나의 클래스로 표현됩니다. 애플리케이션에 해당 디렉토리가 없어도 걱정하지 마세요. `make:notification` Artisan 명령을 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령은 새로운 알림 클래스를 `app/Notifications` 디렉토리에 생성합니다. 각 알림 클래스에는 `via` 메서드와 `toMail` 또는 `toDatabase`와 같은 여러 메시지 빌더 메서드가 포함되어, 알림을 해당 채널에 맞는 메시지로 변환합니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 `Notifiable` 트레이트의 `notify` 메서드를 사용하거나, `Notification` [파사드](/docs/{{version}}/facades)를 사용해서 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다.

    <?php

    namespace App\Models;

    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable
    {
        use Notifiable;
    }

이 트레이트에서 제공하는 `notify` 메서드는 알림 인스턴스를 인자로 받습니다.

    use App\Notifications\InvoicePaid;

    $user->notify(new InvoicePaid($invoice));

> **참고**  
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 제한되는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는, 여러 개의 알림 대상을 묶어서 전송해야 할 때는 `Notification` [파사드](/docs/{{version}}/facades)를 사용할 수 있습니다. 파사드의 `send` 메서드에 알림 대상 집합과 알림 인스턴스를 전달합니다:

    use Illuminate\Support\Facades\Notification;

    Notification::send($users, new InvoicePaid($invoice));

`sendNow` 메서드를 사용하면 큐에 관계없이 즉시 알림이 전송됩니다. 이 방법은 알림이 `ShouldQueue` 인터페이스를 구현해도 즉시 발송합니다:

    Notification::sendNow($developers, new DeploymentCompleted($deployment));

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

모든 알림 클래스에는 이 알림이 어떤 채널로 전달될지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 보낼 수 있습니다.

> **참고**  
> Telegram, Pusher 등 다른 채널을 사용하려면, 커뮤니티에서 제공하는 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 인자로 받으며, 여기에 따라 알림의 전달 채널을 동적으로 지정할 수 있습니다:

    /**
     * 알림이 전달될 채널을 반환합니다.
     *
     * @param  mixed  $notifiable
     * @return array
     */
    public function via($notifiable)
    {
        return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
    }

<a name="queueing-notifications"></a>
### 알림 큐잉하기

> **경고**  
> 알림을 큐잉하기 전에 반드시 큐 설정을 마치고 [작업자 워커를 시작](/docs/{{version}}/queues)해야 합니다.

특정 채널이 알림을 외부 API로 전달해야 할 경우, 알림 발송은 시간이 오래 걸릴 수 있습니다. 응답 속도를 높이려면, 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가해 큐 처리하도록 하세요. `make:notification` 명령으로 만든 알림에는 이미 이들이 임포트되어 있습니다.

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

이제 `ShouldQueue` 인터페이스가 추가되었으므로 평소처럼 알림을 전송하면, Laravel이 자동으로 큐에 넣어 처리합니다:

    $user->notify(new InvoicePaid($invoice));

알림 큐잉 시, 수신자와 채널 조합마다 하나의 큐 작업이 만들어집니다. 예를 들어, 세 명의 수신자와 두 채널이 있으면 여섯 개의 작업이 큐에 전송됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연(delaying)

알림을 일정 시간 후에 발송하고 싶다면, 알림 인스턴스에 `delay` 메서드를 체이닝합니다:

    $delay = now()->addMinutes(10);

    $user->notify((new InvoicePaid($invoice))->delay($delay));

<a name="delaying-notifications-per-channel"></a>
#### 채널별 알림 지연

특정 채널마다 다른 지연 시간을 주려면, `delay`에 배열을 전달하면 됩니다:

    $user->notify((new InvoicePaid($invoice))->delay([
        'mail' => now()->addMinutes(5),
        'sms' => now()->addMinutes(10),
    ]));

또는 알림 클래스에 `withDelay` 메서드를 정의해도 됩니다:

    /**
     * 알림 전달 지연 시간 결정
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

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 커넥션 커스터마이즈

기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 특정 알림에 대해 다른 커넥션을 사용하려면, 알림 클래스에 `$connection` 프로퍼티를 지정하세요:

    /**
     * 이 알림을 큐잉할 때 사용할 큐 커넥션 이름
     *
     * @var string
     */
    public $connection = 'redis';

또는 채널별로 큐 커넥션을 다르게 하려면, `viaConnections` 메서드를 정의합니다:

    /**
     * 각 알림 채널에 사용할 큐 커넥션을 결정합니다.
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

<a name="customizing-notification-channel-queues"></a>
#### 알림 채널별 큐 커스터마이즈

알림 채널별로 큐 이름도 커스터마이즈 할 수 있습니다. `viaQueues` 메서드를 사용하세요:

    /**
     * 각 알림 채널에 사용할 큐를 결정합니다.
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

<a name="queued-notifications-and-database-transactions"></a>
#### 큐 알림과 데이터베이스 트랜잭션

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치되면, 트랜잭션 커밋 전에 큐 작업이 처리될 수 있습니다. 이 경우, 트랜잭션 중에 수정·생성한 모델이나 레코드는 데이터베이스에 반영되지 않았을 수 있습니다. 만약 알림이 이런 데이터에 의존한다면, 예기치 않은 에러가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`인 경우, 알림을 보낼 때 `afterCommit` 메서드를 호출하면 모든 데이터베이스 트랜잭션 커밋 이후에 알림을 디스패치하도록 할 수 있습니다:

    use App\Notifications\InvoicePaid;

    $user->notify((new InvoicePaid($invoice))->afterCommit());

또는 생성자 내에서 `afterCommit`을 호출해도 됩니다.

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
         *
         * @return void
         */
        public function __construct()
        {
            $this->afterCommit();
        }
    }

> **참고**  
> 이런 이슈에 대한 자세한 설명은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐 알림 송신 여부 결정

큐잉된 알림이 백그라운드 작업으로 디스패치된 후에도, 실제 발송 전 송신 여부를 결정하려면 알림 클래스에 `shouldSend` 메서드를 정의하세요. 이 메서드에서 `false`를 반환하면 알림이 발송되지 않습니다:

    /**
     * 알림을 발송할지 여부 결정
     *
     * @param  mixed  $notifiable
     * @param  string  $channel
     * @return bool
     */
    public function shouldSend($notifiable, $channel)
    {
        return $this->invoice->isPaid();
    }

<a name="on-demand-notifications"></a>
### 온디맨드 알림

애플리케이션에 저장된 "user"가 아닌 대상에게도 알림을 보낼 수 있습니다. 이 때는 `Notification` 파사드의 `route` 메서드로 임의의 라우트 정보를 지정한 뒤 `notify`를 호출합니다:

    use Illuminate\Broadcasting\Channel;
    use Illuminate\Support\Facades\Notification;

    Notification::route('mail', 'taylor@example.com')
                ->route('vonage', '5555555555')
                ->route('slack', 'https://hooks.slack.com/services/...')
                ->route('broadcast', [new Channel('channel-name')])
                ->notify(new InvoicePaid($invoice));

`mail` 경로를 지정할 때 수신자의 이름도 함께 제공하려면, 이메일과 이름으로 배열 형태로 전달할 수 있습니다:

    Notification::route('mail', [
        'barrett@example.com' => 'Barrett Blair',
    ])->notify(new InvoicePaid($invoice));

---

(이하의 세부 목차별 설명도 동일한 형식과 용어로 반복 번역됩니다. 질문이 너무 길어 한 번에 입력할 수 없어, **필요하다면 요청하신 추가 섹션**을 따로 요청해주시면 계속 이어서 번역해 드릴 수 있습니다.)