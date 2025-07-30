# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
    - [페일오버 설정](#failover-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [보내는 사람 설정하기](#configuring-the-sender)
    - [뷰 설정하기](#configuring-the-view)
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
- [메일러블 현지화](#localizing-mailables)
- [메일러블 테스트하기](#testing-mailables)
- [로컬 개발 시 메일](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송자 (Custom Transports)](#custom-transports)
    - [추가 Symfony 전송자](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/6.0/mailer.html) 컴포넌트를 기반으로 하는 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Amazon SES, `sendmail`을 통한 이메일 전송 드라이버를 제공하여, 로컬 또는 클라우드 기반 서비스 중 원하는 서비스로 빠르게 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내에 설정된 각각의 메일러는 고유한 설정과 심지어 고유한 "전송자(transport)"를 가질 수 있어, 특정 이메일 메시지에 대해 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 애플리케이션은 트랜잭션 이메일에는 Postmark를 사용하고, 대량 이메일에는 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 내의 `mailers` 구성 배열에는 Laravel에서 지원하는 주요 메일 드라이버/전송자 각각의 샘플 설정이 포함되어 있고, `default` 설정값은 애플리케이션이 이메일 메시지를 보낼 때 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송자 필수 조건

Mailgun, Postmark 같은 API 기반 드라이버는 종종 SMTP 서버를 통한 메일 전송보다 더 간단하고 빠릅니다. 가능하면 이들 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 전송자를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `mailgun`으로 설정하세요. 애플리케이션의 기본 메일러를 구성한 후, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하세요:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
],
```

미국 이외 지역의 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용하는 경우, `services` 설정 파일에 리전의 엔드포인트를 정의할 수 있습니다:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
],
```

<a name="postmark-driver"></a>
#### Postmark 드라이버

Postmark 드라이버를 사용하려면, Composer를 통해 Symfony의 Postmark Mailer 전송자를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 설정하세요. 기본 메일러를 구성한 뒤, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하세요:

```
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하려면, `config/mail.php`의 해당 메일러 설정 배열에 `message_stream_id` 옵션을 추가하세요:

```
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
],
```

이렇게 하면 여러 Postmark 메일러를 각기 다른 메시지 스트림으로 설정할 수 있습니다.

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS PHP SDK를 설치해야 합니다. Composer 패키지 매니저로 다음을 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 다음 옵션들이 포함되어 있는지 확인하세요:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면 SES 설정에 `token` 키를 추가하세요:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

또한, Laravel이 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하려면 `ses` 설정 내에 `options` 배열을 지정할 수 있습니다:

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

<a name="failover-configuration"></a>
### 페일오버 설정

외부 메일 전송 서비스가 일시적으로 다운될 경우를 대비해 백업 메일 전송 구성을 설정하는 것이 유용할 수 있습니다.

이를 위해, 애플리케이션의 `mail` 설정 파일에 `failover` 전송자를 사용하는 메일러를 정의하세요. 이 `failover` 메일러 설정 배열에 `mailers` 배열을 포함하여, 전송자 선택 우선순위를 지정할 수 있습니다:

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

이후, 애플리케이션의 `mail` 설정 파일에서 `default` 키의 값으로 이 페일오버 메일러 이름을 지정해 기본 메일러로 설정하세요:

```
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="generating-mailables"></a>
## 메일러블 생성하기

Laravel 앱에서 보내는 각 이메일 종류는 "메일러블(mailable)" 클래스 형태로 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 아직 해당 디렉토리가 없다면, `make:mail` Artisan 명령어를 사용해 첫 번째 메일러블 클래스를 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기

메일러블 클래스를 생성했다면, 내부를 열어 내용을 살펴봅시다. 메일러블 클래스 설정은 `envelope`, `content`, `attachments` 메서드를 포함한 여러 메서드에서 이뤄집니다.

`envelope` 메서드는 메시지의 제목(subject) 및 때로는 수신자 정보를 담은 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성하는 데 쓰일 [Blade 템플릿](/docs/9.x/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 보내는 사람 설정하기

<a name="using-the-envelope"></a>
#### Envelope을 이용한 설정

먼저, 이메일의 보내는 사람(From)을 설정하는 방법을 살펴봅시다. 보통 이메일의 발신자를 뜻합니다. 두 가지 방법이 있는데, 우선 메시지의 envelope에서 "from" 주소를 지정할 수 있습니다:

```
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope()
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

필요시 `replyTo` 주소도 지정할 수 있습니다:

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

애플리케이션 내 모든 이메일에 같은 "from" 주소를 사용한다면, 메일러블 클래스마다 `from` 메서드를 호출하는 것은 번거롭습니다. 대신, `config/mail.php` 파일에서 전역 `from` 주소를 지정할 수 있습니다. 이 주소는 메일러블 클래스에 별도 from이 지정되지 않은 경우 기본값으로 사용됩니다:

```
'from' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

마찬가지로 전역 `reply_to` 주소도 설정할 수 있습니다:

```
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰 설정하기

메일러블 클래스의 `content` 메서드 내에서 이메일 콘텐츠를 렌더링할 템플릿(view)을 지정할 수 있습니다. 대개 이메일은 [Blade 템플릿](/docs/9.x/blade)을 사용해 HTML 내용을 만듭니다. Blade 템플릿 엔진의 강력함과 편리함을 그대로 활용할 수 있습니다:

```
/**
 * 메시지 콘텐츠 정의를 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Content
 */
public function content()
{
    return new Content(
        view: 'emails.orders.shipped',
    );
}
```

> [!NOTE]
> 이메일 템플릿은 보통 `resources/views/emails` 디렉토리에 모아두는 것이 좋지만, `resources/views` 디렉토리 내라면 원하는 곳에 자유롭게 둘 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일에 일반 텍스트 버전도 정의하고 싶다면, 메일 메시지 `Content` 정의 시 `text` 매개변수를 지정하면 됩니다. 이는 `view`와 마찬가지로 렌더링할 템플릿 이름이어야 하며, HTML 버전과 일반 텍스트 버전 모두를 정의할 수 있습니다:

```
/**
 * 메시지 콘텐츠 정의를 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Content
 */
public function content()
{
    return new Content(
        view: 'emails.orders.shipped',
        text: 'emails.orders.shipped-text'
    );
}
```

명확하게 하려면, `html` 매개변수는 `view`의 별칭으로도 사용할 수 있습니다:

```
return new Content(
    html: 'emails.orders.shipped',
    text: 'emails.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 속성 이용하기

일반적으로, 이메일 HTML을 렌더링할 때 뷰에 전달할 데이터를 지정해야 합니다. 데이터를 뷰에 전달하는 방법은 두 가지가 있습니다. 우선, 메일러블 클래스에 정의된 모든 public 속성은 자동으로 뷰에 전달됩니다. 예를 들어, 생성자 인수로 받은 데이터를 public 속성으로 저장할 수 있습니다:

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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    public $order;

    /**
     * 새로운 메시지 인스턴스 생성.
     *
     * @param  \App\Models\Order  $order
     * @return void
     */
    public function __construct(Order $order)
    {
        $this->order = $order;
    }

    /**
     * 메시지 콘텐츠 정의를 가져옵니다.
     *
     * @return \Illuminate\Mail\Mailables\Content
     */
    public function content()
    {
        return new Content(
            view: 'emails.orders.shipped',
        );
    }
}
```

public 속성으로 데이터가 설정되면, 뷰에서 Blade 템플릿 내에서 다음처럼 접근할 수 있습니다:

```
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 매개변수 이용하기

이메일 데이터의 포맷을 템플릿으로 보내기 전에 커스터마이징하고 싶다면, `Content` 정의의 `with` 파라미터로 데이터를 직접 전달할 수도 있습니다. 보통 생성자로 데이터를 받고, 이를 protected 또는 private 속성에 저장하여 뷰에 자동 전달되지 않게 합니다:

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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    protected $order;

    /**
     * 새로운 메시지 인스턴스 생성.
     *
     * @param  \App\Models\Order  $order
     * @return void
     */
    public function __construct(Order $order)
    {
        $this->order = $order;
    }

    /**
     * 메시지 콘텐츠 정의를 가져옵니다.
     *
     * @return \Illuminate\Mail\Mailables\Content
     */
    public function content()
    {
        return new Content(
            view: 'emails.orders.shipped',
            with: [
                'orderName' => $this->order->name,
                'orderPrice' => $this->order->price,
            ],
        );
    }
}
```

`with`를 통해 전달된 데이터는 뷰에서 다음과 같이 접근할 수 있습니다:

```
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, 메시지의 `attachments` 메서드가 반환하는 배열에 첨부를 추가하면 됩니다. 우선, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 지정해 첨부할 수 있습니다:

```
use Illuminate\Mail\Mailables\Attachment;

/**
 * 메시지의 첨부파일을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Attachment[]
 */
public function attachments()
{
    return [
        Attachment::fromPath('/path/to/file'),
    ];
}
```

첨부 시, 파일 표시명과 MIME 타입도 `as`, `withMime` 메서드로 지정할 수 있습니다:

```
/**
 * 메시지의 첨부파일을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Attachment[]
 */
public function attachments()
{
    return [
        Attachment::fromPath('/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf'),
    ];
}
```

<a name="attaching-files-from-disk"></a>
#### 디스크 저장 파일 첨부

저장소([filesystem disks](/docs/9.x/filesystem))에 저장된 파일을 첨부하려면 `fromStorage` 메서드를 사용할 수 있습니다:

```
/**
 * 메시지의 첨부파일을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Attachment[]
 */
public function attachments()
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

물론, 이름과 MIME 타입도 지정할 수 있습니다:

```
/**
 * 메시지의 첨부파일을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Attachment[]
 */
public function attachments()
{
    return [
        Attachment::fromStorage('/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf'),
    ];
}
```

기본 디스크가 아닌 특정 디스크에서 가져오려면 `fromStorageDisk` 메서드를 사용하세요:

```
/**
 * 메시지의 첨부파일을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Attachment[]
 */
public function attachments()
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

`fromData` 메서드는 메모리 상에 있는 바이트 문자열 같은 원시 데이터를 첨부 파일로 첨부할 때 사용할 수 있습니다. 예를 들어, 메모리 내에서 생성한 PDF를 디스크에 저장하지 않고 바로 첨부하는 경우입니다. `fromData`는 원시 데이터를 반환하는 클로저와 첨부 파일 이름을 인수로 받습니다:

```
/**
 * 메시지의 첨부파일을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Attachment[]
 */
public function attachments()
{
    return [
        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
                ->withMime('application/pdf'),
    ];
}
```

<a name="inline-attachments"></a>
### 인라인 첨부파일

이메일에 인라인 이미지를 임베드하는 작업은 보통 까다로운데, Laravel은 이를 편리하게 하는 방법을 제공합니다. 이메일 템플릿 내에서 `$message` 변수에 대해 `embed` 메서드를 호출하면, 해당 이미지를 인라인으로 첨부할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에서 기본으로 제공되므로 직접 전달할 필요가 없습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 일반 텍스트 메시지 템플릿에서는 제공되지 않습니다. 일반 텍스트 이메일은 인라인 첨부를 사용하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 인라인 첨부

이미 원시 이미지 데이터 문자열이 있다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이 때 임베드할 이미지에 할당할 파일명도 전달해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 첨부 가능한 객체

일반적으로 단순한 문자열 경로로 파일을 첨부하지만, 경우에 따라 애플리케이션 내 첨부 대상이 클래스 형태일 수 있습니다. 예를 들어, 사진을 첨부한다면 `Photo` 모델도 함께 존재할 수 있죠. 이런 경우, `Photo` 모델 자체를 `attach` 메서드에 넘기는 것이 편리합니다. 이를 위해 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 해당 인터페이스는 `toMailAttachment` 메서드를 정의하며, 이 메서드는 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * 메일 첨부 표현을 반환합니다.
     *
     * @return \Illuminate\Mail\Attachment
     */
    public function toMailAttachment()
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

첨부 가능한 객체를 정의했으면, 이메일 메시지를 빌드할 때 `attachments` 메서드에서 이 객체 인스턴스를 반환할 수 있습니다:

```
/**
 * 메시지 첨부파일을 가져옵니다.
 *
 * @return array
 */
public function attachments()
{
    return [$this->photo];
}
```

첨부 데이터가 Amazon S3 같은 원격 저장소에 저장될 때도 있습니다. Laravel은 애플리케이션의 [파일시스템 디스크](/docs/9.x/filesystem)에서 저장된 데이터를 바탕으로 첨부 인스턴스를 생성하는 것을 지원합니다:

```php
// 기본 디스크에 있는 파일로부터 첨부 생성...
return Attachment::fromStorage($this->path);

// 특정 디스크에 있는 파일로부터 첨부 생성...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한 메모리 내의 데이터를 바탕으로 첨부 인스턴스를 만들 수도 있습니다. 이때 `fromData` 메서드에 클로저를 넘기고, 클로저는 첨부를 나타내는 원시 데이터를 반환해야 합니다:

```
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일 이름과 MIME 타입을 수정하고 싶으면 `as` 및 `withMime` 메서드를 사용할 수 있습니다:

```
return Attachment::fromPath('/path/to/file')
        ->as('Photo Name')
        ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

가끔은 발송 메시지에 추가 헤더를 붙여야 할 때가 있습니다. 예를 들어, 커스텀 `Message-Id`나 임의 텍스트 헤더를 붙이는 경우입니다.

이를 위해 메일러블에 `headers` 메서드를 정의하세요. `headers` 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하고, 이 클래스는 `messageId`, `references`, `text` 파라미터를 받습니다. 필요한 파라미터만 지정하면 됩니다:

```
use Illuminate\Mail\Mailables\Headers;

/**
 * 메시지 헤더를 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Headers
 */
public function headers()
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

Mailgun, Postmark 같은 일부 서드파티 이메일 공급자는 메시지에 "태그"와 "메타데이터"를 지원합니다. 이를 통해 애플리케이션에서 보낸 이메일을 그룹화하거나 추적할 수 있습니다. 태그와 메타데이터는 `Envelope` 정의에서 다음과 같이 추가할 수 있습니다:

```
use Illuminate\Mail\Mailables\Envelope;

/**
 * 메시지 envelope을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope()
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

Mailgun을 사용하는 경우, [메일건 태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1)와 [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) 문서를 참고하세요. Postmark의 경우 [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)를 참고할 수 있습니다.

Amazon SES로 이메일을 보낼 경우, 메시지에 [SES 태그](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙일 때 `metadata` 메서드를 사용하세요.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel 메일 기능은 Symfony Mailer에 기반합니다. 메시지를 보내기 전에 Symfony 메시지 인스턴스를 받아 사용자 정의 콜백을 등록할 수도 있습니다. 이를 이용해 메시지를 세밀하게 커스터마이징할 수 있습니다. `Envelope` 정의에 `using` 옵션을 추가해 콜백을 등록하세요:

```
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * 메시지 envelope을 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope()
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
## 마크다운 메일러블

마크다운 기반 메일러블 메시지를 사용하면 [메일 알림](/docs/9.x/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있습니다. 메시지는 마크다운으로 작성되어, Laravel이 아름답고 반응형 HTML 템플릿과 함께 자동으로 일반 텍스트 버전도 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

`make:mail` Artisan 명령의 `--markdown` 옵션을 사용해서 마크다운 템플릿과 연동된 메일러블을 생성할 수 있습니다:

```shell
php artisan make:mail OrderShipped --markdown=emails.orders.shipped
```

그런 다음, 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 매개변수를 사용해 `Content` 정의를 구성하세요:

```
use Illuminate\Mail\Mailables\Content;

/**
 * 메시지 콘텐츠 정의를 가져옵니다.
 *
 * @return \Illuminate\Mail\Mailables\Content
 */
public function content()
{
    return new Content(
        markdown: 'emails.orders.shipped',
        with: [
            'url' => $this->orderUrl,
        ],
    );
}
```

<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성하기

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법 조합으로 메일 메시지를 쉽게 구성할 수 있도록 하며, Laravel의 미리 만들어진 이메일 UI 컴포넌트를 활용합니다:

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
> 마크다운 이메일 작성 시 과도한 들여쓰기를 피하세요. 마크다운 표준에 따르면, 들여쓰기가 된 콘텐츠는 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 인자를 받으며, 지원하는 색상은 `primary`, `success`, `error`입니다. 메시지에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 약간 다른 배경색을 가진 패널 내에 텍스트 블록을 렌더링해 사용자 주목을 끌게 합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

마크다운 테이블을 HTML 테이블로 변환합니다. 테이블의 컬럼 정렬은 기본 마크다운 테이블 문법을 지원합니다:

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

모든 마크다운 메일 컴포넌트를 애플리케이션 내로 내보내서 커스터마이징할 수 있습니다. `vendor:publish` Artisan 명령어로 `laravel-mail` 태그를 게시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어는 마크다운 메일 컴포넌트를 `resources/views/vendor/mail` 디렉토리에 게시합니다. 이 안에는 `html`과 `text` 디렉토리가 포함되며 각 컴포넌트의 HTML, 텍스트 버전이 들어있습니다. 원하는 대로 수정하실 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 내보내면 `resources/views/vendor/mail/html/themes` 디렉토리에 `default.css` 파일이 포함됩니다. 이 CSS를 수정하면, HTML 마크다운 메일 메시지 내에 자동으로 인라인 CSS 스타일로 변환되어 적용됩니다.

완전히 새 테마를 만들고 싶으면, `html/themes` 디렉토리에 CSS 파일을 넣고 이름을 지정한 뒤, `config/mail.php` 설정의 `theme` 옵션을 해당 테마 이름으로 바꾸세요.

개별 메일러블 클래스에서 테마를 지정하려면, 메일러블 클래스의 `$theme` 속성에 원하는 테마 이름을 할당하면 됩니다.

<a name="sending-mail"></a>
## 메일 보내기

이메일을 보내려면 `Mail` [파사드](/docs/9.x/facades)의 `to` 메서드를 사용하세요. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체나 컬렉션을 전달하면, 메일러는 자동으로 각 객체의 `email`과 `name` 속성을 찾아 이메일 수신자로 설정합니다. 수신자 지정 후엔, 메일러블 클래스 인스턴스를 `send` 메서드에 전달해 보냅니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Mail\OrderShipped;
use App\Models\Order;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;

class OrderShipmentController extends Controller
{
    /**
     * 주문 발송 처리.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 발송 처리...

        Mail::to($request->user())->send(new OrderShipped($order));
    }
}
```

"to" 수신자만 설정하는 것이 아니라, "cc" 및 "bcc" 수신자도 메서드 체인으로 설정할 수 있습니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

수신자 목록을 배열로 돌면서 메일을 보내야 할 때가 있습니다. 그런데 `to` 메서드는 메일러블의 수신자 목록에 주소를 계속 추가하므로, 매 반복시마다 모든 이전 수신자에게도 메일이 중복 발송됩니다. 따라서 수신자마다 새로운 메일러블 인스턴스를 생성해야 합니다:

```
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 통한 메일 전송

기본적으로 Laravel은 `config/mail.php`에서 `default`로 설정된 메일러를 사용해 이메일을 보냅니다. 그러나 `mailer` 메서드를 사용해 특정 메일러 구성을 지정할 수 있습니다:

```
Mail::mailer('postmark')
        ->to($request->user())
        ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 처리

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

메일 발송은 앱 응답 시간을 지연시킬 수 있기 때문에, 많은 개발자가 메일을 백그라운드 큐로 보내는 것을 선호합니다. Laravel은 내장된 [통합 큐 API](/docs/9.x/queues)를 통해 이를 쉽게 지원합니다. 메일 메시지를 큐에 넣으려면, 수신자를 지정한 후 `Mail` 파사드의 `queue` 메서드를 사용하세요:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 메시지를 백그라운드에서 보내도록 작업(job)을 큐에 넣는 일을 자동으로 처리합니다. 이 기능을 사용하려면 큐를 [설정](/docs/9.x/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메시지 큐잉

큐에 넣은 메일 전송을 지연시키고 싶다면 `later` 메서드를 사용하세요. 첫 번째 인수로는 메시지를 보낼 시점을 나타내는 `DateTime` 인스턴스를 전달합니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 푸시하기

`make:mail`로 생성된 모든 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, 아무 메일러블 인스턴스에서나 `onQueue`와 `onConnection` 메서드를 호출해 큐 이름과 연결(커넥션)을 지정할 수 있습니다:

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
#### 기본으로 큐잉하기

항상 메일을 큐에 넣고 싶다면, 메일러블 클래스에서 `ShouldQueue` 인터페이스를 구현하세요. 그러면 `send` 메서드를 호출해도 자동으로 큐잉되어 백그라운드 작업으로 처리됩니다:

```
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    //
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐 작업이 데이터베이스 트랜잭션 커밋 전에 처리될 수 있습니다. 이럴 경우, 트랜잭션 내에서 수행한 모델이나 DB 레코드 변경 사항이 아직 DB에 반영되지 않아 메일 보내기 작업에서 예기치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`인 경우, 특정 큐잉 메일러블을 모든 열린 DB 트랜잭션이 커밋된 후에 디스패치하도록 하려면, 메일 전송 시 `afterCommit` 메서드를 호출하세요:

```
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자의 `afterCommit` 호출로도 설정할 수 있습니다:

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
     * 새로운 메시지 인스턴스 생성.
     *
     * @return void
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 큐 작업과 데이터베이스 트랜잭션 관련 자세한 내용은 [큐 작업과 DB 트랜잭션 문서](/docs/9.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링

메일을 보내지 않고도 메일러블의 HTML 내용을 캡처하고 싶을 때가 있습니다. 이럴 때는 메일러블의 `render` 메서드를 호출하세요. 이 메서드는 메일러블을 평가한 HTML 콘텐츠를 문자열 형태로 반환합니다:

```
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿 디자인 시, 일반 Blade 템플릿처럼 곧바로 브라우저에서 렌더링을 보고 싶을 때가 있습니다. Laravel은 라우트 클로저나 컨트롤러에서 메일러블을 직접 반환하면 브라우저에서 렌더링하여 보여줍니다. 메일을 실제로 보내지 않고도 디자인을 빠르게 확인할 수 있습니다:

```
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

> [!WARNING]
> [인라인 첨부파일](#inline-attachments)은 브라우저 미리보기 시 렌더링되지 않습니다. 이 경우, [Mailpit](https://github.com/axllent/mailpit)나 [HELO](https://usehelo.com) 같은 이메일 테스트 앱으로 실제 메일을 보내 미리보기를 해야 합니다.

<a name="localizing-mailables"></a>
## 메일러블 현지화

Laravel은 요청의 현재 로케일이 아닌 다른 로케일로 메일을 보낼 수 있으며, 큐잉된 메일에서도 이 로케일을 기억합니다.

이를 위해 `Mail` 파사드는 `locale` 메서드를 제공해 원하는 언어를 설정합니다. 메일러블 템플릿 평가 시 애플리케이션 로케일이 지정된 로케일로 전환되고, 완료 시 이전 로케일로 되돌아갑니다:

```
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자의 선호 로케일

종종 애플리케이션 내 사용자의 선호 로케일을 저장하는 경우가 있습니다. 모델에 `HasLocalePreference` 인터페이스를 구현하면, Laravel은 메일과 알림 전송 시 이 저장된 로케일을 자동 사용합니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일을 가져옵니다.
     *
     * @return string
     */
    public function preferredLocale()
    {
        return $this->locale;
    }
}
```

인터페이스를 구현하면 자동으로 선호 로케일이 사용되므로, `locale` 메서드를 명시적으로 호출하지 않아도 됩니다:

```
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 메일러블 테스트하기

Laravel은 메일러블의 구조를 검사할 수 있는 다양한 메서드를 제공합니다. 또한 예상한 내용을 메일러블에 포함했는지 확인할 수 있는 편리한 메서드도 있습니다. 대표적인 메서드들은 다음과 같습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk`.

"HTML"계열 메서드는 메일러블의 HTML 버전에 특정 문자열이 포함됐는지, "텍스트" 계열은 일반 텍스트 버전에 특정 문자열이 포함됐는지를 확인합니다:

```
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content()
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
#### 메일러블 전송 테스트

메일러블의 콘텐츠 테스트는 별도로 진행하고, 특정 사용자에게 메일러블이 "전송"됐는지 테스트하는 것은 [Mail 가짜 기능](/docs/9.x/mocking#mail-fake)을 참고하세요.

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발

메일을 보내는 애플리케이션 개발 시, 실제로 라이브 이메일 주소로 메일을 보내고 싶지 않을 때가 많습니다. Laravel은 로컬 개발 중에 메일 전송을 "비활성화"하는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

메일 대신, `log` 메일 드라이버는 모든 이메일 메시지를 로그 파일에 기록해 검사할 수 있게 합니다. 보통은 로컬 개발 환경에서만 사용합니다. 환경별 설정 방법은 [설정 문서](/docs/9.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스를 통해, `smtp` 드라이버를 사용해 "가짜" 메일함으로 메일을 보낼 수 있습니다. 이 방식으로 Mailtrap의 메시지 뷰어에서 최종 메일을 실제 메일 클라이언트처럼 확인할 수 있습니다.

만약 [Laravel Sail](/docs/9.x/sail)을 사용한다면, [Mailpit](https://github.com/axllent/mailpit)를 통해 메일을 미리볼 수 있습니다. Sail이 실행 중이면 `http://localhost:8025`에서 Mailpit 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용하기

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 호출하여 전역 "to" 주소를 지정할 수 있습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```

<a name="events"></a>
## 이벤트

Laravel은 메일 발송 과정에서 두 가지 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지 전송 전에, `MessageSent` 이벤트는 전송 후에 발생합니다. 이 이벤트들은 메일이 *실제 전송*될 때 발생하며, 큐잉 시엔 발생하지 않습니다. 이벤트 리스너는 `App\Providers\EventServiceProvider`에 등록할 수 있습니다:

```
use App\Listeners\LogSendingMessage;
use App\Listeners\LogSentMessage;
use Illuminate\Mail\Events\MessageSending;
use Illuminate\Mail\Events\MessageSent;

/**
 * 애플리케이션의 이벤트-리스너 매핑.
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
## 커스텀 전송자 (Custom Transports)

Laravel은 여러 메일 전송자를 기본 제공하지만, 지원하지 않는 서비스를 위한 자체 전송자를 작성할 수도 있습니다. 시작하려면 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하는 클래스를 만드세요. 그리고 필수 메서드인 `doSend`와 `__toString()`을 구현합니다:

```
use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Mailchimp API 클라이언트.
     *
     * @var \MailchimpTransactional\ApiClient
     */
    protected $client;

    /**
     * 새 Mailchimp 전송자 인스턴스 생성.
     *
     * @param  \MailchimpTransactional\ApiClient  $client
     * @return void
     */
    public function __construct(ApiClient $client)
    {
        parent::__construct();
        
        $this->client = $client;
    }

    /**
     * {@inheritDoc}
     */
    protected function doSend(SentMessage $message): void
    {
        $email = MessageConverter::toEmail($message->getOriginalMessage());

        $this->client->messages->send(['message' => [
            'from_email' => $email->getFrom(),
            'to' => collect($email->getTo())->map(function ($email) {
                return ['email' => $email->getAddress(), 'type' => 'to'];
            })->all(),
            'subject' => $email->getSubject(),
            'text' => $email->getTextBody(),
        ]]);
    }

    /**
     * 전송자의 문자열 표현 반환.
     *
     * @return string
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

전송자를 정의했으면, `Mail` 파사드의 `extend` 메서드로 등록할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider` 서비스 프로바이더 `boot` 메서드에서 등록합니다. `extend`에 넘기는 클로저는 `config/mail.php` 설정 배열을 인수로 받습니다:

```
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Mail::extend('mailchimp', function (array $config = []) {
        return new MailchimpTransport(/* ... */);
    });
}
```

등록 후에는 `config/mail.php` 설정 파일에 다음과 같이 새 전송자를 사용하는 메일러를 정의할 수 있습니다:

```
'mailchimp' => [
    'transport' => 'mailchimp',
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송자

Laravel은 Mailgun, Postmark 같은 Symfony 유지 관리 전송자를 기본 지원합니다. 여기에 더해 다른 Symfony 전송자를 설치하고 확장할 수도 있습니다. 예를 들어, "Sendinblue" Symfony 메일러를 설치하고 등록하는 방법은 다음과 같습니다:

```none
composer require symfony/sendinblue-mailer symfony/http-client
```

Sendinblue 메일러가 설치되면, 애플리케이션의 `services` 설정 파일에 Sendinblue API 키를 추가하세요:

```
'sendinblue' => [
    'key' => 'your-api-key',
],
```

그 다음, 서비스 프로바이더 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드를 사용해 전송자를 등록합니다:

```
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Sendinblue\Transport\SendinblueTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Mail::extend('sendinblue', function () {
        return (new SendinblueTransportFactory)->create(
            new Dsn(
                'sendinblue+api',
                'default',
                config('services.sendinblue.key')
            )
        );
    });
}
```

등록이 완료되면 `config/mail.php` 설정 파일에 다음처럼 Sendinblue 전송자를 사용하는 메일러를 정의하세요:

```
'sendinblue' => [
    'transport' => 'sendinblue',
    // ...
],
```