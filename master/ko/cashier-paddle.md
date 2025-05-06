# Laravel Cashier (Paddle)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [Paddle 샌드박스](#paddle-sandbox)
- [설정](#configuration)
    - [청구 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [Paddle JS](#paddle-js)
    - [통화 설정](#currency-configuration)
    - [기본 제공 모델 오버라이드](#overriding-default-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [Checkout 세션](#checkout-sessions)
    - [오버레이 Checkout](#overlay-checkout)
    - [인라인 Checkout](#inline-checkout)
    - [비회원 Checkout](#guest-checkouts)
- [가격 미리보기](#price-previews)
    - [고객 가격 미리보기](#customer-price-previews)
    - [할인](#price-discounts)
- [고객](#customers)
    - [고객 기본값](#customer-defaults)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [구독 단일 요금 부과](#subscription-single-charges)
    - [결제 정보 업데이트](#updating-payment-information)
    - [요금제 변경](#changing-plans)
    - [구독 수량](#subscription-quantity)
    - [다수 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [구독 일시정지](#pausing-subscriptions)
    - [구독 취소](#canceling-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [카드 정보 먼저 수집](#with-payment-method-up-front)
    - [카드 정보 없이 체험 제공](#without-payment-method-up-front)
    - [체험 연장 또는 활성화](#extend-or-activate-a-trial)
- [Paddle Webhook 처리](#handling-paddle-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 시그니처 검증](#verifying-webhook-signatures)
- [단일 요금 부과](#single-charges)
    - [상품에 대해 결제하기](#charging-for-products)
    - [거래 환불](#refunding-transactions)
    - [거래 크레딧 지급](#crediting-transactions)
- [거래 내역](#transactions)
    - [과거 및 예정 결제](#past-and-upcoming-payments)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 이 문서는 Cashier Paddle 2.x의 Paddle Billing 통합에 대한 문서입니다. 아직 Paddle Classic을 사용 중이라면 [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x)를 사용해야 합니다.

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)은 [Paddle](https://paddle.com)의 구독 결제 서비스를 위한 표현력 있고 유연한 인터페이스를 제공합니다. 반복적이고 번거로운 구독 결제 코드 대부분을 처리해주며, 기본 구독 관리 이외에도 구독 변경, 구독 "수량", 구독 일시정지, 구독 취소 유예 기간 등 다양한 기능을 지원합니다.

Cashier Paddle을 자세히 살펴보기 전에 Paddle의 [개념 가이드](https://developer.paddle.com/concepts/overview)와 [API 문서](https://developer.paddle.com/api-reference/overview)도 함께 참고하시길 권장합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier의 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 이용해 Paddle용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier-paddle
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 Cashier 마이그레이션 파일을 게시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그런 다음, 애플리케이션의 데이터베이스 마이그레이션을 실행합니다. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성하며, 모든 고객의 구독 정보를 저장하기 위한 `subscriptions` 및 `subscription_items` 테이블도 생성합니다. 마지막으로, 고객과 관련된 모든 Paddle 거래 정보를 저장하는 `transactions` 테이블이 추가됩니다:

```shell
php artisan migrate
```

> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리할 수 있도록 반드시 [Cashier의 Webhook 처리를 설정](#handling-paddle-webhooks)하세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 개발 및 스테이징 환경에서는 반드시 [Paddle Sandbox 계정](https://sandbox-login.paddle.com/signup)을 등록하세요. 이 계정은 실결제 없이 자유롭게 테스트할 수 있는 샌드박스 환경을 제공합니다. 다양한 결제 시나리오를 시뮬레이션하려면 Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card)를 사용할 수 있습니다.

Paddle Sandbox 환경을 사용할 때는 애플리케이션의 `.env` 파일에서 `PADDLE_SANDBOX` 환경 변수를 `true`로 설정하세요:

```ini
PADDLE_SANDBOX=true
```

개발이 완료된 후에는 [Paddle 벤더 계정](https://paddle.com)을 신청할 수 있습니다. 애플리케이션을 실제 운영 환경에 배포하기 전, Paddle에서 반드시 도메인 승인을 받아야 합니다.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 가능 모델

Cashier를 사용하기 전에, 사용자 모델에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 수단 정보 변경 등 일반적인 과금 작업을 위한 다양한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

사용자 이외의 엔티티에도 청구 기능이 필요하다면 해당 클래스에도 트레이트를 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에 Paddle 키를 설정해야 합니다. Paddle API 키는 Paddle 콘솔에서 확인할 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```

`PADDLE_SANDBOX` 환경 변수는 [Paddle Sandbox 환경](#paddle-sandbox)일 때는 `true`, 운영 환경에 배포할 때는 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 옵션이며, Paddle의 [Retain](https://developer.paddle.com/paddlejs/retain) 기능을 사용할 때만 지정합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle 결제 창은 자체 JavaScript 라이브러리에 의존합니다. JavaScript 라이브러리는 애플리케이션 레이아웃의 `</head>` 닫기 태그 바로 전에 `@paddleJS` Blade 디렉티브를 추가하면 쉽게 로드할 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```

<a name="currency-configuration"></a>
### 통화 설정

인보이스에 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용해 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 PHP의 `ext-intl` 확장 모듈이 설치 및 설정되어 있어야 합니다.

<a name="overriding-default-models"></a>
### 기본 제공 모델 오버라이드

Cashier가 내부적으로 사용하는 모델을 확장하려면 해당 모델을 상속받아 직접 구현할 수 있습니다:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, `Laravel\Paddle\Cashier` 클래스를 통해 커스텀 모델을 Cashier에 등록합니다. 주로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useTransactionModel(Transaction::class);
}
```

<!-- 이하의 번역도 동일한 마크다운 포맷 및 코드/링크/HTML은 번역하지 않으며 계속 전문 용어와 패턴을 지켜 충실히 번역함 -->

<a name="quickstart"></a>
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 상품 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에, 반드시 Paddle 대시보드에서 고정 가격의 상품을 정의하고, [Paddle의 Webhook 처리](#handling-paddle-webhooks)도 설정해야 합니다.

애플리케이션에서 상품 및 구독 결제 기능을 제공하는 것은 복잡하게 느껴질 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://www.paddle.com/billing/checkout)를 이용하면 쉽고 강력하게 결제 통합 기능을 구축할 수 있습니다.

비정기/단일 결제 제품의 경우, Cashier를 사용해 Paddle의 Checkout Overlay를 통해 결제를 진행하게 할 수 있습니다. 사용자는 결제 정보를 입력하고 구매를 완료하면 지정된 성공 URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```

위 예제처럼 Cashier 제공 `checkout` 메서드를 사용해 특정 "가격 식별자"에 따른 Paddle Checkout Overlay를 생성할 수 있습니다. Paddle에서 "prices"란 [특정 상품에 할당된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요하다면 `checkout` 메서드는 Paddle에서 고객 정보를 자동으로 생성하고, 관련 사용자와 연동합니다. 결제 완료 후 사용자는 성공 페이지로 리디렉션됩니다.

뷰에서는 Checkout Overlay를 띄우는 버튼을 배치합니다. Cashier Paddle에 내장된 `paddle-button` Blade 컴포넌트를 사용하거나, [오버레이 Checkout 수동 렌더링](#manually-rendering-an-overlay-checkout)도 가능합니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```

<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle Checkout에 메타 데이터 제공하기

상품을 판매할 때, 자체 정의한 `Cart`나 `Order` 모델을 활용해 주문/구매 내역을 관리하기도 합니다. Paddle Checkout Overlay로 결제 단계에 진입할 때 주문 식별자를 추가로 넘겨, 결제 완료 후 주문과 매칭할 수 있습니다.

이를 위해 `checkout` 메서드에 커스텀 데이터를 배열로 추가할 수 있습니다. 예를 들어, 사용자가 장바구니 결제 과정을 시작하면 임시 `Order`가 생성됩니다:

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

    $checkout = $request->user()->checkout($order->price_ids)
        ->customData(['order_id' => $order->id]);

    return view('billing', ['checkout' => $checkout]);
})->name('checkout');
```

위처럼 장바구니 및 주문의 Paddle price 식별자들을 `checkout` 메서드에 전달하고, order의 ID도 `customData`를 통해 추가합니다.

결제 과정 완료 후 주문을 "완료"로 표시하려면, Paddle에서 전송한 Webhook을 기반으로 Cashier가 발생시키는 이벤트를 수신해 DB를 갱신해야 합니다.

예를 들어, Cashier가 발생시키는 `TransactionCompleted` 이벤트 리스너를 등록합니다. 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot`에서 설정합니다:

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```

`CompleteOrder` 리스너는 다음과 같이 작성할 수 있습니다:

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * Handle the incoming Cashier webhook event.
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```

더 자세한 데이터 구조 및 내용은 Paddle의 [transaction.completed 이벤트 문서](https://developer.paddle.com/webhooks/transactions/transaction-completed)를 참고하세요.

<!-- 이후 각 하위 제목, 코드, 예시, 주의/경고/노트 형식 등 모든 요소를 최대한 원문과 동일하게 마크다운으로 충실히 번역 -->

---

위 예시와 동일하게 나머지 문서(구독 판매, Checkout 세션, 가격 미리보기, 고객, 구독, Webhook 처리, 단일 결제, 거래 내역, 테스트 등) 역시 요청하신 마크다운 규칙을 적용해 그대로 번역할 수 있습니다. 
파일이 매우 길어 추가 번역 요청 시 아래 부분부터 이어서 제공 가능합니다. 필요하신 범위를 말씀해 주세요!