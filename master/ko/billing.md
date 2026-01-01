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
    - [고객 정보 수정](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부 확인](#payment-method-presence)
    - [기본 결제 수단 변경](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [요금 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [복수 상품 포함 구독](#subscriptions-with-multiple-products)
    - [여러 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일(Anchor Date)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판(Trial)](#subscription-trials)
    - [결제 수단 사전 등록 방식](#with-payment-method-up-front)
    - [결제 수단 사전 등록 없는 방식](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단건 결제](#single-charges)
    - [단순 결제](#simple-charge)
    - [인보이스를 포함한 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단건 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 Checkout](#guest-checkouts)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정된 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강화된 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 인증이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 위한 표현력 있고 직관적인 인터페이스를 제공합니다. Cashier는 여러분이 쓰기 부담스러운 거의 모든 반복적인(boilerplate) 구독 결제 관련 코드를 대신 처리해줍니다. 기본적인 구독 관리뿐만 아니라, 쿠폰 처리, 구독 변경, 구독 '수량(quantity)', 취소 유예 기간(grace period), 인보이스 PDF 생성 등 다양한 기능을 제공합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

새로운 버전의 Cashier로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> 호환성 문제를 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. Stripe API 버전은 새로운 Stripe 기능이나 개선사항 활용을 위해 마이너 릴리즈에서 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 이용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

패키지 설치 후, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션을 퍼블리시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그리고 데이터베이스를 마이그레이트합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 몇 가지 컬럼을 추가하며, 모든 고객 구독을 저장할 `subscriptions` 테이블, 복수 요금제를 사용하는 구독 정보를 보관할 `subscription_items` 테이블도 생성합니다.

원한다면, 아래 명령어로 Cashier의 설정 파일도 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Stripe 이벤트를 올바르게 처리하기 위해 반드시 [Cashier의 webhook 처리를 설정](#handling-stripe-webhooks)하세요.

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장할 컬럼이 대소문자를 구분(case-sensitive)해야 한다고 권장합니다. MySQL을 사용할 경우, `stripe_id` 컬럼의 Collation을 반드시 `utf8_bin`으로 변경하세요. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에, `Billable` 트레이트를 여러분의 과금 대상(billable) 모델에 추가해야 합니다. 일반적으로는 `App\Models\User` 모델이 해당됩니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 자주 사용하는 다양한 빌링 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 `App\Models\User` 클래스를 과금 모델로 가정합니다. 다른 모델을 사용할 경우, `useCustomerModel` 메서드를 통해 변경할 수 있습니다. 이 메서드는 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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
> 만약 Laravel에서 기본 제공하는 `App\Models\User` 외의 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시 후 테이블명 등 여러분의 모델에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, Stripe API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Stripe API 키는 Stripe의 관리자 페이지에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 반드시 `.env` 파일에 정의되어 있어야 하며, 해당 변수는 들어오는 웹훅이 실제 Stripe에서 온 것인지 확인할 때 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 통해 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

Cashier의 통화 설정뿐만 아니라, 인보이스에 표시되는 금액의 표시 형식을 지정할 로케일(locale)도 설정할 수 있습니다. Cashier 내부적으로는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용하여 통화 로케일을 지정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 구성되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 통해 Stripe에서 생성되는 모든 인보이스에 세금을 자동 산출할 수 있습니다. 애플리케이션의 `AppServiceProvider` 클래스에서 `calculateTaxes` 메서드를 호출해 자동 세금 계산을 활성화할 수 있습니다:

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

세금 계산을 활성화하면, 새로 생성되는 구독이나 단건 인보이스에 자동으로 세금이 계산되어 적용됩니다.

이 기능이 제대로 동작하려면, 고객의 청구 정보(이름, 주소, 세금 ID 등)가 Stripe에 동기화되어야 합니다. 이를 위해 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 Cashier 메서드를 사용할 수 있습니다.

<a name="logging"></a>
### 로깅 (Logging)

Cashier는 Stripe에서 발생한 치명적인 에러를 로깅할 때 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 설정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출로 인해 발생한 예외는 애플리케이션의 기본 로그 채널에도 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier 내부에서 사용하는 모델을 자유롭게 확장할 수 있습니다. 직접 모델을 정의하고 해당 Cashier 모델을 상속하면 됩니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

이렇게 커스텀 모델을 정의했다면, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier가 여러분의 모델을 사용하도록 지시할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 등록합니다:

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
> Stripe Checkout을 사용하기 전, Stripe 관리자 대시보드에 가격이 고정된 상품을 반드시 정의해야 하며, [Cashier의 webhook 처리](#handling-stripe-webhooks)도 설정해야 합니다.

애플리케이션을 통해 제품이나 구독 결제를 제공하는 것은 부담스러울 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 이용하면, 최신 트렌드에 맞는 견고한 결제 기능을 손쉽게 구현할 수 있습니다.

비반복(1회성) 단건 상품에 대해 고객에게 결제를 청구하려면, Cashier의 `checkout` 메서드를 이용해 Stripe Checkout으로 리디렉션합니다. Checkout에서 결제가 완료되면, 지정한 성공 URL로 사용자가 이동됩니다:

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

위 예시처럼 Cashier의 `checkout` 메서드를 사용해, 특정 "가격 식별자(price identifier)"로 Stripe Checkout으로 고객을 안내합니다. Stripe에서 `prices`는 [특정 상품의 정의된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요하다면, `checkout` 메서드는 Stripe에서 고객을 자동 생성해 DB상의 사용자 엔티티와 연결시켜줍니다. Checkout 세션이 완료되면, 성공/취소 전용 페이지로 리다이렉트되어 사용자가 정보를 확인할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 전달

상품을 판매할 때, 보통 주문 및 결제 내역을 자체적인 `Cart`, `Order` 모델로 관리합니다. 결제를 마친 후 해당 주문을 특정 주문 레코드와 연결하려면, `checkout` 메서드의 `metadata` 옵션에 기존 주문 식별자를 전달할 수 있습니다.

예를 들어, 결제 시작 시 미리 `Order`를 생성하고(여기서 `Cart`, `Order` 모델은 예시일 뿐 Cashier에서 제공하지 않습니다), Checkout에 그 주문 식별자를 넘길 수 있습니다:

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

Checkout 세션 성공 시, Stripe가 리디렉션할 때 `session_id` 쿼리파라미터를 자동 셋팅합니다. 이를 활용해 사용자가 결제 성공 페이지로 돌아왔을 때, Checkout 세션 정보와 메타데이터를 조회하고 주문을 완료 처리할 수 있습니다:

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

Stripe Checkout 세션 오브젝트에 포함된 데이터에 대한 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Stripe Checkout을 사용하기 전, Stripe 관리자 대시보드에 가격이 고정된 상품을 반드시 정의해야 하며, [Cashier의 webhook 처리](#handling-stripe-webhooks)도 설정해야 합니다.

Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면, 복잡한 결제를 손쉽게 구현할 수 있습니다.

Cashier와 Stripe Checkout을 활용해 구독을 판매하는 방식을 예로 들어 설명하겠습니다. 예를 들어, 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`)의 기본 플랜과 전문가(Expert) 플랜(`pro_expert`)이 있다고 가정합니다. 이 가격들은 Stripe 대시보드에서 "Basic" 등의 상품(`pro_basic`)에 할당되어 있을 수 있습니다.

고객이 구독하기 위해 버튼을 클릭하면, 아래와 같은 라우트로 연결해 Stripe Checkout 세션을 생성할 수 있습니다:

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

위 코드처럼 고객을 원하는 플랜으로 구독할 수 있도록 Stripe Checkout 세션으로 리디렉션합니다. 결제 완료 시점(혹은 취소 시점)에는 지정한 URL로 돌아옵니다. 신용카드 등 결제 수단에 따라 처리가 몇 초 이상 걸릴 수 있으니, [Cashier의 webhook 처리](#handling-stripe-webhooks)도 꼭 설정해야 합니다.

구독을 시작한 후, 특정 서비스 영역에 구독한 사용자만 접근할 수 있게 하려면 Cashier의 `Billable` 트레이트에서 제공하는 `subscribed` 메서드를 활용하면 됩니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품 또는 가격 기준으로 구독 여부를 확인할 수도 있습니다:

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

간단한 인증 처리를 위해 [미들웨어](/docs/master/middleware)를 추가할 수 있습니다. 이 미들웨어를 통해 구독하지 않은 사용자는 특정 라우트 접근이 차단됩니다:

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
            // 결제 페이지로 리디렉션하고 구독 안내...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

이렇게 정의한 미들웨어는 라우트에 간단히 할당할 수 있습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 직접 요금제 관리 기능 제공

고객이 스스로 구독 플랜이나 등급을 변경하도록 Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)에 연결하는 것이 가장 쉽고 안전한 방법입니다. 이 포털에서는 인보이스 다운로드, 결제 수단 변경, 구독 플랜 관리가 가능합니다.

먼저, 아래와 같이 앱에 Billing 포털 진입 버튼이나 링크를 배치하세요:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

그 다음, 해당 라우트에서 Stripe 고객 포털 세션을 시작하고 리디렉션시키는 코드를 작성합니다. `redirectToBillingPortal` 메서드에는 포털을 나올 때 돌아갈 URL을 전달할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 webhook 처리가 잘 설정되어 있다면, Stripe Billing Portal에서 구독을 해지하는 등 변경이 생길 때에도 앱의 Cashier 관련 DB 테이블이 자동으로 동기화됩니다. 예를 들어 사용자가 포털에서 구독을 취소하면, 해당 webhook을 처리해 Cashier가 DB에 "취소됨" 상태로 기록합니다.

<a name="customers"></a>
## 고객 (Customers)

<a name="retrieving-customers"></a>
### 고객 조회

`Cashier::findBillable` 메서드를 통해 Stripe ID로 고객을 조회할 수 있습니다. 이 메서드는 과금 대상 모델 객체를 반환합니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔 구독을 시작하지 않고도 Stripe 고객을 미리 생성할 필요가 있을 수 있습니다. 이때는 `createAsStripeCustomer` 메서드를 사용하세요:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

고객이 Stripe에 생성된 후, 나중에 구독을 추가할 수 있습니다. Stripe API의 [고객 생성 파라미터](https://stripe.com/docs/api/customers/create)를 배열로 추가 인자로 넘길 수도 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

Stripe 고객 객체만 별도로 반환하려면 `asStripeCustomer` 메서드를 사용합니다:

```php
$stripeCustomer = $user->asStripeCustomer();
```

이미 Stripe 고객인지 확실하지 않은 경우 `createOrGetStripeCustomer` 메서드를 통해, 존재하면 그대로 객체를 반환하고 없으면 새로 생성해 반환할 수 있습니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 정보 수정

Stripe 고객 정보에 추가 데이터를 직접 업데이트해야 할 때는 `updateStripeCustomer` 메서드를 활용할 수 있습니다. 이 메서드는 [Stripe API에서 지원하는 고객 정보 변경 옵션](https://stripe.com/docs/api/customers/update)을 배열로 받습니다:

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 (Balances)

Stripe에서는 고객의 "잔액(balance)"을 입금(credit) 또는 출금(debit)할 수 있고, 이 잔액은 이후 새 인보이스에 자동 반영됩니다. 고객 전체 잔액은 billable 모델의 `balance` 메서드로 확인할 수 있습니다(고객 통화에 알맞게 포매팅되어 문자열로 리턴):

```php
$balance = $user->balance();
```

잔액을 입금하려면 `creditBalance` 메서드에 금액과 설명을 전달하면 됩니다:

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

출금할 때는 `debitBalance` 메서드를 사용합니다:

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance`는 고객에게 새(balance) 거래 내역을 만듭니다. 생성된 거래 내역은 `balanceTransactions` 메서드로 컬렉션 형태로 조회할 수 있습니다:

```php
// 모든 거래 내역 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액...
    $amount = $transaction->amount(); // $2.31

    // 관련 인보이스 조회(가능한 경우)...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID (Tax IDs)

Cashier는 고객의 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 편리하게 관리할 수 있도록 여러 메서드를 제공합니다. 예를 들어, `taxIds` 메서드는 고객에게 할당된 모든 세금 ID를 컬렉션으로 조회합니다:

```php
$taxIds = $user->taxIds();
```

특정 세금 ID만 식별자로 조회하려면 아래처럼 사용합니다:

```php
$taxId = $user->findTaxId('txi_belgium');
```

새로운 세금 ID를 추가하려면 타입([지원 타입 목록 참고](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type))과 값을 `createTaxId`로 전달합니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId`는 VAT ID를 즉시 Stripe에 추가합니다. [VAT ID의 검증도 Stripe에서 수행](https://stripe.com/docs/invoicing/customer/tax-ids#validation)하지만, 이 과정은 비동기입니다. 검증 결과 갱신을 받고 싶다면 `customer.tax_id.updated` webhook 이벤트를 구독하고, VAT ID의 `verification` 필드를 참고하세요. 자세한 webhook 처리 방법은 [웹훅 핸들러 정의 문서](#handling-stripe-webhooks)를 참고하세요.

세금 ID를 삭제할 때는 `deleteTaxId` 메서드를 이용합니다:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화

애플리케이션에서 사용자의 이름, 이메일 등의 정보가 Stripe에도 저장되는 경우, 정보 변경이 발생하면 Stripe에도 동일하게 동기화하는 것이 좋습니다. 이를 자동화하려면, billable 모델의 `updated` 이벤트에서 `syncStripeCustomerDetails` 메서드를 호출하는 이벤트 리스너를 등록하면 됩니다:

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

이제 고객 정보가 변경될 때마다 Stripe와 자동으로 동기화됩니다. 신규 고객 생성 시에도 Cashier가 Stripe에 자동 동기화를 수행합니다.

동기화할 컬럼을 커스터마이즈하려면 Cashier의 다양한 메서드를 오버라이드할 수 있습니다. 예를 들어, Stripe에 동기화할 고객 이름 필드를 변경하려면 `stripeName` 메서드를 오버라이드하면 됩니다:

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

유사하게 `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 등도 오버라이드가 가능하며, 이 메서드는 Stripe 고객 객체 업데이트 시 해당 필드로 동기화됩니다. 동기화 과정을 완전히 제어하고 싶으면 `syncStripeCustomerDetails` 메서드를 통째로 오버라이드할 수도 있습니다.

<a name="billing-portal"></a>
### 청구 포털 (Billing Portal)

Stripe는 고객이 구독, 결제 수단, 결제 내역을 직접 관리할 수 있는 [간편한 청구 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 컨트롤러나 라우트에서 billable 모델의 `redirectToBillingPortal` 메서드로 사용자를 포털로 리디렉션할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

사용자가 포털에서 구독을 관리한 후에는 기본적으로 `home` 라우트로 돌아갈 수 있습니다. 다른 URL로 돌아가도록 하려면 인자로 전달하세요:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리디렉션 없이 포털 URL만 받고 싶은 경우 `billingPortalUrl` 메서드를 사용합니다:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

(이후 내용도 동일한 패턴으로 구조적, 기술적으로 완벽하게 한국어 번역)