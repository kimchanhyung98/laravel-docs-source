# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 Backoff](#job-backoff)
    - [무시한 작업](#silenced-jobs)
- [작업자 균형 전략](#balancing-strategies)
    - [자동 균형](#auto-balancing)
    - [간단한 균형](#simple-balancing)
    - [균형 없음](#no-balancing)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행하기](#running-horizon)
    - [Horizon 배포하기](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [지표](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]
> Laravel Horizon을 자세히 다루기 전에, 먼저 Laravel의 기본 [큐 서비스](/docs/12.x/queues)를 익혀두시기 바랍니다. Horizon은 Laravel 큐 시스템에 여러 고급 기능을 추가하므로, 기본 큐 기능에 익숙하지 않으면 다소 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis 큐](/docs/12.x/queues)를 위한 뛰어난 대시보드와 코드 기반 설정 기능을 제공합니다. Horizon을 사용하면 큐 시스템의 주요 지표(작업 처리량, 실행 시간, 작업 실패 등)를 쉽게 모니터링할 수 있습니다.

Horizon을 사용할 경우, 모든 큐 작업자 설정은 하나의 간단한 설정 파일에 저장됩니다. 애플리케이션의 작업자 설정을 버전 관리가 가능한 파일로 정의하면, 배포 시 작업자 수를 쉽게 조정하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon은 [Redis](https://redis.io)를 큐 백엔드로 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결을 반드시 `redis`로 지정해야 합니다.

Composer 패키지 관리자를 이용해 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

Horizon 설치 후, `horizon:install` 아티즌 명령어로 자산을 배포하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

Horizon의 자산을 배포한 후, 주요 설정 파일은 `config/horizon.php`에 위치하게 됩니다. 이 설정 파일에서는 애플리케이션용 큐 작업자 옵션을 정의할 수 있습니다. 각 설정 옵션에는 상세한 설명이 포함되어 있으니, 꼭 이 파일 전체를 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 Redis 연결명은 예약되어 있으므로, `database.php` 설정파일의 다른 Redis 연결명이나 `horizon.php`의 `use` 옵션 값으로 `horizon`을 사용하지 않도록 주의하세요.

<a name="environments"></a>
#### 환경(Environment)

설치 후 가장 먼저 익혀야 할 Horizon 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 동작하는 환경별로 사용할 수 있으며, 각 환경에서 사용할 작업자 프로세스 옵션들을 정의합니다. 기본적으로 `production`과 `local` 환경이 정의되어 있으나, 필요에 따라 환경을 더 추가해도 무방합니다:

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

또한, 와일드카드 환경(`*`)을 정의해 별도의 환경 설정이 없는 경우에 적용할 수도 있습니다:

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

Horizon을 시작할 때, 현재 애플리케이션이 실행 중인 환경에 맞는 작업자 프로세스 설정이 적용됩니다. 보통 이 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment)의 값으로 결정됩니다. 예를 들어 기본 `local` 환경에서는 작업자 프로세스 3개가 자동으로 생성되며, 큐 별로 작업자를 자동으로 분배합니다. 기본 `production` 환경은 최대 10개의 작업자 프로세스를 시작하며, 각 큐에 작업자를 자동 분배하도록 설정되어 있습니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments` 항목에는 Horizon을 실행할 모든 [환경](/docs/12.x/configuration#environment-configuration)에 대한 항목이 반드시 포함되어야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisor)

Horizon의 기본 설정 파일에서 볼 수 있듯, 각 환경에는 하나 이상의 "supervisor(슈퍼바이저)"를 둘 수 있습니다. 기본값은 `supervisor-1`이지만, 이름은 자유롭게 지정할 수 있습니다. 각 supervisor는 하나의 작업자 그룹을 "감독"하는 역할을 하며, 여러 큐에 작업자 프로세스를 분산하는 일을 담당합니다.

특정 환경에서 별도의 작업자 그룹을 운영하고 싶다면 supervisor를 추가해 주시면 됩니다. 예를 들어, 특정 큐에 대해 다른 균형 전략이나 작업자 수를 지정하고 싶으면, supervisor를 분리해서 설정할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)에 있는 동안에는, supervisor의 `force` 옵션이 Horizon 설정파일에 `true`로 명시되지 않는 한 대기 중인 작업들이 실행되지 않습니다:

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

Horizon의 기본 설정 파일에는 `defaults` 옵션이 존재합니다. 이 옵션은 애플리케이션의 [supervisors](#supervisors)에서 사용할 기본값을 지정합니다. supervisor마다 반복적으로 작성해야 하는 값을 줄이기 위해, supervisor별 설정에 기본값을 자동으로 병합해줍니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로, 이 대시보드는 `local` 환경에서만 접근이 허용됩니다. 하지만, `app/Providers/HorizonServiceProvider.php` 파일에는 [인가 게이트](/docs/12.x/authorization#gates)가 설정되어 있습니다. 이 게이트는 **local이 아닌 환경**에서의 Horizon 접근을 제어합니다. 필요에 따라 아래와 같이 접근 대상을 제한할 수 있습니다:

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

Laravel은 기본적으로 인증된 사용자를 게이트 클로저에 자동 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 보안을 적용한다면, 사용자가 별도의 "로그인"을 하지 않아도 됩니다. 이런 경우, 위의 클로저 시그니처를 `function (User $user = null)`로 변경해 인증이 필수로 요구되지 않도록 해야 합니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수

> [!NOTE]
> 이 옵션을 조정하기 전에, Laravel의 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 'attempts(시도)' 개념을 먼저 익혀 두시기 바랍니다.

supervisor 설정에서 작업별 최대 시도 횟수를 지정할 수 있습니다:

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
> 이 옵션은 큐를 처리할 때 사용하는 아티즌 명령어의 `--tries` 옵션과 유사합니다.

특히 `WithoutOverlapping`, `RateLimited` 등과 같은 미들웨어 사용 시, 여러 시도가 소모될 수 있으므로 `tries` 옵션 조정이 중요합니다. supervisor의 `tries` 값 또는 작업 클래스에서 `$tries` 속성을 지정해 시도 횟수를 적절히 설정해 주세요.

`tries` 옵션을 설정하지 않으면 기본적으로 단 1회만 시도합니다. 단, 작업 클래스에 `$tries` 속성이 지정되어 있다면, 해당 값이 Horizon 설정보다 우선 적용됩니다.

`tries` 혹은 `$tries`를 0으로 설정하면 무제한 시도가 가능합니다. 이는 시도 횟수를 예측하기 어려울 때 유용합니다. 단, 끝없는 실패를 방지하려면 작업 클래스에 `$maxExceptions` 속성을 지정해 예외 제한을 두는 것이 좋습니다.

<a name="job-timeout"></a>
### 작업 타임아웃

마찬가지로 supervisor별로 `timeout` 값을 지정할 수 있습니다. 이는 작업자 프로세스가 한 작업을 실행할 수 있는 최대 초(sec)를 의미하며, 제한 초과 시 강제 종료됩니다. 종료된 작업은 큐 설정에 따라 재시도되거나 실패로 처리됩니다:

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
> `auto` 균형 전략을 쓸 때, Horizon은 실행 중인 작업자가 지정된 시간(타임아웃) 내에 작업을 완료하지 못하면 "중단(hanging)" 상태로 간주하여 프로세스를 강제로 종료할 수 있습니다. 항상 Horizon의 타임아웃 값이 개별 작업 레벨의 타임아웃 값보다 더 크게 설정되어야 하며, `config/queue.php`의 `retry_after` 값보다는 몇 초 짧게 두어야 합니다. 그렇지 않으면 작업이 실행 중에 중복 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 Backoff

supervisor 설정에서 `backoff` 값을 지정하여, 처리 중 예외가 발생했을 때 Horizon이 다음 재시도 이전에 얼마나 대기할지 조정할 수 있습니다:

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

또한 배열로 "지수적 backoff" 방식도 설정할 수 있습니다. 예를 들어, 다음 예제에서는 첫 재시도 후 1초, 두 번째 재시도 후 5초, 세 번째 재시도 및 그 이후는 10초 대기합니다:

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
### 무시한 작업

어떤 경우에는, 애플리케이션 또는 외부 패키지에서 발생한 특정 작업을 대시보드의 "완료된 작업" 목록에서 보이지 않게 하고 싶을 수 있습니다. 이런 작업을 무시하고자 한다면, 해당 작업 클래스명을 Horizon 설정파일의 `silenced` 옵션에 추가하면 됩니다:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또한, 무시하려는 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 할 수도 있습니다. 이 경우 `silenced` 설정 배열에 등록하지 않아도 자동으로 무시됩니다:

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 작업자 균형 전략

각 supervisor는 하나 이상의 큐를 처리할 수 있으며, Laravel 기본 큐 시스템과 달리 Horizon은 작업자 균형 전략을 `auto`, `simple`, `false`(균형 없음) 중에서 선택할 수 있습니다.

<a name="auto-balancing"></a>
### 자동 균형

기본값인 `auto` 전략은 현재 각 큐의 작업량에 따라 큐별 작업자 프로세스 수를 자동으로 조절합니다. 예를 들어 `notifications` 큐에 미처리 작업 1,000개, `default` 큐에는 작업이 없다면, Horizon은 `notifications` 큐에 더 많은 작업자를 할당해 큐가 모두 처리될 때까지 집중적으로 작업합니다.

`auto` 전략을 사용할 때 다음과 같은 설정을 추가로 지정할 수 있습니다:

<div class="content-list" markdown="1">

- `minProcesses`: 각 큐별 최소 작업자 프로세스 개수를 지정합니다. 이 값은 1 이상이어야 합니다.
- `maxProcesses`: 모든 큐에 할당될 수 있는 작업자 프로세스 최대 총합을 지정합니다. 일반적으로 (큐 갯수 × minProcesses)보다 크게 지정해야 하며, supervisor가 아예 프로세스를 생성하지 않게 하려면 0으로 설정할 수도 있습니다.

</div>

예를 들어, 각 큐별 최소 1개 프로세스를 유지하고, 전체 최대 10개 프로세스까지 확장할 수 있게 설정할 수 있습니다:

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

`autoScalingStrategy` 옵션은 작업자를 큐에 어떻게 분배할지 전략을 지정합니다:

<div class="content-list" markdown="1">

- `time` 전략: 큐를 비우는 데 걸리는 전체 예측 시간을 기준으로 작업자를 할당합니다.
- `size` 전략: 큐에 쌓인 전체 작업 개수를 기준으로 작업자를 할당합니다.

</div>

`balanceMaxShift`와 `balanceCooldown` 값은 작업자 수를 얼마나 빠르게 조정할지를 결정합니다. 위 예제에서는 3초마다 최대 1개의 새 작업자 프로세스를 추가 또는 삭제할 수 있습니다. 애플리케이션 상황에 맞게 이 값을 조정해 사용하면 됩니다.

<a name="auto-queue-priorities"></a>
#### 큐의 우선순위와 자동 균형

`auto` 균형 전략은 큐 간의 "엄격한 우선순위"를 강제하지 않습니다. supervisor 설정에서 큐를 나열하는 순서는 작업자 분배에 영향을 미치지 않으며, Horizon은 선택한 `autoScalingStrategy`에 따라 큐 양에 맞게 작업자를 동적으로 할당합니다.

예를 들어, 아래처럼 설정해도 high 큐가 default 큐보다 우선시되지는 않습니다:

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

큐간 상대적인 우선순위가 반드시 필요하다면 supervisor를 여러 개 만들어, 각각 큐별로 자원을 명확히 배분해야 합니다:

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

위와 같이 설정하면, default 큐는 최대 10개까지 프로세스를 확장할 수 있지만, images 큐는 오직 1개의 프로세스만 갖게 됩니다. 이렇게 하면 각 큐가 독립적으로 확장 가능합니다.

> [!NOTE]
> 리소스 소모가 큰 작업을 분리하려면, 별도의 큐 및 적정한 `maxProcesses` 값을 지정하는 것이 좋습니다. 그렇지 않으면 CPU 사용량이 과도하게 치솟아 서버에 부담을 줄 수 있습니다.

<a name="simple-balancing"></a>
### 간단한 균형

`simple` 전략은 지정한 큐 목록에 작업자 프로세스를 균등하게 나눠 할당합니다. 이 전략에서는 프로세스 수가 자동으로 확장되지 않고, 고정된 값만큼의 프로세스가 사용됩니다:

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

위 예제라면 default, notifications 큐에 각각 5개씩 총 10개의 프로세스가 할당됩니다.

만약 큐별로 할당된 프로세스 수를 개별적으로 제어하고 싶다면 supervisor를 여러 개 정의할 수 있습니다:

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

이 경우, default 큐에는 10개, notifications 큐에는 2개 작업자 프로세스가 할당됩니다.

<a name="no-balancing"></a>
### 균형 없음

`balance` 옵션을 `false`로 지정하면, Horizon은 큐가 목록에 나온 순서대로만 작업을 처리하고, 이는 Laravel 기본 큐 시스템과 동일합니다. 단, 작업이 쌓이면 작업자 프로세스 수를 자동 확장하는 점이 다릅니다:

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

위 설정이라면 default 큐의 작업이 먼저 모두 처리된 후에야 notifications 큐의 작업을 처리하기 시작합니다.

작업자 프로세스의 최소/최대 개수는 `minProcesses`, `maxProcesses` 옵션으로 제어할 수 있습니다:

<div class="content-list" markdown="1">

- `minProcesses`: 총 최소 작업자 프로세스 수를 지정하며, 1 이상이어야 합니다.
- `maxProcesses`: 작업자 프로세스가 확장될 수 있는 최대 총합을 지정합니다.

</div>

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 주요 버전을 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼭 꼼꼼히 확인해야 합니다.

<a name="running-horizon"></a>
## Horizon 실행하기

애플리케이션의 `config/horizon.php` 설정 파일에서 supervisor와 worker를 설정한 후, `horizon` 아티즌 명령어로 Horizon을 실행할 수 있습니다. 이 명령어 한 번으로 현재 환경에 맞는 작업자 프로세스를 모두 시작합니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지했다가 다시 이어서 작업을 처리하게 하려면, 다음과 같은 명령어를 사용할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

또한, 특정 [supervisor](#supervisors)를 일시 중지/다시 시작하려면 다음 명령어를 사용할 수 있습니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon 프로세스의 현재 상태를 확인하려면 다음 명령어를 사용하세요:

```shell
php artisan horizon:status
```

특정 [supervisor](#supervisors)의 상태를 확인하려면 다음 명령어를 사용합니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료하려면 `horizon:terminate` 명령어를 사용하면 됩니다. 현재 실행 중인 작업은 모두 완료되고 나서 Horizon이 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포하기

실제 애플리케이션 서버에 Horizon을 배포할 때에는, `php artisan horizon` 명령어가 예기치 않게 종료되는 경우 자동으로 다시 시작해줄 수 있도록 "프로세스 모니터"를 설정해야 합니다. 아래에서 프로세스 모니터 설치법을 안내합니다.

배포 과정에서는, 프로세스 모니터가 자동으로 재시작할 수 있도록 Horizon 프로세스를 종료해야 하며, 이 과정에서 신규 코드 변경 내용을 반영할 수 있습니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 환경에서 동작하는 프로세스 모니터로, `horizon` 프로세스가 중지되면 자동으로 재시작해줍니다. Ubuntu에서는 아래와 같은 명령어로 Supervisor를 설치할 수 있습니다. 만약 Ubuntu를 사용하지 않는다면 운영체제에 맞는 패키지 관리자를 이용해 Supervisor를 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> 직접 Supervisor를 설정하는 것이 부담스럽다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 서비스를 통해 백그라운드 프로세스를 간편하게 관리할 수도 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 서버의 `/etc/supervisor/conf.d` 디렉터리에 보관하는 것이 일반적입니다. 이 디렉터리에 다양한 설정 파일을 만들 수 있으며, 각각의 파일에서 supervisor가 모니터링할 프로세스를 지시할 수 있습니다. 예를 들어, `horizon.conf`라는 파일을 생성해 Horizon 프로세스를 시작 및 모니터링하도록 할 수 있습니다:

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

Supervisor 설정에서는 `stopwaitsecs` 값이 실행 중인 작업의 최대 예상 소요시간보다 충분히 길어야 합니다. 그렇지 않으면 Supervisor가 작업 완료 전에 프로세스를 중지시킬 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버에 적합하며, 운영체제에 따라 Supervisor 설정 파일의 위치나 확장자가 다를 수 있습니다. 서버 운영체제별 문서를 꼭 참고하시기 바랍니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 생성한 뒤, 다음 명령어로 Supervisor 설정을 읽고, 프로세스를 시작합니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 운영에 대한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon에서는 메일, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 각종 작업에 "태그"를 지정할 수 있습니다. 실제로 Horizon은 작업에 연관된 Eloquent 모델을 자동으로 인식해 태그를 자동 부여해줍니다. 예시 코드를 살펴보면:

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

이 작업에서 `App\Models\Video` 인스턴스의 `id` 속성이 1인 경우, 자동으로 `App\Models\Video:1` 태그가 지정됩니다. 이는 Horizon이 작업 클래스 내부의 Eloquent 모델 속성을 검색해 데이터 모델의 클래스명과 기본 키(Primary Key) 정보를 토대로 태그를 부여하기 때문입니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 직접 작업에 태그 지정하기

큐에 등록되는 객체에 대해 태그를 직접 지정하고 싶다면, 해당 클래스에 `tags` 메서드를 정의하면 됩니다:

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

큐에 등록된 이벤트 리스너에서 태그를 지정할 경우, Horizon이 이벤트 인스턴스를 `tags` 메서드로 전달해주므로, 이벤트 데이터를 참조하여 태그를 만들 수 있습니다:

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
## 알림

> [!WARNING]
> Horizon에서 Slack 또는 SMS 알림을 설정할 때는, [해당 알림 채널의 사전 필요 사항](/docs/12.x/notifications)을 반드시 확인하세요.

특정 큐의 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider` 클래스의 `boot` 메서드에서 호출할 수 있습니다:

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

"대기 시간이 긴 경우"의 기준을 설정하려면, 애플리케이션의 `config/horizon.php` 설정 파일에서 `waits` 옵션을 사용하면 됩니다. 이 옵션을 통해 연결/큐 종류별로 긴 대기 시간의 임계값(초 단위)을 정할 수 있습니다. 정의되지 않은 연결/큐 조합은 60초가 기본값입니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

대기 시간 임계값을 0으로 설정하면 해당 큐에 대한 긴 대기 알림이 비활성화됩니다.

<a name="metrics"></a>
## 지표

Horizon의 지표 대시보드는 작업 및 큐 대기 시간, 처리량 등에 대한 정보를 제공해줍니다. 이 대시보드를 채우기 위해서는 Horizon의 `snapshot` 아티즌 명령어가 5분마다 실행되도록 `routes/console.php` 파일에 예약 작업을 등록해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 지표 데이터를 삭제하고 싶을 때는 다음과 같은 `horizon:clear-metrics` 명령어를 실행할 수 있습니다:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 하나만 삭제하려면 `horizon:forget` 명령어를 사용할 수 있습니다. 이 명령어는 실패한 작업의 ID 또는 UUID만 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 삭제하고 싶을 때는 `--all` 옵션을 사용할 수 있습니다:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 존재하는 모든 작업을 삭제하고 싶다면, `horizon:clear` 아티즌 명령어로 가능합니다:

```shell
php artisan horizon:clear
```

특정 큐에서만 작업을 삭제하려면, `queue` 옵션을 지정하세요:

```shell
php artisan horizon:clear --queue=emails
```
