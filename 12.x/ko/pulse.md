# 라라벨 Pulse (Laravel Pulse)

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이즈](#dashboard-customization)
    - [사용자 해결](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [항목 캡처](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [별도의 데이터베이스 사용](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황에 대한 인사이트를 한눈에 제공합니다. Pulse를 사용하면 느린 작업(jobs) 및 엔드포인트 등 병목 현상을 추적하고, 가장 활발한 사용자를 찾는 등 다양한 분석이 가능합니다.

단일 이벤트의 심층 디버깅이 필요하다면 [Laravel Telescope](/docs/12.x/telescope) 문서도 참고해 주세요.

<a name="installation"></a>
## 설치

> [!WARNING]
> Pulse의 공식 스토리지 구현은 현재 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다. 다른 데이터베이스 엔진을 사용한다면 Pulse 데이터용으로 별도의 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다.

Pulse는 Composer 패키지 관리자를 이용하여 설치할 수 있습니다.

```shell
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 Pulse 구성 파일과 마이그레이션 파일을 공개(publish)해야 합니다.

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터 저장에 필요한 테이블 생성을 위해 `migrate` 명령어를 실행합니다.

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면 `/pulse` 라우트를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스가 아닌 별도의 데이터베이스에 저장하고 싶다면, [전용 데이터베이스 연결 지정 방법](#using-a-different-database)을 참고하세요.

<a name="configuration"></a>
### 구성

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션, 신규 레코더 등록, 고급 옵션을 구성하려면 `config/pulse.php` 구성 파일을 공개(publish)할 수 있습니다.

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드

<a name="dashboard-authorization"></a>
### 인가

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 이 대시보드는 `local` 환경에서만 접근할 수 있으므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이즈하여 인가를 설정해야 합니다. 이 작업은 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```

<a name="dashboard-customization"></a>
### 커스터마이즈

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰를 공개(publish)해서 수정할 수 있습니다. 대시보드 뷰 파일은 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 생성됩니다.

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 동작하며, 자바스크립트 자산을 빌드할 필요 없이 카드와 레이아웃을 쉽게 커스터마이즈할 수 있습니다.

이 파일 내에서 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며 카드들을 위한 그리드 레이아웃을 제공합니다. 대시보드를 전체 화면 너비로 표시하고 싶다면 해당 컴포넌트에 `full-width` 속성을 전달하면 됩니다.

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12칸 컬럼 그리드를 생성하지만, `cols` 속성을 이용해 그리드 칸 수를 변경할 수 있습니다.

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 `cols`와 `rows` 속성을 받아서 위치와 차지하는 공간을 제어할 수 있습니다.

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드는 카드 전체를 스크롤 없이 확인하고 싶을 때 `expand` 속성을 사용해 확장형 표시가 가능합니다.

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 해결

Application Usage(애플리케이션 사용) 카드처럼 사용자 정보를 표시하는 카드의 경우, Pulse는 사용자의 ID만 기록합니다. 대시보드 렌더링 시에는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 가져오고, Gravatar 웹 서비스를 통해 아바타를 표시합니다.

필드와 아바타 표시 방식을 커스터마이즈하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 호출하면 됩니다.

`user` 메서드는 표시할 `Authenticatable` 모델을 매개변수로 받아, 사용자에 대한 `name`, `extra`, `avatar` 정보를 담은 배열을 반환해야 합니다.

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```

> [!NOTE]
> 인증된 사용자를 캡처하고 조회하는 방식을 완전히 커스터마이즈하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 인터페이스를 구현하고 라라벨의 [서비스 컨테이너](/docs/12.x/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어가 실행 중인 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 리포팅에 대한 자세한 정보는 [servers 레코더](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체하면 일정 시간 후 Pulse 대시보드에서 비활성 서버의 표시를 중단하고 싶을 수 있습니다. 이럴 때 `ignore-after` 속성을 사용하면 비활성 서버가 Pulse 대시보드에서 제거되는 시간을 초 단위로 지정할 수 있습니다. 또는 `1 hour`, `3 days and 1 hour`와 같이 상대적 시간 형태의 문자열도 입력할 수 있습니다.

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용

`<livewire:pulse.usage />` 카드는 애플리케이션에서 요청을 보내거나 작업을 디스패치하며 느린 요청을 경험한 상위 10명의 사용자를 표시합니다.

모든 사용 지표를 한 화면에서 보고 싶으면, 카드를 여러 번 포함시키고 `type` 속성을 지정하면 됩니다.

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 조회하고 표시하는 방식을 커스터마이즈하는 방법은 [사용자 해결](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션에서 요청이나 작업이 매우 많이 발생한다면, [샘플링](#sampling) 기능을 활성화하는 것이 좋습니다. 자세한 내용은 [user requests 레코더](#user-requests-recorder), [user jobs 레코더](#user-jobs-recorder), [slow jobs 레코더](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최근 발생 내역을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치를 기준으로 그룹화됩니다. 자세한 내용은 [exceptions 레코더](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐별 처리량, 즉 대기 중, 처리 중, 처리 완료, 재시도, 실패된 작업의 개수를 보여줍니다. 자세한 내용은 [queues 레코더](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청

`<livewire:pulse.slow-requests />` 카드는 기본적으로 1,000ms를 초과한 애플리케이션의 들어오는 요청을 표시합니다. 자세한 내용은 [slow requests 레코더](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업

`<livewire:pulse.slow-jobs />` 카드는 기본적으로 1,000ms를 초과한 애플리케이션의 대기 작업(jobs)을 보여줍니다. 자세한 내용은 [slow jobs 레코더](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리

`<livewire:pulse.slow-queries />` 카드는 기본적으로 1,000ms를 초과한 애플리케이션의 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외) 및 발생 위치 기준으로 그룹화되지만, 위치 정보를 캡처하지 않고 SQL 쿼리로만 그룹화하도록 설정할 수도 있습니다.

매우 긴 SQL 쿼리에 구문 하이라이팅이 적용되어 렌더링 성능 문제가 발생하면, `without-highlighting` 속성을 추가하여 하이라이팅을 비활성화할 수 있습니다.

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [slow queries 레코더](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청

`<livewire:pulse.slow-outgoing-requests />` 카드는 라라벨 [HTTP 클라이언트](/docs/12.x/http-client)를 이용하여 보낸 외부 요청 중 기본적으로 1,000ms를 초과한 사례를 보여줍니다.

기본적으로 항목들은 전체 URL 기준으로 그룹화됩니다. 그러나 정규식을 이용해 유사한 외부 요청을 정규화하거나 그룹화할 수도 있습니다. 자세한 내용은 [slow outgoing requests 레코더](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시

`<livewire:pulse.cache />` 카드는 애플리케이션의 전역 및 개별 키별 캐시 적중(hit)·실패(miss) 통계를 보여줍니다.

기본적으로 항목은 키별로 그룹화됩니다. 하지만 정규식을 사용해 유사한 키를 그룹화하거나 정규화할 수도 있습니다. 자세한 내용은 [cache interactions 레코더](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 항목 캡처

대부분의 Pulse 레코더는 라라벨에서 발생하는 프레임워크 이벤트를 기반으로 항목을 자동으로 캡처합니다. 하지만 [servers 레코더](#servers-recorder) 및 일부 서드파티 카드는 정보를 주기적으로 폴링해야 합니다. 이러한 카드를 사용하려면 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다.

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor 같은 프로세스 모니터를 사용하여 명령어가 중단되지 않도록 관리하는 것이 좋습니다.

`pulse:check` 명령어는 장시간 실행되는 프로세스이기 때문에 코드가 변경되어도 자동으로 반영되지 않습니다. 배포 시점에는 `pulse:restart` 명령어를 호출하여 해당 프로세스를 정상적으로 다시 시작해야 합니다.

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 사용하여 재시작 신호를 저장하므로, 해당 기능을 이용하기 전에 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더

레코더는 애플리케이션에서 발생한 항목을 캡처하여 Pulse 데이터베이스에 기록하는 역할을 합니다. 레코더는 [Pulse 구성 파일](#configuration)의 `recorders` 섹션에서 등록 및 설정할 수 있습니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [캐시](/docs/12.x/cache) hit(적중) 및 miss(실패) 정보를 캡처하여 [캐시 카드](#cache-card)에 표시합니다.

[샘플링 비율](#sampling)과 무시할 키 패턴을 옵션으로 조정할 수 있습니다.

비슷한 키를 하나의 항목으로 그룹화할 수도 있습니다. 예를 들어 동일한 유형의 정보를 캐싱하면서 각 키에 고유 ID가 포함되어 있다면, 이 고유 ID를 제거해서 그룹화할 수 있습니다. 그룹화는 정규식을 이용한 "찾아 바꾸기" 방식으로 구성 파일에서 설정하며 예시가 포함되어 있습니다.

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

일치하는 첫 번째 패턴이 사용됩니다. 일치하는 패턴이 없다면 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외

`Exceptions` 레코더는 애플리케이션에서 보고 가능한 예외 정보를 캡처하여 [Exceptions 카드](#exceptions-card)에 표시합니다.

[샘플링 비율](#sampling)과 무시할 예외 패턴을 조정할 수 있으며, 예외 발생 위치를 캡처할지 여부도 설정할 수 있습니다. 위치 정보를 캡처하면 Pulse 대시보드에서 예외 원인을 추적하는 데 도움이 되지만, 동일한 예외가 여러 위치에서 발생하면 각 위치별로 중복해서 표시됩니다.

<a name="queues-recorder"></a>
#### 큐

`Queues` 레코더는 애플리케이션의 큐 정보(대기, 처리 중, 완료, 재시도, 실패 등)를 캡처하여 [Queues 카드](#queues-card)에 표시합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴을 설정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업

`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업 정보를 캡처하여 [Slow Jobs 카드](#slow-jobs-recorder)에 표시합니다.

느린 작업 임계값, [샘플링 비율](#sampling), 무시할 작업 패턴을 옵션으로 설정할 수 있습니다.

오래 걸려도 괜찮은 특정 작업이 있다면, 작업별 임계값을 개별적으로 설정할 수 있습니다.

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

작업 클래스명이 어떤 정규식과도 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청

`SlowOutgoingRequests` 레코더는 라라벨의 [HTTP 클라이언트](/docs/12.x/http-client)로 전송된 외부 요청 중, 임계치를 초과한 사례를 캡처하여 [Slow Outgoing Requests 카드](#slow-outgoing-requests-card)에 표시합니다.

느린 외부 요청 임계값, [샘플링 비율](#sampling), 무시할 URL 패턴을 옵션으로 설정할 수 있습니다.

길어도 괜찮은 외부 요청이 있다면, 요청별 임계값을 설정할 수 있습니다.

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

URL이 어떤 정규식과도 일치하지 않으면 `'default'` 값이 사용됩니다.

비슷한 URL을 단일 항목으로 그룹화해서 볼 수도 있습니다. 예를 들어 URL 경로나 도메인별로 묶고 싶다면 정규식을 활용해 그룹을 지정할 수 있습니다. 아래는 구성 파일에 포함된 예시입니다.

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

일치하는 첫 번째 패턴이 사용됩니다. 일치하는 패턴이 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 레코더는 애플리케이션에서 임계값을 초과하는 데이터베이스 쿼리를 캡처하여 [Slow Queries 카드](#slow-queries-card)에 표시합니다.

느린 쿼리 임계값, [샘플링 비율](#sampling), 무시할 쿼리 패턴을 옵션으로 설정할 수 있습니다. 쿼리의 발생 위치를 캡처할지 여부도 선택할 수 있습니다. 발생 위치는 Pulse 대시보드에서 쿼리 원인 추적에 도움이 되지만, 동일한 쿼리가 여러 위치에서 실행되면 각 위치마다 개별 표시됩니다.

일부 쿼리는 오래 걸려도 괜찮을 때, 쿼리별 임계값을 설정할 수 있습니다.

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

SQL이 어떤 정규식과도 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 레코더는 애플리케이션에 대한 요청 정보를 캡처하여 [Slow Requests 카드](#slow-requests-card), [애플리케이션 사용 카드](#application-usage-card)에 표시합니다.

느린 라우트 임계값, [샘플링 비율](#sampling), 무시할 경로 패턴을 설정할 수 있습니다.

특정 요청이 오래 걸려도 괜찮을 경우, 요청별 임계값을 설정할 수 있습니다.

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL이 어떤 정규식과도 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 스토리지 사용량을 캡처하여 [서버 카드](#servers-card)에 표시합니다. 이 레코더는 [pulse:check 명령어](#capturing-entries)가 각 서버에서 실행 중이어야 동작합니다.

각 서버는 고유한 이름을 가져야 하며, 기본적으로 Pulse는 PHP의 `gethostname` 함수의 반환 값을 사용합니다. 이를 커스터마이즈하려면 `PULSE_SERVER_NAME` 환경 변수로 설정할 수 있습니다.

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 구성 파일을 통해 모니터링할 디렉터리도 커스터마이즈할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### User Jobs

`UserJobs` 레코더는 애플리케이션에서 각 사용자가 디스패치한 작업 정보를 캡처하여 [애플리케이션 사용 카드](#application-usage-card)에 표시합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴을 설정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### User Requests

`UserRequests` 레코더는 애플리케이션에서 각 사용자가 보낸 요청 정보를 캡처하여 [애플리케이션 사용 카드](#application-usage-card)에 표시합니다.

[샘플링 비율](#sampling)과 무시할 URL 패턴을 설정할 수 있습니다.

<a name="filtering"></a>
### 필터링

앞서 살펴본 것처럼, 많은 [레코더](#recorders)에서 구성 설정을 통해, 예를 들어 특정 요청 URL 값에 따라 항목을 "무시"할 수 있습니다. 그러나 때로는 현재 인증된 사용자 등 다른 조건에 따라 항목을 필터링할 필요가 있습니다. 이러한 경우 Pulse의 `filter` 메서드에 클로저를 전달하여 기록을 필터링할 수 있습니다. 보통 `filter` 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```

<a name="performance"></a>
## 성능

Pulse는 별도의 인프라 없이 기존 애플리케이션에 손쉽게 적용될 수 있도록 설계되었습니다. 하지만 트래픽이 많은 환경에서는 Pulse가 애플리케이션 성능에 미치는 영향 없이 사용할 수 있는 여러 방법이 있습니다.

<a name="using-a-different-database"></a>
### 별도의 데이터베이스 사용

트래픽이 많은 환경에서는 Pulse 데이터가 애플리케이션 DB에 영향을 주지 않도록 별도의 데이터베이스 연결을 사용하는 것이 좋습니다.

Pulse가 사용할 [데이터베이스 연결](/docs/12.x/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수로 간단히 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis Ingest

> [!WARNING]
> Redis Ingest를 사용하려면 Redis 6.2 이상 및 `phpredis` 또는 `predis`가 애플리케이션의 Redis 클라이언트 드라이버로 설정되어 있어야 합니다.

기본적으로 Pulse는 [설정된 데이터베이스 연결](#using-a-different-database)에 직접 항목을 저장합니다(HTTP 응답 전송 후, 또는 작업 처리 후). 하지만 Pulse의 Redis ingest 드라이버를 사용하면 항목을 데이터베이스 대신 Redis 스트림으로 전송할 수 있습니다. 이를 활성화하려면 `PULSE_INGEST_DRIVER` 환경 변수를 설정하면 됩니다.

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 [기본 Redis 연결](/docs/12.x/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 별도의 연결을 지정할 수도 있습니다.

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis ingest 드라이버를 사용할 때는, 가능한 한 Pulse 인스턴스와 Redis 기반 큐가 서로 다른 Redis 연결을 사용해야 합니다.

Redis ingest를 사용할 때는 `pulse:work` 명령어를 실행해 스트림을 모니터링하고, Redis에 저장된 항목을 Pulse 데이터베이스 테이블로 이동시켜야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 지속적으로 실행하려면 Supervisor 같은 프로세스 관리 도구를 사용해 Pulse worker가 중단되지 않도록 해야 합니다.

`pulse:work` 명령어 역시 장시간 실행되는 프로세스이므로, 코드가 변경되어도 자동으로 반영되지 않습니다. 애플리케이션 배포 과정에서 `pulse:restart` 명령어를 호출해 프로세스를 정상적으로 재시작하세요.

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 사용하여 재시작 신호를 저장하므로, 해당 기능을 사용하기 전에 애플리케이션에 올바른 캐시 드라이버가 설정되어 있는지 반드시 확인하세요.

<a name="sampling"></a>
### 샘플링

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 빠짐없이 기록합니다. 트래픽이 많은 환경에서는 이로 인해 수백만 개의 데이터베이스 행이 대시보드에 집계될 수 있으며, 특히 기간이 길수록 더욱 심해집니다.

이럴 땐 특정 Pulse 데이터 레코더에 "샘플링"을 적용할 수 있습니다. 예를 들어, [User Requests](#user-requests-recorder) 레코더의 샘플링 비율을 `0.1`로 설정하면 모든 요청 중 약 10%만 기록되고, 대시보드에 표시될 때는 값 앞에 `~`가 붙어 근사치임을 표현합니다.

일반적으로, 특정 지표에 대해 충분한 항목이 쌓이면 샘플링 비율을 더 낮게 설정해도 정확도가 크게 떨어지지 않습니다.

<a name="trimming"></a>
### 트리밍

Pulse는 대시보드에서 벗어난 오래된 항목을 자동으로 정리합니다(트리밍). 트리밍은 데이터를 ingest하는 시점에 로터리 방식으로 이뤄지며, Pulse [구성 파일](#configuration)에서 세부 동작을 커스터마이즈할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리

Pulse 데이터 캡처 중 스토리지 데이터베이스 연결 오류 등 예외가 발생하면 애플리케이션에 영향이 없도록 Pulse가 조용히 실패(fail silently) 처리합니다.

예외 처리 방식을 직접 정의하고 싶다면, `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다.

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
## 커스텀 카드

Pulse는 애플리케이션 특성에 맞는 데이터를 표시할 수 있도록 커스텀 카드를 제작할 수 있게 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드를 처음 만들기 전 [공식 문서](https://livewire.laravel.com/docs)를 살펴보는 것을 권장합니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트

라라벨 Pulse에서 커스텀 카드를 생성하려면, 기본 제공되는 `Card` Livewire 컴포넌트를 확장하고, 이에 해당하는 뷰를 정의하는 것부터 시작합니다.

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 활용하면, `Card` 컴포넌트가 자동으로 `cols`, `rows` 속성을 반영해 플레이스홀더를 출력합니다.

Pulse 카드의 뷰를 작성할 때는 Pulse의 Blade 컴포넌트로 디자인의 일관성을 유지할 수 있습니다.

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각 Blade 컴포넌트에 전달되어야 하며, 대시보드 뷰에서 카드 레이아웃을 자유롭게 커스터마이즈할 수 있습니다. 카드가 자동으로 갱신되길 원한다면 뷰에 `wire:poll.5s=""` 속성을 추가하는 것도 좋습니다.

Livewire 컴포넌트와 템플릿을 정의한 이후, [대시보드 뷰](#dashboard-customization)에서 해당 카드를 포함할 수 있습니다.

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 카드가 별도의 패키지에 포함되어 있다면, `Livewire::component` 메서드를 사용해 컴포넌트를 Livewire에 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링

Pulse에서 제공하는 클래스와 컴포넌트 이외에 추가적인 CSS 스타일이 필요할 경우, 커스텀 카드에 사용할 CSS를 포함시키는 몇 가지 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### 라라벨 Vite 통합

커스텀 카드가 애플리케이션 코드베이스 내에 있고, 라라벨의 [Vite 통합](/docs/12.x/vite)을 사용 중이라면, `vite.config.js` 파일에 해당 카드용 CSS 엔트리포인트를 추가하세요.

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

이후 [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 지시문을 사용해 카드용 CSS를 불러올 수 있습니다.

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

Pulse 카드가 별도의 패키지에 포함되어 있는 등 기타 상황에서는, Livewire 컴포넌트에 `css` 메서드를 정의해 추가 스타일시트를 포함시키도록 할 수 있습니다. 이 메서드는 CSS 파일 경로를 반환해야 합니다.

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```

이 카드를 대시보드에 포함시키면, Pulse가 해당 CSS 파일의 내용을 `<style>` 태그로 자동 삽입해주므로, public 디렉터리로 공개(publish)할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 경우, 불필요한 CSS 로딩이나 Pulse의 Tailwind 클래스와 충돌을 방지하려면 카드별 별도의 Tailwind 설정 파일을 작성하는 것이 좋습니다.

```js
export default {
    darkMode: 'class',
    important: '#top-sellers',
    content: [
        './resources/views/livewire/pulse/top-sellers.blade.php',
    ],
    corePlugins: {
        preflight: false,
    },
};
```

CSS 엔트리포인트 파일에서 해당 설정 파일을 지정합니다.

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Tailwind의 [important selector 전략](https://tailwindcss.com/docs/configuration#selector-strategy)을 사용하려면, 카드 뷰 안에 `id` 또는 `class` 속성을 반드시 포함시켜야 합니다. 이 속성은 전략에 지정한 선택자와 일치해야 합니다.

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계

커스텀 카드는 애플리케이션 어디에서든 데이터를 수집/출력할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록·집계 시스템을 활용하는 것이 더 좋을 수 있습니다.

<a name="custom-card-data-capture"></a>
#### 항목 캡처

Pulse에서는 `Pulse::record` 메서드로 항목을 간단히 기록할 수 있습니다.

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 기록할 항목의 `type`, 두 번째 인자는 집계 시 사용하는 `key`입니다. 대부분의 집계 메서드에서는 집계할 `value`도 필요합니다. 위 예시에서 집계 값은 `$sale->amount`입니다. 이후 하나 이상의 집계 메서드(`sum` 등)를 호출해 Pulse가 "버킷" 단위로 미리 집계된 값을 효율적으로 저장·불러올 수 있도록 합니다.

지원하는 집계 메서드는 아래와 같습니다.

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 캡처하는 카드 패키지를 만들 때는, 애플리케이션에 적용된 [사용자 리졸버 커스터마이즈](#dashboard-resolving-users)를 반영할 수 있도록 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용해야 합니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회

Pulse의 `Card` Livewire 컴포넌트를 확장하는 경우, `aggregate` 메서드를 사용해 대시보드에서 보는 기간에 해당하는 집계 데이터를 조회할 수 있습니다.

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```

`aggregate` 메서드는 PHP의 `stdClass` 객체 컬렉션을 반환합니다. 각 객체에는 앞서 캡처한 `key`와 집계값(`sum`, `count` 등) 프로퍼티가 포함됩니다.

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 미리 집계된 버킷 데이터를 활용하므로, 원하는 집계 항목은 반드시 사전에 `Pulse::record` 메서드로 집계해 두어야 합니다. 가장 오래된 버킷은 기간을 일부 벗어날 수 있으나, Pulse가 해당 부분에 맞춰 집계를 보정하여 효율적으로 전체 값을 제공합니다.

특정 타입에 대한 전체 합계를 조회하려면 `aggregateTotal` 메서드를 사용합니다. 예를 들어, 아래와 같이 모든 사용자 판매 합계를 구할 수 있습니다.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시

key로 사용자 ID를 기록한 집계 데이터를 활용할 때는, `Pulse::resolveUsers` 메서드를 사용해 키에서 사용자 객체를 쉽게 얻을 수 있습니다.

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```

`find` 메서드는 `name`, `extra`, `avatar` 속성을 가진 객체를 반환하므로, 이를 `<x-pulse::user-card>` Blade 컴포넌트에 바로 넘길 수 있습니다.

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더

패키지 개발자는 데이터 캡처를 구성할 수 있도록 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 구성 파일의 `recorders` 섹션에 등록됩니다.

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```

레코더는 `$listen` 속성으로 이벤트를 지정할 수 있습니다. Pulse가 리스너를 자동으로 등록하고, 해당 이벤트가 발생하면 레코더의 `record` 메서드가 호출됩니다.

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * The events to listen for.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * Record the deployment.
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```