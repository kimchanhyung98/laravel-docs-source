# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 환경 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리(Pruning)](#data-pruning)
    - [대시보드 권한 부여](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리](#filtering-entries)
    - [배치](#filtering-batches)
- [태그 지정](#tagging)
- [사용 가능한 워처(Watcher)](#available-watchers)
    - [배치 워처](#batch-watcher)
    - [캐시 워처](#cache-watcher)
    - [명령어 워처](#command-watcher)
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

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에 훌륭하게 어울리는 도구입니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐 작업, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 제공합니다.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 Telescope를 Laravel 프로젝트에 설치할 수 있습니다.

    composer require laravel/telescope

Telescope 설치 후, `telescope:install` Artisan 명령어를 사용하여 에셋을 퍼블리시합니다. 또한, Telescope의 데이터를 저장할 테이블을 생성하기 위해 `migrate` 명령어를 실행해야 합니다.

    php artisan telescope:install

    php artisan migrate

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징

Telescope의 기본 마이그레이션을 사용하지 않을 경우, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메소드 안에서 `Telescope::ignoreMigrations` 메소드를 호출해야 합니다. 기본 마이그레이션 파일을 내보내려면 다음 명령어를 사용합니다: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### 로컬 환경 전용 설치

Telescope를 로컬 개발 지원 목적으로만 사용하려면 `--dev` 플래그를 사용해 설치할 수 있습니다.

    composer require laravel/telescope --dev

    php artisan telescope:install

    php artisan migrate

`telescope:install` 명령어를 실행한 후에는, 애플리케이션의 `config/app.php` 파일에서 `TelescopeServiceProvider` 등록을 제거하세요. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메소드에서 Telescope의 서비스 프로바이더를 직접 등록합니다. 현재 환경이 `local`인지 확인한 후 등록해야 합니다.

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

마지막으로, `composer.json` 파일에 아래와 같이 추가하여 Telescope 패키지가 [자동 디스커버리](/docs/{{version}}/packages#package-discovery)되지 않도록 해야 합니다.

    "extra": {
        "laravel": {
            "dont-discover": [
                "laravel/telescope"
            ]
        }
    },

<a name="configuration"></a>
### 설정

Telescope의 에셋을 퍼블리시한 후, 주요 설정 파일은 `config/telescope.php`에 위치합니다. 이 설정 파일을 통해 [워처 옵션](#available-watchers)을 구성할 수 있습니다. 각 옵션에는 목적에 대한 설명이 있으니 꼼꼼하게 확인해 보세요.

필요하다면, `enabled` 설정 옵션으로 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다.

    'enabled' => env('TELESCOPE_ENABLED', true),

<a name="data-pruning"></a>
### 데이터 정리(Pruning)

데이터 정리를 하지 않으면 `telescope_entries` 테이블에 기록이 빠르게 쌓일 수 있습니다. 이를 방지하려면, [스케줄러](/docs/{{version}}/scheduling)를 활용하여 `telescope:prune` Artisan 명령어를 매일 실행하도록 하세요.

    $schedule->command('telescope:prune')->daily();

기본적으로 24시간이 지난 모든 엔트리가 정리됩니다. 명령어 실행 시 `hours` 옵션을 지정하여 데이터 보관 기간을 조정할 수 있습니다. 예를 들어, 아래 명령어는 48시간이 지난 모든 엔트리를 삭제합니다.

    $schedule->command('telescope:prune --hours=48')->daily();

<a name="dashboard-authorization"></a>
### 대시보드 권한 부여

Telescope 대시보드는 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용됩니다. `app/Providers/TelescopeServiceProvider.php` 파일에는 [인가 게이트](/docs/{{version}}/authorization#gates) 정의가 있습니다. 이 게이트는 **로컬이 아닌 환경**에서 Telescope 접근 권한을 제어합니다. 필요에 따라 이 게이트를 수정하여 Telescope 접근을 제한할 수 있습니다.

    /**
     * Telescope 게이트 등록
     *
     * 이 게이트는 로컬 환경이 아닌 곳의 Telescope 접근 권한을 결정합니다.
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

> {note} 운영 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope 설치가 외부에 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 새로운 주요 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 검토하세요.

또한, 새로운 Telescope 버전으로 업그레이드할 때마다 Telescope의 에셋을 다시 퍼블리시해야 합니다.

    php artisan telescope:publish

에셋을 항상 최신 상태로 유지하고 차후 업데이트 시 이슈를 방지하려면, `composer.json` 파일의 `post-update-cmd` 스크립트에 `telescope:publish` 명령어를 추가하세요.

    {
        "scripts": {
            "post-update-cmd": [
                "@php artisan telescope:publish --ansi"
            ]
        }
    }

<a name="filtering"></a>
## 필터링

<a name="filtering-entries"></a>
### 엔트리

`App\Providers\TelescopeServiceProvider` 클래스에 정의된 `filter` 클로저를 통해 Telescope가 기록하는 데이터를 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 작업, 예약된 작업, 모니터링된 태그가 포함된 데이터를 기록합니다.

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

<a name="filtering-batches"></a>
### 배치

`filter` 클로저는 개별 엔트리의 데이터를 필터링하지만, `filterBatch` 메소드를 이용하면 요청이나 콘솔 명령어 단위로 모든 데이터를 필터링하는 클로저를 등록할 수 있습니다. 클로저가 `true`를 반환하면 모든 엔트리가 기록됩니다.

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

<a name="tagging"></a>
## 태그 지정

Telescope는 "태그"로 엔트리를 검색할 수 있습니다. 대부분의 경우, 태그는 Eloquent 모델 클래스명 또는 인증된 사용자 ID이며, Telescope가 자동으로 엔트리에 추가합니다. 때로는 사용자 정의 태그를 엔트리에 추가하고 싶을 수 있는데, 이럴 때는 `Telescope::tag` 메소드를 사용합니다. 이 메소드는 클로저를 인수로 받으며, 클로저는 태그의 배열을 반환해야 합니다. 반환된 태그는 Telescope가 자동 추가하는 태그와 병합됩니다. 일반적으로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메소드 내에서 호출합니다.

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

<a name="available-watchers"></a>
## 사용 가능한 워처(Watcher)

Telescope의 "워처"는 요청 또는 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. 활성화할 워처 목록은 `config/telescope.php` 설정 파일에서 조정할 수 있습니다.

    'watchers' => [
        Watchers\CacheWatcher::class => true,
        Watchers\CommandWatcher::class => true,
        ...
    ],

일부 워처는 추가 설정 옵션도 제공합니다.

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 100,
        ],
        ...
    ],

<a name="batch-watcher"></a>
### 배치 워처

배치 워처는 큐에 저장된 [배치 작업](/docs/{{version}}/queues#job-batching)에 대한 정보(작업, 커넥션 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키에 접근(히트), 미스, 업데이트, 삭제 작업이 발생할 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 명령어 워처

명령어 워처는 Artisan 명령 실행 시 인자, 옵션, 종료 코드, 출력 내용을 기록합니다. 특정 명령어의 기록을 제외하고 싶다면 `config/telescope.php` 파일의 `ignore` 옵션에 명령어를 지정할 수 있습니다.

    'watchers' => [
        Watchers\CommandWatcher::class => [
            'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
            'ignore' => ['key:generate'],
        ],
        ...
    ],

<a name="dump-watcher"></a>
### 덤프 워처

덤프 워처는 변수 덤프를 Telescope에 기록하고 보여줍니다. Laravel에서 변수를 덤프하려면 전역 `dump` 함수를 사용할 수 있습니다. 이 때 덤프 탭이 브라우저에서 열려 있어야만 기록됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 디스패치된 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. 라라벨 프레임워크 내부 이벤트는 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생한 리포팅 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 [게이트와 정책](/docs/{{version}}/authorization) 검사 데이터 및 결과를 기록합니다. 특정 ability를 기록에서 제외하려면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 추가하세요.

    'watchers' => [
        Watchers\GateWatcher::class => [
            'enabled' => env('TELESCOPE_GATE_WATCHER', true),
            'ignore_abilities' => ['viewNova'],
        ],
        ...
    ],

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션에서 발생시키는 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 [잡](/docs/{{version}}/queues)이 디스패치 될 때의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션이 기록하는 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

<a name="mail-watcher"></a>
### 메일 워처

메일 워처를 이용하면 애플리케이션에서 전송한 [이메일](/docs/{{version}}/mail)을 브라우저에서 미리보기 할 수 있고, 관련 데이터도 함께 확인할 수 있습니다. 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 모델의 변경 내용을 기록합니다. 기록할 모델 이벤트는 워처의 `events` 옵션으로 지정할 수 있습니다.

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
        ],
        ...
    ],

요청 중 하이드레이트(조회)된 모델 수를 기록하려면 `hydrations` 옵션을 활성화하세요.

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

알림 워처는 애플리케이션에서 전송한 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 알림이 이메일을 발송하고 메일 워처가 활성화된 상태라면, 메일 워처 화면에서 미리보기도 가능합니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 실행되는 모든 쿼리의 원시 SQL, 바인딩, 실행 시간을 기록합니다. 100밀리초를 초과하는 쿼리는 `slow`로 태깅됩니다. 느린 쿼리의 기준 임계값은 워처의 `slow` 옵션으로 조정할 수 있습니다.

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 50,
        ],
        ...
    ],

<a name="redis-watcher"></a>
### Redis 워처

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. Redis를 캐시에 사용할 경우, 캐시 명령도 함께 기록합니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 애플리케이션에서 처리된 요청의 요청 데이터, 헤더, 세션, 응답 데이터를 기록합니다. 기록되는 응답 데이터의 크기는 `size_limit`(킬로바이트 단위) 옵션으로 제한할 수 있습니다.

    'watchers' => [
        Watchers\RequestWatcher::class => [
            'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
            'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
        ],
        ...
    ],

<a name="schedule-watcher"></a>
### 스케줄 워처

스케줄 워처는 애플리케이션에서 실행한 [예약 작업](/docs/{{version}}/scheduling)의 명령어와 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 뷰 렌더링 시 사용된 [뷰](/docs/{{version}}/views) 이름, 경로, 데이터, "컴포저" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 저장된 엔트리를 기록한 인증 사용자의 아바타 이미지를 표시합니다. 기본적으로 Gravatar 웹 서비스를 통해 아바타를 가져오나, `App\Providers\TelescopeServiceProvider` 클래스에 콜백을 등록하여 아바타 URL을 직접 지정할 수도 있습니다. 이 콜백은 사용자 ID와 이메일을 인수로 받아 사용자의 아바타 이미지 URL을 반환해야 합니다.

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
