# 라라벨 Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 백오프](#job-backoff)
    - [무시하는 작업 설정](#silenced-jobs)
- [밸런싱 전략](#balancing-strategies)
    - [자동 밸런싱](#auto-balancing)
    - [간단 밸런싱](#simple-balancing)
    - [밸런싱 없음](#no-balancing)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> Laravel Horizon을 사용하기 전에, 라라벨의 기본 [큐 서비스](/docs/12.x/queues)에 대해 충분히 익숙해지셔야 합니다. Horizon은 라라벨의 큐에 추가 기능을 제공하므로, 기본 큐 기능을 잘 모르실 경우 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 라라벨로 개발된 [Redis 큐](/docs/12.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정 환경을 제공합니다. Horizon을 통해 작업 처리량, 실행 시간, 실패한 작업 등 큐 시스템의 주요 지표를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 큐 워커(worker) 설정이 하나의 간단한 설정 파일에 저장됩니다. 이렇게 애플리케이션의 워커 구성을 버전 관리 파일로 정의하면, 배포 시 애플리케이션의 큐 워커를 손쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Laravel Horizon을 사용하려면 [Redis](https://redis.io) 기반 큐 연결이 필요합니다. 따라서 `config/queue.php` 설정 파일에서 큐 연결이 반드시 `redis`로 지정되어야 합니다.

Composer 패키지 관리자를 이용해 프로젝트에 Horizon을 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

설치 후에는 `horizon:install` Artisan 명령어로 Horizon의 에셋을 퍼블리시하세요.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정 (Configuration)

에셋을 퍼블리시하고 나면, 주요 설정 파일이 `config/horizon.php`에 생성됩니다. 이 설정 파일을 통해 애플리케이션의 큐 워커 옵션을 구성할 수 있습니다. 각 옵션 아래에는 용도에 대한 설명이 있으니 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 Redis 연결명을 사용합니다. 이 연결명은 예약되어 있으므로 `database.php` 설정 파일의 다른 Redis 연결명이나 `horizon.php` 설정 파일의 `use` 옵션 값으로 할당하지 마세요.

<a name="environments"></a>
#### 환경별 설정

설치 후 가장 먼저 익숙해져야 할 Horizon의 주요 설정은 `environments` 옵션입니다. 이 옵션은 애플리케이션이 실행될 각 환경에 대한 배열로, 각 환경별 워커 프로세스 옵션을 정의합니다. 기본적으로 `production`과 `local` 환경 항목이 있으며, 필요한 경우 더 추가할 수 있습니다.

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

또한, 일치하는 환경을 찾지 못했을 경우 사용할 와일드카드 환경(`*`)도 정의할 수 있습니다.

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

Horizon을 실행할 때, 현재 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 설정을 사용합니다. 일반적으로 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment)의 값에 따라 결정됩니다. 예를 들어, 기본 제공 `local` 환경에서는 워커 프로세스 3개를 기동하고, 각 큐에 할당된 워커 수를 자동으로 조절합니다. `production` 환경은 최대 10개의 워커 프로세스를 시작하여 각 큐에 자동으로 할당합니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments` 항목에는 Horizon을 실행할 모든 [환경](/docs/12.x/configuration#environment-configuration)에 대한 설정이 반드시 포함되어야 합니다.

<a name="supervisors"></a>
#### Supervisor 설정

Horizon의 기본 설정 파일을 보면, 각 환경 아래에 한 개 이상 "슈퍼바이저(supervisor)"를 가질 수 있습니다. 기본적으로 `supervisor-1`이라는 이름이 부여되어 있으나, 자유롭게 원하는 이름을 지정할 수 있습니다. 슈퍼바이저는 특정 워커 프로세스 그룹을 "감독"하며, 큐 별 워커 분배와 관리를 담당합니다.

한 환경에 추가 슈퍼바이저를 더 추가할 수 있습니다. 예를 들어 큐마다 다른 밸런싱 전략이나 워커 프로세스 수를 지정하고 싶을 때 사용할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)에 들어가 있을 때, Horizon에서는 기본적으로 큐에 쌓인 작업이 실행되지 않습니다. 만약 유지보수 모드 중에도 작업 처리가 필요하다면 Horizon 설정 파일에서 supervisor의 `force` 옵션을 `true`로 지정하세요.

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

Horizon 기본 설정 파일에서 `defaults` 옵션을 확인할 수 있습니다. 이 옵션은 각 [supervisor](#supervisors)별 기본값을 지정하며, 각 환경마다 supervisor 설정에 병합되어 중복된 설정 작업을 줄일 수 있습니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가 (Dashboard Authorization)

Horizon 대시보드는 `/horizon` 라우트를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근이 허용됩니다. 하지만, `app/Providers/HorizonServiceProvider.php` 파일에는 [인가 게이트(authorization gate)](/docs/12.x/authorization#gates)가 정의되어 있습니다. 이 게이트를 수정하여 **로컬 환경이 아닌 경우** Horizon 접근을 제한할 수 있습니다.

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
#### 대체 인증 전략

라라벨은 게이트 클로저에 인증된 사용자를 자동으로 주입합니다. 만약 IP 제한 등 별도의 방식으로 Horizon 대시보드의 보안을 적용하는 경우, Horizon 접속 사용자가 "로그인"하지 않아도 될 수 있습니다. 이런 경우, 위 클로저 시그니처를 `function (User $user = null)`처럼 변경하여 인증 요구를 없앨 수 있습니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수 (Max Job Attempts)

> [!NOTE]
> 이 옵션을 다루기 전에, 라라벨의 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 'attempts' 개념을 먼저 이해하시기 바랍니다.

supervisor 설정에서 각 작업에 대한 최대 시도 횟수를 지정할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'tries' => 10,
        ],
    ],
],
```

> [!NOTE]
> 이 옵션은 Artisan 큐 처리 명령어의 `--tries` 옵션과 유사합니다.

`WithoutOverlapping` 또는 `RateLimited` 미들웨어와 같이 시도 횟수를 소모하는 미들웨어를 사용하는 경우, `tries` 옵션의 조정이 중요합니다. supervisor 레벨의 설정 값이나, 작업 클래스에 `$tries` 속성을 정의하여 조절할 수 있습니다.

`tries` 옵션을 설정하지 않으면 기본값은 1회 시도이지만, 작업 클래스에 `$tries` 속성이 있으면 이 값이 설정값보다 우선 적용됩니다.

`tries` 또는 `$tries`를 0으로 설정하면 시도 횟수 제한 없이 무한히 재시도됩니다. 시도 횟수를 예측할 수 없는 경우에는 이 방식을 사용합니다. 대신 무한 반복 실패를 방지하기 위해 작업 클래스의 `$maxExceptions` 속성을 통한 예외 횟수 제한 설정이 권장됩니다.

<a name="job-timeout"></a>
### 작업 타임아웃 (Job Timeout)

마찬가지로 supervisor 레벨에서 `timeout` 값을 설정하여, 워커 프로세스가 각 작업을 최대 몇 초 동안 실행할 수 있는지 제어할 수 있습니다. 제한 시간을 넘기면 작업은 강제로 종료되어, 큐 설정에 따라 재시도되거나 실패로 처리됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'timeout' => 60,
        ],
    ],
],
```

> [!WARNING]
> `timeout` 값은 반드시 `config/queue.php` 파일의 `retry_after` 값보다 몇 초 더 짧게 설정해야 합니다. 그렇지 않으면 작업이 두 번 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 백오프 (Job Backoff)

supervisor 레벨에서 `backoff` 값을 설정하면, 처리 실패 시 작업을 재시도하기 전 몇 초 쉬었다가 시도할지 지정할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => 10,
        ],
    ],
],
```

`backoff` 값으로 배열을 지정하면 "지수 백오프"도 설정할 수 있습니다. 아래 예에서는 첫 번째 재시도는 1초 후, 두 번째 재시도는 5초 후, 세 번째 및 이후 재시도는 10초 간격으로 진행됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => [1, 5, 10],
        ],
    ],
],
```

<a name="silenced-jobs"></a>
### 무시하는 작업 설정 (Silenced Jobs)

때때로 애플리케이션이나 외부 패키지가 사용하는 특정 작업을 대시보드에서 굳이 보고 싶지 않을 수 있습니다. 이런 작업들이 "완료된 작업" 목록에 표시되지 않게 하려면 `horizon` 설정 파일의 `silenced` 옵션에 클래스명을 명시하여 무시할 수 있습니다.

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

혹은, 무시하고 싶은 작업 클래스에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현할 수도 있습니다. 이 인터페이스를 구현하면, 별도로 `silenced` 배열에 추가하지 않아도 자동으로 무시됩니다.

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 밸런싱 전략 (Balancing Strategies)

각 supervisor는 하나 이상의 큐를 처리할 수 있으며, 라라벨의 기본 큐 시스템과 달리 Horizon에서는 `auto`, `simple`, `false` 세 가지 워커 밸런싱 전략 중 하나를 선택할 수 있습니다.

<a name="auto-balancing"></a>
### 자동 밸런싱 (Auto Balancing)

`auto` 전략(기본값)은 각 큐의 현재 작업량을 기반으로 큐별 워커 프로세스 개수를 자동 조절합니다. 예를 들어 `notifications` 큐에 1000개의 작업이 쌓여 있고, `default` 큐는 비어 있다면 Horizon은 더 많은 워커를 `notifications` 큐에 할당하여 빠르게 처리하게 합니다.

`auto` 전략을 사용할 때는 `minProcesses`(각 큐별 최소 워커수) 및 `maxProcesses`(전체 큐 합산 최대 워커수) 옵션을 지정할 수 있습니다.

<div class="content-list" markdown="1">

- `minProcesses`: 큐마다 최소로 배정할 워커 프로세스 수입니다. 1 이상이어야 합니다.
- `maxProcesses`: 모든 큐에 걸쳐 Horizon이 확장할 수 있는 전체 워커 프로세스의 최대치입니다. 일반적으로 (큐 개수 × `minProcesses`)보다 큰 값을 권장합니다. 0으로 지정하면 프로세스가 생성되지 않습니다.

</div>

예를 들면 아래와 같이 각 큐당 최소 1개, 전체적으로는 최대 10개의 프로세스로 제한할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default', 'notifications'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],
],
```

`autoScalingStrategy`는 Queue에 워커를 더 배정할 때의 기준을 지정합니다.

<div class="content-list" markdown="1">

- `time`: 큐를 비우는 데 걸리는 예상 총시간 기준으로 워커를 할당합니다.
- `size`: 큐의 대기 중인 전체 작업 개수 기준으로 워커를 할당합니다.

</div>

`balanceMaxShift`, `balanceCooldown` 값으로 워커 증가/감소 속도를 조절합니다. 위 예시의 경우, 3초마다 최대 1개씩 프로세스가 생성되거나 제거됩니다. 애플리케이션 환경에 맞게 자유롭게 조정하세요.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위와 자동 밸런싱

`auto` 전략을 사용할 경우, 큐 간에 엄격한 우선순위를 적용하지 않습니다. supervisor 설정에서 큐의 나열 순서는 실제 워커 할당에 영향을 주지 않습니다. 대신 선택한 `autoScalingStrategy`에 따라 동적으로 워커가 배정됩니다.

예를 들어, 아래 구성의 경우, high 큐가 default 큐보다 앞에 나와 있다고 해서 더 높은 우선순위를 갖진 않습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['high', 'default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

진짜 상대적 우선순위를 적용하고 싶다면 supervisor를 여러 개 만들고 각각 특정 큐에 리소스를 고정 배정하면 됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
        'supervisor-2' => [
            // ...
            'queue' => ['images'],
            'minProcesses' => 1,
            'maxProcesses' => 1,
        ],
    ],
],
```

위 예시는 default 큐는 최대 10개, images 큐는 1개 프로세스만 사용하도록 하여, 각 큐의 확장성을 독립적으로 제어할 수 있습니다.

> [!NOTE]
> 연산량이 많은 작업의 경우, 별도의 큐와 제한된 `maxProcesses`로 독립 처리하는 것이 좋습니다. 그렇지 않으면 시스템 전체가 과부하를 겪을 수 있습니다.

<a name="simple-balancing"></a>
### 간단 밸런싱 (Simple Balancing)

`simple` 전략을 지정하면, 워커 프로세스가 지정된 큐에 균등하게 분배됩니다. 자동 확장 없이 고정된 워커 수를 사용합니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => 'simple',
            'processes' => 10,
        ],
    ],
],
```

위 설정에서는 각 큐당 5개씩, 총 10개의 워커 프로세스가 균등 할당됩니다.

각 큐별로 서로 다른 워커 수를 지정하고 싶다면 supervisor를 여러 개 정의하면 됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'balance' => 'simple',
            'processes' => 10,
        ],
        'supervisor-notifications' => [
            // ...
            'queue' => ['notifications'],
            'balance' => 'simple',
            'processes' => 2,
        ],
    ],
],
```

이렇게 하면 default 큐에는 10개, notifications 큐에는 2개의 프로세스가 할당됩니다.

<a name="no-balancing"></a>
### 밸런싱 없음 (No Balancing)

`balance` 옵션을 `false`로 설정하면, Laravel 기본 큐 시스템처럼 큐 배열 순서대로 작업이 처리됩니다. 하지만, 작업이 누적되면 Horizon은 워커 프로세스를 자동으로 확장할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => false,
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

위 설정에서는 default 큐가 비워질 때까지 notifications 큐 작업은 대기하게 됩니다(순차 처리). 예를 들어, default 큐에 1,000개, notifications 큐에 10개 작업이 있다면, default 큐를 모두 처리한 후에야 notifications 큐 작업이 시작됩니다.

`minProcesses`와 `maxProcesses` 옵션으로 총 워커 수를 제어할 수 있습니다.

<div class="content-list" markdown="1">

- `minProcesses`: 전체 최소 워커 프로세스 수(1 이상).
- `maxProcesses`: 전체 최대 워커 프로세스 수.

</div>

<a name="upgrading-horizon"></a>
## Horizon 업그레이드 (Upgrading Horizon)

Horizon을 새 메이저 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

<a name="running-horizon"></a>
## Horizon 실행 (Running Horizon)

`config/horizon.php`에 supervisor와 worker 설정을 완료했다면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령 하나로 현재 환경의 모든 설정 워커 프로세스가 시작됩니다.

```shell
php artisan horizon
```

Horizon 프로세스를 일시 정지(pause) 또는 다시 시작(continue)할 때는 아래 명령어를 사용하세요.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [supervisor](#supervisors)에 대해서만 일시 정지/재개하려면:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon 프로세스의 현재 상태는 `horizon:status` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan horizon:status
```

특정 Horizon [supervisor](#supervisors)의 상태만 확인하려면:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료하고 싶다면, `horizon:terminate` Artisan 명령어를 사용하세요. 현재 실행 중인 작업은 마무리된 후, Horizon이 종료됩니다.

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포 (Deploying Horizon)

Horizon을 실제 서버에 배포할 준비가 되었다면, 프로세스 모니터를 설정하여 `php artisan horizon` 명령어가 예기치 않게 종료될 경우 자동으로 재시작되도록 하세요. 프로세스 모니터 설치 방법은 아래에서 다룹니다.

배포 과정에서, 코드가 변경될 때마다 Horizon 프로세스를 종료하도록 지시해야 하고, 그렇게 하면 프로세스 모니터가 자동 재시작하여 최신 코드를 반영할 수 있습니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스용 프로세스 감시 도구로, Horizon 프로세스가 중단되었을 때 자동으로 재시작시켜줍니다. Ubuntu 기준 설치 명령어는 다음과 같습니다. 다른 배포판을 쓰신다면 해당 OS의 패키지 관리자로 Supervisor를 설치하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정이 부담된다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 서비스를 활용해 백그라운드 프로세스를 관리하는 것도 고려해볼 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 서버의 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 폴더 아래에 여러 개의 설정 파일을 만들 수 있으며, 각 파일은 감시할 프로세스를 정의합니다. 예를 들어 `horizon.conf` 파일로 Horizon 프로세스 감시를 설정할 수 있습니다.

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

Supervisor 설정에선 `stopwaitsecs` 값을 가장 오래 실행되는 작업의 소요 시간보다 크게 지정해야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예시들은 Ubuntu 서버 기준으로 유효하며, 다른 OS에서는 Supervisor 설정 파일의 경로나 확장자가 다를 수 있습니다. 자세한 내용은 서버 운영체제의 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 작성한 후에는 아래 명령어로 Supervisor 설정을 갱신하고, 감시 프로세스를 시작하세요.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 운용에 관한 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon에서는 메일 발송 객체, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 작업에 "태그"를 지정할 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델을 기준으로 자동으로 태그를 지정합니다. 예를 들어, 아래와 같은 작업이 있다고 가정해보겠습니다.

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

이 작업에 `id` 값이 1인 `App\Models\Video` 인스턴스를 전달해 큐에 등록하면, 자동으로 `App\Models\Video:1`이라는 태그가 붙게 됩니다. Horizon은 작업의 프로퍼티에서 Eloquent 모델이 있는지 찾고, 있다면 모델의 클래스명과 기본키를 조합해 자동으로 태그화합니다.

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업에 태그 직접 지정하기

큐에 넣을 객체에 직접 태그를 지정하려면, 클래스에 `tags` 메서드를 정의하면 됩니다.

```php
class RenderVideo implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the job.
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

큐에 등록된 이벤트 리스너의 경우, Horizon이 `tags` 메서드에 이벤트 인스턴스를 자동으로 전달합니다. 따라서 이벤트 데이터 기반으로 태그를 만들 수 있습니다.

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the listener.
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
> Slack 또는 SMS로 Horizon 알림을 보내려면, [해당 채널의 필수 준비사항](/docs/12.x/notifications)을 반드시 확인하세요.

큐의 대기 시간이 길어지면 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용하면 됩니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출할 수 있습니다.

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

몇 초 이상을 "대기 시간 길다"고 판단할지 `config/horizon.php` 파일의 `waits` 옵션에서 세밀하게 설정할 수 있습니다. 이 옵션은 연결/큐별로 대기 시간 임계 기준(초 단위)를 지정합니다. 명시되지 않은 조합은 60초가 기본값입니다.

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭 (Metrics)

Horizon에는 작업 및 큐의 대기 시간, 처리량 등 각종 정보를 시각화한 메트릭 대시보드가 있습니다. 이 대시보드에 데이터를 누적하려면, 앱의 `routes/console.php` 파일에 `horizon:snapshot` Artisan 명령어를 5분마다 실행하도록 예약하세요.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 메트릭 데이터를 삭제하려면 `horizon:clear-metrics` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제 (Deleting Failed Jobs)

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용할 수 있습니다. 이 명령에는 삭제할 실패한 작업의 ID 또는 UUID를 인수로 넘깁니다.

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 삭제하려면, `--all` 옵션을 추가하면 됩니다.

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기 (Clearing Jobs From Queues)

애플리케이션의 기본 큐에서 모든 작업을 삭제하려면, `horizon:clear` Artisan 명령을 사용하세요.

```shell
php artisan horizon:clear
```

특정 큐에 있는 작업만 삭제하려면, `queue` 옵션을 추가할 수 있습니다.

```shell
php artisan horizon:clear --queue=emails
```