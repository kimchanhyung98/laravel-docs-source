# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 / 전송 방식 사전 준비](#driver-prerequisites)
    - [Failover 설정](#failover-configuration)
    - [Round Robin 설정](#round-robin-configuration)
- [메일러블 클래스 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [메일러블을 브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로, 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail` 등 다양한 이메일 전송 드라이버를 지원하여, 로컬 또는 클라우드 기반의 원하는 서비스로 신속하게 메일 전송을 시작할 수 있게 해줍니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 안에서 각각의 메일러는 고유한 설정과 전송(transport) 방식을 가질 수 있으므로, 특정 목적에 따라 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 애플리케이션에서 Postmark로 거래(트랜잭션) 메일을 보내고, Amazon SES로 대량 메일을 발송할 수도 있습니다.

`mail` 설정 파일에서는 `mailers` 배열을 찾을 수 있습니다. 이 배열은 Laravel이 지원하는 주요 메일 드라이버/전송 방식에 대한 샘플 구성을 담고 있으며, `default` 값은 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 사전 준비

Mailgun, Postmark, Resend와 같이 API 기반 드라이버는 SMTP 서버를 이용하는 것보다 더 단순하면서 빠른 경우가 많습니다. 가능한 경우 이들 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 전송 패키지를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 파일에서 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 아래와 같이 `mailers` 배열에 Mailgun 설정을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

설정이 완료되면, `config/services.php` 파일에 다음과 같은 Mailgun 옵션을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 이외의 [Mailgun 지역](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하고 있다면, 해당 지역의 엔드포인트를 `services` 설정 파일에서 정의할 수 있습니다:

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

`config/mail.php` 파일의 `default` 값을 `postmark`로 설정한 후, `config/services.php` 파일에 다음 옵션이 포함되었는지 확인합니다:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

특정 Mailer에 대해 사용할 Postmark 메시지 스트림을 지정하려면, `mailers` 배열에 `message_stream_id` 옵션을 추가하세요:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 구성할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer를 통해 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

그리고 `config/mail.php`의 `default` 옵션을 `resend`로 설정한 뒤, `config/services.php` 파일에 아래 옵션을 추가합니다:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 PHP용 Amazon AWS SDK를 Composer로 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

그런 다음, `config/mail.php`에서 기본 메일러를 `ses`로 지정하고, `config/services.php` 파일에 아래 설정이 포함되어 있는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하고 싶다면, `token` 키를 SES 설정에 추가합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환할 수 있습니다:

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

AWS SDK의 `SendEmail` 메서드에 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 전달하려면, `ses` 설정 내에 `options` 배열을 정의할 수 있습니다:

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
### Failover 설정

외부 이메일 서비스가 다운될 경우를 대비해, 백업(예비) 메일 전송 구성을 미리 정의할 수 있습니다. 이런 상황에서는, 하나 이상의 백업 이메일 전송 구성을 사용해 메일 서비스 장애 시 활용할 수 있습니다.

이를 위해, `mail` 설정 파일에 `failover` 전송 방식을 사용하는 메일러를 정의합니다. 해당 메일러의 설정 배열에는 전송에 사용할 메일러들의 순서를 참고할 `mailers` 배열을 포함해야 합니다:

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

failover 메일러를 기본 메일러로 사용하려면, `mail` 설정 파일의 `default` 값을 `failover`로 지정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### Round Robin 설정

`roundrobin` 전송 방식은 여러 메일러에 메일 발송 부하를 분산시킬 수 있도록 해줍니다. `mail` 설정 파일에 `roundrobin` 전송 방식을 사용하는 메일러를 추가하십시오. `mailers` 배열에 실제로 전송에 사용할 메일러들을 나열합니다:

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

마찬가지로, 이 메일러를 default로 사용하려면 다음과 같이 지정합니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

round robin 전송 방식은 설정된 메일러 목록 중 무작위로 메일러를 골라 메일을 보내고, 이후 각 메일은 순차적으로 다음 메일러로 전환됩니다. `failover` 전송 방식이 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)* 을 주로 목표로 한다면, `roundrobin` 전송 방식은 *[부하 분산(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 을 달성하는 데 초점을 둡니다.

<a name="generating-mailables"></a>
## 메일러블 클래스 생성 (Generating Mailables)

Laravel 애플리케이션은 발송되는 각 이메일 유형을 "메일러블(mailable)" 클래스(객체)로 나타냅니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면 첫 번째 메일러블 클래스 생성 시 자동으로 생성됩니다. 메일러블 클래스는 `make:mail` Artisan 명령어를 통해 생성할 수 있습니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 열어서 내부 구조를 살펴볼 수 있습니다. 메일러블 클래스의 설정은 `envelope`, `content`, `attachments` 등의 메서드에서 이루어집니다.

`envelope` 메서드는 메시지의 제목(subject) 및(필요 시) 수신자 정보를 담는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문을 생성할 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope를 이용한 설정

먼저, 이메일의 발신자(from)를 설정하는 방법을 살펴보겠습니다. 두 가지 방식이 있습니다. 첫째, 해당 메시지의 envelope에 직접 발신자 주소를 지정하는 것입니다:

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

필요하다면, `replyTo` 주소도 지정할 수 있습니다:

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
#### 전역 from 주소 사용

애플리케이션의 모든 이메일 발신자가 동일하다면, 각 메일러블마다 from 주소를 추가하는 것이 번거로울 수 있습니다. 이럴 때에는 `config/mail.php` 설정 파일에 전역 from 주소를 지정해두면, 개별 메일러블에서 별도 설정이 없을 경우 이 주소가 자동으로 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, `config/mail.php` 파일에 전역 reply_to 주소도 지정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서, 메일 내용 렌더링에 사용할 템플릿(`view`)을 지정할 수 있습니다. 보통 이메일 본문 작성 시 [Blade 템플릿](/docs/12.x/blade)을 활용하므로, Blade의 강력한 기능을 모두 사용할 수 있습니다:

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
> 이메일 템플릿을 모아둘 용도로 `resources/views/mail` 디렉터리를 만드는 것이 좋으나, 실제로는 `resources/views` 내 원하는 위치 어디든 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일(Plain Text Emails)

일반 텍스트 버전의 이메일도 정의하고 싶다면, 메시지의 `Content` 정의에서 plain-text 템플릿을 추가하면 됩니다. `view`와 마찬가지로 `text` 파라미터에도 템플릿 이름을 지정합니다. HTML과 plain-text 버전을 함께 정의할 수도 있습니다:

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

명확성을 위해, `html` 파라미터를 `view`의 별칭으로 사용할 수도 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성을 통한 데이터 전달

이메일 본문 렌더링용으로, 뷰에 데이터를 전달해야 합니다. 첫 번째 방법은, 메일러블 클래스 내에 정의된 public 속성이 자동으로 뷰에 전달되는 것입니다. 즉, 생성자를 통해 받은 데이터를 public 속성에 할당하면 됩니다:

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

public 속성에 데이터가 할당되면, Blade 템플릿에서 아래와 같이 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### with 파라미터를 통한 데이터 전달

이메일 데이터의 형식을 가공해서 템플릿에 전달하고 싶다면, `Content` 정의에서 `with` 파라미터를 사용할 수 있습니다. 이 경우, 생성자에서는 protected 혹은 private 속성으로 데이터를 보관해야 하며, 템플릿에는 with로 전달한 데이터만 노출됩니다:

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

이렇게 전달한 데이터는 템플릿에서 다음과 같이 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드가 반환하는 배열에 첨부 파일 정보를 추가합니다. 첨부 파일은 `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 넘겨 추가할 수 있습니다:

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

첨부파일을 붙일 때, 표시명과 MIME 타입을 지정할 수도 있습니다:

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

[파일 시스템 디스크](/docs/12.x/filesystem)에 파일이 저장되어 있다면, `fromStorage` 메서드를 사용해 이메일에 첨부할 수 있습니다:

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

이때 역시 이름과 MIME 타입을 지정할 수 있습니다:

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

기본이 아닌 다른 디스크를 사용할 경우, `fromStorageDisk` 메서드를 사용할 수 있습니다:

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

바이트 문자열 데이터를 바로 첨부하고 싶다면, `fromData` 메서드를 사용할 수 있습니다. 예를 들어, 메모리에서 PDF를 생성하고 이를 첨부하고자 할 때 이 방법을 사용합니다. `fromData`는 클로저와 첨부파일 이름을 받습니다:

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

이메일 본문에 이미지를 인라인으로 삽입하는 것은 대개 번거로운 작업이지만, Laravel은 간편한 방법을 제공합니다. 이메일 템플릿에서 `$message` 변수의 `embed` 메서드를 사용해 이미지를 본문에 삽입할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에서 자동으로 사용할 수 있습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 메시지 템플릿에서는 사용할 수 없습니다. plain-text 메시지는 인라인 첨부를 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

Raw 이미지 데이터 문자열을 이미 이메일 템플릿에 넣고자 한다면, `$message`의 `embedData` 메서드를 사용할 수 있습니다. 이때 이미지를 식별할 파일명을 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

간단히 파일 경로 문자열로 첨부파일을 추가하는 것 외에도, 애플리케이션에서 사진 등 첨부 대상으로 쓰일 엔터티가 클래스로 관리되는 경우가 많습니다. 예를 들어, 사진을 첨부파일로 보내려면 Photo 모델을 바로 첨부할 수 있으면 편리합니다. Attachable 객체가 이를 가능케 해줍니다.

먼저, 해당 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현합니다. 이 인터페이스의 `toMailAttachment` 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

이후, 메일 메시지 작성시 `attachments` 메서드에서 해당 객체를 그대로 반환할 수 있습니다:

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

첨부 데이터가 Amazon S3와 같은 원격 스토리지에 있다면, Laravel은 파일 시스템 디스크의 데이터를 통한 첨부도 지원합니다:

```php
// 기본 디스크에서 파일 첨부...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일 첨부...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

메모리 내 데이터로도 첨부파일 인스턴스를 생성할 수 있습니다. 이 경우 `fromData` 메서드에 클로저를 전달하여 원시 데이터를 반환하게 하면 됩니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

추가로, 첨부파일의 이름과 MIME 타입은 `as`와 `withMime` 메서드로 변경할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

가끔은 메시지에 추가적인 헤더를 붙여야 할 때가 있습니다. 예를 들어, 커스텀 `Message-Id`나 기타 임의의 텍스트 헤더를 추가할 수 있습니다.

이를 위해, 메일러블에 `headers` 메서드를 정의하고 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환합니다. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받습니다. 필요한 항목만 선택적으로 지정할 수 있습니다:

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

Mailgun, Postmark와 같은 일부 써드파티 이메일 제공업체들은 "태그"와 "메타데이터"를 지원합니다. 이는 애플리케이션에서 발송한 이메일을 그룹화하거나 추적하는 데 쓸 수 있습니다. `Envelope` 정의에서 태그와 메타데이터를 추가할 수 있습니다:

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

Mailgun 드라이버 사용 시 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) 관련 공식 문서를 참고할 수 있습니다. Postmark에 대해서도 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원 문서를 참고하세요.

Amazon SES를 사용할 경우, `metadata` 메서드를 이용해 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이즈 (Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer 위에서 동작합니다. 메시지 전송 전에 Symfony Message 인스턴스를 활용해 원하는 커스터마이징을 할 수 있도록, 커스텀 콜백을 등록할 수 있습니다. 이를 위해, `Envelope` 정의에서 `using` 파라미터를 사용하면 됩니다:

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

마크다운 메일러블 메시지를 사용하면, [메일 알림](/docs/12.x/notifications#mail-notifications)의 컴포넌트와 사전 제작된 템플릿을 메일러블에서도 그대로 활용할 수 있습니다. 메시지는 마크다운 문법으로 작성하며, Laravel은 자동으로 세련되고 반응형인 HTML 템플릿과 plain-text 버전을 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 연결된 메일러블을 생성하려면, `make:mail` Artisan 명령어의 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그 다음, 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 활용합니다:

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

마크다운 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합해, Laravel이 제공하는 UI 컴포넌트를 간편하게 사용할 수 있습니다:

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
> 마크다운 이메일 작성 시 들여쓰기를 과하게 하지 마세요. 마크다운 규칙에 따라, 들여쓰기된 내용은 코드블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트 (Button Component)

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 옵션인 `color`(옵션: `primary`, `success`, `error`)를 인수로 받으며, 원하는 만큼 여러 번 사용할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트 (Panel Component)

패널 컴포넌트는 지정한 텍스트 블럭을 주변과 배경색이 조금 다른 패널에 표시하여, 특정 내용을 강조합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트 (Table Component)

테이블 컴포넌트를 이용하면 마크다운 테이블을 HTML 테이블로 렌더링할 수 있습니다. 테이블 열 정렬도 마크다운 표준에 따라 지원됩니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈 (Customizing the Components)

모든 마크다운 메일 컴포넌트를 애플리케이션 내로 내보내서(customize) 수정할 수 있습니다. `vendor:publish` Artisan 명령어를 통해 `laravel-mail` 에셋 태그로 컴포넌트를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이렇게 하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리 아래로 복사됩니다. 여기에는 `html` 디렉터리와 `text` 디렉터리가 있으며, 각 컴포넌트의 HTML/텍스트 버전을 담고 있습니다. 자유롭게 수정하세요.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트 퍼블리시 후, `resources/views/vendor/mail/html/themes` 폴더에는 `default.css` 파일이 위치합니다. 이 CSS를 수정하면 스타일이 자동으로 인라인 CSS로 변환되어 HTML 메일에 적용됩니다.

완전히 새 테마를 만들고 싶으면, 해당 디렉터리에 새로운 CSS 파일을 두고, `config/mail.php` 파일의 `theme` 옵션을 새 테마 이름으로 바꾸세요.

개별 메일러블마다 다른 테마를 쓰고 싶다면, 메일러블 클래스의 `$theme` 속성에 테마명을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 전송 (Sending Mail)

메일을 전송하려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to`는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체나 객체 컬렉션을 전달할 경우, 메일러는 자동으로 객체의 `email` 및 `name` 속성을 사용해 메일 수신자를 결정합니다. 수신자를 지정한 후, 메일러블 인스턴스를 `send` 메서드에 넘겨 전송합니다:

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

"to"뿐 아니라, "cc", "bcc" 수신자도 각각 메서드 체이닝으로 추가할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자 반복 처리

여러 수신자에게 반복문으로 메일을 보내야 할 때, `to` 메서드는 이전 대상을 계속 누적합니 다. 따라서 반드시 반복문 내에서 메일러블 인스턴스를 새로 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 전송

기본적으로 Laravel은 `mail` 설정 파일에서 지정한 default 메일러로 이메일을 보냅니다. 하지만, `mailer` 메서드를 사용해 특정 메일러 구성을 이용할 수도 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송은 애플리케이션 응답 시간을 저하시킬 수 있기 때문에, 많은 개발자들은 메일 전송 작업을 큐에 등록(백그라운드 전송)합니다. Laravel은 [통합 큐 API](/docs/12.x/queues)로 이를 쉽게 지원합니다. 메일 전송을 큐에 올리려면 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 큐에 작업을 추가해 백그라운드에서 메시지를 보냅니다. 기능 사용 전 [큐 설정](/docs/12.x/queues)이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메일 큐잉

큐에 등록된 메일의 전송을 일정 시간 늦추고 싶다면, `later` 메서드를 사용할 수 있습니다. 첫 번째 인수로 `DateTime` 인스턴스를 받아, 해당 시각 이후에 전송됩니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐로 전송

`make:mail`로 생성한 메일러블은 모두 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, `onQueue` 및 `onConnection` 메서드로 큐 이름과 연결을 직접 지정할 수 있습니다:

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
#### 기본적으로 큐잉

특정 메일러블 클래스를 항상 큐에 쌓아 전송하고 싶다면, 클래스에서 `ShouldQueue` 인터페이스를 구현하세요. `send`를 호출해도 항상 큐에 쌓여 백그라운드로 전송됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

트랜잭션 내에서 큐잉된 메일러블을 디스패치할 경우, 트랜잭션 커밋 전에 큐에서 작업이 처리될 수 있습니다. 그 경우, 트랜잭션 안에서 변경된 모델/레코드가 아직 커밋되지 않았으므로, 기대와 다른 문제가 발생할 수 있습니다. 또한 트랜잭션 안에서 생성된 레코드는 아직 DB에 존재하지 않을 수도 있습니다.

큐 연결(커넥션)의 `after_commit` 옵션이 `false`이면, `afterCommit` 메서드로 해당 메일러블이 모든 트랜잭션 커밋 후에 디스패치되도록 할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 생성자에서 `afterCommit`을 호출할 수도 있습니다:

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
> 이 문제를 우회하는 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 메일 전송 실패 처리

큐잉된 이메일이 전송에 실패하면, 해당 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 이때 실패 원인이 되는 `Throwable` 인스턴스가 매개변수로 전달됩니다:

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

이메일을 전송하지 않고, 메일러블의 HTML 내용을 그대로 얻고 싶을 때는, 메일러블의 `render` 메서드를 사용할 수 있습니다. 이 메서드는 렌더링된 HTML 내용을 문자열로 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 메일러블을 브라우저에서 미리보기

메일러블의 템플릿을 디자인할 때, 브라우저에서 Blade 템플릿처럼 렌더링 결과를 바로 미리보기 위해, Laravel에서는 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 반환하면 내용을 HTML로 렌더링해 브라우저에 표시합니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 지역화 (Localizing Mailables)

Laravel은 요청의 현재 로캘(locale)과 무관하게 특정 언어로 메일러블을 전송할 수 있으며, 큐에 등록된 경우에도 그 로캘이 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정할 수 있습니다. 메일러블 템플릿을 평가할 때 언어가 일시적으로 바뀌고, 평가가 끝나면 원래 로캘로 돌아갑니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로캘

애플리케이션에서 각 사용자의 선호 로캘(언어)을 저장하는 경우, 모델에 `HasLocalePreference` 인터페이스를 구현하면, 메일 전송 시 자동으로 저장된 언어가 사용됩니다:

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

이 인터페이스를 구현하면, Laravel은 메일러블과 알림 전송에 대해 자동으로 선호 로캘을 사용하므로, `locale` 메서드를 추가로 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

Laravel은 메일러블 구조를 검사할 수 있도록 다양한 메서드를 제공합니다. 또한, 메일러블이 의도한 내용을 담고 있는지 검증할 수 있는 유용한 메서드도 지원합니다:

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

"HTML" 계열의 assertion은 HTML 버전의 메일러블 내용이 해당 문자열을 포함하는지, "text" 계열의 assertion은 plain-text 버전이 해당 문자열을 포함하는지 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트

메일러블 내용을 검증하는 테스트와, 실제로 특정 사용자에게 메일러블이 "전송"됐는지를 검증하는 테스트를 구분할 것을 권장합니다. 많은 경우, 메일러블 내용이 테스트 코드에 직접적으로 중요하지 않으므로, Laravel이 해당 메일러블을 전송했다고 주장(assert)하는 정도면 충분합니다.

메일 전송 방지 목적으로 `Mail` 파사드의 `fake` 메서드를 쓸 수 있습니다. 이를 통해 메일 전송이 실제로 일어나지 않게 만들 수 있고, 그 후에는 특정 메일러블이 전송/큐잉됐는지를 자유롭게 assertion으로 검사할 수 있습니다:

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

큐로 백그라운드 전송하는 경우에는 `assertSent` 대신 `assertQueued` 계열 메서드를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 클로저를 전달해, 특정 조건을 만족하는 메일러블이 전송/큐잉되었는지 검증할 수 있습니다. 최소 하나라도 조건을 만족하면 assertion은 성공합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

클로저형 assertion은, 메일러블 인스턴스의 다양한 검사 메서드를 제공합니다:

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

메일러블 인스턴스는 첨부파일 확인을 위한 다양한 메서드도 제공합니다:

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

전송 **및** 큐잉 둘 다 일어나지 않았음을 검증하고 싶다면, `assertNothingOutgoing` 또는 `assertNotOutgoing`를 사용할 수 있습니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발환경 (Mail and Local Development)

실제 이메일 주소로 메일을 보내길 원하지 않는 로컬 개발 환경에서는, 아래 방법으로 "실제 전송"을 차단할 수 있습니다.

<a name="log-driver"></a>
#### 로그(Log) 드라이버

`log` 메일 드라이버를 사용하면, 이메일 전송 대신 메일 내용을 로그 파일에 기록합니다. 주로 로컬 개발에서만 활용합니다. 환경별 설정 방법은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또 다른 방법으로 [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스를 `smtp` 드라이버와 함께 사용해, 이메일을 "더미" 메일함에 보낼 수 있습니다. 이 방식은 실제 메일 클라이언트에서 최종 출력물을 직접 검사할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용 중이라면, [Mailpit](https://github.com/axllent/mailpit)을 통해 메시지를 미리볼 수 있습니다. Sail 실행 중엔 `http://localhost:8025` 에서 Mailpit 인터페이스를 확인할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 to 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 이용해 전역 "to" 주소를 지정할 수 있습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 아래처럼 사용합니다:

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

`alwaysTo`를 사용하면, 추가적인 "cc"나 "bcc" 주소는 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 발송 시 두 가지 이벤트를 디스패치합니다. `MessageSending` 이벤트는 메일 발송 직전에, `MessageSent` 이벤트는 발송 이후에 디스패치됩니다. 단, 이 이벤트들은 메일을 "전송"할 때 발생하며 "큐에 쌓을 때"가 아닙니다. [이벤트 리스너](/docs/12.x/events)를 만들면 아래처럼 활용할 수 있습니다:

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

Laravel은 다양한 메일 전송 방식을 내장하고 있지만, 지원되지 않는 외부 이메일 서비스와 연동하고 싶을 때 직접 전송 방식을 추가할 수 있습니다. 이를 위해, `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속한 클래스를 만들고, `doSend`, `__toString` 메서드를 구현하세요:

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

사용자 정의 전송 방식을 구현했다면, `Mail` 파사드의 `extend` 메서드로 등록합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 아래와 같이 등록합니다. 이때 `$config`에는 `config/mail.php`에 정의된 해당 메일러 설정 배열이 넘어옵니다:

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

등록을 마쳤으면, `config/mail.php`에 해당 커스텀 전송 방식을 사용하는 메일러 정의를 추가할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식 (Additional Symfony Transports)

Laravel은 Mailgun, Postmark 등 일부 Symfony 공식 메일 전송 방식을 내장 지원합니다. 그 외 추가 지원이 필요한 경우, Composer로 관련 Symfony 메일러 패키지를 설치하고 Laravel에 등록할 수 있습니다. 예를 들어, "Brevo"(구 Sendinblue)를 사용하려면 다음과 같이 진행합니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, Brevo API 정보를 `services` 설정 파일에 추가합니다:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

다음으로, `Mail` 파사드의 `extend` 메서드를 이용하여 전송 방식을 등록하세요. 보통 서비스 프로바이더의 `boot` 메서드에서 작성합니다:

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

이제 해당 전송 방식을 사용할 메일러 정의를 `config/mail.php`에 추가하세요:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
