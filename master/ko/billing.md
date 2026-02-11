# Laravel Cashier (Stripe)

- [소개](#introduction)
- [Cashier 업그레이드](#upgrading-cashier)
- [설치](#installation)
- [설정](#configuration)
    - [과금 가능(Billable) 모델](#billable-model)
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
    - [고객 정보 수정](#updating-customers)
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
    - [구독 수량 관리](#subscription-quantity)
    - [다중 상품 구독](#subscriptions-with-multiple-products)
    - [다중 구독](#multiple-subscriptions)
    - [사용량 기반 과금](#usage-based-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 기준일(Anchor Date)](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험(Trial)](#subscription-trials)
    - [결제 수단 선수집 체험](#with-payment-method-up-front)
    - [결제 수단 없이 체험 시작](#without-payment-method-up-front)
    - [체험 연장](#extending-trials)
- [Stripe Webhook 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 청구](#single-charges)
    - [간단 결제](#simple-charge)
    - [인보이스를 통한 결제](#charge-with-invoice)
    - [결제 의도(Payment Intent) 생성](#creating-payment-intents)
    - [결제 환불](#refunding-charges)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정 인보이스 조회](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [Checkout(체크아웃)](#checkout)
    - [상품 체크아웃](#product-checkouts)
    - [단일 결제 체크아웃](#single-charge-checkouts)
    - [구독 체크아웃](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
    - [비회원 체크아웃](#guest-checkouts)
- [실패한 결제 처리](#handling-failed-payments)
    - [결제 확인](#confirming-payments)
- [강화된 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 인증이 필요한 결제](#payments-requiring-additional-confirmation)
    - [Off-session 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 과금(subscription billing) 서비스를 손쉽고 유연하게 사용할 수 있는 인터페이스를 제공합니다. Cashier를 사용하면 직접 반복적으로 작성해야 할 구독 과금 관련 코드 대부분을 자동으로 처리할 수 있습니다. 기본적인 구독 관리 외에도, Cashier는 쿠폰, 구독 변경, 구독 수량, 구독 취소 유예 기간(grace periods), 인보이스 PDF 생성 등 다양한 기능을 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드 (Upgrading Cashier)

Cashier를 새로운 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인하는 것이 중요합니다.

> [!WARNING]
> 예기치 않은 변경을 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16 버전은 Stripe API `2025-06-30.basil` 버전을 사용합니다. Stripe API 버전은 Stripe 기능 및 개선사항 적용을 위해 마이너 릴리스 시 업데이트될 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용해 Stripe용 Cashier 패키지를 설치하세요:

```shell
composer require laravel/cashier
```

패키지 설치 후, `vendor:publish` Artisan 명령어를 사용해 Cashier의 마이그레이션 파일을 게시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

그리고 데이터베이스를 마이그레이션합니다:

```shell
php artisan migrate
```

Cashier 마이그레이션은 `users` 테이블에 필요한 컬럼을 추가합니다. 또한, 고객 구독 정보를 저장할 `subscriptions` 테이블, 여러 가격을 가진 구독을 위한 `subscription_items` 테이블도 생성합니다.

원한다면, Cashier의 설정 파일도 다음 명령어로 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```

마지막으로, Stripe 이벤트를 올바르게 처리하려면 반드시 [Cashier의 웹훅 핸들링을 설정](#handling-stripe-webhooks)해야 합니다.

> [!WARNING]
> Stripe에서는 Stripe 식별자 저장용 컬럼은 대소문자 구분을 권장합니다. MySQL을 사용할 경우, `stripe_id` 컬럼의 collation이 `utf8_bin`으로 설정되어 있는지 확인하세요. 추가 정보는 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 참고할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="billable-model"></a>
### 과금 가능(Billable) 모델

Cashier를 사용하려면, 우선 결제 대상 모델에 `Billable` 트레이트를 추가해야 합니다. 일반적으로 이 모델은 `App\Models\User`입니다. 이 트레이트 덕분에 구독 생성, 쿠폰 적용, 결제 수단 변경 등 다양한 결제 관련 작업을 간편하게 처리할 수 있습니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

Cashier는 기본적으로 `App\Models\User` 모델을 과금 모델로 가정합니다. 다르게 사용하고 싶다면 `useCustomerModel` 메서드를 활용해 다른 모델로 지정할 수 있습니다. 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 호출합니다:

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
> 기본 `App\Models\User` 모델이 아닌 다른 모델을 사용하는 경우, 반드시 [Cashier 마이그레이션](#installation)을 직접 게시 및 수정하여 대체 모델의 테이블 구조와 맞게 테이블명을 바꿔주어야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, Stripe API 키를 `.env` 파일에 설정하세요. 해당 정보는 Stripe 관리페이지에서 확인할 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

> [!WARNING]
> `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경변수가 반드시 정의되어 있어야 합니다. 이 값은 들어오는 웹훅 요청이 Stripe에서 온 것인지 식별하는 데 사용됩니다.

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면, `.env` 파일에 `CASHIER_CURRENCY` 환경변수를 추가합니다:

```ini
CASHIER_CURRENCY=eur
```

통화 외에도 인보이스에 표시될 금액 포맷에 사용할 로케일(locale)도 지정할 수 있습니다. Cashier는 내부적으로 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe가 생성하는 모든 인보이스에 대해 세금을 자동으로 계산할 수 있습니다. 세금 자동 계산 기능을 활성화하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요:

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

이제부터 새로 생성되는 구독이나 단일 인보이스 모두 자동으로 세금이 계산됩니다.

정확한 세금 계산을 위해서는 고객의 이름, 주소, 세금 ID 등 결제 정보를 Stripe와 동기화해야 합니다. Cashier에서 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 관련 메서드를 활용하시기 바랍니다.

<a name="logging"></a>
### 로깅

Cashier에서는 Stripe에서 발생한 치명적인 에러를 기록할 때 사용할 로그 채널을 지정할 수 있습니다. 이를 위해 `.env` 파일에 `CASHIER_LOGGER` 환경변수를 추가하세요:

```ini
CASHIER_LOGGER=stack
```

Stripe API 호출 시 발생하는 예외는 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier 내부에서 사용하는 모델을 확장하여 커스텀 모델을 정의할 수 있습니다. 예를 들어, 구독 모델을 직접 확장하려면 아래와 같이 선언하세요:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```

이후, Cashier가 이 커스텀 모델을 사용하도록 지정하려면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 아래와 같이 등록합니다:

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

<!-- 이하 번역 계속 -->
