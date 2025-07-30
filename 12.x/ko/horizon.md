# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [밸런싱 전략](#balancing-strategies)
    - [대시보드 권한 설정](#dashboard-authorization)
    - [숨겨진 작업](#silenced-jobs)
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
> Laravel Horizon을 자세히 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/12.x/queues)에 대해 익숙해져야 합니다. Horizon은 Laravel 큐에 추가 기능을 더하는 역할을 하므로, 기본 큐 기능에 익숙하지 않다면 다소 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/12.x/queues)를 위한 세련된 대시보드와 코드 중심의 구성을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패와 같은 큐 시스템의 주요 지표를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용할 때 모든 큐 작업자(worker)의 구성은 단일하고 간단한 구성 파일에 저장됩니다. 애플리케이션의 작업자 구성을 버전 관리 파일로 정의함으로써, 배포 시 큐 작업자를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Laravel Horizon은 큐로 [Redis](https://redis.io)를 사용해야 합니다. 따라서 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 설정되어 있는지 반드시 확인하세요.

Composer 패키지 관리자를 사용하여 프로젝트에 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후 `horizon:install` Artisan 명령어로 Horizon의 자산을 퍼블리시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정 (Configuration)

Horizon 자산을 퍼블리시하면, 기본 구성 파일은 `config/horizon.php`에 위치하게 됩니다. 이 구성 파일에서는 애플리케이션의 큐 작업자 옵션을 설정할 수 있습니다. 각 옵션별 설명이 포함되어 있으니, 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약어이므로, `database.php` 설정 파일이나 `horizon.php` 파일의 `use` 옵션 값으로 중복 지정하지 마세요.

<a name="environments"></a>
#### 환경 (Environments)

설치 후, 가장 먼저 익혀야 할 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 실행되는 여러 환경에 대한 배열이며, 각 환경별 작업자 프로세스 옵션을 정의합니다. 기본값으로는 `production`과 `local` 환경이 포함되어 있지만 필요에 따라 더 추가할 수 있습니다:

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

또한, 와일드카드 환경(`*`)을 정의하여 일치하는 환경이 없을 때 기본값으로 사용할 수 있습니다:

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

Horizon을 시작하면, 현재 애플리케이션이 실행 중인 환경에 정의된 작업자 프로세스 설정을 사용합니다. 보통 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment) 값으로 결정됩니다. 예를 들어, 기본 `local` 환경은 3개의 작업자 프로세스를 시작하고 각 큐에 작업자 수를 자동으로 균등 분배하도록 설정되어 있습니다. 기본 `production` 환경은 최대 10개의 작업자 프로세스를 시작하고, 작업자 수를 자동으로 균형 조정하도록 구성되어 있습니다.

> [!WARNING]
> `horizon` 구성 파일의 `environments` 항목에 Horizon을 실행하려는 모든 [환경](/docs/12.x/configuration#environment-configuration)에 대한 설정이 반드시 포함되어야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저 (Supervisors)

Horizon 기본 구성 파일에서 볼 수 있듯, 각 환경은 하나 이상의 "슈퍼바이저"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 이름이 지정되어 있지만, 필요에 따라 원하는 이름으로 변경할 수 있습니다. 각 슈퍼바이저는 일종의 작업자 그룹을 관리하며, 작업자 프로세스가 여러 큐를 적절히 나눠 처리하도록 균형을 맞추는 역할을 합니다.

필요하다면 환경 내에 여러 슈퍼바이저를 추가하여 각기 다른 큐에 대해 별도의 균형 조정 전략이나 작업자 수를 정의할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지 보수 모드 (Maintenance Mode)

애플리케이션이 [유지 보수 모드](/docs/12.x/configuration#maintenance-mode)일 경우, Horizon은 큐에 쌓인 작업들을 처리하지 않습니다. 다만, `force` 옵션을 `true`로 설정한 슈퍼바이저는 예외로 계속 작업을 처리할 수 있습니다:

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
#### 기본값 (Default Values)

Horizon 기본 구성 파일에서 `defaults` 옵션을 볼 수 있습니다. 이 옵션은 애플리케이션의 [슈퍼바이저](#supervisors)에 적용할 기본 설정값을 지정하며, 환경별 슈퍼바이저 설정에 병합되어 불필요한 반복을 줄여줍니다.

<a name="balancing-strategies"></a>
### 밸런싱 전략 (Balancing Strategies)

Laravel 기본 큐 시스템과 달리 Horizon은 세 가지 작업자 밸런싱 전략(`simple`, `auto`, `false`) 중에서 선택할 수 있습니다. `simple` 전략은 들어오는 작업들을 작업자 프로세스 간에 균등하게 분배합니다:

```
'balance' => 'simple',
```

`auto` 전략은 구성 파일의 기본값이며, 큐의 작업 대기량에 따라 작업자 수를 조절합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고, `render` 큐가 비어 있다면, Horizon은 `notifications` 큐에 더 많은 작업자를 할당해 작업이 모두 처리될 때까지 자동으로 조정합니다.

`auto` 전략을 사용하는 경우, `minProcesses`와 `maxProcesses` 옵션을 정의하여 큐별 최소 작업자 수와 Horizon이 자동으로 확장 또는 축소할 최대 작업자 수를 조절할 수 있습니다:

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

`autoScalingStrategy`는 큐 청소에 걸리는 총 시간(`time` 전략) 또는 큐에 있는 작업 개수(`size` 전략)를 기준으로 작업자 수를 늘릴지 결정합니다.

`balanceMaxShift`와 `balanceCooldown`은 작업자 수를 조정하는 속도를 나타냅니다. 위 예제에서는 최대 1개의 프로세스가 3초마다 생성되거나 종료될 수 있습니다. 필요에 따라 애플리케이션 요구에 맞게 이 값을 조절하세요.

`balance` 옵션이 `false`로 설정되면 Laravel 기본 동작을 따르며, 설정에 나열된 순서대로 큐를 처리합니다.

<a name="dashboard-authorization"></a>
### 대시보드 권한 설정 (Dashboard Authorization)

Horizon 대시보드는 기본적으로 `/horizon` 경로를 통해 접근할 수 있습니다. 기본 설정으로는 오직 `local` 환경에서만 이 대시보드에 접근할 수 있습니다. 하지만 `app/Providers/HorizonServiceProvider.php` 파일 내에 [권한 게이트](/docs/12.x/authorization#gates)가 정의되어 있으며, 이는 **비로컬 환경**에서 Horizon 접속을 제어합니다. 필요에 따라 이 게이트를 수정해 Horizon 접속을 제한할 수 있습니다:

```php
/**
 * Horizon 게이트를 등록합니다.
 *
 * 이 게이트는 비로컬 환경에서 Horizon에 접근할 수 있는 사용자를 결정합니다.
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

Laravel은 게이트 클로저에 인증된 사용자를 자동으로 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 보안을 제공하고 있어, 사용자가 별도의 로그인이 필요 없다면 위의 `function (User $user)` 클로저 시그니처를 `function (User $user = null)`로 변경해 Laravel이 인증을 요구하지 않도록 해야 합니다.

<a name="silenced-jobs"></a>
### 숨겨진 작업 (Silenced Jobs)

경우에 따라 애플리케이션이나 서드파티 패키지에서 디스패치된 특정 작업들을 '완료된 작업' 목록에서 보고 싶지 않을 수 있습니다. 이런 작업들이 목록을 차지하지 않도록 숨길 수 있는데, 이를 위해 `horizon` 설정 파일의 `silenced` 배열에 클래스 이름을 추가하세요:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는 숨기려는 작업 클래스가 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, `silenced` 배열에 없어도 자동으로 숨김 처리됩니다:

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

Horizon의 주요 버전 업그레이드 시, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토하시기 바랍니다.

<a name="running-horizon"></a>
## Horizon 실행하기 (Running Horizon)

애플리케이션의 `config/horizon.php`에서 슈퍼바이저와 작업자 구성을 완료하면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령어 하나로 현재 환경에 구성된 모든 작업자 프로세스를 실행합니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지하고 이후 작업 처리를 재개하려면 다음 명령어를 사용하세요:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)를 일시 중지하거나 계속 실행하려면, 아래 명령을 참고하세요:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스 상태는 다음 명령어로 확인할 수 있습니다:

```shell
php artisan horizon:status
```

특정 슈퍼바이저 상태 확인은 다음과 같이 실행합니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상 종료시키고자 할 때는 이 명령어를 사용하세요. 처리 중인 작업은 완료 후 종료합니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포하기 (Deploying Horizon)

애플리케이션 서버에 Horizon을 배포할 준비가 되면, `php artisan horizon` 명령 수행 프로세스를 모니터링하고 비정상 종료 시 자동 재시작하는 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설치 방법을 설명합니다.

배포 과정 중에는 다음 명령어로 Horizon 프로세스를 종료시키고, 프로세스 모니터가 재시작하도록 지시하세요:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터로, Horizon 프로세스가 멈추면 자동으로 재시작합니다. Ubuntu에서는 다음 명령어로 설치 가능합니다. 다른 운영체제는 각자의 패키지 관리자를 통해 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 어렵다면, Laravel 애플리케이션의 백그라운드 프로세스 관리를 담당하는 [Laravel Cloud](https://cloud.laravel.com) 서비스 이용을 고려해보세요.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버 내 `/etc/supervisor/conf.d` 디렉토리에 위치합니다. 이 폴더에 여러 개의 설정 파일을 만들어 Supervisor가 관리할 프로세스를 지정할 수 있습니다. 예를 들어, `horizon.conf` 파일을 생성해 `horizon` 프로세스를 시작하고 모니터링할 수 있습니다:

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

`stopwaitsecs` 값은 가장 오래 걸리는 작업 소요 시간보다 길게 설정해야 하며, 그렇지 않으면 Supervisor가 작업 종료 전에 프로세스를 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 서버에 적합하며, 다른 운영체제는 Supervisor 설정 파일 위치 및 확장자가 다를 수 있으니 해당 서버 문서를 참조하세요.

<a name="starting-supervisor"></a>
#### Supervisor 실행

설정 파일 생성 후에는 Supervisor 구성을 다시 읽고 적용한 뒤, Horizon 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행 및 관리에 대한 자세한 내용은 [Supervisor 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 큐에 넣은 작업뿐만 아니라 메일, 방송 이벤트, 알림, 큐 이벤트 리스너 등에도 "태그"를 부여할 수 있습니다. 더 나아가 Horizon은 해당 작업에 연결된 Eloquent 모델을 통해 대부분의 작업에 자동으로 태그를 지능적으로 할당합니다. 예를 들면, 다음과 같은 작업을 봅시다:

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
     * 새 작업 인스턴스 생성.
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * 작업 실행.
     */
    public function handle(): void
    {
        // ...
    }
}
```

이 작업이 `id`가 1인 `App\Models\Video` 인스턴스와 함께 큐에 넣어지면, 자동으로 `App\Models\Video:1` 태그가 붙습니다. 이는 Horizon이 작업의 속성에서 Eloquent 모델을 찾아내고, 모델 클래스명과 기본키를 사용해 태그를 생성하기 때문입니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 수동 태그 부여하기

큐 작업 클래스에서 수동으로 태그를 정의하고 싶다면, `tags` 메서드를 구현하면 됩니다:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 할당할 태그 반환.
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
#### 이벤트 리스너에 수동 태그 부여하기

큐에 넣은 이벤트 리스너에서 태그를 조회할 때, Horizon은 이벤트 인스턴스를 `tags` 메서드에 자동으로 전달하므로 이벤트 데이터를 태그에 포함할 수 있습니다:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 할당할 태그 반환.
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
> Slack 또는 SMS 알림을 설정할 때는 해당 알림 채널에 맞는 [사전 준비 사항](/docs/12.x/notifications)을 반드시 확인하세요.

큐의 대기 시간이 길어질 경우 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 보통 애플리케이션의 `App\Providers\HorizonServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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
#### 알림 대기 시간 임계값 구성

대기 시간이 얼마나 길어야 ‘긴 대기’로 간주할지, `config/horizon.php`에서 `waits` 옵션으로 조절할 수 있습니다. 이 값은 연결 및 큐 조합별로 설정할 수 있으며, 미정의된 경우 기본값은 60초입니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 지표 (Metrics)

Horizon에는 작업 및 큐 대기 시간과 처리량에 관한 정보를 보여주는 지표 대시보드가 포함되어 있습니다. 이 대시보드를 채우려면, 애플리케이션의 `routes/console.php` 파일에서 Horizon의 `snapshot` Artisan 명령을 5분마다 실행하도록 예약해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 지표 데이터를 삭제하고 싶다면 `horizon:clear-metrics` Artisan 명령을 실행하세요:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제 (Deleting Failed Jobs)

실패한 작업을 삭제하려면 `horizon:forget` 명령을 사용하세요. 이 명령은 삭제할 작업의 ID나 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 삭제하려면 `--all` 옵션을 함께 사용합니다:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제 (Clearing Jobs From Queues)

애플리케이션 기본 큐에서 모든 작업을 삭제하고 싶다면 `horizon:clear` Artisan 명령을 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐에서 작업을 삭제하려면 `queue` 옵션을 지정합니다:

```shell
php artisan horizon:clear --queue=emails
```