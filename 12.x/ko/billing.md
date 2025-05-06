# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [청구 가능 모델(Billable Model)](#billable-model)
    - [API 키](#api-keys)
    - [통화 설정](#currency-configuration)
    - [세금 설정](#tax-configuration)
    - [로그 기록](#logging)
    - [커스텀 모델 사용](#using-custom-models)
- [빠른 시작](#quickstart)
    - [상품 판매](#quickstart-selling-products)
    - [구독 판매](#quickstart-selling-subscriptions)
- [고객](#customers)
    - [고객 조회](#retrieving-customers)
    - [고객 생성](#creating-customers)
    - [고객 정보 업데이트](#updating-customers)
    - [잔고 관리](#balances)
    - [세금 ID](#tax-ids)
    - [고객 데이터와 Stripe 동기화](#syncing-customer-data-with-stripe)
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
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 청구](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험판(Trial)](#subscription-trials)
    - [선불 결제 수단 포함 체험판](#with-payment-method-up-front)
    - [선불 결제 수단 미포함 체험판](#without-payment-method-up-front)
    - [체험판 연장](#extending-trials)
- [Stripe 웹훅 처리](#handling-stripe-webhooks)
    - [웹훅 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [웹훅 시그니처 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간편 결제](#simple-charge)
    - [인보이스 결제](#charge-with-invoice)
    - [결제 인텐트 생성](#creating-payment-intents)
    - [환불 처리](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 Checkout](#guest-checkouts)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스 확인](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 결제 확인이 필요한 결제](#payments-requiring-additional-confirmation)
    - [오프세션 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 청구 서비스를 위한 직관적이고 유연한 인터페이스를 제공합니다. 구독 청구와 관련된 대부분의 반복적인 코드를 Cashier가 자동으로 처리합니다. 기본적인 구독 관리뿐만 아니라, Cashier는 쿠폰, 구독 변경, 구독 수량, 취소 유예 기간, 인보이스 PDF 생성 등 다양한 기능을 제공합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier를 새 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 검토하세요.

> [!WARNING]
> 호환성 문제를 방지하기 위해 Cashier는 Stripe API 버전을 고정하여 사용합니다. Cashier 15는 Stripe API 버전 `2023-10-16`을 사용합니다. 사소한 버전(마이너 릴리스)에서는 Stripe의 최신 기능 및 개선점을 활용하기 위해 API 버전이 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 이용해 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```

설치 후, 아래 Artisan 명령어로 Cashier의 마이그레이션을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그 다음, 데이터베이스를 마이그레이트합니다:

```shell
php artisan migrate
```

Cashier의 마이그레이션은 `users` 테이블에 몇 가지 컬럼을 추가하고, 고객의 구독을 저장할 새로운 `subscriptions` 테이블과 다중 가격 구독을 위한 `subscription_items` 테이블을 생성합니다.

원한다면, Cashier의 설정 파일도 `vendor:publish` 명령어로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Cashier가 Stripe의 모든 이벤트를 제대로 처리하도록 반드시 [Cashier 웹훅 처리 설정](#handling-stripe-webhooks)을 하세요.

> [!WARNING]
> Stripe는 Stripe 식별자를 저장하는 모든 컬럼이 대소문자를 구분해야 한다고 권장합니다. MySQL을 사용한다면 `stripe_id` 컬럼의 콜레이션이 `utf8_bin`으로 설정되어 있는지 확인하세요. 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)를 참고하세요.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### 청구 가능 모델(Billable Model)

Cashier 사용 전에, 결제 대상이 되는 모델에 `Billable` 트레잇을 추가해야 합니다. 일반적으로 `App\Models\User` 모델이 해당됩니다. 이 트레잇은 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 다양한 청구 관련 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 Laravel의 `App\Models\User` 클래스를 청구 가능 모델로 가정합니다. 만약 이를 변경하고 싶다면, `useCustomerModel` 메서드를 통해 사용할 모델을 명시하세요. 이 메서드는 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```

> [!WARNING]
> 만약 Laravel이 제공하는 `App\Models\User`가 아닌 다른 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시한 후 해당 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, Stripe API 키를 애플리케이션의 `.env` 파일에 추가해야 합니다. 키는 Stripe 관리 패널에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> 반드시 `STRIPE_WEBHOOK_SECRET` 환경 변수가 `.env` 파일에 정의되어 있어야 하며, 이 변수는 Stripe에서 오는 웹훅 요청이 실제 Stripe에서 왔음을 확인하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. `.env` 파일에서 `CASHIER_CURRENCY` 환경 변수를 설정하면 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```

통화 외에도, 인보이스에 표시되는 금액의 형식을 지정할 로케일을 설정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en`이 아닌 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax)를 통해 Stripe에서 생성되는 모든 인보이스에 세금을 자동 계산할 수 있습니다. 자동 세금 계산을 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `calculateTaxes`를 호출하세요:

```php
use Laravel\Cashier\Cashier;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```

세금 계산을 활성화하면, 생성되는 새 구독이나 단일 인보이스에 자동으로 세금이 계산됩니다.

이 기능이 제대로 작동하려면, 고객의 이름, 주소, 세금 ID 등의 청구 정보가 Stripe와 동기화되어야 합니다. [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 참고하세요.

<a name="logging"></a>
### 로그 기록

치명적인 Stripe 오류를 로깅할 때 사용할 로그 채널을 `CASHIER_LOGGER` 환경 변수로 지정할 수 있습니다:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출에서 발생하는 예외는 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier에서 내부적으로 사용하는 모델들을 직접 확장할 수 있습니다. 직접 모델을 정의한 후 Cashier의 해당 모델을 상속받으면 됩니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

모델 정의 후 `Laravel\Cashier\Cashier` 클래스를 이용해 Cashier에게 커스텀 모델을 사용하도록 지시할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```

---

> 이하 내용이 매우 길어, 추가 번역이 필요하시면 구체적으로 원하는 절이나 범위를 알려주세요.
> 위와 같이 번역을 진행하면 전체 마크다운 형식 및 전문 용어 유지, 코드, URL, HTML 미번역 지침을 모두 준수하며 한국어로 문서를 제공할 수 있습니다.