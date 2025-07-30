# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 권한](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리 필터링](#filtering-entries)
    - [배치 필터링](#filtering-batches)
- [태깅](#tagging)
- [사용 가능한 감시자](#available-watchers)
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

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에 훌륭한 동반자가 되어 줍니다. Telescope는 애플리케이션으로 들어오는 요청, 예외, 로그 항목, 데이터베이스 쿼리, 큐에 쌓인 작업, 메일, 알림, 캐시 작업, 예약 작업, 변수 덤프 등 다양한 정보를 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치 (Installation)

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후에는 `telescope:install` Artisan 명령어를 사용해 관련 자산과 마이그레이션 파일을 배포해야 합니다. 그리고 Telescope 데이터를 저장하기 위한 테이블 생성을 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로 `/telescope` 경로를 통해 Telescope 대시보드에 접속할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치 (Local Only Installation)

Telescope를 로컬 개발 지원 용도로만 사용하려면 `--dev` 플래그를 붙여 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후에는 애플리케이션의 `bootstrap/providers.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 수동으로 Telescope 서비스 프로바이더를 등록하세요. 현재 환경이 `local`인 경우에만 등록하도록 처리합니다:

```php
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

마지막으로, Telescope 패키지가 [자동 발견(auto-discovery)](/docs/12.x/packages#package-discovery)되지 않도록 `composer.json` 파일에 아래 내용을 추가하여 비활성화해야 합니다:

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

Telescope 자산을 배포하면 주 설정 파일이 `config/telescope.php`에 생성됩니다. 이 설정 파일에서는 [감시자(watcher) 옵션](#available-watchers)을 구성할 수 있으며, 각 설정 항목에는 용도가 설명되어 있으니 자세히 살펴보세요.

필요에 따라 `enabled` 설정 옵션으로 Telescope 데이터 수집을 완전히 비활성화할 수도 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리 (Data Pruning)

데이터 정리를 하지 않으면 `telescope_entries` 테이블에 데이터가 급속도로 쌓일 수 있습니다. 이를 방지하기 위해 `telescope:prune` Artisan 명령어를 매일 [스케줄](/docs/12.x/scheduling)하여 실행하도록 설정하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

기본적으로 24시간이 지난 모든 데이터는 삭제됩니다. 명령어 실행 시 `hours` 옵션을 사용하여 데이터 보존 기간을 지정할 수도 있습니다. 예를 들어, 아래 명령어는 48시간이 지난 모든 데이터를 삭제합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 권한 (Dashboard Authorization)

Telescope 대시보드에 접속하려면 `/telescope` 경로로 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용됩니다. `app/Providers/TelescopeServiceProvider.php` 파일 내에 [인가 게이트](/docs/12.x/authorization#gates) 정의가 있습니다. 이 게이트는 **local이 아닌 환경**에서 Telescope 접근 권한을 관리합니다. 필요에 따라 이 게이트를 수정해 Telescope 설치에 대한 접근을 제한할 수 있습니다:

```php
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
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
> 프로덕션 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 설정해야 합니다. 그렇지 않으면 Telescope가 공개적으로 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드 (Upgrading Telescope)

Telescope의 주요 버전 업그레이드 시에는 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

또한 새로운 Telescope 버전으로 업그레이드할 때마다 Telescope 자산을 다시 배포해야 합니다:

```shell
php artisan telescope:publish
```

자산을 최신 상태로 유지하고 앞으로 발생할 수 있는 문제를 예방하려면 `composer.json` 파일 내 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령을 추가하는 것도 좋습니다:

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

`App\Providers\TelescopeServiceProvider` 클래스에 정의된 `filter` 클로저를 사용해 Telescope가 기록할 데이터를 필터링할 수 있습니다. 기본 설정은 `local` 환경에서 모든 데이터를 기록하며, 그 외 환경에서는 예외, 실패한 작업, 예약된 작업, 느린 쿼리, 그리고 모니터링 중인 태그가 붙은 데이터만 기록합니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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

`filter` 클로저가 개별 엔트리 단위로 데이터를 필터링하는 반면, `filterBatch` 메서드는 주어진 요청이나 콘솔 커맨드에 따른 모든 데이터를 함께 필터링하는 클로저를 등록합니다. 클로저가 `true`를 반환하면 해당 배치에 포함된 모든 엔트리가 Telescope에 기록됩니다:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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

Telescope는 "태그"를 통해 엔트리를 검색할 수 있게 해 줍니다. 보통 태그는 Eloquent 모델 클래스명이나 인증된 사용자 ID이며, Telescope는 기본적으로 엔트리에 이런 태그를 자동으로 추가합니다. 사용자 정의 태그를 엔트리에 붙이고 싶을 때는 `Telescope::tag` 메서드를 사용할 수 있습니다. 이 메서드는 태그 배열을 반환하는 클로저를 받으며, 클로저가 반환하는 태그는 Telescope가 자동으로 붙이는 태그에 병합되어 저장됩니다. 보통 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출합니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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
## 사용 가능한 감시자 (Available Watchers)

Telescope의 "감시자(watchers)"는 요청이나 콘솔 커맨드 실행 시 애플리케이션 데이터를 수집합니다. 원하는 감시자 목록은 `config/telescope.php` 설정 파일에서 조정할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

일부 감시자는 추가 설정 옵션을 제공하기도 합니다:

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
### 배치 감시자 (Batch Watcher)

배치 감시자는 큐에 쌓인 [배치 작업](/docs/12.x/queues#job-batching)에 관한 정보, 즉 작업과 연결(connection) 정보를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 감시자 (Cache Watcher)

캐시 감시자는 캐시 키가 적중(hit), 미스(miss), 갱신, 삭제될 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 감시자 (Command Watcher)

커맨드 감시자는 Artisan 명령어가 실행될 때 인수, 옵션, 종료 코드, 출력 내용 등을 기록합니다. 특정 명령어를 기록 대상에서 제외하고 싶으면 `config/telescope.php`의 `ignore` 옵션에 명령어를 지정하세요:

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
### 덤프 감시자 (Dump Watcher)

덤프 감시자는 변수 덤프 결과를 Telescope에서 기록하고 표시합니다. Laravel에서는 글로벌 `dump` 함수를 사용해 변수를 덤프할 수 있습니다. 단, 브라우저에서 덤프 감시자 탭이 열려 있을 때만 덤프가 기록되며, 그렇지 않으면 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 감시자 (Event Watcher)

이벤트 감시자는 애플리케이션에서 디스패치한 [이벤트](/docs/12.x/events)의 페이로드, 리스너, 방송 데이터를 기록합니다. Laravel 내부 이벤트는 이벤트 감시자에 의해 무시됩니다.

<a name="exception-watcher"></a>
### 예외 감시자 (Exception Watcher)

예외 감시자는 애플리케이션에서 발생한 보고 대상 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 감시자 (Gate Watcher)

게이트 감시자는 애플리케이션에서 수행하는 [게이트와 정책](/docs/12.x/authorization) 체크의 결과와 데이터를 기록합니다. 기록에서 특정 권한(ability)을 제외하고 싶으면 `config/telescope.php`의 `ignore_abilities` 옵션에 제외할 권한명을 지정하세요:

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
### HTTP 클라이언트 감시자 (HTTP Client Watcher)

HTTP 클라이언트 감시자는 애플리케이션에서 실행하는 [HTTP 클라이언트 요청](/docs/12.x/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 감시자 (Job Watcher)

잡 감시자는 애플리케이션에서 디스패치한 [잡](/docs/12.x/queues)의 데이터 및 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 감시자 (Log Watcher)

로그 감시자는 애플리케이션에서 작성한 [로그 데이터](/docs/12.x/logging)를 기록합니다.

기본값으로는 `error` 레벨 이상 로그만 기록하지만, `config/telescope.php`의 `level` 옵션을 조정해 다른 로그 레벨로 변경할 수 있습니다:

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
### 메일 감시자 (Mail Watcher)

메일 감시자는 애플리케이션에서 발송한 [이메일](/docs/12.x/mail)을 브라우저 내에서 미리보기하며, 관련 데이터도 보여줍니다. `.eml` 파일로 이메일을 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 감시자 (Model Watcher)

모델 감시자는 Eloquent [모델 이벤트](/docs/12.x/eloquent#events)가 발생할 때마다 모델 변경 사항을 기록합니다. 어떤 모델 이벤트를 기록할지 `events` 옵션에서 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

요청 시 수화(hydration)된 모델 수를 기록하려면 `hydrations` 옵션을 활성화하세요:

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
### 알림 감시자 (Notification Watcher)

알림 감시자는 애플리케이션에서 전송한 모든 [알림](/docs/12.x/notifications)을 기록합니다. 알림과 함께 이메일이 발송되고 메일 감시자가 활성화되어 있으면, 해당 이메일도 메일 감시자 화면에서 미리 보기 가능합니다.

<a name="query-watcher"></a>
### 쿼리 감시자 (Query Watcher)

쿼리 감시자는 실행된 모든 쿼리의 원본 SQL, 바인딩 값, 실행 시간을 기록합니다. 느린 쿼리를 자동으로 `slow` 태그로 표시하며, 기본 임계값은 100밀리초입니다. `slow` 옵션을 조정해 느린 쿼리 임계값을 변경할 수 있습니다:

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
### Redis 감시자 (Redis Watcher)

Redis 감시자는 애플리케이션에서 실행된 모든 [Redis](/docs/12.x/redis) 명령어를 기록합니다. Redis 캐시를 사용하는 경우 캐시 명령도 Redis 감시자에 의해 기록됩니다.

<a name="request-watcher"></a>
### 요청 감시자 (Request Watcher)

요청 감시자는 애플리케이션이 처리한 모든 요청에서 요청 정보, 헤더, 세션, 응답 데이터를 기록합니다. `size_limit` 옵션(킬로바이트 단위)을 사용해 기록할 응답 데이터 크기를 제한할 수 있습니다:

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
### 스케줄 감시자 (Schedule Watcher)

스케줄 감시자는 애플리케이션에서 실행하는 [예약 작업](/docs/12.x/scheduling)의 명령과 출력 결과를 기록합니다.

<a name="view-watcher"></a>
### 뷰 감시자 (View Watcher)

뷰 감시자는 뷰 렌더링 시 사용되는 [뷰](/docs/12.x/views)의 이름, 경로, 데이터, 그리고 "컴포저"를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시 (Displaying User Avatars)

Telescope 대시보드에서는 해당 엔트리가 저장될 때 인증된 사용자의 아바타를 보여줍니다. 기본적으로는 Gravatar 웹 서비스를 통해 아바타를 가져오지만, `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 직접 지정할 수도 있습니다. 콜백은 사용자 ID와 이메일 주소를 받아 사용자의 아바타 이미지 URL을 반환해야 합니다:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (?string $id, ?string $email) {
        return ! is_null($id)
            ? '/avatars/'.User::find($id)->avatar_path
            : '/generic-avatar.jpg';
    });
}
```