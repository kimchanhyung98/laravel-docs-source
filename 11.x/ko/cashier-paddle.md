# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
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
    - [구독 단일 요금 부과](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [플랜 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험](#subscription-trials)
    - [결제 수단 제출과 함께](#with-payment-method-up-front)
    - [결제 수단 제출 없이](#without-payment-method-up-front)
    - [체험 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle 웹후크 처리](#handling-paddle-webhooks)
    - [웹후크 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹후크 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [상품 청구](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 적립금 지급](#crediting-transactions)
- [거래](#transactions)
    - [지난 결제 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

> [!WARNING]  
> 본 문서는 Cashier Paddle 2.x의 Paddle Billing 연동 문서입니다. Paddle Classic을 사용하고 있다면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 참고하십시오.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 표현적이고 유연한 인터페이스를 제공합니다. 반복적인 구독 결제 코드의 대부분을 간단하게 처리할 수 있습니다. 기본적인 구독 관리뿐만 아니라, Cashier는 구독 변경, 구독 수량, 구독 일시정지, 취소 유예기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 사용하기 전에, Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview) 및 [API 문서](https://developer.paddle.com/api-reference/overview)를 참고하시길 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새로운 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼하게 확인하세요.

<a name="installation"></a>
## 설치

우선 Composer 패키지 관리자를 이용하여 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

다음으로, `vendor:publish` 아티즌 명령어를 사용해 Cashier 마이그레이션 파일을 배포하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션은 새 `customers` 테이블을 생성합니다. 추가로, 모든 고객의 구독 정보를 저장할 `subscriptions` 및 `subscription_items` 테이블이 생성됩니다. 마지막으로, 고객과 연관된 모든 Paddle 거래를 저장하는 `transactions` 테이블도 만들어집니다:

```shell
php artisan migrate
```

> [!WARNING]  
> Cashier가 모든 Paddle 이벤트를 제대로 처리할 수 있도록 반드시 [Cashier의 웹후크 처리 설정](#handling-paddle-webhooks)을 하시기 바랍니다.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 및 스테이징 환경에서 개발할 때는 [Paddle 샌드박스 계정](https://sandbox-login.paddle.com/signup)을 등록하세요. 샌드박스 계정을 통해 실제 결제 없이 애플리케이션을 테스트하고 개발할 수 있습니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card)를 사용해 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

샌드박스 환경을 사용할 때는 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

애플리케이션 개발이 끝난 후에는 [Paddle 벤더 계정](https://paddle.com)을 신청할 수 있습니다. 프로덕션 환경에 배포하기 전에 Paddle팀의 도메인 승인이 필요합니다.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 가능 모델

Cashier를 사용하기 전에 반드시 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 수단 정보 갱신 등 다양한 청구 관련 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자가 아닌 청구 가능한 엔터티가 있을 경우, 해당 클래스에도 트레이트를 추가할 수 있습니다:

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

다음으로, 애플리케이션의 `.env` 파일에 Paddle 키를 설정합니다. Paddle API 키들은 Paddle 관리자 콘솔에서 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

샌드박스 환경을 사용할 때는 `PADDLE_SANDBOX`를 `true`로, 프로덕션에서 실 운영 벤더 환경을 사용할 때는 `false`로 설정하세요.

`PADDLE_RETAIN_KEY`는 옵션이며, [Retain](https://developer.paddle.com/paddlejs/retain) 서비스를 이용하는 경우에만 설정하세요.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 Paddle 체크아웃 위젯을 띄우기 위해 자체 자바스크립트 라이브러리에 의존합니다. 자바스크립트 라이브러리는 애플리케이션 레이아웃의 `</head>` 태그 바로 전에 `@paddleJS` 블레이드 디렉티브를 추가하여 로드할 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

송장 등에서 통화 값을 표시할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용해 통화 로케일을 지정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 이외의 로케일을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치/설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Cashier에서 내부적으로 사용하는 모델을 직접 확장해 사용할 수 있습니다. 아래와 같이 직접 만든 모델이 Cashier의 모델을 상속하도록 하면 됩니다:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

정의한 모델을 Cashier에 적용하려면, 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 지정합니다:

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
### 상품 판매

> [!NOTE]  
> Paddle 체크아웃 사용 전, Paddle 대시보드에서 고정 가격이 있는 상품을 먼저 정의해야 합니다. 그리고 [Paddle 웹후크 처리](#handling-paddle-webhooks)도 반드시 구성하세요.

애플리케이션에서 상품 및 구독 과금 기능을 제공하는 것은 쉽지 않습니다. 하지만 Cashier와 [Paddle의 체크아웃 오버레이](https://www.paddle.com/billing/checkout)를 이용하면 견고한 결제 연동을 쉽게 구축할 수 있습니다.

비정기적(단일결제) 상품의 결제는 Cashier를 통해 Paddle의 체크아웃 오버레이를 띄워 고객이 결제 정보를 입력 및 결제하도록 할 수 있습니다. 결제가 완료되면 고객은 애플리케이션 내의 선택한 성공 URL로 리다이렉트됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제처럼, Cashier의 `checkout` 메서드로 "가격 식별자"에 해당하는 Paddle 체크아웃 오브젝트를 생성합니다. Paddle에서 "가격"은 [특정 상품에 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요시, `checkout` 메서드는 Paddle에 고객을 자동 생성 후, 해당 고객 레코드를 애플리케이션과 연결합니다. 체크아웃 세션이 끝나면 선택한 성공 페이지로 리다이렉션이 됩니다.

`buy` 뷰에서는 오버레이 체크아웃을 띄우는 버튼을 배치하면 됩니다. `paddle-button` 블레이드 컴포넌트는 Cashier에 포함되어 있습니다. 또한 [체크아웃 오버레이를 직접 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle 체크아웃에 메타데이터 추가하기

상품을 판매할 때, 자체적으로 정의한 `Cart`나 `Order` 모델을 이용해 주문내역이나 구입상품을 관리하는 경우가 많습니다. Paddle 체크아웃 오버레이로 고객을 리다이렉트할 때 기존 주문 식별자를 전달해 결제 완료 후 해당 주문과 결제를 연결할 수 있습니다.

이를 위해 `checkout` 메서드에 커스텀 데이터를 배열로 전달하면 됩니다. 예를 들어, 고객이 체크아웃을 시작할 때 애플리케이션에서 `Order`를 생성한다고 가정합시다(단, `Cart`와 `Order` 모델은 Cashier에서 제공하지 않으며, 애플리케이션 환경에 맞게 직접 구현해야 함):

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

이렇게 하면, 고객이 체크아웃을 시작하면 카트/주문의 연관된 Paddle 가격ID를 모두 `checkout`에 넘깁니다. 또한 주문ID도 `customData`로 Paddle 체크아웃에 전달합니다.

고객 결제가 완료되었다면, 주문을 "완료"로 표시해야 할 것입니다. 이를 위해 Paddle의 웹후크로부터 전달받은 이벤트를 Cashier가 이벤트로 발행해주므로, 웹후크 또는 이벤트 리스너에서 데이터베이스의 주문 정보를 갱신할 수 있습니다.

우선, Cashier가 발행하는 `TransactionCompleted` 이벤트를 리스닝하면 됩니다. 보통 애플리케이션의 `AppServiceProvider`의 `boot`에서 이벤트 리스너를 등록합니다:

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

아래는 `CompleteOrder` 리스너 예제입니다:

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * 핸들러
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

`transaction.completed` 이벤트의 상세 데이터는 Paddle 공식 문서를 참고하세요: [관련 가이드](https://developer.paddle.com/webhooks/transactions/transaction-completed)

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]  
> Paddle 체크아웃 사용 전, Paddle 대시보드에서 고정 가격이 있는 상품을 먼저 정의해야 합니다. 또한 [웹후크 처리](#handling-paddle-webhooks)도 반드시 구성하세요.

Cashier와 [Paddle의 체크아웃 오버레이](https://www.paddle.com/billing/checkout)를 사용하면 구독 판매 연동을 간편하게 만들 수 있습니다.

예를 들어, 기본 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 구독 플랜이 있고, 이 두 가격은 Paddle 대시보드의 "Basic" 상품(`pro_basic`) 하위에 묶여 있습니다. 추가적으로 Expert 플랜(`pro_expert`)도 제공할 수 있습니다.

고객이 우리 서비스에 구독하는 흐름을 살펴봅니다. 예를 들어, 가격 페이지에서 Basic 플랜의 "구독" 버튼을 클릭하면 아래와 같이 Paddle 체크아웃 창이 뜹니다:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```

`subscribe` 뷰에서는 체크아웃 오버레이 버튼을 넣을 수 있습니다. Cashier에서는 `paddle-button` 블레이드 컴포넌트가 제공되며, [직접 오버레이 체크아웃을 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

버튼 클릭 시 고객이 결제 정보를 입력하고 구독을 시작할 수 있습니다. 실제로 구독이 시작되었는지 판단하려면(Paddle 카드 결제의 경우 실 결제가 약간 지연될 수 있음) [웹후크 처리 구성](#handling-paddle-webhooks)도 필요합니다.

이제 구독 중 사용자만 특정 부분에 접근할 수 있도록 제한해야 합니다. Cashier의 `Billable` 트레이트로 제공되는 `subscribed` 메서드를 사용하면 됩니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 구독 중인지도 쉽게 알 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 여부 미들웨어 만들기

보다 편리하게, 요청 사용자가 구독 상태인지 확인하는 [미들웨어](/docs/{{version}}/middleware)를 만들 수 있습니다. 만들었다면, 라우트에 적용해 비구독 사용자의 접근을 제한할 수 있습니다:

```php
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
            // 구독 페이지로 리다이렉트
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```

그리고 라우트에 미들웨어로 적용하면 됩니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객의 구독 플랜 관리 허용

고객은 기존 구독 플랜을 다른 상품이나 "등급"으로 변경하고 싶어 할 수 있습니다. 예를 들어, 월간 구독에서 연간 구독으로 변경을 원할 경우 아래처럼 처리할 수 있습니다. 버튼 클릭 시 아래 라우트로 이동하도록 하면 됩니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // 이 예에서는 "$price"가 "price_basic_yearly"임

    return redirect()->route('dashboard');
})->name('subscription.swap');
```

구독 플랜 변경뿐만 아니라, 구독 취소 버튼도 제공해야 합니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```

이렇게 하면, 구독은 결제 주기의 마지막에 취소됩니다.

> [!NOTE]  
> Cashier 웹후크 처리를 구성해두었다면, Paddle로부터 들어오는 웹후크를 바탕으로 Cashier 관련 데이터베이스 테이블이 자동으로 동기화됩니다. 예를 들어, Paddle 대시보드에서 구독을 취소하면 Cashier가 그에 맞는 웹후크를 수신해 구독을 "취소됨"으로 표시합니다.

<a name="checkout-sessions"></a>
## 체크아웃 세션

고객 청구 작업은 대부분 Paddle의 [체크아웃 오버레이 위젯](https://developer.paddle.com/build/checkout/build-overlay-checkout)이나 [인라인 체크아웃](https://developer.paddle.com/build/checkout/build-branded-inline-checkout)을 통해 수행됩니다.

체크아웃 결제 처리를 진행하기 전, 반드시 Paddle 체크아웃 설정 대시보드에서 [기본 결제 링크](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link)를 설정해두세요.

<a name="overlay-checkout"></a>
### 오버레이 체크아웃

Paddle의 체크아웃 오버레이 위젯을 띄우기 전에, Cashier를 이용해 체크아웃 세션을 먼저 생성해야 합니다. 체크아웃 세션은 위젯에 과금 작업을 알려줍니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

Cashier는 `paddle-button` [블레이드 컴포넌트](/docs/{{version}}/blade#components)를 제공합니다. 체크아웃 세션을 prop으로 전달하면 버튼 클릭 시 Paddle의 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

기본적으로 Paddle의 기본 스타일링으로 표시되지만, [Paddle이 지원하는 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 추가해 위젯을 커스터마이징할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```

Paddle 체크아웃 위젯은 비동기식입니다. 사용자가 위젯에서 구독을 생성하면 Paddle은 웹후크로 애플리케이션에 알려주므로, 데이터베이스의 구독 상태를 맞게 갱신하도록 웹후크를 [반드시 설정](#handling-paddle-webhooks)해야 합니다.

> [!WARNING]  
> 구독 상태가 변경되면 관련 웹후크 수신이 대부분 즉시로 끝나지만, 체크아웃 완료 후 바로 구독이 활성화되지 않을 수 있으니 애플리케이션에서 이에 대한 처리를 고려하세요.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 체크아웃 수동 렌더링

라라벨의 내장 블레이드 컴포넌트 없이도 오버레이 체크아웃을 직접 렌더링할 수 있습니다. 우선 [체크아웃 세션 생성 방식](#overlay-checkout)은 동일합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

다음으로, Paddle.js를 통해 체크아웃을 초기화할 수 있습니다. 아래는 `paddle_button` 클래스를 할당한 링크를 만들고, Paddle.js가 해당 클래스를 감지하여 클릭 시 체크아웃 오버레이를 표시하는 예시입니다:

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

Paddle의 "오버레이" 스타일 체크아웃 위젯 대신, 위젯을 페이지 내에 직접 포함(임베드)시킬 수도 있습니다. HTML 필드를 임의로 조정할 수는 없지만, 애플리케이션 내에 직접 위젯을 삽입할 수 있습니다.

Cashier는 인라인 체크아웃을 쉽게 구현하도록 `paddle-checkout` 블레이드 컴포넌트를 제공합니다. 우선 [체크아웃 세션을 생성](#overlay-checkout)합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```

그 다음, 컴포넌트의 `checkout` 속성에 세션을 전달하여 사용하세요:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

인라인 컴포넌트의 높이는 `height` 속성으로 조정할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

인라인 체크아웃의 커스터마이징 관련 정보는 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) 및 [설정 문서](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)를 참고하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

라라벨의 내장 블레이드 컴포넌트를 사용하지 않고 직접 인라인 체크아웃을 구현할 수도 있습니다. 방식은 [기존 예시](#inline-checkout)와 동일하게 체크아웃 세션을 생성한 후 Paddle.js에서 열 수 있습니다. 아래 예시는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용했으나, 프론트엔드 환경에 맞게 수정해서 쓰시면 됩니다:

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
### 비회원 체크아웃

애플리케이션 계정이 없는 사용자를 위한 체크아웃 세션을 생성하는 경우, `guest` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

체크아웃 세션을 생성했다면 [Paddle 버튼](#overlay-checkout)이나 [인라인 체크아웃](#inline-checkout) 블레이드 컴포넌트에도 전달할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기

Paddle은 통화별로 가격을 커스터마이즈할 수 있어, 국가마다 다른 가격을 설정할 수 있습니다. Cashier Paddle은 `previewPrices` 메서드를 통해 모든 가격을 조회할 수 있습니다. 조회할 가격ID를 배열로 넘기면 됩니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

통화는 요청의 IP 주소에 따라 결정되나, 특정 국가의 가격을 조회하려면 옵션으로 국가 코드를 직접 전달하세요:

```php
$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```

가격을 조회했다면, 자유롭게 표시하면 됩니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```

부가세 등은 아래처럼 별도 표시 가능합니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```

자세한 내용은 Paddle [API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객별 가격 미리보기

이미 Paddle 고객으로 등록된 사용자가 있으면, 해당 고객에게 적용되는 가격을 직접 조회할 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

내부적으로 Cashier는 사용자의 고객ID를 Paddle에 전달하여, 고객 거주 국가의 통화에 맞는 가격을 받아옵니다. 미국 사용자는 달러, 벨기에 사용자는 유로 등으로 자동 처리됩니다. 일치하는 통화를 찾지 못하면 상품의 기본 통화가 사용되며, 모든 가격은 Paddle 대시보드에서 관리할 수 있습니다.

<a name="price-discounts"></a>
### 할인

미리보기 가격에 할인도 적용할 수 있습니다. `previewPrices` 메서드 호출 시 `discount_id` 옵션으로 할인ID를 넘기면 됩니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```

계산된 가격을 표시하세요:

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

Cashier에서는 고객의 이메일 및 이름 같은 일부 기본값을 미리 채울 수 있습니다. 고객 모델에서 아래 메서드를 오버라이드하면, 체크아웃 세션에서 자동으로 반영됩니다:

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

이 기본값은 [체크아웃 세션](#checkout-sessions)을 생성하는 모든 Cashier 액션에서 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

Paddle 고객ID로 고객을 조회할 때는 `Cashier::findBillable` 메서드를 사용하세요. 청구 가능 모델 인스턴스가 반환됩니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔 구독을 시작하지 않고 Paddle 고객만 생성하고 싶을 수 있습니다. 이 경우 `createAsCustomer` 메서드를 사용하세요:

```php
$customer = $user->createAsCustomer();
```

`Laravel\Paddle\Customer` 인스턴스가 반환됩니다. 이후 언제든 구독을 시작할 수 있습니다. 추가 옵션은 [Paddle 고객 생성 API 문서](https://developer.paddle.com/api-reference/customers/create-customer)에서 확인 가능합니다:

```php
$customer = $user->createAsCustomer($options);
```

<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면, 데이터베이스에서 고객 모델 인스턴스를 먼저 가져옵니다. 일반적으로 `App\Models\User`일 것입니다. 그 다음 `subscribe` 메서드로 체크아웃 세션을 만듭니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 12345, 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscribe`의 첫 번째 인자는 구독할 가격ID(Paddle 내 가격 식별자)이며, `returnTo` 메서드는 결제 완료 후 리다이렉트할 URL입니다. 두 번째 인자는 구독의 내부 구분명으로, 앱 내에서만 사용되며 빈칸을 포함하면 안 됩니다(생성 후 변경 금지).

구독과 연관된 추가 정보를 넘기고 싶다면 `customData`로 배열을 넘기세요:

```php
$checkout = $request->user()->subscribe($premium = 12345, 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```

생성한 체크아웃 세션은 [오버레이 체크아웃 블레이드 컴포넌트](#overlay-checkout)로 전달하여 버튼 렌더링에 사용할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```

결제 완료 후 Paddle은 `subscription_created` 웹후크를 보내며, Cashier는 이를 받아 고객 구독을 세팅합니다. 웹후크가 누락 없이 수신/처리되도록 [웹후크 처리 구성을 반드시 확인](#handling-paddle-webhooks)하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

구독 후 사용자의 구독 상태를 손쉽게 여러 메서드로 확인할 수 있습니다. `subscribed` 메서드는 사용자가 유효한 구독 중(체험 기간 포함)이면 `true`를 반환합니다:

```php
if ($user->subscribed()) {
    // ...
}
```

구독이 여러 개인 경우, 구독 타입을 인자로 전달하세요:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [미들웨어](/docs/{{version}}/middleware)로 사용하여 사용자 구독 상태에 따라 라우트/컨트롤러 접근을 필터링할 수 있습니다:

```php
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
            // 유료고객이 아님...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

체험(trial) 기간 중인지 확인하려면, `onTrial` 메서드를 사용하세요. 경고 메시지 등에 활용할 수 있습니다:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```

특정 Paddle 가격ID로 구독 중인지 확인하려면 `subscribedToPrice` 메서드를 사용할 수 있습니다:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```

체험/유예 기간이 아닌 상태의 활성 구독인 경우는 `recurring` 메서드로 확인합니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```

<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

이전에 구독했던 사용자가 구독을 취소했는지 여부는 `canceled` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```

구독을 취소했지만 "유예기간" 내(즉, 아직 완전히 만료되기 전)인지 확인하려면 `onGracePeriod` 메서드를 사용하세요. 이 기간 중에도 `subscribed`는 `true`를 반환합니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

<a name="past-due-status"></a>
#### 연체 상태

구독 결제 실패 시 상태가 `past_due`로 표시됩니다. 이 경우 결제 정보가 갱신되기 전까지 구독이 활성화되지 않습니다. `pastDue` 메서드로 연체인지 확인할 수 있습니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```

연체 시 [결제 정보 업데이트 안내](#updating-payment-information)를 권장하세요.

연체 상태에서도 구독을 유효로 간주하고 싶다면, 보통 `AppServiceProvider`의 `register`에서 `keepPastDueSubscriptionsActive` 메서드를 호출하세요:

```php
use Laravel\Paddle\Cashier;

/**
 * 서비스 등록
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```

> [!WARNING]  
> 연체(`past_due`) 상태에서는 구독 변경이 불가능합니다. 이 상태에서 `swap`이나 `updateQuantity` 메서드를 호출하면 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 범위(스코프)

대부분의 구독 상태는 쿼리 스코프로도 제공되어, 데이터베이스에서 상태별로 손쉽게 조회할 수 있습니다:

```php
// 모든 정상 구독 조회
$subscriptions = Subscription::query()->valid()->get();

// 해당 사용자의 취소된 구독들 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

아래는 사용 가능한 스코프 목록입니다:

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
### 구독 단일 요금 부과

구독자에게 추가 단일요금을 부과할 수 있습니다. `charge` 메서드에 하나 이상의 가격ID를 넘깁니다:

```php
// 한 가지 요금만 청구
$response = $user->subscription()->charge('pri_123');

// 여러 가지 요금을 한 번에 청구
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

이때 실제 요금 부과는 다음 청구 주기에서 이루어집니다. 바로 청구하려면 `chargeAndInvoice` 메서드를 사용하세요:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```

<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 구독별로 결제 정보를 저장합니다. 고객이 구독의 기본 결제 수단을 변경하려면, 구독 모델의 `redirectToUpdatePaymentMethod` 메서드를 사용해 Paddle의 안내 페이지로 보내세요:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```

결제수단 갱신 후 Paddle이 `subscription_updated` 웹후크를 발행하면 Cashier가 데이터베이스의 구독 정보를 갱신합니다.

<a name="changing-plans"></a>
### 플랜 변경

기존 구독자가 다른 계획으로 변경(업그레이드 등)하고자 한다면, 구독의 `swap` 메서드에 Paddle 가격ID를 넘기면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```

즉시 요금을 청구하고 싶다면 `swapAndInvoice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

<a name="prorations"></a>
#### 요금 비례청구(Proration)

기본적으로 Paddle은 플랜 변경 시 비례청구(proration)를 적용합니다. 요금 비례청구 없이 구독 정보를 수정하려면 `noProrate` 메서드를 체인하세요:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

프러레이션 없이 바로 요금 청구도 가능합니다:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

프러레이션 없이 청구 변경만 하고 싶으면 `doNotBill`을 사용하세요:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

자세한 프러레이션 정책은 Paddle [공식 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참고하세요.

<a name="subscription-quantity"></a>
### 구독 수량

구독이 "수량"(예: 프로젝트 수 1개당 요금)을 기반으로 하는 경우, `incrementQuantity`, `decrementQuantity`로 간편하게 수량 증감이 가능합니다:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// 5개씩 추가
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// 5개씩 차감
$user->subscription()->decrementQuantity(5);
```

`updateQuantity`로 특정 수량을 직접 지정할 수도 있습니다:

```php
$user->subscription()->updateQuantity(10);
```

또한 비례과금 없이 수량을 변경하려면:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독의 수량 조정

[다중 상품 구독](#subscriptions-with-multiple-products)에서는 수량을 조정할 가격ID를 두 번째 인자로 넘기세요:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독

[다중 상품 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)은 여러 결제 상품을 하나의 구독에 할당할 수 있게 해줍니다. 예를 들어, 기본 구독 $10/월에 채팅 추가기능 $15/월을 별도 과금하는 경우가 있습니다.

구독 체크아웃 세션 생성 때 가격ID 배열을 첫 번째 인자로 넘기세요:

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

위 예시에서는 고객의 `default` 구독에 두 가지 가격이 함께 부여됩니다. 각 가격별로 수량 또는 키/값 쌍을 지정하려면:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

기존 구독에 다른 가격을 추가하고 싶다면 `swap` 메서드를 써야 합니다. 이 때 기존 가격/수량 전체를 포함시켜야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

즉시 과금하려면 `swapAndInvoice`:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

가격을 제거하려면 제거할 가격을 누락시켜 `swap`에 전달하세요:

```php
$user->subscription()->swap(['price_original' => 2]);
```

> [!WARNING]  
> 구독의 마지막 가격은 제거할 수 없습니다. 대신 구독을 취소하세요.

<a name="multiple-subscriptions"></a>
### 다중 구독

Paddle은 고객이 동시에 여러 구독을 가질 수 있게 합니다. 예를 들어 수영 구독, 웨이트 구독 등 여러 요금제가 있을 수 있습니다.

구독 생성 시 `subscribe`의 두 번째 인자에 구독 종류를 아무 문자열로든 넘길 수 있습니다(예: "swimming"):

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```

이후 플랜 변경 시 구독 종류를 지정하여 사용합니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

구독 전체 취소도 가능합니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="pausing-subscriptions"></a>
### 구독 일시정지

구독을 일시정지하려면, 구독 인스턴스의 `pause`를 호출하세요:

```php
$user->subscription()->pause();
```

일시정지 시, Cashier는 데이터베이스의 `paused_at` 컬럼을 자동으로 설정합니다. 고객이 예를 들어 3월 1일에 일시정지 요청했으나 실제 결제 갱신일이 3월 5일이라면, 그 전까진 `paused`가 false이며 3월 5일부터 true가 됩니다.

일반적으로, 고객이 결제 기간 동안에는 계속 사용할 수 있게 하므로 다음 결제 주기에 일시정지 처리가 됩니다. 즉시 일시정지를 원하면 `pauseNow`를 쓰세요:

```php
$user->subscription()->pauseNow();
```

정확한 시점까지 일시정지하려면:

```php
$user->subscription()->pauseUntil(now()->addMonth());
```

즉시 특정 시점까지 일시정지:

```php
$user->subscription()->pauseNowUntil(now()->addMonth());
```

유예기간(즉, 결제가 끝난 후에도 잠시 이용 중)인지 확인하려면:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```

일시정지된 구독을 재개하려면 `resume`을 호출하세요:

```php
$user->subscription()->resume();
```

> [!WARNING]  
> 일시정지된 상태에서는 구독 변경이 불가합니다. 플랜 변경이나 수량 업데이트 전엔 반드시 구독을 재개하세요.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독을 취소하려면, 구독 인스턴스의 `cancel`을 호출하세요:

```php
$user->subscription()->cancel();
```

취소 시, Cashier는 데이터베이스의 `ends_at` 컬럼을 설정합니다. 고객이 3월 1일에 취소 요청해도 실제 만료일(예: 3월 5일)까지는 계속 이용할 수 있으므로, 그때까지는 `subscribed`도 true로 남습니다.

유예기간 내 취소 여부는 아래처럼 확인하세요:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow`를 호출하세요:

```php
$user->subscription()->cancelNow();
```

유예기간 중인 취소를 정지하려면 `stopCancelation`을 호출하세요:

```php
$user->subscription()->stopCancelation();
```

> [!WARNING]  
> Paddle 구독은 한 번 취소 후 재개할 수 없습니다. 고객이 다시 서비스를 원하면 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험

<a name="with-payment-method-up-front"></a>
### 결제 수단 제출과 함께

체험 기간 동안 결제 수단을 미리 받고자 하는 경우, Paddle 대시보드에서 해당 가격에 체험 기간을 설정한 후 평소처럼 체크아웃 세션을 만드세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

`subscription_created` 이벤트 수신 시, Cashier는 구독 레코드에 체험 종료일을 저장하고 Paddle에도 해당일까지 청구하지 않도록 지시합니다.

> [!WARNING]  
> 체험 기간이 끝나기 전에 구독을 취소하지 않으면 체험이 끝나는 즉시 요금이 청구되므로, 사용자에게 체험 종료일을 반드시 고지하세요.

체험 중인지 확인하려면 사용자 또는 구독 인스턴스의 `onTrial` 메서드를 사용하세요:

```php
if ($user->onTrial()) {
    // ...
}

if ($user->subscription()->onTrial()) {
    // ...
}
```

기존 체험이 만료되었는지는 `hasExpiredTrial`로 확인합니다:

```php
if ($user->hasExpiredTrial()) {
    // ...
}

if ($user->subscription()->hasExpiredTrial()) {
    // ...
}
```

특정 구독 유형에 대해 체험 여부/만료 여부를 확인하려면 타입을 인자로 넘기세요:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```

<a name="without-payment-method-up-front"></a>
### 결제 수단 제출 없이

결제 수단 없이 체험 기간을 제공하려면, 사용자의 고객 레코드의 `trial_ends_at`에 원하는 날짜를 지정하세요. 일반적으로 회원가입 시에 처리합니다:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->addDays(10)
]);
```

이러한 체험을 Cashier에서는 "일반(Generic) 체험"이라고 부릅니다. 체험 중이면 `onTrial`이 true를 반환합니다:

```php
if ($user->onTrial()) {
    // 사용자가 체험 중
}
```

실제 구독을 시작할 준비가 되면 평소처럼 `subscribe`를 사용하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```

체험 종료일은 `trialEndsAt` 메서드로 얻을 수 있습니다. 특정 구독 유형은 옵션 파라미터로 전달하세요:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```

단순히 "일반(Generic) 체험" 중인지 판단하려면 `onGenericTrial`을 사용하세요:

```php
if ($user->onGenericTrial()) {
    // 일반체험 중
}
```

<a name="extend-or-activate-a-trial"></a>
### 체험 연장/즉시 활성화

기존 구독 체험을 연장하려면 `extendTrial`을 사용합니다:

```php
$user->subscription()->extendTrial(now()->addDays(5));
```

즉시 구독을 활성화(체험 종료)하려면 `activate`를 호출합니다:

```php
$user->subscription()->activate();
```

<a name="handling-paddle-webhooks"></a>
## Paddle 웹후크 처리

Paddle은 다양한 이벤트를 웹후크를 통해 애플리케이션에 알릴 수 있습니다. 기본적으로 Cashier 서비스프로바이더가 Cashier 웹후크 컨트롤러로 연결된 라우트를 자동 등록합니다.

이 컨트롤러는 과금 실패로 인한 구독 취소, 구독/결제 정보 갱신 등 기본적인 웹후크 처리를 자동 수행합니다. 별도 웹후크 이벤트 처리가 필요하다면 아래처럼 직접 핸들러를 확장할 수 있습니다.

애플리케이션이 Paddle 웹후크를 수신할 수 있도록 [Paddle 콘솔에서 웹후크 URL을 반드시 구성](https://vendors.paddle.com/alerts-webhooks)하세요. 기본적으로 `/paddle/webhook` 경로가 사용됩니다. 반드시 활성화해야 할 웹후크는 다음과 같습니다:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]  
> Cashier의 포함 미들웨어를 통해 [웹후크 서명 검증](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures)도 꼭 사용하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹후크와 CSRF 보호

Paddle 웹후크가 라라벨의 [CSRF 보호](/docs/{{version}}/csrf)를 우회할 수 있도록 `paddle/*` 경로를 CSRF 예외로 등록해야 합니다. 보통 `bootstrap/app.php` 파일에서 지정합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'paddle/*',
    ]);
})
```

<a name="webhooks-local-development"></a>
#### 로컬 개발 환경의 웹후크

로컬 개발 환경에서 웹후크 수신을 위해 [Ngrok](https://ngrok.com/), [Expose](https://expose.dev/docs/introduction) 등 서비스를 활용해야 합니다. [Laravel Sail](/docs/{{version}}/sail) 환경에서는 [사이트 공유 명령](/docs/{{version}}/sail#sharing-your-site)을 참고하세요.

<a name="defining-webhook-event-handlers"></a>
### 웹후크 이벤트 핸들러 정의

Cashier는 결제 실패로 인한 구독 취소 등 대부분의 Paddle 웹후크를 자동 처리합니다. 추가로 처리할 웹후크가 있다면 아래 이벤트를 리스닝할 수 있습니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

둘 다 Paddle 웹후크의 전체 페이로드를 포함합니다. 예를 들어 `transaction.billed` 웹후크를 처리하려면 [이벤트 리스너](/docs/{{version}}/events#defining-listeners)를 등록하세요:

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Paddle 웹후크 처리
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // 처리 작업
        }
    }
}
```

Cashier는 웹후크 타입별 전용 이벤트도 발행합니다. Paddle 페이로드 외에도 관련 모델(청구모델, 구독, 영수증 등)도 포함합니다:

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

기본 내장 웹후크 라우트를 재정의할 땐 `.env`의 `CASHIER_WEBHOOK` 환경 변수를 설정하세요. Paddle 대시보드의 URL과 정확히 일치해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

<a name="verifying-webhook-signatures"></a>
### 웹후크 서명 검증

웹후크 보안을 위해 [Paddle의 웹후크 서명](https://developer.paddle.com/webhook-reference/verifying-webhooks) 기능을 사용할 수 있습니다. Cashier에는 이를 위한 미들웨어가 내장되어 있어 별도 처리 없이 사용할 수 있습니다.

웹후크 검증 활성화는 `.env` 파일에 `PADDLE_WEBHOOK_SECRET`를 지정하면 됩니다. 해당 값은 Paddle 콘솔에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 청구

<a name="charging-for-products"></a>
### 상품 청구

고객에게 상품 결제를 유도하고 싶다면, 청구가능 모델 인스턴스의 `checkout` 메서드로 체크아웃 세션을 생성하세요. 가격ID 배열/수량도 지정 가능합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```

세션 생성 후 [오버레이 체크아웃 블레이드 컴포넌트](#overlay-checkout)를 사용해 Paddle 체크아웃 위젯을 띄웁니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```

`customData` 메서드로 트랜잭션 생성시 커스텀 옵션도 전달 가능합니다. 자세한 옵션은 [Paddle 공식문서](https://developer.paddle.com/build/transactions/custom-data) 참고:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```

<a name="refunding-transactions"></a>
### 거래 환불

환불은 구매에 사용한 결제수단으로 환급됩니다. 특정 거래를 환불하려면 `Cashier\Paddle\Transaction` 모델의 `refund` 메서드를 사용하세요. 첫 번째 인자는 사유, 두 번째는 환불할 가격ID와 금액(없으면 전부 환불)입니다.

예를 들어, `pri_123`은 전액, `pri_456`은 일부만 환불하는 법:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // 전액 환불
    'pri_456' => 200, // 일부 환불
]);
```

전체 트랜잭션 환불은 이유만 넘기면 됩니다:

```php
$response = $transaction->refund('Accidental charge');
```

자세한 내용은 [Paddle 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments) 참고.

> [!WARNING]  
> 환불은 Paddle의 승인을 받아야 완료됩니다.

<a name="crediting-transactions"></a>
### 거래 적립금 지급(크레딧)

환불처럼 거래에 크레딧을 지급할 수도 있습니다. 이 방법은 고객이 다음 결제에 사용할 수 있는 잔고를 추가합니다. 수동 결제 거래에만 가능하며, 자동 결제(구독 등)는 Paddle이 크레딧을 자동 관리합니다:

```php
$transaction = $user->transactions()->first();

// 특정 항목 전액 크레딧 지급
$response = $transaction->credit('Compensation', 'pri_123');
```

자세한 내용은 [Paddle 크레딧 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참고하세요.

> [!WARNING]  
> 크레딧은 수동 결제 거래에만 적용할 수 있습니다. 자동 결제 거래는 Paddle이 크레딧을 자동 처리합니다.

<a name="transactions"></a>
## 거래

청구가능 모델의 거래 내역은 `transactions` 프로퍼티로 쉽게 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```

거래는 상품 및 구매 결제를 의미하며, 송장도 함께 생성됩니다. 완료된 거래만 데이터베이스에 저장됩니다.

거래를 나열할 때 전용 메서드로 결제정보를 표시할 수 있습니다. 사용자에게 거래 내역을 표로 나열하고 영수증 다운로드를 제공하는 경우:

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

`download-invoice` 라우트는 다음과 같이 구현할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```

<a name="past-and-upcoming-payments"></a>
### 지난 결제 및 예정 결제

`lastPayment`와 `nextPayment` 메서드로 구독의 지난 결제와 예정 결제를 각각 조회 및 표시할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```

두 메서드는 `Laravel\Paddle\Payment` 인스턴스를 반환하지만, 트랜잭션 동기화 전엔 `lastPayment`는 `null`이고, 빌링 주기가 끝난 경우(예: 구독 취소)엔 `nextPayment`가 `null`입니다.

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트

실제 결제 흐름은 수동으로 충분히 테스트하여 정상동작 여부를 반드시 확인하세요.

자동화 테스트(예: CI)에서는 [라라벨 HTTP 클라이언트](/docs/{{version}}/http-client#testing)로 Paddle에 대한 HTTP 요청을 페이크 처리할 수 있습니다. Paddle 응답을 실제로 테스트하는 것은 아니지만 연동 없이 앱 로직을 확인할 수 있습니다.