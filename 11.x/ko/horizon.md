# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [밸런싱 전략](#balancing-strategies)
    - [대시보드 권한 설정](#dashboard-authorization)
    - [무음 처리된 작업](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행하기](#running-horizon)
    - [Horizon 배포하기](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐의 작업 삭제](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]  
> Laravel Horizon을 자세히 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/11.x/queues)에 익숙해져야 합니다. Horizon은 Laravel 큐에 추가 기능을 더하는 도구로서, Laravel의 기본 큐 기능에 익숙하지 않으면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel에서 사용하는 [Redis 큐](/docs/11.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정 기능을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 실패 작업과 같은 큐 시스템의 주요 메트릭을 손쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 설정을 단일 간단한 구성 파일에 저장합니다. 애플리케이션의 워커 설정을 버전 관리 파일로 정의함으로써, 배포 시 애플리케이션의 큐 워커를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> Laravel Horizon은 큐 처리에 [Redis](https://redis.io)를 사용해야 하므로, `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 설정되어 있는지 확인해야 합니다.

Composer 패키지 관리자를 사용해 프로젝트에 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치가 완료되면 `horizon:install` Artisan 명령어로 Horizon의 자산을 게시합니다:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정 (Configuration)

Horizon 자산을 게시하면 주요 설정 파일은 `config/horizon.php`에 위치하게 됩니다. 이 설정 파일에서 애플리케이션의 큐 워커 옵션을 구성할 수 있으며, 각 설정 옵션에는 그 목적에 대한 설명이 포함되어 있으니 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]  
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php` 설정 파일의 `use` 옵션 값으로 다른 Redis 연결에 할당하면 안 됩니다.

<a name="environments"></a>
#### 환경 설정

설치 후에 가장 먼저 익숙해져야 할 Horizon 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 실행되는 다양한 환경을 배열 형식으로 정의하며, 각 환경별로 워커 프로세스 옵션을 지정합니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만, 필요에 따라 추가 환경을 정의할 수 있습니다:

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

또한 다른 환경이 일치하지 않을 때 사용할 와일드카드 환경(`*`)도 정의할 수 있습니다:

```
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

Horizon을 시작하면 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 설정을 사용합니다. 보통 환경은 `APP_ENV` [환경 변수](/docs/11.x/configuration#determining-the-current-environment) 값으로 결정됩니다. 기본적으로 `local` 환경은 세 개의 워커 프로세스를 실행하고 각 큐에 배분량을 자동으로 조절합니다. `production` 환경은 최대 10개의 워커 프로세스를 실행하며 자동 밸런싱 기능을 사용합니다.

> [!WARNING]  
> `horizon` 설정 파일의 `environments` 항목에 Horizon을 실행할 모든 [환경](/docs/11.x/configuration#environment-configuration)이 포함되어 있는지 반드시 확인하세요.

<a name="supervisors"></a>
#### 슈퍼바이저 (Supervisors)

Horizon 기본 설정 파일에서 알 수 있듯, 각 환경은 하나 이상의 "슈퍼바이저"를 가질 수 있습니다. 기본적으로는 `supervisor-1`로 명명되어 있지만, 원하는 이름을 자유롭게 사용할 수 있습니다. 슈퍼바이저는 워커 프로세스 그룹을 관리하며, 큐 별로 워커 프로세스의 균형을 맞추는 역할을 합니다.

필요하다면 같은 환경에 여러 슈퍼바이저를 추가해, 각기 다른 균형 조절 전략이나 워커 수를 지정할 수도 있습니다. 예를 들어, 특정 큐에 대해 다른 설정을 적용하고 싶을 때 유용합니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드 (Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/11.x/configuration#maintenance-mode)일 때는, Horizon이 큐 작업을 처리하지 않습니다. 단, Horizon 구성 파일에서 해당 슈퍼바이저에 대해 `force` 옵션을 `true`로 지정하면 유지보수 모드일 때도 작업이 실행됩니다:

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

Horizon 기본 설정 파일에는 `defaults` 옵션이 있습니다. 이 옵션은 애플리케이션의 [슈퍼바이저](#supervisors)에 대한 기본값을 지정합니다. 각 환경에 정의된 슈퍼바이저 설정과 병합되어 중복된 설정을 줄일 수 있습니다.

<a name="balancing-strategies"></a>
### 밸런싱 전략 (Balancing Strategies)

Laravel 기본 큐 시스템과 달리 Horizon은 세 가지 워커 밸런싱 전략을 제공합니다: `simple`, `auto`, `false`. `simple` 전략은 워커 프로세스들 사이에 작업을 고르게 분배합니다:

```
'balance' => 'simple',
```

기본값인 `auto` 전략은 큐의 현재 작업량에 따라 워커 프로세스 수를 자동으로 조절합니다. 예를 들어, `notifications` 큐에 1,000개의 작업이 대기 중이고 `render` 큐가 빈 상태라면, Horizon은 이 `notifications` 큐에 더 많은 워커를 할당해 작업이 비워질 때까지 처리합니다.

`auto` 전략을 사용할 때는 `minProcesses`와 `maxProcesses` 설정으로 각 큐별 최소 워커 수와 전체 워커 수 최대값을 조절할 수 있습니다:

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

`autoScalingStrategy` 값은 큐를 비우는 데 걸리는 총 시간(`time` 전략)이나 큐에 남은 작업 수(`size` 전략)를 기준으로 워커를 할당할지 결정합니다.

`balanceMaxShift`와 `balanceCooldown`은 Horizon이 얼마나 빠르게 워커 수를 조절할지 설정합니다. 위 예에서는 최대 한 개의 워커를 3초마다 생성하거나 제거할 수 있습니다. 이 값들은 애플리케이션 요구에 따라 적절히 조정하세요.

만약 `balance` 옵션을 `false`로 설정하면, Laravel 기본 방식처럼 설정한 큐 순서대로 작업이 처리됩니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Horizon 대시보드는 기본적으로 `/horizon` 경로를 통해 접근할 수 있습니다. 기본 설정에서는 `local` 환경에서만 접근이 허용됩니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일에서 [권한 게이트](/docs/11.x/authorization#gates)를 정의해 `local` 환경 외에서의 Horizon 접근을 제어할 수 있습니다. 필요에 맞게 이 게이트를 변경해 Horizon 접근을 제한하세요:

```
/**
 * Horizon 게이트 등록.
 *
 * 이 게이트는 non-local 환경에서 Horizon에 접근할 수 있는 사용자를 결정합니다.
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

Laravel은 게이트 클로저에 인증된 사용자를 자동 주입합니다. 만약 IP 제한 등 다른 방법으로 Horizon 보안을 적용할 경우 사용자 로그인이 필요하지 않을 수 있습니다. 이때는 위 게이트의 시그니처를 `function (User $user = null)`로 바꿔 Laravel이 인증을 요구하지 않도록 할 수 있습니다.

<a name="silenced-jobs"></a>
### 무음 처리된 작업 (Silenced Jobs)

애플리케이션이나 서드파티 패키지가 디스패치한 일부 작업이 '완료된 작업' 목록에 표시되는 것이 불필요하다고 생각되면, 해당 작업을 무음 처리할 수 있습니다. 시작하려면 무음 처리할 작업 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가하세요:

```
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는 무음 처리할 작업 자체에 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, `silenced` 목록에 포함되지 않아도 자동으로 무음 처리됩니다:

```
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="upgrading-horizon"></a>
## Horizon 업그레이드 (Upgrading Horizon)

Horizon의 주요 버전 업그레이드 시에는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토하세요.

<a name="running-horizon"></a>
## Horizon 실행하기 (Running Horizon)

애플리케이션의 `config/horizon.php`에서 슈퍼바이저와 워커 설정을 마쳤으면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령어 하나로 현재 환경에 설정된 모든 워커 프로세스가 실행됩니다:

```shell
php artisan horizon
```

`horizon:pause`와 `horizon:continue` 명령어로 Horizon 프로세스를 일시 중지하거나 다시 진행할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)를 대상으로 일시 중지 및 진행 명령도 가능합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스 상태는 `horizon:status` 명령어로 확인할 수 있습니다:

```shell
php artisan horizon:status
```

특정 슈퍼바이저 상태를 확인하려면 `horizon:supervisor-status` 명령어를 사용하세요:

```shell
php artisan horizon:supervisor-status supervisor-1
```

`horizon:terminate` 명령어로 Horizon 프로세스를 우아하게 종료할 수 있습니다. 현재 처리 중인 작업은 완료한 뒤 종료합니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포하기 (Deploying Horizon)

애플리케이션 서버에 Horizon을 배포할 때는, `php artisan horizon` 명령어를 모니터링할 프로세스 모니터를 설정해 비정상 종료 시 자동 재시작하도록 하세요. 아래에서 프로세스 모니터 설치 방법을 안내합니다.

배포 과정에서는 Horizon 프로세스에 `horizon:terminate` 명령어를 보내 종료하도록 지시하세요. 프로세스 모니터가 이를 감지해 Horizon을 재시작하고 새 코드를 반영합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치하기

Supervisor는 Linux용 프로세스 모니터로, `horizon` 프로세스가 멈추면 자동으로 재시작합니다. Ubuntu에서는 다음 명령어로 설치하세요. 다른 OS를 사용하는 경우 OS의 패키지 관리자를 통해 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> 직접 Supervisor 설정이 어렵다면, [Laravel Forge](https://forge.laravel.com)를 사용해 보세요. Forge가 Supervisor를 자동으로 설치하고 구성해 줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 대개 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이곳에 여러 설정 파일을 만들어 각 프로세스들을 모니터링할 수 있습니다. 예를 들어 `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작 및 감시하도록 설정할 수 있습니다:

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

설정 시 `stopwaitsecs` 값이 애플리케이션에서 가장 오래 실행되는 작업 시간보다 커야 합니다. 그렇지 않으면 가장 오래 실행되는 작업이 완료되기 전에 Supervisor가 프로세스를 강제 종료할 수 있습니다.

> [!WARNING]  
> 위 예시는 Ubuntu 기반 서버에 적합하며, 다른 서버 운영체제는 Supervisor 설정 파일 경로나 확장자가 다를 수 있습니다. 운영체제 문서를 참조하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일 생성 후 아래 명령어로 Supervisor 구성을 다시 읽고, 업데이트하며, Horizon 프로세스를 시작하세요:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]  
> Supervisor 사용법에 관한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 작업에 “태그”를 할당할 수 있으며, 여기에는 메일 발송 가능 객체(mailables), 브로드캐스트 이벤트, 알림, 큐 이벤트 리스너가 포함됩니다. 심지어 Eloquent 모델이 작업 속성에 연결된 경우 Horizon이 자동으로 대부분 작업에 태그를 지능적으로 부여합니다.

예를 들어 다음과 같은 작업이 있으면:

```
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

이 작업이 `id`가 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 들어가면, 자동으로 `App\Models\Video:1`이라는 태그가 붙습니다. 이는 Horizon이 작업의 속성들에서 Eloquent 모델을 찾아 모델 클래스명과 기본 키를 기반으로 태그를 부여하기 때문입니다:

```
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 수동으로 작업 태그 지정하기

큐에 넣는 객체에 대해 직접 태그를 지정하고 싶으면, 해당 클래스에 `tags` 메서드를 정의하세요:

```
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 할당할 태그를 반환합니다.
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
#### 수동으로 이벤트 리스너 태그 지정하기

큐 이벤트 리스너의 태그를 가져올 때 Horizon은 자동으로 이벤트 인스턴스를 `tags` 메서드에 전달합니다. 이를 통해 이벤트 데이터를 태그에 포함할 수 있습니다:

```
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
> Horizon의 Slack 또는 SMS 알림을 구성하기 전에 관련 알림 채널의 [필수 조건](/docs/11.x/notifications)을 반드시 확인하세요.

큐가 오래 대기할 경우 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 애플리케이션의 `App\Providers\HorizonServiceProvider`에 있는 `boot` 메서드에서 호출하세요:

```
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

애플리케이션의 `config/horizon.php` 설정 파일 내 `waits` 항목에서 ‘오래된 대기’ 기준 시간을 연결/큐 조합별로 설정할 수 있습니다. 설정하지 않은 조합은 기본값으로 60초가 설정됩니다:

```
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭 (Metrics)

Horizon에는 작업 및 큐 대기 시간, 처리량 정보를 제공하는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드를 채우기 위해 Horizon의 `snapshot` Artisan 명령어를 애플리케이션의 `routes/console.php` 파일에 다음과 같이 추가해 5분마다 실행되도록 구성하세요:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제 (Deleting Failed Jobs)

실패한 작업을 삭제하고 싶으면 `horizon:forget` 명령어를 사용하세요. 인수로 실패한 작업의 ID 또는 UUID를 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 삭제하려면 `--all` 옵션을 추가해 실행하세요:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐의 작업 삭제 (Clearing Jobs From Queues)

애플리케이션 기본 큐에 있는 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐에서 작업을 삭제하려면 `queue` 옵션에 큐 이름을 지정합니다:

```shell
php artisan horizon:clear --queue=emails
```