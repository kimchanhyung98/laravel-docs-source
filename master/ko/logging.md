# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 작성하기](#writing-to-specific-channels)
- [Monolog 채널 사용자화](#monolog-channel-customization)
    - [채널용 Monolog 사용자화하기](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성하기](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성하기](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 메시지 실시간 확인](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내에서 무슨 일이 일어나고 있는지 더 자세히 알 수 있도록, Laravel은 파일이나 시스템 오류 로그뿐만 아니라 Slack 같은 서비스에도 메시지를 기록하여 팀 전체에 알릴 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel 로깅은 "채널(channels)"에 기반합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 로그 파일을 단일 파일에 작성하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 기록될 수 있습니다.

내부적으로 Laravel은 다양한 강력한 로그 핸들러를 지원하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. Laravel은 이러한 핸들러 설정을 쉽게 구성할 수 있도록 해 줌으로써 애플리케이션의 로그 처리 방식을 자유롭게 맞춤화할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 위치합니다. 이 파일을 통해 애플리케이션의 로그 채널을 설정할 수 있으니, 사용 가능한 채널과 옵션을 꼼꼼히 확인해 보시기 바랍니다. 아래에서는 몇 가지 흔히 사용되는 옵션들을 살펴보겠습니다.

기본적으로 Laravel은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 로그 스택 구성에 관한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"로 동작합니다. 드라이버는 로그 메시지가 어디에 어떻게 기록될지를 결정합니다. Laravel 애플리케이션에서 다음과 같은 로그 채널 드라이버들이 기본 제공됩니다. 대부분의 드라이버는 이미 애플리케이션의 `config/logging.php` 설정 파일에 항목이 있으니 파일 내용을 꼭 확인해 보세요.

<div class="overflow-auto">

| 이름          | 설명                                                     |
| ------------ | -------------------------------------------------------- |
| `custom`     | 지정한 팩토리를 호출해 채널을 생성하는 드라이버입니다.       |
| `daily`      | 일별로 로그를 순환하는 `RotatingFileHandler` 기반 Monolog 드라이버입니다. |
| `errorlog`   | `ErrorLogHandler` 기반 Monolog 드라이버입니다.            |
| `monolog`    | 지원하는 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버입니다.  |
| `papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버입니다.            |
| `single`     | 단일 파일 또는 경로 기반 로거 채널(`StreamHandler`)입니다.  |
| `slack`      | `SlackWebhookHandler` 기반 Monolog 드라이버입니다.         |
| `stack`      | 여러 채널을 하나로 묶을 수 있게 돕는 래퍼 드라이버입니다.     |
| `syslog`     | `SyslogHandler` 기반 Monolog 드라이버입니다.              |

</div>

> [!NOTE]
> `monolog`과 `custom` 드라이버에 관한 자세한 내용은 [고급 채널 사용자화](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정하기

기본적으로 Monolog은 현재 환경(`production`, `local` 등) 이름과 일치하는 "채널 이름"으로 생성됩니다. 이 값을 변경하려면 채널 설정 배열에 `name` 옵션을 추가하면 됩니다:

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
#### single, daily 채널 설정

`single`과 `daily` 채널은 `bubble`, `permission`, `locking` 세 가지 선택적 설정이 있습니다.

<div class="overflow-auto">

| 이름         | 설명                                                           | 기본값  |
| ------------ | -------------------------------------------------------------- | ------- |
| `bubble`     | 메시지가 처리된 후 다른 채널로 전달할지 여부 (true면 전달)         | `true`  |
| `locking`    | 로그 파일 쓰기 전 잠금 시도 여부                                 | `false` |
| `permission` | 로그 파일의 퍼미션(권한)                                         | `0644`  |

</div>

또한, `daily` 채널의 로그 보유 기간은 `LOG_DAILY_DAYS` 환경변수나 `days` 설정을 통해 지정할 수 있습니다.

<div class="overflow-auto">

| 이름    | 설명                                  | 기본값  |
| ------- | ------------------------------------- | ------- |
| `days`  | 일별 로그 파일을 보관할 일 수 (보존 기간) | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정이 필요하며, 각각 `PAPERTRAIL_URL`과 `PAPERTRAIL_PORT` 환경변수로 지정할 수 있습니다. 해당 값은 [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### slack 채널 설정

`slack` 채널은 `url` 설정이 필요하며, `LOG_SLACK_WEBHOOK_URL` 환경변수로 정의할 수 있습니다. 이 URL은 Slack 팀을 위해 구성한 [인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)의 URL이어야 합니다.

기본적으로 Slack은 `critical` 레벨 이상 로그만 수신하지만, `LOG_LEVEL` 환경변수 또는 Slack 채널 설정 배열의 `level` 옵션으로 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel 및 다른 라이브러리들은 종종 기능이 언제 사용 중단(deprecated)되어 이후 버전에서 제거될 것임을 알립니다. 이러한 사용 중단 경고를 로그에 남기려면, `LOG_DEPRECATIONS_CHANNEL` 환경변수나 `config/logging.php` 설정 파일 내에 원하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 정의해도 됩니다. 이 채널이 존재하면 항상 사용 중단 경고 로그에 사용됩니다:

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

앞서 언급했듯이, `stack` 드라이버는 여러 채널을 하나로 묶어 편리하게 사용할 수 있도록 해줍니다. 제작 환경에서 볼 수 있는 예시 설정을 통해 로그 스택 사용법을 살펴보겠습니다:

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

이 설정을 분석해 보면, 먼저 `stack` 채널이 두 개의 채널(`syslog`, `slack`)을 `channels` 옵션으로 묶고 있습니다. 따라서 로그 메시지를 기록할 때 두 채널 모두 메시지를 기록할 기회를 갖게 됩니다. 다만, 메시지의 심각도(레벨)에 따라 실제 기록 여부는 달라질 수 있습니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 채널 설정에 존재하는 `level` 옵션은 각 채널이 로그를 기록하기 위해 필요한 최소 "레벨"을 결정합니다. Laravel 로깅 서비스를 구동하는 Monolog은 [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 지원합니다. 심각도 순서(높은 순서부터)는 다음과 같습니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

예를 들어, `debug` 레벨로 로그 메시지를 남긴다고 가정해 보겠습니다:

```php
Log::debug('An informational message.');
```

위 설정에 따르면 `syslog` 채널은 이 메시지를 시스템 로그에 기록하지만, `slack` 채널은 `critical` 이상 메시지만 받으므로 전송하지 않습니다. 반면, `emergency` 레벨 메시지를 기록하면 두 채널 모두 메시지를 로그에 남깁니다:

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

`Log` [파사드](/docs/master/facades)를 사용하여 로그에 정보를 기록할 수 있습니다. 앞서 언급한대로, 다음 8개의 로그 레벨에 대한 메서드를 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**:

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

이 메서드들 중 어떤 것이든 호출하여 해당 레벨에 맞는 로그 메시지를 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에서 정의된 기본 로그 채널에 작성됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자 프로필을 보여줍니다.
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

로그 메서드에 컨텍스트 데이터 배열을 전달할 수 있습니다. 이 컨텍스트 정보는 로그 메시지와 함께 형식화되어 출력됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

가끔은 특정 채널에서 이후의 모든 로그에 포함되어야 할 컨텍스트 정보를 지정하고 싶을 수도 있습니다. 예를 들어, 애플리케이션으로 들어오는 각 요청에 연관된 요청 ID를 로그에 포함시키고 싶을 때가 그렇습니다. 이럴 경우 `Log` 파사드의 `withContext` 메서드를 호출하면 됩니다:

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
     * 들어오는 요청 처리.
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

만약 모든 로깅 채널에 공통의 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 호출할 수 있습니다. 이 메서드는 이미 생성된 모든 채널과 이후 생성될 채널 모두에 컨텍스트 정보를 제공합니다:

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
     * 들어오는 요청 처리.
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
> 큐에 할당된 작업 내에서 로그 컨텍스트를 공유해야 할 경우, [작업 미들웨어](/docs/master/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 작성하기

때때로 기본 로그 채널이 아닌 다른 채널에 메시지를 기록하고 싶을 수 있습니다. 이럴 때는 `Log` 파사드의 `channel` 메서드를 사용해 설정 파일에 정의된 임의의 채널을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 묶은 임시 로그 스택을 만들고 싶다면 `stack` 메서드를 사용해 배열로 전달할 수 있습니다:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드 채널

로그 설정에 미리 등록하지 않고, 런타임 동적으로 채널 설정을 전달해 온디맨드(임시) 로그 채널을 생성할 수도 있습니다. 이때 `Log` 파사드의 `build` 메서드에 설정 배열을 넘기면 됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

또한, 생성한 온디맨드 채널을 다른 채널과 함께 임시 로그 스택에 포함할 수도 있습니다:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog 채널 사용자화

<a name="customizing-monolog-for-channels"></a>
### 채널용 Monolog 사용자화하기

기존 채널에 대해 Monolog 설정을 완전히 제어하고 싶을 경우가 있습니다. 예를 들어 Laravel 내장 `single` 채널에 대해 사용자화한 Monolog `FormatterInterface` 구현을 할 수 있습니다.

이 경우, 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열에는 Monolog 인스턴스가 생성된 이후에 이를 조작할 수 있는 클래스 이름 목록을 담습니다. 해당 클래스들은 프로젝트 내 원하는 위치에 자유롭게 생성할 수 있습니다:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

이제 `tap`에 등록한 클래스의 본체를 다음처럼 작성합니다. 이 클래스는 단 하나의 메서드 `__invoke`만 필요하며, `Illuminate\Log\Logger` 인스턴스를 받아 메서드 호출을 통해 내부 Monolog 인스턴스에 접근할 수 있습니다:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 주어진 로거 인스턴스를 사용자화합니다.
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
> 모든 `tap` 클래스는 [서비스 컨테이너](/docs/master/container)에 의해 자동으로 의존성 주입이 되므로, 필요에 따라 생성자 주입도 문제 없습니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성하기

Monolog은 [다양한 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 제공하지만, Laravel은 모든 핸들러에 대응하는 채널을 내장하고 있지 않습니다. 어떤 경우에는 Laravel 로그 드라이버로 제공하지 않는 특정 Monolog 핸들러 인스턴스를 커스텀 채널로 만들고 싶을 수 있습니다. 이럴 때 `monolog` 드라이버를 사용하면 쉽게 만들 수 있습니다.

`monolog` 드라이버를 사용할 때는 `handler` 설정에 생성할 핸들러 클래스를 지정하면 되고, 필요하다면 `handler_with` 옵션으로 핸들러 생성자 인수도 설정할 수 있습니다:

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

`monolog` 드라이버 사용 시, 기본 포매터는 Monolog의 `LineFormatter`입니다. 하지만 `formatter`와 `formatter_with` 옵션을 사용해 포매터 종류와 설정을 변경할 수 있습니다:

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

자체 포매터를 제공하는 Monolog 핸들러를 사용하는 경우 `formatter` 설정 값을 `default`로 할 수도 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog은 로그 기록 전에 메시지를 가공하는 프로세서를 지원합니다. 직접 프로세서를 만들거나 Monolog이 제공하는 [기존 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

`monolog` 드라이버 채널의 프로세서를 지정하려면 `processors` 설정 배열에 프로세서 클래스를 나열하세요:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 표기법
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션이 필요한 경우
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리로 커스텀 채널 생성하기

Monolog 인스턴스 생성과 설정을 완전히 직접 제어하고 싶다면 `config/logging.php` 내 채널 설정에 `custom` 드라이버를 지정할 수 있습니다. 이때 `via` 옵션에 Monolog 인스턴스를 반환하는 팩토리 클래스명을 명시해야 합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

이제 `custom` 드라이버용 팩토리 클래스는 단일 `__invoke` 메서드를 포함해야 하며, 이 메서드는 Monolog 로거 인스턴스를 반환해야 합니다. 메서드는 채널 설정 배열을 매개변수로 받습니다:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * 커스텀 Monolog 인스턴스를 생성합니다.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Pail을 사용한 로그 메시지 실시간 확인

애플리케이션 로그를 실시간으로 확인해야 할 때가 많습니다. 예를 들면 문제를 디버깅하거나 특정 오류 유형을 모니터링할 때입니다.

Laravel Pail은 Laravel 애플리케이션의 로그 파일을 명령 줄에서 쉽게 실시간 조회할 수 있게 하는 패키지입니다. 기본 `tail` 명령과 달리, Pail은 Sentry나 Flare 같은 모든 로그 드라이버와도 작동하도록 설계되었으며, 유용한 필터링 기능도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PHP 8.2 이상](https://php.net/releases/)과 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장 모듈을 필요로 합니다.

프로젝트에 Pail을 설치하려면 Composer를 사용하세요:

```shell
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 실시간 조회를 시작하려면 `pail` 명령을 실행하세요:

```shell
php artisan pail
```

출력의 길이 제한(…)을 피하고 상세 출력을 원하면 `-v` 옵션을 붙입니다:

```shell
php artisan pail -v
```

예외 스택 트레이스를 표시하며 최대한 상세하게 보려면 `-vv` 옵션을 사용합니다:

```shell
php artisan pail -vv
```

로그 조회를 중단하려면 언제든 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션은 로그 타입, 파일, 메시지, 스택 트레이스 내용으로 로그를 필터링할 수 있습니다:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 내용만으로 로그를 필터링할 때는 `--message` 옵션을 사용하세요:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

[로그 레벨](#log-levels)로 로그를 필터링하려면 `--level` 옵션을 쓸 수 있습니다:

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 표시하려면 사용자 ID를 `--user` 옵션으로 전달하세요:

```shell
php artisan pail --user=1
```