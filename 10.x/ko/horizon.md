# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 권한 설정](#dashboard-authorization)
    - [무시된 작업](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 삭제](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]  
> Laravel Horizon을 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/10.x/queues)를 숙지하는 것이 좋습니다. Horizon은 Laravel 큐에 추가 기능을 더해주기 때문에, 기본 큐 기능에 익숙하지 않으면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel에서 구동하는 [Redis 큐](/docs/10.x/queues)를 위한 훌륭한 대시보드와 코드 기반 설정을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 실패 작업과 같은 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용할 때, 모든 큐 작업자(worker)의 설정이 하나의 간단한 설정 파일에 저장됩니다. 버전 관리가 가능한 설정 파일에 애플리케이션의 작업자 구성을 정의하면, 배포 시 작업자의 수를 손쉽게 조정하거나 변경할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> Laravel Horizon은 큐를 구동하기 위해 반드시 [Redis](https://redis.io)를 사용해야 합니다. 따라서 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 설정되어 있는지 반드시 확인하세요.

Composer 패키지 관리자를 통해 프로젝트에 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어를 사용해 Horizon의 자산을 배포합니다:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정 (Configuration)

Horizon의 자산을 배포하면, 주요 설정 파일은 `config/horizon.php`에 위치하게 됩니다. 이 파일에서 애플리케이션의 큐 작업자 옵션을 설정할 수 있으며, 각 설정 옵션에 대한 설명도 포함되어 있으니 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]  
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 이름은 예약되어 있으므로 `database.php` 설정 파일이나 `horizon.php`의 `use` 옵션에서 다른 Redis 연결 이름으로 사용하면 안 됩니다.

<a name="environments"></a>
#### 환경 설정 (Environments)

설치 후 익숙해져야 할 주요 Horizon 설정 옵션은 `environments`입니다. 이 배열은 애플리케이션이 실행되는 환경들을 나타내며, 각 환경별 작업자 프로세스 설정을 정의합니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만 필요에 따라 환경을 추가할 수 있습니다:

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

Horizon을 시작하면, 애플리케이션이 실행 중인 환경에 따라 해당 환경의 작업자 프로세스 설정이 사용됩니다. 일반적으로 `APP_ENV` [환경 변수](/docs/10.x/configuration#determining-the-current-environment)의 값에 의해 환경이 결정됩니다. 예를 들어 기본 `local` 환경은 3개의 작업자 프로세스를 시작하며, 자동으로 각 큐에 할당된 작업자 프로세스 수를 균형 맞추게 설정되어 있습니다. 기본 `production` 환경은 최대 10개의 작업자 프로세스를 시작하고 자동 부하 분산이 설정되어 있습니다.

> [!WARNING]  
> `horizon` 설정 파일의 `environments` 부분에 Horizon을 실행할 모든 [환경](/docs/10.x/configuration#environment-configuration)에 대한 설정이 반드시 포함되어 있어야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저 (Supervisors)

Horizon의 기본 설정 파일에서 보듯, 각 환경은 하나 이상의 "슈퍼바이저"를 포함할 수 있습니다. 기본적으로 `supervisor-1`로 명명되어 있지만 원하는 이름으로 변경할 수 있습니다. 각 슈퍼바이저는 작업자 프로세스 그룹을 관리하며, 큐에 분산할 작업자 수를 균형 있게 조정하는 역할을 담당합니다.

특정 환경에 여러 감독 그룹을 정의하고 싶다면, 추가 슈퍼바이저를 설정할 수 있습니다. 예를 들어, 애플리케이션에서 사용하는 큐별로 다른 작업자 수나 부하 분산 전략을 적용하고 싶을 때 편리합니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드 (Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/10.x/configuration#maintenance-mode)일 때는, Horizon이 큐 작업을 처리하지 않습니다. 다만, Horizon 설정 파일에서 해당 슈퍼바이저의 `force` 옵션이 `true`로 설정되어 있다면 예외입니다:

```
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
#### 기본값 (Default Values)

Horizon 기본 설정 파일에는 `defaults` 설정 옵션도 있습니다. 이는 애플리케이션의 모든 [슈퍼바이저](#supervisors)에 적용되는 기본값으로, 환경별 슈퍼바이저 설정과 병합되어 불필요한 반복을 줄여줍니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략 (Balancing Strategies)

Laravel 기본 큐 시스템과 달리, Horizon은 세 가지 워커 부하 분산 전략인 `simple`, `auto`, `false` 중 선택할 수 있습니다. 

- `simple` 전략은 들어오는 작업들을 작업자 프로세스 간에 균등하게 분배합니다:

```
'balance' => 'simple',
```

- `auto` 전략(기본값)은 각 큐의 현재 작업량에 따라 작업자 프로세스 수를 조절합니다. 예를 들어 `notifications` 큐에 1,000개의 대기 작업이 있고 `render` 큐는 비어 있을 때, Horizon은 `notifications` 큐에 더 많은 작업자를 할당해 큐가 비워질 때까지 자동 확장합니다.

`auto` 전략 사용 시 `minProcesses`와 `maxProcesses` 옵션으로 Horizon이 확장·축소할 작업자 수의 최소 및 최대값을 지정할 수 있습니다:

```
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

`autoScalingStrategy`는 Horizon이 큐에 작업자 프로세스를 추가할지 결정할 때 큐를 비우는 데 걸리는 전체 시간(`time` 전략) 또는 대기 중 작업 개수(`size` 전략)를 기준으로 합니다.

`balanceMaxShift`와 `balanceCooldown`은 Horizon이 작업자 수를 얼마나 빠르게 조정할지 결정합니다. 위 예시에서는 최대 한 개 작업자를 3초마다 새로 생성하거나 종료합니다. 애플리케이션 상황에 따라 적절히 조정하세요.

- `balance` 옵션이 `false`로 설정되면 기본 Laravel의 행동대로 큐 목록 순서대로 작업을 처리합니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Horizon 대시보드는 기본적으로 `/horizon` 경로로 접근합니다. 기본 설정으로는 `local` 환경에서만 접근이 허용됩니다. `app/Providers/HorizonServiceProvider.php` 파일에 정의된 [권한 게이트](/docs/10.x/authorization#gates)가 비-로컬 환경에서 접근 제어를 담당합니다. 필요한 경우 이 게이트를 수정해 Horizon 접근을 제한할 수 있습니다:

```
/**
 * Horizon 게이트 등록.
 *
 * 이 게이트는 비-로컬 환경에서 Horizon에 접근할 사용자를 결정합니다.
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

Laravel은 권한 게이트 클로저에 자동으로 인증된 사용자를 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 보안을 제공한다면 사용자가 로그인을 하지 않아도 됩니다. 이 경우, 위 클로저 시그니처를 `function (User $user = null)`로 변경하여 인증이 강제되지 않도록 만들어야 합니다.

<a name="silenced-jobs"></a>
### 무시된 작업 (Silenced Jobs)

가끔 애플리케이션이나 서드파티 패키지에서 디스패치한 작업 중 보고 싶지 않은 작업이 있을 수 있습니다. 이 경우 ‘완료된 작업’ 목록 공간을 차지하지 않도록 무시할 수 있습니다. 시작하려면 `horizon` 설정 파일의 `silenced` 옵션에 해당 작업 클래스명을 추가하세요:

```
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는 작업 클래스가 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, `silenced` 배열에 없어도 자동으로 무시됩니다:

```
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    // ...
}
```

<a name="upgrading-horizon"></a>
## Horizon 업그레이드 (Upgrading Horizon)

Horizon의 새 메이저 버전으로 업그레이드 시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 읽는 것이 중요합니다. 또한, 새로운 버전으로 업그레이드 할 때마다 Horizon 자산을 다시 배포하는 것이 좋습니다:

```shell
php artisan horizon:publish
```

자산을 최신 상태로 유지하고 앞으로 발생할 문제를 방지하기 위해 애플리케이션의 `composer.json` 파일에 아래 명령을 `post-update-cmd` 스크립트에 추가할 수 있습니다:

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="running-horizon"></a>
## Horizon 실행 (Running Horizon)

애플리케이션의 `config/horizon.php` 설정 파일에서 슈퍼바이저와 작업자를 모두 설정한 후, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령어는 현재 환경에 대해 구성된 모든 작업자 프로세스를 시작합니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중단하거나 다시 계속 처리하도록 할 수 있으며, 각각 `horizon:pause`와 `horizon:continue` Artisan 명령어를 사용합니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)별로도 일시 중단 및 재시작이 가능하며, `horizon:pause-supervisor`와 `horizon:continue-supervisor` 명령어를 사용합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스 상태를 확인하려면 `horizon:status`를 사용하세요:

```shell
php artisan horizon:status
```

유예를 두고 Horizon 프로세스를 우아하게 종료하려면 `horizon:terminate`를 사용합니다. 현재 실행 중인 작업들은 완료된 후에 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포 (Deploying Horizon)

실제 서버에 Horizon을 배포할 준비가 되면, `php artisan horizon` 명령어를 모니터링하는 프로세스 모니터(process monitor)를 설정해 예기치 않은 종료 시 자동으로 재시작하도록 합니다. 아래에서 프로세스 모니터 설치 방법을 안내합니다.

배포 과정 중에는 Horizon 프로세스를 종료해 프로세스 모니터가 이를 인식하고 자동으로 재시작하며 최신 코드를 반영할 수 있도록 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터로, `horizon` 프로세스가 종료되면 자동으로 재시작합니다. Ubuntu에서는 다음 명령어로 설치합니다. 다른 운영체제의 경우 해당 운영체제 패키지 관리자를 이용해 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> Supervisor 설정이 어렵게 느껴진다면, [Laravel Forge](https://forge.laravel.com)를 사용해보세요. 자동으로 Supervisor 설치 및 구성을 해줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이곳에 여러 개의 설정 파일을 생성해 Supervisor가 프로세스를 어떤 방식으로 모니터링할지 정의할 수 있습니다. 예를 들어, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작하고 모니터링하도록 설정할 수 있습니다:

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

설정 시 `stopwaitsecs` 값은 애플리케이션에서 가장 오래 걸리는 작업 실행 시간보다 길게 설정해야 합니다. 그렇지 않으면 Supervisor가 작업 처리 완료 전에 프로세스를 강제로 종료할 수 있습니다.

> [!WARNING]  
> 위 예는 Ubuntu 기반 서버에 적합한 설정이며, 다른 운영체제에서는 Supervisor 설정 파일 위치나 확장자가 다를 수 있습니다. 서버 문서를 참조하세요.

<a name="starting-supervisor"></a>
#### Supervisor 실행

설정 파일을 생성한 후, 아래 명령어로 Supervisor를 재읽고 설정을 반영하며 `horizon` 프로세스를 시작합니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]  
> Supervisor 관련 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 메일러블(mailables), 브로드캐스트 이벤트, 알림, 큐에 담긴 이벤트 리스너 등 대부분 작업에 "태그"를 지정할 수 있습니다. 특히 Horizon은 작업 객체에 붙은 Eloquent 모델을 탐색해 자동으로 적절한 태그를 지정합니다. 예를 들어 다음 작업을 보겠습니다:

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
     * 새 작업 인스턴스 생성자
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * 작업 실행
     */
    public function handle(): void
    {
        // ...
    }
}
```

이 작업이 `id`가 `1`인 `App\Models\Video` 인스턴스를 큐에 넣으면, Horizon은 자동으로 태그 `App\Models\Video:1`을 붙입니다. 이는 작업 객체 속성에서 Eloquent 모델을 찾아 해당 모델의 클래스명과 기본 키를 기반으로 태깅하기 때문입니다:

```
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업 수동 태그 지정

원하는 경우, 작업 클래스 내에 `tags` 메서드를 정의해 직접 태그를 지정할 수 있습니다:

```
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 할당할 태그 반환
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
#### 이벤트 리스너 수동 태그 지정

큐에 담긴 이벤트 리스너의 태그를 가져올 때, Horizon은 이벤트 인스턴스를 `tags` 메서드에 전달합니다. 이를 활용해 이벤트 데이터를 태그에 포함할 수 있습니다:

```
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 할당할 태그 반환
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
> Horizon에 Slack 또는 SMS 알림을 설정할 때는 [해당 알림 채널의 사전 요구사항](/docs/10.x/notifications)을 반드시 확인하세요.

특정 큐의 대기 시간이 길 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용하세요. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출할 수 있습니다:

```
/**
 * 애플리케이션 서비스 부트스트랩
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

대기 시간이 얼마나 길어야 "장시간 대기"로 간주될지 `config/horizon.php` 설정 파일의 `waits` 옵션에서 조절할 수 있습니다. 지정하지 않은 연결/큐 조합은 기본값 60초가 적용됩니다:

```
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭 (Metrics)

Horizon은 작업 및 큐 대기 시간, 처리량에 관한 정보를 제공하는 메트릭 대시보드를 포함합니다. 이 대시보드를 채우기 위해, 애플리케이션의 [스케줄러](/docs/10.x/scheduling)를 이용해 매 5분마다 Horizon의 `snapshot` Artisan 명령어를 실행하도록 설정하세요:

```
/**
 * 애플리케이션 명령어 스케줄 정의
 */
protected function schedule(Schedule $schedule): void
{
    $schedule->command('horizon:snapshot')->everyFiveMinutes();
}
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제 (Deleting Failed Jobs)

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용하세요. 삭제할 작업의 ID 또는 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제 (Clearing Jobs From Queues)

애플리케이션의 기본 큐에서 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan horizon:clear
```

특정 큐에서 작업을 삭제하려면 `queue` 옵션을 제공합니다:

```shell
php artisan horizon:clear --queue=emails
```