# 로깅 (Logging)

- [소개](#introduction)
- [구성](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 준비 사항](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구축](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보 추가](#contextual-information)
    - [특정 채널로 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이즈](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이즈](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 만들기](#creating-monolog-handler-channels)
    - [팩토리로 커스텀 채널 만들기](#creating-custom-channels-via-factories)
- [Pail을 이용한 로그 실시간 조회](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내부에서 어떤 일이 일어나는지 쉽게 파악할 수 있도록, 라라벨은 강력한 로깅 서비스를 제공합니다. 이를 통해 파일, 시스템 에러 로그, 그리고 전체 팀에 알림을 보낼 수 있는 Slack 등 다양한 곳에 로그 메시지를 남길 수 있습니다.

라라벨의 로깅 시스템은 "채널(channel)" 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 의미합니다. 예를 들어, `single` 채널은 하나의 로그 파일에 메시지를 기록하고, `slack` 채널은 Slack으로 로그 메시지를 전송합니다. 메시지의 심각도(severity)에 따라 여러 채널에 동시에 기록할 수도 있습니다.

내부적으로 라라벨은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하여 다양한 강력한 로그 핸들러를 지원합니다. 라라벨은 이러한 핸들러의 설정을 쉽게 하도록 도와주며, 여러분이 애플리케이션에 맞게 적절히 조합해서 원하는 방식의 로깅을 처리할 수 있도록 설계되었습니다.

<a name="configuration"></a>
## 구성

애플리케이션의 로깅 동작을 제어하는 모든 설정은 `config/logging.php` 설정 파일에 정의되어 있습니다. 이 파일에서는 로그 채널을 구성할 수 있으며, 제공되는 다양한 채널과 그 옵션을 꼼꼼히 살펴보아야 합니다. 아래에서 자주 사용하는 몇 가지 옵션을 간단히 확인해보겠습니다.

기본적으로 라라벨은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어서 사용하는 기능을 담당합니다. 스택을 구축하는 방법은 아래 [문서](#building-log-stacks)에서 더 자세히 설명합니다.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버(driver)"에 의해 동작합니다. 드라이버는 로그 메시지가 실제로 어디에, 어떻게 저장될지 결정합니다. 아래 드라이버들은 모든 라라벨 애플리케이션에서 사용 가능하며, 대부분은 이미 여러분의 애플리케이션 `config/logging.php` 파일에 기본적으로 포함되어 있습니다. 해당 파일을 직접 확인하여 구조를 익혀 보시기 바랍니다.

<div class="overflow-auto">

| 이름         | 설명                                                                    |
| ------------ | ----------------------------------------------------------------------- |
| `custom`     | 지정한 팩토리를 호출해 채널을 생성하는 드라이버입니다.                   |
| `daily`      | 매일 파일을 교체하는 `RotatingFileHandler` 기반 Monolog 드라이버입니다. |
| `errorlog`   | `ErrorLogHandler` 기반 Monolog 드라이버입니다.                           |
| `monolog`    | 어떤 Monolog 핸들러도 사용할 수 있는 Monolog 팩토리 드라이버입니다.      |
| `papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버입니다.                         |
| `single`     | 하나의 파일 또는 경로에 기록하는 `StreamHandler` 기반 로거 채널입니다.  |
| `slack`      | `SlackWebhookHandler` 기반 Monolog 드라이버입니다.                      |
| `stack`      | "멀티채널" 채널 생성을 위한 래퍼입니다.                                 |
| `syslog`     | `SyslogHandler` 기반 Monolog 드라이버입니다.                            |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이즈](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 지정

기본적으로 Monolog는 현재 환경 값(예: `production`, `local`)을 "채널 이름"으로 사용하여 인스턴스를 생성합니다. 값을 변경하고 싶다면 채널 설정에 `name` 옵션을 추가하면 됩니다.

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 사전 준비 사항

<a name="configuring-the-single-and-daily-channels"></a>
#### Single, Daily 채널 설정

`single` 및 `daily` 채널에는 `bubble`, `permission`, `locking`이라는 세 가지 선택적 설정 옵션이 있습니다.

<div class="overflow-auto">

| 이름         | 설명                                                                             | 기본값  |
| ------------ | -------------------------------------------------------------------------------- | ------- |
| `bubble`     | 메시지 처리 후에도 다른 채널로 전달("bubble up")할지 여부를 지정합니다.           | `true`  |
| `locking`    | 로그 파일에 기록하기 전에 잠금을 시도할지 여부입니다.                             | `false` |
| `permission` | 로그 파일 생성 시 부여할 파일 권한입니다.                                         | `0644`  |

</div>

또한, `daily` 채널의 로그 보관 정책은 `LOG_DAILY_DAYS` 환경 변수나 `days` 설정 옵션으로 지정할 수 있습니다.

<div class="overflow-auto">

| 이름   | 설명                                                     | 기본값 |
| ------ | -------------------------------------------------------- | ------ |
| `days` | 일일 로그 파일을 며칠 동안 보관할지 지정합니다.           | `14`   |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널을 사용하려면 `host`와 `port` 설정이 필수입니다. 이는 각각 `PAPERTRAIL_URL`, `PAPERTRAIL_PORT` 환경 변수로 정의할 수 있습니다. Papertrail 관련 정보는 [Papertrail 안내](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 반드시 `url` 설정값이 필요합니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 지정할 수 있고, 여러분의 Slack 팀에서 설정한 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)의 URL과 일치해야 합니다.

기본적으로 Slack은 `critical` 레벨 이상의 로그만 수신하게 되어 있지만, `LOG_LEVEL` 환경 변수나 해당 채널 설정 배열의 `level` 옵션을 통해 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, 라라벨, 그리고 기타 라이브러리들은 일부 기능이 지원 중단(deprecated)되었으며, 향후 버전에서 제거될 것임을 사용자에게 알리기도 합니다. 이러한 사용 중단 경고를 별도로 로그에 남기고 싶다면, 환경 변수 `LOG_DEPRECATIONS_CHANNEL` 또는 `config/logging.php` 설정 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다.

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

혹은, 이름이 `deprecations`인 로그 채널을 추가로 정의해도 됩니다. 이렇게 하면 해당 채널로 항상 사용 중단 경고가 기록됩니다.

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구축

앞서 설명한 것처럼, `stack` 드라이버를 이용하면 여러 채널을 하나의 로그 채널로 묶어 사용할 수 있어 매우 편리합니다. 실제 프로덕션 애플리케이션에서 사용할 수 있는 예시 설정을 살펴보겠습니다.

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

이 설정을 하나씩 살펴보면, 먼저 `stack` 채널의 `channels` 옵션에 `syslog`와 `slack`이 지정된 것을 알 수 있습니다. 그래서 로그 메시지가 발생하면 이 두 채널 모두가 로그 메시지를 받을 기회를 갖게 됩니다. 다만 실제로 각 채널에 기록되는지 여부는 메시지의 심각도(레벨)에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예제에서 `syslog`, `slack` 채널 설정에 각각 `level` 옵션이 지정되어 있습니다. 이 옵션은 메시지가 해당 채널에 남겨지기 위해 최소한 가져야 하는 "레벨"을 의미합니다. 라라벨의 로깅 서비스는 Monolog를 기반으로 하며, [RFC 5424 표준](https://tools.ietf.org/html/rfc5424)의 모든 로그 레벨을 지원합니다. 심각도가 높은 순서대로 **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**가 있습니다.

예를 들어, 아래처럼 `debug` 메서드로 메시지를 기록한다고 가정해봅시다.

```php
Log::debug('An informational message.');
```

이 설정대로라면 `syslog` 채널은 해당 메시지를 시스템 로그에 기록하지만, 이 메시지가 `critical` 이상이 아니므로 Slack에는 전송되지 않습니다. 하지만, 만약 `emergency` 레벨 메시지를 기록한다면, 두 채널 모두에 로그가 남게 됩니다. 왜냐하면 `emergency` 레벨은 각 채널의 최소 레벨보다 높기 때문입니다.

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성

로그에 정보를 남길 때는 `Log` [파사드](/docs/12.x/facades)를 사용할 수 있습니다. 앞서 언급한 대로, 라라벨의 로그 파사드는 [RFC 5424 표준](https://tools.ietf.org/html/rfc5424)에서 정의한 8가지 로그 레벨(**emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**)을 모두 제공합니다.

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

이 중 원하는 메서드를 호출하면 해당 로그 레벨로 메시지가 기록됩니다. 기본적으로 `logging` 설정 파일에서 지정한 기본 로그 채널에 메시지가 저장됩니다.

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
### 컨텍스트 정보 추가

로그 메서드에 컨텍스트 데이터 배열을 함께 전달할 수 있습니다. 이렇게 전달된 데이터는 로그 메시지와 함께 포맷되어 출력됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

때때로, 모든 이후 로그 메시지에 포함했으면 하는 컨텍스트 정보가 있을 수 있습니다. 예를 들어 각 요청마다 고유한 request ID를 로그에 포함하고 싶다면, `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다.

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

모든 로깅 채널에 컨텍스트 정보를 공유하고 싶다면 `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 방법은 이미 생성된 채널은 물론, 이후 생성되는 모든 채널에 컨텍스트 정보가 적용됩니다.

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
> 큐(job) 처리 중에도 로그 컨텍스트를 공유해야 한다면, [잡 미들웨어](/docs/12.x/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널로 기록하기

기본 로그 채널 이외의 채널에 메시지를 남기고 싶을 때는 `Log` 파사드의 `channel` 메서드를 사용하여, 설정 파일에 정의된 임의의 채널로 로그를 남길 수 있습니다.

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 묶어 즉시(on-demand) 스택을 만들어 로그를 남기고 싶을 때는 `stack` 메서드를 사용할 수 있습니다.

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드(즉석) 채널

`logging` 설정 파일에 별도로 정의하지 않아도, 런타임에 설정 배열을 전달해 임시로 채널을 생성할 수도 있습니다. 이때는 `Log` 파사드의 `build` 메서드를 사용하면 됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

그리고 이렇게 생성한 임시(on-demand) 채널을 기존 스택에 포함시켜 사용할 수도 있습니다.

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog 채널 커스터마이즈

<a name="customizing-monolog-for-channels"></a>
### 채널별 Monolog 커스터마이즈

기존 채널의 Monolog 설정을 완전히 제어하고 싶을 때가 있을 수 있습니다. 예를 들어, 라라벨에서 제공하는 `single` 채널에 커스텀 Monolog `FormatterInterface`를 적용하고 싶을 때가 그렇습니다.

먼저, 채널 설정에 `tap` 배열을 추가합니다. `tap` 배열에는 Monolog 인스턴스가 생성된 후에 커스터마이즈(또는 "tap")할 클래스를 나열합니다. 클래스 파일 위치에 특별한 제약은 없으니, 애플리케이션 내에 자유롭게 디렉터리를 만들어 관리하면 됩니다.

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

`tap` 옵션을 설정했다면, 이제 Monolog 인스턴스를 커스터마이즈할 클래스를 정의할 차례입니다. 이 클래스에는 `Illuminate\Log\Logger` 타입을 받는 단일 메서드인 `__invoke`가 필요합니다. 그리고 이 객체를 통해 실제 Monolog 인스턴스로 접근 가능합니다.

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
> `"tap"`에 등록된 모든 클래스는 [서비스 컨테이너](/docs/12.x/container)에서 자동으로 의존성 주입이 지원됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 만들기

Monolog에는 다양한 [핸들러(handler)](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 존재하지만, 라라벨에서는 모든 핸들러에 맞는 기본 채널이 준비되어 있지는 않습니다. 특정 Monolog 핸들러 기반의 커스텀 채널이 필요한 경우, `monolog` 드라이버를 활용하여 간단히 만들 수 있습니다.

`monolog` 드라이버를 사용할 때는 `handler` 옵션에 사용할 핸들러를 지정합니다. 필요하다면, 해당 핸들러의 생성자 인수는 `handler_with` 옵션 배열로 넘길 수 있습니다.

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

`monolog` 드라이버를 사용할 때 기본적으로 Monolog의 `LineFormatter`가 사용됩니다. 하지만 `formatter`, `formatter_with` 설정을 통해 핸들러에 전달할 포매터를 커스터마이즈할 수 있습니다.

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

Monolog 핸들러 자체에 기본 포매터가 내장되어 있다면, `formatter` 설정값을 `default`로 지정할 수도 있습니다.

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog는 로그가 기록되기 전 메시지를 전처리할 수 있습니다. 직접 프로세서를 만들 수도 있고, [Monolog가 제공하는 다양한 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수도 있습니다.

`monolog` 드라이버에서 프로세서를 커스터마이즈하려면 `processors` 설정값을 채널에 추가하세요.

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
### 팩토리로 커스텀 채널 만들기

Monolog의 인스턴스화 및 설정을 자유롭게 완전 제어할 수 있는 커스텀 채널을 만들고 싶다면, `config/logging.php`에 `custom` 드라이버 타입을 지정하세요. 이때 `via` 옵션에 Monolog 인스턴스를 생성할 팩토리 클래스명을 지정해야 합니다.

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

이제 `custom` 드라이버 채널을 구성했으니, 실질적인 Monolog 인스턴스를 생성할 클래스를 만들어야 합니다. 이 클래스에는 `__invoke` 메서드만 하나 있으면 되며, 인수로는 채널 설정 배열이 전달됩니다. 반환값은 Monolog 로그 인스턴스여야 합니다.

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
## Pail을 이용한 로그 실시간 조회

애플리케이션 로그를 실시간으로 조회(테일링)해야 할 때가 종종 있습니다. 예를 들어, 버그를 디버깅하거나 특정 유형의 에러를 실시간으로 모니터링할 때 그렇습니다.

Laravel Pail은 라라벨 애플리케이션의 로그 파일을 커맨드라인에서 실시간으로 탐색할 수 있도록 도와주는 패키지입니다. 표준 `tail` 명령과 달리, Pail은 Sentry나 Flare와 같은 다양한 로그 드라이버와도 연동됩니다. 또한 원하는 정보를 빠르게 찾을 수 있도록 유용한 필터 기능도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail을 사용하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 기능이 필요합니다.

먼저, Composer 패키지 관리자를 이용해 Pail을 개발 의존성으로 설치합니다.

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 테일링(실시간 조회)을 시작하려면 `pail` 명령어를 실행하세요.

```shell
php artisan pail
```

출력 정보를 더 자세히 보고 내용이 생략(…)되는 것을 방지하려면 `-v` 옵션을 사용할 수 있습니다.

```shell
php artisan pail -v
```

가장 상세한 정보와 예외 스택 트레이스까지 표시하려면 `-vv` 옵션을 사용하세요.

```shell
php artisan pail -vv
```

로그 테일링을 중단하려면 언제든 `Ctrl+C`를 누르시면 됩니다.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션을 사용하면 로그의 유형, 파일, 메시지, 스택 트레이스 내용 등을 기준으로 원하는 로그만 필터링할 수 있습니다.

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

로그 메시지 내용 기준으로 필터링하고 싶을 때는 `--message` 옵션을 사용합니다.

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` 옵션으로 [로그 레벨](#log-levels)을 지정하면 해당 레벨의 로그만 출력됩니다.

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 보고 싶다면 `--user` 옵션에 사용자 ID를 전달하시면 됩니다.

```shell
php artisan pail --user=1
```