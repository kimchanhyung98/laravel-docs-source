# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [구성](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매하기](#quickstart-selling-products)
    - [구독 상품 판매](#quickstart-selling-subscriptions)
- [결제 세션](#checkout-sessions)
    - [오버레이 결제](#overlay-checkout)
    - [인라인 결제](#inline-checkout)
    - [비회원 결제](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객별 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회하기](#retrieving-customers)
    - [고객 생성하기](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [여러 상품의 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험판](#subscription-trials)
    - [결제 정보를 먼저 받는 체험판](#with-payment-method-up-front)
    - [결제 정보를 받지 않는 체험판](#without-payment-method-up-front)
    - [체험 연장 및 활성화](#extend-or-activate-a-trial)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [상품 청구](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧 지급](#crediting-transactions)
- [거래](#transactions)
    - [과거 및 예정된 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

> [!WARNING]  
> 이 문서는 Cashier Paddle 2.x가 Paddle Billing과 통합된 버전을 위한 문서입니다. Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 참고하세요.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 청구 서비스를 쉽고 유연하게 사용할 수 있는 인터페이스를 제공합니다. 구독 청구의 보일러플레이트 코드 대부분을 자동으로 처리해줍니다. 단순 구독 관리 외에도 Cashier는 구독 변경, 구독 "수량", 구독 일시정지, 취소 유예기간 등 여러 기능을 지원합니다.

Cashier Paddle을 자세히 살펴보기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 확인하는 것을 추천합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier를 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용하여 Paddle용 Cashier 패키지를 설치하세요.

```shell
composer require laravel/cashier-paddle
```

그 다음, `vendor:publish` Artisan 명령을 사용하여 Cashier 마이그레이션 파일을 퍼블리시해야 합니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성합니다. 또한 고객의 모든 구독을 저장할 `subscriptions` 및 `subscription_items` 테이블이, Paddle 거래 내역을 저장할 `transactions` 테이블도 함께 생성됩니다.

```shell
php artisan migrate
```

> [!WARNING]  
> Cashier가 모든 Paddle 이벤트를 제대로 처리하려면 반드시 [Cashier의 웹훅 처리](#handling-paddle-webhooks)를 세팅해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle Sandbox

로컬 또는 스테이징 환경에서는 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)을 등록해야 합니다. 이 계정을 이용하면 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있습니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card)도 다양한 결제 시나리오 시뮬레이션에 활용할 수 있습니다.

Paddle Sandbox 환경을 사용할 때는, 애플리케이션의 `.env` 파일에 아래와 같이 `PADDLE_SANDBOX` 환경변수를 `true`로 설정하세요.

```ini
PADDLE_SANDBOX=true
```

개발이 마무리되어 실제 환경에 배포할 경우 [Paddle 벤더 계정](https://paddle.com) 승인을 받아야 합니다. Paddle은 애플리케이션 도메인을 프로덕션에 배포하기 전에 별도의 승인 절차를 거칩니다.

<a name="configuration"></a>
## 구성

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에 사용자(User) 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제수단 정보 업데이트 등 일반적인 청구 작업을 위한 다양한 메서드를 제공합니다.

    use Laravel\Paddle\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

유저가 아닌 다른 청구 주체가 있다면, 해당 클래스에도 트레이트를 추가할 수 있습니다.

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Paddle\Billable;

    class Team extends Model
    {
        use Billable;
    }

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에 Paddle 키를 설정해야 합니다. Paddle API 키는 Paddle 콘트롤 패널에서 확인할 수 있습니다.

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 변수는 [Paddle Sandbox 환경](#paddle-sandbox)을 사용할 때 `true`로, 라이브 벤더 환경에서 프로덕션 배포 시에는 `false`로 설정하세요.

`PADDLE_RETAIN_KEY`는 [Retain](https://developer.paddle.com/paddlejs/retain) 사용 시에만 선택적으로 설정하면 됩니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 결제 위젯을 실행하기 위해 자체 JavaScript 라이브러리가 필요합니다. 브레이드 레이아웃의 `</head>` 태그 직전에 `@paddleJS` Blade 디렉티브를 추가하여 해당 JS를 불러올 수 있습니다.

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

인보이스 등에서 표시되는 금액의 통화 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter`](https://www.php.net/manual/en/class.numberformatter.php) 클래스를 활용하여 통화 로케일을 지정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 외의 로케일을 사용하려면 PHP `ext-intl` 확장 모듈이 서버에 설치되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다. 직접 모델을 정의하고 해당 Cashier 모델을 상속해서 사용하세요.

    use Laravel\Paddle\Subscription as CashierSubscription;

    class Subscription extends CashierSubscription
    {
        // ...
    }

생성한 커스텀 모델을 Cashier가 사용하도록 지정하려면 주로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 아래와 같이 설정합니다.

    use App\Models\Cashier\Subscription;
    use App\Models\Cashier\Transaction;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Cashier::useSubscriptionModel(Subscription::class);
        Cashier::useTransactionModel(Transaction::class);
    }

<a name="quickstart"></a>
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 상품 판매하기

> [!NOTE]  
> Paddle Checkout을 사용하기 전에 반드시 Paddle 대시보드에서 고정 가격 상품을 먼저 정의해야 합니다. 또한 [Paddle의 웹훅 처리](#handling-paddle-webhooks)도 꼭 구성하세요.

애플리케이션에서 상품 및 구독 결제 기능을 제공하는 것은 부담스러울 수 있습니다. 하지만 Cashier와 [Paddle Checkout Overlay](https://www.paddle.com/billing/checkout)를 활용하면 쉽고 강력한 결제 시스템을 구현할 수 있습니다.

비정기, 단일 결제 상품에 대해서는 Cashier의 `checkout` 메서드를 사용해 Paddle Checkout Overlay로 청구할 수 있습니다. 고객은 해당 위젯에서 결제 정보를 입력하고 결제를 완료하며, 결제 후에는 애플리케이션에서 지정한 성공 URL로 리디렉션됩니다.

    use Illuminate\Http\Request;

    Route::get('/buy', function (Request $request) {
        $checkout = $request->user()->checkout('pri_deluxe_album')
            ->returnTo(route('dashboard'));

        return view('buy', ['checkout' => $checkout]);
    })->name('checkout');

위 예제처럼 Cashier의 `checkout` 메서드를 사용해 특정 "가격 식별자"에 대한 Paddle Checkout Overlay를 보여줄 checkout 객체를 생성합니다. Paddle에서 "가격"은 [특정 상품에 대하여 정의한 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요할 경우 `checkout` 메서드는 Paddle에 고객을 자동으로 생성하고, 애플리케이션 DB의 해당 사용자와 Paddle 고객 레코드를 연결합니다. 결제 세션이 완료되면, 사용자는 성공 페이지로 리디렉션되어 추가 안내를 볼 수 있습니다.

`buy` 뷰에서는 Checkout Overlay를 띄울 버튼을 만듭니다. Cashier Paddle에 포함된 `paddle-button` Blade 컴포넌트를 사용할 수 있고, [오버레이 결제를 수동으로 구현](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 제공하기

상품을 판매할 때, 자체 Cart와 Order 모델로 주문 상품 및 완료 내역을 추적하고 싶을 수 있습니다. Paddle Checkout Overlay로 리디렉션할 때 주문 식별자를 함께 보내려면, `checkout` 메서드에 커스텀 데이터를 배열로 전달할 수 있습니다.

아래 예시에서 사용자가 결제를 시작하면 미완료 상태의 `Order`가 자동 생성됩니다. 이때 `Cart`, `Order` 모델은 예시일 뿐이며, 실제로는 애플리케이션 요구에 맞춰 구현해야 합니다.

    use App\Models\Cart;
    use App\Models\Order;
    use Illuminate\Http\Request;
    
    Route::get('/cart/{cart}/checkout', function (Request $request, Cart $cart) {
        $order = Order::create([
            'cart_id' => $cart->id,
            'price_ids' => $cart->price_ids,
            'status' => 'incomplete',
        ]);

        $checkout = $request->user()->checkout($order->price_ids)
            ->customData(['order_id' => $order->id]);

        return view('billing', ['checkout' => $checkout]);
    })->name('checkout');

위 예시와 같이, 결제 세션을 시작할 때 관련된 Paddle 가격 식별자와 함께 `checkout`을 호출하며, 주문 ID를 `customData`로 전달합니다.

결제 완료 후 주문을 "완료"로 표시하려면, Paddle이 전송하는 웹훅을 Cashier 이벤트로 받아 DB에 주문 정보를 저장하면 됩니다.

시작하려면 Cashier가 디스패치하는 `TransactionCompleted` 이벤트를 청취하세요. 일반적으로 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 등록합니다.

    use App\Listeners\CompleteOrder;
    use Illuminate\Support\Facades\Event;
    use Laravel\Paddle\Events\TransactionCompleted;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::listen(TransactionCompleted::class, CompleteOrder::class);
    }

예시에서 `CompleteOrder` 리스너는 다음과 같이 작성할 수 있습니다.

    namespace App\Listeners;

    use App\Models\Order;
    use Laravel\Cashier\Cashier;
    use Laravel\Cashier\Events\TransactionCompleted;

    class CompleteOrder
    {
        /**
         * Handle the incoming Cashier webhook event.
         */
        public function handle(TransactionCompleted $event): void
        {
            $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

            $order = Order::findOrFail($orderId);

            $order->update(['status' => 'completed']);
        }
    }

Paddle의 [`transaction.completed` 이벤트 데이터](https://developer.paddle.com/webhooks/transactions/transaction-completed) 관련 문서도 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 상품 판매

> [!NOTE]  
> Paddle Checkout을 사용하기 전에 반드시 Paddle 대시보드에서 고정 가격 상품을 먼저 정의해야 합니다. 또한 [웹훅 처리도](#handling-paddle-webhooks) 꼭 구성하세요.

애플리케이션에서 상품 및 구독 결제 기능 제공은 까다로울 수 있지만, Cashier와 [Paddle Checkout Overlay](https://www.paddle.com/billing/checkout)를 사용하면 신속하게 모던한 결제 흐름을 구현할 수 있습니다.

Cashier와 Paddle Checkout Overlay로 구독을 판매하는 방법을 예를 들어 설명하겠습니다. 예를 들어, 월 구독(`price_basic_monthly`)과 연 구독(`price_basic_yearly`)이 있는 "Basic" 상품(`pro_basic`)이 있고, 추가로 "Expert" 플랜으로 `pro_expert`가 있다고 가정합니다.

먼저 구독 방식은 사용자가 애플리케이션의 가격 페이지에서 원하는 플랜을 선택해 "구독" 버튼을 클릭하는 형태로 구현할 수 있습니다. 이 버튼이 Paddle Checkout Overlay를 호출하도록 아래와 같이 할 수 있습니다.

    use Illuminate\Http\Request;

    Route::get('/subscribe', function (Request $request) {
        $checkout = $request->user()->checkout('price_basic_monthly')
            ->returnTo(route('dashboard'));

        return view('subscribe', ['checkout' => $checkout]);
    })->name('subscribe');

`subscribe` 뷰에서는 아래처럼 Checkout Overlay 버튼을 넣을 수 있습니다. Cashier Paddle에 포함된 `paddle-button` Blade 컴포넌트를 활용하거나, [오버레이 결제를 수동으로](#manually-rendering-an-overlay-checkout) 구현할 수 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 Subscribe 버튼을 클릭하면 사용자는 결제 정보를 입력하고 구독을 시작할 수 있습니다. 결제가 완료되어 실제 구독이 시작되는 시점(특정 결제수단의 경우 몇 초 지연될 수 있음)을 감지하려면 [Cashier의 웹훅 처리](#handling-paddle-webhooks)도 반드시 설정하세요.

구독 상태에 따라 애플리케이션의 일부를 구독 고객만 접근 가능하게 만들 수 있습니다. Cashier의 `Billable` 트레이트에서 제공하는 `subscribed` 메서드를 활용할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 가입되었는지도 쉽게 확인할 수 있습니다.

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독자 전용 미들웨어 만들기

편의를 위해, 요청이 구독자에 의해 생성된 것인지 확인하는 [미들웨어](/docs/{{version}}/middleware)를 만들고, 해당 미들웨어를 라우트에 쉽게 할당할 수 있습니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class Subscribed
    {
        /**
         * Handle an incoming request.
         */
        public function handle(Request $request, Closure $next): Response
        {
            if (! $request->user()?->subscribed()) {
                // 유저를 결제 페이지로 리디렉션해서 구독 유도...
                return redirect('/subscribe');
            }

            return $next($request);
        }
    }

정의한 미들웨어는 다음과 같이 라우트에 할당할 수 있습니다.

    use App\Http\Middleware\Subscribed;

    Route::get('/dashboard', function () {
        // ...
    })->middleware([Subscribed::class]);

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객의 요금제 관리 기능 제공하기

고객이 요금제를 다른 상품이나 "티어"로 변경하길 원할 수도 있습니다. 예를 들어, 월 구독에서 연 구독으로 바꾸는 버튼을 아래와 같은 라우트로 연결해 구현할 수 있습니다.

    use Illuminate\Http\Request;

    Route::put('/subscription/{price}/swap', function (Request $request, $price) {
        $user->subscription()->swap($price); // 예시에서는 "$price"는 "price_basic_yearly"

        return redirect()->route('dashboard');
    })->name('subscription.swap');

플랜 변경 외에 구독 취소 버튼도 별도의 라우트로 만들 수 있습니다.

    use Illuminate\Http\Request;

    Route::put('/subscription/cancel', function (Request $request, $price) {
        $user->subscription()->cancel();

        return redirect()->route('dashboard');
    })->name('subscription.cancel');

이제 구독 요금은 해당 청구주기가 끝날 때 취소됩니다.

> [!NOTE]  
> Cashier의 웹훅 처리를 설정해두었다면, Paddle 대시보드에서 구독을 취소하더라도 관련 webhook 이벤트를 받아 Cashier가 애플리케이션 DB의 구독 상태를 자동으로 동기화합니다.

<!-- 이하 나머지 섹션들은 위와 같은 번역 스타일로 계속 이어집니다... -->

---

**번역이 매우 방대한 관계로, 특별히 필요한 섹션이나 추가 번역이 필요한 부분이 있다면 원하는 항목을 별도 요청해 주세요.  
전체 번역이 필요하신 경우, 추가로 이어서 순차 번역해드릴 수 있습니다.**