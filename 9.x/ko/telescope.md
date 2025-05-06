# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 인증](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [항목](#filtering-entries)
    - [배치](#filtering-batches)
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
## 소개

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에서 훌륭한 동반자가 되어줍니다. Telescope는 애플리케이션으로 들어오는 요청, 예외, 로그 항목, 데이터베이스 쿼리, 큐에 등록된 작업(잡), 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 확인할 수 있도록 지원합니다.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후, `telescope:install` Artisan 명령어로 에셋을 게시해야 합니다. 또한, Telescope 데이터를 저장할 테이블 생성을 위해 `migrate` 명령어도 실행해 주세요:

```shell
php artisan telescope:install

php artisan migrate
```

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이즈

Telescope의 기본 마이그레이션을 사용하지 않을 경우, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메소드에서 `Telescope::ignoreMigrations` 메소드를 호출해야 합니다. 기본 마이그레이션 파일을 내보내려면 다음 명령어를 사용하세요:
`php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### 로컬 전용 설치

Telescope를 로컬 개발 지원용으로만 사용하려면, `--dev` 플래그를 사용해 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후에는, 애플리케이션의 `config/app.php` 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거하세요. 대신 `App\Providers\AppServiceProvider` 클래스의 `register` 메소드에서 직접 Telescope의 서비스 프로바이더를 등록합니다. 현재 환경이 `local`인지 확인 후 프로바이더를 등록합니다:

```php
/**
 * Register any application services.
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

마지막으로, 아래와 같이 `composer.json` 파일에 추가하여 Telescope 패키지가 [자동으로 탐지되지 않도록](/docs/{{version}}/packages#package-discovery) 해야 합니다:

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
### 설정

Telescope의 에셋을 게시하면, 주요 설정 파일은 `config/telescope.php`에 위치하게 됩니다. 이 설정 파일에서는 [워처 옵션](#available-watchers)을 설정할 수 있습니다. 각 설정 옵션에는 그 목적에 대한 설명이 포함되어 있으니, 이 파일을 꼼꼼히 확인해보시기 바랍니다.

원한다면 `enabled` 설정 옵션을 통해 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리

정리를 하지 않을 경우, `telescope_entries` 테이블에는 레코드가 빠르게 누적될 수 있습니다. 이를 방지하기 위해 [스케줄러](/docs/{{version}}/scheduling)에 `telescope:prune` Artisan 명령어를 등록하여 매일 실행하도록 하세요:

```php
$schedule->command('telescope:prune')->daily();
```

기본적으로 24시간이 지난 모든 항목이 정리됩니다. `hours` 옵션을 사용하여 Telescope 데이터를 보관할 시간을 설정할 수 있습니다. 예를 들어, 아래 명령어는 생성된 지 48시간이 지난 모든 레코드를 삭제합니다:

```php
$schedule->command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 인증

Telescope 대시보드는 기본적으로 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 대시보드에 접근할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일 내에는 [인증 게이트](/docs/{{version}}/authorization#gates) 정의가 있습니다. 이 게이트는 **비로컬** 환경에서 Telescope 접근을 제어합니다. 필요하다면 이 게이트를 수정하여 Telescope 접근 권한을 설정할 수 있습니다:

```php
/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
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

> **경고**
> 운영환경에서는 `APP_ENV` 환경 변수를 반드시 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope 인스톨이 외부에 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 새 주요 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼하게 확인해야 합니다.

또한, Telescope의 새로운 버전으로 업그레이드할 때마다 Telescope의 에셋을 다시 게시해야 합니다:

```shell
php artisan telescope:publish
```

최신 상태를 유지하고 추후 발생할 수 있는 문제를 방지하기 위해, 애플리케이션의 `composer.json` 파일에 다음과 같이 `vendor:publish --tag=laravel-assets` 명령어를 `post-update-cmd` 스크립트에 추가할 수 있습니다:

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
## 필터링

<a name="filtering-entries"></a>
### 항목

Telescope에 기록되는 데이터는 `App\Providers\TelescopeServiceProvider` 클래스의 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경의 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 작업, 예약된 작업, 모니터링 태그가 있는 데이터만 기록합니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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
### 배치

`filter` 클로저가 개별 항목을 필터링하는 반면, `filterBatch` 메서드를 통해 요청 또는 콘솔 명령에 대한 모든 데이터를 필터링하는 클로저를 등록할 수 있습니다. 클로저가 `true`를 반환하면 모든 항목이 Telescope에 기록됩니다:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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
## 태깅

Telescope는 "태그"를 이용해 항목을 검색할 수 있습니다. 보통 태그는 Eloquent 모델 클래스명이나 인증된 사용자 ID 등이며, Telescope에서 자동으로 항목에 추가합니다. 필요하다면 직접 커스텀 태그를 항목에 붙일 수도 있습니다. 이를 위해 `Telescope::tag` 메서드를 사용할 수 있으며, 클로저는 태그 배열을 반환해야 합니다. 해당 태그는 Telescope가 자동으로 붙이는 태그와 합쳐집니다. `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출하는 것이 일반적입니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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
## 사용 가능한 워처

Telescope의 "워처"들은 요청 또는 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. `config/telescope.php` 설정 파일 내에서 활성화할 워처 목록을 커스터마이즈할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    ...
],
```

일부 워처는 추가 옵션도 지원합니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    ...
],
```

<a name="batch-watcher"></a>
### 배치 워처

배치 워처는 큐에 등록된 [배치 작업](/docs/{{version}}/queues#job-batching)에 대한 작업 및 연결 정보를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키가 히트, 미스, 업데이트, 삭제될 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처

커맨드 워처는 Artisan 명령이 실행될 때 인자, 옵션, 종료 코드, 출력 결과를 기록합니다. 특정 명령을 워처의 기록에서 제외하려면 `config/telescope.php` 파일의 `ignore` 옵션에 명령어를 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    ...
],
```

<a name="dump-watcher"></a>
### 덤프 워처

덤프 워처는 Telescope 내에서 변수 덤프를 기록하고 표시합니다. Laravel에서는 전역 `dump` 함수로 변수를 덤프할 수 있습니다. 덤프 탭이 브라우저에서 열려 있어야만 덤프가 기록되며, 그렇지 않으면 덤프는 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 발생하는 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. Laravel 프레임워크의 내부 이벤트는 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 보고 가능한 예외가 발생할 때 해당 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 애플리케이션에서 수행한 [게이트 및 정책](/docs/{{version}}/authorization) 검사에 대한 데이터와 결과를 기록합니다. 특정 능력을 워처에서 제외하려면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    ...
],
```

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션에서 발생한 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 애플리케이션에서 발생한 [큐 작업](/docs/{{version}}/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션에서 기록되는 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

<a name="mail-watcher"></a>
### 메일 워처

메일 워처를 통해 애플리케이션에서 전송된 [이메일](/docs/{{version}}/mail)의 인-브라우저 미리보기를 해당 관련 데이터와 함께 확인할 수 있습니다. 또한 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 모델의 변경사항을 기록합니다. 어떤 모델 이벤트를 기록할지 워처의 `events` 옵션으로 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

특정 요청 중 하이드레이션된 모델의 수까지 기록하고 싶을 경우, `hydrations` 옵션을 활성화합니다:

```php
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
### 알림 워처

알림 워처는 애플리케이션에서 발송된 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 알림이 이메일을 트리거하고, 메일 워처가 활성화되어 있다면 이메일을 미리보기로 확인할 수도 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원시 SQL, 바인딩, 실행시간 등을 기록합니다. 또한, 100 밀리초보다 느린 쿼리는 `slow` 태그로 표시됩니다. 느린 쿼리 임계값은 워처의 `slow` 옵션으로 변경할 수 있습니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    ...
],
```

<a name="redis-watcher"></a>
### Redis 워처

Redis 워처는 애플리케이션이 실행한 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. Redis를 캐시로 사용할 경우, 캐시 커맨드도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 애플리케이션에서 처리되는 모든 요청의 요청 데이터, 헤더, 세션, 응답 데이터를 기록합니다. 기록될 응답 데이터량은 `size_limit`(킬로바이트 단위) 옵션으로 제한할 수 있습니다:

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    ...
],
```

<a name="schedule-watcher"></a>
### 스케줄 워처

스케줄 워처는 애플리케이션에서 수행된 [예약 작업](/docs/{{version}}/scheduling)의 커맨드 및 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 [뷰](/docs/{{version}}/views) 렌더링 시 사용된 뷰 이름, 경로, 데이터, "컴포저" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 저장된 항목의 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 이용해 아바타를 가져옵니다. 하지만 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 자유롭게 커스터마이즈할 수 있습니다. 콜백은 사용자 ID 및 이메일을 받아 사용자의 아바타 이미지 URL을 반환해야 합니다:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
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