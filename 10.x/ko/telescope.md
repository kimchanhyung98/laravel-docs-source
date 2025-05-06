# Laravel Telescope

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 인증](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리](#filtering-entries)
    - [배치](#filtering-batches)
- [태깅](#tagging)
- [사용 가능한 워처](#available-watchers)
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

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에 훌륭하게 어울리는 도구입니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐 잡, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 시각적으로 제공해줍니다.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

Telescope를 설치한 후, `telescope:install` Artisan 명령어로 에셋을 퍼블리시하세요. 그 후, Telescope의 데이터를 저장할 테이블을 생성하기 위해 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

마지막으로, `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징

Telescope의 기본 마이그레이션을 사용하지 않을 경우, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Telescope::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션을 다음 명령어로 내보낼 수 있습니다:  
`php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### 로컬 전용 설치

Telescope를 오직 로컬 개발을 지원하기 위해 사용하려는 경우, `--dev` 플래그를 이용해 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install` 실행 후, 애플리케이션의 `config/app.php` 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 Telescope 서비스 프로바이더를 직접 등록하세요. 환경이 `local`일 때만 프로바이더를 등록합니다:

    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        if ($this->app->environment('local')) {
            $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
            $this->app->register(TelescopeServiceProvider::class);
        }
    }

마지막으로, `composer.json` 파일에 아래 내용을 추가해 Telescope 패키지의 [자동 발견](/docs/{{version}}/packages#package-discovery)을 방지해야 합니다:

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

Telescope의 에셋을 퍼블리시한 후에는 주 설정 파일이 `config/telescope.php`에 위치합니다. 이 파일을 통해 [워처 옵션](#available-watchers) 등을 설정할 수 있습니다. 각 옵션에는 해당 목적에 대한 설명도 포함되어 있으니, 꼼꼼히 살펴보시기 바랍니다.

원한다면, `enabled` 설정을 통해 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다:

    'enabled' => env('TELESCOPE_ENABLED', true),

<a name="data-pruning"></a>
### 데이터 정리

데이터 정리를 하지 않으면 `telescope_entries` 테이블에 레코드가 빠르게 쌓일 수 있습니다. 이를 방지하려면 [스케줄러](/docs/{{version}}/scheduling)를 사용해 `telescope:prune` Artisan 명령어를 매일 실행하세요:

    $schedule->command('telescope:prune')->daily();

기본적으로 24시간이 지난 엔트리는 모두 정리합니다. `hours` 옵션을 사용해 얼마나 오래 데이터를 보관할지 지정할 수 있습니다. 예를 들어, 48시간이 지난 레코드를 삭제하려면:

    $schedule->command('telescope:prune --hours=48')->daily();

<a name="dashboard-authorization"></a>
### 대시보드 인증

Telescope 대시보드는 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용됩니다.  
`app/Providers/TelescopeServiceProvider.php` 파일엔 [인증 게이트](/docs/{{version}}/authorization#gates)가 정의되어 있습니다. 이 인증 게이트는 **비로컬** 환경에서 Telescope 접근 권한을 제어합니다. 필요에 따라 이 게이트를 수정해 특정 사용자만 Telescope 대시보드에 접근하도록 제한할 수 있습니다:

    use App\Models\User;

    /**
     * Telescope 게이트 등록
     *
     * 이 게이트는 비로컬 환경의 Telescope 접근 권한을 결정합니다.
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
> 운영 환경의 `APP_ENV` 환경 변수를 반드시 `production`으로 설정해야 합니다. 그렇지 않으면 Telescope가 외부에 공개되어 누구나 접근할 수 있습니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드

Telescope의 새 주요 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

또한, Telescope의 모든 새 버전으로 업그레이드할 때마다 에셋을 다시 퍼블리시해야 합니다:

```shell
php artisan telescope:publish
```

앞으로의 업데이트에서 에셋이 최신 상태로 유지되도록, `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령어를 추가하는 것이 좋습니다:

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

Telescope가 기록하는 데이터를 `App\Providers\TelescopeServiceProvider` 클래스에 정의된 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에선 모든 데이터를 기록하며, 기타 환경에선 예외, 실패한 잡, 예약 작업, 모니터링된 태그의 데이터만 기록합니다:

    use Laravel\Telescope\IncomingEntry;
    use Laravel\Telescope\Telescope;

    /**
     * 애플리케이션 서비스 등록
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

`filter` 클로저는 개별 엔트리에 대한 데이터 필터링을 수행하며, `filterBatch` 메서드를 사용해 하나의 요청이나 콘솔 명령 전체에 대한 엔트리들의 기록 여부를 제어할 수 있습니다. 클로저가 `true`를 반환하면 모든 엔트리가 기록됩니다:

    use Illuminate\Support\Collection;
    use Laravel\Telescope\IncomingEntry;
    use Laravel\Telescope\Telescope;

    /**
     * 애플리케이션 서비스 등록
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
## 태깅

Telescope는 엔트리를 "태그"를 활용해 검색할 수 있게 해줍니다. 일반적으로 태그는 Eloquent 모델의 클래스명이나 인증된 사용자의 ID가 되며, Telescope가 자동으로 엔트리에 추가합니다. 때로, 직접 커스텀 태그를 추가하고 싶을 수 있는데, 이럴 땐 `Telescope::tag` 메서드를 사용하여 클로저를 등록하세요. 이 클로저는 태그 배열을 반환해야 하며, Telescope가 기본적으로 추가하는 태그들과 병합됩니다. 보통은 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출합니다:

    use Laravel\Telescope\IncomingEntry;
    use Laravel\Telescope\Telescope;

    /**
     * 애플리케이션 서비스 등록
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
## 사용 가능한 워처

Telescope의 "워처"는 요청이나 콘솔 명령 실행 시 애플리케이션의 다양한 데이터를 수집합니다. `config/telescope.php` 설정 파일 내에서 활성화할 워처 목록을 커스터마이즈할 수 있습니다:

    'watchers' => [
        Watchers\CacheWatcher::class => true,
        Watchers\CommandWatcher::class => true,
        ...
    ],

일부 워처는 추가 옵션을 제공하기도 합니다:

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 100,
        ],
        ...
    ],

<a name="batch-watcher"></a>
### 배치 워처

배치 워처는 큐에 등록된 [배치 작업](/docs/{{version}}/queues#job-batching)에 대한 정보(잡 정보 및 커넥션 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키에 대한 히트, 미스, 업데이트, 삭제 등 캐시 동작을 기록합니다.

<a name="command-watcher"></a>
### 명령어 워처

명령어 워처는 Artisan 명령어가 실행될 때의 인자, 옵션, 종료 코드, 결과 출력을 기록합니다. 특정 명령을 워처 기록에서 제외하려면, `config/telescope.php` 파일의 `ignore` 옵션에 명령어명을 지정할 수 있습니다:

    'watchers' => [
        Watchers\CommandWatcher::class => [
            'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
            'ignore' => ['key:generate'],
        ],
        ...
    ],

<a name="dump-watcher"></a>
### 덤프 워처

덤프 워처는 Telescope에 변수 덤프를 기록하고 보여줍니다. Laravel을 사용할 경우, 전역 `dump` 함수를 이용할 수 있습니다. 브라우저에서 덤프 워처 탭이 열려 있어야 기록되며, 그렇지 않으면 덤프는 워처에 의해 무시됩니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 발생한 [이벤트](/docs/{{version}}/events)의 페이로드, 리스너, 브로드캐스트 데이터 등을 기록합니다. Laravel 프레임워크의 내부 이벤트는 이벤트 워처에서 무시됩니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생하는 리포팅 가능한 예외의 데이터 및 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### 게이트 워처

게이트 워처는 [게이트 및 폴리시](/docs/{{version}}/authorization) 검증 결과 및 데이터를 기록합니다. 특정 능력(ability)을 기록 대상에서 제외하고 싶다면 `config/telescope.php` 파일의 `ignore_abilities` 옵션에 명시할 수 있습니다:

    'watchers' => [
        Watchers\GateWatcher::class => [
            'enabled' => env('TELESCOPE_GATE_WATCHER', true),
            'ignore_abilities' => ['viewNova'],
        ],
        ...
    ],

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션에서 발생한 [외부 HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 잡 워처

잡 워처는 애플리케이션에서 발생한 [잡](/docs/{{version}}/queues)의 데이터 및 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션이 남긴 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

기본적으로 Telescope는 `error` 레벨 이상의 로그만 기록합니다. 하지만 `config/telescope.php` 파일의 `level` 옵션을 수정해 이 동작을 변경할 수 있습니다:

    'watchers' => [
        Watchers\LogWatcher::class => [
            'enabled' => env('TELESCOPE_LOG_WATCHER', true),
            'level' => 'debug',
        ],

        // ...
    ],

<a name="mail-watcher"></a>
### 메일 워처

메일 워처를 사용하면, 애플리케이션이 전송한 [이메일](/docs/{{version}}/mail)을 브라우저에서 미리 볼 수 있으며, 관련 데이터도 함께 확인할 수 있습니다. 또한 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 모델의 변경 내역을 기록합니다. 워처의 `events` 옵션을 통해 기록할 모델 이벤트를 지정할 수 있습니다:

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
        ],
        ...
    ],

특정 요청에서 하이드레이트된(메모리에 로딩된) 모델의 개수를 기록하려면 `hydrations` 옵션을 활성화하세요:

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

알림 워처는 애플리케이션에서 전송된 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 알림이 이메일을 트리거하고, 메일 워처가 활성화되어 있다면 메일 워처 화면에서도 이메일 미리 보기를 할 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 실행되는 모든 쿼리의 원본 SQL, 바인딩, 실행 시간을 기록합니다. 기본적으로 100ms보다 느린 쿼리는 `slow`로 태그됩니다. 워처의 `slow` 옵션으로 임계값을 변경할 수 있습니다:

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 50,
        ],
        ...
    ],

<a name="redis-watcher"></a>
### Redis 워처

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. 캐시로 Redis를 사용할 경우, 캐시 명령도 함께 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 애플리케이션이 처리한 모든 요청에 대한 요청 정보, 헤더, 세션, 응답 데이터를 기록합니다. `size_limit`(킬로바이트 단위) 옵션을 통해 기록되는 응답 데이터의 용량을 제한할 수 있습니다:

    'watchers' => [
        Watchers\RequestWatcher::class => [
            'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
            'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
        ],
        ...
    ],

<a name="schedule-watcher"></a>
### 스케줄 워처

스케줄 워처는 애플리케이션이 실행한 [예약된 작업](/docs/{{version}}/scheduling)의 명령 및 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 뷰 렌더링 시 사용된 [뷰](/docs/{{version}}/views) 이름, 경로, 데이터, "컴포저" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 각 엔트리를 저장할 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Gravatar 웹 서비스를 이용해 아바타 이미지를 가져옵니다. 하지만, `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 커스터마이즈할 수 있습니다. 이 콜백은 사용자의 ID와 이메일을 받아 아바타 이미지의 URL을 반환해야 합니다:

    use App\Models\User;
    use Laravel\Telescope\Telescope;

    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...

        Telescope::avatar(function (string $id, string $email) {
            return '/avatars/'.User::find($id)->avatar_path;
        });
    }
