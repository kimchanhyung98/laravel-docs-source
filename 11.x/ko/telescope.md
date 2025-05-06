# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 환경 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리(Pruning)](#data-pruning)
    - [대시보드 인증](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리](#filtering-entries)
    - [배치](#filtering-batches)
- [태그 지정](#tagging)
- [사용 가능한 워처(Watcher)](#available-watchers)
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

[Laravel Telescope](https://github.com/laravel/telescope)는 당신의 로컬 Laravel 개발 환경에 훌륭한 동반자가 되어줍니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐에 등록된 잡, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 분석해줍니다.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Telescope를 Laravel 프로젝트에 설치하려면 Composer 패키지 관리자를 사용할 수 있습니다:

```shell
composer require laravel/telescope
```

설치 후, `telescope:install` Artisan 명령을 통해 Telescope의 에셋과 마이그레이션을 게시하십시오. 또한 Telescope가 데이터를 저장하기 위해 필요한 테이블을 생성하려면 반드시 `migrate` 명령을 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

이제 `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 환경 전용 설치

로컬 개발을 위한 용도로만 Telescope를 사용하려면, `--dev` 플래그를 사용하여 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후, `bootstrap/providers.php` 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 그 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메소드 내에서 Telescope의 서비스 프로바이더를 직접 등록하세요. 현재 환경이 `local` 인지 확인한 후 프로바이더를 등록합니다:

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

마지막으로, `composer.json` 파일의 다음 설정을 추가하여 Telescope 패키지가 [자동 검색](/docs/{{version}}/packages#package-discovery)되지 않도록 해야 합니다:

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

Telescope의 에셋을 게시한 후, 주요 설정 파일은 `config/telescope.php`에 위치합니다. 이 파일에서 [워처 옵션](#available-watchers) 등을 설정할 수 있으며, 각 옵션마다 목적에 대한 설명이 포함되어 있으니 꼼꼼하게 살펴보시기 바랍니다.

또한, 원한다면 아래와 같이 `enabled` 옵션을 통해 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다.

    'enabled' => env('TELESCOPE_ENABLED', true),

<a name="data-pruning"></a>
### 데이터 정리(Pruning)

데이터 정리를 하지 않을 경우 `telescope_entries` 테이블에 레코드가 빠르게 누적될 수 있습니다. 데이터를 관리하기 위해 `telescope:prune` Artisan 명령을 [스케줄링](/docs/{{version}}/scheduling)하여 매일 실행되도록 해야 합니다.

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('telescope:prune')->daily();

기본적으로 24시간이 지난 엔트리는 모두 삭제됩니다. 보존 기간을 조절하려면 명령 실행 시 `hours` 옵션을 사용할 수 있습니다. 예를 들어, 아래 명령은 48시간이 지난 모든 레코드를 삭제합니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('telescope:prune --hours=48')->daily();

<a name="dashboard-authorization"></a>
### 대시보드 인증

Telescope 대시보드는 `/telescope` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용됩니다. `app/Providers/TelescopeServiceProvider.php` 파일 내 [인증 게이트](/docs/{{version}}/authorization#gates) 정의를 통해 **비-로컬** 환경에서의 대시보드 접근 권한을 제어할 수 있습니다. 필요한 경우 해당 게이트를 수정하여 Telescope 접근을 제한할 수 있습니다:

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

> [!WARNING]  
> 운영 환경에서는 반드시 `APP_ENV` 환경변수를 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope 설치가 공개적으로 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 새로운 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인해야 합니다.

또한, Telescope의 모든 새 버전 업그레이드 시 에셋을 다시 게시해야 합니다:

```shell
php artisan telescope:publish
```

에셋을 항상 최신 상태로 유지하고 미래의 업데이트 시 문제를 방지하기 위해, `composer.json`의 `post-update-cmd` 스크립트에 아래 명령어를 추가할 수 있습니다:

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

Telescope가 기록하는 데이터를 필터링하고 싶다면 `App\Providers\TelescopeServiceProvider` 클래스에 정의된 `filter` 클로저를 사용할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 잡, 예약된 작업, 모니터링 태그가 있는 데이터만 기록합니다.

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

<a name="filtering-batches"></a>
### 배치

`filter` 클로저가 개별 엔트리를 필터링한다면, `filterBatch` 메서드는 하나의 요청이나 콘솔 명령에 대한 모든 데이터를 필터링할 수 있습니다. 클로저가 `true`를 반환하면 모든 엔트리가 기록됩니다:

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

<a name="tagging"></a>
## 태그 지정

Telescope에서는 엔트리를 "태그"로 검색할 수 있습니다. 일반적으로 태그는 Eloquent 모델 클래스명이나 인증된 사용자 ID 등이 자동 추가되지만, 필요 시 커스텀 태그를 추가할 수도 있습니다. 이를 위해 `Telescope::tag` 메소드를 활용할 수 있으며, 이 메서드는 태그 배열을 반환하는 클로저를 받습니다. 제공된 태그는 Telescope가 자동으로 추가하는 태그와 합쳐집니다. 일반적으로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출합니다:

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

<a name="available-watchers"></a>
## 사용 가능한 워처(Watcher)

Telescope의 "워처"는 요청이나 콘솔 명령이 실행될 때 애플리케이션의 데이터를 수집합니다. 워처의 활성화 여부는 `config/telescope.php` 파일의 `watchers` 항목에서 설정할 수 있습니다:

    'watchers' => [
        Watchers\CacheWatcher::class => true,
        Watchers\CommandWatcher::class => true,
        ...
    ],

일부 워처는 추가 설정 옵션을 허용합니다:

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 100,
        ],
        ...
    ],

<a name="batch-watcher"></a>
### 배치 워처

배치 워처는 [잡 배치](/docs/{{version}}/queues#job-batching)에 대한 정보(잡, 커넥션 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키의 히트, 미스, 업데이트, 삭제 등의 정보를 기록합니다.

<a name="command-watcher"></a>
### 커맨드 워처

커맨드 워처는 Artisan 명령이 실행될 때의 인자, 옵션, 종료 코드, 출력 결과 등을 기록합니다. 특정 Artisan 명령어의 기록을 제외하려면, `config/telescope.php` 파일의 `ignore` 옵션에 명령을 추가하세요:

    'watchers' => [
        Watchers\CommandWatcher::class => [
            'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
            'ignore' => ['key:generate'],
        ],
        ...
    ],

<a name="dump-watcher"></a>
### 덤프 워처

덤프 워처는 변수 덤프를 기록하고 Telescope 내에서 표시합니다. Laravel에서 `dump` 전역 함수를 이용해 변수를 덤프할 수 있으며, 덤프 워처 탭이 브라우저에서 열려 있어야 기록됩니다. 그렇지 않으면 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 발생한 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. Laravel 프레임워크의 내부 이벤트는 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 애플리케이션의 [게이트 및 정책](/docs/{{version}}/authorization) 검사에 대한 데이터와 결과를 기록합니다. 특정 기능(ability)을 기록에서 제외하려면 `config/telescope.php`의 `ignore_abilities` 옵션을 사용하세요:

    'watchers' => [
        Watchers\GateWatcher::class => [
            'enabled' => env('TELESCOPE_GATE_WATCHER', true),
            'ignore_abilities' => ['viewNova'],
        ],
        ...
    ],

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션이 발송한 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 애플리케이션이 디스패치한 모든 [잡](/docs/{{version}}/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션에서 기록한 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

기본적으로 Telescope는 `error` 이상 레벨의 로그만 기록합니다. 그러나, `config/telescope.php`의 `level` 옵션을 변경하여 기록 대상을 설정할 수 있습니다:

    'watchers' => [
        Watchers\LogWatcher::class => [
            'enabled' => env('TELESCOPE_LOG_WATCHER', true),
            'level' => 'debug',
        ],

        // ...
    ],

<a name="mail-watcher"></a>
### 메일 워처

메일 워처는 애플리케이션이 보낸 [이메일](/docs/{{version}}/mail)을 브라우저에서 미리보기로 제공하며, 관련 데이터도 함께 표시합니다. 또한 `.eml` 파일로 다운로드할 수 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때 모델의 변경을 기록합니다. 어떤 이벤트를 기록할지 `events` 옵션에 지정할 수 있습니다:

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
        ],
        ...
    ],

특정 요청에서 하이드레이트된 모델의 개수까지 기록하고 싶다면, `hydrations` 옵션을 활성화하면 됩니다:

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
            'hydrations' => true,
        ],
        ...
    ],

<a name="notification-watcher"></a>
### 알림 워처

알림 워처는 애플리케이션에서 보낸 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 알림이 이메일을 발송하고 메일 워처가 활성화된 경우 이메일도 미리보기 화면에서 확인할 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원시 SQL, 바인딩, 실행시간을 기록합니다. 또한 100밀리초 이상 소요된 쿼리에 `slow` 태그를 추가합니다. 워처의 `slow` 옵션을 통해 느린 쿼리 임계값을 변경할 수 있습니다:

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 50,
        ],
        ...
    ],

<a name="redis-watcher"></a>
### Redis 워처

Redis 워처는 애플리케이션이 실행한 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. Redis를 캐시로 사용하는 경우, 캐시 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 요청, 헤더, 세션, 응답 데이터 등 애플리케이션이 처리한 모든 요청 관련 정보를 기록합니다. 기록되는 응답 데이터의 크기를 `size_limit`(킬로바이트 단위) 옵션으로 제한할 수 있습니다:

    'watchers' => [
        Watchers\RequestWatcher::class => [
            'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
            'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
        ],
        ...
    ],

<a name="schedule-watcher"></a>
### 스케줄 워처

스케줄 워처는 애플리케이션에서 실행된 [예약 작업](/docs/{{version}}/scheduling)의 커맨드와 출력 결과를 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 [뷰](/docs/{{version}}/views) 이름, 경로, 데이터, 그리고 뷰를 렌더링할 때 사용된 "composer" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 각 엔트리가 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Gravatar 웹 서비스를 통해 아바타 이미지를 가져오지만, `App\Providers\TelescopeServiceProvider` 클래스의 콜백을 통해 아바타 URL을 원하는 대로 커스터마이즈할 수 있습니다. 콜백은 사용자 ID와 이메일을 인자로 받아 아바타 이미지의 URL을 반환해야 합니다:

    use App\Models\User;
    use Laravel\Telescope\Telescope;

    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...

        Telescope::avatar(function (string $id, string $email) {
            return '/avatars/'.User::find($id)->avatar_path;
        });
    }
