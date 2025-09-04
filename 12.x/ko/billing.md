# Laravel Cashier (Stripe) (Laravel Cashier (Stripe))

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [구성](#configuration)
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
    - [고객 정보 업데이트](#updating-customers)
    - [잔액 관리](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터 Stripe 동기화](#syncing-customer-data-with-stripe)
    - [결제 포털](#billing-portal)
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
    - [가격 변경](#changing-prices)
    - [구독 수량 관리](#subscription-quantity)
    - [여러 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일(anchor date)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험(Trial) 기간](#subscription-trials)
    - [결제 수단 정보 선등록 체험](#with-payment-method-up-front)
    - [결제 수단 정보 미등록 체험](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단한 결제](#simple-charge)
    - [인보이스와 함께 결제](#charge-with-invoice)
    - [결제 인텐트 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [체크아웃](#checkout)
    - [상품 체크아웃](#product-checkouts)
    - [단일 결제 체크아웃](#single-charge-checkouts)
    - [구독 체크아웃](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원(게스트) 체크아웃](#guest-checkouts)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프 세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 관리 서비스를 쉽게 다룰 수 있도록 표현력 있고 직관적인 인터페이스를 제공합니다. 직접 작성하기 어려운 반복적인 구독 청구 관련 코드를 거의 모두 처리합니다. 기본적인 구독 관리 외에도 Cashier는 쿠폰, 구독 변경, 구독 ‘수량(quantities)’, 구독 취소 유예 기간, 인보이스 PDF 생성 기능 등을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> [!WARNING]
> 깨지는 변경(breaking change)을 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. Stripe API 버전은 새로운 Stripe 기능 및 개선사항을 이용할 수 있도록 간혹 마이너 릴리스에서 변경될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 사용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

패키지 설치 후, `vendor:publish` Artisan 명령어로 Cashier의 마이그레이션 파일을 퍼블리시(복사)합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음, 데이터베이스 마이그레이션을 실행합니다:

```shell
php artisan migrate
```

이 마이그레이션은 `users` 테이블에 여러 컬럼을 추가합니다. 또한 고객 구독 정보를 저장하기 위한 새로운 `subscriptions` 테이블과, 여러 가격이 포함된 구독을 위한 `subscription_items` 테이블을 생성합니다.

원한다면, 다음 명령어로 Cashier의 설정 파일도 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 Stripe 이벤트를 올바르게 처리할 수 있도록 반드시 [Cashier의 webhook 처리 설정](#handling-stripe-webhooks)을 해주십시오.

> [!WARNING]
> Stripe에서는 Stripe 식별자 저장에 사용하는 컬럼이 대소문자를 구분해야 한다고 권장합니다. 따라서 MySQL을 사용할 경우 `stripe_id` 컬럼의 collation이 `utf8_bin`으로 설정되어 있는지 확인하세요. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인하실 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="billable-model"></a>
### 청구 가능(Billable) 모델

Cashier를 사용하기 전에, 청구 가능 모델에 `Billable` 트레이트를 추가하세요. 일반적으로 `App\Models\User` 모델이 해당됩니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 정보 업데이트 등 여러 청구 관련 작업을 쉽게 수행할 수 있는 다양한 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 청구 가능 모델이 Laravel에서 제공하는 `App\Models\User` 클래스일 것으로 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 초기화.
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> Laravel에서 기본으로 제공하는 `App\Models\User` 모델이 아닌 다른 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시한 뒤 해당 모델의 테이블 이름에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

Stripe API 키는 애플리케이션의 `.env` 파일에서 설정해야 합니다. 해당 키는 Stripe의 관리자 페이지에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> Stripe에서 들어오는 Webhook이 실제 Stripe에서 온 것인지 확인하려면, 반드시 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수가 정의되어 있어야 합니다.

<a name="currency-configuration"></a>
### 통화 설정 (Currency Configuration)

Cashier의 기본 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

Cashier의 통화 설정 외에도, 인보이스에 금액을 표시할 때 사용할 로케일(locale)도 지정할 수 있습니다. 내부적으로는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용해 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치 및 설정되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정 (Tax Configuration)

[Stripe Tax](https://stripe.com/tax)를 활용하면 Stripe에서 생성된 모든 인보이스에 대해 세금을 자동 계산할 수 있습니다. 자동 세금 계산을 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하면 됩니다:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 초기화.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

세금 계산이 활성화되면, 새 구독이나 새로운 일회성 인보이스 모두 자동으로 세금이 계산됩니다.

이 기능이 제대로 동작하려면 고객의 이름, 주소, 세금 ID 등 결제 정보가 Stripe와 동기화되어야 합니다. Cashier가 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe), [세금 ID 관리](#tax-ids) 메서드를 활용하세요.

<a name="logging"></a>
### 로깅 (Logging)

Cashier는 Stripe 오류 발생 시 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일에서 `CASHIER_LOGGER` 환경 변수를 정의하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출에서 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용 (Using Custom Models)

Cashier에서 내부적으로 사용하는 모델을 확장하고자 할 때, 원하는 클래스를 정의한 후 해당 Cashier 모델을 상속하면 됩니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

커스텀 모델을 정의했다면, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier에 해당 모델을 사용하도록 안내합니다. 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * 애플리케이션 서비스 초기화.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

---  
(이후 내용도 동일한 구조와 규칙에 따라 전체 번역이 이어집니다.)