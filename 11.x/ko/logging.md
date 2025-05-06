# 로깅

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 요구 사항](#channel-prerequisites)
    - [폐지 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보 제공](#contextual-information)
    - [특정 채널로 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널에 대한 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 만들기](#creating-monolog-handler-channels)
    - [팩토리로 커스텀 채널 만들기](#creating-custom-channels-via-factories)
- [Pail을 이용한 로그 메시지 스트리밍](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션에서 무슨 일이 일어나고 있는지 더 잘 이해할 수 있도록, Laravel은 강력한 로깅 서비스를 제공합니다. 이를 통해 파일, 시스템 에러 로그, 심지어 Slack까지 다양한 위치에 로그 메시지를 기록할 수 있으며, 팀 전체에게 알림을 보낼 수도 있습니다.

Laravel의 로깅은 "채널"을 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방법을 나타냅니다. 예를 들어, `single` 채널은 단일 로그 파일에 기록을 남기고, `slack` 채널은 Slack으로 로그 메시지를 전송합니다. 메시지의 심각도(severity)에 따라 여러 채널에 동시에 기록될 수 있습니다.

Laravel은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 내부적으로 활용하며, 다양한 강력한 로그 핸들러를 지원합니다. Laravel에서는 이러한 핸들러를 손쉽게 설정할 수 있도록 하여, 애플리케이션의 로그 처리 방식을 자유롭게 커스터마이즈할 수 있도록 해줍니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정은 `config/logging.php` 설정 파일에 있습니다. 이 파일을 통해 로그 채널을 구성할 수 있으므로, 제공되는 다양한 채널과 그 옵션을 잘 살펴보시길 바랍니다. 아래에서는 몇 가지 일반적으로 사용하는 옵션을 살펴봅니다.

기본적으로, Laravel은 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나의 채널로 집계하는 역할을 합니다. 스택 구성에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 동작합니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록될지 결정합니다. 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버는 아래와 같습니다. 대부분의 드라이버가 이미 애플리케이션의 `config/logging.php` 파일에 정의되어 있으니 직접 확인해 보시기 바랍니다:

<div class="overflow-auto">

| 이름          | 설명                                                                       |
| ------------- | -------------------------------------------------------------------------- |
| `custom`      | 지정된 팩토리를 호출하여 채널을 생성하는 드라이버                          |
| `daily`       | 일 단위로 회전(rotate)하는 `RotatingFileHandler` 기반 Monolog 드라이버     |
| `errorlog`    | 시스템 에러 로그로 기록하는 `ErrorLogHandler` 기반 Monolog 드라이버        |
| `monolog`     | 모든 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버               |
| `papertrail`  | `SyslogUdpHandler` 기반 Monolog 드라이버                                   |
| `single`      | 단일 파일 또는 경로 기반의 로거 채널 (`StreamHandler`)                   |
| `slack`       | `SlackWebhookHandler` 기반 Monolog 드라이버                                |
| `stack`       | "다중 채널"을 만들기 위한 래퍼 드라이버                                   |
| `syslog`      | `SyslogHandler` 기반 Monolog 드라이버                                      |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징 문서](#monolog-channel-customization)를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경(예: `production`, `local`)에 맞는 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면, 채널의 설정에 `name` 옵션을 추가하면 됩니다:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 사전 요구 사항

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널은 `bubble`, `permission`, `locking`의 세 가지 옵션을 추가로 설정할 수 있습니다.

<div class="overflow-auto">

| 이름          | 설명                                                        | 기본값  |
| ------------- | ----------------------------------------------------------- | ------ |
| `bubble`      | 메시지 처리 후에도 상위 채널로 전파할지 여부를 지정함        | `true` |
| `locking`     | 기록 전에 로그 파일을 잠글지 시도                           | `false`|
| `permission`  | 로그 파일의 권한                                            | `0644` |

</div>

또한, `daily` 채널의 보존 기간은 `LOG_DAILY_DAYS` 환경 변수 또는 설정 파일의 `days` 옵션으로 지정할 수 있습니다.

<div class="overflow-auto">

| 이름   | 설명                                     | 기본값 |
| ------ | ---------------------------------------- | ------ |
| `days` | 일일 로그 파일이 보관되는 일수            | `14`   |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 반드시 `host`와 `port` 옵션이 필요합니다. 이 값들은 `PAPERTRAIL_URL`, `PAPERTRAIL_PORT` 환경 변수로 정의할 수 있으며, [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 발급받을 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 설정이 필수입니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 정의할 수 있습니다. 이 URL은 Slack에서 [인커밍 웹후크](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)로 발급받은 URL이어야 합니다.

기본적으로 Slack에는 `critical` 이상 레벨의 로그만 전송됩니다. 하지만 환경 변수 `LOG_LEVEL`이나 Slack 로그 채널 설정의 `level` 옵션을 조정하여 변경할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 폐지(deprecation) 경고 로깅

PHP, Laravel, 그리고 기타 라이브러리들은 특정 기능이 더 이상 지원되지 않고 곧 제거될 예정임을 종종 경고합니다. 이런 폐지 경고를 로그로 남기고 싶다면, `LOG_DEPRECATIONS_CHANNEL` 환경 변수나 `config/logging.php` 설정 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 정의할 수도 있습니다. 이 경우, 해당 이름의 로그 채널이 존재한다면 항상 폐지 경고를 기록하는 데 사용됩니다:

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

앞서 언급했듯이, `stack` 드라이버는 여러 개의 로그 채널을 하나의 채널로 합쳐서 사용하는 것을 가능하게 해줍니다. 실제 프로덕션 환경에서 볼 수 있는 예시 설정을 살펴보겠습니다:

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'],
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

해당 설정을 살펴보면, `stack` 채널의 `channels` 옵션에 `syslog`와 `slack`이 배열로 들어가 있습니다. 따라서, 로그 메시지를 기록할 때 두 채널 모두에 메시지가 전달됩니다. 그러나 실제로 각 채널이 로그를 남기는지 여부는 메시지의 심각도(레벨)에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 채널 설정에 존재하는 `level` 옵션을 주목하세요. 이 옵션은 해당 채널이 기록할 최소 "레벨"을 결정합니다. Laravel의 로그는 Monolog가 제공하며, 이는 [RFC 5424 스펙](https://tools.ietf.org/html/rfc5424)에 정의된 로그 레벨 전부를 지원합니다. 심각도 순서대로: **emergency(위급)**, **alert(경보)**, **critical(치명적)**, **error(에러)**, **warning(경고)**, **notice(공지)**, **info(정보)**, **debug(디버그)** 가 있습니다.

예를 들어, 아래와 같은 메시지를 `debug` 메서드로 기록한다고 가정합시다.

```php
Log::debug('An informational message.');
```

해당 설정에서는 `syslog` 채널이 이 메시지를 시스템 로그에 기록하지만, `critical` 이상이 아니므로 Slack에는 전송되지 않습니다. 반면 `emergency` 메시지는 두 채널 모두에 기록됩니다:

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

`Log` [파사드](/docs/{{version}}/facades)를 통해 로그에 정보를 남길 수 있습니다. 앞서 언급했듯이, 로거는 [RFC 5424 스펙](https://tools.ietf.org/html/rfc5424)에 정의된 8개의 로그 레벨을 모두 지원합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**

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

이 중 아무 메서드나 호출하여 해당 레벨에 메시지를 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에 지정된 기본 로그 채널에 기록됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필 표시
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
### 컨텍스트 정보 제공

로그 메서드에는 컨텍스트 데이터를 배열로 전달할 수 있습니다. 이 정보는 로그 메시지와 함께 포매팅되어 표시됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널의 이후 모든 로그 항목에 포함될 컨텍스트 정보를 지정하고 싶을 때도 있습니다. 예를 들어, 각 요청마다 요청 ID를 기록하고 싶다면, `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다:

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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 기존 및 추가적으로 생성되는 모든 채널에 컨텍스트 정보가 전달됩니다:

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
> 큐 작업 처리 중에 로그 컨텍스트를 공유하려면 [잡 미들웨어](/docs/{{version}}/queues#job-middleware)를 사용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널로 기록하기

기본 채널이 아닌 다른 채널에 메시지를 기록하고 싶을 때도 있습니다. 이럴 때는 `Log` 파사드의 `channel` 메서드를 사용해 구성 파일에 정의된 채널로 접근하여 로그를 작성할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널로 구성된 온디맨드 스택 로그가 필요하다면 `stack` 메서드를 사용할 수 있습니다:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드 채널

애플리케이션의 `logging` 설정 파일에 미리 정의하지 않은 채널도 런타임에 구성 배열을 전달하여 온디맨드로 만들 수 있습니다. `Log` 파사드의 `build` 메서드에 구성 배열을 전달하세요:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

온디맨드 채널 인스턴스를 스택 배열에도 포함시켜 온디맨드 로그 스택을 구성할 수 있습니다:

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
### 채널에 대한 Monolog 커스터마이징

기존 채널에서 Monolog의 동작을 완전히 제어해야 할 때가 있습니다. 예를 들어 Laravel 내장 `single` 채널에 대한 커스텀 Monolog `FormatterInterface` 구현체를 사용하고 싶을 때입니다.

먼저, 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열에는 Monolog 인스턴스가 생성된 후 커스터마이징("tap in")할 수 있는 클래스들의 리스트를 넣습니다. 이 클래스들은 애플리케이션 내의 자유로운 위치에 둘 수 있습니다.

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

`tap` 옵션을 설정했다면, 이제 실제 Monolog 인스턴스를 커스터마이징하는 클래스를 만듭니다. 이 클래스에는 `Illuminate\Log\Logger` 인스턴스를 인자로 받는 `__invoke` 메소드만 필요합니다. `Illuminate\Log\Logger`는 모든 메서드 호출을 내부 Monolog 인스턴스로 위임합니다.

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 주어진 로거 인스턴스 커스터마이징
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
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)로 해결되므로, 생성자 의존성이 자동 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 만들기

Monolog는 [여러 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 제공합니다. 일부 핸들러는 Laravel에 내장되어 있지 않을 수 있습니다. 별도의 Laravel 드라이버 없이 특정 Monolog 핸들러 인스턴스만 가지고 커스텀 채널을 만들고 싶다면, `monolog` 드라이버를 사용하면 됩니다.

`monolog` 드라이버 사용 시, `handler` 옵션에 인스턴스화할 핸들러 클래스를 지정하고, 필요하다면 생성자 인자들을 `with` 옵션에 지정합니다:

```php
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```

<a name="monolog-formatters"></a>
#### Monolog 포매터

`monolog` 드라이버를 사용할 때는 기본적으로 Monolog의 `LineFormatter`가 사용됩니다. 하지만, `formatter`와 `formatter_with` 설정을 통해 포매터를 직접 지정할 수 있습니다:

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

Monolog 핸들러 자체에서 기본 포매터를 지원하는 경우, `formatter` 값을 `default`로 설정할 수 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog는 로그 메시지를 기록 전 가공할 수 있습니다. 직접 프로세서를 만들거나 [Monolog가 제공하는 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용해도 됩니다.

`monolog` 드라이버의 프로세서를 커스터마이즈하고 싶다면 `processors` 설정을 채널 설정에 추가하세요:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 문법
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션과 함께
        [
           'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
           'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 만들기

Monolog 인스턴스 생성 및 설정을 완전히 직접 제어하는 커스텀 채널을 정의하려면, `config/logging.php`의 채널 설정에서 `custom` 드라이버 타입을 사용하세요. 설정에는 Monolog 인스턴스를 만들 팩토리 클래스명을 `via` 옵션에 지정해야 합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

이제 `custom` 드라이버 채널에 대한 클래스를 만듭니다. 이 클래스는 반드시 Monolog 로거 인스턴스를 반환하는 `__invoke` 메서드를 하나 가지며, 해당 메서드는 채널 구성 배열 하나를 인자로 받습니다:

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
## Pail을 이용한 로그 메시지 스트리밍

애플리케이션의 로그를 실시간으로 스트리밍하고 싶을 때가 있습니다. 예를 들어, 문제를 디버깅하거나 특정 유형의 에러를 모니터링하는 경우입니다.

Laravel Pail은 터미널에서 Laravel 애플리케이션 로그 파일을 쉽게 탐색할 수 있게 해주는 패키지입니다. 표준 `tail` 명령과 달리, Pail은 Sentry, Flare 등 모든 로그 드라이버와 연동되도록 설계되었습니다. 또한 원하는 로그를 빠르게 찾을 수 있는 다양한 유용한 필터도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PHP 8.2 이상](https://php.net/releases/)과 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장이 필요합니다.

우선, Composer 패키지 매니저로 Pail을 프로젝트에 설치하세요:

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 스트리밍을 시작하려면 `pail` 명령어를 실행하세요:

```bash
php artisan pail
```

출력의 상세 수준을 높이고 잘림 현상(…)을 방지하려면 `-v` 옵션을 사용하세요:

```bash
php artisan pail -v
```

최상위 상세 출력 및 예외 스택 트레이스까지 표시하려면 `-vv` 옵션을 사용하세요:

```bash
php artisan pail -vv
```

로그 스트리밍을 중지하려면 언제든지 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션을 사용해 로그의 타입, 파일, 메시지, 스택 트레이스 내용을 기준으로 필터링할 수 있습니다:

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

오직 메시지 내용만 기준으로 필터링하려면 `--message` 옵션을 사용하세요:

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` 옵션을 이용해 [로그 레벨](#log-levels)별로 걸러낼 수 있습니다:

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 작성된 로그만 보고 싶을 때는 사용자 ID를 `--user` 옵션에 지정하세요:

```bash
php artisan pail --user=1
```
