# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 백오프](#job-backoff)
    - [무시된 작업](#silenced-jobs)
- [부하 분산 전략](#balancing-strategies)
    - [자동 분산](#auto-balancing)
    - [단순 분산](#simple-balancing)
    - [분산 없음](#no-balancing)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [대기열에서 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]
> Laravel Horizon을 본격적으로 사용하기 전에, Laravel의 기본 [큐 서비스](/docs/12.x/queues)에 익숙해져야 합니다. Horizon은 Laravel의 큐 기능에 추가 기능을 제공하므로, 기본 큐 기능을 모른다면 다소 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반의 [Redis 큐](/docs/12.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정 기능을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패와 같은 큐 시스템의 주요 지표를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 설정이 단 하나의 간단한 설정 파일에 저장됩니다. 이처럼 워커 구성을 버전 관리되는 파일에서 관리하면, 애플리케이션 배포 시 큐 워커를 손쉽게 확장하거나 변경할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon을 사용하려면 큐 드라이버로 반드시 [Redis](https://redis.io)를 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결을 `redis`로 지정해야 합니다.

Horizon 패키지는 Composer를 사용하여 프로젝트에 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어를 사용해 Horizon의 에셋을 퍼블리시합니다.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

Horizon 에셋을 퍼블리시하면, 주요 설정 파일이 `config/horizon.php`에 생성됩니다. 이 설정 파일에서 애플리케이션의 큐 워커 옵션을 구성할 수 있습니다. 각 설정 사항에는 해당 목적에 대한 설명이 포함되어 있으므로, 이 파일을 꼼꼼히 읽어보는 것이 좋습니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 이름은 예약어이므로, `database.php` 설정 파일이나 `horizon.php` 설정 파일의 `use` 옵션에서 다른 Redis 연결 이름으로 지정해서는 안 됩니다.

<a name="environments"></a>
#### 환경 설정

설치 후 가장 먼저 익숙해져야 할 주요 Horizon 설정 항목은 `environments`입니다. 이 설정 항목은 애플리케이션이 실행되는 환경별로 워커 프로세스 옵션을 정의하는 배열입니다. 기본적으로 `production`과 `local` 환경이 정의되어 있지만, 필요에 따라 더 많은 환경을 추가할 수 있습니다.

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

또한 와일드카드 환경(`*`)도 정의할 수 있으며, 이 값은 일치하는 환경이 없을 때 적용됩니다.

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

Horizon을 시작하면 현재 실행 중인 애플리케이션의 환경에 맞는 워커 프로세스 설정을 사용합니다. 통상적으로 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment)에 의해 결정됩니다. 예를 들어, 기본 `local` Horizon 환경은 워커 프로세스를 3개 시작하며, 각 큐에 할당된 워커 프로세스 수를 자동으로 분산 조정합니다. `production` 환경의 기본값은 최대 10개의 워커 프로세스를 시작하고, 이들 역시 각 큐별로 자동으로 분산됩니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments` 부분에는 Horizon을 실행할 계획이 있는 모든 [환경](/docs/12.x/configuration#environment-configuration)을 반드시 포함해야 합니다.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisors)

Horizon 기본 설정 파일을 보면 각 환경은 하나 이상의 "supervisor(슈퍼바이저)"를 가질 수 있습니다. 디폴트로는 `supervisor-1`이 정의되어 있지만, 원하는 이름으로 슈퍼바이저를 추가할 수 있습니다. 각 슈퍼바이저는 워커 프로세스 그룹의 "감독" 역할을 하며, 워커 프로세스를 큐에 따라 적절히 분배하는 기능도 담당합니다.

환경별로 슈퍼바이저를 추가하면, 해당 환경에서 별도 워커 그룹을 정의할 수 있습니다. 예를 들어, 특정 큐에 대해 다른 분산 전략이나 워커 프로세스 수를 적용하고 싶을 때, 슈퍼바이저를 추가하면 됩니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는, Horizon이 큐에 쌓인 작업을 처리하지 않습니다. 다만 슈퍼바이저의 `force` 옵션을 `true`로 설정하면 유지보수 중에도 작업을 처리할 수 있습니다.

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

Horizon 기본 설정 파일에는 `defaults` 항목이 있습니다. 이 설정은 [슈퍼바이저](#supervisors)의 기본값을 지정하며, 각 환경의 슈퍼바이저 설정에 병합되어 중복 입력을 줄일 수 있습니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로로 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접속할 수 있습니다. 하지만 `app/Providers/HorizonServiceProvider.php` 파일에 정의된 [인가 게이트](/docs/12.x/authorization#gates)를 통해 **비로컬** 환경에서의 접근 권한을 제어할 수 있습니다. 필요에 따라 해당 게이트를 수정하여 Horizon 접근 정책을 강화할 수 있습니다.

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

Laravel은 자동으로 인증된 사용자를 게이트 클로저에 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon의 접근을 보안 처리한다면, 사용자 로그인 과정을 생략할 수도 있습니다. 이 경우 위의 `function (User $user)` 시그니처를 `function (User $user = null)`로 변경하면, Laravel이 인증을 필수로 요구하지 않습니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수

> [!NOTE]
> 이 옵션을 변경하기 전에, Laravel의 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 '시도 횟수'의 개념을 충분히 이해하세요.

슈퍼바이저 설정 내에서 작업의 최대 시도 횟수를 지정할 수 있습니다.

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

`WithoutOverlapping` 또는 `RateLimited`와 같은 미들웨어를 사용할 때는 `tries` 옵션 조정이 중요합니다. 이런 미들웨어는 시도 횟수를 소모하기 때문에, 슈퍼바이저 수준에서 `tries`를 조정하거나 작업 클래스에 `$tries` 속성을 명시해야 합니다.

`tries` 값을 따로 지정하지 않으면 기본값은 1이며, 작업 클래스에 `$tries` 속성이 있으면 그 값이 Horizon 설정보다 우선 적용됩니다.

`tries`나 `$tries` 값을 0으로 설정하면 시도 횟수에 제한이 없어집니다. 시도 횟수를 알 수 없는 경우에 유용합니다. 다만, 끝없는 실패를 방지하기 위해 작업 클래스에 `$maxExceptions` 속성을 설정하여 예외 허용 횟수를 제한할 수 있습니다.

<a name="job-timeout"></a>
### 작업 타임아웃

마찬가지로, 슈퍼바이저 수준에서 `timeout` 값을 지정하면 워커 프로세스가 한 작업을 최대 몇 초 동안 처리할 수 있는지 제한할 수 있습니다. 타임아웃이 지나면 해당 작업은 강제로 종료되며, 이후 작업 재시도 또는 실패 처리됩니다.

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
> `auto` 부하 분산 전략을 사용할 때, Horizon은 진행 중인 워커를 "멈춤" 상태로 보고 Horizon 타임아웃이 지나면 강제 종료합니다(스케일 다운 시). 항상 Horizon의 타임아웃이 작업 레벨 타임아웃보다 커야 하며, 그렇지 않으면 실행 중인 작업이 중간에 종료될 수 있습니다. 또한 `timeout` 값은 반드시 `config/queue.php` 설정 파일에 정해진 `retry_after` 값보다 몇 초 더 짧게 잡아야 합니다. 그렇지 않으면 작업이 두 번 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 백오프

슈퍼바이저 수준의 `backoff` 값으로 처리 실패 시 작업 재시도까지 대기할 시간을 지정할 수 있습니다.

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

배열을 사용하여 "지수(backoff) 대기"를 구성할 수도 있습니다. 예를 들어, 처음에는 1초, 두 번째는 5초, 세 번째 이후는 10초씩 대기하게 됩니다.

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
### 무시된 작업

때때로, 특정 작업은 애플리케이션이나 서드파티 패키지에서 디스패치되더라도 "완료된 작업" 리스트에서 보이지 않기를 원할 수 있습니다. 이럴 때는 무시할 작업의 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가하면 됩니다.

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는, 무시하려는 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 하면, `silenced` 배열에 추가하지 않아도 자동으로 무시됩니다.

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 부하 분산 전략

각 슈퍼바이저는 하나 이상의 큐를 처리할 수 있습니다. Laravel 기본 큐 시스템과 달리, Horizon에서는 세 가지 워커 부하 분산 전략을 선택할 수 있습니다: `auto`, `simple`, `false`

<a name="auto-balancing"></a>
### 자동 분산

`auto` 전략(기본값)은 큐의 현재 작업량에 따라 큐별 워커 프로세스 수를 자동으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고 `default` 큐가 비어 있다면, Horizon은 워커를 `notifications` 큐에 더 많이 할당하여 작업이 비워질 때까지 우선 처리합니다.

`auto` 전략에서는 추가로 `minProcesses`와 `maxProcesses` 옵션도 설정할 수 있습니다.

- `minProcesses`는 큐별 최소 워커 프로세스 수를 지정합니다. 1 이상이어야 합니다.
- `maxProcesses`는 전체 큐에 대해 Horizon이 사용할 수 있는 워커 프로세스 최대 수를 지정합니다. 이 값은 큐 개수 × `minProcesses`보다 충분히 큰 값이 권장됩니다. 프로세스 생성을 막으려면 0으로 설정할 수도 있습니다.

예를 들어, 큐마다 최소 하나의 프로세스를 유지하고, 전체적으로 최대 10개까지 프로세스를 확장하도록 구성할 수 있습니다.

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

`autoScalingStrategy` 옵션은 Horizon이 워커 프로세스를 어떻게 할당할지 결정합니다. 다음 두 가지 전략 중 선택할 수 있습니다.

- `time`: 대기열을 비우는 데 걸리는 총 예상 시간을 기준으로 워커를 할당합니다.
- `size`: 대기 중인 작업 수에 따라 워커를 할당합니다.

`balanceMaxShift`와 `balanceCooldown` 값은 Horizon이 워커 수요에 맞게 얼마나 빠르게 스케일링할지를 조정합니다. 위 예시에서는 3초마다 최대 1개의 프로세스가 생성 또는 종료됩니다. 이 값들은 애플리케이션 상황에 따라 조정 가능합니다.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위와 자동 분산

`auto` 분산 전략을 사용할 때, Horizon은 큐 간 엄격한 우선순위를 적용하지 않습니다. 슈퍼바이저 설정에서 큐를 나열하는 순서가 워커 프로세스 할당에 영향을 주지 않으며, 오직 `autoScalingStrategy`에 따라 동적으로 워커가 분배됩니다.

예를 들어, 아래 설정에서는 `high` 큐가 리스트에 먼저 있어도 `default` 큐보다 우선 처리되지 않습니다.

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

큐 간 상대적 우선순위를 반드시 적용해야 한다면, 여러 슈퍼바이저를 정의하고 각 큐에 명시적으로 자원을 할당할 수 있습니다.

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

이렇게 하면 `default` 큐는 최대 10개, `images` 큐는 최대 1개의 프로세스만 할당되어, 각 큐별 독립적인 확장 구조가 보장됩니다.

> [!NOTE]
> 리소스를 많이 소모하는 작업은 별도의 큐로 분리하고, 해당 큐의 `maxProcesses` 값을 제한하는 것이 좋습니다. 그렇지 않으면 이 작업들이 과도한 CPU를 점유하여 시스템 전체에 영향을 줄 수 있습니다.

<a name="simple-balancing"></a>
### 단순 분산

`simple` 전략은 워커 프로세스를 지정된 큐에 균등하게 할당합니다. 이 전략을 사용하면 워커 프로세스 수가 자동으로 확장되지 않고, 고정된 프로세스 개수로 동작합니다.

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

위 예시에서는 프로세스 10개가 `default`와 `notifications` 큐에 각각 5개씩 자동으로 나뉘어 할당됩니다.

각 큐별로 프로세스 수를 지정하려면, 슈퍼바이저를 여러 개 따로 정의할 수 있습니다.

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

이 설정에서는 `default` 큐에 10개, `notifications` 큐에 2개의 프로세스가 할당됩니다.

<a name="no-balancing"></a>
### 분산 없음

`balance` 옵션을 `false`로 설정하면, Horizon은 큐를 나열한 순서대로(먼저 나열된 큐 우선) 작업을 처리하며, Laravel 기본 큐 시스템과 유사하게 동작합니다. 단, 작업이 많아지면 워커 프로세스의 확장은 계속 발생합니다.

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

위 예시에서는 항상 `default` 큐 작업의 처리가 우선시되며, 그 후에야 `notifications` 큐의 작업이 처리됩니다. 예를 들어 `default`에 1,000개, `notifications`에 10개의 작업이 있을 때, `default` 작업을 모두 처리하고 나서야 `notifications` 작업을 시작합니다.

Horizon의 워커 확장 여부는 `minProcesses`와 `maxProcesses`로 제어할 수 있습니다.

- `minProcesses`: 전체 최소 워커 프로세스 수 (1 이상)
- `maxProcesses`: 전체 최대 워커 프로세스 수

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 새로운 주요 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

<a name="running-horizon"></a>
## Horizon 실행

`config/horizon.php` 설정 파일에서 슈퍼바이저와 워커 구성을 마쳤다면, `horizon` Artisan 명령어로 Horizon을 실행할 수 있습니다. 한 번의 명령어로 현재 환경에 맞는 모든 워커 프로세스가 시작됩니다.

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지하거나, 작업 처리를 다시 시작하는 명령어는 다음과 같습니다.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 [슈퍼바이저](#supervisors)를 개별적으로 일시 중지하거나 재개하려면 아래와 같은 명령어를 사용합니다.

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon 프로세스의 현재 상태를 확인하려면 아래 명령어를 사용합니다.

```shell
php artisan horizon:status
```

특정 [슈퍼바이저](#supervisors)의 상태만 확인하려면 다음과 같은 명령어를 입력합니다.

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료하려면 `horizon:terminate` 명령어를 사용하세요. 현재 처리 중인 작업이 모두 완료된 이후 프로세스가 종료됩니다.

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

실제 서버에 Horizon을 배포할 때는 프로세스 모니터를 설정하여 `php artisan horizon` 명령어가 중단되었을 때 자동으로 재시작되도록 해야 합니다. 프로세스 모니터 설치 방법은 아래에서 자세히 다룹니다.

애플리케이션 배포 과정에서, 프로세스 모니터가 작업 재시작 및 코드 변경 사항을 반영할 수 있도록 Horizon 프로세스를 먼저 종료하는 것이 좋습니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터로, `horizon` 프로세스가 멈췄을 때 자동으로 재시작해줍니다. Ubuntu에서는 아래 명령어로 Supervisor를 설치할 수 있습니다. Ubuntu가 아닌 환경에서는 운영체제별 패키지 매니저로 설치하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정이 어렵다면, [Laravel Cloud](https://cloud.laravel.com)와 같이 백그라운드 프로세스를 관리해주는 서비스를 고려해볼 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 서버의 `/etc/supervisor/conf.d` 디렉터리에 위치하는 것이 일반적입니다. 이 디렉터리 내에서 여러 개의 설정 파일을 만들어 Supervisor가 해당 프로세스를 감시하도록 할 수 있습니다. 예를 들어, `horizon.conf` 파일을 생성해 Horizon 프로세스를 모니터링하게 할 수 있습니다.

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

Supervisor 설정 시, `stopwaitsecs` 값은 가장 오래 실행되는 작업의 소요 시간보다 큰 값으로 지정해야 합니다. 그렇지 않으면 작업이 완료되기 전에 Supervisor가 해당 작업을 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버를 위한 것이며, Supervisor 설정 파일의 위치와 파일 확장자는 운영체제마다 다를 수 있습니다. 자세한 내용은 서버 운영체제의 문서를 확인하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일 생성을 완료하면, 아래 명령어로 Supervisor에 설정을 반영하고 모니터링 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 사용에 대한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 작업(job), 메일러블(mailable), 브로드캐스트 이벤트, 알림, 큐잉된 이벤트 리스너에 "태그"를 지정할 수 있습니다. 사실 Horizon은 대부분의 작업을 Eloquent 모델과 연관지어 자동으로 태깅합니다. 예를 들어, 아래와 같은 작업을 보세요.

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

이 작업이 `id`가 1인 `App\Models\Video` 인스턴스와 함께 큐잉되면, 자동으로 `App\Models\Video:1` 태그가 부여됩니다. Horizon이 작업의 속성을 검사해 Eloquent 모델이 있으면 모델의 클래스명과 기본 키(primary key)를 조합해 태깅하기 때문입니다.

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업에 태그 수동 지정

큐잉 객체(작업 등)에 원하는 태그를 직접 지정하려면 클래스에 `tags` 메서드를 정의하면 됩니다.

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
#### 이벤트 리스너에 태그 수동 지정

큐잉된 이벤트 리스너에 대한 태그를 가져올 때, Horizon은 이벤트 인스턴스를 `tags` 메서드로 전달합니다. 이를 활용해 이벤트 데이터를 태그에 추가할 수 있습니다.

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
> Horizon에서 Slack 또는 SMS 알림을 구성할 때는 반드시 [해당 알림 채널의 각종 사전 준비 사항](/docs/12.x/notifications)을 확인하세요.

특정 큐의 대기 시간이 길어졌을 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하면 됩니다.

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

애플리케이션의 `config/horizon.php` 파일의 `waits` 설정 항목을 통해 "긴 대기(long wait)"로 간주할 대기 시간을 지정할 수 있습니다. 이 값은 각 연결/큐 조합별로 설정 가능하며, 정의되지 않은 조합에는 기본값 60초가 적용됩니다.

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭

Horizon에는 작업 및 큐 대기 시간, 처리량 관련 정보를 제공하는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드를 데이터를 채우기 위해, 애플리케이션의 `routes/console.php` 파일에서 `horizon:snapshot` Artisan 명령어가 5분마다 실행되도록 스케줄링해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 메트릭 데이터를 삭제하려면 `horizon:clear-metrics` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용합니다. 이 명령어는 실패한 작업의 ID 또는 UUID를 인수로 받습니다.

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 한 번에 삭제하려면 `--all` 옵션을 추가합니다.

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 대기열에서 작업 비우기

애플리케이션의 기본 큐에 쌓인 모든 작업을 삭제하려면 `horizon:clear` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:clear
```

특정 큐의 작업만 삭제하려면 `queue` 옵션을 지정합니다.

```shell
php artisan horizon:clear --queue=emails
```
