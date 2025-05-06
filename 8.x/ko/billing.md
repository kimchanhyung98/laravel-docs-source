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
    - [고객 정보 수정](#updating-customers)
    - [잔액](#balances)
    - [세금 ID](#tax-ids)
    - [Stripe와 고객 데이터 동기화](#syncing-customer-data-with-stripe)
    - [결제 포털](#billing-portal)
- [결제 수단](#payment-methods)
    - [결제 수단 저장](#storing-payment-methods)
    - [결제 수단 조회](#retrieving-payment-methods)
    - [사용자가 결제 수단을 갖고 있는지 확인](#check-for-a-payment-method)
    - [기본 결제 수단 정보 업데이트](#updating-the-default-payment-method)
    - [결제 수단 추가](#adding-payment-methods)
    - [결제 수단 삭제](#deleting-payment-methods)
- [구독](#subscriptions)
    - [구독 생성](#creating-subscriptions)
    - [구독 상태 확인](#checking-subscription-status)
    - [가격 변경](#changing-prices)
    - [구독 수량](#subscription-quantity)
    - [다중 가격 구독](#multiprice-subscriptions)
    - [계량형 과금](#metered-billing)
    - [구독 세금](#subscription-taxes)
    - [구독 Anchor 날짜](#subscription-anchor-date)
    - [구독 취소](#cancelling-subscriptions)
    - [구독 재개](#resuming-subscriptions)
- [구독 체험 기간](#subscription-trials)
    - [카드 정보 선등록 시](#with-payment-method-up-front)
    - [카드 정보 선등록 없이](#without-payment-method-up-front)
    - [체험 기간 연장](#extending-trials)
- [Stripe Webhooks 처리](#handling-stripe-webhooks)
    - [Webhook 이벤트 핸들러 정의](#defining-webhook-event-handlers)
    - [Webhook 서명 검증](#verifying-webhook-signatures)
- [단일 결제](#single-charges)
    - [간단 결제](#simple-charge)
    - [인보이스 결제](#charge-with-invoice)
    - [결제 환불](#refunding-charges)
- [Checkout](#checkout)
    - [상품 Checkout](#product-checkouts)
    - [단일 결제 Checkout](#single-charge-checkouts)
    - [구독 Checkout](#subscription-checkouts)
    - [세금 ID 수집](#collecting-tax-ids)
- [인보이스](#invoices)
    - [인보이스 조회](#retrieving-invoices)
    - [예정된 인보이스](#upcoming-invoices)
    - [구독 인보이스 미리보기](#previewing-subscription-invoices)
    - [인보이스 PDF 생성](#generating-invoice-pdfs)
- [결제 실패 처리](#handling-failed-payments)
- [강력한 고객 인증(SCA)](#strong-customer-authentication)
    - [추가 인증이 필요한 결제](#payments-requiring-additional-confirmation)
    - [Off-session 결제 알림](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 위한 표현력 있고 유연한 인터페이스를 제공합니다. Cashier는 여러분이 작성하고 싶지 않은 대부분의 반복되는 구독 결제 코드를 대신 처리해줍니다. 기본적인 구독 관리뿐만 아니라, Cashier는 쿠폰, 구독 변경, 구독 "수량", 취소 유예 기간, 인보이스 PDF 생성도 지원합니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

Cashier를 새로운 버전으로 업그레이드할 때에는 반드시 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

> {note} 주요 변경사항으로 인한 문제를 방지하기 위해, Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 13은 Stripe API 버전 `2020-08-27`을 사용하며, Stripe API 버전은 새로운 Stripe 기능과 개선사항을 활용하기 위해 마이너 릴리스에서 업데이트됩니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치하세요.

    composer require laravel/cashier

> {note} Cashier가 모든 Stripe 이벤트를 올바르게 처리하도록 반드시 [Cashier의 webhook 처리 설정](#handling-stripe-webhooks)을 완료해야 합니다.

<a name="database-migrations"></a>
### 데이터베이스 마이그레이션

Cashier의 서비스 프로바이더는 자체 데이터베이스 마이그레이션 디렉터리를 등록합니다. 따라서 패키지 설치 후 반드시 데이터베이스 마이그레이션을 진행해야 합니다. Cashier 마이그레이션은 `users` 테이블에 여러 컬럼을 추가하고, 고객의 모든 구독 정보를 저장하기 위한 새로운 `subscriptions` 테이블을 생성합니다.

    php artisan migrate

Cashier에서 제공하는 기본 마이그레이션을 덮어쓰고 싶다면, `vendor:publish` Artisan 명령을 사용할 수 있습니다.

    php artisan vendor:publish --tag="cashier-migrations"

Cashier 마이그레이션을 아예 실행하지 않으려면, Cashier에서 제공하는 `ignoreMigrations` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `register` 메서드에 추가해야 합니다.

    use Laravel\Cashier\Cashier;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        Cashier::ignoreMigrations();
    }

> {note} Stripe는 Stripe 식별자를 저장하는 모든 컬럼에 대소문자 구분을 권장합니다. MySQL을 사용할 경우, `stripe_id` 컬럼의 정렬(collation)이 반드시 `utf8_bin`이어야 합니다. 자세한 내용은 [Stripe 공식 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
## 설정

<a name="billable-model"></a>
### Billable 모델

Cashier 사용 전, billable 모델 정의에 `Billable` 트레이트를 추가하세요. 대개 `App\Models\User` 모델이 될 것입니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트 등 다양한 과금 작업을 위한 메서드를 제공합니다.

    use Laravel\Cashier\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

Cashier는 기본적으로 Laravel의 `App\Models\User` 클래스를 billable 모델로 사용합니다. 변경하려면, `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 주로 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

    use App\Models\Cashier\User;
    use Laravel\Cashier\Cashier;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Cashier::useCustomerModel(User::class);
    }

> {note} Laravel에서 제공하는 기본 `App\Models\User` 모델이 아닌 모델을 사용할 경우, [Cashier 마이그레이션](#installation)을 퍼블리시한 후 해당 모델의 테이블명에 맞게 수정해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에 Stripe API 키를 설정하세요. Stripe API 키는 Stripe 관리 콘솔에서 얻을 수 있습니다.

    STRIPE_KEY=your-stripe-key
    STRIPE_SECRET=your-stripe-secret

<a name="currency-configuration"></a>
### 통화 설정

Cashier의 기본 통화는 미국 달러(USD)입니다. 기본 통화를 변경하려면, `.env` 파일의 `CASHIER_CURRENCY` 환경변수를 설정하세요.

    CASHIER_CURRENCY=eur

또한 Cashier에서 송장에 표시될 금액을 포맷팅할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로 Cashier는 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다.

    CASHIER_CURRENCY_LOCALE=nl_BE

> {note} `en` 이외의 로케일을 사용하려면, 서버에 `ext-intl` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="tax-configuration"></a>
### 세금 설정

[Stripe Tax](https://stripe.com/tax) 덕분에 Stripe가 생성한 모든 인보이스의 세금을 자동으로 계산할 수 있습니다. 자동 세금 계산을 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `calculateTaxes` 메서드를 호출하세요.

    use Laravel\Cashier\Cashier;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Cashier::calculateTaxes();
    }

세금 계산이 활성화되면, 새 구독 및 단일 인보이스에도 자동으로 세금 계산이 적용됩니다.

이 기능이 제대로 동작하려면 고객의 이름, 주소, 세금 ID 등 청구 정보가 Stripe와 동기화되어야 합니다. 이를 위해 Cashier에서 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [Tax ID](#tax-ids) 기능을 사용할 수 있습니다.

> {note} 현재 [단일 결제](#single-charges)나 [단일 결제 Checkout](#single-charge-checkouts)에는 세금이 계산되지 않습니다. 또한 Stripe Tax는 베타 기간 동안 "초대제"로 운영되고 있으므로 [Stripe Tax 웹사이트](https://stripe.com/tax#request-access)를 통해 접근 권한을 신청할 수 있습니다.

<a name="logging"></a>
### 로깅

Cashier는 Stripe의 치명적인 오류를 기록할 때 사용할 로그 채널을 지정할 수 있습니다. 애플리케이션의 `.env` 파일에서 `CASHIER_LOGGER` 환경변수를 정의하세요.

    CASHIER_LOGGER=stack

Stripe API 호출로 발생하는 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 커스텀 모델 사용

Cashier가 내부적으로 사용하는 모델을 확장하여 직접 정의할 수 있습니다.

    use Laravel\Cashier\Subscription as CashierSubscription;

    class Subscription extends CashierSubscription
    {
        // ...
    }

모델을 정의한 후, Cashier에 해당 커스텀 모델을 사용하도록 지시하세요. 주로 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다.

    use App\Models\Cashier\Subscription;
    use App\Models\Cashier\SubscriptionItem;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Cashier::useSubscriptionModel(Subscription::class);
        Cashier::useSubscriptionItemModel(SubscriptionItem::class);
    }

...

**(중략)**

*너무 긴 문서로 인해 이곳에 전체를 표시할 수 없습니다. 만약 이후 추가 번역이 필요하시거나 특정 섹션을 요청하신다면, 해당 섹션을 지정해주시면 신속히 번역해 드리겠습니다.*