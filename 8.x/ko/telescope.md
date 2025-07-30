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
## 소개

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에 훌륭한 동반자가 되어 줍니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 대기열 잡, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```
composer require laravel/telescope
```

Telescope를 설치한 후에는 `telescope:install` Artisan 명령어로 자산을 게시해야 합니다. 설치 후에는 Telescope 데이터 저장에 필요한 테이블을 생성하기 위해 `migrate` 명령도 실행해야 합니다:

```
php artisan telescope:install

php artisan migrate
```

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징

Telescope 기본 마이그레이션을 사용하지 않을 경우, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Telescope::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션은 다음 명령어로 내보낼 수 있습니다: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### 로컬 전용 설치

Telescope를 로컬 개발에만 사용할 계획이라면 `--dev` 플래그를 사용해 설치할 수 있습니다:

```
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후, `config/app.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 수동으로 Telescope 서비스 프로바이더를 등록하세요. 등록 전에 현재 환경이 `local`인지 확인해야 합니다:

```
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

마지막으로, `composer.json` 파일에 다음을 추가하여 Telescope 패키지가 [자동 발견](/docs/{{version}}/packages#package-discovery)되지 않도록 해야 합니다:

```
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

Telescope 자산을 게시하면 기본 설정 파일이 `config/telescope.php`에 위치하게 됩니다. 이 설정 파일을 통해 [워처 옵션](#available-watchers)을 구성할 수 있습니다. 각 설정 옵션에는 설명이 포함되어 있으니 꼼꼼히 살펴보시기 바랍니다.

필요하다면 `enabled` 설정 옵션을 통해 Telescope의 데이터 수집을 완전히 비활성화할 수도 있습니다:

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리

데이터 정리를 하지 않으면 `telescope_entries` 테이블에 아주 빠르게 기록이 쌓일 수 있습니다. 이를 방지하기 위해 `telescope:prune` Artisan 명령어를 일일 단위로 [스케줄](/docs/{{version}}/scheduling)해서 실행하는 것을 권장합니다:

```
$schedule->command('telescope:prune')->daily();
```

기본적으로는 24시간이 지난 모든 엔트리가 정리됩니다. 명령어 실행 시 `hours` 옵션을 지정해 데이터를 얼마나 오래 보관할지 설정할 수도 있습니다. 예를 들어, 다음은 48시간 지난 기록을 삭제합니다:

```
$schedule->command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정

Telescope 대시보드는 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 접근이 허용됩니다. `app/Providers/TelescopeServiceProvider.php` 파일 안에 [권한 게이트](/docs/{{version}}/authorization#gates)가 정의되어 있습니다. 이 게이트는 **비로컬** 환경에서 Telescope 접근 권한을 제어합니다. 필요에 따라 이 게이트를 수정해 Telescope 접근 제한을 설정할 수 있습니다:

```
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

> [!NOTE]
> 프로덕션 환경에서는 `APP_ENV` 환경 변수를 반드시 `production`으로 설정해야 합니다. 그렇지 않으면 Telescope가 공개되어 외부에 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 새로운 주요 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

또한, 새 버전으로 업그레이드한 후에는 Telescope 자산을 다시 게시해야 합니다:

```
php artisan telescope:publish
```

자산을 최신 상태로 유지하고 향후 문제를 방지하기 위해, `composer.json` 파일의 `post-update-cmd` 스크립트에 `telescope:publish` 명령어를 추가할 수도 있습니다:

```
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan telescope:publish --ansi"
        ]
    }
}
```

<a name="filtering"></a>
## 필터링

<a name="filtering-entries"></a>
### 엔트리 필터링

Telescope에 기록할 데이터를 `App\Providers\TelescopeServiceProvider` 클래스의 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하며, 다른 환경에서는 예외, 실패한 잡, 예약된 작업, 느린 쿼리, 모니터링되는 태그가 달린 데이터만 기록합니다:

```
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
### 배치 필터링

`filter` 클로저가 개별 엔트리를 필터링하는 반면, `filterBatch` 메서드는 특정 요청 또는 콘솔 명령어에 대해 모든 엔트리들을 함께 필터링할 수 있게 해줍니다. 클로저가 `true`를 반환하면 해당 배치의 모든 엔트리가 Telescope에 기록됩니다:

```
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

Telescope는 "태그"를 통해 엔트리를 검색할 수 있게 합니다. 태그는 주로 Eloquent 모델 클래스명이나 인증된 사용자 ID 등이며, Telescope가 자동으로 엔트리에 추가합니다. 때로는 사용자 정의 태그를 엔트리에 붙이고 싶을 수도 있습니다. 이 경우 `Telescope::tag` 메서드를 사용하면 됩니다. `tag` 메서드는 태그 배열을 반환하는 클로저를 받으며, 이 클로저에서 리턴한 태그는 Telescope가 자동으로 붙이는 태그와 병합됩니다. 일반적으로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출합니다:

```
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

Telescope의 "워처"는 요청이나 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. 활성화할 워처 목록은 `config/telescope.php` 설정 파일에서 구성할 수 있습니다:

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
### 배치 워처

배치 워처는 대기열 [배치](/docs/{{version}}/queues#job-batching)에 관한 정보, 즉 잡과 연결 정보를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키가 조회(hit), 실패(missed), 갱신(updated), 삭제(forgotten)될 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처

커맨드 워처는 Artisan 커맨드 실행 시 인수, 옵션, 종료 코드 그리고 출력 내용을 기록합니다. 특정 커맨드를 기록에서 제외하려면 `config/telescope.php` 파일의 `ignore` 옵션에 해당 커맨드를 지정할 수 있습니다:

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
### 덤프 워처

덤프 워처는 Telescope 내에서 변수 덤프를 기록하고 표시합니다. Laravel에서 변수는 전역 `dump` 함수로 덤프할 수 있습니다. 덤프 워처 탭이 브라우저에서 열려 있어야 덤프 내용이 기록되며, 그렇지 않으면 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 발생하는 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 방송 데이터를 기록합니다. Laravel 내부에서 발생하는 일부 이벤트는 이벤트 워처가 무시합니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생하는 보고 가능한 예외들의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 애플리케이션의 [게이트와 정책](/docs/{{version}}/authorization) 검사 결과를 기록합니다. 특정 능력(abilities)을 기록에서 제외하려면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 해당 능력을 지정할 수 있습니다:

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
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션에서 실행하는 외부 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 애플리케이션에서 디스패치한 [잡](/docs/{{version}}/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션에 의해 작성된 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

<a name="mail-watcher"></a>
### 메일 워처

메일 워처는 애플리케이션에서 발송한 [이메일](/docs/{{version}}/mail)을 브라우저에서 미리 보기 할 수 있게 해주며, 관련 데이터도 보여줍니다. 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 모델 변경 사항을 기록합니다. 어떤 모델 이벤트를 기록할지 워처의 `events` 옵션에 지정할 수 있습니다:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

요청 중에 하이드레이션된 모델 수를 기록하고 싶다면 `hydrations` 옵션을 활성화하세요:

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
### 알림 워처

알림 워처는 애플리케이션에서 발송된 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 만약 알림이 이메일 발송도 포함하고 있고 메일 워처가 활성화되어 있다면, 메일 워처 화면에서 해당 이메일 미리보기도 가능합니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션의 모든 데이터베이스 쿼리의 원본 SQL, 바인딩 값, 실행 시간을 기록합니다. 100밀리초 이상 느린 쿼리는 `slow` 태그가 붙습니다. 느린 쿼리 기준(임계값)은 워처의 `slow` 옵션으로 조정할 수 있습니다:

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
### Redis 워처

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/{{version}}/redis) 명령어를 기록합니다. Redis를 캐싱 용도로 사용할 경우 캐시 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 애플리케이션이 처리하는 요청과 관련된 요청 본문, 헤더, 세션, 응답 데이터를 기록합니다. 기록되는 응답 데이터 크기는 `size_limit` (킬로바이트 단위) 옵션으로 제한할 수 있습니다:

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
### 스케줄 워처

스케줄 워처는 애플리케이션에서 실행하는 모든 [예약 작업](/docs/{{version}}/scheduling)의 명령과 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 뷰 렌더링 시 사용되는 [뷰](/docs/{{version}}/views)의 이름, 경로, 데이터 및 "컴포저"를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 엔트리가 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 그러나 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록하여 아바타 URL을 커스터마이징할 수도 있습니다. 콜백은 사용자의 ID와 이메일을 받아 해당 사용자의 아바타 이미지 URL을 반환해야 합니다:

```
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