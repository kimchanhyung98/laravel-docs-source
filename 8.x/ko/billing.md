# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
    - [데이터베이스 마이그레이션](#database-migrations)
- [설정](#configuration)
    - [Billable 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [결제 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [사용자의 결제 수단 존재 여부 확인](#check-for-a-payment-method)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 가격 구독](#multiprice-subscriptions)
    - [종량제 청구](#metered-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일 설정](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [결제 수단 동시 수집 시](#with-payment-method-up-front)
    - [결제 수단 없이 체험만 제공](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 서명 검증](#verifying-webhook-signatures)
- [일회성 결제](#single-charges)
    - [간단 결제](#simple-charge)
    - [청구서가 포함된 결제](#charge-with-invoice)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [제품 결제](#product-checkouts)
    - [일회성 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
- [청구서](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [다가오는 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [청구서 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
- [강화된 고객 인증 (SCA)](#strong-customer-authentication)
    - [추가 인증이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 청구 서비스를 위한 표현력이 풍부하고 유창한 인터페이스를 제공합니다. 구독 청구 코드의 보일러플레이트 작성 업무를 대부분 처리해주어 개발자가 부담을 덜 수 있습니다. 기본적인 구독 관리 외에도 Cashier는 쿠폰, 구독 교체, 구독 "수량", 취소 유예 기간, PDF 청구서 생성 기능을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

새로운 Cashier 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 주의 깊게 검토해야 합니다.

> [!NOTE]
> 변경으로 인한 문제를 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 13은 Stripe API `2020-08-27` 버전을 사용합니다. 새로운 Stripe 기능과 개선사항을 활용하기 위해 마이너 릴리스 때 API 버전이 갱신될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치하세요:

```
composer require laravel/cashier
```

> [!NOTE]
> Cashier가 Stripe 이벤트를 정상적으로 처리하도록 하려면 [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)을 꼭 수행하세요.

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션 (Database Migrations)

Cashier의 서비스 프로바이더는 자체 마이그레이션 디렉터리를 등록하니, 패키지 설치 후 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하고, 고객의 모든 구독 정보를 관리할 `subscriptions` 테이블을 새로 만듭니다:

```
php artisan migrate
```

만약 Cashier가 기본 제공하는 마이그레이션 파일을 덮어쓰고 싶다면, 다음 Artisan 명령어로 게시할 수 있습니다:

```
php artisan vendor:publish --tag="cashier-migrations"
```

데이터베이스 마이그레이션을 전혀 실행하지 않으려면 Cashier가 제공하는 `ignoreMigrations` 메서드를 사용할 수 있습니다. 일반적으로 `AppServiceProvider` 클래스의 `register` 메서드에서 호출합니다:

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

> [!NOTE]
> Stripe 식별자를 저장하는 모든 컬럼은 대소문자를 구분해야 하므로, MySQL을 사용한다면 `stripe_id` 컬럼의 콜레이션을 `utf8_bin`으로 설정하세요. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### Billable 모델 (Billable Model)

Cashier를 사용하기 전에 구독이 가능한(billable) 모델에 `Billable` 트레이트를 추가하세요. 보통 `App\Models\User` 모델에 추가합니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트처럼 자주 사용하는 청구 관련 작업을 위한 다양한 메서드를 제공합니다:

```
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 Laravel의 `App\Models\User` 클래스를 billable 모델로 간주합니다. 변경하려면 `AppServiceProvider` 클래스의 `boot` 메서드에서 `useCustomerModel` 메서드로 다른 모델을 지정할 수 있습니다:

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

> [!NOTE]
> 기본 Laravel `App\Models\User` 모델이 아닌 다른 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 게시하고 테이블 이름을 적절히 변경해야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

다음으로 애플리케이션의 `.env` 파일에서 Stripe API 키를 설정합니다. Stripe 관리 콘솔에서 API 키를 확인할 수 있습니다:

```
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
```

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 애플리케이션 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 설정하세요:

```
CASHIER_CURRENCY=eur
```

또한 청구서에 표시할 금액의 통화 형식을 지정할 로케일(locale)을 설정할 수도 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!NOTE]
> `en`(영어) 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 통해 Stripe가 생성하는 모든 청구서에 대해 자동으로 세금을 계산할 수 있습니다. `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 자동 세금 계산을 활성화하세요:

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

세금 계산이 활성화되면 새 구독과 단발성 청구서가 자동으로 세금을 계산합니다.

이 기능이 정상 작동하려면 고객의 이름, 주소, 세금 ID 등 청구 세부 정보를 Stripe와 동기화해야 합니다. 이를 위해 Cashier에서 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe)와 [세금 ID](#tax-ids) 기능을 사용할 수 있습니다.

> [!NOTE]
> 현재로서는 [단일 결제](#single-charges)와 [일회성 체크아웃](#single-charge-checkouts)에는 세금 계산이 적용되지 않습니다. 또한 Stripe Tax는 베타 기간 중 "초대 전용" 상태입니다. Stripe Tax 접근 권한은 [Stripe Tax 웹사이트](https://stripe.com/tax#request-access)에서 신청할 수 있습니다.

<a name="logging"></a>
### 로깅 (Logging)

Stripe 치명적 오류 로그에 사용할 채널을 지정하려면 애플리케이션 `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 설정하세요:

```
CASHIER_LOGGER=stack
```

Stripe API 호출에 의해 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier가 내부적으로 사용하는 모델을 직접 정의한 모델로 확장할 수 있습니다. 대상 Cashier 모델을 상속하세요:

```
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // 사용자 정의 내용
}
```

모델을 정의한 뒤 `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에게 커스텀 모델을 사용하도록 알릴 수 있습니다. 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 지정합니다:

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

Stripe ID를 이용해 고객을 조회하려면 `Cashier::findBillable` 메서드를 사용하세요. 이 메서드는 billable 모델 인스턴스를 반환합니다:

```
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```

<a name="creating-customers"></a>
### 고객 생성 (Creating Customers)

때때로 구독을 시작하지 않고 Stripe 고객을 생성하고 싶을 수 있습니다. 이때 `createAsStripeCustomer` 메서드를 사용하세요:

```
$stripeCustomer = $user->createAsStripeCustomer();
```

Stripe에서 고객이 생성된 후 나중에 구독을 시작할 수 있습니다. Stripe API가 지원하는 추가 고객 생성 옵션을 `$options` 배열로 전달할 수 있습니다:

```
$stripeCustomer = $user->createAsStripeCustomer($options);
```

billable 모델에 해당하는 Stripe 고객 객체를 반환받으려면 `asStripeCustomer` 메서드를 사용하세요:

```
$stripeCustomer = $user->asStripeCustomer();
```

billable 모델이 이미 Stripe 고객인지 확실치 않다면 `createOrGetStripeCustomer` 메서드를 사용하세요. 고객이 없으면 새로 생성합니다:

```
$stripeCustomer = $user->createOrGetStripeCustomer();
```

<a name="updating-customers"></a>
### 고객 업데이트 (Updating Customers)

Stripe 고객 정보를 추가로 업데이트하고자 할 때 `updateStripeCustomer` 메서드를 사용하세요. 이 메서드는 Stripe API가 지원하는 [고객 업데이트 옵션 배열](https://stripe.com/docs/api/customers/update)을 인수로 받습니다:

```
$stripeCustomer = $user->updateStripeCustomer($options);
```

<a name="balances"></a>
### 잔액 (Balances)

Stripe에서는 고객 잔액을 크레딧 또는 차감할 수 있습니다. 잔액은 이후 청구서에 반영됩니다. 고객 잔액의 총합을 확인하려면 billable 모델에서 `balance` 메서드를 사용하세요. 고객 통화에 맞춰 포맷된 문자열을 반환합니다:

```
$balance = $user->balance();
```

잔액에 크레딧을 더하려면 음수 값을 `applyBalance` 메서드에 넘기고, 필요 시 설명도 제공합니다:

```
$user->applyBalance(-500, 'Premium customer top-up.');
```

잔액 차감은 양수 값을 넘기면 됩니다:

```
$user->applyBalance(300, 'Bad usage penalty.');
```

`applyBalance` 메서드는 고객 잔액 거래 내역을 생성합니다. 거래 내역은 로그로 보여줄 때 유용하며, `balanceTransactions` 메서드로 조회할 수 있습니다:

```
// 모든 거래 내역 조회
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // 거래 금액 확인 ($2.31 등)
    $amount = $transaction->amount();

    // 가능 시 관련 청구서도 조회
    $invoice = $transaction->invoice();
}
```

<a name="tax-ids"></a>
### 세금 ID (Tax IDs)

Cashier는 고객의 세금 ID 관리를 쉽게 지원합니다. 예를 들어, `taxIds` 메서드로 고객에게 할당된 모든 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션으로 가져올 수 있습니다:

```
$taxIds = $user->taxIds();
```

특정 세금 ID는 식별자로 조회할 수 있습니다:

```
$taxId = $user->findTaxId('txi_belgium');
```

유효한 [세금 ID 타입](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값으로 새 세금 ID를 생성하려면 `createTaxId` 메서드를 사용하세요:

```
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

`createTaxId` 호출 즉시 VAT ID가 고객에 추가됩니다. Stripe는 VAT ID 유효성 검사를 비동기적으로 진행하며, 검사 상태는 `customer.tax_id.updated` 웹훅 이벤트와 VAT ID의 `verification` 파라미터를 통해 알 수 있습니다. 웹훅 처리 방법은 [웹훅 이벤트 핸들러 정의](#handling-stripe-webhooks)를 참고하세요.

세금 ID 삭제는 `deleteTaxId` 메서드로 합니다:

```
$user->deleteTaxId('txi_belgium');
```

<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화 (Syncing Customer Data With Stripe)

애플리케이션 내 사용자가 이름, 이메일 등 정보를 변경하면 Stripe에도 이를 알려 동기화해야 합니다. 이렇게 하면 Stripe 데이터가 애플리케이션과 일치하게 유지됩니다.

자동화를 위해 billable 모델의 `updated` 이벤트에 리스너를 등록하고, 그 안에서 `syncStripeCustomerDetails` 메서드를 호출할 수 있습니다:

```
use function Illuminate\Events\queueable;

/**
 * 모델의 "booted" 메서드
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

이제 고객 모델이 업데이트될 때마다 Stripe 정보도 동기화됩니다. 새로운 고객 생성 시에는 Cashier가 자동으로 이 작업을 수행합니다.

동기화에 사용되는 컬럼을 바꾸고 싶으면 `stripeName`, `stripeEmail`, `stripePhone`, `stripeAddress` 등의 메서드를 오버라이드할 수 있습니다:

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

모든 동기화 과정을 완전히 제어하려면 `syncStripeCustomerDetails` 메서드를 오버라이드하세요.

<a name="billing-portal"></a>
### 결제 포털 (Billing Portal)

Stripe에서 제공하는 [빌링 포털](https://stripe.com/docs/billing/subscriptions/customer-portal)을 설정하면, 고객이 자신의 구독, 결제 수단, 청구 내역을 직접 관리할 수 있습니다. billable 모델에서 `redirectToBillingPortal` 메서드를 호출해 고객을 포털로 리다이렉트하세요:

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```

기본적으로 관리가 끝난 후 고객은 Stripe 빌링 포털 내 링크를 통해 애플리케이션의 `home` 경로로 돌아갑니다. 다른 URL로 리디렉션되도록 하려면 메서드에 URL을 전달하세요:

```
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```

리다이렉트 응답 대신 URL을 얻고 싶으면 `billingPortalUrl` 메서드를 호출하세요:

```
$url = $request->user()->billingPortalUrl(route('billing'));
```

<a name="payment-methods"></a>
## 결제 수단 (Payment Methods)

<a name="storing-payment-methods"></a>
### 결제 수단 저장 (Storing Payment Methods)

Stripe를 통한 구독이나 단발 결제에는 결제 수단 정보 저장과 Stripe로부터 ID 획득이 필요합니다. 결제 수단 저장 방식은 구독용과 일회성 결제용으로 달라, 둘 다 설명하겠습니다.

<a name="payment-methods-for-subscriptions"></a>
#### 구독용 결제 수단 (Payment Methods For Subscriptions)

구독 시 사용할 카드 정보를 안전하게 수집하려면 Stripe의 "Setup Intents" API를 사용해야 합니다. Setup Intent는 Stripe에 고객 결제 수단 청구 의도를 알립니다. Cashier `Billable` 트레이트의 `createSetupIntent` 메서드로 새 Setup Intent를 쉽게 생성할 수 있습니다. 결제 수단 정보를 입력하는 뷰를 렌더링할 라우트 또는 컨트롤러에서 호출하세요:

```
return view('update-payment-method', [
    'intent' => $user->createSetupIntent()
]);
```

Setup Intent를 생성해 뷰에 전달한 뒤에는 뷰 내 결제 수단 수집 요소에 `client_secret`을 포함합니다. 예를 들어, 아래와 같은 "결제 수단 업데이트" 폼이 있습니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

Stripe.js 라이브러리를 활용해 Stripe Element를 폼에 붙이고 안전하게 카드 정보를 수집하세요:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

그 후 Stripe의 `confirmCardSetup` 메서드로 카드 정보를 검증하고 "결제 수단 ID"를 받아옵니다:

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
        // 사용자에게 "error.message" 표시
    } else {
        // 카드 검증 성공
    }
});
```

검증이 완료되면 `setupIntent.payment_method` ID를 Laravel 애플리케이션으로 전달해 고객에 연결할 수 있습니다. 이 결제 수단은 [새 결제 수단 추가](#adding-payment-methods)나 [기본 결제 수단 업데이트](#updating-the-default-payment-method)에 사용할 수 있고, 즉시 [새 구독 생성](#creating-subscriptions)에도 활용할 수 있습니다.

> [!TIP]
> Setup Intents 및 고객 결제 수단 수집에 관한 더 자세한 내용은 [Stripe 개요](https://stripe.com/docs/payments/save-and-reuse#php)를 참고하세요.

<a name="payment-methods-for-single-charges"></a>
#### 일회성 결제용 결제 수단 (Payment Methods For Single Charges)

일회성 결제 시에는 결제 수단 ID를 한 번만 사용합니다. Stripe 제약상 고객의 저장된 기본 결제 수단을 사용할 수 없어, Stripe.js를 통해 결제 수단 정보를 고객이 직접 입력하도록 해야 합니다. 예를 들면 다음과 같은 폼이 있습니다:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

Stripe.js를 사용해 Stripe Element를 연결하고, 안전하게 카드 정보를 수집하세요:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

카드를 검증하고 결제 수단 ID를 받으려면 Stripe의 `createPaymentMethod` 메서드를 사용하세요:

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
        // 사용자에게 "error.message" 표시
    } else {
        // 카드 검증 성공
    }
});
```

검증이 끝나면 `paymentMethod.id`를 Laravel 애플리케이션으로 전달해 [단일 결제](#simple-charge)를 처리하세요.

<a name="retrieving-payment-methods"></a>
### 결제 수단 조회 (Retrieving Payment Methods)

billable 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스들의 컬렉션을 반환합니다:

```
$paymentMethods = $user->paymentMethods();
```

기본적으로 `card` 타입 결제 수단만 반환합니다. 다른 타입을 조회하려면 타입 문자열을 인자로 전달하세요:

```
$paymentMethods = $user->paymentMethods('sepa_debit');
```

고객의 기본 결제 수단은 `defaultPaymentMethod` 메서드로 조회합니다:

```
$paymentMethod = $user->defaultPaymentMethod();
```

billable 모델에 연결된 특정 결제 수단도 `findPaymentMethod` 메서드로 가져올 수 있습니다:

```
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

<a name="check-for-a-payment-method"></a>
### 사용자의 결제 수단 존재 여부 확인 (Determining If A User Has A Payment Method)

기본 결제 수단을 가지고 있는지 확인하려면 `hasDefaultPaymentMethod` 메서드를 사용하세요:

```
if ($user->hasDefaultPaymentMethod()) {
    //
}
```

하나 이상의 `card` 타입 결제 수단을 보유했는지 확인하려면 `hasPaymentMethod` 메서드를 사용하세요:

```
if ($user->hasPaymentMethod()) {
    //
}
```

다른 타입 결제 수단 존재 여부를 확인하려면 타입을 인자로 전달하세요:

```
if ($user->hasPaymentMethod('sepa_debit')) {
    //
}
```

<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트 (Updating The Default Payment Method)

`updateDefaultPaymentMethod` 메서드를 사용해 고객의 기본 결제 수단을 업데이트할 수 있습니다. Stripe 결제 수단 식별자를 인자로 받아 새로운 기본 결제 수단으로 지정합니다:

```
$user->updateDefaultPaymentMethod($paymentMethod);
```

Stripe에 저장된 기본 결제 수단 데이터와 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용하세요:

```
$user->updateDefaultPaymentMethodFromStripe();
```

> [!NOTE]
> 고객의 기본 결제 수단은 청구서 결제 및 신규 구독 생성에만 사용할 수 있습니다. Stripe 제약으로 인해 단일 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가 (Adding Payment Methods)

새 결제 수단을 추가하려면 billable 모델의 `addPaymentMethod` 메서드에 결제 수단 ID를 넘겨 호출하세요:

```
$user->addPaymentMethod($paymentMethod);
```

> [!TIP]
> 결제 수단 ID 획득 방법은 [결제 수단 저장 문서](#storing-payment-methods)를 참고하세요.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제 (Deleting Payment Methods)

`Laravel\Cashier\PaymentMethod` 인스턴스에서 직접 `delete` 메서드를 호출하여 삭제할 수 있습니다:

```
$paymentMethod->delete();
```

billable 모델에서 특정 결제 수단을 삭제하려면 `deletePaymentMethod` 메서드를 사용하세요:

```
$user->deletePaymentMethod('pm_visa');
```

모든 결제 수단을 제거하려면 `deletePaymentMethods`를 호출합니다:

```
$user->deletePaymentMethods();
```

기본적으로 `card` 타입 결제 수단이 삭제됩니다. 다른 타입을 지정하려면 인자로 전달하세요:

```
$user->deletePaymentMethods('sepa_debit');
```

> [!NOTE]
> 사용자에게 활성 구독이 있다면 기본 결제 수단 삭제는 허용하지 않아야 합니다.

<a name="subscriptions"></a>
## 구독 (Subscriptions)

구독은 고객의 반복 결제를 설정하는 방법입니다. Cashier가 관리하는 Stripe 구독은 다중 구독 가격, 구독 수량, 체험 기간 등을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성 (Creating Subscriptions)

구독을 생성하려면 일반적으로 `App\Models\User` 인스턴스를 조회합니다. 그런 다음 `newSubscription` 메서드를 사용해 구독을 만듭니다:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // 추가 처리 ...
});
```

`newSubscription` 첫 번째 인수는 내부 구독 이름(예: `default`, `primary`)입니다. 이 이름은 사용자 표시용이 아니며, 공백 없이 고정값이어야 합니다. 두 번째 인수는 Stripe 가격 식별자입니다.

`create` 메서드는 Stripe 결제 수단 ID 또는 `PaymentMethod` 객체를 받아 구독을 시작하고 데이터베이스에 Stripe 고객 ID 등 청구 정보를 업데이트합니다.

> [!NOTE]
> 결제 수단 ID를 `create` 메서드에 직접 넘기면 사용자 결제 수단에도 자동 등록됩니다.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### 반복 결제 고지 이메일 방식 수집

고객에게 결제를 자동으로 청구하는 대신, Stripe에서 반복 결제 시 매번 청구서를 이메일로 보내 고객이 직접 결제하도록 할 수도 있습니다. 이때는 구독 생성 시 결제 수단을 미리 받지 않아도 됩니다:

```
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

구독 및 청구서 설정에 따라 고객이 청구서를 지불하지 않아 구독이 취소되는 기간이 설정됩니다([Stripe 대시보드](https://dashboard.stripe.com/settings/billing/automatic) 참고).

<a name="subscription-quantities"></a>
#### 구독 수량 (Quantities)

특정 가격 구독 수량을 지정하려면 구독 빌더에서 `quantity` 메서드를 호출한 뒤 구독을 생성하세요:

```
$user->newSubscription('default', 'price_monthly')
     ->quantity(5)
     ->create($paymentMethod);
```

<a name="additional-details"></a>
#### 추가 세부사항 (Additional Details)

Stripe가 지원하는 추가 고객 혹은 구독 옵션은 `create` 메서드 두 번째와 세 번째 인자로 전달할 수 있습니다:

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

Stripe 프로모션 코드를 적용하려면 프로모션 코드 ID를 인자로 `withPromotionCode` 메서드를 호출하세요:

```
$user->newSubscription('default', 'price_monthly')
     ->withPromotionCode('promo_code')
     ->create($paymentMethod);
```

<a name="adding-subscriptions"></a>
#### 구독 추가 (Adding Subscriptions)

이미 기본 결제 수단이 있는 고객에게 구독을 추가하려면 구독 빌더에서 `add` 메서드를 호출합니다:

```
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Stripe 대시보드에서 구독 생성

Stripe 대시보드에서도 구독을 생성할 수 있으며, Cashier는 이를 동기화해 `default` 이름으로 저장합니다. 대시보드 생성 구독의 이름을 바꾸려면 [WebhookController 확장](/docs/{{version}}/billing#defining-webhook-event-handlers) 및 `newSubscriptionName` 메서드 오버라이드를 수행하세요.

대시보드에서 한 유형의 구독만 생성할 수 있으니 여러 구독 타입을 제공하는 앱은 주의하세요.

같은 구독 이름으로 두 개가 존재하면 Cashier는 가장 최근 구독만 사용하며, 이전 구독은 기록용으로 데이터베이스에 남습니다.

<a name="checking-subscription-status"></a>
### 구독 상태 확인 (Checking Subscription Status)

고객의 구독 상태를 쉽게 확인하는 다양한 메서드가 있습니다.

`subscribed` 메서드는 해당 이름의 구독이 활성 상태이거나 체험 기간 중이면 `true`를 반환합니다:

```
if ($user->subscribed('default')) {
    //
}
```

이 메서드는 [라우트 미들웨어](/docs/{{version}}/middleware)로도 사용해, 구독 상태에 따른 접근 제어가 가능합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserIsSubscribed
{
    /**
     * 요청 핸들링
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // 결제 고객이 아님
            return redirect('billing');
        }

        return $next($request);
    }
}
```

체험 여부 확인은 `onTrial` 메서드로 할 수 있습니다:

```
if ($user->subscription('default')->onTrial()) {
    //
}
```

`subscribedToProduct`는 Stripe 제품 ID 기반으로 사용자의 구독 상태를 판단합니다:

```
if ($user->subscribedToProduct('prod_premium', 'default')) {
    //
}
```

배열 인자로 여러 제품을 확인할 수도 있습니다:

```
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    //
}
```

`subscribedToPrice`는 가격 ID로 구독 여부 확인:

```
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    //
}
```

`recurring` 메서드는 현재 구독 중이고 체험 기간이 아닌 경우 `true`를 반환합니다:

```
if ($user->subscription('default')->recurring()) {
    //
}
```

> [!NOTE]
> 같은 이름의 구독이 두 개 있는 경우, `subscription` 메서드는 항상 가장 최신 구독을 반환합니다. 이전 구독은 기록 보존용입니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태 (Canceled Subscription Status)

과거에 구독했으나 취소한 경우는 `canceled` 메서드로 확인합니다:

```
if ($user->subscription('default')->canceled()) {
    //
}
```

구독을 취소하고 아직 결제 유예 기간 중이라면 `onGracePeriod` 메서드가 `true`입니다:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

유예 기간이 끝나 구독이 완전히 종료된 상태는 `ended` 메서드로 확인하세요:

```
if ($user->subscription('default')->ended()) {
    //
}
```

<a name="incomplete-and-past-due-status"></a>
#### 미완료 및 연체 상태 (Incomplete and Past Due Status)

결제 추가 작업이 필요한 경우 구독 상태가 `incomplete`로 표시됩니다. 가격 변경으로 추가 결제가 필요하면 `past_due` 상태가 됩니다. 이 상태일 땐 결제가 확정될 때까지 구독은 비활성화됩니다. 구독이나 billable 모델 인스턴스에서 `hasIncompletePayment` 메서드를 활용해 확인할 수 있습니다:

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

미완료 결제가 있을 땐 `latestPayment` 메서드를 통해 결제 ID를 가져와 Cashier 결제 확인 페이지로 리디렉션하세요:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    결제를 확인해 주세요.
</a>
```

`past_due` 상태에서도 구독을 활성화하려면 `AppServiceProvider`의 `register` 메서드에 `keepPastDueSubscriptionsActive` 호출을 추가합니다:

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
}
```

> [!NOTE]
> `incomplete` 상태 구독은 결제 확정 전까지 변경할 수 없습니다. 따라서 `swap`과 `updateQuantity` 호출 시 예외가 발생합니다.

<a name="subscription-scopes"></a>
#### 구독 스코프 (Subscription Scopes)

대부분 구독 상태는 쿼리 스코프로도 제공되어, 상태별 구독을 조회할 수 있습니다:

```php
// 활성 구독 모두 조회
$subscriptions = Subscription::query()->active()->get();

// 특정 사용자 취소 구독 조회
$subscriptions = $user->subscriptions()->canceled()->get();
```

사용 가능한 모든 스코프 목록:

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

구독 후 고객이 구독 가격을 변경하려면 Stripe 가격 ID를 `swap` 메서드에 전달하세요. 이전에 취소된 구독도 다시 활성화됩니다:

```
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```

체험 기간 유지는 기본 동작입니다. 수량도 유지됩니다.

현재 체험 기간을 종료하려면 `skipTrial` 메서드를 연쇄 호출하세요:

```
$user->subscription('default')
        ->skipTrial()
        ->swap('price_yearly');
```

즉시 청구서를 발행하려면 `swapAndInvoice`를 사용하세요:

```
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```

<a name="prorations"></a>
#### 정산 (Prorations)

기본값으로 Stripe는 가격 변경 시 정산을 수행합니다. 비용 정산 없이 가격만 바꾸려면 `noProrate` 메서드를 호출하세요:

```
$user->subscription('default')->noProrate()->swap('price_yearly');
```

더 자세한 내용은 [Stripe 문서](https://stripe.com/docs/billing/subscriptions/prorations)를 참고하세요.

> [!NOTE]
> `noProrate`와 `swapAndInvoice`를 동시에 호출하면 정산 설정은 무시되고 항상 청구서가 발행됩니다.

<a name="subscription-quantity"></a>
### 구독 수량 (Subscription Quantity)

프로젝트 단위 월 $10처럼 구독 수량이 적용되는 경우, `incrementQuantity` 및 `decrementQuantity`로 쉽게 수량을 조절할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// 현재 수량에 5 추가
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// 현재 수량에서 5 차감
$user->subscription('default')->decrementQuantity(5);
```

`updateQuantity`로 특정 수량으로 설정할 수도 있습니다:

```
$user->subscription('default')->updateQuantity(10);
```

정산 없이 수량만 변경하려면 `noProrate`를 추가하세요:

```
$user->subscription('default')->noProrate()->updateQuantity(10);
```

더 자세한 내용은 [Stripe 문서](https://stripe.com/docs/subscriptions/quantities)를 참고하세요.

<a name="multiprice-subscription-quantities"></a>
#### 다중 가격 구독 수량 (Multiprice Subscription Quantities)

다중 가격 구독일 땐 수량 증감 메서드에 가격 이름을 두 번째 인자로 전달해야 합니다:

```
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

<a name="multiprice-subscriptions"></a>
### 다중 가격 구독 (Multiprice Subscriptions)

[다중 가격 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)은 하나의 구독에 여러 청구 가격을 지정하는 기능입니다. 예를 들어, 기본 월 $10 구독에 라이브 채팅 $15 추가 가격이 있는 경우입니다. 다중 가격 구독 정보는 Cashier의 `subscription_items` 테이블에 저장됩니다.

`newSubscription`에 가격 배열을 넘겨 구독 생성 시 여러 가격을 지정할 수 있습니다:

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

위 예제에서 `default` 구독에 두 가격이 붙어 각각 요금을 청구합니다. 필요시 `quantity`로 가격별 수량을 지정할 수 있습니다:

```
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```

기존 구독에 가격을 추가하려면 `addPrice`를 사용하세요:

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```

즉시 청구하려면 `addPriceAndInvoice`를 사용합니다:

```
$user->subscription('default')->addPriceAndInvoice('price_chat');
```

수량을 지정해 추가할 수도 있습니다:

```
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```

가격을 제거하려면 `removePrice` 메서드를 사용하세요:

```
$user->subscription('default')->removePrice('price_chat');
```

> [!NOTE]
> 구독에 가격이 하나 남았으면 제거할 수 없으며, 이런 경우 구독을 취소해야 합니다.

<a name="swapping-prices"></a>
#### 가격 교체 (Swapping Prices)

다중 가격 구독의 가격을 변경할 수도 있습니다. 예를 들어 기본 가격 `price_basic`과 채팅 가격 `price_chat`이 있는데, `price_basic`을 `price_pro`로 업그레이드하려면:

```
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

위 경우 `price_basic` 항목은 삭제되고 `price_chat`는 유지되며, `price_pro`는 새로 추가됩니다.

`swap` 메서드에 옵션(key/value 배열)을 넘겨 가격별 수량 등을 설정할 수도 있습니다:

```
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```

단일 가격 구독 항목만 교체하려면 해당 구독 아이템의 `swap` 메서드를 호출하세요. 이렇게 하면 나머지 가격 메타데이터를 보존할 수 있습니다:

```
$user = User::find(1);

$user->subscription('default')
        ->findItemOrFail('price_basic')
        ->swap('price_pro');
```

<a name="proration"></a>
#### 정산 (Proration)

가격 추가/제거 시 Stripe가 자동으로 정산을 처리합니다. 정산 없이 조정하려면 작업 전에 `noProrate`를 호출하세요:

```
$user->subscription('default')->noProrate()->removePrice('price_chat');
```

<a name="swapping-quantities"></a>
#### 수량 변경 (Swapping Quantities)

가격별 구독 수량 조절은 [구독 수량 메서드](#subscription-quantity)에 가격 이름을 추가 인자로 넘기면 됩니다:

```
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```

> [!NOTE]
> 다중 가격 구독 시 `Subscription` 모델의 `stripe_price`와 `quantity` 속성은 `null`입니다. 개별 가격 정보는 `items` 관계를 통해 접근해야 합니다.

<a name="subscription-items"></a>
#### 구독 항목 (Subscription Items)

다중 가격 구독이면 데이터베이스 내 `subscription_items` 테이블에 여러 항목이 저장됩니다. `Subscription` 모델의 `items` 관계에서 접근 가능합니다:

```
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// 특정 항목 가격과 수량 조회
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```

특정 가격 항목은 `findItemOrFail` 메서드로 조회할 수 있습니다:

```
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

<a name="metered-billing"></a>
### 종량제 청구 (Metered Billing)

[종량제 청구](https://stripe.com/docs/billing/subscriptions/metered-billing)는 고객 사용량에 따라 청구하는 방식입니다. 월당 문자 수, 이메일 발송 수 등 예시에 맞춰 요금을 부과합니다.

종량제 가격으로 Stripe 대시보드에서 제품을 생성한 후, `meteredPrice`로 구독에 가격 ID를 지정하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```

[Stripe Checkout](#checkout)을 통해 종량제 구독 시작도 가능합니다:

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

고객의 사용량을 Stripe에 보고하여 정확 계산을 돕습니다. `reportUsage` 메서드로 종량제 수량을 하나씩 늘립니다:

```
$user = User::find(1);

$user->subscription('default')->reportUsage();
```

특정 수량만큼 더하려면 인자로 전달:

```
$user = User::find(1);

$user->subscription('default')->reportUsage(15);
```

다중 가격 구독일 땐 `reportUsageFor`로 가격 이름과 수량을 지정하세요:

```
$user = User::find(1);

$user->subscription('default')->reportUsageFor('price_metered', 15);
```

기존에 보고한 사용량을 수정할 땐 두 번째 인자(타임스탬프 또는 `DateTimeInterface` 인스턴스)로 해당 시점을 넘기면 됩니다:

```
$user = User::find(1);

$user->subscription('default')->reportUsage(5, $timestamp);
```

<a name="retrieving-usage-records"></a>
#### 사용 기록 조회 (Retrieving Usage Records)

지난 사용 기록은 구독 인스턴스의 `usageRecords` 메서드로 조회합니다:

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecords();
```

다중 가격이면 `usageRecordsFor`로 가격 이름 지정:

```
$user = User::find(1);

$usageRecords = $user->subscription('default')->usageRecordsFor('price_metered');
```

`usageRecords`는 사용 기간과 총 사용량이 담긴 배열 컬렉션을 반환합니다. 예시:

```
@foreach ($usageRecords as $usageRecord)
    - 시작 일시: {{ $usageRecord['period']['start'] }}
    - 종료 일시: {{ $usageRecord['period']['end'] }}
    - 총 사용량: {{ $usageRecord['total_usage'] }}
@endforeach
```

전체 정보와 페이지네이션 사용법은 [Stripe API 문서](https://stripe.com/docs/api/usage_records/subscription_item_summary_list)를 참고하세요.

<a name="subscription-taxes"></a>
### 구독 세금 (Subscription Taxes)

> [!NOTE]
> 수동으로 세율을 계산하는 대신 [Stripe Tax 사용](#tax-configuration)을 권장합니다.

사용자별 세율 지정은 billable 모델에서 `taxRates` 메서드를 구현해 Stripe 세율 ID 배열을 반환하세요. 세율은 [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 설정할 수 있습니다:

```
/**
 * 해당 고객 구독에 적용할 세율 목록 반환
 *
 * @return array
 */
public function taxRates()
{
    return ['txr_id'];
}
```

`taxRates` 메서드는 다국가 사용자 기반에서 편리합니다.

다중 가격 구독 시에는 `priceTaxRates` 메서드를 구현해 가격별 세율을 정의할 수도 있습니다:

```
/**
 * 해당 고객 구독에 적용할 가격별 세율
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

> [!NOTE]
> `taxRates`는 구독 요금에만 적용됩니다. 일회성 청구에 세금을 적용하려면 수동으로 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화 (Syncing Tax Rates)

`taxRates` 메서드의 하드코딩 세율이 변경되어도 기존 구독 세금 설정은 변하지 않습니다. 새로운 세율로 갱신하려면 구독 인스턴스의 `syncTaxRates`를 호출하세요:

```
$user->subscription('default')->syncTaxRates();
```

다중 가격 구독 시 billable 모델에 `priceTaxRates` 메서드를 구현해야 올바르게 동기화됩니다.

<a name="tax-exemption"></a>
#### 세금 면제 (Tax Exemption)

Cashier는 고객의 세금 면제 상태를 판단하는 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드를 제공합니다. 내부적으로 Stripe API를 호출합니다:

```
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```

이 메서드는 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있지만, 이 경우 청구서 생성 시점 기준의 면제 상태를 조회합니다.

<a name="subscription-anchor-date"></a>
### 구독 기준일 설정 (Subscription Anchor Date)

기본 청구 주기 기준일(anchor)은 구독 생성일이나 체험 종료일입니다. 기준일을 변경하려면 `anchorBillingCycleOn` 메서드를 사용하세요:

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

더 자세한 내용은 [Stripe 청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참고하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소 (Cancelling Subscriptions)

구독을 취소하려면 사용자의 구독에 대해 `cancel` 메서드를 호출하세요:

```
$user->subscription('default')->cancel();
```

취소 시 Cashier는 `subscriptions` 테이블의 `ends_at` 컬럼을 자동 설정해 `subscribed` 메서드가 취소 시점을 인지하도록 합니다.

예를 들어, 3월 1일에 취소했어도 종료 예정일이 3월 5일이면, 3월 5일까지는 여전히 `subscribed`가 `true`입니다.

취소 후 유예 기간 중인지 확인하려면 `onGracePeriod`를 사용하세요:

```
if ($user->subscription('default')->onGracePeriod()) {
    //
}
```

즉시 취소하려면 `cancelNow`를 사용합니다:

```
$user->subscription('default')->cancelNow();
```

즉시 취소와 남은 미청구 종량제 사용량 청구까지 하려면 `cancelNowAndInvoice`를 사용하세요:

```
$user->subscription('default')->cancelNowAndInvoice();
```

특정 시점으로 취소 예약도 가능합니다:

```
$user->subscription('default')->cancelAt(
    now()->addDays(10)
);
```

<a name="resuming-subscriptions"></a>
### 구독 재개 (Resuming Subscriptions)

취소 후 아직 유예 기간 내인 고객 구독을 재개하려면 `resume` 메서드를 호출하세요:

```
$user->subscription('default')->resume();
```

유예 기간 내 재개 시 즉시 요금 청구는 없으며, 기존 청구 주기에 맞춰 요금이 청구됩니다.

<a name="subscription-trials"></a>
## 구독 체험 기간 (Subscription Trials)

<a name="with-payment-method-up-front"></a>
### 결제 수단 동시 수집 시 (With Payment Method Up Front)

체험 기간을 제공하면서 고객 결제 수단도 먼저 받고 싶다면 구독 생성 시 `trialDays` 메서드를 사용하세요:

```
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
                ->trialDays(10)
                ->create($request->paymentMethodId);

    // ...
});
```

이 메서드는 데이터베이스와 Stripe에 체험 종료일을 설정해 그 전까진 결제를 하지 않습니다. 이 경우 Stripe 가격에 설정된 기본 체험 기간 대신 `trialDays` 값이 우선 적용됩니다.

> [!NOTE]
> 체험 종료 후 자동 결제가 이루어지니, 사용자에게 체험 종료일을 반드시 안내해야 합니다.

`trialUntil` 메서드로 직접 종료 시점을 `DateTime` 객체로 지정할 수도 있습니다:

```
use Carbon\Carbon;

$user->newSubscription('default', 'price_monthly')
            ->trialUntil(Carbon::now()->addDays(10))
            ->create($paymentMethod);
```

사용자가 체험 중인지 확인하려면 billable이나 구독 인스턴스 양쪽에서 `onTrial`을 사용할 수 있습니다:

```
if ($user->onTrial('default')) {
    //
}

if ($user->subscription('default')->onTrial()) {
    //
}
```

즉시 체험 종료는 구독에서 `endTrial` 메서드로 합니다:

```
$user->subscription('default')->endTrial();
```

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 체험일 정의

Stripe 대시보드에서 가격별 체험일을 설정하거나, Cashier 코드에서 명시적으로 지정할 수 있습니다. Stripe에 설정한 체험일은 새 구독뿐 아니라 과거 구독자도 체험을 받게 됩니다. 체험 없이 구독하려면 `skipTrial()`을 호출하세요.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 체험만 제공 (Without Payment Method Up Front)

체험 기간 동안 결제 수단을 미리 받지 않으려면, 사용자 레코드의 `trial_ends_at` 컬럼을 체험 종료일로 설정합니다. 일반적으로 회원가입 시 처리합니다:

```
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->addDays(10),
]);
```

> [!NOTE]
> `trial_ends_at` 속성은 [날짜 캐스트](/docs/{{version}}/eloquent-mutators##date-casting)로 지정해 주세요.

이런 체험을 "일반 체험(generic trial)"이라고 하며, 실제 구독과 연결되지 않습니다. `onTrial` 메서드는 현재 날짜가 `trial_ends_at`를 넘지 않았으면 `true`를 반환합니다:

```
if ($user->onTrial()) {
    // 체험 중
}
```

구독을 생성하려면 기존과 같이 `newSubscription`을 사용하면 됩니다:

```
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

사용자의 체험 종료일을 조회하려면 `trialEndsAt` 메서드를 사용하세요. 기본 구독명이 아닌 다른 이름 구독의 체험 종료일을 알고 싶으면 구독 이름을 인자로 넘기면 됩니다:

```
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```

일반 체험 여부만 알고 싶으면 `onGenericTrial` 메서드를 사용하세요:

```
if ($user->onGenericTrial()) {
    // 일반 체험 기간 중
}
```

<a name="extending-trials"></a>
### 체험 기간 연장 (Extending Trials)

`extendTrial` 메서드를 사용해 구독 생성 후 체험 기간을 연장할 수 있습니다. 만약 이미 체험이 끝나고 결제가 시작된 경우에도 연장을 지원하며, 초과한 일수만큼 다음 청구서에서 차감됩니다:

```
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// 지금부터 7일 뒤까지 체험 기간 연장
$subscription->extendTrial(
    now()->addDays(7)
);

// 기존 체험 종료일에 5일 더하기
$subscription->extendTrial(
    $subscription->trial_ends_at->addDays(5)
);
```

<a name="handling-stripe-webhooks"></a>
## Stripe 웹훅 처리 (Handling Stripe Webhooks)

> [!TIP]
> 로컬 개발 중 웹훅 테스트는 [Stripe CLI](https://stripe.com/docs/stripe-cli)를 사용하면 편리합니다.

Stripe는 웹훅을 통해 다양한 이벤트를 앱에 알립니다. Cashier 서비스 프로바이더가 기본적으로 웹훅 컨트롤러 경로를 등록하며, 이 컨트롤러가 모든 웹훅 요청을 처리합니다.

기본 제공 컨트롤러는 청구 실패로 인한 구독 취소, 고객 정보 변경, 구독 및 결제 수단 변경을 자동으로 처리합니다. 필요하면 컨트롤러를 확장해 원하는 Stripe 이벤트를 직접 처리할 수 있습니다.

웹훅 URL은 Stripe 관리 콘솔에서 꼭 설정하세요. 기본값은 `/stripe/webhook` 경로입니다. 활성화할 웹훅 이벤트 목록:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `invoice.payment_action_required`

편의를 위해 Cashier는 `cashier:webhook` Artisan 명령어를 제공합니다. 이를 실행하면 Cashier 관련 이벤트를 모두 받는 웹훅이 Stripe에 생성됩니다:

```
php artisan cashier:webhook
```

기본적으로 `APP_URL`과 `cashier.webhook` 라우트에 연결됩니다. 다른 경로를 원하면 `--url` 옵션을 사용하세요:

```
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

웹훅은 Cashier의 호환 Stripe API 버전으로 생성됩니다. 다른 버전을 쓰려면 `--api-version` 옵션을 설정하세요:

```
php artisan cashier:webhook --api-version="2019-12-03"
```

생성 즉시 활성화되며, 비활성 상태로 만들려면 `--disabled` 옵션을 사용하세요:

```
php artisan cashier:webhook --disabled
```

> [!NOTE]
> Cashier에서 제공하는 [웹훅 서명 검증](#verifying-webhook-signatures) 미들웨어로 웹훅 요청을 보호하세요.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호 (Webhooks & CSRF Protection)

Stripe 웹훅은 Laravel의 [CSRF 보호](/docs/{{version}}/csrf)를 우회해야 하므로, `App\Http\Middleware\VerifyCsrfToken` 미들웨어 예외에 URI를 추가하거나 `web` 미들웨어 그룹 밖에서 등록하세요:

```
protected $except = [
    'stripe/*',
];
```

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의 (Defining Webhook Event Handlers)

Cashier는 구독 취소, 결제 실패 등 기본 처리를 자동 수행하지만, 추가 이벤트 처리도 가능합니다. Cashier가 발생시키는 다음 이벤트를 청취하세요:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

두 이벤트 모두 Stripe 웹훅 페이로드를 포함합니다. 예를 들어 `invoice.payment_succeeded` 이벤트를 처리하려면 이벤트 리스너를 등록하세요:

```
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * 수신된 Stripe 웹훅 이벤트 처리
     *
     * @param  \Laravel\Cashier\Events\WebhookReceived  $event
     * @return void
     */
    public function handle(WebhookReceived $event)
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // 이벤트 처리 로직
        }
    }
}
```

정의한 리스너를 애플리케이션 `EventServiceProvider`에 등록하세요:

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

Stripe 웹훅 보안을 위해 [웹훅 서명](https://stripe.com/docs/webhooks/signatures)을 활용할 수 있습니다. 편리하게도 Cashier는 서명 검증 미들웨어를 기본 제공합니다.

서명 검증을 활성화하려면 애플리케이션 `.env`에 `STRIPE_WEBHOOK_SECRET` 환경 변수를 설정하세요. 이 비밀 키는 Stripe 대시보드에서 받을 수 있습니다.

<a name="single-charges"></a>
## 일회성 결제 (Single Charges)

<a name="simple-charge"></a>
### 간단 결제 (Simple Charge)

> [!NOTE]
> `charge` 메서드는 결제 금액을 애플리케이션 통화의 최소 단위(예: 센트)로 지정합니다.

고객에게 1회 결제를 진행하려면 billable 모델의 `charge` 메서드를 사용하세요. 두 번째 인자로 결제 수단 ID가 필요합니다:

```
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $stripeCharge = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // 처리 내용 ...
});
```

`charge` 메서드는 세 번째 인수로 Stripe 청구 생성 시 옵션 배열을 받을 수 있습니다. 자세한 사항은 [Stripe 청구 생성 문서](https://stripe.com/docs/api/charges/create)를 참고하세요:

```
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```

billable 모델 인스턴스가 없어도 새 인스턴스를 만들고 `charge`를 호출할 수 있습니다:

```
use App\Models\User;

$stripeCharge = (new User)->charge(100, $paymentMethod);
```

결제 실패 시 예외가 발생합니다. 성공 시 `Laravel\Cashier\Payment` 인스턴스가 반환됩니다:

```
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    //
}
```

<a name="charge-with-invoice"></a>
### 청구서가 포함된 결제 (Charge With Invoice)

일회성 결제 때 PDF 영수증이 필요하면 `invoicePrice` 메서드를 사용해 가격 ID와 수량을 넘기세요:

```
$user->invoicePrice('price_tshirt', 5);
```

사용자의 기본 결제 수단으로 즉시 청구서가 결제됩니다. 세 번째 인자는 청구 항목 옵션, 네 번째는 청구서 옵션 배열입니다:

```
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```

또는 `invoiceFor` 메서드로 특정 금액의 단발 청구를 할 수도 있습니다:

```
$user->invoiceFor('One Time Fee', 500);
```

선택적이나 `invoicePrice`를 활용해 미리 정의한 가격을 쓰는 편이 Stripe 대시보드 분석에 유리합니다.

> [!NOTE]
> `invoicePrice`와 `invoiceFor` 메서드로 생성된 Stripe 청구서는 실패 시 자동 재시도됩니다. 재시도를 비활성화 하려면 실패 후 API로 직접 청구서를 닫아야 합니다.

<a name="refunding-charges"></a>
### 결제 환불 (Refunding Charges)

Stripe 결제 환불은 `refund` 메서드를 사용하세요. 첫 인자로 Stripe 결제 의도 ID를 전달합니다:

```
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```

<a name="invoices"></a>
## 청구서 (Invoices)

<a name="retrieving-invoices"></a>
### 청구서 조회 (Retrieving Invoices)

billable 모델의 모든 청구서를 `invoices` 메서드로 쉽게 조회할 수 있습니다. 반환값은 `Laravel\Cashier\Invoice` 인스턴스 컬렉션입니다:

```
$invoices = $user->invoices();
```

대기 중인(미결제) 청구서도 포함하려면 `invoicesIncludingPending`를 사용하세요:

```
$invoices = $user->invoicesIncludingPending();
```

특정 청구서를 ID로 조회하려면 `findInvoice`를 사용합니다:

```
$invoice = $user->findInvoice($invoiceId);
```

<a name="displaying-invoice-information"></a>
#### 청구서 정보 표시 (Displaying Invoice Information)

청구서 리스트 UI에서 아래처럼 날짜, 총액, 다운로드 링크를 표시할 수 있습니다:

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
### 다가오는 청구서 (Upcoming Invoices)

다가오는 청구서는 `upcomingInvoice`로 조회합니다:

```
$invoice = $user->upcomingInvoice();
```

복수 구독이 있다면 특정 구독의 다가오는 청구서를 조회할 수도 있습니다:

```
$invoice = $user->subscription('default')->upcomingInvoice();
```

<a name="previewing-subscription-invoices"></a>
### 구독 청구서 미리보기 (Previewing Subscription Invoice)

가격 변경 전에 예상 청구서를 보고 싶다면 `previewInvoice`를 사용합니다. 단일 가격:

```
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

다중 가격:

```
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

<a name="generating-invoice-pdfs"></a>
### 청구서 PDF 생성 (Generating Invoice PDFs)

라우트나 컨트롤러에서 `downloadInvoice` 메서드로 PDF 청구서 다운로드 응답을 생성할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId, [
        'vendor' => 'Your Company',
        'product' => 'Your Product',
    ]);
});
```

청구서 데이터는 기본적으로 Stripe 고객 및 청구서 데이터를 기반으로 합니다. 두 번째 인자로 회사, 제품 정보 등 사용자 정의 데이터 배열을 넘길 수 있습니다:

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
], 'my-invoice');
```

세 번째 인자로는 PDF 파일명(확장자 없이)을 지정할 수 있으며 자동으로 `.pdf`가 붙습니다:

```
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

<a name="custom-invoice-render"></a>
#### 커스텀 청구서 렌더러 (Custom Invoice Renderer)

기본적으로 Cashier는 `DompdfInvoiceRenderer`로 [dompdf](https://github.com/dompdf/dompdf) 라이브러리를 사용해 청구서를 만듭니다. 원한다면 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현한 커스텀 렌더러를 만들어 사용할 수 있습니다. 예:

```
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * 주어진 청구서를 렌더링해 PDF 바이트를 반환
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

커스텀 렌더러 클래스를 만든 후, 앱 `config/cashier.php`의 `cashier.invoices.renderer` 설정에 클래스 이름을 입력하세요.

<a name="checkout"></a>
## Checkout

Cashier Stripe는 Stripe Checkout도 지원합니다. Stripe Checkout은 미리 만들어진 호스팅 결제 페이지로, 결제 페이지 개발 부담을 줄여줍니다.

아래는 Stripe Checkout 사용법입니다. 더 자세한 내용은 [Stripe Checkout 공식 문서](https://stripe.com/docs/payments/checkout)도 참고하세요.

<a name="product-checkouts"></a>
### 제품 결제 (Product Checkouts)

Stripe 대시보드에서 생성한 제품의 가격으로 Checkout을 시작하려면 billable 모델의 `checkout` 메서드를 사용하세요. 기본적으로 Stripe 가격 ID를 반드시 전달해야 합니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```

필요 시 수량도 지정할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```

배송 성공, 취소 후 리디렉션 URL은 기본 `home` 경로이며, `success_url` 및 `cancel_url` 옵션으로 변경할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```

`success_url` 쿼리 스트링에 `{CHECKOUT_SESSION_ID}`를 포함시키면 Stripe가 실제 체크아웃 세션 ID로 대체합니다:

```
use Illuminate\Http\Request;
use Stripe\Checkout\Session;
use Stripe\Customer;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('checkout-success') . '?session_id={CHECKOUT_SESSION_ID}',
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

기본적으로 Stripe Checkout은 사용자가 직접 사용하는 프로모션 코드를 허용하지 않습니다. 활성화하려면 `allowPromotionCodes` 메서드를 호출하세요:

```
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```

<a name="single-charge-checkouts"></a>
### 일회성 결제 Checkout (Single Charge Checkouts)

Stripe 대시보드에 등록되지 않은 일시 제품에 대해 간단히 결제하려면 billable 모델의 `checkoutCharge` 메서드를 사용하세요. 금액, 제품명, 수량(옵션)을 전달합니다:

```
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```

> [!NOTE]
> `checkoutCharge`는 Stripe에 자동으로 새 제품과 가격을 생성합니다. 미리 Stripe 대시보드에 제품들을 생성해 `checkout` 메서드를 사용하는 편이 권장됩니다.

<a name="subscription-checkouts"></a>
### 구독 Checkout (Subscription Checkouts)

> [!NOTE]
> Stripe Checkout 구독을 사용하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다. 이 웹훅이 데이터베이스 구독 레코드와 관련 아이템을 생성합니다.

Cashier 구독 빌더 메서드를 호출한 후 `checkout` 메서드로 Stripe Checkout 세션을 시작할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```

제품 결제와 마찬가지로 성공, 취소 URL을 옵션으로 지정할 수 있습니다:

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

프로모션 코드도 활성화 가능:

```
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```

> [!NOTE]
> Stripe Checkout에서 구독 빌더의 `anchorBillingCycleOn`, 정산 정책, 결제 정책 등 일부는 적용되지 않습니다. 현재 지원 항목은 [Stripe Checkout 세션 API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참고하세요.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout과 체험 기간

Stripe Checkout으로 체험 기간 설정 가능하지만, 최소 48시간 이상이어야 합니다.

```
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독과 웹훅

Stripe와 Cashier는 웹훅을 통해 구독 상태를 업데이트하므로, 고객이 결제 완료 후 애플리케이션으로 돌아왔을 때 구독이 아직 활성화되지 않았을 수도 있습니다. 이같은 경우 결제 또는 구독 대기 상태임을 사용자에게 알리는 메시지를 띄우는 것이 좋습니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집 (Collecting Tax IDs)

Checkout에서 고객 세금 ID 수집을 활성화하려면 `collectTaxIds` 메서드를 호출하세요:

```
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

이 메서드 호출 시 고객에게 사업자인지 여부를 묻는 체크박스가 표시되고, 회사일 경우 세금 ID를 입력할 수 있습니다.

> [!NOTE]
> 이미 [자동 세금 계산 설정](#tax-configuration) 상태라면 별도 호출 없이 이 기능이 자동 활성화됩니다.

<a name="handling-failed-payments"></a>
## 결제 실패 처리 (Handling Failed Payments)

가끔 구독 또는 단일 결제 실패가 발생합니다. 이때 Cashier는 `Laravel\Cashier\Exceptions\IncompletePayment` 예외를 던집니다. 이 예외를 캐치한 뒤 두 가지 옵션으로 처리할 수 있습니다.

먼저, Cashier의 결제 확인 페이지로 고객을 리디렉션하는 방법입니다. 해당 페이지는 서비스 프로바이더가 기본 경로와 함께 등록합니다. 예:

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

결제 확인 페이지에서 고객은 카드 정보를 다시 입력하고 Stripe 3D Secure 등 추가 인증을 완료합니다. 인증 후 `redirect` 파라미터 URL로 리디렉션되며, `message`(문자열)와 `success`(정수) 쿼리스트링이 붙습니다. 지원 결제 수단 종류는 다음과 같습니다:

- 신용카드
- Alipay
- Bancontact
- BECS 직불
- EPS
- Giropay
- iDEAL
- SEPA 직불

또 다른 방법은 Stripe 대시보드에서 자동 청구 이메일 설정을 켜서 Stripe가 직접 결제 확인 이메일을 발송하게 하는 겁니다. 단, 예외가 발생하면 여전히 고객에게 이메일 확인 안내를 해야 합니다.

`IncompletePayment` 예외는 `charge`, `invoiceFor`, `invoice` 메서드나 `SubscriptionBuilder`의 `create`, `Subscription` 및 `SubscriptionItem` 모델의 `incrementAndInvoice`, `swapAndInvoice` 메서드에서 발생할 수 있습니다.

미완료 결제 여부 확인은 billable 모델 또는 구독 인스턴스에서 `hasIncompletePayment`를 호출하세요:

```
if ($user->hasIncompletePayment('default')) {
    //
}

if ($user->subscription('default')->hasIncompletePayment()) {
    //
}
```

예외 객체의 `payment` 속성에서 상태를 점검할 수 있습니다:

```
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // 결제 의도 상태
    $exception->payment->status;

    // 상태별 조건 체크
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```

<a name="strong-customer-authentication"></a>
## 강화된 고객 인증 (Strong Customer Authentication)

유럽 기반 사업 또는 고객을 대상으로 할 경우, 2019년 9월부터 시행된 EU의 강화된 고객 인증(SCA, Strong Customer Authentication) 규정을 따라야 합니다. Stripe와 Cashier는 이에 대응 가능한 기능을 제공합니다.

> [!NOTE]
> 시작 전 [Stripe의 PSD2 및 SCA 가이드](https://stripe.com/guides/strong-customer-authentication)와 [신규 SCA API 문서](https://stripe.com/docs/strong-customer-authentication)를 확인하세요.

<a name="payments-requiring-additional-confirmation"></a>
### 추가 인증이 필요한 결제 (Payments Requiring Additional Confirmation)

SCA 규정에 따라 결제 진행 시 추가 인증이 필요할 수 있습니다. 이때 Cashier는 `IncompletePayment` 예외를 던지며, [결제 실패 처리](#handling-failed-payments) 문서를 참고해 대응하세요.

Stripe나 Cashier 결제 확인 화면은 은행 또는 카드사별 플로우에 맞춰 카드 인증, 임시 소액 결제, 별도 기기 인증 등 추가 작업을 안내할 수 있습니다.

<a name="incomplete-and-past-due-state"></a>
#### 미완료 및 연체 상태

추가 인증 요구 시 구독이 `incomplete` 또는 `past_due` 상태가 됩니다(`stripe_status` 컬럼 참조). Cashier는 결제 인증 완료 웹훅을 받으면 고객 구독을 자동 활성화합니다.

보다 자세한 내용은 [미완료 및 연체 상태 문서](#incomplete-and-past-due-status)를 참고하세요.

<a name="off-session-payment-notifications"></a>
### 오프 세션 결제 알림 (Off-Session Payment Notifications)

SCA로 인해 구독 갱신 시에도 고객이 결제 확인을 해야 하므로 Cashier가 확인 알림을 전송할 수 있습니다. 알림 클래스 이름을 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수에 설정하세요. 기본 비활성화되어 있으며, 기본 제공 알림 클래스 또는 직접 만든 알림도 사용할 수 있습니다:

```
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

웹훅이 설정되어 있고, Stripe 대시보드에서 `invoice.payment_action_required` 웹훅이 활성 상태여야 합니다. billable 모델은 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다.

> [!NOTE]
> 수동 결제 중인 경우에도 알림이 발송됩니다. Stripe는 수동/오프세션 여부를 구분하지 못합니다. 사용자가 이미 결제를 완료한 경우, 다시 확인 시도는 막혀 추가 결제가 발생하지 않습니다.

<a name="stripe-sdk"></a>
## Stripe SDK

Cashier 객체는 Stripe SDK 객체를 감싼 래퍼입니다. Stripe 객체를 직접 조작하려면 `asStripe` 메서드를 사용하세요:

```
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```

직접 Stripe 구독을 업데이트하려면 `updateStripeSubscription` 메서드를 사용할 수도 있습니다:

```
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

`Cashier` 클래스의 `stripe` 메서드로 직접 `StripeClient`를 사용할 수 있습니다. 예:

```
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```

<a name="testing"></a>
## 테스트 (Testing)

Cashier 사용하는 앱의 테스트 시 Stripe API 호출을 모킹할 수 있으나, Cashier 핵심 동작 일부를 재구현해야 하므로 복잡합니다. 따라서 실제 Stripe API를 호출하는 방향을 권장합니다. 느린 테스트는 별도 PHPUnit 그룹에 분리하세요.

테스트 시작 전 `phpunit.xml`에 테스트용 Stripe 비밀키를 추가하세요:

```
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

테스트 중 Cashier가 Stripe 테스트 환경에 실제 API 요청을 전송합니다. 테스트에 사용할 구독 및 가격 데이터를 Stripe 테스트 계정에 미리 생성해 두면 편리합니다.

> [!TIP]
> Stripe가 제공하는 다양한 [테스트용 카드 번호 및 토큰](https://stripe.com/docs/testing)으로 다양한 청구 시나리오(카드 거절, 실패 등)를 테스트할 수 있습니다.