# 작업 스케줄링(Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 방지](#preventing-task-overlaps)
    - [한 서버에서만 작업 실행하기](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [점검(유지보수) 모드](#maintenance-mode)
- [스케줄러 실행하기](#running-the-scheduler)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅(Hooks)](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

이전에는 각 작업마다 서버에 크론(cron) 설정을 개별적으로 추가했을 것입니다. 하지만 이런 방식은 작업 스케줄이 소스 코드로 관리되지 않고, 기존의 크론 엔트리를 확인하거나 추가하려면 서버에 SSH로 접속해야 하므로 불편함이 발생합니다.

Laravel의 명령어 스케줄러는 서버 내 예약된(스케줄) 작업을 관리하는 새로운 접근 방식을 제공합니다. 스케줄러를 사용하면 예약 작업을 여러분의 Laravel 애플리케이션 내에서 유연하고 표현적으로 정의할 수 있습니다. 별도의 크론 엔트리 없이도, 서버에는 단 한 줄의 크론만 추가하면 됩니다. 실제 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메서드 내에서 정의합니다. 시작을 쉽게 할 수 있도록 간단한 예제가 기본으로 들어 있습니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기

여러분의 모든 스케줄 작업은 애플리케이션의 `App\Console\Kernel` 클래스의 `schedule` 메서드 내에서 정의할 수 있습니다. 우선 간단한 예제를 살펴보겠습니다. 아래 예시에서는 클로저를 매일 자정에 실행하여 데이터베이스에서 테이블을 삭제하는 작업을 예약합니다:

    <?php

    namespace App\Console;

    use Illuminate\Console\Scheduling\Schedule;
    use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
    use Illuminate\Support\Facades\DB;

    class Kernel extends ConsoleKernel
    {
        /**
         * 애플리케이션 명령어 스케줄 정의.
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

클로저 방식 외에도 [호출 가능한 객체(Invokable Object)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄로 사용할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다:

    $schedule->call(new DeleteRecentUsers)->daily();

예약된 작업 목록과 다음 실행 시간을 확인하려면 `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저 외에도 [Artisan 명령어](/docs/{{version}}/artisan) 또는 시스템 명령어를 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 명령어 이름이나 클래스명으로 Artisan 명령을 예약할 수 있습니다.

명령어 클래스로 예약할 경우, 인자로 명령 라인 인자 배열도 전달할 수 있습니다:

    use App\Console\Commands\SendEmailsCommand;

    $schedule->command('emails:send Taylor --force')->daily();

    $schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드를 사용해 [큐 작업](/docs/{{version}}/queues)을 예약할 수 있습니다. `call`로 클로저를 작성하지 않고도 간편하게 큐 작업을 예약할 수 있습니다:

    use App\Jobs\Heartbeat;

    $schedule->job(new Heartbeat)->everyFiveMinutes();

필요하다면 두 번째, 세 번째 인자로 큐 이름과 연결 이름도 지정할 수 있습니다:

    use App\Jobs\Heartbeat;

    // "sqs" 연결의 "heartbeats" 큐로 작업 디스패치
    $schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();

<a name="scheduling-shell-commands"></a>
### 셸 명령어 스케줄링

`exec` 메서드를 사용하면 운영 체제 명령을 실행할 수 있습니다:

    $schedule->exec('node /home/forge/script.js')->daily();

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

작업을 특정 간격마다 실행할 수 있는 다양한 메서드가 있습니다. 아래는 사용 가능한 주기 예시입니다:

메서드  | 설명
------------- | -------------
`->cron('* * * * *');`  |  커스텀 크론 일정에 작업 실행
`->everyMinute();`  |  매분마다 작업 실행
`->everyTwoMinutes();`  |  2분마다 작업 실행
`->everyThreeMinutes();`  |  3분마다 작업 실행
`->everyFourMinutes();`  |  4분마다 작업 실행
`->everyFiveMinutes();`  |  5분마다 작업 실행
`->everyTenMinutes();`  |  10분마다 작업 실행
`->everyFifteenMinutes();`  |  15분마다 작업 실행
`->everyThirtyMinutes();`  |  30분마다 작업 실행
`->hourly();`  |  매시간마다 작업 실행
`->hourlyAt(17);`  |  매시간 17분에 작업 실행
`->everyOddHour();`  |  홀수 시간마다 작업 실행
`->everyTwoHours();`  |  2시간마다 작업 실행
`->everyThreeHours();`  |  3시간마다 작업 실행
`->everyFourHours();`  |  4시간마다 작업 실행
`->everySixHours();`  |  6시간마다 작업 실행
`->daily();`  |  매일 자정에 작업 실행
`->dailyAt('13:00');`  |  매일 13:00에 작업 실행
`->twiceDaily(1, 13);`  |  매일 1:00, 13:00에 작업 실행
`->twiceDailyAt(1, 13, 15);`  |  매일 1:15, 13:15에 작업 실행
`->weekly();`  |  매주 일요일 00:00에 작업 실행
`->weeklyOn(1, '8:00');`  |  매주 월요일 8:00에 작업 실행
`->monthly();`  |  매월 1일 00:00에 작업 실행
`->monthlyOn(4, '15:00');`  |  매월 4일 15:00에 작업 실행
`->twiceMonthly(1, 16, '13:00');`  |  매월 1일, 16일 13:00에 작업 실행
`->lastDayOfMonth('15:00');` | 매월 마지막 날 15:00에 작업 실행
`->quarterly();` |  분기 첫날 00:00에 작업 실행
`->quarterlyOn(4, '14:00');` |  분기마다 4일 14:00에 작업 실행
`->yearly();`  |  매년 1월 1일 00:00에 작업 실행
`->yearlyOn(6, 1, '17:00');`  |  매년 6월 1일 17:00에 작업 실행
`->timezone('America/New_York');` | 작업의 타임존 지정

추가 제약 조건과 함께 조합하여 더욱 세밀하게 작업을 제어할 수 있습니다. 예를 들어, 매주 월요일에만 실행되는 명령을 만들 수도 있습니다:

    // 월요일 13:00에 1회 실행...
    $schedule->call(function () {
        //
    })->weekly()->mondays()->at('13:00');

    // 평일 8시~17시까지 매시간 실행...
    $schedule->command('foo')
              ->weekdays()
              ->hourly()
              ->timezone('America/Chicago')
              ->between('8:00', '17:00');

추가 가능한 제약조건:

메서드  | 설명
------------- | -------------
`->weekdays();`  |  평일(월~금)에만 실행 제한
`->weekends();`  |  주말(토, 일)에만 실행 제한
`->sundays();`  |  일요일에만 실행 제한
`->mondays();`  |  월요일에만 실행 제한
`->tuesdays();`  |  화요일에만 실행 제한
`->wednesdays();`  |  수요일에만 실행 제한
`->thursdays();`  |  목요일에만 실행 제한
`->fridays();`  |  금요일에만 실행 제한
`->saturdays();`  |  토요일에만 실행 제한
`->days(array\|mixed);`  |  특정 요일에만 실행 제한
`->between($startTime, $endTime);`  |  지정 시간 사이에만 실행
`->unlessBetween($startTime, $endTime);`  |  지정 시간대 외에만 실행
`->when(Closure);`  |  참 거짓 테스트 기반 실행 제어
`->environments($env);`  |  특정 환경에서만 실행

<a name="day-constraints"></a>
#### 요일 제약조건

`days` 메서드를 사용해 특정 요일에만 작업을 실행할 수 있습니다. 예를 들어, 일요일과 수요일에 매시간 명령을 실행할 수 있습니다:

    $schedule->command('emails:send')
                    ->hourly()
                    ->days([0, 3]);

또는, `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수 있습니다:

    use Illuminate\Console\Scheduling\Schedule;

    $schedule->command('emails:send')
                    ->hourly()
                    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);

<a name="between-time-constraints"></a>
#### 시간대 제약조건

`between` 메서드를 사용해 특정 시간대에만 작업을 실행할 수 있습니다:

    $schedule->command('emails:send')
                        ->hourly()
                        ->between('7:00', '22:00');

반대로, `unlessBetween`를 사용하면 지정 시간대에는 실행하지 않도록 할 수 있습니다:

    $schedule->command('emails:send')
                        ->hourly()
                        ->unlessBetween('23:00', '4:00');

<a name="truth-test-constraints"></a>
#### 참/거짓 테스트 제약조건

`when` 메서드는 클로저의 반환값이 `true`일 경우에만 작업을 실행합니다. 다른 제약조건이 없을 때만 실행됩니다:

    $schedule->command('emails:send')->daily()->when(function () {
        return true;
    });

반대로, `skip` 메서드는 클로저가 `true`를 반환하면 작업이 실행되지 않습니다:

    $schedule->command('emails:send')->daily()->skip(function () {
        return true;
    });

여러 개의 `when`이 연결 체인으로 사용될 경우, 모든 조건이 `true`일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약조건

`environments` 메서드를 사용해 지정한 환경(`APP_ENV` [환경 변수](/docs/{{version}}/configuration#environment-configuration))에서만 작업을 실행할 수 있습니다:

    $schedule->command('emails:send')
                ->daily()
                ->environments(['staging', 'production']);

<a name="timezones"></a>
### 타임존

`timezone` 메서드를 사용하여 예약된 작업의 시간이 지정된 타임존에 따라 해석되도록 할 수 있습니다:

    $schedule->command('report:generate')
             ->timezone('America/New_York')
             ->at('2:00')

모든 예약 작업에 같은 타임존을 반복해서 할당해야 한다면, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메서드를 정의할 수 있습니다. 이 메서드는 모든 예약 작업에 기본 할당할 타임존을 반환해야 합니다:

    /**
     * 예약 이벤트에 기본 적용될 타임존 반환.
     *
     * @return \DateTimeZone|string|null
     */
    protected function scheduleTimezone()
    {
        return 'America/Chicago';
    }

> **경고**
> 일부 타임존은 서머타임을 사용합니다. 서머타임 변화 시, 예약 작업이 두 번 실행되거나 실행되지 않을 수 있습니다. 그러므로 되도록 타임존 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 방지

기본적으로, 이전 작업의 인스턴스가 아직 실행 중이더라도 예약 작업은 계속 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

    $schedule->command('emails:send')->withoutOverlapping();

이 예시에서는 `emails:send` [Artisan 명령어](/docs/{{version}}/artisan)가 이미 실행 중이 아니라면 매분 실행됩니다. 이 메서드는 실행 시간이 크게 변동될 수 있는 작업에서 유용합니다.

필요하다면, 겹침 방지 락이 만료될 시간을 분 단위로 지정할 수 있습니다. 기본값은 24시간입니다:

    $schedule->command('emails:send')->withoutOverlapping(10);

내부적으로 `withoutOverlapping`은 애플리케이션의 [캐시](/docs/{{version}}/cache)를 이용해 락을 획득합니다. 작업이 서버 문제로 멈춘 경우, `schedule:clear-cache` Artisan 명령어로 캐시 락을 해제할 수 있습니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서만 작업 실행하기

> **경고**
> 이 기능을 사용하려면 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, `redis` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버를 이용해야 합니다.

여러 서버에서 스케줄러가 동작 중이라면, 특정 작업을 한 대의 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일마다 리포트를 생성하는 작업이 3대의 서버에서 동시에 실행될 가능성이 있습니다. 이는 바람직하지 않습니다!

이럴 때 `onOneServer` 메서드를 사용하면, 해당 작업을 최초로 획득한 서버가 다른 서버와의 중복 실행을 방지하는 원자적 락을 확보하게 됩니다:

    $schedule->command('report:generate')
                    ->fridays()
                    ->at('17:00')
                    ->onOneServer();

<a name="naming-unique-jobs"></a>
#### 단일 서버 잡 이름 지정

같은 작업을 여러 파라미터로 여러 번 예약하되, 각 조합을 한 서버에서만 실행하게 하려면 `name` 메서드로 작업마다 고유 이름을 부여해야 합니다:

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

마찬가지로, 클로저를 예약할 때도 한 서버에서만 실행하려면 이름을 반드시 지정해야 합니다:

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로, 같은 시각에 예약된 여러 작업은 `schedule` 메서드 내 정의 순서대로 순차적으로 실행됩니다. 장시간 소요되는 예약 작업이 있다면, 이후 작업의 실행이 지연될 수 있습니다. 여러 작업을 동시에 실행하고 싶다면 `runInBackground` 메서드를 사용하세요:

    $schedule->command('analytics:report')
             ->daily()
             ->runInBackground();

> **경고**
> `runInBackground` 메서드는 `command` 및 `exec` 메서드로 예약된 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 점검(유지보수) 모드

애플리케이션이 [점검 모드](/docs/{{version}}/configuration#maintenance-mode)에 있을 때 예약 작업은 실행되지 않습니다. 이는 서버 점검 중에 작업이 실행되어 영향을 주지 않게 하기 위함입니다. 하지만, 점검 모드에서도 강제로 작업을 실행하고 싶다면, `evenInMaintenanceMode` 메서드를 사용할 수 있습니다:

    $schedule->command('emails:send')->evenInMaintenanceMode();

<a name="running-the-scheduler"></a>
## 스케줄러 실행하기

이제 작업 예약을 어떻게 정의하는지 배웠으니, 실제로 서버에서 어떻게 예약을 실행하는지 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가, 현재 서버 시간에 따라 실행 여부를 판단합니다.

따라서 Laravel 스케줄러를 사용할 때는, 1분마다 `schedule:run` 명령어가 실행되는 단일 크론만 서버에 추가하면 됩니다. 크론 등록 방법을 모르면 [Laravel Forge](https://forge.laravel.com)와 같은 서비스를 활용할 수도 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="running-the-scheduler-locally"></a>
## 로컬에서 스케줄러 실행하기

일반적으로 로컬 개발 환경에는 크론을 추가하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용하면 됩니다. 이 명령은 포그라운드에서 동작하며, 수동으로 종료할 때까지 1분마다 스케줄러를 실행합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약된 작업의 출력물을 다루는 여러 편리한 메서드를 제공합니다. `sendOutputTo` 메서드는 작업 출력을 지정된 파일로 저장합니다:

    $schedule->command('emails:send')
             ->daily()
             ->sendOutputTo($filePath);

출력을 파일에 덧붙이려면 `appendOutputTo` 메서드를 사용할 수 있습니다:

    $schedule->command('emails:send')
             ->daily()
             ->appendOutputTo($filePath);

`emailOutputTo` 메서드를 사용하면 원하는 이메일 주소로 작업 출력을 전송할 수 있습니다. 사용 전에는 Laravel의 [메일 서비스](/docs/{{version}}/mail) 설정이 필요합니다:

    $schedule->command('report:generate')
             ->daily()
             ->sendOutputTo($filePath)
             ->emailOutputTo('taylor@example.com');

Artisan 또는 시스템 명령어가 0이 아닌 값(오류)으로 종료되었을 때만 이메일을 전송하려면, `emailOutputOnFailure`를 사용하세요:

    $schedule->command('report:generate')
             ->daily()
             ->emailOutputOnFailure('taylor@example.com');

> **경고**
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`, `exec` 메서드를 통해 예약된 작업에만 적용됩니다.

<a name="task-hooks"></a>
## 작업 훅(Hooks)

`before`, `after` 메서드를 통해 예약 작업 실행 전후에 실행할 코드를 지정할 수 있습니다:

    $schedule->command('emails:send')
             ->daily()
             ->before(function () {
                 // 작업 실행 전...
             })
             ->after(function () {
                 // 작업 실행 후...
             });

`onSuccess`, `onFailure` 메서드를 사용하면 작업이 성공 또는 실패(0이 아닌 코드로 종료)할 때의 코드를 지정할 수 있습니다:

    $schedule->command('emails:send')
             ->daily()
             ->onSuccess(function () {
                 // 작업 성공...
             })
             ->onFailure(function () {
                 // 작업 실패...
             });

명령의 출력이 필요한 경우, 훅의 클로저에 `Illuminate\Support\Stringable` 타입힌트를 지정하면 출력값에 접근할 수 있습니다:

    use Illuminate\Support\Stringable;

    $schedule->command('emails:send')
             ->daily()
             ->onSuccess(function (Stringable $output) {
                 // 작업 성공...
             })
             ->onFailure(function (Stringable $output) {
                 // 작업 실패...
             });

<a name="pinging-urls"></a>
#### URL 핑(Ping) 보내기

`pingBefore`, `thenPing` 메서드로, 작업 실행 전/후에 지정된 URL을 자동으로 핑할 수 있습니다. 이는 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 작업 상태를 알릴 때 유용합니다:

    $schedule->command('emails:send')
             ->daily()
             ->pingBefore($url)
             ->thenPing($url);

`pingBeforeIf`, `thenPingIf` 메서드를 사용하면 특정 조건이 참일 때만 URL에 핑을 보냅니다:

    $schedule->command('emails:send')
             ->daily()
             ->pingBeforeIf($condition, $url)
             ->thenPingIf($condition, $url);

`pingOnSuccess`, `pingOnFailure`는 작업이 성공하거나 실패했을 때만 URL을 핑합니다(실패는 종료 코드가 0이 아닌 경우를 의미):

    $schedule->command('emails:send')
             ->daily()
             ->pingOnSuccess($successUrl)
             ->pingOnFailure($failureUrl);

모든 핑 메서드는 Guzzle HTTP 라이브러리가 필요합니다. Laravel의 신규 프로젝트에는 기본 설치되어 있지만, 없다면 Composer로 직접 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## 이벤트

필요하다면, 스케줄러가 발생시키는 [이벤트](/docs/{{version}}/events)를 청취할 수 있습니다. 일반적으로 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 매핑됩니다:

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