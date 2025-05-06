# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인증](#dashboard-authorization)
    - [커스터마이즈](#dashboard-customization)
    - [유저 해상](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용](#using-a-different-database)
    - [Redis 인제스트](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능 및 사용 내역을 한눈에 파악할 수 있도록 인사이트를 제공합니다. Pulse를 통해 느린 작업 및 엔드포인트와 같은 병목 현상을 추적하고, 가장 활발한 사용자를 찾아내는 등 다양한 정보를 확인할 수 있습니다.

개별 이벤트에 대한 심층 디버깅은 [Laravel Telescope](/docs/{{version}}/telescope)를 참고하세요.

<a name="installation"></a>
## 설치

> [!WARNING]
> Pulse의 공식 스토리지 구현은 현재 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다. 다른 DB 엔진을 사용할 경우 Pulse 데이터 저장을 위한 별도의 MySQL, MariaDB, PostgreSQL 데이터베이스가 필요합니다.

Composer 패키지 관리자를 통해 Pulse를 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령을 사용하여 Pulse 설정 파일과 마이그레이션 파일을 발행해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로 Pulse 데이터 저장에 필요한 테이블을 생성하려면 `migrate` 명령을 실행하세요:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션을 실행한 후에는 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 기본 애플리케이션 데이터베이스에 저장하지 않으려면, [전용 데이터베이스 연결 지정](#using-a-different-database)이 가능합니다.

<a name="configuration"></a>
### 설정

Pulse의 다양한 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하고, 새로운 레코더를 등록하거나 고급 옵션을 구성하려면, `config/pulse.php` 환경설정 파일을 발행할 수 있습니다:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드

<a name="dashboard-authorization"></a>
### 인증

Pulse 대시보드는 `/pulse` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드를 볼 수 있으므로, 프로덕션 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이즈하여 접근 권한을 설정해야 합니다. 이는 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 진행할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 부트스트랩 서비스.
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

Pulse 대시보드 카드와 레이아웃은 대시보드 뷰 파일을 발행하여 수정할 수 있습니다. 이 뷰는 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 발행됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/) 기반이며, 별도의 JavaScript 빌드 없이 카드나 레이아웃을 쉽게 커스터마이즈할 수 있습니다.

이 파일에서 `<x-pulse>` 컴포넌트는 대시보드 렌더링을 담당하며, 카드의 그리드 레이아웃을 제공합니다. 대시보드를 전체 화면 폭으로 표시하려면 `full-width` prop을 제공하면 됩니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12 컬럼 그리드를 생성하지만, `cols` prop 으로 수정 가능합니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 `cols` 및 `rows` prop을 받아 공간 및 위치를 제어합니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에는 카드 전체를 스크롤 없이 보여주는 `expand` prop도 사용할 수 있습니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 유저 해상

Application Usage 카드 등 사용자 정보를 표시하는 카드의 경우 Pulse는 오직 사용자 ID만 저장합니다. 대시보드 렌더링 시 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 해석해 Gravatar 웹 서비스를 이용해 아바타를 표시합니다.

사용자 필드 및 아바타 표시를 커스터마이즈하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 사용하세요.

`user` 메서드는 표시할 `Authenticatable` 모델을 입력받고 `name`, `extra`, `avatar` 정보를 담은 배열을 반환해야 합니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * 부트스트랩 서비스.
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
> 인증된 사용자 정보를 캡처하고 조회하는 방식을 완전히 커스터마이즈하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel [서비스 컨테이너](/docs/{{version}}/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령을 실행 중인 모든 서버의 시스템 리소스 사용량을 보여줍니다. 시스템 리소스 레포팅 관련 추가 정보는 [서버 레코더](#servers-recorder) 문서를 참고하세요.

인프라 내 서버를 교체한 경우, Pulse 대시보드에서 비활성 서버를 일정 기간 후에 숨기고 싶을 수 있습니다. 이때 `ignore-after` prop을 사용하면 비활성 서버를 대시보드에서 몇 초 후 제외할지 설정할 수 있습니다. 또는 `1 hour`, `3 days and 1 hour` 같은 상대적 시간 문자열도 사용할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내고, 작업을 디스패치하며, 느린 요청을 겪고 있는 상위 10명의 사용자를 보여줍니다.

모든 지표를 한 화면에 보고 싶다면 카드를 여러 번 포함하고 `type` 속성을 지정하면 됩니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 조회하고 표시하는 방식을 커스터마이즈하려면 [유저 해상](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션에서 요청 또는 작업이 많이 발생한다면, [샘플링](#sampling) 사용을 권장합니다. [사용자 요청 레코더](#user-requests-recorder), [사용자 작업 레코더](#user-jobs-recorder), [느린 작업 레코더](#slow-jobs-recorder) 문서도 참고하세요.

<a name="exceptions-card"></a>
#### 예외

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최근 발생 시점을 보여줍니다. 기본적으로 예외 클래스와 발생 지점별로 그룹화됩니다. 자세한 내용은 [예외 레코더](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리 현황(대기, 처리 중, 완료, 재시도, 실패 작업 수 포함)을 보여줍니다. 자세한 정보는 [큐 레코더](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청

`<livewire:pulse.slow-requests />` 카드는 기본적으로 1,000ms 이상의 요청을 기록합니다. 더 자세한 내용은 [느린 요청 레코더](#slow-requests-recorder) 문서를 확인하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업

`<livewire:pulse.slow-jobs />` 카드는 기본적으로 1,000ms 초과 작업을 표시합니다. 자세한 내용은 [느린 작업 레코더](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리

`<livewire:pulse.slow-queries />` 카드는 기본적으로 1,000ms 이상 소요된 데이터베이스 쿼리를 표시합니다.

기본적으로 쿼리는 SQL(바인딩 미포함)과 쿼리 위치로 그룹화되지만, SQL 기준만으로 그룹화할 수도 있습니다.

매우 큰 SQL 구문의 구문 강조로 인해 렌더링 성능에 문제가 있다면, `without-highlighting` prop으로 강조를 끌 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 정보는 [느린 쿼리 레코더](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel [HTTP 클라이언트](/docs/{{version}}/http-client)로 이루어진 1,000ms 초과 외부 요청을 보여줍니다.

기본적으로 전체 URL별로 그룹화되지만, 정규식을 사용해 유사한 요청을 그룹화할 수도 있습니다. 자세한 내용은 [느린 외부 요청 레코더](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시

`<livewire:pulse.cache />` 카드는 애플리케이션의 전체 및 개별 키별 캐시 적중/실패 통계를 보여줍니다.

기본적으로 키별로 그룹화되지만, 비슷한 키를 그룹화하는 정규식 옵션도 있습니다. 자세한 내용은 [캐시 인터랙션 레코더](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처

대부분의 Pulse 레코더는 Laravel에서 발생하는 프레임워크 이벤트를 기반으로 자동으로 엔트리를 캡처합니다. 하지만 [서버 레코더](#servers-recorder) 및 일부 서드파티 카드는 주기적으로 정보를 폴링해야 합니다. 이러한 카드를 사용하려면 모든 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 항상 백그라운드에서 실행하려면 Supervisor 등과 같은 프로세스 관리자를 사용해 명령이 중단되지 않도록 하길 권장합니다.

`pulse:check` 명령은 장시간 실행되는 프로세스이므로 코드베이스 변경을 인지하지 못합니다. 배포 과정에서 `pulse:restart` 명령으로 프로세스를 정상적으로 재시작하세요:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/{{version}}/cache)를 사용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 제대로 설정되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더

레코더는 애플리케이션에서 Pulse 데이터베이스에 저장할 엔트리를 캡처하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration) 내 `recorders` 섹션에서 등록하고 설정합니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 인터랙션

`CacheInteractions` 레코더는 [캐시](/docs/{{version}}/cache) 히트와 미스를 캡처해 [캐시](#cache-card) 카드에 표시합니다.

[샘플링 비율](#sampling) 및 무시할 키 패턴을 설정할 수 있습니다.

비슷한 캐시 키를 하나의 엔트리로 그룹화하고 싶을 때도 구성할 수 있습니다. 예를 들어, 동일 유형의 캐시 정보이지만 유일한 ID가 포함된 키 등. 그룹은 정규식을 사용해 키 일부를 치환합니다. 설정 예:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

첫 번째로 일치하는 패턴이 사용되고, 일치하는 패턴이 없으면 키 자체가 사용됩니다.

<a name="exceptions-recorder"></a>
#### 예외

`Exceptions` 레코더는 애플리케이션에서 발생하는 예외 정보를 캡처하고 [예외](#exceptions-card) 카드에 표시합니다.

[샘플링 비율](#sampling) 및 무시할 예외 패턴을 설정할 수 있습니다. 예외 발생 위치 저장 여부도 설정 가능합니다. 위치를 캡처하면 원인 추적에 도움이 되지만, 여러 위치에서 같은 예외가 발생하면 각 위치별로 여러 번 표시됩니다.

<a name="queues-recorder"></a>
#### 큐

`Queues` 레코더는 애플리케이션 큐 관련 정보를 캡처해 [큐](#queues-card) 카드에 표시합니다. [샘플링 비율](#sampling) 및 무시할 작업 패턴도 지정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업

`SlowJobs` 레코더는 애플리케이션에서 발생하는 느린 작업을 캡처해 [느린 작업](#slow-jobs-recorder) 카드에 표시합니다.

느린 작업 임계값, [샘플링 비율](#sampling), 무시할 작업 패턴을 설정할 수 있습니다.

특정 작업에 대해 더 큰 임계값이 필요하다면 작업별 임계값을 지정할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

작업 클래스명과 일치하는 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청

`SlowOutgoingRequests` 레코더는 Laravel [HTTP 클라이언트](/docs/{{version}}/http-client)로 이루어진, 임계값 초과 외부 HTTP 요청을 캡처해 [느린 외부 요청](#slow-outgoing-requests-card) 카드에 표시합니다.

느린 외부 요청 임계값, [샘플링 비율](#sampling), 무시할 URL 패턴을 설정할 수 있습니다.

특정 외부 요청에 대해 더 큰 임계값이 필요한 경우 요청별 임계값을 지정할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

URL과 일치하는 패턴이 없으면 `'default'` 값이 사용됩니다.

유사한 URL을 하나의 엔트리로 그룹화하고 싶을 때도 정규식을 사용할 수 있습니다. 예시:

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

일치하는 첫 번째 패턴이 사용되며, 없으면 URL 자체가 사용됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 레코더는 임계값 이상이 소요된 DB 쿼리를 캡처해 [느린 쿼리](#slow-queries-card) 카드에 표시합니다.

느린 쿼리 임계값, [샘플링 비율](#sampling), 무시할 쿼리 패턴, 쿼리 위치 캡처 여부도 설정할 수 있습니다. 위치를 캡처하면 원인 추적에 유용하나, 똑같은 쿼리가 다양한 위치에서 발생하면 각각 여러 번 표시됩니다.

특정 쿼리에 대해 더 긴 임계값을 지정하려면 다음과 같이 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

SQL과 일치하는 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 레코더는 애플리케이션에 발생한 요청 정보를 [느린 요청](#slow-requests-card), [애플리케이션 사용량](#application-usage-card) 카드에 표시합니다.

느린 라우트 임계값, [샘플링 비율](#sampling), 무시할 경로도 설정할 수 있습니다.

특정 요청에 대해 더 큰 임계값이 필요하다면 경로별 임계값을 지정할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

URL과 일치하는 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 레코더는 모든 모니터링 대상 서버의 CPU, 메모리, 스토리지 사용량을 캡처해 [서버](#servers-card) 카드에 표시합니다. 이 레코더는 [pulse:check 명령](#capturing-entries)을 각 서버에서 실행해야 합니다.

각 보고 서버는 고유 이름이 있어야 하며, 기본값은 PHP의 `gethostname` 값을 사용합니다. 직접 지정하려면 `PULSE_SERVER_NAME` 환경변수를 사용할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링할 디렉터리도 지정할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업

`UserJobs` 레코더는 애플리케이션에서 작업을 디스패치하는 사용자 정보를 캡처해 [애플리케이션 사용량](#application-usage-card) 카드에 표시합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴도 지정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청

`UserRequests` 레코더는 요청을 보내는 사용자 정보를 캡처해 [애플리케이션 사용량](#application-usage-card) 카드에 표시합니다.

[샘플링 비율](#sampling)과 무시할 URL 패턴도 지정할 수 있습니다.

<a name="filtering"></a>
### 필터링

많은 [레코더](#recorders)는 설정을 통해 값(예: 요청 URL)에 따라 특정 엔트리를 무시할 수 있습니다. 하지만, 인증된 사용자 등 다른 요인 기반으로 엔트리를 필터링하고 싶을 수도 있습니다. 이러한 경우 Pulse의 `filter` 메서드에 클로저를 전달해 필터링할 수 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot`에서 호출합니다:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * 부트스트랩 서비스.
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

Pulse는 추가적인 인프라 도입 없이 바로 기존 애플리케이션에 적용할 수 있도록 설계되었습니다. 단, 트래픽이 많은 환경에서는 Pulse로 인한 영향 최소화를 위해 여러 방법을 제공하고 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용

트래픽이 많은 환경에서는 Pulse를 위해 별도의 DB 연결을 사용하는 것을 권장합니다.

Pulse에서 사용할 [데이터베이스 연결](/docs/{{version}}/database#configuration)은 `PULSE_DB_CONNECTION` 환경변수로 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트

> [!WARNING]
> Redis 인제스트는 Redis 6.2 이상과 `phpredis` 또는 `predis`가 Redis 클라이언트 드라이버로 설정되어 있어야 합니다.

기본적으로 Pulse는 [구성된 데이터베이스 연결](#using-a-different-database)에 HTTP 응답 전송 또는 작업 처리 후 엔트리를 직접 저장합니다. 그러나 Pulse의 Redis 인제스트 드라이버를 이용하면 엔트리를 Redis 스트림으로 보낼 수 있습니다. 이를 사용하려면 `PULSE_INGEST_DRIVER` 환경 변수를 설정하면 됩니다:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본 [Redis 연결](/docs/{{version}}/redis#configuration)을 사용하지만, 필요시 `PULSE_REDIS_CONNECTION` 환경변수로 커스터마이즈할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

Redis 인제스트 사용 시, 엔트리를 모니터링해 Pulse DB로 이동하는 `pulse:work` 명령을 실행해야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 항상 백그라운드에서 실행하려면 Supervisor 등 프로세스 매니저를 활용하세요.

`pulse:work` 명령 또한 장시간 실행되므로 코드 변경사항 반영을 위해서는 배포 후 `pulse:restart` 명령으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/{{version}}/cache)를 통해 재시작 신호를 저장합니다.

<a name="sampling"></a>
### 샘플링

Pulse는 기본적으로 발생하는 모든 이벤트를 캡처합니다. 대규모 트래픽 환경에서는 수백만 건의 DB 행 집계가 발생할 수 있습니다.

따라서 일부 Pulse 데이터 레코더에 대한 "샘플링"을 활성화할 수 있습니다. 예를 들어, [사용자 요청](#user-requests-recorder) 레코더의 샘플 비율을 `0.1`로 설정하면 전체 요청의 10%만 저장합니다. 대시보드에는 값이 `~`로 시작해 근사치임을 나타냅니다.

특정 지표의 데이터가 많을수록 낮은 샘플 비율도 정확도를 크게 해치지 않습니다.

<a name="trimming"></a>
### 트리밍

Pulse는 대시보드에서 벗어난 기간의 데이터를 자동으로 삭제합니다. 트리밍은 로터리(lottery) 시스템으로 데이터가 인제스트될 때 진행되며, Pulse [설정 파일](#configuration)에서 커스터마이즈할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리

Pulse 데이터 캡처 중(예: 스토리지 DB 연결 실패) 예외가 발생할 경우, Pulse는 애플리케이션 동작에 영향을 주지 않도록 조용히 실패합니다.

이 예외 처리 방식을 커스터마이즈하려면 `handleExceptionsUsing` 메서드에 클로저를 지정할 수 있습니다:

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

Pulse는 애플리케이션 상황에 맞는 데이터를 표시하기 위해 커스텀 카드를 제작할 수 있습니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드 제작 전 [관련 문서](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트

Laravel Pulse에서 커스텀 카드를 생성하려면 기본 `Card` Livewire 컴포넌트를 확장하고, 대응되는 뷰를 정의합니다:

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

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy)을 사용할 경우, `Card` 컴포넌트는 자동으로 `cols` 및 `rows` 속성을 반영한 플레이스홀더를 제공합니다.

카드의 뷰 작성 시, Pulse의 Blade 컴포넌트를 활용해 일관된 UI와 UX를 보장할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각 Blade 컴포넌트에 전달되어 대시보드에서 레이아웃 커스터마이즈가 가능합니다. 자동 갱신이 필요하다면 `wire:poll.5s=""` 속성을 추가하세요.

Livewire 컴포넌트와 템플릿을 정의한 후에는 [대시보드 뷰](#dashboard-customization)에 카드를 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 패키지 내부 카드를 사용할 경우, `Livewire::component` 메서드로 컴포넌트 등록이 필요합니다.

<a name="custom-card-styling"></a>
### 스타일링

Pulse에서 제공하는 클래스 및 컴포넌트 외에 별도의 스타일이 필요한 경우, 몇 가지 방법으로 커스텀 CSS를 포함할 수 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 연동

커스텀 카드가 애플리케이션 코드에 포함되어 있고, Laravel의 [Vite 통합](/docs/{{version}}/vite)을 사용 중이라면, `vite.config.js`에 별도 CSS 엔트리포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

이후 [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 지시자를 사용해 CSS 엔트리포인트를 지정합니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

패키지 등 별도 환경에서는 Livewire 컴포넌트에 `css` 메서드를 정의해 CSS 파일 경로를 반환하도록 Pulse에 추가 스타일시트를 로딩하도록 할 수 있습니다:

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

이 카드를 대시보드에 포함하면, Pulse가 파일 내용을 `<style>` 태그로 자동 삽입합니다(따라서 public 디렉터리에 파일을 별도 배포할 필요 없음).

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS 사용 시, 불필요한 CSS가 로드되지 않도록 별도 Tailwind 설정 파일을 생성하는 것이 좋습니다:

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

그리고 CSS 엔트리포인트에서 다음과 같이 설정 파일을 지정합니다:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Tailwind의 [Important 선택자 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에 지정한 셀렉터와 일치하도록 카드 뷰에 `id`나 `class`를 추가하세요:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계

커스텀 카드는 어디에서든 데이터를 가져와 표시할 수 있지만, Pulse의 고성능 데이터 기록/집계 시스템을 활용하는 것이 좋습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처

Pulse는 `Pulse::record` 메서드로 "엔트리" 기록을 지원합니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

첫 번째 인자는 기록 타입, 두 번째 인자는 집계 그룹을 결정하는 키, 대부분의 집계 메서드는 집계할 `value`도 필요합니다. 위 예시에서는 `$sale->amount`가 집계 값입니다. 이후 `sum`, `count` 등 집계 메서드를 연쇄 호출해 미리 집계된 데이터를 효율적으로 저장합니다.

사용 가능한 집계 메서드:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 인증된 사용자 ID를 키로 저장하는 카드 패키지를 만들 경우, 사용자 해상 커스터마이즈를 반영하는 `Pulse::resolveAuthenticatedUserId()`를 사용하세요.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회

Pulse의 `Card` Livewire 컴포넌트에서는 대시보드에서 조회 중인 기간의 집계 데이터를 `aggregate` 메서드로 얻을 수 있습니다:

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

`aggregate`는 PHP `stdClass` 객체의 컬렉션을 반환하며, 각 객체에는 집계 시 캡처한 `key`와, 지정한 집계 필드가 포함됩니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 원칙적으로 사전 집계된 데이터를 사용하므로, `Pulse::record`에서 해당 집계 정보를 미리 기록해야 합니다. 가장 오래된 버킷은 일부만 기간 내에 포함될 수 있으므로, Pulse가 부족한 구간을 합산해 전체 기간의 정확한 값을 제공합니다.

특정 타입의 전체합 등 단일 값 조회는 `aggregateTotal` 메서드를 사용하세요. 예시:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시

키에 사용자 ID를 기록하는 집계 데이터와 함께 사용할 때, `Pulse::resolveUsers` 메서드로 사용자 레코드를 조회할 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar`가 포함된 객체를 반환하며, 이를 `<x-pulse::user-card>` Blade 컴포넌트에 바로 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더

패키지 저자는 사용자가 데이터 캡처 방식을 설정할 수 있도록 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션 `config/pulse.php`의 `recorders` 섹션에 등록됩니다:

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

레코더는 `$listen` 프로퍼티로 이벤트를 지정할 수 있고, Pulse가 자동으로 리스너 등록 및 `record` 메서드 호출을 처리합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 리스닝할 이벤트 목록.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 정보 기록.
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