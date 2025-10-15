# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
    - [장애 조치(Failover) 설정](#failover-configuration)
    - [라운드 로빈(Round Robin) 설정](#round-robin-configuration)
- [메일러블 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
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
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡하지 않아도 됩니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 깔끔하고 단순한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 메일 발송 드라이버를 기본적으로 지원하여, 로컬이나 클라우드 기반 서비스에서 빠르게 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일에 등록된 각 메일러는 고유한 설정과 "트랜스포트"를 가질 수 있으므로, 애플리케이션이 특정 이메일 메시지를 보낼 때 다양한 이메일 서비스별로 구분하여 사용할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark를, 대량 메일은 Amazon SES를 사용하는 형태로 설정할 수 있습니다.

`mail` 설정 파일 내에는 `mailers` 구성 배열이 있으며, 여기에 Laravel이 지원하는 주요 메일 드라이버/트랜스포트의 샘플 설정이 포함되어 있습니다. 그리고 `default` 설정 값은 애플리케이션에서 이메일 발송 시 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비

Mailgun, Postmark, Resend 등 API 기반 드라이버는 SMTP 서버보다 더 간단하고 빠를 수 있습니다. 가능하다면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer 트랜스포트를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그리고 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 다음 설정을 추가하세요:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정했다면, `config/services.php` 파일에 다음 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 [Mailgun 지역](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)이 아니라면, 해당 지역의 endpoint를 `services` 설정 파일에 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php` 설정 파일의 `default` 옵션을 `postmark`로 지정하세요. 이후 `config/services.php` 파일에 다음 옵션이 포함되어 있는지 확인합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

Postmark 메일러별로 사용할 메시지 스트림을 지정하려면, 메일러의 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 옵션은 `config/mail.php` 파일의 해당 메일러 설정에 추가하세요:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러를 구성할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

그리고 `config/mail.php` 설정 파일의 `default` 값을 `resend`로 지정하세요. 이후 `config/services.php` 파일에 다음 옵션이 포함되어야 합니다:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 PHP용 Amazon AWS SDK를 설치해야 합니다. Composer를 통해 이 라이브러리를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

다음으로, `config/mail.php` 설정 파일에서 `default` 옵션을 `ses`로 지정하고, `config/services.php` 파일에 다음 옵션들이 있는지 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면 SES 설정에 `token` 키를 추가하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 다루기 위해, [headers](#headers) 메서드에서 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 추가할 수 있습니다:

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

Laravel이 AWS SDK의 `SendEmail` 메서드로 전달해야 할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)이 있다면, SES 설정에 `options` 배열을 지정할 수 있습니다:

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
### 장애 조치(Failover) 설정

애플리케이션에서 사용하는 외부 메일 서비스가 일시적으로 다운되는 상황에 대비해, 주 메일 드라이버가 장애가 발생했을 때 사용할 백업 메일러 설정을 지정해 둘 수 있습니다.

이를 위해 애플리케이션의 `mail` 설정 파일에 `failover` 트랜스포트를 사용하는 메일러를 정의하세요. 이 메일러의 설정에는 메일 발송 시 사용할 메일러들의 순서를 명시하는 `mailers` 배열이 포함되어야 합니다:

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

`failover` 메일러를 정의했다면, 애플리케이션의 기본 메일러로 위 이름을 지정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(Round Robin) 설정

`roundrobin` 트랜스포트를 이용하면 여러 메일러에 메일 발송 작업을 분산시킬 수 있습니다. 우선, `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의하고, 발송에 사용할 메일러들을 `mailers` 배열에 명시하세요:

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

이제 기본 메일러로 `roundrobin`을 지정하여 메일 분산 처리를 활성화할 수 있습니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 설정된 메일러 중에서 무작위로 하나를 선택하고, 이후의 이메일마다 다음 메일러로 순차적으로 전환합니다. `failover` 트랜스포트가 *[고가용성(High Availability)](https://en.wikipedia.org/wiki/High_availability)* 확보에 중점을 두는 반면, `roundrobin` 트랜스포트는 *[로드 밸런싱(Load Balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 역할에 더 적합합니다.

<a name="generating-mailables"></a>
## 메일러블 생성 (Generating Mailables)

Laravel 애플리케이션에서 발송하는 각 유형의 이메일은 "메일러블(mailable)" 클래스 형태로 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 없다면, `make:mail` Artisan 명령어로 첫 메일러블을 생성하면 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 먼저 열어서 내부 구성을 살펴볼 수 있습니다. 메일러블 클래스의 주요 설정은 `envelope`, `content`, `attachments` 등의 메서드에서 이루어집니다.

`envelope` 메서드는 메시지의 제목과, 경우에 따라 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope로 발신자 지정

이메일의 발신자(즉, "From" 주소)를 설정하는 방법에는 두 가지가 있습니다. 첫 번째는 envelope에서 "from" 주소를 지정하는 것입니다:

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

또한, `replyTo` 주소도 지정할 수 있습니다:

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

애플리케이션 전체에서 동일한 "from" 주소를 사용하는 경우, 메일러블 클래스마다 해당 주소를 반복해서 지정하는 것은 번거롭기 마련입니다. 이럴 때는 `config/mail.php` 파일에서 글로벌 "from" 주소를 지정하세요. 메일러블 내에서 별도로 "from" 주소를 지정하지 않을 경우 이 값이 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한 전체 메일에 적용될 글로벌 "reply_to" 주소도 지정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서 이메일 내용을 랜더링할 템플릿, 즉 `view`를 지정합니다. 각 이메일은 보통 [Blade 템플릿](/docs/12.x/blade)을 이용하여 HTML로 작성하는 것이 일반적이며, Blade 템플릿 엔진의 모든 기능을 자유롭게 활용할 수 있습니다:

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
> 이메일 템플릿을 위한 `resources/views/mail` 디렉토리를 만드는 것이 좋으며, 그 위치는 `resources/views` 내부 어디든 자유롭게 설정할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 별도로 정의하고 싶다면, 메시지 `Content` 정의에서 plain-text 템플릿 이름을 `text` 파라미터에 전달합니다. `view` 파라미터와 마찬가지로, 이메일 본문을 랜더링할 템플릿명으로 지정하세요. HTML 및 plain-text 방식 모두의 메시지를 자유롭게 정의할 수 있습니다:

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

가독성을 위해, `html` 파라미터는 `view` 파라미터의 별칭으로 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 프로퍼티 사용

이메일 랜더링에 필요한 데이터를 뷰에 전달하는 방법에는 두 가지가 있습니다. 첫 번째는 메일러블 클래스에 정의된 public 프로퍼티를 활용하는 것입니다. 메일러블 클래스의 생성자(constructor)에서 데이터를 받아 public 프로퍼티에 할당하면, 해당 프로퍼티는 Blade 템플릿에서 바로 사용할 수 있습니다:

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

public 프로퍼티에 데이터를 할당하면, 해당 값은 Blade 뷰에서 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 사용

이메일 뷰에 데이터를 전달하기 전에 포맷을 조정하거나, 뷰에 노출할 데이터를 직접 컨트롤하고 싶다면, `Content` 정의의 `with` 파라미터를 사용해 데이터를 직접 넘길 수 있습니다. 이 경우, 생성자에서는 데이터를 받아서 protected 또는 private 프로퍼티에 할당하고, public으로 노출하지 않아야 합니다:

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

`with` 파라미터로 전달된 데이터 역시 Blade 템플릿 내에서 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

이메일에 첨부 파일을 추가하려면, 메일러블의 `attachments` 메서드에서 파일 정보를 반환하는 배열에 첨부 파일을 추가합니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달하는 방법입니다:

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

첨부 파일의 표시 이름 또는 MIME 타입 등도 `as`, `withMime` 메서드를 이용해 지정할 수 있습니다:

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

첨부 파일명과 MIME 타입도 추가 지정 가능합니다:

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

기본 외의 다른 스토리지 디스크를 사용하려면 `fromStorageDisk`를 사용할 수 있습니다:

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
#### RAW 데이터 첨부

메모리 상의 바이너리 데이터(예: 메모리에서 바로 생성한 PDF 등)를 첨부하려면, `fromData` 메서드를 사용합니다. 이 메서드는 클로저(실제 바이트 데이터를 반환하는 함수)와 첨부 파일명을 인자로 받습니다:

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
### 인라인 첨부 파일 (Inline Attachments)

이메일 본문에 이미지를 직접 삽입(임베드)하려면 자신의 템플릿에서 `$message` 변수의 `embed` 메서드를 활용하세요. Laravel은 `$message` 변수를 모든 이메일 템플릿에 자동으로 전달하므로 별도 조치가 필요하지 않습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에서는 사용할 수 없습니다(plain-text 메시지는 인라인 첨부를 지원하지 않음).

<a name="embedding-raw-data-attachments"></a>
#### RAW 데이터 인라인 첨부

이미지 데이터를 메모리에 보관 중인 경우, `$message->embedData` 메서드로 이미지 파일 이름과 함께 삽입할 수 있습니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

문자열 경로가 아닌, 모델 등 애플리케이션 내에서 attachable로 표현되는 객체를 메일의 첨부로 사용하고 싶을 때는 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 해당 객체(예: 모델)에 구현하면 됩니다. `toMailAttachment` 메서드를 정의하여 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

이제 메시지 빌더의 `attachments` 메서드에서 모델 인스턴스를 배열로 반환하면 첨부 파일로 자동 처리됩니다:

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

첨부파일 데이터가 원격 저장소(예: Amazon S3 등)에 있다면, [파일시스템 디스크](/docs/12.x/filesystem)의 메서드로 Attachment 인스턴스를 만들 수 있습니다:

```php
// 기본 디스크에서 파일 첨부
return Attachment::fromStorage($this->path);

// 지정한 디스크에서 파일 첨부
return Attachment::fromStorageDisk('backblaze', $this->path);
```

메모리 쿠션 데이터를 첨부파일로 만들려면, `fromData` 메서드에 클로저를 넘깁니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

또한 파일명 지정 및 MIME 타입 커스터마이징도 `as`, `withMime` 메서드로 가능합니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

특정 상황에서는 `Message-Id`나 기타 커스텀 헤더 값을 이메일에 추가해야 할 수 있습니다.

이를 위해, 메일러블 내에 `headers` 메서드를 정의하고, `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하세요. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받으며, 필요한 값만 넘겨주면 됩니다:

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

Mailgun, Postmark와 같은 일부 외부 이메일 서비스는 이메일 메시지를 분류/추적하는데 쓸 수 있는 "태그"와 "메타데이터" 기능을 지원합니다. `Envelope` 정의에서 태그 및 메타데이터를 쉽게 추가할 수 있습니다:

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

Mailgun 드라이버를 사용할 경우, [Mailgun의 태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags), [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) 문서를 참고하세요. Postmark 역시 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 문서를 참조하실 수 있습니다.

Amazon SES 사용 시, `metadata` 메서드를 이용하여 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 붙일 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer에 의해 구동됩니다. 메시지 발송 직전, Symfony Message 인스턴스를 후킹할 커스텀 콜백을 등록해, 메시지 내용을 세밀하게 제어할 수도 있습니다. 이를 위해 `Envelope` 정의의 `using` 파라미터에 콜백 함수를 추가하세요:

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

마크다운 메일러블 메시지를 이용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)의 기본 템플릿 및 컴포넌트를 메일러블에서 그대로 활용할 수 있습니다. 메시지는 마크다운(Markdown)으로 작성하므로, Laravel은 아름답고 반응형인 HTML 템플릿과 plain-text 버전을 자동으로 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿과 함께 메일러블을 생성하려면, `make:mail` Artisan 명령어의 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그리고 `content` 메서드의 `Content` 정의에서 `view` 대신 `markdown` 파라미터를 사용합니다:

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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 혼합하여 활용함으로써, 미려한 UI 구성요소와 함께 쉽게 이메일을 만들 수 있습니다:

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
> 마크다운 이메일 작성 시 과도한 들여쓰기를 사용하지 마세요. 마크다운 표준에 따라 들여쓰기된 내용은 코드 블록으로 처리됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 랜더링합니다. 이 컴포넌트는 `url`과 선택적인 `color` 인자를 받으며, `primary`, `success`, `error` 색상을 지원합니다. 버튼은 메시지 내에 여러 개 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 배경색이 살짝 다른 패널로 랜더링해, 메시지의 특정 부분에 강조를 줄 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면, 마크다운 테이블을 HTML 테이블로 변환할 수 있습니다. 테이블의 컬럼 정렬은 마크다운의 기본 Table Alignment 문법을 따릅니다:

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

마크다운 메일 컴포넌트를 직접 애플리케이션 내에서 수정하려면, `vendor:publish` Artisan 명령어로 `laravel-mail` 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령을 실행하면 `resources/views/vendor/mail` 디렉토리에 마크다운 메일 컴포넌트들이 복사됩니다. `mail` 디렉토리 내부에는 각 컴포넌트의 `html`/`text` 버전이 별도로 존재하므로 마음껏 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 퍼블리시한 후 `resources/views/vendor/mail/html/themes` 디렉토리의 `default.css` 파일을 수정하면, 해당 CSS 스타일이 HTML 메일 메시지에 인라인 스타일로 자동 적용됩니다.

만약 새로운 테마를 만들고 싶다면 `html/themes` 디렉토리에 CSS 파일을 추가하고, `config/mail.php` 파일의 `theme` 옵션을 새 테마의 이름으로 수정하세요.

개별 메일러블에 대해 테마를 바꾸고 싶다면, 해당 클래스의 `$theme` 프로퍼티에 사용할 테마명을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송 (Sending Mail)

메일 발송은 [Mail 파사드](/docs/12.x/facades)의 `to` 메서드를 이용합니다. 이 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자들로 구성된 컬렉션을 인수로 받습니다. 컬렉션이나 객체를 넘기면 각 객체의 `email`과 `name` 프로퍼티가 자동으로 수신자 정보로 추출되니, 객체에 해당 프로퍼티가 있는지 확인해야 합니다. 수신자를 지정했으면, `send` 메서드에 메일러블 인스턴스를 전달하면 됩니다:

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

메일 발송 시 "to"뿐만 아니라 `cc`, `bcc` 수신자도 메서드 체이닝으로 자유롭게 지정할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 반복문으로 다수의 수신자에 발송

여러 수신자에게 각각 별도의 메일을 보내야 할 때, `to` 메서드는 해당 메일러블의 수신자 목록에 추가하는 방식이기 때문에, 반복문에서 같은 인스턴스를 사용하면 이전 수신자까지 계속 포함해서 발송됩니다. 따라서 반드시 매번 새 메일러블 인스턴스를 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 발송

기본적으로 Laravel은 `mail` 설정 파일의 `default` 메일러를 통해 메일을 보냅니다. 그러나, `mailer` 메서드로 원하는 메일러를 선택해 보낼 수도 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지를 큐에 넣기

이메일 발송은 애플리케이션의 응답 속도에 영향을 줄 수 있으므로, 많은 개발자들은 메일 발송 작업을 별도의 큐에 넣어 백그라운드에서 처리하게 합니다. Laravel은 [통합 큐 API](/docs/12.x/queues)로 이를 매우 쉽게 처리할 수 있습니다. `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이때 큐 작업 등록 과정은 Laravel이 자동으로 처리합니다. 사용하기 전 [큐 설정](/docs/12.x/queues)을 마쳐야 합니다.

<a name="delayed-message-queueing"></a>
#### 메일 발송 지연하기

큐잉된 이메일 발송을 일정 시간 뒤로 미루고 싶다면, `later` 메서드를 이용할 수 있습니다. 첫 번째 인수로는 어떤 시점에 보낼지 지정하는 `DateTime` 인스턴스를 전달합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐 지정

`make:mail`로 생성한 모든 메일러블은 `Illuminate\Bus\Queueable` 트레잇을 사용하므로, 특정 큐 이름이나 연결을 지정하고 싶다면 메일러블 인스턴스에서 `onQueue`, `onConnection` 메서드를 사용할 수 있습니다:

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
#### 항상 큐로 발송하기

특정 메일러블 클래스를 항상 큐잉하고 싶다면 `ShouldQueue` 계약을 구현하세요. 이후 `send`로 보낸 경우에도 자동으로 큐잉됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치되는 경우, 큐 작업이 트랜잭션 커밋 전에 처리될 수 있습니다. 이 경우 트랜잭션 중 변경한 모델이나 레코드가 DB에 반영되지 않아 문제가 발생할 수 있습니다. 모델 생성 또한 트랜잭션 완료 전이라면 DB에 존재하지 않을 수 있습니다. 메일러블이 해당 모델을 참조할 경우 예상치 못한 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 옵션이 `false`일 경우, 메일 발송 시 `afterCommit` 메서드를 호출해 모든 열린 트랜잭션이 커밋된 후 메일러블이 디스패치 되도록 지정할 수 있습니다:

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
> 관련 주제에 대한 더 자세한 안내는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 실패 처리

이메일 발송 큐 작업이 실패할 경우, 메일러블 클래스에 `failed` 메서드를 정의해 두었다면 해당 메서드가 호출되며, 실패를 발생시킨 `Throwable` 인스턴스가 전달됩니다:

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

메일러블의 HTML 컨텐츠를 실제로 메일 발송 없이, 문자열로 추출해야 할 때는 `render` 메서드를 호출하세요. 이 메서드는 메일러블의 랜더링된 HTML을 문자열로 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인할 때, 실제 메일 발송 없이 바로 브라우저에서 랜더링 결과를 확인할 수 있습니다. 라우트 클로저 또는 컨트롤러에서 메일러블을 직접 반환하면, 해당 메일러블이 브라우저에서 랜더링되어 실시간 미리보기가 가능합니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 로컬라이징 (Localizing Mailables)

Laravel은 현재 요청 로케일과는 다른 로케일로 메일러블을 발송할 수 있도록 지원하며, 해당 로케일 정보는 메일이 큐잉될 경우에도 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 미리 지정하세요. 메일러블 템플릿을 평가할 때 지정한 로케일이 적용되고, 작업 완료 후 원래 로케일로 복원됩니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자별 선호 로케일

애플리케이션에서 사용자별 선호 로케일을 저장하고 있다면, 모델에 `HasLocalePreference` 계약을 구현하여 해당 로케일로 메일을 발송할 수 있습니다:

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

인터페이스를 구현하면, 메일러블 또는 알림 발송 시 자동으로 사용자의 선호 로케일이 적용되므로 `locale` 메서드를 별도로 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

Laravel은 메일러블 구조 및 내용을 검사하기 위한 다양한 메서드를 제공합니다. 또한, 원하는 내용이 메일러블에 정확히 포함되는지 쉽게 테스트할 수 있습니다:

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

위 예시에서 "HTML" 관련 메서드는 HTML 버전의 메일에 특정 문자열이 포함(혹은 미포함)되는지, "text" 관련 메서드는 plain-text 버전에서 해당 내용을 확인합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 발송 테스트

메일러블의 내용 테스트와 "특정 사용자에게 메일러블이 발송됨" 사실을 확인하는 테스트는 분리할 것을 권장합니다. 실제 내용이 중요한 경우가 아니라면, 해당 메일러블이 정말로 "발송" 지시를 받았는지만으로 충분한 경우가 많습니다.

`Mail` 파사드의 `fake` 메서드를 호출해 실제 메일 발송을 차단할 수 있습니다. 그 이후 메일러블이 올바른 수신자에게 전달되었는지, 어떤 데이터가 전달되었는지 등을 손쉽게 검증할 수 있습니다:

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

백그라운드 큐로 메일러블을 발송하는 경우에는 `assertSent` 대신 `assertQueued`를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 콜백을 전달해, 조건에 맞는 메일러블이 실제로 발송/대기 상태인지 정교하게 테스트할 수도 있습니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

콜백에서는 메일러블 인스턴스를 통해 다양한 검사 메서드도 활용할 수 있습니다:

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

첨부 파일 관련 검증 메서드도 메일러블 인스턴스에서 제공합니다:

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

메일이 발송도, 큐잉도 되지 않았음을 검증하려면 `assertNothingOutgoing`, 조건부로는 `assertNotOutgoing`을 이용합니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

개발 환경에서 실제 이메일을 외부에 발송하는 것은 권장되지 않습니다. Laravel은 로컬 개발 중 실제 메일 발송을 "우회"할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버를 사용하면 이메일이 실제로 발송되지 않고, 모든 이메일 메시지가 로그 파일에 기록됩니다. 이 드라이버는 일반적으로 로컬 개발 환경에서만 사용됩니다. 환경별 설정 방법은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

[HELO](https://usehelo.com) 또는 [Mailtrap](https://mailtrap.io) 같은 서비스를 이용해, `smtp` 드라이버로 실제 이메일 주소가 아닌 "가상" 메일함에 메일을 전송할 수 있습니다. 이 방식은 진짜 이메일 클라이언트와 동일한 형식으로 결과를 확인할 수 있는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용할 경우, [Mailpit](https://github.com/axllent/mailpit)으로도 메시지를 미리 볼 수 있습니다. Sail 실행 중 `http://localhost:8025` 접속 시 Mailpit UI를 볼 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

글로벌 "to" 주소를 지정하려면, `Mail` 파사드의 `alwaysTo` 메서드를 사용하세요. 일반적으로 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

이 메서드를 사용하는 경우, 메일에 지정된 추가 "cc"나 "bcc" 주소는 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 발송 시점에 두 가지 이벤트를 발생시킵니다. `MessageSending` 이벤트는 실제 발송 전, `MessageSent` 이벤트는 발송 후에 발생합니다. 이 이벤트들은 메일이 **실제로 발송**될 때 발생하며, 큐잉 시에는 발생하지 않습니다. 애플리케이션 내에서 [이벤트 리스너](/docs/12.x/events)를 만들어 처리할 수 있습니다:

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
## 커스텀 트랜스포트 (Custom Transports)

기본 내장 메일 트랜스포트 외에, Laravel이 미지원하는 외부 서비스로 이메일을 발송하기 위해 직접 트랜스포트를 작성할 수 있습니다. 우선 `Symfony\Component\Mailer\Transport\AbstractTransport`를 상속하는 클래스를 만들고, `doSend`, `__toString` 메서드를 구현해야 합니다:

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

커스텀 트랜스포트를 정의했다면, `Mail` 파사드의 `extend` 메서드로 등록합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 진행합니다. `$config` 인자에는 `config/mail.php`의 해당 메일러 설정 배열이 전달됩니다:

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

이제 `config/mail.php`에 커스텀 트랜스포트를 사용하는 메일러를 정의할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

Laravel은 Mailgun, Postmark 등 Symfony 공식 트랜스포트를 내장 지원합니다. 이 외에 추가로 Symfony 공식 트랜스포트 패키지를 설치해 Laravel에서 사용할 수 있습니다. 예를 들어 "Brevo"(구 Sendinblue) 트랜스포트를 설치 및 등록하려면:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, API 자격 증명을 `services` 설정 파일에 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그 다음, 서비스 프로바이더의 `boot` 메서드에서 트랜스포트를 등록합니다:

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

트랜스포트 등록이 끝나면, `config/mail.php`에 새로운 메일러를 추가해 사용할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
