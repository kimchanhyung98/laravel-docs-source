# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 요구 사항](#channel-prerequisites)
    - [기능 중단(deprecated) 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보 추가](#contextual-information)
    - [특정 채널에 로그 작성](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 실시간 확인](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내부에서 어떤 일이 일어나는지 더 잘 파악할 수 있도록, 라라벨은 강력한 로깅 서비스를 제공합니다. 이를 통해 메시지를 파일, 시스템 에러 로그, 심지어 Slack과 같은 외부 서비스로 전송하여 팀원 전체에게 알릴 수 있습니다.

라라벨의 로깅 시스템은 "채널"을 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 의미합니다. 예를 들어, `single` 채널은 하나의 파일에 로그를 기록하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 그 심각도에 따라 여러 채널에 동시에 기록될 수도 있습니다.

라라벨은 내부적으로 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하며, 이를 통해 다양한 강력한 로그 핸들러를 지원합니다. 라라벨에서는 이러한 핸들러를 간편하게 설정할 수 있으며, 여러 핸들러를 조합해서 애플리케이션의 로그 처리를 원하는 대로 맞춤 설정할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 위치합니다. 이 파일에서 로그 채널을 자유롭게 구성할 수 있으므로, 사용 가능한 각 채널과 해당 옵션들을 꼼꼼히 확인하시기 바랍니다. 아래에서 몇 가지 대표적인 옵션을 소개합니다.

기본적으로 라라벨은 로그 메시지 기록 시 `stack` 채널을 사용합니다. 스택 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 구성에 대한 더 자세한 내용은 [아래 설명](#building-log-stacks)을 참고해 주세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 동작합니다. 드라이버는 로그 메시지가 어떻게, 어디에 기록되는지 결정합니다. 아래는 모든 라라벨 애플리케이션에서 사용할 수 있는 로그 채널 드라이버 목록입니다. 대부분의 드라이버는 이미 애플리케이션의 `config/logging.php` 파일에 정의되어 있으니, 직접 파일을 확인하며 익숙해질 것을 권장합니다.

<div class="overflow-auto">

| 이름          | 설명                                                               |
| ------------- | ------------------------------------------------------------------ |
| `custom`      | 지정한 팩토리를 호출해 채널을 생성하는 드라이버입니다.              |
| `daily`       | 매일 새 로그 파일로 교체되는 `RotatingFileHandler` 기반 Monolog 드라이버입니다. |
| `errorlog`    | 시스템 오류 로그에 기록하는 `ErrorLogHandler` 기반 Monolog 드라이버입니다.   |
| `monolog`     | 지원되는 어떤 Monolog 핸들러도 이용할 수 있는 Monolog 팩토리 드라이버입니다.  |
| `papertrail`  | `SyslogUdpHandler`를 사용하는 Monolog 드라이버(원격 Syslog 서비스).         |
| `single`      | 하나의 파일 또는 경로에 로그를 기록하는 채널 (`StreamHandler`).           |
| `slack`       | `SlackWebhookHandler` 기반으로 Slack으로 로그를 전송하는 Monolog 드라이버.   |
| `stack`       | 여러 채널을 하나로 묶어주는 래퍼(Wrapper)입니다.                         |
| `syslog`      | 시스템 syslog에 기록하는 `SyslogHandler` 기반 Monolog 드라이버입니다.        |

</div>

> [!NOTE]
> `monolog`과 `custom` 드라이버에 대한 자세한 설명은 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정하기

기본적으로 Monolog 인스턴스는 현재 환경(예: `production`, `local`)에 해당하는 "채널 이름"으로 생성됩니다. 이 값을 변경하고 싶다면 채널 설정에 `name` 옵션을 추가하세요.

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

`single`과 `daily` 채널에는 `bubble`, `permission`, `locking` 총 세 가지의 선택적 설정 옵션이 있습니다.

<div class="overflow-auto">

| 이름          | 설명                                                                            | 기본값  |
| ------------- | ----------------------------------------------------------------------------- | ------- |
| `bubble`      | 메시지가 처리된 후에도 상위 채널로 전달(버블링)할지 여부를 지정합니다.            | `true`  |
| `locking`     | 로그 파일에 기록하기 전에 잠금을 시도할지 여부입니다.                             | `false` |
| `permission`  | 생성되는 로그 파일의 권한 설정입니다.                                           | `0644`  |

</div>

또한, `daily` 채널의 보존 정책은 `LOG_DAILY_DAYS` 환경 변수나 `days` 구성 옵션으로 설정할 수 있습니다.

<div class="overflow-auto">

| 이름     | 설명                                                | 기본값  |
| -------- | -------------------------------------------------- | ------- |
| `days`   | 일별 로그 파일이 몇 일 동안 보관될지 지정합니다.    | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정이 필요합니다. 해당 값들은 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수로 지정합니다. 값은 [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 반드시 `url` 설정값이 필요합니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 지정할 수 있습니다. 이 URL은 여러분이 Slack 팀에 대해 설정한 [인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)의 URL과 일치해야 합니다.

기본적으로 Slack은 `critical` 레벨 이상의 로그만 수신하지만, `LOG_LEVEL` 환경 변수 또는 Slack 채널의 `level` 설정값을 조정해 받을 로그 레벨을 변경할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 기능 중단(deprecated) 경고 로깅

PHP, 라라벨 그리고 기타 라이브러리들은 일부 기능이 더 이상 지원되지 않을 예정임을 알리기 위해 deprecated 경고를 출력합니다. 이러한 경고를 로그로 남기고 싶다면, `LOG_DEPRECATIONS_CHANNEL` 환경 변수나 `config/logging.php` 설정 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다.

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는, `deprecations`라는 이름의 로그 채널을 직접 정의할 수도 있습니다. 이 이름의 채널이 존재하면 deprecations 로그는 항상 해당 채널로 기록됩니다.

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

앞서 언급한 것처럼, `stack` 드라이버를 이용하면 여러 채널을 하나의 로그 채널로 묶어 편리하게 사용할 수 있습니다. 실제 운영 환경에서 많이 볼 수 있는 스택 로그 설정 예시는 다음과 같습니다.

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

이 설정을 하나씩 살펴보면, 먼저 `stack` 채널이 `syslog`와 `slack`이라는 두 채널을 `channels` 옵션을 통해 묶고 있습니다. 그러므로 로그 메시지가 기록되면 이 두 채널 모두 로그를 남길 수 있는 기회를 갖습니다. 단, 실제로 로그 메시지가 기록되는지는 아래에서 다루는 "레벨"에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

위 설정 예시에서 `syslog`와 `slack` 채널에 `level` 설정 옵션이 존재합니다. 이 옵션은 해당 채널에 메시지가 기록되기 위해 필요한 최소 "레벨"을 지정합니다. 라라벨에서 사용하는 Monolog는 [RFC 5424](https://tools.ietf.org/html/rfc5424)에서 정의한 모든 로그 레벨을 지원합니다. 레벨은 심각도가 높은 순서대로 **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 가 있습니다.

예를 들어, 다음과 같이 `debug` 메서드를 이용해 로그를 기록한다면:

```php
Log::debug('An informational message.');
```

이 설정에서는 `syslog` 채널이 메시지를 시스템 로그로 기록합니다. 그러나 이 메시지는 `critical` 이상 레벨이 아니므로 Slack 채널에는 보내지지 않습니다. 만약 `emergency` 메시지를 남긴다면, 두 채널 모두 최소 레벨 조건을 만족하므로 시스템 로그와 Slack 모두에 메시지가 전송됩니다.

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

로그 메시지를 작성할 땐 `Log` [파사드](/docs/12.x/facades)를 사용합니다. 앞서 언급했듯, 라라벨의 로거는 [RFC 5424](https://tools.ietf.org/html/rfc5424)에 정의된 8가지 로그 레벨을 모두 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

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

이 중 어떤 메서드든 호출해 해당 레벨의 메시지를 로그로 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에서 지정한 기본 로그 채널로 저장됩니다.

```php
<?php

namespace App\Http\Controllers;

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
### 컨텍스트 정보 추가

로그 메서드에는 컨텍스트 데이터(배열)를 함께 전달할 수 있습니다. 이 컨텍스트 정보는 로그 메시지와 함께 포맷되어 출력됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널에서 모든 이후 로그 항목에 공통적으로 포함될 컨텍스트 정보를 지정하고 싶은 경우도 있습니다. 예를 들어, 각 요청마다 고유의 요청 ID를 모든 로그에 포함하고 싶을 수 있습니다. 이럴 때는 `Log` 파사드의 `withContext` 메서드를 사용하면 됩니다.

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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하고 싶다면 `Log::shareContext()` 메서드를 사용하세요. 이 메서드를 쓰면 이미 생성된 채널뿐 아니라 이후 생성되는 채널에도 컨텍스트 정보가 공유됩니다.

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
> 큐에서 실행되는 작업(job) 처리 중에도 로그 컨텍스트를 공유해야 할 경우, [작업 미들웨어](/docs/12.x/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 로그 작성

기본 채널이 아닌 다른 채널에 로그 메시지를 기록하고 싶을 때도 있습니다. 이럴 때는 `Log` 파사드의 `channel` 메서드를 사용해서, 설정 파일에 정의된 아무 채널이나 지정해 로그를 남길 수 있습니다.

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 임시로 묶어 로그 스택을 만들고 싶을 때는 `stack` 메서드를 쓸 수 있습니다.

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드(즉시 생성) 채널

`logging` 설정 파일에 등록하지 않고, 런타임에 직접 설정값을 넘겨 온디맨드 채널을 생성할 수도 있습니다. 이럴 땐 `Log` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

온디맨드 채널도 여러 개 묶어서 온디맨드 스택 로그를 만들 수 있습니다. 이 경우 `stack` 메서드에 온디맨드 채널 인스턴스를 배열에 포함시켜 넘기면 됩니다.

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

때로는 기존 채널에 대해 Monolog의 동작을 완전히 직접 제어하고 싶을 수 있습니다. 예를 들어, 라라벨에서 기본 제공하는 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현체를 지정하고 싶은 경우가 그렇습니다.

이렇게 커스터마이징 하려면, 채널 설정값에 `tap` 배열을 추가하세요. 이 배열엔 Monolog 인스턴스가 생성된 뒤 커스터마이징(또는 "탭 인")할 기회를 가지는 클래스들의 목록을 작성합니다. 이런 클래스의 위치는 고정되어 있지 않으니, 애플리케이션 내에 자유롭게 디렉토리를 만들어 관리할 수 있습니다.

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

`tape` 옵션을 지정했다면, 이제 실제로 Monolog 인스턴스를 커스터마이즈하는 클래스를 만듭니다. 이 클래스에는 하나의 `__invoke` 메서드만 있으면 되고, 인자로 `Illuminate\Log\Logger` 인스턴스를 받습니다. 이 인스턴스는 실제 Monolog 인스턴스로의 모든 메서드 호출을 프록시합니다.

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 전달된 로거 인스턴스를 커스터마이징합니다.
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
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/12.x/container)에 의해 의존성이 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 매우 다양한 [핸들러들](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)이 있으며, 라라벨은 모든 핸들러에 맞는 채널을 기본 제공하지는 않습니다. 특정 Monolog 핸들러를 사용하는 커스텀 채널을 만들고 싶다면, `monolog` 드라이버를 사용할 수 있습니다.

`monolog` 드라이버에서는 어떤 핸들러를 사용할지 `handler` 설정값에 지정하면 됩니다. 핸들러가 생성될 때 생성자 인자가 필요하다면, `handler_with` 설정으로 지정할 수 있습니다.

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
#### Monolog 포매터(Formatter)

`monolog` 드라이버 사용 시 Monolog의 `LineFormatter`가 기본 포매터로 지정됩니다. 하지만, 원하는 경우 `formatter` 및 `formatter_with` 설정으로 사용되는 포매터 종류와 옵션을 변경할 수 있습니다.

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

만약 사용 중인 Monolog 핸들러 자체가 전용 포매터를 내장하고 있다면, `formatter` 옵션값을 `default`로 지정하면 됩니다.

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서(Processor)

Monolog는 로그 메시지를 기록하기 전에 사전 처리를 할 수 있습니다. 직접 프로세서를 만들 수도 있고, [Monolog에서 제공하는 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수도 있습니다.

`monolog` 드라이버에서 프로세서를 지정하려면, 채널 설정에 `processors` 값을 추가하세요.

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 문법...
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션 포함...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog 인스턴스의 생성과 구성을 완전히 직접 제어하는 "완전한 커스텀 채널"이 필요하다면, `config/logging.php` 파일에 `custom` 드라이버 타입을 지정할 수 있습니다. 이 설정에는 Monolog 인스턴스를 만들어주는 팩토리 클래스명을 `via` 옵션에 지정해야 합니다.

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 채널 설정이 끝나면, Monolog 인스턴스를 생성하는 클래스를 정의하면 됩니다. 이 클래스에는 반드시 `__invoke` 메서드가 있어야 하며, 인자로 해당 채널의 설정 배열이 전달됩니다. 그리고 Monolog logger 인스턴스를 반환하면 됩니다.

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
## Pail을 사용한 로그 실시간 확인

애플리케이션 로그를 실시간으로 모니터링할 필요가 있을 때가 많습니다. 예를 들어, 문제를 디버깅하거나 특정 에러 유형을 확인하며 로그를 지속적으로 지켜봐야 하는 경우가 그 예입니다.

Laravel Pail 패키지를 사용하면, 커맨드 라인에서 곧바로 라라벨 애플리케이션의 로그 파일을 손쉽게 살펴볼 수 있습니다. 일반적인 `tail` 명령어와 달리, Pail은 Sentry, Flare 등 어떠한 로그 드라이버와도 연동되도록 설계되어 있습니다. 또한 원하는 로그만 빠르게 찾을 수 있게 다양한 필터 기능을 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PHP 8.2 이상](https://php.net/releases/)과 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장이 필요합니다.

Composer 패키지 매니저를 사용해 프로젝트에 Pail을 설치하세요.

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### 사용법

실시간 로그 확인을 시작하려면 `pail` 명령어를 실행합니다.

```shell
php artisan pail
```

출력의 상세함을 높이고 내용이 잘리지 않도록 하려면 `-v` 옵션을 사용하세요.

```shell
php artisan pail -v
```

가장 많은 정보를 확인하고 예외 스택 트레이스까지 출력하려면 `-vv` 옵션을 사용하세요.

```shell
php artisan pail -vv
```

로그 확인을 중지하려면 언제든 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

로그 타입, 파일, 메시지, 스택 트레이스 내용을 기준으로 로그를 필터링하려면 `--filter` 옵션을 사용할 수 있습니다.

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

로그 메시지 내용만을 기준으로 필터링하고 싶다면 `--message` 옵션을 사용하세요.

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

[로그 레벨](#log-levels)에 따라 로그를 필터링하려면 `--level` 옵션을 사용할 수 있습니다.

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 보고 싶을 때는, 해당 사용자의 ID를 `--user` 옵션에 지정하세요.

```shell
php artisan pail --user=1
```
