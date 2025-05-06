# 로깅

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구축](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 로그 작성](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널용 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 통한 사용자 정의 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 메시지 실시간 보기](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내부에서 어떤 일이 일어나는지 더 쉽게 파악할 수 있도록, Laravel은 메시지를 파일, 시스템 오류 로그, 또는 Slack과 같은 팀 전체에게 알릴 수 있는 곳에 기록할 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel의 로깅은 "채널"을 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 파일로 로그를 기록하고, `slack` 채널은 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

내부적으로 Laravel은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하여 다양한 강력한 로그 핸들러를 지원합니다. Laravel은 이러한 핸들러를 손쉽게 설정할 수 있도록 하여, 여러분의 애플리케이션 로그 핸들링을 자유롭게 커스터마이징할 수 있도록 도와줍니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 저장되어 있습니다. 이 파일을 통해 애플리케이션의 로그 채널을 구성할 수 있으므로, 각 채널과 해당 옵션을 반드시 검토하는 것이 좋습니다. 아래에서 몇 가지 일반적인 옵션을 살펴보겠습니다.

기본적으로, Laravel은 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어줍니다. 스택 구축에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 확인하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 구동됩니다. 드라이버는 로그 메시지가 실제로 어디에, 어떻게 기록될지를 결정합니다. 다음은 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버입니다. 대부분의 드라이버 항목은 이미 `config/logging.php` 파일에 포함되어 있으니, 이 파일을 검토하여 내용을 숙지하세요.

<div class="overflow-auto">

| 이름         | 설명                                                                          |
| ------------ | ----------------------------------------------------------------------------- |
| `custom`     | 지정한 팩토리로 채널을 생성하는 드라이버                                      |
| `daily`      | Monolog의 `RotatingFileHandler` 기반 드라이버로, 매일 로그 파일을 교체합니다    |
| `errorlog`   | Monolog의 `ErrorLogHandler` 기반 드라이버                                     |
| `monolog`    | 다양한 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버                  |
| `papertrail` | Monolog의 `SyslogUdpHandler` 기반 드라이버                                    |
| `single`     | 단일 파일 또는 경로 기반 로거 채널 (`StreamHandler`)                          |
| `slack`      | Monolog의 `SlackWebhookHandler` 기반 드라이버                                 |
| `stack`      | "멀티 채널" 채널 생성을 위한 래퍼                                            |
| `syslog`     | Monolog의 `SyslogHandler` 기반 드라이버                                       |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경(`production`, `local` 등)과 동일한 "채널명"으로 인스턴스화됩니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하면 됩니다.

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

`single`과 `daily` 채널에는 세 가지 선택적 설정 옵션이 있습니다: `bubble`, `permission`, `locking`.

<div class="overflow-auto">

| 이름         | 설명                                                                   | 기본값     |
| ------------ | --------------------------------------------------------------------- | ---------- |
| `bubble`     | 메시지 처리 후 다른 채널로 버블링할지 여부                            | `true`     |
| `locking`    | 기록 전에 로그 파일 잠금 시도                                         | `false`    |
| `permission` | 로그 파일 퍼미션                                                      | `0644`     |

</div>

또한, `daily` 채널의 보존 정책은 `LOG_DAILY_DAYS` 환경 변수나 `days` 설정 옵션으로 지정할 수 있습니다.

<div class="overflow-auto">

| 이름    | 설명                                                  | 기본값  |
| ------- | ----------------------------------------------------- | ------- |
| `days`  | 일일 로그 파일 유지 일수                               | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정 옵션이 필요합니다. 이는 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수로 지정할 수 있습니다. 값은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인 가능합니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 옵션이 필요합니다. 이는 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 지정할 수 있습니다. URL은 Slack 팀에 구성한 [인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)과 일치해야 합니다.

기본적으로 Slack은 `critical` 이상의 로그만 받지만, `LOG_LEVEL` 환경 변수나 Slack 로그 채널 설정 배열의 `level` 옵션을 수정하여 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel, 기타 라이브러리는 향후 버전에서 제거될 기능을 사용자에게 경고합니다. 이러한 사용 중단(deprecation) 경고를 기록하려면, `LOG_DEPRECATIONS_CHANNEL` 환경 변수 또는 애플리케이션의 `config/logging.php` 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다.

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는, `deprecations`라는 이름의 로그 채널을 정의할 수도 있습니다. 이렇게 하면, 해당 이름의 로그 채널이 항상 사용 중단 경고 로그를 기록합니다:

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

앞에서 언급한 것처럼 `stack` 드라이버는 여러 채널을 한 로그 채널에 결합할 수 있게 해줍니다. 아래는 실제 운영 환경에서 볼 수 있는 예시 구성입니다.

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

이 예제 구성에서 `stack` 채널은 `syslog`와 `slack` 두 채널을 `channels` 옵션을 통해 묶고 있습니다. 즉, 메시지가 기록되면 두 채널 모두 해당 메시지를 기록할 기회를 갖게 됩니다. 그러나 실제 해당 채널에 메시지가 기록되는지는 메시지의 심각도/레벨에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

앞 예시의 `syslog` 및 `slack` 채널 설정에 있는 `level` 옵션에 주목하세요. 이 옵션은 해당 채널에 기록되기 위한 메시지의 "최소 레벨"을 정합니다. Laravel의 로깅 서비스가 사용하는 Monolog는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 지원합니다. 심각도 순서대로 **emergency(긴급)**, **alert(경고, 즉시 조치 필요)**, **critical(중대)**, **error(오류)**, **warning(경고)**, **notice(참고 사항)**, **info(정보)**, **debug(디버그)**입니다.

예를 들어, 다음과 같이 `debug` 메서드로 로그를 남겼다고 합시다.

```php
Log::debug('An informational message.');
```

구성에 따라, `syslog` 채널은 이 메시지를 시스템 로그에 기록할 것입니다. 하지만, 메시지 레벨이 `critical` 이상이 아니므로 Slack 채널로는 전송되지 않습니다. 반면에, `emergency` 메시지는 두 채널 모두에 기록됩니다.

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성

`Log` [파사드](/docs/{{version}}/facades)를 사용해 정보를 로그에 기록할 수 있습니다. 앞에서 언급한 바와 같이, 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 8가지 로그 레벨 메서드를 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

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

각 메서드를 호출해 해당 레벨의 메시지를 로그에 남길 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에 지정된 기본 로그 채널에 기록됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자 프로필 표시
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

컨텍스트 데이터 배열을 로그 메서드에 전달할 수 있습니다. 이 컨텍스트 데이터는 메시지와 함께 포맷되어 출력됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널에 기록되는 모든 로그 항목에 포함될 컨텍스트 정보를 지정하고 싶을 때는, 예를 들어 각 요청에 대한 request ID를 로그하고 싶다면, `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다.

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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 호출할 수 있습니다. 이 메서드는 생성된 모든 채널과 이후 생성되는 채널에 컨텍스트 정보를 제공합니다.

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
> 대기(큐) 작업 처리 중에 로그 컨텍스트를 공유해야 할 경우, [작업 미들웨어](/docs/{{version}}/queues#job-middleware)를 활용하세요.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 로그 작성

기본 채널 대신 다른 채널에 메시지를 기록하려면, `Log` 파사드의 `channel` 메서드를 사용해 설정 파일에 정의된 아무 채널이나 가져와 기록할 수 있습니다.

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널로 구성된 임시(온디맨드) 스택을 만들려면 `stack` 메서드를 사용하세요.

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드 채널

애플리케이션의 `logging` 설정 파일에 해당 설정이 없어도, 런타임에 직접 구성 배열을 전달하여 온디맨드 채널을 만들 수도 있습니다. 이를 위해 `Log` 파사드의 `build` 메서드에 구성 배열을 전달합니다.

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

온디맨드 채널을 온디맨드 로그 스택에 포함하고 싶다면, `stack` 메서드에 인스턴스를 배열에 포함시켜 전달합니다.

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
### 채널용 Monolog 커스터마이징

기존 채널의 Monolog 인스턴스를 완벽하게 제어해야 하는 경우도 있습니다. 예를 들어, Laravel 내장 `single` 채널에 사용자 지정 Monolog `FormatterInterface` 구현을 사용하고 싶을 때입니다.

이를 위해, 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열에는 Monolog 인스턴스가 생성된 후 커스터마이징(탭)을 수행할 클래스 목록을 나열합니다. 클래스 위치에는 제약이 없으므로 원한다면 별도의 디렉토리를 만들어 보관해도 됩니다.

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

`tape` 옵션을 구성한 후에는 Monolog 인스턴스를 커스터마이징할 클래스를 구현해야 합니다. 이 클래스에는 `__invoke` 메서드 하나만 필요하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. 이 인스턴스는 모든 호출을 내부 Monolog 인스턴스로 프록시합니다.

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 주어진 로거 인스턴스 커스터마이즈
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
> 모든 "tap" 클래스들은 [서비스 컨테이너](/docs/{{version}}/container)에서 해석되므로, 생성자 의존성 주입을 사용할 수 있습니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 [다양한 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있지만, Laravel은 그 모든 핸들러에 대한 내장 채널을 제공하지는 않습니다. 경우에 따라 특정 Monolog 핸들러 인스턴스만 사용하는 커스텀 채널을 만들고 싶을 수 있습니다. 이런 경우 `monolog` 드라이버를 사용하면 손쉽게 해당 채널을 생성할 수 있습니다.

`monolog` 드라이버를 사용할 때는 `handler` 옵션에 생성할 핸들러를 지정합니다. 필요하다면 핸들러 생성자에 전달할 인수를 `handler_with` 옵션에 배열로 지정합니다.

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

`monolog` 드라이버를 사용할 때는 Monolog의 `LineFormatter`가 기본 포매터로 사용됩니다. 하지만 `formatter` 및 `formatter_with` 옵션을 통해 핸들러에 전달할 포매터 유형을 커스터마이즈할 수 있습니다.

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

자체 포매터를 제공할 수 있는 Monolog 핸들러를 사용하는 경우, `formatter` 옵션을 `default`로 설정할 수 있습니다.

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog는 메시지 기록 전 프로세서를 통해 메시지를 가공할 수도 있습니다. 직접 프로세서를 만들거나, [Monolog에서 제공하는 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

`monolog` 드라이버 채널의 프로세서 구성을 커스터마이즈하려면, `processors` 설정 값을 추가하세요.

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 방법...
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션 지정...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 사용자 정의 채널 생성

Monolog 인스턴스의 생성과 설정을 완전히 제어하는 완전한 커스텀 채널을 정의하고 싶다면, `config/logging.php` 파일에 `custom` 드라이버 타입을 명시하세요. 설정에 Monolog 인스턴스를 생성할 팩토리 클래스명을 `via` 옵션으로 지정해야 합니다.

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 채널을 설정했다면, Monolog 인스턴스를 생성할 클래스를 정의해야 합니다. 이 클래스는 하나의 `__invoke` 메서드만 필요하며, 해당 메서드는 단일 인자로 채널의 설정 배열을 받아 Monolog 로거 인스턴스를 리턴해야 합니다.

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * 사용자 정의 Monolog 인스턴스 생성
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Pail을 사용한 로그 메시지 실시간 보기

애플리케이션 로그를 실시간으로 모니터링해야 할 때가 종종 있습니다. 예를 들어, 이슈를 디버깅하거나 특정 오류 유형을 추적하는 경우입니다.

Laravel Pail은 CLI에서 Laravel 애플리케이션의 로그 파일을 쉽게 모니터링할 수 있도록 도와주는 패키지입니다. 표준 `tail` 명령과 달리, Pail은 Sentry, Flare 등 모든 로그 드라이버와 연동됩니다. 또한, 원하는 로그를 빠르게 찾을 수 있도록 다양한 필터 기능도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PHP 8.2+](https://php.net/releases/) 및 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장이 필요합니다.

Composer 패키지 관리자를 사용하여 프로젝트에 Pail을 설치하세요.

```shell
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그를 실시간으로 보려면 `pail` 명령을 실행하세요.

```shell
php artisan pail
```

출력의 상세 수준을 높이고 메시지 잘림(…)을 방지하려면 `-v` 옵션을 사용하세요.

```shell
php artisan pail -v
```

최대 상세 정보 및 예외 스택 트레이스를 표시하려면 `-vv` 옵션을 사용하세요.

```shell
php artisan pail -vv
```

로그 보기 중에는 언제든지 `Ctrl+C`를 눌러 종료할 수 있습니다.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션을 사용해 로그의 타입, 파일, 메시지, 스택 트레이스 내용을 기준으로 필터링할 수 있습니다.

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 기준으로만 로그를 필터링하려면 `--message` 옵션을 사용하세요.

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

[로그 레벨](#log-levels)로 로그를 필터링하려면 `--level` 옵션을 사용하세요.

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 표시하려면 해당 사용자의 ID를 `--user` 옵션에 지정하세요.

```shell
php artisan pail --user=1
```
