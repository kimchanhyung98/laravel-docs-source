# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링하기](#scheduling-artisan-commands)
    - [큐 작업 스케줄링하기](#scheduling-queued-jobs)
    - [쉘 명령어 스케줄링하기](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 실행 방지하기](#preventing-task-overlaps)
    - [한 서버에서만 작업 실행하기](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [점검 모드 (Maintenance Mode)](#maintenance-mode)
- [스케줄러 실행하기](#running-the-scheduler)
    - [1분 미만 간격 스케줄 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅(Hooks)](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

과거에는 서버에서 실행할 각 작업을 위해 개별 크론(cron) 설정 항목을 작성해야 했을 것입니다. 하지만 이렇게 되면 작업 스케줄이 소스 관리에서 분리되고, 기존 크론 항목을 조회하거나 추가하기 위해 서버에 SSH로 접속해야 하는 번거로움이 발생합니다.

Laravel의 커맨드 스케줄러(command scheduler)는 서버에서 예약 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내에서 명령어 스케줄을 유창하고 명확하게 정의할 수 있습니다. 서버에는 단 하나의 크론 항목만 필요하며, 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메서드 내에서 정의됩니다. 시작을 돕기 위해 해당 메서드 안에 간단한 예제가 포함되어 있습니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기 (Defining Schedules)

애플리케이션의 `App\Console\Kernel` 클래스의 `schedule` 메서드에서 모든 예약 작업을 정의할 수 있습니다. 먼저 예제를 살펴보겠습니다. 이 예제에서는 매일 자정에 호출될 클로저를 스케줄링하며, 클로저 내에서 데이터베이스 테이블을 초기화하는 쿼리를 실행합니다:

```php
<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{
    /**
     * 애플리케이션의 명령어 스케줄 정의.
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->call(function () {
            DB::table('recent_users')->delete();
        })->daily();
    }
}
```

클로저를 이용한 스케줄링 외에도, [호출 가능한 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다:

```php
$schedule->call(new DeleteRecentUsers)->daily();
```

스케줄된 작업과 다음 실행 예정 시간의 개요를 보고 싶다면, `schedule:list` Artisan 명령어를 사용하세요:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링하기 (Scheduling Artisan Commands)

클로저 뿐만 아니라 [Artisan 명령어](/docs/10.x/artisan)와 시스템 명령어도 스케줄할 수 있습니다. 예를 들어 `command` 메서드를 통해 명령어 이름이나 클래스명을 사용해 Artisan 명령어를 예약할 수 있습니다.

Artisan 명령어를 클래스명으로 스케줄링할 때는, 명령어가 호출될 때 제공해야 할 추가 커맨드라인 인수를 배열로 넘길 수도 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링하기 (Scheduling Queued Jobs)

`job` 메서드를 활용하면 [큐 작업](/docs/10.x/queues)을 예약할 수 있습니다. 이 메서드는 클로저로 정의된 `call` 메서드를 사용하지 않고도 큐 작업을 쉽게 예약하는 방법을 제공합니다:

```php
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드는 선택적으로 두 번째, 세 번째 인수로 작업을 쓸 큐 이름과 큐 연결을 지정할 수도 있습니다:

```php
use App\Jobs\Heartbeat;

// "sqs" 연결의 "heartbeats" 큐로 작업 디스패치...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 쉘 명령어 스케줄링하기 (Scheduling Shell Commands)

`exec` 메서드를 사용하면 운영체제에 명령어를 직접 실행하도록 지시할 수 있습니다:

```php
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션 (Schedule Frequency Options)

지금까지 몇 가지 예로 작업이 특정 간격으로 실행되게 설정하는 방법을 보았습니다. 그런데 Laravel 스케줄러는 훨씬 다양한 빈도로 작업을 실행할 수 있습니다:

<div class="overflow-auto">

메서드  | 설명
------------- | -------------
`->cron('* * * * *');`  |  원하는 커스텀 크론 스케줄로 작업 실행
`->everySecond();`  |  매초 작업 실행
`->everyTwoSeconds();`  |  2초마다 작업 실행
`->everyFiveSeconds();`  |  5초마다 작업 실행
`->everyTenSeconds();`  |  10초마다 작업 실행
`->everyFifteenSeconds();`  |  15초마다 작업 실행
`->everyTwentySeconds();`  |  20초마다 작업 실행
`->everyThirtySeconds();`  |  30초마다 작업 실행
`->everyMinute();`  |  매분 작업 실행
`->everyTwoMinutes();`  |  2분마다 작업 실행
`->everyThreeMinutes();`  |  3분마다 작업 실행
`->everyFourMinutes();`  |  4분마다 작업 실행
`->everyFiveMinutes();`  |  5분마다 작업 실행
`->everyTenMinutes();`  |  10분마다 작업 실행
`->everyFifteenMinutes();`  |  15분마다 작업 실행
`->everyThirtyMinutes();`  |  30분마다 작업 실행
`->hourly();`  |  매시간 작업 실행
`->hourlyAt(17);`  |  매시간 17분에 작업 실행
`->everyOddHour($minutes = 0);`  |  홀수 시간마다 작업 실행
`->everyTwoHours($minutes = 0);`  |  2시간마다 작업 실행
`->everyThreeHours($minutes = 0);`  |  3시간마다 작업 실행
`->everyFourHours($minutes = 0);`  |  4시간마다 작업 실행
`->everySixHours($minutes = 0);`  |  6시간마다 작업 실행
`->daily();`  |  매일 자정에 작업 실행
`->dailyAt('13:00');`  |  매일 13:00에 작업 실행
`->twiceDaily(1, 13);`  |  매일 1:00 및 13:00에 작업 실행
`->twiceDailyAt(1, 13, 15);`  |  매일 1:15 및 13:15에 작업 실행
`->weekly();`  |  매주 일요일 00:00에 작업 실행
`->weeklyOn(1, '8:00');`  |  매주 월요일 8:00에 작업 실행
`->monthly();`  |  매월 1일 00:00에 작업 실행
`->monthlyOn(4, '15:00');`  |  매월 4일 15:00에 작업 실행
`->twiceMonthly(1, 16, '13:00');`  |  매달 1일과 16일 13:00에 작업 실행
`->lastDayOfMonth('15:00');` | 매월 말일 15:00에 작업 실행
`->quarterly();` | 분기별 첫날 00:00에 작업 실행
`->quarterlyOn(4, '14:00');` | 분기별 4일 14:00에 작업 실행
`->yearly();`  | 매년 1월 1일 00:00에 작업 실행
`->yearlyOn(6, 1, '17:00');`  | 매년 6월 1일 17:00에 작업 실행
`->timezone('America/New_York');` | 작업의 타임존 설정

</div>

이 메서드들은 추가 제약조건과 결합해 특정 요일에만 정교하게 실행되도록 만들 수도 있습니다. 예를 들어 매주 월요일에 한 번 실행되는 명령어를 스케줄할 수도 있습니다:

```php
// 매주 월요일 오후 1시에 실행...
$schedule->call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 매시간 실행...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

추가 스케줄 제약조건 목록은 다음과 같습니다:

<div class="overflow-auto">

메서드  | 설명
------------- | -------------
`->weekdays();`  |  작업을 평일로 제한
`->weekends();`  |  작업을 주말로 제한
`->sundays();`  |  작업을 일요일로 제한
`->mondays();`  |  작업을 월요일로 제한
`->tuesdays();`  |  작업을 화요일로 제한
`->wednesdays();`  |  작업을 수요일로 제한
`->thursdays();`  |  작업을 목요일로 제한
`->fridays();`  |  작업을 금요일로 제한
`->saturdays();`  |  작업을 토요일로 제한
`->days(array\|mixed);`  |  작업을 특정 요일로 제한
`->between($startTime, $endTime);`  |  지정 시간 사이에만 작업 실행
`->unlessBetween($startTime, $endTime);`  |  지정 시간 사이 작업 제외
`->when(Closure);`  |  진리 평가 조건에 따라 실행 제한
`->environments($env);`  |  특정 환경에서만 실행 제한

</div>

<a name="day-constraints"></a>
#### 요일 조건 (Day Constraints)

`days` 메서드를 사용해 작업이 실행될 요일을 제한할 수 있습니다. 예를 들어, 일요일과 수요일에만 매시간 실행되도록 설정할 수 있습니다:

```php
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

또는 `Illuminate\Console\Scheduling\Schedule` 클래스에 정의된 요일 상수를 사용할 수도 있습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 특정 시간대 조건 (Between Time Constraints)

`between` 메서드는 작업 실행을 시간대 기준으로 제한할 때 사용합니다:

```php
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

반대로 `unlessBetween` 메서드를 사용하면 특정 시간대에는 작업 실행을 제외할 수 있습니다:

```php
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건 평가 제한 (Truth Test Constraints)

`when` 메서드는 주어진 조건 클로저가 `true`를 반환할 때만 작업이 실행되도록 제한합니다. 즉, 다른 제한 조건이 실행을 막지 않는 한 클로저가 `true`를 반환하면 작업이 실행됩니다:

```php
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

반면, `skip` 메서드는 `when`의 반대 개념으로, `skip`이 `true`를 반환하면 스케줄 작업이 실행되지 않습니다:

```php
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

여러 개의 `when` 체인 메서드를 사용할 경우, 모든 조건들이 `true`일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제한 (Environment Constraints)

`environments` 메서드를 사용하면 특정 환경(`APP_ENV` 환경변수에 정의된)에서만 작업을 실행하도록 제한할 수 있습니다:

```php
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존 (Timezones)

`timezone` 메서드로 스케줄 작업의 실행 시간을 특정 타임존 기준으로 해석하도록 지정할 수 있습니다:

```php
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00');
```

동일한 타임존을 여러 작업에 반복해서 지정한다면, `App\Console\Kernel` 클래스 내에 `scheduleTimezone` 메서드를 정의해 기본 타임존을 일괄로 지정할 수도 있습니다:

```php
use DateTimeZone;

/**
 * 기본 스케줄 작업에 사용될 타임존 반환.
 */
protected function scheduleTimezone(): DateTimeZone|string|null
{
    return 'America/Chicago';
}
```

> [!WARNING]  
> 일부 타임존은 일광 절약 시간제(Daylight Saving Time)를 사용합니다. 일광 절약 시간 변경 시에는 작업이 두 번 실행되거나 아예 실행되지 않을 수 있으므로, 가능한 타임존 기반 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 실행 방지하기 (Preventing Task Overlaps)

기본적으로 이전 작업이 아직 실행 중이어도 예약된 작업은 계속 실행됩니다. 이를 막으려면 `withoutOverlapping` 메서드를 사용하세요:

```php
$schedule->command('emails:send')->withoutOverlapping();
```

위 예제는 `emails:send` Artisan 명령어가 실행 중이 아닐 때만 매분 실행되도록 합니다. `withoutOverlapping`은 실행 시간이 작업마다 크게 달라 정확한 종료 시간을 예측하기 어려운 작업에서 유용하게 쓰입니다.

필요에 따라 중복 실행 방지 락(lock) 만료 시간(분)을 지정할 수도 있으며, 기본 값은 24시간입니다:

```php
$schedule->command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping`은 애플리케이션의 [캐시](/docs/10.x/cache)를 이용해 락을 관리합니다. 만약 작업이 서버 문제로 멈춰 락이 해제되지 않는다면, `schedule:clear-cache` Artisan 명령어로 락 캐시를 초기화할 수 있습니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서만 작업 실행하기 (Running Tasks on One Server)

> [!WARNING]  
> 이 기능을 사용하려면 기본 캐시 드라이버로 `database`, `memcached`, `dynamodb`, 또는 `redis` 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신 중이어야 합니다.

스케줄러가 여러 서버에서 실행 중이라면 특정 작업이 단 하나의 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤마다 보고서를 생성하는 작업이 있는데, 스케줄러가 3대 서버에서 돌고 있다면 보고서가 3번 생성되는 문제가 발생합니다.

이런 상황을 방지하려면 스케줄 정의 시 `onOneServer` 메서드를 사용하세요. 가장 먼저 작업 락을 취득한 한 서버만 작업을 실행합니다:

```php
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 이름 붙이기 (Naming Single Server Jobs)

같은 작업이라도 서로 다른 인수로 여러 개를 스케줄할 때, 각각을 단일 서버에서만 실행시키고 싶으면 각 스케줄에 고유한 이름을 지정해야 합니다. `name` 메서드를 사용해 이름을 지정하세요:

```php
$schedule->job(new CheckUptime('https://laravel.com'))
            ->name('check_uptime:laravel.com')
            ->everyFiveMinutes()
            ->onOneServer();

$schedule->job(new CheckUptime('https://vapor.laravel.com'))
            ->name('check_uptime:vapor.laravel.com')
            ->everyFiveMinutes()
            ->onOneServer();
```

비슷하게, 단일 서버에서 실행할 예정인 스케줄된 클로저도 이름을 지정해야 합니다:

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업 (Background Tasks)

기본적으로 동시에 스케줄된 여러 작업은 `schedule` 메서드에서 작성된 순서대로 순차 실행됩니다. 실행 시간이 긴 작업이 있으면 이후 작업 시작이 지연될 수 있습니다. 만약 작업을 동시에 백그라운드에서 실행하고 싶다면 `runInBackground` 메서드를 사용하세요:

```php
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!WARNING]  
> `runInBackground` 메서드는 `command` 그리고 `exec` 메서드로 작업을 예약할 때만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 점검 모드 (Maintenance Mode)

애플리케이션이 [점검 모드](/docs/10.x/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 이는 점검 중인 서버 상태와 작업이 충돌하지 않도록 하기 위함입니다. 만약 점검 모드일 때도 특정 작업을 강제로 실행하고 싶다면 `evenInMaintenanceMode` 메서드를 호출하세요:

```php
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행하기 (Running the Scheduler)

이제 스케줄 작업을 정의하는 방법을 배웠으니, 실제로 서버에서 스케줄러를 어떻게 실행하는지 알아봅시다. `schedule:run` Artisan 명령어는 정의된 작업들을 확인하고 현재 서버 시간 기준으로 실행할 작업을 판단해 실행합니다.

따라서 Laravel 스케줄러를 사용할 때는, 서버에 `schedule:run`을 1분마다 실행하는 크론 설정 한 줄만 추가하면 됩니다. 크론 항목을 추가하는 방법을 모를 경우, [Laravel Forge](https://forge.laravel.com) 같은 서비스가 크론 관리를 해줍니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 스케줄 작업 (Sub-Minute Scheduled Tasks)

대부분 운영체제에서 크론 작업은 최소 1분 간격으로만 실행됩니다. 하지만 Laravel 스케줄러는 1초 단위 같은 그 이하 간격으로도 작업을 예약할 수 있습니다:

```php
$schedule->call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

하위 1분 작업이 정의되면, `schedule:run` 명령어는 즉시 종료하지 않고 현재 분이 끝날 때까지 실행 상태를 유지하면서 모든 하위 1분 작업을 호출합니다.

단, 실행 시간이 길어질 경우 이후 하위 1분 작업 실행에 영향을 줄 수 있으므로, 실제 작업 처리는 큐 작업이나 백그라운드 명령어를 디스패치하는 방식을 권장합니다:

```php
use App\Jobs\DeleteRecentUsers;

$schedule->job(new DeleteRecentUsers)->everyTenSeconds();

$schedule->command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 하위 1분 작업 중단하기

`sub-minute` 작업이 켜진 상태의 `schedule:run` 명령은 한 분이 끝날 때까지 계속 실행되므로, 배포 중에 명령을 중단해야 할 때가 있습니다. 중단하지 않으면, 이미 실행 중인 `schedule:run`이 배포 전 코드로 계속 실행될 수 있습니다.

이때는 배포 스크립트에 `schedule:interrupt` 명령어를 추가하여 배포가 끝난 후 실행 중인 스케줄 명령을 중단하세요:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기 (Running the Scheduler Locally)

일반적으로 로컬 개발 환경에서는 크론 항목 설정을 하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용해 스케줄러를 백그라운드가 아닌 포그라운드로 실행할 수 있습니다. 이 명령은 종료할 때까지 매 분마다 스케줄러를 호출합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

Laravel 스케줄러는 작업 실행 중 생성된 출력 결과를 다루기 위한 여러 편리한 메서드를 제공합니다. `sendOutputTo` 메서드를 이용하면 출력 결과를 파일로 저장해 나중에 살펴볼 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

출력을 기존 파일에 추가하고 싶다면 `appendOutputTo` 메서드를 사용하세요:

```php
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 출력 결과를 원하는 이메일 주소로 발송할 수도 있습니다. 이 기능을 쓰려면 미리 Laravel의 [이메일 서비스 설정](/docs/10.x/mail)을 구성해야 합니다:

```php
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

스케줄된 Artisan 혹은 시스템 명령이 비정상 종료(0이 아닌 코드) 시에만 메일을 보내려면 `emailOutputOnFailure` 메서드를 사용하세요:

```php
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]  
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`나 `exec` 메서드로 예약된 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅(Hooks) (Task Hooks)

`schedule` 메서드 체인에서 `before` 및 `after` 메서드를 사용해 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // 작업 실행 직전...
         })
         ->after(function () {
             // 작업 실행 후...
         });
```

`onSuccess` 및 `onFailure` 메서드를 사용하면 작업의 성공 또는 실패 여부에 따라 실행할 코드를 지정할 수 있습니다. 실패는 Artisan 또는 시스템 명령이 비정상 종료되었음을 의미합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function () {
             // 작업 성공 시...
         })
         ->onFailure(function () {
             // 작업 실패 시...
         });
```

명령어 출력 결과가 있다면, `after`, `onSuccess`, `onFailure` 훅 함수에서 `Illuminate\Support\Stringable` 타입을 `$output` 인수로 타입 힌트해 접근할 수 있습니다:

```php
use Illuminate\Support\Stringable;

$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function (Stringable $output) {
             // 작업 성공 시...
         })
         ->onFailure(function (Stringable $output) {
             // 작업 실패 시...
         });
```

<a name="pinging-urls"></a>
#### URL 푸싱 (Pinging URLs)

`pingBefore` 및 `thenPing` 메서드를 사용하면 작업 실행 전후에 특정 URL을 자동으로 ping(HTTP 요청)할 수 있습니다. 이는 [Envoyer](https://envoyer.io) 같은 외부 서비스에 작업 시작 또는 종료를 알릴 때 유용합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

`pingBeforeIf`와 `thenPingIf` 메서드는 주어진 조건이 `true`일 때만 URL을 ping하도록 할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

`pingOnSuccess`와 `pingOnFailure`는 작업 성공 또는 실패 때 각각 URL에 ping을 보냅니다. 실패는 비정상 종료를 의미합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

킷 모든 ping 관련 메서드는 Guzzle HTTP 라이브러리를 필요로 합니다. Laravel 프로젝트에는 기본으로 설치되어 있지만, 제거된 경우 Composer로 직접 설치하세요:

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## 이벤트 (Events)

필요하다면 스케줄러가 발생시키는 [이벤트](/docs/10.x/events)에 리스너를 달아 반응할 수도 있습니다. 보통 이벤트-리스너 매핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에서 정의합니다:

```php
/**
 * 애플리케이션의 이벤트-리스너 매핑.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Console\Events\ScheduledTaskStarting' => [
        'App\Listeners\LogScheduledTaskStarting',
    ],

    'Illuminate\Console\Events\ScheduledTaskFinished' => [
        'App\Listeners\LogScheduledTaskFinished',
    ],

    'Illuminate\Console\Events\ScheduledBackgroundTaskFinished' => [
        'App\Listeners\LogScheduledBackgroundTaskFinished',
    ],

    'Illuminate\Console\Events\ScheduledTaskSkipped' => [
        'App\Listeners\LogScheduledTaskSkipped',
    ],

    'Illuminate\Console\Events\ScheduledTaskFailed' => [
        'App\Listeners\LogScheduledTaskFailed',
    ],
];
```