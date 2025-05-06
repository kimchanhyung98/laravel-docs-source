# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 권한](#dashboard-authorization)
    - [무시할 작업(Silenced Jobs)](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [지표](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> Laravel Horizon을 자세히 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)를 먼저 익혀야 합니다. Horizon은 Laravel의 큐에 추가 기능을 제공하며, 기본 큐 기능을 이해하지 못하면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis 큐](/docs/{{version}}/queues)에 대해 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 통해 작업 처리량, 실행 시간, 작업 실패 건수 등 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 설정이 하나의 간단한 설정 파일에 저장됩니다. 애플리케이션의 워커 설정을 버전 관리되는 파일로 정의함으로써, 애플리케이션을 배포할 때 큐 워커를 손쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## 설치

> [!WARNING]  
> Laravel Horizon을 사용하려면 큐 엔진으로 [Redis](https://redis.io)를 사용해야 합니다. 따라서 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 지정되어 있는지 확인해야 합니다.

Composer 패키지 매니저를 이용해 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어로 Horizon의 에셋을 게시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

Horizon의 에셋을 게시한 후, 기본 설정 파일은 `config/horizon.php`에 위치하게 됩니다. 이 파일에서 애플리케이션의 큐 워커 옵션을 설정할 수 있습니다. 각 옵션에는 목적에 대한 설명이 포함되어 있으니, 파일 전체를 꼼꼼히 확인하는 것이 좋습니다.

> [!WARNING]  
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결명은 예약되어 있으니, `database.php` 설정 파일이나 `horizon.php`의 `use` 옵션에 다른 Redis 연결로 지정하지 마세요.

<a name="environments"></a>
#### 환경(Environment)

설치 후에 가장 먼저 익혀야 할 설정 항목은 `environments` 옵션입니다. 이 옵션은 애플리케이션이 실행되는 환경의 배열이며, 각 환경별로 워커 프로세스 옵션을 정의합니다. 기본적으로, `production`과 `local` 환경이 포함되어 있지만 필요에 따라 환경을 추가할 수 있습니다:

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

Horizon을 시작하면, 현재 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 설정을 사용합니다. 환경은 일반적으로 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment)의 값을 기준으로 판단합니다. 예를 들어, 기본 `local` 환경은 워커 프로세스 3개를 시작하며, 각 큐에 할당된 워커 수를 자동으로 조절합니다. `production` 환경은 최대 10개의 워커 프로세스를 시작하도록 설정되어 있습니다.

> [!WARNING]  
> `horizon` 설정 파일의 `environments` 영역에 Horizon을 실행할 모든 [환경](/docs/{{version}}/configuration#environment-configuration)을 반드시 설정하세요.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisor)

Horizon의 기본 설정 파일에서 보듯, 각 환경은 하나 이상의 "슈퍼바이저"를 가질 수 있습니다. 기본적으로 이 슈퍼바이저의 이름은 `supervisor-1`이지만, 자유롭게 원하는 이름을 붙일 수 있습니다. 각각의 슈퍼바이저는 일종의 워커 그룹을 "감독"하며, 큐에 맞추어 워커 프로세스를 자동으로 분배 및 관리합니다.

특정 환경에 실행할 워커 그룹(슈퍼바이저)을 추가하고 싶다면 슈퍼바이저를 더 추가할 수도 있습니다. 특정 큐에 대해 다른 부하 분산 전략이나 워커 수를 지정해야 할 때 유용합니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드(Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)일 때, Horizon은 슈퍼바이저의 `force` 옵션이 `true`로 설정된 경우에만 큐 작업을 계속 처리합니다:

    'environments' => [
        'production' => [
            'supervisor-1' => [
                // ...
                'force' => true,
            ],
        ],
    ],

<a name="default-values"></a>
#### 기본값

Horizon의 기본 설정 파일에는 `defaults` 옵션이 있습니다. 이 옵션은 [슈퍼바이저](#supervisors)의 기본값을 지정합니다. 이 기본값들은 각 환경에 정의된 슈퍼바이저 설정에 병합되어, 중복을 피할 수 있습니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략

Laravel의 기본 큐 시스템과 달리, Horizon은 `simple`, `auto`, `false`의 세 가지 워커 부하 분산 전략을 제공합니다. `simple` 전략은 들어오는 작업을 모든 워커에게 균등하게 분배합니다:

    'balance' => 'simple',

기본값인 `auto` 전략은 각 큐의 현재 작업량에 따라 큐별 워커 수를 동적으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있다면 Horizon은 이 큐에 더 많은 워커를 할당해 빠르게 작업이 처리되도록 합니다.

`auto` 전략을 사용할 때는 `minProcesses` 및 `maxProcesses` 옵션으로 프로세스 수의 최소 및 최대값을 조절할 수 있습니다:

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

`autoScalingStrategy` 값은 Horizon이 큐의 작업 대기 시간을 기준으로(`time` 전략) 또는 작업 수(`size` 전략) 기준으로 워커 프로세스를 조절할지 결정합니다.

`balanceMaxShift`와 `balanceCooldown`은 Horizon이 워커 수를 얼마나 빠르게 조정할지를 결정합니다. 위 예시에서는 3초마다 최대 한 프로세스씩 추가 또는 삭제됩니다. 애플리케이션 상황에 맞게 이 값들을 조정하세요.

`balance` 옵션이 `false`로 설정되면, 큐들은 설정 파일에 명시된 순서대로 처리되며, Laravel의 기본 동작을 따릅니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한

Horizon 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 가능합니다. 하지만 `app/Providers/HorizonServiceProvider.php` 파일에 있는 [권한 게이트](/docs/{{version}}/authorization#gates) 정의를 수정하면 **local 환경이 아닌 경우** 접근 권한을 제어할 수 있습니다:

    /**
     * Horizon 게이트 등록
     *
     * 이 게이트는 local 환경이 아닌 경우 Horizon 접근 권한을 결정합니다.
     */
    protected function gate(): void
    {
        Gate::define('viewHorizon', function (User $user) {
            return in_array($user->email, [
                'taylor@laravel.com',
            ]);
        });
    }

<a name="alternative-authentication-strategies"></a>
#### 대체 인증 전략

Laravel은 게이트 클로저에 인증된 사용자를 자동으로 주입합니다. 만약 IP 제한 등 별도의 방식으로 Horizon에 접근 권한을 부여하고자 한다면, 사용자가 로그인하지 않아도 되므로, 위 게이트 함수 시그니처를 `function (User $user = null)`로 변경하여 인증을 강제하지 않도록 하세요.

<a name="silenced-jobs"></a>
### 무시할 작업(Silenced Jobs)

특정 작업(자체 또는 서드파티 패키지 작업)이 "완료된 작업" 목록에 나타나지 않게 하고 싶을 때, silenced 처리를 할 수 있습니다. 먼저 `horizon` 설정 파일의 `silenced` 옵션에 job 클래스명을 추가하세요:

    'silenced' => [
        App\Jobs\ProcessPodcast::class,
    ],

또는 해당 작업 클래스에 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하게 하면, 설정 배열에 추가하지 않아도 자동으로 무시됩니다:

    use Laravel\Horizon\Contracts\Silenced;

    class ProcessPodcast implements ShouldQueue, Silenced
    {
        use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

        // ...
    }

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 주요 버전을 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다. 또, 어떤 새로운 버전으로 업그레이드할 때든 Horizon의 에셋을 다시 게시하는 것이 좋습니다:

```shell
php artisan horizon:publish
```

항상 최신 에셋을 유지하고 앞으로의 업데이트 문제를 방지하려면, 애플리케이션의 `composer.json` 파일 `post-update-cmd` 스크립트에 아래와 같이 명령어를 추가하세요:

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
## Horizon 실행

애플리케이션의 `config/horizon.php` 파일에서 슈퍼바이저 및 워커를 설정한 후, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령어 하나로 현재 환경의 모든 워커 프로세스가 시작됩니다:

```shell
php artisan horizon
```

`horizon:pause`와 `horizon:continue` Artisan 명령어로 Horizon 프로세스를 일시 중지하거나 다시 진행할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)만 일시 중지하거나 계속 실행하도록 하려면 아래 명령어를 사용하세요:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스의 상태는 `horizon:status`로 확인할 수 있습니다:

```shell
php artisan horizon:status
```

`horizon:terminate` 명령어로 Horizon 프로세스를 정상적으로 종료할 수 있습니다. 이 경우 현재 처리 중인 작업이 모두 완료된 뒤 Horizon이 멈춥니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

실서버에 Horizon을 배포할 때는 `php artisan horizon` 명령이 비정상적으로 종료되어도 프로세스가 자동 재시작되도록 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설치 방법도 안내합니다.

배포 과정 중에는 코드 변경 사항이 적용되도록 Horizon 프로세스를 종료(`terminate`)하면, 프로세스 모니터가 자동으로 재시작합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스의 프로세스 감시 도구이며, `horizon` 프로세스가 종료될 경우 자동 재시작합니다. Ubuntu에서 아래 명령어로 Supervisor를 설치할 수 있습니다(다른 배포판은 운영체제 패키지 관리자를 참고):

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> Supervisor 직접 설정이 부담스럽다면, [Laravel Forge](https://forge.laravel.com)를 이용하여 자동 설치 및 설정할 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d`에 저장합니다. 이 디렉터리에 사용자의 프로세스를 감시할 설정 파일을 여러 개 만들어 둘 수 있습니다. 예를 들어 `horizon.conf` 파일을 생성해 Horizon 프로세스를 관리할 수 있습니다:

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

Supervisor 설정 시 `stopwaitsecs` 값이, 가장 오래 걸리는 작업의 실행 시간(초)보다 크게 설정되어야 합니다. 그렇지 않으면 Supervisor가 완료 전에 작업을 강제 종료할 수 있습니다.

> [!WARNING]  
> 위 예시는 Ubuntu 서버 기준이며, 운영체제에 따라 설정 파일 경로와 확장자가 다를 수 있습니다. 자세한 내용은 서버 운영체제 설명서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 실행

설정 파일을 만든 후, 다음 명령어로 Supervisor를 재구성하고 감시 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]  
> Supervisor 사용법에 대한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 메일러블, 브로드캐스트 이벤트, 알림, 큐 이벤트 리스너 등 다양한 작업에 "태그"를 지정할 수 있도록 지원합니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델을 바탕으로 대부분의 작업에 태그를 자동으로 부여합니다. 예시로 다음과 같은 작업이 있다고 합시다:

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
         * 새로운 작업 인스턴스 생성
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

`id`가 1인 `App\Models\Video` 인스턴스가 큐에 들어오면, 자동으로 `App\Models\Video:1` 태그가 생성됩니다. 이는 Horizon이 작업 내 속성에서 Eloquent 모델을 찾아 해당 클래스명과 기본키(primary key)로 태그를 붙이기 때문입니다.

    use App\Jobs\RenderVideo;
    use App\Models\Video;

    $video = Video::find(1);

    RenderVideo::dispatch($video);

<a name="manually-tagging-jobs"></a>
#### 작업 태그 수동 지정

큐 작업 클래스에 `tags` 메서드를 추가하면 직접 태그를 지정할 수 있습니다:

    class RenderVideo implements ShouldQueue
    {
        /**
         * 작업에 지정할 태그 반환
         *
         * @return array<int, string>
         */
        public function tags(): array
        {
            return ['render', 'video:'.$this->video->id];
        }
    }

<a name="manually-tagging-event-listeners"></a>
#### 이벤트 리스너에 태그 수동 지정

큐 이벤트 리스너의 경우, Horizon이 `tags` 메서드에 이벤트 인스턴스를 자동으로 넘겨주므로, 이벤트 데이터를 활용한 태그 지정이 가능합니다:

    class SendRenderNotifications implements ShouldQueue
    {
        /**
         * 리스너에 지정할 태그 반환
         *
         * @return array<int, string>
         */
        public function tags(VideoRendered $event): array
        {
            return ['video:'.$event->video->id];
        }
    }

<a name="notifications"></a>
## 알림

> [!WARNING]  
> Horizon에서 Slack 또는 SMS 알림을 구성하려면, [해당 알림 채널의 사전 조건](/docs/{{version}}/notifications)을 먼저 확인하세요.

큐의 대기시간이 길어지면 알림을 받도록 할 수도 있습니다. `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용하면 됩니다. 이는 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하세요:

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

<a name="configuring-notification-wait-time-thresholds"></a>
#### 알림 대기 시간 임계값 설정

얼마나 오랫동안 대기했을 때 "대기 시간이 김"으로 간주할지 `config/horizon.php` 파일에서 지정할 수 있습니다. `waits` 옵션에 연결/큐 별 임계값을 설정하세요. 지정하지 않은 큐는 기본값 60초를 사용합니다:

    'waits' => [
        'redis:critical' => 30,
        'redis:default' => 60,
        'redis:batch' => 120,
    ],

<a name="metrics"></a>
## 지표

Horizon은 작업 및 큐의 대기 시간, 처리량 등 다양한 정보를 제공하는 지표 대시보드를 제공합니다. 이 대시보드에 데이터가 채워지도록, Horizon의 `snapshot` Artisan 명령어를 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)를 이용해 5분마다 실행 설정해야 합니다:

    /**
     * 애플리케이션 커맨드 스케줄 정의
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->command('horizon:snapshot')->everyFiveMinutes();
    }

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용하세요. 실패한 작업의 ID나 UUID를 유일한 인자로 넘기면 됩니다:

```shell
php artisan horizon:forget 5
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 등록된 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐에서만 작업을 삭제하고 싶다면 `queue` 옵션을 추가하세요:

```shell
php artisan horizon:clear --queue=emails
```
