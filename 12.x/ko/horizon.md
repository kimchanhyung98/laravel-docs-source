# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 재시도 대기시간(Backoff)](#job-backoff)
    - [무시된 작업(Silenced Jobs)](#silenced-jobs)
- [작업자 밸런싱 전략](#balancing-strategies)
    - [자동 밸런싱](#auto-balancing)
    - [단순 밸런싱](#simple-balancing)
    - [밸런싱 비활성화](#no-balancing)
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
> Laravel Horizon을 본격적으로 살펴보기 전에, Laravel의 기본 [큐 서비스](/docs/12.x/queues)에 대해 충분히 숙지하시기 바랍니다. Horizon은 Laravel의 큐 시스템에 추가 기능을 제공하므로, 기본 큐 기능에 익숙하지 않다면 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis 큐](/docs/12.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정 기능을 제공합니다. Horizon을 사용하면 큐 시스템의 작업 처리량, 실행 시간, 작업 실패 등 핵심 지표를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용할 경우, 모든 큐 작업자 설정은 하나의 간결한 설정 파일에 저장됩니다. 애플리케이션의 작업자 구성을 버전 관리되는 파일로 정의함으로써, 애플리케이션을 배포할 때 큐 작업자를 쉽게 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon은 [Redis](https://redis.io)를 큐 시스템으로 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결을 반드시 `redis`로 지정해야 합니다.

Composer 패키지 관리자를 사용해 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, `horizon:install` Artisan 명령어를 사용해 Horizon의 애셋을 퍼블리시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

Horizon 애셋을 퍼블리시한 뒤, 주요 설정 파일은 `config/horizon.php`에 위치합니다. 이 파일에서 애플리케이션의 큐 작업자 옵션을 설정할 수 있습니다. 각 옵션에는 용도에 대한 설명이 포함되어 있으니, 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php` 파일의 `use` 옵션 등에서 다른 Redis 연결 이름으로 사용해서는 안 됩니다.

<a name="environments"></a>
#### 환경별 설정

설치 후 가장 먼저 익숙해져야 할 설정 옵션은 `environments` 설정입니다. 이 옵션은 애플리케이션이 실행되는 여러 환경에 대한 배열이며, 각 환경별로 작업자 프로세스 옵션을 정의합니다. 기본적으로 `production`과 `local` 환경이 들어있지만, 필요에 따라 환경을 추가할 수 있습니다:

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

또한 와일드카드 환경(`*`)을 정의할 수 있습니다. 이 경우, 일치하는 환경이 없을 때 사용됩니다:

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

Horizon을 시작하면, 애플리케이션이 실행 중인 환경에 맞는 작업자 프로세스 설정을 사용합니다. 일반적으로, 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment) 값을 기준으로 결정됩니다. 예를 들어, 기본 `local` Horizon 환경은 3개의 작업자 프로세스를 시작하고, 각 큐에 할당되는 작업자 수도 자동으로 밸런싱합니다. `production` 환경은 최대 10개의 작업자 프로세스를 시작하도록 기본 설정되어 있으며, 이 역시 자동 밸런싱됩니다.

> [!WARNING]
> `horizon` 설정 파일의 `environments` 항목에는 Horizon을 실행할 모든 [환경 구성](/docs/12.x/configuration#environment-configuration)이 반드시 포함되어야 합니다.

<a name="supervisors"></a>
#### Supervisor

Horizon의 기본 설정 파일에서 볼 수 있듯, 각 환경에는 하나 이상의 “슈퍼바이저(Supervisor)”를 둘 수 있습니다. 기본적으로 이 supervisor의 이름은 `supervisor-1`으로 되어 있지만, 원하는 이름으로 자유롭게 지정할 수 있습니다. Supervisor는 하나의 작업자 그룹을 "감독"하며, 여러 큐에 대해 작업자 프로세스를 적절히 분배하고 밸런싱하는 역할을 합니다.

특정 환경에 새로운 작업자 그룹을 정의하려면 supervisor를 추가하면 됩니다. 예를 들어, 애플리케이션에서 서로 다른 큐에 대해 별도의 밸런싱 전략이나 작업자 수를 설정하고 싶을 때 사용할 수 있습니다.

<a name="maintenance-mode"></a>
#### 점검 모드

애플리케이션이 [점검 모드](/docs/12.x/configuration#maintenance-mode)일 때, supervisor의 `force` 옵션이 Horizon 설정 파일에서 `true`로 지정되지 않으면 큐에 쌓인 작업이 처리되지 않습니다:

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

Horizon 기본 설정 파일에는 `defaults`라는 설정 항목이 있습니다. 이 옵션은 각 [슈퍼바이저](#supervisors)의 기본값을 지정하며, 환경별 supervisor 설정에 병합됩니다. 덕분에 supervisor를 설정할 때 불필요한 중복을 줄일 수 있습니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드를 사용할 수 있습니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일 내에 [인가 게이트(gate)](/docs/12.x/authorization#gates) 정의가 존재하며, 이 게이트는 **local이 아닌** 환경에서 Horizon 접근을 제어합니다. 필요에 따라 접근 제한 범위를 아래와 같이 수정할 수 있습니다:

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
#### 대체 인증(인가) 전략

Laravel은 위의 gate 클로저에 인증된 사용자를 자동으로 주입합니다. IP 제한과 같은 별도의 방법으로 Horizon 접근 제어를 하고 있다면, 사용자가 굳이 로그인할 필요가 없을 수 있습니다. 이 경우, 위 코드에서 `function (User $user)`를 `function (User $user = null)`로 변경하여 Laravel이 인증을 필수로 요구하지 않도록 할 수 있습니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수

> [!NOTE]
> 이 옵션을 상세히 다루기 전, Laravel의 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 ‘attempts’(시도) 개념을 숙지하십시오.

supervisor 설정에서 작업 하나당 최대 시도 횟수를 지정할 수 있습니다:

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
> 이 옵션은 아티즌 명령어에서 사용하는 `--tries` 옵션과 유사합니다.

`WithoutOverlapping`, `RateLimited`와 같은 미들웨어를 사용할 경우, 작업의 시도 횟수가 소모되므로 `tries` 옵션을 적절히 조정해야 합니다. supervisor 단위로 설정하거나, 작업 클래스에 `$tries` 속성을 정의해 과도한 시도를 방지하세요.

만약 `tries` 옵션을 지정하지 않으면 Horizon에서는 기본적으로 한 번만 시도합니다. 단, 작업 클래스에 `$tries`가 지정돼 있다면, 해당 값이 우선합니다.

`tries` 또는 `$tries` 값을 0으로 두면 시도 횟수 제한이 없어집니다. 예측 불가한 횟수의 작업엔 유용하나, 무한 루프 처리로 이어질 수 있으니, 작업 클래스의 `$maxExceptions` 속성으로 예외 발생 횟수도 제한할 수 있습니다.

<a name="job-timeout"></a>
### 작업 타임아웃

유사하게, supervisor 단위로 `timeout`(초)을 설정해 작업자 프로세스가 작업을 강제 종료하기까지의 최대 실행 시간을 지정할 수 있습니다. 강제로 종료되면, 큐 설정에 따라 작업이 재시도되거나 실패 처리됩니다:

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
> `timeout` 값은 반드시 `config/queue.php`의 `retry_after` 값보다 몇 초 작은 값으로 설정해야 합니다. 그렇지 않으면 동일 작업이 두 번 처리되는 현상이 발생할 수 있습니다.

<a name="job-backoff"></a>
### 작업 재시도 대기시간(Backoff)

unhandled 예외가 발생하여 작업을 재시도 할 때, 얼마나 대기할지 supervisor 단위로 `backoff` 값을 지정할 수 있습니다:

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

"지수(back-off)" 대기가 필요하다면 배열로도 지정할 수 있습니다. 아래 예시는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째 이후는 10초 간격으로 재시도합니다:

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
### 무시된 작업(Silenced Jobs)

특정 작업 또는 외부 패키지의 작업이 "완료된 작업" 목록에 불필요하게 나타나는 것을 원치 않을 때, 해당 작업을 무시할 수 있습니다. `horizon` 설정 파일의 `silenced` 옵션에 작업 클래스명을 추가하면 됩니다:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

또는, 무시할 작업 클래스에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현해도 됩니다. 이 인터페이스를 구현하면, 설정 배열에 없어도 자동으로 무시됩니다:

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 작업자 밸런싱 전략

각 supervisor는 하나 이상의 큐를 처리할 수 있습니다. Laravel의 기본 큐 시스템과 달리, Horizon은 `auto`, `simple`, `false`의 세 가지 작업자 밸런싱 전략을 지원합니다.

<a name="auto-balancing"></a>
### 자동 밸런싱

`auto` 전략(기본값)은 큐별 현재 작업량에 따라 작업자 프로세스 수를 동적으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 작업이 쌓여 있고 `default` 큐는 비어 있다면, Horizon은 `notifications` 큐에 더 많은 작업자를 할당하여 작업이 모두 처리될 때까지 집중적으로 처리합니다.

`auto` 전략 사용 시 `minProcesses`, `maxProcesses` 옵션도 설정할 수 있습니다:

- `minProcesses`: 큐별 최소 작업자 수입니다(1 이상).
- `maxProcesses`: 전체 큐에 걸쳐 Horizon이 확장할 수 있는 최대 총 작업자 수입니다. 보통, 큐 개수 × `minProcesses`보다 큰 값을 사용합니다. supervisor가 작업자를 생성하지 않도록 하려면 0으로 둘 수도 있습니다.

예시로, 큐별로 최소 1개, 최대 10개까지 작업자를 유지하도록 설정할 수 있습니다:

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

`autoScalingStrategy` 옵션은 Horizon이 큐에 작업자 프로세스를 어떻게 분배할지 결정합니다. 두 가지 전략 중 선택할 수 있습니다:

- `time`: 대기 중인 작업 전체를 처리하는데 필요한 예상 시간 기준 작업자 분배
- `size`: 큐에 쌓인 작업 개수 기준으로 작업자 분배

`balanceMaxShift`와 `balanceCooldown` 값은 Horizon이 작업자를 얼마나 신속하게 확장·축소할지 결정합니다. 위 예시에서는, 3초마다 최대 1개의 프로세스를 생성 또는 제거합니다. 애플리케이션 상황에 맞게 이 값들을 조정하세요.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위와 자동 밸런싱

`auto` 밸런싱에서는 큐 간의 엄격한 우선순위가 적용되지 않습니다. supervisor 설정에서 큐 순서를 변경해도 실제 작업자 할당에는 영향을 주지 않습니다. 대신, Horizon은 선택한 `autoScalingStrategy`에 따라 실시간으로 작업자 프로세스를 동적으로 큐별로 배분합니다.

예를 들어, 아래 설정처럼 큐 배열에 high를 먼저 넣어도, default에 비해 우선적으로 할당하지 않습니다:

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

큐별 상대적 우선순위를 확실히 적용하려면, supervisor를 여러 개 두고 각각 다른 밸런싱 전략이나 작업자 수를 지정하면 됩니다:

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

이 예시에서는, default 큐는 최대 10개, images 큐는 최대 1개의 작업자만 할당되어 각각 독립적으로 확장됩니다.

> [!NOTE]
> 시스템 자원을 많이 소모하는 작업이라면 별도의 큐와 supervisor에 할당하고, `maxProcesses` 값을 낮게 설정하는 것이 좋습니다. 그렇지 않으면 해당 작업이 과도한 CPU를 점유해 전체 시스템이 느려질 수 있습니다.

<a name="simple-balancing"></a>
### 단순 밸런싱

`simple` 전략은 지정한 큐에 대해 작업자 프로세스를 균등하게 분배합니다. 이 전략은 작업자 수를 자동으로 확장하지 않고, 고정된 수의 프로세스만 사용합니다:

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

위와 같은 설정에서는, 두 큐에 각각 5개씩, 총 10개의 작업자가 균등 배정됩니다.

특정 큐에만 작업자 수를 다르게 배정하려면 supervisor를 추가로 정의하세요:

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

이렇게 하면, default 큐는 10개, notifications 큐는 2개의 작업자를 할당받습니다.

<a name="no-balancing"></a>
### 밸런싱 비활성화

`balance` 옵션을 `false`로 설정하면, Horizon은 Laravel의 기본 큐 시스템처럼 큐 목록의 순서대로 작업을 처리합니다. 단, 작업이 쌓이면 작업자 프로세스 수는 확장될 수 있습니다:

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

위 예시에서는, default 큐의 작업이 항상 notifications 큐보다 먼저 처리됩니다. 예를 들어 default 큐에 1,000개의 작업이 있고, notifications 큐에 10개가 있다면, default의 모든 작업이 끝난 후에야 notifications 큐가 처리됩니다.

작업자 확장 범위는 `minProcesses`(최소), `maxProcesses`(최대) 옵션으로 제어합니다:

- `minProcesses`: 전체 작업자 프로세스의 최소 개수(1 이상)
- `maxProcesses`: 전체 작업자 프로세스의 최대 개수

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 메이저 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토해 주세요.

<a name="running-horizon"></a>
## Horizon 실행

애플리케이션의 `config/horizon.php`에서 supervisor 및 작업자 구성을 마쳤다면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 단일 명령어로 현재 환경의 모든 worker 프로세스가 실행됩니다:

```shell
php artisan horizon
```

진행 중인 Horizon 프로세스를 일시정지하거나, 작업 처리를 재개하려면 다음의 Artisan 명령어를 사용합니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [슈퍼바이저](#supervisors)만 일시정지/재개할 수도 있습니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon 프로세스의 현재 상태를 확인하려면 다음 명령을 사용하세요:

```shell
php artisan horizon:status
```

특정 Horizon [슈퍼바이저](#supervisors)의 상태만 확인도 가능합니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Graceful하게 Horizon 프로세스를 종료하려면 아래의 명령을 사용하면 됩니다. 현재 처리 중인 작업까지 모두 완료하고 Horizon이 실행 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon 배포

Horizon을 실제 서버에 배포할 때는, `php artisan horizon` 명령어를 감시(process monitoring)하고, 예기치 않게 종료될 경우 재시작시켜 주는 프로세스 모니터를 설정해야 합니다. 이후에 프로세스 모니터 설치 방법을 안내합니다.

배포 작업 중에는 Horizon 프로세스가 새 코드로 재시작될 수 있도록, 아래처럼 종료 명령어를 실행해야 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 환경용 프로세스 모니터링 도구로, `horizon` 프로세스가 중단되면 자동으로 재실행합니다. Ubuntu에서는 다음 명령어로 Supervisor를 설치할 수 있습니다. 다른 OS를 사용 중이라면 운영체제에 맞는 패키지 관리자로 설치해 주세요:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정이 어렵게 느껴진다면, [Laravel Cloud](https://cloud.laravel.com) 서비스를 활용해 백그라운드 프로세스 관리를 맡길 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장합니다. 이 디렉토리 내에 원하는 만큼 설정 파일을 생성해, 어떤 프로세스를 어떻게 감시할지 지정할 수 있습니다. 예를 들어, `horizon.conf` 파일을 생성하여 `horizon` 프로세스를 모니터링하도록 할 수 있습니다:

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

Supervisor 설정 시, `stopwaitsecs` 값이 실행 시간 기준 가장 오래 걸릴 작업의 시간보다 커야 합니다. 그렇지 않으면 Supervisor가 작업 처리 중에 프로세스를 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 계열 서버에 유효합니다. 운영체제에 따라 설정 파일 위치나 확장자가 다를 수 있으므로, 자세한 내용은 서버 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 생성한 후, 아래 명령어로 Supervisor 설정을 적용하고, 프로세스를 시작하세요:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행 및 관리에 관한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 확인하세요.

<a name="tags"></a>
## 태그

Horizon은 작업(메일 전송 객체, 브로드캐스트 이벤트, 알림, 큐 처리 이벤트 리스너 포함)에 “태그”를 붙일 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델에 따라 대부분의 작업에 태그를 자동으로 부여합니다. 예를 들어, 다음과 같은 작업이 있다고 가정해보겠습니다:

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

이 작업이 `id` 속성이 1인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 자동으로 `App\Models\Video:1` 태그가 부여됩니다. Horizon이 작업의 속성에서 Eloquent 모델을 자동으로 찾아, 모델의 클래스명 및 기본키로 태그를 붙이기 때문입니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업에 수동으로 태그 달기

작업 큐에 명시적으로 태그를 추가하고 싶다면, 클래스에 `tags` 메서드를 정의하면 됩니다:

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
#### 이벤트 리스너에 수동으로 태그 달기

큐 처리 이벤트 리스너에 태그를 추가할 때는, Horizon이 이벤트 인스턴스를 `tags` 메서드에 자동으로 넘겨줍니다. 이벤트 데이터를 활용해 태그를 커스텀할 수 있습니다:

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
> Horizon에서 Slack이나 문자 메시지(SMS) 알림을 설정할 때는, [관련 알림 채널의 사전 준비사항](/docs/12.x/notifications)을 반드시 확인해야 합니다.

특정 큐의 대기 시간이 길어지면 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드는 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하세요:

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
#### 알림 대기시간 임계값 설정

"대기 시간이 길다"고 판단할 기준 시간은 `config/horizon.php` 설정 파일의 `waits` 옵션에서 세부적으로 지정할 수 있습니다. 이 옵션은 연결/큐별로 임계값을 지정하며, 미설정 시 60초가 기본값입니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
## 메트릭

Horizon에는 작업 및 큐의 대기시간, 처리량 등의 정보를 제공하는 메트릭 대시보드가 내장되어 있습니다. 이 대시보드를 정상적으로 표시하려면, `routes/console.php` 파일에서 5분마다 `horizon:snapshot` Artisan 명령어가 실행되도록 스케줄링해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 메트릭 데이터를 삭제하려면, 아래의 Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 개별적으로 삭제하려면, `horizon:forget` 명령어를 사용하세요. 이 명령어는 실패한 작업의 ID 또는 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

실패한 모든 작업을 삭제하려면, `--all` 옵션을 같이 사용하세요:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 쌓인 모든 작업을 삭제하려면, 다음의 Artisan 명령을 사용합니다:

```shell
php artisan horizon:clear
```

특정 큐의 작업만 삭제하려면, `queue` 옵션을 같이 쓸 수 있습니다:

```shell
php artisan horizon:clear --queue=emails
```
