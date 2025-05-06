# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [로드 밸런싱 전략](#balancing-strategies)
    - [대시보드 권한](#dashboard-authorization)
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

> **참고**  
> Laravel Horizon을 사용하기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)에 대해 익숙해지는 것이 좋습니다. Horizon은 Laravel의 큐 기능에 다양한 부가 기능을 제공하므로, 기본 큐 기능에 익숙하지 않다면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/{{version}}/queues)를 위한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 통해 작업 처리량, 실행 시간, 실패한 작업 등 큐 시스템의 주요 지표를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용할 때는 모든 큐 워커 설정이 하나의 간단한 설정 파일에 저장됩니다. 설정 파일을 버전 관리함으로써, 애플리케이션 배포 시 큐 워커의 수평 확장이나 수정이 매우 용이해집니다.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## 설치

> **경고**  
> Laravel Horizon은 [Redis](https://redis.io)로 구동되는 큐가 필요합니다. 따라서, `config/queue.php`의 큐 연결이 반드시 `redis`로 설정되어 있는지 확인하세요.

Composer 패키지 관리자를 통해 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어로 Horizon의 에셋을 게시하십시오:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

에셋을 게시하면, 주요 설정 파일은 `config/horizon.php`에 위치합니다. 이 파일에서 애플리케이션의 큐 워커 옵션들을 설정할 수 있습니다. 각 옵션에는 목적에 대한 설명이 있으니, 꼭 전체 파일을 꼼꼼히 살펴보시기 바랍니다.

> **경고**  
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약어이므로, `database.php`나 `horizon.php` 설정 파일의 `use` 옵션에 다른 연결로 할당하지 않도록 주의하세요.

<a name="environments"></a>
#### 환경 설정

설치 후 가장 먼저 익숙해져야 할 Horizon의 주요 설정 옵션은 `environments` 항목입니다. 이 옵션은 애플리케이션이 운영되는 환경별로 워커 프로세스 옵션을 정의하는 배열입니다. 기본적으로 `production`과 `local` 환경이 제공되지만, 필요에 따라 환경을 추가할 수 있습니다:

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

Horizon을 실행하면, 현재 애플리케이션 환경에 맞는 워커 프로세스 설정이 적용됩니다. 환경은 보통 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment) 값으로 결정됩니다. 예를 들어, 기본 `local` 환경에서는 세 개의 워커 프로세스가 실행되며, 각 큐에 할당된 워커 수가 자동으로 조절됩니다. 기본 `production` 환경에서는 최대 10개의 프로세스가 시작되고, 역시 워커가 자동으로 분배됩니다.

> **경고**  
> `horizon` 설정 파일의 `environments` 배열에는 Horizon을 실행하려는 모든 [환경](/docs/{{version}}/configuration#environment-configuration)에 대한 항목이 반드시 있어야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisors)

Horizon의 기본 설정 파일을 보면, 각 환경에 하나 이상의 "슈퍼바이저"를 포함할 수 있음을 알 수 있습니다. 기본적으로 이 슈퍼바이저의 이름은 `supervisor-1`이지만, 원하는 이름을 자유롭게 사용할 수 있습니다. 각 슈퍼바이저는 워커 프로세스 그룹을 "감독"하면서, 큐에 걸쳐 워커의 균형 분배를 담당합니다.

특정 환경에 추가 슈퍼바이저를 추가하여, 그 환경에서 별도의 워커 그룹을 실행할 수 있습니다. 예를 들어, 큐별로 다른 로드 밸런싱 전략이나 워커 수를 정의하려면 이렇게 할 수 있습니다.

<a name="default-values"></a>
#### 기본값

Horizon의 기본 설정 파일에는 `defaults` 옵션이 있습니다. 이 옵션은 [슈퍼바이저](#supervisors)의 기본값을 지정하며, 각 환경의 슈퍼바이저 설정에 병합되어 동일한 설정을 반복할 필요를 줄여줍니다.

<a name="balancing-strategies"></a>
### 로드 밸런싱 전략

Laravel의 기본 큐 시스템과 달리, Horizon은 `simple`, `auto`, `false` 3가지 워커 밸런싱 전략을 제공합니다. 기본값인 `simple` 전략은 들어오는 작업을 워커 프로세스에 고르게 분배합니다:

    'balance' => 'simple',

`auto` 전략은 큐의 현재 작업량에 따라 큐별 워커 프로세스 수를 조절합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고, `render` 큐는 비어 있다면, Horizon은 `notifications` 큐에 더 많은 워커를 할당해 작업이 모두 처리될 때까지 유지합니다.

`auto` 전략을 사용할 때, `minProcesses`와 `maxProcesses` 옵션으로 최소 및 최대 워커 프로세스 수를 설정할 수 있습니다:

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

`balanceMaxShift`와 `balanceCooldown` 값은 Horizon이 워커 수를 얼마나 빠르게 조절할지 결정합니다. 위 예시에서는 3초에 한 번씩 최대 하나의 프로세스를 새로 만들거나 종료합니다. 필요에 따라 이 값을 조정할 수 있습니다.

`balance` 옵션이 `false`일 경우, Laravel 기본 동작이 적용되어, 큐가 설정에 나열된 순서대로 처리됩니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한

Horizon은 `/horizon` URI에 대시보드를 제공합니다. 기본적으로, `local` 환경에서만 대시보드에 접근할 수 있습니다. 하지만, `app/Providers/HorizonServiceProvider.php` 파일에는 [권한 게이트](/docs/{{version}}/authorization#gates) 정의가 포함되어 있습니다. 이 게이트는 **비-local** 환경에서 Horizon 접근 권한을 제어합니다. 필요에 따라 아래 게이트를 수정해 Horizon 설치의 접근을 제한할 수 있습니다:

    /**
     * Horizon 게이트 등록
     *
     * 이 게이트는 비-local 환경에서 Horizon에 접근할 수 있는 사용자를 결정합니다.
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

Laravel은 인증된 사용자를 자동으로 게이트 클로저에 주입합니다. 만약 IP 제한 등 다른 인증 수단으로 Horizon 보안을 제공한다면, 사용자가 반드시 "로그인"할 필요는 없습니다. 따라서 위 클로저 시그니처를 `function ($user = null)`로 변경하여 인증 요구를 강제하지 않도록 해야 합니다.

<a name="silenced-jobs"></a>
### 무음 처리된 작업

때로는 애플리케이션이나 외부 패키지에서 발생한 특정 작업이 "완료된 작업" 목록에 보이길 원하지 않을 수 있습니다. 이 경우, 해당 작업을 무음 처리하여 리스트에서 제외할 수 있습니다. 사용 방법은 `horizon` 설정 파일의 `silenced` 옵션에 작업의 클래스 이름을 추가하면 됩니다:

    'silenced' => [
        App\Jobs\ProcessPodcast::class,
    ],

또는 무음 처리를 원하는 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 할 수도 있습니다. 이렇게 하면 설정 배열에 명시하지 않아도 작업이 자동으로 무음 처리됩니다:

    use Laravel\Horizon\Contracts\Silenced;

    class ProcessPodcast implements ShouldQueue, Silenced
    {
        use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

        // ...
    }

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다. 또한, 새로운 Horizon 버전으로 업그레이드할 때마다 Horizon의 에셋을 다시 게시해야 합니다:

```shell
php artisan horizon:publish
```

향후 업데이트에서 문제가 없도록 에셋을 최신 상태로 유지하려면, 애플리케이션의 `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령을 추가하세요:

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

애플리케이션의 `config/horizon.php` 파일에서 슈퍼바이저와 워커를 설정한 후에는, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령어 한 번으로 현재 환경의 모든 워커 프로세스가 시작됩니다:

```shell
php artisan horizon
```

`horizon:pause`, `horizon:continue` Artisan 명령어로 Horizon을 일시정지하거나 다시 작업을 처리하도록 지시할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

또한, `horizon:pause-supervisor`, `horizon:continue-supervisor` 명령어로 특정 Horizon [슈퍼바이저](#supervisors)를 일시정지하거나 계속 진행할 수 있습니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

`horizon:status` 명령어로 현재 Horizon 프로세스의 상태를 확인할 수 있습니다:

```shell
php artisan horizon:status
```

`horizon:terminate` 명령어로 Horizon 프로세스를 정상적으로 종료할 수 있습니다. 현재 처리 중인 작업은 끝까지 실행된 후 Horizon이 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

Horizon을 실제 서버에 배포할 준비가 되면, `php artisan horizon` 명령을 상시 모니터링하고, 비정상 종료 시 재시작할 수 있도록 프로세스 모니터를 설정해야 합니다. 설치 방법은 아래에서 다룹니다.

배포 과정에서는 반드시 Horizon 프로세스를 종료(`terminate`)하여 프로세스 모니터가 재시작하면서 코드 변경 사항을 적용받도록 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스에서 프로세스를 감시하고, 실행 중단 시 자동 재시작하는 도구입니다. Ubuntu에서는 아래 명령어로 Supervisor를 설치할 수 있습니다. Ubuntu가 아니라면 운영체제의 패키지 관리자를 이용하세요:

```shell
sudo apt-get install supervisor
```

> **참고**  
> Supervisor 직접 설정이 부담스럽다면, [Laravel Forge](https://forge.laravel.com) 사용을 고려하세요. Laravel Forge는 Supervisor 설치 및 설정을 자동으로 처리해줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 서버의 `/etc/supervisor/conf.d` 디렉터리에 주로 위치합니다. 이 디렉터리에 프로세스 모니터링 방법을 정의하는 여러 개의 설정 파일을 생성할 수 있습니다. 예를 들어, `horizon.conf` 파일을 만들어 horizon 프로세스를 시작하고 모니터링하도록 할 수 있습니다:

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

Supervisor 설정 시 `stopwaitsecs` 값을 가장 오래 실행되는 작업 시간보다 크게 설정해야 합니다. 그렇지 않으면 Supervisor가 작업 완료 전에 프로세스를 강제로 종료할 수 있습니다.

> **경고**  
> 위 예제는 Ubuntu 서버에 유효하지만, Supervisor의 설정 파일 위치 및 확장자는 운영체제에 따라 다를 수 있습니다. 자세한 내용은 서버 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 작성한 후, 다음 명령어로 Supervisor 구성을 갱신하고 모니터링 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> **참고**  
> Supervisor 실행에 대한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 메일, 브로드캐스트 이벤트, 알림, 큐 이벤트 리스너 등 여러 작업에 "태그"를 지정할 수 있게 합니다. 실제로, Horizon은 작업에 연결된 Eloquent 모델을 참고해 대부분의 작업에 자동으로 태그를 부여합니다. 예를 들면:

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
         * 동영상 인스턴스
         *
         * @var \App\Models\Video
         */
        public $video;

        /**
         * 새 작업 인스턴스 생성
         *
         * @param  \App\Models\Video  $video
         * @return void
         */
        public function __construct(Video $video)
        {
            $this->video = $video;
        }

        /**
         * 작업 실행
         *
         * @return void
         */
        public function handle()
        {
            //
        }
    }

이 작업이 `id`가 1인 `App\Models\Video` 인스턴스로 큐에 들어가면, 자동으로 `App\Models\Video:1`이라는 태그가 지정됩니다. Horizon은 작업의 프로퍼티에서 Eloquent 모델을 찾아, 모델 클래스명과 기본키를 조합해 태그를 자동 생성하기 때문입니다.

    use App\Jobs\RenderVideo;
    use App\Models\Video;

    $video = Video::find(1);

    RenderVideo::dispatch($video);

<a name="manually-tagging-jobs"></a>
#### 작업에 수동으로 태그 지정

큐 가능한 객체에 수동으로 태그를 지정하려면, 클래스에 `tags` 메소드를 정의할 수 있습니다:

    class RenderVideo implements ShouldQueue
    {
        /**
         * 작업에 적용할 태그 반환
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

> **경고**  
> Horizon에서 Slack 또는 SMS 알림을 설정하려면, 해당 알림 채널의 [사전 조건](/docs/{{version}}/notifications)을 반드시 검토하세요.

특정 큐의 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메소드를 통해 호출할 수 있습니다:

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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

"대기 시간이 김"으로 간주되는 초 단위 임계값을 `config/horizon.php` 파일의 `waits` 옵션에서 큐별로 지정할 수 있습니다:

    'waits' => [
        'redis:default' => 60,
        'redis:critical,high' => 90,
    ],

<a name="metrics"></a>
## 메트릭

Horizon에는 작업과 큐의 대기 시간, 처리량 등 정보를 제공하는 메트릭 대시보드가 있습니다. 이 대시보드를 채우기 위해서는 `horizon:snapshot` Artisan 명령어를 [스케줄러](/docs/{{version}}/scheduling)를 통해 5분마다 실행하도록 설정해야 합니다:

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

실패한 특정 작업을 삭제하려면, `horizon:forget` 명령을 사용하세요. 이 명령의 인수로 실패한 작업의 ID 또는 UUID를 전달합니다:

```shell
php artisan horizon:forget 5
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에서 모든 작업을 삭제하려면, `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐에서만 작업을 삭제하려면 `queue` 옵션을 제공할 수 있습니다:

```shell
php artisan horizon:clear --queue=emails
```
