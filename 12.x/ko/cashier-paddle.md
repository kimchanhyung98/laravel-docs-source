# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [체크아웃 세션](#checkout-sessions)
    - [오버레이 체크아웃](#overlay-checkout)
    - [인라인 체크아웃](#inline-checkout)
    - [비회원 체크아웃](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객별 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [기본값 설정](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [요금제 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [결제 정보 입력 후 체험](#with-payment-method-up-front)
    - [결제 정보 없이 체험](#without-payment-method-up-front)
    - [체험 연장 및 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [상품에 대한 청구](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧 부여](#crediting-transactions)
- [거래](#transactions)
    - [과거 및 예정된 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x에서 제공하는 Paddle Billing 통합에 관한 내용입니다. 만약 아직 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 참고하세요.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 및 결제 서비스를 간결하고 직관적인 인터페이스로 제공합니다. 반복적인 구독 결제 코드 대부분을 Cashier가 알아서 처리해줍니다. 기본 구독 관리 외에도, Cashier는 구독 변경, 구독 수량 지정, 구독 일시정지, 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 자세히 학습하기 전에, Paddle의 [컨셉 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 살펴보시길 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새로운 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 검토하시기 바랍니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 관리자를 사용해 Paddle용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier-paddle
```

다음으로, `vendor:publish` Artisan 명령어를 실행해 Cashier 마이그레이션 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그런 다음 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성합니다. 추가로, 고객이 가진 모든 구독을 저장할 `subscriptions`와 `subscription_items` 테이블이 생성되며, 고객의 Paddle 거래를 저장할 `transactions` 테이블도 함께 생성됩니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리할 수 있도록 반드시 [Cashier의 Webhook 처리](#handling-paddle-webhooks)를 설정해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle Sandbox

로컬 및 스테이징 환경에서 개발할 때는 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)을 등록하는 것이 좋습니다. 이 계정을 통해 실제 결제 없이 애플리케이션 테스트 및 개발이 가능합니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용해 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

Paddle Sandbox 환경을 사용할 때는, 애플리케이션의 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다:

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발을 마친 후에는 [Paddle 벤더 계정](https://paddle.com)에 신청할 수 있습니다. 프로덕션으로 전환하기 전에 Paddle이 애플리케이션의 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 업데이트 등 결제 관련 작업을 수행할 수 있는 다양한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

만약 유저가 아닌 다른 엔터티(예: `Team`)가 결제 대상이라면, 해당 클래스에도 이 트레이트를 추가할 수 있습니다:

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

이제 애플리케이션의 `.env` 파일에 Paddle API 키를 설정해야 합니다. Paddle 제어판(Paddle Control Panel)에서 API 키를 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle Sandbox 환경](#paddle-sandbox)을 사용할 때 `true`로 설정하세요. 라이브 환경(프로덕션)에서는 `false`로 변경해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며, 만약 Paddle의 [Retain](https://developer.paddle.com/concepts/retain/overview) 기능을 사용할 경우에만 설정하면 됩니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle의 결제 위젯을 작동시키기 위해 자체 JavaScript 라이브러리가 필요합니다. 이 라이브러리는 `@paddleJS` Blade 디렉티브를 레이아웃의 마지막 `</head>` 태그 바로 앞에 추가하면 불러올 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

송장(invoice) 등에서 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 포맷을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier에서 사용하는 내부 모델을 확장하려면, 사용자 정의 모델을 작성하고 Cashier의 해당 모델을 상속하세요:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

사용자 정의 모델을 만든 후에는 `Laravel\Paddle\Cashier` 클래스를 이용해 Cashier가 이 모델을 사용하도록 지정할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이를 설정합니다:

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
### 상품 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전, 반드시 Paddle 대시보드에서 고정 가격이 설정된 상품을 등록해야 합니다. 또한 [Paddle의 Webhook 처리](#handling-paddle-webhooks)를 구성해야 합니다.

애플리케이션에서 상품 판매와 구독 결제를 제공하는 일이 다소 어려워 보일 수 있지만, Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 활용하면 강력하고 현대적인 결제 통합을 쉽게 구현할 수 있습니다.

단발성(한 번만 결제되는) 상품을 고객에게 청구하기 위해, Paddle의 Checkout Overlay를 Cashier로 호출하여 결제 정보를 입력받고 구매를 완료하도록 할 수 있습니다. 결제가 완료되면, 사용자는 애플리케이션 내 원하는 성공 URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제에서 볼 수 있듯이, Cashier가 제공하는 `checkout` 메서드를 사용해 고객에게 Paddle Checkout Overlay를 띄울 수 있는 체크아웃 객체를 생성합니다. Paddle의 "price"란 [특정 상품별로 등록된 고유 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요할 경우, `checkout` 메서드는 Paddle에 해당 고객을 자동으로 생성하고, 이 Paddle 고객 레코드를 애플리케이션의 유저와 연결합니다. 체크아웃 세션이 완료되면 고객을 지정한 성공 페이지로 리디렉션하여 안내 메시지를 보여줄 수 있습니다.

`buy` 뷰(view)에서는 Checkout Overlay를 띄우기 위한 버튼을 추가합니다. Cashier Paddle에는 바로 사용할 수 있는 `paddle-button` Blade 컴포넌트가 제공되지만, [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 전달

상품을 판매하는 경우, 자체적으로 구현한 `Cart`와 `Order` 모델을 이용해 주문 완료 이력 및 구매내역을 관리하는 일이 일반적입니다. 고객이 Paddle Checkout Overlay에서 결제를 완료하고 애플리케이션에 돌아올 때, 해당 주문과 연계시키고자 주문 ID와 같은 정보를 전달해야 하는 경우가 있습니다.

이를 위해, `checkout` 메서드에 커스텀 데이터 배열을 전달하면 됩니다. 예를 들어, 체크아웃이 시작될 때 미완료 상태의 `Order`가 생성된다고 가정할 수 있습니다. (이 예시의 `Cart`와 `Order` 모델은 Cashier에서 기본 제공하지 않으므로, 애플리케이션 요구에 따라 직접 구현해야 합니다.)

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

이처럼 사용자가 결제를 시작할 때, 장바구니/주문의 Paddle price 식별자 전체를 `checkout` 메서드에 전달할 수 있습니다. 해당 항목들을 "장바구니" 또는 주문에 연동하는 작업은 애플리케이션에서 직접 관리해야 합니다. 주문 ID 등 추가 정보는 `customData` 메서드로 Paddle Checkout Overlay에 전달할 수 있습니다.

결제 완료 후에는, Paddle에서 송신하는 Webhook을 통해 주문 상태를 "complete"(완료)로 갱신해야 합니다. 이를 위해, Cashier가 발생시키는 `TransactionCompleted` 이벤트를 청취하면 됩니다. 보통은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에 이벤트 리스너를 등록합니다:

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades/Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

여기서 `CompleteOrder` 리스너는 다음과 같이 구현될 수 있습니다:

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

이벤트에서 제공되는 데이터에 관한 더 자세한 내용은 Paddle 문서의 [`transaction.completed` 이벤트 데이터](https://developer.paddle.com/webhooks/transactions/transaction-completed) 부분을 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전, 반드시 Paddle 대시보드에서 고정 가격이 설정된 상품을 등록해야 합니다. 또한 [Paddle의 Webhook 처리](#handling-paddle-webhooks)를 구성해야 합니다.

애플리케이션에서 상품 및 구독 결제를 제공하는 일이 어렵게 느껴질 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 함께 활용하면 쉽고 현대적인 결제 통합이 가능합니다.

Cashier와 Paddle Checkout Overlay를 이용해 구독 상품을 판매하는 방법은 단일 월간 요금제(`price_basic_monthly`) 또는 연간 요금제(`price_basic_yearly`), 그리고 'Expert' 요금제(`pro_expert`)와 같은 구조에서 출발할 수 있습니다. 이 두 가격은 기본 상품(`pro_basic`) 아래에 그룹화해 둘 수 있습니다.

고객이 애플리케이션의 요금제 페이지에서 'Basic' 구독 버튼을 클릭한다고 가정해 볼 수 있습니다. 이 버튼이 해당 상품에 대한 Paddle Checkout Overlay를 띄우게 됩니다. 아래와 같이 `checkout` 메서드를 호출해 체크아웃 세션을 시작할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 Paddle Checkout Overlay를 띄우는 버튼을 추가합니다. Cashier Paddle의 `paddle-button` Blade 컴포넌트를 사용할 수 있으며, [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)하는 방법도 활용 가능합니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 구독 버튼을 클릭하면 고객은 결제 정보를 입력하고 구독을 시작할 수 있습니다. 구독이 실제로 시작된 시점을 인지하려면(일부 결제수단은 처리에 수 초가 걸릴 수 있음) [Cashier의 Webhook 처리](#handling-paddle-webhooks)가 반드시 필요합니다.

구독이 활성화된 고객에게만 애플리케이션의 특정 영역을 허용하려면, Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드로 사용자의 구독 상태를 관리하면 됩니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 대해 구독 여부를 확인할 수도 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 미들웨어 작성

편의상, 요청이 구독한 사용자로부터 온 것인지 확인하는 [미들웨어](/docs/12.x/middleware)를 만들 수도 있습니다. 이 미들웨어를 라우트에 지정하여 구독하지 않은 사용자의 접근을 방지할 수 있습니다:

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
            // 사용자에게 결제 페이지로 리디렉션하여 구독을 유도...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어를 라우트에 할당하는 예시는 다음과 같습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객에게 요금제 관리 허용하기

고객은 구독 요금제를 변경하고 싶어할 수 있습니다. 예를 들어 월간 구독에서 연간 구독으로 변경하고자 하는 경우, 아래와 같은 라우트로 연결되는 버튼을 구현해야 합니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 여기서 $price는 예시로 "price_basic_yearly"

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

구독 변경 외에도, 고객이 구독을 직접 취소할 수 있도록 아래와 같은 라우트도 제공합니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이 방법을 사용하면, 구독은 과금 주기가 종료될 때 취소 처리됩니다.

> [!NOTE]
> Cashier의 Webhook 처리가 정상적으로 구성되어 있다면, Paddle 대시보드에서 고객의 구독을 취소하더라도 Cashier가 수신하는 Webhook을 통해 애플리케이션의 데이터베이스 상태가 자동으로 동기화됩니다. 예를 들어, Paddle에서 취소 시 Webhook 수신 후 구독이 'canceled' 상태로 기록됩니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션 (Checkout Sessions)

고객에게 청구하는 대부분의 작업은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout) 또는 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통해 "체크아웃" 방식으로 수행됩니다.

Paddle을 통한 결제 처리 전, 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 Paddle 체크아웃 설정 대시보드에서 지정해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃 (Overlay Checkout)

Checkout Overlay 위젯을 띄우기 전에, Cashier를 활용해 체크아웃 세션을 먼저 생성해야 합니다. 체크아웃 세션은 위젯에 결제 작업 정보를 전달합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/12.x/blade#components)가 포함되어 있습니다. 이 컴포넌트에 체크아웃 세션을 "prop"으로 넘겨주면, 버튼 클릭 시 Paddle의 결제 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle이 제공하는 스타일로 위젯이 표시됩니다. 필요하다면, [Paddle에서 지원하는 속성](https://developer.paddle.com/paddlejs/html-data-attributes)인 `data-theme='light'` 등을 컴포넌트에 추가해 스타일을 변경할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle의 결제 위젯은 비동기로 동작합니다. 사용자가 위젯에서 구독을 생성하면, Paddle이 Webhook을 통해 애플리케이션에 알림을 보내고, 이때 애플리케이션의 데이터베이스도 상태가 변경됩니다. 따라서 반드시 [Webhook 이벤트 수신 설정](#handling-paddle-webhooks)이 필요합니다.

> [!WARNING]
> 구독 상태가 변경된 후 Webhook을 받기까지 일반적으로는 거의 지연이 없지만, 구독 완료 후 바로 사용자에게 구독 상태가 즉시 반영되지 않을 수 있음을 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 수동 렌더링

Laravel의 내장 Blade 컴포넌트를 사용하지 않고 직접 오버레이 체크아웃을 렌더링할 수도 있습니다. [위 예제](#overlay-checkout)와 같이 체크아웃 세션을 생성한 뒤,

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Paddle.js를 사용해 체크아웃을 초기화할 수 있습니다. 아래 예시에서는 `paddle_button` 클래스를 부여한 링크를 만들고, Paddle.js가 이를 감지해 오버레이 위젯을 띄웁니다:

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

Paddle의 오버레이 스타일 위젯이 아닌, 애플리케이션 내에 직접 위젯을 인라인으로 삽입할 수도 있습니다. 이 방법은 위젯 내 HTML 필드를 수정하는 것은 불가능하지만, 위젯을 페이지 내 원하는 위치에 배치할 수 있습니다.

Cashier는 인라인 체크아웃 초기에 사용할 수 있는 `paddle-checkout` Blade 컴포넌트를 제공합니다. [먼저 체크아웃 세션을 생성](#overlay-checkout)한 뒤,

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

아래와 같이 컴포넌트에 체크아웃 세션을 전달할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 위젯의 높이를 조정하려면 `height` 속성을 넘겨줍니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

커스터마이징 옵션 등 자세한 사항은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [체크아웃 설정 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

내장 Blade 컴포넌트를 사용하지 않고 직접 인라인 체크아웃을 구현하려면, [위 예제](#inline-checkout)처럼 체크아웃 세션을 만든 뒤,

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Paddle.js로 직접 체크아웃을 초기화할 수 있습니다. 이 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하지만, 원하는 프론트엔드 스택에 맞게 수정 가능합니다:

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

가끔 애플리케이션 계정 없이도 결제할 수 있게 하고 싶을 수 있습니다. 이럴 땐 `guest` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

그 뒤로 체크아웃 세션을 [Paddle 버튼](#overlay-checkout) 혹은 [인라인 체크아웃](#inline-checkout) Blade 컴포넌트에 넘기면 됩니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle에서는 통화별로 가격을 개별 지정할 수 있으므로, 국가마다 다른 가격을 설정할 수 있습니다. Cashier Paddle에서는 `previewPrices` 메서드를 이용해 모든 가격 정보를 조회할 수 있습니다. 이 메서드는 가격 ID 목록을 인수로 받습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화는 요청 IP에 따라 자동 결정됩니다. 특정 국가로 가격을 확인하려면 다음처럼 주소 정보를 추가해도 됩니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회 후 가격을 자유롭게 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계와 세금을 별도로 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 [Paddle의 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객별 가격 미리보기 (Customer Price Previews)

이미 고객 정보가 있는 유저에게 적용되는 가격을 표시하고 싶다면, 해당 고객 인스턴스에서 직접 가격 조회가 가능합니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Cashier는 내부적으로 사용자의 고객 ID를 이용해 해당 통화로 가격 정보를 조회합니다. 즉, 미국에 거주하는 사용자는 USD로, 벨기에 사용자는 유로화로 가격을 보게 됩니다. 일치하는 통화가 없을 경우, 상품의 기본 통화가 사용됩니다. 상품/구독 요금제의 모든 가격 정보는 Paddle 제어판에서 자유롭게 조정할 수 있습니다.

<a name="price-discounts"></a>
### 할인 (Discounts)

할인 적용 후 가격도 표시할 수 있습니다. `previewPrices` 호출 시, `discount_id` 옵션으로 할인 ID를 전달합니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

그리고 할인 반영된 가격을 표시합니다:

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
### 기본값 설정 (Customer Defaults)

Cashier에서는 체크아웃 세션 생성 시 고객의 이메일과 이름 등 일부 정보를 미리 채워줄 수 있습니다. 이를 위해 Billable 모델에서 아래 메서드들을 오버라이드하면 됩니다:

```php
/**
 * Paddle에 연동할 고객 이름 반환
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Paddle에 연동할 고객 이메일 주소 반환
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이 기본값들은 Cashier에서 [체크아웃 세션](#checkout-sessions)을 생성할 때마다 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

`Cashier::findBillable` 메서드로 Paddle 고객 ID로 고객 객체를 조회할 수 있습니다. 반환값은 Billable 모델 인스턴스입니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔은 구독을 시작하지 않고 Paddle 고객만 생성하고 싶을 수 있습니다. 이럴 땐 `createAsCustomer` 메서드를 사용하세요:

```php
$customer = $user->createAsCustomer();
```

반환값은 `Laravel\Paddle\Customer` 인스턴스입니다. 고객 생성 후, 나중에 구독 생성이 가능합니다. 필요하다면 `$options` 배열을 추가로 전달해 [Paddle API에서 지원하는 옵션](https://developer.paddle.com/api-reference/customers/create-customer)을 전달할 수 있습니다:

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 데이터베이스에서 Billable 모델 인스턴스(일반적으로 `App\Models\User`)를 가져온 뒤, `subscribe` 메서드를 호출하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

첫 번째 인수는 유저가 구독할 Paddle 가격 식별자입니다. `returnTo` 메서드에는 결제 완료 후 리디렉션될 URL을 지정합니다. 두 번째 인수는 구독의 내부 "타입"으로, 애플리케이션 내부 용도로만 사용되며, 공백이 없어야 하며 한 번 생성 후에는 변경하지 않아야 합니다.

구독 생성 시, `customData` 메서드를 이용해 구독과 관련된 커스텀 메타데이터를 추가할 수도 있습니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

구독 체크아웃 세션이 생성되면, Cashier Paddle의 [paddle-button Blade 컴포넌트](#overlay-checkout)에 전달하여 사용할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

결제가 완료되면 Paddle에서 `subscription_created` Webhook이 전송되며, 이때 Cashier가 Webhook을 받아 내부적으로 구독을 세팅합니다. 반드시 [Webhook 처리 설정](#handling-paddle-webhooks)이 올바르게 적용되어야 합니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

유저의 구독 상태는 아래와 같은 다양한 메서드로 확인할 수 있습니다. `subscribed` 메서드는 구독이 유효한 경우(체험 기간도 포함) `true`를 반환합니다:

```php
if ($user->subscribed()) {
    // ...
}
```

애플리케이션에서 여러 구독을 제공한다면, 구독 타입을 인수로 지정할 수도 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware)로 활용해, 구독 상태에 따라 라우트 접근을 제어할 때 적합합니다:

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
            // 이 사용자는 결제한 고객이 아닙니다...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

유저가 체험 기간인지 확인하려면 `onTrial` 메서드를 사용합니다. (예: 체험 유저에게 경고 문구 표시 등):

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 Paddle price ID에 대해 구독 여부를 확인할 때는 `subscribedToPrice` 메서드를 사용할 수 있습니다:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 트라이얼 기간도, 유예 기간도 아닌 실제 활성 구독 상태인지를 판별합니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

유저가 한때 유효한 구독자였지만 현재는 구독을 취소한 경우, `canceled` 메서드로 상태를 확인할 수 있습니다:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

한편 유예 기간(grace period) 중인 경우(예: 구독이 3월 5일에 취소요청됐으나, 원래 3월 10일 만료까지 아직 기간이 남음), `onGracePeriod` 메서드로 판별할 수 있습니다. 이 기간 동안 `subscribed` 메서드는 여전히 `true`를 반환합니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 미납 상태

구독 결제에 실패하면, 구독은 `past_due` 상태로 마크됩니다. 이 상태에선 결제 정보가 갱신될 때까지 구독이 활성화되지 않습니다. `pastDue` 메서드로 확인 가능합니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

이때에는 사용자가 [결제 정보를 업데이트](#updating-payment-information)하도록 안내해야 합니다.

만약 `past_due` 구독도 유효한 것으로 간주하고 싶다면, `keepPastDueSubscriptionsActive` 메서드를 호출해 설정할 수 있습니다. 주로 `AppServiceProvider`의 `register` 메서드에서 사용합니다:

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
> `past_due` 상태에 있는 구독은 결제 정보가 갱신되기 전까지 변경할 수 없습니다. 따라서 이 상태에서는 `swap`, `updateQuantity` 메서드가 예외를 던집니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

대부분의 구독 상태는 쿼리 스코프로도 제공되어, 원하는 상태의 구독을 쉽게 검색할 수 있습니다:

```php
// 유효한 모든 구독 가져오기
$subscriptions = Subscription::query()->valid()->get();

// 해당 유저의 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 스코프 목록은 아래와 같습니다:

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
### 구독 단일 청구 (Subscription Single Charges)

구독자에게 구독 이외의 추가 청구를 하고 싶을 때는, `charge` 메서드에 하나 이상의 price ID를 넘기면 됩니다:

```php
// price 1개 청구
$response = $user->subscription()->charge('pri_123');

// price 여러 개 동시 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

이렇게 하면 실제 과금은 구독의 다음 과금 주기에 이루어집니다. 바로 결제하고 싶다면 `chargeAndInvoice` 메서드를 사용하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별로 결제 수단을 따로 저장합니다. 구독의 기본 결제 수단을 변경하려면, 구독 모델에서 `redirectToUpdatePaymentMethod` 메서드로 Paddle의 결제 정보 수정 페이지로 고객을 리디렉션하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

고객이 결제 정보를 수정하면, Paddle에서 `subscription_updated` Webhook을 전송하고, 애플리케이션의 구독 정보가 자동으로 갱신됩니다.

<a name="changing-plans"></a>
### 요금제 변경 (Changing Plans)

이미 구독 중인 고객이 새로운 요금제로 변경하고자 한다면, 구독의 `swap` 메서드에 Paddle의 price 식별자를 전달하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

구독 변경 후 즉시 고객에게 청구하고자 한다면, `swapAndInvoice` 메서드를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 프러레이션(Proration)

Paddle은 기본적으로 요금제 변경 시 청구 내역을 프러레이션 처리(즉, 요금차이 정산)합니다. 프러레이션 없이 구독을 변경하려면 `noProrate` 메서드를 사용하세요:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

프러레이션 없이 즉시 청구하려면, `swapAndInvoice` 메서드와 함께 `noProrate`를 사용할 수 있습니다:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

구독 변경 시 청구 자체를 하지 않을 경우, `doNotBill` 메서드를 사용하세요:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle의 프러레이션 정책은 [프러레이션 문서](https://developer.paddle.com/concepts/subscriptions/proration)에서 더 자세히 확인할 수 있습니다.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

구독에 "수량" 개념을 적용할 수도 있습니다. 예를 들어 프로젝트 관리 앱에서 프로젝트당 $10/월 청구 등. 구독 수량을 쉽게 증가/감소시키려면 `incrementQuantity`, `decrementQuantity` 메서드를 사용합니다:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 구독 수량을 5개씩 증가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 구독 수량을 5개씩 감소
$user->subscription()->decrementQuantity(5);
```

특정 수량으로 설정하려면 `updateQuantity` 메서드를 사용하세요:

```php
$user->subscription()->updateQuantity(10);
```

프러레이션 없이 구독 수량을 변경하려면 `noProrate()`와 함께 사용할 수 있습니다:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 상품이 포함된 구독의 수량 변경

[여러 상품이 포함된 구독](#subscriptions-with-multiple-products)의 경우, 증감할 가격의 ID를 두 번째 인수로 넘겨야 합니다:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품이 포함된 구독 (Subscriptions With Multiple Products)

[여러 상품을 포함한 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)은 하나의 구독에 여러 결제 상품을 부여할 수 있습니다. 예를 들어 헬프데스크 앱에서 기본 구독($10/월)에 라이브챗 애드온($15/월)을 추가할 수 있습니다.

구독 생성 시, `subscribe` 메서드의 첫 번째 인수로 여러 price를 배열로 전달할 수 있습니다:

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

각 price별로 수량을 지정하려면, 연관배열을 사용하세요:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 price를 추가하려면, 구독의 `swap` 메서드를 통해 현재 price와 수량 정보를 모두 포함해 호출해야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

위처럼 price를 추가하면, 다음 과금 주기에 청구됩니다. 즉시 청구하려면 `swapAndInvoice` 메서드를 사용하세요:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

price를 구독에서 삭제하려면, 제거할 price를 배열에 제외한 채로 `swap`을 호출합니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독의 마지막 price는 제거할 수 없습니다. 대신 구독을 취소해야 합니다.

<a name="multiple-subscriptions"></a>
### 다중 구독 (Multiple Subscriptions)

Paddle은 한 고객이 여러 개의 구독을 동시에 보유하는 것도 허용합니다. 예를 들어, 헬스장에서 수영 구독과 웨이트 트레이닝 구독을 각각 제공하고, 서로 다른 요금제를 부여할 수도 있습니다. 고객은 둘 중 하나 또는 모두에 구독할 수 있습니다.

구독 생성 시, `subscribe` 메서드의 두 번째 인수로 구독 타입을 문자열로 전달하면 됩니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

이 예시에서는 고객이 월간 수영 구독을 시작했습니다. 이후 연간 구독으로 변경 시, 해당 `swimming` 구독에 대해 price만 바꿀 수 있습니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

물론 구독을 완전히 취소할 수도 있습니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시정지 (Pausing Subscriptions)

구독을 일시정지하려면 구독 인스턴스에서 `pause` 메서드를 호출하세요:

```php
$user->subscription()->pause();
```

구독이 일시정지 되면 Cashier가 자동으로 데이터베이스의 `paused_at` 컬럼을 설정합니다. 예를 들어, 3월 1일에 일시정지 요청을 했지만, 실제 과금 주기가 3월 5일에 끝난다면 그때까지는 `paused` 메서드가 계속해서 `false`를 반환하다가 3월 5일 이후 `true`가 됩니다.

기본적으로 일시정지는 다음 과금 주기에 적용됩니다. 즉시 일시정지하려면 `pauseNow` 메서드를 사용하세요:

```php
$user->subscription()->pauseNow();
```

지정한 시점까지 일시정지하려면 `pauseUntil`을 사용합니다:

```php
$user->subscription()->pauseUntil(now()->addMonth());
```

즉시 일시정지하면서 특정 시점까지로 지정하려면 `pauseNowUntil` 메서드를 사용하세요:

```php
$user->subscription()->pauseNowUntil(now()->addMonth());
```

유예 기간 동안 일시정지된 상태도 `onPausedGracePeriod`로 확인할 수 있습니다:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시정지된 구독을 다시 활성화하려면 `resume` 메서드를 사용하세요:

```php
$user->subscription()->resume();
```

> [!WARNING]
> 일시정지 중인 구독은 변경할 수 없습니다. 요금제를 변경하거나 수량을 수정하려면 우선 구독을 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소 (Canceling Subscriptions)

구독을 취소하려면 구독 인스턴스에서 `cancel`을 호출합니다:

```php
$user->subscription()->cancel();
```

구독 취소 시, Cashier가 자동으로 데이터베이스의 `ends_at` 컬럼을 기록합니다. 예를 들어 3월 1일에 취소 요청 했으나 구독 만료일이 3월 5일이라면, `subscribed` 메서드는 만료일까지 `true`를 반환합니다. 이는 결제 주기가 끝날 때까지 사용자가 서비스를 계속 이용할 수 있도록 하기 위함입니다.

유예 기간 중인 취소 상태는 `onGracePeriod`로 확인할 수 있습니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 구독을 해지하려면 `cancelNow` 메서드를 사용하세요:

```php
$user->subscription()->cancelNow();
```

유예 기간 중 취소를 막고 구독을 유지하려면 `stopCancelation` 메서드를 호출하세요:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle의 구독은 취소 이후 재개할 수 없습니다. 고객이 다시 구독을 원할 경우 새로운 구독 생성이 필요합니다.

<a name="subscription-trials"></a>
## 구독 체험(Trial) (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 정보 입력 후 체험(With Payment Method Up Front)

체험 기간을 제공하되, 결제 정보를 미리 수집하고 싶다면 Paddle 대시보드에서 가격 등록 시 trial 기간을 지정해두세요. 이후 체크아웃 세션은 평소대로 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

애플리케이션이 `subscription_created` 이벤트를 받게 되면, Cashier가 구독 레코드에 trial 종료일을 세팅하고, Paddle 측에도 해당일까지 청구가 시작되지 않도록 처리됩니다.

> [!WARNING]
> 고객의 구독이 trial 만료 전에 취소되지 않는 한, trial이 끝나는 즉시 청구가 발생합니다. 따라서, 사용자에게 trial 종료일을 반드시 안내하시기 바랍니다.

유저가 trial 중인지 확인하려면 아래와 같이 합니다:

```php
if ($user->onTrial()) {
    // ...
}
```

이미 체험이 만료됐는지도 확인 가능합니다:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입에 대해 trial 여부를 확인하려면 타입을 인수로 전달하세요:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 정보 없이 체험 (Without Payment Method Up Front)

결제 정보 없이 trial을 제공하려면, 유저의 고객 레코드에 `trial_ends_at` 컬럼을 원하는 만료일로 지정하면 됩니다. 보통 회원가입 시 아래와 같은 식으로 처리합니다:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

Cashier는 이런 trial을 "일반(generic) trial"이라고 부릅니다. 즉, 특정 구독과 연결되지는 않았습니다. 이 경우에도 유저 인스턴스의 `onTrial` 메서드로 trial 상태를 확인할 수 있습니다:

```php
if ($user->onTrial()) {
    // Trial 중인 사용자...
}
```

이후 실제 구독을 만들고 싶다면 평소대로 `subscribe` 메서드를 호출하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

유저의 trial 만료일을 확인하려면 `trialEndsAt` 메서드를 사용하세요. 구독 타입을 인수로 추가하면, 해당 타입에 대한 trial 종료일을 알 수 있습니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

"일반(generic) trial" 중이며 구독은 아직 만들지 않은 경우를 확인하려면, `onGenericTrial` 메서드를 사용하세요:

```php
if ($user->onGenericTrial()) {
    // "일반" 체험기간 중인 사용자...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 연장 및 활성화 (Extend or Activate a Trial)

기존 구독의 trial 기간을 연장하려면 `extendTrial` 메서드에 만료 일시를 전달하세요:

```php
$user->subscription()->extendTrial(now()->addDays(5));
```

trial을 즉시 종료하고 구독을 활성화하려면, 구독의 `activate` 메서드를 호출할 수 있습니다:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트를 Webhook을 통해 애플리케이션에 알릴 수 있습니다. Cashier에서는 기본적으로 Webhook 컨트롤러로 연결되는 라우트를 자동으로 등록합니다. 이 컨트롤러가 모든 Webhook 요청을 처리합니다.

기본적으로 취소, 실패, 결제수단 변경 등 여러 Paddle Webhook을 자동 처리하며, 필요하다면 이 컨트롤러를 직접 확장해 별도의 Webhook 처리를 구현할 수 있습니다.

애플리케이션이 Paddle Webhook을 받을 수 있도록, Paddle 제어판에서 [Webhook URL을 설정](https://vendors.paddle.com/notifications-v2)해야 합니다. Cashier의 기본 Webhook 컨트롤러는 `/paddle/webhook` URL로 대응합니다. 설정해야 할 Webhook 항목 전체는 다음과 같습니다:

- 고객 정보 변경 (Customer Updated)
- 거래 완료 (Transaction Completed)
- 거래 변경 (Transaction Updated)
- 구독 생성 (Subscription Created)
- 구독 변경 (Subscription Updated)
- 구독 일시정지 (Subscription Paused)
- 구독 취소 (Subscription Canceled)

> [!WARNING]
> Cashier의 제공 미들웨어로 [Webhook 서명 검증](/docs/12.x/cashier-paddle#verifying-webhook-signatures)을 활성화해, 외부 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### Webhook과 CSRF 보호

Paddle Webhook은 Laravel의 [CSRF 보호](/docs/12.x/csrf)를 우회할 수 있어야 하므로, `paddle/*` 경로에 대한 CSRF 토큰 검증을 제외시켜야 합니다. 이를 위해 `bootstrap/app.php` 파일에서 아래와 같이 설정하세요:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 로컬 개발 시 Webhook

Paddle이 로컬 환경의 애플리케이션에 Webhook을 전송하려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction) 같은 서비스로 외부공개해야 합니다. [Laravel Sail](/docs/12.x/sail) 사용 시에는 Sail의 [사이트 공유 명령어](/docs/12.x/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### Webhook 이벤트 핸들러 정의

Cashier는 기본적인 구독 취소, 실패 등 공통 Paddle Webhook을 자동으로 처리합니다. 커스텀 Webhook 처리가 필요한 경우, Cashier가 발생시키는 다음의 이벤트를 청취할 수 있습니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle Webhook의 전체 페이로드를 포함합니다. 예를 들어, `transaction.billed` Webhook을 직접 처리하려면, [이벤트 리스너](/docs/12.x/events#defining-listeners)를 등록할 수 있습니다:

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
            // 이벤트 로직 구현...
        }
    }
}
```

Cashier는 또한 각 Webhook 유형별로 전용 이벤트도 발생시킵니다. Paddle에서 전달된 전체 페이로드 외에도, 처리에 사용된 모델(Billable 모델, 구독, 영수증 등) 객체도 함께 제공합니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

Webhook 라우트를 기본값이 아닌 별도로 지정하고 싶다면, `.env` 파일의 `CASHIER_WEBHOOK` 환경 변수에 전체 Webhook URL을 입력하면 됩니다. 이 URL은 Paddle 제어판에 입력한 Webhook 주소와 동일해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Webhook 서명 검증

Webhooks의 보안을 위해 [Paddle의 Webhook 서명기능](https://developer.paddle.com/webhooks/signature-verification)을 사용할 수 있습니다. Cashier는 Paddle Webhook 요청 유효성을 검사하는 미들웨어를 기본 제공하고 있습니다.

Webhook 검증을 활성화하려면, 애플리케이션의 `.env` 파일에 `PADDLE_WEBHOOK_SECRET` 환경 변수가 반드시 정의되어야 합니다. Webhook 시크릿은 Paddle 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 청구 (Single Charges)

<a name="charging-for-products"></a>
### 상품에 대한 청구 (Charging for Products)

고객에게 상품 구매(단건 결제)를 시도하려면, Billable 모델 인스턴스의 `checkout` 메서드를 통해 체크아웃 세션을 생성할 수 있습니다. `checkout`은 하나 또는 여러 price ID를 받을 수 있고, 필요하다면 연관배열로 수량을 지정할 수도 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

생성된 체크아웃 세션은 Cashier의 `paddle-button` [Blade 컴포넌트](#overlay-checkout)에 전달해, Paddle Checkout 위젯을 띄우고 결제를 완료할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

체크아웃 세션의 `customData` 메서드를 통해, 원하는 커스텀 데이터를 Paddle 트랜잭션 생성에 추가할 수도 있습니다. [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)에서 지원 가능한 옵션을 확인하세요:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불 (Refunding Transactions)

거래를 환불하면 해당 금액이 결제 수단으로 반환됩니다. Paddle 구매를 환불하려면, `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용합니다. 이 메서드는 먼저 환불 사유 문자열, 그리고 하나 또는 여러 price ID+금액이 담긴 연관배열을 인수로 받습니다. Billable 모델의 `transactions` 메서드로 거래를 조회할 수 있습니다.

예를 들어, price `pri_123` 전체와 `pri_456`은 2달러만 환불한다면:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전체 환불
    'pri_456' => 200, // 부분 환불
]);
```

전체 거래를 환불하고 싶다면 환불 사유만 전달하면 됩니다:

```php
$response = $transaction->refund('Accidental charge');
```

자세한 환불 정책은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 모든 환불은 Paddle의 승인이 필요합니다.

<a name="crediting-transactions"></a>
### 거래 크레딧 부여 (Crediting Transactions)

환불과 유사하게, 거래에 크레딧을 부여할 수도 있습니다. 크레딧은 고객의 잔고에 적립되어 미래 결제에 사용할 수 있습니다. 크레딧 부여는 '수동' 거래에만 가능합니다(예를 들어, 구독과 같은 자동 청구 거래엔 적용되지 않음):

```php
$transaction = $user->transactions()->first();

// 특정 항목에 전체 크레딧 부여
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle의 크레딧 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 크레딧은 수동 거래에만 부여 가능하며, 자동 거래(구독 등)는 Paddle이 자체적으로 크레딧 처리를 합니다.

<a name="transactions"></a>
## 거래 (Transactions)

Billable 모델의 `transactions` 프로퍼티로 고객의 거래 내역을 쉽게 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 상품 결제 및 구매를 나타내며 각 거래는 인보이스와 함께 저장됩니다. 완료된 거래만 데이터베이스에 기록됩니다.

거래 내역을 테이블에 표시하면서, 각 거래 영수증을 다운로드할 수 있는 링크도 제공합니다:

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
### 과거 및 예정된 결제 (Past and Upcoming Payments)

구독 방식의 반복 결제에 대해, 최근 결제와 다음 예정 결제를 각각 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 다만, `lastPayment`는 아직 Webhook으로 거래가 동기화되지 않았다면 `null`이며, `nextPayment`는 결제 주기가 종료됐을 때(예: 구독 취소 등) `null`이 됩니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

결제 플로우가 올바르게 동작하는지 수동으로 충분히 테스트해야 합니다.

자동화된 테스트(예: CI 환경 내)에서는 [Laravel HTTP 클라이언트](/docs/12.x/http-client#testing)의 fake 기능을 사용해 Paddle로 나가는 HTTP 요청을 모킹할 수 있습니다. 이 방식은 실제 Paddle 응답을 검증하지는 않지만, Paddle API 호출 없이도 애플리케이션 테스트가 가능합니다.
