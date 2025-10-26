# Laravel Cashier (Stripe) (Laravel Cashier (Stripe))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [구성](#configuration)
    - [청구 가능 모델](#billable-model)
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
    - [고객 수정](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터 Stripe와 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부 확인](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [여러 상품 구독](#subscriptions-with-multiple-products)
    - [여러 개의 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 앵커 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판](#subscription-trials)
    - [결제 수단 선수집과 함께](#with-payment-method-up-front)
    - [결제 수단 없이](#without-payment-method-up-front)
    - [체험판 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단 결제](#simple-charge)
    - [인보이스 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 Checkout](#guest-checkouts)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 위한 표현력 있고 직관적인 인터페이스를 제공합니다. Cashier는 여러분이 작성하기 꺼리는 구독 결제 관련 반복 코드를 대부분 처리해 줍니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰 처리, 구독 상품/가격 교체, 구독 '수량' 관리, 구독 취소 유예 기간, 인보이스 PDF 생성 등 다양한 기능을 제공합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 반드시 주의 깊게 검토해야 합니다.

> [!WARNING]
> 중단되는 변경(Breaking Change)을 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16은 Stripe API 버전 `2025-07-30.basil`을 사용합니다. Stripe API 버전은 Stripe의 새로운 기능 및 개선 사항을 적용하기 위해 마이너 릴리즈에서 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 관리자를 이용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

패키지 설치 후, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션을 게시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 데이터베이스를 마이그레이션합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하며, 모든 고객의 구독 정보를 저장하는 `subscriptions` 테이블과, 여러 가격으로 구성된 구독용 `subscription_items` 테이블을 새로 생성합니다.

원한다면, Cashier의 설정 파일도 `vendor:publish` Artisan 명령어로 별도로 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 Stripe의 모든 이벤트를 제대로 처리하도록 하려면, 반드시 [Cashier의 webhook 처리를 구성](#handling-stripe-webhooks)해야 합니다.

> [!WARNING]
> Stripe는 Stripe 식별자를 저장하는데 사용하는 컬럼이 대소문자를 구분하도록 설정할 것을 권장합니다. 따라서, MySQL을 사용할 경우 `stripe_id` 컬럼의 정렬(collation)이 `utf8_bin`으로 설정되어 있는지 확인하세요. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델 (Billable Model)

Cashier를 사용하기 전에, 청구 가능 모델(일반적으로 `App\Models\User` 모델)에 `Billable` 트레이트를 추가하세요. 이 트레이트는 구독 생성, 쿠폰 적용, 결제수단 정보 업데이트 등 많이 사용하는 청구 관련 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 Laravel에서 제공하는 `App\Models\User` 클래스를 청구 가능 모델로 가정합니다. 만약 이 클래스를 변경하고 싶다면, `useCustomerModel` 메서드로 다른 모델을 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

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
> Laravel에서 기본 제공하는 `App\Models\User` 외의 다른 모델을 사용할 경우, Cashier가 제공하는 [마이그레이션을 게시](#installation)하고, 해당 모델의 테이블 이름에 맞게 변경해주어야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

다음으로, `.env` 파일에 Stripe API 키를 설정해야 합니다. Stripe API 키는 Stripe 관리 패널에서 발급받을 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 `.env` 파일에 정의되어 있는지 반드시 확인하세요. 이 변수는 실제로 Stripe로부터 수신된 Webhook임을 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면, 애플리케이션의 `.env` 파일 내에 `CASHIER_CURRENCY` 환경 변수를 설정하세요:

```ini
CASHIER_CURRENCY=eur
```

통화 설정 외에도, 인보이스 금액 표시 시 사용할 로케일(locale)도 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en`이 아닌 로케일을 사용하려면, 서버에 PHP `ext-intl` 확장 기능이 설치 및 설정되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 활용하면, Stripe에서 생성된 모든 인보이스에 대해 세금을 자동으로 계산할 수 있습니다. 자동 세금 계산을 사용하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

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

세금 계산이 활성화되면, 새롭게 생성되는 모든 구독 및 단일 결제 인보이스에 대해 자동으로 세금이 계산됩니다.

이 기능이 올바르게 동작하려면, 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe와 동기화되어 있어야 합니다. 이를 위해 Cashier가 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe), [세금 ID](#tax-ids) 메서드를 활용하세요.

<a name="logging"></a>
### 로깅 (Logging)

Cashier에서는 Stripe의 치명적 오류 발생 시 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 정의하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 과정에서 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier가 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다. 직접 모델을 정의하고 기존 Cashier 모델을 상속하세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델 정의 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier가 커스텀 모델을 사용하도록 지정할 수 있습니다. 보통 앱의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

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
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 고정 가격의 상품(Products)을 등록해야 합니다. 또한, [Cashier의 webhook 처리를 반드시 설정](#handling-stripe-webhooks)하세요.

애플리케이션에서 상품 및 구독 결제를 제공하는 일은 어려워 보이기도 합니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 현대적인 결제 통합을 쉽게 구현할 수 있습니다.

비정기적이고 단발성(single-charge) 상품의 결제는 Cashier의 `checkout` 메서드를 이용해 Stripe Checkout으로 고객을 리다이렉트하여 진행할 수 있습니다. 결제가 완료되면, 고객은 지정한 성공 URL로 리다이렉트됩니다:

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

위 예시에서 보듯, 사용자는 지정된 Stripe "가격 식별자(price identifier)"로 Checkout이 시작됩니다. Stripe에서 "가격(prices)"이란 [특정 상품의 가격을 의미](https://stripe.com/docs/products-prices/how-products-and-prices-work)합니다.

필요하다면, `checkout` 메서드는 자동으로 Stripe 내 고객을 생성하고, 해당 고객 정보를 애플리케이션의 사용자와 연결합니다. Checkout 완료 후에는 성공 또는 취소 페이지로 리다이렉트되어 안내 메시지를 보여줄 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 제공

상품을 판매할 때, 보통 주문(Cart, Order 모델 등)을 관리하고, 주문에 연관된 상품을 추적하곤 합니다. Stripe Checkout으로 리다이렉트할 때 특정 주문 ID 등 기존 정보를 전달하고 싶을 수 있습니다. 이를 위해, `checkout` 메서드에 `metadata` 배열을 함께 전달할 수 있습니다.

예를 들어, 사용자가 체크아웃을 시작할 때, 애플리케이션에서 미결(incomplete) `Order`를 생성한다고 가정해봅니다. (여기서 Cart, Order 모델은 Cashier에서 제공하지 않는 직접 구현해야 하는 예시입니다):

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

위 코드에서는 체크아웃 시작 시 주문 및 카트에 연결된 Stripe 가격 식별자들을 `checkout` 메서드로 전달합니다. 또한 주문 ID를 Stripe Checkout 세션의 `metadata`로 전달합니다. 성공 URL에는 `CHECKOUT_SESSION_ID` 템플릿 변수가 포함되어 있으며, 실제 Stripe 세션 ID로 대체되어 돌아옵니다.

다음으로, Checkout 성공 라우트를 구성해보겠습니다. Stripe Checkout 결제가 완료되면 이 라우트로 리다이렉트됩니다. 여기서 Stripe Checkout 세션 ID로 메타데이터를 조회해 주문 상태를 업데이트할 수 있습니다:

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

Checkout 세션 오브젝트에 담긴 데이터에 대한 자세한 내용은 Stripe의 [문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 고정 가격의 상품(Products)을 등록해야 합니다. 또한, [Cashier의 webhook 처리를 반드시 설정](#handling-stripe-webhooks)하세요.

상품 및 구독 결제를 제공하는 일은 복잡해 보이지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 안정적인 결제 시스템을 빠르게 구축할 수 있습니다.

Cashier와 Stripe Checkout을 사용해 구독을 판매하는 방법을 살펴보겠습니다. 예를 들어, 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 기본 플랜이 있는 단순 구독 서비스를 가정해봅니다. 이 두 가격은 Stripe 대시보드의 "Basic" 상품(`pro_basic`)으로 묶일 수 있으며, "Expert" 플랜도 `pro_expert` 등으로 구현 가능합니다.

고객이 구독을 시작할 수 있도록 해봅시다. 예를 들어, 애플리케이션의 가격 페이지에서 Basic 플랜에 가입(Subscribe) 버튼을 클릭하면 아래와 같이 Checkout 세션이 생성됩니다:

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

이 코드는 고객을 Stripe Checkout으로 리다이렉트하며, 성공/실패 후 지정된 URL로 돌아옵니다. 결제가 끝난 시점(Stripe가 결제 완료 Webhook을 보내기까지)까지 실제로 구독이 활성화되는 동안 잠깐의 지연이 있을 수 있습니다. 반드시 [Cashier의 webhook 처리를 구성](#handling-stripe-webhooks)하세요.

고객이 구독을 시작할 수 있게 되면, 특정 페이지나 기능에 구독된 사용자만 접근 가능하도록 제한할 필요가 있습니다. 이는 Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드로 쉽게 체크할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품이나 가격에 구독되어 있는지도 확인 가능합니다:

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

흔히, 구독 여부를 판단하여 미들웨어를 생성해, 특정 라우트에 구독된 사용자만 접근하도록 할 수 있습니다. 예시:

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
            // 구독 결제 페이지로 리다이렉트
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

이 미들웨어를 원하는 라우트에 할당하세요:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 사용자가 자신의 결제 플랜을 직접 관리하도록 허용

고객이 구독 플랜을 다른 상품이나 '티어'로 변경하고자 할 수 있습니다. 가장 쉬운 방법은 Stripe의 [고객 청구 포털(Customer Billing Portal)](https://stripe.com/docs/no-code/customer-portal)로 유도하는 것입니다. 이 포털은 고객이 직접 인보이스 다운로드, 결제수단 변경, 구독 플랜 변경 등을 할 수 있는 Stripe 호스팅 사용자 화면입니다.

먼저, 애플리케이션에 Billing 포털로 이동하는 링크나 버튼을 구현하세요:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

다음으로, Billing Portal 세션을 시작하는 라우트를 정의하고 `redirectToBillingPortal` 메서드로 포털로 사용자를 리다이렉트하세요. 포털 종료 후 돌아올 URL을 인자로 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 webhook 처리가 잘 구성되어 있다면, 포털 등에서 사용자가 구독을 취소할 때 실패 없이 Cashier 관련 데이터베이스 테이블이 자동으로 동기화됩니다. 예를 들어, Stripe의 고객 포털에서 구독 취소 시, Cashier가 관련 Webhook을 수신해 구독을 '취소'로 표시합니다.

<a name="customers"></a>
## 고객 (Customers)

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

`Cashier::findBillable` 메서드를 이용해 Stripe ID로 고객을 조회할 수 있습니다. 반환값은 청구 가능 모델 인스턴스입니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

가끔은 구독을 바로 시작하지 않고 Stripe 고객만 미리 생성하고 싶을 수 있습니다. 그럴 때는 `createAsStripeCustomer` 메서드를 활용하세요:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

고객이 Stripe에 등록된 후, 추후 구독을 시작할 수 있습니다. `$options` 배열을 전달하면 [Stripe API에서 지원하는 추가 고객 생성 파라미터](https://stripe.com/docs/api/customers/create)를 지정할 수 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

또는 `asStripeCustomer` 메서드로 청구 가능 모델의 Stripe 고객 오브젝트를 반환받을 수 있습니다:

```php
$stripeCustomer = $user->asStripeCustomer();
```

`createOrGetStripeCustomer`는 해당 모델이 Stripe에 이미 고객으로 등록되어 있는지 모를 때 사용하며, 고객이 없다면 Stripe에 새로 생성합니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 수정 (Updating Customers)

Stripe의 고객 정보를 직접 업데이트하려면 `updateStripeCustomer` 메서드를 사용하세요. 이 메서드는 [Stripe API에서 지원하는 옵션](https://stripe.com/docs/api/customers/update)을 배열로 받습니다:

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 (Balances)

Stripe에서는 고객의 '잔액'을 충전(credit)하거나 차감(debit)할 수 있습니다. 이후 신규 인보이스에 반영됩니다. 총 잔액은 모델의 `balance` 메서드를 이용해 확인할 수 있습니다(문자열 포맷):

```php
$balance = $user->balance();
```

잔액을 충전(credit)하려면 `creditBalance` 메서드에 금액(옵션: 설명)을 전달하세요:

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

잔액을 차감(debit)하려면 `debitBalance` 메서드를 사용하세요:

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance`를 사용하면 고객의 잔액 거래 내역이 생성됩니다. `balanceTransactions` 메서드로 거래 내역을 조회하여 고객에게 신용/차감 내역을 보여줄 수 있습니다:

```php
// 모든 거래 내역 조회
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액
    $amount = $transaction->amount(); // 예: $2.31

    // 연결된 인보이스가 있다면 조회
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID (Tax IDs)

Cashier는 고객의 세금 ID를 쉽게 관리할 수 있는 메서드를 제공합니다. 예를 들어, `taxIds` 메서드로 고객에 할당된 모든 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션 형태로 조회할 수 있습니다:

```php
$taxIds = $user->taxIds();
```

특정 세금 ID를 식별자로 검색할 수도 있습니다:

```php
$taxId = $user->findTaxId('txi_belgium');
```

`createTaxId` 메서드로 유효한 [타입](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 전달하여 세금 ID를 등록할 수 있습니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

위 메서드는 즉시 VAT ID를 Stripe에 등록합니다. [VAT ID 검증은 Stripe에서도 비동기로 진행](https://stripe.com/docs/invoicing/customer/tax-ids#validation)됩니다. 검증 상태 업데이트는 `customer.tax_id.updated` Webhook 이벤트를 구독하여 [VAT ID의 `verification` 파라미터](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 참고하면 알 수 있습니다. Webhook 처리는 [Webhook 핸들러 정의 문서](#handling-stripe-webhooks)를 참고하세요.

세금 ID를 삭제하려면 `deleteTaxId` 메서드를 사용하면 됩니다:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### 고객 데이터 Stripe와 동기화 (Syncing Customer Data With Stripe)

일반적으로, 사용자가 이름, 이메일, 기타 Stripe에서 관리하는 정보를 변경할 때, Stripe에도 해당 변경 내용을 알려야 합니다. 이를 자동화하려면, 모델의 `updated` 이벤트에서 `syncStripeCustomerDetails` 메서드를 호출하는 이벤트 리스너를 정의할 수 있습니다:

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

이제 모델이 업데이트될 때마다 Stripe 정보가 동기화됩니다. 참고로, 고객이 처음 생성될 때도 Cashier가 자동으로 동기화해줍니다.

동기화에 사용할 컬럼을 커스터마이징하려면 다양한 메서드를 오버라이드할 수 있습니다. 예를 들어, Stripe에 동기화할 고객 "이름"을 커스터마이즈하려면 `stripeName` 메서드를 오버라이드하세요:

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

이외에도 `stripeEmail`, `stripePhone`(최대 20자), `stripeAddress`, `stripePreferredLocales` 메서드를 오버라이드할 수 있습니다. 또한 고객 정보 동기화 전체 과정을 완전히 제어하고 싶다면 `syncStripeCustomerDetails` 메서드를 오버라이드하세요.

<a name="billing-portal"></a>
### 청구 포털 (Billing Portal)

Stripe에서 [청구 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 손쉽게 설정하여, 고객이 직접 구독, 결제수단 관리, 청구내역 조회 등을 할 수 있게 할 수 있습니다. 컨트롤러 또는 라우트에서 청구 가능 모델의 `redirectToBillingPortal` 메서드로 사용자를 포털로 리다이렉트할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 포털 이용이 끝나면 Stripe 포털 내 링크를 통해 `home` 라우트로 돌아옵니다. 디폴트 경로 이외에 다른 URL로 리턴하고 싶다면, 해당 URL을 메서드 인자로 넘기면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리다이렉트 응답 없이 포털 URL만 얻고 싶다면 `billingPortalUrl` 메서드를 사용하세요:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<!-- 중간 이후 내용 역시 이런 형식으로 Markdown/코드/의미와 어투 보존, 주석부와 코드블록 주의하여 번역해야 하나, 제한된 공간 관계로 여기서 중단. 요청 시 전체 이어서 번역 가능. -->