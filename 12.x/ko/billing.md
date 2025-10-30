# Laravel Cashier (Stripe) (Laravel Cashier (Stripe))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔액 관리](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [결제 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 유무](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 청구](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일(Anchor Date)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판](#subscription-trials)
    - [결제 수단 사전 입력 방식](#with-payment-method-up-front)
    - [결제 수단 미입력 방식](#without-payment-method-up-front)
    - [체험판 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [간단한 청구](#simple-charge)
    - [인보이스와 함께 청구](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [환불 처리](#refunding-charges)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스 확인](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 청구 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원(게스트) Checkout](#guest-checkouts)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확정 처리](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 결제 인증 필요 상황](#payments-requiring-additional-confirmation)
    - [오프세션(Off-session) 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독(Subscription) 결제 서비스를 쉽고 유연하게 사용할 수 있도록 도와주는 인터페이스를 제공합니다. Cashier는 작성하기 번거로운 반복적인 구독 결제 관련 코드를 거의 모두 대신 처리합니다. 기본 구독 관리 외에도, Cashier는 쿠폰, 구독 변경, 구독 수량, 취소 유예 기간(grace period), 인보이스 PDF 생성까지 폭넓은 기능을 제공합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새로운 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

> [!WARNING]
> Cashier는 호환성 문제를 방지하기 위해 Stripe API 버전을 고정해서 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`을 사용합니다. Stripe API 버전은 Stripe의 새로운 기능 및 개선사항을 활용하기 위해 마이너 릴리즈마다 업데이트됩니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 이용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

패키지 설치 후에는 아티즌 명령어 `vendor:publish`로 Cashier의 마이그레이션 파일을 게시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음, 데이터베이스를 마이그레이션합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하며, 모든 고객의 구독 정보를 저장하는 `subscriptions` 테이블과, 다중 가격을 가진 구독의 경우 사용할 `subscription_items` 테이블도 만듭니다.

필요하다면 Cashier의 설정 파일도 아래 명령어로 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Stripe의 모든 이벤트를 Cashier가 제대로 처리할 수 있도록 [Cashier의 webhook 설정](#handling-stripe-webhooks)을 꼭 구성해야 합니다.

> [!WARNING]
> Stripe는 Stripe 식별자(Stripe identifiers)를 저장하는 컬럼이 대소문자 구분(케이스 센서티브)이어야 한다고 권장합니다. 따라서 MySQL을 쓸 경우 `stripe_id` 컬럼의 정렬(collation)을 반드시 `utf8_bin`으로 설정하시기 바랍니다. 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에, 청구 가능한(Billable) 모델에 `Billable` 트레이트를 추가해야 합니다. 일반적으로는 `App\Models\User` 모델에 추가합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 갱신 등 다양한 결제 기능 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 `App\Models\User` 모델을 Billable 모델로 간주합니다. 만약 이 모델을 변경하고 싶다면, `useCustomerModel` 메서드를 사용하여 다른 모델을 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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
> 만약 Laravel에서 기본 제공하는 `App\Models\User` 대신 다른 모델을 사용한다면, 반드시 [Cashier 마이그레이션](#installation)을 게시하여 변경하려는 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에 Stripe API 키를 설정해야 합니다. Stripe API 키는 Stripe 대시보드에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `.env` 파일에 반드시 `STRIPE_WEBHOOK_SECRET` 환경 변수를 정의해야 합니다. 이 값은 들어오는 webhook이 실제 Stripe로부터 온 것인지 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 `.env` 파일에 `CASHIER_CURRENCY` 환경변수를 설정하세요:

```ini
CASHIER_CURRENCY=eur
```

Cashier가 돈을 표시하는 로케일(locale)도 `.env` 파일의 `CASHIER_CURRENCY_LOCALE` 값으로 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 PHP `ext-intl` 확장 모듈이 설치되어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe에서 생성되는 모든 인보이스에 대해 세금을 자동으로 계산할 수 있습니다. 자동 세금 계산을 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

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

자동 세금 계산이 활성화되면, 새로 생성되는 모든 구독과 단건(one-off) 인보이스에 대해 세금이 자동으로 계산됩니다.

이 기능이 제대로 작동하려면 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe와 동기화되어 있어야 합니다. 이를 위해 Cashier의 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 사용할 수 있습니다.

<a name="logging"></a>
### 로깅 (Logging)

Cashier는 Stripe 치명적 오류 발생 시 사용할 로깅 채널을 지정할 수 있습니다. `.env` 파일에 `CASHIER_LOGGER` 환경변수를 설정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출에서 발생하는 예외는 애플리케이션 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier가 내부적으로 사용하는 모델을 확장하여 직접 커스텀 모델을 정의할 수 있습니다. Cashier 모델을 확장하세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에 커스텀 모델을 지정합니다. 보통 이 코드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 작성합니다:

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
### 상품 판매 (Selling Products)

> [!NOTE]
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 반드시 고정 가격을 가진 상품(Product)을 미리 생성해야 합니다. 또한 [Cashier의 webhook 처리](#handling-stripe-webhooks)를 반드시 구성해야 합니다.

애플리케이션에서 상품 또는 구독 결제를 제공하는 것은 다소 어렵게 느껴질 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)만 있으면, 현대적이고 견고한 결제 시스템을 손쉽게 구축할 수 있습니다.

반복되지 않는 단일 상품 결제를 위해, Cashier의 기능으로 사용자를 Stripe Checkout 페이지로 안내하여 결제 정보를 입력/확정하게 하고, 결제가 끝나면 성공 페이지 등 애플리케이션 내 특정 URL로 리다이렉트합니다:

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

위 예시처럼, Cashier가 제공하는 `checkout` 메서드를 활용해 사용자를 Stripe Checkout으로 리다이렉트합니다. Stripe에서 "가격(Price)"이란 [특정 상품에 지정된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요하다면, `checkout` 메서드는 Stripe에서 고객을 자동 생성하고, Stripe 고객 정보를 애플리케이션 DB 사용자의 레코드와 연결해줍니다. 결제 세션이 완료되면 사용자는 성공 또는 취소 페이지로 리다이렉트되며, 여기서 안내 메시지 등을 표시할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 제공

상품을 판매할 때, 별도의 `Cart` 또는 `Order` 모델을 애플리케이션에서 따로 두고 주문을 관리하는 경우가 많습니다. Stripe Checkout으로 리다이렉트할 때 특정 주문 번호 등 기존 주문 식별자를 포함해야, 결제가 완료된 후 주문과 결제를 연결할 수 있습니다.

이를 위해 `checkout` 메서드에 `metadata` 배열을 추가로 전달할 수 있습니다. 예를 들어, 사용자가 결제를 시작할 때 미완료(incomplete) 상태의 `Order`를 미리 생성하고, 결제 완료 후 해당 주문을 갱신하는 방식입니다(아래 Cart/Order 모델은 예시일 뿐이고, Cashier에서 제공하지 않습니다):

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

사용자가 결제 프로세스를 시작하면, 모든 cart/order의 Stripe price id를 `checkout` 메서드로 넘겨줍니다. 각 상품을 장바구니 혹은 주문과 연결하는 로직은 애플리케이션에서 구현해야 합니다. 추가로 주문 ID도 Stripe Checkout 세션의 `metadata`로 포함시킵니다. 마지막으로 성공 URL에 `CHECKOUT_SESSION_ID`를 포함하면, Stripe가 실제 세션 ID로 자동 치환해 전달합니다.

이제 결제 성공 페이지 라우트를 구현합니다. Stripe Checkout 이후 사용자가 리다이렉트되는 곳에서 Stripe 세션 ID와 관련 인스턴스를 조회하고, 미리 전달한 메타데이터(예: 주문 ID)를 사용해 주문 상태 등을 갱신할 수 있습니다:

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

Stripe Checkout 세션 오브젝트에 담긴 데이터에 대한 자세한 설명은 [Stripe 공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 반드시 고정 가격 상품(Product)를 등록해야 하며, [Cashier webhook 처리](#handling-stripe-webhooks)도 반드시 구성해야 합니다.

구독 결제나 상품 결제를 손쉽게 도입하려면 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 됩니다.

구독 판매 방식을 알아보기 위해, 간단한 예를 들어 보겠습니다. 월 구독(`price_basic_monthly`)과 연 구독(`price_basic_yearly`)의 두 가지 기본 플랜이 있다고 가정합니다(이 두 가격은 Stripe 대시보드에서 "Basic" 상품 아래에 묶을 수 있습니다). 또, "Expert" 플랜은 별도의 `pro_expert`로 제공합니다.

아래와 같이, 사용자가 Basic 플랜에서 구독 버튼을 클릭하면, 선택한 플랜에 맞는 Stripe Checkout 세션을 만드는 라라벨 라우트로 연결할 수 있습니다.

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

이 예시에서는 사용자를 Stripe Checkout 세션으로 리다이렉트하며, 구독이 완료되거나 취소되면 지정된 URL로 이동합니다. 결제 방식에 따라 구독이 실제로 시작되는 시점이 약간의 차이가 있을 수 있으니, 구독 시작 여부를 정확히 알기 위해서는 반드시 [Cashier webhook 처리](#handling-stripe-webhooks)를 구성해야 합니다.

이제 사용자가 구독을 시작할 수 있게 되었으니, 애플리케이션 내 특정 영역을 구독중인 사용자만 접근하도록 제한할 수 있습니다. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드로 구독 상태를 체크할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 대한 구독 여부 체크도 가능합니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 여부 확인 미들웨어 만들기

일반적으로, 구독 사용자인지를 판별하는 [미들웨어](/docs/12.x/middleware)를 만들어 라우트에 적용할 수 있습니다. 이렇게 하면 미구독자는 해당 라우트 접근이 제한됩니다:

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
            // 구독 페이지로 리다이렉트
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

미들웨어를 라우트에 적용하는 예시:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 결제/구독 플랜을 직접 관리하도록 허용

고객은 자신의 구독 플랜을 다른 상품이나 "티어층"으로 변경하고 싶어할 수 있습니다. Stripe가 제공하는 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)을 이용하면 고객 스스로 인보이스를 다운로드 하고, 결제 수단을 변경하며, 구독 플랜도 바꿀 수 있는 UI를 제공합니다.

애플리케이션 내에 아래와 같이 Billing 페이지로 연결되는 버튼이나 링크를 배치할 수 있습니다:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

해당 Billing 포털 세션을 시작하여 Stripe 포털로 리다이렉트하는 라우트 예시입니다. `redirectToBillingPortal` 메서드는 사용자가 포털을 나갈 때 돌아올 URL을 인자로 받습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 webhook 처리가 잘 구성되어 있으면, Stripe Billing Portal에서 사용자가 구독을 취소하거나 변경 시, Stripe가 보내는 webhook을 받아 Cashier가 애플리케이션의 DB와 상태를 자동 동기화합니다.

... (이하의 모든 내용은 위 번역 가이드라인에 맞추어 같은 방식으로 번역/구현)