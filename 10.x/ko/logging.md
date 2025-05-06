# 로깅

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 생성](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널을 위한 Monolog 커스터마이즈](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 만들기](#creating-monolog-handler-channels)
    - [팩토리로 커스텀 채널 만들기](#creating-custom-channels-via-factories)
- [Pail을 사용한 실시간 로그 감시](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션에서 어떤 일이 일어나고 있는지 쉽게 알 수 있도록, Laravel은 강력한 로깅 서비스를 제공하며 메시지를 파일, 시스템 오류 로그, 혹은 Slack으로 기록하여 전체 팀에게 알릴 수 있습니다.

Laravel의 로깅은 "채널" 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방법을 나타냅니다. 예를 들어, `single` 채널은 단일 로그 파일로 로그 메시지를 기록하고, `slack` 채널은 Slack으로 로그 메시지를 전송합니다. 로그 메시지는 심각도(severity)에 따라 여러 채널에 동시에 기록될 수 있습니다.

Laravel은 내부적으로 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. 이는 다양한 강력한 로그 핸들러를 지원하며, Laravel에서는 이 핸들러들을 간단하게 구성할 수 있어 애플리케이션의 로그 핸들링을 손쉽게 커스터마이즈할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작에 대한 모든 설정 옵션은 `config/logging.php` 파일에 들어 있습니다. 이 파일에서 애플리케이션의 로그 채널을 구성할 수 있으므로, 사용 가능한 각 채널과 옵션을 반드시 확인하시기 바랍니다. 아래에서 몇 가지 일반적인 옵션들을 살펴보겠습니다.

기본적으로, Laravel은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 합치는 역할을 합니다. 스택 생성에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog은 현재 환경(`production` 또는 `local` 등)에 맞는 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면, 채널 설정에 `name` 옵션을 추가하면 됩니다:

    'stack' => [
        'driver' => 'stack',
        'name' => 'channel-name',
        'channels' => ['single', 'slack'],
    ],

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 동작합니다. 드라이버는 로그 메시지를 어떻게, 어디에 기록할지를 결정합니다. 아래의 로그 채널 드라이버는 모든 Laravel 애플리케이션에서 사용 가능합니다. 대부분의 드라이버에 대한 항목이 이미 `config/logging.php` 파일에 있으니, 이 파일의 내용을 꼭 확인하세요.

<div class="overflow-auto">

이름 | 설명
------------- | -------------
`custom` | 지정한 팩토리를 호출하여 채널을 생성하는 드라이버
`daily` | 매일 회전되는 `RotatingFileHandler` 기반 Monolog 드라이버
`errorlog` | `ErrorLogHandler` 기반 Monolog 드라이버
`monolog` | 모든 지원되는 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버
`papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버
`single` | 단일 파일 또는 경로(`StreamHandler`) 기반 로그 채널
`slack` | `SlackWebhookHandler` 기반 Monolog 드라이버
`stack` | "멀티 채널" 채널 생성을 위한 래퍼
`syslog` | `SyslogHandler` 기반 Monolog 드라이버

</div>

> [!NOTE]  
> `monolog` 및 `custom` 드라이버에 대해 더 알고 싶다면 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="channel-prerequisites"></a>
### 채널 사전 조건

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single`과 `daily` 채널은 `bubble`, `permission`, `locking`라는 세 가지 선택적 설정 옵션을 가지고 있습니다.

<div class="overflow-auto">

옵션 | 설명 | 기본값
------------- | ------------- | -------------
`bubble` | 처리 후 메시지가 다른 채널로도 전달될지 여부 | `true`
`locking` | 로그 파일에 기록하기 전에 파일을 잠글지 여부 | `false`
`permission` | 로그 파일의 권한 설정 | `0644`

</div>

또한, `daily` 채널의 로그 파일 보관 정책도 `days` 옵션으로 설정할 수 있습니다:

<div class="overflow-auto">

옵션 | 설명 | 기본값
------------- | ----------------------------------- | -------------
`days` | 일일 로그 파일을 보관할 일수 | `7`

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정 옵션이 필요합니다. 이 값들은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 반드시 `url` 설정 옵션이 필요합니다. 이 URL은 Slack팀에 대해 [인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)으로 설정된 URL이어야 합니다.

기본적으로 Slack은 `critical` 레벨 이상인 로그만 받습니다. 필요에 따라, `config/logging.php` 내의 Slack 채널 배열에서 `level` 옵션을 수정하여 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel, 기타 라이브러리는 일부 기능이 더 이상 지원되지 않으며 이후 버전에서 제거될 예정임을 경고합니다. 이러한 사용 중단(Deprecated) 경고를 로깅하고 싶다면, `config/logging.php` 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다.

    'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

    'channels' => [
        ...
    ]

또한, `deprecations`라는 이름의 로그 채널을 직접 정의할 수도 있습니다. 이 이름의 로그 채널이 있으면, 항상 사용 중단 기록에 이 채널이 사용됩니다:

    'channels' => [
        'deprecations' => [
            'driver' => 'single',
            'path' => storage_path('logs/php-deprecation-warnings.log'),
        ],
    ],

<a name="building-log-stacks"></a>
## 로그 스택 생성

앞서 언급한 것처럼, `stack` 드라이버를 이용하면 여러 채널을 하나의 로그 채널로 합칠 수 있습니다. 실전 환경에서 사용할 수 있는 예시 설정을 살펴보겠습니다:

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

이 설정을 살펴보면, `stack` 채널이 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 모읍니다. 따라서 메시지가 기록될 때, 두 채널 모두 로그를 기록할 수 있게 됩니다. 하지만 실제로 로그가 기록되는지는 메시지의 심각도(레벨)에 따라 다를 수 있습니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서, `syslog`와 `slack` 채널 설정에 `level` 옵션이 있습니다. 이 옵션은 채널에 로그를 기록하기 위한 메시지의 최소 "레벨"을 지정합니다. Laravel의 로그 서비스의 기반인 Monolog은 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 제공합니다. 심각도 순으로는: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

예를 들어, 다음과 같이 `debug` 메소드로 로그를 남긴다고 가정해봅시다:

    Log::debug('An informational message.');

이 경우, 예시 설정상 `syslog` 채널은 메시지를 기록하지만, `critical` 이상이 아니므로 Slack에는 전송되지 않습니다. 하지만, 만약 `emergency` 메시지를 기록하면 두 채널 모두 메시지를 기록하게 됩니다:

    Log::emergency('The system is down!');

<a name="writing-log-messages"></a>
## 로그 메시지 작성

로그에 정보를 기록하려면 `Log` [파사드](/docs/{{version}}/facades)를 사용하세요. 앞서 언급했듯, 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 여덟 가지 로그 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**

    use Illuminate\Support\Facades\Log;

    Log::emergency($message);
    Log::alert($message);
    Log::critical($message);
    Log::error($message);
    Log::warning($message);
    Log::notice($message);
    Log::info($message);
    Log::debug($message);

이 중 하나의 메소드를 호출해 해당 레벨로 메시지를 기록할 수 있습니다. 기본적으로 메시지는 `logging` 설정 파일에서 지정한 기본 로그 채널에 기록됩니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
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

<a name="contextual-information"></a>
### 컨텍스트 정보

배열 형태의 컨텍스트 데이터를 로그 메소드에 함께 전달할 수 있습니다. 이 데이터는 로그 메시지와 함께 포맷팅되어 출력됩니다:

    use Illuminate\Support\Facades\Log;

    Log::info('User {id} failed to login.', ['id' => $user->id]);

특정 채널에서 이후 기록되는 모든 로그에 포함될 컨텍스트 정보를 미리 지정하고 싶은 경우도 있습니다. 예를 들어, 각 요청마다 request ID를 로그에 포함시키려면, `Log` 파사드의 `withContext` 메소드를 사용하세요.

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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하고 싶다면 `Log::shareContext()` 메소드를 사용할 수 있습니다. 이 메소드는 모든 기존 및 새로 생성되는 채널에 컨텍스트 데이터를 제공합니다:

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

> [!NOTE]
> 큐 작업을 처리하면서 로그 컨텍스트를 공유해야 한다면, [작업 미들웨어](/docs/{{version}}/queues#job-middleware)를 사용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기

기본 로그 채널이 아닌 다른 채널에 메시지를 기록하려면, `Log` 파사드의 `channel` 메소드를 사용해 설정 파일에 정의된 원하는 채널을 받아와 로그를 기록할 수 있습니다.

    use Illuminate\Support\Facades\Log;

    Log::channel('slack')->info('Something happened!');

여러 채널을 임시 스택으로 묶어서 사용하는 경우, `stack` 메소드를 사용하세요:

    Log::stack(['single', 'slack'])->info('Something happened!');

<a name="on-demand-channels"></a>
#### 온디맨드(즉시 생성) 채널

설정 파일에 미리 정의되지 않은 채널을 런타임에서 즉시 생성하고 싶은 경우, `Log` 파사드의 `build` 메소드에 설정 배열을 전달하면 됩니다:

    use Illuminate\Support\Facades\Log;

    Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ])->info('Something happened!');

온디맨드 채널을 온디맨드 스택에도 포함시킬 수 있습니다. 즉시 생성한 채널 인스턴스를 `stack` 메소드 배열에 넣으면 됩니다:

    use Illuminate\Support\Facades\Log;

    $channel = Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ]);

    Log::stack(['slack', $channel])->info('Something happened!');

<a name="monolog-channel-customization"></a>
## Monolog 채널 커스터마이징

<a name="customizing-monolog-for-channels"></a>
### 채널을 위한 Monolog 커스터마이즈

기존 채널에 대해 Monolog의 설정 전체를 직접 제어해야 할 경우도 있습니다. 예를 들어, Laravel 기본 `single` 채널에 사용자 정의 Monolog `FormatterInterface`를 사용하고 싶을 때가 있습니다.

이를 위해, 해당 채널 설정에 `tap` 배열을 정의합니다. `tap` 배열에는 Monolog 인스턴스가 생성된 뒤 후처리를 할 수 있는 클래스들을 나열합니다. 이 클래스들은 임의의 디렉터리에 자유롭게 생성할 수 있습니다:

    'single' => [
        'driver' => 'single',
        'tap' => [App\Logging\CustomizeFormatter::class],
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
    ],

이제 `tap` 옵션에서 지정한 클래스를 정의하세요. 이 클래스에는 `Illuminate\Log\Logger` 인스턴스를 받는 `__invoke` 메소드만 있으면 됩니다. 모든 메소드 호출은 Monolog 인스턴스로 위임됩니다.

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

> [!NOTE]  
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)로 해석되므로, 생성자 의존성이 있을 경우 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 만들기

Monolog은 매우 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 제공하지만, Laravel이 모든 핸들러용 채널을 내장하고 있지는 않습니다. 특정 Monolog 핸들러 인스턴스를 사용하는 커스텀 채널을 만들고 싶다면, `monolog` 드라이버를 사용하세요.

`monolog` 드라이버를 사용할 때는, `handler` 설정 옵션으로 인스턴스화할 핸들러를 지정하면 됩니다. 핸들러에 생성자 인자가 필요하다면, `with` 옵션에 추가할 수 있습니다.

    'logentries' => [
        'driver'  => 'monolog',
        'handler' => Monolog\Handler\SyslogUdpHandler::class,
        'with' => [
            'host' => 'my.logentries.internal.datahubhost.company.com',
            'port' => '10000',
        ],
    ],

<a name="monolog-formatters"></a>
#### Monolog 포매터

`monolog` 드라이버를 사용할 때는 기본적으로 Monolog의 `LineFormatter`가 적용됩니다. 하지만 `formatter`와 `formatter_with` 설정 옵션으로 핸들러에 전달되는 포매터 타입을 커스터마이즈할 수 있습니다.

    'browser' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\BrowserConsoleHandler::class,
        'formatter' => Monolog\Formatter\HtmlFormatter::class,
        'formatter_with' => [
            'dateFormat' => 'Y-m-d',
        ],
    ],

별도의 포매터를 제공하는 Monolog 핸들러를 사용할 경우, `formatter` 설정 값을 `default`로 지정해도 됩니다.

    'newrelic' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\NewRelicHandler::class,
        'formatter' => 'default',
    ],


 <a name="monolog-processors"></a>
 #### Monolog 프로세서

 Monolog은 로그를 남기기 전에 메시지를 처리할 수 있습니다. 직접 프로세서를 만들거나 [Monolog이 제공하는 기존 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

 `monolog` 드라이버의 프로세서를 커스터마이즈하려면, 채널 설정에 `processors` 옵션을 추가하세요.

     'memory' => [
         'driver' => 'monolog',
         'handler' => Monolog\Handler\StreamHandler::class,
         'with' => [
             'stream' => 'php://stderr',
         ],
         'processors' => [
             // 간단한 문법...
             Monolog\Processor\MemoryUsageProcessor::class,

             // 옵션이 필요한 경우...
             [
                'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
                'with' => ['removeUsedContextFields' => true],
            ],
         ],
     ],


<a name="creating-custom-channels-via-factories"></a>
### 팩토리로 커스텀 채널 만들기

Monolog 인스턴스 생성과 설정을 완전히 직접 제어하는 채널을 만들고 싶다면, `config/logging.php`의 드라이버 타입을 `custom`으로 지정하세요. 그리고 `via` 옵션에 Monolog 인스턴스를 생성할 팩토리 클래스명을 입력합니다.

    'channels' => [
        'example-custom-channel' => [
            'driver' => 'custom',
            'via' => App\Logging\CreateCustomLogger::class,
        ],
    ],

이제, 이 팩토리 클래스에 `__invoke` 메소드를 만들어서 Monolog 인스턴스를 반환하도록 합니다. 이때, 메소드는 해당 채널의 설정 배열을 인자로 받습니다:

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

<a name="tailing-log-messages-using-pail"></a>
## Pail을 사용한 실시간 로그 감시

애플리케이션의 로그를 실시간으로 살펴봐야 할 때가 종종 있습니다. 예를 들어, 문제를 디버깅하거나 특정 오류를 모니터링할 때가 그렇습니다.

Laravel Pail은 터미널에서 직접 Laravel 애플리케이션의 로그 파일을 간편하게 조회할 수 있는 패키지입니다. 표준 `tail` 명령과 달리, Pail은 Sentry, Flare 등 어떤 로그 드라이버와도 작동하도록 설계되어 있습니다. 또한, 원하는 로그를 빠르게 찾을 수 있는 유용한 필터 기능들도 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### 설치

> [!WARNING]  
> Laravel Pail은 [PHP 8.2+](https://php.net/releases/) 및 [PCNTL 확장](https://www.php.net/manual/en/book.pcntl.php)을 필요로 합니다.

Composer 패키지 매니저로 Pail을 프로젝트에 설치하세요:

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
### 사용법

실시간 로그 감시를 시작하려면, 다음 명령을 실행하세요:

```bash
php artisan pail
```

출력의 상세 레벨을 높이고 줄임표(…) 없이 모두 표시하려면, `-v` 옵션을 사용하세요:

```bash
php artisan pail -v
```

가장 상세하게(스택 트레이스까지) 표시하려면, `-vv` 옵션을 사용하세요:

```bash
php artisan pail -vv
```

실시간 로그 감시를 중단하려면 언제든지 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

로그의 타입, 파일, 메시지, 스택트레이스 내용으로 필터링하려면 `--filter` 옵션을 사용할 수 있습니다:

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

로그 메시지 내용만을 기준으로 필터링하려면, `--message` 옵션을 사용하세요:

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` 옵션을 이용해 [로그 레벨](#log-levels)로 필터링할 수 있습니다:

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 보고 싶다면, `--user` 옵션에 사용자 ID를 지정하세요:

```bash
php artisan pail --user=1
```
