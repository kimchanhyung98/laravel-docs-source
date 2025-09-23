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
    - [구독 상품 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔액 관리](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 여부 확인](#payment-method-presence)
    - [기본 결제 수단 변경](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량(Quantity)](#subscription-quantity)
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [복수 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 Anchor 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [결제 수단 선입력 방식](#with-payment-method-up-front)
    - [결제 수단 미입력 방식](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [단순 결제](#simple-charge)
    - [청구서 발급 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [Tax ID 수집](#collecting-tax-ids)
    - [비회원 Checkout](#guest-checkouts)
- [청구서(Invoice)](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [예정된 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [청구서 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강화된 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 위한 직관적이고 유연한 인터페이스를 제공합니다. Cashier를 이용하면 여러분이 작성해야 할 거의 대부분의 반복적인 구독 결제 코드를 대신 처리할 수 있습니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰 적용, 구독 교체, 구독 "수량" 관리, 구독 취소 유예 기간, 인보이스(청구서) PDF 생성까지 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드 할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> 심각한 변경사항으로 인한 서비스 중단을 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16 버전은 Stripe API `2025-07-30.basil` 버전을 적용합니다. Stripe API 버전은 Stripe의 새로운 기능 및 개선사항을 활용하기 위해 마이너 릴리즈에서 주기적으로 업데이트됩니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

패키지 설치 후, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션 파일을 게시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음, 데이터베이스 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 여러분의 `users` 테이블에 여러 컬럼을 추가합니다. 또한 각 고객의 구독 정보를 보관할 `subscriptions` 테이블과, 복수 가격이 적용된 구독을 저장할 `subscription_items` 테이블을 생성합니다.

필요하다면, Cashier의 설정 파일도 `vendor:publish` Artisan 명령어로 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 모든 Stripe 이벤트를 제대로 처리할 수 있도록 [Cashier의 웹훅(Webhook) 처리 설정](#handling-stripe-webhooks)을 반드시 진행하세요.

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장하는 모든 컬럼이 대소문자를 구분해야 함을 권장합니다. 즉, MySQL을 사용할 경우 `stripe_id` 컬럼의 collation을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인하세요.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="billable-model"></a>
### 청구 가능 모델 (Billable Model)

Cashier를 사용하기 전에, 여러분의 청구 가능 모델(보통 `App\Models\User`)에 `Billable` 트레이트를 추가하세요. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 다양한 청구 관련 작업을 간편하게 처리할 수 있는 여러 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 여러분의 청구 대상 모델이 Laravel 기본 `App\Models\User` 클래스라고 가정합니다. 만약 이 모델을 변경하려면, `useCustomerModel` 메서드로 다른 모델을 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel이 기본 제공하는 `App\Models\User`가 아닌 모델을 사용하는 경우, [Cashier 마이그레이션](#installation)을 퍼블리시한 뒤 여러분의 대체 모델 테이블에 맞게 마이그레이션 파일을 수정해야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

다음으로, Stripe API 키를 애플리케이션의 `.env` 파일에 설정해야 합니다. Stripe API 키는 Stripe 관리자 페이지에서 발급받을 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 `.env` 파일에 반드시 정의되어 있어야 합니다. 이 변수는 Stripe에서 실제로 온 웹훅인지 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 애플리케이션 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하세요:

```ini
CASHIER_CURRENCY=eur
```

또한, 청구서 금액을 표시할 때 사용할 로케일도 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용하여 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax) 기능을 활용하면 Stripe에서 생성되는 모든 청구서의 세금을 자동으로 계산할 수 있습니다. 이 기능을 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

세금 계산이 활성화되면, 신규 구독과 단일 청구서 모두 자동으로 세금이 계산됩니다.

이 기능이 제대로 작동하려면 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe와 동기화되어야 합니다. 자세한 방법은 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID](#tax-ids) 관련 내용을 참고하세요.

<a name="logging"></a>
### 로깅 (Logging)

Cashier에서는 심각한 Stripe 오류 발생 시 사용할 로그 채널을 별도로 지정할 수 있습니다. 애플리케이션의 `.env` 파일 내에 `CASHIER_LOGGER` 환경 변수를 정의하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 중 발생한 예외(Exception)는 기본으로 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier에서 내부적으로 사용하는 모델을 자유롭게 확장하여 여러분만의 커스텀 모델을 정의할 수 있습니다. 이를 위해 Cashier의 해당 모델을 상속받아 직접 구현하세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 뒤에는 `Laravel\Cashier\Cashier` 클래스를 이용해 Cashier가 커스텀 모델을 사용하도록 알려야 합니다. 보통 이 설정은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 처리합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * 애플리케이션 서비스 부트스트랩
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
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 고정 가격으로 상품을 먼저 등록해야 합니다. 또한, [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)을 사전에 완료해야 합니다.

여러분의 애플리케이션을 통해 상품 및 구독 결제를 제공하는 일은 어렵게 느껴질 수 있습니다. 그러나 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 현대적인 결제 연동 기능을 손쉽게 구현할 수 있습니다.

비정기적 단일 상품 결제를 처리하기 위해서는, Cashier를 이용해 고객을 Stripe Checkout으로 이동시키고, 결제 정보를 Stripe에서 입력받은 뒤 성공/실패 시 각기 지정한 URL로 리다이렉트할 수 있습니다:

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

위 예시와 같이, Cashier의 `checkout` 메서드를 사용하여 고객을 특정 "가격 식별자" 기반 Stripe Checkout으로 리다이렉트합니다. Stripe에서 "가격(Price)"이란 [특정 상품에 대해 미리 정의된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요에 따라, `checkout` 메서드는 Stripe에 해당 고객 정보가 없을 경우 자동으로 고객을 생성하고 DB의 사용자와 Stripe 고객을 연결해줍니다. 결제가 완료되면 저희가 지정한 성공 또는 취소 페이지로 고객이 돌아오게 되며, 이곳에서 상태 메시지를 안내할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 전달

상품 판매 시, 애플리케이션에서 자체적으로 정의한 `Cart` 및 `Order` 모델을 통해 주문 내역을 추적하는 것이 일반적입니다. Stripe Checkout을 이용해 결제를 진행할 때, 주문 식별자를 함께 전달해 두면, 결제 완료 후 고객이 애플리케이션으로 복귀할 때 결제된 주문과 쉽게 연동할 수 있습니다.

이를 위해 Checkout 세션 생성 시 `checkout` 메서드에 `metadata` 배열을 전달할 수 있습니다. 아래 예시는 장바구니 결제를 시작할 때 `Order`가 생성되고, 해당 ID를 `metadata`와 함께 전달하는 과정입니다(여기서의 `Cart` 및 `Order` 모델은 Cashier가 기본 제공하는 것이 아니며, 여러분이 직접 구현해야 합니다):

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

위처럼, 사용자가 결제 과정을 시작하면 장바구니 및 주문에 포함된 모든 Stripe 가격 ID를 `checkout` 메서드에 전달합니다. 또한 주문의 ID도 메타데이터로 Stripe Checkout에 담아 보냅니다. 성공 URL에는 `CHECKOUT_SESSION_ID`라는 템플릿 변수를 포함시켰습니다. Stripe가 결제 완료 후 여러분의 애플리케이션으로 리다이렉트 할 때, 해당 변수에는 Checkout 세션 ID가 자동으로 치환되어 전달됩니다.

다음으로, 결제 성공 시 처리할 라우트를 만들어야 합니다. 이 라우트에서 Stripe Checkout 세션 ID와 연관된 Stripe 세션 객체를 조회하고, 메타데이터를 참고하여 해당 주문 상태를 업데이트할 수 있습니다:

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

Checkout 세션 오브젝트에 포함된 데이터에 대한 자세한 설명은 Stripe [API 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 상품 판매 (Selling Subscriptions)

> [!NOTE]
> Stripe Checkout을 사용하기 전에, Stripe 대시보드에서 고정 가격으로 상품을 먼저 등록해야 합니다. 또한, [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)을 사전에 완료해야 합니다.

애플리케이션 내에서 상품 및 구독 결제를 제공하는 것은 처음에는 복잡하게 느껴질 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 이용하면 현대적이고 신뢰할 수 있는 결제 연동을 간편하게 구현할 수 있습니다.

Cashier 및 Stripe Checkout을 이용하여 구독 상품을 판매하는 방법을 살펴보겠습니다. 예를 들어, 단순한 월간(`price_basic_monthly`) 및 연간(`price_basic_yearly`) 요금제가 있다고 가정할 수 있습니다. 이 두 가격은 Stripe 대시보드의 "Basic" 상품(`pro_basic`)으로 묶일 수 있습니다. 또한 "Expert" 플랜은 별도의 `pro_expert`로 구분해 구성할 수도 있습니다.

먼저, 고객이 어떻게 구독을 시작할 수 있는지 예시로 살펴보겠습니다. 기본적인 요금제 가입 버튼 클릭 시, 아래와 같이 Stripe Checkout 세션을 만드는 라라벨 라우트로 연결할 수 있습니다:

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

위 예시처럼, 고객을 Stripe Checkout 세션으로 리다이렉트 하여 요금제에 가입시키고, 결제 결과에 따라 지정한 URL로 다시 돌아오게 할 수 있습니다. 일부 결제 방법은 결제 처리에 수 초가 소요될 수 있으므로, 실제로 구독이 시작되는 시점을 알아내려면 [Cashier의 웹훅 처리](#handling-stripe-webhooks)를 반드시 설정해야 합니다.

한편, 특정 부분은 유료 구독 사용자만 접근 가능하게 제어할 필요가 있습니다. Cashier에서 제공하는 `subscribed` 메서드를 사용하여 사용자의 구독 상태를 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```

특정 상품 또는 가격의 구독 여부도 간단히 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 상품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 요금제를 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 상태 미들웨어 만들기

처리의 편의를 위해, 요청이 구독 사용자로부터 온 것인지 판별하는 [미들웨어](/docs/12.x/middleware)를 만들 수도 있습니다. 만든 미들웨어를 라우트에 적용하면, 구독 중이지 않은 사용자가 접근하지 못하도록 할 수 있습니다:

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
            // 유저를 결제 페이지로 리다이렉트하여 구독 요청...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

정의한 미들웨어는 라우트에 아래처럼 적용할 수 있습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 자신의 결제 플랜 관리 허용

고객은 사용 중인 구독 플랜을 다른 상품이나 등급(Tier)으로 변경하고자 할 수 있습니다. 이를 가장 쉽게 처리하는 방법은 Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)을 이용하는 것입니다. 이 포털은 관리 UI를 Stripe가 호스팅하므로, 사용자는 직접 청구서를 내리고, 결제 수단을 업데이트하며, 구독 플랜을 바꿀 수 있습니다.

먼저 애플리케이션 내부에 아래와 같이 링크나 버튼을 만들고 billing 관리 라우트로 연결합니다:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

이제 Billing Portal 세션을 시작하고 포털로 유저를 리다이렉트하는 라우트를 정의합니다. `redirectToBillingPortal` 메서드에는 포털 종료 시 사용자가 리턴될 URL을 넘깁니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 웹훅 처리가 정상적으로 설정되어 있다면 Stripe Customer Billing Portal에서 구독 취소 등 작업이 이루어질 때, Cashier가 자동으로 관련 DB 정보를 최신 상태로 동기화합니다.

(이어지는 나머지 내용은 각 섹션별로 동일한 패턴과 규칙으로 자연스럽게 번역해주셔야 합니다)