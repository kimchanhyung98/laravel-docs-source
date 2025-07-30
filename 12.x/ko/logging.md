# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 준비사항](#channel-prerequisites)
    - [폐기 예정 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 빌드하기](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널로 로그 작성하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널을 위한 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 실시간 조회](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션에서 어떤 일이 발생하는지 더 잘 파악할 수 있도록, 라라벨은 강력한 로깅 서비스를 제공합니다. 덕분에 파일, 시스템 오류 로그, 그리고 Slack 등 다양한 곳에 메세지를 기록하고 전체 팀에 즉시 알릴 수 있습니다.

라라벨의 로깅 시스템은 "채널(channel)"을 기반으로 합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 로그 파일에 메시지를 기록하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

내부적으로 라라벨은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하며, 다양한 강력한 로그 핸들러를 지원합니다. 라라벨은 이러한 핸들러를 쉽게 설정할 수 있게 해주므로, 여러 핸들러를 자유롭게 조합해 애플리케이션에 적합한 로그 처리를 구성할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 위치합니다. 이 파일에서는 애플리케이션의 로그 채널을 구성할 수 있으니, 각 채널과 옵션들을 꼭 살펴봐야 합니다. 아래에서 몇 가지 주요 옵션을 예시로 알아봅니다.

기본적으로 라라벨은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 빌드에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 동작합니다. 드라이버는 실제로 로그 메시지가 어떤 방식으로, 어디에 기록되는지 결정합니다. 아래는 모든 라라벨 애플리케이션에서 사용 가능한 로그 채널 드라이버입니다. 대부분의 드라이버는 이미 애플리케이션의 `config/logging.php` 파일에 포함되어 있으니, 파일을 직접 검토하여 구조를 익혀보세요.

<div class="overflow-auto">

| 이름         | 설명                                                                |
| ------------ | ------------------------------------------------------------------- |
| `custom`     | 지정한 팩토리를 호출하여 채널을 생성하는 드라이버                   |
| `daily`      | 매일 로그 파일을 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버 |
| `errorlog`   | `ErrorLogHandler` 기반 Monolog 드라이버                             |
| `monolog`    | 지원되는 어떤 Monolog 핸들러도 사용할 수 있는 Monolog 팩토리 드라이버 |
| `papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버                            |
| `single`     | 하나의 파일 또는 경로에 기록하는 로그 채널(`StreamHandler`)         |
| `slack`      | `SlackWebhookHandler` 기반 Monolog 드라이버                         |
| `stack`      | "멀티 채널" 생성을 돕는 래퍼 드라이버                              |
| `syslog`     | `SyslogHandler` 기반 Monolog 드라이버                               |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정하기

기본적으로 Monolog은 `production` 또는 `local`처럼 현재 환경 이름을 "채널 이름"으로 사용합니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하면 됩니다.

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 사전 준비사항

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널에는 세 가지 선택적 설정 옵션이 있습니다: `bubble`, `permission`, `locking`.

<div class="overflow-auto">

| 이름         | 설명                                                                   | 기본값   |
| ------------ | ---------------------------------------------------------------------- | -------- |
| `bubble`     | 메시지 처리 후 다른 채널로 위임(버블링)할지 여부를 지정합니다.          | `true`   |
| `locking`    | 로그 파일 기록 전 파일 잠금을 시도할지 설정합니다.                      | `false`  |
| `permission` | 로그 파일에 적용할 파일 권한                                            | `0644`   |

</div>

또한, `daily` 채널의 로그 파일 유지 기간은 `LOG_DAILY_DAYS` 환경 변수나 `days` 환경설정 옵션을 통해 지정할 수 있습니다.

<div class="overflow-auto">

| 이름    | 설명                                               | 기본값 |
| ------- | -------------------------------------------------- | ------ |
| `days`  | 일별 로그 파일을 며칠 동안 보관할지 지정합니다.     | `14`   |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정 옵션이 필요합니다. 이 값들은 각각 `PAPERTRAIL_URL`과 `PAPERTRAIL_PORT` 환경 변수로 지정할 수 있습니다. 값은 [Papertrail 공식 가이드](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 설정값을 필요로 하며, 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수에 지정할 수 있습니다. 이 URL은 조직에서 설정한 [Slack 인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)의 주소와 일치해야 합니다.

기본적으로 Slack 채널은 `critical` 레벨 이상의 로그만 전송합니다. 필요하다면, `LOG_LEVEL` 환경 변수나 Slack 로그 채널 설정 배열의 `level` 옵션을 변경해 로그 레벨을 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 폐기 예정 경고 로깅

PHP, 라라벨, 그리고 여러 라이브러리들은 일부 기능이 폐기(deprecated) 되었으며, 향후 버전에서 제거될 예정임을 사용자에게 알립니다. 이런 폐기 예정 경고를 로그로 남기고 싶다면 `LOG_DEPRECATIONS_CHANNEL` 환경 변수 또는 애플리케이션의 `config/logging.php` 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다.

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는, `deprecations`라는 이름의 로그 채널을 정의할 수도 있습니다. 이 채널이 존재하면 항상 폐기 경고 로그에 사용됩니다.

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 빌드하기

앞서 언급한 것처럼, `stack` 드라이버를 사용하면 여러 채널을 하나의 로그 채널로 묶어서 관리할 수 있습니다. 프로덕션 환경에서 흔히 볼 수 있는 예시 설정을 살펴보겠습니다.

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

이 설정을 분석해보면, `stack` 채널은 `channels` 옵션을 통해 두 개의 채널인 `syslog`와 `slack`을 묶고 있습니다. 즉, 로그 메시지가 기록될 때 두 채널 모두 로그를 기록할 수 있게 되는 것입니다. 다만, 아래에서 보듯 각각의 채널에서 실제로 로그가 기록되는지는 메시지의 심각도(레벨)에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 채널 설정에 있는 `level` 옵션에 주목하세요. 이 옵션은 해당 채널에서 로그로 기록할 최소 "레벨"을 의미합니다. 라라벨의 로깅을 담당하는 Monolog는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에서 정의한 모든 로그 레벨을 지원합니다. 심각도 순(높은 것부터 낮은 것까지)은 다음과 같습니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

예를 들어, `debug` 메서드를 사용해 메시지를 기록할 때:

```php
Log::debug('An informational message.');
```

이 설정에서는 `syslog` 채널이 메시지를 시스템 로그에 기록하지만, 메시지 레벨이 `critical` 이상이 아니므로 Slack에는 전송되지 않습니다. 하지만, `emergency` 메시지를 로그로 남기면 시스템 로그와 Slack 모두에 전송됩니다. 그 이유는 `emergency`가 두 채널이 요구하는 최소 레벨보다 높기 때문입니다.

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성

로그에 정보를 남기려면 `Log` [파사드](/docs/12.x/facades)를 사용하면 됩니다. 앞서 언급했듯이, 라라벨 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 8가지 로그 레벨 메서드를 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

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

이들 메서드 중 원하는 레벨을 호출하면 해당 레벨로 메시지가 로깅됩니다. 기본적으로 메시지는 `logging` 설정 파일에 정의한 기본 로그 채널에 기록됩니다.

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

로그 메서드에는 추가 정보(컨텍스트 데이터)를 배열 형태로 전달할 수 있습니다. 이 정보는 로그 메시지와 함께 포매팅되어 표시됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

때때로, 이후 기록될 모든 로그에 특정 컨텍스트 정보를 포함하고 싶을 때가 있습니다. 예를 들어, 각 요청마다 고유한 request ID를 포함시켜 추적하고 싶을 수 있습니다. 이때는 `Log` 파사드의 `withContext` 메서드를 사용하면 됩니다.

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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드는 이미 생성된 채널은 물론 이후에 생성되는 채널에도 전달됩니다.

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
> 큐 작업 처리 중에 로그 컨텍스트를 공유해야 한다면, [작업 미들웨어](/docs/12.x/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널로 로그 작성하기

때로는 애플리케이션의 기본 채널이 아닌, 다른 특정 채널에 메시지를 기록하고 싶을 때가 있습니다. 이 경우, `Log` 파사드의 `channel` 메서드를 사용해 설정 파일에 정의된 아무 채널이나 선택해 로그를 남길 수 있습니다.

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 즉석에서 묶어 하나의 스택으로 만들어 로그를 기록하고 싶다면 `stack` 메서드를 사용할 수 있습니다.

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 즉석(On-Demand) 채널

`logging` 설정 파일에 미리 정의하지 않고, 런타임에 직접 채널 설정을 만들어 사용할 수도 있습니다. 이때는 `Log` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

즉석으로 만들어진 채널을 즉석 스택에 포함시켜 여러 채널로 동시에 로그를 남길 수도 있습니다. 이땐, 스택에 해당 채널 인스턴스를 배열로 넘깁니다.

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
### 채널을 위한 Monolog 커스터마이징

기존 채널에 대해 Monolog의 동작 또는 구성 방식을 세밀하게 제어해야 할 때가 있습니다. 예를 들어, 라라벨에서 제공하는 기본 `single` 채널에 직접 개발한 Monolog `FormatterInterface` 구현체를 적용하고 싶을 수 있습니다.

먼저, 해당 채널 설정에 `tap` 배열을 추가합니다. 이 배열에는 Monolog 인스턴스를 생성한 후에 커스터마이징(혹은 "탭")할 수 있는 클래스들의 목록을 지정합니다. 이 클래스들은 애플리케이션의 원하는 디렉터리에 자유롭게 만들 수 있습니다.

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

`tap` 옵션 지정을 마쳤으면, 이제 Monolog 인스턴스를 원하는 대로 커스터마이징하는 클래스를 작성하면 됩니다. 이 클래스는 `__invoke`라는 단일 메서드만 필요하며, `Illuminate\Log\Logger` 인스턴스를 파라미터로 전달받습니다. `Logger` 인스턴스는 내부적으로 Monolog 인스턴스에 모든 메서드 호출을 위임합니다.

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
> 모든 "탭" 클래스는 [서비스 컨테이너](/docs/12.x/container)에 의해 해석되기 때문에, 생성자에서 필요한 의존성은 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 존재하지만, 라라벨이 모든 핸들러에 대해 내장 채널을 제공하는 것은 아닙니다. 경우에 따라, 라라벨에서 별도의 드라이버가 없는 Monolog 핸들러만 인스턴스화해서 커스텀 채널을 만들고싶을 수 있습니다. 이런 채널은 `monolog` 드라이버로 간단히 생성할 수 있습니다.

`monolog` 드라이버를 사용할 때, `handler` 옵션은 어떤 핸들러를 인스턴스화할지 지정합니다. 핸들러가 생성자 매개변수를 필요로 한다면, `handler_with` 옵션에 전달하면 됩니다.

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
#### Monolog 포매터(formatter)

`monolog` 드라이버를 사용할 경우, 기본 포매터는 Monolog의 `LineFormatter`가 지정됩니다. 그러나, `formatter` 및 `formatter_with` 설정을 통해 핸들러에 전달할 포매터 타입과 옵션을 자유롭게 조절할 수도 있습니다.

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

Monolog 핸들러가 자체적으로 포매터를 제공할 수 있을 땐, `formatter` 설정값에 `default`를 지정할 수 있습니다.

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서(processor)

Monolog은 메시지를 기록하기 전에 가공/처리하는 프로세서 기능도 지원합니다. 직접 프로세서를 만들거나, [Monolog에서 제공하는 기존 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

`monolog` 드라이버에서 프로세서를 커스터마이징하고 싶다면, 채널 설정에 `processors` 값을 추가하면 됩니다.

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 구문...
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
### 팩토리를 통한 커스텀 채널 생성

Monolog의 인스턴스화와 설정을 완전히 직접 제어하는 커스텀 채널이 필요하다면, `config/logging.php` 파일에 `custom` 드라이버 타입을 지정할 수 있습니다. 이 설정에는 Monolog 인스턴스를 생성할 팩토리 클래스의 이름을 담는 `via` 옵션이 포함되어야 합니다.

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 채널 설정이 끝났다면, 이제 Monolog 인스턴스를 직접 생성하는 클래스를 만들면 됩니다. 이 클래스는 하나의 `__invoke` 메서드만 필요하며, 메서드는 채널의 설정 배열을 인자로 받아 Monolog 로그 인스턴스를 반환해야 합니다.

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
## Pail을 사용한 로그 실시간 조회

실시간으로 애플리케이션 로그를 확인해야 할 때가 자주 있습니다. 예를 들어, 장애 복구 중이거나 특정 종류의 에러를 모니터링 할 때 말이죠.

Laravel Pail은 라라벨 애플리케이션의 로그 파일을 커맨드라인에서 바로 손쉽게 볼 수 있게 해주는 패키지입니다. 일반적인 `tail` 명령어와 달리, Pail은 Sentry, Flare 등 어떤 로그 드라이버와도 함께 동작합니다. 또, 유용한 필터 기능이 있어 필요한 로그를 빠르게 찾을 수 있습니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다.

우선 Composer 패키지 관리자를 통해 Pail을 프로젝트에 설치하세요.

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그를 실시간으로 보기 시작하려면 아래처럼 `pail` 명령어를 실행하세요.

```shell
php artisan pail
```

출력의 상세 수준을 높이고 (줄임표 없이) 모든 내용을 보고 싶다면 `-v` 옵션을 붙이세요.

```shell
php artisan pail -v
```

최대한 자세한 출력과 예외의 스택 트레이스까지 모두 보려면 `-vv` 옵션을 사용하세요.

```shell
php artisan pail -vv
```

로그 실시간 조회를 중단하려면 언제든 `Ctrl+C`를 누르면 됩니다.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

로그의 유형, 파일, 메시지, 스택 트레이스 내용으로 로그를 필터링하려면 `--filter` 옵션을 사용하세요.

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 내용만으로 필터링하려면 `--message` 옵션을 사용할 수 있습니다.

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

로그를 [로그 레벨](#log-levels)별로 필터링하려면 `--level` 옵션을 지정합니다.

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정한 사용자가 인증된 상태에서 남긴 로그만 조회하고 싶다면, 해당 사용자의 ID를 `--user` 옵션에 넘기세요.

```shell
php artisan pail --user=1
```