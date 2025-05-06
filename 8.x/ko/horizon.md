# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 권한 부여](#dashboard-authorization)
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

> {tip} Laravel Horizon을 자세히 알아보기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)에 익숙해지는 것이 좋습니다. Horizon은 Laravel의 큐를 확장하는 추가 기능을 제공하므로, 기본 큐 기능을 모르면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis 큐](/docs/{{version}}/queues)를 위한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon은 작업 처리량, 실행 시간, 작업 실패와 같은 큐 시스템의 주요 지표를 손쉽게 모니터링할 수 있게 해줍니다.

Horizon을 사용하면 모든 큐 워커 설정이 하나의 간단한 설정 파일에 저장됩니다. 버전 관리되는 파일에서 애플리케이션의 워커 구성을 정의함으로써, 애플리케이션 배포 시 손쉽게 큐 워커를 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## 설치

> {note} Laravel Horizon은 [Redis](https://redis.io)를 큐 엔진으로 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 파일에서 큐 연결이 `redis`로 설정되어 있는지 확인하세요.

Composer 패키지 관리자를 사용하여 Horizon을 프로젝트에 설치할 수 있습니다:

    composer require laravel/horizon

Horizon 설치 후, `horizon:install` Artisan 명령어로 에셋을 퍼블리시하세요:

    php artisan horizon:install

<a name="configuration"></a>
### 설정

Horizon의 에셋을 퍼블리시한 후, 기본 설정 파일은 `config/horizon.php`에 위치합니다. 이 설정 파일에서 애플리케이션의 큐 워커 옵션을 구성할 수 있습니다. 각 설정 옵션에는 목적이 설명되어 있으니, 파일을 꼼꼼히 살펴보세요.

> {note} Horizon은 내부적으로 `horizon`이라는 Redis 연결명을 사용합니다. 이 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php`의 `use` 옵션 등에서 다른 Redis 연결에 사용하면 안 됩니다.

<a name="environments"></a>
#### 환경별 설정

설치 후, 가장 먼저 익숙해져야 하는 Horizon 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 동작하는 환경별로 워커 프로세스 옵션을 정의하는 배열입니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만, 필요한 경우 자유롭게 환경을 추가할 수 있습니다.

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

Horizon을 시작하면, 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 설정 옵션을 사용합니다. 일반적으로 실행 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment) 값에 의해 결정됩니다. 예를 들어, 기본 `local` Horizon 환경은 워커 프로세스 세 개를 실행하고 큐별 워커 프로세스를 자동으로 분산합니다. 기본 `production` 환경은 워커 프로세스 최대 10개를 실행하며, 큐별 워커 프로세스를 자동으로 분산할 수 있도록 설정되어 있습니다.

> {note} Horizon을 실행할 모든 [환경](/docs/{{version}}/configuration#environment-configuration)에 대해 `horizon` 설정 파일의 `environments` 부분에 엔트리가 있는지 확인하세요.

<a name="supervisors"></a>
#### 슈퍼바이저

Horizon의 기본 설정 파일에서 볼 수 있듯이, 각 환경에는 하나 이상의 "supervisor(슈퍼바이저)"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 슈퍼바이저가 정의되어 있지만, 원하는 대로 이름을 지정할 수 있습니다. 각 슈퍼바이저는 워커 프로세스 그룹을 "감독"하며 큐 간 워커 프로세스 분산을 책임집니다.

필요에 따라 특정 환경에 추가 슈퍼바이저를 등록할 수 있습니다. 예를 들어, 애플리케이션에서 사용하는 특정 큐에 대해 다른 분산 전략이나 워커 프로세스 수를 지정하고자 할 때 사용할 수 있습니다.

<a name="default-values"></a>
#### 기본값

Horizon의 기본 설정 파일에는 `defaults`라는 설정 옵션이 있습니다. 이 옵션은 애플리케이션 [슈퍼바이저](#supervisors)의 기본값을 지정합니다. 슈퍼바이저의 기본값은 각 환경의 슈퍼바이저 설정에 병합되므로, 중복 설정을 피할 수 있습니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략

Laravel의 기본 큐 시스템과 달리, Horizon은 세 가지 워커 부하 분산 전략을 제공합니다: `simple`, `auto`, 그리고 `false`입니다. 기본값인 `simple` 전략은 들어오는 작업을 워커 프로세스 간에 고르게 분할합니다.

    'balance' => 'simple',

`auto` 전략은 큐의 현재 작업량에 따라 큐당 워커 프로세스 수를 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고 `render` 큐가 비어 있다면, Horizon은 모든 작업이 처리될 때까지 더 많은 워커를 `notifications` 큐에 할당합니다.

`auto` 전략을 사용할 때는 `minProcesses`와 `maxProcesses` 옵션으로 Horizon이 스케일업/다운 할 최소 및 최대 워커 프로세스 수를 지정할 수 있습니다.

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

`balanceMaxShift`와 `balanceCooldown` 값은 Horizon이 워커 수요에 맞춰 얼마나 빠르게 스케일 아웃/인 하는지 결정합니다. 위 예시에서는 3초마다 최대 1개의 프로세스가 생성되거나 제거됩니다. 애플리케이션 상황에 따라 이 값들을 조정할 수 있습니다.

`balance` 옵션이 `false`로 설정되면, 기본 Laravel 동작이 적용되어 설정 파일의 큐 순서대로 작업을 처리합니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 부여

Horizon은 `/horizon` URI에 대시보드를 노출합니다. 기본적으로, 이 대시보드는 `local` 환경에서만 접근할 수 있습니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일 내에 [권한 게이트](/docs/{{version}}/authorization#gates) 정의가 있습니다. 이 게이트는 **비로컬** 환경에서 Horizon 접근을 통제합니다. 필요에 따라 이 게이트를 수정하여 Horizon 접근을 제한할 수 있습니다.

    /**
     * Horizon 권한 게이트 등록
     *
     * 이 게이트는 비로컬 환경에서 누가 Horizon에 접근 가능한지 결정합니다.
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

<a name="alternative-authentication-strategies"></a>
#### 대체 인증 전략

Laravel은 게이트 클로저에 인증된 사용자를 자동 주입합니다. 만약 Horizon의 보안을 IP 제한 등 다른 방식으로 제공한다면, 사용자들이 "로그인"을 하지 않을 수도 있습니다. 이 경우 위의 `function ($user)` 시그니처를 `function ($user = null)`로 변경하여, Laravel이 인증을 요구하지 않도록 해야 합니다.

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 주요 버전을 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토하세요. 또, 새로운 Horizon 버전으로 업그레이드할 때마다 아래 명령어로 Horizon의 에셋을 다시 퍼블리시해야 합니다.

    php artisan horizon:publish

미래의 업데이트에서 문제가 발생하지 않도록 에셋을 최신 상태로 유지하려면, `composer.json` 파일의 `post-update-cmd` 스크립트에 `horizon:publish` 명령어를 추가할 수 있습니다.

    {
        "scripts": {
            "post-update-cmd": [
                "@php artisan horizon:publish --ansi"
            ]
        }
    }

<a name="running-horizon"></a>
## Horizon 실행

애플리케이션의 `config/horizon.php` 파일에서 슈퍼바이저와 워커를 구성한 후, `horizon` Artisan 명령어로 Horizon을 실행할 수 있습니다. 이 명령은 현재 환경의 모든 워커 프로세스를 시작합니다.

    php artisan horizon

`horizon:pause`와 `horizon:continue` Artisan 명령어로 Horizon 프로세스의 작업 처리를 일시 중지/재개 할 수 있습니다.

    php artisan horizon:pause

    php artisan horizon:continue

특정 Horizon [슈퍼바이저](#supervisors)를 대상으로 일시 중지/재개하려면 `horizon:pause-supervisor`와 `horizon:continue-supervisor` Artisan 명령어를 사용할 수 있습니다.

    php artisan horizon:pause-supervisor supervisor-1

    php artisan horizon:continue-supervisor supervisor-1

`horizon:status` 명령어로 현재 Horizon 프로세스의 상태를 확인할 수 있습니다.

    php artisan horizon:status

`horizon:terminate` 명령어로 Horizon 프로세스를 부드럽게 종료할 수 있습니다. 현재 처리 중인 작업이 완료된 뒤에 실행이 중단됩니다.

    php artisan horizon:terminate

<a name="deploying-horizon"></a>
### Horizon 배포

애플리케이션을 실제 서버에 배포할 준비가 되면, `php artisan horizon` 명령어를 모니터링하고 예기치 않게 종료될 경우 자동으로 재시작하는 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터를 설치하는 방법을 안내합니다.

배포 프로세스 중에는 Horizon 프로세스에 종료 명령을 내려, 프로세스 모니터가 이를 감지해 재시작하도록 하여 코드 변경 사항을 적용받을 수 있습니다.

    php artisan horizon:terminate

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제의 프로세스 관리 도구로, `horizon` 프로세스가 중단될 경우 자동으로 재시작해줍니다. Ubuntu에서는 다음 명령어로 Supervisor를 설치할 수 있습니다. 다른 OS를 사용하는 경우 해당 운영체제의 패키지 관리자를 통해 Supervisor를 설치할 수 있습니다.

    sudo apt-get install supervisor

> {tip} Supervisor 설정이 부담스럽다면 [Laravel Forge](https://forge.laravel.com) 서비스를 이용하세요. Forge는 Supervisor를 자동으로 설치·설정해줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉터리에 위치합니다. 이 디렉터리에 원하는 만큼 설정 파일을 생성해, supervisor가 어떻게 각 프로세스를 관리할지 지정할 수 있습니다. 예를 들어, `horizon` 프로세스를 시작하고 모니터링하는 `horizon.conf` 파일을 생성할 수 있습니다.

    [program:horizon]
    process_name=%(program_name)s
    command=php /home/forge/example.com/artisan horizon
    autostart=true
    autorestart=true
    user=forge
    redirect_stderr=true
    stdout_logfile=/home/forge/example.com/horizon.log
    stopwaitsecs=3600

> {note} `stopwaitsecs` 값은 가장 오래 실행되는 작업에 소요되는 시간보다 크게 지정해야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 프로세스를 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일 작성 후, 다음 명령어로 Supervisor 설정을 갱신하고, 모니터되는 프로세스를 시작할 수 있습니다.

    sudo supervisorctl reread

    sudo supervisorctl update

    sudo supervisorctl start horizon

> {tip} Supervisor 사용법에 대한 더 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 메일 발송, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 작업에 "태그"를 지정할 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델을 기반으로 거의 모든 작업을 지능적으로 자동 태그합니다. 예를 들어, 아래의 작업을 살펴보세요.

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

이 작업이 `id` 값이 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 자동으로 `App\Models\Video:1` 태그를 부여받게 됩니다. 이는 Horizon이 작업의 속성에서 Eloquent 모델을 찾아, 모델의 클래스명과 기본 키를 조합하여 태그를 지정하기 때문입니다.

    use App\Jobs\RenderVideo;
    use App\Models\Video;

    $video = Video::find(1);

    RenderVideo::dispatch($video);

<a name="manually-tagging-jobs"></a>
#### 작업에 직접 태그 지정하기

큐에 등록 가능한 객체에서 태그를 직접 지정하려면, 클래스에 `tags` 메서드를 정의하면 됩니다.

    class RenderVideo implements ShouldQueue
    {
        /**
         * 작업에 할당할 태그를 반환합니다.
         *
         * @return array
         */
        public function tags()
        {
            return ['render', 'video:'.$this->video->id];
        }
    }

<a name="notifications"></a>
## 알림

> {note} Horizon에서 Slack 또는 SMS 알림을 구성할 때는 [해당 알림 채널의 사전 요구 사항](/docs/{{version}}/notifications)을 확인하세요.

특정 큐의 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이들 메서드는 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출할 수 있습니다.

    /**
     * 애플리케이션 서비스 부트스트랩
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

<a name="configuring-notification-wait-time-thresholds"></a>
#### 알림 대기 시간 임계값 설정

얼마나 대기해야 "대기 시간이 길다"고 판단할지 애플리케이션의 `config/horizon.php` 파일의 `waits` 옵션에서 설정할 수 있습니다. 이 옵션을 사용해 연결/큐 조합별 임계값을 지정할 수 있습니다.

    'waits' => [
        'redis:default' => 60,
        'redis:critical,high' => 90,
    ],

<a name="metrics"></a>
## 메트릭

Horizon은 작업 및 큐의 대기 시간과 처리량을 제공하는 메트릭 대시보드를 포함합니다. 이 대시보드에 데이터를 채우려면, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)로 Horizon의 `snapshot` Artisan 명령어를 5분마다 실행하도록 예약하세요.

    /**
     * 애플리케이션 명령 스케줄 정의
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        $schedule->command('horizon:snapshot')->everyFiveMinutes();
    }

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용할 수 있습니다. 이 명령어는 실패한 작업의 ID 또는 UUID를 인수로 받습니다.

    php artisan horizon:forget 5

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 포함된 모든 작업을 삭제하려면, `horizon:clear` Artisan 명령어를 사용할 수 있습니다.

    php artisan horizon:clear

특정 큐의 작업만 삭제하려면, `queue` 옵션을 함께 지정하세요.

    php artisan horizon:clear --queue=emails