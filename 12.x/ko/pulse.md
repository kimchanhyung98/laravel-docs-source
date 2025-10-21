# Laravel Pulse (Laravel Pulse)

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [맞춤화](#dashboard-customization)
    - [사용자 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처](#capturing-entries)
    - [기록기](#recorders)
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

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있는 인사이트를 제공합니다. Pulse를 활용하면 느린 작업이나 엔드포인트와 같은 병목 현상을 추적하고, 가장 활발한 사용자를 파악하는 등 다양한 정보를 얻을 수 있습니다.

개별 이벤트의 심층 디버깅이 필요하다면 [Laravel Telescope](/docs/12.x/telescope) 사용을 권장합니다.

<a name="installation"></a>
## 설치

> [!WARNING]
> Pulse의 공식 스토리지 구현은 현재 MySQL, MariaDB 또는 PostgreSQL 데이터베이스만 지원합니다. 다른 데이터베이스 엔진을 사용 중이라면, Pulse 데이터를 위한 별도의 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다.

Pulse는 Composer 패키지 매니저를 사용해 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

그 다음, `vendor:publish` Artisan 명령어를 통해 Pulse 설정 및 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터 저장에 필요한 테이블 생성을 위해 `migrate` 명령어를 실행합니다:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로를 통해 Pulse 대시보드에 접속할 수 있습니다.

> [!NOTE]
> 애플리케이션의 기본 데이터베이스에 Pulse 데이터를 저장하고 싶지 않다면, [별도의 전용 데이터베이스 연결](#using-a-different-database)을 지정할 수 있습니다.

<a name="configuration"></a>
### 구성

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새 기록기를 등록하거나, 고급 옵션을 구성하려면 `config/pulse.php` 설정 파일을 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드

<a name="dashboard-authorization"></a>
### 인가

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근할 수 있으므로, 프로덕션 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이즈해 인가를 구성해야 합니다. 이는 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 다음과 같이 설정할 수 있습니다:

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
### 맞춤화

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰를 퍼블리시하여 수정할 수 있습니다. 해당 뷰 파일은 `resources/views/vendor/pulse/dashboard.blade.php`에 퍼블리시됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 구동되며, 자바스크립트 자산을 다시 빌드하지 않고도 카드나 레이아웃을 자유롭게 커스터마이즈할 수 있습니다.

이 파일 내에서 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며, 카드용 그리드 레이아웃을 제공합니다. 대시보드가 화면 전체 너비를 차지하도록 하려면 컴포넌트에 `full-width` 속성을 추가할 수 있습니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12컬럼 그리드를 생성하지만, `cols` 속성을 통해 자유롭게 조정할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드에는 공간과 위치를 제어하는 `cols` 및 `rows` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에서는 스크롤 대신 카드를 전체 펼쳐서 볼 수 있도록 `expand` 속성도 사용할 수 있습니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 해석

예를 들어 Application Usage 카드처럼 사용자 정보를 표시하는 카드의 경우, Pulse는 사용자의 ID만 기록합니다. 대시보드 렌더링 시 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 가져오고, Gravatar 웹 서비스를 사용해 아바타를 표시합니다.

필드와 아바타 정보를 커스터마이즈하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 안에서 `Pulse::user` 메서드를 호출하면 됩니다.

`user` 메서드는 표시할 `Authenticatable` 모델을 받아 `name`, `extra`, `avatar` 정보를 포함하는 배열을 반환해야 합니다:

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
> 인증된 사용자를 어떻게 캡처하고 조회할지 완전히 커스터마이즈하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel의 [서비스 컨테이너](/docs/12.x/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 보여줍니다. 시스템 리소스 정보 리포팅에 대한 자세한 내용은 [서버 기록기](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체하는 경우, 주어진 시간이 지난 후에는 Pulse 대시보드에서 활동 중단된 서버의 표시를 중단하고 싶을 수 있습니다. 이 경우 `ignore-after` 속성에 초 단위 값이나, `1 hour`, `3 days and 1 hour`와 같은 상대 시간 포맷 문자열을 지정할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나, 작업을 디스패치하거나, 느린 요청을 경험한 상위 10명의 사용자를 표시합니다.

화면상에서 모든 사용량 메트릭을 동시에 보고 싶다면, 카드를 여러 번 포함하고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 가져오는 방식이나 표시 방식을 커스터마이즈하는 방법은 [사용자 해석](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 많은 요청이나 작업이 발생하는 애플리케이션이라면, [샘플링](#sampling) 기능 활성화를 고려해 볼 수 있습니다. 자세한 내용은 [User Requests 기록기](#user-requests-recorder), [User Jobs 기록기](#user-jobs-recorder), [Slow Jobs 기록기](#slow-jobs-recorder) 문서를 참조하세요.

<a name="exceptions-card"></a>
#### 예외

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생하는 예외의 빈도와 최근 시점을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치별로 그룹화됩니다. 상세 내용은 [Exceptions 기록기](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리량을 보여줍니다(대기, 처리 중, 처리 완료, 재시도, 실패 작업 수 등). 자세한 내용은 [Queues 기록기](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청

`<livewire:pulse.slow-requests />` 카드는 기본값(1,000ms) 초과 요청을 표시합니다. 상세 내용은 [Slow Requests 기록기](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업

`<livewire:pulse.slow-jobs />` 카드는 기본값(1,000ms) 초과 큐 작업을 보여줍니다. 자세한 내용은 [Slow Jobs 기록기](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리

`<livewire:pulse.slow-queries />` 카드는 기본값(1,000ms) 초과 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL(바인딩 제외)과 발생 위치별로 그룹화됩니다. 만약 위치를 캡처하지 않고 쿼리만으로 그룹화하기 원한다면, 해당 옵션을 조정할 수 있습니다.

아주 큰 SQL 쿼리가 구문 하이라이트 처리되어 렌더링 속도 문제를 겪는다면, `without-highlighting` 속성으로 하이라이트를 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [Slow Queries 기록기](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)로 생성된 외부 요청 중 설정된 임계치(기본 1,000ms)를 초과하는 요청을 보여줍니다.

기본적으로 전체 URL 기준으로 그룹화됩니다. 그러나 필요에 따라 정규 표현식을 활용해 유사한 외부 요청을 정규화하거나 그룹화할 수도 있습니다. 자세한 사항은 [Slow Outgoing Requests 기록기](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시

`<livewire:pulse.cache />` 카드는 애플리케이션의 전체 및 개별 키별 캐시 적중/미적중 통계를 보여줍니다.

기본 설정은 키별로 그룹화되지만, 필요에 따라 정규 표현식으로 유사한 키를 그룹화할 수 있습니다. 자세한 사항은 [Cache Interactions 기록기](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처

대부분의 Pulse 기록기는 Laravel에서 발생하는 프레임워크 이벤트를 바탕으로 자동으로 엔트리를 캡처합니다. 하지만 [서버 기록기](#servers-recorder)나 일부 써드파티 카드는 주기적으로 정보를 폴링해야 합니다. 이런 카드들을 사용하려면, 각각의 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor와 같은 프로세스 모니터를 활용해 명령어가 멈추지 않도록 해야 합니다.

`pulse:check` 명령은 장시간 실행되는 프로세스이기 때문에, 코드베이스 변경사항 감지가 불가능합니다. 배포 시에는 `pulse:restart` 명령을 호출해 안전하게 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호를 저장하므로, 해당 기능을 사용하기 전에 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인하세요.

<a name="recorders"></a>
### 기록기

기록기는 애플리케이션에서 발생한 엔트리를 Pulse 데이터베이스에 기록하는 역할을 담당합니다. 기록기는 [Pulse 설정 파일](#configuration)의 `recorders` 섹션에서 등록 및 구성됩니다.

<a name="cache-interactions-recorder"></a>
#### Cache Interactions

`CacheInteractions` 기록기는 애플리케이션에서 발생하는 [캐시](/docs/12.x/cache) 적중/미적중 정보를 [캐시](#cache-card) 카드에 표시하기 위해 캡처합니다.

옵션으로 [샘플링 비율](#sampling)과 무시할 키 패턴을 조정할 수 있습니다.

또한 유사한 키를 하나의 엔트리로 그룹화하도록 키 그룹핑을 구성할 수 있습니다. 예를 들어, 동일한 유형의 정보를 캐싱하더라도 고유 ID가 붙은 키를 표준화하고 싶을 때 사용할 수 있습니다. 그룹은 정규 표현식을 사용한 "찾아바꾸기" 방식으로 구성하며, 설정 예시는 아래와 같습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

처음 일치하는 패턴이 사용되며, 어느 패턴과도 일치하지 않으면 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외

`Exceptions` 기록기는 애플리케이션에서 보고 가능한 예외 정보를 [예외](#exceptions-card) 카드에 표시하기 위해 캡처합니다.

[샘플링 비율](#sampling)과 무시할 예외 패턴을 옵션으로 조정할 수 있습니다. 또한 예외가 발생한 위치를 캡처할지 여부도 설정 가능합니다. 캡처된 위치 정보는 Pulse 대시보드에 표시되어 예외 원인을 추적하는 데 도움이 되지만, 동일한 예외가 여러 위치에서 발생한다면 각각의 위치별로 별도 표시됩니다.

<a name="queues-recorder"></a>
#### 큐

`Queues` 기록기는 애플리케이션 큐에 관한 정보를 [큐](#queues-card) 카드에 표시하기 위해 캡처합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴을 옵션으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업

`SlowJobs` 기록기는 애플리케이션에서 발생하는 느린 작업 정보를 [느린 작업](#slow-jobs-recorder) 카드에 표시하기 위해 캡처합니다.

느린 작업 임계치, [샘플링 비율](#sampling), 무시할 작업 패턴을 옵션으로 조정할 수 있습니다.

특정 작업이 다른 작업에 비해 오래 걸리는 것이 예측되는 경우, 작업 유형별로 임계치를 구성할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

정규 표현식과 일치하지 않을 경우, `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청

`SlowOutgoingRequests` 기록기는 Laravel [HTTP 클라이언트](/docs/12.x/http-client)로 발생한 외부 HTTP 요청 중 임계치를 초과한 정보를 [느린 외부 요청](#slow-outgoing-requests-card) 카드에 표시하기 위해 캡처합니다.

느린 외부 요청 임계치, [샘플링 비율](#sampling), 무시할 URL 패턴을 옵션으로 구성할 수 있습니다.

특정 외부 요청의 처리 시간이 길게 걸리는 것이 정상이라면, 요청별로 임계치를 지정할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규 표현식과 일치하지 않으면 `'default'` 임계치가 적용됩니다.

URL 그룹핑도 가능해, 유사 URL을 하나의 엔트리로 그룹화할 수 있습니다. 예를 들어, URL 경로에서 고유 ID를 제거하거나, 도메인 단위로 그룹화할 때 사용할 수 있습니다. 일부 예시는 설정 파일에 포함되어 있습니다:

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

가장 먼저 일치하는 패턴이 사용되며, 일치하는 것이 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 기록기는 애플리케이션에서 임계치 초과 SQL 쿼리를 [느린 쿼리](#slow-queries-card) 카드에 표시하기 위해 캡처합니다.

느린 쿼리 임계치, [샘플링 비율](#sampling), 무시할 쿼리 패턴을 구성할 수 있습니다. 또한 쿼리 위치 캡처 여부도 선택 가능합니다. 쿼리 위치 정보를 대시보드에 표시하여 원인 추적에 활용할 수 있지만, 동일 쿼리가 여러 위치에서 실행되면 각각 별도로 나타납니다.

특정 쿼리별로 임계치를 다르게 지정할 수도 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

정규식을 통해 쿼리 SQL과 매칭되지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 기록기는 애플리케이션에 들어오는 요청 정보를 [느린 요청](#slow-requests-card) 및 [애플리케이션 사용량](#application-usage-card) 카드에 표시할 수 있도록 캡처합니다.

느린 라우트 임계치, [샘플링 비율](#sampling), 무시할 경로 설정이 가능합니다.

특정 요청의 지연이 정상적인 경우, 개별 요청별 임계치 설정이 가능합니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규식과 매칭되지 않는 URL은 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 기록기는 애플리케이션을 구동 중인 서버의 CPU, 메모리, 스토리지 사용량을 [서버](#servers-card) 카드에 표시하기 위해 캡처합니다. 이 기록기를 사용하려면 [pulse:check 명령어](#capturing-entries)가 각 서버에서 실행 중이어야 합니다.

각 서버는 고유한 이름이 필요합니다. 기본적으로 Pulse는 PHP `gethostname` 함수의 반환값을 사용하지만, `PULSE_SERVER_NAME` 환경 변수로 이름을 지정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링 디렉터리도 커스터마이즈할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업

`UserJobs` 기록기는 애플리케이션에서 작업을 디스패치하는 사용자 정보를 [애플리케이션 사용량](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

[샘플링 비율](#sampling), 무시할 작업 패턴 조정이 가능합니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청

`UserRequests` 기록기는 애플리케이션에 요청을 보내는 사용자 정보를 [애플리케이션 사용량](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

[샘플링 비율](#sampling), 무시할 URL 패턴 조정이 가능합니다.

<a name="filtering"></a>
### 필터링

지금까지 살펴본 바와 같이, 많은 [기록기들](#recorders)은 구성 옵션을 통해 요청 URL 등 특정 값에 따라 엔트리를 무시(필터)할 수 있습니다. 그러나 때로는 현재 인증된 사용자 등 다른 조건에 따라 엔트리를 걸러내고 싶을 때도 있습니다. Pulse의 `filter` 메서드에 클로저를 전달하여 엔트리 필터링이 가능합니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

Pulse는 별도의 인프라 없이 기존 애플리케이션에 바로 추가할 수 있도록 설계되었습니다. 하지만 트래픽이 많은 애플리케이션에서는 Pulse가 애플리케이션 성능에 미치는 영향을 낮추는 여러 방식을 제공하고 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용

트래픽이 많은 애플리케이션의 경우, Pulse만을 위한 별도의 데이터베이스 연결을 사용해 애플리케이션 데이터베이스에 미치는 영향을 최소화할 수 있습니다.

Pulse가 사용할 [데이터베이스 연결](/docs/12.x/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수로 설정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트

> [!WARNING]
> Redis 인제스트 기능을 사용하려면 Redis 6.2 이상과, 애플리케이션에 `phpredis` 또는 `predis` 드라이버가 설정되어 있어야 합니다.

기본적으로 Pulse는 HTTP 응답 전송 또는 작업 처리 후, [설정된 데이터베이스 연결](#using-a-different-database)에 엔트리를 바로 저장합니다. 그러나 Pulse의 Redis 인제스트 드라이버를 사용하면, 엔트리를 Redis 스트림으로 전송할 수 있습니다. 이를 사용하려면 `PULSE_INGEST_DRIVER` 환경 변수를 다음과 같이 설정합니다:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 [기본 Redis 연결](/docs/12.x/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 커스터마이즈할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis 인제스트 드라이버를 사용하는 경우, 가능하다면 Redis 기반 큐에서 사용하는 Redis 연결과 Pulse가 사용하는 연결을 구분해야 합니다.

Redis 인제스트를 사용할 때는, `pulse:work` 명령을 실행해 스트림을 모니터링하고 Redis에서 Pulse 데이터베이스 테이블로 엔트리를 옮겨야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor 등으로 관리하세요.

`pulse:work` 명령은 장시간 실행되는 프로세스이므로, 코드 변경사항을 인식하려면 명령을 재시작해야 합니다. 애플리케이션 배포 시에는 `pulse:restart` 명령을 호출해 안전하게 재시작하세요:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 이용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 캐시 드라이버가 올바르게 구성되어 있는지 확인하세요.

<a name="sampling"></a>
### 샘플링

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 캡처합니다. 대규모 트래픽이 유입되는 환경에서는, 특히 긴 기간 대시보드를 볼 때 수백만 개의 행이 집계되어야 하므로 부담이 될 수 있습니다.

이러한 경우, 특정 Pulse 데이터 기록기에서 "샘플링"을 활성화할 수 있습니다. 예를 들어 [User Requests 기록기](#user-requests-recorder)에서 샘플 비율을 `0.1`로 두면, 전체 요청의 약 10%만 기록하고, 대시보드에서는 `~` 기호를 접두사로 붙여 대략적인 값임을 표시합니다.

일반적으로, 특정 메트릭의 엔트리가 많을수록 샘플률을 더 낮춰도 정확도 저하가 크지 않습니다.

<a name="trimming"></a>
### 트리밍

Pulse는 대시보드에 표시되는 기간 밖의 엔트리는 자동으로 삭제(트리밍)합니다. 트리밍은 로터리(lottery) 시스템으로 데이터 인제스트 시 수행되며, Pulse [설정 파일](#configuration)에서 커스터마이즈할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리

Pulse 데이터 캡처 중 스토리지 데이터베이스 연결 실패 등의 예외가 발생할 경우, Pulse는 애플리케이션 동작에 영향을 주지 않도록 예외를 조용히 무시합니다.

이런 예외 처리 방식을 커스터마이즈하려면, `handleExceptionsUsing` 메서드로 클로저를 지정하면 됩니다:

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

Pulse는 애플리케이션 특화 데이터를 표시하는 커스텀 카드를 직접 만들 수 있도록 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드 제작 전 [해당 공식 문서](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트

Laravel Pulse에서 커스텀 카드를 만들려면, 기본 `Card` Livewire 컴포넌트를 상속하고 대응되는 뷰를 정의하는 것부터 시작합니다:

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

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 활용할 경우, `Card` 컴포넌트가 자동으로 `cols`, `rows` 속성을 반영하는 플레이스홀더를 제공합니다.

카드 뷰를 작성할 때 Pulse의 Blade 컴포넌트를 활용하면 일관된 UI를 손쉽게 만들 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각의 Blade 컴포넌트에 전달되어 카드 레이아웃을 대시보드 뷰에서 자유롭게 커스터마이즈할 수 있게 합니다. `wire:poll.5s=""` 속성을 추가하면 카드를 5초마다 자동으로 업데이트하도록 할 수 있습니다.

Livewire 컴포넌트와 템플릿을 정의한 후에는 [대시보드 뷰](#dashboard-customization)에 카드를 추가하면 됩니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 카드가 패키지 형태로 제공된다면, Livewire의 `Livewire::component` 메서드를 사용해 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링

카드가 Pulse 기본 제공 클래스와 컴포넌트만으로 충분하지 않아 추가 스타일링이 필요하다면, 몇 가지 방법으로 커스텀 CSS를 적용할 수 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

커스텀 카드가 애플리케이션 코드베이스 내에 있고, Laravel의 [Vite 통합](/docs/12.x/vite)을 사용 중이라면, `vite.config.js` 파일에 해당 카드 전용 CSS 엔트리포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

이후 [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 디렉티브를 사용해 카드용 CSS 엔트리포인트를 지정합니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일 직접 로드

Pulse 카드가 패키지에 포함되어 있는 등 다른 상황이라면, Livewire 컴포넌트에 `css` 메서드를 정의해 추가 CSS 파일 경로를 반환하도록 할 수 있습니다:

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

이 카드가 대시보드에 포함되면, Pulse는 해당 파일 내용을 `<style>` 태그로 삽입하므로, `public` 디렉터리에 별도 퍼블리시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS 사용 시에는, 불필요한 CSS 로딩과 Pulse의 Tailwind 클래스 충돌을 방지하기 위해 별도의 Tailwind 설정 파일을 만드는 것이 좋습니다:

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

CSS 엔트리포인트에서도 해당 설정 파일을 명시합니다:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Tailwind의 [important selector 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에 맞는 `id` 혹은 `class`를 카드의 뷰에서 지정해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계

커스텀 카드는 원하는 곳 어디에서든 데이터를 가져와 표시할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용하는 것이 좋습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 기록

Pulse는 `Pulse::record` 메서드를 통해 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 기록할 항목의 `type`, 두 번째 인자는 집계 데이터의 그룹화를 좌우하는 `key`입니다. 대부분의 집계 방식에서는 집계 대상이 될 `value`도 지정해야 합니다(위 예제에서는 `$sale->amount`). 그 다음, 한 개 이상의 집계 메서드(예: `sum`)를 체이닝 방식으로 호출해, Pulse가 빠른 데이터 조회를 위해 미리 집계된 값을 "버킷"에 저장하게 할 수 있습니다.

사용 가능한 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 기록하는 카드 패키지를 만들 때는, 애플리케이션의 [사용자 해석](#dashboard-resolving-users) 커스터마이징을 존중하는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하는 것이 좋습니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회

Pulse의 `Card` Livewire 컴포넌트를 상속할 때는, 대시보드 상의 조회 기간에 맞춰 집계 데이터를 `aggregate` 메서드로 쉽게 조회할 수 있습니다:

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

`aggregate` 메서드는 PHP `stdClass` 객체 컬렉션을 반환합니다. 각 객체에는 앞서 캡처된 `key` 속성 및 요청한 집계별 키가 포함됩니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 미리 집계된 버킷에서 데이터를 주로 조회하므로, 집계 메서드는 반드시 `Pulse::record` 호출 시 미리 지정되어야 합니다. 가장 오래된 버킷은 해당 기간과 일부만 겹칠 수 있으므로, Pulse가 그 부분에 대해 신규 집계를 수행해 전체 기간에 대한 정확한 값을 제공합니다.

전체 항목에 대한 총합이 필요할 때는 `aggregateTotal` 메서드를 쓸 수 있습니다. 예를 들어, 아래 메서드는 사용자별 그룹핑 없이 전체 판매 합계를 조회합니다:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 정보 표시

key로 사용자 ID를 기록한 집계 데이터라면, `Pulse::resolveUsers` 메서드로 해당 ID를 사용자 레코드로 쉽게 해석할 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar` 키가 담긴 객체를 반환하므로, 이를 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달할 수도 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 기록기

패키지 제작자는 사용자들이 직접 데이터 캡처 방식을 설정할 수 있도록 기록기 클래스를 제공할 수 있습니다.

기록기는 애플리케이션의 `config/pulse.php` 설정 파일 `recorders` 섹션에 등록됩니다:

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

기록기는 `$listen` 속성에 이벤트를 지정해 이벤트 기반 데이터 캡처가 가능합니다. Pulse는 자동으로 리스너를 등록하고 기록기의 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 리스닝할 이벤트 목록
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 이벤트 기록
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
