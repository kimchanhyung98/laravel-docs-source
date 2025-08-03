# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 권한 설정](#dashboard-authorization)
    - [무음 처리된 작업](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행하기](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [지표](#metrics)
- [실패한 작업 삭제하기](#deleting-failed-jobs)
- [큐에서 작업 삭제하기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> Laravel Horizon을 자세히 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/master/queues)를 먼저 익히는 것이 좋습니다. Horizon은 Laravel의 큐 기능을 확장하여 추가 기능을 제공하는데, 기본 큐 기능에 익숙하지 않다면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/master/queues)를 위한 깔끔한 대시보드와 코드 기반 구성을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패 등 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 작업자(worker) 설정이 하나의 간단한 구성 파일에 저장됩니다. 애플리케이션의 작업자 구성을 버전 관리되는 파일에 정의함으로써 배포 시 작업자를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Laravel Horizon은 큐 동작에 [Redis](https://redis.io)를 사용합니다. 따라서 `config/queue.php` 파일에서 애플리케이션의 큐 연결이 `redis`로 설정되어 있는지 반드시 확인하세요.

Composer 패키지 매니저를 사용하여 프로젝트에 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

Horizon을 설치한 후, `horizon:install` Artisan 명령어를 실행하여 에셋을 공개하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 구성 (Configuration)

Horizon의 에셋을 공개하면 주 구성 파일이 `config/horizon.php`에 생성됩니다. 이 구성 파일을 통해 애플리케이션의 큐 작업자(worker) 옵션을 설정할 수 있습니다. 각 설정 항목은 목적에 대한 설명이 포함되어 있으므로 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 Redis 연결 이름을 사용하므로, 이 이름을 `database.php` 파일이나 `horizon.php` 설정 파일의 `use` 옵션에서 다른 연결 이름으로 사용해서는 안 됩니다.

<a name="environments"></a>
#### 환경 (Environments)

설치 후 가장 먼저 익혀야 할 Horizon의 주요 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 실행되는 각 환경별로 작업자 프로세스 옵션을 정의하는 배열입니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만, 필요에 따라 추가 환경을 자유롭게 정의할 수 있습니다:

```php
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

또한, 다른 환경과 매칭되지 않을 때 사용되는 와일드카드 환경(`*`)을 정의할 수도 있습니다:

```php
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

Horizon을 시작할 때 현재 애플리케이션이 실행 중인 환경의 작업자 프로세스 설정을 사용합니다. 일반적으로 환경은 `APP_ENV` [환경 변수](/docs/master/configuration#determining-the-current-environment)의 값으로 결정됩니다. 예를 들어, 기본 `local` 환경은 작업자 프로세스 3개를 시작하고 큐별 작업자 수를 자동으로 조정하도록 구성되어 있습니다. 기본 `production` 환경은 최대 10개의 작업자 프로세스를 시작하고 자동으로 균형을 맞춥니다.

> [!WARNING]
> `horizon` 구성 파일의 `environments` 항목에 Horizon을 실행할 모든 [환경](/docs/master/configuration#environment-configuration)에 대한 정의가 반드시 포함되어 있는지 확인하세요.

<a name="supervisors"></a>
#### 감독자 (Supervisors)

Horizon 기본 구성 파일을 보면, 각 환경에 하나 이상의 "supervisor"(감독자)를 정의할 수 있습니다. 기본 구성에서는 `supervisor-1`로 명명되어 있지만, 원하는 이름으로 변경 가능합니다. 각 감독자는 작업자 프로세스 그룹을 감독하고 큐별 작업자 프로세스 개수를 균형 있게 관리합니다.

필요하다면 환경별로 새로운 작업자 그룹을 위해 더 많은 감독자를 추가할 수 있습니다. 예를 들어, 애플리케이션에서 사용하는 특정 큐에 대해 다른 부하 분산 전략이나 작업자 수를 설정하고자 할 때 유용합니다.

<a name="maintenance-mode"></a>
#### 유지 모드 (Maintenance Mode)

애플리케이션이 [유지 모드](/docs/master/configuration#maintenance-mode)에 있을 때는 Horizon이 큐 작업을 처리하지 않습니다. 다만, Horizon 구성 파일 내 각 감독자의 `force` 옵션을 `true`로 설정하면 작업 처리를 강제할 수 있습니다:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'force' => true,
        ],
    ],
],
```

<a name="default-values"></a>
#### 기본 값 (Default Values)

Horizon 기본 설정 파일에는 `defaults` 옵션이 있습니다. 이 옵션을 통해 애플리케이션의 [감독자](#supervisors)에 대한 기본 값을 지정할 수 있습니다. 각 환경별 감독자 설정에 이 기본 값들이 합쳐져서 중복 정의를 줄이고 편리하게 사용할 수 있습니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략 (Balancing Strategies)

Laravel 기본 큐 시스템과 달리, Horizon은 세 가지 작업자 부하 분산 전략 중 선택할 수 있습니다: `simple`, `auto`, `false`. 

- `simple` 전략은 들어오는 작업을 작업자 프로세스에 균등하게 분배합니다:

```
'balance' => 'simple',
```

- 기본 설정인 `auto` 전략은 큐의 현재 작업 부하에 따라 큐별 작업자 수를 조절합니다. 예를 들어, `notifications` 큐에 미처리 작업이 1,000건인 반면 `render` 큐는 비어 있다면, Horizon은 작업이 모두 처리될 때까지 `notifications` 큐에 더 많은 작업자를 할당합니다.

`auto` 전략 사용 시 다음 옵션으로 큐별 최소 및 최대 작업자 수와 Horizon 전체의 최대 작업자 수를 제어할 수 있습니다:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
            'tries' => 3,
        ],
    ],
],
```

- `autoScalingStrategy`는 큐를 비우는 데 걸리는 총 시간(`time` 전략)이나 큐에 쌓인 작업 수(`size` 전략)를 기준으로 작업자 수를 조절할지 결정합니다.
- `balanceMaxShift`와 `balanceCooldown`은 작업자 수를 변경하는 속도를 조절합니다. 위 예시에서는 3초마다 최대 1개의 프로세스가 생성 또는 종료됩니다. 애플리케이션 요구에 맞게 값을 조정할 수 있습니다.

`balance` 옵션을 `false`로 설정하면 기본 Laravel 큐 동작으로 돌아가며, 설정된 큐 목록 순서대로 작업을 처리합니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Horizon 대시보드는 기본적으로 `/horizon` 경로에서 접근 가능합니다. 기본 설정에서는 `local` 환경에서만 접근할 수 있습니다. 그 외 환경에서는 `app/Providers/HorizonServiceProvider.php` 파일의 [authorization gate](/docs/master/authorization#gates)에 정의된 권한 게이트가 접근을 제어합니다. 필요에 따라 이 게이트를 수정하여 Horizon 접근을 제한할 수 있습니다:

```php
/**
 * Register the Horizon gate.
 *
 * 이 게이트는 non-local 환경에서 Horizon 접근 권한을 결정합니다.
 */
protected function gate(): void
{
    Gate::define('viewHorizon', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

<a name="alternative-authentication-strategies"></a>
#### 대체 인증 전략

Laravel은 인증된 사용자를 자동으로 게이트 클로저에 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 접근 보안을 설정했다면 사용자가 로그인을 반드시 할 필요가 없을 수 있습니다. 이 경우 게이트 메서드의 시그니처를 `function (User $user)`에서 `function (User $user = null)`로 변경하여 인증을 강제하지 않도록 할 수 있습니다.

<a name="silenced-jobs"></a>
### 무음 처리된 작업 (Silenced Jobs)

애플리케이션이나 서드파티 패키지에서 디스패치하는 특정 작업을 Horizon의 "완료된 작업" 목록에서 보고 싶지 않을 때가 있습니다. 이런 경우 작업을 무음 처리하여 목록에 표시되지 않게 할 수 있습니다. 시작하려면 무음 처리할 작업 클래스 이름을 `horizon` 구성 파일의 `silenced` 옵션에 추가하세요:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또한, 무음 처리할 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 할 수 있습니다. 이 인터페이스를 구현하면 `silenced` 배열에 없어도 자동으로 무음 처리됩니다:

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="upgrading-horizon"></a>
## Horizon 업그레이드 (Upgrading Horizon)

Horizon의 메이저 버전을 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토하시기 바랍니다.

<a name="running-horizon"></a>
## Horizon 실행하기 (Running Horizon)

애플리케이션의 `config/horizon.php`에서 감독자와 작업자 구성을 완료하면, 다음 Artisan 명령으로 Horizon을 시작할 수 있습니다. 이 명령은 현재 환경에 대해 설정된 모든 작업자 프로세스를 실행합니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지하고 작업 처리를 재개하려면 다음 명령을 사용하세요:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [감독자](#supervisors)를 일시 중지하거나 다시 시작하려면 다음 명령을 사용합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon 프로세스 상태를 확인하려면 다음 명령을 사용하세요:

```shell
php artisan horizon:status
```

특정 Horizon 감독자의 상태는 다음 명령으로 확인할 수 있습니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상 종료하려면 다음 명령어를 실행합니다. 처리 중인 작업은 완료되고 Horizon 실행이 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포 (Deploying Horizon)

실제 서버에 Horizon을 배포할 때는 프로세스 모니터(process monitor)를 설정하여 `php artisan horizon` 명령이 예기치 않게 종료될 경우 자동으로 재시작하도록 구성하는 것이 좋습니다. 프로세스 모니터 설치 및 설정 방법은 아래에서 설명합니다.

배포 과정 중에는 Horizon 프로세스를 종료하도록 지시하고, 프로세스 모니터가 이를 감지해 재시작하게 하여 최신 코드를 반영하도록 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치 (Installing Supervisor)

Supervisor는 Linux 운영체제에서 프로세스를 감시하고 `horizon` 프로세스가 멈출 경우 자동으로 재시작하는 도구입니다. Ubuntu에서는 아래 명령어로 설치할 수 있으며, 다른 운영체제에서는 해당 OS의 패키지 관리자를 통해 설치하세요:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 부담스럽다면, Laravel 애플리케이션의 백그라운드 프로세스를 관리해주는 [Laravel Cloud](https://cloud.laravel.com)를 고려해보세요.

<a name="supervisor-configuration"></a>
#### Supervisor 구성 (Supervisor Configuration)

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 경로에 프로세스 모니터링 관련 설정 파일을 여러 개 생성할 수 있습니다. 예를 들어, `horizon.conf` 파일을 생성하여 `horizon` 프로세스를 시작하고 감시하도록 설정할 수 있습니다:

```ini
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

`stopwaitsecs` 값을 가장 오래 걸리는 작업보다 길게 설정해야 합니다. 그렇지 않으면 Supervisor가 작업 종료 전에 프로세스를 강제 종료할 수 있습니다.

> [!WARNING]
> 위 예제는 Ubuntu 기반 서버에 적합하며, 다른 서버 운영체제에서는 Supervisor 구성 파일의 위치 및 확장자가 다를 수 있습니다. 자세한 사항은 서버 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기 (Starting Supervisor)

설정 파일 생성 후 다음 명령어를 이용해 Supervisor 설정을 재읽기하고 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 사용법에 대한 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 메일러블, 방송 이벤트, 알림, 큐 이벤트 리스너 등 다양한 작업에 “태그”를 붙일 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델을 감지하여 자동으로 해당 모델의 클래스 이름과 기본 키를 태그로 지정합니다.

예를 들어, 다음 작업을 살펴보세요:

```php
<?php

namespace App\Jobs;

use App\Models\Video;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class RenderVideo implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        // ...
    }
}
```

이 작업이 `id`가 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 추가되면, 자동으로 `App\Models\Video:1` 태그가 붙습니다. 이는 Horizon이 작업의 속성에서 Eloquent 모델을 찾아내어 클래스명과 기본 키로 태그를 만들기 때문입니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 수동 태그 지정 (Manually Tagging Jobs)

큐에 추가되는 객체에 대해 직접 태그를 지정하고 싶다면, 해당 클래스에 `tags` 메서드를 정의할 수 있습니다:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * 이 작업에 할당할 태그를 반환합니다.
     *
     * @return array<int, string>
     */
    public function tags(): array
    {
        return ['render', 'video:'.$this->video->id];
    }
}
```

<a name="manually-tagging-event-listeners"></a>
#### 이벤트 리스너의 수동 태그 지정

큐에 추가되는 이벤트 리스너의 태그를 가져올 때, Horizon은 이벤트 인스턴스를 `tags` 메서드에 자동으로 전달해 이벤트 데이터를 태그에 포함시킬 수 있게 합니다:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 할당할 태그를 반환합니다.
     *
     * @return array<int, string>
     */
    public function tags(VideoRendered $event): array
    {
        return ['video:'.$event->video->id];
    }
}
```

<a name="notifications"></a>
## 알림 (Notifications)

> [!WARNING]
> Horizon에서 Slack 또는 SMS 알림을 구성할 때는 해당 알림 채널의 [사전 요구 사항](/docs/master/notifications)을 꼭 확인하세요.

큐 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider` 내 `boot` 메서드에서 호출하세요:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    parent::boot();

    Horizon::routeSmsNotificationsTo('15556667777');
    Horizon::routeMailNotificationsTo('example@example.com');
    Horizon::routeSlackNotificationsTo('slack-webhook-url', '#channel');
}
```

<a name="configuring-notification-wait-time-thresholds"></a>
#### 알림 대기 시간 임계값 설정

앱의 `config/horizon.php` 파일에서 `waits` 옵션으로 각 연결/큐 조합의 "긴 대기" 기준(초 단위)을 설정할 수 있습니다. 정의되지 않은 조합은 기본 60초를 사용합니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 지표 (Metrics)

Horizon은 작업 및 큐 대기 시간과 처리량에 관한 정보를 제공하는 지표 대시보드를 포함합니다. 이 대시보드를 채우려면, 앱의 `routes/console.php` 파일에 Horizon의 `snapshot` Artisan 명령이 5분마다 실행되도록 예약해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제하기 (Deleting Failed Jobs)

실패한 작업을 삭제하려면 `horizon:forget` 명령을 사용합니다. 이 명령은 실패 작업의 ID 또는 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패 작업을 삭제하려면 `--all` 옵션을 추가하세요:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제하기 (Clearing Jobs From Queues)

애플리케이션의 기본 큐에서 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용하면 됩니다:

```shell
php artisan horizon:clear
```

특정 큐에서 작업들만 삭제하려면 `--queue` 옵션을 사용하세요:

```shell
php artisan horizon:clear --queue=emails
```