# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
    - [로드 밸런싱 전략](#balancing-strategies)
    - [대시보드 권한 제어](#dashboard-authorization)
    - [무음 처리된 작업](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> Laravel Horizon을 시작하기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)에 익숙해지는 것이 좋습니다. Horizon은 Laravel의 큐에 다양한 기능을 추가하기 때문에, 기본 큐 기능을 이해하지 못한 상태에서는 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/{{version}}/queues)를 위한 아름다운 대시보드와 코드 기반 구성 기능을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패와 같은 주요 메트릭을 손쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 구성이 단일 구성 파일에 저장됩니다. 버전 관리되는 파일에 워커 구성을 정의하면, 애플리케이션 배포 시 큐 워커를 손쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## 설치

> [!WARNING]  
> Laravel Horizon은 [Redis](https://redis.io) 기반 큐만 지원합니다. 따라서 `config/queue.php` 구성 파일에서 큐 연결이 반드시 `redis`로 설정되어 있어야 합니다.

Composer 패키지 관리자를 사용하여 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어로 Horizon의 에셋을 퍼블리시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 구성

에셋을 퍼블리시하면 기본 구성 파일이 `config/horizon.php`에 생성됩니다. 이 파일에서 애플리케이션의 큐 워커 옵션을 설정할 수 있습니다. 각 구성 옵션에는 설명이 있으니, 이 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]  
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결명은 예약되어 있으므로 `database.php`의 다른 Redis 연결이나 `horizon.php`의 `use` 옵션에 할당해서는 안 됩니다.

<a name="environments"></a>
#### 환경별 설정

설치 후 가장 먼저 익숙해져야 할 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 실행되는 여러 환경에 대한 배열이며, 각 환경별 워커 프로세스 옵션을 정의합니다. 기본 값으로는 `production`과 `local` 환경이 포함되어 있지만, 필요에 따라 환경을 추가할 수 있습니다:

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

와일드카드(`*`) 환경을 정의할 수도 있습니다. 해당 환경이 없으면 이 설정이 사용됩니다:

    'environments' => [
        // ...

        '*' => [
            'supervisor-1' => [
                'maxProcesses' => 3,
            ],
        ],
    ],

Horizon을 시작하면 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 옵션이 적용됩니다. 보통 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment)의 값으로 결정됩니다. 예를 들어, 기본 `local` 환경에서는 3개의 워커 프로세스가 생성되고 각 큐에 자동으로 워커가 분배됩니다. `production`에서는 최대 10개의 워커 프로세스가 자동 조절됩니다.

> [!WARNING]  
> `horizon` 구성 파일의 `environments` 부분에 Horizon을 실행할 [모든 환경](/docs/{{version}}/configuration#environment-configuration)에 대한 설정 항목이 있는지 반드시 확인하세요.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisors)

기본 구성 파일에서 볼 수 있듯, 각 환경에는 한 개 이상 "슈퍼바이저"를 둘 수 있습니다. `supervisor-1`라는 이름이 기본으로 제공되지만, 원하는 대로 이름을 지정할 수 있습니다. 각 슈퍼바이저는 워커 프로세스 그룹을 "감독"하며 큐 전체에 워커 분배를 담당합니다.

새로운 워커 그룹이 필요하다면 해당 환경에 추가 슈퍼바이저를 정의할 수 있습니다. 예를 들어, 특정 큐에 대해 별도의 워커 개수나 밸런싱 전략을 원하는 경우 사용할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)일 때는 슈퍼바이저의 `force` 옵션이 `true`로 설정되어 있지 않으면 Horizon이 큐 작업을 처리하지 않습니다:

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

Horizon의 기본 구성 파일에는 `defaults` 옵션이 있습니다. 이는 애플리케이션의 [슈퍼바이저](#supervisors)에 대한 기본 값을 지정합니다. 각 환경에 슈퍼바이저를 정의할 때 이 기본값이 병합되어 불필요한 중복을 줄여줍니다.

<a name="balancing-strategies"></a>
### 로드 밸런싱 전략

Laravel의 기본 큐 시스템과 달리, Horizon은 세 가지 워커 로드 밸런싱 전략인 `simple`, `auto`, `false` 중 선택할 수 있습니다. `simple` 전략은 들어오는 작업을 워커 간에 균등하게 분배합니다:

    'balance' => 'simple',

구성 파일의 기본값인 `auto` 전략은 큐의 현재 작업량에 따라 큐별 워커 프로세스 수를 자동으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고 `render` 큐가 비어있으면 Horizon은 워커를 `notifications` 큐에 더 많이 할당합니다.

`auto` 전략을 사용할 때는 큐별 최소 프로세스 개수(`minProcesses`)와 전체 워커 최대 개수(`maxProcesses`)도 설정할 수 있습니다:

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

`autoScalingStrategy` 옵션은 Horizon이 워커를 큐에 할당할 때, 대기 작업을 모두 처리하는데 걸리는 총 시간 기준(`time`) 또는 큐의 전체 작업 개수 기준(`size`) 중 어떤 기준을 적용할지 결정합니다.

`balanceMaxShift`와 `balanceCooldown` 옵션은 워커 수가 얼마나 빠르게 조정될지를 결정합니다. 예시에서는 3초마다 최대 1개 프로세스가 추가 또는 감소합니다. 애플리케이션에 맞게 조정하세요.

`balance` 옵션을 `false`로 설정하면 기본 Laravel 동작이 적용되어, 구성에 나열된 순서대로 큐가 처리됩니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 제어

Horizon 대시보드는 `/horizon` 경로로 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용됩니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일에는 [권한 게이트](/docs/{{version}}/authorization#gates)가 정의되어 있습니다. 이 게이트는 **로컬이 아닌** 환경에서 Horizon 접근을 통제합니다. 필요에 따라 이 게이트를 수정하여 접근을 제한할 수 있습니다:

    /**
     * Horizon 게이트 등록.
     *
     * 이 게이트는 로컬 환경이 아닌 곳에서 Horizon 접근을 결정합니다.
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

Laravel은 게이트 클로저 내부에 인증된 사용자를 자동으로 주입합니다. 만약 IP 제약 등 다른 방식으로 Horizon 보안을 제공한다면, Horizon 사용자가 "로그인"하지 않아도 됩니다. 이 경우에는 위의 `function (User $user)` 시그니처를 `function (User $user = null)`로 변경하여 인증이 필요하지 않게 할 수 있습니다.

<a name="silenced-jobs"></a>
### 무음 처리된 작업(Silenced Jobs)

때로는 애플리케이션이나 서드 파티 패키지에서 발생하는 특정 작업을 대시보드에 표시하지 않고 싶을 수 있습니다. 이런 작업을 "무음 처리"하면 "완료된 작업" 목록에서 공간을 차지하지 않습니다. 먼저, 무음 처리할 작업의 클래스명을 `horizon` 구성 파일의 `silenced` 옵션 배열에 추가하세요:

    'silenced' => [
        App\Jobs\ProcessPodcast::class,
    ],

또는, 무음 처리하려는 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하게 할 수도 있습니다. 이 인터페이스를 구현한 작업은 `silenced` 배열에 명시하지 않아도 자동으로 무음 처리됩니다:

    use Laravel\Horizon\Contracts\Silenced;

    class ProcessPodcast implements ShouldQueue, Silenced
    {
        use Queueable;

        // ...
    }

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 새로운 주요 버전으로 업그레이드할 경우, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 읽어보시기 바랍니다.

<a name="running-horizon"></a>
## Horizon 실행

`config/horizon.php`에서 슈퍼바이저 및 워커를 구성하면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 한 번의 명령으로 현재 환경에 맞는 모든 워커 프로세스가 시작됩니다:

```shell
php artisan horizon
```

`horizon:pause` 및 `horizon:continue` 명령어로 Horizon을 일시 중지했다가 다시 실행하도록 지시할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)만을 별도로 일시 중지하거나 이어서 실행하려면 `horizon:pause-supervisor` 및 `horizon:continue-supervisor` 명령어를 사용하세요:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

`horizon:status` 명령어로 Horizon 프로세스의 현재 상태를 확인할 수 있습니다:

```shell
php artisan horizon:status
```

특정 Horizon [슈퍼바이저](#supervisors)의 상태를 확인하려면 `horizon:supervisor-status` 명령어를 사용하세요:

```shell
php artisan horizon:supervisor-status supervisor-1
```

`horizon:terminate` 명령어로 Horizon 프로세스를 정상적으로 종료할 수 있습니다. 현재 처리 중인 작업을 완료한 후 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

Horizon을 실제 배포 서버에 올릴 준비가 되면, `php artisan horizon` 명령어가 비정상 종료되었을 때 자동으로 재시작할 수 있도록 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설정 방법을 안내하겠습니다.

배포 과정 중에는 Horizon 프로세스가 재시작되어 코드 변경 사항을 반영할 수 있도록 명령을 내리세요:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터입니다. `horizon` 프로세스가 중단되었을 때 자동으로 재시작해줍니다. Ubuntu에서 설치하려면 아래 명령을 사용하세요. Ubuntu가 아니라면 운영체제의 패키지 관리자를 사용하시기 바랍니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> Supervisor 직접 구성에 부담이 된다면, [Laravel Forge](https://forge.laravel.com)를 사용해보세요. 자동으로 Supervisor를 설치하고 설정해줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 서버의 `/etc/supervisor/conf.d` 디렉터리에 위치합니다. 여기서 원하는 만큼 설정 파일을 만들어 모니터링할 프로세스를 지정할 수 있습니다. 예시로, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작 및 감시할 수 있습니다:

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

Supervisor 설정 시, `stopwaitsecs` 값을 가장 오래 걸리는 작업 소요 시간보다 크게 설정해야 합니다. 그렇지 않으면 Supervisor가 작업 완료 전에 프로세스를 강제 종료할 수 있습니다.

> [!WARNING]  
> 위 예시는 Ubuntu 기반 서버에 적합하지만, 다른 운영체제에서는 Supervisor 설정 파일의 위치나 확장자가 다를 수 있습니다. 서버별 공식 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 작성한 후, 아래 명령으로 Supervisor 구성을 갱신하고 모니터링을 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]  
> Supervisor 사용에 대한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 작업, 메일 발송 객체, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등에 "태그"를 지정할 수 있습니다. 실제로, Horizon은 Eloquent 모델이 작업에 첨부되어 있으면 대부분의 작업을 자동으로 지능적으로 태그합니다. 예를 들어 다음 작업을 살펴보겠습니다:

    <?php

    namespace App\Jobs;

    use App\Models\Video;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Foundation\Queue\Queueable;

    class RenderVideo implements ShouldQueue
    {
        use Queueable;

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

이 작업이 `id`가 1인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면 자동으로 `App\Models\Video:1`이라는 태그를 부여받습니다. 이는 Horizon이 작업 내 프로퍼티에서 Eloquent 모델을 찾아, 모델의 클래스명과 기본 키를 조합해 태그를 생성하기 때문입니다:

    use App\Jobs\RenderVideo;
    use App\Models\Video;

    $video = Video::find(1);

    RenderVideo::dispatch($video);

<a name="manually-tagging-jobs"></a>
#### 작업에 태그 수동 지정

큐잉 객체에 대해 태그를 직접 정의하고 싶다면 클래스에 `tags` 메서드를 구현하면 됩니다:

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

큐에 등록된 이벤트 리스너의 태그를 가져올 때 Horizon은 이벤트 인스턴스를 `tags` 메서드에 전달합니다. 이를 이용해 이벤트 데이터를 태그에 포함할 수 있습니다:

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
> Horizon에서 Slack 또는 SMS 알림을 설정할 때는 [해당 알림 채널의 선행 조건](/docs/{{version}}/notifications)을 반드시 확인하세요.

특정 큐의 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출할 수 있습니다:

    /**
     * 애플리케이션 서비스를 부팅합니다.
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

대기 시간이 "길다"고 간주되는 기준은 `config/horizon.php` 파일에서 설정할 수 있습니다. `waits` 옵션에서 각 연결/큐 조합별로 임계값(초)을 지정합니다. 지정되지 않은 조합은 기본값인 60초가 사용됩니다:

    'waits' => [
        'redis:critical' => 30,
        'redis:default' => 60,
        'redis:batch' => 120,
    ],

<a name="metrics"></a>
## 메트릭

Horizon에는 큐와 작업의 대기 시간, 처리량에 대한 정보를 제공하는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드에 데이터를 채우려면, `routes/console.php`에서 Horizon의 `snapshot` Artisan 명령어가 5분마다 실행되도록 설정해야 합니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('horizon:snapshot')->everyFiveMinutes();

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용할 수 있습니다. 인수로는 실패한 작업의 ID 혹은 UUID만 입력하면 됩니다:

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 삭제하려면 `--all` 옵션을 사용하세요:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 있는 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용하면 됩니다:

```shell
php artisan horizon:clear
```

특정 큐에 있는 작업만 삭제하려면 `queue` 옵션을 전달하세요:

```shell
php artisan horizon:clear --queue=emails
```
