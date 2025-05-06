# Laravel Pulse

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [권한 설정](#dashboard-authorization)
    - [커스터마이즈](#dashboard-customization)
    - [사용자 해석](#dashboard-resolving-users)
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

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있는 인사이트를 제공합니다. Pulse를 사용하면 느린 작업과 엔드포인트와 같은 병목 현상을 추적하고, 가장 활동적인 사용자를 파악하는 등 다양한 정보를 확인할 수 있습니다.

개별 이벤트에 대한 심층 디버깅이 필요하다면 [Laravel Telescope](/docs/{{version}}/telescope)도 참고하세요.

<a name="installation"></a>
## 설치

> [!WARNING]  
> Pulse의 공식 스토리지 구현은 현재 MySQL 또는 PostgreSQL 데이터베이스가 필요합니다. 다른 데이터베이스를 사용하는 경우, Pulse 데이터를 위해 별도의 MySQL 또는 PostgreSQL 데이터베이스가 필요합니다.

Pulse는 현재 베타 단계이므로, 베타 패키지 설치를 허용하기 위해 애플리케이션의 `composer.json` 파일을 다음과 같이 조정해야 할 수 있습니다:

```json
"minimum-stability": "beta",
"prefer-stable": true
```

이후 Composer 패키지 매니저를 사용하여 Laravel 프로젝트에 Pulse를 설치합니다:

```sh
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 Pulse 설정 및 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

그리고 Pulse 데이터를 저장할 테이블을 생성하기 위해 마이그레이션 명령어를 실행하세요:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]  
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하지 않으려면, [별도의 데이터베이스 연결 지정](#using-a-different-database)을 할 수 있습니다.

<a name="configuration"></a>
### 설정

Pulse의 많은 설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하고, 새로운 레코더를 등록하거나 고급 옵션을 설정하려면 `config/pulse.php` 설정 파일을 퍼블리시하세요:

```sh
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드

<a name="dashboard-authorization"></a>
### 권한 설정

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근할 수 있으므로, 운영 환경에서는 `'viewPulse'` 권한 게이트를 커스터마이즈하여 접근 권한을 설정해야 합니다. 이 작업은 `app/Providers/AuthServiceProvider.php` 파일에서 할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 인증/권한 서비스 등록
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

Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰를 퍼블리시하여 설정할 수 있습니다. 대시보드 뷰는 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 생성됩니다:

```sh
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/) 기반으로 동작하며, JavaScript 자산을 재빌드하지 않고도 카드와 레이아웃을 자유롭게 변경할 수 있습니다.

이 파일에서는 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며 카드의 그리드 레이아웃을 제공합니다. 대시보드를 화면 전체 너비로 사용하려면, `full-width` 프로퍼티를 컴포넌트에 추가하면 됩니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12 열 그리드를 생성하지만, `cols` 프로퍼티로 커스터마이즈할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 `cols`와 `rows` 프로퍼티로 공간 및 위치를 제어할 수 있습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에는 `expand` 프로퍼티도 제공되어, 스크롤 없이 전체 카드 내용을 보여줄 수 있습니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 해석

Application Usage 카드 등에서 사용자 정보를 보여줄 때, Pulse는 사용자의 ID만 기록합니다. 대시보드 렌더링 시 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 가져오고, Gravatar 웹 서비스를 통해 아바타를 표시합니다.

필드와 아바타를 커스터마이즈하려면, 애플리케이션의 `App\Providers\AppServiceProvider`에서 `Pulse::user` 메서드를 호출하세요.

`user` 메서드는 표시할 `Authenticatable` 모델을 받아, `name`, `extra`, `avatar` 정보를 담은 배열을 반환해야 합니다:

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
> 인증된 사용자를 캡처하고 불러오는 방식을 완전히 커스터마이즈하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel의 [서비스 컨테이너](/docs/{{version}}/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령을 실행 중인 모든 서버의 시스템 리소스 사용량을 보여줍니다. 시스템 리소스 보고에 대한 자세한 내용은 [servers recorder](#servers-recorder) 문서를 참고하세요.

<a name="application-usage-card"></a>
#### 애플리케이션 사용량

`<livewire:pulse.usage />` 카드는 애플리케이션에서 요청을 보내고 작업을 디스패치하며 느린 요청을 경험한 상위 10명의 사용자를 보여줍니다.

모든 사용량 지표를 동시에 화면에 표시하려면, 여러 번 카드를 추가하고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse의 사용자 정보 가져오기 및 표시 방법을 커스터마이즈하는 법은 [사용자 해석](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]  
> 애플리케이션에서 많은 요청을 받거나 많은 작업을 디스패치하는 경우 [샘플링](#sampling) 활성화를 고려할 수 있습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도 및 최근 발생 현황을 보여줍니다. 기본적으로 예외는 예외 클래스 및 발생 위치 기준으로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리량(대기, 처리 중, 처리 완료, 재처리, 실패한 작업 수 포함)을 보여줍니다. 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청

`<livewire:pulse.slow-requests />` 카드는 구성된 임계값(기본값: 1,000ms)을 초과하는 애플리케이션의 들어오는 요청을 표시합니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업

`<livewire:pulse.slow-jobs />` 카드는 구성된 임계값(기본값: 1,000ms)을 초과한 대기열 작업을 보여줍니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리

`<livewire:pulse.slow-queries />` 카드는 구성된 임계값(기본값: 1,000ms)을 초과한 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외)와 발생 위치 기준으로 그룹화됩니다. 원한다면 위치 캡처 없이 SQL 쿼리만으로 그룹화할 수도 있습니다.

자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/{{version}}/http-client)를 사용해 설정된 임계값(기본값: 1,000ms)을 초과한 외부 요청을 보여줍니다.

기본적으로 전체 URL로 그룹화하지만, 정규표현식을 사용해 비슷한 외부 요청을 노말라이즈하거나 그룹화할 수도 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시

`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 적중율과 실패율을 전체 및 개별 키 단위로 보여줍니다.

기본적으로 키별로 그룹화되지만, 정규표현식을 사용해 비슷한 키를 그룹화할 수도 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처

대부분의 Pulse 레코더는 Laravel에서 발생시키는 프레임워크 이벤트를 기반으로 자동으로 엔트리를 캡처합니다. 하지만, [servers recorder](#servers-recorder)나 일부 서드파티 카드 등은 주기적으로 정보를 폴링해야 합니다. 이러한 카드를 사용하려면, 모든 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]  
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor와 같은 프로세스 모니터를 사용해 명령이 종료되지 않도록 해야 합니다.

`pulse:check` 명령은 장기 실행 프로세스이므로, 코드 변경 사항을 반영하려면 재시작이 필요합니다. 배포 과정에서 `pulse:restart` 명령을 호출하여 명령어를 정상적으로 재시작하세요:

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse는 재시작 신호를 저장하기 위해 [캐시](/docs/{{version}}/cache)를 사용하므로, 이 기능을 사용하려면 애플리케이션에 적절한 캐시 드라이버가 설정되어 있어야 합니다.

<a name="recorders"></a>
### 레코더

레코더는 Pulse 데이터베이스에 기록할 애플리케이션 엔트리를 캡처하는 역할을 합니다. 레코더 등록 및 설정은 [Pulse 설정 파일](#configuration)의 `recorders` 섹션에서 관리합니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용

`CacheInteractions` 레코더는 애플리케이션에서 발생하는 [캐시](/docs/{{version}}/cache) 적중 및 실패 정보를 캡처하여 [Cache](#cache-card) 카드에 표시합니다.

샘플링 비율([sample rate](#sampling))과 무시할 키 패턴을 옵션으로 조정할 수 있습니다.

비슷한 키를 하나로 그룹화하려면 정규표현식을 사용한 "find and replace" 설정도 가능합니다. 예를 들어, 동일 유형의 정보를 캐싱하는 키에서 고유 ID를 제거할 수 있습니다. 구성 파일에 예제가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

첫 번째로 매칭되는 패턴이 사용되며, 매칭되지 않으면 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외

`Exceptions` 레코더는 애플리케이션에서 발생한 리포트 가능한 예외 정보를 캡처하여 [Exceptions](#exceptions-card) 카드에 표시합니다.

샘플링 비율([sample rate](#sampling)), 무시할 예외 패턴, 예외 발생 위치 캡처 여부를 옵션으로 조정할 수 있습니다. 캡처된 위치 정보는 대시보드에 표시되어 예외 원인 추적에 도움이 되지만, 동일 예외가 여러 위치에서 발생하면 각 위치별로 여러 번 표시될 수 있습니다.

<a name="queues-recorder"></a>
#### 큐

`Queues` 레코더는 애플리케이션 큐의 정보를 캡처하여 [Queues](#queues-card)에 표시합니다.

샘플링 비율([sample rate](#sampling))과 무시할 작업 패턴을 옵션으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업

`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업 정보를 캡처하여 [Slow Jobs](#slow-jobs-recorder) 카드에 표시합니다.

느린 작업 임계값, 샘플 비율([sample rate](#sampling)), 무시할 작업 패턴 등을 옵션으로 조정할 수 있습니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/{{version}}/http-client)에 의해 생성된 임계값 초과 외부 요청 정보를 캡처하여 [Slow Outgoing Requests](#slow-outgoing-requests-card) 카드에 표시합니다.

느린 외부 요청 임계값, 샘플링 비율([sample rate](#sampling)), 무시할 URL 패턴 등을 옵션으로 조정할 수 있습니다.

URL 그룹화도 가능하며, 정규표현식을 사용해 비슷한 URL을 그룹화할 수 있습니다. 예시는 구성 파일에 포함되어 있습니다:

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

첫 번째로 일치하는 패턴이 적용되며, 없을 경우 URL은 그대로 기록됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 레코더는 임계값을 초과한 데이터베이스 쿼리 정보를 캡처하여 [Slow Queries](#slow-queries-card) 카드에 표시합니다.

느린 쿼리 임계값, 샘플링 비율([sample rate](#sampling)), 무시할 쿼리 패턴, 쿼리 위치 정보 캡처 여부 등을 설정할 수 있습니다. 위치 정보를 캡처하면 쿼리 발생 원인 추적에 도움이 됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 레코더는 애플리케이션의 들어오는 요청 정보를 캡처하여 [Slow Requests](#slow-requests-card), [Application Usage](#application-usage-card) 카드에 표시합니다.

느린 라우트 임계값, 샘플 비율([sample rate](#sampling)), 무시할 경로 등을 옵션으로 설정할 수 있습니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장소 사용량 정보를 캡처하여 [Servers](#servers-card) 카드에 표시합니다. 이 레코더는 모니터링하려는 각 서버에서 [`pulse:check` 명령](#capturing-entries)이 실행 중이어야 합니다.

서버별로 고유 이름이 필요하며, 기본적으로 PHP의 `gethostname` 반환값을 사용합니다. 직접 지정하려면 `PULSE_SERVER_NAME` 환경 변수를 설정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링할 디렉토리 목록도 커스터마이즈 할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업

`UserJobs` 레코더는 애플리케이션에서 작업을 디스패치한 사용자 정보를 캡처하여 [Application Usage](#application-usage-card) 카드에 표시합니다.

샘플링 비율([sample rate](#sampling)), 무시할 작업 패턴 등을 옵션으로 설정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청

`UserRequests` 레코더는 애플리케이션에서 요청을 보낸 사용자 정보를 캡처하여 [Application Usage](#application-usage-card) 카드에 표시합니다.

샘플링 비율([sample rate](#sampling)), 무시할 작업 패턴 등을 옵션으로 설정할 수 있습니다.

<a name="filtering"></a>
### 필터링

많은 [레코더](#recorders)들은 요청의 URL과 같은 값에 따라 엔트리를 무시하도록 설정할 수 있습니다. 하지만, 인증된 사용자 등 다른 요소를 바탕으로 기록을 필터링하고 싶을 때도 있습니다. 이럴 때는 Pulse의 `filter` 메서드에 클로저를 전달할 수 있습니다. `filter` 메서드는 일반적으로 `AppServiceProvider`의 `boot` 메서드 내에서 호출합니다:

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
## 성능

Pulse는 추가 인프라 없이 기존 애플리케이션에 바로 적용할 수 있도록 설계되었습니다. 하지만 고트래픽 애플리케이션의 경우 Pulse가 미치는 성능 영향을 최소화하는 여러 방법이 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용

고트래픽 애플리케이션에서는 Pulse 전용 데이터베이스 연결을 사용해 메인 데이터베이스에 미치는 영향을 최소화할 수 있습니다.

Pulse가 사용할 [데이터베이스 연결](/docs/{{version}}/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수로 설정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트

> [!WARNING]  
> Redis Ingest는 Redis 6.2 이상과 `phpredis` 또는 `predis`를 Redis 클라이언트 드라이버로 필요로 합니다.

기본적으로 Pulse는 [설정된 데이터베이스 연결](#using-a-different-database)에 엔트리를 직접 저장합니다(HTTP 응답 후나 작업 처리 후). 하지만, Pulse의 Redis 인제스트 드라이버를 사용하면 엔트리를 Redis 스트림으로 전송할 수 있습니다. 이를 사용하려면 `PULSE_INGEST_DRIVER` 환경 변수를 설정하세요:

```
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 [Redis 연결](/docs/{{version}}/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 변경할 수 있습니다:

```
PULSE_REDIS_CONNECTION=pulse
```

Redis 인제스트를 사용할 때는 `pulse:work` 명령을 실행하여 스트림을 모니터링하고, 엔트리를 Pulse 데이터베이스 테이블로 이동시켜야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]  
> `pulse:work` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor 등 프로세스 모니터를 사용해 Pulse 워커가 멈추지 않도록 해야 합니다.

`pulse:work` 명령도 장기 실행 프로세스이므로, 코드 변경 시 재시작이 필요합니다. 배포 단계에서 `pulse:restart` 명령어로 정상적으로 재시작하세요:

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse는 [캐시](/docs/{{version}}/cache)를 사용하여 재시작 신호를 저장합니다. 이 기능을 활용하려면 애플리케이션에 적절한 캐시 드라이버가 설정되어 있어야 합니다.

<a name="sampling"></a>
### 샘플링

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 캡처합니다. 고트래픽 애플리케이션의 경우, 이는 대시보드에서 수백만 개의 행을 집계해야 하므로 성능에 영향을 줄 수 있습니다.

이럴 때는 일부 Pulse 데이터 레코더에서 "샘플링"을 활성화하는 것이 좋습니다. 예를 들어 [`User Requests`](#user-requests-recorder) 레코더의 샘플 비율을 `0.1`로 설정하면, 전체 요청 중 약 10%만 기록합니다. 대시보드에서 이 값은 스케일업되어 `~` 표시로 근사치임이 나타납니다.

일반적으로 하나의 메트릭에 엔트리가 많을수록, 정확도를 크게 희생하지 않고 샘플 비율을 더 낮출 수 있습니다.

<a name="trimming"></a>
### 트리밍

Pulse는 대시보드 윈도우를 벗어난 엔트리를 자동으로 정리(트리밍)합니다. 트리밍은 데이터 인제스트 시 로터리 시스템을 통해 발생하며, Pulse [설정 파일](#configuration)에서 커스터마이즈할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리

Pulse 데이터 캡처 중(예: 스토리지 데이터베이스 연결 실패) 예외가 발생하면, Pulse는 애플리케이션에 영향을 주지 않기 위해 조용히 실패합니다.

이 예외 처리 방식을 커스터마이즈하려면, `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다:

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

Pulse를 통해 애플리케이션의 특정 요구 사항에 맞춘 커스텀 카드를 제작해 원하는 데이터를 표시할 수 있습니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 첫 커스텀 카드를 만들기 전에 [Livewire 문서](https://livewire.laravel.com/docs)를 참고하면 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트

Laravel Pulse에서 커스텀 카드를 만들기 위해서는 기본 `Card` Livewire 컴포넌트를 확장하고, 일치하는 뷰를 정의해야 합니다:

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

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 경우, `Card` 컴포넌트는 자동으로 `cols`와 `rows` 속성에 맞는 플레이스홀더를 제공합니다.

Pulse 카드 뷰를 작성할 때는 Pulse에서 제공하는 Blade 컴포넌트를 활용해 일관된 UI를 구성할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수들은 각 Blade 컴포넌트로 전달해 대시보드에서 카드 레이아웃을 커스터마이즈할 수 있도록 합니다. 또한, `wire:poll.5s=""` 속성을 추가해 카드를 자동으로 갱신할 수 있습니다.

Livewire 컴포넌트와 템플릿을 정의한 후에는, [대시보드 뷰](#dashboard-customization)에 카드를 추가할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]  
> 패키지 내에 카드를 포함할 경우, `Livewire::component` 메서드를 사용해 컴포넌트를 Livewire에 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링

Pulse의 클래스와 컴포넌트로 충분하지 않을 경우, 카드별로 커스텀 CSS를 포함하는 다양한 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 연동

커스텀 카드가 애플리케이션 코드베이스 내에 있고, Laravel의 [Vite 연동](/docs/{{version}}/vite)을 사용하는 경우, `vite.config.js` 파일을 수정해 카드 전용 CSS 엔트리포인트를 추가하세요:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

그런 다음 [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 지시문을 사용하여 CSS 엔트리포인트를 지정할 수 있습니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

패키지 내 Pulse 카드 등 다른 경우에는 Livewire 컴포넌트에서 `css` 메서드를 정의해 css 파일 경로를 반환하면, Pulse가 자동으로 해당 파일을 `<style>` 태그로 인클루드합니다:

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

이렇게 하면 css 파일을 `public` 디렉토리에 퍼블리시(복사)하지 않아도 됩니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 경우 불필요한 CSS 로드 또는 Pulse의 Tailwind 클래스와 충돌을 방지하기 위해, 카드 전용 Tailwind 설정 파일을 생성해야 합니다:

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

그리고 CSS 엔트리포인트에서 설정 파일을 지정하세요:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Tailwind의 [`important` 셀렉터 전략](https://tailwindcss.com/docs/configuration#selector-strategy)에 맞게 카드 뷰에 일치하는 `id`나 `class` 속성도 포함해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계

커스텀 카드는 어느 곳에서나 데이터를 가져와 표시할 수 있지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용하는 것이 좋습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처

Pulse의 `Pulse::record` 메서드를 사용해 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 엔트리의 `type`, 두 번째 인자는 집계 데이터의 그룹화 기준이 되는 `key`입니다. 대부분의 집계 메서드에서는 집계할 `value`도 필요합니다(위 예시의 `$sale->amount`). 그리고 하나 이상의 집계 메서드(`sum` 등)를 호출해 사전에 집계된 데이터를 "버킷"에 저장하도록 할 수 있습니다.

사용할 수 있는 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]  
> 인증된 사용자 ID를 기록하는 카드 패키지를 만들 때는, 애플리케이션의 [사용자 해석 커스터마이즈](#dashboard-resolving-users)를 준수하는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하세요.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회

Pulse의 `Card` Livewire 컴포넌트를 확장할 때, `aggregate` 메서드를 사용해 대시보드에서 보는 기간 기준의 집계 데이터를 조회할 수 있습니다:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count']);
        ]);
    }
}
```

`aggregate` 메서드는 PHP `stdClass` 객체의 컬렉션을 반환합니다. 각 객체는 앞서 기록한 `key`와, 요청한 집계값을 포함합니다:

```
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 사전 집계된 버킷에서 데이터를 가져오기 때문에, 지정한 집계 함수는 반드시 사전에 `Pulse::record` 메서드로 기록되어야 합니다. 가장 오래된 버킷은 기간의 일부밖에 포함하지 않으므로, Pulse는 누락된 부분을 집계하여 전체 기간에 대한 정확한 값을 제공합니다.

특정 타입 전체의 합계 등 전체값이 필요하면 `aggregateTotal` 메서드를 사용할 수 있습니다. 아래 예시는 사용자별이 아니라 모든 사용자에 대한 판매 합계를 반환합니다.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시

Key에 사용자 ID를 기록한 집계 데이터의 경우, `Pulse::resolveUsers` 메서드로 사용자 정보를 불러올 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar` 키를 가진 객체를 반환하며, 이를 `<x-pulse::user-card>` Blade 컴포넌트에 바로 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더

패키지 작성자는 데이터 캡처 설정을 가능하게 하기 위해 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 파일의 `recorders` 섹션에 등록합니다:

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

레코더는 `$listen` 속성에 이벤트를 지정해 이벤트를 리슨할 수 있습니다. Pulse는 자동으로 리스너를 등록하고, 레코더의 `record` 메서드를 호출합니다:

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
     * @var list<class-string>
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
