# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [쉘 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [시간대 설정](#timezones)
    - [작업 중복 실행 방지](#preventing-task-overlaps)
    - [단일 서버에서 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행하기](#running-the-scheduler)
    - [1분 미만 간격 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [작업 출력 처리](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 예약해야 하는 각 작업에 대해 cron 설정 항목을 작성했을 것입니다. 하지만 이렇게 되면 작업 스케줄이 소스 관리에서 분리되고, 기존 cron 항목을 보거나 추가하기 위해 서버에 SSH 접속해야 하는 번거로움이 빠르게 발생합니다.

Laravel의 명령어 스케줄러는 서버에서 예약 작업을 관리하는 새로운 방식을 제공합니다. 이 스케줄러를 사용하면 Laravel 애플리케이션 내에서 명령어 스케줄을 유창하고 명확하게 정의할 수 있습니다. 스케줄러를 사용할 때는 서버의 cron에 단 하나의 항목만 등록하면 되고, 작업 스케줄 정의는 보통 애플리케이션의 `routes/console.php` 파일에 작성합니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에서 정의할 수 있습니다. 시작하기 위해, 매일 자정에 실행되는 클로저를 스케줄링하고, 그 내부에서 테이블을 비우는 데이터베이스 쿼리를 실행하는 예제부터 살펴보겠습니다:

```
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 이용한 스케줄링 외에도, [`__invoke` 메서드를 가진 호출 가능한 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 이용해 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함한 간단한 PHP 클래스입니다:

```
Schedule::call(new DeleteRecentUsers)->daily();
```

`routes/console.php`를 명령어 정의 용도로만 남기고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용해 스케줄 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 인자로 받는 클로저를 정의합니다:

```
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

정의된 예약 작업과 다음 실행 시간이 궁금할 때는, `schedule:list` Artisan 명령어를 사용해 개요를 확인할 수 있습니다:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저뿐 아니라 [Artisan 명령어](/docs/11.x/artisan)와 시스템 명령어도 스케줄링할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 명령어 이름이나 클래스 이름으로 Artisan 명령어를 스케줄링할 수 있습니다.

클래스 이름을 사용해 Artisan 명령어를 스케줄링할 때는, 명령어 호출 시 전달할 추가 커맨드라인 인수를 배열로 넘길 수 있습니다:

```
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Artisan 클로저 명령어 스케줄링

클로저로 정의한 Artisan 명령어를 스케줄링하려면, 명령어 정의 뒤에 스케줄 관련 메서드를 체이닝하면 됩니다:

```
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달해야 할 경우 `schedule` 메서드에 인수를 넣습니다:

```
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드를 이용하면 [큐 작업](/docs/11.x/queues)을 스케줄링할 수 있습니다. 이 방법은 클로저를 사용해 작업을 큐에 넣는 대신 간편하게 큐 작업을 예약할 수 있는 방법입니다:

```
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드에는 옵션으로 두 번째와 세 번째 인수를 넣어 큐 이름과 큐 커넥션을 지정할 수 있습니다:

```
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "sqs" 커넥션의 "heartbeats" 큐에 작업을 디스패치...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 쉘 명령어 스케줄링

`exec` 메서드를 사용하면 운영체제에 쉘 명령어를 직접 실행하도록 예약할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

지금까지 몇 가지 예로 지정한 간격마다 작업을 실행하는 방법을 살펴봤습니다. Laravel은 매우 다양한 빈도 옵션을 제공하여 스케줄링 가능하게 합니다:

<div class="overflow-auto">

| 메서드                             | 설명                                              |
| ---------------------------------- | ------------------------------------------------- |
| `->cron('* * * * *');`             | 직접 크론 형식으로 스케줄을 지정합니다.            |
| `->everySecond();`                 | 매초 작업을 실행합니다.                           |
| `->everyTwoSeconds();`             | 2초마다 작업을 실행합니다.                        |
| `->everyFiveSeconds();`            | 5초마다 작업을 실행합니다.                        |
| `->everyTenSeconds();`             | 10초마다 작업을 실행합니다.                       |
| `->everyFifteenSeconds();`         | 15초마다 작업을 실행합니다.                       |
| `->everyTwentySeconds();`          | 20초마다 작업을 실행합니다.                       |
| `->everyThirtySeconds();`          | 30초마다 작업을 실행합니다.                       |
| `->everyMinute();`                 | 매분 작업을 실행합니다.                           |
| `->everyTwoMinutes();`             | 2분마다 작업을 실행합니다.                        |
| `->everyThreeMinutes();`           | 3분마다 작업을 실행합니다.                        |
| `->everyFourMinutes();`            | 4분마다 작업을 실행합니다.                        |
| `->everyFiveMinutes();`            | 5분마다 작업을 실행합니다.                        |
| `->everyTenMinutes();`             | 10분마다 작업을 실행합니다.                       |
| `->everyFifteenMinutes();`         | 15분마다 작업을 실행합니다.                       |
| `->everyThirtyMinutes();`          | 30분마다 작업을 실행합니다.                       |
| `->hourly();`                      | 매시간 작업을 실행합니다.                         |
| `->hourlyAt(17);`                  | 매 시간 17분에 작업을 실행합니다.                 |
| `->everyOddHour($minutes = 0);`    | 홀수 시간마다 작업을 실행합니다.                   |
| `->everyTwoHours($minutes = 0);`   | 두 시간 간격으로 작업을 실행합니다.                |
| `->everyThreeHours($minutes = 0);` | 세 시간 간격으로 작업을 실행합니다.                |
| `->everyFourHours($minutes = 0);`  | 네 시간 간격으로 작업을 실행합니다.                |
| `->everySixHours($minutes = 0);`   | 여섯 시간 간격으로 작업을 실행합니다.              |
| `->daily();`                       | 매일 자정에 작업을 실행합니다.                      |
| `->dailyAt('13:00');`              | 매일 13시에 작업을 실행합니다.                     |
| `->twiceDaily(1, 13);`             | 매일 1시와 13시에 작업을 실행합니다.              |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1시 15분과 13시 15분에 작업을 실행합니다.     |
| `->weekly();`                      | 매주 일요일 자정에 작업을 실행합니다.              |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8시에 작업을 실행합니다.               |
| `->monthly();`                     | 매월 1일 자정에 작업을 실행합니다.                  |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15시에 작업을 실행합니다.                  |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일과 16일 13시에 작업을 실행합니다.           |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15시에 작업을 실행합니다.            |
| `->quarterly();`                   | 매 분기 첫 날 자정에 작업을 실행합니다.              |
| `->quarterlyOn(4, '14:00');`       | 매 분기 4일 14시에 작업을 실행합니다.                |
| `->yearly();`                      | 매년 1월 1일 자정에 작업을 실행합니다.              |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17시에 작업을 실행합니다.              |
| `->timezone('America/New_York');`  | 작업을 해당 시간대 기준으로 실행하도록 설정합니다.   |

</div>

이런 메서드들은 추가 제약 조건과 조합하여 특정 요일에만 실행하는 등 더욱 세밀한 스케줄링을 만들 수 있습니다. 예를 들어, 월요일마다 한 번씩 실행하는 명령어를 스케줄링할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 13시에 실행...
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

추가 지원하는 스케줄 제약 조건 목록은 다음과 같습니다:

<div class="overflow-auto">

| 메서드                                   | 설명                                              |
| ---------------------------------------- | ------------------------------------------------- |
| `->weekdays();`                          | 평일에만 작업을 제한합니다.                        |
| `->weekends();`                          | 주말에만 작업을 제한합니다.                        |
| `->sundays();`                           | 일요일에만 작업을 제한합니다.                      |
| `->mondays();`                           | 월요일에만 작업을 제한합니다.                      |
| `->tuesdays();`                          | 화요일에만 작업을 제한합니다.                      |
| `->wednesdays();`                        | 수요일에만 작업을 제한합니다.                      |
| `->thursdays();`                         | 목요일에만 작업을 제한합니다.                      |
| `->fridays();`                           | 금요일에만 작업을 제한합니다.                      |
| `->saturdays();`                         | 토요일에만 작업을 제한합니다.                      |
| `->days(array\|mixed);`                  | 특정한 요일에만 작업을 제한합니다.                 |
| `->between($startTime, $endTime);`       | 지정한 시간대에만 작업 실행을 제한합니다.           |
| `->unlessBetween($startTime, $endTime);` | 지정한 시간대에는 작업 실행을 제외합니다.           |
| `->when(Closure);`                       | 주어진 조건이 참일 때만 작업을 실행합니다.          |
| `->environments($env);`                  | 지정한 환경에서만 작업을 실행합니다.                |

</div>

<a name="day-constraints"></a>
#### 요일 제약 조건

`days` 메서드를 이용하면 작업 실행을 특정 요일로 제한할 수 있습니다. 예를 들어, 일요일과 수요일에 시간 단위로 작업을 실행하려면 다음과 같이 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는 `Illuminate\Console\Scheduling\Schedule` 클래스에 정의된 상수를 사용해 요일을 지정할 수도 있습니다:

```
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 특정 시간대 제약 조건

`between` 메서드는 작업 실행을 하루 중 특정 시간대로 제한하는 데 사용할 수 있습니다:

```
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로 `unlessBetween` 메서드는 특정 시간대에는 작업을 실행하지 않도록 할 때 사용합니다:

```
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건 검사 제약 조건

`when` 메서드를 사용하면, 특정 조건을 만족할 때만 작업을 실행하도록 제한할 수 있습니다. 주어진 클로저가 `true`를 반환할 때 작업을 실행하며, 다른 제약 조건에 걸리지 않은 경우 실행됩니다:

```
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`과 반대 개념으로, `true`를 반환하면 작업 실행을 생략합니다:

```
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

체이닝된 여러 `when` 메서드를 사용할 경우 모든 조건이 `true`일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 조건

`environments` 메서드를 사용하면, [환경 변수](/docs/11.x/configuration#environment-configuration) `APP_ENV`에 따라 특정 환경에서만 작업을 실행할 수 있습니다:

```
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 시간대 설정

`timezone` 메서드를 사용하면 스케줄 작업 시간을 특정 시간대 기준으로 설정할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 작업에 같은 시간대를 반복하여 지정한다면, 애플리케이션 `app` 설정 파일 내 `schedule_timezone` 옵션으로 시간대를 통일할 수 있습니다:

```
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]  
> 일부 시간대는 서머타임 제도를 사용합니다. 서머타임 변경 시 작업이 두 번 실행되거나 실행되지 않을 수 있으므로, 될 수 있으면 시간대 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 실행 방지

기본적으로 예약된 작업은 이전 작업이 아직 실행 중이어도 새로 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

위 예제에서 `emails:send` Artisan 명령어는 현재 실행 중이지 않을 때만 매분 실행됩니다. `withoutOverlapping`은 실행 시간이 다양해 예측이 어려운 작업에 특히 유용합니다.

필요 시, 중복 실행 방지 잠금이 풀리기까지 걸리는 분 단위 시간도 지정할 수 있습니다. 기본값은 24시간입니다:

```
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping`은 애플리케이션의 [캐시](/docs/11.x/cache)를 통해 잠금을 관리합니다. 서버 문제로 잠금이 풀리지 않는 경우, `schedule:clear-cache` Artisan 명령어로 캐시 잠금을 강제로 해제할 수 있습니다.

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 작업 실행

> [!WARNING]  
> 이 기능을 사용하려면, 애플리케이션 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis`여야 하며, 모든 서버가 동일 중앙 캐시 서버와 통신 중이어야 합니다.

스케줄러가 여러 서버에서 실행될 경우, 작업이 단일 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤에 보고서를 생성하는 작업이 세 개 서버에서 실행된다면 보고서가 세 번 생성되므로 바람직하지 않습니다.

이때 `onOneServer` 메서드를 사용해 작업이 하나의 서버에서만 실행되도록 지정할 수 있습니다. 가장 먼저 작업을 획득한 서버가 다른 서버 작업 실행을 방지하는 원자 잠금을 잡습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 고유 이름 부여하기

같은 작업을 서로 다른 매개변수로 여러 번 스케줄링하되, 각 변형이 단일 서버에서 실행되게 하려면 `name` 메서드로 스케줄 정의에 고유 이름을 지정하세요:

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

마찬가지로, 단일 서버에서 실행할 예정인 클로저 작업들도 이름을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로 동시에 예약된 여러 작업은 `schedule` 메서드 정의 순서대로 순차 실행됩니다. 만약 오래 걸리는 작업이 있다면 이후 작업이 예상보다 지연될 수 있습니다. 동시에 작업들을 백그라운드에서 실행하고 싶으면 `runInBackground` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]  
> `runInBackground` 메서드는 `command`와 `exec` 메서드를 이용해 스케줄링하는 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/11.x/configuration#maintenance-mode)일 때는 서버에 영향을 미칠 수 있으므로 예약 작업이 실행되지 않습니다. 그러나 유지보수 중에도 작업을 강제로 실행하고 싶다면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하세요:

```
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹

비슷한 설정이 공통적으로 적용되는 작업이 여러 개 있을 때, 작업 그룹 기능을 사용하면 중복되는 설정을 반복하지 않아도 됩니다. 작업 그룹을 만들려면 공통 설정 메서드를 체이닝한 뒤, `group` 메서드에 해당 설정이 적용될 작업들을 클로저 안에 정의하세요:

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
## 스케줄러 실행하기

스케줄 작업을 정의했으니, 이제 실제 서버에서 작업을 실행하는 방식을 알아보겠습니다. `schedule:run` Artisan 명령어는 현재 서버 시간을 기준으로 예약 작업을 평가해 실행할 필요가 있는지 판단합니다.

Laravel 스케줄러를 사용할 때는 서버 크론에 `schedule:run` 명령어를 1분마다 실행하는 단 한 줄의 크론 설정만 추가하면 됩니다. 서버에 크론 설정 추가 방법을 모른다면, [Laravel Forge](https://forge.laravel.com) 같은 서비스를 이용해 자동으로 관리할 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 작업

대부분 운영체제의 크론은 분 단위로만 실행이 가능합니다. 그러나 Laravel 스케줄러는 1초 단위로도 작업을 예약할 수 있게 지원합니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

서브 분 단위 스케줄 작업이 정의되면, `schedule:run` 명령은 바로 종료하지 않고 현재 분이 끝날 때까지 계속 실행되며 필요한 서브 분 작업들을 실행합니다.

서브 분 작업이 예상보다 오래 걸리면 뒤 작업 실행이 지연될 수 있으므로, 이런 작업들은 보통 큐 작업이나 백그라운드 커맨드를 디스패치하는 식으로 실행하는 것을 권장합니다:

```
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 서브 분 작업 중지하기

서브 분 작업이 정의된 상황에서는 `schedule:run` 명령이 실행된 분이 끝날 때까지 종료되지 않습니다. 배포 중에는 실행 중인 `schedule:run` 명령이 이전 버전 코드를 계속 사용할 수도 있기 때문에 중단이 필요할 수 있습니다.

이 때, 배포 스크립트의 완료 후 `schedule:interrupt` 명령을 실행해 진행 중인 `schedule:run` 명령을 중단하도록 설정하세요:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

보통 로컬 개발 환경에서는 크론에 스케줄러 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 실행해 스케줄러를 포그라운드에서 실행할 수 있습니다. 이 명령은 종료할 때까지 매 분 스케줄러를 호출하며, 서브 분 작업도 처리합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 처리

Laravel 스케줄러는 예약 작업의 출력을 다루기에 편리한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용하면 작업 출력물을 파일로 저장해 나중에 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력 내용을 기존 파일에 덧붙이고 싶으면 `appendOutputTo` 메서드를 사용하세요:

```
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드는 작업 출력을 원하는 이메일 주소로 전송합니다. 메일 전송 전에 Laravel의 [이메일 서비스](/docs/11.x/mail)를 반드시 설정해야 합니다:

```
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

예약된 Artisan 또는 시스템 명령어가 비정상 종료(0이 아닌 종료 코드)할 때만 이메일을 보내려면 `emailOutputOnFailure` 메서드를 사용하세요:

```
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]  
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`와 `exec` 메서드를 통해 스케줄링된 작업에만 사용 가능합니다.

<a name="task-hooks"></a>
## 작업 훅

`before`와 `after` 메서드를 사용하면 각 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업 실행 직전...
    })
    ->after(function () {
        // 작업 실행 직후...
    });
```

`onSuccess`와 `onFailure` 메서드는 작업이 성공하거나 실패했을 때 실행할 코드를 지정합니다. 실패는 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료했음을 의미합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업 성공...
    })
    ->onFailure(function () {
        // 작업 실패...
    });
```

명령어 출력이 있을 경우, `after`, `onSuccess`, `onFailure` 훅의 클로저 인자로 `Illuminate\Support\Stringable` 타입을 명시하면 출력값을 받을 수 있습니다:

```
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업 성공 후 출력 처리...
    })
    ->onFailure(function (Stringable $output) {
        // 작업 실패 후 출력 처리...
    });
```

<a name="pinging-urls"></a>
#### URL 호출(Ping)

`schedule` 메서드의 `pingBefore`와 `thenPing` 메서드를 이용하면 일정 작업 실행 전후에 외부 URL을 자동으로 호출할 수 있습니다. 예로 [Envoyer](https://envoyer.io) 같은 외부 서비스에 작업 시작과 완료를 알리는데 사용합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess`와 `pingOnFailure`는 작업 성공 또는 실패 시에만 URL을 호출합니다. 실패는 Artisan 또는 시스템 명령어가 비정상 종료한 것을 뜻합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 조건이 참일 때만 URL을 호출할 수 있게 합니다:

```
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

Laravel은 스케줄링 과정에서 다양한 [이벤트](/docs/11.x/events)를 발생시킵니다. 아래 이벤트 목록에 대한 리스너를 별도로 정의하여 확장할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Console\Events\ScheduledTaskStarting` |
| `Illuminate\Console\Events\ScheduledTaskFinished` |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped` |
| `Illuminate\Console\Events\ScheduledTaskFailed` |

</div>