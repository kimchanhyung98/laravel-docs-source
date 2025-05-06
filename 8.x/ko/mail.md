# 메일

- [소개](#introduction)
    - [환경설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [장애 조치(Failover) 설정](#failover-configuration)
- [Mailable 클래스 생성](#generating-mailables)
- [Mailable 클래스 작성](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [SwiftMailer 메시지 커스터마이즈](#customizing-the-swiftmailer-message)
- [마크다운 Mailable](#markdown-mailables)
    - [마크다운 Mailable 생성](#generating-markdown-mailables)
    - [마크다운 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 전송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [Mailable 렌더링](#rendering-mailables)
    - [브라우저에서 Mailable 미리보기](#previewing-mailables-in-the-browser)
- [Mailable 현지화](#localizing-mailables)
- [Mailable 테스트](#testing-mailables)
- [메일 & 로컬 개발](#mail-and-local-development)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [SwiftMailer](https://swiftmailer.symfony.com/) 라이브러리를 기반으로 하는 깔끔하고 간단한 이메일 API를 제공합니다. Laravel 및 SwiftMailer는 SMTP, Mailgun, Postmark, Amazon SES, 그리고 `sendmail`을 통한 이메일 전송 드라이버를 제공하므로 로컬 또는 클라우드 기반 서비스로 빠르게 메일 발송을 시작할 수 있습니다.

<a name="configuration"></a>
### 환경설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 정의된 각 메일러는 고유한 설정과 전송(transport)을 가질 수 있으므로, 여러 이메일 서비스를 사용하여 상황에 따라 메일을 보낼 수 있습니다. 예를 들어, 트랜잭션 메일은 Postmark로, 대량 메일은 Amazon SES로 보낼 수 있습니다.

`mail` 설정 파일의 `mailers` 배열에는 Laravel이 지원하는 주요 메일 드라이버/트랜스포트의 샘플 설정이 들어 있습니다. `default` 설정 값은 애플리케이션이 이메일을 보낼 때 어떤 메일러를 기본적으로 사용할지 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 트랜스포트 사전 요구사항

Mailgun, Postmark 등 API 기반 드라이버는 SMTP 서버를 이용하는 것보다 더 간단하고 빠릅니다. 가능하다면 이런 드라이버를 사용하시길 권장합니다. 모든 API 기반 드라이버를 사용하려면 Guzzle HTTP 라이브러리가 필요합니다. Composer를 통해 설치할 수 있습니다:

    composer require guzzlehttp/guzzle

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 먼저 Guzzle HTTP 라이브러리를 설치하세요. 그런 다음, `config/mail.php`의 `default` 옵션을 `mailgun`으로 설정합니다. 그리고 `config/services.php` 파일에 다음 옵션이 있는지 확인하세요.

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
    ],

미국이 아닌 [Mailgun 리전](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용한다면, `services` 설정 파일의 endpoint를 정의할 수 있습니다:

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    ],

<a name="postmark-driver"></a>
#### Postmark 드라이버

Postmark 드라이버를 사용하려면, Composer를 이용해 Postmark의 SwiftMailer transport를 설치하세요:

    composer require wildbit/swiftmailer-postmark

그 다음, Guzzle HTTP 라이브러리를 설치하고 `config/mail.php`의 `default`를 `postmark`로 설정합니다. 마지막으로, `config/services.php` 파일이 다음과 같이 구성되어 있는지 확인하세요:

    'postmark' => [
        'token' => env('POSTMARK_TOKEN'),
    ],

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하려면 `message_stream_id` 옵션을 메일러 설정 배열에 추가하세요. 이 설정 배열은 `config/mail.php`에서 찾을 수 있습니다:

    'postmark' => [
        'transport' => 'postmark',
        'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    ],

이렇게 하면 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러를 설정할 수 있습니다.

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 PHP용 AWS SDK를 설치해야 합니다. Composer를 이용해 라이브러리를 설치하세요:

```bash
composer require aws/aws-sdk-php
```

이어서, `config/mail.php`의 `default`를 `ses`로 설정하고 `config/services.php` 파일에 아래와 같이 입력하세요:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면 `token` 키를 추가할 수 있습니다:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'token' => env('AWS_SESSION_TOKEN'),
    ],

Laravel이 AWS SDK의 `SendRawEmail` 메서드에 추가 옵션을 전달하도록 하려면, `ses` 설정값에 `options` 배열을 입력하세요:

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'options' => [
            'ConfigurationSetName' => 'MyConfigurationSet',
            'Tags' => [
                ['Name' => 'foo', 'Value' => 'bar'],
            ],
        ],
    ],

<a name="failover-configuration"></a>
### 장애 조치(Failover) 설정

가끔 외부 메일 서비스가 다운될 수 있습니다. 이럴 때를 대비해 1개 이상의 백업 메일 전송 구성을 정의하여, 기본 운송 드라이버가 다운될 경우 자동으로 사용할 수 있습니다.

이를 구현하려면 `failover` 트랜스포트를 사용하는 메일러를 `mail` 설정 파일에 정의합니다. 이 메일러의 설정 배열 안의 `mailers`에는 메일 드라이버를 사용할 순서를 배열로 지정합니다:

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

이제 장애 조치 메일러를 기본 메일러로 설정하려면 `mail` 설정 파일의 `default` 키 값을 해당 이름으로 변경하면 됩니다:

    'default' => env('MAIL_MAILER', 'failover'),

<a name="generating-mailables"></a>
## Mailable 클래스 생성

Laravel 애플리케이션에서 각 이메일 유형은 "Mailable" 클래스로 표현됩니다. 이 클래스는 `app/Mail` 디렉터리에 저장됩니다. 해당 디렉터리가 없다면, `make:mail` Artisan 명령어로 첫 번째 Mailable 클래스를 만들 때 자동으로 생성됩니다:

    php artisan make:mail OrderShipped

<a name="writing-mailables"></a>
## Mailable 클래스 작성

Mailable 클래스를 생성했다면 파일을 열고 내용을 살펴봅니다. 모든 설정은 `build` 메서드에서 합니다. 이 메서드 안에서 `from`, `subject`, `view`, `attach` 등의 메서드를 호출하여 이메일의 표현 및 전송 방식을 설정할 수 있습니다.

> {tip} Mailable의 `build` 메서드에서 의존성 타입힌트가 가능합니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 의존성을 주입합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정

<a name="using-the-from-method"></a>
#### `from` 메서드 사용하기

먼저 이메일의 발신자를 설정하는 방법입니다. 즉, 이메일이 누구로부터 오는지 지정할 수 있습니다. 두 가지 방법이 있는데, 먼저 Mailable 클래스의 `build` 메서드에서 `from` 메서드를 사용할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->from('example@example.com', 'Example')
                    ->view('emails.orders.shipped');
    }

<a name="using-a-global-from-address"></a>
#### 전역 `from` 주소 사용하기

애플리케이션 전체에서 동일한 "from" 주소를 사용하는 경우라면, 각 Mailable 클래스에서 매번 `from` 메서드를 호출하는 것이 번거로울 수 있습니다. 이 경우, `config/mail.php` 파일에서 전역 "from" 주소를 설정할 수 있습니다. 클래스 내에서 별도 지정이 없으면 이 주소가 사용됩니다:

    'from' => ['address' => 'example@example.com', 'name' => 'App Name'],

또한, 전역 "reply_to" 주소도 아래처럼 정의할 수 있습니다:

    'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],

<a name="configuring-the-view"></a>
### 뷰(View) 설정

Mailable 클래스의 `build` 메서드 안에서 `view` 메서드를 사용해 이메일 렌더링에 사용할 템플릿을 지정할 수 있습니다. 각 메일은 보통 [Blade 템플릿](/docs/{{version}}/blade)을 이용하므로, Blade 템플릿 엔진의 모든 기능을 활용할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped');
    }

> {tip} `resources/views/emails` 디렉터리를 만들어 모든 이메일 템플릿을 보관하는 것을 추천하지만, `resources/views` 내라면 어디든 자유롭게 배치할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하려면 `text` 메서드를 사용할 수 있습니다. `view` 메서드와 마찬가지로, `text` 메서드는 템플릿 이름을 받아 이메일 본문을 렌더링합니다. HTML/텍스트 버전을 모두 정의할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped')
                    ->text('emails.orders.shipped_plain');
    }

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 속성으로 전달

대개 이메일 렌더링에 사용할 데이터를 뷰로 전달하고 싶을 것입니다. 이 때 데이터 전달 방식은 두 가지가 있습니다. 첫째, Mailable 클래스에 public 속성으로 데이터를 넣으면 해당 속성이 자동으로 뷰에 노출됩니다. 예를 들어 생성자에서 데이터를 받아 public 속성에 넣으면:

    <?php

    namespace App\Mail;

    use App\Models\Order;
    use Illuminate\Bus\Queueable;
    use Illuminate\Mail\Mailable;
    use Illuminate\Queue\SerializesModels;

    class OrderShipped extends Mailable
    {
        use Queueable, SerializesModels;

        /**
         * 주문 인스턴스
         *
         * @var \App\Models\Order
         */
        public $order;

        /**
         * 메시지 인스턴스 생성
         *
         * @param  \App\Models\Order  $order
         * @return void
         */
        public function __construct(Order $order)
        {
            $this->order = $order;
        }

        /**
         * 메시지 생성
         *
         * @return $this
         */
        public function build()
        {
            return $this->view('emails.orders.shipped');
        }
    }

이렇게 데이터가 public 속성으로 할당되면 뷰에서는 아래처럼 접근할 수 있습니다:

    <div>
        Price: {{ $order->price }}
    </div>

<a name="via-the-with-method"></a>
#### `with` 메서드로 전달

이메일 데이터 포맷을 템플릿에 보내기 전에 커스터마이즈하고 싶다면, `with` 메서드를 사용해 데이터를 수동으로 뷰로 전달할 수 있습니다. 이 경우 보통 생성자에서 데이터를 받아 클래스의 protected나 private 속성에 넣고, `with` 메서드를 통해 배열로 전달합니다:

    <?php

    namespace App\Mail;

    use App\Models\Order;
    use Illuminate\Bus\Queueable;
    use Illuminate\Mail\Mailable;
    use Illuminate\Queue\SerializesModels;

    class OrderShipped extends Mailable
    {
        use Queueable, SerializesModels;

        /**
         * 주문 인스턴스
         *
         * @var \App\Models\Order
         */
        protected $order;

        /**
         * 메시지 인스턴스 생성
         *
         * @param  \App\Models\Order  $order
         * @return void
         */
        public function __construct(Order $order)
        {
            $this->order = $order;
        }

        /**
         * 메시지 생성
         *
         * @return $this
         */
        public function build()
        {
            return $this->view('emails.orders.shipped')
                        ->with([
                            'orderName' => $this->order->name,
                            'orderPrice' => $this->order->price,
                        ]);
        }
    }

이렇게 데이터를 `with` 메서드로 전달하면 뷰에서는 아래처럼 사용할 수 있습니다:

    <div>
        Price: {{ $orderPrice }}
    </div>

<a name="attachments"></a>
### 첨부파일

이메일에 파일을 첨부하려면 Mailable 클래스의 `build` 메서드에서 `attach` 메서드를 사용하세요. 첫 번째 인수로 파일의 전체 경로를 받습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped')
                    ->attach('/path/to/file');
    }

파일 첨부 시 표시 이름이나 MIME 타입을 지정하려면 두 번째 인수로 배열을 넘깁니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped')
                    ->attach('/path/to/file', [
                        'as' => 'name.pdf',
                        'mime' => 'application/pdf',
                    ]);
    }

<a name="attaching-files-from-disk"></a>
#### 파일 시스템 디스크에서 첨부

파일이 [파일 시스템 디스크](/docs/{{version}}/filesystem)에 저장되어 있다면, `attachFromStorage`를 사용해 이메일에 첨부할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
       return $this->view('emails.orders.shipped')
                   ->attachFromStorage('/path/to/file');
    }

필요하다면 두 번째, 세 번째 인수로 첨부파일 이름과 옵션을 지정할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
       return $this->view('emails.orders.shipped')
                   ->attachFromStorage('/path/to/file', 'name.pdf', [
                       'mime' => 'application/pdf'
                   ]);
    }

기본 디스크가 아니라 다른 디스크를 지정하려면 `attachFromStorageDisk` 메서드를 사용하세요:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
       return $this->view('emails.orders.shipped')
                   ->attachFromStorageDisk('s3', '/path/to/file');
    }

<a name="raw-data-attachments"></a>
#### Raw 데이터 첨부

`attachData` 메서드를 사용하면 바이트 데이터 문자열을 직접 첨부할 수 있습니다. 예를 들어, 메모리상에서 PDF를 생성하여 바로 첨부하고 싶을 때 유용합니다. 첫번째 인수는 raw 데이터, 두번째는 첨부될 파일명, 세번째는 옵션 배열입니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped')
                    ->attachData($this->pdf, 'name.pdf', [
                        'mime' => 'application/pdf',
                    ]);
    }

<a name="inline-attachments"></a>
### 인라인 첨부파일

이메일에 인라인 이미지를 포함시키는 일은 일반적으로 번거롭지만, Laravel은 편리한 방법을 제공합니다. 이메일 템플릿의 `$message` 변수에서 `embed` 메서드를 사용하면 인라인 이미지를 쉽게 넣을 수 있습니다. Laravel은 모든 이메일 템플릿에 `$message` 변수를 자동으로 제공합니다:

    <body>
        Here is an image:

        <img src="{{ $message->embed($pathToImage) }}">
    </body>

> {note} 평문(plain-text) 메시지 템플릿에서는 `$message` 변수를 사용할 수 없으며, 인라인 첨부파일도 사용할 수 없습니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터 인라인 첨부

이미지의 raw 데이터 문자열이 있다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이 때, 이미지에 부여할 파일명을 지정해야 합니다:

    <body>
        Here is an image from raw data:

        <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
    </body>

<a name="customizing-the-swiftmailer-message"></a>
### SwiftMailer 메시지 커스터마이즈

`Mailable` 기본 클래스의 `withSwiftMessage` 메서드를 사용하면, 이메일 전송 전에 SwiftMailer 메시지 인스턴스를 커스터마이징하는 클로저를 등록할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        $this->view('emails.orders.shipped');

        $this->withSwiftMessage(function ($message) {
            $message->getHeaders()->addTextHeader(
                'Custom-Header', 'Header Value'
            );
        });

        return $this;
    }

<a name="markdown-mailables"></a>
## 마크다운 Mailable

마크다운 Mailable 메시지를 사용하면 [메일 알림(Notifications)](/docs/{{version}}/notifications#mail-notifications)에 포함된 미리 만들어진 템플릿과 컴포넌트를 활용할 수 있습니다. 마크다운으로 작성하므로 Laravel이 아름답고 반응형인 HTML 템플릿을 자동으로 생성하며, 동시에 평문 버전도 만들어줍니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 Mailable 생성

마크다운 템플릿이 포함된 Mailable을 만들려면 `make:mail` Artisan 명령어의 `--markdown` 옵션을 사용하세요:

    php artisan make:mail OrderShipped --markdown=emails.orders.shipped

Mailable의 `build` 메서드에서 뷰(View) 대신 `markdown` 메서드를 사용하여 마크다운 템플릿과 전달할 데이터를 지정할 수 있습니다:

    /**
     * 메시지 생성
     *
     * @return $this
     */
    public function build()
    {
        return $this->from('example@example.com')
                    ->markdown('emails.orders.shipped', [
                        'url' => $this->orderUrl,
                    ]);
    }

<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성

마크다운 Mailable은 Blade 컴포넌트와 마크다운 구문을 조합하므로, 미리 만들어진 Laravel의 이메일 UI 컴포넌트를 활용하면서 메일 메시지를 쉽게 구성할 수 있습니다:

    @component('mail::message')
    # Order Shipped

    Your order has been shipped!

    @component('mail::button', ['url' => $url])
    View Order
    @endcomponent

    Thanks,<br>
    {{ config('app.name') }}
    @endcomponent

> {tip} 마크다운 이메일을 작성할 때는 들여쓰기를 과하게 하지 마세요. 표준 마크다운 규칙에 따라, 들여쓰기가 과하면 코드 블록으로 인식됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼을 생성합니다. 인수로 `url`(필수)과 `color`(옵션)를 받으며, 지원 색상은 `primary`, `success`, `error` 입니다. 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

    @component('mail::button', ['url' => $url, 'color' => 'success'])
    View Order
    @endcomponent

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 메시지의 다른 부분과 약간 다른 배경색으로 블록을 감싸 강조합니다:

    @component('mail::panel')
    This is the panel content.
    @endcomponent

<a name="table-component"></a>
#### 표 컴포넌트

표 컴포넌트는 마크다운 표를 HTML 테이블로 변환해줍니다. 마크다운 표 형식이 그대로 사용됩니다:

    @component('mail::table')
    | Laravel       | Table         | Example  |
    | ------------- |:-------------:| --------:|
    | Col 2 is      | Centered      | $10      |
    | Col 3 is      | Right-Aligned | $20      |
    @endcomponent

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈

모든 마크다운 메일 컴포넌트를 애플리케이션에 내보내(customize) 수 있습니다. 내보내려면 `vendor:publish` Artisan 명령어로 `laravel-mail` 태그를 배포하세요:

    php artisan vendor:publish --tag=laravel-mail

이 명령을 실행하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 저장됩니다. `mail` 디렉터리에는 `html`과 `text` 디렉터리가 있으며, 각 컴포넌트의 HTML/텍스트 표현이 들어 있습니다. 원하는 대로 수정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보낸 후에는, `resources/views/vendor/mail/html/themes` 내의 `default.css` 파일에서 원하는 대로 CSS를 수정할 수 있습니다. 이때 스타일은 자동으로 인라인 CSS로 변환되어 적용됩니다.

Laravel 마크다운 컴포넌트용 새로운 테마를 만들려면 `html/themes` 디렉터리에 CSS 파일을 놓으세요. 파일명을 저장한 뒤 `config/mail.php`의 `theme` 옵션을 해당 테마명으로 업데이트하세요.

개별 Mailable 클래스에서만 다른 테마를 적용하려면 해당 클래스의 `$theme` 속성을 테마명으로 지정하면 됩니다.

<a name="sending-mail"></a>
## 메일 전송

메일 전송 시 [Mail 파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용합니다. `to`에는 이메일 주소, 사용자 인스턴스, 혹은 사용자 컬렉션을 넘길 수 있습니다. 오브젝트(혹은 컬렉션)를 넘기면, 이메일과 이름 속성이 자동으로 메일의 수신자로 사용됩니다. 이후 Mailable 클래스의 인스턴스를 `send` 메서드에 전달합니다:

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
         * Ship the given order.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function store(Request $request)
        {
            $order = Order::findOrFail($request->order_id);

            // Ship the order...

            Mail::to($request->user())->send(new OrderShipped($order));
        }
    }

수신자("to")만 지정할 필요는 없습니다. "to", "cc", "bcc" 모두 체이닝 메서드로 설정 가능합니다:

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->send(new OrderShipped($order));

<a name="looping-over-recipients"></a>
#### 수신자 반복(loop) 처리

배열 혹은 여러 이메일 주소로 메일을 개별 발송해야 할 때가 있습니다. 주의할 점은, `to` 메서드는 수신자 리스트에 계속 추가하므로 반복문에서 매번 새로운 Mailable 인스턴스를 생성해야 한다는 점입니다:

    foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
        Mail::to($recipient)->send(new OrderShipped($order));
    }

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러로 메일 보내기

기본적으로 Laravel은 `mail` 설정 파일의 `default` 메일러를 사용합니다. 하지만 `mailer` 메서드로 특정 메일러를 지정해 보낼 수 있습니다:

    Mail::mailer('postmark')
            ->to($request->user())
            ->send(new OrderShipped($order));

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일을 즉시 발송하면 애플리케이션 반응 속도가 저하될 수 있으므로, 많은 개발자들이 이메일을 백그라운드 큐로 보냅니다. Laravel의 [통합 큐 API](/docs/{{version}}/queues)를 사용하여 쉽게 처리할 수 있습니다. `queue` 메서드를 사용하세요:

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue(new OrderShipped($order));

이 메서드는 메일 발송 작업을 큐에 자동으로 넣어 뒤에서 실행합니다. 이 기능을 사용하려면 [큐를 설정](/docs/{{version}}/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연(delayed) 전송

큐에 쌓인 이메일을 일정 시간 뒤에 전송하고 싶다면 `later` 메서드를 사용하세요. 첫번째 인수로 발송 시점을 나타내는 `DateTime` 객체가 필요합니다:

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->later(now()->addMinutes(10), new OrderShipped($order));

<a name="pushing-to-specific-queues"></a>
#### 특정 큐/커넥션 지정

`make:mail` 명령어로 생성된 모든 Mailable 클래스는 `Illuminate\Bus\Queueable` 트레잇을 포함합니다. 따라서 Mailable 인스턴스에서 `onQueue`, `onConnection` 메서드를 호출해 큐명과 커넥션명을 지명할 수 있습니다:

    $message = (new OrderShipped($order))
                    ->onConnection('sqs')
                    ->onQueue('emails');

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue($message);

<a name="queueing-by-default"></a>
#### 기본적으로 큐 처리

항상 큐에 쌓이도록 하고 싶은 Mailable 클래스가 있다면, 클래스에 `ShouldQueue` 계약(Contract)를 구현하세요. 이제 `send` 메서드를 호출해도 큐에 들어갑니다:

    use Illuminate\Contracts\Queue\ShouldQueue;

    class OrderShipped extends Mailable implements ShouldQueue
    {
        //
    }

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 Mailable & DB 트랜잭션

큐에 쌓인 Mailable이 DB 트랜잭션 내에서 디스패치되면, 트랜잭션 커밋 전에 큐가 소비될 가능성이 있습니다. 이 경우, 트랜잭션 도중 변경/생성한 모델 및 레코드가 DB에 반영되지 않았을 수 있습니다. Mailable이 해당 모델에 의존한다면 예상치 못한 에러가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 옵션이 `false`라면, 메일을 보낼 때 `afterCommit` 메서드를 호출해 모든 열린 트랜잭션이 커밋된 직후 처리하도록 만들 수 있습니다:

    Mail::to($request->user())->send(
        (new OrderShipped($order))->afterCommit()
    );

또는 생성자에서 `afterCommit`을 호출할 수도 있습니다:

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
         * 메시지 인스턴스 생성
         *
         * @return void
         */
        public function __construct()
        {
            $this->afterCommit();
        }
    }

> {tip} 이 이슈에 대한 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## Mailable 렌더링

간혹 이메일을 발송하지 않고, Mailable의 HTML만 얻고 싶을 때가 있습니다. 이럴 때 Mailable 객체의 `render` 메서드를 호출하면 HTML 콘텐츠가 문자열로 반환됩니다:

    use App\Mail\InvoicePaid;
    use App\Models\Invoice;

    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))->render();

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 Mailable 미리보기

Mailable 템플릿을 디자인할 때는 일반 Blade 템플릿처럼 브라우저에서 바로 렌더링 결과를 확인하면 편리합니다. Laravel에서 라우트 클로저나 컨트롤러에서 Mailable을 바로 반환하면, 브라우저에 렌더링된 HTML이 표시되어 전송 없이 빠르게 미리볼 수 있습니다:

    Route::get('/mailable', function () {
        $invoice = App\Models\Invoice::find(1);

        return new App\Mail\InvoicePaid($invoice);
    });

> {note} [인라인 첨부파일](#inline-attachments)은 브라우저에서 Mailable 미리보기 시 렌더링되지 않습니다. 이 경우 [MailHog](https://github.com/mailhog/MailHog), [HELO](https://usehelo.com) 같은 이메일 테스트 앱으로 전송하여 미리보기를 하세요.

<a name="localizing-mailables"></a>
## Mailable 현지화

Laravel은 요청의 현재 로케일이 아닌 다른 로케일로 Mailable을 전송할 수 있으며, 큐에 쌓일 경우에도 해당 로케일이 유지됩니다.

이를 위해 `Mail` 파사드의 `locale` 메서드로 원하는 언어를 설정할 수 있습니다. Mailable 템플릿이 렌더링되는 동안 일시적으로 로케일이 변경되고, 완료 후 원래 로케일로 복구됩니다:

    Mail::to($request->user())->locale('es')->send(
        new OrderShipped($order)
    );

<a name="user-preferred-locales"></a>
### 사용자 선호 언어

애플리케이션이 각 사용자의 선호 언어를 저장한다면, 모델에 `HasLocalePreference` 계약(Contract)를 구현해둠으로써 자동으로 해당 로케일로 메일을 보낼 수 있습니다:

    use Illuminate\Contracts\Translation\HasLocalePreference;

    class User extends Model implements HasLocalePreference
    {
        /**
         * 유저의 선호 로케일 반환
         *
         * @return string
         */
        public function preferredLocale()
        {
            return $this->locale;
        }
    }

이 인터페이스를 구현했다면, 메일 전송 시 자동으로 선호 로케일이 사용되므로, 별도로 `locale` 메서드를 호출할 필요가 없습니다:

    Mail::to($request->user())->send(new OrderShipped($order));

<a name="testing-mailables"></a>
## Mailable 테스트

Laravel은 Mailable에 기대하는 콘텐츠가 포함되어 있는지 손쉽게 테스트할 수 있는 몇 가지 메서드를 제공합니다: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInText`, `assertDontSeeInText`.

"HTML" 어서션은 HTML 버전에 문자열이 포함되어 있는지, "text" 어서션은 일반 텍스트 버전에 포함되어 있는지 검증합니다:

    use App\Mail\InvoicePaid;
    use App\Models\User;

    public function test_mailable_content()
    {
        $user = User::factory()->create();

        $mailable = new InvoicePaid($user);

        $mailable->assertSeeInHtml($user->email);
        $mailable->assertSeeInHtml('Invoice Paid');

        $mailable->assertSeeInText($user->email);
        $mailable->assertSeeInText('Invoice Paid');
    }

<a name="testing-mailable-sending"></a>
#### Mailable 전송 테스트

Mailable 콘텐츠 테스트와 Mailable이 특정 사용자에게 "전송"된 것을 어서션하는 테스트는 별도로 분리하는 것을 권장합니다. Mailable이 실제로 전송되었는지의 테스트 방법은 [Mail fake](/docs/{{version}}/mocking#mail-fake) 문서를 참고하세요.

<a name="mail-and-local-development"></a>
## 메일 & 로컬 개발

이메일을 실제로 라이브 계정으로 보내지 않고 개발하고 싶을 때가 많습니다. Laravel은 로컬 개발 환경에서 실제 이메일 발송을 "비활성화"하는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

`log` 메일 드라이버는 메일을 실제로 발송하지 않고 모든 이메일 메시지를 로그 파일에 기록합니다. 일반적으로 로컬 개발 환경에서만 이 드라이버를 사용합니다. 환경별 설정 정보는 [환경설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / MailHog

또 다른 방법으로, [HELO](https://usehelo.com) 또는 [Mailtrap](https://mailtrap.io)과 `smtp` 드라이버를 함께 사용하면 이메일을 "더미" 사서함으로 보내 실제 이메일 클라이언트에서 확인할 수 있습니다. 이 방식은 Mailtrap의 메시지 뷰어에서 최종 메일을 실제로 검사할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/{{version}}/sail)을 사용할 경우 [MailHog](https://github.com/mailhog/MailHog)로도 미리보기가 가능합니다. Sail 실행 중에는 `http://localhost:8025`에서 MailHog 인터페이스에 접근하세요.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드로 전역 "to" 주소를 지정할 수 있습니다. 일반적으로 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

    use Illuminate\Support\Facades\Mail;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        if ($this->app->environment('local')) {
            Mail::alwaysTo('taylor@example.com');
        }
    }

<a name="events"></a>
## 이벤트

Laravel은 메일 발송 과정에서 두 가지 이벤트를 발생시킵니다. `MessageSending` 이벤트는 발송 전에, `MessageSent` 이벤트는 발송 후에 발생합니다.
이 이벤트들은 메일이 실제로 *보내질 때* 발생하며, 큐에 쌓일 때는 발생하지 않습니다. 이 이벤트에 대한 리스너는 `App\Providers\EventServiceProvider`에서 등록합니다:

    /**
     * 애플리케이션의 이벤트 리스너 매핑 배열
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Mail\Events\MessageSending' => [
            'App\Listeners\LogSendingMessage',
        ],
        'Illuminate\Mail\Events\MessageSent' => [
            'App\Listeners\LogSentMessage',
        ],
    ];