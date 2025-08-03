# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 권한 설정](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리 필터링](#filtering-entries)
    - [배치 필터링](#filtering-batches)
- [태깅](#tagging)
- [사용 가능한 워처](#available-watchers)
    - [배치 워처](#batch-watcher)
    - [캐시 워처](#cache-watcher)
    - [커맨드 워처](#command-watcher)
    - [덤프 워처](#dump-watcher)
    - [이벤트 워처](#event-watcher)
    - [예외 워처](#exception-watcher)
    - [게이트 워처](#gate-watcher)
    - [HTTP 클라이언트 워처](#http-client-watcher)
    - [잡 워처](#job-watcher)
    - [로그 워처](#log-watcher)
    - [메일 워처](#mail-watcher)
    - [모델 워처](#model-watcher)
    - [알림 워처](#notification-watcher)
    - [쿼리 워처](#query-watcher)
    - [Redis 워처](#redis-watcher)
    - [요청 워처](#request-watcher)
    - [스케줄 워처](#schedule-watcher)
    - [뷰 워처](#view-watcher)
- [사용자 아바타 표시](#displaying-user-avatars)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Telescope](https://github.com/laravel/telescope)은 로컬 Laravel 개발 환경에 매우 유용한 도구입니다. Telescope는 애플리케이션으로 들어오는 요청, 예외, 로그 항목, 데이터베이스 쿼리, 큐에 들어간 작업, 메일, 알림, 캐시 동작, 예약된 작업, 변수 덤프 등 다양한 정보를 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치 (Installation)

Composer 패키지 매니저를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후, `telescope:install` Artisan 명령어로 자산을 게시하세요. 또한 Telescope 데이터를 저장할 테이블을 생성하려면 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로 `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징

Telescope 기본 마이그레이션을 사용하지 않을 경우, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `register` 메서드 내에서 `Telescope::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션은 다음 명령어로 내보낼 수 있습니다: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### 로컬 전용 설치 (Local Only Installation)

로컬 개발 환경에서만 Telescope를 사용하려면 `--dev` 플래그를 이용해 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후, 애플리케이션 `config/app.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거하세요. 대신 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에 Telescope 서비스 프로바이더를 수동으로 등록합니다. 이때 현재 환경이 `local`인지 확인한 후 등록합니다:

```
/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    if ($this->app->environment('local')) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

마지막으로 `composer.json` 파일에 다음 내용을 추가하여 Telescope 패키지가 [자동 탐색](/docs/10.x/packages#package-discovery)되지 않도록 해야 합니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},
```

<a name="configuration"></a>
### 설정 (Configuration)

Telescope 자산을 게시한 후 기본 설정 파일은 `config/telescope.php` 에 위치합니다. 이 파일에서 [워처 옵션](#available-watchers)을 구성할 수 있으며, 각 설정 항목에 기능 설명이 포함되어 있으니 꼭 자세히 살펴보세요.

필요한 경우 `enabled` 설정 옵션을 이용해 Telescope의 데이터 수집을 완전히 비활성화할 수도 있습니다:

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리 (Data Pruning)

데이터 정리 없이 `telescope_entries` 테이블에 데이터가 빠르게 쌓일 수 있습니다. 이를 방지하려면 `telescope:prune` Artisan 명령어를 [스케줄](/docs/10.x/scheduling)하여 매일 실행하도록 설정하는 것이 좋습니다:

```
$schedule->command('telescope:prune')->daily();
```

기본적으로 24시간이 지난 모든 기록은 정리됩니다. `hours` 옵션을 명령어 호출 시 지정하면 데이터를 보관할 시간을 조절할 수 있습니다. 예를 들어, 48시간이 지난 모든 기록을 삭제하려면 다음과 같이 설정합니다:

```
$schedule->command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Telescope 대시보드는 `/telescope` 경로로 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접속할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일에는 [인가 게이트](/docs/10.x/authorization#gates)가 정의되어 있어, **비로컬 환경**에서 Telescope 접근 권한을 제어합니다. 필요에 따라 이 게이트를 수정해 Telescope 접근 범위를 제한할 수 있습니다:

```
use App\Models\User;

/**
 * Telescope 게이트를 등록합니다.
 *
 * 이 게이트는 비로컬 환경에서 Telescope에 접근할 수 있는 사용자를 결정합니다.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]  
> 운영 환경에서는 `APP_ENV` 환경 변수를 반드시 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope가 공개되어 누구나 접근할 수 있게 됩니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드 (Upgrading Telescope)

새로운 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하는 것이 중요합니다.

또한 Telescope를 새 버전으로 업그레이드할 때는 자산을 다시 게시하는 것이 좋습니다:

```shell
php artisan telescope:publish
```

자산을 최신 상태로 유지하고 향후 업데이트 문제를 방지하려면, 애플리케이션 `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령을 추가할 수 있습니다:

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="filtering"></a>
## 필터링 (Filtering)

<a name="filtering-entries"></a>
### 엔트리 필터링 (Entries)

`App\Providers\TelescopeServiceProvider` 클래스에서 정의된 `filter` 클로저를 통해 Telescope가 기록할 데이터를 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하며, 다른 환경에서는 예외, 실패한 작업, 예약 작업, 느린 쿼리, 모니터링 태그가 포함된 데이터만 기록합니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}
```

<a name="filtering-batches"></a>
### 배치 필터링 (Batches)

`filter` 클로저가 단일 엔트리에 대한 데이터를 필터링하는 반면, `filterBatch` 메서드는 특정 요청이나 콘솔 커맨드에 관련된 모든 데이터(배치)를 필터링할 클로저를 등록할 때 사용합니다. 클로저가 `true`를 반환하면 해당 배치의 모든 엔트리가 Telescope에 기록됩니다:

```
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}
```

<a name="tagging"></a>
## 태깅 (Tagging)

Telescope는 "태그"를 통해 엔트리를 검색할 수 있게 해줍니다. 태그는 일반적으로 Eloquent 모델 클래스명이나 인증된 사용자 ID로, Telescope가 자동으로 엔트리에 추가합니다. 가끔은 사용자가 직접 커스텀 태그를 엔트리에 붙이고 싶을 때가 있습니다. 이럴 경우 `Telescope::tag` 메서드를 사용합니다. 이 메서드는 태그 배열을 반환하는 클로저를 인자로 받으며, 반환된 태그는 Telescope가 자동으로 붙이는 태그와 병합됩니다. 보통 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 안에서 호출합니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === 'request'
                    ? ['status:'.$entry->content['response_status']]
                    : [];
    });
 }
```

<a name="available-watchers"></a>
## 사용 가능한 워처 (Available Watchers)

Telescope "워처"는 요청이나 콘솔 커맨드가 실행될 때 애플리케이션 내 데이터를 수집합니다. 활성화할 워처 목록을 `config/telescope.php` 설정 파일 안에서 커스터마이징할 수 있습니다:

```
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    ...
],
```

일부 워처는 추가 설정 옵션도 제공합니다:

```
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    ...
],
```

<a name="batch-watcher"></a>
### 배치 워처 (Batch Watcher)

배치 워처는 [배치](/docs/10.x/queues#job-batching) 큐 작업에 대한 정보, 작업과 연결 관련 데이터를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처 (Cache Watcher)

캐시 워처는 캐시 키가 적중(hit), 미스(miss), 업데이트, 삭제될 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처 (Command Watcher)

커맨드 워처는 Artisan 명령이 실행될 때 인수, 옵션, 종료 코드, 출력 결과를 기록합니다. 특정 명령어를 제외하려면 `config/telescope.php` 파일에서 `ignore` 옵션에 명령어를 지정할 수 있습니다:

```
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    ...
],
```

<a name="dump-watcher"></a>
### 덤프 워처 (Dump Watcher)

덤프 워처는 변수 덤프를 기록하고 Telescope에서 표시합니다. Laravel에서는 전역 `dump` 함수를 통해 변수를 덤프할 수 있습니다. 덤프 워처 탭이 브라우저에 열려 있어야 덤프가 기록되며, 그렇지 않으면 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처 (Event Watcher)

이벤트 워처는 애플리케이션에서 디스패치한 [이벤트](/docs/10.x/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. Laravel 프레임워크 내부 이벤트는 이벤트 워처가 무시합니다.

<a name="exception-watcher"></a>
### 예외 워처 (Exception Watcher)

예외 워처는 애플리케이션에서 던져지는 보고 대상 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처 (Gate Watcher)

게이트 워처는 애플리케이션에서 수행되는 [게이트 및 정책](/docs/10.x/authorization) 검증 데이터와 결과를 기록합니다. 특정 권한을 기록 대상에서 제외하려면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 그 권한명을 지정하세요:

```
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    ...
],
```

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처 (HTTP Client Watcher)

HTTP 클라이언트 워처는 애플리케이션에서 발생하는 [HTTP 클라이언트 요청](/docs/10.x/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처 (Job Watcher)

잡 워처는 애플리케이션에서 디스패치되는 [잡](/docs/10.x/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처 (Log Watcher)

로그 워처는 애플리케이션에서 작성되는 [로그 데이터](/docs/10.x/logging)를 기록합니다.

기본적으로 Telescope는 `error` 레벨 이상의 로그만 기록합니다. 하지만 애플리케이션 `config/telescope.php` 설정 파일에서 `level` 옵션을 수정해 이를 변경할 수 있습니다:

```
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],
```

<a name="mail-watcher"></a>
### 메일 워처 (Mail Watcher)

메일 워처를 통해 애플리케이션에서 발송된 [메일](/docs/10.x/mail)의 브라우저 내 미리보기를 볼 수 있습니다. 또한 이메일 파일을 `.eml` 형식으로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 워처 (Model Watcher)

모델 워처는 Eloquent [모델 이벤트](/docs/10.x/eloquent#events)가 발생할 때 모델 변경사항을 기록합니다. `events` 옵션을 통해 어떤 모델 이벤트를 기록할지 지정할 수 있습니다:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

요청당 수화(hydration)된 모델 개수를 기록하려면 `hydrations` 옵션을 활성화하세요:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    ...
],
```

<a name="notification-watcher"></a>
### 알림 워처 (Notification Watcher)

알림 워처는 애플리케이션에서 발송된 모든 [알림](/docs/10.x/notifications)을 기록합니다. 알림이 메일을 트리거하고 메일 워처가 활성화된 경우, 해당 메일도 메일 워처 화면에서 미리볼 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처 (Query Watcher)

쿼리 워처는 애플리케이션에서 실행되는 모든 SQL 쿼리의 원본 SQL, 바인딩, 실행 시간을 기록합니다. 또한 100밀리초를 초과한 느린 쿼리를 `slow` 태그로 표시합니다. `slow` 옵션으로 느린 쿼리 임계값을 조정할 수 있습니다:

```
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    ...
],
```

<a name="redis-watcher"></a>
### Redis 워처 (Redis Watcher)

Redis 워처는 애플리케이션에서 실행되는 모든 [Redis](/docs/10.x/redis) 명령을 기록합니다. Redis를 캐시로 사용 중이라면 캐시 관련 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처 (Request Watcher)

요청 워처는 애플리케이션이 처리하는 요청, 헤더, 세션, 응답 데이터를 기록합니다. `size_limit` 옵션으로 기록할 응답 데이터 크기 제한(킬로바이트 단위)을 설정할 수 있습니다:

```
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    ...
],
```

<a name="schedule-watcher"></a>
### 스케줄 워처 (Schedule Watcher)

스케줄 워처는 애플리케이션에서 실행하는 [예약된 작업](/docs/10.x/scheduling)의 커맨드와 출력 결과를 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처 (View Watcher)

뷰 워처는 뷰를 렌더링할 때 사용된 [뷰](/docs/10.x/views) 이름, 경로, 데이터, 그리고 "컴포저(composers)"를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시 (Displaying User Avatars)

Telescope 대시보드는 특정 엔트리 저장 시 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 하지만 `App\Providers\TelescopeServiceProvider` 클래스에 콜백을 등록하여 아바타 URL을 커스터마이징할 수 있습니다. 콜백은 사용자 ID와 이메일을 받아 사용자 아바타 이미지 URL을 반환해야 합니다:

```
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (string $id, string $email) {
        return '/avatars/'.User::find($id)->avatar_path;
    });
}
```