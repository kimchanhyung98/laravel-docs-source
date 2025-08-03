# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이징](#dashboard-customization)
    - [사용자 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처하기](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용하기](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 구성요소](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있는 인사이트를 제공합니다. Pulse를 통해 느린 작업 및 엔드포인트와 같은 병목 현상을 추적하고, 가장 활발한 사용자를 찾는 등의 작업이 가능합니다.

개별 이벤트에 대한 심도 있는 디버깅이 필요하다면 [Laravel Telescope](/docs/10.x/telescope)를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> 현재 Pulse의 1차 저장소 구현은 MySQL 또는 PostgreSQL 데이터베이스를 요구합니다. 다른 데이터베이스 엔진을 사용하고 있다면, Pulse 데이터 저장용으로 별도의 MySQL 또는 PostgreSQL 데이터베이스가 필요합니다.

Pulse는 현재 베타 버전이므로, `composer.json` 파일에서 베타 패키지 설치를 허용하도록 최소 안정성 설정을 조정해야 할 수 있습니다:

```json
"minimum-stability": "beta",
"prefer-stable": true
```

그런 다음 Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Pulse를 설치하세요:

```sh
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 통해 Pulse의 설정 및 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, 데이터 저장에 필요한 테이블을 생성하기 위해 `migrate` 명령어를 실행하세요:

```shell
php artisan migrate
```

Pulse의 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]  
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않다면, [전용 데이터베이스 연결 설정](#using-a-different-database)을 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 여러 설정 옵션은 환경변수를 통해 제어할 수 있습니다. 사용 가능한 옵션 확인, 새로운 레코더 등록, 고급 설정을 위해 `config/pulse.php` 설정 파일을 퍼블리시 하세요:

```sh
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 인가 (Authorization)

Pulse 대시보드는 `/pulse` 경로에서 접근할 수 있습니다. 기본적으로 이 대시보드는 `local` 환경에서만 접근 가능하므로, 운영 환경에서 접근을 허용하려면 `'viewPulse'` 인가 게이트를 커스터마이징 해야 합니다. 이는 애플리케이션의 `app/Providers/AuthServiceProvider.php` 파일에서 다음과 같이 구현할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 인증 및 인가 서비스 등록.
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

Pulse 대시보드의 카드 및 레이아웃은 대시보드 뷰를 퍼블리시하여 구성할 수 있습니다. 뷰는 `resources/views/vendor/pulse/dashboard.blade.php` 경로로 퍼블리시됩니다:

```sh
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 구현되어 있어, JavaScript 자산을 재빌드하지 않고도 카드와 레이아웃을 수정할 수 있습니다.

퍼블리시한 뷰 파일 내에서 `<x-pulse>` 컴포넌트가 대시보드를 렌더링하고 카드들을 위한 그리드 레이아웃을 제공합니다. 화면 전체 너비를 활용하려면 `full-width` prop을 컴포넌트에 제공하세요:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>`는 12컬럼 그리드를 생성하지만, `cols` prop을 사용해 컬럼 수를 조정할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드 컴포넌트는 공간과 위치 제어를 위해 `cols`와 `rows` prop을 받습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분 카드들은 스크롤 대신 전체 카드를 보여주는 `expand` prop도 지원합니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 해석 (Resolving Users)

사용자 정보를 보여주는 카드(예: Application Usage 카드는) Pulse가 사용자 ID만 기록합니다. 대시보드 렌더링 시 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 해석하고, Gravatar 웹 서비스를 이용해 아바타를 표시합니다.

사용자 필드 및 아바타를 커스터마이징 하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 호출하세요.

`user` 메서드는 표시할 `Authenticatable` 모델을 인수로 받아 사용자 이름(`name`), 추가 정보(`extra`), 아바타(`avatar`) 정보를 담은 배열을 반환하는 클로저를 받습니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * 애플리케이션 서비스 부트스트랩.
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
> 인증된 사용자를 캡처하고 조회하는 방식을 완전히 커스터마이즈 하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고, 이를 Laravel의 [서비스 컨테이너](/docs/10.x/container#binding-a-singleton)에 바인딩하면 됩니다.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### 서버 (Servers)

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 리포팅에 관한 상세 정보는 [servers recorder](#servers-recorder) 문서를 참조하세요.

<a name="application-usage-card"></a>
#### 애플리케이션 사용 (Application Usage)

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나 작업을 실행하며, 느린 요청을 경험한 상위 10명의 사용자를 표시합니다.

모든 사용량 지표를 화면에 동시에 보려면 카드를 여러 번 포함하고 `type` 속성으로 유형을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 어떻게 조회하고 표시하는지 커스터마이징하는 방법은 [사용자 해석 문서](#dashboard-resolving-users)를 참고하세요.

> [!NOTE]  
> 애플리케이션에 많은 요청이 들어오거나 작업이 많다면 [샘플링](#sampling)을 활성화하는 것을 권장합니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외 (Exceptions)

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외 빈도와 최근 발생 시점을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치를 기준으로 그룹핑됩니다. 상세 내용은 [exceptions recorder](#exceptions-recorder) 문서를 확인하세요.

<a name="queues-card"></a>
#### 큐 (Queues)

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리량을 나타내며, 대기 중, 처리 중, 처리 완료, 다시 출시, 실패한 작업 수를 보여줍니다. 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참조하세요.

<a name="slow-requests-card"></a>
#### 느린 요청 (Slow Requests)

`<livewire:pulse.slow-requests />` 카드는 설정된 임계값(기본 1,000ms)을 초과한 애플리케이션으로 들어오는 요청을 보여줍니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업 (Slow Jobs)

`<livewire:pulse.slow-jobs />` 카드는 설정된 임계값(기본 1,000ms)을 초과하는 대기 중인 작업을 보여줍니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리 (Slow Queries)

`<livewire:pulse.slow-queries />` 카드는 설정된 임계값(기본 1,000ms)을 초과하는 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 바인딩 없이 SQL 쿼리와 발생 위치를 기준으로 그룹핑되지만, 위치 캡처를 하지 않고 SQL 쿼리만으로 그룹핑할 수도 있습니다.

자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/10.x/http-client)를 통해 발생한, 설정된 임계값(기본 1,000ms)을 초과하는 외부 요청을 보여줍니다.

기본적으로 전체 URL 기준으로 그룹화하지만, 정규 표현식을 사용하여 URL을 정규화하거나 유사 요청을 그룹화할 수 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 확인하세요.

<a name="cache-card"></a>
#### 캐시 (Cache)

`<livewire:pulse.cache />` 카드는 애플리케이션의 전역 및 개별 키 별 캐시 적중(hit) 및 미스(miss) 통계를 보여줍니다.

기본적으로 키 기준으로 그룹핑되지만, 정규 표현식을 사용해 유사한 키를 묶어 그룹화할 수도 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참조하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처하기 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel이 발행하는 프레임워크 이벤트를 자동으로 캡처합니다. 하지만 [servers recorder](#servers-recorder) 및 일부 서드파티 카드들은 주기적으로 정보를 폴링해야 합니다. 이러한 카드를 사용하려면 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]  
> `pulse:check` 프로세스가 항상 백그라운드에서 계속 실행되도록 하려면 Supervisor 같은 프로세스 모니터를 사용하는 것이 좋습니다.

`pulse:check`는 장시간 실행되는 프로세스이므로 코드 변경 사항을 자동으로 감지하지 못합니다. 배포 과정에서 `pulse:restart` 명령어로 프로세스를 안전하게 재시작해야 합니다:

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse가 재시작 신호를 저장하는 데 [캐시](/docs/10.x/cache)를 사용하므로 캐시 드라이버가 애플리케이션에 적절히 설정되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 캡처한 데이터를 Pulse 데이터베이스에 기록하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration)의 `recorders` 섹션에서 등록 및 설정됩니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용 (Cache Interactions)

`CacheInteractions` 레코더는 애플리케이션 내 발생하는 [캐시](/docs/10.x/cache) 적중 및 미스 정보를 캡처하여 [캐시](#cache-card) 카드에 표시합니다.

샘플링 비율([샘플링](#sampling))과 무시할 키 패턴을 조정할 수 있습니다.

또한 유사한 캐시 키를 하나로 그룹화할 수 있도록 정규 표현식을 이용한 그룹 설정이 가능합니다. 예를 들어 같은 유형의 데이터를 캐시하나 키 내 고유 ID를 제거하고자 할 때 유용합니다. 설정 파일에 예시가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

가장 먼저 일치하는 패턴이 적용되며, 일치하는 패턴이 없다면 키는 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외 (Exceptions)

`Exceptions` 레코더는 애플리케이션 내 보고 가능한 예외 정보를 캡처하여 [예외](#exceptions-card) 카드에 표시합니다.

샘플링 비율과 무시할 예외 패턴, 예외 발생 위치 캡처 여부를 설정할 수 있습니다. 위치 정보는 대시보드에서 예외 발생 지점을 추적할 수 있게 도우나 동일 예외가 여러 위치에서 발생하면 각각 별도로 표시됩니다.

<a name="queues-recorder"></a>
#### 큐 (Queues)

`Queues` 레코더는 애플리케이션 큐 상태를 캡처하여 [큐](#queues-card) 카드에 표시합니다.

샘플링 비율과 무시할 작업 패턴을 설정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업 (Slow Jobs)

`SlowJobs` 레코더는 애플리케이션의 느린 작업 정보를 캡처하여 [느린 작업](#slow-jobs-recorder) 카드에 표시합니다.

느린 작업 임계값, 샘플링 비율, 무시할 작업 패턴을 설정할 수 있습니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/10.x/http-client)를 통해 발생한 느린 외부 HTTP 요청을 캡처하여 [느린 외부 요청](#slow-outgoing-requests-card) 카드에 표시합니다.

느린 요청 임계값, 샘플링 비율, 무시할 URL 패턴을 설정할 수 있습니다.

또한 유사한 URL을 하나로 그룹화하는 설정이 가능하며, URL 경로의 고유 ID 제거나 도메인별 그룹화가 그 예입니다. 정규 표현식을 사용하며, 예시가 설정 파일에 포함되어 있습니다:

```php
Recorders\OutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

첫 번째 매칭되는 패턴이 적용되고, 없는 경우 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리 (Slow Queries)

`SlowQueries` 레코더는 애플리케이션에서 실행된, 설정된 임계값을 초과한 데이터베이스 쿼리를 캡처하여 [느린 쿼리](#slow-queries-card) 카드에 표시합니다.

느린 쿼리 임계값, 샘플링 비율, 무시할 쿼리 패턴, 쿼리 위치 캡처 여부를 설정할 수 있습니다. 위치 정보는 대시보드에서 쿼리 발생 지점을 추적하는 데 도움이 되지만, 동일 쿼리가 여러 위치에서 발생하면 각각 별도 표시됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청 (Slow Requests)

`Requests` 레코더는 애플리케이션에 들어오는 요청 데이터를 캡처하여 [느린 요청](#slow-requests-card) 및 [애플리케이션 사용](#application-usage-card) 카드에 표시합니다.

느린 경로 임계값, 샘플링 비율, 무시할 경로를 설정할 수 있습니다.

<a name="servers-recorder"></a>
#### 서버 (Servers)

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장 공간 사용량을 캡처하여 [서버](#servers-card) 카드에 보여줍니다. 이 레코더는 각 서버에서 [`pulse:check` 명령어](#capturing-entries)가 실행 중이어야 합니다.

각 보고 서버는 고유한 이름이 있어야 하며, 기본적으로 PHP의 `gethostname` 함수가 반환하는 값을 사용합니다. 이름을 직접 지정하려면 `PULSE_SERVER_NAME` 환경변수를 설정하세요:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링할 디렉터리도 지정할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업 (User Jobs)

`UserJobs` 레코더는 애플리케이션에서 작업을 실행하는 사용자 정보를 캡처하여 [애플리케이션 사용](#application-usage-card) 카드에 표시합니다.

샘플링 비율과 무시할 작업 패턴을 설정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청 (User Requests)

`UserRequests` 레코더는 애플리케이션에 요청을 보내는 사용자 정보를 캡처하여 [애플리케이션 사용](#application-usage-card) 카드에 표시합니다.

샘플링 비율과 무시할 작업 패턴을 설정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

여러 [레코더](#recorders)는 설정을 통해 요청 URL 등 값에 따라 특정 엔트리를 무시하는 기능을 제공합니다. 하지만 때때로 현재 인증된 사용자 등 다른 조건에 따라 기록을 필터링하는 것이 필요할 수 있습니다.

이럴 때는 Pulse의 `filter` 메서드에 클로저를 전달하여 조건을 정의할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * 애플리케이션 서비스 부트스트랩.
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

Pulse는 추가 인프라 없이 기존 애플리케이션에 바로 도입할 수 있도록 설계되었습니다. 하지만 고트래픽 환경에서는 Pulse가 애플리케이션 성능에 미치는 영향을 줄이기 위한 여러 방법이 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용하기 (Using a Different Database)

고트래픽 환경에서는 Pulse가 애플리케이션 기본 데이터베이스에 영향을 미치지 않도록 전용 데이터베이스 연결을 사용하는 것이 좋습니다.

Pulse가 사용하는 [데이터베이스 연결](/docs/10.x/database#configuration)은 `PULSE_DB_CONNECTION` 환경변수를 설정해 커스터마이즈할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis Ingest

> [!WARNING]  
> Redis Ingest는 Redis 6.2 이상과 `phpredis` 또는 `predis` 클라이언트 드라이버가 필요합니다.

기본적으로 Pulse는 HTTP 응답이 클라이언트로 전송되거나 작업 처리가 완료된 후, [설정된 데이터베이스 연결](#using-a-different-database)에 직접 엔트리를 저장합니다. 하지만 Pulse의 Redis ingest 드라이버를 사용하면 대신 Redis 스트림에 엔트리를 전송할 수 있습니다. 이를 위해 `PULSE_INGEST_DRIVER` 환경변수를 설정하세요:

```
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본 [Redis 연결](/docs/10.x/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경변수로 변경할 수 있습니다:

```
PULSE_REDIS_CONNECTION=pulse
```

Redis ingest를 사용할 때는 `pulse:work` 명령어를 실행하여 스트림을 모니터링하고, Redis에서 Pulse 데이터베이스 테이블로 엔트리를 이동시켜야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]  
> `pulse:work` 프로세스가 백그라운드에서 항상 실행되도록 하려면 Supervisor 같은 프로세스 모니터를 사용하는 것이 좋습니다.

`pulse:work`도 장시간 실행되는 프로세스이므로 코드 변경 사항을 인식하지 못합니다. 배포 시 `pulse:restart` 명령어로 안전하게 재시작하세요:

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse는 재시작 신호를 저장하는 데 [캐시](/docs/10.x/cache)를 사용하므로, 캐시 드라이버가 올바로 구성되어 있는지 확인해야 합니다.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 캡처합니다. 고트래픽 환경에선 대시보드에서 수백만 건의 데이터베이스 행을 집계해야 할 수도 있습니다, 특히 긴 기간을 조회할 때 그렇습니다.

이럴 때는 특정 Pulse 데이터 레코더에 "샘플링" 기능을 활성화할 수 있습니다. 예를 들어 [`User Requests`](#user-requests-recorder) 레코더의 샘플 비율을 `0.1`로 설정하면, 약 10% 요청만 기록됩니다. 대시보드에서는 값이 확대되고 `~` 기호가 붙어 대략치임을 표시합니다.

일반적으로 특정 메트릭에 데이터가 많을수록, 샘플 비율을 낮춰도 정확도를 크게 떨어뜨리지 않고 사용 가능합니다.

<a name="trimming"></a>
### 트리밍 (Trimming)

Pulse는 대시보드 기간 범위를 벗어난 저장 엔트리를 자동으로 삭제(트리밍)합니다. 트리밍 작업은 데이터 수집 시 복권 방식을 사용하며, 이 방식은 Pulse [설정 파일](#configuration)에서 조정할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 수집 중 예를 들어 저장소 데이터베이스 연결 실패 같은 예외가 발생하면, 애플리케이션에 영향을 주지 않도록 조용히 실패합니다.

예외 처리 방식을 커스터마이징하려면 `handleExceptionsUsing` 메서드에 클로저를 제공하세요:

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

Pulse는 애플리케이션의 특수한 요구에 맞는 커스텀 카드를 만들 수 있도록 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드를 만들기 전에 Livewire 문서를 한번 살펴보시는 것을 권장합니다.

<a name="custom-card-components"></a>
### 카드 구성요소 (Card Components)

Laravel Pulse에서 커스텀 카드를 만드는 것은 기본 `Card` Livewire 컴포넌트를 확장하고 대응하는 뷰를 정의하는 것으로 시작합니다:

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

Livewire의 [레이지 로딩](https://livewire.laravel.com/docs/lazy) 기능을 사용할 경우, `Card` 컴포넌트는 `cols` 및 `rows` 속성을 반영하는 플레이스홀더를 자동으로 제공합니다.

Pulse 카드에 대응하는 뷰를 작성할 때는 일관된 UI를 위해 Pulse의 Blade 컴포넌트를 활용하세요:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 카드 레이아웃 커스터마이징을 위해 대시보드 뷰에서 전달되어야 합니다. 카드가 자동 업데이트되도록 하려면 `wire:poll.5s=""` 속성을 포함하면 됩니다.

정의한 Livewire 컴포넌트와 템플릿은 [대시보드 뷰](#dashboard-customization)에서 카드로 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]  
> 카드가 패키지에 포함된 경우, Livewire 컴포넌트를 `Livewire::component` 메서드로 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

Pulse 기본 클래스와 구성요소 이외에 별도의 CSS가 필요하다면, 카드에 커스텀 CSS를 포함하는 몇 가지 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

커스텀 카드가 애플리케이션 코드베이스 내에 있고 Laravel의 [Vite 통합](/docs/10.x/vite)을 사용 중이라면, `vite.config.js` 파일에 카드 전용 CSS 진입점(entry point)을 추가하세요:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

대시보드 뷰에서 `@vite` Blade 지시자를 사용하여 카드용 CSS 진입점을 포함시킬 수 있습니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일 직접 포함

패키지 내 Pulse 카드 등 다른 경우에는 Livewire 컴포넌트에 `css` 메서드를 정의해 CSS 파일 경로를 반환하도록 할 수 있습니다:

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

이 카드가 대시보드에 포함되면 Pulse가 CSS 파일 내용을 `<style>` 태그에 자동으로 포함하므로 `public` 디렉터리에 퍼블리시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 때는 불필요한 CSS 로딩이나 Pulse Tailwind 클래스와 충돌을 피하기 위해 별도의 Tailwind 설정 파일을 만드는 것이 좋습니다:

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

CSS 진입점에 다음과 같이 설정 파일을 지정하세요:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

또한 카드 뷰에 Tailwind `important` 설정과 맞는 `id` 또는 `class` 속성을 추가해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계 (Data Capture and Aggregation)

커스텀 카드에서 데이터를 어디서든 가져와 표시할 수 있지만, Pulse의 강력한 데이터 기록 및 집계 시스템을 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처하기 (Capturing Entries)

Pulse는 `Pulse::record` 메서드를 사용해 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드 첫 번째 인자는 기록할 엔트리의 `type`이며, 두 번째 인자는 집계할 때 그룹핑 기준이 될 `key`입니다. 대부분의 집계 메서드는 집계할 `value`를 지정해야 하며, 위 예시에서는 `$sale->amount`가 값으로 사용됩니다.

`sum` 같은 집계 메서드를 한 개 이상 호출하여 Pulse가 효율적인 조회를 위해 "버킷" 형태로 미리 집계된 값을 저장하도록 할 수 있습니다.

가능한 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]  
> 현재 인증된 사용자 ID를 캡처하는 카드 패키지를 만들 때는, 애플리케이션에서 개별 [사용자 해석 커스터마이징](#dashboard-resolving-users)을 존중하는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하세요.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회하기 (Retrieving Aggregate Data)

Pulse의 `Card` Livewire 컴포넌트를 확장할 때는 `aggregate` 메서드를 사용해 대시보드에서 보는 기간의 집계 데이터를 가져올 수 있습니다:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count']),
        ]);
    }
}
```

`aggregate` 메서드는 PHP `stdClass` 객체 컬렉션을 반환하며, 각 객체는 앞서 기록한 `key`와 요청한 집계된 각 값 키를 갖습니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 기본적으로 미리 집계된 버킷에서 데이터를 조회합니다. 따라서 `Pulse::record` 호출 시 집계 메서드가 미리 지정돼 있어야 합니다. 가장 오래된 버킷 데이터는 기간을 일부 벗어날 수 있는데, Pulse는 이 부분을 별도로 집계해 대시보드에 정확한 값을 제공합니다.

`aggregateTotal` 메서드를 사용하면 특정 타입의 총합만 가져올 수도 있습니다. 예를 들어 모든 사용자 매출의 합계를 구하는 방법:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시하기 (Displaying Users)

사용자 ID를 키로 기록한 집계 데이터를 사용할 때는 `Pulse::resolveUsers` 메서드를 활용해 사용자 레코드를 조회할 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar` 키가 포함된 객체를 반환하며, 이를 Pulse의 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더 (Custom Recorders)

패키지 작성자는 사용자가 데이터를 캡처하는 방식을 구성할 수 있게 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션 `config/pulse.php` 설정 파일의 `recorders` 항목에서 등록합니다:

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

레코더는 `$listen` 프로퍼티에 이벤트 클래스를 지정해 이벤트 리스너를 등록하며, 해당 이벤트가 발생할 때 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 수신할 이벤트 목록.
     *
     * @var list<class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 기록.
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