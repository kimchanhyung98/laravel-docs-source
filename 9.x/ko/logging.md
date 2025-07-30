# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 조건](#channel-prerequisites)
    - [폐기 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구축하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 이용한 커스텀 채널 생성](#creating-custom-channels-via-factories)

<a name="introduction"></a>
## 소개

애플리케이션 내부에서 어떤 일이 발생하는지 더 잘 파악할 수 있도록, Laravel은 파일, 시스템 에러 로그, 심지어 Slack 알림을 통해 팀 전체에 알릴 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel의 로깅은 "채널"을 기반으로 작동합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 의미합니다. 예를 들어, `single` 채널은 로그를 단일 파일에 기록하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 기록될 수 있습니다.

내부적으로 Laravel은 다양한 강력한 로그 핸들러를 제공하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. Laravel은 이러한 핸들러를 간단하게 설정할 수 있게 해 주어, 여러 핸들러를 조합해 애플리케이션의 로그 처리를 맞춤화할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작에 대한 모든 설정 옵션은 `config/logging.php` 파일에 있습니다. 이 파일을 통해 애플리케이션의 로그 채널을 구성할 수 있으므로, 사용 가능한 채널과 각 옵션을 꼼꼼히 살펴보아야 합니다. 아래에서는 몇 가지 일반적인 옵션을 설명합니다.

기본적으로 Laravel은 메시지를 로깅할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 만드는 법에 대해서는 [아래 문서](#building-log-stacks)를 참조하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정하기

기본적으로 Monolog 인스턴스는 현재 환경(`production`, `local` 등)과 동일한 "채널 이름"을 가집니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하세요:

```
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"로 동작합니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록되는지를 결정합니다. 다음은 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버 목록입니다. 대부분의 드라이버 설정은 `config/logging.php` 파일에 이미 존재하므로, 내용을 잘 숙지하는 것이 좋습니다:

| 이름          | 설명                                                         |
| ------------- | ------------------------------------------------------------ |
| `custom`      | 지정한 팩토리를 호출해 채널을 생성하는 드라이버             |
| `daily`       | 매일 로그 파일을 회전하는 `RotatingFileHandler` 기반 드라이버 |
| `errorlog`    | `ErrorLogHandler` 기반 드라이버                             |
| `monolog`     | Monolog 핸들러 중 하나를 사용할 수 있는 팩토리 드라이버     |
| `null`        | 모든 로그 메시지를 무시하는 드라이버                         |
| `papertrail`  | `SyslogUdpHandler` 기반 드라이버                             |
| `single`      | 단일 파일(또는 경로)에 기록하는 채널 (`StreamHandler`)       |
| `slack`       | `SlackWebhookHandler` 기반 드라이버                         |
| `stack`       | 여러 채널을 하나로 묶기 위한 래퍼                            |
| `syslog`      | `SyslogHandler` 기반 드라이버                               |

> [!NOTE]
> `monolog` 및 `custom` 드라이버를 더 자세히 알고 싶다면 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="channel-prerequisites"></a>
### 채널 사전 조건

<a name="configuring-the-single-and-daily-channels"></a>
#### single 및 daily 채널 설정하기

`single` 및 `daily` 채널은 `bubble`, `permission`, `locking` 세 가지 선택적 설정을 가질 수 있습니다.

| 이름         | 설명                                      | 기본값      |
| ------------ | ----------------------------------------- | ---------- |
| `bubble`     | 처리 후 메시지가 다른 채널로 전달될지 여부 | `true`     |
| `locking`    | 기록 전에 로그 파일을 잠글지 여부           | `false`    |
| `permission` | 로그 파일의 권한 (퍼미션) 설정              | `0644`     |

또한, `daily` 채널의 로그 보관 기간은 `days` 옵션으로 설정할 수 있습니다:

| 이름   | 설명                                            | 기본값  |
| ------ | ----------------------------------------------- | ------- |
| `days` | 일일 로그 파일을 보관할 일수                      | `7`     |

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정하기

`papertrail` 채널은 `host`와 `port` 옵션이 필요합니다. 이 값들은 [Papertrail 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정하기

`slack` 채널은 `url` 설정이 필요하며, 이 URL은 Slack 팀에 설정한 [인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 주소여야 합니다.

기본적으로 Slack에는 `critical` 레벨 이상의 로그만 전송됩니다. 그러나 `config/logging.php`의 Slack 채널 설정 배열 내 `level` 옵션을 수정하여 이 설정을 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 폐기 경고 로깅

PHP, Laravel, 기타 라이브러리는 자주 기능이 폐기(deprecated)되어 향후 버전에서 사라질 예정임을 사용자에게 알립니다. 이러한 폐기 경고를 로그로 기록하고 싶다면 애플리케이션의 `config/logging.php` 파일에서 `deprecations` 채널을 지정할 수 있습니다:

```
'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

'channels' => [
    ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 직접 정의할 수도 있습니다. 이 이름의 채널이 존재하면 폐기 로그를 항상 이 채널로 기록합니다:

```
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구축하기

앞서 언급했듯, `stack` 드라이버를 사용하면 여러 채널을 하나의 로그 채널로 묶어 편리하게 사용할 수 있습니다. 실제 운영 애플리케이션에서 볼 수 있는 예제 설정을 살펴봅시다:

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

이 설정을 살펴보면, `stack` 채널이 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 묶고 있음을 알 수 있습니다. 따라서 메시지를 로깅할 때 두 채널 모두 메시지를 기록하려 시도합니다. 다만, 아래에서 설명할 메시지의 심각도(레벨)에 따라 실제로 기록할지 결정됩니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예제에서 `syslog`와 `slack` 채널 설정에 `level` 옵션이 있습니다. 이 옵션은 로그 메시지가 해당 채널에 기록되기 위한 최소 레벨을 지정합니다. Laravel 로깅은 Monolog을 기반으로 하며, [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 지원합니다. 심각도 순서대로 로그 레벨은 다음과 같습니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

예를 들어, `debug` 레벨로 로그를 남기면:

```
Log::debug('An informational message.');
```

우리 설정에서는 `syslog` 채널이 이 메시지를 기록하지만, `slack` 채널은 `critical` 이상 레벨만 받으므로 기록하지 않습니다. 반면, `emergency` 레벨 메시지를 기록하면:

```
Log::emergency('The system is down!');
```

양쪽 채널 모두 이 메시지를 기록합니다. 왜냐하면 `emergency`가 두 채널의 최소 레벨 조건을 모두 만족하기 때문입니다.

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

로그 메시지는 `Log` [파사드](/docs/9.x/facades)를 사용해 기록할 수 있습니다. 앞서 설명한대로, RFC 5424에 정의된 여덟 가지 로깅 레벨을 지원합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**:

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

이 중 원하는 메서드를 호출해 해당 레벨의 로그 메시지를 작성할 수 있습니다. 기본적으로 메시지는 설정된 기본 로그 채널에 기록됩니다.

예시:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Support\Facades\Log;

class UserController extends Controller
{
    /**
     * 지정된 사용자 프로필을 보여줍니다.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        Log::info('Showing the user profile for user: '.$id);

        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<a name="contextual-information"></a>
### 컨텍스트 정보

로그 메서드에 컨텍스트 데이터를 배열 형태로 전달할 수 있습니다. 이 컨텍스트 데이터는 로그 메시지와 함께 포맷되어 표시됩니다:

```
use Illuminate\Support\Facades\Log;

Log::info('User failed to login.', ['id' => $user->id]);
```

종종 특정 채널에 후속 로그에 항상 포함할 컨텍스트 정보를 설정하고 싶을 때가 있습니다. 예를 들어, 들어오는 모든 요청에 연관된 요청 ID(request ID)를 로그에 남기려 한다면, `Log` 파사드의 `withContext` 메서드를 호출하면 됩니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;

class AssignRequestId
{
    /**
     * 요청을 처리합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        return $next($request)->header('Request-Id', $requestId);
    }
}
```

모든 로깅 채널에 걸쳐 공통 컨텍스트 정보를 공유하고 싶다면 `Log::shareContext()` 메서드를 사용할 수 있습니다. 해당 정보는 생성된 모든 채널 및 이후 생성될 채널에도 전달됩니다. 일반적으로 이 메서드는 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;

class AppServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩 메서드.
     *
     * @return void
     */
    public function boot()
    {
        Log::shareContext([
            'invocation-id' => (string) Str::uuid(),
        ]);
    }
}
```

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기

가끔 기본 로그 채널이 아닌 다른 채널에 메시지를 남기고 싶을 때가 있습니다. 이럴 땐 `Log` 파사드의 `channel` 메서드를 사용해 설정 파일에 정의된 채널에 접근할 수 있습니다:

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널을 묶은 로그 스택을 즉시 생성해 사용하고 싶다면 `stack` 메서드를 사용할 수도 있습니다:

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 즉석 채널 만들기

애플리케이션 설정 파일에 정의하지 않은 새 로그 채널을 즉석에서 생성할 수도 있습니다. 이런 경우 `Log` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다:

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

즉석 채널을 즉석 로그 스택에 포함할 수도 있습니다. 아래처럼 즉석 채널 인스턴스를 `stack` 메서드에 넘겨주면 됩니다:

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

기존 채널의 Monolog 설정을 완전히 제어해야 할 때가 있습니다. 예를 들어, Laravel의 기본 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현체를 적용하고자 한다면 다음 단계를 따릅니다.

먼저, 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열은 Monolog 인스턴스가 생성된 후 설정에 참여할 클래스 목록을 담습니다. 이 클래스들은 애플리케이션 내 아무 디렉터리에 자유롭게 만들면 됩니다:

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
],
```

이제 Monolog 인스턴스를 커스터마이징할 클래스를 정의합시다. 이 클래스는 단일 `__invoke` 메서드를 가져야 하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. `Illuminate\Log\Logger`는 내부 Monolog 인스턴스에 메서드를 프록시해 전달합니다:

```
<?php

namespace App\Logging;

use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 전달받은 로그 인스턴스를 커스터마이징합니다.
     *
     * @param  \Illuminate\Log\Logger  $logger
     * @return void
     */
    public function __invoke($logger)
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
> 모든 `tap` 클래스는 [서비스 컨테이너](/docs/9.x/container)를 통해 자동 해석되므로, 생성자에 필요한 의존성도 자동 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 [다양한 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있지만 Laravel은 모두를 기본 제공하지는 않습니다. 특정 Monolog 핸들러 인스턴스를 Laravel 로그 드라이버에 해당하는 커스텀 채널로 만들고 싶을 때 `monolog` 드라이버를 사용할 수 있습니다.

`monolog` 드라이버를 사용할 땐 `handler` 옵션으로 생성할 핸들러 클래스를 지정합니다. 필요하다면 핸들러 생성자에 전달할 인자를 `with` 옵션 배열로 지정할 수 있습니다:

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

`monolog` 드라이버 사용 시, 기본적으로 Monolog의 `LineFormatter`가 포매터로 적용됩니다. 그러나 `formatter` 옵션과 `formatter_with` 옵션을 사용해 핸들러에 전달될 포매터 종류와 옵션을 조정할 수 있습니다:

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

Monolog 핸들러가 자체 포매터를 제공한다면, `formatter` 옵션을 `default`로 지정할 수 있습니다:

```
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 이용한 커스텀 채널 생성

Monolog 인스턴스 생성과 설정 방식까지 완전히 제어하는 커스텀 로그 채널을 정의하고 싶다면, `config/logging.php` 설정에서 `custom` 드라이버 타입을 사용할 수 있습니다. 이 설정은 Monolog 인스턴스를 생성할 팩토리 클래스명을 `via` 옵션에 지정해야 합니다:

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

이제 Monolog 인스턴스를 생성하는 클래스를 정의합니다. 단일 `__invoke` 메서드만 있으면 되며, 이 메서드는 채널 설정 배열을 인자로 받고, Monolog `Logger` 인스턴스를 반환해야 합니다:

```
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * 커스텀 Monolog 인스턴스를 생성합니다.
     *
     * @param  array  $config
     * @return \Monolog\Logger
     */
    public function __invoke(array $config)
    {
        return new Logger(/* ... */);
    }
}
```