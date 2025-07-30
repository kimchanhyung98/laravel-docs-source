# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이징](#dashboard-customization)
    - [사용자 정보 해결하기](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처하기](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용하기](#using-a-different-database)
    - [Redis 인게스트](#ingest)
    - [샘플링](#sampling)
    - [데이터 트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 보여주는 인사이트를 제공합니다. Pulse를 통해 느린 잡(Job)이나 엔드포인트 같은 병목 현상을 추적하고, 가장 활발한 사용자들을 확인할 수 있습니다.

개별 이벤트에 대한 깊이 있는 디버깅이 필요하다면 [Laravel Telescope](/docs/11.x/telescope)을 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> Pulse의 자체 저장소 구현은 현재 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스를 필요로 합니다. 다른 데이터베이스 엔진을 사용 중이라면 Pulse 데이터를 저장하기 위해 별도의 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스가 필요합니다.

Composer 패키지 관리자를 사용해 Pulse를 설치할 수 있습니다:

```sh
composer require laravel/pulse
```

다음으로 `vendor:publish` Artisan 명령어를 사용해 Pulse 설정 및 마이그레이션 파일을 게시하세요:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로 `migrate` 명령어를 실행해 Pulse 데이터 저장에 필요한 테이블을 생성해야 합니다:

```shell
php artisan migrate
```

Pulse의 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]  
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않은 경우, [전용 데이터베이스 연결 설정](#using-a-different-database)을 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 현재 사용 가능한 옵션 확인, 새로운 레코더 등록, 고급 설정을 위해 `config/pulse.php` 설정 파일을 게시할 수 있습니다:

```sh
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 인가 (Authorization)

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근할 수 있으므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이징하여 접근 권한을 설정해야 합니다. 이를 위해 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 다음과 같이 설정할 수 있습니다:

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
### 커스터마이징 (Customization)

Pulse 대시보드의 카드 및 레이아웃은 대시보드 뷰를 게시하여 구성할 수 있습니다. 게시된 뷰 파일은 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 위치합니다:

```sh
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 동작하며, 자바스크립트 자산을 다시 빌드하지 않고도 카드와 레이아웃을 자유롭게 커스터마이징할 수 있습니다.

해당 파일 안에서 `<x-pulse>` 컴포넌트가 대시보드 렌더링과 카드들의 그리드 레이아웃을 담당합니다. 대시보드를 화면 전체 너비로 넓히려면 `full-width` 프로퍼티를 컴포넌트에 제공하세요:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12컬럼 그리드를 생성하지만, `cols` 프로퍼티로 컬럼 개수를 변경할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드 컴포넌트는 위치와 공간을 제어하는 `cols` 및 `rows` 프로퍼티를 받습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분 카드들은 `expand` 프로퍼티도 받아 스크롤 없이 전체 내용을 보여줄 수 있습니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 정보 해결하기 (Resolving Users)

사용자 정보를 표시하는 카드(예: Application Usage 카드)의 경우, Pulse는 사용자 ID만 기록합니다. 대시보드를 렌더링할 때 기본 `Authenticatable` 모델에서 `name`과 `email`을 가져오고 Gravatar 웹 서비스를 활용해 아바타를 보여줍니다.

사용자 필드와 아바타를 변경하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 호출해 커스터마이징할 수 있습니다.

`user` 메서드는 표시할 `Authenticatable` 모델을 받아 사용자에 대한 `name`, `extra`, `avatar` 정보를 포함하는 배열을 반환하는 클로저를 인수로 받습니다:

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
> 인증된 사용자를 캡처하고 조회하는 방식을 완전히 커스터마이징하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel의 [서비스 컨테이너](/docs/11.x/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### Servers

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 자원 사용량을 보여줍니다. 시스템 자원 보고에 대한 자세한 내용은 [servers recorder](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체한 경우, 비활성 서버를 일정 기간 후에 Pulse 대시보드에서 제거하고 싶다면 `ignore-after` 프로퍼티를 이용할 수 있습니다. 이 프로퍼티는 비활성 서버를 대시보드에 표시하지 않을 기간(초 단위)이나, `1 hour`, `3 days and 1 hour` 같은 상대 시간 형식 문자열을 받습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### Application Usage

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나 잡을 디스패치하고, 느린 요청을 경험하는 상위 10명의 사용자를 표시합니다.

모든 사용량 메트릭을 동시에 보고 싶다면 카드를 여러 번 포함시키고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 조회하고 표시하는 방법 커스터마이징은 [사용자 정보 해결하기](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]  
> 애플리케이션이 많은 요청을 받거나 잡을 다수 디스패치하면 [샘플링](#sampling)을 활성화하는 것이 좋습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder)를 참고하세요.

<a name="exceptions-card"></a>
#### Exceptions

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생하는 예외의 빈도와 최근 발생 시점을 보여줍니다. 기본적으로 예외는 예외 클래스 및 발생 위치를 기준으로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder)를 참고하세요.

<a name="queues-card"></a>
#### Queues

`<livewire:pulse.queues />` 카드는 큐의 처리량, 큐에 쌓인 잡 수, 처리 중인 잡, 처리 완료된 잡, 릴리즈된 잡, 실패한 잡 수를 보여줍니다. 자세한 내용은 [queues recorder](#queues-recorder)를 참고하세요.

<a name="slow-requests-card"></a>
#### Slow Requests

`<livewire:pulse.slow-requests />` 카드는 애플리케이션으로 들어오는 요청 중 설정된 임계값(기본 1,000ms)을 초과하는 느린 요청들을 표시합니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder)를 참고하세요.

<a name="slow-jobs-card"></a>
#### Slow Jobs

`<livewire:pulse.slow-jobs />` 카드는 큐에 쌓여 실행 중인 잡들 중 설정된 임계값(기본 1,000ms)을 초과하는 느린 잡들을 보여줍니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder)를 참고하세요.

<a name="slow-queries-card"></a>
#### Slow Queries

`<livewire:pulse.slow-queries />` 카드는 애플리케이션 내에서 실행되는 데이터베이스 쿼리 중, 설정된 임계값(기본 1,000ms)을 초과하는 느린 쿼리들을 보여줍니다.

기본적으로 느린 쿼리는 바인딩 없이 SQL 쿼리와 발생 위치를 기준으로 그룹화됩니다. 단, SQL 쿼리만 기준으로 그룹화하고 위치 정보 캡처를 하지 않을 수도 있습니다.

매우 큰 SQL 쿼리의 문법 하이라이팅이 렌더링 성능에 문제를 일으키면 `without-highlighting` 프로퍼티를 통해 하이라이팅을 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [slow queries recorder](#slow-queries-recorder)를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### Slow Outgoing Requests

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP client](/docs/11.x/http-client)를 사용해 발생한 외부 요청 중 설정된 임계값(기본 1,000ms)을 초과한 느린 요청들을 보여줍니다.

기본적으로 전체 URL을 기준으로 그룹핑하지만, 유사한 요청을 정규 표현식으로 정규화하거나 그룹화할 수 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder)를 참고하세요.

<a name="cache-card"></a>
#### Cache

`<livewire:pulse.cache />` 카드는 애플리케이션의 전역 및 개별 키별 [cache](/docs/11.x/cache) 적중률과 실패율을 보여줍니다.

기본적으로 키별로 그룹화하지만, 정규 표현식을 사용해 유사한 키를 그룹화하거나 정규화할 수 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder)를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처하기 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel이 발생시키는 프레임워크 이벤트를 기반으로 엔트리를 자동 캡처합니다. 그러나 [servers recorder](#servers-recorder) 및 일부 서드파티 카드는 주기적으로 폴링해야 합니다. 이 카드를 사용하려면 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]  
> `pulse:check` 프로세스를 백그라운드에서 계속 유지하려면 Supervisor 같은 프로세스 모니터를 사용해 프로세스가 중단되지 않도록 해야 합니다.

`pulse:check` 명령은 장시간 실행되는 프로세스이므로 코드 변경사항을 반영하려면 재시작해야 합니다. 배포 과정에서 `pulse:restart` 명령어로 프로세스를 안전하게 재시작하세요:

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse는 재시작 신호를 저장하기 위해 [cache](/docs/11.x/cache)를 사용하므로, 기능 사용 전에 적절한 캐시 드라이버가 구성되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 캡처할 엔트리를 Pulse 데이터베이스에 기록하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration)의 `recorders` 섹션에서 등록 및 구성됩니다.

<a name="cache-interactions-recorder"></a>
#### Cache Interactions

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [cache](/docs/11.x/cache) 적중과 실패 정보를 캡처해 [Cache](#cache-card) 카드에서 표시합니다.

옵션으로 [샘플링](#sampling) 비율과 무시할 키 패턴을 조절할 수 있습니다.

또한 유사한 키를 하나로 그룹화하기 위해 키 그룹화를 설정할 수 있습니다. 예를 들어, 동일 유형의 데이터를 캐싱하는 키에서 고유 ID 부분을 제거할 때 사용할 수 있습니다. 그룹 설정은 정규 표현식으로 "찾기 및 치환"합니다. 설정 파일에 예시가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

가장 먼저 일치하는 패턴이 사용됩니다. 일치하는 패턴이 없으면 키를 원래대로 캡처합니다.

<a name="exceptions-recorder"></a>
#### Exceptions

`Exceptions` 레코더는 애플리케이션에서 발생하는 보고 가능한 예외 정보를 캡처해 [Exceptions](#exceptions-card) 카드에 표시합니다.

옵션으로 [샘플링](#sampling) 비율, 무시할 예외 패턴, 예외 발생 위치 캡처 여부를 설정할 수 있습니다. 위치 정보는 대시보드에 표시되어 예외 발생지를 추적하는 데 도움을 줍니다. 단, 동일한 예외가 여러 위치에서 발생하면 각 위치별로 여러 항목이 표시됩니다.

<a name="queues-recorder"></a>
#### Queues

`Queues` 레코더는 애플리케이션 큐 정보를 캡처해 [Queues](#queues-card)에 표시합니다.

옵션으로 [샘플링](#sampling) 비율과 무시할 잡 패턴을 조절할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### Slow Jobs

`SlowJobs` 레코더는 애플리케이션에서 발생하는 느린 잡 정보를 캡처해 [Slow Jobs](#slow-jobs-card)에 표시합니다.

느린 잡 임계값, [샘플링](#sampling) 비율, 무시할 잡 패턴을 옵션으로 설정할 수 있습니다.

특정 잡이 기본 임계값보다 오래 걸리는 것이 예상된다면, 잡별 임계값도 설정할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

잡의 클래스명과 일치하는 정규 표현식이 없으면 `'default'` 값을 사용합니다.

<a name="slow-outgoing-requests-recorder"></a>
#### Slow Outgoing Requests

`SlowOutgoingRequests` 레코더는 Laravel [HTTP client](/docs/11.x/http-client)를 통해 발생한 외부 요청 중 설정 임계값을 초과하는 요청을 캡처해 [Slow Outgoing Requests](#slow-outgoing-requests-card) 카드에 표시합니다.

느린 외부 요청 임계값, [샘플링](#sampling) 비율, 무시할 URL 패턴을 옵션으로 설정할 수 있습니다.

특정 요청이 기본 임계값보다 오래 걸리는 경우 요청별 임계값 설정도 가능합니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL과 일치하는 정규 표현식이 없으면 `'default'` 값을 사용합니다.

또한 URL 경로에서 고유 ID를 제거하거나 도메인별로 그룹화하는 등의 URL 그룹화 기능도 지원합니다. 정규 표현식으로 치환할 부분을 지정할 수 있습니다. 설정 파일에 예가 포함되어 있습니다:

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

처음 일치하는 패턴이 사용되며, 없으면 URL을 그대로 캡처합니다.

<a name="slow-queries-recorder"></a>
#### Slow Queries

`SlowQueries` 레코더는 애플리케이션 내에서 실행되는 데이터베이스 쿼리 중 설정 임계값을 초과하는 쿼리를 캡처해 [Slow Queries](#slow-queries-card) 카드에서 보여줍니다.

느린 쿼리 임계값, [샘플링](#sampling) 비율, 무시할 쿼리 패턴, 쿼리 위치 캡처 여부를 옵션으로 설정할 수 있습니다. 위치 정보는 대시보드에 표시되어 쿼리 출처를 파악하는 데 도움이 됩니다. 단, 동일 쿼리가 여러 위치에서 실행되면 각 위치마다 별도 항목이 표시됩니다.

특정 쿼리가 기본 임계값보다 오래 걸리는 것이 예상된다면 쿼리별 임계값도 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

쿼리 SQL과 일치하는 정규 표현식이 없으면 `'default'` 값을 사용합니다.

<a name="slow-requests-recorder"></a>
#### Slow Requests

`Requests` 레코더는 애플리케이션에 들어오는 요청 정보를 캡처해 [Slow Requests](#slow-requests-card)와 [Application Usage](#application-usage-card) 카드에 표시합니다.

느린 요청 임계값, [샘플링](#sampling) 비율, 무시할 경로를 옵션으로 설정할 수 있습니다.

특정 요청이 기본 임계값보다 오래 걸리는 것이 예상된다면 요청별 임계값도 설정할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL과 일치하는 정규 표현식이 없으면 `'default'` 값을 사용합니다.

<a name="servers-recorder"></a>
#### Servers

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 스토리지 사용량을 캡처해 [Servers](#servers-card) 카드에 표시합니다. 이 레코더는 [pulse:check 명령어](#capturing-entries)를 각 서버에서 실행해야 작동합니다.

각 서버는 고유한 이름을 가져야 합니다. 기본적으로 PHP의 `gethostname` 함수 반환값을 사용합니다. 이름을 변경하려면 `PULSE_SERVER_NAME` 환경 변수를 설정하세요:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서는 모니터링할 디렉터리를 커스터마이징할 수도 있습니다.

<a name="user-jobs-recorder"></a>
#### User Jobs

`UserJobs` 레코더는 애플리케이션에서 잡을 디스패치하는 사용자 정보를 캡처해 [Application Usage](#application-usage-card) 카드에 표시합니다.

옵션으로 [샘플링](#sampling) 비율과 무시할 잡 패턴을 설정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### User Requests

`UserRequests` 레코더는 애플리케이션에 요청을 보내는 사용자 정보를 캡처해 [Application Usage](#application-usage-card) 카드에 표시합니다.

옵션으로 [샘플링](#sampling) 비율과 무시할 URL 패턴을 설정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

앞서 살펴본 것처럼, 많은 [레코더들](#recorders)은 구성으로 특정 기준에 맞는 항목(예: 요청 URL)을 무시할 수 있습니다. 하지만 때로는 현재 인증된 사용자 같은 다른 조건을 기반으로 기록을 필터링하고 싶을 수 있습니다.

이 경우, Pulse의 `filter` 메서드에 클로저를 전달해 필터링할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드 안에서 호출합니다:

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

Pulse는 별도의 인프라 없이 기존 애플리케이션에 쉽게 통합되도록 설계되었습니다. 하지만 트래픽이 매우 많은 애플리케이션의 경우, Pulse가 애플리케이션 성능에 미치는 영향을 최소화하기 위한 여러 방식을 제공합니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용하기 (Using a Different Database)

트래픽이 많은 애플리케이션에서는 Pulse가 애플리케이션 데이터베이스에 영향을 주지 않도록 전용 데이터베이스 연결을 사용하는 것이 좋습니다.

`PULSE_DB_CONNECTION` 환경 변수를 설정해 Pulse가 사용할 [데이터베이스 연결](/docs/11.x/database#configuration)을 지정할 수 있습니다:

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인게스트 (Redis Ingest)

> [!WARNING]  
> Redis 인게스트는 Redis 6.2 이상과, `phpredis` 또는 `predis`를 애플리케이션에 설정된 Redis 클라이언트 드라이버로 요구합니다.

기본적으로 Pulse는 HTTP 응답 전송 후나 잡 처리 완료 후 바로 [설정된 데이터베이스 연결](#using-a-different-database)에 엔트리를 저장합니다. 하지만 Pulse의 Redis 인게스트 드라이버를 사용해 엔트리를 Redis 스트림으로 전송할 수 있습니다. 활성화하려면 `PULSE_INGEST_DRIVER` 환경 변수에 `redis`를 설정하세요:

```
PULSE_INGEST_DRIVER=redis
```

기본 Redis 연결은 애플리케이션의 기본 [Redis 연결](/docs/11.x/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 변경할 수 있습니다:

```
PULSE_REDIS_CONNECTION=pulse
```

Redis 인게스트를 사용하면, `pulse:work` 명령을 실행해 Redis 스트림을 모니터링하고 엔트리를 Pulse 데이터베이스로 이동시켜야 합니다:

```php
php artisan pulse:work
```

> [!NOTE]  
> 백그라운드에서 `pulse:work` 프로세스가 계속 실행되도록 하려면 Supervisor 같은 프로세스 모니터를 써서 프로세스 종료를 방지하세요.

`pulse:work` 명령어는 장시간 실행되는 프로세스이므로 코드 변경 사항을 반영하려면 재시작해야 합니다. 배포 시 `pulse:restart` 명령어를 실행해 안전하게 재시작하세요:

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse는 재시작 신호를 저장하기 위해 [cache](/docs/11.x/cache)를 사용하므로, 적절한 캐시 드라이버가 설정되어 있는지 확인하세요.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 캡처합니다. 트래픽이 많은 경우, 대시보드에서 수백만 건의 데이터베이스 행을 집계해야 하는 상황이 생길 수 있습니다. 특히 긴 시간 구간일 때 그렇습니다.

이런 경우 특정 Pulse 데이터 레코더에 "샘플링"을 적용해 일부 이벤트만 기록하도록 할 수 있습니다. 예를 들어, [`User Requests`](#user-requests-recorder) 레코더에 샘플링 비율 `0.1`을 설정하면 전체 요청 중 약 10%만 기록됩니다. 대시보드에서는 값이 보정되어 `~` 기호가 붙어 근사값임을 표시합니다.

일반적으로 특정 지표에 수집된 엔트리가 많을수록 샘플링 비율을 낮춰도 정확도가 크게 떨어지지 않습니다.

<a name="trimming"></a>
### 데이터 트리밍 (Trimming)

Pulse는 대시보드에 표시하는 기간 외의 오래된 엔트리를 자동으로 잘라냅니다(트리밍). 트리밍은 데이터 인게스트 과정에서 확률 기반 로터리 시스템을 사용하며, 이 동작은 Pulse [설정 파일](#configuration)에서 조절할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 캡처 중 스토리지 데이터베이스 연결 실패 같은 예외가 발생하면, 애플리케이션에 영향을 주지 않도록 예외를 무시하고 조용히 실패합니다.

예외 처리 방식을 커스터마이징하려면 `handleExceptionsUsing` 메서드에 클로저를 전달하세요:

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('Pulse에서 예외 발생', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
## 커스텀 카드 (Custom Cards)

Pulse는 애플리케이션 별 맞춤 데이터를 보여주는 커스텀 카드를 만들 수 있도록 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드 제작 전에 Livewire [문서](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트 (Card Components)

Laravel Pulse에서 커스텀 카드를 만들려면 기본 `Card` Livewire 컴포넌트를 확장하고, 대응하는 뷰를 정의하세요:

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

Livewire의 [지연 로딩](https://livewire.laravel.com/docs/lazy) 기능을 활용하면, `Card` 컴포넌트가 자동으로 `cols`와 `rows` 속성을 반영하는 플레이스홀더를 제공합니다.

Pulse 카드에 대응하는 뷰는 Pulse의 Blade 컴포넌트를 활용해 일관된 UI를 구현할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각 해당 Blade 컴포넌트에 전달해 카드 레이아웃을 대시보드 뷰에서 커스터마이징할 수 있습니다. 카드가 자동 갱신되도록 `wire:poll.5s=""` 속성을 추가하는 것도 좋습니다.

Livewire 컴포넌트와 템플릿을 정의한 후, [대시보드 뷰](#dashboard-customization)에 카드를 포함시킬 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]  
> 카드가 패키지에 포함되어 있다면, `Livewire::component` 메서드로 Livewire 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

카드에 Pulse 기본 컴포넌트와 클래스 이상의 별도 스타일링이 필요하면, 커스텀 CSS를 포함하는 여러 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

애플리케이션 코드에 카드를 만들고 Laravel의 [Vite 통합](/docs/11.x/vite)을 사용한다면, `vite.config.js`에서 카드 전용 CSS 진입점을 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

대시보드 뷰에서는 `@vite` Blade 디렉티브를 사용해 CSS를 포함하세요:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일 직접 포함

패키지에 포함된 Pulse 카드 등 다른 경우, Livewire 컴포넌트에 `css` 메서드를 정의해 CSS 파일 경로를 반환하도록 할 수 있습니다:

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

이 카드를 대시보드에 포함하면 Pulse가 자동으로 해당 CSS 내용을 `<style>` 태그로 인라인 포함하므로, CSS 파일을 `public` 디렉터리에 별도 배포할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 쓸 경우 불필요한 CSS를 줄이고 Pulse 기본 Tailwind 클래스와 충돌하지 않도록 별도의 Tailwind 설정 파일을 만드세요:

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

CSS 진입점에서 설정 파일을 지정합니다:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

또한 카드 뷰에 Tailwind의 [`important` 선택자 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에서 지정한 선택자(`#top-sellers`)를 일치시키는 `id` 또는 `class` 속성을 포함해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계 (Data Capture and Aggregation)

커스텀 카드는 데이터 출처에 상관없이 정보를 가져와 표시할 수 있지만, Pulse가 제공하는 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처하기 (Capturing Entries)

Pulse는 `Pulse::record` 메서드를 통해 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 기록할 엔트리의 `type`이고, 두 번째 인자는 집계를 위한 그룹화 기준인 `key`입니다. 대부분의 집계 메서드는 집계할 `value`도 지정해야 하는데, 위 예제에서는 `$sale->amount`가 이에 해당합니다. 그 후 `sum` 등 하나 이상의 집계 메서드를 호출해 Pulse가 미리 집계된 값을 "버킷"에 저장하고, 이후 효율적인 조회가 가능하도록 합니다.

사용 가능한 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]  
> 현재 인증된 사용자 ID를 기록하는 카드 패키지를 작성할 때는 애플리케이션의 [사용자 해석기 커스터마이징](#dashboard-resolving-users)을 준수하는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하세요.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회하기 (Retrieving Aggregate Data)

Pulse의 `Card` Livewire 컴포넌트를 확장할 때, 대시보드에서 조회 시점의 기간 내 집계 데이터를 가져오기 위해 `aggregate` 메서드를 사용할 수 있습니다:

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

`aggregate`는 PHP `stdClass` 객체 컬렉션을 반환합니다. 각 객체는 앞서 저장한 `key` 프로퍼티와 요청한 집계 결과 키(`sum`, `count` 등)를 가집니다:

```
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 미리 집계된 버킷에서 데이터를 조회합니다. 집계가 지정된 항목만 조회 가능하며, 가장 오래된 버킷은 기간 일부에만 포함되어 있어 Pulse가 오래된 엔트리를 추가 집계해 갭을 메워줍니다. 이를 통해 요청 시마다 전체 기간을 모두 집계하는 비용을 줄입니다.

특정 타입의 총합을 집계하려면 `aggregateTotal` 메서드를 쓸 수 있습니다. 예를 들어, 모든 사용자 매출 총합은 다음과 같이 조회합니다:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시하기 (Displaying Users)

키가 사용자 ID인 집계 데이터를 다룰 때, `Pulse::resolveUsers` 메서드로 ID를 사용자 정보로 변환할 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar` 키를 가진 객체를 반환하며, `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달해 사용할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더 (Custom Recorders)

패키지 제작자는 사용자가 데이터를 캡처하도록 설정할 수 있는 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 설정 파일 `recorders` 섹션에서 등록합니다:

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

레코더는 `$listen` 프로퍼티에 이벤트 클래스를 지정해 이벤트를 수신하고, `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 수신할 이벤트 클래스 목록.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 이벤트 기록.
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