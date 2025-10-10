# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드로빈 설정](#round-robin-configuration)
- [Mailable 클래스 생성](#generating-mailables)
- [Mailable 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(view) 설정](#configuring-the-view)
    - [뷰 데이터 전달](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운(Markdown) 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메일 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 대기열 처리](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식(Transport)](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 직관적이고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail` 등을 위한 드라이버를 지원하며, 로컬 또는 클라우드 기반 서비스 중 원하는 것을 빠르게 선택해 메일을 보낼 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일에 설정된 각 메일러는 고유한 설정값과 "전송 방식(transport)"를 가질 수 있으므로, 애플리케이션에서 특정 메일 메시지를 전송하는 데 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, Postmark는 트랜잭션 메일 전송에, Amazon SES는 대량 이메일 발송에 사용할 수 있습니다.

`mail` 설정 파일 내에 `mailers` 배열이 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송 방식 별로 예시 구성 항목이 들어 있으며, `default` 설정값은 애플리케이션에서 이메일을 보낼 때 기본적으로 어떤 메일러를 사용할지 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 필수 조건 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 일반적으로 SMTP 서버를 통한 이메일 전송보다 더 간단하고 빠릅니다. 가능한 경우 이러한 드라이버를 사용하실 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer 전송 패키지를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 지정하세요:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그 다음, `mailers` 배열에 다음과 같은 설정 배열을 추가하세요:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러 설정이 완료되면, `config/services.php` 파일에 다음 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 [Mailgun region](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하지 않는 경우, `services` 설정 파일에서 해당 지역의 endpoint를 지정할 수 있습니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    'scheme' => 'https',
],
```

<a name="postmark-driver"></a>
#### Postmark 드라이버

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 전송 패키지를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `postmark`로 설정하세요. 기본 메일러 설정 후, `config/services.php` 파일에 다음 옵션이 들어 있는지 확인하세요:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하려면, `config/mail.php` 파일의 해당 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `resend`로 설정하세요. 기본 메일러 설정 후, `config/services.php` 파일에 아래 옵션이 있는지 확인하세요:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer를 사용해 다음과 같이 설치하세요:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 아래 옵션이 있는지 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

[AWS 임시 자격증명(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능(subscription management features)](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환하도록 할 수 있습니다:

```php
/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-List-Management-Options' => 'contactListName=MyContactList;topicName=MyTopic',
        ],
    );
}
```

이메일 전송 시 Laravel이 AWS SDK의 `SendEmail` 메서드에 추가 옵션을 전달하도록 하려면, `ses` 설정에 `options` 배열을 정의할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'options' => [
        'ConfigurationSetName' => 'MyConfigurationSet',
        'EmailTags' => [
            ['Name' => 'foo', 'Value' => 'bar'],
        ],
    ],
],
```

<a name="mailersend-driver"></a>
#### MailerSend 드라이버

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스이며, Laravel용 API 기반 메일 드라이버 패키지를 제공합니다. 해당 패키지는 Composer로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

패키지 설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경변수를 추가하세요. 또한, `MAIL_MAILER` 환경변수는 `mailersend`로 정의해 주세요:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php` 파일의 `mailers` 배열에 MailerSend를 추가하세요:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend 및 호스팅된 템플릿 사용 방법 등 자세한 내용은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정 (Failover Configuration)

외부 메일 서비스가 다운되는 경우가 있을 수 있습니다. 이런 상황에는 하나 이상의 백업 메일 발송 구성(장애 조치용 설정)을 정의해 놓으면 유용합니다.

이를 위해서는 `failover` 전송 방식을 사용하는 메일러를 `mail` 설정 파일에서 생성해야 합니다. `failover` 메일러는 사용 순서대로 참조할 `mailers` 목록 배열을 포함해야 합니다:

```php
'mailers' => [
    'failover' => [
        'transport' => 'failover',
        'mailers' => [
            'postmark',
            'mailgun',
            'sendmail',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

failover 메일러를 정의했다면, 이 메일러명을 `mail` 설정 파일의 `default` 키에 지정하여 애플리케이션의 기본 메일러로 사용하도록 설정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드로빈 설정 (Round Robin Configuration)

`roundrobin` 전송 방식은 메일 발송 workload를 여러 메일러에 분산할 수 있습니다. 사용하려면, `mail` 설정 파일에서 `roundrobin` 전송 방식을 사용하는 메일러를 정의하고, `mailers` 배열에 사용할 메일러들을 나열하세요:

```php
'mailers' => [
    'roundrobin' => [
        'transport' => 'roundrobin',
        'mailers' => [
            'ses',
            'postmark',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

라운드로빈 메일러를 기본 메일러로 사용할 땐 `mail` 설정 파일의 `default` 키값에 이 메일러명을 지정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 전송 방식은 설정된 메일러 목록에서 무작위로 하나를 선택한 뒤, 이후 이메일에서는 차례로 다음 메일러를 사용합니다. `failover`가 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)* 달성을 목표로 하는 반면, `roundrobin`은 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*에 중점을 둡니다.

<a name="generating-mailables"></a>
## Mailable 클래스 생성 (Generating Mailables)

Laravel 애플리케이션을 만들 때, 애플리케이션이 보내는 각 이메일 유형은 "Mailable" 클래스(메일러블)로 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 이 디렉토리가 없다면 걱정하지 마세요. `make:mail` Artisan 명령어를 통해 첫 메일러블 클래스를 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 클래스 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 해당 파일을 열어 내용을 살펴보세요. 메일러블 클래스는 여러 메서드에서 설정할 수 있으며, 대표적으로 `envelope`, `content`, `attachments` 메서드 등이 있습니다.

`envelope` 메서드는 메세지의 제목(subject) 및 때때로 수신자를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메세지 내용을 생성할 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope를 사용한 발신자 설정

우선, 이메일의 발신자, 즉 "from" 주소를 설정하는 방법입니다. 두 가지 방식이 있습니다. 첫 번째는 메세지의 envelope에서 "from" 주소를 직접 지정하는 방법입니다:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

필요하다면 `replyTo` 주소도 지정할 수 있습니다:

```php
return new Envelope(
    from: new Address('jeffrey@example.com', 'Jeffrey Way'),
    replyTo: [
        new Address('taylor@example.com', 'Taylor Otwell'),
    ],
    subject: 'Order Shipped',
);
```

<a name="using-a-global-from-address"></a>
#### 전역 `from` 주소 사용

애플리케이션에서 모든 이메일에 동일한 "from" 주소를 쓴다면, 매번 각 메일러블 클래스에 설정하는 대신, `config/mail.php` 파일에 전역 "from" 주소를 지정할 수 있습니다. 이 경우, 메일러블 클래스 내에서 별도 지정하지 않으면 이 주소가 기본으로 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, 전역 "reply_to" 주소도 설정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(view) 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드 내에서 이메일 본문을 렌더링할 때 사용할 `view`(또는 템플릿)을 지정할 수 있습니다. 일반적으로 이메일은 [Blade 템플릿](/docs/12.x/blade)을 사용하므로, Blade의 모든 기능과 편의성을 그대로 이용해 HTML을 만들 수 있습니다:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> [!NOTE]
> 모든 이메일 템플릿을 보관할 `resources/views/mail` 디렉토리를 생성하는 것이 좋습니다. 단, 꼭 거기 두지 않아도 `resources/views` 내 원하는 곳에 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 따로 정의하고 싶다면, `Content` 정의 시 `text` 파라미터에 plain-text 템플릿을 지정하면 됩니다. HTML, Plain-text 버전을 동시에 정의해 둘 수도 있습니다:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```

참고로, `html` 파라미터는 `view`와 동일한 역할을 하며, 별칭으로 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 전달 (View Data)

<a name="via-public-properties"></a>
#### public 프로퍼티 이용

이메일의 HTML을 렌더링할 때 사용할 데이터를 뷰에 전달해야 할 일이 많습니다. 데이터를 뷰에 전달하는 방법은 두 가지가 있습니다. 먼저, 메일러블 클래스에 정의된 public 프로퍼티는 자동으로 뷰에서 사용할 수 있습니다. 즉, 생성자에서 데이터를 받으면 public 프로퍼티로 할당하세요:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

public 프로퍼티에 할당한 데이터는 Blade 템플릿에서 곧바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 이용

템플릿으로 전달하는 데이터의 포맷을 커스터마이즈하고 싶은 경우에는, `Content` 정의의 `with` 파라미터로 직접 데이터를 전달할 수 있습니다. 이 경우 데이터는 생성자에서 받아 `protected` 또는 `private` 프로퍼티로 관리해야 템플릿에 자동 노출되지 않습니다:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
            with: [
                'orderName' => $this->order->name,
                'orderPrice' => $this->order->price,
            ],
        );
    }
}
```

`with` 파라미터에 전달한 데이터도 Blade 템플릿에서 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일 (Attachments)

이메일에 첨부파일을 추가하려면, 메일 메시지의 `attachments` 메서드에서 반환하는 배열에 첨부파일을 추가하세요. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달하여 첨부파일을 추가할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Attachment;

/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file'),
    ];
}
```

첨부파일의 표시 이름이나 MIME 타입을 지정하고 싶다면, `as`, `withMime` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="attaching-files-from-disk"></a>
#### 파일 시스템 Disk에서 첨부하기

[파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 첨부하려면 `fromStorage` 메서드를 사용하세요:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

첨부 이름과 MIME 타입도 지정할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

기본 디스크 이외의 스토리지 디스크를 사용할 경우 `fromStorageDisk` 메서드를 사용하세요:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorageDisk('s3', '/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="raw-data-attachments"></a>
#### Raw 데이터 첨부파일

파일을 직접 저장하지 않고 메모리상의 raw 데이터(예: 생성된 PDF 등)를 첨부하려면, `fromData` 메서드를 사용하세요. 이 메서드는 raw 바이트 데이터를 resolve하는 클로저와 첨부될 파일명(name)을 인자로 받습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="inline-attachments"></a>
### 인라인 첨부파일 (Inline Attachments)

이메일에 인라인 이미지를 삽입하는 것은 보통 번거로운 작업이지만, Laravel은 이를 쉽게 처리할 수 있는 방법을 제공합니다. 인라인 이미지를 포함하려면 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하세요. `$message`는 모든 이메일 템플릿에서 자동으로 사용할 수 있습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에서는 사용할 수 없습니다. plain-text 메세지는 인라인 첨부파일 기능이 적용되지 않습니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터로 인라인 첨부

raw 이미지 데이터를 직접 이메일 템플릿에 인라인 삽입하려면 `$message` 변수의 `embedData` 메서드를 호출하세요. 이 때, 첨부 이미지의 파일명을 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체 (Attachable Objects)

단순히 파일 경로 문자열로 첨부하는 것 이외에, 애플리케이션에서 첨부 가능한 엔티티(예: 사진)가 클래스로 표현되는 경우가 많습니다. 예를 들어, 사진을 첨부할 때 `Photo` 모델이 있다면, 이 객체를 직접 `attach` 메서드에 넘기고 싶을 수 있습니다. Attachable 객체는 이를 가능하게 해줍니다.

먼저, 메시지에 첨부할 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 이 인터페이스에는 `toMailAttachment` 메서드가 요구되며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * Get the attachable representation of the model.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

Attachable 객체를 만든 후에는, 이메일 메시지의 `attachments` 메서드에서 이 객체를 반환할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

물론 첨부파일 데이터가 Amazon S3와 같은 원격 파일 스토리지에 저장되어 있을 수 있습니다. 이를 위해 Laravel은 [파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 사용해 첨부파일 인스턴스를 생성할 수 있도록 지원합니다:

```php
// 기본 디스크의 파일로 첨부파일 생성
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일로 첨부파일 생성
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 있는 데이터로 첨부파일 인스턴스를 만들 수 있습니다. 이 경우 `fromData` 메서드에 클로저를 전달하세요:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일의 이름이나 MIME 타입을 커스터마이즈하려면 `as`, `withMime` 메서드를 추가로 사용할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

특정 상황에서는 메시지에 추가 헤더를 붙여야 할 수 있습니다. 예를 들면, `Message-Id` 또는 임의의 텍스트 헤더를 추가하는 경우입니다.

이를 위해서는 메일러블 클래스에 `headers` 메서드를 정의하고, `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하세요. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받으며, 필요한 것만 입력하면 됩니다:

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        messageId: 'custom-message-id@example.com',
        references: ['previous-message@example.com'],
        text: [
            'X-Custom-Header' => 'Custom Value',
        ],
    );
}
```

<a name="tags-and-metadata"></a>
### 태그 및 메타데이터 (Tags and Metadata)

Mailgun, Postmark 등 일부 서드파티 이메일 제공업체는 "태그"나 "메타데이터"를 이용해 메일을 그룹화 및 추적할 수 있도록 지원합니다. 메일러블의 `Envelope` 정의에서 태그와 메타데이터를 추가할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        tags: ['shipment'],
        metadata: [
            'order_id' => $this->order->id,
        ],
    );
}
```

Mailgun 드라이버를 사용할 경우 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags), [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대한 Mailgun 문서를 참고하세요. Postmark의 [태그 지원](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서도 마찬가지입니다.

Amazon SES를 사용하는 경우, [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부하려면 `metadata` 메서드를 활용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징 (Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer를 사용합니다. 메일 전송 직전 Symfony Message 인스턴스를 통해 추가적으로 메시지를 커스터마이즈할 수 있도록 콜백을 등록할 수 있습니다. 이를 위해 `Envelope` 정의에 `using` 파라미터를 추가하세요:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        using: [
            function (Email $message) {
                // ...
            },
        ]
    );
}
```

<a name="markdown-mailables"></a>
## 마크다운(Markdown) 메일러블 (Markdown Mailables)

마크다운 메일러블 메시지를 사용하면 [메일 알림(mail notifications)](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿 및 컴포넌트를 메일러블에서도 손쉽게 쓸 수 있습니다. 메시지가 마크다운 문법으로 작성되면, Laravel이 자동으로 아름답고 반응형인 HTML 템플릿을 생성하며, plain-text 버전도 함께 만듭니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성 (Generating Markdown Mailables)

마크다운 템플릿이 포함된 메일러블을 생성하려면, `make:mail` Artisan 명령어에 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그 다음, 해당 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용해 Content를 정의하세요:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        markdown: 'mail.orders.shipped',
        with: [
            'url' => $this->orderUrl,
        ],
    );
}
```

<a name="writing-markdown-messages"></a>
### 마크다운 메일 메시지 작성 (Writing Markdown Messages)

마크다운 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합해 이메일을 보다 쉽게 작성할 수 있습니다. Laravel의 미리 만들어진 이메일 UI 컴포넌트도 그대로 활용할 수 있습니다:

```blade
<x-mail::message>
# Order Shipped

Your order has been shipped!

<x-mail::button :url="$url">
View Order
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

> [!NOTE]
> 마크다운 이메일을 작성할 때 과도한 들여쓰기는 사용하지 마세요. 마크다운 표준에 따라, 들여쓰기가 많으면 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url`(필수), `color`(선택: `primary`, `success`, `error`) 두 개의 인자를 받을 수 있습니다. 버튼은 원하는 만큼 메일에 여러 개 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 일반 메일 내용과 다른 배경색 패널로 감싸 강조합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환해줍니다. 마크다운의 기본 테이블 정렬 문법도 지원합니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징 (Customizing the Components)

Laravel의 마크다운 이메일 컴포넌트 전체를 애플리케이션에서 커스터마이즈할 수 있도록 내보낼 수 있습니다. `vendor:publish` Artisan 명령어로 `laravel-mail` 에셋 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

위 명령을 실행하면 `resources/views/vendor/mail` 디렉토리 하위에 마크다운 컴포넌트가 export됩니다. 이 디렉토리엔 `html`, `text` 디렉토리가 있으며, 각각 모든 컴포넌트의 HTML 및 텍스트 표현이 들어 있습니다. 이들 컴포넌트를 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 export 후, `resources/views/vendor/mail/html/themes` 디렉토리에 `default.css` 파일이 생성됩니다. 이 CSS를 수정하면, 해당 스타일이 HTML 이메일 본문에 자동으로 인라인 스타일로 삽입되어 적용됩니다.

마크다운 컴포넌트용 새로운 테마를 만들고 싶다면, CSS 파일을 `html/themes` 디렉토리에 추가하고, `config/mail.php` 설정 파일의 `theme` 옵션을 새 테마명으로 변경하면 됩니다.

특정 메일러블에서 개별적으로 테마를 커스터마이즈하려면, 메일러블 클래스의 `$theme` 프로퍼티에 사용하고자 하는 테마 이름을 지정하세요.

<a name="sending-mail"></a>
## 메일 발송 (Sending Mail)

메일 발송은 `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to`에는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션을 전달할 수 있습니다. 객체나 컬렉션을 전달할 경우, 해당 객체에 `email`, `name` 속성이 있어야 하며, 메일러가 자동으로 수신자를 결정합니다. 수신자가 정해지면, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하기만 하면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Mail\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Ship the order...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

메일 발송 시 "to"뿐만 아니라 "cc", "bcc" 등 모든 형태의 수신자도 지정할 수 있습니다. 해당 메서드들을 체이닝해서 사용하면 됩니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

배열 형태로 여러 수신자에게 메일러블을 개별 발송해야 하는 경우, `to` 메서드는 반복 호출마다 기존 수신자 목록에 이메일을 추가하므로, 반복문 내에서 각 수신자별로 항상 새로운 메일러블 인스턴스를 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

Laravel은 기본적으로 `mail` 설정 파일의 `default`로 지정된 메일러를 사용하지만, `mailer` 메서드로 특정 메일러를 지정해 메일을 발송할 수 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 대기열 처리 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 대기열 처리

이메일 발송은 애플리케이션 응답 시간에 부정적인 영향을 줄 수 있으므로, 많은 개발자들이 이메일 전송을 백그라운드 작업으로 대기열 처리합니다. Laravel에서는 [통합 대기열 API](/docs/12.x/queues)를 통해서 이를 쉽게 할 수 있습니다. 메일 대기열 처리는 `Mail` 파사드의 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 대기열에 작업을 등록하여, 메일이 백그라운드에서 발송되도록 처리합니다. 사용 전 [대기열을 반드시 설정](/docs/12.x/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 발송 처리

대기열에 올린 이메일의 발송을 일정 시간 이후로 지연하고 싶다면, `later` 메서드를 사용하세요. 첫 번째 인자로 메일 발송 시점을 나타내는 `DateTime` 인스턴스를 전달하면 됩니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐(Queue)에 작업 넣기

`make:mail` 명령으로 생성한 모든 메일러블 클래스에는 `Illuminate\Bus\Queueable` 트레이트가 포함되어 있으므로, 어떤 메일러블 인스턴스이든 `onQueue`, `onConnection` 메서드를 사용하여 큐 연결 및 큐 이름을 지정할 수 있습니다:

```php
$message = (new OrderShipped($order))
    ->onConnection('sqs')
    ->onQueue('emails');

Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue($message);
```

<a name="queueing-by-default"></a>
#### 항상 기본적으로 대기열 처리하기

항상 대기열로 처리하고 싶은 메일러블 클래스가 있다면, 해당 클래스에서 `ShouldQueue` 계약(Contract)을 구현하면 됩니다. `send` 메서드로 발송해도 자동으로 대기열에 등록됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 대기열 메일러블과 데이터베이스 트랜잭션

대기열 메일러블을 데이터베이스 트랜잭션 내에서 디스패치하면, 큐에서 작업을 처리할 때 아직 트랜잭션이 커밋되지 않았을 수 있습니다. 이 경우, 트랜잭션 중 수정된 모델/레코드가 데이터베이스에는 아직 반영되지 않았을 수 있고, 트랜잭션 내에서 새로 생성된 레코드는 데이터베이스에 없을 수 있습니다. 메일러블이 이런 모델에 의존한다면, 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 경우, 메일러블 발송 시 `afterCommit` 메서드를 호출하여 모든 데이터베이스 트랜잭션이 커밋된 이후 작업이 실행되도록 할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 메일러블 생성자에서 `afterCommit`을 호출할 수도 있습니다:

```php
<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable implements ShouldQueue
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 위와 같은 문제에 대한 자세한 해결책은, [대기열 작업과 데이터베이스 트랜잭션 관련 문서](/docs/12.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="queued-email-failures"></a>
#### 대기열 메일 발송 실패 처리

대기열 이메일 발송이 실패하면, 메일러블 클래스에 `failed` 메서드를 정의한 경우 해당 메서드가 호출됩니다. 이때, 실패 원인이 된 `Throwable` 인스턴스가 전달됩니다:

```php
<?php

namespace App\Mail;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Throwable;

class OrderDelayed extends Mailable implements ShouldQueue
{
    use SerializesModels;

    /**
     * Handle a queued email's failure.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링 (Rendering Mailables)

이메일을 전송하지 않고 메일러블의 HTML 내용을 그대로 가져오고 싶을 때가 있습니다. 이때는 메일러블의 `render` 메서드를 사용하세요. 해당 메서드는 평가된 HTML 내용을 문자열로 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 미리보기 (Previewing Mailables in the Browser)

메일러블 템플릿을 작업할 때는, 메일을 실제 이메일로 보내기 전에 바로 브라우저로 렌더링해 미리보는 것이 편리합니다. 이를 위해, 라우트 클로저나 컨트롤러에서 메일러블을 반환하면 해당 메일러블이 브라우저에서 바로 렌더링되어 디자인을 빠르게 확인할 수 있습니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 지역화 (Localizing Mailables)

Laravel에서는 메일러블을 현재 요청의 언어(locale)와 다른 언어로 보낼 수 있으며, 이 메일이 대기열 처리되는 경우에도 해당 언어를 기억합니다.

이를 위해 `Mail` 파사드에서 `locale` 메서드로 사용할 언어를 지정할 수 있습니다. 메일러블의 템플릿을 평가할 때 지정된 언어로 전환했다가, 평가가 끝나면 원래 언어로 돌아갑니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 언어 지원

애플리케이션이 각 사용자의 선호 언어 정보를 저장하는 경우가 있습니다. 모델에서 `HasLocalePreference` 계약을 구현하면, 메일 발송 시 이 언어가 자동으로 적용됩니다:

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

이 인터페이스를 구현하면, 메일러블이나 알림을 보낼 때 자동으로 해당 선호 언어가 사용되므로 `locale` 메서드를 따로 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트 (Testing Mailable Content)

Laravel은 메일러블의 구조를 검사할 다양한 메서드를 제공합니다. 또한, 메일러블이 예상하는 내용을 갖고 있는지도 손쉽게 테스트할 수 있습니다:

```php tab=Pest
use App\Mail\InvoicePaid;
use App\Models\User;

test('mailable content', function () {
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
});
```

```php tab=PHPUnit
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content(): void
{
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
}
```

"HTML" 관련 assert 메서드는 HTML 버전에 대해, "text" 관련 메서드는 plain-text 버전에 대해 해당 문자열이 포함되어 있는지 테스트합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 발송 테스트 (Testing Mailable Sending)

메일러블의 내용 검증은 메일 발송 여부와는 별도로 테스트하는 것이 좋습니다. 일반적으로 메일러블의 내용은 테스트하려는 실제 코드와 직접 관련이 없으므로, 특정 메일러블이 특정 사용자에게 "**발송되었다**"는 것만 assert 하는 것으로 충분합니다.

`Mail` 파사드의 `fake` 메서드를 사용하면 실제 메일 발송을 막아 테스트 중에만 사용 가능합니다. `fake` 호출 후에는 메일 발송 여부는 물론, 메일러블에 전달된 데이터도 검사할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // Perform order shipping...

    // Assert that no mailables were sent...
    Mail::assertNothingSent();

    // Assert that a mailable was sent...
    Mail::assertSent(OrderShipped::class);

    // Assert a mailable was sent twice...
    Mail::assertSent(OrderShipped::class, 2);

    // Assert a mailable was sent to an email address...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // Assert a mailable was sent to multiple email addresses...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // Assert a mailable was not sent...
    Mail::assertNotSent(AnotherMailable::class);

    // Assert a mailable was sent twice...
    Mail::assertSentTimes(OrderShipped::class, 2);

    // Assert 3 total mailables were sent...
    Mail::assertSentCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Mail::fake();

        // Perform order shipping...

        // Assert that no mailables were sent...
        Mail::assertNothingSent();

        // Assert that a mailable was sent...
        Mail::assertSent(OrderShipped::class);

        // Assert a mailable was sent twice...
        Mail::assertSent(OrderShipped::class, 2);

        // Assert a mailable was sent to an email address...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // Assert a mailable was sent to multiple email addresses...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // Assert a mailable was not sent...
        Mail::assertNotSent(AnotherMailable::class);

        // Assert a mailable was sent twice...
        Mail::assertSentTimes(OrderShipped::class, 2);

        // Assert 3 total mailables were sent...
        Mail::assertSentCount(3);
    }
}
```

백그라운드 대기열로 메일러블을 발송했다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등 메서드에 클로저를 전달해, 특정 조건을 만족하는 메일러블만 검증할 수도 있습니다. 조건을 만족하는 메일러블이 하나라도 있으면 assert가 통과합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

클로저로 받은 메일러블 인스턴스에는 다양한 유틸리티 메서드가 있습니다:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...') &&
           $mail->usesMailer('ses');
});
```

첨부파일에 대한 assert 메서드도 제공합니다:

```php
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```

메일이 발송되지 않았는지(혹은 큐에 등록되지 않았는지) assert하려면 `assertNotSent`, `assertNotQueued` 두 메서드가 있습니다. 둘 중 하나라도 아무 동작이 없었음을 assert하려면, `assertNothingOutgoing`, `assertNotOutgoing`를 사용할 수 있습니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

실제 이메일 주소로 메일을 보내지 않고도 메일 기능을 개발 및 테스트하고 싶은 경우가 많습니다. Laravel은 로컬 개발 환경에서 실제 이메일 발송을 "비활성화"할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 이메일을 실제로 보내지 않고, 모든 메일 메시지를 로그 파일에 기록해 확인할 수 있도록 해줍니다. 일반적으로 이 드라이버는 로컬 개발 시에만 사용합니다. 환경별로 애플리케이션 설정하는 법은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

이외에도, [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io) 등의 서비스를 사용하여 `smtp` 드라이버와 함께 "더미" 메일박스로 메시지를 보낼 수 있습니다. 이를 통해 실제 이메일 클라이언트 환경에서 최종 메일 결과를 확인할 수 있습니다.

[Laravel Sail](/docs/12.x/sail) 사용 시에는 [Mailpit](https://github.com/axllent/mailpit)에서 메시지를 미리 볼 수 있습니다. Sail이 실행 중일 때는 `http://localhost:8025`에서 Mailpit 인터페이스에 접근하면 됩니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 통해 전역 "to" 주소를 지정해 모든 메일이 특정 주소로만 발송되도록 할 수 있습니다. 이 메서드는 보통 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 일반적입니다:

```php
use Illuminate\Support\Facades\Mail;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```

`alwaysTo`를 사용하면, 메일별로 추가 지정된 "cc" 및 "bcc" 주소는 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 메시지를 보낼 때 두 가지 이벤트를 디스패치합니다. `MessageSending` 이벤트는 메시지 전송 직전에, `MessageSent` 이벤트는 메시지 전송 직후에 발생합니다. 이 이벤트들은 메일이 *전송될 때* 실행되며, 큐에 등록될 때가 아니라는 점에 유의하세요. 애플리케이션에서 [이벤트 수신기](/docs/12.x/events)를 만들어 활용할 수 있습니다:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * Handle the event.
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## 커스텀 전송 방식(Transport) (Custom Transports)

Laravel은 다양한 메일 전송 방식을 기본 지원하지만, 공식적으로 지원하지 않는 서비스도 직접 구현해 사용할 수 있습니다. 이를 위해서는 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속한 클래스를 만들고, `doSend`, `__toString` 메서드를 구현하면 됩니다:

```php
<?php

namespace App\Mail;

use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Create a new Mailchimp transport instance.
     */
    public function __construct(
        protected ApiClient $client,
    ) {
        parent::__construct();
    }

    /**
     * {@inheritDoc}
     */
    protected function doSend(SentMessage $message): void
    {
        $email = MessageConverter::toEmail($message->getOriginalMessage());

        $this->client->messages->send(['message' => [
            'from_email' => $email->getFrom(),
            'to' => collect($email->getTo())->map(function (Address $email) {
                return ['email' => $email->getAddress(), 'type' => 'to'];
            })->all(),
            'subject' => $email->getSubject(),
            'text' => $email->getTextBody(),
        ]]);
    }

    /**
     * Get the string representation of the transport.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

커스텀 전송 방식 클래스를 만들었다면, `Mail` 파사드의 `extend` 메서드로 등록할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 처리합니다. `extend`에 넘기는 클로저에는 `mail` 설정 파일의 해당 메일러 구성 배열이 `$config`로 전달됩니다:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        $client = new ApiClient;

        $client->setApiKey($config['key']);

        return new MailchimpTransport($client);
    });
}
```

커스텀 전송 방식을 등록했다면, 이 전송 방식(`transport`)을 사용하는 메일러를 `config/mail.php`의 `mailers` 배열에 추가하여 사용할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식 (Additional Symfony Transports)

Laravel은 Mailgun, Postmark 등 일부 Symfony 전송 방식을 내장 지원합니다. 그러나, 더 다양한 Symfony 전송 방식을 추가로 사용하고 싶다면, Composer로 관련 패키지를 설치하고 Laravel에 등록해 쓸 수 있습니다. 예를 들어, "Brevo"(구 Sendinblue) Symfony 메일러를 설치하려면:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, `services` 설정 파일에 Brevo API 인증 정보를 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

다음으로, `Mail` 파사드의 `extend` 메서드로 전송 방식을 등록하세요. 서비스 프로바이더의 `boot` 메서드에서 처리하면 됩니다:

```php
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('brevo', function () {
        return (new BrevoTransportFactory)->create(
            new Dsn(
                'brevo+api',
                'default',
                config('services.brevo.key')
            )
        );
    });
}
```

등록이 끝나면, 이 전송 방식을 사용하는 메일러 정의를 `config/mail.php`에 추가해 사용할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
