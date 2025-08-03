# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [밸런싱 전략](#balancing-strategies)
    - [대시보드 권한 설정](#dashboard-authorization)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [지표](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 삭제](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!TIP]
> Laravel Horizon을 다루기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)에 익숙해져야 합니다. Horizon은 Laravel의 큐에 추가 기능을 더하는데, 기본 큐 기능에 익숙하지 않으면 다소 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/{{version}}/queues)를 위한 아름다운 대시보드와 코드 기반 구성을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패와 같은 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용할 경우, 모든 큐 워커 설정은 단일 간단한 구성 파일에 저장됩니다. 애플리케이션의 워커 구성을 버전 관리 파일에 정의함으로써, 애플리케이션 배포 시 큐 워커를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!NOTE]
> Laravel Horizon은 큐 구동에 [Redis](https://redis.io)를 반드시 사용해야 합니다. 따라서 애플리케이션의 `config/queue.php` 구성 파일에서 큐 연결이 `redis`로 설정되어 있어야 합니다.

Composer 패키지 관리자를 이용해 프로젝트에 Horizon을 설치할 수 있습니다:

```
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어로 관련 자산을 배포하세요:

```
php artisan horizon:install
```

<a name="configuration"></a>
### 설정 (Configuration)

Horizon의 자산을 배포한 다음, 주요 설정 파일은 `config/horizon.php`에 위치합니다. 이 구성 파일에서 애플리케이션의 큐 워커 옵션을 설정할 수 있습니다. 각 옵션에는 용도에 대한 설명이 포함되어 있으니 꼭 자세히 살펴보세요.

> [!NOTE]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 이름은 예약되어 있으므로 `database.php` 설정파일에서나 `horizon.php` 설정 파일의 `use` 옵션 값으로 다른 Redis 연결에 할당하지 않아야 합니다.

<a name="environments"></a>
#### 환경 설정 (Environments)

설치 후에 가장 먼저 익혀야 할 주요 Horizon 설정은 `environments` 옵션입니다. 이 배열은 애플리케이션이 실행될 환경 목록을 정의하며, 각 환경에 대해 워커 프로세스 옵션을 설정합니다. 기본적으로 `production`과 `local` 환경이 들어있지만 필요에 따라 환경을 추가할 수 있습니다:

```
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],

    'local' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

Horizon을 시작할 때는 애플리케이션이 실행되는 환경에 맞는 워커 프로세스 설정을 사용합니다. 보통 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment) 값으로 결정됩니다. 예를 들어, 기본 `local` 환경은 3개의 워커 프로세스를 시작하고 각 큐에 할당된 프로세스를 자동으로 밸런싱하도록 설정되어 있습니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 시작하고 자동 밸런싱을 수행합니다.

> [!NOTE]
> Horizon을 실행하려는 각 [환경](/docs/{{version}}/configuration#environment-configuration)에 대해 `horizon` 설정 파일 내 `environments` 항목이 반드시 포함되어 있어야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저 (Supervisors)

Horizon 기본 설정 파일을 보면, 각 환경은 한 개 이상의 "supervisor"를 포함할 수 있습니다. 기본 설정은 `supervisor-1`이라는 이름을 사용하지만, 원하는 이름으로 자유롭게 변경할 수 있습니다. 각 supervisor는 워커 프로세스 그룹을 감독하고, 큐별 워커 프로세스 수의 밸런싱을 담당합니다.

특정 환경에 새로운 워커 프로세스 그룹을 정의하고 싶다면, 다른 supervisor를 추가할 수도 있습니다. 예를 들어, 애플리케이션에서 사용하는 특정 큐에 대해 다른 밸런싱 전략이나 워커 개수를 지정하고자 할 때 유용합니다.

<a name="default-values"></a>
#### 기본 값 (Default Values)

Horizon 기본 설정 파일에는 `defaults` 옵션이 있습니다. 이 옵션은 애플리케이션 내 각 [supervisor](#supervisors)의 기본값을 지정합니다. 각 환경의 supervisor 별 설정에 이 기본값들이 병합되어 중복된 설정 작성을 줄일 수 있습니다.

<a name="balancing-strategies"></a>
### 밸런싱 전략 (Balancing Strategies)

Laravel 기본 큐 시스템과 달리, Horizon은 `simple`, `auto`, `false` 세 가지 워커 밸런싱 전략을 제공합니다. 기본값인 `simple` 전략은 들어오는 작업을 워커 프로세스 간 균등하게 분배합니다:

```
'balance' => 'simple',
```

`auto` 전략은 큐의 현재 작업량에 따라 워커 프로세스 수를 동적으로 조절합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고 `render` 큐는 비어 있을 경우, Horizon은 `notifications` 큐에 더 많은 워커를 할당하여 대기 작업이 없을 때까지 처리합니다.

`auto` 전략을 사용할 때, `minProcesses`와 `maxProcesses` 옵션을 통해 워커 프로세스의 최소/최대 개수를 지정할 수 있습니다:

```
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default'],
            'balance' => 'auto',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
            'tries' => 3,
        ],
    ],
],
```

`balanceMaxShift`와 `balanceCooldown` 값은 워커 수를 확장/축소하는 속도를 제어합니다. 위 예시에서 3초마다 최대 1개의 프로세스만 새로 생성하거나 종료할 수 있습니다. 애플리케이션 상황에 따라 이 값을 조정할 수 있습니다.

`balance` 옵션을 `false`로 설정하면 Laravel 기본 동작이 적용되어, 설정에 나열된 순서대로 큐를 처리합니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Horizon은 `/horizon` URI에 대시보드를 노출합니다. 기본적으로는 `local` 환경에서만 접근할 수 있습니다. `app/Providers/HorizonServiceProvider.php` 파일 내에는 [authorization gate](/docs/{{version}}/authorization#gates)가 정의되어 있어서, **비로컬 환경**에서의 Horizon 접근 권한을 제어합니다. 필요에 따라 이 게이트를 수정해 Horizon 접근을 제한할 수 있습니다:

```
/**
 * Register the Horizon gate.
 *
 * This gate determines who can access Horizon in non-local environments.
 *
 * @return void
 */
protected function gate()
{
    Gate::define('viewHorizon', function ($user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

<a name="alternative-authentication-strategies"></a>
#### 대체 인증 전략 (Alternative Authentication Strategies)

Laravel은 gate 클로저에 자동으로 인증된 사용자를 주입합니다. 만약 애플리케이션에서 IP 제한 같은 다른 방식으로 Horizon 보안을 제공하는 경우, 사용자가 로그인할 필요가 없을 수 있습니다. 이 경우 위 `function ($user)` 클로저 시그니처를 `function ($user = null)`로 변경해야 Laravel이 인증을 요구하지 않도록 할 수 있습니다.

<a name="upgrading-horizon"></a>
## Horizon 업그레이드 (Upgrading Horizon)

Horizon 메이저 버전 업그레이드 시, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다. 그리고 모든 버전 업그레이드 후에는 Horizon 자산을 다시 배포해야 합니다:

```
php artisan horizon:publish
```

향후 업데이트 시 자산 관련 문제를 방지하려면, 애플리케이션의 `composer.json` 파일 내 `post-update-cmd` 스크립트에 `horizon:publish` 명령을 추가할 수 있습니다:

```
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan horizon:publish --ansi"
        ]
    }
}
```

<a name="running-horizon"></a>
## Horizon 실행 (Running Horizon)

애플리케이션의 `config/horizon.php`에서 supervisor와 워커를 설정한 후, 다음 Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 단일 명령어가 현재 환경에 설정된 모든 워커 프로세스를 실행합니다:

```
php artisan horizon
```

Horizon 프로세스를 일시 중지하거나 작업 처리를 다시 시작하려면 각각 `horizon:pause`와 `horizon:continue` 명령을 사용하세요:

```
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [supervisor](#supervisors)를 일시 중지하거나 다시 시작하려면 다음 명령어를 사용합니다:

```
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스 상태는 다음 명령어로 확인할 수 있습니다:

```
php artisan horizon:status
```

`horizon:terminate` 명령으로 Horizon 프로세스를 안전하게 종료할 수 있습니다. 현재 처리 중인 작업은 완료 후 종료됩니다:

```
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포 (Deploying Horizon)

Horizon을 실제 서버에 배포할 때는 `php artisan horizon` 명령을 모니터링하고 비정상 종료 시 자동 재시작하는 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설치 방법을 설명합니다.

배포 과정에서는 Horizon 프로세스를 종료시키고, 프로세스 모니터가 재시작하여 코드 변경 사항을 반영하도록 해야 합니다:

```
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치 (Installing Supervisor)

Supervisor는 Linux용 프로세스 모니터로, `horizon` 프로세스가 중단되면 자동으로 재시작합니다. Ubuntu에서는 다음 명령어로 설치할 수 있습니다. Ubuntu 외 다른 OS도 해당 OS 패키지 관리자를 통해 설치할 수 있습니다:

```
sudo apt-get install supervisor
```

> [!TIP]
> Supervisor 구성에 어려움이 있다면, Laravel 프로젝트를 위한 Supervisor를 자동 설치 및 구성해 주는 [Laravel Forge](https://forge.laravel.com)를 사용하는 것도 고려해 보세요.

<a name="supervisor-configuration"></a>
#### Supervisor 구성 (Supervisor Configuration)

Supervisor 구성 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 디렉토리에 여러 개의 구성 파일을 만들어 프로세스 모니터링 설정을 할 수 있습니다. 예를 들어, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작하고 모니터링하도록 설정할 수 있습니다:

```
[program:horizon]
process_name=%(program_name)s
command=php /home/forge/example.com/artisan horizon
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/horizon.log
stopwaitsecs=3600
```

> [!NOTE]
> `stopwaitsecs` 값은 가장 오래 걸리는 작업의 실행 시간보다 커야 합니다. 그렇지 않으면 Supervisor가 작업 완료 전에 강제로 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작 (Starting Supervisor)

구성 파일이 준비되면 다음 명령어로 Supervisor 설정을 갱신하고, 모니터링 프로세스를 시작합니다:

```
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!TIP]
> Supervisor 사용에 대한 추가 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 메일, 브로드캐스트 이벤트, 알림 및 큐잉된 이벤트 리스너 등의 작업에 “태그”를 지정할 수 있습니다. 실제로, Horizon은 대부분의 작업에 연결된 Eloquent 모델에 따라 자동으로 적절한 태그를 똑똑하게 할당합니다. 예를 들어, 다음 작업을 보세요:

```
<?php

namespace App\Jobs;

use App\Models\Video;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class RenderVideo implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * The video instance.
     *
     * @var \App\Models\Video
     */
    public $video;

    /**
     * Create a new job instance.
     *
     * @param  \App\Models\Video  $video
     * @return void
     */
    public function __construct(Video $video)
    {
        $this->video = $video;
    }

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        //
    }
}
```

이 작업이 `id` 속성이 `1`인 `App\Models\Video` 인스턴스로 큐잉되면, 자동으로 `App\Models\Video:1` 태그가 지정됩니다. 이는 Horizon이 작업 속성에서 Eloquent 모델을 탐색하여, 모델 클래스명과 기본 키를 조합해 태그를 만들어내기 때문입니다:

```
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 수동 태그 지정 (Manually Tagging Jobs)

큐잉 가능한 작업 클래스에 직접 태그를 지정하고 싶다면, `tags` 메서드를 정의할 수 있습니다:

```
class RenderVideo implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the job.
     *
     * @return array
     */
    public function tags()
    {
        return ['render', 'video:'.$this->video->id];
    }
}
```

<a name="notifications"></a>
## 알림 (Notifications)

> [!NOTE]
> Horizon에서 Slack 또는 SMS 알림을 설정할 때는 관련 알림 채널의 [사전 요구 사항](/docs/{{version}}/notifications)을 반드시 확인하세요.

큐가 오랜 대기 시간을 가질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 애플리케이션 `App\Providers\HorizonServiceProvider` 클래스의 `boot` 메서드에서 호출하세요:

```
/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    parent::boot();

    Horizon::routeSmsNotificationsTo('15556667777');
    Horizon::routeMailNotificationsTo('example@example.com');
    Horizon::routeSlackNotificationsTo('slack-webhook-url', '#channel');
}
```

<a name="configuring-notification-wait-time-thresholds"></a>
#### 알림 대기 시간 임계값 설정 (Configuring Notification Wait Time Thresholds)

오래 대기하는 시간을 몇 초로 간주할지 `config/horizon.php` 설정 파일의 `waits` 옵션에서 환경별로 제어할 수 있습니다:

```
'waits' => [
    'redis:default' => 60,
    'redis:critical,high' => 90,
],
```

<a name="metrics"></a>
## 지표 (Metrics)

Horizon은 작업 및 큐 대기 시간, 처리량 등 정보를 제공하는 지표 대시보드를 포함합니다. 이 대시보드를 채우기 위해, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에서 매 5분마다 Horizon의 `snapshot` Artisan 명령어를 실행하도록 설정해야 합니다:

```
/**
 * Define the application's command schedule.
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('horizon:snapshot')->everyFiveMinutes();
}
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제 (Deleting Failed Jobs)

실패한 작업을 삭제하고 싶으면 `horizon:forget` 명령을 사용할 수 있습니다. 이 명령은 삭제할 실패 작업의 ID 또는 UUID를 인수로 받습니다:

```
php artisan horizon:forget 5
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제 (Clearing Jobs From Queues)

애플리케이션 기본 큐에서 모든 작업을 삭제하고 싶다면 `horizon:clear` Artisan 명령어를 사용하세요:

```
php artisan horizon:clear
```

특정 큐의 작업만 삭제하려면 `queue` 옵션을 지정할 수 있습니다:

```
php artisan horizon:clear --queue=emails
```