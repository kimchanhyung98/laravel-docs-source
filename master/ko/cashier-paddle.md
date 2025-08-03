# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [빌러블 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 구성](#currency-configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
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
    - [여러 제품으로 구성된 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험기간](#subscription-trials)
    - [선결제 결제정보 필요 시](#with-payment-method-up-front)
    - [선결제 결제정보 없이](#without-payment-method-up-front)
    - [체험기간 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle 웹훅 처리](#handling-paddle-webhooks)
    - [웹훅 이벤트 핸들러 정의하기](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [제품 청구](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 적립](#crediting-transactions)
- [거래](#transactions)
    - [과거 및 예정된 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x와 Paddle Billing 통합에 관한 것입니다. 아직 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)는 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 표현력 있으며 직관적인 인터페이스를 제공합니다. 번거로운 구독 결제 관련 코드를 거의 모두 처리해줍니다. 기본 구독 관리뿐 아니라 구독 교체, 구독 수량, 구독 일시정지, 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 사용하기 전에는 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)를 먼저 살펴보시길 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 안내서](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 주의 깊게 확인하세요.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer를 사용하여 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

이후 `vendor:publish` Artisan 명령어를 통해 Cashier 마이그레이션 파일을 배포하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

마지막으로 애플리케이션 데이터베이스 마이그레이션을 실행합니다. Cashier 마이그레이션은 고객 정보를 저장할 `customers` 테이블과 구독 정보를 저장할 `subscriptions`, `subscription_items` 테이블을 생성합니다. 그리고 Paddle 거래 정보를 담을 `transactions` 테이블도 생성합니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 Paddle 이벤트를 제대로 처리하려면 [Cashier 웹훅 처리 설정](#handling-paddle-webhooks)을 반드시 하세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스 (Paddle Sandbox)

로컬 및 스테이징 환경에서는 [Paddle 샌드박스 계정](https://sandbox-login.paddle.com/signup)을 등록하세요. 이 계정은 실제 결제없이 테스트와 개발을 할 수 있는 격리된 환경을 제공합니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card)를 사용해 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

샌드박스 환경을 사용할 때는 애플리케이션의 `.env` 파일에 `PADDLE_SANDBOX` 환경변수를 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

개발을 마친 후에는 [Paddle 판매자 계정 신청](https://paddle.com)을 하세요. 프로덕션 배포 전에는 Paddle의 도메인 승인 절차가 필요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 빌러블 모델 (Billable Model)

Cashier를 사용하려면, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 정보 업데이트 등 일반적인 청구 관련 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자 외에도 청구 대상 엔티티가 있다면 해당 클래스에 이 트레이트를 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키 (API Keys)

이제 Paddle API 키를 애플리케이션 `.env` 파일에 설정하세요. Paddle 컨트롤 패널에서 API 키를 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX`는 샌드박스 환경 사용 시 `true`로 설정하고, 라이브 환경에서는 `false`로 설정하세요.

`PADDLE_RETAIN_KEY`는 Retain과 함께 Paddle을 사용할 때만 설정하는 선택적 키입니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle 체크아웃 위젯을 띄우기 위해 Paddle의 JavaScript 라이브러리가 필요합니다. 애플리케이션 레이아웃의 닫는 `</head>` 태그 바로 전에 `@paddleJS` Blade 디렉티브를 추가하세요:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 구성 (Currency Configuration)

송장 등에서 통화 금액 표시 시 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 PHP의 [NumberFormatter 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 외 로케일을 사용할 경우 서버에 `ext-intl` PHP 확장 모듈이 설치 및 구성되어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

Cashier가 내부에서 사용하는 모델을 확장하고 싶다면, 자신의 모델을 정의하여 Cashier 모델을 상속받으세요:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

이후 `Laravel\Paddle\Cashier` 클래스를 통해 Cashier에게 사용자 정의 모델을 사용하도록 설정하세요. 일반적으로, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 정의합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * 부트스트랩 애플리케이션 서비스.
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
### 제품 판매 (Selling Products)

> [!NOTE]
> Paddle 체크아웃을 사용하기 전에, Paddle 대시보드에서 고정 가격이 설정된 제품을 정의해야 합니다. 또한 [Paddle 웹훅 처리](#handling-paddle-webhooks)도 구성해야 합니다.

애플리케이션에서 제품과 구독 결제를 제공하는 것은 다소 복잡할 수 있습니다. 그러나 Cashier와 [Paddle 체크아웃 오버레이](https://www.paddle.com/billing/checkout)를 사용하면 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

비반복 단일 제품 청구를 할 때는 Paddle의 체크아웃 오버레이를 띄워 고객이 결제 정보를 입력하고 구매를 확인하도록 만듭니다. 결제가 완료되면 고객은 애플리케이션 내 지정한 성공 URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제에서 보듯, Cashier의 `checkout` 메서드를 통해 가격 식별자에 해당하는 체크아웃 객체를 생성하여 Paddle 체크아웃 오버레이를 제공합니다. 여기서 "price identifier"(가격 ID)는 [Paddle 대시보드에서 정의하는 상품별 가격을 의미합니다](https://developer.paddle.com/build/products/create-products-prices).

필요하다면 `checkout` 메서드가 자동으로 Paddle에 고객을 생성하고, 애플리케이션의 사용자와 Paddle 고객 레코드를 연결해줍니다. 결제 세션이 끝나면 고객은 성공 페이지로 리디렉션되어 안내 메시지를 볼 수 있습니다.

`buy` 뷰에서는 체크아웃 오버레이를 띄우는 버튼을 포함합니다. Cashier Paddle에 기본 제공되는 `paddle-button` Blade 컴포넌트를 사용하거나 직접 [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle 체크아웃에 메타 데이터 전달하기

제품 판매 시, 주문 정보를 `Cart`와 `Order` 모델로 관리하는 경우가 많습니다. Paddle 체크아웃으로 리디렉션할 때 기존 주문 ID를 전달해야 구매 완료 후 사용자와 주문을 쉽게 연결할 수 있죠.

예를 들어, 사용자가 체크아웃을 시작할 때 애플리케이션에 `Order`가 생성된다고 가정합시다. 이 예제의 `Cart`와 `Order` 모델은 Cashier에서 제공하지 않으니 직접 구현해야 합니다:

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

위와 같이 `checkout` 메서드에 장바구니/주문과 연결된 Paddle 가격 ID를 모두 전달합니다. `customData` 메서드로 주문 ID를 Paddle에 넘겨줄 수도 있습니다.

결제 완료 후 주문을 "완료" 상태로 변경하려면, Paddle과 Cashier가 발송하는 웹훅을 받아 주문 정보를 데이터베이스에 저장해야 합니다.

시작하려면, Cashier가 발송하는 `TransactionCompleted` 이벤트에 리스너를 등록하세요. 보통은 `AppServiceProvider`의 `boot` 메서드에서 등록합니다:

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * 부트스트랩 애플리케이션 서비스.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

리스너 예시:

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * 들어오는 Cashier 웹훅 이벤트 처리.
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

`transaction.completed` 이벤트에 포함되는 데이터에 관해서는 Paddle [공식 문서](https://developer.paddle.com/webhooks/transactions/transaction-completed)를 참조하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]
> Paddle 체크아웃을 사용하기 전에, Paddle 대시보드에서 고정 가격이 설정된 제품을 정의해야 하며 [Paddle 웹훅 처리](#handling-paddle-webhooks)를 구성해야 합니다.

제품과 구독 결제를 지원하는 것은 복잡할 수 있지만 Cashier와 [Paddle 체크아웃 오버레이](https://www.paddle.com/billing/checkout)를 이용하면 쉽게 실현 가능합니다.

간단한 예를 들어, 월간(`price_basic_monthly`)과 연간(`price_basic_yearly`) 플랜이 있고, 이 둘은 "Basic" 제품(`pro_basic`) 아래에 묶여 있다고 가정해보겠습니다. 또한 "Expert" 플랜도 있을 수 있죠.

고객이 Basic 플랜에 가입하는 과정을 살펴봅시다. 예를 들어 고객이 가격 페이지의 "Subscribe" 버튼을 클릭하면 해당 플랜에 대한 Paddle 체크아웃 오버레이가 뜹니다. 우선 `checkout` 메서드로 체크아웃 세션을 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 체크아웃 오버레이 버튼을 포함합니다. `paddle-button` Blade 컴포넌트를 사용하거나 직접 [오버레이 체크아웃 수동 렌더링](#manually-rendering-an-overlay-checkout)도 가능합니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

Subscribe 버튼 클릭 후, 고객은 결제 정보를 입력하여 구독을 시작합니다. 일부 결제 방법은 처리에 시간이 걸리므로 구독 시작을 확실히 알기 위해 [Cashier 웹훅 처리](#handling-paddle-webhooks)를 반드시 구성해야 합니다.

구독이 시작되면, 애플리케이션 내 특정 영역은 구독한 사용자만 접근 가능하도록 제한하는 것이 일반적입니다. 사용자의 구독 상태는 `Billable` 트레이트의 `subscribed` 메서드로 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 제품 또는 가격 ID에 대한 구독 여부도 쉽게 판별할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 제품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 플랜을 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 미들웨어 작성하기

편의를 위해, 요청 사용자가 구독 중인지 확인하는 [미들웨어](/docs/master/middleware)를 작성할 수 있습니다. 작성 후 해당 미들웨어를 라우트에 할당하여 비구독자는 접근을 차단할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * 들어오는 요청 처리.
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // 구독하지 않은 사용자는 청구 페이지로 리디렉션...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

미들웨어 등록 예시:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 결제 플랜 관리 가능하게 하기

고객이 월간에서 연간 구독으로 변경하는 등 결제 플랜을 변경할 수 있어야 합니다. 예를 들어 다음과 같이 플랜 교체를 실행하는 경로를 구현할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // $price는 예시로 price_basic_yearly

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

또한 구독 취소도 제공해야 합니다. 취소 라우트 예:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이제 구독이 현재 청구 기간 종료 시점에 취소됩니다.

> [!NOTE]
> Cashier 웹훅 처리를 설정했다면, Paddle 대시보드에서 구독 취소 시 해당 웹훅이 도착해 Cashier가 데이터베이스 상태를 자동으로 동기화합니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션 (Checkout Sessions)

대부분의 고객 청구 작업은 Paddle의 [체크아웃 오버레이 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통해 수행됩니다.

체크아웃 결제 전에 Paddle 체크아웃 설정에서 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 설정해두세요.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃 (Overlay Checkout)

체크아웃 오버레이 위젯을 띄우려면 우선 Cashier를 통해 체크아웃 세션을 생성해야 합니다. 생성된 세션에는 결제 관련 정보가 포함됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier는 `paddle-button` Blade 컴포넌트를 포함합니다. 이 컴포넌트에 체크아웃 세션을 프로퍼티로 전달하면 버튼 클릭 시 Paddle 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle의 기본 스타일이 적용됩니다. `data-theme='light'` 등 Paddle이 지원하는 속성으로 스타일을 커스터마이징할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

체크아웃 위젯은 비동기 처리됩니다. 구독 생성 후 Paddle은 웹훅을 보내 애플리케이션에 상태 변경을 알립니다. 반드시 [웹훅 처리](#handling-paddle-webhooks)를 준비하세요.

> [!WARNING]
> 구독 상태 변경 후 해당 웹훅 수신 지연이 보통 매우 짧지만, 사용자 구독 상태가 즉시 반영되지 않을 수 있으니 애플리케이션에서 유념하세요.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 수동 렌더링

Laravel이 제공하는 Blade 컴포넌트를 사용하지 않고 수동으로 오버레이 체크아웃을 띄울 수도 있습니다. 우선 앞서 설명한 대로 체크아웃 세션을 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그 다음 Paddle.js를 이용해 초기화합니다. `paddle_button` 클래스를 갖는 링크를 만들면 Paddle.js가 감지하여 클릭 시 체크아웃 오버레이를 표시합니다:

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

Paddle의 오버레이 위젯 대신, 위젯을 애플리케이션 내에 직접 임베드하는 인라인 체크아웃도 가능합니다.

Cashier는 `paddle-checkout` Blade 컴포넌트를 제공해 인라인 체크아웃을 쉽게 구현할 수 있습니다. 먼저 체크아웃 세션을 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

컴포넌트에 체크아웃 세션을 넘겨 표시합니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

컴포넌트 높이는 `height` 속성으로 조절할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

자세한 설정 옵션은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)와 [체크아웃 설정](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참조하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

Blade 컴포넌트 대신 수동 렌더링도 가능합니다. 체크아웃 세션을 생성한 다음, 아래 예시처럼 [Alpine.js](https://github.com/alpinejs/alpine) 등을 이용해 Paddle 체크아웃을 초기화할 수 있습니다:

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

애플리케이션 계정을 만들 필요가 없는 비회원용 체크아웃 세션도 생성할 수 있습니다. `Checkout::guest` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

이 세션은 [paddle-button](#overlay-checkout)이나 [inline checkout](#inline-checkout) 컴포넌트에 전달하여 사용 가능합니다.

<a name="price-previews"></a>
## 가격 미리보기 (Price Previews)

Paddle은 국가별 통화를 고려한 맞춤형 가격 설정이 가능합니다. Cashier Paddle의 `previewPrices` 메서드로 특정 가격 ID들의 가격 정보를 조회할 수 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화는 요청 IP로 판단되지만, 특정 국가를 지정할 수도 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

조회한 가격은 원하는 방식으로 출력할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

소계와 세금을 분리해서 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} 세금)</li>
    @endforeach
</ul>
```

더 자세한 내용은 Paddle의 [가격 미리보기 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객별 가격 미리보기 (Customer Price Previews)

이미 고객인 사용자에게 적용되는 가격을 보여주려면 해당 고객 인스턴스에서 바로 가격을 조회할 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 사용자의 고객 ID를 이용해 통화에 맞는 가격을 받아옵니다. 예를 들어 미국 사용자는 달러, 벨기에 사용자는 유로 가격을 보게 됩니다. 통화에 맞는 가격이 없으면 제품 기본 통화가 사용됩니다. Paddle 컨트롤 패널에서 제품 또는 구독 플랜의 가격을 모두 조정할 수 있습니다.

<a name="price-discounts"></a>
### 할인 (Discounts)

할인 적용 후 가격도 보여줄 수 있습니다. `previewPrices` 호출 시 `discount_id` 옵션을 넘겨 할인 코드를 지정하세요:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격은 다음과 같이 출력할 수 있습니다:

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

체크아웃 세션 생성 시 미리 고객 이메일이나 이름을 채워 넣으면 결제 과정이 빠릅니다. 빌러블 모델에 다음 메서드를 오버라이드해 기본값을 설정할 수 있습니다:

```php
/**
 * Paddle에 연관 지을 고객 이름.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Paddle에 연관 지을 고객 이메일.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```

이 값들은 모든 Cashier 작업에서 체크아웃 세션 생성 시 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

Paddle 고객 ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 빌러블 모델 인스턴스를 반환합니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

가끔 구독을 시작하지 않고 고객만 생성하고 싶을 때 `createAsCustomer` 메서드를 사용합니다:

```php
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스가 반환됩니다. 고객 생성 후 구독은 나중에 시작할 수 있습니다. 옵션 배열을 전달해 Paddle API가 지원하는 추가 고객 생성 파라미터를 넘길 수 있습니다:

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독 (Subscriptions)

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면, 보통 사용자 모델 인스턴스를 데이터베이스에서 조회한 뒤 `subscribe` 메서드로 체크아웃 세션을 만든 후 뷰에 전달합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

- 첫 번째 인자는 구독할 Paddle 가격 식별자입니다.
- `returnTo`는 결제 성공 후 리디렉션할 URL입니다.
- 두 번째 인자는 내부 구독 유형이며, 단일 구독만 있다면 보통 `default` 또는 `primary`로 하며 사용자에게 노출되지 않고 변경하지 않습니다.

`customData` 메서드로 구독 관련 임의 메타데이터 전달도 가능합니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

체크아웃 세션은 `paddle-button` Blade 컴포넌트에 전달해 사용할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

구독 생성 후 Paddle에서 `subscription_created` 웹훅이 발송되고, Cashier가 받아서 데이터베이스에 구독을 설정합니다. 웹훅 처리가 제대로 되어 있는지 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

사용자가 구독 중인지 확인하는 여러 메서드가 제공됩니다. 가장 기본은 `subscribed` 메서드로, 유효한 구독이 있으면 `true`를 반환하며 체험 기간 내도 포함합니다:

```php
if ($user->subscribed()) {
    // 구독 중...
}
```

다중 구독이 있는 경우 인자로 구독 유형을 지정할 수 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/master/middleware)로 활용해 접근 권한 필터링에 쓰기 좋습니다.

체험 기간 내 여부는 `onTrial` 메서드로 확인하세요:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 가격 ID에 대한 구독도 `subscribedToPrice`로 확인 가능합니다:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

`recurring` 메서드는 구독이 활성구독이고 체험기간 및 유예기간이 아닐 때 `true`를 반환합니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

과거 구독했으나 현재 취소된 구독인지 확인하려면 `canceled` 메서드를 사용하세요:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

아직 구독 기간 종료 전 유예 기간에 있는 경우 `onGracePeriod`가 `true`를 반환하며, 유예 기간 동안 `subscribed`도 `true`입니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체 상태

결제가 실패할 경우 구독은 `past_due` 상태가 됩니다. 이 상태로는 결제 정보 갱신 전까지 활성화되지 않습니다. 해당 상태인지 `pastDue` 메서드로 확인하세요:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

`past_due` 구독자는 결제정보 갱신을 안내하는 것이 좋습니다.

연체 구독을 계속 활성 상태로 유지하려면 `Cashier::keepPastDueSubscriptionsActive()` 메서드를 호출하세요. 일반적으로 `AppServiceProvider`의 `register` 메서드에서 호출합니다:

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
> `past_due` 상태 구독은 결제 정보가 업데이트되기 전까지 `swap` 및 `updateQuantity` 메서드 사용 시 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 스코프

구독 상태를 기반으로 쉽게 데이터베이스 쿼리를 할 수 있도록 스코프 메서드도 제공합니다:

```php
// 유효한 구독 모두 조회…
$subscriptions = Subscription::query()->valid()->get();

// 특정 사용자의 취소된 구독 조회…
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

구독 중인 고객에게 구독 외 단발성 청구를 하려면 `charge` 메서드에 단일 또는 여러 가격 ID를 제공하세요:

```php
// 단일 가격 청구...
$response = $user->subscription()->charge('pri_123');

// 여러 가격 동시에 청구...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

`charge`는 실제 청구는 다음 청구 주기에 이루어집니다. 즉시 청구하려면 대신 `chargeAndInvoice`를 호출하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트 (Updating Payment Information)

Paddle은 구독별로 결제 수단을 저장합니다. 기본 결제 수단을 변경하려면 구독 모델에서 `redirectToUpdatePaymentMethod` 메서드로 Paddle 결제 수단 업데이트 페이지로 리디렉션하세요:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

업데이트가 완료되면 Paddle에서 `subscription_updated` 웹훅이 발송되어 애플리케이션 데이터베이스가 갱신됩니다.

<a name="changing-plans"></a>
### 플랜 변경 (Changing Plans)

구독 플랜 변경은 구독의 `swap` 메서드에 새로운 Paddle 가격 ID를 전달하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 청구하려면 `swapAndInvoice`를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 비례 요금 조정(Prorations)

기본적으로 Paddle은 플랜 교체 시 비례 요금을 계산합니다. 비례 청구 없이 플랜을 변경하려면 `noProrate` 메서드를 체인으로 사용하세요:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

비례 조정 없이 즉시 청구도 가능합니다:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

또는 청구를 하지 않고 플랜만 변경하려면 `doNotBill`을 사용하세요:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

Paddle 비례 요금 정책은 [Paddle 공식 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

"수량"으로 구독 요금이 결정되는 경우, `incrementQuantity`와 `decrementQuantity` 메서드로 쉽게 수량을 조정할 수 있습니다:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 수량 5 증가...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 수량 5 감소...
$user->subscription()->decrementQuantity(5);
```

특정 수량으로 설정하려면 `updateQuantity`를 사용합니다:

```php
$user->subscription()->updateQuantity(10);
```

비례 청구 없이 수량 변경 시 `noProrate`를 체인하세요:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 제품 구독 수량 조정

[여러 제품이 포함된 구독](#subscriptions-with-multiple-products)에서 특정 가격의 수량만 변경하려면 두 번째 인자로 가격 ID를 넘깁니다:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 제품으로 구성된 구독 (Subscriptions With Multiple Products)

여러 청구 제품을 하나의 구독에 연결할 수 있습니다. 예를 들어 기본 $10 구독에 라이브 채팅 추가 요금 $15를 더하는 경우입니다.

구독 체크아웃 생성 시, `subscribe` 메서드에 가격 배열을 전달하세요:

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

이렇게 생성된 구독에는 두 가격이 모두 포함되어 각각 청구됩니다.

수량을 지정하려면 다음과 같이 연관 배열로 전달합니다:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 새 가격을 추가하려면 `swap` 시 기존 가격과 수량을 모두 포함해야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

즉시 청구하려면 `swapAndInvoice`를 사용하세요:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

가격 제거는 `swap`에서 해당 가격을 빼면 됩니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]
> 구독에서 마지막 가격은 제거할 수 없습니다. 마지막 가격을 제거하려면 구독을 취소하세요.

<a name="multiple-subscriptions"></a>
### 다중 구독 (Multiple Subscriptions)

Paddle은 하나의 고객이 여러 구독을 동시에 가질 수 있도록 지원합니다. 여러 종류의 서비스를 운영하는 경우 각 구독별로 다른 이름(type)을 지정하세요.

구독 생성 시 `subscribe` 메서드 두 번째 인자로 구독 유형 문자열을 넘깁니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

구독 변경 시에도 해당 유형을 지정해 `swap` 합니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

완전 취소도 가능합니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시정지 (Pausing Subscriptions)

구독을 일시정지하려면 `pause` 메서드를 호출합니다:

```php
$user->subscription()->pause();
```

이때 `paused_at` 컬럼이 설정되며, 보통 다음 청구 주기부터 정지 상태가 반영됩니다. 예를 들어 3월 5일 청구 주기 예정인 구독을 3월 1일 정지했다면, 3월 5일 전까지는 여전히 활성 상태(`paused`는 `false`)입니다.

즉시 정지하려면 `pauseNow` 메서드를 사용하세요:

```php
$user->subscription()->pauseNow();
```

특정 시점까지 정지하려면 `pauseUntil`:

```php
$user->subscription()->pauseUntil(now()->addMonth());
```

즉시 정지 후 특정 기간 정지는 `pauseNowUntil`:

```php
$user->subscription()->pauseNowUntil(now()->addMonth());
```

유예 기간 내 일시정지 상태 여부는 `onPausedGracePeriod` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

정지된 구독을 재개하려면 `resume`을 호출하세요:

```php
$user->subscription()->resume();
```

> [!WARNING]
> 정지된 상태에선 구독을 변경할 수 없습니다. 변경하려면 먼저 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소 (Canceling Subscriptions)

구독을 취소하려면 `cancel` 메서드를 호출합니다:

```php
$user->subscription()->cancel();
```

취소 시 `ends_at` 컬럼이 설정되어, 종료일까지 구독 유효 상태가 유지됩니다. 종료일까지 `subscribed`는 계속 `true`입니다.

유예 기간 내 취소 여부는 `onGracePeriod`로 확인할 수 있습니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow`를 사용하세요:

```php
$user->subscription()->cancelNow();
```

취소 예정 상태에서 취소를 중지하려면 `stopCancelation`을 호출하세요:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]
> Paddle 구독은 취소 후 재개할 수 없습니다. 재개하려면 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 선결제 결제정보 필요 시

사용자에게 체험 기간을 주면서도 결제 정보를 미리 수집하려면 Paddle 대시보드에서 가격에 체험 기간을 설정하세요. 그 후 일반 구독 체크아웃을 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 웹훅 수신 시 Cashier는 애플리케이션 데이터베이스의 구독 레코드에 체험 종료일을 기록하고, Paddle에도 과금 시작을 연기하도록 지시합니다.

> [!WARNING]
> 체험 종료일 전에 구독을 취소하지 않으면 체험 종료와 동시에 청구가 시작되므로 사용자에게 종료일을 알리는 것이 좋습니다.

사용자가 체험 중인지 `onTrial` 메서드로 확인할 수 있습니다:

```php
if ($user->onTrial()) {
    // ...
}
```

체험이 만료됐는지 확인하려면 `hasExpiredTrial` 메서드를 사용하세요:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```

특정 구독 유형에 대한 검사도 가능합니다:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 선결제 결제정보 없이

사용자로부터 결제 정보를 미리 받지 않고 체험 기간을 제공하려면, 가입 시 `trial_ends_at` 컬럼을 사용자와 연결된 Paddle 고객 레코드에 설정하세요:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

Cashier는 이를 "일반 체험(generic trial)"이라 부릅니다. 구독이 존재하지 않아도 `onTrial` 메서드는 이 값을 기준으로 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // 체험 중...
}
```

체험 종료 후 구독이 필요하면 일반 구독 생성 과정을 진행하세요.

체험 종료일 조회는 `trialEndsAt`으로 합니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

일반 체험 상태인지 특화하여 확인하려면 `onGenericTrial` 메서드를 사용하십시오:

```php
if ($user->onGenericTrial()) {
    // 일반 체험 중...
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험기간 연장 또는 활성화

기존 구독의 체험 기간을 연장하려면 `extendTrial` 메서드에 종료일을 지정하세요:

```php
$user->subscription()->extendTrial(now()->addDays(5));
```

즉시 체험을 종료하고 구독을 활성화하려면 `activate`를 호출하세요:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹훅 처리 (Handling Paddle Webhooks)

Paddle은 다양한 이벤트를 웹훅으로 애플리케이션에 통지합니다. Cashier는 기본적으로 웹훅 요청을 처리하는 컨트롤러를 제공합니다.

이 컨트롤러는 실패 구독 취소, 구독 업데이트, 결제 수단 변경 등을 자동 처리하며, 원하는 Paddle 웹훅 이벤트를 직접 처리하도록 확장도 가능합니다.

웹훅 처리가 가능하도록 Paddle 대시보드에 웹훅 URL을 설정하세요. 기본 경로는 `/paddle/webhook`입니다.

활성화할 웹훅 목록:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Cashier가 제공하는 [웹훅 서명 검증](/docs/master/cashier-paddle#verifying-webhook-signatures) 미들웨어를 사용해 요청 보호를 꼭 하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Paddle 웹훅은 Laravel CSRF 보호를 우회해야 하므로, `paddle/*` 경로에 대해서는 CSRF 검증을 제외해야 합니다. `bootstrap/app.php`에서 다음처럼 설정하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 웹훅과 로컬 개발

로컬 개발 중 Paddle 웹훅을 받으려면 [Ngrok](https://ngrok.com/)이나 [Expose](https://expose.dev/docs/introduction) 같은 사이트 공유 서비스를 사용해 애플리케이션을 외부에 공개하세요. Laravel Sail 사용자라면 Sail의 [사이트 공유 명령어](/docs/master/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의하기 (Defining Webhook Event Handlers)

Cashier는 실패한 결제 시 구독 취소 등 기본 웹훅을 자동 처리합니다. 추가로 웹훅을 처리하려면 다음 이벤트에 리스너를 등록하세요:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트는 Paddle 웹훅 전체 페이로드를 포함합니다. 예를 들어 `transaction.billed` 웹훅을 처리하려면:

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Paddle 웹훅 수신 처리.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // 이벤트 처리...
        }
    }
}
```

Cashier는 웹훅 종류별로 다음 이벤트도 발송합니다. 페이로드 외에 관련된 모델 인스턴스(예: 빌러블, 구독, 영수증 등)도 포함합니다:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

웹훅용 기본 라우트를 오버라이드하려면 애플리케이션 `.env` 파일에 `CASHIER_WEBHOOK` 환경변수를 정의하세요. 이 값은 웹훅 URL이며 Paddle에도 같은 URL을 등록해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증 (Verifying Webhook Signatures)

웹훅 보안을 위해 Paddle에서 제공하는 [웹훅 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks)을 사용하세요. Cashier는 웹훅 요청이 유효한지 검증하는 미들웨어를 기본 포함합니다.

사용하려면 `.env` 파일에 `PADDLE_WEBHOOK_SECRET` 환경변수를 Paddle 대시보드에서 가져온 비밀키로 설정하세요.

<a name="single-charges"></a>
## 단일 청구 (Single Charges)

<a name="charging-for-products"></a>
### 제품 청구 (Charging for Products)

고객에게 제품 구매를 청구하려면, 빌러블 모델 인스턴스의 `checkout` 메서드를 통해 가격 ID 배열로 체크아웃 세션을 만듭니다. 필요에 따라 수량도 연관 배열로 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

생성한 체크아웃 세션은 Cashier의 `paddle-button` Blade 컴포넌트에 전달해 사용자가 Paddle 체크아웃 위젯을 볼 수 있도록 합니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`customData` 메서드로 거래 생성 시 사용자 정의 데이터를 Paddle에 넘길 수 있습니다. 가능한 옵션은 [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)를 참고하세요:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불 (Refunding Transactions)

거래 환불은 고객이 결제 수단으로 되돌려 줄 금액을 반환합니다. Paddle 구매 환불은 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드로 수행하며, 이유와 환불할 가격 ID 및 금액(부분 환불 가능)을 인자로 받습니다. 빌러블 모델의 `transactions` 메서드로 관련 거래 조회 가능:

예를 들어, 거래에서 `pri_123`은 전액 환불, `pri_456`은 부분 환불($2)에 대해:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전체 환불
    'pri_456' => 200, // 부분 환불 (단위: 센트)
]);
```

전체 거래를 환불하려면 이유만 넘기세요:

```php
$response = $transaction->refund('Accidental charge');
```

환불 관련 자세한 내용은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 환불은 Paddle의 승인을 반드시 받아야 완료됩니다.

<a name="crediting-transactions"></a>
### 거래 적립 (Crediting Transactions)

거래 적립도 가능하며, 이는 고객 잔액에 자금을 추가하여 이후 구매에 사용할 수 있게 합니다. 수동으로 결제된 거래에만 적용되고, 자동 청구 구독에는 Paddle에서 자동으로 처리합니다:

```php
$transaction = $user->transactions()->first();

// 특정 상품에 대해 전액 적립...
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle 적립 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]
> 적립은 수동 결제 거래에만 가능하며, 자동 결제 거래는 Paddle이 직접 처리합니다.

<a name="transactions"></a>
## 거래 (Transactions)

빌러블 모델의 거래 목록은 `transactions` 프로퍼티로 쉽게 조회 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 제품 및 구매 결제와 영수증과 연결되며, 완료된 거래만 데이터베이스에 저장됩니다.

거래 목록을 화면에 표시할 때는 거래 인스턴스 메서드를 활용해 결제 정보 등을 출력할 수 있습니다. 예를 들어 표로 출력 및 송장 다운로드 링크 제공:

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

구독에 대한 과거 결제와 다음 예정 결제는 `lastPayment`와 `nextPayment` 메서드로 조회 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 `Laravel\Paddle\Payment` 인스턴스를 반환하며, 아직 동기화되지 않은 경우 `null`일 수도 있습니다. 예:

```blade
다음 결제: {{ $nextPayment->amount() }} ({{ $nextPayment->date()->format('d/m/Y') }}) 예정
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시 직접 결제 흐름을 수동으로 확인해 통합이 정상 동작하는지 확인하세요.

자동화 테스트(CI 포함)에서는 [Laravel HTTP 클라이언트](/docs/master/http-client#testing)를 사용해 Paddle에 대한 HTTP 호출을 모킹할 수 있습니다. 이는 Paddle의 실제 응답을 테스트하지는 않지만, Paddle API 호출 없이 애플리케이션 테스트가 가능합니다.