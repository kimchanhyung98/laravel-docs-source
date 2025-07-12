# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [장애 조치(페일오버) 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [메일러블 클래스 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [첨부 가능한 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 보내기](#sending-mail)
    - [메일 큐에 등록하기](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 다국어 지원](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일을 보내는 일은 복잡하지 않아도 됩니다. 라라벨은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깔끔하고 간단한 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 이메일 전송 드라이버를 제공하여, 여러분이 원하는 로컬 또는 클라우드 기반 메일 서비스로 손쉽게 메일을 보낼 수 있도록 지원합니다.

<a name="configuration"></a>
### 설정

라라벨의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에서 각각의 메일러는 서로 다른 고유한 설정과 “트랜스포트(전송 방식)”를 가질 수 있어서, 애플리케이션 내에서 특정 이메일 메시지를 보낼 때 각기 다른 메일 서비스를 사용할 수 있습니다. 예를 들어, 거래 관련 메일은 Postmark를 통해, 대량 메일은 Amazon SES로 전송하도록 나누어 설정할 수 있습니다.

`mail` 설정 파일 안에는 `mailers` 설정 배열이 있습니다. 이 배열에는 라라벨에서 지원하는 주요 메일 드라이버/트랜스포트 예제가 포함되어 있으며, `default` 설정 값은 애플리케이션에서 이메일을 보낼 때 기본적으로 사용될 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비사항

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 대체로 SMTP 서버를 통한 메일 전송보다 더 간단하고 빠른 작업이 가능합니다. 가능하다면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer 트랜스포트 패키지를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고, 아래의 설정 배열을 `mailers` 배열에 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

애플리케이션의 기본 메일러를 설정한 후, 다음 옵션을 `config/services.php` 설정 파일에 추가해야 합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 Mailgun 리전([Mailgun region](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions))을 사용하지 않는 경우, `services` 설정 파일에서 해당 리전의 엔드포인트를 직접 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 트랜스포트 패키지를 설치해야 합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 지정합니다. 이후, `config/services.php` 설정 파일에 아래와 같은 옵션이 포함되어 있는지 확인하십시오:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하려면, 메일러 설정 배열에 `message_stream_id` 설정을 추가할 수 있습니다. 이 설정은 `config/mail.php` 설정 파일에서 찾을 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 가지는 여러 Postmark 메일러도 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend의 PHP SDK를 설치해야 합니다:

```shell
composer require resend/resend-php
```

그런 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `resend`로 설정합니다. 이후, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하십시오:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 먼저 Amazon AWS SDK for PHP 라이브러리를 설치해야 합니다. 이 라이브러리는 Composer 패키지 매니저를 사용해서 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 설정 파일에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 설정 파일에 아래와 같은 옵션이 포함되어 있는지 확인하세요:

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

SES의 [구독 관리(subscription management)](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html) 기능을 사용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 추가할 수 있습니다:

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

라라벨이 이메일을 보낼 때 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, `ses` 설정에 `options` 배열을 추가하면 됩니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 메일과 SMS 서비스를 제공하며, 라라벨용 API 기반 메일 드라이버를 직접 관리합니다. 이 드라이버가 포함된 패키지는 Composer를 통해 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

패키지를 설치한 후, 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가해야 합니다. 또한 `MAIL_MAILER` 환경 변수는 `mailersend`로 지정해야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, 애플리케이션의 `config/mail.php` 설정 파일의 `mailers` 배열에 MailerSend를 추가합니다:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

호스팅된 템플릿 사용 방법 등 MailerSend에 대한 더 자세한 내용은 [MailerSend 드라이버 공식 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하시기 바랍니다.

<a name="failover-configuration"></a>
### 장애 조치(페일오버) 설정

외부 서비스를 통해 애플리케이션의 메일을 발송하도록 구성한 경우, 외부 서비스에 장애가 발생할 수 있습니다. 이런 상황을 대비해, 주 메일 전송 드라이버가 동작하지 않을 때 사용할 예비(백업) 메일 전송 설정을 지정하면 유용합니다.

이를 위해서는 `failover` 트랜스포트를 사용하는 메일러를 `mail` 설정 파일에 정의하면 됩니다. `failover` 메일러의 설정 배열에는 메일 발송 시 사용할 메일러의 우선순위를 지정하는 `mailers` 배열이 포함되어야 합니다:

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

페일오버 메일러를 정의한 후에는, 해당 메일러의 이름을 애플리케이션의 기본 메일러(`default` 설정 값)로 지정해야 합니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈 설정

`roundrobin` 트랜스포트를 사용하면 여러 메일러에 메일 발송 작업을 분산시킬 수 있습니다. 먼저, ` mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의합니다. 이때 설정 배열의 `mailers` 항목에는 사용할 메일러 목록을 지정합니다:

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

라운드 로빈 메일러를 정의한 후에는 `default` 설정 값에 이 메일러의 이름을 지정해야 합니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

`roundrobin` 트랜스포트는 설정된 메일러 목록 중 무작위로 하나를 선택하여 메일을 보낸 뒤, 이후 순차적으로 다음 메일러를 사용합니다. *[장애 복구(고가용성, high availability)](https://en.wikipedia.org/wiki/High_availability)*를 위해 사용하는 `failover`와 달리, `roundrobin` 트랜스포트는 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 기능을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 클래스 생성

라라벨 애플리케이션을 개발할 때, 애플리케이션에서 발송하는 각 이메일 유형은 "메일러블(mailable)" 클래스 하나로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 이 디렉터리가 현재 애플리케이션 내에 보이지 않더라도 걱정하지 마십시오. `make:mail` Artisan 명령어로 첫 메일러블 클래스를 생성하면 자동으로 디렉터리가 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성

메일러블 클래스를 생성했다면, 이제 클래스를 열고 그 구조를 살펴보겠습니다. 메일러블 클래스의 주요 설정은 `envelope`, `content`, `attachments` 등 다양한 메서드에서 이루어집니다.

`envelope` 메서드는 메시지의 제목(subject)과 때로는 수신자 등의 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope 사용하기

이메일의 발신자를 어떻게 설정하는지부터 살펴보겠습니다. 즉, 이메일이 누구로부터 오는지를 지정하는 방법입니다. 발신자를 지정하는 방법에는 두 가지가 있습니다. 첫 번째로, 메시지의 envelope에서 "from" 주소를 지정할 수 있습니다:

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
#### 전역 `from` 주소 사용

애플리케이션 전송 메일의 발신자 주소가 모두 동일한 경우, 매번 새로 생성하는 메일러블 클래스마다 일일이 추가하는 것이 번거로울 수 있습니다. 이럴 때는 `config/mail.php` 설정 파일에서 전역 "from" 주소를 지정할 수 있습니다. 메일러블 클래스 내에서 직접 "from" 주소를 별도로 지정하지 않는 한, 여기서 지정한 전역 "from" 주소가 적용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

추가로, 전역 "reply_to" 주소도 `config/mail.php` 파일에 정의할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드에서 메일 본문 내용을 렌더링할 때 사용할 `view`(즉, Blade 템플릿)를 지정할 수 있습니다. 대부분의 이메일은 [Blade 템플릿](/docs/12.x/blade)을 이용해 내용을 렌더링하므로, 이메일의 HTML을 구축할 때 Blade 템플릿 엔진의 모든 기능과 편리함을 사용할 수 있습니다:

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
> 모든 이메일 템플릿을 보관하기 위한 `resources/views/mail` 디렉터리를 별도로 만들어 관리하는 것을 추천하지만, 실제로는 `resources/views` 내에서 원하는 위치에 자유롭게 템플릿 파일을 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 따로 정의하고 싶다면, 메시지의 `Content` 정의 시 plain-text 템플릿도 지정할 수 있습니다. `view` 파라미터와 마찬가지로, `text` 파라미터에도 템플릿 이름을 지정하고 해당 템플릿이 이메일의 내용을 렌더링합니다. 따라서 HTML 버전과 일반 텍스트 버전 모두를 자유롭게 정의할 수 있습니다:

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

참고로, `html` 파라미터는 `view` 파라미터의 별칭처럼 사용할 수 있습니다:

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

이메일의 HTML을 렌더링할 때에서 사용할 데이터를 뷰에 전달하고자 할 때 보통 가장 많이 사용하는 방법은 public 속성을 통한 방식입니다. 메일러블 클래스에 정의된 모든 public 속성은 자동으로 뷰에서 사용할 수 있습니다. 예를 들어, 메일러블 클래스 생성자에서 받은 데이터를 클래스의 public 속성에 할당하면 아래와 같이 활용할 수 있습니다:

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

이렇게 public 속성에 데이터를 할당하면, 뷰에서 Blade 문법으로 바로 해당 데이터를 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

템플릿에 넘길 데이터의 형식을 직접 커스터마이즈하고 싶다면, `Content` 정의의 `with` 파라미터로 데이터를 명시적으로 뷰에 전달할 수 있습니다. 이 경우에도 생성자에서 데이터를 받아 사용하지만, 이 데이터는 public이 아닌 protected 혹은 private 속성에 저장해야 하며, 따라서 자동 노출되지 않습니다:

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

이렇게 `with` 파라미터로 데이터를 넘기면 뷰에서 해당 변수를 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드에서 반환하는 배열에 첨부 파일을 추가하면 됩니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달하면 첨부 파일을 추가할 수 있습니다:

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

첨부 파일을 추가할 때, 파일의 표시 이름이나 MIME 타입을 `as` 및 `withMime` 메서드로 지정할 수도 있습니다:

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
#### 디스크에서 파일 첨부하기

파일이 [파일 시스템 디스크](/docs/12.x/filesystem)에 저장되어 있다면, `fromStorage` 첨부 메서드를 사용해서 해당 파일을 메일에 첨부할 수 있습니다:

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

물론, 첨부 파일의 이름과 MIME 타입도 지정할 수 있습니다:

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

기본 디스크가 아닌 다른 스토리지 디스크를 사용할 경우에는 `fromStorageDisk` 메서드를 사용하면 됩니다:

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

#### Raw Data 첨부하기

`fromData` 첨부 메서드는 바이트 형태의 원시 문자열을 첨부 파일로 추가할 때 사용할 수 있습니다. 예를 들어, 메모리에서 PDF 파일을 생성하여 디스크에 저장하지 않고 바로 메일에 첨부하고 싶을 때 이 방법이 유용합니다. `fromData` 메서드는 첨부할 데이터 바이트를 리턴하는 클로저와 첨부 파일의 이름을 받습니다.

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
### 인라인 첨부 파일

이메일에 이미지를 인라인으로 삽입하는 것은 번거로운 작업일 수 있습니다. 하지만 라라벨은 이메일에 이미지를 첨부할 수 있는 편리한 방법을 제공합니다. 인라인 이미지를 삽입하려면 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하세요. 라라벨은 모든 이메일 템플릿에 `$message` 변수를 자동으로 전달해주므로, 직접 값을 넘겨줄 필요가 없습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 텍스트 전용 메시지(plain text message) 템플릿에서는 사용할 수 없습니다. 텍스트 메시지는 인라인 첨부 파일을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터로 첨부 파일 임베딩하기

이미 원시 이미지 데이터 문자열을 가지고 있고, 이를 이메일 템플릿에 임베드하고 싶다면 `$message` 변수의 `embedData` 메서드를 호출할 수 있습니다. `embedData`를 사용할 때는 임베드할 이미지에 지정할 파일 이름을 반드시 함께 전달해야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

파일 첨부를 단순 파일 경로 문자열로 처리하는 것도 좋지만, 실제로 애플리케이션 내 첨부 대상이 클래스(모델)로 존재할 때가 많습니다. 예를 들어, 사진을 메시지에 첨부한다고 할 때, 여러분의 애플리케이션에는 그 사진을 나타내는 `Photo` 모델이 있을 수 있습니다. 이런 경우라면, 그냥 `attach` 메서드에 `Photo` 모델 객체를 바로 넘기고 싶지 않으신가요? Attachable 객체를 사용하면 이렇게 할 수 있습니다.

시작하려면, 첨부할 오브젝트에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현합니다. 이 인터페이스는 `toMailAttachment` 메서드를 정의해야 하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

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

이제 attachable 객체를 정의했다면, 이메일 메시지를 만들 때 `attachments` 메서드에서 해당 객체 인스턴스를 반환할 수 있습니다.

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

물론, 첨부할 파일 데이터가 Amazon S3 같은 원격 파일저장소에 있을 수도 있습니다. 이런 경우를 위해, 라라벨은 애플리케이션의 [파일시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터로부터도 첨부 인스턴스를 생성할 수 있도록 지원합니다.

```php
// 기본 디스크에서 파일로 첨부 만들기...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일로 첨부 만들기...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 있는 데이터를 사용하여 첨부 인스턴스를 만들 수도 있습니다. 이 경우, `fromData` 메서드에 클로저를 전달하여 첨부할 원시 데이터를 반환하도록 하면 됩니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

라라벨은 첨부 파일을 커스터마이즈할 수 있는 다양한 추가 메서드를 제공합니다. 예를 들어, `as`와 `withMime` 메서드를 사용하면 파일의 이름이나 MIME 타입을 원하는 값으로 지정할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

경우에 따라 이메일 메시지에 추가 헤더를 붙여야 할 수도 있습니다. 예를 들어, 커스텀 `Message-Id`나 기타 임의의 텍스트 헤더를 추가해야 할 때가 있을 수 있습니다.

이럴 때는, mailable 클래스에 `headers` 메서드를 정의하세요. `headers` 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 합니다. 이 클래스는 `messageId`, `references`, `text` 매개변수를 받을 수 있으며, 필요한 것만 선택적으로 지정하면 됩니다.

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

Mailgun, Postmark 등 일부 서드파티 이메일 서비스에서는 메시지 "태그(tags)"와 "메타데이터(metadata)" 기능을 지원합니다. 이를 활용하면 애플리케이션에서 보낸 이메일을 그룹화하고 추적할 수 있습니다. 이메일에 태그와 메타데이터를 추가하려면, 여러분의 `Envelope` 정의에서 지정할 수 있습니다.

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

Mailgun 드라이버를 사용할 경우, [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 관한 자세한 내용은 Mailgun 공식 문서를 참고하세요. 또한 Postmark 서비스를 사용할 경우, [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)에 대한 Postmark 문서도 참고할 수 있습니다.

만약 애플리케이션에서 Amazon SES를 사용하여 이메일을 전송한다면, 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가하려면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이즈

라라벨의 메일 시스템은 Symfony Mailer를 기반으로 작동합니다. 라라벨에서는 메시지 전송 전, Symfony Message 인스턴스에 접근해 직접 커스텀 콜백을 등록할 수 있습니다. 이렇게 하면 메시지가 실제로 전송되기 전에 메시지를 세밀하게 수정할 수 있습니다. 이를 위해, `Envelope` 정의에 `using` 파라미터를 지정하면 됩니다.

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
## 마크다운 메일러블(Markdown Mailables)

마크다운 메일러블 메시지는 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 여러분의 메일러블에서 활용할 수 있게 해줍니다. 메일 메시지를 마크다운으로 작성하면, 라라벨이 아름답고 반응형인 HTML 템플릿을 자동으로 렌더링하는 것은 물론, 텍스트 버전(plain-text)도 함께 생성해 줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

마크다운 템플릿이 포함된 메일러블을 생성하려면 `make:mail` 아티즌 명령어에 `--markdown` 옵션을 사용할 수 있습니다.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그런 다음, 메일러블 클래스의 `content` 메서드에서 `Content` 정의를 할 때, `view` 파라미터 대신 `markdown` 파라미터를 사용합니다.

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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법의 조합으로 메시지를 쉽게 구성할 수 있도록 합니다. 이를 통해 라라벨이 제공하는 다양한 미리 만들어진 이메일 UI 컴포넌트를 활용할 수 있습니다.

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
> 마크다운 이메일을 작성할 때는 들여쓰기를 과도하게 사용하지 마세요. 마크다운 표준에 따라 과도한 들여쓰기는 코드 블록으로 렌더링될 수 있습니다.

<a name="button-component"></a>
#### Button 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`(필수)과 `color`(옵션)라는 두 개의 인수를 받습니다. 지원하는 색상은 `primary`, `success`, `error`입니다. 한 메일 메시지 안에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### Panel 컴포넌트

Panel 컴포넌트는 전달된 텍스트 블록을 기존 메시지와는 약간 다른 배경색의 패널에 표시합니다. 이를 통해 특정 텍스트 블록에 주목을 끌 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### Table 컴포넌트

Table 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환해줍니다. 이 컴포넌트는 마크다운 테이블을 컨텐츠로 받으며, 기본 마크다운 표 정렬 문법을 그대로 사용할 수 있습니다.

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

마크다운 메일 컴포넌트를 원하는 대로 수정하고 싶다면, 컴포넌트를 직접 애플리케이션으로 내보낼 수 있습니다. 컴포넌트를 내보내려면 `laravel-mail` 에셋 태그를 이용해 `vendor:publish` 아티즌 명령어를 실행하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 복사됩니다. `mail` 디렉터리는 각각 HTML, 텍스트 버전이 들어있는 `html`, `text` 폴더로 구성됩니다. 원하는 대로 자유롭게 컴포넌트를 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보낸 후, `resources/views/vendor/mail/html/themes` 디렉터리 안에 `default.css` 파일이 있습니다. 이 파일의 CSS를 커스터마이즈하면, 해당 스타일이 HTML용 마크다운 메일 메시지에 자동으로 인라인 CSS로 변환되어 적용됩니다.

라라벨 마크다운 컴포넌트에 완전히 새로운 테마를 만들고 싶은 경우, CSS 파일을 `html/themes` 디렉터리에 저장하면 됩니다. 파일명을 지정한 후, 애플리케이션의 `config/mail.php` 설정 파일의 `theme` 옵션을 새로운 테마 이름에 맞춰 업데이트하세요.

특정 메일러블에만 다른 테마를 적용하고 싶다면, 메일러블 클래스의 `$theme` 속성 값을 사용할 테마 이름으로 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 보내기

메일을 보내려면 [Mail 파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체 또는 컬렉션을 전달하면, 라라벨은 해당 객체의 `email`과 `name` 속성을 자동으로 사용해 수신자를 결정합니다. 이 필드들이 여러분의 객체에 있는지 꼭 확인하세요. 수신자를 지정한 뒤 mailable 클래스의 인스턴스를 `send` 메서드에 넘기면 됩니다.

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

메일을 보낼 때 "to"만 지정하는 것도 가능하지만, "cc", "bcc" 등 다른 수신자도 추가할 수 있습니다. 각각의 메서드를 체이닝해서 여러 수신자를 동시에 지정할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자에게 메일을 순차적으로 보내기

때때로, 배열로 받은 여러 수신자에게 각각 메일을 보내고 싶을 수 있습니다. 주의할 점은, `to` 메서드는 수신자 리스트에 계속 이어붙이므로, 반복문 안에서 매번 새로운 mailable 인스턴스를 만들어야 이전 수신자에게 중복 발송되는 것을 막을 수 있습니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 사용해 메일 보내기

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에서 `default`로 설정된 메일러를 사용하여 이메일을 전송합니다. 하지만, `mailer` 메서드를 사용하면 원하는 메일러 설정을 이용해 메일을 보낼 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐에 넣기

이메일 전송이 애플리케이션 응답 속도에 영향을 줄 수 있으므로, 많은 개발자들은 이메일 전송 작업을 백그라운드에서 처리하도록 큐에 넣는 방식을 선호합니다. 라라벨은 내장 [통합 큐 API](/docs/12.x/queues)를 통해 아주 쉽게 메일 메시지를 큐잉할 수 있습니다. 수신자를 지정한 후 `queue` 메서드를 사용하면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 큐에 잡을 넣어 백그라운드에서 메일이 전송되도록 처리합니다. 이 기능을 사용하려면 [큐 설정](/docs/12.x/queues)이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 딜레이 된(지연된) 메일 전송

큐에 넣은 메일 메시지의 전송 시점을 지연하려면 `later` 메서드를 사용할 수 있습니다. `later`의 첫 번째 인자로 메시지가 전송될 시점을 `DateTime` 인스턴스로 넘겨줍니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 밀어넣기

`make:mail` 명령어로 생성된 모든 mailable 클래스는 `Illuminate\Bus\Queueable` 트레이트를 내장하고 있습니다. 따라서 mailable 인스턴스에 대해 `onQueue`와 `onConnection` 메서드를 호출해, 원하는 큐 연결과 큐 이름을 지정할 수 있습니다.

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
#### 기본적으로 큐잉 처리하기

특정 mailable 클래스가 항상 큐에 올라가야 한다면, 해당 클래스에 `ShouldQueue` 계약을 구현하면 됩니다. 이렇게 하면 `send` 메서드를 사용하더라도 mailable이 큐로 전송됩니다(계약을 구현했기 때문입니다).

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치(발송)되는 경우, 큐가 데이터베이스 트랜잭션 커밋 전에 작업을 시작할 수 있습니다. 이런 상황에서는 트랜잭션 과정에서 수정한 모델이나 레코드가 데이터베이스에 아직 반영되지 않았을 수 있고, 트랜잭션으로 새로 만든 모델이나 레코드는 아직 DB에 없을 수도 있습니다. 만약 여러분의 mailable이 이런 모델에 의존할 경우, 큐 작업 처리 시 예기치 못한 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`로 되어 있어도, 특정 큐잉된 mailable이 모든 열린 DB 트랜잭션이 커밋된 후에 디스패치되길 원한다면, 메일 메시지를 보낼 때 `afterCommit` 메서드를 호출하면 됩니다.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, mailable의 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
> 이러한 이슈를 우회하는 방법에 대한 자세한 설명은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 메일 실패 처리

큐에 넣은 메일 전송이 실패하면, 만약 mailable 클래스에 `failed` 메서드가 정의되어 있을 경우 해당 메서드가 호출됩니다. 이때 실패 원인을 담고 있는 `Throwable` 인스턴스가 `failed` 메서드로 전달됩니다.

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

가끔 메일을 실제로 보내지 않고도 HTML 내용을 직접 확인하고 싶을 때가 있습니다. 이럴 때는 mailable의 `render` 메서드를 호출하면, 해당 mailable이 렌더링한 HTML 콘텐츠를 문자열로 반환받을 수 있습니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블의 템플릿을 디자인할 때 일반 Blade 템플릿처럼 브라우저에서 바로 결과를 확인할 수 있으면 매우 편리합니다. 이를 위해 라라벨은 라우트 클로저나 컨트롤러에서 mailable을 직접 리턴할 수 있도록 지원합니다. mailable 인스턴스를 반환하면 실제 이메일을 보내지 않아도 브라우저에서 디자인을 바로 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 다국어(로케일) 지원

라라벨은 메일러블을 요청의 현재 로케일이 아닌, 다른 언어로도 보낼 수 있으며, 메일이 큐에 들어간 상태에서도 지정한 로케일을 기억합니다.

이를 위해 Mail 파사드는 `locale` 메서드를 지원합니다. 원하는 언어로 로케일을 지정하면, 메일러블 템플릿이 평가될 때 해당 언어로 전환되었다가 평가가 끝나면 원래 로케일로 돌아갑니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 언어(로케일) 사용

애플리케이션에서 사용자마다 선호하는 언어(로케일)를 저장하는 경우도 있습니다. 한 모델 또는 여러 모델에 `HasLocalePreference` 계약을 구현하면 라라벨이 메일 전송 시 저장된 언어로 자동 전환하도록 할 수 있습니다.

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

이 인터페이스를 구현하면, 라라벨은 mailable이나 notification 메시지를 발송할 때 해당 모델의 선호 언어를 자동 적용합니다. 따라서 별도로 `locale` 메서드를 사용할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>

## 테스트

<a name="testing-mailable-content"></a>
### Mailable 콘텐츠 테스트

라라벨은 Mailable 클래스의 구조를 점검할 수 있는 다양한 메서드를 제공합니다. 또한, Mailable이 기대하는 콘텐츠를 포함하고 있는지 테스트할 수 있는 여러 편리한 메서드도 제공합니다. 주요 메서드는 다음과 같습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk`.

예상할 수 있듯이, "HTML" 관련 assertion은 Mailable의 HTML 버전에 특정 문자열이 포함되어 있는지 검증하며, "text" 관련 assertion은 Mailable의 일반 텍스트 버전에 특정 문자열이 포함되어 있는지를 검증합니다.

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
### 메일 발송 테스트

메일 콘텐츠 자체 테스트는 실제로 해당 메일이 특정 사용자에게 "전송"되었는지 검증하는 테스트와는 별도로 작성할 것을 권장합니다. 대부분의 경우, 메일의 실제 콘텐츠는 테스트하려는 코드와는 관련이 없으므로, 라라벨이 특정 Mailable을 발송하도록 지시받았는지만 확인하면 충분합니다.

실제 메일 발송을 방지하려면 `Mail` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드를 호출한 뒤에는, 특정 Mailable이 사용자에게 발송되었는지, 그리고 Mailable이 받은 데이터까지 점검하는 assertion을 작성할 수 있습니다.

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

만약 메일 발송을 백그라운드에서 큐에 등록해 처리한다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 클로저를 전달하여, 특정 조건("진실성 테스트")을 만족하는 Mailable이 발송되었는지 검증할 수 있습니다. 조건을 만족하는 Mailable이 하나라도 발송(혹은 큐에 등록)된 경우 Assertion은 성공합니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 assertion 메서드에서 사용되는 클로저에 전달된 Mailable 인스턴스는 메일의 다양한 정보를 점검할 수 있는 여러 유용한 메서드를 제공합니다.

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

또한, 첨부파일을 점검할 수 있는 여러 메서드도 제공합니다.

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

메일이 발송되지 않았음을 검증할 때는 `assertNotSent`와 `assertNotQueued` 두 메서드를 사용할 수 있습니다. 때로는 메일이 **전혀** 발송되지도, 큐에 등록되지도 않았음을 확인하고 싶을 수 있습니다. 이럴 때는 `assertNothingOutgoing`이나 `assertNotOutgoing`을 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일 및 로컬 개발 환경

이메일을 실제로 발송하는 애플리케이션을 개발할 때, 실제 이메일 주소로 메일을 보내고 싶지 않을 것입니다. 라라벨은 로컬 개발 환경에서 실제 이메일 발송을 "비활성화"할 수 있는 다양한 방법을 제공합니다.

<a name="log-driver"></a>
#### Log 드라이버

이메일을 실제로 발송하는 대신, `log` 메일 드라이버는 모든 이메일 메시지를 애플리케이션의 로그 파일에 기록합니다. 보통 이 드라이버는 로컬 개발 환경에서만 사용됩니다. 환경별로 애플리케이션을 설정하는 방법은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하십시오.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는, [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 등의 서비스를 활용하고, 라라벨의 `smtp` 드라이버를 사용해 이메일을 "더미" 사서함으로 보낼 수 있습니다. 이 방법을 쓰면 실제 이메일 클라이언트로 최종 메일을 확인할 수 있는 장점이 있습니다.

[라라벨 Sail](/docs/12.x/sail)을 사용 중이라면, [Mailpit](https://github.com/axllent/mailpit)으로 메시지를 미리 볼 수도 있습니다. Sail이 실행 중일 때는 `http://localhost:8025`에서 Mailpit 인터페이스에 접근할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, `Mail` 파사드가 제공하는 `alwaysTo` 메서드를 호출해, 전역적으로 "to" 주소를 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출하는 게 좋습니다.

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

라라벨은 메일 메시지가 발송되는 중에 두 개의 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지가 발송되기 *이전*에, `MessageSent` 이벤트는 메시지가 *발송된 후*에 발생합니다. 이 이벤트들은 메일이 *즉시* 발송될 때 실행되며, 큐에 등록될 때는 실행되지 않는 점을 유의하십시오. 이 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내에 작성할 수 있습니다.

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

라라벨은 여러 기본 메일 트랜스포트를 지원하지만, 라라벨이 기본적으로 지원하지 않는 서비스를 통해 이메일을 발송해야 하는 경우 직접 트랜스포트를 개발할 수 있습니다. 이를 위해서는 먼저 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 클래스를 정의해야 합니다. 그리고 `doSend` 및 `__toString()` 메서드를 구현합니다.

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

커스텀 트랜스포트를 정의했다면, `Mail` 파사드의 `extend` 메서드를 통해 등록할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이 작업을 진행합니다. `extend` 메서드에 전달한 클로저에는 `$config` 인자가 주어지며, 이 배열에는 애플리케이션의 `config/mail.php` 설정 파일에 정의된 메일러 설정이 담겨 있습니다.

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

커스텀 트랜스포트를 등록했다면, 이제 애플리케이션의 `config/mail.php` 설정 파일에 해당 트랜스포트를 사용하는 메일러 정의를 추가할 수 있습니다.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트 사용

라라벨은 Mailgun, Postmark 등 일부 Symfony에서 유지관리하는 트랜스포트도 기본적으로 지원합니다. 하지만, 더 다양한 Symfony 트랜스포트를 라라벨에 직접 추가하여 사용할 수도 있습니다. 해당 Symfony 메일러 패키지를 Composer로 설치한 후, 라라벨에 등록하면 됩니다. 예를 들어, "Brevo"(이전 이름: Sendinblue) Symfony 메일러를 설치하고 사용하고자 한다면 아래와 같이 진행할 수 있습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지 설치 후, 애플리케이션의 `services` 설정 파일에 Brevo API 자격 증명을 추가합니다.

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

그리고, 서비스 프로바이더의 `boot` 메서드에서 `Mail` 파사드의 `extend`를 호출해 트랜스포트를 등록합니다.

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

트랜스포트를 등록한 후, `config/mail.php` 설정 파일에서 해당 트랜스포트를 사용하는 메일러 항목을 정의합니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```