# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 인가](#dashboard-authorization)
    - [무음 처리된 작업](#silenced-jobs)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐의 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]
> Laravel Horizon을 사용하기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)를 먼저 익혀두는 것이 좋습니다. Horizon은 Laravel의 큐에 추가적인 기능을 제공하며, 기본 큐 기능에 익숙하지 않으면 다소 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/{{version}}/queues)에 대한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 실패 작업 등 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 설정이 하나의 단순한 설정 파일에 저장됩니다. 애플리케이션 워커 구성을 버전 관리되는 파일로 정의함으로써, 애플리케이션을 배포할 때 큐 워커를 손쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon은 큐 구동을 위해 [Redis](https://redis.io)가 필요합니다. 따라서 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 지정되어 있는지 확인해야 합니다.

Composer 패키지 관리자를 사용하여 프로젝트에 Horizon을 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

Horizon 설치 후, `horizon:install` Artisan 명령어를 사용하여 에셋을 퍼블리시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

Horizon 에셋을 퍼블리시한 후, 주요 설정 파일은 `config/horizon.php`에 위치하게 됩니다. 이 파일을 통해 애플리케이션의 큐 워커 옵션을 정의할 수 있습니다. 각 설정 옵션에는 그 목적에 대한 설명이 포함되어 있으므로, 이 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약되어 있으며, `database.php` 설정 파일이나 `horizon.php` 설정 파일의 `use` 옵션 값으로 다른 Redis 연결에 할당해서는 안 됩니다.

<a name="environments"></a>
#### 환경

설치 후 가장 먼저 익혀둘 설정 옵션은 `environments` 옵션입니다. 이 설정은 애플리케이션이 실행되는 각 환경과, 각 환경별 워커 프로세스 옵션을 정의하는 배열입니다. 기본적으로 `production`과 `local` 환경에 대한 항목이 있으며, 필요에 따라 환경을 추가할 수 있습니다:

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

별표(`*`) 환경을 정의하여, 다른 환경과 매칭되는 항목이 없을 경우 사용하도록 할 수도 있습니다:

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

Horizon을 시작하면, 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 설정 옵션을 사용하게 됩니다. 일반적으로 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment)의 값으로 결정됩니다. 예를 들어, 기본 `local` 환경은 세 개의 워커 프로세스를 시작하며, 각 큐에 할당된 워커 프로세스 수를 자동으로 조정합니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 시작하고, 마찬가지로 각 큐에 할당된 워커 프로세스 수를 자동으로 조정합니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments` 부분에는 Horizon을 실행할 [모든 환경](/docs/{{version}}/configuration#environment-configuration)에 대한 항목이 포함되어야 합니다.

<a name="supervisors"></a>
#### Supervisor

Horizon의 기본 설정 파일에서 볼 수 있듯, 각 환경에는 하나 이상의 "supervisor"를 포함할 수 있습니다. 기본적으로 이 supervisor의 이름은 `supervisor-1`로 정의되어 있으나, 원하는 대로 이름을 지정할 수 있습니다. 각 supervisor는 일련의 워커 프로세스를 "감독"하며, 큐 전체에 워커 프로세스를 균형 있게 분배하는 역할을 합니다.

특정 환경에서 실행되는 워커 프로세스 그룹을 새롭게 정의하고 싶다면 supervisor를 추가로 지정할 수 있습니다. 예를 들어, 애플리케이션이 사용하는 특정 큐에 대해 다른 부하 분산 전략이나 워커 프로세스 수를 지정하고자 할 때 사용할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지 관리 모드

애플리케이션이 [유지 관리 모드](/docs/{{version}}/configuration#maintenance-mode)일 때, supervisor의 `force` 옵션이 Horizon 설정 파일 내에 `true`로 정의되어 있지 않으면 대기 중인 작업이 Horizon에서 처리되지 않습니다:

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
#### 기본값

Horizon의 기본 설정 파일에는 `defaults`라는 설정 옵션이 있습니다. 이 옵션을 통해 애플리케이션의 [supervisor](#supervisors)에 대한 기본값을 지정할 수 있습니다. supervisor의 기본 설정값은 각 환경별 supervisor 설정에 병합되어, supervisor를 정의할 때 불필요한 반복을 피할 수 있습니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략

Laravel의 기본 큐 시스템과 달리, Horizon에서는 세 가지 워커 부하 분산 전략(`simple`, `auto`, `false`) 중에서 선택할 수 있습니다. `simple` 전략은 들어오는 작업을 워커 프로세스에 고르게 분배합니다:

    'balance' => 'simple',

`auto` 전략은 설정 파일의 기본값이며, 큐의 현재 작업 부하에 따라 각 큐별 워커 프로세스 수를 동적으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 중인 작업이 있고 `render` 큐가 비어 있는 경우, Horizon은 더 많은 워커를 `notifications` 큐에 할당하여 큐를 신속하게 비웁니다.

`auto` 전략을 사용할 때는 큐별 최소 워커 프로세스 수(`minProcesses`)와 전체 Horizon에서 사용할 최대 워커 프로세스 수(`maxProcesses`)를 설정할 수 있습니다:

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

`autoScalingStrategy` 설정 값은 Horizon이 더 많은 워커 프로세스를 큐에 할당할 때, 큐를 비우는 데 걸리는 총 시간(`time` 전략) 또는 큐에 쌓인 총 작업 건수(`size` 전략) 중 어떤 기준을 사용할지 결정합니다.

`balanceMaxShift`와 `balanceCooldown` 옵션은 Horizon이 워커 수요에 맞춰 얼마나 빠르게 확장 또는 축소할지 결정합니다. 위 예시에서는 최대 3초마다 하나의 프로세스만 새로 생성되거나 종료됩니다. 애플리케이션의 필요에 따라 이 값을 조정할 수 있습니다.

`balance` 옵션이 `false`로 설정되면, 라라벨의 기본 동작과 같이 큐 목록의 순서대로 작업이 처리됩니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근할 수 있습니다. 하지만 `app/Providers/HorizonServiceProvider.php` 파일 내에는 [인가 게이트](/docs/{{version}}/authorization#gates) 정의가 존재합니다. 이 인가 게이트는 **로컬 이외의 환경**에서 Horizon에 대한 접근을 제어합니다. 필요에 따라 이 게이트를 수정하여, Horizon 설치에 대한 접근을 제한할 수 있습니다:

```php
/**
 * Horizon 게이트를 등록합니다.
 *
 * 이 게이트는 비로컬 환경에서 누가 Horizon에 접근할 수 있는지 결정합니다.
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

라라벨은 게이트 클로저에 인증된 유저 객체를 자동으로 주입합니다. 만약 애플리케이션이 IP 제한 등 다른 방식으로 Horizon 보안을 제공하고 있다면, Horizon 사용자에게 별도의 "로그인"이 필요 없을 수 있습니다. 이런 경우 위의 `function (User $user)` 클로저 시그니처를 `function (User $user = null)`로 변경하여, 라라벨이 인증을 필수로 요구하지 않도록 해야 합니다.

<a name="silenced-jobs"></a>
### 무음 처리된 작업

애플리케이션이나 서드파티 패키지가 보낸 특정 작업의 결과를 보고 싶지 않을 때가 있습니다. 이러한 작업이 "완료된 작업" 목록에서 공간을 차지하지 않도록, 무음 처리할 수 있습니다. 사용하려면, 무음 처리할 작업의 클래스명을 애플리케이션의 `horizon` 설정 파일의 `silenced` 옵션에 추가하세요:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는, 무음 처리할 작업 클래스에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현할 수도 있습니다. 작업이 이 인터페이스를 구현하면, `silenced` 설정 배열에 없더라도 자동으로 무음 처리됩니다:

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 새로운 주요 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토하시기 바랍니다.

<a name="running-horizon"></a>
## Horizon 실행

애플리케이션의 `config/horizon.php` 설정 파일에서 supervisor와 워커 구성을 마쳤으면, `horizon` Artisan 명령어를 사용하여 Horizon을 시작할 수 있습니다. 이 명령어 하나로 현재 환경에 맞게 구성된 모든 워커 프로세스가 실행됩니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지하거나 다시 실행하도록 지시하려면 `horizon:pause` 및 `horizon:continue` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [supervisor](#supervisors)를 일시 중지하거나 다시 실행하려면 `horizon:pause-supervisor`와 `horizon:continue-supervisor` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon 프로세스의 현재 상태를 확인하려면 `horizon:status` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:status
```

특정 Horizon [supervisor](#supervisors)의 상태를 확인하려면 `horizon:supervisor-status` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료(Graceful Terminate)하려면 `horizon:terminate` Artisan 명령어를 사용하세요. 현재 처리 중인 작업이 모두 종료된 후, Horizon은 실행을 멈춥니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

Horizon을 실제 서버에 배포할 준비가 되면, 프로세스 모니터를 설정하여 `php artisan horizon` 명령이 종료될 경우 자동으로 재시작하도록 해야 합니다. 걱정하지 마세요, 아래에서 프로세스 모니터 설치 방법을 안내합니다.

애플리케이션 배포 과정 중에는 Horizon 프로세스를 종료(`terminate`)해서, 프로세스 모니터가 재시작하도록 하고, 변경된 코드가 반영되도록 해야 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터로서, `horizon` 프로세스가 중지되면 자동으로 재시작해줍니다. Ubuntu에서 Supervisor를 설치하려면 다음 명령을 사용할 수 있습니다. Ubuntu를 사용하지 않는 경우, 사용하는 운영체제의 패키지 관리자를 이용해 Supervisor를 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 어렵게 느껴진다면, [Laravel Cloud](https://cloud.laravel.com)의 이용을 고려해보세요. 이는 Laravel 애플리케이션의 백그라운드 프로세스를 관리해줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 내에, Supervisor가 프로세스를 어떻게 모니터링할지 지시하는 설정 파일을 여러 개 만들 수 있습니다. 예를 들어, `horizon.conf` 파일을 생성하여 `horizon` 프로세스를 시작 및 모니터링할 수 있습니다:

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

Supervisor 설정 시, `stopwaitsecs`의 값이 가장 오래 걸리는 작업이 소요하는 시간(초)보다 커야 합니다. 그렇지 않으면 Supervisor가 작업 처리 도중 프로세스를 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버에 적합하나, 서버의 운영체제에 따라 Supervisor 설정 파일의 위치와 파일 확장자가 다를 수 있습니다. 자세한 내용은 서버 문서를 참고하시기 바랍니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 생성한 후, 아래 명령어로 Supervisor 설정을 갱신하고 모니터링되는 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행에 대한 자세한 정보는 [Supervisor 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon을 이용하면 메일, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 작업에 “태그”를 지정할 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델에 따라 대부분의 작업을 자동으로 지능적으로 태깅합니다. 예를 들어, 아래 작업을 살펴보세요:

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
     * 새 작업 인스턴스 생성자.
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * 작업 실행 메서드.
     */
    public function handle(): void
    {
        // ...
    }
}
```

이 작업이 `id` 속성이 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 자동으로 `App\Models\Video:1` 태그가 부여됩니다. 이는 Horizon이 작업의 속성에서 Eloquent 모델을 찾아, 모델의 클래스명과 기본키(primary key)로 작업을 지능적으로 태깅하기 때문입니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업의 태그 수동 지정

큐 작업 클래스에 `tags` 메서드를 정의하여, 수동으로 태그를 직접 지정할 수 있습니다:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 지정할 태그 반환.
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
#### 이벤트 리스너의 태그 수동 지정

큐에 등록된 이벤트 리스너에 대해 태그를 검색할 때, Horizon은 이벤트 인스턴스를 `tags` 메서드에 자동으로 전달하므로, 태그에 이벤트 데이터를 추가할 수 있습니다:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 지정할 태그 반환.
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
## 알림

> [!WARNING]
> Horizon이 Slack 또는 SMS 알림을 보내도록 설정하려면, [해당 알림 채널의 사전 준비 사항](/docs/{{version}}/notifications)을 확인하시기 바랍니다.

큐의 대기 시간이 길어졌을 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드는 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하면 됩니다:

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

"오랜 대기"로 간주할 시간을 애플리케이션의 `config/horizon.php` 설정 파일에서 지정할 수 있습니다. 이 파일의 `waits` 옵션을 통해 각 연결/큐 조합별 임계값을 지정할 수 있습니다. 정의되지 않은 조합은 기본적으로 60초가 "오랜 대기"로 간주됩니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭

Horizon에는 작업 및 큐 대기 시간, 처리량에 대한 정보를 제공하는 메트릭 대시보드가 내장되어 있습니다. 이 대시보드를 채우기 위해, Horizon의 `snapshot` Artisan 명령어를 5분마다 실행하도록 애플리케이션의 `routes/console.php` 파일에 등록해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령을 사용하세요. 이 명령어에는 삭제할 실패 작업의 ID 또는 UUID를 인수로 전달합니다:

```shell
php artisan horizon:forget 5
```

실패한 모든 작업을 삭제하려면 `--all` 옵션을 사용할 수 있습니다:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐의 작업 비우기

애플리케이션의 기본 큐에서 모든 작업을 삭제하고 싶다면, `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐의 작업만 삭제하려면 `queue` 옵션을 사용할 수 있습니다:

```shell
php artisan horizon:clear --queue=emails
```
