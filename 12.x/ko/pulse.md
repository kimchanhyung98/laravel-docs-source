# Laravel Pulse (Laravel Pulse)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이징](#dashboard-customization)
    - [사용자 정보 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 수집 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능 및 사용 현황을 한눈에 파악할 수 있도록 도와줍니다. Pulse를 사용하면 느린 작업(Job)과 엔드포인트 같은 병목 현상을 추적하고, 가장 활동적인 사용자를 파악하는 등 다양한 통계를 확인할 수 있습니다.

개별 이벤트를 심층적으로 디버깅하려면 [Laravel Telescope](/docs/12.x/telescope)를 참고하십시오.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Pulse의 공식 스토리지 구현은 현재 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스가 필요합니다. 만약 다른 데이터베이스 엔진을 사용 중이라면 Pulse 데이터를 위해 별도의 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스를 준비해야 합니다.

Pulse는 Composer 패키지 매니저를 사용하여 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

다음으로 `vendor:publish` Artisan 명령어를 이용해 Pulse 설정 파일과 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터 저장을 위해 필요한 테이블을 생성하려면 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면, `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않다면, [전용 데이터베이스 커넥션을 지정](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 다양한 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나 새로운 레코더를 등록하고 고급 옵션을 설정하려면, `config/pulse.php` 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 인가 (Authorization)

Pulse 대시보드는 `/pulse` 경로를 통해 접속할 수 있습니다. 기본적으로는 `local` 환경에서만 대시보드에 접근할 수 있으므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이징하여 접근 권한을 설정해야 합니다. 다음은 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 이를 설정하는 예시입니다:

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
### 커스터마이징 (Customization)

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰 파일을 퍼블리시하여 설정할 수 있습니다. 해당 뷰 파일은 `resources/views/vendor/pulse/dashboard.blade.php`에 퍼블리시됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/) 기반으로 동작하므로, JavaScript 에셋을 다시 빌드하지 않고도 카드 및 레이아웃을 자유롭게 커스터마이징할 수 있습니다.

이 파일 내에서 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며, 카드들을 위한 그리드 레이아웃을 제공합니다. 대시보드를 화면 전체 너비로 확장하려면 `full-width` prop을 추가할 수 있습니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12 컬럼 그리드를 생성하지만, `cols` prop을 사용하여 컬럼 수를 조정할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드에는 공간 및 위치를 조절하기 위한 `cols`와 `rows` prop을 사용할 수 있습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에서는 전체 카드 내용을 스크롤 없이 표시하려면 `expand` prop을 사용할 수 있습니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 정보 해석 (Resolving Users)

애플리케이션 사용량 카드 등 사용자 정보를 표시하는 카드의 경우, Pulse는 기본적으로 사용자의 ID만 기록합니다. 대시보드를 렌더링할 때 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 해석하고, 아바타는 Gravatar 웹 서비스를 통해 표시합니다.

이 필드와 아바타 로직을 커스터마이징하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내에서 `Pulse::user` 메서드를 호출할 수 있습니다.

`user` 메서드는 표시 대상 `Authenticatable` 모델을 인수로 받아야 하며, 사용자 정보로 사용할 `name`, `extra`, `avatar` 정보를 포함한 배열을 반환해야 합니다:

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
> 인증된 사용자를 캡처하고 검색하는 방법을 완전히 커스터마이징하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하여 Laravel의 [서비스 컨테이너](/docs/12.x/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### 서버 (Servers)

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 리포팅에 대한 자세한 내용은 [서버 레코더](#servers-recorder) 문서를 참고하십시오.

인프라의 서버를 교체한 경우, 원하는 기간이 지난 후에는 더 이상 사용하지 않는 서버를 대시보드에서 숨기고 싶을 수 있습니다. 이때 `ignore-after` prop을 사용하여, 비활성 서버가 Pulse 대시보드에서 제거되는 초(second) 단위를 지정할 수 있습니다. 또는 `1 hour`, `3 days and 1 hour`와 같은 상대 시간 문자열도 입력할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량 (Application Usage)

`<livewire:pulse.usage />` 카드는 요청, 작업(Job) 디스패치, 느린 요청을 발생시키는 상위 10명의 사용자를 표시합니다.

모든 사용 지표를 동시에 한 화면에서 보고 싶다면 카드 컴포넌트를 여러 번 포함시키고 `type` 속성을 각각 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 검색하고 표시하는 방법을 커스터마이징하는 방법은 [사용자 정보 해석 문서](#dashboard-resolving-users)를 참고하십시오.

> [!NOTE]
> 애플리케이션이 많은 요청이나 작업을 처리한다면, [샘플링](#sampling) 설정을 고려해볼 수 있습니다. 자세한 내용은 [사용자 요청 레코더](#user-requests-recorder), [사용자 작업 레코더](#user-jobs-recorder), [느린 작업 레코더](#slow-jobs-recorder) 문서를 참고하십시오.

<a name="exceptions-card"></a>
#### 예외 (Exceptions)

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생하는 예외의 빈도 및 최근 발생 시점 등을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치를 기준으로 그룹화됩니다. 자세한 내용은 [예외 레코더](#exceptions-recorder) 문서를 참고하십시오.

<a name="queues-card"></a>
#### 큐 (Queues)

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 작업 관련 통계(대기 중, 처리 중, 완료, 릴리즈, 실패된 작업 건수 등)를 확인할 수 있습니다. 자세한 사항은 [큐 레코더](#queues-recorder) 문서를 참고하십시오.

<a name="slow-requests-card"></a>
#### 느린 요청 (Slow Requests)

`<livewire:pulse.slow-requests />` 카드는 설정된 임계값(기본 1,000ms)을 초과한 애플리케이션의 수신 요청을 표시합니다. 자세한 내용은 [느린 요청 레코더](#slow-requests-recorder)를 참고하십시오.

<a name="slow-jobs-card"></a>
#### 느린 작업 (Slow Jobs)

`<livewire:pulse.slow-jobs />` 카드는 설정된 임계값(기본 1,000ms)을 초과한 큐 작업을 표시합니다. 자세한 내용은 [느린 작업 레코더](#slow-jobs-recorder)를 참고하십시오.

<a name="slow-queries-card"></a>
#### 느린 쿼리 (Slow Queries)

`<livewire:pulse.slow-queries />` 카드는 설정된 임계값(기본 1,000ms)을 초과하는 애플리케이션의 데이터베이스 쿼리를 표시합니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외)와 발생 위치를 기준으로 그룹화됩니다. 단, 쿼리 위치를 캡처하지 않고 SQL 쿼리만으로 그룹화하도록 변경할 수도 있습니다.

매우 큰 SQL 쿼리에 구문 강조(syntax highlighting)가 적용되어 렌더링 성능 문제가 발생한다면, `without-highlighting` prop을 추가하여 강조를 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [느린 쿼리 레코더](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)를 통해 전송된 요청 중, 설정된 임계값(기본 1,000ms)을 초과하는 외부 HTTP 요청을 표시합니다.

기본적으로 엔트리는 전체 URL을 기준으로 그룹화됩니다. 하지만 유사한 외부 요청을 정규표현식을 사용해 그룹화하거나 정규화할 수도 있습니다. 자세한 내용은 [느린 외부 요청 레코더](#slow-outgoing-requests-recorder)를 참고하십시오.

<a name="cache-card"></a>
#### 캐시 (Cache)

`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 조회 결과(히트 및 미스) 통계를 글로벌 및 개별 키 단위로 보여줍니다.

기본적으로 엔트리는 키(key) 단위로 그룹화됩니다. 필요하다면 유사한 키를 정규표현식으로 그룹화하거나 정규화할 수 있습니다. 자세한 내용은 [캐시 상호작용 레코더](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel에서 발생하는 프레임워크 이벤트를 기반으로 엔트리를 자동 캡처합니다. 하지만 [서버 레코더](#servers-recorder) 및 일부 서드파티 카드는 주기적으로 정보를 폴링해야 합니다. 이런 카드들을 사용하려면, 개별 애플리케이션 서버마다 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor 같은 프로세스 관리자를 활용해야 하며, 명령어가 중단되지 않도록 관리해야 합니다.

`pulse:check` 명령어는 장시간 실행되는 프로세스이므로, 코드베이스 변경을 반영하려면 재시작이 필요합니다. 애플리케이션 배포 과정에서 `pulse:restart` 명령어로 명령을 안정적으로 재시작할 수 있습니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호를 저장하므로, 해당 기능 사용 전 캐시 드라이버가 제대로 설정되어 있는지 확인하십시오.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 엔트리를 캡처하여 Pulse 데이터베이스에 기록하는 역할을 담당합니다. 레코더는 [Pulse 설정 파일](#configuration) 내 `recorders` 섹션에서 등록 및 설정할 수 있습니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용 (Cache Interactions)

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [캐시](/docs/12.x/cache) 히트 및 미스 정보를 [캐시 카드](#cache-card)에 표시하기 위해 캡처합니다.

[샘플 비율](#sampling) 및 무시할 키 패턴을 선택적으로 조정할 수 있습니다.

또한 비슷한 키를 하나의 엔트리로 그룹화하도록 키 그룹화를 설정할 수 있습니다. 예를 들어, 동일한 데이터 유형을 캐싱하되 각기 다른 고유 ID가 포함된 키를 그룹화하고자 할 수 있습니다. 그룹화는 정규표현식을 사용하여 키의 일부를 "찾아서 바꾸기" 방식으로 처리할 수 있으며, 설정 파일에 예제가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

첫 번째로 매칭되는 패턴이 적용되며, 매칭되는 패턴이 없다면 키를 원본 그대로 캡처합니다.

<a name="exceptions-recorder"></a>
#### 예외 (Exceptions)

`Exceptions` 레코더는 애플리케이션에서 보고 가능한 예외에 대한 정보를 [예외 카드](#exceptions-card)에 표시하기 위해 캡처합니다.

[샘플 비율](#sampling)과 무시할 예외 패턴을 선택적으로 조정할 수 있습니다. 또한 예외가 발생한 위치 정보를 캡처할지 여부를 설정할 수 있습니다. 위치 정보를 캡처하면 예외의 출처를 추적하는 데 도움이 되지만, 동일한 예외가 여러 위치에서 발생한다면 고유 위치별로 여러 번 표시될 수 있습니다.

<a name="queues-recorder"></a>
#### 큐 (Queues)

`Queues` 레코더는 애플리케이션의 큐 관련 정보를 [큐 카드](#queues-card)에 표시하기 위해 캡처합니다.

[샘플 비율](#sampling) 및 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업 (Slow Jobs)

`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업 정보를 [느린 작업 카드](#slow-jobs-recorder)에 표시하기 위해 캡처합니다.

느린 작업 임계값, [샘플 비율](#sampling), 무시할 작업 패턴을 개별적으로 조정할 수 있습니다.

특정 작업이 다른 작업보다 오래 걸릴 수 있다면, 개별 작업 임계값을 다음과 같이 지정할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

정규표현식 중 작업의 클래스명이 매칭되지 않으면, `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)를 통해 발생한 외부 HTTP 요청 중, 설정된 임계값을 초과하는 요청을 [느린 외부 요청 카드](#slow-outgoing-requests-card)에 표시하기 위해 캡처합니다.

느린 외부 요청 임계값, [샘플 비율](#sampling), 무시할 URL 패턴을 선택적으로 조정 가능합니다.

특정 외부 요청이 다른 요청보다 오래 걸릴 것으로 예상된다면, 개별 요청 임계값을 설정할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규표현식이 URL과 매칭되지 않으면, `'default'` 값이 사용됩니다.

또한 비슷한 URL을 하나의 엔트리로 그룹화할 수도 있습니다. 예를 들어, URL 경로에서 고유 ID를 제거하거나 도메인 단위로 그룹화할 수 있습니다. 그룹화는 정규표현식을 사용하여 URL의 일부를 치환 방식으로 처리합니다. 일부 예시는 설정 파일에 포함되어 있습니다:

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

처음으로 매칭되는 패턴이 적용되며, 매칭되는 패턴이 없다면 URL을 원본 그대로 캡처합니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리 (Slow Queries)

`SlowQueries` 레코더는 설정된 임계값을 초과하는 애플리케이션의 데이터베이스 쿼리를 [느린 쿼리 카드](#slow-queries-card)에 표시하기 위해 캡처합니다.

느린 쿼리 임계값, [샘플 비율](#sampling), 무시할 쿼리 패턴, 쿼리 위치 정보 캡처 여부 등을 선택적으로 조정할 수 있습니다. 위치 정보는 쿼리의 발생 위치를 추적하는 데 도움이 되지만, 동일 쿼리가 여러 곳에서 실행된다면 각 위치별로 엔트리가 여러 번 표시될 수 있습니다.

특정 쿼리가 다른 쿼리보다 오래 걸릴 것으로 예상된다면, 개별 쿼리 임계값을 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

정규표현식과 쿼리의 SQL이 매칭되지 않으면, `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청 (Slow Requests)

`Requests` 레코더는 애플리케이션으로 들어오는 요청 정보를 [느린 요청 카드](#slow-requests-card) 및 [애플리케이션 사용량 카드](#application-usage-card)에 표시하기 위해 캡처합니다.

느린 라우트 임계값, [샘플 비율](#sampling), 무시할 경로 등을 개별적으로 조정할 수 있습니다.

특정 요청이 다른 요청보다 오래 걸릴 것으로 예상된다면, 개별 요청 임계값을 다음과 같이 지정할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규표현식과 요청의 URL이 매칭되지 않으면, `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버 (Servers)

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장소 사용량을 [서버 카드](#servers-card)에 표시하기 위해 캡처합니다. 이 레코더는 [pulse:check 명령어](#capturing-entries)가 각 서버에서 실행되고 있어야 작동합니다.

각 서버마다 고유한 이름이 필요하며, 기본적으로는 PHP의 `gethostname` 함수 결과가 사용됩니다. 필요하다면 `PULSE_SERVER_NAME` 환경 변수를 사용해 이름을 지정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일을 통해 모니터링할 디렉토리 경로도 커스터마이징할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업 (User Jobs)

`UserJobs` 레코더는 애플리케이션에서 작업을 디스패치하는 사용자 정보를 [애플리케이션 사용량 카드](#application-usage-card)에 표시하기 위해 캡처합니다.

[샘플 비율](#sampling) 및 무시할 작업 패턴을 개별적으로 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청 (User Requests)

`UserRequests` 레코더는 애플리케이션에 요청을 보내는 사용자 정보를 [애플리케이션 사용량 카드](#application-usage-card)에 표시하기 위해 캡처합니다.

[샘플 비율](#sampling) 및 무시할 URL 패턴을 개별적으로 조정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

앞에서 살펴본 것처럼, 다양한 [레코더](#recorders)는 설정을 통해 요청 URL 등 값에 기반하여 특정 엔트리를 무시할 수 있습니다. 하지만 경우에 따라 현재 인증된 사용자 등 다른 조건에 의해 기록을 필터링해야 할 수도 있습니다. 이를 위해 Pulse의 `filter` 메서드에 클로저를 전달하여 커스텀 필터링 로직을 적용할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 사용합니다:

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
## 성능 (Performance)

Pulse는 별도의 추가 인프라 없이 기존 애플리케이션에 손쉽게 도입할 수 있도록 설계되었습니다. 하지만 트래픽이 많은 애플리케이션에서는 Pulse가 성능에 미치는 영향을 최소화하는 다양한 방법들이 제공됩니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용 (Using a Different Database)

트래픽이 많은 애플리케이션이라면 Pulse 전용 데이터베이스 커넥션을 사용하여 애플리케이션의 주 데이터베이스에 미치는 영향을 줄일 수 있습니다.

Pulse에서 사용할 [데이터베이스 커넥션](/docs/12.x/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수로 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis Ingest

> [!WARNING]
> Redis Ingest 기능을 사용하려면 Redis 6.2 이상과 `phpredis` 또는 `predis`가 Redis 클라이언트 드라이버로 설정되어 있어야 합니다.

기본적으로 Pulse는 [설정된 데이터베이스 커넥션](#using-a-different-database)에 HTTP 응답 전송 후 또는 작업 완료 후 엔트리를 직접 저장합니다. 하지만 Pulse의 Redis ingest 드라이버를 활성화하면 엔트리가 Redis 스트림으로 전송됩니다. 이를 활성화하려면 `PULSE_INGEST_DRIVER` 환경 변수를 다음과 같이 설정합니다:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 애플리케이션의 [기본 Redis 커넥션](/docs/12.x/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 커넥션을 커스터마이징할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis ingest 드라이버 사용 시, 큐에 사용되는 Redis와는 반드시 별도의 Redis 커넥션을 사용해야 합니다.

Redis ingest를 사용할 때는 Redis 스트림을 모니터링해 엔트리를 Pulse 데이터베이스로 옮기는 작업을 담당하는 `pulse:work` 명령어를 실행해야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor 같은 프로세스 관리자 활용이 권장됩니다.

`pulse:work` 명령어도 장시간 실행되는 프로세스이므로 코드 변경사항을 반영하려면 재시작이 필요합니다. 배포 과정에서 `pulse:restart` 명령어를 호출하여 안정적으로 재시작할 수 있습니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호를 저장하므로, 해당 기능 사용 전 캐시 드라이버가 정상적으로 설정되어 있는지 확인하십시오.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 발생한 모든 관련 이벤트를 캡처합니다. 트래픽이 많은 애플리케이션에서는 장기간 대시보드에서 집계를 수행할 때 수백만 개의 데이터 행이 필요할 수 있습니다.

이럴 때는 특정 Pulse 데이터 레코더에서 "샘플링"을 활성화할 수 있습니다. 예를 들어 [사용자 요청 레코더](#user-requests-recorder)의 샘플 비율을 `0.1`로 설정하면, 전체 요청의 약 10%만 기록하게 됩니다. 대시보드에는 값이 상향 조정되어 보여지며, 대략적인 값임을 나타내기 위해 `~` 기호가 붙게 됩니다.

일반적으로 특정 메트릭에 대한 엔트리 수가 많을수록 정확도를 크게 잃지 않고 샘플 비율을 더 낮게 설정할 수 있습니다.

<a name="trimming"></a>
### 트리밍 (Trimming)

Pulse는 대시보드에서 설정된 표시 기간을 벗어난 데이터 엔트리를 자동으로 트리밍(삭제)합니다. 트리밍은 데이터 인제스트 후 로터리(lottery) 방식으로 발생하며, Pulse [설정 파일](#configuration)에서 커스터마이징할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 캡처 시 저장 데이터베이스 연결 불가 등 예외가 발생하는 경우, Pulse는 애플리케이션에 영향을 미치지 않도록 조용히 실패합니다.

이 예외 처리 방식을 커스터마이징하려면, `handleExceptionsUsing` 메서드에 클로저를 등록할 수 있습니다:

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
## 커스텀 카드 (Custom Cards)

Pulse는 애플리케이션에 특화된 데이터를 표시할 수 있도록 커스텀 카드를 만들 수 있습니다. Pulse는 [Livewire](https://livewire.laravel.com)를 기반으로 하므로, 커스텀 카드를 만들기 전에 [Livewire 문서](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트 (Card Components)

Laravel Pulse에서 커스텀 카드를 만들려면, 기본 `Card` Livewire 컴포넌트를 상속받아 해당하는 뷰를 정의하면 됩니다:

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

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 경우, `Card` 컴포넌트는 전달받은 `cols`와 `rows` 속성에 맞춰 자동으로 플레이스홀더를 표시해줍니다.

카드의 뷰 파일 작성 시, 일관된 디자인을 위해 Pulse의 Blade 컴포넌트를 활용할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수들은 각각 Blade 컴포넌트에 전달하여 대시보드 뷰에서 카드 레이아웃을 자유롭게 커스터마이즈할 수 있습니다. 카드가 자동으로 갱신되도록 하려면 뷰에 `wire:poll.5s=""` 속성을 추가하는 것도 좋습니다.

Livewire 컴포넌트와 템플릿을 정의했다면, [대시보드 뷰](#dashboard-customization)에서 카드를 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 만약 카드를 패키지로 개발했다면, `Livewire::component` 메서드를 사용하여 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

카드에 Pulse에서 제공하는 클래스 및 컴포넌트 이외의 추가 CSS 스타일링이 필요하다면, 다음 방법 중 하나를 사용할 수 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

애플리케이션 코드베이스 내부에 커스텀 카드가 있고, Laravel의 [Vite 통합](/docs/12.x/vite)을 사용하는 경우, `vite.config.js` 파일에 카드 전용 CSS 엔트리 포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

이후 [대시보드 뷰](#dashboard-customization)에 `@vite` Blade 디렉티브를 사용해 CSS 엔트리포인트를 포함하면 됩니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

Pulse 카드가 패키지에 포함되어 있거나, 다른 상황에서는 Livewire 컴포넌트에서 `css` 메서드를 정의해 추가 스타일시트 파일의 경로를 반환할 수 있습니다:

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

이 카드가 대시보드에 포함될 때 Pulse는 해당 파일의 내용을 자동으로 `<style>` 태그로 임베드하므로, 추가로 public 디렉터리로 퍼블리시하지 않아도 됩니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 때는 전용 CSS 엔트리포인트를 생성해야 합니다. 다음 예시처럼 Tailwind의 [preflight](https://tailwindcss.com/docs/preflight) 기본 스타일은 이미 Pulse에 포함되어 있으므로 제외하고, CSS 선택자를 이용해 Tailwind 범위를 제한(스코프)해야 Pulse의 Tailwind 클래스와 충돌을 방지할 수 있습니다:

```css
@import "tailwindcss/theme.css";

@custom-variant dark (&:where(.dark, .dark *));
@source "./../../views/livewire/pulse/top-sellers.blade.php";

@theme {
  /* ... */
}

#top-sellers {
  @import "tailwindcss/utilities.css" source(none);
}
```

엔트리포인트 CSS의 선택자와 일치하도록 카드 뷰에 `id` 또는 `class` 속성을 추가해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 수집 및 집계 (Data Capture and Aggregation)

커스텀 카드는 어디에서든 데이터를 가져와 표시할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 적극 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 수집 (Capturing Entries)

Pulse의 `Pulse::record` 메서드를 사용해 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 엔트리의 `type`, 두 번째 인자는 집계 데이터의 그룹화를 위한 `key`입니다. 대부분의 집계 메서드에는 집계할 `value`도 지정해야 하며, 예시에서는 `$sale->amount`가 그것입니다. 필요한 집계 방식(예: `sum`)을 추가로 호출하면, Pulse가 "버킷" 단위로 미리 집계된 값을 효율적으로 저장하고 이후 조회에 활용합니다.

지원되는 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 기록해야 하는 카드 패키지를 빌드할 때는, 애플리케이션의 [사용자 정보 해석 커스터마이징](#dashboard-resolving-users)을 반영할 수 있도록 `Pulse::resolveAuthenticatedUserId()` 메서드를 이용하는 것이 좋습니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회 (Retrieving Aggregate Data)

Pulse의 `Card` Livewire 컴포넌트를 확장할 때, `aggregate` 메서드를 사용해 대시보드에서 조회 중인 기간 범위의 집계 데이터를 조회할 수 있습니다:

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

`aggregate` 메서드는 PHP `stdClass` 객체 컬렉션을 반환합니다. 각 객체에는 앞서 캡처한 `key` 속성과 요청한 집계값(예: `sum`, `count`)이 포함되어 있습니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 미리 집계된 버킷에서 데이터를 가져오며, 지정한 집계값은 `Pulse::record`에서 미리 세팅되어야 합니다. 가장 오래된 버킷은 기간 초과 범위를 일부 포함할 수 있으므로, Pulse가 누락 기간의 엔트리를 수동 집계해 전체 기간에 대한 정확한 값을 제공합니다.

특정 타입에 대해 전체 합계를 조회하려면 `aggregateTotal` 메서드를 사용할 수 있습니다. 예를 들어 다음은 모든 사용자 판매 합계를 조회하는 예시입니다.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시 (Displaying Users)

key 값이 사용자 ID인 집계를 다룰 때는 `Pulse::resolveUsers` 메서드를 사용해 해당 키를 가진 사용자 레코드를 조회할 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar` 키를 가진 객체를 반환하며, 이 값을 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달할 수도 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더 (Custom Recorders)

패키지 제작자는 사용자에게 데이터 캡처 설정을 구성할 수 있도록 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 설정 파일 내 `recorders` 섹션에 등록합니다:

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

레코더는 `$listen` 속성을 지정해 이벤트를 수신할 수 있습니다. Pulse는 리스너를 자동 등록하며, 레코더의 `record` 메서드를 호출합니다:

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