# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈(round robin) 설정](#round-robin-configuration)
- [메일러블(mailable) 클래스 생성](#generating-mailables)
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
- [메일러블 로컬라이즈](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 콘텐츠 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일을 보내는 작업은 복잡할 필요가 없습니다. 라라벨은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깨끗하고 간단한 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 이메일 발송을 지원하는 다양한 드라이버를 제공하므로, 로컬 또는 클라우드 기반 서비스 중 원하는 것을 선택해 손쉽게 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

라라벨 애플리케이션의 이메일 서비스는 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 설정된 각 메일러(mailer)는 고유한 설정과 "트랜스포트"를 가질 수 있어서, 애플리케이션에서 특정 이메일 메시지를 보낼 때 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일 안에는 `mailers` 설정 배열이 있습니다. 이 배열에는 라라벨에서 지원하는 주요 메일 드라이버/트랜스포트에 대한 예시 설정이 포함되어 있고, `default` 설정 값은 애플리케이션이 이메일 메시지를 보낼 때 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비사항

Mailgun, Postmark, Resend, MailerSend와 같이 API 기반 드라이버들은 종종 SMTP 서버를 통한 메일 발송보다 더 간단하고 빠릅니다. 가능하다면 이들 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그 다음, 아래와 같이 `mailers` 배열에 mailgun 설정을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션을 추가해야 합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용하지 않는 경우에는, `services` 설정 파일에서 해당 리전의 엔드포인트를 지정할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer를 통해 Symfony의 Postmark Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

이후, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 지정합니다. 그리고 기본 메일러를 설정한 다음, `config/services.php` 설정 파일에 아래와 같은 옵션이 포함되어 있는지 확인합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하고 싶다면, mailer의 설정 배열에 `message_stream_id` 옵션을 추가하면 됩니다. 이 설정 배열은 `config/mail.php` 파일에서 찾을 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이 방식으로 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer를 통해 Resend의 PHP SDK를 설치해야 합니다:

```shell
composer require resend/resend-php
```

이후, `config/mail.php` 설정 파일의 `default` 옵션을 `resend`로 지정하세요. 기본 메일러를 설정한 다음, `config/services.php` 파일에 아래와 같은 옵션이 포함되어 있는지 확인합니다:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer 패키지 매니저로 아래 라이브러리를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

그리고 `config/mail.php` 설정 파일에서 `default` 옵션을 `ses`로 지정한 뒤, `config/services.php` 파일이 아래와 같은 옵션을 포함하는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰을 통해 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드가 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 반환하면 됩니다:

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

라라벨에서 이메일을 보낼 때 AWS SDK의 `SendEmail` 메서드에 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 전달하고 싶다면, `ses` 설정에 `options` 배열을 정의할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스를 제공하는 서비스로, 라라벨용 API 기반 메일 드라이버 패키지를 별도로 관리하고 있습니다. 이 드라이버 패키지는 Composer 패키지 매니저로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

패키지 설치 후에는 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경변수를 추가하세요. 그리고 `MAIL_MAILER` 환경변수도 `mailersend`로 지정해야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

이제 애플리케이션의 `config/mail.php` 설정 파일 내 `mailers` 배열에 MailerSend를 추가합니다:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend 및 호스팅 템플릿 등 더 많은 정보는 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정

외부 서비스를 사용해 메일을 보내다 보면, 가끔 해당 서비스가 다운될 수도 있습니다. 이럴 때, 주 메일 발송 드라이버가 다운되었을 때 사용할 백업 메일 발송 설정을 하나 이상 정의해 두면 유용합니다.

이를 위해, `failover` 트랜스포트를 사용하는 메일러를 `mail` 설정 파일에 정의해야 합니다. 이 `failover` 메일러의 설정 배열에는 어떤 순서로 설정된 메일러를 사용할지 지정하는 `mailers` 배열이 포함됩니다:

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

failover 메일러를 정의했다면, 이 이름을 `mail` 설정 파일의 `default` 설정의 값으로 지정하여 애플리케이션의 기본 메일러로 설정해야 합니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(round robin) 설정

`roundrobin` 트랜스포트를 사용하면 여러 메일러에 메일 발송 작업을 분산시킬 수 있습니다. 이를 위해, `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의하고, 어떤 메일러를 사용할지 지정하는 `mailers` 배열을 포함해야 합니다:

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

round robin 메일러를 정의한 후에는, 해당 이름을 `mail` 설정 파일의 `default` 설정 값으로 지정하면 애플리케이션이 기본적으로 이 메일러를 사용하게 됩니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

round robin 트랜스포트는 설정된 메일러 목록에서 무작위로 하나를 선택하여 메일을 보내고, 이후에는 다음에 사용할 수 있는 메일러로 계속 순차적으로 전환합니다. `failover` 트랜스포트가 *[고가용성(HA)](https://en.wikipedia.org/wiki/High_availability)*을 위한 것이라면, `roundrobin` 트랜스포트는 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블(mailable) 클래스 생성

라라벨 애플리케이션에서 발송하는 각 이메일 유형은 "메일러블(mailable)" 클래스 하나로 표현됩니다. 이러한 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 이 디렉터리가 프로젝트에 보이지 않더라도 걱정할 필요 없습니다. `make:mail` 아티즌 명령어로 처음 메일러블 클래스를 생성하면 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성

메일러블 클래스를 생성했다면, 이제 내용을 살펴보겠습니다. 메일러블 클래스의 다양한 설정은 `envelope`, `content`, `attachments` 메서드 등에서 이뤄집니다.

`envelope` 메서드는 메시지의 제목(subject)과 (필요할 경우) 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문을 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope를 이용한 설정

먼저, 이메일의 발신자(sendeer)를 설정하는 방법을 살펴보겠습니다. 즉, 이메일이 "누구로부터" 보내지는지를 정하는 것입니다. 발신자 설정에는 두 가지 방법이 있습니다. 먼저, 메시지의 envelope에 "from" 주소를 지정할 수 있습니다:

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
#### 전역 `from` 주소 사용

만약 애플리케이션 전체에서 같은 "from" 주소를 사용한다면, 생성하는 모든 메일러블 클래스마다 이 주소를 추가해야 하는 것이 번거로울 수 있습니다. 이럴 때는 `config/mail.php` 설정 파일에 전역 "from" 주소를 지정할 수 있습니다. 별도의 "from" 주소를 메일러블 클래스에서 지정하지 않은 경우 이 주소가 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, `config/mail.php` 파일에서 전역 "reply_to" 주소도 지정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드에서 이메일 본문을 렌더링할 때 사용할 `view`, 즉 템플릿을 지정할 수 있습니다. 일반적으로 이메일의 콘텐츠는 [Blade 템플릿](/docs/12.x/blade)으로 작성하므로, 이메일 HTML 구성에도 Blade의 여러 편리함을 모두 활용할 수 있습니다:

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
> `resources/views/mail` 디렉터리를 따로 만들어 이메일 템플릿을 모아 둘 수 있지만, 실제 위치는 `resources/views` 디렉터리 아래 어디든 자유롭게 배치하셔도 됩니다.

<a name="plain-text-emails"></a>
#### 텍스트 전용 이메일

이메일의 텍스트 전용(plain-text) 버전을 정의하고 싶다면, 메시지의 `Content` 정의에서 텍스트 템플릿을 지정하면 됩니다. `view` 파라미터와 마찬가지로, `text` 파라미터에 템플릿명을 넘기면 이메일 본문의 텍스트 버전을 렌더링할 수 있습니다. HTML 버전과 텍스트 버전을 모두 정의해도 괜찮습니다:

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

더 명확하게 하고 싶다면, `html` 파라미터를 `view` 대신 사용할 수도 있습니다:

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

이메일의 HTML을 렌더링할 때, 뷰에서 사용할 데이터를 전달해야 할 때가 많습니다. 데이터 전달에는 두 가지 방법이 있습니다. 첫 번째로, 메일러블 클래스에 정의한 public 속성은 자동으로 뷰에 전달됩니다. 예를 들어, 생성자에서 데이터를 인자로 받으면, 이 데이터를 public 속성에 할당할 수 있습니다:

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

데이터를 public 속성에 할당하면 뷰에서도 곧바로 사용할 수 있으므로, Blade 템플릿에서 다른 데이터와 마찬가지로 변수로 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 이용한 데이터 전달

이메일에 전달하는 데이터의 형식을 뷰로 넘기기 전에 직접 커스터마이즈하고 싶다면, `Content` 정의의 `with` 파라미터를 활용해 데이터를 수동으로 전달할 수 있습니다. 보통 생성자에서 데이터를 받아오고, 해당 데이터는 `protected`나 `private` 속성에 저장해서 자동으로 뷰에 노출되지 않도록 합니다:

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

`with` 파라미터로 데이터를 전달하면 역시 뷰에서는 일반 변수를 접근하듯 아래와 같이 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메일 메시지의 `attachments` 메서드에서 반환하는 배열에 첨부 파일 정보를 추가하면 됩니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 넘겨 첨부할 수 있습니다:

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

파일을 첨부할 때 `as`와 `withMime` 메서드를 활용하면 첨부 파일의 표시 이름이나 MIME 타입도 지정할 수 있습니다:

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

[파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 이메일에 첨부하고 싶을 때는, `fromStorage` 첨부 메서드를 사용하면 됩니다:

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

물론, 첨부 파일의 이름과 MIME 타입도 다음과 같이 지정할 수 있습니다:

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

기본 디스크 외에 다른 스토리지 디스크에서 파일을 첨부해야 한다면, `fromStorageDisk` 메서드를 사용할 수도 있습니다:

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

`fromData` 첨부 메서드는 바이트로 이루어진 원시 문자열 데이터를 첨부파일로 직접 추가할 때 사용합니다. 예를 들어, 메모리 내에서 PDF를 생성한 뒤 디스크에 별도로 저장하지 않고 이메일에 바로 첨부하고 싶을 때 이 방법을 사용할 수 있습니다. `fromData` 메서드는 첨부될 원시 데이터를 반환하는 클로저와 첨부파일 이름을 인수로 받습니다.

```php
/**
 * 메시지에 대한 첨부파일을 반환합니다.
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

이메일에 이미지를 인라인으로 삽입하는 작업은 보통은 복잡하지만, 라라벨에서는 이미지를 쉽게 첨부할 수 있도록 편리한 방법을 제공합니다. 인라인 이미지를 삽입하려면, 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. 라라벨은 모든 이메일 템플릿에 `$message` 변수를 자동으로 제공하므로 별도로 전달할 필요가 없습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메시지(plain-text) 템플릿에서는 사용할 수 없습니다. 일반 텍스트 메시지는 인라인 첨부파일을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 첨부파일 인라인 삽입

이메일 템플릿에 삽입하고 싶은 이미지 데이터가 원시 데이터 문자열로 이미 존재한다면, `$message` 변수의 `embedData` 메서드를 호출하면 됩니다. 이때, 삽입할 이미지에 부여할 파일명을 지정해주어야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

메시지에 파일 경로만 지정해서 파일을 첨부하는 방식이 간단할 때도 있지만, 실제 애플리케이션에서는 '첨부 가능한' 엔티티가 별도의 클래스로 표현되는 경우가 많습니다. 예를 들어, 사진을 메시지에 첨부한다면, 해당 사진을 나타내는 `Photo` 모델이 있을 수 있습니다. 이럴 때 `attach` 메서드에 `Photo` 모델 인스턴스를 바로 전달할 수 있다면 훨씬 편리하겠죠? Attachable 객체를 통해 이 작업이 가능합니다.

Attachable 객체를 만들기 위해서는 해당 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다. 이 인터페이스는 클래스에 `toMailAttachment` 메서드를 정의하도록 요구하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 모델의 첨부파일 표현을 반환합니다.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

Attachable 객체를 정의했다면, 이메일을 생성할 때 `attachments` 메서드에서 해당 객체 인스턴스를 그대로 반환할 수 있습니다.

```php
/**
 * 메시지에 대한 첨부파일을 반환합니다.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

물론, 첨부파일 데이터가 Amazon S3와 같은 원격 파일 스토리지 서비스에 저장되어 있을 수도 있습니다. 라라벨은 애플리케이션의 [파일시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 통해서도 첨부파일 인스턴스를 생성할 수 있도록 지원합니다.

```php
// 기본 디스크에서 파일로 첨부파일 인스턴스 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일로 첨부파일 인스턴스 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 존재하는 데이터를 이용해 첨부파일 인스턴스를 생성할 수도 있습니다. 이를 위해 `fromData` 메서드에 클로저를 전달하면 됩니다. 클로저는 첨부파일의 원시 데이터를 반환해야 합니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

라라벨은 첨부파일을 커스터마이즈할 수 있는 다양한 추가 메서드도 지원합니다. 예를 들어, `as`와 `withMime` 메서드를 사용해 파일명을 변경하거나, MIME 타입을 지정할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 설정

경우에 따라서는 발송하는 메시지에 추가 헤더를 첨부해야 할 수도 있습니다. 예를 들어, 커스텀 `Message-Id` 헤더나 기타 텍스트 기반의 임의 헤더를 지정하고 싶을 때가 있습니다.

이럴 땐, mailable 클래스에 `headers` 메서드를 정의하면 됩니다. `headers` 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 합니다. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받을 수 있으며, 필요한 항목만 선택적으로 전달하면 됩니다.

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

Mailgun, Postmark와 같은 일부 서드파티 이메일 서비스 제공자는 메시지 "태그(tags)"와 "메타데이터(metadata)"를 지원하며, 이를 통해 발송된 이메일을 그룹화하거나 추적할 수 있습니다. `Envelope` 정의에서 태그와 메타데이터를 손쉽게 추가할 수 있습니다.

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 봉투(envelope)를 반환합니다.
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

Mailgun 드라이버를 사용할 경우, Mailgun의 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages) 문서를 참고하실 수 있습니다. 마찬가지로, Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)에 대한 문서도 참고 가능합니다.

Amazon SES를 이용해 이메일을 발송하는 경우, 메시지에 [SES의 "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부하려면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

라라벨의 메일 기능은 Symfony Mailer를 기반으로 동작합니다. 라라벨에서는 메시지를 전송하기 바로 직전에 Symfony Message 인스턴스에 접근하고 커스터마이즈할 수 있도록, 사용자 정의 콜백을 등록하는 기능을 제공합니다. 이를 위해 `Envelope` 정의에 `using` 매개변수를 지정하면 됩니다.

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지 봉투(envelope)를 반환합니다.
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
## Markdown 메일러블

Markdown 메일러블 메시지는 [메일 알림](/docs/12.x/notifications#mail-notifications)에서 제공하는 미리 만들어진 템플릿과 컴포넌트의 혜택을 메일러블에서 그대로 사용할 수 있도록 해줍니다. 메시지는 Markdown으로 작성되기 때문에, 라라벨은 메일에 대해 아름답고 반응형인 HTML 템플릿을 렌더링하며, 동시에 plain-text 버전도 자동으로 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### Markdown 메일러블 생성

Markdown 템플릿이 포함된 메일러블을 생성하려면, Artisan의 `make:mail` 명령어에서 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그런 다음, 메일러블 클래스의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용하여 `Content` 정의를 구성합니다.

```php
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지의 내용 정의를 반환합니다.
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
### Markdown 메시지 작성

Markdown 메일러블은 Blade 컴포넌트와 Markdown 문법을 함께 사용할 수 있게 해줍니다. 이를 통해 라라벨이 미리 만들어둔 이메일 UI 컴포넌트를 적극적으로 활용하면서 손쉽게 메일 메시지를 만들 수 있습니다.

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
> Markdown 이메일을 작성할 때는 들여쓰기를 과하게 사용하지 마십시오. Markdown 규칙에 따라, 들여쓰기가 많은 내용은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 만들어줍니다. `url`과 선택적 인자인 `color`를 인수로 받을 수 있습니다. 지원하는 색상은 `primary`, `success`, `error`입니다. 버튼 컴포넌트는 여러 개 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 배경색이 살짝 다른 패널로 강조해줍니다. 이 컴포넌트로 특정 텍스트 블록을 강조해서 보여줄 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 Markdown 테이블을 HTML 테이블로 변환해줍니다. Markdown 표 문법을 그대로 컴포넌트 내용으로 전달하면 됩니다. 컬럼 정렬은 기본 Markdown 표 문법과 동일하게 지원됩니다.

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

Markdown 메일 컴포넌트 전체를 애플리케이션으로 내보내서 원하는 대로 수정할 수 있습니다. 컴포넌트를 내보내기 위해서는 Artisan의 `vendor:publish` 명령어에서 `laravel-mail` 애셋 태그를 이용합니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 Markdown 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 복사됩니다. `mail` 디렉터리에는 `html`과 `text` 하위 디렉터리가 각각 HTML, 텍스트용 컴포넌트를 포함합니다. 이 파일들은 자유롭게 커스터마이즈하실 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보내고 나면 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. 이 파일의 CSS를 수정하면, 여러분의 스타일이 Markdown 메일 메시지의 HTML 버전에 인라인 CSS로 자동 적용됩니다.

라라벨의 Markdown 컴포넌트에 대해 완전히 새로운 테마를 구축하고 싶다면, `html/themes` 디렉터리에 새로운 CSS 파일을 추가하면 됩니다. 원하는 이름으로 저장한 후, 애플리케이션의 `config/mail.php` 설정 파일에서 `theme` 옵션을 새 테마 이름으로 맞추세요.

개별 메일러블에 대해 테마를 변경하고 싶다면, 해당 메일러블 클래스의 `$theme` 프로퍼티에 적용할 테마 이름을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송하기

메시지를 발송하려면 `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용합니다. `to` 메서드는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션 모두를 받을 수 있습니다. 객체나 컬렉션을 전달하는 경우, 해당 객체에 `email`과 `name` 속성이 존재하는지 확인해야 합니다. 수신자를 지정한 후, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하면 됩니다.

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
     * 주문을 발송합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문을 발송 처리...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

메일 발송 시 "to" 수신자만 지정할 필요는 없습니다. "to", "cc", "bcc" 수신자를 각각 메서드 체이닝으로 자유롭게 추가할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 발송

간혹 여러 수신자에게 메일을 보내고자 배열이나 컬렉션을 반복할 수 있는데, 주의할 점이 있습니다. `to` 메서드는 매번 추가하는 방식이기 때문에, 루프를 돌리면 이전까지의 모든 수신자에게도 동일한 메시지가 반복해서 발송될 수 있습니다. 그러므로 반드시 각 수신자마다 새로운 메일러블 인스턴스를 생성해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 발송

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에서 `default`로 지정된 메일러 설정을 사용해 이메일을 발송합니다. 그러나, `mailer` 메서드를 활용해 특정 메일러 설정을 통해 메시지를 발송할 수도 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐 처리

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐에 보내기

이메일 발송은 애플리케이션의 응답 속도를 저하시킬 수 있기 때문에, 많은 개발자들이 메일을 백그라운드에서 처리되도록 큐에 등록하는 방식을 택합니다. 라라벨에서는 자체 [큐 API](/docs/12.x/queues)를 통해 쉽게 메일 메시지를 백그라운드 큐에 보낼 수 있습니다. 메시지 수신자를 지정한 후, `Mail` 파사드의 `queue` 메서드를 사용하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 방식은 메시지 발송을 별도의 작업(job)으로 큐에 등록해 백그라운드에서 처리합니다. 이 기능을 사용하기 전에는 [큐 설정](/docs/12.x/queues)이 완료되어 있어야 합니다.

<a name="delayed-message-queueing"></a>
#### 발송 지연(Delay) 설정

큐에 등록한 이메일의 발송 시점을 지연시키고 싶을 때는 `later` 메서드를 사용할 수 있습니다. 첫 번째 인수로는 메시지를 발송할 시점을 나타내는 `DateTime` 인스턴스를 넣으면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/커넥션 지정

`make:mail` 명령어로 생성되는 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 기본적으로 포함합니다. 즉, `onQueue` 및 `onConnection` 메서드를 통해 작업이 들어갈 큐 또는 커넥션을 임의로 지정할 수 있습니다.

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
#### 항상 큐 사용하기

특정 메일러블 클래스를 항상 큐를 이용해 처리하고 싶다면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이렇게 하면, 명시적으로 `send` 메서드를 호출하더라도 실제로는 항상 큐에 등록되어 처리됩니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉 메일러블과 DB 트랜잭션

DB 트랜잭션 내부에서 큐에 등록된 메일러블이 큐에서 즉시 처리되는 경우, 트랜잭션이 아직 커밋되기 전이기 때문에 모델이나 데이터가 아직 DB에 반영되지 않았을 수 있습니다. 따라서, 트랜잭션 내에서 생성되거나 수정된 데이터에 의존하는 메일러블에서는 예상치 못한 오류가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정값이 `false`라면, 특정 메일러블만 트랜잭션 커밋 이후에 큐에 등록되도록 하고 싶을 때는, 메시지 발송 시 `afterCommit` 메서드를 호출하십시오.

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
     * 새로운 메시지 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이 문제를 다루는 더 자세한 내용은 [큐잉 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고해 주세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 발송 실패 감지

큐에 등록된 이메일 발송이 실패하면, 해당 메일러블 클래스에 `failed` 메서드가 정의되어 있을 경우 이 메서드가 자동으로 호출됩니다. 이때, 발송 실패의 원인이 된 `Throwable` 인스턴스가 인수로 전달됩니다.

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
     * 큐잉된 이메일 발송 실패 처리.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링

경우에 따라 메일을 실제로 보내지 않고, 단순히 메일러블의 HTML 내용을 문자열로 받아오고 싶을 때가 있습니다. 이런 경우, 메일러블의 `render` 메서드를 호출하면, 렌더링된 HTML이 문자열로 반환됩니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 미리보기

메일러블 템플릿을 디자인할 때, Blade 템플릿처럼 결과물을 브라우저에서 바로 볼 수 있다면 매우 편리합니다. 라라벨은 라우트 클로저(route closure)나 컨트롤러에서 메일러블을 반환하면, 브라우저에서 그 내용을 바로 렌더링해줍니다. 이를 통해 실제 이메일을 발송하지 않아도 빠르게 디자인을 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블의 다국어 지원

라라벨은 메일을 발송할 때, 현재 요청의 로케일(locale)과 다른 언어로도 발송할 수 있으며, 큐에 등록된 메일 메시지 역시 해당 로케일이 보존됩니다.

이를 위해 `Mail` 파사드는 원하는 언어를 지정하는 `locale` 메서드를 제공합니다. 메일러블의 템플릿을 렌더링할 때만 지정한 로케일로 전환하고, 렌더링이 끝나면 자동으로 이전 로케일로 복구됩니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 언어 사용

애플리케이션에서 사용자마다 선호하는 언어를 저장하는 경우가 많습니다. 이럴 때, 모델에 `HasLocalePreference` 계약(Contract)을 구현하면, 메일 발송 시 자동으로 저장된 선호 로케일을 사용하도록 라라벨에 지시할 수 있습니다.

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

이 인터페이스를 구현하면, 라라벨은 해당 모델에 메일러블이나 알림을 보낼 때 자동으로 선호 언어를 적용합니다. 이 경우에는 별도로 `locale` 메서드를 호출할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>

## 테스트

<a name="testing-mailable-content"></a>
### 메일러블(Mailable) 콘텐츠 테스트

라라벨은 메일러블의 구조를 검사할 수 있는 다양한 메서드를 제공합니다. 또한, 메일러블이 기대하는 콘텐츠를 포함하고 있는지 확인할 수 있는 여러 편리한 테스트 메서드도 제공합니다. 사용 가능한 메서드는 다음과 같습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk`.

예상할 수 있듯, "HTML"로 끝나는 어서션은 메일러블의 HTML 버전에 특정 문자열이 포함되어 있는지 검사하고, "text" 어서션은 메일러블의 평문 텍스트 버전에 특정 문자열이 포함되어 있는지 검사합니다.

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

메일러블의 콘텐츠 테스트와, 특정 사용자가 "메일러블을 전송받았다"는 것을 검증하는 테스트는 별도로 작성하는 것을 권장합니다. 일반적으로, 실제로 테스트하려는 코드의 맥락에서는 메일러블의 내부 콘텐츠 자체는 중요하지 않고, 라라벨이 특정 메일러블을 전송하도록 지시받았는지만 검증해도 충분합니다.

실제로 이메일이 전송되는 것을 막고 싶다면 `Mail` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Mail::fake()`를 호출한 후에는, 어떤 메일러블이 어떤 사용자에게 전송되었는지 어서션할 수 있으며, 해당 메일러블에 전달된 데이터도 검사할 수 있습니다.

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 발송 작업 실행...

    // 어떤 메일러블도 전송되지 않았는지 검증...
    Mail::assertNothingSent();

    // 특정 메일러블이 전송되었는지 검증...
    Mail::assertSent(OrderShipped::class);

    // 메일러블이 두 번 전송되었는지 검증...
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일 주소로 전송되었는지 검증...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 여러 이메일 주소로 전송되었는지 검증...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 메일러블이 전송되지 않았는지 검증...
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3개의 메일러블이 전송되었는지 검증...
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

        // 주문 발송 작업 실행...

        // 어떤 메일러블도 전송되지 않았는지 검증...
        Mail::assertNothingSent();

        // 특정 메일러블이 전송되었는지 검증...
        Mail::assertSent(OrderShipped::class);

        // 메일러블이 두 번 전송되었는지 검증...
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 이메일 주소로 전송되었는지 검증...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // 여러 이메일 주소로 전송되었는지 검증...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // 메일러블이 전송되지 않았는지 검증...
        Mail::assertNotSent(AnotherMailable::class);

        // 총 3개의 메일러블이 전송되었는지 검증...
        Mail::assertSentCount(3);
    }
}
```

만약 메일러블을 백그라운드 큐에 등록해 전송하고 있다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued`와 같은 메서드에는 클로저를 전달해, 원하는 조건을 만족하는(일명 "진위 테스트"를 통과하는) 메일러블이 실제로 전송되었는지 어서션할 수 있습니다. 해당 조건을 만족하는 메일러블이 하나라도 전송되었다면 어서션은 성공합니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드 어서션 메서드에 전달되는 메일러블 인스턴스는, 메일러블을 다양한 방식으로 검사할 수 있는 여러 편리한 메서드를 제공합니다.

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

메일러블 인스턴스에는 첨부파일을 검사할 수 있는 다양한 메서드도 포함되어 있습니다.

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

메일이 전송되지 않았는지를 어서션할 때는 `assertNotSent`와 `assertNotQueued` 두 가지 방법이 있습니다. 어떤 경우에는, "메일이 전송되지도 않고 큐에도 오르지 않았다"는 점까지 검증하고 싶을 수 있습니다. 이럴 때는 `assertNothingOutgoing` 또는 `assertNotOutgoing` 메서드를 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

이메일을 발송하는 애플리케이션을 개발할 때, 실제로 라이브 환경의 이메일 주소로 메일을 보내고 싶지 않을 경우가 많습니다. 라라벨은 로컬 개발 환경에서 실제 메일 전송을 "비활성화"할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그(Log) 드라이버

이메일을 전송하는 대신, `log` 메일 드라이버는 모든 이메일 메시지를 검사할 수 있도록 로그 파일에 기록합니다. 일반적으로 이 드라이버는 로컬 개발 환경에서만 사용합니다. 환경별 애플리케이션 설정 방법에 대해서는 [설정 관련 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

다른 방법으로, [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 서비스, 그리고 `smtp` 드라이버를 사용하여 이메일 메시지를 "더미" 메일박스로 보낼 수 있습니다. 실제 이메일 클라이언트에서 해당 메시지를 확인할 수 있어, 최종적으로 발송되는 이메일이 정확히 어떻게 보이는지 Mailtrap의 메시지 뷰어 등으로 직접 확인할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용 중이라면 [Mailpit](https://github.com/axllent/mailpit)을 이용해 메시지를 미리볼 수도 있습니다. Sail이 실행 중이라면 다음 주소에서 Mailpit 인터페이스를 열 수 있습니다: `http://localhost:8025`

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 사용하여 전역적으로 모든 메일의 수신 주소를 지정할 수도 있습니다. 일반적으로 이 메서드는 애플리케이션 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출하면 됩니다.

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

라라벨은 메일 메시지를 전송할 때 두 개의 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지가 실제로 전송되기 **직전에** 발생하며, `MessageSent` 이벤트는 메시지가 전송 **완료된 후** 발생합니다. 이 이벤트들은 메일이 *실제로 전송될 때* 발생하며, 큐에만 등록된 경우에는 발생하지 않습니다. 애플리케이션에서 이 이벤트들을 위한 [이벤트 리스너](/docs/12.x/events)를 직접 만들어 사용할 수 있습니다.

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * 이벤트 처리기
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## 사용자 정의 메일 전송(Transport) 만들기

라라벨에는 다양한 메일 전송 방식(트랜스포트)이 내장되어 있습니다. 하지만 라라벨이 기본적으로 지원하지 않는 외부 서비스로 이메일을 전송하고 싶은 경우, 직접 트랜스포트를 구현할 수 있습니다. 이를 위해, 먼저 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 클래스를 만듭니다. 그리고 `doSend` 및 `__toString()` 메서드를 구현합니다.

```php
use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * 새로운 Mailchimp 트랜스포트 인스턴스 생성자
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
     * 트랜스포트의 문자열 표현 반환
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

사용자 정의 트랜스포트를 정의했다면, 이제 `Mail` 파사드의 `extend` 메서드를 사용해 등록할 수 있습니다. 일반적으로 이 과정은 애플리케이션의 `AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 진행합니다. `extend` 메서드에 전달되는 클로저에는 `$config` 인자가 제공되며, 이는 애플리케이션의 `config/mail.php` 파일에 정의된 해당 메일러의 설정 배열입니다.

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

트랜스포트가 정의되고 등록되었다면, 이제 애플리케이션의 `config/mail.php` 설정 파일에서 이 트랜스포트를 사용하는 메일러를 정의해 사용할 수 있습니다.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트 사용

라라벨은 Mailgun, Postmark와 같은 기존에 Symfony에서 관리하는 일부 트랜스포트도 기본적으로 지원합니다. 만약 이외의 추가 Symfony 트랜스포트를 사용하고 싶다면, Composer로 해당 Symfony 메일러를 설치하고 라라벨에 직접 등록할 수 있습니다. 예를 들어, "Brevo"(이전 명칭: Sendinblue) Symfony 메일러를 설치하고 등록할 수 있습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지가 설치되었다면, 애플리케이션의 `services` 설정 파일에 Brevo API 인증 정보를 입력하세요.

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

그 다음, `Mail` 파사드의 `extend` 메서드를 사용해 라라벨에 트랜스포트를 등록합니다. 이 작업은 보통 서비스 프로바이더의 `boot` 메서드에서 수행합니다.

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

이제 트랜스포트가 등록되었으니, `config/mail.php` 설정 파일에서 새로운 트랜스포트를 사용하는 메일러를 추가해 사용할 수 있습니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```