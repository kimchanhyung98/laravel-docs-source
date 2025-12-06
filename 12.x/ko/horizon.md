# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 재시도 대기(backoff)](#job-backoff)
    - [침묵 처리된 작업](#silenced-jobs)
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
- [큐의 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]
> Laravel Horizon을 본격적으로 사용하기 전에, Laravel의 기본 [큐 서비스](/docs/12.x/queues)를 숙지하는 것이 좋습니다. Horizon은 Laravel 큐 시스템에 추가적인 기능을 제공하므로, 기본 큐 동작에 익숙하지 않으면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel에서 동작하는 [Redis 큐](/docs/12.x/queues)를 위한 뛰어난 대시보드와 코드 기반 구성 방식을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 실패한 작업 등 큐 시스템의 주요 지표를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용할 경우, 모든 큐 워커(worker) 설정이 단일이며 심플한 구성 파일에 저장됩니다. 작업자의 설정을 버전 관리되는 파일에 정의함으로써, 애플리케이션을 배포할 때 큐 워커의 수평 확장이나 수정 작업을 쉽게 할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon은 큐 시스템이 [Redis](https://redis.io)를 사용하도록 요구합니다. 따라서 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 설정되어 있는지 반드시 확인하십시오. 현재 시점에서 Horizon은 Redis Cluster와 호환되지 않습니다.

Composer 패키지 매니저를 통해 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치가 완료되면, 다음의 `horizon:install` Artisan 명령어를 실행해 Horizon의 에셋을 퍼블리시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 구성

Horizon의 에셋을 퍼블리시한 후, 주요 설정 파일은 `config/horizon.php`에 위치하게 됩니다. 이 파일을 통해 애플리케이션의 큐 워커 관련 옵션들을 설정할 수 있습니다. 각 옵션에는 해당 목적이나 설명이 포함되어 있으니, 설정 파일을 꼼꼼히 확인하시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 Redis 연결명을 사용합니다. 이 연결명은 예약되어 있으므로, `database.php`의 다른 Redis 연결이나 `horizon.php` 구성 파일의 `use` 옵션에 할당해서는 안 됩니다.

<a name="environments"></a>
#### 환경별 설정

설치 후 가장 먼저 익숙해져야 할 Horizon 설정 옵션은 `environments` 항목입니다. 이 옵션은 애플리케이션이 동작하는 여러 환경별로 워커 프로세스 설정을 정의할 수 있도록 배열로 제공됩니다. 기본값으로는 `production`과 `local` 환경이 포함되어 있으나, 필요에 따라 환경을 자유롭게 추가할 수 있습니다:

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

다른 환경과 일치하는 값이 없을 때 사용할 와일드카드 환경(`*`)도 정의할 수 있습니다:

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

Horizon을 시작하면, 현재 애플리케이션 환경에 해당하는 워커 프로세스 설정으로 동작하게 됩니다. 일반적으로 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment)의 값을 기반으로 결정됩니다. 예를 들어 기본 `local` 환경에서는 워커 프로세스가 3개로 시작하며 각 큐에 자동으로 작업자를 분배합니다. `production` 환경에서는 최대 10개의 워커 프로세스로 시작하고, 각 큐에 대해 자동 분산이 적용됩니다.

> [!WARNING]
> 추후 Horizon을 실행할 모든 [환경](/docs/12.x/configuration#environment-configuration)에 대해 `horizon` 설정 파일의 `environments` 항목에 엔트리가 포함되어 있는지 꼭 확인하세요.

<a name="supervisors"></a>
#### 슈퍼바이저(Supervisor)

Horizon의 기본 설정 파일에서 알 수 있듯, 각 환경마다 하나 이상의 "슈퍼바이저"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 이름으로 정의되어 있지만, 원하는대로 자유롭게 이름을 지정할 수 있습니다. 각 슈퍼바이저는 하나의 워커 프로세스 그룹을 "감독"하는 역할을 하며, 큐별로 워커 분산을 관리합니다.

각기 다른 큐에 대해 별도의 부하 분산 전략이나 워커 수를 설정하고 싶을 때 슈퍼바이저를 추가로 구성할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)에 있을 경우, supervisor의 `force` 옵션이 `true`로 지정된 경우를 제외하고는 Horizon에서 큐 작업이 처리되지 않습니다:

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
#### 기본값 설정

Horizon의 기본 설정 파일에는 `defaults`라는 항목이 있습니다. 이 옵션은 [슈퍼바이저](#supervisors)별로 적용될 기본값을 지정합니다. 슈퍼바이저별 기본값은 각 환경 설정에 병합되므로, 중복 정의를 방지할 수 있습니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로로 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 대시보드에 접근할 수 있습니다. 하지만, `app/Providers/HorizonServiceProvider.php` 파일에 [인가 게이트](/docs/12.x/authorization#gates)가 정의되어 있으며, 이는 **로컬 환경이 아닌** 경우의 Horizon 접근 권한을 제어합니다. 필요에 따라 아래 게이트를 수정하여 Horizon 접근을 제어할 수 있습니다:

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

Laravel에서는 게이트 클로저에 인증된 사용자를 자동으로 주입합니다. 다른 방식(IP 제한 등)으로 Horizon 접근을 제어하는 경우 사용자가 반드시 로그인할 필요가 없습니다. 이럴 때에는 위의 클로저 시그니처를 `function (User $user)`에서 `function (User $user = null)`로 변경하여 인증을 강제하지 않도록 할 수 있습니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수

> [!NOTE]
> 이 옵션을 설정하기 전에, Laravel 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 작업 'attempts' 개념을 숙지하세요.

슈퍼바이저 설정에서 작업당 최대 시도 횟수를 지정할 수 있습니다:

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
> 이 옵션은 Artisan 큐 처리 명령어의 `--tries` 옵션과 유사하게 동작합니다.

`WithoutOverlapping`, `RateLimited` 같은 미들웨어를 사용하는 경우 시도 횟수가 소비되므로, supervisor 수준 또는 작업 클래스의 `$tries` 속성을 적절히 조정해야 합니다.

`tries` 옵션을 설정하지 않은 경우, Horizon의 기본값은 1회이며, 작업 클래스에 `$tries` 속성이 정의되어 있는 경우에는 이 값을 우선합니다.

`tries` 또는 `$tries`를 0으로 설정하면 시도 횟수에 제한이 없어집니다. 시도 횟수를 특정할 수 없는 상황에서 사용할 수 있지만, 무한 반복 실패를 막기 위해 작업 클래스에 `$maxExceptions` 속성을 설정하여 예외 허용 횟수를 제한할 수 있습니다.

<a name="job-timeout"></a>
### 작업 타임아웃

마찬가지로, supervisor 레벨에서 `timeout` 값을 설정해 워커 프로세스가 작업을 강제로 종료하기 전까지 실행할 최대 초 단위를 지정할 수 있습니다. 강제로 종료된 작업은 큐 설정에 따라 재시도 처리되거나 실패로 기록됩니다:

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
> `auto` 전략 사용 시, Horizon은 처리 중인 워커를 "지연" 상태로 간주하며 Horizon 타임아웃 시간이 지나면 강제 종료합니다. 항상 작업 별 타임아웃보다 Horizon의 타임아웃이 더 크도록 설정하세요. 그렇지 않으면 실행 중인 작업이 중간에 종료될 수 있습니다. 또한, 이 `timeout` 값은 `config/queue.php`의 `retry_after` 값보다 반드시 몇 초 작아야 하며, 그렇지 않으면 작업이 중복 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 재시도 대기(backoff)

supervisor 레벨에서 `backoff` 값을 설정하면, 처리되지 않은 예외 발생 시 Horizon이 작업을 재시도하기 전에 대기할 시간을 지정할 수 있습니다:

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

배열로 지정하여 "지수 백오프"도 구성할 수 있습니다. 아래 예시에서는 첫 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 이후는 모두 10초씩 대기합니다:

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
### 침묵 처리된 작업

가끔, 애플리케이션 또는 서드파티 패키지에서 발생시키는 특정 작업은 대시보드에서 보고 싶지 않을 수 있습니다. 이런 작업들은 "Completed Jobs" 목록에서 공간만 차지하게 되므로, 침묵 처리가 가능합니다. 설정 파일의 `silenced` 항목에 해당 작업 클래스 이름을 추가하면 됩니다:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

이 외에도, [태그](#tags)를 기준으로 여러 작업을 한 번에 숨길 수도 있습니다:

```php
'silenced_tags' => [
    'notifications'
],
```

또는 침묵 처리하려는 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 하면, 이 작업이 `silenced` 배열에 없더라도 자동으로 침묵 처리됩니다:

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

각 슈퍼바이저는 하나 이상의 큐를 처리할 수 있으며, Laravel 기본 큐 시스템과는 다르게 Horizon에서는 `auto`, `simple`, `false` 세 가지 워커 부하 분산 전략을 선택할 수 있습니다.

<a name="auto-balancing"></a>
### 자동 부하 분산

기본값인 `auto` 전략은 현재 큐의 작업량에 따라 큐별 워커 프로세스 수를 자동 조절합니다. 예를 들어, `notifications` 큐에 1,000개의 작업이 대기 중이고 `default` 큐는 비어 있다면, Horizon은 `notifications` 큐에 워커를 집중 배치합니다.

`auto` 전략에서는 `minProcesses`와 `maxProcesses` 옵션을 함께 설정할 수 있습니다:

- `minProcesses`는 큐별 최소 워커 프로세스 수(1 이상)를 의미합니다.
- `maxProcesses`는 Horizon이 전체 큐에 할당할 최대 워커 프로세스 총합입니다. 일반적으로 큐 개수 × `minProcesses` 값보다 크게 잡으며, 0으로 지정하면 supervisor가 프로세스를 생성하지 않습니다.

예를 들어, 큐별 최소 1개, 전체 최대 10개 프로세스를 유지하려면 다음과 같이 설정합니다:

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

`autoScalingStrategy` 옵션은 Horizon이 큐에 추가 워커를 배정하는 방식을 정합니다. 두 가지 전략 중 선택할 수 있습니다:

- `time` : 큐를 비우는 데 걸릴 총 예상 시간에 따라 워커를 할당합니다.
- `size` : 큐에 쌓인 작업 개수에 따라 워커를 할당합니다.

`balanceMaxShift`와 `balanceCooldown` 설정값은 워커 수 증감 속도를 결정합니다. 위 예시에서는 3초마다 새 프로세스 1개가 생성 또는 종료될 수 있습니다. 애플리케이션 상황에 맞게 값을 조정할 수 있습니다.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위와 자동 부하 분산

`auto` 전략을 사용할 때는 큐 간 우선순위가 엄격하게 보장되지 않습니다. supervisor 설정에서 큐의 순서는 워커 분배에 영향을 주지 않으며, Horizon은 선택한 `autoScalingStrategy`에 따라 워커 프로세스를 동적으로 할당합니다.

예를 들어, 아래 설정에서 `high` 큐가 `default` 큐보다 앞에 있어도 자동으로 우선 처리되지 않습니다:

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

큐 간 상대적 우선순위를 지정하고 싶다면, supervisor를 복수로 정의해 각 큐에 할당된 리소스를 명확히 나눠야 합니다:

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

위 예시에서는 `default` 큐가 최대 10개, `images` 큐는 최대 1개 프로세스만 사용하도록 하여 각 큐가 독립적으로 확장할 수 있도록 했습니다.

> [!NOTE]
> 자원 소모가 큰 작업은 별도의 큐와 적은 `maxProcesses` 값을 할당하는 것이 시스템 과부하를 방지하는 데 도움이 됩니다.

<a name="simple-balancing"></a>
### 단순 부하 분산

`simple` 전략은 지정된 큐 목록에 워커 프로세스를 균등 분배합니다. 이 때 Horizon은 워커 프로세스 개수를 자동 확장하지 않고, 지정한 개수만큼만 사용합니다:

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

위에서는 큐 2개가 각각 5개씩, 총 10개로 나뉘어 할당됩니다.

특정 큐에 개별적으로 워커 수를 지정하려면 supervisor를 여러 개 지정하면 됩니다:

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

이 설정에서는 `default` 큐에 10개, `notifications` 큐에 2개의 프로세스가 각각 할당됩니다.

<a name="no-balancing"></a>
### 부하 분산 없음

`balance` 옵션을 `false`로 설정하면, Horizon은 Laravel 기본 큐 시스템과 마찬가지로 큐 목록 순서대로 작업을 처리합니다. 하지만 큐에 작업이 쌓일 때 워커 프로세스 확장은 계속 지원됩니다:

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

위 예시에서는 항상 `default` 큐의 작업이 `notifications` 큐보다 먼저 처리됩니다. 예를 들어, `default` 큐에 1,000개, `notifications` 큐에 10개 작업이 대기 중이라면, `default` 큐 작업이 모두 처리된 뒤에야 `notifications` 큐에 대한 처리가 시작됩니다.

Horizon의 워커 수 확장/축소 범위는 `minProcesses`와 `maxProcesses` 옵션으로 제어합니다:

- `minProcesses`: 전체의 최소 워커 프로세스 수(1 이상).
- `maxProcesses`: 전체의 최대 워커 프로세스 수.

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 새로운 메이저 버전으로 업그레이드할 때에는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="running-horizon"></a>
## Horizon 실행

애플리케이션의 `config/horizon.php`에서 supervisor와 워커를 설정한 후, 단일 Artisan 명령어로 Horizon을 실행할 수 있습니다. 이 명령어는 현재 환경 설정에 따른 모든 워커 프로세스를 시작합니다:

```shell
php artisan horizon
```

Horizon 프로세스를 일시 중지하거나 다시 처리하도록 명령하려면 다음 명령어를 사용할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 [슈퍼바이저](#supervisors)만을 일시 중지하거나 다시 시작하려면 아래 명령어를 사용합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스의 상태를 확인하려면 `horizon:status`를 실행하세요:

```shell
php artisan horizon:status
```

특정 supervisor의 현재 상태를 확인하려면 `horizon:supervisor-status`를 이용합니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 안전하게 종료하려면 `horizon:terminate` 명령어를 사용할 수 있습니다. 이 경우 현재 처리 중인 작업까지 완료된 뒤 프로세스가 멈춥니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

애플리케이션 서버에 실제로 Horizon을 배포할 때에는, `php artisan horizon` 명령어를 감시하고 예기치 않게 중단되었을 때 재시작하도록 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설치법을 다룹니다.

배포 과정에서는 Horizon 프로세스를 종료시켜, 프로세스 모니터가 새로운 코드 버전을 반영하여 자동 재시작할 수 있도록 해야 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터로, `horizon` 프로세스가 중단될 경우 자동으로 재시작해줍니다. Ubuntu에서 Supervisor 설치는 다음 명령어를 사용합니다. Ubuntu가 아니라면 운영체제용 패키지 매니저로 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정이 부담스럽다면, [Laravel Cloud](https://cloud.laravel.com)를 이용해 백그라운드 프로세스 관리 기능을 사용할 수도 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 구성

Supervisor 구성 파일은 보통 서버 `/etc/supervisor/conf.d` 디렉터리에 위치합니다. 이 디렉터리 내에서 supervisor가 감시할 프로세스별 설정 파일을 자유롭게 생성할 수 있습니다. 예를 들어, `horizon` 프로세스를 시작·감시하는 `horizon.conf` 파일을 생성할 수 있습니다:

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

Supervisor를 설정할 때는 `stopwaitsecs` 값이 실행 중인 가장 긴 작업의 소요 시간보다 커야 합니다. 그렇지 않으면 Supervisor가 작업을 처리 완료 전에 강제로 종료시킬 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 서버 기준이며, 기타 운영체제에서는 Supervisor 설정 파일 위치나 확장자가 다를 수 있습니다. 해당 서버의 공식 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 실행

설정 파일을 생성했다면, 다음 명령어로 supervisor 구성을 갱신하고 감시 대상을 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행 및 관리에 관한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon에서는 작업, 메일 발송 메일러블, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 대기 작업에 "태그"를 부여할 수 있습니다. 실제로, Horizon은 대부분의 작업에서 연관된 Eloquent 모델을 기반으로 자동으로 태그를 지정해줍니다. 예를 들어, 아래와 같은 작업이 있다고 가정해봅시다:

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

이 작업이 `id` 속성이 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 자동으로 `App\Models\Video:1` 태그가 붙게 됩니다. Horizon은 작업의 프로퍼티에서 Eloquent 모델을 찾아 모델 클래스명+기본키 형식으로 태그를 자동 생성합니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업 태그 수동 지정

큐에 등록된 객체의 태그를 직접 정의하려면 해당 클래스에 `tags` 메서드를 추가하면 됩니다:

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

큐에 등록된 이벤트 리스너의 경우, Horizon은 이벤트 인스턴스를 `tags` 메서드에 전달해주기 때문에, 이벤트 데이터를 태그에 활용할 수 있습니다:

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
> Horizon에서 Slack 또는 SMS 알림을 설정할 때는 반드시 [해당 알림 채널의 사전 요구 사항](/docs/12.x/notifications)을 확인하세요.

특정 큐에서 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 보통 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출합니다:

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

각 큐별로 대기 시간이 몇 초를 초과하면 "대기 시간 길어짐"으로 간주할지, `config/horizon.php`의 `waits` 항목에서 설정할 수 있습니다. 정의하지 않은 큐/연결 조합에는 기본값 60초가 적용됩니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

특정 큐의 임계값을 `0`으로 지정하면 해당 큐의 대기 시간 알림을 비활성화할 수 있습니다.

<a name="metrics"></a>
## 메트릭

Horizon에는 메트릭 대시보드가 포함되어 있어, 작업 및 큐의 대기 시간/처리량 등 다양한 정보를 제공합니다. 이 대시보드를 채우려면, `routes/console.php` 파일에서 Horizon의 `snapshot` Artisan 명령이 5분마다 실행되도록 스케줄링해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 메트릭 데이터를 삭제하려면, 다음 Artisan 명령을 실행할 수 있습니다:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 삭제하려면 `horizon:forget` 명령을 사용할 수 있습니다. 이 명령은 실패한 작업의 ID나 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 한 번에 삭제하려면, `--all` 옵션을 추가합니다:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐의 작업 비우기

애플리케이션의 기본 큐에 등록된 모든 작업을 삭제하려면, 다음 Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐의 작업만 비우고 싶다면 `queue` 옵션을 사용할 수 있습니다:

```shell
php artisan horizon:clear --queue=emails
```
