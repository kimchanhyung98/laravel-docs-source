# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐잉된 잡 스케줄링](#scheduling-queued-jobs)
    - [쉘 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [시간대 설정](#timezones)
    - [작업 중첩 방지](#preventing-task-overlaps)
    - [한 서버에서 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
- [스케줄러 실행하기](#running-the-scheduler)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 후크](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 예약해야 하는 각 작업마다 별도의 cron 설정 항목을 작성했을 것입니다. 하지만 이렇게 되면 작업 스케줄이 소스 관리에서 벗어나고, 기존 cron 항목을 확인하거나 추가하려면 서버에 SSH로 접속해야 하기 때문에 불편해질 수 있습니다.

Laravel의 command scheduler는 서버에서 예약 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내에서 명령어 스케줄을 유창하고 표현력 있게 정의할 수 있습니다. 스케줄러를 사용할 경우 서버에는 단 하나의 cron 항목만 필요합니다. 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메서드 내에서 정의됩니다. 시작을 돕기 위해, 해당 메서드에 간단한 예제가 포함되어 있습니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

애플리케이션의 `App\Console\Kernel` 클래스의 `schedule` 메서드에서 모든 예약 작업을 정의할 수 있습니다. 우선 예제를 살펴보겠습니다. 이 예제에서는 자정마다 실행되는 클로저를 스케줄링하고, 클로저 내부에서 데이터베이스 쿼리를 실행하여 특정 테이블을 비우는 작업을 수행합니다:

```
<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{
    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        $schedule->call(function () {
            DB::table('recent_users')->delete();
        })->daily();
    }
}
```

클로저를 사용한 스케줄링 외에도, [인보커블 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 스케줄링할 수 있습니다. 인보커블 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다:

```
$schedule->call(new DeleteRecentUsers)->daily();
```

예약된 작업과 다음 실행 시간을 요약해서 보고 싶다면, `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저뿐만 아니라 [Artisan 명령어](/docs/9.x/artisan)와 시스템 명령어도 스케줄할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 Artisan 명령어를 이름 또는 클래스명을 통해 스케줄링할 수 있습니다.

클래스명을 통해 Artisan 명령어를 스케줄링할 때는, 호출 시 전달할 추가 명령줄 인수를 배열로 넘길 수 있습니다:

```
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐잉된 잡 스케줄링

`job` 메서드는 [큐잉된 잡](/docs/9.x/queues)을 스케줄링할 때 사용합니다. 이 메서드는 클로저를 정의하여 큐에 잡을 넣는 대신, 간편하게 잡을 예약할 수 있게 해줍니다:

```
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

선택적으로 두 번째와 세 번째 인수로 큐 이름과 큐 연결을 지정할 수 있습니다:

```
use App\Jobs\Heartbeat;

// "sqs" 연결의 "heartbeats" 큐에 잡을 디스패치...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 쉘 명령어 스케줄링

`exec` 메서드를 사용하면 운영체제에서 실행할 명령어를 지정할 수 있습니다:

```
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

이미 몇 가지 예시를 통해 작업을 특정 주기로 실행하는 방법을 보았습니다. 하지만 할당할 수 있는 스케줄 빈도는 훨씬 다양합니다:

| 메서드 | 설명 |
|-------------|-------------|
| `->cron('* * * * *');` | 작업을 커스텀 cron 스케줄에 맞춰 실행합니다 |
| `->everyMinute();` | 매분 작업 실행 |
| `->everyTwoMinutes();` | 2분마다 작업 실행 |
| `->everyThreeMinutes();` | 3분마다 작업 실행 |
| `->everyFourMinutes();` | 4분마다 작업 실행 |
| `->everyFiveMinutes();` | 5분마다 작업 실행 |
| `->everyTenMinutes();` | 10분마다 작업 실행 |
| `->everyFifteenMinutes();` | 15분마다 작업 실행 |
| `->everyThirtyMinutes();` | 30분마다 작업 실행 |
| `->hourly();` | 매시간 작업 실행 |
| `->hourlyAt(17);` | 매시간 17분에 작업 실행 |
| `->everyOddHour();` | 홀수 시간에 작업 실행 |
| `->everyTwoHours();` | 2시간마다 작업 실행 |
| `->everyThreeHours();` | 3시간마다 작업 실행 |
| `->everyFourHours();` | 4시간마다 작업 실행 |
| `->everySixHours();` | 6시간마다 작업 실행 |
| `->daily();` | 매일 자정에 작업 실행 |
| `->dailyAt('13:00');` | 매일 13시에 작업 실행 |
| `->twiceDaily(1, 13);` | 매일 1시와 13시에 작업 실행 |
| `->twiceDailyAt(1, 13, 15);` | 매일 1시 15분과 13시 15분에 작업 실행 |
| `->weekly();` | 매주 일요일 00시에 작업 실행 |
| `->weeklyOn(1, '8:00');` | 매주 월요일 8시에 작업 실행 |
| `->monthly();` | 매달 1일 00시에 작업 실행 |
| `->monthlyOn(4, '15:00');` | 매달 4일 15시에 작업 실행 |
| `->twiceMonthly(1, 16, '13:00');` | 매달 1일과 16일 13시에 작업 실행 |
| `->lastDayOfMonth('15:00');` | 매달 마지막 날 15시에 작업 실행 |
| `->quarterly();` | 매 분기 첫날 00시에 작업 실행 |
| `->quarterlyOn(4, '14:00');` | 매 분기 4일 14시에 작업 실행 |
| `->yearly();` | 매년 1월 1일 00시에 작업 실행 |
| `->yearlyOn(6, 1, '17:00');` | 매년 6월 1일 17시에 작업 실행 |
| `->timezone('America/New_York');` | 작업의 시간대 설정 |

이 메서드들은 추가 조건과 결합하여 요일별 제약 등 더욱 세밀한 스케줄을 만들 수 있습니다. 예를 들어 매주 월요일에 실행하도록 명령어를 예약할 수 있습니다:

```
// 매주 월요일 오후 1시에 한 번 실행...
$schedule->call(function () {
    //
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 한 시간마다 실행...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

아래는 추가적인 스케줄 제약 조건 목록입니다:

| 메서드 | 설명 |
|-------------|-------------|
| `->weekdays();` | 작업을 평일에만 제한 |
| `->weekends();` | 작업을 주말에만 제한 |
| `->sundays();` | 작업을 일요일에만 제한 |
| `->mondays();` | 작업을 월요일에만 제한 |
| `->tuesdays();` | 작업을 화요일에만 제한 |
| `->wednesdays();` | 작업을 수요일에만 제한 |
| `->thursdays();` | 작업을 목요일에만 제한 |
| `->fridays();` | 작업을 금요일에만 제한 |
| `->saturdays();` | 작업을 토요일에만 제한 |
| `->days(array\|mixed);` | 작업을 특정 요일에만 제한 |
| `->between($startTime, $endTime);` | 작업 실행 시간을 특정 시간 구간으로 제한 |
| `->unlessBetween($startTime, $endTime);` | 작업 실행을 특정 시간 구간에서 제외 |
| `->when(Closure);` | 참 테스트 결과에 따라 작업 실행 제한 |
| `->environments($env);` | 특정 환경에서만 작업 실행 제한 |

<a name="day-constraints"></a>
#### 요일 제한

`days` 메서드를 사용하면 작업 실행을 요일별로 제한할 수 있습니다. 예를 들어, 일요일과 수요일에 한 시간마다 실행하도록 스케줄링할 수 있습니다:

```
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

또는 `Illuminate\Console\Scheduling\Schedule` 클래스가 제공하는 상수를 사용해 요일을 정의할 수도 있습니다:

```
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 특정 시간 구간 제한

`between` 메서드는 작업이 실행되는 시간을 특정 시간대 사이로 제한할 때 사용합니다:

```
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

반대로 `unlessBetween` 메서드는 특정 시간 구간 동안 작업 실행을 제외하는 데 사용됩니다:

```
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건 검사에 따른 제한

`when` 메서드는 주어진 조건(clojure)이 `true`일 때만 작업을 실행하도록 제한할 수 있습니다. 즉, `when`에 넘긴 클로저가 `true`를 반환하면 해당 작업은 실행되며, 다른 제한 조건이 없다면 수행됩니다:

```
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

반대로 `skip` 메서드는 `when`의 반대 개념입니다. `skip`이 `true`를 반환하면 작업이 실행되지 않습니다:

```
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

체인으로 여러 `when` 메서드를 사용하면, 모든 `when` 조건이 참일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제한

`environments` 메서드는 작업이 특정 환경에서만 실행되도록 제한합니다. 환경은 `APP_ENV` [환경 변수](/docs/9.x/configuration#environment-configuration)를 기준으로 합니다:

```
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 시간대 설정

`timezone` 메서드를 사용하면 작업의 시간이 특정 시간대에 맞춰 해석되도록 지정할 수 있습니다:

```
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00');
```

만약 모든 작업에 반복해서 동일한 시간대를 지정한다면, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메서드를 정의할 수 있습니다. 이 메서드는 모든 작업에 기본으로 적용할 시간대를 반환해야 합니다:

```
/**
 * Get the timezone that should be used by default for scheduled events.
 *
 * @return \DateTimeZone|string|null
 */
protected function scheduleTimezone()
{
    return 'America/Chicago';
}
```

> [!WARNING]
> 일부 시간대는 일광 절약 시간제(Daylight Savings)를 사용합니다. 일광 절약 시간 변경이 발생하면 작업이 두 번 실행되거나 아예 실행되지 않을 수 있습니다. 따라서 가능하면 시간대 설정은 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 작업 중첩 방지

기본적으로 예약된 작업은 이전 작업 인스턴스가 실행 중이라도 계속 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```
$schedule->command('emails:send')->withoutOverlapping();
```

위 예제에서 `emails:send` Artisan 명령어는 실행 중이지 않을 경우 매분 실행됩니다. `withoutOverlapping`은 실행 시간이 크게 달라서 예상하기 어려운 작업에 매우 유용합니다.

필요하다면 중첩 방지 잠금의 만료 시간을 분 단위로 지정할 수도 있습니다. 기본 잠금 만료 시간은 24시간입니다:

```
$schedule->command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping`은 애플리케이션의 [캐시](/docs/9.x/cache)를 사용하여 잠금을 획득합니다. 만약 작업이 예상치 않게 중단되어 잠금이 풀리지 않는 경우, `schedule:clear-cache` Artisan 명령어로 캐시 잠금을 해제할 수 있습니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서 작업 실행

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션이 기본 캐시 드라이버로 `database`, `memcached`, `dynamodb` 또는 `redis` 중 하나를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신 중이어야 합니다.

여러 서버에서 스케줄러가 실행 중이라면, 특정 작업을 단 하나의 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어 매주 금요일 밤 새 리포트를 생성하는 작업이 있을 때, 작업 스케줄러가 3개의 워커 서버에서 같이 실행되면 작업이 3번 중복 실행되어 리포트도 3개 생성될 수 있습니다. 이는 원치 않는 상황입니다!

이런 경우 스케줄 작업에 `onOneServer` 메서드를 사용해 한 서버에서만 실행되도록 지정하세요. 작업을 가장 먼저 획득한 서버가 해당 작업에 원자적 잠금을 걸어 다른 서버가 동시에 실행하지 못하게 합니다:

```
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 이름 지정

같은 잡을 매개변수가 다르게 여러 개 스케줄링할 때, Laravel에게 각각의 작업이 별도로 원 서버에서만 실행되어야 함을 알릴 수 있습니다. 이를 위해 `name` 메서드로 각각 스케줄에 고유 이름을 지정할 수 있습니다:

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

마찬가지로, 스케줄된 클로저 역시 단일 서버 실행을 의도한다면 이름을 할당해야 합니다:

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로 같은 시간에 예약된 여러 작업은 `schedule` 메서드에서 정의된 순서대로 순차적으로 실행됩니다. 만약 오래 실행되는 작업이 있다면 이후 작업들이 예상보다 많이 늦게 시작될 수 있습니다. 모든 작업을 동시에 백그라운드로 실행하길 원할 경우, `runInBackground` 메서드를 사용할 수 있습니다:

```
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command`와 `exec` 메서드로 예약된 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/9.x/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 유지보수 중 서버에 영향을 주고 싶지 않기 때문입니다. 하지만 유지보수 모드에서도 특정 작업을 강제로 실행하려면 `evenInMaintenanceMode` 메서드를 호출하면 됩니다:

```
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행하기

스케줄된 작업을 정의했으니, 서버에서 실제로 실행하는 방법을 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 점검하여 서버 현재 시간 기준으로 실행이 필요한 작업을 실행합니다.

따라서 Laravel 스케줄러를 사용할 때 서버에 추가해야 할 cron 항목은 단 하나뿐입니다. 이 cron은 매분 `schedule:run`을 실행합니다. 서버에 cron 항목 추가 방법을 모른다면, [Laravel Forge](https://forge.laravel.com) 같은 서비스를 이용해 관리할 수도 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기

일반적으로 로컬 개발 환경에 스케줄러 cron 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용하세요. 이 명령어는 포그라운드에서 실행되며, 종료할 때까지 매분 스케줄러를 호출합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약 작업의 출력물을 다룰 여러 편리한 메서드를 제공합니다. 먼저 `sendOutputTo` 메서드를 사용하면 작업 출력 내용을 파일로 저장하여 나중에 확인할 수 있습니다:

```
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

출력을 파일에 덧붙이고 싶다면 `appendOutputTo` 메서드를 사용할 수 있습니다:

```
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드는 출력 내용을 지정한 이메일 주소로 보낼 수 있습니다. 이메일 전송 전에 Laravel 이메일 서비스를 적절히 설정해야 합니다:

```
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

예약된 Artisan 또는 시스템 명령어가 실패 (0이 아닌 종료 코드)했을 때만 이메일을 보내고 싶다면 `emailOutputOnFailure` 메서드를 사용하세요:

```
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드로 예약된 작업에만 적용됩니다.

<a name="task-hooks"></a>
## 작업 후크

`before`와 `after` 메서드를 사용하면 예약 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // 작업이 실행되기 직전...
         })
         ->after(function () {
             // 작업 실행 완료 후...
         });
```

`onSuccess`와 `onFailure` 메서드는 작업 성공 또는 실패 시 실행할 코드를 지정합니다. 실패는 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우를 의미합니다:

```
$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function () {
             // 작업 성공 시...
         })
         ->onFailure(function () {
             // 작업 실패 시...
         });
```

만약 명령어의 출력이 존재한다면, `after`, `onSuccess`, `onFailure` 후크에 `Illuminate\Support\Stringable` 타입 힌트를 주어 `$output` 인수로 전달받아 출력 내용에 접근할 수 있습니다:

```
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
#### URL 핑하기

`schedule`은 `pingBefore`와 `thenPing` 메서드를 제공하여 작업 실행 전후에 지정 URL에 자동으로 핑을 보낼 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io) 같은 외부 서비스에 작업 시작 및 완료 알림을 보내는 등 유용합니다:

```
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

`pingBeforeIf`와 `thenPingIf` 메서드는 특정 조건이 참일 때만 URL에 핑을 보냅니다:

```
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

`pingOnSuccess`와 `pingOnFailure` 메서드는 작업이 성공하거나 실패했을 때만 특정 URL에 핑을 보냅니다. 실패는 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우입니다:

```
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

모든 핑 메서드는 Guzzle HTTP 라이브러리를 필요로 합니다. Laravel 신규 프로젝트에는 기본 설치되어 있지만, 실수로 제거된 경우 Composer로 직접 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## 이벤트

필요하다면 스케줄러가 발행하는 [이벤트](/docs/9.x/events)를 수신할 수 있습니다. 일반적으로 이벤트와 리스너 매핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 정의합니다:

```
/**
 * The event listener mappings for the application.
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