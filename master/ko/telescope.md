# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 접근 권한 설정](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리 필터링](#filtering-entries)
    - [배치 필터링](#filtering-batches)
- [태그 지정](#tagging)
- [사용 가능한 워처 목록](#available-watchers)
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
    - [레디스 워처](#redis-watcher)
    - [요청 워처](#request-watcher)
    - [스케줄 워처](#schedule-watcher)
    - [뷰 워처](#view-watcher)
- [사용자 아바타 표시](#displaying-user-avatars)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에서 매우 유용한 동반자 역할을 합니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 항목, 데이터베이스 쿼리, 대기열 작업, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 상세히 제공해 줍니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치 (Installation)

Composer 패키지 매니저를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후에는 `telescope:install` Artisan 명령어를 사용하여 자산과 마이그레이션 파일을 퍼블리시해야 합니다. 또한, Telescope 데이터를 저장할 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로 `/telescope` 경로로 접속하여 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치 (Local Only Installation)

Telescope를 로컬 개발 환경에서만 사용하려면 `--dev` 플래그를 사용해 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후에는 애플리케이션의 `bootstrap/providers.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 Telescope 서비스 프로바이더들을 수동으로 등록할 수 있습니다. 이때, 현재 환경이 `local`인지 확인한 후 등록하도록 해야 합니다:

```php
/**
 * 애플리케이션 서비스 등록.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

마지막으로, Telescope 패키지가 [자동 발견](/docs/master/packages#package-discovery)되지 않도록 `composer.json` 파일에 아래 내용을 추가해야 합니다:

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

Telescope 자산을 퍼블리시한 후 기본 설정 파일은 `config/telescope.php`에 위치합니다. 이 설정 파일에서는 [워처 옵션](#available-watchers)을 구성할 수 있으며, 각 옵션에는 해당 설정의 목적이 설명되어 있으니 자세히 살펴보세요.

원한다면, `enabled` 설정을 통해 Telescope의 데이터 수집을 완전히 비활성화할 수도 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리 (Data Pruning)

데이터 정리 없이 `telescope_entries` 테이블은 매우 빠르게 데이터가 쌓일 수 있습니다. 이를 방지하기 위해 `telescope:prune` Artisan 명령어를 매일 [스케줄링](/docs/master/scheduling)하는 것이 좋습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

기본적으로, 24시간 이상 된 모든 엔트리를 정리합니다. `--hours` 옵션을 사용해 보관 기간을 조정할 수 있습니다. 예를 들어 아래 명령은 48시간 이전의 모든 레코드를 삭제합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 접근 권한 설정 (Dashboard Authorization)

Telescope 대시보드는 `/telescope` 경로로 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 접근할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일에는 [인가 게이트](/docs/master/authorization#gates) 정의가 포함되어 있습니다. 이 게이트는 **비로컬 환경**에서 Telescope 접근 제어를 담당합니다. 필요에 따라 이 게이트를 수정해 Telescope 접근 권한을 제한할 수 있습니다:

```php
use App\Models\User;

/**
 * Telescope 게이트 등록.
 *
 * 이 게이트는 비로컬 환경에서 Telescope 접근 권한을 결정합니다.
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
> 프로덕션 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 설정해야 합니다. 그렇지 않으면 Telescope 설치가 공개적으로 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드 (Upgrading Telescope)

새로운 주요 버전의 Telescope로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하는 것이 중요합니다.

또한, 모든 새로운 Telescope 버전으로 업그레이드할 때마다 Telescope 자산을 다시 퍼블리시해야 합니다:

```shell
php artisan telescope:publish
```

향후 업데이트 시 자산 문제를 방지하고 최신 상태를 유지하려면, 애플리케이션의 `composer.json` 파일 내 `post-update-cmd` 스크립트에 아래 명령을 추가할 수 있습니다:

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

Telescope가 기록하는 데이터를 `App\Providers\TelescopeServiceProvider` 클래스 내에 정의된 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 작업, 예약된 작업, 느린 쿼리, 모니터링 태그가 포함된 데이터만 기록합니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스 등록.
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

`filter` 클로저는 개별 엔트리를 필터링하지만, `filterBatch` 메서드를 사용하면 요청이나 콘솔 명령에 해당하는 모든 데이터를 필터링하는 클로저를 등록할 수 있습니다. 클로저 반환값이 `true`이면 해당 요청에 포함된 모든 엔트리가 Telescope에 기록됩니다:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스 등록.
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
## 태그 지정 (Tagging)

Telescope는 "태그"를 이용해 엔트리를 검색할 수 있게 합니다. 태그는 종종 Eloquent 모델 클래스명이나 인증된 사용자 ID이며, Telescope가 엔트리에 자동으로 추가합니다. 때로는 직접 커스텀 태그를 엔트리에 추가하고 싶을 수 있습니다. 이럴 때는 `Telescope::tag` 메서드를 사용할 수 있습니다. 이 메서드는 태그의 배열을 반환하는 클로저를 인자로 받고, 반환된 태그들은 Telescope가 자동으로 붙이는 태그와 병합됩니다. 일반적으로 이 `tag` 메서드는 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출됩니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스 등록.
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
## 사용 가능한 워처 목록 (Available Watchers)

Telescope "워처"는 요청이나 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. `config/telescope.php` 설정 파일에서 활성화할 워처 목록을 커스터마이징할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

일부 워처는 추가 설정 옵션을 제공하기도 합니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    // ...
],
```

<a name="batch-watcher"></a>
### 배치 워처 (Batch Watcher)

배치 워처는 대기열 [배치](/docs/master/queues#job-batching)에 대한 정보, 즉 작업 및 연결 정보를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처 (Cache Watcher)

캐시 워처는 캐시 키가 적중(hit), 미스(miss), 갱신, 삭제(forget)될 때의 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처 (Command Watcher)

커맨드 워처는 Artisan 명령어가 실행될 때 인수, 옵션, 종료 코드, 출력 데이터를 기록합니다. 특정 명령어를 제외하고 싶으면 `config/telescope.php` 파일 내의 `ignore` 옵션에 해당 명령어를 명시할 수 있습니다:

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    // ...
],
```

<a name="dump-watcher"></a>
### 덤프 워처 (Dump Watcher)

덤프 워처는 변수 덤프를 기록하고 Telescope 내에서 표시합니다. Laravel에서는 전역 `dump` 함수를 통해 변수를 덤프할 수 있습니다. 이 워처가 기록하려면 브라우저에서 덤프 워처 탭이 열려 있어야 하며, 그렇지 않으면 덤프가 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처 (Event Watcher)

이벤트 워처는 애플리케이션에서 발생하는 모든 [이벤트](/docs/master/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. 단, Laravel 프레임워크 내부 이벤트는 이 워처에서 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처 (Exception Watcher)

예외 워처는 애플리케이션에서 발생하는 보고 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처 (Gate Watcher)

게이트 워처는 애플리케이션의 [게이트 및 정책](/docs/master/authorization) 검증 데이터와 결과를 기록합니다. 특정 능력(abilities)을 기록에서 제외하고 싶다면 `config/telescope.php`에서 `ignore_abilities` 옵션에 해당 능력들을 명시할 수 있습니다:

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    // ...
],
```

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처 (HTTP Client Watcher)

HTTP 클라이언트 워처는 애플리케이션에서 발생하는 외부 [HTTP 클라이언트 요청](/docs/master/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처 (Job Watcher)

잡 워처는 애플리케이션에서 디스패치되는 모든 [잡](/docs/master/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처 (Log Watcher)

로그 워처는 애플리케이션에서 작성되는 [로그 데이터](/docs/master/logging)를 기록합니다.

기본적으로는 error 레벨 이상의 로그만 기록하지만, `config/telescope.php` 내 `level` 옵션을 수정해 동작을 바꿀 수 있습니다:

```php
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

메일 워처는 애플리케이션에서 전송된 [이메일](/docs/master/mail)을 브라우저 내에서 미리 볼 수 있게 해줍니다. 관련 메일 데이터도 함께 확인 가능하며, `.eml` 파일로도 다운로드할 수 있습니다.

<a name="model-watcher"></a>
### 모델 워처 (Model Watcher)

모델 워처는 Eloquent [모델 이벤트](/docs/master/eloquent#events)가 발생할 때마다 모델 변경사항을 기록합니다. 어떤 모델 이벤트를 기록할지 watcher's `events` 옵션에 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

요청 내에서 하이드레이션된 모델 수를 기록하려면 `hydrations` 옵션을 활성화하세요:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    // ...
],
```

<a name="notification-watcher"></a>
### 알림 워처 (Notification Watcher)

알림 워처는 애플리케이션에서 전송된 모든 [알림](/docs/master/notifications)을 기록합니다. 만약 알림이 메일을 발송하고 메일 워처도 활성화되어 있다면, 메일 워처 화면에서 해당 이메일 미리보기도 확인할 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처 (Query Watcher)

쿼리 워처는 애플리케이션에서 실행된 쿼리의 원본 SQL, 바인딩된 값, 실행 시간을 기록합니다. 실행 시간이 100밀리초를 초과하는 쿼리는 `slow` 태그가 붙습니다. 느린 쿼리 임계값은 watcher's `slow` 옵션으로 조절할 수 있습니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    // ...
],
```

<a name="redis-watcher"></a>
### 레디스 워처 (Redis Watcher)

레디스 워처는 애플리케이션에서 실행되는 모든 [Redis](/docs/master/redis) 명령어를 기록합니다. 캐시로 Redis를 사용하는 경우 캐시 명령도 이 워처에 의해 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처 (Request Watcher)

요청 워처는 애플리케이션이 처리하는 요청과 관련된 요청 본문, 헤더, 세션, 응답 데이터를 기록합니다. 응답 데이터 용량은 `size_limit` (킬로바이트 단위) 옵션으로 제한할 수 있습니다:

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    // ...
],
```

<a name="schedule-watcher"></a>
### 스케줄 워처 (Schedule Watcher)

스케줄 워처는 애플리케이션에서 실행되는 모든 [예약 작업](/docs/master/scheduling)의 명령어와 출력 결과를 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처 (View Watcher)

뷰 워처는 뷰를 렌더링할 때 사용된 [뷰](/docs/master/views)의 이름, 경로, 전달된 데이터, 뷰 "컴포저"를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시 (Displaying User Avatars)

Telescope 대시보드는 주어진 엔트리가 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 하지만 `App\Providers\TelescopeServiceProvider` 클래스 내에 콜백을 등록하여 아바타 URL을 커스터마이징할 수 있습니다. 콜백은 사용자의 ID와 이메일 주소를 인자로 받아 해당 사용자의 아바타 이미지 URL을 반환해야 합니다:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * 애플리케이션 서비스 등록.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (string $id, string $email) {
        return '/avatars/'.User::find($id)->avatar_path;
    });
}
```