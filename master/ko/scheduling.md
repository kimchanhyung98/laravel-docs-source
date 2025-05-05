```markdown
# 작업 스케줄링

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 방지](#preventing-task-overlaps)
    - [한 서버에서만 작업 실행하기](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행](#running-the-scheduler)
    - [1분 미만 간격의 작업 스케줄](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 후크](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 예약해야 하는 각 작업마다 크론(cron) 설정 항목을 직접 작성해야 했을 수 있습니다. 하지만 이렇게 하면 작업 스케줄이 소스 제어에서 벗어나고, 현재의 크론 항목을 확인하거나 추가하려면 서버에 SSH로 접속해야 하므로 번거롭게 됩니다.

Laravel의 명령 스케줄러는 서버에서 예약 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러는 명령 스케줄을 Laravel 애플리케이션 내에서 직관적이고 간결하게 정의할 수 있도록 해줍니다. 스케줄러를 사용하면 서버에 단 하나의 크론(corn) 항목만 추가하면 됩니다. 일반적으로 모든 작업 스케줄은 애플리케이션의 `routes/console.php` 파일에 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에서 정의할 수 있습니다. 먼저 예제를 살펴보겠습니다. 이 예제에서는 매일 자정에 호출되는 클로저(익명 함수)를 예약하고, 해당 클로저 내부에서 데이터베이스 테이블을 비우는 쿼리를 실행합니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 이용한 작업 예약 외에도, [호출 가능(Invokable) 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 예약할 수도 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다.

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

`routes/console.php` 파일을 명령 정의 용도로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용하여 예약 작업을 정의할 수도 있습니다. 이 메서드는 스케줄러 인스턴스를 인자로 받는 클로저를 인수로 받습니다.

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

예약된 작업 목록과 다음 실행 예정 시간을 확인하려면, `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령 스케줄링

클로저뿐만 아니라 [Artisan 명령](/docs/{{version}}/artisan)이나 시스템 명령도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용해 명령 이름이나 클래스명을 통해 Artisan 명령을 예약할 수 있습니다.

클래스명을 이용하여 Artisan 명령을 예약할 때는 명령이 실행될 때 사용할 추가 명령행 인자를 배열로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### 클로저 기반 Artisan 명령 스케줄링

클로저로 정의된 Artisan 명령을 예약하려면, 명령 정의 후 예약 관련 메서드를 메서드 체이닝으로 연결합니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령에 인자를 전달해야 하는 경우에는 `schedule` 메서드에 인자를 배열로 제공하면 됩니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드는 [큐 작업](/docs/{{version}}/queues)을 예약하는 데 사용할 수 있습니다. 이 메서드는 작업을 예약하기 위해 매번 클로저 내부에서 작업을 큐에 넣는 번거로움 없이 간결하게 정의할 수 있게 해줍니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드의 두 번째와 세 번째 인자를 사용하여, 작업을 큐할 때 사용할 큐 이름과 큐 연결(Connection)을 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "heartbeats" 큐에 "sqs" 연결로 작업을 디스패치합니다...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령 스케줄링

`exec` 메서드를 사용하면 운영체제 명령을 직접 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

작업 실행 빈도 예시를 이미 몇 가지 살펴보았지만, 그 외에도 다양한 빈도 옵션을 사용할 수 있습니다:

<div class="overflow-auto">

| 메서드                                   | 설명                                                      |
| ---------------------------------------- | ---------------------------------------------------------- |
| `->cron('* * * * *');`                   | 사용자 지정 크론 스케줄로 작업 실행                       |
| `->everySecond();`                       | 매초 작업 실행                                            |
| `->everyTwoSeconds();`                   | 2초마다 작업 실행                                         |
| `->everyFiveSeconds();`                  | 5초마다 작업 실행                                         |
| `->everyTenSeconds();`                   | 10초마다 작업 실행                                        |
| `->everyFifteenSeconds();`               | 15초마다 작업 실행                                        |
| `->everyTwentySeconds();`                | 20초마다 작업 실행                                        |
| `->everyThirtySeconds();`                | 30초마다 작업 실행                                        |
| `->everyMinute();`                       | 매분 작업 실행                                            |
| `->everyTwoMinutes();`                   | 2분마다 작업 실행                                         |
| `->everyThreeMinutes();`                 | 3분마다 작업 실행                                         |
| `->everyFourMinutes();`                  | 4분마다 작업 실행                                         |
| `->everyFiveMinutes();`                  | 5분마다 작업 실행                                         |
| `->everyTenMinutes();`                   | 10분마다 작업 실행                                        |
| `->everyFifteenMinutes();`               | 15분마다 작업 실행                                        |
| `->everyThirtyMinutes();`                | 30분마다 작업 실행                                        |
| `->hourly();`                            | 매시간 작업 실행                                          |
| `->hourlyAt(17);`                        | 매시간 17분에 작업 실행                                   |
| `->everyOddHour($minutes = 0);`          | 홀수 시간마다 작업 실행                                   |
| `->everyTwoHours($minutes = 0);`         | 2시간마다 작업 실행                                       |
| `->everyThreeHours($minutes = 0);`       | 3시간마다 작업 실행                                       |
| `->everyFourHours($minutes = 0);`        | 4시간마다 작업 실행                                       |
| `->everySixHours($minutes = 0);`         | 6시간마다 작업 실행                                       |
| `->daily();`                             | 매일 자정에 작업 실행                                     |
| `->dailyAt('13:00');`                    | 매일 13:00에 작업 실행                                    |
| `->twiceDaily(1, 13);`                   | 매일 1:00, 13:00에 작업 실행                              |
| `->twiceDailyAt(1, 13, 15);`             | 매일 1:15, 13:15에 작업 실행                              |
| `->weekly();`                            | 매주 일요일 00:00에 작업 실행                             |
| `->weeklyOn(1, '8:00');`                 | 매주 월요일 8:00에 작업 실행                              |
| `->monthly();`                           | 매월 1일 00:00에 작업 실행                                |
| `->monthlyOn(4, '15:00');`               | 매월 4일 15:00에 작업 실행                                |
| `->twiceMonthly(1, 16, '13:00');`        | 매월 1일, 16일 13:00에 작업 실행                          |
| `->lastDayOfMonth('15:00');`             | 매월 말일 15:00에 작업 실행                               |
| `->quarterly();`                         | 매분기 첫날 00:00에 작업 실행                             |
| `->quarterlyOn(4, '14:00');`             | 매분기 4일 14:00에 작업 실행                              |
| `->yearly();`                            | 매년 1월 1일 00:00에 작업 실행                            |
| `->yearlyOn(6, 1, '17:00');`             | 매년 6월 1일 17:00에 작업 실행                            |
| `->timezone('America/New_York');`        | 이 작업의 타임존을 설정                                   |

</div>

이러한 메서드들은 추가 제한 조건과 결합하여 특정 요일에만 작업을 실행하는 등 더욱 정교한 일정 설계를 할 수 있습니다. 예를 들어, 월요일마다 작업을 실행하도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 오후 1시에 한 번 실행...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 매시 실행...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

아래는 추가적인 스케줄 제약 조건 목록입니다:

<div class="overflow-auto">

| 메서드                                     | 설명                                              |
| ------------------------------------------ | ------------------------------------------------- |
| `->weekdays();`                            | 평일에만 작업 실행                                 |
| `->weekends();`                            | 주말에만 작업 실행                                 |
| `->sundays();`                             | 일요일에만 작업 실행                               |
| `->mondays();`                             | 월요일에만 작업 실행                               |
| `->tuesdays();`                            | 화요일에만 작업 실행                               |
| `->wednesdays();`                          | 수요일에만 작업 실행                               |
| `->thursdays();`                           | 목요일에만 작업 실행                               |
| `->fridays();`                             | 금요일에만 작업 실행                               |
| `->saturdays();`                           | 토요일에만 작업 실행                               |
| `->days(array|mixed);`                     | 명시한 특정 요일에만 작업 실행                     |
| `->between($startTime, $endTime);`         | 특정 시간대에만 작업 실행                          |
| `->unlessBetween($startTime, $endTime);`   | 특정 시간대에는 작업 실행 제외                     |
| `->when(Closure);`                         | 클로저에서 true 반환 시에만 작업 실행              |
| `->environments($env);`                    | 지정 환경에서만 작업 실행                          |

</div>

<a name="day-constraints"></a>
#### 요일 제약

`days` 메서드를 사용하면 작업 실행을 특정 요일로 제한할 수 있습니다. 예를 들어, 일요일과 수요일에 매시 작업을 실행하려면:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는, 작업 실행 요일 정의 시 `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간대 제약

`between` 메서드를 사용하여 시간대별로 작업 실행을 제한할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로, `unlessBetween` 메서드를 사용하면 특정 시간대에는 작업 실행을 제외할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건부 제약

`when` 메서드는 주어진 클로저의 반환값이 true일 때만 작업이 실행되도록 제한합니다. 즉, 클로저가 true를 반환하고 다른 제약이 없는 한 작업이 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`의 반대입니다. `skip` 메서드가 true를 반환하면 해당 작업이 실행되지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

여러 개의 `when` 메서드를 체이닝하여 사용할 경우, 모든 조건이 true여야 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약

`environments` 메서드는 [환경 변수](/docs/{{version}}/configuration#environment-configuration) `APP_ENV`로 정의된 특정 환경에서만 작업이 실행되도록 할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존

`timezone` 메서드를 사용해 예약 작업의 실행 시점이 특정 타임존을 기준으로 해석되도록 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 예약 작업에 항상 동일한 타임존을 지정해야 할 경우, 애플리케이션의 `app` 설정 파일에 `schedule_timezone` 옵션을 지정할 수도 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 썸머타임(일광 절약제)을 적용하므로, 썸머타임 변경 시 스케줄된 작업이 두 번 실행되거나 아예 실행되지 않을 수 있습니다. 가능하다면 타임존 스케줄링은 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 방지

기본적으로 예약 작업은 이전 인스턴스가 아직 실행 중이더라도 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

위 예에서, `emails:send` [Artisan 명령](/docs/{{version}}/artisan)은 아직 실행 중이 아니라면 매분 실행됩니다. `withoutOverlapping`은 실행 시간이 일정하지 않은 작업의 경우 유용하게 사용할 수 있습니다.

필요하다면 중복 방지(lock) 유지 시간을 분 단위로 지정할 수 있습니다. 기본 유지 시간은 24시간입니다.

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

이 기능은 애플리케이션의 [캐시](/docs/{{version}}/cache)를 활용해 락을 관리합니다. 작업이 서버 문제 등으로 중단되어 락이 해제되지 않는다면, `schedule:clear-cache` Artisan 명령으로 락을 해제할 수 있습니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서만 작업 실행하기

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, `redis` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

스케줄러가 여러 서버에서 실행 중이라면, 특정 작업을 단 한 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 금요일 밤마다 새 보고서를 생성하는 작업이 세 대의 워커 서버에서 각각 실행된다면, 보고서가 세 번 생성됩니다. 이는 바람직하지 않습니다!

`onOneServer` 메서드를 사용하여 첫 번째로 락을 획득한 서버가 유일하게 해당 작업을 실행하도록 할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 이름 지정

파라미터별로 동일한 잡을 여러 번 예약하되 각각이 한 서버에서만 실행되도록 하려면, `name` 메서드로 각 예약 정의에 고유한 이름을 부여합니다:

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

마찬가지로, 한 서버에서만 실행하도록 설정하려는 클로저 예약 작업도 반드시 이름을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로 동일 시점에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서대로 순차적으로 실행됩니다. 작업 시간이 긴 작업이 있다면, 뒤의 작업 시작이 지연될 수 있습니다. 여러 작업을 백그라운드에서 동시에 실행하고 싶다면 `runInBackground` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground`는 `command`와 `exec` 메서드를 통해 예약한 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

[유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)에서는 예약 작업이 실행되지 않습니다. 이는 서버 정비 도중 수행 중인 작업이 간섭받는 것을 방지하기 위함입니다. 하지만, 유지보수 모드에도 불구하고 작업을 강제로 실행하고 싶다면 `evenInMaintenanceMode` 메서드를 사용하면 됩니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹

유사한 설정을 갖는 예약 작업이 다수 있을 경우, 작업 그룹핑 기능을 활용해 중복 설정 작성을 방지할 수 있습니다. 그룹핑은 코드를 간결하게 하고 관련 작업 간 일관성을 보장합니다.

그룹을 만들 때에는 원하는 설정 메서드를 연결한 뒤, `group` 메서드로 묶고, 공유 설정을 갖는 작업들을 클로저 내에서 정의합니다:

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
## 스케줄러 실행

이제 예약 작업을 정의했으니, 실제 서버에서 어떻게 실행하는지 살펴보겠습니다. `schedule:run` Artisan 명령은 현재 서버 시간 기준으로 예약된 모든 작업의 실행 필요 여부를 평가합니다.

따라서 Laravel의 스케줄러를 사용할 땐, 단 하나의 크론 항목을 추가하여 매분마다 `schedule:run` 명령을 실행하도록 하면 됩니다. 크론 설정 방법을 잘 모른다면, [Laravel Cloud](https://cloud.laravel.com) 와 같은 관리형 플랫폼을 사용하면 예약 작업 실행을 자동으로 관리할 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격의 작업 스케줄

대부분의 운영체제에서 크론 작업은 최소 1분 간격으로만 실행할 수 있습니다. 하지만 Laravel 스케줄러는 1초 간격 등 더 짧은 주기로 작업을 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

1분 미만 작업이 정의되어 있으면, `schedule:run` 명령은 바로 종료하지 않고 현재 분이 끝날 때까지 계속 실행됩니다. 이를 통해 한 분 동안 필요한 모든 하위(minute 내) 작업을 실행할 수 있습니다.

실행에 시간이 오래 걸리는 하위 작업으로 인해 후속 작업 실행 지연이 발생할 수 있으므로, 하위 작업은 실제 작업 처리를 큐 작업이나 백그라운드 실행 방식으로 넘기는 것이 좋습니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 실행 중단

하위 작업이 정의된 경우 `schedule:run` 명령이 한 분 동안 계속 실행되므로, 애플리케이션 배포 시 이를 강제로 중단해야 할 때가 있습니다. 이미 실행 중인 프로세스가 있을 경우, 최신 코드가 배포되어도 그 분이 끝날 때까지 이전 코드를 계속 사용하게 됩니다.

진행 중인 `schedule:run`을 중단하려면, 배포 스크립트에 다음과 같이 `schedule:interrupt` 명령을 추가하세요. 이 명령은 배포 작업 후에 실행해야 합니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기

로컬 개발 머신에는 보통 크론 항목을 추가하지 않습니다. 대신, `schedule:work` Artisan 명령을 사용하여 실행하면, 명령이 종료될 때까지 매분 스케줄러가 포그라운드에서 동작합니다. 하위(1분 미만) 작업이 정의되어 있을 경우, 매분 그 안에서 연속적으로 처리됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약 작업의 출력 결과를 쉽게 다룰 수 있는 여러 메서드를 제공합니다. 우선, `sendOutputTo` 메서드를 사용하여 작업 출력을 파일로 보낼 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력을 파일에 덧붙이고 싶다면 `appendOutputTo` 메서드를 사용하면 됩니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 작업 출력 결과를 원하는 이메일로 전송할 수 있습니다. 이 기능을 사용하기 전에 Laravel의 [이메일 서비스](/docs/{{version}}/mail)를 반드시 구성해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

만약 예약된 Artisan 또는 시스템 명령이 실패(비정상 종료, exit code 0이 아님)했을 때만 이메일을 보내길 원한다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo`는 `command` 및 `exec` 메서드를 통해 예약된 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 후크

`before` 및 `after` 메서드를 사용하면 예약 작업이 실행되기 전후에 실행할 코드를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업 실행 전
    })
    ->after(function () {
        // 작업 실행 후
    });
```

`onSuccess`와 `onFailure` 메서드는 작업이 성공했거나 실패했을 때 실행할 코드를 지정합니다. "실패"란 Artisan 또는 시스템 명령이 비정상 종료(0이 아닌 종료 코드)될 때를 의미합니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업 성공 후 코드
    })
    ->onFailure(function () {
        // 작업 실패 후 코드
    });
```

명령에서 출력(Output)이 발생했다면, 훅(후크) 클로저 정의의 `$output` 인자로 `Illuminate\Support\Stringable` 인스턴스를 타입힌트하여 해당 출력을 활용할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 성공시 출력값 활용
    })
    ->onFailure(function (Stringable $output) {
        // 실패시 출력값 활용
    });
```

<a name="pinging-urls"></a>
#### URL 핑(Ping) 보내기

`pingBefore`와 `thenPing` 메서드를 사용하면, 작업 실행 전/후에 지정된 URL로 자동으로 핑(Ping) 요청을 보낼 수 있습니다. 이는 외부 서비스(예: [Envoyer](https://envoyer.io))에 예약 작업 시작 또는 종료를 알릴 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess`와 `pingOnFailure`는 작업이 성공 또는 실패했을 때만 URL로 핑을 보냅니다(실패: 0이 아닌 종료 코드):

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 지정 조건이 true일 때만 해당 URL로 핑을 보냅니다:

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
## 이벤트

Laravel은 스케줄링 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 다음 이벤트에 대해 [리스너를 정의](/docs/{{version}}/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Console\Events\ScheduledTaskStarting` |
| `Illuminate\Console\Events\ScheduledTaskFinished` |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped` |
| `Illuminate\Console\Events\ScheduledTaskFailed` |

</div>
```
