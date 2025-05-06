# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 인증](#dashboard-authorization)
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
## 소개

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에서 훌륭한 동반자 역할을 합니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐잉된 작업, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 시각적으로 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Telescope를 Laravel 프로젝트에 설치하려면 Composer 패키지 매니저를 사용할 수 있습니다.

```shell
composer require laravel/telescope
```

Telescope 설치 후, `telescope:install` Artisan 명령어를 사용해 에셋과 마이그레이션을 퍼블리시하세요. 그리고 Telescope의 데이터를 저장할 테이블을 만들기 위해 `migrate` 명령어를 실행해야 합니다.

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로, `/telescope` 경로에서 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치

Telescope를 로컬 개발에서만 사용할 계획이라면, `--dev` 플래그를 사용하여 설치할 수 있습니다.

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후, 애플리케이션의 `bootstrap/providers.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메소드에서 Telescope의 서비스 프로바이더들을 명시적으로 등록하세요. 서비스 프로바이더 등록 전에 현재 환경이 `local`인지 확인합니다:

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

또한, 아래 설정을 `composer.json` 파일에 추가하여 Telescope 패키지가 [자동 검색](/docs/{{version}}/packages#package-discovery)되지 않도록 해야 합니다:

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

Telescope의 에셋을 퍼블리시한 후, 주요 설정 파일은 `config/telescope.php` 위치에 생성됩니다. 이 설정 파일에서는 [워처 옵션](#available-watchers) 등을 구성할 수 있습니다. 각 옵션에는 용도에 대한 설명이 포함되어 있으니, 반드시 이 파일을 꼼꼼히 살펴보세요.

원하는 경우, `enabled` 설정 옵션을 사용하여 Telescope의 데이터 수집을 전체적으로 비활성화할 수 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리

프루닝(pruning)을 하지 않으면 `telescope_entries` 테이블이 매우 빠르게 누적될 수 있습니다. 이를 방지하려면 [스케줄러](/docs/{{version}}/scheduling)를 이용해 `telescope:prune` Artisan 명령어를 매일 실행해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

기본적으로 24시간 이상된 모든 엔트리가 삭제됩니다. 명령어 실행 시 `hours` 옵션을 사용해 Telescope 데이터를 보존할 시간을 지정할 수 있습니다. 예를 들어, 아래와 같이 48시간이 지난 모든 레코드를 삭제할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 인증

Telescope 대시보드에는 `/telescope` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일 내에는 [인증 게이트](/docs/{{version}}/authorization#gates) 정의가 포함되어 있으며, 이 게이트는 **비-로컬** 환경에서의 Telescope 접근 권한을 제어합니다. 필요에 따라 이 게이트를 수정해 Telescope 설치에 대한 접근을 제한할 수 있습니다:

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
> 운영 환경에서는 `APP_ENV` 환경 변수를 반드시 `production`으로 변경해야 합니다. 그렇지 않으면, Telescope 설치가 외부에 공개됩니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 신규 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

또한, Telescope의 어떤 버전으로든 업그레이드할 때에는 Telescope 에셋을 다시 퍼블리시해야 합니다:

```shell
php artisan telescope:publish
```

향후 업데이트에서 자산 파일들이 항상 최신 상태로 유지되도록, 애플리케이션의 `composer.json` 파일 내 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령어를 추가할 수 있습니다:

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
### 엔트리 필터링

`App\Providers\TelescopeServiceProvider` 클래스 내에서 정의된 `filter` 클로저를 사용하여 Telescope에 기록되는 데이터를 필터링할 수 있습니다. 기본적으로, 이 클로저는 `local` 환경에서는 모든 데이터를 기록하며, 그 외 환경에서는 예외, 실패한 잡, 예약된 작업, 특정 태그가 연결된 데이터만 기록합니다:

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
### 배치 필터링

`filter` 클로저가 개별 엔트리에 대한 데이터를 필터링한다면, `filterBatch` 메소드는 하나의 요청이나 콘솔 명령에 대한 모든 데이터를 필터링하는 클로저를 등록하는 데 사용됩니다. 클로저가 `true`를 반환하면 해당 엔트리들이 모두 기록됩니다:

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
## 태깅

Telescope는 `"태그"`로 엔트리를 검색할 수 있도록 지원합니다. 대부분의 경우 태그는 Eloquent 모델 클래스 이름이나 인증된 사용자 ID 등이며, 이는 Telescope가 엔트리에 자동으로 추가합니다. 필요에 따라 엔트리에 커스텀 태그를 추가하고 싶을 때는 `Telescope::tag` 메소드를 사용할 수 있습니다. 이 메소드는 태그 배열을 반환하는 클로저를 인자로 받으며, 반환된 태그는 Telescope가 자동으로 부여하는 태그와 합쳐집니다. 보통 이 메소드는 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메소드 내에서 호출합니다:

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
## 사용 가능한 워처

Telescope의 `"워처"`는 요청 또는 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. `config/telescope.php` 설정 파일에서 활성화하고 싶은 워처 목록을 자유롭게 구성할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

일부 워처는 추가적인 설정 옵션도 제공합니다:

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

배치 워처는 큐로 처리되는 [배치 작업](/docs/{{version}}/queues#job-batching)에 대한 잡과 연결 정보 등을 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키가 히트, 미스, 갱신, 삭제될 때의 정보를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처

커맨드 워처는 Artisan 명령이 실행될 때 인자, 옵션, 종료 코드, 출력 등을 기록합니다. 특정 명령어의 기록을 제외하고 싶다면, `config/telescope.php`의 `ignore` 옵션에 명령어를 지정하세요:

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

덤프 워처는 변수 덤프를 Telescope 내에서 기록/표시합니다. Laravel에서는 전역 `dump` 함수를 사용하여 변수 덤프가 가능합니다. 단, 브라우저에서 덤프 워처 탭이 열려있어야 덤프가 기록되며, 그렇지 않은 경우에는 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 발생하는 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 브로드캐스트 데이터 등을 기록합니다. Laravel 프레임워크의 내부 이벤트는 기록하지 않습니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생하는 보고 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 애플리케이션의 [게이트 및 정책](/docs/{{version}}/authorization) 체크에 대한 데이터와 결과를 기록합니다. 특정 권한(ability)에 대해 기록을 제외하려면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 해당 권한명을 입력하세요:

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

HTTP 클라이언트 워처는 애플리케이션에서 발생한 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 애플리케이션에서 발생한 [잡](/docs/{{version}}/queues)에 대한 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션에서 기록된 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

기본적으로, Telescope는 `error` 레벨 이상의 로그만 기록합니다. 다만, 애플리케이션의 `config/telescope.php` 파일의 `level` 옵션을 변경해 동작을 수정할 수 있습니다:

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

메일 워처를 통해 애플리케이션에서 전송된 [이메일](/docs/{{version}}/mail) 및 해당 데이터의 브라우저 미리보기가 가능합니다. 또한, 이메일을 `.eml` 파일로 다운로드할 수 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 관련 모델의 변동 사항을 기록합니다. 워처의 `events` 옵션을 통해 기록할 모델 이벤트를 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

요청 중 하이드레이션된 모델의 수를 기록하고 싶다면 `hydrations` 옵션을 활성화하세요:

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

알림 워처는 애플리케이션에서 전송된 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 만약 알림이 이메일을 트리거하고, 메일 워처가 활성화되어 있다면, 해당 이메일도 메일 워처 화면에서 미리보기가 가능합니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원본 SQL, 바인딩, 실행 시간을 기록합니다. 또한, 100밀리초 이상 걸린 쿼리는 `slow` 태그로 강조됩니다. 워처의 `slow` 옵션을 이용해 느린 쿼리 임계값을 조정할 수 있습니다:

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

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. 캐시 용도로 Redis를 사용한다면, 캐시 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 애플리케이션에서 처리된 요청의 요청 정보, 헤더, 세션, 응답 데이터를 기록합니다. 기록되는 응답 데이터의 크기는 `size_limit`(킬로바이트 단위) 옵션으로 제한할 수 있습니다:

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

스케줄 워처는 애플리케이션에서 실행된 [스케줄 작업](/docs/{{version}}/scheduling)의 명령어와 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 [뷰](/docs/{{version}}/views)의 이름, 경로, 데이터, 뷰 렌더링에 사용한 "composer" 등을 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 엔트리가 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 하지만 필요하다면 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 커스터마이즈할 수 있습니다. 이 콜백은 사용자 ID와 이메일 주소를 받아서 이미지 URL을 반환해야 합니다:

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