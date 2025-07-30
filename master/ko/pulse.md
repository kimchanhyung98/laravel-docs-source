# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [권한 설정](#dashboard-authorization)
    - [커스터마이징](#dashboard-customization)
    - [사용자 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [별도의 데이터베이스 사용](#using-a-different-database)
    - [Redis 인게스트](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 볼 수 있는 인사이트를 제공합니다. Pulse를 사용하면 느린 작업이나 엔드포인트와 같은 병목 현상을 추적하고, 가장 활발한 사용자를 찾는 등 다양한 정보를 파악할 수 있습니다.

개별 이벤트를 깊이 있게 디버깅하려면 [Laravel Telescope](/docs/master/telescope)를 확인하세요.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Pulse의 기본 스토리지 구현은 현재 MySQL, MariaDB 또는 PostgreSQL 데이터베이스를 필요로 합니다. 만약 다른 데이터베이스 엔진을 사용 중이라면, Pulse 데이터를 저장하기 위해 별도의 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스가 필요합니다.

Composer 패키지 관리자를 사용해 Pulse를 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 통해 Pulse 설정 파일과 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터를 저장하기 위한 테이블 생성을 위해 `migrate` 명령어를 실행하세요:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로로 Pulse 대시보드에 접속할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않다면, [전용 데이터베이스 연결을 지정](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나 신규 레코더를 등록하거나 고급 옵션을 구성하려면 `config/pulse.php` 설정 파일을 게시하세요:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 권한 설정 (Authorization)

Pulse 대시보드에는 기본적으로 `/pulse` 경로로 접근할 수 있습니다. 기본 설정으로는 로컬 환경(`local`)에서만 접근이 가능하므로, 프로덕션 환경에서는 `'viewPulse'` 권한 게이트를 커스터마이징하여 접근 권한을 설정해야 합니다. 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 다음과 같이 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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
### 커스터마이징 (Customization)

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰를 게시하여 구성할 수 있습니다. 게시하면 `resources/views/vendor/pulse/dashboard.blade.php` 위치에 저장됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 작동하며, 자바스크립트 자산을 재빌드하지 않고도 카드와 레이아웃을 커스터마이징할 수 있습니다.

이 파일 내 `<x-pulse>` 컴포넌트가 대시보드를 렌더링하며 카드 그리드 레이아웃을 제공합니다. 화면 전체 폭을 활용하고 싶다면 `full-width` 프로퍼티를 컴포넌트에 전달할 수 있습니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12열 그리드를 생성하지만, `cols` 프로퍼티로 커스터마이징 가능합니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드에는 공간과 위치를 제어하는 `cols`와 `rows` 프로퍼티가 있습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분 카드에는 전체 카드를 스크롤 없이 표시하는 `expand` 프로퍼티도 지원됩니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 해석 (Resolving Users)

사용자 정보를 표시하는 카드(예: Application Usage 카드)는 Pulse가 사용자 ID만 기록합니다. 대시보드 렌더링 시 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 해석하고, Gravatar 웹 서비스를 통해 아바타를 표시합니다.

사용자 필드와 아바타를 커스터마이징하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내에서 `Pulse::user` 메서드를 호출하세요.

`user` 메서드는 표시할 `Authenticatable` 모델을 받는 클로저를 인수로 받으며, 배열로 사용자 `name`, `extra`, `avatar` 정보를 반환해야 합니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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
> 인증된 사용자를 완전히 커스터마이징하여 캡처하고 조회하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel의 [서비스 컨테이너](/docs/master/container#binding-a-singleton)에 바인딩하세요.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### 서버 (Servers)

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행하는 모든 서버의 시스템 리소스 사용 정보를 표시합니다. 시스템 리소스 보고에 관한 자세한 내용은 [서버 레코더](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체한 후, 비활성 서버를 일정 기간이 지난 후 Pulse 대시보드에서 제외하고 싶을 수 있습니다. 이 경우 `ignore-after` 프로퍼티에 비활성 서버를 대시보드에서 제거할 초 단위 시간을 지정하거나, `1 hour` 또는 `3 days and 1 hour` 같은 상대 시간 문자열을 사용할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량 (Application Usage)

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나 작업을 디스패치하며 느린 요청이 발생한 상위 10명의 사용자를 표시합니다.

모든 사용량 지표를 동시에 보고 싶다면 카드를 여러 번 포함하고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse의 사용자 정보 조회 및 표시 방식을 커스터마이징하려면 [사용자 해석](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션에 요청이 많거나 작업이 많이 디스패치되는 경우 [샘플링](#sampling)을 활성화하는 것이 좋습니다. 자세한 내용은 [사용자 요청 레코더](#user-requests-recorder), [사용자 작업 레코더](#user-jobs-recorder), [느린 작업 레코더](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외 (Exceptions)

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생하는 예외의 빈도와 최근성을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치에 따라 그룹화됩니다. 자세한 내용은 [예외 레코더](#exceptions-recorder)를 참조하세요.

<a name="queues-card"></a>
#### 큐 (Queues)

`<livewire:pulse.queues />` 카드는 애플리케이션 큐의 처리량을 표시하며, 큐에 들어간 작업 수, 처리 중, 처리 완료, 해제, 실패한 작업 수를 보여줍니다. 자세한 내용은 [큐 레코더](#queues-recorder)를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청 (Slow Requests)

`<livewire:pulse.slow-requests />` 카드는 설정된 임계값(기본 1,000ms)을 넘는 애플리케이션으로 들어오는 요청을 보여줍니다. 자세한 내용은 [느린 요청 레코더](#slow-requests-recorder)를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업 (Slow Jobs)

`<livewire:pulse.slow-jobs />` 카드는 설정된 임계값(기본 1,000ms)을 넘는 대기 중인 작업을 보여줍니다. 자세한 내용은 [느린 작업 레코더](#slow-jobs-recorder)를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리 (Slow Queries)

`<livewire:pulse.slow-queries />` 카드는 설정된 임계값(기본 1,000ms)을 넘는 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외)와 발생 위치별로 그룹화되지만, 위치 캡처를 비활성화하여 쿼리만으로 그룹화할 수도 있습니다.

매우 큰 SQL 쿼리에 구문 강조 표시를 하여 렌더링 성능 이슈가 발생하는 경우, `without-highlighting` 프로퍼티를 추가해 강조를 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [느린 쿼리 레코더](#slow-queries-recorder)를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/master/http-client)를 사용해 발생한 외부 요청 중 설정된 임계값(기본 1,000ms)을 초과하는 요청을 표시합니다.

기본적으로 항목은 전체 URL별로 그룹화하지만, 정규식으로 유사한 요청을 정규화하거나 그룹화할 수도 있습니다. 자세한 내용은 [느린 외부 요청 레코더](#slow-outgoing-requests-recorder)를 참고하세요.

<a name="cache-card"></a>
#### 캐시 (Cache)

`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 적중 및 실패 현황을 전역과 개별 키별로 보여줍니다.

기본적으로 항목은 키별로 그룹화되지만, 정규식을 사용해 비슷한 키를 그룹화하거나 정규화할 수 있습니다. 자세한 내용은 [캐시 상호 작용 레코더](#cache-interactions-recorder)를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel에서 발생하는 프레임워크 이벤트를 기반으로 자동으로 엔트리를 캡처합니다. 그러나 [서버 레코더](#servers-recorder)와 일부 서드파티 카드는 정기적으로 정보를 폴링해야 하므로, 애플리케이션의 각 서버에서 다음 명령어를 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 항상 실행하려면 Supervisor 같은 프로세스 모니터를 사용해 명령어가 중단되지 않도록 관리해야 합니다.

`pulse:check` 명령어는 장기 실행 프로세스이므로 코드 변경 사항을 반영하려면 재시작이 필요합니다. 배포 과정에서 `pulse:restart` 명령어를 호출해 우아하게 재시작하세요:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 재시작 시그널을 저장하기 위해 [캐시](/docs/master/cache)를 사용하므로, 이 기능을 사용하기 전에 캐시 드라이버가 애플리케이션에 적절히 설정되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 캡처된 엔트리를 Pulse 데이터베이스에 기록하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration)의 `recorders` 섹션에서 등록 및 구성합니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용 (Cache Interactions)

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [캐시](/docs/master/cache)의 적중과 실패 정보를 캡처하여 [캐시](#cache-card) 카드에 표시합니다.

선택적으로 [샘플 비율](#sampling)과 무시할 키 패턴을 조정할 수 있습니다.

또한 비슷한 키들을 하나의 항목으로 그룹화하도록 정규식 기반의 키 그룹화도 구성할 수 있습니다. 예를 들어, 동일한 유형의 정보를 캐싱하는 키에서 고유 ID를 제거하고 싶을 때 사용합니다. 설정 파일에 예시가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

첫 번째 매칭되는 패턴이 사용되며, 매칭되는 패턴이 없으면 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외 (Exceptions)

`Exceptions` 레코더는 애플리케이션 내에 발생하는 보고 가능한 예외 정보를 캡처하여 [예외](#exceptions-card) 카드에 표시합니다.

선택적으로 [샘플 비율](#sampling)과 무시할 예외 패턴을 조정할 수 있습니다. 예외 발생 위치를 캡처할지도 선택할 수 있는데, 캡처한 위치는 Pulse 대시보드에 표시되어 예외의 출처 추적에 도움이 됩니다. 하지만 동일한 예외가 여러 위치에서 발생하면 각 위치별로 별도의 항목으로 나타납니다.

<a name="queues-recorder"></a>
#### 큐 (Queues)

`Queues` 레코더는 애플리케이션 큐 정보를 캡처하여 [큐](#queues-card) 카드에 표시합니다.

선택적으로 [샘플 비율](#sampling)과 무시할 작업 패턴을 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업 (Slow Jobs)

`SlowJobs` 레코더는 애플리케이션에서 발생하는 느린 작업 정보를 캡처하여 [느린 작업](#slow-jobs-card) 카드에 표시합니다.

선택적으로 느린 작업 임계값, [샘플 비율](#sampling), 무시할 작업 패턴을 조정할 수 있습니다.

일부 작업은 오래 걸릴 것으로 예상될 수 있으므로, 작업별 임계값을 설정할 수도 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

작업 클래스명에 매칭되는 정규식 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`SlowOutgoingRequests` 레코더는 Laravel [HTTP 클라이언트](/docs/master/http-client)를 통해 발생하는 느린 외부 HTTP 요청 정보를 캡처하여 [느린 외부 요청](#slow-outgoing-requests-card) 카드에 표시합니다.

선택적으로 느린 외부 요청 임계값, [샘플 비율](#sampling), 무시할 URL 패턴을 조정할 수 있습니다.

특정 요청이 오래 걸릴 것으로 예상될 수 있으므로, 요청별 임계값도 구성할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL에 매칭되는 정규식 패턴이 없으면 `'default'` 값이 사용됩니다.

또한 URL 경로에서 고유 ID 제거 또는 도메인별 그룹화 등 유사 URL을 하나로 그룹화하기 위한 URL 그룹화 설정도 가능합니다. 설정 파일에 몇 가지 예시가 포함되어 있습니다:

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

첫 번째 매칭되는 패턴이 사용되며, 매칭 패턴이 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리 (Slow Queries)

`SlowQueries` 레코더는 설정된 임계값을 넘는 데이터베이스 쿼리를 캡처하여 [느린 쿼리](#slow-queries-card) 카드에 표시합니다.

선택적으로 느린 쿼리 임계값, [샘플 비율](#sampling), 무시할 쿼리 패턴, 쿼리 발생 위치 캡처 여부를 조정할 수 있습니다. 위치 정보는 대시보드에서 쿼리 출처 추적에 유용하지만 여러 위치에서 동일 쿼리가 발생하면 각 위치별로 별도의 항목이 생성됩니다.

쿼리별 임계값도 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

SQL 쿼리와 매칭되는 정규식 패턴이 없으면 `'default'` 값이 적용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청 (Slow Requests)

`Requests` 레코더는 애플리케이션에 들어오는 요청 정보를 캡처하여 [느린 요청](#slow-requests-card) 및 [애플리케이션 사용량](#application-usage-card) 카드에 표시합니다.

선택적으로 느린 경로 임계값, [샘플 비율](#sampling), 무시할 경로 패턴을 조정할 수 있습니다.

경로별 임계값도 설정 가능합니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL에 매칭되는 정규식 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버 (Servers)

`Servers` 레코더는 애플리케이션에 필요한 서버들의 CPU, 메모리, 저장소 사용량을 캡처하여 [서버](#servers-card) 카드에 표시합니다. 해당 레코더를 사용하려면 [ `pulse:check` 명령어](#capturing-entries)가 각 서버에서 실행되고 있어야 합니다.

각 서버가 고유한 이름을 가져야 하며, 기본적으로 PHP의 `gethostname` 함수 반환값을 사용합니다. 커스터마이즈하려면 `PULSE_SERVER_NAME` 환경 변수를 설정하세요:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링할 디렉터리도 설정할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업 (User Jobs)

`UserJobs` 레코더는 애플리케이션에서 작업을 디스패치하는 사용자 정보를 캡처하여 [애플리케이션 사용량](#application-usage-card) 카드에 표시합니다.

선택적으로 [샘플 비율](#sampling) 및 무시할 작업 패턴을 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청 (User Requests)

`UserRequests` 레코더는 애플리케이션에 요청을 보내는 사용자 정보를 캡처하여 [애플리케이션 사용량](#application-usage-card) 카드에 표시합니다.

선택적으로 [샘플 비율](#sampling) 및 무시할 URL 패턴을 조정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

앞서 살펴본 많은 [레코더](#recorders)는 설정을 통해 특정 값(예: 요청 URL)에 따라 "무시"할 수 있습니다. 그러나 때로는 현재 인증된 사용자와 같은 다른 조건에 따라 기록을 필터링하고 싶을 수 있습니다. 이 경우 Pulse의 `filter` 메서드에 클로저를 전달할 수 있습니다. 보통 `filter` 메서드는 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

Pulse는 추가 인프라 없이 기존 애플리케이션에 간편히 도입되도록 설계되었습니다. 하지만 트래픽이 많은 애플리케이션의 경우 Pulse가 애플리케이션 성능에 미치는 영향을 줄일 여러 방법이 있습니다.

<a name="using-a-different-database"></a>
### 별도의 데이터베이스 사용 (Using a Different Database)

트래픽이 높은 애플리케이션은 Pulse가 애플리케이션 데이터베이스에 영향을 주지 않도록 전용 데이터베이스 연결을 사용하는 것이 좋습니다.

환경 변수 `PULSE_DB_CONNECTION`을 설정하여 Pulse가 사용할 [데이터베이스 연결](/docs/master/database#configuration)을 커스터마이징할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인게스트 (Redis Ingest)

> [!WARNING]
> Redis 인게스트를 사용하려면 Redis 6.2 이상과 `phpredis` 또는 `predis` Redis 클라이언트가 필요합니다.

기본적으로 Pulse는 HTTP 응답 전송 후나 작업 처리 직후에 [설정된 데이터베이스 연결](#using-a-different-database)에 항목을 직접 저장합니다. 그러나 Pulse의 Redis 인게스트 드라이버를 사용해 Redis 스트림으로 항목을 전송할 수도 있습니다. 이 경우 `PULSE_INGEST_DRIVER` 환경 변수로 활성화하세요:

```ini
PULSE_INGEST_DRIVER=redis
```

기본 Redis 연결은 애플리케이션의 기본 [Redis 설정](/docs/master/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 커스터마이징할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

Redis 인게스트를 사용할 경우 `pulse:work` 명령어를 실행하여 Redis 스트림을 모니터링하고 항목을 Pulse 데이터베이스로 이동해야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 항상 실행하려면 Supervisor 같은 프로세스 모니터를 사용해 워커가 중단되지 않도록 관리하세요.

`pulse:work` 명령어도 장기 실행 프로세스이므로 코드 변경 사항을 반영하려면 재시작이 필요합니다. 배포 과정에서 `pulse:restart` 명령어로 우아하게 재시작하세요:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 재시작 시그널을 위해 [캐시](/docs/master/cache)를 사용하므로, 캐시 드라이버가 적절히 설정되었는지 확인해야 합니다.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 애플리케이션 내 모든 관련 이벤트를 캡처합니다. 트래픽이 많을 경우, 특히 장기 기간동안 대시보드에 백만 건 이상의 데이터베이스 행을 집계해야 하는 상황이 발생할 수 있습니다.

이 경우 특정 Pulse 데이터 레코더에 "샘플링"을 활성화할 수 있습니다. 예를 들어 [`User Requests`](#user-requests-recorder) 레코더에 샘플 비율을 `0.1`로 설정하면, 약 10%의 요청만 기록되고 대시보드에서는 값이 `~` 표기가 붙어 근사치임을 나타냅니다.

일반적으로 특정 메트릭에 대해 샘플 항목이 많을수록 정확도를 크게 떨어뜨리지 않고 샘플 비율을 더 낮게 설정할 수 있습니다.

<a name="trimming"></a>
### 트리밍 (Trimming)

Pulse는 대시보드 기간을 벗어난 저장된 엔트리를 자동으로 트리밍합니다. 트리밍은 인게스트 중 복권 방식으로 발생하며, Pulse [설정 파일](#configuration)에서 커스터마이징할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 캡처 중 예외가 발생하면(예: 스토리지 데이터베이스 연결 불가) 애플리케이션에 영향을 주지 않도록 조용히 실패합니다.

이 예외 처리 방식을 커스터마이징하려면 `handleExceptionsUsing` 메서드에 클로저를 전달하세요:

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
## 커스텀 카드 (Custom Cards)

Pulse는 애플리케이션 요구에 맞춰 데이터를 표시하는 커스텀 카드를 만들 수 있게 해줍니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하는 만큼, 첫 커스텀 카드를 만들기 전에 [Livewire 문서](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트 (Card Components)

Laravel Pulse에서 커스텀 카드를 만드는 첫 단계는 기본 `Card` Livewire 컴포넌트를 확장하고 그에 대응하는 뷰를 정의하는 것입니다:

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

Livewire의 [지연 로딩](https://livewire.laravel.com/docs/lazy) 기능을 사용하면, `Card` 컴포넌트가 자동으로 `cols` 및 `rows` 속성을 반영하는 플레이스홀더를 제공합니다.

Pulse 카드에 대응하는 뷰를 작성할 때는 Pulse의 Blade 컴포넌트를 활용하여 일관된 UI를 유지할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각의 Blade 컴포넌트에 전달되어 카드 레이아웃을 대시보드 뷰에서 제어할 수 있도록 합니다. 또한 카드가 자동으로 갱신되도록 `wire:poll.5s=""` 속성을 뷰에 포함하는 것을 추천합니다.

Livewire 컴포넌트와 템플릿을 정의한 후에는 [대시보드 뷰](#dashboard-customization)에서 다음과 같이 카드를 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 카드를 패키지 내에 포함할 경우 `Livewire::component` 메서드로 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

카드에 기본 Pulse 클래스와 컴포넌트 이상의 추가 스타일링이 필요한 경우, 커스텀 CSS를 포함할 여러 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

커스텀 카드가 애플리케이션 코드베이스 내에 있고 Laravel의 [Vite 통합](/docs/master/vite)을 사용하는 경우, `vite.config.js`에 카드 전용 CSS 엔트리 포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

이후 [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 디렉티브로 CSS 엔트리포인트를 지정해 포함하세요:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

패키지 내 Pulse 카드처럼 다른 사용 사례는 Livewire 컴포넌트에 `css` 메서드를 정의해 CSS 파일 경로를 반환하게 할 수 있습니다:

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

이 카드가 대시보드에 포함되면 Pulse는 해당 CSS 파일 내용을 `<style>` 태그로 자동 포함하여 `public` 디렉터리로 게시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용하는 경우, 불필요한 CSS 로딩과 Pulse Tailwind 클래스 충돌을 방지하려면 별도의 Tailwind 설정 파일을 만들어야 합니다:

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

그 후 CSS 엔트리포인트에서 해당 설정 파일을 지정합니다:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

카드 뷰의 루트 요소에 Tailwind [`important` selector 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에서 지정한 셀렉터(`id` 또는 `class`)를 포함해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계 (Data Capture and Aggregation)

커스텀 카드는 어디서든 데이터를 가져와 표시할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처 (Capturing Entries)

Pulse는 `Pulse::record` 메서드를 사용해 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 기록할 엔트리의 `type`이며, 두 번째 인자는 집계 데이터 그룹화 키를 결정하는 `key`입니다. 대부분의 집계 메서드에서는 집계할 `value`도 지정해야 합니다. 위 예시에서는 `$sale->amount`가 집계 값입니다. 이어서 `sum` 같은 집계 메서드를 하나 이상 호출해 Pulse가 미리 집계된 값을 "버킷" 단위로 효율적으로 기록하고 조회할 수 있도록 합니다.

사용 가능한 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 캡처할 때는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하세요. 이 메서드는 애플리케이션의 [사용자 해석 커스터마이징](#dashboard-resolving-users)을 존중합니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회 (Retrieving Aggregate Data)

Pulse의 `Card` Livewire 컴포넌트를 확장할 때, `aggregate` 메서드로 대시보드에서 현재 보고 있는 기간에 해당하는 집계 데이터를 조회할 수 있습니다:

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

`aggregate` 메서드는 PHP `stdClass` 객체 컬렉션을 반환하며, 각 객체는 앞서 캡처된 `key` 속성과 요청한 모든 집계 키를 포함합니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 사전 집계된 버킷에서 주로 데이터를 조회하므로, 지정된 집계 메서드는 반드시 `Pulse::record` 호출 시 캡처되어야 합니다. 가장 오래된 버킷은 기간 일부만 포함할 수 있어 Pulse가 최후 집계가 필요한 구간을 보정하지만, 전체 기간을 매번 재집계하지 않아도 정확한 값 제공이 가능합니다.

특정 타입에 대한 총합을 단독으로 조회하려면 `aggregateTotal` 메서드를 사용할 수 있습니다. 예를 들어 모든 사용자 판매 총합을 조회하려면 다음과 같이 합니다:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시 (Displaying Users)

사용자 ID를 키로 하는 집계에서 키 값을 사용자 정보로 해석하려면 `Pulse::resolveUsers` 메서드를 사용하세요:

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

`find` 메서드는 `name`, `extra`, `avatar` 키를 포함하는 객체를 반환하며, 이 정보는 옵션으로 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더 (Custom Recorders)

패키지 작성자는 사용자가 데이터를 캡처 구성할 수 있도록 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 설정 파일 내 `recorders` 섹션에 등록됩니다:

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

레코더는 감지할 이벤트를 `$listen` 속성에 명시할 수 있으며, Pulse가 자동으로 리스너를 등록하고 레코더의 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 감지할 이벤트 목록
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포를 기록합니다.
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