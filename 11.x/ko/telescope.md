# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리(Pruning)](#data-pruning)
    - [대시보드 권한 설정](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [항목 필터링](#filtering-entries)
    - [배치 필터링](#filtering-batches)
- [태깅](#tagging)
- [사용 가능한 워처(Watchers)](#available-watchers)
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

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에 놀라운 동반자가 되어줍니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 항목, 데이터베이스 쿼리, 큐 작업, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 통찰할 수 있도록 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치 (Installation)

Telescope를 Laravel 프로젝트에 설치하려면 Composer 패키지 매니저를 사용할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후, `telescope:install` Artisan 명령어를 사용하여 에셋과 마이그레이션을 퍼블리시하세요. 또한 Telescope 데이터를 저장할 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로, `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치 (Local Only Installation)

Telescope를 로컬 개발에만 사용하려는 경우, `--dev` 플래그를 사용하여 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 명령어 실행 후에는 애플리케이션의 `bootstrap/providers.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 환경이 `local`일 때에만 Telescope 서비스 프로바이더를 수동으로 등록하도록 합니다:

```
/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

마지막으로, Telescope 패키지가 [자동 발견(auto-discovery)](/docs/11.x/packages#package-discovery)되지 않도록 하기 위해 `composer.json` 파일에 다음 구문을 추가해야 합니다:

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

Telescope의 에셋을 퍼블리시 한 후, 기본 설정 파일은 `config/telescope.php`에 위치합니다. 이 설정 파일에서는 [워처 옵션](#available-watchers)을 설정할 수 있으며, 각 옵션에 대한 설명도 포함되어 있으므로 꼼꼼히 살펴보시기 바랍니다.

원한다면 `enabled` 설정 옵션을 사용하여 Telescope의 데이터 수집을 완전히 비활성화할 수도 있습니다:

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리(Pruning)

데이터 정리가 없으면 `telescope_entries` 테이블에 레코드가 매우 빠르게 쌓일 수 있습니다. 이를 방지하기 위해 매일 실행되는 `telescope:prune` Artisan 명령어를 [스케줄](/docs/11.x/scheduling)에 등록해야 합니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

기본적으로 24시간이 지난 모든 항목은 정리됩니다. 명령어 실행 시 `hours` 옵션을 사용하여 데이터를 유지할 기간을 조절할 수 있습니다. 예를 들어, 다음 명령은 48시간 이상 된 모든 레코드를 삭제합니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Telescope 대시보드는 `/telescope` 경로로 접근할 수 있습니다. 기본적으로 `local` 환경에서만 이 대시보드에 접근할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일 내에는 [인가 게이트](/docs/11.x/authorization#gates) 정의가 있습니다. 이 게이트는 **로컬이 아닌 환경**에서의 Telescope 접근을 제어합니다. 필요에 따라 적절히 수정하여 Telescope 설치를 제한할 수 있습니다:

```
use App\Models\User;

/**
 * Telescope 접근 권한을 등록합니다.
 *
 * 이 게이트는 로컬이 아닌 환경에서 Telescope 접근 가능 여부를 결정합니다.
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
> 프로덕션 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope 설치가 공개적으로 접근 가능해질 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드 (Upgrading Telescope)

Telescope의 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 살펴보는 것이 중요합니다.

또한 모든 새 버전 업그레이드 시 Telescope의 에셋을 다시 퍼블리시 해야 합니다:

```shell
php artisan telescope:publish
```

에셋을 최신 상태로 유지하고 이후 업데이트에서 문제를 피하려면 애플리케이션 `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령을 추가할 수 있습니다:

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
### 항목 필터링 (Entries)

Telescope가 기록하는 데이터를 필터링하려면 `App\Providers\TelescopeServiceProvider` 클래스 내에 정의된 `filter` 클로저를 사용할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 잡, 예약된 작업, 느린 쿼리 및 모니터링된 태그가 붙은 데이터만 기록합니다:

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

`filter` 클로저가 개별 항목을 필터링하는 반면, `filterBatch` 메서드는 요청이나 콘솔 명령에 대한 모든 데이터를 필터링하는 클로저를 등록할 수 있습니다. 클로저가 `true`를 반환하면 해당 배치의 모든 항목이 Telescope에 기록됩니다:

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

Telescope는 "태그(tag)"로 항목을 검색할 수 있도록 해줍니다. 태그는 보통 Eloquent 모델 클래스명이나 인증된 사용자 ID일 수 있으며, Telescope가 자동으로 항목에 추가합니다. 가끔은 사용자가 직접 커스텀 태그를 항목에 붙이고 싶을 수 있습니다. 이를 위해 `Telescope::tag` 메서드를 사용할 수 있습니다. 이 메서드는 태그 배열을 반환하는 클로저를 인자로 받으며, 반환된 태그는 Telescope가 자동으로 추가하는 태그와 병합됩니다. 보통 이 `tag` 메서드는 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출합니다:

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
## 사용 가능한 워처(Watchers) (Available Watchers)

Telescope의 "워처"는 요청이나 콘솔 명령 실행 시 애플리케이션 데이터를 수집합니다. 활성화할 워처 목록은 `config/telescope.php` 설정 파일에서 사용자 정의할 수 있습니다:

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

배치 워처는 [배치](/docs/11.x/queues#job-batching)에 관한 정보를 기록하며, 잡 및 연결 정보도 포함합니다.

<a name="cache-watcher"></a>
### 캐시 워처 (Cache Watcher)

캐시 워처는 캐시 키가 조회(hit), 미스(miss), 업데이트 또는 삭제(forget)될 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처 (Command Watcher)

커맨드 워처는 Artisan 명령 실행 시 인수, 옵션, 종료 코드, 출력 내용을 기록합니다. 특정 커맨드를 워처에서 제외하려면 `config/telescope.php` 파일 내 `ignore` 옵션에 해당 커맨드를 지정할 수 있습니다:

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

덤프 워처는 변수 덤프 내용을 기록하고 Telescope에서 보여줍니다. Laravel에서는 전역 `dump` 함수를 사용해 변수를 덤프할 수 있고, 이 워처 탭이 브라우저에서 열려 있어야 덤프가 기록됩니다. 탭이 닫혀 있다면 덤프는 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처 (Event Watcher)

이벤트 워처는 애플리케이션에서 발생하는 [이벤트](/docs/11.x/events)의 페이로드, 리스너, 방송 데이터를 기록합니다. Laravel 프레임워크 내부 이벤트는 이벤트 워처에서 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처 (Exception Watcher)

예외 워처는 애플리케이션에서 발생한 보고 가능한 예외에 대한 데이터 및 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처 (Gate Watcher)

게이트 워처는 애플리케이션에서 실행된 [게이트 및 정책 체크](/docs/11.x/authorization)의 데이터와 결과를 기록합니다. 일부 능력(abilities)을 워처에서 제외하고 싶으면 `config/telescope.php` 파일 내 `ignore_abilities` 옵션에 해당 능력을 지정할 수 있습니다:

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

HTTP 클라이언트 워처는 애플리케이션에서 발생하는 [외부 HTTP 클라이언트 요청](/docs/11.x/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처 (Job Watcher)

잡 워처는 애플리케이션에서 디스패치된 [잡](/docs/11.x/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처 (Log Watcher)

로그 워처는 애플리케이션에서 작성된 [로그 데이터](/docs/11.x/logging)를 기록합니다.

기본적으로 Telescope는 `error` 이상의 로그 레벨만 기록하지만, 설정 파일에서 `level` 옵션을 수정하여 저장할 로그 레벨을 변경할 수 있습니다:

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

메일 워처를 통해 애플리케이션에서 발송된 [이메일](/docs/11.x/mail)을 브라우저에서 미리보기할 수 있으며, 관련 데이터를 함께 확인할 수 있습니다. 또한 이메일을 `.eml` 파일로 다운로드할 수 있습니다.

<a name="model-watcher"></a>
### 모델 워처 (Model Watcher)

모델 워처는 Eloquent [모델 이벤트](/docs/11.x/eloquent#events)가 발생할 때마다 모델 변경사항을 기록합니다. 어떤 모델 이벤트를 기록할지 `events` 옵션으로 지정할 수 있습니다:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

특정 요청 동안 모델이 얼마나 많이 하이드레이션되었는지 기록하려면 `hydrations` 옵션을 활성화할 수 있습니다:

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

알림 워처는 애플리케이션에서 발송된 모든 [알림](/docs/11.x/notifications)을 기록합니다. 알림이 이메일을 트리거하고 메일 워처가 활성화되어 있다면, 메일 워처 화면에서도 해당 이메일을 미리볼 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처 (Query Watcher)

쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원본 SQL, 바인딩 값, 실행 시간을 기록합니다. 또한 100밀리초보다 느린 쿼리에 `slow` 태그를 붙입니다. 느린 쿼리 기준은 설정 파일의 `slow` 옵션으로 조정 가능합니다:

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

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/11.x/redis) 명령을 기록합니다. Redis를 캐시에 사용 중일 경우 캐시 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처 (Request Watcher)

요청 워처는 애플리케이션이 처리하는 요청과 관련된 요청 정보, 헤더, 세션, 응답 데이터를 기록합니다. 응답 데이터 크기는 `size_limit` 옵션(킬로바이트 단위)을 통해 제한할 수 있습니다:

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

스케줄 워처는 애플리케이션에서 실행하는 [예약된 작업](/docs/11.x/scheduling)의 명령어와 출력 결과를 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처 (View Watcher)

뷰 워처는 [뷰](/docs/11.x/views)의 이름, 경로, 데이터, 그리고 뷰 렌더링 시 사용된 "composer"들을 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시 (Displaying User Avatars)

Telescope 대시보드는 특정 항목이 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 그러나 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 커스터마이징할 수 있습니다. 이 콜백은 사용자 ID와 이메일을 받아 사용자 아바타 이미지 URL을 반환해야 합니다:

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