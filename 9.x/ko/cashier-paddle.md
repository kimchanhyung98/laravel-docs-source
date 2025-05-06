# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
    - [데이터베이스 마이그레이션](#database-migrations)
- [설정](#configuration)
    - [결제 가능(Billable) 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [핵심 개념](#core-concepts)
    - [Pay Link](#pay-links)
    - [인라인 결제(Checkout)](#inline-checkout)
    - [사용자 식별](#user-identification)
- [가격](#prices)
- [고객](#customers)
    - [고객 기본 값](#customer-defaults)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [요금제 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [구독 모디파이어(Modifier)](#subscription-modifiers)
    - [복수 구독](#multiple-subscriptions)
    - [구독 일시중지](#pausing-subscriptions)
    - [구독 취소](#cancelling-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [사전 결제 정보와 함께](#with-payment-method-up-front)
    - [사전 결제 정보 없이](#without-payment-method-up-front)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [간단한 청구](#simple-charge)
    - [상품 청구](#charging-products)
    - [주문 환불](#refunding-orders)
- [영수증](#receipts)
    - [이전 및 예정된 결제](#past-and-upcoming-payments)
- [실패한 결제 처리](#handling-failed-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)는 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 직관적이고 유연한 인터페이스를 제공합니다. 복잡한 구독 결제에 필요한 대부분의 반복 코드를 대신 처리해줍니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰, 구독 변경, 구독 "수량", 취소 유예 기간 등 다양한 기능을 제공합니다.

Cashier를 사용하면서 Paddle의 [사용자 가이드](https://developer.paddle.com/guides)와 [API 문서](https://developer.paddle.com/api-reference)도 함께 참고하시길 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용해 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

> **경고**  
> Cashier가 모든 Paddle 이벤트를 제대로 처리할 수 있도록 [Cashier 웹훅 핸들링을 반드시 설정](#handling-paddle-webhooks)하세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 또는 스테이징 개발 중에는 반드시 [Paddle 샌드박스 계정](https://developer.paddle.com/getting-started/sandbox)을 등록하세요. 이 계정은 실제 결제 없이 다양한 시나리오를 테스트할 수 있습니다. 결제 상황을 시뮬레이션할 때는 [Paddle의 테스트 카드 번호](https://developer.paddle.com/getting-started/sandbox#test-cards)를 사용하세요.

Paddle 샌드박스 환경을 사용하려면 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

개발이 모두 끝나면 [Paddle 벤더 계정](https://paddle.com)을 신청할 수 있습니다. 운영 환경에 배포하기 전에, Paddle은 반드시 해당 도메인을 승인해야 합니다.

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션

Cashier 서비스 프로바이더는 자체 마이그레이션 디렉토리를 등록합니다. 패키지를 설치한 후 반드시 데이터베이스 마이그레이션을 실행하세요. Cashier 마이그레이션은 새로운 `customers` 테이블, 모든 고객의 구독 정보를 저장하는 `subscriptions` 테이블, 그리고 모든 영수증 정보를 저장하는 `receipts` 테이블을 생성합니다:

```shell
php artisan migrate
```

Cashier에 기본 포함된 마이그레이션을 오버라이드하려면, `vendor:publish` Artisan 명령어를 사용해 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

혹시 Cashier의 마이그레이션을 전혀 실행하고 싶지 않다면, 제공된 `ignoreMigrations` 메서드를 사용할 수 있습니다. 일반적으로 `AppServiceProvider`의 `register` 메서드에서 호출하면 됩니다:

```php
use Laravel\Paddle\Cashier;

public function register()
{
    Cashier::ignoreMigrations();
}
```

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 결제 가능(Billable) 모델

Cashier를 사용하기 전에, 사용자 모델 정의에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 정보 갱신 등 자주 쓰이는 결제 관련 작업을 손쉽게 처리할 수 있게 도와줍니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

만약 사용자 외에 결제가 가능한 엔티티(예: 팀)를 쓴다면 해당 클래스에도 트레이트를 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키

다음으로, Paddle 키를 `.env` 파일에 설정해야 합니다. 이 키는 Paddle 콘솔에서 발급받을 수 있습니다:

```ini
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경변수는 [Paddle 샌드박스 환경](#paddle-sandbox)을 사용할 때 `true`로 두세요. 운영환경 및 라이브 벤더 계정 사용 시에는 `false`로 설정합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 자체 JavaScript 라이브러리를 사용하여 결제 위젯을 띄웁니다. `</head>` 태그 바로 전에 `@paddleJS` Blade 디렉티브를 넣어 JS 라이브러리를 로드하세요:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. `.env` 파일의 `CASHIER_CURRENCY` 환경변수로 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=EUR
```

통화 이외에도, 청구서 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> **경고**  
> `en` 이외의 로케일을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치 및 설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Cashier에서 내부적으로 사용되는 모델을 직접 확장할 수 있습니다:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Paddle\Cashier` 클래스에 해당 모델 사용을 명시하세요. 일반적으로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Cashier\Receipt;
use App\Models\Cashier\Subscription;

public function boot()
{
    Cashier::useReceiptModel(Receipt::class);
    Cashier::useSubscriptionModel(Subscription::class);
}
```

<a name="core-concepts"></a>
## 핵심 개념

<a name="pay-links"></a>
### Pay Link

Paddle은 구독 상태 변경을 위한 방대한 CRUD API가 없습니다. 따라서 대부분의 작업은 [결제 위젯](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout)을 통해 이루어집니다. 위젯을 띄우기 전에는 Cashier를 통해 "페이 링크(pay link)"를 만들어야 합니다. 이 링크는 어떤 결제 작업을 할 것인지 위젯에 알려줍니다:

```php
use App\Models\User;
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 34567)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

Cashier는 `paddle-button` [Blade 컴포넌트](/docs/{{version}}/blade#components)를 제공합니다. 이 컴포넌트에 페이 링크 URL을 prop으로 넘기면, 클릭 시 Paddle 위젯이 나타납니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 표준 Paddle 스타일을 적용하지만, `data-theme="none"` 속성을 추가하면 Paddle 스타일을 제거할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

Paddle 결제 위젯은 비동기적으로 동작합니다. 사용자가 위젯에서 구독을 생성하거나 변경하면, Paddle은 웹훅을 통해 애플리케이션에 알리므로 반드시 [웹훅을 제대로 설정](#handling-paddle-webhooks)해야 합니다.

페이 링크에 관한 자세한 정보는 [Paddle API 문서의 pay link 생성 부분](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)을 참고하십시오.

> **경고**  
> 구독 상태 변경 후, 해당 웹훅 도달까지는 일반적으로 지연이 거의 없지만, 사용자의 구독이 위젯 완료 직후 바로 반영되지 않을 수 있음을 염두에 두어야 합니다.

<a name="manually-rendering-pay-links"></a>
#### Pay Link 직접 렌더링

Blade 컴포넌트 대신 직접 링크를 사용할 수도 있습니다. 예제와 같이 URL을 생성한 후, HTML `<a>` 태그에 연결합니다:

```html
<a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
    Paddle Checkout
</a>
```

<a name="payments-requiring-additional-confirmation"></a>
#### 추가 결제 인증이 필요한 경우

간혹 결제의 추가 인증이 필요할 때가 있습니다. 이 경우 Paddle이 결제 확인 화면을 보여줍니다. 은행이나 카드에 따라 별도의 카드 인증, 소액 임시 청구, 별도 기기 인증 등 절차가 추가될 수 있습니다.

<a name="inline-checkout"></a>
### 인라인 결제(Checkout)

Paddle의 "오버레이" 스타일 결제 위젯 대신 페이지 내에 직접 위젯을 임베드할 수도 있습니다. 이 방식은 HTML 필드를 수정할 수는 없지만, 위젯을 앱 내부에 포함할 수 있는 장점이 있습니다.

Cashier는 인라인 체크아웃을 쉽게 구현할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. [페이 링크](#pay-links)를 생성하고 `override` 속성에 전달하세요:

```blade
<x-paddle-checkout :override="$payLink" class="w-full" />
```

인라인 체크아웃 컴포넌트의 높이를 조정하려면 `height` 속성을 전달하세요:

```blade
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
#### 페이 링크 없이 인라인 체크아웃 사용

페이 링크 대신 커스텀 옵션으로 위젯을 설정할 수도 있습니다:

```blade
@php
$options = [
    'product' => $productId,
    'title' => 'Product Title',
];
@endphp

<x-paddle-checkout :options="$options" class="w-full" />
```

자세한 옵션 정보는 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout)와 [파라미터 레퍼런스](https://developer.paddle.com/reference/paddle-js/parameters)를 참고하세요.

> **경고**  
> `passthrough` 옵션을 쓰려면 반드시 key/value 배열 형태로 값을 넘기세요. Cashier가 자동으로 JSON 문자열로 변환해줍니다. 단, `customer_id` passthrough 옵션은 Cashier 내부에서 사용하므로 사용을 피하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 직접 렌더링

Blade 컴포넌트 없이도 직접 페이 링크를 생성하고 Paddle.js를 통해 위젯을 초기화할 수 있습니다. 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하고 있지만, 원하는 프론트엔드 프레임워크로 변경 가능합니다:

```alpine
<div class="paddle-checkout" x-data="{}" x-init="
    Paddle.Checkout.open({
        override: {{ $payLink }},
        method: 'inline',
        frameTarget: 'paddle-checkout',
        frameInitialHeight: 366,
        frameStyle: 'width: 100%; background-color: transparent; border: none;'
    });
">
</div>
```

<a name="user-identification"></a>
### 사용자 식별

Stripe와 달리 Paddle의 사용자는 Paddle 전체에서 유일합니다(즉, 각 벤더별로 유일하지 않음). Paddle API에서는 이메일 등 사용자의 세부 정보를 갱신할 수 없습니다. 페이 링크 생성 시 `customer_email` 파라미터로 사용자를 식별합니다. 구독 생성 시, Paddle은 제공된 이메일로 기존 사용자를 식별하려 시도합니다.

이러한 특성 때문에 유의해야 할 점:
- **Cashier상 동일한 사용자라 해도 Paddle 내부 시스템에서는 서로 다른 유저로 연결될 수 있습니다.**
- 각 구독은 별도의 결제 수단/이메일을 갖고 있을 수 있습니다.

따라서 구독 정보 표시 시, 반드시 해당 구독에 연결된 이메일/결제 정보를 표시하세요. 이 때는 `Laravel\Paddle\Subscription` 모델의 다음 메서드를 사용할 수 있습니다:

```php
$subscription = $user->subscription('default');
$subscription->paddleEmail();
$subscription->paymentMethod();
$subscription->cardBrand();
$subscription->cardLastFour();
$subscription->cardExpirationDate();
```

Paddle API에서는 사용자의 이메일을 변경할 수 있는 방법이 없습니다. 사용자가 이메일을 변경하려면 Paddle 고객지원에 직접 문의해야 하며, 문의 시에는 구독의 `paddleEmail` 값을 정확히 제시해야 합니다.

<a name="prices"></a>
## 가격

Paddle은 각 통화(국가)별로 가격을 다르게 설정할 수 있습니다. Cashier Paddle의 `productPrices` 메서드는 상품 ID 배열을 입력받아 상품별 가격 정보를 조회할 수 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456]);
```

통화는 요청의 IP에 따라 자동으로 결정되며, `customer_country` 옵션으로 특정 국가를 지정할 수도 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);
```

조회된 가격 정보를 원하는 형태로 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

세금 제외 금액 및 세금만 별도 분리해 표시하려면:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

구독 상품의 경우 최초 결제와 반복 결제를 구분해서 보여줄 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

더 자세한 정보는 [Paddle 가격 API 문서](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)를 참고하세요.

<a name="prices-customers"></a>
#### 고객

이미 고객인 사용자를 위한 가격을 보여주고 싶다면, 해당 고객 인스턴스에서 직접 가격을 조회할 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->productPrices([123, 456]);
```

내부적으로 Cashier는 사용자의 [`paddleCountry` 메서드](#customer-defaults)를 통해 적합한 통화를 정합니다. 기본적으로 미국 거주자라면 USD, 벨기에 거주자라면 EUR로 표시됩니다. 해당 통화가 없으면 상품의 기본 통화가 적용됩니다. Paddle 콘솔에서 상품이나 구독 요금제별 가격을 자유롭게 커스터마이즈할 수 있습니다.

<a name="prices-coupons"></a>
#### 쿠폰

쿠폰 적용 후의 가격도 표시할 수 있습니다. `productPrices` 메서드에 쿠폰 코드를 콤마로 구분된 문자열로 전달하세요:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], [
    'coupons' => 'SUMMERSALE,20PERCENTOFF'
]);
```

쿠폰 적용가를 표시하려면 `price` 메서드를 사용하세요:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

쿠폰 할인이 적용되지 않은 원래 가격은 `listPrice` 메서드로 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> **경고**  
> 가격 API 이용 시, Paddle은 쿠폰을 일회성 제품에는 적용할 수 있으나 구독 플랜에는 적용할 수 없습니다.

<a name="customers"></a>
## 고객

<a name="customer-defaults"></a>
### 고객 기본 값

Cashier는 pay link 생성 시, 고객의 이메일, 국가, 우편번호 등 몇 가지 기본값을 미리 지정할 수 있게 해줍니다. 이로써 사용자가 위젯에서 즉시 결제 단계로 넘어갈 수 있습니다. 이러한 기본값은 billable 모델에서 다음과 같이 오버라이드합니다:

```php
/**
 * Paddle에 연동할 고객 이메일 주소 반환.
 */
public function paddleEmail()
{
    return $this->email;
}

/**
 * Paddle에 연동할 고객 국가 반환 (2자리 국가코드).
 * https://developer.paddle.com/reference/platform-parameters/supported-countries
 */
public function paddleCountry()
{
    //
}

/**
 * Paddle에 연동할 고객 우편번호 반환.
 * https://developer.paddle.com/reference/platform-parameters/supported-countries#countries-requiring-postcode
 */
public function paddlePostcode()
{
    //
}
```

이 기본값들은 페이 링크를 생성하는 Cashier의 모든 액션에 사용됩니다.

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

처음 구독을 만들려면, 보통 `App\Models\User` 인스턴스와 같은 billable 모델 인스턴스를 데이터베이스에서 가져오고 `newSubscription` 메서드를 사용해 구독 pay link를 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

`newSubscription`의 첫 번째 인수는 구독의 내부명(예시: `default`, `primary`)입니다. 이 이름은 사용자에게 노출되지 않고, 단 한 번만 정해진 후 변경 불가입니다. 두 번째 인수는 Paddle의 요금제 식별자입니다. `returnTo`는 결제 후 사용자가 이동할 URL을 받습니다.

`create` 메서드는 결제 버튼을 만들 때 쓸 수 있는 페이 링크를 만듭니다. 위에서는 Cashier의 `paddle-button` [Blade 컴포넌트](/docs/{{version}}/blade#components)를 사용해 결제 버튼을 만들 수 있습니다:

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

체크아웃이 완료되면 Paddle에서 `subscription_created` 웹훅이 전송되고, Cashier에서 구독을 세팅합니다. [웹훅 처리가 정상적으로 동작](#handling-paddle-webhooks)하는지 확인하세요.

<a name="additional-details"></a>
#### 추가 정보 지정

추가 고객 정보나 구독 정보를 지정하려면, `create` 메서드에 key/value 배열을 전달하세요. 사용 가능한 추가 필드는 [Paddle 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요:

```php
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->create([
        'vat_number' => $vatNumber,
    ]);
```

<a name="subscriptions-coupons"></a>
#### 쿠폰

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요:

```php
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withCoupon('code')
    ->create();
```

<a name="metadata"></a>
#### 메타데이터

`withMetadata` 메서드를 사용해 추가 메타데이터도 넘길 수 있습니다:

```php
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withMetadata(['key' => 'value'])
    ->create();
```

> **경고**  
> 메타데이터 키로 `subscription_name`은 사용할 수 없습니다. 이 키는 Cashier 내부에서 사용됩니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 구독 중인지 확인하려면 다양한 편의 메서드를 사용할 수 있습니다. 우선 `subscribed` 메서드는 사용자가(체험 기간을 포함하여) 활성 구독을 갖고 있으면 `true`를 반환합니다:

```php
if ($user->subscribed('default')) {
    //
}
```

`subscribed`는 [라우트 미들웨어](/docs/{{version}}/middleware)로 이용해 유료 구독 사용자인 경우에만 접근 가능한 페이지/컨트롤러를 만들 때에도 유용합니다:

```php
class EnsureUserIsSubscribed
{
    public function handle($request, Closure $next)
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 구독 미결제 사용자
            return redirect('billing');
        }

        return $next($request);
    }
}
```

사용자가 체험 기간에 속해 있는지 확인하려면 `onTrial` 메서드를 쓰세요. 체험 중임을 알려주는 배너 등을 띄울 때 유용합니다:

```php
if ($user->subscription('default')->onTrial()) {
    //
}
```

특정 요금제(예: 월/년 요금제)에 구독 중인지 확인하려면 `subscribedToPlan` 메서드를 사용하세요:

```php
if ($user->subscribedToPlan($monthly = 12345, 'default')) {
    //
}
```

여러 플랜(예: 월, 년) 중 하나라도 해당하면 구독 중으로 간주하도록 배열로 전달할 수도 있습니다:

```php
if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
    //
}
```

트라이얼이 지났는지 확인하려면 `recurring` 메서드를 사용하세요:

```php
if ($user->subscription('default')->recurring()) {
    //
}
```

<a name="cancelled-subscription-status"></a>
#### 구독 취소 상태

예전에 구독자인 적이 있지만 현재는 취소된 경우, `cancelled` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription('default')->cancelled()) {
    //
}
```

"유예 기간(grace period)" 중에 있는 사용자는 `onGracePeriod`로 확인할 수 있습니다. 예를 들어, 3월 5일 취소, 3월 10일까지 구독 유지라면 3월 10일까지 유예입니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

진짜로 구독이 끝났는지는 `ended` 메서드로 확인하세요:

```php
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="past-due-status"></a>
#### 연체(past_due) 상태

결제 실패 시 구독은 `past_due`로 표시됩니다. 이 상태에서는 결제 정보를 갱신하기 전까지 활성화되지 않습니다. 해당 상태는 `pastDue`로 확인합니다:

```php
if ($user->subscription('default')->pastDue()) {
    //
}
```

이때는 [결제 정보 업데이트](#updating-payment-information)를 안내해야 합니다. 연체 상태 관리 방식은 [Paddle 구독 설정](https://vendors.paddle.com/subscription-settings)에서 조정할 수 있습니다.

연체 상태에서도 구독을 활성화 상태로 간주하려면, Cashier의 `keepPastDueSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register`에서 사용하세요:

```php
use Laravel\Paddle\Cashier;

public function register()
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> **경고**  
> 연체 상태의 구독은 결제 정보 갱신 전까지는 변경할 수 없습니다. 이 상태에서 `swap`, `updateQuantity` 같은 메서드는 예외를 던집니다.

<a name="subscription-scopes"></a>
#### 구독 스코프

다양한 구독 상태는 Eloquent 쿼리 스코프 형태로도 제공되어 데이터베이스에서 특정 상태 구독만 쉽게 조회할 수 있습니다:

```php
// 전체 활성 구독 가져오기
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자의 취소된 구독만 조회
$subscriptions = $user->subscriptions()->cancelled()->get();
```

사용 가능한 모든 스코프:

```php
Subscription::query()->active();
Subscription::query()->onTrial();
Subscription::query()->notOnTrial();
Subscription::query()->pastDue();
Subscription::query()->recurring();
Subscription::query()->ended();
Subscription::query()->paused();
Subscription::query()->notPaused();
Subscription::query()->onPausedGracePeriod();
Subscription::query()->notOnPausedGracePeriod();
Subscription::query()->cancelled();
Subscription::query()->notCancelled();
Subscription::query()->onGracePeriod();
Subscription::query()->notOnGracePeriod();
```

<a name="subscription-single-charges"></a>
### 구독 단일 청구

구독자에게 구독 외에 1회성 추가 금액을 청구할 수 있습니다:

```php
$response = $user->subscription('default')->charge(12.99, 'Support Add-on');
```

[단일 청구](#single-charges)와 달리, 이 방식은 사용자 구독의 저장된 결제 수단에 즉시 청구합니다. 금액은 구독 통화로 전달해야 합니다.

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독마다 별도의 결제 수단을 저장합니다. 특정 구독의 기본 결제 수단을 변경하려면, 먼저 구독 모델에서 `updateUrl` 메서드로 "업데이트 URL"을 생성하세요:

```php
use App\Models\User;

$user = User::find(1);

$updateUrl = $user->subscription('default')->updateUrl();
```

이 URL을 `paddle-button` Blade 컴포넌트에 넘겨 사용자가 위젯을 통해 결제 정보를 변경할 수 있게 합니다:

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

정보 변경이 끝나면 Paddle이 `subscription_updated` 웹훅을 발송하고, Cashier가 DB의 구독 정보를 업데이트합니다.

<a name="changing-plans"></a>
### 요금제 변경

기존 사용자가 요금제를 변경하고 싶다면, 구독 모델의 `swap` 메서드에 Paddle 요금제 식별자를 전달하세요:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap($premium = 34567);
```

즉시 청구서를 발송하면서 플랜을 변경하려면, `swapAndInvoice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice($premium = 34567);
```

> **경고**  
> 트라이얼이 진행 중인 구독은 플랜 변경이 불가합니다. 자세한 제한 사항은 [Paddle 문서](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes) 참고.

<a name="prorations"></a>
#### 일할 계산(Prorate)

기본적으로 Paddle은 플랜 변경 시 일할 계산(Prorate)된 요금을 부과합니다. 일할 계산 없이 변경하려면 `noProrate` 메서드를 사용하세요:

```php
$user->subscription('default')->noProrate()->swap($premium = 34567);
```

<a name="subscription-quantity"></a>
### 구독 수량

경우에 따라 구독이 "수량(Quantity)"에 영향을 받을 수 있습니다(예: 프로젝트별 10달러/월 등). `incrementQuantity`, `decrementQuantity` 메서드는 수량 조정에 사용됩니다:

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity();
// 현재 수량에서 5 증가
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();
// 현재 수량에서 5 감소
$user->subscription('default')->decrementQuantity(5);
```

직접 특정 수량으로 지정하려면 `updateQuantity`를 씁니다:

```php
$user->subscription('default')->updateQuantity(10);
```

일할 계산 없이 수량만 변경하려면:

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<a name="subscription-modifiers"></a>
### 구독 모디파이어(Modifier)

구독 모디파이어는 [계량형 청구(metered billing)](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers)나 애드온 기능을 구현할 때 사용됩니다.

예를 들어 "프리미엄 지원" 같은 애드온을 추가하고 싶다면:

```php
$modifier = $user->subscription('default')->newModifier(12.99)->create();
```

위 예시는 구독에 매번 $12.99가 추가되는 애드온을 생성합니다. 간단한 설명도 추가하려면:

```php
$modifier = $user->subscription('default')->newModifier(12.99)
    ->description('Premium Support')
    ->create();
```

계량형 청구를 하고 싶을 경우(예: SMS발송 건수별 과금), Paddle 콘솔에서 $0 요금제를 만들고, 아래처럼 모디파이어를 추가합니다:

```php
$modifier = $user->subscription('default')->newModifier(0.99)
    ->description('New text message')
    ->oneTime()
    ->create();
```

`oneTime`을 호출하면, 한 번만 청구되고 반복되지 않습니다.

<a name="retrieving-modifiers"></a>
#### 모디파이어 조회

구독의 모든 모디파이어 목록은 `modifiers` 메서드로 가져올 수 있습니다:

```php
$modifiers = $user->subscription('default')->modifiers();

foreach ($modifiers as $modifier) {
    $modifier->amount(); // $0.99
    $modifier->description; // New text message.
}
```

<a name="deleting-modifiers"></a>
#### 모디파이어 삭제

`Laravel\Paddle\Modifier` 인스턴스에서 `delete`를 호출하세요:

```php
$modifier->delete();
```

<a name="multiple-subscriptions"></a>
### 복수 구독

Paddle은 한 고객이 여러 구독에 동시에 가입하는 것을 지원합니다. 예를 들어, 수영장/헬스장 구독을 두 개 따로 운영하며 각각 가격이 다를 수 있습니다.

구독 생성 시, `newSubscription`에 구독명을 지정하세요:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()
        ->newSubscription('swimming', $swimmingMonthly = 12345)
        ->create($request->paymentMethodId);

    // ...
});
```

나중에 연 요금제 등으로 전환할 때는 해당 구독명을 그대로 써서 값을 변경하면 됩니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 34567);
```

구독을 완전히 취소하려면:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시중지

구독을 일시중지하려면 구독의 `pause` 메서드를 호출하세요:

```php
$user->subscription('default')->pause();
```

일시중지 시, Cashier는 DB의 `paused_from` 필드를 자동으로 설정합니다. 예를 들어 3월 1일 일시중지, 결제 예정일이 3월 5일이라면 3월 5일까지는 아직 active로 취급됩니다.

일시중지 유예기간 여부는 `onPausedGracePeriod`로 확인합니다:

```php
if ($user->subscription('default')->onPausedGracePeriod()) {
    //
}
```

일시중지 취소시 `unpause`를 호출하세요:

```php
$user->subscription('default')->unpause();
```

> **경고**  
> 일시중지 상태인 구독은 변경할 수 없습니다. 플랜 변경/수량 변경하고 싶다면 구독을 먼저 재개하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 다음을 사용하세요:

```php
$user->subscription('default')->cancel();
```

취소 시, Cashier는 DB의 `ends_at` 필드를 설정합니다. 예를 들어 3월 1일 취소, 실제 종료일이 3월 5일이면 그때까지는 계속 구독자로 간주됩니다.

구독 취소 유예기간은 `onGracePeriod`로 확인할 수 있습니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

즉시 취소하려면 `cancelNow`를 호출하세요:

```php
$user->subscription('default')->cancelNow();
```

> **경고**  
> Paddle 구독은 한 번 취소하면 재개할 수 없습니다. 다시 구독하려면 새로 가입해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험(Trial)

<a name="with-payment-method-up-front"></a>
### 사전 결제 정보와 함께

> **경고**  
> 체험 중 결제 정보를 미리 받으면 구독 변경(요금제 변경, 수량 조정 등)이 불가합니다. 체험 중 변경을 허용하려면 구독을 취소 후 재생성해야 합니다.

체험 기간 중에도 결제 정보를 미리 받고 싶다면, 구독 pay link 생성 시 `trialDays`를 사용하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $monthly = 12345)
                ->returnTo(route('home'))
                ->trialDays(10)
                ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

이 방식은 Cashier DB에 체험 종료일을 기록하고, Paddle 역시 해당일까지는 결제 청구하지 않습니다.

> **경고**  
> 사용자가 체험기간 내에 구독을 취소하지 않으면, 만료 즉시 바로 결제됩니다. 사용자가 체험 만료일을 인지할 수 있도록 알림을 표시해야 합니다.

유저가 체험중인지 확인하려면 `onTrial`을 아래 예시처럼 쓰세요(두 방법 모두 동일):

```php
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

체험이 만료되었는지 확인하려면 `hasExpiredTrial`를 사용하세요:

```php
if ($user->hasExpiredTrial('default')) {
    //
}

if ($user->subscription('default')->hasExpiredTrial()) {
    //
}
```

<a name="defining-trial-days-in-paddle-cashier"></a>
#### Paddle/Cashier에서 체험 기간 정의

체험 기간은 Paddle 콘솔에서 플랜별로 지정하거나, 항상 Cashier에서 명시적으로 `trialDays`로 지정할 수 있습니다. Paddle에서 정의하면 동일 고객이 재구독 시에도 항상 체험이 부여되니, 반드시 `trialDays(0)`을 명시적으로 지정해야 합니다.

<a name="without-payment-method-up-front"></a>
### 사전 결제 정보 없이

결제 정보를 미리 받지 않고 체험만 제공하려면, 사용자의 고객 레코드에 `trial_ends_at` 컬럼을 추가/설정합니다. 보통 회원가입 시 처리합니다:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

이 방식을 Cashier에서는 "일반(Generic) 체험"이라 부릅니다. 실제 구독이란 연결되지 않고, `trial_ends_at` 날짜 전이면 `onTrial` 메서드에서 true를 반환합니다:

```php
if ($user->onTrial()) {
    // 체험 기간 중
}
```

실제 구독 생성 시에는 기존과 동일하게 `newSubscription` 사용:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

체험 만료일 조회는 `trialEndsAt`로, 특정 구독명을 넣으면 해당 정보만 확인할 수 있습니다:

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

실제 구독이 없는 "일반(Generic)" 체험 여부 확인은 `onGenericTrial`로 가능합니다:

```php
if ($user->onGenericTrial()) {
    // 일반(trials) 체험 기간 중
}
```

> **경고**  
> Paddle 구독 생성 후에는 체험 기간 연장/수정이 불가합니다.

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리

Paddle은 다양한 이벤트를 웹훅으로 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더는 자신의 웹훅 컨트롤러 라우트를 등록합니다. 이 컨트롤러가 모든 웹훅 요청을 처리합니다.

이 컨트롤러는 Paddle의 반복 결제 실패, 구독 갱신/변경, 결제 수단 변경 등 주요 이벤트는 자동 처리합니다. 추가적인 웹훅도 직접 확장할 수 있습니다.

Paddle 웹훅을 제대로 처리하려면 [Paddle 콘솔에서 웹훅 URL을 등록](https://vendors.paddle.com/alerts-webhooks)하세요. 기본적으로 Cashier 웹훅 컨트롤러는 `/paddle/webhook` 경로로 응답합니다. Paddle 콘솔에서는 다음 웹훅을 활성화해야 합니다:

- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded

> **경고**  
> Cashier의 [웹훅 서명 검증](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures) 미들웨어로 외부 요청 보호를 꼭 활성화하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅 & CSRF 보호

Paddle 웹훅이 Laravel의 [CSRF 보호](/docs/{{version}}/csrf)를 우회하려면, `App\Http\Middleware\VerifyCsrfToken`의 예외로 등록하거나 `web` 미들웨어 그룹 밖에 위치해야 합니다:

```php
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
#### 웹훅 & 로컬 개발

로컬 개발 중 웹훅을 테스트하려면, [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 셰어링 서비스를 써서 외부로 노출해야 합니다. [Laravel Sail](/docs/{{version}}/sail)로 개발한다면 Sail의 [사이트 셰어링 명령어](/docs/{{version}}/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 결제 실패 시 구독 취소 등 주요 Paddle 웹훅을 자동 처리합니다. 추가적으로 처리하고 싶은 이벤트가 있다면 하단 이벤트들을 리스닝할 수 있습니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

이벤트 객체에는 Paddle 웹훅의 전체 payload가 담겨 있습니다. 예를 들어 `invoice.payment_succeeded` 웹훅을 처리하려면:

```php
namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'payment_succeeded') {
            // 이벤트 핸들링
        }
    }
}
```

리스너를 정의했다면 `EventServiceProvider`에 등록하세요:

```php
namespace App\Providers;

use App\Listeners\PaddleEventListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Paddle\Events\WebhookReceived;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        WebhookReceived::class => [
            PaddleEventListener::class,
        ],
    ];
}
```

또한 Cashier는 웹훅 타입별 전용 이벤트도 제공합니다. 이 객체에는 Paddle 원본 데이터뿐 아니라 관련 billable 모델, 구독, 영수증 객체가 함께 포함됩니다:

- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

기본 내장 웹훅 경로를 커스텀 값으로 바꾸려면 `.env` 파일의 `CASHIER_WEBHOOK` 환경변수에 전체 URL을 설정하고, Paddle 콘솔에도 동일하게 등록하세요:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안을 위해 [Paddle의 웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks) 방식을 쓸 수 있습니다. Cashier는 Paddle 웹훅 요청의 유효성을 검증하는 미들웨어를 포함합니다.

웹훅 검증을 위해, `.env` 파일에 `PADDLE_PUBLIC_KEY` 환경변수가 반드시 정의되어 있어야 합니다. 해당 키는 Paddle 대시보드에서 확인 가능합니다.

<a name="single-charges"></a>
## 단일 청구

<a name="simple-charge"></a>
### 간단한 청구

고객에게 일회성 청구(온디맨드 결제)를 하려면, billable 모델 인스턴스에서 `charge` 메서드를 사용해 페이 링크를 생성하세요. 첫 번째 인수는 금액(float), 두 번째는 설명입니다:

```php
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $user->charge(12.99, 'Action Figure')
    ]);
});
```

생성된 페이 링크를 `paddle-button` Blade 컴포넌트로 전달하면 위젯이 실행됩니다:

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

세 번째 인수로 옵션 배열을 넘겨 파라미터를 커스터마이즈할 수 있습니다. 지원 옵션은 [Paddle 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) 참고:

```php
$payLink = $user->charge(12.99, 'Action Figure', [
    'custom_option' => $value,
]);
```

결제 통화는 기본적으로 `cashier.currency` 설정값(기본 USD)입니다. `.env`의 `CASHIER_CURRENCY`로 변경 가능합니다:

```ini
CASHIER_CURRENCY=EUR
```

Paddle의 동적 가격 정책을 사용해 통화별 가격을 지정하려면 금액 배열을 넘깁니다:

```php
$payLink = $user->charge([
    'USD:19.99',
    'EUR:15.99',
], 'Action Figure');
```

<a name="charging-products"></a>
### 상품 청구

Paddle에 등록된 특정 상품의 일회성 결제를 진행하려면 `chargeProduct`를 사용하세요:

```php
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $request->user()->chargeProduct($productId = 123)
    ]);
});
```

이 링크를 `paddle-button`에 넘깁니다:

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`chargeProduct`의 두 번째 인수로 옵션 배열을 넘겨 추가 파라미터를 사용할 수 있습니다. 자세한 내용은 [Paddle 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) 참고:

```php
$payLink = $user->chargeProduct($productId, [
    'custom_option' => $value,
]);
```

<a name="refunding-orders"></a>
### 주문 환불

Paddle 주문을 환불하려면 `refund` 메서드를 사용하세요. 첫 번째 인수는 Paddle 주문 ID입니다. 사용자의 영수증은 `receipts` 메서드로 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$receipt = $user->receipts()->first();

$refundRequestId = $user->refund($receipt->order_id);
```

특정 금액만 환불하거나 사유를 명시하려면 두 번째/세 번째 인수를 전달하세요:

```php
$refundRequestId = $user->refund(
    $receipt->order_id, 5.00, 'Unused product time'
);
```

> **참고**  
> 환불 관련 문의 시 `$refundRequestId`를 Paddle 지원팀에 참조로 쓸 수 있습니다.

<a name="receipts"></a>
## 영수증

billable 모델의 영수증은 `receipts` 프로퍼티로 바로 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$receipts = $user->receipts;
```

사용자에게 영수증 목록을 보여줄 때 각 인스턴스의 메서드를 활용해 필요한 정보를 보여줄 수 있습니다:

```html
<table>
    @foreach ($receipts as $receipt)
        <tr>
            <td>{{ $receipt->paid_at->toFormattedDateString() }}</td>
            <td>{{ $receipt->amount() }}</td>
            <td><a href="{{ $receipt->receipt_url }}" target="_blank">Download</a></td>
        </tr>
    @endforeach
</table>
```

<a name="past-and-upcoming-payments"></a>
### 이전 및 예정된 결제

구독의 이전 결제/예정 결제 정보를 표시할 때는 `lastPayment`, `nextPayment`를 쓰세요:

```php
use App\Models\User;

$user = User::find(1);
$subscription = $user->subscription('default');

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 단, `nextPayment`는 청구 주기가 종료된 경우(null반환)입니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
## 실패한 결제 처리

카드 만료, 잔액 부족 등으로 구독 결제에 실패할 수 있습니다. 이 경우 Paddle의 [자동 결제 알림 메일](https://vendors.paddle.com/subscription-settings) 기능을 활용하는 것이 가장 간편합니다.

또는 Cashier가 발행하는 `WebhookReceived` 이벤트를 리스닝해 `subscription_payment_failed` 웹훅을 직접 처리할 수도 있습니다. Paddle 대시보드의 Webhook 설정에서 "Subscription Payment Failed" 항목도 활성화해야 합니다:

```php
namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'subscription_payment_failed') {
            // 결제 실패 이벤트 처리
        }
    }
}
```

리스너를 정의했다면 `EventServiceProvider`에 등록하세요:

```php
namespace App\Providers;

use App\Listeners\PaddleEventListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Paddle\Events\WebhookReceived;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        WebhookReceived::class => [
            PaddleEventListener::class,
        ],
    ];
}
```

<a name="testing"></a>
## 테스트

실제 결제 플로우가 정상적으로 동작하는지 수동 테스트는 반드시 진행해야 합니다.

자동화된 테스트(예: CI 환경)에서는 [Laravel HTTP 클라이언트](/docs/{{version}}/http-client#testing)의 fake 기능을 써서 Paddle 호출을 모방할 수 있습니다. 이는 실제 Paddle 응답을 검증하지는 않지만, API 연동 없이 앱 로직 자체를 테스트하는 데 유용합니다.