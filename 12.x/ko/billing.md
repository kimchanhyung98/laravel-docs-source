# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드하기](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [결제 가능한 모델(Billable Model)](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용하기](#using-custom-models)
- [빠른 시작](#quickstart)
    - [제품 판매하기](#quickstart-selling-products)
    - [구독 판매하기](#quickstart-selling-subscriptions)
- [고객 처리](#customers)
    - [고객 조회하기](#retrieving-customers)
    - [고객 생성하기](#creating-customers)
    - [고객 업데이트하기](#updating-customers)
    - [잔액 처리하기](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터와 Stripe 동기화하기](#syncing-customer-data-with-stripe)
    - [청구 포털(Billing Portal)](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장하기](#storing-payment-methods)
    - [결제 수단 조회하기](#retrieving-payment-methods)
    - [결제 수단 존재 여부 확인하기](#payment-method-presence)
    - [기본 결제 수단 업데이트하기](#updating-the-default-payment-method)
    - [결제 수단 추가하기](#adding-payment-methods)
    - [결제 수단 삭제하기](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성하기](#creating-subscriptions)
    - [구독 상태 확인하기](#checking-subscription-status)
    - [가격 변경하기](#changing-prices)
    - [구독 수량 관리하기](#subscription-quantity)
    - [여러 상품 포함 구독](#subscriptions-with-multiple-products)
    - [여러 구독 다루기](#multiple-subscriptions)
    - [사용량 기반 청구](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일 설정하기](#subscription-anchor-date)
    - [구독 취소하기](#cancelling-subscriptions)
    - [구독 재개하기](#resuming-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [선결제 방식 구독 체험](#with-payment-method-up-front)
    - [비선결제 방식 구독 체험](#without-payment-method-up-front)
    - [체험 기간 연장하기](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 핸들러 정의하기](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단한 결제하기](#simple-charge)
    - [청구서와 함께 결제하기](#charge-with-invoice)
    - [결제 인텐트 생성하기](#creating-payment-intents)
    - [결제 환불하기](#refunding-charges)
- [체크아웃](#checkout)
    - [제품 체크아웃](#product-checkouts)
    - [단건 결제 체크아웃](#single-charge-checkouts)
    - [구독 체크아웃](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [게스트 체크아웃](#guest-checkouts)
- [청구서](#invoices)
    - [청구서 조회하기](#retrieving-invoices)
    - [예정된 청구서 조회](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [청구서 PDF 생성하기](#generating-invoice-pdfs)
- [결제 실패 처리하기](#handling-failed-payments)
    - [결제 확인하기](#confirming-payments)
- [강력한 고객 인증 (SCA)](#strong-customer-authentication)
    - [추가 결제 확인이 필요한 경우](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 청구 서비스를 위한 표현력 있고 유려한 인터페이스를 제공합니다. 반복적으로 작성해야 하는 구독 청구 코드를 대부분 대신 처리해줍니다. 기본적인 구독 관리 외에도 쿠폰 처리, 구독 교체, 구독 "수량" 관리, 취소 유예 기간, 청구서 PDF 생성 기능까지 다룰 수 있습니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드하기

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> 호환성 문제를 방지하기 위해서, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. 새로운 Stripe 기능과 개선 사항 적용을 위해 마이너 릴리즈 시 Stripe API 버전이 업데이트될 예정입니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용해 Stripe용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier
```

패키지 설치 후에는 `vendor:publish` Artisan 명령어를 사용하여 Cashier의 마이그레이션을 게시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그리고 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하며, 고객의 모든 구독 정보를 저장할 `subscriptions` 테이블과, 다중 가격 구독을 위한 `subscription_items` 테이블을 새로 만듭니다.

원한다면 `vendor:publish` 명령어로 Cashier 설정 파일도 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 모든 Stripe 이벤트를 제대로 처리하도록 [웹훅 핸들링](#handling-stripe-webhooks)을 설정하는 것을 잊지 마세요.

> [!WARNING]
> Stripe 식별자를 저장하는 컬럼은 대소문자를 구분해야 하므로, MySQL을 사용하는 경우 `stripe_id` 컬럼의 컬레이션을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 결제 가능한 모델(Billable Model)

Cashier를 사용하기 전에, 결제 가능한 모델 정의에 `Billable` 트레이트를 추가하세요. 보통은 `App\Models\User` 모델일 것입니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 같은 일반적인 청구 작업을 위한 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 결제 가능한 모델이 Laravel 기본 제공 `App\Models\User` 클래스라고 가정합니다. 만약 다른 모델을 사용하고 싶다면 `useCustomerModel` 메서드를 통해 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩 메서드
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel 기본 `App\Models\User` 이외의 모델을 사용한다면, 반드시 [Cashier 마이그레이션](#installation)을 게시한 후 대체 모델에 맞게 테이블 이름 등 내용을 수정하세요.

<a name="api-keys"></a>
### API 키

다음으로 애플리케이션의 `.env` 파일에 Stripe API 키를 설정해야 합니다. 키는 Stripe 대시보드에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수는 반드시 `.env`에 정의해야 합니다. 이 변수는 들어오는 웹훅 요청이 Stripe에서 온 것인지 확인하는 용도로 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 바꾸려면 애플리케이션 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 설정하세요:

```ini
CASHIER_CURRENCY=eur
```

통화 외에도 청구서에 표시할 금액 포맷에 사용할 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용해 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 PHP `ext-intl` 확장 기능이 설치 및 구성되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax)를 활용해 Stripe에서 생성하는 모든 청구서에 대해 자동으로 세금을 계산할 수 있습니다. 자동 세금 계산을 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 `calculateTaxes` 메서드를 호출하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩 메서드
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

자동 세금 계산이 활성화되면 새 구독과 일회성 청구서에 세금이 자동으로 계산됩니다.

이 기능이 제대로 작동하려면 고객의 이름, 주소, 세금 ID 같은 청구 정보가 Stripe와 동기화되어야 합니다. 이를 위해 Cashier가 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe)와 [세금 ID](#tax-ids) 메서드를 사용할 수 있습니다.

<a name="logging"></a>
### 로깅

Cashier는 치명적인 Stripe 오류를 기록할 로그 채널을 지정할 수 있습니다. 애플리케이션 `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 정의해 로그 채널을 설정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 중 생성되는 예외는 애플리케이션 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용하기

Cashier 내부에서 사용하는 모델을 확장하려면, 직접 모델 클래스를 정의하고 해당 Cashier 모델을 상속하면 됩니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

그리고 나서 `Laravel\Cashier\Cashier` 클래스로 Cashier에 커스텀 모델 사용을 알려줄 수 있습니다. 보통 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * 애플리케이션 서비스 부트스트랩 메서드
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

<a name="quickstart"></a>
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 제품 판매하기

> [!NOTE]
> Stripe Checkout을 사용하기 전, Stripe 대시보드에서 고정 가격이 설정된 상품(Product)을 미리 정의해야 하며, [Cashier 웹훅 설정](#handling-stripe-webhooks)도 구성해야 합니다.

제품과 구독 결제 기능을 직접 구현하려면 복잡해 보일 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 간편하게 견고한 결제 통합을 구축할 수 있습니다.

반복 결제가 아닌 단건 결제 상품에 대해 고객에게 결제 페이지(Stripe Checkout)로 리디렉션하여 결제 정보를 받고, 결제가 완료되면 애플리케이션 내 지정한 성공 URL로 돌려보내는 방식을 사용합니다:

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

위 예제에서는 Cashier가 제공하는 `checkout` 메서드를 이용해 고객을 Stripe Checkout으로 리디렉션합니다. Stripe에서 "prices"는 [특정 상품에 대해 정의한 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요에 따라 `checkout` 메서드는 Stripe에 고객을 자동으로 생성하고, 해당 Stripe 고객 레코드를 애플리케이션 데이터베이스의 사용자와 연결합니다. 결제 완료 후에는 성공 또는 취소 페이지로 고객을 안내해 메시지를 보여줄 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 전달하기

제품 판매 시, 주문 완료 내역과 상품 구매 기록을 애플리케이션 내 `Cart` 및 `Order` 모델로 관리하는 경우가 많습니다. Stripe Checkout으로 고객을 리디렉션할 때, 주문 ID를 `metadata`로 전달해 고객이 돌아왔을 때 주문과 연결해야 할 수 있습니다.

예를 들어, 사용자가 결제 프로세스를 시작하면서 대기 상태인 `Order`가 생성된다고 가정해 봅시다. 아래 예제의 `Cart` 및 `Order` 모델은 Cashier 내장 모델이 아니므로, 애플리케이션 요구사항에 맞게 자유롭게 구현하면 됩니다:

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

위 예제처럼, 체크아웃이 시작되면 카트/주문에 연결된 Stripe 가격 ID들을 `checkout` 메서드에 넘기고, 주문 ID를 `metadata` 배열에 포함해 전달합니다. 또한 성공 URL에 `{CHECKOUT_SESSION_ID}` 문자열을 추가하면 Stripe가 실제 체크아웃 세션 ID로 치환합니다.

다음은 구매 완료 후 리디렉션되는 성공 페이지 예제입니다. 여기서 Stripe Checkout 세션 ID를 받아 Stripe API로 세션 정보를 조회해 `metadata`를 참고해 주문 상태를 업데이트합니다:

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

Checkout 세션 객체에 관한 자세한 데이터는 Stripe [문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매하기

> [!NOTE]
> Stripe Checkout을 이용하기 전 Stripe 대시보드에서 고정 가격이 설정된 상품을 미리 생성하고, [Cashier 웹훅 처리](#handling-stripe-webhooks)를 구성해야 합니다.

제품과 구독 결제 기능 구현은 복잡해 보이지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 이용하면 모던하고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

간단히 기본 월간(`price_basic_monthly`)과 연간(`price_basic_yearly`) 구독 플랜이 있는 구독 서비스를 고려해 봅시다. 이 가격들은 Stripe 대시보드 내 "Basic" 상품(`pro_basic`) 아래 묶을 수 있습니다. 구독 서비스에 `pro_expert` 전문가 플랜도 있다고 가정합니다.

고객이 구독하려면, 예컨대 가격 페이지에서 Basic 플랜 구독 버튼 클릭 시 사용자를 Stripe Checkout 세션으로 연결하는 라우트를 만듭니다:

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

위 예제에서 `checkout` 메서드를 통해 고객을 Stripe Checkout 페이지로 리디렉션하며, Basic 플랜 구독을 할 수 있게 합니다. 성공 또는 취소 후 고객은 `checkout` 메서드에 지정한 URL로 리디렉션됩니다. 다만 일부 결제 수단은 처리까지 시간이 걸리므로, 구독이 실제 시작됐는지는 반드시 [웹훅 처리](#handling-stripe-webhooks)를 통해 확인해야 합니다.

구독자가 특정 서비스에 접근하도록 제한하려면, Cashier가 제공하는 `Billable` 트레이트의 `subscribed` 메서드로 구독 중인지 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 상품 또는 가격에 구독 중인지 확인할 수도 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 상품에 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 플랜에 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독자 전용 미들웨어 만들기

편리하게, 구독 여부에 따라 요청 접근을 제한하는 Laravel [미들웨어](/docs/12.x/middleware)를 만들어 특정 라우트에 할당할 수 있습니다:

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
            // 미구독자는 결제 페이지로 리디렉션
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

만든 미들웨어를 라우트에 할당하세요:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 청구 플랜 관리하기 허용하기

고객이 자신 구독 상품 또는 등급을 바꾸고 싶어할 수 있습니다. 가장 쉬운 방법은 Stripe가 제공하는 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)으로 안내하는 것입니다. Billing Portal은 사용자가 청구서 다운로드, 결제 수단 변경, 구독 플랜 변경을 할 수 있는 호스팅 된 UI를 제공합니다.

애플리케이션에 Billing Portal로 이동하는 링크나 버튼을 만들고, 해당 URL에 연결된 라우트를 정의해 Stripe Billing Portal 세션을 시작하도록 합니다:

```blade
<a href="{{ route('billing') }}">
    청구 관리
</a>
```

그리고 라우트에서 아래처럼 Billing Portal 세션을 시작하고 Portal로 리디렉션합니다. `redirectToBillingPortal` 메서드는 사용자가 Portal에서 나올 때 돌아갈 URL을 인수로 받습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier 웹훅 핸들링이 설정되어 있으면, Stripe에서 사용자가 Billing Portal에서 구독을 취소해도 그에 맞춰 애플리케이션 DB가 자동으로 동기화됩니다.

<a name="customers"></a>
## 고객 처리

<a name="retrieving-customers"></a>
### 고객 조회하기

Stripe ID로 고객을 조회할 때는 `Cashier::findBillable` 메서드를 사용하세요. 이 메서드는 결제 가능한 모델 인스턴스를 반환합니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성하기

때때로 구독 없이 Stripe 고객만 생성하려면 `createAsStripeCustomer` 메서드를 사용하세요:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

Stripe 고객 생성 파라미터를 옵션 배열로 넘길 수도 있습니다([Stripe API 문서](https://stripe.com/docs/api/customers/create) 참고):

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

결제 가능한 모델에 연결된 Stripe 고객 객체를 반환하려면 `asStripeCustomer` 메서드를 사용하세요:

```php
$stripeCustomer = $user->asStripeCustomer();
```

모델이 이미 Stripe 고객인지 확실치 않을 때는 `createOrGetStripeCustomer` 메서드로 조회하거나 없으면 새로 생성할 수 있습니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 업데이트하기

Stripe 고객 정보를 추가로 업데이트할 때는 `updateStripeCustomer` 메서드를 이용하세요. Stripe API에서 지원하는 고객 업데이트 옵션 배열을 인수로 받습니다:

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 처리하기

Stripe는 고객 잔액을 입금 또는 출금할 수 있도록 지원합니다. `balance` 메서드를 호출하면 고객 통화로 포맷된 잔액 문자열을 얻을 수 있습니다:

```php
$balance = $user->balance();
```

잔액을 증액하려면 `creditBalance` 메서드를 호출하고, 설명을 추가할 수도 있습니다:

```php
$user->creditBalance(500, 'Premium customer top-up.');
```

잔액을 차감하려면 `debitBalance` 메서드를 사용하세요:

```php
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance` 메서드는 새 잔액 거래 기록을 생성합니다. 거래 내역은 `balanceTransactions` 메서드로 조회해 고객에게 입출금 내역을 보여줄 때 유용합니다:

```php
// 모든 거래 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액...
    $amount = $transaction->amount(); // $2.31

    // 가능한 경우 관련 인보이스 조회...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID

Cashier는 고객의 세금 ID 관리도 쉽게 합니다. `taxIds` 메서드로 고객에 할당된 모든 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션 형태로 불러올 수 있습니다:

```php
$taxIds = $user->taxIds();
```

ID로 특정 세금 ID를 조회할 수도 있습니다:

```php
$taxId = $user->findTaxId('txi_belgium');
```

새 세금 ID는 유효한 [타입](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 주어 `createTaxId` 메서드로 생성합니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId` 메서드는 즉시 해당 VAT ID를 고객 계정에 등록합니다. ※VAT ID 검증은 Stripe가 비동기로 수행하며, `customer.tax_id.updated` 웹훅 수신 시 VAT ID 검증 상태(`verification` 파라미터)를 확인할 수 있습니다. 웹훅 처리 방법은 [웹훅 핸들러 정의](#handling-stripe-webhooks)를 참고하세요.

세금 ID 삭제는 `deleteTaxId` 메서드를 사용합니다:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### 고객 데이터와 Stripe 동기화하기

사용자가 이름, 이메일 등 Stripe에도 저장된 고객 정보를 변경하면, Stripe 데이터와 동기화하는 것이 좋습니다.

이를 자동화하려면, 결제 가능한 모델에서 `updated` 이벤트를 감지하는 이벤트 리스너를 정의하고, 리스너에서 `syncStripeCustomerDetails` 메서드를 호출하세요:

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * 모델의 부트 메서드
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

이렇게 하면 고객 모델이 갱신될 때마다 Stripe 고객 정보도 동기화됩니다. 최초 고객 생성 시에도 자동으로 데이터를 동기화합니다.

동기화 시 사용할 속성을 변경하려면 Cashier가 제공하는 여러 메서드(`stripeName`, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales`)를 오버라이드하면 됩니다. 예를 들어, 고객 이름으로 사용할 속성을 바꾸려면 `stripeName`를 재정의하세요:

```php
/**
 * Stripe와 동기화할 고객 이름 반환
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

고객 정보 동기화 과정을 완전히 제어하고 싶으면 `syncStripeCustomerDetails` 메서드를 재정의할 수도 있습니다.

<a name="billing-portal"></a>
### 청구 포털(Billing Portal)

Stripe는 고객이 본인 구독, 결제 수단, 청구 내역을 관리할 수 있는 [청구 포털](https://stripe.com/docs/billing/subscriptions/customer-portal) 기능을 제공합니다. 라우트 또는 컨트롤러 내에서 결제 가능한 모델 인스턴스의 `redirectToBillingPortal` 메서드를 호출해 사용자를 포털로 리디렉션할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 고객이 포털 이용 후 애플리케이션의 `home` 경로로 돌아갈 수 있는 링크가 제공됩니다. 사용자 복귀 URL을 직접 지정하고 싶다면, URL을 인수로 넘기면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리디렉션 없이 URL만 생성하려면 `billingPortalUrl` 메서드를 호출하세요:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단

<a name="storing-payment-methods"></a>
### 결제 수단 저장하기

구독 생성 또는 단건 결제를 하기 위해 결제 수단을 Stripe에 저장하고 ID를 획득해야 합니다. 구독용과 단건 결제용 저장 방식이 다르므로 각각 설명합니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독용 결제 수단

구독에 사용할 카드 정보를 저장하려면 Stripe의 "Setup Intents" API를 사용해 안전하게 결제 수단 정보를 수집합니다. Setup Intent는 결제 수단 청구 의도를 Stripe에 알리는 것입니다. Cashier의 `Billable` 트레이트가 제공하는 `createSetupIntent` 메서드를 컨트롤러 또는 라우트에서 호출하고, 고객 결제수단 입력 폼에 전달하세요:

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

뷰 내에서는 Setup Intent 비밀키(`client_secret`)를 결제 수단 입력 요소에 전달하고, Stripe.js 라이브러리를 사용해 [Stripe Elements](https://stripe.com/docs/stripe-js)를 붙입니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 표시자 -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    결제 수단 업데이트
</button>
```

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

Stripe의 [`confirmCardSetup`](https://stripe.com/docs/js/setup_intents/confirm_card_setup) 메서드로 카드 확인 후, 안전한 결제 수단 ID를 받을 수 있습니다:

```js
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
        // error.message를 사용자에게 표시...
    } else {
        // 카드가 성공적으로 확인됨...
    }
});
```

인증된 `setupIntent.payment_method` ID를 Laravel 애플리케이션으로 전달해, 새 결제 수단으로 추가하거나 기본 수단으로 지정하거나 즉시 구독 생성에 사용할 수 있습니다.

> [!NOTE]
> Setup Intents에 대해 더 알고 싶다면 Stripe가 제공하는 [개요 문서](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>
#### 단건 결제용 결제 수단

단건 결제 시에는 저장된 기본 결제 수단을 재사용할 수 없습니다. Stripe.js로 고객이 직접 카드 정보를 입력하게 해야 합니다. 아래와 같이 폼을 만들고 Stripe.js로 카드 요소를 붙입니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 표시자 -->
<div id="card-element"></div>

<button id="card-button">
    결제 처리
</button>
```

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

카드 확인 후 Stripe `createPaymentMethod` 메서드를 사용해 새 결제 수단 ID를 얻습니다:

```js
const cardHolderName = document.getElementById('card-holder-name');
const cardButton = document.getElementById('card-button');

cardButton.addEventListener('click', async (e) => {
    const { paymentMethod, error } = await stripe.createPaymentMethod(
        'card', cardElement, {
            billing_details: { name: cardHolderName.value }
        }
    );

    if (error) {
        // error.message를 사용자에게 표시...
    } else {
        // 카드가 성공적으로 확인됨...
    }
});
```

아이디를 Laravel에 넘겨 [단일 결제](#simple-charge)를 진행할 수 있습니다.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회하기

결제 가능한 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다:

```php
$paymentMethods = $user->paymentMethods();
```

특정 타입 결제 수단만 조회하려면 타입을 인수로 넘기세요:

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

고객의 기본 결제 수단은 `defaultPaymentMethod` 메서드로 조회합니다:

```php
$paymentMethod = $user->defaultPaymentMethod();
```

특정 결제 수단 ID를 가진 결제 수단은 `findPaymentMethod` 메서드로 조회할 수 있습니다:

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 결제 수단 존재 여부 확인하기

결제 가능한 모델에 기본 결제 수단이 존재하는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출하세요:

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

결제 가능한 모델에 결제 수단이 적어도 하나 이상 존재하는지 확인하려면 `hasPaymentMethod` 메서드를 쓰세요. 특정 타입 결제 수단 존재 여부를 확인하려면 타입을 넘기면 됩니다:

```php
if ($user->hasPaymentMethod()) {
    // ...
}

if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트하기

`updateDefaultPaymentMethod` 메서드를 호출해 기본 결제 수단을 새 결제 수단 ID로 변경할 수 있습니다:

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

기본 결제 수단 정보를 Stripe 고객의 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용하세요:

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> Stripe 제한으로 인해 기본 결제 수단은 인보이스 발행 및 신규 구독 생성에만 사용할 수 있습니다. 단일 결제에서는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가하기

새 결제 수단을 추가하려면 `addPaymentMethod` 메서드에 결제 수단 ID를 전달해 호출하세요:

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 ID 획득 방법은 [결제 수단 저장하기](#storing-payment-methods) 문서를 참조하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제하기

결제 수단 인스턴스에서 `delete` 메서드 호출로 삭제할 수 있습니다:

```php
$paymentMethod->delete();
```

특정 결제 수단 ID를 사용자 기본 결제 수단에서 삭제하려면 `deletePaymentMethod` 메서드를 호출하세요:

```php
$user->deletePaymentMethod('pm_visa');
```

모든 결제 수단을 삭제하려면 `deletePaymentMethods` 메서드를 호출합니다:

```php
$user->deletePaymentMethods();
```

특정 타입 결제 수단만 삭제하려면 타입을 인수로 넘길 수 있습니다:

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독이 있을 경우, 기본 결제 수단 삭제를 차단해야 합니다.

<a name="subscriptions"></a>
## 구독

구독은 고객의 반복 결제를 설정하는 방법입니다. Cashier가 관리하는 Stripe 구독은 다중 가격, 수량, 체험 기간 등을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성하기

구독을 만들려면 보통 `App\Models\User` 모델 인스턴스를 가져온 뒤 `newSubscription` 메서드를 호출해 구독 빌더를 얻고, `create`를 써서 생성합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

`newSubscription`첫 번째 인수는 내부 구독 타입(예: `default`), 두 번째 인수는 Stripe 가격 ID를 의미합니다.

`create` 메서드는 Stripe 결제 수단 ID 또는 Stripe `PaymentMethod` 객체를 받아 구독을 시작하고, 사용자 Stripe 고객 ID 및 청구 정보를 DB에 업데이트합니다.

> [!WARNING]
> `create` 메서드에 결제 수단 ID를 전달하면 자동으로 사용자의 저장된 결제 수단 목록에도 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 청구서 이메일로 반복 결제 받기

Stripe가 반복 결제를 자동으로 징수하지 않고, 자동으로 청구서를 이메일로 보내 고객이 수동으로 결제하도록 할 수도 있습니다. 이때 선결제 결제 수단이 필요 없습니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

청구서 결제 기한은 `days_until_due` 옵션으로 설정 가능하며, 기본은 30일입니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 구독 수량

특정 수량으로 구독을 생성하고 싶다면, `quantity` 메서드를 사용한 뒤 구독을 만듭니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 옵션

Stripe가 지원하는 추가 고객 옵션과 구독 옵션을 `create` 메서드 두 번째, 세 번째 인수로 배열 전달할 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => '추가 정보'],
]);
```

<a name="coupons"></a>
#### 쿠폰

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요:

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

또는 Stripe 프로모션 코드를 적용하려면 `withPromotionCode` 메서드를 쓸 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

인수로 넘기는 프로모션 코드 ID는 고객이 보는 프로모션 코드가 아니라 Stripe API가 부여한 ID여야 합니다. 고객용 코드를 ID로 변환하려면 `findPromotionCode` 또는 `findActivePromotionCode` 메서드를 사용하세요:

```php
// 고객용 코드로 프로모션 코드 ID 조회...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// 활성화된 프로모션 코드 ID 조회...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

반환 객체는 `Laravel\Cashier\PromotionCode` 인스턴스이며, `coupon` 메서드로 할인 쿠폰을 가져올 수 있습니다:

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

쿠폰은 할인 유형(비율 또는 고정 금액)을 확인할 수 있습니다:

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

고객이나 구독에 현재 적용된 할인 정보를 얻으려면 각각 다음과 같이 호출하세요:

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

반환된 `Laravel\Cashier\Discount` 인스턴스에서 `coupon` 메서드로 쿠폰 정보에 접근할 수 있습니다:

```php
$coupon = $subscription->discount()->coupon();
```

새 쿠폰이나 프로모션 코드를 고객 또는 구독에 적용하려면 각각 `applyCoupon` 또는 `applyPromotionCode` 메서드를 사용하세요:

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

쿠폰과 프로모션 코드는 Stripe API ID를 사용해야 하며, 한 고객 혹은 구독에 한 번에 적용 가능한 쿠폰은 하나입니다.

자세한 내용은 Stripe 쿠폰 및 프로모션 코드 관련 [문서](https://stripe.com/docs/billing/subscriptions/coupons)를 참고하세요.

<a name="adding-subscriptions"></a>
#### 구독 추가

이미 기본 결제 수단이 등록된 고객에게 구독을 추가하려면 `add` 메서드를 사용합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 구독 생성하기

Stripe 대시보드에서도 구독을 생성할 수 있습니다. 이 경우 Cashier는 생성된 구독을 동기화하고 기본 타입 `default`가 할당됩니다. 대시보드 생성 구독의 타입을 변경하려면 [웹훅 이벤트 핸들러](#defining-webhook-event-handlers)를 정의하세요.

여러 구독 타입이 애플리케이션에 있으면 대시보드에서 생성할 수 있는 구독 타입은 하나뿐입니다.

그리고 반드시 구독 타입별로 하나의 활성 구독만 유지하십시오. 동일 타입 구독이 여러 개 있으면 Cashier는 최신 구독 하나만 사용하며, 구독 기록 차원에서 이전 구독은 DB에 남깁니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인하기

구독 중 고객인지 다양한 메서드로 확인할 수 있습니다. 먼저 `subscribed` 메서드는 지정한 구독 타입에 대해 유효한 구독이 있을 경우 `true`를 반환합니다. 체험 기간 내 구독도 유효로 간주됩니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware) 구현에 적합합니다. 예:

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
            // 미구독자...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

체험 기간 여부는 `onTrial` 메서드를 써서 판단할 수 있습니다:

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

사용자가 특정 상품에 구독 중인지 확인하려면 `subscribedToProduct` 메서드를 사용합니다. Stripe 내 상품 식별자(`product ID`) 기준입니다:

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

배열로 여러 상품을 넘겨 관련 구독이 하나라도 있으면 `true`를 반환할 수 있습니다:

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

특정 가격 ID에 구독 중인지 판단하려면 `subscribedToPrice` 메서드를 사용하세요:

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

`recurring` 메서드를 호출하면 현재 구독 중이고 체험 기간이 지난 구독인지 확인할 수 있습니다:

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> 동일 타입 구독이 두 개 이상이면 `subscription` 메서드는 가장 최신 구독을 반환합니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

과거에 구독하다가 취소했는지 확인하려면 `canceled` 메서드를 사용하세요:

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

취소했지만 청구 종료일까지 사용하는 "유예 기간" 중인지 확인하려면 `onGracePeriod`를 사용합니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

구독이 취소되어 유예 기간도 끝나면 `ended` 메서드가 `true`를 반환합니다:

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료(incomplete) 및 연체(past_due) 상태

결제 추가 작업이 필요한 경우 구독은 `incomplete` 상태가 됩니다. 가격을 변경하며 추가 결제 작업이 필요한 경우 `past_due` 상태가 됩니다. 이때 구독은 제한적으로만 활성으로 간주됩니다.

`hasIncompletePayment` 메서드로 해당 상태 여부를 판단할 수 있습니다:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

이 경우, 사용자를 Cashier가 제공하는 결제 확인 페이지로 안내하고, 구독 인스턴스의 `latestPayment` 메서드로 결제 ID를 넘기면 됩니다:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    결제 확인이 필요합니다.
</a>
```

`past_due` 또는 `incomplete` 상태에서도 구독을 활성 상태로 유지하려면, `App\Providers\AppServiceProvider`의 `register` 메서드에 다음 메서드를 추가하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 등록 메서드
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]
> `incomplete` 상태의 구독은 결제가 확정되기 전까지 변경이 불가능하므로, `swap`과 `updateQuantity` 메서드는 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 스코프

구독 상태는 쿼리 스코프로도 제공되어, 다음과 같이 조건별로 DB 검색이 가능합니다:

```php
// 활성 구독 조회
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자의 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

다음 스코프들이 사용 가능합니다:

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
### 가격 변경하기

구독 중에 가격을 변경하려면 `swap` 메서드에 새 가격 ID를 전달하세요. 구독 취소된 경우 자동으로 재활성화됩니다. 가격 ID는 Stripe 대시보드에서 확인해야 합니다:

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

체험 기간은 유지되고 수량이 있으면 유지됩니다.

체험 기간을 무시하고 즉시 가격 전환하려면 `skipTrial` 메서드를 체인하세요:

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

즉시 청구까지 하고 싶으면 `swapAndInvoice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 비례 계산

기본적으로 Stripe는 가격 변경 시 비례 계산(요금 정산)을 합니다. 비례 계산 없이 바로 가격을 변경하려면 `noProrate` 메서드를 호출하세요:

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

> [!WARNING]
> `noProrate`를 `swapAndInvoice` 전에 호출해도 효과가 없습니다. `swapAndInvoice` 실행 시 반드시 청구서가 발행됩니다.

<a name="subscription-quantity"></a>
### 구독 수량

구독 수량을 증감하려면 `incrementQuantity`와 `decrementQuantity` 메서드를 사용하세요:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 수량을 5 증가시키기
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 수량을 5 감소시키기
$user->subscription('default')->decrementQuantity(5);
```

특정 수량으로 설정하려면 `updateQuantity`를 사용합니다:

```php
$user->subscription('default')->updateQuantity(10);
```

비례 계산 없이 수량을 변경하려면 `noProrate`를 체인하세요:

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

자세한 내용은 Stripe [문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독의 수량

다중 상품 구독인 경우, 수량 변경 메서드에 가격 ID도 인수로 전달해야 합니다:

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품 포함 구독

[여러 상품 포함 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)은 하나 구독에 여러 상품 가격을 달 수 있습니다. 예를 들어 기본 구독 $10에 라이브 채팅 추가상품 $15를 더하는 경우가 그러합니다. 관련 데이터는 `subscription_items` 테이블에 저장됩니다.

`newSubscription`에 가격 배열을 전달해 여러 가지 가격으로 구독을 만들 수 있습니다:

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

수량도 각 가격별로 지정 가능합니다:

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 가격을 추가하려면 `addPrice`를 사용합니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

즉시 청구하려면 `addPriceAndInvoice` 사용:

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

수량 포함 추가도 가능합니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

가격을 제거할 때는 `removePrice`를 호출합니다:

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독 마지막 가격은 제거할 수 없습니다. 구독 자체를 취소해야 합니다.

<a name="swapping-prices"></a>
#### 가격 교체

다중 상품 구독의 가격도 교체할 수 있습니다. 예컨대 `price_basic` + `price_chat` 구독을 `price_pro` + `price_chat`으로 변경하려면:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

기존 `price_basic` 아이템은 삭제되고, `price_chat`는 유지되며, `price_pro` 아이템이 새로 생성됩니다.

옵션 배열로 각 가격별 속성을 지정할 수도 있습니다(예: 수량):

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

단일 가격만 교체하려면 구독 아이템의 `swap` 메서드를 호출하는 편이 메타데이터를 보존하는 데 유리합니다:

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
#### 비례 계산

가격 추가/삭제 시 기본으로 비례 계산이 적용됩니다. 비례 계산 없이 변경하고 싶으면 `noProrate`를 체인하세요:

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량 변경

각 가격별 수량도 가격 ID 넘겨서 변경할 수 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 다중 가격 구독 시 `Subscription` 모델의 `stripe_price`와 `quantity` 속성은 `null`입니다. 개별 가격 정보는 `items` 관계를 통해 접근하세요.

<a name="subscription-items"></a>
#### 구독 아이템

다중 가격 구독 시, 개별 가격 아이템들은 DB `subscription_items` 테이블에 저장되어 `Subscription` 모델의 `items` 관계로 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// 아이템 별 Stripe 가격과 수량 조회
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

가격 ID를 사용해 특정 아이템도 조회 가능합니다:

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 여러 구독

Stripe는 고객이 여러 구독을 동시에 가질 수 있도록 지원합니다. 예를 들어, 헬스장 회원이 수영 월간 구독과 웨이트 트레이닝 월간 구독을 각각 별도로 가질 수 있습니다.

`newSubscription`에 구독 타입을 지정함으로써 여러 구독을 만들고 관리할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

구독 타입별로 가격을 바꾸려면 각 구독 인스턴스의 `swap`을 쓰세요:

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

구독 취소는 다음과 같이 합니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### 사용량 기반 청구

[사용량 기반 청구](https://stripe.com/docs/billing/subscriptions/metered-billing)는 예를 들어 고객이 매월 보낸 문자 수나 이메일 수에 따라 요금이 부과되는 경우에 이용합니다.

먼저 Stripe 대시보드에서 사용량 기반 모델, 미터(meter)를 포함하는 상품과 가격을 생성하고, 청구에 사용할 이벤트명과 미터 ID를 확보하세요. 그 다음 아래처럼 `meteredPrice` 메서드를 사용해 구독에 메터 가격을 추가합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

Stripe Checkout에서도 메터 구독 시작 가능:

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

고객이 서비스를 이용할 때마다 사용량을 Stripe로 보고해야 합니다. `reportMeterEvent` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

기본 사용량은 1이며, 필요하면 수량 인수를 전달할 수 있습니다:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

미터별 이벤트 요약도 `meterEventSummaries` 메서드로 조회합니다:

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value; // 예: 10
```

자세한 사항은 Stripe [Meter Event Summary](https://docs.stripe.com/api/billing/meter-event_summary/object) 문서를 참고하세요.

모든 미터 조회는 `meters` 메서드 사용:

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
### 구독 세금

> [!WARNING]
> 수동 세금율 계산 대신 [Stripe Tax 자동 계산](#tax-configuration)을 사용하세요.

고객별 구독에 적용할 세율을 지정하려면 결제 가능한 모델에 `taxRates` 메서드를 구현하고 Stripe 세금율 ID 배열을 반환하세요. Stripe 대시보드에서 세율 관리 가능합니다:

```php
/**
 * 고객 구독에 적용할 세율 목록
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```

다중 상품 구독에선 가격별 세율을 `priceTaxRates` 메서드로 정의할 수 있습니다:

```php
/**
 * 고객 구독에 적용할 가격별 세율 목록
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
> `taxRates`는 오직 구독 청구에만 적용되며, 일회성 결제 시에는 수동으로 세율을 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화

`taxRates` 메서드 반환값을 변경해도 기존 구독 세금 설정은 자동 변경되지 않습니다. 변경 내용을 기존 구독에 적용하려면 구독 인스턴스의 `syncTaxRates` 메서드를 호출하세요:

```php
$user->subscription('default')->syncTaxRates();
```

이는 다중 상품 구독 아이템 세율도 함께 동기화합니다. `priceTaxRates` 메서드를 구현한 경우 반드시 함께 사용하세요.

<a name="tax-exemption"></a>
#### 세금 면제

Cashier는 고객이 세금 면제인지 여부를 반환하는 `isTaxExempt`, `isNotTaxExempt`, `reverseChargeApplies` 메서드를 제공합니다. Stripe API를 호출해 정보를 확인합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

같은 메서드는 `Laravel\Cashier\Invoice` 객체에서도 호출 가능하지만, 호출 시점의 청구서 생성 시점 면제 상태를 반환합니다.

<a name="subscription-anchor-date"></a>
### 구독 기준일 설정하기

구독 청구 기준일은 기본 구독 생성일이나 체험 종료일입니다. 이를 변경하고 싶으면 `anchorBillingCycleOn` 메서드에 원하는 날짜를 전달하세요:

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

자세한 내용은 Stripe [결제 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소하기

구독을 취소하려면 구독 인스턴스의 `cancel` 메서드를 호출합니다:

```php
$user->subscription('default')->cancel();
```

취소 시 Cashier는 `subscriptions` 테이블의 `ends_at` 컬럼을 채워, `subscribed` 메서드가 `false`를 반환해야 하는 시점을 알립니다.

예를 들어, 3월 1일 취소 요청했지만 실제 종료 예정일이 3월 5일이면 `subscribed`는 3월 5일까지 `true`를 반환해 사용자가 청구 종료일까지 서비스를 계속 이용하도록 합니다.

취소했고 종료일까지 여유 기간인 "유예 기간" 중인지 확인하려면 `onGracePeriod` 메서드를 쓰세요:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

바로 취소하려면 `cancelNow` 메서드를 사용하세요:

```php
$user->subscription('default')->cancelNow();
```

즉시 취소하고 청구하지 않은 미터 사용량, 새 청구내역을 청구서로 생성하려면 `cancelNowAndInvoice`를 호출합니다:

```php
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점에 취소 예약하려면 `cancelAt`에 종료일을 전달하세요:

```php
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

사용자 모델 삭제 전에는 반드시 구독을 취소해야 합니다:

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### 구독 재개하기

취소한 구독이 유예 기간 중이면 `resume` 메서드로 구독을 재개할 수 있습니다:

```php
$user->subscription('default')->resume();
```

유예 기간 이내에 재개 시 즉시 청구하지 않고 원래 결제 주기에 따라 청구됩니다.

<a name="subscription-trials"></a>
## 구독 체험 기간

<a name="with-payment-method-up-front"></a>
### 선결제 방식 구독 체험

결제 수단을 미리 받아 체험 기간을 제공하려면 구독 생성 시 `trialDays` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

이 메서드는 DB 내 구독 레코드에 체험 종료 일자를 기록하며, Stripe에 청구 시작일을 체험 종료일 이후로 설정합니다. Stripe 대시보드에 미리 설정한 기본 체험 기간은 이 메서드 호출 시 덮어씌워집니다.

> [!WARNING]
> 체험 기간 종료일까지 구독을 취소하지 않으면 체험 종료 즉시 요금이 청구되므로, 사용자에게 만료 일정을 반드시 안내하세요.

`trialUntil` 메서드는 종료일을 `DateTime` 객체로 직접 지정할 수 있습니다:

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->addDays(10))
    ->create($paymentMethod);
```

체험 중인지 확인할 때는 사용자 인스턴스의 `onTrial` 또는 구독 인스턴스의 `onTrial`을 사용하세요:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

즉시 체험 종료하려면 `endTrial`을 호출합니다:

```php
$user->subscription('default')->endTrial();
```

기존 체험이 만료됐는지도 `hasExpiredTrial` 메서드로 확인할 수 있습니다:

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe 또는 Cashier에서 체험 기간 정의하기

체험 기간을 Stripe 대시보드에서 정하거나 Cashier에서 명시적으로 지정할 수 있습니다. Stripe에서 체험 기간을 정의하면, 새 구독뿐 아니라 과거 구독 이력 고객도 기본적으로 체험 기간을 갖습니다. 이때 체험 기간 없이 구독을 만들려면 `skipTrial()`을 명시적으로 호출해야 합니다.

<a name="without-payment-method-up-front"></a>
### 비선결제 방식 구독 체험

체험 기간 동안 결제 수단을 미리 받지 않으려면 사용자 등록 시 `trial_ends_at` 컬럼에 원하는 체험 종료일을 설정합니다:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]
> `trial_ends_at` 속성은 반드시 [날짜 캐스팅](/docs/12.x/eloquent-mutators#date-casting)으로 처리해 주세요.

이를 "일반 체험(Generic Trial)"이라 부르며, 구독과 직접 연결되어 있지 않습니다. `onTrial` 메서드는 현재 시점이 `trial_ends_at` 값보다 이전인지 판단해 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // 체험 기간 중인 사용자
}
```

체험 기간 종료 후 구독을 만들려면 기존과 같이 `newSubscription`을 호출하세요:

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

사용자의 체험 종료 시점을 조회하려면 `trialEndsAt`을 사용하며, 구독 타입 인수를 넘길 수도 있습니다:

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

특히 일반 체험 상태인지 확인하려면 `onGenericTrial` 메서드를 쓰면 됩니다:

```php
if ($user->onGenericTrial()) {
    // 일반 체험 기간 중
}
```

<a name="extending-trials"></a>
### 체험 기간 연장하기

`extendTrial` 메서드는 구독 생성 후 체험 기간을 연장합니다. 이미 체험이 만료돼 결제중인 상태라도, 사용자의 다음 청구서에서 적용할 수 있습니다:

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 체험 기간을 지금부터 7일 후로 연장
$subscription->extendTrial(
    now()->addDays(7)
);

// 기존 체험 종료일에 5일 추가
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe 웹훅 처리

> [!NOTE]
> 로컬 개발 시 웹훅 테스트에는 [Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용하세요.

Stripe는 다양한 이벤트를 웹훅으로 애플리케이션에 알립니다. 기본으로 Cashier 서비스 프로바이더가 웹훅 컨트롤러를 자동 등록하며, 들어오는 요청을 처리합니다.

Cashier 컨트롤러는 실패한 결제 취소, 고객 및 구독 업데이트, 결제 수단 변경 같은 기본 웹훅 이벤트를 자동 처리하지만, 원하는 이벤트는 확장해 처리할 수도 있습니다.

애플리케이션에서 Stripe 웹훅 URL을 반드시 Stripe 대시보드에 등록하세요. 기본 경로는 `/stripe/webhook`입니다. 활성화해야 할 웹훅 이벤트 목록은 다음과 같습니다:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

편의상 Cashier는 `cashier:webhook` Artisan 명령어를 제공합니다. 이 명령어로 Cashier가 필요한 이벤트를 listen하는 Stripe 웹훅을 만듭니다:

```shell
php artisan cashier:webhook
```

기본으로 `APP_URL`과 `cashier.webhook` 라우트가 조합된 URL을 등록하며, `--url` 옵션으로 다른 URL 지정 가능합니다:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

등록된 웹훅은 Cashier 호환 Stripe API 버전을 사용합니다. 다른 버전을 원하면 `--api-version` 옵션을 지정하세요:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

필요하면 `--disabled` 옵션으로 생성은 하지만 비활성 상태로 둘 수도 있습니다:

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Cashier에서 제공하는 [웹훅 서명 검증](#verifying-webhook-signatures) 미들웨어로 Stripe 웹훅 요청을 반드시 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Stripe 웹훅 요청은 Laravel의 [CSRF 보호](/docs/12.x/csrf)를 우회해야 하므로, 애플리케이션 `bootstrap/app.php`에서 `stripe/*` 경로는 CSRF 예외로 등록해야 합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의하기

Cashier는 공통 웹훅 이벤트는 자체 처리하지만, 추가 이벤트를 받고 싶으면 Cashier가 발생하는 이벤트를 리스닝하세요:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

두 이벤트 모두 Stripe 웹훅 전체 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` 이벤트를 처리하려면 이벤트 리스너를 다음처럼 만드세요:

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
            // 이벤트 처리...
        }
    }
}
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안을 위해 [Stripe 웹훅 서명](https://stripe.com/docs/webhooks/signatures)을 사용하세요. Cashier는 들어오는 Stripe 웹훅 요청의 진위를 검증하는 미들웨어를 기본 포함합니다.

서명 검증을 활성화하려면 `.env`에 `STRIPE_WEBHOOK_SECRET` 환경 변수를 설정하고, 값을 Stripe 대시보드에서 받으세요.

<a name="single-charges"></a>
## 단일 결제

<a name="simple-charge"></a>
### 간단한 결제하기

한 번에 한 번만 결제하는 경우, 결제 가능한 모델 인스턴스의 `charge` 메서드를 사용하세요. 결제 수단 ID를 두 번째 인수로 제공해야 합니다:

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

세 번째 인수로 Stripe 결제 생성 옵션 배열을 넘길 수 있습니다. 상세한 옵션은 [Stripe 문서](https://stripe.com/docs/api/charges/create)를 참고하세요:

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

모델이 아닌 기본 결제 가능한 모델의 새 인스턴스에도 `charge`를 호출할 수 있습니다:

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

결제 실패 시 `charge`는 예외를 발생시키며, 성공 시 `Laravel\Cashier\Payment` 인스턴스를 반환합니다:

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // 예외 처리...
}
```

> [!WARNING]
> 결제 금액은 애플리케이션 통화의 최소 단위로 지정해야 합니다. 예를 들어, 미국 달러일 땐 센트 단위로 금액을 지정하세요.

<a name="charge-with-invoice"></a>
### 청구서와 함께 결제하기

청구서 PDF를 고객에게 제공하는 단일 결제는 `invoicePrice` 메서드를 사용하세요. 예:

```php
$user->invoicePrice('price_tshirt', 5);
```

기본 결제 수단으로 즉시 청구합니다. 세 번째 인수(배열)는 청구서 아이템 옵션, 네 번째 인수는 청구서 옵션입니다:

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

`invoicePrice`와 유사하게 여러 아이템(최대 250개)을 고객의 "tab"에 추가 후 청구하는 `tabPrice` 메서드도 있습니다:

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

`invoiceFor` 메서드로도 간단한 금액을 청구할 수 있습니다:

```php
$user->invoiceFor('One Time Fee', 500);
```

그러나 `invoicePrice`와 `tabPrice`로 사전 정의한 가격을 사용하는 게 Stripe 대시보드 내에서 상품별 분석에 유리합니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor`는 실패 결제를 재시도하는 Stripe 청구서를 생성합니다. 실패 시 재시도 원치 않으면 Stripe API로 청구서를 닫아야 합니다.

<a name="creating-payment-intents"></a>
### 결제 인텐트 생성하기

결제 가능한 모델 인스턴스의 `pay` 메서드로 Stripe 결제 인텐트를 만듭니다. 반환값은 `Laravel\Cashier\Payment` 인스턴스입니다:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

생성한 클라이언트 시크릿을 프론트엔드에 넘겨주어 사용자가 브라우저에서 결제를 진행하도록 합니다. Stripe 결제 인텐트 전체 과정은 [Stripe 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

`pay` 메서드 사용 시 Stripe 대시보드 내 활성화된 기본 결제 수단 메서드를 모두 사용할 수 있습니다. 특정 결제 수단만 허용하고 싶다면 `payWith` 메서드를 쓰세요:

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
> `pay`, `payWith` 메서드에 전달하는 금액은 통화 최소 단위로 지정하세요. (예: 달러는 센트 단위)

<a name="refunding-charges"></a>
### 결제 환불하기

결제 환불하려면 결제 인텐트 ID를 첫 번째 인수로 `refund` 메서드를 호출하세요:

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 청구서

<a name="retrieving-invoices"></a>
### 청구서 조회하기

결제 가능한 모델의 모든 청구서 목록은 `invoices` 메서드로 컬렉션 형태로 가져옵니다:

```php
$invoices = $user->invoices();
```

대기 중인 청구서도 포함하려면 `invoicesIncludingPending` 메서드를 사용하세요:

```php
$invoices = $user->invoicesIncludingPending();
```

특정 청구서는 `findInvoice`로 조회합니다:

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 청구서 정보 표시하기

목록을 표로 보여주고 다운로드 링크도 만들려면, 청구서 객체의 메서드를 활용하세요:

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
### 예정 청구서 조회

고객의 다음 예정 청구서를 조회할 때는 `upcomingInvoice` 메서드를 사용하세요:

```php
$invoice = $user->upcomingInvoice();
```

복수 구독 고객은 특정 구독 인스턴스에서 `upcomingInvoice`를 호출해 조회할 수 있습니다:

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 청구서 미리보기

가격 변경 전 예상 청구서를 미리 보려면 `previewInvoice` 메서드를 사용합니다. 변경할 가격 ID를 인수로 전달하세요:

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

여러 가격 ID 배열을 넘겨 다중 가격 구독 예상 청구서도 조회 가능합니다:

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 청구서 PDF 생성하기

청구서 PDF 생성을 위해 [dompdf](https://github.com/dompdf/dompdf) 패키지를 설치합니다:

```shell
composer require dompdf/dompdf
```

라우트나 컨트롤러에서 `downloadInvoice` 메서드로 PDF 다운로드 응답을 생성하세요:

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

청구서 데이터 기본값은 Stripe 고객 및 청구서 데이터에서 가져오며, 파일명은 `app.name` 구성 값에 따릅니다. 둘째 인수 배열로 회사 및 제품 정보 등 일부 항목을 사용자 지정할 수 있습니다:

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

셋째 인수로 파일명을 지정할 수도 있으며, `.pdf` 확장자가 자동 붙습니다:

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 청구서 렌더러

Cashier는 기본 `DompdfInvoiceRenderer` 외에, 원하는 대로 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현해 커스텀 렌더러를 쓸 수 있습니다.

아래 예제는 외부 PDF 변환 API를 호출하는 렌더러 구현 예시입니다:

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * 주어진 인보이스를 렌더링해 PDF 바이트를 반환
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

커스텀 렌더러를 구현했다면, 애플리케이션 `config/cashier.php` 내 `cashier.invoices.renderer` 값을 클래스명으로 바꾸세요.

<a name="checkout"></a>
## 체크아웃

Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)도 지원합니다. Stripe Checkout은 직접 결제 페이지를 구현해야 하는 부담을 줄여주는 사전 구축(hosted) 결제 페이지입니다.

이 문서는 Cashier로 Stripe Checkout을 시작하는 방법을 안내하며, Stripe Checkout 관련 보다 자세한 내용은 Stripe 공식 [Checkout 문서](https://stripe.com/docs/payments/checkout)를 참고하세요.

<a name="product-checkouts"></a>
### 제품 체크아웃

Stripe 대시보드 내 사전에 정의된 가격을 가진 기존 제품에 대해 결제를 진행하려면 결제 가능한 모델에서 `checkout` 메서드를 사용하세요. `checkout` 메서드는 새 Stripe Checkout 세션을 만듭니다. 기본적으로 Stripe 가격 ID를 넘겨야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

상품 수량도 넘길 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

기본 리디렉션 경로는 `home`이지만, `success_url`과 `cancel_url` 옵션으로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

성공 URL 쿼리 문자열에 `{CHECKOUT_SESSION_ID}`를 추가하면 Stripe가 세션 ID로 치환합니다:

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
#### 프로모션 코드

기본적으로 Stripe Checkout은 [사용자가 직접 사용할 수 있는 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 허용하지 않습니다. `allowPromotionCodes` 메서드 호출로 활성화하세요:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 단건 결제 체크아웃

Stripe 대시보드에 등록되지 않은 임시 상품에 대해 결제를 진행하려면 결제 가능한 모델의 `checkoutCharge` 메서드에 금액, 상품명과 수량(옵션)을 넘겨 사용하세요:

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge`를 줄곧 사용하면 Stripe 대시보드에 상품과 가격이 지속해서 생성되니, 가능하면 대시보드에서 미리 상품을 등록하고 `checkout`을 사용하는 것을 권장합니다.

<a name="subscription-checkouts"></a>
### 구독 체크아웃

> [!WARNING]
> Stripe Checkout으로 구독을 시작하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다. 이 웹훅은 애플리케이션 DB 내 구독 레코드를 생성하고 관련 아이템을 저장합니다.

구독을 설정하려면 구독 빌더 호출 후 `checkout` 메서드를 호출합니다. 고객은 Stripe Checkout 페이지로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

제품 체크아웃처럼 취소 및 성공 리디렉션 URL을 지정할 수 있습니다:

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

프로모션 코드 적용도 가능합니다:

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
> Stripe Checkout은 구독 빌더의 `anchorBillingCycleOn`, 가격 변경과 같은 일부 구독 청구 옵션을 지원하지 않습니다. 상세 사항은 [Stripe Checkout 세션 API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout과 체험 기간

Stripe Checkout을 통한 구독 생성 시 체험 기간을 설정할 수 있으나 최소 48시간 이상이어야 합니다:

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독과 웹훅

웹훅을 통해서만 구독 상태가 업데이트되므로, 결제 완료 후 애플리케이션에 방문하는 시점에 구독이 아직 활성화되지 않았을 수 있습니다. 이 점을 사용자에게 사전에 안내하는 UI가 필요합니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집

체크아웃 시 고객의 세금 ID를 수집하려면 `collectTaxIds` 메서드를 체인해서 호출하세요:

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

고객에게 회사 소속 여부 확인과 Tax ID 입력 칸을 제공합니다.

> [!WARNING]
> 이미 [자동 세금 계산](#tax-configuration) 구성이 되어 있다면 이 기능은 자동 활성화되므로 `collectTaxIds` 호출이 필요 없습니다.

<a name="guest-checkouts"></a>
### 게스트 체크아웃

계정 없는 고객(게스트)을 위한 체크아웃 세션 생성 시 `Checkout::guest`를 사용하세요:

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

기존 결제 가능한 모델과 마찬가지로 `CheckoutBuilder` 메서드를 체인해 프로모션 코드 등을 설정할 수 있습니다:

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

게스트 체크아웃 후 Stripe가 `checkout.session.completed` 웹훅을 보내므로, Stripe 대시보드에서 이 이벤트 전송을 활성화하고 [Cashier 웹훅 처리](#handling-stripe-webhooks)를 구성하세요.

웹훅 페이로드에 포함된 Checkout 객체를 분석해 주문 처리를 구현할 수 있습니다.

<a name="handling-failed-payments"></a>
## 결제 실패 처리하기

구독 또는 단건 결제 실패 시 `Laravel\Cashier\Exceptions\IncompletePayment` 예외가 발생합니다. 이 예외를 잡은 후 두 가지 방법으로 처리할 수 있습니다.

첫째, Cashier가 제공하는 결제 확인 페이지로 고객을 리디렉션합니다. 이 페이지는 이미 서비스 프로바이더가 등록한 명명된 라우트가 있습니다:

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

결제 확인 페이지에서 고객은 카드 정보 재입력, "3D Secure" 확인 등 Stripe가 요구하는 추가 인증을 진행할 수 있습니다. 처리 성공 후엔 `redirect` 파라미터로 지정된 URL로 리디렉션됩니다. 이때 URL에 `message`(알림문자열)와 `success`(성공 여부, 1 또는 0) 쿼리 변수가 자동으로 추가됩니다.

현재 결제 페이지는 다음 결제 수단 유형을 지원합니다:

- 신용카드
- Alipay
- Bancontact
- BECS 직불카드
- EPS
- Giropay
- iDEAL
- SEPA 직불카드

둘째, Stripe의 자동 결제 확인 이메일을 활용하는 방법이 있습니다. 그러나 `IncompletePayment` 예외 발생 시 사용자에게 이메일 수신 예정임을 알려야 합니다.

`charge`, `invoiceFor`, `invoice`, `SubscriptionBuilder`의 `create`, `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 메서드에서 결제 실패 예외가 발생할 수 있습니다.

기존 구독에 미확인 결제가 있으면 `hasIncompletePayment` 메서드로 확인하세요:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

예외 객체에서 자세한 결제 상태는 `payment` 속성에서 확인합니다:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 인텐트 상태 조회
    $exception->payment->status;

    // 상황별 분기 처리
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="confirming-payments"></a>
### 결제 확인

SEPA 등 일부 결제 방식은 결제 확인에 추가 데이터가 필요합니다. `withPaymentConfirmationOptions` 메서드로 확인 옵션을 지정할 수 있습니다:

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

결제 확인 시 accepted 옵션 전부는 Stripe API 문서([confirm](https://stripe.com/docs/api/payment_intents/confirm))를 참고하세요.

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증 (SCA)

유럽 소재 사업체 또는 고객은 EU의 강력한 고객 인증(SCA) 규정을 준수해야 합니다. 이 규정은 2019년 9월 도입돼 결제 사기를 예방합니다. Stripe와 Cashier는 SCA 규정에 맞는 앱 개발을 지원합니다.

> [!WARNING]
> 시작 전 Stripe의 [PSD2 및 SCA 가이드](https://stripe.com/guides/strong-customer-authentication) 및 [새 SCA API 문서](https://stripe.com/docs/strong-customer-authentication)를 반드시 읽어보세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 결제 확인이 필요한 경우

SCA 규정은 종종 결제 확인에 추가 인증을 요구합니다. 이런 상황에서 Cashier는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 던집니다. 이 예외 처리법은 [결제 실패 처리](#handling-failed-payments)를 참고하세요.

Stripe나 Cashier가 제공하는 결제 인증 화면은 지급 은행이나 카드 발급사별로 더 엄격한 카드 인증, 임시 소액 청구, 별도 기기 인증 등 다양한 검증 절차가 포함될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
#### `incomplete` 및 `past_due` 상태

추가 인증이 필요한 결제는 DB `stripe_status` 컬럼에서 `incomplete` 또는 `past_due` 상태가 됩니다. 인증 완료 및 Stripe 웹훅 통지 후 Cashier가 구독을 자동 활성화합니다.

`incomplete` 및 `past_due` 상태에 대해서는 [별도 설명](#incomplete-and-past-due-status)을 참고하세요.

<a name="off-session-payment-notifications"></a>
### 오프 세션 결제 알림

SCA 규정으로 활성 구독 중에도 고객이 오프 세션 결제 확인을 가끔 해야 하므로, Cashier는 결제 확인 필요 시 고객에게 알림을 보내는 기능을 제공합니다.

알림을 활성화하려면 `.env`에 알림 클래스명을 `CASHIER_PAYMENT_NOTIFICATION` 변수로 작성하세요. 기본은 비활성화입니다. Cashier 기본 알림 클래스가 포함되어 있으며, 원하는 대로 커스텀 알림 클래스를 등록할 수 있습니다:

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

오프 세션 결제 알림이 제대로 전달되려면 Stripe 웹훅이 구성되어 있어야 하며, Stripe 대시보드에서 `invoice.payment_action_required` 웹훅 이벤트가 활성화되어 있어야 합니다. 또한, `Billable` 모델은 Laravel `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다.

> [!WARNING]
> 고객이 직접 결제하는 경우에도 알림이 전송될 수 있습니다. Stripe는 결제 방식(수동/오프 세션)을 구분할 수 없으며, 고객이 결제 확인 페이지를 방문하면 중복 확인이 불가하도록 처리해 이중 청구를 방지합니다.

<a name="stripe-sdk"></a>
## Stripe SDK

Cashier 객체들은 Stripe SDK 객체를 감싸고 있습니다. Stripe 객체를 직접 조작하려면 `asStripe` 메서드를 활용하세요:

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

Stripe 구독 객체를 직접 업데이트하려면 `updateStripeSubscription` 메서드를 사용할 수 있습니다:

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

Stripe 클라이언트를 직접 사용하려면 `Cashier::stripe()` 메서드를 호출하세요. 예를 들어 가격 목록 조회:

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트

Cashier 기반 애플리케이션 테스트 시 Stripe API 호출을 모킹할 수도 있지만, Cashier 동작을 부분 재구현해야 하므로 권장하지 않습니다.

대신 테스트에서 실제 Stripe API 호출을 허용하는 편이 더 신뢰할 수 있습니다. 속도가 느리지만 Cashier 동작 전체를 테스트할 필요 없이 애플리케이션 내 결제 및 구독 흐름만 집중 테스트할 수 있습니다.

우선 `phpunit.xml` 등에 테스트용 Stripe 비밀키를 추가하세요:

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

이후 테스트 중 Cashier는 Stripe 테스트 환경으로 직접 API 호출을 보냅니다. Stripe 테스트 계정에 테스트용 구독/가격을 미리 채워두는 것을 권장합니다.

> [!NOTE]
> 카드 거부, 결제 실패 등 다양한 시나리오 테스트를 위해 Stripe가 제공하는 방대한 [테스트 카드 번호 및 토큰](https://stripe.com/docs/testing)을 사용하세요.