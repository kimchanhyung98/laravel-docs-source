# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [페일오버(failover) 설정](#failover-configuration)
    - [라운드 로빈(round robin) 설정](#round-robin-configuration)
- [메이라블(mailable) 생성하기](#generating-mailables)
- [메이라블 작성하기](#writing-mailables)
    - [발신자 설정하기](#configuring-the-sender)
    - [뷰(view) 설정하기](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [첨부 객체(attachable object)](#attachable-objects)
    - [헤더(headers)](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메이라블](#markdown-mailables)
    - [마크다운 메이라블 생성하기](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송하기](#sending-mail)
    - [메일 큐잉(queueing)](#queueing-mail)
- [메이라블 렌더링(rendering)](#rendering-mailables)
    - [브라우저에서 메이라블 미리보기](#previewing-mailables-in-the-browser)
- [메이라블 로컬라이징(localizing)](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메이라블 콘텐츠 테스트](#testing-mailable-content)
    - [메이라블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트(custom transports)](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 발송은 복잡할 필요가 없습니다. 라라벨은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깔끔하고 직관적인 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통해 이메일을 발송할 수 있는 드라이버를 지원하여, 여러분이 원하는 로컬 또는 클라우드 기반 메일 서비스를 빠르게 연결해 사용할 수 있도록 돕습니다.

<a name="configuration"></a>
### 설정

라라벨의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일에 정의된 각각의 메일러(mailers)는 고유의 설정과 "트랜스포트(transport)" 방식을 가질 수 있어, 애플리케이션에서 다양한 이메일 서비스를 상황에 따라 다르게 사용할 수 있습니다. 예를 들어, 트랜잭션(거래) 이메일은 Postmark로, 대량 이메일은 Amazon SES로 발송하도록 설정할 수 있습니다.

`mail` 설정 파일 내에는 `mailers` 설정 배열이 존재합니다. 이 배열에는 라라벨이 지원하는 주요 메일 드라이버/트랜스포트 각각에 대한 샘플 설정이 제공되며, `default` 설정값은 애플리케이션이 이메일을 발송할 때 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/트랜스포트 사전 준비 사항

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 SMTP 서버를 통한 메일 발송보다 더 간편하고 빠른 경우가 많습니다. 가능하다면 이러한 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, 먼저 Composer로 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 우선, 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 아래와 같은 설정 배열을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러 설정이 완료되었으면, `config/services.php` 파일에도 아래와 같은 옵션을 추가해야 합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 외의 [Mailgun 지역(Region)](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)에서 메일을 발송한다면, 해당 지역의 엔드포인트를 `services` 설정 파일에 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer를 통해 Symfony의 Postmark Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

다음으로, `config/mail.php` 파일의 `default` 옵션을 `postmark`로 설정하세요. 기본 메일러를 설정한 후에는, `config/services.php` 파일에 다음 옵션이 포함되어 있는지 확인합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하고 싶다면, `message_stream_id` 설정 옵션을 해당 메일러 설정 배열에 추가할 수 있습니다. 이 설정 배열은 애플리케이션의 `config/mail.php`에 위치합니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer로 Resend의 PHP SDK를 설치합니다:

```shell
composer require resend/resend-php
```

그 다음, 애플리케이션의 `config/mail.php`파일에서 `default` 옵션을 `resend`로 설정하세요. 그리고 기본 메일러 설정 후에는 `config/services.php` 파일이 아래와 같은 옵션을 포함하는지 확인합니다:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer를 이용해 해당 라이브러리를 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일이 아래의 옵션을 포함하는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰을 통해 사용하려면, SES 설정에 `token` 키를 추가하면 됩니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능(subscription management features)](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하고 싶다면, 메일 메시지의 [headers](#headers) 메서드가 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 다음과 같이 추가하세요:

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

라라벨이 이메일 전송 시 AWS SDK의 `SendEmail` 메서드로 전달해야 할 [추가 옵션들](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, `ses` 설정에 `options` 배열을 추가할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션(거래) 이메일 및 SMS 서비스를 제공하며, 라라벨 전용 API 기반 메일 드라이버 패키지를 배포합니다. 이 드라이버 패키지는 Composer로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

패키지 설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하고, `MAIL_MAILER` 환경 변수도 `mailersend`로 지정해야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php` 파일의 `mailers` 배열에 MailerSend를 추가합니다:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend 사용 방법 및 호스팅 템플릿 활용 방법 등 자세한 사항은 [MailerSend 드라이버 공식 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 페일오버(failover) 설정

가끔, 외부 메일 서비스가 다운될 수 있습니다. 이런 상황을 대비해 메일 발송에 사용할 백업 메일러 설정을 미리 지정해 두면 좋습니다.

이를 위해서는 애플리케이션의 `mail` 설정 파일에 `failover` 트랜스포트를 사용하는 메일러를 정의해야 합니다. `failover` 메일러의 설정 배열에는 실제로 메일 발송에 사용될 메일러를 순서대로 나열한 `mailers` 배열이 포함되어야 합니다:

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

페일오버 메일러를 정의한 뒤, 이 메일러를 애플리케이션에서 기본으로 사용하도록 `mail` 설정 파일의 `default` 키 값에 해당 메일러 이름을 지정해야 합니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(round robin) 설정

`roundrobin` 트랜스포트는 메일 발송 작업을 여러 메일러에 분산시켜 처리할 수 있게 해줍니다. 사용하려면, `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의합니다. 이 설정 배열에는 메일 발송에 사용할 메일러를 나열한 `mailers` 배열이 포함되어야 합니다:

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

라운드 로빈 메일러를 정의한 뒤, 이 메일러를 기본 메일러로 사용하려면 `mail` 설정 파일의 `default` 항목에 해당 메일러 이름을 지정하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 설정한 메일러 리스트에서 무작위로 하나를 선택한 뒤, 그 이후에는 메일이 발송될 때마다 다음 메일러로 순차적으로 전환합니다. 즉, *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*를 위해 사용되는 `failover` 트랜스포트와 달리, `roundrobin` 트랜스포트는 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 기능을 제공합니다.

<a name="generating-mailables"></a>
## 메이라블(mailable) 생성하기

라라벨 애플리케이션에서는, 각 이메일 유형을 "메이라블(mailable)" 클래스가 담당합니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 애플리케이션에 이 디렉터리가 보이지 않더라도 걱정하지 마세요. `make:mail` 아티즌(Artisan) 명령어로 처음 메이라블 클래스를 생성하면 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메이라블 작성하기

메이라블 클래스를 생성했다면, 이제 파일을 열어서 내부 구성을 살펴봅시다. 메이라블 클래스의 설정은 주로 `envelope`, `content`, `attachments` 등의 메서드에서 이루어집니다.

`envelope` 메서드는 메시지의 제목(subject)과, 필요한 경우 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 콘텐츠 생성을 위해 사용할 [Blade 템플릿](/docs/12.x/blade) 정보를 담은 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정하기

<a name="using-the-envelope"></a>
#### Envelope로 발신자 지정하기

먼저, 이메일의 발신자를 설정하는 방법을 살펴봅시다. 즉, "보내는 사람(from)"이 누구인지를 지정하는 것입니다. 이 발신자를 설정하는 방법은 두 가지가 있습니다. 첫 번째 방식은 메시지의 envelope에서 "from" 주소를 지정하는 것입니다:

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

필요하다면, `replyTo` 주소도 함께 지정할 수 있습니다:

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

하지만 애플리케이션의 모든 이메일이 동일한 "from" 주소를 사용한다면, 각각의 메이라블 클래스에 일일이 지정하는 것이 번거로울 수 있습니다. 이런 경우에는 `config/mail.php` 설정 파일에 전역 "from" 주소를 미리 지정할 수 있습니다. 별도로 메이라블 클래스에서 "from"을 지정하지 않은 경우, 이 전역 설정이 적용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, 전역 "reply_to" 주소도 마찬가지로 `config/mail.php`에 설정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(view) 설정하기

메이라블 클래스의 `content` 메서드 안에서, 이메일 본문 렌더링에 사용할 뷰(템플릿)를 정의할 수 있습니다. 대부분의 경우, 이메일 콘텐츠는 [Blade 템플릿](/docs/12.x/blade)으로 작성하게 되므로, HTML 이메일을 만들 때 Blade의 편리함과 강력함을 그대로 활용할 수 있습니다:

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
> 이메일 템플릿을 보관할 `resources/views/mail` 폴더를 따로 만드는 것을 권장하지만, `resources/views` 디렉터리 내 원하는 경로에 자유롭게 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트(plain-text) 이메일

이메일에 일반 텍스트 버전을 추가하고 싶다면, `Content` 정의 시 plain-text 템플릿을 함께 지정하면 됩니다. `view` 파라미터와 마찬가지로, `text`에는 이메일 내용을 렌더링할 템플릿명을 지정합니다. HTML 버전과 텍스트 버전을 모두 정의할 수도 있습니다:

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

혼란을 줄이기 위해, `html` 파라미터는 `view` 파라미터의 별칭으로 사용할 수 있습니다:

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

일반적으로는, 이메일 본문 렌더링 시 활용할 데이터를 뷰에 전달하고자 할 것입니다. 뷰에 데이터를 전달하는 방법은 두 가지가 있습니다. 첫 번째는 메이라블 클래스에 public 속성을 정의하는 것입니다. 생성자에서 전달받은 데이터를 public 속성에 할당하면, 해당 속성은 자동으로 뷰에서 사용할 수 있게 됩니다:

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

데이터가 public 속성에 저장되면, 뷰에서 다른 Blade 템플릿 데이터처럼 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

이메일 데이터의 가공이나 형식을 커스터마이즈하고 싶다면, `Content` 정의의 `with` 파라미터를 통해 템플릿에 직접 데이터를 넘길 수 있습니다. 보통은 생성자에서 데이터를 받아오되, 해당 데이터를 public이 아닌 `protected` 또는 `private` 속성에 저장하여 뷰에 자동으로 노출되지 않게 한 뒤, `with` 파라미터로 원하는 데이터만 전달하면 됩니다:

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

`with` 파라미터로 전달한 데이터 역시 뷰에서 바로 접근 가능합니다. Blade 템플릿에서도 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메일 메시지의 `attachments` 메서드에서 첨부파일을 배열로 반환하면 됩니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 지정해 첨부할 수 있습니다:

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

첨부파일 추가 시, `as` 및 `withMime` 메서드를 활용하면 첨부파일의 표시 이름이나 MIME 타입을 지정할 수도 있습니다:

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
#### 파일 시스템에서 첨부하기

[파일 시스템 디스크](/docs/12.x/filesystem)에 파일을 저장해두었다면, `fromStorage` 메서드로 이메일에 첨부할 수 있습니다:

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

물론, 첨부파일의 이름과 MIME 타입도 지정할 수 있습니다:

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

기본 디스크 외에 다른 스토리지 디스크를 사용하려면 `fromStorageDisk` 메서드를 이용하세요:

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

`fromData` 첨부 메서드를 사용하면 바이트 문자열 데이터를 직접 첨부파일로 추가할 수 있습니다. 예를 들어, PDF 파일을 메모리에서 생성한 뒤 디스크에 파일로 저장하지 않고 바로 이메일에 첨부하고 싶을 때 이 메서드를 사용할 수 있습니다. `fromData` 메서드는 첨부할 원시 데이터 바이트를 반환하는 클로저와 첨부파일로 지정할 이름을 인수로 받습니다.

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

이메일에 인라인 이미지를 삽입하는 것은 일반적으로 번거로운 작업이지만, 라라벨에서는 이미지를 이메일에 쉽게 첨부할 수 있는 편리한 방법을 제공합니다. 인라인 이미지를 넣으려면, 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. 라라벨은 모든 이메일 템플릿에서 `$message` 변수를 자동으로 사용할 수 있게 해주므로, 별도로 전달할 필요가 없습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> 플레인 텍스트 메시지 템플릿에서는 `$message` 변수를 사용할 수 없습니다. 플레인 텍스트 메시지는 인라인 첨부파일을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw Data 첨부파일 임베딩

이미 이미지의 원시 데이터를 문자열 형태로 가지고 있고, 이 데이터를 이메일 템플릿에 임베드하고 싶다면 `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. `embedData`를 호출할 때는, 임베드될 이미지에 할당할 파일명을 함께 지정해야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

문자열 경로로 파일을 첨부하는 것도 충분하지만, 애플리케이션에 있는 첨부 대상이 클래스(객체)로 표현되는 경우도 다양하게 있습니다. 예를 들어, 사진을 메시지에 첨부한다면 애플리케이션에는 그 사진을 표현하는 `Photo` 모델도 있을 수 있습니다. 이럴 때, `Photo` 모델 인스턴스를 `attach` 메서드에 그대로 전달해 첨부할 수 있으면 매우 편리할 것입니다. Attachable 객체는 바로 이런 기능을 제공합니다.

이 기능을 사용하려면, 첨부 가능한 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다. 이 인터페이스는 클래스에 `toMailAttachment` 메서드를 정의하도록 요구합니다. 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

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

Attachable 객체를 정의했으면, 이메일 메시지를 만들 때 `attachments` 메서드에서 이 객체의 인스턴스를 반환하면 됩니다.

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

물론, 첨부 데이터가 Amazon S3 같은 원격 파일 스토리지 서비스에 저장되었을 수도 있습니다. 이런 경우, 라라벨에서는 애플리케이션의 [파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 바탕으로 첨부 인스턴스를 생성할 수도 있습니다.

```php
// 기본 디스크에 저장된 파일로부터 첨부파일 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 첨부파일 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 보관 중인 데이터를 통해서도 첨부 인스턴스를 만들 수 있습니다. 이를 위해 `fromData` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 첨부에 해당하는 원시 데이터를 반환해야 합니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

라라벨은 첨부파일을 더욱 세밀하게 커스터마이즈할 수 있는 여러 추가 메서드도 제공합니다. 예를 들어, `as` 및 `withMime` 메서드를 이용해 파일 이름과 MIME 타입을 지정할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

경우에 따라 발신 메시지에 추가 헤더를 설정해야 할 수 있습니다. 예를 들어, 커스텀 `Message-Id` 나 기타 임의의 텍스트 헤더를 지정하고 싶을 수 있습니다.

이럴 때는, mailable 클래스에 `headers` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 합니다. 이 클래스는 `messageId`, `references`, `text` 매개변수를 제공할 수 있도록 되어 있습니다. 물론, 필요한 매개변수만 전달해도 무방합니다.

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

일부 서드파티 이메일 제공 서비스(예: Mailgun, Postmark)는 메시지 "태그(tags)" 및 "메타데이터(metadata)"를 지원하며, 이를 통해 애플리케이션에서 발송하는 이메일을 그룹화하거나 추적할 수 있습니다. 이메일 메시지에 태그 및 메타데이터를 추가하려면 `Envelope` 정의에서 해당 값을 지정하면 됩니다.

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

Mailgun 드라이버를 사용하는 경우, [Mailgun 태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대한 공식 문서도 참고할 수 있습니다. Postmark를 사용하는 경우에도 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원 문서를 참고하시기 바랍니다.

Amazon SES를 통해 이메일을 발송하는 경우, 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부하려면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

라라벨의 메일 기능은 Symfony Mailer를 기반으로 동작합니다. 메일 전송 전, Symfony Message 인스턴스를 이용해 메시지를 커스터마이즈할 수 있도록 콜백을 등록해서 활용할 수 있습니다. 이를 위해 `Envelope` 정의에 `using` 매개변수를 추가하세요.

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

마크다운 메일러블 메시지를 사용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)에서 제공하는 템플릿과 컴포넌트를 메일러블에서도 활용할 수 있습니다. 메시지를 마크다운으로 작성하면, 라라벨이 아름답고 반응형(Responsive) HTML 템플릿을 자동으로 렌더링하고, 동시에 플레인 텍스트 버전도 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿이 연결된 메일러블을 생성하려면, `make:mail` 아티즌 명령어에서 `--markdown` 옵션을 사용하면 됩니다.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, 해당 메일러블 클래스의 `content` 메서드에서 Content 정의를 구성할 때, `view` 대신 `markdown` 파라미터를 사용하세요.

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

마크다운 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합해서, 라라벨의 미리 만들어진 이메일 UI 컴포넌트들을 손쉽게 활용하면서 메일 메시지를 만들 수 있게 해줍니다.

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
> 마크다운 이메일을 작성할 때에는 들여쓰기를 과하게 사용하지 마십시오. Markdown 표준에 따라, 들여쓰기된 줄은 코드 블록으로 처리될 수 있습니다.

<a name="button-component"></a>
#### 버튼(Button) 컴포넌트

버튼 컴포넌트는 중앙에 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color` 파라미터를 받습니다. 지원하는 색상 값은 `primary`, `success`, `error`입니다. 메시지에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널(Panel) 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 약간 다른 배경색의 패널에 표시해줍니다. 이를 통해 특정 텍스트 블록에 주목을 유도할 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블(Table) 컴포넌트

테이블 컴포넌트를 사용하면 Markdown 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 Markdown 테이블을 content로 받으며, 컬럼 정렬도 기본 Markdown 테이블 정렬 문법을 그대로 지원합니다.

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

마크다운 메일 컴포넌트 전체를 내 애플리케이션에 복사해 원하는 대로 커스터마이즈할 수 있습니다. 이를 위해 `vendor:publish` 아티즌 명령어를 사용하여 `laravel-mail` 에셋 태그를 퍼블리시하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령을 실행하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 퍼블리시됩니다. 이 안의 `mail` 디렉터리에는 `html`과 `text` 디렉터리가 각각 존재하며, 각 컴포넌트의 HTML과 텍스트 버전을 포함합니다. 원하시는 방식으로 자유롭게 컴포넌트를 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 퍼블리시한 이후, `resources/views/vendor/mail/html/themes` 디렉터리 내에는 `default.css` 파일이 생성됩니다. 이 파일의 CSS를 자유롭게 수정할 수 있고, 적용한 스타일은 마크다운 메일 메시지의 HTML 버전을 렌더링할 때 자동으로 인라인 CSS로 변환됩니다.

만약 라라벨의 마크다운 컴포넌트를 위한 완전히 새로운 테마를 만들고 싶다면, `html/themes` 디렉터리에 새로운 CSS 파일을 추가하면 됩니다. 파일에 이름을 지정하여 저장한 후, 애플리케이션의 `config/mail.php` 설정 파일에서 `theme` 옵션을 해당 테마 이름으로 변경하면 새로운 테마가 적용됩니다.

특정 개별 메일러블에만 다른 테마를 지정하고 싶다면, 메일러블 클래스의 `$theme` 속성에 사용할 테마명을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송

메시지를 발송하려면 `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용하십시오. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체 혹은 객체 컬렉션을 전달한다면, 메일러는 자동으로 해당 객체의 `email`과 `name` 속성을 찾아 이메일 수신자를 결정합니다. 이런 속성을 객체에 꼭 추가해 두어야 합니다. 수신자가 정해졌다면, 메일러블 클래스의 인스턴스를 `send` 메서드에 전달하면 됩니다.

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

메일 전송 시 반드시 "to" 수신자만 지정해야 하는 것은 아닙니다. 필요하다면 "to", "cc", "bcc" 수신자를 각 메서드로 체이닝해서 모두 지정할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자에게 반복 전송

때때로, 배열로 여러 명의 이메일 수신자가 있을 때 반복문으로 각각에게 메일러블을 발송해야 할 수 있습니다. 하지만 `to` 메서드는 이메일 주소를 누적시키는 방식이기 때문에, 반복문을 돌며 전송하면 모든 이전 수신자에게도 메일이 계속 전송됩니다. 따라서 반드시 각 수신자마다 새로운 메일러블 인스턴스를 생성해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 전송

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에 있는 `default` 메일러 설정을 사용합니다. 하지만, 특정 메일러 설정을 써서 메시지를 보내고 싶다면 `mailer` 메서드를 쓸 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉(Queueing)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송은 애플리케이션의 응답 시간을 저하시킬 수 있으므로, 많은 개발자들이 메일 전송을 백그라운드에서 처리하기 위해 큐를 활용합니다. 라라벨에서는 내장된 [통합 큐 API](/docs/12.x/queues)를 통해 이를 쉽게 사용할 수 있습니다. 메일 메시지를 큐잉하려면, 메시지의 수신자를 지정한 후 `Mail` 파사드에서 `queue` 메서드를 사용하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 해당 메일을 백그라운드에서 전송하도록 자동으로 큐에 잡(Job)을 추가합니다. 이 기능을 사용하려면 [큐 설정](/docs/12.x/queues)이 먼저 되어 있어야 합니다.

<a name="delayed-message-queueing"></a>
#### 딜레이 큐잉(Delay) 메일 전송

큐에 등록한 메일 메시지의 전송을 지연(delay)하고 싶으면, `later` 메서드를 사용할 수 있습니다. 첫 번째 인수로는 언제 메시지를 보낼지에 대한 `DateTime` 인스턴스를 전달하면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/커넥션으로 밀어넣기

`make:mail` 명령어로 생성된 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레잇을 사용하므로, 모든 메일러블 인스턴스에서 `onQueue` 및 `onConnection` 메서드를 호출할 수 있습니다. 이를 통해 메시지가 어떤 커넥션과 큐에 들어갈지 지정할 수 있습니다.

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
#### 항상 큐잉되는 메일러블 만들기

특정 메일러블 클래스가 항상 큐에 등록되도록 하고 싶다면, 해당 클래스에서 `ShouldQueue` 인터페이스를 구현하면 됩니다. 이렇게 하면 `send` 메서드로 메일을 보낼 때도 항상 큐에 등록되어 백그라운드에서 처리됩니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블을 데이터베이스 트랜잭션 안에서 디스패치하면, 트랜잭션이 커밋되기 전에 큐 워커가 잡을 처리할 수도 있습니다. 이런 경우, 트랜잭션 내에서 작업한 모델이나 레코드의 상태가 데이터베이스에 반영되지 않았을 수 있습니다. 또한, 트랜잭션 중에 생성한 모델이나 레코드가 아직 데이터베이스에 존재하지 않아, 해당 모델에 의존하는 메일러블에서 예기치 않은 오류가 발생할 위험이 있습니다.

큐 커넥션의 `after_commit` 설정 옵션이 `false`일 때도, 특정 큐잉 메일러블을 모든 열린 데이터베이스 트랜잭션이 커밋된 이후에만 디스패치되도록 하려면 메일 전송 시 `afterCommit` 메서드를 호출하면 됩니다.

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
     * Create a new message instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이러한 문제를 회피하는 방법에 대해 더 자세한 내용은 [큐 잡과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하시기 바랍니다.

<a name="queued-email-failures"></a>
#### 큐잉 이메일 실패 처리

큐잉된 이메일이 전송 과정에서 실패하면, 해당 큐잉 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 이때 실패를 유발한 `Throwable` 인스턴스가 `failed` 메서드의 인수로 전달됩니다.

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

종종 메일을 실제로 발송하지 않고도 메일러블의 HTML 내용을 미리 확인하고 싶을 수 있습니다. 이럴 때는 메일러블의 `render` 메서드를 호출하면 됩니다. 이 메서드는 평가된 HTML 콘텐츠를 문자열로 반환합니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블의 템플릿을 디자인할 때, 일반 Blade 템플릿처럼 브라우저에서 렌더된 메일러블을 바로 미리볼 수 있으면 편리합니다. 이를 위해 라라벨에서는 라우트 클로저나 컨트롤러에서 메일러블을 직접 반환할 수 있습니다. 이렇게 반환하면 이메일로 실제 발송하지 않아도 렌더링되어 브라우저에서 디자인을 빠르게 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 다국어 지원(Localization)

라라벨에서는 현재 요청의 언어(locale)와 다른 언어로 메일러블을 보낼 수 있습니다. 심지어, 메일이 큐에 등록되어 있어도 이 언어 설정이 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정하십시오. 메일러블의 템플릿이 평가되는 동안 애플리케이션의 언어가 지정된 것으로 임시 변경되고, 평가가 끝나면 다시 원래 언어로 돌아갑니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 언어 지원

애플리케이션에서 각 사용자의 선호 언어(locale)를 저장할 때가 있습니다. 이 경우, 한 개 이상의 모델에 `HasLocalePreference` 인터페이스를 구현하면, 해당 모델에 저장된 언어로 메일을 보낼 수 있습니다.

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

이 인터페이스를 구현했다면, 이제 라라벨에서는 그 모델에 메일러블이나 알림을 보낼 때 자동으로 선호 언어를 적용합니다. 따라서 `locale` 메서드를 따로 호출할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>

## 테스트

<a name="testing-mailable-content"></a>
### 메일러블(Mailable) 콘텐츠 테스트

라라벨은 메일러블의 구조를 확인할 수 있는 다양한 메서드를 제공합니다. 또한, 메일러블에 기대하는 콘텐츠가 포함되어 있는지 편리하게 테스트할 수 있는 여러 메서드도 지원합니다. 주요 메서드는 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk`입니다.

이름에서 알 수 있듯, "HTML" 관련 assertion(확인) 메서드는 메일러블의 HTML 버전에 특정 문자열이 포함되어 있는지 검증하고, "text" assertion은 일반 텍스트 버전에 해당 문자열이 있는지 검증합니다.

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
### 메일러블(Mailable) 발송 테스트

메일러블의 내용을 개별적으로 테스트하는 것과 실제로 특정 사용자에게 "전송"되었는지를 테스트하는 것을 분리하는 것을 권장합니다. 일반적으로, 메일러블의 내용은 해당 테스트하려는 코드의 핵심과 직접적인 연관이 없는 경우가 많으므로, 라라벨이 해당 메일러블을 전송하도록 지시했는지만 확인하면 충분할 수 있습니다.

이메일이 실제로 전송되는 것을 방지하려면 `Mail` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드를 호출한 후에는, 메일러블이 특정 사용자에게 전송되었는지 또는 전달된 데이터가 어떤 것인지를 단언할 수 있습니다.

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

만약 메일러블을 백그라운드에서 대기열로 처리(큐잉)하고 있다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

메일이 발송되었는지, 또는 발송이 되지 않았는지를 통해 진위값을 확인하고 싶을 때, 클로저(익명 함수)를 `assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued`에 전달할 수 있습니다. 전달한 클로저에서 "참"을 반환하는 경우, 해당하는 메일러블이 하나라도 있다면 assertion은 성공합니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

이렇게 클로저로 전달되는 메일러블 인스턴스는, 메일러블을 다양한 방식으로 검사할 수 있도록 다음과 같은 유용한 메서드를 제공합니다.

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

메일러블의 첨부 파일(Attachment) 역시 아래와 같이 추가로 검증할 수 있습니다.

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

발송이 되지 않았음을 검증하는 방법에는 `assertNotSent`, `assertNotQueued`가 있지만, 간혹 "메일이 전송도 아니고 큐에도 들어가지 않았음"을 한번에 확인하고 싶을 때가 있습니다. 이럴 때는 `assertNothingOutgoing`, `assertNotOutgoing` 메서드를 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

이메일을 발송하는 애플리케이션을 개발할 때 실제 이메일 주소로 메일이 보내지기를 원치 않으실 수 있습니다. 라라벨은 로컬 개발 중 실제 이메일 전송을 "비활성화"할 수 있는 몇 가지 방법을 제공합니다.

<a name="log-driver"></a>
#### Log 드라이버

이메일을 실제로 전송하지 않고, `log` 메일 드라이버를 사용하면 모든 이메일 메시지가 로그 파일에 기록되어 확인할 수 있습니다. 이 드라이버는 주로 로컬 개발 환경에서만 사용합니다. 환경별로 애플리케이션을 구성하는 방법에 대해서는 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또 다른 방법으로, [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스를 이용하고 `smtp` 드라이버를 설정하면, 메일을 "가짜" 메일함으로 전송하여 실제 이메일 클라이언트에서 메일을 조회할 수 있습니다. 이 방식은 Mailtrap의 메시지 뷰어 등을 통해 실제 전송된 형태의 이메일을 직접 확인할 수 있다는 장점이 있습니다.

[라라벨 Sail](/docs/12.x/sail)을 사용한다면 [Mailpit](https://github.com/axllent/mailpit)을 통해 메시지를 미리 볼 수도 있습니다. Sail이 실행 중일 때는 `http://localhost:8025`에서 Mailpit 인터페이스에 접근할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 이용해 전역 "to" 주소를 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출하는 것이 좋습니다.

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

라라벨은 메일 메시지 전송 시 두 가지 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지가 전송되기 *직전*에 발생하며, `MessageSent` 이벤트는 메시지가 전송된 *이후*에 발생합니다. 주의할 점은 이 이벤트들은 메일이 실제로 "전송"될 때 발행(디스패치)되며, 큐에 추가되는 것과는 다르다는 점입니다. 애플리케이션 내에서 이 이벤트들에 대해 [이벤트 리스너](/docs/12.x/events)를 작성할 수 있습니다.

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
## 커스텀 메일 트랜스포트

라라벨은 다양한 메일 트랜스포트(전송 방식)를 제공합니다. 하지만 라라벨에서 기본적으로 지원하지 않는 별도의 외부 서비스로 이메일을 보내고 싶다면, 직접 트랜스포트를 구현할 수 있습니다. 시작하려면 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 클래스를 정의하고, 그 안에 `doSend`와 `__toString` 메서드를 구현해야 합니다.

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

커스텀 트랜스포트를 정의했다면, 이제 `Mail` 파사드의 `extend` 메서드를 통해 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider` 서비스 프로바이더의 `boot` 메서드 내에서 수행하면 됩니다. 이때, `extend`에 넘기는 클로저(익명 함수)에는 `$config` 인자가 전달됩니다. 이 인자에는 애플리케이션 `config/mail.php`에 정의된 메일러 설정 배열이 포함됩니다.

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

커스텀 트랜스포트 등록이 끝나면, 이제 `config/mail.php` 설정 파일에 새로운 트랜스포트를 사용하는 메일러 정의를 추가할 수 있습니다.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

라라벨은 Mailgun, Postmark 등 이미 Symfony에서 관리하는 일부 메일 트랜스포트를 기본 지원합니다. 하지만 필요하다면 Symfony에서 지원하는 다른 메일 트랜스포트도 추가로 사용할 수 있습니다. 이렇게 하려면 필요한 Symfony 메일러 패키지를 Composer로 설치하고, 라라벨에 트랜스포트를 등록하면 됩니다. 예를 들어 "Brevo"(구 Sendinblue) Symfony 메일러를 설치 및 등록하는 방법은 아래와 같습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지가 설치되었다면, 이제 애플리케이션의 `services` 설정 파일에 API 인증 정보를 추가합니다.

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

이제 `Mail` 파사드의 `extend` 메서드를 통해 트랜스포트를 등록할 수 있습니다. 이 작업 역시 서비스 프로바이더의 `boot` 메서드에서 하는 것이 일반적입니다.

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

트랜스포트 등록이 완료되면, `config/mail.php` 설정 파일에 새 트랜스포트를 사용할 메일러 정의를 추가할 수 있습니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```