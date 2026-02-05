# Laravel Cashier (Stripe) (Laravel Cashier (Stripe))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [청구 모델 설정](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로그 설정](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔액(Balances)](#balances)
    - [Tax ID(세금식별자)](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [결제 포털(Billing Portal)](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부 확인](#payment-method-presence)
    - [기본 결제 수단 갱신](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 제품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 Anchor Date](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 트라이얼](#subscription-trials)
    - [선결제 트라이얼](#with-payment-method-up-front)
    - [결제 정보 없는 트라이얼](#without-payment-method-up-front)
    - [트라이얼 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [단순 결제](#simple-charge)
    - [인보이스 사용 결제](#charge-with-invoice)
    - [결제 인텐트 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스 확인](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [제품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [Tax ID 수집](#collecting-tax-ids)
    - [게스트 Checkout](#guest-checkouts)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK 사용](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 쉽게 사용할 수 있도록 직관적이고 유연한 인터페이스를 제공합니다. Cashier는 귀찮은 구독 및 빌링 관련 보일러플레이트 코드를 거의 대부분 자동으로 처리해줍니다. 기본적인 구독 관리 외에도, 쿠폰 적용, 구독 상품 교체, 구독 수량 관리, 취소 유예 기간 설정, 인보이스 PDF 생성 등 다양한 기능을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼하게 검토하시기 바랍니다.

> [!WARNING]
> Cashier는 주요 변경으로 인한 문제를 방지하기 위해 Stripe API 버전을 고정하여 사용합니다. Cashier 16 버전은 Stripe API `2025-06-30.basil` 버전을 사용합니다. Stripe API 버전은 Stripe의 새로운 기능 및 개선 사항을 사용하기 위해 마이너 릴리즈에서 갱신될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 이용하여 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier
```

패키지를 설치한 후, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음 데이터베이스를 마이그레이션합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하며, 모든 고객의 구독 정보를 저장하는 `subscriptions` 테이블과 다중 가격 구독 항목을 저장하는 `subscription_items` 테이블을 새로 생성합니다.

필요하다면 Cashier의 설정 파일도 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로 Stripe 이벤트 처리를 위해 반드시 [Cashier의 webhook 처리를 설정](#handling-stripe-webhooks)해야 합니다.

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장할 컬럼이 대소문자를 구분하도록 권장하고 있습니다. MySQL 사용하는 경우 `stripe_id` 컬럼의 컬레이션(collation)을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 모델 설정 (Billable Model)

Cashier를 사용하기 전에, 청구를 담당할 모델에 `Billable` 트레이트를 추가하세요. 일반적으로 `App\Models\User` 모델에 추가합니다. 이 트레이트를 통해 구독 생성, 쿠폰 적용, 결제 수단 정보 갱신 등과 같은 주요 결제 업무 메서드를 사용할 수 있습니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 `App\Models\User` 클래스를 청구 모델로 가정합니다. 만약 이를 변경하고 싶다면 `useCustomerModel` 메서드를 이용해 다른 모델을 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel의 기본 `App\Models\User` 모델이 아닌 다른 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시한 다음 해당 모델의 테이블명에 맞게 변경해야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

`.env` 파일에 Stripe API 키를 설정해야 합니다. Stripe API 키는 Stripe 관리자 페이지에서 발급받을 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `.env` 파일에 반드시 `STRIPE_WEBHOOK_SECRET` 환경 변수를 정의해야 합니다. 이 변수는 Stripe에서 전송하는 webhook이 실제로 Stripe에서 온 것인지 보장하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. `.env` 파일에서 `CASHIER_CURRENCY` 변수를 변경하여 기본 통화를 설정할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

통화 설정 외에도 인보이스 등에서 금액을 표시할 때 사용할 로케일(locale)도 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en`이 아닌 다른 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 이용하면 Stripe가 생성하는 모든 인보이스에 대해 세금을 자동으로 계산할 수 있습니다. 자동 세금 계산을 사용하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

이렇게 설정하면 새로 생성되는 구독과 일회성 인보이스에 대해 자동으로 세금이 계산됩니다.

이 기능이 올바르게 작동하려면, 고객의 청구 정보(이름, 주소, Tax ID 등)가 Stripe와 동기화되어 있어야 합니다. Cashier가 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 활용할 수 있습니다.

<a name="logging"></a>
### 로그 설정 (Logging)

Cashier에서는 Stripe의 심각한 오류를 로깅할 로그 채널을 지정할 수 있습니다. `.env` 파일의 `CASHIER_LOGGER` 변수로 설정합니다:

```ini
CASHIER_LOGGER=stack
```

API 호출 중 발생한 예외는 애플리케이션의 기본 로그 채널에도 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier 내부에서 사용하는 기본 모델을 확장하여 자체 모델을 정의할 수 있습니다. 아래처럼 Cashier의 모델을 상속받아 사용하세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 뒤, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 Cashier에 커스텀 모델을 알려줄 수 있습니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

<a name="quickstart-selling-products"></a>
### 제품 판매 (Selling Products)

> [!NOTE]
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에 고정 가격의 제품(Products)을 정의해야 합니다. 또한, [Cashier의 webhook 처리](#handling-stripe-webhooks)도 반드시 설정해야 합니다.

애플리케이션을 통해 제품과 구독을 판매하는 것은 복잡할 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 쉽고 현대적인 결제 시스템을 손쉽게 구축할 수 있습니다.

비정기적, 단일 결제 방식의 상품을 판매하려면, Cashier를 사용해 고객을 Stripe Checkout으로 리디렉션합니다. 고객이 Checkout을 통해 결제를 완료하면 지정한 성공 URL로 다시 돌아오게 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/checkout', function (Request $request) {
    $stripePriceId = 'price_deluxe_album';

    $quantity = 1;

    return $request->user()->checkout([$stripePriceId => $quantity], [
        'success_url' => route('checkout-success'),
        'cancel_url' => route('checkout-cancel'),
    ]);
})->name('checkout');

Route::view('/checkout/success', 'checkout.success')->name('checkout-success');
Route::view('/checkout/cancel', 'checkout.cancel')->name('checkout-cancel');
```

위 예제처럼 `checkout` 메서드를 이용해 특정 "가격 식별자"로 고객을 Stripe Checkout에 보냅니다. Stripe에서 "price"란 [제품별로 정의된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요한 경우, `checkout` 메서드는 Stripe에 고객을 자동으로 생성하고, 이를 애플리케이션의 사용자와 연결합니다. Checkout 세션이 완료되면 고객은 지정한 성공/취소 페이지로 리디렉션됩니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타 데이터 제공하기

제품을 판매할 때, 각 주문을 트래킹하거나 주문 모델을 별도로 관리하고 싶을 수 있습니다. Stripe Checkout으로 리디렉션할 때 기존 주문 ID 등 메타 데이터를 함께 넘기면, 고객이 결제를 마치고 돌아올 때 결제 내역과 주문을 매칭할 수 있습니다.

이를 위해 `checkout` 메서드에 `metadata` 배열을 전달할 수 있습니다. 아래는 사용자가 결제 프로세스를 시작할 때 애플리케이션에 임시 `Order` 객체를 생성하는 예시입니다(여기서 `Cart`와 `Order` 모델은 Cashier가 직접 제공하지 않습니다):

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

    return $request->user()->checkout($order->price_ids, [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
        'metadata' => ['order_id' => $order->id],
    ]);
})->name('checkout');
```

위처럼 결제 과정에서 관련 price id와 order id를 함께 전달할 수 있습니다. 성공 페이지의 URL 쿼리에 `CHECKOUT_SESSION_ID`를 포함시키면, Stripe가 해당 세션 ID로 실제 값을 자동으로 채워줍니다.

이제 성공 페이지 라우트를 구현해보겠습니다. Stripe Checkout에서 결제가 성공하면 사용자는 이 라우트로 돌아오고, Stripe Checkout 세션 정보를 조회할 수 있습니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;
use Laravel\Cashier\Cashier;

Route::get('/checkout/success', function (Request $request) {
    $sessionId = $request->get('session_id');

    if ($sessionId === null) {
        return;
    }

    $session = Cashier::stripe()->checkout->sessions->retrieve($sessionId);

    if ($session->payment_status !== 'paid') {
        return;
    }

    $orderId = $session['metadata']['order_id'] ?? null;

    $order = Order::findOrFail($orderId);

    $order->update(['status' => 'completed']);

    return view('checkout-success', ['order' => $order]);
})->name('checkout-success');
```

Checkout 세션 오브젝트에 포함된 데이터에 대한 자세한 정보는 [Stripe 공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에 고정 가격의 제품(Products)을 정의해야 합니다. 또한, [Cashier의 webhook 처리](#handling-stripe-webhooks)도 반드시 설정해야 합니다.

애플리케이션을 통한 구독 결제도 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 쉽고 안전하게 구현할 수 있습니다.

Cashier와 Stripe Checkout을 이용해 구독 서비스를 제공하는 가장 기본적인 시나리오를 살펴보겠습니다. 예를 들어, 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 구독 상품이 있다고 가정합니다(둘 다 Stripe 대시보드에서 "Basic"이라는 제품으로 묶을 수 있습니다). 이외에도 "Expert"와 같이 추가 요금제가 있을 수 있습니다.

먼저 한 명의 사용자가 구독을 시작하는 프로세스를 살펴봅니다. 사용자가 요금제 페이지에서 "등록" 버튼을 누르면 아래와 같이 Stripe Checkout 세션을 만드세요:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_basic_monthly')
        ->trialDays(5)
        ->allowPromotionCodes()
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

위 예제처럼 `newSubscription` 메서드를 이용해 Stripe Checkout 세션을 생성합니다. 결제 성공 또는 취소 후에는 지정한 URL로 리디렉션되며, 구독이 실제로 활성화되었는지는 일부 결제 방식에서는 약간의 지연이 있을 수 있으므로 [webhook 처리](#handling-stripe-webhooks)도 반드시 필요합니다.

구독이 시작된 후에는 Cashier의 `Billable` 트레이트에서 제공하는 `subscribed` 메서드를 통해 구독 여부를 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 제품 또는 가격에 가입했는지 여부도 확인 가능합니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 여부를 체크하는 미들웨어 만들기

편의상 요청 사용자가 유효한 구독자인지 확인하는 [미들웨어](/docs/master/middleware)를 만들어 특정 라우트에 적용할 수 있습니다:

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
            // 구독 페이지로 리디렉션
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

이 미들웨어를 라우트에 지정하면, 미구독자는 해당 라우트 접근 시 빌링 페이지로 리디렉션하게 할 수 있습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 직접 요금제를 관리하도록 허용

고객이 스스로 구독 요금제(또는 티어)를 변경하고 싶어 할 수 있습니다. Stripe의 [고객 결제 포털(Customer Billing Portal)](https://stripe.com/docs/no-code/customer-portal)을 사용하면, 고객이 인보이스 다운로드, 결제 수단 변경, 구독 변경 등을 할 수 있는 UI를 Stripe가 호스팅합니다.

애플리케이션에서 다음과 같이 결제 포털로 이동하는 링크 혹은 버튼을 만들어주세요:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

그리고 Stripe의 Customer Billing Portal 세션을 시작하고 사용자를 포털로 리디렉션하는 Laravel 라우트를 구현합니다. `redirectToBillingPortal` 메서드는 포털에서 나올 때 돌아올 URL을 인자로 받습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 webhook 처리가 설정되어 있다면, Stripe 포털에서 사용자가 구독을 해지하는 경우에도 Cashier가 webhook 이벤트를 감지하여 애플리케이션의 데이터베이스 구독 상태를 자동으로 "취소됨"으로 동기화해줍니다.

... (중략: 이어서 전체 문서를 계속 번역하여 출력해야 함. 질문에 용량 제한이 있으므로, 필요시 이어서 번역 요청 가능합니다.)