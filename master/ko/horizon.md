# Laravel Horizon

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 인증](#dashboard-authorization)
    - [사일런스 처리된 작업](#silenced-jobs)
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
> Laravel Horizon을 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/{{version}}/queues)에 대해 익숙해지시기를 권장합니다. Horizon은 Laravel의 큐에 다양한 기능을 추가하므로, Laravel의 기본 큐 기능에 익숙하지 않다면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/{{version}}/queues)를 위한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 통해 작업 처리량, 실행 시간, 작업 실패 등 큐 시스템의 주요 메트릭을 손쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커의 설정이 하나의 간단한 설정 파일에 저장됩니다. 설정 파일을 버전 관리하므로, 애플리케이션을 배포할 때 큐 워커를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon은 큐를 작동하기 위해 반드시 [Redis](https://redis.io)를 사용해야 합니다. 따라서 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 반드시 `redis`로 설정되어 있는지 확인해야 합니다.

Composer 패키지 관리자를 사용하여 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어로 에셋을 배포하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

에셋을 배포한 후, 주요 설정 파일은 `config/horizon.php` 위치에 생성됩니다. 이 파일에서는 애플리케이션의 큐 워커 옵션을 설정할 수 있습니다. 각 옵션에는 목적에 대한 설명이 붙어 있으니, 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 Redis 연결을 사용합니다. 이 연결 이름은 예약되어 있으니, `database.php` 설정 파일 또는 `horizon.php`의 `use` 옵션 값으로 다른 연결에 할당하면 안 됩니다.

<a name="environments"></a>
#### 환경 설정

설치 후 반드시 익숙해져야 할 Horizon 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 동작하는 여러 환경별로 워커 프로세스 옵션을 정의하는 배열입니다. 기본적으로 `production`과 `local` 환경이 포함되어 있습니다. 필요에 따라 환경을 추가할 수 있습니다:

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

일치하는 환경이 없을 때 사용할 와일드카드 환경(`*`)도 정의할 수 있습니다:

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

Horizon을 실행하면, 애플리케이션이 현재 동작 중인 환경의 워커 프로세스 설정을 적용합니다. 보통 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#determining-the-current-environment) 값으로 결정됩니다. 예를 들어, 기본 `local` 환경에서는 워커 프로세스 3개가 실행되고, 각 큐에 자동으로 균등 분산됩니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 시작하고 자동 분산됩니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments`에 Horizon을 실행할 모든 [환경](/docs/{{version}}/configuration#environment-configuration)에 대한 항목이 포함되어 있는지 확인하세요.

<a name="supervisors"></a>
#### Supervisor(감독자)

기본 설정 파일에서 알 수 있듯, 각 환경에는 한 개 이상의 "supervisor(감독자)"를 포함할 수 있습니다. 기본적으로 `supervisor-1`로 정의되어 있으나, 원하는 이름으로 자유롭게 변경할 수 있습니다. 각 supervisor는 워커 프로세스의 그룹을 관리하며, 큐간 워커 수의 균형을 담당합니다.

특정 환경에 새로운 워커 그룹(새 supervisor)을 추가할 수 있습니다. 예를 들어, 애플리케이션에서 사용하는 특정 큐에 대해 다른 부하 분산 전략이나 워커 개수를 적용하고 싶을 때 사용할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)일 때, supervisor의 `force` 옵션이 `true`로 설정되어 있지 않으면 대기 중인 큐 작업이 Horizon에서 처리되지 않습니다:

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

Horizon의 기본 설정 파일에서 `defaults` 옵션을 확인할 수 있습니다. 이 옵션은 애플리케이션의 [supervisor](#supervisors)에 적용될 기본 값을 지정합니다. supervisor의 설정 값들과 병합되어 반복 정의를 피할 수 있습니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략

Laravel의 기본 큐와 달리 Horizon에서는 세 가지 워커 부하 분산 전략(`simple`, `auto`, `false`) 중 선택할 수 있습니다. `simple` 전략은 들어오는 작업을 워커 프로세스에 균등하게 분배합니다:

    'balance' => 'simple',

기본값인 `auto` 전략은 현재 큐의 작업량에 따라 큐마다 워커 수를 자동으로 조절합니다. 예를 들어, `notifications` 큐에는 1,000개의 대기 작업이 있고 `render` 큐에는 작업이 없는 경우, Horizon은 더 많은 워커를 `notifications` 큐에 할당해 큐를 빠르게 비웁니다.

`auto` 전략에서는 큐별 프로세스 최소/최대 개수를 `minProcesses`, `maxProcesses`로 제어할 수 있습니다:

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

`autoScalingStrategy` 값은 Horizon이 큐를 정리하는 전체 예상 시간(`time`) 기준이거나 큐에 남은 작업 수(`size`) 기준 중 무엇으로 워커를 확장할지 결정합니다.

`balanceMaxShift`와 `balanceCooldown`은 워커 확장 속도를 조절합니다. 위 예시에서는 3초마다 최대 1개의 새 프로세스가 생성 혹은 제거됩니다. 애플리케이션 상황에 맞게 값은 자유롭게 조정할 수 있습니다.

`balance` 옵션이 `false`인 경우, 라라벨 기본 동작과 같이 설정에 나열된 순서대로 큐가 처리됩니다.

<a name="dashboard-authorization"></a>
### 대시보드 인증

Horizon 대시보드는 `/horizon` 경로로 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근할 수 있습니다. 단, `app/Providers/HorizonServiceProvider.php` 파일 내에 [인증 게이트](/docs/{{version}}/authorization#gates) 정의가 있습니다. 이 게이트는 **local이 아닌 환경**에서 Horizon 접근을 제어하며, 필요에 따라 Horizon 접근을 제한할 수 있습니다:

```php
/**
 * Horizon 게이트 등록
 *
 * 이 게이트는 non-local 환경에서 Horizon 접근자를 제어합니다.
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
#### 대체 인증 방식

라라벨은 인증된 사용자를 게이트 클로저에 자동으로 주입합니다. IP 제한 등 다른 방식으로 Horizon 보안을 적용할 경우, 사용자는 "로그인"이 필요하지 않을 수 있습니다. 이 때, 위 클로저 시그니처를 `function (User $user = null)`로 변경하여 인증이 필수가 아니도록 하면 됩니다.

<a name="silenced-jobs"></a>
### 사일런스 처리된 작업

애플리케이션이나 서드파티 패키지가 디스패치한 특정 작업을 "완료된 작업" 목록에서 제외하고 싶을 수 있습니다. 이럴 때 해당 작업을 사일런스 처리할 수 있습니다. 먼저, `horizon` 설정 파일의 `silenced`에 작업 클래스명을 추가하세요:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는, 사일런스하고자 하는 작업 클래스가 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, 설정 배열에 없어도 자동으로 사일런스 처리됩니다:

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

Horizon의 새 메이저 버전으로 업그레이드할 때는, [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 반드시 꼼꼼하게 확인해야 합니다.

<a name="running-horizon"></a>
## Horizon 실행

`config/horizon.php`에서 supervisor 및 worker 설정을 완료했다면, `horizon` Artisan 명령어로 Horizon을 실행할 수 있습니다. 이 한 명령으로 현재 환경에 맞게 모든 워커 프로세스가 시작됩니다:

```shell
php artisan horizon
```

`horizon:pause`와 `horizon:continue` Artisan 명령어를 사용해 Horizon 프로세스를 일시 중지하거나 재개할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 [supervisor](#supervisors)를 일시 중지/재개하는 것도 가능합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

`horizon:status` 명령어로 Horizon의 현재 상태를 확인할 수 있습니다:

```shell
php artisan horizon:status
```

특정 [supervisor](#supervisors)의 상태도 확인 가능합니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

`horizon:terminate` 명령어로 Horizon 프로세스를 정상 종료할 수 있습니다. 처리 중인 작업은 완료 후 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

운영 서버에 Horizon을 배포할 준비가 되었다면, `php artisan horizon` 명령을 모니터링하고 비정상 종료 시 자동 재시작하도록 프로세스 모니터를 설정해야 합니다. 프로세스 모니터 설치 방법도 아래에서 소개합니다.

배포 과정 중 새로운 코드를 반영하려면 Horizon 프로세스의 종료를 안내하여, 프로세스 모니터가 프로세스를 재시작하게 만들어야 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux용 프로세스 모니터로, `horizon` 프로세스가 종료되면 자동으로 재시작해줍니다. Ubuntu에서는 다음 명령어로 Supervisor를 설치할 수 있습니다. Ubuntu 사용 중이 아니라면, 운영체제의 패키지 관리자로 Supervisor 설치가 가능합니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 어렵게 느껴진다면 [Laravel Cloud](https://cloud.laravel.com)를 고려해보세요. 백그라운드 프로세스는 Laravel Cloud에서 관리할 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 디렉토리 내에 원하는 만큼 설정 파일을 생성하여, supervisor에게 프로세스 모니터링 방법을 지시할 수 있습니다. 예를 들어 `horizon.conf` 파일을 생성해 `horizon` 프로세스를 시작 및 모니터링하도록 할 수 있습니다:

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

Supervisor의 `stopwaitsecs` 값은, 가장 오래 실행되는 작업의 소요 시간보다 충분히 커야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 종료해버릴 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 서버에서 유효합니다. 운영체제에 따라 Supervisor 설정 파일의 위치나 확장자가 다를 수 있으니, 서버 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일 생성 후, 아래 명령어로 Supervisor 설정을 갱신하고 실행 중인 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 사용법에 대한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 작업, 메일러블, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 작업에 "태그"를 지정할 수 있도록 해줍니다. 대부분의 작업은 연결된 Eloquent 모델에 따라 Horizon이 태그를 자동으로 지정합니다. 예를 들어, 다음 작업을 살펴보겠습니다:

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
     * 새 작업 인스턴스 생성
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

이 작업이 `id` 값이 `1`인 `App\Models\Video` 인스턴스로 큐에 등록된다면, 자동으로 `App\Models\Video:1` 태그가 붙습니다. Horizon은 작업 속성에서 Eloquent 모델을 찾아, 모델 클래스명과 기본키를 활용해 태그를 지정합니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업에 태그 수동 지정

큐잉 가능한 객체에서 직접 태그를 지정하고 싶다면, 클래스에 `tags` 메서드를 정의하면 됩니다:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 부여할 태그 반환
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
#### 이벤트 리스너에 태그 수동 지정

큐에 등록된 이벤트 리스너의 태그 조회 시, Horizon은 이벤트 인스턴스를 `tags` 메서드에 전달해줍니다. 따라서 태그에 이벤트 데이터를 활용할 수 있습니다:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 부여할 태그 반환
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
> Horizon이 Slack 또는 SMS 알림을 보내도록 설정할 때는, [해당 알림 채널의 사전 요구 사항](/docs/{{version}}/notifications)을 확인하시기 바랍니다.

큐 중 하나의 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드는 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하세요:

```php
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

애플리케이션의 `config/horizon.php`에서 "대기 시간이 길다"고 간주할 기준(초 단위)을 설정할 수 있습니다. 파일의 `waits` 옵션에서 연결/큐별로 기준치를 조정할 수 있습니다. 정의되지 않은 연결/큐 조합은 기본적으로 60초가 적용됩니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭

Horizon에는 작업과 큐의 대기 시간 및 처리량 정보를 제공하는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드에 데이터를 채우려면, 애플리케이션의 `routes/console.php`에 Horizon의 `snapshot` Artisan 명령어가 5분마다 실행되도록 예약하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하고 싶다면 `horizon:forget` 명령을 사용할 수 있습니다. 작업의 ID나 UUID를 인자로 받습니다:

```shell
php artisan horizon:forget 5
```

실패한 모든 작업을 삭제하려면, `--all` 옵션을 제공합니다:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에서 모든 작업을 삭제하고 싶다면, `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐의 작업을 비우려면 `queue` 옵션을 사용할 수 있습니다:

```shell
php artisan horizon:clear --queue=emails
```
