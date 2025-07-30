# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐에 쌓인 작업 스케줄링](#scheduling-queued-jobs)
    - [쉘 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 주기 옵션](#schedule-frequency-options)
    - [시간대 설정](#timezones)
    - [작업 중첩 방지](#preventing-task-overlaps)
    - [한 서버에서만 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행하기](#running-the-scheduler)
    - [1분 미만 간격 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

과거에는 서버에서 예약해야 하는 각 작업마다 직접 크론(cron) 설정 항목을 작성했을 수 있습니다. 하지만 이렇게 하면 작업 스케줄이 소스 관리에 포함되지 않아 관리가 어렵고, 기존 크론 항목을 보거나 새 항목을 추가하기 위해 서버에 SSH로 접속해야 하기 때문에 번거로워집니다.

Laravel의 커맨드 스케줄러는 서버에서 예약 작업을 관리하는 새로운 방식을 제공합니다. 이 스케줄러를 사용하면 Laravel 애플리케이션 내부에서 명령 스케줄을 유창하고 명확한 방식으로 정의할 수 있습니다. 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 있으면 됩니다. 작업 스케줄은 일반적으로 `routes/console.php` 파일에 정의됩니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기 (Defining Schedules)

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 예를 들어, 매일 자정에 호출될 클로저를 예약하고, 클로저 내에서 데이터베이스 쿼리를 실행하여 특정 테이블을 초기화하는 경우를 살펴봅시다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 이용한 스케줄링 외에도 `__invoke` 메서드를 포함하는 간단한 PHP 클래스인 [호출 가능한 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄할 수도 있습니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

만약 `routes/console.php` 파일을 명령어 정의 전용으로 쓰고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용해 스케줄 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 인수로 받는 클로저를 허용합니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

현재 정의된 예약 작업과 다음 실행 시점을 한눈에 보고 싶다면 `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링 (Scheduling Artisan Commands)

클로저 외에도 Artisan 명령어와 시스템 명령어를 스케줄할 수 있습니다. 예를 들어, `command` 메서드를 이용해 명령어 이름이나 클래스명을 사용해 Artisan 명령어를 예약할 수 있습니다.

클래스명을 이용해 Artisan 명령어를 예약하는 경우, 명령어 실행 시 추가할 커맨드라인 인수를 배열로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Artisan 클로저 명령어 스케줄링

클로저로 정의된 Artisan 명령어를 예약하려면, 명령어 정의 뒤에 스케줄링 메서드를 체인할 수 있습니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달하려면 `schedule` 메서드에 인수 배열을 넣습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐에 쌓인 작업 스케줄링 (Scheduling Queued Jobs)

`job` 메서드는 [큐 작업](/docs/12.x/queues) 예약에 사용할 수 있습니다. 이 방법은 `call` 메서드를 통해 클로저를 정의하지 않고 간편히 큐 작업을 예약할 수 있게 해줍니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드에 선택적으로 두 번째, 세 번째 인수로 큐 이름과 큐 연결명을 지정해 작업을 특정 큐에 보낼 수도 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "sqs" 커넥션의 "heartbeats" 큐로 작업 디스패치
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 쉘 명령어 스케줄링 (Scheduling Shell Commands)

`exec` 메서드는 운영체제에 명령어를 실행하도록 지시할 때 사용합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 주기 옵션 (Schedule Frequency Options)

작업을 지정한 간격으로 실행하는 몇 가지 방법을 살펴봤지만, 사실 더 많은 빈도 옵션을 지정할 수 있습니다:

<div class="overflow-auto">

| 메서드                             | 설명                                              |
| ---------------------------------- | -------------------------------------------------- |
| `->cron('* * * * *');`             | 커스텀 크론 스케줄에 맞게 작업 실행               |
| `->everySecond();`                 | 매초 작업 실행                                    |
| `->everyTwoSeconds();`             | 2초마다 작업 실행                                 |
| `->everyFiveSeconds();`            | 5초마다 작업 실행                                 |
| `->everyTenSeconds();`             | 10초마다 작업 실행                                |
| `->everyFifteenSeconds();`         | 15초마다 작업 실행                                |
| `->everyTwentySeconds();`          | 20초마다 작업 실행                                |
| `->everyThirtySeconds();`          | 30초마다 작업 실행                                |
| `->everyMinute();`                 | 매분 작업 실행                                    |
| `->everyTwoMinutes();`             | 2분마다 작업 실행                                 |
| `->everyThreeMinutes();`           | 3분마다 작업 실행                                 |
| `->everyFourMinutes();`            | 4분마다 작업 실행                                 |
| `->everyFiveMinutes();`            | 5분마다 작업 실행                                 |
| `->everyTenMinutes();`             | 10분마다 작업 실행                                |
| `->everyFifteenMinutes();`         | 15분마다 작업 실행                                |
| `->everyThirtyMinutes();`          | 30분마다 작업 실행                                |
| `->hourly();`                      | 매시간 작업 실행                                  |
| `->hourlyAt(17);`                  | 매시간 17분에 작업 실행                           |
| `->everyOddHour($minutes = 0);`    | 홀수 시간마다 작업 실행                            |
| `->everyTwoHours($minutes = 0);`   | 2시간마다 작업 실행                               |
| `->everyThreeHours($minutes = 0);` | 3시간마다 작업 실행                               |
| `->everyFourHours($minutes = 0);`  | 4시간마다 작업 실행                               |
| `->everySixHours($minutes = 0);`   | 6시간마다 작업 실행                               |
| `->daily();`                       | 매일 자정에 작업 실행                             |
| `->dailyAt('13:00');`              | 매일 13:00에 작업 실행                            |
| `->twiceDaily(1, 13);`             | 매일 1:00과 13:00에 작업 실행                     |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1:15와 13:15에 작업 실행                     |
| `->weekly();`                      | 매주 일요일 00:00에 작업 실행                      |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8:00에 작업 실행                       |
| `->monthly();`                     | 매월 첫째 날 00:00에 작업 실행                     |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15:00에 작업 실행                         |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일과 16일 13:00에 작업 실행                  |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15:00에 작업 실행                    |
| `->quarterly();`                   | 분기별 첫째 날 00:00에 작업 실행                   |
| `->quarterlyOn(4, '14:00');`       | 분기별 4일 14:00에 작업 실행                        |
| `->yearly();`                      | 매년 첫날 00:00에 작업 실행                         |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17:00에 작업 실행                      |
| `->timezone('America/New_York');`  | 작업의 시간대를 설정                               |

</div>

이 메서드들은 추가적인 조건과 결합하여, 특정 요일 등에만 실행되는 정밀한 스케줄을 만들 수 있습니다. 예를 들어 매주 월요일에만 명령을 실행하도록 하려면 다음과 같이 합니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 오후 1시에 한 번 실행...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 매시간 실행...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

추가적인 스케줄 제약 조건들은 다음과 같습니다:

<div class="overflow-auto">

| 메서드                                   | 설명                                            |
| ---------------------------------------- | ------------------------------------------------|
| `->weekdays();`                          | 평일에만 작업 실행                              |
| `->weekends();`                          | 주말에만 작업 실행                              |
| `->sundays();`                           | 일요일에만 작업 실행                            |
| `->mondays();`                           | 월요일에만 작업 실행                            |
| `->tuesdays();`                          | 화요일에만 작업 실행                            |
| `->wednesdays();`                        | 수요일에만 작업 실행                            |
| `->thursdays();`                         | 목요일에만 작업 실행                            |
| `->fridays();`                           | 금요일에만 작업 실행                            |
| `->saturdays();`                         | 토요일에만 작업 실행                            |
| `->days(array\|mixed);`                  | 지정한 요일에만 작업 실행                        |
| `->between($startTime, $endTime);`       | 시작 시각부터 종료 시각 사이에만 작업 실행         |
| `->unlessBetween($startTime, $endTime);` | 시작 시각부터 종료 시각 사이에는 작업 실행 제외     |
| `->when(Closure);`                       | 주어진 조건이 참일 때만 작업 실행                  |
| `->environments($env);`                  | 특정 환경에서만 작업 실행                         |

</div>

<a name="day-constraints"></a>
#### 요일 제약 (Day Constraints)

`days` 메서드는 특정 요일에만 작업을 실행하도록 제한할 수 있습니다. 예를 들어, 매주 일요일과 수요일에 한 시간마다 `emails:send` 명령어를 실행하고 싶다면:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는 `Illuminate\Console\Scheduling\Schedule` 클래스 내 상수를 사용해 요일을 명시할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간대 제한 (Between Time Constraints)

`between` 메서드는 작업 실행을 특정 시간 범위로 제한할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로 `unlessBetween` 메서드는 지정한 시간대에 작업 실행을 제외하고 싶을 때 사용합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건 검사 제약 (Truth Test Constraints)

`when` 메서드는 주어진 클로저의 반환값이 `true`일 때만 작업을 실행하도록 제한합니다. 다른 조건이 없으면 `true` 반환 시 작업이 진행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`과 반대 개념으로, `true`를 반환하면 작업 실행을 건너뜁니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

`when` 메서드를 체인으로 여러 개 사용하면, 모든 조건이 `true`일 때만 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 (Environment Constraints)

`environments` 메서드는 지정한 환경(`APP_ENV` 환경 변수 기준)에서만 작업이 실행되도록 제한할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 시간대 설정 (Timezones)

`timezone` 메서드로 예약 작업 시간의 기준이 될 시간대를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 작업에 동일한 시간대를 지정하고 싶다면 애플리케이션 `app` 설정 파일에 `schedule_timezone` 옵션을 정의하면 됩니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 시간대는 일광 절약 시간제(DST)를 사용합니다. DST 변경 시 작업이 두 번 실행되거나 전혀 실행되지 않을 수도 있으니, 가능하면 시간대별 예약은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중첩 방지 (Preventing Task Overlaps)

기본적으로 예약 작업은 이전 인스턴스가 아직 실행 중이어도 계속 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

위 예시의 `emails:send` Artisan 명령어는 이미 실행 중이지 않을 때만 매분 실행됩니다. 이 기능은 실행 시간이 크게 달라서 작업 종료 예상 시간을 알기 어려운 작업에 특히 유용합니다.

잠금 만료 시간은 기본 24시간이며, 필요하면 분 단위로 커스터마이즈할 수 있습니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping`는 애플리케이션의 [캐시](/docs/12.x/cache)를 활용합니다. 락이 풀리지 않는 문제가 생기면 `schedule:clear-cache` Artisan 명령어로 락 캐시를 초기화할 수 있습니다. 이런 상황은 주로 예상치 못한 서버 문제로 작업이 멈췄을 때만 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서만 작업 실행 (Running Tasks on One Server)

> [!WARNING]
> 이 기능을 사용하려면 앱 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 혹은 `redis` 여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

애플리케이션 스케줄러가 여러 서버에서 실행되는 경우, 특정 작업을 한 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤마다 보고서를 생성하는 작업이 있는데 스케줄러가 세 서버에서 실행 중이라면, 작업이 세 번 중복 실행될 수 있습니다. 이는 바람직하지 않습니다.

한 서버에서만 실행하려면 작업 정의 시 `onOneServer` 메서드를 사용합니다. 작업을 먼저 획득한 서버가 원자적 락을 확보하여 다른 서버가 동시에 실행하지 못하게 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

원자적 락을 얻는데 사용할 캐시 저장소를 변경하려면 `useCache` 메서드를 사용합니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 이름 지정하기

인수를 달리해 동일한 작업을 여러 스케줄로 예약하면서도, 각각은 한 서버에서만 실행되도록 하고 싶다면, 각 작업에 `name` 메서드로 고유한 이름을 부여해야 합니다:

```php
Schedule::job(new CheckUptime('https://laravel.com'))
    ->name('check_uptime:laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();

Schedule::job(new CheckUptime('https://vapor.laravel.com'))
    ->name('check_uptime:vapor.laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();
```

마찬가지로 단일 서버에서 실행할 예약 클로저도 이름을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업 (Background Tasks)

기본적으로 동시에 예약된 여러 작업은 `schedule` 메서드 정의 순서대로 순차 실행됩니다. 작업이 오래 걸리면 후속 작업 시작이 지연될 수 있습니다. 모든 작업을 동시에 실행했으면 한다면 `runInBackground` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command` 및 `exec` 메서드로 예약한 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드 (Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 서버 유지보수를 방해하지 않기 위함입니다. 하지만 유지보수 중에도 특정 작업을 강제로 실행하려면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하면 됩니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹 (Schedule Groups)

구성 옵션이 비슷한 여러 작업을 정의할 때, 반복 코드가 많아지기 쉬운데 Laravel은 작업 그룹 기능을 제공해 이를 쉽게 처리할 수 있습니다. 그룹 메서드를 호출하며 공통 옵션을 설정하고, 클로저 안에 설정을 공유하는 작업들을 정의하면 코드가 간결해지고 일관성이 유지됩니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::daily()
    ->onOneServer()
    ->timezone('America/New_York')
    ->group(function () {
        Schedule::command('emails:send --force');
        Schedule::command('emails:prune');
    });
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행하기 (Running the Scheduler)

작업 스케줄 정의법을 알았으니, 이번에는 실제로 서버에서 예약 작업을 실행하는 방법을 알아봅니다. `schedule:run` Artisan 명령어는 현재 서버 시간을 기준으로 실행할 작업이 있는지 평가해 해당하는 작업들을 동작시킵니다.

따라서 Laravel 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 등록하면 됩니다. 이 크론은 매분 `schedule:run` 명령어를 실행하도록 설정합니다. 서버에 크론 등록이 익숙하지 않다면, 작동을 편리하게 관리해주는 [Laravel Cloud](https://cloud.laravel.com) 같은 관리형 플랫폼 이용도 고려해 보세요:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 작업 (Sub-Minute Scheduled Tasks)

대부분 운영체제에서 크론 작업은 1분에 한 번만 실행할 수 있지만, Laravel 스케줄러는 1초 단위로도 수행할 수 있도록 지원합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션에 1분 미만 간격 작업이 정의되어 있으면, `schedule:run` 명령은 즉시 종료하지 않고 현재 분이 끝날 때까지 계속 실행되어 필요한 모든 작업을 호출합니다.

1분 미만 작업이 예상보다 오래 걸리면 다음 작업 실행이 지연될 우려가 있으므로, 실제 작업 처리 로직은 큐 작업이나 백그라운드 커맨드로 디스패치하는 방식을 권장합니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 간격 작업 중단 (Interrupting Sub-Minute Tasks)

`sub-minute` 작업이 정의되어 있으면 `schedule:run` 명령은 한 분이 끝날 때까지 지속 실행됩니다. 배포 시에는 이전 버전으로 실행 중인 이 명령이 종료될 때까지 기다려야 하는데, 이를 방지하려면 배포 스크립트에 `schedule:interrupt` 명령을 호출해 실행 중인 스케줄러 인스턴스를 중단할 수 있습니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기 (Running the Scheduler Locally)

로컬 개발 환경에는 크론 항목을 추가하지 않는 것이 일반적입니다. 대신 `schedule:work` Artisan 명령어를 사용합니다. 이 명령은 포그라운드에서 실행되며, 중지할 때까지 매분 스케줄러를 호출합니다. 1분 미만 작업도 처리합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

Laravel 스케줄러는 예약 작업이 생성하는 출력을 다루기 위한 여러 편리한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용하면 출력 결과를 파일에 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력 내용을 파일 끝에 덧붙이고 싶으면 `appendOutputTo` 메서드를 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드는 출력 결과를 지정한 이메일 주소로 전송합니다. 다만, 출력 이메일 전송 전에 Laravel의 [메일 서비스](/docs/12.x/mail) 설정을 완료해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

예약 Artisan이나 시스템 명령어가 비정상 종료(종료 코드가 0이 아닌 경우)에 한해서만 출력 메일을 보내려면 `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 또는 `exec` 메서드로 예약된 작업에만 쓸 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅 (Task Hooks)

`before`와 `after` 메서드는 예약 작업 실행 전후에 실행할 코드를 지정할 때 사용합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업이 실행되기 직전...
    })
    ->after(function () {
        // 작업 실행 완료 후...
    });
```

`onSuccess` 및 `onFailure` 메서드는 예약 작업이 성공하거나 실패했을 때 실행할 코드를 각각 지정할 수 있습니다. 실패란 예약 Artisan이나 시스템 명령어가 종료 코드 0이 아닌 상태로 종료됨을 뜻합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업 성공 시...
    })
    ->onFailure(function () {
        // 작업 실패 시...
    });
```

명령어의 출력이 있다면, `after`, `onSuccess`, `onFailure` 훅에서 `Illuminate\Support\Stringable` 타입 힌트 `$output` 매개변수를 이용해 출력에 접근할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업 성공 시...
    })
    ->onFailure(function (Stringable $output) {
        // 작업 실패 시...
    });
```

<a name="pinging-urls"></a>
#### URL 자동 호출 (Pinging URLs)

`schedule` 메서드의 `pingBefore`와 `thenPing` 메서드를 사용하면 작업 실행 전후에 지정된 URL을 자동으로 호출할 수 있습니다. 이는 [Envoyer](https://envoyer.io) 같은 외부 서비스에 작업 시작 및 완료를 알릴 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess`와 `pingOnFailure` 메서드는 작업 성공 또는 실패 시에만 URL을 호출합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 지정한 조건이 `true`일 때만 URL을 호출하는 기능을 제공합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBeforeIf($condition, $url)
    ->thenPingIf($condition, $url);

Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccessIf($condition, $successUrl)
    ->pingOnFailureIf($condition, $failureUrl);
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 스케줄링 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 이벤트들에 대한 [리스너](/docs/12.x/events)를 등록해 추가 작업을 수행할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                                   |
| ------------------------------------------------------------ |
| `Illuminate\Console\Events\ScheduledTaskStarting`            |
| `Illuminate\Console\Events\ScheduledTaskFinished`            |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished`  |
| `Illuminate\Console\Events\ScheduledTaskSkipped`             |
| `Illuminate\Console\Events\ScheduledTaskFailed`              |

</div>