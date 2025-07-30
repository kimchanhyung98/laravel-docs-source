# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [데이터베이스 마이그레이션](#database-migrations)
- [설정](#configuration)
    - [빌러블 모델(Billable Model)](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용하기](#using-custom-models)
- [고객 (Customers)](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터 Stripe와 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단 (Payment Methods)](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [사용자 결제 수단 확인](#check-for-a-payment-method)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독 (Subscriptions)](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [측정 기반 과금 (Metered Billing)](#metered-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 청구 주기 기준일 설정](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험 (Trials)](#subscription-trials)
    - [결제 수단 입력 후 체험](#with-payment-method-up-front)
    - [결제 수단 없이 체험](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제 (Single Charges)](#single-charges)
    - [단순 결제](#simple-charge)
    - [청구서와 함께 결제](#charge-with-invoice)
    - [결제 인텐트 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [체크아웃 (Checkout)](#checkout)
    - [상품 체크아웃](#product-checkouts)
    - [단일 결제 체크아웃](#single-charge-checkouts)
    - [구독 체크아웃](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 체크아웃](#guest-checkouts)
- [청구서 (Invoices)](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [예정된 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [PDF 형태로 청구서 생성](#generating-invoice-pdfs)
- [실패한 결제 처리](#handling-failed-payments)
- [강력한 고객 인증 (SCA)](#strong-customer-authentication)
    - [추가 결제 확인 필요한 경우](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 Stripe의 구독 청구 서비스를 위한 표현력 있고 직관적인 인터페이스를 제공합니다. 반복적인 구독 청구 코드를 대신 처리해 주어 개발자의 부담을 줄여줍니다. 기본 구독 관리 외에도, 쿠폰 처리, 구독 전환, 구독 "수량", 취소 유예 기간, 청구서 PDF 생성 등 다양한 기능을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새 버전으로 업그레이드 할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 주의 깊게 확인해야 합니다.

> [!WARNING]
> 파괴적 변경을 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 14버전은 Stripe API 버전 `2022-11-15`를 사용합니다. Stripe API 버전은 새로운 기능 및 개선 사항에 맞춰 마이너 버전 업데이트 때 갱신됩니다.

<a name="installation"></a>
## 설치 (Installation)

우선 Composer 패키지 관리자를 통해 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier
```

> [!WARNING]
> Cashier가 Stripe 이벤트를 정상 처리하려면, 반드시 [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)을 반드시 해야 합니다.

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션 (Database Migrations)

Cashier의 서비스 프로바이더는 자체 마이그레이션 디렉터리를 등록합니다. 따라서 패키지 설치 후 반드시 데이터베이스 마이그레이션을 수행하세요. Cashier 마이그레이션은 `users` 테이블에 여러 칼럼을 추가하고, 고객 구독 정보를 담는 새로운 `subscriptions` 테이블을 만듭니다:

```shell
php artisan migrate
```

Cashier에 기본 탑재된 마이그레이션을 덮어쓰고 싶으면, `vendor:publish` 아티즌 명령어를 사용해 마이그레이션 파일을 공개할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

Cashier 마이그레이션을 아예 실행하지 않으려면 Cashier가 제공하는 `ignoreMigrations` 메서드를 호출하세요. 보통 `AppServiceProvider` 클래스의 `register` 메서드에서 호출합니다:

```
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 등록
 *
 * @return void
 */
public function register()
{
    Cashier::ignoreMigrations();
}
```

> [!WARNING]
> Stripe에서는 Stripe 식별자를 저장하는 칼럼에 대해 대소문자를 구분하는 정렬(collation) 설정을 권장합니다. MySQL 사용 시, `stripe_id` 칼럼에 `utf8_bin` 정렬을 반드시 설정하세요. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 빌러블 모델(Billable Model)

Cashier를 사용하기 전에, 구독 및 결제 관련 메서드를 사용할 `Billable` 트레이트를 빌러블 모델에 추가하세요. 보통 `App\Models\User` 모델이 여기에 해당합니다:

```
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 Laravel에서 제공하는 `App\Models\User` 클래스를 빌러블 모델로 간주합니다. 만약 다른 모델을 사용하려면 `useCustomerModel` 메서드를 통해 다른 모델 클래스를 지정할 수 있습니다. 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel 기본 `App\Models\User` 외 다른 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시하고 해당 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

애플리케이션 `.env` 파일에 Stripe API 키를 설정하세요. Stripe 콘솔에서 해당 키를 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `STRIPE_WEBHOOK_SECRET` 환경 변수를 반드시 정의해야 하며, 이는 들어오는 웹훅이 Stripe에서 전송된 것인지 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

또한, 청구서에 표시할 돈 단위 포맷을 지정하기 위해 로케일(locale) 설정도 가능합니다. 내부적으로 Cashier는 [PHP `NumberFormatter`](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외 로케일을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화 되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 이용하면 Stripe에서 생성되는 모든 청구서의 세금을 자동으로 계산할 수 있습니다. 이를 활성화하려면 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

```
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Cashier::calculateTaxes();
}
```

세금 계산이 활성화되면, 신규 구독 및 일회성 청구서에 대해 자동 세금 계산이 적용됩니다.

이 기능이 정상 작동하려면, 고객 이름, 주소, 세금 ID 등 고객 정보가 Stripe와 동기화되어야 합니다. Cashier의 [고객 데이터 동기화](#syncing-customer-data-with-stripe)와 [세금 ID](#tax-ids) 메서드를 참고하세요.

> [!WARNING]
> [단일 결제](#single-charges)나 [단일 결제 체크아웃](#single-charge-checkouts)에는 세금이 자동 계산되지 않습니다.

<a name="logging"></a>
### 로깅 (Logging)

Stripe 관련 치명적인 오류를 기록할 로그 채널을 지정할 수 있습니다. `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 설정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출에서 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용하기 (Using Custom Models)

Cashier의 기본 모델을 확장하여 자신만의 모델을 사용할 수 있습니다. 다음 예시는 `Subscription` 모델을 확장한 경우입니다:

```
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델을 정의한 후, `Laravel\Cashier\Cashier` 클래스를 통해 해당 커스텀 모델을 Cashier에 등록하세요. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

<a name="customers"></a>
## 고객 (Customers)

<a name="retrieving-customers"></a>
### 고객 조회 (Retrieving Customers)

Stripe ID를 사용해 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 이 메서드는 빌러블 모델 인스턴스를 반환합니다:

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

때때로 Stripe 고객을 구독 없이 미리 생성하고 싶을 수 있습니다. 이때는 `createAsStripeCustomer` 메서드를 사용합니다:

```
$stripeCustomer = $user->createAsStripeCustomer();
```

추후에 구독을 시작할 수 있습니다. Stripe API가 지원하는 추가 고객 생성 인수를 포함시키려면 옵션 배열을 전달하세요:

```
$stripeCustomer = $user->createAsStripeCustomer($options);
```

빌러블 모델에서 Stripe 고객 객체를 바로 얻고 싶으면 `asStripeCustomer` 메서드를 사용하세요:

```
$stripeCustomer = $user->asStripeCustomer();
```

Stripe에 이미 고객이 있는지 모르는 경우 `createOrGetStripeCustomer` 메서드가 있으면 기존 고객을 반환하고 없으면 새로 만듭니다:

```
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 정보 업데이트 (Updating Customers)

고객 정보를 Stripe에 직접 업데이트하고 싶으면 `updateStripeCustomer` 메서드를 사용하세요. 인수로는 Stripe 고객 업데이트 API가 지원하는 옵션 배열을 전달합니다:

```
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 (Balances)

Stripe는 고객 잔액에 신용또는 차감 처리를 지원합니다. 잔액은 이후 청구서에 반영됩니다. 고객의 전체 잔액 조회는 빌러블 모델에서 `balance` 메서드를 사용하세요. 고객 통화 포맷으로 된 문자열을 반환합니다:

```
$balance = $user->balance();
```

고객 잔액을 충전할 때는 `creditBalance` 메서드에 금액과 선택적 설명을 제공합니다:

```
$user->creditBalance(500, 'Premium customer top-up.');
```

잔액을 차감하려면 `debitBalance` 메서드를 사용하세요:

```
$user->debitBalance(300, 'Bad usage penalty.');
```

`applyBalance` 메서드는 새로운 잔액 거래를 생성합니다. 거래 기록은 `balanceTransactions` 메서드로 불러올 수 있으며 고객에게 남긴 크레딧, 차감 내역 로그에 유용합니다:

```
// 모든 거래 기록 조회...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액(예: $2.31)
    $amount = $transaction->amount();

    // 가능한 경우 관련 청구서 조회...
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID (Tax IDs)

Cashier는 고객의 세금 ID 관리를 간편하게 도와줍니다. 예를 들어 `taxIds` 메서드로 모든 세금 ID 컬렉션을 조회합니다:

```
$taxIds = $user->taxIds();
```

특정 세금 ID는 `findTaxId` 메서드에 ID를 넘겨 조회합니다:

```
$taxId = $user->findTaxId('txi_belgium');
```

유효한 유형과 값을 `createTaxId` 메서드에 전달해 새 세금 ID를 만들 수 있습니다:

```
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId` 메서드는 즉시 VAT ID를 고객 계정에 추가합니다. Stripe도 VAT ID 검증을 비동기적으로 수행합니다. 검증 결과 확인은 `customer.tax_id.updated` 웹훅 이벤트를 구독하고 VAT ID의 `verification` 파라미터를 검사하세요. 웹훅 처리 관련 내용은 [웹훅 핸들러 문서](#handling-stripe-webhooks)도 참고하세요.

`deleteTaxId` 메서드로 세금 ID 삭제가 가능합니다:

```
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### 고객 데이터 Stripe와 동기화 (Syncing Customer Data With Stripe)

애플리케이션 내 사용자가 이름, 이메일 등 정보 변경 시 Stripe에도 업데이트가 필요합니다. Stripe 데이터와 동기화하려면 모델의 `updated` 이벤트 리스너를 만들어, 해당 이벤트에서 `syncStripeCustomerDetails` 메서드를 호출하세요:

```
use function Illuminate\Events\queueable;

/**
 * 모델 "booted" 메서드
 *
 * @return void
 */
protected static function booted()
{
    static::updated(queueable(function ($customer) {
        if ($customer->hasStripeId()) {
            $customer->syncStripeCustomerDetails();
        }
    }));
}
```

이제 고객 모델 업데이트 시마다 Stripe 정보가 자동 동기화됩니다. 첫 고객 생성 시에도 Cashier가 자동으로 동기화를 수행합니다.

동기화 칼럼을 커스텀하고 싶으면 Cashier가 제공하는 다양한 메서드(예: `stripeName`)를 오버라이드하세요:

```
/**
 * Stripe에 동기화할 고객 이름 반환
 *
 * @return string|null
 */
public function stripeName()
{
    return $this->company_name;
}
```

같은 방법으로 `stripeEmail`, `stripePhone`, `stripeAddress`, `stripePreferredLocales` 메서드도 오버라이드할 수 있습니다. 보다 완전한 동기화 제어가 필요하면 `syncStripeCustomerDetails` 메서드를 직접 오버라이드하세요.

<a name="billing-portal"></a>
### 청구 포털 (Billing Portal)

Stripe는 고객이 직접 구독, 결제 수단, 청구 내역을 관리할 수 있는 [청구 관리 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 빌러블 모델에서 `redirectToBillingPortal` 메서드를 호출하면 해당 포털로 리다이렉트합니다:

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

사용자가 관리 후 기본적으로 애플리케이션 `home` 경로로 돌아가게 됩니다. 리턴 URL을 커스텀하고 싶으면 인자로 URL을 전달하세요:

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

HTTP 리다이렉트 없이 청구 포털 URL만 받고 싶으면 `billingPortalUrl` 메서드를 호출하세요:

```
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단 (Payment Methods)

<a name="storing-payment-methods"></a>
### 결제 수단 저장 (Storing Payment Methods)

Stripe 구독 또는 단일 결제를 위해 결제 수단을 저장하고 Stripe에 식별자를 받아야 합니다. 저장 방법은 구독용과 단일 결제용이 다릅니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독용 결제 수단

구독 결제 수단 저장에는 Stripe의 "Setup Intents" API를 사용해야 합니다. Setup Intent는 Stripe에 고객 결제 수단을 저장할 의도를 알리는 역할입니다. Billable 트레이트의 `createSetupIntent` 메서드로 생성하며, 이를 결제 입력 폼을 렌더링하는 컨트롤러/라우트에서 호출합니다:

```
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

뷰의 `client_secret` 값을 카드 정보 입력 폼에 전달하세요:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 표시자 -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

Stripe.js를 사용해 카드 요소를 폼에 붙이고 안전하게 고객 결제 정보를 모읍니다:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

아래 코드는 Stripe의 `confirmCardSetup` 메서드를 사용해 카드 검증과 안전한 결제 수단 식별자를 가져오는 방법입니다:

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
        // 사용자에게 "error.message" 출력...
    } else {
        // 카드가 성공적으로 검증됨...
    }
});
```

검증 후 `setupIntent.payment_method` 식별자를 Laravel 애플리케이션에 전달해 고객에게 결제 수단을 연결하거나, 기본 결제 수단을 업데이트하거나, 즉시 구독 생성에 사용할 수 있습니다.

> [!NOTE]
> Setup Intent 및 고객 결제 정보 수집에 관해 더 알고 싶으면 [Stripe 문서 개요](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>
#### 단일 결제용 결제 수단

단일 결제에서는 결제 수단 식별자를 한 번만 사용합니다. Stripe 제한으로 인해 기본 결제 수단은 단일 결제에 사용할 수 없으므로 고객이 Stripe.js 폼으로 직접 결제 정보를 입력해야 합니다. 예를 들어:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements 자리 표시자 -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

Stripe.js를 붙여 보안 결제 정보를 수집합니다:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

`createPaymentMethod` 메서드로 카드 검증과 결제 수단 ID 획득:

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
        // 사용자에게 "error.message" 출력...
    } else {
        // 검증 성공...
    }
});
```

검증 성공 시 `paymentMethod.id`를 Laravel 애플리케이션에 전달하여 단일 결제 작업을 수행할 수 있습니다.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회 (Retrieving Payment Methods)

빌러블 모델에서 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스 컬렉션을 반환합니다:

```
$paymentMethods = $user->paymentMethods();
```

기본값은 `card` 형식 결제 수단입니다. 다른 종류 조회 시에는 인자로 타입을 전달하세요:

```
$paymentMethods = $user->paymentMethods('sepa_debit');
```

고객의 기본 결제 수단 조회는 `defaultPaymentMethod` 메서드를 사용합니다:

```
$paymentMethod = $user->defaultPaymentMethod();
```

빌러블 모델에 연결된 특정 결제 수단 조회는 `findPaymentMethod` 메서드로 수행합니다:

```
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="check-for-a-payment-method"></a>
### 사용자가 결제 수단이 있는지 확인하기 (Determining If A User Has A Payment Method)

기본 결제 수단이 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 호출하세요:

```
if ($user->hasDefaultPaymentMethod()) {
    //
}
```

결제 수단이 최소 하나라도 있는지 확인하려면 `hasPaymentMethod` 메서드를 사용합니다:

```
if ($user->hasPaymentMethod()) {
    //
}
```

기본값은 `card` 타입 결제 수단 확인이며, 다른 타입을 확인하려면 인자로 타입을 넘기세요:

```
if ($user->hasPaymentMethod('sepa_debit')) {
    //
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트 (Updating The Default Payment Method)

`updateDefaultPaymentMethod` 메서드는 Stripe 결제 수단 식별자를 받아 고객의 기본 결제 수단을 업데이트합니다:

```
$user->updateDefaultPaymentMethod($paymentMethod);
```

기본 결제 수단을 Stripe 고객의 기본 결제 수단과 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용하세요:

```
$user->updateDefaultPaymentMethodFromStripe();
```

> [!WARNING]
> 고객 기본 결제 수단은 청구 및 새 구독 생성에만 사용되며, Stripe 제한으로 인해 단일 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가 (Adding Payment Methods)

결제 수단 ID를 빌러블 모델에 추가하려면 `addPaymentMethod` 메서드를 호출하세요:

```
$user->addPaymentMethod($paymentMethod);
```

> [!NOTE]
> 결제 수단 ID 획득 방법은 [결제 수단 저장 문서](#storing-payment-methods)를 참조하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제 (Deleting Payment Methods)

`Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출해 개별 결제 수단을 삭제하세요:

```
$paymentMethod->delete();
```

빌러블 모델에서 특정 결제 수단을 삭제하려면 `deletePaymentMethod` 메서드를 사용합니다:

```
$user->deletePaymentMethod('pm_visa');
```

모든 결제 수단을 삭제하려면 `deletePaymentMethods` 메서드를 호출하세요:

```
$user->deletePaymentMethods();
```

기본값은 `card` 타입 삭제이며, 다른 타입 삭제 시 인자로 타입을 넘겨주세요:

```
$user->deletePaymentMethods('sepa_debit');
```

> [!WARNING]
> 활성 구독이 있는 사용자가 기본 결제 수단을 삭제하지 못하게 애플리케이션에서 막아야 합니다.

<a name="subscriptions"></a>
## 구독 (Subscriptions)

구독은 고객의 반복 결제를 간편하게 설정하는 방법입니다. Cashier가 관리하는 Stripe 구독은 다중 구독 가격, 수량, 체험 기간 등 다양한 기능을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 빌러블 모델 인스턴스를 조회한 후 `newSubscription` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```

`newSubscription` 첫 번째 인자는 구독 내 내부에서 사용하는 이름이며, `default` 등으로 지정합니다. 이름은 사용자에게 보이지 않으며 공백을 포함해선 안 되고, 생성 이후 변경해서도 안 됩니다. 두 번째 인자는 Stripe 가격 ID를 넘깁니다.

`create` 메서드는 Stripe 결제 수단 ID 또는 `PaymentMethod` 객체를 받아 구독을 시작하며, 데이터베이스에 Stripe 고객 ID 및 결제 정보를 업데이트합니다.

> [!WARNING]
> `create` 메서드에 결제 수단 ID를 직접 넘기면 자동으로 해당 결제 수단을 사용자 결제 수단에 추가합니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 청구서 이메일 통한 반복 결제 수집

Stripe가 자동 결제 대신, 결제 시마다 청구서를 이메일로 보내는 방식도 가능합니다. 이 경우 고객이 결제 수단을 미리 등록할 필요가 없습니다:

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

청구서 납부 만료일까지(subscription cancel 전까지) 30일(기본) 외 다른 기간 설정도 가능합니다:

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```

<a name="subscription-quantities"></a>
#### 수량 설정 (Quantities)

구독 가격 수량을 지정하려면 구독 빌더에 `quantity` 메서드를 체인 후 `create` 하세요:

```
$user->newSubscription('default', 'price_monthly')
     ->quantity(5)
     ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 정보 (Additional Details)

Stripe가 지원하는 고객 또는 구독 옵션을 추가로 전달할 때는 `create` 메서드에 두 번째, 세 번째 인자로 배열을 넘깁니다:

```
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```

<a name="coupons"></a>
#### 쿠폰 (Coupons)

구독 생성 시 쿠폰을 적용하려면 `withCoupon` 메서드를 사용하세요:

```
$user->newSubscription('default', 'price_monthly')
     ->withCoupon('code')
     ->create($paymentMethod);
```

Stripe 프로모션 코드를 적용하려면 `withPromotionCode` 메서드를 사용합니다:

```
$user->newSubscription('default', 'price_monthly')
     ->withPromotionCode('promo_code_id')
     ->create($paymentMethod);
```

프로모션 코드 ID는 Stripe API상 부여된 ID이며, 고객에게 보이는 코드가 아닙니다. 고객 코드로 ID를 찾으려면 `findPromotionCode`, 활성 코드는 `findActivePromotionCode` 메서드를 사용하세요:

```
// 프로모션 코드 ID 조회
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// 활성 프로모션 코드 ID 조회
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

`Laravel\Cashier\PromotionCode` 인스턴스인 반환 객체에서 쿠폰 정보는 `coupon` 메서드로 가져올 수 있습니다:

```
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

특정 할인 유형 확인 예:

```
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```

사용자 또는 구독에 적용된 할인은 각각 다음 메서드로 조회:

```
$discount = $billable->discount();

$discount = $subscription->discount();
```

`Laravel\Cashier\Discount` 인스턴스이며, 할인 쿠폰은 `coupon` 메서드로 조회할 수 있습니다:

```
$coupon = $subscription->discount()->coupon();
```

새 쿠폰이나 프로모션 코드를 적용하려면 다음 메서드를 사용하세요:

```
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```

쿠폰이나 프로모션 코드는 한 번에 하나만 적용 가능하며, 프로모션 코드 ID는 Stripe API상의 ID여야 합니다.

더 자세한 내용은 Stripe의 [쿠폰 문서](https://stripe.com/docs/billing/subscriptions/coupons)와 [프로모션 코드 문서](https://stripe.com/docs/billing/subscriptions/coupons/codes)를 참고하세요.

<a name="adding-subscriptions"></a>
#### 구독 추가 (Adding Subscriptions)

이미 기본 결제 수단이 있는 고객에게 구독을 추가하려면 구독 빌더의 `add` 메서드를 사용하세요:

```
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 구독 생성

Stripe 대시보드에서 구독을 생성할 수도 있습니다. 이 때 Cashier는 새 구독을 `default` 이름으로 동기화합니다. 대시보드 구독 생성 시 할당할 구독 이름을 바꾸려면 [WebhookController](#defining-webhook-event-handlers)를 확장해 `newSubscriptionName` 메서드를 오버라이드하세요.

대시보드에서는 한 종류 구독만 생성 가능합니다. 애플리케이션에서 여러 구독을 지원할 경우, 대시보드에서는 하나만 관리할 수 있습니다.

또한, 같은 이름의 여러 활성 구독이 있으면 Cashier는 가장 최근 구독만 사용하고 과거 구독은 참조용으로 유지합니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

고객 구독이 활성인지 쉽게 확인할 수 있습니다. `subscribed` 메서드는 해당 구독 이름에 대해 활성(체험 기간 포함) 구독이 있으면 `true`를 반환합니다:

```
if ($user->subscribed('default')) {
    //
}
```

`subscribed`는 라우트 미들웨어로도 사용해 구독 상태 기반 접근 제어에 활용할 수 있습니다.

체험 기간 중인 경우 확인은 구독 인스턴스의 `onTrial` 메서드를 사용하세요:

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

특정 Stripe 상품 ID에 대해 구독 여부 확인은 `subscribedToProduct` 메서드를 사용합니다:

```
if ($user->subscribedToProduct('prod_premium', 'default')) {
    //
}
```

여러 상품 배열 전달도 가능합니다:

```
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    //
}
```

가격 ID에 따른 구독 여부 확인은 `subscribedToPrice` 메서드를 사용하세요:

```
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    //
}
```

현재 구독 중이면서 체험 기간이 끝난 상태는 `recurring` 메서드로 확인 가능합니다:

```
if ($user->subscription('default')->recurring()) {
    //
}
```

> [!WARNING]
> 같은 이름 구독이 여러 개 있을 경우, `subscription` 메서드는 가장 최근 구독을 반환합니다. 이전 구독은 기록을 위해 데이터베이스에 남아 있습니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태 (Canceled Subscription Status)

과거에 구독했다가 취소한 상태는 `canceled` 메서드로 확인 가능:

```
if ($user->subscription('default')->canceled()) {
    //
}
```

취소 이후 아직 남은 유예 기간(그레이스 기간) 중인지 확인하려면 `onGracePeriod` 메서드를 사용하세요:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

유예 기간이 끝났다면 `ended` 메서드를 사용해 확인할 수 있습니다:

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료 및 연체 상태 (Incomplete and Past Due Status)

결제 추가 확인이 필요한 경우 구독 상태는 `incomplete`로 표시됩니다. 가격 변경 시 추가 결제 조치가 필요한 경우엔 `past_due` 상태가 됩니다. 상태 정보는 `stripe_status` 컬럼에 저장됩니다.

이 상태에선 결제가 완료될 때까지 구독이 활성화되지 않습니다. 미완료 결제 여부는 빌러블 모델이나 구독 인스턴스의 `hasIncompletePayment` 메서드로 확인하세요:

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

미완료 결제 시 사용자를 Cashier 결제 확인 페이지로 안내하세요. 구독 인스턴스의 `latestPayment` 메서드로 결제 ID를 구할 수 있습니다:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    결제 확인이 필요합니다.
</a>
```

`past_due` 또는 `incomplete` 상태임에도 구독을 활성 상태로 유지하려면 `keepPastDueSubscriptionsActive`와 `keepIncompleteSubscriptionsActive` 메서드를 `AppServiceProvider`의 `register` 메서드에서 호출하세요:

```
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 등록
 *
 * @return void
 */
public function register()
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```

> [!WARNING]
> `incomplete` 상태에선 결제 확인 전까지 구독 변경이 불가능하므로 `swap`, `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 조회용 쿼리 스코프 (Subscription Scopes)

다양한 구독 상태 조회용 Eloquent 쿼리 스코프도 제공합니다:

```
// 활성 구독 모두 조회
$subscriptions = Subscription::query()->active()->get();

// 사용자 취소 구독 모두 조회
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

구독 가격을 변경하려면 구독 인스턴스의 `swap` 메서드에 새 가격 ID를 전달하세요. 가격 변경 시 구독이 취소 상태였다면 재활성화됩니다. 가격 ID는 Stripe에 등록된 가격 식별자여야 합니다:

```
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

체험 기간 유지, 수량 유지됩니다.

체험을 바로 무효화하려면 `skipTrial` 메서드도 호출하세요:

```
$user->subscription('default')
        ->skipTrial()
        ->swap('price_yearly');
```

즉시 고객에게 인보이스 발행하고 싶으면 `swapAndInvoice` 메서드를 사용하세요:

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 가격 조정 시 비례 요금 무시 (Prorations)

기본적으로 Stripe는 가격 변경 시 비례 요금을 계산합니다. 이를 방지하려면 `noProrate` 메서드를 호출하세요:

```
$user->subscription('default')->noProrate()->swap('price_yearly');
```

> [!WARNING]
> `noProrate` 메서드 호출 후 바로 `swapAndInvoice` 호출하면 비례 요금 무시는 효력이 없습니다. 인보이스는 반드시 발행됩니다.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

“수량”에 영향을 받는 구독도 있습니다. 예를 들어, 프로젝트당 월 $10 과금 시 수량을 쉽게 증가, 감소할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 5개 만큼 추가
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 5개 만큼 감소
$user->subscription('default')->decrementQuantity(5);
```

특정 수량으로 바로 설정하려면 `updateQuantity` 메서드 사용:

```
$user->subscription('default')->updateQuantity(10);
```

비례 요금 계산 없이 수량만 변경하려면 `noProrate` 체인을 붙이세요:

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

더 자세한 건 [Stripe 문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 다중 상품 구독 수량 증가/감소

여러 상품을 동시에 구독하는 경우 수량을 증가/감소하려면 두 번째 인자로 가격 ID를 지정하세요:

```
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="subscriptions-with-multiple-products"></a>
### 다중 상품 구독 (Subscriptions With Multiple Products)

Stripe 다중 상품 구독은 하나 구독에 여러 청구 상품을 연결하는 기능입니다. 예를 들어 기본 구독 월 $10, 라이브 채팅 추가 상품 월 $15를 동시에 결제하는 경우가 그렇습니다. 다중 상품 구독 정보는 DB `subscription_items` 테이블에 저장됩니다.

다중 상품을 지정하려면 `newSubscription` 두 번째 인자로 가격 ID 배열을 전달하세요:

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

특정 상품의 수량을 지정하려면 `quantity` 메서드에 가격 ID를 추가 인자로 넘길 수 있습니다:

```
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 가격을 추가하려면 `addPrice` 메서드 사용:

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

즉시 고객에게 청구하려면 `addPriceAndInvoice` 메서드를 사용합니다:

```
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

특정 수량 포함해 추가 시 두 번째 인자로 수량을 넘기세요:

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

가격을 제거하려면 `removePrice` 메서드 사용:

```
$user->subscription('default')->removePrice('price_chat');
```

> [!WARNING]
> 구독에서 마지막 남은 가격은 제거할 수 없습니다. 전체 구독을 취소하세요.

<a name="swapping-prices"></a>
#### 다중 상품 구독 가격 교체 (Swapping Prices)

여러 상품 구독에 기존 가격을 교체할 수도 있습니다. 예를 들어 기본 가격을 `price_basic`에서 `price_pro`로 변경하려면:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

`price_basic` 아이템은 삭제되고 `price_chat`은 유지됩니다.

가격별 수량, 메타데이터 지정하려면 `swap` 메서드에 옵션 배열을 넘기세요:

```
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

단일 가격만 변경할 경우, 구독 아이템 인스턴스의 `swap` 메서드를 사용해 해당 가격만 변경할 수 있습니다:

```
$user = User::find(1);

$user->subscription('default')
        ->findItemOrFail('price_basic')
        ->swap('price_pro');
```

<a name="proration"></a>
#### 비례 요금 (Proration)

다중 상품 구독에서는 가격 추가/제거 시 Stripe가 기본으로 비례 요금 계산합니다. 이를 막으려면 가격 변경 시 `noProrate` 메서드를 붙이세요:

```
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량 변경 (Quantities)

다중 상품 각각의 수량 변경 시, 앞서 설명한 수량 관련 메서드에 가격 ID를 추가 인자로 넘기세요:

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!WARNING]
> 다중 가격 구독의 경우 `Subscription` 모델의 `stripe_price`와 `quantity` 속성은 `null`입니다. 개별 가격 정보는 `items` 관계를 통해 접근하세요.

<a name="subscription-items"></a>
#### 구독 아이템 (Subscription Items)

가격별 구독 아이템은 DB `subscription_items` 테이블에 저장됩니다. 구독에서 `items` 관계로 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

특정 아이템은 `findItemOrFail` 메서드로 조회:

```
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="multiple-subscriptions"></a>
### 다중 구독 (Multiple Subscriptions)

Stripe는 한 고객이 동시에 여러 구독을 가질 수 있도록 지원합니다. 예를 들어 수영 구독과 웨이트 트레이닝 구독을 별도로 운영하는 경우가 그렇습니다.

구독을 생성할 때 이름을 지정해 여러 구독을 관리할 수 있습니다:

```
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```

나중에 월간 구독을 연간 구독으로 전환하려면:

```
$user->subscription('swimming')->swap('price_swimming_yearly');
```

구독 취소는 다음과 같이 합니다:

```
$user->subscription('swimming')->cancel();
```

<a name="metered-billing"></a>
### 측정 기반 과금 (Metered Billing)

[측정 기반 과금](https://stripe.com/docs/billing/subscriptions/metered-billing)은 고객 사용량 기반으로 과금합니다. 예를 들어 고객의 SMS 송신 수에 따라 과금할 때 씁니다.

먼저 Stripe 대시보드에서 측정 가격을 만드는 것이 필요합니다. 이후 `meteredPrice` 메서드로 해당 가격 ID를 구독에 추가하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

Stripe Checkout에서도 측정 기반 구독이 가능합니다:

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
#### 사용량 보고 (Reporting Usage)

고객 사용량은 차후 청구서에 반영되도록 Stripe에 신고해야 합니다. 기본 단위 1 추가:

```
$user = User::find(1);

$user->subscription('default')->reportUsage();
```

특정 단위 수량 전달도 가능:

```
$user = User::find(1);

$user->subscription('default')->reportUsage(15);
```

구독에 여러 가격이 있으면 `reportUsageFor` 메서드로 가격 ID 지정:

```
$user = User::find(1);

$user->subscription('default')->reportUsageFor('price_metered', 15);
```

기존 신고 사용량을 특정 시점으로 업데이트하려면, 두 번째 인자로 타임스탬프 또는 `DateTimeInterface` 인스턴스 전달:

```
$user = User::find(1);

$user->subscription('default')->reportUsage(5, $timestamp);
```

<a name="retrieving-usage-records"></a>
#### 사용 기록 조회 (Retrieving Usage Records)

과거 사용량은 구독 인스턴스의 `usageRecords` 메서드로 조회:

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecords();
```

다중 가격 구독이라면 `usageRecordsFor` 메서드 사용:

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecordsFor('price_metered');
```

반환된 컬렉션을 반복해 기간별 총 사용량 출력 가능:

```
@foreach ($usageRecords as $usageRecord)
    - 시작 기간: {{ $usageRecord['period']['start'] }}
    - 종료 기간: {{ $usageRecord['period']['end'] }}
    - 총 사용량: {{ $usageRecord['total_usage'] }}
@endforeach
```

상세 데이터와 커서 기반 페이징 방법은 [Stripe API 문서](https://stripe.com/docs/api/usage_records/subscription_item_summary_list) 참조.

<a name="subscription-taxes"></a>
### 구독 세금 (Subscription Taxes)

> [!WARNING]
> 직접 세율을 계산하지 말고 [Stripe Tax 자동 세금 계산](#tax-configuration)을 활용하세요.

사용자별 구독 세율은 빌러블 모델에서 `taxRates` 메서드를 구현해 Stripe 세율 ID 배열을 반환하세요. Stripe 대시보드에서 세율을 정의할 수 있습니다:

```
/**
 * 고객 구독에 적용할 세율 배열 반환
 *
 * @return array
 */
public function taxRates()
{
    return ['txr_id'];
}
```

나라별 세금이 다를 때 유용합니다.

다중 상품 구독에서는 `priceTaxRates` 메서드를 구현해 가격별 세율도 지정 가능:

```
/**
 * 고객 구독에 적용할 가격별 세율
 *
 * @return array
 */
public function priceTaxRates()
{
    return [
        'price_monthly' => ['txr_id'],
    ];
}
```

> [!WARNING]
> `taxRates` 메서드는 구독 요금에만 적용되며, 단일 결제 시 수동으로 세율을 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화 (Syncing Tax Rates)

`taxRates` 반환값을 바꿔도 기존 구독 세율은 변경되지 않습니다. 기존 구독 세율을 최신 값으로 갱신하려면 구독 인스턴스의 `syncTaxRates` 메서드를 호출하세요:

```
$user->subscription('default')->syncTaxRates();
```

다중 상품 구독일 경우 아이템 세율도 동기화합니다.

<a name="tax-exemption"></a>
#### 세금 면제 (Tax Exemption)

Cashier는 Stripe API로 고객 세금 면제 상태를 확인하는 다음 메서드를 제공합니다:

```
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

> [!WARNING]
> 이 메서드들은 `Laravel\Cashier\Invoice` 인스턴스에서도 사용 가능하며, 이 경우 청구서 생성 시점 면제 상태를 확인합니다.

<a name="subscription-anchor-date"></a>
### 구독 청구 주기 기준일 설정 (Subscription Anchor Date)

기본 청구 기준일은 구독 생성일(혹은 체험 종료일)입니다. 변경하려면 `anchorBillingCycleOn` 메서드를 사용하세요:

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

자세한 것은 [Stripe 청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소 (Cancelling Subscriptions)

구독을 취소하려면 `cancel` 메서드를 호출하세요:

```
$user->subscription('default')->cancel();
```

취소 시 `ends_at` 칼럼이 설정되어 구독 종료 시점을 관리합니다. 예를 들어 3월 1일에 취소해도 청구 주기 종료일인 3월 5일까지는 여전히 구독이 활성(`subscribed` 메서드 `true`)입니다.

취소 후 유예 기간 확인은 `onGracePeriod` 메서드:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

즉시 취소하려면 `cancelNow` 메서드를 사용하세요:

```
$user->subscription('default')->cancelNow();
```

즉시 취소와 미청구된 사용량/요금 항목 청구까지 하려면 `cancelNowAndInvoice` 쓰세요:

```
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점 취소도 가능합니다:

```
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

<a name="resuming-subscriptions"></a>
### 구독 재개 (Resuming Subscriptions)

유예 기간 내 취소한 구독은 `resume` 메서드로 재개할 수 있습니다:

```
$user->subscription('default')->resume();
```

재개하면 본래 청구 주기로 다시 과금됩니다.

<a name="subscription-trials"></a>
## 구독 체험 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 입력 후 체험 (With Payment Method Up Front)

체험 기간을 제공하면서 결제 수단도 미리 수집하려면 구독 생성 시 `trialDays` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
                ->trialDays(10)
                ->create($request->paymentMethodId);

    // ...
});
```

이 메서드는 DB 구독 레코드에 체험 종료일을 설정하고 Stripe에서는 해당기간 동안 과금을 시작하지 않습니다. 기본 체험 기간을 덮어씁니다.

> [!WARNING]
> 체험 종료 이전에 구독을 취소하지 않으면 종료 직후 바로 과금되니 사용자에게 종료일을 명확히 알려주세요.

`trialUntil` 메서드는 종료일을 `DateTime` 인스턴스로 지정할 때 사용합니다:

```
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
            ->trialUntil(Carbon::now()->addDays(10))
            ->create($paymentMethod);
```

체험 중인지 확인하려면 사용자 인스턴스의 `onTrial` 또는 구독 인스턴스의 `onTrial` 메서드를 쓰세요:

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

즉시 체험 종료는 `endTrial` 메서드 사용:

```
$user->subscription('default')->endTrial();
```

체험 기간 만료 여부는 `hasExpiredTrial` 메서드로 확인하세요:

```
if ($user->hasExpiredTrial('default')) {
    //
}

if ($user->subscription('default')->hasExpiredTrial()) {
    //
}
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 체험 기간 정의

스트라이프 대시보드에서 가격별 체험 기간을 설정하거나, Cashier에서 항상 명시적으로 지정할 수 있습니다. Stripe에 체험을 등록하면, 재구독 고객도 체험을 받으며, 이를 원하지 않으면 반드시 `skipTrial()`을 호출하세요.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 체험 (Without Payment Method Up Front)

체험 기간 동안 결제 수단 정보를 받지 않을 경우, 사용자의 `trial_ends_at` 칼럼에 체험 종료일을 직접 설정해 주세요. 보통 사용자 등록 시 설정합니다:

```
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!WARNING]
> 빌러블 모델 클래스 내 `trial_ends_at` 속성에 [날짜 캐스트](/docs/9.x/eloquent-mutators#date-casting)를 등록해야 합니다.

이를 "일반 체험(Generic Trial)"이라 부릅니다. 빌러블 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at`보다 이전이면 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 체험 기간임...
}
```

실제 구독 생성은 평소처럼 `newSubscription`으로 합니다:

```
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

체험 종료일 조회는 `trialEndsAt` 메서드로 하며, 기본 구독 아닌 특정 구독 구분자도 인자로 넘길 수 있습니다:

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

"`generic` 체험"임을 명확히 확인하려면 `onGenericTrial` 메서드를 사용하세요:

```
if ($user->onGenericTrial()) {
    // 일반 체험 기간입니다...
}
```

<a name="extending-trials"></a>
### 체험 기간 연장 (Extending Trials)

`extendTrial` 메서드로 구독 체험 기간을 연장할 수 있습니다. 이미 만료되어 과금 시작된 경우에도 연장 가능하며, 연장 기간은 다음 청구서에서 차감됩니다:

```
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 7일 뒤에 체험 종료일 설정
$subscription->extendTrial(
    now()->addDays(7)
);

// 기존 체험 종료일에 5일 추가
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe Webhook 처리 (Handling Stripe Webhooks)

> [!NOTE]
> Stripe CLI를 사용하면 로컬 개발 중 웹훅 테스트에 도움이 됩니다.

Stripe는 다양한 이벤트를 웹훅으로 애플리케이션에 알려줍니다. 기본적으로 Cashier 서비스 프로바이더가 웹훅 컨트롤러 경로를 등록해 요청을 처리합니다.

기본 웹훅 컨트롤러는 실패한 결제에 따른 구독 자동 취소, 고객 및 구독 변경, 결제 수단 변경 등을 자동 처리합니다. 추가 웹훅 이벤트는 컨트롤러를 확장해 처리할 수 있습니다.

앱에서 웹훅을 처리하려면 Stripe 콘솔에서 웹훅 URL을 설정하세요. 기본 경로는 `/stripe/webhook` 입니다. Cashier가 필요로 하는 웹훅 목록:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

`cashier:webhook` Artisan 명령어로 Stripe에 웹훅을 생성할 수도 있습니다:

```shell
php artisan cashier:webhook
```

기본 생성 웹훅은 `.env`의 `APP_URL`에 정의된 URL과 `cashier.webhook` 라우트로 연결됩니다. 별도 URL 지정도 가능합니다:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

다른 Stripe API 버전을 지정하려면 `--api-version` 옵션을 사용:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

생성 시 바로 활성화되며, 비활성 상태로 만들려면 `--disabled` 옵션 추가:

```shell
php artisan cashier:webhook --disabled
```

> [!WARNING]
> Cashier가 제공하는 [웹훅 서명 검증](#verifying-webhook-signatures) 미들웨어를 반드시 사용해 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅 & CSRF 보호 우회

Stripe 웹훅은 Laravel CSRF 보호 대상이 아니므로, `App\Http\Middleware\VerifyCsrfToken` 미들웨어 예외에 경로를 추가하거나 `web` 미들웨어 그룹에서 제외하세요:

```
protected $except = [
    'stripe/*',
];
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 실패 결제로 인한 구독 취소 등 주요 이벤트를 자동 처리하지만, 추가 처리할 이벤트가 있으면 Cashier가 발송하는 이벤트 리스너를 등록하세요:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

이벤트에는 Stripe 웹훅 전체 페이로드가 포함됩니다. 예를 들어 `invoice.payment_succeeded` 이벤트를 처리하려면:

```
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Stripe 웹훅 이벤트 처리
     *
     * @param  \Laravel\Cashier\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // 이벤트 처리 로직...
        }
    }
}
```

리스너 등록은 `EventServiceProvider`에서:

```
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

웹훅 보안을 위해 Stripe 웹훅 서명을 활용하세요. Cashier에는 Stripe 서명 검증 미들웨어가 기본 포함되어 있습니다.

검증 활성화를 위해 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 변수에 Stripe 대시보드에서 받은 웹훅 시크릿을 설정하세요.

<a name="single-charges"></a>
## 단일 결제 (Single Charges)

<a name="simple-charge"></a>
### 단순 결제 (Simple Charge)

단일 결제를 수행하고 싶으면 빌러블 모델 인스턴스에서 `charge` 메서드를 호출하세요. 두 번째 인자로 결제 수단 ID를 넘겨야 합니다:

```
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```

세 번째 인자는 Stripe API의 결제 생성 옵션 배열입니다:

```
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

빌러블 모델 인스턴스가 없을 경우 새 모델 인스턴스에서 바로 호출할 수도 있습니다:

```
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

충전 실패 시 예외가 발생하며 성공 시 `Laravel\Cashier\Payment` 인스턴스를 반환합니다:

```
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    //
}
```

> [!WARNING]
> 결제 금액은 애플리케이션 화폐 단위 최하위 단위로 지정해야 합니다. 예를 들어 미국 달러라면 센트 단위로 지정하세요.

<a name="charge-with-invoice"></a>
### 청구서와 함께 결제 (Charge With Invoice)

PDF 영수증을 고객에게 제공하고 싶으면 `invoicePrice` 메서드를 사용하세요. 예를 들어 셔츠 다섯 벌 결제:

```
$user->invoicePrice('price_tshirt', 5);
```

청구서는 기본 결제 수단으로 즉시 결제 처리됩니다. 세 번째 인자는 청구 항목 옵션, 네 번째 인자는 청구서 옵션입니다:

```
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

`invoicePrice`와 비슷하게 여러 품목을 "탭"으로 추가 후 청구도 가능합니다:

```
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```

단일 과금을 위해 `invoiceFor` 메서드도 제공:

```
$user->invoiceFor('One Time Fee', 500);
```

가격 정의된 메서드 사용이 분석 및 통계에 유리합니다.

> [!WARNING]
> `invoice`, `invoicePrice`, `invoiceFor` 메서드로 생성된 인보이스는 실패 시 결제 재시도가 발생합니다. 실패 후 재시도를 하지 않으려면 Stripe API로 직접 인보이스를 닫아야 합니다.

<a name="creating-payment-intents"></a>
### 결제 인텐트 생성 (Creating Payment Intents)

`pay` 메서드로 Stripe 결제 인텐트를 생성할 수 있습니다. 반환값은 `Laravel\Cashier\Payment` 인스턴스입니다:

```
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```

생성 후 클라이언트 시크릿을 프런트엔드에 넘겨 Stripe 결제를 진행합니다. 결제 흐름 더 자세한 내용은 [Stripe 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web) 참조.

기본 이용 가능한 결제 수단 외 일부만 지정하고 싶으면 `payWith` 메서드를 사용하세요:

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
> `pay`, `payWith` 메서드도 화폐 단위 최하위 단위로 금액을 지정해야 합니다.

<a name="refunding-charges"></a>
### 결제 환불 (Refunding Charges)

Stripe 결제를 환불하려면 `refund` 메서드를 사용하세요. 첫 번째 인자는 결제 인텐트 ID입니다:

```
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 청구서 (Invoices)

<a name="retrieving-invoices"></a>
### 청구서 조회 (Retrieving Invoices)

빌러블 모델의 청구서 목록은 `invoices` 메서드로 간편 조회:

```
$invoices = $user->invoices();
```

미확정 청구서 포함은 `invoicesIncludingPending` 사용:

```
$invoices = $user->invoicesIncludingPending();
```

특정 청구서는 `findInvoice` 메서드로 ID 조회:

```
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 청구서 정보 표시

청구서 리스트를 표 형태로 출력 예:

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
### 예정된 청구서 (Upcoming Invoices)

다음 청구서는 `upcomingInvoice` 메서드로 조회:

```
$invoice = $user->upcomingInvoice();
```

구독별 예고 청구서도 가능:

```
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 청구서 미리보기 (Previewing Subscription Invoices)

가격 변경 전 청구서 미리보기는 `previewInvoice` 메서드에 새 가격 ID 전달:

```
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

가격 여러 개 배열 전달도 지원:

```
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### PDF 형태로 청구서 생성 (Generating Invoice PDFs)

PDF 청구서 생성을 위해 Dompdf 라이브러리를 설치하세요:

```php
composer require dompdf/dompdf
```

라우트나 컨트롤러에서 `downloadInvoice` 메서드로 PDF 다운로드 응답 생성:

```
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```

기본값으로 청구서 데이터는 Stripe 고객 및 청구서 정보 기반입니다. 파일명은 `app.name` 기준 생성됩니다. 다음과 같이 커스텀 정보 전달 가능:

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

셋째 인자로 파일명 지정 가능하며 `.pdf`가 자동 붙습니다:

```
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 청구서 렌더러

기본 `DompdfInvoiceRenderer` 외 원하는 PDF 렌더러를 구현할 수 있습니다. `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현하세요. 예를 들어 외부 API 호출 렌더러:

```
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * 청구서 렌더링 후 PDF 바이트 반환
     *
     * @param  \Laravel\Cashier\Invoice $invoice
     * @param  array  $data
     * @param  array  $options
     * @return string
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```

설치 후 `config/cashier.php` 의 `cashier.invoices.renderer` 설정값에 클래스를 지정하세요.

<a name="checkout"></a>
## 체크아웃 (Checkout)

Cashier Stripe는 Stripe Checkout도 지원합니다. Stripe Checkout은 결제용 커스텀 페이지 구현 부담을 줄여주는 호스팅된 결제 페이지입니다.

아래는 Stripe Checkout 시작법으로, Stripe 공식 [Checkout 문서](https://stripe.com/docs/payments/checkout)도 참고하세요.

<a name="product-checkouts"></a>
### 상품 체크아웃 (Product Checkouts)

Stripe 대시보드에 등록된 기존 상품에 대해 `checkout` 메서드로 체크아웃 세션을 생성합니다. 기본으로 가격 ID를 인자로 넘겨야 합니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

수량도 지정 가능:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

성공/취소 후 리디렉션할 URL은 `success_url`, `cancel_url` 옵션으로 지정:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

성공 URL 쿼리 문자열에 체크아웃 세션 ID 포함 시 `{CHECKOUT_SESSION_ID}` 리터럴을 포함하세요. Stripe가 실제 세션 ID로 대체합니다:

```
use Illuminate\Http\Request;

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

Stripe Checkout 기본값은 유저가 프로모션 코드를 직접 입력하지 못합니다. 활성화하려면 `allowPromotionCodes` 메서드를 호출하세요:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 단일 결제 체크아웃 (Single Charge Checkouts)

Stripe 대시보드에 없는 임시 상품에 대해 단일 결제를 하려면 `checkoutCharge` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!WARNING]
> `checkoutCharge` 사용 시 Stripe에 새 제품과 가격이 생성됩니다. 가급적 뒤늦게 생성하지 말고 Stripe 대시보드에서 미리 상품을 만들어 `checkout`을 이용하세요.

<a name="subscription-checkouts"></a>
### 구독 체크아웃 (Subscription Checkouts)

> [!WARNING]
> Stripe Checkout으로 구독하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅 활성화가 필요합니다. 이 웹훅으로 구독 레코드가 생성됩니다.

Cashier 구독 빌더로 구독 설정 후 `checkout` 메서드를 호출하면 Stripe Checkout 세션이 만들어집니다:

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

성공 및 취소 URL도 지정 가능합니다:

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

프로모션 코드도 체크아웃에 활성화 가능:

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
> 현재 Stripe Checkout은 `anchorBillingCycleOn` 사용, 가격 변경시 proration 설정, 결제 동작 설정 등 일부 구독 청구 옵션을 지원하지 않습니다. 상세 내용은 [Stripe Checkout Session API](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout & 체험 기간

Stripe Checkout 구독 생성 시 체험 기간 설정 가능:

```
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

최소 체험 기간은 48시간 이상이어야 합니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독 및 웹훅

Stripe와 Cashier는 웹훅으로 구독 상태를 관리합니다. 따라서 고객이 체크아웃 후 앱에 돌아올 때 구독이 준비 중일 수 있음을 주의하세요. 이 때는 대기 메시지 등을 보여주는 UX가 필요합니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집 (Collecting Tax IDs)

체크아웃 세션에서 고객 세금 ID 수집을 활성화하려면 `collectTaxIds` 메서드를 사용하세요:

```
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

체크아웃에 구매자가 회사임을 표시하고 세금 ID를 입력할 수 있도록 체크박스가 나타납니다.

> [!WARNING]
> 애플리케이션에서 이미 자동 세금 계산([세금 설정](#tax-configuration))을 활성화했다면, 이 옵션은 별도로 호출하지 않아도 자동 적용됩니다.

<a name="guest-checkouts"></a>
### 비회원 체크아웃 (Guest Checkouts)

`Checkout::guest` 메서드로 계정이 없는 비회원용 체크아웃 세션을 생성할 수 있습니다:

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

기존 체크아웃 빌더 메서드도 적용할 수 있습니다:

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

비회원 체크아웃 완료 후 Stripe가 `checkout.session.completed` 웹훅 이벤트를 전송하므로, Stripe 대시보드에서 이벤트 활성화 후 Cashier로 처리하세요. 웹훅 페이로드에는 [`checkout` 객체](https://stripe.com/docs/api/checkout/sessions/object)가 포함되며 주문 처리에 활용할 수 있습니다.

<a name="handling-failed-payments"></a>
## 실패한 결제 처리 (Handling Failed Payments)

구독이나 단발 결제가 실패할 수 있습니다. 이 경우 Cashier가 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 던집니다. 예외 처리 후 두 가지 대응법이 있습니다.

먼저 Cashier가 제공하는 결제 확인 페이지로 리다이렉트해 추가 결제 절차를 진행할 수 있습니다. 예외를 처리할 때 `cashier.payment` 이름 라우트로 리다이렉트하세요:

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

이 페이지에서 고객은 카드 정보를 다시 입력하고 Stripe가 요구하는 추가 인증(예: 3D Secure)을 완료합니다. 완료 후 `redirect` 매개변수의 URL로 리다이렉트됩니다. 성공 여부와 메시지 정보가 쿼리 스트링으로 전달됩니다.

현재 지원되는 결제 수단 유형:

- 신용카드
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

두 번째 방법은 Stripe 대시보드에서 자동 청구 이메일을 설정해 Stripe가 결제 확인을 직접 수행하게 하는 것입니다. 그러나 `IncompletePayment` 예외가 발생하면 사용자에게 이메일이 전송되어야 한다고 알리는 로직이 필요합니다.

`charge`, `invoiceFor`, `invoice` 메서드, `SubscriptionBuilder`의 `create` 메서드, `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 메서드 등이 결제 불완료 예외를 던질 수 있습니다.

미완료 결제 상태는 빌러블 모델과 구독 인스턴스의 `hasIncompletePayment` 메서드로 확인하세요:

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

예외의 `payment` 속성으로 결제 인텐트 상태를 확인하고 상세 처리도 가능합니다:

```
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 상태 확인
    $exception->payment->status;

    // 조건별 처리
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="strong-customer-authentication"></a>
## 강력한 고객 인증 (SCA)

유럽 법률에 따라 2019년 9월부터 SCA(강력한 고객 인증)를 준수해야 합니다. Stripe와 Cashier는 SCA 규정 준수를 지원합니다.

> [!WARNING]
> 시작 전에 [Stripe PSD2 & SCA 가이드](https://stripe.com/guides/strong-customer-authentication) 및 [SCA API 문서](https://stripe.com/docs/strong-customer-authentication)를 꼭 읽어보세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 결제 확인 필요 상황 (Payments Requiring Additional Confirmation)

SCA는 추가 인증 과정을 요구하는 경우가 많습니다. 이때 Cashier는 `IncompletePayment` 예외를 던집니다. 예외 처리 방법은 앞서 [실패한 결제 처리](#handling-failed-payments) 문서를 참고하세요.

Stripe나 Cashier 결제 확인 페이지는 은행 인증 흐름 및 추가 결제 수단 확인, 소액 임시 결제, 디바이스 인증 등 다양한 방식으로 표시됩니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체 상태

추가 결제 확인이 필요한 동안 구독 상태는 데이터베이스 `stripe_status` 컬럼에서 `incomplete` 또는 `past_due`로 표시됩니다. 결제 완료가 확인되고 Stripe 웹훅이 도착하면 구독이 자동 활성화됩니다.

이 상태 관련 자세한 설명은 [미완료와 연체 상태](#incomplete-and-past-due-status)를 참조하세요.

<a name="off-session-payment-notifications"></a>
### 오프 세션 결제 알림 (Off-Session Payment Notifications)

SCA 요구사항에 따라 구독 갱신 등 오프 세션 결제 시 추가 확인이 필요하면 사용자에게 알림을 보낼 수 있습니다. 알림 클래스는 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수에 알림 클래스명을 지정해 활성화합니다. 기본값은 비활성화 상태이며, Cashier가 기본 제공하는 알림 클래스도 사용 가능합니다:

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

알림이 제대로 가도록 Stripe 웹훅(`invoice.payment_action_required`)이 활성화되어 있고, 빌러블 모델에 Laravel `Notifiable` 트레이트가 적용되어 있는지 확인하세요.

> [!WARNING]
> Stripe는 수동 결제와 오프 세션 진행 여부를 구분 못합니다. 결제 확인 페이지에서 중복 결제를 막고, 결제 이후 재확인 시 간단한 성공 메시지만 표시됩니다.

<a name="stripe-sdk"></a>
## Stripe SDK

Cashier 객체는 Stripe SDK 객체를 감싼 래퍼입니다. Stripe 객체를 직접 다루려면 `asStripe` 메서드를 사용하세요:

```
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

또는 `updateStripeSubscription` 메서드로 Stripe 구독을 직접 업데이트할 수 있습니다:

```
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Cashier::stripe()` 메서드는 Stripe SDK의 `Stripe\StripeClient` 인스턴스를 반환합니다. 예를 들어 Stripe 가격 목록을 조회할 수 있습니다:

```
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트 (Testing)

Cashier를 사용하는 애플리케이션 테스트 시 Stripe API 호출을 모킹할 수도 있지만 Cashier 자체 동작을 부분 재구현해야 해, 실제 Stripe 테스트 환경을 사용하는 것을 권장합니다. 느리지만 애플리케이션 동작 신뢰성이 올라가며, 느린 테스트는 별도 PHPUnit 테스트 그룹에 넣을 수 있습니다.

테스트 환경에서 Stripe 비밀 키를 `phpunit.xml` 에 설정하세요:

```
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

실제 Stripe 테스트 계정과 상호작용하며, 테스트용 구독과 가격을 미리 준비해 두세요.

> [!NOTE]
> 카드 거절, 실패 등 각종 시나리오 테스트를 위해 Stripe가 제공하는 [다양한 테스트 카드 번호 및 토큰](https://stripe.com/docs/testing)을 참고하세요.