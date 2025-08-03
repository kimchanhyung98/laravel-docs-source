# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로그 기록](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객 관리](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터 Stripe와 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [복수 상품 구독](#subscriptions-with-multiple-products)
    - [복수 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 수단 정보 선제공](#with-payment-method-up-front)
    - [결제 수단 정보 없이](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [단순 청구](#simple-charge)
    - [인보이스 포함 청구](#charge-with-invoice)
    - [결제 인텐트 생성](#creating-payment-intents)
    - [청구 환불](#refunding-charges)
- [Checkout](#checkout)
    - [제품 Checkout](#product-checkouts)
    - [단일 청구 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [게스트 Checkout](#guest-checkouts)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정된 인보이스 조회](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증 (SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 간결하고 직관적인 인터페이스로 제공합니다. 반복되는 구독 결제 관련 코드 작성 부담을 거의 완전히 덜어줍니다. 기본적인 구독 관리 외에도 쿠폰, 구독 전환, 구독 "수량", 취소 유예 기간, 인보이스 PDF 생성 등 다양한 기능을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

> [!WARNING]
> 호환성 문제를 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`를 사용합니다. 새로운 기능 및 개선 사항 반영을 위해, Stripe API 버전은 마이너 릴리스 시 업데이트됩니다.

<a name="installation"></a>
## 설치 (Installation)

우선, Composer 패키지 매니저를 이용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

설치 후, `vendor:publish` Artisan 명령으로 Cashier의 마이그레이션 파일을 배포하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음 데이터베이스 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하고, 고객의 구독 정보를 담기 위한 `subscriptions` 테이블과, 복수 가격 구독용 `subscription_items` 테이블을 생성합니다.

필요하다면, 다음 명령으로 Cashier 설정 파일도 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Stripe 이벤트 처리에 Cashier가 정상 작동하도록 [웹훅 처리 설정](#handling-stripe-webhooks)을 꼭 구성하세요.

> [!WARNING]
> Stripe는 식별자 저장에 쓰이는 컬럼은 대소문자를 구분해야 한다고 권장합니다. 따라서 MySQL 사용 시 `stripe_id` 컬럼의 컬레이션을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델 (Billable Model)

Cashier를 사용하기 전에, 청구 가능 모델에 `Billable` 트레이트를 추가하세요. 일반적으로 `App\Models\User` 모델이 여기에 해당합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 업데이트 같은 다양한 결제 관련 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 Laravel에 포함된 `App\Models\User` 모델을 청구 가능 모델로 가정합니다. 다른 모델을 사용하려면 `Cashier::useCustomerModel` 메서드로 변경할 수 있습니다. 보통 이 코드는 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel 기본 `App\Models\User` 이외 모델을 사용하는 경우, [Cashier 마이그레이션](#installation)을 게시 및 수정해 해당 모델의 테이블명을 반영해야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

다음으로, `.env` 파일에 Stripe API 키를 설정합니다. 키는 Stripe 대시보드에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수를 반드시 `.env` 에 정의해야 하며, 이 값은 Stripe 웹훅 요청이 실제 Stripe에서 온 것인지 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

기본 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 변수를 설정해 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

또한 인보이스에 표시할 금액 포맷을 위한 통화 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 이용해 Stripe가 생성하는 모든 인보이스에 대해 자동 세금 계산이 가능합니다. 애플리케이션 `App\Providers\AppServiceProvider` 의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 활성화하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

세금 계산이 활성화되면, 신규 구독과 단일 인보이스 모두 자동으로 세금이 계산됩니다.

이 기능이 정확히 작동하려면 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe에 동기화되어야 합니다. 이를 위해 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 기능과 [세금 ID 관련 메서드](#tax-ids)를 활용하세요.

<a name="logging"></a>
### 로그 기록 (Logging)

치명적인 Stripe 오류 발생 시 로깅할 로그 채널을 `CASHIER_LOGGER` 환경 변수로 지정할 수 있습니다:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 관련 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier가 내부적으로 사용하는 모델을 확장하려면, 먼저 커스텀 모델을 정의하여 해당 Cashier 모델을 상속하세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

그 다음 `Laravel\Cashier\Cashier` 클래스에서 커스텀 모델 사용을 알려야 합니다. 보통 `App\Providers\AppServiceProvider` 의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * 애플리케이션 서비스 초기화
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
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격이 설정된 제품을 만들어야 합니다. 또한 [Cashier 웹훅 처리](#handling-stripe-webhooks)를 반드시 구성하세요.

애플리케이션에서 제품 및 구독 결제를 제공하는 것은 복잡할 수 있으나, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 모던하고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

일회성 구매(구독이 아닌) 제품 결제를 위한 예시입니다. Cashier의 `checkout` 메서드를 사용하여 고객을 Stripe Checkout으로 리다이렉트하고 결제 정보를 제공한 뒤 구매를 완료하도록 합니다. 결제 완료 시 고객은 애플리케이션 내 지정한 성공 URL로 리다이렉트됩니다:

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

위 예시에서 처럼 `checkout` 메서드에 "가격 식별자"를 전달해 고객을 Stripe Checkout 세션으로 리다이렉트합니다. Stripe에서 "가격"은 특정 제품의 [정의된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요하다면 `checkout` 메서드는 Stripe에 자동으로 고객을 생성하고, Stripe 고객 레코드와 애플리케이션 사용자 데이터를 연동합니다. Checkout 세션 완료 후 고객은 성공 또는 취소 페이지로 안내되며, 여기서 구매 정보를 보여줄 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 전달하기

제품 판매 시, 주문 및 구매한 상품 정보를 애플리케이션 내 `Cart` 와 `Order` 모델로 관리하는 경우가 많습니다. Stripe Checkout을 통해 결제를 진행할 때, 특정 주문 ID를 전달하여 결제 완료 후 주문과 매칭할 필요가 있습니다.

다음 예시는 사용자가 Checkout을 시작할 때 Pending 상태의 `Order`를 생성하고, Stripe Checkout 세션에 주문 ID를 메타데이터로 전달하는 방법입니다. `Cart`, `Order` 모델은 Cashier가 제공하는 모델이 아니며, 예시용 구현입니다:

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

위 예시에서, 주문과 연관된 모든 가격 ID를 `checkout` 메서드에 전달하고, `metadata` 배열로 주문 ID를 넘깁니다. 또한 Checkout 세션 성공 URL에 `{CHECKOUT_SESSION_ID}` 템플릿 변수도 추가했습니다. Stripe는 성공 페이지 리디렉션 시 이 값을 실제 Checkout 세션 ID로 치환해 전달합니다.

이제 성공 페이지에서 Checkout 세션 ID를 이용해 Stripe Checkout 세션 정보를 조회하고, 메타데이터의 주문 ID를 찾아 주문 상태를 완료로 변경해봅시다:

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

더 자세한 Stripe Checkout 세션 객체 데이터는 [Stripe 공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]
> Stripe Checkout을 사용하기 전 Stripe 대시보드에서 고정 가격 제품을 먼저 생성해야 하며, [Cashier 웹훅 처리](#handling-stripe-webhooks)도 반드시 설정해야 합니다.

애플리케이션에서 제품 및 구독 결제를 제공하는 과정은 까다로울 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 간단히 견고한 결제 시스템을 구축할 수 있습니다.

예를 들어 매월(기본 `price_basic_monthly`) 또는 매년(기본 `price_basic_yearly`) 요금제가 있고, Stripe 대시보드에서 두 가격이 "Basic" 제품(`pro_basic`)에 연결되어 있다고 가정합니다. 이외에 보다 고급 플랜도 제공할 수 있습니다(`pro_expert`).

다음은 고객이 Basic 요금제 구독을 시작하는 간단한 예시입니다. 고객이 가격 선택 후 해당 라우트로 이동하면 Stripe Checkout 세션이 생성됩니다:

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

위 예시처럼 `newSubscription` 으로 새 구독을 정의하고 `checkout` 으로 Stripe Checkout 세션을 시작합니다. 성공 또는 취소 시 해당 URL로 리다이렉트됩니다. 결제가 실제 완료된 시점은 결제 수단에 따라 약간의 처리 시간이 필요하므로, [웹훅 처리](#handling-stripe-webhooks)를 반드시 설정하세요.

구독 접근 제한을 위해 구독 여부를 판단하는 쉬운 방법도 있습니다. Cashier `Billable` 트레이트의 `subscribed` 메서드를 사용해 현재 구독 상태를 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 상품이나 가격에 대해 구독 여부를 확인할 수도 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 상품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 요금제를 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독자 전용 미들웨어 작성하기

필요하다면 요청자가 구독자인지 확인하는 [미들웨어](/docs/master/middleware)를 만들어 특정 라우트 접근을 차단할 수 있습니다:

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
            // 구독이 없으면 청구 페이지로 리다이렉션
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

미들웨어를 라우트에 할당해 사용합니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 결제 플랜 관리 허용하기

고객이 플랜을 변경하려면 Stripe의 [고객 청구 포털](https://stripe.com/docs/no-code/customer-portal)로 안내하는 게 가장 간단합니다. 이 포털에서는 고객이 인보이스 다운로드, 결제 수단 변경, 구독 플랜 변경 등을 할 수 있습니다.

애플리케이션에 청구 페이지 링크를 생성합니다:

```blade
<a href="{{ route('billing') }}">
    청구 관리
</a>
```

라우트 내에서 `redirectToBillingPortal` 메서드로 Stripe Billing Portal 세션을 시작하고, 완료 시 리다이렉트할 경로를 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier 웹훅이 제대로 구성되어 있다면, Stripe 포털에서 구독 취소 시 관련 웹훅을 수신하여 애플리케이션 내 구독 상태도 자동으로 갱신됩니다.

<a name="customers"></a>
## 고객 관리 (Customers)

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

Stripe ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 청구 가능 모델 인스턴스가 반환됩니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

때때로 구독 시작 없이 Stripe 고객만 생성하고 싶을 때가 있습니다. `createAsStripeCustomer` 메서드를 사용하세요:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

추가 Stripe 고객 생성 파라미터가 필요하면 옵션 배열을 넘겨 생성할 수 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

기존 Stripe 고객 객체를 반환받고 싶다면 `asStripeCustomer` 메서드를 사용하세요:

```php
$stripeCustomer = $user->asStripeCustomer();
```

Stripe에 고객이 존재할 수도, 안 할 수도 있을 때는 `createOrGetStripeCustomer` 메서드로 고객을 생성하거나 조회할 수 있습니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 정보 업데이트 (Updating Customers)

Stripe 고객 정보를 직접 갱신하고 싶다면 `updateStripeCustomer` 메서드를 사용하세요. Stripe API에서 지원하는 고객 업데이트 옵션 배열을 인자로 받습니다:

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 (Balances)

Stripe는 고객 잔액을 플러스(크레딧) 또는 마이너스(차감)로 관리할 수 있습니다. 잔액을 조회하려면 청구 가능 모델의 `balance` 메서드를 사용하세요. 출력값은 통화 단위가 적용된 문자열입니다:

```php
$balance = $user->balance();
```

잔액을 적립(크레딧)하려면 금액과 설명을 `creditBalance` 메서드에 넘기세요:

```php
$user->creditBalance(500, '프리미엄 고객 충전');
```

잔액을 차감하려면 `debitBalance` 메서드를 사용합니다:

```php
$user->debitBalance(300, '부적절 이용 패널티');
```

`applyBalance` 메서드는 고객의 잔액 거래 기록을 생성합니다. 거래 기록은 `balanceTransactions` 메서드로 조회 가능합니다:

```php
// 전체 거래 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액 조회...
    $amount = $transaction->amount(); // 예: $2.31

    // 연관된 인보이스가 있으면 조회...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID (Tax IDs)

Cashier는 고객 세금 ID 관리를 간단하게 해줍니다. `taxIds` 메서드는 고객에게 부여된 모든 세금 ID를 [컬렉션 형태](https://stripe.com/docs/api/customer_tax_ids/object)로 반환합니다:

```php
$taxIds = $user->taxIds();
```

특정 세금 ID를 찾으려면 식별자를 인자로 전달하세요:

```php
$taxId = $user->findTaxId('txi_belgium');
```

새로운 세금 ID는 유효한 유형과 값을 `createTaxId` 메서드를 통해 생성할 수 있습니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId`는 즉시 VAT ID를 계정에 추가하며, Stripe가 비동기적으로 유효성 검증을 수행합니다. `customer.tax_id.updated` 웹훅을 구독해 검증 상태 변경을 수신할 수 있습니다. 자세한 내용은 [웹훅 이벤트 핸들링 참고](#handling-stripe-webhooks) 바랍니다.

세금 ID 삭제는 `deleteTaxId` 메서드로 합니다:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### 고객 데이터 Stripe와 동기화 (Syncing Customer Data With Stripe)

사용자 이름, 이메일 등 Stripe에도 저장된 고객 데이터가 변경되면 Stripe와 앱 데이터를 동기화해주는 게 좋습니다. 모델의 `updated` 이벤트에 리스너를 등록해 `syncStripeCustomerDetails` 메서드를 호출하면 됩니다:

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * 모델의 booted 메서드
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

기본적으로 고객 생성 시에도 자동으로 동기화됩니다.

동기화 대상 컬럼을 바꾸려면 `stripeName`, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 등의 메서드를 커스터마이징하세요. 전체 과정을 직접 구현하려면 `syncStripeCustomerDetails` 메서드를 오버라이드할 수도 있습니다.

<a name="billing-portal"></a>
### 청구 포털 (Billing Portal)

Stripe는 고객이 구독, 결제 수단, 청구 내역을 편리하게 관리하는 [고객 청구 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. `redirectToBillingPortal` 메서드를 호출해 고객을 포털로 리다이렉트할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 종료 후 애플리케이션의 `home` 경로로 돌아갑니다. 다른 URL을 지정하려면 인자로 전달하세요:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

리다이렉트하지 않고 URL만 받으려면 `billingPortalUrl` 메서드를 사용하세요:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단 (Payment Methods)

<a name="storing-payment-methods"></a>
### 결제 수단 저장 (Storing Payment Methods)

구독 등록 또는 단일 결제 시 결제 수단 식별자를 Stripe에서 받아야 합니다. 구독용과 단일 청구용 결제 수단 처리 방법이 다르므로 각각 설명합니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독용 결제 수단

구독 결제용 카드 정보를 안전하게 수집하려면 Stripe "Setup Intents" API를 사용해야 합니다. `Billable` 트레이트의 `createSetupIntent` 메서드로 Setup Intent를 생성해 결제 수단 입력 폼에 제공합니다:

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

폼에서는 Setup Intent의 `client_secret` 값을 Stripe Elements에 넘겨 결제 수단을 수집합니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    결제 수단 업데이트
</button>
```

Stripe.js 라이브러리로 Elements를 초기화하고 아래와 같이 `confirmCardSetup` 으로 카드 정보 확인 및 결제 수단 ID를 받습니다:

```js
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');

    const cardHolderName = document.getElementById('card-holder-name');
    const cardButton = document.getElementById('card-button');
    const clientSecret = cardButton.dataset.secret;

    cardButton.addEventListener('click', async (e) => {
        const { setupIntent, error } = await stripe.confirmCardSetup(
            clientSecret, {
                payment_method: {
                    card: cardElement,
                    billing_details: { name: cardHolderName.value }
                }
            }
        );

        if (error) {
            // 에러 메시지 사용자에게 표시
        } else {
            // 정상 처리
            // setupIntent.payment_method 값을 앱 서버로 전달해 사용
        }
    });
</script>
```

검증된 결제 수단 ID는 [결제 수단 추가](#adding-payment-methods) 또는 [기본 결제 수단 업데이트](#updating-the-default-payment-method)에 쓸 수 있으며, 바로 [구독 생성](#creating-subscriptions)에도 사용할 수 있습니다.

> [!NOTE]
> Setup Intents 및 결제 수단 수집에 관한 자세한 내용은 [Stripe 공식 개요](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>
#### 단일 청구용 결제 수단

일회성 청구 결제 수단은 매번 Stripe.js로 새로 입력받아야 합니다. 아래처럼 폼과 Elements를 준비하고 `createPaymentMethod` 로 결제 수단 ID를 생성합니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 -->
<div id="card-element"></div>

<button id="card-button">
    결제 처리
</button>
```

```js
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');

    const cardHolderName = document.getElementById('card-holder-name');
    const cardButton = document.getElementById('card-button');

    cardButton.addEventListener('click', async (e) => {
        const { paymentMethod, error } = await stripe.createPaymentMethod(
            'card', cardElement, {
                billing_details: { name: cardHolderName.value }
            }
        );

        if (error) {
            // 에러 메시지 표시
        } else {
            // 정상 처리
            // paymentMethod.id 값을 서버에 전달해 단일 청구 처리
        }
    });
</script>
```

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회 (Retrieving Payment Methods)

청구 가능 모델의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다:

```php
$paymentMethods = $user->paymentMethods();
```

특정 결제 수단 유형을 지정하려면 인자에 `type`을 넘기세요:

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

기본 결제 수단은 `defaultPaymentMethod` 메서드로 조회 가능합니다:

```php
$paymentMethod = $user->defaultPaymentMethod();
```

특정 결제 수단 ID가 연결된 경우 `findPaymentMethod` 메서드로 조회할 수 있습니다:

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 결제 수단 존재 여부 (Payment Method Presence)

기본 결제 수단 존재 여부는 `hasDefaultPaymentMethod` 메서드를 통해 확인합니다:

```php
if ($user->hasDefaultPaymentMethod()) {
    // 기본 결제 수단 있음
}
```

아무 결제 수단이라도 있는지 확인하려면 `hasPaymentMethod` 메서드를 사용하세요:

```php
if ($user->hasPaymentMethod()) {
    // 최소 하나 이상의 결제 수단 존재
}
```

특정 유형의 결제 수단이 있는지 조회할 때도 `type` 인자를 넘기면 됩니다:

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // SEPA 직불 결제 수단이 있음
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트 (Updating the Default Payment Method)

`updateDefaultPaymentMethod` 메서드에 Stripe 결제 수단 ID를 넘겨 기본 결제 수단으로 설정할 수 있습니다:

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

Stripe 상 기본 결제 수단 정보를 앱 데이터와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 호출하세요:

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> Stripe의 기본 결제 수단은 구독 및 인보이스 청구 시에만 활용 가능합니다. 단일 청구에는 사용할 수 없는 Stripe 제한 사항이 있으니 참고하세요.

<a name="adding-payment-methods"></a>
### 결제 수단 추가 (Adding Payment Methods)

신규 결제 수단 추가는 `addPaymentMethod` 메서드에 식별자를 넘겨 수행합니다:

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 얻는 방법은 [결제 수단 저장](#storing-payment-methods) 문서를 참고하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제 (Deleting Payment Methods)

결제 수단 인스턴스에서 `delete` 메서드로 개별 삭제가 가능합니다:

```php
$paymentMethod->delete();
```

사용자별 결제 수단을 ID로 삭제하려면 `deletePaymentMethod` 메서드를 사용하세요:

```php
$user->deletePaymentMethod('pm_visa');
```

모든 결제 수단 삭제는 `deletePaymentMethods` 메서드를 호출합니다:

```php
$user->deletePaymentMethods();
```

특정 종류만 삭제하고 싶으면 `type` 인자를 넘깁니다:

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독 중이면 기본 결제 수단 삭제를 허용해서는 안 됩니다.

<a name="subscriptions"></a>
## 구독 (Subscriptions)

구독은 고객에게 반복 결제를 처리할 수 있도록 합니다. Cashier가 관리하는 Stripe 구독은 복수 가격, 수량, 체험 기간 등 다양한 기능을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 먼저 청구 가능 모델 인스턴스(일반적으로 `App\Models\User`)를 조회하고 `newSubscription` 메서드를 호출합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

첫 번째 인자는 애플리케이션 내부 구독 타입명이며, 보통 'default'나 'primary'로 부릅니다. 이 이름은 사용자에게 보여지지 않으며, 공백을 포함하면 안 되고 구독 생성 후 변경하지 않아야 합니다. 두 번째 인자는 Stripe 가격 ID입니다.

`create` 메서드는 결제 수단 ID(`PaymentMethod`)를 받아 구독을 시작하며 관련 Stripe 고객 ID와 청구 정보를 앱 데이터베이스에 저장합니다.

> [!WARNING]
> `create` 메서드에 결제 수단 ID를 넘길 때 자동으로 사용자의 저장된 결제 수단에 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 인보이스 이메일로 반복 결제 수금

자동 결제 대신 Stripe가 고객에게 인보이스 이메일을 발송해 수동으로 결제하도록 할 수도 있습니다. 이 경우 구독 생성 시 초기 결제 수단 정보 수집이 필요 없습니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

인보이스 결제 기한(days_until_due)은 기본 30일이며 옵션으로 변경 가능합니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 수량 설정

구독 생성 시 가격별 수량을 지정하려면 `quantity` 메서드를 구독 빌더에 체인합니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 세부 정보

Stripe API 고객 및 구독 옵션을 따로 지정하려면 `create` 메서드 두 번째(고객 옵션)와 세 번째(구독 옵션) 인자로 배열을 넘기세요:

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => '추가 정보'],
]);
```

<a name="coupons"></a>
#### 쿠폰 사용

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요:

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('코드')
    ->create($paymentMethod);
```

Stripe 프로모션 코드를 적용하려면 `withPromotionCode` 를 사용하세요. 프로모션 코드 ID는 고객에게 노출되는 코드가 아닌 Stripe API에서 부여한 식별자여야 합니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

고객 코드로 프로모션 코드 ID를 찾으려면 `findPromotionCode` 또는 활성 코드만 찾으려면 `findActivePromotionCode` 를 사용하세요:

```php
// 고객 코드로 프로모션 코드 ID 조회...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// 활성 프로모션 코드 ID 조회...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

반환된 객체는 `Laravel\Cashier\PromotionCode` 인스턴스로, 철저히 감싼 Stripe 프로모션 코드입니다. `coupon` 메서드로 관련 쿠폰도 조회할 수 있습니다:

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

쿠폰이 고정 금액인지 백분율인지 확인하려면 아래 예처럼 검토하세요:

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 예: 21.5%
} else {
    return $coupon->amountOff(); // 예: $5.99
}
```

현재 고객 또는 구독에 적용된 할인 정보는 아래처럼 조회합니다:

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

`Laravel\Cashier\Discount` 객체는 `Stripe\Discount` 를 감쌉니다. 관련 쿠폰은 `coupon` 메서드로 조회 가능:

```php
$coupon = $subscription->discount()->coupon();
```

고객 또는 구독에 새로운 쿠폰 적용은 `applyCoupon` 또는 `applyPromotionCode` 메서드를 사용합니다:

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

단 한 번에 쿠폰 또는 프로모션 코드 하나만 적용할 수 있습니다.

자세한 내용은 [Stripe 쿠폰](https://stripe.com/docs/billing/subscriptions/coupons)과 [프로모션 코드](https://stripe.com/docs/billing/subscriptions/coupons/codes) 문서를 참고하세요.

<a name="adding-subscriptions"></a>
#### 추가 구독 생성

이미 결제 수단이 등록된 고객은 `add` 메서드로 쉽게 구독을 추가할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드 구독 생성

Stripe 대시보드에서도 구독을 생성할 수 있습니다. 이 경우 구독 유형은 자동으로 `default`로 할당됩니다. 대시보드에서 생성된 구독의 타입을 바꾸려면 [웹훅 핸들러](#defining-webhook-event-handlers)를 작성하세요.

대시보드는 한 유형만 생성 가능하며, 다중 구독형 앱에서는 한 개만 대시보드로 추가할 수 있습니다.

중요하게, 사용자별로 구독 유형당 활성 구독은 하나만 유지하세요. 두 개 이상의 `default` 구독이 있을 경우 Cashier는 가장 최신 구독만 사용합니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

구독자 여부 및 구독 상태 확인은 다양한 메서드로 간단합니다.

우선, `subscribed` 메서드는 활성 구독이 있으면(`체험 기간 포함`) `true`를 리턴합니다. 첫 인자로 구독 타입명을 넣으세요:

```php
if ($user->subscribed('default')) {
    // 구독 상태임
}
```

이 메서드는 [라우트 미들웨어](/docs/master/middleware)로도 활용 가능해 구독자만 접근 가능하도록 필터링할 수 있습니다:

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
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 결제 미완료 사용자 리다이렉션
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

체험 기간 여부 판단은 `onTrial` 메서드로 가능합니다:

```php
if ($user->subscription('default')->onTrial()) {
    // 체험 기간 중
}
```

특정 상품 구독 여부는 `subscribedToProduct` 로, 상품 식별자는 Stripe Dashboard 내 상품 ID를 사용합니다:

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // 프리미엄 상품 구독 중
}
```

배열로 여러 상품 비교도 가능합니다:

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // 베이직 또는 프리미엄 상품 구독 중
}
```

구독한 가격 ID 여부는 `subscribedToPrice` 메서드를 사용합니다:

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // 월간 요금제를 구독 중
}
```

`recurring` 메서드는 "구독 중이며 체험 기간이 아닌" 상태 여부를 반환합니다:

```php
if ($user->subscription('default')->recurring()) {
    // 구독 중이고 체험 기간이 아님
}
```

> [!WARNING]
> 같은 유형 `default` 구독이 여러 개 있으면 `subscription` 메서드는 가장 최신 구독을 제공합니다. 오래된 구독은 데이터 보존용입니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

`canceled` 메서드는 이전에 구독했으나 취소한 경우 `true`를 반환합니다:

```php
if ($user->subscription('default')->canceled()) {
    // 구독 취소됨
}
```

취소했으나 유예 기간 중인 경우(`ends_at` 이후) 판단하려면 `onGracePeriod` 를 사용:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // 구독 취소 후 유예 기간 중
}
```

유예 기간이 끝났다면 `ended` 메서드를 사용해 판단하세요:

```php
if ($user->subscription('default')->ended()) {
    // 구독 종료됨
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료(incomplete) 및 연체(past_due) 상태

지불 추가 인증이 필요한 경우 구독 상태는 `incomplete` 혹은 가격 변경 후 결제가 지연되면 `past_due` 상태가 됩니다. 이 상태에서 구독은 활성화되지 않으므로, 반드시 결제 확인을 진행해야 합니다.

미완료 결제 상태는 아래처럼 확인 가능합니다:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

미완료 결제가 있으면 사용자를 Cashier 내 결제 확인 페이지로 안내하고, `latestPayment` 메서드로 결제 ID를 넘겨주면 됩니다:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    결제 확인을 진행해주세요.
</a>
```

`AppServiceProvider` 의 `register` 메서드에 아래 설정을 추가하면 `past_due` 와 `incomplete` 상태 구독을 활성 상태로 유지할 수 있습니다:

```php
use Laravel\Cashier\Cashier;

/**
 * 서비스 등록
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]
> `incomplete` 상태에서는 구독 변경이 불가능하므로 `swap`, `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 상태 쿼리 스코프

다음과 같은 쿼리 스코프를 사용해 원하는 상태 구독을 쿼리할 수 있습니다:

```php
Subscription::query()->active();
Subscription::query()->canceled();
Subscription::query()->ended();
Subscription::query()->incomplete();
Subscription::query()->notCanceled();
Subscription::query()->notOnGracePeriod();
Subscription::query()->notOnTrial();
Subscription::query()->onGracePeriod();
Subscription::query()->onTrial();
Subscription::query()->pastDue();
Subscription::query()->recurring();
```

<a name="changing-prices"></a>
### 가격 변경 (Changing Prices)

고객이 구독 가격을 변경하고 싶으면 `swap` 메서드에 새 가격 ID를 넘겨 구독을 교체할 수 있습니다. 이때 구독 취소 상태면 자동으로 구독이 재활성화됩니다:

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

체험 기간을 무시하고 즉시 가격 변경하려면 `skipTrial` 메서드를 체인하세요:

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

즉시 고객에게 인보이스를 발행하며 가격 변경하려면 `swapAndInvoice` 메서드를 사용합니다:

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 가격 변경 시 정산(Proration)

기본적으로 Stripe는 가격 변경 시 정산을 수행합니다. 정산 없이 가격을 변경하려면 `noProrate` 메서드를 체인하세요:

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

> [!WARNING]
> `noProrate` 체인 후 `swapAndInvoice` 호출 시 정산을 적용하지 못합니다. 인보이스 발행이 우선됩니다.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

구독 수량은 `incrementQuantity` / `decrementQuantity` 메서드로 쉽게 증감할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 현재 수량에 5 추가...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 현재 수량에서 5 차감...
$user->subscription('default')->decrementQuantity(5);
```

정확한 수량 지정은 `updateQuantity` 메서드를 사용하세요:

```php
$user->subscription('default')->updateQuantity(10);
```

정산 없이 수량 변경 시 `noProrate` 체인:

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

더 자세한 내용은 [Stripe 구독 수량 문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독에서 수량 설정

다중 가격이 있는 구독이라면 증감 메서드의 두 번째 인자로 수량을 변경할 가격 ID를 넣어야 합니다:

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독 (Subscriptions With Multiple Products)

다중 상품 구독은 하나의 구독에 여러 과금 상품을 붙이는 기능입니다. 예를 들어, 기본 월 $10 구독에 라이브 채팅 추가 $15 옵션을 붙일 수 있습니다. 이 정보는 `subscription_items` 테이블에 저장됩니다.

가격 배열을 `newSubscription` 메서드 두 번째 인자로 전달해 구독을 만듭니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', [
        'price_monthly',
        'price_chat',
    ])->create($request->paymentMethodId);

    // ...
});
```

각 가격별로 수량 설정도 가능합니다:

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 새 가격을 추가할 때는 `addPrice` 메서드를 사용합니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

즉시 결제하려면 `addPriceAndInvoice` 를 사용하세요:

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

수량을 지정하여 추가도 가능합니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

가격 제거는 `removePrice` 로 수행합니다:

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독 내 마지막 가격은 제거할 수 없습니다. 구독을 취소하세요.

<a name="swapping-prices"></a>
#### 가격 교체

다중 가격 구독에서 가격을 교체할 수도 있습니다. 예를 들어 `price_basic`을 `price_pro`로 업그레이드할 때:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

기존 `price_basic` 구독 항목은 삭제되고, `price_chat`은 유지되며 `price_pro`가 추가됩니다.

수량 지정 등 옵션도 넘길 수 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

특정 구독 항목만 교체할 수도 있습니다:

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
#### 정산(Proration)

다중 가격 추가 및 제거도 기본적으로 정산이 적용됩니다. 정산 없이 처리하려면 `noProrate` 메서드를 체인하세요:

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량 변경

다중 가격 개별 수량 변경 시 두 번째 인자로 가격 ID를 전달합니다:

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 다중 가격 구독은 `Subscription` 모델의 `stripe_price` 와 `quantity` 속성이 `null`입니다. 개별 가격 정보는 `items` 관계를 통해 확인하세요.

<a name="subscription-items"></a>
#### 구독 아이템 (Subscription Items)

다중 가격 구독은 DB `subscription_items` 테이블에 복수 구독 항목으로 저장됩니다. `items` 관계로 접근 가능:

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// 특정 아이템의 Stripe 가격과 수량 조회
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

가격 ID로 특정 아이템 조회는 `findItemOrFail` 메서드를 사용합니다:

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 복수 구독 (Multiple Subscriptions)

Stripe는 고객당 복수 구독 생성도 지원합니다. 예를 들어 수영 구독과 웨이트 구독을 개별 제공할 수 있습니다.

구독 생성 시 구독 타입명을 지정하세요:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

타입별 구독 가격 변경도 간단합니다:

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

구독 취소 역시 마찬가지:

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### 사용량 기반 과금 (Usage Based Billing)

사용량 기반 과금은 청구 주기 내 실제 사용량에 따라 비용을 부과하는 방식입니다. 예: 한 달간 보낸 이메일 수에 따라 과금.

이용하려면 Stripe 대시보드에서 사용량 기반 과금 모델과 미터를 생성한 후 Meter ID와 이벤트명을 저장하세요. `meteredPrice` 메서드로 고객 구독에 과금 항목을 추가합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

Stripe Checkout으로도 시작 가능:

```php
$checkout = Auth::user()
    ->newSubscription('default', [])
    ->meteredPrice('price_metered')
    ->checkout();

return view('your-checkout-view', [
    'checkout' => $checkout,
]);
```

<a name="reporting-usage"></a>
#### 사용량 보고

서비스 사용량은 `reportMeterEvent` 메서드로 Stripe에 보고하세요:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

기본 수량은 1이며 `quantity` 인자로 임의 값도 전달 가능합니다:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

특정 미터 이벤트의 사용 요약은 `meterEventSummaries` 메서드로 조회합니다:

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

모든 미터 목록은 `meters` 메서드 사용:

```php
$user = User::find(1);

$user->meters();
```

더 자세한 내용은 Stripe [Meter Event Summary 객체 문서](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참조하세요.

<a name="subscription-taxes"></a>
### 구독 세금 (Subscription Taxes)

> [!WARNING]
> 직접 세율 계산하지 말고 [Stripe Tax 자동 세금 계산](#tax-configuration)을 사용하세요.

구독별 세금율을 지정하려면 청구 가능 모델에 `taxRates` 메서드를 구현하고 Stripe 세율 ID 배열을 반환하세요. 세율은 [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 설정합니다:

```php
/**
 * 고객 구독에 적용할 세율
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```

상품별 다양한 세율 적용은 `priceTaxRates` 메서드 구현:

```php
/**
 * 고객 구독 상품별 세율
 *
 * @return array<string, array<int, string>>
 */
public function priceTaxRates(): array
{
    return [
        'price_monthly' => ['txr_id'],
    ];
}
```

> [!WARNING]
> `taxRates`는 구독 청구에만 적용됩니다. 단일 결제 시는 별도 세율 지정이 필요합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화

`taxRates` 메서드 세율 ID 변경 시 기존 구독의 세율은 유지됩니다. 변경 사항을 기존 구독에 반영하려면 다음처럼 `syncTaxRates`를 호출하세요:

```php
$user->subscription('default')->syncTaxRates();
```

복수 상품 구독도 포함됩니다. 이때 청구 가능 모델에 `priceTaxRates` 메서드를 구현해야 합니다.

<a name="tax-exemption"></a>
#### 세금 면제 상태

Cashier는 Stripe API를 호출해 고객 세금 면제 여부를 판단하는 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드를 제공합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

이 메서드들은 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있으나, 해당 인보이스 생성 시점의 면제 상태를 판단합니다.

<a name="subscription-anchor-date"></a>
### 구독 기준일 (Subscription Anchor Date)

구독 청구 기준일은 기본적으로 구독 생성일 또는 체험 기간 종료일입니다. 변경하려면 `anchorBillingCycleOn` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $anchor = Carbon::parse('first day of next month');

    $request->user()->newSubscription('default', 'price_monthly')
        ->anchorBillingCycleOn($anchor->startOfDay())
        ->create($request->paymentMethodId);

    // ...
});
```

자세한 구독 청구 주기 관리는 [Stripe 청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소 (Cancelling Subscriptions)

구독 취소는 `cancel` 메서드로 실행합니다:

```php
$user->subscription('default')->cancel();
```

취소 시 `subscriptions` 테이블의 `ends_at` 컬럼을 설정해 구독 기간 만료 시점을 기록합니다. 예를 들어 3월 1일 취소하더라도 청구 주기 종료일인 3월 5일까지는 서비스 이용이 유지되어 `subscribed` 메서드는 참으로 남습니다.

취소 후 유예 기간 여부 확인은 `onGracePeriod` 메서드를 사용합니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow` 메서드를 호출하세요:

```php
$user->subscription('default')->cancelNow();
```

즉시 취소 후 남은 미청구 사용량이나 잔여 정산 항목까지 인보이스에 포함해 청구하려면 `cancelNowAndInvoice`를 사용합니다:

```php
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점에 취소 예약도 가능합니다:

```php
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

삭제 전에 구독을 반드시 취소해야 합니다:

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### 구독 재개 (Resuming Subscriptions)

유예 기간 내에 구독을 재개하려면 `resume` 메서드를 호출하세요:

```php
$user->subscription('default')->resume();
```

재개 시 즉시 청구되지 않고 기존 청구 주기에 맞춰 청구됩니다.

<a name="subscription-trials"></a>
## 구독 체험 기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 정보 선제공 (With Payment Method Up Front)

선제공된 결제 수단과 함께 체험 기간을 설정하려면 `trialDays` 메서드를 체인하세요:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

구독 레코드 db에 체험 종료일이 설정되고 Stripe에는 체험 기간 종료 후 청구 시작 명령이 전달됩니다. `trialDays` 는 Stripe 가격 기본 설정을 덮어씁니다.

> [!WARNING]
> 체험 종료일까지 구독을 취소하지 않으면 체험 종료 시점에 자동 결제가 진행되므로 사용자에게 종료일을 알려야 합니다.

`trialUntil` 메서드는 구체적인 날짜 지정용입니다:

```php
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->addDays(10))
    ->create($paymentMethod);
```

체험 여부 판단은 사용자 또는 구독 인스턴스의 `onTrial` 메서드 두 가지가 모두 가능합니다:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

즉시 체험 종료는 `endTrial` 메서드를 호출하면 됩니다:

```php
$user->subscription('default')->endTrial();
```

체험 만료 여부는 `hasExpiredTrial` 메서드를 통해 판단:

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier 체험 기간 설정 방법

가격별 기본 체험 일수는 Stripe Dashboard에서 정의하거나 Cashier에서 명시적으로 지정할 수 있습니다. Stripe에서 설정하면 과거 구독자도 매번 초기 구독 시 체험 기간을 받는다는 점에 유의하세요(`skipTrial()` 호출 시 예외).

<a name="without-payment-method-up-front"></a>
### 결제 수단 정보 없이 (Without Payment Method Up Front)

결제 수단 없이 체험 기간 제공하려면 사용자 등록 시 `trial_ends_at` 컬럼에 체험 종료 날짜를 세팅하세요:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]
> 청구 가능 모델에 `trial_ends_at` 속성에 [날짜 캐스팅](/docs/master/eloquent-mutators#date-casting)을 반드시 추가해야 합니다.

이는 "Generic Trial"로 불리며, 구독 기록과는 별개입니다. `onTrial` 메서드는 현재 시점과 `trial_ends_at` 비교 결과를 반환합니다:

```php
if ($user->onTrial()) {
    // 유저가 체험 기간 중임
}
```

이후 기존처럼 `newSubscription` 으로 구독을 생성할 수 있습니다:

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

사용자 체험 종료 시간은 `trialEndsAt` 메서드에서 조회 가능하며 타입 인자를 넘겨 특정 구독의 체험 종료 시간도 얻을 수 있습니다:

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

"Generic Trial"임을 명확히 확인하려면 `onGenericTrial` 메서드를 사용하세요:

```php
if ($user->onGenericTrial()) {
    // 아직 구독을 생성하지 않은 체험 기간
}
```

<a name="extending-trials"></a>
### 체험 기간 연장 (Extending Trials)

`extendTrial` 메서드로 구독 체험 기간을 연장할 수 있습니다. 이미 체험 기간이 만료된 고객도 연장 가능하며, 체험료 시간은 차기 인보이스에서 차감됩니다:

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 7일 연장
$subscription->extendTrial(
    now()->addDays(7)
);

// 기존 종료일에 5일 추가
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe 웹훅 처리 (Handling Stripe Webhooks)

> [!NOTE]
> Stripe CLI를 사용하면 로컬 개발 시 웹훅 테스트를 쉽게 할 수 있습니다.

Stripe는 다양한 이벤트를 웹훅으로 애플리케이션에 통보할 수 있습니다. 기본적으로 Cashier 서비스 프로바이더에서 웹훅 라우트를 등록하며, Cashier 웹훅 컨트롤러가 이를 처리합니다.

웹훅 컨트롤러는 구독 취소, 고객 정보 변경, 결제 수단 변경 등 주요 이벤트를 자동 처리하지만, 필요하면 이벤트를 확장하여 직접 처리할 수도 있습니다.

Stripe 대시보드에 웹훅 URL을 설정하세요. 기본 경로는 `/stripe/webhook` 입니다. Cashier 이용 시 등록해야 할 이벤트 목록:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

> Artisan 명령어 `cashier:webhook` 으로 필요한 웹훅을 자동 생성할 수 있습니다:

```shell
php artisan cashier:webhook
```

기본 생성 URL은 `APP_URL` 환경변수와 `cashier.webhook` 라우트입니다. URL 변경은 `--url` 옵션 사용:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

Stripe API 버전 변경은 `--api-version`으로:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

생성 시 바로 활성화되며, 비활성화 시작은 `--disabled` 옵션 지정:

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> 웹훅 요청은 반드시 [웹훅 서명 검증](#verifying-webhook-signatures) 미들웨어로 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

웹훅은 Laravel CSRF 보호를 우회해야 하므로, `stripe/*` 경로를 CSRF 검증 제외 목록에 추가해야 합니다. 예를 들어 `bootstrap/app.php` 등에서 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 구독 취소 등 기본 이벤트를 자동 처리하지만, 추가 이벤트는 이벤트 디스패치로 처리할 수 있습니다.

리스너는 다음 이벤트를 구독할 수 있습니다:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

페이로드 전체를 포함합니다. 예를 들어 `invoice.payment_succeeded` 웹훅 핸들러 예시:

```php
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Stripe 웹훅 수신 처리
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // 이벤트 처리
        }
    }
}
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증 (Verifying Webhook Signatures)

웹훅 보안을 위해 Stripe 서명 검증이 필요합니다. Cashier는 웹훅 요청 유효성 검사 미들웨어를 기본 제공합니다.

`STRIPE_WEBHOOK_SECRET` 환경 변수에 Stripe 대시보드에서 받은 서명 비밀키를 설정해야 합니다.

<a name="single-charges"></a>
## 단일 청구 (Single Charges)

<a name="simple-charge"></a>
### 단순 청구 (Simple Charge)

일회성 결제는 청구 가능 모델 인스턴스의 `charge` 메서드를 사용합니다. 두 번째 인자로 결제 수단 ID가 필요합니다:

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

세 번째 인자로 Stripe 청구 생성 옵션 배열을 넘길 수 있습니다. 자세한 옵션은 [Stripe 문서](https://stripe.com/docs/api/charges/create) 참조:

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

청구 대상을 고객 없이 새 청구 가능 모델 인스턴스에서 생성할 수도 있습니다:

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

청구 실패 시 예외가 발생하며, 성공 시 `Laravel\Cashier\Payment` 인스턴스를 반환합니다:

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> 금액은 애플리케이션 통화 단위의 최하위 단위(예: USD는 센트)로 지정해야 합니다.

<a name="charge-with-invoice"></a>
### 인보이스 포함 청구 (Charge With Invoice)

인보이스 PDF를 포함한 일회성 청구는 `invoicePrice` 메서드를 사용합니다. 예: 티셔츠 5벌 청구

```php
$user->invoicePrice('price_tshirt', 5);
```

세 번째 인자로 인보이스 항목 옵션, 네 번째 인자로 인보이스 전체 옵션 배열도 전달 가능:

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

`tabPrice` 메서드는 인보이스에 여러 항목(최대 250개) 임시 적립 후 청구를 지원합니다:

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

`invoiceFor` 메서드는 기본 결제 수단으로 일회성 결제를 진행합니다:

```php
$user->invoiceFor('One Time Fee', 500);
```

`invoicePrice`와 `tabPrice`는 미리 정의된 가격 사용으로 Stripe 대시보드에서 상세 분석이 가능하므로 선호됩니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 인보이스가 청구 실패 시 재시도합니다. 실패 시 반복 청구가 필요 없으면 Stripe API로 인보이스를 닫아야 합니다.

<a name="creating-payment-intents"></a>
### 결제 인텐트 생성 (Creating Payment Intents)

새 결제 인텐트를 생성하려면 `pay` 메서드를 호출하세요. 반환 값은 `Laravel\Cashier\Payment` 인스턴스입니다:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

프론트엔드로 클라이언트 시크릿을 반환해 Stripe에서 결제 완료하도록 합니다. 전체 결제 흐름은 [Stripe 결제 인텐트 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

허용 결제 수단을 제한하려면 `payWith` 메서드를 사용합니다:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->payWith(
        $request->get('amount'), ['card', 'bancontact']
    );

    return $payment->client_secret;
});
```

> [!WARNING]
> 금액은 최소 화폐 단위이며, 예컨대 미국 달러의 경우 센트로 지정해야 합니다.

<a name="refunding-charges"></a>
### 청구 환불 (Refunding Charges)

Stripe 결제 환불은 `refund` 메서드를 사용하며, 첫 인자에 결제 인텐트 ID를 전달합니다:

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 인보이스 (Invoices)

<a name="retrieving-invoices"></a>
### 인보이스 조회 (Retrieving Invoices)

청구 가능 모델의 인보이스 목록은 `invoices` 메서드로 `Laravel\Cashier\Invoice` 인스턴스 컬렉션을 얻습니다:

```php
$invoices = $user->invoices();
```

대기 중인 인보이스도 포함하려면 `invoicesIncludingPending` 사용:

```php
$invoices = $user->invoicesIncludingPending();
```

특정 인보이스 조회는 `findInvoice` 메서드를 사용합니다:

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 인보이스 정보 출력

인보이스 리스트를 표로 출력할 때 다음과 같이 각 인보이스의 날짜, 총액, 다운로드 링크를 표기할 수 있습니다:

```blade
<table>
    @foreach ($invoices as $invoice)
        <tr>
            <td>{{ $invoice->date()->toFormattedDateString() }}</td>
            <td>{{ $invoice->total() }}</td>
            <td><a href="/user/invoice/{{ $invoice->id }}">다운로드</a></td>
        </tr>
    @endforeach
</table>
```

<a name="upcoming-invoices"></a>
### 예정된 인보이스 조회 (Upcoming Invoices)

예정된 인보이스는 `upcomingInvoice` 메서드로 조회합니다:

```php
$invoice = $user->upcomingInvoice();
```

복수 구독 고객은 특정 구독의 예정 인보이스도 조회 가능합니다:

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 인보이스 미리보기 (Previewing Subscription Invoices)

가격 변경 전 인보이스 예상 요금을 `previewInvoice` 메서드로 확인할 수 있습니다:

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

복수 가격 배열 전달도 가능합니다:

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 인보이스 PDF 생성 (Generating Invoice PDFs)

인보이스 PDF 생성을 위해 Dompdf 라이브러리를 설치하세요:

```shell
composer require dompdf/dompdf
```

라우트 또는 컨트롤러 내 `downloadInvoice` 메서드로 PDF 다운로드 응답을 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

두 번째 인자에 회사/제품 정보 등 커스텀 데이터도 전달할 수 있습니다:

```php
return $request->user()->downloadInvoice($invoiceId, [
    'vendor' => 'Your Company',
    'product' => 'Your Product',
    'street' => 'Main Str. 1',
    'location' => '2000 Antwerp, Belgium',
    'phone' => '+32 499 00 00 00',
    'email' => 'info@example.com',
    'url' => 'https://example.com',
    'vendorVat' => 'BE123456789',
]);
```

세 번째 인자에 원하는 파일명을 넘기면 `.pdf` 확장자와 함께 사용됩니다:

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 인보이스 렌더러 (Custom Invoice Renderer)

기본적으로 Cashier는 [DompdfInvoiceRenderer](https://github.com/dompdf/dompdf)를 이용하지만, `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현해 커스텀 렌더러를 만들 수도 있습니다. 예를 들어 3rd-party API 사용:

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * Invoice PDF 바이트 생성
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

완성 후 `config/cashier.php` 설정의 `cashier.invoices.renderer` 값을 커스텀 클래스명으로 수정하세요.

<a name="checkout"></a>
## Checkout

Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)을 지원합니다. Stripe Checkout은 커스텀 결제 페이지 개발 부담을 줄이고, 호스팅된 결제 페이지를 제공합니다.

아래는 Cashier와 Checkout 사용법을 소개합니다. Stripe 공식 Checkout 문서도 참고하세요: https://stripe.com/docs/payments/checkout

<a name="product-checkouts"></a>
### 제품 Checkout (Product Checkouts)

Stripe 대시보드에 생성된 제품의 가격으로 Checkout 세션을 생성하려면 청구 가능 모델의 `checkout` 메서드를 사용하세요. 기본적으로 Stripe 가격 ID를 전달해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

수량 지정도 가능:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

고객이 Checkout 완료 또는 취소 시 리다이렉션될 URL도 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

성공 URL에 `{CHECKOUT_SESSION_ID}` 를 쿼리 문자열에 사용하면 Stripe가 세션 ID로 자동 교체합니다:

```php
use Illuminate\Http\Request;
use Stripe\Checkout\Session;
use Stripe\Customer;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
    ]);
});

Route::get('/checkout-success', function (Request $request) {
    $checkoutSession = $request->user()->stripe()->checkout->sessions->retrieve($request->get('session_id'));

    return view('checkout.success', ['checkoutSession' => $checkoutSession]);
})->name('checkout-success');
```

<a name="checkout-promotion-codes"></a>
#### 프로모션 코드 (Promotion Codes)

Stripe 기본 Checkout은 고객이 직접 프로모션 코드를 등록하는 기능을 제공하지 않습니다. `allowPromotionCodes` 메서드로 활성화할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 단일 청구 Checkout (Single Charge Checkouts)

Stripe 대시보드에 등록되지 않은 즉석 제품 결제도 가능합니다. `checkoutCharge` 메서드에 금액, 상품명, 수량을 전달해 Checkout 세션을 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 는 Stripe에 새 제품과 가격을 생성하므로, 미리 Stripe 대시보드에 제품을 만들어 `checkout` 메서드 사용을 권장합니다.

<a name="subscription-checkouts"></a>
### 구독 Checkout (Subscription Checkouts)

> [!WARNING]
> Stripe Checkout 기반 구독은 Stripe 대시보드에서 `customer.subscription.created` 웹훅이 반드시 활성화되어야 합니다. 이 웹훅이 구독 데이터를 애플리케이션으로 동기화합니다.

Cashier 구독 빌더 메서드 체인으로 구독을 정의한 뒤 `checkout` 메서드를 호출하면 Checkout 세션이 시작됩니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

성공 및 취소 URL도 지정 가능:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

프로모션 코드도 허용 가능합니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!WARNING]
> Stripe Checkout은 구독 빌더에서 `anchorBillingCycleOn` 메서드, 정산 설정, 결제 동작 설정 등의 일부 옵션을 지원하지 않습니다. 자세한 사항은 [Stripe Checkout 세션 API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout 체험 기간

Checkout 체험 기간을 지정할 수 있긴 하지만, 최소 48시간 이상이어야 합니다:

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독과 웹훅

Stripe와 Cashier는 웹훅으로 구독 상태를 업데이트하므로, 고객이 결제 완료 후 앱 복귀 시점에 구독이 아직 활성화되지 않을 수 있습니다. 이럴 때는 결제 또는 구독 대기 중임을 사용자에게 알리는 메시지 표시가 필요합니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집 (Collecting Tax IDs)

Checkout 세션에서 고객 세금 ID 수집 기능을 활성화하려면 `collectTaxIds` 메서드를 체인하세요:

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

체크박스가 활성화되어 고객이 회사로 구매 시 세금 ID 입력을 요청합니다.

> [!WARNING]
> [자동 세금 계산](#tax-configuration)을 설정했다면 이 옵션을 따로 호출할 필요 없습니다.

<a name="guest-checkouts"></a>
### 게스트 Checkout (Guest Checkouts)

계정이 없는 비회원 게스트용 Checkout 세션은 `Checkout::guest` 메서드를 사용해 생성합니다:

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()->create('price_tshirt', [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

추가로 프로모션 코드도 설정 가능:

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()
        ->withPromotionCode('promo-code')
        ->create('price_tshirt', [
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```

체크아웃 완료 시 Stripe가 `checkout.session.completed` 이벤트를 발생시키므로, 웹훅 설정을 반드시 완료하고 Cashier에서 처리하세요.

<a name="handling-failed-payments"></a>
## 실패한 결제 처리 (Handling Failed Payments)

가끔 구독이나 단일 결제 실패 시 `Laravel\Cashier\Exceptions\IncompletePayment` 예외가 발생합니다. 이를 잡아 다음 두 가지 방법 중 하나로 대응하세요.

첫째, Cashier 제공 결제 확인 페이지로 리다이렉트하는 방식입니다. 이 페이지는 결제 재확인 및 Stripe가 추가 보안 인증(예: 3D Secure)을 진행하도록 안내합니다. 예:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $subscription = $user->newSubscription('default', 'price_monthly')
        ->create($paymentMethod);
} catch (IncompletePayment $exception) {
    return redirect()->route(
        'cashier.payment',
        [$exception->payment->id, 'redirect' => route('home')]
    );
}
```

결제 확인 후 지정 URL로 이동하면 URL 쿼리에 `message` 문자열과 `success` 불리언 값이 추가됩니다. 현재 결제 페이지는 다음 결제 수단을 지원합니다:

- 신용카드
- 알리페이
- 반콘탁
- BECS 직불
- EPS
- 기로페이
- iDEAL
- SEPA 직불

둘째, Stripe 대시보드에서 [자동 청구 이메일](https://dashboard.stripe.com/account/billing/automatic)을 설정할 수도 있습니다. 실패 시 사용자에게 별도 청구 안내 메일이 발송됩니다.

`IncompletePayment` 예외는 `charge`, `invoiceFor`, `invoice` 메서드 및 구독 `create`, `incrementAndInvoice`, `swapAndInvoice` 메서드 등에서 발생할 수 있습니다.

미완료 결제 상태 확인은 다음과 같습니다:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

예외 인스턴스의 `payment` 속성을 통해 상태 세부정보를 확인하세요:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 인텐트 상태 조회
    $exception->payment->status;

    // 특정 조건 확인
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="confirming-payments"></a>
### 결제 확인 (Confirming Payments)

일부 결제 수단(예: SEPA)의 경우 추가 맞춤 결제 확인 정보(예: 계약서 정보)가 필요할 수 있습니다. `withPaymentConfirmationOptions` 메서드로 결제 확인 옵션을 넘깁니다:

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

Stripe API 문서(https://stripe.com/docs/api/payment_intents/confirm)에서 허용 옵션을 확인하세요.

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증 (Strong Customer Authentication, SCA)

EU 내 결제는 2019년 9월 시행된 PSD2, SCA 규정을 반드시 준수해야 합니다. Stripe와 Cashier는 이를 지원하는 기능을 제공합니다.

> [!WARNING]
> 시작 전 [Stripe PSD2 & SCA 가이드](https://stripe.com/guides/strong-customer-authentication)와 [새 SCA API 문서](https://stripe.com/docs/strong-customer-authentication)를 꼭 읽어보세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 확인이 필요한 결제

SCA에 따라 추가 인증이 요구될 수 있으며, 이때도 `IncompletePayment` 예외가 발생합니다. [실패한 결제 처리](#handling-failed-payments) 내용을 참고해 대응하세요.

Stripe가 제공하는 결제화면은 카드사별 추가 인증, 소액 청구, 디바이스 인증 등 여러 방법으로 구성될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체 상태

추가 확인 필요 결제 중인 구독은 `stripe_status` DB 컬럼에 `incomplete` 또는 `past_due` 상태로 표시됩니다. 결제 승인이 완료되면 Stripe 웹훅으로 구독 활성화가 자동 처리됩니다.

`incomplete` 및 `past_due` 상태에 관해서는 [관련 문서](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>
### 오프 세션 결제 알림

SCA 규정상 구독 갱신 시 오프 세션 결제도 가끔 추가 인증이 필요할 수 있습니다. Cashier는 이때 고객에게 알림을 보낼 수 있습니다. 알림 클래스를 `CASHIER_PAYMENT_NOTIFICATION` 환경변수로 지정하세요. 기본적으로는 비활성화되어 있습니다. 기본 제공 알림 클래스를 써도 되고, 원하는대로 커스텀해도 무방합니다:

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

알림 정상 작동하려면 앱에 Stripe 웹훅([`invoice.payment_action_required`](#handling-stripe-webhooks))도 활성화하고, 청구 가능 모델이 Laravel `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다.

> [!WARNING]
> 알림은 수동 결제에도 보내집니다. Stripe는 수동/오프 세션 여부를 구분하지 못하지만, 이미 확인한 결제는 중복 확인이 불가해 이중 과금 걱정은 없습니다.

<a name="stripe-sdk"></a>
## Stripe SDK

Cashier 객체는 Stripe SDK 객체를 감싸고 있으므로 필요시 원본 객체에 접근할 수 있습니다.

Stripe 구독 객체를 직접 수정할 때:

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

Stripe 구독 객체를 업데이트하려면:

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Cashier::stripe()` 로 Stripe SDK 클라이언트에 바로 접근해 가격 리스트 등 조회할 수 있습니다:

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트 (Testing)

Cashier 사용하는 애플리케이션 테스트 시 실제 Stripe API 호출을 모킹해도 되지만, Cashier 동작 일부를 재구현해야 해 권장하지 않습니다. 테스트 시 Stripe API를 그대로 호출하는 게 신뢰성이 높으며 느린 테스트는 별도 그룹으로 분리하세요.

Cashier 내 테스트가 자체적으로 충분하므로, 애플리케이션 구독 및 결제 흐름 테스트에 집중하세요.

`phpunit.xml` 에 테스트용 Stripe 비밀키도 설정해야 합니다:

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

이렇게 하면 실제 Stripe 테스트 환경에 요청이 전송됩니다. 테스트용 Stripe 계정 내에 미리 가격 및 구독 데이터를 준비해두세요.

> [!NOTE]
> 카드 거부 및 실패 등 다양한 시나리오 테스트는 Stripe가 제공하는 [테스트 카드 번호 및 토큰](https://stripe.com/docs/testing)을 활용하세요.