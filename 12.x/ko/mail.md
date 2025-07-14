# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [장애 조치 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [Mailable 클래스 생성](#generating-mailables)
- [Mailable 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
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
## 소개

이메일을 보내는 일은 결코 복잡할 필요가 없습니다. 라라벨은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깔끔하고 간단한 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail` 등 다양한 방법으로 이메일을 전송할 수 있는 드라이버를 제공하므로, 로컬 또는 클라우드 기반의 원하는 서비스로 신속하게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

라라벨의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 정의된 각 메일러는 고유한 설정과 전송 방식(transport)을 지정할 수 있으므로, 애플리케이션에서 특정 이메일 종류별로 다른 메일 서비스를 사용할 수 있습니다. 예를 들어, 애플리케이션에서는 거래 관련 이메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일 내에는 `mailers` 배열이 있습니다. 이 배열에는 라라벨이 지원하는 주요 메일 드라이버 또는 트랜스포트에 대한 샘플 설정이 담겨 있습니다. 그리고 `default` 설정 값은 애플리케이션이 이메일을 전송할 때 기본으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비 사항

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 일반적으로 SMTP 서버를 통한 방식보다 더 간편하고 빠릅니다. 가능하다면 이 중 하나의 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 지정합니다.

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 아래와 같이 mailgun 설정을 추가합니다.

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러 설정 이후, `config/services.php` 설정 파일에 다음 옵션을 추가합니다.

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 이외의 [Mailgun 리전](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하는 경우, `services` 설정 파일에서 해당 리전의 엔드포인트를 지정해야 합니다.

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치합니다.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 지정합니다. 기본 메일러를 설정한 후, `config/services.php` 설정 파일에 아래 옵션이 있는지 확인합니다.

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하려면, 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 배열은 애플리케이션의 `config/mail.php`에 있습니다.

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 여러 개의 Postmark 메일러를 각각 다른 메시지 스트림으로 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend의 PHP SDK를 설치해야 합니다.

```shell
composer require resend/resend-php
```

이후 `config/mail.php` 설정 파일의 `default` 옵션을 `resend`로 지정합니다. 기본 메일러를 설정한 뒤, `config/services.php` 설정 파일에 다음과 같은 옵션이 포함되어야 합니다.

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 우선 Amazon AWS SDK for PHP를 설치해야 합니다. Composer 패키지 관리자를 이용해 아래와 같이 설치할 수 있습니다.

```shell
composer require aws/aws-sdk-php
```

다음으로, `config/mail.php` 설정 파일의 `default` 옵션을 `ses`로 지정하고, `config/services.php` 설정 파일에 아래와 같은 옵션이 있는지 확인합니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰을 통해 사용할 경우, SES 설정에 `token` 키를 추가할 수 있습니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환되는 배열에 `X-Ses-List-Management-Options` 헤더를 반환할 수 있습니다.

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

이메일 전송 시 라라벨이 AWS SDK의 `SendEmail` 메서드에 추가적으로 옵션을 전달하도록 하려면, `ses` 설정에 `options` 배열을 지정할 수 있습니다. [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)도 마찬가지로 지정합니다.

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일과 SMS를 제공하는 서비스로, 라라벨용 API 기반 메일 드라이버 패키지를 직접 제공합니다. 이 드라이버 패키지는 Composer 패키지 관리자로 설치할 수 있습니다.

```shell
composer require mailersend/laravel-driver
```

패키지 설치 후에는 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 또한 `MAIL_MAILER` 환경 변수 역시 `mailersend`로 지정해야 합니다.

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php` 설정 파일의 `mailers` 배열에 MailerSend를 추가하세요.

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend에 대한 자세한 내용과 호스팅 템플릿 사용 방법 등은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)에서 확인할 수 있습니다.

<a name="failover-configuration"></a>
### 장애 조치(Failover) 설정

외부 서비스가 다운되어 애플리케이션의 메일 발송이 중단될 수 있습니다. 이럴 때를 대비해, 기본 메일 드라이버가 정상 동작하지 않을 경우 사용될 백업용 메일 발송 구성을 하나 이상 정의해두면 도움이 됩니다.

이를 위해서는 `mail` 설정 파일에 `failover` 트랜스포트를 사용하는 메일러를 정의해야 합니다. `failover` 메일러 설정 배열에는 메일 발송 순서를 참고할 메일러 배열이 포함되어야 합니다.

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

`failover` 메일러를 정의했다면, 이 메일러를 애플리케이션에서 사용할 기본 메일러로 지정해야 합니다. 이를 위해 `mail` 설정 파일의 `default` 설정 값을 해당 이름으로 지정하세요.

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(Round Robin) 설정

`roundrobin` 트랜스포트를 사용하면 여러 개의 메일러에 메일 전송 작업을 분산시킬 수 있습니다. 먼저 `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의해야 합니다. 설정 배열의 `mailers` 값에 실제로 사용할 메일러들을 나열합니다.

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

`roundrobin` 메일러를 정의했다면, 이 메일러를 애플리케이션의 기본 메일러로 지정해야 합니다. 이를 위해 `mail` 설정 파일의 `default` 값에 이름을 설정하세요.

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 구성된 메일러 목록에서 무작위로 하나를 선택해 메일을 발송한 후, 다음 이메일부터는 순서대로 계속해서 사용할 수 있도록 스위칭합니다. `failover` 트랜스포트가 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)* 확보에 중점을 둔다면, `roundrobin` 트랜스포트는 *[부하 분산(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 을 제공합니다.

<a name="generating-mailables"></a>
## Mailable 클래스 생성

라라벨 애플리케이션을 구축할 때, 애플리케이션에서 발송하는 각각의 이메일 타입은 "mailable" 클래스 하나로 표현됩니다. 이 클래스들은 기본적으로 `app/Mail` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없다면 걱정하지 마세요. 최초로 mailable 클래스를 `make:mail` Artisan 명령어로 생성하면 자동으로 만들어집니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 클래스 작성

mailable 클래스를 생성했다면, 파일을 열어서 내부를 살펴보겠습니다. Mailable 클래스의 여러 설정은 `envelope`, `content`, `attachments` 등의 메서드에서 구현합니다.

`envelope` 메서드는 메시지의 제목(Subject)과, 필요에 따라 수신자(Recipient)를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade) 정보를 담는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope를 이용한 방식

먼저, 이메일의 발신자를 설정하는 방법부터 살펴보겠습니다. 즉, 이 이메일이 누구로부터 발송되는지("from")를 정의하는 것입니다. 설정 방법은 두 가지가 있습니다. 첫 번째는, 메시지의 envelope(봉투)에 "from" 주소를 명시하는 방법입니다.

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

필요하다면 `replyTo` 주소도 동시에 지정할 수 있습니다.

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

만약 모든 메일의 발신자 주소가 동일하다면, 모든 mailable 클래스에서 직접 지정하는 것은 번거로울 수 있습니다. 이럴 때는, `config/mail.php` 설정 파일에 글로벌 "from" 주소를 지정해둘 수 있습니다. 이 값은 mailable 클래스에서 따로 "from" 주소를 지정하지 않은 경우 기본값으로 사용됩니다.

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, `config/mail.php` 파일에 글로벌 "reply_to" 주소를 정의할 수도 있습니다.

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

mailable 클래스의 `content` 메서드에서 이메일 본문을 렌더링할 때 사용할 `view`(템플릿)를 지정할 수 있습니다. 대부분의 이메일 본문은 [Blade 템플릿](/docs/12.x/blade)으로 작성하며, 이를 활용하면 익숙한 Blade의 모든 편의 기능과 문법을 사용할 수 있습니다.

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
> 이메일 템플릿을 모두 보관할 용도로 `resources/views/mail` 디렉토리를 만들기를 권장하지만, 실제로는 `resources/views` 디렉터리 내 어느 위치에 두어도 무방합니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트(Plain Text) 이메일

이메일의 일반 텍스트 버전을 따로 정의하고 싶을 때는, 메시지의 `Content` 정의 시 plain-text용 템플릿을 지정할 수 있습니다. `text` 파라미터였던 것처럼, 템플릿 이름을 지정하면 해당 템플릿이 이메일의 내용으로 렌더링됩니다. HTML 버전과 plain-text 버전을 모두 정의해둘 수도 있습니다.

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

연관성을 명확하게 하고 싶다면, `view` 대신 `html` 파라미터를 사용할 수도 있습니다.

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 프로퍼티를 통한 데이터 전달

대부분의 경우, 이메일을 렌더링할 때 사용할 데이터를 뷰에 전달하고 싶을 것입니다. 뷰로 데이터를 전달하는 방법은 두 가지가 있습니다. 첫 번째는, mailable 클래스에 public 프로퍼티를 선언하고 여기에 생성자 등에서 값을 할당하는 것입니다. 이렇게 하면 해당 데이터가 자동으로 뷰에서 사용할 수 있게 됩니다.

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

public 프로퍼티에 값이 할당된 후에는, Blade 템플릿에서 다른 데이터처럼 자유롭게 사용할 수 있습니다.

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 데이터 전달

템플릿에 데이터를 전달하기 전에 포맷을 커스터마이즈하고 싶다면, mailable의 `Content` 정의 시 `with` 파라미터를 통해 직접 데이터를 전달할 수 있습니다. 일반적으로 mailable 클래스의 생성자에서 데이터를 받아오되, 이 경우 해당 값을 `protected` 또는 `private` 프로퍼티에 저장해야 뷰에서 자동으로 노출되지 않습니다.

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

이렇게 `with` 파라미터를 통해 데이터를 전달하면, 해당 데이터 역시 템플릿 내에서 바로 사용할 수 있습니다.

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드가 반환하는 배열에 파일을 추가하면 됩니다. 먼저 `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 넘겨 첨부할 수 있습니다.

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

파일을 첨부할 때, 표시될 파일 이름이나 MIME 타입 지정도 가능합니다. 각각 `as` 와 `withMime` 메서드를 사용하면 됩니다.

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
#### 파일 시스템 디스크에서 파일 첨부

만약 파일을 [파일시스템 디스크](/docs/12.x/filesystem)에 저장해두었다면, `fromStorage` 첨부 메서드를 사용해 이메일에 파일을 첨부할 수 있습니다.

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

마찬가지로, 첨부 파일 이름이나 MIME 타입을 지정할 수 있습니다.

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

기본 파일시스템 디스크 이외의 디스크에서 파일을 첨부해야 한다면, `fromStorageDisk` 메서드를 사용할 수 있습니다.

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

#### Raw Data 첨부 파일

`fromData` 첨부 파일 메서드를 사용하면 바이트 문자열(원시 데이터)을 첨부 파일로 추가할 수 있습니다. 예를 들어, 메모리 내에서 PDF 파일을 생성한 뒤, 디스크에 저장하지 않고 바로 이메일에 첨부해야 할 때 이 방법을 활용할 수 있습니다. `fromData` 메서드는 첨부할 원시 데이터 바이트를 반환하는 클로저와 첨부 파일에 지정할 이름을 인수로 받습니다.

```php
/**
 * 해당 메시지의 첨부 파일을 반환합니다.
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
### 인라인 첨부 파일

이메일에 인라인 이미지를 삽입하는 작업은 일반적으로 번거롭지만, 라라벨에서는 이미지를 쉽게 첨부할 수 있는 편리한 방법을 제공합니다. 인라인 이미지를 삽입하려면, 메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. 라라벨은 모든 메일 템플릿에서 `$message` 변수를 자동으로 사용할 수 있도록 해주기 때문에, 직접 전달할 필요가 없습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트(plain-text) 메일 템플릿에서는 사용할 수 없습니다. 일반 텍스트 메시지에는 인라인 첨부 파일 기능이 제공되지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 첨부 이미지 삽입

만약 이메일 템플릿에 삽입하려는 이미지 데이터가 문자열 형태의 원시 데이터로 이미 있다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이 메서드를 호출할 때, 임베드된 이미지에 지정할 파일명을 함께 전달해야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체(Attachable Objects)

파일 경로 문자열로 메시지에 파일을 첨부하는 것이 충분한 경우가 많지만, 실제로 애플리케이션에서 첨부해야 하는 엔티티가 클래스로 표현되는 경우도 많습니다. 예를 들어, 애플리케이션에서 사진을 메시지에 첨부할 때, 해당 사진을 나타내는 `Photo` 모델이 있을 수 있습니다. 이럴 때 `Photo` 모델 객체 자체를 `attach` 메서드에 전달할 수 있다면 매우 편리할 것입니다. 바로 이 역할을 첨부 가능한 객체(Attachable Objects)가 담당합니다.

먼저, 메시지에 첨부 가능한 객체가 되려면 해당 객체에서 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현해야 합니다. 이 인터페이스는 클래스 내에 `toMailAttachment` 메서드가 구현되어 있어야 하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 모델의 첨부 파일 표현을 반환합니다.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

첨부 가능한 객체를 정의했다면, 이메일 메시지를 만들 때 `attachments` 메서드에서 해당 객체의 인스턴스를 반환할 수 있습니다.

```php
/**
 * 해당 메시지의 첨부 파일을 반환합니다.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

물론 첨부 파일 데이터가 Amazon S3 등 외부 파일 저장 서비스에 저장되어 있을 수도 있습니다. 라라벨은 애플리케이션의 [파일 시스템 디스크](/docs/12.x/filesystem) 중 하나에 저장된 데이터로부터 첨부 파일 인스턴스를 생성할 수 있도록 지원합니다.

```php
// 기본 디스크에서 파일로 첨부 파일 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일로 첨부 파일 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

이외에도, 메모리에 가지고 있는 데이터로 첨부 파일 인스턴스를 생성할 수도 있습니다. 이 경우에는 `fromData` 메서드에 클로저를 전달하여 첨부 파일의 원시 데이터를 반환하게 하면 됩니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

라라벨은 첨부 파일의 다양한 사용자 지정을 지원하는 메서드도 제공합니다. 예를 들어 `as` 및 `withMime` 메서드를 사용하여 파일 이름과 MIME 타입을 원하는 값으로 지정할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

때로는 발신 메시지에 추가 헤더를 붙여야 할 필요가 있습니다. 예를 들어, 커스텀 `Message-Id`를 지정하거나 임의의 텍스트 헤더를 추가해야 할 수도 있습니다.

이럴 때는 mailable 클래스에 `headers` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 파라미터를 받을 수 있습니다. 물론 필요한 파라미터만 선택적으로 전달하면 됩니다.

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * 메시지 헤더를 반환합니다.
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

Mailgun, Postmark 같은 일부 외부 이메일 서비스에서는 메시지에 대한 "태그"와 "메타데이터"를 지원하며, 이를 이용해 애플리케이션에서 보낸 이메일을 그룹화하거나 추적할 수 있습니다. 태그와 메타데이터는 `Envelope` 정의에서 이메일 메시지에 추가할 수 있습니다.

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope을 반환합니다.
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

만약 애플리케이션에서 Mailgun 드라이버를 사용한다면, [Mailgun 문서의 태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) 관련 정보를 참고하시기 바랍니다. Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원에 대해서도 Postmark 공식 문서를 참고하실 수 있습니다.

만약 Amazon SES를 이용해 이메일을 보내는 경우, [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부하기 위해 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

라라벨의 메일 기능은 Symfony Mailer를 기반으로 동작합니다. 라라벨에서는 실제 메시지가 전송되기 전에 Symfony Message 인스턴스로 커스텀 콜백을 등록할 수 있는데, 이를 통해 메시지 발송 전에 메시지를 더욱 세밀하게 커스터마이즈할 수 있습니다. 이를 위해, `Envelope` 정의에 `using` 파라미터를 추가하면 됩니다.

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지 envelope을 반환합니다.
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
## 마크다운(Markdown) 메일러블

마크다운 메일러블 메시지를 사용하면, 메일 알림([mail notifications](/docs/12.x/notifications#mail-notifications))의 사전 제작된 템플릿 및 컴포넌트의 이점을 메일러블에서도 활용할 수 있습니다. 메시지가 마크다운으로 작성되므로 라라벨은 메시지에 대해 보기 좋고 반응형인 HTML 템플릿을 렌더링해주며, 동시에 일반 텍스트 버전도 자동으로 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 적용된 메일러블을 생성하려면, `make:mail` 아티즌 명령어의 `--markdown` 옵션을 사용할 수 있습니다.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, 메일러블 내의 `content` 메서드에서 mailable의 `Content` 정의를 구성할 때, `view` 대신 `markdown` 파라미터를 사용합니다.

```php
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지 컨텐츠 정의를 반환합니다.
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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 구문을 조합하여, 라라벨의 내장 이메일 UI 컴포넌트를 쉽게 활용하면서 메일 메시지를 손쉽게 작성할 수 있도록 도와줍니다.

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
> 마크다운 이메일을 작성할 때에는 들여쓰기를 과도하게 사용하지 마십시오. 마크다운 표준에 따라, 마크다운 파서는 들여쓰기된 내용을 코드 블록으로 렌더링합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 필수 인수로 `url`, 선택적 인수로 `color`를 받습니다. 지원되는 색상 옵션은 `primary`, `success`, `error`입니다. 한 메시지에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 제공된 텍스트 블록을, 메시지의 다른 부분과 약간 다른 배경색을 가진 패널로 렌더링하여 특정 텍스트 블록에 주목을 끌 수 있게 해줍니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환할 수 있게 해줍니다. 이 컴포넌트는 내용으로 마크다운 테이블을 받으며, 기본 마크다운 테이블 정렬 구문을 이용해 컬럼 정렬도 지원합니다.

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

모든 마크다운 메일 컴포넌트를 내 애플리케이션에 내보내어 자유롭게 커스터마이징할 수 있습니다. 컴포넌트를 내보내려면, `vendor:publish` 아티즌 명령어를 사용하여 `laravel-mail` 에셋 태그를 퍼블리시합니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령은 마크다운 메일 컴포넌트들을 `resources/views/vendor/mail` 디렉터리에 퍼블리시합니다. `mail` 디렉터리는 `html`과 `text` 디렉터리를 포함하며, 각각의 디렉터리에는 모든 컴포넌트의 HTML 및 텍스트 버전 뷰 파일이 들어 있습니다. 이제 이 컴포넌트들을 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보낸 뒤에는 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. 이 파일에서 CSS를 원하는 대로 수정하면, 작성한 스타일이 마크다운 메일 메시지의 HTML 버전에 자동으로 인라인 CSS로 적용됩니다.

라라벨의 마크다운 컴포넌트 테마를 아예 새로 만들고 싶다면, 새 CSS 파일을 `html/themes` 디렉터리에 추가하면 됩니다. 파일명을 정하고 저장한 후, 애플리케이션의 `config/mail.php` 설정 파일에서 `theme` 옵션 값을 새 테마 이름으로 업데이트하면 됩니다.

개별 mailable에 대해 사용할 테마를 달리 하고 싶다면, mailable 클래스의 `$theme` 프로퍼티에 사용하고자 하는 테마 이름을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 보내기

메일을 보내려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 인수로 받을 수 있습니다. 객체나 객체의 컬렉션을 전달하면, 해당 객체의 `email`과 `name` 속성을 자동으로 참조하여 이메일의 수신자를 결정하므로, 이 속성이 객체에 정의되어 있어야 합니다. 수신자를 지정한 뒤, 전송할 mailable 클래스의 인스턴스를 `send` 메서드에 전달하면 됩니다.

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
     * 지정한 주문을 배송 처리합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문을 배송 처리...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

메일 전송 시 "받는 사람(to)"만 지정할 필요는 없습니다. "받는 사람(to)", "참조(cc)", "숨은 참조(bcc)"를 각각의 메서드로 연이어 지정할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자 반복 루프 처리

때때로, 여러 명의 수신자나 이메일 주소 배열을 순회하면서 각각에게 개별적으로 메일러블을 전송해야 할 수 있습니다. 이때 `to` 메서드는 수신자 리스트에 이메일을 추가하기 때문에, 루프를 돌 때마다 모든 이전 수신자에게도 다시 메일이 전송됩니다. 따라서 반드시 수신자마다 새로운 메일러블 인스턴스를 생성해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에서 `default`로 지정된 메일러를 사용해 이메일을 전송합니다. 하지만 `mailer` 메서드를 사용하면, 특정 메일러 설정을 이용해 메시지를 보낼 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송은 애플리케이션의 응답 시간을 저하시킬 수 있기 때문에, 많은 개발자들은 이메일 전송 작업을 백그라운드로 큐에 보내는 방식을 선호합니다. 라라벨은 내장 [통합 큐 API](/docs/12.x/queues)를 통해 이 작업을 손쉽게 처리할 수 있습니다. 메일 메시지를 큐에 넣으려면, 수신자를 지정한 후 `Mail` 파사드의 `queue` 메서드를 사용하면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 큐에 작업을 추가하여, 메시지가 백그라운드에서 전송되게 만들어줍니다. 이 기능을 사용하기 전에 반드시 [큐를 설정](/docs/12.x/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메시지 큐잉

큐에 넣은 이메일 메시지 전송을 일정 시간 지연하고 싶다면, `later` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 언제 메시지를 전송할지 나타내는 `DateTime` 인스턴스를 받습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 넣기

`make:mail` 명령어로 생성된 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, 모든 메일러블 인스턴스에서 `onQueue`와 `onConnection` 메서드를 사용할 수 있습니다. 이를 이용하면 메시지 전송에 사용할 큐 연결 이름 및 큐 이름을 지정할 수 있습니다.

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

일부 메일러블 클래스는 항상 큐로 처리되길 원할 수 있습니다. 이 경우 해당 클래스에서 `ShouldQueue` 계약을 구현하면 됩니다. 이렇게 하면 `send` 메서드를 사용해도 실제로는 큐에 넣어 비동기적으로 전송됩니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블을 데이터베이스 트랜잭션 내에서 디스패치할 경우, 메시지가 데이터베이스 트랜잭션이 커밋되기 전에 큐에 의해 처리될 수도 있습니다. 이럴 경우, 트랜잭션 중에 모델이나 DB 레코드를 업데이트했다면, 아직 DB에는 반영되지 않았을 수 있습니다. 또한, 트랜잭션 내에서 생성한 모델이나 레코드가 아예 DB에 존재하지 않을 수도 있습니다. 만약 메일러블이 이러한 모델에 의존한다면, 큐 작업이 처리될 때 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정 옵션이 `false`로 되어 있다면, 특정 큐잉 메일러블만 데이터베이스 트랜잭션이 모두 커밋된 이후에 디스패치하도록, 메일 전송 시 `afterCommit` 메서드를 호출할 수 있습니다.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 메일러블의 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
     * 새 메시지 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이러한 문제점의 우회 방안에 대해 더 알아보고 싶다면, [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하시기 바랍니다.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 전송 실패 처리

큐잉된 이메일 전송이 실패한 경우, 해당 큐잉 메일러블 클래스에 `failed` 메서드가 정의되어 있다면 이 메서드가 호출됩니다. 실패 원인이 담긴 `Throwable` 인스턴스가 `failed` 메서드의 인수로 전달됩니다.

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
     * 큐잉된 이메일 전송 실패를 처리합니다.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링

가끔 메일을 실제로 보내지 않고, 해당 메일러블의 HTML 컨텐츠만 얻고 싶을 때가 있습니다. 이럴 땐 메일러블의 `render` 메서드를 호출하면 됩니다. 이 메서드는 mailable의 랜더링된 HTML 콘텐츠를 문자열로 반환합니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인할 때, 일반 Blade 템플릿처럼 브라우저에서 빠르게 렌더링 미리보기를 할 수 있으면 매우 편리합니다. 라라벨에서는 경로 클로저나 컨트롤러에서 어떤 메일러블이든 반환만 하면, 실제 메일 주소로 전송하지 않고도 렌더링 결과를 바로 브라우저에서 미리볼 수 있게 해줍니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블의 로케일 지정

라라벨은 현재 요청의 로케일과는 다른 언어로 메일러블을 보낼 수 있으며, 큐에 들어간 경우에도 이 로케일 설정을 기억합니다.

이를 위해 `Mail` 파사드에서는 원하는 언어를 지정할 수 있는 `locale` 메서드를 제공합니다. 이 메서드를 사용하면, 해당 메일러블의 템플릿이 평가되는 동안 애플리케이션의 로케일을 일시적으로 변경했다가, 평가가 끝나면 원래 로케일로 자동 복구됩니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자의 선호 로케일

어떤 애플리케이션에서는 각 사용자의 선호 언어(로케일)를 사용자별로 저장해 둘 수 있습니다. 모델에 `HasLocalePreference` 계약을 구현하면, 해당 모델로 메일을 보낼 때 라라벨이 자동으로 저장된 로케일을 적용하도록 할 수 있습니다.

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일을 반환합니다.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

인터페이스를 구현했다면, 라라벨이 해당 모델에 메일러블이나 알림을 보낼 때 자동으로 선호 로케일을 사용합니다. 따라서, 이 인터페이스를 사용할 때는 별도로 `locale` 메서드를 호출할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>

## 테스트

<a name="testing-mailable-content"></a>
### 메일러블(Mailable) 콘텐츠 테스트

라라벨은 메일러블의 구조를 확인할 수 있는 다양한 메서드를 제공합니다. 또한, 메일러블에 예상한 콘텐츠가 포함되어 있는지 테스트하는 데 유용한 여러가지 메서드도 제공합니다. 제공되는 메서드는 다음과 같습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk`.

이 중 "HTML"로 끝나는 어서션 메서드는 메일러블의 HTML 버전에 특정 문자열이 있는지 확인하며, "text"로 끝나는 어서션 메서드는 평문(plain-text) 버전에 특정 문자열이 포함되어 있는지 확인합니다:

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
### 메일러블 발송 테스트

메일러블의 "발송" 자체가 특정 사용자에게 이루어졌는지 테스트하는 코드와, 메일러블의 콘텐츠 자체를 테스트하는 코드를 분리해서 작성하는 것이 좋습니다. 일반적으로 메일러블의 실제 콘텐츠는 여러분이 테스트하려는 코드와 직접적으로 관련되지 않으며, 라라벨이 해당 메일러블을 발송하도록 "지시"했는지만 확인해도 충분합니다.

실제 메일이 전송되지 않게 하려면 `Mail` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드를 호출한 뒤, 특정 메일러블이 사용자에게 발송되었는지 여부와, 메일러블이 전달받은 데이터까지도 검사할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 발송 처리...

    // 어떤 메일러블도 발송되지 않았는지 확인
    Mail::assertNothingSent();

    // 메일러블이 발송되었는지 확인
    Mail::assertSent(OrderShipped::class);

    // 메일러블이 두 번 발송되었는지 확인
    Mail::assertSent(OrderShipped::class, 2);

    // 지정한 이메일 주소로 메일러블이 발송되었는지 확인
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 여러 이메일 주소로 메일러블이 발송되었는지 확인
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 해당 메일러블이 발송되지 않았는지 확인
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3개의 메일러블이 발송되었는지 확인
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

        // 주문 발송 처리...

        // 어떤 메일러블도 발송되지 않았는지 확인
        Mail::assertNothingSent();

        // 메일러블이 발송되었는지 확인
        Mail::assertSent(OrderShipped::class);

        // 메일러블이 두 번 발송되었는지 확인
        Mail::assertSent(OrderShipped::class, 2);

        // 지정한 이메일 주소로 메일러블이 발송되었는지 확인
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // 여러 이메일 주소로 메일러블이 발송되었는지 확인
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // 해당 메일러블이 발송되지 않았는지 확인
        Mail::assertNotSent(AnotherMailable::class);

        // 총 3개의 메일러블이 발송되었는지 확인
        Mail::assertSentCount(3);
    }
}
```

메일러블을 백그라운드에서 큐로 발송하는 경우에는 `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

메일이 발송(또는 큐잉)되었는지 검사할 때, `assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 주어진 "조건"을 만족하는 메일러블이 하나라도 있으면 어서션은 성공합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

이러한 어서션 메서드에 전달하는 클로저 내부에서는, 메일러블 인스턴스가 메일의 수신자, 참조, 숨은 참조, 답장 주소, 발신자, 제목 등을 검사할 수 있는 다양한 메서드를 제공합니다:

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

메일러블 인스턴스에서는 첨부파일에 대해서도 다음과 같이 여러 편리한 메서드를 제공합니다:

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

메일이 발송되지 않았는지 확인하는 메서드로 `assertNotSent`, `assertNotQueued` 두 가지가 있습니다. 메일이 "발송되지도 않고 큐에도 등록되지 않음"을 동시에 확인하려면 `assertNothingOutgoing` 또는 `assertNotOutgoing`를 사용할 수 있습니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

이메일을 보내는 애플리케이션을 개발할 때, 실제 이메일 주소로 메일이 발송되는 것은 원치 않을 수 있습니다. 라라벨은 로컬 개발시 실제 메일 발송을 "비활성화"할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버를 사용하면 실제로 이메일을 보내는 대신, 모든 메일 메시지를 로그 파일에 기록하여 확인할 수 있습니다. 이 드라이버는 주로 로컬 개발 단계에서 사용됩니다. 환경별 애플리케이션 설정에 대해 더 알고 싶다면 [환경별 설정 문서](/docs/12.x/configuration#environment-configuration)를 참고해 주세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)과 같은 서비스를 `smtp` 드라이버와 함께 사용할 수 있습니다. 이를 통해 이메일 메시지를 "더미" 메일함으로 보내고, 실제 이메일 클라이언트에서 메일을 확인할 수 있습니다. 이 방법은 Mailtrap의 메시지 뷰어에서 최종적으로 어떤 이메일이 전송되는지 직접 확인할 수 있다는 점이 장점입니다.

[라라벨 Sail](/docs/12.x/sail)을 사용 중이라면, [Mailpit](https://github.com/axllent/mailpit)을 이용해 메일을 미리 볼 수 있습니다. Sail이 실행 중인 경우, `http://localhost:8025`에서 Mailpit 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 사용하여 모든 메일이 특정 주소로만 발송되도록 전역 "to" 주소를 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션 서비스 프로바이더의 `boot` 메서드 안에서 호출해야 합니다:

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

라라벨에서는 메일 메시지가 발송되는 과정에서 두 가지 이벤트가 발생합니다. `MessageSending` 이벤트는 메시지가 발송되기 *직전*에, `MessageSent` 이벤트는 메시지 발송이 완료된 *직후*에 발생합니다. 이 이벤트들은 메일이 "발송(send)"될 때(즉, 큐에 등록될 때가 아니라 실제로 발송되는 시점)에 발생한다는 점을 유의하세요. 애플리케이션에서 이 이벤트들을 위한 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다:

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
## 커스텀 트랜스포트

라라벨은 다양한 메일 트랜스포트를 기본 제공하지만, 라라벨이 기본적으로 지원하지 않는 서비스로 이메일을 발송하고자 할 때 직접 트랜스포트를 작성할 수도 있습니다. 커스텀 메일 트랜스포트를 만들려면 먼저 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 확장하는 클래스를 정의합니다. 그리고 나서 `doSend`와 `__toString` 메서드를 구현하면 됩니다:

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

커스텀 트랜스포트를 정의했다면, `Mail` 파사드에서 제공하는 `extend` 메서드를 사용해 트랜스포트를 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 수행합니다. 이때, `extend` 메서드에 전달하는 클로저에는 설정 파일(`config/mail.php`)에 정의한 해당 메일러의 설정 배열이 `$config` 인자로 전달됩니다:

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

트랜스포트 등록이 완료되면, `config/mail.php` 설정 파일에 새로운 트랜스포트를 사용하는 메일러 정의를 추가할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

라라벨은 Mailgun, Postmark와 같이 Symfony 공식 트랜스포트를 지원합니다. 그 외의 Symfony에서 관리되는 추가 트랜스포트를 사용하고 싶은 경우, Composer로 관련 Symfony 메일러 패키지를 설치한 뒤 라라벨에 등록할 수 있습니다. 예를 들어 "Brevo"(이전 명칭: "Sendinblue") Symfony 메일러를 설치하고 등록하려면 다음과 같이 합니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지를 설치한 후, 애플리케이션의 `services` 설정 파일에 Brevo API 인증 정보를 추가합니다:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그 다음, `Mail` 파사드의 `extend` 메서드를 이용해 라라벨에 트랜스포트를 등록합니다. 이 작업은 주로 서비스 프로바이더의 `boot` 메서드 안에서 처리합니다:

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

이제 등록한 트랜스포트를 사용하는 메일러 정의를 `config/mail.php` 설정 파일에 다음과 같이 추가하여 사용할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```