# Logging

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Available Channel Drivers](#available-channel-drivers)
    - [Channel Prerequisites](#channel-prerequisites)
    - [Logging Deprecation Warnings](#logging-deprecation-warnings)
- [Building Log Stacks](#building-log-stacks)
- [Writing Log Messages](#writing-log-messages)
    - [Contextual Information](#contextual-information)
    - [Writing to Specific Channels](#writing-to-specific-channels)
- [Monolog Channel Customization](#monolog-channel-customization)
    - [Customizing Monolog for Channels](#customizing-monolog-for-channels)
    - [Creating Monolog Handler Channels](#creating-monolog-handler-channels)
    - [Creating Custom Channels via Factories](#creating-custom-channels-via-factories)
- [Tailing Log Messages Using Pail](#tailing-log-messages-using-pail)
    - [Installation](#pail-installation)
    - [Usage](#pail-usage)
    - [Filtering Logs](#pail-filtering-logs)

<a name="소개"></a>
## Introduction

애플리케이션 내에서 일어나는 일에 대해 자세히 알 수 있도록 Laravel은 파일, 시스템 오류 로그, 심지어 Slack에 메시지를 기록하여 전체 팀에 알릴 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel 로깅은 "채널"을 기반으로 합니다. 각 채널은 로그 정보를 기록하는 특정 방법을 나타냅니다. 예를 들어, `단일` 채널은 단일 로그 파일에 로그 파일을 작성하고, `슬랙` 채널은 로그 메시지를 Slack으로 보냅니다. 로그 메시지는 심각도에 따라 여러 채널에 기록될 수 있습니다.

내부적으로 Laravel은 다양하고 강력한 로그 핸들러를 지원하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 활용합니다. Laravel을 사용하면 이러한 핸들러를 쉽게 구성할 수 있으므로 애플리케이션의 로그 처리를 사용자 정의하기 위해 혼합 및 조합할 수 있습니다.

<a name="configuration"></a>
## Configuration

애플리케이션의 로깅 동작을 제어하는 모든 구성 옵션은 `config/logging.php` 구성 파일에 있습니다. 이 파일을 통해 애플리케이션의 로그 채널을 구성할 수 있으므로 사용 가능한 각 채널과 해당 옵션을 검토해야 합니다. 아래에서 몇 가지 일반적인 옵션을 검토하겠습니다.

기본적으로 Laravel은 메시지를 로깅할 때 `stack` 채널을 사용합니다. 스택` 채널은 여러 로그 채널을 단일 채널로 집계하는 데 사용됩니다. 스택 구축에 대한 자세한 내용은 [아래 문서](#건물-로그-스택)를 참조하세요.

<a name="available-channel-drivers"></a>
### Available Channel Drivers

각 로그 채널은 '드라이버'에 의해 구동됩니다. 드라이버는 로그 메시지가 실제로 기록되는 방법과 위치를 결정합니다. 다음 로그 채널 드라이버는 모든 Laravel 애플리케이션에서 사용할 수 있습니다. 대부분의 드라이버에 대한 항목은 애플리케이션의 `config/logging.php` 구성 파일에 이미 존재하므로 이 파일을 검토하여 내용을 숙지하세요:

<div class="overflow-auto">

| 이름 | 설명 |
| ------------ | -------------------------------------------------------------------- |
| `custom` | 지정된 팩토리를 호출하여 채널을 생성하는 드라이버입니다.         |
| 매일` | 매일 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버입니다.    |
| `errorlog` | `ErrorLogHandler` 기반 Monolog 드라이버.                           |
| `monolog` | 지원되는 모든 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버. |
| 페이퍼트레일` | `SyslogUdpHandler` 기반 Monolog 드라이버.                           |
| 단일` | 단일 파일 또는 경로 기반 로거 채널(`StreamHandler`).        |
| slack` | `SlackWebhookHandler` 기반 Monolog 드라이버.                        |
| `stack` | "다중 채널" 채널을 쉽게 생성하기 위한 래퍼.           |
| `syslog` | `SyslogHandler` 기반 Monolog 드라이버.                              |

</div>

> [!NOTE]
> 고급 채널 사용자 정의](#monolog-channel-customization) 문서를 확인하여 `monolog` 및 `custom` 드라이버에 대해 자세히 알아보세요.

<a name="configuring-the-channel-name"></a>
#### Configuring the Channel Name

기본적으로 Monolog는 현재 환경과 일치하는 '채널 이름'으로 인스턴스화됩니다(예: `production` 또는 `local`). 이 값을 변경하려면 채널의 구성에 `name` 옵션을 추가하면 됩니다:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-pre-requisites"></a>
### Channel Prerequisites

<a name="configuring-the-single-and-daily-channels"></a>
#### Configuring the Single and Daily Channels

단일` 및 `데일리` 채널에는 세 가지 선택적 구성 옵션이 있습니다: 버블`, `퍼미션`, `잠금`의 세 가지 옵션이 있습니다.

<div class="overflow-auto">

| 이름 | 설명 | 기본값 |
| ------------ | ----------------------------------------------------------------------------- | ------- |
| `버블` | 메시지가 처리된 후 다른 채널로 버블을 발생시킬지 여부를 나타냅니다. | `true` |
| `locking`` 로그 파일에 쓰기 전에 잠그기를 시도합니다.                            | `false` |
| `permission` | 로그 파일의 권한입니다.                                                   | `0644` |

</div>

또한 `매일` 채널에 대한 보존 정책은 `LOG_DAILY_DAYS` 환경 변수를 통해 구성하거나 `days` 구성 옵션을 설정하여 구성할 수 있습니다.

<div class="overflow-auto">

| 이름 | 설명 | 기본값 |
| ------ | ----------------------------------------------------------- | ------- |
| `days` | 일일 로그 파일을 보관할 일수입니다. | `14` |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Configuring the Papertrail Channel

페이퍼트레일` 채널에는 `host` 및 `port` 구성 옵션이 필요합니다. 이 옵션은 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수를 통해 정의할 수 있습니다. 이 값은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 얻을 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Configuring the Slack Channel

슬랙` 채널에는 `url` 구성 옵션이 필요합니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수를 통해 정의할 수 있습니다. 이 URL은 Slack 팀에 대해 구성한 [수신 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)의 URL과 일치해야 합니다.

기본적으로 Slack은 `critical` 수준 이상의 로그만 수신하지만 `LOG_LEVEL` 환경 변수를 사용하거나 Slack 로그 채널의 구성 배열 내에서 `level` 구성 옵션을 수정하여 이를 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### Logging Deprecation Warnings

PHP, Laravel 및 기타 라이브러리는 종종 일부 기능이 더 이상 사용되지 않으며 향후 버전에서 제거될 것임을 사용자에게 알립니다. 이러한 사용 중단 경고를 기록하려면 `LOG_DEPRECATIONS_CHANNEL` 환경 변수를 사용하거나 애플리케이션의 `config/logging.php` 구성 파일 내에서 선호하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 정의할 수 있습니다. 이 이름을 가진 로그 채널이 존재하면 항상 사용 중단을 기록하는 데 사용됩니다:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## Building Log Stacks

앞서 언급했듯이 `stack` 드라이버를 사용하면 편의를 위해 여러 채널을 단일 로그 채널로 결합할 수 있습니다. 로그 스택을 사용하는 방법을 설명하기 위해 프로덕션 애플리케이션에서 볼 수 있는 구성 예시를 살펴보겠습니다:

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

이 구성을 자세히 분석해 보겠습니다. 먼저, `stack` 채널이 `channels` 옵션을 통해 두 개의 다른 채널인 `syslog`와 `slack`을 집계한다는 점을 주목하세요. 따라서 메시지를 로깅할 때 이 두 채널 모두 메시지를 로깅할 기회를 갖게 됩니다. 그러나 아래에서 살펴보겠지만 이러한 채널이 실제로 메시지를 기록할지 여부는 메시지의 심각도/"수준"에 따라 결정될 수 있습니다.

<a name="log-levels"></a>
#### Log Levels

위 예의 `syslog` 및 `slack` 채널 구성에 있는 `level` 구성 옵션에 주목하세요. 이 옵션은 채널에서 메시지를 기록하기 위해 메시지의 최소 '수준'을 결정합니다. Laravel의 로깅 서비스를 구동하는 Monolog는 [RFC 5424 사양](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 제공합니다. 심각도에 따라 내림차순으로 로그 레벨은 다음과 같습니다: **긴급**, **경고**, **중요**, **오류**, **경고**, **공지**, **정보**, **디버그**입니다.

따라서 `debug` 메서드를 사용하여 메시지를 로깅한다고 가정해 보겠습니다:

```php
Log::debug('An informational message.');
```

이 구성에서 `syslog` 채널은 메시지를 시스템 로그에 기록하지만 오류 메시지가 `critical` 이상이 아니므로 Slack으로 전송되지 않습니다. 그러나 `긴급` 메시지를 기록하는 경우에는 `긴급` 수준이 두 채널의 최소 수준 임계값을 초과하므로 시스템 로그와 Slack 모두에 전송됩니다:

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## Writing Log Messages

로그` [facade](/docs/{{version}}/facades)를 사용하여 로그에 정보를 기록할 수 있습니다. 앞서 언급했듯이 로거는 [RFC 5424 사양](https://tools.ietf.org/html/rfc5424)에 정의된 8가지 로깅 수준을 제공합니다: **긴급**, **경고**, **중요**, **오류**, **경고**, **주의**, **정보**, **디버그**:

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

이러한 메서드 중 하나를 호출하여 해당 수준에 대한 메시지를 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에 구성된 기본 로그 채널에 기록됩니다:

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
### Contextual Information

컨텍스트 데이터 배열이 로그 메서드에 전달될 수 있습니다. 이 컨텍스트 데이터는 형식이 지정되고 로그 메시지와 함께 표시됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널의 모든 후속 로그 항목에 포함되어야 하는 일부 문맥 정보를 지정하고 싶을 때가 있습니다. 예를 들어 애플리케이션으로 들어오는 각 요청과 연관된 요청 ID를 기록할 수 있습니다. 이를 위해 `Log` 파사드의 `withContext` 메서드를 호출하면 됩니다:

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

모든_ 로깅 채널에서 컨텍스트 정보를 공유하려면 `Log::shareContext()` 메서드를 호출할 수 있습니다. 이 메서드는 생성된 모든 채널과 이후에 생성되는 모든 채널에 컨텍스트 정보를 제공합니다:

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
> 대기 중인 작업을 처리하는 동안 로그 컨텍스트를 공유해야 하는 경우, [작업 미들웨어](/docs/{{version}}/queues#job-middleware)를 활용할 수 있습니다.

<a name="특정 채널에 쓰기"></a>
### Writing to Specific Channels

애플리케이션의 기본 채널이 아닌 다른 채널에 메시지를 기록하고 싶을 때가 있습니다. 로그` 전면의 `채널` 메서드를 사용하여 구성 파일에 정의된 채널을 검색하고 해당 채널에 로깅할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널로 구성된 온디맨드 로깅 스택을 만들려면 `stack` 메서드를 사용할 수 있습니다:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### On-Demand Channels

애플리케이션의 `로깅` 구성 파일에 해당 구성이 없어도 런타임에 구성을 제공하여 온디맨드 채널을 생성할 수도 있습니다. 이를 위해 `로그` 파사드의 `build` 메서드에 구성 배열을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

온디맨드 로깅 스택에 온디맨드 채널을 포함할 수도 있습니다. 이는 `stack` 메서드에 전달된 배열에 온디맨드 채널 인스턴스를 포함하면 됩니다:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog Channel Customization

<a name="customizing-monolog-for-channels"></a>
### Customizing Monolog for Channels

기존 채널에 대해 Monolog가 구성되는 방식을 완전히 제어해야 하는 경우가 있습니다. 예를 들어, Laravel의 기본 제공 `단일` 채널에 대해 사용자 지정 Monolog `FormatterInterface` 구현을 구성하고 싶을 수 있습니다.

시작하려면 채널의 구성에 `tap` 배열을 정의하세요. 탭` 배열에는 Monolog 인스턴스가 생성된 후 사용자 정의(또는 "탭")할 수 있는 클래스 목록이 포함되어야 합니다. 이러한 클래스를 배치해야 하는 일반적인 위치는 없으므로 애플리케이션 내에 이러한 클래스를 포함할 디렉터리를 자유롭게 생성할 수 있습니다:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

채널에서 '탭' 옵션을 구성했으면 이제 Monolog 인스턴스를 사용자 지정할 클래스를 정의할 준비가 된 것입니다. 이 클래스에는 `__invoke`라는 단일 메서드만 필요하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 수신합니다. 일루미네이트\로그\로거` 인스턴스는 모든 메서드 호출을 기본 Monolog 인스턴스로 프록시합니다:

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
> 모든 "탭" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)에서 해결되므로 필요한 모든 생성자 종속성이 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Creating Monolog Handler Channels

Monolog에는 다양한 [사용 가능한 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있으며, Laravel에는 각 핸들러에 대한 기본 제공 채널이 포함되어 있지 않습니다. 경우에 따라 해당 Laravel 로그 드라이버가 없는 특정 Monolog 핸들러의 인스턴스일 뿐인 사용자 정의 채널을 만들고 싶을 수도 있습니다.  이러한 채널은 `monolog` 드라이버를 사용하여 쉽게 생성할 수 있습니다.

Monolog` 드라이버를 사용할 때 `handler` 구성 옵션을 사용하여 인스턴스화할 핸들러를 지정합니다. 선택적으로, 처리기에 필요한 생성자 매개변수는 `handler_with` 구성 옵션을 사용하여 지정할 수 있습니다:

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
#### Monolog Formatters

Monolog` 드라이버를 사용하는 경우, Monolog `LineFormatter`가 기본 포맷터로 사용됩니다. 그러나 `formatter` 및 `formatter_with` 구성 옵션을 사용하여 핸들러에 전달되는 포맷터 유형을 사용자 지정할 수 있습니다:

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

자체 포맷터를 제공할 수 있는 Monolog 핸들러를 사용하는 경우 `formatter` 구성 옵션의 값을 `default`로 설정할 수 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog Processors

Monolog는 메시지를 로깅하기 전에 메시지를 처리할 수도 있습니다. 자체 프로세서를 만들거나 Monolog에서 제공하는 [기존 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

'monolog` 드라이버에 대한 프로세서를 사용자 지정하려면 채널의 구성에 `processors` 구성 값을 추가하세요:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // Simple syntax...
        Monolog\Processor\MemoryUsageProcessor::class,

        // With options...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### Creating Custom Channels via Factories

Monolog의 인스턴스화 및 구성을 완전히 제어할 수 있는 완전히 사용자 정의 채널을 정의하려면 `config/logging.php` 구성 파일에 `custom` 드라이버 유형을 지정할 수 있습니다. 구성에는 Monolog 인스턴스를 생성하기 위해 호출될 팩토리 클래스의 이름이 포함된 `via` 옵션이 포함되어야 합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

Custom` 드라이버 채널을 구성했으면 이제 Monolog 인스턴스를 생성할 클래스를 정의할 준비가 된 것입니다. 이 클래스에는 Monolog 로거 인스턴스를 반환해야 하는 단일 `__invoke` 메서드만 필요합니다. 이 메서드는 채널 구성 배열을 유일한 인수로 받습니다:

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
## Tailing Log Messages Using Pail

애플리케이션의 로그를 실시간으로 추적해야 하는 경우가 종종 있습니다. 예를 들어 문제를 디버깅하거나 애플리케이션의 로그에서 특정 유형의 오류를 모니터링할 때입니다.

Laravel Pail은 명령줄에서 직접 Laravel 애플리케이션의 로그 파일을 쉽게 살펴볼 수 있는 패키지입니다. 표준 `tail` 명령과 달리, Pail은 Sentry 또는 Flare를 포함한 모든 로그 드라이버와 함께 작동하도록 설계되었습니다. 또한 Pail은 원하는 것을 빠르게 찾을 수 있도록 유용한 필터 세트를 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### Installation

> [!WARNING]
> 라라벨 페일에는 [PHP 8.2+](https://php.net/releases/) 및 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장 프로그램이 필요합니다.

시작하려면 Composer 패키지 관리자를 사용하여 프로젝트에 Pail을 설치하세요:

```shell
composer require laravel/pail
```

<a name="pail-usage"></a>
### Usage

로그 테일링을 시작하려면 `pail` 명령을 실행합니다:

```shell
php artisan pail
```

출력의 상세도를 높이고 잘림(...)을 방지하려면 `-v` 옵션을 사용합니다:

```shell
php artisan pail -v
```

자세한 내용을 최대화하고 예외 스택 추적을 표시하려면 `-vv` 옵션을 사용합니다:

```shell
php artisan pail -vv
```

로그 추적을 중지하려면 언제든지 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### Filtering Logs

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

필터` 옵션을 사용하여 로그의 유형, 파일, 메시지, 스택 추적 콘텐츠별로 로그를 필터링할 수 있습니다:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지만 기준으로 로그를 필터링하려면 `--메시지` 옵션을 사용할 수 있습니다:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

로그 수준](#log-levels)을 기준으로 로그를 필터링하려면 `--level` 옵션을 사용할 수 있습니다:

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 작성된 로그만 표시하려면 `--사용자` 옵션에 사용자 ID를 제공하면 됩니다:

```shell
php artisan pail --user=1
```
