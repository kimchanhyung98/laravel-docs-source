# 작업 스케줄링

- [소개](#introduction)
- [스케줄 정의](#defining-schedules)
    - [Artisan 명령 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 방지](#preventing-task-overlaps)
    - [한 서버에서만 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
- [스케줄러 실행](#running-the-scheduler)
    - [1분 이하(초 단위) 작업 스케줄](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 스케줄링이 필요한 각 작업마다 별도의 크론(cron) 설정을 작성했을 수 있습니다. 하지만 이렇게 하면 소스 관리에서 스케줄 구성이 분리되고, 기존 크론 항목을 확인하거나 추가하려면 SSH로 서버에 직접 접속해야 하므로 상당히 번거로울 수 있습니다.

Laravel의 명령어 스케줄러를 사용하면 서버에서 예약된 작업을 보다 일관되고 쉽게 관리할 수 있습니다. 이 스케줄러는 명령 스케줄을 Laravel 애플리케이션 내에서 유창하고 표현적으로 정의할 수 있도록 해줍니다. 스케줄러를 사용할 경우, 서버에는 단 하나의 크론 항목만 필요합니다. 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메소드 내에 정의합니다. 시작을 돕기 위해 간단한 예제 코드도 메소드에 포함되어 있습니다.

<a name="defining-schedules"></a>
## 스케줄 정의

모든 예약 작업은 애플리케이션의 `App\Console\Kernel` 클래스의 `schedule` 메소드에서 정의할 수 있습니다. 먼저 예제부터 살펴보겠습니다. 이 예제에서는 매일 자정에 실행되는 클로저를 예약합니다. 클로저 내부에서는 데이터베이스 쿼리를 실행하여 테이블을 비웁니다:

```php
<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{
    /**
     * 애플리케이션 명령어 스케줄 정의.
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->call(function () {
            DB::table('recent_users')->delete();
        })->daily();
    }
}
```

클로저를 사용하는 것 외에도, [호출 가능한 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 예약할 수도 있습니다. 호출 가능한 객체란 `__invoke` 메소드를 가진 단순 PHP 클래스를 의미합니다:

```php
$schedule->call(new DeleteRecentUsers)->daily();
```

예약된 작업의 개요와 다음 실행 예정 시각을 확인하고 싶다면, `schedule:list` Artisan 명령을 사용할 수 있습니다:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령 스케줄링

클로저 스케줄링 외에도 [Artisan 명령](/docs/{{version}}/artisan)과 시스템 명령을 예약할 수 있습니다. 예를 들어, `command` 메소드로 Artisan 명령의 이름이나 클래스를 사용해 예약할 수 있습니다.

명령 클래스 이름을 사용해 Artisan 명령을 예약할 땐, 해당 명령 실행 시 전달할 명령줄 인수를 배열로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메소드는 [큐 작업](/docs/{{version}}/queues) 예약에 사용할 수 있습니다. 이 메소드는 클로저를 통해 큐 작업을 예약하지 않고도 편리하게 큐 작업을 예약할 수 있습니다:

```php
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

선택적으로, `job` 메소드에 두 번째 및 세 번째 인수로 큐 이름과 큐 커넥션을 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;

// "heartbeats" 큐에, "sqs" 커넥션으로 작업 디스패치
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령 스케줄링

`exec` 메소드를 이용해 운영체제 명령을 실행할 수 있습니다:

```php
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

지정된 간격으로 작업을 실행하도록 구성하는 예제를 이미 살펴봤습니다. 하지만, 작업에 할당할 수 있는 다양한 스케줄 빈도 옵션이 더 많습니다:

<div class="overflow-auto">

메소드  | 설명
------------- | -------------
`->cron('* * * * *');`  |  커스텀 크론 일정에 작업 실행
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
`->hourly();`  |  매 시간 작업 실행
`->hourlyAt(17);`  |  매 시간 17분에 작업 실행
`->everyOddHour($minutes = 0);`  |  홀수 시간마다 작업 실행
`->everyTwoHours($minutes = 0);`  |  2시간마다 작업 실행
`->everyThreeHours($minutes = 0);`  |  3시간마다 작업 실행
`->everyFourHours($minutes = 0);`  |  4시간마다 작업 실행
`->everySixHours($minutes = 0);`  |  6시간마다 작업 실행
`->daily();`  |  매일 자정에 작업 실행
`->dailyAt('13:00');`  |  매일 13:00에 작업 실행
`->twiceDaily(1, 13);`  |  매일 1:00, 13:00에 작업 실행
`->twiceDailyAt(1, 13, 15);`  |  매일 1:15, 13:15에 작업 실행
`->weekly();`  |  매주 일요일 00:00에 작업 실행
`->weeklyOn(1, '8:00');`  |  매주 월요일 8:00에 작업 실행
`->monthly();`  |  매달 1일 00:00에 작업 실행
`->monthlyOn(4, '15:00');`  |  매달 4일 15:00에 작업 실행
`->twiceMonthly(1, 16, '13:00');`  |  매달 1일, 16일 13:00에 작업 실행
`->lastDayOfMonth('15:00');` | 매월 마지막 날 15:00에 작업 실행
`->quarterly();` |  분기 첫날 00:00에 작업 실행
`->quarterlyOn(4, '14:00');` |  분기마다 4일 14:00에 작업 실행
`->yearly();`  |  매년 1월 1일 00:00에 작업 실행
`->yearlyOn(6, 1, '17:00');`  |  매년 6월 1일 17:00에 작업 실행
`->timezone('America/New_York');` | 작업의 타임존 설정

</div>

이 메소드들은 추가적인 제약 조건과 함께 조합해 특정 요일에만 동작하도록 섬세하게 스케줄을 구성할 수 있습니다. 예를 들어, 매주 월요일에 명령어를 실행하고자 할 때는 다음과 같이 작성할 수 있습니다:

```php
// 매주 월요일 오후 1시에 한 번 실행...
$schedule->call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 매 시간 실행...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

아래는 추가적인 스케줄 제약 조건 목록입니다:

<div class="overflow-auto">

메소드  | 설명
------------- | -------------
`->weekdays();`  |  평일에만 작업 제한
`->weekends();`  |  주말에만 작업 제한
`->sundays();`  |  일요일에만 작업 제한
`->mondays();`  |  월요일에만 작업 제한
`->tuesdays();`  |  화요일에만 작업 제한
`->wednesdays();`  |  수요일에만 작업 제한
`->thursdays();`  |  목요일에만 작업 제한
`->fridays();`  |  금요일에만 작업 제한
`->saturdays();`  |  토요일에만 작업 제한
`->days(array\|mixed);`  |  특정 요일에만 작업 제한
`->between($startTime, $endTime);`  |  특정 시간 사이에만 작업 실행
`->unlessBetween($startTime, $endTime);`  |  특정 시간 사이에는 작업 실행 안 함
`->when(Closure);`  |  참/거짓 조건에 따라 작업 실행 제한
`->environments($env);`  |  특정 환경에서만 작업 실행

</div>

<a name="day-constraints"></a>
#### 요일 제약

`days` 메소드는 작업 실행을 특정 요일로 제한할 수 있습니다. 예를 들어, 매시간 일요일과 수요일에 명령을 실행할 수 있습니다:

```php
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

또는, 작업이 실행될 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 특정 시간대 제약

`between` 메소드는 하루 중 특정 시간에만 작업을 실행하도록 제한할 수 있습니다:

```php
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

유사하게, `unlessBetween` 메소드는 특정 시간대에는 작업이 실행되지 않도록 설정할 수 있습니다:

```php
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 참/거짓(Truth Test) 제약

`when` 메소드는 주어진 조건의 참/거짓에 따라 작업의 실행을 제한할 수 있습니다. 다시 말해, 전달한 클로저가 `true`를 반환하면, 다른 제약 조건이 없을 경우 해당 작업이 실행됩니다:

```php
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메소드는 `when`의 반대 역할을 합니다. `skip`이 `true`를 반환하면, 작업은 실행되지 않습니다:

```php
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

여러 `when` 메소드를 체이닝할 경우, 모든 `when` 조건이 모두 `true`여야 명령어가 실행됩니다.

<a name="environment-constraints"></a>
#### 환경(Environments) 제약

`environments` 메소드를 이용해 특정 환경(예: 프로덕션, 스테이징 등)에서만 작업이 실행되도록 제한할 수 있습니다. 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 정의됩니다:

```php
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존

`timezone` 메소드를 사용하면 예약된 작업의 시간이 특정 타임존 기준으로 해석되도록 지정할 수 있습니다:

```php
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00')
```

모든 작업에 동일한 타임존을 반복적으로 할당하게 된다면, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메소드를 정의하는 것이 좋습니다. 이 메소드는 모든 예약 작업에 기본으로 할당될 타임존을 반환해야 합니다:

```php
use DateTimeZone;

/**
 * 예약 이벤트의 기본 타임존 반환.
 */
protected function scheduleTimezone(): DateTimeZone|string|null
{
    return 'America/Chicago';
}
```

> [!WARNING]  
> 일부 타임존은 일광절약시간제(DST)를 적용합니다. 일광절약시간 변경이 발생하는 경우, 예약된 작업이 두 번 실행되거나 아예 실행되지 않을 수도 있습니다. 따라서 가능하다면 타임존 스케줄링은 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 방지

기본적으로 예약된 작업은 이전 인스턴스가 아직 실행 중이어도 새롭게 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메소드를 사용할 수 있습니다:

```php
$schedule->command('emails:send')->withoutOverlapping();
```

이 예제에서는 `emails:send` [Artisan 명령](/docs/{{version}}/artisan)이 이미 실행 중이 아니라면 매분 실행됩니다. 실행 시간이 예측 불가한 작업의 중복 실행을 방지하는 데 유용합니다.

필요하다면 중복 방지 잠금(락)이 만료되기까지 지난 분(minutes) 수를 명시할 수 있습니다. 기본으로는 24시간 후 만료됩니다:

```php
$schedule->command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping` 메소드는 애플리케이션의 [캐시](/docs/{{version}}/cache)를 사용해 Lock을 얻습니다. 예기치 못한 서버 문제로 작업이 멈췄다면 `schedule:clear-cache` Artisan 명령으로 Lock을 수동으로 해제할 수 있습니다. 단, 보통은 필요하지 않습니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서만 작업 실행

> [!WARNING]  
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis`여야 하며, 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

애플리케이션의 스케줄러가 여러 서버에서 작동할 때, 작업을 단 한 서버에서만 실행할 수 있습니다. 예를 들어, 금요일 밤 새로운 리포트를 생성하는 작업이 있고, 스케줄러가 세 대의 워커 서버에서 실행 중이라면 모든 서버가 리포트를 각각 생성하게 됩니다. 이는 원치 않는 동작입니다!

작업을 한 서버에서만 실행하려면, 작업 정의 시 `onOneServer` 메소드를 사용하세요. 작업을 가장 먼저 잡은 서버가 해당 작업의 원자적 락(Lock)을 획득해 다른 서버의 동시 실행을 방지합니다:

```php
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 이름 지정

동일한 작업을 서로 다른 매개변수와 함께 예약하면서도, 각 조합별 작업을 단일 서버에서만 실행하도록 하려면 `name` 메소드로 각 스케줄 정의에 고유 이름을 지정하면 됩니다:

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

마찬가지로, 예약된 클로저도 한 서버에서만 실행하려면 반드시 이름을 지정해야 합니다:

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로, 동일한 시간에 예약된 여러 작업은 `schedule` 메소드에 정의된 순서대로 순차 실행됩니다. 장시간 실행되는 작업이 있으면 이후 작업이 늦게 시작될 수 있습니다. 모든 작업을 동시에 병렬로 실행하려면 `runInBackground` 메소드를 사용하세요:

```php
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!WARNING]  
> `runInBackground` 메소드는 오직 `command` 및 `exec` 메소드로 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)일 때에는, 유지보수 중인 서버에 불필요한 작업이 영향 주는 것을 막기 위해 예약 작업이 실행되지 않습니다. 만약 유지보수 모드에서도 특정 작업을 강제로 실행하고 싶다면, `evenInMaintenanceMode` 메소드를 작업에 추가하세요:

```php
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행

작업 예약 정의법을 익혔다면, 실제로 서버에서 어떻게 실행하는지도 알아보죠. `schedule:run` Artisan 명령은 모든 예약된 작업을 평가하여 서버의 현재 시간에 따라 실행할지 결정합니다.

따라서, Laravel 스케줄러를 사용할 경우, `schedule:run` 명령을 매분 실행시키는 단일 크론 항목만 서버에 추가하면 됩니다. 크론 항목 추가 방법을 모른다면, [Laravel Forge](https://forge.laravel.com)와 같은 서비스를 통해 쉽게 관리할 수도 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만(초 단위) 작업 스케줄

대부분의 운영 체제에서 크론 작업은 최대 분 단위로만 실행 가능합니다. 하지만 Laravel 스케줄러는 초 단위 등 더 자주 실행되도록 작업을 예약할 수 있습니다:

```php
$schedule->call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션에 1분 미만의 작업이 정의된 경우, `schedule:run` 명령은 바로 종료되지 않고 해당 분이 끝날 때까지 계속 실행됩니다. 이를 통해 필요한 모든 1분 미만 작업을 계속 호출할 수 있습니다.

예상보다 오래 걸리는 1분 미만 작업으로 인해 이후 sub-minute 작업 실행이 지연되지 않도록, 모든 1분 미만 예약 작업을 큐 작업으로 디스패치하거나 백그라운드 명령으로 실행하길 권장합니다:

```php
use App\Jobs\DeleteRecentUsers;

$schedule->job(new DeleteRecentUsers)->everyTenSeconds();

$schedule->command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단(인터럽트)

sub-minute 작업이 정의된 상태에서 `schedule:run` 명령이 해당 분 동안 계속 실행되므로, 배포(deploy) 시 해당 명령을 중단(인터럽트)해야 할 수도 있습니다. 그렇지 않으면 이미 실행 중인 `schedule:run` 명령이 해당 분이 끝날 때까지 기존 코드를 계속 사용할 수 있습니다.

진행 중인 `schedule:run` 실행을 중단하려면, 배포 스크립트에 `schedule:interrupt` 명령을 추가하세요. 이 명령은 배포가 끝난 후에 실행하면 됩니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

일반적으로 로컬 개발 환경에서는 크론 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령을 사용할 수 있습니다. 이 명령은 포그라운드에서 계속 실행되며, 중단할 때까지 매분 스케줄러를 호출합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약 작업이 생성하는 출력을 다루는 편리한 메소드를 제공합니다. 먼저, `sendOutputTo` 메소드를 사용해 출력을 파일에 기록할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

출력을 파일에 덧붙이고 싶다면, `appendOutputTo` 메소드를 사용할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

`emailOutputTo` 메소드를 사용하면 출력을 원하는 이메일 주소로 전송할 수 있습니다. 이 작업 전에는 Laravel의 [이메일 서비스](/docs/{{version}}/mail)를 반드시 설정해야 합니다:

```php
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

예약된 Artisan 또는 시스템 명령이 0이 아닌 종료 코드로 종료될 때만 이메일 알림을 보내고 싶다면, `emailOutputOnFailure` 메소드를 사용하세요:

```php
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]  
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메소드는 `command`, `exec` 메소드에만 적용됩니다.

<a name="task-hooks"></a>
## 작업 훅

`before`와 `after` 메소드를 사용해 예약 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // 작업이 곧 실행됩니다...
         })
         ->after(function () {
             // 작업이 실행되었습니다...
         });
```

`onSuccess`와 `onFailure` 메소드를 이용하면 작업이 성공 또는 실패했을 때 실행할 코드를 지정할 수 있습니다. 실패란 예약된 Artisan 또는 시스템 명령이 0이 아닌 종료 코드로 종료됨을 의미합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function () {
             // 작업이 성공했습니다...
         })
         ->onFailure(function () {
             // 작업이 실패했습니다...
         });
```

명령의 출력이 있다면, `after`, `onSuccess`, `onFailure` 훅의 클로저 정의에서 `$output` 매개변수로 `Illuminate\Support\Stringable` 인스턴스를 타입힌트 해 출력값에 접근할 수 있습니다:

```php
use Illuminate\Support\Stringable;

$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function (Stringable $output) {
             // 작업이 성공했습니다...
         })
         ->onFailure(function (Stringable $output) {
             // 작업이 실패했습니다...
         });
```

<a name="pinging-urls"></a>
#### URL Ping

`pingBefore`와 `thenPing` 메소드를 사용하면 작업 실행 전 또는 후에 지정된 URL을 자동으로 핑할 수 있습니다. 이 방법은 [Envoyer](https://envoyer.io) 등 외부 서비스에 예약 작업이 시작/종료됨을 알리는 데 유용합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

`pingBeforeIf`, `thenPingIf` 메소드는 주어진 조건이 `true`일 때만 URL을 핑할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

`pingOnSuccess`와 `pingOnFailure` 메소드는 작업이 성공 또는 실패한 경우에만 URL을 핑할 수 있습니다. 실패란 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우입니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

모든 핑 메소드는 Guzzle HTTP 라이브러리가 필요합니다. Guzzle은 대부분의 신규 Laravel 프로젝트에 기본적으로 설치되어 있지만, 만약 제거되었거나 없다면 Composer 패키지 관리자로 직접 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## 이벤트

필요하다면, 스케줄러가 발생시키는 [이벤트](/docs/{{version}}/events)를 수신할 수 있습니다. 보통 이벤트 리스너 매핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스 내에 정의됩니다:

```php
/**
 * 애플리케이션 이벤트 리스너 매핑.
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
