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
    - [고객 기본 설정](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 요금 청구](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [다중 제품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시 중지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 방법 사전 등록](#with-payment-method-up-front)
    - [결제 방법 미등록](#without-payment-method-up-front)
    - [체험 기간 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 요금 청구](#single-charges)
    - [제품 요금 청구](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧](#crediting-transactions)
- [거래](#transactions)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

> [!WARNING]  
> 이 문서는 Cashier Paddle 2.x의 Paddle Billing 통합 문서입니다. 여전히 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 직관적이고 유연한 인터페이스를 제공합니다. 구독 결제 관련 반복적인 코드를 대부분 대신 처리해 주어 부담을 줄여줍니다. 기본적인 구독 관리 외에도 구독 플랜 변경, 구독 "수량" 관리, 구독 일시 중지, 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 본격적으로 사용하기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)를 함께 확인하는 것을 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용해 Paddle용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier-paddle
```

그다음, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션 파일을 배포합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이후 애플리케이션의 데이터베이스 마이그레이션을 실행하면, Cashier가 고객 정보 저장용 `customers` 테이블과 구독 정보 저장용 `subscriptions`, `subscription_items` 테이블, Paddle 결제 내역 저장용 `transactions` 테이블을 생성합니다:

```shell
php artisan migrate
```

> [!WARNING]  
> Cashier가 모든 Paddle 이벤트를 정상 처리하도록 하려면 [웹훅 처리 설정](#handling-paddle-webhooks)을 반드시 해주세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 또는 스테이징 환경에서 개발할 때는 [Paddle 샌드박스 계정](https://sandbox-login.paddle.com/signup)을 등록해 사용하는 것이 좋습니다. 이 계정을 통해 실제 결제를 하지 않고도 테스트용 환경에서 앱을 개발 및 테스트할 수 있습니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card)를 사용해 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

샌드박스 환경을 사용하기 위해서는 애플리케이션 `.env` 파일에 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

개발이 완료되면 [Paddle 판매자 계정](https://paddle.com)을 신청할 수 있습니다. 운영 환경에 배포하기 전 Paddle에서 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 가능한 모델

Cashier를 사용하려면, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 업데이트 등 일반적인 청구 작업에 필요한 여러 메서드를 제공합니다:

```
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 다른 청구 대상 모델에도 트레잇을 적용할 수 있습니다:

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

다음으로 애플리케이션 `.env` 파일에 Paddle API 키들을 설정하세요. Paddle 콘트롤 패널에서 키를 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 변수는 [샌드박스 환경](#paddle-sandbox) 사용 시 `true`로, 라이브 운영 환경에서는 `false`로 설정합니다.

`PADDLE_RETAIN_KEY`는 Retain 기능을 사용할 때만 설정하세요. 자세한 내용은 [Retain 관련 문서](https://developer.paddle.com/paddlejs/retain)를 참고하세요.

<a name="paddle-js"></a>
### Paddle JS

Paddle는 자체 JavaScript 라이브러리를 사용해 결제 위젯을 초기화합니다. 애플리케이션 레이아웃의 `</head>` 닫는 태그 바로 전에 `@paddleJS` Blade 디렉티브를 삽입해 라이브러리를 불러오세요:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

인보이스에 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 통해 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 외 다른 로케일을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Cashier가 내부적으로 사용하는 모델들을 확장하고 싶다면, 자신의 모델을 정의해 Cashier 모델을 상속받으세요:

```
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

그 후, `Laravel\Paddle\Cashier` 클래스에 커스텀 모델을 지정하면 됩니다. 일반적으로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

```
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * 애플리케이션 서비스 부트스트랩
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
### 제품 판매하기

> [!NOTE]  
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격이 있는 제품을 정의해야 합니다. 또한 [웹훅 처리 설정](#handling-paddle-webhooks)도 완료해야 합니다.

애플리케이션에서 제품 및 구독 결제를 제공하는 일은 어렵게 느껴질 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://www.paddle.com/billing/checkout)를 이용하면 모던하고 견고한 결제 통합 기능을 쉽게 구축할 수 있습니다.

비반복(일회성) 상품에 대해 고객에게 요금을 청구하려면, Cashier의 `checkout` 메서드를 사용해 Paddle의 Checkout Overlay를 표시합니다. 고객은 결제 정보를 입력하고 구매를 확인합니다. 결제가 완료되면 고객은 애플리케이션 내 지정한 성공 페이지로 리디렉션됩니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제에서 `checkout` 메서드는 해당 `price identifier`에 대응하는 Paddle Checkout Overlay 세션을 생성합니다. Paddle에서 가격(Price)은 특정 제품에 대해 정의된 가격을 의미합니다.

필요시, `checkout` 메서드는 Paddle 고객을 자동으로 생성하고 관련 고객 정보를 애플리케이션의 사용자와 연결합니다. 결제 완료 후, 고객은 지정한 성공 페이지로 이동됩니다.

`buy` 뷰에서는 Checkout Overlay를 띄우는 버튼을 포함합니다. `paddle-button` Blade 컴포넌트가 Cashier Paddle에 기본 제공되지만, 필요하면 [직접 오버레이 결제를 렌더링하는 방법](#manually-rendering-an-overlay-checkout)을 사용할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타 데이터 전달하기

제품 판매 시, 애플리케이션의 `Cart` 또는 `Order` 모델 등으로 주문과 구매 내역을 관리하는 경우가 많습니다. 고객이 Paddle Checkout Overlay에서 구매를 완료하면, 애플리케이션에서 해당 주문과 구매 내역을 연동하려면 주문 ID 등의 커스텀 데이터를 전달해야 할 수 있습니다.

이를 위해 `checkout` 메서드에 커스텀 데이터를 배열 형태로 전달할 수 있습니다. 예를 들어, 사용자가 체크아웃을 시작할 때 애플리케이션에서 미완료 상태인 `Order`를 생성하는 경우를 생각해봅시다. 여기서 `Cart`, `Order` 모델은 예시일 뿐 Cashier에서 제공하는 것이 아니며, 애플리케이션에 맞게 구현해야 합니다:

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

사용자가 체크아웃할 때, 관련 Paddle 가격 식별자를 모두 `checkout` 메서드에 전달합니다. 주문 ID도 `customData` 메서드를 통해 전달해 Paddle Checkout Overlay에 포함시킵니다.

구매가 완료되면, 웹훅과 이벤트를 통해 애플리케이션에서 주문 상태를 갱신할 수 있습니다. 예를 들어, `TransactionCompleted` 이벤트에 대한 리스너를 작성할 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 이벤트 리스너를 등록합니다:

```
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

예시 `CompleteOrder` 리스너는 다음과 같을 수 있습니다:

```
namespace App\Listeners;

use App\Models\Order;
use Laravel\Cashier\Cashier;
use Laravel\Cashier\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * Cashier 웹훅 이벤트 처리
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

더 자세한 내용은 Paddle 문서의 [`transaction.completed` 이벤트 데이터](https://developer.paddle.com/webhooks/transactions/transaction-completed)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매하기

> [!NOTE]  
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격이 있는 제품을 정의해야 합니다. 또한 [웹훅 처리 설정](#handling-paddle-webhooks)도 완료해야 합니다.

제품과 구독 결제를 애플리케이션에서 제공하는 것이 처음에는 어려워 보일 수 있지만, Cashier와 [Paddle Checkout Overlay](https://www.paddle.com/billing/checkout)를 사용하면 강력한 결제 통합 기능을 쉽게 구축할 수 있습니다.

간단한 구독 시나리오를 가정해보겠습니다. 예를 들어, 기본 월간(`price_basic_monthly`)과 연간(`price_basic_yearly`) 플랜이 있으며 이 둘은 "Basic" 제품 (`pro_basic`) 아래 묶여 있습니다. 별도의 Expert 플랜(`pro_expert`)도 있다고 가정합니다.

고객이 "구독하기" 버튼을 클릭하면, 선택한 플랜에 대한 Paddle Checkout Overlay가 표시됩니다. 이를 위해 `checkout` 메서드로 결제 세션을 생성합니다:

```
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에 Checkout Overlay를 띄우는 버튼을 포함합니다. `paddle-button` Blade 컴포넌트가 Cashier Paddle에 기본 제공되지만, 직접 [오버레이 결제 렌더링](#manually-rendering-an-overlay-checkout)도 가능합니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

구독 버튼 클릭 시 고객은 결제 정보를 입력하고 구독을 시작할 수 있습니다. 일부 결제 방식은 처리에 시간이 걸릴 수 있으므로, 구독이 실제 시작되었는지 알려면 반드시 [Cashier 웹훅 처리](#handling-paddle-webhooks)를 설정해야 합니다.

이제 고객이 구독을 시작할 수 있으니, 애플리케이션에서 구독한 사용자만 접근할 수 있는 영역을 제한해야 합니다. 사용자의 구독 상태는 Cashier가 제공하는 `Billable` 트레이트의 `subscribed` 메서드로 간단히 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 제품 또는 가격으로 구독했는지도 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 제품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 플랜을 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 상태 미들웨어 만들기

편의상, 요청자가 구독 사용자임을 확인하는 [미들웨어](/docs/10.x/middleware)를 생성할 수 있습니다. 미들웨어를 경로에 적용하면, 구독하지 않은 사용자는 접근이 제한됩니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // 사용자에게 청구 페이지로 리디렉션 후 구독 요청
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어 생성 후, 경로에 할당하면 됩니다:

```
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 구독 플랜 관리하기 허용하기

고객은 월간 플랜에서 연간 플랜으로 변경하는 등 구독 플랜을 변경할 수 있어야 합니다. 아래 예시는 플랜 변경 요청을 처리하는 라우트입니다:

```
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 예: "price_basic_yearly"

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

또한 구독 취소도 허용해야 합니다. 취소 요청은 다음과 같이 라우트를 정의할 수 있습니다:

```
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이후 구독은 청구 기간이 끝날 때 자동으로 종료됩니다.

> [!NOTE]  
> Cashier 웹훅 처리가 설정되어 있으면, 예를 들어 Paddle 콘트롤 패널에서 구독을 취소해도 Paddle에서 웹훅이 발생해 Cashier가 자동으로 애플리케이션 데이터베이스에 변경 내용을 반영합니다.

<a name="checkout-sessions"></a>
## 결제 세션

대부분의 고객 결제 처리는 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 결제](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)를 통해 수행됩니다.

결제를 진행하기 전에, Paddle 콘솔에서 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 설정해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 결제

Checkout Overlay 위젯을 표시하기 전에, 반드시 Cashier로부터 결제 세션을 생성해야 합니다. 세션 정보는 위젯에 청구할 결제 내역을 알리는 역할을 합니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier는 `paddle-button` [Blade 컴포넌트](/docs/10.x/blade#components)를 포함합니다. 생성한 세션을 컴포넌트에 prop으로 전달하면, 버튼을 클릭할 때 Paddle 결제 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle 기본 스타일로 위젯이 표시됩니다. `data-theme='light'` 등의 Paddle 지원 속성을 추가해 스타일을 조절할 수 있습니다:

```html
<x-paddle-button :url="$payLink" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기 동작합니다. 구독 생성 후 Paddle에서 앱으로 웹훅을 전송해 데이터베이스 상태를 갱신하므로, 반드시 [웹훅 설정](#handling-paddle-webhooks)을 올바르게 구성해야 합니다.

> [!WARNING]  
> 구독 상태 변경 후 웹훅 전송까지는 보통 지연이 거의 없지만, 결제 완료 직후 구독 정보가 즉시 반영되지 않을 수 있음을 앱에서 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 결제 수동 렌더링

Laravel의 Blade 컴포넌트를 사용하지 않고 직접 오버레이 체크아웃을 구현할 수도 있습니다. 먼저 위 예시처럼 결제 세션을 생성합니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그다음 Paddle.js를 사용해 체크아웃 위젯을 초기화할 수 있습니다. 아래 예시는 `paddle_button` 클래스를 가진 링크를 만들어 버튼 클릭 시 오버레이 체크아웃이 표시되게 합니다:

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
### 인라인 결제

Paddle 오버레이 위젯 대신 결제를 애플리케이션 내부에 직접 내장된 형태로 표시하고 싶다면, 인라인 결제 옵션을 활용할 수 있습니다. 이 방법은 HTML 필드를 조정할 수는 없지만, 애플리케이션 내에서 결제 UI를 임베딩할 수 있습니다.

Cashier는 인라인 결제를 쉽게 시작할 수 있도록 `paddle-checkout` Blade 컴포넌트를 제공합니다. 먼저 결제 세션을 준비합니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

뷰에서는 다음과 같이 세션을 컴포넌트의 `checkout` 속성으로 전달합니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

컴포넌트 높이를 조절하려면 `height` 속성을 지정하세요:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

자세한 커스터마이징은 Paddle의 [인라인 결제 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [설정 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 결제 수동 렌더링

Blade 컴포넌트를 사용하지 않고 직접 인라인 결제를 구현할 수도 있습니다. 위 예시처럼 결제 세션을 생성한 뒤 Paddle.js를 사용해 초기화합니다. 아래 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용했지만, 원하는 프론트엔드 스택으로 변경 가능합니다:

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
### 게스트 결제

계정 없이 구매할 필요가 있는 경우, `guest` 메서드를 사용해 결제 세션을 생성할 수 있습니다:

```
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest('pri_34567')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이후 [Paddle 버튼](#overlay-checkout) 또는 [인라인 결제](#inline-checkout) 컴포넌트에 세션을 전달해 사용합니다.

<a name="price-previews"></a>
## 가격 미리보기

Paddle에서는 국가별로 통화에 맞춰 가격을 다르게 설정할 수 있습니다. Cashier Paddle은 `previewPrices` 메서드를 통해 가격 ID 목록에 대한 모든 현지화된 가격을 조회할 수 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

가격 조회 시, 요청 IP로부터 국가가 결정되지만, 명시적으로 국가를 지정하여 조회할 수도 있습니다:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::productPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회한 가격 정보를 자유롭게 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계와 세금만 따로 보여주는 것도 가능합니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product_title }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} 세금)</li>
    @endforeach
</ul>
```

더 자세한 내용은 Paddle API 문서의 [가격 미리보기](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참조하세요.

<a name="customer-price-previews"></a>
### 고객 가격 미리보기

이미 고객으로 등록된 사용자의 현지화된 가격을 표시하려면, 고객 인스턴스에서 직접 가격을 조회할 수 있습니다:

```
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Cashier는 내부적으로 Paddle 고객 ID를 이용해 해당 고객의 통화 가격을 조회합니다. 예를 들어, 미국 사용자는 달러 가격을, 벨기에 사용자는 유로 가격을 보게 됩니다. 매칭되는 통화가 없으면 제품 기본 통화가 사용됩니다. Paddle 콘솔에서 제품과 구독 플랜의 모든 가격을 관리할 수 있습니다.

<a name="price-discounts"></a>
### 할인

할인 적용 가격을 표시하려면, `previewPrices` 메서드 호출 시 `discount_id` 옵션에 할인 ID를 전달하세요:

```
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격을 출력합니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

<a name="customers"></a>
## 고객

<a name="customer-defaults"></a>
### 고객 기본 설정

Cashier는 결제 세션 생성 시 고객 이메일과 이름을 미리 채우기 위한 기본값을 설정할 수 있게 합니다. 청구 가능한 모델에서 다음 메서드를 오버라이드해 기본 값을 정의하세요:

```
/**
 * Paddle에 연결할 고객 이름 반환
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Paddle에 연결할 고객 이메일 반환
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이 기본값은 Cashier 내의 모든 결제 세션 생성 작업에 적용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

Paddle 고객 ID로 고객 모델을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 청구 가능한 모델 인스턴스가 반환됩니다:

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔 구독을 시작하지 않고 Paddle 고객만 생성하고 싶을 때가 있습니다. `createAsCustomer` 메서드를 사용하면 됩니다:

```
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스가 반환됩니다. 고객 생성 후 나중에 구독을 시작할 수 있습니다. Paddle API가 지원하는 추가 고객 생성 파라미터는 `$options` 배열로 전달할 수 있습니다:

```
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면, 먼저 데이터베이스에서 청구 가능한 사용자 모델(예: `App\Models\User`) 인스턴스를 조회합니다. 그 후 `subscribe` 메서드를 사용해 결제 세션을 생성할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 12345, 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

첫 번째 인수는 사용자가 구독할 특정 가격(Price ID)입니다. 이는 Paddle 내 가격 식별자와 일치해야 합니다. `returnTo` 메서드는 구독 완료 후 리디렉션할 URL을 받습니다.

두 번째 인수는 구독 타입이며, 여러 구독이 없는 경우 보통 `default`나 `primary`로 지정합니다. 이 값은 애플리케이션 내부용이며 사용자가 볼 필요 없고 생성 후 변경하면 안 됩니다.

`customData` 메서드로 구독 관련 커스텀 메타 데이터를 넘길 수도 있습니다:

```
$checkout = $request->user()->subscribe($premium = 12345, 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

생성한 구독 결제 세션은 Cashier Paddle이 제공하는 `paddle-button` Blade 컴포넌트에 전달해 사용할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

사용자가 체크아웃을 완료하면 Paddle에서 `subscription_created` 웹훅이 전송되고 Cashier가 구독 정보를 설정합니다. 모든 웹훅이 제대로 처리되도록 [웹훅 설정](#handling-paddle-webhooks)을 꼭 완료하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 구독 중인지 여러 메서드로 간편히 확인할 수 있습니다. 기본적으로 `subscribed` 메서드는 유효한 구독(체험 기간 포함)이 있을 경우 `true`를 반환합니다:

```
if ($user->subscribed()) {
    // ...
}
```

복수 구독을 제공하면, 특정 구독 명칭을 인자로 전달할 수 있습니다:

```
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/10.x/middleware)로 사용해 구독 사용자만 접근 허용하는 필터를 만들 때도 유용합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed()) {
            // 구독하지 않은 사용자…
            return redirect('billing');
        }

        return $next($request);
    }
}
```

체험 기간 중인지 확인하려면 `onTrial` 메서드를 사용하세요. 사용자에게 체험 기간임을 알려주는 메시지를 보여줄 때 유용합니다:

```
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 Paddle 가격 ID의 구독 여부는 `subscribedToPrice` 메서드를 써서 확인할 수 있습니다:

```
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

구독이 활성이며 체험 기간, 유예 기간이 아닌 경우는 `recurring` 메서드로 확인합니다:

```
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

한때 구독자였으나 현재 취소 상태인 경우는 `canceled` 메서드로 확인할 수 있습니다:

```
if ($user->subscription()->canceled()) {
    // ...
}
```

취소했지만 청구 기간 종료 전 유예 기간인 경우는 `onGracePeriod` 메서드가 `true`를 반환합니다. 예를 들어 3월 5일 취소했지만 종료일은 3월 10일인 경우, 3월 10일까지는 `subscribed`도 여전히 `true`입니다:

```
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체 상태

결제 실패 등으로 구독 상태가 `past_due`가 되면, 고객이 결제 정보를 업데이트하기 전까지 구독이 비활성화됩니다. `pastDue` 메서드로 연체 상태를 확인할 수 있습니다:

```
if ($user->subscription()->pastDue()) {
    // ...
}
```

연체 상태인 경우 [결제 정보 업데이트](#updating-payment-information)를 안내해야 합니다.

연체 상태 구독을 계속 활성화 상태로 유지하려면 `keepPastDueSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register` 메서드에서 호출하세요:

```
use Laravel\Paddle\Cashier;

/**
 * 애플리케이션 서비스 등록
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]  
> 연체 상태인 구독은 결제 정보 업데이트 전까지 변경할 수 없습니다. 따라서 `swap` 및 `updateQuantity` 메서드를 호출하면 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

구독 상태별 쿼리 스코프가 제공되어, 원하는 상태의 구독을 쉽게 조회할 수 있습니다:

```
// 모든 유효한 구독 조회
$subscriptions = Subscription::query()->valid()->get();

// 사용자의 취소된 구독 조회
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
### 구독 단일 요금 청구

구독자에게 구독료 외 일회성 요금을 청구할 수 있습니다. `charge` 메서드 인자로 하나 이상의 가격 ID를 전달하세요:

```
// 단일 가격 청구
$response = $user->subscription()->charge('pri_123');

// 여러 가격 동시 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge`는 실제 결제를 즉시 처리하지 않고 다음 결제 주기에 청구합니다. 즉시 청구하려면 `chargeAndInvoice`를 사용하세요:

```
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별 결제 수단을 저장합니다. 기본 결제 수단을 변경하려면 구독 모델의 `redirectToUpdatePaymentMethod` 메서드를 호출해 Paddle 결제 수단 변경 페이지로 리디렉션하세요:

```
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

사용자가 변경을 완료하면 Paddle에서 `subscription_updated` 웹훅이 전송되고 앱 데이터베이스가 갱신됩니다.

<a name="changing-plans"></a>
### 플랜 변경

사용자가 구독 플랜을 바꾸고 싶을 때는 Paddle 가격 식별자를 `swap` 메서드에 전달해 구독을 변경할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 청구까지 하려면 `swapAndInvoice`를 사용하세요:

```
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 비례 요금(proration)

기본적으로 Paddle은 플랜 변경 시 요금을 비례 계산합니다. 비례요금 없이 교체하려면 `noProrate`를 사용하세요:

```
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

요금 비례 계산 없이 즉시 청구하려면 `noProrate`와 `swapAndInvoice`를 함께 사용합니다:

```
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

청구하지 않고 플랜만 변경하려면 `doNotBill` 메서드를 활용하세요:

```
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

더 자세한 내용은 Paddle의 [비례 요금 정책 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량

종종 구독에 수량이 영향을 미칠 수 있습니다. 예를 들어 프로젝트 관리 앱이 프로젝트당 월 $10씩 부과한다면, `incrementQuantity`, `decrementQuantity` 메서드를 사용해 수량을 조정할 수 있습니다:

```
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 현재 수량에 5개 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 현재 수량에서 5개 감소
$user->subscription()->decrementQuantity(5);
```

특정 수량을 바로 설정하려면 `updateQuantity`를 사용하세요:

```
$user->subscription()->updateQuantity(10);
```

수량 변경 시 비례 요금을 적용하지 않으려면 `noProrate`를 호출하세요:

```
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 제품 구독의 수량 관리

다중 제품 구독일 경우, 증가/감소 메서드의 두 번째 인자로 수량을 조절할 가격 ID를 전달해야 합니다:

```
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 제품 구독

[Paddle 다중 제품 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)을 사용하면 하나의 구독에 여러 제품의 가격을 붙일 수 있습니다. 예를 들어 기본 구독 월 $10에 라이브 챗 애드온 $15를 추가하는 구조입니다.

다중 제품을 구독에 포함시키려면 `subscribe` 메서드에 가격 ID 배열을 전달하세요:

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

수량을 명시하려면 연관 배열로 전달합니다:

```
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 가격을 추가하려면 `swap` 메서드 호출 시 기존 가격과 수량도 전달해야 합니다:

```
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

위 예는 새 가격을 추가하지만 다음 결제 기간까지 추가 요금 청구는 발생하지 않습니다. 즉시 청구하려면 `swapAndInvoice`를 사용하세요:

```
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

가격 제거는 `swap`에서 제거할 가격을 빼고 호출하면 됩니다:

```
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]  
> 구독의 마지막 가격을 제거할 수는 없습니다. 대신 구독을 취소하세요.

<a name="multiple-subscriptions"></a>
### 다중 구독

Paddle은 고객이 여러 구독을 동시에 보유하는 것도 지원합니다. 예를 들어 수영 구독과 웨이트 트레이닝 구독을 각각 운영할 수 있습니다.

애플리케이션에서 구독을 생성할 때는 `subscribe` 메서드 두 번째 인수에 구독의 타입 문자열을 전달하세요:

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

이후 구독 변경 시 해당 타입을 지정해 `swap`을 호출할 수 있습니다:

```
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

물론 구독 전체를 취소할 수도 있습니다:

```
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시 중지

구독을 일시 중지하려면 `pause` 메서드를 호출하세요:

```
$user->subscription()->pause();
```

일시 중지하면 `paused_at` 컬럼이 설정되어, 구독이 실제 중지된 시점부터 `paused` 메서드가 `true`를 반환합니다. 기본값으로는 다음 결제 주기부터 중지되며, 고객이 납부한 기간은 계속 이용 가능합니다.

즉시 중지하고 싶다면 `pauseNow` 메서드를 사용하세요:

```
$user->subscription()->pauseNow();
```

특정 기간까지 일시 중지하려면 `pauseUntil` 메서드를 붙입니다:

```
$user->subscription()->pauseUntil(now()->addMonth());
```

즉시 일시 중지 + 특정 기간까지는 `pauseNowUntil`을 사용하세요:

```
$user->subscription()->pauseNowUntil(now()->addMonth());
```

일시 중지 상태에서 유예 기간인지 확인하려면 `onPausedGracePeriod` 메서드를 사용합니다:

```
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

중지된 구독을 재개하려면 `resume` 메서드를 호출하세요:

```
$user->subscription()->resume();
```

> [!WARNING]  
> 일시 중지 상태에서는 구독을 변경할 수 없습니다. 플랜 교체나 수량 변경 전에 반드시 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독 취소는 `cancel` 메서드 호출로 수행합니다:

```
$user->subscription()->cancel();
```

취소하면 `ends_at` 컬럼이 설정되어, 취소 시점부터 청구 종료일까지 구독은 유효하지만 종료일 이후부터 `subscribed`가 `false`를 반환합니다.

취소 후 유예 기간에 있는지 확인하려면 `onGracePeriod` 메서드를 사용하세요:

```
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow` 메서드를 호출하세요:

```
$user->subscription()->cancelNow();
```

취소 예정 상태를 취소하려면 `stopCancelation` 메서드를 사용합니다:

```
$user->subscription()->stopCancelation();
```

> [!WARNING]  
> Paddle 구독은 취소 후 재개가 불가능합니다. 재개하려면 새 구독을 만들어야 합니다.

<a name="subscription-trials"></a>
## 구독 체험 기간

<a name="with-payment-method-up-front"></a>
### 결제 방법 사전 등록

결제 정보를 먼저 받고 체험 기간을 제공하려면, Paddle 대시보드에서 가격에 체험 기간을 설정한 후 평소처럼 구독 결제 세션을 만드세요:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe('pri_monthly')
                ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트를 받으면, Cashier가 애플리케이션 DB에 체험 종료 날짜를 저장하고, Paddle이 그때까지 결제를 시작하지 않도록 처리합니다.

> [!WARNING]  
> 체험 기간이 끝날 때까지 취소하지 않으면, 자동으로 결제가 시작되니 사용자에게 체험 종료일을 안내하세요.

사용자가 체험 기간 중인지 확인하려면 `onTrial` 메서드를 구독 또는 사용자 인스턴스에서 호출하면 됩니다:

```
if ($user->onTrial()) {
    // ...
}

if ($user->subscription()->onTrial()) {
    // ...
}
```

체험 만료 여부는 `hasExpiredTrial` 메서드로 확인합니다:

```
if ($user->hasExpiredTrial()) {
    // ...
}

if ($user->subscription()->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입을 체험 중인지 확인하려면, 인수로 타입 문자열을 전달하세요:

```
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 방법 미등록

결제 정보를 받지 않고 체험 기간만 제공하려면, 사용자가 생성될 때 고객에 해당하는 Paddle 레코드에 `trial_ends_at` 컬럼을 설정하세요:

```
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

Cashier는 이를 "generic trial"(일반 체험)으로 부르며, 사용자가 실제 구독을 생성하지 않은 상태의 체험입니다. 이 기간 동안 `User` 인스턴스의 `onTrial` 메서드는 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 체험 기간 중
}
```

이후 구독을 생성할 때는 평소처럼 `subscribe` 메서드를 사용합니다:

```
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $user->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

체험 종료일은 `trialEndsAt` 메서드로 조회할 수 있습니다. 구독 타입 인수를 지정할 수 있으며, 체험 중이 아니면 `null`을 반환합니다:

```
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

특정 사용자가 일반 체험 중인지 확인하려면 `onGenericTrial` 메서드를 사용하세요:

```
if ($user->onGenericTrial()) {
    // 일반 체험 기간 중...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 기간 연장 또는 활성화

기존 구독 체험 기간을 연장하려면 `extendTrial` 메서드를 다음과 같이 호출하세요:

```
$user->subsription()->extendTrial(now()->addDays(5));
```

체험 기간을 즉시 끝내려면 구독의 `activate` 메서드를 호출하면 됩니다:

```
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리

Paddle은 각종 이벤트를 웹훅으로 앱에 알릴 수 있습니다. 기본적으로 Cashier 서비스 프로바이더가 웹훅 요청을 처리하는 라우트와 컨트롤러를 등록해 자동 처리합니다.

이 컨트롤러는 결제 실패 시 구독 취소, 구독 정보 업데이트, 결제 수단 변경 등 Paddle 웹훅을 기본 처리합니다. 필요에 따라 컨트롤러를 확장해 추가 이벤트를 처리할 수도 있습니다.

웹훅 처리를 위해 Paddle 콘트롤 패널에서 웹훅 URL을 설정해야 합니다. 기본 Cashier 웹훅 URL은 `/paddle/webhook`입니다. Paddle에서 반드시 활성화해야 할 웹훅 목록:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]  
> Cashier가 제공하는 [웹훅 서명 검증](/docs/10.x/cashier-paddle#verifying-webhook-signatures) 미들웨어로 요청을 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅은 Laravel의 [CSRF 보호](/docs/10.x/csrf)를 우회해야 하므로, `App\Http\Middleware\VerifyCsrfToken`의 `$except` 배열에 URI를 추가하거나 `web` 미들웨어 그룹 밖에 라우트를 등록하세요:

```
protected $except = [
    'paddle/*',
];
```

<a name="webhooks-local-development"></a>
#### 웹훅과 로컬 개발

로컬에서 웹훅을 수신하려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction) 같은 외부 공개 터널링 서비스를 이용해야 합니다. [Laravel Sail](/docs/10.x/sail)에서는 Sail 내장 [사이트 공유 명령](/docs/10.x/sail#sharing-your-site)을 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 결제 실패 시 구독 취소 등 기본 웹훅 처리를 자동 수행하지만, 추가 이벤트를 직접 처리할 수도 있습니다. Cashier가 발행하는 이벤트를 청취하세요:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅 전체 페이로드를 포함합니다. 예를 들어 `transaction_billed` 이벤트를 처리하려면, 다음과 같은 리스너를 만듭니다:

```
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Paddle 웹훅 수신 처리
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['alert_name'] === 'transaction_billed') {
            // 이벤트 처리...
        }
    }
}
```

리스너를 만든 후, 애플리케이션 `EventServiceProvider`에 등록합니다:

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

Cashier는 특정 이벤트 타입별 이벤트도 제공합니다. 이들은 Paddle의 페이로드뿐 아니라 이벤트 처리에 사용된 모델(청구 대상, 구독, 영수증 등)도 담고 있습니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

웹훅 라우트를 기본값 대신 직접 정의하려면, `.env` 파일에 `CASHIER_WEBHOOK` 환경 변수를 설정합니다. 이 값은 Paddle 콘솔에 등록된 웹훅 URL과 일치해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안을 위해 [Paddle 웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 사용할 수 있습니다. Cashier는 들어오는 요청이 유효한지 검증하는 미들웨어를 기본 제공합니다.

Webhook 비밀 키(`PADDLE_WEBHOOK_SECRET`)를 `.env`에 꼭 정의하세요. 키는 Paddle 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 요금 청구

<a name="charging-for-products"></a>
### 제품 요금 청구

고객에게 제품 구매를 시작하려면, 청구 가능한 모델에서 `checkout` 메서드를 호출해 구매용 결제 세션을 생성하세요. 가격 ID를 하나 이상 전달할 수 있고, 필요하다면 연관 배열로 수량도 전달 가능합니다:

```
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

결제 세션을 받은 후, Cashier가 제공하는 `paddle-button` [Blade 컴포넌트](#overlay-checkout)를 사용해 Paddle 결제 위젯을 표시할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`customData` 메서드를 사용해 거래 생성 시 원하는 임의 데이터를 전달할 수도 있습니다. 자세한 옵션은 [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요:

```
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불

환불은 고객이 구매 시 결제한 수단으로 금액을 반환합니다. 거래 환불을 원한다면 `Cashier\Paddle\Transaction` 모델에서 `refund` 메서드를 사용하세요. 첫 번째 인수는 환불 사유이고, 두 번째 인수로 가격 ID 또는 가격별 금액을 연관 배열로 넘겨 부분 환불할 수 있습니다.

예를 들어, 가격 `pri_123`은 전액 환불, `pri_456`은 2달러만 환불하고 싶다면 아래처럼 작성합니다:

```
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 부분 환불 (단위 센트)
]);
```

전체 거래를 환불하려면 이유만 넘기면 됩니다:

```
$response = $transaction->refund('Accidental charge');
```

자세한 환불 절차는 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]  
> 환불은 Paddle 승인이 필요하여 즉시 처리되지 않을 수 있습니다.

<a name="crediting-transactions"></a>
### 거래 크레딧

환불과 유사하지만, 거래 크레딧은 고객 잔액에 금액을 적립하여 미래 구매 시 사용할 수 있게 합니다. 크레딧은 수동으로 수집된 거래에 대해서만 가능하며, 구독 같은 자동 수집의 경우 Paddle이 자동으로 처리합니다:

```
$transaction = $user->transactions()->first();

// 특정 가격 항목에 대해 전액 크레딧 부여
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle 크레딧 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]  
> 자동 결제 거래는 Paddle이 직접 크레딧을 처리합니다.

<a name="transactions"></a>
## 거래

청구 가능한 모델의 거래 내역은 `transactions` 속성으로 쉽게 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 제품 및 구매 결제 내역과 인보이스를 나타내며, 완료된 거래만 데이터베이스에 저장됩니다.

거래 목록을 표시할 때는 거래 인스턴스의 메서드를 활용해 결제 정보를 보여주고, 인보이스 다운로드 링크를 제공할 수 있습니다:

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

인보이스 다운로드 라우트 예시:

```
use Illuminate\Http\Request;
use Laravel\Cashier\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 과거 및 예정 결제

`lastPayment`와 `nextPayment` 메서드를 이용해 고객의 과거 결제 및 다음 결제 예정 정보를 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 다만, `lastPayment`는 아직 웹훅으로 동기화되지 않았으면 `null`이고, `nextPayment`는 청구 주기가 종료(예: 구독 취소 시)되면 `null`을 반환합니다:

```blade
다음 결제: {{ $nextPayment->amount() }} (예정일: {{ $nextPayment->date()->format('d/m/Y') }})
```

<a name="testing"></a>
## 테스트

테스트 시, 먼저 결제 흐름을 수동으로 직접 실행해 통합 상태를 확인하는 것이 좋습니다.

자동화된 테스트(CI 환경 포함)에서는 [Laravel HTTP 클라이언트](/docs/10.x/http-client#testing)의 페이크 기능을 사용해 Paddle API 호출을 모킹할 수 있습니다. 이는 Paddle 실제 응답은 테스트하지 않지만, 앱의 웹 요청 흐름을 검증하는 데 도움이 됩니다.