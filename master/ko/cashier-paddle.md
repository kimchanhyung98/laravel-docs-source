# Laravel Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [설정](#configuration)
    - [결제 가능(Billable) 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매하기](#quickstart-selling-products)
    - [구독 판매하기](#quickstart-selling-subscriptions)
- [체크아웃 세션](#checkout-sessions)
    - [오버레이 체크아웃](#overlay-checkout)
    - [인라인 체크아웃](#inline-checkout)
    - [비회원(Guest) 체크아웃](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [사용자별 가격 미리보기](#customer-price-previews)
    - [할인 적용](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성하기](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 결제](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량 관리](#subscription-quantity)
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [복수 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험 기간(Trial)](#subscription-trials)
    - [결제 수단 먼저 등록 시](#with-payment-method-up-front)
    - [결제 수단 없이 체험 제공](#without-payment-method-up-front)
    - [체험기간 연장 및 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [상품 결제](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧 지급](#crediting-transactions)
- [거래](#transactions)
    - [과거 및 예정 결제 내역](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 본 문서는 Cashier Paddle 2.x의 Paddle Billing 통합에 대한 설명입니다. 여전히 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x) 문서를 참고하시기 바랍니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 쉽고 직관적인 인터페이스를 제공합니다. 반복적이고 지루한 구독 빌링 코드의 대부분을 Cashier가 처리해 줍니다. 기본적인 구독 관리뿐만 아니라, Cashier는 구독 전환, 구독 "수량" 조정, 일시 정지, 해지 유예 기간 등 다양한 기능을 제공합니다.

Cashier Paddle을 본격적으로 사용하기 전에, Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 살펴보시기를 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용하여 Paddle용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier-paddle
```

이후, `vendor:publish` Artisan 명령어를 통해 Cashier 마이그레이션 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그리고 애플리케이션의 데이터베이스 마이그레이션을 실행합니다. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성하고, 추가로 모든 고객의 구독 정보를 저장할 `subscriptions` 및 `subscription_items` 테이블도 생성합니다. 마지막으로, 고객별로 연관된 Paddle 거래 내역을 저장할 `transactions` 테이블이 만들어집니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 제대로 처리할 수 있도록 반드시 [Cashier Webhook 처리](#handling-paddle-webhooks)를 설정하세요.

<a name="paddle-sandbox"></a>
### Paddle Sandbox

로컬 또는 스테이징 환경에서 개발할 때는 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)에 가입하는 것이 좋습니다. 이 계정을 이용하면 실제 결제가 발생하지 않는 샌드박스 환경에서 충분히 테스트하고 개발할 수 있습니다. 다양한 결제 시나리오를 시뮬레이션하기 위해 Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용할 수 있습니다.

Paddle Sandbox 환경을 사용할 때는 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다:

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발을 마친 뒤에는 [Paddle 벤더 계정](https://paddle.com)을 신청할 수 있습니다. 운영 환경(프로덕션)에 배포하기 전에는 Paddle에서 애플리케이션의 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 결제 가능(Billable) 모델

Cashier를 사용하려면 우선 사용자 모델에 `Billable` 트레이트(trait)를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 갱신 등 다양한 빌링 작업을 위한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

만약 사용자가 아닌 다른 엔터티(예: 조직, 팀 등)도 결제가 가능하다면, 해당 클래스에도 이 트레이트를 추가할 수 있습니다:

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

다음으로, Paddle 키들을 애플리케이션의 `.env` 파일에 설정해야 합니다. Paddle 제어판에서 API 키를 얻을 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle Sandbox 환경](#paddle-sandbox)에서 사용할 때 `true`로, 운영 환경에서 실제 Paddle 벤더 환경을 사용할 때는 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며, Paddle의 [Retain](https://developer.paddle.com/concepts/retain/overview) 기능을 사용할 때만 설정하면 됩니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 자체 JavaScript 라이브러리를 통해 결제 위젯을 띄웁니다. 이 JavaScript 라이브러리는 애플리케이션 레이아웃의 `</head>` 태그 바로 전에 `@paddleJS` Blade 디렉티브를 삽입하여 로드할 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

인보이스의 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 이용하여 통화 로케일을 처리합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 다른 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier에서 사용되는 기본 모델을 확장하여 나만의 모델을 정의할 수 있습니다. 이 경우 Cashier의 모델을 상속한 뒤, 새로운 모델을 만듭니다:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Paddle\Cashier` 클래스를 통해 Cashier가 해당 모델을 사용하도록 지정해야 합니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다:

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
### 상품 판매하기

> [!NOTE]
> Paddle Checkout을 사용하기 전에 Paddle 대시보드에서 고정 가격의 상품을 반드시 정의해야 합니다. 그리고 반드시 [Paddle Webhook 처리를](#handling-paddle-webhooks) 설정하세요.

애플리케이션을 통해 상품 및 구독 결제 기능을 제공하는 것은 어렵게 느껴질 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 쉽게 최신 결제 기능을 구현할 수 있습니다.

반복 결제가 아닌 단일 상품 결제를 처리하고자 할 때는 Cashier를 통해 Paddle Checkout Overlay로 결제 과정을 진행하면 됩니다. 사용자가 자신의 결제 정보를 입력하고 결제를 완료하면, 지정한 성공(리턴) URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예시처럼, Cashier의 `checkout` 메서드를 활용해 고객이 Paddle Checkout Overlay에서 결제를 진행할 수 있도록 체크아웃 객체를 만듭니다. 여기서 사용되는 "price identifier"는 [특정 상품에 대해 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요하다면, `checkout` 메서드는 Paddle에 고객이 존재하지 않을 경우 자동으로 고객을 생성하고, 이 정보를 애플리케이션과 연동합니다. 체크아웃 세션이 완료되면, 고객은 원하는 성공 페이지로 이동하며 안내 메시지를 표시할 수 있습니다.

`buy` 뷰에서는 결제 Overlay를 띄울 수 있도록 버튼을 배치합니다. Cashier Paddle에는 `paddle-button` Blade 컴포넌트가 기본 제공되나, [오버레이 체크아웃을 직접 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타 데이터 제공하기

상품을 판매할 때, 자체적으로 `Cart`나 `Order` 모델을 이용해 주문 및 구매 정보를 추적하는 것이 일반적입니다. Paddle Checkout Overlay로 리디렉션할 때, 기존 주문의 식별자를 전달해 고객이 결제를 완료하고 애플리케이션으로 돌아왔을 때 주문 내역과 연결할 수 있습니다.

이를 위해 `checkout` 메서드에 커스텀 데이터 배열을 전달할 수 있습니다. 예를 들어, 사용자가 결제를 시작할 때 새로운 `Order`를 만든 상황을 가정해봅시다. (여기서 `Cart`와 `Order` 모델은 예시일 뿐 Cashier에서 제공하지 않습니다. 여러분의 애플리케이션에 맞게 구현하시면 됩니다.):

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

위 예시에서 사용자가 결제를 시작하면, 해당 장바구니나 주문에 연결된 모든 Paddle 가격 식별자를 `checkout` 메서드에 전달합니다. 이런 방식으로 "장바구니" 또는 주문과 상품 정보를 연결할 수 있습니다. 그리고 `customData` 메서드를 이용해 주문 ID를 Paddle Checkout Overlay에 함께 전달할 수 있습니다.

결제가 끝난 뒤에는 보통 주문 상태를 "완료"로 변경하기를 원할 것입니다. 이를 위해서는 Paddle이 보내는 웹훅(webhook) 이벤트와 Cashier가 방출하는 이벤트를 사용해 주문 정보를 데이터베이스에 저장하면 됩니다.

시작하려면, Cashier가 발생시키는 `TransactionCompleted` 이벤트를 청취(listen)하면 됩니다. 이 이벤트 리스너는 보통 `AppServiceProvider`의 `boot` 메서드에서 등록합니다:

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

예를 들어 `CompleteOrder` 리스너는 다음과 같은 형태가 될 수 있습니다:

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

`transaction.completed` 이벤트에 포함된 데이터에 대한 자세한 내용은 Paddle 문서의 [관련 항목](https://developer.paddle.com/webhooks/transactions/transaction-completed)을 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매하기

> [!NOTE]
> Paddle Checkout을 사용하기 전에 Paddle 대시보드에서 고정 가격의 상품을 반드시 정의해야 합니다. 그리고 반드시 [Paddle Webhook 처리를](#handling-paddle-webhooks) 설정하세요.

애플리케이션에서 상품 또는 구독 결제 기능을 제공하는 것은 복잡하게 느껴질 수 있지만, Cashier와 [Paddle Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 이용하면 손쉽게 결제 시스템을 구축할 수 있습니다.

Cashier와 Paddle의 Checkout Overlay로 구독을 판매하는 방법을 알아보기 위해 기본 월(`price_basic_monthly`) 및 연(`price_basic_yearly`) 플랜이 있는 구독 서비스를 예로 들어보겠습니다. 이 두 가격은 Paddle 대시보드의 "Basic" 상품(`pro_basic`)에 묶일 수 있습니다. 또, "Expert" 플랜(`pro_expert`)도 제공할 수 있습니다.

먼저, 고객이 어떻게 구독을 시작할 수 있는지 살펴봅니다. 보통은 애플리케이션의 요금제 페이지에서 "구독하기" 버튼을 클릭하면, Paddle Checkout Overlay가 나타나게 되고 자신의 플랜을 선택할 수 있습니다. 체크아웃 세션을 시작하려면 `checkout` 메서드를 사용합니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 결제 오버레이 버튼을 배치합니다. Cashier Paddle에 기본 포함된 `paddle-button` Blade 컴포넌트를 사용하거나, 필요하다면 [오버레이 체크아웃을 직접 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 구독 버튼을 클릭하면, 고객은 자신의 결제 정보를 입력하고 구독을 시작할 수 있습니다. 신용카드 등 일부 결제 수단은 처리가 지연될 수 있으니, 구독이 실제로 시작된 시점을 파악하려면 반드시 [Cashier의 Webhook 처리를](#handling-paddle-webhooks) 설정해야 합니다.

고객이 구독을 시작할 수 있게 되면, 특정 기능이나 영역은 구독자만 접근하도록 제한할 수 있습니다. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 이용해 현재 사용자의 구독 여부를 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 대한 구독 여부도 아래와 같이 간단히 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 확인 미들웨어 만들기

편리하게 사용하려면, 요청이 구독자인지 확인하는 [미들웨어](/docs/master/middleware)를 만들 수 있습니다. 이 미들웨어를 라우트에 할당하면, 구독하지 않은 사용자가 접근하지 못하도록 차단할 수 있습니다:

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
            // 사용자를 결제 페이지로 리디렉션하여 구독 안내...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어를 만든 뒤에는 해당 라우트에 쉽게 할당할 수 있습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 직접 요금제를 관리할 수 있도록 허용하기

고객은 언제든지 자신의 구독 플랜(상품, 티어 등)을 변경하고 싶어할 수 있습니다. 예를 들어, 월간 구독에서 연간 구독으로 전환하려면 아래와 같은 버튼을 구현할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 이 예시에서는 "$price"가 "price_basic_yearly"임.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

플랜 변경 외에도 구독 취소 기능도 제공해야 합니다. 아래와 같이 버튼을 만들어 라우트로 연결하면 됩니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이런 방식으로 구독은 청구 주기 만료 시점에 해지됩니다.

> [!NOTE]
> Cashier의 Webhook 처리를 올바르게 설정했다면, Paddle에서 구독을 변경하거나 취소해도 Cashier가 들어오는 Webhook을 통해 DB 상태를 자동으로 동기화합니다. 예를 들어, Paddle 대시보드에서 고객의 구독을 취소해도 애플리케이션 DB에서 해당 구독이 "canceled" 상태가 됩니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션 (Checkout Sessions)

고객 결제의 대부분 작업은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 사용하는 "체크아웃"을 통해 수행됩니다.

Paddle을 통해 결제 처리를 진행하기 전에, 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 Paddle 체크아웃 설정 대시보드에 정의해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃 (Overlay Checkout)

체크아웃 오버레이 위젯을 표시하기 전에, 반드시 Cashier를 통해 체크아웃 세션을 생성해야 합니다. 체크아웃 세션은 어떤 결제 작업이 수행될지 Paddle 결제 위젯에 알리는 역할을 합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/master/blade#components)가 포함되어 있습니다. 체크아웃 세션을 "프롭(prop)"으로 전달하면, 버튼을 클릭했을 때 Paddle 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 위젯은 Paddle의 기본 스타일로 표시됩니다. 필요하다면 [Paddle에서 지원하는 HTML 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 예시와 같이 컴포넌트에 추가해 다양한 옵션을 조정할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기적으로 동작합니다. 사용자가 위젯에서 구독을 생성하면, Paddle은 애플리케이션으로 Webhook을 보내며, 이를 통해 결제 상태를 데이터베이스에 갱신해야 하므로 반드시 [Webhook을 설정](#handling-paddle-webhooks)해야 합니다.

> [!WARNING]
> 구독 상태 변경 후 관련 Webhook을 받기까지의 지연은 보통 매우 짧지만, 사용자가 체크아웃을 완료한 즉시 구독 권한이 바로 활성화되지 않을 수 있음을 염두에 두고 애플리케이션을 설계하세요.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 직접 렌더링하기

Laravel의 내장 Blade 컴포넌트를 사용하지 않고 오버레이 체크아웃을 직접 렌더링할 수도 있습니다. 우선 [이전 예시처럼](#overlay-checkout) 체크아웃 세션을 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

이후 Paddle.js를 활용해 체크아웃을 초기화할 수 있습니다. 아래 예시는 `paddle_button` 클래스를 가진 링크를 만들어주며, Paddle.js가 해당 클래스를 감지해 클릭 시 오버레이 체크아웃을 보여줍니다:

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

Paddle의 "오버레이" 스타일 체크아웃 위젯을 사용하지 않으려면, 위젯을 애플리케이션 내부에 인라인으로 삽입할 수도 있습니다. 이 방식은 체크아웃의 HTML 필드를 직접 조정할 수는 없지만, 애플리케이션 내 페이지에 자연스럽게 결제 창을 넣을 수 있습니다.

Cashier에서는 인라인 체크아웃을 위해 `paddle-checkout` Blade 컴포넌트를 제공합니다. 우선 [체크아웃 세션을 생성](#overlay-checkout)합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

이후 Blade 컴포넌트의 `checkout` 속성에 세션을 전달합니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 체크아웃 컴포넌트의 높이를 조정하려면 `height` 속성을 활용할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

인라인 체크아웃의 맞춤 옵션에 대해서는 Paddle의 [Inline Checkout 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [사용 가능한 체크아웃 설정](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)을 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 직접 렌더링하기

Blade 컴포넌트를 사용하지 않고 인라인 체크아웃을 직접 렌더링할 수도 있습니다. [이전 예시처럼](#inline-checkout) 체크아웃 세션을 생성한 후, 아래와 같이 Paddle.js를 활용하면 됩니다. 이 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 이용하지만, 프론트엔드 환경에 맞게 자유롭게 수정해도 됩니다:

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
### 비회원(Guest) 체크아웃

애플리케이션의 계정이 필요하지 않은 사용자를 위한 체크아웃 세션이 필요할 때는 `guest` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이렇게 만든 체크아웃 세션도 [Paddle 버튼](#overlay-checkout)이나 [인라인 체크아웃](#inline-checkout) Blade 컴포넌트에 전달해서 사용할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle에서는 통화(국가)별로 가격을 다르게 지정할 수 있습니다. Cashier Paddle에서는 `previewPrices` 메서드를 통해 여러 가격 정보를 미리 조회할 수 있습니다. 이 메서드에는 조회할 가격 ID 목록을 넘깁니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

기본적으로 통화 정보는 요청의 IP 주소를 바탕으로 자동 결정되지만, 아래처럼 특정 국가의 가격 미리보기를 직접 지정할 수도 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회한 가격 정보는 자유롭게 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

또한, 합계와 세금을 각각 따로 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 [Paddle의 API 문서 - 가격 미리보기](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 사용자별 가격 미리보기

이미 고객이 등록된 사용자에 대해 적용 가능한 가격을 표시하고 싶다면, 해당 고객 인스턴스에서 직접 가격 정보를 얻을 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 고객의 Paddle Customer ID를 이용해 그 사용자에 맞는 통화로 가격 정보를 가져옵니다. 따라서 미국에 사는 사용자는 달러 가격을, 벨기에에 사는 사용자는 유로 가격을 받게 됩니다. 매칭되는 통화가 없으면 상품의 기본 통화가 사용됩니다. 모든 가격은 Paddle 제어판에서 커스터마이즈할 수 있습니다.

<a name="price-discounts"></a>
### 할인 적용

할인 적용 후 가격을 표시하고 싶다면 `previewPrices` 호출 시 `discount_id` 옵션을 함께 전달하면 됩니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격 정보를 표시합니다:

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

Cashier에서는 체크아웃 세션 생성 시 유용한 고객 기본값(예: 이메일, 이름 등)을 정의할 수 있습니다. 이를 오버라이드하면 결제 위젯의 이메일/이름 등 입력란이 미리 채워져 사용자 경험이 개선됩니다. 결제 가능(Billable) 모델에서 다음 메서드를 구현하세요:

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

이 기본값들은 Cashier의 모든 [체크아웃 세션](#checkout-sessions) 생성 시 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

`Cashier::findBillable` 메서드를 이용해 Paddle Customer ID로 고객을 조회할 수 있습니다. 이 메서드는 결제 가능(Billable) 모델 인스턴스를 반환합니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

구독 대신 Paddle 고객만 먼저 생성하고 싶을 때는 `createAsCustomer` 메서드를 사용할 수 있습니다:

```php
$customer = $user->createAsCustomer();
```

이 메서드는 `Laravel\Paddle\Customer` 인스턴스를 반환합니다. 고객 생성 이후 언제든지 구독을 시작할 수 있습니다. 필요하다면 Paddle API에서 지원하는 [추가 고객 생성 옵션](https://developer.paddle.com/api-reference/customers/create-customer)을 `$options` 배열로 전달할 수 있습니다:

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성하기

구독을 생성하려면, 우선 데이터베이스에서 결제 가능(Billable) 모델(보통은 `App\Models\User`)의 인스턴스를 가져옵니다. 그리고 `subscribe` 메서드를 이용해 체크아웃 세션을 만듭니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe`에 첫 번째 인수는 사용자가 구독할 Paddle 가격의 식별자입니다. 두 번째 인수는 구독의 "타입"을 의미하며, 내부적으로만 사용됩니다. 단일 구독만 제공한다면 `default`나 `primary` 등으로 지정하면 됩니다. 타입 값은 공백 없이 지정해야 하며 구독 생성 후에는 절대 변경하지 마세요.

구독에 대한 커스텀 메타데이터를 추가할 때는 `customData` 메서드를 사용합니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

체크아웃 세션이 생성된 후에는, 해당 세션을 [paddle-button] Blade 컴포넌트에 전달해 결제 UI를 구현할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

유저가 결제를 완료하면 Paddle에서는 `subscription_created` Webhook을 전송합니다. Cashier가 이를 받아 고객의 구독 정보를 설정합니다. 모든 Webhook이 제대로 처리되는지 꼭 [Webhook 처리를](#handling-paddle-webhooks) 설정하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

유저가 구독 상태인지 여부는 다양한 편의 메서드를 통해 확인할 수 있습니다. 우선, `subscribed` 메서드는 사용자가 유효한 구독을 가지고 있을 때(체험 기간도 포함하여) `true`를 반환합니다:

```php
if ($user->subscribed()) {
    // ...
}
```

여러 구독이 있을 때는 구독의 타입을 인수로 넘길 수 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/master/middleware)에서도 유용하게 쓸 수 있어, 구독 상태에 따라 특정 라우트와 컨트롤러 접근을 쉽게 제어할 수 있습니다:

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
            // 유료 고객이 아님...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

유저가 체험 기간 중인지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이를 이용해 체험 기간 안내 메시지 등을 표시할 수 있습니다:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 플랜(가격)에 대한 구독 여부는 `subscribedToPrice`로 확인할 수 있습니다. 예를 들어, 사용자의 `default` 구독이 월간 플랜에 직접 가입되어 있는지 확인하려면:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 사용자가 체험이나 유예 기간이 없는, 활성 구독 상태인지를 확인합니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 구독 취소 상태

한때 활성 구독자였으나 구독을 해지한 상태인지는 `canceled` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

구독을 취소했지만 아직 "유예 기간(grace period)"에 있는지도 확인할 수 있습니다. 예를 들어, 3월 5일에 구독을 해지했으나 3월 10일까지 효력이 남아있는 경우, 유예 기간 동안은 `subscribed` 역시 `true`를 계속 반환합니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 미납(Past Due) 상태

구독 결제 실패 시 구독이 `past_due` 상태로 표시됩니다. 이 상태에서는 고객이 결제 정보를 갱신하기 전까지 구독이 활성화되지 않습니다. `pastDue` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

이 경우, 사용자에게 [결제 정보 갱신](#updating-payment-information)을 안내해야 합니다.

만약 미납 상태에서도 구독을 유효하다고 간주하려면, Cashier의 `keepPastDueSubscriptionsActive` 메서드를 이용하세요. 보통은 `AppServiceProvider`의 `register` 메서드에서 호출하면 됩니다:

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
> `past_due` 상태에서는 구독 변경(`swap`), 수량 변경(`updateQuantity`) 등이 불가능합니다. 해당 상태에서 위 메서드를 호출하면 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 Scope

대부분의 구독 상태는 쿼리 스코프(query scope)를 통해 DB에서 손쉽게 조회할 수 있습니다:

```php
// 모든 유효한 구독 조회
$subscriptions = Subscription::query()->valid()->get();

// 사용자의 취소된 구독만 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 모든 스코프는 아래와 같습니다:

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
### 구독 단일 결제

구독에 추가로 일회성 단일 결제를 청구(single charge)할 수 있습니다. `charge` 메서드에 하나 이상의 가격 ID를 전달하세요:

```php
// 한 개 가격 청구
$response = $user->subscription()->charge('pri_123');

// 여러 가격을 한 번에 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge` 메서드는 실제 청구 과금은 구독의 다음 결제 주기에 이뤄집니다. 즉시 결제하고 싶다면 `chargeAndInvoice` 메서드를 사용하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별로 결제 수단을 저장합니다. 구독의 기본 결제 수단을 업데이트하고 싶을 때는 Paddle에서 호스팅하는 결제 수단 업데이트 페이지로 리디렉션하면 됩니다. 구독 모델의 `redirectToUpdatePaymentMethod` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

정보 업데이트가 완료되면 Paddle은 `subscription_updated` Webhook을 전송하고, Cashier가 애플리케이션 DB의 구독 정보를 갱신합니다.

<a name="changing-plans"></a>
### 플랜 변경

고객이 구독 플랜을 변경하고자 할 때는, 구독의 `swap` 메서드에 Paddle 가격 식별자를 넘기면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 결제서를 발송하고 싶다면 `swapAndInvoice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 비례배분(Proration)

기본적으로 Paddle은 플랜 변경 시 요금을 비례배분(prorate)합니다. 비례배분 없이 구독을 변경하려면 `noProrate` 메서드를 사용하세요:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

비례배분 없이 즉시 인보이스를 발행하려면 `swapAndInvoice`와 `noProrate`를 함께 사용하면 됩니다:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

플랜 변경 시 결제하지 않도록 하려면 `doNotBill`을 사용하세요:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle의 비례배분 정책에 대해 더 자세히 알고 싶다면 [관련 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량 관리

구독에서 수량을 조정해야 할 경우(예: 월 $10씩 프로젝트 개수만큼 과금하는 앱 등), 아래 메서드로 간편하게 수량을 증감할 수 있습니다:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 5개 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 5개 빼기
$user->subscription()->decrementQuantity(5);
```

특정 수량을 직접 지정하려면 `updateQuantity` 메서드를 사용하세요:

```php
$user->subscription()->updateQuantity(10);
```

비례배분 없이 수량을 업데이트하려면 `noProrate`와 함께 사용합니다:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 상품이 포함된 구독의 수량 관리

만약 구독이 [여러 상품을 포함](#subscriptions-with-multiple-products)한다면, 증감하려는 가격의 ID를 두 번째 인수로 넘겨줘야 합니다:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품이 포함된 구독

[여러 상품이 포함된 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)은 하나의 구독에 여러 상품을 복수로 할당해 각각 청구할 수 있게 해줍니다. 예를 들어, 헬프데스크 앱이 기본 요금제 $10/월과 라이브챗 애드온 $15/월을 함께 팔 수 있습니다.

구독 체크아웃 세션을 생성할 때는 첫 번째 인수로 가격 배열을 넘기면 됩니다:

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

위 예시에서 고객의 `default` 구독에 두 가격이 함께 추가됩니다. 각 가격은 해당 청구 주기에 따라 요금이 부과됩니다. 가격별로 수량을 따로 지정하려면 아래처럼 연관 배열을 넘기면 됩니다:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 가격을 추가하려면 `swap` 메서드를 이용해야 하며, 이때 반드시 현재 구독에 포함된 모든 가격 및 수량을 함께 넘겨야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

이 경우, 새 가격이 추가되지만 다음 청구 주기에 과금됩니다. 즉시 결제서를 발행하려면 `swapAndInvoice`를 사용하세요:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

특정 가격을 구독에서 제거하려면 `swap` 메서드 호출에서 해당 가격을 포함시키지 않으면 됩니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서 마지막 가격을 제거하는 것은 불가능하며, 이 경우 구독을 취소해야 합니다.

<a name="multiple-subscriptions"></a>
### 복수 구독

Paddle은 고객이 여러 개의 구독을 동시에 가질 수 있도록 지원합니다. 예를 들어, 헬스장에서 수영 구독과 웨이트 구독을 따로 결제하는 경우를 들 수 있습니다.

애플리케이션에서 여러 구독을 만들 때는 `subscribe`의 두 번째 인수로 구독 타입을 지정하면 됩니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

이 예시처럼 수영종목 월간 구독을 만들 수도 있고, 추후 연간 구독으로 전환할 때는 해당 타입에 가격만 변경하면 됩니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

전체 구독을 취소할 수도 있습니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시정지

구독을 일시정지하려면, 구독 모델에서 `pause` 메서드를 호출합니다:

```php
$user->subscription()->pause();
```

구독이 일시정지되면 Cashier는 DB의 `paused_at` 컬럼을 자동으로 갱신합니다. 이 컬럼을 이용해 `paused` 메서드가 언제부터 `true`를 반환할지 판단합니다. 예를 들어, 3월 1일에 정지 요청했지만 3월 5일에 결제가 예정되어 있다면 3월 5일까지는 `paused`가 `false`를 반환합니다. 즉, 대개 유료로 결제한 기간은 남은 기간 끝까지 사용할 수 있게 됩니다.

기본적으로 정지는 다음 결제 주기부터 적용되지만, 즉시 정지하고 싶다면 `pauseNow` 메서드를 사용하세요:

```php
$user->subscription()->pauseNow();
```

특정 시점까지 정지하려면 `pauseUntil`을, 즉시 특정 시점까지 정지하려면 `pauseNowUntil`을 사용합니다:

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

"정지 유예 기간"에 있는지 확인하려면 `onPausedGracePeriod` 메서드를 사용하세요:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

정지된 구독을 다시 활성화하려면 `resume` 메서드를 호출합니다:

```php
$user->subscription()->resume();
```

> [!WARNING]
> 정지 상태에서는 구독 수정이 불가능합니다. 플랜 전환, 수량 변경 등을 하려면 구독을 먼저 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 구독 모델에서 `cancel` 메서드를 호출합니다:

```php
$user->subscription()->cancel();
```

구독을 취소하면 Cashier가 자동으로 DB의 `ends_at` 컬럼을 갱신합니다. 예를 들어, 3월 1일에 취소를 신청해도 원래 구독 만료일이 3월 5일이라면, 3월 5일까지는 여전히 `subscribed()`가 `true`를 반환합니다.

"유예 기간"에 해당하는지 확인하려면 `onGracePeriod`를 사용하세요:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 구독을 종료하려면 `cancelNow`를 사용하세요:

```php
$user->subscription()->cancelNow();
```

유예 기간 상태의 구독 취소를 중단하려면 `stopCancelation` 메서드를 호출하세요:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle 구독은 취소 후 재개가 불가능합니다. 고객이 다시 사용을 원하면 반드시 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 먼저 등록 시(With Payment Method Up Front)

결제 수단 정보를 먼저 받고 체험 기간을 제공하려면 Paddle 대시보드에서 구독 가격에 체험 기간을 설정한 후 평소처럼 체크아웃 세션을 시작하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트 수신 시, Cashier는 체험 종료일을 DB에 기록하고, Paddle에는 체험 기간이 끝난 뒤부터 결제가 진행되도록 지시합니다.

> [!WARNING]
> 체험 만료 전에 구독이 취소되지 않으면 즉시 결제가 발생하므로, 체험 종료 예정일을 반드시 사용자에게 알리세요.

사용자가 체험 중인지 확인하려면 아래와 같이 `onTrial` 메서드를 사용합니다:

```php
if ($user->onTrial()) {
    // ...
}
```

체험이 만료되었는지는 `hasExpiredTrial`로 확인할 수 있습니다:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입의 체험 기간만 확인하려면 타입을 인수로 전달합니다:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 체험 제공(Without Payment Method Up Front)

결제 정보를 먼저 받지 않고 체험 기간을 제공하려면, 사용자에 연결된 고객 레코드의 `trial_ends_at` 컬럼을 원하는 날짜로 지정하면 됩니다. 보통 회원 가입 시 설정합니다:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```

이것을 "일반(Generic) 체험"이라고 하며, 아직 구독과 연결되지 않은 체험 기간입니다. `User` 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at`을 지나지 않았다면 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // 유저는 체험 기간 중...
}
```

구독 생성이 필요할 때는 평소처럼 `subscribe` 메서드를 사용하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

사용자의 체험 기간 종료일을 구하려면 `trialEndsAt` 메서드를 사용하며, 타입을 선택할 수도 있습니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

아직 실제 구독 생성 전 "일반(Generic) 체험" 기간 중인지 확인하려면 `onGenericTrial`을 사용할 수 있습니다:

```php
if ($user->onGenericTrial()) {
    // 유저는 "일반(Generic) 체험" 기간 중...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험기간 연장 및 활성화

기존 구독의 체험 기간을 연장하려면 `extendTrial` 메서드에 종료 시점을 넘깁니다:

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```

반대로, 즉시 체험을 종료하고 구독을 활성화하려면 `activate` 메서드를 호출하면 됩니다:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트를 Webhook을 통해 애플리케이션에 통보할 수 있습니다. 기본적으로, Cashier 서비스 프로바이더는 Webhook 컨트롤러로 연결되는 라우트를 자동 등록합니다. 이 컨트롤러가 모든 Webhook 요청을 처리합니다.

기본 컨트롤러에서는 결제 실패 시 구독 취소, 구독 상태 갱신, 결제 수단 변경 등 일반적인 Paddle Webhook을 자동으로 처리합니다. 물론, 필요하다면 사용자 정의 Webhook 처리를 추가할 수도 있습니다.

애플리케이션에서 Paddle Webhook을 처리하려면 [Paddle 제어판에서 Webhook URL을 설정](https://vendors.paddle.com/notifications-v2)해야 합니다. 기본적으로 Cashier의 Webhook 컨트롤러는 `/paddle/webhook` 경로를 사용합니다. Paddle 제어판에서 반드시 아래 모든 Webhook을 활성화하세요:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Cashier에서 제공하는 [Webhook 서명 검증](/docs/master/cashier-paddle#verifying-webhook-signatures) 미들웨어로 반드시 들어오는 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### Webhook과 CSRF 보호

Paddle Webhook은 Laravel의 [CSRF 보호](/docs/master/csrf)를 우회해야 하므로, `paddle/*` 엔드포인트에 대해 CSRF 검증이 적용되지 않도록 해야 합니다. 보통 애플리케이션의 `bootstrap/app.php`에 아래처럼 예외를 등록합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### Webhook과 로컬 개발환경

로컬 개발 환경에서 Paddle이 Webhook을 전송하려면, [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction) 같은 사이트 공유 서비스를 통해 애플리케이션을 외부에 노출해야 합니다. [Laravel Sail](/docs/master/sail)로 개발 중이라면 Sail의 [사이트 공유 명령어](/docs/master/sail#sharing-your-site)를 활용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### Webhook 이벤트 핸들러 정의

Cashier는 결제 실패로 인한 구독 취소 등 자주 발생하는 Paddle Webhook을 자동으로 처리합니다. 하지만 추가적으로 처리할 이벤트가 있다면 Cashier가 방출하는 아래 이벤트들을 청취하면 됩니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

양쪽 모두 Paddle Webhook의 전체 payload 정보를 담고 있습니다. 예를 들어, `transaction.billed` Webhook을 처리하려면 [리스너](/docs/master/events#defining-listeners)를 아래와 같이 작성할 수 있습니다:

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
            // Handle the incoming event...
        }
    }
}
```

Cashier는 수신된 Webhook 타입에 따라 모델과 함께 제공되는 전용 이벤트도 방출합니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

Webhooks의 기본 내장 라우트를 오버라이드하고 싶다면 `.env` 파일에 `CASHIER_WEBHOOK` 환경 변수를 지정할 수 있습니다. 이 값은 Paddle 제어판에 등록한 URL과 반드시 일치해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### Webhook 서명 검증

Webhook 보안을 위해 [Paddle Webhook 서명](https://developer.paddle.com/webhooks/signature-verification) 기능을 사용할 수 있습니다. Cashier는 Paddle Webhook 요청의 유효성을 검증하는 미들웨어를 자동 포함합니다.

Webhook 검증 활성화를 위해서는 `.env`에 `PADDLE_WEBHOOK_SECRET` 변수값을 지정하면 됩니다. 해당 시크릿은 Paddle 계정 대시보드에서 확인 가능합니다.

<a name="single-charges"></a>
## 단일 결제 (Single Charges)

<a name="charging-for-products"></a>
### 상품 결제

고객에게 단일 상품 결제를 유도하고자 한다면, 결제 가능(Billable) 모델 인스턴스의 `checkout` 메서드에서 체크아웃 세션을 생성합니다. 인수로 하나 이상 가격 ID를 넘기고, 필요하다면 상품별 수량 정보를 연관 배열로 넘길 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

체크아웃 세션을 생성한 후에는 Cashier의 [paddle-button] Blade 컴포넌트로 고객이 Paddle 결제 창에서 주문을 마칠 수 있도록 구현합니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`customData` 메서드를 활용해 체크아웃 세션에 원하는 커스텀 데이터를 추가할 수도 있습니다. 데이터 형식 및 옵션은 [Paddle 공식 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불

환불은 결제 시 사용한 결제 수단으로 금액이 반환되도록 합니다. Paddle에서 환불을 처리하려면 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용하세요. 첫 번째 인수는 사유, 두 번째는 환불할 가격 ID(들)과 환불 금액(연관 배열)을 지정하면 됩니다. 특정 유저의 거래 내역은 `transactions` 메서드로 가져올 수 있습니다.

예를 들어, `pri_123`은 전액 환불, `pri_456`에는 2달러만 부분 환불하고 싶다면:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 2달러만 환불
]);
```

전제 거래를 환불할 때는 사유만 지정하면 됩니다:

```php
$response = $transaction->refund('Accidental charge');
```

환불 관련 자세한 정보는 [Paddle Refund 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 환불 처리는 반드시 Paddle의 승인을 받아야 최종 완료됩니다.

<a name="crediting-transactions"></a>
### 거래 크레딧 지급

환불과 유사하게, 거래 금액을 크레딧 형태로 지급할 수도 있습니다. 크레딧은 고객 잔액에 추가되어, 이후 결제에서 사용할 수 있습니다. 크레딧은 수동 결제만 가능하며 구독 등 자동 결제에는 사용되지 않습니다(Paddle이 자동으로 처리합니다):

```php
$transaction = $user->transactions()->first();

// 특정 아이템 전액 크레딧 지급
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 정보는 [Paddle 크레딧 지급 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 자동 결제는 크레딧 지급이 불가하며, 수동 결제에만 적용할 수 있습니다. 자동 결제의 경우 Paddle에서 직접 크레딧을 처리합니다.

<a name="transactions"></a>
## 거래 (Transactions)

결제 가능(Billable) 모델의 `transactions` 프로퍼티로 거래 내역 배열을 간단히 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 제품/구매 결제를 나타내며, 각 거래에는 청구서(인보이스)가 첨부됩니다. 완료된 거래만 애플리케이션 데이터베이스에 저장됩니다.

고객 거래 내역을 표로 표시할 때는 트랜잭션 인스턴스의 메서드를 사용해 결제 정보를 자유롭게 렌더링할 수 있습니다. 예를 들어, 거래 목록과 다운로드 링크를 제공할 수 있습니다:

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

`download-invoice` 라우트 예시는 다음과 같습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정 결제 내역

반복 구독의 과거 결제 내역 또는 다음 결제 예정 내역은 `lastPayment`, `nextPayment` 메서드로 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환하며, 거래가 아직 Webhook으로 연동되지 않았다면 `lastPayment`는 `null`을, 결제 주기가 종료되었다면(구독 취소 등) `nextPayment`는 `null`을 반환합니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시, 실제 결제 흐름이 제대로 동작하는지 수동으로 확인하는 것이 중요합니다.

자동화된 테스트 환경(CI 포함)에서는 [Laravel HTTP 클라이언트](/docs/master/http-client#testing)로 Paddle에 대한 HTTP 호출을 Fake 처리할 수 있습니다. 비록 실제 Paddle 응답을 테스트할 수는 없지만, API 호출 없이 애플리케이션의 나머지 동작을 테스트할 수 있는 방법입니다.
