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

<a name="introduction"></a>
## Introduction

애플리케이션 내에서 무슨 일이 일어나고 있는지 더 잘 파악할 수 있도록, Laravel은 robust한 로깅 서비스를 제공하여 메시지를 파일, 시스템 에러 로그, 심지어 Slack에도 기록하여 팀 전체에 알릴 수 있게 합니다.

Laravel의 로깅은 "채널(channels)"을 기반으로 합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 로그 파일을 단일 로그 파일에 기록하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널로 기록될 수 있습니다.



내부적으로, Laravel은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하며, 이는 강력한 로그 핸들러들을 다양하게 지원합니다. Laravel은 이러한 핸들러를 간편하게 설정할 수 있도록 하여, 애플리케이션의 로그 처리를 커스터마이징하기 위해 혼합해 사용할 수 있게 합니다.
## Configuration



<a name="configuration"></a>

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 있습니다. 이 파일에서는 애플리케이션의 로그 채널을 설정할 수 있으므로, 사용 가능한 각 채널과 그 옵션을 꼭 확인하세요. 아래에서 몇 가지 일반적인 옵션을 살펴보겠습니다.
### Available Channel Drivers



<div class="overflow-auto">

기본적으로, Laravel은 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나의 채널로 통합하는 데 사용됩니다. 스택을 구성하는 방법에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
각 로그 채널은 "driver"에 의해 구동됩니다. driver는 로그 메시지가 실제로 어떻게, 어디에 기록되는지를 결정합니다. 다음의 로그 채널 드라이버들은 모든 Laravel 애플리케이션에서 사용할 수 있습니다. 대부분의 드라이버에 대한 항목은 이미 애플리케이션의 `config/logging.php` 설정 파일에 있으므로, 이 파일을 확인하여 해당 내용을 숙지하시기 바랍니다:

| Name         | Description                                                          |
| ------------ | -------------------------------------------------------------------- |
| `custom`     | 지정된 팩토리를 호출하여 채널을 생성하는 드라이버.                  |
| `daily`      | 매일 회전되는 `RotatingFileHandler` 기반의 Monolog 드라이버.         |
| `errorlog`   | `ErrorLogHandler` 기반의 Monolog 드라이버.                           |
| `monolog`    | 지원되는 모든 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버. |

</div>

> [!NOTE]
| `papertrail` | `SyslogUdpHandler` 기반의 Monolog 드라이버.                          |

| `single`     | 단일 파일 또는 경로 기반의 로거 채널 (`StreamHandler`).              |
#### Configuring the Channel Name

| `slack`      | `SlackWebhookHandler` 기반의 Monolog 드라이버.                       |

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

| `stack`      | "멀티 채널" 채널을 만들 수 있도록 하는 래퍼.                        |
### Channel Prerequisites

| `syslog`     | `SyslogHandler` 기반의 Monolog 드라이버.                             |
#### Configuring the Single and Daily Channels



<div class="overflow-auto">

> [advanced channel customization](#monolog-channel-customization)에 대한 문서를 확인하여 `monolog` 및 `custom` 드라이버에 대해 더 알아보세요.

<a name="configuring-the-channel-name"></a>
기본적으로, Monolog는 현재 환경(`production` 또는 `local` 등)과 일치하는 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면, 채널 설정에 `name` 옵션을 추가하면 됩니다:


</div>

<a name="channel-prerequisites"></a>

<div class="overflow-auto">

<a name="configuring-the-single-and-daily-channels"></a>
`single` 및 `daily` 채널에는 `bubble`, `permission`, `locking` 세 가지 선택적 설정 옵션이 있습니다.


</div>

| Name         | Description                                                                   | Default |
#### Configuring the Papertrail Channel

| ------------ | ----------------------------------------------------------------------------- | ------- |

| `bubble`     | 메시지가 처리된 후 다른 채널로 전달될지 여부를 나타냅니다.                   | `true`  |
#### Configuring the Slack Channel

| `locking`    | 기록하기 전에 로그 파일을 잠그려고 시도합니다.                               | `false` |

| `permission` | 로그 파일의 권한을 설정합니다.                                                | `0644`  |

Additionally, the retention policy for the `daily` channel can be configured via the `LOG_DAILY_DAYS` environment variable or by setting the `days` configuration option.  
### Logging Deprecation Warnings

| Name   | Description                                                 | Default |

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

| ------ | ----------------------------------------------------------- | ------- |

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

| `days` | 매일 로그 파일을 얼마나 오래(일 수) 보관할지 설정합니다.                 | `14`    |
## Building Log Stacks



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

<a name="configuring-the-papertrail-channel"></a>

The `papertrail` channel requires `host` and `port` configuration options. These may be defined via the `PAPERTRAIL_URL` and `PAPERTRAIL_PORT` environment variables. You can obtain these values from [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app).
#### Log Levels



<a name="configuring-the-slack-channel"></a>

```php
Log::debug('An informational message.');
```

The `slack` channel requires a `url` configuration option. This value may be defined via the `LOG_SLACK_WEBHOOK_URL` environment variable. This URL should match a URL for an [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) that you have configured for your Slack team.  

```php
Log::emergency('The system is down!');
```

By default, Slack will only receive logs at the `critical` level and above; however, you can adjust this using the `LOG_LEVEL` environment variable or by modifying the `level` configuration option within your Slack log channel's configuration array.
## Writing Log Messages



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

<a name="logging-deprecation-warnings"></a>

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

PHP, Laravel, and other libraries often notify their users that some of their features have been deprecated and will be removed in a future version. If you would like to log these deprecation warnings, you may specify your preferred `deprecations` log channel using the `LOG_DEPRECATIONS_CHANNEL` environment variable, or within your application's `config/logging.php` configuration file:  
### Contextual Information

Or, you may define a log channel named `deprecations`. If a log channel with this name exists, it will always be used to log deprecations:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```



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

<a name="building-log-stacks"></a>

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
As mentioned previously, the `stack` driver allows you to combine multiple channels into a single log channel for convenience. To illustrate how to use log stacks, let's take a look at an example configuration that you might see in a production application:  

Let's dissect this configuration. First, notice our `stack` channel aggregates two other channels via its `channels` option: `syslog` and `slack`. So, when logging messages, both of these channels will have the opportunity to log the message. However, as we will see below, whether these channels actually log the message may be determined by the message's severity / "level".
### Writing to Specific Channels



```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

<a name="log-levels"></a>

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

Take note of the `level` configuration option present on the `syslog` and `slack` channel configurations in the example above. This option determines the minimum "level" a message must be in order to be logged by the channel. Monolog, which powers Laravel's logging services, offers all of the log levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424). In descending order of severity, these log levels are: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, and **debug**.
#### On-Demand Channels



```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

So, imagine we log a message using the `debug` method:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

Given our configuration, the `syslog` channel will write the message to the system log; however, since the error message is not `critical` or above, it will not be sent to Slack. However, if we log an `emergency` message, it will be sent to both the system log and Slack since the `emergency` level is above our minimum level threshold for both channels:
## Monolog Channel Customization


### Customizing Monolog for Channels

<a name="writing-log-messages"></a>

You may write information to the logs using the `Log` [facade](/docs/{{version}}/facades). As previously mentioned, the logger provides the eight logging levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

다음은 원문을 ko로 번역한 내용입니다(코드, 링크, 마크다운 구문은 그대로 유지):

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


You may call any of these methods to log a message for the corresponding level. By default, the message will be written to the default log channel as configured by your `logging` configuration file:
### Creating Monolog Handler Channels

<a name="contextual-information"></a>

로그 메서드에 컨텍스트 데이터 배열을 전달할 수 있습니다. 이 컨텍스트 데이터는 로그 메시지와 함께 포맷팅되어 표시됩니다:

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

가끔, 이후에 기록되는 모든 로그 항목에 포함되어야 하는 컨텍스트 정보를 지정하고 싶을 때가 있을 수 있습니다. 예를 들어, 애플리케이션으로 들어오는 각 요청과 연관된 요청 ID를 로깅하고 싶을 수 있습니다. 이를 위해서는 `Log` 퍼사드의 `withContext` 메서드를 호출하면 됩니다:
#### Monolog Formatters

모든 로깅 채널에 걸쳐 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 호출할 수 있습니다. 이 메서드는 이미 생성된 모든 채널 및 이후에 생성되는 모든 채널에 컨텍스트 정보를 제공합니다:

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

> 큐에 적재된 작업을 처리하면서 로그 컨텍스트를 공유해야 할 경우, [job middleware](/docs/{{version}}/queues#job-middleware)를 활용할 수 있습니다.

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```


#### Monolog Processors

<a name="writing-to-specific-channels"></a>

때로는 애플리케이션의 기본 채널이 아닌 다른 채널에 메시지를 기록하고자 할 수 있습니다. 이 경우 `Log` 퍼사드의 `channel` 메서드를 사용하여 구성 파일에 정의된 어떤 채널이든 가져와서 로그를 기록할 수 있습니다:

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

여러 채널로 구성된 온디맨드 로깅 스택을 생성하고 싶다면, `stack` 메서드를 사용할 수 있습니다:
### Creating Custom Channels via Factories



```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

<a name="on-demand-channels"></a>

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

애플리케이션의 `logging` 구성 파일에 없는 설정을 런타임에 제공함으로써 온디맨드 채널을 생성할 수도 있습니다. 이를 위해 `Log` 퍼사드의 `build` 메서드에 구성 배열을 전달하면 됩니다:
## Tailing Log Messages Using Pail

온디맨드 로깅 스택에 온디맨드 채널을 포함하고 싶을 수도 있습니다. 이를 위해서는 온디맨드 채널 인스턴스를 `stack` 메서드에 전달되는 배열에 포함하면 됩니다:



<img src="https://laravel.com/img/docs/pail-example.png">

<a name="monolog-channel-customization"></a>
### Installation

> [!WARNING]
<a name="customizing-monolog-for-channels"></a>

기존 채널에 대해 Monolog의 구성 방식을 완전히 제어해야 하는 경우가 있을 수 있습니다. 예를 들어, Laravel에 내장된 `single` 채널에 대해 사용자 정의 Monolog `FormatterInterface` 구현을 설정하고 싶을 수 있습니다.

```shell
composer require laravel/pail
```

먼저, 채널의 구성에서 `tap` 배열을 정의합니다. `tap` 배열은 Monolog 인스턴스가 생성된 후 이를 커스터마이즈(또는 '탭')할 수 있는 클래스들의 목록을 포함해야 합니다. 이 클래스들이 위치해야 할 전통적인 디렉터리는 없으므로, 애플리케이션 내에서 새로운 디렉터리를 만들어 자유롭게 저장할 수 있습니다:
### Usage

채널에서 `tap` 옵션을 설정한 뒤, 이제 Monolog 인스턴스를 커스터마이즈할 클래스를 정의할 수 있습니다. 이 클래스에는 단 하나의 메서드, 즉 `__invoke`만 필요하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 전달받습니다. `Illuminate\Log\Logger` 인스턴스는 내부의 Monolog 인스턴스에 모든 메서드 호출을 프록싱합니다:

```shell
php artisan pail
```

> 모든 'tap' 클래스는 [service container](/docs/{{version}}/container)에 의해 해석되므로, 필요한 생성자 종속성이 자동으로 주입됩니다.

```shell
php artisan pail -v
```



```shell
php artisan pail -vv
```

<a name="creating-monolog-handler-channels"></a>

Monolog에는 [사용 가능한 다양한 핸들러들](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)이 있으며, Laravel은 각각에 대한 빌트인 채널을 제공하지 않습니다. 경우에 따라, 특정 Monolog 핸들러에 해당하는 별도의 Laravel 로그 드라이버가 없을 때, 그 인스턴스만을 사용하는 커스텀 채널을 만들고 싶을 수 있습니다. 이러한 채널은 `monolog` 드라이버를 사용하여 손쉽게 생성할 수 있습니다.
### Filtering Logs

`monolog` 드라이버를 사용할 때, `handler` 구성 옵션을 통해 어떤 핸들러가 인스턴스화될지를 지정합니다. 선택적으로, 핸들러가 필요로 하는 생성자 파라미터는 `handler_with` 구성 옵션을 사용하여 지정할 수 있습니다:
#### `--filter`



```shell
php artisan pail --filter="QueryException"
```

<a name="monolog-formatters"></a>
#### `--message`

`monolog` 드라이버를 사용할 때, 기본 포매터로 Monolog `LineFormatter`가 사용됩니다. 그러나 `formatter` 및 `formatter_with` 구성 옵션을 사용하여 핸들러에 전달되는 포매터 유형을 커스터마이징할 수 있습니다:

```shell
php artisan pail --message="User created"
```


#### `--level`

Monolog 핸들러가 자체 포매터를 제공할 수 있는 경우, `formatter` 구성 옵션의 값을 `default`로 설정할 수 있습니다:

```shell
php artisan pail --level=error
```


#### `--user`

<a name="monolog-processors"></a>

```shell
php artisan pail --user=1
```
