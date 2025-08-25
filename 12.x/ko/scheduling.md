# 태스크 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [Shell 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 주기 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [태스크 중복 실행 방지](#preventing-task-overlaps)
    - [단일 서버에서 태스크 실행](#running-tasks-on-one-server)
    - [백그라운드 태스크](#background-tasks)
    - [메인터넌스 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행](#running-the-scheduler)
    - [1분 미만의 스케줄 태스크](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [태스크 출력](#task-output)
- [태스크 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

과거에는 서버에서 실행할 각 태스크마다 별도의 cron 설정을 작성해야 했습니다. 그러나 이 방식은 유지보수가 번거로워질 수 있습니다. cron 스케줄러 설정이 소스 제어에서 벗어나고, 기존 cron 엔트리의 조회나 추가를 위해 서버에 SSH로 접속해야 하기 때문입니다.

Laravel의 커맨드 스케줄러는 서버에서 예약된 태스크를 관리하는 새로운 접근 방식을 제공합니다. 스케줄러를 사용하면 명령어 실행 일정을 Laravel 애플리케이션 내부에서 간결하고 명확하게 정의할 수 있습니다. 스케줄러를 사용할 때 서버에는 단 하나의 cron 엔트리만 필요합니다. 일반적으로 태스크 스케줄은 애플리케이션의 `routes/console.php` 파일에서 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의 (Defining Schedules)

예약할 모든 태스크는 애플리케이션의 `routes/console.php` 파일에서 정의할 수 있습니다. 우선 예시부터 살펴보겠습니다. 아래 예시에서는 클로저를 매일 자정에 호출하여 데이터베이스 테이블을 비우는 쿼리를 실행합니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 사용한 스케줄링 외에도 [호출 가능한 객체(invokable object)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 예약할 수도 있습니다. 호출 가능한 객체란 `__invoke` 메서드를 포함한 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

`routes/console.php` 파일을 명령어 정의 용도로만 남겨두고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에 있는 `withSchedule` 메서드를 이용해 예약 태스크를 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 전달받는 클로저를 인수로 받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

예약된 태스크 목록과 다음 실행 시점을 확인하고 싶다면, `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저 외에도 [Artisan 명령어](/docs/12.x/artisan)와 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 이용해 명령어의 이름이나 클래스명을 통해 Artisan 명령어를 예약할 수 있습니다.

명령어 클래스명을 사용해 Artisan 명령어를 예약할 때, 명령어 실행 시 제공할 추가 명령줄 인수를 배열로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Artisan 클로저 명령어 스케줄링

클로저로 정의한 Artisan 명령어를 예약하고 싶다면, 명령어 정의 뒤에 스케줄 관련 메서드를 체이닝하면 됩니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달해야 한다면, `schedule` 메서드에 인수를 전달할 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

[큐 작업(queued job)](/docs/12.x/queues)은 `job` 메서드로 예약할 수 있습니다. 이 메서드를 사용하면 클로저를 통해 큐 작업을 등록하지 않고도 손쉽게 예약할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드에는 옵션으로 큐 이름과 큐 연결명을 두 번째, 세 번째 인수로 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "heartbeats" 큐를 "sqs" 연결로 작업을 디스패치합니다...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### Shell 명령어 스케줄링

`exec` 메서드를 사용하면 운영체제의 명령어를 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 주기 옵션

지정한 간격으로 태스크를 실행하는 방법을 이미 살펴보았습니다. 하지만 태스크에 지정할 수 있는 실행 주기는 더욱 다양합니다:

<div class="overflow-auto">

| 메서드                               | 설명                                                    |
| ------------------------------------ | ------------------------------------------------------- |
| `->cron('* * * * *');`               | 커스텀 cron 스케줄로 태스크 실행                         |
| `->everySecond();`                   | 매초 태스크 실행                                         |
| `->everyTwoSeconds();`               | 2초마다 태스크 실행                                      |
| `->everyFiveSeconds();`              | 5초마다 태스크 실행                                      |
| `->everyTenSeconds();`               | 10초마다 태스크 실행                                     |
| `->everyFifteenSeconds();`           | 15초마다 태스크 실행                                     |
| `->everyTwentySeconds();`            | 20초마다 태스크 실행                                     |
| `->everyThirtySeconds();`            | 30초마다 태스크 실행                                     |
| `->everyMinute();`                   | 1분마다 태스크 실행                                      |
| `->everyTwoMinutes();`               | 2분마다 태스크 실행                                      |
| `->everyThreeMinutes();`             | 3분마다 태스크 실행                                      |
| `->everyFourMinutes();`              | 4분마다 태스크 실행                                      |
| `->everyFiveMinutes();`              | 5분마다 태스크 실행                                      |
| `->everyTenMinutes();`               | 10분마다 태스크 실행                                     |
| `->everyFifteenMinutes();`           | 15분마다 태스크 실행                                     |
| `->everyThirtyMinutes();`            | 30분마다 태스크 실행                                     |
| `->hourly();`                        | 매시간 태스크 실행                                       |
| `->hourlyAt(17);`                    | 매시간 17분에 태스크 실행                                |
| `->everyOddHour($minutes = 0);`      | 홀수 시에 태스크 실행                                    |
| `->everyTwoHours($minutes = 0);`     | 2시간마다 태스크 실행                                    |
| `->everyThreeHours($minutes = 0);`   | 3시간마다 태스크 실행                                    |
| `->everyFourHours($minutes = 0);`    | 4시간마다 태스크 실행                                    |
| `->everySixHours($minutes = 0);`     | 6시간마다 태스크 실행                                    |
| `->daily();`                         | 매일 자정 태스크 실행                                    |
| `->dailyAt('13:00');`                | 매일 13:00에 태스크 실행                                 |
| `->twiceDaily(1, 13);`               | 매일 1:00, 13:00에 태스크 실행                           |
| `->twiceDailyAt(1, 13, 15);`         | 매일 1:15, 13:15에 태스크 실행                           |
| `->weekly();`                        | 매주 일요일 00:00에 태스크 실행                          |
| `->weeklyOn(1, '8:00');`             | 매주 월요일 8:00에 태스크 실행                           |
| `->monthly();`                       | 매월 첫째 날 00:00에 태스크 실행                         |
| `->monthlyOn(4, '15:00');`           | 매월 4일 15:00에 태스크 실행                             |
| `->twiceMonthly(1, 16, '13:00');`    | 매월 1일, 16일 13:00에 태스크 실행                       |
| `->lastDayOfMonth('15:00');`         | 매월 마지막 날 15:00에 태스크 실행                       |
| `->quarterly();`                     | 분기별(1,4,7,10월) 첫째 날 00:00에 태스크 실행           |
| `->quarterlyOn(4, '14:00');`         | 분기별 4일 14:00에 태스크 실행                           |
| `->yearly();`                        | 매년 첫째 날 00:00에 태스크 실행                         |
| `->yearlyOn(6, 1, '17:00');`         | 매년 6월 1일 17:00에 태스크 실행                         |
| `->timezone('America/New_York');`    | 태스크에 사용할 타임존 설정                              |

</div>

이러한 메서드는 추가 제약조건과 조합해 요일별로 실행하도록 세밀한 스케줄을 만들 수도 있습니다. 예를 들어, 명령어를 매주 월요일에만 실행하도록 스케줄링할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 오후 1시에 1회 실행...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 시간마다 실행...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

추가 스케줄 제약 조건 목록은 아래와 같습니다:

<div class="overflow-auto">

| 메서드                                 | 설명                                               |
| -------------------------------------- | -------------------------------------------------- |
| `->weekdays();`                        | 평일(월~금)에만 태스크 실행                        |
| `->weekends();`                        | 주말(토,일)에만 태스크 실행                        |
| `->sundays();`                         | 일요일에만 태스크 실행                             |
| `->mondays();`                         | 월요일에만 태스크 실행                             |
| `->tuesdays();`                        | 화요일에만 태스크 실행                             |
| `->wednesdays();`                      | 수요일에만 태스크 실행                             |
| `->thursdays();`                       | 목요일에만 태스크 실행                             |
| `->fridays();`                         | 금요일에만 태스크 실행                             |
| `->saturdays();`                       | 토요일에만 태스크 실행                             |
| `->days(array|mixed);`                 | 특정 요일에만 태스크 실행                          |
| `->between($startTime, $endTime);`     | 시작/종료 시간 사이에만 태스크 실행                |
| `->unlessBetween($startTime, $endTime);` | 시작/종료 시간 사이에는 태스크 실행하지 않음       |
| `->when(Closure);`                     | 지정한 반환값이 true인 경우에만 태스크 실행         |
| `->environments($env);`                | 특정 환경에서만 태스크 실행                        |

</div>

<a name="day-constraints"></a>
#### 요일 제약 (Day Constraints)

`days` 메서드는 태스크의 실행을 특정 요일로 제한하는 데 사용할 수 있습니다. 예를 들어, 매시간 일요일과 수요일에만 명령어를 예약하려면 다음과 같이 작성합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는, 태스크 실행 요일을 지정할 때 `Illuminate\Console\Scheduling\Schedule` 클래스에 정의된 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간 제약 (Between Time Constraints)

`between` 메서드는 태스크 실행을 특정 시간대에만 제한할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

유사하게, `unlessBetween` 메서드를 사용하면 지정한 시간대 동안 태스크 실행을 제외할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 참/거짓 테스트 제약 (Truth Test Constraints)

`when` 메서드는 주어진 클로저의 반환값에 따라 태스크 실행을 제한할 수 있습니다. 즉, 클로저가 `true`를 반환하는 경우, 다른 조건이 없으면 태스크가 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`과 반대 개념으로, 클로저가 `true`를 반환하면 해당 태스크는 실행되지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

`when` 메서드를 체이닝할 경우, 지정한 모든 `when` 조건이 `true`를 반환해야 명령이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 (Environment Constraints)

`environments` 메서드를 사용하면 지정한 [환경 변수](/docs/12.x/configuration#environment-configuration) `APP_ENV` 값에 해당하는 환경에서만 태스크를 실행하도록 할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존 (Timezones)

`timezone` 메서드를 사용하면 예약된 태스크의 시간이 지정한 타임존 기준으로 해석되도록 할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

여러 태스크에 같은 타임존을 반복해서 지정한다면, 애플리케이션의 `app` 설정 파일 내에 `schedule_timezone` 옵션을 추가해 전체 스케줄에 타임존을 지정할 수 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 서머타임(일광절약시간제)을 사용합니다. 서머타임이 전환되면 예약된 태스크가 두 번 실행되거나 아예 실행되지 않을 수 있으니, 가능한 경우 타임존 스케줄링을 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 태스크 중복 실행 방지 (Preventing Task Overlaps)

기본적으로 예약된 태스크는 이전 인스턴스가 아직 실행 중일 경우에도 계속해서 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

이 예시에서 `emails:send` [Artisan 명령어](/docs/12.x/artisan)는 이미 실행 중이 아닌 경우에만 매분 실행됩니다. `withoutOverlapping` 메서드는 실행 시간이 크게 변동되는 태스크를 예측 가능한 방식으로 관리할 때 매우 유용합니다.

필요하다면 "중복 실행 방지" 락이 만료되기까지 유지될 분 수를 지정할 수 있습니다. 기본 만료 시간은 24시간(1440분)입니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로, `withoutOverlapping` 메서드는 애플리케이션의 [캐시](/docs/12.x/cache)를 이용해 락을 관리합니다. 만약 서버 문제 등으로 태스크가 중단되어 락이 남아 있다면, `schedule:clear-cache` Artisan 명령어로 해당 캐시 락을 수동으로 해제할 수 있습니다. 이 기능은 예기치 않은 서버 문제로 태스크가 고착되었을 때만 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 태스크 실행 (Running Tasks on One Server)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis` 이어야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

애플리케이션의 스케줄러가 여러 서버에서 실행되고 있다면, 특정 예약 작업이 한 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 새 보고서를 매주 금요일 밤마다 생성하는 태스크가 있다고 가정하면, 세 개의 워커(server)에서 스케줄러가 실행되고 있으면 같은 작업이 세 번 수행될 수 있습니다. 이는 바람직하지 않습니다!

태스크를 단 하나의 서버에서만 실행하려면, 태스크 정의 시 `onOneServer` 메서드를 사용하세요. 가장 먼저 해당 작업을 점유한 서버가 락을 획득하여 다른 서버에서는 같은 태스크를 동시에 실행하지 못하도록 만듭니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

`useCache` 메서드를 사용하면 단일 서버 태스크를 위한 락을 획득할 캐시 저장소를 커스터마이징할 수 있습니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 이름 지정

서로 다른 매개변수로 동작하는 같은 작업을 각각 한 서버에서만 실행하도록 하고 싶은 경우, 각 스케줄 정의에 `name` 메서드로 고유한 이름을 부여하면 됩니다:

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

마찬가지로, 예약된 클로저도 단일 서버에서 실행하려면 반드시 이름을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 태스크 (Background Tasks)

기본적으로 같은 시간에 예약된 여러 태스크는 `schedule` 메서드에 정의한 순서대로 차례대로 실행됩니다. 실행 시간이 오래 걸리는 태스크가 있을 경우, 이후 태스크가 예상보다 늦게 시작될 수 있습니다. 모든 태스크를 동시에 백그라운드에서 실행하고 싶다면, `runInBackground` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command` 또는 `exec` 메서드를 이용한 태스크에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 메인터넌스 모드 (Maintenance Mode)

애플리케이션이 [메인터넌스 모드](/docs/12.x/configuration#maintenance-mode)일 때는 예약된 태스크가 실행되지 않습니다. 이는 미완성된 서버 유지보수를 방해하지 않기 위해서입니다. 그러나 메인터넌스 모드에서도 특정 태스크를 강제로 실행하고 싶다면, 태스크 정의에 `evenInMaintenanceMode` 메서드를 추가하면 됩니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹 (Schedule Groups)

비슷한 설정값을 가진 여러 예약 태스크를 정의할 때, 반복 코드를 줄이고 일관성을 유지하기 위해 Laravel의 태스크 그룹 기능을 사용할 수 있습니다.

스케줄 그룹을 만들려면, 공통 설정 메서드에 이어 `group` 메서드를 호출하세요. `group` 메서드에는 해당 그룹 내에서 공유 설정을 가진 태스크를 정의하는 클로저를 전달합니다:

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
## 스케줄러 실행 (Running the Scheduler)

이제 예약된 태스크를 정의하는 방법을 배웠으니, 이를 실제 서버에서 실행하는 방법을 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 태스크를 평가하여 서버의 현재 시간에 따라 실행 여부를 결정합니다.

즉, Laravel의 스케줄러를 사용할 때는 서버에 `schedule:run` 명령어를 1분마다 실행하는 단 하나의 cron 엔트리만 추가해주면 됩니다. cron 엔트리 추가 방법을 잘 모른다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 관리형 플랫폼을 사용하는 것도 고려해보세요. 해당 플랫폼에서는 예약 태스크 실행 관리를 대신해줍니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만의 스케줄 태스크 (Sub-Minute Scheduled Tasks)

대부분의 운영체제에서 cron 작업은 1분에 한 번만 실행할 수 있습니다. 하지만 Laravel의 스케줄러는 1초마다 실행되는 등 더욱 짧은 간격으로 태스크를 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션에 1분 미만의 태스크가 정의되어 있으면, `schedule:run` 명령어는 즉시 종료하지 않고 해당 분이 끝날 때까지 계속 실행됩니다. 이를 통해 명령어가 해당 분 동안 필요한 모든 1분 미만 태스크를 반복적으로 호출할 수 있습니다.

단, 1분 미만 태스크가 예상보다 오래 걸리면 이후의 1분 미만 태스크 실행이 지연될 수 있으므로, 모든 1분 미만 태스크는 큐 작업 또는 백그라운드 명령어로 태스크 처리부를 실행하는 것이 좋습니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 태스크 중단

1분 미만 태스크가 정의된 경우, `schedule:run` 명령어는 분 동안 계속 실행됩니다. 따라서 애플리케이션을 배포(deploy)할 때 이 명령을 중단시켜야 할 상황이 있을 수 있습니다. 이미 실행 중인 `schedule:run` 프로세스가 새로 배포된 코드 없이 이전 버전으로 동작할 수 있기 때문입니다.

진행 중인 `schedule:run` 인스턴스를 중단하려면, 배포 스크립트 내에서 `schedule:interrupt` 명령어를 실행하세요. 애플리케이션 배포가 끝난 후에 호출해야 합니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행 (Running the Scheduler Locally)

보통 로컬 개발 환경에는 스케줄러용 cron 엔트리를 추가하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며, 사용자가 명령을 중단하기 전까지 1분마다 스케줄러를 실행합니다. 1분 미만 태스크가 정의된 경우에는, 해당 분 동안 계속해서 반복 실행됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 태스크 출력 (Task Output)

Laravel 스케줄러는 예약 태스크가 생성하는 출력을 다루는 여러 편리한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용하면 태스크 출력을 파일로 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력을 파일에 추가(append)하고 싶을 때는 `appendOutputTo` 메서드를 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 지정한 이메일 주소로 태스크 출력을 메일로 전송할 수도 있습니다. 태스크 출력 메일 발송 전에 Laravel의 [이메일 서비스](/docs/12.x/mail)가 먼저 설정되어 있어야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

예약된 Artisan 또는 시스템 명령어가 비정상 종료(non-zero exit code)한 경우에만 이메일로 출력을 받고 싶다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`와 `exec` 메서드를 사용할 때만 적용할 수 있습니다.

<a name="task-hooks"></a>
## 태스크 훅 (Task Hooks)

`before` 및 `after` 메서드를 활용해 예약 태스크가 실행되기 전과 후에 따로 코드를 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 태스크 실행 직전...
    })
    ->after(function () {
        // 태스크 실행 후...
    });
```

`onSuccess` 및 `onFailure` 메서드로 예약 태스크가 성공 또는 실패할 때 각각 실행할 코드를 지정할 수도 있습니다. 실패란 예약된 Artisan 또는 시스템 명령어가 비정상 종료한 경우를 의미합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 태스크 성공...
    })
    ->onFailure(function () {
        // 태스크 실패...
    });
```

명령에서 출력이 발생했다면, `after`, `onSuccess`, `onFailure` 훅에서 `$output` 인수 타입에 `Illuminate\Support\Stringable`을 지정하면 출력을 참조할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 태스크 성공...
    })
    ->onFailure(function (Stringable $output) {
        // 태스크 실패...
    });
```

<a name="pinging-urls"></a>
#### URL 핑(Pinging URLs)

`pingBefore`와 `thenPing` 메서드를 사용하면, 태스크 실행 전 또는 실행 후에 지정한 URL로 HTTP 요청(핑)을 자동 전송할 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 예약 태스크 시작/완료 알림을 보낼 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess` 및 `pingOnFailure` 메서드는 태스크가 성공/실패했을 때에만 URL로 핑을 보냅니다. 실패란 예약된 Artisan 또는 시스템 명령어가 비정상 종료한 경우를 의미합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`·`thenPingIf`·`pingOnSuccessIf`·`pingOnFailureIf` 메서드를 통해 주어진 조건이 `true`일 때만 URL로 핑을 보낼 수도 있습니다:

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

Laravel은 태스크 예약 및 실행 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 이벤트 중 하나에 [리스너(이벤트 리스너)](/docs/12.x/events)를 정의할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                                    |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
