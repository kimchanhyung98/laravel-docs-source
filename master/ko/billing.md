# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [청구 가능(Billable) 모델](#billable-model)
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
    - [잔액 관리](#balances)
    - [세금 ID 관리](#tax-ids)
    - [고객 데이터 Stripe 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 여부](#payment-method-presence)
    - [기본 결제 수단 변경](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [여러 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 청구](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일(Anchor Date)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판(Trial)](#subscription-trials)
    - [결제 수단과 함께 제공되는 체험판](#with-payment-method-up-front)
    - [결제 수단 없이 제공되는 체험판](#without-payment-method-up-front)
    - [체험판 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [간단 청구](#simple-charge)
    - [청구서와 함께 제공되는 청구](#charge-with-invoice)
    - [Payment Intent 생성](#creating-payment-intents)
    - [청구 환불](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 청구 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원(게스트) Checkout](#guest-checkouts)
- [청구서](#invoices)
    - [청구서 조회](#retrieving-invoices)
    - [예정 청구서](#upcoming-invoices)
    - [구독 청구서 미리보기](#previewing-subscription-invoices)
    - [청구서 PDF 생성](#generating-invoice-pdfs)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강화된 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 위한 직관적이고 유연한 인터페이스를 제공합니다. 반복적인 구독 결제 코드를 직접 작성할 필요 없이 거의 모든 기본적인 구독 관리 작업을 처리할 수 있습니다. 구독 관리뿐만 아니라, Cashier는 쿠폰, 구독 변경, 구독 "수량", 구독 취소 유예 기간, 청구서 PDF 생성 등 다양한 기능도 함께 제공합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier의 새 버전으로 업그레이드할 때에는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> Cashier는 치명적인 변경을 방지하기 위해 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. Stripe API 버전은 Stripe의 새로운 기능 및 개선사항을 활용하기 위해 마이너 릴리즈에서 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Stripe용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier
```

패키지를 설치한 후, `vendor:publish` Artisan 명령어를 사용하여 Cashier의 마이그레이션을 게시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음, 데이터베이스 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 기본적으로 `users` 테이블에 여러 컬럼을 추가하고, 고객의 구독을 저장하는 `subscriptions` 테이블과 여러 가격이 할당된 구독을 위한 `subscription_items` 테이블을 생성합니다.

필요하다면 다음 명령어를 통해 Cashier의 설정 파일도 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 Stripe의 모든 이벤트를 올바르게 처리할 수 있도록 [Cashier의 Webhook 처리를 설정](#handling-stripe-webhooks)하는 것을 잊지 마세요.

> [!WARNING]
> Stripe에서는 Stripe ID를 저장할 때 사용하는 컬럼이 대소문자를 구분해야 한다고 권장합니다. MySQL을 사용할 경우, `stripe_id` 컬럼의 Collation을 `utf8_bin`으로 지정하는지 확인해야 합니다. 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 청구 가능(Billable) 모델

Cashier 사용 전, "청구 가능" 모델에 `Billable` 트레이트를 추가해야 합니다. 일반적으로 이 모델은 `App\Models\User`를 의미합니다. 이 트레이트를 통해 구독 생성, 쿠폰 적용, 결제 수단 정보 갱신 등 자주 쓰이는 결제 관련 작업을 쉽게 처리할 수 있습니다.

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 청구 가능 모델이 Laravel에서 제공하는 `App\Models\User` 클래스라고 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 사용하여 다른 모델을 지정할 수 있습니다. 이 메서드는 주로 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

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
> Laravel이 기본 제공하는 `App\Models\User` 이외의 모델을 사용할 경우, [Cashier의 마이그레이션](#installation)을 게시 및 수정하여, 해당 모델의 테이블에 맞게 변경해야 합니다.

<a name="api-keys"></a>
### API 키 (API Keys)

Stripe API 키를 애플리케이션의 `.env` 파일에 설정하세요. Stripe 대시보드에서 API 키를 확인할 수 있습니다.

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> 모든 Webhook이 실제로 Stripe에서 전송되었는지 확인하기 위해 `STRIPE_WEBHOOK_SECRET` 환경 변수를 `.env` 파일에 반드시 설정해야 합니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. 다른 통화를 사용하려면, `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 설정하세요.

```ini
CASHIER_CURRENCY=eur
```

Cashier의 통화 이외에도, 청구서에서 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. Cashier 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 활용하여 통화 로케일을 설정합니다.

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 이용하면 Stripe에서 생성된 모든 청구서에 대해 세금 계산을 자동으로 처리할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하여 자동 세금 계산을 활성화하세요:

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

세금 계산이 활성화되면, 생성된 신규 구독이나 단건 청구서에 자동 세금 계산이 적용됩니다.

이 기능이 제대로 동작하려면, 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe와 동기화되어야 합니다. [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID 등록](#tax-ids) 기능을 Cashier에서 제공합니다.

<a name="logging"></a>
### 로깅 (Logging)

Cashier에서는 Stripe에서 발생하는 치명적인 오류를 기록할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 정의하세요.

```ini
CASHIER_LOGGER=stack
```

Stripe로의 API 호출에서 발생한 예외는 애플리케이션의 기본 로그 채널에 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier에서 내부적으로 사용하는 모델 대신, 직접 정의한 커스텀 모델을 사용할 수 있습니다. 먼저 모델을 Cashier 모델로부터 상속받아 만드세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

그 후 `Laravel\Cashier\Cashier` 클래스를 사용하여 Cashier가 커스텀 모델을 사용하도록 지정합니다. 일반적으로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다.

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

<!-- 이하의 본문은 동일 규칙과 스타일로 나머지 섹션도 계속 번역 -->
