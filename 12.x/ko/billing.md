# 라라벨 Cashier (Stripe) (Laravel Cashier (Stripe))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
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
    - [고객 정보 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
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
    - [여러 상품이 포함된 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일(앵커 날짜)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험(트라이얼)](#subscription-trials)
    - [결제 수단 선등록 체험](#with-payment-method-up-front)
    - [결제 수단 없이 체험](#without-payment-method-up-front)
    - [체험(트라이얼) 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [단순 결제](#simple-charge)
    - [인보이스 결제](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원(게스트) Checkout](#guest-checkouts)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정된 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강화된 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 인증이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 쉽고 직관적으로 사용할 수 있는 유창한 인터페이스를 제공합니다. Cashier는 여러분이 작성하기 꺼려하는 거의 모든 반복적인 구독 결제 코드를 대신 처리합니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰, 구독 변경, 구독 "수량" 처리, 해지 후 유예 기간, 인보이스 PDF 생성까지 다양한 기능을 제공합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier를 새로운 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

> [!WARNING]
> 변경으로 인한 장애를 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용하며, 새로운 Stripe 기능과 개선 사항을 적용하기 위해 소규모(minor) 릴리즈에서 Stripe API 버전이 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치하세요.

```shell
composer require laravel/cashier
```

패키지 설치 후, `vendor:publish` Artisan 명령어를 이용해 Cashier 마이그레이션을 게시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

이제 데이터베이스 마이그레이션을 실행하세요:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 여러분의 `users` 테이블에 여러 컬럼을 추가하며, 고객의 모든 구독 정보를 관리할 `subscriptions` 테이블과, 여러 가격이 포함된 구독을 위한 `subscription_items` 테이블을 새로 생성합니다.

원하는 경우, 아래 명령어를 이용해 Cashier의 설정 파일도 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 모든 Stripe 이벤트를 올바르게 처리하도록 반드시 [Cashier의 Webhook 처리를 설정](#handling-stripe-webhooks)해야 합니다.

> [!WARNING]
> Stripe에서는 Stripe 식별자(Stripe ID)를 저장하는 컬럼은 대소문자를 구분해야 한다고 권장합니다. 따라서, MySQL을 사용한다면 `stripe_id` 컬럼의 컬레이션(collaion)을 반드시 `utf8_bin`으로 설정하세요. 관련 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 가능 모델

Cashier를 사용하기 전에, 여러분의 청구 가능(과금 대상) 모델 정의에 `Billable` 트레이트(trait)를 추가해야 합니다. 보통은 `App\Models\User` 모델이 해당됩니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 청구 작업에 필요한 다양한 메서드를 제공합니다.

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 청구 가능 모델이 라라벨에서 제공하는 `App\Models\User` 클래스라고 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 좋습니다.

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
> 라라벨 기본 제공 `App\Models\User` 모델이 아닌 다른 모델을 사용할 경우, Cashier에서 제공하는 [마이그레이션 파일을 게시하고](#installation) 해당 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에 Stripe API 키를 설정해야 합니다. Stripe API 키는 Stripe 관리자 페이지에서 확인할 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경변수는 반드시 `.env` 파일에 정의되어 있어야 합니다. 이 변수는 Webhook 요청이 실제 Stripe로부터 온 것인지 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경변수를 설정하세요.

```ini
CASHIER_CURRENCY=eur
```

추가로, Cashier의 통화 설정 외에도, 인보이스에 표시되는 금액을 포맷할 때 사용할 로케일(locale)을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용해 통화 로케일을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe에서 생성되는 모든 인보이스에 대해 자동으로 세금을 계산할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 자동 세금 계산을 활성화하세요.

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

세금 계산을 활성화하면, 새로 생성되는 모든 구독 및 단일 인보이스에 자동으로 세금이 계산됩니다.

해당 기능이 제대로 동작하려면 고객의 이름, 주소, 세금 ID 등 결제 정보가 Stripe로 동기화되어야 합니다. 이를 위해 Cashier에서 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe)와 [세금 ID](#tax-ids) 관련 메서드를 사용할 수 있습니다.

<a name="logging"></a>
### 로깅

Cashier는 Stripe 오류 발생 시 사용할 로그 채널을 직접 지정할 수 있게 해줍니다. 애플리케이션의 `.env` 파일에 `CASHIER_LOGGER` 환경변수를 정의하여 로그 채널을 선택하세요.

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 과정에서 발생한 예외는 기본적으로 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier에서 내부적으로 사용하는 모델을 확장해서 자신만의 모델을 정의할 수도 있습니다. 이를 위해 직접 모델을 만들고 Cashier 모델을 상속 받으세요.

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에 커스텀 모델을 사용하도록 지정할 수 있습니다. 보통 이 작업은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다.

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
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 상품 판매

> [!NOTE]
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격의 상품을 먼저 정의해야 합니다. 또한, 반드시 [Cashier의 Webhook 처리를 설정](#handling-stripe-webhooks)하세요.

애플리케이션에서 상품 및 구독 결제를 제공하는 일은 어렵게 느껴질 수 있습니다. 그러나 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 이용하면 최신 웹 애플리케이션에 견고한 결제 연동 기능을 손쉽게 구축할 수 있습니다.

비정기적인 단일 상품 결제를 위해, Cashier의 기능을 활용하여 고객을 Stripe Checkout으로 리다이렉트시킬 수 있습니다. Stripe Checkout에서 고객은 결제 정보를 입력하고 구매를 확정하게 됩니다. 결제가 완료된 후에는 애플리케이션 내에서 원하는 성공 URL로 고객을 리다이렉트할 수 있습니다.

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

위 예시와 같이, Cashier에서 제공하는 `checkout` 메서드를 사용해 Stripe에서 정의한 "가격 식별자"를 기반으로 고객을 Checkout으로 리다이렉트할 수 있습니다. Stripe에서 말하는 "price"란 [특정 상품에 대한 가격을 미리 정의한 것](https://stripe.com/docs/products-prices/how-products-and-prices-work)입니다.

필요하다면, `checkout` 메서드는 Stripe 고객을 자동으로 생성하고, Stripe 고객 레코드를 애플리케이션의 해당 사용자와 연결해줍니다. 결제 세션이 완료되면, 고객은 사용자에게 알림 메시지를 표시할 수 있는 전용 성공 또는 취소 페이지로 이동하게 됩니다.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Stripe Checkout에 메타데이터 전달하기

상품 판매 시, 주문 완료 내역 및 구매 상품을 직접 정의한 `Cart`와 `Order` 모델을 통해 관리하는 경우가 많습니다. Stripe Checkout을 사용해 결제를 완료하는 고객을 리다이렉트할 때, 기존 주문 식별자를 전달하여 결제가 완료되었을 때 해당 주문과 연결할 필요가 있을 수 있습니다.

이럴 때, `checkout` 메서드에 `metadata` 배열을 전달하면 됩니다. 예를 들어, 사용자가 Checkout을 시작할 때, 애플리케이션에서 미결제 상태의 `Order`를 먼저 생성했다고 가정해보겠습니다. 참고로 `Cart`와 `Order` 모델은 예시 목적일 뿐 실제로 Cashier에서 제공하지 않으므로, 여러분의 애플리케이션 상황에 맞게 자유롭게 구현하면 됩니다.

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

위 예시와 같이, 사용자가 결제를 시작하면 장바구니 및 주문에 연관된 Stripe 가격 식별자를 모두 `checkout` 메서드로 전달합니다. 쇼핑 카트나 주문과 같은 구조로 고객이 상품을 장바구니에 담으면 해당 내용들을 여러분 애플리케이션에서 관리하는 책임이 있습니다. 우리는 또한 주문의 ID를 `metadata` 배열을 통해 Stripe Checkout 세션에 전달하고, Checkout 성공 경로에 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe가 결제 완료 후 고객을 여러분의 애플리케이션으로 리다이렉션할 때, 이 템플릿 변수는 자동으로 Checkout 세션 ID로 치환됩니다.

다음으로 Checkout 성공 라우트를 구현해봅시다. 이 라우트는 Stripe Checkout을 통해 결제가 완료된 뒤 사용자가 이동하게 될 경로입니다. 이곳에서는 Stripe Checkout 세션 ID와 연관된 Stripe Checkout 인스턴스를 불러와, 전달한 메타데이터에 접근하고 주문 상태를 업데이트할 수 있습니다.

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

Checkout 세션 객체에 담긴 데이터에 대한 자세한 내용은 Stripe의 [공식 문서](https://stripe.com/docs/api/checkout/sessions/object)를 참고하세요.

<a name="quickstart-selling-subscriptions"></a>
### 구독 판매

> [!NOTE]
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격의 상품을 먼저 정의해야 합니다. 또한, 반드시 [Cashier의 Webhook 처리를 설정](#handling-stripe-webhooks)하세요.

애플리케이션에서 상품 및 구독 결제를 제공하는 일은 어렵게 느껴질 수 있습니다. 하지만 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 활용하면 쉽고 견고한 결제 연동을 구현할 수 있습니다.

Cashier와 Stripe Checkout으로 구독 상품 판매 방법을 알아보겠습니다. 예를 들어, `price_basic_monthly`(월간)와 `price_basic_yearly`(연간) 플랜이 있는 'Basic' 구독 서비스, 그리고 추가로 `pro_basic` 상품, `pro_expert` 플랜이 있다고 가정합시다.

먼저, 고객이 서비스에 구독하는 방식부터 살펴보겠습니다. 고객이 애플리케이션의 가격 페이지에서 Basic 플랜에 가입 버튼을 클릭했다고 가정할 수 있습니다. 이 버튼이나 링크는 사용자가 선택한 플랜에 대한 Stripe Checkout 세션을 생성하는 라라벨 라우트로 연결해야 합니다.

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

위 예시처럼, 고객은 Basic 플랜 구독을 Stripe Checkout 세션에서 진행하게 됩니다. 결제 또는 취소가 성공하면, `checkout` 메서드에 전달한 URL로 고객이 리다이렉트됩니다. 일부 결제 수단은 처리에 시간이 걸릴 수 있으므로 실제로 고객의 구독이 시작되는 시점을 정확하게 파악하려면 [Cashier의 Webhook 처리](#handling-stripe-webhooks)도 함께 설정해야 합니다.

이제 고객이 구독을 시작할 수 있게 되었으니, 구독한 사용자만 특정 페이지에 접근할 수 있도록 제한해보겠습니다. Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 사용해, 사용자의 구독 상태를 손쉽게 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>당신은 현재 구독 중입니다.</p>
@endif
```

사용자가 특정 상품이나 가격에 구독 중인지도 쉽게 확인할 수 있습니다.

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>Basic 상품을 구독 중입니다.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>월간 Basic 플랜을 구독 중입니다.</p>
@endif
```

<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독 여부를 체크하는 미들웨어 만들기

좀 더 편리하게 구독자를 구분하고 싶다면, [미들웨어](/docs/12.x/middleware)를 만들어, 들어오는 요청이 구독자인지 쉽게 확인할 수 있습니다. 미들웨어를 정의한 후, 해당 라우트에 지정하면 구독하지 않은 사용자가 접근하지 못하도록 할 수 있습니다.

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
            // 사용자에게 구독 페이지로 리다이렉트 안내...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

미들웨어를 정의한 후 라우트에 적용할 수 있습니다.

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```

<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 직접 결제 플랜을 관리할 수 있게 하기

고객이 구독 플랜을 다른 상품이나 "등급"으로 변경하고 싶어할 수 있습니다. 이를 가장 간단하게 제공하는 방법은 Stripe의 [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal)을 활용하는 것입니다. 이 포털은 고객이 인보이스 다운로드, 결제 수단 변경, 구독 플랜 변경이 가능한 Stripe의 자체 호스팅 UI입니다.

먼저, 여러분의 애플리케이션에서 Stripe Customer Billing Portal 세션을 시작하는 라우트로 연결되는 링크나 버튼을 생성합니다.

```blade
<a href="{{ route('billing') }}">
    결제 관리
</a>
```

이제 Stripe Customer Billing Portal 세션을 시작하고 사용자를 포털로 리다이렉트하는 라우트를 정의합니다. `redirectToBillingPortal` 메서드는 포털 종료 후 사용자를 돌려보낼 URL을 인자로 받을 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```

> [!NOTE]
> Cashier의 Webhook 처리만 제대로 되어 있다면, Cashier가 Stripe에서 들어오는 webhook을 확인하여 애플리케이션의 Cashier 관련 데이터베이스 정보도 자동으로 동기화해줍니다. 예를 들어, 고객이 Stripe Customer Billing Portal에서 구독을 취소하면, Cashier는 해당 webhook을 수신하여 애플리케이션의 구독 상태를 'cancelled'로 변경합니다.

<a name="customers"></a>
## 고객

<a name="retrieving-customers"></a>
### 고객 조회

Stripe ID로 고객을 조회하려면, `Cashier::findBillable` 메서드를 사용하세요. 이 메서드는 청구 가능(billable) 모델의 인스턴스를 반환합니다.

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성

가끔은 구독을 시작하지 않고도 Stripe 고객만 미리 만들어야 할 수도 있습니다. `createAsStripeCustomer` 메서드를 사용해 이를 수행할 수 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer();
```

Stripe에 고객이 생성되고 나면, 이후에 구독을 시작할 수 있습니다. Stripe API에서 허용하는 [고객 생성 옵션](https://stripe.com/docs/api/customers/create)을 추가 인수로 배열 형태로 전달할 수도 있습니다.

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```

청구 가능(billable) 모델에 대한 Stripe 고객 객체를 반환하고 싶다면 `asStripeCustomer` 메서드를 사용할 수 있습니다.

```php
$stripeCustomer = $user->asStripeCustomer();
```

지정된 청구 가능 모델이 Stripe에 이미 고객으로 등록되어 있는지 확신이 들지 않을 때는, `createOrGetStripeCustomer` 메서드를 사용하세요. 이 메서드는 필요하면 새로 고객을 Stripe에 생성합니다.

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 정보 업데이트

가끔은 Stripe에 저장된 고객 정보를 직접 수정하고 싶을 때가 있습니다. `updateStripeCustomer` 메서드를 사용하면 됩니다. 이 메서드는 [Stripe API가 지원하는 고객 정보 업데이트 옵션](https://stripe.com/docs/api/customers/update) 배열을 인수로 받습니다.

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액

Stripe에서는 고객의 "잔액"을 추가(credit)하거나 차감(debit)할 수 있습니다. 차후 생성되는 새 인보이스에 해당 잔액이 반영됩니다. 고객의 전체 잔액은 청구 가능 모델에 포함된 `balance` 메서드로 확인할 수 있습니다. 이 메서드는 고객 통화로 포맷된 잔액 문자열을 반환합니다.

```php
$balance = $user->balance();
```

고객에게 잔액을 추가(credit)하려면, `creditBalance` 메서드에 금액을 전달하세요. 필요하다면 설명도 함께 전달할 수 있습니다.

```php
$user->creditBalance(500, '프리미엄 고객 충전.');
```

`debitBalance` 메서드에 값을 전달하면 해당 금액만큼 잔액이 차감(debit)됩니다.

```php
$user->debitBalance(300, '사용 제한 페널티.');
```

`applyBalance` 메서드는 고객에게 새로운 잔액 트랜잭션(거래 내역)을 생성합니다. `balanceTransactions` 메서드를 사용해 거래 내역 레코드 전체를 조회할 수 있습니다. 고객에게 크레딧 및 디빗 내역을 보여주려면 이 기능이 유용합니다.

```php
// 모든 거래 내역 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액...
    $amount = $transaction->amount(); // $2.31

    // 필요 시 연관 인보이스도 조회...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID

Cashier는 고객의 세금 ID(Tax ID) 관리를 쉽게 할 수 있는 기능을 제공합니다. 예를 들어, `taxIds` 메서드를 사용하면 고객에게 할당된 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션 형태로 모두 가져올 수 있습니다.

```php
$taxIds = $user->taxIds();
```

고객의 특정 세금 ID를 식별자로 조회할 수도 있습니다.

```php
$taxId = $user->findTaxId('txi_belgium');
```

적법한 [타입](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 `createTaxId` 메서드에 전달하여 새로운 세금 ID도 생성할 수 있습니다.

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId` 메서드는 즉시 해당 VAT ID를 고객 계정에 추가합니다. [VAT ID 검증은 Stripe에서 자동으로 수행](https://stripe.com/docs/invoicing/customer/tax-ids#validation)됩니다. 단, 검증 처리는 비동기적으로 진행되므로 웹훅 `customer.tax_id.updated` 이벤트를 수신하고, [VAT ID의 `verification` 파라미터](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 확인하면 검증 결과를 알 수 있습니다. Webhook 처리에 관한 자세한 내용은 [Webhook 핸들러 정의 문서](#handling-stripe-webhooks)를 참고하세요.

세금 ID 삭제는 `deleteTaxId` 메서드로 처리할 수 있습니다.

```php
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화

대개 애플리케이션에서 사용자가 이름, 이메일, 기타 Stripe에도 저장되는 정보를 수정했을 때, Stripe에도 동일한 정보를 반영해줘야 합니다. 이렇게 하면 Stripe와 애플리케이션의 정보가 항상 동기화된 상태로 유지됩니다.

이를 자동화하려면, 청구 가능(billable) 모델의 `updated` 이벤트에 리스너(이벤트 핸들러)를 정의할 수 있습니다. 해당 이벤트가 발생하면 모델에서 `syncStripeCustomerDetails` 메서드를 호출하도록 설정하면 됩니다.

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

이제 고객 모델이 업데이트될 때마다 해당 정보가 Stripe와 자동으로 동기화됩니다. 참고로, Cashier는 고객이 처음 생성될 때도 Stripe와 자동으로 정보를 동기화합니다.

Stripe와 동기화되는 고객 정보 컬럼을 좀 더 세밀하게 제어하고 싶다면, Cashier에서 제공하는 여러 메서드를 오버라이드하면 됩니다. 예를 들어, Stripe로 동기화할 고객의 "이름" 속성을 커스터마이징하고 싶은 경우 `stripeName` 메서드를 오버라이드하면 됩니다.

```php
/**
 * Stripe에 동기화할 고객 이름 반환.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```

이와 비슷하게, `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 등의 메서드도 오버라이드할 수 있습니다. 이 메서드들은 [Stripe 고객 객체 업데이트](https://stripe.com/docs/api/customers/update) 시 각 파라미터에 해당 정보를 동기화합니다. 만약 전체 동기화 프로세스를 완전히 직접 제어하고 싶다면, `syncStripeCustomerDetails` 메서드를 오버라이드하면 됩니다.

<a name="billing-portal"></a>
### 청구 포털

Stripe는 [청구 포털을 간단히 설정할 수 있는 기능](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 이를 이용하면 고객이 스스로 구독 관리, 결제 수단 관리, 청구 내역 열람을 할 수 있습니다. 컨트롤러나 라우트에서 빌러블(billable) 모델의 `redirectToBillingPortal` 메서드를 실행하면 해당 고객을 Stripe의 청구 포털로 리다이렉트시킬 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 사용자가 Stripe 청구 포털에서 구독 관리 등을 마치면, Stripe 포털 내에 제공되는 링크를 통해 라라벨 애플리케이션의 `home` 라우트로 돌아올 수 있습니다. 사용자가 포털 종료 후 이동할 URL을 직접 지정하려면, `redirectToBillingPortal` 메서드에 URL을 인수로 전달하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리다이렉트 응답을 생성하지 않고 청구 포털 URL만 얻고 싶다면, `billingPortalUrl` 메서드를 사용하세요.

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단

<a name="storing-payment-methods"></a>
### 결제 수단 저장

Stripe에서 구독 생성이나 "단건(1회성)" 결제를 하려면, 결제 수단을 미리 저장하고 Stripe에서 해당 결제 수단 식별자를 받아와야 합니다. 이 절차는 구독에 사용할 때와 1회성 결제에 사용할 때 각각 다르므로, 아래에서 각각의 경우를 살펴보겠습니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독을 위한 결제 수단

정기 결제를 목적으로 고객의 카드 정보를 저장할 때는 Stripe의 "Setup Intents" API를 사용해야 합니다. 이 API를 이용하면 고객의 결제 수단 정보를 안전하게 수집할 수 있습니다. "Setup Intent"란 Stripe에 결제 수단 저장 의도를 알리는 역할을 합니다. Cashier의 `Billable` 트레이트는 `createSetupIntent` 메서드를 제공하여 쉽게 Setup Intent를 만들 수 있도록 도와줍니다. 이 메서드는 결제 수단 입력 폼을 렌더링하는 라우트나 컨트롤러에서 사용해야 합니다.

```php
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

Setup Intent를 생성한 후 뷰(view)로 전달했다면, 이 비밀값(secret)을 결제 수단 정보를 입력받는 요소에 바인딩해주어야 합니다. 예를 들어, 다음과 같은 "결제 수단 업데이트" 폼을 참고하세요.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

다음으로, Stripe.js 라이브러리를 이용해 [Stripe Element](https://stripe.com/docs/stripe-js)를 폼에 연결하고, 고객의 결제 정보를 안전하게 수집할 수 있습니다.

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

이제 카드를 검증하고 Stripe에서 안전한 "결제 수단 식별자"를 발급받으려면, [Stripe의 `confirmCardSetup` 메서드](https://stripe.com/docs/js/setup_intents/confirm_card_setup)를 사용하면 됩니다.

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
        // Display "error.message" to the user...
    } else {
        // The card has been verified successfully...
    }
});
```

Stripe에서 카드 정보가 정상적으로 검증되었다면, 생성된 `setupIntent.payment_method` 식별자를 라라벨 애플리케이션으로 전달하여 고객에게 결제 수단으로 등록시킬 수 있습니다. 이 결제 수단은 [새 결제 수단으로 추가](#adding-payment-methods)하거나, [기본 결제 수단으로 지정](#updating-the-default-payment-method)하거나, 즉시 [새 구독 생성](#creating-subscriptions)에 활용할 수 있습니다.

> [!NOTE]
> Setup Intent와 고객 결제 정보 수집에 대해 더 자세한 내용을 알고 싶다면 [Stripe에서 제공하는 개요 가이드](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>

#### 단일 청구 시 결제 수단 처리

물론, 고객의 결제 수단으로 단일 청구를 수행할 경우에는 결제 수단 식별자를 한 번만 사용하면 충분합니다. Stripe의 제한으로 인해, 고객의 저장된 기본 결제 수단을 단일 청구에 사용할 수 없습니다. Stripe.js 라이브러리를 사용하여 고객이 직접 결제 정보를 입력하도록 해야 합니다. 예를 들어, 아래와 같은 폼을 생각해 볼 수 있습니다.

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

이와 같은 폼을 정의한 후에는 Stripe.js 라이브러리를 사용하여 폼에 [Stripe Element](https://stripe.com/docs/stripe-js)를 연결하고 고객의 결제 정보를 안전하게 수집할 수 있습니다.

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

다음으로, 카드를 검증하고 Stripe의 [Stripe의 `createPaymentMethod` 메서드](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method)를 통해 안전한 "결제 수단 식별자"를 받아올 수 있습니다.

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
        // Display "error.message" to the user...
    } else {
        // The card has been verified successfully...
    }
});
```

카드가 성공적으로 인증되었다면, `paymentMethod.id`를 라라벨 애플리케이션에 전달하여 [단일 청구](#simple-charge)를 처리할 수 있습니다.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회

billable(청구 가능) 모델 인스턴스에서 `paymentMethods` 메서드를 호출하면 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다.

```php
$paymentMethods = $user->paymentMethods();
```

기본적으로 이 메서드는 모든 종류의 결제 수단을 반환합니다. 특정 타입의 결제 수단만 조회하려면, `type`을 인수로 전달하면 됩니다.

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```

고객의 기본 결제 수단을 조회하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다.

```php
$paymentMethod = $user->defaultPaymentMethod();
```

billable 모델에 연결된 특정 결제 수단을 조회하려면 `findPaymentMethod` 메서드를 사용하세요.

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="payment-method-presence"></a>
### 결제 수단 존재 여부 확인

billable 모델이 기본 결제 수단을 가지고 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출합니다.

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```

billable 모델이 하나 이상의 결제 수단을 가지고 있는지 확인하려면 `hasPaymentMethod` 메서드를 사용할 수 있습니다.

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```

이 메서드는 billable 모델에 어떤 결제 수단이라도 있는지 검사합니다. 특정 타입의 결제 수단이 존재하는지 확인하려면 `type`을 인수로 전달하면 됩니다.

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 갱신

`updateDefaultPaymentMethod` 메서드를 사용하여 고객의 기본 결제 수단 정보를 갱신할 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 받아 새로운 결제 수단을 기본 결제 수단으로 지정합니다.

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```

Stripe에 저장된 고객의 기본 결제 수단 정보와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용하세요.

```php
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객의 기본 결제 수단은 인보이스 발급 및 신규 구독 생성에만 사용할 수 있습니다. Stripe에서 정한 제한으로 인해 단일 청구에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가

새로운 결제 수단을 추가하려면, 결제 수단 식별자를 전달하여 billable 모델에서 `addPaymentMethod` 메서드를 호출하면 됩니다.

```php
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 식별자를 어떻게 얻는지 알고 싶으시다면, [결제 수단 저장 문서](#storing-payment-methods)를 참고하시기 바랍니다.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제

결제 수단을 삭제하려면 삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출하세요.

```php
$paymentMethod->delete();
```

billable 모델에서 특정 결제 수단을 삭제하려면 `deletePaymentMethod` 메서드를 사용하면 됩니다.

```php
$user->deletePaymentMethod('pm_visa');
```

`deletePaymentMethods` 메서드는 billable 모델에 저장된 모든 결제 수단 정보를 삭제합니다.

```php
$user->deletePaymentMethods();
```

기본적으로 이 메서드는 모든 타입의 결제 수단을 삭제합니다. 특정 타입만 삭제하고 싶다면 `type`을 인수로 전달하면 됩니다.

```php
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 사용자가 활성 구독을 보유하고 있는 경우, 애플리케이션에서 해당 사용자가 기본 결제 수단을 삭제하지 못하도록 해야 합니다.

<a name="subscriptions"></a>
## 구독(Subscriptions)

구독을 통해서 고객에게 반복 결제(정기 결제)를 제공할 수 있습니다. Cashier에서 관리하는 Stripe 구독은 여러 구독 가격, 구독 수량, 체험(Trial) 기간 등 다양한 기능을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면 먼저 billable 모델 인스턴스(일반적으로 `App\Models\User` 인스턴스)를 가져와야 합니다. 모델 인스턴스를 가져온 뒤에는 `newSubscription` 메서드를 통해 구독을 생성할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

`newSubscription` 메서드의 첫 번째 인수는 구독의 내부용 타입입니다. 애플리케이션에서 구독이 단 하나밖에 없다면 `default`나 `primary` 등으로 지정할 수 있습니다. 이 구독 타입은 내부적으로만 사용되며 사용자에게는 노출되지 않습니다. 또한 반드시 공백이 없어야 하며, 한 번 구독을 생성한 뒤에는 변경해서는 안 됩니다. 두 번째 인수는 사용자가 구독할 구체적인 가격(Stripe의 price 식별자)입니다. 이 값은 Stripe에서 해당 가격의 식별자와 일치해야 합니다.

그리고 [Stripe 결제 수단 식별자](#storing-payment-methods) 또는 Stripe `PaymentMethod` 객체를 받는 `create` 메서드를 호출하면 구독을 시작하고, billable 모델의 Stripe 고객 ID와 기타 결제 관련 정보도 데이터베이스에 업데이트됩니다.

> [!WARNING]
> 구독의 `create` 메서드에 결제 수단 식별자를 바로 전달하면, 해당 결제 수단이 자동으로 사용자의 저장된 결제 수단 목록에도 추가됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 인보이스 이메일을 통한 반복 결제 청구

고객의 반복 결제를 자동으로 진행하는 대신, Stripe에서 결제 기한이 도래할 때마다 인보이스를 이메일로 보내도록 설정할 수 있습니다. 이 경우 고객이 인보이스를 수신한 후 직접 결제할 수 있으며, 반복 결제를 인보이스로 청구하는 경우 고객이 결제 수단을 사전에 입력하지 않아도 됩니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

고객이 결제를 완료하기 전까지 구독이 취소되지 않도록 허용할 기간은 `days_until_due` 옵션에 의해 결정됩니다. 기본값은 30일이지만, 필요하다면 원하는 값으로 지정할 수 있습니다.

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 구독 수량(Quantity) 지정

구독 생성 시 가격별로 [수량(Quantity)](https://stripe.com/docs/billing/subscriptions/quantities)을 지정하려면, 구독 빌더에서 `quantity` 메서드를 먼저 호출하세요.

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 정보 입력

Stripe에서 지원하는 [고객 정보](https://stripe.com/docs/api/customers/create)나 [구독 옵션](https://stripe.com/docs/api/subscriptions/create) 등 추가 옵션을 지정하려면, `create` 메서드의 두 번째와 세 번째 인수로 옵션을 전달하면 됩니다.

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
#### 쿠폰 적용

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요.

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```

또는, [Stripe 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하고 싶다면 `withPromotionCode` 메서드를 이용하세요.

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```

여기서 넘기는 프로모션 코드 ID는 프로모션 코드에 할당된 Stripe API ID이어야 하며, 고객이 실제로 보는 프로모션 코드가 아닙니다. 만약 고객용 프로모션 코드로부터 실제 Stripe 프로모션 코드 ID를 찾고 싶으면 `findPromotionCode` 메서드를 이용할 수 있습니다.

```php
// 고객용 코드로 프로모션 코드 ID 찾기...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// 활성화된 프로모션 코드 ID 찾기...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

위 예시에서 반환된 `$promotionCode` 객체는 `Laravel\Cashier\PromotionCode` 인스턴스이며, 내부적으로 `Stripe\PromotionCode` 객체를 감쌉니다. 프로모션 코드와 연결된 쿠폰을 조회하려면 `coupon` 메서드를 호출하면 됩니다.

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

쿠폰 인스턴스를 사용하여 할인 금액 및 쿠폰이 고정 할인 쿠폰인지, 비율 할인 쿠폰인지를 확인할 수 있습니다.

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

현재 고객이나 구독에 적용된 할인(Discounts)도 조회할 수 있습니다.

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```

반환되는 `Laravel\Cashier\Discount` 인스턴스는 내부적으로 Stripe의 `Discount` 객체 인스턴스를 감쌉니다. 해당 할인에 연결된 쿠폰을 조회하려면 아래와 같이 합니다.

```php
$coupon = $subscription->discount()->coupon();
```

신규 쿠폰 또는 프로모션 코드를 고객 또는 구독에 적용하고 싶다면, `applyCoupon` 또는 `applyPromotionCode` 메서드를 이용하면 됩니다.

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

Stripe에서 발급한 프로모션 코드의 API ID를 반드시 사용해야 하며, 고객용 프로모션 코드 자체가 아님을 유의하세요. 고객이나 구독에는 한 번에 하나의 쿠폰 또는 프로모션 코드만 적용할 수 있습니다.

이 내용에 대한 자세한 정보는 Stripe 공식 문서를 참고하시기 바랍니다: [쿠폰 공식 문서](https://stripe.com/docs/billing/subscriptions/coupons), [프로모션 코드 공식 문서](https://stripe.com/docs/billing/subscriptions/coupons/codes).

<a name="adding-subscriptions"></a>
#### 구독 추가

기본 결제 수단을 이미 가지고 있는 고객에게 구독을 추가하고 싶다면, 구독 빌더 인스턴스에서 `add` 메서드를 호출하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 직접 구독 생성

Stripe 대시보드에서 직접 구독을 생성할 수도 있습니다. 이 경우 Cashier는 새로 생성된 구독을 동기화하고 구독 타입을 `default`로 지정합니다. 대시보드에서 생성된 구독에 할당된 타입을 변경하고 싶다면, [Webhook 이벤트 핸들러 등록](#defining-webhook-event-handlers)을 참고하세요.

단, Stripe 대시보드를 통해서는 한 가지 타입의 구독만 생성 가능합니다. 애플리케이션에서 여러 타입의 구독을 제공한다면 대시보드를 통해서는 한 타입만 추가할 수 있습니다.

또한, 반드시 애플리케이션에서 제공하는 각 구독 타입별로 한 명의 사용자가 단 하나의 활성 구독만 가질 수 있도록 관리해야 합니다. 만약 한 고객이 `default` 타입의 구독을 2개 보유하게 되면, Cashier는 데이터베이스 동기화 이후 가장 최근에 추가된 구독을 사용합니다(두 구독 모두 DB에는 저장되나 실제 결제에 사용되는 것은 최신 구독입니다).

<a name="checking-subscription-status"></a>
### 구독 상태 확인

고객이 애플리케이션을 구독하면 여러 편리한 메서드를 통해 구독 상태를 쉽게 확인할 수 있습니다. 먼저, `subscribed` 메서드는 고객이 활성 구독을 가지고 있을 때(체험 기간 포함) `true`를 반환합니다. 이 메서드는 첫 번째 인수로 구독의 타입을 받습니다.

```php
if ($user->subscribed('default')) {
    // ...
}
```

`subscribed` 메서드는 [라우트 미들웨어](/docs/12.x/middleware)로도 사용할 수 있으므로, 사용자의 구독 상태에 따라 라우트, 컨트롤러 접근을 제어할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```

사용자가 체험 기간(trial)에 있는지 확인하려면 `onTrial` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 체험 기간 중임을 사용자에게 알리는 경고를 표시할 때 유용합니다.

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```

구독자가 Stripe의 특정 제품(product)에 가입되어 있는지 확인하려면 `subscribedToProduct` 메서드를 사용할 수 있습니다. Stripe에서 제품은 가격(price)들의 모음입니다. 아래 예시에서는 사용자의 `default` 구독이 애플리케이션의 "premium" 제품에 가입되어 있는지 확인합니다. 전달하는 Stripe 제품 식별자는 Stripe 대시보드에 있는 제품 중 하나여야 합니다.

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```

배열을 전달하면 `default` 구독이 "basic" 또는 "premium" 제품에 가입되어 있는지 확인할 수도 있습니다.

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```

구독의 가격(price) 식별자로 구독 여부를 확인하려면 `subscribedToPrice` 메서드를 사용할 수 있습니다.

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```

`recurring` 메서드는 사용자가 현재 활성 구독 중이며 체험 기간을 벗어난 상태인지를 판단합니다.

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```

> [!WARNING]
> 동일한 타입의 구독을 두 개 이상 보유한 경우, `subscription` 메서드는 항상 가장 최근 구독 인스턴스를 반환합니다. 예를 들어, 한 사용자가 `default` 타입의 구독을 2개 가지고 있다면, 하나는 오래된 만료 구독이고 다른 하나는 현재 활성 구독일 수 있습니다. 이 경우 Cashier는 최신 구독을 반환하며, 이전 구독 정보는 과거 이력용으로 데이터베이스에 남아 있습니다.

<a name="cancelled-subscription-status"></a>
#### 구독 취소 상태

사용자가 한때 활성 구독자였으나 구독을 취소한 이력이 있는지 확인하려면 `canceled` 메서드를 사용하세요.

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```

사용자가 구독을 취소했지만 "유예 기간"(grace period)이 남아 있을 수도 있습니다. 예를 들어, 사용자가 3월 5일에 구독을 취소하였고 만료일이 3월 10일이었다면, 3월 10일까지가 유예 기간입니다. 이 기간에도 `subscribed` 메서드는 계속 `true`를 반환합니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

구독을 취소했고 더 이상 유예 기간이 남아 있지 않은지도 `ended` 메서드로 확인할 수 있습니다.

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```

<a name="incomplete-and-past-due-status"></a>
#### 결제 미완료 및 연체 상태

구독 생성 후 추가 결제 조치가 필요한 경우, 해당 구독의 상태가 `incomplete`로 표시됩니다. 구독 상태 정보는 Cashier의 `subscriptions` 데이터베이스 테이블의 `stripe_status` 컬럼에 저장됩니다.

마찬가지로, 가격 변경(swap) 시 추가 결제 조치가 필요한 경우 구독 상태가 `past_due`로 변경됩니다. 이러한 상태에서는 고객이 결제를 완료하기 전까지 구독이 활성화되지 않습니다. 구독에 미완료 결제가 존재하는지 확인하려면 billable 모델 또는 구독 인스턴스의 `hasIncompletePayment` 메서드를 사용하면 됩니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

구독에 미완결 결제가 있다면, 고객을 Cashier의 결제 확인 페이지로 안내하고, `latestPayment` 식별자를 전달해야 합니다. 구독 인스턴스의 `latestPayment` 메서드를 통해 이 식별자를 가져올 수 있습니다.

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

`past_due` 또는 `incomplete` 상태에서도 구독이 활성 상태로 간주되길 원한다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 보통 이 메서드들은 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출합니다.

```php
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
> 구독이 `incomplete` 상태인 경우, 결제가 완료되기 전까지 가격 변경(swap)이나 수량 변경(updateQuantity) 등 일부 작업을 할 수 없습니다. 따라서 `swap` 및 `updateQuantity` 메서드는 구독이 `incomplete` 상태일 때 예외를 던집니다.

<a name="subscription-scopes"></a>
#### 구독 상태별 조회(스코프)

대부분의 구독 상태는 쿼리 스코프로도 제공되므로, 특정 상태의 구독만 데이터베이스에서 손쉽게 조회할 수 있습니다.

```php
// 모든 활성 구독 가져오기...
$subscriptions = Subscription::query()->active()->get();

// 사용자의 취소된 구독 전부 가져오기...
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 전체 스코프 목록은 아래와 같습니다.

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
### 가격 변경(Swap)

고객이 애플리케이션에 구독한 이후에 다른 구독 가격으로 변경하고 싶을 때가 있습니다. Stripe의 price 식별자를 `swap` 메서드에 전달하여 고객 구독 가격을 변경할 수 있습니다. 가격 변경 시에는 기존 구독이 취소된 상태여도 다시 활성화되는 것으로 간주됩니다. 전달한 price 식별자는 Stripe 대시보드에 등록된 가격 식별자와 일치해야 합니다.

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

고객이 체험(trial) 기간 중이라면, 기존 체험 기간이 그대로 유지됩니다. 또한, 구독에 "수량(quantity)"이 지정되어 있다면 해당 수량도 그대로 유지됩니다.

가격을 변경할 때 현 체험 기간을 취소하고 즉시 전환하고 싶다면 `skipTrial` 메서드를 사용하세요.

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```

가격을 변경함과 동시에 다음 결제 주기를 기다리지 않고 즉시 인보이스를 발급하려면 `swapAndInvoice` 메서드를 활용하세요.

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 일할 계산(Proration)

기본적으로 Stripe는 가격 변경(swap) 시 비용을 일할 계산(프로레이션)합니다. 일할 계산 없이 구독 가격만 변경하려면 `noProrate` 메서드를 사용할 수 있습니다.

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```

구독 일할 계산에 대한 더 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/billing/subscriptions/prorations)를 참조하세요.

> [!WARNING]
> `swapAndInvoice` 메서드 전에 `noProrate`를 호출해도 일할 계산에 영향이 없습니다. 이 경우 인보이스가 항상 발급됩니다.

<a name="subscription-quantity"></a>
### 구독 수량(Quantity)

일부 구독은 "수량"에 따라 달라질 수 있습니다. 예를 들어, 프로젝트 관리 애플리케이션에서 프로젝트 1개당 월 $10씩 청구할 수 있습니다. `incrementQuantity`, `decrementQuantity` 메서드를 사용하면 구독 수량을 쉽게 늘리거나 줄일 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 현재 구독 수량에 5 추가...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 현재 구독 수량에서 5만큼 차감...
$user->subscription('default')->decrementQuantity(5);
```

특정 수량으로 바로 변경하려면 `updateQuantity` 메서드를 사용하세요.

```php
$user->subscription('default')->updateQuantity(10);
```

요금 변경 시 일할 계산 없이 수량만 업데이트하고 싶으면 `noProrate` 메서드를 함께 사용할 수 있습니다.

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```

구독 수량(Quantity)에 대한 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독의 수량(Quantity) 지정

[다중 상품 구독](#subscriptions-with-multiple-products)의 경우, 수량을 증가/감소시키고자 하는 가격의 ID를 `increment`/`decrement` 메서드의 두 번째 인수로 전달해야 합니다.

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독

[다중 상품 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)을 사용하면, 하나의 구독에 여러 결제 상품을 할당할 수 있습니다. 예를 들어, $10/월의 기본 구독에 $15/월 라이브 채팅 부가 상품을 추가하는 헬프데스크 형태의 고객 지원 애플리케이션을 만들 수 있습니다. 이런 다중 상품 구독 정보는 Cashier의 `subscription_items` 테이블에 저장됩니다.

여러 상품을 지정하려면, `newSubscription` 메서드의 두 번째 인수로 가격 배열을 전달하세요.

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

위 예시에서는 "default" 구독에 두 개의 가격이 연결되어 각각의 결제 주기대로 함께 청구됩니다. 필요하다면 `quantity` 메서드를 이용해 각 결제 상품별 수량을 개별로 지정할 수도 있습니다.

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 추가 가격을 더하고 싶다면 `addPrice` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

위 예시는 새 가격이 추가되어, 다음 결제 주기에 해당 금액이 청구됩니다. 고객에게 즉시 청구하고 싶으면 `addPriceAndInvoice`를 사용합니다.

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

특정 수량을 지정해 가격을 추가하고자 한다면, 두 번째 인수로 수량을 넘기세요.

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

구독에서 가격을 제거하려면 `removePrice` 메서드를 사용하면 됩니다.

```php
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독의 마지막 가격은 삭제할 수 없습니다. 구독을 아예 취소해야 합니다.

<a name="swapping-prices"></a>
#### 가격 스왑(Swapping)

다중 상품 구독에서도 연결된 가격들을 변경할 수 있습니다. 예를 들어, 고객이 `price_basic` 구독에 `price_chat` 추가 상품이 있는 상태에서, 기본 구독을 `price_basic`에서 `price_pro`로 업그레이드하고 싶다면 다음과 같이 할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

위의 예제를 실행하면, 기존 `price_basic` 항목이 삭제되고, `price_chat` 항목은 그대로 유지되며, 새롭게 `price_pro` 항목이 추가됩니다.

가격별로 옵션을 지정해야 할 때에는, 가격 식별자를 key로 하고 관련 옵션을 value로 하여 배열 형태로 전달할 수 있습니다. 예를 들어 구독 가격별 수량을 개별로 지정하려면 아래와 같이 할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

하나의 가격만 다른 것으로 바꾸고 싶다면, 구독 아이템 자체의 `swap` 메서드를 사용하면 됩니다. 이 방식은 구독의 다른 가격에 입력된 메타데이터가 모두 그대로 유지되기 때문에 유용합니다.

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```

<a name="proration"></a>

#### 비례 배분(Proration)

기본적으로 Stripe는 여러 상품이 포함된 구독에서 가격을 추가하거나 제거할 때 자동으로 비용을 비례 배분하여 처리합니다. 만약 비례 배분 없이 가격을 조정하고 싶다면, 가격 연산에 `noProrate` 메서드를 체이닝하여 사용해야 합니다.

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량(Quantities)

개별 구독 가격의 수량을 업데이트하고 싶다면, 기존의 [수량 메서드](#subscription-quantity)에 가격의 ID를 추가 인수로 전달하여 사용할 수 있습니다.

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 하나의 구독에 여러 가격이 있으면 `Subscription` 모델의 `stripe_price`와 `quantity` 속성은 `null`이 됩니다. 개별 가격의 속성에 접근하려면 `Subscription` 모델에 있는 `items` 연관관계를 사용해야 합니다.

<a name="subscription-items"></a>
#### 구독 아이템(Subscription Items)

하나의 구독에 여러 가격이 존재할 경우, 데이터베이스의 `subscription_items` 테이블에 여러 개의 구독 "아이템"이 저장됩니다. 이런 아이템들은 구독의 `items` 연관관계를 통해 접근할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// 특정 아이템의 Stripe 가격과 수량 가져오기...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

`findItemOrFail` 메서드를 이용해 특정 가격의 아이템을 직접 조회할 수도 있습니다.

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 다중 구독(Multiple Subscriptions)

Stripe는 고객이 동시에 여러 개의 구독을 가질 수 있도록 지원합니다. 예를 들어, 헬스장 서비스를 운영한다면 수영 구독과 웨이트 구독을 각각 따로 제공하고, 구독별로 요금제를 다르게 책정할 수 있습니다. 물론 고객은 한 가지 또는 두 가지 플랜 모두에 가입할 수 있습니다.

애플리케이션에서 구독을 생성할 때에는 `newSubscription` 메서드에 구독의 타입을 지정할 수 있습니다. 타입은 사용자가 가입하려는 구독을 구분할 수 있는 임의의 문자열이면 됩니다.

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

이 예시에서는 고객에게 월간 수영 구독을 시작했습니다. 하지만 나중에 연간 구독으로 변경하고 싶을 수도 있습니다. 이런 경우에는 해당 사용자의 `swimming` 구독에 대해 가격을 간단히 교체할 수 있습니다.

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```

물론, 구독을 완전히 취소하는 것도 가능합니다.

```php
$user->subscription('swimming')->cancel();
```

<a name="usage-based-billing"></a>
### 사용량 기반 과금(Usage Based Billing)

[사용량 기반 과금](https://stripe.com/docs/billing/subscriptions/metered-billing)은 고객이 주기적으로 사용하는 상품이나 서비스의 사용량에 따라 비용을 청구할 수 있게 해줍니다. 예를 들어, 한 달 동안 전송한 문자 메시지 수나 이메일 건수에 따라 요금을 책정할 수 있습니다.

사용량 기반 과금 기능을 사용하려면 먼저 Stripe 대시보드에서 [사용량 기반 과금 모델](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide)이 적용된 새 상품을 만들고, [미터(meter)](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter)를 생성해야 합니다. 미터를 생성한 후, 사용량 보고 및 조회에 필요한 이벤트 이름과 미터 ID를 저장합니다. 그런 다음, `meteredPrice` 메서드를 사용해 미터 가격 ID를 고객의 구독에 추가할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

또한 [Stripe Checkout](#checkout)을 통해서도 미터 기반 구독을 시작할 수 있습니다.

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
#### 사용량 보고(Reporting Usage)

고객이 애플리케이션을 사용할 때, 정확한 요금 청구를 위해 Stripe에 사용량을 보고해야 합니다. 미터 이벤트의 사용량을 보고하려면 `Billable` 모델에서 `reportMeterEvent` 메서드를 사용합니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```

기본적으로 "사용량 수량" 1이 결제 주기에 추가됩니다. 고객의 해당 결제 주기에 더 많은 "사용량"을 추가하고 싶을 때는 구체적인 수치를 명시할 수도 있습니다.

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```

고객의 특정 미터에 대한 이벤트 요약을 조회하려면, `Billable` 인스턴스의 `meterEventSummaries` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value // 10
```

미터 이벤트 요약에 대한 자세한 내용은 Stripe의 [Meter Event Summary 오브젝트 문서](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참고하세요.

[모든 미터를 나열](https://docs.stripe.com/api/billing/meter/list)하려면, `Billable` 인스턴스의 `meters` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->meters();
```

<a name="subscription-taxes"></a>
### 구독 세금(Subscription Taxes)

> [!WARNING]
> 세율(Tax Rate)을 직접 계산하는 대신, [Stripe Tax를 통해 세금을 자동 계산하는 기능](#tax-configuration)도 사용할 수 있습니다.

사용자가 구독 시 납부할 세율을 명시하려면, 청구(billable) 모델에 `taxRates` 메서드를 구현하고, Stripe에서 정의한 세율 ID를 문자열 배열로 반환해야 합니다. 이 세율은 [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 정의할 수 있습니다.

```php
/**
 * 고객의 구독에 적용할 세율 목록을 반환합니다.
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```

`taxRates` 메서드를 사용하면 국가별, 지역별로 다른 세율을 고객 단위로 동적으로 적용할 수 있어 글로벌 서비스를 운영할 때 매우 유용합니다.

만약 여러 상품을 포함하는 구독을 제공한다면, 각 가격별로 별도의 세율을 적용하는 `priceTaxRates` 메서드도 구현할 수 있습니다.

```php
/**
 * 각 가격별로 고객의 구독에 적용할 세율을 정의합니다.
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
> `taxRates` 메서드는 구독 청구에만 적용됩니다. 만약 Cashier를 사용해 "일회성" 결제를 처리한다면, 별도로 세율을 직접 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화(Syncing Tax Rates)

`taxRates` 메서드에서 반환하는 하드코딩된 세율 ID가 변경되어도, 기존 사용자의 구독 세팅에는 그대로 유지됩니다. 이미 생성된 구독의 세율을 새롭게 적용한 `taxRates` 값으로 동기화하려면, 해당 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출하면 됩니다.

```php
$user->subscription('default')->syncTaxRates();
```

이 동작은 여러 상품이 포함된 구독의 각 아이템 세율도 함께 동기화합니다. 만약 여러 상품 구독을 제공한다면, 꼭 앞서 소개한 `priceTaxRates` 메서드를 billable 모델에 구현했는지 확인해야 합니다.

<a name="tax-exemption"></a>
#### 세금 면제(Tax Exemption)

Cashier는 고객이 세금 면제 대상인지 확인하기 위한 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드도 제공합니다. 이 메서드들은 Stripe API를 호출해서 고객의 세금 면제 여부를 확인합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> 이 메서드들은 모든 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있습니다. 단, Invoice 객체에서 호출하면 송장이 생성된 시점의 면제 상태를 반환합니다.

<a name="subscription-anchor-date"></a>
### 구독 고정 일자(Subscription Anchor Date)

기본적으로 구독의 결제 주기는 구독 생성일, 또는 체험 기간이 있다면 체험이 종료되는 날짜를 기준(anchor)으로 시작합니다. 만약 계산 기준 일자를 직접 지정하고 싶다면, `anchorBillingCycleOn` 메서드를 사용할 수 있습니다.

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

구독 결제 주기(anchor) 관리에 대한 더 자세한 안내는 [Stripe 결제 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소(Cancelling Subscriptions)

구독을 취소하려면 사용자의 구독 인스턴스에서 `cancel` 메서드를 호출합니다.

```php
$user->subscription('default')->cancel();
```

구독이 취소되면 Cashier는 `subscriptions` 테이블의 `ends_at` 컬럼 값을 자동으로 설정합니다. 이 컬럼은 `subscribed` 메서드의 반환값을 결정하는 기준이 됩니다.

예를 들어, 사용자가 3월 1일 구독을 취소했지만 실제로는 3월 5일에 종료되도록 예약되어 있다면, `subscribed` 메서드는 3월 5일까지 계속 `true`를 반환합니다. 이는 대부분의 서비스가 결제 주기 종료일까지 사용자를 계속 이용 가능하도록 허용하기 때문입니다.

사용자가 구독을 취소했으나 여전히 "유예 기간(grace period)"에 있는지 확인하려면 `onGracePeriod` 메서드를 사용할 수 있습니다.

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```

즉시 구독을 취소하고 싶다면 `cancelNow` 메서드를 호출합니다.

```php
$user->subscription('default')->cancelNow();
```

즉시 구독을 취소하면서, 남은 미청구 사용량 또는 새로운/보류 중인 비례청구 인보이스 항목까지 함께 청구하려면 `cancelNowAndInvoice` 메서드를 사용합니다.

```php
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점에 구독이 취소되게 하고 싶을 때는 다음과 같이 사용할 수 있습니다.

```php
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

마지막으로, 회원 모델을 삭제하기 전에 반드시 그 사용자의 구독부터 취소해 주어야 합니다.

```php
$user->subscription('default')->cancelNow();

$user->delete();
```

<a name="resuming-subscriptions"></a>
### 구독 재개(Resuming Subscriptions)

고객이 구독을 취소했지만 "유예 기간" 내에 다시 구독을 활성화(resume)하고 싶다면, 해당 구독 인스턴스에서 `resume` 메서드를 호출할 수 있습니다.

```php
$user->subscription('default')->resume();
```

고객이 구독을 취소한 후 만료 전(즉, 유예 기간 내) 다시 구독을 재개하면 즉시 요금이 청구되지 않습니다. 대신 구독이 재활성화되고 원래의 결제 주기 일정에 맞춰 다시 결제가 진행됩니다.

<a name="subscription-trials"></a>
## 구독 체험(Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 정보를 먼저 받는 경우

고객에게 체험 기간을 제공하면서 결제 수단 정보는 미리 받고 싶다면, 구독 생성 시 `trialDays` 메서드를 사용하세요.

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```

이 메서드는 데이터베이스의 구독 레코드에 체험 기간 종료일을 지정하고, 해당 종료일까지 고객에게 요금을 부과하지 않도록 Stripe에 지시합니다. Stripe 대시보드에서 가격별로 기본 체험 기간이 설정되어 있어도, `trialDays`를 사용하면 Cashier가 이를 덮어쓰게 됩니다.

> [!WARNING]
> 고객이 체험 기간이 끝나기 전에 구독을 취소하지 않으면, 곧바로 요금이 청구되므로 반드시 사용자가 체험 종료일을 명확히 안내받도록 하세요.

또한, `trialUntil` 메서드를 사용해 체험 기간 종료일을 `DateTime` 인스턴스로 지정할 수 있습니다.

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->addDays(10))
    ->create($paymentMethod);
```

사용자가 체험 기간 내에 있는지 확인하려면 유저 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드를 사용합니다(아래 두 예시는 동일한 결과를 줍니다).

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```

`endTrial` 메서드를 사용하면 구독의 체험을 즉시 종료할 수도 있습니다.

```php
$user->subscription('default')->endTrial();
```

기존 체험 기간이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용하세요.

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 체험 일수 정의

Stripe 대시보드에서 가격별로 체험 기간(일수)을 직접 지정하거나, 항상 Cashier에서 명시적으로 지정할 수도 있습니다. Stripe 대시보드에서 체험 일수를 정의했다면 신규 구독(과거 구독 이력이 있는 고객이 다시 구독할 때 포함)에도 무조건 체험 기간이 적용됩니다. 체험 기간을 건너뛰려면 `skipTrial()` 메서드를 반드시 호출해야 합니다.

<a name="without-payment-method-up-front"></a>
### 결제 수단 정보를 먼저 받지 않는 경우

결제 수단 정보를 받지 않고 체험 기간을 제공하려면, 사용자 레코드의 `trial_ends_at` 컬럼에 원하는 체험 종료일을 저장하면 됩니다. 이는 대개 회원가입 시 자동으로 처리합니다.

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]
> `trial_ends_at` 속성에는 [날짜 캐스팅](/docs/12.x/eloquent-mutators#date-casting)을 billable 모델에서 지정해야 합니다.

Cashier에서는 이런 형태의 체험을 "일반 체험(generic trial)"이라고 부릅니다. 구독과는 직접 연결되지 않은 체험입니다. billable 모델 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 이전이면 `true`를 반환합니다.

```php
if ($user->onTrial()) {
    // 사용자가 체험 기간 내에 있습니다...
}
```

이후 실제 구독을 생성할 준비가 되었다면 일반적으로 `newSubscription` 메서드를 사용하면 됩니다.

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

사용자의 체험 종료일을 확인하려면 `trialEndsAt` 메서드를 사용할 수 있습니다. 사용자가 체험 중이라면 Carbon 날짜 인스턴스를 반환하고, 체험이 아니면 `null`을 반환합니다. 기본이 아닌 특정 구독의 체험 종료일이 필요하다면 인수로 구독 타입을 넘길 수 있습니다.

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

특히 "일반(generic) 체험" 기간에 있고 아직 구독을 생성하지 않은 상태인지 확인하려면, `onGenericTrial` 메서드를 사용할 수 있습니다.

```php
if ($user->onGenericTrial()) {
    // 사용자가 현재 "일반(generic) 체험" 기간입니다...
}
```

<a name="extending-trials"></a>
### 체험 기간 연장(Extending Trials)

`extendTrial` 메서드를 사용하면 구독이 생성된 이후에도 체험 기간을 연장할 수 있습니다. 이미 체험이 만료되어 정기 과금이 시작된 경우라도 추가 체험을 제공할 수 있습니다. 체험 기간에 추가된 시간은 다음 청구서에서 차감됩니다.

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 지금부터 7일 뒤로 체험 기간 종료...
$subscription->extendTrial(
    now()->addDays(7)
);

// 체험 기간에 5일 추가...
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe Webhook 처리

> [!NOTE]
> 로컬 개발 환경에서 [Stripe CLI](https://stripe.com/docs/stripe-cli)를 이용해 Webhook 테스트를 쉽게 할 수 있습니다.

Stripe는 Webhook을 통해 다양한 이벤트를 애플리케이션에 알려줍니다. 기본적으로 Cashier 서비스 프로바이더가 Cashier의 Webhook 컨트롤러를 가리키는 라우트를 자동으로 등록합니다. 이 컨트롤러가 들어오는 모든 Webhook 요청을 처리합니다.

기본적으로 Cashier의 Webhook 컨트롤러는 Stripe 설정에 따라 실패 결제가 누적된 구독 취소, 고객 정보 변경, 고객 삭제, 구독 정보 변경, 결제 수단 변경 등 여러 Stripe 이벤트를 자동 처리합니다. 추가로 원하는 Webhook 이벤트가 있다면 컨트롤러를 확장하여 원하는 이벤트도 처리할 수 있습니다.

Stripe Webhook 처리를 지원하려면 Stripe 관리 패널에서 Webhook URL을 올바르게 설정해야 합니다. 기본적으로 Cashier의 Webhook 컨트롤러는 `/stripe/webhook` 경로에 응답합니다. Stripe 관리 패널에서 반드시 활성화해야 하는 Webhook 이벤트 목록은 다음과 같습니다.

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

편의를 위해 Cashier는 `cashier:webhook` 아티즌 명령어를 제공합니다. 이 명령어는 Cashier에 필요한 모든 이벤트를 Stripe에 등록합니다.

```shell
php artisan cashier:webhook
```

기본적으로 새로 생성된 Webhook은 `APP_URL` 환경 변수와 Cashier에 포함된 `cashier.webhook` 라우트로 지정됩니다. 다른 URL로 설정하려면 명령어 실행 시 `--url` 옵션을 사용할 수 있습니다.

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

Webhook 생성 시 사용되는 Stripe API 버전은 Cashier와 호환되는 Stripe 버전으로 자동 지정됩니다. 다른 버전을 사용하려면 `--api-version` 옵션을 추가합니다.

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

Webhook는 생성 직후 바로 활성화됩니다. 필요하다면 생성은 하지만 바로 활성화하지 않으려면 `--disabled` 옵션을 사용할 수 있습니다.

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Stripe Webhook 요청은 반드시 Cashier의 [Webhook 서명 검증](#verifying-webhook-signatures) 미들웨어를 통해 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>
#### Webhook과 CSRF 보호

Stripe Webhook은 Laravel의 [CSRF 보호](/docs/12.x/csrf)를 우회해야 합니다. 따라서, Stripe Webhook에 대해 CSRF 토큰 검증을 하지 않도록 애플리케이션의 `bootstrap/app.php` 파일에서 `stripe/*`를 제외 처리해야 합니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
    ]);
})
```

<a name="defining-webhook-event-handlers"></a>
### Webhook 이벤트 핸들러 정의

Cashier는 결제 실패에 의한 구독 취소 등 주요 Stripe Webhook 이벤트를 자동 처리합니다. 그러나 별도의 Webhook 이벤트 처리가 필요하다면 Cashier가 제공하는 다음 이벤트 리스너를 이용하면 됩니다.

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

이 두 이벤트는 Stripe Webhook 전체 페이로드(payload)를 포함합니다. 예를 들어, `invoice.payment_succeeded` Webhook을 처리하고 싶다면, 아래와 같이 [리스너](/docs/12.x/events#defining-listeners)를 등록할 수 있습니다.

```php
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Stripe Webhook 수신 핸들러.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // 이벤트 처리 로직 작성...
        }
    }
}
```

<a name="verifying-webhook-signatures"></a>
### Webhook 서명 검증(Verifying Webhook Signatures)

Webhook의 보안을 위해, [Stripe의 Webhook 서명](https://stripe.com/docs/webhooks/signatures) 기능을 사용하는 것이 좋습니다. Cashier는 Stripe Webhook 요청의 유효성 검증 미들웨어를 자동으로 포함하고 있습니다.

Webhook 검증을 활성화하려면 애플리케이션의 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수를 반드시 설정하세요. Webhook `secret` 값은 Stripe 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 결제(Single Charges)

<a name="simple-charge"></a>
### 간단 결제(Simple Charge)

고객에게 한 번만 금액을 청구하고 싶다면, Billable 모델 인스턴스에서 `charge` 메서드를 사용할 수 있습니다. 이때 [결제 수단 식별자](#payment-methods-for-single-charges)를 두 번째 인수로 전달해야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

`charge` 메서드는 세 번째 인수로 옵션 배열을 받을 수 있어, Stripe의 결제 생성에 사용할 다양한 옵션을 전달할 수 있습니다. 지원하는 옵션 목록은 [Stripe 공식 문서](https://stripe.com/docs/api/charges/create)에서 확인할 수 있습니다.

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

`charge` 메서드는 고객 또는 사용자가 아닌 경우에도 사용할 수 있습니다. 이렇게 하려면 Billable 모델의 새 인스턴스에서 바로 `charge` 메서드를 호출하면 됩니다.

```php
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

`charge` 메서드는 결제가 실패하면 예외(Exception)를 발생시킵니다. 결제가 성공하면, `Laravel\Cashier\Payment` 인스턴스가 반환됩니다.

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```

> [!WARNING]
> `charge` 메서드의 결제 금액은 애플리케이션에서 사용하는 통화의 최소 단위로 입력해야 합니다. 예를 들어 미국 달러라면, 금액을 센트(1달러 = 100센트) 단위로 지정해야 합니다.

<a name="charge-with-invoice"></a>
### 인보이스와 함께 결제(Charge With Invoice)

때로는 한 번의 결제를 하면서 고객에게 PDF 인보이스도 제공해야 할 때가 있습니다. 그럴 때는 `invoicePrice` 메서드를 사용하세요. 예를 들어, 고객에게 티셔츠 5벌을 인보이스로 청구하려면 다음과 같이 하면 됩니다.

```php
$user->invoicePrice('price_tshirt', 5);
```

이 인보이스는 즉시 사용자의 기본 결제 수단으로 결제됩니다. `invoicePrice`는 세 번째 인수로 옵션 배열을 받을 수 있습니다(인보이스 아이템용). 네 번째 인수도 배열로, 인보이스 자체의 설정 옵션을 전달할 수 있습니다.

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

`invoicePrice`과 비슷하게, `tabPrice` 메서드를 사용해 고객의 "탭"에 여러 인보이스 항목(최대 250개 인보이스 항목)을 추가한 뒤, 한 번에 청구(Invoicing)할 수도 있습니다. 예를 들어 티셔츠 5벌과 머그잔 2개를 함께 청구할 수 있습니다.

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

또는, `invoiceFor` 메서드를 사용해 고객의 기본 결제 수단으로 바로 "단일(one-off)" 청구를 할 수도 있습니다.

```php
$user->invoiceFor('One Time Fee', 500);
```

`invoiceFor` 메서드도 사용할 수 있지만, 가급적 미리 정의된 가격과 함께 `invoicePrice` 또는 `tabPrice`를 사용하는 것이 Stripe 대시보드에서 상품별 판매 데이터 분석에 유리합니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor` 메서드는 Stripe 인보이스를 생성하며, 인보이스 결제 실패 시 자동 재시도합니다. 인보이스 결제 실패 시 재시도를 원하지 않는다면, Stripe API를 통해 첫 실패 후 인보이스를 직접 종료해야 합니다.

<a name="creating-payment-intents"></a>
### 결제 인텐트 생성(Creating Payment Intents)

`pay` 메서드를 Billable 모델 인스턴스에서 호출하면 Stripe 결제 인텐트(Payment Intent)를 새로 만들 수 있습니다. 이 결제 인텐트는 `Laravel\Cashier\Payment` 인스턴스에 래핑되어 반환됩니다.

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

결제 인텐트 생성 후, `client_secret` 값을 프론트엔드에 반환해 사용자가 브라우저에서 결제를 완료할 수 있도록 합니다. Stripe 결제 인텐트를 활용한 결제 플로우 전체 구현 방법은 [Stripe 공식 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참고하세요.

`pay` 메서드를 사용할 때 Stripe 대시보드에서 활성화된 모든 기본 결제 수단을 사용할 수 있습니다. 특정 결제 수단만 허용하고 싶으면 `payWith` 메서드를 사용하세요.

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
> `pay`, `payWith` 메서드의 결제 금액도 반드시 해당 통화의 최소 단위로 입력해야 합니다. 예를 들어, 미국 달러를 사용한다면 센트(1달러 = 100센트) 단위로 입력해야 합니다.

<a name="refunding-charges"></a>
### 결제 환불(Refunding Charges)

Stripe 결제를 환불해야 할 경우, `refund` 메서드를 사용하면 됩니다. 이 메서드는 [결제 인텐트 ID](#payment-methods-for-single-charges)를 첫 번째 인수로 받습니다.

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 인보이스(청구서)

<a name="retrieving-invoices"></a>
### 인보이스 조회

Billable 모델의 모든 인보이스를 간편하게 조회할 때는 `invoices` 메서드를 사용할 수 있습니다. 이 메서드는 `Laravel\Cashier\Invoice` 인스턴스의 컬렉션을 반환합니다.

```php
$invoices = $user->invoices();
```

결제 대기 중(pending)인 인보이스도 함께 조회하려면 `invoicesIncludingPending` 메서드를 사용하세요.

```php
$invoices = $user->invoicesIncludingPending();
```

`findInvoice` 메서드를 이용해 특정 ID의 인보이스를 직접 조회할 수도 있습니다.

```php
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>

#### 인보이스 정보 표시

고객의 인보이스 목록을 표시할 때는 인보이스 객체의 메서드를 활용하여 관련 정보를 보여줄 수 있습니다. 예를 들어, 사용자가 각 인보이스를 쉽게 다운로드할 수 있도록 테이블 형태로 인보이스 목록을 보여줄 수 있습니다.

```blade
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
### 예정된 인보이스 조회

고객의 예정된 인보이스를 조회하려면 `upcomingInvoice` 메서드를 사용할 수 있습니다.

```php
$invoice = $user->upcomingInvoice();
```

고객이 여러 구독을 가지고 있는 경우, 특정 구독의 예정 인보이스만 조회할 수도 있습니다.

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 인보이스 미리보기

`previewInvoice` 메서드를 활용하면 가격 변경 전에 인보이스가 어떻게 표시될지 미리 확인할 수 있습니다. 이를 통해 고객의 인보이스가 가격 변경 시 어떻게 보일지 알 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

`previewInvoice` 메서드에 여러 가격을 배열로 전달하면, 여러 가지 신규 가격이 적용된 인보이스도 미리 확인할 수 있습니다.

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 인보이스 PDF 생성

인보이스 PDF를 생성하기 전에, Cashier에서 기본적으로 사용하는 인보이스 렌더러인 Dompdf 라이브러리를 Composer로 설치해야 합니다.

```shell
composer require dompdf/dompdf
```

라우트나 컨트롤러에서 `downloadInvoice` 메서드를 사용하면 지정한 인보이스의 PDF 파일 다운로드를 쉽게 처리할 수 있습니다. 이 메서드는 인보이스 다운로드에 필요한 적절한 HTTP 응답을 자동으로 생성합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

기본적으로 인보이스의 모든 데이터는 Stripe에 저장된 고객 및 인보이스 데이터를 기반으로 합니다. 파일 이름은 `app.name` 설정 값이 기준이 됩니다. 하지만, 두 번째 인자로 배열을 전달하여 회사명, 제품 정보 등 일부 데이터를 커스터마이징할 수 있습니다.

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

또한, 세 번째 인자로 파일명을 지정할 수 있으며, 지정한 파일명 뒤에는 `.pdf` 확장자가 자동으로 붙습니다.

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 인보이스 렌더러

Cashier에서는 커스텀 인보이스 렌더러도 사용할 수 있습니다. 기본적으로 Cashier는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 활용하는 `DompdfInvoiceRenderer` 구현체를 사용합니다. 하지만, 원하는 어떤 렌더러라도 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하면 사용할 수 있습니다. 예를 들어, 외부 PDF 렌더링 API를 호출해 인보이스 PDF를 생성할 수도 있습니다.

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * Render the given invoice and return the raw PDF bytes.
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

이렇게 커스텀 렌더러를 구현했다면, 애플리케이션의 `config/cashier.php` 설정 파일에서 `cashier.invoices.renderer` 값을 커스텀 렌더러 클래스명으로 변경해 주어야 합니다.

<a name="checkout"></a>
## 체크아웃(Checkout)

Cashier Stripe는 [Stripe Checkout](https://stripe.com/payments/checkout) 기능도 지원합니다. Stripe Checkout을 이용하면 결제 처리를 위한 커스텀 페이지를 직접 만들 필요 없이, 미리 만들어진 Stripe의 호스팅 결제 페이지를 바로 사용할 수 있습니다.

아래 문서에서는 Cashier와 Stripe Checkout을 함께 사용하는 방법을 안내합니다. Stripe Checkout에 대해 더 자세히 알고 싶다면 [Stripe 공식 Checkout 문서](https://stripe.com/docs/payments/checkout)도 참고해 보시기 바랍니다.

<a name="product-checkouts"></a>
### 상품 결제

Stripe 대시보드에서 이미 생성해둔 상품에 대한 결제를 수행하려면, Billable 모델에서 `checkout` 메서드를 사용하면 됩니다. 이 메서드는 새로운 Stripe Checkout 세션을 시작합니다. 기본적으로 Stripe Price ID를 인수로 전달해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

필요하다면 상품의 수량도 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

고객이 이 경로에 접근하면 Stripe의 Checkout 페이지로 리디렉션됩니다. 기본적으로 구매가 성공하거나 취소되면 사용자는 애플리케이션의 `home` 라우트로 리디렉션됩니다. 하지만, `success_url`과 `cancel_url` 옵션을 사용해 별도의 콜백 URL을 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

`success_url` 옵션을 지정할 때, Stripe가 해당 URL로 이동할 때 체크아웃 세션 ID를 쿼리 스트링 파라미터로 추가하도록 할 수도 있습니다. 이를 위해 `success_url`의 쿼리 스트링에 `{CHECKOUT_SESSION_ID}` 문자열을 그대로 넣으면, Stripe가 이 자리에서 실제 체크아웃 세션 ID로 대체해 전달합니다.

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

기본적으로 Stripe Checkout에서는 [사용자가 직접 사용할 수 있는 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)가 비활성화되어 있습니다. 다행히도, 간단하게 이 기능을 활성화할 수 있는데, `allowPromotionCodes` 메서드를 호출하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 단일 결제(즉석 상품 결제)

Stripe 대시보드에 상품으로 등록하지 않은 즉석 상품에 대한 간단한 결제를 처리할 수도 있습니다. 이 경우 Billable 모델에서 `checkoutCharge` 메서드를 사용하여 결제 금액, 상품 이름, 필요하다면 수량을 전달합니다. 고객이 이 경로에 접근하면 마찬가지로 Stripe Checkout 페이지로 이동합니다.

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 메서드를 사용할 경우, Stripe에서는 항상 새 상품과 가격(price)이 Stripe 대시보드에 생성됩니다. 따라서, 되도록 미리 Stripe 대시보드에서 상품을 생성하고 `checkout` 메서드를 사용하는 것이 좋습니다.

<a name="subscription-checkouts"></a>
### 구독 체크아웃

> [!WARNING]
> Stripe Checkout을 구독에 사용하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅(webhook)을 활성화해야 합니다. 이 웹훅을 통해 데이터베이스에 구독 레코드를 생성하고 관련 구독 항목들을 저장합니다.

Stripe Checkout을 사용하여 구독을 시작할 수도 있습니다. Cashier의 subscription builder 메서드로 구독을 정의한 후, `checkout` 메서드를 호출하면 됩니다. 고객이 이 경로에 접근하면 Stripe Checkout 페이지로 리디렉션됩니다.

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

상품 결제와 마찬가지로, 성공 및 취소 시 리디렉션될 URL을 커스터마이징할 수 있습니다.

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

당연히 구독 결제에도 프로모션 코드를 활성화할 수 있습니다.

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
> Stripe Checkout에서는 구독 시작 단계에서 모든 구독 청구 옵션을 사용할 수 있는 것은 아닙니다. 예를 들어, subscription builder에서 `anchorBillingCycleOn` 메서드를 사용하거나, 청구 비례(proration) 설정, 결제 처리 방식 설정(payment behavior)은 Stripe Checkout 세션에서는 반영되지 않습니다. 사용 가능한 파라미터 목록은 [Stripe Checkout Session API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout과 체험(Trial) 기간

Stripe Checkout을 이용해 구독을 생성할 때도 체험(Trial) 기간을 설정할 수 있습니다.

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

단, Stripe Checkout에서 지원하는 체험 기간의 최소 값은 48시간이므로, trial 기간은 반드시 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독과 웹훅

Stripe와 Cashier는 웹훅을 통해 구독 상태를 업데이트합니다. 따라서 고객이 결제 정보를 입력하고 애플리케이션으로 돌아왔을 때 구독이 아직 활성화되지 않았을 가능성이 있습니다. 이러한 상황을 처리하려면 사용자에게 결제 또는 구독이 보류 중(pending)이라는 안내 메시지를 표시하는 것이 좋습니다.

<a name="collecting-tax-ids"></a>
### 세금 식별 번호(Tax ID) 수집

Checkout은 고객의 세금 식별 번호(Tax ID)도 수집할 수 있습니다. 체크아웃 세션을 생성할 때 `collectTaxIds` 메서드를 호출하면 이 기능이 활성화됩니다.

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

이렇게 하면, 고객이 기업용 구매 여부를 선택할 수 있는 새로운 체크박스가 체크아웃 화면에 표시되며, 기업용 구매라면 Tax ID 입력란도 나타납니다.

> [!WARNING]
> 만약 이미 애플리케이션의 서비스 프로바이더에서 [자동 세금 수집](#tax-configuration) 기능을 설정한 경우, 이 기능이 자동으로 활성화되므로 `collectTaxIds` 메서드를 다시 호출할 필요는 없습니다.

<a name="guest-checkouts"></a>
### 비회원(Guest) 체크아웃

`Checkout::guest` 메서드를 통해, "계정"이 없는 애플리케이션의 방문자(비회원)에 대해서도 체크아웃 세션을 생성할 수 있습니다.

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

기존 사용자와 마찬가지로, `Laravel\Cashier\CheckoutBuilder` 인스턴스에서 제공되는 다양한 메서드를 활용하여 비회원 체크아웃 세션도 자유롭게 커스터마이징할 수 있습니다.

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

비회원 체크아웃이 완료되면 Stripe에서 `checkout.session.completed` 웹훅 이벤트를 전송할 수 있습니다. 따라서 반드시 [Stripe 웹훅을 애플리케이션에 연결](https://dashboard.stripe.com/webhooks)해 이 이벤트를 전달받을 수 있도록 설정해야 합니다. Stripe 대시보드에서 해당 웹훅을 활성화하면, [Cashier의 웹훅 처리](#handling-stripe-webhooks) 기능을 통해 이 이벤트를 처리할 수 있습니다. 웹훅 페이로드의 주요 객체는 [checkout object](https://stripe.com/docs/api/checkout/sessions/object)이므로, 이 객체를 확인하여 고객 주문을 처리하면 됩니다.

<a name="handling-failed-payments"></a>
## 결제 실패 처리

때때로 구독이나 단일 상품 결제가 실패할 수 있습니다. 이런 상황이 발생하면 Cashier는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 발생시켜 문제를 알립니다. 이 예외를 잡아서 처리할 때는 두 가지 방식을 선택할 수 있습니다.

첫 번째 방법은, Cashier에서 제공하는 결제 확인 전용 페이지로 사용자를 리디렉션하는 것입니다. 이 페이지는 Cashier의 서비스 프로바이더를 통해 이미 등록되어 있으므로, `IncompletePayment` 예외를 잡아 아래와 같이 결제 확인 페이지로 리디렉션할 수 있습니다.

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

결제 확인 페이지에서는 고객이 신용카드 정보를 다시 입력하거나 Stripe에서 요구하는 추가 작업(예: "3D Secure" 인증 등)을 진행하게 됩니다. 결제 확인이 끝나면 `redirect` 파라미터로 지정한 URL로 리디렉션되고, 해당 URL에는 `message`(문자열)와 `success`(정수) 쿼리 스트링 변수가 추가됩니다. 결제 페이지에서는 현재 다음과 같은 결제 방법을 지원합니다.

<div class="content-list" markdown="1">

- 신용카드(Credit Cards)
- Alipay
- Bancontact
- BECS 다이렉트 디빗(BECS Direct Debit)
- EPS
- Giropay
- iDEAL
- SEPA 다이렉트 디빗(SEPA Direct Debit)

</div>

두 번째 방법은 Stripe가 결제 확인을 대신하도록 맡기는 것입니다. 이 경우에는, 사용자를 결제 확인 페이지로 보내는 대신 Stripe 대시보드에서 [자동 청구 이메일](https://dashboard.stripe.com/account/billing/automatic) 설정을 활성화하면 됩니다. 다만, `IncompletePayment` 예외가 발생한 경우 사용자가 결제 안내 이메일을 받게 될 것이라는 메시지는 꼭 전해주어야 합니다.

결제 관련 예외는 `Billable` 트레이트를 사용하는 모델의 `charge`, `invoiceFor`, `invoice` 메서드 및 구독 연관 작업에서 있는 `SubscriptionBuilder`의 `create`, `Subscription`과 `SubscriptionItem`에서의 `incrementAndInvoice`, `swapAndInvoice`에서 발생할 수 있습니다.

기존 구독에 미완료 결제가 있는지 확인하려면 billable 모델 또는 구독 인스턴스의 `hasIncompletePayment` 메서드를 사용하면 됩니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```

특정 미완료 결제의 상세 상태는 예외 인스턴스의 `payment` 속성을 확인해 알 수 있습니다.

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 intent 상태를 확인합니다...
    $exception->payment->status;

    // 구체적인 조건별로 처리합니다...
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="confirming-payments"></a>
### 결제 확인

일부 결제 방식(SEPA 등)은 결제 확인을 위해 추가 데이터가 필요합니다. 예를 들어, SEPA 결제 방법은 결제 프로세스 중에 추가적인 mandate 데이터를 요구할 수 있습니다. 이 경우 Cashier에서 `withPaymentConfirmationOptions` 메서드를 사용해 이 데이터를 제공할 수 있습니다.

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

결제 확인에서 사용 가능한 모든 옵션은 [Stripe API 문서](https://stripe.com/docs/api/payment_intents/confirm)를 참고하세요.

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증(SCA)

비즈니스나 고객이 유럽에 있다면 EU의 SCA(Strong Customer Authentication, 강력한 고객 인증) 규정을 준수해야 합니다. 이 규정은 2019년 9월부터 유럽연합에서 결제 사기 방지를 위해 도입되었습니다. Stripe와 Cashier는 SCA 준수 애플리케이션 구축에 적합하게 준비되어 있습니다.

> [!WARNING]
> 시작하기 전에 [Stripe의 PSD2 및 SCA 가이드](https://stripe.com/guides/strong-customer-authentication)와 [SCA 관련 Stripe 문서](https://stripe.com/docs/strong-customer-authentication)를 먼저 확인하시기 바랍니다.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 인증이 필요한 결제

SCA 규정에 따르면 결제 시 추가 인증이 필요한 경우가 많습니다. 이럴 때 Cashier는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 던져서 추가 인증이 필요함을 알려줍니다. 해당 예외 처리 방법은 [결제 실패 처리](#handling-failed-payments) 문서를 참고하세요.

Stripe 또는 Cashier에서 제공하는 결제 확인 화면은 해당 은행 또는 카드사에 맞춘 인증 흐름을 따를 수 있으며, 카드 추가 인증, 소액 임시 결제, 별도 기기 인증 등 다양한 방식이 사용될 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체(past due) 상태

추가 결제 인증이 필요한 경우, 구독 상태는 `incomplete` 또는 `past_due`로 남아 있게 되며, 이는 데이터베이스의 `stripe_status` 컬럼에 기록됩니다. 결제가 완료되고 Stripe가 웹훅을 통해 완료를 알리면 Cashier가 자동으로 구독을 활성화합니다.

`incomplete` 및 `past_due` 상태에 대한 더 자세한 내용은 [별도 문서](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>
### 오프 세션 결제 알림

SCA 규정에 따라 활성화된 구독 상태에서도 때때로 결제 정보를 추가 확인해야 하는 상황이 발생할 수 있습니다(예: 구독 갱신 시). 이때 Cashier는 고객에게 결제 확인 알림을 이메일 등으로 발송할 수 있습니다. 알림을 활성화하려면 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수에 알림 클래스명을 지정하면 됩니다. 이 기능은 기본적으로 비활성화되어 있으며, Cashier가 제공하는 기본 알림 클래스를 쓸 수도 있고 직접 만들 수도 있습니다.

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

이 알림 기능이 잘 동작하려면 [Stripe 웹훅이 설정](#handling-stripe-webhooks)되어 있고, Stripe 대시보드에서 `invoice.payment_action_required` 웹훅도 활성화되어 있어야 합니다. 또한, `Billable` 모델에 Laravel의 `Illuminate\Notifications\Notifiable` 트레이트도 적용되어야 합니다.

> [!WARNING]
> 추가 인증이 필요한 결제를 고객이 직접 진행할 때도 알림이 전송될 수 있습니다. Stripe에서는 해당 결제가 수동(수기) 결제인지 오프세션 결제(off-session)인지를 구분하지 않기 때문입니다. 하지만 사용자가 이미 결제를 완료한 후 결제 페이지에 접속하면 "결제 성공(Payment Successful)" 메시지가 표시되고, 같은 결제로 두 번 결제되는 일은 발생하지 않습니다.

<a name="stripe-sdk"></a>
## Stripe SDK

Cashier의 많은 객체는 Stripe SDK 객체를 감싼 래퍼입니다. Stripe 객체에 직접 접근하고 싶다면, `asStripe` 메서드를 사용해 쉽게 해당 Stripe 객체를 가져올 수 있습니다.

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

또한, Stripe 구독을 직접 업데이트하려면 `updateStripeSubscription` 메서드를 사용하면 됩니다.

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Cashier` 클래스의 `stripe` 메서드를 호출하면, `Stripe\StripeClient` 인스턴스를 직접 활용할 수 있습니다. 예를 들어, 이 메서드를 이용해 Stripe 계정의 가격(Price) 목록을 조회할 수 있습니다.

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트

Cashier를 사용하는 애플리케이션을 테스트할 때는 Stripe API로 실제 HTTP 요청을 보내는 대신 이를 목(mock) 처리할 수도 있지만, 이 경우 Cashier의 내부 동작을 일부 재구현해야 하므로 권장하지 않습니다. 테스트가 느려질 수 있지만, Stripe의 실제 API를 테스트에서 사용하는 것이 애플리케이션이 정상적으로 동작하는지 더 확실히 검증할 수 있기 때문입니다. 이런 느린 테스트는 Pest나 PHPUnit에서 별도의 그룹으로 분리해 관리할 수 있습니다.

테스트 시에는 Cashier 자체의 테스트가 이미 충분히 잘 마련되어 있으므로, 자체적으로는 구독 및 결제 플로우만 집중해서 검증하면 됩니다. Cashier의 세부 동작 하나하나까지 모두 테스트할 필요는 없습니다.

먼저, 테스트를 위해 Stripe 시크릿의 **테스트** 버전을 `phpunit.xml` 파일에 추가합니다.

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

이제 테스트 코드에서 Cashier를 이용할 때 Stripe의 테스트 환경으로 실제 API 요청이 전송됩니다. 편의를 위해, 미리 Stripe 테스트 계정에 테스트에서 사용할 구독이나 가격 정보를 등록해 두는 것이 좋습니다.

> [!NOTE]
> 다양한 결제 시나리오(예: 신용카드 거절/실패 등)를 테스트하려면 Stripe에서 제공하는 다양한 [테스트 카드 번호 및 토큰](https://stripe.com/docs/testing)을 활용하실 수 있습니다.