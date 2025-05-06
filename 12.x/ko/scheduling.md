# 작업 스케줄링

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 방지](#preventing-task-overlaps)
    - [단일 서버에서 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [점검 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행하기](#running-the-scheduler)
    - [1분 미만 간격 스케줄](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 스케줄링해야 하는 각 작업마다 크론(cron) 설정을 직접 작성했을 수도 있습니다. 하지만 이런 방식은 작업 스케줄이 소스 코드 관리에서 벗어나게 되며, 기존 크론 엔트리를 확인하거나 추가하려면 매번 SSH로 서버에 접속해야 하므로 매우 불편합니다.

Laravel의 명령어 스케줄러는 서버에서 예약된 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내에서 명령어 스케줄을 간결하고 명확하게 정의할 수 있습니다. 스케줄러를 사용할 때 서버에는 오직 하나의 크론 엔트리만 필요합니다. 작업 스케줄은 일반적으로 애플리케이션의 `routes/console.php` 파일에 정의됩니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 먼저 예시를 살펴보겠습니다. 아래 예시에서는 매일 자정에 클로저를 호출하여 데이터베이스 테이블을 비우는 작업을 예약합니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 사용한 스케줄링 외에도 [호출 가능한(Invokable) 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄할 수도 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

`routes/console.php` 파일을 커맨드 정의 전용으로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용해 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 받는 클로저를 인자로 받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

예약된 작업의 개요와 다음에 실행될 시점을 확인하고 싶다면, 다음 Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저뿐만 아니라 [Artisan 명령어](/docs/{{version}}/artisan) 및 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 명령어 이름이나 클래스명을 이용해 Artisan 명령어를 스케줄할 수 있습니다.

클래스명을 사용하여 Artisan 명령어를 스케줄할 때는, 명령어 실행 시 전달할 추가 인자를 배열로 넘길 수도 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### 클로저 Artisan 명령어 스케줄링

클로저로 정의된 Artisan 명령어를 예약하려면, 명령어 정의 후에 스케줄 관련 메서드를 체이닝하면 됩니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인자를 전달해야 할 경우, `schedule` 메서드를 사용해 지정할 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드를 사용하여 [큐 작업](/docs/{{version}}/queues)를 예약할 수 있습니다. 이 메서드는 클로저를 사용하지 않고도 큐 작업을 쉽게 예약할 수 있게 해줍니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

선택적으로 두 번째, 세 번째 인자로 큐 이름, 큐 커넥션을 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "heartbeats" 큐를 "sqs" 커넥션에서 사용하도록 예약...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령어 스케줄링

`exec` 메서드를 사용해 운영 체제의 명령어를 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

이미 일부 작업을 정해진 간격으로 실행하는 예시를 살펴봤지만, 할당할 수 있는 예약 빈도는 더 다양합니다:

<div class="overflow-auto">

| 메서드                                  | 설명                                                 |
| ---------------------------------------- | ---------------------------------------------------- |
| `->cron('* * * * *');`                   | 커스텀 크론 스케줄로 작업 실행                        |
| `->everySecond();`                       | 매초 작업 실행                                        |
| `->everyTwoSeconds();`                   | 2초마다 작업 실행                                     |
| `->everyFiveSeconds();`                  | 5초마다 작업 실행                                     |
| `->everyTenSeconds();`                   | 10초마다 작업 실행                                    |
| `->everyFifteenSeconds();`               | 15초마다 작업 실행                                    |
| `->everyTwentySeconds();`                 | 20초마다 작업 실행                                   |
| `->everyThirtySeconds();`                | 30초마다 작업 실행                                    |
| `->everyMinute();`                       | 매분 작업 실행                                        |
| `->everyTwoMinutes();`                   | 2분마다 작업 실행                                     |
| `->everyThreeMinutes();`                 | 3분마다 작업 실행                                     |
| `->everyFourMinutes();`                  | 4분마다 작업 실행                                     |
| `->everyFiveMinutes();`                  | 5분마다 작업 실행                                     |
| `->everyTenMinutes();`                   | 10분마다 작업 실행                                    |
| `->everyFifteenMinutes();`               | 15분마다 작업 실행                                    |
| `->everyThirtyMinutes();`                | 30분마다 작업 실행                                    |
| `->hourly();`                            | 매시간 작업 실행                                      |
| `->hourlyAt(17);`                        | 매시간 17분에 작업 실행                               |
| `->everyOddHour($minutes = 0);`          | 홀수 시간마다 작업 실행                               |
| `->everyTwoHours($minutes = 0);`         | 2시간마다 작업 실행                                   |
| `->everyThreeHours($minutes = 0);`       | 3시간마다 작업 실행                                   |
| `->everyFourHours($minutes = 0);`        | 4시간마다 작업 실행                                   |
| `->everySixHours($minutes = 0);`         | 6시간마다 작업 실행                                   |
| `->daily();`                             | 매일 자정에 작업 실행                                 |
| `->dailyAt('13:00');`                    | 매일 13:00에 작업 실행                                |
| `->twiceDaily(1, 13);`                   | 매일 1:00, 13:00에 작업 실행                          |
| `->twiceDailyAt(1, 13, 15);`             | 매일 1:15, 13:15에 작업 실행                          |
| `->weekly();`                            | 매주 일요일 00:00에 작업 실행                         |
| `->weeklyOn(1, '8:00');`                 | 매주 월요일 8:00에 작업 실행                          |
| `->monthly();`                           | 매달 1일 00:00에 작업 실행                            |
| `->monthlyOn(4, '15:00');`               | 매달 4일 15:00에 작업 실행                            |
| `->twiceMonthly(1, 16, '13:00');`        | 매달 1일, 16일 13:00에 작업 실행                      |
| `->lastDayOfMonth('15:00');`             | 매월 말일 15:00에 작업 실행                            |
| `->quarterly();`                         | 매 분기 첫째 날 00:00에 작업 실행                     |
| `->quarterlyOn(4, '14:00');`             | 매 분기 4일 14:00에 작업 실행                         |
| `->yearly();`                            | 매년 첫날 00:00에 작업 실행                            |
| `->yearlyOn(6, 1, '17:00');`             | 매년 6월 1일 17:00에 작업 실행                        |
| `->timezone('America/New_York');`        | 작업의 타임존을 설정                                  |

</div>

이 메서드들은 추가적인 제약 조건과 결합해 더 세밀한 스케줄을 생성할 수 있습니다. 예를 들어, 명령어를 매주 월요일에만 실행하려면 다음과 같이 할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 13시에 1회 실행...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시~오후 5시 매시간 실행...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

추가적으로 사용할 수 있는 스케줄 제약 조건 목록은 아래와 같습니다:

<div class="overflow-auto">

| 메서드                                | 설명                                                  |
| -------------------------------------- | ----------------------------------------------------- |
| `->weekdays();`                       | 평일에만 작업 실행                                    |
| `->weekends();`                       | 주말에만 작업 실행                                    |
| `->sundays();`                        | 일요일에만 작업 실행                                  |
| `->mondays();`                        | 월요일에만 작업 실행                                  |
| `->tuesdays();`                       | 화요일에만 작업 실행                                  |
| `->wednesdays();`                     | 수요일에만 작업 실행                                  |
| `->thursdays();`                      | 목요일에만 작업 실행                                  |
| `->fridays();`                        | 금요일에만 작업 실행                                  |
| `->saturdays();`                      | 토요일에만 작업 실행                                  |
| `->days(array|mixed);`                | 지정한 요일에만 작업 실행                             |
| `->between($startTime, $endTime);`    | 지정한 기간 동안에만 작업 실행                        |
| `->unlessBetween($startTime, $endTime);` | 지정한 기간에는 작업 실행 안 함                     |
| `->when(Closure);`                    | 특정 조건이 true일 경우에만 작업 실행                 |
| `->environments($env);`               | 지정 환경에서만 작업 실행                             |

</div>

<a name="day-constraints"></a>
#### 요일 제약

`days` 메서드는 작업 실행을 특정 요일로 제한할 수 있습니다. 예를 들어, 매주 일요일과 수요일마다 명령어를 매시간 실행하려면 다음처럼 할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는, `Illuminate\Console\Scheduling\Schedule` 클래스에서 제공하는 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간 제약

`between` 메서드는 하루 중 특정 시간 범위에만 작업을 실행하도록 제한할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

유사하게, `unlessBetween` 메서드로 특정 시간대에는 작업 실행을 제외할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건 제약

`when` 메서드는 전달된 클로저의 결과가 `true`인 경우에만 작업이 실행되도록 할 수 있습니다. 다른 제약 조건에 의해 방해받지 않는 한 클로저가 `true`를 반환하면 작업이 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`의 반대입니다. `skip`이 `true`를 반환하면 해당 작업은 실행되지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

`when` 메서드를 여러 번 체이닝할 시, 모든 `when` 조건이 `true`를 반환해야 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약

`environments` 메서드는 지정한 환경(`APP_ENV` [환경 변수](/docs/{{version}}/configuration#environment-configuration))에서만 작업이 실행되도록 할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존

`timezone` 메서드를 사용하여 예약 작업 시간이 특정 타임존 기준으로 해석되도록 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 작업에 동일한 타임존을 반복적으로 지정하는 대신, 애플리케이션의 `app` 설정 파일에 `schedule_timezone` 옵션을 정의하여 전체 예약 작업에 사용할 타임존을 지정할 수도 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 일광절약시간(썸머타임)을 사용합니다. 일광절약시간이 변경되는 경우, 예약 작업이 두 번 실행되거나 실행되지 않을 수 있습니다. 이런 이유로, 가능하다면 타임존 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 방지

기본적으로 예약 작업은 이전 인스턴스가 실행 중이어도 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

이 예시에서는, `emails:send` [Artisan 명령어](/docs/{{version}}/artisan)가 이미 실행 중이지 않을 때마다 매분마다 실행됩니다. `withoutOverlapping`은 작업 실행 시간이 예측 불가할 때 유용합니다.

필요하다면 "중복 방지" 락(lock)이 만료되기까지 대기할 분(minute) 수를 지정할 수 있습니다. 기본적으로는 24시간 후 만료됩니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping`은 애플리케이션의 [캐시](/docs/{{version}}/cache)를 통해 락을 획득합니다. 만약 서버의 문제로 작업이 멈춘 경우, `schedule:clear-cache` Artisan 명령어로 락을 해제할 수 있습니다. 이 명령어는 락이 비정상적으로 유지되는 상황에서만 사용하면 됩니다.

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 작업 실행

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, `redis` 이어야 하며, 모든 서버가 동일한 중앙 캐시 서버를 참조해야 합니다.

애플리케이션의 스케줄러가 여러 서버에서 동작한다면, 예약된 작업이 단 한 대의 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤에 리포트를 생성하는 작업이 있고, 스케줄러가 워커 서버 세 대에서 모두 실행된다면, 리포트가 세 번 생성됩니다.

작업이 한 대의 서버에서만 실행되도록 하려면, 예약 작업 정의 시 `onOneServer` 메서드를 사용하세요. 가장 먼저 락을 획득한 서버만 작업을 실행합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

단일 서버 작업에 사용할 캐시 스토어를 커스터마이징하려면 `useCache` 메서드를 사용할 수 있습니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 이름 설정

동일한 작업을 서로 다른 인자로 예약하되, 각 경우를 단일 서버에서만 실행하고 싶을 때는, 각 스케줄 정의에 고유한 이름을 `name` 메서드로 부여할 수 있습니다:

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

마찬가지로, 단일 서버에서 실행하고자 하는 예약된 클로저에는 반드시 이름을 부여해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로 같은 시간에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서대로 순차적으로 실행됩니다. 실행 시간이 긴 작업이 있다면, 이후 작업이 예상보다 늦게 시작될 수 있습니다. 여러 작업을 동시에 실행하고 싶을 땐, `runInBackground` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command`와 `exec` 메서드로 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 점검 모드

애플리케이션이 [점검 모드](/docs/{{version}}/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 이는 서버에서 점검 작업이 끝나지 않았을 때 예약 작업이 간섭하는 것을 막기 위해서입니다. 그러나 점검 모드에서도 특정 작업을 강제로 실행하고 싶다면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하세요:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹

비슷한 설정의 여러 예약 작업을 정의할 때, 작업 그룹화 기능을 사용하면 동일한 설정을 반복해서 작성할 필요가 없습니다. 그룹화는 코드를 간소화하고 관련 작업의 일관성을 보장합니다.

작업 그룹을 만들려면, 원하는 예약 설정 메서드에 이어 `group` 메서드를 호출하고, 그룹 내부에서 공유 설정을 가진 작업을 정의하는 클로저를 넘기면 됩니다:

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

이제 예약 작업을 정의하는 방법을 배웠으니, 이를 실제 서버에서 어떻게 실행할지 알아봅니다. `schedule:run` Artisan 명령어는 서버의 현재 시각을 기준으로 예약된 모든 작업을 평가하고 필요한 작업을 실행합니다.

즉, Laravel 스케줄러를 사용할 때 서버에 오직 하나의 크론 엔트리만 등록해서 1분마다 `schedule:run` 명령어가 실행되도록 하면 됩니다. 크론 엔트리 추가 방법을 모를 경우, [Laravel Cloud](https://cloud.laravel.com)와 같은 관리형 플랫폼을 사용해 예약 작업 실행을 맡겨도 됩니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 스케줄

대부분의 운영 체제에서 크론 잡은 최대 1분 간격으로만 실행할 수 있습니다. 하지만 Laravel의 스케줄러는 1초처럼 더 짧은 간격으로도 작업을 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션 내에 1분 미만 작업을 정의하면, `schedule:run` 명령어가 즉시 종료되지 않고 현재 분이 끝날 때까지 계속 실행되면서 필요한 모든 1분 미만 작업을 실행합니다.

예상보다 오래 걸리는 작업이 있으면 이후의 1분 미만 작업 실행이 지연될 수 있으므로, 1분 미만 작업에서는 실제 처리는 큐 작업이나 백그라운드 명령어로 위임하는 것이 좋습니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단하기

1분 미만 작업이 있을 경우, `schedule:run` 명령어는 1분 동안 끝까지 실행됩니다. 따라서 애플리케이션 배포 중에 이 명령어 인스턴스를 중단해야 할 때가 있습니다. 그렇지 않으면 진행 중인 `schedule:run` 프로세스가 이전 배포본의 코드를 계속 사용합니다.

진행 중인 `schedule:run`을 중단하려면, 배포 스크립트 마지막에 `schedule:interrupt` 명령어를 추가하세요:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

로컬 개발 환경에서는 보통 크론 엔트리를 추가하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드로 실행되며, 직접 종료할 때까지 1분마다 스케줄러를 동작시킵니다. 1분 미만 작업이 있으면 매분 동안 해당 작업을 계속 처리합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약 작업에서 생성된 출력 결과를 다루는 여러 편리한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드로 출력을 파일에 기록할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력 결과를 파일에 덧붙이고 싶다면, `appendOutputTo` 메서드를 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 출력 결과를 원하는 이메일 주소로 발송할 수 있습니다. 이메일 발송 전에는 Laravel의 [이메일 서비스](/docs/{{version}}/mail)를 미리 구성해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

아티즌 또는 시스템 명령어가 비정상 종료(0이 아닌 종료 코드로 종료)할 때만 출력 결과를 메일로 받고 싶다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`와 `exec` 메서드에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅

`before`와 `after` 메서드를 사용하여 예약 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업이 곧 실행됩니다...
    })
    ->after(function () {
        // 작업이 실행되었습니다...
    });
```

`onSuccess`와 `onFailure` 메서드는 예약 작업이 성공하거나 실패했을 때 실행할 코드를 지정할 수 있습니다. 실패란, 스케줄된 아티즌 또는 시스템 명령어가 0이 아닌 코드로 종료된 경우를 의미합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업이 성공했습니다...
    })
    ->onFailure(function () {
        // 작업이 실패했습니다...
    });
```

명령어에서 출력 결과가 있다면, `after`, `onSuccess`, `onFailure` 훅의 클로저에서 `Illuminate\Support\Stringable` 인스턴스를 타입힌트하여 접근할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업이 성공했습니다...
    })
    ->onFailure(function (Stringable $output) {
        // 작업이 실패했습니다...
    });
```

<a name="pinging-urls"></a>
#### URL 핑(Ping)하기

`pingBefore`와 `thenPing` 메서드를 사용하면 작업 실행 전후에 자동으로 지정 URL에 핑(ping) 요청을 보낼 수 있습니다. 외부 서비스(예: [Envoyer](https://envoyer.io))에 작업 시작 또는 완료를 알릴 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess`, `pingOnFailure` 메서드는 작업 성공 또는 실패시에만 지정 URL로 핑을 보낼 수 있습니다. 실패란, 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우입니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드를 사용하면 주어진 조건이 true일 때만 해당 URL로 핑을 보냅니다:

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

Laravel은 스케줄링 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 다음 이벤트 중 원하는 이벤트에 [리스너를 정의](/docs/{{version}}/events)해 사용할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Console\Events\ScheduledTaskStarting` |
| `Illuminate\Console\Events\ScheduledTaskFinished` |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped` |
| `Illuminate\Console\Events\ScheduledTaskFailed` |

</div>
