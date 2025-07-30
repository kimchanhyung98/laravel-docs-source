# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [대기열 작업 스케줄링](#scheduling-queued-jobs)
    - [쉘 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 실행 주기 옵션](#schedule-frequency-options)
    - [시간대 설정](#timezones)
    - [작업 중복 실행 방지](#preventing-task-overlaps)
    - [단일 서버에서 작업 실행하기](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
- [스케줄러 실행하기](#running-the-scheduler)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 후크](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

과거에는 서버에서 예약해야 할 각 작업마다 크론(cron) 설정 항목을 직접 작성했을 것입니다. 하지만 이렇게 하면 작업 스케줄이 소스 컨트롤에 포함되지 않고, 기존 크론 항목을 확인하거나 추가하려면 서버에 SSH로 접속해야 하기 때문에 관리가 불편해집니다.

Laravel의 명령어 스케줄러는 서버에 예약된 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내에서 명령어 스케줄을 유창하고 표현력 있게 정의할 수 있습니다. 이를 사용하면 서버에는 단 한 개의 크론 항목만 있으면 되고, 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메서드 내에 정의됩니다. 시작하기 쉽게, 해당 메서드 내에 간단한 예제가 정의되어 있습니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기 (Defining Schedules)

모든 예약 작업은 애플리케이션의 `App\Console\Kernel` 클래스 내의 `schedule` 메서드에서 정의할 수 있습니다. 우선, 간단한 예제를 살펴봅시다. 이 예제에서는 매일 자정에 실행될 클로저(무명 함수)를 스케줄링합니다. 클로저 내부에서는 데이터베이스 쿼리를 실행해 특정 테이블을 비우는 작업을 수행합니다:

```
<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{
    /**
     * 애플리케이션의 명령어 스케줄을 정의합니다.
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

클로저를 이용한 스케줄링 이외에도 [호출 가능한 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 사용할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함하는 간단한 PHP 클래스입니다:

```
$schedule->call(new DeleteRecentUsers)->daily();
```

예약된 작업과 다음 실행 예정 시각을 한눈에 확인하고 싶다면 `schedule:list` Artisan 명령어를 사용하세요:

```nothing
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링 (Scheduling Artisan Commands)

클로저 외에 [Artisan 명령어](/docs/{{version}}/artisan) 및 시스템 명령어도 스케줄할 수 있습니다. 예를 들어, `command` 메서드를 사용해 명령어의 이름이나 클래스 이름으로 Artisan 명령어를 스케줄링할 수 있습니다.

명령어 클래스 이름을 사용해 Artisan 명령어를 스케줄링할 때는, 명령어 호출 시 전달할 추가 커맨드라인 인수를 배열로 넘길 수 있습니다:

```
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 대기열 작업 스케줄링 (Scheduling Queued Jobs)

`job` 메서드는 [대기열 작업](/docs/{{version}}/queues) 스케줄링에 사용할 수 있습니다. 이 방법은 클로저를 정의해 작업을 대기열에 넣는 `call` 메서드 대신에 간편하게 대기열 작업을 예약할 수 있게 해줍니다:

```
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

선택적으로 `job` 메서드에 두 번째와 세 번째 인수로 대기열 이름과 대기열 연결을 지정할 수 있습니다:

```
use App\Jobs\Heartbeat;

// "sqs" 연결의 "heartbeats" 대기열에 작업을 보내기...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 쉘 명령어 스케줄링 (Scheduling Shell Commands)

`exec` 메서드는 운영체제(OS) 쉘 명령어를 실행할 때 사용합니다:

```
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 실행 주기 옵션 (Schedule Frequency Options)

지금까지 작업을 특정 간격으로 실행하는 몇 가지 예시를 살펴보았습니다. 하지만 작업에 지정할 수 있는 다양한 실행 주기가 더 많이 있습니다:

| 메서드                | 설명                                  |
|-----------------------|-------------------------------------|
| `->cron('* * * * *');`   | 커스텀 크론 스케줄로 작업 실행           |
| `->everyMinute();`       | 매 분마다 작업 실행                     |
| `->everyTwoMinutes();`   | 매 2분마다 작업 실행                   |
| `->everyThreeMinutes();` | 매 3분마다 작업 실행                   |
| `->everyFourMinutes();`  | 매 4분마다 작업 실행                   |
| `->everyFiveMinutes();`  | 매 5분마다 작업 실행                   |
| `->everyTenMinutes();`   | 매 10분마다 작업 실행                  |
| `->everyFifteenMinutes();` | 매 15분마다 작업 실행                |
| `->everyThirtyMinutes();` | 매 30분마다 작업 실행                 |
| `->hourly();`            | 매 시간 작업 실행                      |
| `->hourlyAt(17);`        | 매 시간 17분에 작업 실행                |
| `->everyTwoHours();`     | 매 2시간마다 작업 실행                  |
| `->everyThreeHours();`   | 매 3시간마다 작업 실행                  |
| `->everyFourHours();`    | 매 4시간마다 작업 실행                  |
| `->everySixHours();`     | 매 6시간마다 작업 실행                  |
| `->daily();`             | 매일 자정에 작업 실행                   |
| `->dailyAt('13:00');`    | 매일 13시에 작업 실행                   |
| `->twiceDaily(1, 13);`   | 매일 1시와 13시에 작업 실행              |
| `->weekly();`            | 매주 일요일 00:00에 작업 실행            |
| `->weeklyOn(1, '8:00');` | 매주 월요일 8시에 작업 실행              |
| `->monthly();`           | 매월 1일 00:00에 작업 실행               |
| `->monthlyOn(4, '15:00');` | 매월 4일 15시에 작업 실행             |
| `->twiceMonthly(1, 16, '13:00');` | 매월 1일과 16일 13시에 작업 실행 |
| `->lastDayOfMonth('15:00');` | 매월 마지막 날 15시에 작업 실행        |
| `->quarterly();`         | 분기별 첫날 00:00에 작업 실행            |
| `->yearly();`            | 매년 1월 1일 00:00에 작업 실행            |
| `->yearlyOn(6, 1, '17:00');` | 매년 6월 1일 17시에 작업 실행         |
| `->timezone('America/New_York');` | 작업 시간대 설정                    |

이 메서드들은 요일별로 실행하는 등 더 세밀하게 조건을 조합할 때 함께 사용할 수 있습니다. 예를 들어 매주 월요일에 실행하도록 하려면 다음과 같이 작성합니다:

```
// 매주 월요일 오후 1시에 한 번 실행...
$schedule->call(function () {
    //
})->weekly()->mondays()->at('13:00');

// 주중 8시부터 17시까지 매 시간마다 실행...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

아래는 추가로 사용할 수 있는 스케줄 제한 조건 목록입니다:

| 메서드                 | 설명                                   |
|------------------------|--------------------------------------|
| `->weekdays();`          | 평일에만 작업 실행 제한                   |
| `->weekends();`          | 주말에만 작업 실행 제한                   |
| `->sundays();`           | 일요일에만 작업 실행 제한                  |
| `->mondays();`           | 월요일에만 작업 실행 제한                  |
| `->tuesdays();`          | 화요일에만 작업 실행 제한                  |
| `->wednesdays();`        | 수요일에만 작업 실행 제한                  |
| `->thursdays();`         | 목요일에만 작업 실행 제한                  |
| `->fridays();`           | 금요일에만 작업 실행 제한                  |
| `->saturdays();`         | 토요일에만 작업 실행 제한                  |
| `->days(array\|mixed);`    | 특정 요일에만 작업 실행 제한                |
| `->between($startTime, $endTime);` | 지정된 시간 사이에만 작업 실행 제한       |
| `->unlessBetween($startTime, $endTime);` | 지정된 시간 사이에는 작업 실행 제한    |
| `->when(Closure);`       | 주어진 조건에 따라 작업 실행 제한              |
| `->environments($env);`  | 특정 환경에서만 작업 실행 제한                |

<a name="day-constraints"></a>
#### 요일 제한 (Day Constraints)

`days` 메서드는 작업 실행 요일을 제한할 때 사용합니다. 예를 들어, 매주 일요일과 수요일에만 작업을 시간 단위로 실행하도록 예약할 수 있습니다:

```
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

또는 `Illuminate\Console\Scheduling\Schedule` 클래스가 제공하는 상수를 사용할 수도 있습니다:

```
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간 범위 제한 (Between Time Constraints)

`between` 메서드는 작업 실행을 특정 시간 범위 내로 제한합니다:

```
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

반대로 `unlessBetween` 메서드는 지정한 시간 범위 내에서는 작업 실행을 제외합니다:

```
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건 기반 제한 (Truth Test Constraints)

`when` 메서드는 주어진 조건(클로저)의 반환값이 true일 때만 작업이 실행되도록 제한합니다. 다시 말해, 클로저가 true를 반환하고 다른 제한 조건들이 작업 실행을 막지 않으면, 작업이 실행됩니다:

```
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when` 메서드의 반대 개념으로, 클로저가 true를 반환하면 작업이 실행되지 않습니다:

```
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

체인으로 여러 개의 `when`을 사용하면 모두 true를 반환해야 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제한 (Environment Constraints)

`environments` 메서드는 주어진 환경에서만 작업이 실행되도록 제한합니다. 환경은 `APP_ENV` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 정의된 값입니다:

```
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 시간대 설정 (Timezones)

`timezone` 메서드를 사용하면 예약 작업의 시간이 지정한 시간대 기준으로 해석되도록 설정할 수 있습니다:

```
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00')
```

만약 모든 예약 작업에 동일한 시간대를 반복해서 지정한다면, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메서드를 정의해 기본 시간대를 설정할 수 있습니다:

```
/**
 * 예약 이벤트에 기본으로 사용할 시간대를 반환합니다.
 *
 * @return \DateTimeZone|string|null
 */
protected function scheduleTimezone()
{
    return 'America/Chicago';
}
```

> [!NOTE]
> 일부 시간대는 일광 절약 시간제(Daylight Savings Time)를 사용합니다. 일광 절약 시간 변경 시 예약 작업이 두 번 실행되거나 아예 실행되지 않을 수 있으니, 가능하면 시간대 스케줄링 사용을 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 실행 방지 (Preventing Task Overlaps)

기본적으로 예약 작업은 이전 작업 인스턴스가 아직 실행 중이어도 다시 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요:

```
$schedule->command('emails:send')->withoutOverlapping();
```

예를 들어, `emails:send` [Artisan 명령어](/docs/{{version}}/artisan)는 실행 중이 아니면 매 분 실행됩니다. 실행 시간이 들쭉날쭉한 작업에 특히 유용하며, 특정 작업 실행 시간을 정확히 예측하기 어려울 때 중복 실행을 막아줍니다.

기본적으로 "중복 방지" 락(lock)은 24시간 후 만료됩니다. 만약 락 유지 시간을 분 단위로 변경하고 싶다면 인수를 전달할 수 있습니다:

```
$schedule->command('emails:send')->withoutOverlapping(10);
```

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 작업 실행하기 (Running Tasks On One Server)

> [!NOTE]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis` 중 하나이고, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

스케줄러가 여러 서버에서 실행 중이라면, 특정 작업을 오직 한 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어 매주 금요일 밤마다 새로운 보고서를 생성하는 작업이 있다고 가정할 때, 세 대의 작업자 서버에서 스케줄러가 돌고 있다면, 작업이 세 번 중복 실행되어 보고서가 세 개가 만들어질 수 있습니다. 이는 원하지 않는 결과입니다.

작업을 한 대 서버에서만 실행하도록 하려면, `onOneServer` 메서드를 지정하세요. 작업을 가장 먼저 획득한 서버가 원자적 잠금을 걸어 다른 서버가 동시에 같은 작업을 실행하지 못하게 합니다:

```
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업 (Background Tasks)

기본적으로 같은 시각에 예약된 여러 작업은 `schedule` 메서드 내 정의 순서대로 순차적으로 실행됩니다. 만약 오래 걸리는 작업이 있다면 이후 작업 실행이 예상보다 늦어질 수 있습니다. 모든 작업을 동시에 실행하도록 백그라운드 처리하고 싶다면 `runInBackground` 메서드를 사용하세요:

```
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!NOTE]
> `runInBackground` 메서드는 `command`와 `exec` 메서드로 예약한 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드 (Maintenance Mode)

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)일 때는 예약 작업이 실행되지 않습니다. 이는 유지보수 중인 서버에 작업이 영향을 주지 않도록 하기 위함입니다. 만약 유지보수 모드에서도 작업을 강제로 실행하려면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하세요:

```
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행하기 (Running The Scheduler)

이제 예약 작업을 정의했으니, 실제 서버에서 작업을 실행하는 방법을 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가해 현재 서버 시간 기준으로 실행이 필요한 작업을 실행합니다.

따라서 Laravel 스케줄러를 사용할 때는 서버에 단 한 개 크론 설정만 추가하면 됩니다. 이 크론은 매 분마다 `schedule:run` 명령어를 실행합니다. 서버에 크론 항목을 추가하는 방법을 모른다면, 크론 관리를 대신해주는 [Laravel Forge](https://forge.laravel.com) 같은 서비스를 이용해 보세요:

    * * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기 (Running The Scheduler Locally)

로컬 개발 환경에서는 일반적으로 별도의 크론 항목을 등록하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며, 직접 종료할 때까지 매 분 스케줄러를 호출합니다:

```
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

Laravel 스케줄러는 예약 작업에서 생성된 출력을 쉽게 처리하도록 여러 메서드를 제공합니다. 먼저 `sendOutputTo` 메서드를 사용하면 출력 내용을 특정 파일에 저장해 나중에 확인할 수 있습니다:

```
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

출력 내용을 파일에 덧붙이려면 `appendOutputTo` 메서드를 사용하세요:

```
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 출력 내용을 원하는 이메일 주소로 전송할 수 있습니다. 이메일 발송 전에 Laravel의 [메일 서비스](/docs/{{version}}/mail)를 설정해야 합니다:

```
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료될 때만 이메일을 보내려면 `emailOutputOnFailure` 메서드를 사용하세요:

```
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!NOTE]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드로 예약한 작업에만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 후크 (Task Hooks)

`schedule` 메서드에서 `before`, `after` 메서드를 사용하면, 예약 작업 실행 전후에 코드를 실행하도록 설정할 수 있습니다:

```
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // 작업 실행 직전...
         })
         ->after(function () {
             // 작업 실행 완료 후...
         });
```

`onSuccess`, `onFailure` 메서드는 예약 작업이 성공하거나 실패했을 때 실행할 코드를 정의합니다. 실패는 명령이 0이 아닌 종료 코드로 끝난 경우를 의미합니다:

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

명령의 출력이 있을 경우, 후크 함수에 `Illuminate\Support\Stringable` 타입 힌트를 추가해 출력 내용을 받을 수 있습니다 (`after`, `onSuccess`, `onFailure`):

```
use Illuminate\Support\Stringable;

$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function (Stringable $output) {
             // 작업 성공 시 출력 접근 가능...
         })
         ->onFailure(function (Stringable $output) {
             // 작업 실패 시 출력 접근 가능...
         });
```

<a name="pinging-urls"></a>
#### URL 핑 보내기 (Pinging URLs)

`schedule` 메서드에서 `pingBefore`와 `thenPing` 메서드를 사용하면, 작업 실행 전후로 특정 URL에 자동 핑을 보낼 수 있습니다. 이것은 [Envoyer](https://envoyer.io) 같은 외부 서비스에 작업 시작 및 완료를 알리는데 유용합니다:

```
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

조건을 만족할 때만 핑을 보내려면 각각 `pingBeforeIf`, `thenPingIf` 메서드를 사용합니다:

```
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

작업 성공 시와 실패 시에 각각 핑을 보내려면 `pingOnSuccess`, `pingOnFailure` 메서드를 사용하세요. 실패는 명령어가 0이 아닌 종료 코드로 끝난 경우입니다:

```
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

이 모든 핑 메서드들은 Guzzle HTTP 라이브러리를 필요로 합니다. Laravel 새 프로젝트에는 기본적으로 Guzzle이 설치되어 있지만, 만약 삭제되었다면 Composer로 다시 설치할 수 있습니다:

```
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## 이벤트 (Events)

필요하다면 스케줄러가 발생시키는 [이벤트](/docs/{{version}}/events)를 청취할 수 있습니다. 일반적으로 이벤트-리스너 매핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 정의합니다:

```
/**
 * 애플리케이션의 이벤트 리스너 매핑.
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