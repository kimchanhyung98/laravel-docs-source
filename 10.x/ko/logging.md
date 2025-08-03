# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 선행 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [문맥 정보](#contextual-information)
    - [특정 채널에 기록하기](#writing-to-specific-channels)
- [Monolog 채널 사용자 정의](#monolog-channel-customization)
    - [채널별 Monolog 사용자 정의](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 메시지 실시간 확인 (Tailing)](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내부에서 어떤 일이 일어나고 있는지 더 잘 파악할 수 있도록, Laravel은 파일, 시스템 오류 로그, 심지어 팀 전체에게 알림을 전송하는 Slack까지 다양한 방법으로 메시지를 기록할 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel의 로깅은 "채널" 기반입니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 단일 로그 파일에 로그를 기록하며, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

내부적으로 Laravel은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 활용하는데, 이는 다양한 강력한 로그 핸들러를 지원합니다. Laravel은 이 핸들러들을 쉽게 설정할 수 있도록 하여, 여러 핸들러를 조합하여 애플리케이션의 로그 처리 방식을 맞춤화할 수 있게 해줍니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로그 동작에 관련된 모든 설정 옵션은 `config/logging.php` 파일에 모여 있습니다. 이 파일에서 로그 채널들을 설정할 수 있으므로, 제공되는 채널들과 옵션들을 꼼꼼히 확인해 보시기 바랍니다. 아래에서는 몇 가지 일반적인 옵션에 대해 살펴보겠습니다.

기본적으로, Laravel은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 구성 방법에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경 이름(예: `production`, `local`)과 동일한 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면, 채널 설정에 `name` 옵션을 추가하면 됩니다:

```
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 작동됩니다. 드라이버는 로그 메시지가 어떻게, 어디에 실제로 기록될지 결정합니다. Laravel 애플리케이션에 기본 제공되는 로그 채널 드라이버는 아래와 같습니다. 대부분 `config/logging.php` 설정 파일에 기본 항목으로 포함되어 있으니 내용을 꼭 확인하세요:

<div class="overflow-auto">

이름 | 설명
------------- | -------------
`custom` | 지정한 팩토리를 사용해 채널을 생성하는 드라이버
`daily` | 일별로 로그 파일을 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버
`errorlog` | `ErrorLogHandler` 기반 Monolog 드라이버
`monolog` | 임의 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버
`papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버
`single` | 단일 파일 또는 경로를 사용하는 로거 채널 (`StreamHandler`)
`slack` | `SlackWebhookHandler` 기반 Monolog 드라이버
`stack` | 여러 채널을 묶는 "멀티-채널" 래퍼
`syslog` | `SyslogHandler` 기반 Monolog 드라이버

</div>

> [!NOTE]  
> `monolog` 및 `custom` 드라이버에 대해 더 자세히 알고 싶다면 [고급 채널 사용자 정의](#monolog-channel-customization) 문서를 참고하세요.

<a name="channel-prerequisites"></a>
### 채널 선행 조건

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널은 선택적으로 다음 세 가지 옵션을 지원합니다: `bubble`, `permission`, `locking`.

<div class="overflow-auto">

이름 | 설명 | 기본값
------------- | ------------- | -------------
`bubble` | 메시지 처리 후 다른 채널로도 버블링(bubble)할지 여부 | `true`
`locking` | 로그 파일에 기록하기 전에 잠금 시도 여부 | `false`
`permission` | 로그 파일 권한 설정 | `0644`

</div>

추가로, `daily` 채널의 로그 보존 기간은 `days` 옵션을 통해 설정할 수 있습니다:

<div class="overflow-auto">

이름 | 설명 | 기본값
------------- |-------------------------------------------------------------------| -------------
`days` | 일별 로그 파일을 얼마나 오래 보관할지(일 단위) | `7`

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널에는 `host`와 `port` 옵션이 필요합니다. 이 값들은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 옵션이 필수입니다. 이 URL은 Slack 팀용 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)으로 설정한 주소여야 합니다.

기본적으로 Slack은 `critical` 이상의 심각도 메시지만 수신합니다. 이 동작은 `config/logging.php` 안의 Slack 로그 채널 내 `level` 설정을 수정하여 변경할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel, 그리고 기타 라이브러리들은 종종 기능이 더 이상 지원되지 않으며 미래 버전에서 제거될 예정임을 사용자에게 알립니다. 이러한 사용 중단 경고를 로그에 기록하려면, 애플리케이션의 `config/logging.php` 설정 파일에서 선호하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```
'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

'channels' => [
    ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 직접 정의할 수 있습니다. 해당 이름의 채널이 정의되어 있으면, 항상 이 채널로 사용 중단 로그가 기록됩니다:

```
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구성하기

앞서 언급했듯, `stack` 드라이버는 여러 채널을 하나의 로그 채널로 묶어 사용 편의성을 제공합니다. 실제 프로덕션 애플리케이션에서 사용할 수 있는 예시 구성을 살펴보겠습니다:

```
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'],
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => 'debug',
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => 'Laravel Log',
        'emoji' => ':boom:',
        'level' => 'critical',
    ],
],
```

이 설정을 자세히 보면, `stack` 채널은 `channels` 옵션을 통해 `syslog`와 `slack` 두 개 채널을 묶고 있습니다. 따라서 로그 메시지가 기록될 때 이 두 채널 모두 메시지를 처리할 기회를 갖습니다. 다만, 아래에서 설명할 메시지 심각도(레벨)에 따라 실제 로그가 기록될지 결정됩니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시의 `syslog`와 `slack` 채널 설정에서 `level` 옵션에 주목하세요. 이 옵션은 해당 채널이 기록할 최소 로그 레벨을 지정합니다. Laravel 로깅은 Monolog를 기반으로 하며, RFC 5424 명세에서 정의한 다음 로그 레벨들을 모두 지원합니다(높은 심각도 순서):

**emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**

예를 들어 `debug` 메서드로 로그를 남기면:

```
Log::debug('An informational message.');
```

우리 설정 대로라면, `syslog` 채널은 메시지를 시스템 로그에 기록하지만, `slack` 채널은 `critical` 이상만 수신하므로 메시지를 전송하지 않습니다. 반면, 아래처럼 `emergency` 레벨로 기록하면 두 채널 모두 이 메시지를 기록하게 됩니다:

```
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

`Log` [파사드(Facade)](/docs/10.x/facades)를 사용하여 로그에 정보를 기록할 수 있습니다. 앞서 언급했듯, 이 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에서 정의된 8가지 로그 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**:

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

해당 레벨에 대응하는 메서드를 호출하여 로그 메시지를 남기면 됩니다. 기본적으로는 `logging` 설정 파일에서 지정한 기본 로그 채널에 메시지가 기록됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
### 문맥 정보

로그 메서드에 문맥 정보를 담은 배열을 전달할 수 있습니다. 이 정보는 로그 메시지와 함께 형식화되어 표시됩니다:

```
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

가끔 특정 채널에서 이후의 모든 로그 기록에 함께 포함될 문맥 정보를 지정하고 싶을 때가 있습니다. 예를 들어, 애플리케이션에 들어오는 각 요청에 연관된 요청 ID를 포함하려 할 수 있습니다. 이럴 때는 `Log` 파사드의 `withContext` 메서드를 호출하세요:

```
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

만약 _모든_ 로깅 채널에 걸쳐 문맥 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드는 이미 생성된 모든 채널과 앞으로 생성될 모든 채널에 문맥 정보를 제공합니다:

```
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
> 큐된 작업 처리 중에도 로그 문맥을 공유해야 하면, [job middleware](/docs/10.x/queues#job-middleware)를 활용하세요.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기

가끔은 애플리케이션의 기본 채널 이외의 채널에 로그를 기록하고 싶을 수 있습니다. 이때는 `Log` 파사드의 `channel` 메서드를 사용해 구성 파일에서 정의한 채널을 불러와 로그를 기록할 수 있습니다:

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 묶는 로그 스택을 임시로 만들고 싶다면 `stack` 메서드를 사용할 수 있습니다:

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 즉석(온디맨드) 채널

애플리케이션 설정 파일에 없는 로그 채널 구성을 런타임에 직접 전달하여 즉석에서 채널을 생성할 수도 있습니다. 이를 위해서는 `Log` 파사드의 `build` 메서드에 구성 배열을 넘겨줍니다:

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

즉석 채널을 포함하는 즉석 로그 스택을 만들 때는, 생성한 채널 인스턴스를 `stack` 메서드 배열에 넣으면 됩니다:

```
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog 채널 사용자 정의

<a name="customizing-monolog-for-channels"></a>
### 채널별 Monolog 사용자 정의

기존 채널의 Monolog 설정을 완전히 제어해야 할 때가 있습니다. 예를 들어, 기본 제공되는 `single` 채널에 대해 커스텀 Monolog `FormatterInterface` 구현체를 설정하려고 할 수 있습니다.

시작하려면 채널 구성에 `tap` 배열을 정의하세요. 이 배열은 Monolog 인스턴스가 생성된 후 설정을 수정(“tap” 작업)할 기회를 갖게 될 클래스 목록을 담습니다. 이 클래스들은 별도 디렉터리에 자유롭게 만들 수 있습니다.

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
],
```

`tap` 옵션을 설정한 뒤, Monolog 인스턴스를 사용자 정의할 단일 `__invoke` 메서드를 가진 클래스를 정의하세요. 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 받으며, 이것은 실제 Monolog 인스턴스로의 모든 메서드 호출을 대리합니다:

```
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
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/10.x/container)로부터 자동으로 의존성 주입을 받아 생성됩니다. 따라서 생성자 의존성도 함께 자동 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 제공합니다만, Laravel은 그 모든 핸들러별 내장 채널을 제공하지는 않습니다. 특정 Monolog 핸들러 인스턴스를 그대로 사용하는 커스텀 채널이 필요하다면 `monolog` 드라이버를 활용하면 쉽게 생성할 수 있습니다.

`monolog` 드라이버를 사용할 때, 생성할 핸들러 클래스를 `handler` 옵션으로 지정합니다. 생성자 인자가 필요한 경우 `with` 옵션을 통해 지정하세요:

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
#### Monolog 포매터 설정

`monolog` 드라이버에서는 기본적으로 Monolog의 `LineFormatter`가 선택됩니다. 하지만 `formatter`와 `formatter_with` 옵션을 사용하여 핸들러에 적용할 포매터 종류와 설정을 커스텀할 수 있습니다:

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

만약 핸들러가 자체 포매터를 제공하는 경우라면, `formatter` 옵션에 `'default'`를 지정할 수 있습니다:

```
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog는 로그를 기록하기 전에 메시지를 가공할 수도 있습니다. 직접 프로세서를 만들거나 [기존 Monolog 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 활용할 수도 있습니다.

`monolog` 드라이버 채널에 프로세서를 적용하려면, 채널 설정에 `processors` 옵션을 추가하세요:

```
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 문법
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션 포함
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog 인스턴스 생성과 설정을 완전히 직접 제어하는 완전한 커스텀 채널을 정의하려면, `config/logging.php`에서 `custom` 드라이버 유형과 생성자 클래스를 명시할 수 있습니다. `via` 옵션에는 Monolog 인스턴스를 생성할 팩토리 클래스명을 적습니다:

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 채널을 구성한 후에는, Monolog 인스턴스를 생성하는 `__invoke` 메서드만 가진 클래스를 정의하세요. 이 메서드는 채널 설정 배열을 인수로 받고 Monolog `Logger` 인스턴스를 반환하면 됩니다:

```
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
## Pail을 사용한 로그 메시지 실시간 확인 (Tailing)

애플리케이션 로그를 실시간으로 확인해야 할 때가 많습니다. 예를 들어 버그를 찾거나 특정 오류 유형을 모니터링할 때 그렇습니다.

Laravel Pail은 명령줄에서 Laravel 애플리케이션의 로그 파일을 쉽게 확인할 수 있는 패키지입니다. 표준 `tail` 명령어와 달리 Pail은 Sentry, Flare 같은 다양한 로그 드라이버와도 호환됩니다. 또한 필요한 로그를 신속히 찾도록 다양한 유용한 필터 기능도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]  
> Laravel Pail은 [PHP 8.2+](https://php.net/releases/) 및 [PCNTL 확장](https://www.php.net/manual/en/book.pcntl.php)을 필요로 합니다.

프로젝트에 Composer 패키지로 Pail을 추가하세요:

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 실시간 확인을 시작하려면 `pail` 명령을 실행하세요:

```bash
php artisan pail
```

출력 수를 늘리고 생략부호 (…)를 없애려면 `-v` 옵션을 붙여 실행하세요:

```bash
php artisan pail -v
```

가장 상세한 출력과 예외 스택 트레이스를 보고 싶다면 `-vv` 옵션을 사용하세요:

```bash
php artisan pail -vv
```

실시간 확인을 중지하려면 언제든 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

로그 타입, 파일, 메시지, 스택 트레이스 내용을 기준으로 필터링할 때 사용합니다:

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지만으로 필터링하려면 `--message` 옵션을 씁니다:

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

[로그 레벨](#log-levels)로 필터링하려면 `--level` 옵션을 사용하세요:

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 동안 작성된 로그만 보고 싶을 때는 사용자 ID를 `--user` 옵션에 넘기면 됩니다:

```bash
php artisan pail --user=1
```