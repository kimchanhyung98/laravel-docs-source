# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 덮어쓰기](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [결제 세션](#checkout-sessions)
    - [오버레이 결제](#overlay-checkout)
    - [인라인 결제](#inline-checkout)
    - [비회원 결제](#guest-checkouts)
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
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [복수 구독](#multiple-subscriptions)
    - [구독 일시중지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험기간](#subscription-trials)
    - [결제 정보 선제출 시](#with-payment-method-up-front)
    - [결제 정보 없이](#without-payment-method-up-front)
    - [체험기간 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [제품 결제](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 적립](#crediting-transactions)
- [거래 내역](#transactions)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 이 문서는 Paddle Billing과 통합된 Cashier Paddle 2.x에 관한 내용입니다. 아직 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 직관적이고 유창한 인터페이스를 제공합니다. 복잡한 구독 결제 처리 코드를 대부분 자동화해 줍니다. 기본적인 구독 관리 외에도 구독 전환, 구독 수량, 일시 중지, 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle 사용 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 확인할 것을 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier를 새 버전으로 업그레이드할 때는 항상 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="installation"></a>
## 설치

먼저, Composer로 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

다음으로 `vendor:publish` Artisan 명령어로 Cashier 마이그레이션 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 후, 데이터베이스 마이그레이션을 실행하세요. Cashier 마이그레이션은 새로운 `customers` 테이블과, 고객 구독 정보를 저장하는 `subscriptions`, `subscription_items` 테이블, 그리고 Paddle 거래 내역을 저장할 `transactions` 테이블을 생성합니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 적절히 처리하려면 [Cashier의 웹훅 처리 설정](#handling-paddle-webhooks)을 반드시 구성해야 합니다.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 또는 스테이징 개발 중에는 [Paddle 샌드박스 계정](https://sandbox-login.paddle.com/signup)을 등록하여 실제 결제 없이 테스트할 수 있는 환경을 구축하세요. Paddle에서 제공하는 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 이용하면 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

샌드박스 환경을 사용할 때는 `.env` 파일에 `PADDLE_SANDBOX`를 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

개발을 완료한 뒤에는 [Paddle 판매자 계정](https://paddle.com)에 신청할 수 있으며, 운영 환경에 배포하기 전에 Paddle이 애플리케이션의 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하려면, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 업데이트 등 일반적인 청구 작업을 할 수 있는 다양한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 다른 청구 대상 모델이 있다면 해당 모델에도 같은 트레이트를 추가할 수 있습니다:

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

다음으로, `.env` 파일에 Paddle API 키를 설정하세요. Paddle 제어판에서 API 키를 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 변수는 샌드박스 환경일 때 `true`로, 실제 운영 환경에서는 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 [Retain](https://developer.paddle.com/concepts/retain/overview)을 사용하는 경우에만 선택적으로 설정하세요.

<a name="paddle-js"></a>
### Paddle JS

Paddle의 결제 위젯을 띄우기 위해서는 Paddle JavaScript 라이브러리가 필요합니다. 애플리케이션의 레이아웃 템플릿에서 `</head>` 바로 전에 `@paddleJS` Blade 디렉티브를 추가하여 로드할 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

청구서에 표시되는 금액을 포맷할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en`이 아닌 다른 로케일을 사용하려면 서버에 PHP `ext-intl` 확장 모듈이 설치 및 설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 덮어쓰기

Cashier 내부에서 사용하는 모델을 확장하고 싶다면, 자체 모델을 정의해 Cashier 모델을 상속받으세요:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

그 후, `Laravel\Paddle\Cashier` 클래스를 사용해 Cashier에 커스텀 모델을 지정할 수 있습니다. 일반적으로 이 작업은 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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
> Paddle Checkout을 사용하기 전에 Paddle 대시보드에서 고정 가격의 제품을 정의하고, [Paddle 웹훅 처리 설정](#handling-paddle-webhooks)도 해야 합니다.

애플리케이션을 통해 제품과 구독 결제를 제공하는 작업은 초기에는 어렵게 느껴질 수 있습니다. 그러나 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 활용하면 현대적이고 견고한 결제 통합을 손쉽게 만들 수 있습니다.

일회성 제품 구매 결제는 사용자가 결제 정보를 입력하고 구매를 확정하도록 Paddle Checkout Overlay를 통해 진행합니다. 결제가 완료되면 고객은 여러분의 애플리케이션 내 지정한 성공 URL로 리다이렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예시에서 알 수 있듯, Cashier가 제공하는 `checkout` 메서드를 이용해 특정 "가격 식별자"의 Paddle Checkout Overlay를 위한 결제 세션을 생성합니다. Paddle에서 "가격"은 [특정 제품에 대해 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요시 `checkout` 메서드는 Paddle에 고객 레코드를 자동 생성하고, 해당 정보를 애플리케이션 사용자와 연결합니다. 결제 세션 완료 후에는 고객이 지정한 성공 페이지로 리다이렉션됩니다.

`buy` 뷰에서는 Checkout Overlay를 띄우는 버튼을 포함할 것입니다. `paddle-button` Blade 컴포넌트는 Cashier Paddle에 기본 포함되어 있지만, 직접 [오버레이 체크아웃을 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타데이터 전달하기

주문 완료 후 `Cart`와 `Order` 모델 등으로 주문 및 구매 내역을 관리한다면, Paddle Checkout Overlay에 주문 ID 같은 고유 식별자를 전달해 결제 완료 후 애플리케이션에서 주문과 연결할 수 있습니다.

가령 사용자가 결제 프로세스를 시작할 때 대기중인 주문 `Order`를 생성하는 상황을 생각해 보겠습니다. 참고로 이 예시에서 `Cart`와 `Order`는 Cashier가 제공하는 모델이 아니며, 애플리케이션 필요에 따라 직접 구현해야 합니다:

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

위 예시처럼 장바구니 또는 주문에 연결된 Paddle 가격 식별자들을 `checkout` 메서드에 전달하며, 주문 ID는 `customData` 메서드를 통해 Paddle Checkout Overlay에 전달합니다.

주문이 완료되면, Paddle에서 발생하는 웹훅을 듣고 Cashier 이벤트를 활용해 주문 상태를 "완료"로 변경할 수 있습니다.

예를 들어 `TransactionCompleted` 이벤트를 수신하도록 `AppServiceProvider`의 `boot` 메서드에 리스너를 등록하세요:

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

리스너 예시는 아래와 같습니다:

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * 수신된 Cashier 웹훅 이벤트 처리
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

`transaction.completed` 이벤트에서 전달되는 데이터 구조에 관한 자세한 내용은 Paddle 문서의 [관련 부분](https://developer.paddle.com/webhooks/transactions/transaction-completed)을 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에 Paddle 대시보드에서 고정 가격의 제품을 정의하고, [Paddle 웹훅 처리 설정](#handling-paddle-webhooks)도 해야 합니다.

애플리케이션에서 구독 결제를 제공하는 것은 처음엔 복잡하게 느껴질 수 있습니다. 그러나 Cashier와 [Paddle Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout)를 활용하면 손쉽게 강력한 결제 통합을 구축할 수 있습니다.

예를 들어 'Basic' 제품(`pro_basic`)에 월간(`price_basic_monthly`)과 연간(`price_basic_yearly`) 두 가지 구독 요금제가 있다고 가정해 보겠습니다. 또 다른 제품으로 'Expert' 구독(`pro_expert`)도 있습니다.

우선 고객이 구독을 시작하는 방법을 보겠습니다. 사용자가 애플리케이션 가격 페이지에서 `Basic` 플랜의 "구독" 버튼을 클릭하면, 해당 플랜의 Paddle Checkout Overlay를 띄우게 됩니다. 아래는 그 예시입니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 Checkout Overlay를 띄우는 버튼을 포함합니다. `paddle-button` Blade 컴포넌트는 Cashier Paddle에 포함되어 있지만, 직접 [오버레이 체크아웃을 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

이제 사용자가 구독 버튼을 클릭하면 결제 정보 입력을 완료하고 구독을 시작할 수 있습니다. 결제가 실제 처리되어 구독이 시작되었음을 확인하려면, [Cashier 웹훅 처리](#handling-paddle-webhooks)도 함께 설정해야 합니다.

고객이 구독을 시작하면, 구독한 사용자만 접근 가능한 애플리케이션 영역을 제한할 수 있습니다. 현재 구독 상태는 Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드로 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 제품 또는 가격에 대한 구독 여부도 다음과 같이 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 상품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 플랜을 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 미들웨어 작성

편의를 위해, 요청이 구독한 사용자에게서 오는지 검증하는 [미들웨어](/docs/12.x/middleware)를 작성할 수 있습니다. 이렇게 작성한 미들웨어를 라우트에 지정하면 미구독자의 접근을 차단할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * 들어오는 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // 구독하지 않은 사용자는 결제 페이지로 리다이렉트
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

작성한 미들웨어를 라우트에 할당하는 예시는 다음과 같습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 구독 요금제를 관리하도록 허용하기

고객이 월간 구독에서 연간 구독으로 요금제 변경을 원할 때, 아래와 같은 라우트를 구현할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 예시: 'price_basic_yearly'

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

또 구독 취소 기능도 함께 제공해야 합니다. 아래는 취소 라우트 예시입니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이제 구독은 결제 주기 종료 시점에 취소됩니다.

> [!NOTE]
> Cashier의 웹훅 처리가 구성되어 있으면, Paddle 대시보드에서 구독을 취소할 때도 자동으로 애플리케이션 DB가 동기화됩니다.

<a name="checkout-sessions"></a>
## 결제 세션

고객 청구 대부분은 Paddle의 [Checkout Overlay 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통해 "checkout" 중심으로 이루어집니다.

결제 처리를 시작하기 전엔 Paddle 대시보드에서 애플리케이션의 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 설정해야 합니다.

<a name="overlay-checkout"></a>
### 오버레이 결제

Checkout Overlay 위젯을 띄우기 전에 Cashier로 결제 세션을 생성해야 합니다. 이 세션은 결제 위젯에 처리 정보를 전달합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier에는 `paddle-button` [Blade 컴포넌트](/docs/12.x/blade#components)가 포함되어 있어, 결제 세션을 'prop'으로 전달하면 버튼 클릭 시 Paddle 결제 위젯을 띄웁니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본으로 Paddle의 기본 스타일이 적용되지만, `data-theme='light'` 같은 [Paddle 지원 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 추가해 위젯을 꾸밀 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 위젯은 비동기적으로 동작하며, 구독이 생성되면 Paddle에서 웹훅을 보내 구독 상태를 애플리케이션 DB에 반영하도록 합니다. 따라서 반드시 [웹훅 설정](#handling-paddle-webhooks)을 해야 합니다.

> [!WARNING]
> 구독 상태 변경 후 웹훅 수신까지 약간의 지연이 있을 수 있으니, 완료 직후 구독 상태가 즉시 반영되지 않을 수 있음을 애플리케이션에서 반드시 고려해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 결제 수동 렌더링

Laravel 기본 Blade 컴포넌트를 사용하지 않고 오버레이 결제를 수동으로 렌더링할 수도 있습니다. 우선, 앞 예시처럼 결제 세션을 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그 다음 Paddle.js를 이용해 체크아웃을 초기화할 수 있습니다. 아래는 `paddle_button` 클래스를 할당한 링크로, 클릭 시 오버레이가 나타납니다:

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

Paddle "오버레이" 대신 위젯을 애플리케이션 내부에 임베드하고 싶을 때, Paddle은 인라인 결제 옵션도 제공합니다.

이용이 편하도록 Cashier는 `paddle-checkout` Blade 컴포넌트를 제공합니다. 결제 세션을 생성(앞 예시 참고) 후 아래처럼 전달하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 결제 위젯 높이 조절이 필요하면 `height` 속성을 줍니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

자세한 내용은 Paddle의 [인라인 결제 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [설정 옵션 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 결제 수동 렌더링

Laravel Blade 컴포넌트를 사용하지 않고 인라인 체크아웃을 수동 렌더링할 수도 있습니다. 다음처럼 결제 세션을 생성 후:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Alpine.js를 예로 들어 Paddle.js를 초기화하는 방식입니다 (기본 코드이며 프론트엔드 스택에 맞게 수정하세요):

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
### 비회원 결제

애플리케이션에 계정이 없는 사용자도 결제하도록 하려면 `guest` 메서드를 이용해 결제 세션을 생성할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이후 생성된 결제 세션은 [Paddle 버튼](#overlay-checkout) 또는 [인라인 체크아웃](#inline-checkout) 컴포넌트에 전달하면 됩니다.

<a name="price-previews"></a>
## 가격 미리보기

Paddle은 국가별로 서로 다른 가격을 설정할 수 있습니다. Cashier Paddle에서는 `previewPrices` 메서드로 이러한 가격들을 조회할 수 있습니다. 조회하고자 하는 가격 ID들을 배열로 넘기면 됩니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

기본으로 IP 주소를 기준으로 통화가 결정되지만, 특정 국가 코드와 우편번호를 포함해 요청할 수도 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

받은 가격 데이터는 아래처럼 원하는 형태로 출력할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계 및 세금을 분리해서 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

더 자세한 내용은 [Paddle 가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객 가격 미리보기

이미 고객 정보가 있는 사용자의 경우, 해당 고객 인스턴스를 통해 맞춤 가격을 조회할 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로는 고객의 Paddle ID를 이용해 해당 고객에 맞는 통화로 가격을 받아옵니다. 예를 들어 미국 거주자는 달러, 벨기에는 유로로 가격을 표시합니다. Paddle 대시보드에서 상품이나 플랜의 모든 통화별 가격을 자유롭게 설정할 수 있습니다.

<a name="price-discounts"></a>
### 할인

할인을 적용해 가격을 표시하려면 `previewPrices` 호출 시 `discount_id` 옵션에 할인 ID를 전달하세요:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

그 후, 계산된 할인가격을 출력하면 됩니다:

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
### 고객 기본값

결제 세션을 생성할 때 이메일과 이름을 미리 채워 사용자가 결제 화면으로 바로 넘어가도록 도와줄 수 있습니다. Billable 모델에 다음 메서드를 오버라이드하여 기본 값을 정의합니다:

```php
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

이 기본값은 모든 Cashier 결제 세션 생성에 적용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

Paddle 고객 ID로 Billable 모델 인스턴스를 조회하려면 `Cashier::findBillable` 메서드를 사용하세요:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔 구독하지 않고도 Paddle 고객을 만들고 싶다면 `createAsCustomer` 메서드를 이용할 수 있습니다:

```php
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스가 반환되며, 나중에 구독을 시작할 수 있습니다. 추가 파라미터를 전달하려면 옵션 배열을 넘기면 됩니다 ([Paddle API 문서](https://developer.paddle.com/api-reference/customers/create-customer) 참고):

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면, Billable 모델 인스턴스를 먼저 가져옵니다. 그 후 `subscribe` 메서드로 구독 결제 세션을 만듭니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe` 의 첫 번째 인자는 구독할 가격 식별자(Paddle의 가격 ID)입니다. `returnTo`는 결제 완료 후 리다이렉트할 URL입니다. 두 번째 인자는 내부 구독 종류를 나타내며, `default` 같은 이름을 쓰고 공백을 포함하지 않아야 합니다. 이 값은 사용자에게 노출되지 않고 내부 용도로만 사용합니다.

추가로 구독 관련 메타데이터를 `customData` 메서드로 넘길 수도 있습니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

결제 세션은 앞서 소개한 `paddle-button` Blade 컴포넌트에 넘겨 띄울 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

결제 완료 후 Paddle에서 구독 생성 웹훅(`subscription_created`)이 전송되며, Cashier가 이 웹훅을 처리해 구독 정보를 애플리케이션 DB에 기록합니다. 웹훅 처리 설정을 반드시 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 구독 중인지 확인할 수 있는 다양한 메서드를 제공합니다. 기본적으로 `subscribed` 메서드는 유효한 구독이 있으면(true), 체험 기간 중이라도 true를 반환합니다:

```php
if ($user->subscribed()) {
    // ...
}
```

복수 구독이 있는 경우, 구독 종류를 인자로 넘길 수 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware)에 쓰기에도 적합해서, 구독 여부에 따른 접근 제어를 구현할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * 들어오는 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed()) {
            // 결제하지 않은 사용자면...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

체험 기간 중 여부를 확인하는 `onTrial` 메서드도 있습니다. 사용자에게 체험 기간 알림을 표시할 때 유용합니다:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 Paddle 가격 ID에 가입했는지 확인하려면 `subscribedToPrice`를 사용하세요:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 현재 정상 구독 중이면서 체험이나 유예 기간이 아닌 상태를 체크할 때 씁니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 한때 구독하다가 취소했는지 확인하려면 `canceled` 메서드를 씁니다:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

취소했지만 구독 만료일까지 아직 이용 가능한 유예 기간 중인지 확인하려면 `onGracePeriod`를 사용하세요. 유예 기간에는 여전히 `subscribed`가 true를 반환합니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체 상태

결제 실패 시 구독 상태가 `past_due`가 됩니다. 이 상태에서는 결제 정보 업데이트가 필요합니다. `pastDue` 메서드로 상태를 확인할 수 있습니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

연체 중인 구독이 계속 유효하도록 하려면 `keepPastDueSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register`에서 호출하세요:

```php
use Laravel\Paddle\Cashier;

/**
 * 애플리케이션 서비스 등록.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]
> `past_due` 상태에서는 결제 정보를 업데이트해야 하므로, `swap`과 `updateQuantity` 호출 시 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 쿼리 스코프

구독 상태별로 쿼리할 수 있는 스코프들이 제공됩니다. 예:

```php
// 유효한 구독만 조회
$subscriptions = Subscription::query()->valid()->get();

// 특정 사용자의 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 스코프一覧:

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

구독자에게 구독 외에 일회성 요금을 청구할 수 있습니다. `charge` 메서드에 가격 ID를 하나 또는 여러 개 전달하세요:

```php
// 단일 가격 결제
$response = $user->subscription()->charge('pri_123');

// 여러 가격 동시 결제
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge` 메서드는 실제로 다음 결제 주기에 청구합니다. 즉시 청구하려면 `chargeAndInvoice`를 사용하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별로 결제 수단을 저장합니다. 기본 결제 수단 변경을 원한다면 구독 모델의 `redirectToUpdatePaymentMethod` 메서드를 사용해 Paddle 호스팅 결제 정보 업데이트 페이지로 리다이렉트하세요:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

정보 수정 완료 후 `subscription_updated` 웹훅이 Paddle에서 발송되며, Cashier가 애플리케이션 DB 내용을 갱신합니다.

<a name="changing-plans"></a>
### 요금제 변경

사용자가 구독 요금제를 다른 것으로 변경하고자 할 때, Paddle 가격 식별자를 `swap` 메서드에 전달하세요:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 청구하고 싶으면 `swapAndInvoice` 메서드를 씁니다:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 요금 일할 계산(Prorations)

기본적으로 Paddle은 요금제 변경 시 일할 계산을 적용합니다. 이를 비활성화하려면 `noProrate` 메서드를 체인으로 호출하세요:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

즉시 청구와 조합해 사용 가능:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

요금 청구 없이 요금제를 변경하려면 `doNotBill` 메서드를 추가하세요:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle의 요금 일할 계산 정책은 [공식 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량

구독마다 "수량" 개념을 반영할 수도 있습니다. 예를 들어 프로젝트 당 월 $10 부과하는 서비스에서, `incrementQuantity` 및 `decrementQuantity` 메서드로 쉽게 증감할 수 있습니다:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 5개 증가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 5개 감소
$user->subscription()->decrementQuantity(5);
```

특정 수량으로 설정하려면 `updateQuantity` 메서드를 사용하세요:

```php
$user->subscription()->updateQuantity(10);
```

일할 계산 적용 없이 변경하려면 `noProrate` 메서드와 조합합니다:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독의 수량

[여러 상품 구독](#subscriptions-with-multiple-products)이라면 두 번째 인자로 수량을 변경할 가격 ID를 넘기세요:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독

[Paddle 다중 상품 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)을 이용하면 한 구독에 여러 과금 상품을 연동할 수 있습니다. 예를 들어 기본 구독이 월 $10이고, 라이브 채팅 애드온이 월 $15라고 가정할 때입니다.

구독 세션 생성 시 가격 ID 배열을 전달해 여러 상품을 지정할 수 있습니다:

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

두 요금제 모두 `default` 구독에 연결되어 각각 요금 주기에 따라 결제됩니다. 필요한 경우 연관 배열로 수량을 지정할 수도 있습니다:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 새 가격을 추가할 때는 `swap` 메서드를 사용하며, 현재 가격과 수량도 모두 포함해야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

즉시 청구하려면 `swapAndInvoice`를 쓰세요:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

가격을 구독에서 제외하려면 `swap` 시 해당 가격을 제외하면 됩니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서 마지막 가격을 제거할 수 없습니다. 구독 자체를 취소하세요.

<a name="multiple-subscriptions"></a>
### 복수 구독

Paddle은 고객이 여러 구독을 동시에 가질 수 있도록 지원합니다. 예를 들어 헬스장에서 수영 구독과 웨이트 리프팅 구독을 각각 운영할 수 있습니다.

구독을 생성할 때는 `subscribe` 메서드 두 번째 인자로 구독 종류를 전달하세요:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

요금제를 변경할 때는 해당 구독 종류에 `swap`을 호출하세요:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

취소도 동일 구독에서 실행할 수 있습니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시중지

구독을 일시중지하려면 `pause` 메서드를 호출하세요:

```php
$user->subscription()->pause();
```

이 때 Cashier는 DB의 `paused_at` 컬럼을 자동 설정합니다. 예를 들어 고객이 3월 1일에 일시중지하지만, 실제 결제 주기는 3월 5일에 종료된다면 해당 날짜 전까지는 `paused` 메서드가 `false`를 반환하는데, 이는 고객이 결제한 기간 내 서비스를 계속 이용할 수 있도록 하기 위함입니다.

즉시 중지하려면 `pauseNow`를 쓰세요:

```php
$user->subscription()->pauseNow();
```

특정 기간까지 중지하려면 `pauseUntil` 메서드를 사용합니다:

```php
$user->subscription()->pauseUntil(now()->addMonth());
```

즉시 시작하면서 특정 기간까지 중지하려면 `pauseNowUntil` 메서드를 사용하세요:

```php
$user->subscription()->pauseNowUntil(now()->addMonth());
```

중지 상태에서 유예 기간인지를 `onPausedGracePeriod` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

중지 상태를 해제하려면 `resume` 메서드를 호출하세요:

```php
$user->subscription()->resume();
```

> [!WARNING]
> 중지 상태일 때는 구독 내용 수정이 불가합니다. 요금제를 바꾸거나 수량을 변경하려면 먼저 일시중지 상태를 해제해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독 취소는 `cancel` 메서드로 실행합니다:

```php
$user->subscription()->cancel();
```

취소 시 Cashier가 DB의 `ends_at` 컬럼을 설정합니다. 예를 들어 3월 1일에 취소했지만 종료일이 3월 5일이면, 만료일까지 여전히 `subscribed`가 true입니다.

취소 후 유예 기간은 `onGracePeriod` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow`를 사용하세요:

```php
$user->subscription()->cancelNow();
```

유예 기간 중인 구독 취소를 중단하려면 `stopCancelation`을 호출하면 됩니다:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle 구독은 취소 후 재개할 수 없습니다. 재개하려면 새 구독을 만들어야 합니다.

<a name="subscription-trials"></a>
## 구독 체험기간

<a name="with-payment-method-up-front"></a>
### 결제 정보 선제출 시

고객에게 체험 기간을 제공하면서도 결제 정보를 미리 받으려면, Paddle 대시보드에서 체험기간을 설정하고 결제를 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트를 받으면 체험 종료 날짜가 DB에 저장되고, Paddle은 해당 시점까지 청구를 보류합니다.

> [!WARNING]
> 체험 기간 종료 전에 구독 취소하지 않으면 체험 종료 후 자동 청구되므로, 체험 기간 종료일을 사용자에게 반드시 알리세요.

`onTrial` 메서드로 사용자 체험 여부를 확인할 수 있습니다:

```php
if ($user->onTrial()) {
    // ...
}
```

체험이 만료됐는지는 `hasExpiredTrial` 메서드로 알 수 있습니다:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 타입의 체험 상태를 확인하려면 구독 유형명을 인자로 넘기면 됩니다:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 정보 없이

체험 기간 동안 결제 정보를 요구하지 않을 경우, 사용자 생성 시 Paddle 고객 기록에 `trial_ends_at`을 지정하세요:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

이를 "일반 체험(generic trial)"이라 하며, 구독과 연결되지 않습니다. `User`의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 이내인 경우 true를 반환합니다:

```php
if ($user->onTrial()) {
    // 체험 중...
}
```

실제 구독 생성 시 `subscribe` 메서드를 실행하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

체험 종료일 조회는 `trialEndsAt` 메서드를 사용합니다. 구독 종류를 인자로 줄 수도 있습니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

아직 구독을 생성하지 않은 일반 체험 상태인지 확인하려면 `onGenericTrial`을 사용하세요:

```php
if ($user->onGenericTrial()) {
    // "일반 체험" 기간 중...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험기간 연장 또는 활성화

기존 구독 체험 기간을 연장하려면 `extendTrial` 메서드를 호출하세요:

```php
$user->subscription()->extendTrial(now()->addDays(5));
```

체험을 종료하고 즉시 구독을 활성화하려면 `activate` 메서드를 호출합니다:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle Webhook 처리

Paddle은 다양한 이벤트를 웹훅으로 애플리케이션에 전달합니다. 기본적으로 Cashier는 웹훅 컨트롤러 라우트를 등록하며, 이 컨트롤러가 웹훅 요청을 처리합니다.

기본 기능으로 구독 취소, 구독 정보 업데이트, 결제 방법 변경 등이 처리되지만, 필요하면 컨트롤러를 확장해 추가 웹훅을 직접 처리할 수도 있습니다.

웹훅 작동을 위해 Paddle 대시보드에 웹훅 URL을 설정하세요. 기본값은 `/paddle/webhook` 경로입니다. 설정해야 할 이벤트는 다음과 같습니다:

- 고객 정보 업데이트(Customer Updated)
- 거래 완료(Transaction Completed)
- 거래 업데이트(Transaction Updated)
- 구독 생성(Subscription Created)
- 구독 업데이트(Subscription Updated)
- 구독 일시중지(Subscription Paused)
- 구독 취소(Subscription Canceled)

> [!WARNING]
> 반드시 Cashier에 포함된 [웹훅 서명 검증](/docs/12.x/cashier-paddle#verifying-webhook-signatures) 미들웨어로 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅은 Laravel의 [CSRF 보호](/docs/12.x/csrf)를 우회해야 하므로, `paddle/*` 경로를 CSRF 예외로 등록해야 합니다. `bootstrap/app.php` 파일에서 다음과 같이 설정하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 웹훅과 로컬 개발

Paddle이 로컬 개발 환경에서도 웹훅을 보낼 수 있도록 하려면 Ngrok이나 Expose 같은 사이트 공유 서비스를 사용해 외부에 노출하세요. Laravel Sail 이용 시 [Sail의 사이트 공유 명령어](/docs/12.x/sail#sharing-your-site)를 활용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 기본적으로 실패 결제로 인한 구독 취소 등 주요 웹훅을 자동 처리하지만, 추가 웹훅 처리도 가능합니다. 이벤트 리스너에서 다음 이벤트를 구독하세요:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅 전체 페이로드를 포함합니다. 예를 들어 `transaction.billed` 이벤트를 처리하려면:

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * 수신된 Paddle 웹훅 처리
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // 이벤트 처리...
        }
    }
}
```

또한 특정 웹훅 전용 이벤트도 있습니다. 페이로드와 함께 처리에 활용된 모델 인스턴스도 포함합니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

웹훅 경로를 기본 `/paddle/webhook`가 아닌 다른 경로로 변경하려면 `.env`에 `CASHIER_WEBHOOK` 변수를 지정하세요. 이 값은 Paddle 대시보드와 일치해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안을 위해 [Paddle 웹훅 서명](https://developer.paddle.com/webhooks/signature-verification)을 지원합니다. Cashier는 이를 검증하는 미들웨어를 기본 포함합니다.

웹훅 검증을 활성화하려면 `.env`에 `PADDLE_WEBHOOK_SECRET` 변수를 정의해야 하며, Paddle 계정에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 결제

<a name="charging-for-products"></a>
### 제품 결제

고객에게 제품 구매를 시작하려면 Billable 모델 인스턴스의 `checkout` 메서드로 결제 세션을 생성하세요. 하나 또는 여러 가격 ID를 전달할 수 있으며, 연관 배열을 써서 수량도 지정 가능합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

생성된 결제 세션은 Cashier가 제공하는 `paddle-button` Blade 컴포넌트에 넘겨, Paddle 위젯을 띄우고 구매를 완료할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`customData` 메서드로 결제 처리 시 필요한 커스텀 데이터를 전달할 수 있습니다. Paddle의 [커스텀 데이터 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불

환불은 고객이 구매할 때 사용한 결제 수단으로 환불 금액을 돌려줍니다. Paddle 결제를 환불하려면, `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용하세요. 이유, 환불할 가격 ID 및 선택적 금액을 인자로 넘깁니다.

예를 들어, `pri_123`은 전액, `pri_456`는 2달러만 환불하고 싶다면:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 부분 환불 (단위는 페니 또는 센트)
]);
```

전체 거래를 환불하려면 이유만 전달하세요:

```php
$response = $transaction->refund('Accidental charge');
```

더 자세한 환불 정책은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 환불 처리는 Paddle의 승인 후에 최종적으로 완료됩니다.

<a name="crediting-transactions"></a>
### 거래 적립

환불과 달리 적립은 고객 잔고에 금액을 더해 향후 결제에 사용할 수 있도록 합니다. 수동 결제 건에만 가능하며, 자동 결제(구독)는 Paddle에서 자동으로 처리합니다:

```php
$transaction = $user->transactions()->first();

// 특정 가격 항목을 전액 적립
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle 적립 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 적립은 수동 결제만 가능하며, 자동 결제는 Paddle에서 관리합니다.

<a name="transactions"></a>
## 거래 내역

Billable 모델의 거래 내역은 `transactions` 속성으로 쉽게 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 제품 및 결제 내역을 나타내며, 완료된 거래만 DB에 저장됩니다.

사용자에게 거래 목록과 청구서를 표시하려면 각 거래 인스턴스의 관련 메서드를 활용해 정보를 출력할 수 있습니다:

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
### 과거 및 예정 결제

반복 결제 구독에 대해, 고객의 과거 및 예정 결제를 `lastPayment`와 `nextPayment` 메서드로 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 모두 `Laravel\Paddle\Payment` 인스턴스를 반환하며, `lastPayment`는 아직 웹훅으로 트랜잭션이 동기화되지 않은 경우 `null`이 될 수 있습니다. `nextPayment`는 구독 종료 시에도 `null` 반환 가능합니다.

결과를 출력할 때 예시:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트

테스트 시에는 실제 결제 흐름을 수동으로 점검해 통합이 제대로 됐는지 확인하세요.

자동화된 테스트(CI 환경 등)에서는 Laravel HTTP Client의 [가짜 호출 기능](/docs/12.x/http-client#testing)을 활용해 Paddle API 요청을 가짜로 처리할 수 있습니다. 실제 Paddle 응답을 검증하지는 않지만, 자체 애플리케이션 동작 테스트는 가능합니다.