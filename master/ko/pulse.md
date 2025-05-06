# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이즈](#dashboard-customization)
    - [사용자 확인](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 수집](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용](#using-a-different-database)
    - [Redis 인제스트](#ingest)
    - [샘플링](#sampling)
    - [트리밍(데이터 정리)](#trimming)
    - [Pulse 예외 핸들링](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있는 인사이트를 제공합니다. Pulse를 사용하면 느린 작업이나 엔드포인트와 같은 병목 현상을 추적하고, 가장 활동적인 사용자를 찾는 등 다양한 기능을 활용할 수 있습니다.

개별 이벤트의 심층 디버깅이 필요하다면 [Laravel Telescope](/docs/{{version}}/telescope)를 참고하세요.

<a name="installation"></a>
## 설치

> [!WARNING]
> Pulse의 1차 스토리지 구현은 현재 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다. 다른 데이터베이스 엔진을 사용하는 경우 Pulse 데이터를 위한 별도의 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다.

Composer 패키지 매니저를 사용하여 Pulse를 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 Pulse 설정과 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse의 데이터 저장에 필요한 테이블을 생성하기 위해 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan migrate
```

Pulse의 데이터베이스 마이그레이션을 완료한 후 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 기본 애플리케이션 데이터베이스에 저장하고 싶지 않은 경우, [별도의 데이터베이스 연결을 지정](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
### 설정

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새 레코더를 등록하거나, 고급 옵션을 설정하려면 `config/pulse.php` 설정 파일을 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드

<a name="dashboard-authorization"></a>
### 인가

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로, 이 대시보드는 `local` 환경에서만 접근 가능하므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 맞춤화하여 접근 권한을 설정해야 합니다. 이는 `app/Providers/AppServiceProvider.php` 파일에서 설정할 수 있습니다:

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

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰를 퍼블리시하여 설정할 수 있습니다. 퍼블리시된 대시보드 뷰는 `resources/views/vendor/pulse/dashboard.blade.php`에 위치합니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

이 대시보드는 [Livewire](https://livewire.laravel.com/)로 구현되어 있어, JavaScript 자산을 별도로 빌드하지 않고도 카드와 레이아웃을 자유롭게 커스터마이즈할 수 있습니다.

이 파일 내에서, `<x-pulse>` 컴포넌트가 대시보드를 렌더링하며 카드들의 그리드 레이아웃을 제공합니다. 대시보드의 너비를 전체 화면으로 확장하고 싶다면, `full-width` 프로퍼티를 컴포넌트에 전달하세요:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12 컬럼 그리드를 생성하지만, `cols` 프로퍼티로 컬럼수를 조정할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 공간과 위치를 제어하는 `cols` 및 `rows` 프로퍼티를 가집니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에서는 스크롤 대신 카드를 전체로 펼쳐서 보여주는 `expand` 프로퍼티도 지원합니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 확인

Application Usage 카드 등 사용자 정보를 표시하는 카드의 경우, Pulse는 기본적으로 사용자의 ID만 기록합니다. 대시보드 렌더링 시, Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드 값을 조회하고 Gravatar 서비스를 통해 아바타를 표시합니다.

필드와 아바타를 커스터마이즈하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내에서 `Pulse::user` 메서드를 사용할 수 있습니다.

`user` 메서드는 표시할 `Authenticatable` 모델을 인자로 받아, 사용자에 대한 `name`, `extra`, `avatar` 정보를 포함하는 배열을 반환해야 합니다:

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
> 인증된 사용자를 캡처하고 조회하는 방식을 완전히 커스터마이즈하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 인터페이스를 구현하여 Laravel의 [서비스 컨테이너](/docs/{{version}}/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령을 실행 중인 모든 서버의 시스템 리소스 사용 현황을 보여줍니다. 시스템 리소스 정보에 대한 자세한 내용은 [서버 레코더](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체할 경우, Pulse 대시보드에서 일정 기간 후 비활성 서버를 표시하지 않도록 할 수 있습니다. `ignore-after` 프로퍼티를 사용하여, 비활성 서버가 대시보드에서 제거될 시간을 초 단위 또는 `1 hour`, `3 days and 1 hour` 형식의 문자열로 지정할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나, 잡(Jobs)을 디스패치하고, 느린 요청을 겪는 상위 10명의 사용자 정보를 표시합니다.

모든 사용 지표를 한 번에 화면에 표시하려면, 카드를 여러 번 추가하고 `type` 속성을 지정하세요:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 조회 및 표시하는 방법을 커스터마이즈하는 법은 [사용자 확인](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션이 많은 요청을 받거나 잡(Jobs)을 많이 디스패치하는 경우, [샘플링](#sampling) 활성화를 고려할 수 있습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최근 발생 정보를 보여줍니다. 기본적으로 예외는 예외 클래스 및 발생 위치를 기준으로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐

`<livewire:pulse.queues />` 카드는 애플리케이션 큐의 처리량(대기 중, 처리 중, 완료, 릴리즈, 실패)을 보여줍니다. 더 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청

`<livewire:pulse.slow-requests />` 카드는 기본값 1,000ms를 초과하는 애플리케이션의 들어오는 요청을 표시합니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder)를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 잡

`<livewire:pulse.slow-jobs />` 카드는 기본값 1,000ms를 초과하는 대기잡(queued job)을 보여줍니다. 더 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리

`<livewire:pulse.slow-queries />` 카드는 기본값 1,000ms를 초과하는 데이터베이스 쿼리를 표시합니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외) 및 실행 위치별로 그룹화됩니다. 만약, 오로지 쿼리 기준으로만 그룹화하고 싶다면 위치 캡처를 비활성화할 수 있습니다.

쿼리 구문 하이라이팅(Green)으로 인해 렌더링 성능 문제가 있을 경우, `without-highlighting` 프로퍼티를 통해 하이라이팅을 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/{{version}}/http-client)로 전송된, 기본값 1,000ms를 초과한 외부 요청을 표시합니다.

기본적으로 전체 URL 기준으로 그룹화하지만, 정규식을 사용해 유사한 외부 요청을 그룹화하거나 정규화할 수 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시

`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 적중/미스 통계를 전역 및 개별 키별로 보여줍니다.

기본적으로 키별로 그룹화하지만, 정규식을 사용해 유사한 키를 그룹화할 수 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 수집

대부분의 Pulse 레코더는 Laravel의 프레임워크 이벤트에 의해 자동으로 엔트리를 수집합니다. 그러나 [서버 레코더](#servers-recorder)나 일부 서드파티 카드는 정보를 정기적으로 폴링해야 하므로, 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor와 같은 프로세스 모니터를 사용하여 명령어가 중단되지 않도록 해야 합니다.

`pulse:check` 명령은 장기 실행 프로세스이므로, 코드베이스 변경 사항을 감지하지 못합니다. 배포 시 `pulse:restart` 명령어를 호출하여 프로세스를 안전하게 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/{{version}}/cache)를 재시작 신호 저장소로 사용하므로, 이 기능을 사용하기 전 애플리케이션에 적절한 캐시 드라이버가 구성되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더

레코더는 애플리케이션에서 Pulse 데이터베이스에 저장할 엔트리를 수집하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration)의 `recorders` 항목에 등록 및 설정할 수 있습니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [캐시](/docs/{{version}}/cache) 적중/미스 정보를 [캐시 카드](#cache-card)에 표시하기 위해 수집합니다.

[샘플 레이트](#sampling)나 무시할 키 패턴 등도 선택적으로 조정할 수 있습니다.

유사한 키를 묶어서 그룹화할 수도 있습니다. 예를 들어, 동일한 유형의 정보를 캐싱하는 키에서 고유 ID를 제거하려는 경우, 정규 표현식을 활용해 키의 일부를 치환할 수 있습니다. 설정 예시는 아래와 같습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

가장 먼저 매칭되는 패턴이 사용되며, 매칭되는 패턴이 없다면 그대로 키를 저장합니다.

<a name="exceptions-recorder"></a>
#### 예외

`Exceptions` 레코더는 애플리케이션 내에서 reportable한 예외 정보를 [Exceptions 카드](#exceptions-card)에서 표시하기 위해 수집합니다.

[샘플 레이트](#sampling), 무시할 예외 패턴, 예외 발생 위치 기록 여부 등을 선택적으로 설정할 수 있습니다. 예외 위치를 캡처하면 Pulse 대시보드에서 추적에 도움이 되지만, 동일 예외가 여러 위치에서 발생할 경우 각각 별도로 표시됩니다.

<a name="queues-recorder"></a>
#### 큐

`Queues` 레코더는 애플리케이션의 큐 정보를 [큐 카드](#queues-card)에 표시하기 위해 수집합니다.

[샘플 레이트](#sampling)나 무시할 잡 패턴도 선택적으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 잡

`SlowJobs` 레코더는 애플리케이션에서 발생하는 느린 작업 정보를 [느린 잡 카드](#slow-jobs-recorder)에서 표시하기 위해 수집합니다.

느린 작업 임계값, [샘플 레이트](#sampling), 무시할 잡 패턴 등도 선택적으로 조정할 수 있습니다.

특정 잡(Job)이 오래 걸릴 것으로 예상된다면 아래와 같이 잡별 임계값 설정도 가능합니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

정규식 패턴이 잡 클래스를 매칭하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/{{version}}/http-client)로 전송된 외부 HTTP 요청이 임계값을 초과할 경우 [느린 외부 요청 카드](#slow-outgoing-requests-card)에 표시하도록 정보를 수집합니다.

임계값, [샘플 레이트](#sampling), 무시할 URL 패턴 등을 선택적으로 설정할 수 있습니다.

특정 요청이 오래 걸릴 것으로 예상된다면 아래와 같이 요청별 임계값 설정도 가능합니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규식 패턴이 요청의 URL을 매칭하지 않으면 `'default'` 값이 사용됩니다.

유사한 URL 묶기도 가능합니다. 예를 들어, URL 경로의 고유 ID를 제거하거나 도메인별 그룹화 등을 위해 정규 표현식으로 URL 일부를 치환할 수 있습니다:

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

가장 먼저 매칭되는 패턴이 사용되며, 매칭되는 패턴이 없다면 URL은 그대로 저장됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 레코더는 임계값을 초과하는 데이터베이스 쿼리를 [느린 쿼리 카드](#slow-queries-card)에 표시하기 위해 수집합니다.

느린 쿼리 임계값, [샘플 레이트](#sampling), 무시할 쿼리 패턴, 쿼리 위치 캡처 여부 등을 선택적으로 조정할 수 있습니다. 여러 위치에서 동일한 쿼리가 발생할 경우, 각각의 위치별로 별도 표시됩니다.

특정 쿼리가 오래 걸릴 것으로 예상된다면 쿼리별 임계값도 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

정규 표현식이 쿼리의 SQL을 매칭하지 않으면 `'default'` 값을 사용합니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 레코더는 애플리케이션에 대한 요청 정보를 [느린 요청 카드](#slow-requests-card) 및 [애플리케이션 사용 카드](#application-usage-card)에 표시하기 위해 수집합니다.

느린 라우트 임계값, [샘플 레이트](#sampling), 무시할 경로 등을 옵션으로 조정할 수 있습니다.

특정 요청이 오래 걸릴 것으로 예상된다면 아래와 같이 요청별 임계값 설정도 가능합니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규 표현식 패턴이 요청의 URL을 매칭하지 않으면 `'default'` 값을 사용합니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 레코더는 애플리케이션을 구동하는 서버의 CPU, 메모리, 스토리지 사용량을 수집하여 [서버 카드](#servers-card)에 표시합니다. 이 레코더는 [pulse:check 명령어](#capturing-entries)가 모니터링할 각 서버에서 실행 중이어야 합니다.

모든 서버에는 고유한 이름이 필요하며, 기본적으로 Pulse는 PHP의 `gethostname` 함수가 반환하는 값을 사용합니다. 이를 커스터마이즈하려면 `PULSE_SERVER_NAME` 환경 변수를 지정하세요:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일을 통해 감시할 디렉터리도 커스터마이즈할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 잡

`UserJobs` 레코더는 잡을 디스패치하는 사용자 정보를 [애플리케이션 사용 카드](#application-usage-card)에 표시하기 위해 수집합니다.

[샘플 레이트](#sampling) 및 무시할 잡 패턴도 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청

`UserRequests` 레코더는 요청을 보내는 사용자 정보를 [애플리케이션 사용 카드](#application-usage-card)에 표시하기 위해 수집합니다.

[샘플 레이트](#sampling) 및 무시할 URL 패턴도 조정할 수 있습니다.

<a name="filtering"></a>
### 필터링

앞서 언급했듯, 많은 [레코더](#recorders)가 구성 옵션을 통해 들어오는 엔트리를 무시(예: 요청 URL별)하도록 지원합니다. 그러나 때로는 인증된 사용자 등 다른 조건을 기준으로 기록을 필터링해야 할 수도 있습니다. 이 경우 Pulse의 `filter` 메서드에 클로저를 전달할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `boot` 메서드 내에서 호출합니다:

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

Pulse는 별도의 인프라 없이도 기존 애플리케이션에 바로 적용할 수 있도록 설계되었습니다. 다만, 대규모 트래픽 환경에서는 Pulse로 인해 성능에 영향이 가지 않도록 여러 방법을 제공하고 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용

대규모 트래픽이 예상되는 경우 Pulse 데이터를 별도의 데이터베이스 연결로 관리하여 애플리케이션 데이터베이스에 영향을 주지 않도록 할 수 있습니다.

`PULSE_DB_CONNECTION` 환경 변수를 설정하여 Pulse에서 사용할 [데이터베이스 연결](/docs/{{version}}/database#configuration)을 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트

> [!WARNING]
> Redis 인제스트 기능은 Redis 6.2 이상 및 `phpredis` 또는 `predis` Redis 클라이언트 드라이버가 필요합니다.

기본적으로 Pulse는 [설정된 데이터베이스 연결](#using-a-different-database)에 엔트리를 직접 저장하지만, `PULSE_INGEST_DRIVER` 환경 변수를 통해 엔트리를 Redis 스트림으로 전송할 수 있습니다:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 [Redis 연결](/docs/{{version}}/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 커스터마이즈할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

Redis 인제스트를 사용할 경우, 반드시 `pulse:work` 명령으로 스트림을 모니터링하고 Redis에서 Pulse 데이터베이스 테이블로 엔트리를 이동해야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드로 영구 실행하려면 Supervisor와 같은 프로세스 모니터를 사용해야 합니다.

`pulse:work` 명령 역시 장기 실행 프로세스이기 때문에, 코드 변경 사항을 반영하려면 배포 시 `pulse:restart` 명령어로 안전하게 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/{{version}}/cache)를 재시작 신호 저장소로 활용하므로, 이 기능을 사용하기 전 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인하세요.

<a name="sampling"></a>
### 샘플링

Pulse는 기본적으로 발생한 모든 관련 이벤트를 기록합니다. 대규모 트래픽 환경에서는 대시보드 집계 시 수백만 개의 데이터베이스 행을 다뤄야 할 수도 있습니다.

이럴 때 Pulse의 일부 레코더는 "샘플링" 기능을 활성화할 수 있습니다. 예를 들어, [`User Requests`](#user-requests-recorder) 레코더의 샘플 레이트를 `0.1`로 지정하면 실제 요청의 약 10%만 기록하게 됩니다. 대시보드에서는 값이 스케일업되어 `~` 기호가 붙은 근사치로 표시됩니다.

특정 메트릭 엔트리가 많을수록, 샘플 레이트를 낮춰도 정확도가 크게 저하되지 않습니다.

<a name="trimming"></a>
### 트리밍(데이터 정리)

Pulse는 대시보드 창(window) 밖으로 벗어난 엔트리를 자동으로 정리(트리밍)합니다. 트리밍은 인제스트(수집) 과정에서 복권(lottery) 시스템을 통해 발생하며, Pulse [설정 파일](#configuration)에서 커스터마이즈 할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 핸들링

Pulse 데이터 캡처 중 데이터베이스 연결 실패 등 예외가 발생하면, Pulse는 애플리케이션에 영향을 주지 않도록 조용히 실패하도록 설계되어 있습니다.

이 예외 처리 방식을 커스터마이즈하려면 `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다:

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

Pulse는 애플리케이션의 특정 데이터 요구사항에 맞춘 커스텀 카드를 제작할 수 있도록 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)을 사용하므로, 시작 전 [Livewire 문서](https://livewire.laravel.com/docs)를 참고할 것을 권장합니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트

Laravel Pulse에서 커스텀 카드를 만들려면 기본 `Card` Livewire 컴포넌트를 상속하고, 대응되는 뷰를 작성하는 것부터 시작합니다:

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

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 때, `Card` 컴포넌트는 카드에 전달된 `cols`, `rows` 속성을 반영한 플레이스홀더를 자동 제공합니다.

카드의 뷰에서는 Pulse의 Blade 컴포넌트를 활용하여 일관된 UI/UX를 구현할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각 대응하는 Blade 컴포넌트에 전달되어야 하며, 이를 통해 대시보드 뷰에서 카드의 레이아웃을 자유롭게 커스터마이즈할 수 있습니다. 카드 자동 갱신이 필요하다면 `wire:poll.5s=""` 속성을 사용할 수 있습니다.

Livewire 컴포넌트와 템플릿을 정의한 후, 카드를 [대시보드 뷰](#dashboard-customization)에 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 패키지에서 카드를 배포하는 경우, Livewire의 `Livewire::component` 메서드를 사용하여 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링

카드에 Pulse 기본 클래스 및 컴포넌트 외 커스텀 스타일이 필요하다면, 다음과 같이 스타일을 추가할 수 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

커스텀 카드가 애플리케이션 코드 내에 있고 Laravel의 [Vite 통합](/docs/{{version}}/vite)을 사용하는 경우, `vite.config.js` 파일에서 카드용 CSS 엔트리포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

그 후 [대시보드 뷰](#dashboard-customization)에서 `@vite` 블레이드 디렉티브로 CSS 엔트리포인트를 참조하세요:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일 직접 추가

패키지 등에 포함된 Pulse 카드 등 다른 사용 사례에서는, Livewire 컴포넌트에 `css` 메서드를 정의하여 CSS 파일 경로를 반환하게 할 수 있습니다:

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

카드가 대시보드에 포함될 때 Pulse가 자동으로 `<style>` 태그로 파일 내용을 추가해주므로 `public` 디렉터리로 퍼블리시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS 사용 시, 불필요한 CSS 로드나 Pulse Tailwind 클래스와의 충돌을 방지하기 위해 별도의 Tailwind 설정 파일을 생성합니다:

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

그런 다음 CSS 엔트리포인트에 설정 파일을 지정합니다:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

또한, 카드의 뷰에는 Tailwind의 [`important` 선택자 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에 맞는 `id` 또는 `class` 속성이 포함되어야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계

커스텀 카드는 어디서나 데이터를 가져와 표시할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템도 활용할 수 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처

Pulse는 `Pulse::record` 메서드를 사용하여 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

첫 번째 인수는 레코딩할 엔트리의 `type`, 두 번째 인수는 집계 데이터 그룹화를 결정하는 `key`입니다. 대부분의 집계 메서드는 집계할 `value`도 필요합니다(예: `$sale->amount`). 그 후, 하나 이상의 집계 메서드(예: `sum`)를 호출해, Pulse가 사전에 집계된 "버킷"에 값을 저장하도록 할 수 있습니다.

사용 가능한 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 인증된 사용자 ID를 기록하는 카드 패키지를 개발할 때는, 애플리케이션의 [사용자 확인 관련 커스터마이즈](#dashboard-resolving-users)를 반영하는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하는 것이 좋습니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회

Pulse의 `Card` Livewire 컴포넌트를 확장할 때, 대시보드에서 선택한 기간에 대한 집계 데이터를 가져오기 위해 `aggregate` 메서드를 사용할 수 있습니다:

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

`aggregate` 메서드는 PHP `stdClass` 객체의 컬렉션을 반환하며, 각 객체에는 앞서 저장한 `key`와, 요청한 집계별 키(`sum`, `count` 등)가 포함됩니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 사전 집계된 버킷에서 데이터를 조회하므로, 반드시 집계가 필요한 값은 사전에 `Pulse::record` 메서드로 기록해야 합니다. 가장 오래된 버킷은 기간의 일부만 포함할 수 있어, 해당 부분만 합산 집계하여 전체 기간의 정확한 값이 계산됩니다.

특정 타입의 전체 합계를 조회하려면 `aggregateTotal` 메서드를 사용할 수 있습니다. 다음 예시는 사용자별 합계가 아닌, 전체 사용자 판매 금액의 총합을 조회합니다.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시

`key`에 사용자 ID를 저장하는 집계 데이터의 경우, `Pulse::resolveUsers` 메서드로 해당 키를 사용자 레코드로 변환할 수 있습니다.

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

`find` 메서드는 `name`, `extra`, `avatar` 값을 포함한 객체를 반환하며, 이를 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달할 수도 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더

패키지 제작자는 데이터 캡처를 위한 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 설정 파일의 `recorders`에 등록합니다:

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

레코더는 `$listen` 속성으로 이벤트를 지정할 수 있습니다. Pulse가 자동으로 이벤트 리스너를 등록하고 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 청취할 이벤트 목록.
     *
     * @var array<int, class-string>
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