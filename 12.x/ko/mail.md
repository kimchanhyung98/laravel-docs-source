# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
    - [장애 조치(Failover) 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [메일러블 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부](#inline-attachments)
    - [첨부 가능한 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스텀](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스텀](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 로컬라이징](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail` 드라이버를 지원하므로, 로컬 서비스나 클라우드 기반 서비스를 선택해 간편하게 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일 안에 설정된 각 메일러는 자체의 고유한 설정과 "전송 방식(transport)"을 가질 수 있기 때문에, 여러 메일 서비스를 상황에 맞게 유연하게 사용할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일 내의 `mailers` 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송 방식에 대한 샘플 설정이 포함되어 있습니다. 그리고 `default` 항목은 애플리케이션에서 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 사전 준비 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend와 같은 API 기반 드라이버는 SMTP 서버를 사용한 메일 발송보다 더 쉽고 빠른 경우가 많습니다. 가능하다면 이런 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer transport 패키지를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

이제 애플리케이션의 `config/mail.php` 파일에서 두 가지를 설정합니다. 첫째, 기본 메일러를 `mailgun`으로 설정하세요.

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

둘째, `mailers` 배열에 아래 구성 배열을 추가하세요.

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러 설정 후, `config/services.php` 파일에 아래 옵션들을 추가해야 합니다.

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국이 아닌 다른 [Mailgun region](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하는 경우, 그 지역의 endpoint를 `services` 설정 파일에 지정해야 합니다.

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer transport 패키지를 설치해야 합니다.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

다음으로, `config/mail.php` 파일에서 `default` 옵션을 `postmark`로 설정합니다. 그리고 `config/services.php` 파일에서 아래와 같이 옵션이 포함되어 있는지 확인합니다.

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하려면, 해당 메일러의 구성 배열에 `message_stream_id` 옵션을 추가할 수 있습니다.

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend의 PHP SDK 패키지를 설치해야 합니다.

```shell
composer require resend/resend-php
```

`config/mail.php` 파일의 `default` 옵션을 `resend`로 설정하고, `config/services.php` 파일에 아래 옵션이 있는지 확인합니다.

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 우선 Amazon AWS SDK for PHP를 Composer로 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

`config/mail.php`에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 아래 옵션이 포함되어 있는지 확인하세요.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 인증 정보(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)를 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능(subscription management)](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환할 수 있습니다.

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

이메일 전송 시 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, SES 설정에서 `options` 배열을 사용할 수 있습니다.

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
### 장애 조치(Failover) 설정 (Failover Configuration)

외부 메일 발송 서비스가 다운된 경우에 대비해, 하나 이상의 백업 메일 전송 구성을 지정하면 유용합니다. 이렇게 하려면, `mail` 설정 파일에 `failover` 전송 방식을 사용하는 메일러를 정의하세요. 이 메일러의 구성 배열에는 사용할 메일러 순서를 정하는 `mailers` 배열이 포함되어야 합니다.

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

장애 조치 메일러를 구성한 후, `.env` 파일에서 이 메일러를 기본 메일러로 설정하세요.

```ini
MAIL_MAILER=failover
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(Round Robin) 설정 (Round Robin Configuration)

`roundrobin` 전송 방식을 사용하면 여러 메일러에 메일 발송 작업을 분산시킬 수 있습니다. `mail` 설정 파일에 `roundrobin` 전송 방식을 가진 메일러를 아래와 같이 정의합니다.

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

그리고 `mail` 설정 파일의 `default` 항목에 이 메일러의 이름을 설정하세요.

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 전송 방식은 등록된 메일러 중 하나를 무작위로 선택하고, 이후 발송 시에는 순서대로 다음 메일러를 사용합니다. `failover` 전송 방식이 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*을 지향한다면, `roundrobin`은 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성 (Generating Mailables)

Laravel 애플리케이션에서는, 전송할 각 이메일 유형에 대해 하나의 "메일러블(mailable)" 클래스를 생성합니다. 이 클래스들은 `app/Mail` 디렉터리에 위치합니다. 만약 이 디렉터리가 없다면, `make:mail` Artisan 명령어로 메일러블을 최초 생성할 때 자동으로 만들어집니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 해당 파일을 열어 내용을 확인해봅시다. 메일러블 클래스는 주로 `envelope`, `content`, `attachments` 메서드에서 설정합니다.

`envelope` 메서드는 메시지의 제목(subject), 필요하다면 수신자도 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용 생성을 위한 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope를 이용한 발신자 지정

이메일의 발신자(즉, "from" 주소)를 지정하는 방법을 살펴봅시다. 발신자는 두 가지 방법으로 지정할 수 있습니다. 먼저, 메시지의 envelope에 "from" 주소를 지정할 수 있습니다.

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

필요하다면 `replyTo` 주소도 지정할 수 있습니다.

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

애플리케이션 전체에서 항상 동일한 "from" 주소를 사용할 경우, 각 메일러블마다 일일이 지정하는 대신 `config/mail.php` 설정 파일에 글로벌 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 "from" 주소가 따로 지정되지 않은 경우 이 값이 사용됩니다.

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한 전역적으로 "reply_to" 주소를 지정할 수도 있습니다.

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서는 메일 본문의 내용을 렌더링할 뷰(view) 또는 템플릿을 지정할 수 있습니다. Laravel에서는 보통 [Blade 템플릿](/docs/12.x/blade)을 사용하여 HTML 이메일을 작성하며, Blade의 강력하고 편리한 문법을 그대로 활용할 수 있습니다.

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
> 이메일 템플릿을 관리하기 위해 `resources/views/mail` 디렉터리를 생성하는 것이 일반적이지만, 실제로는 `resources/views` 디렉터리 내 원하는 곳에 자유롭게 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트(Plain Text) 이메일

이메일의 일반 텍스트 버전을 별도로 정의하고 싶다면, 메시지 `Content` 정의에 plain-text 템플릿을 함께 지정할 수 있습니다. `text` 파라메터 역시 뷰 이름이며, HTML 버전과 plain-text 버전을 모두 지정할 수 있습니다.

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

더 명확하게 하고 싶다면, `view` 대신 `html` 파라메터를 사용할 수도 있습니다.

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성을 통한 뷰 데이터 전달

이메일 본문에서 사용할 데이터를 Blade 뷰로 전달하려면 크게 두 가지 방식이 있습니다. 첫 번째는, 메일러블 클래스의 public 속성에 값을 할당하는 방법입니다. 생성자에서 데이터를 받아 해당 속성에 할당하면, 뷰에서 곧바로 접근할 수 있습니다.

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

이렇게 할당된 public 속성은 Blade 템플릿에서 바로 사용할 수 있습니다.

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라메터를 통한 뷰 데이터 전달

이메일에 전달할 데이터를 직접 가공해서 전달하고 싶은 경우, `Content` 정의의 `with` 파라메터를 사용할 수 있습니다. 보통 데이터는 생성자에서 받아 protected 또는 private 속성에 보관하고, `with` 파라메터로 뷰에 넘깁니다.

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

`with` 파라메터로 넘긴 데이터는 Blade 템플릿에서 다음과 같이 사용할 수 있습니다.

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

이메일에 첨부 파일을 추가하려면, 메일러블 클래스의 `attachments` 메서드에서 파일들을 반환합니다. `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달해 첨부할 수 있습니다.

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

첨부 파일의 표시 이름이나 MIME 타입도 `as`와 `withMime` 메서드를 통해 지정할 수 있습니다.

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
#### 파일 시스템 디스크에서 첨부

[파일 시스템 디스크](/docs/12.x/filesystem)에 저장되어 있는 파일을 첨부하려면 `fromStorage` 메서드를 사용할 수 있습니다.

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

물론, 이름과 MIME 타입도 지정 가능합니다.

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

기본이 아닌 다른 스토리지 디스크의 파일을 첨부하려면 `fromStorageDisk`를 사용하면 됩니다.

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

`fromData` 메서드를 사용하면, 메모리상의 Raw 바이트 문자열도 첨부파일로 추가할 수 있습니다. 예를 들어, PDF를 메모리에서 직접 생성했다면, 파일로 저장하지 않고 바로 첨부할 때 사용할 수 있습니다.

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
### 인라인 첨부 (Inline Attachments)

이메일에 이미지를 인라인으로 삽입하는 작업은 번거롭지만, Laravel은 간편하게 처리할 수 있도록 도와줍니다. 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용해 이미지를 인라인 삽입할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에 자동으로 제공되므로 따로 전달하지 않아도 됩니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에서는 사용할 수 없습니다. plain-text 메시지는 인라인 첨부를 지원하지 않습니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터의 인라인 삽입

Raw 이미지 데이터 문자열을 이메일에 인라인으로 삽입하려면 `$message` 변수의 `embedData` 메서드를 사용하면 됩니다. 파일 이름을 함께 지정해줍니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체 (Attachable Objects)

파일 경로 문자열로 첨부하는 것과 달리, 애플리케이션 내 엔터티(예: "사진")를 클래스로 표현하고 있을 때 해당 모델 전체를 첨부하고 싶을 수 있습니다. 이럴 때 "첨부 가능한 객체(Attachable Objects)" 기능을 사용하면 모델 자체를 간단하게 첨부할 수 있습니다.

먼저, 첨부하려는 클래스(예: Photo)에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 그리고 `toMailAttachment` 메서드에서 `Illuminate\Mail\Attachment` 인스턴스를 반환합니다.

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

정의한 객체는 메일러블 클래스의 `attachments` 메서드에서 반환하면 자동으로 첨부됩니다.

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

첨부 데이터가 Amazon S3와 같은 원격 파일 스토리지에 있다면, Laravel의 [파일 시스템 디스크](/docs/12.x/filesystem)를 활용한 첨부도 지원됩니다.

```php
// 기본 디스크의 파일 첨부
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일 첨부
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리상의 데이터를 첨부하고 싶다면, `fromData` 메서드에 클로저를 전달하면 됩니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부 파일 이름과 MIME 타입 등은 `as`와 `withMime` 메서드로 커스텀할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

특정 헤더(예: `Message-Id`나 기타 커스텀 텍스트 헤더)를 메시지에 추가해야 하는 경우, 메일러블 클래스에 `headers` 메서드를 정의하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 파라메터를 필요에 따라 지정할 수 있습니다.

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
### 태그와 메타데이터 (Tags and Metadata)

Mailgun, Postmark 등 일부 외부 메일 서비스는 메시지를 그룹화하거나 추적할 수 있도록 "태그(tags)"와 "메타데이터(metadata)" 기능을 지원합니다. 메일러블의 `Envelope` 정의에서 태그와 메타데이터를 설정할 수 있습니다.

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

Mailgun 드라이버의 태그 및 메타데이터에 대한 자세한 내용은 [Mailgun 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags), [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)를 참고하세요. Postmark 역시 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서가 준비되어 있습니다.

만약 Amazon SES를 사용 중이라면, 태그 기능은 `metadata` 메서드로 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스텀 (Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer로 구현되어 있습니다. 메시지 전송 전에 Symfony Message 인스턴스를 이용해 더욱 세밀하게 메시지를 커스텀할 수도 있습니다. 이를 위해 `Envelope`에 `using` 파라메터로 콜백을 등록할 수 있습니다.

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

마크다운 메일러블을 이용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 제작된 템플릿과 컴포넌트를 그대로 활용할 수 있습니다. 메시지를 마크다운으로 작성하면, Laravel이 자동으로 반응형 HTML 템플릿과 plain-text 버전을 함께 렌더링해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 포함된 메일러블을 생성하려면, `make:mail` Artisan 명령어의 `--markdown` 옵션을 사용합니다.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 파라메터를 사용하여 마크다운 템플릿을 지정합니다.

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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 조합해 손쉽게 메시지를 작성할 수 있습니다. Laravel이 제공하는 미리 만들어진 이메일 UI 컴포넌트를 자유롭게 활용하세요.

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
> 마크다운 이메일에서는 들여쓰기를 과도하게 사용하지 마세요. 마크다운 표준에 따라, 들여쓰기가 있는 내용은 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트(Button Component)

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url`(필수)과 `color`(선택) 두 가지 인수를 받으며, 지원 색상은 `primary`, `success`, `error`입니다. 원하는 만큼 여러 개의 버튼을 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트(Panel Component)

패널 컴포넌트는 전달된 텍스트 블록을 탐색성 높은 배경색으로 둘러싼 패널 영역에 표시합니다. 특정 텍스트 블록에 주목시키고 싶을 때 활용하세요.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트(Table Component)

테이블 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환해줍니다. 마크다운 문법 내에서 열 정렬 문법도 지원합니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스텀 (Customizing the Components)

마크다운 메일 컴포넌트는 직접 커스텀할 수 있습니다. 이 컴포넌트들을 내 애플리케이션으로 내보내려면, `vendor:publish` Artisan 명령어로 `laravel-mail` 에셋 태그를 사용하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

명령이 실행되면 `resources/views/vendor/mail` 디렉터리에 마크다운 메일 컴포넌트가 복사됩니다. `mail` 디렉터리에는 `html`, `text` 디렉터리가 각각 포함되어 있고, 각 컴포넌트의 HTML/텍스트 버전이 들어 있습니다. 원하는 대로 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스텀

컴포넌트를 내보낸 후, `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. 이 파일의 CSS를 수정한 내용이 자동으로 마크다운 메일의 HTML 버전 인라인 스타일로 적용됩니다.

마크다운 컴포넌트용 새로운 테마를 만들고 싶다면, 위 디렉터리에 새 CSS 파일을 추가하면 됩니다. 파일 이름에 맞춰 `config/mail.php`의 `theme` 옵션을 변경하세요.

특정 메일러블에만 개별적으로 테마를 적용하고 싶다면, 해당 클래스의 `$theme` 속성에 사용할 테마 이름을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송 (Sending Mail)

메일을 전송하려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to`는 이메일 주소, 사용자 인스턴스, 혹은 사용자 컬렉션을 받을 수 있습니다. 객체나 컬렉션을 전달하면, Laravel은 객체의 `email`과 `name` 속성을 이용해 자동으로 수신자를 결정합니다. 이후, 메일러블 인스턴스를 `send` 메서드에 전달해 메일을 보냅니다.

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

메일을 보낼 때 "to" 수신자 외에도 "cc", "bcc" 수신자 역시 메서드 체이닝으로 지정할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자 반복 발송

여러 수신자에게 메일러블을 반복 전송해야 할 때, `to` 메서드는 이전에 지정된 수신자에 계속 추가되므로, 매번 새로운 메일러블 인스턴스를 생성해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러 사용

기본적으로 Laravel은 `mail` 설정 파일의 `default` 메일러로 메일을 보냅니다. 하지만, `mailer` 메서드를 사용하면 지정한 메일러 설정을 통해 발송할 수도 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 발송은 응답 속도를 저하시킬 수 있으므로, 백그라운드에서 메일을 큐(Queue)에 넣어 전송하는 것이 일반적입니다. Laravel의 [통합 큐 API](/docs/12.x/queues)를 이용해 간단히 메일을 큐잉할 수 있습니다. 수신자 지정 후, `queue` 메서드를 사용하면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 큐에 작업(Job)을 쌓아, 메일을 백그라운드에서 전송합니다. 사용 전에는 [큐 설정](/docs/12.x/queues)이 되어 있어야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 전송

일정 시간 후에 큐잉된 이메일을 보낼 경우, `later` 메서드를 쓸 수 있습니다. 첫 번째 인수는 `DateTime` 인스턴스이며, 언제 발송할지 지정합니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/연결 사용

`make:mail`로 생성한 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, `onQueue`, `onConnection` 메서드를 통해 큐 이름과 연결을 지정할 수 있습니다.

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
#### 항상 큐에 넣기

특정 메일러블이 항상 큐에 들어가길 원한다면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현하면 됩니다. 이렇게 하면, `send`로 바로 보내더라도 항상 큐에 들어갑니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐된 메일러블과 데이터베이스 트랜잭션

큐로 발송되는 메일러블이 데이터베이스 트랜잭션 내에서 디스패치 될 때, 큐에서 처리되는 시점에 트랜잭션이 아직 커밋되지 않았을 수 있습니다. 이 경우, 트랜잭션 동안 변경한 모델이나 레코드가 아직 데이터베이스에 반영되지 않아 예기치 않은 오류가 날 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`여도, 메일 메시지 전송 시 `afterCommit` 메서드를 호출하면 모든 트랜잭션 커밋 후 실행되도록 할 수 있습니다.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

혹은 메일러블 클래스 생성자에서 `afterCommit`을 호출할 수도 있습니다.

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
> 이러한 문제에 대한 자세한 우회 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐 메일 발송 실패 처리

큐에 들어간 메일이 실패할 경우, 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 이때 실패 원인이 되는 `Throwable` 인스턴스가 전달됩니다.

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

메일러블을 실제로 전송하지 않고, HTML 내용을 문자열로 받아오고 싶을 때는 `render` 메서드를 사용하세요. 메일러블의 HTML이 문자열로 반환됩니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 만들 때, Blade 템플릿처럼 브라우저로 직접 렌더링해 미리보기하면 매우 편리합니다. 이를 위해, 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 직접 반환하면, 브라우저에서 바로 내용을 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 로컬라이징 (Localizing Mailables)

Laravel은 메일 발송 시 현재 요청의 로케일이 아닌 다른 언어(로케일)로도 메일러블을 전송할 수 있으며, 메일이 큐에 들어가더라도 해당 로케일이 기억됩니다.

이를 위해 `Mail` 파사드는 `locale` 메서드를 제공합니다. 메일러블 템플릿이 렌더링되는 동안 지정한 로케일로 변경되었다가, 이후에는 원래 로케일로 복원됩니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

애플리케이션에서 사용자별 선호 로케일을 저장하고 있다면, 모델에 `HasLocalePreference` 인터페이스를 구현할 수 있습니다. 이를 구현하면 Laravel이 메일 및 알림 발송 시 자동으로 해당 로케일을 사용합니다.

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

이렇게 하면, `locale` 메서드를 따로 호출하지 않아도 자동으로 사용자의 선호 언어로 메일이 전송됩니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트 (Testing Mailable Content)

Laravel은 메일러블의 구조와 내용을 검사할 수 있는 다양한 메서드를 제공합니다. 아래는 메일러블에 특정 내용 또는 첨부가 포함되어 있는지 테스트하는 예시입니다.

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

HTML 관련 assertion은 메일러블의 HTML 버전에서, text 관련 assertion은 plain-text 버전에서 해당 문자열의 존재 여부를 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 발송 테스트 (Testing Mailable Sending)

메일러블의 내용 테스트와, 실제로 특정 사용자에게 메일러블이 "전송"되었는지 테스트는 별도로 하는 것이 좋습니다. 일반적으로 코드에서 중요한 것은 "메일러블이 전송되었는가"이므로, 메일러블의 내용까지 테스트하지 않아도 충분한 경우가 많습니다.

메일 발송을 실제로 하지 않으려면, `Mail` 파사드의 `fake` 메서드를 사용하세요. 이 후, `Mail` 파사드의 various assertion 메서드를 통해 발송 지시에 대한 테스트를 할 수 있습니다.

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

백그라운드 큐로 메일러블을 발송했다면, `assertSent` 대신 `assertQueued`를 사용하세요.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등의 메서드에는 클로저를 넘겨 특정 조건을 만족하는 메일러블이 전송/큐잉 되었는지 체크할 수 있습니다. 해당 조건을 만족하는 메일러블이 1개 이상 있다면 통과합니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

이 때 전달되는 메일러블 인스턴스는 아래와 같이 여러 유용한 메서드로 상태를 확인할 수 있습니다.

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

첨부파일에 대해서도 아래와 같이 검증할 수 있습니다.

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

메일이 전혀 발송 또는 큐잉되지 않았는지도 아래처럼 확인할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

개발 중 실제로 이메일이 발송되는 것은 바람직하지 않습니다. Laravel은 로컬 개발 시 이메일이 실제로 전송되지 않도록 다양한 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버(Log Driver)

`log` 메일 드라이버는 이메일을 실제로 전송하는 대신 로그 파일에 기록해줍니다. 주로 개발 환경에서 사용하며, 환경별 설정 방법은 [환경 설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io) 등의 서비스를 `smtp` 드라이버와 함께 이용해 가상(더미) 메일함으로 메시지를 전송해 볼 수 있습니다. 이 방식은 실제 이메일 클라이언트에서 최종 이메일을 직접 확인할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, [Mailpit](https://github.com/axllent/mailpit)과 연동해 메일 미리보기도 가능합니다. Sail이 실행 중이면 `http://localhost:8025`에서 Mailpit 인터페이스를 확인할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드로 글로벌 "to" 주소를 지정할 수 있습니다. 이 메서드는 보통 서비스 프로바이더의 `boot` 메서드에서 호출하면 됩니다.

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

`alwaysTo` 메서드를 활성화하면, 추가로 지정된 "cc"와 "bcc" 주소는 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 발송 시 두 개의 이벤트를 발생시킵니다. `MessageSending` 이벤트는 발송 직전에, `MessageSent` 이벤트는 발송 후에 발생합니다. 이들 이벤트는 실제 *발송* 시점에 발생하며, 큐에 들어간 시점이 아님에 유의하세요. 애플리케이션에서 [이벤트 리스너](/docs/12.x/events)를 등록해 활용할 수 있습니다.

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
## 커스텀 전송 방식 (Custom Transports)

Laravel은 다양한 메일 전송 방식을 기본적으로 제공하지만, 직접 구현해 다른 서비스로 메일을 보내고 싶을 때가 있습니다. 이럴 때는 `Symfony\Component\Mailer\Transport\AbstractTransport`를 상속받아 새로운 트랜스포트 클래스를 만드세요. 그리고 `doSend`, `__toString` 메서드를 구현합니다.

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

커스텀 전송 방식을 제작했다면, `Mail` 파사드의 `extend` 메서드로 등록하세요. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 등록하면 됩니다. 콜백에는 설정 파일의 해당 mailer 설정 배열이 `$config`로 전달됩니다.

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

등록이 완료됐다면, `config/mail.php`에 아래처럼 mailer를 등록하세요.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식 (Additional Symfony Transports)

Laravel은 Mailgun, Postmark 등 일부 Symfony 공식 트랜스포트를 내장 지원합니다. 추가로 다른 Symfony 트랜스포트를 사용하려면 Composer로 해당 메일러를 설치한 뒤, Laravel에 트랜스포트를 직접 등록하면 됩니다. 예시로 "Brevo"(구 Sendinblue) 메일러를 설치, 등록하는 방법입니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, `services` 설정 파일에 Brevo API 정보를 입력하세요.

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그리고 서비스 프로바이더의 `boot` 메서드에서 아래처럼 등록합니다.

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

등록이 끝나면, `config/mail.php`에 mailer를 아래와 같이 등록할 수 있습니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
