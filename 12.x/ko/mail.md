# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 전제 조건](#driver-prerequisites)
    - [장애 조치(Failover) 설정](#failover-configuration)
    - [라운드 로빈(Round Robin) 설정](#round-robin-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [발신자 설정하기](#configuring-the-sender)
    - [뷰 설정하기](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부](#inline-attachments)
    - [첨부 가능 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징하기](#customizing-the-symfony-message)
- [마크다운 메일러블 (Markdown Mailables)](#markdown-mailables)
    - [마크다운 메일러블 생성하기](#generating-markdown-mailables)
    - [마크다운 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 전송하기](#sending-mail)
    - [메일 큐잉하기](#queueing-mail)
- [메일러블 렌더링하기](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 로컬라이징하기](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 콘텐츠 테스트하기](#testing-mailable-content)
    - [메일러블 전송 테스트하기](#testing-mailable-sending)
- [메일과 로컬 개발](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가적인 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 꼭 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트 기반의 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 이메일 전송을 위한 드라이버를 제공하며, 이를 통해 로컬 또는 클라우드 기반 서비스 중 원하는 서비스를 손쉽게 선택하여 이메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내에서 설정된 각 메일러는 고유한 설정과 심지어 고유한 "트랜스포트(transport)"를 가질 수 있어, 애플리케이션 내에서 특정 이메일 메시지에 대해 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭션 이메일 전송에는 Postmark를, 대량 메일 발송에는 Amazon SES를 사용하는 식입니다.

`mail` 설정 파일에서 `mailers` 구성 배열을 확인할 수 있습니다. 이 배열은 Laravel이 지원하는 주요 메일 드라이버/트랜스포트별 기본 샘플 설정을 포함하며, `default` 설정 값은 애플리케이션이 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 전제 조건

Mailgun, Postmark, Resend, MailerSend 같은 API 기반 드라이버는 SMTP 서버를 통한 전송보다 간단하고 빠른 경우가 많습니다. 가능하다면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

이후 애플리케이션의 `config/mail.php` 설정 파일에서 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

다음으로, `mailers` 배열에 다음 구성을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이후 `config/services.php` 설정 파일에 다음 옵션들을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 외의 Mailgun 지역을 사용하는 경우, `services` 설정 파일에서 해당 지역에 맞는 엔드포인트를 정의할 수 있습니다:

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

`config/mail.php`에서 기본 메일러를 `postmark`로 설정합니다. 그리고 `config/services.php`에 다음 옵션을 포함시킵니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 Postmark 메시지 스트림을 지정하려면 `config/mail.php`에서 해당 메일러 설정 배열에 `message_stream_id` 옵션을 추가하세요:

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

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer로 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

`config/mail.php`에서 기본 메일러를 `resend`로 설정하고, `config/services.php`에 아래 옵션을 추가하세요:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 우선 Amazon AWS SDK for PHP를 설치해야 합니다. Composer 패키지 매니저를 통해 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

`config/mail.php`에서 기본 메일러를 `ses`로 설정하고, `config/services.php`에 다음 내용을 설정하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면 다음과 같이 `token` 키를 SES 설정에 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메일 메시지의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 반환할 수 있습니다:

```php
/**
 * 메세지 헤더를 가져옵니다.
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

AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, `ses` 설정 배열에 `options`를 추가하세요:

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

트랜잭셔널 이메일 및 SMS 서비스인 [MailerSend](https://www.mailersend.com/)는 Laravel 전용 API 기반 메일러 드라이버를 제공합니다. 이 패키지는 Composer로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

설치 후, 애플리케이션 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가합니다. 또한 `MAIL_MAILER` 환경 변수는 `mailersend`로 설정되어야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php`의 `mailers` 배열에 MailerSend 설정을 추가합니다:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

호스팅 템플릿 사용법 등 자세한 내용은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 확인하세요.

<a name="failover-configuration"></a>
### 장애 조치(Failover) 설정

때때로 메일 전송에 사용 중인 외부 서비스가 다운될 수 있습니다. 이럴 때, 주 메일 전송 드라이버가 실패하면 사용할 하나 이상의 백업 메일러 구성을 정의하는 것이 유용합니다.

이를 위해서는, 애플리케이션의 `mail` 설정 파일 내에 `failover` 트랜스포트를 사용하는 메일러를 정의해야 합니다. 이 `failover` 메일러 설정 배열에는 선택할 메일러 순서를 지정하는 `mailers` 배열이 포함되어야 합니다:

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

장애 조치 메일러를 정의했으면, 애플리케이션의 `mail` 설정 파일에서 `default` 키의 값으로 이 메일러 이름을 지정해 기본 메일러로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(Round Robin) 설정

`roundrobin` 트랜스포트는 여러 메일러에 메일 전송 작업을 분산할 수 있게 합니다. 이를 위해, 애플리케이션의 `mail` 설정 파일 내에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의하세요. 이 메일러 설정 배열에 포함된 `mailers` 배열에 분산할 메일러 목록을 적습니다:

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

라운드 로빈 메일러를 정의한 다음, `default` 구성 키에 이름을 지정하여 기본 메일러로 설정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 구성된 메일러 목록에서 무작위로 하나를 선택하고, 이후 각 이메일마다 다음 메일러로 순회하며 전송합니다. `failover` 트랜스포트가 *고가용성(high availability)* 달성을 목표로 하는 반면, `roundrobin` 트랜스포트는 *부하분산(load balancing)* 기능을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기

Laravel 애플리케이션 개발 시, 전송하는 이메일 유형별로 메일러블(mailable) 클래스를 만듭니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 아직 없다면 `make:mail` Artisan 명령어로 첫 번째 메일러블 클래스를 생성할 때 자동으로 생성됩니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기

메일러블 클래스를 생성했으면 열어보며 내부 구성을 살펴봅시다. 메일러블 클래스 구성은 주로 `envelope`, `content`, `attachments` 메서드에서 이루어집니다.

- `envelope` 메서드는 메일 제목(subject)과 때로는 수신자(recipient)를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다.
- `content` 메서드는 메시지 내용을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정하기

<a name="using-the-envelope"></a>
#### Envelope 사용하기

메일 발신자 설정, 즉 이메일이 누구로부터 왔는지 설정하는 두 가지 방법이 있습니다. 먼저, 메시지의 Envelope에서 "from" 주소를 직접 지정할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지의 envelope을 반환합니다.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

필요하다면 `replyTo` 주소도 지정할 수 있습니다:

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

만약 애플리케이션에서 모든 이메일에 같은 "from" 주소를 쓴다면, 각 메일러블 클래스마다 이를 지정하기 번거롭습니다. 이 때는 `config/mail.php` 설정 파일에서 전역 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 별도 "from" 주소를 지정하지 않으면 이 주소가 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한 전역 "reply_to" 주소도 `config/mail.php`에 정의할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정하기

메일러블 클래스의 `content` 메서드에서는 이메일 본문을 렌더링할 `view` 또는 템플릿을 지정할 수 있습니다. 일반적으로 이메일 본문은 [Blade 템플릿](/docs/12.x/blade)을 사용해 작성하므로, Blade 템플릿 엔진의 강력하고 편리한 기능을 활용할 수 있습니다:

```php
/**
 * 메시지 콘텐츠 정의를 반환합니다.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> [!NOTE]
> 이메일 템플릿을 `resources/views/mail` 디렉토리에 모아두는 것이 좋지만, `resources/views` 내 원하는 위치에 자유롭게 배치할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 플레인 텍스트(일반 텍스트) 버전을 정의하려면, `Content` 정의에 `text` 파라미터로 플레인 텍스트용 템플릿을 지정할 수 있습니다. HTML과 플레인 텍스트 버전을 모두 정의할 수 있습니다:

```php
/**
 * 메시지 콘텐츠 정의를 반환합니다.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```

명시적 대체 명칭으로 `html` 파라미터에 `view` 파라미터를 대신 사용할 수도 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 속성을 통한 데이터 전달

일반적으로 메일의 HTML을 렌더링할 때 사용할 데이터를 뷰에 전달해야 합니다. 이 데이터 전달 방법은 두 가지가 있습니다. 첫 번째는, 메일러블 클래스 내에 정의된 모든 public 속성은 자동으로 뷰에 전달됩니다. 따라서 예를 들어, 데이터를 생성자 인수로 받아 public 속성에 할당하면 됩니다:

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
     * 새 메시지 인스턴스를 생성합니다.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * 메시지 콘텐츠 정의를 반환합니다.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

public 속성에 데이터가 설정되면 뷰에서 해당 데이터를 바로 사용할 수 있습니다. Blade 템플릿에서 아래처럼 접근합니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 데이터 전달

이메일에 전달할 데이터를 템플릿에 넘기기 전 가공하려면 `Content` 정의의 `with` 파라미터를 활용할 수 있습니다. 이 경우 생성자에서 전달받은 데이터는 `protected` 또는 `private` 속성에 할당해 자동으로 뷰에 전달되지 않도록 하고, `content` 메서드 내에서 가공된 데이터를 `with` 배열로 넘기세요:

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
     * 새 메시지 인스턴스를 생성합니다.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * 메시지 콘텐츠 정의를 반환합니다.
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

`with` 배열을 통해 뷰에 전달된 데이터는 Blade 템플릿에서 아래와 같이 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면 메시지의 `attachments` 메서드가 반환하는 배열에 첨부파일을 추가하세요. 가장 간단한 방법은 `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 지정하는 것입니다:

```php
use Illuminate\Mail\Mailables\Attachment;

/**
 * 메시지의 첨부파일들을 반환합니다.
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

첨부 시 파일명이나 MIME 타입을 지정할 수도 있습니다. `as` 메서드로 표시명, `withMime` 메서드로 MIME 타입을 지정하세요:

```php
/**
 * 메시지의 첨부파일들을 반환합니다.
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
#### 디스크 저장소에서 파일 첨부하기

[파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 파일이라면 `fromStorage` 메서드로 첨부할 수 있습니다:

```php
/**
 * 메시지의 첨부파일들을 반환합니다.
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

물론 파일명과 MIME 타입은 다음과 같이 지정할 수 있습니다:

```php
/**
 * 메시지의 첨부파일들을 반환합니다.
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

기본 디스크 외 다른 디스크에서 파일을 첨부하려면 `fromStorageDisk` 메서드를 사용하세요:

```php
/**
 * 메시지의 첨부파일들을 반환합니다.
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
#### 원시 데이터(raw data) 첨부파일

메모리 내 생성한 PDF 같은 원시 데이터 바이트 배열을 디스크에 기록하지 않고 첨부하려면 `fromData` 메서드를 사용하세요. 이 메서드는 원시 데이터를 반환하는 클로저와 첨부파일 이름을 인수로 받습니다:

```php
/**
 * 메시지의 첨부파일들을 반환합니다.
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
### 인라인 첨부

이메일 본문에 이미지를 인라인으로 삽입하는 작업은 보통 번거롭지만, Laravel은 `embed` 메서드로 이를 간편하게 할 수 있습니다. 이메일 템플릿 내에서 `$message` 변수를 사용해 이미지 경로를 전달하세요. Laravel은 이메일 템플릿 내 전역으로 `$message` 변수를 제공합니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 플레인 텍스트 이메일 템플릿에서는 사용할 수 없습니다. 플레인 텍스트 메시지는 인라인 첨부 기능을 쓰지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 인라인 첨부

이미 원시 이미지 데이터 문자열이 있다면, `$message` 변수의 `embedData` 메서드를 호출해 이메일에 인라인 삽입할 수 있습니다. 이 때, 첨부할 이미지 파일명을 함께 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능 객체(Attachable Objects)

단순한 파일 경로 문자열 이외에, 종종 애플리케이션 내에 첨부하려는 대상이 클래스 형식으로 되어있기도 합니다. 예를 들어, 사진을 이메일에 첨부한다면 해당 사진을 나타내는 `Photo` 모델이 있을 수 있습니다. 이 경우 `Photo` 모델 자체를 `attach` 메서드에 직접 전달할 수 있다면 편리하지 않을까요? 첨부 가능 객체 스펙이 바로 이를 지원합니다.

먼저, 첨부 가능 객체가 될 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하고, `toMailAttachment` 메서드에서 `Illuminate\Mail\Attachment` 인스턴스를 반환하도록 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 메일 첨부 가능 표현을 반환합니다.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

정의한 첨부 가능 객체는 메일빌더에 있는 `attachments` 메서드에서 이렇게 반환해서 첨부할 수 있습니다:

```php
/**
 * 메시지의 첨부파일들을 반환합니다.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

첨부할 데이터가 Amazon S3 같은 원격 파일 저장소에 있다면, Laravel은 다음처럼 파일 시스템 디스크 경로에서 첨부 인스턴스를 생성할 수도 있습니다:

```php
// 기본 디스크에서 첨부 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 첨부 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한 메모리에 저장된 데이터로 첨부 인스턴스를 생성하려면 `fromData` 메서드에 클로저를 전달하세요. 클로저에서 첨부할 원시 데이터를 반환해야 합니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일 이름이나 MIME 타입을 변경하려면 `as`와 `withMime` 메서드를 사용하세요:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

추가로 메일에 커스텀 헤더를 붙여야 할 경우가 있습니다. 예를 들어 커스텀 `Message-Id` 헤더나 기타 임의 텍스트 헤더를 넣어야 할 때가 그렇습니다.

이럴 때는 메일러블 클래스에 `headers` 메서드를 정의하고, `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하세요. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받을 수 있습니다. 필요한 것만 지정하면 됩니다:

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
### 태그와 메타데이터

Mailgun, Postmark 같은 서드파티 이메일 공급자들은 메일에 "태그(tags)"와 "메타데이터(metadata)"를 첨부할 수 있습니다. 이를 통해 애플리케이션에서 보낸 메일을 그룹화하거나 추적할 수 있죠. Laravel은 `Envelope` 정의를 통해 태그와 메타데이터를 설정할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지의 envelope을 반환합니다.
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

Mailgun 드라이버를 사용하는 경우 [Mailgun 태그 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)를 참고하세요.

Postmark 사용 시에도 각각 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원 사항이 있습니다.

Amazon SES를 사용하는 경우, [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)는 `metadata` 메서드를 통해 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel 메일 기능은 Symfony Mailer 기반입니다. 메일이 전송되기 전에 Symfony Message 인스턴스에 커스텀 콜백을 등록해 메시지를 깊이 있게 조작할 수 있습니다. 이를 위해 `Envelope` 정의에 `using` 파라미터로 콜백 배열을 지정하세요:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지의 envelope을 반환합니다.
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

마크다운 메일러블을 사용하면, Laravel [메일 알림](/docs/12.x/notifications#mail-notifications)에서 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있습니다. 메일 내용은 마크다운으로 작성하며, Laravel은 이들을 아름답고 반응형 HTML 템플릿으로 렌더링하면서 자동으로 대응하는 플레인 텍스트 버전도 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

Markdown 템플릿을 함께 생성하려면 `make:mail` Artisan 명령어에 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

메일러블의 `content` 메서드 내에선 `view` 대신 `markdown` 파라미터를 사용해 콘텐츠 정의를 지정합니다:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지 콘텐츠 정의를 반환합니다.
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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 조합하여 쉽게 메일 메시지를 작성하면서 Laravel의 선제작 이메일 UI 컴포넌트를 활용할 수 있습니다:

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
> 마크다운 이메일 작성 시에는 들여쓰기를 과도하게 하지 마세요. 마크다운 규칙에 따라 들여쓴 내용은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더합니다. `url`과 선택 가능한 `color` 인수를 받으며, 지원하는 색상은 `primary`, `success`, `error`입니다. 메시지 내에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 메시지 내에서 배경색이 살짝 다른 패널 영역에 텍스트 블록을 보여 줍니다. 특정 문구나 블록에 시선을 집중시킬 때 유용합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 형식의 테이블을 HTML 테이블로 변환합니다. 컴포넌트 내용에 마크다운 테이블을 작성하며, 기본적인 마크다운 테이블 정렬 문법도 지원합니다:

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

모든 마크다운 메일 컴포넌트를 애플리케이션 내로 내보내어 커스터마이징할 수 있습니다. `vendor:publish` Artisan 명령어로 `laravel-mail` 태그를 퍼블리싱하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

퍼블리싱 후 `resources/views/vendor/mail` 디렉토리에 컴포넌트들이 생성됩니다. `html` 및 `text` 하위 디렉토리에 각각 HTML과 텍스트 버전 컴포넌트가 포함됩니다. 원하는 대로 편집할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

퍼블리싱 후 `resources/views/vendor/mail/html/themes` 디렉토리 내 `default.css` 파일이 있습니다. 이 파일의 CSS를 수정하면, 마크다운 메일의 HTML 렌더링 시 자동으로 인라인 CSS로 변환됩니다.

완전히 새 테마를 만들고 싶다면 이 `html/themes` 디렉토리에 CSS 파일을 추가하고, `config/mail.php`의 `theme` 옵션을 새 테마 이름으로 변경하면 됩니다.

특정 메일러블 클래스에서 테마를 개별적으로 지정하려면 클래스 내부의 `$theme` 속성에 테마 이름을 할당하세요.

<a name="sending-mail"></a>
## 메일 전송하기

메일을 보내려면 `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용하세요. `to` 메서드에는 이메일 주소, 사용자 객체, 또는 사용자 컬렉션을 전달할 수 있습니다. 객체나 컬렉션을 전달하면 해당 객체의 `email`과 `name` 속성을 자동으로 수신자 정보로 사용합니다. 수신자를 지정한 후에는 `send` 메서드에 메일러블 인스턴스를 전달하여 전송합니다:

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
     * 주문 배송 처리
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 처리 코드...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

단지 "to" 수신자만 지정하는 것이 아니라, `cc`, `bcc`도 체인으로 메서드를 연결해 지정할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

수신자 목록을 순회하며 하나씩 메일을 보내야 할 때가 있습니다. 그러나 `to` 메서드는 호출할 때마다 기존 수신자 목록에 추가하므로, 반복문 내에서 같은 메일러블 인스턴스를 쓰면 이전 수신자들에게 중복 전송됩니다. 따라서 수신자마다 항상 새 메일러블 인스턴스를 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 전송하기

기본적으로 Laravel은 `config/mail.php` 설정의 `default` 메일러를 사용해 이메일을 전송합니다. 특정 메일러 설정을 사용하려면 `mailer` 메서드를 사용하세요:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉하기

이메일 전송은 애플리케이션 응답 속도에 영향을 줄 수 있으므로, 메일을 큐에 쌓아 백그라운드로 전송하는 것이 좋습니다. Laravel은 내장된 [통합 큐 API](/docs/12.x/queues)를 제공해 이를 쉽게 만듭니다. 메일 수신자를 지정한 뒤 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 큐에 작업을 밀어 넣어 백그라운드 작업으로 메일을 보냅니다. 사용 전에는 [큐 설정](/docs/12.x/queues)을 반드시 완료해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 큐잉

큐에 쌓은 메일 전송을 지연시키려면 `later` 메서드를 사용하세요. 첫 번째 인수로 `DateTime` 인스턴스를 주어 전송시점을 지정합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 작업 푸시하기

`make:mail`로 생성된 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, 인스턴스에 `onQueue`, `onConnection` 메서드를 호출해 큐 연결 및 큐 이름을 지정할 수 있습니다:

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

항상 메일이 큐에 쌓여 전송되기를 원한다면 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이렇게 하면 `send` 메서드를 호출해도 항상 큐에 쌓여 처리됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 큐잉된 메일러블이 디스패치되면, 큐 작업 실행 시점에 트랜잭션이 아직 커밋되지 않아 DB 상태와 동기화되지 않을 수 있습니다. 이로 인해 모델이나 레코드가 유효하지 않거나 존재하지 않아서 에러가 발생할 수 있습니다.

`queue` 연결 설정의 `after_commit` 옵션이 `false`이면, 특정 메일러블에 대해 트랜잭션 커밋 후에 디스패치하도록 `afterCommit` 메서드를 호출할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자에서 호출할 수도 있습니다:

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
     * 새 메시지 인스턴스 생성자
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 큐 작업과 데이터베이스 트랜잭션 관련 이슈는 [큐 문서 내 해당 섹션](/docs/12.x/queues#jobs-and-database-transactions)을 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 실패 처리

큐에 쌓인 이메일이 실패하면, 실패 원인이 된 `Throwable` 인스턴스가 인수로 전달되는 `failed` 메서드가 정의되어 있으면 호출됩니다:

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
     * 큐잉된 이메일 실패 시 실행
     */
    public function failed(Throwable $exception): void
    {
        // 실패 처리 로직...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링하기

메일러블을 실제 전송하지 않고 HTML 내용을 얻고자 할 때가 있습니다. 이럴 땐 메일러블의 `render` 메서드를 호출하면, 메일러블 결과 HTML을 문자열로 반환받을 수 있습니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인할 때, 일반 Blade 뷰처럼 브라우저에서 바로 렌더링된 결과를 확인하는 것이 편리합니다. Laravel은 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 그대로 반환하면, 그 결과를 렌더링하여 브라우저에 표시합니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 로컬라이징하기

Laravel은 요청의 현재 로케일과 다른 언어로 메일러블을 보내는 것을 지원하며, 큐잉된 메일에서도 이 로케일을 기억합니다.

`Mail` 파사드의 `locale` 메서드를 사용해 원하는 언어를 지정할 수 있습니다. 메일러블 평가 시 해당 로케일로 전환되며, 평가가 끝나면 이전 로케일로 복귀합니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

사용자별 선호 언어를 저장하는 애플리케이션이라면, 모델에 `HasLocalePreference` 인터페이스를 구현하여 Laravel에 선호 로케일을 제공할 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자 선호 로케일 반환
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면 Laravel은 메일 및 알림 전송 시 자동으로 선호 로케일을 사용하므로, 추가로 `locale` 메서드를 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### 메일러블 콘텐츠 테스트하기

Laravel은 메일러블 구조 점검과, 기대한 콘텐츠가 포함되었는지 테스트할 수 있는 다양한 메서드를 제공합니다:

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

"HTML" 관련 어서션은 HTML 버전에서, "text" 관련 어서션은 플레인 텍스트 버전에서 해당 문자열 포함 여부를 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트하기

메일러블 콘텐츠 테스트와는 별도로, 특정 메일러블이 실제로 "전송" 명령을 받았는지 테스트하는 것이 좋습니다. 일반적으로 콘텐츠는 테스트 대상 코드와 관련 없으므로, Laravel이 해당 메일러블 전송을 명령받았는지 검증하는 것이 충분합니다.

`Mail` 파사드의 `fake` 메서드를 쓰면 실제 메일 전송을 막고 테스트할 수 있습니다. 이후엔 메일러블 전송 호출 여부와 대상, 전달된 데이터를 쉽게 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 배송 처리...

    // 메일 전송 요청이 없었는지 검증
    Mail::assertNothingSent();

    // 특정 메일러블이 전송되었는지 검증
    Mail::assertSent(OrderShipped::class);

    // 특정 메일러블이 두 번 전송되었는지 검증
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일 주소로 메일 전송되었는지 검증
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 여러 이메일 주소로 메일 전송되었는지 검증
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 다른 메일러블이 전송되지 않았는지 검증
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3건의 메일 전송 요청이 있었는지 검증
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

        // 주문 배송 처리...

        Mail::assertNothingSent();
        Mail::assertSent(OrderShipped::class);
        Mail::assertSent(OrderShipped::class, 2);
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);
        Mail::assertNotSent(AnotherMailable::class);
        Mail::assertSentCount(3);
    }
}
```

메일러블을 백그라운드 큐에 쌓아 처리한다면 `assertSent` 대신 `assertQueued` 메서드를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 클로저를 인수로 주어, 특정 조건(예: 특정 주문 ID일 때)으로 필터링할 수 있습니다. 조건에 맞는 메일러블이 하나라도 전송되거나 큐에 쌓이면 테스트는 성공합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

클로저 내부의 메일러블 인스턴스는 아래와 같은 메서드를 제공해 추가 검증할 수 있습니다:

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

첨부파일에 대해서도 검사 메서드가 있습니다:

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

메일이 전송되거나 큐에 쌓이지 않았음을 검증하는 메서드가 두 가지 있습니다. 모두를 검증하고 싶다면 `assertNothingOutgoing` 및 `assertNotOutgoing` 메서드를 쓰세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발

이메일을 전송하는 애플리케이션을 개발할 때, 실제 이메일 주소로 메일이 보내지지 않게 하고 싶을 수 있습니다. Laravel은 로컬 개발에서 실제 메일 전송을 "비활성화"하는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 이메일 메시지를 전송하는 대신 로그 파일에 모두 기록합니다. 보통 로컬 개발 환경에서만 사용합니다. 환경별 설정 관련 내용은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스를 이용하거나, Laravel Sail 사용자라면 [Mailpit](https://github.com/axllent/mailpit)을 실행해 실제 메일 전송 대신 더미 메일함으로 메일을 받아볼 수 있습니다. Mailpit UI는 기본적으로 `http://localhost:8025`에서 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 설정하기

마지막으로, 모든 메일이 특정 "to" 주소로 무조건 전송되게 하려면 `Mail` 파사드의 `alwaysTo` 메서드를 호출하세요. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 환경 체크 후 호출합니다:

```php
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 부트스트랩
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

Laravel은 이메일 전송 중 두 가지 이벤트를 방출합니다. 메일이 보내지기 전에는 `MessageSending` 이벤트가, 전송 후에는 `MessageSent` 이벤트가 발생합니다. 이 이벤트들은 "전송" 시점에서 발생하며, 큐에 쌓이는 시점이 아닙니다. 애플리케이션 내에서 이 이벤트들을 핸들링하려면 [이벤트 리스너](/docs/12.x/events)를 만들어 등록할 수 있습니다:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * 이벤트 처리
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## 커스텀 트랜스포트

Laravel은 여러 메일 트랜스포트를 내장하고 있지만, 필요 시 자체 트랜스포트를 만들어 Laravel에서 지원하지 않는 다른 서비스와 연동할 수 있습니다.

먼저 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 클래스를 만들고, `doSend`와 `__toString` 메서드를 구현하세요:

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
     * 새로운 Mailchimp 트랜스포트 인스턴스를 생성합니다.
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
     * 트랜스포트의 문자열 표현을 반환합니다.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

그리고 `AppServiceProvider` 등 서비스 프로바이더의 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드를 이용해 커스텀 트랜스포트를 등록하세요. 등록 콜백에 `$config` 배열을 전달받아 설정 정보를 사용할 수 있습니다:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * 애플리케이션 부트스트랩
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

트랜스포트 등록이 완료되면, `config/mail.php` 설정 파일에 다음과 같이 메일러 정의를 추가해 사용할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가적인 Symfony 트랜스포트

Laravel은 Mailgun, Postmark 같은 Symfony가 관리하는 메일 트랜스포트 일부를 기본 지원합니다. 더 많은 Symfony 트랜스포트를 추가로 지원하려면 필요한 Symfony 메일러를 Composer로 설치하고 Laravel에 등록하세요.

예를 들어 "Brevo"(이전 "Sendinblue") Symfony 메일러를 설치하고 등록하는 과정은 다음과 같습니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

`services` 설정 파일에 Brevo API 키를 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

서비스 프로바이더의 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드로 등록합니다:

```php
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * 애플리케이션 부트스트랩
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

등록 후 `config/mail.php`에 다음과 같은 메일러 정의를 추가하세요:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```