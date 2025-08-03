# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [장애 조치 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
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
- [메일러블 다국어 처리](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 컨텐츠 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [로컬 개발 환경의 메일 처리](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 전송은 복잡할 필요가 없습니다. Laravel은 널리 사용되는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 하는 깔끔하고 단순한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 통한 이메일 발송용 드라이버를 제공하므로 로컬 또는 클라우드 기반 서비스 중 원하는 것으로 빠르게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 구성된 각 메일러는 고유한 설정과 전송 방식(transport)을 가질 수 있어, 애플리케이션이 특정 이메일 메시지를 보낼 때 각각 다른 이메일 서비스를 사용하는 것도 가능합니다. 예를 들어, 트랜잭션 이메일은 Postmark로, 대량 이메일은 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 안에는 `mailers` 배열이 있습니다. 이 배열은 Laravel에서 지원하는 주요 메일 드라이버/전송 방식별 샘플 구성 항목을 포함하고 있습니다. 또한 `default` 설정값은 애플리케이션에서 이메일을 전송할 때 기본으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 사전 요구사항 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend, MailerSend 같은 API 기반 드라이버는 SMTP 서버를 통해 메일을 보내는 것보다 보통 더 간단하고 빠릅니다. 가능하면 이러한 드라이버를 사용하는 것이 좋습니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer로 Symfony의 Mailgun Mailer 전송 방식을 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 기본 메일러를 `mailgun`으로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고 `mailers` 배열에 다음 구성을 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

마지막으로 `config/services.php` 파일에 다음 옵션들을 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

만약 미국 이외의 [Mailgun 리전](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용한다면, 자신의 리전 엔드포인트로 `services` 설정 파일에서 정의할 수 있습니다:

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer로 Symfony의 Postmark Mailer 전송 방식을 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php` 설정 파일의 `default` 값을 `postmark`로 설정하세요. 그리고 `config/services.php` 파일에 다음 옵션이 포함되어 있는지 확인합니다:

```php
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에 대해 사용할 Postmark 메시지 스트림을 지정하려면, 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. `config/mail.php` 설정 파일 내 메일러 배열에 다음과 같이 구성할 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이를 통해 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러도 설정할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Resend의 PHP SDK를 Composer로 설치하세요:

```shell
composer require resend/resend-php
```

설정에서 기본 메일러를 `resend`로 지정한 뒤, `config/services.php` 파일에 다음 옵션을 포함하세요:

```php
'resend' => [
    'key' => env('RESEND_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 우선 Amazon AWS SDK for PHP를 설치해야 합니다. Composer를 통해 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

이후 `config/mail.php` 파일에서 기본 메일러를 `ses`로 설정하고, `config/services.php` 구성에 다음 옵션들이 포함되어 있는지 확인하세요:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면 `token` 키를 `ses` 설정에 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 연동하려면, 메일 메시지 클래스의 [headers](#headers) 메서드에서 `X-Ses-List-Management-Options` 헤더를 포함하도록 설정할 수 있습니다:

```php
/**
 * 메일 메시지 헤더 반환.
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

AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 지정하려면, `ses` 설정에 `options` 배열을 정의할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일과 SMS 서비스로 자체 API 기반 Laravel 메일 드라이버를 제공합니다. Composer로 해당 패키지를 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

설치 후, 애플리케이션 `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 또한 `MAIL_MAILER` 환경 변수는 `mailersend`로 설정되어야 합니다:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로 `config/mail.php`의 `mailers` 배열에 MailerSend를 추가합니다:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

호스팅 템플릿 사용법 등 MailerSend 관련 자세한 정보는 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치 설정 (Failover Configuration)

때때로, 애플리케이션 메일 전송에 사용되는 외부 서비스가 다운될 수 있습니다. 이럴 경우 기본 전송 드라이버가 동작하지 않을 때 사용할 하나 이상의 백업 메일 전송 구성을 정의하면 유용합니다.

이를 위해 `failover` 전송 방식을 사용하는 메일러를 애플리케이션의 `mail` 설정 파일에 정의하세요. `failover` 메일러 설정 배열에는 전송에 사용할 메일러 이름들의 배열(`mailers`)이 포함되어야 합니다. 순서대로 사용 가능한 메일러를 선택해 메일을 전송합니다:

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

이 `failover` 메일러를 애플리케이션의 기본 메일러로 사용하려면 `default` 설정에 이름을 지정하세요:

```php
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드 로빈 설정 (Round Robin Configuration)

`roundrobin` 전송 방식은 다중 메일러에 걸쳐 메일 발송 부하를 분산할 수 있도록 돕습니다. 시작하려면 `roundrobin` 전송 방식을 사용하는 메일러를 `mail` 설정 파일에 정의하세요. `mailers` 배열에는 메일 발송에 사용할 메일러 목록이 포함되어야 합니다:

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

설정을 마치면 `default` 설정에 `roundrobin` 메일러 이름을 지정하여 기본 메일러로 사용하세요:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

`roundrobin` 전송은 등록된 메일러 목록 중 무작위로 선택 후, 이어지는 이메일마다 다음 메일러를 순서대로 선택해 발송합니다. 이는 장애 시 대체 사용을 목표로 하는 `failover` 전송과 달리 *로드 밸런싱(load balancing)* 을 제공하는 방식입니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기 (Generating Mailables)

Laravel 애플리케이션에서 보내는 메일 유형별로 "메일러블" 클래스가 존재합니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, `make:mail` Artisan 명령어로 첫 번째 메일러블 클래스를 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기 (Writing Mailables)

메일러블 클래스를 생성한 후, 내부 구성을 살펴보겠습니다. 메일러블 설정은 `envelope`, `content`, `attachments` 등의 여러 메서드에서 수행됩니다.

`envelope` 메서드는 메일 제목(subject)과 경우에 따라 수신자(recipient)를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 이메일 내용 생성을 위한 [Blade 템플릿](/docs/12.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope 사용하기

먼저, 이메일 발신자 설정 방법을 살펴봅니다. 즉, "from" 주소를 지정하는 방법입니다. 기본적으로 두 가지 방법이 있습니다. 첫 번째는 메시지의 envelope에 "from" 주소를 명시하는 것입니다:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope 반환
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

만약 애플리케이션의 모든 이메일이 동일한 "from" 주소를 사용한다면, 매 메일러블 클래스마다 지정하는 것은 번거롭습니다. 이 경우 `config/mail.php` 설정 파일에서 전역 "from" 주소를 지정할 수 있습니다. 메일러블에서 별도로 지정하지 않으면 이 주소가 기본으로 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, 전역 "reply_to" 주소도 같은 설정 파일에서 정의할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서 `view`를 정의하여 이메일 내용 렌더링에 사용할 템플릿을 지정할 수 있습니다. 각 이메일은 보통 [Blade 템플릿](/docs/12.x/blade)로 내용이 렌더링되므로, Blade 템플릿 엔진의 모든 기능을 활용할 수 있습니다:

```php
/**
 * 메시지 내용 정의 반환
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> [!NOTE]
> 이메일 템플릿을 모아두기 위해 `resources/views/mail` 디렉터리를 생성하는 것을 권장하지만, `resources/views` 내 어디에 두어도 무방합니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하려면, `Content` 정의 시 `text` 파라미터에 일반 텍스트용 템플릿 명을 지정하세요. HTML 템플릿(`view`)과 일반 텍스트 템플릿(`text`)을 모두 정의할 수 있습니다:

```php
/**
 * 메시지 내용 정의 반환
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
#### 공개 속성(public properties) 활용

일반적으로 이메일 내용을 렌더링할 때 사용할 데이터를 뷰에 전달해야 합니다. 이때 두 가지 방법이 있습니다. 첫 번째는 메일러블 클래스 내 정의된 공개 속성(public property)이 자동으로 뷰에서 사용 가능해지는 것입니다. 예를 들어 생성자에서 데이터를 전달받아 공개 속성에 할당할 수 있습니다:

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
     * 새로운 인스턴스 생성
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * 메시지 내용 정의 반환
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

뷰에서는 글로벌 데이터처럼 쉽게 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 활용

이메일 데이터를 템플릿에 전달하기 전에 포맷을 직접 처리하고 싶다면, `Content` 정의의 `with` 파라미터로 데이터를 명시적으로 전달할 수 있습니다. 이 경우 생성자에서 전달받은 데이터는 `protected` 또는 `private` 속성에 저장해 뷰에 자동으로 노출되지 않도록 합니다:

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
     * 새로운 인스턴스 생성
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * 메시지 내용 정의 반환
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

`with`를 통해 전달된 데이터는 Blade 템플릿에서 다음과 같이 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일 (Attachments)

이메일에 첨부파일을 추가하려면 메시지 클래스의 `attachments` 메서드에서 첨부파일 배열을 반환해야 합니다. 먼저 `Attachment` 클래스의 `fromPath`를 사용해 파일 경로를 지정할 수 있습니다:

```php
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

첨부파일의 표시 이름이나 MIME 타입을 지정하려면 `as`와 `withMime` 메서드를 함께 사용할 수 있습니다:

```php
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
#### 저장소 디스크에서 첨부파일 추가

파일시스템([filesystem disks](/docs/12.x/filesystem))에 저장된 파일을 첨부하려면 `fromStorage` 메서드를 사용할 수 있습니다:

```php
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

이때도 `as`와 `withMime`으로 이름과 MIME 타입 지정이 가능합니다:

```php
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

기본 디스크 외 특정 디스크를 지정하려면 `fromStorageDisk` 메서드를 사용하세요:

```php
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
#### Raw 데이터 첨부파일

메모리 내에서 생성한 PDF 등, 원시 바이트(raw string)를 첨부하려면 `fromData` 메서드를 사용할 수 있습니다. 클로저 내부에서 raw 데이터를 반환하며, 두 번째 인자로 첨부파일명도 지정해야 합니다:

```php
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

이메일에 인라인 이미지 삽입은 번거로울 수 있지만, Laravel은 편리한 방법을 제공합니다. 템플릿 내부에서 `$message` 변수의 `embed` 메서드를 사용해 인라인 이미지를 삽입할 수 있습니다. Laravel은 모든 메일 템플릿에 `$message` 변수를 자동으로 제공합니다:

```blade
<body>
    여기 이미지가 있습니다:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메일 템플릿에서는 사용할 수 없습니다. 일반 텍스트 메일은 인라인 첨부파일을 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 인라인 첨부

이미 원시 이미지 데이터를 보유하고 있다면, `$message` 변수의 `embedData` 메서드를 호출하여 첨부할 수 있습니다. 이때 첨부 이미지에 부여할 파일명도 인자로 제공합니다:

```blade
<body>
    원시 데이터에서 이미지 첨부:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체 (Attachable Objects)

첨부파일을 단순 파일 경로 대신 클래스 객체 형태로 표현할 때가 많습니다. 예를 들어 사진을 첨부할 때, `Photo` 모델 객체를 그대로 첨부 메서드에 전달할 수 있다면 편리할 것입니다. 첨부 가능한 객체를 사용하면 이를 구현할 수 있습니다.

우선, 첨부 가능한 객체 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 이 인터페이스는 `toMailAttachment` 메서드를 요구하며, 여기서 `Illuminate\Mail\Attachment` 객체를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 메일 첨부 표현 반환
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

그 다음, 메일러블의 `attachments` 메서드에서 해당 객체 인스턴스를 반환하면 됩니다:

```php
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

파일이 Amazon S3 같은 원격 파일 저장소에 있을 때도, Laravel은 파일시스템 디스크에서 데이터를 읽어 첨부 인스턴스를 생성할 수 있도록 지원합니다:

```php
// 기본 디스크의 파일로부터 첨부 생성
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일로부터 첨부 생성
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리에 보유한 데이터를 클로저로 반환하여 첨부 인스턴스를 만들 수 있습니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

이 밖에 `as`, `withMime` 메서드를 사용해 첨부 파일 이름이나 MIME 유형을 커스터마이징 가능합나다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

추가 헤더를 메일에 붙여야 하는 경우가 있습니다. 예를 들어, 커스텀 `Message-Id` 헤더나 임의의 텍스트 헤더 등이 그 예입니다.

이때, 메일러블 클래스에 `headers` 메서드를 정의하여 `Illuminate\Mail\Mailables\Headers` 객체를 반환하세요. 이 객체는 `messageId`, `references`, `text` 파라미터를 인자로 받으며 필요한 것만 지정하면 됩니다:

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * 메시지 헤더 반환
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

Mailgun, Postmark 같은 일부 서드파티 메일 제공자는 메일 그룹화 및 추적을 위한 "태그(tags)"와 "메타데이터(metadata)" 기능을 지원합니다. `Envelope` 정의 내에서 태그와 메타데이터를 추가할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope 반환
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

Mailgun 드라이버를 쓴다면 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 관한 Mailgun 문서를 참고하세요. Postmark도 [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)를 지원하며, 문서를 참조할 수 있습니다.

Amazon SES를 이용한다면, `metadata`를 통해 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메일에 붙일 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징 (Customizing the Symfony Message)

Laravel의 메일은 Symfony Mailer 위에서 동작합니다. Symfony 메시지를 전송하기 전 더욱 세밀하게 조작하고 싶으면, `Envelope` 정의에 `using` 파라미터로 커스텀 콜백을 등록할 수 있습니다. 콜백에는 Symfony 메시지 인스턴스가 전달됩니다:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지 envelope 반환
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

마크다운 메일러블은 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있게 해줍니다. 메시지가 마크다운으로 작성되며, Laravel은 이를 아름답고 반응형인 HTML 템플릿으로 렌더링하며 자동으로 일반 텍스트 버전도 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

마크다운 템플릿이 포함된 메일러블을 생성하려면 `make:mail` Artisan 명령어에 `--markdown` 옵션을 지정하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그 다음 `content` 메서드 내 `Content` 정의 시 `view` 대신 `markdown` 파라미터를 사용하세요:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지 내용 정의 반환
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

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 결합해 간단히 메일 메시지를 제작할 수 있으며, Laravel이 미리 정의한 메일 UI 컴포넌트를 사용할 수 있습니다:

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
> 마크다운 이메일 작성 시 과도한 들여쓰기는 피하세요. 마크다운 표준에 따라 들여쓰기는 코드 블록으로 처리됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 생성합니다. `url`과 선택적 `color` 인자를 받으며, 색상은 `primary`, `success`, `error`를 지원합니다. 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 메시지 배경색과 약간 다르게 되어 주목을 끌 수 있는 패널에 텍스트를 표시합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

마크다운 테이블을 HTML 테이블로 변환하는 컴포넌트입니다. 마크다운의 기본 테이블 정렬 구문을 지원합니다:

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

마크다운 메일 컴포넌트를 애플리케이션 내로 내보내어 수정할 수 있습니다. 아래 명령어를 통해 `laravel-mail` 태그로 배포하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

해당 명령은 `resources/views/vendor/mail` 디렉터리에 컴포넌트를 배포하며, HTML 및 텍스트 각각 디렉터리가 포함되어 있습니다. 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 배포하면 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. CSS를 수정하면, 변경된 스타일이 마크다운 메일 메시지의 HTML에 자동으로 인라인 스타일로 적용됩니다.

새로운 테마를 만들려면 `html/themes` 디렉터리에 CSS 파일을 생성하세요. 그리고 `config/mail.php` 설정 파일에서 `theme` 옵션을 새 테마 이름으로 변경합니다.

특정 메일러블 클래스에 대해 테마를 사용하려면, 클래스 내 `$theme` 속성에 테마 이름을 지정하세요.

<a name="sending-mail"></a>
## 메일 보내기 (Sending Mail)

메일을 보내려면 `Mail` [파사드(facade)](/docs/12.x/facades)의 `to` 메서드를 사용하세요. `to`에 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 전달할 수 있습니다. 객체나 컬렉션을 전달할 경우, 메일러는 자동으로 `email`과 `name` 속성을 수신자 정보로 사용하므로 해당 속성이 반드시 존재해야 합니다. 수신자를 지정하고 나서, 메일러블 클래스 인스턴스를 `send` 메서드에 넘겨 메일을 보낼 수 있습니다:

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

        // 배송 처리...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

"to" 수신자만 지정하는 것이 아니라, "cc", "bcc" 수신자도 다음과 같이 메서드 체인으로 추가할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 전송

수신자 배열을 반복하며 메일러블을 보내야 할 때가 있습니다. `to` 메서드는 수신자 목록을 누적해 추가하므로, 반복문을 돌 때마다 이전 수신자에게도 메일이 다시 전송될 수 있습니다. 따라서 반복할 때마다 새 메일러블 인스턴스를 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 이용해 메일 보내기

기본적으로 Laravel은 설정된 기본 메일러를 통해 메일을 보냅니다. 하지만 `mailer` 메서드를 사용하면 특정 메일러를 지정해 메일을 보낼 수 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉하기 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 전송은 애플리케이션 응답 시간을 저하시킬 수 있으므로, 백그라운드 작업으로 처리하는 경우가 많습니다. Laravel은 내장된 [공통 큐 API](/docs/12.x/queues)를 통해 이를 쉽게 처리합니다. 메시지를 큐에 보내려면, 수신자를 지정한 뒤 `queue` 메서드를 호출하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

백그라운드에서 전송 작업을 담당할 큐 구성은 반드시 사전에 설정되어 있어야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 전송 큐잉

큐에 넣은 메일 전달 시점을 지연시키려면 `later` 메서드를 사용하세요. 첫 번째 인자로 `DateTime` 인스턴스를 받으며, 해당 시점까지 기다린 후 메시지를 보냅니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 작업 추가하기

`make:mail` 명령어로 생성된 메일러블 클래스는 기본적으로 `Illuminate\Bus\Queueable` 트레이트를 사용합니다. 따라서 메시지 인스턴스에 `onQueue`와 `onConnection` 메서드를 호출해 큐 이름이나 연결을 설정할 수 있습니다:

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

메일러블 클래스에 `ShouldQueue` 계약을 구현하면, `send` 메서드를 호출해도 항상 큐에 쌓이도록 할 수 있습니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 메일과 데이터베이스 트랜잭션 함께 쓰기

데이터베이스 트랜잭션 내에서 큐에 쌓인 메일러블이 커밋 전에 실행되면, 모델이나 레코드의 최신 상태가 반영되지 않을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델이나 레코드는 아직 DB에 없을 수도 있어 오류를 유발합니다.

큐 연결의 `after_commit` 설정이 `false`인 경우라면, 메일 메시지를 보낼 때 `afterCommit` 메서드를 호출해 트랜잭션 커밋 후에 메시지가 처리되도록 지정할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자에서 호출해도 됩니다:

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
     * 새 인스턴스 생성
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 큐 작업과 DB 트랜잭션 관련 문제 해결법은 [큐와 데이터베이스 트랜잭션 문서](/docs/12.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐 이메일 실패 처리

큐에 쌓인 이메일 전송 실패 시, 메일러블 클래스 내 `failed` 메서드가 정의되어 있다면 실패 원인 `Throwable`을 인자로 호출됩니다:

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
     * 큐 메시지 실패 처리
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링 (Rendering Mailables)

메일을 실제로 보내지 않고, 메일러블의 HTML 내용을 캡처할 때가 있습니다. 이를 위해 메일러블의 `render` 메서드를 호출하면 렌더링된 HTML 문자열을 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿 디자인을 빠르게 확인하려면, 메일러블 객체를 라우트 클로저나 컨트롤러에서 직접 반환하면 브라우저에 렌더링된 HTML이 표시됩니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 다국어 처리 (Localizing Mailables)

Laravel은 요청의 현재 로케일(locale)과 다르게 메일러블을 특정 로케일로 전송할 수 있으며, 큐에 들어가도 이 로케일을 기억합니다.

이 기능을 사용하려면 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정하세요. 메일러블 템플릿 렌더링 시 해당 로케일이 자동으로 활성화됩니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

사용자의 선호 로케일을 저장하는 경우, 모델에 `HasLocalePreference` 계약을 구현하면 Laravel이 자동으로 해당 로케일을 사용합니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일 반환
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스 구현 후에는 `locale` 메서드를 호출하지 않아도 이 로케일이 자동 적용됩니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 컨텐츠 테스트

Laravel은 메일러블 구조를 점검하고 예상한 내용을 포함했는지 테스트하는 다양한 메서드를 제공합니다:

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

"HTML" 관련 assertion은 메일러블의 HTML 버전에 특정 문자열 포함 여부를 확인하며, "텍스트" 관련 assertion은 일반 텍스트 버전을 확인합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트

메일러블 내용 테스트와 메일 전송 여부 테스트는 분리해서 하는 것이 좋습니다. 일반적으로 메일 컨텐츠는 테스트 코드와 큰 관련이 없으며, Laravel이 해당 메일러블을 전송하도록 지시했는지만 확인하면 충분합니다.

`Mail` 파사드의 `fake` 메서드를 사용하면 메일 전송이 실제로 이루어지지 않게 가짜 환경을 만들 수 있고, 이후 전송 여부를 검사할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 배송 처리...

    // 아무 메일도 보내지 않았음 검사
    Mail::assertNothingSent();

    // 특정 메일러블이 전송되었음 검사
    Mail::assertSent(OrderShipped::class);

    // 특정 메일러블이 두 번 전송되었음 검사
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일로 메일러블이 전송되었음 검사
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 여러 이메일 주소로 메일러블 전송 검사
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 특정 메일러블이 전송되지 않았음 검사
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3건의 메일러블 전송 여부 검사
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

큐에 넣어 메일을 전송하는 경우에는 `assertSent` 대신 `assertQueued`를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 클로저를 넘겨 조건을 검사할 수도 있습니다. 해당 클로저에서 `true`를 반환하면 assertion이 성공합니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 assertion 메서드에 넘겨지는 메일러블 인스턴스는 수신자, 제목, 메일러 등 여러 검사에 유용한 메서드를 포함합니다:

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

첨부파일 관련 검사도 도와주는 메서드들이 있습니다:

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

메일 전송이나 큐잉 모두 없었음을 검사하려면 `assertNothingOutgoing`, 특정 조건에 맞는 메일이 없음을 검사하려면 `assertNotOutgoing` 메서드를 사용하세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 로컬 개발 환경의 메일 처리 (Mail and Local Development)

개발 중 실제 이메일이 전송되는 것은 원치 않을 수 있습니다. Laravel은 여러 방법으로 실제 메일 전송을 "비활성화"할 수 있습니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 메일을 전송하는 대신 모든 메시지를 로그 파일에 기록합니다. 보통 로컬 개발 시 사용합니다. 환경별 설정 관련 자세한 내용은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

[HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스를 SMTP 드라이버와 함께 쓰면, 실제 이메일이 아니라 테스트용 메일박스로 전달되어 이메일 클라이언트에서 확인할 수 있습니다.

Laravel Sail을 사용하는 경우, [Mailpit](https://github.com/axllent/mailpit)를 사용해 메일 미리보기가 가능합니다. Sail 실행 중에는 `http://localhost:8025`에서 Mailpit 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

전역으로 모든 메일을 특정 주소로 보내려면 `Mail` 파사드의 `alwaysTo` 메서드를 사용하세요. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```php
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

Laravel은 메일 전송 시 두 종류 이벤트를 발생시킵니다. 메일 전송 전에 `MessageSending` 이벤트, 전송 완료 후에 `MessageSent` 이벤트가 각각 발생합니다. 이 이벤트들은 메일이 *전송되는 시점*에 발생하며, 큐에 들어갔을 때가 아닙니다. 애플리케이션 내에 이벤트 리스너를 만들어 처리할 수 있습니다:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * 이벤트 핸들러
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## 커스텀 전송 방식 (Custom Transports)

Laravel은 다양한 메일 전송 방식을 기본 제공합니다. 하지만 지원하지 않는 서비스를 위한 전송 방식을 직접 구현할 수도 있습니다. `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속해 전송 클래스를 만들고, `doSend`와 `__toString` 메서드를 구현하세요:

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
     * Mailchimp 전송 인스턴스 생성자
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
     * 전송 방식 문자열 표현 반환
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

정의한 전송 클래스를 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `Mail` 파사드의 `extend` 메서드로 등록합니다. `$config` 인자는 `config/mail.php` 설정 배열이 전달됩니다:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * 애플리케이션 서비스 부트스트랩
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

등록 후 `config/mail.php`에서 해당 전송 방식을 사용하는 메일러를 정의하세요:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식

Mailgun, Postmark 외에도 Symfony에서 관리하는 전송 방식을 지원하기 위해, 필요한 Symfony 메일러를 Composer로 설치하고 Laravel에 등록할 수 있습니다. 예를 들어 "Brevo"(옛 Sendinblue) Symfony 메일러 설치 및 등록 방법은 다음과 같습니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```

`services` 설정 파일에 Brevo API 키를 추가하세요:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

서비스 프로바이더 내 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드로 등록합니다:

```php
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

등록 완료 후 `config/mail.php`의 메일러 배열에 새 전송 방식을 이용하도록 정의하세요:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```