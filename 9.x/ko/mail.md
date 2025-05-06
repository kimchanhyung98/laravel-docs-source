# 메일

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [폴백(실패) 설정](#failover-configuration)
- [Mailable 생성](#generating-mailables)
- [Mailable 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더(Header)](#headers)
    - [태그 & 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
- [마크다운(Markdown) Mailable](#markdown-mailables)
    - [마크다운 Mailable 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [Mailable 렌더링](#rendering-mailables)
    - [브라우저에서 Mailable 미리보기](#previewing-mailables-in-the-browser)
- [Mailable 현지화(Localization)](#localizing-mailables)
- [Mailable 테스트](#testing-mailables)
- [메일 & 로컬 개발환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 트랜스포트](#custom-transports)
    - [추가 Symfony 트랜스포트](#additional-symfony-transports)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/6.0/mailer.html) 컴포넌트를 기반으로 한, 깔끔하고 단순한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Amazon SES, 그리고 `sendmail`을 통한 이메일 발송을 위한 드라이버를 제공하므로, 로컬이나 클라우드 기반 서비스를 통해 빠르게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일에 설정된 각 메일러는 고유한 설정 및 "트랜스포트"를 가질 수 있으므로, 애플리케이션은 상황에 따라 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark를, 대량 메일은 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 안에는 `mailers` 설정 배열이 있습니다. 이 배열은 Laravel에서 지원하는 주요 메일 드라이버/트랜스포트에 대한 샘플 설정이 들어 있으며, `default` 설정 값은 애플리케이션이 이메일을 보낼 때 기본적으로 사용할 메일러를 지정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 준비 사항

Mailgun, Postmark와 같은 API 기반 드라이버는 SMTP 서버를 통한 메일 전송보다 더 단순하고 빠른 경우가 많습니다. 가능하다면 이러한 드라이버를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer 트랜스포트를 설치합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `mailgun`으로 설정합니다. 기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션이 있는지 확인하세요:

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
    ],

미국 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)이 아닌 경우, 지역 엔드포인트를 `services` 설정 파일에 지정할 수 있습니다:

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    ],

<a name="postmark-driver"></a>
#### Postmark 드라이버

Postmark 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer 트랜스포트를 설치합니다:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 파일에서 `default` 옵션을 `postmark`로 설정하세요. 기본 메일러를 설정한 후, `config/services.php`에 다음 옵션이 있는지 확인하세요:

    'postmark' => [
        'token' => env('POSTMARK_TOKEN'),
    ],

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하려면 mailer 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

    'postmark' => [
        'transport' => 'postmark',
        'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    ],

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 구성할 수 있습니다.

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 우선 PHP용 Amazon AWS SDK를 설치해야 합니다. Composer 패키지 매니저로 이 라이브러리를 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```

그 다음, `config/mail.php` 파일의 `default` 옵션을 `ses`로 설정하고, `config/services.php`에 다음 옵션이 있는지 확인하세요:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

AWS [임시 자격증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 세션 토큰으로 사용하려면 SES 설정에 `token` 키를 추가하세요:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'token' => env('AWS_SESSION_TOKEN'),
    ],

Laravel이 이메일 전송 시 AWS SDK의 `SendEmail` 메서드에 추가 옵션을 전달하도록 하려면, `ses` 설정에서 `options` 배열을 정의할 수 있습니다:

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

<a name="failover-configuration"></a>
### 폴백(실패) 설정

외부 메일 전송 서비스를 구성했으나 해당 서비스가 다운될 수 있습니다. 이런 경우, 하나 이상의 백업 메일 전송 설정(폴백)을 정의해 두는 것이 좋습니다.

이를 위해, `failover` 트랜스포트를 사용하는 메일러를 `mail` 설정 파일에 정의해야 합니다. `failover` 메일러의 설정 배열에는 메일 드라이버가 사용될 우선 순서를 참조하는 `mailers` 배열이 있어야 합니다:

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

failover 메일러를 정의했다면, 애플리케이션이 사용하는 기본 메일러로 지정해야 합니다. 이를 위해 `mail` 설정 파일에서 `default` 옵션에 해당 메일러의 이름을 입력하세요:

    'default' => env('MAIL_MAILER', 'failover'),

<a name="generating-mailables"></a>
## Mailable 생성

Laravel 애플리케이션을 개발할 때, 애플리케이션에서 발송하는 각 이메일 종류는 "Mailable" 클래스 형태로 나타냅니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 만약 이 디렉토리가 없다면, `make:mail` 아티즌(Artisan) 명령어로 첫 Mailable을 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## Mailable 작성

Mailable 클래스를 생성했다면, 해당 파일을 열어서 구조를 살펴봅니다. Mailable 클래스는 `envelope`, `content`, `attachments` 등의 여러 메서드에서 구성할 수 있습니다.

`envelope` 메서드는 메시지의 제목(subject) 및 경우에 따라 수신자를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문을 생성할 [Blade 템플릿](/docs/{{version}}/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-envelope"></a>
#### Envelope 사용하기

먼저, 이메일의 발신자 설정을 살펴봅니다. 즉, 이메일의 "from" 주소를 지정하는 방법입니다. 발신자 설정에는 두 가지 방법이 있습니다. 우선 메시지의 envelope에서 "from" 주소를 지정할 수 있습니다:

    use Illuminate\Mail\Mailables\Address;
    use Illuminate\Mail\Mailables\Envelope;

    /**
     * Get the message envelope.
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

필요하다면 `replyTo` 주소도 지정할 수 있습니다:

    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        replyTo: [
            new Address('taylor@example.com', 'Taylor Otwell'),
        ],
        subject: 'Order Shipped',
    );

<a name="using-a-global-from-address"></a>
#### 글로벌 `from` 주소 사용

애플리케이션의 모든 이메일이 동일한 "from" 주소를 사용할 경우, 각 Mailable에서 매번 `from`을 지정하는 것이 번거로울 수 있습니다. 이럴 땐, `config/mail.php` 설정 파일에 글로벌 "from" 주소를 지정할 수 있습니다. 이 경우, 별도 지정이 없는 한 해당 주소가 사용됩니다:

    'from' => ['address' => 'example@example.com', 'name' => 'App Name'],

또한, 글로벌 "reply_to" 주소 역시 설정 가능합니다:

    'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],

<a name="configuring-the-view"></a>
### 뷰(View) 설정

Mailable 클래스의 `content` 메서드에서는 이메일 본문을 랜더링할 때 사용할 `view(뷰)`를 지정할 수 있습니다. 이메일은 보통 [Blade 템플릿](/docs/{{version}}/blade)을 사용하므로, Blade의 모든 기능을 이용할 수 있습니다:

    /**
     * Get the message content definition.
     *
     * @return \Illuminate\Mail\Mailables\Content
     */
    public function content()
    {
        return new Content(
            view: 'emails.orders.shipped',
        );
    }

> **참고**
> 이메일 템플릿을 위한 `resources/views/emails` 디렉토리를 생성하는 것이 좋지만, 반드시 그럴 필요 없이 `resources/views` 내 원하는 위치에 배치 가능합니다.

<a name="plain-text-emails"></a>
#### 평문(Plain text) 이메일

이메일의 평문 버전을 정의하려면, 메시지의 `Content` 정의 시 평문 템플릿을 `text` 파라미터로 지정하면 됩니다. `view`와 마찬가지로 `text`에는 템플릿명을 지정합니다. HTML 버전과 평문 버전을 모두 정의할 수 있습니다:

    /**
     * Get the message content definition.
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

가독성을 위해 `html` 파라미터를 `view`의 별칭처럼 사용할 수도 있습니다:

    return new Content(
        html: 'emails.orders.shipped',
        text: 'emails.orders.shipped-text'
    );

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 프로퍼티로 전달

보통, 이메일 랜더링 시 사용할 데이터를 뷰에 전달해야 합니다. 데이터를 전달하는 방법은 두 가지가 있습니다. 첫 번째로, Mailable 클래스의 public 프로퍼티에 데이터를 할당하면 자동으로 뷰에서 사용 가능합니다. 예를 들어, 생성자에서 데이터를 받아 public 프로퍼티에 할당할 수 있습니다:

```php
// 코드 예제는 번역되지 않습니다. 원문 참고
```

데이터가 public 프로퍼티에 할당되면 뷰(Blade 템플릿)에서 아래와 같이 사용할 수 있습니다:

    <div>
        Price: {{ $order->price }}
    </div>

<a name="via-the-with-parameter"></a>
#### `with` 파라미터로 전달

템플릿에 데이터를 전달하기 전에 포맷을 커스터마이즈하고 싶다면, Content 정의의 `with` 파라미터를 사용해 수동으로 전달할 수 있습니다. 이때 생성자에서 데이터를 받아 protected 또는 private 프로퍼티에 저장한다면, 해당 데이터는 자동으로 뷰에 노출되지 않습니다:

```php
// 코드 예제는 번역되지 않습니다. 원문 참고
```

`with`를 통해 전달된 데이터도 Blade 템플릿에서 아래와 같이 사용할 수 있습니다:

    <div>
        Price: {{ $orderPrice }}
    </div>

<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면 메시지의 `attachments` 메서드가 반환하는 배열에 첨부파일을 넣으면 됩니다. 예시처럼 파일 경로를 `Attachment` 클래스의 `fromPath` 메서드에 전달해 첨부할 수 있습니다:

    use Illuminate\Mail\Mailables\Attachment;

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromPath('/path/to/file'),
        ];
    }

첨부파일의 표시 이름 또는 MIME 타입을 지정하고 싶다면, `as`, `withMime` 메서드를 사용할 수 있습니다:

    Attachment::fromPath('/path/to/file')
        ->as('name.pdf')
        ->withMime('application/pdf'),

<a name="attaching-files-from-disk"></a>
#### 저장소(디스크)에서 파일 첨부

[파일 시스템 디스크](/docs/{{version}}/filesystem)에 파일이 저장되어 있다면, `fromStorage` 메서드를 사용해 첨부할 수 있습니다:

    Attachment::fromStorage('/path/to/file'),

특정 디스크를 지정하려면 `fromStorageDisk` 메서드를 사용합니다:

    Attachment::fromStorageDisk('s3', '/path/to/file')
        ->as('name.pdf')
        ->withMime('application/pdf'),

<a name="raw-data-attachments"></a>
#### Raw 데이터 첨부

`fromData` 메서드로 바이트 스트링을 직접 첨부파일로 추가할 수 있습니다. 예를 들어, 메모리에 PDF를 생성하고 바로 첨부할 때 사용할 수 있습니다. 이 메서드는 raw 데이터 바이트를 리턴하는 클로저와 첨부파일 이름을 받습니다:

    Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
        ->withMime('application/pdf'),

<a name="inline-attachments"></a>
### 인라인 첨부파일

인라인 이미지를 이메일에 삽입하는 것은 보통 번거롭지만, Laravel은 손쉽게 이미지 첨부 및 삽입을 지원합니다. `$message` 변수의 `embed` 메서드를 Blade 템플릿 내에서 사용하세요(이 변수는 자동 제공):

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> **경고**
> `$message` 변수는 평문 이메일 템플릿에서는 사용할 수 없습니다(인라인 첨부 활용 불가).

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

raw 이미지 데이터 문자열을 이미 가지고 있다면 `$message`의 `embedData` 메서드를 사용하여 삽입할 수 있습니다. 이때 파일명을 부여해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

단순 파일 경로만으로 첨부파일을 다루는 것이 충분한 경우도 있지만, 애플리케이션에서 첨부될 엔티티가 클래스로 표현되는 경우가 있습니다. 예를 들어 사진을 첨부할 때, `Photo` 모델로 구현되어 있다면 이 모델 자체를 첨부파일로 전달하는 것이 직관적일 것입니다. 이것이 attachable 객체의 개념입니다.

`Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하여 해당 객체에 `toMailAttachment` 메서드를 제공하면 attachable로 사용할 수 있습니다:

```php
// 코드 예제는 번역되지 않습니다. 원문 참고
```

이제 해당 객체를 바로 `attachments` 메서드에서 리턴하여 첨부할 수 있습니다.

S3 등 원격 파일 스토리지에 저장된 데이터로도 첨부파일 인스턴스를 생성할 수 있습니다. 또한 메모리에 있는 데이터로부터 첨부파일을 만들려면 `fromData` 메서드에 클로저를 전달하세요.

첨부파일의 이름이나 MIME type 역시 `as` 및 `withMime` 메서드로 커스터마이징 가능합니다.

<a name="headers"></a>
### 헤더(Header)

메일 전송 시 추가 헤더가 필요한 경우가 있습니다(예: 커스텀 `Message-Id` 및 기타 텍스트 헤더).

이를 위해 Mailable에 `headers` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하며, `messageId`, `references`, `text` 등을 지정할 수 있습니다. 값은 필요한 만큼만 지정하면 됩니다.

<a name="tags-and-metadata"></a>
### 태그 & 메타데이터

Mailgun, Postmark 등 일부 외부 이메일 공급자는 이메일에 "태그" 및 "메타데이터"를 붙여 그룹화, 추적이 가능합니다. `Envelope` 정의에서 태그와 메타데이터를 추가할 수 있습니다.

- Mailgun의 [태그](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1), [메타데이터](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages)
- Postmark의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)

Amazon SES를 사용하는 경우, `metadata` 메서드로 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스터마이징

Laravel의 메일 기능은 Symfony Mailer에 의해 구동됩니다. 메일이 전송되기 전에 Symfony Message 인스턴스에 대해 실행될 커스텀 콜백을 등록할 수 있습니다. 이를 위해서 `Envelope` 정의의 `using` 파라미터에 콜백을 지정하세요.

<a name="markdown-mailables"></a>
## 마크다운(Markdown) Mailable

마크다운 mailable 메시지는 [메일 알림](/docs/{{version}}/notifications#mail-notifications)의 사전 구축된 템플릿과 컴포넌트를 활용할 수 있습니다. 메시지가 마크다운으로 작성되어, Laravel이 자동으로 반응형 HTML 템플릿과 평문 버전을 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 Mailable 생성

마크다운 템플릿과 함께 mailable을 생성하려면, `make:mail` 아티즌 명령어에서 `--markdown` 옵션을 사용합니다:

```shell
php artisan make:mail OrderShipped --markdown=emails.orders.shipped
```

Mailable의 `content` 메서드에서는 `view` 대신 `markdown` 파라미터를 사용하세요.

<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성

마크다운 메시지는 Blade 컴포넌트와 마크다운 문법을 함께 사용, Laravel의 미리 준비된 이메일 UI 컴포넌트를 쉽게 조합할 수 있습니다.

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

> **참고**
> 마크다운 이메일 작성 시 마크다운 문법상 들여쓰기를 과하게 사용하지 마세요. 과도한 들여쓰기는 코드블럭으로 처리됩니다.

#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 인자를 가집니다(지원 색상: `primary`, `success`, `error`). 버튼 컴포넌트는 여러 개 추가할 수 있습니다.

#### 패널 컴포넌트

패널 컴포넌트는 지정된 텍스트 블럭을 메시지의 다른 영역과 구분된 배경색의 패널로 표시해 강조합니다.

#### 테이블 컴포넌트

테이블 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환합니다. 열 정렬은 마크다운 표준에 따릅니다.

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

마크다운 메일 컴포넌트는 `vendor:publish` 명령어의 `laravel-mail` 태그로 내 애플리케이션으로 직접 추출(customize)할 수 있습니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어는 `resources/views/vendor/mail`에 컴포넌트를 복사하며, 각 컴포넌트의 HTML, Text 버전 등을 자유롭게 수정할 수 있습니다.

#### CSS 커스터마이징

컴포넌트를 추출한 후, `resources/views/vendor/mail/html/themes/default.css` 파일에서 CSS를 원하는 대로 편집하세요. 새로운 테마를 만들 경우 해당 CSS 파일을 추가한 뒤, `config/mail.php` 파일의 `theme` 옵션을 업데이트하면 됩니다.

개별 mailable마다 사용할 테마를 지정하려면, mailable 클래스의 `$theme` 프로퍼티를 적절히 설정하세요.

<a name="sending-mail"></a>
## 메일 발송

메시지를 전송하려면 [Mail 파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용합니다. 이 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체 또는 컬렉션을 전달하면, 해당 객체의 `email`, `name` 속성을 자동으로 수신자 정보로 사용합니다.

수신자 지정 이후, mailable 클래스 인스턴스를 `send` 메서드에 전달합니다. "to" 외에도 "cc", "bcc" 를 체인으로 추가 지정할 수 있습니다.

#### 수신자별 반복 발송

여러 수신자에 반복적으로 메일을 보내야 한다면, 반드시 각 수신자마다 mailable 인스턴스를 새로 생성해야 중복 발송되는 일이 없습니다.

#### 특정 메일러로 발송

기본적으로는 `config/mail.php`의 `default` 메일러를 사용하지만, `mailer` 메서드로 특정 메일러를 사용할 수 있습니다.

<a name="queueing-mail"></a>
### 메일 큐잉

#### 메일 메시지 큐잉

이메일 전송은 애플리케이션의 응답속도에 영향을 줄 수 있으므로, 대부분의 개발자는 이메일 메시지를 백그라운드 큐에 등록합니다. Laravel의 [통합 큐 API](/docs/{{version}}/queues)를 이용해 메일을 쉽게 큐잉할 수 있습니다. `queue` 메서드를 사용하세요.

#### 지연(delayed) 큐잉

`later` 메서드로 큐 등록을 딜레이할 수 있습니다. 첫 번째 인자로 메시지가 발송되어야 할 시점의 `DateTime` 인스턴스를 넘겨줍니다.

#### 특정 큐 지정

모든 mailable 클래스는 기본적으로 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, `onQueue`, `onConnection` 메서드로 큐/커넥션 설정이 가능합니다.

#### 큐 기본화

항상 큐에 등록되고자 하는 mailable 클래스는 `ShouldQueue` 인터페이스를 구현하세요. `send` 메서드를 사용해도 자동으로 큐잉됩니다.

#### 큐 Mailable과 DB 트랜잭션

큐 Mailable이 데이터베이스 트랜잭션 내에서 디스패치(dispatch)될 경우, 트랜잭션 커밋 전에 큐가 처리되어, 아직 커밋되지 않은 DB 상태가 반영되지 않을 수 있습니다. 큐의 `after_commit` 옵션이 `false`라면, `afterCommit` 메서드 호출로 트랜잭션 커밋 이후에 큐를 처리하도록 할 수 있습니다.

> **참고**
> 이 문제의 자세한 대처법은 [큐 작업과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## Mailable 렌더링

메일을 실제로 전송하지 않고, mailable의 HTML 콘텐츠만 추출하고 싶다면, mailable 인스턴스의 `render` 메서드를 호출하세요.

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 Mailable 미리보기

Mailable 템플릿을 개발 중, 실시간 미리보기가 필요하다면, 라우트 또는 컨트롤러에서 mailable을 반환(return)하세요. 그러면 이메일 발송 없이 브라우저에서 랜더링된 결과를 확인할 수 있습니다.

> **경고**
> [인라인 첨부파일](#inline-attachments)은 브라우저 미리보기에서 랜더링되지 않습니다. 해당 기능을 확인하려면 [Mailpit](https://github.com/axllent/mailpit)이나 [HELO](https://usehelo.com) 같은 이메일 테스트 도구를 이용하세요.

<a name="localizing-mailables"></a>
## Mailable 현지화(Localization)

Laravel은 요청의 현재 로케일과 다른 언어로 mailable을 보낼 수 있으며, 나아가 큐에도 로케일을 저장합니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 언어를 지정할 수 있습니다. mailable의 템플릿 평가 시 해당 로케일로 전환되었다가, 처리 후 원래 로케일로 복귀합니다.

### 사용자 선호 로케일(User Preferred Locales)

사용자별로 선호 로케일을 저장한 경우, 모델에 `HasLocalePreference` 인터페이스를 구현하면 Laravel이 해당 모델로 메일을 보낼 때 이 로케일을 자동으로 사용합니다. 별도의 `locale` 호출이 필요 없습니다.

<a name="testing-mailables"></a>
## Mailable 테스트

Laravel은 mailable의 구조 및 내용을 검증할 수 있는 다양한 메서드를 제공합니다.
- `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInOrderInHtml`
- `assertSeeInText`, `assertDontSeeInText`, `assertSeeInOrderInText`
- `assertHasAttachment`, `assertHasAttachedData`
- `assertHasAttachmentFromStorage`, `assertHasAttachmentFromStorageDisk` 등

"HTML" assertion은 HTML 버전을, "text" assertion은 평문 버전을 대상으로 동작합니다.

#### Mailable 전송 테스트

mailable의 콘텐츠 테스트와 "특정 사용자에게 전송됨" 검증 테스트는 분리하는 것이 좋습니다. mailable의 전송 여부 검증은 [Mail fake](/docs/{{version}}/mocking#mail-fake) 문서 참고.

<a name="mail-and-local-development"></a>
## 메일 & 로컬 개발환경

이메일을 실제 주소로 전송하고 싶지 않을 때, Laravel은 "실제 전송"을 비활성화할 수 있는 몇 가지 방법을 지원합니다.

#### Log 드라이버

`log` 메일 드라이버는 이메일을 로그파일로 기록하기만 하므로, 로컬 개발 시에만 사용할 것을 권장합니다. 환경별 설정법은 [설정 문서](/docs/{{version}}/configuration#environment-configuration) 참고.

#### HELO / Mailtrap / Mailpit

[HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)과 같은 도구 또는 Mailpit을 사용할 수 있습니다. `smtp`드라이버로 더미(가짜) 메일박스에 메일을 보냅니다. [Laravel Sail](/docs/{{version}}/sail) 사용 시에는 Sail 실행 중인 상태에서 `http://localhost:8025`에서 Mailpit 인터페이스에 접근할 수 있습니다.

#### 글로벌 `to` 주소 사용

`Mail` 파사드의 `alwaysTo` 메서드를 사용해 모든 이메일의 수신자를 특정 주소로 지정할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

<a name="events"></a>
## 이벤트

이메일 발송 과정에서 Laravel은 두 가지 이벤트를 발생시킵니다. 발송 전에는 `MessageSending`, 발송 후에는 `MessageSent` 이벤트가 발생합니다(큐잉 시점이 아님에 유의). `App\Providers\EventServiceProvider`에 이벤트 리스너를 등록할 수 있습니다.

<a name="custom-transports"></a>
## 커스텀 트랜스포트

Laravel은 다양한 메일 트랜스포트를 내장하지만, 지원하지 않는 외부 서비스로 메일을 보내려면 직접 트랜스포트를 작성할 수 있습니다. `Symfony\Component\Mailer\Transport\AbstractTransport`를 상속하고, `doSend`, `__toString()` 메서드를 구현합니다.

트랜스포트를 정의한 후, `Mail` 파사드의 `extend`로 등록하면 됩니다(일반적으로 `AppServiceProvider`의 `boot` 메서드에서). `config/mail.php` 설정에서 트랜스포트를 사용하는 메일러를 정의할 수 있습니다.

<a name="additional-symfony-transports"></a>
### 추가 Symfony 트랜스포트

Laravel은 Mailgun, Postmark 등 일부 Symfony 트랜스포트를 지원합니다. 더 많은 Symfony 트랜스포트를 추가하려면, 해당 mailer를 Composer로 설치하고, 등록하면 됩니다. 예를 들어, Sendinblue mailer 등록은 다음과 같습니다:

```none
composer require symfony/sendinblue-mailer symfony/http-client
```

`services` 설정에 API 키 등록 후, `Mail::extend`를 통해 트랜스포트를 등록합니다. 이후 `config/mail.php`에서 해당 트랜스포트를 사용하는 메일러를 정의하세요.