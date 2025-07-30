# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
    - [데이터베이스 마이그레이션](#database-migrations)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
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
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [구독 수식어](#subscription-modifiers)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시중지](#pausing-subscriptions)
    - [구독 취소](#cancelling-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 정보 선입력 시](#with-payment-method-up-front)
    - [결제 정보 미선입력 시](#without-payment-method-up-front)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [간단한 청구](#simple-charge)
    - [상품 청구](#charging-products)
    - [주문 환불](#refunding-orders)
- [영수증](#receipts)
    - [과거 및 다가오는 결제](#past-and-upcoming-payments)
- [실패한 결제 처리](#handling-failed-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 사용할 때 표현력이 뛰어나고 유연한 인터페이스를 제공합니다. 이 패키지는 여러분이 번거로워하는 대부분의 구독 결제 보일러플레이트 코드를 처리해 줍니다. 기본 구독 관리 외에도 Cashier는 쿠폰, 구독 변경, 구독 수량, 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier를 사용할 때는 Paddle의 [사용자 가이드](https://developer.paddle.com/guides)와 [API 문서](https://developer.paddle.com/api-reference)도 함께 참고하는 것을 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

> [!WARNING]
> Cashier가 Paddle 이벤트를 제대로 처리하게 하려면, 반드시 [웹훅 설정](#handling-paddle-webhooks)을 진행하세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 및 스테이징 개발 시에는 [Paddle 샌드박스 계정](https://developer.paddle.com/getting-started/sandbox)을 등록하세요. 이 계정은 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있는 환경을 제공합니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/getting-started/sandbox#test-cards)를 사용해 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

샌드박스 환경에서 작업할 때는 `.env` 파일에 `PADDLE_SANDBOX` 변수 값을 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

개발이 완료되면 [Paddle 벤더 계정](https://paddle.com)에 신청하세요. 운영 환경으로 배포하기 전에 Paddle에서 애플리케이션 도메인을 승인해야 합니다.

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션

Cashier 서비스 프로바이더는 자체 마이그레이션 디렉토리를 등록하므로, 패키지 설치 후 데이터베이스 마이그레이션을 잊지 마세요. 이 마이그레이션은 `customers` 테이블을 새로 생성하며, 고객들의 구독 내역을 저장할 `subscriptions` 테이블과 애플리케이션의 영수증 정보를 저장할 `receipts` 테이블도 생성합니다:

```shell
php artisan migrate
```

만약 Cashier의 기본 마이그레이션을 변경하고 싶다면 다음 Artisan 명령어로 공개할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

Cashier의 마이그레이션 실행을 완전히 막고 싶다면, `ignoreMigrations` 메서드를 사용할 수 있습니다. 일반적으로 이 코드는 앱의 `AppServiceProvider`의 `register` 메서드 내에서 호출합니다:

```
use Laravel\Paddle\Cashier;

/**
 * Register any application services.
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
### Billable 모델

Cashier를 사용하기 전에 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 정보 업데이트 등 일반적인 결제 작업을 수행할 수 있는 여러 메서드를 제공합니다:

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

만약 사용자 외에 결제 대상 엔티티가 있다면, 해당 클래스에도 트레이트를 추가할 수 있습니다:

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

다음으로, 애플리케이션의 `.env` 파일에서 Paddle API 키를 설정하세요. 키는 Paddle 제어판에서 확인할 수 있습니다:

```ini
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
PADDLE_PUBLIC_KEY="your-paddle-public-key"
PADDLE_SANDBOX=true
```

샌드박스 환경을 사용할 때는 `PADDLE_SANDBOX`를 `true`로 설정하고, 실제 운영 환경에서는 `false`로 지정하세요.

<a name="paddle-js"></a>
### Paddle JS

Paddle는 Paddle 체크아웃 위젯 실행을 위해 자체 JavaScript 라이브러리를 사용합니다. 이 라이브러리는 애플리케이션 레이아웃의 `</head>` 닫는 태그 직전에 Blade 디렉티브 `@paddleJS`를 넣어 불러올 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 애플리케이션 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 지정하세요:

```ini
CASHIER_CURRENCY=EUR
```

또한 청구서 내 화폐 금액 형식에 사용할 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 구성되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이딩

Cashier 내부에서 사용하는 모델을 확장하려면, 직접 모델을 정의하고 Cashier 모델을 상속받으면 됩니다:

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 뒤에는 `Laravel\Paddle\Cashier` 클래스를 통해 Cashier에 사용자 정의 모델을 알릴 수 있습니다. 보통 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다:

```
use App\Models\Cashier\Receipt;
use App\Models\Cashier\Subscription;

/**
 * Bootstrap any application services.
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

Paddle은 구독 상태 변경을 위한 CRUD API가 부족하기 때문에, 대부분의 상호작용은 Paddle의 [체크아웃 위젯](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout)으로 처리됩니다. 체크아웃 위젯을 표시하려면 먼저 Cashier를 사용해 "결제 링크"를 생성해야 하는데, 이 링크는 위젯에 어떤 결제 작업을 수행할지 알려줍니다:

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

Cashier는 `paddle-button` [Blade 컴포넌트](/docs/9.x/blade#components)도 제공합니다. 결제 링크 URL을 이 컴포넌트에 전달하면, 버튼 클릭 시 Paddle 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle의 스타일이 적용된 버튼이 생성됩니다. `data-theme="none"` 속성을 넣으면 Paddle 스타일을 제거할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기로 동작합니다. 구독 생성 또는 변경 후 Paddle은 웹훅을 보내 애플리케이션 데이터베이스에 구독 상태를 업데이트할 수 있게 하므로, 반드시 [웹훅 설정](#handling-paddle-webhooks)을 완료해야 합니다.

결제 링크에 관한 자세한 내용은 [Paddle 결제 링크 생성 관련 API 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

> [!WARNING]
> 구독 상태가 변경된 후 웹훅 수신까지 지연이 거의 없지만, 실제로는 미세한 시차가 있을 수 있으니, 사용자가 결제를 마친 직후에 구독이 즉시 활성화되어 있지 않을 수도 있음을 애플리케이션에서 유념하세요.

<a name="manually-rendering-pay-links"></a>
#### 수동으로 결제 링크 렌더링하기

Laravel Blade 컴포넌트를 사용하지 않고도 결제 링크를 직접 렌더링할 수 있습니다. 위 예제처럼 결제 링크 URL을 생성한 다음:

```
$payLink = $request->user()->newSubscription('default', $premium = 34567)
    ->returnTo(route('home'))
    ->create();
```

HTML 내에서 `a` 태그에 링크를 붙여넣으면 됩니다:

```
<a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
    Paddle Checkout
</a>
```

<a name="payments-requiring-additional-confirmation"></a>
#### 추가 확인이 필요한 결제

때때로 결제 확인을 위해 추가 인증 절차가 필요할 수 있습니다. Paddle에서는 은행이나 카드 발급사의 결제 흐름에 따라 카드 확인, 소액 임시 청구, 별도 장치 인증 등 여러 검증 과정을 표시할 수 있습니다.

<a name="inline-checkout"></a>
### 인라인 체크아웃

Paddle의 "오버레이" 방식 체크아웃이 불편하다면, 인라인으로 위젯을 표시하는 옵션도 제공합니다. 이 방식은 체크아웃 HTML 필드를 조정할 수 없지만 애플리케이션 내에 위젯을 직접 삽입할 수 있는 장점이 있습니다.

Cashier는 인라인 체크아웃을 쉽게 구현할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. 먼저 [결제 링크](#pay-links)를 생성하고, 컴포넌트에 `override` 속성으로 전달하면 됩니다:

```blade
<x-paddle-checkout :override="$payLink" class="w-full" />
```

컴포넌트 높이는 `height` 속성으로 지정할 수 있습니다:

```blade
<x-paddle-checkout :override="$payLink" class="w-full" height="500" />
```

<a name="inline-checkout-without-pay-links"></a>
#### 결제 링크 없이 인라인 체크아웃 사용하기

결제 링크 대신에 커스텀 옵션을 통해 위젯을 조정할 수 있습니다:

```blade
@php
$options = [
    'product' => $productId,
    'title' => 'Product Title',
];
@endphp

<x-paddle-checkout :options="$options" class="w-full" />
```

인라인 체크아웃의 옵션에 관한 자세한 내용은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout)와 [파라미터 참고 문서](https://developer.paddle.com/reference/paddle-js/parameters)를 참고하세요.

> [!WARNING]
> `passthrough` 옵션을 커스텀 옵션에 포함할 경우, 키-값 배열을 전달해야 하며, Cashier가 자동으로 JSON 문자열로 변환해 줍니다. `customer_id` passthrough 옵션은 Cashier 내부에서 예약되어 있으니 주의하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

Laravel Blade 컴포넌트를 사용하지 않고도 인라인 체크아웃을 수동으로 렌더링할 수 있습니다. 우선 [결제 링크 생성](#pay-links) 예제처럼 링크 URL을 얻은 뒤, Paddle.js를 이용해 체크아웃 위젯을 초기화하세요. 아래 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용한 간단한 예시입니다만, 원하는 프런트엔드 스택으로 응용할 수 있습니다:

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

Stripe와 달리 Paddle 사용자 ID는 Paddle 전체에서 고유하며, 개별 Paddle 계정별로 구분되지 않습니다. 때문에 Paddle API는 사용자의 이메일 주소 등 상세 정보를 업데이트하는 기능을 제공하지 않습니다. 결제 링크 생성 시 Paddle은 `customer_email`로 사용자를 식별하며, 이 이메일을 기존 사용자와 매칭하려고 시도합니다.

이로 인해 Cashier와 Paddle 사용 시에는 중요한 점이 있습니다. 구독이 같은 애플리케이션 사용자에 연결되었더라도 **Paddle 내부 시스템에서는 서로 다른 사용자에 연결되어 있을 수 있습니다**. 구독별로 결제 수단과 이메일 주소도 다를 수 있습니다(구독 생성 시 할당된 이메일에 따라 다름).

따라서 구독 정보를 표시할 때는 구독별로 연결된 이메일 주소나 결제 수단 정보를 반드시 사용자에게 알려야 합니다. `Laravel\Paddle\Subscription` 모델에서 다음 메서드로 정보를 가져올 수 있습니다:

```
$subscription = $user->subscription('default');

$subscription->paddleEmail();
$subscription->paymentMethod();
$subscription->cardBrand();
$subscription->cardLastFour();
$subscription->cardExpirationDate();
```

현재 Paddle API를 통해 사용자의 이메일을 직접 변경할 수 없습니다. 사용자가 이메일 주소를 수정하려면 Paddle 고객 지원에 연락해, 변경하고자 하는 대상 구독의 `paddleEmail` 값을 제공해야 합니다.

<a name="prices"></a>
## 가격

Paddle은 국가별로 다른 통화를 사용해 가격을 맞춤 설정할 수 있습니다. Cashier Paddle은 `productPrices` 메서드를 통해 특정 상품의 모든 가격을 조회할 수 있습니다. 상품 ID 배열을 인수로 전달하세요:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456]);
```

통화는 요청의 IP 주소를 기준으로 결정되지만, 특정 국가를 명시해 가격을 조회할 수도 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);
```

조회한 가격은 자유롭게 출력할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

세전 가격과 세금을 분리해 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

구독 플랜 가격의 초기 가격과 반복 가격을 따로 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

자세한 내용은 [Paddle 가격 API 문서](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)를 참고하세요.

<a name="prices-customers"></a>
#### 고객별 가격

이미 고객 등록이 된 사용자가 해당 고객에게 적용되는 가격을 보고 싶다면, 고객 인스턴스에서 직접 가격을 조회할 수 있습니다:

```
use App\Models\User;

$prices = User::find(1)->productPrices([123, 456]);
```

구현상 Cashier는 사용자의 [`paddleCountry` 메서드](#customer-defaults)를 참조하여 해당 국가 통화로 가격을 선택합니다. 예를 들어 미국 사용자는 USD, 벨기에 사용자는 EUR 가격을 보게 됩니다. 만약 통화가 일치하지 않으면 상품의 기본 통화 가격이 사용됩니다. Paddle 제어판에서 상품 또는 구독 플랜의 가격 설정을 언제든 수정할 수 있습니다.

<a name="prices-coupons"></a>
#### 쿠폰 할인 가격 표시

`productPrices` 메서드 호출 시 쿠폰 코드를 콤마로 구분한 문자열로 전달해 할인된 가격을 계산할 수 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices([123, 456], [
    'coupons' => 'SUMMERSALE,20PERCENTOFF'
]);
```

조회한 가격은 `price` 메서드를 통해 표시하세요:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

원래 가격(쿠폰 할인 제외)은 `listPrice` 메서드로 출력할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> [!WARNING]
> 가격 API를 사용할 때 쿠폰은 일회성 상품에만 적용되며, 구독 플랜에는 적용되지 않습니다.

<a name="customers"></a>
## 고객

<a name="customer-defaults"></a>
### 고객 기본값

Cashier는 결제 링크 생성 시 고객 이메일, 국가, 우편번호 등의 기본값을 미리 채울 수 있도록 도와줍니다. Billable 모델에서 다음 메서드를 오버라이딩해 기본값을 정의하세요:

```
/**
 * Paddle에 연결할 고객 이메일을 반환합니다.
 *
 * @return string|null
 */
public function paddleEmail()
{
    return $this->email;
}

/**
 * Paddle에 연결할 고객 국가 코드를 반환합니다.
 *
 * 2자리 알파벳 코드여야 합니다. 지원 국가 목록은 아래 링크를 참고하세요.
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
 * 일부 국가에서는 필요합니다. 지원 국가 목록은 아래 링크를 참고하세요.
 *
 * @return string|null
 * @link https://developer.paddle.com/reference/platform-parameters/supported-countries#countries-requiring-postcode
 */
public function paddlePostcode()
{
    //
}
```

이 기본값은 Cashier에서 결제 링크를 생성하는 모든 작업에 사용됩니다.

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면, 우선 데이터베이스에서 Billable 모델 인스턴스(보통 `App\Models\User`)를 얻으세요. 그런 다음 `newSubscription` 메서드를 사용해 구독 결제 링크를 만듭니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $request->user()->newSubscription('default', $premium = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

`newSubscription`의 첫 번째 인수는 구독 내부 식별명입니다. 애플리케이션에 구독이 하나뿐이라면 보통 `default` 또는 `primary`라 부릅니다. 이 이름은 내부용으로만 사용되며 사용자에게 표시되면 안됩니다. 또한 공백을 포함하지 않고, 생성 후 변경하지 않아야 합니다.

두 번째 인수는 사용자가 구독할 특정 Paddle 플랜 식별자입니다. `returnTo` 메서드는 결제가 완료된 후 사용자를 리디렉션할 URL을 받습니다.

`create` 메서드는 결제 링크를 생성하며, 이는 이후 결제 버튼 생성에 사용됩니다. 버튼은 Cashier Paddle에 포함된 `paddle-button` [Blade 컴포넌트](/docs/9.x/blade#components)로 쉽게 생성할 수 있습니다:

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

사용자가 결제를 마치면 Paddle에서 `subscription_created` 웹훅을 보내고, Cashier가 이를 받아 고객 구독을 설정합니다. 웹훅 설정이 제대로 되어 있어야 모든 웹훅이 정상 처리됩니다.

<a name="additional-details"></a>
#### 추가 정보

추가 고객 또는 구독 정보를 전달하고 싶으면, `create` 메서드에 키/값 배열을 인수로 전달하세요. Paddle의 [결제 링크 생성 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)에서 지원하는 필드를 확인할 수 있습니다:

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->create([
        'vat_number' => $vatNumber,
    ]);
```

<a name="subscriptions-coupons"></a>
#### 쿠폰

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요:

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withCoupon('code')
    ->create();
```

<a name="metadata"></a>
#### 메타데이터

추가 데이터를 전달하고 싶다면 `withMetadata` 메서드를 사용할 수 있습니다:

```
$payLink = $user->newSubscription('default', $monthly = 12345)
    ->returnTo(route('home'))
    ->withMetadata(['key' => 'value'])
    ->create();
```

> [!WARNING]
> 메타데이터 키로 `subscription_name`은 피하세요. 이 키는 Cashier 내부에서 사용됩니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 구독 중인지 확인할 때는 여러 편리한 메서드가 있습니다. 우선 `subscribed` 메서드는 사용자가 구독 중이거나, 구독 체험 기간 중이면 `true`를 반환합니다:

```
if ($user->subscribed('default')) {
    //
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/9.x/middleware)와 함께 사용하면, 구독 상태에 따라 접근을 제한할 때 매우 유용합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 결제 중인 고객이 아님...
            return redirect('billing');
        }

        return $next($request);
    }
}
```

사용자가 체험 기간인지 확인하려면 `onTrial` 메서드를 사용하세요. 이는 사용자가 체험 기간 내임을 알리는 경고 표시 등에서 유용합니다:

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

`subscribedToPlan` 메서드는 특정 Paddle 플랜 ID를 사용자가 구독 중인지 확인합니다. 예를 들어, 다음은 사용자의 `default` 구독이 월간 플랜에 구독 중인지 판단합니다:

```
if ($user->subscribedToPlan($monthly = 12345, 'default')) {
    //
}
```

플랜 여러 개를 배열로 넘기면, 하나라도 구독 중인지 확인할 수 있습니다:

```
if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
    //
}
```

`recurring` 메서드는 사용자가 현재 구독 중이며, 체험 기간이 끝난 상태인지 확인합니다:

```
if ($user->subscription('default')->recurring()) {
    //
}
```

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

이전에 구독 중이었으나 취소한 경우에는 `cancelled` 메서드를 사용해 확인할 수 있습니다:

```
if ($user->subscription('default')->cancelled()) {
    //
}
```

사용자가 구독을 취소했지만 구독 만료일까지 유예 기간에 있다면(`grace period`), `onGracePeriod` 메서드는 `true`를 반환합니다. 예를 들어 3월 5일에 취소했고 구독은 3월 10일 만료일 경우, 3월 10일까지는 `subscribed` 메서드가 `true`를 유지합니다:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

유예 기간도 끝나 완전히 구독이 종료된 경우는 `ended` 메서드로 확인할 수 있습니다:

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="past-due-status"></a>
#### 연체 상태

결제가 실패하면 구독은 `past_due` 상태가 됩니다. 이 상태에서는 사용자가 결제 정보를 갱신해야 구독이 활성화됩니다. 상태 확인은 `pastDue` 메서드로 할 수 있습니다:

```
if ($user->subscription('default')->pastDue()) {
    //
}
```

연체 상태에서는 사용자가 [결제 정보 갱신](#updating-payment-information)을 하도록 안내해야 합니다. 연체 구독 처리 방식은 [Paddle 구독 설정](https://vendors.paddle.com/subscription-settings)에서 조정할 수 있습니다.

`past_due` 상태의 구독도 계속 활성 상태로 간주하려면, Cashier의 `keepPastDueSubscriptionsActive` 메서드를 사용하세요. 보통 앱의 `AppServiceProvider` `register` 메서드에서 호출합니다:

```
use Laravel\Paddle\Cashier;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]
> `past_due` 상태인 구독은 결제 정보가 업데이트될 때까지 변경할 수 없으므로, `swap`이나 `updateQuantity` 메서드는 예외를 던집니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

주요 구독 상태는 쿼리 스코프로도 제공되어, 상태별 구독을 쉽게 조회할 수 있습니다:

```
// 활성 구독 모두 조회...
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자의 취소된 구독 모두 조회...
$subscriptions = $user->subscriptions()->cancelled()->get();
```

사용 가능한 전체 스코프 목록은 다음과 같습니다:

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
### 구독 단일 청구

구독자에게 구독 외에 일회성 요금을 청구하려면 구독 인스턴스의 `charge` 메서드를 사용하세요:

```
$response = $user->subscription('default')->charge(12.99, 'Support Add-on');
```

[단일 청구](#single-charges)와 달리 이 메서드는 즉시 구독에 연결된 결제 수단에서 요금을 청구합니다. 금액은 항상 구독 통화 기준으로 지정해야 합니다.

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별로 하나의 결제 수단을 저장합니다. 기본 결제 수단을 변경하려면 구독 모델의 `updateUrl` 메서드로 "업데이트 URL"을 생성하세요:

```
use App\Models\User;

$user = User::find(1);

$updateUrl = $user->subscription('default')->updateUrl();
```

생성된 URL과 `paddle-button` Blade 컴포넌트를 사용해 사용자가 Paddle 결제 위젯을 실행하고 결제 정보를 갱신할 수 있습니다:

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

결제 정보 갱신이 완료되면 Paddle에서 `subscription_updated` 웹훅을 보내고, 구독 정보가 데이터베이스에 반영됩니다.

<a name="changing-plans"></a>
### 플랜 변경

사용자가 구독 플랜을 변경하려면, 해당 Paddle 플랜의 식별자를 `swap` 메서드에 전달합니다:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap($premium = 34567);
```

변경 즉시 청구서 발행을 원하면 `swapAndInvoice` 메서드를 사용하세요:

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice($premium = 34567);
```

> [!WARNING]
> 체험 기간 도중에는 플랜 변경이 불가능합니다. 자세한 제한 사항은 [Paddle 문서](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes)를 참고하세요.

<a name="prorations"></a>
#### 비례 청구 설정

기본적으로 Paddle은 플랜 변경 시 요금을 일할 계산(proration)합니다. 비례 청구 없이 변경하려면 `noProrate` 메서드를 앞에 호출하세요:

```
$user->subscription('default')->noProrate()->swap($premium = 34567);
```

<a name="subscription-quantity"></a>
### 구독 수량

구독에 수량이 적용되는 경우도 있습니다. 예를 들어 프로젝트 관리 앱에서 프로젝트별 월 $10을 청구하는 경우입니다. 수량을 증가, 감소하려면 각각 `incrementQuantity`, `decrementQuantity` 메서드를 사용하세요:

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 5 증가
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 5 감소
$user->subscription('default')->decrementQuantity(5);
```

특정 수량으로 설정하려면 `updateQuantity` 메서드를 쓰세요:

```
$user->subscription('default')->updateQuantity(10);
```

`noProrate` 메서드로 수량 변경 시 비례 청구 없이 업데이트할 수도 있습니다:

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

<a name="subscription-modifiers"></a>
### 구독 수식어

수식어는 [사용량 기반 청구](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers) 구현이나 애드온 확장에 활용됩니다.

예를 들어 "프리미엄 지원" 애드온을 추가하려면 이렇게 만듭니다:

```
$modifier = $user->subscription('default')->newModifier(12.99)->create();
```

기본적으로 수식어는 구독의 각 청구 주기마다 반복 청구됩니다. 읽기 쉬운 설명도 추가할 수 있습니다:

```
$modifier = $user->subscription('default')->newModifier(12.99)
    ->description('Premium Support')
    ->create();
```

사용량 기반 청구 예시로 SMS 메시지당 요금을 부과한다고 가정하면, Paddle 대시보드에 $0 플랜을 만들어야 합니다. 사용자 구독 후, SMS별 수식어를 추가합니다:

```
$modifier = $user->subscription('default')->newModifier(0.99)
    ->description('New text message')
    ->oneTime()
    ->create();
```

위 예시에서 `oneTime` 메서드를 호출했는데, 이는 이 수식어가 한 번만 청구되며 반복되지 않도록 합니다.

<a name="retrieving-modifiers"></a>
#### 수식어 조회

구독에 연결된 모든 수식어는 `modifiers` 메서드로 불러올 수 있습니다:

```
$modifiers = $user->subscription('default')->modifiers();

foreach ($modifiers as $modifier) {
    $modifier->amount(); // $0.99
    $modifier->description; // New text message.
}
```

<a name="deleting-modifiers"></a>
#### 수식어 삭제

`Laravel\Paddle\Modifier` 인스턴스에서 `delete` 메서드를 호출하면 수식어를 삭제할 수 있습니다:

```
$modifier->delete();
```

<a name="multiple-subscriptions"></a>
### 다중 구독

Paddle은 고객이 여러 구독을 동시에 가질 수 있습니다. 예를 들어 체육관에서 수영과 웨이트 트레이닝 구독을 별도로 운영하는 경우입니다.

구독 생성 시 `newSubscription`에 구독 이름을 임의로 지정할 수 있습니다. 이 이름은 구독 유형을 구분짓습니다:

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()
        ->newSubscription('swimming', $swimmingMonthly = 12345)
        ->create($request->paymentMethodId);

    // ...
});
```

수영 구독 외에 연간 구독으로 바꾸려면 해당 구독에 대해 `swap` 메서드를 호출하면 됩니다:

```
$user->subscription('swimming')->swap($swimmingYearly = 34567);
```

물론 구독 취소도 가능합니다:

```
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시중지

구독을 일시중지하려면 구독의 `pause` 메서드를 호출하세요:

```
$user->subscription('default')->pause();
```

구독이 일시중지되면 Cashier는 DB의 `paused_from` 컬럼을 자동으로 설정합니다. 이 컬럼은 언제 `paused` 메서드가 `true`를 반환해야 하는지 판단하는 데 쓰입니다. 예를 들어, 고객이 3월 1일에 일시중지했더라도, 구독이 3월 5일에 갱신 예정이라면 3월 5일까지는 `paused`가 `false`를 유지합니다. 이는 보통 청구 주기까지는 서비스를 계속 사용할 수 있도록 하기 위함입니다.

일시중지된 구독이 유예 기간에 있는지 `onPausedGracePeriod` 메서드로 확인할 수 있습니다:

```
if ($user->subscription('default')->onPausedGracePeriod()) {
    //
}
```

일시중지 해제는 `unpause` 메서드를 호출하세요:

```
$user->subscription('default')->unpause();
```

> [!WARNING]
> 구독이 일시중지 상태에서는 플랜 변경이나 수량 업데이트가 불가능합니다. 변경하려면 먼저 구독을 재개해야 합니다.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 `cancel` 메서드를 호출하세요:

```
$user->subscription('default')->cancel();
```

구독 취소 시 Cashier는 `ends_at` 컬럼을 설정합니다. 이를 토대로 `subscribed` 메서드는 구독 종료일 전까지 `true`를 반환합니다. 예를 들어 사용자가 3월 1일에 취소해도 만료일인 3월 5일까지는 구독이 활성 상태로 간주됩니다.

취소 후 유예 기간에 있는지 `onGracePeriod` 메서드로 확인할 수 있습니다:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

즉시 취소하려면 `cancelNow` 메서드를 사용하세요:

```
$user->subscription('default')->cancelNow();
```

> [!WARNING]
> Paddle은 구독이 완전히 취소된 후에는 재개할 수 없습니다. 다시 구독하려면 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간

<a name="with-payment-method-up-front"></a>
### 결제 정보 선입력 시

> [!WARNING]
> 결제 정보를 미리 수집하면서 체험 기간 중일 때는 Paddle이 플랜 변경이나 수량 업데이트를 막습니다. 사용자가 체험 기간 중 플랜을 변경하려면 구독을 취소 후 새로 만들어야 합니다.

결제 정보 수집과 함께 체험 기간을 제공하려면, 구독 결제 링크 생성 시 `trialDays` 메서드로 체험 기간 일수를 지정하세요:

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

이 메서드는 데이터베이스 내 구독 레코드의 체험 종료일을 설정하고, Paddle로 하여금 체험 기간 전까지 과금하지 않도록 지시합니다.

> [!WARNING]
> 체험 종료일 전에 구독을 취소하지 않으면, 체험 종료 즉시 과금되니 사용자에게 반드시 종료일을 알려주세요.

사용자가 체험 중인지 확인하려면 `User` 또는 구독 인스턴스의 `onTrial` 메서드를 사용하세요:

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

기존 체험 기간이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용합니다:

```
if ($user->hasExpiredTrial('default')) {
    //
}

if ($user->subscription('default')->hasExpiredTrial()) {
    //
}
```

<a name="defining-trial-days-in-paddle-cashier"></a>
#### Paddle / Cashier에서 체험 기간 정의

Paddle 대시보드에서 플랜별 체험 일수를 설정하거나, 항상 Cashier에서 명시적으로 전달할 수 있습니다. Paddle에서 플랜의 체험 일수를 설정한 경우, 새 구독이 생성될 때마다 체험 기간이 할당됩니다(과거 구독이 있어도 동일). 단, 체험 기간 없이 생성하려면 `trialDays(0)`을 호출해야 합니다.

<a name="without-payment-method-up-front"></a>
### 결제 정보 미선입력 시

결제 정보를 미리 수집하지 않고 체험 기간만 제공하려면, 사용자의 Billable 고객 기록에 `trial_ends_at` 컬럼을 원하는 종료일로 설정하세요. 보통 회원가입 시 처리합니다:

```
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

이런 체험을 "일반 체험(generic trial)"이라 부릅니다. `User` 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 이전이면 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 체험 기간 중임...
}
```

구독 생성 시에는 평소와 같이 `newSubscription`을 사용하세요:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create();

    return view('billing', ['payLink' => $payLink]);
});
```

체험 종료일을 조회하려면 `trialEndsAt` 메서드를 사용합니다. 체험 중이면 Carbon 날짜 인스턴스를, 아니면 `null`을 반환합니다. 특정 구독명을 지정할 수도 있습니다:

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

사용자가 아직 실제 구독을 생성하지 않은 "일반 체험"인지 구분하려면 `onGenericTrial` 메서드를 사용하세요:

```
if ($user->onGenericTrial()) {
    // 일반 체험 기간 중임...
}
```

> [!WARNING]
> Paddle 구독이 생성된 후 체험 기간을 연장하거나 변경하는 방법은 없습니다.

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리

Paddle은 다양한 이벤트를 웹훅으로 통지할 수 있습니다. 기본적으로 Cashier 서비스 프로바이더가 Cashier 웹훅 컨트롤러를 라우트에 등록하며, 이 컨트롤러가 들어오는 웹훅을 처리합니다.

컨트롤러는 기본적으로 결제 실패에 따른 구독 취소 처리, 구독 업데이트, 결제 수단 변경 등을 자동으로 처리합니다. 그러나 필요하다면 원하는 Paddle 웹훅 이벤트를 직접 다룰 수 있도록 확장할 수 있습니다.

Paddle 대시보드에서 웹훅 URL을 반드시 설정하세요. 기본값은 `/paddle/webhook` 경로입니다. Paddle 제어판에서 다음 웹훅들을 모두 활성화하는 것이 좋습니다:

- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded

> [!WARNING]
> Cashier가 제공하는 [웹훅 서명 검증 미들웨어](/docs/9.x/cashier-paddle#verifying-webhook-signatures)로 수신 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅 & CSRF 보호 예외 설정

Paddle 웹훅은 Laravel의 [CSRF 보호](/docs/9.x/csrf)를 우회해야 하므로, `App\Http\Middleware\VerifyCsrfToken` 미들웨어에서 해당 URI를 예외 처리하거나 `web` 미들웨어 그룹에서 뺍니다:

```
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
#### 웹훅 & 로컬 개발

로컬 개발 중에도 Paddle이 웹훅을 보내려면, [Ngrok](https://ngrok.com/) 또는 [Expose](https://expose.dev/docs/introduction) 같은 사이트 공유 도구를 사용해 외부 접속이 가능해야 합니다. Laravel Sail을 쓴다면 [Sail의 사이트 공유 명령어](/docs/9.x/sail#sharing-your-site)를 활용하세요.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 결제 실패 시 구독 취소 등 주요 Paddle 웹훅 처리를 자동으로 합니다. 추가 이벤트를 다루려면 Cashier가 발생시키는 다음 이벤트를 구독하세요:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` 이벤트를 처리하려면 다음처럼 이벤트 리스너를 정의합니다:

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * 수신된 Paddle 웹훅 처리.
     *
     * @param  \Laravel\Paddle\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'payment_succeeded') {
            // 이벤트 처리 코드 작성...
        }
    }
}
```

작성한 리스너는 애플리케이션 `EventServiceProvider`에 등록해야 합니다:

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

Cashier는 웹훅 유형별 이벤트도 따로 제공합니다. 이들은 Paddle에서 받은 전체 페이로드와 함께, 웹훅 처리에 사용된 관련 모델들(빌러블 모델, 구독, 영수증 등)을 포함합니다:

- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

웹훅 기본 라우트는 `.env` 파일의 `CASHIER_WEBHOOK` 변수로 재정의할 수 있습니다. 이 값은 Paddle 대시보드 설정과 일치하는 전체 URL이어야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안을 위해 [Paddle 웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 활용할 수 있습니다. Cashier는 들어오는 웹훅 요청 유효성을 검사하는 미들웨어를 기본 제공하므로 편리합니다.

웹훅 서명 검증을 사용하려면 `.env`에 `PADDLE_PUBLIC_KEY`를 반드시 설정하세요. 공개키는 Paddle 계정에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 청구

<a name="simple-charge"></a>
### 간단한 청구

고객에게 일회성 청구를 하려면 Billable 모델의 `charge` 메서드를 사용해 결제용 링크를 생성하세요. 첫 번째 인수는 청구 금액, 두 번째 인수는 청구 설명입니다:

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $user->charge(12.99, 'Action Figure')
    ]);
});
```

결제 링크를 생성한 뒤에는 Cashier의 `paddle-button` Blade 컴포넌트로 사용자가 Paddle 위젯을 띄우고 결제를 완료할 수 있도록 합니다:

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`charge` 메서드의 세 번째 인수로 옵션 배열도 전달 가능하며, Paddle 문서에서 자세한 옵션을 확인할 수 있습니다:

```
$payLink = $user->charge(12.99, 'Action Figure', [
    'custom_option' => $value,
]);
```

청구는 `cashier.currency` 설정에 지정된 통화로 이루어지며, 기본값은 USD입니다. `.env`의 `CASHIER_CURRENCY` 변수로 기본 통화를 바꿀 수 있습니다:

```ini
CASHIER_CURRENCY=EUR
```

Paddle 동적 가격 매칭 시스템을 이용해 통화별 가격을 다르게 설정할 수도 있습니다. 이 경우 고정 금액 대신 가격 배열을 넘깁니다:

```
$payLink = $user->charge([
    'USD:19.99',
    'EUR:15.99',
], 'Action Figure');
```

<a name="charging-products"></a>
### 상품 청구

Paddle에 미리 등록된 특정 상품에 대해 일회성 청구를 만들려면 Billable 모델의 `chargeProduct` 메서드를 사용해 결제 링크를 생성하세요:

```
use Illuminate\Http\Request;

Route::get('/store', function (Request $request) {
    return view('store', [
        'payLink' => $request->user()->chargeProduct($productId = 123)
    ]);
});
```

생성한 결제 링크는 `paddle-button` 컴포넌트에 전달해 사용자가 Paddle 위젯을 실행하도록 할 수 있습니다:

```blade
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

옵션 배열도 두 번째 인수로 전달 가능합니다:

```
$payLink = $user->chargeProduct($productId, [
    'custom_option' => $value,
]);
```

옵션은 Paddle 문서에서 확인하세요.

<a name="refunding-orders"></a>
### 주문 환불

Paddle 주문을 환불하려면 `refund` 메서드를 사용합니다. 첫 인수로 Paddle 주문 ID를 받아야 합니다. 특정 Billable 모델의 영수증은 `receipts` 메서드로 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$receipt = $user->receipts()->first();

$refundRequestId = $user->refund($receipt->order_id);
```

환불 금액과 환불 사유를 지정할 수도 있습니다:

```
$receipt = $user->receipts()->first();

$refundRequestId = $user->refund(
    $receipt->order_id, 5.00, 'Unused product time'
);
```

> [!NOTE]
> `$refundRequestId`를 Paddle 지원팀과 환불 관련 문의 시 참고용으로 사용할 수 있습니다.

<a name="receipts"></a>
## 영수증

Billable 모델 인스턴스의 영수증 목록은 `receipts` 속성으로 쉽게 가져올 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$receipts = $user->receipts;
```

영수증 목록을 테이블 등으로 나열할 때는 영수증 인스턴스의 메서드를 활용해 결제일, 금액, 영수증 다운로드 링크 등을 표시하세요:

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
### 과거 및 다가오는 결제

구독 과거 결제와 다음 결제를 조회하려면 `lastPayment`와 `nextPayment` 메서드를 사용하세요:

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription('default');

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 `Laravel\Paddle\Payment` 인스턴스를 반환하며, `nextPayment`는 청구 주기가 종료됐으면 `null`을 반환합니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="handling-failed-payments"></a>
## 실패한 결제 처리

구독 결제가 실패하는 사례는 카드 만료, 한도 부족 등 여러 가지입니다. 이런 경우 Paddle이 자동 결제 실패 이메일을 보내도록 [Paddle 대시보드에서 설정](https://vendors.paddle.com/subscription-settings)하는 것을 권장합니다.

직접 세밀한 처리를 원한다면, Cashier가 전송하는 `WebhookReceived` 이벤트 내에서 `subscription_payment_failed` 이벤트를 수신해 처리할 수 있습니다. 또한 Paddle 웹훅 설정에서 "Subscription Payment Failed" 항목을 활성화해야 합니다:

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * 수신된 Paddle 웹훅 처리.
     *
     * @param  \Laravel\Paddle\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['alert_name'] === 'subscription_payment_failed') {
            // 실패한 결제 처리...
        }
    }
}
```

정의한 리스너는 `EventServiceProvider`에 등록하세요:

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

<a name="testing"></a>
## 테스트

통합을 검증하려면, 수동으로 모든 결제 흐름을 테스트하는 것을 권장합니다.

자동화 테스트 및 CI 환경에서는 [Laravel HTTP 클라이언트](/docs/9.x/http-client#testing)로 Paddle API 호출을 모킹할 수 있습니다. 실제 Paddle 응답을 테스트할 수는 없지만, 애플리케이션 내 API 호출 예상을 검증하는 데 유용합니다.