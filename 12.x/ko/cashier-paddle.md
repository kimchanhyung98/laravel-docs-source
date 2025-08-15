# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [설정](#configuration)
    - [청구 가능(Billable) 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 상품 판매](#quickstart-selling-subscriptions)
- [체크아웃 세션](#checkout-sessions)
    - [오버레이 체크아웃](#overlay-checkout)
    - [인라인 체크아웃](#inline-checkout)
    - [비회원 체크아웃](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객별 가격 미리보기](#customer-price-previews)
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
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [결제 정보 선등록 체험](#with-payment-method-up-front)
    - [결제 정보 없이 체험](#without-payment-method-up-front)
    - [체험 기간 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [상품 결제](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧](#crediting-transactions)
- [거래 내역](#transactions)
    - [과거 및 예정된 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Paddle Billing과의 Cashier Paddle 2.x 통합을 위한 문서입니다. 만약 여전히 Paddle Classic을 사용 중이시라면, [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 참고하세요.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 빌링 서비스를 쉽고 유연하게 사용할 수 있는 인터페이스를 제공합니다. Cashier는 복잡하고 반복적인 구독 처리 코드를 대신 처리해주기 때문에 개발자는 핵심 로직에 집중할 수 있습니다. 기본적인 구독 관리 외에도 Cashier는 플랜 교체, 구독 "수량" 관리, 일시정지, 취소 유예 기간 등 다양한 기능을 제공합니다.

Cashier Paddle을 본격적으로 사용하기 전에, Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 살펴보실 것을 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 주의 깊게 확인하시기 바랍니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용하여 Paddle용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier-paddle
```

그 다음, `vendor:publish` Artisan 명령어를 사용하여 Cashier 마이그레이션 파일을 배포합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 애플리케이션의 데이터베이스 마이그레이션을 실행하십시오. Cashier 마이그레이션은 새 `customers` 테이블을 생성합니다. 또한, 고객의 구독 정보를 저장할 `subscriptions` 및 `subscription_items` 테이블이, 고객과 연관된 Paddle 거래 내역을 저장할 `transactions` 테이블도 생성됩니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리할 수 있도록 반드시 [Cashier의 Webhook 처리를 설정](#handling-paddle-webhooks)해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle Sandbox

로컬 및 스테이징 개발 중에는 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)을 등록하여 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있습니다. 다양한 결제 시나리오를 시뮬레이션하기 위해 Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용할 수 있습니다.

Paddle Sandbox 환경을 사용할 때는 애플리케이션의 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다:

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발을 마친 후, [Paddle 벤더 계정 신청](https://paddle.com)을 통해 운영 환경으로 전환할 수 있습니다. 운영 환경에 배포하기 전에는 Paddle의 승인을 받아야 하며, Paddle은 애플리케이션의 도메인을 확인합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 가능(Billable) 모델

Cashier를 사용하기 전에, `Billable` 트레이트를 사용자 모델(User) 정의에 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 업데이트 등 여러 청구 작업을 위한 다양한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 다른 엔티티도 청구가 가능하다면 해당 클래스에도 이 트레이트를 추가할 수 있습니다:

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

다음으로, Padde API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Paddle API 키들은 Paddle 관리 페이지에서 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle Sandbox 환경](#paddle-sandbox) 사용 시 `true`, 운영 환경에서는 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택적으로, Paddle의 [Retain](https://developer.paddle.com/concepts/retain/overview) 기능을 사용할 경우에만 설정하면 됩니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 결제 위젯을 띄우기 위해 자체 JavaScript 라이브러리를 사용합니다. 이 라이브러리는 애플리케이션 레이아웃의 `</head>` 태그 바로 앞에 `@paddleJS` Blade 디렉티브를 추가하여 로드할 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

금액을 인보이스 등에 표시할 때 사용할 로케일(locale)을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용해 통화를 포맷합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치·설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier가 사용하는 기본 모델을 자유롭게 확장하여 커스텀 모델로 교체할 수 있습니다. Cashier 모델을 상속받아 본인만의 모델을 만들고:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

이후, `Laravel\Paddle\Cashier` 클래스의 메서드를 통해 Cashier에게 커스텀 모델을 알려줄 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 설정합니다:

```php
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
### 상품 판매 (Selling Products)

> [!NOTE]
> Paddle Checkout 사용 전에는 반드시 Paddle 대시보드에서 고정 가격의 상품(Products)과 가격(Prices)을 정의해야 합니다. 또한, [Paddle의 webhook 처리를 설정](#handling-paddle-webhooks)해야 합니다.

애플리케이션 내에서 상품 및 구독 결제를 제공하는 일은 처음에는 어렵게 느껴질 수 있습니다. 그러나 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 활용하면 강력하고 현대적인 결제 연동을 쉽게 만들 수 있습니다.

일회성 단일 상품을 판매하기 위해 Cashier의 `checkout` 메서드를 사용하여 Paddle Checkout Overlay를 통한 결제 세션을 생성할 수 있습니다. 사용자는 위젯에서 결제 정보 입력 후 구매를 완료합니다. 결제가 성공하면, 고객은 애플리케이션 내의 원하는 성공 URL로 리다이렉트됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제에서는 가격 식별자("price identifier")를 넘겨서 checkout 객체를 생성하고 고객에게 Paddle의 Checkout Overlay UI를 보여줍니다. Paddle에서 "prices"는 [특정 상품에 대해 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요하다면 `checkout` 메서드는 Paddle에 고객을 자동 생성하고, Paddle 고객 레코드를 애플리케이션 사용자와 연결합니다. 체크아웃 세션이 끝나면 고객은 별도의 성공 페이지로 이동되어 추가 메시지를 안내할 수 있습니다.

`buy` 뷰에서는 Checkout Overlay를 띄우는 버튼을 렌더링합니다. Cashier Paddle에는 `paddle-button` Blade 컴포넌트가 포함되어 있습니다. 물론 [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 제공

상품을 판매할 때, 주문 및 구매 상품 내역을 애플리케이션의 `Cart`, `Order` 모델에 기록하는 경우가 많습니다. 고객이 결제 후 돌아왔을 때 주문을 연동하기 위해, 기존 주문번호 같은 값을 Paddle Checkout Overlay로 보낼 필요가 있습니다.

이를 위해 `checkout` 메서드에 커스텀 데이터 배열을 제공할 수 있습니다. 예를 들어, 사용자가 결제 프로세스를 시작하면 애플리케이션에서 미결(Order status: incomplete) 주문을 하나 만든다고 가정합시다.

```php
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

이와 같이 고객이 결제 프로세스를 시작할 때, 카트/주문에 연관된 모든 Paddle 가격 식별자를 `checkout` 메서드에 넘깁니다. 주문 ID도 `customData` 메서드를 통해 전달하여, 결제 성공 후 Paddle에서 응답받은 webhook 이벤트에서 주문과 연동할 수 있습니다.

결제 완료 후에는 주문을 "complete"(완료)로 마킹해야 합니다. 이를 위해, Paddle이 발생시키는 webhook 이벤트를 Cashier가 전파한 다음, 적절히 처리하면 됩니다.

예를 들어 Cashier가 전달하는 `TransactionCompleted` 이벤트를 리스닝할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 리스너를 등록합니다:

```php
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

리스너 예시는 다음과 같습니다:

```php
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

`transaction.completed` 이벤트 내부 데이터 구조에 대한 자세한 내용은 Paddle 공식 문서를 참고하세요: [transaction.completed event](https://developer.paddle.com/webhooks/transactions/transaction-completed)

<a name="quickstart-selling-subscriptions"></a>
### 구독 상품 판매 (Selling Subscriptions)

> [!NOTE]
> Paddle Checkout을 사용하기 전에 반드시 Paddle 대시보드에서 고정 가격 상품을 정의하고, [webhook 처리를 설정](#handling-paddle-webhooks)해야 합니다.

상품 및 구독 결제 연동은 쉽지 않은 작업이지만, Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 활용하면 빠르게 결제 기능을 만들 수 있습니다.

예를 들어 "기본(Basic)" 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제(Price)를 Paddle 대시보드의 "Basic" 상품(`pro_basic`) 아래에 등록했다고 가정해봅시다. 추가로 "전문가(Expert)" 플랜(`pro_expert`)도 제공할 수 있습니다.

먼저, 고객이 어떻게 구독을 시작하는지 살펴봅니다. 예를 들어, 고객이 애플리케이션의 가격 페이지에서 Basic 플랜의 "구독" 버튼을 클릭하면 Paddle Checkout Overlay를 통해 결제 과정을 시작하게 할 수 있습니다. 시작은 `checkout` 메서드로 체크아웃 세션을 생성하는 것입니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 Checkout Overlay를 띄우는 버튼을 렌더링합니다. Cashier Paddle의 `paddle-button` Blade 컴포넌트를 사용할 수도 있고, [오버레이 체크아웃 수동 렌더링](#manually-rendering-an-overlay-checkout)도 가능합니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 Subscribe 버튼을 클릭하면 고객은 결제 정보를 입력하고 구독을 시작할 수 있습니다. 결제가 확정됐는지 판단해야 할 때(특정 결제수단의 경우 처리에 몇 초 소요될 수 있음), Cashier의 [webhook 처리](#handling-paddle-webhooks)를 반드시 설정해야 합니다.

구독 기능이 준비되었다면, 구독한 유저만 접근 가능한 애플리케이션 영역을 제한해야 할 수 있습니다. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 활용하여 사용자의 구독 상태를 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 구독 중인지 쉽게 확인할 수도 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 미들웨어 만들기

요청자가 구독 중인 사용자임을 확인하는 [미들웨어](/docs/12.x/middleware)를 만들어 루트에 쉽게 적용할 수 있습니다. 예를 들어 구독하지 않은 사용자는 접근을 차단할 수 있습니다:

```php
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
            // 결제 페이지로 리다이렉트 후 구독 요청
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

정의한 미들웨어를 라우트에 적용:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객의 플랜 관리 허용

고객이 플랜을 월간 → 연간 등 다른 상품("티어")로 변경하고 싶어할 수 있습니다. 버튼 등을 통해 아래 경로로 유도하면 됩니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 예: $price = "price_basic_yearly" 등

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

플랜 변경 외에도 구독 취소 기능도 제공해야 합니다. 이 역시 버튼을 만들어 다음과 같이 처리할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이제 구독이 현재 결제 주기 종료 시점에 맞춰 취소됩니다.

> [!NOTE]
> Cashier의 webhook 처리를 설정했다면, Paddle 대시보드에서 직접 구독을 취소하더라도 관련 webhook이 전달되어 애플리케이션 내 구독 정보가 자동으로 "취소됨"으로 동기화됩니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션 (Checkout Sessions)

대부분의 고객 청구 작업은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout) 또는 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 사용하여 "체크아웃"을 통해 이루어집니다.

결제 처리를 시작하기 전, Paddle 대시보드에서 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 등록해두어야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃 (Overlay Checkout)

Checkout Overlay 위젯을 표시하기 전, Cashier로 체크아웃 세션을 생성해야 합니다. 이 세션이 해당 결제 작업의 정보를 위젯에 제공합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier는 `paddle-button` [Blade 컴포넌트](/docs/12.x/blade#components)를 제공합니다. 체크아웃 세션을 "prop"으로 넘기면 버튼 클릭 시 Paddle 결제 위젯이 나타납니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle의 스타일로 표시되지만, [지원 속성](https://developer.paddle.com/paddlejs/html-data-attributes)인 `data-theme='light'` 등으로 스타일을 조정할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle Checkout 위젯은 비동기로 동작합니다. 사용자가 위젯 내에서 구독을 생성하면 Paddle이 webhook을 보내므로, 애플리케이션의 데이터베이스에 구독 상태를 정확히 반영하려면 반드시 [webhook 처리를 설정](#handling-paddle-webhooks)해야 합니다.

> [!WARNING]
> 구독 상태 변경 후 대응 webhook의 수신이 약간 지연될 수 있으니, 결제 완료 즉시 구독이 즉시 반영되지 않을 수 있음을 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 수동 렌더링

Laravel의 Blade 컴포넌트를 사용하지 않고 오버레이 체크아웃을 직접 렌더링할 수도 있습니다. 체크아웃 세션 생성은 [앞서와 동일하게](#overlay-checkout) 작성합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그 다음, Paddle.js를 이용하여 체크아웃을 초기화합니다. 예시에서는 `paddle_button` 클래스를 가진 링크를 만들고 Paddle.js가 이를 잡아 위젯을 띄우게 합니다:

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
### 인라인 체크아웃 (Inline Checkout)

오버레이 스타일 위젯 대신, Paddle의 인라인 체크아웃을 사용할 수도 있습니다. 이 방식은 체크아웃 HTML 필드를 수정할 수는 없지만, 애플리케이션 내에 위젯을 직접 삽입할 수 있다는 장점이 있습니다.

Cashier는 이를 간단하게 하기 위해 `paddle-checkout` Blade 컴포넌트를 제공합니다. 체크아웃 세션은 [오버레이와 동일하게 생성](#overlay-checkout)하고:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

컴포넌트의 `checkout` 속성에 세션을 넘깁니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

높이를 조정하려면 `height` 속성을 전달하면 됩니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

자세한 인라인 체크아웃 커스터마이징은 Paddle의 [Inline Checkout 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [설정 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하십시오.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

Blade 컴포넌트 없이 인라인 체크아웃을 직접 렌더링할 수도 있습니다. [이전과 동일하게 체크아웃 세션을 생성](#inline-checkout)하고:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Paddle.js를 이용하여 인라인 체크아웃을 초기화합니다. 아래 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하지만, 원하는 방식에 맞게 수정 가능합니다:

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
### 비회원 체크아웃 (Guest Checkouts)

애플리케이션 계정이 없는 사용자에 대해서도 체크아웃 세션을 만들 수 있습니다. 이를 위해 `guest` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이후 [Paddle 버튼](#overlay-checkout) 또는 [인라인 체크아웃](#inline-checkout) Blade 컴포넌트에 해당 세션을 전달하면 됩니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle은 통화별, 국가별로 가격을 다양하게 설정할 수 있습니다. Cashier Paddle의 `previewPrices` 메서드로 원하는 price ID들의 모든 가격 정보를 조회할 수 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

기본적으로는 요청자의 IP로 통화를 결정하지만, 아래처럼 특정 국가를 지정할 수도 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회한 가격 정보를 원하는 형식으로 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계 및 세금만 따로 표시하려면:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

좀 더 자세한 내용은 [Paddle의 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객별 가격 미리보기

이미 고객인 사용자가 적용받을 실제 가격 정보를 조회하려면, 해당 고객 인스턴스에서 바로 가져올 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Cashier는 내부적으로 고객의 currency 정보로 가격을 조회하므로, 예를 들어 미국에 거주하는 사용자는 USD로, 벨기에 사용자는 EUR로 가격이 표시됩니다. 일치하는 통화가 없다면 상품의 기본 통화가 사용됩니다. Paddle 관리 콘솔에서 상품(또는 구독 플랜)별 모든 가격 정보를 관리할 수 있습니다.

<a name="price-discounts"></a>
### 할인

할인 후 가격도 표시할 수 있습니다. `previewPrices` 호출 시 `discount_id` 옵션을 통해 할인 ID를 전달합니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격을 표시:

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
### 고객 기본값

Cashier는 체크아웃 세션 생성 시 고객에 대한 기본값(이메일, 이름 등)을 미리 채울 수 있게 해줍니다. 청구 가능 모델에서 아래 메서드들을 오버라이드하여 이 값을 지정할 수 있습니다:

```php
/**
 * Get the customer's name to associate with Paddle.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Get the customer's email address to associate with Paddle.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이 기본값은 Cashier가 [체크아웃 세션](#checkout-sessions)을 생성할 때마다 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

Paddle 고객 ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용합니다. 이 메서드는 청구 가능 모델 인스턴스를 반환합니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

때로는 바로 구독을 시작하지 않고 Paddle 고객만 미리 생성해야 할 수 있습니다. 이 경우 `createAsCustomer` 메서드를 사용하세요:

```php
$customer = $user->createAsCustomer();
```

반환값은 `Laravel\Paddle\Customer` 인스턴스입니다. 고객 생성을 완료한 후, 나중에 구독을 시작할 수 있습니다. 필요하다면 추가 옵션도 넘길 수 있습니다([Paddle 고객 생성 지원 파라미터](https://developer.paddle.com/api-reference/customers/create-customer) 참고):

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면, 먼저 데이터베이스에서 청구 가능 모델(보통 `App\Models\User`) 인스턴스를 가져옵니다. 그런 후, `subscribe` 메서드로 체크아웃 세션을 생성할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe` 메서드의 첫 번째 인자는 사용자가 결제할 가격(Paddle price 식별자), `returnTo`는 결제 성공 후 이동할 URL입니다. 두 번째 인자는 내부적으로 정의할 구독 타입(예: `default`, `primary` 등)입니다. 이 타입은 사용자에게 노출하지 않으며, 일반적으로 한번 지정하면 변경하지 않아야 합니다.

구독에 대한 추가 메타데이터가 필요한 경우 `customData`로 넘길 수 있습니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

체크아웃 세션이 생성되면, [Cashier 기본 Blade 컴포넌트](#overlay-checkout)인 `paddle-button`에 전달하여 구독 버튼을 만들 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

결제 완료 시 Paddle은 `subscription_created` webhook을 보냅니다. Cashier는 이 webhook을 수신하여 구독을 설정합니다. 모든 webhook이 정상적으로 처리될 수 있도록 [Webhook 처리를 반드시 설정](#handling-paddle-webhooks)해야 합니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 구독한 이후, 다양한 메서드로 구독 상태를 확인할 수 있습니다. `subscribed` 메서드는 유효한 구독이 있으면 `true`를 반환하며, 체험 기간(trial) 중이어도 `true`입니다:

```php
if ($user->subscribed()) {
    // ...
}
```

애플리케이션에서 여러 구독을 제공한다면, 구독 타입을 지정할 수도 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

이 `subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware)로도 활용할 수 있어, 구독 상태로 접근을 제어할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed()) {
            // 이 사용자는 결제 고객이 아님
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

사용자가 체험 기간(trial) 내에 있는지 확인하고 싶다면 `onTrial` 메서드를 사용하면 됩니다:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 Paddle price ID에 구독 중인지 확인하려면 `subscribedToPrice`를 사용합니다:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

사용자가 현재 활성 구독 상태이며, 더 이상 체험(trial)이나 유예(grace) 기간에 있지 않은지 확인하려면 `recurring`을 사용할 수 있습니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 구독 취소 상태

한때 구독 중이었다가 구독을 취소했는지 확인하려면 `canceled` 메서드를 사용합니다:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

취소한 구독이 아직 "유예 기간(grace period)"내인지 확인할 수도 있습니다. 예를 들어, 3월 5일에 취소했으나 본래 3월 10일까지 기간이 남았다면, 3월 10일까지 유예 기간입니다. 이 동안에는 `subscribed`도 여전히 `true`입니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체(past_due) 상태

결제 실패로 구독이 `past_due`(연체) 상태가 되면, 결제가 완료되어야 다시 활성화됩니다. 이 상태는 구독 인스턴스의 `pastDue`로 확인할 수 있습니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

구독이 연체 상태일 때는 고객에게 [결제 정보 업데이트](#updating-payment-information)를 안내해야 합니다.

만약 연체 상태에서도 구독을 계속 유효한 것으로 간주하고 싶다면, `keepPastDueSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register`에서 호출하십시오:

```php
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
> `past_due` 상태의 구독은 결제 정보가 갱신되기 전에는 변경할 수 없습니다. 따라서 `swap`, `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 Scope

구독 상태 대부분은 쿼리 스코프로도 제공되어, 데이터베이스에서 특정 상태의 구독만 쉽게 조회할 수 있습니다:

```php
// 모든 유효한 구독 조회
$subscriptions = Subscription::query()->valid()->get();

// 고객의 모든 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 쿼리 스코프 목록:

```php
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
### 구독 단일 청구

구독 중인 고객에게 구독 요금 외의 추가 상품(일회성 상품 등)을 추가로 청구할 수도 있습니다. `charge` 메서드 사용 시 하나 또는 여러 price ID를 전달합니다:

```php
// 개별 가격 한 개 청구
$response = $user->subscription()->charge('pri_123');

// 여러 가격 한 번에 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge` 메서드는 실제 청구가 구독의 다음 청구 주기 때 일어나게 합니다. 즉시 청구하고 싶다면 `chargeAndInvoice` 메서드를 사용하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독마다 결제 정보를 별도로 보관합니다. 구독의 기본 결제 정보를 업데이트하려면 구독 모델의 `redirectToUpdatePaymentMethod`를 사용하여 Paddle의 결제 정보 수정 페이지로 고객을 리다이렉트하세요:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

고객이 정보를 업데이트하면 Paddle은 `subscription_updated` webhook을 전송하며, Cashier가 구독 정보를 데이터베이스에 반영합니다.

<a name="changing-plans"></a>
### 플랜 변경

구독 중인 사용자가 다른 구독 플랜으로 변경하고자 하면, 대상 price ID를 `swap` 메서드에 전달하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 청구서를 발행해 결제하기를 원한다면 `swapAndInvoice`를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 발췌(proration) 정책

기본적으로 Paddle은 플랜 변경 시 요금을 발췌(남은 일수/잔여분만큼 계산)하여 정산합니다. 발췌 없이 바로 변경하려면 `noProrate`를 쓸 수 있습니다:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

즉시 청구와 발췌 없이 변경하려면:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

변경 시 추가 결제 없이 요금 계산 자체를 하지 않으려면 `doNotBill`을 사용합니다:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

자세한 발췌 정책은 Paddle의 [proration 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량

경우에 따라 구독에 "수량" 개념이 적용될 수 있습니다. 예를 들어, 프로젝트 수 당 요금이 붙는 SaaS에서는 구독 수량에 따라 결제해야 합니다. 수량을 조작할 때는 `incrementQuantity`, `decrementQuantity`를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 현재 수량에 5 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 현재 수량에서 5 차감
$user->subscription()->decrementQuantity(5);
```

직접 특정 수량으로 지정하고 싶을 때는 `updateQuantity`:

```php
$user->subscription()->updateQuantity(10);
```

발췌 없이 수량 변경하려면 `noProrate`와 함께 사용:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독 시의 수량 조정

[다중 상품 구독](#subscriptions-with-multiple-products)인 경우, 조정할 price ID를 두 번째 인자로 전달합니다:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독

[다중 상품 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)은 하나의 구독에 여러 결제 상품을 할당할 수 있는 기능입니다. 예를 들어, 기본 구독($10/월)에 라이브 챗 추가상품($15/월)을 부가로 제공하는 커스텀 헬프데스크 SaaS가 있을 수 있습니다.

구독 생성 시, `subscribe`의 첫 번째 인자에 price들의 배열을 넘기면 여러 상품이 등록됩니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe([
        'price_monthly',
        'price_chat',
    ]);

    return view('billing', ['checkout' => $checkout]);
});
```

동일 구독에 두 price가 등록되고, 각 가격은 별도 청구 주기에 따라 결제됩니다. quantity 지정이 필요할 경우 price => quantity 형태의 연관 배열도 전달할 수 있습니다:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 새로운 price를 추가하려면 `swap` 메서드로 기존/신규 가격 및 수량 정보를 함께 전달합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

이렇게 하면 새로운 price가 추가되지만, 다음 결제일에 청구됩니다. 즉시 청구하려면 `swapAndInvoice` 사용:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

특정 price를 구독에서 뺄 때는 빼고 싶은 price만 제외시켜 전달하면 됩니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서 마지막 남은 price는 제거할 수 없습니다. 구독 자체를 취소해야 합니다.

<a name="multiple-subscriptions"></a>
### 다중 구독

Paddle은 한 고객이 여러 구독을 동시에 가질 수 있습니다. 예를 들어 헬스장에서 수영, 웨이트 트레이닝 등 여러 구독 플랜을 제공한다면 고객이 각각의 구독을 별개로 구독/취소할 수 있습니다.

구독 생성 시 타입(이름)을 두 번째 인자로 전달하면 됩니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

타입(여기서는 'swimming')을 기준으로 나중에 플랜을 변경(`swap`)하거나 취소(`cancel`) 할 수 있습니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시정지

구독을 일시정지하려면 구독 인스턴스의 `pause`를 호출합니다:

```php
$user->subscription()->pause();
```

일시정지 시점은 DB의 `paused_at` 컬럼에 저장되며, 실제 결제 기간 만료 전까지는 `paused` 메서드가 계속 `false`를 반환할 수 있습니다(남은 결제 기간 동안 서비스 사용 가능).

즉시 일시정지하려면 `pauseNow`를 사용합니다:

```php
$user->subscription()->pauseNow();
```

특정 일시로까지 일시정지하려면 `pauseUntil`:

```php
$user->subscription()->pauseUntil(now()->addMonth());
```

즉시 시작하여 특정 시점까지 일시정지하려면 `pauseNowUntil`:

```php
$user->subscription()->pauseNowUntil(now()->addMonth());
```

구독이 일시정지되어 있지만 아직 "유예 기간"인 경우 `onPausedGracePeriod`로 확인할 수 있습니다:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시정지된 구독을 다시 재개하려면 `resume` 호출:

```php
$user->subscription()->resume();
```

> [!WARNING]
> 일시정지 중인 구독은 플랜/수량 등 변경이 불가능하며, 먼저 재개해야 수정할 수 있습니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 구독의 `cancel` 메서드를 호출합니다:

```php
$user->subscription()->cancel();
```

취소 시 DB의 `ends_at` 컬럼이 설정되며, 만약 결제 주기가 남아 있다면 만료일까지는 계속 이용 가능합니다. 이 기간 동안은 `subscribed`가 여전히 `true`를 반환합니다.

구독이 취소되었지만 아직 "유예 기간"인지는 `onGracePeriod`로 알 수 있습니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 구독을 중단하고 싶으면 `cancelNow`를 사용합니다:

```php
$user->subscription()->cancelNow();
```

유예 기간 중 취소(만료)를 멈추려면 `stopCancelation`을 호출합니다:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle 구독은 한 번 취소하면 다시 재개할 수 없습니다. 사용자 재개를 원할 경우 새 구독을 만들어야 합니다.

<a name="subscription-trials"></a>
## 구독 체험(Trial) (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 정보 선등록 체험

고객에게 체험 기간(Trial)을 제공하면서 결제 정보(카드 등)를 미리 받아두고 싶다면, Paddle 대시보드에서 price에 체험 기간을 지정하세요. 그리고 평소처럼 체크아웃 세션을 시작하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트를 수신하면, Cashier는 구독 레코드에 trial 종료 날짜를 기록하고, Paddle에는 trial 동안 과금이 되지 않도록 안내합니다.

> [!WARNING]
> 체험 기간이 끝나기 전에 구독을 취소하지 않으면 trial 만료 즉시 자동 청구가 발생하므로, 유저에게 trial 종료를 미리 안내해야 합니다.

사용자가 trial 내에 있는지는 `onTrial`로 확인합니다:

```php
if ($user->onTrial()) {
    // ...
}
```

기존 trial이 만료되었는지는 `hasExpiredTrial`로 확인 가능합니다:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입별로 trial 여부를 확인하려면:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 정보 없이 체험

결제 정보를 미리 받지 않고 trial을 제공하려면, 사용자 생성시 고객 레코드의 `trial_ends_at`을 원하는 일시로 지정하세요:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

이렇게 생성된 trial은 구독에 연결되어 있지 않아 "generic trial"(일반 trial)로 분류됩니다. `User` 인스턴스의 `onTrial`은 현재 날짜가 trial 기간 내라면 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // Trial 기간 내
}
```

나중에 실제 구독을 생성하려면 평소와 같이 `subscribe`를 사용합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

trial 종료일은 `trialEndsAt` 메서드로 조회할 수 있습니다. 구독 타입 파라미터도 선택적으로 사용할 수 있습니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

아직 구독이 없는 "generic trial" 상태만 판별하고 싶다면 `onGenericTrial`을 사용하세요:

```php
if ($user->onGenericTrial()) {
    // generic trial 기간 내
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 기간 연장 또는 활성화

구독의 기존 trial 기간을 연장하려면 `extendTrial`에 trial 종료 시점을 지정해 호출합니다:

```php
$user->subscription()->extendTrial(now()->addDays(5));
```

즉시 구독을 활성화(체험 종료)하려면 `activate` 호출:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트 발생 시 애플리케이션에 webhook을 보냅니다. Cashier는 기본적으로 자체 webhook 컨트롤러를 경로에 등록하여 모든 webhook 요청을 처리합니다.

기본 컨트롤러는 일반적인 구독 취소, 결제 실패에 따른 상태 변경, 결제 정보 변경 등을 자동으로 처리합니다. 그 외 추가 이벤트가 필요하면 컨트롤러를 확장할 수도 있습니다.

애플리케이션이 Paddle webhook을 수신할 수 있도록, 반드시 Paddle 벤더 대시보드에 webhook URL을 등록해야 합니다. 기본적으로 Cashier의 webhook 경로는 `/paddle/webhook`입니다. Paddle 대시보드에서 활성화해야 할 webhook 리스트는 아래와 같습니다:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Cashier에서 제공하는 [webhook 서명 검증 미들웨어](/docs/12.x/cashier-paddle#verifying-webhook-signatures)로 외부 요청을 반드시 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### Webhook과 CSRF 보호

Paddle webhook은 Laravel의 [CSRF 보호](/docs/12.x/csrf)를 우회해야 하므로, 애플리케이션의 `bootstrap/app.php`에서 `paddle/*` 엔드포인트를 CSRF 검증에서 제외해야 합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### Webhook과 로컬 개발

Paddle이 로컬 개발 환경의 애플리케이션에 webhook을 전송할 수 있게 하려면, [Ngrok](https://ngrok.com/), [Expose](https://expose.dev/docs/introduction) 등 사이트 공유 서비스를 사용하여 외부에서 접속할 수 있도록 해야 합니다. [Laravel Sail](/docs/12.x/sail)을 쓴다면 [site sharing 커맨드](/docs/12.x/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### Webhook 이벤트 핸들러 정의

Cashier는 결제 실패로 인한 구독 취소 등 주요 Paddle webhook을 자동으로 처리합니다. 추가 webhook 처리가 필요하다면 Cashier가 전파하는 아래 이벤트를 리스닝하면 됩니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle webhook 페이로드 전체를 포함합니다. 예를 들어, `transaction.billed` webhook을 처리하려면 다음과 같이 리스너를 등록할 수 있습니다:

```php
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
            // 이벤트 처리
        }
    }
}
```

Cashier는 페이로드 외에도 구독, 고객, 영수증 등 관련 모델을 포함하는 이벤트도 제공합니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

기본 webhook 경로가 아닌 맞춤 경로를 쓰고 싶다면, `.env`의 `CASHIER_WEBHOOK` 환경 변수에 해당 URL을 지정하고 Paddle 대시보드에 동일 URL을 입력해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Webhook 서명 검증

보안 강화를 위해 [Paddle의 webhook 서명 기능](https://developer.paddle.com/webhooks/signature-verification)을 사용할 수 있습니다. Cashier는 Paddle webhook 서명을 검증하는 미들웨어를 기본 탑재하고 있습니다.

webhook 검증 활성화를 위해서는 `.env` 파일에 `PADDLE_WEBHOOK_SECRET` 환경 변수를 반드시 입력해야 합니다. 이 값은 Paddle 계정 대시보드에서 확인 가능합니다.

<a name="single-charges"></a>
## 단일 청구 (Single Charges)

<a name="charging-for-products"></a>
### 상품 결제

상품을 고객에게 한 번 결제시키려면, 청구 가능 모델 인스턴스의 `checkout` 메서드를 통해 결제 세션을 생성합니다. 이 메서드는 price ID 여러 개 또는 수량 등도 배열로 설정 가능합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

결제 세션을 생성한 후, Cashier의 `paddle-button` [Blade 컴포넌트](#overlay-checkout)로 사용자가 Paddle 결제 위젯을 볼 수 있게 하십시오:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

체크아웃 세션의 `customData` 메서드를 통해 트랜잭션 생성 시 원하는 커스텀 데이터를 전달할 수 있습니다. 더 자세한 내용은 [Paddle 공식문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불

거래 환불은 고객이 결제 당시 사용한 결제 수단으로 다시 금액을 돌려줍니다. Paddle 구매를 환불하려면 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용하세요. 처음 인자는 사유, 그 뒤로 하나 이상 price ID(또는 금액-수량 배열)를 보낼 수 있습니다. 거래 인스턴스는 `transactions` 메서드로 가져올 수 있습니다.

예를 들어, `pri_123`는 전액 환불, `pri_456`은 2달러만 환불한다면:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 2달러만 환불
]);
```

전체 트랜잭션을 모두 환불하려면 사유만 적으면 됩니다:

```php
$response = $transaction->refund('Accidental charge');
```

환불 자세한 내용은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참조하세요.

> [!WARNING]
> 환불은 반드시 Paddle의 승인을 거쳐야만 처리됩니다.

<a name="crediting-transactions"></a>
### 거래 크레딧

환불 외에도 거래를 "크레딧" 처리할 수 있습니다. 크레딧 처리 시 해당 금액이 고객의 잔고로 적립되어 추후 결제에 사용할 수 있습니다. 단, Paddle은 수동 수금(직접 청구) 타입에만 크레딧을 허용합니다. (구독 등 자동 청구는 Paddle이 자동 크레딧 처리함)

```php
$transaction = $user->transactions()->first();

// 특정 라인 아이템 전체 크레딧
$response = $transaction->credit('Compensation', 'pri_123');
```

좀 더 자세한 내용은 [Paddle 크레딧 공식문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 크레딧은 수동 청구 거래에만 가능합니다. 자동 청구 거래는 Paddle이 직접 처리합니다.

<a name="transactions"></a>
## 거래 내역 (Transactions)

청구 가능 모델 인스턴스의 `transactions` 프로퍼티로 거래 내역 배열을 쉽게 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래 내역은 상품 결제 및 영수증(invoice) 정보와 함께 저장됩니다. 완료된 트랜잭션만 데이터베이스에 기록됩니다.

고객의 거래 내역을 테이블 등에서 표시할 때, 각 거래 인스턴스의 메서드를 활용하면 관련 결제 정보와 영수증 다운로드 기능 등을 구현할 수 있습니다:

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

`download-invoice` 라우트 예시:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정된 결제

`lastPayment`, `nextPayment` 메서드로 구독 사용자 기준 과거 결제 또는 다음 예정 결제 정보를 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

둘 다 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 단, `lastPayment`는 아직 webhook 동기화가 안 됐다면 `null`, `nextPayment`는 구독 종료 상태라면 `null`을 반환합니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

빌링 플로우는 수동 테스트로 통합 연동이 잘 작동하는지 꼭 확인해야 합니다.

CI 환경 등 자동화된 테스트에서는 [Laravel의 HTTP 클라이언트](/docs/12.x/http-client#testing)를 활용해 Paddle 호출을 모킹할 수 있습니다. 이 방법은 Paddle의 실제 응답을 테스트하지는 않지만, Paddle API 호출 없이 애플리케이션의 나머지 코드 로직 테스트에 활용할 수 있습니다.
