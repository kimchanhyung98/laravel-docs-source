# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드로빈(round robin) 설정](#round-robin-configuration)
- [메일러블 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일(Attachments)](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더(Headers)](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스텀](#customizing-the-symfony-message)
- [Markdown 메일러블](#markdown-mailables)
    - [Markdown 메일러블 생성](#generating-markdown-mailables)
    - [Markdown 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블의 로컬라이징](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 컨텐츠 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발환경](#mail-and-local-development)
- [이벤트(Events)](#events)
- [커스텀 트랜스포트(Transports)](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 깔끔하고 직관적인 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 이메일 전송을 지원하는 드라이버를 제공하여, 로컬 또는 클라우드 기반 서비스에서 빠르게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 설정된 각 메일러(mailers)는 고유한 설정과 고유한 "트랜스포트(transport)"를 가질 수 있어, 애플리케이션에서 특정 메일 메시지마다 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭션 알림 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일에는 `mailers` 설정 배열이 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버/트랜스포트별 샘플 설정이 포함되어 있습니다. `default` 설정 값은 애플리케이션이 이메일을 전송할 때 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비 사항 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 SMTP 서버를 이용하는 것보다 더 간단하고 빠를 수 있습니다. 가능하다면 이러한 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 두 가지 변경을 해야 합니다. 먼저 기본 메일러를 `mailgun`으로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그 다음, 다음 설정 배열을 `mailers` 배열에 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러 설정을 완료한 후, `config/services.php` 파일에 다음 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국이 아닌 [Mailgun 리전](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용한다면, `services` 파일에서 해당 리전의 엔드포인트를 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `postmark`로 지정합니다. 이후, `config/services.php` 파일에 아래 옵션이 포함되어 있는지 확인하세요:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하려면, 메일러 설정 배열에 `message_stream_id` 옵션을 추가하세요(`config/mail.php`):

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이 방식으로 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer로 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `resend`로 지정합니다. 그리고 `config/services.php` 파일에 아래 옵션이 포함되어 있는지 확인하세요:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer로 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일의 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 아래 옵션이 포함되어 있는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면 SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능(subscription management)](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환되는 배열에 `X-Ses-List-Management-Options` 헤더를 추가할 수 있습니다:

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

Laravel이 이메일 전송 시 AWS SDK의 `SendEmail` 메서드에 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 전달하도록 하려면, `ses` 설정 내에 `options` 배열을 정의할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스를 제공하며, Laravel용 API 기반 메일 드라이버 패키지를 직접 관리합니다. Composer로 아래 패키지를 설치하세요:

```shell
composer require mailersend/laravel-driver
```

패키지 설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가합니다. 또한, `MAIL_MAILER` 환경 변수는 `mailersend`로 지정해야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php` 파일의 `mailers` 배열에 MailerSend 를 추가하세요:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend에 대해 더 자세히 알고 싶거나 호스티드 템플릿 사용법이 궁금하다면 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정

외부 메일 서비스가 다운되는 경우가 있을 수 있습니다. 이런 상황에서 주 메일 드라이버가 다운됐을 때 사용할 백업 메일 전송 설정을 하나 이상 정의하는 것이 유용할 수 있습니다.

이를 위해서는, `mail` 설정 파일에서 `failover` 트랜스포트를 사용하는 메일러를 정의합니다. 이 설정 배열에는 사용할 메일러들의 이름을 순서대로 나열합니다:

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

`failover` 메일러를 정의한 후에는 `mail` 설정 파일의 `default` 키에 해당 메일러 이름을 지정하여 기본 메일러로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드로빈(round robin) 설정

`roundrobin` 트랜스포트는 메일 발송 업무를 여러 메일러에 분산할 수 있게 해줍니다. 먼저, `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의하세요. 이 설정 배열에는 사용할 메일러들을 나열합니다:

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

`roundrobin` 메일러를 정의한 후, `default` 설정에 해당 메일러 이름을 넣어 기본 메일러로 사용할 수 있습니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 트랜스포트는 설정한 메일러 중 무작위로 하나를 선택하고, 이후 각 이메일마다 순차적으로 다음 메일러로 바꿔가며 전송합니다. `failover` 트랜스포트가 *[고가용성](https://en.wikipedia.org/wiki/High_availability)* 을 위한 것이라면, `roundrobin` 트랜스포트는 *[로드 밸런싱(부하 분산)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성 (Generating Mailables)

Laravel에서 각 이메일 유형은 "메일러블(mailable)" 클래스 형태로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, 아래와 같이 `make:mail` Artisan 명령어로 처음 메일러블 클래스를 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 파일을 열어 내용을 확인해보세요. 메일러블 클래스의 설정은 여러 메서드(`envelope`, `content`, `attachments` 등)를 통해 이뤄집니다.

`envelope` 메서드는 메시지의 제목 및(경우에 따라) 수신자를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성하는 데 사용할 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope로 설정하기

이메일의 발신자를 설정하는 방법부터 살펴보겠습니다. 즉, 이메일이 누구로부터 오는지 지정하는 것입니다. 발신자 설정에는 두 가지 방법이 있습니다. 첫 번째는 메시지의 envelope에 "from" 주소를 지정하는 것입니다:

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
#### 글로벌 `from` 주소 사용

애플리케이션이 모든 이메일에서 동일한 "from" 주소를 사용한다면, 메일러블 클래스마다 개별 지정하는 대신 `config/mail.php` 파일에 글로벌 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 별도 설정이 없을 경우 이 주소가 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, 글로벌 "reply_to" 주소도 설정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드 내에서 뷰를 지정할 수 있습니다. 즉, 이메일 내용 렌더링에 사용할 템플릿을 설정합니다. 각각의 이메일은 보통 [Blade 템플릿](/docs/12.x/blade)을 사용하므로, Blade 템플릿 엔진의 모든 기능을 자유롭게 활용할 수 있습니다:

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
> 모든 이메일 템플릿을 보관할 `resources/views/mail` 디렉터리를 생성하는 것이 좋지만, 실제 사용 위치는 `resources/views` 내에 자유롭게 정할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일(Plain Text Emails)

이메일의 일반 텍스트 버전을 정의하고 싶을 때는, 메시지의 `Content` 정의에서 plain-text 템플릿을 지정할 수 있습니다. `view`와 마찬가지로 `text` 파라미터에도 템플릿명을 지정하세요. HTML 버전과 plain-text 두 가지 모두를 정의할 수 있습니다:

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

더 명확하게 하고 싶다면, `html` 파라미터를 `view` 파라미터의 별칭으로 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성으로 전달

이메일 렌더링 시에 사용할 데이터를 뷰에 전달하려면 두 가지 방법이 있습니다. 첫 번째는, 메일러블 클래스의 public 속성에 데이터를 할당하는 것입니다. 클래스의 생성자에서 데이터를 전달받아 public 속성으로 지정하면, 해당 데이터가 자동으로 뷰에서 사용 가능합니다:

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

public 속성에 저장된 데이터는 Blade 템플릿에서 다음과 같이 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터로 전달

이메일 데이터를 뷰에 전달하기 전에 포맷을 직접 커스터마이즈하고 싶다면, `Content` 정의의 `with` 파라미터로 데이터 배열을 직접 넘길 수 있습니다. 이 경우 생성자에서는 protected 혹은 private 속성에 데이터를 저장해야 템플릿에 자동 공개되지 않습니다:

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

이렇게 전달한 데이터도 Blade 템플릿에서 다음과 같이 쉽게 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일(Attachments)

이메일에 첨부파일을 추가하려면, 메일러블의 `attachments` 메서드에서 반환하는 배열에 첨부파일을 등록하면 됩니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달하여 첨부할 수 있습니다:

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

디스플레이 이름이나 MIME 타입도 `as`, `withMime` 메서드로 지정 가능하며, 둘 다 생략해도 됩니다:

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
#### 디스크에서 파일 첨부

[파일시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 이메일에 첨부하려면, `fromStorage` 메서드를 사용합니다:

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

첨부파일의 이름이나 MIME 타입도 함께 지정할 수 있습니다:

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

기본 디스크가 아닌 특정 저장소 디스크를 지정하려면 `fromStorageDisk`를 사용합니다:

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
#### Raw 데이터 첨부

`fromData` 메서드를 사용하면 바이트 문자열(예: 메모리 내 PDF 등)을 파일로 저장하지 않고 직접 첨부할 수 있습니다. 이때 클로저로 raw 데이터와 파일명을 전달합니다:

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
### 인라인 첨부파일(Inline Attachments)

이메일에 인라인 이미지를 삽입하는 것은 보통 까다롭지만, Laravel은 이를 쉽게 할 수 있게 해줍니다. 이메일 템플릿 안에서 `$message` 변수에 제공된 `embed` 메서드를 사용하여 인라인 이미지를 집어넣을 수 있습니다. `$message`는 모든 이메일 템플릿에서 자동으로 사용할 수 있습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에서는 사용할 수 없습니다. plain-text 메일은 인라인 첨부파일 기능을 지원하지 않습니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

raw 이미지 데이터 문자열이 있다면 `$message->embedData` 메서드를 사용하여 인라인 이미지로 삽입할 수 있습니다. 이때 파일명도 반드시 전달해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

파일 경로 문자열로 첨부하는 것이 대부분이지만, 애플리케이션 내에서 첨부 대상이 객체(예: 첨부용 Photo 모델)일 수 있습니다. 이럴 때 attachable 객체를 만들어 손쉽게 첨부할 수 있습니다.

먼저, 첨부할 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 이 인터페이스는 `toMailAttachment` 메서드를 정의하고, 이는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

이제 메일러블의 `attachments` 메서드에서 해당 객체 인스턴스를 반환하면 자동으로 첨부됩니다:

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

첨부 데이터가 Amazon S3와 같은 원격 파일 스토리지에 있다면, [파일시스템 디스크](/docs/12.x/filesystem)를 활용해 첨부 인스턴스를 생성할 수도 있습니다:

```php
// 기본 디스크에서 파일 첨부
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일 첨부
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 있는 데이터로부터도 첨부 인스턴스를 만들 수 있습니다. 이 경우, `fromData` 메서드에 raw 데이터를 반환하는 클로저를 전달하세요:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일 이름이나 MIME 타입을 커스터마이즈하고 싶다면 `as`, `withMime` 메서드를 사용할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더(Headers)

경우에 따라 이메일에 추가 헤더(예: custom `Message-Id`나 기타 텍스트 헤더)를 붙여야 할 수 있습니다.

이를 위해 메일러블에서 `headers` 메서드를 정의하고, `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하세요. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받으며, 필요한 것만 제공하면 됩니다:

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
### 태그와 메타데이터(Tags and Metadata)

Mailgun, Postmark 등 일부 외부 이메일 서비스는 메시지별 "태그"와 "메타데이터"를 지원하여, 메일 그룹화와 추적 등에 사용할 수 있습니다. Envelope 정의에 태그와 메타데이터를 추가할 수 있습니다:

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

Mailgun 드라이버를 사용한다면 [Mailgun 태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) 문서를( 참고하시고, Postmark는 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 문서를 참고하세요.

Amazon SES로 메일을 보내는 경우, [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙이려면 `metadata` 메서드를 사용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스텀(Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer에 기반합니다. Laravel은 메시지 전송 전에 Symfony Message 인스턴스에 호출할 커스텀 콜백을 등록할 수 있게 해줍니다. 이로써 실제 전송 직전 메시지를 더 깊이 커스터마이즈할 수 있습니다. Envelope 정의에 `using` 파라미터를 추가하면 됩니다:

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
## Markdown 메일러블 (Markdown Mailables)

Markdown 메일러블 메시지는 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있게 해줍니다. 메시지를 Markdown으로 작성하면, Laravel이 아름답고 반응형인 HTML 템플릿을 자동으로 렌더링하고, plain-text 버전도 자동 생성합니다.

<a name="generating-markdown-mailables"></a>
### Markdown 메일러블 생성

Markdown 템플릿과 함께 메일러블을 생성하려면, `make:mail` Artisan 명령어의 `--markdown` 옵션을 사용합니다:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, 해당 클래스의 `content` 메서드에서 Content 정의에 `markdown` 파라미터를 사용하세요:

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
### Markdown 메시지 작성

Markdown 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합하여, 쉽고 간결하게 메일 메시지를 생성하면서 Laravel의 기본 이메일 UI 컴포넌트를 활용할 수 있게 해줍니다:

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
> Markdown 이메일을 작성할 때 불필요한 들여쓰기는 사용하지 마세요. Markdown 표준에 따라, 들여쓰기는 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트(Button Component)

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적 `color` 인자를 받습니다. 지원 색상은 `primary`, `success`, `error`입니다. 여러 개의 버튼을 한 메시지에 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트(Panel Component)

패널 컴포넌트는 주어진 텍스트 블록을 메시지의 다른 부분과 구분되는 배경색 위에 표시합니다. 이를 통해 특정 메시지 부분에 시선을 끌 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트(Table Component)

테이블 컴포넌트를 사용하면 Markdown 테이블을 HTML 테이블로 변환할 수 있습니다. 이때 컬럼 정렬은 Markdown 표준 문법을 따릅니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈(Customizing the Components)

Markdown 메일 컴포넌트 전체를 직접 커스터마이즈하려면, `vendor:publish` Artisan 명령어로 `laravel-mail` 에셋을 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면, Markdown 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 퍼블리시됩니다. 이 `mail` 디렉터리에는 각각의 HTML 및 텍스트 버전이 존재하므로, 자유롭게 커스터마이즈할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 퍼블리시한 후에는 `resources/views/vendor/mail/html/themes` 디렉터리의 `default.css` 파일에서 CSS를 커스터마이즈할 수 있습니다. 이 파일을 수정하면, 스타일이 자동으로 이메일 HTML에 inline 스타일로 변환 적용됩니다.

Laravel Markdown 컴포넌트에 완전히 새로운 테마를 적용하려면, 새 CSS 파일을 `html/themes` 디렉터리에 추가한 뒤, `config/mail.php` 설정 파일의 `theme` 옵션을 새 테마 이름으로 지정하세요.

특정 메일러블에서만 다른 테마를 사용하고 싶다면, 메일러블 클래스의 `$theme` 속성을 해당 테마명으로 설정하면 됩니다.

<a name="sending-mail"></a>
## 메일 전송 (Sending Mail)

메시지를 전송하려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 인자로 받을 수 있습니다. 객체나 객체 컬렉션을 넘기면, 메일러가 자동으로 해당 객체에 정의된 `email`과 `name` 속성을 참조하므로, 반드시 해당 속성이 존재해야 합니다. 수신자를 정한 후에는, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하면 됩니다:

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

메시지 전송 시 "to" 뿐만 아니라 "cc", "bcc" 수신자도 각각의 메서드를 체이닝하여 동시에 지정할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자에게 반복 전송

여러 명에게 반복해서 메일러블을 보내야 할 경우, 주의해야 할 점이 있습니다. `to` 메서드는 이전 수신자 리스트에 계속 추가하는 방식이므로, 루프에서 같은 메일러블 인스턴스를 재사용하면 이전 수신자들에게도 중복 발송됩니다. 따라서 반드시 수신자마다 메일러블 인스턴스를 새로 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 통한 메일 전송

Laravel은 기본적으로 `mail` 설정 파일의 `default` 메일러를 사용하여 이메일을 전송합니다. 특정 메일러를 통해 메일을 보내고 싶다면 `mailer` 메서드를 사용하면 됩니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉(Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송 때문에 애플리케이션 응답 속도가 느려지는 것을 방지하려면, 메일을 백그라운드에서 큐로 처리하는 것이 좋습니다. Laravel은 내장된 [통합 큐 API](/docs/12.x/queues)로 이 과정을 쉽게 처리할 수 있습니다. 메일 큐잉은 수신자 지정 후, `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 기능을 사용하기 전에 [큐 설정](/docs/12.x/queues)을 완료해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연된(Delayed) 메일 메시지 큐잉

큐에 올라간 메일의 전송 시점을 지연하려면, `later` 메서드를 사용하세요. 첫 번째 인자로 전송 시각(`DateTime` 인스턴스)을 전달합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 전송

`make:mail`로 생성한 모든 메일러블 클래스에는 `Illuminate\Bus\Queueable` 트레이트가 포함되므로, 인스턴스에서 `onQueue`와 `onConnection` 메서드를 사용해 사용할 큐 이름과 연결(connection)을 지정할 수 있습니다:

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
#### 항상 큐잉하기

항상 큐를 통해 전송하고 싶은 메일러블 클래스가 있다면, 클래스에 `ShouldQueue` 계약을 구현하세요. 이 경우 `send` 메서드를 호출하더라도 항상 큐잉됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐된 메일러블과 데이터베이스 트랜잭션

큐에 올라간 메일러블이 데이터베이스 트랜잭션 내에서 디스패치되면, 큐 워커가 트랜잭션 커밋 이전에 작업을 처리할 수 있습니다. 이 경우, 트랜잭션 내에서 수정된 모델이나 레코드가 아직 반영되지 않았거나, 트랜잭션이 끝나기 전에는 새로 생성된 레코드가 존재하지 않을 수 있습니다. 메일러블이 트랜잭션 내에서 생성하거나 수정된 데이터에 의존한다면, 작업 처리 중 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`로 되어 있을 때도, 특정 메일러블만이라도 트랜잭션 커밋 후에만 실행되게 하려면, 전송 시에 `afterCommit` 메서드를 호출하세요:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 메일러블 생성자에서 `afterCommit` 메서드를 호출할 수 있습니다:

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
> 관련 문제를 우회하는 방법 등 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐된 이메일 전송 실패

큐된 이메일 전송이 실패하면, 해당 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 실패를 일으킨 `Throwable` 인스턴스가 `failed` 메서드로 전달됩니다:

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

이메일을 실제로 전송하지 않고, 메일러블의 HTML 컨텐츠만 따로 얻고 싶을 때가 있습니다. 이럴 때는 메일러블 인스턴스에서 `render` 메서드를 호출하면, 평가된 HTML 문자열이 반환됩니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인할 때, Blade 템플릿처럼 브라우저에서 바로 결과를 확인하며 작업하면 매우 편리합니다. Laravel에서는 라우트 클로저나 컨트롤러에서 메일러블을 반환하면, 해당 메일러블이 HTML로 렌더링되어 브라우저에 표시됩니다. 실제 이메일 주소로 전송할 필요 없이 바로 디자인을 확인할 수 있습니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블의 로컬라이징 (Localizing Mailables)

Laravel은 메일러블을 현재 요청의 로케일(locale)과 다르게 전송할 수 있으며, 큐에 넣어도 이 로케일을 기억합니다.

이를 위해, `Mail` 파사드는 원하는 언어로 전환할 수 있는 `locale` 메서드를 제공합니다. 메일러블의 템플릿이 평가되는 동안 지정한 로케일로 변경되었다가, 평가가 끝나면 다시 원래 로케일로 돌아갑니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 기본 로케일(User Preferred Locales)

사용자마다 선호하는 로케일을 따로 저장하는 경우, 모델에 `HasLocalePreference` 계약을 구현하면 Laravel이 자동으로 이 정보를 사용합니다:

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

인터페이스를 구현하면, Laravel은 메일러블이나 알림을 보낼 때 자동으로 해당 사용자의 선호 로케일을 사용합니다. 따라서 이런 경우에는 별도로 `locale` 메서드를 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 컨텐츠 테스트(Testing Mailable Content)

Laravel은 메일러블의 구조를 점검할 수 있는 다양한 메서드를 제공합니다. 또한 기대한 컨텐츠가 포함됐는지 편리하게 테스트할 수 있는 메서드도 있습니다:

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

"HTML" 어서션은 메일러블의 HTML 버전에서 문자열이 포함됨을 확인하고, "text" 어서션은 plain-text 버전에서 해당 내용을 확인합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트(Testing Mailable Sending)

메일러블의 내용 자체 테스트와 메일이 특정 사용자에게 실제로 전송되었는지의 테스트는 분리하는 것이 좋습니다. 보통 메일러블 내용은 검증 대상 코드의 핵심 요소가 아니므로, Laravel이 메일러블을 전송하도록 명령만 했는지 확인하는 것으로 충분합니다.

`Mail` 파사드의 `fake` 메서드를 사용하면 실제 메일 전송을 막고, 어떤 메일러블이 누구에게 전송되었는지 어서션으로 쉽게 테스트할 수 있습니다:

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

백그라운드 작업 큐로 메일러블을 전송한다면 `assertSent` 대신 `assertQueued`를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued`에 클로저를 인자로 전달하여, 특정 조건을 만족하는 메일러블만 전송(혹은 전송되지 않음)을 assert할 수도 있습니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

한편, 어서션 메서드에서 제공하는 메일러블 인스턴스는 메일 본문, 수신자, 첨부파일 등 다양하게 점검할 수 있는 메서드가 존재합니다:

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

첨부파일도 다음과 같이 어서트할 수 있습니다:

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

메일이 **전송도, 큐잉도** 되지 않았는지 확인할 때는 `assertNothingOutgoing`과 `assertNotOutgoing` 메서드를 활용하세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발환경 (Mail and Local Development)

애플리케이션 개발 시 실제 이메일을 전송하고 싶지 않을 때가 있습니다. Laravel은 로컬 개발 중에 실제 메일 전송을 "비활성화"시킬 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버(Log Driver)

이메일을 실제로 보내는 대신, 로그 메일 드라이버(`log`)를 사용하면 모든 메일 메시지가 로그 파일에 기록되어 확인할 수 있습니다. 이 드라이버는 보통 로컬 개발 환경에만 사용됩니다. [환경별 설정](/docs/12.x/configuration#environment-configuration) 문서에서 자세한 내용을 확인하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

다른 방법으로 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)과 같은 서비스 또는 SMTP 드라이버를 이용해 "더미" 메일박스에 이메일을 보낼 수 있습니다. 이를 통해 실제 이메일 클라이언트처럼 메일을 확인할 수 있으므로, 최종 이메일이 어떻게 보일지 직접 점검할 수 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용하고 있다면, [Mailpit](https://github.com/axllent/mailpit)을 이용해 메일을 미리볼 수 있습니다. Sail이 실행 중일 때, `http://localhost:8025`에서 Mailpit 인터페이스를 확인하세요.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 호출해 전 애플리케이션 메일 전송 대상 주소를 고정시킬 수 있습니다. 보통 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

<a name="events"></a>
## 이벤트(Events)

Laravel은 메일 메시지를 전송할 때 두 가지 이벤트를 발생시킵니다. `MessageSending` 이벤트는 전송 전에, `MessageSent` 이벤트는 전송 후에 발생합니다. 이 이벤트들은 메일이 "*전송될 때*" 발생하며, 큐에 등록될 때가 아니라는 점을 기억하세요. [이벤트 리스너](/docs/12.x/events)를 애플리케이션에 자유롭게 등록할 수 있습니다:

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
## 커스텀 트랜스포트(Custom Transports)

Laravel은 다양한 메일 트랜스포트를 지원하지만, 지원되지 않는 서비스로 메일을 전송하려면 직접 트랜스포트를 구현할 수 있습니다. 먼저 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 새 클래스를 정의하고, `doSend`, `__toString` 메서드를 구현하세요:

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

커스텀 트랜스포트를 만들었다면, `Mail` 파사드의 `extend` 메서드로 등록하세요. 주로 `AppServiceProvider`의 `boot` 메서드에서 처리하며, 콜백에 `$config` 배열이 전달됩니다. 이 배열에는 `config/mail.php`의 해당 메일러 설정이 담깁니다:

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

등록을 완료했다면, `config/mail.php` 파일에 새 트랜스포트를 사용하는 메일러 정의를 추가하세요:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

Laravel은 Mailgun, Postmark 등 기존의 여러 Symfony 유지 트랜스포트를 지원합니다. 이 밖에 추가로 Symfony 유지 트랜스포트를 쓰고자 한다면, Composer로 트랜스포트를 설치한 뒤 Laravel에 등록할 수 있습니다. 예를 들어, "Brevo"(이전 Sendinblue) 트랜스포트를 설치하고 등록하는 방법은 다음과 같습니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지 설치 후, `services` 설정 파일에 Brevo API 자격 정보를 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그리고 서비스 프로바이더의 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드로 등록하세요:

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

등록을 마쳤으면, `config/mail.php` 파일에 새 트랜스포트를 사용하는 메일러 정의를 추가하세요:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```