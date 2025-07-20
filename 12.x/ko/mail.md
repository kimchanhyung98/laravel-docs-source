# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [장애 조치(Failover) 설정](#failover-configuration)
    - [라운드로빈(Round Robin) 설정](#round-robin-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
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
    - [마크다운 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송하기](#sending-mail)
    - [메일 큐잉하기](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저로 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 현지화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일을 보내는 일은 결코 어렵지 않습니다. 라라벨은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 간결하고 쉬운 이메일 API를 제공합니다. 라라벨과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 메일 발송 드라이버를 기본적으로 제공하여, 로컬 혹은 클라우드 기반 서비스 중 원하는 방식을 빠르게 선택해 메일을 보낼 수 있습니다.

<a name="configuration"></a>
### 설정

라라벨의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 정의된 각각의 메일러별로 고유한 설정을 가질 수 있으며, 심지어 각각의 메일러가 서로 다른 "트랜스포트"를 사용할 수 있습니다. 덕분에 애플리케이션에서 특정 유형의 이메일은 서로 다른 이메일 서비스를 통해 발송할 수 있게 됩니다. 예를 들어 Postmark로 거래 관련 이메일을 보내고, Amazon SES로는 대량 이메일을 발송하는 식입니다.

`mail` 설정 파일 안에는 `mailers`라는 설정 배열이 있습니다. 이 배열은 라라벨이 지원하는 주요 메일 드라이버/트랜스포트별로 예시 설정 항목을 포함하고 있습니다. 한편, `default` 설정 값은 애플리케이션이 이메일을 보낼 때 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비사항

Mailgun, Postmark, Resend, MailerSend과 같이 API 기반으로 동작하는 드라이버들은 보통 SMTP 서버를 이용하는 것보다 더 간단하며 빠르게 작동합니다. 가능한 경우, 이 중 하나의 드라이버를 사용할 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지 수정을 진행합니다. 먼저, 기본 메일러를 `mailgun`으로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

두 번째로, `mailers` 배열에 아래 구성 배열을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션들을 추가합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 이외의 [Mailgun region](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용한다면, 해당 리전의 엔드포인트를 `services` 설정 파일에서 지정할 수 있습니다:

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

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 지정합니다. 기본 메일러 설정이 완료되었다면, `config/services.php` 설정 파일에 아래 항목들이 포함되어 있는지 확인합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하려면, 메일러의 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 설정 배열은 `config/mail.php` 파일에서 찾을 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이런 방식으로 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer를 통해 Resend PHP SDK를 설치해야 합니다:

```shell
composer require resend/resend-php
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `resend`로 지정합니다. 그리고 `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인합니다:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하기 위해서는 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer 패키지 관리자를 통해 다음과 같이 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 아래와 같이 옵션들이 포함되어 있는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

세션 토큰을 통해 AWS의 [임시 인증 정보](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)를 사용하려면, SES 설정에 `token` 키를 추가하면 됩니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환하는 배열 안에 `X-Ses-List-Management-Options` 헤더를 추가할 수 있습니다:

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

또한, 라라벨이 이메일을 전송할 때 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 지정하려면, `ses` 설정에 `options` 배열을 정의할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스를 제공하며, 라라벨용 API 기반 메일 드라이버를 별도로 제공합니다. 이 드라이버는 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

패키지 설치가 완료되면, 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가합니다. 그리고 `MAIL_MAILER` 환경 변수도 `mailersend`로 지정해야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, 애플리케이션의 `config/mail.php` 설정 파일 내 `mailers` 배열에 MailerSend를 추가합니다:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend의 자세한 사용법(호스팅된 템플릿 사용 등)은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(Failover) 설정

때때로, 외부 이메일 발송 서비스가 정상적으로 동작하지 않을 수 있습니다. 이런 상황을 대비해, 기본 발송용 드라이버가 작동하지 않을 때 사용할 백업 메일 발송 설정을 미리 지정할 수 있습니다.

이를 위해, 애플리케이션의 `mail` 설정 파일에 `failover` 트랜스포트를 사용하는 메일러를 설정합니다. `failover` 메일러에 대한 설정 배열에는 실제로 이메일이 발송될 메일러들의 우선순위가 정의된 `mailers` 배열이 포함되어야 합니다:

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

장애 조치 메일러를 정의했다면, 애플리케이션의 기본 메일러로 사용하려면 `mail` 설정 파일 내 `default` 설정 값에 해당 메일러 이름을 지정하면 됩니다:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드로빈(Round Robin) 설정

`roundrobin` 트랜스포트를 이용하면 여러 메일러에 메일 발송을 분산시킬 수 있습니다. 먼저, 애플리케이션의 `mail` 설정 파일에 `roundrobin` 트랜스포트를 사용하는 메일러를 정의합니다. 이 설정 배열에는 실제로 이메일을 발송할 메일러들의 목록이 담긴 `mailers` 배열이 있어야 합니다:

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

라운드로빈 메일러를 정의했다면, 이 메일러를 애플리케이션의 기본 메일러로 사용하려면, `mail` 설정 파일 내 `default` 설정 값에 해당 메일러 이름을 지정하면 됩니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드로빈 트랜스포트는 설정한 메일러 목록 중 하나를 무작위로 선택해서 사용한 뒤, 그 다음 이메일부터는 차례로 다음 메일러로 전환합니다. 이는 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*을 목표로 하는 `failover` 방식과는 달리, *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기

라라벨 애플리케이션에서는, 각 이메일 유형마다 "메일러블(mailable)" 클래스로 표현합니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, 처음으로 메일러블 클래스를 만들 때 `make:mail` 아티즌 명령어를 통해 자동으로 생성됩니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기

메일러블 클래스를 생성했다면, 실제로 해당 클래스 내부 코드를 들여다볼 수 있습니다. 메일러블 클래스의 주요 설정은 `envelope`, `content`, `attachments`와 같은 여러 메서드에서 이뤄집니다.

`envelope` 메서드는 메시지의 제목(subject)과 (필요한 경우) 수신자 정보를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 실제 이메일 콘텐츠를 생성할 때 사용할 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope로 설정하기

먼저, 이메일의 발신자(Sender), 다시 말해 이메일이 "누구로부터" 발송되는지 설정하는 방법을 알아보겠습니다. 발신자를 설정하는 방법에는 두 가지가 있습니다. 첫 번째는 메시지의 envelope(봉투)에 "from" 주소를 지정하는 방식입니다:

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

원한다면 `replyTo`(회신 주소)도 지정할 수 있습니다:

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
#### 글로벌 "from" 주소 사용하기

애플리케이션에서 모든 이메일에 동일한 "from" 주소를 사용하는 경우, 매번 메일러블 클래스를 생성할 때마다 주소를 지정하는 것은 번거로울 수 있습니다. 이럴 때는 `config/mail.php` 설정 파일에 전역 "from" 주소를 지정하면 됩니다. 별도로 "from" 주소를 지정하지 않으면 이 전역 설정이 자동으로 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

추가로, `config/mail.php` 설정 파일에서 전역 "reply_to" 주소도 지정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정

메일러블 클래스의 `content` 메서드 안에서, 실제 메일 내용을 렌더링할 때 사용할 뷰(템플릿)를 지정할 수 있습니다. 대부분 이메일은 내용을 만들 때 [Blade 템플릿](/docs/12.x/blade)을 활용하므로, HTML도 Blade의 다양한 기능과 편의성을 그대로 사용할 수 있습니다:

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
> 이메일 템플릿들을 관리하기 위해 `resources/views/mail` 디렉터리를 생성하는 것이 좋습니다. 하지만 실제로는 `resources/views` 디렉터리 내 원하는 어느 위치든 자유롭게 템플릿을 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트(plain-text) 버전을 별도로 정의하고 싶다면, 메시지의 `Content` 정의에서 plain-text 템플릿을 지정하면 됩니다. `view` 파라미터와 마찬가지로, `text` 파라미터에는 해당 이메일 내용을 렌더링할 템플릿명을 지정하면 됩니다. 한 메시지에서 HTML과 plain-text 두 버전을 동시에 정의할 수도 있습니다:

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

가독성을 위해, `html` 파라미터는 `view` 파라미터의 별칭으로 사용할 수 있습니다:

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

대부분의 경우, 이메일의 HTML을 렌더링할 때 뷰에서 사용할 데이터를 전달해야 합니다. 데이터를 뷰에 전달하는 방법에는 두 가지가 있습니다. 먼저, 메일러블 클래스에 정의된 public 속성은 자동으로 뷰에 전달되어 사용할 수 있습니다. 예를 들어, 생성자에서 데이터를 받아 클래스의 public 속성에 할당하는 방식입니다:

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

이렇게 public 속성에 데이터를 할당하면, 뷰에서 Blade 템플릿 변수로 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 데이터 전달

이메일 데이터의 형식을 템플릿에 전달하기 전에 직접 커스터마이즈하고 싶다면, `Content` 정의의 `with` 파라미터를 통해 데이터를 직접 넘길 수 있습니다. 이 경우에도 대개 생성자를 통해 데이터를 전달하지만, 해당 데이터는 `protected`나 `private` 속성에 할당하여 템플릿에서 자동 노출되지 않도록 할 수 있습니다:

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

`with` 파라미터로 데이터를 전달하면 뷰에서 해당 데이터를 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메시지의 `attachments` 메서드에서 첨부파일 객체들을 배열에 담아 반환하면 됩니다. 가장 기본적으로는 `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달하여 첨부할 수 있습니다:

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

첨부파일에 대해 표시 이름이나 MIME 타입을 지정하고 싶을 때는 `as`와 `withMime` 메서드를 연이어 사용할 수 있습니다:

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
#### 파일 시스템 디스크에서 첨부하기

[파일시스템 디스크](/docs/12.x/filesystem)에 저장된 파일을 이메일에 첨부하려면, `fromStorage` 첨부 메서드를 사용하면 됩니다:

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

물론, 첨부파일의 이름이나 MIME 타입도 지정할 수 있습니다:

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

기본 디스크가 아닌 특정 스토리지 디스크에서 첨부파일을 지정하려면, `fromStorageDisk` 메서드를 사용할 수 있습니다:

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
#### Raw 데이터 첨부

`fromData` 첨부 메서드를 사용하면, 메모리 상의 바이트 문자열을 첨부파일로 바로 추가할 수 있습니다. 예를 들어, PDF를 메모리에서 생성하고 바로 첨부하고 싶을 때 사용할 수 있습니다. `fromData` 메서드는 raw 데이터 바이트를 반환하는 클로저와 첨부파일로 지정할 이름을 인자로 받습니다:

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

이메일에 이미지를 인라인으로 삽입하는 작업은 일반적으로 번거롭지만, 라라벨은 이를 간단히 처리할 수 있는 기능을 제공합니다. 인라인 이미지를 삽입하려면, 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. 라라벨은 모든 이메일 템플릿에서 `$message` 변수를 자동으로 사용할 수 있도록 해주므로, 별도로 전달할 필요가 없습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text(일반 텍스트) 메시지 템플릿에서는 사용할 수 없습니다. plain-text 메시지는 인라인 첨부파일을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

만약 이메일 템플릿에 이미 가지고 있는 raw 이미지 데이터를 인라인으로 넣고 싶다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이때, 이미지에 지정할 파일명을 함께 전달해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체

경로 문자열을 이용한 단순한 첨부도 충분하지만, 실제로는 애플리케이션 내에서 첨부할 수 있는 대상이 클래스(예: Photo 모델 등)로 표현되는 경우가 많습니다. 이런 경우라면, 굳이 파일 경로를 직접 지정하기보다, 해당 객체(예: Photo 모델 인스턴스)를 바로 `attach` 메서드에 넘기는 것이 훨씬 편리합니다. 첨부 가능한 객체(Attachable objects)를 사용하면 이를 쉽게 구현할 수 있습니다.

시작하려면, 첨부 가능한 객체로 만들고자 하는 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다. 이 인터페이스는 클래스에 `toMailAttachment` 메서드를 정의하도록 요구하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

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

이렇게 attachable 객체를 정의했다면, 이메일 메시지를 생성할 때 `attachments` 메서드에서 해당 객체 인스턴스를 바로 반환할 수 있습니다:

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

첨부파일 데이터가 Amazon S3와 같은 원격 파일 스토리지 서비스에 저장되어 있는 경우도 많으니, 라라벨은 [파일시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 이용해서도 첨부파일 인스턴스를 생성할 수 있도록 지원합니다:

```php
// 기본 디스크에서 파일을 통한 첨부...
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일을 통한 첨부...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

추가로, 이미 메모리에 있는 데이터를 이용해서 첨부파일 인스턴스를 만들고 싶다면, `fromData` 메서드에 클로저를 넘겨주면 됩니다. 이 클로저는 첨부파일에 해당하는 raw 데이터를 반환해야 합니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일을 커스터마이징하기 위해, 라라벨은 추가 메서드도 제공합니다. 예를 들어, 파일 이름과 MIME 타입을 각각 `as`, `withMime` 메서드로 지정할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>

### 헤더(Headers)

가끔 메일을 발송할 때 추가 헤더를 지정해야 하는 경우가 있습니다. 예를 들어, 커스텀 `Message-Id`를 설정하거나 임의의 텍스트 헤더를 추가해야 할 수도 있습니다.

이를 달성하려면, 보낼 메일러블(mailable)에 `headers` 메서드를 정의하면 됩니다. `headers` 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, 이 클래스는 `messageId`, `references`, `text` 파라미터를 받습니다. 당연히 각 메시지에 필요한 파라미터만 넘겨도 됩니다.

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

Mailgun, Postmark 같은 일부 외부 이메일 서비스 제공업체는 메시지 "태그(tags)"와 "메타데이터(metadata)" 기능을 지원합니다. 이 기능은 애플리케이션이 발송하는 이메일을 그룹화하거나 추적하는 데 사용됩니다. `Envelope` 정의에서 태그와 메타데이터를 추가할 수 있습니다.

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

애플리케이션에서 Mailgun 드라이버를 사용한다면, 태그와 메타데이터 관련하여 [Mailgun의 태그 관련 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터 관련 문서](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)를 참고하시기 바랍니다. Postmark를 사용하는 경우 [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 문서도 참고할 수 있습니다.

Amazon SES를 사용해 이메일을 발송하는 경우, [SES의 "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부하려면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

라라벨의 메일 기능은 Symfony Mailer가 기반입니다. 라라벨은 메시지를 실제로 보내기 전에 Symfony Message 인스턴스로 콜백을 등록해 직접 커스터마이징할 수 있도록 지원합니다. 이를 위해 `Envelope` 정의에 `using` 파라미터를 추가하면 됩니다.

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
## 마크다운 메일러블(Markdown Mailables)

마크다운 메일러블 메시지를 사용하면 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 메일러블에서 활용할 수 있습니다. 메시지는 마크다운 문법으로 작성되어, 라라벨이 아름답고 반응형인 HTML 템플릿을 렌더링하고, 동시에 텍스트 버전도 자동으로 생성해줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

마크다운 템플릿이 포함된 메일러블을 생성하려면, `make:mail` 아티즌 명령어에 `--markdown` 옵션을 사용할 수 있습니다.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그리고 `content` 메서드에서 메일러블의 `Content` 정의 시, `view` 파라미터 대신 `markdown` 파라미터를 사용합니다.

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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 조합하여, 라라벨이 미리 제공하는 이메일 UI 컴포넌트들을 쉽게 활용해 메일을 작성할 수 있습니다.

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
> 마크다운 이메일을 작성할 때 들여쓰기를 과하게 사용하지 마세요. 마크다운 표준상 들여쓰기된 내용은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트(Button Component)

버튼 컴포넌트는 중앙에 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적인 `color` 두 가지 인자를 받습니다. 지원되는 색상은 `primary`, `success`, `error`입니다. 한 메시지에 버튼 컴포넌트를 여러 번 사용할 수도 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트(Panel Component)

패널 컴포넌트는 지정한 텍스트 블록을 주변 내용과 약간 다른 배경색의 패널에 표시합니다. 이를 통해 특정 텍스트 블록에 주의를 끌 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트(Table Component)

테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 마크다운 테이블을 콘텐츠로 받아 표시합니다. 기본 마크다운 테이블 정렬 문법을 사용해 컬럼 정렬도 지원됩니다.

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

모든 마크다운 메일 컴포넌트를 직접 애플리케이션으로 내보낸 후 커스터마이징할 수도 있습니다. 이를 위해 `laravel-mail` 태그를 가진 `vendor:publish` 아티즌 명령어를 실행하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 마크다운 메일 컴포넌트들이 `resources/views/vendor/mail` 디렉터리에 복사됩니다. `mail` 디렉터리에는 각각의 컴포넌트에 대응하는 `html` 및 `text` 디렉터리가 들어 있습니다. 이 컴포넌트 파일들을 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보내면, `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. 이 파일에서 CSS를 자유롭게 수정할 수 있으며, 작성한 스타일은 자동으로 HTML 메일의 인라인 CSS로 변환되어 적용됩니다.

라라벨의 마크다운 컴포넌트에 완전히 새로운 테마를 적용하고 싶다면, 직접 CSS 파일을 `html/themes` 디렉터리에 추가하면 됩니다. 파일명을 정하고 저장한 후, 애플리케이션의 `config/mail.php` 설정 파일에서 `theme` 옵션을 새로운 테마 이름으로 지정하세요.

특정 메일러블에만 다른 테마를 적용하고 싶다면, 해당 메일러블 클래스의 `$theme` 속성을 사용하려는 테마 이름으로 지정할 수 있습니다.

<a name="sending-mail"></a>
## 메일 발송하기

메시지를 발송하려면, [Mail 파사드](/docs/12.x/facades)에서 `to` 메서드를 사용하면 됩니다. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체나 컬렉션을 전달하면, 라라벨은 해당 객체의 `email`과 `name` 속성을 자동으로 사용하여 수신자를 결정하므로, 해당 속성이 객체에 정의되어 있는지 반드시 확인해야 합니다. 수신자를 지정한 후, 메일러블 클래스의 인스턴스를 `send` 메서드에 전달해 메일을 보낼 수 있습니다.

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
     * 주어진 주문을 발송합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 발송 처리...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

메일을 보낼 때 단순히 "to"만 지정할 필요는 없습니다. "to", "cc", "bcc" 수신자를 각각의 메서드를 체이닝해서 함께 지정할 수도 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 다수 수신자 루프 돌리기

때때로, 한 번에 여러 명에게 메일러블을 보내기 위해 수신자 또는 이메일 주소 배열을 순회해야 할 때가 있습니다. 그러나 `to` 메서드는 메일러블의 수신자 목록에 이메일 주소를 추가하는 방식이므로, 루프를 돌 때마다 이전까지의 모든 수신자에게 메일이 한 번 더 발송됩니다. 따라서 각 수신자마다 반드시 메일러블 인스턴스를 새로 생성해서 사용해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

기본적으로 라라벨은 애플리케이션의 `mail` 설정 파일에서 `default`로 지정된 메일러 설정을 사용해 메일을 보냅니다. 하지만, `mailer` 메서드를 통해 특정 메일러 설정을 명시적으로 선택하여 메일을 보낼 수도 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일을 큐에 등록하기

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐에 등록하기

이메일 전송은 애플리케이션의 응답 시간을 늦출 수 있기 때문에, 많은 개발자들이 이메일 메시지를 백그라운드에서 비동기적으로 보내기 위해 큐에 등록합니다. 라라벨은 [통합 큐 API](/docs/12.x/queues)를 통해 이 기능을 간편하게 제공합니다. 메일 메시지를 큐에 등록하려면, `Mail` 파사드에서 수신자를 지정한 후 `queue` 메서드를 호출하면 됩니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 큐에 작업(Job)을 추가하여 메시지가 백그라운드에서 발송되도록 처리합니다. 이 기능을 사용하기 전에 반드시 [큐 설정](/docs/12.x/queues)을 완료해야 합니다.

<a name="delayed-message-queueing"></a>
#### 메일 발송 지연

큐에 등록된 메일 메시지의 발송을 일정 시간 뒤로 늦추고 싶다면, `later` 메서드를 사용할 수 있습니다. `later` 메서드는 첫 번째 인자로 언제 전송할 것인지 `DateTime` 인스턴스를 받습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 작업 넣기

`make:mail` 커맨드로 생성된 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레잇을 포함하므로, 메일러블 인스턴스에서 `onQueue`와 `onConnection` 메서드를 호출해 연결 및 큐 이름을 직접 지정할 수 있습니다.

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
#### 기본적으로 큐에 등록하는 메일러블

항상 큐를 이용해 보내야 하는 메일러블 클래스라면, 해당 클래스에 `ShouldQueue` 계약(Contract)을 구현하면 됩니다. 이렇게 하면, 나중에 `send` 메서드를 호출해도 큐에 등록되어 전송됩니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 사용 시 데이터베이스 트랜잭션 주의

큐에 등록한 메일러블을 데이터베이스 트랜잭션 내에서 디스패치하면, 트랜잭션이 완료되기 전에 큐에서 작업이 처리될 수 있습니다. 이럴 경우, 트랜잭션 내에서 모델 변경이나 데이터베이스 레코드 생성이 아직 완료되지 않아, 메일러블이 기대하는 모델 또는 데이터가 존재하지 않아 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정값이 `false`라면, 메일을 보낼 때 `afterCommit` 메서드를 호출하여 반드시 모든 데이터베이스 트랜잭션이 커밋된 후에 발송되도록 지정할 수 있습니다.

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
     * 새로운 메시지 인스턴스 생성자.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이런 문제들에 대한 자세한 대처 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐에 등록된 메일 발송 실패 처리

큐에 등록된 이메일 발송이 실패할 경우, 만약 메일러블 클래스에 `failed` 메서드가 정의되어 있다면 이 메서드가 호출됩니다. 이때 실패 원인이 된 `Throwable` 인스턴스가 `failed` 메서드에 전달됩니다.

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
     * 큐에 등록된 이메일 발송 실패 처리.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링(Rendering Mailables)

가끔 메일을 실제로 보내지 않고, 메일러블의 HTML 내용을 미리 확인하고 싶을 때가 있습니다. 이때는 메일러블의 `render` 메서드를 호출하면 됩니다. 이 메서드는 메일러블의 HTML 렌더링 결과를 문자열로 반환합니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블의 템플릿을 디자인할 때, Blade 템플릿처럼 빠르게 브라우저에서 렌더링 결과를 미리 볼 수 있으면 매우 편리합니다. 라라벨에서는 이러한 목적으로 라우트 클로저나 컨트롤러에서 메일러블을 직접 반환할 수 있습니다. 메일러블이 반환되면 자동으로 렌더링되어 브라우저에 표시되므로, 실제로 이메일을 전송하지 않고도 디자인을 빠르게 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블의 다국어 지원(Localizing Mailables)

라라벨은 메일러블을 현재 요청의 로케일과 다른 언어로 보내는 기능을 제공합니다. 더불어, 해당 메일을 큐에 등록한 경우에도 지정한 로케일이 기억되어 적용됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드를 사용해 원하는 언어를 지정할 수 있습니다. 메일러블의 템플릿을 렌더링하는 동안 애플리케이션의 로케일이 지정한 로케일로 변경되었다가, 렌더링이 끝나면 원래 로케일로 복구됩니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자별 선호 로케일(User Preferred Locales)

애플리케이션에서 각 사용자의 선호 언어를 저장하는 경우, 한 개 이상의 모델에 `HasLocalePreference` 계약(Contract)을 구현해두면 라라벨이 메일 발송 시 이 값을 자동으로 사용하도록 할 수 있습니다.

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

인터페이스를 구현하면, 라라벨은 해당 모델로 메일러블이나 알림을 보낼 때 자동으로 선호하는 로케일을 적용하므로, 별도로 `locale` 메서드를 호출할 필요가 없습니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트(Test)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

라라벨은 메일러블의 구조를 검사할 수 있는 다양한 메서드를 제공합니다. 또한, 메일러블이 예상하는 콘텐츠를 포함하는지 편리하게 검증할 수 있는 여러 메서드도 지원합니다.

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

예상할 수 있듯, "HTML"로 시작하는 assertion은 HTML 버전의 메일러블이 특정 문자열을 포함하는지, "text"로 시작하는 assertion은 일반 텍스트 버전이 특정 문자열을 포함하는지 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트

메일러블의 콘텐츠 테스트는, 특정 사용자를 대상으로 해당 메일러블이 "전송"되었는지 테스트하는 코드와 별도로 작성하는 것이 좋습니다. 실제 코드를 테스트할 때는 메일러블의 실제 내용이 아니라, 라라벨이 해당 메일러블을 전송하도록 지시했는지만 확인하면 충분하기 때문입니다.

메일 발송을 실제로 하지 않으려면 `Mail` 파사드의 `fake` 메서드를 활용하면 됩니다. 이 메서드를 호출한 뒤에는, 메일러블이 특정 사용자로 전송 지시되었는지 assertion으로 확인할 수 있으며, 메일러블에 전달된 데이터도 검사할 수 있습니다.

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 발송 작업 수행...

    // 아무 메일러블도 전송되지 않았는지 확인...
    Mail::assertNothingSent();

    // 메일러블이 전송되었는지 확인...
    Mail::assertSent(OrderShipped::class);

    // 메일러블이 두 번 전송되었는지 확인...
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일 주소로 전송되었는지 확인...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 복수의 이메일 주소로 전송되었는지 확인...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 다른 메일러블은 전송되지 않았는지 확인...
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3개의 메일러블이 전송되었는지 확인...
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

        // 주문 발송 작업 수행...

        // 아무 메일러블도 전송되지 않았는지 확인...
        Mail::assertNothingSent();

        // 메일러블이 전송되었는지 확인...
        Mail::assertSent(OrderShipped::class);

        // 메일러블이 두 번 전송되었는지 확인...
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 이메일 주소로 전송되었는지 확인...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // 복수의 이메일 주소로 전송되었는지 확인...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // 다른 메일러블은 전송되지 않았는지 확인...
        Mail::assertNotSent(AnotherMailable::class);

        // 총 3개의 메일러블이 전송되었는지 확인...
        Mail::assertSentCount(3);
    }
}
```

메일러블을 큐에 등록해 백그라운드로 보낸다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등의 메서드에는 클로저를 전달하여, 전달된 "truth test"를 통과하는 메일러블이 적어도 하나 이상 있는 경우 assertion이 성공 처리되도록 할 수 있습니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 assertion 메서드에 클로저를 전달하면, 해당 메일러블 인스턴스에서 다양한 유용한 메서드를 통해 수신자/제목/참조 등을 편리하게 검사할 수 있습니다.

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

메일러블 인스턴스는 첨부 파일을 검사할 수 있는 여러 편리한 메서드도 제공합니다.

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

메일이 "전송되지 않았음"을 확인하는 방법으로는 `assertNotSent`와 `assertNotQueued` 두 가지가 있습니다. 때로는 메일이 전송되지 **않았고**, 큐에 등록도 **되지 않았음**을 모두 확인해야 할 때가 있는데, 이럴 땐 `assertNothingOutgoing` 또는 `assertNotOutgoing` 메서드를 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일 및 로컬 개발 환경

이메일을 발송하는 애플리케이션을 개발할 때, 실제 이메일 주소로 메일을 보내고 싶지 않을 때가 많습니다. 라라벨은 로컬 개발 환경에서 실제 메일 전송을 "비활성화" 할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버(Log Driver)

메일을 실제로 보내지 않고, 모든 이메일 메시지를 로그 파일에만 기록하도록 하려면 `log` 메일 드라이버를 사용할 수 있습니다. 보통 이 드라이버는 개발 환경에서만 사용합니다. 환경별 설정 방법 등 자세한 내용은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io)과 같은 서비스를 사용하고, `smtp` 드라이버를 이용해 실제 메일 전송 없이 "더미" 메일박스에서 메일을 확인하는 방법도 있습니다. 이런 방식을 사용하면 Mailtrap의 메시지 뷰어에서 최종적으로 어떤 이메일이 만들어지는지 실제로 확인할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, [Mailpit](https://github.com/axllent/mailpit)으로 메시지를 미리 볼 수 있습니다. Sail이 실행 중이라면, `http://localhost:8025`에서 Mailpit 인터페이스에 접속해 메시지를 확인할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 "to" 주소 사용

마지막으로, `Mail` 파사드에서 제공하는 `alwaysTo` 메서드를 이용해 특정 이메일 주소로만 항상 메일을 받도록 전역 "to" 주소를 지정할 수 있습니다. 보통 이 메서드는 애플리케이션 서비스 프로바이더의 `boot` 메서드 안에서 호출하는 것이 일반적입니다.

```php
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 초기화 처리.
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

라라벨은 메일 메시지를 보낼 때 두 가지 이벤트를 디스패치합니다. `MessageSending` 이벤트는 메시지가 전송되기 *직전에* 디스패치되며, `MessageSent` 이벤트는 메시지 전송이 끝난 후에 디스패치됩니다. 이 이벤트들은 메일이 실제로 *전송*될 때 발생한다는 점에 주의해야 하며, 큐에 넣을 때는 발생하지 않습니다. 애플리케이션에서 이러한 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 작성할 수 있습니다:

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

라라벨은 다양한 메일 트랜스포트를 기본으로 제공합니다. 그러나 라라벨에서 기본적으로 지원하지 않는 다른 서비스로 이메일을 전달하고 싶다면 여러분만의 트랜스포트를 작성할 수도 있습니다. 트랜스포트를 작성하려면, 먼저 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 확장하는 클래스를 정의해야 합니다. 그리고 트랜스포트에서 `doSend` 및 `__toString` 메서드를 구현합니다:

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

커스텀 트랜스포트를 정의했다면, `Mail` 파사드의 `extend` 메서드를 통해 해당 트랜스포트를 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다. `extend` 메서드에 전달되는 클로저에는 `$config` 인자가 전달되며, 이 인자에는 애플리케이션의 `config/mail.php` 설정 파일에서 정의된 메일러의 설정 배열이 포함됩니다:

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

커스텀 트랜스포트를 정의하고 등록했다면, 애플리케이션의 `config/mail.php` 설정 파일에서 새로운 트랜스포트를 사용하는 메일러 정의를 추가할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가적인 Symfony 트랜스포트

라라벨은 Mailgun, Postmark처럼 Symfony에서 공식적으로 관리하는 일부 메일 트랜스포트도 지원합니다. 하지만 이 외에 추가로 Symfony에서 제공하는 트랜스포트를 라라벨에 등록해 사용하고자 할 수도 있습니다. 이 경우, Composer를 통해 필요한 Symfony 메일러 패키지를 설치하고, 라라벨에 트랜스포트를 등록하면 됩니다. 예를 들어, "Brevo"(이전 명칭 "Sendinblue") Symfony 메일러를 설치 및 등록해보겠습니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지가 설치됐다면, 애플리케이션의 `services` 설정 파일에 Brevo API 인증 정보를 추가합니다:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그 다음, `Mail` 파사드의 `extend` 메서드를 사용해 라라벨에 해당 트랜스포트를 등록할 수 있습니다. 일반적으로 이 작업은 서비스 프로바이더의 `boot` 메서드에서 수행합니다:

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

이렇게 트랜스포트를 등록했다면, 이제 애플리케이션의 `config/mail.php` 설정 파일에 새로운 트랜스포트를 활용하는 메일러 정의를 추가할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```