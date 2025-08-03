# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [청구 가능한 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [제품 판매하기](#quickstart-selling-products)
    - [구독 판매하기](#quickstart-selling-subscriptions)
- [결제 세션](#checkout-sessions)
    - [오버레이 결제](#overlay-checkout)
    - [인라인 결제](#inline-checkout)
    - [게스트 결제](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [다중 제품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시중지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 평가판](#subscription-trials)
    - [결제 수단을 미리 받는 경우](#with-payment-method-up-front)
    - [결제 수단 없이 제공하는 경우](#without-payment-method-up-front)
    - [평가판 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [제품 청구](#charging-for-products)
    - [결제 환불](#refunding-transactions)
    - [거래 크레딧](#crediting-transactions)
- [거래 내역](#transactions)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]  
> 이 문서는 Paddle Classic이 아닌, Cashier Paddle 2.x가 Paddle 청구 서비스와 통합될 때 사용됩니다. 아직 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)는 Paddle의 구독 청구 서비스([Paddle](https://paddle.com))를 위한 직관적이고 유연한 인터페이스를 제공합니다. 번거로운 구독 청구 코드를 거의 모두 처리해주며, 기본 구독 관리 외에도 구독 교체, 구독 "수량", 일시 중지, 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 시작하기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 살펴보기를 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새 버전으로 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 주의 깊게 확인해야 합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용해 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

그 다음, `vendor:publish` Artisan 명령어를 사용해 Cashier 마이그레이션 파일을 발행하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. Cashier 마이그레이션은 `customers` 테이블과 고객 구독을 저장할 `subscriptions`, `subscription_items` 테이블, 그리고 Paddle 거래 내역을 저장할 `transactions` 테이블을 생성합니다:

```shell
php artisan migrate
```

> [!WARNING]  
> Cashier가 모든 Paddle 이벤트를 제대로 처리하도록 [웹훅 핸들링 설정](#handling-paddle-webhooks)을 반드시 해주세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스 (Paddle Sandbox)

로컬 및 스테이징 단계 개발 중에는 [Paddle 샌드박스 계정 등록](https://sandbox-login.paddle.com/signup)을 추천합니다. 이 계정으로 실제 결제 없이 안전하게 테스트 환경을 마련할 수 있습니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card)를 활용해 다양한 결제 상황을 시뮬레이션할 수 있습니다.

샌드박스 환경을 사용하는 경우, `.env` 파일 내의 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다:

```ini
PADDLE_SANDBOX=true
```

개발이 완료되면 [Paddle 판매자 계정](https://paddle.com)을 신청하실 수 있습니다. 애플리케이션을 프로덕션에 배포하기 전에 Paddle이 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 가능한 모델 (Billable Model)

Cashier를 사용하기 전에 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 수단 정보 업데이트 등 일반적인 청구 작업 수행에 필요한 여러 메서드를 제공합니다:

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 청구 가능한 엔티티가 있다면, 해당 클래스에 이 트레이트를 추가하면 됩니다:

```
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키 (API Keys)

`.env` 파일에 Paddle API 키들을 설정하세요. Paddle 제어판에서 키를 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle 샌드박스 환경](#paddle-sandbox)을 사용할 때 `true`로, 라이브 환경에서는 `false`로 설정합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며, [Retain 기능](https://developer.paddle.com/paddlejs/retain)을 사용할 때만 설정하세요.

<a name="paddle-js"></a>
### Paddle JS

Paddle 결제 위젯을 시작하려면 Paddle의 JavaScript 라이브러리를 로드해야 합니다. 애플리케이션 레이아웃의 `</head>` 닫는 태그 바로 전에 `@paddleJS` Blade 디렉티브를 삽입하세요:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

송장에 금액을 표시할 때 사용할 로케일(locale)을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 통해 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 외 다른 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 기능이 설치 및 활성화되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

Cashier가 내부적으로 사용하는 모델들을 확장하려면, 자신만의 모델을 정의하고 해당 Cashier 모델을 상속받으세요:

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

이후, `Laravel\Paddle\Cashier` 클래스에 커스텀 모델을 사용하도록 알려줍니다. 보통은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 설정합니다:

```
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
```

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

<a name="quickstart-selling-products"></a>
### 제품 판매하기 (Selling Products)

> [!NOTE]  
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격이 있는 제품(Products)을 먼저 정의하세요. 또한, [Paddle 웹훅 설정](#handling-paddle-webhooks)도 해야 합니다.

애플리케이션에서 제품 및 구독 결제 기능을 추가하는 일은 복잡할 수 있지만, Cashier와 [Paddle의 Checkout Overlay](https://www.paddle.com/billing/checkout) 덕분에 견고하고 현대적인 결제 통합을 쉽게 만들 수 있습니다.

비구독성(한번 결제) 제품을 판매하고자 할 때는, Cashier를 사용해 고객을 Paddle의 Checkout Overlay로 이동시켜 결제를 진행하도록 합니다. 결제가 완료되면 고객을 애플리케이션 내 원하는 성공 페이지로 리다이렉트합니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예시에서, 우리는 `checkout` 메서드를 통해 Paddle Checkout Overlay를 위한 체크아웃 객체를 생성합니다. Paddle에서는 "price identifier"가 [특정 제품 가격을 의미합니다](https://developer.paddle.com/build/products/create-products-prices).

필요할 경우, `checkout` 메서드는 Paddle에서 고객을 자동으로 생성하고 해당 고객 기록을 애플리케이션 사용자와 연결합니다. 결제 완료 후에는 고객이 지정한 성공 페이지로 이동됩니다.

`buy` 뷰에서 Checkout Overlay를 표시할 버튼을 추가할 수 있습니다. `paddle-button` Blade 컴포넌트는 Cashier Paddle에 내장되어 있습니다. 물론 직접 [오버레이 결제 화면을 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타 데이터 전달하기

클래스 내에서 자체적으로 정의한 `Cart`와 `Order` 모델을 사용해 완료된 주문과 구입 내역을 추적하는 경우가 많습니다. Paddle Checkout Overlay로 리다이렉트 할 때 이미 존재하는 주문 ID를 제공하여 백엔드에서 구매 내역과 연결할 필요가 있을 수 있습니다.

예를 들어, 사용자가 결제 프로세스를 시작할 때 애플리케이션에서 '미완료' 상태의 `Order`를 생성할 수 있습니다. 아래 코드는 `Cart`와 `Order`가 예시일 뿐 Cashier에 포함된 모델은 아닙니다. 필요에 따라 구현하세요:

```
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
```

위 예시는, 사용자가 결제를 시작할 때 장바구니와 주문에 연결된 Paddle 가격 ID 배열을 `checkout` 메서드에 넘깁니다. 주문 ID도 `customData` 메서드로 Paddle Checkout Overlay에 전달합니다.

구매 완료 시 주문 상태를 "완료"로 변경하고자 한다면, Paddle에서 발생하는 웹훅을 Cashier 이벤트 리스너로 처리해 데이터베이스에 저장할 수 있습니다.

시작점으로 `TransactionCompleted` 이벤트를 수신하는 리스너를 `AppServiceProvider`의 `boot` 메서드에 등록하는 예시는 다음과 같습니다:

```
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
```

`CompleteOrder` 리스너 예시는 아래와 같습니다:

```
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

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
```

자세한 페이로드 정보는 Paddle 문서에서 [`transaction.completed` 이벤트](https://developer.paddle.com/webhooks/transactions/transaction-completed)를 확인하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매하기 (Selling Subscriptions)

> [!NOTE]  
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격이 있는 제품을 먼저 정의하고 [웹훅 설정](#handling-paddle-webhooks)을 완료해야 합니다.

제품과 구독 결제를 앱에 도입하는 것은 부담스러울 수 있으나, Cashier와 Paddle의 Checkout Overlay 덕분에 쉽고 견고한 결제 기능을 구축할 수 있습니다.

예를 들어, 기본 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 플랜이 있는 구독 서비스를 가정해봅시다. 이 두 가격은 Paddle 대시보드 내 "Basic" 제품(`pro_basic`) 아래 묶여 있을 수 있습니다. 전문 플랜은 `pro_expert`로 제공할 수도 있습니다.

구매자가 구독을 시작하는 방법을 살펴보겠습니다. 예를 들어, 사용자가 앱 가격 페이지에서 Basic 플랜의 "구독" 버튼을 클릭하면 Paddle Checkout Overlay가 실행됩니다. 다음은 Checkout 세션을 생성하는 방법입니다:

```
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에 Checkout Overlay를 표시할 버튼을 추가합니다. `paddle-button` Blade 컴포넌트가 Cashier Paddle에 내장되어 있으나, 직접 [오버레이 결제 렌더링](#manually-rendering-an-overlay-checkout)도 가능합니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

구독 버튼 클릭 시 고객은 결제 정보를 입력하고 구독을 시작할 수 있습니다. 구독 시작 시점은 일부 결제수단 처리 지연이 있을 수 있으므로, 반드시 [웹훅 처리](#handling-paddle-webhooks)도 함께 설정하세요.

사용자가 구독상태인지 판단해 앱 내 접근을 제한하고 싶다면, Billable 트레이트의 `subscribed` 메서드를 활용하세요:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 제품이나 가격에 대한 구독 여부도 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 상태 미들웨어 만들기

편의를 위해, 요청자를 구독자 여부로 판별하는 [미들웨어](/docs/11.x/middleware)를 생성할 수 있습니다. 미들웨어 등록 후 구독하지 않은 사용자의 접근을 쉽게 막을 수 있습니다:

```
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
            // 청구 페이지로 리다이렉트하여 구독하도록 안내...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어를 라우트에 할당하는 방법:

```
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 결제 플랜 관리하기 허용하기

고객이 구독 플랜을 변경하도록 지원하는 것도 중요합니다. 예를 들어 월간 플랜에서 연간 플랜으로 변경하길 원할 수 있습니다. 다음은 해당 라우트 예시입니다:

```
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 예: "price_basic_yearly"

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

구독 취소 기능도 제공합니다:

```
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

구독 취소 후에는 해당 구독이 현재 결제 주기 종료 시점에 취소됩니다.

> [!NOTE]  
> 웹훅 설정이 되어 있다면 Paddle 대시보드에서 구독을 취소할 경우에도 Cashier가 자동으로 데이터베이스를 동기화합니다.

<a name="checkout-sessions"></a>
## 결제 세션 (Checkout Sessions)

대부분의 결제 작업은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통해 이루어집니다.

결제 전에 Paddle 대시보드에서 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 설정해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 결제 (Overlay Checkout)

Checkout Overlay를 표시하기 전에 Cashier로 체크아웃 세션을 생성해야 합니다. 체크아웃 세션은 위젯에 수행할 청구 작업을 알립니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier의 `paddle-button` [Blade 컴포넌트](/docs/11.x/blade#components)에 체크아웃 세션을 전달할 수 있습니다. 버튼 클릭 시 Paddle 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본 스타일 대신 [Paddle 지원 속성들](https://developer.paddle.com/paddlejs/html-data-attributes)을 추가해 위젯을 커스터마이징할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 위젯은 비동기 방식입니다. 구독 생성 후 Paddle이 웹훅을 전송하므로, 꼭 [웹훅 설정](#handling-paddle-webhooks)을 해 구독 상태 변경에 대비하세요.

> [!WARNING]  
> 구독 상태 변경 후 웹훅 수신까지 딜레이가 있을 수 있으니, 구독 완료 직후에 상태가 바로 반영되지 않을 수도 있음을 고려하세요.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 수동으로 오버레이 결제 렌더링하기

Laravel Blade 컴포넌트를 사용하지 않고 직접 Overlay Checkout을 띄울 수도 있습니다. 먼저 체크아웃 세션을 생성하세요:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Blade 뷰 내에서 Paddle.js를 사용해 초기화합니다. 아래는 `paddle_button` 클래스를 가진 링크를 클릭 시 Overlay가 나타나도록 하는 예시입니다:

```blade
<?php
$items = $checkout->getItems();
$customer = $checkout->getCustomer();
$custom = $checkout->getCustomData();
?>

<a
    href='#!'
    class='paddle_button'
    data-items='{!! json_encode($items) !!}'
    @if ($customer) data-customer-id='{{ $customer->paddle_id }}' @endif
    @if ($custom) data-custom-data='{{ json_encode($custom) }}' @endif
    @if ($returnUrl = $checkout->getReturnUrl()) data-success-url='{{ $returnUrl }}' @endif
>
    Buy Product
</a>
```

<a name="inline-checkout"></a>
### 인라인 결제 (Inline Checkout)

Overlay 위젯 대신 인라인 방식으로도 결제 화면을 앱 내부에 직접 삽입할 수 있습니다. 다만 HTML 필드를 수정하는 등의 커스터마이징은 불가능합니다.

Cashier는 인라인 결제 쉽게 시작하도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. 먼저 [체크아웃 세션을 생성](#overlay-checkout)하세요:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그런 다음 컴포넌트에 체크아웃 세션을 전달합니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 컴포넌트 높이 조정은 `height` 속성으로 수행합니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

더 자세한 설정은 Paddle의 [인라인 결제 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [설정 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 수동으로 인라인 결제 렌더링하기

Blade 컴포넌트를 쓰지 않고 직접 인라인 결제를 띄울 수도 있습니다. 먼저 체크아웃 세션을 생성하세요:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Alpine.js를 활용한 Paddle.js 초기화 예시는 다음과 같습니다. 필요한 경우 다른 프론트엔드 스택에 맞게 수정하세요:

```blade
<?php
$options = $checkout->options();

$options['settings']['frameTarget'] = 'paddle-checkout';
$options['settings']['frameInitialHeight'] = 366;
?>

<div class="paddle-checkout" x-data="{}" x-init="
    Paddle.Checkout.open(@json($options));
">
</div>
```

<a name="guest-checkouts"></a>
### 게스트 결제 (Guest Checkouts)

계정이 필요 없는 비회원 결제 세션도 생성할 수 있습니다. `guest` 메서드를 사용하세요:

```
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

생성한 체크아웃 세션을 [Paddle 버튼](#overlay-checkout)이나 [인라인 결제 컴포넌트](#inline-checkout)에 전달해 사용하세요.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle은 각 통화별로 가격을 다르게 설정할 수 있습니다. Cashier Paddle의 `previewPrices` 메서드는 원하는 가격 ID들의 가격 정보를 조회합니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

기본 통화는 요청 IP 기반으로 결정되지만, 특정 국가를 지정할 수도 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회한 가격들은 자유롭게 화면에 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

부분별 금액, 예를 들어 세금 제외 금액과 세금만 분리해서 출력할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

더 자세한 내용은 [Paddle 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객 가격 미리보기 (Customer Price Previews)

이미 고객이 있는 경우, 해당 고객 인스턴스에서 직접 가격 정보를 조회할 수 있습니다:

```
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Cashier는 내부적으로 사용자에게 연결된 Paddle 고객 ID를 이용해 그 사용자의 통화에 맞는 가격을 조회합니다. 예를 들어 미국 사용자는 미국 달러로, 벨기에 사용자는 유로화로 가격을 표시합니다. 일치하는 통화가 없으면 제품의 기본 통화가 사용됩니다.

가격 설정은 Paddle 대시보드에서 제품이나 구독 플랜별로 조정할 수 있습니다.

<a name="price-discounts"></a>
### 할인 (Discounts)

할인 적용 가격도 조회할 수 있습니다. `previewPrices` 호출 시 `discount_id` 옵션에 할인 ID를 전달하세요:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격은 이렇게 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
## 고객 (Customers)

<a name="customer-defaults"></a>
### 고객 기본값 (Customer Defaults)

Checkout 세션 생성 시 고객 이메일, 이름 등 기본 정보를 채워 결제 과정을 간소화할 수 있습니다. Billable 모델에 아래 메서드를 재정의해 설정하세요:

```
/**
 * Paddle에 연결할 고객 이름 반환.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Paddle에 연결할 고객 이메일 반환.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이 기본값은 [체크아웃 세션 생성](#checkout-sessions) 시 자동으로 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

Paddle 고객 ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 이 메서드는 Billable 모델 인스턴스를 반환합니다:

```
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

구독 시작 없이 Paddle 고객만 생성하고자 할 때는, Billable 인스턴스의 `createAsCustomer` 메서드를 사용하세요:

```
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스가 반환됩니다. 추가 [Paddle 고객 생성 API 옵션](https://developer.paddle.com/api-reference/customers/create-customer)을 `$options` 배열로 전달할 수도 있습니다:

```
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독 생성은 Billable 모델 인스턴스를 조회 후 `subscribe` 메서드를 호출해 체크아웃 세션을 만들며 이루어집니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 12345, 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

첫 번째 인자는 Paddle 가격 ID이며, 두 번째 인자는 내부 구독 타입 식별자입니다. 단일 구독만 있다면 `default` 혹은 `primary`로 명명하세요. 이 타입은 사용자에게 공개되지 않고, 한 번 생성되면 변경하지 않는 것이 좋습니다.

`customData` 메서드로 구독에 추가 메타데이터를 전달할 수도 있습니다:

```
$checkout = $request->user()->subscribe($premium = 12345, 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

체크아웃 세션을 `paddle-button` 컴포넌트에 전달해서 결제 버튼을 만들 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

결제가 완료되고 Paddle에서 `subscription_created` 웹훅이 전송되면 Cashier가 구독 정보를 애플리케이션 데이터베이스에 저장합니다. 웹훅 설정을 꼭 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

사용자가 구독 중인지 확인하려면 여러 편리한 메서드를 사용할 수 있습니다. 가장 단순한 `subscribed` 메서드는 유효한 구독이 있으면 `true`를 반환하며, 평가판 기간 중인 경우도 포함됩니다:

```
if ($user->subscribed()) {
    // ...
}
```

구독 타입이 여러 개라면, `subscribed` 메서드에 타입을 명시할 수 있습니다:

```
if ($user->subscribed('default')) {
    // ...
}
```

이를 [미들웨어](/docs/11.x/middleware)에서 활용해 경로 접근을 제한할 수도 있습니다.

평가판 기간인지 확인하려면 `onTrial` 메서드를 사용하세요:

```
if ($user->subscription()->onTrial()) {
    // 평가판 기간임
}
```

특정 가격에 구독 중인지 확인하려면 `subscribedToPrice`를 사용합니다:

```
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // 월간 플랜에 구독 중
}
```

현재 활성 구독이며 평가판도 아니고 유예 기간도 아닌 상태 확인은 `recurring` 메서드로 합니다:

```
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태 (Canceled Subscription Status)

과거에 활성 구독이었지만 취소한 구독인지 확인할 때는 `canceled` 메서드를 사용합니다:

```
if ($user->subscription()->canceled()) {
    // ...
}
```

아직 구독 종료일 전 유예 기간이면 `onGracePeriod`가 `true`를 반환합니다. 이때 `subscribed` 메서드도 `true`입니다:

```
if ($user->subscription()->onGracePeriod()) {
    // 유예 기간 중
}
```

<a name="past-due-status"></a>
#### 연체 상태 (Past Due Status)

구독 결제 실패가 발생해 `past_due` 상태가 되면 구독은 비활성화되며, 고객이 결제 정보를 업데이트해야 활성화됩니다. `pastDue` 메서드로 상태를 확인하세요:

```
if ($user->subscription()->pastDue()) {
    // ...
}
```

이 경우 사용자에게 [결제 정보 업데이트](#updating-payment-information)를 안내해야 합니다.

만약 `past_due` 구독도 활성 상태로 간주하고 싶으면, `AppServiceProvider`의 `register` 메서드 내에서 다음을 호출하세요:

```
use Laravel\Paddle\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]  
> `past_due` 상태 구독은 결제 정보 업데이트가 필요하므로, `swap` 또는 `updateQuantity` 메서드 호출 시 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 스코프 (Subscription Scopes)

구독 상태에 따른 쿼리 스코프도 제공되므로, 조건에 맞는 구독만 쉽게 조회할 수도 있습니다:

```
// 유효한 구독 모두 조회
$subscriptions = Subscription::query()->valid()->get();

// 특정 사용자의 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 스코프 목록:

```
Subscription::query()->valid();
Subscription::query()->onTrial();
Subscription::query()->expiredTrial();
Subscription::query()->notOnTrial();
Subscription::query()->active();
Subscription::query()->recurring();
Subscription::query()->pastDue();
Subscription::query()->paused();
Subscription::query()->notPaused();
Subscription::query()->onPausedGracePeriod();
Subscription::query()->notOnPausedGracePeriod();
Subscription::query()->canceled();
Subscription::query()->notCanceled();
Subscription::query()->onGracePeriod();
Subscription::query()->notOnGracePeriod();
```

<a name="subscription-single-charges"></a>
### 구독 단일 청구 (Subscription Single Charges)

구독에 단일 청구(일회성 청구)를 추가할 수 있습니다. `charge` 메서드에 단일 또는 다수의 가격 ID를 전달하세요:

```
// 단일 가격 청구
$response = $user->subscription()->charge('pri_123');

// 다중 가격 동시 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge`는 실제 청구를 다음 결제 주기 때까지 미룹니다. 즉시 청구하려면 `chargeAndInvoice` 메서드를 사용하세요:

```
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트 (Updating Payment Information)

Paddle은 구독별로 결제 수단을 저장합니다. 기본 결제 수단을 바꾸려면 구독 모델의 `redirectToUpdatePaymentMethod` 메서드를 사용해 Paddle 호스팅 결제수단 변경 페이지로 리다이렉트하세요:

```
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

수정이 완료되면 Paddle이 `subscription_updated` 웹훅을 보내 구독 정보를 업데이트합니다.

<a name="changing-plans"></a>
### 플랜 변경 (Changing Plans)

사용자가 구독 플랜을 변경하고자 할 때는 `swap` 메서드에 새 가격 ID를 전달합니다:

```
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

바로 청구하고 싶다면 `swapAndInvoice`를 사용하세요:

```
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 비례 계산 (Prorations)

기본적으로 Paddle은 플랜 변경 시 비례 계산을 적용합니다. 비례 계산 없이 변경하려면 `noProrate` 메서드를 붙이세요:

```
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

즉시 청구까지 하고 싶으면 이렇게 사용합니다:

```
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

청구하지 않고 변경하려면 `doNotBill` 메서드를 사용하세요:

```
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

비례 계산 정책에 대한 자세한 내용은 Paddle의 [비례 계산 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

일부 구독은 수량 기반일 수 있습니다. 예를 들어 프로젝트 관리 앱에서는 프로젝트당 월 10달러가 청구될 수 있습니다.

수량을 편리하게 늘리거나 줄이려면 `incrementQuantity` / `decrementQuantity` 메서드를 사용하세요:

```
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 현재 수량에 5 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 현재 수량에서 5 감소
$user->subscription()->decrementQuantity(5);
```

원하는 수량으로 직접 설정하려면 `updateQuantity` 메서드를 사용합니다:

```
$user->subscription()->updateQuantity(10);
```

비례 계산 없이 수량을 변경하려면 `noProrate` 메서드를 호출 후 수행하세요:

```
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 제품 구독 시 수량 지정

여러 제품이 포함된 구독이라면, 변경할 가격 ID를 두 번째 인자로 전달해야 합니다:

```
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 제품 구독 (Subscriptions With Multiple Products)

[Paddle의 다중 제품 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)은 한 구독에 여러 제품을 결제할 수 있게 합니다.

예를 들어, 기반 구독 월 10달러에 라이브 채팅 부가상품 $15를 추가하는 고객 서비스 앱을 생각해봅시다.

구독 체크아웃 생성 시 가격 배열을 넘겨 여러 제품을 포함시킬 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe([
        'price_monthly',
        'price_chat',
    ]);

    return view('billing', ['checkout' => $checkout]);
});
```

위 경우 고객은 `default` 구독에 2개의 가격이 붙으며 각각 청구됩니다.

수량을 지정하려면 연관 배열 형태로 전달하세요:

```
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 가격을 추가하려면, 현재 가격 및 수량과 함께 `swap`을 호출합니다:

```
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

추가 가격은 다음 결제 주기 때 청구되며, 즉시 청구하려면 `swapAndInvoice`를 사용하세요:

```
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

가격을 제외하려면 `swap`에서 빼면 됩니다:

```
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]  
> 구독에서 마지막 가격은 절대 제외할 수 없습니다. 구독을 완전히 종료하려면 취소하세요.

<a name="multiple-subscriptions"></a>
### 다중 구독 (Multiple Subscriptions)

Paddle은 한 고객이 여러 구독을 동시에 가질 수 있게 지원합니다. 예를 들어 헬스장 회원이 수영 구독과 웨이트 트레이닝 구독을 별도로 가입하는 상황입니다.

구독 생성 시 `subscribe` 메서드 두 번째 인자로 구독 타입을 넘깁니다:

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

나중에 변경하려면 `swimming` 타입 구독에서 가격을 바꿉니다:

```
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

전체 취소도 가능합니다:

```
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시중지 (Pausing Subscriptions)

구독을 일시중지하려면 `pause` 메서드를 호출하세요:

```
$user->subscription()->pause();
```

일시중지하면 DB의 `paused_at` 컬럼이 설정됩니다. 예를 들어 결제 주기 종료일 전이라면 `paused` 메서드는 일시중지로 판단하지 않습니다. 왜냐하면 사용자가 이미 결제한 기간 중에는 계속 사용 가능하기 때문입니다.

기본적으로 중지는 다음 결제 주기에 이루어집니다. 즉시 중지하려면 `pauseNow`를 사용하세요:

```
$user->subscription()->pauseNow();
```

특정 기간 동안 일시중지하려면 `pauseUntil`을 사용하고 즉시 시작하려면 `pauseNowUntil`을 사용하세요:

```
$user->subscription()->pauseUntil(now()->addMonth());

$user->subscription()->pauseNowUntil(now()->addMonth());
```

일시중지 중이지만 유예기간인 경우 다음과 같이 확인합니다:

```
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시중지한 구독을 다시 활성화하려면 `resume`을 호출하세요:

```
$user->subscription()->resume();
```

> [!WARNING]  
> 일시중지 상태에서는 구독 변경(플랜 변경, 수량 조정 등)이 불가능합니다. 변경 전에 반드시 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소 (Canceling Subscriptions)

구독을 취소하려면 `cancel` 메서드를 호출하세요:

```
$user->subscription()->cancel();
```

취소 시 DB의 `ends_at` 컬럼이 설정됩니다. 구독 종료일까지는 여전히 활성 상태(`subscribed` 메서드가 참)로 간주됩니다.

유예기간인지 확인하려면:

```
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow`를 사용하세요:

```
$user->subscription()->cancelNow();
```

유예기간에서 취소를 중단하려면 `stopCancelation`을 호출합니다:

```
$user->subscription()->stopCancelation();
```

> [!WARNING]  
> Paddle 구독은 취소 후 재개할 수 없습니다. 다시 구독하려면 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 평가판 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단을 미리 받는 경우 (With Payment Method Up Front)

결제 수단 정보를 미리 받은 상태에서 평가판을 제공하려면, Paddle 대시보드에서 가격에 평가판 기간을 설정하세요. 그 후 평소처럼 체크아웃 세션을 생성합니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트 수신 시, Cashier가 DB 구독 레코드에 평가판 종료일을 저장하고 Paddle이 해당일까지 청구를 미루도록 지시합니다.

> [!WARNING]  
> 평가판 종료일 전에 구독이 취소되지 않으면, 평가판 종료 시점에 자동으로 청구되니 사용자에게 종료일을 알려야 합니다.

평가판 여부 판단은 `User`나 `Subscription` 인스턴스의 `onTrial` 메서드를 사용하면 됩니다:

```
if ($user->onTrial()) {
    // ...
}

if ($user->subscription()->onTrial()) {
    // ...
}
```

기존 평가판 만료 확인도 가능합니다:

```
if ($user->hasExpiredTrial()) {
    // ...
}

if ($user->subscription()->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입 평가판 여부를 판단하려면, 타입을 메서드에 인자로 넘기세요:

```
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 제공하는 경우 (Without Payment Method Up Front)

결제 수단 미등록 상태로 평가판을 제공하려면, 사용자에게 연결된 Paddle 고객 레코드의 `trial_ends_at` 컬럼에 평가판 종료일을 설정하세요. 보통 가입 시점에 설정합니다:

```
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

Cashier에서는 이 평가판을 "일반 평가판(generic trial)"이라 부릅니다. `User` 인스턴스의 `onTrial`은 현재 날짜가 `trial_ends_at` 이전이라면 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 평가판 기간 중임
}
```

구독이 필요할 때는 기존대로 `subscribe` 메서드를 사용해 생성하세요:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

평가판 종료일은 `trialEndsAt` 메서드로 받으며, 구독 타입 인자도 전달 가능합니다:

```
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

특히 일반 평가판 상태인지 확인하려면 `onGenericTrial` 메서드를 사용하면 됩니다:

```
if ($user->onGenericTrial()) {
    // 일반 평가판 상태
}
```

<a name="extend-or-activate-a-trial"></a>
### 평가판 연장 또는 활성화 (Extend or Activate a Trial)

구독 평가판 기간을 연장하려면 `extendTrial` 메서드에 새 종료일을 전달하세요:

```
$user->subscription()->extendTrial(now()->addDays(5));
```

즉시 평가판을 종료하고 구독을 활성화하려면 `activate` 메서드를 호출합니다:

```
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트를 웹훅으로 알립니다. 기본적으로 Cashier의 서비스 프로바이더가 웹훅 컨트롤러용 라우트를 등록하며, 모든 웹훅 요청을 처리합니다.

이 컨트롤러는 자동으로 실패한 청구로 구독 취소, 구독 정보 업데이트, 결제 수단 변경을 처리하지만, 필요 시 확장해 원하는 이벤트를 핸들링할 수 있습니다.

앱이 Paddle 웹훅을 받을 수 있도록 Paddle 제어판에서 [웹훅 URL을 등록](https://vendors.paddle.com/alerts-webhooks)하세요. 기본 경로는 `/paddle/webhook`입니다. 아래 웹훅들은 반드시 활성화하세요:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]  
> Cashier에 포함된 [웹훅 서명 검증](/docs/11.x/cashier-paddle#verifying-webhook-signatures) 미들웨어로 들어오는 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅은 Laravel의 [CSRF 보호](/docs/11.x/csrf)를 우회해야 하므로, `paddle/*` 경로를 CSRF 검증 예외로 등록해야 합니다. 예시는 `bootstrap/app.php` 내 다음과 같이 설정하세요:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 웹훅과 로컬 개발

Paddle이 로컬 개발 중인 애플리케이션에 웹훅을 전달하려면, Ngrok(https://ngrok.com/) 또는 Expose(https://expose.dev/docs/introduction) 같은 사이트 공유 서비스를 이용해 외부에서 접근 가능해야 합니다. Laravel Sail을 활용하는 경우에도 Sail의 [사이트 공유 명령어](/docs/11.x/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 구독 취소와 같은 일반적인 웹훅을 자동 처리하지만, 추가적으로 이벤트를 처리하려면 다음과 같은 이벤트 리스너를 정의하세요:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `transaction.billed` 이벤트를 처리하는 리스너 예시는 다음과 같습니다:

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Handle received Paddle webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // 이벤트 처리...
        }
    }
}
```

또한 Cashier는 각 웹훅 유형별로 전용 이벤트를 발행합니다. 이 이벤트에는 페이로드뿐 아니라 관련 Billable 모델, 구독, 영수증 등도 포함됩니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

디폴트 웹훅 경로를 변경하려면 `.env` 파일에 `CASHIER_WEBHOOK` 환경 변수를 등록하세요. 이 값은 Paddle 대시보드에 등록된 URL과 일치해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증 (Verifying Webhook Signatures)

웹훅 보안을 위해 [Paddle의 웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 사용할 수 있습니다. Cashier는 자동으로 Paddle 웹훅 요청이 유효한지 검증하는 미들웨어를 포함합니다.

웹훅 서명 검증을 활성화하려면 `.env` 파일에 `PADDLE_WEBHOOK_SECRET` 환경 변수를 설정하세요. 이 비밀키는 Paddle 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 청구 (Single Charges)

<a name="charging-for-products"></a>
### 제품 청구 (Charging for Products)

특정 제품에 대해 고객에게 청구를 시작하려면 Billable 인스턴스의 `checkout` 메서드를 사용해 체크아웃 세션을 생성하세요. 가격 ID를 단일 또는 복수로 전달할 수 있으며, 수량도 연관 배열로 지정할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

생성한 체크아웃 세션은 `paddle-button` [Blade 컴포넌트](#overlay-checkout)를 통해 사용자에게 Paddle 결제 위젯을 보여주도록 할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`customData` 메서드로 거래 생성 시 추가 커스텀 데이터를 전달할 수도 있습니다. 관련 옵션은 [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요:

```
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 결제 환불 (Refunding Transactions)

환불 시 결제된 금액이 고객 결제 수단으로 돌아갑니다. Paddle 구매 환불은 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드로 처리합니다. 첫 번째 인자에 환불 이유, 두 번째에 환불할 가격 ID 및 금액(부분 환불 시)을 담을 수 있습니다. 거래는 Billable 모델의 `transactions` 메서드로 조회 가능합니다.

예를 들어, 한 거래에서 가격 `pri_123`은 전액 환불, `pri_456`은 2달러만 환불할 때:

```
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 부분 환불(센트 단위)
]);
```

전체 거래를 환불하려면 이유만 넘기면 됩니다:

```
$response = $transaction->refund('Accidental charge');
```

자세한 내용은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]  
> 환불은 Paddle 승인 후에만 최종 처리됩니다.

<a name="crediting-transactions"></a>
### 거래 크레딧 (Crediting Transactions)

환불과 비슷하게, 크레딧은 고객 잔고에 금액을 적립해 향후 결제에 사용할 수 있도록 합니다. 다만 수동 결제 건에만 가능하며, 구독 같은 자동 결제 건은 Paddle이 직접 처리합니다:

```
$transaction = $user->transactions()->first();

// 특정 항목 전체 크레딧 적립
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle 크레딧 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]  
> 자동 결제 거래에는 크레딧을 적용할 수 없습니다.

<a name="transactions"></a>
## 거래 내역 (Transactions)

Billable 모델의 `transactions` 속성으로 거래 내역을 쉽게 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래 내역은 제품 구매 결제에 해당하며, 청구서와 함께 저장됩니다. 애플리케이션 DB에는 완료된 거래만 기록됩니다.

거래 목록을 테이블로 보여주고, 사용자가 청구서를 다운로드하도록 할 수도 있습니다:

```html
<table>
    @foreach ($transactions as $transaction)
        <tr>
            <td>{{ $transaction->billed_at->toFormattedDateString() }}</td>
            <td>{{ $transaction->total() }}</td>
            <td>{{ $transaction->tax() }}</td>
            <td><a href="{{ route('download-invoice', $transaction->id) }}" target="_blank">Download</a></td>
        </tr>
    @endforeach
</table>
```

`download-invoice` 경로는 다음과 같이 구성할 수 있습니다:

```
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정 결제 (Past and Upcoming Payments)

구독의 과거 결제 및 예정 결제를 조회하려면 `lastPayment` 및 `nextPayment` 메서드를 사용하세요:

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 `Laravel\Paddle\Payment` 인스턴스를 반환하며, `lastPayment`는 아직 웹훅 동기화 전이면 `null` 일 수 있고, `nextPayment`는 구독 종료 시점이면 `null`을 반환합니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시, 실제 청구 절차가 정상 동작하는지 수동으로 확인하세요.

자동화 테스트(CI 환경 포함)에서는 [Laravel HTTP 클라이언트](/docs/11.x/http-client#testing)를 사용해 Paddle로의 HTTP 호출을 가짜로 만들어 테스트할 수 있습니다. 이 방법은 Paddle 응답을 실제로 검증하진 않지만, API 호출 없이도 앱의 흐름을 검사할 수 있습니다.