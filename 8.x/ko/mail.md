# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 조건](#driver-prerequisites)
    - [페일오버 설정](#failover-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [발신자 설정하기](#configuring-the-sender)
    - [뷰 설정하기](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부파일](#attachments)
    - [인라인 첨부파일](#inline-attachments)
    - [SwiftMailer 메시지 커스터마이징](#customizing-the-swiftmailer-message)
- [마크다운 메일러블](#markdown-mailables)
    - [마크다운 메일러블 생성하기](#generating-markdown-mailables)
    - [마크다운 메시지 작성하기](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 보내기](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 현지화](#localizing-mailables)
- [메일러블 테스트](#testing-mailables)
- [메일 & 로컬 개발](#mail-and-local-development)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [SwiftMailer](https://swiftmailer.symfony.com/) 라이브러리를 기반으로 하는 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 SwiftMailer는 SMTP, Mailgun, Postmark, Amazon SES, 그리고 `sendmail`을 통한 이메일 전송용 드라이버를 제공하여, 로컬 또는 클라우드 기반 서비스를 통해 빠르게 메일 전송을 시작할 수 있도록 돕습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일 내에 구성된 각 메일러는 고유한 설정과 별도의 "transport"를 가질 수 있어, 애플리케이션에서 특정 이메일 메시지에 대해 서로 다른 이메일 서비스를 사용할 수 있습니다. 예를 들어, 애플리케이션은 트랜잭션 이메일에는 Postmark를, 대량 이메일 전송에는 Amazon SES를 사용할 수 있습니다.

`mail` 설정 파일 내에서는 `mailers` 배열을 찾을 수 있습니다. 이 배열에는 Laravel에서 지원하는 주요 메일 드라이버/전송 수단 별 샘플 설정이 포함되어 있습니다. 또한, `default` 설정 값은 애플리케이션이 메일을 보낼 때 기본으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 수단 사전 조건 (Driver / Transport Prerequisites)

Mailgun, Postmark와 같은 API 기반 드라이버는 SMTP 서버를 통한 전송보다 보통 더 간단하고 빠릅니다. 가능하면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다. 모든 API 기반 드라이버는 Composer 패키지 관리자를 통해 설치 가능한 Guzzle HTTP 라이브러리를 필요로 합니다:

```
composer require guzzlehttp/guzzle
```

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 먼저 Guzzle HTTP 라이브러리를 설치하세요. 그런 다음 `config/mail.php` 설정 파일에서 `default` 옵션을 `mailgun`으로 설정합니다. 다음으로 `config/services.php` 파일에 다음 설정이 포함되어 있는지 확인하세요:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
],
```

미국 [Mailgun 지역](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용하지 않는 경우, `services` 설정 파일에 해당 지역의 엔드포인트도 정의할 수 있습니다:

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
],
```

<a name="postmark-driver"></a>
#### Postmark 드라이버

Postmark 드라이버를 사용하려면 우선 Composer로 Postmark의 SwiftMailer transport를 설치합니다:

```
composer require wildbit/swiftmailer-postmark
```

그 다음 Guzzle HTTP 라이브러리를 설치하고, `config/mail.php` 설정 파일 내 `default` 옵션을 `postmark`로 설정하세요. 마지막으로 `config/services.php` 파일 내에 다음 설정이 포함되어 있는지 확인합니다:

```
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

특정 메일러가 사용할 Postmark 메시지 스트림을 지정하고 싶다면, 애플리케이션 `config/mail.php` 파일 내 메일러 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다:

```
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
],
```

이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark 메일러를 설정할 수 있습니다.

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer 패키지 관리자를 통해 설치할 수 있습니다:

```bash
composer require aws/aws-sdk-php
```

그런 다음 `config/mail.php` 설정 파일 내 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 다음 설정을 포함해야 합니다:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)에 세션 토큰을 사용하려면, SES 구성에 `token` 키를 추가하세요:

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

추가적으로, Laravel이 이메일을 전송할 때 AWS SDK `SendRawEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-email-2010-12-01.html#sendrawemail)을 정의하고자 한다면, `ses` 설정 내에 `options` 배열을 만들 수 있습니다:

```
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
```

<a name="failover-configuration"></a>
### 페일오버 설정 (Failover Configuration)

가끔 외부 메일 전송 서비스가 다운될 수 있습니다. 이럴 때 기본 전송 드라이버가 작동하지 않으면, 백업용 메일 전송 설정을 미리 정의해두는 것이 유용합니다.

이를 위해, 애플리케이션의 `mail` 설정 파일에 `failover` 전송 수단을 사용하는 메일러를 정의하세요. 이 `failover` 메일러의 설정 배열에는 전송 드라이버 우선순위를 가진 `mailers` 배열이 포함됩니다:

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

이후 `failover` 메일러를 기본 메일러로 지정하려면, 애플리케이션 `mail` 설정 내 `default` 설정 키에 해당 메일러 이름을 적절히 설정합니다:

```
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="generating-mailables"></a>
## 메일러블 생성하기 (Generating Mailables)

Laravel 애플리케이션에서 전송하는 이메일 종류별로 "메일러블" 클래스가 있습니다. 메일러블 클래스는 `app/Mail` 디렉터리에 저장됩니다. 만약 `Mail` 디렉터리가 없다면, `make:mail` Artisan 명령어로 첫 메일러블 클래스를 만들 때 자동으로 생성됩니다:

```
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기 (Writing Mailables)

메일러블 클래스를 생성했다면, 내부 내용을 열어보세요. 모든 메일러블 설정은 `build` 메서드에서 이루어집니다. 이 안에서 `from`, `subject`, `view`, `attach` 같은 메서드를 호출해 이메일의 발신자, 제목, 뷰, 첨부파일 등을 설정할 수 있습니다.

> [!TIP]
> `build` 메서드에서 의존성 주입을 타입힌트로 받을 수 있습니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 주입해줍니다.

<a name="configuring-the-sender"></a>
### 발신자 설정하기 (Configuring The Sender)

<a name="using-the-from-method"></a>
#### `from` 메서드 사용하기

이메일 발신자를 설정하는 방법부터 살펴보겠습니다. 즉, 이메일이 누구로부터 발신되는지 지정하는 것입니다. 발신자 설정 방법은 두 가지가 있습니다. 우선, 메일러블 클래스의 `build` 메서드 내에서 `from` 메서드를 사용할 수 있습니다:

```
/**
 * 메시지를 구성합니다.
 *
 * @return $this
 */
public function build()
{
    return $this->from('example@example.com', 'Example')
                ->view('emails.orders.shipped');
}
```

<a name="using-a-global-from-address"></a>
#### 전역 `from` 주소 사용하기

만약 애플리케이션에서 모든 이메일에 동일한 발신자 주소를 사용한다면, 매 메일러블 클래스마다 `from` 메서드를 호출하는 것은 번거로울 수 있습니다. 대신, `config/mail.php` 설정에 전역 `from` 주소를 지정할 수 있습니다. 이 설정은 메일러블에서 별도로 `from`이 지정되지 않을 때 사용됩니다:

```
'from' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

또한, `reply_to`의 전역 주소도 `config/mail.php`에서 지정할 수 있습니다:

```
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
### 뷰 설정하기 (Configuring The View)

메일러블의 `build` 메서드 내에서 `view` 메서드를 호출해 이메일 내용을 렌더링할 템플릿을 지정할 수 있습니다. 각 이메일은 보통 [Blade 템플릿](/docs/{{version}}/blade)을 사용해 작성하며, Blade 템플릿 엔진의 모든 기능과 편리함을 활용해 이메일 HTML을 구성할 수 있습니다:

```
/**
 * 메시지를 구성합니다.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped');
}
```

> [!TIP]
> 모든 이메일 템플릿을 저장할 `resources/views/emails` 디렉터리를 만들어도 좋지만, 원한다면 `resources/views` 내 어디든 자유롭게 배치할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일 작성

이메일의 일반 텍스트 버전을 따로 정의하고 싶다면 `text` 메서드를 사용하세요. `text` 메서드는 메시지 내용을 렌더링할 템플릿 이름을 받습니다. HTML과 일반 텍스트 버전 모두를 정의할 수 있습니다:

```
/**
 * 메시지를 구성합니다.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped')
                ->text('emails.orders.shipped_plain');
}
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성을 통한 전달

일반적으로 뷰에서 사용할 데이터를 메일러블에 전달해야 합니다. 데이터를 뷰에서 사용할 수 있도록 하는 방법은 두 가지입니다. 첫 번째는 메일러블 클래스에 정의한 `public` 속성입니다. 보통 생성자에서 전달받은 데이터를 `public` 속성에 할당하면, 뷰에서 자동으로 이 데이터에 접근할 수 있습니다:

```php
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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    public $order;

    /**
     * 새 메시지 인스턴스 생성.
     *
     * @param  \App\Models\Order  $order
     * @return void
     */
    public function __construct(Order $order)
    {
        $this->order = $order;
    }

    /**
     * 메시지를 구성합니다.
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped');
    }
}
```

이렇게 public 속성으로 할당된 데이터는 자동으로 뷰에서 사용 가능하므로, Blade 템플릿에서 아래처럼 접근할 수 있습니다:

```
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-method"></a>
#### `with` 메서드를 통한 전달

이메일 데이터의 포맷을 변환하거나 가공해 뷰에 전달하고 싶다면 `with` 메서드를 활용할 수 있습니다. 보통 생성자에서 데이터를 받아 필드를 `protected` 또는 `private`으로 숨기고, `with` 메서드에 전달할 배열을 명시적으로 작성합니다:

```php
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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    protected $order;

    /**
     * 새 메시지 인스턴스 생성.
     *
     * @param  \App\Models\Order  $order
     * @return void
     */
    public function __construct(Order $order)
    {
        $this->order = $order;
    }

    /**
     * 메시지를 구성합니다.
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
```

이 후, 뷰 내에서는 다음처럼 접근 가능합니다:

```
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부파일 (Attachments)

메일러블의 `build` 메서드 안에서 `attach` 메서드를 사용해 이메일에 첨부파일을 추가할 수 있습니다. `attach`는 첫 번째 인수로 전체 파일 경로를 받습니다:

```
/**
 * 메시지를 구성합니다.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped')
                ->attach('/path/to/file');
}
```

첨부 시, 두 번째 인수로 배열을 주면 표시될 이름(`as`)이나 MIME 타입(`mime`)을 지정할 수도 있습니다:

```
/**
 * 메시지를 구성합니다.
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
```

<a name="attaching-files-from-disk"></a>
#### 스토리지 디스크에서 첨부하기

만약 [파일시스템 디스크](/docs/{{version}}/filesystem)에 저장된 파일을 첨부하려면 `attachFromStorage` 메서드를 사용하세요:

```
/**
 * 메시지를 구성합니다.
 *
 * @return $this
 */
public function build()
{
   return $this->view('emails.orders.shipped')
               ->attachFromStorage('/path/to/file');
}
```

파일명과 추가 옵션은 두 번째, 세 번째 인수로 넘길 수 있습니다:

```
/**
 * 메시지를 구성합니다.
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
```

기본 저장소 디스크 외 특정 디스크에서 파일을 첨부하고 싶으면 `attachFromStorageDisk` 메서드를 사용하세요:

```
/**
 * 메시지를 구성합니다.
 *
 * @return $this
 */
public function build()
{
   return $this->view('emails.orders.shipped')
               ->attachFromStorageDisk('s3', '/path/to/file');
}
```

<a name="raw-data-attachments"></a>
#### raw 데이터 첨부파일

문자열 바이트(raw data) 자체를 첨부파일로 이메일에 붙이고 싶다면 `attachData` 메서드를 사용할 수 있습니다. 예를 들어 메모리 상에서 생성한 PDF를 디스크에 쓰지 않고 첨부하고 싶을 때 유용합니다. 첫 번째 인자로 raw 데이터, 두 번째 인자로 파일 이름, 세 번째 인자로 옵션 배열을 받습니다:

```
/**
 * 메시지를 구성합니다.
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
```

<a name="inline-attachments"></a>
### 인라인 첨부파일 (Inline Attachments)

이메일에 이미지와 같은 인라인 첨부파일을 포함하는 것은 보통 번거롭습니다. 하지만 Laravel은 이를 간편하게 처리하는 방법을 제공합니다. 이메일 템플릿 내에서 `$message` 변수의 `embed` 메서드를 사용해 이미지를 삽입할 수 있습니다. `$message` 변수는 자동으로 모든 이메일 템플릿에서 사용할 수 있으므로 따로 전달할 필요가 없습니다:

```
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!NOTE]
> `$message` 변수는 일반 텍스트 이메일 템플릿에서는 사용 불가능합니다. 일반 텍스트 메시지는 인라인 첨부파일을 활용하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### raw 데이터 첨부파일 임베드

만약 원시 이미지 데이터를 이미 가지고 있다면 `$message` 변수의 `embedData` 메서드를 호출해 이메일에 임베드할 수 있습니다. 이때 임베드할 이미지 파일 이름도 함께 지정해줘야 합니다:

```
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="customizing-the-swiftmailer-message"></a>
### SwiftMailer 메시지 커스터마이징

`Mailable` 기본 클래스의 `withSwiftMessage` 메서드를 사용하면, 메시지를 전송하기 전에 SwiftMailer 메시지 인스턴스를 인수로 받는 클로저를 등록할 수 있습니다. 이 방법으로 전송 전에 메시지를 상세히 조작할 수 있습니다:

```
/**
 * 메시지를 구성합니다.
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
```

<a name="markdown-mailables"></a>
## 마크다운 메일러블 (Markdown Mailables)

마크다운 스타일 메일러블은 [메일 알림](/docs/{{version}}/notifications#mail-notifications)에서 제공하는 사전 구축된 템플릿과 컴포넌트를 활용할 수 있게 해줍니다. 메시지를 마크다운 문법으로 작성하면, Laravel이 아름답고 반응형인 HTML 템플릿을 렌더링하고 자동으로 일반 텍스트 버전도 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일러블 생성하기

마크다운 템플릿과 연동되는 메일러블을 만들려면, `make:mail` Artisan 명령어에 `--markdown` 옵션을 사용하세요:

```
php artisan make:mail OrderShipped --markdown=emails.orders.shipped
```

그리고 `build` 메서드에서 `view` 대신 `markdown` 메서드를 호출합니다. `markdown` 메서드는 마크다운 템플릿 이름과, 선택적으로 템플릿에 전달할 데이터를 받습니다:

```
/**
 * 메시지를 구성합니다.
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
```

<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성하기

마크다운 메일러블은 Blade 컴포넌트와 마크다운 문법을 혼합하여 사용할 수 있어, Laravel이 미리 만들어 둔 이메일 UI 컴포넌트를 편리하게 활용할 수 있습니다:

```
@component('mail::message')
# 주문이 발송되었습니다

Your order has been shipped!

@component('mail::button', ['url' => $url])
주문 보기
@endcomponent

감사합니다,<br>
{{ config('app.name') }}
@endcomponent
```

> [!TIP]
> 마크다운 이메일 작성 시 과도한 들여쓰기를 하지 마세요. 마크다운 파서는 들여쓰기된 내용을 코드 블록으로 해석할 수 있습니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

`button` 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적 `color` 인수를 받으며, `primary`, `success`, `error` 3가지 색상을 지원합니다. 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```
@component('mail::button', ['url' => $url, 'color' => 'success'])
주문 보기
@endcomponent
```

<a name="panel-component"></a>
#### 패널 컴포넌트

`panel` 컴포넌트는 메시지 본문과 약간 다른 배경색을 가진 패널로 텍스트 블록을 감싸 시선을 끌 수 있도록 합니다:

```
@component('mail::panel')
이것이 패널 내용입니다.
@endcomponent
```

<a name="table-component"></a>
#### 테이블 컴포넌트

`table` 컴포넌트는 마크다운 테이블을 HTML 테이블로 변환해줍니다. 기본 마크다운 테이블 정렬 문법에 따라 열 정렬이 지원됩니다:

```
@component('mail::table')
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
@endcomponent
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징

모든 마크다운 메일 컴포넌트를 내 애플리케이션으로 내보내어 직접 수정하려면 `vendor:publish` Artisan 명령어를 사용해 `laravel-mail` 태그를 퍼블리시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어는 `resources/views/vendor/mail` 디렉터리에 컴포넌트를 퍼블리시합니다. 이 안에는 `html`과 `text` 디렉터리가 각각 있으며, 각 디렉터리에 컴포넌트의 구현체가 담겨 있습니다. 필요에 따라 자유롭게 수정 가능합니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트를 퍼블리시한 후에는 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일이 생성됩니다. 이 파일을 수정하면, 마크다운 메일 HTML에서 인라인 스타일로 자동 변환되어 반영됩니다.

만약 완전히 새로운 테마를 만들고 싶으면, `html/themes` 디렉터리에 새 CSS 파일을 추가하고, `config/mail.php` 설정의 `theme` 옵션을 새 테마 이름으로 변경하세요.

특정 메일러블에서만 다른 테마를 적용하고 싶으면, 메일러블 클래스 내 `$theme` 속성에 사용하고자 하는 테마 이름을 설정하면 됩니다.

<a name="sending-mail"></a>
## 메일 보내기 (Sending Mail)

메일을 보내려면 `Mail` [파사드](/docs/{{version}}/facades)의 `to` 메서드를 사용하세요. `to`는 이메일 주소, 사용자 인스턴스, 혹은 사용자 컬렉션을 받을 수 있습니다. 객체나 컬렉션을 넘기면, 메일러가 자동으로 `email`과 `name` 속성을 사용해 수신자를 결정하니 이 속성들이 반드시 존재해야 합니다. 수신자를 지정한 후, `send` 메서드에 메일러블 인스턴스를 전달하면 됩니다:

```php
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

"to" 수신자뿐만 아니라 "cc", "bcc" 수신자도 메서드 체이닝으로 지정할 수 있습니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

수신자 배열을 순회하면서 메일을 보내야 할 때가 있습니다. 하지만 `to` 메서드는 수신자를 누적시키므로, 루프마다 이전 수신자에게도 중복 전송됩니다. 따라서 루프 내부에서 매번 새로운 메일러블 인스턴스를 생성해야 합니다:

```
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 지정해 메일 보내기

기본적으로 Laravel은 `mail` 설정에서 `default`로 지정한 메일러를 사용합니다. 하지만 `mailer` 메서드를 활용해 특정 메일러를 지정해 메일을 보낼 수 있습니다:

```
Mail::mailer('postmark')
        ->to($request->user())
        ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉하기

이메일 전송은 응답 속도에 영향을 줄 수 있으므로, 백그라운드에서 처리하도록 메시지를 큐에 넣는 것이 좋습니다. Laravel은 내장된 [통합 큐 API](/docs/{{version}}/queues)를 이용해 쉽게 구현할 수 있습니다. 수신자 지정 후, `queue` 메서드를 사용해 메시지를 큐에 넣으세요:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이 메서드는 메시지를 비동기로 전송할 수 있도록 자동으로 큐 작업을 생성해줍니다. 사용하려면 먼저 [큐 설정](/docs/{{version}}/queues)이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 큐 메시지 전송 지연하기

큐 처리된 이메일 전송을 일정 시간 뒤로 미루고 싶다면 `later` 메서드를 사용하세요. 첫 번째 인수로 `DateTime` 인스턴스를 받아 메시지 전송 시점을 결정합니다:

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐에 전송하기

`make:mail`로 생성된 메일러블은 기본적으로 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, `onQueue`와 `onConnection` 메서드를 호출해 큐 이름과 큐 연결을 지정할 수 있습니다:

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
#### 기본 큐잉 활성화하기

항상 큐잉을 적용하고 싶은 메일러블 클래스에는 `ShouldQueue` 계약을 구현하면 됩니다. 이렇게 하면 `send` 메서드를 호출해도 자동으로 큐잉 처리됩니다:

```
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    //
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 데이터베이스 트랜잭션과 큐잉된 메일러블

데이터베이스 트랜잭션 내에서 큐잉된 메일러블이 디스패치될 경우, 트랜잭션 커밋 전 큐에서 작업을 처리할 수 있습니다. 이 때 데이터가 아직 커밋되지 않아 모델 변경 내용이나 신규 데이터가 반영되지 않을 수 있습니다. 메일러블이 이런 모델에 의존하면 예상치 못한 오류가 발생할 수 있습니다.

만약 큐 연결 설정 `after_commit` 옵션이 `false`라면, 큐에 넣는 시점에 `afterCommit` 메서드를 호출해 트랜잭션 커밋 후에 디스패치되도록 지정할 수 있습니다:

```
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

혹은 메일러블 생성자에서 호출해도 됩니다:

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
     * 새 메시지 인스턴스 생성.
     *
     * @return void
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!TIP]
> 이와 관련해 자세한 내용은 [큐 작업과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="rendering-mailables"></a>
## 메일러블 렌더링 (Rendering Mailables)

메일러블을 전송하지 않고, HTML 내용을 미리 확인하고 싶을 때가 있습니다. 이럴 때는 메일러블의 `render` 메서드를 호출하면 렌더링된 HTML 문자열을 반환합니다:

```
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블 템플릿 디자인 시, 브라우저에서 바로 렌더링된 결과를 확인하면 매우 편리합니다. Laravel은 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 바로 반환할 수 있도록 지원합니다. 이 경우 메일러블이 렌더링되어 브라우저에서 표시됩니다:

```
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

> [!NOTE]
> [인라인 첨부파일](#inline-attachments)은 브라우저 미리보기에서 렌더링되지 않습니다. 이런 메일러블을 확인하려면 [MailHog](https://github.com/mailhog/MailHog) 또는 [HELO](https://usehelo.com) 같은 이메일 테스트 도구로 실제 발송 후 확인하세요.

<a name="localizing-mailables"></a>
## 메일러블 현지화 (Localizing Mailables)

Laravel에서는 요청의 현재 로케일과 다른 언어로 메일러블을 보낼 수 있으며, 큐잉 시에도 이 로케일 설정이 기억됩니다.

이를 위해 `Mail` 파사드에 `locale` 메서드가 제공되며, 이 메서드로 원하는 언어를 지정하면 메일러블 템플릿 렌더링 시 해당 로케일을 일시적으로 적용하고, 렌더링 완료 후에는 원래 로케일로 되돌립니다:

```
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
### 사용자 선호 로케일

종종 애플리케이션은 사용자마다 선호하는 로케일을 저장합니다. `HasLocalePreference` 계약을 모델에서 구현하면, Laravel은 해당 모델로 메일과 알림을 보낼 때 저장된 로케일을 자동으로 사용합니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * 사용자의 선호 로케일을 반환.
     *
     * @return string
     */
    public function preferredLocale()
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현하면, `locale` 메서드를 직접 호출하지 않아도 Laravel이 자동으로 적용합니다:

```
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 메일러블 테스트 (Testing Mailables)

Laravel은 메일러블의 예상 콘텐츠 포함 여부를 확인할 수 있는 여러 편리한 메서드를 제공합니다. 주요 메서드는 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInText`, `assertDontSeeInText` 입니다.

각 메서드는 "HTML" 버전 또는 "텍스트" 버전에 특정 문자열이 있는지 없는지를 검증합니다:

```
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
```

<a name="testing-mailable-sending"></a>
#### 메일러블 발송 테스트

메일러블 내용 테스트와 별도로, 특정 메일러블이 특정 사용자에게 발송되었는지 검증하는 테스트가 필요할 수 있습니다. 이 경우 [Mail fake](/docs/{{version}}/mocking#mail-fake) 문서를 참고해 모킹하는 방법을 배우세요.

<a name="mail-and-local-development"></a>
## 메일 & 로컬 개발 (Mail & Local Development)

메일 전송 기능 개발 시 실제 메일을 보내는 대신 전송을 "비활성화" 하거나 대체하는 방법들이 있습니다.

<a name="log-driver"></a>
#### 로그 드라이버

메일을 전송하는 대신, `log` 메일 드라이버는 모든 메일 메시지를 로그 파일에 기록합니다. 보통 로컬 개발 환경에서만 사용합니다. [환경별 설정](/docs/{{version}}/configuration#environment-configuration) 문서를 참조하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / MailHog

또는 [HELO](https://usehelo.com), [Mailtrap](https://mailtrap.io)와 같은 서비스를 `smtp` 드라이버와 함께 사용해, 실제 이메일 클라이언트가 아닌 "더미" 우편함으로 메일을 전송해 최종 이메일을 점검할 수 있습니다.

Laravel Sail 사용 시 [MailHog](https://github.com/mailhog/MailHog)로 메일을 미리 볼 수 있습니다. Sail이 실행 중이라면 `http://localhost:8025` 주소에서 MailHog 인터페이스에 접속하세요.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 설정하기

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드로 전역 "to" 주소를 지정할 수 있습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
## 이벤트 (Events)

Laravel은 메일 전송 과정에서 두 개의 이벤트를 발생시킵니다. 메일 전송 직전에 발생하는 `MessageSending` 이벤트와 전송 완료 후 발생하는 `MessageSent` 이벤트입니다. 이 이벤트들은 메일이 *전송*될 때 발생하며, 큐잉 시 발생하지 않습니다. 해당 이벤트에 대한 리스너를 `App\Providers\EventServiceProvider`에 등록할 수 있습니다:

```
/**
 * 애플리케이션 이벤트 리스너 매핑.
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
```