# 작업 스케줄링

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업(Job) 스케줄링](#scheduling-queued-jobs)
    - [셸 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 방지](#preventing-task-overlaps)
    - [단일 서버에서 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
- [스케줄러 실행하기](#running-the-scheduler)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅(Hook)](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 스케줄링해야 하는 각 작업마다 크론(cron) 설정 항목을 작성했을 것입니다. 하지만 이렇게 하면 작업 스케줄이 더 이상 소스 관리에 포함되지 않으며, 기존 크론 항목을 확인하거나 추가로 추가하려면 서버에 SSH로 접속해야 하므로 번거로워집니다.

Laravel의 명령어 스케줄러는 서버에서 예약 작업을 관리하는 완전히 새로운 접근 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내에서 명령어 스케줄을 유창하고 표현적으로 정의할 수 있습니다. 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 필요합니다. 여러분의 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메소드 안에 정의됩니다. 시작에 도움이 되도록 간단한 예제가 해당 메소드 내에 정의되어 있습니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

애플리케이션의 `App\Console\Kernel` 클래스 내 `schedule` 메소드에서 모든 예약 작업을 정의할 수 있습니다. 시작을 위해 예제를 살펴보겠습니다. 이 예제에서는 매일 자정에 호출될 클로저를 예약합니다. 클로저 내부에서는 데이터베이스 쿼리를 실행하여 테이블을 비웁니다:

```php
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

클로저를 사용한 스케줄링 외에도, [호출 가능한 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 예약할 수 있습니다. 호출 가능한 객체는 `__invoke` 메소드를 포함하는 단순한 PHP 클래스입니다:

```php
$schedule->call(new DeleteRecentUsers)->daily();
```

예약된 작업 개요와 다음 실행 예정 시간을 확인하고 싶다면, `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```nothing
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저뿐만 아니라 [Artisan 명령어](/docs/{{version}}/artisan) 및 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메소드를 사용해 명령어의 이름이나 클래스명을 인자로 전달하여 Artisan 명령어를 예약할 수 있습니다.

명령어 클래스명을 사용해 Artisan 명령어를 예약할 때, 명령어 실행 시 제공되어야 할 추가 커맨드 라인 인자를 배열로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업(Job) 스케줄링

`job` 메소드를 사용해 [큐 작업](/docs/{{version}}/queues)을 예약할 수 있습니다. 이 방법은 클로저를 사용해 큐 작업을 예약하는 것보다 더 간편하게 작업을 스케줄링할 수 있습니다:

```php
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

작업을 큐에 넣을 때 사용할 큐 이름과 큐 연결을 두 번째, 세 번째 인자로 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;

// "heartbeats" 큐, "sqs" 연결로 작업을 디스패치...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령어 스케줄링

`exec` 메소드를 사용해 운영체제에 명령어를 전달해 실행할 수 있습니다:

```php
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

지정된 간격으로 작업을 실행하는 몇 가지 예시를 이미 살펴보았습니다. 하지만 이외에도 다양한 스케줄 빈도를 설정할 수 있습니다:

메소드  | 설명
------------- | -------------
`->cron('* * * * *');`  |  커스텀 크론 스케줄로 작업 실행
`->everyMinute();`  |  매 분마다 작업 실행
`->everyTwoMinutes();`  |  2분마다 작업 실행
`->everyThreeMinutes();`  |  3분마다 작업 실행
`->everyFourMinutes();`  |  4분마다 작업 실행
`->everyFiveMinutes();`  |  5분마다 작업 실행
`->everyTenMinutes();`  |  10분마다 작업 실행
`->everyFifteenMinutes();`  |  15분마다 작업 실행
`->everyThirtyMinutes();`  |  30분마다 작업 실행
`->hourly();`  |  매 시간마다 작업 실행
`->hourlyAt(17);`  |  매 시간 정각 17분에 작업 실행
`->everyTwoHours();`  |  2시간마다 작업 실행
`->everyThreeHours();`  |  3시간마다 작업 실행
`->everyFourHours();`  |  4시간마다 작업 실행
`->everySixHours();`  |  6시간마다 작업 실행
`->daily();`  |  매일 자정(00:00)에 작업 실행
`->dailyAt('13:00');`  |  매일 13:00에 작업 실행
`->twiceDaily(1, 13);`  |  매일 1:00과 13:00에 작업 실행
`->weekly();`  |  매주 일요일 00:00에 작업 실행
`->weeklyOn(1, '8:00');`  |  매주 월요일 8:00에 작업 실행
`->monthly();`  |  매월 1일 00:00에 작업 실행
`->monthlyOn(4, '15:00');`  |  매월 4일 15:00에 작업 실행
`->twiceMonthly(1, 16, '13:00');`  |  매월 1일, 16일 13:00에 작업 실행
`->lastDayOfMonth('15:00');` | 매월 마지막 날 15:00에 작업 실행
`->quarterly();` |  매 분기 첫째 날 00:00에 작업 실행
`->yearly();`  |  매년 1월 1일 00:00에 작업 실행
`->yearlyOn(6, 1, '17:00');`  |  매년 6월 1일 17:00에 작업 실행
`->timezone('America/New_York');` | 작업에 사용할 타임존 지정

이러한 메소드들은 추가 제약 조건과 조합하여 더욱 세밀하게 특정 요일에만 작업이 실행되도록 만들 수 있습니다. 예를 들어, 명령어를 매주 월요일에 실행하도록 예약하고 싶다면:

```php
// 매주 월요일 13시에 1회 실행...
$schedule->call(function () {
    //
})->weekly()->mondays()->at('13:00');
```

```php
// 평일 8시부터 17시까지 한 시간마다 실행...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

추가 스케줄 제약 조건 목록은 아래와 같습니다:

메소드  | 설명
------------- | -------------
`->weekdays();`  |  평일(월~금)에만 실행
`->weekends();`  |  주말(토~일)에만 실행
`->sundays();`  |  일요일에만 실행
`->mondays();`  |  월요일에만 실행
`->tuesdays();`  |  화요일에만 실행
`->wednesdays();`  |  수요일에만 실행
`->thursdays();`  |  목요일에만 실행
`->fridays();`  |  금요일에만 실행
`->saturdays();`  |  토요일에만 실행
`->days(array|mixed);`  |  특정 요일만 실행 (숫자, 상수 등)
`->between($startTime, $endTime);`  |  시작~종료 시간 사이에만 실행
`->unlessBetween($startTime, $endTime);`  |  시작~종료 시간 사이 *외*에만 실행
`->when(Closure);`  |  참/거짓 테스트에 따라 실행
`->environments($env);`  |  특정 환경(예: production, staging)에서만 실행

<a name="day-constraints"></a>
#### 요일 제약

`days` 메소드를 사용해 작업이 실행될 요일을 지정할 수 있습니다. 예를 들어, 매주 일요일과 수요일에 한 시간마다 명령어를 예약하려면 다음과 같이 할 수 있습니다:

```php
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

또는, `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간 범위 제약

`between` 메소드는 하루 중 특정 시간대에만 작업 실행을 제한합니다:

```php
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

비슷하게, `unlessBetween` 메소드를 사용하면 특정 시간대 동안에만 작업이 *실행되지 않도록* 할 수 있습니다:

```php
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 참/거짓 테스트 제약

`when` 메소드는 주어진 클로저의 반환값이 `true`이면 작업이 실행되도록 합니다. (다른 제약 조건이 없다는 전제 하에):

```php
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메소드는 `when`의 반대 역할을 합니다. 클로저가 `true`를 반환하면 예약된 작업은 *실행되지 않습니다*:

```php
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

여러 `when` 메소드를 체이닝하면, *모든* 조건이 `true`일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약

`environments` 메소드를 사용해 [환경 변수](/docs/{{version}}/configuration#environment-configuration) `APP_ENV` 값에 따라 특정 환경에서만 작업이 실행되도록 지정할 수 있습니다:

```php
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존

`timezone` 메소드를 사용해 예약된 작업의 시간이 지정된 타임존으로 해석되도록 할 수 있습니다:

```php
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00');
```

모든 예약된 작업에 동일한 타임존을 반복적으로 지정한다면, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메소드를 정의하는 것이 좋습니다. 이 메소드는 모든 예약 작업의 기본 타임존을 반환해야 합니다:

```php
/**
 * 예약 이벤트에 기본적으로 사용할 타임존을 반환합니다.
 *
 * @return \DateTimeZone|string|null
 */
protected function scheduleTimezone()
{
    return 'America/Chicago';
}
```

> {note} 일부 타임존은 서머타임(DST)이 적용됩니다. 서머타임이 변경되는 경우 예약 작업이 두 번 실행되거나 아예 실행되지 않을 수도 있으니, 가능하다면 타임존 스케줄링 사용을 지양하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 방지

기본적으로, 예약된 작업이 이전 실행 인스턴스가 아직 실행 중이어도 중복으로 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메소드를 사용할 수 있습니다:

```php
$schedule->command('emails:send')->withoutOverlapping();
```

예제에서 `emails:send` [Artisan 명령어](/docs/{{version}}/artisan)는 이미 실행 중이 아닐 때만 매 분마다 실행됩니다. `withoutOverlapping`은 실행 시간 예측이 어려운 작업에 사용하면 특히 유용합니다.

필요하다면, 중복 방지 락이 해제될 때까지 대기 시간(분 단위)을 직접 지정할 수도 있습니다. 기본값은 24시간입니다:

```php
$schedule->command('emails:send')->withoutOverlapping(10);
```

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 작업 실행

> {note} 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `database`, `memcached`, `dynamodb`, `redis` 중 하나를 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

애플리케이션 스케줄러가 여러 서버에서 실행 중이라면, 작업이 오직 하나의 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤마다 보고서를 생성하는 예약 작업이 있고, 스케줄러가 3대의 워커 서버에서 실행 중이라면 세 서버에서 각각 작업이 실행되어 보고서가 3개가 생성되어버릴 수 있습니다.

이런 현상을 방지하려면 예약 작업에 `onOneServer` 메소드를 추가합니다. 작업을 최초로 잡은 서버가 원자적 락을 확보해 나머지 서버에서는 작업이 실행되지 않습니다:

```php
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로, 같은 시간에 예약된 여러 작업은 `schedule` 메소드에 작성된 순서대로 차례로 실행됩니다. 만약 실행 시간이 긴 작업이 있다면, 이후 작업들의 시작 시간이 예상보다 늦어질 수 있습니다. 모든 작업을 동시에, 백그라운드에서 실행하고 싶다면 `runInBackground` 메소드를 사용할 수 있습니다:

```php
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> {note} `runInBackground`는 `command` 및 `exec` 방식의 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)에 진입해 있으면 예약 작업은 실행되지 않습니다. 이는 서버 유지보수 도중 예약 작업이 수행되는 것을 방지하기 위함입니다. 다만, 유지보수 모드일 때에도 강제로 작업을 실행하려면 `evenInMaintenanceMode` 메소드를 사용할 수 있습니다:

```php
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행하기

예약 작업을 정의하는 방법을 살펴보았으니, 실제로 서버에서 작업을 실행하는 방법을 알아봅시다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하고 서버의 현재 시간에 따라 실행할지 여부를 결정합니다.

즉, Laravel 스케줄러를 사용할 때는 서버에 아래와 같이 매 분마다 `schedule:run` 명령어를 실행하는 크론 항목만 추가하면 됩니다. (서버에 크론을 추가하는 방법을 모르겠다면, [Laravel Forge](https://forge.laravel.com)와 같은 서비스 사용을 권장합니다):

```crontab
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="running-the-scheduler-locally"></a>
## 로컬에서 스케줄러 실행하기

일반적으로, 로컬 개발 머신에서는 크론 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 전경(foreground)에서 실행되며, 명령어를 중지시키기 전까지 매 분마다 스케줄러를 실행합니다:

```bash
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약 작업이 출력하는 결과물을 다루기 위한 여러 편리한 메소드를 제공합니다. 먼저, `sendOutputTo` 메소드를 사용하여 작업 출력을 파일로 남길 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

출력을 지정한 파일에 추가(append)하고 싶다면, `appendOutputTo` 메소드를 사용하세요:

```php
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

`emailOutputTo` 메소드를 사용하면, 작업 출력을 원하는 이메일 주소로 전송할 수 있습니다. (이 기능을 사용하기 전에는 Laravel의 [이메일 서비스](/docs/{{version}}/mail) 설정이 필요합니다.)

```php
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

예약된 Artisan 명령어나 시스템 명령어가 0이 아닌 종료 코드로 종료됐을 때만 출력을 이메일로 받고 싶다면 `emailOutputOnFailure`를 사용하면 됩니다:

```php
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> {note} `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo`는 `command`, `exec` 메소드에만 적용됩니다.

<a name="task-hooks"></a>
## 작업 훅(Hook)

`before`, `after` 메소드를 이용해 예약된 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // 작업 실행 직전...
         })
         ->after(function () {
             // 작업 실행 직후...
         });
```

`onSuccess`, `onFailure` 메소드는 예약 작업이 성공하거나 실패했을 때 실행할 코드를 지정합니다. 실패란, Artisan 명령어나 시스템 명령어가 0이 아닌 종료 코드로 종료됐음을 의미합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function () {
             // 작업 성공...
         })
         ->onFailure(function () {
             // 작업 실패...
         });
```

명령어의 출력 결과가 있다면, `after`, `onSuccess`, `onFailure` 훅의 클로저에 `Illuminate\Support\Stringable` 타입힌트로 `$output` 인자를 선언하여 출력값에 접근할 수 있습니다:

```php
use Illuminate\Support\Stringable;

$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function (Stringable $output) {
             // 작업 성공...
         })
         ->onFailure(function (Stringable $output) {
             // 작업 실패...
         });
```

<a name="pinging-urls"></a>
#### URL 핑(Ping) 전송

`pingBefore`, `thenPing` 메소드를 사용하면 작업 실행 전 또는 후에 지정한 URL로 자동으로 핑을 전송할 수 있습니다. 이 방법은 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 작업 실행 시작/종료를 알릴 때 유용합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

`pingBeforeIf`, `thenPingIf` 메소드는 특정 조건이 `true`일 때만 핑을 전송합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

`pingOnSuccess`, `pingOnFailure` 메소드는 작업 성공/실패 시 각각 지정한 URL로 핑을 전송합니다. 실패는 Artisan 명령어나 시스템 명령어가 0이 아닌 종료 코드로 종료됐을 때를 의미합니다:

```php
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

모든 핑 관련 메소드는 Guzzle HTTP 라이브러리가 필요합니다. Guzzle은 기본적으로 모든 새로운 Laravel 프로젝트에 설치되어 있지만, 만약 없다면 Composer로 직접 설치할 수 있습니다:

```
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## 이벤트

필요하다면, 스케줄러가 발생시키는 [이벤트](/docs/{{version}}/events)를 수신(listen)할 수 있습니다. 보통 이벤트 리스너 맵핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스 내에 정의합니다:

```php
/**
 * 애플리케이션의 이벤트 리스너 맵핑입니다.
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
