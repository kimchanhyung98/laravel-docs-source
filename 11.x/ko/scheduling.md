# 작업 스케줄링

- [소개](#introduction)
- [스케줄 정의](#defining-schedules)
    - [아티즌(Artisan) 명령 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령 스케줄링](#scheduling-shell-commands)
    - [스케줄 주기 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 방지](#preventing-task-overlaps)
    - [단일 서버에서 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행](#running-the-scheduler)
    - [1분 미만 주기의 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

과거에는 서버에서 스케줄링해야 하는 작업마다 별도의 크론(cron) 설정 항목을 직접 작성해야 했을 것입니다. 이 방식은 스케줄이 더 이상 소스 관리에 포함되지 않고, 현재 존재하는 크론 항목을 확인하거나 추가로 항목을 넣기 위해 SSH로 서버에 직접 접속해야 하므로 매우 번거로울 수 있습니다.

Laravel의 명령 스케줄러는 서버에서 예약 작업을 효과적으로 관리할 수 있는 새로운 방식을 제공합니다. 이 스케줄러를 이용하면 명령 스케줄을 Laravel 애플리케이션 자체 내에서 간결하고 명확하게 정의할 수 있습니다. 스케줄러를 사용할 경우, 서버에는 단 하나의 크론 항목만 필요합니다. 작업 스케줄은 일반적으로 애플리케이션의 `routes/console.php` 파일에서 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 먼저 예시를 살펴보겠습니다. 다음 예제에서는 매일 자정에 클로저를 실행하도록 예약하고, 이 클로저 내에서 데이터베이스 쿼리를 통해 특정 테이블을 비워줍니다:

    <?php

    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Facades\Schedule;

    Schedule::call(function () {
        DB::table('recent_users')->delete();
    })->daily();

클로저를 이용한 예약 외에도, [호출 가능한 객체(invokable object)](https://secure.php.net/manual/kr/language.oop5.magic.php#object.invoke)를 예약할 수도 있습니다. 호출 가능한 객체란 `__invoke` 메서드를 포함한 간단한 PHP 클래스를 의미합니다:

    Schedule::call(new DeleteRecentUsers)->daily();

만약 `routes/console.php` 파일을 명령 정의만을 위해 남기고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 활용하여 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 인자로 받는 클로저를 인수로 전달받습니다:

    use Illuminate\Console\Scheduling\Schedule;

    ->withSchedule(function (Schedule $schedule) {
        $schedule->call(new DeleteRecentUsers)->daily();
    })

예약된 작업 목록과 다음 실행 예정 시간을 확인하고 싶다면, `schedule:list` 아티즌 명령을 사용할 수 있습니다:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### 아티즌(Artisan) 명령 스케줄링

클로저 예약과 더불어 [아티즌 명령](/docs/{{version}}/artisan)과 시스템 명령도 예약할 수 있습니다. 예를 들어, `command` 메서드를 이용하여 명령의 이름이나 클래스 이름으로 아티즌 명령을 예약할 수 있습니다.

명령의 클래스명을 이용해 예약할 경우, 명령 실행시 필요한 추가 명령행 인자를 배열로 전달할 수 있습니다:

    use App\Console\Commands\SendEmailsCommand;
    use Illuminate\Support\Facades\Schedule;

    Schedule::command('emails:send Taylor --force')->daily();

    Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();

<a name="scheduling-artisan-closure-commands"></a>
#### 클로저로 정의된 아티즌 명령 예약

클로저로 정의한 아티즌 명령을 예약하려면, 명령 정의 뒤에 예약 관련 메서드를 체이닝하면 됩니다:

    Artisan::command('delete:recent-users', function () {
        DB::table('recent_users')->delete();
    })->purpose('최근 사용자 삭제')->daily();

클로저 명령에 인자를 전달하고 싶다면 `schedule` 메서드에 인자를 넘기면 됩니다:

    Artisan::command('emails:send {user} {--force}', function ($user) {
        // ...
    })->purpose('지정한 사용자에게 이메일 발송')->schedule(['Taylor', '--force'])->daily();

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드는 [큐 작업](/docs/{{version}}/queues)을 예약할 때 사용할 수 있습니다. 이 메서드를 사용하면 클로저 없이 직접 큐 작업을 예약할 수 있습니다:

    use App\Jobs\Heartbeat;
    use Illuminate\Support\Facades\Schedule;

    Schedule::job(new Heartbeat)->everyFiveMinutes();

옵션으로 두 번째와 세 번째 인자로, 큐 이름과 큐 연결명을 지정할 수 있습니다:

    use App\Jobs\Heartbeat;
    use Illuminate\Support\Facades\Schedule;

    // "heartbeats" 큐에서 "sqs" 연결로 작업 전송...
    Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();

<a name="scheduling-shell-commands"></a>
### 셸 명령 스케줄링

`exec` 메서드를 사용하면 운영체제 명령을 실행할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::exec('node /home/forge/script.js')->daily();

<a name="schedule-frequency-options"></a>
### 스케줄 주기 옵션

특정 간격으로 작업을 실행하도록 설정하는 예시를 이미 살펴봤습니다. 하지만, 작업에 지정할 수 있는 다양한 주기 옵션이 더 존재합니다:

<div class="overflow-auto">

| 메서드                            | 설명                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| `->cron('* * * * *');`             | 사용자 정의 크론 스케줄로 작업 실행                               |
| `->everySecond();`                 | 매초 작업 실행                                               |
| `->everyTwoSeconds();`             | 2초마다 작업 실행                                            |
| `->everyFiveSeconds();`            | 5초마다 작업 실행                                            |
| `->everyTenSeconds();`             | 10초마다 작업 실행                                           |
| `->everyFifteenSeconds();`         | 15초마다 작업 실행                                           |
| `->everyTwentySeconds();`          | 20초마다 작업 실행                                           |
| `->everyThirtySeconds();`          | 30초마다 작업 실행                                           |
| `->everyMinute();`                 | 매분 작업 실행                                               |
| `->everyTwoMinutes();`             | 2분마다 작업 실행                                            |
| `->everyThreeMinutes();`           | 3분마다 작업 실행                                            |
| `->everyFourMinutes();`            | 4분마다 작업 실행                                            |
| `->everyFiveMinutes();`            | 5분마다 작업 실행                                            |
| `->everyTenMinutes();`             | 10분마다 작업 실행                                           |
| `->everyFifteenMinutes();`         | 15분마다 작업 실행                                           |
| `->everyThirtyMinutes();`          | 30분마다 작업 실행                                           |
| `->hourly();`                      | 매시간 작업 실행                                             |
| `->hourlyAt(17);`                  | 매시간 17분에 작업 실행                                      |
| `->everyOddHour($minutes = 0);`    | 홀수 시간마다 작업 실행                                      |
| `->everyTwoHours($minutes = 0);`   | 2시간마다 작업 실행                                          |
| `->everyThreeHours($minutes = 0);` | 3시간마다 작업 실행                                          |
| `->everyFourHours($minutes = 0);`  | 4시간마다 작업 실행                                          |
| `->everySixHours($minutes = 0);`   | 6시간마다 작업 실행                                          |
| `->daily();`                       | 매일 자정에 작업 실행                                        |
| `->dailyAt('13:00');`              | 매일 13:00에 작업 실행                                       |
| `->twiceDaily(1, 13);`             | 매일 1:00 및 13:00에 작업 실행                               |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1:15 및 13:15에 작업 실행                               |
| `->weekly();`                      | 매주 일요일 00:00에 작업 실행                                 |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8:00에 작업 실행                                 |
| `->monthly();`                     | 매월 1일 00:00에 작업 실행                                   |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15:00에 작업 실행                                   |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일과 16일 13:00에 작업 실행                            |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15:00에 작업 실행                             |
| `->quarterly();`                   | 분기 첫날 00:00에 작업 실행                                  |
| `->quarterlyOn(4, '14:00');`       | 매 분기 4일 14:00에 작업 실행                                |
| `->yearly();`                      | 매년 1월 1일 00:00에 작업 실행                               |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17:00에 작업 실행                               |
| `->timezone('America/New_York');`  | 작업의 타임존 설정                                           |

</div>

이 메서드들은 추가 제약 조건과 결합해 특정 요일에만 작업이 실행되도록 더 정밀한 스케줄도 구성할 수 있습니다. 예를 들어, 매주 월요일에 명령을 실행하도록 예약할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    // 매주 월요일 13시에 한 번 실행...
    Schedule::call(function () {
        // ...
    })->weekly()->mondays()->at('13:00');

    // 평일 8시~17시 사이 매시간 실행...
    Schedule::command('foo')
        ->weekdays()
        ->hourly()
        ->timezone('America/Chicago')
        ->between('8:00', '17:00');

아래는 추가 스케줄 제약 조건의 목록입니다:

<div class="overflow-auto">

| 메서드                                 | 설명                                                |
| ------------------------------------- | ---------------------------------------------------- |
| `->weekdays();`                       | 평일에만 작업 제한                                   |
| `->weekends();`                       | 주말에만 작업 제한                                   |
| `->sundays();`                        | 일요일에만 작업 제한                                 |
| `->mondays();`                        | 월요일에만 작업 제한                                 |
| `->tuesdays();`                       | 화요일에만 작업 제한                                 |
| `->wednesdays();`                     | 수요일에만 작업 제한                                 |
| `->thursdays();`                      | 목요일에만 작업 제한                                 |
| `->fridays();`                        | 금요일에만 작업 제한                                 |
| `->saturdays();`                      | 토요일에만 작업 제한                                 |
| `->days(array\|mixed);`               | 특정 요일에만 작업 제한                              |
| `->between($startTime, $endTime);`    | 특정 시간 구간에만 작업 실행                         |
| `->unlessBetween($startTime, $endTime);` | 특정 시간 구간 외에만 작업 실행                  |
| `->when(Closure);`                    | 참/거짓 테스트 결과에 따라 작업 실행                 |
| `->environments($env);`               | 지정된 환경에서만 작업 실행                          |

</div>

<a name="day-constraints"></a>
#### 요일 제약

`days` 메서드를 사용하면 작업을 특정 요일에만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 일요일과 수요일마다 명령을 한 시간마다 실행하도록 예약할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('emails:send')
        ->hourly()
        ->days([0, 3]);

또는, `Illuminate\Console\Scheduling\Schedule` 클래스에 정의된 상수를 사용할 수도 있습니다:

    use Illuminate\Support\Facades;
    use Illuminate\Console\Scheduling\Schedule;

    Facades\Schedule::command('emails:send')
        ->hourly()
        ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);

<a name="between-time-constraints"></a>
#### 시간대 제약

`between` 메서드는 작업을 특정 시간대에만 실행하도록 제한합니다:

    Schedule::command('emails:send')
        ->hourly()
        ->between('7:00', '22:00');

이와 비슷하게, `unlessBetween` 메서드를 사용하면 작업 실행 제외 시간을 지정할 수 있습니다:

    Schedule::command('emails:send')
        ->hourly()
        ->unlessBetween('23:00', '4:00');

<a name="truth-test-constraints"></a>
#### 참/거짓 테스트 제약

`when` 메서드는 해당 클로저의 반환값이 `true`일 때(다른 제약 조건이 없다면)만 작업을 실행하게 제한합니다:

    Schedule::command('emails:send')->daily()->when(function () {
        return true;
    });

`skip` 메서드는 `when`의 반대로, 클로저가 `true`를 반환하면 작업이 실행되지 않습니다:

    Schedule::command('emails:send')->daily()->skip(function () {
        return true;
    });

`when` 메서드를 체이닝할 경우, 모든 조건이 `true`를 반환해야 명령이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약

`environments` 메서드를 사용하면 지정한 환경(`APP_ENV` [환경 변수](/docs/{{version}}/configuration#environment-configuration))에서만 작업이 실행되도록 할 수 있습니다:

    Schedule::command('emails:send')
        ->daily()
        ->environments(['staging', 'production']);

<a name="timezones"></a>
### 타임존

`timezone` 메서드를 통해 예약 작업의 시간이 특정 타임존 기준으로 해석되도록 설정할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('report:generate')
        ->timezone('America/New_York')
        ->at('2:00')

만약 모든 예약 작업에 동일한 타임존을 반복해서 할당한다면, 애플리케이션의 `app` 설정 파일 내에 `schedule_timezone` 옵션을 지정해 전체 작업의 기본 타임존을 지정할 수 있습니다:

    'timezone' => 'UTC',

    'schedule_timezone' => 'America/Chicago',

> [!WARNING]  
> 일부 타임존은 일광절약시간제(서머타임)를 사용합니다. 이 기간에는 예약 작업이 두 번 실행되거나 아예 실행되지 않을 수 있습니다. 가능한 한 타임존 예약을 피할 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 방지

기본적으로 예약 작업은 이전 작업 인스턴스가 아직 실행 중이어도 계속 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('emails:send')->withoutOverlapping();

이 예제에서 `emails:send` [아티즌 명령](/docs/{{version}}/artisan)는 현재 실행 중이 아니면 매분 실행됩니다. `withoutOverlapping`은 실행 시간이 매번 크게 달라 예측이 힘든 작업에서 특히 유용합니다.

필요하다면, "중복 방지" 락이 해제되기까지 대기할 최대 시간을 분 단위로 지정할 수 있습니다. 기본값은 24시간입니다:

    Schedule::command('emails:send')->withoutOverlapping(10);

내부적으로 `withoutOverlapping`는 애플리케이션의 [캐시](/docs/{{version}}/cache)를 이용해 락을 관리합니다. 필요하다면 `schedule:clear-cache` 아티즌 명령으로 이러한 캐시 락을 해제할 수 있습니다. 서버 문제로 인해 작업이 멈출 때만 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 작업 실행

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis`여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

여러 서버에서 스케줄러가 실행 중인 경우에도, 작업을 한 대의 서버에서만 실행하고 싶다면 다음과 같이 할 수 있습니다. 예를 들어, 매주 금요일 밤에 보고서를 생성하는 예약 작업이 있을 때, 스케줄러가 세 대의 서버에서 돌아가면 작업이 3회 중복 실행됩니다.

이런 경우 예약 작업 정의 시 `onOneServer` 메서드를 사용하면, 가장 먼저 락을 확보하는 서버만 해당 작업을 실행하고 나머지 서버는 실행하지 않습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('report:generate')
        ->fridays()
        ->at('17:00')
        ->onOneServer();

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업의 이름 지정

동일한 작업을 다른 파라미터로 여러 번 스케줄링하되 각각을 "한 서버에서만" 실행하고 싶을 때는 각 스케줄 정의에 고유한 이름을 `name` 메서드로 부여하세요:

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

마찬가지로, 단일 서버에서 실행해야 하는 클로저 작업도 반드시 `name`을 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로 같은 시간에 예약된 작업은 `schedule` 메서드에 정의된 순서대로 순차 실행됩니다. 장시간 실행되는 작업이 있다면 이후 작업이 지연될 수 있습니다. 모든 작업을 동시에 백그라운드에서 실행시키고 싶다면, `runInBackground` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('analytics:report')
        ->daily()
        ->runInBackground();

> [!WARNING]  
> `runInBackground`는 `command`와 `exec` 메서드를 통해 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

[유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)에서는 예약 작업이 실행되지 않습니다. 이는 서버 작업 중에 예약 작업이 방해되지 않도록 하기 위함입니다. 하지만 유지보수 모드에서도 특정 작업을 실행하고 싶다면, 예약 시 `evenInMaintenanceMode` 메서드를 호출하세요:

    Schedule::command('emails:send')->evenInMaintenanceMode();

<a name="schedule-groups"></a>
### 스케줄 그룹

비슷한 설정이 필요한 예약 작업을 여러 개 정의할 때, Laravel의 작업 그룹 기능을 이용하면 각 작업마다 같은 설정을 반복하지 않아도 됩니다. 작업 그룹을 사용하면 코드가 간결해지고, 관련 작업에 동일한 구성을 적용할 수 있습니다.

스케줄 작업 그룹을 생성하려면, 원하는 구성 메서드를 호출한 뒤 `group` 메서드를 사용하세요. `group`에는 해당 설정을 공유하는 작업을 정의하는 클로저를 전달하면 됩니다:

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
## 스케줄러 실행

이제 예약 작업을 어떻게 정의하는지 알았으니, 서버에서 이를 실제로 실행하는 방법을 살펴보겠습니다. `schedule:run` 아티즌 명령은 모든 예약 작업을 평가하여, 서버의 현재 시간 기준으로 실행 여부를 판단합니다.

즉, Laravel 스케줄러를 사용할 때는, 서버의 크론에 1분마다 실행되는 아래 한 줄만 추가하면 됩니다. 서버에 어떻게 크론을 추가하는지 모른다면, [Laravel Forge](https://forge.laravel.com)와 같은 서비스를 이용해 크론 관리를 할 수도 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 주기의 작업

대부분 운영체제에서 크론은 최대 1분마다 한 번만 실행할 수 있습니다. 하지만, Laravel 스케줄러는 초 단위 등, 더 짧은 간격으로 작업을 예약할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::call(function () {
        DB::table('recent_users')->delete();
    })->everySecond();

1분 미만 간격 작업이 정의되어 있으면, `schedule:run` 명령은 다음 분이 끝날 때까지 실행되며, 그 사이 필요한 모든 하위 주기의 작업을 실행합니다.

실행 시간이 오래 걸리는 1분 미만 간격 작업으로 인해 이후 작업이 지연될 수 있기 때문에, 모든 1분 미만 작업은 가급적 큐 작업이나 백그라운드 명령을 통해 실제 처리를 하길 권장합니다:

    use App\Jobs\DeleteRecentUsers;

    Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

    Schedule::command('users:delete')->everyTenSeconds()->runInBackground();

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단

1분 미만 간격 작업이 정의되어 있으면, `schedule:run` 명령은 해당 분이 끝날 때까지 계속 돌게 됩니다. 배포 시 이미 실행 중인 `schedule:run`이 종료되지 않으면, 이전 배포된 코드를 계속 사용하게 될 수 있습니다.

이런 경우, `schedule:interrupt` 명령을 배포 스크립트에 추가하여 실행 중인 스케줄러를 중단할 수 있습니다. 이 명령은 애플리케이션 배포 완료 후 호출하세요:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

로컬 개발 환경에서는 크론 항목을 추가하지 않고, `schedule:work` 아티즌 명령을 사용할 수 있습니다. 이 명령은 포그라운드에서 1분마다 스케줄러를 실행합니다. 1분 미만 주기의 작업이 정의되어 있을 경우, 당해 분 동안 계속 실행하며 처리합니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약 작업에서 생성되는 출력을 다루기 위한 다양한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드로 출력을 파일로 저장할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('emails:send')
        ->daily()
        ->sendOutputTo($filePath);

출력을 파일에 이어붙이고 싶다면 `appendOutputTo` 메서드를 사용하세요:

    Schedule::command('emails:send')
        ->daily()
        ->appendOutputTo($filePath);

`emailOutputTo` 메서드를 사용하면, 지정한 이메일 주소로 작업 출력을 전송할 수 있습니다. 단, 우선 Laravel의 [메일 서비스](/docs/{{version}}/mail)를 설정해야 합니다:

    Schedule::command('report:generate')
        ->daily()
        ->sendOutputTo($filePath)
        ->emailOutputTo('taylor@example.com');

명령이 정상 종료가 아닌 비정상 종료(0이 아닌 종료 코드)일 때만 이메일로 출력을 받고 싶다면 `emailOutputOnFailure`를 사용하세요:

    Schedule::command('report:generate')
        ->daily()
        ->emailOutputOnFailure('taylor@example.com');

> [!WARNING]  
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo`는 `command`와 `exec` 메서드로 예약된 작업에만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅(Hook)

`before` 및 `after` 메서드를 사용하여, 예약 작업 실행 전후에 코드가 실행되도록 할 수 있습니다:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('emails:send')
        ->daily()
        ->before(function () {
            // 작업이 곧 실행됨...
        })
        ->after(function () {
            // 작업이 실행됨...
        });

`onSuccess`와 `onFailure` 메서드를 사용하면 작업 성공/실패 시 실행할 코드를 정의할 수 있습니다. 실패는 예약된 아티즌 또는 시스템 명령이 0이 아닌 종료 코드로 끝나면 발생합니다:

    Schedule::command('emails:send')
        ->daily()
        ->onSuccess(function () {
            // 작업 성공...
        })
        ->onFailure(function () {
            // 작업 실패...
        });

명령의 출력을 활용하려면, 훅 클로저의 인자로 `Illuminate\Support\Stringable` 인스턴스를 타입힌트하면 `after`, `onSuccess`, `onFailure` 훅에서 출력값에 접근할 수 있습니다:

    use Illuminate\Support\Stringable;

    Schedule::command('emails:send')
        ->daily()
        ->onSuccess(function (Stringable $output) {
            // 작업 성공...
        })
        ->onFailure(function (Stringable $output) {
            // 작업 실패...
        });

<a name="pinging-urls"></a>
#### URL 핑(Ping)

`pingBefore` 및 `thenPing` 메서드를 사용하면, 예약 작업 전/후에 지정한 URL로 자동으로 핑을 보낼 수 있습니다. 이 메서드는 [Envoyer](https://envoyer.io)와 같은 외부 서비스에, 예약 작업 시작 혹은 완료를 알릴 때 유용합니다:

    Schedule::command('emails:send')
        ->daily()
        ->pingBefore($url)
        ->thenPing($url);

`pingOnSuccess`와 `pingOnFailure`는 작업 성공 또는 실패시에만 핑을 전송합니다:

    Schedule::command('emails:send')
        ->daily()
        ->pingOnSuccess($successUrl)
        ->pingOnFailure($failureUrl);

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 지정한 조건이 `true`일 때만 핑을 보냅니다:

    Schedule::command('emails:send')
        ->daily()
        ->pingBeforeIf($condition, $url)
        ->thenPingIf($condition, $url);             

    Schedule::command('emails:send')
        ->daily()
        ->pingOnSuccessIf($condition, $successUrl)
        ->pingOnFailureIf($condition, $failureUrl);

<a name="events"></a>
## 이벤트

Laravel은 스케줄링 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 아래의 이벤트에 대해 [리스너를 정의](/docs/{{version}}/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Console\Events\ScheduledTaskStarting` |
| `Illuminate\Console\Events\ScheduledTaskFinished` |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped` |
| `Illuminate\Console\Events\ScheduledTaskFailed` |

</div>