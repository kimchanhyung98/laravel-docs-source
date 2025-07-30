# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 전제 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 작성하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 사용한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 메시지 실시간 확인](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션에서 발생하는 일을 더 잘 이해할 수 있도록, Laravel은 파일, 시스템 에러 로그, 심지어 Slack을 통해 팀 전체에 알림을 보낼 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel의 로깅은 "채널"을 기반으로 합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어 `single` 채널은 단일 로그 파일에 로그를 기록하고, `slack` 채널은 Slack으로 로그 메시지를 보냅니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

내부적으로 Laravel은 다양한 강력한 로그 핸들러를 지원하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. Laravel은 이 핸들러들을 쉽게 구성할 수 있도록 하여 필요에 따라 조합해 애플리케이션의 로그 처리를 맞춤 설정할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 포함되어 있습니다. 이 파일에서 애플리케이션의 로그 채널을 구성할 수 있으므로, 사용 가능한 채널과 각 옵션을 반드시 살펴보시기 바랍니다. 여기서는 몇 가지 일반적인 옵션을 살펴보겠습니다.

기본적으로, Laravel은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어줍니다. 스택 구성에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"를 기반으로 작동합니다. 드라이버는 로그 메시지가 실제로 어떻게 어디에 기록될지를 결정합니다. 다음 로그 채널 드라이버들은 모든 Laravel 애플리케이션에서 사용할 수 있습니다. 대부분의 드라이버 설정은 기본적으로 애플리케이션의 `config/logging.php` 설정 파일에 이미 포함되어 있으므로, 파일을 열어 내용을 숙지하시기 바랍니다:

<div class="overflow-auto">

| 이름         | 설명                                                                   |
| ------------ | -------------------------------------------------------------------- |
| `custom`     | 지정된 팩토리를 호출해 채널을 생성하는 드라이버입니다.               |
| `daily`      | 일별로 로그를 회전하는 Monolog 기반 `RotatingFileHandler` 드라이버입니다. |
| `errorlog`   | Monolog의 `ErrorLogHandler` 기반 드라이버입니다.                    |
| `monolog`    | Monolog 팩토리 드라이버로, 지원되는 아무 핸들러나 사용할 수 있습니다.    |
| `papertrail` | Monolog의 `SyslogUdpHandler` 기반 드라이버입니다.                   |
| `single`     | 단일 파일 혹은 경로 기반의 로거 채널 (`StreamHandler`)입니다.       |
| `slack`      | Monolog의 `SlackWebhookHandler` 기반 드라이버입니다.                 |
| `stack`      | 여러 채널을 묶어 다중 채널 로깅을 쉽게 하는 래퍼입니다.              |
| `syslog`     | Monolog의 `SyslogHandler` 기반 드라이버입니다.                      |

</div>

> [!NOTE]  
> `monolog` 및 `custom` 드라이버에 대해 더 자세히 알고 싶으면 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 구성하기

기본적으로 Monolog은 현재 환경 이름(`production`, `local` 등)과 일치하는 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하고 싶다면 채널 설정에 `name` 옵션을 추가할 수 있습니다:

```
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

`single`과 `daily` 채널은 선택적 구성 옵션으로 `bubble`, `permission`, 그리고 `locking`이 있습니다.

<div class="overflow-auto">

| 이름          | 설명                                                                    | 기본값   |
| ------------ | ----------------------------------------------------------------------- | ------- |
| `bubble`     | 메시지가 처리된 후 다른 채널에도 전파(bubble up)될지 여부입니다.          | `true`  |
| `locking`    | 로그 쓰기 전에 파일 락(lock)을 시도할지 여부입니다.                     | `false` |
| `permission` | 로그 파일에 적용할 파일 권한입니다.                                     | `0644`  |

</div>

또한, `daily` 채널의 보존 기간 정책은 `LOG_DAILY_DAYS` 환경 변수 또는 `days` 옵션으로 설정할 수 있습니다.

<div class="overflow-auto">

| 이름   | 설명                                              | 기본값 |
| ------ | -------------------------------------------------| ------- |
| `days` | 일별 로그 파일이 보존될 일수입니다.               | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정하기

`papertrail` 채널은 `host`와 `port` 옵션이 필요합니다. 이들은 보통 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수로 정의합니다. 값은 [Papertrail 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정하기

`slack` 채널은 `url` 옵션이 필요하며, 보통 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 정의됩니다. 이 URL은 Slack 팀에 설정된 [수신 웹훅(incoming webhook)](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 주소와 일치해야 합니다.

기본적으로 Slack 채널은 `critical` 이상 레벨의 로그만 수신하지만, `LOG_LEVEL` 환경 변수나 `level` 옵션을 수정하여 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel, 기타 라이브러리는 기능이 향후 버전에서 제거될 예정이라는 사용 중단(Deprecation) 경고를 자주 알립니다. 이런 경고를 로그에 기록하고 싶으면, `LOG_DEPRECATIONS_CHANNEL` 환경 변수나 `config/logging.php` 설정 파일에서 원하는 `deprecations` 채널을 지정할 수 있습니다:

```
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 정의할 수도 있습니다. 만약 이 이름의 로그 채널이 존재하면, 사용 중단 경고는 항상 이 채널을 통해 기록됩니다:

```
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구성

앞서 언급했듯, `stack` 드라이버는 여러 개의 채널을 하나의 로그 채널로 묶어서 편리하게 사용할 수 있게 해줍니다. 다음은 운영 환경에서 자주 사용되는 예시 설정입니다:

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

설정을 살펴보면, `stack` 채널은 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 합친 것을 확인할 수 있습니다. 따라서 로그 메시지가 기록될 때, 두 채널 모두 메시지를 기록할 기회를 갖게 됩니다. 하지만 다음에 설명하듯, 각 채널의 로그 기록 여부는 메시지 심각도(레벨)에 따라 다를 수 있습니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 채널 설정에 `level` 옵션이 있는 것을 주목하세요. 이 옵션은 해당 채널이 로그를 기록할 최소 심각도 레벨을 의미합니다. Laravel 로깅 서비스를 제공하는 Monolog은 [RFC 5424 사양](https://tools.ietf.org/html/rfc5424)에서 정의한 다음 8가지 로그 레벨을 지원합니다. 심각도 내림차순으로 나열하면: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

예를 들어, `Log::debug('An informational message.')` 메서드를 호출해서 `debug` 레벨의 메시지를 기록한다고 가정해 봅시다.

```
Log::debug('An informational message.');
```

설정된 대로라면 `syslog` 채널은 이 메시지를 시스템 로그에 기록하지만, Slack은 `critical` 이상만 수신하므로 이 `debug` 메시지는 Slack으로 전송되지 않습니다. 반면에 `emergency` 레벨 메시지를 기록하면, 다음처럼 두 채널 모두 로그를 기록합니다:

```
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성

`Log` [파사드](/docs/11.x/facades)를 사용해 로그에 정보를 기록할 수 있습니다. 앞서 설명한 대로, 로그에는 [RFC 5424 사양](https://tools.ietf.org/html/rfc5424)에서 정의한 8가지 레벨이 있습니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

```
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

이 중 원하는 메서드를 호출하여 해당 레벨의 로그 메시지를 기록하면 됩니다. 기본적으로 메시지는 `logging` 설정 파일에서 기본 채널로 지정된 곳에 작성됩니다:

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
     * 주어진 사용자의 프로필을 보여줍니다.
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

로그 메서드에 컨텍스트 데이터를 담은 배열을 함께 전달할 수 있습니다. 이 데이터는 로그 메시지에 포맷되어 함께 표시됩니다:

```
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

때때로는 특정 채널에서 이후 기록되는 로그에 항상 포함할 컨텍스트 정보를 지정하고 싶을 때가 있습니다. 예를 들어, 애플리케이션에 들어오는 요청마다 발급되는 요청 ID를 로그에 포함시키고 싶은 경우입니다. 이럴 때는 `Log` 파사드의 `withContext` 메서드를 호출합니다:

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
     * 들어오는 요청을 처리합니다.
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

_모든_ 로그 채널에 컨텍스트를 공유하고 싶다면 `Log::shareContext()` 메서드를 호출할 수도 있습니다. 이 메서드는 이미 생성된 모든 채널과 앞으로 생성될 채널에도 컨텍스트를 제공합니다:

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
     * 들어오는 요청을 처리합니다.
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
> 대기열 큐 작업 처리 중에도 로그 컨텍스트를 공유해야 한다면, [작업 미들웨어](/docs/11.x/queues#job-middleware)를 활용하세요.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 작성하기

애플리케이션 기본 채널 외에 다른 채널로 로그를 기록하고 싶은 경우가 있습니다. 이럴 때는 `Log` 파사드의 `channel` 메서드를 사용하여 설정에 정의된 특정 채널을 호출할 수 있습니다:

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

또한 여러 채널을 묶어 즉석에서 스택을 구성할 수도 있습니다. `stack` 메서드가 이를 지원합니다:

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 즉석에서 생성하는 채널 (On-Demand Channels)

애플리케이션의 설정 파일에 정의되지 않은 채널 구성을 런타임 시에 즉석에서 제공해 만들 수도 있습니다. 이때는 `Log` 파사드의 `build` 메서드에 설정 배열을 넘기면 됩니다:

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

즉석에서 만든 채널을 스택에도 포함시킬 수 있습니다. 이럴 때는, `stack` 메서드에 배열로 다른 채널들과 함께 즉석 채널 인스턴스도 전달합니다:

```
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

가끔 기존 채널의 Monolog 설정에 대해 완전한 제어권이 필요할 때가 있습니다. 예를 들어, Laravel 내장 `single` 채널에 맞춤형 Monolog `FormatterInterface` 구현체를 적용하고 싶을 수 있습니다.

이때는 해당 채널 설정에 `tap` 배열을 정의합니다. `tap` 배열에는 Monolog 인스턴스가 생성된 후 이를 조작할 수 있는 클래스 목록을 담습니다. 이 클래스들을 담을 고정된 위치는 없으니, 애플리케이션 내 마음에 드는 디렉토리를 생성해 클래스를 배치하세요:

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

설정 후에는, Monolog 인스턴스를 커스터마이징할 클래스를 한 개 정의하면 됩니다. 이 클래스는 하나의 `__invoke` 메서드만 있으면 되며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. 이 `Illuminate\Log\Logger`는 내부 Monolog 인스턴스에 모든 메서드 호출을 전달해 줍니다:

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
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/11.x/container)를 통해 해결되므로, 생성자 의존성이 있으면 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에서는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 지원하지만, Laravel은 모든 핸들러별 내장 채널을 제공하지는 않습니다. 특정 Monolog 핸들러에 해당하는 Laravel 로그 드라이버가 없으면, `monolog` 드라이버를 사용해 원하는 핸들러 인스턴스를 가진 커스텀 채널을 쉽게 만들 수 있습니다.

`monolog` 드라이버를 사용할 때는 `handler` 옵션에 생성할 핸들러 클래스를 지정하며, 생성자 인자를 필요에 따라 `with` 옵션으로 넘깁니다:

```
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

`monolog` 드라이버에선 기본으로 Monolog의 `LineFormatter`가 사용됩니다. 하지만 `formatter`와 `formatter_with` 옵션으로 핸들러에 전달할 포매터 타입과 옵션을 변경할 수 있습니다:

```
'browser' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\BrowserConsoleHandler::class,
    'formatter' => Monolog\Formatter\HtmlFormatter::class,
    'formatter_with' => [
        'dateFormat' => 'Y-m-d',
    ],
],
```

핸들러 자체가 포매터를 제공하는 경우, `formatter` 옵션을 `default`로 설정할 수 있습니다:

```
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog은 로그 기록 전에 메시지를 가공하는 프로세서도 지원합니다. 직접 프로세서를 만들거나 [Monolog이 제공하는 프로세서들](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)을 사용할 수 있습니다.

`monolog` 드라이버 채널 설정에 `processors` 옵션을 추가해 프로세서를 지정할 수 있습니다:

```
 'memory' => [
     'driver' => 'monolog',
     'handler' => Monolog\Handler\StreamHandler::class,
     'with' => [
         'stream' => 'php://stderr',
     ],
     'processors' => [
         // 단순 방식...
         Monolog\Processor\MemoryUsageProcessor::class,

         // 옵션 포함 방식...
         [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
     ],
 ],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 이용한 커스텀 채널 생성

Monolog 인스턴스의 생성과 구성을 완전 제어하고 싶으면, `config/logging.php` 설정에 `custom` 드라이버 타입을 지정할 수 있습니다. 이때 `via` 옵션에 팩토리 클래스 이름을 넣으면, 이 클래스가 Monolog 인스턴스를 생성합니다:

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

이제 Monolog 인스턴스를 생성할 팩토리 클래스를 하나 만드세요. 이 클래스는 하나의 `__invoke` 메서드를 포함하며, 이 메서드는 채널 구성 배열을 인자로 받고 Monolog 로거 인스턴스를 반환해야 합니다:

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
## Pail을 사용한 로그 메시지 실시간 확인 (Tailing Log Messages Using Pail)

문제를 디버깅하거나 특정 유형의 에러를 실시간 모니터링할 때, 애플리케이션 로그를 실시간으로 확인해야 할 때가 많습니다.

Laravel Pail은 Laravel 애플리케이션의 로그 파일을 커맨드 라인에서 쉽게 실시간으로 확인할 수 있게 해 주는 패키지입니다. 일반적인 `tail` 명령어와 달리, Pail은 Sentry나 Flare 같은 로그 드라이버도 지원하며, 원하는 로그를 빠르게 찾을 수 있도록 여러 필터 기능도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" alt="Pail 로그 예시" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]  
> Laravel Pail은 [PHP 8.2 이상](https://php.net/releases/)과 [PCNTL 확장](https://www.php.net/manual/en/book.pcntl.php)이 필요합니다.

Composer 패키지 관리자를 통해 프로젝트에 Pail을 설치합니다:

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 실시간 확인을 시작하려면 `pail` 명령어를 실행하세요:

```bash
php artisan pail
```

출력의 자세한 정도를 높이고 로그 메시지가 잘리거나 …로 표시되는 것을 막으려면 `-v` 옵션을 사용하세요:

```bash
php artisan pail -v
```

가장 자세한 출력과 예외 스택 트레이스를 보려면 `-vv` 옵션을 사용합니다:

```bash
php artisan pail -vv
```

실시간 로그 확인을 멈추려면 언제든지 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션을 사용해 로그 타입, 파일, 메시지, 스택 트레이스 내용 등으로 로그를 필터링할 수 있습니다:

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 내용으로만 로그를 필터링하려면 `--message` 옵션을 사용합니다:

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

로그 레벨에 따라 필터링하려면 `--level` 옵션을 사용하세요:

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 보고 싶다면, `--user` 옵션에 사용자 ID를 지정합니다:

```bash
php artisan pail --user=1
```