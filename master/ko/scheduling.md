# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐드 작업 스케줄링](#scheduling-queued-jobs)
    - [쉘 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 실행 빈도 옵션](#schedule-frequency-options)
    - [시간대 설정](#timezones)
    - [작업 중복 실행 방지](#preventing-task-overlaps)
    - [한 서버에서 작업 실행하기](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행하기](#running-the-scheduler)
    - [1분 미만 간격 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 후크](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

과거에는 서버에서 실행할 각 작업마다 별도의 cron 설정 항목을 작성했을 것입니다. 그러나 이렇게 하면 작업 스케줄이 소스 관리에 포함되지 않고 추가 작업을 하거나 기존 cron 항목을 확인하려면 서버에 SSH로 접속해야 하므로 번거로울 수 있습니다.

Laravel의 명령어 스케줄러는 서버에서 실행할 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내부에서 명령어 스케줄을 유연하고 표현력 있게 정의할 수 있으며, 서버에는 단 하나의 cron 항목만 필요합니다. 일반적으로 작업 스케줄은 애플리케이션의 `routes/console.php` 파일에 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기 (Defining Schedules)

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 예시를 통해 살펴보겠습니다. 이 예제에서는 매일 자정에 실행할 클로저를 스케줄링하여, 클로저 내부에서 데이터베이스 쿼리를 실행해 테이블을 청소합니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저 외에도 [호출 가능한 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함하는 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

만약 `routes/console.php` 파일을 명령어 정의 용도로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용해 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 전달받는 클로저를 받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

정의된 예약 작업과 다음 실행 시간을 확인하려면 `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링 (Scheduling Artisan Commands)

클로저를 스케줄링하는 것 외에도 [Artisan 명령어](/docs/master/artisan) 또는 시스템 명령어를 스케줄링할 수 있습니다. 예를 들어, `command` 메서드를 사용해 명령 이름이나 클래스 이름으로 Artisan 명령어를 예약할 수 있습니다.

클래스 이름으로 Artisan 명령어를 스케줄링할 경우, 명령어가 호출될 때 전달할 추가 커맨드라인 인수 배열을 함께 넘길 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Artisan 클로저 명령어 스케줄링

클로저로 정의한 Artisan 명령어를 스케줄링하려면 명령어 정의 뒤에 스케줄 관련 메서드를 체이닝하면 됩니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달하려면, `schedule` 메서드에 인수를 배열로 제공하면 됩니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐드 작업 스케줄링 (Scheduling Queued Jobs)

`job` 메서드는 [큐된 작업](/docs/master/queues)을 스케줄링할 때 사용합니다. 이 메서드는 `call` 메서드로 클로저를 정의해 작업을 큐에 넣는 번거로움 없이 간편하게 큐 작업을 예약할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

두 번째와 세 번째 인수로 각각 큐 이름과 큐 연결을 지정할 수도 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "sqs" 연결의 "heartbeats" 큐로 작업 디스패치...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 쉘 명령어 스케줄링 (Scheduling Shell Commands)

`exec` 메서드를 이용하면 운영체제 명령어를 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 실행 빈도 옵션 (Schedule Frequency Options)

앞서 몇 가지 작업 실행 간격 예시를 보았습니다. 하지만 작업에 할당할 수 있는 다양한 스케줄 실행 빈도 옵션이 존재합니다:

<div class="overflow-auto">

| 메서드                               | 설명                                                 |
| ---------------------------------- | ---------------------------------------------------- |
| `->cron('* * * * *');`             | 사용자 지정 cron 스케줄로 실행.                       |
| `->everySecond();`                 | 매초 실행.                                          |
| `->everyTwoSeconds();`             | 2초마다 실행.                                        |
| `->everyFiveSeconds();`            | 5초마다 실행.                                        |
| `->everyTenSeconds();`             | 10초마다 실행.                                       |
| `->everyFifteenSeconds();`         | 15초마다 실행.                                       |
| `->everyTwentySeconds();`          | 20초마다 실행.                                       |
| `->everyThirtySeconds();`          | 30초마다 실행.                                       |
| `->everyMinute();`                 | 매분 실행.                                          |
| `->everyTwoMinutes();`             | 2분마다 실행.                                        |
| `->everyThreeMinutes();`           | 3분마다 실행.                                        |
| `->everyFourMinutes();`            | 4분마다 실행.                                        |
| `->everyFiveMinutes();`            | 5분마다 실행.                                        |
| `->everyTenMinutes();`             | 10분마다 실행.                                       |
| `->everyFifteenMinutes();`         | 15분마다 실행.                                       |
| `->everyThirtyMinutes();`          | 30분마다 실행.                                       |
| `->hourly();`                      | 매시간 실행.                                        |
| `->hourlyAt(17);`                  | 매시간 17분에 실행.                                  |
| `->everyOddHour($minutes = 0);`   | 홀수시간마다 실행.                                   |
| `->everyTwoHours($minutes = 0);`  | 2시간마다 실행.                                      |
| `->everyThreeHours($minutes = 0);`| 3시간마다 실행.                                      |
| `->everyFourHours($minutes = 0);` | 4시간마다 실행.                                      |
| `->everySixHours($minutes = 0);`  | 6시간마다 실행.                                      |
| `->daily();`                       | 매일 자정에 실행.                                    |
| `->dailyAt('13:00');`              | 매일 13시에 실행.                                    |
| `->twiceDaily(1, 13);`             | 매일 1시와 13시에 실행.                              |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1시 15분과 13시 15분에 실행.                    |
| `->weekly();`                      | 매주 일요일 00:00에 실행.                            |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8시에 실행.                              |
| `->monthly();`                     | 매월 1일 00:00에 실행.                               |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15시에 실행.                                |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일과 16일 13시에 실행.                         |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15시에 실행.                          |
| `->quarterly();`                   | 매분기 첫째 날 00:00에 실행.                         |
| `->quarterlyOn(4, '14:00');`       | 매분기 4일 14시에 실행.                              |
| `->yearly();`                      | 매년 1월 1일 00:00에 실행.                           |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17시에 실행.                            |
| `->timezone('America/New_York');`  | 작업을 적용할 시간대 설정.                           |

</div>

이 메서드들은 추가 제약 조건과 결합해 특정 요일에만 작동하는 더 세밀한 예약 구성이 가능합니다. 예를 들어, 매주 월요일에 명령어를 실행하도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 오후 1시에 한 번 실행...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시 사이에 매 시간 실행...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

아래는 추가 가능한 스케줄 제약 조건 목록입니다:

<div class="overflow-auto">

| 메서드                             | 설명                                             |
| -------------------------------- | ------------------------------------------------- |
| `->weekdays();`                  | 평일에만 작업 실행 제한.                          |
| `->weekends();`                  | 주말에만 작업 실행 제한.                          |
| `->sundays();`                   | 일요일에만 작업 실행 제한.                        |
| `->mondays();`                   | 월요일에만 작업 실행 제한.                        |
| `->tuesdays();`                  | 화요일에만 작업 실행 제한.                        |
| `->wednesdays();`                | 수요일에만 작업 실행 제한.                        |
| `->thursdays();`                 | 목요일에만 작업 실행 제한.                        |
| `->fridays();`                   | 금요일에만 작업 실행 제한.                        |
| `->saturdays();`                 | 토요일에만 작업 실행 제한.                        |
| `->days(array\|mixed);`          | 특정 요일만 작업 실행 제한.                       |
| `->between($startTime, $endTime);` | 특정 시간 구간 내에서만 작업 실행 제한.             |
| `->unlessBetween($startTime, $endTime);` | 특정 시간 구간 내에서는 작업 실행 제외.            |
| `->when(Closure);`               | 조건식이 참일 때만 작업 실행 제한.                |
| `->environments($env);`          | 특정 환경에서만 작업 실행 제한.                    |

</div>

<a name="day-constraints"></a>
#### 요일 제약 조건 (Day Constraints)

`days` 메서드는 작업 실행을 특정 요일로 제한할 때 사용합니다. 예를 들어, 일요일과 수요일에만 매 시간 실행하도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는 `Illuminate\Console\Scheduling\Schedule` 클래스에 정의된 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간 구간 제약 조건 (Between Time Constraints)

`between` 메서드는 작업 실행을 하루 중 특정 시간 구간으로 제한합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로, `unlessBetween` 메서드는 작업 실행을 특정 시간 구간에서 제외하고자 할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건식 제약 조건 (Truth Test Constraints)

`when` 메서드는 작업 실행 여부를 특정 조건식(클로저) 반환 값에 따라 제한합니다. 조건식이 `true`를 반환하면, 다른 제약 조건에 의해 실행이 막히지 않는 한 작업이 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`의 반대로, 조건식이 `true`일 경우 작업 실행을 건너뜁니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

`when` 메서드가 여러 개 체이닝된 경우, 모든 조건이 `true`일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 조건 (Environment Constraints)

`environments` 메서드는 작업이 특정 환경(`APP_ENV` [환경 변수](/docs/master/configuration#environment-configuration) 값)에서만 실행되도록 제한할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 시간대 설정 (Timezones)

`timezone` 메서드를 사용하면 예약된 작업의 실행 시간을 특정 시간대로 해석하도록 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 예약 작업에 동일한 시간대를 반복해서 지정한다면, 애플리케이션의 `app` 구성 파일에서 `schedule_timezone` 옵션을 설정해 전역 시간대를 지정할 수 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 시간대는 일광 절약 시간제(Daylight Saving Time)를 사용합니다. 이 때문에 일광 절약 시간이 바뀌는 시점에는 작업이 두 번 실행되거나 아예 실행되지 않을 수 있습니다. 가능한 경우 시간대 지정 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 실행 방지 (Preventing Task Overlaps)

기본적으로 예약 작업은 이전 작업이 아직 실행 중이어도 새 인스턴스를 실행합니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

위 예제에서 `emails:send` Artisan 명령어는 현재 실행 중이 아니면 매분 실행됩니다. `withoutOverlapping`은 실행 시간이 크게 변동되는 작업에 유용해, 실행 시간이 얼마나 걸릴지 예측하기 어려운 경우에도 중복 실행을 막을 수 있습니다.

만약 중복 방지 자물쇠(lock)가 만료되기까지 기다릴 시간을 분 단위로 지정하려면, 기본 24시간 대신 원하는 시간을 전달할 수 있습니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

`withoutOverlapping`은 애플리케이션의 [캐시](/docs/master/cache)를 이용해 락을 관리합니다. 필요 시 `schedule:clear-cache` Artisan 명령어로 캐시 락을 초기화할 수 있으며, 이는 일반적으로 서버 문제로 인해 작업이 중단되어 락이 해제되지 못한 경우에 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서 작업 실행하기 (Running Tasks on One Server)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis` 여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

여러 서버에서 스케줄러가 실행 중일 경우, 특정 작업을 단일 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤에 새 보고서를 생성하는 스케줄 작업이 있다고 가정합시다. 만약 스케줄러가 세 개의 워커 서버에서 실행 중이라면, 이 작업이 세 서버 모두에서 중복 실행되어 세 번 보고서가 생성됩니다. 이는 원치 않는 결과입니다.

해당 작업이 한 서버에서만 실행되도록 하려면, 스케줄 정의 시 `onOneServer` 메서드를 사용합니다. 작업을 가장 먼저 획득한 서버가 원자적 락을 걸어 동시에 다른 서버에서 실행되지 않도록 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 이름 지정하기 (Naming Single Server Jobs)

같은 작업을 인자가 다른 여러 형태로 스케줄링하더라도 각 작업을 한 서버에서만 실행하려는 경우, `name` 메서드로 각 작업 정의에 고유 이름을 지정할 수 있습니다:

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

마찬가지로, 한 서버에서 실행할 클로저 작업도 반드시 이름을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업 (Background Tasks)

기본적으로 동시에 실행되는 여러 작업은 정의된 순서대로 순차 실행됩니다. 실행 시간이 긴 작업이 있으면 뒤따르는 작업이 예상보다 뒤로 밀릴 수 있습니다. 작업들을 동시에 병렬 실행하려면, `runInBackground` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command` 또는 `exec` 메서드로 예약한 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드 (Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/master/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 서버 유지보수를 방해하지 않기 위함입니다. 하지만 유지보수 모드에서도 특정 작업을 강제로 실행하고 싶으면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하세요:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹 (Schedule Groups)

비슷한 설정을 공유하는 여러 예약 작업을 정의할 때, 작업 그룹 기능을 사용하면 각 작업마다 반복해서 설정을 작성하지 않아도 되어 편리하고 코드가 간결해집니다.

그룹을 생성하려면 원하는 공통 설정 메서드를 호출 후 `group` 메서드를 호출하고, 클로저 내에 그룹에 포함할 작업들을 정의합니다:

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

이제 예약 작업 정의 방법을 알았으니, 실제 서버에서 작업을 실행하는 방법을 살펴보겠습니다. `schedule:run` Artisan 명령어는 현재 서버 시간에 따라 모든 예약 작업을 검사해 실행할 작업을 결정합니다.

Laravel 스케줄러를 사용할 때는 서버에 단 하나의 cron 항목만 추가하면 되며, 매분 `schedule:run` 명령어를 호출하도록 설정합니다. 서버에 cron 항목을 추가하는 방법을 모른다면, [Laravel Cloud](https://cloud.laravel.com) 같은 관리형 플랫폼을 활용해 예약 작업 실행을 맡길 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 작업 (Sub-Minute Scheduled Tasks)

대부분 운영체제에서 cron 작업은 1분마다 최대 한 번 실행됩니다. 그러나 Laravel 스케줄러는 작업을 1초 간격으로도 실행할 수 있도록 허용합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

1분 미만 간격 작업이 정의된 경우, `schedule:run` 명령어는 즉시 종료하지 않고 현재 분이 끝날 때까지 계속 실행되면서 필요한 하위 분 작업을 모두 수행합니다.

1분 미만 간격 작업이 예상보다 오래 걸리면 뒤이어 대기 중인 작업 실행이 지연될 수 있으므로, 이 경우 모든 하위 분 작업을 큐에 넣거나 백그라운드 명령으로 처리하는 것이 권장됩니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 하위 분 작업 중단하기 (Interrupting Sub-Minute Tasks)

`sub-minute` 작업이 정의된 경우, `schedule:run` 명령어는 실행 1분 동안 계속 동작합니다. 따라서 배포할 때 이미 실행 중인 `schedule:run` 인스턴스가 기존 코드를 계속 사용하다가 새 배포가 반영되지 않는 문제가 발생할 수 있습니다.

이를 방지하려면 배포 스크립트에 `schedule:interrupt` 명령어를 추가해 현재 실행 중인 `schedule:run` 인스턴스를 중단시킬 수 있습니다. 배포가 완료된 이후에 호출하면 됩니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기 (Running the Scheduler Locally)

로컬 개발 환경에서는 보통 cron 항목을 따로 등록하지 않고, 대신 `schedule:work` Artisan 명령어를 사용합니다. 이 명령어는 포그라운드에서 실행되며, 종료할 때까지 매분 스케줄러를 호출합니다. 1분 미만 간격 작업이 있을 경우에도 이를 계속 처리합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

Laravel 스케줄러는 예약 작업이 생성하는 출력을 편리하게 다룰 수 있도록 여러 메서드를 제공합니다. 먼저 `sendOutputTo` 메서드를 사용해서 출력을 파일에 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력을 기존 파일에 덧붙이려면 `appendOutputTo` 메서드를 사용하세요:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 이용하면 작업의 출력을 지정한 이메일 주소로 보낼 수 있습니다. 이메일 발송 전에 Laravel의 [이메일 서비스](/docs/master/mail)를 적절히 설정해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

종료 코드가 0이 아닌 실패 상태일 때만 출력 이메일을 보내려면 `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드로 예약한 작업에만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 후크 (Task Hooks)

`before` 와 `after` 메서드를 사용하면 예약 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업 실행 직전 수행...
    })
    ->after(function () {
        // 작업 실행 직후 수행...
    });
```

`onSuccess` 와 `onFailure` 메서드를 사용하면 예약 작업이 성공하거나 실패했을 때 실행할 코드를 정의할 수 있습니다. 실패란 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드를 반환한 경우를 의미합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업 성공 시 처리...
    })
    ->onFailure(function () {
        // 작업 실패 시 처리...
    });
```

명령어 출력이 존재한다면, `after`, `onSuccess`, `onFailure` 후크에서 `Illuminate\Support\Stringable` 타입 힌트를 `$output` 인자로 지정해 출력 내용을 받을 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업 성공 시 처리...
    })
    ->onFailure(function (Stringable $output) {
        // 작업 실패 시 처리...
    });
```

<a name="pinging-urls"></a>
#### URL 핑 전송하기 (Pinging URLs)

`schedule` 메서드에는 작업 실행 전후에 외부 URL을 자동으로 핑하는 기능이 있습니다. 이 기능은 [Envoyer](https://envoyer.io) 같은 외부 서비스에 작업 시작 또는 종료를 알리고자 할 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess` 와 `pingOnFailure` 메서드는 작업이 성공하거나 실패했을 때만 URL을 핑합니다. 실패는 명령어 종료 코드가 0이 아닌 경우입니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 해당 조건이 `true`일 때만 URL을 핑합니다:

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

Laravel은 예약 과정 중 다음과 같은 다양한 [이벤트](/docs/master/events)를 발생시킵니다. 아래 이벤트들에 대해 [리스너](/docs/master/events)를 정의할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                              |
| -------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting` |
| `Illuminate\Console\Events\ScheduledTaskFinished` |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped` |
| `Illuminate\Console\Events\ScheduledTaskFailed` |

</div>