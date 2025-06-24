# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
    - [장애 조치(Failover) 구성](#failover-configuration)
    - [라운드 로빈(Round Robin) 구성](#round-robin-configuration)
- [메일러블(Mailable) 클래스 생성](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더 설정](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 발송하기](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 로컬라이징](#localizing-mailables)
- [테스트하기](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일을 보내는 일은 복잡할 필요가 없습니다. 라라벨은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트 기반의 직관적이고 간단한 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail` 등 다양한 메일 전송 드라이버를 지원하므로, 로컬 또는 클라우드 기반 서비스 중 원하는 방식으로 손쉽게 메일을 보낼 수 있습니다.

<a name="configuration"></a>
### 설정

라라벨의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내에 각 메일러별로 고유한 설정(트랜스포트 포함)을 할 수 있어, 애플리케이션에서 특정 이메일은 서로 다른 메일 서비스를 사용해 보낼 수 있습니다. 예를 들어, 거래 관련 메일은 Postmark로 보내고, 대규모 이메일은 Amazon SES로 발송하는 식입니다.

`mail` 설정 파일에서 `mailers`라는 설정 배열을 찾을 수 있습니다. 이 배열에는 라라벨이 지원하는 주요 메일 드라이버/트랜스포트별로 샘플 설정이 들어 있습니다. `default` 설정 값은 애플리케이션이 이메일을 보낼 때 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 필수 조건

Mailgun, Postmark, Resend, MailerSend 등 API 기반의 드라이버는 보통 SMTP 서버 방식보다 더 간편하고 빠릅니다. 가능하다면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 먼저 기본 메일러를 `mailgun`으로 설정합니다.

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 다음 설정 배열을 `mailers` 배열에 추가합니다.

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

메일러 기본 설정이 끝났으면, `config/services.php` 설정 파일에 다음 옵션을 추가하세요.

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 외의 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용한다면, `services` 설정 파일 내에서 해당 리전의 엔드포인트를 지정할 수 있습니다.

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치하세요.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php`에서 `default` 항목을 `postmark`로 설정합니다. 설정 후, `config/services.php`에 다음 옵션이 포함되어 있는지 확인하세요.

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 Postmark 메시지 스트림을 메일러별로 지정하고 싶다면, `message_stream_id` 옵션을 해당 메일러의 설정 배열에 추가하면 됩니다. 이 설정 배열은 `config/mail.php` 파일에 있습니다.

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러도 구성할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer로 Resend의 PHP SDK를 설치하세요.

```shell
composer require resend/resend-php
```

애플리케이션의 `config/mail.php`에서 `default`를 `resend`로 설정합니다. 설정 후, `config/services.php` 파일에 다음 옵션을 포함해야 합니다.

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer에서 다음 라이브러리를 설치하세요.

```shell
composer require aws/aws-sdk-php
```

그리고 `config/mail.php`의 `default` 옵션을 `ses`로 설정하고, `config/services.php`에 다음 옵션이 있는지 확인합니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면 SES 설정에 `token` 키를 추가할 수 있습니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메일 메시지의 [headers](#headers) 메서드에서 배열을 반환할 때 `X-Ses-List-Management-Options` 헤더를 지정할 수 있습니다.

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

또, 라라벨이 이메일을 전송할 때 AWS SDK의 `SendEmail` 메서드로 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면 SES 설정에 `options` 배열을 추가할 수 있습니다.

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스를 제공하며, 라라벨 전용 API 기반 메일 드라이버를 직접 제공합니다. 해당 드라이버는 Composer로 설치할 수 있습니다.

```shell
composer require mailersend/laravel-driver
```

패키지 설치 후, 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 그리고 `MAIL_MAILER` 환경 변수도 `mailersend`로 지정합니다.

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php` 설정 파일의 `mailers` 배열에 MailerSend를 추가합니다.

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend에 대해 더 자세한 사용법(호스팅된 템플릿 사용법 등)은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(Failover) 구성

애플리케이션 메일 전송용으로 외부 서비스를 구성했는데, 해당 서비스가 일시적으로 다운되는 경우가 있습니다. 이런 상황을 대비해, 메인 드라이버가 장애일 때 사용할 하나 이상의 백업 메일 전송 설정을 정의할 수 있습니다.

이를 위해, 애플리케이션의 `mail` 설정 파일에 `failover` 트랜스포트를 사용하는 메일러를 정의해야 합니다. 이 메일러의 설정 배열에는 실제 메일러들의 이름이 포함된 `mailers` 배열이 있습니다. 이 배열의 순서대로 차례로 메일 전송을 시도합니다.

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

장애 조치용 메일러를 정의했다면, 이 메일러를 기본 메일러로 사용하도록 `mail` 설정 파일의 `default` 옵션에 해당 이름을 지정합니다.

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(Round Robin) 구성

`roundrobin` 트랜스포트를 사용하면 여러 메일러에 걸쳐 메일 전송 작업을 분산할 수 있습니다. 먼저, `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의하세요. 여기서 `mailers` 배열에는 실제로 사용할 메일러 이름들이 들어갑니다.

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

라운드 로빈 메일러가 정의되면, `mail` 설정 파일의 `default` 옵션에 해당 이름을 지정하여 기본 메일러로 사용하면 됩니다.

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 구성된 메일러 목록 중 무작위 하나를 골라 메일을 보낸 후, 이후 메일은 순차적으로 다음 메일러로 전환하여 분산 처리합니다. 장애 조치(`failover`) 트랜스포트가 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)* 확보에 초점을 맞췄다면, 라운드 로빈은 *[부하 분산(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*에 중점을 둡니다.

<a name="generating-mailables"></a>
## 메일러블(Mailable) 클래스 생성

라라벨 애플리케이션에서 각 이메일 종류는 "메일러블(Mailable)" 클래스 하나로 표현됩니다. 이런 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 이 디렉터리가 없다면 걱정하지 않으셔도 됩니다. 최초로 메일러블을 Artisan 명령어로 생성할 때 자동으로 만들어집니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기

메일러블 클래스를 생성했으면, 이제 해당 파일을 열어 내부 내용을 살펴볼 수 있습니다. 메일러블 클래스의 구성은 여러 메서드를 통해 이뤄집니다. 대표적으로 `envelope`, `content`, `attachments` 메서드가 있습니다.

`envelope` 메서드는 메시지의 제목(subject)과 경우에 따라 수신자 정보까지 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope를 통한 설정

먼저, 이메일의 발신자(sender)를 어떻게 지정하는지 살펴보겠습니다. 즉, 해당 이메일이 누구의 이름으로 발송될지 정하는 것입니다. 이를 설정하는 방법은 두 가지가 있습니다. 첫 번째 방법은 메시지의 envelope에서 `from` 주소를 직접 지정하는 것입니다.

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
#### 전역 `from` 주소 사용하기

반면, 애플리케이션 전체 이메일이 동일한 발신자 주소를 사용한다면, 매번 메일러블 클래스마다 `from`을 지정하는 일이 번거로울 수 있습니다. 이럴 땐 `config/mail.php` 설정 파일에 전역 "from" 주소를 지정할 수 있습니다. 메일러블에서 별도로 `from`을 지정하지 않으면 이 전역 주소가 사용됩니다.

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, `config/mail.php` 설정 파일에 전역 "reply_to" 주소도 지정할 수 있습니다.

```php
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드에서 이메일 내용을 렌더링할 때 사용할 `view`(템플릿)를 지정할 수 있습니다. 일반적으로 각 이메일은 [Blade 템플릿](/docs/12.x/blade)을 사용해 HTML을 생성하므로, 라라벨의 강력한 Blade 템플릿 기능을 모두 활용할 수 있습니다.

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
> 이메일 전용 Blade 템플릿을 보관하려면 `resources/views/emails` 디렉터리를 만드는 것이 좋습니다. 하지만 반드시 이 위치에 둘 필요는 없으며, `resources/views` 안 어디든 자유롭게 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 별도로 정의하고 싶으면, 메시지의 `Content` 정의 시 plain-text 템플릿을 지정할 수 있습니다. `view` 파라미터와 마찬가지로, `text` 파라미터에는 이메일 내용 생성을 위한 템플릿 이름을 넣으면 됩니다. 이렇게 하면 HTML 버전과 plain-text 버전을 모두 따로 지정할 수 있습니다.

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

또한, 더 명확하게 `html` 파라미터를 `view` 파라미터 대신 사용할 수도 있습니다.

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 속성을 통한 전달

일반적으로 이메일 렌더링 시 사용할 데이터를 뷰에 전달하고 싶을 것입니다. 데이터를 뷰에 넘기는 방법은 두 가지가 있습니다. 첫 번째로, 메일러블 클래스에서 정의한 public 속성은 자동으로 뷰에서 사용할 수 있게 됩니다. 예를 들어, 메일러블 클래스 생성자에서 데이터를 받아와 public 속성에 세팅하는 식입니다.

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

public 속성에 데이터가 저장되면, 뷰에서는 Blade 템플릿에서 일반 데이터처럼 접근할 수 있습니다.

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

이메일에 전달할 데이터의 포맷을 렌더링 전 커스텀하고 싶을 경우, `Content` 정의의 `with` 파라미터를 통해 데이터를 뷰에 전달할 수 있습니다. 이 방식에서는 보통 메일러블 생성자에서 데이터를 받아 protected나 private 속성에 저장합니다(자동 공개 방지 목적).

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

`with` 메서드로 전달된 데이터 역시 Blade 템플릿에서 일반 데이터처럼 사용할 수 있습니다.

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드가 반환하는 배열에 첨부 파일을 추가하면 됩니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 넣어 첨부 파일을 등록할 수 있습니다.

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

파일을 첨부할 때, 표시될 파일명이나 MIME 타입을 `as` 및 `withMime` 메서드로 지정할 수도 있습니다.

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
#### 파일 시스템의 파일 첨부

[파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 첨부하려면 `fromStorage` 메서드를 사용할 수 있습니다.

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

물론, 첨부 파일의 이름과 MIME 타입도 지정할 수 있습니다.

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

기본 디스크가 아닌 다른 저장소 디스크의 파일을 첨부하려면 `fromStorageDisk` 메서드를 사용하면 됩니다.

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

#### Raw Data 첨부

`fromData` 첨부 메서드를 사용하면, 원시 바이트 문자열을 첨부파일로 바로 추가할 수 있습니다. 예를 들어, 메모리 내에서 PDF 파일을 생성하여 디스크에 저장하지 않고 바로 이메일에 첨부하려는 경우 이 방법을 사용할 수 있습니다. `fromData` 메서드는 첨부할 원시 데이터 바이트를 반환하는 클로저와 해당 첨부파일의 이름을 인자로 받습니다.

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

이메일에 인라인 이미지를 삽입하는 작업은 보통 번거롭지만, 라라벨에서는 이미지를 손쉽게 이메일에 첨부할 수 있는 방법을 제공합니다. 인라인 이미지를 삽입하려면, 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. 라라벨은 모든 이메일 템플릿에 `$message` 변수를 자동으로 제공하므로 별도로 전달할 필요가 없습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메시지 템플릿에서는 사용하실 수 없습니다. 일반 텍스트 메시지에서는 인라인 첨부파일 기능을 사용할 수 없기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터로 첨부파일 임베딩

만약 이메일 템플릿에 첨부하고 싶은 이미지의 원시 데이터 문자열이 이미 있다면, `$message` 변수에서 `embedData` 메서드를 사용할 수 있습니다. `embedData` 메서드를 쓸 때는 임베딩할 이미지에 부여할 파일명을 함께 지정해야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체(Attachable Objects)

일반적으로 문자열 경로를 이용해 파일을 첨부하는 것으로 충분하지만, 실제 애플리케이션에서는 첨부할 대상을 객체(예: 모델)로 관리하는 경우가 많습니다. 예를 들어, 사진을 메시지에 첨부한다면 그 사진을 나타내는 `Photo` 모델이 있을 수도 있습니다. 이럴 때 해당 모델 인스턴스를 직접 `attach` 메서드에 전달할 수 있다면 훨씬 편리할 것입니다. 첨부 가능한 객체(Attachable 객체)를 사용하면 이렇게 할 수 있습니다.

시작하려면, 메시지에 첨부할 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 이 인터페이스는 반드시 `toMailAttachment` 메서드를 구현해야 하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

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

Attachable 객체를 정의했다면, 이메일 작성 시 `attachments` 메서드에서 해당 객체 인스턴스를 반환하면 됩니다.

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

물론 첨부파일 데이터가 Amazon S3와 같은 외부 파일 저장소에 저장되어 있을 수도 있습니다. 이 경우, 라라벨은 애플리케이션의 [파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 첨부파일 인스턴스로 생성할 수 있도록 도와줍니다.

```php
// 기본 디스크에 있는 파일로 첨부파일 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크(예: backblaze)에 있는 파일로 첨부파일 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 있는 데이터로 첨부파일 인스턴스를 만들 수도 있습니다. 이를 위해 `fromData` 메서드에 클로저를 전달하면 되며, 이 클로저는 첨부할 원시 데이터를 반환해야 합니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

라라벨은 첨부파일을 커스터마이즈할 수 있는 몇 가지 추가 메서드도 제공합니다. 예를 들어, `as`와 `withMime` 메서드를 사용해 파일 이름이나 MIME 타입을 원하는 대로 지정할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

때로는 발송하는 메시지에 추가 헤더를 붙여야 할 필요가 있습니다. 예를 들어, 특정 `Message-Id`를 지정하거나 임의의 텍스트 헤더를 추가하고 싶은 경우가 그렇습니다.

이럴 때는 mailable 클래스에 `headers` 메서드를 정의하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, 이 클래스는 `messageId`, `references`, `text` 파라미터를 받을 수 있습니다. 메시지에 필요한 값만 선택적으로 입력하면 됩니다.

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

Mailgun, Postmark 등 일부 외부 이메일 서비스에서는 발송하는 메시지에 "태그(tags)"나 "메타데이터(metadata)"를 붙여 그룹화하거나 추적할 수 있는 기능을 지원합니다. 이런 태그와 메타데이터는 mailable 클래스의 `Envelope` 정의에서 추가할 수 있습니다.

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

Mailgun을 사용할 경우, [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages)에 대한 자세한 내용은 공식 문서를 참고하세요. Postmark 역시 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 공지가 있으니 참고하시면 됩니다.

Amazon SES를 사용하는 경우, 메시지에 [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙이려면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

라라벨의 메일 기능은 Symfony Mailer를 기반으로 동작합니다. 라라벨에서는 실제 메시지 발송 전에 Symfony Message 인스턴스에 접근하여 커스터마이징할 수 있도록 커스텀 콜백을 등록할 수 있습니다. 이를 위해, `Envelope` 정의 시 `using` 파라미터를 전달합니다.

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
## 마크다운(Markdown) 메일러블

마크다운 메일러블 메시지를 사용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)의 사전에 만들어진 템플릿와 컴포넌트를 메일러블에서도 그대로 활용할 수 있습니다. 메시지가 마크다운으로 작성되기 때문에, 라라벨이 아름답고 반응형인 HTML 템플릿을 자동으로 렌더링하며, 동시에 일반 텍스트 버전도 생성해 줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

마크다운 템플릿이 포함된 메일러블을 만들려면, `make:mail` 아티즌 명령어의 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그 다음, 메일러블의 `content` 메서드에서 `Content` 정의 시 `view` 대신 `markdown` 파라미터를 사용하면 됩니다.

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
### 마크다운 메시지 작성하기

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 조합해서 사용합니다. 이를 통해 라라벨이 제공하는 다양한 이메일 UI 컴포넌트를 활용하면서 손쉽게 메일 메시지를 구성할 수 있습니다.

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
> 마크다운 이메일을 쓸 때는 불필요하게 들여쓰기를 많이 하지 마세요. Markdown 표준상, 들여쓰기가 많은 줄은 코드 블록으로 자동 해석될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적으로 `color`라는 두 가지 매개변수를 받을 수 있습니다. 사용 가능한 색상은 `primary`, `success`, `error`입니다. 한 메시지에 여러 개의 버튼 컴포넌트를 추가해도 괜찮습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정된 텍스트 블록을 일반 메시지 내용과 대비되는 배경색이 적용된 패널로 표시합니다. 이를 통해 특정 내용을 더욱 돋보이게 만들 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 표를 HTML 테이블로 변환해줍니다. 컴포넌트에는 마크다운 표를 콘텐츠로 전달하면 되며, 기본적인 마크다운 표 정렬 문법도 그대로 사용할 수 있습니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈하기

마크다운 메일 컴포넌트 전체를 직접 내 애플리케이션으로 내보내고 원하는 대로 수정할 수 있습니다. 컴포넌트를 내보내려면 `vendor:publish` 아티즌 명령어로 `laravel-mail` 에셋 태그를 게시하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 마크다운 메일 컴포넌트들이 `resources/views/vendor/mail` 디렉터리에 복사됩니다. 이 `mail` 디렉토리에는 각각의 컴포넌트별로 `html`과 `text` 폴더가 들어 있습니다. 원하는 대로 컴포넌트를 수정해서 사용할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보낸 후, `resources/views/vendor/mail/html/themes` 폴더 안에 `default.css` 파일이 생성됩니다. 이 파일의 CSS를 수정하면, 마크다운 메일 메시지의 HTML에 자동으로 인라인 CSS가 변환되어 적용됩니다.

라라벨의 마크다운 컴포넌트용으로 아예 새로운 테마를 만들고 싶다면, `html/themes` 폴더에 CSS 파일을 추가하면 됩니다. 새 CSS 파일의 이름을 지정한 뒤 저장하고, 애플리케이션의 `config/mail.php` 설정파일에서 `theme` 옵션을 새 테마 이름으로 변경하세요.

특정 메일러블에만 별도의 테마를 적용하고 싶을 때는, 메일러블 클래스의 `$theme` 속성에 사용할 테마 이름을 설정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송

메일을 보내려면, [Mail 파사드](/docs/12.x/facades)의 `to` 메서드를 사용하세요. `to`는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체나 컬렉션을 전달하면, 라라벨은 자동으로 각 객체의 `email`과 `name` 속성을 찾아 수신자를 결정하므로, 이 속성이 반드시 객체에 포함되어 있어야 합니다. 수신자를 지정한 후, `send` 메서드에 메일러블 클래스 인스턴스를 전달하면 됩니다.

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

메일을 보낼 때 단순히 "to" 수신자만 지정하는 것에 그치지 않고, "to", "cc", "bcc" 모두 원하는 대로 지정할 수 있습니다. 각 메서드를 체이닝하여 사용하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자에게 반복 발송

여러 수신자(또는 이메일 주소)에게 반복적으로 메일러블을 보내야 할 때, `to` 메서드는 각 반복에서 수신자 목록에 이메일을 계속 추가합니다. 그래서 루프마다 매번 이전 수신자까지 모든 이들에게 이메일이 발송되는 문제가 생길 수 있습니다. 이를 방지하려면, 반드시 각 수신자마다 새로운 메일러블 인스턴스를 생성해서 보내야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 이용해 메일 발송

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에서 `default`로 지정된 메일러를 사용해 이메일을 보냅니다. 하지만 `mailer` 메서드를 사용하면 특정 메일러 설정을 적용해 메시지를 보낼 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 발송은 애플리케이션의 응답 속도를 늦출 수 있기 때문에, 많은 개발자들이 이메일 발송을 백그라운드 작업으로 큐에 넣어 처리합니다. 라라벨에서는 [통합 큐 API](/docs/12.x/queues)를 통해 간편하게 메일 메시지를 큐에 등록할 수 있습니다. 수신자를 지정한 후, `Mail` 파사드의 `queue` 메서드를 사용하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 메시지가 백그라운드에서 발송될 수 있도록 자동으로 작업을 큐에 넣어줍니다. 큐 기능을 사용하려면 [큐 설정](/docs/12.x/queues)을 먼저 완료해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 발송(큐잉) 메시지

큐에 등록된 이메일 메시지의 발송을 일정 시간 뒤로 미루고 싶을 때는, `later` 메서드를 사용하세요. `later`의 첫 번째 인자로는 이메일을 발송할 시점을 나타내는 `DateTime` 객체를 전달해야 합니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/연결에 할당하기

`make:mail` 명령어로 생성한 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 포함하므로, 모든 메일러블 인스턴스에서 `onQueue`, `onConnection` 메서드를 호출해 사용할 연결(connection)이나 큐(queue) 이름을 지정할 수 있습니다.

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

항상 큐잉 방식으로 처리하고 싶은 메일러블 클래스가 있다면, 해당 클래스에 `ShouldQueue` 계약(Contract)을 구현하면 됩니다. 이제 `send` 메서드로 발송을 요청해도, 해당 메일러블이 계약을 구현하고 있으니 자동으로 큐에 등록됩니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션이 커밋되기 전에 큐에서 작업이 처리될 수도 있습니다. 이때, 해당 트랜잭션에서 변경된 모델이나 레코드가 아직 데이터베이스에 반영되지 않아 작업이 올바로 처리되지 않을 수 있습니다. 트랜잭션 안에서 모델이 생성되었으나 실제로 DB에 없는 경우도 마찬가지입니다. 이렇게 큐 작업에서 모델이 필요한 상황에서는 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정값이 `false`라면, 특정 큐잉 메일러블만 트랜잭션이 전부 커밋된 이후에 디스패치되도록 `afterCommit` 메서드를 호출해 지정할 수 있습니다.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 메일러블의 생성자 안에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
> 이 문제를 우회하는 더 자세한 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 실패 처리

큐잉된 이메일 전송이 실패하면, 해당 메일러블 클래스에서 `failed` 메서드를 정의해 두었다면 자동으로 호출됩니다. 이때, 실패의 원인이 된 `Throwable` 인스턴스가 `failed` 메서드의 인자로 전달됩니다.

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
## 메일러블 렌더링

메일러블의 HTML 콘텐츠만 반환하고, 실제로 발송하지 않고자 할 때가 있을 수 있습니다. 이럴 때는 메일러블 인스턴스의 `render` 메서드를 호출하면 해당 메일러블의 평가된 HTML 내용을 문자열로 돌려줍니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블의 템플릿을 디자인할 때, Blade 템플릿처럼 미리보기를 빠르게 하고 싶을 수 있습니다. 그래서 라라벨은 라우트 클로저나 컨트롤러에서 아무 메일러블을 직접 반환할 수 있도록 해줍니다. 이렇게 반환하면, 해당 메일러블의 템플릿이 HTML로 렌더링되어 브라우저에서 바로 미리볼 수 있습니다. 실제 이메일 주소로 발송하지 않아도 디자인을 빠르게 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 다국어 지원

라라벨은 메일러블을 현재 요청의 로케일과는 다른 언어(로케일)로 보낼 수 있으며, 이 메일을 큐에 등록해도 로케일이 기억됩니다.

이 기능을 사용하려면, `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정하세요. 이메일 템플릿이 평가되는 동안 지정한 로케일로 전환되어 처리된 후, 작업이 끝나면 이전 로케일로 원복됩니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자별 선호 로케일

애플리케이션에서 각 사용자의 선호 언어(로케일)를 저장하는 경우가 종종 있습니다. 이런 경우, 한 모델에 `HasLocalePreference` 계약을 구현해두면, 라라벨이 이메일을 보낼 때 자동으로 해당 사용자의 선호 로케일을 사용하게 할 수 있습니다.

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

이 인터페이스를 구현하면, 라라벨은 해당 모델로 메일러블이나 알림을 보낼 때 자동으로 선호 로케일을 사용합니다. 따라서 `locale` 메서드를 별도로 호출할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>

## 테스트

<a name="testing-mailable-content"></a>
### 메일러블(Mailable) 콘텐츠 테스트

라라벨은 메일러블의 구조를 검사할 수 있는 다양한 메서드를 제공합니다. 또한 메일러블이 기대하는 내용을 실제로 포함하고 있는지 테스트할 수 있는 여러 편리한 메서드도 제공합니다. 주요 메서드는 다음과 같습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk`.

예상할 수 있듯, "HTML" 관련 assertion은 메일러블의 HTML 버전에 특정 문자열이 포함되어 있는지 확인하고, "text" assertion은 순수 텍스트 버전에 해당 문자열이 포함되어 있는지 검사합니다.

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

메일러블의 내용 테스트는, 실제로 특정 사용자에게 메일러블이 "발송"되었는지를 검증하는 테스트와는 별도로 진행하는 것을 권장합니다. 보통은 메일러블의 내용이 테스트하려는 코드와 직접적인 관련이 없기 때문에, 라라벨이 해당 메일러블을 발송하도록 지시받았는지만 확인하면 충분합니다.

메일 발송을 실제로 하지 않도록 하려면 `Mail` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Mail::fake()` 호출 후, 메일러블이 실제 사용자를 대상으로 발송되도록 지시되었는지, 그리고 메일러블이 받은 데이터를 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 발송 로직 실행...

    // 어떤 메일러블도 발송되지 않았는지 확인...
    Mail::assertNothingSent();

    // 메일러블이 발송되었는지 확인...
    Mail::assertSent(OrderShipped::class);

    // 메일러블이 두 번 발송되었는지 확인...
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일 주소로 메일러블이 발송되었는지 확인...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 여러 이메일 주소로 메일러블이 발송되었는지 확인...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 메일러블이 발송되지 않았는지 확인...
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3개의 메일러블이 발송되었는지 확인...
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

        // 주문 발송 로직 실행...

        // 어떤 메일러블도 발송되지 않았는지 확인...
        Mail::assertNothingSent();

        // 메일러블이 발송되었는지 확인...
        Mail::assertSent(OrderShipped::class);

        // 메일러블이 두 번 발송되었는지 확인...
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 이메일 주소로 메일러블이 발송되었는지 확인...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // 여러 이메일 주소로 메일러블이 발송되었는지 확인...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // 메일러블이 발송되지 않았는지 확인...
        Mail::assertNotSent(AnotherMailable::class);

        // 총 3개의 메일러블이 발송되었는지 확인...
        Mail::assertSentCount(3);
    }
}
```

만약 메일러블을 백그라운드에서 큐잉하여 발송한다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등의 메서드에는 클로저를 전달할 수 있습니다. 이 클로저를 통해 주어진 "진위 테스트"를 통과하는 메일러블이 실제로 발송되었는지 검증할 수 있습니다. 하나 이상의 메일러블이 해당 조건을 만족하면 assertion이 통과합니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 assertion 메서드에 전달된 클로저의 메일러블 인스턴스에서는 메일러블을 좀 더 세밀하게 검사할 수 있는 다양한 메서드를 사용할 수 있습니다.

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

메일러블 인스턴스는 첨부 파일을 검사할 수 있는 편리한 메서드도 제공합니다.

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

메일이 발송되지 않았음을 검증하는 메서드는 `assertNotSent`와 `assertNotQueued`가 있습니다. 때로는 발송도, 큐잉도 전혀 이루어지지 않았음을 검증하고 싶을 수도 있습니다. 이럴 때는 `assertNothingOutgoing`과 `assertNotOutgoing` 메서드를 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

이메일을 발송하는 애플리케이션을 개발할 때 실제로 실사용 이메일 주소로 메일이 전송되기를 원하지 않을 것입니다. 라라벨은 로컬 개발 환경에서 메일이 실제 전송되지 않도록 하는 여러 가지 방법을 제공합니다.

<a name="log-driver"></a>
#### Log 드라이버

이메일을 실제로 발송하는 대신, `log` 메일 드라이버를 사용하면 모든 이메일 메시지가 로그 파일에 기록되어 직접 내용을 확인할 수 있습니다. 이 드라이버는 주로 로컬 개발 환경에서 사용합니다. 환경별 애플리케이션 설정 방법에 대해서는 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는, [HELO](https://usehelo.com) 또는 [Mailtrap](https://mailtrap.io)과 같은 서비스를 `smtp` 드라이버와 함께 사용할 수 있습니다. 이 방식은 이메일 메시지가 실제로 발송되는 대신 "더미" 우편함으로 보내지기 때문에, 실제 이메일 클라이언트에서 메일을 확인할 수 있습니다. 특히 Mailtrap의 메시지 뷰어에서 최종 이메일을 직접 확인하는 것이 가능하여, 테스트에 유용합니다.

[라라벨 Sail](/docs/12.x/sail)을 사용 중이라면, [Mailpit](https://github.com/axllent/mailpit)으로 메시지를 미리 볼 수 있습니다. Sail이 실행 중일 때는 `http://localhost:8025` 주소에서 Mailpit 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 이용하여 모든 이메일의 수신자를 전역적으로 지정할 수 있습니다. 보통 이 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출합니다.

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

라라벨은 메일 메시지가 발송되는 동안 두 가지 이벤트를 디스패치합니다. `MessageSending` 이벤트는 메시지가 실제로 발송되기 *전*에 발생하고, `MessageSent` 이벤트는 메시지 발송이 *완료된 후* 발생합니다. 참고로, 이 이벤트들은 *큐잉* 시점이 아니라 실제 발송 시점에 발생한다는 점을 기억하세요. 애플리케이션 내에서 이 이벤트들을 위한 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다.

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
## 커스텀 트랜스포트(전송 방식) 만들기

라라벨은 여러 유형의 메일 트랜스포트를 내장하고 있지만, 라라벨에서 기본으로 지원하지 않는 다른 서비스로 이메일을 전송하고 싶을 때는 직접 트랜스포트 클래스를 작성할 수 있습니다. 시작하려면, `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 확장(extends)하는 새 클래스를 정의하세요. 그런 다음, `doSend`와 `__toString()` 메서드를 구현해야 합니다.

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

커스텀 트랜스포트를 정의했다면, `Mail` 파사드의 `extend` 메서드를 통해 이를 등록할 수 있습니다. 보통 이 작업은 애플리케이션의 `AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 수행합니다. `extend` 메서드에 넘기는 클로저에는 `$config` 인자가 전달되는데, 이는 애플리케이션 `config/mail.php` 파일의 해당 메일러에 대한 설정 배열입니다.

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

커스텀 트랜스포트 등록이 끝났다면, 애플리케이션의 `config/mail.php` 설정 파일에서 해당 트랜스포트를 사용하는 메일러 정의를 추가할 수 있습니다.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트 지원

라라벨은 Mailgun, Postmark 등 일부 Symfony에서 관리하는 메일 트랜스포트에 대한 내장 지원을 제공합니다. 그러나 이외에도 Symfony에서 공식적으로 관리하는 다른 트랜스포트를 라라벨에서 사용하려면 Composer로 필요한 Symfony 메일러 패키지를 설치하고, 라라벨에 직접 등록할 수 있습니다. 예를 들어, "Brevo"(이전 이름: Sendinblue) Symfony 메일러를 설치하고 등록하는 방법은 다음과 같습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지를 설치했으면, 애플리케이션의 `services` 설정 파일에 Brevo API 자격 증명을 등록합니다.

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

다음으로, `Mail` 파사드의 `extend` 메서드를 사용하여 라라벨에 트랜스포트를 등록할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 실행합니다.

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

트랜스포트 등록을 마쳤으면, 애플리케이션의 `config/mail.php` 설정 파일에서 해당 트랜스포트를 사용하는 메일러 정의를 추가합니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```