# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [작업 최대 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 재시도 대기시간(Backoff)](#job-backoff)
    - [무음 처리된 작업](#silenced-jobs)
- [부하 분산 전략](#balancing-strategies)
    - [자동 부하 분산](#auto-balancing)
    - [단순 부하 분산](#simple-balancing)
    - [부하 분산 없음](#no-balancing)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 제거](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> Laravel Horizon을 본격적으로 사용하기 전에 Laravel의 기본 [큐 서비스](/docs/12.x/queues)에 대해 먼저 숙지하시기 바랍니다. Horizon은 Laravel의 큐 기능에 다양한 추가 기능을 제공하므로, 기본 큐 기능을 익히지 않으면 일부 개념이 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis 큐](/docs/12.x/queues)에 대한 아름다운 대시보드와 코드 중심의 설정 기능을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패 등 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용할 경우, 모든 큐 워커(Worker)의 설정이 하나의 간단한 구성 파일에 저장됩니다. 워커 설정을 버전 관리 파일에 정의함으로써, 애플리케이션을 배포할 때 큐 워커를 손쉽게 확장하거나 변경할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Laravel Horizon을 사용하려면 큐 드라이버로 반드시 [Redis](https://redis.io)를 사용해야 합니다. 따라서 `config/queue.php` 파일에서 큐 연결 방식이 반드시 `redis`로 설정되어 있는지 확인해야 합니다.

Composer 패키지 관리자를 사용하여 프로젝트에 Horizon을 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어를 실행하여 Horizon의 에셋을 퍼블리시합니다.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 구성 (Configuration)

에셋을 퍼블리시 한 후에는, 메인 설정 파일이 `config/horizon.php`에 생성됩니다. 이 파일에서 애플리케이션의 큐 워커 옵션을 설정할 수 있습니다. 각 설정 항목에는 역할에 대한 설명이 포함되어 있으므로 이 파일을 꼼꼼히 살펴보는 것이 좋습니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결명은 예약되어 있으니, `database.php` 설정 파일의 다른 Redis 연결이나 `horizon.php`의 `use` 옵션 등 다른 곳에서 사용하지 않도록 해야 합니다.

<a name="environments"></a>
#### 환경별 설정

설치가 끝나면, 가장 먼저 익혀야 할 주요 Horizon 설정 항목은 `environments` 설정 옵션입니다. 이 옵션은 애플리케이션이 실행되는 여러 환경별로 설정할 수 있으며, 각 환경별 워커 프로세스 옵션을 정의합니다. 기본적으로 `production`과 `local` 환경 항목이 있습니다. 필요에 따라 환경을 추가할 수도 있습니다.

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

별도의 환경이 없을 경우 사용할 와일드카드 환경(`*`)도 정의할 수 있습니다:

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

Horizon을 시작하면, 현재 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 설정을 사용합니다. 일반적으로 이 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment) 값에 따라 결정됩니다. 예를 들어, 기본적으로 `local` 환경에서는 3개의 워커 프로세스를 시작하고, 각 큐에 할당하는 워커 수를 자동으로 조절하도록 설정되어 있습니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 생성하며, 각 큐에 할당하는 워커 수도 자동으로 조절합니다.

> [!WARNING]
> Horizon을 실행하려는 모든 [환경](/docs/12.x/configuration#environment-configuration)에 대해 반드시 `environments` 설정에 엔트리가 포함되어 있는지 확인해야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저 (Supervisors)

Horizon의 기본 설정 파일에서 볼 수 있듯, 각 환경에는 하나 이상의 "슈퍼바이저(Supervisor)"를 지정할 수 있습니다. 기본적으로 이 슈퍼바이저는 `supervisor-1`로 정의되어 있지만, 원하는 이름으로 자유롭게 지정할 수 있습니다. 각 슈퍼바이저는 지정한 워커 그룹을 "감독"하며, 큐에 워커 프로세스를 적절히 분배하는 역할을 합니다.

특정 환경에서 실행할 워커 그룹을 새로 정의하고 싶다면, 슈퍼바이저를 추가로 지정할 수 있습니다. 예를 들어, 큐 별로 다른 부하 분산 전략이나 워커 프로세스 개수를 달리 정하고 싶을 때 유용합니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드 (Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)에 들어가면, Horizon은 슈퍼바이저의 `force` 옵션이 `true`로 설정된 경우를 제외하고 큐 작업을 처리하지 않습니다.

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

Horizon의 기본 설정 파일에는 `defaults` 설정 항목이 있습니다. 이 항목은 [슈퍼바이저](#supervisors)에 대한 기본값을 지정합니다. 슈퍼바이저의 기본 설정 값은 개별 환경 설정 값에 병합되어 반복적인 설정을 줄일 수 있습니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가 (Dashboard Authorization)

Horizon 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로 이 대시보드는 `local` 환경에서만 접근 가능합니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일의 [인가 게이트(gate)](/docs/12.x/authorization#gates) 정의를 통해 **비-local** 환경에서의 접근 제한을 제어할 수 있습니다. 필요하다면 아래와 같이 이 게이트를 수정하여, Horizon 대시보드 접근 대상을 제한할 수 있습니다.

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

Laravel은 게이트 클로저에 인증된 사용자를 자동 주입합니다. 만약 IP 제한 등 다른 방법으로 Horizon 보안을 제공한다면, 사용자가 별도로 로그인할 필요가 없을 수 있습니다. 이 경우, 위 클로저 시그니처를 `function (User $user = null)`로 수정하여 Laravel이 인증을 필수로 요구하지 않도록 할 수 있습니다.

<a name="max-job-attempts"></a>
### 작업 최대 시도 횟수 (Max Job Attempts)

> [!NOTE]
> 이 옵션을 조정하기 전에 Laravel의 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 '시도 횟수' 개념에 대해 충분히 이해해야 합니다.

슈퍼바이저의 설정에서 작업 당 최대 시도 횟수를 지정할 수 있습니다.

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
> 이 옵션은 Artisan 명령어에서 사용하는 `--tries` 옵션과 유사합니다.

`WithoutOverlapping`, `RateLimited` 같은 미들웨어를 사용할 때는 시도 횟수가 추가로 소모될 수 있으므로, `tries` 옵션을 supervisor 레벨에서 또는 작업 클래스의 `$tries` 속성을 통해 적절하게 조정해야 합니다.

`tries` 옵션을 지정하지 않으면 Horizon은 기본적으로 1회만 시도합니다. 단, 작업 클래스에 `$tries`가 명시되어 있으면 이 값이 우선합니다.

`tries` 또는 `$tries`를 0으로 설정하면 시도 횟수 제한이 해제됩니다. 시도 횟수를 알 수 없는 경우에 유용하지만, 무한 실패를 방지하기 위해 필요한 경우 작업 클래스의 `$maxExceptions` 속성으로 예외 발생 횟수 제한을 둘 수 있습니다.

<a name="job-timeout"></a>
### 작업 타임아웃 (Job Timeout)

마찬가지로 supervisor 레벨에서 `timeout` 값을 지정할 수 있습니다. 이 값은 워커 프로세스가 단일 작업을 실행할 수 있는 최대 초(sec) 단위 시간을 의미하며, 시간이 초과되면 강제로 종료됩니다. 종료된 작업은 큐 설정에 따라 재시도되거나 실패 처리됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...¨
            'timeout' => 60,
        ],
    ],
],
```

> [!WARNING]
> `auto` 부하 분산 전략을 사용할 때에는, Horizon이 스케일 다운 과정에서 지정된 타임아웃이 지난 워커를 "중단(hanging)" 된 것으로 간주해 강제 종료(kill)합니다. 항상 Horizon 타임아웃 값이 개별 작업의 타임아웃보다 크게 설정되어야 하며, `config/queue.php`의 `retry_after` 값보다 Horizon 타임아웃 값이 몇 초 더 작아야 합니다. 그렇지 않으면 작업이 중복 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 재시도 대기시간(Backoff) (Job Backoff)

supervisor 레벨에서 `backoff` 값을 지정해, 처리 중 미처리 예외가 발생할 경우 작업을 재시도하기까지 Horizon이 대기할 시간을 지정할 수 있습니다.

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

`backoff` 값에 배열을 사용하면 "지수적(Exponential)" 대기시간을 설정할 수 있습니다. 예를 들어, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째와 이후 재시도는 10초 간 대기하게 할 수 있습니다.

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
### 무음 처리된 작업 (Silenced Jobs)

애플리케이션 또는 외부 패키지에서 실행되는 특정 작업의 상태를 "완료된 작업" 목록에서 보고 싶지 않을 수 있습니다. 이럴 때, 해당 작업을 무음 처리할 수 있습니다. 우선 무음 처리할 작업의 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가합니다.

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

개별 작업 클래스 외에도, [태그](#tags)를 기준으로 여러 작업을 무음 처리할 수도 있습니다. 태그가 같은 여러 작업을 숨기고 싶을 때 유용합니다.

```php
'silenced_tags' => [
    'notifications'
],
```

또는 무음 처리할 작업 클래스에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, 설정 배열에 없어도 자동으로 무음 처리됩니다.

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 부하 분산 전략 (Balancing Strategies)

각 슈퍼바이저는 하나 이상의 큐를 처리할 수 있습니다. Laravel의 기본 큐 시스템과 달리 Horizon은 세 가지 워커 부하 분산 전략(`auto`, `simple`, `false`) 중 하나를 선택할 수 있습니다.

<a name="auto-balancing"></a>
### 자동 부하 분산 (Auto Balancing)

`auto` 전략은 (기본값) 현재 각 큐의 작업량에 따라 큐 별 워커 프로세스 수를 자동으로 조절합니다. 예를 들어 `notifications` 큐에 1,000개의 대기 작업이 있고 `default` 큐에 작업이 없다면, Horizon은 더 많은 워커를 `notifications` 큐에 할당해 작업이 모두 처리될 때까지 집중합니다.

`auto` 전략 선택 시, `minProcesses`, `maxProcesses` 등 추가 옵션도 지정할 수 있습니다.

<div class="content-list" markdown="1">

- `minProcesses`: 큐 별 최소 워커 수 (1 이상)
- `maxProcesses`: 전체 큐에 허용되는 총 워커 프로세스의 최대값으로, 일반적으로 큐 수에 `minProcesses` 값 곱한 것보다 크게 설정해야 합니다. 워커 생성을 막으려면 0으로 설정할 수 있습니다.

</div>

예를 들어, 각 큐에 최소 1개의 프로세스를 유지하고, 전체 프로세스 수는 10까지 스케일 업하도록 설정할 수 있습니다.

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

`autoScalingStrategy` 옵션은 Horizon이 큐에 워커를 어떻게 더 할당할지 결정합니다. 두 가지 전략이 있습니다.

<div class="content-list" markdown="1">

- `time`: 큐가 모두 비워지기까지 추정 소요 시간을 기준으로 워커 할당
- `size`: 큐에 있는 전체 작업 개수 기준으로 워커 할당

</div>

`balanceMaxShift`, `balanceCooldown` 값은 워커 수 증감 속도를 제어합니다. 위 예시의 경우 3초마다 신규 프로세스를 최대 1개까지 추가하거나 제거합니다. 프로젝트 상황에 맞춰 이 값들을 조정할 수 있습니다.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위 & 자동 부하 분산

`auto` 전략은 큐 간의 엄격한 우선순위를 보장하지 않습니다. 슈퍼바이저 설정에서 큐의 순서는 워커 배정에 영향을 주지 않으며, 지정한 `autoScalingStrategy`에 따라 동적으로 워커가 할당됩니다.

즉, 아래 설정에서도 `high` 큐는 `default` 큐보다 우선시 처리되지 않습니다.

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

큐 간 상대적 우선순위를 엄격히 적용해야 한다면, 여러 슈퍼바이저를 정의하고 리소스를 명시적으로 분배하세요.

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

위 예시에서는 `default` 큐는 10개까지 프로세스 확장 가능하고, `images` 큐는 1개로 제한되어 있습니다. 이 방식으로 큐 별 독립적인 확장 전략을 만들 수 있습니다.

> [!NOTE]
> 리소스를 많이 소모하는 작업은 별도의 큐로 분리해 `maxProcesses` 값을 제한하는 것이 좋습니다. 그렇지 않으면 해당 작업들이 CPU나 시스템 자원을 지나치게 점유할 수 있습니다.

<a name="simple-balancing"></a>
### 단순 부하 분산 (Simple Balancing)

`simple` 전략은 지정된 큐에 워커 프로세스 수를 균등하게 배분합니다. 이 전략에서는 워커 수가 자동으로 늘어나지 않으며, 고정 프로세스 개수만 사용합니다.

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

위 예시에서는 각각의 큐에 5개씩, 총 10개의 프로세스를 나누어 배정합니다.

각 큐 별로 프로세스 수를 세밀히 제어하고 싶으면, 슈퍼바이저를 여러 개 만들어 사용할 수 있습니다.

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

이 경우, `default` 큐에는 10개, `notifications` 큐에는 2개의 워커가 할당됩니다.

<a name="no-balancing"></a>
### 부하 분산 없음 (No Balancing)

`balance` 옵션을 `false`로 하면, Horizon은 큐를 명시한 순서대로 처리합니다. Laravel의 기본 큐와 비슷하지만, 작업이 쌓이면 워커 프로세스를 자동으로 확장하는 기능은 남아 있습니다.

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

위 설정에서는 항상 `default` 큐가 `notifications` 큐보다 우선 처리됩니다. 예를 들어, `default`에 1,000개, `notifications`에 10개의 작업이 있더라도, Horizon은 먼저 `default` 작업을 모두 처리한 후에야 `notifications` 큐 작업을 처리합니다.

워커 프로세스의 최소∙최대 개수는 `minProcesses`, `maxProcesses` 옵션으로 제어할 수 있습니다.

<div class="content-list" markdown="1">

- `minProcesses`: 전체 워커의 최소 개수 (1 이상)
- `maxProcesses`: 전체 워커의 최대 개수

</div>

<a name="upgrading-horizon"></a>
## Horizon 업그레이드 (Upgrading Horizon)

Horizon의 새로운 주요 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

<a name="running-horizon"></a>
## Horizon 실행 (Running Horizon)

`config/horizon.php`에서 슈퍼바이저와 워커를 설정했다면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 명령어 하나로 현재 환경에 맞게 모든 워커 프로세스가 시작됩니다.

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지했다가 재개하려면 각각 `horizon:pause`, `horizon:continue` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)만 선택적으로 일시 중지∙재개할 수도 있습니다.

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스의 상태는 `horizon:status` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan horizon:status
```

특정 [슈퍼바이저](#supervisors)의 상태는 아래처럼 확인합니다.

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로(Graceful) 종료하려면 `horizon:terminate` Artisan 명령어를 사용합니다. 현재 처리 중인 작업은 모두 완료된 후 Horizon이 완전히 정지됩니다.

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포 (Deploying Horizon)

실서버에 Horizon을 배포할 때는, `php artisan horizon` 명령어가 비정상 종료되었을 경우를 대비해, 프로세스 모니터를 사용해 자동 재시작하도록 설정해야 합니다. 아래에서 프로세스 모니터 설치 방법을 안내합니다.

배포 과정에서는, 코드 변경사항이 반영될 수 있도록 Horizon 프로세스를 종료하여, 프로세스 모니터가 새로 프로세스를 시작하게 해야 합니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제에서 동작하는 프로세스 모니터링 도구입니다. 만약 `horizon` 프로세스가 예기치 않게 종료되면 Supervisor가 자동으로 재시작해줍니다. Ubuntu에서는 다음 명령어로 Supervisor를 설치할 수 있습니다. Ubuntu가 아닌 경우, 해당 OS의 패키지 관리자를 통해 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 부담된다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 서비스를 이용하여 백그라운드 프로세스 관리를 맡길 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 구성

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장합니다. 이곳에 여러 설정 파일을 만들어 각각의 프로세스 모니터링을 지시할 수 있습니다. 예시로, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작 및 모니터링하는 방법입니다.

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

Supervisor 설정 시, `stopwaitsecs` 값이 가장 오래 실행되는 작업에 소요되는 시간(초)보다 커야 합니다. 그렇지 않으면 Supervisor가 작업 처리가 완료되기 전에 강제로 프로세스를 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 서버에는 유효하지만, Supervisor 구성 파일의 위치나 확장자는 운영체제에 따라 다를 수 있습니다. 자세한 내용은 해당 서버 OS의 공식 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 만든 후, 아래 명령어들로 Supervisor 설정을 갱신하고 관련 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행과 관련한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그 (Tags)

Horizon은 작업(job), 메일 전송 객체, 방송 이벤트, 알림(notification), 큐에 등록된 이벤트 리스너 등에 "태그"를 붙일 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델을 활용해 대부분의 작업을 자동으로 태그 처리합니다. 예를 들어, 아래와 같은 작업을 살펴보세요.

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

이 작업을 `id`가 1인 `App\Models\Video` 인스턴스와 함께 큐에 등록하면, 자동으로 `App\Models\Video:1`이라는 태그가 붙습니다. 이는 Horizon이 작업의 속성 중 Eloquent 모델을 탐색해, 모델의 클래스명과 기본키(primary key) 값을 조합해 태그로 생성하기 때문입니다.

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업의 태그 수동 지정

큐에 등록할 객체에 태그를 직접 지정하고 싶다면, 클래스에 `tags` 메서드를 추가합니다.

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
#### 이벤트 리스너 태그 수동 지정

큐에 등록된 이벤트 리스너의 경우, Horizon은 이벤트 인스턴스를 `tags` 메서드에 자동으로 넘겨주므로 이벤트 데이터를 태그에 활용할 수 있습니다.

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
> Horizon에서 Slack, SMS 알림을 설정할 경우, 반드시 [해당 알림 채널의 사전 조건](/docs/12.x/notifications)을 확인해 주세요.

큐 대기 시간이 비정상적으로 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출합니다.

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
#### 대기시간 기준 임계값 설정

각 큐별 얼마나 길게 기다려야 "오래 대기(long wait)" 상태로 간주할지, `config/horizon.php` 파일의 `waits` 설정을 통해 지정할 수 있습니다. 이 옵션은 연결/큐 조합별로 긴 대기 임계값(초 단위)을 지정하며, 별도로 지정하지 않은 경우 기본값은 60초입니다.

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

임계값을 0으로 지정하면 해당 큐에 대한 "긴 대기" 알림이 꺼집니다.

<a name="metrics"></a>
## 메트릭 (Metrics)

Horizon은 작업 별, 큐별 대기시간 및 처리량을 제공하는 메트릭 대시보드를 내장하고 있습니다. 해당 대시보드를 활성화하기 위해서는, 애플리케이션의 `routes/console.php` 파일에서 Horizon의 `snapshot` Artisan 명령어가 5분마다 실행되도록 스케줄을 등록해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

메트릭 데이터를 모두 삭제하고 싶다면, `horizon:clear-metrics` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제 (Deleting Failed Jobs)

실패한 작업을 개별적으로 삭제하려면 `horizon:forget` 명령어를 사용하세요. 이 명령어는 실패한 작업의 ID 또는 UUID를 유일한 인수로 받습니다.

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 한 번에 삭제하려면 `--all` 옵션을 사용할 수 있습니다.

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 제거 (Clearing Jobs From Queues)

애플리케이션의 기본 큐에서 모든 작업을 삭제하고 싶다면, `horizon:clear` Artisan 명령어를 사용하면 됩니다.

```shell
php artisan horizon:clear
```

특정 큐에서만 작업을 삭제하려면 `queue` 옵션을 추가하세요.

```shell
php artisan horizon:clear --queue=emails
```
