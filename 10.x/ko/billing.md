# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [결제 가능 모델](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로깅](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [제품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터 Stripe와 동기화](#syncing-customer-data-with-stripe)
    - [청구 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [결제 수단 존재 확인](#payment-method-presence)
    - [기본 결제 수단 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [요금 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [측정형 과금](#metered-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 Anchor 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판(Trial)](#subscription-trials)
    - [결제 수단 정보 선입력 체험판](#with-payment-method-up-front)
    - [결제 수단 정보 없이 체험판 제공](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단 결제](#simple-charge)
    - [인보이스와 함께 결제](#charge-with-invoice)
    - [결제 Intent 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [제품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 Checkout](#guest-checkouts)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [실패 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 청구 서비스를 위한 표현적이고 유연한 인터페이스를 제공합니다. 여러분이 직접 작성하기 번거로운 구독 청구 관련 코드 대부분을 Cashier가 처리해줍니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰 처리, 요금제 교체, 구독 “수량(quantities)”, 구독 취소 유예기간, 인보이스 PDF 생성까지 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

새 버전의 Cashier로 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인하십시오.

> [!WARNING]  
> 주요 변경 사항이 발생하는 것을 막기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. Stripe API 버전은 Stripe의 새로운 기능 및 개선사항을 활용하기 위해서 소규모 릴리즈(minor release) 시점에만 업데이트됩니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자로 Stripe용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier
```

패키지를 설치한 후, Cashier의 마이그레이션을 `vendor:publish` Artisan 명령어로 발행하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음, 데이터베이스를 마이그레이트하세요:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하며, 모든 고객의 구독 정보를 저장할 `subscriptions` 테이블과 다중 가격 구독을 위한 `subscription_items` 테이블도 생성합니다.

원한다면, Cashier의 설정 파일도 아래 Artisan 명령어로 발행할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 Stripe의 모든 이벤트를 올바르게 처리할 수 있도록 [Cashier Webhook 핸들링을 설정](#handling-stripe-webhooks)하세요.

> [!WARNING]  
> Stripe는 Stripe 식별자를 저장하는 모든 컬럼이 대소문자를 구분해야 한다고 권장합니다. 따라서 MySQL 사용 시 `stripe_id` 컬럼의 정렬 방식(collation)을 `utf8_bin`으로 설정해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 결제 가능 모델(Billable Model)

Cashier 사용 전, billable 모델 정의에 `Billable` 트레이트를 추가하세요. 일반적으로 이 모델은 `App\Models\User`일 것입니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 자주 쓰는 결제 관련 작업을 쉽게 할 수 있도록 여러 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 billable 모델이 Laravel에서 제공하는 `App\Models\User` 클래스일 것으로 가정합니다. 다른 모델을 사용하고 싶다면 `useCustomerModel` 메서드로 지정할 수 있습니다. 주로 이 메서드는 `AppServiceProvider`의 `boot` 메서드 내에서 호출합니다:

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
> Laravel 기본 `App\Models\User` 모델이 아닌 다른 모델을 사용할 경우, 제공된 [Cashier 마이그레이션](#installation)을 발행 및 수정하여 여러분의 모델 테이블명에 맞게 조정해주어야 합니다.

<a name="api-keys"></a>
### API 키

이제 `.env` 파일에 Stripe API 키를 설정하세요. Stripe 대시보드에서 API 키를 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]  
> `STRIPE_WEBHOOK_SECRET` 환경 변수가 `.env` 파일에 반드시 정의되어야 하며, 이 값은 Stripe webhooks가 실제로 Stripe에서 온 것인지 검증하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면 `.env` 파일에 `CASHIER_CURRENCY` 환경 변수를 설정하세요:

```ini
CASHIER_CURRENCY=eur
```

통화 설정 외에, 인보이스에 표시되는 금액의 로케일도 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용해 통화 로케일을 설정합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 `ext-intl` PHP 확장 모듈이 서버에 설치 및 설정되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe에서 생성된 모든 인보이스에 대해 자동으로 세금 계산이 가능합니다. 자동 세금 계산을 활성화하려면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

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

세금 계산이 활성화되면, 새로 생성되는 구독이나 단일 인보이스 모두에서 자동으로 세금이 계산됩니다.

이 기능이 올바르게 작동하려면 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe와 동기화되어야 합니다. 이를 위해 Cashier가 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID](#tax-ids) 메서드를 활용하세요.

> [!WARNING]
> [단일 결제](#single-charges) 또는 [단일 결제 Checkout](#single-charge-checkouts)에는 세금이 자동 계산되지 않습니다.

<a name="logging"></a>
### 로깅

치명적인 Stripe 오류가 발생했을 때 Cashier로 로그가 남도록 로그 채널을 지정할 수 있습니다. `.env` 파일에 `CASHIER_LOGGER` 환경 변수를 설정하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출로 발생한 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier 내부에서 사용하는 모델을 상속하여 자유롭게 여러분만의 모델을 정의할 수 있습니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

정의한 모델을 Cashier에서 사용하도록 지정하려면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 지정하세요:

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

...

---

##### (이하 모든 마크다운 목차 및 섹션의 번역 또한 위의 스타일(마크다운, 코드/URL/예시 외 부분 번역, 용어 일관성 유지)로 진행됩니다. 길이상 추가 번역이 필요하시면 이어서 제공해 드릴 수 있습니다.)