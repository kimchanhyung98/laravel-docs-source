# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용하기](#using-custom-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객(Customer)](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔액(Balances)](#balances)
    - [세금 ID 관리](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털(Billing Portal)](#billing-portal)
- [결제 수단(Payment Methods)](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독(Subscriptions)](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량(Quantity)](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 청구](#usage-based-billing)
    - [구독 세금 처리](#subscription-taxes)
    - [구독 청구 주기 기준일 지정](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 트라이얼](#subscription-trials)
    - [선불 결제수단과 함께 트라이얼](#with-payment-method-up-front)
    - [결제수단 없이 트라이얼 제공](#without-payment-method-up-front)
    - [트라이얼 기간 연장하기](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 핸들러 정의하기](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [단일 결제 처리](#single-charges)
    - [간단 결제](#simple-charge)
    - [청구서와 함께 결제](#charge-with-invoice)
    - [결제 의도 생성하기](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원(Guest) Checkout](#guest-checkouts)
- [청구서(Invoices)](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [예정된 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [청구서 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK 통합](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 Stripe의 구독 결제 서비스를 쉽게 사용할 수 있도록 유창하고 명확한 인터페이스를 제공합니다. 번거롭게 느껴질 수 있는 구독 결제 코드를 대부분 처리해 주며, 기본 구독 관리 외에도 쿠폰, 구독 변경, 구독 수량 조절, 취소 유예 기간 관리 그리고 청구서 PDF 생성까지 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

새 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인하세요.

> [!WARNING]  
> 변경으로 인한 문제 발생을 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. 마이너 릴리스가 있을 때마다 Stripe의 새로운 기능과 개선 사항을 반영하기 위해 API 버전을 업데이트합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

설치 후, `vendor:publish` Artisan 명령어를 사용해 Cashier의 마이그레이션 파일을 게시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그리고 데이터베이스 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

이 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하며, 고객의 구독 정보를 저장할 `subscriptions` 테이블과 다중 가격 구독용 `subscription_items` 테이블을 생성합니다.

필요하다면, `vendor:publish` Artisan 명령어를 다시 사용해 Cashier 구성 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, 모든 Stripe 이벤트를 제대로 처리하기 위해 [Cashier 웹훅 처리 설정](#handling-stripe-webhooks)을 꼭 구성하세요.

> [!WARNING]  
> Stripe ID를 저장하는 컬럼은 대소문자를 구분하도록 권장됩니다. MySQL을 사용하는 경우 `stripe_id` 컬럼의 콜레이션을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### Billable 모델

Cashier를 사용하기 전에, `Billable` 트레이트를 청구 가능한 모델에 추가하세요. 일반적으로는 `App\Models\User` 모델일 것입니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 일반적인 청구 작업을 수행할 수 있는 여러 메서드를 제공합니다:

```
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 `App\Models\User` 클래스를 청구 가능한 모델로 가정합니다. 다른 모델을 사용하려면 `Cashier::useCustomerModel` 메서드를 이용해 변경할 수 있습니다. 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
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
> Laravel 기본 `App\Models\User` 모델을 사용하지 않는 경우, [Cashier 마이그레이션](#installation)을 게시한 후 대체 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

앱의 `.env` 파일에서 Stripe API 키를 설정하세요. Stripe 대시보드에서 API 키를 받을 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]  
> 반드시 `STRIPE_WEBHOOK_SECRET` 변수를 `.env` 파일에 정의해야 합니다. 이 변수는 들어오는 웹훅이 실제 Stripe에서 온 것인지 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier 기본 통화는 미국 달러(USD)입니다. 필요하면 앱 `.env` 파일의 `CASHIER_CURRENCY` 환경 변수로 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

청구서에 표시되는 금액 서식을 위해서는 통화에 맞는 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 외 다른 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax)를 통해 Stripe에서 생성하는 모든 청구서의 세금을 자동 계산할 수 있습니다. 자동 세금 계산을 활성화하려면 앱의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `Cashier::calculateTaxes`를 호출하세요:

```
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

이 설정이 적용되면 새 구독이나 개별 청구서에 세금이 자동으로 계산됩니다.

원활한 기능을 위해 고객의 이름, 주소, 세금 ID 같은 청구 정보가 Stripe와 동기화되어야 합니다. Cashier의 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID 관리](#tax-ids) 기능을 이용해 구현할 수 있습니다.

<a name="logging"></a>
### 로깅

치명적인 Stripe 오류 로그를 기록할 채널을 설정할 수 있습니다. 앱 `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 지정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 중 발생하는 예외는 앱의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier 내부에서 사용하는 모델을 확장해 사용하려면, 먼저 해당 모델을 직접 정의하고 Cashier 모델을 상속하도록 하세요:

```
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

정의 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에 모델 변경 사실을 알려야 합니다. 보통 앱의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 다음과 같이 설정합니다:

```
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
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 상품 판매

> [!NOTE]  
> Stripe Checkout 사용 전에 Stripe 대시보드에서 가격이 고정된 제품을 정의해 두세요. 또한 [Cashier 웹훅 설정](#handling-stripe-webhooks)도 반드시 구성해야 합니다.

상품 및 구독 결제를 애플리케이션에 도입하려면 복잡해 보일 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)이 함께하면 쉽고 견고한 결제 통합을 구현할 수 있습니다.

한 번만 결제되는 상품에 대해 고객에게 비용을 청구하려면, Cashier의 `checkout` 메서드로 Stripe Checkout 페이지로 리다이렉트해 고객이 결제 정보를 입력하고 구매를 확정하도록 합니다. 결제가 완료되면 고객은 앱 내 지정한 성공 URL로 리디렉트됩니다:

```
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

예제에서 보듯, Cashier의 `checkout` 메서드는 "가격 ID(price identifier)"를 Stripe로 넘겨 고객을 Checkout 세션으로 안내합니다. Stripe에서 가격은 [특정 제품에 정해진 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요시 `checkout` 메서드는 Stripe 고객을 자동 생성하고, 생성한 Stripe 고객과 앱의 사용자 레코드를 연결합니다. Checkout 세션 종료 후 성공 또는 취소 페이지로 리디렉션되어 고객에게 안내 메시지를 표시할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 제공하기

주문 추적 목적으로 고객의 구매 내역을 `Cart`와 `Order` 모델로 관리하는 경우, Stripe Checkout으로 리디렉션할 때 기존 주문 ID를 전달해 결제 완료 후 앱 내 주문과 연동할 수 있습니다.

예를 들어, 사용자가 체크아웃을 시작할 때 앱에서 `Order` 모델을 생성한다고 가정합니다. `Cart`와 `Order`는 Cashier가 제공하는 모델이 아니므로 애플리케이션에 맞게 구현하십시오:

```
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

이 예에서 사용자가 결제를 시작하면, 장바구니와 주문에 속한 Stripe 가격 ID를 `checkout` 메서드에 전달합니다. 또한 주문 ID를 `metadata` 배열로 Checkout 세션에 넘겨줍니다. 성공 URL에 `{CHECKOUT_SESSION_ID}` 템플릿 변수를 삽입하면 Stripe가 실제 세션 ID로 대체합니다.

이제 결제 성공 라우트를 만들어 사용자가 결제를 완료하고 돌아왔다고 가정해 봅니다. 이 라우트에선 세션 ID로 Checkout 세션 데이터를 조회해 메타데이터를 확인하고 주문 상태를 업데이트할 수 있습니다:

```
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

Checkout 세션 객체에 관한 자세한 내용은 Stripe [공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]  
> Stripe Checkout 사용 전에 Stripe 대시보드에서 가격이 고정된 제품을 정의해 두십시오. 또한 [Cashier 웹훅 설정](#handling-stripe-webhooks)을 꼭 완료하세요.

상품과 구독 결제를 앱에서 제공하는 것은 어려워 보일 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 모던하고 견고한 결제 통합을 쉽게 구현할 수 있습니다.

간단한 시나리오로 월별(`price_basic_monthly`)과 연별(`price_basic_yearly`) 기본 플랜이 있는 구독 서비스를 생각해 봅시다. 이 두 가격은 Stripe 대시보드 내 "Basic" 제품(`pro_basic`)으로 그룹화할 수 있습니다. 또한 전문가 플랜 `pro_expert`도 있을 수 있습니다.

먼저, 고객이 우리 서비스를 구독하는 방법을 봅시다. 고객이 앱의 가격 페이지에서 Basic 플랜 구독 버튼을 클릭하면 Laravel 라우트가 호출되어 선택한 플랜에 대한 Stripe Checkout 세션이 생성됩니다:

```
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

위 코드처럼 고객은 Stripe Checkout 세션으로 리디렉션되고, Basic 플랜에 구독 방문을 하게 됩니다. 결제 성공 또는 취소 시 지정된 URL로 리디렉션됩니다. 구독이 실제 시작되었는지 확인하려면(일부 결제 방식은 처리까지 시간이 소요되므로), [Cashier 웹훅 처리](#handling-stripe-webhooks)를 반드시 설정하세요.

구독 시작 후에는 Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드로 사용자의 현재 구독 상태를 쉽게 체크할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 제품이나 가격에 가입했는지도 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 제품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월별 Basic 플랜을 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독자 전용 미들웨어 만들기

특정 라우트에 구독자만 접근하도록 제한하고 싶으면, 구독 여부를 확인하는 [미들웨어](/docs/11.x/middleware)를 직접 작성할 수 있습니다. 예시는 다음과 같습니다:

```
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
            // 청구 페이지로 리다이렉트하여 구독 유도
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

정의한 미들웨어는 라우트에 할당할 수 있습니다:

```
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객의 청구 구독 관리 허용하기

고객이 자신의 구독 요금제를 변경하고 싶다면 Stripe의 [고객 청구 포털(Billing Portal)](https://stripe.com/docs/no-code/customer-portal)을 이용하세요. 이 포털은 청구 내역 확인, 결제 수단 갱신, 구독 변경 등을 할 수 있는 호스팅된 UI를 제공합니다.

먼저, 앱 내에 고객이 청구 포털로 이동할 링크나 버튼을 만듭니다:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```

다음으로, 이 링크가 호출할 라우트를 정의하여 Stripe 청구 포털 세션을 생성하고 고객을 포털로 리디렉트합니다. `redirectToBillingPortal` 메서드에 포털 종료 후 돌아올 URL을 지정할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]  
> Cashier 웹훅 처리가 설정된 상태라면, Stripe 고객 포털에서 구독을 취소할 때도 Cashier가 해당 웹훅을 받아 앱 내 데이터베이스 구독 상태를 자동으로 취소됨으로 표시합니다.

<a name="customers"></a>
## 고객(Customer)

<a name="retrieving-customers"></a>
### 고객 조회

Stripe ID로 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 이 메서드는 청구 가능한 모델 인스턴스를 반환합니다:

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔 구독 없이 Stripe 고객만 생성하고 싶을 때가 있습니다. `createAsStripeCustomer` 메서드를 사용하면 됩니다:

```
$stripeCustomer = $user->createAsStripeCustomer();
```

옵션 배열 `$options`를 이용해 Stripe API에서 지원하는 추가 고객 생성 파라미터를 넘길 수도 있습니다:

```
$stripeCustomer = $user->createAsStripeCustomer($options);
```

Stripe 고객 객체를 반환받으려면 `asStripeCustomer` 메서드를 사용하세요:

```
$stripeCustomer = $user->asStripeCustomer();
```

기존에 Stripe 고객 여부를 모를 때는 `createOrGetStripeCustomer`를 사용하세요. 고객이 없으면 새로 생성해줍니다:

```
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 정보 업데이트

Stripe 고객 정보를 직접 업데이트해야 할 경우 `updateStripeCustomer` 메서드를 쓰세요. Stripe API가 지원하는 업데이트 옵션 배열을 넘기면 됩니다:

```
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액(Balances)

Stripe는 고객의 "잔액"을 입금하거나 출금하는 것을 지원합니다. 잔액은 이후 청구 시 결제에 반영됩니다. 전체 잔액 확인은 청구 가능한 모델 인스턴스의 `balance` 메서드를 사용하세요. 반환값은 고객 통화에 맞춰 포맷된 문자열입니다:

```
$balance = $user->balance();
```

잔액에 크레딧을 추가하려면 `creditBalance` 메서드를 사용하며, 설명 추가도 가능합니다:

```
$user->creditBalance(500, 'Premium customer top-up.');
```

잔액 차감은 `debitBalance`를 사용합니다:

```
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance`는 새 잔액 변동 트랜잭션을 생성합니다. 트랜잭션 목록 조회는 `balanceTransactions` 메서드를 이용하세요:

```
// 모든 거래 내역 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액...
    $amount = $transaction->amount(); // $2.31

    // 관련 청구서가 있을 경우 조회...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID 관리

Cashier는 고객의 세금 ID 목록 관리를 간편하게 지원합니다. 고객에게 할당된 모든 세금 ID는 `taxIds` 메서드로 컬렉션 형태로 조회할 수 있습니다:

```
$taxIds = $user->taxIds();
```

특정 세금 ID는 `findTaxId` 메서드로 식별자를 통해 조회하세요:

```
$taxId = $user->findTaxId('txi_belgium');
```

새 세금 ID 생성은 `createTaxId` 메서드를 사용하며, 유효한 타입과 값을 넘기면 즉시 고객 계정에 추가됩니다:

```
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

세금 ID의 유효성 검증은 Stripe가 비동기적으로 수행합니다. 검증 상태 업데이트는 `customer.tax_id.updated` 웹훅 이벤트를 구독해 처리하세요. 자세한 사항은 [웹훅 핸들링 문서](#handling-stripe-webhooks)를 참고하세요.

세금 ID 삭제는 `deleteTaxId` 호출로 수행합니다:

```
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화

고객 이름, 이메일 등 Stripe에 저장된 정보가 변경되면 Stripe 쪽에 변경 내용을 동기화하는 것이 좋습니다. 이를 위해 billable 모델의 `updated` 이벤트 리스너를 등록해 `syncStripeCustomerDetails` 메서드를 호출하면 자동 동기화됩니다:

```
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

최초 고객 생성 시에는 Cashier가 자동으로 동기화합니다.

추가로, Cashier가 동기화할 때 사용할 컬럼을 커스터마이징하려면 `stripeName`, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 메서드들을 오버라이드할 수 있습니다. 완전한 제어가 필요하다면 `syncStripeCustomerDetails` 메서드를 오버라이드하세요.

예를 들어, 고객 이름으로 `company_name` 컬럼을 쓰고 싶으면:

```
/**
 * Stripe에 동기화할 고객 이름 반환
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

<a name="billing-portal"></a>
### 청구 포털(Billing Portal)

고객이 직접 구독 관리, 결제 수단, 청구 내역 확인 등을 할 수 있도록 Stripe의 [청구 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 활용할 수 있습니다. `redirectToBillingPortal` 메서드를 호출해 사용자를 포털로 리디렉트하세요:

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 포털 종료 후 앱 내 `home` 경로로 돌아가지만, 인자로 URL을 넘겨 원하는 경로를 지정할 수도 있습니다:

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

포털의 URL만 생성하고 리다이렉트하지 않으려면 `billingPortalUrl` 메서드를 호출하세요:

```
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단(Payment Methods)

<a name="storing-payment-methods"></a>
### 결제 수단 저장

Stripe 구독 또는 단발성 결제를 위해 고객의 결제 수단을 저장하고 Stripe ID를 받아야 합니다. 구독과 단발 결제에서 절차가 다르므로 각각 설명합니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독 결제수단 저장

고객의 신용카드 정보를 구독 결제에 안전하게 저장하려면 Stripe "Setup Intents" API를 사용해야 합니다. Setup Intent는 고객의 결제를 준비한다는 의미입니다. Cashier Billable 트레이트의 `createSetupIntent` 메서드로 Setup Intent를 쉽게 생성할 수 있습니다:

```
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

생성한 Setup Intent 객체에서 비밀 키를 뷰로 넘기고, 이 키를 카드 정보 입력 폼에 붙입니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

Stripe.js 라이브러리를 사용해 Stripe Element를 폼에 장착하고 안전하게 카드 정보를 받습니다:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

그 다음 카드 정보를 검증하고 Stripe에서 결제 수단 식별자를 받는 콜백을 구현합니다:

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
        // 사용자에게 "error.message" 표시...
    } else {
        // 카드가 성공적으로 검증됨...
    }
});
```

검증 완료된 `setupIntent.payment_method` 식별자는 서버로 보내어 결제 수단 추가 또는 기본 결제 수단 업데이트에 사용할 수 있습니다. 바로 이 결제 수단으로 새 구독 생성도 가능합니다.

> [!NOTE]  
> Setup Intents에 관한 자세한 내용은 [Stripe 설명 문서](https://stripe.com/docs/payments/save-and-reuse#php)를 참조하세요.

<a name="payment-methods-for-single-charges"></a>
#### 단발 결제용 결제 수단 저장

단일 결제를 위해서만 결제 수단 식별자가 필요하므로 저장된 기본 결제 수단을 이용할 수 없습니다. Stripe.js 라이브러리로 결제 수단을 안전하게 수집해야 합니다. 예시 폼:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

Stripe Elements는 앞서 설명한 것과 동일하게 설정하세요.

결제 수단 생성은 Stripe의 `createPaymentMethod` 메서드를 사용합니다:

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
        // 사용자에게 "error.message" 표시...
    } else {
        // 카드가 성공적으로 검증됨...
    }
});
```

검증이 되면 `paymentMethod.id`를 서버로 보내어 단발 결제 처리에 사용하세요.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회

청구 가능한 모델 인스턴스에서 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다:

```
$paymentMethods = $user->paymentMethods();
```

특정 타입 결제수단만 조회하고 싶다면 타입을 인자로 넘깁니다:

```
$paymentMethods = $user->paymentMethods('sepa_debit');
```

기본 결제 수단 조회는 `defaultPaymentMethod` 메서드입니다:

```
$paymentMethod = $user->defaultPaymentMethod();
```

특정 결제 수단을 찾으려면 `findPaymentMethod`를 사용하세요:

```
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 결제 수단 존재 여부

기본 결제 수단이 있는지 확인하려면 `hasDefaultPaymentMethod`를 호출합니다:

```
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

아예 결제 수단이 하나 이상 있는지도 `hasPaymentMethod` 메서드로 체크할 수 있습니다:

```
if ($user->hasPaymentMethod()) {
    // ...
}
```

특정 타입 결제 수단 존재 여부 판단도 가능합니다:

```
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트

`updateDefaultPaymentMethod`는 할당할 Stripe 결제 수단 ID를 받고 고객의 기본 결제 수단으로 지정합니다:

```
$user->updateDefaultPaymentMethod($paymentMethod);
```

Stripe 내 고객 기본 결제 수단과 로컬 정보를 동기화하려면 `updateDefaultPaymentMethodFromStripe`를 호출하세요:

```
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]  
> Stripe 제한으로 기본 결제 수단은 인보이스 결제 및 구독 생성에만 사용 가능합니다. 단일 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가

새 결제 수단을 추가하려면 `addPaymentMethod`에 결제 수단 식별자를 넘기면 됩니다:

```
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]  
> 결제 수단 식별자 취득법은 [결제 수단 저장](#storing-payment-methods) 문서를 참조하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제

삭제할 `Laravel\Cashier\PaymentMethod` 인스턴스의 `delete` 메서드를 호출하거나:

```
$paymentMethod->delete();
```

청구 가능한 모델에서 특정 결제 수단 피해를 삭제하려면:

```
$user->deletePaymentMethod('pm_visa');
```

모든 결제 수단을 삭제하려면:

```
$user->deletePaymentMethods();
```

특정 타입만 삭제하려면 타입 인자를 전달하세요:

```
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]  
> 활성 구독이 있는 경우 사용자가 기본 결제 수단 삭제를 못하도록 앱에서 제한해야 합니다.

<a name="subscriptions"></a>
## 구독(Subscriptions)

구독은 고객의 반복 결제를 설정합니다. Cashier로 관리되는 Stripe 구독은 다중 가격, 수량, 트라이얼 기간 등을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성

먼저 일반적으로 `App\Models\User` 인스턴스를 조회하세요. 그 다음 `newSubscription` 메서드로 구독을 생성할 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

첫 번째 인자는 내부 구독 타입명으로, 공백 없이 보통 `default`나 `primary`를 사용합니다. 이 이름은 앱 내부용이며, 사용자에게는 노출하지 않습니다. 바꿀 수도 있으나 구독 생성 후에 변경하지 않는 것이 좋습니다. 두 번째 인자는 Stripe 내 가격 ID와 일치해야 합니다.

`create` 메서드는 Stripe 결제 수단 ID 또는 `PaymentMethod` 객체를 받아 구독 시작과 데이터베이스에 Stripe 고객 ID 및 기타 청구 정보를 기록합니다.

> [!WARNING]  
> 구독 생성 시 결제 수단 ID를 직접 전달하면 자동으로 사용자 결제 수단에 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 인보이스 이메일을 통한 반복 결제 수집

자동 결제 대신 Stripe가 결제 기한마다 고객에게 인보이스 이메일을 보내도록 할 수 있습니다. 고객은 이메일에서 수동으로 인보이스를 결제합니다. 결제 수단은 미리 수집할 필요가 없습니다:

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

고객이 인보이스를 결제할 시간(`days_until_due`)은 기본 30일이나 옵션으로 조절할 수 있습니다:

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 구독 수량 설정

구독 가격별 수량을 지정하려면 구독 생성 전 `quantity` 메서드를 체인하세요:

```
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 옵션 지정

Stripe API가 지원하는 고객(customers) 또는 구독(subscriptions) 관련 추가 옵션을 각각 두 번째, 세 번째 인자로 넘길 수 있습니다:

```
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
#### 쿠폰 적용

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용합니다:

```
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

Stripe 프로모션 코드를 적용하려면 `withPromotionCode`를 사용하세요:

```
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

`promo_code_id`는 고객에게 보이는 코드가 아니라 Stripe API ID임을 주의하세요. 고객 코드로부터 프로모션 코드 ID를 찾으려면 `findPromotionCode` 또는 활성 코드만 찾을 땐 `findActivePromotionCode`를 사용합니다:

```
// 고객 사랑하는 프로모션 코드로 ID 찾기...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// 활성 프로모션 코드로 ID 찾기...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

`Laravel\Cashier\PromotionCode` 객체 아래에는 Stripe `PromotionCode`가 있고, `coupon` 메서드로 쿠폰 정보를 가져올 수 있습니다:

```
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

쿠폰 타입에 따른 할인 금액이나 비율을 조회할 수도 있습니다:

```
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 예: 21.5%
} else {
    return $coupon->amountOff(); // 예: $5.99
}
```

현재 고객이나 구독에 적용중인 할인도 `discount` 메서드로 조회할 수 있습니다:

```
$discount = $billable->discount();

$discount = $subscription->discount();
```

할인 쿠폰은 `Stripe\Discount` 객체를 감싼 `Laravel\Cashier\Discount` 타입입니다. 쿠폰 정보는 `coupon()` 메서드로 얻습니다:

```
$coupon = $subscription->discount()->coupon();
```

새 쿠폰이나 프로모션 코드를 고객이나 구독에 적용하려면 각각 `applyCoupon` 또는 `applyPromotionCode`를 호출하세요:

```
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

쿠폰은 한 번에 한 개만 적용 가능하며, stripe API ID를 사용해야 합니다.

더 자세한 내용은 Stripe 문서의 [쿠폰](https://stripe.com/docs/billing/subscriptions/coupons) 및 [프로모션 코드](https://stripe.com/docs/billing/subscriptions/coupons/codes)를 참고하세요.

<a name="adding-subscriptions"></a>
#### 구독 추가

기본 결제 수단이 이미 있는 고객에 대해서 구독을 추가하려면 구독 빌더의 `add` 메서드를 사용하세요:

```
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 구독 생성하기

Stripe 대시보드에서 구독을 생성할 수도 있습니다. Cashier는 이런 구독을 동기화하여 타입을 `default`로 지정합니다. 다른 구독 타입을 설정하려면 [웹훅 이벤트 핸들러](#defining-webhook-event-handlers)를 작성하세요.

Stripe 대시보드는 여러 구독 타입 생성은 지원하지 않으므로, 앱에서 다중 구독 타입을 제공한다면 대시보드에서는 한 타입만 가능하다는 점도 유의하세요.

한 타입에 두 건 이상의 활성 구독이 존재하면 Cashier는 최신 구독만 사용하며, 이전 구독은 기록용으로만 보관합니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인하기

고객의 구독 상태를 확인하려면 다양한 편의 메서드를 사용하세요. `subscribed`는 활성 구독이 있으면 `true`를 반환하며, 트라이얼 기간도 포함합니다. 구독 타입을 인자로 넘길 수 있습니다:

```
if ($user->subscribed('default')) {
    // ...
}
```

이 메서드는 [라우트 미들웨어](/docs/11.x/middleware)로 사용해 구독자만 특정 URL에 접근하도록 제한하는 데도 효과적입니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * 들어오는 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 결제가 되지 않은 사용자...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

사용자의 트라이얼 기간 내 여부를 확인하려면 `onTrial` 메서드를 호출하세요:

```
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

`subscribedToProduct`는 Stripe 제품 식별자에 해당하는 제품에 가입되어 있는지 확인합니다. 제품은 여러 가격의 묶음입니다:

```
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

배열을 넘겨 여러 제품 구독 여부도 확인할 수 있습니다:

```
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

`subscribedToPrice`는 특정 가격 ID에 가입 여부를 반환합니다:

```
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

`recurring`는 현재 구독 중이며 트라이얼이 지난 상태 여부를 확인합니다:

```
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]  
> 동일 타입으로 두 개 이상의 구독이 있으면 항상 최신 구독이 `subscription` 메서드로 반환됩니다. 오래된 구독은 기록 보관용입니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

과거에 구독했으나 취소한 경우는 `canceled` 메서드로 확인할 수 있습니다:

```
if ($user->subscription('default')->canceled()) {
    // ...
}
```

취소 후 아직 유예 기간(`grace period`)에 있는 경우는 `onGracePeriod`로 확인합니다:

```
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

유예 기간이 지나 만료된 경우는 `ended`를 사용하세요:

```
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료(Incomplete) 및 연체(Past Due) 상태

이차 결제가 필요한 경우 구독은 `incomplete` 상태가 됩니다. 결제 방법 변경 시 `past_due`가 되기도 합니다. 이 상태 구독은 결제가 확정되어야 활성 상태가 됩니다. 모델 혹은 구독 인스턴스에서 다음 메서드로 체크할 수 있습니다:

```
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

미완료 결제가 있으면 Cashier 결제 확인 페이지로 유도하고, `latestPayment` 메서드로 결제 ID를 넘기세요:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    결제를 확인해주세요.
</a>
```

`past_due` 혹은 `incomplete` 상태일 때도 구독을 활성으로 보고 싶으면, `AppServiceProvider`의 `register` 메서드에 다음을 호출합니다:

```
use Laravel\Cashier\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]  
> `incomplete` 상태 구독은 결제 확인 전까지 변경할 수 없습니다. `swap` 또는 `updateQuantity` 메서드 호출 시 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 상태 쿼리 스코프

구독 DB 쿼리를 쉽게 하기 위해 다음과 같은 스코프를 사용할 수 있습니다:

```
// 활성 구독 조회...
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자 취소 구독 조회...
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 스코프 리스트:

```
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
### 가격 변경

고객 구독의 가격을 변경하려면 새 가격 ID를 `swap` 메서드에 넘기세요. 고객 구독 취소 상태라면 재활성화됩니다:

```
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

트라이얼 기간 유지, 수량도 유지합니다.

트라이얼을 무시하고 바로 가격 변경하려면 `skipTrial` 체인:

```
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

즉시 청구하려면 `swapAndInvoice` 메서드를 쓰세요:

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 요금 정산(Prorations)

가격 변경 시 기본적으로 Stripe는 정산을 적용합니다. 정산을 하지 않으려면 `noProrate` 메서드를 체인하세요:

```
$user->subscription('default')->noProrate()->swap('price_yearly');
```

> [!WARNING]  
> `noProrate`를 `swapAndInvoice` 앞에 호출해도 정산이 무시되지 않습니다. 인보이스가 항상 생성됩니다.

<a name="subscription-quantity"></a>
### 구독 수량

프로젝트 수에 따라 월 $10씩 과금하는 앱과 같이, 특정 가격에 수량이 반영될 수 있습니다. `incrementQuantity`와 `decrementQuantity` 메서드를 사용해 수량을 손쉽게 조절할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 5 증가하기...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 5 감소하기...
$user->subscription('default')->decrementQuantity(5);
```

특정 수량을 직접 지정하려면 `updateQuantity`를 호출합니다:

```
$user->subscription('default')->updateQuantity(10);
```

수량 변경 시 정산을 하지 않으려면 `noProrate` 메서드를 체인하세요:

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

더 자세한 내용은 Stripe [수량 문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독에서 수량 조절

[다중 상품 구독](#subscriptions-with-multiple-products)일 때는 두 번째 인자로 가격 ID를 넘겨 수량 조절하세요:

```
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독

[다중 상품 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)은 한 구독에 여러 과금 상품을 추가하는 기능입니다. 예를 들어 기본 구독 $10에 라이브 채팅 부가 서비스 $15 추가 가능하며, 관련 정보는 `subscription_items` 테이블에 저장됩니다.

`newSubscription` 두 번째 인자로 가격 ID 배열을 전달해 다중 상품 구독을 생성할 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', [
        'price_monthly',
        'price_chat',
    ])->create($request->paymentMethodId);

    // ...
});
```

필요하면 가격별로 수량 설정도 가능:

```
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 가격을 추가하려면 `addPrice` 사용:

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

즉시 청구까지 하려면 `addPriceAndInvoice`를 사용하세요:

```
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

수량 지정도 가능:

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

가격 제거는 `removePrice` 메서드 사용:

```
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]  
> 구독에서 마지막 남은 가격을 제거할 수 없으며, 구독을 취소해야 합니다.

<a name="swapping-prices"></a>
#### 가격 교체

다중 상품 구독의 가격을 교체하려면 `swap` 메서드에 배열로 가격을 넘깁니다. 예를 들어 `price_basic`과 `price_chat`을 가진 구독을 `price_pro`와 `price_chat`으로 변경할 때:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

`price_basic`에 대응하는 아이템이 삭제되고 `price_chat`은 유지되며 `price_pro` 아이템이 새로 생성됩니다.

수량 같은 옵션도 함께 지정할 수 있습니다:

```
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

단일 가격만 교체하고 싶으면, 해당 구독 아이템(`SubscriptionItem`)의 `swap` 메서드를 호출합니다:

```
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>
#### 요금 정산

가격 추가/제거 시 기본적으로 Stripe가 정산을 적용합니다. 정산 없이 변경하려면 `noProrate` 메서드를 체인하세요:

```
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량 변경

가격별 수량 변경은 기존 수량 메서드에 가격 ID를 추가로 넘기면 됩니다:

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]  
> 다중 가격 구독 시 `Subscription` 모델의 `stripe_price`와 `quantity` 속성은 `null`입니다. 개별 가격 정보는 `items` 관계에서 접근하세요.

<a name="subscription-items"></a>
#### 구독 아이템

다중 가격 구독은 DB `subscription_items` 테이블에 여러 아이템으로 저장됩니다. `Subscription` 모델의 `items` 관계로 접근 가능합니다:

```
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// 해당 아이템의 Stripe 가격과 수량 조회...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

특정 가격 아이템은 `findItemOrFail` 메서드로 조회할 수 있습니다:

```
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 다중 구독

Stripe는 고객 별로 여러 구독을 동시에 가질 수 있도록 지원합니다. 예를 들어 헬스장 회원이 수영 구독과 웨이트 트레이닝 구독을 별도로 구독할 수 있습니다. 두 구독에 각각 다른 가격이 할당될 수 있습니다.

`newSubscription` 메서드 첫 인자로 구독 타입명을 지정하세요:

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

구독 가격 변경은 해당 타입 구독에 대해 `swap` 호출:

```
$user->subscription('swimming')->swap('price_swimming_yearly');
```

전체 구독 취소도 가능합니다:

```
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### 사용량 기반 청구 (Usage Based Billing)

[사용량 기반 청구](https://stripe.com/docs/billing/subscriptions/metered-billing)는 고객이 정한 기간 내 제품 사용량에 따라 과금하는 방식입니다. 예를 들어 전송한 문자 수, 이메일 수에 비례해 비용 청구할 수 있습니다.

먼저 Stripe 대시보드에서 사용량 기반 청구 모델과 미터(meter)를 포함한 새 제품을 생성하세요. 미터 ID와 이벤트 이름은 사용량 보고와 조회 시 필요합니다. 구독 빌더에 `meteredPrice` 메서드를 호출해 가격 ID를 추가합니다:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

Stripe Checkout을 통한 metered 구독 시작도 가능합니다:

```
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

앱에서 고객의 사용량을 Stripe에 보고해 정확한 과금을 해야 합니다. `reportMeterEvent` 메서드를 호출해 이벤트 이름과 수량을 전달하세요:

```
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

기본 수량은 1이며, 필요하면 두 번째 인자로 수량을 지정할 수 있습니다:

```
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

특정 미터의 사용 요약을 `meterEventSummaries` 메서드로 조회할 수 있습니다:

```
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 예: 10
```

추가로, Stripe 문서의 [Meter Event Summary 객체](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참고하세요.

모든 미터 목록 조회는 `meters` 메서드로 가능합니다:

```
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
### 구독 세금 처리

> [!WARNING]  
> 수동으로 세율을 계산하지 말고 [Stripe Tax를 이용한 자동 세금 계산](#tax-configuration)을 권장합니다.

사용자별 구독에 적용할 세율 ID 배열을 billable 모델의 `taxRates` 메서드에서 반환하세요. 세율은 [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 정의합니다:

```
/**
 * 고객 구독에 적용할 세율 ID 배열 반환
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```

다중 상품 구독이라면 개별 가격별 세율도 아래와 같이 구현할 수 있습니다:

```
/**
 * 고객 구독에 적용할 가격별 세율 ID 배열 반환
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
> `taxRates`는 구독 청구에만 적용되며 Cashier에서 "단발 결제" 시 수동으로 세율을 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화

`taxRates`가 변경되어도 기존 구독의 세금 설정은 변경되지 않습니다. 기존 구독 세율을 동기화하려면 `syncTaxRates` 메서드를 호출하세요:

```
$user->subscription('default')->syncTaxRates();
```

이 메서드는 다중 상품 세율도 동기화합니다. 다중 상품 구독 시 billable 모델에 [priceTaxRates](#subscription-taxes) 메서드도 구현하세요.

<a name="tax-exemption"></a>
#### 면세 여부

Cashier는 고객의 면세 여부를 판단하는 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드를 제공합니다. Stripe API를 호출해 확인합니다:

```
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]  
> 이 메서드는 `Laravel\Cashier\Invoice` 객체에서 호출해 해당 청구서 생성 시점의 면세 여부를 분석할 수도 있습니다.

<a name="subscription-anchor-date"></a>
### 구독 청구 주기 기준일 지정

기본 청구 주기 기준일은 구독 생성일 또는 트라이얼 종료일입니다. 기준일을 바꾸려면 `anchorBillingCycleOn` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $anchor = Carbon::parse('first day of next month');

    $request->user()->newSubscription('default', 'price_monthly')
        ->anchorBillingCycleOn($anchor->startOfDay())
        ->create($request->paymentMethodId);

    // ...
});
```

자세한 내용은 Stripe [청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 `cancel` 메서드를 호출하세요:

```
$user->subscription('default')->cancel();
```

구독 취소 시 Cashier는 `subscriptions` 테이블의 `ends_at` 컬럼에 종료일을 기록합니다. 구독 종료 예정일까지는 `subscribed` 메서드가 `true`를 반환합니다.

예를 들어 구독자가 3월 1일에 구독을 취소하지만 종료일이 3월 5일이면, 3월 5일까지는 구독 상태로 인정됩니다. 이는 일반적으로 고객이 결제 기간까지 서비스를 이용할 수 있도록 하기 위함입니다.

취소 후 유예 기간인지 확인은 `onGracePeriod` 메서드:

```
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

즉시 취소하려면 `cancelNow` 호출:

```
$user->subscription('default')->cancelNow();
```

즉시 취소 후 미청구된 사용량을 포함해 인보이스 발행하려면 `cancelNowAndInvoice`:

```
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점에 취소할 수도 있습니다:

```
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

항상 사용자 모델 삭제 전에 구독을 취소하세요:

```
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### 구독 재개

고객이 구독을 취소했으나 유예 기간 내 다시 시작하려면 `resume` 메서드를 호출하세요:

```
$user->subscription('default')->resume();
```

기존 구독이 완전히 만료되기 전 재개하면 즉시 과금되지 않고 원래 청구 주기에 따라 과금됩니다.

<a name="subscription-trials"></a>
## 구독 트라이얼

<a name="with-payment-method-up-front"></a>
### 선불 결제수단과 함께 트라이얼 제공

트라이얼 기간 동안에는 결제수단 정보를 수집하면서 구독 시작 시 `trialDays` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

이 설정은 DB 구독 레코드에 트라이얼 종료일을 기록하고 Stripe에 고객 과금 시작을 미룹니다. `trialDays`는 Stripe 가격에 설정된 기본 트라이얼 기간을 덮어씁니다.

> [!WARNING]  
> 트라이얼 종료 전에 구독을 취소하지 않으면 종료 시점에 자동 과금되니 사용자에게 안내하세요.

`trialUntil` 메서드는 `DateTime` 객체를 받아 직접 종료일을 지정합니다:

```
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->addDays(10))
    ->create($paymentMethod);
```

트라이얼 여부 확인은 사용자 인스턴스 또는 구독 인스턴스의 `onTrial` 메서드로 할 수 있습니다:

```
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

즉시 트라이얼 종료는 `endTrial` 메서드:

```
$user->subscription('default')->endTrial();
```

트라이얼 만료 여부 확인은 `hasExpiredTrial`를 사용합니다:

```
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 트라이얼 기간 정의하기

트라이얼 기간을 Stripe 대시보드에서 설정하거나 Cashier에서 명시적으로 지정할 수 있습니다. Stripe 대시보드에서 설정하면, 새로운 구독은 과거 구독이 있더라도 기본적으로 트라이얼이 적용됩니다. 명시적으로 트라이얼 없이 하려면 `skipTrial()`을 호출하세요.

<a name="without-payment-method-up-front"></a>
### 결제수단 없이 트라이얼 제공

트라이얼을 제공하되 결제수단은 초기 수집하지 않으려면, 사용자 테이블에 `trial_ends_at` 컬럼에 종료일을 직접 설정하세요. 일반적으로 회원가입 시 설정합니다:

```
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]  
> `trial_ends_at` 속성에 [date cast](/docs/11.x/eloquent-mutators#date-casting)를 추가해야 합니다.

이러한 트라이얼을 "Generic trial"이라 하며, 실제 구독에 붙어 있지 않아도 됩니다. billable 모델 인스턴스의 `onTrial` 메서드는 현재 시간이 `trial_ends_at` 이전이면 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 사용자 트라이얼 기간 내...
}
```

트라이얼 기간 내에 구독이 생성되면 평소처럼 `newSubscription`을 호출해 구독 시작:

```
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

트라이얼 종료일 조회는 `trialEndsAt` 메서드로 하며, 구독 타입 인자를 선택적으로 넘길 수 있습니다:

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

"Generic trial" 여부는 `onGenericTrial` 메서드로 확인 가능:

```
if ($user->onGenericTrial()) {
    // "Generic" 트라이얼 기간 내...
}
```

<a name="extending-trials"></a>
### 트라이얼 기간 연장하기

`extendTrial` 메서드로 구독 생성 후 트라이얼을 연장할 수 있습니다. 트라이얼 만료 후 과금 중인 고객도 연장할 수 있으며, 이전 트라이얼 기간은 다음 청구서에서 공제됩니다:

```
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 지금부터 7일 후에 트라이얼 종료...
$subscription->extendTrial(
    now()->addDays(7)
);

// 기존 종료일에서 5일 더 연장...
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe 웹훅 처리

> [!NOTE]  
> Stripe CLI를 사용하면 로컬 개발 중 웹훅 테스트가 편리합니다.

Stripe는 여러 이벤트를 웹훅으로 앱에 알릴 수 있습니다. Cashier 서비스 프로바이더가 기본으로 Cashier 웹훅 컨트롤러 경로를 등록합니다. 이 컨트롤러는 모든 웹훅 요청을 처리합니다.

기본적으로 구독 취소, 고객 변경, 결제 수단 변경 등 주요 이벤트 처리가 자동으로 이뤄집니다. 필요하다면 컨트롤러를 확장해 추가 Stripe 웹훅 이벤트를 처리할 수 있습니다.

웹훅 URL을 Stripe 대시보드에 설정하세요. 기본 경로는 `/stripe/webhook`입니다. 활성화해야 할 웹훅 이벤트는 다음과 같습니다:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

편의를 위해 Cashier는 `cashier:webhook` Artisan 명령어를 제공합니다. 이 명령은 Cashier가 필요한 모든 이벤트를 구독하는 웹훅을 Stripe에 생성합니다:

```shell
php artisan cashier:webhook
```

기본 생성 URL은 `APP_URL` 환경 변수와 `cashier.webhook` 라우트에 기반합니다. 다양한 옵션도 제공:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
php artisan cashier:webhook --api-version="2019-12-03"
php artisan cashier:webhook --disabled
```

> [!WARNING]  
> Stripe 웹훅요청을 Cashier의 [서명 검증](#verifying-webhook-signatures) 미들웨어로 반드시 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호 제외

Stripe 웹훅은 Laravel CSRF 보호를 우회해야 합니다. `bootstrap/app.php`에서 다음과 같이 `stripe/*` 경로를 CSRF 검증 예외로 등록하세요:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의하기

Cashier는 기본 웹훅 이외 이벤트를 처리하도록 두 가지 이벤트를 발행합니다:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

모두 Stripe 웹훅 원본 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` 를 처리하는 리스너는 다음과 같습니다:

```
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
            // 이벤트 처리 코드...
        }
    }
}
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅 보안을 위해 [Stripe 웹훅 서명](https://stripe.com/docs/webhooks/signatures) 검증을 Cashier가 자동 Middleware로 제공합니다.

서명 검증을 활성화하려면 `.env`에 `STRIPE_WEBHOOK_SECRET`을 설정하세요. 이 값은 Stripe 대시보드에서 확인 가능합니다.

<a name="single-charges"></a>
## 단일 결제

<a name="simple-charge"></a>
### 간단 결제

일회성 결제는 청구 가능한 모델 인스턴스의 `charge` 메서드를 사용하세요. 두 번째 인자로 결제 수단 식별자를 넘겨야 합니다:

```
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

세 번째 인자에 Stripe 결제 생성 옵션을 배열로 넘길 수 있습니다:

```
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

사용자 없이 결제하려면 billable 모델 인스턴스를 새로 만들어 호출하세요:

```
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

실패 시 예외가 발생하며, 성공 시 `Laravel\Cashier\Payment` 객체를 반환합니다:

```
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]  
> 금액은 앱 통화 단위에서 최소 분모 단위로 지정해야 하며, USD의 경우 센트 단위입니다.

<a name="charge-with-invoice"></a>
### 청구서 포함 결제

청구서 PDF를 제공해야 할 때는 `invoicePrice` 메서드를 사용해 가격 ID 및 수량으로 청구서를 생성할 수 있습니다:

```
$user->invoicePrice('price_tshirt', 5);
```

기본 결제 수단으로 바로 결제하며, 세 번째 인자는 청구 항목 옵션, 네 번째 인자는 청구서 옵션 배열입니다:

```
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

복수 항목 청구는 `tabPrice`로 여러 항목을 추가하고, `invoice`로 청구서 생성합니다:

```
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

금액만 청구하려면 `invoiceFor` 메서드 사용:

```
$user->invoiceFor('One Time Fee', 500);
```

가격 ID를 미리 정해 관리하는 것을 권장합니다. 대시보드에서 분석하기 편리해집니다.

> [!WARNING]  
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 청구 실패 시 재시도를 수행합니다. 실패 시 즉시 재시도하지 않으려면 Stripe API로 청구서를 별도로 닫아야 합니다.

<a name="creating-payment-intents"></a>
### 결제 의도 생성

청구 가능한 모델의 `pay` 메서드로 Stripe 결제 의도(Payment Intent)를 생성할 수 있습니다. 반환값은 `Laravel\Cashier\Payment` 인스턴스입니다:

```
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

클라이언트에 `client_secret`를 전달해 브라우저에서 결제를 완료하게 합니다. Stripe 결제 의도 관련 자세한 가이드는 [Stripe 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

허용할 결제 수단을 제한하려면 `payWith` 메서드에 허용 결제 수단 배열을 넘기세요:

```
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->payWith(
        $request->get('amount'), ['card', 'bancontact']
    );

    return $payment->client_secret;
});
```

> [!WARNING]  
> 금액은 앱 통화 최소 단위로 지정하세요.

<a name="refunding-charges"></a>
### 결제 환불

Stripe 결제 환불은 `refund` 메서드로 처리하며, 첫 번째 인자로 결제 의도 ID를 넘깁니다:

```
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 청구서(Invoices)

<a name="retrieving-invoices"></a>
### 청구서 조회

`invoices` 메서드로 청구서 배열을 쉽게 가져오며, `Laravel\Cashier\Invoice` 객체 컬렉션을 반환합니다:

```
$invoices = $user->invoices();
```

진행 중인 청구서도 포함하려면 `invoicesIncludingPending` 사용:

```
$invoices = $user->invoicesIncludingPending();
```

특정 청구서를 조회하려면 `findInvoice`:

```
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 청구서 정보 표시

청구서 목록을 표로 나열하며, 다운로드 링크를 제공하는 예:

```
<table>
    @foreach ($invoices as $invoice)
        <tr>
            <td>{{ $invoice->date()->toFormattedDateString() }}</td>
            <td>{{ $invoice->total() }}</td>
            <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
        </tr>
    @endforeach
</table>
```

<a name="upcoming-invoices"></a>
### 예정된 청구서

고객의 예정 청구서는 `upcomingInvoice` 메서드로 조회 가능:

```
$invoice = $user->upcomingInvoice();
```

다중 구독이 있으면 특정 구독에 대해 조회도 가능합니다:

```
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 청구서 미리보기

가격 변경 시 예상 청구서를 미리 보려면 `previewInvoice` 메서드를 호출하세요:

```
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

여러 가격을 넘겨 미리볼 수도 있습니다:

```
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 청구서 PDF 생성

청구서 PDF 생성을 위해 Dompdf 라이브러리 설치가 필요합니다:

```shell
composer require dompdf/dompdf
```

라우트 또는 컨트롤러에서 `downloadInvoice` 메서드를 호출하면 HTTP 응답으로 PDF 다운로드를 제공합니다:

```
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

`downloadInvoice` 두 번째 인자로 공급업체, 제품명, 주소 등 회사 정보를 커스터마이징할 수 있습니다:

```
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

세 번째 인자로 파일명을 지정할 수도 있으며 `.pdf`가 자동 붙습니다:

```
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 청구서 렌더러

Cashier는 기본 Dompdf 이외에도 자신만의 렌더러를 구현해 사용할 수 있습니다. `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하세요:

```
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * 청구서를 렌더링해 PDF 바이트 반환
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

구현 후 `config/cashier.php` 내 `cashier.invoices.renderer` 값을 클래스명으로 변경하세요.

<a name="checkout"></a>
## Checkout

Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)을 지원합니다. Stripe Checkout은 직접 결제 페이지를 만들 필요 없이 Stripe가 미리 만들어준 호스팅 페이지를 제공합니다.

아래는 Cashier로 Stripe Checkout 사용법 예시입니다. Stripe 공식 Checkout 문서도 참조하세요: https://stripe.com/docs/payments/checkout

<a name="product-checkouts"></a>
### 상품 Checkout

Stripe 대시보드에서 만든 상품에 대해 청구 가능한 모델의 `checkout` 메서드로 Checkout 세션을 만들 수 있습니다. 기본적으로 Stripe 가격 ID를 전달해야 합니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

수량을 지정할 수도 있습니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

고객은 Checkout 페이지로 이동하며, 기본 성공/취소 URL은 `home`이지만 옵션으로 변경할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

성공 URL에서 `{CHECKOUT_SESSION_ID}`를 쿼리 매개변수로 포함하면 Stripe가 체크아웃 세션 ID로 자동 치환합니다:

```
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
#### 프로모션 코드 지원

Stripe Checkout 기본 세션은 사용자 적용 가능한 프로모션 코드를 지원하지 않습니다. `allowPromotionCodes` 메서드를 호출해 활성화할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 단일 결제 Checkout

Stripe 대시보드에 미리 생성하지 않은 임의 금액 단품 결제를 하려면 `checkoutCharge`를 사용합니다. 청구 금액, 상품명, 수량을 넘깁니다. 접속 시 Checkout 페이지로 리디렉션됩니다:

```
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]  
> `checkoutCharge`는 Stripe에 상품과 가격을 자동 생성하므로, 미리 상품을 만들어 두고 `checkout` 메서드를 사용하는 것을 권장합니다.

<a name="subscription-checkouts"></a>
### 구독 Checkout

> [!WARNING]  
> 구독용 Stripe Checkout 활용 시 반드시 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다.

Cashier 구독 빌더 후 `checkout` 메서드로 구독 시작 Checkout 세션을 만듭니다:

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

상품 Checkout과 마찬가지로 성공/취소 URL을 제공합니다:

```
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

프로모션 코드도 활성화할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!WARNING]  
> Stripe Checkout은 구독 시작 시 모든 청구 옵션을 지원하지 않습니다. `anchorBillingCycleOn`, 정산 설정, 결제 동작 설정 등은 영향을 주지 않으므로 Stripe Checkout 세션 API 문서를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout과 트라이얼 기간

Stripe Checkout 구독 시 트라이얼을 설정할 수 있으나 최소 48시간 이상의 기간이어야 Stripe에서 지원합니다:

```
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독과 웹훅

결제 완료 후 고객 앱 복귀 시점에 구독이 아직 활성화되지 않았을 수 있으므로, 구독 상태가 대기 중임을 알려주는 메시지 표시가 필요합니다. Stripe와 Cashier가 웹훅을 통해 상태를 업데이트합니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집

Checkout 세션에서 고객 세금 ID 수집을 활성화하려면 `collectTaxIds` 메서드를 호출하세요:

```
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

이 옵션을 켜면 고객이 기업 구매자인지 확인하는 체크박스가 나타나며, 세금 ID 번호를 입력할 수 있습니다.

> [!WARNING]  
> 앱에서 이미 [자동 세금 계산](#tax-configuration)을 설정한 경우, 이 옵션 호출은 불필요합니다.

<a name="guest-checkouts"></a>
### 비회원(Guest) Checkout

계정이 없는 비회원 대상 Checkout 세션은 `Checkout::guest` 메서드로 시작합니다:

```
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()->create('price_tshirt', [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

기존 `CheckoutBuilder` 메서드들도 체이닝 가능한데, 예를 들어 프로모션 코드 적용까지 가능합니다:

```
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

비회원 Checkout 완료 시 Stripe가 `checkout.session.completed` 웹훅을 보내므로 반드시 Stripe 대시보드에서 활성화하고 Cashier로 처리하세요.

웹훅 페이로드는 [checkout 객체](https://stripe.com/docs/api/checkout/sessions/object)이므로 이 데이터를 참고해 주문 처리를 수행합니다.

<a name="handling-failed-payments"></a>
## 결제 실패 처리

구독이나 단일 결제 실패 시 `Laravel\Cashier\Exceptions\IncompletePayment` 예외가 발생합니다. 이 예외를 잡아 처리하는 방법은 두 가지입니다.

우선 Cashier가 제공하는 전용 결제 확인 페이지(Arisan 라우트 등록 포함)로 고객을 유도할 수 있습니다. 예외 발생 시 다음과 같이 리다이렉트하세요:

```
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

결제 확인 페이지에서 고객은 카드 정보를 다시 입력하고 Stripe에서 요구하는 추가 인증(예: 3D Secure)을 수행할 수 있습니다. 완료 후 지정된 URL로 리디렉션되고, `message` 및 `success` 쿼리 파라미터가 전달됩니다.

현재 이 페이지는 다음 결제 수단 타입을 지원합니다:

- 신용카드
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

대신 Stripe 대시보드에서 자동 청구 이메일을 활성화하고, 고객이 이메일 지침을 직접 따라 결제하도록 할 수도 있습니다. 다만 `IncompletePayment` 예외 발생 시 사용자에게 이메일 확인 알림을 해야 합니다.

예외는 `charge`, `invoiceFor`, `invoice` 등의 메서드나 구독 빌더 및 모델의 `create`, `incrementAndInvoice`, `swapAndInvoice` 등에서 던질 수 있습니다.

기존 구독에 미완료 결제가 있는지도 다음과 같이 확인 가능합니다:

```
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

예외의 `payment` 프로퍼티를 확인해 상세 상태를 알 수 있습니다:

```
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 의도 상태 확인...
    $exception->payment->status;

    // 조건 체크...
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="confirming-payments"></a>
### 결제 확인

일부 결제 수단은 결제 확인 시 추가 정보를 요구합니다. 예를 들어 SEPA 결제수단은 청구 프로세스 중 "mandate" 데이터가 필요합니다. `withPaymentConfirmationOptions` 메서드로 Cashier에 전달할 수 있습니다:

```
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

Stripe API 결제 확인 파라미터는 [Stripe 문서](https://stripe.com/docs/api/payment_intents/confirm)를 참고하세요.

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증 (Strong Customer Authentication, SCA)

유럽 사업자는 2019년 9월부터 시행된 유럽연합 PSD2와 SCA 규정에 따른 고객 인증 요건을 따라야 합니다. Stripe와 Cashier는 이를 지원하는 기능을 제공합니다.

> [!WARNING]  
> 시작 전 Stripe의 [PSD2 및 SCA 안내](https://stripe.com/guides/strong-customer-authentication)와 [새 SCA API 문서](https://stripe.com/docs/strong-customer-authentication)를 반드시 숙지하세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 인증이 필요한 결제

SCA 규정으로 추가 결제 인증이 필요한 경우, Cashier는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 던져 이를 알려줍니다. 상세한 예외 처리법은 [결제 실패 처리](#handling-failed-payments)를 참고하세요.

Stripe 또는 Cashier의 결제 확인 화면은 은행이나 카드 발급사 별 프로세스에 맞춰 다르게 나타날 수 있으며, 카드 재인증, 임시 소액 청구, 디바이스 인증 등 다양한 인증 절차가 포함될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체 상태

추가 인증이 필요한 결제는 구독의 `stripe_status` 컬럼이 `incomplete` 또는 `past_due`로 남으며, 인증 완료 후 Stripe 웹훅으로 앱에 알림이 오면 자동으로 구독이 활성화됩니다.

이 두 상태에 관한 자세한 내용은 [추가 문서](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>
### 오프 세션 결제 알림

SCA 규정상 고객에게 간혹 결제 인증이 필요함을 알리는 기능도 포함되어 있습니다. 제대로 활성화하려면 `.env`에 알림 클래스를 지정하세요 (기본은 미활성):

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

올바른 웹훅 설정 및 `invoice.payment_action_required` 이벤트 활성화도 필요합니다. 모델은 Laravel 알림 기능 `Illuminate\Notifications\Notifiable` 트레이트를 포함해야 합니다.

> [!WARNING]  
> 고객이 수동 결제를 해도 이 알림이 전송됩니다. 수동 결제 후 재확인 페이지 방문 시 "결제 성공" 메시지를 받을 뿐 중복 결제는 방지됩니다.

<a name="stripe-sdk"></a>
## Stripe SDK

Cashier 객체는 Stripe SDK 객체를 감싸므로 직접 Stripe 객체에 접근할 수 있습니다. 예:

```
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

`updateStripeSubscription` 메서드로 Stripe 구독을 직접 업데이트할 수도 있습니다:

```
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Cashier::stripe()` 메서드로 `Stripe\StripeClient` 인스턴스에 접근할 수 있으며, 예를 들어 가격 목록을 조회할 수 있습니다:

```
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트

Cashier를 사용하는 애플리케이션 테스트 시 Stripe API 요청을 모킹할 수도 있지만, Cashier 동작을 재구현해야 하므로 권장하지 않습니다. 실제 Stripe API를 사용하는 편이 느리지만 더 신뢰성 높은 테스트가 가능합니다.

Cashier 자체 테스트 커버리지가 뛰어나므로, 애플리케이션의 구독 및 결제 플로우에 집중해 테스트하면 됩니다.

테스트 시작 전 `phpunit.xml`에 테스트용 Stripe 비밀 키를 추가하세요:

```
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

이제 테스트 시 Cashier가 Stripe 테스트 환경으로 API 요청을 보냅니다. 테스트용 Stripe 계정에 테스트용 구독/가격을 미리 채워두는 것을 추천합니다.

> [!NOTE]  
> 카드 승인 거부, 실패 등 다양한 시나리오 테스트를 위해 Stripe가 제공하는 [테스트 카드 번호 및 토큰](https://stripe.com/docs/testing) 목록을 활용하세요.