# 메일

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈 설정](#round-robin-configuration)
- [Mailable 클래스 생성](#generating-mailables)
- [Mailable 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 Mailable](#markdown-mailables)
    - [마크다운 Mailable 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [Mailable 렌더링](#rendering-mailables)
    - [브라우저에서 Mailable 미리보기](#previewing-mailables-in-the-browser)
- [Mailable 로컬라이징](#localizing-mailables)
- [테스트](#testing-mailables)
    - [Mailable 콘텐츠 테스트](#testing-mailable-content)
    - [Mailable 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기있는 [Symfony Mailer](https://symfony.com/doc/7.0/mailer.html) 컴포넌트를 기반으로 한 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail`을 통한 메일 발송 드라이버를 제공하므로, 로컬 또는 클라우드 기반 서비스로 메일을 손쉽게 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 구성된 각 메일러마다 고유한 설정과 "transport(전송 방식)"를 지정할 수 있어, 애플리케이션이 다양한 이메일 서비스를 통해 서로 다른 이메일을 발송할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark로, 대량 메일은 Amazon SES로 발송하도록 설정할 수 있습니다.

`mail` 설정 파일 내의 `mailers` 배열에는 Laravel이 지원하는 주요 메일 드라이버/전송 방식의 샘플 설정이 들어있으며, `default` 설정 값은 애플리케이션에서 메일 발송 시 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/전송 방식 사전 준비 사항

Mailgun, Postmark, Resend, MailerSend와 같은 API 기반 드라이버는 SMTP 서버로 메일을 보내는 것보다 더 간단하고 빠른 경우가 많습니다. 가능한 경우, 이들 중 하나의 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer를 통해 Symfony의 Mailgun Mailer 전송 모듈을 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에 두 가지를 수정해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 설정합니다:

    'default' => env('MAIL_MAILER', 'mailgun'),

그리고, 다음 설정을 `mailers` 배열에 추가합니다:

    'mailgun' => [
        'transport' => 'mailgun',
        // 'client' => [
        //     'timeout' => 5,
        // ],
    ],

기본 메일러를 설정한 후에는 `config/services.php` 파일에 다음 옵션을 추가하세요:

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
        'scheme' => 'https',
    ],

미국 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)이 아닌 지역을 사용한다면, region에 따라 endpoint를 다음과 같이 설정할 수 있습니다:

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
        'scheme' => 'https',
    ],

<a name="postmark-driver"></a>
#### Postmark 드라이버

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer로 Symfony의 Postmark 전송 모듈을 설치해야 합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, `config/mail.php`의 `default` 옵션을 `postmark`로 설정하세요. 설정이 완료되면 `config/services.php` 파일에 다음 옵션이 포함되어 있는지 확인하세요:

    'postmark' => [
        'token' => env('POSTMARK_TOKEN'),
    ],

메일러별로 Postmark 메시지 스트림을 지정하려면, 메일러 설정 배열에 `message_stream_id` 항목을 추가할 수 있습니다:

    'postmark' => [
        'transport' => 'postmark',
        'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
        // 'client' => [
        //     'timeout' => 5,
        // ],
    ],

이로 인해 서로 다른 메시지 스트림을 사용하는 다중 Postmark 메일러의 설정이 가능합니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer로 Resend PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```

그 다음, `config/mail.php`에서 `default` 옵션을 `resend`로, 그리고 `config/services.php`에 다음을 추가하세요:

    'resend' => [
        'key' => env('RESEND_KEY'),
    ],

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면, 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer로 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그런 다음, `config/mail.php`에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 다음 옵션이 있는지 확인하세요:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'token' => env('AWS_SESSION_TOKEN'),
    ],

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)을 활용하려면, 메일 메시지의 [`headers`](#headers) 메서드가 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 추가할 수 있습니다:

```php
/**
 * 메시지 헤더 반환
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

`SendEmail` 메서드에 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 전달하려면, `ses` 설정에 `options` 배열을 정의하세요:

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

<a name="mailersend-driver"></a>
#### MailerSend 드라이버

[MailerSend](https://www.mailersend.com/)는 API 기반 메일 드라이버 패키지를 제공하며, Composer로 설치할 수 있습니다:

```shell
composer require mailersend/laravel-driver
```

설치 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하고, `MAIL_MAILER`도 `mailersend`로 설정하세요:

```ini
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

마지막으로, `config/mail.php`의 `mailers` 배열에 MailerSend를 추가하세요:

```php
'mailersend' => [
    'transport' => 'mailersend',
],
```

MailerSend와 운용 템플릿 사용법 등 자세한 내용은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정

애플리케이션의 메일 발송에 사용되는 외부 서비스가 다운될 때를 대비해 백업 메일 전송 설정을 지정하는 것이 유용할 수 있습니다.

이를 위해, `mail` 설정 파일에서 `failover` 전송 방식을 사용하는 mailer를 정의하세요. 그리고 `mailers` 배열에 사용할 드라이버의 선택 순서를 나열하세요:

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

장애 조치 mailer를 설정했으면 기본 mailer로 지정하세요:

    'default' => env('MAIL_MAILER', 'failover'),

<a name="round-robin-configuration"></a>
### 라운드 로빈 설정

`roundrobin` 전송 방식을 사용하면 여러 mailer에 걸쳐 메일 발송 부하를 분산시킬 수 있습니다. 이를 위해 'roundrobin' transport를 사용하여 mailer를 정의하고 사용할 mailer를 나열하세요:

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

라운드 로빈 mailer를 기본 mailer로 지정하세요:

    'default' => env('MAIL_MAILER', 'roundrobin'),

라운드 로빈 전송 방식은 설정된 메일러 중 랜덤하게 선택한 후, 다음 이메일을 보낼 때는 순서대로 다음 메일러로 넘깁니다. 이는 장애 조치 전송 방식(`failover`)이 *[고가용성](https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1)*을 목표로 하는 것과 달리, *[로드 밸런싱](https://ko.wikipedia.org/wiki/%EB%A1%9C%EB%93%9C_%EB%B2%A8%EB%9F%B0%EC%8B%B1)*을 제공합니다.

<a name="generating-mailables"></a>
## Mailable 클래스 생성

Laravel에서 각 이메일 유형은 "Mailable" 클래스로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 해당 디렉터리가 없더라도 Artisan의 `make:mail` 명령으로 첫 mailable 클래스를 생성하면 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 작성

Mailable 클래스를 생성했다면, 클래스 파일을 열어 구성을 확인해 봅시다. Mailable 클래스는 주로 `envelope`, `content`, 그리고 `attachments` 메서드를 통해 설정합니다.

`envelope` 메서드는 메시지의 제목과 수신자(필요하다면)를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 콘텐츠 생성을 위한 [Blade 템플릿](/docs/{{version}}/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope 사용

이메일의 발신자를 설정해봅시다. 이메일의 "from" 정보는 두 가지 방법 중 하나로 설정할 수 있습니다. 첫째, 메시지의 envelope에 직접 지정할 수 있습니다:

    use Illuminate\Mail\Mailables\Address;
    use Illuminate\Mail\Mailables\Envelope;

    /**
     * 메시지 엔벨로프 가져오기
     */
    public function envelope(): Envelope
    {
        return new Envelope(
            from: new Address('jeffrey@example.com', 'Jeffrey Way'),
            subject: 'Order Shipped',
        );
    }

`replyTo` 주소도 아래와 같이 지정할 수 있습니다:

    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        replyTo: [
            new Address('taylor@example.com', 'Taylor Otwell'),
        ],
        subject: 'Order Shipped',
    );

<a name="using-a-global-from-address"></a>
#### 전역 `from` 주소 사용

애플리케이션 전체에서 동일한 "from" 주소를 사용한다면, 매번 지정하지 않고 `config/mail.php` 설정 파일에서 전역 "from" 주소를 지정할 수 있습니다:

    'from' => [
        'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
        'name' => env('MAIL_FROM_NAME', 'Example'),
    ],

전역 "reply_to" 주소도 지정할 수 있습니다:

    'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],

<a name="configuring-the-view"></a>
### 뷰 설정

mailable 클래스의 `content` 메서드에서 이메일 내용을 렌더링할 템플릿(`view`)을 정의할 수 있습니다. 보통 [Blade 템플릿](/docs/{{version}}/blade)을 사용하므로 매우 편리합니다:

    /**
     * 메시지 콘텐츠 정의 가져오기
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }

> [!NOTE]  
> 모든 이메일 템플릿을 보관할 `resources/views/emails` 디렉터리를 만들어 사용하는 것을 권장합니다.

<a name="plain-text-emails"></a>
#### 평문(Plain Text) 이메일

이메일의 평문 버전을 별도로 만들고 싶다면 `Content` 정의 시 `text` 파라미터에 지정하면 됩니다. HTML 버전과 평문 버전을 모두 정의할 수 있습니다:

    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
            text: 'mail.orders.shipped-text'
        );
    }

명확성을 위해 `html` 파라미터도 사용할 수 있습니다:

    return new Content(
        html: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### 공용(public) 프로퍼티 활용

뷰에서 사용하고자 하는 데이터를 전달하는 대표적인 방법은 mailable 클래스의 공용(public) 프로퍼티로 설정하는 것입니다. 생성자에서 데이터를 받아 공용 프로퍼티에 할당하면, 해당 데이터는 뷰에서 바로 사용할 수 있습니다:

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

        public function __construct(
            public Order $order,
        ) {}

        public function content(): Content
        {
            return new Content(
                view: 'mail.orders.shipped',
            );
        }
    }

뷰에서는 Blade 문법을 사용해 데이터를 참조합니다:

    <div>
        Price: {{ $order->price }}
    </div>

<a name="via-the-with-parameter"></a>
#### `with` 파라미터 활용

보내기 전 데이터 포맷을 커스터마이즈하고 싶다면 `Content`의 `with` 파라미터를 사용할 수 있습니다. 이 경우, 생성자에서 받은 데이터를 protected/protected 또는 private로 정의하여 직접 템플릿에 노출되지 않도록 합니다:

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

        public function __construct(
            protected Order $order,
        ) {}

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

이렇게 전달된 데이터는 뷰에서 바로 사용할 수 있습니다:

    <div>
        Price: {{ $orderPrice }}
    </div>

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면, `attachments` 메서드에서 첨부파일을 반환합니다. 파일 경로를 `Attachment` 클래스의 `fromPath` 메서드에 전달하면 됩니다:

    use Illuminate\Mail\Mailables\Attachment;

    public function attachments(): array
    {
        return [
            Attachment::fromPath('/path/to/file'),
        ];
    }

첨부파일 표시 이름 또는 MIME 타입을 지정하려면 `as`와 `withMime` 메서드를 사용하세요:

    public function attachments(): array
    {
        return [
            Attachment::fromPath('/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf'),
        ];
    }

<a name="attaching-files-from-disk"></a>
#### 디스크에서 파일 첨부

[파일 시스템 디스크](/docs/{{version}}/filesystem)에 저장된 파일도 `fromStorage`를 사용해 첨부할 수 있습니다:

    public function attachments(): array
    {
        return [
            Attachment::fromStorage('/path/to/file'),
        ];
    }

첨부파일 이름과 MIME 타입 지정 역시 가능합니다:

    public function attachments(): array
    {
        return [
            Attachment::fromStorage('/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf'),
        ];
    }

기본 디스크가 아닌 다른 디스크를 사용하려면 `fromStorageDisk`를 사용하세요:

    public function attachments(): array
    {
        return [
            Attachment::fromStorageDisk('s3', '/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf'),
        ];
    }

<a name="raw-data-attachments"></a>
#### Raw 데이터 첨부

`fromData` 메서드를 사용하면, 메모리상에 있는 raw 바이트 문자열을 첨부 파일로 보낼 수 있습니다(예: 메모리에서 생성한 PDF):

    public function attachments(): array
    {
        return [
            Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
                ->withMime('application/pdf'),
        ];
    }

<a name="inline-attachments"></a>
### 인라인 첨부파일

이메일에 인라인 이미지를 삽입할 때는 보통 번거롭지만, Laravel에서는 매우 간단합니다. 이메일 템플릿에서 `$message->embed($pathToImage)` 메서드를 사용하세요. `$message` 변수는 모든 이메일 템플릿에 자동으로 전달됩니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]  
> `$message` 변수는 평문 메일 템플릿에서는 사용할 수 없습니다(인라인 첨부파일 미지원).

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 이미지를 임베드

Raw 이미지 데이터를 템플릿에 임베드하려면 `$message->embedData($data, 'example-image.jpg')`를 사용하세요:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

파일 경로를 직접 지정하지 않고, 파일을 나타내는 모델 같은 객체(예: Photo)를 첨부 객체로 만들 수 있습니다. 해당 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Mail\Attachable;
    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Mail\Attachment;

    class Photo extends Model implements Attachable
    {
        public function toMailAttachment(): Attachment
        {
            return Attachment::fromPath('/path/to/file');
        }
    }

이렇게 하면, `attachments` 메서드에서 해당 객체를 반환할 수 있습니다:

    public function attachments(): array
    {
        return [$this->photo];
    }

원격 파일 저장소(예: S3)나 메모리 데이터 등에서도 Attachments를 만들 수 있습니다:

    // 디폴트 디스크에서 파일 첨부
    return Attachment::fromStorage($this->path);

    // 특정 디스크에서 파일 첨부
    return Attachment::fromStorageDisk('backblaze', $this->path);

    // 메모리 데이터로 첨부파일 생성
    return Attachment::fromData(fn () => $this->content, 'Photo Name');

이름과 MIME 타입도 커스터마이즈 할 수 있습니다:

    return Attachment::fromPath('/path/to/file')
        ->as('Photo Name')
        ->withMime('image/jpeg');

<a name="headers"></a>
### 헤더

추가 헤더가 필요할 때는 mailable에 `headers` 메서드를 정의해 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하세요:

    use Illuminate\Mail\Mailables\Headers;

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

<a name="tags-and-metadata"></a>
### 태그와 메타데이터

Mailgun, Postmark와 같은 일부 이메일 공급자는 메시지 "태그"와 "메타데이터"를 지원하여 이메일 추적 및 그룹화가 가능합니다. 이런 값들은 `Envelope` 정의에서 추가할 수 있습니다:

    use Illuminate\Mail\Mailables\Envelope;

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

더 자세한 정보는 Mailgun의 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tagging), [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#attaching-data-to-messages), Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서를 참조하세요.

Amazon SES 사용 시, `metadata` 메서드를 통해 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer가 기반이므로, 메시지 전송 전 Symfony Message 인스턴스를 커스터마이즈할 수 있습니다. `Envelope` 정의의 `using` 파라미터에 콜백을 등록하세요:

    use Illuminate\Mail\Mailables\Envelope;
    use Symfony\Component\Mime\Email;

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

<a name="markdown-mailables"></a>
## 마크다운 Mailable

마크다운 mailable 메시지는 [메일 알림](/docs/{{version}}/notifications#mail-notifications)의 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있으며, 마크다운 문법을 사용하므로 아름답고 반응형인 HTML과 평문 버전을 자동으로 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 Mailable 생성

마크다운 템플릿이 포함된 mailable을 생성하려면 `make:mail` Artisan 명령의 `--markdown` 옵션을 사용하세요:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

`content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용하십시오:

    use Illuminate\Mail\Mailables\Content;

    public function content(): Content
    {
        return new Content(
            markdown: 'mail.orders.shipped',
            with: [
                'url' => $this->orderUrl,
            ],
        );
    }

<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성

마크다운 mailable은 Blade 컴포넌트와 마크다운 문법을 결합해 사용하므로, 미려한 이메일 UI 컴포넌트를 쉽게 사용할 수 있습니다:

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
> 마크다운 이메일 작성 시 불필요한 들여쓰기는 피하세요. 마크다운 파서는 들여쓰기된 내용을 코드블록으로 처리합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 지정이 가능하며, 여러 개의 버튼을 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 입력한 텍스트 블록을 배경색이 다른 패널로 렌더링하여, 주의를 끌고 싶을 때 유용합니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환해줍니다. 컬럼 정렬도 지원합니다:

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

마크다운 이메일 컴포넌트는 커스터마이징을 위해 `vendor:publish` Artisan 명령으로 내 앱에 복사할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

그러면 `resources/views/vendor/mail` 하위에 복사되며, 자유롭게 수정해 사용할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 export 후 `resources/views/vendor/mail/html/themes/default.css` 파일을 수정하면, 스타일이 인라인 CSS로 자동 반영됩니다.

새로운 마크다운 테마를 만들려면 CSS 파일을 `html/themes`에 추가하면 되며, `config/mail.php` 파일의 `theme` 옵션을 변경하세요. 개별 mailable에 테마를 지정하고자 할 때에는 클래스의 `$theme` 프로퍼티를 이용하세요.

<a name="sending-mail"></a>
## 메일 발송

메시지를 보내려면 `Mail` [파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용하세요. 이메일 주소, 유저 모델, 또는 모델 컬렉션 모두 지원합니다. 대상 지정 후 mailable 인스턴스를 `send`에 전달하면 됩니다:

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
        public function store(Request $request): RedirectResponse
        {
            $order = Order::findOrFail($request->order_id);

            // 주문 발송 처리...

            Mail::to($request->user())->send(new OrderShipped($order));

            return redirect('/orders');
        }
    }

`to` 뿐만 아니라, `cc`, `bcc`를 체이닝하여 여러 수신자를 추가할 수 있습니다:

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->send(new OrderShipped($order));

<a name="looping-over-recipients"></a>
#### 여러 수신자 반복 발송

여러 명에게 하나씩 개별 이메일을 보내려면, 루프마다 새 mailable 인스턴스를 만들어야 합니다:

    foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
        Mail::to($recipient)->send(new OrderShipped($order));
    }

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 발송

기본 메일러 외에 다른 메일러 설정으로 보낼 때는 `mailer` 메서드를 사용하세요:

    Mail::mailer('postmark')
        ->to($request->user())
        ->send(new OrderShipped($order));

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

응답 시간을 개선하려면 메일 발송을 백그라운드로 큐에 등록하는 것이 효율적입니다. `queue` 메서드를 사용하세요:

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue(new OrderShipped($order));

이때 [큐 설정](/docs/{{version}}/queues)을 먼저 준비해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 발송(Delayed Queue)

큐에 등록된 메일 발송을 지연하려면 `later` 메서드를 사용하세요:

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->later(now()->addMinutes(10), new OrderShipped($order));

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 할당

모든 mailable은 기본적으로 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, `onQueue`와 `onConnection`으로 큐 이름과 커넥션을 지정할 수 있습니다:

    $message = (new OrderShipped($order))
        ->onConnection('sqs')
        ->onQueue('emails');

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue($message);

<a name="queueing-by-default"></a>
#### 기본적으로 큐 처리

항상 큐 처리하고자 하는 mailable 클래스는 `ShouldQueue` 인터페이스를 구현하세요:

    use Illuminate\Contracts\Queue\ShouldQueue;

    class OrderShipped extends Mailable implements ShouldQueue
    {
        // ...
    }

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 처리와 DB 트랜잭션

큐가 DB 트랜잭션 내에서 실행되면, 트랜잭션 커밋 전에 큐가 처리될 수 있으니 주의가 필요합니다. 이런 경우 `afterCommit` 메서드로 처리 시점을 제어하세요:

    Mail::to($request->user())->send(
        (new OrderShipped($order))->afterCommit()
    );

생성자 내부에서 호출해도 됩니다:

    class OrderShipped extends Mailable implements ShouldQueue
    {
        use Queueable, SerializesModels;

        public function __construct()
        {
            $this->afterCommit();
        }
    }

> [!NOTE]  
> 이슈를 우회하는 상세 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## Mailable 렌더링

실제로 발송하지 않고 mailable의 HTML 콘텐츠만 받고 싶을 때 `render` 메서드를 사용하세요:

    use App\Mail\InvoicePaid;
    use App\Models\Invoice;

    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))->render();

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 미리보기

메일 템플릿을 개발하는 동안, 경로(route)에서 mailable을 직접 반환하면 브라우저 상에서 곧바로 내용을 확인할 수 있습니다:

    Route::get('/mailable', function () {
        $invoice = App\Models\Invoice::find(1);

        return new App\Mail\InvoicePaid($invoice);
    });

<a name="localizing-mailables"></a>
## Mailable 로컬라이징

Laravel은 mailable을 현재 요청의 로케일이 아닌 다른 언어로 보낼 수 있으며, 큐에 등록됐을 때도 해당 언어를 기억합니다.

`Mail` 파사드의 `locale` 메서드로 언어를 지정하세요:

    Mail::to($request->user())->locale('es')->send(
        new OrderShipped($order)
    );

<a name="user-preferred-locales"></a>
### 사용자 선호 언어 자동 적용

모델에 `HasLocalePreference` 인터페이스를 구현하면, 해당 사용자의 로케일 정보를 자동으로 사용할 수 있습니다:

    use Illuminate\Contracts\Translation\HasLocalePreference;

    class User extends Model implements HasLocalePreference
    {
        public function preferredLocale(): string
        {
            return $this->locale;
        }
    }

이 인터페이스를 구현한 뒤엔 수동으로 `locale`을 호출할 필요 없이 자동으로 적용됩니다.

    Mail::to($request->user())->send(new OrderShipped($order));

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### Mailable 콘텐츠 테스트

Laravel은 mailable 구조 점검은 물론, 예상한 콘텐츠가 포함되어 있는지도 다양한 어서션 메서드로 테스트할 수 있습니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등.

HTML/텍스트 각각의 버전에 대해 어서션이 이뤄집니다:

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
### Mailable 발송 테스트

메일의 콘텐츠와, 실제로 특정 유저에게 해당 메일이 **발송**됐는지를 별개로 테스트하는 것이 좋습니다. `Mail` 파사드의 `fake` 메서드로 실제 발송을 차단하고, 다양한 어서션을 사용할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // 주문 발송 수행...

    // 어떤 메일도 발송되지 않았는지 확인
    Mail::assertNothingSent();

    // 특정 mailable이 발송됐는지 확인
    Mail::assertSent(OrderShipped::class);

    // 두 번 발송됐는지 확인
    Mail::assertSent(OrderShipped::class, 2);

    // 특정 이메일 주소로 발송됐는지 확인
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // 복수 이메일 주소로 발송됐는지 확인
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // 발송되지 않았는지 확인
    Mail::assertNotSent(AnotherMailable::class);

    // 총 3개가 발송됐는지 확인
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

        // 주문 발송 수행...

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

백그라운드 큐로 보낼 땐 `assertQueued`를 사용하세요:

    Mail::assertQueued(OrderShipped::class);
    Mail::assertNotQueued(OrderShipped::class);
    Mail::assertNothingQueued();
    Mail::assertQueuedCount(3);

클로저를 전달하여, 특정 조건을 만족하는 경우만 검사할 수 있습니다:

    Mail::assertSent(function (OrderShipped $mail) use ($order) {
        return $mail->order->id === $order->id;
    });

mailable 인스턴스는 다양한 헬퍼 메서드로 수신자, 참조자, 제목, 첨부파일까지 점검할 수 있습니다:

    Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
        return $mail->hasTo($user->email) &&
               $mail->hasCc('...') &&
               $mail->hasBcc('...') &&
               $mail->hasReplyTo('...') &&
               $mail->hasFrom('...') &&
               $mail->hasSubject('...');
    });

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

메일이 **전혀** 발송/큐잉되지 않았는지 확인하려면 `assertNothingOutgoing`와 `assertNotOutgoing`을 사용하세요:

    Mail::assertNothingOutgoing();

    Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
        return $mail->order->id === $order->id;
    });

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발

개발 단계에선 실제 이메일이 전송되지 않게 하길 원할 수 있습니다. Laravel은 다양한 방식으로 실제 발송을 비활성화할 수 있습니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 메일 내용을 로그 파일에 기록합니다. 주로 개발환경에서 사용하며, 환경별 설정은 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

[HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io)과 같은 서비스를 smtp 드라이버와 함께 사용해, "가상" 메일함에서 실제 메일을 확인할 수도 있습니다.

[Laravel Sail](/docs/{{version}}/sail) 사용 시 [Mailpit](https://github.com/axllent/mailpit)으로도 미리보기가 가능합니다. Sail이 동작 중이라면 `http://localhost:8025`에서 사용할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

모든 발송을 특정 주소로 강제하고 싶다면, `Mail` 파사드의 `alwaysTo` 메서드를 사용하세요(예: 서비스 프로바이더의 `boot` 메서드):

    use Illuminate\Support\Facades\Mail;

    public function boot(): void
    {
        if ($this->app->environment('local')) {
            Mail::alwaysTo('taylor@example.com');
        }
    }

<a name="events"></a>
## 이벤트

메일 발송 시 Laravel은 두 이벤트를 발생시킵니다. `MessageSending`(발송 전)과 `MessageSent`(발송 후)입니다. 이 이벤트는 *실제 발송* 시 발생하며, 큐잉 시가 아닙니다. [이벤트 리스너](/docs/{{version}}/events)에서 처리할 수 있습니다:

    use Illuminate\Mail\Events\MessageSending;
    // use Illuminate\Mail\Events\MessageSent;

    class LogMessage
    {
        public function handle(MessageSending $event): void
        {
            // ...
        }
    }

<a name="custom-transports"></a>
## 커스텀 전송 방식

지원하지 않는 외부 메일 서비스를 위해선 커스텀 transport 클래스를 작성할 수 있습니다. `Symfony\Component\Mailer\Transport\AbstractTransport`를 상속해 `doSend`와 `__toString()`을 구현하세요:

    use MailchimpTransactional\ApiClient;
    use Symfony\Component\Mailer\SentMessage;
    use Symfony\Component\Mailer\Transport\AbstractTransport;
    use Symfony\Component\Mime\Address;
    use Symfony\Component\Mime\MessageConverter;

    class MailchimpTransport extends AbstractTransport
    {
        public function __construct(
            protected ApiClient $client,
        ) {
            parent::__construct();
        }

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

        public function __toString(): string
        {
            return 'mailchimp';
        }
    }

커스텀 transport를 등록하려면 `Mail` 파사드의 `extend` 메서드를 사용하세요(예: 서비스 프로바이더의 `boot` 메서드):

    use App\Mail\MailchimpTransport;
    use Illuminate\Support\Facades\Mail;

    public function boot(): void
    {
        Mail::extend('mailchimp', function (array $config = []) {
            return new MailchimpTransport(/* ... */);
        });
    }

설정이 끝나면 `config/mail.php`에서 메일러 정의 시 새 transport를 사용하세요:

    'mailchimp' => [
        'transport' => 'mailchimp',
        // ...
    ],

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식

Laravel은 Mailgun, Postmark 등 몇 가지 Symfony Mailer의 전송 방식을 기본 지원하지만, 추가로 다른 Symfony Mailer를 설치해 사용할 수도 있습니다. 예시로 Brevo(구 Sendinblue)를 설치하실 수 있습니다:

```none
composer require symfony/brevo-mailer symfony/http-client
```

설치 후 `services` 설정에 API 키를 추가하세요:

    'brevo' => [
        'key' => 'your-api-key',
    ],

`Mail` 파사드의 `extend`로 등록합니다(서비스 프로바이더의 `boot` 메서드):

    use Illuminate\Support\Facades\Mail;
    use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
    use Symfony\Component\Mailer\Transport\Dsn;

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

이제 `config/mail.php`의 메일러 정의에서 새 전송 방식을 사용할 수 있습니다:

    'brevo' => [
        'transport' => 'brevo',
        // ...
    ],
