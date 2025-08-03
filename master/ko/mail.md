# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 조건](#driver-prerequisites)
    - [페일오버 구성](#failover-configuration)
    - [라운드로빈 구성](#round-robin-configuration)
- [메일러블 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [첨부 가능한 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 현지화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [개발 환경에서 메일 다루기](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송](#custom-transports)
    - [추가 Symfony 전송](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/7.0/mailer.html) 컴포넌트를 기반으로 하는 깔끔하고 단순한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 통한 이메일 전송용 드라이버를 제공하여, 사용자가 로컬이나 클라우드 기반 서비스 중 선택하여 빠르게 메일을 보낼 수 있도록 합니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내 각 메일러는 고유한 설정과 고유한 "transport"를 가질 수 있어서, 애플리케이션에서 특정 이메일 메시지 전송에 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭셔널 이메일에는 Postmark를, 대량 이메일에는 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 내부에는 `mailers` 배열이 있습니다. 이 배열은 Laravel이 지원하는 주요 메일 드라이버/전송기 각각의 예제 구성 항목을 포함하고 있으며, `default` 설정 값은 애플리케이션에서 기본으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송기 사전 조건

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버들이 SMTP 서버를 통한 메일 전송보다 간단하고 빠른 경우가 많습니다. 가능하면 이들 드라이버 중 하나를 사용하길 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 사용해 Symfony의 Mailgun Mailer 전송기를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그다음, 애플리케이션의 `config/mail.php` 설정 파일에서 기본 메일러를 `mailgun`으로 설정하세요:

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

추가로, `config/services.php` 파일에 다음 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 이외의 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용한다면, `services` 설정 파일에서 리전의 엔드포인트를 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 전송기를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그다음 애플리케이션의 `config/mail.php` 기본 옵션을 `postmark`로 설정하세요. 이후 `config/services.php` 설정 파일에는 다음 옵션을 포함해야 합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하려면, `config/mail.php` 파일 내 해당 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 사용하는 다중 Postmark 메일러를 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer를 통해 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

이후 `config/mail.php`에서 기본 메일러를 `resend`로 설정하고, `config/services.php`에는 다음 설정을 포함해야 합니다:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer로 다음 패키지를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

그후 `config/mail.php`에서 기본 메일러를 `ses`로 설정하고, `config/services.php`에 다음 옵션들이 포함되었는지 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

세션 토큰을 사용한 AWS [임시 자격증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 활용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메일 메시지의 [`headers`](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환하세요:

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

AWS SDK의 `SendEmail` 메서드에 전달할 추가 [옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, SES 설정에 `options` 배열을 추가하세요:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스를 위한 API 기반 Laravel 드라이버를 제공합니다. Composer로 다음 패키지를 설치하세요:

```shell
composer require mailersend/laravel-driver
```

설치 후, 애플리케이션 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하고, `MAIL_MAILER` 변수는 `mailersend`로 설정하세요:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php` 파일 내 `mailers` 배열에 MailerSend 설정을 추가하세요:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend의 호스팅 템플릿 사용법 등 자세한 내용은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 페일오버 구성

간혹 설정한 외부 메일 전송 서비스가 중단될 수 있습니다. 이 경우, 기본 전송기가 중단되었을 때 사용할 하나 이상의 백업 메일 전송 구성을 정의하는 것이 유용합니다.

이를 위해, 애플리케이션의 `mail` 설정에서 `failover` 전송기를 사용하는 메일러를 정의하세요. 그리고 `failover` 메일러의 설정 배열에 이메일 전송 시 선택할 순서대로 `mailers` 배열을 지정합니다:

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

`failover` 메일러를 정의한 후, 애플리케이션 기본 메일러로 설정하려면 `default` 설정 키에 해당 이름을 지정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드로빈 구성

`roundrobin` 전송기는 여러 메일러에 분산해서 메일 전송 작업을 분배할 수 있게 합니다. 시작하려면, `mail` 설정 파일에 `roundrobin` 전송기를 사용하는 메일러를 정의하고, 어떤 메일러들을 사용할지 `mailers` 배열로 지정하세요:

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

이후 기본 메일러를 `roundrobin` 메일러로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 전송기는 구성된 메일러 리스트에서 무작위로 하나를 선택하고, 이후 메일부터는 다음 메일러로 순차적으로 전환합니다. 이는 `failover` 전송기가 *[고가용성](https://en.wikipedia.org/wiki/High_availability)*을 구현하는 것과 달리, *[로드 밸런싱](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성

Laravel 애플리케이션에서 전송하는 각 이메일 유형은 "mailable" 클래스 하나로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없더라도 걱정하지 마세요. `make:mail` Artisan 명령어로 첫 번째 메일러블 클래스를 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성

메일러블 클래스를 생성한 후에는 내용을 확인해 보세요. 메일러블 설정은 `envelope`, `content`, `attachments` 메서드 등 여러 곳에서 이뤄집니다.

`envelope` 메서드는 메일 제목과 때로는 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문 생성을 위한 [Blade 템플릿](/docs/master/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope 사용하기

이제 이메일 발신자, 즉 이메일이 "누구로부터" 발송되는지 설정하는 방법을 살펴보겠습니다. 발신자 설정법은 크게 두 가지가 있는데, 첫 번째는 메시지의 envelope에서 직접 "from" 주소를 지정하는 방법입니다:

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
#### 전역 `from` 주소 사용하기

애플리케이션이 모든 이메일에 동일한 "from" 주소를 사용한다면, 매 메일러블마다 이를 반복해서 지정하는 건 번거로울 수 있습니다. 그 대신 `config/mail.php` 설정 파일에 전역 "from" 주소를 지정할 수 있습니다. 이 주소는 메일러블 클래스에서 별도의 `from` 주소를 지정하지 않을 때 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한 `reply_to` 전역 주소도 설정 파일에서 지정할 수 있습니다:

```php
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰 설정

메일러블 클래스의 `content` 메서드 안에서, 이메일 내용 렌더링을 위한 템플릿인 `view`를 지정할 수 있습니다. 이메일은 주로 [Blade 템플릿](/docs/master/blade)로 작성되기 때문에, Laravel의 강력한 Blade 기능을 활용해 편리하고 유연하게 이메일 HTML을 작성할 수 있습니다:

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
> 이메일 템플릿을 한 곳에 모아두려면 `resources/views/emails` 디렉터리를 만들어서 이를 활용해도 좋지만, `resources/views` 내 어디에 두어도 무방합니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하고 싶다면, `Content` 정의 시 `text` 파라미터에 plain-text 템플릿을 지정할 수 있습니다. `view`와 마찬가지로 템플릿 이름을 지정하며, HTML과 일반 텍스트 버전을 모두 가질 수 있습니다:

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

명확성을 위해 `html` 파라미터도 `view`의 별칭으로 사용할 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### 퍼블릭 프로퍼티를 통한 전달

일반적으로 뷰에서 렌더링할 데이터를 전달하려면, 메일러블 클래스에서 공용 퍼블릭 프로퍼티로 데이터를 정의하면 자동으로 뷰에 전달됩니다. 예를 들어, 생성자에서 데이터를 받아 퍼블릭 프로퍼티에 할당하세요:

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

이렇게 설정한 데이터는 Blade 템플릿에서 일반 데이터처럼 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

이메일에 전달하는 데이터 형식을 템플릿 전달 전에 가공하고 싶다면, `Content` 정의의 `with` 파라미터를 사용해 데이터를 직접 뷰에 전달할 수 있습니다. 보통 생성자에 전달된 데이터는 `protected` 혹은 `private` 프로퍼티로 설정해 자동으로 전달되는 것을 방지하고, `with`로 가공된 데이터를 제공합니다:

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

뷰에서 이렇게 전달한 데이터는 일반 변수처럼 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메시지의 `attachments` 메서드가 반환하는 배열에 첨부 파일들 정보를 추가하세요. 가장 간단한 방법은 파일 경로를 `Attachment` 클래스의 `fromPath` 메서드에 전달하는 것입니다:

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

첨부 파일의 표시 이름과 MIME 타입을 지정할 때는 `as` 와 `withMime` 메서드를 사용할 수 있습니다:

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
#### 디스크에 저장된 파일 첨부

파일 시스템 디스크에 저장된 파일을 첨부하려면 `fromStorage` 메서드를 사용하세요:

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

첨부 파일명과 MIME 타입 지정도 가능합니다:

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

기본 디스크가 아닌 다른 스토리지 디스크에서 파일을 첨부해야 할 경우 `fromStorageDisk`를 사용하세요:

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
#### 바이너리 데이터 첨부

메모리 내에 생성한 PDF 등 바이너리 데이터를 저장하지 않고 직접 첨부하려면, `fromData` 메서드를 사용할 수 있습니다. 이 메서드는 첨부할 데이터를 반환하는 클로저와 첨부파일명을 받습니다:

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

이메일에 인라인 이미지를 삽입하는 것은 보통 번거롭지만, Laravel은 편리한 방법을 제공합니다. 메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하세요. Laravel은 메일 템플릿에 자동으로 `$message` 변수를 제공하여 직접 전달할 필요가 없습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메일 템플릿에서는 지원되지 않습니다. 일반 텍스트는 인라인 첨부파일을 사용하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 바이너리 데이터 인라인 첨부

이미 원시 이미지 데이터를 가진 경우, `$message` 변수를 통해 `embedData` 메서드를 호출하고 인라인으로 삽입할 수 있습니다. 이때 파일명을 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체

대부분 경로 문자열로 파일을 첨부하지만, 자주 사용하는 여러 엔티티를 객체로 표현하는 경우가 많습니다. 예를 들어, 앱에서 사진을 첨부한다면 `Photo` 모델이 있을 수 있죠. 이럴 때 `Photo` 모델 인스턴스를 직접 전달해서 첨부할 수 있다면 매우 편리합니다. 이것이 첨부 가능한 객체입니다.

사용법은 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 해당 클래스에 구현하는 것입니다. 이 인터페이스는 `toMailAttachment` 메서드를 정의하도록 요구하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

이제 메일 메시지의 `attachments` 메서드에서 `Photo` 객체를 반환할 수 있습니다:

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

첨부파일 데이터가 Amazon S3 같은 원격 스토리지에 있을 수도 있으므로, Laravel은 앱의 [파일시스템 디스크](/docs/master/filesystem) 저장 데이터를 첨부하는 방법도 제공합니다:

```php
// 기본 디스크에 저장된 파일로 첨부 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 첨부 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한 메모리 내 데이터를 이용한 첨부 파일 생성도 가능합니다. `fromData` 메서드에 데이터를 생성하는 클로저와 이름을 전달하세요:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부 파일을 커스터마이징 하고 싶다면, `as` 및 `withMime` 메서드로 파일명과 MIME 타입을 지정할 수도 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

때로는 전송되는 메시지에 추가 헤더가 필요할 수 있습니다. 예를 들어, 사용자 정의 `Message-Id`나 임의 텍스트 헤더를 지정하는 경우입니다.

이를 위해 메일러블에 `headers` 메서드를 정의하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 파라미터를 받습니다. 필요한 것만 지정하면 됩니다:

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
### 태그와 메타데이터

Mailgun이나 Postmark 같은 일부 서드파티 이메일 공급자는 메시지를 그룹화하고 추적하기 위한 "태그"와 "메타데이터"를 지원합니다. 이는 메일 메시지의 `Envelope` 정의에 추가할 수 있습니다:

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

Mailgun 드라이버를 사용하는 경우, [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages)에 관한 자세한 내용은 Mailgun 문서를 참고하세요. Postmark 역시 [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)를 지원합니다.

Amazon SES를 사용하는 경우, 메일에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙이려면 `metadata` 메서드를 활용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer로 구현됩니다. Laravel은 메시지 전송 전에 Symfony 메시지 인스턴스에 커스텀 콜백을 등록할 수 있게 하여, 메일 전송 전에 메시지를 세밀하게 수정할 수 있습니다. 이 기능은 `Envelope` 정의에서 `using` 파라미터를 정의하면 됩니다:

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

마크다운 기반 메일러블 메시지는 [메일 알림](/docs/master/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있습니다. Markdown 문법으로 작성하면, Laravel은 아름답고 반응형인 HTML 템플릿과 자동으로 생성된 일반 텍스트 대체 버전을 렌더링합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿을 사용하는 메일러블은 `make:mail` Artisan 명령어의 `--markdown` 옵션으로 생성할 수 있습니다:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그리고 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용하세요:

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

Markdown 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합하여, Laravel 내장 이메일 UI 컴포넌트를 쉽게 활용할 수 있습니다:

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
> Markdown 이메일 작성 시 과도한 들여쓰기를 피하세요. Markdown 표준에 따라 들여쓰기는 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링하며, `url`과 선택적 `color` 인자를 받습니다. 지원 색상은 `primary`, `success`, `error`입니다. 메시지 내에 여러 버튼을 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 본문과 약간 다른 배경색의 영역으로 텍스트 블록을 감싸 주의를 끄는 데 활용됩니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 Markdown 테이블을 HTML 테이블로 변환하며, 콘텐츠로 Markdown 형식의 테이블을 받습니다. 기본 Markdown 테이블 정렬 문법을 지원합니다:

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

Markdown 메일 컴포넌트를 앱에 내보내어 직접 커스터마이징할 수 있습니다. `vendor:publish` Artisan 명령어를 사용해 `laravel-mail` 태그를 지정하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

명령어 실행 후 `resources/views/vendor/mail` 경로에 `html`과 `text` 폴더가 생성되며, 각 폴더 내에는 컴포넌트별 템플릿이 포함됩니다. 자유롭게 수정 가능합니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 내보낸 뒤, `resources/views/vendor/mail/html/themes` 폴더에 `default.css` 파일이 있습니다. CSS를 수정하면 Markdown 메일 메시지의 HTML에 자동으로 인라인 스타일로 변환됩니다.

새 테마를 만들고 싶으면 `html/themes` 디렉터리에 CSS 파일을 추가한 후, `config/mail.php` 설정에서 `theme` 옵션에 새 테마 이름을 지정하세요.

특정 메일러만 다르게 스타일 적용하고 싶으면, 해당 메일러 클래스의 `$theme` 속성에 테마 이름을 설정하면 됩니다.

<a name="sending-mail"></a>
## 메일 전송

`Mail` [퍼사드](/docs/master/facades)의 `to` 메서드를 사용해 메일을 보낼 수 있습니다. `to`에는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션을 지정할 수 있습니다. 객체나 컬렉션을 전달하면 자동으로 각각의 `email`과 `name` 속성을 사용해 수신자를 설정합니다. 수신자 지정 후, `send` 메서드에 메일러블 인스턴스를 전달하세요:

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

또한, "to" 뿐만 아니라 "cc"와 "bcc" 수신자를 메서드 체이닝으로 지정할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

받는 사람 목록에 여러 명이 있을 때 반복문으로 메일을 순차 전송할 수도 있지만, `to` 메서드는 수신자를 누적시키므로 이전 수신자에게도 계속 메일이 가는 점에 유의하세요. 따라서 수신자마다 매번 메일러블 인스턴스를 새로 생성해 메일을 전송해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 이용한 메일 전송

기본적으로 Laravel은 `config/mail.php`에서 설정된 기본 메일러로 이메일을 전송합니다. 하지만 `mailer` 메서드를 통해 특정 메일러를 지정할 수 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송은 응답 시간을 지연시킬 수 있어, 보통 메일을 백그라운드 작업으로 큐에 넣어 보내는 경우가 많습니다. Laravel의 내장 [통합 큐 API](/docs/master/queues)를 사용하면 쉽게 구현 가능합니다. `Mail` 퍼사드의 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

큐 사용을 위해서는 [큐 설정](/docs/master/queues)이 미리 필요합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메일 큐잉

지정한 시간 후에 메일을 보내려면, `later` 메서드를 사용하세요. 첫 번째 인수로는 `DateTime` 인스턴스를 전달합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐와 연결에 푸시하기

`make:mail`로 생성한 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용합니다. 이를 통해 각 메일러블 인스턴스에서 `onQueue`와 `onConnection` 메서드를 호출해 큐 이름과 큐 드라이버를 지정할 수 있습니다:

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
#### 기본적으로 큐에 넣기

항상 큐로 처리하길 원하는 메일러블 클래스가 있다면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이렇게 하면 `send` 메서드를 호출해도 항상 큐로 작업이 넘어갑니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### DB 트랜잭션과 큐된 메일러블

DB 트랜잭션 안에서 큐로 메일러블 작업을 디스패치하면 트랜잭션이 커밋되기 전에 큐 작업이 실행될 수 있습니다. 이 경우 트랜잭션 내에서 변경되거나 생성한 모델, 데이터가 큐 작업 시점에 존재하지 않아 문제를 일으킬 수 있습니다.

큐 연결 설정 중 `after_commit`이 `false`로 되어 있다면, `afterCommit` 메서드를 호출해 해당 메일러블이 트랜잭션 커밋 후에 디스패치되도록 할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자 안에서 `afterCommit`을 호출할 수도 있습니다:

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
> 큐 작업과 DB 트랜잭션 관련 추가 정보는 [큐 작업과 DB 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링

메일러블을 실제로 전송하지 않고 HTML 내용을 캡처하고 싶을 때가 있습니다. 이때, 메일러블의 `render` 메서드를 호출하면 평가된 HTML 문자열을 얻을 수 있습니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인 중일 때, 실제 이메일을 보내지 않고도 브라우저에서 미리보기를 원할 수 있습니다. Laravel은 라우트 클로저나 컨트롤러에서 메일러블 객체를 직접 반환할 때, 이를 렌더링하여 브라우저에 표시해주는 기능을 제공합니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 현지화

Laravel은 요청의 현재 로케일 외에 다른 로케일로도 메일러블을 전송할 수 있으며, 큐 작업으로 예약해도 이 설정을 기억합니다.

이를 위해 `Mail` 퍼사드의 `locale` 메서드를 사용해 원하는 언어를 지정하세요. 메일러블 템플릿 평가 시 해당 로케일로 변경됐다가 평가 완료 후 원래 로케일로 돌아갑니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

애플리케이션이 각 사용자의 선호 로케일을 저장한다면, 해당 모델에 `HasLocalePreference` 인터페이스를 구현해 Laravel이 선호 로케일을 자동으로 사용하게 할 수 있습니다:

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

인터페이스 구현 후에는 `locale` 메서드를 따로 호출하지 않아도 해당 로케일로 메일/알림이 전송됩니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

Laravel은 메일러블 구조를 검사하는 다양한 메서드를 제공합니다. 메일러블 내용이 기대하는 내용을 포함하는지 검증하는 편리한 메서드들도 있습니다. 여기에는 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등이 있습니다.

HTML 검증은 HTML 버전에서, 텍스트 검증은 일반 텍스트 버전에서 주어진 문자열 포함 여부를 확인합니다:

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

메일러블 내용 테스트와는 별개로, 특정 메일러블이 사용자에게 "전송되었는지" 테스트할 수도 있습니다. 메일러블의 구체적인 내용은 테스트 대상 코드와 충분히 분리할 수 있으므로, Laravel이 메일 전송 요청을 받았음을 확인하는 것만으로 충분한 경우가 많습니다.

`Mail` 퍼사드의 `fake` 메서드를 호출하면 실제 메일을 보내지 않고, 다음과 같이 여러 검증 메서드를 제공받습니다:

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

백그라운드에서 큐로 메일러블을 전송하는 경우에는 `assertSent` 대신 `assertQueued` 메서드를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 검사 조건을 담는 클로저를 전달해 해당 조건을 만족하는 메일러블이 전송되었는지 확인할 수 있습니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

또한, 메일러블 인스턴스는 `hasTo`, `hasCc`, `hasBcc`, `hasReplyTo`, `hasFrom`, `hasSubject` 와 같은 유용한 검사 메서드를 제공합니다:

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

첨부파일에 대해서도 검사 메서드를 제공합니다:

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

메일이 전송되지 않았음을 검증하는 메서드엔 `assertNotSent`와 `assertNotQueued`가 있습니다. 메일이 전송도, 큐에 저장도 되지 않았음을 확인하려면 `assertNothingOutgoing` 및 `assertNotOutgoing` 메서드를 사용하세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 개발 환경에서 메일 다루기

이메일 전송 앱을 개발할 때, 실제 이메일을 보내는 것이 부담될 수 있습니다. Laravel은 개발환경에서 이메일 전송을 "비활성화" 하거나 대체할 다양한 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 이메일을 실제 보내는 대신 로그 파일에 기록해 이메일 내용을 확인할 수 있습니다. 이 드라이버는 주로 개발 환경에서 사용합니다. 환경별 설정 방법은 [환경 구성 문서](/docs/master/configuration#environment-configuration)를 참조하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com) 또는 [Mailtrap](https://mailtrap.io) 같은 서비스를 사용해, `smtp` 드라이버로 메일을 "더미" 메일박스로 보내 실 이메일 클라이언트 환경에서 메일 내용을 확인할 수 있습니다. 이 방식을 쓰면 메일trap 메시지 뷰어에서 완성된 이메일을 직접 검토할 수 있습니다.

[Laravel Sail](/docs/master/sail) 이용 시, [Mailpit](https://github.com/axllent/mailpit) 으로 메일 미리보기가 가능합니다. Sail 실행 중에는 `http://localhost:8025` 경로에서 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, 모든 발송 메일이 특정 주소로 전송되도록 `Mail` 퍼사드의 `alwaysTo` 메서드를 호출해 전역 수신자를 설정할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 실행합니다:

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

Laravel은 메일 전송 과정에서 두 가지 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메일 전송 직전에, `MessageSent` 이벤트는 전송 후에 발생합니다. 큐잉 시점이 아니라 실제 *전송* 시점에 발생합니다. 애플리케이션 내에서 이 이벤트들의 [리스너](/docs/master/events)를 정의할 수 있습니다:

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
## 커스텀 전송

Laravel은 다양한 메일 전송기를 내장하지만, 지원하지 않는 메일 서비스를 위해 직접 전송기를 작성할 수도 있습니다. 이를 위해 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하고 `doSend`와 `__toString()` 메서드를 구현하세요:

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

전송기를 정의한 후, `Mail` 퍼사드의 `extend` 메서드로 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 수행하며, 설정 배열을 인자로 받는 클로저를 전달하세요:

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

커스텀 전송기 등록 후에는 `config/mail.php` 파일에 해당 전송기를 사용하는 메일러 설정을 추가하세요:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송기

Laravel은 Mailgun, Postmark 등 일부 Symfony 유지 보수 전송기를 지원합니다. 추가로 다른 Symfony 전송기를 적용하려면 Composer로 패키지를 설치하고, Laravel에 등록하세요. 예를 들어, "Brevo" (전 "Sendinblue") Symfony 메일러를 설치하는 방법입니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후 `config/services.php` 파일에 API 키를 추가하세요:

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

`boot` 메서드에서 `Mail` 퍼사드의 `extend`로 등록합니다:

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

정의한 전송기를 `config/mail.php` 설정 내 메일러 정의에 추가하세요:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```