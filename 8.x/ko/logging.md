# 로깅

- [소개](#introduction)
- [구성](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 준비 사항](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 빌드하기](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 작성하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성](#creating-custom-channels-via-factories)

<a name="introduction"></a>
## 소개

애플리케이션에서 무슨 일이 일어나고 있는지 더 잘 파악할 수 있도록, Laravel은 강력한 로깅 서비스를 제공합니다. 이를 통해 메시지를 파일, 시스템 에러 로그, 또는 Slack 등으로 기록하여 팀 전체에 알릴 수 있습니다.

Laravel의 로깅은 "채널(channel)"을 기반으로 동작합니다. 각 채널은 로그 정보를 쓰는 특정 방법을 나타냅니다. 예를 들어, `single` 채널은 단일 로그 파일에 기록하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

Laravel은 내부적으로 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하며, 다양한 강력한 로그 핸들러를 지원합니다. Laravel에서는 이러한 핸들러를 손쉽게 설정할 수 있어, 애플리케이션의 로그 처리 방식을 자유롭게 맞춤화할 수 있습니다.

<a name="configuration"></a>
## 구성

애플리케이션의 로깅 동작에 대한 모든 구성 옵션은 `config/logging.php` 파일에 정의되어 있습니다. 이 파일을 통해 애플리케이션의 로그 채널을 구성할 수 있으니, 각 채널과 그 옵션을 반드시 검토하시기 바랍니다. 아래에서는 몇 가지 일반적인 옵션을 살펴봅니다.

Laravel은 기본적으로 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택 구성에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경(`production`, `local` 등)과 동일한 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하려면, 채널 설정에 `name` 옵션을 추가하면 됩니다.

    'stack' => [
        'driver' => 'stack',
        'name' => 'channel-name',
        'channels' => ['single', 'slack'],
    ],

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 동작합니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록될지 결정합니다. 다음은 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버입니다. 대부분의 드라이버는 이미 `config/logging.php` 파일에 항목이 있으니, 이 파일을 꼼꼼히 살펴보시기 바랍니다.

이름 | 설명
------------- | -------------
`custom` | 지정된 팩토리를 호출하여 채널을 생성하는 드라이버
`daily` | 매일 로그 파일을 교체하는 `RotatingFileHandler` 기반 Monolog 드라이버
`errorlog` | `ErrorLogHandler` 기반 Monolog 드라이버
`monolog` | 모든 지원되는 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버
`null` | 모든 로그 메시지를 무시하는 드라이버
`papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버
`single` | 단일 파일(또는 경로)에 기록하는 채널 (`StreamHandler`)
`slack` | `SlackWebhookHandler` 기반 Monolog 드라이버
`stack` | "다중 채널" 채널 생성을 용이하게 하는 래퍼
`syslog` | `SyslogHandler` 기반 Monolog 드라이버

> {tip} `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="channel-prerequisites"></a>
### 채널 사전 준비 사항

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널에는 선택적 구성 옵션이 세 가지 있습니다: `bubble`, `permission`, `locking`.

이름 | 설명 | 기본값
------------- | ------------- | -------------
`bubble` | 메시지 처리가 끝난 후 다른 채널로 버블업할지 여부 | `true`
`locking` | 기록 전 로그 파일 잠금 시도 | `false`
`permission` | 로그 파일의 권한 설정 | `0644`

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 구성 옵션이 필요합니다. 이 값은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 구성 옵션이 필요합니다. 이 URL은 Slack 팀용으로 설정된 [Incoming Webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)의 URL이어야 합니다.

기본적으로 Slack은 `critical` 레벨 이상의 로그만 수신합니다. 하지만, `config/logging.php` 파일에서 Slack 로그 채널의 구성 배열에 있는 `level` 옵션을 수정하여 조절할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단(deprecation) 경고 로깅

PHP, Laravel 및 기타 라이브러리에서는 기능이 더 이상 지원되지 않을 예정임을 알리는 사용 중단 경고를 제공합니다. 이러한 사용 중단 경고 로그를 남기고 싶다면, 애플리케이션의 `config/logging.php` 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다:

    'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

    'channels' => [
        ...
    ]

또는, `deprecations`라는 이름의 로그 채널을 직접 정의할 수도 있습니다. 이 이름으로 된 로그 채널이 존재하면, 항상 deprecation 로그에 사용됩니다:

    'channels' => [
        'deprecations' => [
            'driver' => 'single',
            'path' => storage_path('logs/php-deprecation-warnings.log'),
        ],
    ],

<a name="building-log-stacks"></a>
## 로그 스택 빌드하기

앞서 언급한 것처럼, `stack` 드라이버를 사용하면 여러 채널을 하나의 로그 채널로 결합할 수 있습니다. 다음은 실제 운영 환경에서 볼 수 있는 예시 구성입니다:

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

이 구성을 분석해봅시다. 먼저, `stack` 채널의 `channels` 옵션을 통해 `syslog`, `slack` 두 가지 채널을 집계(aggregate)합니다. 따라서 로그 메시지가 기록될 때 두 채널 모두 해당 메시지를 기록할 기회를 갖게 됩니다. 하지만 실제로 어느 채널에서 로그를 기록할지는 메시지의 심각도/레벨에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 구성에 있는 `level` 옵션에 주목하세요. 이 옵션은 메시지가 해당 채널에 기록되기 위한 최소 "레벨"을 결정합니다. Laravel의 로깅 서비스를 지원하는 Monolog는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

예를 들어, `debug` 메서드로 메시지를 기록한다고 가정해보겠습니다.

    Log::debug('An informational message.');

이 경우, 구성에 따라 `syslog` 채널은 메시지를 시스템 로그에 기록하지만, 이 에러가 `critical` 이상이 아니므로 Slack에는 전송되지 않습니다. 반면, `emergency` 메시지를 기록하면 해당 수준이 모든 채널의 최소 레벨보다 높으므로 시스템 로그와 Slack 모두에 전송됩니다:

    Log::emergency('The system is down!');

<a name="writing-log-messages"></a>
## 로그 메시지 작성

`Log` [파사드](/docs/{{version}}/facades)를 사용하여 로그에 정보를 기록할 수 있습니다. 앞에서 언급한 것처럼, 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 여덟 가지 로그 레벨(**emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**)에 대응하는 메서드를 제공합니다.

    use Illuminate\Support\Facades\Log;

    Log::emergency($message);
    Log::alert($message);
    Log::critical($message);
    Log::error($message);
    Log::warning($message);
    Log::notice($message);
    Log::info($message);
    Log::debug($message);

이 메서드 중 필요한 것을 호출해서 해당 레벨로 로그 메시지를 남길 수 있습니다. 기본적으로 메시지는 `logging` 구성 파일에서 설정한 기본 로그 채널로 기록됩니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Models\User;
    use Illuminate\Support\Facades\Log;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필 보여주기.
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

<a name="contextual-information"></a>
### 컨텍스트 정보

로그 메서드에 컨텍스트 데이터 배열을 전달할 수 있습니다. 이 컨텍스트 데이터는 로그 메시지와 함께 포매팅되어 표시됩니다.

    use Illuminate\Support\Facades\Log;

    Log::info('User failed to login.', ['id' => $user->id]);

때때로, 이후의 모든 로그에 포함시킬 공통의 컨텍스트 정보를 지정하고 싶을 때가 있습니다. 예를 들어, 모든 요청에 연관된 요청 ID를 로그에 남기고 싶다면, 파사드의 `withContext` 메서드를 사용할 수 있습니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Support\Facades\Log;
    use Illuminate\Support\Str;

    class AssignRequestId
    {
        /**
         * 들어오는 요청 처리.
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

<a name="writing-to-specific-channels"></a>
### 특정 채널에 작성하기

기본 채널이 아닌 다른 채널에 로그를 남기고 싶을 때는, `Log` 파사드의 `channel` 메서드를 사용하여 설정 파일에 정의된 채널을 선택적으로 사용할 수 있습니다:

    use Illuminate\Support\Facades\Log;

    Log::channel('slack')->info('Something happened!');

여러 채널로 이루어진 임시(온디맨드) 로그 스택을 만들어 로그를 남기고 싶을 경우, `stack` 메서드를 사용할 수 있습니다:

    Log::stack(['single', 'slack'])->info('Something happened!');

<a name="on-demand-channels"></a>
#### 온디맨드 채널

애플리케이션의 `logging` 설정 파일에 미리 설정하지 않은 채널도, 런타임에 옵션 배열을 제공해서 즉석에서 만들 수 있습니다. 이를 위해 `Log` 파사드의 `build` 메서드에 구성 배열을 전달하면 됩니다:

    use Illuminate\Support\Facades\Log;

    Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ])->info('Something happened!');

온디맨드 채널을 온디맨드 로그 스택에 포함시키려면, 해당 인스턴스를 `stack` 메서드에 전달된 배열에 추가하면 됩니다:

    use Illuminate\Support\Facades\Log;

    $channel = Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ]);

    Log::stack(['slack', $channel])->info('Something happened!');

<a name="monolog-channel-customization"></a>
## Monolog 채널 커스터마이징

<a name="customizing-monolog-for-channels"></a>
### 채널별 Monolog 커스터마이징

경우에 따라 기존 채널의 Monolog 구성을 완전히 제어해야 할 때가 있습니다. 예를 들어, Laravel의 기본 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현체를 적용하고 싶을 수 있습니다.

먼저, 채널의 설정에 `tap` 배열을 정의하세요. 이 배열에는 Monolog 인스턴스가 생성된 후 추가로 커스터마이징할 클래스들을 나열합니다. 이러한 tap 클래스는 프로젝트 내의 아무 폴더에나 자유롭게 생성할 수 있습니다.

    'single' => [
        'driver' => 'single',
        'tap' => [App\Logging\CustomizeFormatter::class],
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
    ],

이제 `tap` 옵션에 명시한 클래스를 다음과 같이 작성하면 됩니다. 이 클래스는 `__invoke`라는 단일 메서드만 필요하며, `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. 이 인스턴스는 내부적으로 모든 메서드 호출을 Monolog 인스턴스로 프록시합니다.

    <?php

    namespace App\Logging;

    use Monolog\Formatter\LineFormatter;

    class CustomizeFormatter
    {
        /**
         * 지정된 로거 인스턴스를 커스터마이즈.
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

> {tip} 모든 "tap" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해석되므로, 생성자 의존성이 있다면 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 존재하지만, Laravel은 이 모든 핸들러를 위한 내장 채널을 제공하지는 않습니다. 특정 Monolog 핸들러를 활용하고 싶을 때는, Laravel에 대응하는 로그 드라이버가 없더라도 `monolog` 드라이버를 사용해 채널을 쉽게 만들 수 있습니다.

`monolog` 드라이버를 사용할 때는, `handler` 설정 옵션을 이용하여 어떤 핸들러를 인스턴스화할지 지정합니다. 핸들러의 생성자 인자 역시 `with` 옵션으로 전달할 수 있습니다:

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

`monolog` 드라이버를 사용할 땐, Monolog의 `LineFormatter`가 기본 포매터로 사용됩니다. 하지만, `formatter` 및 `formatter_with` 옵션을 통해 원하는 포매터 타입 및 생성자 인수를 지정할 수 있습니다:

    'browser' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\BrowserConsoleHandler::class,
        'formatter' => Monolog\Formatter\HtmlFormatter::class,
        'formatter_with' => [
            'dateFormat' => 'Y-m-d',
        ],
    ],

만약 Monolog 핸들러가 자체적으로 포매터를 제공한다면, `formatter` 옵션 값을 `default`로 지정할 수도 있습니다:

    'newrelic' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\NewRelicHandler::class,
        'formatter' => 'default',
    ],

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog의 생성 및 구성을 완전히 컨트롤하는 완전한 커스텀 채널을 만들고 싶다면, `config/logging.php` 파일에 `custom` 드라이버 타입을 지정할 수 있습니다. 그리고 `via` 옵션에, Monolog 인스턴스를 생성할 팩토리 클래스명을 지정해야 합니다:

    'channels' => [
        'example-custom-channel' => [
            'driver' => 'custom',
            'via' => App\Logging\CreateCustomLogger::class,
        ],
    ],

이제 커스텀 드라이버 채널을 위한 클래스를 정의할 차례입니다. 이 클래스에는 Monolog 로거 인스턴스를 반환하는 `__invoke` 메서드 한 개만 필요하며, 해당 메서드는 채널의 구성 배열을 인자로 받습니다.

    <?php

    namespace App\Logging;

    use Monolog\Logger;

    class CreateCustomLogger
    {
        /**
         * 커스텀 Monolog 인스턴스 생성.
         *
         * @param  array  $config
         * @return \Monolog\Logger
         */
        public function __invoke(array $config)
        {
            return new Logger(...);
        }
    }
