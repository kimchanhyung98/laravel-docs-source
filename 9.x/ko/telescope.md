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
- [사용 가능한 감시자(Watchers)](#available-watchers)
    - [배치 감시자](#batch-watcher)
    - [캐시 감시자](#cache-watcher)
    - [커맨드 감시자](#command-watcher)
    - [덤프 감시자](#dump-watcher)
    - [이벤트 감시자](#event-watcher)
    - [예외 감시자](#exception-watcher)
    - [게이트 감시자](#gate-watcher)
    - [HTTP 클라이언트 감시자](#http-client-watcher)
    - [잡 감시자](#job-watcher)
    - [로그 감시자](#log-watcher)
    - [메일 감시자](#mail-watcher)
    - [모델 감시자](#model-watcher)
    - [알림 감시자](#notification-watcher)
    - [쿼리 감시자](#query-watcher)
    - [Redis 감시자](#redis-watcher)
    - [요청 감시자](#request-watcher)
    - [스케줄 감시자](#schedule-watcher)
    - [뷰 감시자](#view-watcher)
- [사용자 아바타 표시](#displaying-user-avatars)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에 매우 유용한 도구입니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 기록, 데이터베이스 쿼리, 대기열 작업, 메일, 알림, 캐시 작업, 예약 작업, 변수 덤프 등 다양한 정보를 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치 (Installation)

Telescope를 Laravel 프로젝트에 설치하려면 Composer 패키지 관리자를 사용할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후, `telescope:install` Artisan 명령어로 관련 자산을 배포하세요. 또한 Telescope 데이터를 저장할 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징

Telescope 기본 마이그레이션을 사용하지 않을 경우, 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Telescope::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션을 내보내려면 다음 명령어를 사용할 수 있습니다: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### 로컬 전용 설치 (Local Only Installation)

Telescope를 로컬 개발에만 사용하려면 `--dev` 플래그를 이용해 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후, `config/app.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거하고, 대신 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 수동으로 Telescope 서비스 프로바이더를 등록해야 합니다. 등록 시 현재 환경이 `local`인지 확인하도록 합니다:

```
/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
{
    if ($this->app->environment('local')) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

마지막으로, `composer.json` 파일에 다음 설정을 추가하여 Telescope 패키지가 [자동 발견](/docs/9.x/packages#package-discovery)되지 않도록 해야 합니다:

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

Telescope 자산을 퍼블리시하면 기본 설정 파일은 `config/telescope.php`에 위치하게 됩니다. 이 설정 파일에서 [감시자 설정](#available-watchers)을 지정할 수 있으며, 각 옵션에는 용도에 대한 설명이 포함되어 있으니 꼼꼼히 살펴보세요.

원한다면 `enabled` 설정 옵션을 사용해 Telescope의 데이터 수집을 완전히 비활성화할 수도 있습니다:

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리 (Data Pruning)

정리 없이 데이터를 계속 쌓으면 `telescope_entries` 테이블의 기록이 빠르게 증가할 수 있습니다. 이를 방지하기 위해 [스케줄링](/docs/9.x/scheduling) 기능을 사용하여 `telescope:prune` Artisan 명령어를 매일 실행하도록 설정하는 것이 좋습니다:

```
$schedule->command('telescope:prune')->daily();
```

기본적으로 24시간 이상된 모든 기록이 정리됩니다. `hours` 옵션을 명령어에 지정하여 데이터를 보관할 시간을 조정할 수 있습니다. 예를 들어, 48시간 이상 된 기록들을 삭제하려면 다음과 같이 설정합니다:

```
$schedule->command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Telescope 대시보드는 기본적으로 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용됩니다. `app/Providers/TelescopeServiceProvider.php` 파일 내에는 [인가 게이트](/docs/9.x/authorization#gates) 정의가 존재하며, 이 게이트는 **비로컬 환경**에서 Telescope 접근을 제어합니다. 필요에 따라 이 게이트를 수정하여 Telescope 접속을 제한할 수 있습니다:

```
/**
 * Telescope 접근 권한을 등록합니다.
 *
 * 이 게이트는 비로컬 환경에서 Telescope 접속 권한을 결정합니다.
 *
 * @return void
 */
protected function gate()
{
    Gate::define('viewTelescope', function ($user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]
> 운영 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 설정하여야 합니다. 그렇지 않으면 Telescope 대시보드가 공개되어 외부에 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드 (Upgrading Telescope)

Telescope의 새 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 자세히 확인해야 합니다.

또한, Telescope 버전을 업데이트할 때는 반드시 관련 자산을 다시 배포해야 합니다:

```shell
php artisan telescope:publish
```

앞으로의 업데이트에도 최신 자산을 유지하려면 애플리케이션의 `composer.json` 파일 내 `post-update-cmd` 스크립트에 다음 명령어를 추가해 자동으로 배포하도록 할 수 있습니다:

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

`filter` 클로저를 `App\Providers\TelescopeServiceProvider` 클래스 내에 정의하여 Telescope가 기록하는 데이터를 필터링할 수 있습니다. 기본 설정은 `local` 환경에서 모든 데이터를 기록하며, 그 외 환경에서는 예외, 실패한 잡, 예약 작업, 느린 쿼리, 그리고 모니터링 태그가 달린 데이터만 기록합니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
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

`filter` 클로저는 개별 엔트리를 필터링하지만, `filterBatch` 메서드는 요청이나 콘솔 명령어 단위로 전체 데이터를 필터링할 수 있습니다. 클로저가 `true`를 반환하면 해당 배치에 포함된 모든 엔트리가 Telescope에 기록됩니다:

```
use Illuminate\Support\Collection;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function ($entry) {
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

Telescope는 "태그"를 이용해 엔트리를 검색할 수 있습니다. 보통 태그는 Eloquent 모델 클래스 이름이나 인증된 사용자 ID이며 Telescope가 자동으로 엔트리에 붙입니다. 경우에 따라 사용자 정의 태그를 엔트리에 추가하고 싶을 때는 `Telescope::tag` 메서드를 사용할 수 있습니다. 이 메서드는 태그 배열을 반환하는 클로저를 인수로 받으며, 클로저에서 반환된 태그는 Telescope가 자동으로 붙이는 태그와 합쳐집니다. 일반적으로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출합니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
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
## 사용 가능한 감시자(Watchers) (Available Watchers)

Telescope의 "watcher"는 요청이나 콘솔 명령 실행 시 애플리케이션 데이터를 수집합니다. `config/telescope.php` 설정 파일에서 활성화할 감시자 목록과 옵션을 지정할 수 있습니다:

```
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    ...
],
```

일부 감시자는 추가 커스터마이징 옵션도 지원합니다:

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
### 배치 감시자 (Batch Watcher)

배치 감시자는 대기열 [배치](/docs/9.x/queues#job-batching)에 관한 잡 및 연결 정보를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 감시자 (Cache Watcher)

캐시 감시자는 캐시 키가 조회(hit), 실패(miss), 갱신, 삭제될 때의 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 감시자 (Command Watcher)

커맨드 감시자는 Artisan 명령 실행 시 인수, 옵션, 종료 코드, 출력 정보를 기록합니다. 특정 명령을 감시 대상에서 제외하려면 `config/telescope.php` 파일의 `ignore` 옵션에 해당 명령을 명시하세요:

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
### 덤프 감시자 (Dump Watcher)

덤프 감시자는 변수 덤프를 기록하고 Telescope에 표시합니다. Laravel의 글로벌 `dump` 함수를 사용하여 변수를 덤프할 수 있습니다. 단, 덤프 감시자 탭이 브라우저에서 열려 있어야 덤프가 기록되며, 그렇지 않으면 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 감시자 (Event Watcher)

이벤트 감시자는 애플리케이션에서 발생하는 [이벤트](/docs/9.x/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. Laravel 내부 이벤트는 감시 대상에서 제외됩니다.

<a name="exception-watcher"></a>
### 예외 감시자 (Exception Watcher)

예외 감시자는 애플리케이션에서 발생하는 보고 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 감시자 (Gate Watcher)

게이트 감시자는 애플리케이션의 [게이트 및 정책](/docs/9.x/authorization) 검사 데이터와 결과를 기록합니다. 특정 능력(ability)을 감시 대상에서 제외하려면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 능력을 명시할 수 있습니다:

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
### HTTP 클라이언트 감시자 (HTTP Client Watcher)

HTTP 클라이언트 감시자는 애플리케이션에서 발생하는 아웃바운드 [HTTP 클라이언트 요청](/docs/9.x/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 감시자 (Job Watcher)

잡 감시자는 애플리케이션에서 발생하는 모든 [잡](/docs/9.x/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 감시자 (Log Watcher)

로그 감시자는 애플리케이션에서 작성한 [로그 데이터](/docs/9.x/logging)를 기록합니다.

<a name="mail-watcher"></a>
### 메일 감시자 (Mail Watcher)

메일 감시자는 애플리케이션에서 발송된 [이메일](/docs/9.x/mail)을 브라우저 내에서 미리보기할 수 있게 하며, 관련 데이터도 함께 보여줍니다. `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 감시자 (Model Watcher)

모델 감시자는 Eloquent [모델 이벤트](/docs/9.x/eloquent#events)가 발생할 때마다 모델 변경 사항을 기록합니다. 감시할 모델 이벤트는 감시자의 `events` 옵션으로 지정할 수 있습니다:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

요청 시 모델이 하이드레이션(hydration)된 개수를 기록하고 싶다면, `hydrations` 옵션을 활성화하세요:

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
### 알림 감시자 (Notification Watcher)

알림 감시자는 애플리케이션에서 발송된 모든 [알림](/docs/9.x/notifications)을 기록합니다. 만약 알림에 이메일이 포함되어 있고 메일 감시자가 활성화되어 있다면, 해당 이메일은 메일 감시자 화면에서도 미리보기할 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 감시자 (Query Watcher)

쿼리 감시자는 애플리케이션에서 실행되는 모든 쿼리의 원본 SQL, 바인딩, 실행 시간을 기록합니다. 100밀리초를 초과하는 느린 쿼리는 자동으로 `slow` 태그가 붙습니다. 느린 쿼리 기준 시간은 `slow` 옵션으로 조절할 수 있습니다:

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
### Redis 감시자 (Redis Watcher)

Redis 감시자는 애플리케이션에서 실행되는 모든 [Redis](/docs/9.x/redis) 명령을 기록합니다. Redis를 캐시로 사용하는 경우 캐시 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 감시자 (Request Watcher)

요청 감시자는 애플리케이션이 처리하는 모든 요청의 요청 정보, 헤더, 세션, 응답 데이터를 기록합니다. `size_limit`(킬로바이트 단위) 옵션을 통해 기록할 응답 데이터 크기를 제한할 수 있습니다:

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
### 스케줄 감시자 (Schedule Watcher)

스케줄 감시자는 애플리케이션에서 실행된 모든 [예약 작업](/docs/9.x/scheduling)의 명령과 출력 결과를 기록합니다.

<a name="view-watcher"></a>
### 뷰 감시자 (View Watcher)

뷰 감시자는 뷰 [뷰](/docs/9.x/views)의 이름, 경로, 데이터, 그리고 뷰 컴포저(view composers)를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시 (Displaying User Avatars)

Telescope 대시보드는 각 엔트리 기록 시 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 그러나 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 직접 지정할 수 있습니다. 콜백은 사용자 ID와 이메일을 인수로 받아 사용자 아바타 이미지 URL을 반환해야 합니다:

```
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function register()
{
    // ...

    Telescope::avatar(function ($id, $email) {
        return '/avatars/'.User::find($id)->avatar_path;
    });
}
```