# 메일

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [Mailable 생성](#generating-mailables)
- [Mailable 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony Message 커스터마이징](#customizing-the-symfony-message)
- [마크다운 Mailable](#markdown-mailables)
    - [마크다운 Mailable 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [이메일 발송](#sending-mail)
    - [메일 큐에 넣기](#queueing-mail)
- [Mailable 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [Mailable 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [Mailable 내용 테스트](#testing-mailable-content)
    - [Mailable 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/7.0/mailer.html) 컴포넌트를 기반으로 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 이메일 발송 드라이버를 제공하여, 로컬 또는 클라우드 기반 서비스 중 원하는 것에 빠르게 연동할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내에서 설정된 각 메일러마다 자신만의 고유한 설정과 "트랜스포트"를 가질 수 있으므로, 애플리케이션이 특정 이메일 메시지를 전송할 때 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭션 이메일은 Postmark로, 대량 이메일은 Amazon SES로 보내는 식입니다.

`mail` 설정 파일에서는 `mailers` 구성 배열을 볼 수 있습니다. 이 배열에는 Laravel에서 지원하는 주요 메일 드라이버/트랜스포트의 예시 설정이 들어 있습니다. `default` 값은 애플리케이션이 이메일을 보낼 때 기본으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/트랜스포트 사전 준비 사항

Mailgun, Postmark, Resend, MailerSend와 같이 API 기반의 드라이버는 SMTP 서버를 사용하는 것보다 더 간단하고 빠를 때가 많습니다. 가능하다면 이들 중 하나를 사용하는 것이 좋습니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 두 가지를 변경하세요. 먼저, 기본 메일러를 `mailgun`으로 설정:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 다음 구성을 추가하세요:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

Mailgun을 기본 메일러로 설정한 후에는 `config/services.php` 파일에 아래 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 이외의 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용하는 경우 `services` 설정 파일에서 endpoint를 변경할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치하세요.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

이후, `config/mail.php` 파일의 `default` 옵션을 `postmark`로 설정하세요. 그리고 `config/services.php` 파일에 다음 설정이 있는지 확인합니다.

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하려면, mailer 설정 배열에 `message_stream_id` 항목을 추가할 수 있습니다. 이 배열은 `config/mail.php`에서 찾을 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 스트림을 사용하는 여러 Postmark 메일러도 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Resend의 PHP SDK를 Composer로 설치하세요.

```shell
composer require resend/resend-php
```

이후, `config/mail.php` 파일의 `default` 옵션을 `resend`로 설정하세요. 그리고 `config/services.php`에 다음 옵션을 추가하세요:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, PHP용 Amazon AWS SDK를 Composer로 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

다음으로 `config/mail.php`에서 `default` 옵션을 `ses`로 설정한 뒤, `config/services.php`에 아래와 같이 입력합니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면 `token` 키를 추가할 수 있습니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메시지의 [`headers`](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환해야 합니다.

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

Laravel이 이메일을 보낼 때 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, `ses` 설정에 `options` 배열을 지정할 수 있습니다.

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스이며, 자체 API 기반의 Laravel용 메일 드라이버를 유지 관리하고 있습니다. 해당 드라이버 패키지는 Composer로 설치할 수 있습니다.

```shell
composer require mailersend/laravel-driver
```

설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 그리고 `MAIL_MAILER` 환경 변수도 `mailersend`로 설정합니다.

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로 `config/mail.php`의 `mailers` 배열에 MailerSend를 추가합니다.

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend에 대해 더 자세히 알아보려면 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(Failover) 설정

외부 서비스가 다운되었을 때를 대비해, 하나 또는 여러 개의 백업 메일 발송 구성을 정의할 수 있습니다.

그렇게 하려면, `mail` 설정 파일에서 `failover` 트랜스포트를 사용하는 메일러를 정의하세요. 이 메일러의 설정 배열에 메일러 우선순위대로 나열하면 됩니다.

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

failover 메일러를 정의한 후, 기본 메일러로 지정하세요.

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(Round Robin) 설정

`roundrobin` 트랜스포트는 여러 메일러에 이메일 발송 부하를 분산합니다. 이 트랜스포트를 사용하는 메일러를 다음과 같이 설정할 수 있습니다.

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

이후 기본 메일러로 roundrobin 메일러를 설정하세요.

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 설정된 메일러 중 무작위로 하나를 선택하고, 이후에는 순차적으로 다음 메일러로 전환합니다. `failover`가 *[고가용성](https://en.wikipedia.org/wiki/High_availability)*을, `roundrobin`은 *[로드 밸런싱](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## Mailable 생성

Laravel 애플리케이션에서 각 이메일 유형은 "Mailable" 클래스에 의해 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 위치합니다. 만약 이 디렉토리가 없다면, `make:mail` 아티즌 명령어를 통해 첫 번째 Mailable을 만들 때 자동 생성됩니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 작성

Mailable 클래스를 생성한 후, 내용을 열어보세요. Mailable 클래스의 설정은 주로 `envelope`, `content`, `attachments` 메서드에서 이루어집니다.

`envelope` 메서드는 메일의 제목과, 필요하다면 수신자를 정의한 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 [Blade 템플릿](/docs/{{version}}/blade)을 정의한 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope 사용하기

가장 먼저, 이메일의 발신자("From")를 설정하는 방법을 살펴봅니다. 두 가지 방법이 있으며, 우선 메시지의 envelope에 "from" 주소를 지정할 수 있습니다.

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
#### 글로벌 `from` 주소 설정

모든 이메일에서 동일한 "from" 주소를 쓴다면, 각각의 mailable마다 입력하는 것이 번거로울 수 있습니다. 이럴 때 `config/mail.php` 파일에 글로벌 "from" 주소를 지정하면, 개별 Mailable에서 따로 지정하지 않아도 이 주소가 사용됩니다.

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

글로벌 "reply_to" 주소도 마찬가지 방법으로 지정할 수 있습니다.

```php
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰 설정

Mailable 클래스의 `content` 메서드에서 어떤 템플릿을 사용할지(view)를 지정할 수 있습니다. 대부분 [Blade 템플릿](/docs/{{version}}/blade)을 사용하며, Blade의 모든 기능을 자유롭게 활용할 수 있습니다.

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
> 이메일 템플릿은 별도의 `resources/views/emails` 디렉토리를 만들어 관리하는 것이 좋지만, 원하는 곳에 자유롭게 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 만들고 싶다면, message의 `Content` 정의에서 plain-text 템플릿을 지정하면 됩니다. `view` 파라미터처럼 `text`에도 템플릿명을 넣습니다.

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

명확성을 위해 `html` 파라미터도 `view`의 별칭으로 사용할 수 있습니다.

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### 퍼블릭 프로퍼티를 통한 데이터 전달

뷰에서 사용할 데이터를 전달하고 싶으면, Mailable 클래스의 public 프로퍼티를 이용할 수 있습니다. 생성자에서 데이터를 받아 public 프로퍼티에 할당하세요.

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

이렇게 하면 Blade 템플릿에서 `$order->price`처럼 접근할 수 있습니다.

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 사용

템플릿에 전달하는 데이터를 커스터마이징 하고 싶다면, `Content` 정의의 `with` 파라미터를 사용하세요. 이런 경우 생성자에서는 protected/protected/private 프로퍼티에 값을 넣어야 템플릿에 자동 노출되지 않습니다.

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

템플릿에서는 다음과 같이 사용할 수 있습니다.

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메시지의 `attachments` 메서드에서 배열로 반환하면 됩니다. 예시는 다음과 같습니다.

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

첨부 파일의 표시 이름 및 MIME 타입은 `as`와 `withMime`로 지정할 수 있습니다.

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

[파일 시스템 디스크](/docs/{{version}}/filesystem) 중 하나에 저장한 파일을 첨부하려면, `fromStorage`를 사용하세요.

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

첨부파일의 이름과 MIME 타입도 지정 가능합니다.

```php
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

기본 디스크 대신 다른 디스크를 사용하려면 `fromStorageDisk`를 쓰세요.

```php
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

메모리 내의 바이트 스트링을 직접 첨부하려면 `fromData`를 사용하세요. 예를 들어, PDF를 메모리에서 만들어 디스크에 저장하지 않고 첨부할 때 유용합니다.

```php
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

이메일에 인라인 이미지를 삽입하려면, 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하세요. 이 변수는 Laravel이 자동으로 주입합니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에서는 사용할 수 없습니다. Plain-text 메시지는 인라인 첨부파일을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

이미지를 raw 데이터로 가지고 있다면 `embedData` 메서드로 첨부할 수 있습니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

파일 경로만으로 첨부하는 대신, 애플리케이션의 객체(예: Photo 모델)를 첨부하고 싶을 때가 있습니다. 이런 경우를 위해 Attachable 객체를 사용할 수 있습니다.

먼저, 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하고 `toMailAttachment` 메서드를 정의하세요.

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

이렇게 하면, 메일 작성 시 해당 객체를 그대로 `attachments`에서 반환할 수 있습니다.

```php
public function attachments(): array
{
    return [$this->photo];
}
```

데이터가 S3와 같은 원격 파일 스토리지에 있다면, [파일 시스템 디스크](/docs/{{version}}/filesystem)에서 `fromStorage` 및 `fromStorageDisk`를 사용할 수 있습니다.

```php
return Attachment::fromStorage($this->path);

// 또는 특정 디스크 사용 시
return Attachment::fromStorageDisk('backblaze', $this->path);
```

메모리 내 데이터를 첨부하고 싶으면 `fromData`에 클로저를 넘기세요.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

`as`, `withMime` 등 추가 커스터마이징 메서드도 지원합니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

특정 상황에서는 메일에 추가 헤더를 붙여야 할 수도 있습니다(예: custom Message-Id 등). 이럴 경우, mailable에 `headers` 메서드를 추가하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환합니다.

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

Mailgun, Postmark 등 일부 이메일 서비스는 메시지 "태그"와 "메타데이터"를 지원해서, 그룹별 추적이 가능합니다. `Envelope` 정의에서 tags와 metadata를 추가할 수 있습니다.

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

Mailgun의 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages), Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)를 참조하세요.

Amazon SES를 사용하는 경우, `metadata` 메서드로 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메일에 추가해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony Message 커스터마이징

Laravel의 메일 기능은 Symfony Mailer로 구현되어 있습니다. Symfony Message 인스턴스를 직접 커스터마이징하고 싶으면, `Envelope` 정의에서 `using` 파라미터로 콜백을 등록하면 됩니다.

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
## 마크다운(Markdown) Mailable

마크다운 메일러는 [메일 알림](/docs/{{version}}/notifications#mail-notifications)의 기본 템플릿과 컴포넌트를 mailable에서도 활용할 수 있도록 해줍니다. 마크다운으로 메시지를 작성하면 Laravel이 자동으로 보기 좋은 HTML과 plain-text 버전을 모두 렌더링해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 Mailable 생성

마크다운 템플릿과 연결된 mailable을 생성하려면, `make:mail` 아티즌 명령어에 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그런 다음, mailable의 `content` 메서드에서 `view` 대신 `markdown`을 지정합니다.

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

마크다운 Mailable에서는 Blade 컴포넌트와 마크다운 문법을 조합해서, 간단하게 보기 좋은 메일 메시지를 만들 수 있습니다.

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
> 마크다운 이메일을 쓸 때 불필요한 들여쓰기는 피하세요. 표준 마크다운 파서에서는 들여쓴 내용을 코드 블록으로 렌더링합니다.

<a name="button-component"></a>
#### Button 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 만들어줍니다. `url`과 선택적 `color` 속성을 받을 수 있습니다. 색상 옵션은 `primary`, `success`, `error`입니다. 버튼은 여러 개 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### Panel 컴포넌트

Panel 컴포넌트는 메시지 중 원하는 블록을 배경색이 다른 패널에 넣어서 강조할 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### Table 컴포넌트

Table 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환해줍니다. 표 정렬도 마크다운 표 문법 그대로 지원됩니다.

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

마크다운 메일 컴포넌트 전체를 내 프로젝트로 복사해서 수정할 수 있습니다. 다음 artisan 명령어로 `laravel-mail` asset 태그를 퍼블리시하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

그러면 `resources/views/vendor/mail` 디렉토리 아래에 `html`과 `text` 폴더가 만들어지고, 각종 컴포넌트가 담겨있습니다. 마음대로 커스터마이즈하세요.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보내면, `resources/views/vendor/mail/html/themes` 폴더에 `default.css` 파일이 생깁니다. 이 파일을 수정하면 스타일이 자동으로 HTML 메일에 인라인으로 적용됩니다.

마크다운 컴포넌트만을 위한 새로운 테마를 만들고 싶으면, `html/themes` 폴더에 CSS 파일을 만들고, `config/mail.php`의 `theme` 옵션을 해당 파일명으로 지정합니다.

특정 Mailable에만 테마를 다르게 하고 싶으면, 해당 클래스의 `$theme` 프로퍼티에 원하는 테마명을 지정하면 됩니다.

<a name="sending-mail"></a>
## 이메일 발송

이메일을 보내려면 [Mail 파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용합니다. 이 메서드는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션을 받을 수 있습니다. 객체를 전달하면 `email`, `name` 속성이 있는지 확인하세요. 그 다음 `send`에 mailable 인스턴스를 넘겨주면 됩니다.

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

"To" 주소 외에도 "cc", "bcc"를 체이닝해서 지정할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

한 명씩 다른 메일을 보내야 한다면, 매 반복마다 새로운 mailable 인스턴스를 만들어야 합니다. 그렇지 않으면 이전 수신자도 같이 들어갈 수 있습니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

Laravel은 기본적으로 `mail` 설정 파일의 `default` 메일러를 사용하지만, `mailer` 메서드로 특정 메일러를 사용할 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐에 넣기

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 발송은 응답 속도에 영향을 미칠 수 있어, 보통 백그라운드 큐잉 작업으로 처리합니다. 메일을 큐에 넣으려면, `Mail` 파사드에서 `queue`를 호출하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 방법을 쓰려면 [큐 설정](/docs/{{version}}/queues)이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 지연 큐잉

메일 발송을 지연시키려면 `later` 메서드에 발송시각을 지정하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/커넥션에 넣기

`make:mail`로 만든 모든 mailable은 `Illuminate\Bus\Queueable` 트레이트를 포함하므로, mailable 인스턴스에서 `onQueue`, `onConnection`을 호출해 연결명/큐명을 지정할 수 있습니다.

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
#### 무조건 큐잉

항상 큐잉이 되도록 하고 싶으면, 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이러면 `send`로 보내도 큐에 쌓입니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉과 DB 트랜잭션

큐잉된 mailable이 데이터베이스 트랜잭션 내부에서 디스패치되면, 큐 워커가 DB 트랜잭션 커밋 전에 작업을 처리할 수 있습니다. 이럴 때 최신 DB 상태가 반영되지 않을 수 있습니다. 이런 상황이 걱정된다면, 큐 커넥션의 `after_commit` 옵션이 `false`일 때, mailable을 보내며 `afterCommit`을 호출하면 반드시 커밋 이후에 발송됩니다.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

아니면 mailable 생성자에서 호출하세요.

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
> 이와 관련된 자세한 내용은 [큐 작업과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## Mailable 렌더링

때때로 메일을 실제로 보내지 않고, mailable의 HTML을 문자열로 얻고 싶을 때가 있습니다. 이럴 땐 `render` 메서드를 사용하세요.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 Mailable 미리보기

메일 템플릿을 만들 때, Blade 템플릿처럼 직접 브라우저에서 결과물을 미리 볼 수 있습니다. 라우트 혹은 컨트롤러에서 mailable을 그대로 반환하면 됩니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## Mailable 지역화

Laravel은 요청의 현재 로캘이 아닌 다른 언어로도 mailable을 보낼 수 있으며, 메일이 큐잉되어 있어도 해당 로캘을 기억합니다.

이를 위해 `Mail` 파사드의 `locale` 메서드를 사용하면 됩니다. mailable의 템플릿을 평가하는 동안 언어가 전환되고, 완료되면 다시 돌아옵니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로캘

애플리케이션이 사용자별 선호 언어를 저장한다면, 모델에 `HasLocalePreference` 인터페이스를 구현하여, 자동으로 해당 로캘로 메일/알림을 보낼 수 있습니다.

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

이 인터페이스를 구현하면, 별도로 `locale` 메서드를 호출하지 않아도 자동으로 선호 로캘이 적용됩니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### Mailable 내용 테스트

Laravel은 mailable의 구조와 내용을 확인할 수 있는 다양한 메서드를 제공합니다. 대표적으로 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등이 있습니다.

"HTML" 계열은 mailable의 HTML 버전에 문자열이 들어있는지, "text" 계열은 plain-text 버전에 있는지 검사합니다.

<details>
<summary>예시(Pest)</summary>

```php
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
</details>

<details>
<summary>예시(PHPUnit)</summary>

```php
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
</details>

<a name="testing-mailable-sending"></a>
### Mailable 발송 테스트

mailable의 내용을 테스트하는 것과, 특정 mailable이 발송되었는지 테스트하는 것은 별도로 할 것을 권장합니다. 내용 검증보다는, 지정한 mailable이 실제로 발송되도록 명령되었는지를 확인하면 충분할 경우가 많기 때문입니다.

메일 발송을 실제로 막으려면 `Mail` 파사드의 `fake`를 사용하세요. 그리고 나서 각종 assert 메서드로 메일이 발송(혹은 큐잉)됐는지, 누구에게 갔는지 등을 검사하세요.

<details>
<summary>예시(Pest)</summary>
  
```php
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
</details>

<details>
<summary>예시(PHPUnit)</summary>

```php
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
</details>

큐에 넣은 메일이면, `assertSent` 대신 `assertQueued`를 사용하세요.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

콜백을 넘기면, 특정 조건을 검사할 수 있습니다. 

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

콜백에서 mailable 인스턴스가 제공되며, 다양한 검사 메서드를 쓸 수 있습니다.

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

첨부파일 관련 검사도 지원합니다.

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

메일이 **발송도, 큐잉도 전혀 되지 않았음**을 검사할 땐 `assertNothingOutgoing`, `assertNotOutgoing`를 사용하세요.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

개발 중에는 실제 이메일이 발송되지 않게 하는 다양한 방법이 있습니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 메일을 실제로 보내지 않고 로그 파일에 기록합니다. 주로 로컬 개발에서 사용됩니다.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

[HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io) 등과 `smtp` 드라이버를 조합하면, 진짜 이메일 클라이언트로 메일을 확인할 수 있는 "더미" 메일 박스를 사용할 수 있습니다. [Laravel Sail](/docs/{{version}}/sail) 사용 시 [Mailpit](https://github.com/axllent/mailpit)으로 `http://localhost:8025`에서 볼 수도 있습니다.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

모든 메일을 임시 주소로 강제로 보내고 싶다면, `Mail` 파사드의 `alwaysTo`를 사용하세요. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

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

Laravel은 메일 발송 전후에 `MessageSending`, `MessageSent` 두 이벤트를 dispatch합니다. (큐잉 시점이 *아니라*, 실제로 메일이 전송될 때 발생합니다.) 필요하면 [이벤트 리스너](/docs/{{version}}/events)를 만들어서 사용할 수 있습니다.

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
## 커스텀 트랜스포트

Laravel이 기본으로 제공하지 않는 다른 이메일 서비스를 통해 메일을 보내고 싶다면, 커스텀 트랜스포트를 작성할 수 있습니다. `Symfony\Component\Mailer\Transport\AbstractTransport`를 상속하고, `doSend` 및 `__toString()`을 구현하세요.

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

작성한 트랜스포트는 `Mail` 파사드의 `extend` 메서드로 등록하세요. 보통 `AppServiceProvider`의 `boot`에서 처리합니다. `$config`에는 `config/mail.php`의 mailer 설정 배열이 넘어옵니다.

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

트랜스포트 등록 후에는 `config/mail.php`에 mailer를 추가하세요.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

Laravel은 기본적으로 Mailgun, Postmark 등 Symfony에서 유지하는 드라이버 일부만 내장하고 있습니다. 추가 Symfony 트랜스포트를 사용하려면 관련 패키지를 설치하고 mailer에 등록하면 됩니다.

예를 들어, "Brevo" 트랜스포트를 설치하고 등록하는 방법은 다음과 같습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후 `services` 설정 파일에 API 키를 추가하세요.

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

서비스 프로바이더의 `boot` 메서드에서 트랜스포트를 등록하세요.

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

마지막으로, `config/mail.php`에 mailer를 추가하세요.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
