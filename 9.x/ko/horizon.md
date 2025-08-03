# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 권한 관리](#dashboard-authorization)
    - [무시할 작업](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행하기](#running-horizon)
    - [Horizon 배포하기](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [지표](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 삭제](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> Laravel Horizon에 대해 자세히 살펴보기 전에 Laravel의 기본 [큐 서비스](/docs/9.x/queues)를 먼저 익히는 것이 좋습니다. Horizon은 Laravel의 큐 기능을 확장하지만, 기본 큐 기능에 익숙하지 않으면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel에서 사용하는 [Redis 큐](/docs/9.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 실패한 작업 수 등 큐 시스템의 핵심 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용할 때는 모든 큐 워커 설정이 하나의 간단한 설정 파일에 저장됩니다. 애플리케이션 워커 구성을 버전 관리가 적용된 파일에 정의함으로써, 애플리케이션 배포 시 큐 워커를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Laravel Horizon은 큐 동력으로 [Redis](https://redis.io)를 반드시 사용해야 합니다. 따라서 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 설정되어 있는지 반드시 확인하세요.

Composer 패키지 관리자를 사용해 프로젝트에 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

Horizon을 설치한 후에는 `horizon:install` Artisan 명령어를 사용해 자산을 공개하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정 (Configuration)

Horizon 자산을 공개한 후, 주요 설정 파일은 `config/horizon.php`에 위치합니다. 이 설정 파일은 애플리케이션의 큐 워커 옵션을 구성할 수 있도록 해 줍니다. 각 설정 옵션에는 사용 목적에 대한 설명이 포함되어 있으니 꼼꼼히 살펴보세요.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php`의 `use` 옵션에서 다른 Redis 연결 이름으로 지정하지 않도록 주의하세요.

<a name="environments"></a>
#### 환경 (Environments)

설치 후 가장 먼저 익혀야 하는 Horizon 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 실행되는 환경 배열이며, 각 환경별 워커 프로세스 옵션을 정의합니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만 필요에 따라 환경을 추가할 수 있습니다:

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

Horizon을 시작하면 현재 애플리케이션 실행 환경에 맞는 워커 프로세스 구성 옵션을 사용합니다. 보통 환경은 `APP_ENV` [환경 변수](/docs/9.x/configuration#determining-the-current-environment) 값으로 판별합니다. 예를 들어, 기본 `local` 환경은 세 개의 워커 프로세스를 시작하고 각 큐에 할당된 워커 프로세스 수를 자동으로 조정하도록 설정되어 있습니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 시작하고 자동 균형 조정을 수행하도록 설정되어 있습니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments` 항목에 Horizon을 실행할 모든 [환경](/docs/9.x/configuration#environment-configuration)을 반드시 포함해야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저 (Supervisors)

Horizon 기본 설정 파일에서 볼 수 있듯, 각 환경은 하나 이상의 "슈퍼바이저"를 포함할 수 있습니다. 기본적으로 `supervisor-1`로 명명되어 있지만 원하는 이름으로 자유롭게 변경할 수 있습니다. 각 슈퍼바이저는 워커 프로세스 그룹을 "감독(supervise)"하고 큐별 워커 프로세스의 부하 분산을 담당합니다.

특정 환경에서 새 작업 그룹을 정의하려면 해당 환경에 추가 슈퍼바이저를 등록할 수 있습니다. 이를 통해 애플리케이션이 사용하는 특정 큐에 대해 다른 부하 분산 전략이나 워커 프로세스 수를 정의할 수 있습니다.

<a name="default-values"></a>
#### 기본 값 (Default Values)

Horizon 기본 설정 파일에 `defaults` 옵션이 있습니다. 이 옵션은 애플리케이션의 [슈퍼바이저](#supervisors)에 대한 기본값을 지정합니다. 각 환경의 슈퍼바이저 구성에 기본값이 병합되어 중복 설정을 줄여 줍니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략 (Balancing Strategies)

Laravel 기본 큐 시스템과 달리, Horizon은 `simple`, `auto`, `false` 세 가지 워커 부하 분산 전략을 지원합니다. 기본값인 `simple` 전략은 들어오는 작업을 워커 프로세스들 사이에 균등하게 나눕니다:

```
'balance' => 'simple',
```

`auto` 전략은 큐에 쌓인 현재 작업량에 따라 큐별 워커 프로세스 수를 자동으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 작업이 대기 중이고 `render` 큐가 비어 있으면, Horizon은 `notifications` 큐에 더 많은 워커를 할당하여 큐가 비워질 때까지 작업을 처리합니다.

`auto` 전략 사용 시에는 `minProcesses`와 `maxProcesses` 옵션을 정의해 Horizon이 조정할 워커 프로세스 수의 최소/최대 한계를 지정할 수 있습니다:

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

`balanceMaxShift`와 `balanceCooldown` 설정은 Horizon이 워커 수요에 맞춰 얼마나 빠르게 확장/축소할지 결정합니다. 위 예시에서는 최대 1개의 프로세스를 3초마다 생성하거나 종료할 수 있습니다. 필요에 따라 애플리케이션 상황에 맞게 조정하세요.

`balance` 옵션을 `false`로 설정하면 Laravel 기본 동작이 적용되어, 큐에 설정된 순서대로 작업이 처리됩니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 관리 (Dashboard Authorization)

Horizon은 `/horizon` URI에서 대시보드를 노출합니다. 기본적으로는 `local` 환경에서만 접근이 가능합니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일에 정의된 [권한 게이트](/docs/9.x/authorization#gates)를 통해 **로컬이 아닌 환경에서** Horizon 접근 권한을 관리합니다. 필요에 따라 이 권한 게이트를 수정해 Horizon 접근을 제한할 수 있습니다:

```
/**
 * Register the Horizon gate.
 *
 * 이 게이트는 로컬이 아닌 환경에서 누가 Horizon에 접근할 수 있는지를 결정합니다.
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
#### 대체 인증 전략

Laravel은 권한 게이트 클로저에 자동으로 인증된 사용자를 주입합니다. 만약 IP 제한과 같은 다른 방식으로 Horizon 보안을 제공하고 인증 과정을 생략하려면, 위 클로저의 시그니처를 `function ($user = null)`로 바꿔 Laravel이 인증을 요구하지 않도록 해야 합니다.

<a name="silenced-jobs"></a>
### 무시할 작업 (Silenced Jobs)

때로는 애플리케이션이나 서드파티 패키지에서 발생시키는 특정 작업을 대시보드에서 보고 싶지 않을 수 있습니다. 이런 작업은 "완료 작업(Completed Jobs)" 목록에서 공간을 차지하므로 무시할 수 있습니다. 시작하려면 `horizon` 설정 파일의 `silenced` 옵션에 해당 작업 클래스명을 추가하세요:

```
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는 무시할 작업 클래스가 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 할 수도 있습니다. 이 인터페이스를 구현한 작업은 `silenced` 배열에 명시되지 않아도 자동으로 무시 처리됩니다:

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

Horizon의 새로운 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 읽어 보세요. 또한, 모든 Horizon 버전 업그레이드 후에는 자산을 재게시해야 합니다:

```shell
php artisan horizon:publish
```

자산을 최신 상태로 유지하고 향후 업데이트에서 문제를 예방하려면, 애플리케이션의 `composer.json` 파일 `post-update-cmd` 스크립트에 다음 명령어를 추가할 수 있습니다:

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
## Horizon 실행하기 (Running Horizon)

`config/horizon.php` 설정 파일에서 슈퍼바이저와 워커 구성을 마친 후, `horizon` Artisan 명령어를 사용해 Horizon을 시작할 수 있습니다. 이 명령어는 현재 환경에 맞는 모든 워커 프로세스를 실행합니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지하거나 다시 시작하고 싶으면, 각각 `horizon:pause`와 `horizon:continue` 명령어를 사용하세요:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)를 일시 중지하거나 재개하려면 `horizon:pause-supervisor`와 `horizon:continue-supervisor` 명령어를 사용합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스 상태는 `horizon:status` 명령어로 확인할 수 있습니다:

```shell
php artisan horizon:status
```

Horizon 프로세스를 정상 종료하려면 `horizon:terminate` 명령어를 사용하세요. 실행 중인 작업은 완료 후 프로세스가 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포하기 (Deploying Horizon)

실제 서버에 Horizon을 배포할 준비가 되면, `php artisan horizon` 명령어를 모니터링하고 비정상 종료 시 재시작할 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설치 방법을 다룹니다.

애플리케이션 배포 중에는 Horizon 프로세스에 종료 신호를 보내 변경 사항이 반영된 후 프로세스 모니터가 재시작하도록 하는 것이 좋습니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치하기

Supervisor는 Linux 운영체제용 프로세스 모니터로, `horizon` 프로세스가 중단되면 자동으로 재시작합니다. Ubuntu에서는 다음 명령어로 Supervisor를 설치할 수 있습니다. 다른 OS를 사용하는 경우 운영체제의 패키지 관리자를 통해 설치하세요:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 어렵게 느껴진다면, [Laravel Forge](https://forge.laravel.com)를 사용해 보세요. Laravel Forge가 Laravel 프로젝트용 Supervisor를 자동으로 설치하고 구성해 줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 서버의 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 곳에 여러 설정 파일을 만들어 Supervisor가 프로세스를 감시하도록 지시할 수 있습니다. 예를 들어 다음과 같은 `horizon.conf` 파일을 생성할 수 있습니다:

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

설정 시 `stopwaitsecs` 값은 가장 오래 실행되는 작업이 소모하는 시간보다 커야 합니다. 그렇지 않으면 Supervisor가 작업 완료 전에 프로세스를 강제 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버용이며, Supervisor 설정 파일의 위치나 확장자는 다른 운영체제마다 다를 수 있습니다. 서버 문서를 반드시 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 작성한 후 다음 명령어로 Supervisor 설정을 갱신하고 모니터링 중인 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 사용법에 대해 더 알고 싶으면 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 메일 가능 객체(mailables), 방송 이벤트(broadcast events), 알림, 큐 이벤트 리스너 등 다양한 작업에 “태그”를 할당할 수 있습니다. 실제로 Horizon은 작업에 첨부된 Eloquent 모델을 분석해 대부분 작업에 지능적으로 자동 태그를 생성합니다. 예를 들어 다음 작업을 보세요:

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

만약 `App\Models\Video` 인스턴스가 `id` 속성이 1인 객체와 함께 이 작업이 큐에 쌓이면, 자동으로 `App\Models\Video:1` 태그가 붙습니다. 이는 Horizon이 작업의 속성(property)에서 Eloquent 모델을 검색하고 모델의 클래스명 및 기본키를 사용해 지능적으로 태그를 생성하기 때문입니다:

```
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 수동 태그 지정

큐에 넣는 객체에 대해 직접 태그를 정의하고 싶다면 클래스에 `tags` 메서드를 작성하면 됩니다:

```
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 할당할 태그들을 반환합니다.
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

> [!WARNING]
> Horizon에서 Slack 또는 SMS 알림을 설정할 때는 해당 알림 채널의 [사전 조건](/docs/9.x/notifications)을 반드시 확인하세요.

큐 대기 시간이 너무 길 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션 `App\Providers\HorizonServiceProvider`의 `boot` 메서드 내에서 호출할 수 있습니다:

```
/**
 * 애플리케이션 서비스 부트스트랩.
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
#### 알림 대기 시간 임계값 설정

애플리케이션의 `config/horizon.php` 설정 파일에서 "긴 대기 시간"임을 판단할 임계값(초)을 설정할 수 있습니다. `waits` 설정 옵션은 각 큐 연결 조합별 긴 대기 임계값을 제어합니다:

```
'waits' => [
    'redis:default' => 60,
    'redis:critical,high' => 90,
],
```

<a name="metrics"></a>
## 지표 (Metrics)

Horizon은 작업 및 큐 대기 시간과 처리량에 관한 정보를 제공하는 지표 대시보드를 포함합니다. 이 대시보드 데이터를 수집하려면, Horizon의 `snapshot` Artisan 명령어를 애플리케이션의 [스케줄러](/docs/9.x/scheduling)를 통해 5분마다 실행하도록 설정하세요:

```
/**
 * 애플리케이션 명령어 스케줄 정의.
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

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용하세요. 이 명령어는 실패 작업의 ID 또는 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제 (Clearing Jobs From Queues)

애플리케이션의 기본 큐에서 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐에서 작업만 삭제하려면 `queue` 옵션을 함께 지정할 수 있습니다:

```shell
php artisan horizon:clear --queue=emails
```