# 라라벨 Cashier (Paddle) (Laravel Cashier (Paddle))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [과금 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [체크아웃 세션](#checkout-sessions)
    - [오버레이 체크아웃](#overlay-checkout)
    - [인라인 체크아웃](#inline-checkout)
    - [비회원 체크아웃](#guest-checkouts)
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
    - [구독 단일 결제](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [요금제 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [여러 제품의 구독](#subscriptions-with-multiple-products)
    - [복수 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 정보 선입력 체험](#with-payment-method-up-front)
    - [결제 정보 미입력 체험](#without-payment-method-up-front)
    - [체험 기간 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [제품 단일 결제](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧 지급](#crediting-transactions)
- [거래 내역](#transactions)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x 버전의 Paddle Billing 연동에 대한 가이드입니다. 여전히 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x) 문서를 참고하시기 바랍니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 쉽고 유연하게 사용할 수 있도록 도와주는 인터페이스를 제공합니다. 복잡한 구독 결제 관련 코드의 대부분을 Cashier가 대신 처리해줍니다. 기본적인 구독 관리 이외에도, Cashier는 구독 변경, 구독 "수량", 구독 일시 정지, 취소 후 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 본격적으로 사용하기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview) 및 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 참고하시기를 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier를 새로운 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼하게 확인하셔야 합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용하여 Paddle용 Cashier 패키지를 설치합니다.

```shell
composer require laravel/cashier-paddle
```

그 다음, `vendor:publish` 아티즌 명령어를 사용하여 Cashier에서 제공하는 마이그레이션 파일을 퍼블리시해줍니다.

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션이 수행되면, `customers` 테이블이 새로 생성됩니다. 또한 모든 고객의 구독 정보를 저장할 수 있도록 `subscriptions` 및 `subscription_items` 테이블이 만들어지며, 마지막으로 고객과 연관된 Paddle 거래 정보를 기록할 `transactions` 테이블도 생성됩니다.

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리하려면, [Cashier의 webhook 처리를 반드시 설정](#handling-paddle-webhooks)해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 및 스테이징 환경에서 개발할 때는 [Paddle 샌드박스 계정](https://sandbox-login.paddle.com/signup)을 등록하세요. 샌드박스 계정은 실제 결제가 발생하지 않는 안전한 테스트 환경을 제공합니다. 다양한 결제 시나리오를 테스트하려면 Paddle에서 제공하는 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용하면 됩니다.

Paddle 샌드박스 환경을 사용할 때는, 애플리케이션의 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정해야 합니다.

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발을 완료했다면 [Paddle 벤더 계정](https://paddle.com) 신청을 진행할 수 있습니다. 운영 환경에서 애플리케이션을 출시에 앞서 Paddle 측의 도메인 승인이 필요하니 참고하세요.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 과금 가능 모델

Cashier를 사용하기 전에, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트를 통해 구독 생성, 결제 정보 업데이트 등 다양한 과금 관련 메서드를 사용할 수 있습니다.

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

만약 사용자가 아닌 다른 엔터티(예: Team 등)가 과금 대상이라면, 해당 클래스에도 트레이트를 추가할 수 있습니다.

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

다음으로, 애플리케이션의 `.env` 파일에 Paddle API 키들을 설정해야 합니다. 키 값은 Paddle 관리자 페이지에서 확인할 수 있습니다.

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle 샌드박스 환경](#paddle-sandbox) 사용 시 `true`로, 운영 환경에서 라이브 Paddle 벤더 계정을 사용할 때는 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며, [Retain](https://developer.paddle.com/concepts/retain/overview) 기능을 사용할 때만 지정하면 됩니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 결제 위젯 실행을 위해 자체 자바스크립트 라이브러리에 의존합니다. 애플리케이션 레이아웃의 `<head>` 태그 닫기 직전에 `@paddleJS` Blade 디렉티브를 추가해 Paddle JS를 로드할 수 있습니다.

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

청구서 등에서 금액을 표기할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용해 통화 로케일을 적용합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면, 서버에 PHP `ext-intl` 확장 모듈이 설치되어 있고 올바르게 설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Cashier에서 내부적으로 사용하는 모델을 직접 확장하여 사용할 수도 있습니다. Cashier의 모델을 상속받아 자신만의 모델을 정의하세요.

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후에는, `Laravel\Paddle\Cashier` 클래스를 통해 Cashier에 사용자 정의 모델을 지정해주어야 합니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 Cashier에게 커스텀 모델을 알려줍니다.

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
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 제품 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격의 제품(Product)을 먼저 정의해야 합니다. 또한 [Paddle Webhook 처리를 반드시 설정](#handling-paddle-webhooks)해야 합니다.

애플리케이션에서 제품 및 구독 결제를 제공하는 일은 복잡하게 느껴질 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 활용하면, 쉽고 견고한 결제 연동을 구현할 수 있습니다.

비구독 단일 결제 상품의 결제가 필요한 경우, Cashier를 이용해 Paddle의 Checkout Overlay로 고객이 결제 정보를 입력하고 구매를 확정하도록 할 수 있습니다. 결제가 완료되면, 고객은 설정한 성공 URL로 리다이렉트됩니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예시와 같이, Cashier의 `checkout` 메서드를 사용하여 결제에 사용할 "가격 식별자"로 Paddle Checkout Overlay를 띄울 수 있습니다. Paddle에서 "prices"란, [특정 제품에 대한 고정 가격 정보](https://developer.paddle.com/build/products/create-products-prices)를 뜻합니다.

필요하다면, `checkout` 메서드가 자동으로 Paddle에서 고객을 생성하고, Paddle 고객 정보를 애플리케이션의 사용자와 연결해줍니다. 결제 세션이 끝나면 고객은 별도의 성공 페이지로 이동하며, 이곳에서 구매 성공 메시지 등 안내를 표시할 수 있습니다.

`buy` 뷰에서는 Checkout Overlay를 호출하는 버튼을 추가합니다. Cashier Paddle에서 `paddle-button` Blade 컴포넌트가 기본 제공되지만, [수동으로 오버레이 체크아웃을 랜더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 제공

제품 판매 시, 보통 구매 완료된 주문이나 구매 제품을 추적하기 위해 애플리케이션에서 `Cart`나 `Order` 모델을 활용합니다. 고객이 Paddle Checkout Overlay 결제 화면으로 이동할 때, 기존 주문의 식별자를 함께 전달하여, 결제 완료 후 고객이 애플리케이션으로 돌아올 때 해당 주문과 연결할 수 있습니다.

이를 위해, `checkout` 메서드에 커스텀 데이터를 배열로 전달하면 됩니다. 예를 들어, 사용자가 결제를 시작하면 새로운 대기(Order) 객체를 만든다고 가정해봅시다. 이때 `Cart`와 `Order` 모델은 예시용이며, Cashier에서 기본적으로 제공하는 모델은 아닙니다. 실제 사용 시에는 프로젝트 요구사항에 맞게 자유롭게 구현하시면 됩니다.

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

이 예시처럼, 고객이 결제 과정을 시작하면 해당 주문과 연관된 모든 Paddle 가격 식별자를 `checkout` 메서드에 전달하고 있습니다. 결제 품목(=카트, 주문 등)과 가격 정보의 매핑은 애플리케이션에서 직접 관리해야 합니다. 추가로, `customData` 메서드를 사용해 주문의 ID를 Paddle Checkout Overlay에 함께 전달합니다.

물론, 고객이 결제 과정을 정상적으로 끝마치면 해당 주문을 "완료" 상태로 갱신해야 하겠죠. 이를 위해 Paddle에서 제공하는 webhook 신호를 받아 Cashier가 발생시키는 이벤트를 수신하여 주문 상태를 DB에 반영하면 됩니다.

먼저, Cashier에서 `TransactionCompleted` 이벤트를 리스닝합니다. 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 리스너를 등록합니다.

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

예시에서 `CompleteOrder` 리스너는 다음과 같이 구현할 수 있습니다.

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

자세한 데이터 구조는 Paddle 공식 문서의 [`transaction.completed` 이벤트 내용](https://developer.paddle.com/webhooks/transactions/transaction-completed)을 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격의 제품(Product)을 먼저 정의해야 합니다. 또한 [Paddle Webhook 처리를 반드시 설정](#handling-paddle-webhooks)해야 합니다.

애플리케이션에서 제품 및 구독 결제를 제공하는 일은 쉽지 않을 수 있습니다. 그러나 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 함께 사용하면, 현대적인 결제 경험을 빠르게 구축할 수 있습니다.

Cashier와 Paddle Checkout Overlay로 구독을 판매하는 기본적인 흐름을 살펴보겠습니다. 예를 들어, 한 달(`price_basic_monthly`) 또는 1년(`price_basic_yearly`) 요금제가 있는 가장 단순한 구독 서비스가 있다고 가정해봅시다. 이 둘은 Paddle 대시보드의 "Basic" 제품(`pro_basic`) 아래에 연결할 수 있습니다. 추가로, "Expert" 요금제인 `pro_expert`도 있다고 가정할 수 있습니다.

먼저, 실제로 고객이 어떻게 구독을 시작하는지부터 알아보겠습니다. 예를 들어, 애플리케이션의 가격 페이지에서 Basic 요금제의 "구독" 버튼을 클릭할 수 있습니다. 이 버튼이 Paddle Checkout Overlay를 호출하여 결제 과정을 시작할 수 있습니다. `checkout` 메서드를 통해 체크아웃 세션을 만듭니다.

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 팝업 형태의 Checkout Overlay를 띄우는 버튼을 추가합니다. Cashier Paddle에서 `paddle-button` Blade 컴포넌트가 기본으로 제공되지만, [수동으로 오버레이 체크아웃을 랜더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 "Subscribe" 버튼을 클릭하면 고객이 결제 정보를 입력해서 실제 구독을 시작할 수 있습니다. 실제 구독이 시작되는 시점을 판단하려면(일부 결제 방법은 처리 시간이 필요함), [Cashier의 webhook 처리 설정](#handling-paddle-webhooks)도 함께 완료해야 합니다.

구독 기능이 구현되면, 구독 중인 사용자만 접근할 수 있는 곳을 별도로 제한해야 할 수 있습니다. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 활용해 사용자의 현재 구독 상태를 쉽게 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 제품 또는 가격의 구독 여부도 편리하게 확인할 수 있습니다.

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

더 편리하게 관리하기 위해, 구독 중인 사용자인지 요청 단계에서 판단하는 [미들웨어](/docs/12.x/middleware)를 만들어볼 수 있습니다. 이 미들웨어를 라우트에 지정하면, 구독하지 않은 사용자가 접근하는 것을 쉽게 막을 수 있습니다.

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
            // 사용자를 결제 페이지로 리다이렉트하며 구독을 유도합니다...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

이렇게 생성한 미들웨어는 다음과 같이 라우트에 연결할 수 있습니다.

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 스스로 요금제를 관리하도록 허용하기

사용자가 자신의 구독 요금제를 다른 상품이나 "등급"으로 변경하고 싶어할 수 있습니다. 예를 들어, 월간 요금제에서 연간 요금제로 전환하도록 허락해주려면 아래와 같은 버튼을 연결된 라우트에 만들어주면 됩니다.

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 예시에서는 "price_basic_yearly"가 "$price" 역할을 합니다.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

요금제 변경과 마찬가지로, 고객이 구독을 취소할 수 있도록 해주어야 합니다. 아래와 같이 취소 버튼을 통해 라우트를 연결할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이제 구독은 남은 결제 주기 이후 자동으로 취소 처리됩니다.

> [!NOTE]
> Cashier의 webhook 처리가 정상적으로 구성되어 있다면, Paddle의 대시보드에서 구독을 취소하더라도 Cashier가 웹훅을 통해 해당 구독을 애플리케이션 데이터베이스에서 "취소" 상태로 자동 동기화해줍니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션

대부분의 결제 처리는 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통해 "체크아웃" 세션으로 이루어집니다.

Paddle을 이용하여 결제 처리를 시작하기 전에, 애플리케이션의 [기본 결제 링크 설정](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)을 Paddle checkout 설정에서 반드시 완료해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃

Checkout Overlay 위젯을 띄우기 전, 먼저 Cashier를 통해 체크아웃 세션을 생성해야 합니다. 이 세션 정보를 위젯에 넘기면 어떤 결제 작업을 수행할지 Paddle에 알려줄 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier는 결제 세션을 `paddle-button` [Blade 컴포넌트](/docs/12.x/blade#components)로 넘길 수 있습니다. 이 버튼을 클릭하면 Paddle의 결제 위젯이 팝업됩니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이 기본 사용 방식에서는 Paddle의 기본 스타일이 적용된 위젯이 나타납니다. `data-theme='light'`와 같이 [Paddle에서 지원하는 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 Blade 컴포넌트에 추가해 위젯을 커스텀할 수 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기적으로 동작합니다. 사용자가 위젯 내에서 구독 결제를 완료하면, Paddle이 애플리케이션에 webhook을 전송하여 구독 상태를 DB에서 정확히 반영할 수 있도록 해줍니다. 반드시 [웹훅 설정](#handling-paddle-webhooks)을 올바르게 해야 Paddle이 전송하는 상태 변경을 수신할 수 있습니다.

> [!WARNING]
> 구독 상태 변경 후 webhook 도착까지 소요되는 시간은 일반적으로 매우 짧지만, 결제가 바로 반영되지 않을 수도 있다는 점을 코드 로직에서 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 직접 랜더링하기

라라벨에서 제공하는 Blade 컴포넌트를 사용하지 않고 직접 오버레이 체크아웃을 랜더링할 수도 있습니다. [앞서 소개한 방법](#overlay-checkout)대로 체크아웃 세션을 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

이제 Paddle.js를 이용해 체크아웃을 띄울 수 있습니다. 아래 예시는 Paddle 버튼 역할을 할 링크에 `paddle_button` 클래스를 지정해두었습니다. Paddle.js가 이 클래스를 인식해 클릭 시 오버레이 체크아웃을 표시해줍니다.

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
### 인라인 체크아웃

Paddle의 "오버레이" 형태 위젯 대신, 위젯을 애플리케이션 내에 바로 삽입하는 인라인(내장) 체크아웃 기능도 제공합니다. 이 방식은 체크아웃 폼의 HTML 필드를 커스터마이즈할 수는 없지만, UI를 원하는 곳에 임베드할 수 있다는 장점이 있습니다.

Cashier는 인라인 체크아웃을 쉽게 사용할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. 사용 방법은 [오버레이 체크아웃과 동일하게](#overlay-checkout) 세션을 먼저 생성한 뒤 아래처럼 Blade에서 넣어주면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

이제 컴포넌트에 `checkout` 속성으로 세션을 넘기면 됩니다.

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 체크아웃 컴포넌트의 높이를 조정하고 싶다면, `height` 속성을 전달할 수 있습니다.

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

인라인 체크아웃의 상세 커스터마이징 옵션은 Paddle 공식 문서의 [Inline Checkout 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [결제창 설정 가이드](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 직접 랜더링하기

Blade 컴포넌트를 사용하지 않고도 인라인 체크아웃을 직접 구현할 수 있습니다. [앞선 예시와 동일하게](#inline-checkout) 체크아웃 세션을 먼저 만듭니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그 다음 Paddle.js를 활용해 인라인 체크아웃을 띄울 수 있습니다. 본 예시에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용했지만, 프론트엔드 환경에 맞게 자유롭게 구현하셔도 됩니다.

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

### 비회원 결제(Guest Checkouts)

애플리케이션에 계정을 만들 필요가 없는 사용자를 위해 결제 세션을 생성해야 할 때가 있습니다. 이럴 때는 `guest` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이렇게 생성한 결제 세션을 [Paddle 버튼](#overlay-checkout) 또는 [인라인 결제](#inline-checkout) Blade 컴포넌트에 전달할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기(Price Previews)

Paddle은 통화별로 가격을 맞춤 설정할 수 있어, 국가별로 서로 다른 가격을 지정할 수 있습니다. Cashier Paddle은 `previewPrices` 메서드를 사용해서 이 모든 가격 정보를 조회할 수 있습니다. 이 메서드에는 조회하려는 가격 ID 목록을 전달합니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화 정보는 요청의 IP 주소를 바탕으로 결정됩니다. 다만, 특정 국가의 가격을 별도로 조회하고 싶다면 아래처럼 옵션을 추가로 지정할 수 있습니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

이렇게 가격 정보를 받아온 뒤에 원하는 방식으로 표시하면 됩니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

가격의 소계와 세금 금액을 각각 따로 표시하고 싶을 때는 아래와 같이 할 수 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

더 자세한 내용은 [Paddle의 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하십시오.

<a name="customer-price-previews"></a>
### 고객별 가격 미리보기(Customer Price Previews)

이미 고객인 사용자에 대해 해당 고객에게 적용되는 가격을 보여주고 싶다면, 고객 인스턴스에서 직접 가격 정보를 조회할 수 있습니다.

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 사용자의 고객 ID를 사용해 해당 사용자의 통화로 가격 정보를 불러옵니다. 따라서 미국에 거주하는 사용자는 미국 달러로, 벨기에에 거주하는 사용자는 유로로 가격이 표시됩니다. 만약 일치하는 통화를 찾지 못하면 상품의 기본 통화를 사용합니다. 상품이나 구독 플랜의 모든 가격은 Paddle 콘트롤 패널에서 설정할 수 있습니다.

<a name="price-discounts"></a>
### 할인(Discounts) 적용

할인 적용 후의 가격을 표시하고 싶을 때는, `previewPrices`를 호출할 때 `discount_id` 옵션을 전달하면 됩니다.

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 할인 적용 가격은 다음과 같이 출력할 수 있습니다.

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
## 고객(Customers)

<a name="customer-defaults"></a>
### 고객 기본 정보(Customer Defaults)

Cashier를 사용하면 결제 세션 생성 시 고객을 위한 기본값을 지정할 수 있습니다. 이 기본값을 지정하면 결제 위젯에 고객의 이메일과 이름이 미리 입력되어, 고객이 바로 결제 단계로 넘어갈 수 있습니다. 다음과 같이 빌링 가능한 모델에서 해당 메서드를 오버라이드하면 기본값을 설정할 수 있습니다.

```php
/**
 * Paddle과 연결할 고객 이름 반환.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Paddle과 연결할 고객 이메일 주소 반환.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이렇게 지정한 기본 정보는 Cashier에서 [결제 세션](#checkout-sessions)을 생성하는 모든 동작에 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회(Retrieving Customers)

Paddle 고객 ID를 사용해서 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하면 됩니다. 이 메서드는 빌링 가능한 모델 인스턴스를 반환합니다.

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성(Creating Customers)

때로는 구독을 시작하지 않고도 Paddle 고객을 생성하고 싶을 수 있습니다. 이럴 때는 `createAsCustomer` 메서드를 사용할 수 있습니다.

```php
$customer = $user->createAsCustomer();
```

이 메서드는 `Laravel\Paddle\Customer` 인스턴스를 반환합니다. 고객이 Paddle에 생성된 후, 이후 언제든 구독을 시작할 수 있습니다. 추가로 [Paddle API가 지원하는 고객 생성 파라미터](https://developer.paddle.com/api-reference/customers/create-customer)를 `$options` 배열 형태로 전달해줄 수도 있습니다.

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독(Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성(Creating Subscriptions)

구독을 생성하려면, 먼저 데이터베이스에서 빌링 가능한 모델 인스턴스를 가져와야 합니다. 일반적으로 `App\Models\User` 인스턴스가 될 것입니다. 모델 인스턴스를 가져오면 `subscribe` 메서드를 사용해서 해당 모델의 결제 세션을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe` 메서드의 첫 번째 인수는 사용자가 구독할 가격(Price)입니다. 이 값은 Paddle 가격의 식별자와 일치해야 합니다. `returnTo` 메서드에는 사용자가 결제 후 리디렉션될 URL을 지정합니다. `subscribe`의 두 번째 인수로는 내부적으로 사용할 구독의 "타입"을 정합니다. 애플리케이션에 구독 플랜이 하나라면 `default`나 `primary`와 같이 지을 수 있습니다. 이 구독 타입은 내부적으로만 사용하며, 사용자에게 노출되지 않습니다. 또한, 공백이 들어가선 안 되며, 구독 생성 후에는 절대로 변경해서는 안 됩니다.

구독 과정에 대한 추가 정보를 담고 싶으면 `customData` 메서드를 통해 메타데이터 배열을 전달할 수 있습니다.

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

구독 결제 세션이 생성되면, Cashier Paddle에 포함된 `paddle-button` [Blade 컴포넌트](#overlay-checkout)에 이 세션을 전달할 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

사용자가 결제를 마치면 Paddle에서 `subscription_created` 웹훅이 전송됩니다. Cashier는 이 웹훅을 받아서 해당 고객의 구독을 자동으로 설정합니다. 웹훅이 애플리케이션에서 올바로 수신·처리될 수 있도록 [웹훅 처리 설정](#handling-paddle-webhooks)이 제대로 되었는지 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인(Checking Subscription Status)

사용자가 애플리케이션의 구독 상태인지 확인하려면 여러 편리한 메서드를 사용할 수 있습니다. 먼저, `subscribed` 메서드는 사용자가 유효한 구독 상태(체험 기간 중이어도 포함)이면 `true`를 반환합니다.

```php
if ($user->subscribed()) {
    // ...
}
```

여러 구독을 제공하는 경우라면 구독 타입을 명시하여 확인할 수 있습니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware)로 사용하기에 적합해, 사용자의 구독 상태에 따라 라우트나 컨트롤러 접근을 제어할 수 있습니다.

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
            // 이 사용자는 유료 고객이 아닙니다.
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

사용자가 아직 체험 기간(trial)인지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드를 활용해 체험 기간임을 사용자에게 경고로 안내하는 등 다양한 처리를 할 수 있습니다.

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

`subscribedToPrice` 메서드는 특정 Paddle 가격 ID에 대해 사용자가 해당 요금제에 구독 중인지 확인할 때 사용할 수 있습니다. 아래 예시에서는 사용자의 `default` 구독이 월간 요금제에 정상 구독 중인지 체크합니다.

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 사용자가 현재 활성 구독 중이며, 체험 기간이나 유예 기간(grace period)이 아닌 경우를 판단할 때 사용됩니다.

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 구독 해지 상태(Canceled Subscription Status)

사용자가 한때 활성 가입자였으나 구독을 해지했다면 `canceled` 메서드로 확인할 수 있습니다.

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

또한, 구독 해지 이후에도 "유예 기간"이 남아 있을 때를 확인할 수도 있습니다. 예를 들어 3월 5일에 구독을 취소했는데 원래 만료일이 3월 10일이라면, 3월 10일까지는 유예 기간이며, 이때도 `subscribed`는 여전히 `true`를 반환합니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체(past due) 상태

구독 결제 시 결제가 실패하면 해당 구독은 `past_due` 상태가 됩니다. 이런 경우 결제 정보가 갱신될 때까지 구독이 활성화되지 않습니다. 구독 인스턴스에서 `pastDue` 메서드를 사용해 결제가 연체 상태인지 확인할 수 있습니다.

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

구독이 `past_due` 상태라면 사용자가 [결제 정보를 업데이트](#updating-payment-information)하도록 안내해야 합니다.

만약 구독이 `past_due` 상태일 때도 여전히 유효하다고 인정하고 싶다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 `AppServiceProvider`의 `register` 메서드에서 호출하면 됩니다.

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
> 구독이 `past_due` 상태일 때는 결제 정보가 갱신되기 전까지 구독 변경이 불가능합니다. 따라서 이 상태에서는 `swap` 및 `updateQuantity` 메서드 호출 시 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 스코프(Subscription Scopes)

대부분의 구독 상태는 쿼리 스코프로도 제공되므로, 원하는 상태의 구독만 쉽게 데이터베이스에서 조회할 수 있습니다.

```php
// 모든 유효한 구독 조회...
$subscriptions = Subscription::query()->valid()->get();

// 특정 사용자의 해지된 구독 조회...
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 구독 관련 스코프 목록은 다음과 같습니다.

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
### 구독 단일 청구(Subscription Single Charges)

구독 중인 고객에게 정기 구독 이외에 한 번만 추가로 청구하고 싶을 때, `charge` 메서드에 가격 ID를 하나 또는 여러 개 전달하면 됩니다.

```php
// 가격 한 건만 청구...
$response = $user->subscription()->charge('pri_123');

// 여러 가격을 한 번에 청구...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge` 메서드는 해당 구독의 다음 청구 주기 때 실제로 결제가 발생합니다. 즉시 청구 및 청구서를 발행하고 싶다면 `chargeAndInvoice` 메서드를 사용하세요.

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 변경(Updating Payment Information)

Paddle은 구독마다 별도의 결제 수단을 저장합니다. 구독의 기본 결제 수단을 변경하려면, `redirectToUpdatePaymentMethod` 메서드로 Paddle이 제공하는 결제수단 변경 페이지로 리디렉션하세요.

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

사용자가 정보를 수정하면 Paddle에서 `subscription_updated` 웹훅을 전송하며, 애플리케이션의 데이터베이스에도 구독 정보가 갱신됩니다.

<a name="changing-plans"></a>
### 구독 플랜 변경(Changing Plans)

사용자가 구독을 시작한 뒤에 새로운 구독 플랜으로 변경하고 싶을 때는, 구독의 `swap` 메서드에 Paddle 가격 식별자를 전달하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 새로운 플랜으로 변경하고 바로 인보이스(청구서)를 발행하려면 `swapAndInvoice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 기간 비례(Prorations)

기본적으로 Paddle은 플랜을 변경(swap)할 때 금액을 기간에 맞게 비례 계산합니다. 비례 계산 없이 구독을 갱신하고 싶다면, `noProrate` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

비례 계산 없이 즉시 요금을 청구하고 싶다면, `noProrate`와 `swapAndInvoice`를 함께 사용할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

또는, 구독 변경 시 추가 결제를 원하지 않으면 `doNotBill` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle의 기간 비례(Proration) 정책에 대한 자세한 내용은 [Paddle 공식 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량 관리(Subscription Quantity)

일부 서비스는 구독 "수량"에 따라 금액이 달라집니다. 예를 들어, 프로젝트마다 월 $10을 청구하는 프로젝트 관리 앱이라면, `incrementQuantity`와 `decrementQuantity` 메서드로 구독 수량을 쉽게 늘리거나 줄일 수 있습니다.

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 구독 수량을 5개 늘리기...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 구독 수량을 5개 줄이기...
$user->subscription()->decrementQuantity(5);
```

혹은, `updateQuantity` 메서드로 특정 수량으로 바로 설정할 수도 있습니다.

```php
$user->subscription()->updateQuantity(10);
```

수량 변경 시 금액 비례 계산 없이 바로 바꾸고 싶을 때는 `noProrate`를 함께 사용할 수 있습니다.

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 상품이 포함된 구독의 수량 관리

구독이 [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)이라면, 수량을 늘리거나 줄일 상품의 가격 ID를 두 번째 인수로 전달해야 합니다.

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품이 포함된 구독(Subscriptions With Multiple Products)

[여러 상품이 포함된 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)을 사용하면 단일 구독에 여러 상품을 할당할 수 있습니다. 예를 들어, 고객 지원 헬프데스크 애플리케이션에서 기본 구독은 월 $10, 여기에 라이브 채팅 애드온을 월 $15로 추가하는 등 다양한 조합이 가능합니다.

구독 결제 세션을 생성할 때, 구독에 여러 상품을 할당하고 싶으면 `subscribe` 메서드의 첫 번째 인수로 가격 배열을 전달하세요.

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

위 예시에서는 고객의 `default` 구독에 두 가지 가격이 할당됩니다. 두 가지 가격 모두 각자 청구 주기에 맞춰 청구됩니다. 만약 각 가격에 수량을 지정하고 싶다면, 키-값 쌍이 포함된 연관 배열을 전달할 수 있습니다.

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 새로운 가격을 추가하고 싶으면 구독의 `swap` 메서드를 사용해야 합니다. 이때 현 구독의 가격·수량 정보도 함께 모두 전달해야 합니다.

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

위 예시는 새로운 가격을 추가하지만, 실제 청구는 다음 청구 주기부터 진행됩니다. 즉시 청구하려면 `swapAndInvoice`를 사용하면 됩니다.

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

특정 가격을 구독에서 제거하려면, 제거할 가격을 빼고 나머지 가격만 넘기면 됩니다.

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서는 마지막 가격을 제거할 수 없습니다. 대신 구독을 해지해야 합니다.

<a name="multiple-subscriptions"></a>
### 다중 구독(Multiple Subscriptions)

Paddle은 한 명의 고객이 동시에 여러 구독을 소유하는 것도 지원합니다. 예를 들어 헬스장에서 수영 구독과 헬스 구독을 각각 별도의 가격으로 운영할 수 있습니다. 사용자는 두 구독에 동시 가입할 수도 있고, 어느 하나만 가입할 수도 있습니다.

구독을 생성할 때는, `subscribe` 메서드의 두 번째 인수로 구독 타입을 지정하면 됩니다. 이 타입은 사용자가 구독을 시작하는 구독명, 아무 문자열이나 가능합니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

예시에서는 고객에게 월간 수영 구독을 추가했습니다. 향후 연간 구독으로 바꾸고 싶을 때는 해당 구독 타입에 맞게 가격만 바꿔주면 됩니다.

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

물론, 구독 전체를 해지할 수도 있습니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시중지(Pausing Subscriptions)

사용자의 구독을 일시중지 하려면, `pause` 메서드를 호출하면 됩니다.

```php
$user->subscription()->pause();
```

구독이 일시중지되면, Cashier가 데이터베이스의 `paused_at` 컬럼 값을 자동으로 설정합니다. 이 컬럼 값으로부터 `paused` 메서드가 언제 `true`를 반환할지 결정합니다. 예를 들어 3월 1일에 구독을 일시중지 했으나 다음 결제 주기가 3월 5일이면, 3월 5일까지는 `paused`가 계속 `false`를 반환합니다. 이것은 일반적으로 사용자가 결제한 기간이 끝날 때까지 서비스를 계속 이용할 수 있도록 하기 위함입니다.

기본적으로는 다음 결제 주기에 일시중지가 적용되어 남은 결제 기간만큼 서비스를 쓸 수 있습니다. 즉시 일시중지를 원한다면, `pauseNow` 메서드를 사용할 수 있습니다.

```php
$user->subscription()->pauseNow();
```

`pauseUntil` 메서드를 사용하면, 특정 시점까지 구독을 일시중지 할 수도 있습니다.

```php
$user->subscription()->pauseUntil(now()->addMonth());
```

혹은 `pauseNowUntil` 메서드로 즉시 일시중지 하고 지정한 시점까지 유지할 수도 있습니다.

```php
$user->subscription()->pauseNowUntil(now()->addMonth());
```

고객이 구독을 일시중지했으나 "유예 기간"에 있는지 확인하려면 `onPausedGracePeriod` 메서드를 사용하세요.

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시중지된 구독을 다시 활성화하려면 `resume` 메서드를 호출하면 됩니다.

```php
$user->subscription()->resume();
```

> [!WARNING]
> 일시중지 상태의 구독은 수정(플랜 변경, 수량 변경 등)이 불가능합니다. 구독을 변경하려면 먼저 다시 활성화(resume)해야 합니다.

<a name="canceling-subscriptions"></a>

### 구독 취소하기

구독을 취소하려면, 사용자 인스턴스의 `subscription`에 대해 `cancel` 메서드를 호출합니다.

```php
$user->subscription()->cancel();
```

구독이 취소되면, Cashier는 데이터베이스의 `ends_at` 컬럼을 자동으로 설정합니다. 이 컬럼은 `subscribed` 메서드가 언제 `false`를 반환해야 하는지를 결정하는 데 사용됩니다. 예를 들어, 고객이 3월 1일에 구독을 취소했지만 실제 구독 종료일이 3월 5일이라면, `subscribed` 메서드는 3월 5일까지 계속해서 `true`를 반환합니다. 이는 사용자가 청구 주기가 끝날 때까지 애플리케이션을 계속 사용할 수 있도록 하기 위함입니다.

사용자가 구독을 취소했지만 아직 "유예 기간(grace period)"에 있는지 확인하려면, `onGracePeriod` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

구독을 즉시 취소하고 싶다면, 구독 인스턴스에서 `cancelNow` 메서드를 호출할 수 있습니다.

```php
$user->subscription()->cancelNow();
```

유예 기간 중인 구독의 취소를 중지하고자 할 때는, `stopCancelation` 메서드를 호출합니다.

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle의 구독은 취소 후 다시 재개할 수 없습니다. 고객이 구독을 재개하고 싶다면 새로운 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간

<a name="with-payment-method-up-front"></a>
### 결제 수단을 먼저 받은 상태에서의 체험 기간

체험 기간을 제공하면서도 고객의 결제 수단 정보를 미리 받고 싶다면, Paddle 대시보드에서 고객이 가입할 가격(Price)에 대해 체험 기간을 설정해야 합니다. 그 다음, 일반적으로 체크아웃 세션을 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

애플리케이션이 `subscription_created` 이벤트를 수신하면, Cashier는 애플리케이션 데이터베이스 내 구독 레코드에 체험 기간 종료일을 설정하고, Paddle에는 해당 날짜까지 고객에게 요금을 청구하지 않도록 지시합니다.

> [!WARNING]
> 고객의 구독이 체험 종료일 전에 취소되지 않으면, 체험이 끝나는 즉시 요금이 청구됩니다. 따라서 사용자에게 체험 만료 예정일을 미리 안내해야 합니다.

사용자가 체험 기간 내에 있는지 확인하려면, 사용자 인스턴스의 `onTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->onTrial()) {
    // ...
}
```

이미 존재하는 체험 기간이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용하면 됩니다.

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 유형에 대해 사용자가 체험 상태인지 확인하고 싶다면, 해당 구독 유형을 `onTrial`이나 `hasExpiredTrial` 메서드에 전달할 수 있습니다.

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단을 미리 받지 않는 체험 기간

고객의 결제 수단 없이 체험 기간을 제공하고 싶다면, 사용자와 연결된 고객 레코드의 `trial_ends_at` 컬럼에 원하는 체험 종료일을 직접 설정하면 됩니다. 주로 회원가입 시 아래와 같이 사용합니다.

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

Cashier는 이러한 형태의 체험 기간을 "일반(generic) 체험 기간"이라고 부릅니다. 이는 실제 구독에 연결되지 않은 체험입니다. 현재 날짜가 `trial_ends_at`보다 이전이면, 사용자 인스턴스의 `onTrial` 메서드는 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // 사용자가 체험 기간 내에 있습니다...
}
```

실제 구독 생성을 진행하고 싶다면, 평소처럼 `subscribe` 메서드를 호출해서 구독을 생성하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

사용자의 체험 종료일을 가져오려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 체험 기간 중이면 Carbon 날짜 인스턴스를 반환하고, 그렇지 않으면 `null`을 반환합니다. 기본 구독 외에 특정 구독에 대해 체험 종료일을 조회하고 싶다면, 구독 유형을 파라미터로 전달할 수도 있습니다.

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

특히 사용자가 "일반(generic) 체험 기간" 동안이고, 아직 실제 구독을 생성하지 않았는지 확인하고 싶다면 `onGenericTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->onGenericTrial()) {
    // 사용자가 "일반(generic) 체험 기간" 내에 있습니다...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 기간 연장 또는 즉시 활성화

이미 활성화된 구독의 체험 기간을 연장하려면 `extendTrial` 메서드를 호출하고, 체험 기간이 종료될 시점을 지정하면 됩니다.

```php
$user->subscription()->extendTrial(now()->addDays(5));
```

또는 구독의 체험 기간을 즉시 종료하고 구독을 바로 활성화하고 싶다면, 해당 구독에 대해 `activate` 메서드를 호출합니다.

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹후크(Webhook) 처리

Paddle은 웹후크를 통해 여러 가지 이벤트를 애플리케이션에 통지할 수 있습니다. 기본적으로, Cashier 서비스 프로바이더는 Cashier의 웹후크 컨트롤러로 연결된 라우트를 등록합니다. 이 컨트롤러가 모든 웹후크 요청을 처리하게 됩니다.

이 컨트롤러는 자동으로 너무 많은 청구 실패로 인한 구독 취소, 구독 갱신, 결제 수단 변경 등과 같은 작업을 처리합니다. 그리고 필요하다면, 이 컨트롤러를 확장해 원하는 모든 Paddle 웹후크 이벤트를 직접 처리할 수도 있습니다.

애플리케이션이 Paddle 웹후크를 올바르게 처리할 수 있도록 하려면, 반드시 [Paddle 관리 패널에서 웹후크 URL을 설정](https://vendors.paddle.com/notifications-v2)해야 합니다. 기본적으로 Cashier의 웹후크 컨트롤러는 `/paddle/webhook` URL 경로에 응답합니다. Paddle 관리 패널에서 활성화해야 하는 웹후크 목록은 아래와 같습니다.

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Cashier에서 제공하는 [웹후크 서명 검증](/docs/12.x/cashier-paddle#verifying-webhook-signatures) 미들웨어로 수신 요청을 반드시 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹후크와 CSRF 보호

Paddle 웹후크가 라라벨의 [CSRF 보호](/docs/12.x/csrf)를 우회하도록 하려면, Paddle 웹후크에서 CSRF 토큰 검증이 발생하지 않도록 `bootstrap/app.php` 파일에서 `paddle/*`을 CSRF 보호에서 제외해야 합니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 로컬 개발 환경에서의 웹후크 처리

Paddle이 로컬 개발 환경의 애플리케이션에 웹후크를 보낼 수 있도록 하려면, [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 공유 서비스를 이용해 애플리케이션을 외부에 노출해야 합니다. [Laravel Sail](/docs/12.x/sail)로 로컬 개발을 하고 있다면 Sail의 [사이트 공유 명령어](/docs/12.x/sail#sharing-your-site)를 사용할 수도 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹후크 이벤트 핸들러 정의하기

Cashier는 결제 실패로 인한 구독 취소와 많은 일반적인 Paddle 웹후크를 자동으로 처리합니다. 하지만 추가로 필요한 웹후크 이벤트가 있다면, Cashier에서 발생시키는 다음의 이벤트들을 리스닝하여 직접 처리할 수 있습니다.

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹후크의 전체 페이로드를 포함합니다. 예를 들어 `transaction.billed` 웹후크를 처리하려면 [리스너](/docs/12.x/events#defining-listeners)를 등록하여 아래와 같이 구현할 수 있습니다.

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Paddle 웹후크를 처리합니다.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // 들어온 이벤트를 처리...
        }
    }
}
```

Cashier는 수신된 웹후크 유형에 맞는 별도의 이벤트도 발생시킵니다. 이 이벤트들은 Paddle에서 받은 전체 페이로드와 함께, 웹후크 처리에 사용된 관련 모델(빌러블 모델, 구독, 영수증 등) 정보도 함께 포함되어 있습니다.

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

기본적으로 내장된 웹후크 라우트를 재정의하려면, 애플리케이션의 `.env` 파일에서 `CASHIER_WEBHOOK` 환경 변수를 정의하면 됩니다. 이 값은 웹후크 라우트의 전체 URL이어야 하며, Paddle 관리 패널에 설정된 URL과 일치해야 합니다.

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹후크 서명 검증

웹후크의 보안을 위해 [Paddle의 웹후크 서명](https://developer.paddle.com/webhooks/signature-verification)을 사용할 수 있습니다. Cashier는 편의상 Paddle에서 들어오는 웹후크 요청의 유효성을 자동으로 검증하는 미들웨어를 내장하고 있습니다.

웹후크 검증을 활성화하려면, 애플리케이션의 `.env` 파일에 `PADDLE_WEBHOOK_SECRET` 환경 변수가 정의되어 있어야 합니다. 이 값은 Paddle 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 결제

<a name="charging-for-products"></a>
### 상품에 대한 결제

고객이 상품을 구매할 수 있게 하려면, 빌러블 모델 인스턴스에서 `checkout` 메서드를 사용해 결제 세션을 생성할 수 있습니다. `checkout` 메서드는 한 개 또는 여러 개의 가격(Price) ID를 받을 수 있습니다. 필요하다면, 구입할 상품의 수량을 명시하는 연관 배열로도 전달할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

체크아웃 세션을 생성한 후, Cashier가 제공하는 `paddle-button` [Blade 컴포넌트](#overlay-checkout)를 사용하여 사용자가 Paddle 결제 위젯에서 직접 결제를 완료할 수 있도록 할 수 있습니다.

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

체크아웃 세션에는 `customData` 메서드가 있어, 원하는 커스텀 데이터를 트랜잭션 생성 시 함께 전송할 수 있습니다. 커스텀 데이터 옵션에 대한 자세한 내용은 [Paddle 공식 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요.

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 트랜잭션 환불

트랜잭션을 환불하면 고객이 구매에 사용한 결제 수단으로 해당 금액이 반환됩니다. Paddle 구매를 환불하려면, `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용합니다. 이 메서드는 환불 사유(첫 번째 인수)와 환불할 가격 ID, 환불 금액(연관 배열 형태)을 받을 수 있습니다. 특정 빌러블 모델에 대한 트랜잭션은 `transactions` 메서드로 조회할 수 있습니다.

예를 들어, 가격 ID가 `pri_123`과 `pri_456`인 트랜잭션을 환불하는 상황을 가정해보겠습니다. `pri_123`은 전액 환불하고, `pri_456`은 2달러만 부분 환불하려고 합니다.

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 이 가격은 전액 환불...
    'pri_456' => 200, // 이 가격은 2달러만 부분 환불...
]);
```

위 예시는 트랜잭션 내 특정 라인 아이템만 환불합니다. 트랜잭션 전체를 환불하려면, 환불 사유만 전달하면 됩니다.

```php
$response = $transaction->refund('Accidental charge');
```

환불 처리에 대해 더 자세히 알고 싶다면 [Paddle의 환불 관련 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> Paddle에서 반드시 환불 승인을 받은 후에만 환불이 완전히 처리됩니다.

<a name="crediting-transactions"></a>
### 트랜잭션에 크레딧 지급

환불뿐만 아니라 트랜잭션에 크레딧(포인트)을 지급할 수도 있습니다. 크레딧 지급은 해당 금액을 고객의 잔액으로 돌려주기 때문에, 이후 다른 결제에 사용할 수 있습니다. 단, 크레딧 지급은 수동 청구된 트랜잭션에만 적용할 수 있으며, 자동 청구(예: 구독) 트랜잭션은 Paddle이 자동으로 크레딧을 처리합니다.

```php
$transaction = $user->transactions()->first();

// 특정 라인 아이템에 전액 크레딧 지급...
$response = $transaction->credit('Compensation', 'pri_123');
```

더 많은 정보는 [Paddle 크레딧 관련 공식 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 크레딧은 오직 수동 결제 트랜잭션에만 적용할 수 있습니다. 자동 결제 트랜잭션은 Paddle이 자체적으로 크레딧을 처리합니다.

<a name="transactions"></a>
## 트랜잭션

빌러블 모델의 `transactions` 속성을 통해 손쉽게 트랜잭션 목록(배열)을 조회할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

트랜잭션은 여러분의 상품 및 구매에 대한 결제 내역을 나타내며, 인보이스가 함께 제공됩니다. 오직 "완료된 트랜잭션"만 애플리케이션 데이터베이스에 저장됩니다.

고객의 트랜잭션 목록을 보여줄 때, 각 트랜잭션 인스턴스의 메서드를 이용해 결제 정보 등을 표시할 수 있습니다. 예를 들어, 각 트랜잭션을 테이블 형식으로 나열하고, 사용자가 인보이스 파일을 쉽게 다운로드받도록 구현할 수 있습니다.

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

`download-invoice` 라우트는 다음과 같이 정의할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정된 결제 정보 조회

`lastPayment`와 `nextPayment` 메서드를 사용하면 반복 구독에 대한 고객의 이전 결제 내역이나 다가오는 결제 내역을 조회하거나 표시할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

이 두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 다만, 거래가 아직 웹후크로 동기화되지 않았다면 `lastPayment`는 `null`을 반환하고, 결제 주기가 종료된 경우(예: 구독 취소 이후)에는 `nextPayment`가 `null`을 반환합니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트

청구 관련 플로우를 개발할 때는 직접 결제 흐름을 테스트하여 정상적으로 동작하는지 꼼꼼하게 확인해야 합니다.

자동화된 테스트(예: CI 환경 등)에서는 [라라벨의 HTTP 클라이언트](/docs/12.x/http-client#testing)를 사용하여 Paddle로 보내는 HTTP 요청을 페이크 처리할 수 있습니다. 이 방법은 실제로 Paddle의 응답을 테스트하진 않지만, Paddle API와 통신하지 않아도 애플리케이션의 흐름을 검증하는 데 유용합니다.