# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [사용자 정의](#dashboard-customization)
    - [사용자 정보 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [별도의 데이터베이스 사용](#using-a-different-database)
    - [Redis 인제스트](#ingest)
    - [샘플링](#sampling)
    - [데이터 정리](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [사용자 정의 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있도록 도와줍니다. Pulse를 사용하면 느린 작업(job)이나 엔드포인트 같은 병목 현상을 추적하고, 가장 활발히 활동하는 사용자를 찾아낼 수 있습니다.

개별 이벤트의 상세 디버깅이 필요할 경우, [Laravel Telescope](/docs/12.x/telescope)를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Pulse의 기본 저장소 구현은 현재 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스가 필요합니다. 다른 데이터베이스 엔진을 사용 중이면 Pulse 데이터를 위한 별도의 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스가 필요합니다.

Composer 패키지 관리자를 사용해 Pulse를 설치할 수 있습니다.

```shell
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 Pulse 구성 및 마이그레이션 파일을 공개하세요:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터 저장에 필요한 테이블을 생성하기 위해 `migrate` 명령어를 실행하세요:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로에서 Pulse 대시보드에 접속할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스가 아닌 별도의 데이터베이스에 저장하려면 [전용 데이터베이스 연결을 지정](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새 레코더를 등록하거나 고급 설정을 구성하려면 `config/pulse.php` 설정 파일을 공개하세요:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 인가 (Authorization)

Pulse 대시보드에 접근하려면 기본적으로 `local` 환경에서만 가능합니다. 프로덕션 환경에서 접근하려면 `'viewPulse'` 인가 게이트를 커스터마이즈 해야 합니다. 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에 다음과 같이 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 애플리케이션 서비스 부트스트랩
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
### 사용자 정의 (Customization)

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰를 공개하여 구성할 수 있습니다. 공개된 대시보드 뷰는 `resources/views/vendor/pulse/dashboard.blade.php`에 위치합니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 동작하며, JavaScript 자산을 다시 빌드할 필요 없이 카드와 레이아웃을 자유롭게 사용자 정의할 수 있습니다.

이 파일 내 `<x-pulse>` 컴포넌트가 대시보드를 렌더링하며 카드의 그리드 레이아웃을 제공합니다. 화면 가로 전체 폭을 사용하려면 `full-width` 프롭을 추가할 수 있습니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12칸 그리드를 생성하지만, `cols` 프롭으로 조정할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 `cols`, `rows` 프롭을 받아 공간과 위치를 조절합니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분 카드에는 스크롤 없이 전체 카드를 표시하는 `expand` 프롭도 지원합니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 정보 해석 (Resolving Users)

사용자에 관한 정보를 표시하는 카드(예: Application Usage 카드)의 경우, Pulse는 사용자 ID만 기록합니다. 대시보드 렌더링 시 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 해석하며, Gravatar 웹 서비스를 통해 아바타를 표시합니다.

사용자 정보 필드와 아바타 설정을 커스터마이즈 하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내에서 `Pulse::user` 메서드를 호출하세요.

`user` 메서드는 `Authenticatable` 모델을 인자로 받는 클로저를 인수로 받아야 하며, `name`, `extra`, `avatar` 정보를 포함한 배열을 반환해야 합니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * 애플리케이션 서비스 부트스트랩
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
> 인증된 사용자의 캡처 및 조회 방식을 완전히 재정의하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel의 [서비스 컨테이너](/docs/12.x/container#binding-a-singleton)에 바인딩하세요.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### 서버 (Servers)

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 자원 사용량을 표시합니다. 시스템 자원 정보를 수집하는 [servers recorder](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체하는 경우, 비활성 서버를 일정 기간 이후 Pulse 대시보드에서 숨기려면 `ignore-after` 프롭을 사용하세요. 초(seconds)를 입력하거나 `1 hour`, `3 days and 1 hour` 같은 상대 시간 문자열도 가능합니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량 (Application Usage)

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나 작업을 디스패치하는 사용자의 상위 10명을 보여주고 느린 요청도 표시합니다.

모든 사용량 지표를 동시에 보고 싶으면 카드를 여러 번 포함하고 `type` 속성을 지정하세요:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 조회하고 표시하는 방법을 커스터마이즈하는 법은 [사용자 정보 해석](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션에 많은 요청이나 작업 디스패치가 발생하는 경우, [샘플링](#sampling)을 활성화하는 것이 좋습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외 (Exceptions)

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생하는 예외의 빈도와 최신 상태를 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치별로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐 (Queues)

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리량을 보여줍니다. 큐에 쌓인 작업 수, 처리 중, 완료, 재발행, 실패한 작업 수를 포함합니다. 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청 (Slow Requests)

`<livewire:pulse.slow-requests />` 카드는 설정된 기준 시간(기본 1,000ms)을 초과한 애플리케이션의 수신 요청을 보여줍니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업 (Slow Jobs)

`<livewire:pulse.slow-jobs />` 카드는 설정된 기준 시간(기본 1,000ms)을 초과한 애플리케이션의 큐 작업을 보여줍니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리 (Slow Queries)

`<livewire:pulse.slow-queries />` 카드는 애플리케이션에서 실행된 데이터베이스 쿼리 중 설정한 임계값(기본 1,000ms)을 초과한 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외)와 발생 위치별로 그룹화하지만, 위치 정보를 캡처하지 않고 SQL 쿼리만으로 그룹화할 수도 있습니다.

매우 긴 SQL 쿼리에 구문 강조가 성능 문제를 일으키면, `without-highlighting` 프롭을 추가해 구문 강조를 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)로 보낸 외부 요청 중 설정된 임계값(기본 1,000ms)을 초과한 요청을 보여줍니다.

기본적으로는 전체 URL별로 그룹화되지만, 정규식으로 유사한 URL 경로를 정규화하거나 그룹화할 수도 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시 (Cache)

`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 히트 및 미스 통계를 전역 및 개별 키별로 보여줍니다.

기본적으로 키별로 그룹화하지만, 정규식으로 유사한 키를 그룹화하거나 정규화할 수 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel에서 발생하는 프레임워크 이벤트를 기반으로 자동으로 엔트리를 캡처합니다. 다만, [servers recorder](#servers-recorder)와 일부 서드파티 카드는 정기적으로 폴링하여 정보를 수집해야 합니다. 이를 위해 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행하세요:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 계속 실행하려면 Supervisor 같은 프로세스 모니터를 사용해 해당 명령어가 중지되지 않도록 관리해야 합니다.

`pulse:check` 명령어는 장시간 실행되는 프로세스이므로, 코드 변경사항을 인지하려면 재시작해야 합니다. 배포 과정에서 `pulse:restart` 명령어로 안전하게 재시작하세요:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 재시작 신호 저장에 [캐시](/docs/12.x/cache)를 사용하므로, 캐시 드라이버가 올바르게 설정되었는지 확인하세요.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 엔트리를 수집하여 Pulse 데이터베이스에 기록하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration)의 `recorders` 항목에서 등록 및 구성됩니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용 (Cache Interactions)

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [캐시](/docs/12.x/cache) 히트 및 미스 정보를 캡처해 [캐시 카드](#cache-card)에 표시합니다.

샘플 비율([sample rate](#sampling))과 무시할 키 패턴을 설정할 수 있습니다.

또한 유사한 키를 하나로 묶기 위한 키 그룹화도 구성할 수 있습니다. 예를 들어, 캐시 키에 포함된 고유 ID를 공통으로 대체해 동일한 유형의 정보를 그룹화할 수 있습니다. 그룹은 정규식으로 "찾아 바꾸기" 방식으로 지정하며, 예시는 설정파일에 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

패턴은 첫 매칭된 것이 사용되며, 매칭되지 않으면 원본 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외 (Exceptions)

`Exceptions` 레코더는 애플리케이션에서 보고 가능한 예외 정보를 캡처해 [예외 카드](#exceptions-card)에 표시합니다.

샘플 비율([sample rate](#sampling))과 무시할 예외 패턴, 예외가 발생한 위치 캡처 여부를 설정할 수 있습니다. 위치 정보는 예외 발생지를 추적하는 데 유용하지만, 같은 예외가 여러 위치에서 발생하면 각 위치별로 중복 표시됩니다.

<a name="queues-recorder"></a>
#### 큐 (Queues)

`Queues` 레코더는 애플리케이션 큐 정보를 캡처해 [큐 카드](#queues-card)에 표시합니다.

샘플 비율([sample rate](#sampling))과 무시할 작업 패턴을 설정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업 (Slow Jobs)

`SlowJobs` 레코더는 애플리케이션에서 느리게 실행되는 작업 정보를 캡처해 [느린 작업 카드](#slow-jobs-recorder)에 표시합니다.

느린 작업 임계값, 샘플 비율, 무시할 작업 패턴을 설정할 수 있습니다.

작업별로 예상 실행시간이 다를 경우, 작업별 임계값을 설정할 수도 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

작업 클래스명이 어떤 정규식 패턴에도 매칭되지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)를 통해 발생한 외부 요청 중 느린 요청을 캡처해 [느린 외부 요청 카드](#slow-outgoing-requests-card)에 표시합니다.

느린 요청 임계값, 샘플 비율, 무시 URL 패턴을 설정할 수 있습니다.

특정 요청의 예상 지연 시간이 다른 경우 요청별 임계값을 구성할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL이 어떤 정규식에도 매칭되지 않으면 `'default'` 값이 사용됩니다.

또한 URL 경로 내 고유 ID를 제거하거나 도메인 단위로 그룹화하는 등 URL 그룹화도 정규식으로 구성할 수 있습니다. 설정 파일에 여러 예시가 포함되어 있습니다:

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

첫 번째 매칭 패턴이 사용되며, 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리 (Slow Queries)

`SlowQueries` 레코더는 애플리케이션 데이터베이스 쿼리 중 느린 쿼리를 캡처해 [느린 쿼리 카드](#slow-queries-card)에 표시합니다.

느린 쿼리 임계값, 샘플 비율, 무시 쿼리 패턴, 쿼리 위치 캡처 여부를 설정할 수 있습니다. 위치 정보는 쿼리 발생 위치를 추적하는 데 유용하지만, 같은 쿼리가 여러 위치에서 발생하면 각 위치별로 중복 표시됩니다.

쿼리별로 임계값을 다르게 설정할 수도 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

쿼리 SQL이 어떤 정규식에도 매칭되지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청 (Slow Requests)

`Requests` 레코더는 애플리케이션으로 들어오는 요청 중 느린 요청을 캡처해 [느린 요청 카드](#slow-requests-card)와 [애플리케이션 사용량 카드](#application-usage-card)에 표시합니다.

느린 요청 임계값, 샘플 비율, 무시 경로를 설정할 수 있습니다.

요청별 임계값 설정도 가능합니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL이 어떤 정규식에도 매칭되지 않으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버 (Servers)

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장소 사용량을 캡처해 [서버 카드](#servers-card)에 표시합니다. 이 레코더는 각 서버에서 [pulse:check 명령어](#capturing-entries)를 실행해야 합니다.

각 서버는 고유한 이름을 가져야 하며, 기본적으로 PHP `gethostname` 함수 반환 값을 사용합니다. 커스터마이징하려면 `PULSE_SERVER_NAME` 환경 변수를 설정하세요:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링할 디렉터리도 조정할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업 (User Jobs)

`UserJobs` 레코더는 애플리케이션에서 작업을 디스패치하는 사용자 정보를 캡처해 [애플리케이션 사용량 카드](#application-usage-card)에 표시합니다.

샘플 비율과 무시 작업 패턴을 설정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청 (User Requests)

`UserRequests` 레코더는 애플리케이션으로 요청을 보내는 사용자 정보를 캡처해 [애플리케이션 사용량 카드](#application-usage-card)에 표시합니다.

샘플 비율과 무시 URL 패턴을 설정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

많은 [레코더](#recorders)는 설정을 통해 요청 URL 등 값에 따라 엔트리를 "무시"할 수 있게 지원합니다. 하지만 때때로 현재 인증된 사용자 같은 다른 조건에 따라 기록을 필터링하고 싶을 수도 있습니다.

이 경우 `Pulse::filter` 메서드에 클로저를 전달할 수 있으며, 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * 애플리케이션 서비스 부트스트랩
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
## 성능 (Performance)

Pulse는 추가 인프라 없이도 기존 애플리케이션에 쉽게 통합되도록 설계되었습니다. 하지만 트래픽이 많은 고성능 애플리케이션에서는 Pulse가 애플리케이션 성능에 미치는 영향을 최소화할 방법이 여러 가지 있습니다.

<a name="using-a-different-database"></a>
### 별도의 데이터베이스 사용 (Using a Different Database)

트래픽이 많은 애플리케이션에서는 Pulse의 영향으로 기본 애플리케이션 데이터베이스 성능 저하를 피하기 위해 Pulse 전용 데이터베이스 연결을 사용할 수 있습니다.

`PULSE_DB_CONNECTION` 환경 변수를 설정하여 Pulse가 사용할 데이터베이스 연결을 변경하세요:

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트 (Redis Ingest)

> [!WARNING]
> Redis 인제스트를 사용하려면 Redis 6.2 이상과 `phpredis` 또는 `predis`가 설정된 Redis 클라이언트가 필요합니다.

기본적으로 Pulse는 HTTP 응답 전송 후나 작업 처리 완료 후에 [설정된 데이터베이스 연결](#using-a-different-database)에 직접 데이터를 저장합니다. 하지만 Redis 스트림으로 엔트리를 전송하는 Redis 인제스트 드라이버를 사용할 수 있습니다. 설정하려면 `PULSE_INGEST_DRIVER` 환경 변수를 다음과 같이 설정하세요:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본 Redis 연결을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 변경할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis 인제스트 사용 시, Redis 기반 큐를 사용하는 경우 Pulse는 반드시 큐와 다른 Redis 연결을 사용해야 합니다.

Redis 인제스트를 사용할 때는 `pulse:work` 명령어를 실행해 Redis 스트림을 모니터링하고 엔트리를 Pulse 데이터베이스로 이동해야 합니다:

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 계속 실행하려면 Supervisor 같은 프로세스 모니터를 사용하세요.

`pulse:work` 명령어도 장시간 실행 프로세스이므로, 코드 변경 사항을 반영하려면 재시작해야 합니다. 배포 과정에서 `pulse:restart` 명령어로 안전하게 재시작하세요:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 재시작 신호 저장에 [캐시](/docs/12.x/cache)를 사용하므로, 캐시 드라이버 설정을 확인하세요.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 기록합니다. 하지만 트래픽이 많은 애플리케이션에서는 특히 긴 기간 동안 수백만 건의 데이터가 집계되어 대시보드 성능에 영향을 줄 수 있습니다.

이런 경우 특정 Pulse 레코더에서 "샘플링"을 활성화할 수 있습니다. 예를 들어, [User Requests](#user-requests-recorder) 레코더의 샘플 비율을 `0.1`로 설정하면 전체 요청 중 약 10%만 기록합니다. 대시보드에서는 값이 보정되어 `~` 표시로 근사치임을 알려줍니다.

대체로 수집 데이터가 많을수록 샘플 비율을 낮춰도 정확성을 크게 해치지 않습니다.

<a name="trimming"></a>
### 데이터 정리 (Trimming)

Pulse는 대시보드 창 범위를 벗어난 오래된 엔트리를 자동으로 삭제합니다. 데이터 정리는 인제스트 시 복권(로터리) 시스템으로 수행되며, Pulse [설정 파일](#configuration)에서 구성할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 캡처 중 예외 발생(예: 저장소 데이터베이스 연결 실패)이 발생하면, 애플리케이션에 영향을 미치지 않도록 조용히 실패합니다.

이 동작을 커스터마이즈하려면 `handleExceptionsUsing` 메서드에 클로저를 제공하세요:

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('Pulse에서 예외가 발생했습니다', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
## 사용자 정의 카드 (Custom Cards)

Pulse는 애플리케이션의 특정 요구에 맞는 데이터를 표시하는 사용자 정의 카드를 만들 수 있게 합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 사용자 정의 카드 제작 전에 [Livewire 문서](https://livewire.laravel.com/docs)를 검토하는 것을 권장합니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트 (Card Components)

Laravel Pulse에서 사용자 정의 카드를 만들려면 기본 `Card` Livewire 컴포넌트를 확장하고 대응하는 뷰를 정의합니다:

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

Livewire의 [지연 로딩](https://livewire.laravel.com/docs/lazy) 기능을 사용할 경우, `Card` 컴포넌트는 전달받은 `cols`와 `rows` 속성에 맞는 자리 표시자(placeholder)를 자동으로 제공합니다.

Pulse 카드의 뷰를 작성할 때 일관된 디자인을 위해 Pulse의 Blade 컴포넌트를 활용할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 카드 레이아웃 최적화를 위해 대시보드 뷰에서 해당 Blade 컴포넌트로 전달되어야 합니다. 또한 자동 갱신을 원할 경우 `wire:poll.5s=""` 속성을 추가하는 것이 좋습니다.

Livewire 컴포넌트와 템플릿을 정의한 후 대시보드 뷰에 카드를 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 카드가 패키지에 포함된 경우에는 `Livewire::component` 메서드를 사용해 Livewire에 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

카드에 Pulse 내 기본 클래스 및 컴포넌트 이상으로 추가 스타일링이 필요할 경우, 사용자 정의 CSS를 포함하는 여러 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 연동

카드가 애플리케이션 코드 베이스 내에 있고 Laravel의 [Vite 통합](/docs/12.x/vite)을 사용 중이라면, `vite.config.js`에 카드용 별도 CSS 진입점을 추가하세요:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

대시보드 뷰에 `@vite` Blade 지시어로 CSS 진입점을 포함하세요:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

패키지 등 다른 경우에는 Livewire 컴포넌트에 `css` 메서드를 정의해 CSS 파일 경로를 반환하게 할 수 있습니다:

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

대시보드에 카드가 포함되면 Pulse가 해당 CSS 파일 내용을 `<style>` 태그로 자동 포함하므로, `public` 디렉터리에 복사할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 때는 불필요한 CSS 로드나 Pulse Tailwind 클래스와 충돌을 막기 위해 별도 Tailwind 설정 파일을 만드세요:

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

CSS 진입점에서는 다음과 같이 설정 파일을 지정하세요:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

카드 뷰에서는 Tailwind의 [important 선택자 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에 맞게 id나 class 속성을 추가해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계 (Data Capture and Aggregation)

사용자 정의 카드는 데이터를 어디서든 가져와서 표시할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처 (Capturing Entries)

Pulse는 `Pulse::record` 메서드로 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 기록하는 엔트리의 `type`이며, 두 번째 인자는 집계 데이터 그룹핑 기준인 `key`입니다. 대부분 집계 메서드는 집계할 `value`도 필요합니다. 위 예시는 판매금액 `$sale->amount`를 집계하는 모습입니다.

그 후 `sum` 등 집계 메서드를 호출하면 Pulse는 효율적 조회를 위한 "버킷" 단위로 사전 집계된 값을 저장합니다.

사용 가능한 집계 메서드는:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 캡처하는 카드 패키지를 만들 때는, 애플리케이션에서 적용한 [사용자 해석기 커스터마이즈](#dashboard-resolving-users)를 존중하는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하세요.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회 (Retrieving Aggregate Data)

Pulse의 `Card` Livewire 컴포넌트를 확장해, 대시보드에서 보고 있는 기간 단위로 집계 데이터를 `aggregate` 메서드로 조회할 수 있습니다:

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

`aggregate`는 PHP `stdClass` 객체 컬렉션을 반환하며, 각 객체는 앞서 기록한 `key` 속성과 요청한 집계 값들을 포함합니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 사전 집계된 버킷에서 데이터를 조회하므로, 조회 시점 범위에 완전히 포함되지 않는 가장 오래된 버킷은 부분 집계 해 정확성을 보장합니다. 덕분에 매번 전체 기간을 집계할 필요 없이 빠른 처리가 가능합니다.

`aggregateTotal` 메서드로 특정 타입 집계값의 합계만 조회할 수도 있습니다. 예를 들어 모든 사용자 판매금액 합계를 조회하려면:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시 (Displaying Users)

사용자 ID를 키로 가진 집계에서 ID를 사용자 레코드로 변환하려면 `Pulse::resolveUsers` 메서드를 사용하세요:

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

`find` 메서드는 `name`, `extra`, `avatar` 키를 포함하는 객체를 반환하며, 이를 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달해 활용할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 사용자 정의 레코더 (Custom Recorders)

패키지 작성자는 사용자가 데이터를 캡처하도록 도와주는 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션 `config/pulse.php` 설정 파일의 `recorders` 항목에 등록됩니다:

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

레코더는 리슨할 이벤트 배열을 `$listen` 프로퍼티로 명시할 수 있습니다. Pulse가 자동으로 이벤트를 등록하고 레코더의 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 리슨할 이벤트 목록
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 기록
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