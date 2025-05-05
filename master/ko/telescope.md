# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 권한 부여](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리](#filtering-entries)
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

[Laravel Telescope](https://github.com/laravel/telescope)는 여러분의 로컬 Laravel 개발 환경에 훌륭한 동반자가 됩니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 기록, 데이터베이스 쿼리, 큐 작업, 메일, 알림, 캐시 동작, 예약 작업, 변수 덤프 등 다양한 정보를 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 여러분의 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope 설치 후, `telescope:install` Artisan 명령어를 사용하여 자산과 마이그레이션을 게시해야 합니다. Telescope를 설치한 후에는 Telescope 데이터 저장에 필요한 테이블을 만들기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로, `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치

Telescope를 오직 로컬 개발을 지원하기 위해서만 사용할 계획이라면, `--dev` 플래그를 사용하여 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install`을 실행한 뒤에는, 애플리케이션의 `bootstrap/providers.php` 구성 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 Telescope의 서비스 프로바이더를 직접 등록하세요. 다음 예제처럼 현재 환경이 `local`인지 확인 후 프로바이더를 등록합니다:

```php
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

마지막으로, 다음 내용을 `composer.json` 파일의 `"extra"` 항목에 추가하여 Telescope 패키지가 [자동 검색](/docs/{{version}}/packages#package-discovery)되지 않도록 해야 합니다:

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

Telescope의 자산을 게시한 후에는 주요 설정 파일이 `config/telescope.php`에 위치합니다. 이 설정 파일에서 [워처 옵션](#available-watchers)을 구성할 수 있습니다. 각 설정 옵션에는 용도에 대한 설명이 포함되어 있으므로, 이 파일을 꼼꼼히 살펴보시기 바랍니다.

원한다면, `enabled` 설정 옵션을 사용하여 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리

데이터 정리를 하지 않으면, `telescope_entries` 테이블에 기록이 매우 빠르게 쌓일 수 있습니다. 이를 방지하기 위해, [스케줄러](/docs/{{version}}/scheduling)를 이용하여 `telescope:prune` Artisan 명령어를 매일 실행하도록 예약해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

기본적으로 24시간이 지난 모든 엔트리가 정리됩니다. Telescope 데이터를 얼마 동안 유지할지 결정하고 싶다면 명령 실행 시 `hours` 옵션을 사용할 수 있습니다. 예를 들어, 아래 명령어는 48시간(2일) 이상된 모든 기록을 삭제합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 권한 부여

Telescope 대시보드는 `/telescope` 경로를 통해 접근할 수 있습니다. 기본적으로, 이 대시보드는 `local` 환경에서만 접근 가능합니다. `app/Providers/TelescopeServiceProvider.php` 파일에는 [인증 게이트](/docs/{{version}}/authorization#gates) 정의가 포함되어 있습니다. 이 인증 게이트는 **로컬 환경이 아닌** 환경에서의 Telescope 접근을 제어합니다. 필요에 따라 이 게이트를 수정하여 Telescope 설치에 대한 접근을 제한할 수 있습니다:

```php
use App\Models\User;

/**
 * Telescope 게이트를 등록합니다.
 *
 * 이 게이트는 로컬 환경이 아닌 곳에서 Telescope에 접근 가능한 사용자를 결정합니다.
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
> 실서버 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 변경해야 합니다. 그렇지 않으면 여러분의 Telescope 설치가 외부에 공개될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 새로운 주요 버전으로 업그레이드할 경우, 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

또한, Telescope의 새로운 버전으로 업그레이드할 때마다 Telescope의 자산을 다시 게시해야 합니다:

```shell
php artisan telescope:publish
```

자산을 최신 상태로 유지하고 향후 업데이트 시 문제를 방지하기 위해, 애플리케이션의 `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령을 추가할 수 있습니다:

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
### 엔트리

Telescope를 통해 기록되는 데이터를 `App\Providers\TelescopeServiceProvider` 클래스에 정의된 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로, 해당 클로저는 `local` 환경에서는 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 잡, 예약 작업, 모니터드 태그가 포함된 데이터를 기록합니다:

```php
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
### 배치

`filter` 클로저가 개별 엔트리 데이터를 필터링하는 반면, `filterBatch` 메소드는 하나의 요청이나 콘솔 명령 전체에 대한 데이터를 필터링하는 클로저를 등록할 수 있습니다. 클로저가 `true`를 반환하면 모든 엔트리가 Telescope에 기록됩니다:

```php
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
## 태깅

Telescope를 이용하면 "태그"를 기반으로 엔트리를 검색할 수 있습니다. 종종 Eloquent 모델 클래스명이나 인증된 사용자 ID가 Telescope에 의해 자동으로 엔트리에 태그로 추가됩니다. 때로는 사용자 정의 태그를 엔트리에 붙이고 싶을 수 있습니다. 이를 위해 `Telescope::tag` 메소드를 사용할 수 있습니다. `tag` 메소드는 태그 배열을 반환해야 하는 클로저를 인자로 받습니다. 클로저가 반환하는 태그는 Telescope가 자동으로 붙이는 태그와 병합됩니다. 일반적으로, 이 메소드는 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메소드 내에서 호출합니다:

```php
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
## 사용 가능한 워처

Telescope의 "워처"는 요청이나 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. `config/telescope.php` 설정 파일에서 활성화할 워처 목록을 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

일부 워처는 추가로 커스터마이징 옵션을 제공하기도 합니다:

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
### 배치 워처

배치 워처는 큐에 등록된 [배치](/docs/{{version}}/queues#job-batching) 작업의 정보(작업 및 연결 정보 포함)를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키에 대한 히트, 미스, 업데이트, 삭제 등의 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처

커맨드 워처는 Artisan 커맨드가 실행될 때 인수, 옵션, 종료 코드, 출력 결과를 기록합니다. 특정 커맨드를 기록하지 않으려면 `config/telescope.php`의 `ignore` 옵션에 커맨드 이름을 지정할 수 있습니다:

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
### 덤프 워처

덤프 워처는 Telescope에서 변수 덤프를 기록하고 표시합니다. Laravel에서는 전역 `dump` 함수를 사용해 변수를 덤프할 수 있습니다. 이 워처로 덤프를 기록하려면 브라우저의 덤프 탭이 열려 있어야 하며, 그렇지 않을 경우 덤프는 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 발생시킨 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 브로드캐스트 정보를 기록합니다. Laravel 프레임워크 내부 이벤트는 워처에서 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생하는 리포트 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 애플리케이션에서 발생한 [게이트 및 정책](/docs/{{version}}/authorization) 체크의 데이터 및 결과를 기록합니다. 특정 권한에 대한 기록을 제외하려면 `config/telescope.php`의 `ignore_abilities` 옵션에 명시하세요:

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
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션에서 발생한 모든 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 애플리케이션에서 디스패치한 [잡](/docs/{{version}}/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션에서 남긴 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

기본적으로, Telescope는 `error` 레벨 이상의 로그만 기록합니다. 필요에 따라 `config/telescope.php`의 `level` 값을 수정할 수 있습니다:

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
### 메일 워처

메일 워처는 애플리케이션에서 전송된 [이메일](/docs/{{version}}/mail)의 브라우저 내 미리보기를 제공합니다. 관련 데이터와 함께 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 모델 변화를 기록합니다. 기록할 모델 이벤트는 워처의 `events` 옵션에서 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

요청 처리 중 하이드레이션된 모델 수를 기록하려면 `hydrations` 옵션을 활성화하세요:

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
### 알림 워처

알림 워처는 애플리케이션에서 전송된 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 알림이 이메일을 트리거하고 메일 워처가 활성화되어 있다면 해당 이메일을 메일 워처 화면에서 미리볼 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 수행된 모든 쿼리의 원시 SQL, 바인딩, 실행 시간을 기록합니다. 또한 100 밀리초보다 느린 쿼리는 `slow` 태그를 부여합니다. 워처의 `slow` 옵션을 사용해 느린 쿼리 기준을 변경할 수 있습니다:

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
### Redis 워처

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. Redis를 캐시로 사용할 경우, 캐시 관련 커맨드도 Redis 워처가 기록합니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 애플리케이션이 처리한 요청의 본문, 헤더, 세션, 응답 데이터를 기록합니다. 기록할 응답 데이터의 최대 크기는 `size_limit` 옵션(킬로바이트 단위)으로 제한할 수 있습니다:

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
### 스케줄 워처

스케줄 워처는 애플리케이션에서 실행된 [예약 작업](/docs/{{version}}/scheduling)의 커맨드와 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 [뷰](/docs/{{version}}/views)명, 경로, 데이터, 렌더링할 때 사용된 "컴포저"에 대한 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 각 엔트리가 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 하지만, `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록하여 아바타 URL을 자유롭게 커스터마이징할 수 있습니다. 콜백은 사용자의 ID와 이메일 주소를 받아서 사용자의 아바타 이미지 URL을 반환해야 합니다:

```php
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
