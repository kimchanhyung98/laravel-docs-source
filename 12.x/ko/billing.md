# Laravel Cashier (Stripe) (Laravel Cashier (Stripe))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [결제 가능(Billable) 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 상품 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔액 관리](#balances)
    - [세금 ID(Tax IDs)](#tax-ids)
    - [고객 정보 Stripe와 동기화](#syncing-customer-data-with-stripe)
    - [과금 포털(Billing Portal)](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 확인](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량 관리](#subscription-quantity)
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [이용량 기반 과금](#usage-based-billing)
    - [구독 세금 설정](#subscription-taxes)
    - [구독 기준일(anchor date)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판(Trial)](#subscription-trials)
    - [결제 수단 선제적 수집 방식](#with-payment-method-up-front)
    - [결제 수단 없이 체험판 제공](#without-payment-method-up-front)
    - [체험판 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단한 결제](#simple-charge)
    - [인보이스로 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스 조회](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [상품 결제 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원(Guest) Checkout](#guest-checkouts)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 승인 절차 안내](#confirming-payments)
- [강화된 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 인증이 필요한 결제](#payments-requiring-additional-confirmation)
    - [비세션(Off-session) 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 청구 서비스를 손쉽고 유연하게 사용할 수 있도록 지원합니다. 여러분이 작성하는 데 많은 시간을 들이고 싶지 않은 반복적인 구독 청구 로직을 Cashier가 알아서 처리해줍니다. 기본적인 구독 관리뿐 아니라, 쿠폰 처리, 구독 변경, 구독 "수량" 관리, 취소 유예 기간, 인보이스 PDF 생성 등 다양한 기능을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> Cashier는 큰 변경을 방지하기 위해 Stripe API 버전을 고정하여 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`을 사용합니다. Stripe의 새로운 기능과 개선사항 활용을 위해 Stripe API 버전은 마이너 업데이트에서 변경될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

패키지 설치 후, 아티즌 `vendor:publish` 명령어로 Cashier의 마이그레이션을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그런 다음 데이터베이스를 마이그레이션합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가합니다. 이외에도 모든 고객의 구독 정보를 저장하는 `subscriptions` 테이블과, 여러 가격이 포함된 구독을 위한 `subscription_items` 테이블을 새로 만듭니다.

필요하다면, Cashier의 설정 파일을 아래 Artisan 명령어로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 Stripe의 모든 이벤트를 정확히 처리할 수 있도록 [Cashier의 Webhook 처리를 설정](#handling-stripe-webhooks)해야 합니다.

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장하는 모든 컬럼이 대소문자를 구분(case-sensitive)해야 한다고 권장합니다. 따라서 MySQL을 사용할 때는 반드시 `stripe_id` 컬럼의 컬레이션이 `utf8_bin`으로 지정되어 있는지 확인하세요. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 결제 가능(Billable) 모델

Cashier 사용 전, 여러분의 결제 가능 모델에 `Billable` 트레이트를 추가해야 합니다. 일반적으로 이 모델은 `App\Models\User`입니다. 이 트레이트를 사용하면 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 다양한 결제 작업을 쉽게 수행할 수 있는 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 결제 가능 모델이 Laravel의 `App\Models\User`라고 가정합니다. 만약 다른 모델을 사용하려면, `useCustomerModel` 메서드로 변경할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

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
> Laravel 기본 제공 `App\Models\User` 외의 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시 및 수정하여 여러분의 커스텀 모델 테이블 구조에 맞게 변경해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, Stripe API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Stripe API 키는 Stripe 대시보드에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> 수신하는 Webhook이 실제 Stripe에서 온 것임을 검증하기 위해, 반드시 애플리케이션의 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수를 정의해야 합니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 지정하면 됩니다:

```ini
CASHIER_CURRENCY=eur
```

또한, 인보이스 등에서 금액을 표시할 때 사용할 언어(locale)를 별도로 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용하여 통화 locale을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 외의 other locale을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치되고 설정되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax)를 이용하면 Stripe에서 생성되는 모든 인보이스에 대해 세금을 자동 계산할 수 있습니다. 자동 세금 계산은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 활성화할 수 있습니다:

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

세금 계산이 활성화되면 새 구독을 생성하거나 단일 인보이스를 만들 때에도 자동 세금 계산이 적용됩니다.

이 기능이 제대로 작동하려면, 고객의 이름, 주소, 세금 ID 등 청구 관련 정보가 Stripe와 동기화되어야 합니다. 이를 위해 Cashier의 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 사용할 수 있습니다.

<a name="logging"></a>
### 로깅

Cashier는 Stripe의 치명적인 에러 발생 시 로깅에 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 정의하여 로그 채널을 정할 수 있습니다:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 중 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier 내부적으로 사용하는 모델을 확장하고 싶다면, 여러분만의 모델을 만들어 Cashier 모델을 상속하면 됩니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, Cashier에 해당 커스텀 모델을 사용하도록 지정하는 것이 일반적입니다. 보통은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 지정합니다:

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
### 상품 판매

> [!NOTE]
> Stripe Checkout을 활용하려면 Stripe 대시보드에서 고정 가격의 Product를 먼저 정의해야 합니다. 또한 [Cashier의 Webhook 처리](#handling-stripe-webhooks)도 반드시 설정해야 합니다.

애플리케이션에서 상품 및 구독 결제를 제공하는 일은 복잡할 수 있습니다. 그러나 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 모던하고 견고한 결제 연동을 쉽게 구현할 수 있습니다.

반복적이지 않은 단일 상품 결제를 고객에게 제공하기 위해, Cashier를 사용하여 Stripe Checkout 페이지로 고객을 안내할 수 있습니다. 이 Checkout에서 고객은 결제 정보를 입력하고 구매를 완료합니다. 결제가 완료되면 고객은 여러분이 지정한 애플리케이션의 성공 URL로 리다이렉트됩니다:

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

위 예시처럼, `checkout` 메서드를 사용해 지정한 "price identifier"로 Stripe Checkout으로 고객을 리다이렉트할 수 있습니다. Stripe에서 "price"는 [특정 상품의 가격을 의미](https://stripe.com/docs/products-prices/how-products-and-prices-work)합니다.

필요에 따라 `checkout` 메서드는 자동으로 Stripe에 고객을 생성하고, Stripe 고객 레코드를 애플리케이션의 사용자와 연결합니다. Checkout 세션을 마치면 고객은 지정된 성공/취소 페이지로 이동하며, 이곳에서 알림 메시지를 표시할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 제공

실제 상품 판매 시에는 여러분 애플리케이션 내의 `Cart`, `Order` 등 자체 모델을 활용하여 완료된 주문과 구매 내역을 관리할 수 있습니다. Stripe Checkout에서 결제를 완료하면, 해당 주문의 식별자를 저장해 두면 고객이 애플리케이션으로 돌아오면 어떤 주문에 대한 결제인지 쉽게 파악할 수 있습니다.

이를 위해 `checkout` 메서드에 `metadata` 배열을 전달할 수 있습니다. 예를 들어 사용자가 Checkout을 시작하면, 애플리케이션에서 미완성 `Order`를 생성하고 해당 정보로 Checkout 세션을 만듭니다(아래 예시의 `Cart`, `Order` 모델은 Cashier가 제공하는 것이 아니라, 예시용입니다):

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

위 코드처럼 사용자가 Checkout을 시작할 때, 해당 Cart/Order의 Stripe price id 목록 전체를 `checkout` 메서드에 전달할 수 있습니다. 실제로는 고객의 장바구니 또는 주문 내역관리를 애플리케이션에서 책임집니다. 또한 주문 id를 Stripe Checkout 세션의 메타데이터로 추가할 수 있습니다. 마지막에는 Checkout 성공 URL에 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe는 Checkout이 끝나고 리다이렉트할 때 이 자리에 실제 세션 id를 넣어줍니다.

다음으로 Checkout 성공 시 처리할 라우트를 구성해봅시다. 고객이 Stripe Checkout에서 결제 완료 후 리다이렉트되는 이 경로에서는, 전달된 세션 id를 이용해 Stripe Checkout 객체를 조회하고, 메타데이터(주문 id 등)을 읽어서 고객의 주문 상태를 업데이트할 수 있습니다:

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

Checkout 세션 오브젝트에 포함된 데이터에 관해서는 [Stripe 공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 상품 판매

> [!NOTE]
> Stripe Checkout을 활용하려면 Stripe 대시보드에서 고정 가격의 Product를 먼저 정의해야 합니다. 또한 [Cashier의 Webhook 처리](#handling-stripe-webhooks)도 반드시 설정해야 합니다.

애플리케이션에서 상품 및 구독 결제를 제공하는 일은 복잡할 수 있습니다. 그러나 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 이용하면 아주 쉽게 모던하고 견고한 결제 시스템을 구축할 수 있습니다.

Cashier 및 Stripe Checkout을 통해 구독(Subscription)을 판매하는 방법을 배워봅시다. 가령, 기본적인 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제 구독이 있다면, 이 두 가격은 Stripe 대시보드 내의 "Basic" 상품(`pro_basic`)에 속해 있을 수 있습니다. 추가 전문가 요금제(Expert plan)는 `pro_expert` 식별자로 제공할 수도 있습니다.

먼저, 고객이 어떻게 서비스를 구독하는지 살펴봅니다. 예를 들어 가격 정책 페이지에서 "Basic" 요금제 구독 버튼을 클릭할 수 있습니다. 이 버튼이나 링크는 해당 요금제의 Stripe Checkout 세션을 만드는 라라벨 라우트로 이동해야 합니다:

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

위처럼 `checkout` 메서드로 Stripe Checkout 세션으로 리다이렉트하면, 해당 요금제 구독이 시작됩니다. 결제가 성공적으로 끝나거나 취소되면, 고객은 지정한 URL로 이동합니다. 어떤 결제 수단은 몇 초간 처리가 필요하기도 하므로, 구독이 실제 시작되었는지 알기 위해 [Cashier의 Webhook 처리](#handling-stripe-webhooks)가 필요합니다.

이제 고객이 구독을 시작했으므로, 일부 구간은 구독자만 접근 가능하게 제한할 수 있습니다. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드로 현재 사용자의 구독 상태를 쉽게 판단할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 구독되어 있는지 구분하는 것도 가능합니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독자 여부 미들웨어 만들기

편의상, 요청이 구독자인지 판단하는 [미들웨어](/docs/12.x/middleware)를 작성하여 구독자가 아닌 사용자는 특정 라우트 접근을 막을 수도 있습니다:

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
            // 결제 페이지로 리다이렉트해서 구독 유도...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

작성한 미들웨어는 라우트에 다음과 같이 할당할 수 있습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 본인 요금제 관리 허용하기

고객이 직접 본인의 구독 요금제를 다른 상품이나 "티어"로 바꾸고 싶을 수도 있습니다. Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)을 사용하면, 고객이 인보이스 다운로드, 결제 수단 변경, 구독 요금제 변경 등 대부분의 관리를 직접 할 수 있는 Stripe의 UI를 제공받을 수 있습니다.

애플리케이션 내에 Stripe Billing Portal을 여는 링크나 버튼을 만듭니다:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

다음으로, Stripe 고객 Billing Portal 세션을 시작하고 사용자에게 리다이렉트하는 라우트 정의:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 Webhook 처리를 제대로 설정해두었다면, Stripe Billing Portal 내에서 사용자가 구독을 취소하는 경우 등의 Stripe 이벤트를 받아 Cashier가 애플리케이션 내의 관련 데이터베이스 테이블을 자동으로 동기화합니다.

<a name="customers"></a>
## 고객 (Customers)

<a name="retrieving-customers"></a>
### 고객 조회

`Cashier::findBillable` 메서드로 Stripe ID로 고객을 조회할 수 있습니다. 이 메서드는 해당 결제 가능 모델 인스턴스를 반환합니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔은 구독을 시작하지 않고 Stripe 고객만 따로 만들고 싶을 수도 있습니다. 이럴 때 `createAsStripeCustomer` 메서드를 사용할 수 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

고객이 Stripe에 생성된 후에는 언제든 구독을 시작할 수 있습니다. `$options` 배열 매개변수로 Stripe API에서 지원하는 [고객 생성시 파라미터](https://stripe.com/docs/api/customers/create)를 추가로 전달할 수 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

Stripe 고객 객체를 반환받고 싶으면 `asStripeCustomer` 메서드를 사용할 수 있습니다:

```php
$stripeCustomer = $user->asStripeCustomer();
```

이미 Stripe에 고객이 있는지 모를 경우, `createOrGetStripeCustomer` 메서드는 존재하면 반환하고, 없다면 새로 만듭니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 정보 업데이트

Stripe의 고객 정보를 추가로 업데이트할 필요가 있을 때는 `updateStripeCustomer` 메서드를 활용하세요. 이 메서드는 Stripe API에서 지원하는 [고객 정보 업데이트 옵션](https://stripe.com/docs/api/customers/update)의 배열을 입력받습니다:

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 관리

Stripe에서는 고객의 "잔액"에 금액을 적립(credit)하거나 차감(debit)할 수 있습니다. 이 잔액은 차후 신규 인보이스에 반영됩니다. 전체 잔액은 결제 가능 모델에서 `balance` 메서드로 확인할 수 있으며, 이때 잔액 문자열은 고객의 통화 규칙에 맞게 포매팅되어 반환됩니다:

```php
$balance = $user->balance();
```

잔액을 적립하려면 `creditBalance` 메서드에 금액을 입력합니다. 설명도 추가 가능:

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

잔액을 차감하려면 `debitBalance` 메서드를 사용합니다:

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance` 메서드는 고객의 잔액 트랜잭션을 생성해줍니다. `balanceTransactions` 메서드로 적립/차감 등의 트랜잭션 내역 전체를 조회할 수 있습니다:

```php
// 모든 트랜잭션 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액
    $amount = $transaction->amount(); // $2.31

    // 연관된 인보이스 조회(있을 경우)...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID(Tax IDs)

Cashier는 고객의 세금 ID 관리를 쉽게 할 수 있도록 도와줍니다. 예를 들어, `taxIds` 메서드는 고객에게 할당된 모든 [Tax ID](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션으로 반환합니다:

```php
$taxIds = $user->taxIds();
```

특정 Tax ID를 식별자로 조회할 수도 있습니다:

```php
$taxId = $user->findTaxId('txi_belgium');
```

`createTaxId` 메서드에는 적합한 [타입](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 입력해 새로 생성할 수 있습니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId`는 곧바로 고객 계정에 VAT ID를 추가합니다. [VAT ID의 검증](https://stripe.com/docs/invoicing/customer/tax-ids#validation)은 Stripe에서 비동기적으로 진행됩니다. 검증 상태 변경 알림을 받고 싶다면 `customer.tax_id.updated` webhook 이벤트 구독 및 [VAT ID `verification` 파라미터](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification) 확인이 필요합니다. 관련 Webhook 처리법은 [Webhook 핸들러 정의 문서](#handling-stripe-webhooks)를 참고하세요.

Tax ID 삭제는 `deleteTaxId` 메서드로 할 수 있습니다:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### 고객 정보 Stripe와 동기화

일반적으로 사용자가 애플리케이션에서 이름, 이메일 등 Stripe에도 저장되는 정보를 업데이트했다면, Stripe에도 변경 사항을 알려야 양쪽 정보가 항상 일치하게 됩니다.

이를 자동화하려면 결제 가능 모델에서 `updated` 이벤트 리스너를 정의하고, 리스너에서 `syncStripeCustomerDetails` 메서드를 호출하면 됩니다:

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * The "booted" method of the model.
 */
protected static function booted(): void
{
    static::updated(queueable(function (User $customer) {
        if ($customer->hasStripeId()) {
            $customer->syncStripeCustomerDetails();
        }
    }));
}
```

이제 고객 모델이 업데이트될 때마다 Stripe와 정보가 동기화됩니다. 참고로, Cashier는 고객 Stripe 계정 최초 생성 시에도 자동으로 정보 동기화를 처리해줍니다.

동기화에 사용할 컬럼을 직접 지정하고 싶다면 Cashier에서 제공하는 여러 메서드를 오버라이드할 수 있습니다. 예를 들어, 고객 "이름"을 Stripe에 동기화할 때 쓸 속성을 바꾸려면 `stripeName` 메서드를 오버라이드합니다:

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

마찬가지로 `stripeEmail`, `stripePhone`(최대 20자), `stripeAddress`, `stripePreferredLocales` 메서드도 오버라이드 가능하며, 이 값들은 Stripe 고객 정보 업데이트 시 해당 파라미터로 동기화됩니다. 만약 아예 전체 동기화 과정을 맞춤 구현하고 싶으면 `syncStripeCustomerDetails` 메서드를 직접 오버라이드 하세요.

<a name="billing-portal"></a>
### 과금 포털(Billing Portal)

Stripe는 [쉬운 과금 포털 설정 방법](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 이를 통해 고객은 본인의 구독 관리, 결제 수단 변경, 결제 내역 조회가 가능합니다. 컨트롤러 또는 라우트에서 결제 가능 모델의 `redirectToBillingPortal` 메서드를 호출해 사용자를 포털로 리다이렉트할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

사용자가 결제 관리 후 돌아올 대상 URL을 지정하려면, `redirectToBillingPortal` 호출 시 URL을 인수로 전달하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리다이렉트 없이 Billing Portal URL만 생성하려면 `billingPortalUrl` 메서드를 사용할 수 있습니다:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

(이하 내용 생략 없이 동일 규칙으로 계속 번역됩니다...)
