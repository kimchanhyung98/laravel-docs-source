# 로깅

- [소개](#introduction)
- [구성](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 사전 준비 사항](#channel-prerequisites)
    - [폐기 예정 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구축](#building-log-stacks)
- [로그 메시지 기록](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성](#creating-custom-channels-via-factories)

<a name="introduction"></a>
## 소개

애플리케이션에서 일어나는 일을 더 잘 파악할 수 있도록, Laravel은 메시지를 파일, 시스템 에러 로그, 그리고 Slack 등 다양한 위치에 기록할 수 있는 강력한 로깅 서비스를 제공합니다. 이를 통해 팀 전체에게 실시간으로 알림을 보낼 수도 있습니다.

Laravel의 로깅은 "채널"을 기반으로 합니다. 각 채널은 로그 정보를 쓰는 특정한 방법을 나타냅니다. 예를 들어, `single` 채널은 하나의 로그 파일에 기록하고, `slack` 채널은 Slack으로 메시지를 전송합니다. 로그 메시지는 심각도(severity)에 따라 여러 개의 채널에 동시에 기록될 수 있습니다.

Laravel은 내부적으로 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용하며, 이 라이브러리는 다양한 강력한 로그 핸들러를 지원합니다. Laravel에서는 이 핸들러들의 설정과 조합이 매우 간편하여, 애플리케이션에 맞게 자유롭게 로그 관리를 커스터마이징할 수 있습니다.

<a name="configuration"></a>
## 구성

애플리케이션의 모든 로깅 동작 설정은 `config/logging.php` 설정 파일에 있습니다. 이 파일을 통해 다양한 로그 채널을 설정할 수 있으므로, 각 채널과 해당 옵션을 꼭 확인해보시기 바랍니다. 아래에서는 몇 가지 일반적인 옵션을 살펴봅니다.

Laravel은 기본적으로 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 집계하는 데 사용됩니다. 스택 구축에 대한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경(예: `production` 또는 `local`)을 기반으로 "채널 이름"을 설정합니다. 이 값을 변경하고 싶다면 채널 설정에 `name` 옵션을 추가하세요:

    'stack' => [
        'driver' => 'stack',
        'name' => 'channel-name',
        'channels' => ['single', 'slack'],
    ],

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"에 의해 동작합니다. 드라이버는 로그 메시지를 실제로 어떻게, 어디에 기록할지 결정합니다. 모든 Laravel 애플리케이션에는 아래와 같은 로그 채널 드라이버가 기본 제공됩니다. 대부분의 드라이버 엔트리는 이미 `config/logging.php` 구성 파일에 있으니, 해당 파일을 꼭 살펴보세요.

이름 | 설명
------------- | -------------
`custom` | 지정한 팩토리를 호출하여 채널을 생성하는 드라이버
`daily` | 하루마다 파일을 순환(rotating)하는 Monolog의 `RotatingFileHandler` 기반 드라이버
`errorlog` | PHP `ErrorLogHandler` 기반 Monolog 드라이버
`monolog` | 지원되는 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버
`null` | 모든 로그 메시지를 무시하는 드라이버
`papertrail` | Monolog의 `SyslogUdpHandler` 기반 드라이버
`single` | 하나의 파일 또는 경로에 기록하는 채널 (`StreamHandler`)
`slack` | Monolog의 `SlackWebhookHandler` 기반 드라이버
`stack` | 다중 채널 생성을 위한 래퍼
`syslog` | Monolog의 `SyslogHandler` 기반 드라이버

> **참고**
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징 문서](#monolog-channel-customization)를 참고하세요.

<a name="channel-prerequisites"></a>
### 채널 사전 준비 사항

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single`과 `daily` 채널에는 `bubble`, `permission`, `locking` 세 가지 선택적 옵션이 있습니다.

이름 | 설명 | 기본값
------------- | ------------- | -------------
`bubble` | 메시지 처리가 끝난 후에도 다른 채널로 버블링할지 여부 | `true`
`locking` | 기록 전 로그 파일을 잠글지 여부 | `false`
`permission` | 로그 파일 권한 | `0644`

또한, `daily` 채널의 로그 보존 정책은 `days` 옵션으로 설정할 수 있습니다.

이름 | 설명 | 기본값
------------- | ------------- | -------------
`days` | 일별 로그 파일을 보존할 일수 | `7`

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host` 및 `port` 설정이 필요합니다. 자세한 내용은 [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)를 참고하세요.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널은 `url` 설정이 필요합니다. 이 URL은 [Slack의 인커밍 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)에 설정한 주소와 일치해야 합니다.

기본적으로 Slack은 `critical` 레벨 이상의 로그만 수신하지만, `config/logging.php` 파일에서 Slack 채널 설정의 `level` 옵션을 수정해 원하는 수준을 적용할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 폐기 예정(Deprecation) 경고 로깅

PHP, Laravel, 그리고 기타 라이브러리들은 사용 중인 일부 기능이 곧 제거될 예정임을 경고하기도 합니다. 이러한 폐기 예정보고를 로그로 남기고 싶다면, 애플리케이션의 `config/logging.php` 설정 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다:

    'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

    'channels' => [
        ...
    ]

또는, `deprecations`라는 이름의 로그 채널을 직접 정의할 수도 있습니다. 이 이름의 채널이 존재하면 항상 폐기 경고 로그에 사용됩니다:

    'channels' => [
        'deprecations' => [
            'driver' => 'single',
            'path' => storage_path('logs/php-deprecation-warnings.log'),
        ],
    ],

<a name="building-log-stacks"></a>
## 로그 스택 구축

앞서 언급했듯이, `stack` 드라이버를 이용하면 여러 채널을 하나의 로그 채널로 결합하여 편리하게 사용할 수 있습니다. 프로덕션 환경에서 자주 볼 수 있는 예시 설정은 다음과 같습니다:

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

이 설정을 해부해 봅시다. 먼저, `stack` 채널은 `channels` 옵션을 통해 두 개의 채널(`syslog`, `slack`)을 집계합니다. 따라서 메시지가 기록될 때 이 두 채널 모두 로그를 기록할 기회를 갖게 됩니다. 다만, 실제로 어떤 채널에 로그가 기록될지는 메시지의 심각도("level")에 따라 결정됩니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 채널 설정에 `level` 옵션이 있는 것을 볼 수 있습니다. 이 설정은 해당 채널에 기록되려면 메시지가 갖추어야 하는 최소 "레벨"을 의미합니다. Laravel의 로깅 서비스는 [RFC 5424 스펙](https://tools.ietf.org/html/rfc5424)에서 정의된 아래의 로그 레벨을 모두 지원합니다(심각한 순서대로): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

예를 들어, `debug` 메서드를 사용해 메시지를 남긴다면:

    Log::debug('An informational message.');

위 구성에서는 `syslog` 채널은 이 메시지를 시스템 로그에 기록하지만, `critical` 이상의 에러가 아니므로 Slack에는 전달되지 않습니다. 반면 `emergency` 메시지를 남긴다면, 이 메시지는 `syslog` 및 Slack 양쪽 모두에 기록됩니다.

    Log::emergency('The system is down!');

<a name="writing-log-messages"></a>
## 로그 메시지 기록

로그를 남기고 싶을 때는 `Log` [파사드](/docs/{{version}}/facades)를 사용할 수 있습니다. 앞서 언급했듯이, 이 로거는 [RFC 5424 스펙](https://tools.ietf.org/html/rfc5424)에 정의된 8가지 로그 레벨 (**emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**)을 모두 제공합니다:

    use Illuminate\Support\Facades\Log;

    Log::emergency($message);
    Log::alert($message);
    Log::critical($message);
    Log::error($message);
    Log::warning($message);
    Log::notice($message);
    Log::info($message);
    Log::debug($message);

이 중 어떤 메서드든 호출하면 해당 레벨에 맞는 로그 메시지가 기록됩니다. 기본적으로 설정된 로그 채널(`logging` 설정 파일 참조)에 메시지가 기록됩니다.

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Models\User;
    use Illuminate\Support\Facades\Log;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필을 보여줍니다.
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

로그 메서드에 컨텍스트 데이터(배열)을 함께 전달할 수 있습니다. 컨텍스트 데이터는 로그 메시지와 함께 포매팅되어 출력됩니다.

    use Illuminate\Support\Facades\Log;

    Log::info('User failed to login.', ['id' => $user->id]);

특정 채널에서 이후 모든 로그 항목마다 포함하고 싶은 공통 컨텍스트가 있을 수도 있습니다. 예를 들어, 각 요청마다 연관되는 request ID를 기록하고 싶다면 `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다.

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

_모든_ 로깅 채널에 컨텍스트 정보를 공유하고 싶다면 `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드는 이미 생성된 모든 채널과 이후에 생성되는 채널에 컨텍스트 정보를 제공합니다. 일반적으로 이 메서드는 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출해야 합니다.

    use Illuminate\Support\Facades\Log;
    use Illuminate\Support\Str;

    class AppServiceProvider
    {
        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
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

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기

기본 채널 이외의 채널에 로그 메시지를 남기고 싶을 때는 `Log` 파사드의 `channel` 메서드를 사용하면 됩니다. 이 메서드로 원하는 채널을 지정해 로그를 기록할 수 있습니다.

    use Illuminate\Support\Facades\Log;

    Log::channel('slack')->info('Something happened!');

여러 채널로 구성된 온디맨드(즉석) 로그 스택을 생성하려면 `stack` 메서드를 사용할 수 있습니다.

    Log::stack(['single', 'slack'])->info('Something happened!');

<a name="on-demand-channels"></a>
#### 온디맨드 채널

애플리케이션의 `logging` 구성 파일에 정의하지 않고도, 런타임에 직접 채널 설정 배열을 전달해 임의의(on-demand) 채널을 생성할 수 있습니다. 이를 위해 `Log` 파사드의 `build` 메서드에 설정 배열을 넘기면 됩니다:

    use Illuminate\Support\Facades\Log;

    Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ])->info('Something happened!');

온디맨드 채널 인스턴스를, 온디맨드 로그 스택의 일원으로 포함할 수도 있습니다. 아래처럼 인스턴스를 `stack` 메서드에 배열로 넘기면 됩니다.

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

기존 채널에 대해 Monolog 설정을 완전히 제어해야 할 때가 있습니다. 예를 들어, Laravel 내장 `single` 채널에 대해 커스텀 Monolog `FormatterInterface` 구현체를 설정하고 싶을 수 있습니다.

이런 경우 채널 설정에 `tap` 배열을 정의합니다. 이 배열은 Monolog 인스턴스가 생성된 후 이를 커스터마이징(또는 "탭")할 클래스 목록을 포함합니다. 이 클래스들은 자유롭게 애플리케이션 내 임의의 디렉터리에 둘 수 있습니다.

    'single' => [
        'driver' => 'single',
        'tap' => [App\Logging\CustomizeFormatter::class],
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
    ],

이제 `tap`에서 지정한 클래스를 구현해 Monolog 인스턴스를 커스터마이징할 수 있습니다. 이 클래스는 `__invoke`라는 단일 메서드만 필요하며, `Illuminate\Log\Logger` 인스턴스를 전달받습니다. 이 인스턴스는 모든 메서드 호출을 내부 Monolog 인스턴스에 프록시합니다.

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

> **참고**
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)로 해석(resolved)되므로, 생성자 의존성 주입이 자동으로 이뤄집니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성

Monolog에는 [다양한 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있으나, Laravel은 각각에 대한 내장 채널을 제공하지 않습니다. 특정 Monolog 핸들러 인스턴스만 필요하고, 별도의 Laravel 드라이버가 없는 경우에는, `monolog` 드라이버를 사용해 손쉽게 채널을 만들 수 있습니다.

`monolog` 드라이버 사용 시, `handler` 설정에 인스턴스화할 핸들러를 지정합니다. 필요시, 생성자 매개변수는 `with` 옵션에 배열로 전달할 수 있습니다.

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

`monolog` 드라이버 사용시, Monolog의 `LineFormatter`가 기본 포매터로 쓰입니다. 하지만 `formatter`와 `formatter_with` 옵션을 이용해 포매터 타입과 생성자 전달 인수를 커스터마이징할 수 있습니다.

    'browser' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\BrowserConsoleHandler::class,
        'formatter' => Monolog\Formatter\HtmlFormatter::class,
        'formatter_with' => [
            'dateFormat' => 'Y-m-d',
        ],
    ],

핸들러가 자체 포매터를 제공하는 경우, `formatter` 옵션에 `default`를 지정할 수 있습니다.

    'newrelic' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\NewRelicHandler::class,
        'formatter' => 'default',
    ],

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog의 인스턴스화와 설정을 완전히 직접 제어하고 싶다면, `config/logging.php` 설정 파일에서 `custom` 드라이버 타입을 지정할 수 있습니다. 이때 `via` 옵션에 Monolog 인스턴스 생성을 담당할 팩토리 클래스명을 지정해야 합니다:

    'channels' => [
        'example-custom-channel' => [
            'driver' => 'custom',
            'via' => App\Logging\CreateCustomLogger::class,
        ],
    ],

이제 `custom` 드라이버를 위한 클래스를 만듭니다. 이 클래스에는 반환값이 Monolog 로거 인스턴스인 `__invoke` 메서드 하나만 필요합니다. 해당 메서드는 채널의 구성 배열을 인자로 받습니다.

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