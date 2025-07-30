# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [페일오버 설정](#failover-configuration)
    - [라운드로빈 설정](#round-robin-configuration)
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
- [Markdown 메일러블](#markdown-mailables)
    - [Markdown 메일러블 생성하기](#generating-markdown-mailables)
    - [Markdown 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 콘텐츠 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 드라이버](#custom-transports)
    - [추가 Symfony 전송 드라이버](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. Laravel은 널리 사용되는 [Symfony Mailer](https://symfony.com/doc/6.2/mailer.html) 컴포넌트를 기반으로 하는 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Amazon SES, `sendmail`을 통한 메일 전송용 드라이버를 제공하여, 로컬 또는 클라우드 기반의 원하는 서비스로 손쉽게 메일을 보낼 수 있도록 합니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에서 각 메일러는 고유한 설정과 독립적인 "전송(transport)"을 가질 수 있어, 애플리케이션이 특정 이메일 메시지를 보내기 위해 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 거래 이메일에는 Postmark를, 대량 이메일에는 Amazon SES를 사용하는 식입니다.

`mail` 설정 파일 내에는 `mailers` 설정 배열이 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송별 샘플 설정 항목이 포함되어 있으며, `default` 설정 값은 애플리케이션이 이메일을 보낼 때 기본으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 사전 요구사항

Mailgun, Postmark, MailerSend 같은 API 기반 드라이버는 SMTP 서버를 통한 메일 전송보다 보통 더 간단하고 빠릅니다. 가능한 경우 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 전송을 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `mailgun`으로 설정하세요. 기본 메일러를 구성한 후에는 `config/services.php` 설정 파일에 다음 항목들이 있는지 확인합니다:

```
'mailgun' => [
    'transport' => 'mailgun',
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
],
```

미국 이외의 [Mailgun 지역](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용하는 경우, `services` 설정 파일에서 해당 지역 엔드포인트를 정의할 수 있습니다:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
],
```

<a name="postmark-driver"></a>
#### Postmark 드라이버

Postmark 드라이버를 사용하려면, Composer를 통해 Symfony의 Postmark Mailer 전송을 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 설정하세요. 기본 메일러를 구성한 후 `config/services.php` 파일에 다음 항목이 있는지 확인합니다:

```
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하고 싶다면, 애플리케이션의 `config/mail.php` 내 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

```
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
],
```

이렇게 여러 Postmark 메일러를 서로 다른 메시지 스트림과 함께 구성할 수 있습니다.

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 우선 Amazon AWS PHP SDK를 설치해야 합니다. Composer 패키지 매니저를 통해 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 후, `config/mail.php` 설정 파일의 `default` 옵션을 `ses`로 설정하고 `config/services.php` 설정 파일에 다음 항목들이 포함되어 있는지 확인합니다:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

Laravel이 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면, `ses` 설정 내에 `options` 배열을 설정할 수 있습니다:

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

[MailerSend](https://www.mailersend.com/)는 거래용 이메일 및 SMS 서비스로, Laravel용 API 기반 메일 드라이버 패키지를 제공합니다. 해당 패키지는 Composer로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하고, `MAIL_MAILER` 환경 변수는 `mailersend`로 설정해야 합니다:

```shell
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

MailerSend 및 호스팅 템플릿 사용법에 대한 자세한 내용은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 페일오버 설정

사용 중인 외부 메일 전송 서비스가 다운될 수 있습니다. 이런 경우에 대비해 백업 메일 전송 구성을 한 개 이상 정의해두면, 기본 전송 드라이버가 실패할 때 백업 설정을 순서대로 사용하여 메일을 보낼 수 있습니다.

이를 위해 애플리케이션의 `mail` 설정 파일에서 `failover` 전송 방식의 메일러를 정의하세요. `failover` 메일러 설정 배열은 전송에 사용할 메일러 이름 목록을 포함한 `mailers` 배열을 가집니다:

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

`failover` 메일러를 정의했다면, 애플리케이션에서 기본 메일러로 사용하도록 `mail` 설정 파일의 `default` 키 값을 `failover`로 지정하세요:

```
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="round-robin-configuration"></a>
### 라운드로빈 설정

`roundrobin` 전송은 여러 개의 메일러에 메일 전송 부하를 분산시키는 데 사용됩니다. 사용하려면 `roundrobin` 전송을 사용하는 메일러를 `mail` 설정 파일에 정의하세요. `mailers` 배열은 사용할 메일러 목록을 담습니다:

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

정의 후, 애플리케이션의 기본 메일러로 쓰도록 `default` 키 값을 `roundrobin`으로 지정합니다:

```
'default' => env('MAIL_MAILER', 'roundrobin'),
```

`roundrobin` 전송은 목록 내 메일러 중 하나를 무작위로 선택해 전송하고, 그 다음부터 순차적으로 다른 메일러로 전환됩니다. 반면에 `failover`는 *[고가용성](https://en.wikipedia.org/wiki/High_availability)*을 목표로 하지만, `roundrobin`은 *[부하 분산](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 기능을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기

Laravel 애플리케이션에서 전송하는 이메일 유형마다 "mailable" 클래스로 표현합니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 해당 폴더가 없다면, `make:mail` Artisan 명령어로 첫 메일러블 클래스를 생성할 때 자동으로 생성됩니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기

메일러블 클래스를 생성한 뒤, 내용을 열어 구성 방식을 살펴보세요. 메일러블은 `envelope`, `content`, `attachments` 메서드 등에서 설정합니다.

`envelope` 메서드는 메시지의 제목과 수신자(가끔)를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메일 메시지 콘텐츠 생성을 위한 [Blade 템플릿](/docs/10.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope 사용하기

먼저 이메일의 발신자를 설정하는 방법을 살펴보겠습니다. 이메일이 누가 보낸지 지정하는 두 가지 방법이 있습니다. 첫째, 메시지 Envelope에서 "from" 주소를 명시할 수 있습니다:

```
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope을 반환합니다.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

필요하다면 `replyTo` 주소도 설정할 수 있습니다:

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

모든 이메일에 동일한 "from" 주소를 사용한다면, 메일러블 클래스마다 일일이 지정하는 대신 `config/mail.php` 설정 파일에서 전역 "from" 주소를 지정하는 것이 편리합니다. 이 주소는 메일러블 클래스 내에서 별도로 "from" 주소를 지정하지 않았을 경우 사용됩니다:

```
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

마찬가지로, 전역 "reply_to" 주소도 `config/mail.php`에서 지정할 수 있습니다:

```
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰 설정

메일러블 클래스의 `content` 메서드에서, 이메일 내용을 렌더링할 템플릿인 `view`를 지정할 수 있습니다. 각 이메일은 보통 [Blade 템플릿](/docs/10.x/blade)을 사용해 HTML을 생성하므로, 이메일 HTML 작성 시 Blade 템플릿 엔진의 강력한 기능을 그대로 활용할 수 있습니다:

```
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
> `resources/views/emails` 디렉터리를 생성해 모든 이메일 템플릿을 모아도 좋고, `resources/views` 내 원하는 위치에 자유롭게 배치해도 됩니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

일반 텍스트 버전을 정의하려면, `Content` 정의에서 `text` 파라미터를 지정하세요. `view`가 HTML용 템플릿 이름이라면, `text`는 일반 텍스트용 템플릿 이름입니다. HTML과 일반 텍스트 버전을 모두 자유롭게 정의할 수 있습니다:

```
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

명확한 표현을 위해 `html` 파라미터를 `view` 파라미터의 별칭으로 사용할 수도 있습니다:

```
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### 공개 속성으로 전달하기

보통 이메일 HTML을 렌더링할 때 사용할 데이터를 템플릿에 전달합니다. 방법은 두 가지인데, 첫째로 메일러블 클래스 내 정의된 모든 공개(public) 속성은 자동으로 뷰에 전달됩니다. 예를 들어, 생성자에서 데이터를 받아 공개 속성으로 저장할 수 있습니다:

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
     * 새로운 메시지 인스턴스 생성자.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * 메시지 콘텐츠 정의 반환.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

일단 공개 속성에 데이터가 설정되면, Blade 템플릿 내에서 일반 데이터처럼 접근할 수 있습니다:

```
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터로 전달하기

템플릿에 전달하기 전, 데이터를 가공하거나 변형하려면 `Content` 정의의 `with` 파라미터를 통해 직접 데이터를 넘길 수 있습니다. 이때 생성자는 데이터를 `protected` 또는 `private` 속성에 저장해 템플릿에 직접 노출되지 않도록 처리하는 것이 일반적입니다:

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
     * 새로운 메시지 인스턴스 생성자.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * 메시지 콘텐츠 정의 반환.
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

이렇게 넘긴 데이터는 Blade 템플릿에서 직접 아래와 같이 사용할 수 있습니다:

```
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메일러블 클래스의 `attachments` 메서드가 반환하는 배열에 `Attachment` 인스턴스를 넣어야 합니다. 파일 경로를 지정해 첨부할 때는 `Attachment` 클래스의 `fromPath` 메서드를 사용할 수 있습니다:

```
use Illuminate\Mail\Mailables\Attachment;

/**
 * 메시지에 첨부할 파일들을 반환합니다.
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

첨부파일에 표시 이름이나 MIME 타입을 지정하려면 `as`와 `withMime` 메서드를 체이닝해서 사용할 수 있습니다:

```
/**
 * 메시지에 첨부할 파일들을 반환합니다.
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

[파일시스템 디스크](/docs/10.x/filesystem)에 저장된 파일이라면 `fromStorage` 첨부 메서드를 사용해 첨부할 수 있습니다:

```
/**
 * 메시지에 첨부할 파일들을 반환합니다.
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

물론 이름과 MIME 타입도 지정 가능합니다:

```
/**
 * 메시지에 첨부할 파일들을 반환합니다.
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

기본 디스크 외에 다른 디스크에서 파일을 첨부하려면 `fromStorageDisk` 메서드를 사용하세요:

```
/**
 * 메시지에 첨부할 파일들을 반환합니다.
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

`fromData` 첨부 메서드는 메모리 내에서 생성한 PDF 같은 원시 바이트 문자열을 첨부하는 데 유용합니다. 파일을 디스크에 쓰지 않고 보내고 싶을 때 사용하세요. 이 메서드는 원시 데이터 바이트를 반환하는 클로저와 첨부파일에 지정할 이름을 받습니다:

```
/**
 * 메시지에 첨부할 파일들을 반환합니다.
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

이메일 내에 이미지를 바로 삽입하는 작업은 보통 번거로운데, Laravel은 인라인 이미지를 편리하게 첨부하는 방식을 제공합니다. 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용해 이미지를 삽입하세요. Laravel은 모든 이메일 템플릿에 `$message` 변수를 자동으로 제공합니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]  
> `$message` 변수는 일반 텍스트 메일 템플릿에서는 제공되지 않습니다. 일반 텍스트 메일은 인라인 첨부를 사용하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 인라인 첨부하기

이미 원시 이미지 데이터 문자열을 가지고 있다면, `$message`의 `embedData` 메서드를 사용해 삽입할 수 있습니다. 이때 첨부 이미지 파일명을 인자로 제공해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체

파일 경로 문자열만으로 첨부하는 방식도 좋지만, 애플리케이션 내 객체로 첨부 엔티티를 표현하는 경우엔 조금 다릅니다. 예를 들어 사진을 첨부한다면, Photo 모델이 있을 수 있습니다. 이런 객체를 그냥 `attach` 메서드에 넘기는 방식이 편리합니다.

시작하려면, 첨부할 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 이 인터페이스는 `toMailAttachment` 메서드를 정의하도록 요구하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 메일 첨부 가능한 표현을 반환합니다.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

첨부 가능한 객체를 정의했다면, 메일 메시지 작성 시 `attachments` 메서드에서 해당 객체 인스턴스를 반환하면 됩니다:

```
/**
 * 메시지에 첨부할 파일들을 반환합니다.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

첨부 파일 데이터를 Amazon S3 같은 원격 파일 저장 서비스에 저장할 수도 있으므로, Laravel은 [파일시스템 디스크](/docs/10.x/filesystem)에 저장된 데이터로부터도 첨부를 생성할 수 있습니다:

```
// 기본 디스크의 파일로부터 첨부 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일로부터 첨부 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

메모리 내 데이터를 활용해 첨부를 생성하려면 `fromData` 메서드에 원시 데이터를 반환하는 클로저를 넘겨주세요:

```
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부 시 파일 이름이나 MIME 타입 설정을 위해 `as`, `withMime` 메서드도 사용할 수 있습니다:

```
return Attachment::fromPath('/path/to/file')
        ->as('Photo Name')
        ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

특정 메시지에 임의의 추가 헤더를 붙여야 할 때가 있습니다. 예를 들어 `Message-Id` 같은 헤더를 커스터마이징하거나 다른 텍스트 헤더를 추가하고 싶은 경우입니다.

이럴 때는 메일러블 클래스에 `headers` 메서드를 정의하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 등의 파라미터를 받을 수 있습니다. 필요한 항목만 지정해도 됩니다:

```
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

Mailgun, Postmark 같은 서드파티 이메일 제공자에서는 이메일 메시지에 "태그(tags)"와 "메타데이터(metadata)"를 지원합니다. 이를 통해 애플리케이션에서 보낸 메일을 분류하고 추적할 수 있습니다. 이들은 메일러블 클래스의 `Envelope` 정의에서 추가할 수 있습니다:

```
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope 반환.
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

Mailgun 드라이버를 사용하는 경우, [Mailgun 태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1) 및 [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages)에 대해 Mailgun 문서를 참고하세요. Postmark에 대해서는 [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원 문서를 참고하면 됩니다.

Amazon SES를 사용할 경우, 메일 메시지에 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙이려면 `metadata` 메서드를 사용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer를 사용합니다. 메시지 전송 전에 Symfony 메시지 인스턴스를 인자로 받는 커스텀 콜백을 등록할 수 있어 메시지를 세밀하게 조정할 수 있습니다. 이를 위해 `Envelope` 정의에 `using` 파라미터를 설정하면 됩니다:

```
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지 envelope 반환.
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

Markdown 메일러블 메시지를 사용하면 [메일 알림(mail notifications)](/docs/10.x/notifications#mail-notifications)에 내장된 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있습니다. Markdown으로 작성된 메시지는 아름답고 반응형인 HTML 템플릿으로 렌더링되며, 동시에 일반 텍스트 버전도 자동 생성됩니다.

<a name="generating-markdown-mailables"></a>
### Markdown 메일러블 생성하기

`make:mail` Artisan 명령어에 `--markdown` 옵션을 써서 Markdown 템플릿이 연결된 메일러블을 생성할 수 있습니다:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그 다음, 메일러블 클래스 `content` 메서드에서 `view` 대신 `markdown` 파라미터로 템플릿을 지정하세요:

```
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지 콘텐츠 정의 반환.
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
### Markdown 메시지 작성하기

Markdown 메일러블은 Blade 컴포넌트와 Markdown 문법을 함께 사용해 쉽게 메시지를 구성할 수 있으며, Laravel이 미리 만들어둔 이메일 UI 컴포넌트를 활용합니다:

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
> Markdown 이메일 작성 시 과도한 들여쓰기는 피하세요. Markdown 표준에 따라 들여쓰기는 코드 블록으로 인식될 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 인수를 받습니다. 지원하는 색상은 `primary`, `success`, `error` 입니다. 메시지에 원하는 만큼 버튼을 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 메시지의 나머지 부분과 약간 다른 배경색을 가진 박스 형태로 텍스트 블록을 렌더링합니다. 주의를 환기시키기 좋습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 Markdown 표를 HTML 테이블로 변환해줍니다. 콘텐츠에 Markdown 테이블을 작성하면 되고, 열 정렬도 Markdown 표 기본 문법을 지원합니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

Markdown 메일 컴포넌트를 애플리케이션으로 내보내어 직접 수정할 수 있습니다. `vendor:publish` Artisan 명령어로 `laravel-mail` 태그를 지정해 컴포넌트를 배포하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

그러면 `resources/views/vendor/mail` 디렉터리에 Markdown 메일 컴포넌트가 배포됩니다. `html`과 `text` 폴더 각각에 해당 컴포넌트의 표현이 들어 있으며, 원하는 대로 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보낸 뒤, `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 있습니다. 이 파일에서 CSS를 수정하면 Markdown 메일 메시지의 HTML 표현에 인라인 CSS로 자동 변환됩니다.

완전히 새로운 테마를 제작하고 싶으면, `html/themes` 디렉터리에 CSS 파일을 만들고 저장하세요. 그 뒤에 애플리케이션의 `config/mail.php` 파일 내 `theme` 옵션을 새 테마 이름으로 변경합니다.

개별 메일러블에 대해 테마를 지정하려면, 메일러블 클래스의 `$theme` 속성에 사용할 테마 이름을 설정하세요.

<a name="sending-mail"></a>
## 메일 전송

`Mail` [파사드](/docs/10.x/facades)의 `to` 메서드를 사용해 메일을 보냅니다. `to` 메서드는 이메일 주소 문자열, 유저 인스턴스, 또는 유저 컬렉션을 인자로 받습니다. 객체 또는 컬렉션을 넘기면, 메일러는 그 객체들의 `email` 및 `name` 속성을 자동으로 사용하여 수신자를 결정합니다. 수신자를 지정한 후, 메세지를 보낼 메일러블 클래스 인스턴스를 `send` 메서드에 전달하세요:

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
     * 주문을 배송 처리합니다.
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

메일 전송 시 "to" 수신자뿐 아니라 "cc", "bcc" 수신자도 함께 설정할 수 있습니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 배열 순회 전송

수신자 배열을 루프 돌며 메일을 보내야 할 때가 있습니다. 그러나 `to` 메서드가 수신자 목록에 주소를 추가하는 방식이므로, 메일러블 인스턴스를 매번 새로 생성하지 않으면 이전 수신자들에게도 중복 발송됩니다. 따라서 항상 루프마다 새 메일러블 인스턴스를 생성하세요:

```
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

기본적으로 Laravel은 `mail` 설정에서 `default`로 지정한 메일러를 사용합니다. 특정 메일러를 지정하려면 `mailer` 메서드를 사용하세요:

```
Mail::mailer('postmark')
        ->to($request->user())
        ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐에 넣기

메일 전송은 서버 응답 속도에 영향을 줄 수 있어, 백그라운드 작업으로 처리하는 개발자가 많습니다. Laravel은 내장 [통합 큐 API](/docs/10.x/queues)를 사용해 쉽게 큐잉할 수 있습니다. 메시지 수신자를 지정한 뒤 `queue` 메서드로 메일을 큐에 넣으세요:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

큐잉 시 작업이 백그라운드에서 처리됩니다. 이 기능을 사용하려면 [큐 설정](/docs/10.x/queues)이 먼저 되어 있어야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 큐잉

예약 전송을 원할 경우 `later` 메서드를 사용하세요. 첫 번째 인자로 `DateTime` 인스턴스를 받아, 그 시점부터 메일을 전송합니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/커넥션 사용하기

`make:mail` 명령어로 생성되는 메일러블 클래스들은 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, 메일러블 인스턴스에 `onQueue` 및 `onConnection` 메서드를 호출할 수 있어 큐 이름과 큐 커넥션을 지정할 수 있습니다:

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
#### 기본적으로 큐잉하기

항상 큐에 넣어야 하는 메일러블 클래스가 있다면, 해당 클래스에서 `ShouldQueue` 계약을 구현하세요. 이렇게 하면 `send` 메서드를 호출해도 메일이 큐에 들어갑니다:

```
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉 메일러블과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 큐잉된 메일러블은 트랜잭션이 완료되기 전에 작업이 실행될 수 있습니다. 이 경우 트랜잭션 내에서 변경한 데이터가 메일러블 처리 시점에 아직 DB에 반영되어 있지 않을 수 있어, 의도치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`일 때, 특정 큐잉 메일러블을 데이터베이스 트랜잭션 커밋 후에 처리하도록 강제하려면, 메일 전송 시 `afterCommit` 메서드를 호출하세요:

```
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자 내에서 `afterCommit` 메서드를 호출할 수도 있습니다:

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
     * 새 메시지 인스턴스 생성.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]  
> 이러한 이슈 해결 방법에 대해 더 알고 싶으면, [큐잉 작업과 데이터베이스 트랜잭션](/docs/10.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링

메일을 전송하지 않고, HTML 내용을 문자열로 얻고 싶을 수 있습니다. 이때는 메일러블 인스턴스의 `render` 메서드를 호출하면, 메일 내용이 렌더링된 HTML 문자열로 반환됩니다:

```
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿을 디자인하는 동안, 일반 Blade 템플릿처럼 브라우저에서 바로 렌더링 결과를 확인하고 싶을 때가 있습니다. 이럴 때는 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 직접 반환하면, 메일러블이 렌더링되어 브라우저에 표시됩니다:

```
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 지역화

애플리케이션 요청의 현재 로케일과 다른 언어로 메일러블을 보낼 수 있으며, 큐잉된 경우에도 이 로케일 정보를 기억합니다.

이를 위해 `Mail` 파사드의 `locale` 메서드를 사용해 원하는 언어를 지정할 수 있습니다. 메일 템플릿이 평가되는 동안 애플리케이션이 해당 로케일로 변경되었다가, 평가 종료 후에는 원래 로케일로 복구됩니다:

```
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

앱에서 각 사용자의 선호 로케일을 저장할 경우, `HasLocalePreference` 계약을 모델에 구현하면 Laravel이 메일 전송 시 자동으로 그 로케일을 사용합니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일 반환.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

인터페이스를 구현하면, 메일이나 알림 전송 시 별도의 `locale` 호출 없이도 선호 로케일이 자동 적용됩니다:

```
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### 메일러블 콘텐츠 테스트

Laravel은 메일러블 구조를 검사하는 다양한 메서드를 지원합니다. 특히 예상되는 내용을 포함하는지 검사하는 간편한 메서드를 제공합니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등이 있습니다.

"HTML" 어설션은 메일의 HTML 버전에 대해, "텍스트" 어설션은 일반 텍스트 버전에 대해 검사합니다:

```
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

메일러블 내용 테스트와, 특정 메일러블이 특정 사용자에게 "전송되었는지"를 검증하는 테스트를 분리하는 것이 좋습니다. 보통 메일 내부 내용은 테스트 대상 코드와 무관하기 때문에, Laravel이 특정 메일러블을 보내도록 지시했는지만 확인해도 충분하기 때문입니다.

`Mail` 파사드의 `fake` 메서드를 호출하면 메일 전송을 막고 테스트 중 검사할 수 있습니다. 이후 메일 전송 여부를 다음과 같이 확인할 수 있습니다:

```
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

        // 주문 배송 실행...

        // 메일러블이 전송되지 않았는지 확인...
        Mail::assertNothingSent();

        // 특정 메일러블 전송 여부 확인...
        Mail::assertSent(OrderShipped::class);

        // 특정 메일러블이 2회 이상 전송되었는지 확인...
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 메일러블이 전송되지 않았는지 확인...
        Mail::assertNotSent(AnotherMailable::class);

        // 총 3건의 메일러블 전송이 있었는지 확인...
        Mail::assertSentCount(3);
    }
}
```

메일러블을 큐잉하는 경우에는 `assertSent` 대신 `assertQueued` 메서드를 사용합니다:

```
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 클로저를 넘겨, 특정 조건을 만족하는 메일러블이 전송되었는지 검사할 수도 있습니다. 조건을 통과하는 메일러블이 한 번이라도 존재하면 테스트 통과입니다:

```
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

또, 클로저에 전달된 메일러블 인스턴스는 다음과 같은 수신자 및 제목 관련 도움 메서드를 제공합니다:

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

첨부파일의 존재 여부를 확인하는 메서드도 있습니다:

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

메일 전송과 큐잉에 대해 모두 메일이 없었음을 확인하고 싶을 때는 `assertNothingOutgoing`와 `assertNotOutgoing` 메서드를 사용하세요:

```
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발

메일 전송 기능을 개발할 때, 실제로 외부로 메일을 보내고 싶지 않은 경우가 많습니다. Laravel은 로컬 개발 환경에서 메일 전송을 "중지"시키거나 "대체"할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

메일을 보내는 대신 로그 파일에 메일 메시지를 기록하는 `log` 메일 드라이버가 있습니다. 주로 로컬 개발 환경에서 사용합니다. 환경별 설정 방법은 [환경 설정 문서](/docs/10.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io) 같은 서비스를 `smtp` 드라이버와 함께 사용해 메일을 가상 수신함으로 보내 실제 이메일 클라이언트처럼 확인할 수 있습니다. Mailtrap의 메시지 뷰어로 전송된 최종 메일을 살펴볼 수 있어 장점입니다.

[Laravel Sail](/docs/10.x/sail)을 사용하는 경우 [Mailpit](https://github.com/axllent/mailpit)을 사용해 메일을 확인할 수 있습니다. Sail 구동 중일 때 다음 주소에서 Mailpit 인터페이스를 열 수 있습니다: `http://localhost:8025`.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, 모든 이메일을 특정 주소로 강제로 보내고 싶다면 `Mail` 파사드의 `alwaysTo` 메서드를 사용하세요. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 로컬 환경인 경우 호출합니다:

```
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Laravel은 메일 전송 과정에서 두 가지 이벤트를 발생시킵니다. 메시지 전송 전에 발생하는 `MessageSending` 이벤트와, 메시지 전송 후 발생하는 `MessageSent` 이벤트입니다. 이 이벤트들은 메일이 전송(실제 발송)될 때 발생하며, 큐잉 시점에는 발생하지 않습니다.

이벤트 리스너는 `App\Providers\EventServiceProvider` 내 `$listen` 배열에 등록할 수 있습니다:

```
use App\Listeners\LogSendingMessage;
use App\Listeners\LogSentMessage;
use Illuminate\Mail\Events\MessageSending;
use Illuminate\Mail\Events\MessageSent;

/**
 * 애플리케이션 이벤트 리스너 매핑.
 *
 * @var array
 */
protected $listen = [
    MessageSending::class => [
        LogSendingMessage::class,
    ],

    MessageSent::class => [
        LogSentMessage::class,
    ],
];
```

<a name="custom-transports"></a>
## 커스텀 전송 드라이버

Laravel은 여러 메일 전송 드라이버를 내장하지만, 직접 원하는 외부 서비스용 전송 드라이버를 작성해서 Laravel에 통합할 수 있습니다. 시작하려면 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 클래스를 정의하세요. 그리고 `doSend`와 `__toString()` 메서드를 구현합니다:

```
use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Mailchimp 전송 인스턴스 생성.
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
     * 전송 드라이버 문자열 표현 반환.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

커스텀 전송 클래스를 정의했다면, `Mail` 파사드의 `extend` 메서드를 사용해 등록할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에서 등록하며, `$config` 인자는 `config/mail.php` 내 메일러 설정 배열입니다:

```
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        return new MailchimpTransport(/* ... */);
    });
}
```

등록 후엔 `config/mail.php` 내 메일러 정의에서 새 전송 방식을 사용할 수 있습니다:

```
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 드라이버

Laravel은 Mailgun, Postmark 등의 Symfony 전송을 기본 제공하지만, 추가 Symfony 전송을 Composer로 설치해 Laravel에 등록할 수도 있습니다. 예를 들어 "Brevo" (이전 "Sendinblue") Symfony 메일러를 설치하려면 다음을 실행하세요:

```none
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, `config/services.php`에 Brevo API 키를 추가합니다:

```
'brevo' => [
    'key' => 'your-api-key',
],
```

이제 서비스 프로바이더의 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드로 등록할 수 있습니다:

```
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * 애플리케이션 서비스 부트스트랩.
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

등록 후 `config/mail.php` 설정에 Brevo 전송을 사용하는 메일러 정의를 추가하세요:

```
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```