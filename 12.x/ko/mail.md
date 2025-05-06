# 메일

- [소개](#introduction)
    - [구성](#configuration)
    - [드라이버/전송 요구사항](#driver-prerequisites)
    - [Failover(장애조치) 구성](#failover-configuration)
    - [라운드로빈 구성](#round-robin-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬개발](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송(트랜스포트)](#custom-transports)
    - [추가 Symfony 전송](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트 기반의 깔끔하고 단순한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 통한 이메일 전송 드라이버를 제공하므로, 로컬 또는 클라우드 기반의 다양한 서비스로 빠르게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 구성

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 설정된 각 메일러는 고유한 구성을 가질 수 있으며, 메일러마다 고유한 "전송(transport)"도 사용할 수 있습니다. 이를 통해 특정 이메일 메시지마다 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 거래 이메일은 Postmark로, 대량 이메일은 Amazon SES로 전송할 수 있습니다.

`mail` 설정 파일 내 `mailers` 설정 배열에는 Laravel에서 기본적으로 지원하는 주요 메일 드라이버/전송에 대한 예시 항목이 포함되어 있습니다. `default` 설정 값은 애플리케이션에서 이메일 메시지를 전송할 때 기본적으로 사용할 메일러를 정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/전송 요구사항

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 종종 SMTP 서버보다 더 간단하고 빠릅니다. 가능하다면 이들 API 기반 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer를 통해 Symfony의 Mailgun Mailer 전송 패키지를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지 변경이 필요합니다. 먼저, 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 다음 설정을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션을 추가합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 지역 이외의 [Mailgun 지역](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용하는 경우, 해당 지역의 endpoint를 `services` 설정에 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer를 통해 Symfony의 Postmark Mailer 전송 패키지를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

`config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 변경합니다. 그리고 `config/services.php` 파일에 다음 옵션이 있는지 확인하세요:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하려면, 메일러 설정 배열에 `message_stream_id` 옵션을 추가하세요:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이 방법으로 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer를 통해 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

`config/mail.php`에서 `default` 옵션을 `resend`로 설정한 후, `config/services.php`에 다음 옵션이 있는지 확인하세요:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP 패키지를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

그런 다음, `config/mail.php`에서 `default`를 `ses`로 설정하고, `config/services.php`에서 아래 옵션들을 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 인증정보(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)를 사용하려면, `token` 키를 추가하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메일 메시지의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환하세요:

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

AWS SDK의 `SendEmail` 메서드에 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 전달하려면, ses 설정에 `options` 배열을 추가하세요:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스로, Laravel용 API 기반 자체 드라이버를 제공합니다. Composer를 통해 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경변수를 추가하세요. `MAIL_MAILER` 환경변수도 `mailersend`로 지정해야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

그리고, `config/mail.php`의 `mailers` 배열에 MailerSend를 추가하세요:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend 사용법과 호스팅 템플릿 사용법은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### Failover(장애조치) 구성

외부 이메일 서비스가 다운될 수 있기 때문에, 메일 전송에 장애 발생 시 사용할 백업 메일 전송 구성을 지정하는 것이 유용합니다.

이를 위해 `mail` 설정 파일에 `failover` 전송을 사용하는 메일러를 정의하세요. 설정 배열의 `mailers` 항목에는 대체 메일러 후보를 순서대로 배열로 지정합니다:

```php
'mailers' => [
    'failover' => [
        'transport' => 'failover',
        'mailers' => [
            'postmark',
            'mailgun',
            'sendmail',
        ],
    ],

    // ...
],
```

이후, `default` 설정에 `failover`를 지정하여 기본 메일러로 사용할 수 있습니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드로빈 구성

`roundrobin` 전송은 여러 메일러에 걸쳐 메일 발송 부하를 분산합니다. 이제 `mail` 설정 파일에서 `roundrobin` 전송을 사용하는 메일러를 정의하세요. 사용되는 메일러들을 배열로 지정합니다:

```php
'mailers' => [
    'roundrobin' => [
        'transport' => 'roundrobin',
        'mailers' => [
            'ses',
            'postmark',
        ],
    ],

    // ...
],
```

정의 후, `default` 메일러를 `roundrobin`으로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 전송은 최초 전송에는 무작위 메일러를 선택하고, 이후에는 순차적으로 전환합니다. `failover`가 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*을 목적으로 한다면, `roundrobin`은 *[부하분산(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기

Laravel 애플리케이션에서는 각 이메일 타입마다 "메일러블(mailable)" 클래스로 정의합니다. 이 클래스들은 `app/Mail` 디렉터리에 위치합니다. 해당 디렉터리가 없는 경우 첫 메일러블 클래스를 생성할 때 자동으로 생성됩니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기

메일러블 클래스를 생성했다면, 클래스를 열고 내용을 살펴볼 수 있습니다. 메일러블의 설정은 여러 메서드(예: `envelope`, `content`, `attachments` 등)에서 이루어집니다.

`envelope` 메서드는 제목과 수신자 등을 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 [Blade 템플릿](/docs/{{version}}/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope로 지정하기

우선, 이메일 발신자(From) 설정부터 살펴보겠습니다. 두 가지 방법이 있습니다. 첫 번째는 메시지의 envelope에서 "from" 주소를 지정하는 방법입니다:

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

필요에 따라 `replyTo` 주소도 지정할 수 있습니다:

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
#### 글로벌 "from" 주소 사용

애플리케이션에서 모든 이메일에 항상 같은 발신 주소를 쓴다면, 매번 메일러블 클래스마다 이를 지정하는 것은 번거로울 수 있습니다. 이런 경우 `config/mail.php`에서 글로벌 "from" 주소를 지정할 수 있습니다. 메일러블에서 별도 지정이 없으면 이 주소가 기본 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

글로벌 "reply_to" 주소도 아래와 같이 지정할 수 있습니다:

```php
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드에서 렌더링에 사용할 `view`(템플릿)를 지정할 수 있습니다. 각 이메일은 보통 [Blade 템플릿](/docs/{{version}}/blade)을 사용하므로, HTML 작성에 Blade의 모든 기능과 편의를 누릴 수 있습니다:

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
> 이메일 템플릿을 모두 보관할 별도 `resources/views/emails` 디렉터리를 만드는 것이 좋지만, 이는 필수가 아니라 `resources/views` 아래 원하는 위치에 배치해도 됩니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 별도로 정의하려면 `Content` 정의 시 plain-text 템플릿을 지정할 수 있습니다. `view`와 동일하게 `text`에 템플릿명을 지정하면 됩니다:

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

혼동을 피하기 위해 `html` 파라미터는 `view`의 별칭으로 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 속성 이용

이메일 HTML을 렌더링할 때 사용할 데이터를 뷰에 전달하려면 두 가지 방법이 있습니다. 첫 번째는 메일러블 클래스에 정의된 모든 public 속성에 자동으로 데이터를 전달하는 방법입니다. 즉, 생성자에서 전달한 데이터를 클래스의 public 속성에 할당하면, 해당 속성은 자동으로 뷰에서 사용할 수 있습니다:

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

할당된 데이터는 Blade 템플릿에서 아래처럼 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### with 파라미터 이용

템플릿으로 전달하는 데이터의 포맷을 직접 조정하고 싶다면, `Content` 정의에서 `with` 파라미터를 사용해 뷰에 전달할 수 있습니다. 이때 생성자에서는 데이터를 `protected`나 `private` 속성에 저장하세요. (public을 사용하면 Blade에서 자동 노출됨)

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

이 데이터 역시 Blade 템플릿에서 아래처럼 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메일러블의 `attachments` 메서드가 반환하는 배열에 파일을 추가하면 됩니다. 파일 경로를 `Attachment` 클래스의 `fromPath` 메서드에 전달하세요:

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

첨부파일의 표시 이름이나 MIME 타입을 지정하려면 `as` 및 `withMime` 메서드를 추가로 사용할 수 있습니다:

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
#### 디스크 파일 첨부

파일을 [스토리지 디스크](/docs/{{version}}/filesystem)에 저장해 둔 경우 `fromStorage` 메서드로 첨부할 수 있습니다:

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

파일 이름과 MIME 타입도 아래처럼 지정할 수 있습니다:

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

기본 디스크가 아닌 다른 디스크 파일을 첨부하려면 `fromStorageDisk` 메서드를 사용하세요:

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

`fromData` 메서드는 메모리 내 raw 바이너리 데이터를 첨부파일로 첨부할 때 사용합니다. 예를 들어, 메모리에서 PDF를 생성하고 파일로 저장하지 않은 상태로 첨부할 수 있습니다:

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
### 인라인 첨부파일

Laravel은 이메일 본문에 이미지를 손쉽게 인라인 첨부할 수 있는 방법을 제공합니다. 인라인 이미지를 삽입하려면 이메일 템플릿 내에서 `$message->embed($pathToImage)`를 사용하세요. `$message` 변수는 모든 이메일 템플릿에서 자동으로 사용할 수 있습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에는 사용 불가합니다(plain-text 이메일은 인라인 첨부를 지원하지 않으므로).

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

raw 이미지 데이터를 인라인 첨부하려면 `$message->embedData($data, 'example-image.jpg')` 메서드를 사용합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

간단한 문자열 파일경로가 아닌, 애플리케이션의 attachable 엔티티가 클래스로 표현된 경우도 많습니다. 예를 들어, 사진 첨부 시 Photo 모델이 존재할 수 있습니다. 이럴 때는 Attachble 인터페이스를 사용하면 모델 인스턴스 자체를 첨부할 수 있습니다.

먼저 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하고, `toMailAttachment` 메서드에서 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

정의 후에는 메일러블의 `attachments` 메서드에서 인스턴스를 배열로 반환하면 됩니다:

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

첨부 데이터가 Amazon S3 등 외부 스토리지에 있을 수도 있으므로, [스토리지 디스크](/docs/{{version}}/filesystem)에 저장된 데이터도 아래처럼 바로 첨부할 수 있습니다:

```php
// 기본 디스크에서 첨부 파일 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 첨부 파일 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한 메모리에 있는 데이터를 첨부파일로 만들려면 클로저를 `fromData`에 전달하세요:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일의 이름이나 MIME 타입은 `as`, `withMime`로 지정할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

이메일에 추가 헤더를 붙여야 할 때(예: custom `Message-Id` 등)에는 메일러블에서 `headers` 메서드를 정의하고, `Illuminate\Mail\Mailables\Headers` 객체를 반환하세요. 이 클래스는 `messageId`, `references`, `text` 파라미터를 지원합니다:

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
### 태그 및 메타데이터

Mailgun, Postmark 같은 타사 이메일 제공업체는 메시지 태그(tag)와 메타데이터(metadata)를 지원하여 이메일 그룹화 및 추적을 돕습니다. `Envelope` 정의를 통해 태그와 메타데이터를 메시지에 추가할 수 있습니다:

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

Mailgun 태그와 메타데이터는 [Mailgun 공식 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging), [metadata](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages) 참고. Postmark는 [tags](https://postmarkapp.com/blog/tags-support-for-smtp), [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서를 참고하세요.

Amazon SES 사용 시에는 `metadata` 메서드로 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙일 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이즈

Laravel의 메일 기능은 Symfony Mailer에서 구동됩니다. 메일 전송 전 Symfony Message 인스턴스에 대해 커스텀 콜백을 등록할 수 있습니다. 이를 위해 `Envelope`에 `using` 파라미터를 지정하세요:

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
## 마크다운 메일러블

Markdown 메일러블 메시지를 사용하면 [메일 알림](/docs/{{version}}/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 쉽고 강력하게 활용할 수 있습니다. Markdown 기반이므로 Laravel이 반응형 HTML 템플릿과 plain-text 버전을 자동으로 생성해 줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 포함된 메일러블을 생성하려면 Artisan 명령어에서 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

`content` 메서드 내에서 Content 정의 시 `view` 대신 `markdown` 파라미터를 사용합니다:

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

마크다운 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합하여, Laravel의 이메일 UI 요소를 손쉽게 사용할 수 있습니다:

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
> 마크다운 이메일 작성 시 들여쓰기를 과도하게 사용하지 마세요. Markdown 파서가 들여쓰기된 코드를 코드블록으로 처리할 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적으로 `color` 인자를 받으며, 지원 색상은 `primary`, `success`, `error`입니다. 메시지에 여러 버튼을 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 해당 텍스트 블록을 배경색이 다른 패널로 강조하여 보여줍니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 실제 HTML 테이블로 변환해줍니다. 마크다운 테이블의 열 정렬 문법도 지원합니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈

마크다운 메일 컴포넌트를 애플리케이션에 내보내어 자유롭게 수정할 수 있습니다. 아래 Artisan 명령어를 사용하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

명령 실행 시, `resources/views/vendor/mail` 아래에 컴포넌트 템플릿이 복사됩니다. `mail` 디렉터리 내 `html`, `text` 디렉터리에 각각의 컴포넌트가 위치합니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보낸 뒤, `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css`가 있습니다. 원하는 대로 CSS를 수정하면 HTML 메일에서 자동으로 인라인 스타일로 변환됩니다.

전혀 새로운 테마를 만들려면 `html/themes`에 CSS 파일을 추가하고, `config/mail.php`에서 `theme` 값을 해당 파일명으로 지정하세요.

특정 메일러블의 테마만 변경하려면, 클래스의 `$theme` 속성에 테마명을 지정하세요.

<a name="sending-mail"></a>
## 메일 전송

메일을 전송하려면 `Mail` [파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용합니다. `to`에는 이메일, 사용자 인스턴스, 사용자 컬렉션 모두 전달할 수 있습니다. 객체나 컬렉션을 넘기면, 객체의 `email`, `name` 필드를 자동으로 참조하니 속성이 존재하는지 확인하세요.

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

"to"만 사용할 필요는 없습니다. 체이닝하여 "cc", "bcc"도 지정 가능합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자에게 반복 전송

여러 수신자에게 반복적으로 메일러블을 전송해야 할 때는, 루프 안에서 반드시 매번 새로운 메일러블 인스턴스를 만들어야 합니다. 그렇지 않으면 이전 수신자에게 중복 전송될 수 있습니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 통한 전송

기본적으로 Laravel은 `default`로 지정된 메일러를 사용하지만, `mailer` 메서드로 특정 메일러를 지정할 수 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

메일 전송은 응답 시간을 지연시킬 수 있기 때문에, 많은 개발자가 메일을 백그라운드에서 큐로 전송하도록 선택합니다. Laravel의 [큐 API](/docs/{{version}}/queues)로 쉽고 일관되게 구현할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 방법은 자동으로 큐에 작업(job)을 추가해 메일을 백그라운드에서 전송합니다. 이 기능을 사용하려면 큐 구성이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 지연 메일 큐 전송

큐에 올린 메일 발송 시점을 지연하려면 `later` 메서드를 사용하세요. 첫 번째 매개변수로 발송 시각(DateTime 인스턴스)을 지정합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐로 전송

`make:mail`로 생성된 메일러블은 `Illuminate\Bus\Queueable` 트레이트를 포함하므로, 메일러블 인스턴스에 `onQueue`, `onConnection` 메서드로 연결, 큐 이름을 지정할 수 있습니다:

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
#### 기본적으로 큐잉하기

무조건 큐로 전송하고자 하는 메일러블은 `ShouldQueue` 인터페이스를 구현하세요. 이제 `send`로 전송해도 자동으로 큐잉됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치(dispatched)되면, 큐가 트랜잭션이 커밋되기 전에 작업을 처리할 수 있습니다. 이 경우 트랜잭션에서 변경한 내용이 데이터베이스에 반영되기 전일 수 있으므로, 모델/레코드에 대한 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`인 경우에도, `afterCommit` 메서드로 해당 작업이 모든 트랜잭션 커밋 후 실행되도록 할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자에서 `afterCommit`을 호출할 수도 있습니다:

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
> 더 자세한 내용은 [큐와 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링

때때로 메일러블을 실제로 보내지 않고 HTML 내용을 생성만 하고 싶을 수 있습니다. 이럴 때는 메일러블의 `render` 메서드를 호출하면 HTML 문자열을 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

이메일 템플릿을 디자인할 때, 마치 Blade 템플릿을 미리보기 하듯 브라우저에서 바로 확인하면 매우 편리합니다. 라우트 클로저나 컨트롤러에서 메일러블을 return하면 자동으로 렌더링되어 브라우저에서 볼 수 있습니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 지역화

현재 요청과 다른 언어(로케일)로 메일러블을 보내고 싶고, 심지어 메일을 큐에 쌓을 때에도 해당 로케일로 보낼 수 있습니다.

`Mail` 파사드의 `locale` 메서드를 사용하여 원하는 언어를 지정하세요. 메일러블 템플릿 렌더링 시에는 이 로케일이 적용되었다가 렌더링이 끝나면 원래의 로케일로 돌아옵니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 언어

사용자마다 선호 로케일을 저장하는 경우, 모델에 `HasLocalePreference`인터페이스를 구현하면, 메일/알림 발송 시 자동으로 해당 로케일이 적용됩니다:

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

이 인터페이스 구현 시, 별도로 `locale` 메서드를 호출하지 않아도 Laravel이 선호 언어를 자동 적용합니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

Laravel은 메일러블 구조 검사뿐 아니라, 원하는 내용이 포함되어 있는지 손쉽게 검증하는 여러 메서드를 제공합니다.

- `assertSeeInHtml`
- `assertDontSeeInHtml`
- `assertSeeInOrderInHtml`
- `assertSeeInText`
- `assertDontSeeInText`
- `assertSeeInOrderInText`
- `assertHasAttachment`
- `assertHasAttachedData`
- `assertHasAttachmentFromStorage`
- `assertHasAttachmentFromStorageDisk`

HTML는 메일러블의 HTML 버전에 문자열 포함 여부를, text는 plain-text 버전에 문자열 포함 여부를 검사합니다.

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
    $mailable->assertSeeInHtml('Invoice Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
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
    $mailable->assertSeeInHtml('Invoice Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
}
```

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트

메일러블의 내용 테스트와 "특정 사용자에게 실제로 메일이 발송되었는지" 여부는 개별 테스트가 바람직하며, 후자는 Laravel이 지정 메일러블 전송을 지시했는지를 검증하면 충분합니다.

`Mail` 파사드의 `fake` 메서드로 실제 메일 발송을 막고, 메일 전송/큐잉 여부나 전달받은 데이터까지 확인 가능합니다.

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

        // Assert 3 total mailables were sent...
        Mail::assertSentCount(3);
    }
}
```

백그라운드 전송(큐잉)이라면 `assertSent` 대신 `assertQueued`를 써야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등에는 클로저를 전달하여 "XXX 조건을 만족한 메일러블이 전송(혹은 큐잉)되었는가"를 정밀하게 검증할 수 있습니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

메일러블 인스턴스에는 to, cc, bcc, replyTo, from, subject 등 주요 속성 확인 메서드가 있습니다:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...');
});
```

첨부파일의 존재까지 아래처럼 검증할 수 있습니다:

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

메일이 전혀 발송/큐잉되지 않았음을 검증하려면 `assertNothingOutgoing`, `assertNotOutgoing`를 활용하세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발

이메일을 실제로 보내고 싶지 않은 로컬 개발 환경에서는, 아래 방법들로 실제 발송을 막을 수 있습니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버를 사용하면, 이메일 내용이 모두 로그 파일에 기록될 뿐 실제 발송되지 않습니다. 이 드라이버는 주로 개발 환경에서만 사용합니다. 환경별 설정법은 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는, [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)과 `smtp` 드라이버를 조합하여 "더미" 메일함으로 메시지를 보내 실제 이메일 클라이언트에서 확인할 수 있습니다. Mailtrap으로 최종 이메일을 진짜 클라이언트처럼 확인할 수 있어 매우 편리합니다.

[Laravel Sail](/docs/{{version}}/sail) 사용 시에는 [Mailpit](https://github.com/axllent/mailpit)으로 미리보기가 가능합니다. Sail 실행 중이면 `http://localhost:8025`에서 접근할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 글로벌 "to" 주소 사용

모든 메일을 특정 주소로 보내고 싶으면, `Mail` 파사드의 `alwaysTo` 메서드로 글로벌 수신자를 지정하세요. 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출하면 됩니다:

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
## 이벤트

Laravel은 메일 전송 과정에서 두 개의 이벤트를 발생시킵니다. `MessageSending`은 전송 직전에, `MessageSent`는 전송 직후에 디스패치됩니다. (큐잉 시가 아니라, 실제 발송 시 발생!) 애플리케이션에서 [이벤트 리스너](/docs/{{version}}/events)를 만들어 사용할 수 있습니다:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * Handle the given event.
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## 커스텀 전송(트랜스포트)

Laravel은 다양한 전송 방식을 내장하고 있으나, 지원하지 않는 타사 서비스로 전송하려면 직접 커스텀 트랜스포트를 구현할 수 있습니다. Symfony의 `Symfony\Component\Mailer\Transport\AbstractTransport`를 상속받아, `doSend`, `__toString()`을 구현하세요:

```php
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

커스텀 트랜스포트 정의 후에는 `Mail` 파사드의 `extend` 메서드로 등록합니다. 일반적으로 `AppServiceProvider`의 `boot`에서 지정합니다. `$config` 인자로 `config/mail.php`의 메일러 설정 배열이 전달됩니다:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        return new MailchimpTransport(/* ... */);
    });
}
```

커스텀 트랜스포트 등록 후, `config/mail.php`에 정의한 메일러에서 트랜스포트 이름을 지정하세요:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송

Laravel은 Mailgun, Postmark 등 Symfony에서 유지관리하는 메일 전송을 지원합니다. 추가로 필요한 Symfony 트랜스포트가 있다면, Composer로 해당 패키지를 설치 후 등록만 하면 됩니다. 예시: Brevo(Sendinblue) 트랜스포트 추가

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, `services` 설정에 API 키를 추가하세요:

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

그 다음, 서비스 프로바이더의 `boot`에서 트랜스포트를 등록합니다:

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

트랜스포트 등록 후, `config/mail.php`에 메일러를 추가하세요:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
