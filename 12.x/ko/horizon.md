# 라라벨 Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [부하 분산 전략](#balancing-strategies)
    - [대시보드 접근 권한](#dashboard-authorization)
    - [제외된 작업(Silenced Jobs)](#silenced-jobs)
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
> 라라벨 Horizon을 학습하기 전에, 우선 라라벨의 기본 [큐 서비스](/docs/12.x/queues)에 익숙해지시는 것이 좋습니다. Horizon은 라라벨의 큐 기능을 확장해주지만, 기본 큐 기능을 이해하지 않으면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 라라벨 기반의 [Redis 큐](/docs/12.x/queues) 시스템을 위한 시각화 대시보드와 코드 기반의 손쉬운 설정 기능을 제공합니다. Horizon을 통해 큐 시스템의 주요 지표(처리량, 실행 시간, 작업 실패 등)를 쉽게 모니터링할 수 있습니다.

Horizon을 사용하면, 모든 큐 워커(작업자) 관련 설정이 하나의 간결한 설정 파일에 저장됩니다. 이처럼 설정을 버전 관리 파일로 관리하면, 애플리케이션을 배포할 때 큐 워커를 손쉽게 확장하거나 변경할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> 라라벨 Horizon을 사용하기 위해서는 [Redis](https://redis.io)를 큐 백엔드로 반드시 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 지정되어 있는지 확인하세요.

Composer 패키지 관리자를 이용해 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` 아티즌 명령어를 실행해 Horizon의 에셋을 배포합니다:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

Horizon의 에셋을 배포하면, 주 설정 파일이 `config/horizon.php`에 생성됩니다. 이 파일에서 애플리케이션의 큐 워커 옵션을 자유롭게 설정할 수 있습니다. 각 설정값에는 간단한 설명이 붙어 있으니, 파일 전체를 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php` 설정 파일의 `use` 옵션값으로 절대 사용하지 마세요.

<a name="environments"></a>
#### 환경(environments)

설치 후 가장 먼저 익혀야 할 주요 Horizon 설정값은 `environments` 옵션입니다. 이 옵션은 애플리케이션의 다양한 환경에서 어떤 워커 프로세스 옵션을 사용할지 지정하는 배열입니다. 기본적으로 `production`과 `local` 환경이 포함되어 있으며, 필요에 따라 원하는 만큼 환경을 추가할 수 있습니다:

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

와일드카드 환경(`*`)을 정의해, 어떤 다른 환경과도 일치하지 않을 때 사용하도록 할 수도 있습니다:

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

Horizon을 시작하면, 애플리케이션이 동작 중인 환경에 맞는 워커 프로세스 설정이 적용됩니다. 이 환경 값은 보통 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment)에 의해 결정됩니다. 예를 들어, 기본 `local` 환경은 워커 프로세스를 3개로 자동 시작하고, 각 큐에 할당된 워커 수를 자동으로 맞춥니다. 반면, 기본 `production` 환경은 최대 10개의 워커를 실행하고, 큐별로 할당할 워커 수도 자동 조절됩니다.

> [!WARNING]
> Horizon을 실행할 모든 [환경](/docs/12.x/configuration#environment-configuration)에 대해 `horizon` 설정 파일의 `environments` 항목에 반드시 엔트리가 포함되어야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisors)

Horizon 기본 설정 파일을 살펴보면, 각 환경에 하나 이상 "슈퍼바이저"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 이름이 지정되어 있지만, 원하는 대로 이름을 정할 수 있습니다. 슈퍼바이저는 워커 프로세스 그룹을 "감독"하는 역할을 하며, 여러 큐에 적절히 워커를 분산시킵니다.

환경마다 별도의 슈퍼바이저를 여러 개 추가할 수도 있습니다. 예를 들어, 특정 큐만 따로 관리하거나, 워커 수 또는 분산 전략을 달리하고 싶다면 새로운 슈퍼바이저를 정의하면 됩니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는, 설정 파일의 슈퍼바이저에 `force` 옵션을 `true`로 명시하지 않는 한 Horizon이 큐에 쌓인 작업을 처리하지 않습니다:

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

Horizon 설정 파일에서 `defaults` 항목을 찾을 수 있습니다. 이 값은 [슈퍼바이저](#supervisors)의 기본 설정을 지정하며, 각 환경의 슈퍼바이저 설정에 병합되어 코드 중복을 최소화할 수 있습니다.

<a name="balancing-strategies"></a>
### 부하 분산 전략

라라벨의 기본 큐 시스템과 달리, Horizon에서는 세 가지 분산 전략(`simple`, `auto`, `false`) 중에서 선택할 수 있습니다. `simple` 전략은 들어오는 작업을 워커들에게 균등하게 배분합니다:

```
'balance' => 'simple',
```

기본값인 `auto` 전략은, 큐의 현재 작업량에 따라 큐별 워커 수를 자동으로 조정합니다. 예를 들어 `notifications` 큐에 1,000개의 대기중인 작업이 있고, `render` 큐가 비어 있다면, Horizon은 더 많은 워커를 `notifications` 큐에 할당해 그 큐가 먼저 소진되도록 합니다.

`auto` 전략을 사용할 때는, `minProcesses`와 `maxProcesses`로 큐별 최소 워커 수와 Horizon 전체에서 최대 워커 수를 제한할 수 있습니다:

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

`autoScalingStrategy` 옵션은 Horizon이 워커를 얼마나 할당할지 결정하는 기준입니다. `time` 값이면 남은 큐 처리 시간으로, `size` 값이면 큐의 작업 개수로 판단합니다.

`balanceMaxShift`와 `balanceCooldown` 값은 Horizon이 워커 수를 얼마나 빠르게 조정할 것인지 결정합니다. 위 예시라면, 3초마다 한 개의 워커 프로세스만 새로 만들어지거나 삭제됩니다. 애플리케이션 필요에 맞게 값을 조정하세요.

`balance` 옵션을 `false`로 지정하면, 라라벨의 기본 큐 처리 방식처럼 설정에 나열된 순서대로 처리합니다.

<a name="dashboard-authorization"></a>
### 대시보드 접근 권한

Horizon 대시보드에는 `/horizon` 경로로 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 접근이 가능하지만, `app/Providers/HorizonServiceProvider.php` 파일의 [인가 게이트(gate)](/docs/12.x/authorization#gates) 정의를 수정해, **비-로컬** 환경에서도 접근 대상자를 제한할 수 있습니다:

```php
/**
 * Register the Horizon gate.
 *
 * This gate determines who can access Horizon in non-local environments.
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

라라벨은 위의 게이트 클로저에 인증된 사용자 정보를 자동으로 주입해줍니다. 만약 IP 제한 등 다른 방식으로 Horizon 접근을 제어한다면, 사용자가 굳이 "로그인" 할 필요가 없습니다. 이 경우, 위 클로저의 시그니처를 `function (User $user = null)`로 변경해 인증이 필수가 아니라는 점을 라라벨에게 알려야 합니다.

<a name="silenced-jobs"></a>
### 제외된 작업(Silenced Jobs)

필요에 따라, 애플리케이션이나 외부 패키지에서 발생하는 일부 작업(Job)을 대시보드의 "완료된 작업" 리스트에서 표시하지 않고 제외하고 싶을 수 있습니다. 이에 해당하는 작업 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가하면 됩니다:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는, 해당 작업 클래스에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, `silenced` 배열에 별도로 추가하지 않아도 자동으로 제외됩니다:

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

Horizon의 새로운 주요 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="running-horizon"></a>
## Horizon 실행

애플리케이션의 `config/horizon.php` 설정 파일에서 슈퍼바이저와 워커 구성을 마쳤다면, `horizon` 아티즌 명령어로 Horizon을 실행할 수 있습니다. 이 명령어 하나만으로 현재 환경에 맞는 모든 워커 프로세스가 작동합니다:

```shell
php artisan horizon
```

작업 처리를 일시 중단하거나 다시 시작하려면, `horizon:pause` 및 `horizon:continue` 아티즌 명령어를 사용하세요:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 [슈퍼바이저](#supervisors)만 일시 중단/재개하려면, 각각 `horizon:pause-supervisor` 또는 `horizon:continue-supervisor` 명령어를 사용합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스의 상태는 `horizon:status` 명령어로 확인할 수 있습니다:

```shell
php artisan horizon:status
```

특정 [슈퍼바이저](#supervisors)의 상태를 확인하려면, 다음과 같이 입력합니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료하려면 `horizon:terminate` 명령어를 사용하세요. 현재 진행중인 작업은 마치고 나서 종료하게 됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

실제 서버에 Horizon을 배포할 준비가 되었다면, `php artisan horizon` 명령을 실행 중인지 상시 모니터링하고, 종료되었을 때 자동 재시작 해줄 프로세스 모니터 도구를 설정해야 합니다. 아래에서 프로세스 모니터 설치 및 설정법을 다루겠습니다.

서버에 새로운 배포를 진행할 때에는, 프로세스 모니터가 코드를 반영하도록 Horizon 프로세스를 명시적으로 종료시켜 주세요. 그러면 자동으로 재시작됩니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제용 프로세스 모니터링 도구로, `horizon` 프로세스가 멈췄을 때 자동으로 재시작해줍니다. Ubuntu 기준으로 아래 명령어로 설치할 수 있습니다. (다른 OS에서는 해당 OS용 패키지 관리자를 이용하세요.)

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 복잡하게 느껴진다면, 백그라운드 프로세스 관리를 대신 해주는 [Laravel Cloud](https://cloud.laravel.com) 사용도 고려할 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

보통 Supervisor 설정 파일은 서버의 `/etc/supervisor/conf.d` 디렉터리에 저장합니다. 이 디렉터리 안에 원하는 만큼 설정 파일을 생성해, 어떤 프로세스를 어떻게 모니터링할지 지정할 수 있습니다. 예를 들어, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 구동 및 감시하려면 다음과 같이 설정합니다:

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

설정 시, `stopwaitsecs` 값이 가장 오래 걸리는 작업의 소요 시간(초)보다 충분히 길어야 합니다. 그렇지 않으면, Supervisor가 작업을 끝나기 전에 강제로 중단시킬 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기준입니다. 서버 OS에 따라 Supervisor 설정 파일의 위치나 확장자가 달라질 수 있으니, 서버 문서를 꼭 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 만들었다면, 아래 명령어로 Supervisor 설정을 갱신하고 감시 중인 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor에 대한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon에서는 작업(Job)에 "태그"를 부여할 수 있습니다. 이 기능은 메일 전송, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등에 모두 적용됩니다. 실제로 Eloquent 모델이 연결된 작업의 경우, Horizon이 자동으로 관련 태그를 지능적으로 덧붙여줍니다. 예를 들어 아래와 같은 작업을 살펴보세요:

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

이 작업이 `id`가 1인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 자동으로 `App\Models\Video:1`이라는 태그가 추가됩니다. Horizon은 작업 내부의 속성 중에서 Eloquent 모델을 찾아내고, 그 모델의 클래스명과 기본키로 태그를 자동 생성합니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업에 태그 직접 지정하기

큐에 넣는 작업 클래스에서 태그를 직접 정의하려면, 해당 클래스에 `tags` 메서드를 추가하면 됩니다:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 부여할 태그 목록을 반환합니다.
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
#### 이벤트 리스너에 태그 직접 지정하기

큐에 등록된 이벤트 리스너의 경우, Horizon이 태그를 가져갈 때 이벤트 인스턴스를 `tags` 메서드의 인자로 자동 전달합니다. 따라서 이벤트 데이터를 바탕으로 태그를 자유롭게 생성할 수 있습니다:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 부여할 태그 목록을 반환합니다.
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
> Horizon에서 Slack이나 SMS 알림을 활용하려면, 반드시 [해당 알림 채널의 사전 조건](/docs/12.x/notifications)을 먼저 확인하세요.

큐 중 하나에 긴 대기열이 생겼을 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 활용하면 됩니다. 보통 애플리케이션의 `App\Providers\HorizonServiceProvider` 클래스의 `boot` 메서드에서 호출하세요:

```php
/**
 * Bootstrap any application services.
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

"긴 대기"로 간주할 시간(초)이 얼마인지, 애플리케이션의 `config/horizon.php` 파일에서 설정할 수 있습니다. 이 파일의 `waits` 옵션에서 연결 및 큐 조합별로 임계값을 지정하면 됩니다. 지정하지 않은 조합은 기본적으로 60초로 간주됩니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭

Horizon에는 작업 및 큐의 대기 시간, 처리량 등을 확인할 수 있는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드 데이터를 모으려면, 애플리케이션의 `routes/console.php` 파일에서 `snapshot` 아티즌 명령어가 5분마다 실행되도록 예약하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

메트릭 데이터를 모두 삭제하려면, 다음 명령어를 실행하세요:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용할 수 있습니다. 이 명령어는 삭제하고자 하는 실패 작업의 ID 또는 UUID를 인자로 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패 작업을 한 번에 삭제하려면, `--all` 옵션을 사용하세요:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 쌓인 모든 작업을 삭제하려면, `horizon:clear` 아티즌 명령어를 실행하면 됩니다:

```shell
php artisan horizon:clear
```

특정 큐에 쌓인 작업만 삭제하려면, `queue` 옵션을 지정하세요:

```shell
php artisan horizon:clear --queue=emails
```
