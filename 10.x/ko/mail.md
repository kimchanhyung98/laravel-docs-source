# 메일

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드로빈 설정](#round-robin-configuration)
- [Mailable 생성하기](#generating-mailables)
- [Mailable 작성하기](#writing-mailables)
    - [발신자 설정하기](#configuring-the-sender)
    - [뷰 설정하기](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더 설정](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운 Mailable](#markdown-mailables)
    - [마크다운 Mailable 생성하기](#generating-markdown-mailables)
    - [마크다운 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐에 등록하기](#queueing-mail)
- [Mailable 렌더링](#rendering-mailables)
    - [브라우저에서 Mailable 미리보기](#previewing-mailables-in-the-browser)
- [Mailable 현지화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [Mailable 내용 테스트](#testing-mailable-content)
    - [Mailable 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일을 보내는 일은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/6.2/mailer.html) 컴포넌트에 의해 구동되는 깔끔하고 단순한 이메일 API를 제공합니다. Laravel 및 Symfony Mailer는 SMTP, Mailgun, Postmark, Amazon SES, 그리고 `sendmail`을 통한 메일 송신 드라이버를 제공하여, 로컬 또는 클라우드 기반 서비스에서 신속하게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 파일에서 설정할 수 있습니다. 이 파일에 설정된 각 메일러는 고유한 설정, 그리고 고유한 "트랜스포트"를 가질 수 있어, 애플리케이션에서 특정 메일 메시지마다 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark를, 대량 메일은 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 내에는 `mailers` 설정 배열이 있습니다. 이 배열은 Laravel에서 지원하는 주요 메일 드라이버/트랜스포트에 대한 샘플 설정을 포함하고 있으며, `default` 설정 값은 애플리케이션이 이메일을 전송할 때 기본적으로 어떤 메일러를 사용할 것인지 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버/트랜스포트 사전 준비

Mailgun, Postmark, MailerSend와 같은 API 기반 드라이버는 SMTP 서버를 통해 메일을 전송하는 것보다 더 간단하고 빠른 경우가 많습니다. 가능한 경우 이러한 드라이버 중 하나를 사용하는 것이 좋습니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer를 통해 Symfony의 Mailgun Mailer 트랜스포트를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그다음, 애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `mailgun`으로 설정하세요. 이후, 기본 메일러를 설정한 후, `config/services.php`에 아래와 같이 옵션이 포함되어 있는지 확인하세요.

    'mailgun' => [
        'transport' => 'mailgun',
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
    ],

미국 외의 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용한다면, `services` 설정 파일에서 엔드포인트를 지정할 수 있습니다:

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    ],

<a name="postmark-driver"></a>
#### Postmark 드라이버

Postmark 드라이버를 사용하려면 Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치하세요.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그다음, `config/mail.php`의 `default` 옵션을 `postmark`로 설정하세요. 이후, `config/services.php`에 아래와 같이 옵션이 포함되어 있는지 확인하세요.

    'postmark' => [
        'token' => env('POSTMARK_TOKEN'),
    ],

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하고 싶다면, 메일러의 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 설정 배열은 `config/mail.php`에 있습니다.

    'postmark' => [
        'transport' => 'postmark',
        'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    ],

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 Composer로 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그다음, `config/mail.php`의 `default` 옵션을 `ses`로 설정하고, `config/services.php`에 아래 옵션이 포함되어 있는지 확인하세요.

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

AWS [임시 자격증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면, SES 설정에 `token` 키를 추가할 수 있습니다.

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'token' => env('AWS_SESSION_TOKEN'),
    ],

Laravel이 이메일을 전송할 때 AWS SDK의 `SendEmail` 메서드로 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하고 싶다면, `ses` 설정에 `options` 배열을 정의할 수 있습니다.

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

[MailerSend](https://www.mailersend.com/)는 트랜잭션 이메일 및 SMS 서비스로, Laravel용 자체 API 기반 메일 드라이버를 제공합니다. Composer를 통해 아래 패키지를 설치하세요.

```shell
composer require mailersend/laravel-driver
```

패키지를 설치한 후, `.env` 파일에 `MAILERSEND_API_KEY` 환경 변수를 추가하세요. 또한 `MAIL_MAILER` 환경 변수를 `mailersend`로 정의해야 합니다.

```shell
MAIL_MAILER=mailersend
MAIL_FROM_ADDRESS=app@yourdomain.com
MAIL_FROM_NAME="App Name"

MAILERSEND_API_KEY=your-api-key
```

MailerSend에 대한 더 자세한 사용 방법 및 호스팅된 템플릿 사용법은 [MailerSend 드라이버 문서](https://github.com/mailersend/mailersend-laravel-driver#usage)를 참고하세요.

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정

외부 이메일 서비스에 문제가 발생할 경우, 예비 메일 전송 구성을 정의해서 1차 메일러에 장애가 있을 때 자동으로 백업 메일러를 사용할 수 있습니다.

이를 위해 `mail` 설정 파일에서 `failover` 트랜스포트를 사용하는 메일러를 정의해야 합니다. 해당 메일러의 설정 배열에는 메일러명 배열을 포함시키며, 우선순위에 따라 메일러를 나열합니다.

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

장애 조치용 메일러를 정의한 후, `mail` 설정 파일의 `default` 값을 `failover`로 설정하세요.

    'default' => env('MAIL_MAILER', 'failover'),

<a name="round-robin-configuration"></a>
### 라운드로빈(Round Robin) 설정

`roundrobin` 트랜스포트는 메일 발송 작업을 여러 메일러 간에 분산시킵니다. `mail` 설정 파일에서 `roundrobin` 트랜스포트를 사용하는 메일러를 정의한 후, 어떤 메일러들을 분산 대상에 포함할지 배열에 나열합니다.

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

정의한 라운드로빈 메일러를 기본 메일러로 사용하려면 `default` 값에 해당 메일러명을 할당하세요.

    'default' => env('MAIL_MAILER', 'roundrobin'),

라운드로빈 트랜스포트는 설정된 메일러 목록에서 무작위로 하나를 선택하고, 이후 각 이메일마다 순차적으로 다음 메일러로 전환합니다. `failover` 트랜스포트가 *[고가용성](https://en.wikipedia.org/wiki/High_availability)*을 제공한다면, `roundrobin` 트랜스포트는 *[로드 밸런싱](https://en.wikipedia.org/wiki/Load_balancing_(computing))* 기능을 제공합니다.

<a name="generating-mailables"></a>
## Mailable 생성하기

Laravel 애플리케이션을 개발할 때, 애플리케이션에서 전송되는 각 이메일 유형은 "Mailable" 클래스 형태로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 이 디렉터리가 없다면, `make:mail` 아티즌 명령어로 처음 Mailable 클래스를 생성하면 자동으로 생성됩니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 작성하기

Mailable 클래스를 생성한 후, 해당 파일을 열어 내용을 확인해 보세요. Mailable 클래스의 설정은 `envelope`, `content`, `attachments` 등 여러 메서드 내에서 이루어집니다.

`envelope` 메서드는 제목과 경우에 따라 수신자를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성할 [Blade 템플릿](/docs/{{version}}/blade)를 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정하기

<a name="using-the-envelope"></a>
#### Envelope 사용하기

이메일의 발신자, 즉 'from' 주소를 설정하는 방법입니다. 두 가지 방법이 있습니다. 첫 번째는 메시지의 envelope에서 직접 "from" 주소를 지정하는 것입니다.

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

원한다면, `replyTo` 주소도 지정할 수 있습니다.

    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        replyTo: [
            new Address('taylor@example.com', 'Taylor Otwell'),
        ],
        subject: 'Order Shipped',
    );

<a name="using-a-global-from-address"></a>
#### 글로벌 `from` 주소 사용

모든 이메일에 동일한 "from" 주소를 사용하는 경우, 매번 Mailable 클래스에 입력하는 것은 번거롭습니다. 대신, `config/mail.php` 설정 파일에 글로벌 "from" 주소를 지정할 수 있습니다. Mailable 클래스에서 별도로 지정하지 않았다면 이 주소가 사용됩니다.

    'from' => [
        'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
        'name' => env('MAIL_FROM_NAME', 'Example'),
    ],

또한, 글로벌 "reply_to" 주소도 지정할 수 있습니다.

    'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],

<a name="configuring-the-view"></a>
### 뷰(View) 설정

Mailable 클래스의 `content` 메서드 안에서, 이메일 내용 렌더링에 사용할 `view`를 지정할 수 있습니다. 각 이메일은 보통 [Blade 템플릿](/docs/{{version}}/blade)으로 내용을 렌더링하므로, 강력한 Blade 템플릿 기능을 그대로 사용할 수 있습니다.

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }

> [!NOTE]  
> 모든 이메일 템플릿을 저장할 `resources/views/emails` 디렉토리를 생성하는 것이 좋지만, 반드시 이 경로에 둘 필요는 없습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하고 싶다면, 메시지의 `Content` 정의에서 plain-text 템플릿을 지정할 수 있습니다. `view`처럼, `text` 파라미터도 템플릿 이름이어야 하며, 이메일 본문을 렌더링합니다. HTML과 일반 텍스트 버전을 모두 정의할 수 있습니다.

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

가독성을 위해, `html` 파라미터 역시 `view` 파라미터의 별칭으로 사용할 수 있습니다.

    return new Content(
        html: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### 퍼블릭 프로퍼티로 전달

이메일 렌더링 시 사용할 데이터를 뷰로 전달하려면 두 가지 방법이 있습니다. 첫 번째는, Mailable 클래스에 정의된 public 프로퍼티가 자동으로 뷰에서 사용 가능하다는 점을 활용하는 것입니다. 예를 들어, 생성자에서 받은 데이터를 퍼블릭 프로퍼티에 할당하면, 뷰에서 바로 사용할 수 있습니다.

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

이렇게 데이터를 public 프로퍼티로 저장하면, Blade 템플릿에서 즉시 사용할 수 있습니다.

    <div>
        Price: {{ $order->price }}
    </div>

<a name="via-the-with-parameter"></a>
#### `with` 파라미터로 전달

템플릿으로 전달되는 데이터의 형식을 직접 커스터마이즈하고 싶다면, `Content` 정의의 `with` 파라미터를 통해 데이터를 전달할 수 있습니다. 보통은 생성자로 데이터를 전달하지만, 이때는 프로퍼티를 `protected` 혹은 `private`로 설정하세요.

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

`with` 파라미터로 데이터를 전달하면, 뷰에서도 다른 Blade 데이터처럼 바로 사용할 수 있습니다.

    <div>
        Price: {{ $orderPrice }}
    </div>

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드에서 배열로 첨부파일을 반환하세요. 우선, `Attachment` 클래스의 `fromPath` 메서드에 파일 경로를 넘겨 첨부할 수 있습니다.

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

첨부 파일의 이름이나 MIME 타입을 지정하려면, `as` 및 `withMime` 메서드를 사용합니다.

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

<a name="attaching-files-from-disk"></a>
#### 파일 시스템에서 첨부

파일을 [파일 시스템 디스크](/docs/{{version}}/filesystem)에 저장했다면, `fromStorage` 메서드로 첨부할 수 있습니다.

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

첨부파일 이름과 MIME 타입도 지정 가능합니다.

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

기본 디스크 외에 특정 스토리지 디스크를 지정하려면 `fromStorageDisk` 를 사용하세요.

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

<a name="raw-data-attachments"></a>
#### 원시 데이터 첨부

`fromData` 메서드는 직접 생성한 바이트 문자열을 첨부할 때 사용합니다. 예를 들어, 메모리 상에 PDF를 만들어 직접 첨부할 수 있습니다. `fromData`는 클로저(바이트 반환용)와 첨부될 파일 이름을 파라미터로 받습니다.

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

<a name="inline-attachments"></a>
### 인라인 첨부 파일

이메일에 인라인 이미지를 포함하는 것은 번거롭지만, Laravel은 이를 쉽게 할 수 있게 합니다. 인라인 이미지는 이메일 템플릿 내 `$message->embed($pathToImage)`로 첨부합니다. Laravel은 모든 이메일 템플릿에 `$message` 변수를 자동으로 제공합니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]  
> `$message` 변수는 일반 텍스트 메시지 템플릿에는 사용할 수 없습니다. (plain-text는 인라인 첨부를 지원하지 않기 때문입니다.)

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 첨부 이미지 인라인

이미지를 원시 데이터(바이트 문자열 등)로 보유하고 있다면 `$message->embedData($data, 'example-image.jpg')`를 사용하세요.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

단순 문자열 경로로 파일을 첨부하는 것으로 충분할 때도 있지만, 애플리케이션의 어태치 가능한 엔티티가 클래스 형태일 수 있습니다. 예: 사진 첨부 시, `Photo` 모델로 그 사진을 표현할 수 있습니다. 이 경우, attach 메서드에 모델 인스턴스를 전달하면 매우 편리합니다.

이를 사용하려면, 해당 클래스에서 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현해야 하며, `toMailAttachment` 메서드에서 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

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

Attachable 객체를 정의한 후에는, 메일 작성 시 `attachments` 메서드에서 해당 객체 인스턴스를 반환할 수 있습니다.

    /**
     * Get the attachments for the message.
     *
     * @return array<int, \Illuminate\Mail\Mailables\Attachment>
     */
    public function attachments(): array
    {
        return [$this->photo];
    }

첨부 데이터가 Amazon S3 등 외부 스토리지에 저장된다면, Laravel은 [파일 시스템 디스크](/docs/{{version}}/filesystem)에서 첨부 인스턴스를 생성할 수 있는 메서드를 제공합니다.

    // 기본 디스크의 파일에서 첨부 생성...
    return Attachment::fromStorage($this->path);

    // 특정 디스크에서 첨부 생성...
    return Attachment::fromStorageDisk('backblaze', $this->path);

또한, 메모리 내 데이터를 통해 첨부 인스턴스를 생성하려면, `fromData` 메서드에 클로저(데이터 반환), 파일 이름을 전달하세요.

    return Attachment::fromData(fn () => $this->content, 'Photo Name');

첨부 파일의 이름이나 MIME 타입을 커스터마이즈할 때는, `as`, `withMime` 메서드를 사용하세요.

    return Attachment::fromPath('/path/to/file')
            ->as('Photo Name')
            ->withMime('image/jpeg');

<a name="headers"></a>
### 헤더 설정

가끔 메시지에 추가 헤더를 붙여야 할 때가 있습니다. 예를 들어, 커스텀 `Message-Id` 또는 임의의 텍스트 헤더를 설정해야 할 수 있습니다.

이를 위해 mailable에 `headers` 메서드를 정의하세요. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, `messageId`, `references`, `text` 파라미터를 받을 수 있습니다.

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

<a name="tags-and-metadata"></a>
### 태그 및 메타데이터

Mailgun, Postmark 같은 일부 외부 이메일 서비스들은 메시지 "태그"와 "메타데이터" 기능을 제공합니다. 이를 통해 애플리케이션에서 발송한 이메일을 그룹화하거나 추적할 수 있습니다. `Envelope` 정의에서 태그와 메타데이터를 추가할 수 있습니다.

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

Mailgun 드라이버를 사용할 경우, [태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1)와 [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) 관련 문서를 참고하세요. Postmark 관련 정보는 [여기](https://postmarkapp.com/blog/tags-support-for-smtp), [여기](https://postmarkapp.com/support/article/1125-custom-metadata-faq)를 참고하세요.

Amazon SES를 사용하는 경우, `metadata` 메서드로 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer를 기반으로 합니다. Laravel은 메시지 전송 전, Symfony Message 인스턴스와 함께 호출되는 커스텀 콜백을 등록할 수 있게 해줍니다. `Envelope` 정의의 `using` 파라미터에 콜백을 등록하세요.

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

<a name="markdown-mailables"></a>
## 마크다운 Mailable

마크다운(Markdown) Mailable 메시지를 사용하면 [메일 알림](/docs/{{version}}/notifications#mail-notifications)의 사전 제작 템플릿과 컴포넌트를 활용할 수 있습니다. 메시지를 마크다운으로 작성하면, Laravel이 아름답고 반응형인 HTML 템플릿과 함께 자동으로 plain-text 버전까지 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 Mailable 생성하기

마크다운 템플릿과 함께 mailable을 생성하려면, `make:mail` 아티즌 명령어의 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, mailable의 `content` 메서드 내 Content 정의에서는 `view` 대신 `markdown` 파라미터를 사용하면 됩니다.

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

<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성하기

마크다운 Mailable은 Blade 컴포넌트와 마크다운 구문을 함께 사용하여, 미리 준비된 Laravel의 이메일 UI 컴포넌트를 쉽게 활용할 수 있습니다.

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
> 마크다운 이메일을 작성할 때는 들여쓰기를 남용하지 마세요. 마크다운 표준에 따르면, 들여쓰기는 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. `url`과, 선택적으로 `color`를 인자로 받으며, 지원하는 색상은 `primary`, `success`, `error` 입니다. 메시지에 버튼 컴포넌트를 여러 개 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 메시지의 배경색과 약간 다른 색상의 패널로 표현합니다. 특정 메시지에 강조를 줄 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 표를 HTML 테이블로 변환합니다. 기본 마크다운 테이블 정렬 문법을 지원합니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈

모든 마크다운 메일 컴포넌트를 애플리케이션에 내보내서 커스터마이즈할 수 있습니다. `vendor:publish` 아티즌 명령어로 `laravel-mail` 에셋 태그를 퍼블리시하세요.

```shell
php artisan vendor:publish --tag=laravel-mail
```

명령 실행 후, 마크다운 메일 컴포넌트가 `resources/views/vendor/mail`에 내보내집니다. `mail` 디렉토리에는 `html`, `text` 디렉토리가 있으며 각각 모든 컴포넌트 파일이 포함되어 있습니다. 자유롭게 커스터마이즈하세요.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트 내보내기 후, `resources/views/vendor/mail/html/themes/default.css`에서 CSS를 커스터마이즈할 수 있습니다. 이 파일의 스타일은 자동으로 HTML 메일 내 인라인 CSS로 변환되어 반영됩니다.

완전히 새로운 마크다운 테마를 만들려면 `html/themes` 디렉토리에 CSS 파일을 추가하세요. 저장 후, `config/mail.php`의 `theme` 옵션에 테마명을 지정하세요.

Mailable 개별적으로 테마를 바꾸려면, Mailable 클래스의 `$theme` 속성에 해당 테마명을 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 전송

메시지를 전송하려면, `Mail` [파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용하세요. `to` 메서드는 이메일 주소, 유저 인스턴스, 혹은 유저 컬렉션을 받습니다. 객체(혹은 컬렉션)를 전달하면, 해당 객체의 `email`, `name` 속성이 자동으로 수신자 정보로 사용됩니다(꼭 속성이 정의되어 있어야 함). 수신자 지정 뒤에는, mailable 인스턴스를 `send` 메서드에 전달하세요.

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

"to"로만 수신자를 지정할 필요는 없습니다. "to", "cc", "bcc"를 메소드 체이닝으로 함께 사용할 수 있습니다.

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->send(new OrderShipped($order));

<a name="looping-over-recipients"></a>
#### 수신자 반복(루프 돌기)

여러 수신자에게 mailable을 보낼 때는 배열을 돌면서 각각 메일을 보내야 합니다. 하지만, `to` 메서드는 수신자 목록에 계속 추가하므로, 매번 새 mailable 인스턴스를 만들어야 이전 수신자 중복 발송을 막을 수 있습니다.

    foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
        Mail::to($recipient)->send(new OrderShipped($order));
    }

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

Laravel은 기본적으로 `mail` 설정 파일의 `default` 메일러를 사용합니다. 하지만, `mailer` 메서드로 특정 메일러를 선택해서 메시지를 보낼 수 있습니다.

    Mail::mailer('postmark')
            ->to($request->user())
            ->send(new OrderShipped($order));

<a name="queueing-mail"></a>
### 메일 큐에 추가하기

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐 등록

이메일 전송이 응답 속도에 영향을 줄 수 있으므로, 많은 개발자들이 이메일을 백그라운드에서 보내도록 큐에 등록합니다. Laravel은 [통합 큐 API](/docs/{{version}}/queues)를 통해 이 작업을 쉽게 합니다. 수신자 지정 후에는 `queue` 메서드를 사용하세요.

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue(new OrderShipped($order));

이 메서드는 메시지가 백그라운드에서 전송되도록 자동으로 큐에 등록합니다. 사용 전, 반드시 [큐를 설정](/docs/{{version}}/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메일 큐 등록

큐에 등록된 이메일 발송을 일정 시간 후에 지연하고 싶다면, `later` 메서드를 사용할 수 있습니다. 첫 번째 인자로는 메시지를 발송할 시점을 나타내는 `DateTime` 인스턴스를 전달합니다.

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->later(now()->addMinutes(10), new OrderShipped($order));

<a name="pushing-to-specific-queues"></a>
#### 특정 큐 지정하기

`make:mail`로 생성한 모든 mailable 클래스는 `Illuminate\Bus\Queueable` 트레이트를 포함하므로, mailable 인스턴스에서 `onQueue`, `onConnection` 메서드를 사용해 연결 및 큐를 지정할 수 있습니다.

    $message = (new OrderShipped($order))
                    ->onConnection('sqs')
                    ->onQueue('emails');

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue($message);

<a name="queueing-by-default"></a>
#### 기본적으로 큐에 태우기

언제나 큐에 등록해 보내고 싶은 mailable 클래스가 있다면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이 경우, `send` 메서드로 발송해도 큐에 등록됩니다.

    use Illuminate\Contracts\Queue\ShouldQueue;

    class OrderShipped extends Mailable implements ShouldQueue
    {
        // ...
    }

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 등록 Mailable과 DB 트랜잭션

데이터베이스 트랜잭션 내에서 큐 등록되는 mailable은, 트랜잭션이 커밋되기 전 큐 작업이 실행될 수 있습니다. 이 경우, 모델/레코드에 대한 업데이트가 DB에 반영되지 않았거나, 모델이 아직 DB에 존재하지 않아 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`일 때도, 메일을 보낼 때 `afterCommit` 메서드를 호출하여 트랜잭션 커밋 후에 큐 등록하도록 지정할 수 있습니다.

    Mail::to($request->user())->send(
        (new OrderShipped($order))->afterCommit()
    );

또는, mailable의 생성자에서 `afterCommit`을 호출할 수 있습니다.

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

> [!NOTE]  
> 자세한 사항은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## Mailable 렌더링

가끔 메일을 실제로 보내지 않고 HTML 내용을 캡처해야 할 때가 있습니다. 이럴 때 mailable의 `render` 메서드를 호출하면, 평가된 HTML 내용을 문자열로 반환합니다.

    use App\Mail\InvoicePaid;
    use App\Models\Invoice;

    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))->render();

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 Mailable 미리보기

Mailable 템플릿을 디자인할 때, 웹 브라우저에서 빠르게 디자인 결과를 미리 확인하고 싶을 때가 있습니다. 이를 위해, 라우트 클로저 또는 컨트롤러에서 mailable을 직접 반환하면 해당 mailable이 렌더되어 브라우저에 표시됩니다.

    Route::get('/mailable', function () {
        $invoice = App\Models\Invoice::find(1);

        return new App\Mail\InvoicePaid($invoice);
    });

<a name="localizing-mailables"></a>
## Mailable 현지화

Laravel로 메일을 현지화하여, 현재 요청의 로케일과 다르게 메일을 보낼 수 있습니다. 또한, 메일이 큐에 쌓여도 이 언어 설정이 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 지정하세요. 메일의 템플릿이 평가되는 동안 지정한 언어로 변한 뒤, 완료되면 원래 로케일로 복구됩니다.

    Mail::to($request->user())->locale('es')->send(
        new OrderShipped($order)
    );

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

애플리케이션에서 각 사용자의 선호 로케일을 저장할 수 있습니다. 모델 중 하나 이상에 `HasLocalePreference` 계약을 구현하면, 메일 발송 시 해당 사용자의 언어를 자동으로 사용합니다.

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

이 인터페이스를 구현하면, Laravel은 해당 모델로 메일이나 알림을 보낼 때 자동으로 언어를 적용합니다. 따라서, `locale` 메서드를 따로 호출할 필요가 없습니다.

    Mail::to($request->user())->send(new OrderShipped($order));

<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### Mailable 내용 테스트

Laravel은 mailable의 구조를 검사하기 위한 다양한 메서드를 제공합니다. 또한, mailable에 기대하는 내용이 실제로 포함되어 있는지도 테스트할 수 있습니다. 제공되는 메서드로는 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`, `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`, `assertHasAttachment`, `assertHasAttachedData`, `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등이 있습니다.

"HTML 어서션"은 mailable의 HTML 버전에 특정 문자열이 포함되어 있는지 검사하고, "텍스트 어서션"은 plain-text 버전을 검사합니다.

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

<a name="testing-mailable-sending"></a>
### Mailable 발송 테스트

mailable의 내용을 검사하는 테스트와, 실제로 특정 사용자에게 mailable이 "전송"됐는지 검사하는 테스트는 분리해서 작성하길 권장합니다. mailable의 내용은 테스트하려는 코드와 무관한 경우가 많으며, Laravel이 실제로 해당 mailable을 보내려고 시도했는지만 어서션하는 것으로 충분합니다.

메일 전송을 막으려면, `Mail` 파사드의 `fake` 메서드를 사용하세요. `fake` 호출 후, mailable이 전송 혹은 큐에 등록됐는지, 어떤 데이터가 전달됐는지 어서션할 수 있습니다.

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

            // Assert a mailable was not sent...
            Mail::assertNotSent(AnotherMailable::class);

            // Assert 3 total mailables were sent...
            Mail::assertSentCount(3);
        }
    }

메시지를 큐에 전송하는 경우에는 `assertSent` 대신 `assertQueued`를 사용해야 합니다.

    Mail::assertQueued(OrderShipped::class);
    Mail::assertNotQueued(OrderShipped::class);
    Mail::assertNothingQueued();
    Mail::assertQueuedCount(3);

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued`에는 클로저를 전달할 수 있으며, 특정 조건을 만족하는 mailable이 전송/큐에 등록됐는지 검사할 수 있습니다. 조건을 만족하는 mailable이 하나라도 있으면 어서션은 성공합니다.

    Mail::assertSent(function (OrderShipped $mail) use ($order) {
        return $mail->order->id === $order->id;
    });

클로저로 전달받는 mailable 인스턴스는 다양한 수신자/제목 검사 메서드를 제공합니다.

    Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
        return $mail->hasTo($user->email) &&
               $mail->hasCc('...') &&
               $mail->hasBcc('...') &&
               $mail->hasReplyTo('...') &&
               $mail->hasFrom('...') &&
               $mail->hasSubject('...');
    });

첨부파일을 검사하는 유용한 메서드도 있습니다.

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

메일이 전송되지 않았음을 검사하는 `assertNotSent`와 `assertNotQueued`가 있습니다. 둘 중 하나라도 메일이 **전송 또는 큐에 등록되지 않았는지**를 확인하려면 `assertNothingOutgoing`와 `assertNotOutgoing`를 사용할 수 있습니다.

    Mail::assertNothingOutgoing();

    Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
        return $mail->order->id === $order->id;
    });

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경

실제 이메일 주소로 메일을 보내고 싶지 않은 로컬 개발 환경에서는 메일을 실제로 발송하지 못하도록 여러 가지 방법을 제공합니다.

<a name="log-driver"></a>
#### Log 드라이버

실제 메일 대신, `log` 메일 드라이버를 사용하면 모든 이메일 메시지가 로그 파일에 기록됩니다. 주로 로컬 개발 환경에서 사용합니다. 환경별 설정 자세한 내용은 [구성 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

대안으로, [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스를 사용하여 `smtp` 드라이버를 통해 "더미" 메일박스에 이메일을 보낼 수 있습니다. 이 방법은 Mailtrap의 메시지 뷰어에서 실제 이메일을 확인할 수 있는 장점이 있습니다.

[Laravel Sail](/docs/{{version}}/sail)을 사용 중이라면, [Mailpit](https://github.com/axllent/mailpit)으로 메시지를 미리볼 수 있습니다. Sail이 동작 중일 때, Mailpit 인터페이스는 `http://localhost:8025`에서 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 글로벌 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드로 모든 이메일의 수신자를 전역적으로 지정할 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다.

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

<a name="events"></a>
## 이벤트

메일 메시지 전송 과정 중에 두 개의 이벤트가 발생합니다. 메시지 전송 전에 `MessageSending` 이벤트가, 메시지 전송 후에 `MessageSent` 이벤트가 발생합니다. 이 이벤트들은 큐에서는 아니라, 실제 메일이 *발송*될 때 발생합니다. `App\Providers\EventServiceProvider`에서 이벤트 리스너를 등록할 수 있습니다.

    use App\Listeners\LogSendingMessage;
    use App\Listeners\LogSentMessage;
    use Illuminate\Mail\Events\MessageSending;
    use Illuminate\Mail\Events\MessageSent;

    /**
     * The event listener mappings for the application.
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

<a name="custom-transports"></a>
## 커스텀 트랜스포트

Laravel은 다양한 메일 트랜스포트를 기본으로 제공하지만, 직접 구현한 트랜스포트를 통해 지원되지 않는 서비스에 메일을 보낼 수도 있습니다. `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속하여, `doSend`, `__toString()` 메서드를 구현하세요.

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

커스텀 트랜스포트 정의 후에는, `Mail` 파사드의 `extend` 메서드로 등록할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 등록하면 됩니다. `extend`에 전달되는 콜백의 `$config` 인자로는 `config/mail.php`의 해당 메일러 설정값이 전달됩니다.

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

트랜스포트 등록 후, `config/mail.php` 파일에 해당 트랜스포트를 사용하는 메일러 정의를 추가하세요.

    'mailchimp' => [
        'transport' => 'mailchimp',
        // ...
    ],

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

Laravel은 Mailgun, Postmark 등 일부 Symfony가 관리하는 메일 트랜스포트를 지원합니다. 그 외 추가 트랜스포트도 Composer로 패키지를 설치한 후 트랜스포트를 등록하면 사용할 수 있습니다. 예를 들어, "Brevo"(구 Sendinblue) Symfony 메일러를 설치하고 등록할 수 있습니다.

```none
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 설치 후, `services` 설정 파일에 Brevo API 인증 정보를 추가하세요.

    'brevo' => [
        'key' => 'your-api-key',
    ],

트랜스포트 등록은 보통 서비스 프로바이더의 `boot`에서 진행합니다.

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

트랜스포트 등록 후엔, `config/mail.php` 설정 파일에 해당 트랜스포트를 사용하는 메일러를 정의하세요.

    'brevo' => [
        'transport' => 'brevo',
        // ...
    ],