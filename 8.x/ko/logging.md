# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 전제 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 작성하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리로 커스텀 채널 생성하기](#creating-custom-channels-via-factories)

<a name="introduction"></a>
## 소개

애플리케이션에서 무슨 일이 벌어지는지 더 잘 이해할 수 있도록, Laravel은 파일, 시스템 에러 로그, 심지어 Slack까지 메시지를 기록할 수 있는 강력한 로깅 서비스를 제공합니다. 이를 통해 팀 전체에 알림을 보낼 수 있습니다.

Laravel 로깅은 "채널"을 기반으로 합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 로그 파일에 기록하는 반면, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 중요도에 따라 로그 메시지를 여러 채널에 기록할 수도 있습니다.

내부적으로 Laravel은 다양한 강력한 로그 핸들러를 제공하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. Laravel은 이 핸들러들을 손쉽게 구성할 수 있도록 하며, 여러 핸들러를 조합해 애플리케이션의 로그 처리 방식을 자유롭게 맞춤화할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작과 관련된 모든 설정 옵션은 `config/logging.php` 설정 파일에 있습니다. 이 파일을 통해 애플리케이션의 로그 채널들을 설정할 수 있으므로, 사용 가능한 각 채널과 옵션을 꼭 살펴보세요. 다음은 몇 가지 일반적인 옵션입니다.

기본적으로 Laravel은 로그 메시지 기록 시 `stack` 채널을 사용합니다. 이 `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 빌드에 관한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경 이름(`production`, `local` 등)과 일치하는 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하세요:

```
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 구동됩니다. 드라이버는 로그 메시지를 실제로 어떻게, 어디에 기록할지 결정합니다. 다음은 모든 Laravel 애플리케이션에 기본으로 포함된 로그 채널 드라이버 목록입니다. 대부분의 드라이버 항목이 이미 `config/logging.php` 파일에 정의되어 있으므로 내용을 꼭 검토하세요:

| 이름 | 설명 |
| ------------- | ------------- |
| `custom` | 지정한 팩토리를 호출해 채널을 생성하는 드라이버 |
| `daily` | 매일 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버 |
| `errorlog` | `ErrorLogHandler` 기반 Monolog 드라이버 |
| `monolog` | 모든 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버 |
| `null` | 모든 로그 메시지를 버리는 드라이버 |
| `papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버 |
| `single` | 단일 파일 또는 경로 기반 로그 채널 (`StreamHandler`) |
| `slack` | `SlackWebhookHandler` 기반 Monolog 드라이버 |
| `stack` | 여러 채널을 묶어주는 래퍼 |
| `syslog` | `SyslogHandler` 기반 Monolog 드라이버 |

> [!TIP]  
> `monolog` 및 `custom` 드라이버에 대해 더 상세히 알고 싶다면 [고급 채널 커스터마이징 문서](#monolog-channel-customization)를 참고하세요.

<a name="channel-prerequisites"></a>
### 채널 전제 조건

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널에는 `bubble`, `permission`, `locking` 세 가지 선택적 설정 옵션이 있습니다.

| 이름 | 설명 | 기본값 |
| ------------- | ------------- | ------------- |
| `bubble` | 메시지가 처리 후 다른 채널로 전파되는지 여부 | `true` |
| `locking` | 쓰기 전 로그 파일 잠금 시도 여부 | `false` |
| `permission` | 로그 파일 권한 | `0644` |

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정이 필요합니다. 해당 값은 [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 설정값이 필요합니다. 이 URL은 Slack 팀에 맞춰 설정한 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) URL이어야 합니다.

기본적으로 Slack은 `critical` 등급 이상의 로그만 수신합니다. 다만, Slack 로그 채널 설정 배열 내의 `level` 옵션을 수정해 이 동작을 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel, 그리고 타 라이브러리들은 종종 일부 기능이 사용 중단(deprecated)되어 이후 버전에서 제거될 예정임을 알립니다. 이런 사용 중단 경고를 로그로 남기고 싶다면 `config/logging.php` 파일에서 선호하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```
'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

'channels' => [
    ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 정의할 수도 있습니다. 만약 해당 이름의 채널이 존재하면, 항상 사용 중단 경고를 기록할 때 이 채널이 사용됩니다:

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

앞서 언급했듯이 `stack` 드라이버를 사용하면 여러 채널을 하나의 로그 채널로 묶을 수 있어 편리합니다. 실제 운영 환경에서 볼 수 있는 예시 설정은 다음과 같습니다:

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

구성을 살펴보면, `stack` 채널이 두 개의 채널 `syslog`와 `slack`을 `channels` 옵션으로 묶고 있습니다. 따라서 로그 메시지가 기록될 때 두 채널 모두 메시지를 기록할 기회를 갖습니다. 다만, 아래에 설명할 메시지 심각도(레벨)에 따라 실제 로그 기록 여부가 결정될 수 있습니다.

<a name="log-levels"></a>
#### 로그 레벨

예제에서 `syslog`와 `slack` 채널 설정에 `level` 옵션이 있는 점을 주목하세요. 이 옵션은 채널이 로그를 기록하기 위한 최소 레벨을 지정합니다. Laravel 로깅 서비스를 제공하는 Monolog는 [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에 정의된 다음 8가지 로그 레벨을 지원합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

예를 들어, `debug` 메서드로 로그를 기록하면:

```
Log::debug('An informational message.');
```

설정 상 `syslog` 채널은 시스템 로그에 메시지를 남깁니다. 하지만 메시지 레벨이 `critical` 이상이 아니기 때문에 Slack으로는 전송되지 않습니다. 반대로 심각한 `emergency` 메시지를 기록하면:

```
Log::emergency('The system is down!');
```

`emergency` 레벨이 두 채널 모두의 최소 레벨 기준치를 충족하므로, 시스템 로그와 Slack 둘 다에 메시지가 기록됩니다.

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

로그 정보는 `Log` [파사드](/docs/{{version}}/facades)를 통해 기록할 수 있습니다. 앞서 언급했듯이, 로그 레벨은 [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에 정의된 여덟 가지를 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

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

해당 메서드들을 호출해 대응하는 레벨의 메시지를 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에 지정된 기본 로그 채널로 기록됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Support\Facades\Log;

class UserController extends Controller
{
    /**
     * 지정한 사용자의 프로필을 보여줍니다.
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

로그 메서드에 컨텍스트 배열을 전달할 수 있습니다. 이 배열은 로그 메시지와 함께 포맷되어 표시됩니다:

```
use Illuminate\Support\Facades\Log;

Log::info('User failed to login.', ['id' => $user->id]);
```

때로는 모든 후속 로그 항목에 포함될 컨텍스트 정보를 지정하고 싶을 수 있습니다. 예를 들어, 애플리케이션으로 들어오는 각 요청에 연결된 요청 ID를 모든 로그에 남기려 할 때, `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;

class AssignRequestId
{
    /**
     * 들어오는 요청을 처리합니다.
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

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기

애플리케이션 기본 채널이 아닌 다른 채널에 로그를 기록하고 싶을 때가 있습니다. `Log` 파사드의 `channel` 메서드를 사용해 설정 파일에 정의한 특정 채널을 선택하여 로그를 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널로 이루어진 즉석 스택을 만들고 싶을 때는 `stack` 메서드를 사용할 수 있습니다:

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 즉석 채널

애플리케이션의 설정 파일에 정의되지 않은 구성을 런타임에 제공해 즉석에서 채널을 만들 수도 있습니다. 이때는 `Log` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다:

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

즉석 채널 인스턴스를 즉석 로그 스택에 포함시키고 싶다면 다음과 같이 `stack` 메서드에 전달하면 됩니다:

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

기존 채널의 Monolog 설정을 완전히 제어해야 할 때가 있습니다. 예를 들어 Laravel의 기본 `single` 채널에 사용자 정의 Monolog `FormatterInterface` 구현체를 적용하고 싶을 수 있습니다.

먼저, 채널 설정에 `tap` 배열을 정의하세요. 이 배열은 Monolog 인스턴스가 생성된 후 이를 커스터마이즈(또는 "탭")할 클래스 목록을 포함해야 합니다. 이 클래스들은 특별한 위치에 둘 필요 없으며, 원하는 디렉터리를 만들어 자유롭게 관리할 수 있습니다:

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
],
```

`tap` 옵션 설정 후에는 Monolog 인스턴스를 커스터마이징할 클래스를 정의하세요. 이 클래스는 단일 메서드 `__invoke`만 필요하며, `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. 이 인스턴스는 내부 Monolog 인스턴스로 모든 메서드 호출을 프록시합니다:

```php
<?php

namespace App\Logging;

use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 주어진 로거 인스턴스를 커스터마이징합니다.
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

> [!TIP]  
> 모든 `tap` 클래스는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 생성자 의존성이 자동 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 제공하지만, Laravel이 모두를 기본 채널로 포함하진 않습니다. 때로는 Laravel 로그 드라이버에 없는 특정 Monolog 핸들러 인스턴스로만 구성된 커스텀 채널을 만들고 싶을 수 있습니다. 이런 채널은 `monolog` 드라이버로 쉽게 만들 수 있습니다.

`monolog` 드라이버를 사용할 때, `handler` 옵션에 생성할 핸들러 클래스를 지정합니다. 선택적으로 핸들러의 생성자 파라미터를 `with` 옵션으로 넘길 수 있습니다:

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

`monolog` 드라이버 사용 시 기본 포매터는 Monolog `LineFormatter`입니다. 하지만 `formatter`와 `formatter_with` 옵션으로 핸들러에 전달할 포매터 종류와 설정을 커스터마이징할 수 있습니다:

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

자체 포매터를 제공할 수 있는 Monolog 핸들러를 사용하는 경우, `formatter` 옵션 값을 `default`로 지정할 수 있습니다:

```
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog 인스턴스 생성과 구성에 완전한 제어권을 갖는 완전한 커스텀 채널을 만들고 싶다면, `config/logging.php`에서 `custom` 드라이버 타입을 지정하세요. 설정 배열에 Monolog 인스턴스를 생성할 팩토리 클래스 이름을 담은 `via` 옵션을 포함해야 합니다:

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버를 설정한 뒤에는 Monolog 인스턴스를 생성할 클래스를 정의합니다. 이 클래스는 `__invoke` 메서드 하나만 필요하며, 해당 메서드는 Monolog 로거 인스턴스를 반환해야 합니다. 메서드는 채널 설정 배열을 인자로 받습니다:

```php
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
        return new Logger(...);
    }
}
```