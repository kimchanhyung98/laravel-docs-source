# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
    - [데이터베이스 마이그레이션](#database-migrations)
- [설정](#configuration)
    - [청구 대상 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
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
    - [구독 단일 결제](#subscription-single-charges)
    - [결제 정보 변경](#updating-payment-information)
    - [상품 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [구독 수정자](#subscription-modifiers)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#cancelling-subscriptions)
- [구독 체험](#subscription-trials)
    - [결제 수단 미리 받기](#with-payment-method-up-front)
    - [결제 수단 없이 시작](#without-payment-method-up-front)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단 결제](#simple-charge)
    - [상품 결제](#charging-products)
    - [주문 환불](#refunding-orders)
- [영수증](#receipts)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [실패한 결제 처리](#handling-failed-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)는 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 직관적이고 유연한 인터페이스를 제공합니다. 구독 결제와 관련된 반복적인 코드를 거의 모두 처리해주며, 기본적인 구독 관리뿐 아니라 쿠폰, 구독 변경, 구독 "수량", 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier를 사용할 때는 Paddle의 [사용자 가이드](https://developer.paddle.com/guides)와 [API 문서](https://developer.paddle.com/api-reference/intro)도 함께 참고하시길 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새로운 버전으로 업그레이드할 때에는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용하여 Paddle 용 Cashier 패키지를 설치하세요:

    composer require laravel/cashier-paddle

> {note} Cashier가 모든 Paddle 이벤트를 제대로 처리하도록 하려면 반드시 [Cashier의 웹훅 처리 설정](#handling-paddle-webhooks)을 해주세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 및 스테이징 개발 시 [Paddle 샌드박스 계정](https://developer.paddle.com/getting-started/sandbox)을 등록해야 합니다. 샌드박스 계정을 통해 실제 결제 없이 애플리케이션을 테스트할 수 있습니다. 결제 시나리오 테스트를 위해서는 Paddle의 [테스트 카드 번호](https://developer.paddle.com/getting-started/sandbox#test-cards)를 사용할 수 있습니다.

샌드박스 환경을 사용할 때는 애플리케이션의 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정하세요:

PADDLE_SANDBOX=true

개발이 끝나면 [Paddle 판매자 계정](https://paddle.com)에 신청할 수 있습니다.

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션

Cashier 서비스 제공자(Service Provider)는 자체 데이터베이스 마이그레이션 디렉터리를 등록합니다. 패키지 설치 후에는 데이터베이스 마이그레이션을 꼭 실행하세요. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성하며, 고객 구독 정보를 저장하는 `subscriptions` 테이블과 영수증 정보를 저장하는 `receipts` 테이블도 함께 생성합니다:

    php artisan migrate

Cashier에 포함된 마이그레이션을 오버라이드해야 할 경우에는 `vendor:publish` Artisan 명령을 사용해 마이그레이션을 퍼블리시할 수 있습니다:

    php artisan vendor:publish --tag="cashier-migrations"

Cashier의 마이그레이션 자체 실행을 막고 싶다면 Cashier가 제공하는 `ignoreMigrations`를 사용하세요. 일반적으로는 `AppServiceProvider`의 `register` 메소드에서 호출합니다:

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

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 대상 모델

Cashier를 사용하기 전에 반드시 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 정보 갱신 등 다양한 청구 관련 메소드를 제공합니다.

    use Laravel\Paddle\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

사용자 이외의 청구 가능한 엔티티에도 동일하게 트레이트를 추가할 수 있습니다:

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Paddle\Billable;

    class Team extends Model
    {
        use Billable;
    }

<a name="api-keys"></a>
### API 키

다음으로, Paddle 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Paddle API 키는 Paddle 콘솔 패널에서 확인할 수 있습니다:

    PADDLE_VENDOR_ID=your-paddle-vendor-id
    PADDLE_VENDOR_AUTH_CODE=your-paddle-vendor-auth-code
    PADDLE_PUBLIC_KEY="your-paddle-public-key"
    PADDLE_SANDBOX=true

샌드박스 환경을 사용할 때는 `PADDLE_SANDBOX` 값을 `true`로, 프로덕션에 배포할 때는 `false`로 설정하세요.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 자체 JavaScript 라이브러리를 통해 결제 위젯을 초기화합니다. Blade 레이아웃의 `</head>` 닫는 태그 바로 전에 `@paddleJS` 디렉티브를 추가하면 라이브러리를 불러올 수 있습니다:

    <head>
        ...

        @paddleJS
    </head>

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 다른 통화로 변경하려면 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 정의하세요:

    CASHIER_CURRENCY=EUR

또한, 송장 등에서 금액 표시에 사용할 로케일을 설정하려면 다음처럼 `CASHIER_CURRENCY_LOCALE`을 지정하세요:

    CASHIER_CURRENCY_LOCALE=nl_BE

> {note} `en` 이외의 로케일을 사용하려면 PHP의 `ext-intl` 확장 모듈이 서버에 설치 및 구성되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier가 내부적으로 사용하는 모델을 확장하고 싶다면, 직접 모델을 정의하고 Cashier 모델을 상속하세요:

    use Laravel\Paddle\Subscription as CashierSubscription;

    class Subscription extends CashierSubscription
    {
        // ...
    }

이후 `Laravel\Paddle\Cashier`를 통해 Cashier에게 커스텀 모델을 사용하도록 알릴 수 있습니다. 일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메소드에서 지정합니다:

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

<a name="core-concepts"></a>
## 핵심 개념

<a name="pay-links"></a>
### 결제 링크

Paddle은 구독 상태 변경을 위한 방대한 CRUD API를 제공하지 않습니다. 따라서 대부분의 상호작용은 [체크아웃 위젯](https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout)을 통해 이루어지며, 체크아웃 위젯을 표시하려면 Cashier로 "결제 링크(pay link)"를 생성해야 합니다. 결제 링크는 어떤 청구 작업을 할지 Paddle에 알립니다.

    use App\Models\User;
    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $request->user()->newSubscription('default', $premium = 34567)
            ->returnTo(route('home'))
            ->create();

        return view('billing', ['payLink' => $payLink]);
    });

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/{{version}}/blade#components)가 포함되어 있습니다. 결제 링크 URL을 "prop"으로 전달해 버튼을 만들 수 있습니다. 클릭 시 Paddle 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle 스타일이 적용된 버튼이 표시됩니다. Paddle 스타일을 모두 제거하려면 `data-theme="none"` 속성을 추가하세요:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="none">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기식입니다. 사용자가 체크아웃에서 구독을 생성하거나 수정하면, Paddle이 웹훅을 통해 상태 변경을 애플리케이션에 알려야 하므로, [웹훅 처리](#handling-paddle-webhooks) 설정이 매우 중요합니다.

더 많은 정보는 [Paddle의 결제 링크 생성 API 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요.

> {note} 구독 상태 변경 후 관련 웹훅 수신에는 보통 짧은 지연이 있지만, 사용자가 체크아웃을 마친 직후 구독이 즉시 활성화되지 않을 수 있다는 점을 염두에 두세요.

<a name="manually-rendering-pay-links"></a>
#### 결제 링크 수동 렌더링

Laravel의 내장 Blade 컴포넌트를 사용하지 않고 직접 결제 링크를 표시할 수도 있습니다. 아래와 같이 결제 링크 URL을 생성한 후:

    $payLink = $request->user()->newSubscription('default', $premium = 34567)
        ->returnTo(route('home'))
        ->create();

HTML의 `a` 요소와 함께 사용할 수 있습니다:

    <a href="#!" class="ml-4 paddle_button" data-override="{{ $payLink }}">
        Paddle Checkout
    </a>

<a name="payments-requiring-additional-confirmation"></a>
#### 추가 확인이 필요한 결제

결제 처리 중 추가 인증이 필요한 경우 Paddle이 결제 확인 화면을 띄울 수 있습니다. Paddle 또는 Cashier가 표시하는 결제 확인 화면은 특정 은행이나 카드 발급사의 결제 절차에 맞게 맞춤 설계될 수 있고, 추가 카드 확인, 소액 임시 결제, 별도 기기 인증, 또는 기타 검증 절차가 포함될 수 있습니다.

<a name="inline-checkout"></a>
### 인라인 체크아웃

Paddle의 오버레이(팝업형) 방식이 아닌 인라인 방식으로 위젯을 표시할 수도 있습니다. 이 방식은 체크아웃의 HTML 필드는 조정할 수 없지만 애플리케이션 내에 위젯을 직접 임베드할 수 있습니다.

Cashier는 인라인 체크아웃을 쉽게 사용할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. 먼저 [결제 링크를 생성](#pay-links)한 뒤, 이를 `override` 속성으로 전달하세요:

```html
<x-paddle-checkout :override="$payLink" class="w-full" />
```

높이를 조정하려면 `height` 속성을 넘길 수 있습니다:

    <x-paddle-checkout :override="$payLink" class="w-full" height="500" />

<a name="inline-checkout-without-pay-links"></a>
#### 결제 링크 없이 인라인 체크아웃

결제 링크 대신 커스텀 옵션을 지정해 위젯을 표시할 수도 있습니다:

    $options = [
        'product' => $productId,
        'title' => 'Product Title',
    ];

    <x-paddle-checkout :options="$options" class="w-full" />

인라인 체크아웃의 상세 옵션은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/guides/how-tos/checkout/inline-checkout)와 [파라미터 레퍼런스](https://developer.paddle.com/reference/paddle-js/parameters)를 참고하세요.

> {note} 커스텀 옵션 지정 시 `passthrough` 옵션도 배열 형태로 넘기면 Cashier가 자동으로 JSON 문자열로 변환합니다. 단, `customer_id` passthrough 옵션은 Cashier 내부용으로 예약되어 있습니다.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 직접 렌더링

Blade 컴포넌트 없이 직접 인라인 체크아웃을 구현할 수도 있습니다. 먼저 [결제 링크를 생성](#pay-links)합니다.

이 예시에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하지만, 원하는 프론트엔드 스택 어디든 적용 가능합니다:

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

Stripe와 달리, Paddle의 사용자는 Paddle 전체에서 유일합니다(판매자 단위가 아님). 따라서 Paddle API는 사용자의 이메일 등 정보를 수정하는 기능을 제공하지 않습니다. 결제 링크 생성 시 `customer_email` 파라미터로 사용자를 식별하고, 구독 생성 시 해당 이메일과 일치하는 사용자를 Paddle에서 찾습니다.

이 때문에 다음과 같은 주의사항이 있습니다. Cashier에서 구독이 하나의 사용자에 묶여 있어도 **Paddle 내부적으로는 서로 다른 사용자 계정에 연결될 수 있습니다**. 각 구독은 자체 결제 정보와, 생성 당시 이메일로 Paddle 내에 관리될 수 있습니다.

따라서 구독 정보를 사용자에게 표시할 때는, 구독별로 연결된 이메일과 결제 정보 등을 반드시 안내해야 합니다. 아래는 `Laravel\Paddle\Subscription` 모델에서 해당 정보를 조회하는 예시입니다:

    $subscription = $user->subscription('default');

    $subscription->paddleEmail();
    $subscription->paymentMethod();
    $subscription->cardBrand();
    $subscription->cardLastFour();
    $subscription->cardExpirationDate();

현재로서는 Paddle API 를 통해 사용자의 이메일 주소를 변경할 수 없습니다. 사용자가 이메일을 변경하려면 Paddle 고객 지원에 직접 `paddleEmail` 값을 제공해 변경 요청을 해야 합니다.

<a name="prices"></a>
## 가격

Paddle은 통화별로 가격을 개별 설정할 수 있습니다. Cashier Paddle은 `productPrices` 메소드를 통해 제품에 대한 가격 정보를 모두 가져올 수 있습니다. 이 메소드는 가격을 조회할 제품 ID 배열을 받습니다:

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices([123, 456]);

기본적으로 요청의 IP 주소를 기반으로 통화가 판단되며, 특정 국가 가격을 조회하려면 `customer_country` 파라미터를 넘길 수 있습니다:

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices([123, 456], ['customer_country' => 'BE']);

가져온 가격 정보는 자유롭게 표시할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

순수 가격(세금 제외)과 세액 정보를 별도로 표시할 수도 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->net() }} (+ {{ $price->price()->tax() }} tax)</li>
    @endforeach
</ul>
```

구독 상품 가격을 조회한 경우에는 최초 결제금액과 반복 결제금액을 각각 노출할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - Initial: {{ $price->initialPrice()->gross() }} - Recurring: {{ $price->recurringPrice()->gross() }}</li>
    @endforeach
</ul>
```

자세한 내용은 [Paddle 가격 API 문서](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)를 참고하세요.

<a name="prices-customers"></a>
#### 고객별 가격

이미 구매 이력이 있는 사용자에게 적용되는 실제 가격 정보를 보여주고 싶다면 고객 인스턴스의 메소드를 사용하세요:

    use App\Models\User;

    $prices = User::find(1)->productPrices([123, 456]);

내부적으로 Cashier는 사용자의 [`paddleCountry` 메소드](#customer-defaults)를 사용해 해당 사용자의 통화에 맞는 가격을 가져옵니다. 예를 들어, 미국 사용자는 USD, 벨기에 사용자는 EUR로 가격이 표시됩니다. 일치하는 통화가 없으면 상품의 기본 통화가 사용됩니다. 가격은 Paddle 콘솔 패널에서 언제든 조정할 수 있습니다.

<a name="prices-coupons"></a>
#### 쿠폰

쿠폰 적용 후 할인된 가격을 표시하려면, `productPrices` 호출 시 쿠폰을 콤마로 구분된 문자열로 넘기세요:

    use Laravel\Paddle\Cashier;

    $prices = Cashier::productPrices([123, 456], [
        'coupons' => 'SUMMERSALE,20PERCENTOFF'
    ]);

계산된 가격은 `price` 메소드로 노출할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->price()->gross() }}</li>
    @endforeach
</ul>
```

할인 전 원래 가격은 `listPrice` 메소드로 표시할 수 있습니다:

```html
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->listPrice()->gross() }}</li>
    @endforeach
</ul>
```

> {note} Paddle 가격 API 사용 시 쿠폰은 일회성 구매 상품에만 적용할 수 있으며, 구독 플랜에는 직접 적용할 수 없습니다.

<a name="customers"></a>
## 고객

<a name="customer-defaults"></a>
### 고객 기본값

Cashier는 결제 링크 생성 시 고객 정보를 미리 입력할 수 있는 유용한 기본값 설정 방법을 제공합니다. 이를 통해 고객의 이메일, 국가, 우편번호 등을 미리 체크아웃 위젯에 자동 입력할 수 있습니다. 청구 대상 모델에서 아래 메소드를 오버라이드하면 됩니다:

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
     * 반드시 2글자 코드여야 하며, 지원 국가 목록은 아래 링크를 참고하세요.
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
     * 어떤 국가에서 필요로 하는지 아래 링크를 참고하세요.
     *
     * @return string|null
     * @link https://developer.paddle.com/reference/platform-parameters/supported-countries#countries-requiring-postcode
     */
    public function paddlePostcode()
    {
        //
    }

이 기본값은 Cashier의 모든 [결제 링크 생성](#pay-links) 작업에 적용됩니다.

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 만들려면, 보통 `App\Models\User` 인스턴스를 먼저 가져온 뒤 `newSubscription` 메소드를 사용해 결제 링크를 생성하세요:

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $user->newSubscription('default', $premium = 12345)
            ->returnTo(route('home'))
            ->create();

        return view('billing', ['payLink' => $payLink]);
    });

`newSubscription`의 첫 번째 인자는 구독의 내부 이름입니다. 단일 구독만 제공한다면 `default`나 `primary`로 써도 무방합니다. 이 이름은 내부 용도일 뿐 사용자에게 노출되지 않으며, 한 번 지정한 뒤에는 변경하지 마세요. 두 번째 인자는 사용자가 구독할 Paddle 플랜의 ID입니다. `returnTo` 메소드는 결제 완료 후 리디렉션할 URL을 지정합니다.

`create` 메소드로 생성한 결제 링크는 [paddle-button 컴포넌트](/docs/{{version}}/blade#components)로 결제 버튼을 만들 때 사용할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

결제가 완료되면 Paddle이 `subscription_created` 웹훅을 전송하며, Cashier가 이를 수신해 구독을 설정합니다. 반드시 [웹훅 처리](#handling-paddle-webhooks)를 제대로 설정했는지 점검하세요.

<a name="additional-details"></a>
#### 추가 세부정보

추가 고객 정보 또는 구독 정보를 입력하고자 한다면, `create` 메소드에 key/value 배열로 전달할 수 있습니다. 지원 필드는 Paddle의 [결제 링크 생성 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요:

    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->create([
            'vat_number' => $vatNumber,
        ]);

<a name="subscriptions-coupons"></a>
#### 쿠폰

구독 생성 시 쿠폰을 적용하려면, `withCoupon` 메소드를 사용하세요:

    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->withCoupon('code')
        ->create();

<a name="metadata"></a>
#### 메타데이터

구독 생성 시 `withMetadata` 메소드로 메타데이터 배열을 지정할 수 있습니다:

    $payLink = $user->newSubscription('default', $monthly = 12345)
        ->returnTo(route('home'))
        ->withMetadata(['key' => 'value'])
        ->create();

> {note} 메타데이터로는 `subscription_name` 키를 사용하지 마세요. 이 키는 Cashier 내부에서 예약되어 있습니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

구독 여부는 다양한 헬퍼 메소드로 확인할 수 있습니다. 먼저 `subscribed` 메소드는 사용자가 구독 활성(트라이얼 기간 포함)이면 `true`를 반환합니다:

    if ($user->subscribed('default')) {
        //
    }

`subscribed` 메소드는 [라우트 미들웨어](/docs/{{version}}/middleware)로 사용하여 구독 상태에 따라 접근 권한을 제어할 수 있습니다:

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureUserIsSubscribed
    {
        public function handle($request, Closure $next)
        {
            if ($request->user() && ! $request->user()->subscribed('default')) {
                // 이 사용자는 유료 고객이 아닙니다...
                return redirect('billing');
            }

            return $next($request);
        }
    }

트라이얼 상태인지 확인하려면 `onTrial` 메소드를 사용하세요. 남은 체험 기간 안내 등에 활용할 수 있습니다:

    if ($user->subscription('default')->onTrial()) {
        //
    }

특정 Paddle 플랜에 가입되어 있는지 확인하려면 `subscribedToPlan` 메소드를 사용하세요:

    if ($user->subscribedToPlan($monthly = 12345, 'default')) {
        //
    }

복수 플랜 검사도 가능합니다:

    if ($user->subscribedToPlan([$monthly = 12345, $yearly = 54321], 'default')) {
        //
    }

트라이얼 기간이 끝났는지 확인하려면 `recurring` 메소드를 사용합니다:

    if ($user->subscription('default')->recurring()) {
        //
    }

<a name="cancelled-subscription-status"></a>
#### 구독 취소 상태

구독이 취소된 적이 있는지 확인하려면 `cancelled` 메소드 사용:

    if ($user->subscription('default')->cancelled()) {
        //
    }

"유예 기간(grace period)"에는 취소되어도 `subscribed`가 `true`지만, 유예 여부를 확인하려면:

    if ($user->subscription('default')->onGracePeriod()) {
        //
    }

유예 기간이 끝났는지도 `ended` 메소드로 확인하세요:

    if ($user->subscription('default')->ended()) {
        //
    }

<a name="past-due-status"></a>
#### 연체(past due) 상태

결제 실패 시 구독이 `past_due`로 표시됩니다. 이때는 고객이 결제 정보를 업데이트해야만 다시 활성화됩니다. `pastDue`로 연체 여부 확인이 가능합니다:

    if ($user->subscription('default')->pastDue()) {
        //
    }

연체 시에는 반드시 [결제 정보 변경](#updating-payment-information)을 안내하세요. Paddle 대시보드의 [구독 설정](https://vendors.paddle.com/subscription-settings)에서 연체 처리 방식을 조정할 수 있습니다.

연체 상태도 활성 상태로 간주하고 싶으면 Cashier의 `keepPastDueSubscriptionsActive` 메소드를 사용하세요. 보통 `AppServiceProvider`의 `register`에서 호출합니다:

    use Laravel\Paddle\Cashier;

    public function register()
    {
        Cashier::keepPastDueSubscriptionsActive();
    }

> {note} 연체 상태에서는 트라이얼 중 상품 변경, 수량 변경 등은 불가합니다(`swap`, `updateQuantity`는 예외 발생).

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

대부분의 구독 상태는 쿼리 스코프로도 제공되어, 원하는 상태의 구독을 쉽게 조회할 수 있습니다:

    // 활성 구독 모두 조회
    $subscriptions = Subscription::query()->active()->get();

    // 해당 사용자의 취소된 구독 조회
    $subscriptions = $user->subscriptions()->cancelled()->get();

이 외에도 아래와 같은 스코프들이 있습니다:

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

<a name="subscription-single-charges"></a>
### 구독 단일 결제

구독 중인 고객에게 일시적으로 추가금액을 청구할 수 있습니다:

    $response = $user->subscription('default')->charge(12.99, 'Support Add-on');

[단일 결제](#single-charges)와는 달리, 이 방식은 구독에 저장된 결제 수단에 바로 청구합니다. 금액은 구독의 기본 통화로 지정하세요.

<a name="updating-payment-information"></a>
### 결제 정보 변경

Paddle은 구독별 결제 수단을 저장합니다. 결제 정보를 변경하려면 구독 모델의 `updateUrl` 메소드로 결제 정보 변경 URL을 생성하세요:

    use App\Models\User;

    $user = User::find(1);

    $updateUrl = $user->subscription('default')->updateUrl();

생성한 URL을 paddle-button Blade 컴포넌트와 함께 사용해 Paddle 위젯을 통해 변경하도록 할 수 있습니다:

```html
<x-paddle-button :url="$updateUrl" class="px-8 py-4">
    Update Card
</x-paddle-button>
```

변경이 완료되면 `subscription_updated` 웹훅이 발송되며, Cashier가 이것을 수신해 구독 세부정보를 갱신합니다.

<a name="changing-plans"></a>
### 상품 변경(플랜 변경)

구독자가 플랜 업그레이드/다운그레이드를 원할 때는 구독의 `swap` 메소드에 Paddle 플랜 ID를 넘기세요:

    use App\Models\User;

    $user = User::find(1);

    $user->subscription('default')->swap($premium = 34567);

즉시 청구서를 발행(청구)하고 싶다면 `swapAndInvoice` 메소드 사용:

    $user = User::find(1);

    $user->subscription('default')->swapAndInvoice($premium = 34567);

> {note} 트라이얼 중에는 플랜 변경이 불가합니다. 이 제한은 [Paddle 문서](https://developer.paddle.com/api-reference/subscription-api/users/updateuser#usage-notes)를 참고하세요.

<a name="prorations"></a>
#### 비례 계산(Prorations)

기본적으로 Paddle은 플랜 변경 시 금액을 비례 계산합니다. 비례 계산을 원하지 않으면 `noProrate` 메소드를 사용하세요:

    $user->subscription('default')->noProrate()->swap($premium = 34567);

<a name="subscription-quantity"></a>
### 구독 수량

구독 수량이 사용되는 경우(예: 한 프로젝트당 월 $10), `incrementQuantity`, `decrementQuantity`로 쉽게 수량 변경이 가능합니다:

    $user = User::find(1);

    $user->subscription('default')->incrementQuantity();

    // 5개 증가
    $user->subscription('default')->incrementQuantity(5);

    $user->subscription('default')->decrementQuantity();

    // 5개 감소
    $user->subscription('default')->decrementQuantity(5);

정확한 수량을 지정하려면 `updateQuantity` 사용:

    $user->subscription('default')->updateQuantity(10);

비례 계산 없이 변경하려면:

    $user->subscription('default')->noProrate()->updateQuantity(10);

<a name="subscription-modifiers"></a>
### 구독 수정자(Modifiers)

구독 수정자는 [사용량 기반 청구](https://developer.paddle.com/guides/how-tos/subscriptions/metered-billing#using-subscription-price-modifiers)나 애드온(부가상품) 제공에 활용할 수 있습니다.

예를 들어, "프리미엄 지원" 애드온을 만들고자 한다면:

    $modifier = $user->subscription('default')->newModifier(12.99)->create();

이 예제는 구독에 $12.99 애드온을 추가합니다. 기본적으로 매 구독 주기마다 반복 청구됩니다. `description` 메소드로 설명을 추가할 수 있습니다:

    $modifier = $user->subscription('default')->newModifier(12.99)
        ->description('Premium Support')
        ->create();

사용량 기반 청구를 위해, Paddle 대시보드에 $0 플랜을 만든 뒤 사용량만큼 modifier를 추가할 수 있습니다:

    $modifier = $user->subscription('default')->newModifier(0.99)
        ->description('New text message')
        ->oneTime()
        ->create();

`oneTime` 메소드는 해당 modifier가 최초 한 번만 청구되도록 합니다.

<a name="retrieving-modifiers"></a>
#### 수정자 목록 가져오기

구독의 모든 수정자는 `modifiers` 메소드로 가져올 수 있습니다:

    $modifiers = $user->subscription('default')->modifiers();

    foreach ($modifiers as $modifier) {
        $modifier->amount(); // $0.99
        $modifier->description; // New text message.
    }

<a name="deleting-modifiers"></a>
#### 수정자 삭제

`Laravel\Paddle\Modifier` 인스턴스에서 `delete` 호출로 삭제할 수 있습니다:

    $modifier->delete();

<a name="pausing-subscriptions"></a>
### 구독 일시정지

구독을 일시정지하려면, 구독의 `pause` 메소드 호출:

    $user->subscription('default')->pause();

일시정지 시, 데이터베이스의 `paused_from` 컬럼이 자동 설정됩니다. 예를 들어, 결제일이 5일인데 1일에 일시정지했다면 5일까지는 `paused`가 false입니다.

유예 기간동안 일시정지 여부 확인은 `onPausedGracePeriod`로 합니다:

    if ($user->subscription('default')->onPausedGracePeriod()) {
        //
    }

일시정지 해제는 `unpause` 메소드로 가능합니다:

    $user->subscription('default')->unpause();

> {note} 일시정지된 구독은 변경이 불가합니다. 다른 플랜이나 수량을 변경하려면 먼저 해제하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독 취소는 `cancel`로 가능:

    $user->subscription('default')->cancel();

취소 시 `ends_at` 컬럼이 설정됩니다. 예를 들어, 3월 1일에 취소해도 결제 주기가 3월 5일까지면 5일까지는 `subscribed`가 true를 반환합니다.

유예 기간 여부 확인은 `onGracePeriod`로:

    if ($user->subscription('default')->onGracePeriod()) {
        //
    }

즉시 취소하려면 `cancelNow` 사용:

    $user->subscription('default')->cancelNow();

> {note} Paddle 구독은 취소 후 재개 불가입니다. 재개하려면 새로 가입해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험

<a name="with-payment-method-up-front"></a>
### 결제 수단 미리 받기

> {note} 체험 중 결제 수단을 미리 받으면 Paddle은 상품 변경/수량 변경을 불허합니다. 체험 중 플랜 변경을 지원하려면 구독을 취소 후 재생성해야 합니다.

체험 기간을 제공하되 결제 수단도 받고 싶을 때는 `trialDays` 메소드를 사용하세요:

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $request->user()->newSubscription('default', $monthly = 12345)
                    ->returnTo(route('home'))
                    ->trialDays(10)
                    ->create();

        return view('billing', ['payLink' => $payLink]);
    });

이 메소드는 체험 종료일을 애플리케이션 DB와 Paddle에 모두 반영하여, 해당일까지는 결제가 시작되지 않습니다.

> {note} 체험 종료 전 구독이 취소되지 않으면 체험 만료와 동시에 결제가 이루어집니다. 사용자에게 체험 만료일을 반드시 안내하세요.

체험 중 여부 확인은 `onTrial` 메소드로. 아래 예시 두 가지는 동일합니다:

    if ($user->onTrial('default')) {
        //
    }

    if ($user->subscription('default')->onTrial()) {
        //
    }

<a name="defining-trial-days-in-paddle-cashier"></a>
#### Paddle/Cashier에서 체험일 정의

체험일을 Paddle 대시보드에서 지정해도 되며, Cashier에서 명시적으로 넘길 수도 있습니다. Paddle 쪽에 설정했다면 새 구독마다 체험일이 부여됩니다(이전 구독자 포함). 체험 없이 바로 유료로 전환하고 싶을 때는 `trialDays(0)`을 명시적으로 지정하세요.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 체험 시작

결제 수단 없이 체험을 제공하려면, 고객 레코드의 `trial_ends_at` 컬럼을 원하는 체험 만료일로 설정하세요. 주로 회원가입 시에 사용합니다:

    use App\Models\User;

    $user = User::create([
        // ...
    ]);

    $user->createAsCustomer([
        'trial_ends_at' => now()->addDays(10)
    ]);

Cashier에서는 이를 "제네릭 체험(generic trial)"이라고 하며, 아직 구독이 없는 상태에서 적용됩니다. `User` 인스턴스의 `onTrial`은 현재 날짜가 `trial_ends_at` 이전이면 true를 반환합니다:

    if ($user->onTrial()) {
        // 체험 기간 내에 있음...
    }

구독 생성이 필요해지면, 일반적인 방법으로 `newSubscription`을 사용하세요:

    use Illuminate\Http\Request;

    Route::get('/user/subscribe', function (Request $request) {
        $payLink = $user->newSubscription('default', $monthly = 12345)
            ->returnTo(route('home'))
            ->create();

        return view('billing', ['payLink' => $payLink]);
    });

체험 종료일은 `trialEndsAt` 메소드로 확인할 수 있습니다. 구독명이 여러개면 첫 번째 인자를 이름으로 지정하세요:

    if ($user->onTrial()) {
        $trialEndsAt = $user->trialEndsAt('main');
    }

구독이 없는 "제네릭 체험" 상태인지만 확인하려면, `onGenericTrial`을 사용하세요:

    if ($user->onGenericTrial()) {
        // 구독 없는 체험 기간 내에 있음...
    }

> {note} Paddle 구독 생성 이후에는 체험 기간을 연장하거나 수정할 수 없습니다.

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리

Paddle은 다양한 이벤트를 웹훅으로 애플리케이션에 통지할 수 있습니다. Cashier 서비스 제공자는 `/paddle/webhook`에 기본 라우트를 등록하며, 이 컨트롤러에서 모든 웹훅 요청을 처리합니다.

이 컨트롤러는 결제 실패로 인한 구독 취소, 구독 갱신, 결제 정보 변경 등 일반적인 Paddle 웹훅을 자동 처리해줍니다. 별도 웹훅 이벤트의 커스텀 핸들링이 필요하다면 확장도 가능합니다.

웹훅 처리를 위해 반드시 [Paddle 콘솔 패널에서 웹훅 URL을 설정](https://vendors.paddle.com/alerts-webhooks)해야 하며, Cashier는 기본적으로 `/paddle/webhook` 엔드포인트를 사용합니다. 반드시 아래 웹훅을 활성화하세요:

- Subscription Created
- Subscription Updated
- Subscription Cancelled
- Payment Succeeded
- Subscription Payment Succeeded

> {note} 웹훅 요청은 Cashier의 [서명 검증 미들웨어](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures)로 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>
#### 웹훅 & CSRF 보호

웹훅은 Laravel의 [CSRF 보호](/docs/{{version}}/csrf)를 우회해야 하므로, `App\Http\Middleware\VerifyCsrfToken`에 예외 URI로 등록하거나 routes 파일에서 `web` 미들웨어 그룹 밖에 위치시키세요:

    protected $except = [
        'paddle/*',
    ];

<a name="webhooks-local-development"></a>
#### 웹훅 & 로컬 개발

로컬 개발 중 웹훅을 수신하려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction)와 같은 도구로 외부에서 접속 가능한 환경을 만들어야 합니다. [Laravel Sail](/docs/{{version}}/sail)로 개발한다면 [사이트 공유 명령](/docs/{{version}}/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 결제 실패로 인한 구독 취소 등 일반적인 웹훅을 자동 처리합니다. 추가로 직접 처리할 웹훅 이벤트가 있다면 Cashier에서 제공하는 이벤트 리스너를 사용하세요:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` 웹훅을 처리하려면 다음처럼 하면 됩니다:

    <?php

    namespace App\Listeners;

    use Laravel\Paddle\Events\WebhookReceived;

    class PaddleEventListener
    {
        /**
         * Paddle 웹훅 처리.
         *
         * @param  \Laravel\Paddle\Events\WebhookReceived  $event
         * @return void
         */
        public function handle(WebhookReceived $event)
        {
            if ($event->payload['alert_name'] === 'payment_succeeded') {
                // 이벤트 처리...
            }
        }
    }

리스너를 정의했다면, `EventServiceProvider`에 다음과 같이 등록하세요:

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

Cashier는 웹훅 타입별로 전용 이벤트도 브로드캐스트합니다. 이 이벤트에는 Paddle에서 받은 전체 페이로드뿐 아니라 연관된 모델(청구 대상 모델, 구독, 영수증 등)도 함께 포함됩니다.

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\PaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionPaymentSucceeded`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionCancelled`

</div>

또한, 기본 웹훅 라우트 URL을 `.env` 파일에서 `CASHIER_WEBHOOK` 변수로 오버라이드할 수 있습니다. 이 값은 Paddle 대시보드에 등록한 웹훅 URL과 반드시 일치해야 합니다:

```bash
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅의 보안을 위해 [Paddle의 웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 사용할 수 있습니다. Cashier는 기본적으로 Paddle 서명을 검증하는 미들웨어를 내장하고 있습니다.

서명 검증을 활성화하려면 `.env` 파일에 `PADDLE_PUBLIC_KEY` 환경 변수가 설정되어 있어야 합니다. 퍼블릭 키는 Paddle 계정 대시보드에서 획득합니다.

<a name="single-charges"></a>
## 단일 결제

<a name="simple-charge"></a>
### 간단 결제

단일 결제를 생성하려면, billable 모델 인스턴스의 `charge` 메소드로 결제 링크를 만들 수 있습니다. 첫 번째 인자는 금액(float), 두 번째 인자는 결제 설명입니다:

    use Illuminate\Http\Request;

    Route::get('/store', function (Request $request) {
        return view('store', [
            'payLink' => $user->charge(12.99, 'Action Figure')
        ]);
    });

생성된 결제 링크는 `paddle-button` 컴포넌트로 Paddle 위젯을 띄우는 데 사용할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`charge` 메서드는 세 번째 인자로 옵션 배열을 받습니다. 사용할 수 있는 옵션은 [Paddle 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요:

    $payLink = $user->charge(12.99, 'Action Figure', [
        'custom_option' => $value,
    ]);

결제는 `cashier.currency` 설정에 지정된 통화로 진행됩니다(기본값 USD). 기본 통화는 `.env`의 `CASHIER_CURRENCY`로 오버라이드할 수 있습니다:

```bash
CASHIER_CURRENCY=EUR
```

또는 [통화별 다이나믹 가격](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink#price-overrides)을 적용할 수도 있습니다:

    $payLink = $user->charge([
        'USD:19.99',
        'EUR:15.99',
    ], 'Action Figure');

<a name="charging-products"></a>
### 상품 결제

Paddle에 등록된 특정 상품에 대해 단일 결제를 받으려면, `chargeProduct` 메소드로 결제 링크를 생성하세요:

    use Illuminate\Http\Request;

    Route::get('/store', function (Request $request) {
        return view('store', [
            'payLink' => $request->user()->chargeProduct($productId = 123)
        ]);
    });

결제 링크를 `paddle-button`에 전달해 Paddle 위젯을 띄울 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4">
    Buy
</x-paddle-button>
```

옵션이 필요하다면 두 번째 인자로 넘길 수 있으며, 세부 내용은 [Paddle 문서](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink)를 참고하세요:

    $payLink = $user->chargeProduct($productId, [
        'custom_option' => $value,
    ]);

<a name="refunding-orders"></a>
### 주문 환불

Paddle 주문을 환불하려면 `refund` 메소드를 사용하세요. 첫 번째 인자로 Paddle 주문 ID를 받습니다. Billable 모델의 `receipts`로 영수증을 조회할 수 있습니다:

    use App\Models\User;

    $user = User::find(1);

    $receipt = $user->receipts()->first();

    $refundRequestId = $user->refund($receipt->order_id);

부분 환불이나 환불 사유를 지정할 수도 있습니다:

    $receipt = $user->receipts()->first();

    $refundRequestId = $user->refund(
        $receipt->order_id, 5.00, 'Unused product time'
    );

> {tip} Paddle 고객 지원에 문의할 때 `$refundRequestId`로 환불 내역을 조회할 수 있습니다.

<a name="receipts"></a>
## 영수증

Billable 모델의 `receipts` 속성으로 간단하게 영수증 목록을 가져올 수 있습니다:

    use App\Models\User;

    $user = User::find(1);

    $receipts = $user->receipts;

영수증을 테이블로 표시할 때 각 인스턴스의 메소드로 다양한 정보를 얻을 수 있습니다. 예를 들어 다음과 같이 모든 영수증을 다운로드할 수 있게 할 수 있습니다:

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
### 과거 및 예정 결제

구독자의 과거/예정 결제 정보를 `lastPayment`, `nextPayment` 메소드로 조회할 수 있습니다:

    use App\Models\User;

    $user = User::find(1);

    $subscription = $user->subscription('default');

    $lastPayment = $subscription->lastPayment();
    $nextPayment = $subscription->nextPayment();

두 메소드는 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 단, `nextPayment`는 결제 주기가 종료된 경우(예: 구독 취소) null을 반환합니다:

    Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}

<a name="handling-failed-payments"></a>
## 실패한 결제 처리

구독 결제가 실패하는 원인은 카드 만료, 한도 초과 등 다양합니다. 이런 경우 Paddle의 [자동 청구 이메일](https://vendors.paddle.com/subscription-settings) 기능을 설정해 Paddle이 직접 결제 실패 처리를 하게 두는 것이 좋습니다.

더 정밀하게 처리하려면 [`subscription_payment_failed`](https://developer.paddle.com/webhook-reference/subscription-alerts/subscription-payment-failed) 웹훅과 대시보드의 "Subscription Payment Failed" 옵션을 사용해 직접 코드를 작성할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use Laravel\Paddle\Http\Controllers\WebhookController as CashierController;

    class WebhookController extends CashierController
    {
        /**
         * 구독 결제 실패 처리.
         *
         * @param  array  $payload
         * @return void
         */
        public function handleSubscriptionPaymentFailed($payload)
        {
            // 결제 실패 처리...
        }
    }

<a name="testing"></a>
## 테스트

테스트 시에는 실제로 결제 플로우를 직접 점검해야 합니다.

자동화 테스트(예: CI 환경)에서는 [Laravel HTTP 클라이언트](/docs/{{version}}/http-client#testing)로 Paddle과의 HTTP 호출을 가짜로 할 수 있습니다. 실제 Paddle 응답을 테스트하지는 않지만, Paddle API 호출 없이 애플리케이션 동작을 검증할 수 있습니다.