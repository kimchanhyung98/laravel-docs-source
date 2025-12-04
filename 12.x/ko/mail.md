# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [장애 시 대체 설정](#failover-configuration)
    - [라운드로빈 설정](#round-robin-configuration)
- [메일러블 클래스 생성](#generating-mailables)
- [메일러블 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일 추가](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony Message 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 다국어 지원](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송방식(Transport)](#custom-transports)
    - [추가 Symfony 전송방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 깔끔하고 직관적인 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail` 등 다양한 전송방식(드라이버)을 지원하므로, 로컬 또는 클라우드 기반 서비스를 통해 손쉽게 이메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일 내에서 각 메일러는 고유한 설정과 전송방식(transport, 드라이버)을 가질 수 있으므로, 여러 가지 이메일 서비스를 조합하여 특정 이메일을 보낼 수 있습니다. 예를 들어, Postmark로 트랜잭션(개별) 메일을, Amazon SES로 대량 메일을 보낼 수 있습니다.

`mail` 설정 파일 내부의 `mailers` 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송방식에 대한 샘플 설정이 포함되어 있습니다. `default` 값은 애플리케이션에서 이메일을 보낼 때 기본적으로 사용될 메일러를 정의합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송방식 사전 준비 사항 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend 같은 API 기반 드라이버는 SMTP 서버를 통한 메일 발송보다 더 간단하고 빠른 경우가 많습니다. 가능하다면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 전송 패키지를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 후, 애플리케이션의 `config/mail.php` 파일에서 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 다음 설정을 추가하십시오:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이제 애플리케이션의 기본 메일러가 설정되었으니, `config/services.php` 파일에도 아래 옵션을 추가해야 합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 이외의 [Mailgun region](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하는 경우, `services` 설정 파일에 해당 지역의 endpoint를 지정해줘야 합니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 전송 패키지를 설치해야 합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php` 파일의 `default` 옵션을 `postmark`로 설정하고, `config/services.php` 파일에 아래와 같이 옵션을 추가합니다:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하고 싶다면, 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

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

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer를 통해 Resend의 PHP SDK를 설치합니다:

```shell
composer require resend/resend-php
```

그리고 `config/mail.php` 파일의 `default` 옵션을 `resend`로 설정합니다. 그 다음 `config/services.php` 파일에 아래 옵션을 추가해야 합니다:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하기 위해서는 먼저 Amazon AWS SDK for PHP 라이브러리를 설치해야 합니다. Composer를 사용하여 설치하세요:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일의 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 아래 옵션을 반드시 포함해야 합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격증명(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) 사용 시, `token` 키를 SES 설정에 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환하도록 설정할 수 있습니다:

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

Laravel이 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하고 싶다면, `ses` 설정에 `options` 배열을 넣을 수 있습니다:

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

<a name="failover-configuration"></a>
### 장애 시 대체 설정 (Failover Configuration)

외부 이메일 서비스가 일시적으로 장애가 발생할 수 있습니다. 이때, 1차 메일 전송 드라이버가 동작하지 않을 경우를 대비해 하나 이상의 백업(대체) 메일 전송 구성을 정의하는 것이 좋습니다.

이를 위해, `config/mail.php` 파일에 `failover` 전송방식을 사용하는 메일러를 정의하세요. 이 메일러의 설정 배열에는 메일러의 선택 순서를 지정하는 `mailers` 배열이 포함되어야 합니다:

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

이제 `.env` 파일에서 기본 메일러를 `failover`로 지정하면 장애 시 자동으로 대체 설정이 동작합니다:

```ini
MAIL_MAILER=failover
```

<a name="round-robin-configuration"></a>
### 라운드로빈 설정 (Round Robin Configuration)

`roundrobin` 전송방식은 여러 메일러 간에 메일 발송 작업을 분산(로드 밸런싱)할 수 있도록 해줍니다. 우선, `config/mail.php` 파일에 `roundrobin` 전송방식을 사용하는 메일러를 정의해야 합니다. 이 설정 배열에는 발송에 사용할 메일러 목록을 `mailers` 배열에 지정합니다:

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

`roundrobin` 메일러가 정의되면, 기본 메일러로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 전송방식은 등록된 메일러 중 랜덤으로 하나를 고른 뒤, 이후 이메일마다 다음 메일러로 순차적으로 전환하여 발송합니다. `failover`가 *[고가용성(High Availability)](https://en.wikipedia.org/wiki/High_availability)*을 제공하는 반면, `roundrobin`은 *[부하 분산(Load Balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 기능을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 클래스 생성 (Generating Mailables)

Laravel에서 애플리케이션이 발송하는 각 이메일 유형은 "메일러블(mailable)" 클래스 하나로 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 이 디렉토리가 없다면, 첫 메일러블 클래스를 Artisan `make:mail` 명령어로 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 클래스 작성 (Writing Mailables)

메일러블 클래스를 만들었다면, 클래스 내부를 살펴보겠습니다. 메일러블 클래스는 주로 `envelope`, `content`, `attachments` 메서드를 통해 설정합니다.

`envelope` 메서드는 메시지의 제목(subject)과 때로는 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope를 이용한 설정

이메일의 발송자를 설정하는 방법을 살펴보겠습니다. 즉, 이메일의 "from" 주소를 지정하는 방법입니다. 발신자 정보는 다음 두 가지 방식 중 하나로 정의할 수 있습니다. 첫 번째는 메시지의 envelope에 "from" 주소를 지정하는 것입니다:

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

만약 애플리케이션의 모든 이메일에서 동일한 "from" 주소를 사용한다면, 매번 메일러블 클래스에 추가하는 것이 번거로울 수 있습니다. 이럴 때는 `config/mail.php` 파일에서 전역 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 별도로 "from" 주소를 지정하지 않았다면 이 전역 설정이 적용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

추가로, 전역 "reply_to" 주소도 설정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서는 이메일 내용 렌더링에 사용할 `view`(템플릿)를 정의합니다. 각각의 이메일은 보통 [Blade 템플릿](/docs/12.x/blade)을 사용하므로, Blade 템플릿 엔진의 모든 기능을 활용할 수 있습니다:

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
> 이메일 템플릿을 보관할 `resources/views/mail` 디렉토리를 만들어 관리할 것을 권장합니다. 하지만 실제로는 `resources/views` 내 원하는 위치에 자유롭게 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일 (Plain Text Emails)

이메일의 일반 텍스트 버전을 별도로 정의하려면, 메시지의 `Content` 정의 시 plain-text 템플릿을 지정할 수 있습니다. `view`와 같이, `text` 파라미터에도 템플릿 이름을 지정하세요. HTML과 텍스트 버전을 모두 정의해도 무방합니다:

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

명확성을 위해 `html` 파라미터를 `view` 대신 쓸 수도 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성 사용

일반적으로 이메일 템플릿을 렌더링할 때 사용할 데이터를 뷰에 전달하게 됩니다. 이를 위해 두 가지 방법을 사용할 수 있습니다. 첫 번째는, 메일러블 클래스의 public 속성에 데이터를 할당하는 방법입니다. 생성자에서 데이터를 받아 public 속성에 할당하면, 이 데이터는 자동으로 템플릿에서 사용할 수 있습니다:

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

데이터가 public 속성에 할당되면 Blade 템플릿에서 일반 변수처럼 쉽게 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 사용

메일 데이터의 포맷을 자유롭게 제어하고 싶을 때는, `Content` 정의의 `with` 파라미터를 통해 데이터를 수동으로 전달할 수 있습니다. 이 방식을 쓸 때는 데이터를 생성자에서 받아 메일러블 클래스의 `protected`나 `private` 속성에 할당한 뒤, 템플릿에는 자동 노출되지 않도록 합니다:

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

이렇게 데이터를 전달하면 Blade 템플릿에서 전달된 변수로 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일 추가 (Attachments)

이메일에 첨부파일을 추가하려면, 메시지의 `attachments` 메서드에서 반환하는 배열에 첨부파일을 추가하면 됩니다. 우선, 파일 경로를 `Attachment` 클래스의 `fromPath` 메서드에 전달해서 첨부할 수 있습니다:

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

첨부파일을 추가할 때, 표시 이름과 MIME 타입도 `as`, `withMime` 메서드로 지정할 수 있습니다:

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
#### 파일시스템 디스크의 파일 첨부

[파일시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 이메일에 첨부하려면, `fromStorage` 메서드를 사용하세요:

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

첨부파일 이름이나 MIME 타입도 함께 지정할 수 있습니다:

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

기본 디스크가 아닌 특정 스토리지 디스크의 파일을 첨부하려면 `fromStorageDisk` 메서드를 사용하세요:

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

`fromData` 첨부 메서드를 사용하면, 메모리 상의 원시 바이트 데이터를 첨부파일로 추가할 수 있습니다. 예를 들어, 메모리에서 PDF 파일을 생성하고 디스크에 저장하지 않고 첨부할 경우 유용하게 사용할 수 있습니다. `fromData` 메서드는 raw 데이터 바이트를 반환하는 클로저와 첨부파일 이름을 인자로 받습니다:

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

이메일에 인라인 이미지를 삽입하는 일은 보통 번거롭지만, Laravel은 이를 매우 쉽게 처리할 수 있는 방법을 제공합니다. 인라인 이미지를 삽입하려면, 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 이용하시면 됩니다. `$message` 변수는 모든 이메일 템플릿에서 자동으로 사용 가능하므로 별도로 전달할 필요가 없습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메시지 템플릿에는 사용할 수 없습니다. 일반 텍스트 메시지는 인라인 첨부 기능을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

raw 이미지 데이터 문자열을 이메일에 인라인으로 삽입하고자 할 때는 `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이 메서드를 호출할 때는 삽입할 파일 이름도 전달해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체 (Attachable Objects)

파일 경로로 첨부하는 것도 충분하지만, 실제로는 애플리케이션에서 첨부할 엔티티 자체가 클래스로 표현되는 경우가 많습니다. 예를 들어, 사진을 첨부한다면 그 사진을 나타내는 `Photo` 모델이 있을 수 있습니다. 이럴 때는 해당 모델 자체를 첨부파일로 바로 지정할 수 있습니다.

이 기능을 사용하려면, 첨부 가능한 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현해야 합니다. 이 인터페이스는 `toMailAttachment` 메서드(반드시 `Illuminate\Mail\Attachment` 인스턴스 반환)를 구현하도록 요구합니다:

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

이렇게 attachable 객체를 정의한 후, 이메일 메시지 작성 시 `attachments` 메서드에서 해당 객체를 반환할 수 있습니다:

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

첨부파일 데이터가 Amazon S3처럼 원격 파일 스토리지에 있을 수도 있습니다. 이럴 때는 Laravel의 [파일시스템 디스크](/docs/12.x/filesystem) 기반 첨부를 활용하세요:

```php
// 기본 스토리지 디스크의 파일로 첨부...
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일로 첨부...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리 상의 데이터를 이용해 첨부파일을 만들 수도 있습니다. 이 경우 `fromData` 메서드에 클로저를 전달하면 됩니다. 클로저는 첨부파일의 raw 데이터를 반환해야 합니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

Laravel은 첨부파일 이름과 MIME 타입을 커스터마이즈할 수 있도록 `as`, `withMime` 메서드도 제공합니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

간혹 이메일 메시지를 발송할 때 추가적인 헤더를 붙여야 할 때가 있습니다. 예를 들어, 커스텀 `Message-Id`나 임의의 텍스트 헤더를 추가하는 등입니다.

이때는 메일러블에 `headers` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 파라미터를 받을 수 있습니다. 필요한 파라미터만 전달하면 됩니다:

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

Mailgun, Postmark와 같은 일부 외부 이메일 공급자들은 메시지 "태그"와 "메타데이터" 기능을 지원합니다. 이 기능을 이용하면 애플리케이션이 발송하는 메일을 그룹화하거나 추적할 수 있습니다. `Envelope` 정의에서 태그와 메타데이터를 추가할 수 있습니다:

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

Mailgun 드라이버를 사용할 때는 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 관한 공식 문서를 참고하세요. Postmark 역시 [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)에 관한 정보를 제공합니다.

Amazon SES를 사용하는 경우, `metadata` 메서드를 활용해 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony Message 커스터마이징 (Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer를 기반으로 합니다. 메시지 전송 직전에 Symfony Message 인스턴스를 커스터마이징할 수 있도록 콜백을 등록할 수 있습니다. 이를 위해서, `Envelope` 정의에 `using` 파라미터를 추가하면 됩니다:

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
## 마크다운 메일러블 (Markdown Mailables)

마크다운 메일러블 메시지는 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트의 이점을 메일러블에서 그대로 활용할 수 있게 해줍니다. 메시지는 마크다운으로 작성되므로, Laravel은 아름답고 반응형의 HTML 템플릿은 물론 텍스트 버전까지 자동으로 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 적용된 메일러블을 생성하려면, Artisan `make:mail` 명령어에서 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용하세요:

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
### 마크다운 메시지 작성

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법이 결합된 형태로, 쉽고 간편하게 이메일 메시지를 작성할 수 있으며 Laravel이 제공하는 다양한 이메일 UI 컴포넌트를 활용할 수 있습니다:

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
> 마크다운 메일 작성 시, 과도한 들여쓰기는 피하세요. 마크다운 규칙에 따라 들여쓴 내용은 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트 (Button Component)

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 만들어줍니다. `url`, 그리고 선택적으로 `color`(지원 색상: `primary`, `success`, `error`)를 인자로 받을 수 있습니다. 여러 개의 버튼도 메시지에 추가 가능합니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트 (Panel Component)

패널 컴포넌트는 텍스트 블록을 메시지 본문과 구별되는 색상의 패널로 감싸 강조할 수 있도록 해줍니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트 (Table Component)

테이블 컴포넌트는 마크다운 표를 HTML 표로 변환해줍니다. 컴포넌트의 내용으로 마크다운 표를 넣으시면 됩니다. 컬럼 정렬은 기본 마크다운 표 문법을 따릅니다:

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

모든 마크다운 메일 컴포넌트를 애플리케이션으로 내보내어 원하는 대로 커스터마이징할 수 있습니다. 아래 Artisan 명령어로 `laravel-mail` 태그의 컴포넌트를 export 하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

실행하면 `resources/views/vendor/mail` 디렉토리에 컴포넌트가 복사됩니다. `mail` 디렉토리 아래에는 `html`과 `text` 폴더가 각각의 컴포넌트 파일 형태로 들어있고, 이 파일들을 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보낸 뒤에는, `resources/views/vendor/mail/html/themes` 디렉토리 아래에 생성된 `default.css` 파일을 수정해 CSS를 커스터마이징할 수 있습니다. 이 스타일은 HTML 메일에 inline CSS로 자동 적용됩니다.

만약 Laravel 마크다운 컴포넌트를 위한 새로운 테마를 만들고 싶다면 `html/themes` 디렉토리에 CSS 파일을 추가하고, `config/mail.php` 설정의 `theme` 옵션에서 새 테마 이름을 지정하세요.

특정 메일러블에만 커스텀 테마를 적용하고 싶다면, 해당 클래스의 `$theme` 속성에 사용할 테마 이름을 지정할 수 있습니다.

<a name="sending-mail"></a>
## 메일 발송 (Sending Mail)

이메일을 보내려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용하세요. `to` 메서드는 이메일 주소, User 인스턴스, 혹은 User 컬렉션을 받을 수 있습니다. 객체 또는 컬렉션을 전달할 경우, 해당 객체의 `email`, `name` 속성이 자동으로 수신자 정보로 사용되므로 필드를 반드시 추가하세요. 수신자를 지정한 후에는 메일러블 클래스 인스턴스를 `send` 메서드에 전달합니다:

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

메시지를 보낼 때 `to` 수신자만 지정할 필요는 없습니다. `cc`, `bcc` 수신자를 각각 체이닝해서 지정할 수도 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 발송

배열로 여러 수신자에게 메일을 반복 발송해야 할 때, `to` 메서드는 수신자 목록을 계속 누적하므로 반복문 내에서 반드시 메일러블 인스턴스를 새로 만들어야 합니다. 그렇지 않으면 이전 수신자들에게도 중복 발송됩니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 발송

기본적으로 Laravel은 설정된 `default` 메일러로 메일을 보냅니다. 그러나 `mailer` 메서드를 이용하면 특정 메일러 설정을 사용해 메일을 보낼 수도 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 발송은 응답 속도에 영향을 미칠 수 있기 때문에, 많은 개발자들이 이메일을 백그라운드에서 전송하도록 큐에 넣는 방식을 선호합니다. Laravel은 [큐 API](/docs/12.x/queues)를 통해 이를 아주 쉽게 처리할 수 있게 해줍니다. 메일 메시지를 큐에 넣으려면, 수신자를 지정한 뒤 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이때 자동으로 메일 전송 작업이 큐에 쌓이고, 백그라운드에서 처리됩니다. 먼저 [큐 설정](/docs/12.x/queues)을 완료해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 발송(Delayed Message Queueing)

큐에 쌓인 메일 메시지의 발송을 지연하고자 할 때는 `later` 메서드를 사용하세요. 첫 번째 인자로 `DateTime` 인스턴스를 받아, 해당 시점 이후에 메시지가 발송됩니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/커넥션 지정

`make:mail` 명령어로 생성한 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, 인스턴스에서 `onQueue`, `onConnection` 메서드를 호출해 작업이 사용될 큐와 연결을 지정할 수 있습니다:

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
#### 기본적으로 큐에 전달

언제나 큐잉되는 메일러블 클래스를 만들고 싶다면, 클래스에 `ShouldQueue` 계약을 구현하세요. 이렇게 하면 `send` 메서드를 사용해도 항상 큐에 쌓여 비동기로 전송됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치되면, 작업이 트랜잭션 커밋 전에 큐에서 처리될 수 있습니다. 이 경우, 해당 트랜잭션 안에서 생성/수정된 모델이나 레코드에 대한 변경사항이 아직 데이터베이스에 반영되지 않아 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 옵션이 `false`라도, 개별 메일러블 전송 시 메시지 작업을 모든 열린 트랜잭션 커밋 후 처리되도록 하려면, `afterCommit` 메서드를 호출하세요:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 메일러블의 생성자에서 직접 호출해도 됩니다:

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
> 이러한 상황에서 발생할 수 있는 문제와 해결방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 실패 처리

큐에 쌓여있는 메일이 실패하면, 해당 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 실패의 원인이 된 `Throwable` 인스턴스가 인자로 전달됩니다:

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

가끔은 실제로 발송하지 않고, 메일러블의 HTML 내용을 문자열로 렌더링해야 할 때가 있습니다. 이 경우, 메일러블의 `render` 메서드를 호출하면 평가된 HTML 문자열이 반환됩니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 미리보기 (Previewing Mailables in the Browser)

메일러블 템플릿을 디자인할 때, 일반 Blade 템플릿처럼 브라우저에서 바로 미리보기 할 수 있다면 매우 편리합니다. 라라벨에서는 라우트 클로저나 컨트롤러에서 메일러블을 그대로 반환하면, 이메일을 실제로 전송하지 않고 브라우저에 렌더링된 결과를 보여줍니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 다국어 지원 (Localizing Mailables)

Laravel은 메일러블을 요청의 현재 언어(locale)와 다르게 발송할 수 있으며, 메일이 큐에 쌓여 백그라운드 처리될 때도 해당 로케일이 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드를 사용해서 원하는 언어를 지정할 수 있습니다. 메일러블 템플릿이 평가되는 동안에는 지정한 언어로 전환되고, 완료되면 원래 언어로 되돌아옵니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 언어(User Preferred Locales)

애플리케이션에서 사용자마다 선호 언어(locale)를 저장하는 경우도 있습니다. 모델에 `HasLocalePreference` 계약을 구현하면, 메일 전송 시 모델에 저장된 로케일이 자동으로 사용됩니다:

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

이 인터페이스를 구현했다면, Laravel은 메일러블 또는 알림 발송 시 자동으로 적용된 로케일로 처리해주므로, 별도로 `locale` 메서드를 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트 (Testing Mailable Content)

Laravel은 메일러블 구조를 검사할 수 있는 다양한 메서드를 제공합니다. 또한, 원하는 콘텐츠가 메일러블에 포함되어 있는지 간편하게 테스트할 수 있도록 여러 메서드를 지원합니다:

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

"HTML" 관련 assertion은 메일러블의 HTML 버전에, "text" 관련 assertion은 plain-text 버전에 문자열이 포함되었는지 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일 전송 테스트 (Testing Mailable Sending)

메일러블의 내용 테스트는 실제 발신과는 별도로, "특정 메일러블이 특정 사용자에게 전송되었는지"만 체크하는 것이 실무 테스트에 더 효과적입니다. 대부분의 경우, 메일러블 내용보다 해당 메일이 실제로 발송되었는지만 확인하면 충분합니다.

`Mail` 파사드의 `fake` 메서드로 실제 메일발송을 방지하고, 이후 메일러블이 발송(또는 큐에 쌓임)되었는지 assertion 메서드로 검사할 수 있습니다:

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

백그라운드로 큐잉되어 발송되는 경우에는 `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 클로저를 전달하면, 특정 조건을 만족하는 메일러블이 실제로 발송 또는 큐잉됐는지 정교하게 검사할 수 있습니다. 조건을 만족하는 메일이 1건이라도 있다면 assertion은 성공합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

클로저로 받은 메일러블 인스턴스에는 다양한 검사 도우미 메서드가 제공됩니다:

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

첨부파일 검사 도우미도 함께 사용할 수 있습니다:

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

메일 전송이 아예 이루어지지 않았는지 또는 큐에 쌓이지 않았는지 동시에 검증하고 싶다면, `assertNothingOutgoing`, `assertNotOutgoing` 메서드를 활용하세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

개발 환경에서는 실제 이메일 주소로 메일을 보내고 싶지 않을 때가 많습니다. Laravel은 로컬 개발 중 이메일 전송을 "비활성화"하는 다양한 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버(Log Driver)

`log` 메일 드라이버는 실제로 이메일을 발송하지 않고 로그 파일에 기록합니다. 주로 로컬 개발 환경에서만 사용하게 됩니다. [환경별 설정 방법](/docs/12.x/configuration#environment-configuration)은 공식 문서를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또 다른 방법으로는 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)과 같은 서비스와 함께 `smtp` 드라이버를 사용해 실제 이메일 주소로 메일을 보내는 대신, "더미" 사서함으로 전송하여 이메일 클라이언트에서 직접 확인할 수 있습니다. 특히 Mailtrap은 실제 전송 결과를 뷰어에서 편하게 점검할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용한다면, [Mailpit](https://github.com/axllent/mailpit)을 통해 메일을 미리보기 할 수 있습니다. Sail이 실행 중이라면 브라우저에서 `http://localhost:8025`로 접속하면 됩니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 이용해 "전역 to 주소"를 지정할 수도 있습니다. 이 메서드는 보통 애플리케이션의 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

`alwaysTo` 메서드를 사용하면, 추가적으로 지정된 "cc"나 "bcc" 주소는 모두 무시됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 메시지 발송 시 두 개의 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지 발송 전에, `MessageSent` 이벤트는 메시지 발송 후에 발생합니다. 이 이벤트들은 실제로 이메일이 *전송*될 때 발생하며, 큐에 쌓일 때는 발생하지 않습니다. 이 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 만들어 활용할 수 있습니다:

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
## 커스텀 전송방식(Transport) (Custom Transports)

Laravel은 다양한 메일 전송방식을 기본으로 지원합니다. 하지만 기존에 지원하지 않는 서비스로 이메일을 보내고 싶다면 직접 커스텀 전송방식을 만들 수 있습니다. 우선 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속한 클래스를 작성하고, `doSend`와 `__toString` 메서드를 구현해야 합니다:

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

커스텀 전송방식을 정의했다면, 이제 `Mail` 파사드의 `extend` 메서드로 등록할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다. `extend` 메서드에 전달한 클로저에는 `config/mail.php`의 메일러 설정이 `$config` 배열로 전달됩니다:

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

커스텀 전송방식을 정의 · 등록했다면, `config/mail.php`에 새로운 메일러 설정을 추가해 사용할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송방식 (Additional Symfony Transports)

Laravel은 Mailgun, Postmark 등 일부 Symfony에서 지원하는 메일 전송방식을 내장하지만, 그 외에 원하는 Symfony 전송방식을 직접 추가할 수도 있습니다. 필요한 Symfony 메일러 패키지를 Composer로 설치 후, Laravel에 직접 등록하면 됩니다. 예를 들어, "Brevo"(구 Sendinblue) Symfony 메일러를 추가하려면:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치가 완료되면, 아래처럼 Brevo API 자격 증명을 `services` 설정 파일에 추가합니다:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그런 다음 `Mail` 파사드의 `extend` 메서드로 전송방식을 등록하세요. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 처리합니다:

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

커스텀 전송방식이 등록되면, `config/mail.php`에서 이 전송방식을 사용하는 메일러를 정의할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
