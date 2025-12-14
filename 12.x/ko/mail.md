# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 / 전송 방식 사전 준비](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드로빈(Round Robin) 설정](#round-robin-configuration)
- [메일러블 클래스 생성](#generating-mailables)
- [메일러블 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(view) 설정](#configuring-the-view)
    - [뷰 데이터 전달](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더(Headers)](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 현지화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 콘텐츠 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식(Transport)](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡하지 않아도 됩니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 통한 이메일 발송을 지원하는 다양한 드라이버를 제공하므로, 원하는 로컬 또는 클라우드 기반 서비스로 손쉽게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일로 구성할 수 있습니다. 이 파일에 정의된 각 메일러는 고유한 설정과 "전송 방식(transport)"을 가질 수 있어, 애플리케이션에서 서로 다른 이메일 서비스를 사용해 개별 메일을 발송할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일에는 `mailers` 설정 배열이 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송 방식에 대한 샘플 설정이 포함되어 있습니다. 전체 설정에서 `default` 값은 애플리케이션이 이메일을 보낼 때 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 사전 준비

Mailgun, Postmark, Resend와 같은 API 기반 드라이버는 SMTP 서버를 통한 메일 발송보다 일반적으로 더 간단하고 빠릅니다. 가능하다면 이러한 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer 전송 패키지를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 아래 설정을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

설정을 마친 후 `config/services.php` 파일에 다음 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국이 아닌 다른 [Mailgun 리전](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하는 경우, 해당 리전의 엔드포인트를 `services` 설정 파일에 정의할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 전송 패키지를 설치합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그런 다음, 애플리케이션의 `config/mail.php`에서 `default` 옵션을 `postmark`로 설정하세요. 마지막으로 `config/services.php` 파일에 아래 옵션이 포함되어 있는지 확인하세요:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하려면, 해당 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 설정 배열은 `config/mail.php` 파일에 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림으로 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

애플리케이션의 `config/mail.php`에서 기본 메일러를 `resend`로 설정한 뒤, `config/services.php` 파일에도 아래 옵션이 포함되어야 합니다:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 먼저 Amazon AWS SDK for PHP를 Composer로 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php`에서 기본 메일러를 `ses`로 설정하고, `config/services.php`에 아래와 같은 SES 옵션이 있는지 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메일 메시지의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 배열로 반환하세요:

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

이메일 전송 시 AWS SDK의 `SendEmail` 메서드에 Laravel에서 추가로 넘겨야 하는 [옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)이 있다면, SES 설정의 `options` 배열에 정의할 수 있습니다:

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
### 장애 조치(failover) 설정

외부 메일 서비스를 사용하다가 서비스가 다운되는 상황이 생길 수 있습니다. 이럴 때를 대비해, 기본 메일 전송 드라이버가 다운된 경우 사용할 보조(백업) 메일 전송 설정을 지정할 수 있습니다.

이를 위해, `mail` 설정 파일에 `failover` 전송 방식을 사용하는 메일러를 정의하세요. `failover` 메일러의 설정 배열에는 사용할 메일러들의 우선순위가 담긴 `mailers` 배열이 필요합니다:

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

장애 조치 기능을 사용하려면, `.env` 파일에서 `MAIL_MAILER` 값을 `failover`로 설정하세요:

```ini
MAIL_MAILER=failover
```

<a name="round-robin-configuration"></a>
### 라운드로빈(Round Robin) 설정

`roundrobin` 전송 방식은 여러 메일러에 메일 발송 작업을 분산시켜 처리할 수 있게 해줍니다. 우선, `mail` 설정 파일에 `roundrobin` 전송 방식을 사용하는 메일러를 아래와 같이 정의합니다:

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

`roundrobin` 메일러를 정의했다면, 설정 파일의 `default`에 해당 메일러 이름을 지정해 기본 메일러로 사용하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 전송 방식은 구성된 메일러 목록에서 무작위로 하나를 선택해 처음 메일을 보내고, 이후에는 순차적으로 다음 메일러를 선택하는 방식입니다. 이는 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*을 제공하는 `failover` 방식과 달리, *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 클래스 생성 (Generating Mailables)

Laravel 애플리케이션을 설계할 때, 애플리케이션이 보내는 각 유형의 이메일은 "메일러블(mailable)" 클래스로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없다면, 처음 메일러블 클래스를 `make:mail` Artisan 명령어로 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 클래스 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 그 내부를 살펴볼 차례입니다. 메일러블 클래스의 설정은 주로 `envelope`, `content`, `attachments` 등의 메서드에서 이루어집니다.

`envelope` 메서드는 메시지의 제목(subject) 및 필요에 따라 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope를 사용한 설정

이메일의 발신자, 즉 "from" 주소를 설정하는 방법은 두 가지가 있습니다. 첫째로, 메일 메시지의 envelope에서 "from" 주소를 지정할 수 있습니다:

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

또한, `replyTo` 주소를 지정할 수도 있습니다:

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

애플리케이션의 모든 이메일이 동일한 "from" 주소를 사용한다면, 매번 메일러블 클래스마다 지정하는 것은 번거로울 수 있습니다. 이럴 땐, `config/mail.php`의 설정 파일에서 글로벌 "from" 주소를 지정하세요. 메일러블 클래스에서 "from" 주소를 별도로 지정하지 않은 경우 이 주소가 사용됩니다:

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
### 뷰(view) 설정

메일러블 클래스의 `content` 메서드 내에서 메일 콘텐츠를 렌더링할 때 사용할 `view`(템플릿)를 지정할 수 있습니다. 보통 각 이메일은 [Blade 템플릿](/docs/12.x/blade)을 사용하기 때문에, 템플릿 시스템의 다양한 기능과 편리함을 메일에서 그대로 활용할 수 있습니다:

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
> 이메일 템플릿 파일을 `resources/views/mail` 디렉터리에 생성하면 관리가 쉽지만, `resources/views` 하위의 원하는 위치에 저장해도 무방합니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트(plain-text) 이메일

이메일의 일반 텍스트 버전을 별도 정의하고 싶다면 평문 템플릿의 이름을 `Content` 정의의 `text` 파라미터로 지정할 수 있습니다. `view` 파라미터와 마찬가지로, 템플릿 이름을 지정합니다. HTML 버전과 plain-text 버전을 모두 정의할 수도 있습니다:

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

명확하게 하기 위해, `html` 파라미터 역시 `view`의 별칭으로 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 전달

<a name="via-public-properties"></a>
#### 퍼블릭 속성(public property) 이용

이메일 렌더링 시, Blade 템플릿에서 활용할 데이터를 뷰로 전달하는 방법은 크게 두 가지입니다. 첫 번째로, 메일러블 클래스에서 정의한 모든 퍼블릭 속성은 자동으로 뷰에 전달됩니다. 예를 들어, 생성자를 통해 데이터를 받아 퍼블릭 속성에 할당하면 됩니다:

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

프로퍼티에 할당된 데이터는 템플릿에서 직접 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 이용

템플릿으로 전달되는 데이터 포맷이나 값 자체를 커스터마이즈하고 싶다면, `Content` 정의에서 `with` 파라미터로 배열을 직접 전달할 수 있습니다. 이 경우에도 생성자에서는 데이터 할당을 하고, 해당 속성은 `protected` 또는 `private`으로 선언하세요. 이렇게 하면 해당 데이터는 자동으로 템플릿에 전달되지 않습니다:

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

이렇게 하면 `with`에 전달한 각각의 데이터가 템플릿에서 바로 사용 가능합니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메일러블 클래스의 `attachments` 메서드에서 반환하는 배열에 첨부 파일을 추가하면 됩니다. `Attachment` 클래스의 `fromPath` 메서드를 이용해 파일 경로를 전달할 수 있습니다:

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

파일 첨부 시, 표시 이름(display name)과 MIME 타입을 각각 `as`, `withMime` 메서드로 지정할 수 있습니다:

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

애플리케이션의 [파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 첨부하려면, `fromStorage` 메서드를 사용할 수 있습니다:

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

파일 이름과 MIME 타입 역시 지정 가능합니다:

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

기본 디스크가 아닌 다른 스토리지 디스크를 사용하려면 `fromStorageDisk` 메서드를 사용하면 됩니다:

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

메모리 상에 존재하는 데이터(예: 생성한 PDF 바이트열 등)를 파일로 저장하지 않고 바로 첨부할 때는 `fromData` 메서드를 사용할 수 있습니다. 이때는 raw 데이터를 반환하는 클로저와 파일 이름을 전달합니다:

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
### 인라인 첨부 파일

이메일 본문에 이미지를 인라인으로 삽입하는 일은 다소 번거롭지만, Laravel은 이를 간편하게 지원합니다. 이메일 템플릿에서 `$message` 변수의 `embed` 메서드를 활용해 이미지를 인라인 첨부할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에서 자동으로 사용할 수 있습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> plain-text 메시지 템플릿에서는 `$message` 변수를 사용할 수 없습니다. plain-text는 인라인 첨부를 지원하지 않습니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

이미 메모리상에 raw 이미지 데이터가 있다면, `$message->embedData` 메서드로 인라인 이미지를 삽입할 수 있습니다. 이때 파일명을 함께 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

문자열 경로로 파일을 첨부하는 것이 충분한 경우가 많지만, 실제로 메일에 첨부하는 엔티티가 클래스(예: `Photo` 모델)로 표현되는 경우도 있습니다. `Attachable` 객체를 활용하면, 해당 클래스를 직접 첨부할 수 있습니다.

우선, 첨부 가능한 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하고, `toMailAttachment` 메서드에서 `Illuminate\Mail\Attachment` 인스턴스를 반환하세요:

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

이제 `attachments` 메서드에서 해당 객체를 배열로 반환하면 자동으로 첨부처리됩니다:

```php
public function attachments(): array
{
    return [$this->photo];
}
```

첨부 데이터가 S3와 같은 원격 저장소에 있을 경우, [파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 첨부로 변환할 수 있습니다:

```php
// 기본 디스크의 파일 첨부
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일 첨부
return Attachment::fromStorageDisk('backblaze', $this->path);
```

메모리상 데이터로도 첨부 인스턴스를 생성할 수 있습니다. 이 경우 `fromData` 메서드에 클로저를 전달하세요:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

`as`, `withMime` 등의 메서드로 파일명과 MIME 타입을 커스터마이즈할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더(Headers)

간혹, 메일에 커스텀 헤더(예: 직접 지정한 `Message-Id`, 임의의 텍스트 헤더 등)를 추가해야 할 때가 있습니다.

이럴 때는 메일러블 클래스에 `headers` 메서드를 정의하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 매개변수를 지원합니다. 필요에 따라 원하는 것만 지정하면 됩니다:

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

Mailgun, Postmark와 같은 일부 외부 이메일 서비스는 메시지 "태그"와 "메타데이터"를 지원하며, 이를 이용해 이메일을 그룹별로 추적할 수 있습니다. `Envelope` 정의를 통해 태그와 메타데이터를 이메일에 추가할 수 있습니다:

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

Mailgun 드라이버를 쓴다면 [Mailgun 태그 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)를 참고하세요. Postmark 역시 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서를 참고하세요.

Amazon SES를 사용할 경우, `metadata` 메서드로 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이즈

Laravel의 메일 기능은 Symfony Mailer를 기반으로 합니다. 메일 발송 전, Symfony 메시지 인스턴스에 커스텀 콜백을 등록할 수 있어, 메시지를 심도 있게 커스터마이징할 수 있습니다. 이를 위해 `Envelope` 정의에서 `using` 파라미터를 활용하세요:

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

마크다운 메일러블 메시지는 [메일 알림](/docs/12.x/notifications#mail-notifications)의 여러 템플릿과 컴포넌트를 활용할 수 있도록 해줍니다. 메시지를 Markdown으로 작성하면, Laravel은 아름답고 반응형의 HTML 템플릿을 자동으로 렌더링하고 plain-text 버전도 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 포함된 메일러블을 만들려면, `make:mail` Artisan 명령어에 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그리고 해당 마크다운 템플릿을 사용하려면, `content` 메서드의 `Content` 정의에서 `view` 대신 `markdown` 파라미터를 사용합니다:

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

마크다운 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합해서 이메일을 쉽게 구성할 수 있게 해줍니다. Laravel에서 제공하는 여러 UI 컴포넌트도 활용 가능합니다:

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
> 마크다운 이메일을 작성할 때 과도한 들여쓰기를 사용하지 마세요. Markdown 공식 문서에 따르면, 들여쓴 내용은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. 인자값으로 `url`과 선택적으로 `color`를 받으며, `primary`, `success`, `error` 색상을 지원합니다. 원하는 만큼 버튼을 넣을 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 텍스트 블록에 약간 다른 배경색을 적용해 강조할 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 HTML로 변환합니다. 열 정렬도 마크다운 문법으로 지원합니다:

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

마크다운 메일 컴포넌트를 내 애플리케이션에서 직접 커스터마이즈할 수 있습니다. Artisan의 `vendor:publish` 명령어로 `laravel-mail` asset 태그를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

위 명령으로 `resources/views/vendor/mail` 디렉터리에 마크다운 메일 컴포넌트가 복사됩니다. 이 디렉터리의 `html`과 `text` 폴더에서 모든 컴포넌트를 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보내면, `resources/views/vendor/mail/html/themes` 폴더에 `default.css`가 생성됩니다. 이 파일을 수정하면, HTML 메일에서 자동으로 인라인 스타일로 적용됩니다.

새로운 마크다운 테마를 만들려면, `html/themes` 디렉터리에 별도의 CSS 파일을 만들고 `config/mail.php` 설정 파일의 `theme` 옵션 값을 새 테마 이름으로 지정합니다.

개별 메일러블에서만 테마를 변경하려면, 메일러블 클래스의 `$theme` 속성을 설정하면 됩니다.

<a name="sending-mail"></a>
## 메일 전송 (Sending Mail)

메일을 보내려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to`에는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션 등을 전달할 수 있습니다. 객체나 컬렉션을 전달하면, 자동으로 객체의 `email`, `name` 속성이 수신자로 사용됩니다(이 속성이 객체에 있다면). 수신자를 지정한 후, 메일러블 클래스 인스턴스를 `send` 메서드로 전달하세요:

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

"To" 이외에도 "cc", "bcc" 수신자를 메서드 체이닝으로 추가할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 루프 처리

여러 수신자에게 메일을 반복 전송해야 할 경우, 메일러블 인스턴스를 매번 새로 생성해야 합니다. 그렇지 않으면, `to`가 수신자 목록에 이전 수신자를 계속 추가하기 때문입니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 전송

기본적으로 Laravel은 `mail` 설정의 `default` 메일러를 사용해 메일을 전송합니다. 하지만 `mailer` 메서드로 특정 메일러를 지정할 수 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송은 애플리케이션 응답 속도에 영향을 줄 수 있으므로, 많은 개발자들이 메일 전송을 비동기로 백그라운드에서 처리하길 원합니다. Laravel은 내장된 [통합 큐 API](/docs/12.x/queues)로 이 작업을 쉽게 할 수 있도록 도와줍니다. 메일 메시지를 큐에 올리려면, 수신자를 지정한 후 `queue` 메서드를 사용하면 됩니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이렇게 하면, 메시지가 자동으로 큐에 job으로 올라가 백그라운드에서 발송됩니다. 이 기능을 사용하려면 [큐 설정](/docs/12.x/queues)이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 메일 전송 지연 큐잉

큐에 등록된 메일의 전송을 일정 시간 지연하고 싶다면, `later` 메서드를 사용하세요. 첫 번째 인자로는 언제 전송할지 나타내는 `DateTime` 객체를 전달합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐로 전송하기

`make:mail`로 생성된 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용합니다. 이로 인해, 모든 메일러블 인스턴스에서 `onQueue` 및 `onConnection` 메서드를 써서 큐와 연결명을 지정할 수 있습니다:

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
#### 기본적으로 메일 큐잉

모든 상황에서 항상 큐잉되는 메일러블을 원한다면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이제 `send` 메서드를 사용해도 메일러블은 큐에 등록됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐가 트랜잭션 커밋 전에 메일러블을 처리할 수 있습니다. 이 경우, 트랜잭션 내에서 모델이나 DB 레코드를 갱신했더라도 아직 DB에 반영되지 않아, 메일러블이 이를 참조하면 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`로 설정된 경우, 해당 메일러 메시지를 모든 오픈된 트랜잭션 커밋 후에 디스패치하려면 `afterCommit` 메서드를 사용하세요:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 클래스의 생성자에서 직접 호출할 수도 있습니다:

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
> 이러한 이슈를 회피하는 자세한 방법은 [큐 job과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 실패 처리

큐잉된 이메일 전송에 실패하면, 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 오류에 대한 `Throwable` 인스턴스가 파라미터로 전달됩니다:

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

가끔 메일을 실제로 보내지 않고도, 메일러블의 HTML 콘텐츠를 추출하고 싶을 때가 있습니다. 이럴 때 `render` 메서드를 사용할 수 있으며, 이 메서드는 평가된 HTML 문자열을 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인할 때, 마치 일반 Blade 템플릿처럼 브라우저에서 바로 보기 편리합니다. 이를 위해, Laravel은 라우트 클로저나 컨트롤러에서 메일러블 객체를 직접 반환하면 HTML로 랜더링하여 브라우저에 표시해줍니다. 실제 이메일 주소로 보내지 않아도 디자인을 쉽게 확인할 수 있습니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 현지화 (Localizing Mailables)

Laravel은 현재 요청의 로케일과 다른 로케일로 메일러블을 전송하는 기능을 지원하며, 메일이 큐에 올라가 있더라도 해당 로케일을 기억해 전송할 수 있습니다.

이를 위해, `Mail` 파사드의 `locale` 메서드를 사용해 원하는 언어를 지정하면 됩니다. 렌더링 시 해당 언어가 적용되고, 렌더링 이후에는 기존 로케일로 복귀합니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

애플리케이션에 사용자의 선호 로케일이 저장되어 있다면, 모델에 `HasLocalePreference` 인터페이스를 구현하세요. 그러면 메일 발송 시 자동으로 사용자의 선호 로케일이 적용됩니다:

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

이 인터페이스를 구현하면, `locale` 메서드를 별도 호출하지 않아도 자동으로 적용됩니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 콘텐츠 테스트

Laravel은 메일러블 구조를 검사할 수 있는 다양한 메서드를 제공합니다. 또한, 기대하는 콘텐츠가 실제로 메일러블에 포함되어 있는지 테스트할 여러 메서드도 제공합니다:

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

"HTML" 어서션은 메일러블의 HTML 버전에 문자열이 포함됐는지, "text" 어서션은 plain-text 버전에 포함됐는지 각각 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 발송 테스트

테스트에서는 메일러블 콘텐츠 검증과, 실제로 특정 사용자에게 메일이 "발송되었는가"를 구분해서 수행하는 것이 좋습니다. 대부분의 경우, 콘텐츠 검증은 별도의 테스트로 분리하고, 발송 자체를 어서션만 해도 충분합니다.

`Mail` 파사드의 `fake` 메서드로 실제 메일 발송을 방지할 수 있습니다. `fake` 이후에는 메일러블이 특정 사용자에게 전송됐는지, 전달 받은 데이터가 무엇인지 등도 검사할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // Perform order shipping...

    // 실제로 전송된 메일러블 없음 검사
    Mail::assertNothingSent();

    // 메일러블 전송됨 검사
    Mail::assertSent(OrderShipped::class);

    // 두 번 전송 검사
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 주소로 전송 검증
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 복수 주소 검증
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 보내지 않음 검증
    Mail::assertNotSent(AnotherMailable::class);

    // 두 번 전송 검증
    Mail::assertSentTimes(OrderShipped::class, 2);

    // 전체 3개 전송 검증
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

        // 실제로 전송된 메일러블 없음 검사
        Mail::assertNothingSent();

        // 메일러블 전송됨 검사
        Mail::assertSent(OrderShipped::class);

        // 두 번 전송 검사
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 주소로 전송 검증
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // 복수 주소 검증
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // 보내지 않음 검증
        Mail::assertNotSent(AnotherMailable::class);

        // 두 번 전송 검증
        Mail::assertSentTimes(OrderShipped::class, 2);

        // 전체 3개 전송 검증
        Mail::assertSentCount(3);
    }
}
```

메일러블을 백그라운드에서 큐잉 전송할 경우, `assertSent` 대신 `assertQueued`를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등의 메서드에는 클로저를 전달해, 특정 조건을 만족하는 메일러블이 전송됐는지 테스트할 수 있습니다. 하나라도 조건을 만족하는 메일러블이 있으면 true로 처리됩니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

클로저로 전달되는 메일러블 인스턴스에는 여러가지 검사를 위한 유틸리티 메서드도 있습니다:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...') &&
           $mail->hasMetadata('order_id', $mail->order->id);
           $mail->usesMailer('ses');
});
```

첨부 파일이 있는지 등도 구체적으로 검사할 수 있습니다:

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

`assertNotSent`, `assertNotQueued`처럼 메일이 절대 전송되지 않았는지, 또는 아무것도 나가지 않았는지 검사하려면 `assertNothingOutgoing`, `assertNotOutgoing`를 사용합니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

개발 환경에서 실제 이메일 계정으로 진짜 메일이 나가지 않도록 하고 싶을 때가 많습니다. Laravel은 여러가지 방법으로 실제 메일 전송을 "비활성화" 할 수 있도록 지원합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버를 사용하면, 메일을 실제로 보내지 않고 로그 파일에 기록만 할 수 있습니다. 주로 로컬 개발 환경에서 사용됩니다. 환경별 설정 방법은 [환경 구성 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

[HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io) 같은 서비스를 사용하고, `smtp` 드라이버로 메일을 "실제 발송"해도 더미 박스에서 확인할 수 있습니다. Mailtrap 등의 메시지 뷰어를 통해 실제 최종 이메일 레이아웃을 확인할 수 있는 것이 장점입니다.

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, [Mailpit](https://github.com/axllent/mailpit)에서 메시지를 미리 볼 수 있습니다. Sail이 실행 중이라면, `http://localhost:8025`에서 Mailpit 인터페이스를 이용하세요.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

마지막으로, 애플리케이션 시작 시점에 `Mail` 파사드의 `alwaysTo` 메서드로 글로벌 수신 주소를 지정할 수도 있습니다. 보통 ServiceProvider의 `boot` 메서드에서 호출합니다:

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

`alwaysTo`를 사용하면, 모든 메일의 추가 "cc", "bcc" 주소는 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

메일 메시지 전송 중, Laravel은 두 가지 이벤트를 디스패치합니다. `MessageSending`은 메시지 발송 전에, `MessageSent`는 메시지 발송 후에 발생합니다. 이 이벤트들은 *큐잉이 아니라 실제 전송 시점*에만 발생합니다. 필요하다면 [이벤트 리스너](/docs/12.x/events)를 구현해 활용하세요:

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

Laravel은 여러가지 이메일 전송 방식을 기본 제공합니다. 그러나 직접 지원하지 않는 외부 서비스를 위해 커스텀 전송 방식을 작성할 수도 있습니다. 새로운 전송 방식을 만들려면, `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속받고, `doSend`, `__toString` 메서드를 구현하세요:

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

정의한 커스텀 전송 방식은, `Mail` 파사드의 `extend` 메서드로 등록해야 합니다. 보통은 `AppServiceProvider`의 `boot` 메서드에서 이 작업을 합니다. 이때, 클로저의 `$config` 인자엔 `config/mail.php` 설정에서 해당 메일러에 할당한 설정 배열이 전달됩니다:

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

커스텀 전송 방식 등록이 끝나면, `config/mail.php` 설정에 해당 전송 방식을 사용하는 메일러를 추가하세요:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식

Laravel은 Mailgun, Postmark 등 일부 Symfony 공식 메일 전송 방식을 기본 제공하지만, 그 외 Symfony에서 관리하는 추가 패키지도 자유롭게 확장해 쓸 수 있습니다. 예를 들어, "Brevo"(구 Sendinblue) Symfony 메일러를 Composer로 추가하고 아래처럼 등록할 수 있습니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치가 완료되면, 애플리케이션의 `services` 설정 파일에 Brevo API 자격증명을 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그리고 서비스 프로바이더의 `boot`에서 `Mail` 파사드의 `extend`로 전송 방식을 등록합니다:

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

이제 `config/mail.php`에서 해당 전송 방식을 갖는 메일러를 정의하면 사용할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
