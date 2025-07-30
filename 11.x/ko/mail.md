# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 조건](#driver-prerequisites)
    - [실패 대비 구성](#failover-configuration)
    - [라운드 로빈 구성](#round-robin-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [첨부 가능한 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성하기](#generating-markdown-mailables)
    - [마크다운 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 보내기](#sending-mail)
    - [메일 큐잉하기](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송기](#custom-transports)
    - [추가 Symfony 전송기](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/7.0/mailer.html) 컴포넌트를 기반으로 한 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통해 이메일을 보낼 수 있는 드라이버를 제공하여, 로컬 또는 클라우드 서비스를 신속하게 통해 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일 내에 설정된 각 메일러는 고유한 설정과 심지어 고유한 "transport"를 가질 수 있어서, 특정 이메일 메시지는 다른 이메일 서비스를 사용해 보낼 수 있습니다. 예를 들어, 애플리케이션은 트랜잭션 이메일에는 Postmark를, 대량 이메일에는 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 내에는 `mailers` 구성 배열이 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송기를 위한 샘플 구성 항목이 포함되어 있습니다. 또한 `default` 설정 값은 기본적으로 이메일을 보낼 때 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송기 사전 조건 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend, MailerSend와 같이 API 기반 드라이버는 종종 SMTP 서버를 통한 메일 발송보다 더 간단하고 빠릅니다. 가능한 경우 이러한 드라이버 중 하나를 사용하시는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 먼저 Composer를 통해 Symfony의 Mailgun Mailer 전송기를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에 두 가지 변경 사항을 적용해야 합니다. 먼저 기본 메일러를 `mailgun`으로 설정하세요:

```
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 다음 구성 배열을 추가하세요:

```
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션을 추가하세요:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 이외의 [Mailgun 지역](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용한다면, 이 설정 파일에서 해당 지역의 엔드포인트를 지정할 수 있습니다:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    'scheme' => 'https',
],
```

<a name="postmark-driver"></a>
#### Postmark 드라이버

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer를 통해 Symfony의 Postmark Mailer 전송기를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php` 설정 파일에서 기본값을 `postmark`로 설정하세요. 그리고 `config/services.php` 파일에 다음 옵션들이 포함되어 있는지 확인하세요:

```
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하고 싶다면, `config/mail.php` 파일 내 메일러 구성 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

```
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이렇게 하면 여러 Postmark 메일러를 다른 메시지 스트림과 함께 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer를 통해 Resend PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

그 다음, `config/mail.php` 설정 파일에서 기본값을 `resend`로 설정하세요. 그리고 `config/services.php` 파일에 다음 옵션들이 포함되어 있는지 확인하세요:

```
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. 이 라이브러리는 Composer로 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php`에서 기본 메일러를 `ses`로 설정하고, `config/services.php` 파일에 다음 구성이 포함되어 있는지 확인하세요:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면, `ses` 설정에 `token` 키를 추가하세요:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 사용하려면, 메일 메시지의 [`headers`](#headers) 메서드에서 반환되는 배열에 `X-Ses-List-Management-Options` 헤더를 포함시킬 수 있습니다:

```php
/**
 * 메시지 헤더 얻기
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

Laravel이 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)를 정의하고 싶다면, `ses` 설정 배열 내에 `options` 배열을 정의할 수 있습니다:

```
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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스로, Laravel용 자체 API 기반 메일 드라이버를 운영합니다. 이 드라이버가 포함된 패키지는 Composer로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

설치가 완료되면, 애플리케이션의 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 또한 `MAIL_MAILER` 환경 변수도 `mailersend`로 설정되어야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, 애플리케이션의 `config/mail.php` 설정 파일 내 `mailers` 배열에 MailerSend 항목을 추가하세요:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend 및 호스티드 템플릿 사용법 등 자세한 내용은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 실패 대비 구성 (Failover Configuration)

가끔씩, 메일 발송을 위해 설정한 외부 서비스가 다운되는 경우가 있습니다. 이런 상황에 대비해 하나 이상의 백업 메일 전송 구성을 정의해둘 수 있습니다. 이렇게 하면 기본 전송기가 다운됐을 때 백업 구성들이 사용됩니다.

이를 위해, 애플리케이션의 `mail` 설정 파일에 `failover` 전송기를 사용하는 메일러를 정의하세요. 그리고 `failover` 메일러 구성의 `mailers` 배열에 사용할 메일러들을 순서대로 지정합니다:

```
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

구성한 failover 메일러를 기본 메일러로 사용하려면, `mail` 설정 파일의 `default` 키 값을 `failover`로 설정하세요:

```
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈 구성 (Round Robin Configuration)

`roundrobin` 전송기는 여러 메일러에 메일 발송 부하를 분산시켜 줍니다. 사용하려면 `roundrobin` 전송기를 사용하는 메일러를 `mail` 설정에 정의하고, `mailers` 배열에 어떤 메일러들이 순차적으로 선택될지 배열로 지정하세요:

```
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

정의된 round robin 메일러를 기본 메일러로 지정하려면, `default` 값을 `roundrobin`으로 설정하세요:

```
'default' => env('MAIL_MAILER', 'roundrobin'),
```

`roundrobin` 전송기는 등록한 메일러 목록에서 랜덤으로 하나를 선택하고, 이후 메일마다 다음 메일러로 순차적으로 돌아가는 방식입니다. 반면 `failover` 전송기는 *고가용성(high availability)*를 위한 전송 실패 대비 기능이고, `roundrobin` 전송기는 *부하 분산(load balancing)*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기 (Generating Mailables)

Laravel 애플리케이션에서 보내는 각 유형의 이메일은 "mailable" 클래스 형식으로 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 아직 해당 디렉토리가 없다면, `make:mail` Artisan 명령어로 첫 번째 메일러블 클래스를 생성할 때 자동으로 생성됩니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기 (Writing Mailables)

메일러블 클래스를 생성했다면, 내용을 살펴보겠습니다. 메일러블 설정은 여러 메서드에서 이루어지는데, 대표적으로 `envelope`, `content`, `attachments` 메서드가 있습니다.

- `envelope` 메서드는 메시지 주제(subject)와 가끔 수신자(recipient)를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다.
- `content` 메서드는 메시지 내용을 생성할 때 사용할 [Blade 템플릿](/docs/11.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope 사용하기

먼저, 이메일 발신자를 설정하는 방법부터 보겠습니다. 즉, 이메일이 "누구로부터(from)" 보내지는지 설정하는 것입니다. 발신자 설정 방법은 두 가지입니다. 먼저, 메시지의 Envelope에 "from" 주소를 지정할 수 있습니다:

```
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 Envelope 얻기
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

```
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

애플리케이션에서 모든 이메일에 같은 "from" 주소를 사용하는 경우, 매번 메일러블 클래스에 추가하는 것은 번거롭습니다. 대신 `config/mail.php`에 전역 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 별도로 지정하지 않으면 이 주소가 사용됩니다:

```
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

전역 "reply_to" 주소도 마찬가지로 `config/mail.php`에 지정할 수 있습니다:

```
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서, 메일 내용 렌더링에 사용할 `view`—즉 어떤 템플릿을 사용할지—를 정의할 수 있습니다. 보통 이메일은 [Blade 템플릿](/docs/11.x/blade)을 사용해 HTML을 렌더링하기 때문에, Blade 템플릿 엔진의 강력한 기능과 편리함을 그대로 메일 작성에 활용할 수 있습니다:

```
/**
 * 메시지 내용 정의 가져오기
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> [!NOTE]  
> 이메일 템플릿을 모아놓기 위해 `resources/views/emails` 디렉토리를 생성해도 좋지만, `resources/views` 내 어디든 원하는 위치에 자유롭게 두셔도 됩니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 플레인 텍스트 버전을 정의하고 싶으면, `Content` 정의 시 `text` 파라미터에 템플릿 이름을 지정하세요. `view` 파라미터처럼, `text`는 메일 내용 렌더링에 사용할 템플릿 이름입니다. HTML과 플레인 텍스트 버전 둘 다 정의 가능합니다:

```
/**
 * 메시지 내용 정의 가져오기
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```

명확성을 위해, `html` 파라미터는 `view` 파라미터의 별칭으로 사용할 수 있습니다:

```
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### 공개 속성 이용하기

보통 뷰에 데이터를 전달해 이메일 HTML 렌더링에 사용하려 합니다. 뷰에 데이터를 전달하는 방법은 두 가지가 있습니다. 우선, 메일러블 클래스에서 정의한 공개 속성은 자동으로 뷰에 전달됩니다. 따라서 보통은 생성자에서 데이터를 받아 그 값을 공개 속성으로 지정합니다:

```
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
     * 새 메시지 인스턴스 생성
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * 메시지 내용 정의 가져오기
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

데이터가 공개 속성에 설정되면, Blade 템플릿 내에서 다른 변수처럼 간편하게 접근할 수 있습니다:

```
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 이용하기

데이터를 템플릿에 전달하기 전에 포맷을 변형하거나 커스터마이징하고 싶다면, `Content` 정의의 `with` 파라미터를 통해 명시적으로 전달할 수 있습니다. 보통은 여전히 생성자에서 데이터를 받되, 이 경우 속성을 `protected`나 `private`으로 정의해 자동 전달을 막고 `with` 배열로 직접 전달합니다:

```
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
     * 새 메시지 인스턴스 생성
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * 메시지 내용 정의 가져오기
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

`with`로 전달한 데이터는 뷰 내에서 변수명으로 값에 접근할 수 있습니다:

```
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일 (Attachments)

이메일에 첨부파일을 추가하려면, 메시지의 `attachments` 메서드에서 반환하는 배열에 첨부 정보를 추가하면 됩니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 전달하여 첨부를 추가할 수 있습니다:

```
use Illuminate\Mail\Mailables\Attachment;

/**
 * 메시지 첨부파일 반환
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

첨부 시 보여질 파일 이름과 MIME 타입을 지정하려면 `as`와 `withMime` 메서드를 사용하세요:

```
/**
 * 메시지 첨부파일 반환
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
#### 디스크 저장소에서 첨부하기

애플리케이션의 [파일 시스템 디스크](/docs/11.x/filesystem)에 저장된 파일을 첨부할 때는 `fromStorage` 메서드를 사용하세요:

```
/**
 * 메시지 첨부파일 반환
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

물론 이름과 MIME 타입 지정도 가능합니다:

```
/**
 * 메시지 첨부파일 반환
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

기본 디스크가 아닌 특정 디스크에서 파일을 첨부하려면 `fromStorageDisk` 메서드를 사용하세요:

```
/**
 * 메시지 첨부파일 반환
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
#### 원시 데이터 첨부파일

`fromData` 메서드는 메모리 내 원시 바이트 데이터를 첨부파일로 추가할 때 사용합니다. 예를 들어, 메모리 내에서 생성한 PDF를 디스크에 쓰지 않고 바로 첨부할 때 유용합니다. 이 메서드는 원시 데이터를 반환하는 클로저와 첨부파일 이름을 인수로 받습니다:

```
/**
 * 메시지 첨부파일 반환
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

이메일에 인라인 이미지를 삽입하는 과정은 보통 복잡하지만, Laravel은 이를 간단히 하기 위한 방법을 제공합니다. 인라인 이미지 삽입은 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용하면 됩니다. Laravel은 이 `$message` 변수를 모든 이메일 템플릿에서 자동으로 사용할 수 있게 해 줍니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]  
> `$message` 변수는 일반 텍스트(plain-text) 메시지 템플릿에서는 사용할 수 없습니다. 일반 텍스트 메시지는 인라인 첨부파일을 사용하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 인라인 삽입

이미 원시 이미지 데이터 문자열이 있을 경우, `$message` 변수의 `embedData` 메서드를 호출해 HTML에 삽입할 수 있습니다. 이때, 임베드 이미지에 이름을 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체 (Attachable Objects)

파일 경로 문자열로 첨부하는 것만으로도 충분하지만, 때때로 애플리케이션 내 첨부 파일이 클래스로 표현되어 있기도 합니다. 예를 들어, 사진을 첨부할 때 `Photo` 모델이 존재할 수 있습니다. 이런 경우, 사진 모델 객체를 직접 `attach` 메서드에 넘길 수 있으면 편리하겠죠. 이것이 첨부 가능한 객체 기능입니다.

먼저, 첨부 가능한 객체가 될 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 인터페이스는 `toMailAttachment` 메서드를 요구하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 모델의 첨부 가능한 표현 얻기
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

이런 객체를 정의한 뒤, 이메일 메시지 작성 시 `attachments` 메서드에서 해당 객체 인스턴스를 반환할 수 있습니다:

```
/**
 * 메시지 첨부파일 반환
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

물론 첨부 데이터가 원격 파일 저장소, 예를 들어 Amazon S3 같은 서비스에 있으면 Laravel은 애플리케이션의 [파일 시스템 디스크](/docs/11.x/filesystem)에 저장된 데이터를 첨부 파일로 생성하는 것도 지원합니다:

```
// 기본 디스크의 파일로 첨부 파일 생성하기...
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일로 첨부 파일 생성하기...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한 메모리 내 데이터로부터 첨부파일 인스턴스를 생성할 수도 있습니다. 이 경우 `fromData` 메서드에 원시 데이터를 반환하는 클로저를 제공합니다:

```
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일 이름 및 MIME 타입 등은 `as`와 `withMime` 메서드로 자유롭게 커스터마이징할 수 있습니다:

```
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

가끔은 메시지에 추가 헤더를 첨부해야 할 때가 있습니다. 예를 들어 커스텀 `Message-Id`나 임의의 텍스트 헤더를 지정하는 경우입니다.

이때는 메일러블 클래스에 `headers` 메서드를 정의하여, `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하세요. 이 클래스는 `messageId`, `references`, `text` 파라미터를 받아들이며, 필요한 파라미터만 제공하면 됩니다:

```
use Illuminate\Mail\Mailables\Headers;

/**
 * 메시지 헤더 얻기
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
### 태그 및 메타데이터 (Tags and Metadata)

Mailgun, Postmark 같은 일부 이메일 공급자는 메시지에 "태그(tags)"와 "메타데이터(metadata)" 기능을 제공하여 애플리케이션에서 보낸 이메일 그룹핑이나 추적에 활용할 수 있습니다. 이를 메일 메시지의 `Envelope` 정의에서 지정할 수 있습니다:

```
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 Envelope 얻기
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

Mailgun 드라이버를 사용할 때는 [Mailgun 태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages) 문서를 참고하세요. Postmark 문서 역시 각각 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)를 참고할 수 있습니다.

Amazon SES를 사용하는 경우에는 `metadata` 메서드에서 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer를 기반으로 합니다. Laravel은 메시지를 보내기 전에 Symfony 메시지 인스턴스를 조작할 수 있도록 사용자 정의 콜백을 등록할 수 있게 해 줍니다. 이를 위해 `Envelope` 정의에 `using` 파라미터를 지정하세요:

```
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지 Envelope 얻기
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        using: [
            function (Email $message) {
                // 커스터마이징 작업 수행
            },
        ]
    );
}
```

<a name="markdown-mailables"></a>
## 마크다운 메일러블 (Markdown Mailables)

마크다운 메일러블은 미리 만들어진 [메일 알림](/docs/11.x/notifications#mail-notifications)의 템플릿과 컴포넌트를 활용해 메시지를 작성할 수 있습니다. 마크다운 문법으로 작성되므로, Laravel은 반응형 HTML뿐 아니라 자동으로 플레인 텍스트 버전도 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

마크다운 템플릿과 연동되는 메일러블을 생성하려면, `make:mail` Artisan 명령의 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그 후, 메일러블의 `content` 메서드 내에서 `view` 대신 `markdown` 파라미터를 사용해 `Content` 정의를 구성하세요:

```
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지 내용 정의 가져오기
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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 조합해 쉽고 빠르게 메일 메시지를 작성할 수 있으며, Laravel 기본 이메일 UI 컴포넌트를 활용합니다:

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
> 마크다운 이메일 작성 시 너무 과도한 들여쓰기는 피하세요. 마크다운 표준에 따라 들여쓰기된 내용은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링하며, `url`과 선택적 `color` 인자를 받습니다. 지원하는 색상은 `primary`, `success`, `error`입니다. 한 메시지 내에 버튼 컴포넌트를 여러 개 넣을 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 배경색이 약간 다른 박스에 텍스트를 렌더링해 특정 내용을 강조할 때 사용합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 표를 HTML 테이블로 변환합니다. 기본적인 마크다운 테이블 정렬 문법을 지원합니다:

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

모든 마크다운 메일 컴포넌트를 애플리케이션 내로 내보내어 원하는 대로 수정할 수 있습니다. 컴포넌트를 내보내려면 `vendor:publish` Artisan 명령어로 `laravel-mail` 태그를 지정합니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령으로 `resources/views/vendor/mail` 디렉토리에 컴포넌트가 복사됩니다. `mail` 폴더 하위에 `html`과 `text` 폴더가 있고, 각각의 컴포넌트가 포함되어 있습니다. 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보낸 뒤, `resources/views/vendor/mail/html/themes` 디렉토리에 `default.css` 파일이 있습니다. 이 CSS 파일을 수정하면, 마크다운 메일 메시지 HTML에 자동으로 인라인 스타일로 적용됩니다.

새 테마를 만드려면, `html/themes` 디렉토리에 CSS 파일을 추가 후, `config/mail.php`의 `theme` 옵션을 그 파일명으로 설정하세요.

개별 메일러블 클래스에서 테마를 지정하려면, 메일러블 클래스 속성 `$theme`에 테마명을 설정할 수 있습니다.

<a name="sending-mail"></a>
## 메일 보내기 (Sending Mail)

메일을 보내려면 `Mail` [파사드](/docs/11.x/facades)의 `to` 메서드를 사용합니다. `to`는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 인수로 받습니다. 객체나 컬렉션을 넘길 경우, 메일러는 자동으로 그 객체(들)의 `email` 및 `name` 속성을 수신자 정보로 사용하니, 해당 속성들이 있는지 확인하세요. 수신자를 지정한 후에는 메일러블 클래스 인스턴스를 `send` 메서드에 넘기면 됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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

        // 주문 배송 처리...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

메일 발송 시 수신자를 "to"뿐만 아니라 "cc"와 "bcc"로 지정할 수도 있습니다. 각 메서드를 체이닝하면 됩니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 루프 처리

때때로 수신자 배열을 반복해 모두에게 메일을 보내야 할 때가 있습니다. 그런데 `to`는 수신자 목록을 누적해서 저장하므로, 루프 내에서 메일러블 인스턴스를 매번 새로 생성하지 않으면 이전 수신자들에게도 반복해서 메일이 발송됩니다. 항상 루프 내에서 새로운 메일러블 인스턴스를 만들어서 사용하세요:

```
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

기본적으로 Laravel은 `config/mail.php`의 기본 메일러로 메일을 전송합니다. 하지만 `mailer` 메서드를 사용해 특정 메일러를 지정할 수 있습니다:

```
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉하기 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉하기

메일 발송은 애플리케이션 응답에 영향을 줄 가능성이 있으므로, 많은 개발자가 메일 메시지를 백그라운드 큐에 넣어 비동기로 발송합니다. Laravel은 이를 간단히 처리할 수 있게 [통합 큐 API](/docs/11.x/queues)를 제공합니다. 큐에 넣으려면, 수신자 지정을 한 후 `queue` 메서드를 사용하세요:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 자동으로 작업을 큐에 넣어 백그라운드에서 전송하도록 처리합니다. 이용 전에 [큐 설정](/docs/11.x/queues)을 완료해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메시지 큐잉

큐에 넣는 메일 발송을 일정 시간 뒤로 미루고 싶으면 `later` 메서드를 사용하세요. 첫 번째 인자로 `DateTime` 인스턴스를 전달해 발송 시간을 지정합니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 작업 넣기

`make:mail` 명령어로 생성되는 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용합니다. 따라서 메일러블 인스턴스에 `onQueue`, `onConnection` 메서드를 호출해 큐 연결명과 큐 이름을 지정할 수 있습니다:

```
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

특정 메일러블 클래스를 항상 큐에 넣고 싶다면, `ShouldQueue` 계약을 클래스에 구현하면 됩니다. 이렇게 하면 `send` 메서드를 호출해도 큐에 넣어 발송합니다:

```
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 DB 트랜잭션

데이터베이스 트랜잭션 중에 큐잉된 메일러블이 디스패치되면, 트랜잭션 커밋 전에 큐 처리될 수 있습니다. 이 경우 트랜잭션 내에서 변경한 모델이나 DB 레코드가 반영되지 않아 오류가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정이 `false`이면, 메일 발송 시 `afterCommit` 메서드를 호출해 트랜잭션 커밋 완료 후에 작업이 디스패치되게 할 수 있습니다:

```
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 클래스 생성자 내에서 `afterCommit`을 호출할 수도 있습니다:

```
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
     * 새 메시지 인스턴스 생성
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]  
> 큐 작업과 트랜잭션 사이 문제에 관한 더 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/11.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링 (Rendering Mailables)

메일을 실제로 보내지 않고, 메일러블의 HTML 콘텐츠를 문자열 형태로 얻고 싶을 때가 있습니다. 이럴 때는 메일러블 인스턴스의 `render` 메서드를 호출하세요. 렌더링된 HTML을 문자열로 반환합니다:

```
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인할 때 브라우저에서 바로 미리보기하는 것이 편리합니다. Laravel은 라우트 클로저나 컨트롤러에서 메일러블을 바로 반환하면, 실제 메일 발송 없이 브라우저에 HTML을 렌더링해 보여줍니다:

```
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 지역화 (Localizing Mailables)

Laravel은 요청의 현재 로케일과 다른 로케일로 메일러블을 보내는 것을 지원하며, 큐에도 이 로케일 정보를 기억시킬 수 있습니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정하세요. 메일러블 템플릿 평가 시 설정된 로케일로 바꾸었다가, 완료 후 원래 로케일로 되돌립니다:

```
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자의 선호 로케일

때로는 애플리케이션에 각 사용자의 선호 로케일이 저장되어 있습니다. 그럴 때는 모델이 `HasLocalePreference` 계약을 구현하도록 하고, 선호 로케일을 반환하도록 하면 Laravel이 자동으로 해당 로케일을 사용합니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자가 선호하는 로케일 반환
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면, 메일러블이나 알림 발송 시 자동으로 선호 언어를 사용하므로 별도로 `locale` 메서드를 호출할 필요가 없습니다:

```
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트

Laravel은 메일러블 구조를 검사하는 다양한 메서드를 제공합니다. 특히 메일러블 내용이 예상대로 포함되었는지 테스트하는 여러 메서드가 있습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등이 있습니다.

"HTML" 어서션은 HTML 버전의 메일러블에 특정 문자열이 포함됐는지 확인하며, "text" 어서션은 플레인 텍스트 버전에 대해 작동합니다:

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

메일러블 내용 테스트와는 별도로, 메일이 특정 사용자에게 "전송됨"을 확인하는 테스트도 분리해 작성하는 것이 좋습니다. 메일 내용은 테스트 코드와 무관한 경우가 많으므로, 간단히 Laravel이 메일 전송 지시를 받았는지만 검증하는 편이 일반적입니다.

메일이 실제로 전송되는 것을 막으려면 `Mail` 파사드의 `fake` 메서드를 사용하세요. `fake` 호출 후에는 메일이 전송 요청됐는지, 전송 횟수, 수신자 등도 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 배송 처리...

    // 메일이 전송되지 않았음을 검증...
    Mail::assertNothingSent();

    // 특정 메일러블이 전송됨을 검증...
    Mail::assertSent(OrderShipped::class);

    // 특정 메일러블이 두 번 전송됨을 검증...
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일 주소로 메일러블이 전송됨을 검증...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 여러 이메일 주소로 메일러블 전송 검증...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 다른 메일러블이 전송되지 않음을 검증...
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3건의 메일러블이 전송됨을 검증...
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

        // 메일이 전송되지 않았음을 검증...
        Mail::assertNothingSent();

        // 특정 메일러블이 전송됨을 검증...
        Mail::assertSent(OrderShipped::class);

        // 특정 메일러블이 두 번 전송됨을 검증...
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 이메일 주소로 메일러블이 전송됨을 검증...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // 여러 이메일 주소로 메일러블 전송 검증...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // 다른 메일러블이 전송되지 않음을 검증...
        Mail::assertNotSent(AnotherMailable::class);

        // 총 3건의 메일러블이 전송됨을 검증...
        Mail::assertSentCount(3);
    }
}
```

메일을 백그라운드 큐에 넣는 경우에는 `assertSent` 대신 `assertQueued`를 사용하세요:

```
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 클로저를 넘겨 조건에 맞는 메일러블이 존재하는지 검증할 수도 있습니다. 조건에 맞는 메일러블이 한 건이라도 있으면 성공입니다:

```
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

검증용 클로저에 전달되는 메일러블 인스턴스는 다음과 같은 수신객체 검사 메서드를 제공합니다:

```
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...');
});
```

첨부파일 검사도 여러 메서드로 지원합니다:

```
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

메일이 "전송 안 됨"을 검증하는 메서드는 `assertNotSent`와 `assertNotQueued` 두 가지가 있습니다. 만약 메일이 보내지거나 큐에 들어가지 않은 상태임을 모두 확인하고 싶다면, `assertNothingOutgoing`과 `assertNotOutgoing` 메서드를 사용하세요:

```
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 (Mail and Local Development)

이메일을 발송하는 애플리케이션을 개발할 때, 실제 이메일이 전송되어 실제 수신자가 이메일을 받는 것을 원하지 않을 수 있습니다. Laravel은 이런 로컬 개발 환경에서 메일 발송을 "사용 중지"하거나 대체하는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

메일을 실제로 전송하는 대신, 모든 이메일 메시지를 로그 파일에 기록하는 `log` 메일 드라이버가 있습니다. 보통 로컬 개발 시에 활용합니다. 각 환경 설정 방법에 대해선 [환경별 설정 문서](/docs/11.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또 다른 방법으로는, [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io) 같은 서비스를 `smtp` 드라이버와 함께 사용해 실제 이메일을 전송하지 않고 테스트용 우편함에서 확인하는 것입니다. 이런 방식의 장점은 최종 이메일을 메일 클라이언트처럼 보여주는 Mailtrap 뷰어에서 직접 확인 가능하다는 점입니다.

Laravel Sail을 사용하는 경우, [Mailpit](https://github.com/axllent/mailpit)을 통해 메일을 미리 볼 수 있습니다. Sail 실행 중이라면 다음 주소에서 Mailpit 인터페이스에 접속할 수 있습니다: `http://localhost:8025`.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

개발 환경에서 항상 특정 이메일 주소로만 메일을 보내고 싶다면, `Mail` 파사드의 `alwaysTo` 메서드를 사용하세요. 이 메서드는 보통 서비스 프로바이더 내 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 메시지 전송 시 두 개의 이벤트를 발행합니다. `MessageSending` 이벤트는 메일 발송 직전에, `MessageSent` 이벤트는 메일 발송 후에 발생합니다. 주의할 점은, 이벤트는 메일을 *전송할 때* 발생하며, *큐잉할 때*는 발생하지 않는다는 점입니다. 이 이벤트에 대한 [이벤트 리스너](/docs/11.x/events)를 애플리케이션 내에 정의해 활용할 수 있습니다:

```
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * 이벤트 핸들러
     */
    public function handle(MessageSending $event): void
    {
        // 이벤트 처리 작업...
    }
}
```

<a name="custom-transports"></a>
## 커스텀 전송기 (Custom Transports)

Laravel은 다양한 메일 전송기를 기본 제공하지만, 지원하지 않는 다른 서비스 연동을 위해 직접 전송기를 작성하고 싶을 수 있습니다. 이를 위해 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속받고 `doSend`와 `__toString()` 메서드를 구현하면 됩니다:

```
use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * 새 Mailchimp 전송기 인스턴스 생성
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
     * 전송기의 문자열 표현 반환
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

정의한 전송기는 `Mail` 파사드의 `extend` 메서드를 사용해 등록합니다. 보통 `AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 다음과 같이 등록하세요. 클로저는 `config/mail.php` 설정에 정의된 메일러 구성 배열을 `$config` 매개변수로 받습니다:

```
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        return new MailchimpTransport(/* ... */);
    });
}
```

커스텀 전송기를 등록한 후에는 `config/mail.php`에 새 전송기를 사용할 메일러 항목을 추가할 수 있습니다:

```
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송기

Laravel은 Mailgun, Postmark 같은 Symfony 커뮤니티가 관리하는 전송기를 기본 지원합니다. 만약 Brevo(구 Sendinblue) 같은 다른 Symfony 전송기를 Laravel에 추가하고 싶으면, 필요한 패키지를 Composer로 설치한 뒤 전송기를 등록하세요. 예를 들어 Brevo 패키지 설치는 다음과 같습니다:

```none
composer require symfony/brevo-mailer symfony/http-client
```

설치 후 `services` 설정 파일에 Brevo API 키 등 설정을 추가합니다:

```
'brevo' => [
    'key' => 'your-api-key',
],
```

그 다음, 서비스 프로바이더 `boot` 메서드에서 `Mail` 파사드의 `extend`를 사용해 전송기를 등록합니다:

```
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * 애플리케이션 서비스 부트스트랩
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

전송기 등록 후에는 `config/mail.php`에 새 전송기를 사용하는 메일러 항목을 추가합니다:

```
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```