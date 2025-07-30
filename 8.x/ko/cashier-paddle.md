# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
    - [데이터베이스 마이그레이션](#database-migrations)
- [설정](#configuration)
    - [청구 가능한 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이딩](#overriding-default-models)
- [핵심 개념](#core-concepts)
    - [결제 링크](#pay-links)
    - [인라인 체크아웃](#inline-checkout)
    - [사용자 식별](#user-identification)
- [가격](#prices)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
- [구독](#subscriptions)
    - [구독 생성하기](#creating-subscriptions)
    - [구독 상태 확인하기](#checking-subscription-status)
    - [구독 일회성 결제](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [요금제 변경하기](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [구독 수정자](#subscription-modifiers)
    - [구독 일시 중지](#pausing-subscriptions)
    - [구독 취소](#cancelling-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 수단을 먼저 받는 경우](#with-payment-method-up-front)
    - [결제 수단 없이 체험 기간만 제공하는 경우](#without-payment-method-up-front)
- [Paddle 웹훅 처리하기](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의하기](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [일회성 결제](#single-charges)
    - [간단한 결제](#simple-charge)
    - [제품 결제](#charging-products)
    - [주문 환불](#refunding-orders)
- [영수증](#receipts)
    - [과거 및 예정된 결제](#past-and-upcoming-payments)
- [결제 실패 처리](#handling-failed-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 사용하기 위한 표현력 풍부하고 직관적인 인터페이스를 제공합니다. 반복적으로 작성해야 하는 구독 결제 코드 대부분을 자동으로 처리해 줍니다. 기본적인 구독 관리 기능 외에도 쿠폰, 구독 교체, 구독 수량, 취소 유예 기간 등 다양한 기능들을 지원합니다.

Cashier를 사용할 때는 Paddle의 [사용자 가이드](https://developer.paddle.com/guides)와 [API 문서](https://developer.paddle.com/api-reference/intro)도 함께 확인할 것을 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 검토하시기 바랍니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용하여 Paddle용 Cashier 패키지를 설치하세요:

```
composer require laravel/cashier-paddle
```

> [!NOTE]
> Cashier가 Paddle의 모든 이벤트를 올바르게 처리하려면 [Cashier 웹훅 설정](#handling-paddle-webhooks)을 반드시 구성해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 또는 스테이징 개발 환경에서는 [Paddle 샌드박스 계정](https://developer.paddle.com/getting-started/sandbox)을 등록하여 실제 결제 없이 테스트와 개발을 진행하세요. Paddle의 [테스트 카드 번호](https://developer.paddle.com/getting-started/sandbox#test-cards)를 사용해 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

샌드박스 환경을 사용하는 경우, 애플리케이션의 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다:

```
PADDLE_SANDBOX=true
```

개발이 완료된 후에는 [Paddle 판매자(vendor) 계정을 신청할 수 있습니다](https://paddle.com).

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션

Cashier 서비스 프로바이더는 자체 데이터베이스 마이그레이션 경로를 등록하므로, 패키지 설치 후에는 데이터베이스 마이그레이션을 실행해야 합니다. Cashier의 마이그레이션은 `customers` 테이블과 함께, 고객 구독 정보를 저장하는 `subscriptions` 테이블, 그리고 영수증 정보를 저장하는 `receipts` 테이블을 생성합니다:

```
php artisan migrate
```

Cashier 기본 마이그레이션을 덮어쓰려고 한다면, `vendor:publish` Artisan 명령어를 사용해 마이그레이션을 내보낼 수 있습니다:

```
php artisan vendor:publish --tag="cashier-migrations"
```

마이그레이션을 아예 실행하지 않도록 하려면, Cashier가 제공하는 `ignoreMigrations` 메서드를 `AppServiceProvider`의 `register` 메서드 안에서 호출하세요:

```
use Laravel\Paddle\Cashier;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
{
    Cashier::ignoreMigrations();
}
```

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 가능한 모델

Cashier를 사용하기 전에, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 정보 업데이트 등의 공통 결제 작업을 수행할 수 있는 메서드들을 제공합니다:

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 다른 청구 가능한 엔티티가 있다면 해당 클래스에도 같은 트레이트를 사용할 수 있습니다:

```
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키

이제 애플리케이션 `.env` 파일에 Paddle API 키를 설정하세요. Paddle 콘트롤 패널에서 아래 키를 얻을 수 있습니다:

```
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 변수는 위에서 설명한 [샌드박스 환경](#paddle-sandbox)을 사용할 때 `true`로 설정하고, 운영 환경에서는 `false`로 설정해야 합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle 체크아웃 위젯을 실행하려면 Paddle의 JavaScript 라이브러리가 필요합니다. 애플리케이션 레이아웃의 `</head>` 닫는 태그 직전에 `@paddleJS` Blade 지시자를 추가해서 라이브러리를 불러올 수 있습니다:

```
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 애플리케이션 `.env`에 `CASHIER_CURRENCY` 환경 변수를 정의하세요:

```
CASHIER_CURRENCY=EUR
```

또한 인보이스에 표시되는 금액의 포맷을 설정할 때 사용하는 로케일도 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 NumberFormatter 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!NOTE]
> `en` 외 다른 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되고 활성화되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이딩

Cashier가 내부적으로 사용하는 모델을 확장하고 싶으면, 직접 모델을 정의하고 해당 Cashier 모델을 상속하여 구현할 수 있습니다:

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Paddle\Cashier` 클래스로 Cashier에 사용자 지정 모델을 알려줘야 합니다. 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 다음과 같이 구성합니다:

```
use App\Models\Cashier\Receipt;
use App\Models\Cashier\Subscription;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 *
 * @return void
 */
public function boot()
{
    Cashier::useReceiptModel(Receipt::class);
    Cashier::useSubscriptionModel(Subscription::class);
}
```

<a name="core-concepts"></a>
## 핵심 개념

<a name="pay-links"></a>
### 결제 링크

Paddle은 구독 상태 변경을 위한 다양하고 자세한 CRUD API를 제공하지 않습니다. 따라서 Paddle과의 대부분 상호작용은 [체크아웃 위젯](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout)을 통해 이루어집니다. 이 위젯을 표시하기 전에, Cashier를 통해 수행할 결제 작업에 대한 정보를 담은 "결제 링크"를 생성해야 합니다:

```
use App\Models\User;
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 34567)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

Cashier는 `paddle-button` [Blade 컴포넌트](/docs/{{version}}/blade#components)를 제공하며, 위 생성한 결제 링크 URL을 "prop"으로 전달할 수 있습니다. 버튼 클릭 시 Paddle 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    구독하기
</x-paddle-button>
```

기본적으로 Paddle 스타일로 꾸며진 버튼이 표시됩니다. 만약 Paddle의 모든 기본 스타일을 제거하고 싶으면 `data-theme="none"` 속성을 추가하세요:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    구독하기
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기 처리로 동작합니다. 사용자가 위젯 내에서 구독을 생성 또는 업데이트하면 Paddle에서 웹훅을 통해 변경 사항을 알려주므로, 이를 받아 자체 DB 구독 상태를 업데이트할 수 있도록 반드시 [웹훅 설정](#handling-paddle-webhooks)을 완료해야 합니다.

더 자세한 결제 링크 생성 방법은 [Paddle API 문서의 결제 링크 생성 관련 내용](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

> [!NOTE]
> 구독 상태가 변경된 후 이와 관련된 웹훅이 도착하는 지연 시간은 보통 짧지만, 결제가 완료된 직후에 사용자의 구독 상태가 즉시 반영되지 않을 수 있음을 애플리케이션 내에서 고려해야 합니다.

<a name="manually-rendering-pay-links"></a>
#### 결제 링크 직접 렌더링하기

Laravel의 Blade 컴포넌트를 사용하지 않고 직접 결제 링크를 렌더링할 수도 있습니다. 앞서 예시처럼 결제 링크 URL을 먼저 생성하세요:

```
$payLink = $request->user()->newSubscription('default', $premium = 34567)
    ->returnTo(route('home'))
    ->create();
```

그다음 HTML에서 `a` 태그에 결제 링크 URL을 연결하세요:

```
<a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
    Paddle 체크아웃
</a>
```

<a name="payments-requiring-additional-confirmation"></a>
#### 추가 확인이 필요한 결제

때때로 결제 확인 및 처리를 위해 추가 검증이 필요할 수 있습니다. 이때 Paddle은 카드사 또는 은행의 결제 플로우에 맞춘 별도의 결제 확인 화면을 표시합니다. 여기에는 카드 확인, 임시 소액 청구, 별도 기기 인증 등 다양한 확인 방식이 포함될 수 있습니다.

<a name="inline-checkout"></a>
### 인라인 체크아웃

Paddle의 "오버레이" 방식 체크아웃 위젯 대신, 위젯을 애플리케이션 내에 직접 삽입하는 인라인 방식도 제공합니다. 인라인 체크아웃은 HTML 필드를 조작할 수 없지만, 내장 위젯을 앱 내에 임베드할 수 있습니다.

Cashier는 인라인 체크아웃을 간편하게 시작할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. [결제 링크를 생성](#pay-links)하여 `override` 속성에 전달하세요:

```html
<x-paddle-checkout :override="$payLink" class="w-full" />
```

컴포넌트 높이를 조절하려면 `height` 속성을 전달할 수 있습니다:

```
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
#### 결제 링크 없이 인라인 체크아웃 사용하기

결제 링크를 사용하지 않고, 원하는 옵션을 직접 지정해 위젯을 커스터마이징할 수도 있습니다:

```
$options = [
    'product' => $productId,
    'title' => '제품명',
];

<x-paddle-checkout :options="$options" class="w-full" />
```

더 자세한 사항은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout)와 [파라미터 레퍼런스](https://developer.paddle.com/reference/paddle-js/parameters)를 참고하세요.

> [!NOTE]
> 추가 옵션으로 `passthrough`를 사용하려면, 키/값 배열을 넘기면 Cashier가 자동으로 JSON 문자열로 변환해 줍니다. 단, `customer_id` passthrough 키는 내부적으로 Cashier 전용으로 예약되어 있습니다.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 직접 렌더링

Laravel Blade 컴포넌트를 사용하지 않고 인라인 체크아웃을 직접 렌더링할 수도 있습니다. 우선 [앞서 설명한대로 결제 링크를 생성한 후](#pay-links), Paddle.js를 이용해 체크아웃을 초기화합니다. 예시에서는 간단히 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하였으나, 원하는 프론트엔드 스택으로 쉽게 변환할 수 있습니다:

```html
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

Stripe와는 달리 Paddle의 사용자는 Paddle 전체에 걸쳐 고유하며, Paddle 계정별 고유가 아닙니다. 따라서 Paddle API는 사용자의 이메일 같은 상세 정보를 업데이트할 수 있는 방법을 제공하지 않습니다. 결제 링크 생성 시 Paddle은 `customer_email` 파라미터로 사용자를 식별하며, 구독 생성 시 전달된 이메일로 기존 Paddle 사용자와 매칭을 시도합니다.

이 특성 때문에 Cashier와 Paddle을 함께 사용할 때는 몇 가지 유의할 점이 있습니다. 첫째, Cashier 상의 동일 사용자의 구독이라도 Paddle 내부에서는 서로 다른 사용자에 연결될 수 있습니다. 둘째, 각 구독은 자체 결제 정보와 내부적으로 서로 다른 이메일 주소를 가질 수 있습니다 (구독 생성 시 지정된 이메일에 따라 다름).

따라서 구독을 표시할 때는 사용자에게 각 구독별 연결된 이메일 주소나 결제 정보를 명확히 안내하는 것이 좋습니다. 다음 `Laravel\Paddle\Subscription` 모델이 제공하는 메서드로 이 정보를 조회할 수 있습니다:

```
$subscription = $user->subscription('default');

$subscription->paddleEmail();
$subscription->paymentMethod();
$subscription->cardBrand();
$subscription->cardLastFour();
$subscription->cardExpirationDate();
```

현재 Paddle API를 통해 사용자의 이메일 주소를 변경할 수 있는 방법은 없습니다. 사용자가 Paddle 내 이메일을 변경하고자 하면 Paddle 고객 지원에 문의해야 하며, 이때 위 `paddleEmail` 값을 알려줘야 정확한 사용자를 식별할 수 있습니다.

<a name="prices"></a>
## 가격

Paddle은 국가별로 다른 통화와 가격을 설정할 수 있어 국가마다 가격이 다를 수 있습니다. Cashier Paddle에서는 특정 상품에 대한 모든 가격을 `productPrices` 메서드로 조회할 수 있습니다. 이 메서드는 가격을 조회할 상품 ID 배열을 인수로 받습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456]);
```

통화는 기본적으로 요청자의 IP 주소를 기반으로 결정되나, 특정 국가를 수동으로 지정할 수도 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);
```

가져온 가격 정보는 원하는 형태로 출력할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

부가세를 제외한 순수 가격(net price)과 세금 금액을 별도로 표시할 수도 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} 세금)</li>
    @endforeach
</ul>
```

구독 요금제를 위한 가격이라면 초기 가격과 반복 가격을 별도로 표시할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - 초기: {{ $price->initialPrice()->gross() }} - 반복: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

추가로 Paddle의 [가격 관련 API 문서](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)를 참고하세요.

<a name="prices-customers"></a>
#### 고객별 가격

이미 고객 정보가 있는 유저에게 해당 고객 맞춤 가격을 보여주려면, 유저 인스턴스에서 `productPrices`를 조회할 수 있습니다:

```
use App\Models\User;

$prices = User::find(1)->productPrices([123, 456]);
```

내부적으로 Cashier는 유저의 [`paddleCountry` 메서드](#customer-defaults)를 호출해 해당 통화로 가격을 조회합니다. 예를 들어 미국에 사는 사용자는 USD 가격을, 벨기에 사용자는 EUR 가격을 보게 됩니다. 일치하는 통화가 없으면 상품의 기본 통화가 사용됩니다. Paddle 콘트롤 패널에서 상품과 구독 요금제의 가격을 모두 변경할 수 있습니다.

<a name="prices-coupons"></a>
#### 쿠폰

쿠폰 할인을 적용한 가격을 보여주고 싶다면, `productPrices` 호출 시 쿠폰 코드를 쉼표로 구분한 문자열로 전달할 수 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], [
    'coupons' => 'SUMMERSALE,20PERCENTOFF'
]);
```

계산된 할인 가격은 `price` 메서드로 표시합니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

할인 적용 전 원래 가격은 `listPrice` 메서드로 표시할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> [!NOTE]
> Paddle 가격 API는 쿠폰을 1회성 구매 제품에만 적용할 수 있으며, 구독 요금제에는 쿠폰 적용이 불가능합니다.

<a name="customers"></a>
## 고객

<a name="customer-defaults"></a>
### 고객 기본값

Cashier는 결제 링크 생성 시 고객의 이메일, 국가, 우편번호 등을 미리 채워 사용자가 결제 페이지에서 바로 결제 단계로 넘어가도록 도와주는 기본값을 정의할 수 있게 합니다. 이를 위해 청구 가능한 모델에서 다음 메서드들을 오버라이드하세요:

```
/**
 * Paddle에 연결할 고객 이메일 주소를 반환합니다.
 *
 * @return string|null
 */
public function paddleEmail()
{
    return $this->email;
}

/**
 * Paddle에 연결할 고객 국가를 2자리 국가 코드로 반환합니다.
 *
 * 지원 국가 목록은 링크를 참고하세요.
 *
 * @return string|null
 * @link https://developer.paddle.com/reference/platform-parameters/supported-countries
 */
public function paddleCountry()
{
    //
}

/**
 * Paddle에 연결할 고객 우편번호를 반환합니다.
 *
 * 우편번호가 필요한 국가 목록은 링크를 참고하세요.
 *
 * @return string|null
 * @link https://developer.paddle.com/reference/platform-parameters/supported-countries#countries-requiring-postcode
 */
public function paddlePostcode()
{
    //
}
```

이 기본값들은 Cashier 내에서 결제 링크를 생성하는 모든 작업에 사용됩니다.

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성하기

구독을 생성하려면, 우선 보통 `App\Models\User` 인스턴스를 가져옵니다. 그 후, `newSubscription` 메서드를 사용해 구독 결제 링크를 생성할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $premium = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

`newSubscription`의 첫 번째 인자는 애플리케이션 내에서 구독을 식별할 내부 이름입니다. 애플리케이션이 단일 구독만 제공한다면 `default`나 `primary` 같은 이름을 사용할 수 있습니다. 이 이름은 사용자에게 공개하지 않으며, 공백이 포함되어선 안 되고 한 번 생성 후 변경해서도 안 됩니다.

두 번째 인자는 사용자가 가입할 Paddle 요금제 식별자입니다. `returnTo`는 체크아웃 성공 후 사용자를 리다이렉트할 URL입니다.

`create` 메서드는 결제 버튼 생성에 사용할 결제 링크(pay link)를 만듭니다. 이 결제 버튼은 Cashier Paddle이 제공하는 `paddle-button` [Blade 컴포넌트](/docs/{{version}}/blade#components)로 쉽게 생성할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    구독하기
</x-paddle-button>
```

사용자의 결제가 완료되면 Paddle에서 `subscription_created` 웹훅이 전송됩니다. Cashier가 이를 감지해 고객 구독 정보를 앱 DB에 생성합니다. 이 과정을 위해 [웹훅 설정](#handling-paddle-webhooks)을 잊지 마세요.

<a name="additional-details"></a>
#### 추가 세부 사항

추가 고객 정보나 구독 옵션을 지정하려면, `create` 메서드에 키/값 배열을 전달할 수 있습니다. Paddle의 결제 링크 생성 문서에서 지원하는 필드를 참고하세요:

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->create([
        'vat_number' => $vatNumber,
    ]);
```

<a name="subscriptions-coupons"></a>
#### 쿠폰 적용

구독 생성 시 쿠폰 할인 적용이 필요하면 `withCoupon` 메서드를 사용하세요:

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withCoupon('code')
    ->create();
```

<a name="metadata"></a>
#### 메타데이터

`withMetadata` 메서드로 임의 키/값 배열의 메타데이터도 첨부할 수 있습니다:

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withMetadata(['key' => 'value'])
    ->create();
```

> [!NOTE]
> 메타데이터 키로 `subscription_name` 은 사용하지 마세요. 이 키는 내부적으로 Cashier에서 예약되어 있습니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인하기

사용자가 구독 중인지 다양한 편리한 메서드로 확인할 수 있습니다. 먼저 `subscribed` 메서드는 구독이 활성 상태이거나 체험 기간 중인 경우 `true`를 반환합니다:

```
if ($user->subscribed('default')) {
    //
}
```

`subscribed`는 [라우트 미들웨어](/docs/{{version}}/middleware)로도 활용해 구독자만 접근이 가능한 라우트를 만들 수 있습니다:

```
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserIsSubscribed
{
    /**
     * 요청을 처리합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 활성 구독자가 아님
            return redirect('billing');
        }

        return $next($request);
    }
}
```

체험 기간인지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 체험 기간임을 사용자에게 알릴 때 유용합니다:

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

`subscribedToPlan` 메서드는 특정 Paddle 요금제에 사용자가 가입되어 있는지를 검사합니다. 예를 들어, `default` 구독이 월간 요금제에 가입되어 있는지 확인할 수 있습니다:

```
if ($user->subscribedToPlan($monthly = 12345, 'default')) {
    //
}
```

배열을 전달해 여러 요금제 중 어느 하나에 가입된 상태인지도 확인할 수 있습니다:

```
if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
    //
}
```

`recurring` 메서드는 사용자가 현재 활성 구독이면서 체험 기간은 지난 상태인지 확인할 때 씁니다:

```
if ($user->subscription('default')->recurring()) {
    //
}
```

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

과거에 활성 구독자였으나 구독을 취소한 상태는 `cancelled` 메서드로 확인할 수 있습니다:

```
if ($user->subscription('default')->cancelled()) {
    //
}
```

취소는 했지만 아직 기간 만료 전인 "유예 기간(grace period)"에 있는지는 `onGracePeriod` 메서드로 확인합니다. 예를 들어 3월 1일 취소했지만 3월 5일 만료 예정이라면 그 기간이 유예 기간입니다. 이때 `subscribed`는 여전히 `true`를 반환합니다:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

유예 기간이 끝나 구독이 완전히 종료된 상태는 `ended` 메서드로 확인하세요:

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="past-due-status"></a>
#### 연체 상태

결제가 실패해 `past_due` 상태가 되면 고객이 결제 정보를 업데이트하기 전까지 구독이 활성화되지 않습니다. `pastDue` 메서드로 확인할 수 있습니다:

```
if ($user->subscription('default')->pastDue()) {
    //
}
```

연체 상태인 경우 [결제 정보 업데이트](#updating-payment-information)를 안내해야 하며, 처리 방식은 Paddle 구독 설정에서 조정할 수 있습니다.

연체 상태여도 구독을 활성 상태로 유지하려면 Cashier의 `keepPastDueSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register` 메서드에서 호출하세요:

```
use Laravel\Paddle\Cashier;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!NOTE]
> 연체 상태 구독은 결제 정보가 갱신될 때까지 수정할 수 없습니다. 따라서 `swap`, `updateQuantity` 같은 메서드는 연체 상태에서 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

대부분 구독 상태는 쿼리 스코프로도 제공되어 데이터베이스에서 원하는 상태의 구독을 쉽게 조회할 수 있습니다:

```
// 활성 구독 모두 조회
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자 취소된 구독 조회
$subscriptions = $user->subscriptions()->cancelled()->get();
```

사용할 수 있는 전체 스코프 목록:

```
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
### 구독 일회성 결제

구독자에게 구독 요금 외 추가로 일회성 결제를 청구할 수 있습니다:

```
$response = $user->subscription('default')->charge(12.99, '지원 추가 서비스');
```

보통 [일회성 결제](#single-charges)와 달리, 이 메서드는 구독자의 저장된 결제 수단을 즉시 청구합니다. 금액은 항상 구독 통화 단위로 지정해야 합니다.

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별 결제 수단을 저장합니다. 기본 결제 수단을 변경하려면, 해당 구독 모델에서 `updateUrl` 메서드로 업데이트 URL을 생성하세요:

```
use App\Models\User;

$user = User::find(1);

$updateUrl = $user->subscription('default')->updateUrl();
```

해당 URL을 앞서 설명한 `paddle-button` Blade 컴포넌트에 넘기면 사용자는 Paddle 위젯을 통해 결제 정보를 갱신할 수 있습니다:

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    카드 업데이트
</x-paddle-button>
```

사용자가 업데이트를 완료하면 Paddle에서 `subscription_updated` 웹훅이 발송되고, 앱 DB의 구독 정보도 갱신됩니다.

<a name="changing-plans"></a>
### 요금제 변경하기

사용자가 요금제를 변경하려면 구독의 `swap` 메서드에 Paddle 요금제 ID를 넘기세요:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap($premium = 34567);
```

즉시 청구서를 발행하고 싶으면 `swapAndInvoice` 메서드를 사용합니다:

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice($premium = 34567);
```

> [!NOTE]
> 체험 기간에는 요금제를 변경할 수 없습니다. 이 점과 관련한 자세한 내용은 [Paddle 문서](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes)를 참고하세요.

<a name="prorations"></a>
#### 사용 기간 비례 계산 (Proration)

기본적으로 Paddle은 요금제 변경 시 기간에 따라 사용 금액을 비례 계산합니다. 비례 계산 없이 변경하려면 `noProrate` 메서드를 체인으로 호출하세요:

```
$user->subscription('default')->noProrate()->swap($premium = 34567);
```

<a name="subscription-quantity"></a>
### 구독 수량

구독 수량은 예를 들어 프로젝트당 월 $10과 같은 상황에서 사용할 수 있습니다. 구독 수량을 간편히 늘리거나 줄이려면 `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하세요:

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 현재 수량에 5 추가
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 현재 수량에서 5 감소
$user->subscription('default')->decrementQuantity(5);
```

특정 수량으로 설정하려면 `updateQuantity` 메서드를 사용합니다:

```
$user->subscription('default')->updateQuantity(10);
```

비례 계산 없이 수량을 변경하려면 다음과 같이 `noProrate` 메서드를 체인 연결하세요:

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<a name="subscription-modifiers"></a>
### 구독 수정자

구독 수정자는 [사용량 기반 청구(metered billing)](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers)이나 부가 기능 추가에 사용됩니다.

예를 들어, 기본 구독에 "프리미엄 지원" 추가 옵션을 붙이고 싶다면 다음처럼 수정자를 만듭니다:

```
$modifier = $user->subscription('default')->newModifier(12.99)->create();
```

기본적으로 이 비용은 구독 기간마다 반복 청구됩니다. 필요하면 `description` 메서드로 설명을 추가할 수 있습니다:

```
$modifier = $user->subscription('default')->newModifier(12.99)
    ->description('프리미엄 지원')
    ->create();
```

문자 메시지 발송 수에 따라 과금하는 예시로, Paddle에서 $0 요금제를 만든 뒤 각 메시지마다 수정자를 생성할 수 있습니다:

```
$modifier = $user->subscription('default')->newModifier(0.99)
    ->description('새 문자 메시지')
    ->oneTime()
    ->create();
```

`oneTime` 메서드는 해당 수정자가 일회성으로만 부과되고 반복 청구되지 않도록 합니다.

<a name="retrieving-modifiers"></a>
#### 수정자 조회

`modifiers` 메서드로 구독의 모든 수정자 목록을 가져올 수 있습니다:

```
$modifiers = $user->subscription('default')->modifiers();

foreach ($modifiers as $modifier) {
    $modifier->amount(); // $0.99
    $modifier->description; // 새 문자 메시지
}
```

<a name="deleting-modifiers"></a>
#### 수정자 삭제

`Laravel\Paddle\Modifier` 인스턴스의 `delete` 메서드를 호출하면 삭제할 수 있습니다:

```
$modifier->delete();
```

<a name="pausing-subscriptions"></a>
### 구독 일시 중지

구독을 일시 중지하려면 사용자의 구독 인스턴스에서 `pause` 메서드를 호출하세요:

```
$user->subscription('default')->pause();
```

일시 중지 시 `paused_from` 컬럼에 값이 저장됩니다. 이 컬럼은 `paused` 메서드가 `true`를 반환할 시점을 결정하는 데 사용됩니다. 예를 들어 사용자가 3월 1일에 일시 중지했지만 3월 5일에 다음 결제일이 있다면, 3월 5일 이전까지는 여전히 `paused`가 `false`를 반환합니다. 이는 사용자가 청구 주기 종료일까지 앱을 계속 사용할 수 있도록 하기 위함입니다.

일시 중지했지만 아직 유예 기간에 있는지는 `onPausedGracePeriod` 메서드로 검사할 수 있습니다:

```
if ($user->subscription('default')->onPausedGracePeriod()) {
    //
}
```

일시 중지된 구독을 재개하려면 `unpause` 메서드를 호출하세요:

```
$user->subscription('default')->unpause();
```

> [!NOTE]
> 일시 중지된 구독 상태에서는 요금제 변경이나 수량 업데이트가 불가능합니다. 변경하려면 먼저 구독을 재개해야 합니다.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 사용자의 구독 인스턴스에서 `cancel` 메서드를 호출합니다:

```
$user->subscription('default')->cancel();
```

취소 시 `ends_at` 컬럼에 만료 예정일이 저장되며, 이 기간까지는 `subscribed` 메서드가 `true`를 반환합니다. 예를 들어 3월 1일에 취소했지만 3월 5일까지 유효하다면 3월 5일까지 여전히 활성 구독으로 간주됩니다.

취소했지만 유예 기간에 있는 경우 `onGracePeriod` 메서드를 통해 판단할 수 있습니다:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

즉시 취소하려면 `cancelNow` 메서드를 호출하세요:

```
$user->subscription('default')->cancelNow();
```

> [!NOTE]
> Paddle 구독은 취소 후 재개할 수 없습니다. 구독 재개를 원하는 고객은 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간

<a name="with-payment-method-up-front"></a>
### 결제 수단을 먼저 받는 경우

> [!NOTE]
> 체험 기간 중 결제 수단을 먼저 받으면 Paddle은 요금제 변경이나 수량 업데이트를 제한합니다. 체험 기간 중 요금제 변경을 허용하려면 현재 구독을 취소 후 새로 생성해야 합니다.

체험 기간을 제공하면서 결제 수단도 미리 받으려면 구독 결제 링크 생성 시 `trialDays` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $monthly = 12345)
                ->returnTo(route('home'))
                ->trialDays(10)
                ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

이 메서드는 앱 DB에 체험 종료일을 기록하며, Paddle에도 체험 기간 동안 과금하지 말라고 알립니다.

> [!NOTE]
> 체험 종료일까지 구독 취소가 이루어지지 않으면, 체험 종료 즉시 자동으로 요금이 청구됩니다. 사용자에게 체험 종료일을 반드시 알려야 합니다.

`onTrial` 메서드로 유저가 체험 기간 중인지 확인할 수 있습니다. 다음 두 예시는 동일합니다:

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

<a name="defining-trial-days-in-paddle-cashier"></a>
#### Paddle / Cashier에서 체험 일수 정의하기

체험 기간 일수는 Paddle 대시보드에서 각 요금제별로 설정하거나 Cashier에서 항상 명시적으로 전달할 수 있습니다. Paddle에서 체험 기간을 정의한 경우, 새 구독뿐 아니라 과거 구독자로부터 새 구독이 생성되어도 항상 체험 기간이 적용됩니다. 단, `trialDays(0)`을 호출하면 체험 기간을 비활성화할 수 있습니다.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 체험 기간만 제공하는 경우

결제 수단 없이 체험 기간만 제공하려면, 유저가 연결된 고객 모델에 `trial_ends_at` 컬럼 값을 설정하세요. 보통 회원가입 과정에서 설정합니다:

```
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

Cashier는 이를 "일반 체험(generic trial)"로 부르며, 구독이 생성되지 않은 체험 상태입니다. 유저의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at`보다 이전이면 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 체험 기간 중임
}
```

구독을 생성할 준비가 되면, 언제나처럼 `newSubscription` 메서드로 구독 결제 링크를 만듭니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

체험 종료일을 얻으려면 `trialEndsAt` 메서드를 사용하세요. 구독 이름을 인수로 전달해 특정 구독 종료일을 가져올 수도 있습니다:

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

특히 일반 체험 상태인지 확인하려면 `onGenericTrial` 메서드를 사용하세요:

```
if ($user->onGenericTrial()) {
    // 일반 체험 기간 중임
}
```

> [!NOTE]
> Paddle 구독은 생성 후 체험 기간을 연장하거나 변경할 방법이 없습니다.

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리하기

Paddle은 다양한 이벤트를 웹훅으로 앱에 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더는 자체 웹훅 컨트롤러에 연결되는 라우트를 등록하여 모든 웹훅 요청을 처리합니다.

기본 컨트롤러는 실패한 결제에 따른 구독 취소, 구독 업데이트, 결제 수단 변경을 자동 처리하지만, 필요하다면 컨트롤러를 확장해 다른 Paddle 이벤트도 처리할 수 있습니다.

앱이 Paddle 웹훅을 제대로 처리하려면 Paddle 콘트롤 패널에서 웹훅 URL을 정확히 설정하세요. 기본값은 `/paddle/webhook` 경로입니다. 활성화해야 하는 웹훅 목록은 다음과 같습니다:

- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded

> [!NOTE]
> Cashier가 제공하는 [웹훅 서명 검증](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures) 미들웨어를 반드시 적용해 보안에 신경써야 합니다.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅은 Laravel의 [CSRF 보호](/docs/{{version}}/csrf)를 우회해야 하므로 `App\Http\Middleware\VerifyCsrfToken` 미들웨어에서 URI를 제외 목록에 추가하거나, `web` 미들웨어 그룹 밖에 라우트를 배치해야 합니다:

```
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
#### 웹훅과 로컬 개발

로컬 개발 환경에서 Paddle 웹훅을 받으려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction) 같은 도구로 앱을 외부에 노출할 필요가 있습니다. Laravel Sail을 사용할 경우 [Sail의 사이트 공유 명령어](/docs/{{version}}/sail#sharing-your-site)를 활용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의하기

Cashier는 실패 결제에 따른 구독 취소 같은 주요 Paddle 웹훅을 자동 처리합니다. 만약 추가로 웹훅 이벤트를 직접 처리하려면 다음 Cashier 이벤트를 리스닝할 수 있습니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` 웹훅을 처리하려면 이벤트 리스너를 등록할 수 있습니다:

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Paddle 웹훅 수신 처리
     *
     * @param  \Laravel\Paddle\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'payment_succeeded') {
            // 이벤트 처리 로직...
        }
    }
}
```

정의한 리스너는 앱 `EventServiceProvider`에 등록합니다:

```
<?php

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

Cashier는 특화된 웹훅 이벤트별 이벤트도 발송하며, 관련 모델 (청구 가능한 모델, 구독, 영수증 등) 정보도 함께 제공합니다:

- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

기본 웹훅 경로를 변경하고 싶으면 애플리케이션 `.env`에 `CASHIER_WEBHOOK` 환경 변수를 설정하세요. 이 URL은 Paddle 콘솔에 등록된 URL과 일치해야 합니다:

```bash
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안 강화를 위해 Paddle은 [웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks) 기능을 제공합니다. Cashier는 이 검증을 자동 처리하는 미들웨어를 포함합니다.

웹훅 검증을 활성화하려면 앱 `.env`에 `PADDLE_PUBLIC_KEY` 환경 변수를 Paddle 계정 대시보드에서 받은 공개 키로 설정하세요.

<a name="single-charges"></a>
## 일회성 결제

<a name="simple-charge"></a>
### 간단한 결제

고객에게 일회성 결제를 청구하려면, 청구 가능한 모델 인스턴스에서 `charge` 메서드를 호출해 결제 링크를 생성할 수 있습니다. 첫 번째 인자는 금액(실수형), 두 번째 인자는 결제 설명입니다:

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $user->charge(12.99, '액션 피규어')
    ]);
});
```

생성한 결제 링크를 Cashier가 제공하는 `paddle-button` Blade 컴포넌트에 전달해 사용자에게 결제 위젯을 표시할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    구매하기
</x-paddle-button>
```

`charge` 메서드는 세 번째 인자로 배열을 받아 Paddle 결제 링크 생성 시 전달할 옵션을 넘길 수 있습니다. 자세한 내용은 [Paddle 결제 링크 생성 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요:

```
$payLink = $user->charge(12.99, '액션 피규어', [
    'custom_option' => $value,
]);
```

결제 통화는 `cashier.currency` 설정 옵션에 따르며 기본값은 USD입니다. `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정해 기본 통화를 변경할 수 있습니다:

```bash
CASHIER_CURRENCY=EUR
```

또한 Paddle 동적 가격 매칭 시스템을 사용해 통화별 가격을 각각 지정할 수도 있습니다. 이때 고정 값 대신 가격 배열을 넘겨줍니다:

```
$payLink = $user->charge([
    'USD:19.99',
    'EUR:15.99',
], '액션 피규어');
```

<a name="charging-products"></a>
### 제품 결제

Paddle에 등록된 특정 제품에 대한 일회성 결제를 만들려면, `chargeProduct` 메서드를 사용해 결제 링크를 생성하세요:

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $request->user()->chargeProduct($productId = 123)
    ]);
});
```

이후 `paddle-button` 컴포넌트에 결제 링크를 넘겨 결제 위젯을 활성화할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    구매하기
</x-paddle-button>
```

`chargeProduct` 메서드는 두 번째 인자로 배열 옵션을 받으며, Paddle 결제 링크 생성 시 전달할 추가 옵션을 지정할 수 있습니다:

```
$payLink = $user->chargeProduct($productId, [
    'custom_option' => $value,
]);
```

옵션에 관한 자세한 내용은 [Paddle 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 확인하세요.

<a name="refunding-orders"></a>
### 주문 환불

Paddle 주문을 환불하려면 `refund` 메서드를 사용하세요. 첫 번째 인자로 Paddle 주문 ID를 넘깁니다. 청구 가능한 모델의 영수증은 `receipts` 메서드로 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$receipt = $user->receipts()->first();

$refundRequestId = $user->refund($receipt->order_id);
```

환불 금액이나 환불 사유도 지정할 수 있습니다:

```
$receipt = $user->receipts()->first();

$refundRequestId = $user->refund(
    $receipt->order_id, 5.00, '사용하지 않은 상품 기간 환불'
);
```

> [!TIP]
> `refundRequestId` 값은 Paddle 지원팀에 문의할 때 환불 참조 ID로 활용할 수 있습니다.

<a name="receipts"></a>
## 영수증

청구 가능한 모델의 영수증 목록은 `receipts` 속성을 통해 쉽게 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$receipts = $user->receipts;
```

영수증 목록을 테이블 등으로 표시할 때, 영수증 객체의 메서드를 이용해 필요한 정보를 출력하세요:

```html
<table>
    @foreach ($receipts as $receipt)
        <tr>
            <td>{{ $receipt->paid_at->toFormattedDateString() }}</td>
            <td>{{ $receipt->amount() }}</td>
            <td><a href="{{ $receipt->receipt_url }}" target="_blank">다운로드</a></td>
        </tr>
    @endforeach
</table>
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정된 결제

구독의 과거 결제 및 다음 예정 결제 정보를 `lastPayment`와 `nextPayment` 메서드로 가져올 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription('default');

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 단, 구독 만료 후에는 `nextPayment`가 `null`을 반환합니다:

```
다음 결제: {{ $nextPayment->amount() }} - 결제 예정일: {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
## 결제 실패 처리

구독 결제는 카드 만료, 잔고 부족 등 다양한 이유로 실패할 수 있습니다. 이 경우 Paddle의 [자동 청구 이메일 설정](https://vendors.paddle.com/subscription-settings)을 활용해 자동으로 실패 결제를 처리하는 것을 권장합니다.

좀 더 세밀한 커스터마이징이 필요하면 [`subscription_payment_failed`](https://developer.paddle.com/webhook-reference/subscription-alerts/subscription-payment-failed) 웹훅을 처리하고, Paddle 대시보드 웹훅 설정에서 "Subscription Payment Failed" 옵션을 활성화하세요:

```
<?php

namespace App\Http\Controllers;

use Laravel\Paddle\Http\Controllers\WebhookController as CashierController;

class WebhookController extends CashierController
{
    /**
     * 구독 결제 실패 처리
     *
     * @param  array  $payload
     * @return void
     */
    public function handleSubscriptionPaymentFailed($payload)
    {
        // 결제 실패를 처리하는 로직...
    }
}
```

<a name="testing"></a>
## 테스트

테스트 시 결제 흐름을 수동으로 시행해 통합이 정상적으로 동작하는지 확인하세요.

자동화 테스트, 특히 CI 환경에서는 [Laravel HTTP 클라이언트](/docs/{{version}}/http-client#testing)를 사용해 Paddle 호출을 가짜(faking) 처리할 수 있습니다. 이는 Paddle의 실제 응답을 테스트하지는 않지만, Paddle API 호출 없이 애플리케이션 로직만 테스트할 수 있는 방법입니다.