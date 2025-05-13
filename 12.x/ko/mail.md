# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [메일러블 클래스 생성](#generating-mailables)
- [메일러블 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
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
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 현지화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. 라라벨은 유명한 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 하는 깔끔하고 단순한 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 통한 이메일 전송을 위한 드라이버를 제공하므로, 로컬 또는 클라우드 기반의 원하는 서비스로 빠르게 메일을 보내기 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

라라벨의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 설정합니다. 이 파일에 정의된 각 메일러(mailers)는 고유한 설정 값과 "트랜스포트(transport)"를 가질 수 있으므로, 애플리케이션에서 여러 이메일 서비스를 각각 다르게 활용하여 특정 메일 메시지를 전송할 수 있습니다. 예를 들어, 트랜잭션(거래)성 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일에는 `mailers` 설정 배열이 있습니다. 이 배열에는 라라벨이 지원하는 대표적인 메일 드라이버/트랜스포트에 대한 샘플 설정 값이 포함되어 있으며, `default` 설정 값은 애플리케이션에서 이메일을 전송할 때 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/트랜스포트 사전 요구사항

Mailgun, Postmark, Resend, MailerSend와 같이 API 기반의 드라이버들은 일반적으로 SMTP 서버를 이용한 전송보다 더 간단하고 빠릅니다. 가능한 한 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지 변경이 필요합니다. 첫 번째로, 기본 메일러를 `mailgun`으로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

두 번째로, 아래와 같이 `mailers` 배열에 `mailgun` 설정을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정한 후에는 `config/services.php` 설정 파일에 다음 옵션을 추가해야 합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 Mailgun 리전이 아닌 다른 [Mailgun 지역](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 이용한다면, `services` 설정 파일에서 해당 지역의 엔드포인트를 지정할 수 있습니다:

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

설치 후, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 지정하세요. 이후 기본 메일러가 설정되면, `config/services.php` 설정 파일에 아래 옵션이 포함되어 있는지 반드시 확인합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하려면, mailer의 설정 배열에 `message_stream_id` 설정 값을 추가할 수 있습니다. 이 배열은 `config/mail.php` 설정 파일에서 찾을 수 있습니다:

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

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer를 통해 Resend의 PHP SDK를 설치해야 합니다:

```shell
composer require resend/resend-php
```

설치 후, `config/mail.php` 설정 파일에서 `default` 옵션을 `resend`로 지정하세요. 기본 메일러 설정이 끝나면, `config/services.php` 설정 파일에 아래 옵션이 포함되어 있는지 확인합니다:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 먼저 PHP용 Amazon AWS SDK를 설치해야 합니다. 이 라이브러리는 Composer로 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

설치 후, `config/mail.php` 설정 파일에서 `default` 옵션을 `ses`로 지정하고, `config/services.php` 설정 파일에 아래와 같은 옵션이 있는지 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰을 통해 사용하려면 SES 설정에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환되는 배열에 `X-Ses-List-Management-Options` 헤더를 추가할 수 있습니다:

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

이메일을 보낼 때 라라벨이 AWS SDK의 `SendEmail` 메서드로 전달해야 할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)이 있다면, `ses` 설정 내에 `options` 배열을 정의할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스를 제공하며, 라라벨을 위한 자체 API 기반 메일 드라이버를 제공합니다. 이 드라이버 패키지는 Composer를 사용해서 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

패키지 설치가 완료되면, 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 그리고 `MAIL_MAILER` 환경 변수는 `mailersend`로 지정해야 합니다:

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

호스팅된 템플릿 사용법 등 MailerSend에 대한 더 많은 내용을 알고 싶다면 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정

외부 서비스에 메일 전송을 맡겼는데 해당 서비스가 다운되는 경우가 있을 수 있습니다. 이런 상황에서는, 기본 전송 드라이버에 장애가 발생했을 때를 대비하여 하나 이상의 백업 메일 전송 설정을 정의할 수 있습니다.

이를 위해서는 애플리케이션의 `mail` 설정 파일에서 `failover` 트랜스포트를 사용하는 메일러를 정의하면 됩니다. 이때 `failover` 메일러에 대한 설정 배열에는 실제 전송에 사용할 메일러의 우선순위가 지정된 `mailers` 배열이 포함되어야 합니다:

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

장애 조치 메일러를 정의한 뒤에는, 이 메일러 이름을 애플리케이션의 `mail` 설정 파일 내 `default` 설정 키에 지정하여 애플리케이션이 사용할 기본 메일러로 설정해야 합니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈 설정

`roundrobin` 트랜스포트를 사용하면 여러 메일러에 메일 전송 작업을 분산시킬 수 있습니다. 사용을 시작하려면, 애플리케이션의 `mail` 설정 파일에서 `roundrobin` 트랜스포트를 사용하는 메일러를 정의해야 합니다. 이때 라운드 로빈 메일러의 설정 배열에는 실제 전송에 사용할 메일러의 목록이 지정된 `mailers` 배열이 포함되어야 합니다:

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

라운드 로빈 메일러를 정의한 뒤에는, 이 이름을 기본 메일러로 지정해줍니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 트랜스포트는 구성된 메일러 목록에서 무작위로 하나를 선택한 뒤, 이후 메일 전송마다 다음 메일러로 순차적으로 전환됩니다. 이는 장애 조치(`failover`) 트랜스포트가 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)* 확보에 도움을 준다면, 라운드 로빈(`roundrobin`) 트랜스포트는 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 클래스 생성

라라벨 애플리케이션을 개발할 때, 여러분이 전송하는 각 유형의 이메일은 "메일러블(mailable)" 클래스 형태로 구현하게 됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 애플리케이션에서 이 디렉터리가 보이지 않는다면 걱정하지 않아도 됩니다. `make:mail` 아티즌 명령어로 첫 번째 메일러블 클래스를 만들면, 해당 디렉터리가 자동으로 생성됩니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 클래스 작성

메일러블 클래스를 생성했다면, 파일을 열어서 그 내용을 살펴보겠습니다. 메일러블 클래스의 설정은 주로 `envelope`, `content`, `attachments` 등의 여러 메서드에서 이루어집니다.

`envelope` 메서드는 메시지의 제목(subject)과 경우에 따라 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문을 생성할 때 사용되는 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope를 이용한 발신자 설정

우선, 이메일의 발신자 — 즉, 이메일이 "누구로부터" 보내지는지 — 를 설정하는 방법을 살펴봅니다. 발신자 설정 방법은 두 가지가 있습니다. 첫 번째로, 메시지의 envelope(봉투)에 "from" 주소를 지정하는 방법입니다:

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

그리고 필요하다면 `replyTo` 주소도 지정할 수 있습니다:

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

애플리케이션에서 모든 이메일을 동일한 "from" 주소로 보낸다면, 매번 메일러블 클래스를 생성할 때마다 이를 지정하는 것이 번거로울 수 있습니다. 이럴 땐, `config/mail.php` 설정 파일에 글로벌 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 별도로 "from" 주소를 지정하지 않을 경우, 이 글로벌 주소가 자동으로 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, `config/mail.php` 파일에서 글로벌 "reply_to" 주소도 정의할 수 있습니다:

```php
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드에서는 이메일 본문을 렌더링할 때 사용할 `view`(템플릿)를 지정할 수 있습니다. 각 이메일은 주로 [Blade 템플릿](/docs/12.x/blade)을 사용하여 내용을 렌더링하므로, 라라벨의 강력하고 편리한 Blade 템플릿 엔진을 그대로 활용할 수 있습니다:

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
> 모든 이메일 템플릿을 보관할 `resources/views/emails` 디렉터리를 별도로 만들어 관리하는 것이 좋습니다. 물론, `resources/views` 내에 원하는 위치에 자유롭게 배치해도 괜찮습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하고 싶다면 메시지의 `Content` 정의 시 plain-text 템플릿을 지정할 수 있습니다. `view` 파라미터와 마찬가지로, `text` 파라미터 역시 이메일 내용을 렌더링할 템플릿 이름을 지정합니다. HTML과 plain-text 버전의 메시지를 모두 정의할 수 있습니다:

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

좀 더 명확하게 작성하려면, `html` 파라미터를 `view` 파라미터의 별칭으로 사용할 수도 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 프로퍼티를 통한 전달

일반적으로 이메일의 HTML을 렌더링할 때 사용할 데이터를 뷰(View)로 전달하고 싶을 것입니다. 이 데이터를 전달하는 방법은 두 가지입니다. 첫 번째는, 메일러블 클래스에 정의된 public 프로퍼티(public property)를 통해 데이터를 전달하는 것입니다. 예를 들어, 생성자에서 데이터를 받아 해당 클래스를 public 속성에 할당하면 됩니다:

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

이렇게 public 프로퍼티에 데이터를 할당하면, 해당 데이터는 자동으로 뷰에서 사용 가능해지므로 일반 Blade 템플릿 데이터를 다루듯 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

템플릿에 데이터를 전달하기 전에 직접 데이터를 가공해서 넘기고 싶다면, `Content` 정의의 `with` 파라미터를 사용하여 데이터를 수동으로 뷰에 전달할 수 있습니다. 일반적으로, 데이터는 여전히 메일러블 클래스의 생성자에 전달하지만, 데이터를 public이 아닌 protected나 private 속성으로 저장해두면 템플릿에 자동으로 노출되지 않습니다:

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

데이터가 `with`에 지정되면, 뷰에서 Blade 템플릿 데이터처럼 자유롭게 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드가 반환하는 배열에 첨부 파일을 추가하면 됩니다. 먼저, `Attachment` 클래스가 제공하는 `fromPath` 메서드에 파일 경로를 지정해서 첨부 파일을 추가할 수 있습니다:

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

파일을 첨부하면서 파일의 표시 이름이나 MIME 타입을 함께 지정하고 싶다면 `as` 및 `withMime` 메서드를 사용할 수 있습니다:

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
#### 파일시스템 디스크에서 파일 첨부

[파일 시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 이메일에 첨부하고 싶다면, `fromStorage` 첨부 메서드를 사용할 수 있습니다:

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

물론, 첨부 파일의 이름이나 MIME 타입도 지정할 수 있습니다:

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

기본 디스크가 아닌 다른 저장소 디스크를 지정하려면 `fromStorageDisk` 메서드를 사용할 수 있습니다:

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

`fromData` 첨부 메서드를 사용하면 바이트의 원시 문자열 데이터를 첨부파일로 추가할 수 있습니다. 예를 들어, 메모리 내에서 PDF를 생성하고 이를 디스크에 저장하지 않고 이메일에 첨부하고 싶을 때 이 방법을 사용할 수 있습니다. `fromData` 메서드는 첨부할 데이터의 바이트 원시값을 반환하는 클로저와 첨부파일로 지정할 이름을 인수로 받습니다.

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

이메일에 인라인 이미지를 삽입하는 것은 일반적으로 번거로운 작업입니다. 하지만 라라벨에서는 이미지를 이메일에 손쉽게 첨부할 수 있는 편리한 방법을 제공합니다. 인라인 이미지를 삽입하려면 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. 라라벨은 모든 이메일 템플릿에서 `$message` 변수를 자동으로 사용할 수 있게 해주므로, 별도의 전달 작업이 필요하지 않습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메시지 템플릿에서는 사용할 수 없습니다. 일반 텍스트 메시지는 인라인 첨부파일 기능을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 첨부파일 임베딩

인라인으로 삽입할 이미지를 원시 데이터 문자열로 이미 보유하고 있다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이 메서드 사용 시, 첨부될 이미지의 파일명을 반드시 인수로 넘겨주어야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한(Attachable) 객체

단순한 문자열 경로를 통해 파일을 첨부하는 것만으로도 충분한 경우가 많지만, 실제 애플리케이션에서는 첨부하고자 하는 대상을 클래스로 표현한 경우가 많습니다. 예를 들어, 애플리케이션이 메시지에 사진을 첨부한다면, 그 사진을 나타내는 `Photo` 모델을 보유하고 있을 수도 있습니다. 이럴 때, `attach` 메서드에 `Photo` 모델을 편리하게 바로 전달할 수 있다면 좋지 않을까요? Attachable 객체를 사용하면 이를 손쉽게 구현할 수 있습니다.

시작하려면, 첨부 가능한 객체 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다. 이 인터페이스는 클래스가 `Illuminate\Mail\Attachment` 인스턴스를 반환하는 `toMailAttachment` 메서드를 정의하도록 요구합니다.

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

이렇게 attachable 객체를 정의한 후, 이메일 메시지를 생성하며 `attachments` 메서드에서 해당 객체의 인스턴스를 반환할 수 있습니다.

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

물론, 첨부파일 데이터가 Amazon S3 같은 원격 파일 저장소에 저장되어 있을 수도 있습니다. 라라벨에서는 애플리케이션의 [파일시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 이용해서도 쉽게 첨부파일 인스턴스를 만들 수 있습니다.

```php
// 기본 디스크에 있는 파일로 첨부파일 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에 있는 파일로 첨부파일 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

추가로, 메모리에 보관 중인 데이터로도 첨부파일 인스턴스를 만들 수 있습니다. 이를 위해서는 `fromData` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 첨부파일의 원시 데이터를 반환해야 합니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

라라벨은 첨부파일을 커스터마이즈할 수 있는 다양한 메서드도 제공합니다. 예를 들어, 파일의 이름과 MIME 타입을 지정할 때 `as`와 `withMime` 메서드를 사용할 수 있습니다.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

가끔은 발송되는 이메일 메시지에 추가적인 헤더가 필요할 수 있습니다. 예를 들어, 커스텀 `Message-Id` 를 설정하거나 임의의 텍스트 헤더를 추가해야 할 수도 있습니다.

이럴 땐, mailable 클래스에 `headers` 메서드를 정의합니다. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 합니다. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받으며, 필요에 따라 원하는 항목만 선택해서 제공할 수 있습니다.

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
### 태그(Tag)와 메타데이터(Metadata)

Mailgun, Postmark와 같은 일부 서드파티 이메일 제공업체는 메시지 "태그"와 "메타데이터" 기능을 지원합니다. 이를 활용하면 애플리케이션에서 발송한 이메일을 그룹화하고 추적할 수 있습니다. 태그와 메타데이터는 `Envelope` 정의에 추가하면 됩니다.

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

만약 Mailgun 드라이버를 사용 중이라면, 자세한 내용은 Mailgun의 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages) 문서를 참고하세요. Postmark 드라이버를 사용할 경우에도 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 문서를 참고할 수 있습니다.

Amazon SES로 이메일을 전송하는 경우에는, `metadata` 메서드를 사용하여 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

라라벨의 메일 시스템은 Symfony Mailer를 기반으로 동작합니다. 라라벨에서는 메시지 전송 전, Symfony의 Message 인스턴스를 커스터마이즈할 수 있도록 커스텀 콜백을 등록할 수 있습니다. 이를 통해 발송 전 메시지를 세부적으로 수정할 수 있습니다. 구현하려면 `Envelope` 정의에 `using` 파라미터를 지정하세요.

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

마크다운 메일러블 메시지를 사용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)의 사전 제작된 템플릿과 컴포넌트를 메일러블에서도 활용할 수 있습니다. 메시지가 마크다운 문법으로 작성되기 때문에, 라라벨은 아름답고 반응형인 HTML 템플릿을 자동으로 렌더링하면서, 동시에 일반 텍스트 버전도 자동 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성

마크다운 템플릿과 함께 메일러블을 생성하려면 `make:mail` 아티즌 명령어에 `--markdown` 옵션을 사용하면 됩니다.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그리고 메일러블의 `content` 메서드 안에서 메시지의 Content 정의를 구성할 때, `view` 파라미터 대신에 `markdown` 파라미터를 사용하세요.

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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 조합하여 사용합니다. 이를 통해 라라벨이 제공하는 사전 제작된 이메일 UI 컴포넌트를 활용하여 손쉽게 메일 메시지를 작성할 수 있습니다.

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
> 마크다운 이메일 작성 시 들여쓰기를 과하게 사용하지 마세요. 마크다운 표준에 따라, 마크다운 파서가 들여쓰인 내용은 코드 블록으로 렌더링합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 필수 인수인 `url`과, 선택적으로 버튼의 색상을 지정하는 `color` 인수를 받습니다. 지원되는 색상은 `primary`, `success`, `error`입니다. 버튼 컴포넌트는 한 메시지 내에 여러 번 사용할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 특정 블록의 텍스트를 메시지 내 다른 영역보다 약간 다른 배경색의 패널로 감싸 보여줍니다. 이를 통해 사용자의 관심을 특정 부분에 집중시킬 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 마크다운 테이블을 내용으로 전달받으며, 컬럼 정렬도 마크다운 표준 문법에 따라 지원됩니다.

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

마크다운 메일 컴포넌트를 프로젝트 내에 직접 추출해 수정하고 싶다면, `vendor:publish` 아티즌 명령어를 사용하여 `laravel-mail` 에셋 태그를 퍼블리시하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 마크다운 메일 컴포넌트들이 `resources/views/vendor/mail` 디렉터리에 복사됩니다. `mail` 디렉터리에는 각각의 컴포넌트별 HTML과 텍스트(view) 디렉터리가 포함되어 있습니다. 마음껏 원하는 대로 해당 컴포넌트 파일을 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보낸 후, `resources/views/vendor/mail/html/themes` 디렉터리에는 `default.css` 파일이 생성됩니다. 이 파일의 CSS 스타일을 자유롭게 수정하면, 해당 스타일이 마크다운 메일 메시지의 HTML 뷰에 자동으로 인라인 CSS로 반영됩니다.

라라벨의 마크다운 컴포넌트용으로 완전히 새로운 테마를 구축하고 싶다면, `html/themes` 디렉터리에 CSS 파일을 새로 추가하면 됩니다. 이 파일에 이름을 붙여 저장한 후, 애플리케이션의 `config/mail.php` 설정 파일에서 `theme` 옵션을 새로운 테마의 이름으로 변경하면 됩니다.

개별 메일러블에 대해 테마를 다르게 하고 싶다면, 메일러블 클래스의 `$theme` 속성에 사용할 테마명을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송

메시지를 전송하려면, [Mail 파사드](/docs/12.x/facades)의 `to` 메서드를 사용하세요. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 인스턴스 콜렉션을 받을 수 있습니다. 객체 또는 객체 컬렉션을 전달하면, 라라벨은 해당 객체의 `email`과 `name` 속성을 자동으로 참조해 수신자를 결정합니다. 이 속성들이 객체 내에 반드시 존재해야 합니다. 하나 이상의 수신자를 지정한 후, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하면 메일이 발송됩니다.

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

메일 발송 시 "to" 수신자만 지정할 필요는 없습니다. "to", "cc", "bcc"를 각각 지정하여 여러 방법으로 수신자를 추가할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자에게 반복적으로 발송하기

경우에 따라, 수신자 목록(이메일 주소 배열 등)을 순회하며 일일이 메일러블을 각각 발송해야 할 수도 있습니다. 하지만 `to` 메서드는 호출할 때마다 수신자 리스트에 이메일을 추가하므로, 반복문 안에서 메일러블 인스턴스를 계속 재사용하면 이전까지의 모든 수신자들에게 중복해서 메일이 발송됩니다. 따라서 반드시 각 반복마다 새로운 메일러블 인스턴스를 생성해 사용해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 통한 메일 발송

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에 지정된 `default` 메일러를 이용해 이메일을 보냅니다. 하지만 `mailer` 메서드를 이용하면 특정 메일러 구성으로 메일을 발송할 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉(Queueing)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐에 넣기

이메일 발송 작업은 애플리케이션의 응답 속도에 악영향을 줄 수 있으므로, 많은 개발자들은 이메일 메시지를 큐에 넣어 백그라운드에서 발송되게끔 합니다. 라라벨에서는 내장 [통합 큐 API](/docs/12.x/queues)를 통해 이 과정을 쉽게 처리할 수 있습니다. 메일 메시지를 큐잉하려면, `Mail` 파사드에서 수신자 설정 후 `queue` 메서드를 사용하면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 방식은 자동으로 큐에 작업이 추가되어 백그라운드에서 메일 발송이 진행됩니다. 이 기능을 사용하려면 [큐 설정](/docs/12.x/queues)을 반드시 미리 해두어야 합니다.

<a name="delayed-message-queueing"></a>
#### 메일 발송 지연(Delay) 큐잉

큐에 넣은 메일 메시지의 발송을 일정 시간 지연하고 싶다면, `later` 메서드를 사용할 수 있습니다. 이 메서드의 첫 번째 인수로는 메시지가 발송되어야 할 시점을 나타내는 `DateTime` 인스턴스를 전달하세요.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐(Queue)에 넣기

`make:mail` 명령어로 생성되는 모든 메일러블 클래스에는 `Illuminate\Bus\Queueable` 트레이트가 포함됩니다. 따라서, 메일러블 인스턴스에 대해 `onQueue`, `onConnection` 메서드를 호출해 메시지가 사용될 큐의 연결과 이름을 직접 지정할 수 있습니다.

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
#### 기본적으로 큐잉하도록 설정

특정 메일러블 클래스가 항상 큐잉되게 하고 싶다면, 해당 클래스에 `ShouldQueue` 계약을 구현하세요. 이제 `send` 메서드를 사용해도, 이 메일러블은 자동으로 큐에 넣어집니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐에 넣은 메일러블이 데이터베이스 트랜잭션 내에서 디스패치되는 경우, 큐 프로세스가 실제로 트랜잭션 커밋 전에 실행될 수 있습니다. 이럴 경우, 트랜잭션 중에 데이터베이스 레코드나 모델을 업데이트한 내용이 아직 커밋되지 않아, 큐에서 해당 내용을 읽지 못하게 될 수 있습니다. 또한 트랜잭션 내에서 새로 생성된 모델이나 레코드는 아직 DB에 존재하지 않을 수 있습니다. 만약 메일러블이 이 모델에 의존한다면, 예기치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 구성 옵션이 `false`로 되어 있는 경우, 특정 큐잉 메일러블을 모든 데이터베이스 트랜잭션 커밋 이후에 디스패치하고 싶다면, 메일 발송 시 `afterCommit` 메서드를 호출하세요.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또한 원하는 경우, 메일러블의 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
> 이러한 문제의 근본적인 원인과 해결책에 대해 더 알고 싶다면 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링

가끔 메일을 실제로 발송하지 않고, 메일러블의 HTML 콘텐츠만 추출(렌더링)해보고 싶을 때가 있습니다. 이럴 땐 메일러블의 `render` 메서드를 호출하면, 메일러블의 최종 HTML 콘텐츠가 문자열로 반환됩니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블의 템플릿을 디자인할 때, Blade 템플릿처럼 브라우저에서 빠르게 결과를 바로 확인할 수 있다면 편리하겠죠? 라라벨에서는 이를 위해 라우트 클로저나 컨트롤러 메서드에서 메일러블 자체를 반환할 수 있게 지원합니다. 이 경우 메일러블이 렌더되어 브라우저에 표시되므로, 실제 이메일 주소로 발송하지 않고도 디자인을 쉽고 빠르게 미리볼 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블의 다국어 지원(Localization)

라라벨에서는 요청의 기본 로케일과 다른 언어로 메일러블을 작성해 보낼 수 있습니다. 만약 메일이 큐에 들어가더라도 지정한 로케일 정보가 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드를 통해 원하는 언어를 지정할 수 있습니다. 메일러블의 템플릿이 렌더링될 때 임시로 해당 로케일로 전환되고, 렌더링이 끝나면 다시 원래 로케일로 돌아갑니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자별 선호 언어(로케일) 지원

애플리케이션에서 각 사용자의 선호 로케일을 저장하고 있다면, 한 모델에 `HasLocalePreference` 계약을 구현하여 저장된 로케일 정보를 기반으로 메일을 발송할 수 있습니다.

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

이 인터페이스를 구현한 후에는, 라라벨이 자동으로 해당 모델의 선호 로케일을 사용하여 메일러블 및 알림을 발송합니다. 따라서 이 인터페이스를 사용할 때는 별도로 `locale` 메서드를 호출할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

라라벨에서는 메일러블의 구조를 확인할 수 있는 다양한 메서드를 제공합니다. 또한, 메일러블에 기대한 내용이 실제로 포함되어 있는지 테스트할 수 있는 여러 편리한 assertion 메서드도 지원합니다. 대표적으로 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등이 있습니다.

이 중 "HTML" 관련 assertion들은 메일러블의 HTML 버전에 특정 문자열이 포함되어 있는지, "text" 관련 assertion들은 일반 텍스트 버전에 문자열이 포함되어 있는지를 검사합니다.

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

### 메일러블 전송 테스트하기

특정 메일러블이 실제로 "특정 사용자에게 전송"되었는지 검증하는 테스트와, 메일러블의 내용 자체를 검증하는 테스트는 별도로 작성하는 것을 권장합니다. 일반적으로, 메일러블의 구체적 내용은 여러분이 테스트하려는 코드와 직접적인 관련이 없는 경우가 많으며, 라라벨이 특정 메일러블을 전송하도록 지시받았는지만 확인해도 충분합니다.

메일이 실제로 발송되지 않도록 하려면 `Mail` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Mail::fake()`를 호출한 뒤에는, 어떤 메일러블이 어떤 사용자에게 전송되었는지 검증하거나, 메일러블이 받은 데이터를 직접 확인할 수 있습니다.

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

만약 메일러블을 백그라운드에서 큐잉하여 발송하고 있다면, `assertSent` 대신에 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에는 클로저를 전달하여, 특정 "조건에 맞는" 메일러블이 전송되었는지 검증할 수 있습니다. 주어진 조건을 만족하는 메일러블이 단 하나라도 전송되었다면 해당 검증은 성공합니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 검증 메서드에서 제공하는 클로저로 받은 메일러블 인스턴스는 다양한 정보 확인용 메서드를 제공합니다.

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

메일러블 인스턴스는 첨부파일을 검사하기 위한 메서드도 제공합니다.

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

메일이 전송되지 않았음을 검증하는 메서드는 `assertNotSent`와 `assertNotQueued`가 있습니다. 그러나 경우에 따라, "아무 메일도 전송 **또는** 큐잉되지 않았다"를 한 번에 검증하고 싶을 수 있습니다. 이때는 `assertNothingOutgoing`, `assertNotOutgoing` 메서드를 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

이메일을 발송하는 애플리케이션을 개발할 때는, 실제로 존재하는 이메일 주소로 메일이 발송되는 상황을 피하고 싶을 것입니다. 라라벨은 로컬 개발 중에 실제 이메일 전송을 "비활성화"하는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

이메일을 실질적으로 발송하는 대신, `log` 메일 드라이버를 사용하면 모든 이메일 메시지가 로그 파일에 기록되어 내용을 직접 확인할 수 있습니다. 일반적으로 이 드라이버는 로컬 개발 환경에서만 사용됩니다. 환경별로 애플리케이션을 설정하는 방법에 대해 더 많이 알고 싶다면 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또 다른 방법으로, [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io)과 같은 서비스를 `smtp` 드라이버와 함께 사용하여, 실제 이메일 발송 대신 메시지를 "가상의" 사서함으로 보내고, 이를 이메일 클라이언트에서 직접 확인할 수 있습니다. 이 방식의 장점은, Mailtrap의 메시지 뷰어에서 완성된 이메일을 실제로 확인할 수 있다는 데 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용한다면, [Mailpit](https://github.com/axllent/mailpit)을 이용해 메시지를 미리 볼 수 있습니다. Sail이 실행 중일 때는, `http://localhost:8025`에서 Mailpit 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 이용해 특정 이메일 주소로만 모든 메일이 발송되도록 전역 "to" 주소를 지정할 수 있습니다. 이 메서드는 보통 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출합니다.

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

라라벨은 메일 메시지를 전송하는 과정에서 두 개의 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지가 **전송되기 전**에 발생하고, `MessageSent` 이벤트는 메시지 **전송 후** 발생합니다. 참고로, 이 이벤트들은 메일이 *전송*될 때만 발생하며, *큐에 등록*될 때는 발생하지 않습니다. 애플리케이션에서 이 이벤트들을 위한 [이벤트 리스너](/docs/12.x/events)를 구현할 수 있습니다.

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

라라벨은 다양한 메일 트랜스포트를 기본 제공하지만, 지원하지 않는 다른 서비스로 이메일을 발송하고 싶을 때는 직접 트랜스포트를 구현할 수도 있습니다. 먼저, `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속한 클래스를 정의합니다. 그런 다음, 해당 트랜스포트에서 `doSend`와 `__toString()` 메서드를 구현하면 됩니다.

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

이제 커스텀 트랜스포트를 정의했다면, `Mail` 파사드의 `extend` 메서드를 통해 트랜스포트를 등록할 수 있습니다. 주로 애플리케이션의 `AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 이 작업을 수행합니다. `extend` 메서드에 전달하는 클로저에는 `$config` 인자가 전달되며, 이 값은 애플리케이션의 `config/mail.php` 설정 파일에 정의한 설정 배열입니다.

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

이렇게 커스텀 트랜스포트를 정의·등록한 후에는, `config/mail.php` 설정 파일에 해당 트랜스포트를 사용하는 메일러 정의를 추가할 수 있습니다.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

라라벨은 Mailgun, Postmark 등 Symfony에서 공식적으로 유지 관리하는 여러 메일 트랜스포트를 기본 지원합니다. 더 많은 Symfony 트랜스포트를 라라벨에서 활용하고 싶다면, Composer로 해당 Symfony 메일러 패키지를 설치하고, 라라벨에 직접 트랜스포트를 등록할 수 있습니다. 예를 들어 "Brevo"(이전 명칭: Sendinblue)용 Symfony 메일러를 설치하고 등록하는 방법은 아래와 같습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지를 설치한 뒤에는, 애플리케이션의 `services` 설정 파일에 Brevo API 자격증명을 추가합니다.

```php
'brevo' => [
    'key' => 'your-api-key',
],
```

그리고 `Mail` 파사드의 `extend` 메서드로 해당 트랜스포트를 라라벨에 등록합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 이 작업을 수행합니다.

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

트랜스포트를 등록한 후에는, 애플리케이션의 `config/mail.php` 설정 파일에 해당 트랜스포트를 사용하는 메일러를 정의하면 됩니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```