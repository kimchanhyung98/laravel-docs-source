# 로깅

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 조건](#channel-prerequisites)
    - [폐기 예정 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널로 작성](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리로 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail로 로그 메시지 실시간 감시](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내에서 어떤 일이 발생하고 있는지 더 잘 파악할 수 있도록, Laravel은 다양한 로그 메시지를 파일, 시스템 에러 로그 또는 Slack으로 기록해 팀 전체에 알릴 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel의 로깅은 "채널"을 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 로그 파일에 기록하며, `slack` 채널은 Slack으로 로그 메시지를 전송합니다. 로그 메시지는 심각도에 따라 여러 채널로 동시에 기록될 수 있습니다.

Laravel은 내부적으로 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. Monolog는 다양한 강력한 로그 핸들러를 지원하며, Laravel은 이 핸들러의 설정을 손쉽게 할 수 있도록 하여 다양한 조합으로 애플리케이션의 로그 처리를 커스터마이징할 수 있게 해줍니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 구성 파일에 있습니다. 이 파일에서 로그 채널들을 설정할 수 있으니, 각 채널과 옵션을 반드시 확인하세요. 여기서 일반적으로 자주 사용하는 옵션을 몇 가지 살펴보겠습니다.

기본적으로 Laravel은 메시지 로깅 시 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 구성에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 구동됩니다. 드라이버는 로그 메시지를 실제로 어떻게, 어디에 기록할지 결정합니다. 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버는 다음과 같습니다. 대부분의 드라이버는 이미 애플리케이션의 `config/logging.php` 파일에 포함되어 있으니, 이 파일을 꼼꼼히 살펴보세요:

<div class="overflow-auto">

| 이름         | 설명                                                            |
| ------------ | -------------------------------------------------------------- |
| `custom`     | 지정한 팩토리를 호출해 채널을 생성하는 드라이버.                   |
| `daily`      | 매일 파일을 롤링하는 `RotatingFileHandler` 기반 Monolog 드라이버.  |
| `errorlog`   | `ErrorLogHandler` 기반 Monolog 드라이버.                         |
| `monolog`    | 지원하는 모든 Monolog 핸들러를 사용할 수 있는 Monolog 공장 드라이버.|
| `papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버.                        |
| `single`     | 단일 파일 또는 경로 기반 로거 채널 (`StreamHandler`).             |
| `slack`      | `SlackWebhookHandler` 기반 Monolog 드라이버.                     |
| `stack`      | "다중 채널" 채널 생성을 위한 래퍼.                               |
| `syslog`     | `SyslogHandler` 기반 Monolog 드라이버.                           |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경(예: `production`, `local`)과 일치하는 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하고 싶다면, 채널 설정에 `name` 옵션을 추가하세요:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 사전 조건

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널에는 선택적 설정 옵션으로 `bubble`, `permission`, `locking`이 있습니다.

<div class="overflow-auto">

| 이름         | 설명                                                                | 기본값  |
| ------------ | ------------------------------------------------------------------- | ------- |
| `bubble`     | 메시지 처리 후 다른 채널로 전파할지 여부.                            | `true`  |
| `locking`    | 기록 전 로그 파일 잠금 시도.                                         | `false` |
| `permission` | 로그 파일 퍼미션.                                                  | `0644`  |

</div>

또한, `daily` 채널의 로그 보관 기간은 `LOG_DAILY_DAYS` 환경 변수 또는 `days` 옵션을 통해 설정할 수 있습니다.

<div class="overflow-auto">

| 이름    | 설명                                              | 기본값 |
| ------- | ------------------------------------------------- | ------ |
| `days`  | 일일 로그 파일을 유지할 일수.                      | `14`   |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정이 필요합니다. 이 값들은 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수로 정의할 수 있습니다. 해당 값들은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인 가능합니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 설정이 필요합니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경변수로 정의할 수 있습니다. 해당 URL은 [Slack 수신 Webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)에서 발급받으세요.

기본적으로, Slack은 `critical` 레벨 이상의 로그만 수신합니다. 이 동작은 `LOG_LEVEL` 환경변수나 Slack 로그 채널의 `level` 옵션을 수정해 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 폐기 예정 경고 로깅

PHP, Laravel, 그리고 여러 라이브러리는 일부 기능이 폐기(deprecated)될 예정임을 사용자에게 알립니다. 이런 폐기 경고를 로그로 남기고 싶다면, `LOG_DEPRECATIONS_CHANNEL` 환경변수 또는 애플리케이션의 `config/logging.php` 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는, `deprecations`라는 이름의 로그 채널을 정의해도 됩니다. 해당 이름의 채널이 있으면, 항상 여기에 폐기 경고가 기록됩니다:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구성

앞서 설명했듯, `stack` 드라이버는 여러 채널을 하나의 로그 채널로 결합하는 기능을 제공합니다. 생산 환경에서 자주 볼 수 있는 구성 예시는 다음과 같습니다:

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

이 구성을 살펴보면, `stack` 채널이 `syslog`, `slack` 두 채널을 `channels` 옵션으로 묶고 있습니다. 즉, 로그 메시지를 기록할 때 두 채널 모두 메시지를 기록할 수 있습니다. 하지만 메시지가 실제로 각 채널에 기록되는지는 메시지의 심각도(레벨)에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시 구성의 `syslog` 및 `slack` 채널에 있는 `level` 옵션을 주목하세요. 이 옵션은 해당 채널에 기록되기 위한 최소 "레벨"을 결정합니다. Laravel 로깅 서비스의 기반인 Monolog는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에서 정의된 모든 로그 레벨을 지원합니다. 심각도 순으로, 로그 레벨은 **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

예를 들어, `debug` 메서드로 메시지를 기록할 경우:

```php
Log::debug('An informational message.');
```

이 구성에 따르면 `syslog` 채널은 메시지를 시스템 로그에 기록하게 됩니다. 하지만 메시지 레벨이 `critical` 이하거나 그보다 높지 않으므로 Slack에는 메시지가 전송되지 않습니다. 반면, `emergency` 메시지는 두 채널 모두에 전송됩니다.

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성

`Log` [파사드](/docs/{{version}}/facades)를 사용해 로그에 정보를 기록할 수 있습니다. 앞서 언급했듯, 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에서 정의한 **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 8개 로그 레벨을 지원합니다:

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

각 메서드를 호출하면 해당 레벨에 맞는 로그 메시지가 기록됩니다. 기본적으로 메시지는 `logging` 설정 파일에서 지정한 기본 로그 채널에 기록됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
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

로그 메서드에는 컨텍스트 데이터 배열을 전달할 수 있습니다. 이 데이터는 로그 메시지와 함께 포매팅되어 표시됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널의 모든 로그 엔트리에 포함될 컨텍스트 정보가 필요한 경우가 있습니다. 예를 들어, 각 요청에 연결된 Request ID를 로그에 남기고 싶을 때, `Log` 파사드의 `withContext` 메서드를 사용하면 됩니다:

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
     * Handle an incoming request.
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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하려면, `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드를 호출하면, 이미 생성된 모든 채널과 이후 생성되는 모든 채널에 해당 컨텍스트 정보가 제공됩니다:

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
     * Handle an incoming request.
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
> 큐 작업 처리 중 로그 컨텍스트를 공유할 필요가 있을 때는 [작업 미들웨어](/docs/{{version}}/queues#job-middleware)를 활용하세요.

<a name="writing-to-specific-channels"></a>
### 특정 채널로 작성

기본 로그 채널 이외의 채널에 로그를 남기고 싶을 때는, `Log` 파사드의 `channel` 메서드를 사용해 설정 파일에 정의된 채널을 지정해 기록할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 동시에 묶어 임시로 로그를 생성하려면, `stack` 메서드를 사용할 수 있습니다:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드 채널

애플리케이션의 `logging` 설정 파일에 없는 특정 구성을 런타임에 직접 전달해, 임시 온디맨드 채널을 만들 수도 있습니다. 이를 위해서는 설정 배열을 `Log` 파사드의 `build` 메서드에 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

온디맨드 채널을 온디맨드 스택에 포함시키고 싶을 때는, 해당 채널 인스턴스를 `stack` 메서드의 배열에 추가하면 됩니다:

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

가끔은 기존 채널에 Monolog 설정을 완전히 커스터마이징해야 할 수도 있습니다. 예를 들어, Laravel 내장 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현을 적용하고 싶을 때가 이에 해당합니다.

이를 위해 채널 설정에 `tap` 배열을 정의하세요. 이 배열에는 Monolog 인스턴스가 생성된 후 커스터마이즈(탭) 할 기회를 받을 클래스 목록이 들어갑니다. 위치는 자유롭게 정해 별도 디렉토리를 생성해서 클래스를 보관하십시오:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

`tap` 옵션을 설정했다면, 이제 Monolog 인스턴스를 커스터마이즈할 클래스를 작성해야 합니다. 이 클래스는 `Illuminate\Log\Logger` 인스턴스를 받는 `__invoke` 메서드 하나만 필요합니다. `Logger` 인스턴스는 모든 메서드 호출을 내부 Monolog 인스턴스로 넘깁니다:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * Customize the given logger instance.
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
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)로 해석되므로, 생성자 의존성은 자동 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 지원하며, Laravel은 그 모든 핸들러에 내장 채널을 제공하지 않습니다. 특정 Monolog 핸들러를 위한 커스텀 채널이 필요하다면, `monolog` 드라이버를 사용해 쉽게 생성할 수 있습니다.

`monolog` 드라이버 사용 시, `handler` 옵션으로 인스턴스화할 핸들러를 지정합니다. 핸들러에 생성자 인자가 필요하다면 `handler_with` 옵션에 함께 명시합니다:

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

`monolog` 드라이버를 사용할 때 기본 포매터는 Monolog의 `LineFormatter`입니다. 그러나 `formatter`와 `formatter_with` 옵션으로 핸들러에 전달할 포매터 유형을 커스터마이즈할 수 있습니다:

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

Monolog 핸들러가 자체 포매터를 지원하는 경우, `formatter` 옵션에 `default`를 설정하면 됩니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog는 로그 메시지를 기록하기 전에 프로세싱할 수도 있습니다. 사용자 정의 프로세서를 만들거나 [Monolog의 내장 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

`monolog` 드라이버에서 프로세서를 커스터마이즈하려면, 로그 채널 설정에 `processors` 값을 추가하세요:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 방식...
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션과 함께...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리로 커스텀 채널 생성

Monolog 인스턴스화와 설정을 완전히 직접 제어하고 싶을 때는, `config/logging.php` 파일에서 `custom` 드라이버 타입을 사용할 수 있습니다. 설정에는 `via` 옵션이 필요하며, 이 옵션에 Monolog 인스턴스를 생성할 팩토리 클래스명을 지정합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 채널을 설정했다면, 이제 Monolog 인스턴스를 생성할 클래스를 정의해야 합니다. 이 클래스는 Monolog Logger 인스턴스를 반환하는 `__invoke` 메서드 하나만 구현하면 됩니다. 해당 메서드는 채널 설정 배열을 인자로 받습니다:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * Create a custom Monolog instance.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Pail로 로그 메시지 실시간 감시

애플리케이션 로그를 실시간 감시해야 할 때가 종종 있습니다. 예를 들어, 이슈 디버깅 혹은 특정 유형의 오류를 모니터링할 때 그렇습니다.

Laravel Pail은 커맨드라인에서 바로 Laravel 애플리케이션의 로그 파일을 손쉽게 탐색할 수 있게 하는 패키지입니다. 일반 `tail` 명령과 달리, Pail은 Sentry, Flare와 같은 다양한 로그 드라이버와도 연동되도록 설계되었습니다. 또한 원하는 정보를 빠르게 찾을 수 있도록 유용한 필터 기능을 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PHP 8.2+](https://php.net/releases/)와 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장 모듈이 필요합니다.

먼저 Composer 패키지 매니저로 Pail을 설치하세요:

```shell
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 실시간 감시를 시작하려면, 다음 명령을 실행하세요:

```shell
php artisan pail
```

출력의 상세도를 높이고 잘림(…) 없이 보려면 `-v` 옵션을 사용하세요:

```shell
php artisan pail -v
```

최대 상세도와 예외 스택 트레이스까지 출력하려면 `-vv` 옵션을 사용하세요:

```shell
php artisan pail -vv
```

감시 모드를 중단하려면 언제든 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션으로 로그의 유형, 파일, 메시지, 스택 트레이스까지 필터링할 수 있습니다:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 내용만으로 로그를 필터링하려면 `--message` 옵션을 사용합니다:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` 옵션은 [로그 레벨](#log-levels)별로 로그를 필터링할 수 있습니다:

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 작성된 로그만 보려면 `--user` 옵션에 사용자 ID를 지정하세요:

```shell
php artisan pail --user=1
```
