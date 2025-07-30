# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 전제 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 작성하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 이용한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 이용한 로그 메시지 실시간 보기](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내에서 무슨 일이 일어나고 있는지 파악하는 데 도움을 주기 위해, Laravel은 파일, 시스템 에러 로그, 그리고 Slack을 통해 팀 전체에 알림을 보내는 로그 서비스를 제공합니다.

Laravel 로깅은 "채널(channels)"을 기반으로 합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 로그를 단일 파일에 작성하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

기본적으로 Laravel은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하며, Monolog은 다양한 강력한 로그 핸들러를 지원합니다. Laravel은 이러한 핸들러를 쉽게 설정할 수 있도록 하여, 원하는 조합으로 애플리케이션 로그 처리를 커스터마이징할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 들어 있습니다. 이 파일에서 애플리케이션 로그 채널을 설정할 수 있으므로, 사용 가능한 여러 채널과 그 옵션들을 꼭 확인하세요. 아래에서 몇 가지 기본 옵션을 살펴보겠습니다.

기본적으로 Laravel은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶는 역할을 합니다. 로그 스택 구성에 관한 자세한 내용은 아래 [로그 스택 구성하기](#building-log-stacks) 문서를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버(driver)"에 의해 구동됩니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록되는지를 결정합니다. Laravel 애플리케이션에서 사용 가능한 드라이버는 다음과 같습니다. 대부분의 드라이버는 기본적으로 `config/logging.php` 내에 이미 설정되어 있으니 익숙해지세요:

<div class="overflow-auto">

| 이름           | 설명                                                                 |
| -------------- | -------------------------------------------------------------------- |
| `custom`       | 지정된 팩토리를 호출해 채널을 생성하는 드라이버입니다.                 |
| `daily`        | 일별로 로그 파일을 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버. |
| `errorlog`     | `ErrorLogHandler` 기반 Monolog 드라이버입니다.                        |
| `monolog`      | Monolog 핸들러를 이용하는 팩토리 드라이버입니다.                      |
| `papertrail`   | `SyslogUdpHandler` 기반 Monolog 드라이버입니다.                       |
| `single`       | 단일 파일 또는 경로 기반 로거 채널 (`StreamHandler`)입니다.           |
| `slack`        | `SlackWebhookHandler` 기반 Monolog 드라이버입니다.                    |
| `stack`        | 여러 채널을 묶어주는 래퍼 역할을 하는 드라이버입니다.                 |
| `syslog`       | `SyslogHandler` 기반 Monolog 드라이버입니다.                          |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대해 더 알고 싶으면 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정하기

기본적으로 Monolog은 현재 환경 이름(예: `production`, `local`)과 동일한 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하면 됩니다:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 전제 조건

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single`과 `daily` 채널엔 선택적 설정값인 `bubble`, `permission`, `locking` 옵션 3가지가 있습니다.

<div class="overflow-auto">

| 이름         | 설명                                                                         | 기본값  |
| ------------ | ----------------------------------------------------------------------------- | ------- |
| `bubble`     | 로그 메시지 처리 후 다른 채널에도 버블링(전달)할지 여부                         | `true`  |
| `locking`    | 파일 기록 전에 로그 파일을 잠글지 여부                                        | `false` |
| `permission` | 로그 파일의 파일 권한                                                         | `0644`  |

</div>

추가로, `daily` 채널의 보존 기간은 `LOG_DAILY_DAYS` 환경 변수나 `days` 설정 옵션으로 지정할 수 있습니다.

<div class="overflow-auto">

| 이름       | 설명                                      | 기본값  |
| ---------- | ----------------------------------------- | ------- |
| `days`     | 일별 로그 파일을 보존할 일수              | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 옵션이 필요합니다. 이는 `PAPERTRAIL_URL`과 `PAPERTRAIL_PORT` 환경변수로 정의할 수 있습니다. 값은 [Papertrail 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 참고하세요.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 옵션을 반드시 지정해야 하며, `LOG_SLACK_WEBHOOK_URL` 환경변수로 설정합니다. 이 URL은 Slack 팀에 설정한 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 주소여야 합니다.

기본적으로 Slack에는 `critical` 레벨 이상의 로그만 전송됩니다. 필요하다면 `LOG_LEVEL` 환경변수나 Slack 로그 채널 설정의 `level` 옵션으로 조정 가능합니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel 및 기타 라이브러리는 종종 기능 사용 중단(Deprecated) 경고를 사용자에게 알립니다. 이 경고를 로그에 남기고 싶다면, `LOG_DEPRECATIONS_CHANNEL` 환경변수로 원하는 로그 채널을 지정하거나, `config/logging.php` 설정에 명시하세요:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는 `deprecations`라는 로그 채널을 직접 정의해도 됩니다. 이 이름의 채널이 있으면 항상 사용 중단 경고 로그에 사용됩니다:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구성하기

앞서 언급했듯이, `stack` 드라이버는 여러 채널을 하나로 묶어 로그를 기록할 때 편리합니다. 프로덕션 애플리케이션에서 볼 수 있는 예시 설정을 보겠습니다:

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'], // [tl! add]
        'ignore_exceptions' => false,
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => env('LOG_LEVEL', 'debug'),
        'facility' => env('LOG_SYSLOG_FACILITY', LOG_USER),
        'replace_placeholders' => true,
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => env('LOG_SLACK_USERNAME', 'Laravel Log'),
        'emoji' => env('LOG_SLACK_EMOJI', ':boom:'),
        'level' => env('LOG_LEVEL', 'critical'),
        'replace_placeholders' => true,
    ],
],
```

이 설정을 자세히 보면, `stack` 채널은 `channels` 옵션으로 두 개의 채널(`syslog`, `slack`)을 묶고 있습니다. 즉, 로그가 기록될 때 두 채널 모두 메시지를 받아 처리할 수 있습니다. 다만, 아래에서 보겠지만 실제 메시지 기록 여부는 로그 심각도(level)에 따라 달라질 수 있습니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예제의 `syslog`와 `slack` 채널 설정에서 볼 수 있는 `level` 옵션은, 해당 채널이 기록할 최소 로그 레벨을 지정합니다. Monolog(즉, Laravel 로깅 서비스)는 [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에서 정의한 모든 로그 레벨을 지원합니다. 심각도 순서대로 나열하면: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, 그리고 **debug**입니다.

예를 들어, 만약 `debug` 레벨 메시지를 기록한다면:

```php
Log::debug('An informational message.');
```

현재 설정에 따르면 `syslog` 채널은 이 메시지를 시스템 로그에 기록하지만, `slack`은 `critical` 이상 레벨만 받도록 설정되어 있어 이 메시지는 전송되지 않습니다. 반면에 긴급 메시지인 경우:

```php
Log::emergency('The system is down!');
```

이 메시지는 두 채널 모두에 기록됩니다. (`emergency`는 두 채널에서 최소 레벨보다 높기 때문입니다.)

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

`Log` [퍼사드](/docs/12.x/facades)를 사용해 로그에 정보를 작성할 수 있습니다. 앞서 언급한 바와 같이, 로그는 RFC 5424 규격에 정의된 8가지 로그 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

```php
use Illuminate\Support\Facades\Log;

Log::emergency($message);
Log::alert($message);
Log::critical($message);
Log::error($message);
Log::warning($message);
Log::notice($message);
Log::info($message);
Log::debug($message);
```

이 메서드들 중 하나를 호출해 해당 레벨의 로그 메시지를 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에 지정된 기본 채널에 기록됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
     */
    public function show(string $id): View
    {
        Log::info('Showing the user profile for user: {id}', ['id' => $id]);

        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<a name="contextual-information"></a>
### 컨텍스트 정보

로그 메서드에 컨텍스트 데이터 배열을 전달할 수 있습니다. 이 컨텍스트 데이터는 로그 메시지와 함께 포매팅되어 보여집니다:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

가끔 특정 채널에서 모든 후속 로그 항목에 포함될 컨텍스트 정보를 지정하고 싶을 때가 있습니다. 예를 들어, 각 들어오는 요청에 대해 고유한 요청 ID를 로그에 남기고 싶다면, `Log` 퍼사드의 `withContext` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * 들어오는 요청 처리
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        $response = $next($request);

        $response->headers->set('Request-Id', $requestId);

        return $response;
    }
}
```

앱 내 _모든_ 로그 채널에 공통 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 호출하면 됩니다. 이 메서드는 이후 생성되는 모든 채널에 컨텍스트 정보를 전달합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * 들어오는 요청 처리
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::shareContext([
            'request-id' => $requestId
        ]);

        // ...
    }
}
```

> [!NOTE]
> 큐 작업을 처리하는 동안 로그 컨텍스트를 공유해야 할 경우, [잡 미들웨어](/docs/12.x/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 작성하기

기본 채널이 아닌 다른 채널에 로그를 기록하고 싶을 때는 `Log` 퍼사드의 `channel` 메서드를 이용해 해당 채널을 불러와 로그할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

복수 채널을 묶은 임시 로그 스택을 만들고 싶으면 `stack` 메서드를 사용하는 방법도 있습니다:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드 채널

애플리케이션 설정 파일에 미리 정의하지 않고 실행 시점에 로그 채널 구성을 지정할 수도 있습니다. 이때는 `Log` 퍼사드의 `build` 메서드에 설정 배열을 전달하세요:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

온디맨드 채널 인스턴스를 포함해 온디맨드 로그 스택도 만들 수 있습니다. `stack` 메서드에 해당 채널 인스턴스를 배열에 넣으면 됩니다:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog 채널 커스터마이징

<a name="customizing-monolog-for-channels"></a>
### 채널별 Monolog 커스터마이징

기존 채널에서 Monolog 설정을 완전히 제어하고 싶을 때가 있습니다. 예를 들어, 내장 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현을 적용하고 싶을 수 있죠.

먼저, 채널 설정에 `tap` 배열을 추가하세요. `tap`에 들어가는 클래스는 Monolog 인스턴스가 생성된 후 이를 커스터마이징할 기회를 갖습니다. 이 클래스들은 원하는 위치에 자유롭게 만들 수 있습니다:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

이제 Monolog 인스턴스를 커스터마이징할 클래스를 정의합니다. 이 클래스에는 오직 하나의 메서드 `__invoke`만 있으면 됩니다. 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 인자로 받는데, 이 인스턴스는 실제 Monolog 객체에 호출을 위임합니다:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 주어진 로거 인스턴스를 커스터마이징합니다.
     */
    public function __invoke(Logger $logger): void
    {
        foreach ($logger->getHandlers() as $handler) {
            $handler->setFormatter(new LineFormatter(
                '[%datetime%] %channel%.%level_name%: %message% %context% %extra%'
            ));
        }
    }
}
```

> [!NOTE]
> 모든 `tap` 클래스는 [서비스 컨테이너](/docs/12.x/container)에 의해 자동으로 인스턴스화되므로, 생성자 의존성도 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있지만, Laravel이 모두 기본 지원하지는 않습니다. 따라서 Laravel 로그 드라이버로 제공되지 않는 특정 Monolog 핸들러 인스턴스만을 위한 채널을 직접 만들고 싶을 때, `monolog` 드라이버를 사용하면 됩니다.

`monolog` 드라이버를 사용할 때는 어떤 핸들러를 인스턴스화할지 `handler` 옵션에 클래스를 지정합니다. 또한, 핸들러 생성자에 필요한 인수가 있다면 `handler_with` 옵션에 배열로 전달하세요:

```php
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'handler_with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```

<a name="monolog-formatters"></a>
#### Monolog 포매터

`monolog` 드라이버 사용 시 기본 포매터는 Monolog의 `LineFormatter`입니다. 그렇지만 `formatter`와 `formatter_with` 옵션으로 어떤 포매터를 사용할지 변경할 수 있습니다:

```php
'browser' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\BrowserConsoleHandler::class,
    'formatter' => Monolog\Formatter\HtmlFormatter::class,
    'formatter_with' => [
        'dateFormat' => 'Y-m-d',
    ],
],
```

만약 핸들러가 자체 포매터를 제공한다면, `formatter` 옵션을 `'default'`로 지정할 수도 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog은 로그 메시지를 기록하기 전에 가공하는 프로세서도 지원합니다. 직접 프로세서를 만들거나 Monolog이 제공하는 [기본 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

`monolog` 드라이버의 프로세서 설정은 채널 설정에 `processors` 배열을 추가해 지정합니다:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 예
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션이 포함된 예
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 이용한 커스텀 채널 생성

Monolog 인스턴스를 완전히 직접 제어하는 맞춤 채널을 만들고 싶다면, `config/logging.php`에서 `custom` 드라이버 유형을 지정할 수 있습니다. 이때 `via` 옵션에 Monolog 인스턴스를 생성하는 팩토리 클래스 이름을 넣으세요:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 설정 후에는 해당 클래스에 단일 `__invoke` 메서드를 정의하면 됩니다. 이 메서드는 Monolog 로거 인스턴스를 반환해야 하며, 설정 배열이 인자로 전달됩니다:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * 커스텀 Monolog 인스턴스 생성
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Pail을 이용한 로그 메시지 실시간 보기

문제를 디버깅하거나 특정 오류 유형을 실시간으로 모니터링하고 싶을 때, 애플리케이션 로그를 실시간으로 보는 것이 유용합니다.

Laravel Pail은 Laravel 애플리케이션 로그 파일을 명령줄에서 쉽게 실시간으로 확인할 수 있도록 돕는 패키지입니다. 일반 `tail` 명령과 달리, Pail은 Sentry나 Flare 같은 다양한 로그 드라이버도 지원하며, 유용한 필터 기능도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail 사용을 위해 PHP의 [PCNTL 확장](https://www.php.net/manual/en/book.pcntl.php)이 필요합니다.

프로젝트에 Pail을 설치하려면, Composer를 사용하세요:

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 실시간 보기(tail)를 시작하려면 다음 명령어를 실행합니다:

```shell
php artisan pail
```

출력의 가독성을 높이고 생략 부호(…) 없이 전체 로그를 보려면 `-v` 옵션을 붙이세요:

```shell
php artisan pail -v
```

최대한 상세한 출력과 예외 스택 트레이스까지 보고 싶다면 `-vv` 옵션을 사용합니다:

```shell
php artisan pail -vv
```

실시간 로그 보기를 종료하려면 언제든 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션으로 로그 유형, 파일, 메시지, 스택 트레이스 내용 등을 기준으로 필터링할 수 있습니다:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 내용만으로 필터링하려면 `--message` 옵션을 사용하세요:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

로그 레벨 기준 필터링은 `--level` 옵션으로 수행합니다:

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 보고 싶다면, `--user` 옵션에 사용자 ID를 지정하세요:

```shell
php artisan pail --user=1
```