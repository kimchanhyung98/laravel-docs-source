# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [아티즌 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐잉된 작업(Job) 스케줄링](#scheduling-queued-jobs)
    - [셸(Shell) 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존 관리](#timezones)
    - [작업 중복 실행 방지](#preventing-task-overlaps)
    - [단일 서버에서만 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업 실행](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행하기](#running-the-scheduler)
    - [1분 미만 단위의 스케줄 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [작업 출력 다루기](#task-output)
- [작업 훅 (Hooks)](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 스케줄링이 필요한 각 작업마다 cron 설정을 직접 작성했을지도 모릅니다. 하지만 이런 방식은 작업 스케줄이 소스 코드로 관리되지 않으므로, 기존 cron 항목을 확인하거나 새로 추가하려면 서버에 SSH 접속을 해야 하고, 점점 번거로워집니다.

라라벨의 명령어 스케줄러는 서버의 예약 작업을 깔끔하게 관리할 수 있는 새로운 접근 방식을 제공합니다. 스케줄러를 활용하면 라라벨 애플리케이션 내부에서 명령어 스케줄을 간결하고 표현력 있게 정의할 수 있습니다. 스케줄러를 사용할 때는 서버에 오직 하나의 cron 항목만 추가하면 되고, 실제 작업 스케줄은 일반적으로 애플리케이션의 `routes/console.php` 파일에서 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 먼저, 간단한 예시를 살펴보겠습니다. 아래 예시에서는 매일 자정마다 실행되는 클로저(익명 함수)를 예약하고, 이 클로저에서 데이터베이스 쿼리를 사용해 테이블을 비웁니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 이용한 스케줄링 외에도, [인보커블(호출 가능) 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄링할 수도 있습니다. 인보커블 객체는 `__invoke` 메서드를 갖는 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

만약 `routes/console.php` 파일을 명령어 정의에만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용해 예약 작업을 정의할 수도 있습니다. 이 메서드는 스케줄러 인스턴스를 받는 클로저를 인자로 받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

예약된 작업들의 전체 목록과, 각 작업의 다음 실행 예정 시간을 보고 싶다면 `schedule:list` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### 아티즌 명령어 스케줄링

클로저뿐만 아니라 [아티즌 명령어](/docs/12.x/artisan)와 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용하면 명령어의 이름이나 클래스명을 통해 아티즌 명령어를 예약할 수 있습니다.

아티즌 명령어를 클래스 이름으로 예약하는 경우, 명령어 실행 시 인자로 전달할 추가 명령줄 인수를 배열로 지정할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### 클로저 아티즌 명령어 스케줄링

클로저로 정의된 아티즌 명령어를 예약하고 싶다면, 명령어 정의 이후에 스케줄 관련 메서드를 체이닝하여 사용할 수 있습니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수(argument)를 전달해야 한다면, `schedule` 메서드에 인수를 배열로 넘길 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐잉된 작업(Job) 스케줄링

`job` 메서드를 사용하면 [큐잉된 작업](/docs/12.x/queues)을 쉽게 예약할 수 있습니다. 이 방법은 클로저 내에서 큐 작업을 처리하기 위해 따로 코드를 작성하는 번거로움 없이 바로 큐 작업을 예약할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드에는 선택적으로 두 번째, 세 번째 인자로 큐 이름과 큐 커넥션을 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "heartbeats" 큐의 "sqs" 커넥션으로 작업을 디스패치합니다...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸(Shell) 명령어 스케줄링

`exec` 메서드를 사용하여 운영체제에 명령어를 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

지금까지 특정 간격(주기)으로 작업을 반복 실행하는 몇 가지 방법을 살펴봤습니다. 라라벨은 이 외에도 다양한 빈도로 작업을 예약할 수 있는 여러 메서드를 제공합니다:

<div class="overflow-auto">

| 메서드                               | 설명                                                    |
| ------------------------------------ | ------------------------------------------------------ |
| `->cron('* * * * *');`               | 사용자 정의 cron 스케줄로 작업 실행                        |
| `->everySecond();`                   | 매초마다 작업 실행                                        |
| `->everyTwoSeconds();`               | 2초마다 작업 실행                                         |
| `->everyFiveSeconds();`              | 5초마다 작업 실행                                         |
| `->everyTenSeconds();`               | 10초마다 작업 실행                                        |
| `->everyFifteenSeconds();`           | 15초마다 작업 실행                                        |
| `->everyTwentySeconds();`            | 20초마다 작업 실행                                        |
| `->everyThirtySeconds();`            | 30초마다 작업 실행                                        |
| `->everyMinute();`                   | 매분마다 작업 실행                                        |
| `->everyTwoMinutes();`               | 2분마다 작업 실행                                         |
| `->everyThreeMinutes();`             | 3분마다 작업 실행                                         |
| `->everyFourMinutes();`              | 4분마다 작업 실행                                         |
| `->everyFiveMinutes();`              | 5분마다 작업 실행                                         |
| `->everyTenMinutes();`               | 10분마다 작업 실행                                        |
| `->everyFifteenMinutes();`           | 15분마다 작업 실행                                        |
| `->everyThirtyMinutes();`            | 30분마다 작업 실행                                        |
| `->hourly();`                        | 매시간마다 작업 실행                                      |
| `->hourlyAt(17);`                    | 매시간 17분에 작업 실행                                   |
| `->everyOddHour($minutes = 0);`      | 홀수 시간(1, 3, 5, ...)마다 작업 실행                     |
| `->everyTwoHours($minutes = 0);`     | 2시간마다 작업 실행                                       |
| `->everyThreeHours($minutes = 0);`   | 3시간마다 작업 실행                                       |
| `->everyFourHours($minutes = 0);`    | 4시간마다 작업 실행                                       |
| `->everySixHours($minutes = 0);`     | 6시간마다 작업 실행                                       |
| `->daily();`                         | 매일 자정에 작업 실행                                     |
| `->dailyAt('13:00');`                | 매일 오후 1시에 작업 실행                                 |
| `->twiceDaily(1, 13);`               | 매일 오전 1시, 오후 1시에 작업 실행                       |
| `->twiceDailyAt(1, 13, 15);`         | 매일 오전 1시 15분, 오후 1시 15분에 작업 실행             |
| `->weekly();`                        | 매주 일요일 00:00에 작업 실행                             |
| `->weeklyOn(1, '8:00');`             | 매주 월요일 오전 8시에 작업 실행                          |
| `->monthly();`                       | 매월 1일 00:00에 작업 실행                                |
| `->monthlyOn(4, '15:00');`           | 매월 4일 오후 3시에 작업 실행                             |
| `->twiceMonthly(1, 16, '13:00');`    | 매월 1일, 16일 오후 1시에 작업 실행                       |
| `->lastDayOfMonth('15:00');`         | 매월 마지막 날 오후 3시에 작업 실행                       |
| `->quarterly();`                     | 분기마다 첫째 날 00:00에 작업 실행                        |
| `->quarterlyOn(4, '14:00');`         | 분기마다 4일 오후 2시에 작업 실행                         |
| `->yearly();`                        | 매년 1월 1일 00:00에 작업 실행                            |
| `->yearlyOn(6, 1, '17:00');`         | 매년 6월 1일 오후 5시에 작업 실행                         |
| `->timezone('America/New_York');`    | 해당 작업의 타임존을 설정                                 |

</div>

이런 빈도 메서드는 다양한 제약 조건과 조합하여 더 정밀한 스케줄 설정이 가능합니다. 예를 들면, 특정 요일에만 작업이 실행되도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 오후 1시에 한 번 실행
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시~오후 5시까지 매시간 실행
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

추가로 사용할 수 있는 제약 조건 메서드는 아래와 같습니다:

<div class="overflow-auto">

| 메서드                                 | 설명                                               |
| -------------------------------------- | ------------------------------------------------- |
| `->weekdays();`                       | 평일(월~금)에만 작업 실행                          |
| `->weekends();`                       | 주말(토,일)에만 작업 실행                          |
| `->sundays();`                        | 일요일에만 작업 실행                               |
| `->mondays();`                        | 월요일에만 작업 실행                               |
| `->tuesdays();`                       | 화요일에만 작업 실행                               |
| `->wednesdays();`                     | 수요일에만 작업 실행                               |
| `->thursdays();`                      | 목요일에만 작업 실행                               |
| `->fridays();`                        | 금요일에만 작업 실행                               |
| `->saturdays();`                      | 토요일에만 작업 실행                               |
| `->days(array\|mixed);`               | 특정 요일만 지정해서 작업 실행                     |
| `->between($startTime, $endTime);`    | 지정된 시간대에만 작업 실행                        |
| `->unlessBetween($startTime, $endTime);` | 지정된 시간대 이외에만 작업 실행                |
| `->when(Closure);`                    | 조건(Closure)이 참일 때에만 작업 실행               |
| `->environments($env);`               | 특정 환경(APP_ENV)에만 작업 실행                   |

</div>

<a name="day-constraints"></a>
#### 요일 제약

`days` 메서드를 사용하면 작업이 실행될 요일을 제한할 수 있습니다. 예를 들어, 일요일과 수요일에만 매시간 실행되도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는, 작업을 실행할 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스에 미리 정의된 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간대 제약

`between` 메서드는 특정 시간대에만 작업이 실행되도록 제한할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로, `unlessBetween` 메서드는 지정한 시간대에는 작업을 실행하지 않도록 할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건(Truth Test) 제약

`when` 메서드는 주어진 조건(진리값)에 따라 작업 실행 여부를 제한할 수 있습니다. 즉, 전달된 클로저가 `true`를 반환하면 다른 제약에 걸리지 않는 한 해당 작업이 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`과 반대 개념입니다. 즉, `skip` 에 전달한 클로저가 `true`를 반환하면 예약된 작업은 실행되지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

여러 개의 `when` 메서드를 체이닝해 사용할 수도 있으며, 이 경우 모든 `when` 조건이 `true`여야만 명령이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약

`environments` 메서드는 [환경 변수](/docs/12.x/configuration#environment-configuration) `APP_ENV`에 지정된 특정 환경에서만 작업이 실행되도록 할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존 관리

`timezone` 메서드를 사용하면 예약 작업의 실행 시간을 특정 타임존 기준으로 해석할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 예약 작업에 같은 타임존을 반복적으로 적용해야 한다면, 애플리케이션의 `app` 설정 파일에서 `schedule_timezone` 옵션에 타임존을 지정할 수도 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존에서는 서머타임(일광 절약 시간제)이 적용됩니다. 이로 인해, 시간대가 변경될 때 스케줄 작업이 두 번 실행되거나 아예 실행되지 않을 수도 있습니다. 이런 현상을 방지하려면 가급적 타임존 기반 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 실행 방지

기본적으로 예약 작업은 이전 작업 인스턴스가 아직 실행 중이어도 중복으로 실행됩니다. 만약 이런 중복 실행을 막고 싶다면 `withoutOverlapping` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

이 예시에서는, `emails:send` [아티즌 명령어](/docs/12.x/artisan)가 이미 실행 중이지 않은 경우에만 매분 실행됩니다. `withoutOverlapping` 메서드는 실행 시간이 예측이 어려운 작업에 매우 유용하게 사용할 수 있습니다.

필요하다면 중복 방지(락)의 만료 시간을 분 단위로 지정할 수도 있습니다. 기본적으로 락은 24시간 후 만료됩니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping` 메서드는 애플리케이션의 [캐시](/docs/12.x/cache)를 사용해 락을 얻습니다. 서버 문제 등 예상치 못한 상황으로 작업이 중단되어 락이 풀리지 않는 경우, `schedule:clear-cache` 아티즌 명령어로 락을 강제로 해제할 수 있습니다. 보통 이런 경우에만 락 삭제가 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서만 작업 실행

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `database`, `memcached`, `dynamodb`, 또는 `redis` 드라이버를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버에 연결되어 있어야 합니다.

애플리케이션의 스케줄러가 여러 서버에서 동시에 실행되는 상황이라면, 특정 예약 작업을 단 한 대의 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤에 새로운 리포트를 생성하는 작업이 있다고 가정합시다. 이 작업이 세 대의 워커 서버에서 동시에 실행된다면 리포트가 세 번 만들어질 것입니다. 바람직하지 않겠죠!

이럴 때 스케줄 작업 정의 시 `onOneServer` 메서드를 사용해 해당 작업이 단일 서버에서만 실행되도록 지정할 수 있습니다. 작업을 먼저 획득한(락을 거는 데 성공한) 서버에서만 작업이 실행되고, 다른 서버에서는 실행되지 않습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

또한, `useCache` 메서드를 이용하여 싱글 서버 작업에 필요한 락을 저장할 때 사용하는 캐시 스토어를 직접 지정할 수 있습니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 이름 지정

때때로 같은 작업을 여러 파라미터로 각각 예약하고 싶으면서도, 각각을 한 서버에서만 실행하도록 하고 싶을 수 있습니다. 이런 경우 각 스케줄 정의에 `name` 메서드로 고유 이름을 부여할 수 있습니다:

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

마찬가지로, 스케줄 클로저도 단일 서버에서 실행하려면 이름을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업 실행

기본적으로 동일 시각에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서대로 차례차례 실행됩니다. 만에 하나 실행 시간이 오래 걸리는 작업이 있으면 이후 작업 실행이 지연될 수 있습니다. 여러 작업을 동시에 병렬로(백그라운드로) 실행하려면 `runInBackground` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command`, `exec` 메서드를 통한 작업 예약에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 이는 유지보수 작업 중 불완전한 상태에서 예약 작업이 실행되지 않도록 하기 위함입니다. 하지만, 유지보수 모드여도 특정 작업을 강제로 실행하고 싶다면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하면 됩니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹

비슷한 설정을 가진 여러 예약 작업을 반복적으로 정의해야 할 때, 라라벨의 작업 그룹 기능을 활용하면 코드 중복을 줄이고, 관련 작업들 간의 설정 일관성을 보장할 수 있습니다.

작업 그룹을 정의하려면 원하는 설정 메서드를 호출한 뒤 `group` 메서드를 사용하고, 그룹 내에서 정의할 작업들을 클로저에서 나열합니다:

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

이제 예약 작업을 정의하는 법을 배웠으니, 실제로 서버에서 예약 작업을 실행하는 방법을 살펴보겠습니다. `schedule:run` 아티즌 명령어는 모든 예약 작업을 검사해 서버의 현재 시간을 기준으로 실행 여부를 판단합니다.

라라벨의 스케줄러를 사용할 때는 서버에 단 하나의 cron 항목만 추가해, 매분마다 `schedule:run` 명령어를 실행하면 됩니다. 만약 서버에서 cron 설정이 익숙하지 않다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 관리형 플랫폼을 활용해 예약 작업 실행을 쉽게 관리할 수도 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 단위의 스케줄 작업

대부분의 운영 체제에서는 cron 작업이 최소 1분에 한 번만 실행될 수 있습니다. 그러나 라라벨 스케줄러를 사용하면 작업을 초 단위로(예: 매초마다) 더욱 짧은 간격으로 예약할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션 내에 1분 미만 단위로 예약 작업이 정의되어 있으면, `schedule:run` 명령어는 즉시 종료되지 않고 해당 분이 끝날 때까지 계속 실행됩니다. 이로써 각 초 단위 작업이 필요한 모든 타이밍에 호출될 수 있게 됩니다.

실행 시간이 예상보다 오래 걸리는 1분 미만(초 단위) 작업이 있다면, 이후 작업 실행이 지연될 수 있으므로, 모든 초 단위 작업은 큐 작업(Job) 또는 백그라운드(Command)로 실제 처리를 위임하는 것이 좋습니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단(interrupt)하기

1분 미만 작업이 있을 때 `schedule:run` 명령어는 해당 분이 끝날 때까지 실행됩니다. 애플리케이션을 배포(deploy)할 때 이미 실행 중이던 커맨드가 끝날 때까지 이전 코드로 계속 동작하게 됩니다.

배포 중에 현재 실행 중인 `schedule:run` 명령어를 강제로 중단하려면, 배포 스크립트에서 `schedule:interrupt` 명령어를 실행하세요. 이 명령어는 애플리케이션 배포가 끝난 후 호출합니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

로컬 개발 환경에서는 보통 cron 작업을 등록하지 않습니다. 대신, `schedule:work` 아티즌 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드(foreground)에서 실행되며, 사용자가 명령어를 중지시킬 때까지 매분마다 스케줄러를 실행합니다. 1분 미만(초 단위) 작업이 있다면 해당 분 동안 계속해서 실행됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 다루기

라라벨 스케줄러는 예약 작업의 실행 결과(출력)를 다루기 위한 여러 편리한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용해 작업 출력을 파일로 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력을 파일에 덮어쓰는 것이 아니라 이어서 쌓고 싶다면, `appendOutputTo` 메서드를 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 작업 출력을 원하는 이메일 주소로 전송할 수 있습니다. 이 기능을 사용하기 전에 라라벨의 [메일 서비스](/docs/12.x/mail) 설정이 필요합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

만약 예약된 아티즌 명령어 또는 시스템 명령어가 비정상적으로 종료(종료코드 non-zero)된 경우에만 출력을 이메일로 받고 싶다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`, `exec` 메서드로 예약한 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅 (Hooks)

`before`, `after` 메서드를 사용해 예약 작업 실행 전·후에 실행할 코드를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업이 곧 실행됩니다...
    })
    ->after(function () {
        // 작업이 방금 실행을 마쳤습니다...
    });
```

`onSuccess`, `onFailure` 메서드를 사용해 작업이 성공 또는 실패할 때 실행할 코드를 지정할 수 있습니다. 실패란 예약된 아티즌/시스템 명령어가 비정상 종료(non-zero exit code)로 반환된 경우를 의미합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업이 성공적으로 종료됨...
    })
    ->onFailure(function () {
        // 작업이 실패함...
    });
```

명령어 실행 결과(출력)가 있다면, `after`, `onSuccess`, `onFailure`에서 클로저의 인자로 `Illuminate\Support\Stringable` 타입을 지정하여 출력 값을 받을 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업이 성공했을 때의 출력값을 활용
    })
    ->onFailure(function (Stringable $output) {
        // 작업이 실패했을 때의 출력값을 활용
    });
```

<a name="pinging-urls"></a>
#### URL 핑(Ping) 전송

`pingBefore`, `thenPing` 메서드를 활용하면 예약 작업 실행 전후에 특정 URL을 자동으로 호출(ping)할 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io) 등 외부 서비스에 작업이 시작되거나 끝났음을 알릴 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess`, `pingOnFailure` 메서드를 사용하면 작업이 성공/실패할 때만 특정 URL을 호출하도록 할 수 있습니다. 실패는 예약한 아티즌/시스템 명령어가 비정상적으로 종료된 경우입니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 등은 특정 조건이 참일 때만 지정한 URL을 호출(ping)합니다:

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

라라벨은 예약 작업 처리과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 이벤트들에 대해 [리스너를 등록](/docs/12.x/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                              |
| ------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>