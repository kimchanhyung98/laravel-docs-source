# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [빌러블 모델](#billable-model)
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
    - [고객 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
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
    - [여러 상품 구독](#subscriptions-with-multiple-products)
    - [복수 구독](#multiple-subscriptions)
    - [미터링 빌링](#metered-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 앵커 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 수단 선수집 체험](#with-payment-method-up-front)
    - [결제 수단 없이 체험](#without-payment-method-up-front)
    - [체험 기간 연장하기](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [일회성 결제](#single-charges)
    - [간단 결제](#simple-charge)
    - [청구서와 함께 결제](#charge-with-invoice)
    - [결제 인텐트 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [체크아웃](#checkout)
    - [상품 체크아웃](#product-checkouts)
    - [일회성 결제 체크아웃](#single-charge-checkouts)
    - [구독 체크아웃](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 체크아웃](#guest-checkouts)
- [청구서](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [예정 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [PDF 청구서 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증 (SCA)](#strong-customer-authentication)
    - [추가 결제 승인 필요](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com) 구독 결제 서비스를 위한 표현력이 풍부하고 간결한 인터페이스를 제공합니다. 반복적이고 귀찮은 구독 결제 코드를 거의 모두 처리해 줍니다. 기본적인 구독 관리뿐만 아니라 쿠폰 처리, 구독 전환, 구독 "수량" 관리, 취소 유예 기간 처리, 심지어 청구서 PDF 생성도 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

새 버전의 Cashier로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

> [!WARNING]  
> 변경으로 인한 오류를 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`를 사용합니다. 새로운 Stripe 기능과 개선사항을 활용하기 위해 마이너 릴리즈마다 Stripe API 버전이 갱신됩니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

설치 후, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션을 게시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그다음 데이터베이스 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하고, 고객의 구독 정보를 저장할 새로운 `subscriptions` 테이블과 여러 가격을 가진 구독을 위한 `subscription_items` 테이블을 생성합니다.

필요하다면 `vendor:publish` Artisan 명령어로 Cashier의 설정 파일도 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 모든 Stripe 이벤트를 올바르게 처리하도록 [Cashier 웹훅 설정](#handling-stripe-webhooks)을 반드시 수행하세요.

> [!WARNING]  
> Stripe는 식별자를 저장하는 모든 컬럼을 대소문자를 구분하도록 권장합니다. MySQL에서는 `stripe_id` 컬럼의 콜레이션을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 빌러블 모델 (Billable Model)

Cashier를 사용하기 전에 빌러블 모델 정의에 `Billable` 트레잇을 추가하세요. 보통 이는 `App\Models\User` 모델입니다. 이 트레잇은 구독 생성, 쿠폰 적용, 결제 수단 업데이트 등 흔히 사용하는 결제 작업을 수행할 수 있는 여러 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 Laravel 기본 사용자 모델인 `App\Models\User`를 빌러블 모델로 가정합니다. 만약 이를 변경하고 싶다면, `AppServiceProvider` 클래스의 `boot` 메서드에서 `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다:

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
> Laravel 기본 `App\Models\User` 모델이 아닌 모델을 사용하는 경우, Cashier 마이그레이션을 게시하고(설치 참고) 해당 모델의 테이블 이름에 맞게 변경해야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

다음으로, 애플리케이션의 `.env` 파일에 Stripe API 키를 설정하세요. Stripe 컨트롤 패널에서 API 키를 얻을 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]  
> `STRIPE_WEBHOOK_SECRET` 환경 변수를 반드시 `.env`에 정의해야 합니다. 이 변수는 들어오는 웹훅이 실제 Stripe에서 보내진 것인지를 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 설정해 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

Cashier 통화 설정과 함께 청구서에 표시되는 금액의 포맷을 위해 로케일도 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]  
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 활용하면 Stripe가 생성하는 모든 청구서에 대해 자동으로 세금을 계산할 수 있습니다. 자동 세금 계산을 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

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

세금 계산을 활성화하면 새로 생성되는 구독과 일회성 청구서에 자동 세금이 적용됩니다.

이 기능이 제대로 작동하려면, 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe에 동기화되어 있어야 합니다. 이를 위해 Cashier가 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID](#tax-ids) 관련 메서드를 활용하세요.

> [!WARNING]  
> [일회성 결제](#single-charges)나 [일회성 결제 체크아웃](#single-charge-checkouts)에는 세금이 자동 계산되지 않습니다.

<a name="logging"></a>
### 로깅 (Logging)

Cashier는 치명적인 Stripe 오류가 발생했을 때 사용할 로그 채널을 지정할 수 있습니다. `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 설정하여 로그 채널을 지정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 중 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

내부에서 Cashier가 사용하는 모델을 확장해서 자신의 모델을 정의할 수 있습니다. 예를 들어, 구독 모델을 확장하려면 다음과 같이 작성합니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에게 커스텀 모델을 사용하도록 지시할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 커스텀 모델을 알립니다:

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
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격을 가진 상품을 정의해야 하며, [Cashier 웹훅 설정](#handling-stripe-webhooks)도 완료해야 합니다.

애플리케이션에서 상품과 구독 결제를 제공하는 것은 복잡할 수 있습니다. 그러나 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 사용하면 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

비반복성 일회성 상품에 대해 결제하려면, 고객을 Stripe Checkout으로 리디렉션해 결제 상세 정보를 입력하고 구매를 확정하도록 합니다. 결제가 완료되면 고객은 애플리케이션 내에서 지정한 성공 URL로 리디렉션됩니다:

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

Route::view('checkout.success')->name('checkout-success');
Route::view('checkout.cancel')->name('checkout-cancel');
```

위 예제에서 `checkout` 메서드를 사용해 해당 가격 식별자(`price_deluxe_album`)에 대해 Stripe Checkout으로 고객을 리디렉션합니다. Stripe에서 "가격"(price)은 [특정 상품에 대한 정의된 가격](https://stripe.com/docs/products-prices/how-products-and-prices-work)을 의미합니다.

필요하다면 `checkout` 메서드는 Stripe에 고객을 자동 생성하고, 생성된 Stripe 고객 레코드를 애플리케이션 데이터베이스의 사용자와 연결합니다. 체크아웃 완료 후 고객은 전용 성공 또는 취소 페이지로 이동하며 해당 페이지에서 알림 메시지를 표시할 수 있습니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타 데이터 제공하기

제품 판매 시, 애플리케이션에서 `Cart`와 `Order` 모델로 완료된 주문 및 상품을 관리하는 경우가 많습니다. Stripe Checkout으로 리디렉션할 때 기존 주문 식별자를 제공하여, 체크아웃 후 고객이 돌아왔을 때 주문과 결제가 연결되도록 할 수 있습니다.

예를 들어, 사용자가 체크아웃을 시작할 때 보류 중인 `Order`를 생성한다고 가정해 보겠습니다. 아래 예제는 Cashier가 제공하는 모델이 아니라, 애플리케이션 상황에 따라 직접 구현해야 하는 개념입니다:

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

위 코드를 보면, 체크아웃 시작 시 `Cart`/`Order`에 연관된 Stripe 가격 ID 배열(`price_ids`)을 `checkout` 메서드에 전달합니다. 또한 주문 ID도 `metadata` 배열에 포함해 Stripe Checkout 세션에 넘깁니다. 주문 완료 후 반환되는 성공 URL에는 `{CHECKOUT_SESSION_ID}` 자리 표시자가 포함되어 있는데, Stripe가 실제 체크아웃 세션 ID로 자동 바꿉니다.

다음으로, 체크아웃 성공 라우트를 구현합니다. 사용자가 결제를 완료하고 돌아오는 이 라우트에서, Stripe Checkout 세션 ID로 세션 객체를 조회하고 메타 데이터를 받아 주문 상태를 갱신할 수 있습니다:

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

더 자세한 Checkout 세션 객체 정보는 Stripe의 [Checkout 세션 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매 (Selling Subscriptions)

> [!NOTE]  
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에 고정 가격이 정의된 상품이 있어야 하며, [Cashier 웹훅 설정](#handling-stripe-webhooks)도 완료해야 합니다.

애플리케이션에서 상품과 구독 결제를 제공하는 것이 복잡할 수 있지만, Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout) 덕분에 간단하게 강력한 결제 통합을 구현할 수 있습니다.

간단한 구독 서비스 예로, 기본 월간(`price_basic_monthly`) 플랜과 연간(`price_basic_yearly`) 플랜이 있다고 생각해 보겠습니다. 이 두 가격은 Stripe 대시보드 내 "Basic" 상품(`pro_basic`)에 묶여 있을 수 있습니다. 또 Expert 요금제는 `pro_expert`로 구분할 수도 있겠죠.

먼저, 고객이 구독 옵션을 선택하면, 라우트에서 Stripe Checkout 세션을 만드는 예입니다:

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

위 예제처럼 `newSubscription`으로 구독을 만들고 `checkout`을 호출해 고객을 Stripe Checkout으로 리디렉션합니다. 결제 완료 혹은 취소 시 제공된 URL로 리디렉션됩니다. 구독 시작 상태는 [웹훅 설정](#handling-stripe-webhooks)으로 정확히 동기화해야 합니다.

고객 구독 상태는 Cashier `Billable` 트레잇의 `subscribed` 메서드로 간단히 확인할 수 있습니다:

```blade
@if ($user->subscribed())
    <p>구독 중입니다.</p>
@endif
```

특정 상품이나 가격으로 구독 중인지도 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 상품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>Basic 월간 플랜에 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 미들웨어 만들기

필요하다면 미들웨어를 만들어 구독하지 않은 사용자의 라우트 접근을 막을 수 있습니다. 예시 미들웨어 코드는 다음과 같습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * 인수로 들어온 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // 미구독 유저를 청구 페이지로 리디렉션
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

미들웨어 정의 후, 라우트에 할당합니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 청구 플랜을 관리하도록 허용하기

고객이 자신의 구독 플랜을 바꾸고 싶을 때, Stripe의 [고객 청구 포털](https://stripe.com/docs/no-code/customer-portal)을 사용하는 것이 가장 간단합니다. 이 포털은 구독, 결제 수단, 청구서 내역 등을 관리할 수 있는 Stripe 호스팅 UI를 제공합니다.

애플리케이션 내에 청구 페이지 링크를 만들고, 해당 링크에 연결되는 라우트를 다음과 같이 정의하세요:

```blade
<a href="{{ route('billing') }}">
    청구 관리
</a>
```

아래는 Stripe 고객 청구 포털 세션을 생성하고 리디렉션하는 라우트 예제입니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]  
> Cashier 웹훅을 설정하면 Stripe 고객 청구 포털에서 구독을 취소할 때, 관련 웹훅을 받아 앱 내 데이터베이스 구독 상태도 자동으로 업데이트됩니다.

<a name="customers"></a>
## 고객 (Customers)

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

`Cashier::findBillable` 메서드를 사용하면 Stripe ID로 고객을 조회할 수 있습니다. 이 메서드는 빌러블 모델 인스턴스를 반환합니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

가끔 구독을 시작하지 않고 Stripe 고객만 생성하고 싶을 때가 있습니다. `createAsStripeCustomer` 메서드로 가능합니다:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

Stripe 고객 생성 후 나중에 구독을 시작할 수 있습니다. Stripe API가 지원하는 추가 고객 생성 옵션을 배열로 전달할 수도 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

빌러블 모델이 Stripe 고객 객체를 직접 반환하도록 하려면 `asStripeCustomer` 메서드를 사용하세요:

```php
$stripeCustomer = $user->asStripeCustomer();
```

고객이 이미 Stripe에 존재할지 확실하지 않을 경우 `createOrGetStripeCustomer` 메서드를 사용하면, 없으면 생성하고 있으면 조회합니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 업데이트 (Updating Customers)

Stripe 고객 정보를 직접 업데이트 하고 싶다면 `updateStripeCustomer` 메서드를 사용하세요. Stripe API에서 지원하는 업데이트 옵션 배열을 전달할 수 있습니다:

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 (Balances)

Stripe는 고객 잔액을 증가 혹은 감소시킬 수 있습니다. 이 잔액은 이후 청구서에서 상쇄됩니다. 고객 잔액을 포맷된 문자열로 얻으려면 `balance` 메서드를 사용하세요:

```php
$balance = $user->balance();
```

잔액에 크레딧을 추가하려면 `creditBalance` 메서드에 금액과 설명을 전달하세요:

```php
$user->creditBalance(500, '프리미엄 고객 추가 충전.');
```

잔액 차감 시에는 `debitBalance` 메서드를 사용하세요:

```php
$user->debitBalance(300, '불량 사용 패널티.');
```

고객 잔액 거래기록은 `balanceTransactions` 메서드로 조회할 수 있어 고객에게 크레딧/차감 내역을 보여줄 때 유용합니다:

```php
// 모든 거래 내역 조회
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액
    $amount = $transaction->amount(); // 예: $2.31

    // 연관된 청구서가 있을 때 조회
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID (Tax IDs)

Cashier는 고객의 세금 ID 관리를 간소화해 줍니다. `taxIds` 메서드로 고객에게 연결된 모든 세금 ID를 컬렉션 형태로 가져올 수 있습니다:

```php
$taxIds = $user->taxIds();
```

특정 세금 ID는 식별자로 조회할 수 있습니다:

```php
$taxId = $user->findTaxId('txi_belgium');
```

유효한 [세금 ID 타입](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 `createTaxId` 메서드에 넘겨 새로운 세금 ID를 생성할 수 있습니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

이 메서드는 즉시 고객 계정에 VAT ID를 추가하며, Stripe가 비동기적으로 검증합니다. [웹훅 `customer.tax_id.updated` 이벤트](#handling-stripe-webhooks)를 구독해 검증 상태를 확인할 수 있습니다.

세금 ID 삭제는 `deleteTaxId` 메서드로 합니다:

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화 (Syncing Customer Data With Stripe)

애플리케이션에서 사용자 이름, 이메일 등 정보를 수정하면 Stripe 상의 고객 데이터도 동기화해야 합니다. 모델의 `updated` 이벤트 리스너에서 `syncStripeCustomerDetails` 메서드를 호출하는 방법으로 자동화할 수 있습니다:

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * 모델의 "booted" 메서드
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

이렇게 하면 고객 모델 수정 시마다 Stripe 고객 정보도 자동 동기화됩니다. 초기 고객 생성 시에도 자동으로 동기화를 수행합니다.

동기화에 사용할 속성을 변경하고 싶으면 `stripeName`, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 메서드를 오버라이드하세요. 완전 제어가 필요하면 `syncStripeCustomerDetails` 메서드를 직접 오버라이드할 수 있습니다.

예를 들어 이름 컬럼을 커스터마이징하려면:

```php
/**
 * Stripe와 동기화할 고객 이름을 반환
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

<a name="billing-portal"></a>
### 청구 포털 (Billing Portal)

Stripe는 [청구 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공하여 고객이 구독, 결제 수단, 청구 기록을 직접 관리하도록 돕습니다. 라우트 또는 컨트롤러에서 빌러블 모델의 `redirectToBillingPortal` 메서드를 호출해 청구 포털로 리디렉션할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본 리턴 경로는 애플리케이션의 `home` 경로입니다. 리턴 경로를 바꾸려면 URL을 인자로 넘기세요:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

리디렉션 없이 청구 포털 URL 만 필요하면 `billingPortalUrl` 메서드를 사용하세요:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단 (Payment Methods)

<a name="storing-payment-methods"></a>
### 결제 수단 저장 (Storing Payment Methods)

구독 생성이나 단발성 결제를 위해 결제 수단을 저장하고 Stripe의 결제 수단 식별자를 받아야 합니다. 구독과 단발 결제에 사용하는 방식이 다르므로 각각 설명합니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독용 결제 수단

구독에서 고객의 카드 정보를 저장하려면 Stripe의 "Setup Intents" API를 사용해 안전하게 결제 수단을 수집해야 합니다. Cashier의 `createSetupIntent` 메서드로 Setup Intent를 쉽게 생성할 수 있으니, 결제 수단 정보를 입력하는 뷰를 렌더링 할 컨트롤러/라우트에서 호출하세요:

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

Setup Intent의 시크릿 키(`client_secret`)를 입력폼 요소에 붙입니다. 예를 들어:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    결제 수단 업데이트
</button>
```

이후 Stripe.js 라이브러리를 이용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 마운트합니다:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

결제 수단이 올바른지 Stripe에 검증 요청하고, Setup Intent 결과에서 결제 수단 식별자를 취득할 수 있습니다:

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
        // 에러 메시지 표시
    } else {
        // 카드가 성공적으로 검증됨
    }
});
```

Stripe가 검증해 준 `setupIntent.payment_method` 식별자를 Laravel 앱에 전달해 고객에게 결제 수단으로 추가하거나 기본 결제 수단을 업데이트할 수 있습니다. 즉시 구독 생성에 사용할 수도 있습니다.

> [!NOTE]  
> Setup Intents 및 고객 결제 수단 저장에 관한 자세한 내용은 [Stripe 가이드](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>
#### 단발성 결제용 결제 수단

단발성 결제 채널에서는 결제 수단 식별자가 한번만 필요하므로, 기본 결제 수단 저장 및 재사용을 하지 않습니다. Stripe.js로 고객에게 결제 정보를 직접 입력받아야 합니다.

예시 폼:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 -->
<div id="card-element"></div>

<button id="card-button">
    결제 처리
</button>
```

Stripe.js로 Stripe Element를 마운트하는 부분은 구독용과 동일합니다.

카드 검증 후 Stripe의 `createPaymentMethod` 메서드를 사용해 안전하게 결제 수단 식별자를 취득합니다:

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
        // 에러 표시
    } else {
        // 카드 성공 검증 완료
    }
});
```

검증 성공 시 `paymentMethod.id`를 Laravel 앱에 전달해 [단일 결제](#simple-charge)를 진행할 수 있습니다.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회 (Retrieving Payment Methods)

빌러블 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다:

```php
$paymentMethods = $user->paymentMethods();
```

특정 타입만 조회하려면 `type` 인자를 전달하세요:

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

고객의 기본 결제 수단은 `defaultPaymentMethod` 메서드로 조회합니다:

```php
$paymentMethod = $user->defaultPaymentMethod();
```

특정 결제 수단을 `findPaymentMethod` 메서드로 가져올 수도 있습니다:

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 결제 수단 존재 여부 (Payment Method Presence)

기본 결제 수단 유무는 `hasDefaultPaymentMethod` 메서드로 확인할 수 있습니다:

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

최소 하나라도 결제 수단이 있는지는 `hasPaymentMethod` 메서드로 확인합니다:

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

특정 형식 결제 수단 여부는 `type` 인자를 넘겨 확인합니다:

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트 (Updating the Default Payment Method)

`updateDefaultPaymentMethod` 메서드에 결제 수단 식별자를 넘겨 기본 결제 수단 정보를 업데이트할 수 있습니다:

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

Stripe와 기본 결제 수단 동기화는 `updateDefaultPaymentMethodFromStripe` 메서드로 할 수 있습니다:

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]  
> 기본 결제 수단은 청구와 구독 생성시에만 사용 가능하며, Stripe 제한으로 인해 단발성 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가 (Adding Payment Methods)

`addPaymentMethod` 메서드에 결제 수단 식별자를 전달해 새로운 결제 수단을 추가합니다:

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]  
> 결제 수단 식별자를 얻는 방법은 [결제 수단 저장 문서](#storing-payment-methods)를 참고하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제 (Deleting Payment Methods)

삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출해 지울 수 있습니다:

```php
$paymentMethod->delete();
```

빌러블 모델 메서드인 `deletePaymentMethod`는 특정 결제 수단을 삭제합니다:

```php
$user->deletePaymentMethod('pm_visa');
```

`deletePaymentMethods` 메서드는 모든 결제 수단을 삭제합니다:

```php
$user->deletePaymentMethods();
```

특정 타입 결제 수단만 삭제하려면 `type` 인자를 넘기세요:

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]  
> 사용자가 구독 중이면 기본 결제 수단 삭제를 허용하지 마세요.

<a name="subscriptions"></a>
## 구독 (Subscriptions)

구독은 고객의 반복 결제를 설정하는 방법입니다. Cashier는 Stripe 구독을 여러 가격, 수량, 체험 기간 등을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 일반적으로 빌러블 모델 인스턴스(`App\Models\User`)를 가져온 후 `newSubscription` 메서드를 사용합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

첫 번째 인자는 내부 구독 타입으로, 단일 구독일 땐 `default`, `primary` 등으로 지정합니다. 이 값은 사용자에게 노출되지 않고, 공백 없이 변경하면 안 됩니다. 두 번째 인자는 Stripe 가격 ID입니다.

`create` 메서드는 [Stripe 결제 수단 식별자](#storing-payment-methods) 또는 Stripe `PaymentMethod` 객체를 받아 구독을 시작하고 관련 고객 ID, 청구 정보를 DB에 저장합니다.

> [!WARNING]  
> `create` 메서드에 결제 수단 식별자를 직접 넘기면 자동으로 사용자의 저장된 결제 수단으로 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 청구서 이메일로 반복 결제 수금

자동 반복 결제 대신 Stripe가 고객에게 청구서를 이메일로 보내도록 할 수 있습니다. 고객은 이메일 청구서를 받으면 수동으로 결제합니다. 이 경우 구독 생성 시 결제 수단 없이도 됩니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

결제가 완료될 때까지 시간 제한(`days_until_due`)을 설정할 수 있습니다. 기본값은 30일이며, 옵션 배열로 바꿀 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 수량 (Quantities)

구독 생성 시 특정 가격 수량을 지정하려면 `quantity` 메서드를 구독 빌더에 체인하세요:

```php
$user->newSubscription('default', 'price_monthly')
     ->quantity(5)
     ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 옵션

Stripe가 지원하는 추가 고객(`customer`) 또는 구독(`subscription`) 옵션을 `create` 메서드 두 번째, 세 번째 인자로 전달할 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => '추가 정보.'],
]);
```

<a name="coupons"></a>
#### 쿠폰 (Coupons)

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요:

```php
$user->newSubscription('default', 'price_monthly')
     ->withCoupon('code')
     ->create($paymentMethod);
```

Stripe 프로모션 코드를 사용하려면 `withPromotionCode` 메서드를 씁니다:

```php
$user->newSubscription('default', 'price_monthly')
     ->withPromotionCode('promo_code_id')
     ->create($paymentMethod);
```

프로모션 코드 ID는 고객이 보는 코드가 아닌 Stripe가 부여한 API ID여야 합니다. 고객용 코드로 ID를 찾으려면 `findPromotionCode` 메서드를 쓰세요:

```php
// 고객용 코드로 프로모션 코드 찾기
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// 활성 상태인 프로모션 코드 찾기
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

반환 객체는 `Laravel\Cashier\PromotionCode` 인스턴스로, 내부에 Stripe `PromotionCode` 객체가 포함되어 있습니다. 쿠폰은 `coupon` 메서드로 얻습니다:

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

쿠폰이 고정 금액 할인인지 백분율 할인인지 아래와 같이 확인할 수 있습니다:

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 예: 21.5%
} else {
    return $coupon->amountOff(); // 예: $5.99
}
```

현재 고객이나 구독에 적용된 할인도 조회할 수 있습니다:

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

`Laravel\Cashier\Discount` 인스턴스이며, 관련 쿠폰은 `coupon` 메서드로 조회합니다:

```php
$coupon = $subscription->discount()->coupon();
```

새 쿠폰 또는 프로모션 코드를 고객이나 구독에 적용하려면, `applyCoupon` 또는 `applyPromotionCode` 메서드를 사용하세요:

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

단, 동시에 하나의 쿠폰 또는 프로모션 코드만 적용할 수 있습니다.

자세한 내용은 Stripe 문서의 [쿠폰](https://stripe.com/docs/billing/subscriptions/coupons)과 [프로모션 코드](https://stripe.com/docs/billing/subscriptions/coupons/codes)를 참고하세요.

<a name="adding-subscriptions"></a>
#### 구독 추가 (Adding Subscriptions)

기본 결제 수단이 고객에게 이미 있다면, 구독 빌더의 `add` 메서드로 구독을 추가할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 구독 생성

Stripe 대시보드에서도 구독을 생성할 수 있습니다. 이 경우 Cashier가 구독을 동기화하며 기본 구독 타입은 `default`로 지정됩니다. 대시보드 구독 타입 변경은 [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)에서 조절하세요.

다만, 대시보드에서는 하나의 구독 타입만 생성할 수 있습니다. 애플리케이션이 여러 구독 타입을 지원하면 각 타입당 하나의 활성 구독만 생성해야 하며, 두 개 이상 있으면 가장 최근 구독만 활용됩니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

고객이 구독 중인지 다양한 메서드로 간단히 확인할 수 있습니다. `subscribed` 메서드는 활성 구독이거나 체험 기간 내면 `true`를 반환하며, 구독 타입을 첫 매개변수로 받습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```

이 메서드는 [라우트 미들웨어](/docs/10.x/middleware)로 특정 구독 사용자만 접근하게 할 때 유용합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * 인수로 들어온 요청 처리
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 구독 중이 아닌 사용자
            return redirect('billing');
        }

        return $next($request);
    }
}
```

체험 기간 내인지는 `onTrial` 메서드로 확인할 수 있습니다:

```php
if ($user->subscription('default')->onTrial()) {
    // ....
}
```

특정 상품 구독 여부는 `subscribedToProduct`로 검사할 수 있습니다. Stripe에서 상품은 여러 가격을 묶은 개념입니다. 예를 들어 "premium" 상품 구독 여부:

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

배열을 넘겨 여러 상품 중 하나라도 구독 중인지 확인할 수도 있습니다:

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

특정 가격 ID로 구독 중인지 확인은 `subscribedToPrice` 메서드를 씁니다:

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

구독이 체험 기간이 끝났고 실제 반복 결제 중인지 확인은 `recurring` 메서드로 합니다:

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]  
> 같은 구독 타입을 여러 개 가질 경우 `subscription` 메서드는 최신 구독만 반환합니다. 과거 만료 구독은 DB에 보관되지만 반환되지 않습니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 과거에는 구독 중이었으나 이제 취소했는지 확인하려면 `canceled` 메서드를 씁니다:

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

취소는 했지만 유예 기간(`grace period`) 내인지 보려면 `onGracePeriod` 메서드가 유용합니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

예를 들어 3월 5일 취소했지만 종료 예정일이 3월 10일이면, 이 기간 동안은 `subscribed`가 계속 `true`입니다.

취소하고 유예 기간도 지났는지 확인은 `ended` 메서드로 가능합니다:

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료 및 연체 상태

결제 추가 조치가 필요하면 구독은 `incomplete` 상태가 되고, 가격 변경 후 결제 조치가 필요하면 `past_due` 상태가 됩니다. 상태는 `subscriptions` 테이블의 `stripe_status` 컬럼에 저장됩니다. 이 상태에서는 구독이 활성화되지 않습니다.

불완전 결제 여부는 빌러블 모델 혹은 구독 인스턴스의 `hasIncompletePayment` 메서드로 확인 가능합니다:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

불완전 결제 상태면 `latestPayment` 메서드가 반환하는 결제 아이디를 참조해 결제 확인 페이지로 안내하세요:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    결제를 확인해 주세요.
</a>
```

`past_due` 또는 `incomplete` 상태에서도 구독을 활성으로 유지하려면 `keepPastDueSubscriptionsActive`, `keepIncompleteSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register`에서 호출하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 등록
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]  
> `incomplete` 상태인 구독은 결제가 완료될 때까지 변경할 수 없습니다. 이 상태에서 `swap`, `updateQuantity` 메서드는 예외를 던집니다.

<a name="subscription-scopes"></a>
#### 구독 스코프

구독 상태별 쿼리 스코프도 지원되어 쉽게 DB에서 상태별 구독을 조회할 수 있습니다:

```php
// 활성 구독 모두 조회
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자의 취소된 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 스코프 목록:

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
### 가격 변경 (Changing Prices)

구독 중인 고객이 다른 가격으로 바꾸려면 구독 인스턴스의 `swap` 메서드를 호출하며 교체할 Stripe 가격 식별자를 전달하세요:

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

체험 기간이 있으면 유지되고, 구독 수량도 그대로 유지됩니다.

체험 기간을 취소하려면 `skipTrial` 메서드를 체인하세요:

```php
$user->subscription('default')
        ->skipTrial()
        ->swap('price_yearly');
```

즉시 청구서를 발행해 교체하고 싶으면 `swapAndInvoice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 정산 (Prorations)

기본적으로 Stripe는 가격을 바꿀 때 차액 정산을 수행합니다. 정산 없이 가격을 변경하려면 `noProrate` 메서드를 체인하세요:

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

단, `noProrate`를 `swapAndInvoice` 앞에 호출하면 효과가 없습니다. 인보이스가 발행되면 항상 정산 청구됩니다.

자세한 내용은 Stripe의 [프레이션 문서](https://stripe.com/docs/billing/subscriptions/prorations)를 참고하세요.

> [!WARNING]  
> `noProrate`를 `swapAndInvoice` 메서드 호출 전 실행해도 효과가 없습니다. 인보이스가 반드시 발행됩니다.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

예를 들어 프로젝트 관리 앱에서 프로젝트당 월 $10를 청구할 때, `incrementQuantity`와 `decrementQuantity` 메서드로 구독 수량을 조정할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 5만큼 수량 더하기
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 5만큼 수량 빼기
$user->subscription('default')->decrementQuantity(5);
```

특정 수량을 지정하려면 `updateQuantity`를 사용하세요:

```php
$user->subscription('default')->updateQuantity(10);
```

정산 없이 수량을 변경하려면 `noProrate`와 체인합니다:

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

[Stripe 문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 구독 상품 수량

여러 상품 구독이라면 수량 변경 메서드에 두 번째 인자로 특정 가격 ID를 전달하세요:

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 여러 상품 구독 (Subscriptions With Multiple Products)

[여러 상품 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)은 하나 구독에 여러 상품을 연결하는 기능입니다. 예: 기본 월 $10 구독에 추가 상품으로 월 $15 라이브 채팅 추가.

이 정보는 `subscription_items` 테이블에 저장됩니다.

몇 개 가격이든 배열로 정의해 `newSubscription` 두 번째 인자로 넘길 수 있습니다:

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

특정 가격에 수량을 지정하려면 `quantity` 메서드를 체인하며 해당 가격 ID를 두 번째 인자로 전달:

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 가격을 추가하려면 `addPrice` 메서드를 사용하세요:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

즉시 결제하려면 `addPriceAndInvoice` 메서드를 사용합니다:

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

추가 가격에 수량 지정도 가능합니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

가격을 제거하려면 `removePrice` 메서드를 사용:

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]  
> 구독이 하나의 가격만 가질 수 있기 때문에 마지막 가격은 제거할 수 없습니다. 구독 자체를 취소하세요.

<a name="swapping-prices"></a>
#### 가격 교체

하나 가격을 다른 가격으로 바꾸는 것도 가능합니다. 예: 기본 요금제(`price_basic`)와 라이브 채팅(`price_chat`)을 쓰는 고객을 `price_pro` 요금제로 업그레이드하는 경우:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

이 경우 기존 `price_basic` 아이템은 삭제되고, `price_chat` 유지, `price_pro` 새 생성됩니다.

가격별 수량 같은 구독 아이템 설정을 하려면 키-값 배열 형태로 `swap` 메서드에 전달합니다:

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

단일 구독 아이템에서 `swap`도 가능하며, 다른 아이템 메타데이터를 유지할 때 유용합니다:

```php
$user = User::find(1);

$user->subscription('default')
        ->findItemOrFail('price_basic')
        ->swap('price_pro');
```

<a name="proration"></a>
#### 정산

다중 상품 구독에서 추가/제거 시 정산이 기본 적용됩니다. 정산 없이 변경하려면 `noProrate`를 체인하세요:

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량 변경

상품별 수량 변경도 가능합니다:

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]  
> 여러 가격 구독은 `Subscription` 모델의 `stripe_price`와 `quantity` 속성이 `null`입니다. 개별 가격 정보는 `items` 관계에서 꺼내야 합니다.

<a name="subscription-items"></a>
#### 구독 아이템

여러 가격 있는 구독은 여러 구독 아이템을 가집니다(`subscription_items` 테이블). `Subscription` 모델의 `items` 관계로 접근 가능:

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// 단일 아이템의 Stripe 가격 및 수량 조회
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

특정 가격 아이템은 `findItemOrFail`로 조회:

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 복수 구독 (Multiple Subscriptions)

Stripe는 고객이 여러 구독을 가질 수 있게 합니다. 예를 들어 헬스장 구독에서 수영과 웨이트 구독이 다른 가격으로 따로 있을 수 있습니다.

애플리케이션에서 구독 생성 시 타입을 자유롭게 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

후에 연간 구독으로 바꿀 때:

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

구독 취소도 가능합니다:

```php
$user->subscription('swimming')->cancel();
```

<a name="metered-billing"></a>
### 미터링 빌링 (Metered Billing)

[미터링 빌링](https://stripe.com/docs/billing/subscriptions/metered-billing)은 사용량 기반 청구를 가능하게 합니다. 예: 월별 문자, 이메일 송신 수에 따라 요금이 청구됩니다.

먼저 Stripe 대시보드에서 미터링 가격이 있는 상품을 만들고, `meteredPrice` 메서드로 구독에 미터링 가격 추가:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

[Stripe Checkout](#checkout)으로도 미터링 구독 시작 가능:

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

고객이 서비스를 사용할 때 사용량을 Stripe에 보고해야 정확한 청구가 이뤄집니다. 사용량 증가 시 `reportUsage`를 호출:

```php
$user = User::find(1);

$user->subscription('default')->reportUsage();
```

기본적으로 1 단위 추가이며 원하는 양을 지정할 수도 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->reportUsage(15);
```

복수 가격 구독 시 보고할 가격 ID와 양을 지정하세요:

```php
$user = User::find(1);

$user->subscription('default')->reportUsageFor('price_metered', 15);
```

과거 사용량을 수정하려면 두 번째 인자로 타임스탬프를 전달:

```php
$user = User::find(1);

$user->subscription('default')->reportUsage(5, $timestamp);
```

<a name="retrieving-usage-records"></a>
#### 사용량 기록 조회

과거 사용량은 `usageRecords` 메서드로 받아올 수 있습니다:

```php
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecords();
```

복수 가격 구독은 `usageRecordsFor` 메서드로 가격 지정 가능:

```php
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecordsFor('price_metered');
```

사용량 기록을 반복문으로 출력 가능:

```blade
@foreach ($usageRecords as $usageRecord)
    - 기간 시작: {{ $usageRecord['period']['start'] }}
    - 기간 종료: {{ $usageRecord['period']['end'] }}
    - 총 사용량: {{ $usageRecord['total_usage'] }}
@endforeach
```

Stripe 문서의 [사용량 API 참조](https://stripe.com/docs/api/usage_records/subscription_item_summary_list)도 참고하세요.

<a name="subscription-taxes"></a>
### 구독 세금 (Subscription Taxes)

> [!WARNING]  
> 세금율을 직접 계산하지 않고 [Stripe Tax 자동 계산](#tax-configuration)을 사용하는 걸 권장합니다.

사용자별 적용할 세율을 빌러블 모델에 `taxRates` 메서드로 Stripe 세율 ID 배열을 반환해 지정합니다. 세율은 [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 정의합니다:

```php
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

복수 상품 구독 시, 각 가격별 세율을 사용자에게 적용하도록 `priceTaxRates` 메서드를 정의할 수 있습니다:

```php
/**
 * 고객 구독에 적용할 가격별 세율 배열 반환
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
> `taxRates` 메서드는 구독 청구에만 적용되며, 일회성 결제 시에는 수동으로 세율을 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화

`taxRates`가 바뀌어도 기존 구독 세금 설정은 유지됩니다. 새 세율로 변경하려면 구독 인스턴스의 `syncTaxRates` 메서드를 호출하세요:

```php
$user->subscription('default')->syncTaxRates();
```

이 메서드는 다중 상품 구독 아이템 세율도 동기화합니다. 다중 상품 구독 시 빌러블 모델에서 `priceTaxRates` 역시 구현하세요.

<a name="tax-exemption"></a>
#### 세금 면제

`isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드로 고객의 세금 면제 여부를 조회할 수 있습니다. 내부에서 Stripe API를 호출합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]  
> 이 메서드들은 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있지만, 청구서 작성 시점 기준으로 세금 면제 상태를 확인합니다.

<a name="subscription-anchor-date"></a>
### 구독 앵커 날짜 (Subscription Anchor Date)

기본적으로 청구 주기 시작일은 구독 생성일 또는 체험 종료일입니다. 변경하려면 `anchorBillingCycleOn` 메서드에 원하는 날짜를 넘기세요:

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

청구 주기 관리에 관한 자세한 내용은 [Stripe 청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소 (Cancelling Subscriptions)

구독 취소는 구독 인스턴스의 `cancel` 메서드를 호출합니다:

```php
$user->subscription('default')->cancel();
```

취소 시 `subscriptions` 테이블의 `ends_at` 컬럼에 취소 종료 시점이 기록되어, `subscribed` 메서드가 해당 일시까지 `true`를 반환합니다. 즉, 유저는 구독 종료일까지 계속 서비스를 사용할 수 있습니다.

유예 기간 중인지 확인하려면 다음과 같이 합니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

즉시 종료하려면 `cancelNow` 메서드를 사용하세요:

```php
$user->subscription('default')->cancelNow();
```

즉시 종료하면서 청구서 전송이 필요한 경우 `cancelNowAndInvoice`:

```php
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점에 취소 예약도 가능합니다:

```php
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

사용자 모델 삭제 전에 구독을 반드시 취소하세요:

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### 구독 재개 (Resuming Subscriptions)

취소 후 유예 기간 내면 `resume` 메서드로 구독을 다시 활성화할 수 있습니다:

```php
$user->subscription('default')->resume();
```

재개 시 기존 청구 주기에 맞춰 청구되며 즉시 과금되지 않습니다.

<a name="subscription-trials"></a>
## 구독 체험 기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 선수집 체험 (With Payment Method Up Front)

체험 기간 동안 결제 수단을 미리 수집하려면 구독 생성 시 `trialDays` 메서드를 사용하세요:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
                ->trialDays(10)
                ->create($request->paymentMethodId);

    // ...
});
```

이렇게 하면 구독 기록과 Stripe에 체험 종료일이 설정되고, 종료 시 자동 결제가 시작됩니다. `trialDays` 호출 시 Stripe 대시보드 설정 체험 기간은 무시됩니다.

> [!WARNING]  
> 체험 종료일까지 구독이 취소되지 않으면 체험 종료 시점에 요금이 청구됩니다. 사용자에게 체험 종료일을 반드시 알려 주세요.

체험 종료 시점을 `DateTime` 인스턴스로 명시하려면 `trialUntil` 메서드를 사용합니다:

```php
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
            ->trialUntil(Carbon::now()->addDays(10))
            ->create($paymentMethod);
```

체험 중인지 확인하려면 `onTrial` 메서드를 사용합니다 (사용자 혹은 구독 인스턴스 모두 가능):

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

즉시 체험 종료는 `endTrial` 메서드를 호출:

```php
$user->subscription('default')->endTrial();
```

체험 기간 만료 여부 확인은 `hasExpiredTrial` 메서드를 씁니다:

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 체험일 설정

Stripe 대시보드에 체험 기간을 설정하거나 직접 Cashier에서 전달할 수 있습니다. Stripe 대시보드 설정 체험 기간이 기본이며, 구독을 새로 시작할 때마다 체험이 적용됩니다. 체험 없이 바로 시작하려면 `skipTrial()` 메서드를 호출해야 합니다.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 체험 (Without Payment Method Up Front)

체험 기간 동안 결제 수단 없이도 체험을 제공하려면, 사용자가 생성될 때 `trial_ends_at` 속성을 설정하세요:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]  
> 빌러블 모델에서 `trial_ends_at` 속성에 [날짜 캐스팅](/docs/10.x/eloquent-mutators#date-casting)을 추가해야 합니다.

이런 체험을 "일반 체험"이라 부르며, `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 내 같으면 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // 체험 중
}
```

이후 구독 생성 시 일반 방식대로 `newSubscription`을 호출하면 됩니다:

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

체험 종료일을 조회할 땐 `trialEndsAt` 메서드를 사용하세요. 구독 타입을 인자로 전달할 수도 있습니다:

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

특히 일반 체험인지 알고 싶으면 `onGenericTrial` 메서드를 활용:

```php
if ($user->onGenericTrial()) {
    // 일반 체험 중
}
```

<a name="extending-trials"></a>
### 체험 기간 연장하기 (Extending Trials)

`extendTrial` 메서드로 구독 생성 후 체험 기간을 연장할 수 있습니다. 이미 체험 기간이 끝나 결제가 시작된 구독도 연장이 가능하며, 이 경우 혜택 기간만큼 다음 청구서에서 할인해 줍니다:

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 7일 더 연장
$subscription->extendTrial(
    now()->addDays(7)
);

// 기존 체험 종료일보다 5일 추가 연장
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe 웹훅 처리 (Handling Stripe Webhooks)

> [!NOTE]  
> 로컬 개발 시 [Stripe CLI](https://stripe.com/docs/stripe-cli)를 활용해 웹훅 테스트에 도움을 받을 수 있습니다.

Stripe는 웹훅으로 다양한 이벤트를 애플리케이션에 알립니다. Cashier는 기본적으로 웹훅 컨트롤러 라우트를 등록해 요청을 처리합니다.

웹훅 컨트롤러는 기본적으로 구독 취소, 고객 업데이트, 삭제, 구독 업데이트, 결제 수단 변경 등을 자동 처리하며, 필요에 따라 확장 가능합니니다.

웹훅 URL은 Stripe 대시보드에서 설정하세요. 기본 경로는 `/stripe/webhook`입니다. 다음 이벤트를 활성화하세요:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

편의를 위해 Cashier는 `cashier:webhook` Artisan 명령어를 제공합니다. 이 명령어는 Cashier가 필요한 모든 이벤트를 듣는 Stripe 웹훅을 생성합니다:

```shell
php artisan cashier:webhook
```

기본적으로 이 웹훅은 `APP_URL` 환경변수와 `cashier.webhook` 라우트를 사용합니다. 다른 URL을 사용하려면 `--url` 옵션을 제공합니다:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

웹훅 생성 시 Stripe API 버전을 지정하려면 `--api-version` 옵션 사용:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

즉시 활성화하지 않고 비활성 상태로 두려면 `--disabled` 옵션을 씁니다:

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]  
> Cashier에 포함된 웹훅 서명 검증 미들웨어([서명 검증](#verifying-webhook-signatures))로 들어오는 Stripe 웹훅 요청을 반드시 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Stripe 웹훅은 Laravel CSRF 보호를 우회해야 하므로 `App\Http\Middleware\VerifyCsrfToken` 미들웨어 내 `$except` 프로퍼티에 URI를 추가하거나, 웹 미들웨어 그룹 밖에 라우트를 등록하세요:

```php
protected $except = [
    'stripe/*',
];
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 일부 웹훅 이벤트를 자동 처리하지만, 추가 이벤트를 처리하려면 다음 이벤트를 구독하세요:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

두 이벤트 모두 Stripe 웹훅 전체 페이로드를 포함합니다.

예: `invoice.payment_succeeded` 처리용 이벤트 리스너 정의:

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
            // 수신한 이벤트 처리
        }
    }
}
```

리스너 등록은 `EventServiceProvider` 클래스에서 합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\StripeEventListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Cashier\Events\WebhookReceived;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        WebhookReceived::class => [
            StripeEventListener::class,
        ],
    ];
}
```

<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증 (Verifying Webhook Signatures)

웹훅 보안을 위해 [Stripe 웹훅 서명](https://stripe.com/docs/webhooks/signatures)을 이용할 수 있습니다. Cashier에는 Stripe에서 온 합법적 요청인지 검증하는 미들웨어가 포함되어 있습니다.

검증을 활성화하려면 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경변수를 설정하세요. 이 비밀 키는 Stripe 대시보드에서 얻습니다.

<a name="single-charges"></a>
## 일회성 결제 (Single Charges)

<a name="simple-charge"></a>
### 간단 결제 (Simple Charge)

일회성 결제를 하려면 빌러블 모델의 `charge` 메서드를 사용하세요. 두 번째 인자로 결제 수단 식별자가 필요합니다:

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

세 번째 인자에 배열 옵션을 전달해 Stripe 청구 생성 옵션을 지정할 수 있습니다:

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

기본 고객이 없거나 사용자 인스턴스 없이 결제하려면 새 빌러블 모델 인스턴스에서 호출하세요:

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

결제 실패 시 예외가 던져지고, 성공 시 `Laravel\Cashier\Payment` 인스턴스를 반환합니다:

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]  
> `charge` 메서드는 애플리케이션 통화의 최소 단위(예: 미국 달러는 센트)로 금액을 입력해야 합니다.

<a name="charge-with-invoice"></a>
### 청구서와 함께 결제 (Charge With Invoice)

청구서 생성과 함께 일회성 결제를 하려면 `invoicePrice` 메서드를 사용하세요. 예: 티셔츠 5개 청구:

```php
$user->invoicePrice('price_tshirt', 5);
```

기본 결제 수단으로 청구되며, 세 번째 인자에 인보이스 항목 옵션, 네 번째 인자에 인보이스 옵션 배열을 전달할 수 있습니다:

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

`invoicePrice`와 비슷한 `tabPrice`를 사용하면 여러 상품을 고객의 "탭"에 추가하고 청구할 수 있습니다(최대 250개 항목):

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

또는 `invoiceFor` 메서드로 간단한 명목상 청구도 가능합니다:

```php
$user->invoiceFor('One Time Fee', 500);
```

`invoiceFor`보다 미리 정의된 가격으로 `invoicePrice`, `tabPrice`를 사용하는 게 Stripe 대시보드 분석에 이점이 있습니다.

> [!WARNING]  
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 Stripe 청구서를 생성하며 실패하면 재시도합니다. 실패 시 재시도 없이 바로 종료하려면 Stripe API로 청구서를 종료해야 합니다.

<a name="creating-payment-intents"></a>
### 결제 인텐트 생성 (Creating Payment Intents)

빌러블 모델에서 `pay` 메서드로 Stripe 결제 인텐트를 생성할 수 있습니다. 반환 값은 `Laravel\Cashier\Payment` 인스턴스입니다:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

생성한 클라이언트 시크릿을 프론트엔드에 반환해 사용자 결제를 진행할 수 있습니다. Stripe 결제 인텐트 전체 흐름은 [Stripe 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

허용할 결제 수단 타입을 직접 지정하려면 `payWith` 메서드를 사용합니다:

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
> `pay`와 `payWith` 메서드는 금액을 애플리케이션 통화의 최소 단위로 받습니다.

<a name="refunding-charges"></a>
### 결제 환불 (Refunding Charges)

Stripe 결제 환불은 `refund` 메서드를 사용합니다. 첫 번째 인자는 Stripe 결제 인텐트 ID입니다:

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 청구서 (Invoices)

<a name="retrieving-invoices"></a>
### 청구서 조회 (Retrieving Invoices)

빌러블 모델의 청구서를 배열로 쉽게 조회할 수 있습니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스의 컬렉션을 반환합니다:

```php
$invoices = $user->invoices();
```

보류 중인 청구서도 포함하려면 `invoicesIncludingPending` 메서드 사용:

```php
$invoices = $user->invoicesIncludingPending();
```

특정 청구서를 ID로 조회하려면 `findInvoice`:

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 청구서 정보 표시

청구서를 리스트할 때 각 청구서의 날짜, 총액, 다운로드 링크 등을 보여줄 수 있습니다:

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
### 예정 청구서 (Upcoming Invoices)

고객의 다음 청구서를 조회하려면 `upcomingInvoice` 메서드를 사용하세요:

```php
$invoice = $user->upcomingInvoice();
```

복수 구독 고객이라면 특정 구독의 예정 청구서도 조회 가능:

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 청구서 미리보기 (Previewing Subscription Invoices)

가격 변경 전 예상 청구서를 미리 볼 때 `previewInvoice` 메서드를 사용:

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

여러 가격 배열도 전달할 수 있습니다:

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### PDF 청구서 생성 (Generating Invoice PDFs)

청구서를 PDF로 생성하려면 기본 렌더러인 Dompdf 라이브러리를 설치해야 합니다:

```php
composer require dompdf/dompdf
```

라우트 혹은 컨트롤러에서 `downloadInvoice` 메서드를 호출하면 HTTP 다운로드 응답을 반환합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

청구서 표시 데이터와 파일명 등을 옵션으로 커스터마이즈할 수도 있습니다:

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

파일명도 인자로 줘서 바꿀 수 있습니다(`.pdf` 확장자 자동 추가):

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 청구서 렌더러

기본 Dompdf 이외에 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현해 원하는 렌더러를 사용할 수 있습니다. 예로 타사 API로 PDF를 생성하는 경우:

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * 청구서 렌더링 후 PDF 바이트 반환
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

이후 `config/cashier.php` 파일의 `cashier.invoices.renderer` 값을 커스텀 렌더러 클래스명으로 변경하세요.

<a name="checkout"></a>
## 체크아웃 (Checkout)

Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout)을 지원합니다. Stripe Checkout은 결제용 맞춤 페이지 구현 부담을 줄이고, 호스팅된 결제 페이지를 제공합니다.

아래 문서에서는 Cashier와 Stripe Checkout 사용법을 안내합니다. Stripe 공식 [Checkout 문서](https://stripe.com/docs/payments/checkout)도 참고하세요.

<a name="product-checkouts"></a>
### 상품 체크아웃 (Product Checkouts)

Stripe 대시보드에 생성된 상품에 대한 체크아웃은 빌러블 모델의 `checkout` 메서드로 수행하며, Stripe 가격 ID를 전달합니다:

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

고객은 체크아웃 페이지로 리디렉션되고, 구매 성공 또는 취소 시 기본적으로 `home` 경로로 이동합니다. 직접 콜백 URL을 지정하려면 `success_url`과 `cancel_url` 옵션을 넘기세요:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

`success_url` 쿼리 문자열에 `{CHECKOUT_SESSION_ID}` 자리 표시자를 넣으면 Stripe가 해당 세션 ID로 대체합니다:

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

Stripe Checkout 기본 설정에서는 고객이 직접 프로모션 코드를 입력할 수 없습니다. 이를 허용하려면 `allowPromotionCodes` 메서드를 호출하세요:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 일회성 결제 체크아웃 (Single Charge Checkouts)

Stripe 대시보드에 상품이 없어도 임시 상품에 대해 간단한 결제 체크아웃을 진행할 수 있습니다. `checkoutCharge` 메서드에 금액, 상품명, 수량을 전달하세요:

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]  
> `checkoutCharge` 사용 시 Stripe 대시보드에 새 상품과 가격이 생성되므로, 사전에 상품 등록 후 `checkout` 메서드를 사용하는 게 권장됩니다.

<a name="subscription-checkouts"></a>
### 구독 체크아웃 (Subscription Checkouts)

> [!WARNING]  
> Stripe Checkout으로 구독 생성 시 `customer.subscription.created` 웹훅을 반드시 활성화해야 합니다. 이 웹훅이 구독 데이터베이스 기록을 생성하고 각 구독 아이템 정보를 저장합니다.

Stripe Checkout으로 구독 시작도 가능합니다. 구독 빌더의 `checkout` 메서드를 호출하면 해당 세션으로 고객을 리디렉션합니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

성공/취소 URL을 직접 지정할 수 있습니다:

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

프로모션 코드도 허용 가능:

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
> Stripe Checkout은 일부 구독 청구 옵션을 지원하지 않습니다. `anchorBillingCycleOn`, 정산 동작(proration behavior), 결제 동작(payment behavior) 설정은 체크아웃 세션에 영향을 주지 않습니다. 가능한 설정은 [Stripe Checkout Session API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout과 체험 기간

Stripe Checkout 이용 시 체험 기간도 정의할 수 있습니다:

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

단, 체험 기간은 최소 48시간 이상이어야 합니다. 이는 Stripe Checkout 제한입니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독과 웹훅

Stripe와 Cashier는 웹훅으로 구독 상태를 갱신하므로, 고객이 결제 후 앱으로 돌아올 때 구독이 아직 활성화되지 않았을 수 있습니다. 이 경우 구독 대기 중임을 알리는 메시지 표시를 고려하세요.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집 (Collecting Tax IDs)

체크아웃 세션에서 고객 세금 ID 수집을 활성화하려면 `collectTaxIds` 메서드를 호출하세요:

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

이렇게 하면 고객이 기업체 구매자로 표시 여부를 체크하는 체크박스가 생기며, 세금 ID를 입력할 수 있게 됩니다.

> [!WARNING]  
> 자동 세금 계산([세금 설정](#tax-configuration) 참고)를 구성했다면 이 메서드 호출은 필요 없습니다.

<a name="guest-checkouts"></a>
### 비회원 체크아웃 (Guest Checkouts)

`Checkout::guest` 메서드를 통해 계정 없는 비회원 체크아웃 세션을 만들 수 있습니다:

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

비회원 체크아웃 세션도 프로모션 코드 적용 등 추가 기능 사용 가능:

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

비회원 체크아웃 완료 후 Stripe가 `checkout.session.completed` 웹훅을 발송할 수 있으므로, 웹훅 설정도 꼭 하세요.

<a name="handling-failed-payments"></a>
## 결제 실패 처리 (Handling Failed Payments)

가끔 구독이나 단일 결제 실패 시 `Laravel\Cashier\Exceptions\IncompletePayment` 예외가 던져집니다. 이 경우 두 가지 대응책이 있습니다.

먼저, Cashier가 제공하는 결제 확인 페이지로 리디렉션하는 방법:

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

확인 페이지에서 고객은 카드 정보를 다시 입력하고 3D Secure 같은 추가 인증을 거칩니다. 인증 후 `redirect` 파라미터로 지정된 URL로 리디렉션되며, 성공/실패 메시지가 쿼리스트링으로 전달됩니다.

지원되는 결제 방법:

- 신용카드
- Alipay
- Bancontact
- BECS 직접 인출
- EPS
- Giropay
- iDEAL
- SEPA 직접 인출

다른 방법으로는 Stripe 대시보드에서 [자동 청구 이메일 설정](https://dashboard.stripe.com/account/billing/automatic)을 해 Stripe가 결제 확인을 처리하게 할 수도 있습니다. 다만 예외 발생 시 고객에게 결제 안내 이메일이 발송되니 알리셔야 합니다.

참고로 `charge`, `invoiceFor`, `invoice` 메서드, `SubscriptionBuilder`의 `create`, 그리고 `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 메서드도 불완전 결제 예외를 던질 수 있습니다.

불완전 결제 여부 확인은 다음과 같이:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

예외 객체에서 구체적 결제 상태도 확인 가능:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 인텐트 상태 조회
    $exception->payment->status;

    if ($exception->payment->requiresPaymentMethod()) {
        // 결제 수단 필요
    } elseif ($exception->payment->requiresConfirmation()) {
        // 추가 확인 필요
    }
}
```

<a name="confirming-payments"></a>
### 결제 확인 (Confirming Payments)

일부 결제 수단은 확인과정에서 추가 정보가 필요합니다. 예: SEPA는 "엔드유저 위임" 데이터를 요구합니다.

`withPaymentConfirmationOptions` 메서드로 옵션을 넘겨 결제 확인 설정을 할 수 있습니다:

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

[Stripe 결제 인텐트 확인 API 문서](https://stripe.com/docs/api/payment_intents/confirm)를 참고해 옵션 종류를 확인하세요.

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증 (Strong Customer Authentication, SCA)

유럽 거주 사업자 또는 고객은 2019년 9월부터 시행된 EU SCA 규정을 따라야 합니다. Stripe와 Cashier는 SCA 규정을 준수하도록 돕습니다.

> [!WARNING]  
> 시작 전 [Stripe PSD2 & SCA 가이드](https://stripe.com/guides/strong-customer-authentication)와 [SCA API 문서](https://stripe.com/docs/strong-customer-authentication)를 확인하세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 결제 승인 필요

SCA 규정은 결제 확인에 추가 인증을 요구할 수 있습니다. 이 경우 Cashier가 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 던지며, [결제 실패 처리](#handling-failed-payments)를 참고해 대응하세요.

Stripe 혹은 Cashier가 제공하는 결제 확인 화면은 특정 은행/카드사의 플로우에 맞춰 3D Secure, 소액 임시 결제, 단말 인증 등을 안내합니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체 상태

추가 인증 요청 중 구독 상태는 `incomplete` 혹은 `past_due`로 유지됩니다 (`stripe_status` 열 기준). Cashier가 결제 완료 웹훅을 받으면 자동으로 구독을 활성화합니다.

`incomplete`, `past_due` 상태에 대한 자세한 내용은 [이전 문서](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>
### 오프세션 결제 알림

SCA 규정상 구독 유지 중에도 고객이 결제 상세를 다시 확인해야 할 때 Cashier가 알림을 보낼 수 있습니다. 예: 구독 갱신 시.

알림 기능을 켜려면 `.env`에 다음과 같이 알림 클래스를 지정하세요(기본적으로 비활성):

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

알림을 성공적으로 보내려면 Stripe 웹훅에서 `invoice.payment_action_required` 이벤트 사용 설정 및 빌러블 모델에 `Illuminate\Notifications\Notifiable` 트레잇을 추가하세요.

> [!WARNING]  
> 사용자 수동 결제 시에도 알림이 갈 수 있습니다. Stripe가 수동인지 오프세션인지 구별할 수 없기 때문이며, 이미 결제 완료했으면 중복 결제가 발생하지 않습니다.

<a name="stripe-sdk"></a>
## Stripe SDK

많은 Cashier 객체는 내부적으로 Stripe SDK 객체를 래핑합니다. Stripe 객체에 직접 접근하려면 `asStripe` 메서드를 사용하세요:

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

Stripe 구독 직접 업데이트는 `updateStripeSubscription` 메서드로:

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Cashier` 클래스의 `stripe` 메서드로 `Stripe\StripeClient` 인스턴스를 바로 사용할 수도 있습니다:

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트 (Testing)

Cashier 기반 앱 테스트 시 Stripe API를 모킹할 수 있으나, Cashier 로직 일부를 다시 구현해야 하므로 권장하지 않습니다. 실제 Stripe API를 호출하도록 하는 게 더 안정적인 테스트입니다. 느리면 별도 PHPUnit 그룹에 분리하세요.

테스트 환경에서 사용할 Stripe 비밀 키를 `phpunit.xml`에 추가하세요:

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

테스트 시 Cashier는 이 시험용 Stripe 환경으로 요청을 보내며, 사전에 구독과 가격을 Stripe 테스트 계정에 준비해 두면 편리합니다.

> [!NOTE]  
> 카드 거부 등 다양한 결제 시나리오 테스트를 위해 [Stripe 테스트 카드 번호 및 토큰](https://stripe.com/docs/testing)을 활용하세요.