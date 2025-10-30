# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버/전송 방식의 사전 준비](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [Mailable 클래스 생성](#generating-mailables)
- [Mailable 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [Markdown Mailable](#markdown-mailables)
    - [Markdown Mailable 생성](#generating-markdown-mailables)
    - [Markdown 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 큐 처리](#queueing-mail)
- [Mailable 렌더링](#rendering-mailables)
    - [브라우저에서 Mailable 미리보기](#previewing-mailables-in-the-browser)
- [Mailable 로컬라이징](#localizing-mailables)
- [테스트](#testing-mailables)
    - [Mailable 내용 테스트](#testing-mailable-content)
    - [Mailable 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일을 발송하는 일은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깨끗하고 단순한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 포함한 다양한 이메일 전송 드라이버를 지원하므로, 로컬 또는 클라우드 기반 서비스 중 원하는 방법으로 쉽게 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내에 정의된 각 메일러(mailer)는 고유한 설정 및 "전송 방식(transport)"을 가질 수 있으므로, 다양한 이메일 서비스를 상황에 맞게 사용할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일 안에는 `mailers` 배열이 있으며, 이 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송 방식 예제가 포함되어 있습니다. 메일을 보낼 때 기본적으로 사용할 메일러는 `default` 설정 값으로 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/전송 방식의 사전 준비 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend와 같은 API 기반 드라이버는 SMTP 서버를 통한 메일 발송보다 대체로 더 쉽고 빠릅니다. 가능하다면 이런 드라이버를 사용할 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 전송 패키지를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 파일에서 두 가지 변경이 필요합니다. 먼저, 기본 메일러를 `mailgun`으로 지정하세요:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

두 번째로, `mailers` 배열에 다음과 같은 설정을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이후, `config/services.php` 파일에 다음 옵션을 추가합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국이 아닌 다른 [Mailgun 지역](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용한다면, `services` 설정 파일에서 해당 지역의 endpoint를 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer로 Symfony의 Postmark Mailer 전송 패키지를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그다음, 애플리케이션의 `config/mail.php`에서 `default` 값을 `postmark`로 설정해야 합니다. 또한, `config/services.php` 파일에 다음 옵션이 포함되어 있는지 확인하세요:

```php
'postmark' => [
    'key' => env('POSTMARK_API_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하고 싶으면, 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 배열은 `config/mail.php` 파일에 위치합니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이 방법으로 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러도 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer로 Resend의 PHP SDK를 설치합니다:

```shell
composer require resend/resend-php
```

그다음, `config/mail.php` 파일의 `default` 값을 `resend`로 설정하세요. 그리고 `config/services.php` 파일에 다음 옵션이 포함되어 있어야 합니다:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 우선 Amazon AWS SDK for PHP를 설치해야 합니다. Composer를 통해 다음과 같이 설치하세요:

```shell
composer require aws/aws-sdk-php
```

이후, `config/mail.php` 파일에서는 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 다음 옵션이 포함되어 있는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 이용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 추가하면 됩니다:

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

Laravel이 이메일을 보낼 때 AWS SDK의 `SendEmail` 메서드에 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 전달하도록 하고 싶다면, SES 설정에 `options` 배열을 지정할 수 있습니다:

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
### 장애 조치(failover) 설정 (Failover Configuration)

애플리케이션의 메일 전송을 담당하는 외부 서비스가 다운될 수 있습니다. 이런 경우를 대비해 기본(주) 발송 드라이버에 문제가 생겼을 때 사용할 백업 메일 전달 설정을 정의해 두는 것이 유용합니다.

이를 위해서는, 애플리케이션의 `mail` 설정 파일에 `failover` 전송 방식을 사용하는 메일러를 정의하세요. 이 `failover` 메일러 설정 배열에는 실제 메일 전송에 사용할 메일러들의 목록을 `mailers` 배열로 명시합니다:

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

failover 메일러를 정의했다면, `mail` 설정 파일의 `default` 값에 해당 메일러 이름을 지정하여 기본 메일러로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈 설정 (Round Robin Configuration)

`roundrobin` 전송 방식은 여러 메일러로 메일 발송 작업을 분산시킬 수 있습니다. 사용하려면, `mail` 설정 파일에 `roundrobin` 전송 방식의 메일러를 정의하세요. 이 메일러 설정에서는 실제로 사용할 메일러를 `mailers` 배열에 나열합니다:

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

round robin 메일러를 정의했다면, 마찬가지로 이를 기본 메일러로 `default` 값에 지정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 전송 방식은 설정된 메일러 목록 중 하나를 무작위로 선택하여 메일을 발송하고, 이후 메일마다 다음 메일러로 순차적으로 전환합니다. `failover` 전송 방식이 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)* 을 목표로 한다면, `roundrobin`은 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 을 제공합니다.

<a name="generating-mailables"></a>
## Mailable 클래스 생성 (Generating Mailables)

Laravel 애플리케이션에서 발송하는 각 유형의 메일은 “mailable” 클래스로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없다면, `make:mail` Artisan 명령어로 mailable 클래스를 생성할 때 자동으로 생성됩니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 클래스 작성 (Writing Mailables)

mailable 클래스를 생성했다면, 열어서 내용을 살펴보세요. mailable 클래스의 설정은 `envelope`, `content`, `attachments` 메서드 등에서 이루어집니다.

`envelope` 메서드는 메시지의 제목과(필요에 따라) 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용 생성에 사용할 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope로 설정하기

이메일의 발신자(즉, 'from' 주소)에 대해 설정해봅시다. 발신자는 두 가지 방법으로 설정할 수 있습니다. 첫 번째는 메시지의 envelope에 "from" 주소를 명시하는 방법입니다:

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

원한다면 `replyTo` 주소도 지정할 수 있습니다:

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
#### 글로벌 `from` 주소 사용하기

모든 이메일에 동일한 "from" 주소를 사용할 경우, 매번 mailable 클래스마다 지정하는 것은 번거로울 수 있습니다. 이럴 땐, `config/mail.php` 파일에서 글로벌 "from" 주소를 설정할 수 있습니다. mailable 클래스에서 별도로 지정하지 않는 한 이 글로벌 주소가 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, 글로벌 "reply_to" 주소도 정의할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰 설정 (Configuring the View)

mailable 클래스의 `content` 메서드에서 어떤 뷰(템플릿)를 사용할지 정의할 수 있습니다. 각 이메일은 [Blade 템플릿](/docs/12.x/blade)을 사용하여 HTML을 렌더링하므로, Blade의 강력함을 모두 사용할 수 있습니다:

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
> 이메일 템플릿을 보관할 `resources/views/mail` 디렉터리를 만드는 것이 좋지만, `resources/views` 디렉터리 내 어디든 자유롭게 저장할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하고 싶다면, 메시지의 `Content` 정의에서 plain-text 템플릿을 지정할 수 있습니다. `text` 파라미터에는 Blade처럼 템플릿명을 입력하고, HTML 버전과 일반 텍스트 버전을 모두 정의할 수 있습니다:

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

참고로, `html` 파라미터를 `view` 파라미터의 별칭처럼 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성을 통한 전달

이메일 내용 HTML을 렌더링할 때 사용할 데이터를 뷰에 전달하고 싶을 것입니다. 데이터를 뷰에 전달하는 방법은 두 가지가 있습니다. 첫 번째는, mailable 클래스에 public 속성(public property)으로 데이터를 설정하면 뷰에서 자동으로 사용할 수 있습니다. 예를 들어, 생성자에 데이터를 받아서 public 속성에 할당하면 됩니다:

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

public 속성으로 데이터를 저장하면 뷰에서 바로 사용할 수 있으므로, Blade 템플릿에서 일반 데이터처럼 접근 가능합니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

이메일에 전달할 데이터의 포맷을 직접 커스터마이징하고 싶다면, `Content` 정의의 `with` 파라미터를 통해 뷰에 데이터를 넘길 수 있습니다. 대개는 생성자에서 데이터를 받고, protected 또는 private 속성에 저장한 후 템플릿에는 `with`로 전달합니다(이 경우 자동으로 공용 속성을 통해 뷰로 전달되지는 않습니다):

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

`with` 파라미터로 전달된 데이터는 뷰에서 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드에서 반환되는 배열에 첨부 파일을 추가하면 됩니다. 우선, `Attachment` 클래스의 `fromPath` 메서드를 사용해 파일 경로로 첨부할 수 있습니다:

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

파일 첨부시 `as`(파일 표시 이름)와 `withMime`(MIME 타입) 메서드로 파일명을 변경하거나 MIME 타입을 지정할 수 있습니다:

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

[파일 시스템 디스크](/docs/12.x/filesystem)에 파일이 저장되어 있다면, `fromStorage` 메서드로 첨부할 수 있습니다:

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

역시 파일명 및 MIME 타입 지정이 가능합니다:

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

기본 디스크 이외의 디스크를 사용하려면 `fromStorageDisk`를 사용하세요:

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

`fromData` 메서드를 사용하면 바이트 문자열(raw data)을 첨부로 추가할 수 있습니다. 예를 들어, 메모리 상에서 PDF 파일을 생성한 경우 파일로 저장하지 않고 바로 첨부할 수 있습니다. `fromData`에는 raw 데이터 바이트를 반환하는 클로저와 첨부 파일의 이름을 전달합니다:

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
### 인라인 첨부 파일 (Inline Attachments)

이메일에 인라인 이미지를 삽입하는 일은 보통 번거롭지만, Laravel은 이를 편리하게 처리할 수 있는 기능을 제공합니다. 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 이미지를 인라인으로 첨부할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에서 자동으로 사용할 수 있습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 메일 템플릿에서는 사용할 수 없습니다. plain-text 메일에는 인라인 첨부 파일 기능이 적용되지 않습니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터로 인라인 첨부 이미지 삽입

만약 raw 이미지 데이터 문자열이 이미 있다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이때 이미지를 식별할 파일 이름도 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체 (Attachable Objects)

단순히 파일 경로만으로 첨부하는 대신, 애플리케이션 내의 객체(예: Photo 모델 등)를 첨부할 수 있다면 더욱 편리합니다. 이를 위해선 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다. 이 인터페이스는 `toMailAttachment` 메서드를 정의하도록 요구하며, 여기서 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

Attachable 객체를 정의했다면, 이메일 메시지의 `attachments` 메서드에서 해당 객체를 반환할 수 있습니다:

```php
public function attachments(): array
{
    return [$this->photo];
}
```

첨부 데이터가 원격 파일 스토리지(Amazon S3 등)에 저장되어 있을 수도 있으므로, Laravel은 [파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 기반으로 첨부 인스턴스를 생성하는 것도 지원합니다:

```php
// 기본 디스크에서 파일로 첨부
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일로 첨부
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 있는 데이터로 첨부 객체를 생성할 수도 있습니다. 이때는 `fromData` 메서드에 raw 데이터를 반환하는 클로저를 전달합니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부 파일의 이름과 MIME 타입은 `as`, `withMime` 메서드로 자유롭게 지정할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

가끔 발송되는 메시지에 추가적인 헤더가 필요할 수 있습니다(예: 커스텀 `Message-Id` 또는 임의의 텍스트 헤더 지정 등).

이럴 땐 mailable에 `headers` 메서드를 정의하고, `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하면 됩니다. 이 클래스는 `messageId`, `references`, `text` 파라미터를 지원하며, 필요한 값만 지정하면 됩니다:

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

Mailgun, Postmark와 같은 일부 외부 이메일 제공업체는 "태그(tags)"와 "메타데이터(metadata)"를 지원하며, 이를 통해 애플리케이션에서 발송되는 이메일을 그룹화하고 추적할 수 있습니다. 이런 태그와 메타데이터는 `Envelope` 정의에서 추가할 수 있습니다:

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

Mailgun, Postmark에 대한 태그 및 메타데이터 자세한 내용은 각 서비스의 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags), [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages), [Postmark 태그](https://postmarkapp.com/blog/tags-support-for-smtp), [Postmark 메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서를 참고하세요.

Amazon SES를 통해 메일을 발송할 경우에는 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가할 때 `metadata` 메서드를 이용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징 (Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer 플랫폼을 기반으로 동작합니다. 메시지가 전송되기 전, Symfony Message 인스턴스에서 직접 커스터마이징할 수 있도록 콜백을 등록할 수 있습니다. 이를 위해 `Envelope` 정의에 `using` 파라미터를 추가하면 됩니다:

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
## Markdown Mailable (Markdown Mailables)

Markdown mailable 메시지를 사용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿 및 컴포넌트를 mailable에도 활용할 수 있습니다. 메시지가 Markdown으로 작성되었기 때문에, Laravel은 아름답고 반응형인 HTML 템플릿은 물론 plain-text 버전도 자동으로 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### Markdown Mailable 생성 (Generating Markdown Mailables)

Markdown 템플릿이 연계된 mailable을 생성하려면 `make:mail` Artisan 명령어에서 `--markdown` 옵션을 사용합니다:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후 mailable의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용하여 Content를 정의합니다:

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
### Markdown 메시지 작성 (Writing Markdown Messages)

Markdown mailable은 Blade 컴포넌트와 Markdown 문법을 조합하여, Laravel에서 제공하는 이메일 UI 컴포넌트를 이용해 쉽게 메일 메시지를 작성할 수 있습니다:

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
> Markdown 이메일을 작성할 때 들여쓰기를 과도하게 사용하지 마세요. Markdown 표준에 따라, 들여쓰기된 내용은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. `url`, 선택적 `color` 인자를 지원하며, 지원 색상은 `primary`, `success`, `error`입니다. 메시지 안에 여러 개의 버튼 컴포넌트를 쓸 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 배경색이 살짝 다른 패널로 표현하여, 특정 내용을 강조할 수 있게 해줍니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 Markdown 테이블을 HTML 테이블로 변환해줍니다. 컴포넌트의 내용으로 Markdown 테이블을 넣으면 되고, 표 컬럼 정렬도 기본 Markdown 문법을 따릅니다:

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

Markdown 메일 컴포넌트를 여러분의 애플리케이션에 복사하여 자유롭게 커스터마이징할 수 있습니다. 컴포넌트 내보내기는 `vendor:publish` Artisan 명령어를 사용하여 `laravel-mail` 에셋 태그를 퍼블리시 하면 됩니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어로 `resources/views/vendor/mail` 디렉터리에 Markdown 메일 컴포넌트가 퍼블리시됩니다. 이 `mail` 디렉터리에는 HTML/텍스트별 하위 디렉터리가 있으며, 원하는 대로 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 내보내기 후, `resources/views/vendor/mail/html/themes`에 `default.css` 파일이 생성됩니다. 이 파일의 CSS를 수정하면 스타일이 자동으로 이메일의 HTML 내에 인라인 스타일로 적용됩니다.

만약 Laravel Markdown 컴포넌트에 대해 완전히 새로운 테마를 만들고자 한다면, 해당 디렉터리에 CSS 파일을 추가하고, `config/mail.php`의 `theme` 옵션에 테마 이름을 지정해주면 됩니다.

특정 mailable에서 별도의 테마를 사용하고 싶다면, mailable 클래스의 `$theme` 속성에 사용할 테마명을 지정하세요.

<a name="sending-mail"></a>
## 메일 발송 (Sending Mail)

메시지를 보내려면 [Mail 파사드](/docs/12.x/facades)의 `to` 메서드를 사용하세요. `to`는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션을 받을 수 있습니다. 객체나 컬렉션을 전달하면 해당 객체의 `email`, `name` 속성을 이용해 자동으로 수신자를 결정하므로, 이 속성이 정의되어 있어야 합니다. 수신자를 지정한 뒤, mailable 클래스 인스턴스를 `send` 메서드에 전달하면 됩니다:

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

수신자("to")만 지정하는 것이 아니라, "cc", "bcc"도 체이닝 메서드로 설정할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

리스트에 있는 여러 수신자에게 메일을 반복 발송해야 할 경우가 있을 수 있습니다. `to` 메서드는 수신자 목록에 이메일을 계속 추가하기 때문에, 반복문 내에서 mailable 인스턴스를 매번 새로 생성해야 합니다. 그렇지 않으면 메일이 이전 모든 수신자에게 중복 발송됩니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 발송

Laravel은 기본적으로 `mail` 설정 파일의 `default` 메일러를 사용하지만, `mailer` 메서드를 이용해 특정 메일러를 명시할 수도 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐 처리 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐 등록

이메일 발송이 애플리케이션 응답 속도에 악영향을 줄 수 있으므로, 많은 개발자들이 이메일을 백그라운드에서 비동기로 발송(큐 처리)합니다. Laravel은 [통합 큐 API](/docs/12.x/queues)를 통해 이를 손쉽게 지원합니다. 메일 메시지를 큐에 등록하려면 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 이메일 발송 작업을 자동으로 큐에 넣어, 백그라운드에서 작업이 실행되게 합니다. 이 기능을 사용하려면 [큐를 미리 설정](/docs/12.x/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 딜레이된 메시지 큐

큐에 등록된 이메일 발송을 지정한 시간만큼 지연시키고 싶다면 `later` 메서드를 사용할 수 있습니다. 첫 번째 인자로 언제 보낼지 `DateTime` 인스턴스를 전달하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐로 메시지 추가

`make:mail` 명령어로 생성한 모든 mailable 클래스에는 `Illuminate\Bus\Queueable` 트레이트가 적용되어 있으므로, mailable 인스턴스에서 `onQueue`, `onConnection` 메서드를 호출해 큐 이름이나 연결명을 지정할 수 있습니다:

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
#### 기본적으로 큐 처리하기

특정 mailable 클래스가 항상 큐에서 처리되길 원한다면, 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이렇게 하면 `send`로 메일을 보내더라도 무조건 큐에 등록하게 됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 메일과 데이터베이스 트랜잭션

큐에 등록된 메일러가 데이터베이스 트랜잭션 내에서 실행될 때, 큐가 트랜잭션 커밋 이전에 처리될 위험이 있습니다. 이 경우, 트랜잭션 내에서 수정/추가한 데이터가 아직 데이터베이스에 반영되지 않았을 수 있으므로, 큐가 처리되면 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`인 경우에도, 메일 발송 작업이 모든 열린 데이터베이스 트랜잭션 커밋 후 처리되도록 하려면, 메일러 인스턴스를 생성할 때 `afterCommit` 메서드를 호출하세요:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 mailable의 생성자에서 `afterCommit`를 호출할 수도 있습니다:

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
> 이런 이슈에 대한 더 자세한 workaround는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐 메일 발송 실패 처리

큐로 발송되는 메일이 실패할 경우, mailable 클래스에 `failed` 메서드가 정의되어 있다면 해당 메서드가 호출됩니다. 실패 원인인 `Throwable` 인스턴스가 인자로 전달됩니다:

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
## Mailable 렌더링 (Rendering Mailables)

가끔 메일을 실제로 보내지 않고, mailable의 HTML 컨텐츠만 가져와서 활용하고 싶을 수 있습니다. 이럴 때는 mailable의 `render` 메서드를 호출하세요. 이 메서드는 렌더링된 HTML 컨텐츠를 문자열로 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 Mailable 미리보기

메일 템플릿을 디자인할 때 실제 이메일을 발송하지 않고 브라우저에서 바로 렌더링 결과를 미리 보는 것이 편리합니다. Laravel에서는 route 클로저 혹은 컨트롤러에서 mailable을 바로 반환하면, 실제 메일 전송 없이 렌더링 결과가 브라우저에 표시됩니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## Mailable 로컬라이징 (Localizing Mailables)

Laravel은 요청의 현재 로케일과 다르게 mailable을 다른 언어로 보낼 수 있도록 지원하며, 이 로케일 설정은 메일이 큐에 들어가도 기억됩니다.

이를 위해, `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정할 수 있습니다. mailable의 템플릿이 렌더링되는 동안에는 이 로케일이 적용되고, 평가가 끝나면 이전 로케일로 돌아갑니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 언어 사용

애플리케이션에서 사용자별 선호 로케일을 저장하는 경우도 있습니다. 이럴 땐 모델에 `HasLocalePreference` 계약을 구현하면, 메일 발송 시 해당 사용자의 저장된 로케일이 자동으로 사용됩니다:

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

이 인터페이스를 구현한 후에는, Laravel이 자동으로 해당 로케일을 사용하여 메일과 알림을 발송하므로 `locale` 메서드를 따로 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### Mailable 내용 테스트 (Testing Mailable Content)

Laravel은 mailable 구조 및 컨텐츠 검사를 위한 다양한 메서드를 제공합니다. 다음은 mailable이 기대한 내용을 담고 있는지 검증할 수 있는 여러 방법입니다:

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

여기서 "HTML" 관련 assertion은 mailable의 HTML 버전에, "text" assertion은 plain-text 버전에 문자열이 포함되는지 확인합니다.

<a name="testing-mailable-sending"></a>
### Mailable 발송 테스트 (Testing Mailable Sending)

mailable의 내용 테스트와, 특정 mailable이 특정 사용자에게 "발송"되었다는 점에 대한 테스트는 구분하는 것이 좋습니다. 실제 코드에서는 mailable 내용보다 "발송 여부"만 중요할 때가 많기 때문에, 해당 사실만을 assert하면 충분합니다.

메일 발송을 실제로 중단하려면 `Mail` 파사드의 `fake` 메서드를 사용합니다. fake 상태에서 mailables가 특정 사용자에게 발송 요청되었는지를 assert 할 수 있고, 전달된 데이터를 점검할 수도 있습니다:

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

만약 메일을 큐를 통해 백그라운드로 발송할 때는 `assertSent` 대신 `assertQueued`를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 클로저를 전달하여 "특정 조건을 만족하는" mailable이 발송(혹은 미발송)되었는지 검사할 수도 있습니다. 클로저 조건을 만족하는 mailable이 1개라도 있으면 assertion이 성공합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

이 클로저의 인자인 mailable 인스턴스는 다양한 내부 정보 확인 메서드를 제공합니다:

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

또한, 첨부 파일에 대한 검사 메서드도 포함되어 있습니다:

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

메일이 발송되지(큐 등록되지) 않았음을 검사하는 방법에는 `assertNotSent`, `assertNotQueued` 두 가지가 있습니다. 메일이 **전혀** 발송(또는 큐 등록)되지 않았음을 확인하려면 `assertNothingOutgoing`, 특정 메일이 발송(혹은 큐 등록)되지 않았음을 검사하려면 `assertNotOutgoing`을 사용할 수 있습니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

애플리케이션 개발 중 실제 이메일을 실사용 주소로 보내는 것은 위험할 수 있습니다. Laravel은 실제 이메일 발송을 “비활성화”하는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### Log 드라이버

`log` 메일 드라이버를 사용하면 이메일을 실제로 보내지 않고, 로그 파일에 메일 내용을 남깁니다. 주로 로컬 개발 환경에서 사용되며, 환경별 설정 방법은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)과 같은 서비스를 이용하거나, `smtp` 드라이버를 통해 이메일을 외부로 보내지 않고 임시 메일박스에서 확인할 수도 있습니다. 이런 서비스를 이용하면 실제 이메일 클라이언트에서 최종 메일을 확인할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용한다면, [Mailpit](https://github.com/axllent/mailpit) 을 통해 메시지 미리보기도 가능합니다. Sail 실행 중에는 `http://localhost:8025`에서 Mailpit 인터페이스를 확인하세요.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

마지막으로, 개발/테스트 환경에서 모든 메일을 특정 주소로 보내고 싶을 땐 `Mail` 파사드의 `alwaysTo` 메서드를 사용할 수 있습니다. 일반적으로 한 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

`alwaysTo` 메서드를 사용할 경우, 메일 메시지의 추가 "cc"나 "bcc" 주소는 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 메시지를 발신하는 과정에서 두 가지 이벤트를 발생시킵니다. 메시지 전송 전에 `MessageSending`, 전송 후에 `MessageSent` 이벤트가 발생합니다. 이 이벤트는 메일이 *실제로 발송*될 때 발생하며, 큐에 등록될 때는 발생하지 않습니다. 이 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내부에 생성할 수 있습니다:

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

Laravel은 다양한 메일 전송 방식을 내장하고 있지만, Laravel이 기본적으로 지원하지 않는 외부 서비스로 이메일을 보내고 싶다면, 직접 전송 방식을 구현할 수 있습니다. 이를 위해 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속받아, `doSend`와 `__toString` 메서드를 구현합니다:

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

커스텀 전송 방식을 정의했다면, `Mail` 파사드의 `extend` 메서드로 등록해야 합니다. 일반적으로는 `AppServiceProvider`의 `boot` 메서드에서 등록합니다. 클로저에는 `config/mail.php`에서 해당 메일러에 지정한 설정 배열이 `$config`로 전달됩니다:

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

그 다음, `config/mail.php` 설정 파일에서 새 전송 방식을 사용하는 메일러 정의를 추가합니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식 (Additional Symfony Transports)

Laravel은 기본적으로 Mailgun, Postmark 등의 공식 Symfony 메일 전송 방식을 지원합니다. 이 외에 다른 Symfony 전송 방식도 Composer로 메일러 패키지를 설치하고 등록해 사용할 수 있습니다. 예를 들어, "Brevo"(이전 이름: "Sendinblue") Symfony 메일러를 설치하려면:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, 애플리케이션의 `services` 설정 파일에 API 자격 정보 항목을 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그다음, `Mail` 파사드의 `extend` 메서드로 Laravel에 전송 방식을 등록합니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 합니다:

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

등록을 마쳤다면, `config/mail.php`에서 새로운 전송 방식을 사용하는 메일러 정의를 추가할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
